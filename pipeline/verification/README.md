# Vérification — Bascule

Propriétaire : **Inès (CAIO)**.

Contrôle chaque contact extrait par l'agent **avant** l'envoi vers HubSpot : nettoyage, mapping des champs, doublons et anomalies. Aucune dépendance à installer (Python 3 standard).

```
Agent H ──► contacts JSON ──► verify_batch() ──► rapports ──► HubSpot (Alexis)
                                                     └──────► migration_log + écran de suivi
```

## Utilisation

```bash
# Contacts d'exemple d'Alexis (tout doit passer)
python pipeline/verification/verify.py data/contacts.sample.json

# Démo des cas pièges
python pipeline/verification/verify.py pipeline/verification/exemples_pieges.json

# Rapport complet en JSON
python pipeline/verification/verify.py data/contacts.sample.json --json rapport.json

# Tests
python -m unittest pipeline.verification.test_verify -v
```

Depuis du code Python :

```python
from pipeline.verification.verify import verify_batch, summarize
reports = verify_batch(contacts)         # un rapport par contact
a_envoyer = [r["hubspot"] for r in reports if r["status"] != "error"]
```

## Statut d'une fiche

| Statut | Signification | Envoyée à HubSpot ? |
|---|---|---|
| `ok` | Rien à signaler | ✅ |
| `warning` | Corrigée ou incomplète, à signaler sur l'écran de suivi | ✅ |
| `error` | Bloquante : à relire ou corriger | ❌ |

## Règles appliquées

| Code | Contrôle | Gravité |
|---|---|---|
| `missing_required` | Prénom, nom ou identifiant vide | ❌ error |
| `bad_legacy_id` | Identifiant différent de `C-0000` | ❌ error |
| `bad_email` | E-mail mal formé | ❌ error |
| `duplicate_id` | Même identifiant qu’une fiche précédente | ❌ error |
| `duplicate_email` | Même e-mail qu'une fiche précédente | ❌ error |
| `duplicate_person` | Même prénom + nom + entreprise (accents et majuscules ignorés) | ⚠️ warning |
| `duplicate_phone` | Même téléphone qu'une fiche précédente | ⚠️ warning |
| `missing_email` | Pas d'e-mail (HubSpot ne pourra pas dédoublonner) | ⚠️ warning |
| `bad_phone` | Téléphone non reconnu (gardé tel quel) | ⚠️ warning |
| `case_fixed` | `MOREAU` → `Moreau`, `lyon` → `Lyon` | ⚠️ warning |
| `missing_optional` | Entreprise ou ville vide | ⚠️ warning |
| `unknown_field` | Champ inventé par l'agent (ignoré) | ⚠️ warning |

Nettoyages automatiques : espaces en trop, `-` / `N/A` traités comme vides, e-mail en minuscules, téléphone au format international (`06 39 98 00 01` → `+33639980001`).

En cas de doublon, **la première fiche est gardée**, la suivante est signalée.

## Mapping vers HubSpot

Voir [`mapping.py`](mapping.py).

| Bascule | HubSpot |
|---|---|
| `first_name` | `firstname` |
| `last_name` | `lastname` |
| `email` | `email` |
| `phone` | `phone` |
| `company` | `company` |
| `job_title` | `jobtitle` |
| `city` | `city` |
| `legacy_id` | `bascule_legacy_id` *(propriété personnalisée à créer)* |
| `notes` | `bascule_notes` *(propriété personnalisée à créer)* |

> ⚠️ **Pour Alexis** : `bascule_legacy_id` et `bascule_notes` doivent être créées une fois dans HubSpot (Paramètres → Propriétés → Contact), sinon l'API refuse le contact.
