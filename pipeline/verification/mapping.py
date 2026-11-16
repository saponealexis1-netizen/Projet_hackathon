"""Correspondance entre un contact Bascule et les propriétés d'un contact HubSpot.

Propriétaire : Inès (CAIO). Consommé par : Alexis (pipeline/hubspot/).

Les propriétés HubSpot standard d'un contact sont : firstname, lastname, email,
phone, company, jobtitle, city.

Deux champs n'ont pas d'équivalent standard ; ils demandent des propriétés
personnalisées à créer une fois dans HubSpot (Paramètres → Propriétés → Contact) :
  - legacy_id → bascule_legacy_id  (garder le lien avec la fiche d'origine)
  - notes     → bascule_notes      (texte multiligne)
"""

FIELD_MAP = {
    "first_name": "firstname",
    "last_name": "lastname",
    "email": "email",
    "phone": "phone",
    "company": "company",
    "job_title": "jobtitle",
    "city": "city",
    "legacy_id": "bascule_legacy_id",  # propriété personnalisée
    "notes": "bascule_notes",          # propriété personnalisée
}


def to_hubspot(contact: dict) -> dict:
    """Renvoie les propriétés HubSpot (les champs vides ne sont pas envoyés)."""
    return {hs: contact[f] for f, hs in FIELD_MAP.items() if contact.get(f)}
