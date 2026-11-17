"""Client HubSpot minimal (Python standard, aucune dépendance).

Propriétaire : Alexis (CDO).

Le jeton est lu dans la variable d'environnement HUBSPOT_TOKEN (clé de service HubSpot,
droits crm.objects.contacts.* et crm.schemas.contacts.*). Il ne doit jamais être écrit
dans le code ni dans Git : uniquement dans .env.local ou dans les variables Vercel.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

API = "https://api.hubapi.com"
ID_PROPERTY = "bascule_legacy_id"  # propriété unique : un contact Bascule = un legacy_id
BATCH_SIZE = 100                   # limite de l'API HubSpot pour un appel « batch »


class HubSpotError(Exception):
    def __init__(self, status: int, body: str):
        super().__init__(f"HubSpot HTTP {status} : {body[:300]}")
        self.status = status
        self.body = body


def _token() -> str:
    token = os.environ.get("HUBSPOT_TOKEN")
    if not token:
        raise RuntimeError("Variable HUBSPOT_TOKEN absente (voir pipeline/hubspot/README.md).")
    return token


def request(method: str, path: str, body: dict | None = None) -> dict:
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(
        API + path,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {_token()}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as res:
            raw = res.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        raise HubSpotError(e.code, e.read().decode("utf-8", "replace")) from None


def upsert_contacts(properties_list: list[dict]) -> dict[str, str]:
    """Crée ou met à jour des contacts, en se basant sur bascule_legacy_id.

    Relancer une migration ne crée donc jamais de doublon dans HubSpot.
    Renvoie {legacy_id: identifiant HubSpot}.
    """
    ids: dict[str, str] = {}
    for start in range(0, len(properties_list), BATCH_SIZE):
        chunk = properties_list[start:start + BATCH_SIZE]
        body = {
            "inputs": [
                {"id": p[ID_PROPERTY], "idProperty": ID_PROPERTY, "properties": p}
                for p in chunk
            ]
        }
        result = request("POST", "/crm/v3/objects/contacts/batch/upsert", body)
        for item in result.get("results", []):
            ids[item["properties"][ID_PROPERTY]] = item["id"]
    return ids


def find_bascule_contacts(limit: int = 100) -> list[dict]:
    """Liste les contacts créés par Bascule (ceux qui ont un bascule_legacy_id)."""
    body = {
        "filterGroups": [{"filters": [{"propertyName": ID_PROPERTY, "operator": "HAS_PROPERTY"}]}],
        "properties": ["firstname", "lastname", "email", ID_PROPERTY],
        "limit": limit,
    }
    return request("POST", "/crm/v3/objects/contacts/search", body).get("results", [])


def archive_contact(hubspot_id: str) -> None:
    """Supprime (archive) un contact HubSpot. Sert uniquement au nettoyage des tests."""
    request("DELETE", f"/crm/v3/objects/contacts/{hubspot_id}")
