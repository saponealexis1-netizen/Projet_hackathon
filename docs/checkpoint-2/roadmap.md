# Bascule — Roadmap jusqu'à jeudi

> État au **mardi 17/11/2026 au soir**. L'objectif de mercredi (parcours complet sur 5 fiches) a été atteint **dès mardi**, puis étendu à **100 fiches**.
> Règle de l'équipe : **on n'attend pas le lendemain**. Dès qu'une tâche est finie, on enchaîne sur la suivante.

---

## 1. Déjà fait ✅

| Brique | Qui |
|---|---|
| Cadrage et décisions du MVP (D1 à D14), dont ce qui rend l'agent spécifique | Alexis |
| Format commun des contacts + base Supabase de l'ancien CRM : **100 contacts fictifs** | Alexis |
| Vérification des fiches (ok / à vérifier / bloquée) | Inès |
| **Ancien CRM en ligne, v1 et v2** (autre mise en page, autres libellés) : 10 contacts par page, fiche sur 2 onglets, téléphone derrière un bouton, « Message du jour » à fermer, aucun export — [v1](https://projet-hackathon-uffi.vercel.app) · [v2](https://projet-hackathon-uffi.vercel.app/v2) | Maxime (socle : Victoria) |
| **Agent H Company + orchestration** : zéro configuration, 3 agents en parallèle, contrôle d'identité et relance, capture d'écran gardée pour chaque fiche | Alexis |
| Envoi des contacts vérifiés vers HubSpot (sans doublon) + journal `migration_log` | Alexis |
| 🎯 **Migration complète : 100/100 fiches dans HubSpot, 100 % exactes**, 31 s et ~0,015 $ par fiche, 1,53 $ au total | Toute l'équipe |
| Écran de suivi **branché sur la vraie migration** : [?run=tout](https://projet-hackathon-jow2.vercel.app/?run=tout) | Inès (branchement : Alexis) |
| Mesures : réussite par fiche et par champ, temps, coût, extrapolation à 3 000 fiches | Alexis |
| Business model, parcours utilisateur, brouillon du pitch deck | Maxime |
| Schéma d'architecture | Inès |
| Livrable 2 : parcours, architecture, vidéo du mini-pitch, roadmap, avancement réel | Toute l'équipe |

## 2. Mercredi — Livrable 2 et démo plus forte

| Tâche | Qui | Terminé quand… |
|---|---|---|
| 📦 **Dépôt du livrable 2** | Alexis | **Avant 17h** (prévu 16h30) |
| **Fiches pièges** dans l'ancien CRM : doublon, e-mail invalide, prénom vide, téléphone incomplet | Alexis + Inès | Bascule les **bloque** ou les **relit** (D13), et l'écran de suivi l'affiche |
| Scénario de la démo live (vue HubSpot vidée puis remplie, ou lancement en direct de quelques fiches) | Alexis + Maxime | Scénario écrit et testé une fois |

## 3. Jeudi — Fiabiliser et préparer vendredi

| Tâche | Qui | Terminé quand… |
|---|---|---|
| Migration finale des 100 fiches + pièges, mesures définitives | Alexis | Chiffres finaux dans `pipeline/metrics/` |
| Pitch deck (8 à 12 slides) avec les **vrais chiffres** (100/100, 31 s, 0,015 $, ~46 $ pour 3 000 fiches) | Maxime | Relu par Alexis |
| Retour d'expérience Agent API : ce qui a marché, cassé, surpris | Inès + Alexis | Section prête pour le pitch et le README |
| Plan B : vidéo de secours de la démo | Inès | La démo peut être montrée sans réseau |
| 🎯 **Répétition de la démo à 18h** | Toute l'équipe | Démo réussie de bout en bout |

**Vendredi :** 11h, prototype + dépôt GitHub + vidéo de 5 min · 15h, pitch deck · ensuite, pitch.

## 4. Risques principaux

| Risque | Parade |
|---|---|
| L'agent se trompe de fiche ou lit mal une valeur | Contrôle d'identité + relance automatique, vérification, relecture ciblée (déjà en place : 3 erreurs sur 100 bloquées puis corrigées) |
| Plus de crédits H Company | ~0,015 $ par fiche : une migration de 100 fiches coûte ~1,5 $ ; clé d'Inès en secours |
| La démo live plante (réseau, agent) | Vidéo de secours jeudi ; les 100 fiches déjà migrées restent visibles dans HubSpot et sur l'écran de suivi |
