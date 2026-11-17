# Bascule — Roadmap jusqu'à jeudi

> État au **lundi 16/11/2026 au soir**, à mettre à jour avant le dépôt de mercredi 17h.
> Règle de l'équipe : **on n'attend pas le lendemain**. Dès qu'une tâche est finie, on enchaîne sur la suivante. Seules les échéances des livrables sont fixes.

**Légende** : ✅ fait (fusionné) · 🔄 en cours · ⏳ à faire

---

## 1. Où on en est

| Brique | État | Qui | Référence |
|---|---|---|---|
| Cadrage du MVP et décisions D1 à D11 | ✅ | Alexis | [CADRAGE.md](../CADRAGE.md) |
| Organisation de l'équipe et circuit de fusion | ✅ | Alexis | [ORGANISATION.md](../ORGANISATION.md) |
| Contrat commun d'un contact + 20 contacts d'exemple | ✅ | Alexis | `shared/contact.schema.json`, `data/` |
| Tables Supabase (`legacy_contacts`, `migration_log`) | ✅ | Alexis | `supabase/` |
| Vérification (mapping, doublons, anomalies) | ✅ | Inès | `pipeline/verification/` |
| Business model + suivi des crédits | ✅ | Maxime | [business-model.md](../pitch/business-model.md) |
| Parcours utilisateur (version finale) | ✅ | Maxime | [parcours-utilisateur.md](../parcours/parcours-utilisateur.md) |
| Premier test de l'agent H (3 fiches sur 3, ~48 s et ~0,02 $ par fiche) | ✅ | Maxime | section 7 du business model |
| Socle Next.js de l'ancien CRM | 🔄 PR ouverte | Victoria | `apps/legacy-crm/` |
| Instructions de l'agent (v0) | 🔄 | Inès | `agent/prompts/` |

## 2. Ce qui reste, dans l'ordre

Le chemin critique est **ancien CRM en ligne → agent qui lit une fiche → agent qui lit plusieurs fiches → parcours complet**. Tout le reste peut avancer en parallèle.

### Étape 1 — Fondations (avant mercredi midi)

| Tâche | Qui | État | Terminé quand… |
|---|---|---|---|
| Ancien CRM simulé : liste paginée + fiche détail, sans export, style « 2010 », en ligne sur Vercel | Victoria | ⏳ | On ouvre chaque fiche dans le navigateur |
| Premier agent H qui lit **une fiche** de l'ancien CRM | Victoria | ⏳ | L'agent renvoie les 9 champs d'une fiche |
| Instructions de l'agent testées sur une fiche | Inès | 🔄 | Testées avec Victoria |
| Compte HubSpot gratuit + création d'un contact par l'API | Alexis | ⏳ | Un contact de test apparaît dans HubSpot |

### Étape 2 — Premier parcours complet (mercredi)

| Tâche | Qui | État | Terminé quand… |
|---|---|---|---|
| Agent qui parcourt **plusieurs fiches** (liste → fiche → retour) | Victoria | ⏳ | 5 fiches extraites d'affilée |
| Envoi des contacts vérifiés vers HubSpot + écriture dans `migration_log` | Alexis | ⏳ | 5 contacts arrivent dans HubSpot |
| Orchestration : agent → vérification → HubSpot, en un seul lancement | Victoria | ⏳ | **Parcours complet sur 5 fiches** |
| Schéma d'architecture | Victoria | ⏳ | Dans `docs/architecture/` |
| **Livrable du checkpoint 2** : parcours, architecture, Loom de 2 min, roadmap | Maxime (dépôt : Alexis) | 🔄 | Déposé **avant mercredi 17h** |

### Étape 3 — Fiabiliser et mesurer (jeudi)

| Tâche | Qui | État | Terminé quand… |
|---|---|---|---|
| Passage à **20 fiches**, gestion des erreurs et des relances | Victoria | ⏳ | 20 fiches en un lancement |
| Cas pièges dans l'ancien CRM + amélioration des instructions | Inès | ⏳ | Les pièges sont détectés et signalés |
| Écran de suivi : bouton « Lancer », tableau de bord, anomalies, encadré « Bilan » | Inès | ⏳ | Lisible par le jury |
| Mesures : taux de réussite par fiche et par champ, temps, coût par fiche | Alexis | ⏳ | Tableau de chiffres dans `pipeline/metrics/` |
| Coût de run final, go-to-market, brouillon du pitch deck (8 à 12 slides) | Maxime | ⏳ | Relu par Alexis |
| Plan B : vidéo de secours + jeu de données de secours | Victoria | ⏳ | La démo peut être montrée même sans réseau |
| **Répétition de démo à 18h** | Tous | ⏳ | Démo réussie de bout en bout |

### Vendredi — Livrer

| Échéance | Livrable |
|---|---|
| Avant 9h | Gel du code : seulement des corrections |
| **11h** | Prototype en ligne, fiche projet + dépôt GitHub, vidéo démo de 5 min |
| **15h** | Pitch deck (8 à 12 slides) |
| Après 15h | Pitch de 6 min + 4 min de questions |

## 3. Risques et parades

| Risque | Parade |
|---|---|
| L'ancien CRM n'est pas en ligne à temps : l'agent ne peut rien lire | C'est la priorité n°1 de l'étape 1. En attendant, l'agent est testé sur un site public (déjà fait : 3 fiches sur 3) |
| L'agent se trompe ou bloque sur une fiche | Vérification automatique (déjà faite) + nombre maximal d'étapes par fiche + relance |
| Limite de 3 agents en parallèle par personne en offre gratuite | Les 20 fiches de la démo sont lancées juste avant le pitch ; clé de secours d'Inès si Victoria n'a plus de crédits |
| Le réseau ou l'agent lâche pendant la démo | Plan B : vidéo enregistrée et jeu de données de secours |
| HubSpot refuse un contact (doublon, format) | La vérification bloque ces fiches avant l'envoi ; les erreurs restantes sont enregistrées dans `migration_log` |
