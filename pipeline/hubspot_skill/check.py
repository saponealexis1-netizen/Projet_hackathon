"""Diagnostic du skill HubSpot : tout est-il prêt pour que les 2 IA travaillent ?

N'écrit rien, n'envoie rien dans HubSpot. Affiche ✅ / ❌ et « que faire » pour chaque point.

  python -m pipeline.hubspot_skill.check
  (ou GitHub → Actions → « Veille HubSpot (skill) » → cocher « diagnostic » → Run workflow)
"""
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request

from pipeline.hubspot_skill import llm, skill as sk

OK, KO, INFO = "✅", "❌", "ℹ️ "


def _models_list(cfg: dict) -> tuple[set[str] | None, str]:
    req = urllib.request.Request(f"{cfg['base_url']}/models", headers={"Authorization": f"Bearer {cfg['api_key']}"})
    try:
        with urllib.request.urlopen(req, timeout=30) as res:
            data = json.loads(res.read().decode())
        return {m.get("id") for m in data.get("data", [])}, ""
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code} {e.read().decode(errors='replace')[:200]}"
    except Exception as e:  # noqa: BLE001
        return None, str(e)


def run() -> int:
    problems = 0

    def line(ok: bool | None, text: str, todo: str = "") -> None:
        nonlocal problems
        icon = INFO if ok is None else (OK if ok else KO)
        print(f"{icon} {text}")
        if ok is False:
            problems += 1
            if todo:
                print(f"     → Que faire : {todo}")

    print("— Skill —")
    s = sk.load()
    line(s is not None, f"skill.json lisible (version {(s or {}).get('version')})", "restaurer skill.json depuis main")
    if s:
        errs = sk.mapping_errors(s.get("mapping") or {})
        line(not errs, "correspondance des champs valide" + (f" : {errs}" if errs else ""),
             "restaurer la correspondance de main")

    print("\n— Les 2 IA —")
    for n in (1, 2):
        cfg = llm.config(n)
        role = "l'analyste" if n == 1 else "le contrôleur"
        if not cfg["api_key"]:
            line(False, f"IA n°{n} ({role}) : aucune clé", "ajouter le secret HF_TOKEN dans GitHub")
            continue
        line(None, f"IA n°{n} ({role}) : {cfg['base_url']} · modèle {cfg['model']} · secours {cfg['fallbacks']}")
        models, err = _models_list(cfg)
        if models is None:
            line(None, f"   liste des modèles indisponible ({err}) : on teste directement")
        else:
            served = [m for m in [cfg["model"]] + cfg["fallbacks"] if m in models]
            line(bool(served), f"   modèles servis avec cette clé : {served or 'aucun de ceux prévus'}",
                 f"mettre dans SKILL_LLM{n}_MODEL un modèle de la liste {cfg['base_url']}/models")
        try:
            answer = llm.chat_json(n, "Réponds uniquement avec un objet JSON.",
                                   'Renvoie exactement {"ok": true}.', timeout=60)
            line(answer.get("ok") is True, f"   réponse de l'IA n°{n} : {answer}")
        except llm.LLMError as e:
            line(False, f"   l'IA n°{n} ne répond pas : {e}",
                 "si « clé refusée » : recréer la clé Hugging Face avec le droit « Make calls to Inference "
                 "Providers » ; si « HTTP 400/404 » : changer de modèle (SKILL_LLM%d_MODEL)" % n)

    print("\n— HubSpot —")
    try:
        from pipeline.hubspot_skill.sources import contact_properties
        props = contact_properties()
        names = {p["name"] for p in props}
        line(True, f"{len(props)} propriétés de contacts lues")
        if s:
            errs = sk.mapping_errors(s.get("mapping") or {}, names)
            line(not errs, "toutes les propriétés du skill existent dans HubSpot" + (f" : {errs}" if errs else ""),
                 "créer les propriétés manquantes dans HubSpot ou corriger le skill")
    except Exception as e:  # noqa: BLE001
        line(False, f"lecture des propriétés HubSpot impossible : {e}",
             "vérifier HUBSPOT_TOKEN et le droit crm.schemas.contacts.read")

    print("\n— Veille —")
    try:
        from pipeline.hubspot_skill.sources import changelog_text
        text = changelog_text()
        line(len(text) > 500, f"changelog HubSpot lu ({len(text)} caractères)",
             "changer HUBSPOT_CHANGELOG_URL")
    except Exception as e:  # noqa: BLE001
        line(False, f"changelog HubSpot illisible : {e}", "changer HUBSPOT_CHANGELOG_URL")

    print(f"\n{'Tout est prêt.' if not problems else f'{problems} point(s) à corriger.'}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(run())
