"""Vérifie qu'un fichier de contacts respecte shared/contact.schema.json.

Usage : python data/validate_contacts.py data/contacts.sample.json
"""
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
schema = json.loads((ROOT / "shared" / "contact.schema.json").read_text(encoding="utf-8"))
validator = Draft202012Validator(schema)

path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "data" / "contacts.sample.json"
contacts = json.loads(path.read_text(encoding="utf-8"))

errors = 0
ids = set()
for contact in contacts:
    cid = contact.get("legacy_id", "?")
    for err in validator.iter_errors(contact):
        errors += 1
        print(f"❌ {cid} : {err.message}")
    if cid in ids:
        errors += 1
        print(f"❌ {cid} : identifiant en double")
    ids.add(cid)

print(f"{len(contacts)} contacts vérifiés, {errors} erreur(s).")
sys.exit(1 if errors else 0)
