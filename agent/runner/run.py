"""Orchestration Bascule : agent H → vérification → HubSpot → journal.

Propriétaire : Alexis.

Pour chaque fiche demandée :
  1. un agent H Company ouvre l'ancien CRM et lit la fiche (zéro configuration, D12) ;
  2. la vérification d'Inès contrôle le résultat ;
  3. si un champ est en anomalie (e-mail, téléphone…), l'agent est renvoyé le relire (D13) ;
  4. migrate() envoie dans HubSpot et écrit migration_log (temps, coût, capture d'écran : D14).

Usage :
  python -m agent.runner.run --url https://ancien-crm.example --ids C-0001,C-0002
  python -m agent.runner.run --url https://ancien-crm.example --first 5
  python -m agent.runner.run --url ... --first 5 --dry-run     (n'envoie rien dans HubSpot)

Variables : HAI_API_KEY (H Company), HUBSPOT_TOKEN, SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY (facultatif).
"""
from __future__ import annotations

import json
import sys
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from agent.runner import hclient
from agent.runner.prompts import ANSWER_FORMAT, FIELD_LABELS, FIELDS, READ_RECORD, REREAD_FIELD
from pipeline.verification.verify import verify_contact

ROOT = Path(__file__).resolve().parents[2]
REREAD_CODES = {"bad_email", "bad_phone", "missing_required"}   # anomalies qui justifient une relecture


EMPTY = {"", "none", "null", "n/a", "-"}


def _blank(value) -> bool:
    return value is None or (isinstance(value, str) and value.strip().lower() in EMPTY)


def normalize_answer(answer, legacy_id: str) -> tuple[dict, str | None]:
    """Transforme la réponse de l'agent en contact + éventuelle erreur, avec filets de sécurité.

    - réponse sous forme de texte JSON → décodée ;
    - fiche entière rangée dans un champ (ex. « notes ») → récupérée ;
    - « None », « null », "" → absent ;
    - fiche différente de celle demandée → erreur.
    """
    if isinstance(answer, str):
        try:
            answer = json.loads(answer)
        except ValueError:
            answer = {}
    answer = answer if isinstance(answer, dict) else {}
    for value in list(answer.values()):            # fiche JSON cachée dans un champ
        if isinstance(value, str) and value.lstrip().startswith("{") and '"legacy_id"' in value:
            try:
                inner = json.loads(value)
            except ValueError:
                continue
            if isinstance(inner, dict) and inner.get("legacy_id") == legacy_id:
                answer = {**answer, **inner}
                break
    contact = {f: (None if _blank(answer.get(f)) else str(answer.get(f)).strip()) for f in FIELDS}
    error = None if _blank(answer.get("error")) else str(answer["error"]).strip()
    if contact["legacy_id"] and contact["legacy_id"] != legacy_id and not error:
        error = f"l'agent a renvoyé la fiche {contact['legacy_id']} au lieu de {legacy_id}"
    if not error and all(contact[f] is None for f in FIELDS if f != "legacy_id"):
        error = "réponse vide"
    contact["legacy_id"] = legacy_id
    return contact, error


def read_record(url: str, legacy_id: str, run_id: str, task: str | None = None) -> dict:
    """Lance un agent sur une fiche et attend sa réponse."""
    task = task or READ_RECORD.format(url=url, legacy_id=legacy_id)
    session_id = hclient.create_session(task, ANSWER_FORMAT, start_url=url, group_id=f"bascule-{run_id}")
    result = hclient.wait(session_id)
    result["contact"], result["agent_error"] = normalize_answer(result["answer"], legacy_id)
    if result.get("status") != "completed" and not result["agent_error"]:
        result["agent_error"] = result.get("error") or f"session {result.get('status')}"
    return result


def reread_if_needed(url: str, run_id: str, result: dict) -> dict:
    """D13 : si la vérification signale un champ suspect, l'agent retourne le relire une fois."""
    report = verify_contact(result["contact"])
    suspects = [a for a in report["anomalies"] if a["code"] in REREAD_CODES and a["field"]]
    if not suspects or result.get("agent_error"):
        return result
    a = suspects[0]
    task = REREAD_FIELD.format(url=url, legacy_id=result["contact"]["legacy_id"],
                               field_label=FIELD_LABELS.get(a["field"], a["field"]),
                               previous=result["contact"].get(a["field"]), reason=a["message"])
    second = read_record(url, result["contact"]["legacy_id"], run_id, task=task)
    if second.get("agent_error"):
        result["reread"] = {"field": a["field"], "before": result["contact"].get(a["field"]),
                            "after": None, "error": second["agent_error"]}
        return result
    second["reread"] = {"field": a["field"], "before": result["contact"].get(a["field"]),
                        "after": second["contact"].get(a["field"])}
    for k in ("cost_usd", "duration_ms", "steps"):   # on additionne les deux lectures
        if result.get(k) is not None and second.get(k) is not None:
            second[k] = second[k] + result[k]
    second["screenshots"] = result.get("screenshots", []) + second.get("screenshots", [])
    return second


def process(url: str, legacy_id: str, run_id: str, reread: bool) -> dict:
    try:
        result = read_record(url, legacy_id, run_id)
        if result.get("agent_error") and "au lieu de" in result["agent_error"]:
            # Mauvaise fiche ouverte (ex. C-0007 au lieu de C-0070) : une seconde tentative
            first_error = result["agent_error"]
            result = read_record(url, legacy_id, run_id)
            result["retry"] = first_error
        if reread:
            result = reread_if_needed(url, run_id, result)
    except Exception as e:  # agent en panne, quota, réseau…
        result = {"contact": {"legacy_id": legacy_id}, "status": "failed", "error": str(e),
                  "cost_usd": None, "duration_ms": None, "screenshots": []}
    return result


def main(argv: list[str]) -> int:
    def arg(name):
        return argv[argv.index(name) + 1] if name in argv else None

    url = arg("--url")
    if not url:
        print(__doc__)
        return 2
    if arg("--ids"):
        ids = arg("--ids").split(",")
    else:
        base = json.loads((ROOT / "data" / "contacts.legacy.json").read_text(encoding="utf-8"))
        ids = [c["legacy_id"] for c in base[: int(arg("--first") or 1)]]
    run_id = arg("--run-id") or str(uuid.uuid4())
    parallel = int(arg("--parallel") or 3)
    dry_run = "--dry-run" in argv

    print(f"Migration {run_id} : {len(ids)} fiche(s), {parallel} agent(s) en parallèle, ancien CRM {url}")
    with ThreadPoolExecutor(max_workers=parallel) as pool:
        results = list(pool.map(lambda i: process(url, i, run_id, "--no-reread" not in argv), ids))

    for r in results:
        c = r["contact"]
        extra = f" · relu : {r['reread']['field']} « {r['reread']['before']} » → « {r['reread']['after']} »" if r.get("reread") else ""
        cost = f"{r['cost_usd']:.4f} $" if r.get("cost_usd") is not None else "—"
        dur = f"{r['duration_ms'] / 1000:.0f} s" if r.get("duration_ms") else "—"
        print(f"  {c['legacy_id']}  agent={r.get('status')}  {dur}  {cost}  "
              f"{c.get('first_name')} {c.get('last_name')} <{c.get('email')}>"
              f"{' · ' + str(r.get('agent_error') or r.get('error')) if (r.get('agent_error') or r.get('error')) else ''}{extra}")

    from pipeline.hubspot.send import migrate  # import tardif : HubSpot seulement si on arrive ici
    ok = [r for r in results if r.get("status") == "completed" and not r.get("agent_error")]
    metrics = {r["contact"]["legacy_id"]: {
        "duration_ms": r.get("duration_ms"),
        "credits_used": r.get("cost_usd"),
        "agent_session_id": r.get("session_id"),
        "screenshot_url": (r.get("screenshots") or [None])[-1],
        "reread": r.get("reread"),
    } for r in ok}
    rows = migrate([r["contact"] for r in ok], run_id, metrics=metrics, dry_run=dry_run)
    sent = sum(1 for row in rows if row["hubspot_id"])
    print(f"\n{len(ok)}/{len(ids)} fiches lues par l'agent · {sent} dans HubSpot"
          f"{' (simulation)' if dry_run else ''} · run_id {run_id}")
    out = ROOT / "agent" / "runner" / "last_run.json"
    out.write_text(json.dumps({"run_id": run_id, "url": url, "results": results, "log": rows},
                              ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    print(f"Détail complet : {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
