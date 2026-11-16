# Données — Bascule

Propriétaire : **Alexis (CDO)**.

| Fichier | Rôle |
|---|---|
| [`../shared/contact.schema.json`](../shared/contact.schema.json) | **Contrat commun** : format d'un contact, utilisé par l'agent, la vérification, HubSpot et les mesures |
| `contacts.sample.json` | 20 contacts d'exemple, conformes au contrat. Ils servent à remplir l'ancien CRM et à tester chaque brique sans attendre l'agent |
| `validate_contacts.py` | Vérifie qu'un fichier de contacts respecte le contrat |
| `generate_seed.py` | Génère `supabase/seed.sql` à partir de `contacts.sample.json` |

## Le format d'un contact

| Champ | Obligatoire | Exemple |
|---|---|---|
| `legacy_id` | ✅ | `C-0001` (format `C-` + 4 chiffres) |
| `first_name` | ✅ | `Julien` |
| `last_name` | ✅ | `Moreau` |
| `email` | — | `julien.moreau@boulangerie-moreau.example` |
| `phone` | — | `+33 6 39 98 00 01` |
| `company` | — | `Boulangerie Moreau` |
| `job_title` | — | `Gérant` |
| `city` | — | `Lyon` |
| `notes` | — | `Commande hebdomadaire de flyers` ou `null` |

Un champ absent dans l'ancien CRM vaut `null`.

## Données 100 % fictives

- Les adresses e-mail utilisent le domaine réservé **`.example`** : elles ne peuvent appartenir à personne.
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
