# Bascule — Fiche projet

> **Brouillon du 17/11/2026** (Inès, pour Maxime). À relire vendredi matin et à adapter au formulaire Eugenia du livrable 3 (vendredi 20/11, 11h) : couper ou fusionner les rubriques selon les champs demandés.

---

## En bref

| | |
|---|---|
| **Nom** | Bascule |
| **Slogan** | Changez de logiciel, sans perdre vos données. |
| **En une phrase** | Un agent IA qui récupère les fiches clients d'un ancien CRM **sans export ni API**, en lisant son écran comme un humain, puis les vérifie et les importe dans HubSpot. |
| **Équipe** | Team 8 — Maxime Bazin (CEO), Alexis Sapone (CDO, chef de projet), Inès Soubran (CAIO), Victoria Ifrah (CTO), Mehdi Zitouni (CPO), Natalia Medrano (CAO) |
| **Track** | Creative Entrepreneur — Hackathon Eugenia 2026 « Build The Future » |

## Le problème

Une petite entreprise qui veut changer de CRM est bloquée quand son ancien logiciel n'a **ni export ni API** : il faut recopier chaque fiche à la main. Pour 3 000 fiches, c'est environ 100 heures de travail. Pour 44 % des PME, la migration des données est le premier obstacle au changement de CRM. Pour l'éditeur ou l'agence qui vend le nouveau CRM, c'est souvent la dernière objection avant la signature.

## La solution

1. **Lire** : un agent H Company ouvre l'ancien logiciel, trouve la liste, ouvre chaque fiche et la lit **à l'écran**. Il ne reçoit que l'adresse du logiciel : aucune configuration.
2. **Vérifier** : chaque fiche est nettoyée et classée **ok / à vérifier / bloquée** (e-mail invalide, champ obligatoire vide, doublon…). Un champ suspect est relu par l'agent.
3. **Importer** : les fiches valides sont créées dans **HubSpot** par son API, sans doublon.
4. **Suivre** : un écran de suivi montre la migration en direct, le bilan, et **la capture d'écran de chaque fiche** vue par l'agent, comme preuve.

## Pour qui

- **Thomas**, responsable onboarding d'un éditeur de CRM ou d'une agence partenaire HubSpot : il lance la migration et ne traite que les cas douteux. **C'est lui qui paie.**
- **Camille**, gérante d'une petite agence : elle donne un accès en lecture à son ancien logiciel et retrouve ses contacts dans HubSpot.

## Résultats

| Mesure | Ancien CRM v1 | Ancien CRM v2 (autre mise en page, autres libellés) |
|---|---|---|
| Fiches exactes (9 champs sur 9) | **100 / 100** | **100 / 100** |
| Fiches pièges (doublon, e-mail invalide, prénom vide…) | — | **5 / 5** traitées comme prévu |
| Mauvaise fiche envoyée dans HubSpot | **0** | **0** |
| Durée réelle, 3 agents en parallèle | 33 min (avant correction) | **16,9 min** pour 105 fiches |
| Coût de l'agent par fiche | ~0,015 $ | ~0,008 $ |

**Le même agent, avec les mêmes consignes, a migré deux logiciels différents.** C'est ce qu'un script ou un robot RPA ne sait pas faire.

## Technologies

| Outil | Rôle |
|---|---|
| **H Company — Agent API** (`h/web-surfer-flash`) | Lecture visuelle de l'ancien CRM, réponse JSON imposée, captures d'écran, coût et durée par fiche |
| **HubSpot** (API) | CRM cible réel |
| **Next.js sur Vercel** | Ancien CRM simulé (2 versions) et écran de suivi |
| **Python** | Orchestration des agents, vérification, envoi HubSpot, mesures |
| **Supabase** | Base cachée de l'ancien CRM et journal de migration |
| **GitHub + Claude Code** | Développement en équipe |

## Ce qu'on a appris sur l'Agent API

L'agent sait naviguer seul dans un logiciel qu'il n'a jamais vu, mais il préfère inventer une valeur crédible plutôt que laisser un champ vide. Ce sont les garde-fous autour de lui qui ont tout changé : **1 fiche exacte sur 5 au premier essai, 100 sur 100 ensuite**. Détail : [retour d'expérience](../retour-agent-api/README.md).

## Modèle économique

- **Qui paie** : l'éditeur ou l'agence qui vend le nouveau CRM.
- **Prix** 🔎 : 490 € jusqu'à 2 000 fiches, 990 € jusqu'à 10 000 fiches.
- **Coût de fonctionnement** : ~45 $ pour 3 000 fiches, soit **~95 % de marge** sur un forfait de 990 €.
- **Premiers clients visés** : agences partenaires HubSpot en France.

Détail : [business model](../pitch/business-model.md).

## Limites et suite

| Aujourd'hui (MVP) | Ensuite |
|---|---|
| Contacts uniquement | Notes et pièces jointes |
| Ancien CRM sans mot de passe | Connexion sécurisée (coffre-fort H Company) |
| HubSpot uniquement | Salesforce, Pipedrive, Zoho |
| 3 agents en parallèle | 10 agents et plus (offre Builder) |
| Données fictives | Pilote avec une agence partenaire |
| Prix non encore testés auprès de clients | Entretiens avec des agences partenaires HubSpot (questions prêtes dans le business model) |

## Liens

| | Adresse |
|---|---|
| Dépôt GitHub | https://github.com/saponealexis1-netizen/Projet_hackathon |
| Ancien CRM simulé | https://projet-hackathon-uffi.vercel.app |
| Écran de suivi (vraie migration) | https://projet-hackathon-jow2.vercel.app/?run=tout |
| Vidéo démo (5 min) | `[à ajouter vendredi]` |
| Architecture | [docs/architecture/](../architecture/README.md) |
