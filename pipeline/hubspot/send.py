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


# --------------------------------------------------------------------------- #
# Supabase (facultatif) : écriture dans migration_log via l'API REST
# --------------------------------------------------------------------------- #
def supabase_configured() -> bool:
    return bool(os.environ.get("SUPABASE_URL") and os.environ.get("SUPABASE_SERVICE_ROLE_KEY"))


def write_supabase_log(rows: list[dict]) -> None:
    key = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
    req = urllib.request.Request(
        os.environ["SUPABASE_URL"].rstrip("/") + "/rest/v1/migration_log",
        data=json.dumps(rows).encode("utf-8"),
        method="POST",
        headers={
            "apikey": key,
            "Authorization": f"Bearer {key}",
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
