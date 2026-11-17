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
