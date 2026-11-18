# Bascule — Roadmap jusqu'à jeudi

> État au **mercredi 18/11/2026**. L'objectif de mercredi (parcours complet sur 5 fiches) a été atteint **dès mardi**, puis étendu à **100 fiches**, puis à **un deuxième logiciel** mercredi.
> Règle de l'équipe : **on n'attend pas le lendemain**. Dès qu'une tâche est finie, on enchaîne sur la suivante.

---

## 1. Déjà fait ✅

| Brique | Qui |
|---|---|
| Cadrage et décisions du MVP (D1 à D14), dont ce qui rend l'agent spécifique | Alexis |
| Format commun des contacts + base Supabase de l'ancien CRM : **105 contacts fictifs**, dont 5 fiches pièges | Alexis |
| Vérification des fiches (ok / à vérifier / bloquée) | Inès |
| **Ancien CRM en ligne, v1 et v2** (autre mise en page, autres libellés) : 10 contacts par page, fiche sur 2 onglets, téléphone derrière un bouton, « Message du jour » à fermer, aucun export — [v1](https://projet-hackathon-uffi.vercel.app) · [v2](https://projet-hackathon-uffi.vercel.app/v2) | Maxime (socle : Victoria) |
| **Agent H Company + orchestration** : zéro configuration, 3 agents en parallèle, contrôle d'identité et relance, relecture ciblée, capture d'écran gardée pour chaque fiche | Alexis |
| Envoi des contacts vérifiés vers HubSpot (sans doublon) + journal `migration_log`, fiche par fiche | Alexis |
| 🎯 **Migration v1 : 100/100 fiches dans HubSpot, 100 % exactes**, ~0,015 $ par fiche | Toute l'équipe |
| 🎯 **Migration v2, sans rien reconfigurer : 105 fiches lues, 100/100 exactes, 5/5 pièges traités comme prévu**, 16,9 min, ~0,008 $ par fiche | Alexis + Inès |
| Écran de suivi **branché sur la vraie migration** : [?run=tout](https://projet-hackathon-jow2.vercel.app/?run=tout), preuves (capture + champs lus), bilan | Inès (branchement : Alexis) |
| **Bouton « Lancer la migration » = le vrai agent**, via une action GitHub (rien à installer), et panneau **« Agents en direct »** | Alexis |
| **Réparation automatique** quand HubSpot refuse une fiche : skill HubSpot tenu à jour par 2 IA, garde-fous, nouvel essai — testée en réel | Inès |
| Mesures : réussite par fiche et par champ, temps, coût, extrapolation à 3 000 fiches | Alexis |
| Business model, parcours utilisateur, pitch deck et fiche projet avec les vrais chiffres | Maxime + Inès |
| Schéma d'architecture, retour d'expérience Agent API | Inès |
| Mode d'emploi de la démo live (déroulé, plans B), script de la vidéo de secours | Alexis + Inès |
| Livrable 2 : parcours, architecture, vidéo du mini-pitch, roadmap, avancement réel | Toute l'équipe |

## 2. Mercredi — Livrable 2 et démo plus forte

| Tâche | Qui | État |
|---|---|---|
| 📦 **Dépôt du livrable 2** | Alexis | Avant 16h30 |
| **Fiches pièges** dans l'ancien CRM : doublon, e-mail invalide, prénom vide, téléphone incomplet, majuscules | Alexis + Inès | ✅ 5/5 traitées comme prévu |
| Scénario de la démo live | Alexis + Maxime | ✅ Écrit et testé en réel ([docs/demo](../demo/README.md)) |
| Démo en un clic depuis l'écran de suivi, sans installation | Alexis | ✅ Testée en réel (6 fiches) |
| Réparation automatique si HubSpot refuse une fiche | Inès | ✅ Testée en réel (2 essais réussis) |
| Design de l'écran de suivi | Mehdi | En cours |

## 3. Jeudi — Fiabiliser et préparer vendredi

| Tâche | Qui | Terminé quand… |
|---|---|---|
| Design de l'écran de suivi finalisé | Mehdi | PR fusionnée avant 18h |
| Pitch deck (8 à 12 slides) avec les **vrais chiffres** | Maxime | Relu par Alexis |
| Plan B : vidéo de secours de la démo | Inès | La démo peut être montrée sans réseau |
| Passage de relais : **Mehdi fait la démo vendredi** (Alexis absent) | Alexis + Mehdi | Mehdi a fait la démo en entier une fois |
| 🎯 **Répétition de la démo à 18h** : démo principale, puis réparation automatique | Toute l'équipe | Démo réussie de bout en bout |
| **Gel du code** après la répétition | Toute l'équipe | Plus aucune fusion, sauf correctif urgent |

**Vendredi :** 11h, prototype + dépôt GitHub + vidéo de 5 min · 15h, pitch deck · ensuite, pitch (démo : Mehdi au clavier, Maxime à la parole).

## 4. Risques principaux

| Risque | Parade |
|---|---|
| L'agent se trompe de fiche ou lit mal une valeur | Contrôle d'identité + relance automatique, vérification, relecture ciblée (4 erreurs sur 205 fiches, toutes bloquées puis corrigées) |
| HubSpot refuse une fiche (champ disparu, règle nouvelle) | Réparation automatique par le skill HubSpot ; sinon la fiche est bloquée avec sa raison, rien de faux n'est envoyé |
| Plus de crédits H Company | ~0,008 à 0,015 $ par fiche : une démo de 6 fiches coûte ~0,11 $ ; clé d'Inès en secours |
| La démo live plante (réseau, agent) | Vidéo de secours ; les fiches déjà migrées restent visibles dans HubSpot et sur l'écran de suivi |
