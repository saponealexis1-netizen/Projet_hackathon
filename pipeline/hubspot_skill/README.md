# Skill HubSpot — Bascule s'adapte tout seul à HubSpot

Propriétaire : **Inès (CAIO)**. Python 3 standard, aucune dépendance. Validé par Alexis le 17/11.

**L'idée** : ce que Bascule sait de HubSpot (où ranger chaque champ, ce que HubSpot refuse, les erreurs déjà vues) n'est plus écrit en dur dans le code, mais dans un **skill** : un fichier que **deux IA** tiennent à jour quand HubSpot évolue.

- **Côté ancien CRM** : l'agent H Company lit n'importe quel logiciel, **sans configuration** (D12).
- **Côté HubSpot** : le skill suit les nouveautés de HubSpot, **sans réécrire de code**.

| Fichier | Rôle |
|---|---|
| [`skill.json`](skill.json) | Le skill lu par le code : correspondance des champs, règles, erreurs connues, nouveautés, alertes, historique |
| [`SKILL.md`](SKILL.md) | Le même skill, lisible par un humain (généré, ne pas modifier à la main) |
| `update.py` | Les deux IA, les garde-fous et les trois déclencheurs |
| `llm.py` | Appel des modèles (Hugging Face ou Vercel AI Gateway) |
| `sources.py` | Ce que la veille regarde : propriétés des contacts HubSpot, changelog HubSpot |
| `heal.py` | **Fallback en direct** : HubSpot refuse une fiche → les 2 IA réparent le skill → nouvel essai |
| `test_skill.py`, `test_heal.py` | 25 tests avec de fausses IA et un faux HubSpot (sans réseau) |
| [`../../.github/workflows/skill-hubspot.yml`](../../.github/workflows/skill-hubspot.yml) | La veille quotidienne |

## Comment ça marche

```
          ┌──────────── chaque jour (GitHub Actions) ou à la main ────────────┐
          │                                                                     │
   Champs des contacts HubSpot        Changelog HubSpot           Erreur renvoyée par HubSpot
   (API, empreinte)                   (nouveautés)                (fiche refusée)
          │                                  │                            │
          └──────────────────────────────────┼────────────────────────────┘
                                             ▼
                    🧠 IA n°1 « l'analyste » (Qwen3, Hugging Face)
                       propose une modification du skill (JSON)
                                             ▼
                    🛡️ Garde-fous du code : 9 champs du contrat, legacy_id verrouillé,
                       propriétés qui existent vraiment dans HubSpot, pas de doublon
                                             ▼
                    🔍 IA n°2 « le contrôleur » (autre modèle : Hugging Face ou Vercel)
                       approuve ou refuse
                                             ▼
               ✅ les deux d'accord → nouvelle version du skill → pull request → Alexis fusionne
               🛑 sinon → skill inchangé + alerte notée pour l'équipe
```

**Ce qui change automatiquement** (si les deux IA sont d'accord) : la correspondance des champs, les extensions d'e-mail refusées, les erreurs connues, les nouveautés notées.
**Ce qui reste une alerte** : un gros changement (API retirée, changement de format) est signalé à l'équipe, jamais corrigé seul.

**Économe** : pour les champs, les IA ne sont appelées **que si l'empreinte des propriétés HubSpot a changé** (ou si la correspondance ne colle plus). Un jour sans changement ne coûte rien.

## Ce que le skill change déjà dans Bascule

| Où | Effet |
|---|---|
| `pipeline/verification/mapping.py` → `to_hubspot()` | Utilise la correspondance du skill (secours : `FIELD_MAP` si le skill est absent ou invalide) |
| `pipeline/verification/verify.py` | Nouvelle anomalie **`email_refused_by_hubspot`** (bloquante) : e-mails dont l'extension est refusée par HubSpot d'après le skill (aujourd'hui `.example`, la leçon d'Alexis) |
| Envoi d'Alexis (`pipeline/hubspot/send.py`) | **Aucune modification** : il passe déjà par `to_hubspot()` |

## Fallback en direct : Bascule se répare pendant la migration

Principe expliqué par le professeur : quand une action échoue, le système revient en arrière, recalcule, se met à jour et réessaie ; on le voit dans les journaux. Validé par Alexis le 17/11.

```
❌ HubSpot refuse une fiche (erreur 400 : propriété inconnue, valeur refusée…)
🧠 IA n°1 lit l'erreur + la liste des propriétés HubSpot → propose une correction du skill
🛡️ garde-fous du code → 🔍 IA n°2 valide → skill enregistré (nouvelle version)
🔁 la fiche est revérifiée avec le skill corrigé, puis renvoyée UNE fois
✅ « envoyée après correction »  ou  🛑 « bloquée avant HubSpot (règle apprise) »  ou  ⚠️ « non corrigée »
```

| Où | Ce qui se passe |
|---|---|
| `pipeline/hubspot/send.py` → `migrate_one()` | En cas d'échec de l'envoi : `self_heal_and_retry()` (≈ 30 lignes, accord d'Alexis) |
| `migration_log.self_heal` | Compte rendu : erreur HubSpot, ce que les IA ont fait, version du skill, résultat. **Colonne à créer** : `supabase/migrations/20261118120000_self_heal.sql` |
| Écran de suivi | Ligne `🩹 ❌ refusée par HubSpot → 🧠 skill vN corrigé par les 2 IA → ✅ envoyée après correction`, détail dans la fenêtre « Preuve », compteur dans le bilan. Tant que la colonne n'existe pas, l'écran fonctionne sans. |
| Journal de la migration (GitHub Actions) | `🩹 envoyée après correction (skill vN)` sur la ligne de la fiche, et résumé des réparations en fin de lancement |

**Ce qui n'est jamais « réparé »** : jeton invalide (401/403), limite de débit (429), HubSpot en panne (5xx).
**Crédits maîtrisés** : une même erreur n'est analysée qu'une fois par lancement (les fiches suivantes utilisent directement le skill corrigé, sans échec), et au plus 5 analyses par lancement.

### La démo du fallback (pour le jury)

*GitHub → Actions → « Lancer la migration » → cocher **panne_demo** → Run workflow.*

Le skill est cassé volontairement au début du lancement : la fonction (« job_title ») part vers une propriété HubSpot qui n'existe pas (`jobtitle_ancien`). Résultat attendu :
1. la 1re fiche est **refusée par HubSpot** ;
2. les 2 IA lisent l'erreur, retrouvent `jobtitle` dans la liste des propriétés, corrigent le skill ;
3. la fiche est **renvoyée et acceptée** ; les fiches suivantes passent **directement** ;
4. l'écran de suivi montre la ligne 🩹, et le résumé du lancement affiche la réparation.

La réparation faite pendant cette démo n'est **pas** enregistrée dans Git (le skill de `main` n'a jamais été cassé).

## Diagnostic en un clic

*GitHub → Actions → « Veille HubSpot (skill) » → cocher **diagnostic** → Run workflow* (ou `python -m pipeline.hubspot_skill.check`).
N'écrit rien. Vérifie : le skill, **les 2 IA** (clé acceptée ? modèles servis avec notre clé ? réponse JSON ?), la lecture des propriétés HubSpot, le changelog. Chaque ❌ est suivi de « Que faire ».

**Robustesse de l'appel aux IA** (après l'essai réel du 18/11, où la réparation n'a pas abouti) :
- si le modèle principal n'est pas servi avec notre clé, les **modèles de secours** sont essayés (`SKILL_LLMn_FALLBACK_MODELS`) ; le modèle réellement utilisé est noté dans l'historique du skill ;
- clé refusée (401/403) → message clair (droit « Make calls to Inference Providers », crédits) ;
- secrets GitHub vides ignorés (valeurs par défaut) ;
- réponse de Qwen3 rangée dans le raisonnement → récupérée ;
- l'erreur HubSpot « Property "…" does not exist » est décodée et le champ concerné est indiqué à l'IA ;
- la **raison** d'une réparation non aboutie est affichée sur la ligne 🩹 du journal de migration.

## Utilisation

```bash
# Depuis la racine du dépôt, avec HUBSPOT_TOKEN et HF_TOKEN dans l'environnement
python -m pipeline.hubspot_skill.update --champs --nouveautes          # la veille complète
python -m pipeline.hubspot_skill.update --champs --dry-run             # sans rien écrire
python -m pipeline.hubspot_skill.update --erreur "Property values were not valid: email"
python -m pipeline.hubspot_skill.skill                                 # régénérer SKILL.md
python -m unittest pipeline.hubspot_skill.test_skill pipeline.hubspot_skill.test_heal -v   # tests (sans réseau)
```

## Configuration (secrets, jamais dans Git)

| Variable | Rôle | Défaut |
|---|---|---|
| `HUBSPOT_TOKEN` | Lire les propriétés des contacts (droit `crm.schemas.contacts.read`, déjà présent) | — |
| `HF_TOKEN` | Clé Hugging Face (crédits de l'équipe), droit « Make calls to Inference Providers » | — |
| `SKILL_LLM1_MODEL` | Modèle de l'IA n°1 | `Qwen/Qwen3-32B` |
| `SKILL_LLM2_MODEL` | Modèle de l'IA n°2 (un **autre** modèle, pour un vrai 2e avis) | `Qwen/Qwen3-Next-80B-A3B-Instruct` |
| `SKILL_LLM2_BASE_URL`, `SKILL_LLM2_API_KEY` | Pour mettre l'IA n°2 sur les **crédits Vercel** : `https://ai-gateway.vercel.sh/v1` + clé AI Gateway | Hugging Face |
| `HUBSPOT_CHANGELOG_URL` | Page des nouveautés HubSpot lue par la veille | `https://developers.hubspot.com/changelog` |

**Pour activer la veille quotidienne (Alexis)** : ajouter le secret `HF_TOKEN` dans *Settings → Secrets and variables → Actions* ; autoriser GitHub Actions à ouvrir des pull requests (*Settings → Actions → General → Workflow permissions → « Allow GitHub Actions to create and approve pull requests »*). Puis *Actions → « Veille HubSpot (skill) » → Run workflow* pour un premier essai.

## À vérifier au premier vrai essai

- [ ] Les deux noms de modèles sont bien disponibles avec notre clé Hugging Face (sinon, changer `SKILL_LLM1_MODEL` / `SKILL_LLM2_MODEL`).
- [ ] Le changelog HubSpot se lit bien en texte (sinon, changer `HUBSPOT_CHANGELOG_URL`).
- [ ] Le premier passage `--champs` enregistre l'empreinte sans appeler les IA (comportement attendu).
