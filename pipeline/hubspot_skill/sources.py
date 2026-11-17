"""Ce que la veille regarde chez HubSpot : les propriétés des contacts et le journal des nouveautés.

- Propriétés : API HubSpot (clé HUBSPOT_TOKEN, droit crm.schemas.contacts.read).
- Nouveautés : page publique du changelog développeurs (adresse modifiable : HUBSPOT_CHANGELOG_URL).
"""
from __future__ import annotations

import hashlib
import html
import json
import os
import re
import urllib.request

CHANGELOG_URL = "https://developers.hubspot.com/changelog"


def contact_properties() -> list[dict]:
    """Propriétés des contacts du compte HubSpot : nom, libellé, type (sans valeurs de contacts)."""
    from pipeline.hubspot import client  # même client et même clé que l'envoi d'Alexis

    data = client.request("GET", "/crm/v3/properties/contacts")
    props = []
    for p in data.get("results", []):
        if p.get("hidden") or p.get("calculated"):
            continue
        props.append({
            "name": p.get("name"),
            "label": p.get("label"),
            "type": p.get("type"),
            "fieldType": p.get("fieldType"),
            "readOnly": bool((p.get("modificationMetadata") or {}).get("readOnlyValue")),
            "unique": bool(p.get("hasUniqueValue")),
        })
    return sorted(props, key=lambda p: p["name"] or "")


def schema_hash(props: list[dict]) -> str:
    """Empreinte des propriétés : si elle change, HubSpot a changé."""
    key = json.dumps([[p["name"], p["type"], p["readOnly"]] for p in props], sort_keys=True)
    return hashlib.sha256(key.encode()).hexdigest()[:16]


def changelog_text(max_chars: int = 15000) -> str:
    """Texte brut du changelog HubSpot (sans HTML), tronqué pour l'IA."""
    url = os.environ.get("HUBSPOT_CHANGELOG_URL", CHANGELOG_URL)
    req = urllib.request.Request(url, headers={"User-Agent": "Bascule-veille/1.0"})
    with urllib.request.urlopen(req, timeout=30) as res:
        raw = res.read().decode("utf-8", errors="replace")
    raw = re.sub(r"(?is)<(script|style|nav|footer|header)[^>]*>.*?</\1>", " ", raw)
    text = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    return re.sub(r"\s+", " ", text).strip()[:max_chars]
