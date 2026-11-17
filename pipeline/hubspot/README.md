# Envoi vers HubSpot — Bascule

Propriétaire : **Alexis (CDO)**. Python 3 standard, aucune dépendance à installer.

```
contacts extraits par l'agent
   → vérification d'Inès (pipeline/verification)
   → HubSpot : fiches « ok » et « à vérifier » uniquement
   → Supabase migration_log : une ligne par fiche (écran de suivi + mesures)
```

## Utilisation

```bash
# Simulation : vérifie et prépare, n'envoie rien
python -m pipeline.hubspot.send data/contacts.sample.json --dry-run

# Envoi réel des 5 premières fiches
python -m pipeline.hubspot.send data/contacts.sample.json --limit 5

# Tests (sans réseau : HubSpot et Supabase sont simulés)
python -m unittest pipeline.hubspot.test_send -v
```

Depuis l'orchestration (Victoria) :

```python
from pipeline.hubspot.send import migrate

rows = migrate(
    contacts,                 # liste au format shared/contact.schema.json
    run_id,                   # le même run_id que celui envoyé par l'écran de suivi
    metrics={"C-0001": {"duration_ms": 48000, "credits_used": 0.02}},  # facultatif
)
```

`migrate()` renvoie les lignes de `migration_log` et les écrit dans Supabase si les variables Supabase sont présentes.

## Variables d'environnement

À mettre dans `.env.local` (jamais commité) ou dans Vercel :

| Variable | Rôle | Obligatoire |
|---|---|---|
| `HUBSPOT_TOKEN` | Clé de service HubSpot (`pat-…`) | ✅ pour un envoi réel |
| `SUPABASE_URL` | URL du projet Supabase | Pour écrire `migration_log` |
| `SUPABASE_SERVICE_ROLE_KEY` | Clé secrète Supabase (côté serveur uniquement) | Pour écrire `migration_log` |

### Créer la clé HubSpot

HubSpot → *Paramètres* → *Développement* → **Clés → Clés de service** → *Créer*, avec les droits :
`crm.objects.contacts.read`, `crm.objects.contacts.write`, `crm.schemas.contacts.read`, `crm.schemas.contacts.write`.

## Règles de l'envoi

| Statut de vérification | Envoyée dans HubSpot ? | Statut dans `migration_log` |
|---|---|---|
| `ok` | ✅ | `success` |
| `warning` (à vérifier) | ✅ sans note (décision D10) | `partial` |
| `error` avec doublon (`duplicate_id`, `duplicate_email`) | ❌ | `duplicate` |
| `error` autre (champ obligatoire vide, e-mail invalide…) | ❌ | `failed` |
| HubSpot refuse ou ne répond pas | — | `failed` + message dans `error` |

- **Pas de doublon dans HubSpot** : l'envoi se fait en *upsert* sur la propriété unique `bascule_legacy_id`. Relancer une migration met à jour les contacts existants au lieu d'en créer de nouveaux.
- Seuls les contacts portant un `bascule_legacy_id` sont concernés : les autres contacts du compte HubSpot ne sont jamais touchés.

## Propriétés HubSpot

Créées le 17/11/2026 sur le compte de l'équipe :

| Propriété | Type | Rôle |
|---|---|---|
| `bascule_legacy_id` | Texte, **valeur unique** | Identifiant de la fiche dans l'ancien CRM (C-0001…) |
| `bascule_notes` | Texte multiligne | Notes de l'ancien CRM |

## Ce qu'on a appris (retour d'expérience)

- **HubSpot refuse les e-mails en `.example`** (« adresse e-mail invalide »). Les contacts d'exemple utilisent donc `.example.com`, aussi réservé et sans propriétaire.
- **La recherche HubSpot met quelques secondes à se mettre à jour** après une création : pour vérifier un contact juste après l'envoi, il faut le lire par son identifiant, pas par une recherche.

## Test réel (17/11/2026)

| Test | Résultat |
|---|---|
| Envoi de C-0001 | ✅ contact créé, tous les champs corrects (téléphone `+33639980001`) |
| Second envoi de C-0001 | ✅ même identifiant HubSpot : pas de doublon |
| E-mail en `.example` | ❌ refusé par HubSpot → fiche marquée `failed` avec la raison, rien de créé |
| Nettoyage | ✅ contact de test supprimé |
