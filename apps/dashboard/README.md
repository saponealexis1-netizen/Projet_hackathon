# Écran de suivi de migration — Bascule

Propriétaire : **Inès (CAIO)**. Décisions : D8, D9, D10 dans [`docs/CADRAGE.md`](../../docs/CADRAGE.md).

Un seul écran, en trois parties :

1. **En haut : le bouton « Lancer la migration »** (écran de lancement, D8).
2. **Au milieu : le suivi en direct.** Barre de progression, compteurs (migrées, à vérifier, bloquées, temps moyen, crédits) et une ligne par fiche avec son statut et ses anomalies.
3. **En bas : l'encadré « Bilan ».** Fiches envoyées dans HubSpot, taux de réussite, durée, crédits, **fiches bloquées avec leur raison** (pas de correction dans l'outil, D9) et anomalies par type.

| Statut affiché | `migration_log.status` | Envoyée dans HubSpot ? |
|---|---|---|
| Migrée | `success` | ✅ |
| À vérifier | `partial` | ✅ sans note, anomalie affichée (D10) |
| Bloquée | `failed`, `duplicate` | ❌ affichée avec sa raison (D9) |
| Ignorée | `skipped` | ❌ |

## Lancer en local

```bash
cd apps/dashboard
npm install
npm run dev        # http://localhost:3001 (le port 3000 reste à l'ancien CRM)
```

Sans fichier `.env.local`, l'écran tourne en **mode démo** : la migration est simulée (une fiche toutes les 1,2 s) sur les 20 contacts d'exemple et 4 cas pièges, passés par la vraie vérification. Un bandeau « Mode démo : données simulées » est affiché.

Pour régénérer les données de démo après une modification de la vérification :

```bash
python apps/dashboard/scripts/make_demo_data.py
```

## Brancher sur la vraie migration

Copier `.env.example` en `.env.local` (jamais commité) et remplir :

| Variable | Rôle |
|---|---|
| `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY` | Lecture de `migration_log` (côté serveur uniquement) |
| `GITHUB_DISPATCH_TOKEN` | Le bouton lance le **vrai agent** via l'action GitHub « Lancer la migration » (voir [docs/demo](../../docs/demo/README.md)) |
| `HAI_API_KEY` | Captures d'écran de l'agent et panneau « Agents en direct » |
| `ORCHESTRATOR_URL` | Autre orchestration HTTP, si pas de jeton GitHub |
| `MIGRATION_TOTAL` | Nombre de fiches attendu (si l'orchestration ne le renvoie pas) |
| `HUBSPOT_CONTACT_URL` | Optionnel : lien « Ouvrir » vers chaque contact HubSpot |

### Contrat avec l'orchestration (Victoria)

```
Bouton ──POST /api/migration──► dashboard ──POST ORCHESTRATOR_URL {"run_id": "<uuid>"}──► orchestration
                                                           ◄── {"total": 20} ──

orchestration ──une ligne par fiche, avec ce run_id──► Supabase migration_log
dashboard ──toutes les 2 s : GET /api/migration/<run_id>──► lit migration_log
```

Ce qui est attendu dans chaque ligne de `migration_log` :
- `anomalies` = la liste `anomalies` renvoyée par `pipeline/verification` (champs `field`, `code`, `severity`, `message`) ;
- `status` = `success` si la vérification renvoie `ok`, `partial` si `warning`, `failed` si `error` (`duplicate` pour un doublon bloquant) ;
- `duration_ms`, `credits_used`, `hubspot_id` remplis quand c'est possible.

## Fichiers

| Fichier | Rôle |
|---|---|
| `app/page.tsx` | L'écran (lancement, suivi, bilan) |
| `app/api/migration/route.ts` | Bouton « Lancer » → orchestration (ou démo) |
| `app/api/migration/[runId]/route.ts` | État d'une migration, lu dans `migration_log` |
| `lib/bilan.ts` | Calcul du bilan et correspondance des statuts |
| `lib/demo.ts`, `lib/demo-data.json` | Mode démo |
| `lib/supabase.ts` | Lecture Supabase par l'API REST (aucune dépendance) |

## Afficher une migration réelle

Une fois `SUPABASE_URL` et `SUPABASE_SERVICE_ROLE_KEY` configurées (dans `.env.local` ou dans Vercel) :

| Adresse | Ce qui s'affiche |
|---|---|
| `/?run=tout` | **L'état de chaque fiche migrée**, tous lancements confondus (dernière lecture de chaque fiche) |
| `/?run=<identifiant>` | Un lancement précis, déjà terminé |
| `/?run=<identifiant>&total=100` | Un lancement **en cours**, lancé depuis `agent/runner` avec `--run-id <identifiant>` : l'écran se remplit en direct |
| `/?run=dernier` | **Le lancement le plus récent**, suivi en continu (pratique pendant la démo) |

## Migration réelle en direct (bouton et agents en direct)

1. Le bouton appelle `POST /api/migration`. Avec `GITHUB_DISPATCH_TOKEN`, il crée un identifiant de lancement et déclenche l'action GitHub **« Lancer la migration »** sur `main` (6 fiches de démo : C-0004 + les 5 pièges). Il refuse si des agents Bascule travaillent déjà.
2. L'action remet ces fiches à zéro dans HubSpot, puis lance `agent/runner` : chaque fiche est vérifiée, envoyée et **écrite dans `migration_log` dès qu'elle est lue**.
3. L'écran suit ce lancement (`?run=<id>&total=6`). Le panneau **« Agents en direct »** (`/api/live/<id>`) montre les agents H au travail, avec leur dernière capture d'écran (`/api/live/shot/<session>`, rafraîchie toutes les 3 s, clé gardée côté serveur, uniquement les sessions du groupe `bascule-…`).

Coûts affichés en dollars (`credits_used` = coût de la fiche en $, mesuré par l'Agent API).

## Preuves de l'agent (D13, D14)

- **Colonne « Preuve » → bouton « 📷 Voir »** : ouvre une fenêtre avec, à gauche, **la capture d'écran de la fiche vue par l'agent** (`screenshot_url`, D14) et, à droite, **les 9 champs qu'il a lus**. C'est la réponse à « Et si l'agent se trompe ? ». Si la capture a expiré, un message le dit.
- **Relecture ciblée (D13)** : quand l'agent a relu un champ, la colonne « Anomalies » affiche `🔁 Téléphone relu par l'agent : « avant » → « après »` (en bleu si la valeur a été corrigée, « confirmé » sinon), et le champ est surligné dans la fenêtre Preuve.
- **Bilan** : nombre de champs relus (et corrigés), et nombre de fiches avec capture d'écran.

## Captures d'écran de l'agent (preuve visuelle, D14)

Les captures de l'Agent API H Company ne se téléchargent qu'**avec la clé API** : le navigateur ne peut pas les afficher directement. L'écran passe donc par un relais serveur, **`/api/capture/<session>`**, qui :
- ne sert que les captures enregistrées dans `migration_log` pour cette session ;
- n'interroge que l'hôte de l'Agent API ;
- garde la clé côté serveur (variable **`HAI_API_KEY`**, à ajouter dans Vercel).

Testé avec une vraie capture : image servie (PNG), session inconnue → 404, identifiant invalide → 400.
