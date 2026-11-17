"""Le skill HubSpot : ce que Bascule sait de HubSpot, dans un fichier qui se met à jour tout seul.

Propriétaire : Inès (CAIO).

- skill.json : la version lue par le code (correspondance des champs, règles, erreurs connues…).
- SKILL.md   : la même chose, lisible par un humain (générée par render_markdown()).

Le code d'envoi ne lit QUE la partie validée du skill. Si le fichier est absent ou abîmé,
on revient à la correspondance écrite à la main (pipeline/verification/mapping.py) : rien ne casse.
"""
from __future__ import annotations

import json
from pathlib import Path

SKILL_PATH = Path(__file__).with_name("skill.json")
SKILL_MD_PATH = Path(__file__).with_name("SKILL.md")

# Les 9 champs du contrat commun (shared/contact.schema.json).
CONTRACT_FIELDS = ["legacy_id", "first_name", "last_name", "email", "phone",
                   "company", "job_title", "city", "notes"]

# Champs que les IA n'ont PAS le droit de changer : l'envoi fait un upsert sur bascule_legacy_id.
LOCKED = {"legacy_id": "bascule_legacy_id"}

# Correspondance de secours (identique à la version 1 du skill).
FALLBACK_MAPPING = {
    "legacy_id": "bascule_legacy_id", "first_name": "firstname", "last_name": "lastname",
    "email": "email", "phone": "phone", "company": "company", "job_title": "jobtitle",
    "city": "city", "notes": "bascule_notes",
}


def load(path: Path = SKILL_PATH) -> dict | None:
    """Le skill, ou None s'il est absent ou illisible."""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def save(skill: dict, path: Path = SKILL_PATH, md_path: Path | None = SKILL_MD_PATH) -> None:
    path.write_text(json.dumps(skill, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if md_path is not None:
        md_path.write_text(render_markdown(skill), encoding="utf-8")


def mapping_errors(mapping: dict, hubspot_properties: set[str] | None = None) -> list[str]:
    """Garde-fous appliqués à toute correspondance, même validée par les deux IA."""
    errors = []
    if not isinstance(mapping, dict):
        return ["la correspondance n'est pas un objet"]
    missing = [f for f in CONTRACT_FIELDS if not mapping.get(f)]
    if missing:
        errors.append(f"champs sans destination : {', '.join(missing)}")
    unknown = [f for f in mapping if f not in CONTRACT_FIELDS]
    if unknown:
        errors.append(f"champs inconnus du contrat : {', '.join(unknown)}")
    for f, hs in LOCKED.items():
        if mapping.get(f) != hs:
            errors.append(f"« {f} » doit rester « {hs} » (identifiant de l'upsert)")
    targets = [v for v in mapping.values() if v]
    if len(targets) != len(set(targets)):
        errors.append("deux champs envoyés vers la même propriété HubSpot")
    if hubspot_properties is not None:
        absent = [v for v in targets if isinstance(v, str) and v not in hubspot_properties]
        if absent:
            errors.append(f"propriétés absentes de HubSpot : {', '.join(absent)}")
    return errors


def current_mapping() -> dict:
    """La correspondance à utiliser : celle du skill si elle est valide, sinon celle de secours."""
    skill = load()
    mapping = (skill or {}).get("mapping")
    if mapping and not mapping_errors(mapping):
        return mapping
    return FALLBACK_MAPPING


def refused_email_tlds() -> list[str]:
    """Extensions d'e-mail que HubSpot refuse (ex. « .example »)."""
    tlds = ((load() or {}).get("rules") or {}).get("refused_email_tlds") or []
    return [t.lower() if t.startswith(".") else "." + t.lower() for t in tlds if isinstance(t, str) and t]


def render_markdown(skill: dict) -> str:
    """SKILL.md : le mode d'emploi de HubSpot, tel que Bascule le connaît aujourd'hui."""
    lines = [
        "# Skill HubSpot — Bascule",
        "",
        f"> **Version {skill.get('version')}** du {skill.get('updated_at')} · {skill.get('updated_by')}",
        "> Fichier **généré** à partir de `skill.json` : ne pas le modifier à la main.",
        "> Mis à jour par la veille automatique (2 IA qui se contrôlent), voir [README](README.md).",
        "",
        "## 1. Où ranger chaque information",
        "",
        "| Champ Bascule | Propriété HubSpot |",
        "|---|---|",
    ]
    for f in CONTRACT_FIELDS:
        hs = (skill.get("mapping") or {}).get(f, "—")
        lock = " 🔒" if f in LOCKED else ""
        lines.append(f"| `{f}` | `{hs}`{lock} |")
    rules = skill.get("rules") or {}
    lines += ["", "## 2. Ce que HubSpot refuse", ""]
    tlds = rules.get("refused_email_tlds") or []
    lines.append(f"- E-mails dont l'extension est : {', '.join(f'`{t}`' for t in tlds)} → bloqués dès la vérification."
                 if tlds else "- Rien de connu pour l'instant.")
    lines += ["", "## 3. Erreurs déjà rencontrées", ""]
    for e in skill.get("known_errors") or []:
        lines.append(f"- **{e.get('message')}** ({e.get('learned_at')}) : {e.get('cause')} → {e.get('action')}")
    if not skill.get("known_errors"):
        lines.append("- Aucune.")
    lines += ["", "## 4. Nouveautés HubSpot qui nous concernent", ""]
    for n in skill.get("hubspot_news") or []:
        lines.append(f"- {n.get('date', '?')} — **{n.get('title')}** : {n.get('summary')} *(impact : {n.get('impact')})*")
    if not skill.get("hubspot_news"):
        lines.append("- Aucune pour l'instant.")
    lines += ["", "## 5. Alertes pour l'équipe", ""]
    for a in skill.get("alerts") or []:
        lines.append(f"- ⚠️ {a.get('date')} — {a.get('message')}")
    if not skill.get("alerts"):
        lines.append("- Aucune.")
    lines += ["", "## 6. Historique", "", "| Version | Date | Déclencheur | Ce qui a changé |", "|---|---|---|---|"]
    for h in reversed(skill.get("history") or []):
        lines.append(f"| {h.get('version')} | {h.get('date')} | {h.get('trigger')} | {h.get('summary')} |")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":  # python -m pipeline.hubspot_skill.skill → régénère SKILL.md
    s = load()
    if s is None:
        raise SystemExit("skill.json absent ou illisible")
    SKILL_MD_PATH.write_text(render_markdown(s), encoding="utf-8")
    print(f"SKILL.md régénéré (version {s.get('version')})")
