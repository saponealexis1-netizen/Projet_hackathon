"""Remise à zéro de HubSpot avant une démo : supprime les contacts créés par Bascule.

Propriétaire : Alexis (CDO).

Ne touche QUE les contacts qui portent un bascule_legacy_id. Les autres contacts du compte
ne sont jamais lus ni modifiés.

Usage :
  python -m pipeline.hubspot.reset            # affiche ce qui serait supprimé, ne supprime rien
  python -m pipeline.hubspot.reset --yes      # supprime pour de vrai
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from pipeline.hubspot import client

ROOT = Path(__file__).resolve().parents[2]
KNOWN_FILES = [ROOT / "data" / "contacts.legacy.json", ROOT / "data" / "contacts.pieges.json",
               ROOT / "pipeline" / "verification" / "exemples_pieges.json"]


def known_legacy_ids() -> list[str]:
    ids = set()
    for p in KNOWN_FILES:
        if p.exists():
            ids.update(c["legacy_id"] for c in json.loads(p.read_text(encoding="utf-8")))
    return sorted(ids)


def find_all() -> dict[str, dict]:
    """Contacts Bascule : lecture directe par identifiant connu + recherche (qui peut avoir du retard)."""
    found: dict[str, dict] = {}
    ids = known_legacy_ids()
    for start in range(0, len(ids), 100):
        res = client.request("POST", "/crm/v3/objects/contacts/batch/read", {
            "idProperty": client.ID_PROPERTY,
            "properties": ["firstname", "lastname", client.ID_PROPERTY],
            "inputs": [{"id": i} for i in ids[start:start + 100]],
        })
        for c in res.get("results", []):
            found[c["id"]] = c
    for c in client.find_bascule_contacts(limit=100):
        found.setdefault(c["id"], c)
    return found


def main(argv: list[str]) -> int:
    contacts = find_all()
    for c in sorted(contacts.values(), key=lambda c: c["properties"].get(client.ID_PROPERTY) or ""):
        p = c["properties"]
        print(f"  {p.get(client.ID_PROPERTY)}  {p.get('firstname')} {p.get('lastname')}  (HubSpot {c['id']})")
    print(f"{len(contacts)} contact(s) Bascule dans HubSpot.")

    if "--yes" not in argv:
        print("Simulation : rien n'est supprimé. Relancer avec --yes pour supprimer.")
        return 0
    ids = list(contacts)
    for start in range(0, len(ids), 100):
        client.request("POST", "/crm/v3/objects/contacts/batch/archive",
                       {"inputs": [{"id": i} for i in ids[start:start + 100]]})
    print(f"✅ {len(ids)} contact(s) supprimé(s). La vue « Bascule » de HubSpot est vide.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
