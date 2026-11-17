"""Mesures d'une migration Bascule, à partir du journal migration_log.

Propriétaire : Alexis (CDO).

Calcule :
  - le taux de réussite par fiche (envoyées dans HubSpot / traitées) ;
  - le taux de réussite par champ (ce que l'agent a lu, comparé à la vraie fiche) ;
  - le temps par fiche (moyen, médian, total) ;
  - le coût par fiche et l'extrapolation à 3 000 fiches.

Sources possibles pour le journal :
  python -m pipeline.metrics.compute --log journal.json            (export JSON de migration_log)
  python -m pipeline.metrics.compute --run-id <uuid>               (lecture directe dans Supabase)

La « vérité » (ce que chaque fiche contient vraiment) vient de data/contacts.legacy.json (base de l'ancien CRM),
complétable avec --truth <fichier.json> (ex. les cas pièges ajoutés jeudi).
"""
from __future__ import annotations

import json
import os
import statistics
import sys
import urllib.parse
import urllib.request
from pathlib import Path

from pipeline.hubspot.send import supabase_rest_url
from pipeline.verification.verify import ALLOWED_FIELDS, verify_contact

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_TRUTH = ROOT / "data" / "contacts.legacy.json"
FIELDS = [f for f in ALLOWED_FIELDS if f != "legacy_id"]   # les 8 champs lus par l'agent
SENT = {"success", "partial"}
EXTRAPOLATION = 3000


def load_truth(paths: list[Path]) -> dict[str, dict]:
    """Vraies fiches, nettoyées comme le fait la vérification (pour comparer à l'identique)."""
    truth: dict[str, dict] = {}
    for p in paths:
        for c in json.loads(p.read_text(encoding="utf-8")):
            truth[c["legacy_id"]] = verify_contact(c)["contact"]
    return truth


def _same(a, b) -> bool:
    return (a or None) == (b or None)


def compute(rows: list[dict], truth: dict[str, dict]) -> dict:
    total = len(rows)
    by_status: dict[str, int] = {}
    for r in rows:
        by_status[r["status"]] = by_status.get(r["status"], 0) + 1
    sent = sum(by_status.get(s, 0) for s in SENT)

    # --- Précision par champ : uniquement les fiches que l'agent a lues et dont on connaît la vérité
    field_ok = {f: 0 for f in FIELDS}
    compared, exact = 0, 0
    for r in rows:
        extracted, expected = r.get("extracted"), truth.get(r["legacy_id"])
        if not extracted or not expected:
            continue
        compared += 1
        all_ok = True
        for f in FIELDS:
            if _same(extracted.get(f), expected.get(f)):
                field_ok[f] += 1
            else:
                all_ok = False
        exact += all_ok

    durations = [r["duration_ms"] for r in rows if r.get("duration_ms") is not None]
    credits = [float(r["credits_used"]) for r in rows if r.get("credits_used") is not None]

    def pct(n, d):
        return round(100 * n / d, 1) if d else None

    mean_s = round(statistics.mean(durations) / 1000, 1) if durations else None
    cost = round(statistics.mean(credits), 4) if credits else None
    return {
        "fiches_traitees": total,
        "par_statut": by_status,
        "envoyees_hubspot": sent,
        "taux_reussite_fiche_pct": pct(sent, total),
        "fiches_comparees": compared,
        "fiches_100pct_exactes": exact,
        "taux_fiches_exactes_pct": pct(exact, compared),
        "precision_par_champ_pct": {f: pct(field_ok[f], compared) for f in FIELDS},
        "temps_moyen_s": mean_s,
        "temps_median_s": round(statistics.median(durations) / 1000, 1) if durations else None,
        "temps_total_min": round(sum(durations) / 60000, 1) if durations else None,
        "cout_moyen_par_fiche": cost,
        "cout_total": round(sum(credits), 4) if credits else None,
        "extrapolation_3000": {
            "cout": round(cost * EXTRAPOLATION, 2) if cost is not None else None,
            "heures_1_agent": round(mean_s * EXTRAPOLATION / 3600, 1) if mean_s else None,
            "heures_3_agents": round(mean_s * EXTRAPOLATION / 3600 / 3, 1) if mean_s else None,
        },
    }


def to_markdown(m: dict) -> str:
    def v(x, unit=""):
        return "—" if x is None else f"{x}{unit}"

    lines = [
        "| Mesure | Valeur |",
        "|---|---|",
        f"| Fiches traitées | {m['fiches_traitees']} |",
        f"| Envoyées dans HubSpot | {m['envoyees_hubspot']} ({v(m['taux_reussite_fiche_pct'], ' %')}) |",
        f"| Statuts | {', '.join(f'{k} : {n}' for k, n in sorted(m['par_statut'].items()))} |",
        f"| Fiches lues 100 % exactes | {m['fiches_100pct_exactes']} / {m['fiches_comparees']} ({v(m['taux_fiches_exactes_pct'], ' %')}) |",
        f"| Temps moyen par fiche | {v(m['temps_moyen_s'], ' s')} (médiane {v(m['temps_median_s'], ' s')}) |",
        f"| Temps total (agents cumulés) | {v(m['temps_total_min'], ' min')} |",
        f"| Coût moyen par fiche | {v(m['cout_moyen_par_fiche'], ' $')} |",
        f"| Coût total | {v(m['cout_total'], ' $')} |",
        f"| Extrapolation 3 000 fiches | {v(m['extrapolation_3000']['cout'], ' $')} · "
        f"{v(m['extrapolation_3000']['heures_1_agent'], ' h')} avec 1 agent, "
        f"{v(m['extrapolation_3000']['heures_3_agents'], ' h')} avec 3 |",
        "",
        "| Champ | Précision de lecture |",
        "|---|---|",
    ]
    lines += [f"| `{f}` | {v(p, ' %')} |" for f, p in m["precision_par_champ_pct"].items()]
    return "\n".join(lines)


def fetch_supabase_rows(run_id: str) -> list[dict]:
    key = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
    query = urllib.parse.urlencode({
        "select": "legacy_id,status,extracted,anomalies,hubspot_id,duration_ms,credits_used,error",
        "run_id": f"eq.{run_id}",
    })
    req = urllib.request.Request(
        supabase_rest_url("migration_log") + "?" + query,
        headers={"apikey": key, "Authorization": f"Bearer {key}"},
    )
    with urllib.request.urlopen(req, timeout=30) as res:
        return json.loads(res.read().decode("utf-8"))


def main(argv: list[str]) -> int:
    def arg(name):
        return argv[argv.index(name) + 1] if name in argv else None

    if arg("--log"):
        rows = json.loads(Path(arg("--log")).read_text(encoding="utf-8"))
    elif arg("--run-id"):
        rows = fetch_supabase_rows(arg("--run-id"))
    else:
        print(__doc__)
        return 2

    truth_paths = [DEFAULT_TRUTH] + [Path(argv[i + 1]) for i, a in enumerate(argv) if a == "--truth"]
    metrics = compute(rows, load_truth(truth_paths))
    print(to_markdown(metrics))
    if arg("--json"):
        Path(arg("--json")).write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\nMesures écrites dans {arg('--json')}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
