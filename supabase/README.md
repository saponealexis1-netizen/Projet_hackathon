# Supabase — Bascule

Propriétaire : **Alexis (CDO)**.

Supabase n'est **pas** le CRM cible (c'est HubSpot). Il sert à deux choses :

| Table | Rôle | Qui lit / écrit |
|---|---|---|
| `legacy_contacts` | Base **cachée** de l'ancien CRM simulé (20 contacts fictifs) | L'ancien CRM la lit côté serveur. **L'agent H n'y a pas accès** : il passe par l'écran. |
| `migration_log` | Journal de migration : **une ligne par fiche traitée** | L'orchestration écrit ; les mesures et l'écran de suivi lisent. |

## Fichiers

| Fichier | Contenu |
|---|---|
| `migrations/20261117090000_init_tables.sql` | Création des 2 tables + sécurité (RLS) |
| `seed.sql` | Chargement des 20 contacts de `data/contacts.sample.json` (généré par `data/generate_seed.py`) |

## Installation (5 minutes, une seule fois)

1. Ouvrir le projet Supabase → **SQL Editor** → **New query**.
2. Coller le contenu de `migrations/20261117090000_init_tables.sql` → **Run**.
3. Nouvelle requête : coller le contenu de `seed.sql` → **Run**.
4. Vérifier :
   ```sql
   select count(*) from legacy_contacts;   -- doit afficher 20
   ```
5. **Table Editor** : les deux tables `legacy_contacts` et `migration_log` apparaissent, avec le badge RLS activé.

Les deux scripts peuvent être relancés sans risque : ils ne créent ni doublon ni erreur.

## Colonnes de `migration_log`

| Colonne | Type | Exemple |
|---|---|---|
| `id` | nombre auto | `1` |
| `run_id` | uuid | identique pour toutes les fiches d'un même lancement |
| `legacy_id` | texte | `C-0001` |
| `status` | texte | `success`, `partial`, `failed`, `duplicate` ou `skipped` |
| `extracted` | JSON | le contact lu par l'agent (format `shared/contact.schema.json`) |
| `anomalies` | JSON | `[]` ou la liste des anomalies trouvées par la vérification |
| `hubspot_id` | texte | identifiant du contact créé dans HubSpot |
| `duration_ms` | entier | `4200` (temps de traitement de la fiche) |
| `credits_used` | nombre | crédits Agent API consommés |
| `error` | texte | message d'erreur éventuel |
| `created_at` | date | rempli automatiquement |

## Sécurité

- **RLS activée sur les deux tables, sans aucune politique publique** : avec la clé publique (`anon` / *publishable*), on ne voit **rien**.
- Les applications lisent et écrivent **côté serveur** avec la clé **service_role** (ou *secret key*).
- Cette clé va uniquement dans `.env.local` et dans les variables d'environnement Vercel, **sans** préfixe `NEXT_PUBLIC_` : elle ne doit jamais arriver dans le navigateur.

Variables à prévoir (noms indicatifs) :

```
SUPABASE_URL=https://<id-du-projet>.supabase.co
SUPABASE_SERVICE_ROLE_KEY=...
```

## Modifier les contacts

1. Modifier `data/contacts.sample.json`.
2. Vérifier : `python data/validate_contacts.py`
3. Régénérer : `python data/generate_seed.py`
4. Relancer `seed.sql` dans le SQL Editor.

## Tests effectués (PostgreSQL 16 local)

- Migration et seed lancés **deux fois** : aucune erreur, aucun doublon.
- 20 contacts chargés, dont 9 sans note (`null`).
- Statut inconnu dans `migration_log` → refusé.
- Identifiant mal formé (`X1`) dans `legacy_contacts` → refusé.
- Rôle `anon`, même avec un droit de lecture → **0 ligne visible** (RLS).
