# Checkpoint 3 — Produit

**Projet :** Bascule — *Changez de logiciel, sans perdre vos données.*
**Événement :** Hackathon Eugenia 2026 « Build The Future » · Team 8
**Échéance :** vendredi 20 novembre 2026, **11h** · dépôt : **Mehdi** (Alexis est absent)

---

## Contenu du livrable

| # | Élément demandé | Où | État |
|---|---|---|---|
| 01 | **Prototype** en ligne | [Ancien CRM v1](https://projet-hackathon-uffi.vercel.app) · [v2](https://projet-hackathon-uffi.vercel.app/v2) · [Écran de suivi de la vraie migration](https://projet-hackathon-jow2.vercel.app/?run=tout) | ✅ En ligne, testé en réel |
| 02 | **Fiche projet** | [fiche-projet.md](fiche-projet.md) | ✅ Version finale |
| 03 | **Dépôt GitHub** | https://github.com/saponealexis1-netizen/Projet_hackathon (page d'accueil : « Tester en 2 minutes », résultats, architecture) | ✅ À jour |
| 04 | **Vidéo de démonstration** | [bascule-video-5min.mp4](https://github.com/saponealexis1-netizen/Projet_hackathon/raw/main/docs/checkpoint-3/bascule-video-5min.mp4) (4 min 38, le lien la télécharge) | ✅ Tournée le 19/11 · voix off d'Inès à ajouter (même lien) |

## La vidéo de démonstration

Tournée le 19/11 sur le **vrai prototype** : une vraie migration de 6 fiches et une vraie réparation, sans trucage.

| Temps | Séquence |
|---|---|
| 0:00 | Titre |
| 0:07 | L'ancien CRM v1 : aucun export, numéro caché derrière un bouton |
| 0:36 | L'ancien CRM v2 : autre mise en page, même agent sans réglage |
| 0:53 | Les données de départ dans Supabase (105 contacts dont 5 pièges, journal des migrations) |
| 1:17 | Un clic : la vraie migration démarre |
| 1:33 | Les 3 agents H Company en direct (accéléré ×3) |
| 2:07 | Le bilan : 3 fiches envoyées, les 3 pièges bloqués |
| 2:23 | Chaque fiche vérifiée et prouvée (capture et champs lus, e-mail invalide relu puis bloqué) |
| 2:58 | Le résultat dans HubSpot |
| 3:19 | Panne volontaire côté HubSpot, puis réparation automatique par 2 IA |
| 4:00 | Toute la base : 105 fiches, bilan |
| 4:21 | Chiffres clés et fin |

Fichiers :
- [voix-off-video-5min.md](voix-off-video-5min.md) : le texte d'Inès, en 13 blocs calés sur la vidéo ;
- [textes-video-5min.md](textes-video-5min.md) : titres et sous-titres à incruster, et ce que dit l'orateur si la vidéo passe pendant l'oral.

## Les chiffres (réels, mesurés)

| | |
|---|---|
| Logiciels migrés sans rien reconfigurer | **2** (v1 et v2) |
| Fiches exactes (9 champs sur 9) | **100 / 100** sur chacun |
| Fiches pièges traitées comme prévu | **5 / 5** |
| Mauvaise fiche envoyée dans HubSpot | **0** |
| Durée réelle, 3 agents | **16,9 min** pour 105 fiches (médiane 21 s par fiche) |
| Coût de l'agent | **~0,008 à 0,015 $** par fiche · 3 000 fiches ≈ 25 à 45 $ |
| Réparation automatique | Champ HubSpot disparu : fiche réparée et renvoyée (essais réels des 18 et 19/11) |

## Avant 11h (Mehdi)

- [ ] Fusionner les PR marquées « PRÊT POUR MERGE » restantes (onglet *Pull requests*), puis **ne plus rien fusionner**.
- [ ] Ouvrir, **sans être connecté** (navigation privée) : les 3 liens du prototype, le dépôt GitHub, la fiche projet, le lien de la vidéo (elle doit se télécharger).
- [ ] Si Inès a envoyé sa voix off et que Claude a monté la version finale : vérifier que le lien de la vidéo donne bien la version avec voix.
- [ ] Déposer sur **inside.eugenia.com** avec le message ci-dessous.

## Message de dépôt (à copier)

```
Team 8 — Bascule — Livrable 3 : produit

Bascule migre les fiches clients d'un vieux logiciel sans export ni API vers HubSpot : un agent H Company lit l'ancien logiciel à l'écran comme un humain, chaque fiche est vérifiée et prouvée par une capture d'écran, puis envoyée dans HubSpot.

🎥 Vidéo de démonstration (4 min 38, prototype réel ; le lien télécharge la vidéo) :
https://github.com/saponealexis1-netizen/Projet_hackathon/raw/main/docs/checkpoint-3/bascule-video-5min.mp4

🖥️ Prototype en ligne :
• Ancien CRM simulé (v1) : https://projet-hackathon-uffi.vercel.app
• Ancien CRM simulé (v2) : https://projet-hackathon-uffi.vercel.app/v2
• Écran de suivi de la vraie migration : https://projet-hackathon-jow2.vercel.app/?run=tout

📄 Fiche projet :
https://github.com/saponealexis1-netizen/Projet_hackathon/blob/main/docs/checkpoint-3/fiche-projet.md

📁 Dépôt GitHub (README : « Tester en 2 minutes », résultats, architecture) :
https://github.com/saponealexis1-netizen/Projet_hackathon

Dossier complet du livrable :
https://github.com/saponealexis1-netizen/Projet_hackathon/tree/main/docs/checkpoint-3
```

## Plans B

| Problème | Que faire |
|---|---|
| La vidéo ne s'ouvre pas dans le navigateur | C'est normal sur GitHub : le lien **télécharge** la vidéo, qui s'ouvre ensuite sur l'ordinateur |
| Le formulaire Eugenia demande un fichier vidéo, pas un lien | Télécharger la vidéo avec le lien ci-dessus, puis la joindre |
| Le formulaire a des rubriques précises | Copier-coller depuis [fiche-projet.md](fiche-projet.md), rubrique par rubrique |
| Un lien du prototype ne s'ouvre pas | Prévenir l'équipe immédiatement ; la vidéo montre tout le prototype en fonctionnement réel |
