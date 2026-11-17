# Bascule — Roadmap jusqu'à jeudi

> État au **mardi 17/11/2026 au matin**, à mettre à jour avant le dépôt de mercredi 17h.
> Règle de l'équipe : **on n'attend pas le lendemain**. Dès qu'une tâche est finie, on enchaîne sur la suivante.

---

## 1. Déjà fait ✅

| Brique | Qui |
|---|---|
| Cadrage et décisions du MVP (D1 à D11) | Alexis |
| Format commun des contacts + 20 contacts d'exemple + base Supabase | Alexis |
| Vérification des fiches (ok / à vérifier / bloquée) | Inès |
| Écran de suivi : bouton « Lancer la migration » et encadré « Bilan » | Inès |
| Socle de l'ancien CRM simulé | Victoria |
| Business model et parcours utilisateur | Maxime |
| Premier test de l'agent H sur un site public : 3 fiches sur 3, ~48 s et ~0,02 $ par fiche | Maxime |

## 2. Mercredi — Premier parcours complet

| Tâche | Qui | Terminé quand… |
|---|---|---|
| Ancien CRM : liste et fiches des 20 contacts, sans export, en ligne sur Vercel | Victoria | On ouvre chaque fiche dans le navigateur |
| Agent H qui lit les fiches de l'ancien CRM | Victoria + Inès | 5 fiches extraites d'affilée |
| Envoi des contacts vérifiés vers HubSpot | Alexis | 5 contacts arrivent dans HubSpot |
| Schéma d'architecture | Victoria | Dans `docs/architecture/` |
| 🎯 **Parcours complet : ancien CRM → agent → vérification → HubSpot** | Toute l'équipe | **Sur 5 fiches, en un seul lancement** |
| 📦 **Dépôt du livrable 2** (parcours, architecture, Loom, roadmap) | Maxime, dépôt par Alexis | **Avant 17h** |

## 3. Jeudi — Fiabiliser et mesurer

| Tâche | Qui | Terminé quand… |
|---|---|---|
| Passage à 20 fiches + cas pièges (doublons, champs vides) | Victoria + Inès | 20 fiches traitées en un lancement |
| Mesures : taux de réussite, temps et coût par fiche | Alexis | Tableau de chiffres dans `pipeline/metrics/` |
| Pitch deck (8 à 12 slides) avec les vrais chiffres | Maxime | Relu par Alexis |
| Plan B : vidéo de secours de la démo | Victoria | La démo peut être montrée sans réseau |
| 🎯 **Répétition de la démo à 18h** | Toute l'équipe | Démo réussie de bout en bout |

**Vendredi :** 11h, prototype + dépôt GitHub + vidéo de 5 min · 15h, pitch deck · ensuite, pitch.

## 4. Risques principaux

| Risque | Parade |
|---|---|
| L'ancien CRM n'est pas prêt à temps (Victoria absente mardi) | Priorité n°1 de mercredi ; l'agent est déjà testé sur un site public en attendant |
| L'agent se trompe ou bloque sur une fiche | Vérification automatique + relance de la fiche |
| La démo live plante | Vidéo de secours prête jeudi |
