# Mesures — Bascule

Propriétaire : **Alexis (CDO)**. Python 3 standard, aucune dépendance.

Transforme le journal `migration_log` en **chiffres pour le pitch (slide 9) et le bilan de la démo**.

## Utilisation

```bash
# Depuis Supabase, pour un lancement donné (variables SUPABASE_URL et SUPABASE_SERVICE_ROLE_KEY)
python -m pipeline.metrics.compute --run-id <uuid>

# Depuis un export JSON de migration_log
python -m pipeline.metrics.compute --log journal.json

# Avec les cas pièges en plus des 20 contacts, et un export JSON des chiffres
python -m pipeline.metrics.compute --run-id <uuid> --truth data/pieges.json --json mesures.json

# Tests (faux journal, sans réseau)
python -m unittest pipeline.metrics.test_compute -v
```

La sortie est un tableau Markdown prêt à coller dans le pitch deck.

## Ce qui est mesuré

| Mesure | Calcul |
|---|---|
| Taux de réussite par fiche | fiches envoyées dans HubSpot (`success` + `partial`) / fiches traitées |
| Fiches 100 % exactes | les 8 champs lus par l'agent sont identiques à la vraie fiche |
| Précision par champ | pour chaque champ, part des fiches où l'agent a lu la bonne valeur |
| Temps par fiche | moyenne et médiane de `duration_ms` |
| Coût par fiche | moyenne de `credits_used` |
| Extrapolation 3 000 fiches | coût × 3 000 ; temps avec 1 agent et avec 3 agents en parallèle |

- **Comparaison juste** : la vraie fiche passe par le même nettoyage que la vérification d'Inès. Ainsi, « 06 39 98 00 01 » lu par l'agent et « +33 6 39 98 00 01 » dans la base comptent comme identiques.
- **La « vérité »** vient de `data/contacts.sample.json` (les fiches de l'ancien CRM), complétable avec `--truth`.

## Convention pour l'orchestration

Dans `migrate(..., metrics=...)`, pour chaque fiche :
- `duration_ms` : temps de l'agent pour cette fiche, en millisecondes ;
- `credits_used` : **coût de la fiche en dollars** (champ `metrics` de la session H Company).
