"""Vérification des contacts extraits par l'agent, avant l'envoi vers HubSpot.

Propriétaire : Inès (CAIO).

Entrée  : une liste de contacts au format shared/contact.schema.json.
Sortie  : pour chaque contact, un rapport avec
          - status : "ok" | "warning" | "error"
          - contact : le contact nettoyé (espaces, e-mail, téléphone normalisés)
          - hubspot : les propriétés HubSpot prêtes à envoyer (voir mapping.py)
          - anomalies : la liste des problèmes trouvés

Règle de décision :
  - "error"   → la fiche N'EST PAS envoyée à HubSpot (à corriger ou relire).
  - "warning" → la fiche est envoyée, mais l'anomalie est signalée sur l'écran de suivi.
  - "ok"      → rien à signaler.

Usage :
  python pipeline/verification/verify.py data/contacts.sample.json
  python pipeline/verification/verify.py data/contacts.sample.json --json rapport.json
"""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

try:  # exécution comme module (tests) ou comme script
    from .mapping import to_hubspot
except ImportError:  # pragma: no cover
    from mapping import to_hubspot

ALLOWED_FIELDS = [
    "legacy_id", "first_name", "last_name", "email", "phone",
    "company", "job_title", "city", "notes",
]
REQUIRED_FIELDS = ["legacy_id", "first_name", "last_name"]

LEGACY_ID_RE = re.compile(r"^C-[0-9]{4}$")
EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+'-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}$")

ERROR = "error"
WARNING = "warning"


# --------------------------------------------------------------------------- #
# Petits outils de nettoyage
# --------------------------------------------------------------------------- #
def clean_text(value):
    """Supprime les espaces en trop. Une chaîne vide ou un tiret devient None."""
    if value is None:
        return None
    if not isinstance(value, str):
        value = str(value)
    value = re.sub(r"\s+", " ", value).strip()
    if value in {"", "-", "—", "N/A", "n/a", "null", "None"}:
        return None
    return value


def fold(value) -> str:
    """Clé de comparaison : minuscules, sans accents ni ponctuation."""
    if not value:
        return ""
    value = unicodedata.normalize("NFKD", value)
    value = "".join(c for c in value if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", value.lower())


def normalize_phone(raw):
    """Renvoie (téléphone au format international +33…, message d'anomalie ou None).

    Accepte : "06 39 98 00 01", "06.39.98.00.01", "+33 6 39 98 00 01",
              "0033 6 39 98 00 01", "+33 (0)6 39 98 00 01".
    """
    if raw is None:
        return None, None
    compact = raw.replace("(0)", "")
    compact = re.sub(r"[\s.\-/()]", "", compact)
    if compact.startswith("00"):
        compact = "+" + compact[2:]
    if re.fullmatch(r"0[1-9][0-9]{8}", compact):  # numéro français national
        compact = "+33" + compact[1:]
    if re.fullmatch(r"\+33[1-9][0-9]{8}", compact):
        return compact, None
    if re.fullmatch(r"\+[1-9][0-9]{7,14}", compact):  # numéro étranger plausible
        return compact, None
    return raw, f"téléphone non reconnu : « {raw} »"


def fix_case(value):
    """« MOREAU » ou « moreau » → « Moreau » (garde les noms composés)."""
    if value and (value.isupper() or value.islower()) and len(value) > 1:
        return "-".join(" ".join(w.capitalize() for w in part.split(" ")) for part in value.split("-"))
    return value


# --------------------------------------------------------------------------- #
# Vérification d'une fiche
# --------------------------------------------------------------------------- #
def verify_contact(raw: dict) -> dict:
    anomalies = []

    def flag(field, code, severity, message):
        anomalies.append({"field": field, "code": code, "severity": severity, "message": message})

    if not isinstance(raw, dict):
        return {
            "legacy_id": None, "status": ERROR, "contact": None, "hubspot": None,
            "anomalies": [{"field": None, "code": "not_an_object", "severity": ERROR,
                           "message": "la fiche n'est pas un objet JSON"}],
        }

    # 1. Champs inconnus (l'agent a inventé un champ)
    for key in raw:
        if key not in ALLOWED_FIELDS:
            flag(key, "unknown_field", WARNING, f"champ inconnu « {key} » ignoré")

    contact = {f: clean_text(raw.get(f)) for f in ALLOWED_FIELDS}

    # 2. Champs obligatoires
    for f in REQUIRED_FIELDS:
        if not contact[f]:
            flag(f, "missing_required", ERROR, f"champ obligatoire « {f} » vide")

    # 3. Identifiant de l'ancien CRM
    if contact["legacy_id"] and not LEGACY_ID_RE.match(contact["legacy_id"]):
        flag("legacy_id", "bad_legacy_id", ERROR,
             f"identifiant « {contact['legacy_id']} » invalide (attendu C-0000)")

    # 4. Majuscules des noms et villes
    for f in ("first_name", "last_name", "city"):
        fixed = fix_case(contact[f])
        if fixed != contact[f]:
            flag(f, "case_fixed", WARNING, f"casse corrigée : « {contact[f]} » → « {fixed} »")
            contact[f] = fixed

    # 5. E-mail
    if contact["email"]:
        email = contact["email"].replace(" ", "").lower()
        if email.startswith("mailto:"):
            email = email[len("mailto:"):]
        contact["email"] = email
        if not EMAIL_RE.match(email):
            flag("email", "bad_email", ERROR, f"e-mail invalide : « {email} »")
    else:
        flag("email", "missing_email", WARNING, "pas d'e-mail : HubSpot ne pourra pas dédoublonner ce contact")

    # 6. Téléphone
    if contact["phone"]:
        phone, problem = normalize_phone(contact["phone"])
        contact["phone"] = phone
        if problem:
            flag("phone", "bad_phone", WARNING, problem)

    # 7. Champs facultatifs vides (information, pas bloquant)
    for f in ("company", "city"):
        if not contact[f]:
            flag(f, "missing_optional", WARNING, f"champ « {f} » vide")

    status = ERROR if any(a["severity"] == ERROR for a in anomalies) else (
        WARNING if anomalies else "ok")
    return {
        "legacy_id": contact["legacy_id"],
        "status": status,
        "contact": contact,
        "hubspot": None if status == ERROR else to_hubspot(contact),
        "anomalies": anomalies,
    }


# --------------------------------------------------------------------------- #
# Vérification d'un lot (doublons entre fiches)
# --------------------------------------------------------------------------- #
def verify_batch(contacts: list) -> list:
    reports = [verify_contact(c) for c in contacts]

    keys = {
        "duplicate_id": lambda c: c["legacy_id"] or "",
        "duplicate_email": lambda c: c["email"] or "",
        "duplicate_phone": lambda c: c["phone"] if (c["phone"] or "").startswith("+") else "",
        "duplicate_person": lambda c: (fold(c["first_name"]) + "|" + fold(c["last_name"]) + "|"
                                       + fold(c["company"])) if c["first_name"] and c["last_name"] else "",
    }
    labels = {
        "duplicate_id": "même identifiant",
        "duplicate_email": "même e-mail",
        "duplicate_phone": "même téléphone",
        "duplicate_person": "même prénom, nom et entreprise",
    }

    for code, key_fn in keys.items():
        seen = {}
        for i, rep in enumerate(reports):
            if rep["contact"] is None:
                continue
            key = key_fn(rep["contact"])
            if not key:
                continue
            if key in seen:
                first = reports[seen[key]]
                # La 1re fiche est gardée, la suivante est bloquée (doublon).
                severity = ERROR if code in ("duplicate_id", "duplicate_email") else WARNING
                rep["anomalies"].append({
                    "field": None, "code": code, "severity": severity,
                    "message": f"doublon possible de {first['legacy_id']} ({labels[code]})",
                })
            else:
                seen[key] = i

    for rep in reports:  # recalcul du statut après les doublons
        if any(a["severity"] == ERROR for a in rep["anomalies"]):
            rep["status"], rep["hubspot"] = ERROR, None
        elif rep["anomalies"] and rep["status"] == "ok":
            rep["status"] = WARNING
    return reports


def summarize(reports: list) -> dict:
    total = len(reports)
    count = {s: sum(r["status"] == s for r in reports) for s in ("ok", WARNING, ERROR)}
    codes = {}
    for r in reports:
        for a in r["anomalies"]:
            codes[a["code"]] = codes.get(a["code"], 0) + 1
    return {
        "total": total,
        "ok": count["ok"],
        "warning": count[WARNING],
        "error": count[ERROR],
        "ready_for_hubspot": count["ok"] + count[WARNING],
        "anomalies_by_code": codes,
    }


# --------------------------------------------------------------------------- #
# Ligne de commande
# --------------------------------------------------------------------------- #
def main(argv: list) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 2
    contacts = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    reports = verify_batch(contacts)
    summary = summarize(reports)

    icons = {"ok": "✅", WARNING: "⚠️ ", ERROR: "❌"}
    for r in reports:
        print(f"{icons[r['status']]} {r['legacy_id'] or '?'}")
        for a in r["anomalies"]:
            print(f"     - [{a['severity']}] {a['message']}")
    print(f"\n{summary['total']} fiches : {summary['ok']} ok, {summary['warning']} avec avertissement, "
          f"{summary['error']} bloquées → {summary['ready_for_hubspot']} prêtes pour HubSpot.")

    if "--json" in argv:
        out = Path(argv[argv.index("--json") + 1])
        out.write_text(json.dumps({"summary": summary, "reports": reports}, ensure_ascii=False, indent=2),
                       encoding="utf-8")
        print(f"Rapport écrit dans {out}")
    return 1 if summary["error"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
