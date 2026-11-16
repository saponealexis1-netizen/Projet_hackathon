# Bascule

> **Changez de logiciel, sans perdre vos données.**

Bascule est un agent IA qui récupère les fiches clients d'un ancien CRM **sans export ni API**, en utilisant son interface visuelle comme le ferait un humain, puis prépare leur migration vers un nouveau CRM.

Projet réalisé lors du **Hackathon Eugenia 2026 — « Build The Future »** (16 → 20 novembre 2026), track *Creative Entrepreneur*, en partenariat avec H Company, Hugging Face et Vercel.

---

## Sommaire

- [Le problème](#le-problème)
- [La solution](#la-solution)
- [Personas](#personas)
- [Stack technique](#stack-technique)
- [L'équipe](#léquipe)
- [Livrables](#livrables)
- [Structure du dépôt](#structure-du-dépôt)

---

## Le problème

Changer de CRM devient difficile quand les fiches clients ne peuvent pas être exportées simplement.

| | Constat | Conséquence |
|---|---|---|
| 01 | **Un logiciel fermé** : le CRM historique ne propose ni API accessible ni export exploitable. | Les outils de migration classiques sont inutilisables. |
| 02 | **Une ressaisie manuelle** : l'équipe doit ouvrir chaque fiche et la recopier dans le nouveau logiciel. | Temps perdu et risque d'erreur. |
| 03 | **Un frein à la migration** : l'entreprise hésite à adopter une meilleure solution. | Elle reste bloquée sur un outil dépassé. |

> Le vrai problème n'est pas de choisir un nouveau CRM. C'est de réussir à quitter l'ancien.

## La solution

**Une migration pilotée par un agent IA.** L'agent utilise l'interface visuelle du CRM source ; le traitement et l'écriture sont ensuite contrôlés par notre application.

```
 1. CRM ANCIEN          2. AGENT H COMPANY       3. VÉRIFICATION           4. CRM CIBLE
 Interface web     →    Observe, clique et   →   Mapping des champs,   →   CRM réel : HubSpot,
 simulée, sans          extrait les contacts     doublons et anomalies     alimenté via son API
 export ni API
```

**Périmètre du MVP**
- 10 à 20 contacts **synthétiques**.
- Aucun accès direct à la base source.
- Aucune donnée réelle.
- Ancien CRM **simulé** (on contrôle la démo et on prouve l'absence d'export) ; CRM cible **réel** (HubSpot).

**Pourquoi un agent *computer-use* ?** Sans API ni export, une automatisation classique (script, connecteur) ne peut pas lire les données : il faut « voir » l'écran et naviguer dans l'interface. L'agent n'intervient que là où c'est indispensable (la lecture de l'ancien CRM) ; l'écriture dans HubSpot passe par son API, plus fiable.

Le cadrage complet (options étudiées, décisions, planning) est détaillé dans [docs/CADRAGE.md](docs/CADRAGE.md).
La répartition des tâches et les règles de travail en équipe sont dans [docs/ORGANISATION.md](docs/ORGANISATION.md).

## Personas

Personas fictifs de cadrage — business model B2B à tester.

| | **Camille** — utilisatrice finale | **Thomas** — client / payeur potentiel |
|---|---|---|
| Rôle | Gérante d'une petite agence | Responsable onboarding d'un éditeur CRM |
| Situation | Utilise un vieux CRM et connaît peu les outils IA. Elle redoute de ressaisir ses contacts et de perdre des informations. | Veut automatiser l'intégration des nouveaux clients, mais les anciens logiciels sans export bloquent ses outils habituels. |
| Citation | « Je veux changer d'outil, pas tout recopier. » | « La migration ne devrait pas bloquer une vente. » |

## Stack technique

| Outil | Rôle dans le projet |
|---|---|
| **H Company** (Agent API) | Navigation visuelle et extraction des fiches dans l'ancien CRM |
| **HubSpot** (CRM gratuit + API) | CRM cible réel, dans lequel les contacts sont importés |
| **Next.js / TypeScript** | Ancien CRM simulé, interface de suivi et orchestration |
| **Vercel** | Hébergement des interfaces |
| **Supabase** | Base cachée de l'ancien CRM + journal de migration et mesures (**ce n'est pas le CRM cible**) |
| **Hugging Face** | Jeu de données synthétique de référence |
| **GitHub + Claude Code** | Versionnage et développement |

## L'équipe

Team 8 — six rôles attribués.

| Membre | Rôle | Responsabilités |
|---|---|---|
| Maxime Bazin | **CEO** | Vision, pitch, priorités |
| Victoria Ifrah | **CTO** | Conception des agents |
| Inès Soubran | **CAIO** | Extraction et vérification IA |
| Alexis Sapone | **CDO** | Données, mapping, mesures |
| Mehdi Zitouni | **CPO** | Design, parcours, interface |
| Natalia Medrano | **CAO** | Automatisations, marketing |

## Livrables

| Checkpoint | Échéance | Contenu | Statut |
|---|---|---|---|
| **1 — Validation d'idée** | Lun. 16/11, 17h | [Slides (PDF)](docs/checkpoint-1/) | ✅ Livré |
| 2 — Point intermédiaire | Mer. 18/11, 17h | Parcours utilisateur, architecture, mini pitch, roadmap | À venir |
| 3 — Produit | Ven. 20/11, 11h | Prototype, fiche projet + repo, vidéo démo | À venir |
| 4 — Pitch deck | Ven. 20/11, 15h | 8 à 12 slides | À venir |

## Structure du dépôt

```
.
├── README.md                    ← présentation du projet (ce fichier)
└── docs/
    ├── CADRAGE.md               ← décisions de cadrage et planning de la semaine
    ├── ORGANISATION.md          ← qui fait quoi, règles Git, circuit de merge
    └── checkpoint-1/
        ├── README.md            ← détail du livrable 1
        └── Bascule_Livrable1_Validation_Idee_CORRIGE.pdf
```
