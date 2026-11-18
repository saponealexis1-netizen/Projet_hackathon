"""Envoi des contacts vérifiés vers HubSpot + écriture du journal de migration.

Propriétaire : Alexis (CDO).

Chaîne :  contacts extraits par l'agent
          → vérification d'Inès (pipeline/verification)
          → HubSpot (fiches « ok » et « à vérifier » uniquement)
          → Supabase migration_log (une ligne par fiche, pour l'écran de suivi et les mesures)

Utilisation depuis l'orchestration (Victoria) :

    from pipeline.hubspot.send import migrate
    rows = migrate(contacts, run_id, metrics={"C-0001": {"duration_ms": 48000, "credits_used": 0.02}})

En ligne de commande :

    python -m pipeline.hubspot.send data/contacts.sample.json --dry-run
    python -m pipeline.hubspot.send data/contacts.sample.json --limit 5
"""
from __future__ import annotations

import json
import re
import os
import sys
import urllib.error
import urllib.request
import uuid
from pathlib import Path
from typing import Callable

from pipeline.hubspot import client
from pipeline.verification.verify import verify_batch

DUPLICATE_CODES = {"duplicate_id", "duplicate_email"}


def log_status(report: dict) -> str:
    """Statut de migration_log à partir du rapport de vérification."""
    if report["status"] == "ok":
        return "success"
    if report["status"] == "warning":
        return "partial"
    codes = {a["code"] for a in report["anomalies"]}
    return "duplicate" if codes & DUPLICATE_CODES else "failed"


def migrate(
    contacts: list[dict],
    run_id: str,
    metrics: dict[str, dict] | None = None,
    dry_run: bool = False,
    upsert: Callable[[list[dict]], dict[str, str]] = client.upsert_contacts,
    write_log: Callable[[list[dict]], None] | None = None,
) -> list[dict]:
    """Vérifie, envoie vers HubSpot et journalise. Renvoie les lignes de migration_log."""
    metrics = metrics or {}
    reports = verify_batch(contacts)
    to_send = [r for r in reports if r["status"] != "error"]

    hubspot_ids: dict[str, str] = {}
    send_error: str | None = None
    if to_send and not dry_run:
        try:
            hubspot_ids = upsert([r["hubspot"] for r in to_send])
        except Exception as e:  # HubSpot indisponible, jeton invalide…
            send_error = str(e)

    rows = []
    for r in reports:
        status = log_status(r)
        error = None
        hubspot_id = hubspot_ids.get(r["legacy_id"] or "")
        if r["status"] != "error" and not dry_run and not hubspot_id:
            status, error = "failed", send_error or "contact non renvoyé par HubSpot"
        m = metrics.get(r["legacy_id"] or "", {})
        rows.append({
            "run_id": run_id,
            "legacy_id": r["legacy_id"] or "?",
            "status": status,
            "extracted": r["contact"],
            "anomalies": r["anomalies"],
            "hubspot_id": hubspot_id,
            "duration_ms": m.get("duration_ms"),
            "credits_used": m.get("credits_used"),
            "error": error,
            # Preuves de l'agent (D13, D14) : fournies par l'orchestration, sinon vides
            "agent_session_id": m.get("agent_session_id"),
            "screenshot_url": m.get("screenshot_url"),
            "reread": m.get("reread"),
            "agent_started_at": m.get("agent_started_at"),
            "agent_finished_at": m.get("agent_finished_at"),
        })

    if write_log is None and not dry_run and supabase_configured():
        write_log = write_supabase_log
    if write_log and rows:
        write_log(rows)
    return rows


def migrate_one(
    contact: dict,
    run_id: str,
    previous: list[dict],
    metrics: dict | None = None,
    dry_run: bool = False,
    upsert: Callable[[list[dict]], dict[str, str]] = client.upsert_contacts,
    write_log: Callable[[list[dict]], None] | None = None,
    heal: bool = True,
) -> dict:
    """Migre UNE fiche dès qu'elle est lue (l'écran de suivi se remplit en direct).

    Si HubSpot refuse la fiche (erreur 400), le skill HubSpot se répare et la fiche est renvoyée
    une fois (pipeline/hubspot_skill/heal.py) ; le compte rendu est dans row["self_heal"].

    Les doublons sont cherchés parmi les fiches déjà traitées dans ce lancement (`previous`) :
    la première fiche vue est gardée, la suivante est signalée.
    """
    legacy_id = contact.get("legacy_id") or "?"
    rows = migrate(previous + [contact], run_id, metrics={legacy_id: metrics or {}},
                   dry_run=True, write_log=lambda r: None)
    row = rows[-1]
    if not dry_run and row["status"] in ("success", "partial"):
        report_props = verify_batch(previous + [contact])[-1]["hubspot"]
        try:
            row["hubspot_id"] = upsert([report_props]).get(legacy_id)
            if not row["hubspot_id"]:
                row["status"], row["error"] = "failed", "contact non renvoyé par HubSpot"
        except Exception as e:
            row["status"], row["error"] = "failed", str(e)
            if heal:  # Fallback (Inès) : les 2 IA corrigent le skill, puis on réessaie une fois
                row.update(self_heal_and_retry(e, contact, previous, report_props, run_id, upsert))
    if write_log is None and not dry_run and supabase_configured():
        write_log = write_supabase_log
    if write_log:
        write_log([row])
    return row


def self_heal_and_retry(error: Exception, contact: dict, previous: list[dict], payload: dict,
                        run_id: str, upsert: Callable[[list[dict]], dict[str, str]]) -> dict:
    """Fallback : réparation du skill par les 2 IA, revérification, puis un seul nouvel essai.

    Renvoie les champs de la ligne à mettre à jour (au minimum « self_heal »)."""
    from pipeline.hubspot_skill import heal

    if not heal.is_healable(error):
        return {}
    report = heal.attempt(error, payload, run_id)
    if not report["applied"]:
        return {"self_heal": {**report, "result": "non corrigée"}}

    legacy_id = contact.get("legacy_id") or "?"
    fresh = verify_batch(previous + [contact])[-1]   # revérifiée avec le skill corrigé
    if fresh["status"] == "error":                   # la règle apprise bloque désormais la fiche
        return {"status": log_status(fresh), "anomalies": fresh["anomalies"], "error": None,
                "self_heal": {**report, "result": "bloquée avant HubSpot (règle apprise)"}}
    try:
        hubspot_id = upsert([fresh["hubspot"]]).get(legacy_id)
    except Exception as e:
        return {"error": str(e), "self_heal": {**report, "result": "échec après correction"}}
    if not hubspot_id:
        return {"self_heal": {**report, "result": "échec après correction"}}
    return {"status": log_status(fresh), "hubspot_id": hubspot_id, "error": None,
            "anomalies": fresh["anomalies"], "self_heal": {**report, "result": "envoyée après correction"}}


def failed_row(run_id: str, legacy_id: str, error: str, contact: dict | None = None,
               metrics: dict | None = None) -> dict:
    """Ligne de journal pour une fiche que l'agent n'a pas pu lire."""
    m = metrics or {}
    return {
        "run_id": run_id, "legacy_id": legacy_id, "status": "failed", "extracted": contact,
        "anomalies": [], "hubspot_id": None, "duration_ms": m.get("duration_ms"),
        "credits_used": m.get("credits_used"), "error": error,
        "agent_session_id": m.get("agent_session_id"), "screenshot_url": m.get("screenshot_url"),
        "reread": m.get("reread"), "agent_started_at": m.get("agent_started_at"),
        "agent_finished_at": m.get("agent_finished_at"),
    }


# --------------------------------------------------------------------------- #
# Supabase (facultatif) : écriture dans migration_log via l'API REST
# --------------------------------------------------------------------------- #
def supabase_configured() -> bool:
    return bool(os.environ.get("SUPABASE_URL") and os.environ.get("SUPABASE_SERVICE_ROLE_KEY"))


def supabase_rest_url(table: str) -> str:
    """Adresse REST d'une table. Accepte SUPABASE_URL avec ou sans « /rest/v1 » à la fin."""
    base = os.environ["SUPABASE_URL"].strip().rstrip("/")
    base = re.sub(r"/rest/v1$", "", base)
    return f"{base}/rest/v1/{table}"


def supabase_schema() -> str:
    """Schéma Postgres de nos tables (« hackathon », pour ne pas les mélanger avec d'autres projets)."""
    return os.environ.get("SUPABASE_SCHEMA", "").strip() or "hackathon"


def supabase_headers(key: str, write: bool = False) -> dict:
    """En-têtes de l'API REST : clé, et schéma visé (Accept-Profile en lecture, Content-Profile en écriture)."""
    h = {"apikey": key, "Authorization": f"Bearer {key}", "Accept-Profile": supabase_schema()}
    if write:
        h["Content-Profile"] = supabase_schema()
    return h


def write_supabase_log(rows: list[dict]) -> None:
    key = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
    req = urllib.request.Request(
        supabase_rest_url("migration_log"),
        data=json.dumps(rows).encode("utf-8"),
        method="POST",
        headers={
            **supabase_headers(key, write=True),
            "Content-Type": "application/json",
            "Prefer": "return=minimal",
        },
    )
    try:
        urllib.request.urlopen(req, timeout=30).close()
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Supabase HTTP {e.code} : {e.read().decode('utf-8', 'replace')[:300]}") from None


# --------------------------------------------------------------------------- #
# Ligne de commande
# --------------------------------------------------------------------------- #
def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 2
    contacts = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    if "--limit" in argv:
        contacts = contacts[: int(argv[argv.index("--limit") + 1])]
    dry_run = "--dry-run" in argv
    run_id = str(uuid.uuid4())

    rows = migrate(contacts, run_id, dry_run=dry_run)

    icons = {"success": "✅", "partial": "⚠️ ", "duplicate": "🔁", "failed": "❌", "skipped": "⏭️ "}
    for row in rows:
        detail = row["error"] or ", ".join(a["code"] for a in row["anomalies"]) or ""
        print(f"{icons.get(row['status'], '?')} {row['legacy_id']}  {row['status']:<9} "
              f"HubSpot={row['hubspot_id'] or '—'}  {detail}")
    sent = sum(1 for r in rows if r["hubspot_id"])
    mode = "SIMULATION (rien n'est envoyé)" if dry_run else f"run_id {run_id}"
    print(f"\n{len(rows)} fiches · {sent} dans HubSpot · {mode}"
          f"{' · journal écrit dans Supabase' if supabase_configured() and not dry_run else ''}")
    return 1 if any(r["status"] == "failed" for r in rows) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
