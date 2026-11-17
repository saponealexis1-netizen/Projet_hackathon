"""Génère lib/demo-data.json : les 20 contacts d'exemple + 4 cas pièges, passés par la vraie vérification.

Usage (depuis la racine du dépôt) : python apps/dashboard/scripts/make_demo_data.py
"""
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from pipeline.verification.verify import verify_batch  # noqa: E402

contacts = json.loads((ROOT / "data/contacts.sample.json").read_text(encoding="utf-8"))
pieges = json.loads((ROOT / "pipeline/verification/exemples_pieges.json").read_text(encoding="utf-8"))
contacts += [c for c in pieges if c["legacy_id"] != "C-0001"]

random.seed(17)
rows = []
for r in verify_batch(contacts):
    status = {"ok": "success", "warning": "partial", "error": "failed"}[r["status"]]
    if any(a["code"].startswith("duplicate") and a["severity"] == "error" for a in r["anomalies"]):
        status = "duplicate"
    rows.append({
        "legacy_id": r["legacy_id"],
        "status": status,
        "extracted": r["contact"],
        "anomalies": r["anomalies"],
        "duration_ms": random.randint(21_000, 42_000),  # mesuré : ~31 s par fiche
        "credits_used": round(random.uniform(0.009, 0.024), 4),  # coût mesuré : ~0,015 $ par fiche
    })
out = ROOT / "apps/dashboard/lib/demo-data.json"
out.write_text(json.dumps(rows, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"{len(rows)} fiches écrites dans {out}")
