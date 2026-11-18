"""Fallback en direct : quand HubSpot refuse une fiche, Bascule se répare et réessaie.

Propriétaire : Inès (CAIO). Appelé par pipeline/hubspot/send.py → migrate_one() (accord d'Alexis, 17/11).

  ❌ HubSpot refuse la fiche (erreur 400 : donnée ou propriété refusée)
  🧠 les 2 IA lisent l'erreur et corrigent le skill (mêmes garde-fous que la veille)
  🔁 la fiche est revérifiée avec le skill corrigé, puis renvoyée une fois
  ✅ résultat écrit dans migration_log.self_heal → visible sur l'écran de suivi

On ne répare PAS : un jeton invalide (401/403), une limite de débit (429), HubSpot en panne (5xx).
Garde-fous : une erreur identique n'est analysée qu'une fois par lancement (les fiches suivantes
réutilisent la correction), et au plus MAX_HEALS_PER_RUN analyses par lancement (crédits maîtrisés).
"""
from __future__ import annotations

import re
import threading

from pipeline.hubspot_skill import llm, skill as sk, update

MAX_HEALS_PER_RUN = 5

_lock = threading.Lock()
_seen: dict[tuple[str, str], dict] = {}      # (run_id, erreur normalisée) → compte rendu
_count: dict[str, int] = {}                   # run_id → nombre d'analyses par les IA


def is_healable(error: Exception | str) -> bool:
    """Seules les erreurs 400 (données refusées) peuvent être corrigées par le skill."""
    status = getattr(error, "status", None)
    if status is not None:
        return status == 400
    return bool(re.search(r"HTTP 400\b", str(error)))


def _key(message: str) -> str:
    """Même erreur, autre fiche : on retire les valeurs propres à la fiche (e-mails, nombres)."""
    m = re.sub(r"[\w.+-]+@[\w.-]+", "<email>", message.lower())
    return re.sub(r"\d+", "<n>", m)[:300]


def attempt(error: Exception | str, payload: dict | None, run_id: str,
            chat: update.Chat = llm.chat_json, props: list[dict] | None = None) -> dict:
    """Les 2 IA tentent de corriger le skill à partir de l'erreur. Renvoie le compte rendu."""
    message = str(error)
    report = {"error": message[:300], "tried": False, "applied": False, "reused": False,
              "summary": None, "skill_version": None}
    key = (run_id, _key(message))
    with _lock:
        if key in _seen:
            return {**_seen[key], "error": message[:300], "reused": True}
        if _count.get(run_id, 0) >= MAX_HEALS_PER_RUN:
            return {**report, "summary": f"limite de {MAX_HEALS_PER_RUN} réparations atteinte pour ce lancement"}
        if chat is llm.chat_json and not llm.available(1):
            return {**report, "summary": "IA non configurée (HF_TOKEN absent) : pas de réparation"}
        current = sk.load()
        if current is None:
            return {**report, "summary": "skill.json absent : pas de réparation"}
        _count[run_id] = _count.get(run_id, 0) + 1

        if props is None:
            try:
                from pipeline.hubspot_skill.sources import contact_properties
                props = contact_properties()
            except Exception:  # sans la liste, les garde-fous vérifient seulement la structure
                props = None

        before = current.get("version")
        _, summary = update.learn_from_error(current, message, payload, chat, props)
        applied = current.get("version") != before
        if applied:
            sk.save(current)
        result = {**report, "tried": True, "applied": applied, "summary": summary,
                  "skill_version": current.get("version")}
        _seen[key] = result
        return result


def reset() -> None:
    """Pour les tests : oublie les réparations déjà faites."""
    with _lock:
        _seen.clear()
        _count.clear()
