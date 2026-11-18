"""Mise à jour du skill HubSpot par deux IA qui se contrôlent.

Propriétaire : Inès (CAIO).

Trois déclencheurs :
  --champs      les propriétés des contacts HubSpot ont-elles changé ? (API HubSpot)
  --nouveautes  le changelog HubSpot annonce-t-il quelque chose qui nous concerne ?
  --erreur MSG  HubSpot a refusé une fiche : que faut-il retenir ?

Pour chacun :
  1. IA n°1 « l'analyste » propose une modification du skill (JSON) ;
  2. garde-fous du code (skill.mapping_errors) : champs du contrat, identifiant verrouillé,
     propriétés qui existent vraiment dans HubSpot, pas de doublon ;
  3. IA n°2 « le contrôleur » relit et approuve ou refuse ;
  4. appliqué seulement si les garde-fous passent ET si l'IA n°2 approuve.
     Sinon le skill ne change pas, et une alerte est notée pour l'équipe.

Usage (depuis la racine du dépôt) :
  python -m pipeline.hubspot_skill.update --champs --nouveautes
  python -m pipeline.hubspot_skill.update --erreur "Property values were not valid: email"
  python -m pipeline.hubspot_skill.update --champs --dry-run     # n'écrit rien
"""
from __future__ import annotations

import json
import re
import sys
from datetime import date
from typing import Callable

from pipeline.hubspot_skill import llm, skill as sk

Chat = Callable[[int, str, str], dict]

SYSTEM_ANALYST = """Tu es l'analyste HubSpot de Bascule, un outil qui migre des contacts d'un ancien CRM vers HubSpot.
Bascule envoie 9 champs : legacy_id, first_name, last_name, email, phone, company, job_title, city, notes.
Tu tiens à jour un « skill » : la correspondance de ces 9 champs vers les propriétés HubSpot des contacts,
les règles de ce que HubSpot refuse, les erreurs connues et les nouveautés HubSpot utiles.

Règles :
- Ne propose un changement QUE s'il est nécessaire. Sinon, renvoie une proposition vide.
- Dans « mapping », les CLÉS sont TOUJOURS l'un des 9 champs Bascule ci-dessus (ex. « job_title »),
  et les VALEURS sont TOUJOURS des propriétés HubSpot (ex. « jobtitle »). Jamais l'inverse.
  Exemple de réparation : le skill contient "job_title": "jobtitle_ancien" et HubSpot répond
  « Property "jobtitle_ancien" does not exist » ; la propriété « jobtitle » existe.
  Bonne réponse : "mapping": {"job_title": "jobtitle"}.
  Mauvaises réponses : {"jobtitle_ancien": "jobtitle"} ou {"jobtitle": "job_title"}.
- « legacy_id » doit rester « bascule_legacy_id » (identifiant unique utilisé pour éviter les doublons).
- N'utilise que des propriétés HubSpot qui existent dans la liste fournie (quand elle est fournie).
- Une nouveauté qui pourrait casser l'envoi (API retirée, changement de format) est une ALERTE pour l'équipe :
  ne la corrige pas toi-même dans la correspondance.
- Réponds UNIQUEMENT avec un objet JSON, sans texte autour :
{
  "summary": "une phrase en français : ce qui change et pourquoi (ou « rien à changer »)",
  "mapping": { "<champ Bascule>": "<propriété HubSpot>" },          // seulement les champs à changer, sinon {}
  "add_refused_email_tlds": [".exemple"],                           // sinon []
  "known_error": {"message": "...", "cause": "...", "action": "..."}, // sinon null
  "news": [{"title": "...", "date": "AAAA-MM-JJ", "summary": "...", "impact": "aucun|skill|alerte"}], // sinon []
  "alerts": ["message court pour l'équipe"]                          // sinon []
}"""

SYSTEM_REVIEWER = """Tu es le contrôleur du skill HubSpot de Bascule. Une autre IA propose une modification.
Vérifie qu'elle est nécessaire, logique, cohérente avec les informations fournies, et sans danger
(aucune donnée envoyée dans la mauvaise propriété, « legacy_id » toujours vers « bascule_legacy_id »).
Dans le doute, refuse : le skill actuel fonctionne.
Réponds UNIQUEMENT avec un objet JSON : {"approve": true|false, "reasons": ["…"]}"""


def _empty(proposal: dict) -> bool:
    return not any([proposal.get("mapping"), proposal.get("add_refused_email_tlds"),
                    proposal.get("known_error"), proposal.get("news"), proposal.get("alerts")])


def normalize_mapping(skill: dict, proposal: dict) -> list[str]:
    """Remet dans le bon sens une correspondance mal écrite par l'IA (constaté le 18/11, essai n°4).

    - clé = ancienne propriété HubSpot du skill  →  remplacée par le champ Bascule qui l'utilisait
      ex. {"jobtitle_ancien": "jobtitle"}  →  {"job_title": "jobtitle"}
    - clé = propriété HubSpot et valeur = champ Bascule (inversion complète)  →  remise à l'endroit
      ex. {"jobtitle": "job_title"}  →  {"job_title": "jobtitle"}
    Les garde-fous vérifient toujours le résultat. Renvoie la liste des corrections faites."""
    mapping = proposal.get("mapping")
    if not isinstance(mapping, dict) or not mapping:
        return []
    current = skill.get("mapping") or {}
    by_property = {hs: field for field, hs in current.items()}
    fixed, notes = {}, []
    for key, value in mapping.items():
        if key in sk.CONTRACT_FIELDS:
            fixed[key] = value
        elif key in by_property and value not in sk.CONTRACT_FIELDS:
            fixed[by_property[key]] = value
            notes.append(f"« {key} » → champ « {by_property[key]} »")
        elif value in sk.CONTRACT_FIELDS:
            fixed[value] = key
            notes.append(f"inversion « {key}: {value} » remise à l'endroit")
        else:
            fixed[key] = value  # inconnu : les garde-fous le refuseront
    proposal["mapping"] = fixed
    return notes


def merged_mapping(skill: dict, proposal: dict) -> dict:
    return {**(skill.get("mapping") or {}), **(proposal.get("mapping") or {})}


def propose_and_review(skill: dict, trigger: str, context: str, properties: set[str] | None,
                       chat: Chat = llm.chat_json) -> dict:
    """Les deux IA + les garde-fous. Renvoie {applied, proposal, review, checks, error}."""
    current = json.dumps({k: skill.get(k) for k in ("mapping", "rules", "known_errors", "hubspot_news")},
                         ensure_ascii=False)
    user = f"DÉCLENCHEUR : {trigger}\n\nSKILL ACTUEL :\n{current}\n\nINFORMATIONS :\n{context}"
    try:
        proposal = chat(1, SYSTEM_ANALYST, user)
    except llm.LLMError as e:
        return {"applied": False, "proposal": None, "review": None, "checks": [], "error": f"analyste : {e}"}

    if _empty(proposal):
        return {"applied": False, "proposal": proposal, "review": None, "checks": [], "error": None}

    normalized = normalize_mapping(skill, proposal)
    if normalized:
        proposal["normalized"] = normalized  # gardé dans le compte rendu, par transparence

    checks = sk.mapping_errors(merged_mapping(skill, proposal), properties)
    if checks:
        return {"applied": False, "proposal": proposal, "review": None, "checks": checks, "error": None}

    try:
        review = chat(2, SYSTEM_REVIEWER,
                      f"{user}\n\nPROPOSITION DE L'ANALYSTE :\n{json.dumps(proposal, ensure_ascii=False)}")
    except llm.LLMError as e:
        return {"applied": False, "proposal": proposal, "review": None, "checks": [], "error": f"contrôleur : {e}"}

    return {"applied": bool(review.get("approve")), "proposal": proposal, "review": review,
            "checks": [], "error": None}


def apply(skill: dict, result: dict, trigger: str, today: str | None = None) -> bool:
    """Écrit le résultat dans le skill. Renvoie True si le skill a changé."""
    today = today or date.today().isoformat()
    p = result.get("proposal") or {}

    if not result["applied"]:
        reason = result.get("error") or "; ".join(result.get("checks") or []) or \
            "; ".join((result.get("review") or {}).get("reasons") or [])
        if not reason:
            return False  # proposition vide : rien à faire, rien à signaler
        skill.setdefault("alerts", []).append(
            {"date": today, "message": f"[{trigger}] proposition non appliquée : {reason}"})
        return True

    changes = []
    if p.get("mapping"):
        skill["mapping"] = merged_mapping(skill, p)
        changes.append("correspondance : " + ", ".join(f"{k} → {v}" for k, v in p["mapping"].items()))
    tlds = skill.setdefault("rules", {}).setdefault("refused_email_tlds", [])
    for t in p.get("add_refused_email_tlds") or []:
        if t not in tlds:
            tlds.append(t)
            changes.append(f"e-mails {t} refusés")
    if p.get("known_error"):
        skill.setdefault("known_errors", []).append({**p["known_error"], "learned_at": today})
        changes.append("erreur apprise")
    titles = {n.get("title") for n in skill.get("hubspot_news") or []}
    for n in p.get("news") or []:
        if n.get("title") not in titles and n.get("impact") != "aucun":
            skill.setdefault("hubspot_news", []).append(n)
            changes.append(f"nouveauté : {n.get('title')}")
    for a in p.get("alerts") or []:
        skill.setdefault("alerts", []).append({"date": today, "message": a})
        changes.append("alerte pour l'équipe")
    if not changes:
        return False

    skill["version"] = int(skill.get("version") or 0) + 1
    skill["updated_at"] = today
    skill["updated_by"] = (f"IA n°1 {llm.last_model.get(1, llm.config(1)['model'])} (proposition) + "
                           f"IA n°2 {llm.last_model.get(2, llm.config(2)['model'])} (validation)")
    skill.setdefault("history", []).append({
        "version": skill["version"], "date": today, "trigger": trigger,
        "summary": p.get("summary") or "; ".join(changes),
    })
    return True


# --------------------------------------------------------------------------- #
# Les trois déclencheurs
# --------------------------------------------------------------------------- #
def check_fields(skill: dict, props: list[dict], chat: Chat = llm.chat_json) -> tuple[bool, str]:
    """Propriétés HubSpot : on n'appelle les IA que si quelque chose a changé ou ne va plus."""
    from pipeline.hubspot_skill.sources import schema_hash

    names = {p["name"] for p in props}
    h = schema_hash(props)
    problems = sk.mapping_errors(skill.get("mapping") or {}, names)
    previous = set(skill.get("schema_properties") or [])
    added, removed = sorted(names - previous), sorted(previous - names)

    if h == skill.get("schema_hash") and not problems:
        return False, "propriétés HubSpot inchangées"
    if skill.get("schema_hash") is None and not problems:
        skill["schema_hash"], skill["schema_properties"] = h, sorted(names)
        return True, f"empreinte des {len(names)} propriétés HubSpot enregistrée (correspondance valide)"

    context = json.dumps({
        "problemes_detectes_par_le_code": problems,
        "proprietes_ajoutees": added[:200], "proprietes_retirees": removed[:200],
        "proprietes_hubspot": [{k: p[k] for k in ("name", "label", "type", "readOnly")} for p in props][:400],
    }, ensure_ascii=False)
    result = propose_and_review(skill, "champs HubSpot modifiés", context, names, chat)
    changed = apply(skill, result, "champs")
    if result["applied"] or not problems:
        skill["schema_hash"], skill["schema_properties"] = h, sorted(names)
        changed = True
    return changed, _describe(result)


def check_news(skill: dict, changelog: str, chat: Chat = llm.chat_json) -> tuple[bool, str]:
    result = propose_and_review(skill, "nouveautés HubSpot (changelog)", changelog, None, chat)
    return apply(skill, result, "nouveautés"), _describe(result)


def learn_from_error(skill: dict, message: str, payload: dict | None = None,
                     chat: Chat = llm.chat_json, props: list[dict] | None = None) -> tuple[bool, str]:
    """HubSpot a refusé une fiche : les 2 IA cherchent quoi changer dans le skill.
    Avec `props` (propriétés HubSpot), les garde-fous vérifient que les propriétés proposées existent."""
    info = {"erreur_hubspot": message, "donnees_envoyees": payload}
    # Aide au diagnostic : propriétés que HubSpot dit inexistantes, et le champ Bascule qui les utilise.
    missing = sorted(set(re.findall(r'Property \\*"([\w-]+)\\*" does not exist', message)))
    if missing:
        current = skill.get("mapping") or {}
        info["proprietes_inexistantes"] = missing
        info["champs_bascule_concernes"] = {f: hs for f, hs in current.items() if hs in missing}
        info["consigne"] = ("Pour chaque champ concerné, choisis dans « proprietes_hubspot » la propriété "
                            "existante qui correspond au même sens, et mets-la dans « mapping ».")
    if props:
        info["proprietes_hubspot"] = [{k: p.get(k) for k in ("name", "label", "type")} for p in props][:400]
    context = json.dumps(info, ensure_ascii=False)
    names = {p["name"] for p in props} if props else None
    result = propose_and_review(skill, "HubSpot a refusé une fiche", context, names, chat)
    return apply(skill, result, "erreur HubSpot"), _describe(result)


def _describe(result: dict) -> str:
    if result.get("error"):
        return f"❌ {result['error']}"
    if result.get("checks"):
        return "🛑 refusé par les garde-fous : " + "; ".join(result["checks"])
    p = result.get("proposal") or {}
    if result.get("review") is None:
        return f"✅ rien à changer ({p.get('summary') or 'proposition vide'})"
    if result["applied"]:
        return f"🧠 appliqué : {p.get('summary')}"
    return "🛑 refusé par le contrôleur : " + "; ".join(result["review"].get("reasons") or [])


def main(argv: list[str]) -> int:
    if not any(a in argv for a in ("--champs", "--nouveautes", "--erreur")):
        print(__doc__)
        return 2
    from pipeline.hubspot_skill import sources

    skill = sk.load()
    if skill is None:
        print("skill.json absent ou illisible.")
        return 1
    changed = False
    if "--champs" in argv:
        c, msg = check_fields(skill, sources.contact_properties())
        changed |= c
        print(f"Champs HubSpot : {msg}")
    if "--nouveautes" in argv:
        c, msg = check_news(skill, sources.changelog_text())
        changed |= c
        print(f"Nouveautés HubSpot : {msg}")
    if "--erreur" in argv:
        c, msg = learn_from_error(skill, argv[argv.index("--erreur") + 1])
        changed |= c
        print(f"Erreur HubSpot : {msg}")

    if changed and "--dry-run" not in argv:
        sk.save(skill)
        print(f"Skill enregistré : version {skill['version']} (pipeline/hubspot_skill/SKILL.md)")
    elif changed:
        print("--dry-run : rien n'est écrit.")
    else:
        print("Skill inchangé.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
