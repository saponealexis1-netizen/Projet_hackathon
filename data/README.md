# Données — Bascule

Propriétaire : **Alexis (CDO)**.

| Fichier | Rôle |
|---|---|
| [`../shared/contact.schema.json`](../shared/contact.schema.json) | **Contrat commun** : format d'un contact, utilisé par l'agent, la vérification, HubSpot et les mesures |
| `contacts.legacy.json` | **Base complète de l'ancien CRM : 100 contacts fictifs** (C-0001 à C-0100). C'est elle qui est chargée dans Supabase (`legacy_contacts`) |
| `contacts.pieges.json` | **5 fiches pièges** (C-0101 à C-0105) ajoutées à l'ancien CRM le 17/11 : doublon, e-mail invalide, prénom manquant, téléphone incomplet, majuscules. Elles servent à montrer la vérification et la relecture en action |
| `contacts.sample.json` | Les 20 premiers contacts (identiques à C-0001 à C-0020), utilisés par les tests de l'équipe |
| `generate_contacts.py` | Génère `contacts.legacy.json` (reproductible : même résultat à chaque lancement) |
| `validate_contacts.py` | Vérifie qu'un fichier de contacts respecte le contrat |
| `generate_seed.py` | Génère `supabase/seed.sql` à partir de `contacts.legacy.json` |

## Le format d'un contact

| Champ | Obligatoire | Exemple |
|---|---|---|
| `legacy_id` | ✅ | `C-0001` (format `C-` + 4 chiffres) |
| `first_name` | ✅ | `Julien` |
| `last_name` | ✅ | `Moreau` |
| `email` | — | `julien.moreau@boulangerie-moreau.example.com` |
| `phone` | — | `+33 6 39 98 00 01` |
| `company` | — | `Boulangerie Moreau` |
| `job_title` | — | `Gérant` |
| `city` | — | `Lyon` |
| `notes` | — | `Commande hebdomadaire de flyers` ou `null` |

Un champ absent dans l'ancien CRM vaut `null`.

## Données 100 % fictives

- Les adresses e-mail se terminent par **`.example.com`**, un domaine réservé : elles ne peuvent appartenir à personne. (Le domaine `.example` seul est refusé par HubSpot.)
- Les numéros utilisent la plage **06 39 98 xx xx**, réservée par l'ARCEP aux œuvres de fiction.
- Les noms et entreprises sont inventés.

Les cas pièges (doublons, champs vides, formats bizarres) seront ajoutés jeudi, dans un fichier séparé, avec Inès.

## Vérifier un fichier

```bash
pip install jsonschema
```

```bash
python data/validate_contacts.py data/contacts.sample.json
```
