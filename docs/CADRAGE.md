# Cadrage du projet Bascule

Ce document fixe le périmètre du MVP et explique les choix faits pour la semaine du hackathon (16 → 20 novembre 2026).

---

## 1. Ce que le jury évalue

D'après la présentation Eugenia du hackathon :

- **Critère n°1** : une démo **live**, sur un **vrai cas business**, avec un agent qui tourne.
- L'agent doit **agir sur une interface** (voir l'écran, cliquer, taper, naviguer), et son usage doit être justifié : pas d'API, pas d'export.
- **Un seul parcours qui fonctionne de bout en bout**, plutôt que dix fonctionnalités à moitié faites.
- **Des mesures** : taux de réussite, latence, cas d'échec, coût de fonctionnement.

| Critère | Poids |
|---|---|
| Pertinence et impact | 25 % |
| Excellence technique et Agents API | 30 % |
| Faisabilité, adoption et apprentissages | 25 % |
| UX, démo et pitch | 20 % |

## 2. Le constat de départ

La première version des slides prévoyait une migration d'un faux CRM vers **Supabase**. Or **Supabase est une base de données, pas un CRM** : ce scénario ne représentait pas un vrai cas de migration.

## 3. Options étudiées

| Option | Ancien CRM | Nouveau CRM | Verdict |
|---|---|---|---|
| A | Simulé | Supabase | ❌ Supabase n'est pas un CRM : pas de vrai cas |
| B | Réel | Réel | ❌ Difficile de trouver un vieux CRM réellement sans export et stable pour une démo live |
| **C** | **Simulé, réaliste** | **Réel : HubSpot** | ✅ **Retenue** |

## 4. Décisions

| # | Décision | Justification |
|---|---|---|
| D1 | **L'ancien CRM est simulé** (application Next.js au style ancien, sans export ni API, fiches à ouvrir une par une). | Démo maîtrisée, absence d'export prouvable, aucune donnée réelle. |
| D2 | **Le CRM cible est réel : HubSpot** (offre gratuite). Solution de repli : Twenty (CRM open source). | Montre un vrai cas de migration vers un logiciel utilisé par de vraies entreprises. |
| D3 | **L'agent H Company lit l'ancien CRM ; l'écriture dans HubSpot passe par son API.** | L'agent est utilisé là où il est indispensable (pas d'API côté source) ; l'API est plus fiable côté cible. |
| D4 | **Supabase est conservé, en version minimale** (2 tables). Ce n'est pas le CRM cible. | Sert de base cachée à l'ancien CRM et de journal de migration. Sur Vercel, aucun fichier n'est conservé : il faut une base pour garder les mesures. |
| D5 | **Plan B Supabase** : fichier JSON pour les contacts, export CSV pour les mesures. | Le cœur de la démo (ancien CRM → agent → HubSpot) n'en dépend pas. |
| D6 | **n8n est exclu du MVP.** | Pas nécessaire au parcours principal. |
| D7 | **100 contacts synthétiques** dans l'ancien CRM (`data/contacts.legacy.json`), relevé de 20 à 100 le 17/11 pour plus de crédibilité. | Aucune donnée personnelle réelle ; volume crédible pour la démo et les mesures. |
| D8 | **Écran de lancement et bilan final = deux parties de l'écran de suivi** (bouton « Lancer la migration » en haut, encadré « Bilan » en bas), construit par Inès. | Évite deux écrans supplémentaires. |
| D9 | **Une fiche bloquée est affichée avec sa raison, mais n'est pas corrigeable dans l'outil.** | Un formulaire de correction n'est pas indispensable au parcours principal. En démo : « Thomas la corrige à la main ». |
| D10 | **Les fiches « à vérifier » (warning) partent dans HubSpot, sans note.** L'anomalie est enregistrée dans `migration_log` et affichée sur l'écran de suivi. | Reste simple ; l'information n'est pas perdue. |
| D11 | **L'ancien CRM n'a pas de mot de passe pour le MVP.** | Gestion des connexions par l'agent H encore inconnue ; à ajouter si le temps le permet. |

## 5. Architecture cible

```
┌──────────────────────┐      ┌─────────────────┐      ┌──────────────────┐      ┌──────────────────┐
│ Ancien CRM (simulé)  │      │ Agent H Company │      │  Vérification    │      │ HubSpot (réel)   │
│ Next.js sur Vercel   │ ───► │ lit l'écran,    │ ───► │ mapping, doublons│ ───► │ contacts créés   │
│ sans export ni API   │      │ clique, extrait │      │ anomalies        │      │ via l'API        │
└──────────┬───────────┘      └─────────────────┘      └────────┬─────────┘      └──────────────────┘
           │ lit ses données                                    │ enregistre chaque fiche
           ▼                                                    ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ Supabase                                                                     │
│  • legacy_contacts : base cachée de l'ancien CRM (l'agent n'y a pas accès)   │
│  • migration_log   : statut, champs extraits, anomalies, temps, coût         │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Tables Supabase

| Table | Rôle |
|---|---|
| `legacy_contacts` | Les contacts fictifs affichés par l'ancien CRM. L'agent n'a **pas** le droit de la lire directement. |
| `migration_log` | Une ligne par fiche migrée : statut, champs extraits, anomalies, temps, coût. |

## 6. Mesures à produire

- Taux de réussite **par fiche** et **par champ**.
- Temps moyen par fiche.
- Coût par fiche (crédits Agent API H Company).
- Liste et typologie des cas d'échec.

## 7. Planning de la semaine

> **Règle de rythme : on n'attend pas le lendemain.** Le planning ci-dessous donne un **ordre** et des **échéances** (les livrables Eugenia), pas un calendrier à respecter jour par jour. Dès qu'une tâche est finie, on enchaîne sur la suivante, même si elle est prévue pour un autre jour. Seules les échéances des livrables sont fixes.

| Jour | Livrable Eugenia | Objectif de l'équipe |
|---|---|---|
| **Lun. 16** | Validation d'idée (17h) ✅ | Cadrage, création du compte HubSpot |
| **Mar. 17** | — | Ancien CRM en ligne avec 100 contacts ; premier agent H qui lit **une fiche** |
| **Mer. 18** | Point intermédiaire (17h) : parcours, architecture, Loom de 2 min, roadmap | Parcours complet sur quelques fiches : ancien CRM → agent → vérification → HubSpot |
| **Jeu. 19** | — | 20 fiches, mesures, plan B pour la démo live |
| **Ven. 20** | Prototype, fiche projet + repo, vidéo démo (11h) · Pitch deck de 8 à 12 slides (15h) | Démo live, README complet, retour d'expérience sur l'Agent API, business model et coût de run |

## 8. Points à vérifier

- [ ] Offre gratuite HubSpot et création de contacts via l'API (jeton d'application privée).
- [ ] Accès et crédits Agent API H Company.
- [ ] Visibilité du dépôt GitHub pour le jury.
