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


def current_map() -> dict:
    """La correspondance du skill HubSpot (pipeline/hubspot_skill/, tenue à jour par 2 IA),
    ou FIELD_MAP si le skill est absent ou invalide."""
    try:
        from pipeline.hubspot_skill.skill import current_mapping
        return current_mapping()
    except Exception:  # le skill ne doit jamais empêcher une migration
        return FIELD_MAP


def to_hubspot(contact: dict) -> dict:
    """Renvoie les propriétés HubSpot (les champs vides ne sont pas envoyés)."""
    return {hs: contact[f] for f, hs in current_map().items() if contact.get(f)}
