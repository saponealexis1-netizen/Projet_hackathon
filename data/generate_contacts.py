"""Génère data/contacts.legacy.json : la base complète de l'ancien CRM (100 contacts fictifs).

Usage : python data/generate_contacts.py [nombre]      (100 par défaut)

- Les 20 premières fiches sont EXACTEMENT celles de data/contacts.sample.json (C-0001 à C-0020).
- Les suivantes sont générées de façon reproductible (même résultat à chaque lancement).
- Données 100 % fictives : e-mails en .example.com, téléphones dans la plage ARCEP
  réservée à la fiction (06 39 98 xx xx).
"""
import json
import random
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOTAL = int(sys.argv[1]) if len(sys.argv) > 1 else 100

FEMININS = {"Agathe", "Alice", "Amandine", "Aurélie", "Bérénice", "Céline", "Coralie", "Delphine",
            "Émilie", "Fanny", "Gaëlle", "Hélène", "Isabelle", "Jade", "Léa", "Lina", "Lucie", "Margaux",
            "Marion", "Mélanie", "Noémie", "Pauline", "Salomé", "Sandrine", "Valérie", "Yasmine", "Zoé"}
PRENOMS = ["Adrien", "Agathe", "Alice", "Amandine", "Antoine", "Aurélie", "Bastien", "Benjamin",
           "Bérénice", "Céline", "Clément", "Coralie", "Damien", "Delphine", "Émilie", "Étienne",
           "Fanny", "Florian", "Gaëlle", "Guillaume", "Hélène", "Isabelle", "Jérôme", "Jade",
           "Kévin", "Léa", "Léon", "Lina", "Louis", "Lucie", "Margaux", "Marion", "Maxence",
           "Mélanie", "Nicolas", "Noémie", "Olivier", "Pauline", "Quentin", "Rachid", "Romain",
           "Salomé", "Samuel", "Sandrine", "Sofiane", "Théo", "Valérie", "Victor", "Yasmine", "Zoé"]
NOMS = ["Arnaud", "Barbier", "Baron", "Benoît", "Bertrand", "Boyer", "Brun", "Carpentier",
        "Caron", "Charpentier", "Clément", "Collet", "Colin", "Denis", "Duval", "Faure", "Fournier",
        "Gauthier", "Gérard", "Guérin", "Henry", "Jacob", "Joly", "Laurent", "Leclerc", "Lemaire",
        "Lucas", "Marchand", "Martinez", "Masson", "Meunier", "Michel", "Noël", "Perrot", "Picard",
        "Renaud", "Rey", "Riviere", "Robin", "Rousseau", "Roussel", "Schmitt", "Simon", "Tessier",
        "Vasseur", "Vincent", "Benhamou", "Nguyen", "Traoré", "Kaddour"]
METIERS = [  # (préfixe d'entreprise, poste au masculin, poste au féminin)
    ("Boulangerie", "Gérant", "Gérante"), ("Cabinet", "Associé", "Associée"),
    ("Garage", "Responsable atelier", "Responsable atelier"), ("Agence", "Chargé de clientèle", "Chargée de clientèle"),
    ("Studio", "Directeur artistique", "Directrice artistique"), ("Atelier", "Fondateur", "Fondatrice"),
    ("Pharmacie", "Pharmacien adjoint", "Pharmacienne adjointe"), ("Immobilier", "Agent immobilier", "Agente immobilière"),
    ("Transports", "Responsable logistique", "Responsable logistique"), ("Traiteur", "Chef de cuisine", "Cheffe de cuisine"),
    ("Fleurs", "Fleuriste", "Fleuriste"), ("Optique", "Opticien", "Opticienne"),
    ("Menuiserie", "Artisan", "Artisane"), ("Conseil", "Consultant", "Consultante"),
    ("Imprimerie", "Responsable commercial", "Responsable commerciale"), ("Coiffure", "Gérant", "Gérante"),
    ("Paysage", "Paysagiste", "Paysagiste"), ("Informatique", "Technicien", "Technicienne"),
    ("Électricité", "Électricien", "Électricienne"), ("Événements", "Chef de projet", "Cheffe de projet"),
]
VILLES = ["Paris", "Lyon", "Marseille", "Toulouse", "Nice", "Nantes", "Strasbourg", "Montpellier",
          "Bordeaux", "Lille", "Rennes", "Reims", "Le Havre", "Saint-Étienne", "Toulon", "Grenoble",
          "Dijon", "Angers", "Nîmes", "Brest", "Tours", "Limoges", "Amiens", "Perpignan", "Metz",
          "Besançon", "Orléans", "Rouen", "Caen", "Nancy", "Annecy", "La Rochelle", "Pau", "Avignon"]
NOTES = ["Client depuis {an}", "Rappeler en {mois}", "Préfère être contacté par e-mail",
         "Devis envoyé le {jour}/{m:02d}", "Paiement à 30 jours", "Intéressé par l'offre pro",
         "Salon professionnel en {mois}", "Contrat de maintenance annuel", "Ancien client, à relancer",
         "Commande mensuelle", "Recommandé par un partenaire", "Facturation trimestrielle"]
MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "septembre", "octobre"]


def slug(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-")


def generate(total: int) -> list[dict]:
    base = json.loads((ROOT / "data" / "contacts.sample.json").read_text(encoding="utf-8"))
    contacts = base[:total]
    rng = random.Random(2026)  # graine fixe : résultat identique à chaque lancement
    emails = {c["email"] for c in contacts}
    persons = {(c["first_name"], c["last_name"]) for c in contacts}

    i = len(contacts)
    while len(contacts) < total:
        i += 1
        first, last = rng.choice(PRENOMS), rng.choice(NOMS)
        if (first, last) in persons:
            continue
        prefix, job_m, job_f = rng.choice(METIERS)
        job = job_f if first in FEMININS else job_m
        company = f"{prefix} {last}"
        email = f"{slug(first)}.{slug(last)}@{slug(company)}.example.com"
        if email in emails:
            continue
        persons.add((first, last))
        emails.add(email)
        note = None
        if rng.random() < 0.55:
            note = rng.choice(NOTES).format(an=rng.randint(2012, 2024), mois=rng.choice(MOIS),
                                            jour=rng.randint(1, 28), m=rng.randint(1, 12))
        n = len(contacts) + 1
        contacts.append({
            "legacy_id": f"C-{n:04d}",
            "first_name": first,
            "last_name": last,
            "email": email,
            "phone": f"+33 6 39 98 {n // 100:02d} {n % 100:02d}",
            "company": company,
            "job_title": job,
            "city": rng.choice(VILLES),
            "notes": note,
        })
    return contacts


if __name__ == "__main__":
    out = ROOT / "data" / "contacts.legacy.json"
    data = generate(TOTAL)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{out.relative_to(ROOT)} généré ({len(data)} contacts).")
