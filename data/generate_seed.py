"""Génère supabase/seed.sql à partir de data/contacts.sample.json.

Usage : python data/generate_seed.py
À relancer chaque fois que contacts.sample.json change.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COLS = ["legacy_id", "first_name", "last_name", "email", "phone",
        "company", "job_title", "city", "notes"]


def sql_value(value):
    if value is None:
        return "null"
    return "'" + str(value).replace("'", "''") + "'"


contacts = json.loads((ROOT / "data" / "contacts.sample.json").read_text(encoding="utf-8"))
rows = ",\n".join(
    "  (" + ", ".join(sql_value(c.get(k)) for k in COLS) + ")" for c in contacts
)
updates = ",\n  ".join(f"{k} = excluded.{k}" for k in COLS[1:])

sql = f"""-- Bascule — chargement des {len(contacts)} contacts d'exemple dans legacy_contacts.
-- Fichier GÉNÉRÉ depuis data/contacts.sample.json par data/generate_seed.py : ne pas modifier à la main.
-- À lancer APRÈS la migration des tables. Peut être relancé sans créer de doublons.

insert into public.legacy_contacts ({", ".join(COLS)}) values
{rows}
on conflict (legacy_id) do update set
  {updates};
"""

(ROOT / "supabase" / "seed.sql").write_text(sql, encoding="utf-8")
print(f"supabase/seed.sql généré ({len(contacts)} contacts).")
