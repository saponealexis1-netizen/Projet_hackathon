# Agent H et orchestration — Bascule

Propriétaire : **Alexis**. Python 3 standard, aucune dépendance. Doc H Company : https://hub.hcompany.ai/agents-api/overview

```
pour chaque fiche (3 agents en parallèle) :
  agent H Company  ── lit la fiche à l'écran, zéro configuration (D12)
        ↓ JSON imposé (9 champs du contrat + « error »)
  vérification d'Inès ── anomalie sur l'e-mail / le téléphone ? → l'agent relit le champ (D13)
        ↓
  migrate() ── HubSpot + migration_log (temps, coût, session de l'agent, capture d'écran : D14)
```

## Utilisation

```bash
# 1 fiche, simulation (rien n'est envoyé dans HubSpot)
python -m agent.runner.run --url <adresse de l'ancien CRM> --ids C-0001 --dry-run

# Les 5 premières fiches, pour de vrai
python -m agent.runner.run --url <adresse de l'ancien CRM> --first 5

# Les 100 fiches, 3 agents en parallèle
python -m agent.runner.run --url <adresse de l'ancien CRM> --first 100 --parallel 3

# Tests (agent simulé, sans réseau)
python -m unittest agent.runner.test_run -v
```

Options : `--ids C-0001,C-0002` · `--first N` · `--parallel N` · `--run-id <uuid>` · `--dry-run` · `--no-reread`.
Le détail complet du dernier lancement est écrit dans `agent/runner/last_run.json` (ignoré par Git).

## Variables d'environnement

| Variable | Rôle |
|---|---|
| `HAI_API_KEY` | Clé Agent API H Company (nom utilisé par la doc et les SDK de H) |
| `HUBSPOT_TOKEN` | Clé de service HubSpot |
| `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY` | Pour écrire `migration_log` (facultatif) |

## Fichiers

| Fichier | Rôle |
|---|---|
| `hclient.py` | Client de l'Agent API : créer une session, la suivre (long-poll `/changes`), récupérer réponse, coût, durée, captures |
| `prompts.py` | Instructions de l'agent (règles d'Inès) en version **zéro configuration**, format JSON imposé, consigne de relecture |
| `run.py` | Orchestration : agents en parallèle → relecture ciblée → `migrate()` |
| `test_run.py` | 5 tests avec un agent simulé |

## Ce qui rend l'agent spécifique

| Décision | Dans le code |
|---|---|
| **D12 Zéro configuration** | L'agent ne reçoit que l'adresse et l'identifiant ; il explore, ferme les fenêtres, ouvre onglets et boutons « afficher », comprend les libellés par leur sens (`prompts.READ_RECORD`) |
| **D13 Relecture ciblée** | Si la vérification signale `bad_email`, `bad_phone` ou `missing_required`, une 2e session relit ce champ (`run.reread_if_needed`) ; avant/après enregistrés dans `migration_log.reread` |
| **D14 Preuve visuelle** | Session de l'agent et dernière capture d'écran enregistrées dans `migration_log` (`agent_session_id`, `screenshot_url`) |

## Premier test réel (17/11/2026)

En attendant l'ancien CRM, l'agent a lu la fiche C-0003 sur la page GitHub de `data/contacts.legacy.json` :

| Mesure | Résultat |
|---|---|
| Exactitude | 9/9 champs identiques à la vraie fiche |
| Temps | 12 s |
| Coût | 0,0038 $ |
| Capture d'écran | 1 récupérée |

Paramètres : agent `h/web-surfer-flash`, `max_steps` 40, `max_time_s` 240, quota de 3 agents en parallèle (offre gratuite).

## Tests sur l'ancien CRM (17/11/2026) — ce qu'on a appris

| Test | Résultat | Leçon |
|---|---|---|
| v1, C-0042 (page 5, onglets, bouton « Afficher le numéro »), instructions v1 | 8/9 : **téléphone inventé** | La capture finale montre le bouton jamais cliqué : l'agent a deviné un numéro plausible. La vérification ne peut pas le voir (format correct). |
| Même fiche, instructions durcies (« une valeur n'est valable que si tu la vois », « clique sur les boutons Afficher ») | ✅ 9/9, 34 s, 0,019 $ | L'agent clique bien sur le bouton. |
| v2 (autre mise en page, autres libellés), C-0057 | 8/9 : chiffre mal lu (« 39 » → « 99 ») | Erreur de lecture de l'image. |
| Mode visuel **avec le texte de la page** (`markdown: true`) | ✅ v2 : 9/9, 21 s, 0,013 $ · v1 : 9/9, 36 s, 0,024 $ | L'agent navigue sur les captures mais lit les caractères exacts. |

**Pour le pitch** : c'est la preuve visuelle (D14) qui a permis de comprendre l'erreur, et le **même agent, sans configuration, lit les deux versions du CRM** (D12).

## Premier parcours complet : 5 fiches de bout en bout (17/11/2026)

**1er essai (3 agents en parallèle) : 1/5 seulement.** L'agent avait bien lu les fiches, mais il a parfois rangé toute la fiche en JSON dans le champ « notes » et écrit le mot « None » comme erreur ; une relecture lancée sur une fiche vide a même produit « User User ».

**Corrections** : format de réponse en texte seul (chaîne vide si absent), récupération d'une fiche rangée dans un champ, « None » / « null » ignorés, contrôle que la fiche renvoyée est bien celle demandée, pas de relecture d'une fiche vide (`run.normalize_answer`, 5 tests).

**2e essai, mêmes fiches C-0006 à C-0010** (run `36cc087b-a298-43fe-b874-1f5f78d4378d`, enregistré dans `migration_log`) :

| Mesure | Valeur |
|---|---|
| Fiches lues par l'agent | 5 / 5 |
| Fiches 100 % exactes | **5 / 5** (9/9 champs chacune) |
| Envoyées dans HubSpot | 5 / 5 |
| Temps moyen par fiche | 24 s |
| Coût moyen par fiche | **0,013 $** |
| Durée totale (3 agents en parallèle) | ~1 min |
| Extrapolation 3 000 fiches | ~39 $ · ~6,7 h avec 3 agents |

## Migration complète : les 100 fiches (17/11/2026)

Ancien CRM v1 en ligne → 3 agents H en parallèle → vérification → HubSpot → `migration_log`.

| Mesure | Valeur |
|---|---|
| Fiches migrées dans HubSpot | **100 / 100** |
| Fiches **100 % exactes** (9/9 champs) | **100 / 100** |
| Temps moyen par fiche | 31 s (médiane 29 s) |
| Durée réelle (3 agents en parallèle) | **32 min 56 s** mesurées (≈ 33 s perdues par tour d'agents, voir ci-dessous) |
| Coût total agent H | **1,53 $** (~0,015 $ par fiche) |
| Extrapolation 3 000 fiches | ~46 $ · ~8,7 h avec 3 agents (~2,6 h avec 10, offre Builder) |

**Ce qui a coincé** : au 1er passage, 3 fiches sur 100 (C-0070, C-0077, C-0088) ont été **bloquées par le contrôle d'identité** : l'agent avait ouvert C-0007 / C-0008, dont le numéro ressemble. Aucune mauvaise fiche n'est partie dans HubSpot. Correction : consigne « l'identifiant doit être exactement {legacy_id}, caractère par caractère » + **relance automatique une fois** si la fiche renvoyée n'est pas la bonne. Les 3 fiches relancées : 3/3 exactes.

Runs : `b961da00-eb32-4e73-b21f-4b705cf9d198` (97 fiches) et `f7962b57-39f2-4829-9440-a0647263a5a6` (3 fiches relancées), dans `migration_log`.

## Durée réelle : 33 min mesurées, ~17 min après correction (17/11/2026)

Les horaires de début et de fin de chaque session d'agent (API H : `started_at`, `finished_at`) sont maintenant enregistrés dans `migration_log` (`agent_started_at`, `agent_finished_at`) et récupérés pour les migrations passées.

| | Avant | Après correction |
|---|---|---|
| Migration des 100 fiches (du 1er agent démarré au dernier terminé) | **32 min 56 s** | ~17-18 min (projection) |
| Test : 6 fiches, 3 agents | — | **62 s** |

**Cause** : une fois la réponse de l'agent reçue, `hclient.wait` relançait une attente longue (20 s) de l'API pour confirmer qu'il n'y avait plus rien : **~20 s perdues par fiche**. Correction : arrêt dès que la session est terminée et la réponse reçue ; plus d'attente longue après la fin.

L'écran de suivi affiche désormais la **durée réelle** (dernière fin − premier début, par lancement), et non plus le temps cumulé des agents.
