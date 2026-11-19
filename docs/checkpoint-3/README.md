# Checkpoint 3 — Produit

**Projet :** Bascule — *Changez de logiciel, sans perdre vos données.*
**Événement :** Hackathon Eugenia 2026 « Build The Future » · Team 8
**Échéance :** vendredi 20 novembre 2026, **11h**

---

## Contenu du livrable

| # | Élément demandé | Où | État |
|---|---|---|---|
| 01 | **Prototype** en ligne | [Ancien CRM v1](https://projet-hackathon-uffi.vercel.app) · [v2](https://projet-hackathon-uffi.vercel.app/v2) · [Écran de suivi de la vraie migration](https://projet-hackathon-jow2.vercel.app/?run=tout) | ✅ En ligne, testé en réel |
| 02 | **Fiche projet** | [fiche-projet.md](fiche-projet.md) | ✅ Version finale |
| 03 | **Dépôt GitHub** | https://github.com/saponealexis1-netizen/Projet_hackathon (page d'accueil : « Tester en 2 minutes », résultats, architecture) | ✅ À jour |
| 04 | **Vidéo de démonstration** | [video-finale-livrable-3.mp4](https://github.com/saponealexis1-netizen/Projet_hackathon/raw/main/docs/checkpoint-3/video-finale-livrable-3.mp4) (3 min 01, voix d'Inès, le lien la télécharge) | ✅ Finale |

## Les deux vidéos (ne pas les mélanger)

| Fichier | Durée | Pour quoi |
|---|---|---|
| **[video-finale-livrable-3.mp4](https://github.com/saponealexis1-netizen/Projet_hackathon/raw/main/docs/checkpoint-3/video-finale-livrable-3.mp4)** | 3 min 01 | **La vidéo du livrable 3**, à déposer. Avec la voix d'Inès ([texte](voix-off-video-5min.md)) : elle se comprend seule. |
| [video-sans-voix-pour-oral.mp4](https://github.com/saponealexis1-netizen/Projet_hackathon/raw/main/docs/checkpoint-3/video-sans-voix-pour-oral.mp4) | 4 min 38 | Les mêmes images, plus lentes et **sans son**, à passer derrière l'orateur pendant le pitch ([textes de l'orateur](textes-video-5min.md)). **Ne pas déposer.** |

Les deux ont été tournées le 19/11 sur le **vrai prototype** : une vraie migration de 6 fiches et une vraie réparation, sans trucage.

### Déroulé de la vidéo finale

| Temps | Séquence |
|---|---|
| 0:00 | Titre |
| 0:08 | L'ancien CRM v1 : aucun export, numéro caché derrière un bouton |
| 0:30 | L'ancien CRM v2 : autre mise en page, même agent sans réglage |
| 0:43 | Les données de départ dans Supabase (105 contacts dont 5 pièges, journal des migrations) |
| 1:02 | Un clic : la vraie migration démarre |
| 1:11 | Les 3 agents H Company en direct (accéléré) |
| 1:29 | Le bilan : 3 fiches envoyées, les 3 pièges bloqués |
| 1:39 | Chaque fiche vérifiée et prouvée (capture et champs lus, e-mail invalide relu puis bloqué) |
| 2:00 | Le résultat dans HubSpot |
| 2:11 | Panne volontaire côté HubSpot |
| 2:21 | Réparation automatique par 2 IA, la fiche repart |
| 2:36 | Toute la base : 105 fiches, bilan |
| 2:47 | Chiffres clés et fin |

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

## Avant le dépôt

- [ ] Ouvrir, **sans être connecté** (navigation privée) : les 3 liens du prototype, le dépôt GitHub, la fiche projet, et le lien de la **vidéo finale** (elle doit se télécharger et durer 3 min 01, avec la voix d'Inès).
- [ ] Vérifier qu'aucune PR utile n'est restée ouverte (onglet *Pull requests*).
- [ ] Déposer sur **inside.eugenia.com** avec le message ci-dessous.

## Message de dépôt (à copier)

```
Team 8 — Bascule — Livrable 3 : produit

Bascule migre les fiches clients d'un vieux logiciel sans export ni API vers HubSpot : un agent H Company lit l'ancien logiciel à l'écran comme un humain, chaque fiche est vérifiée et prouvée par une capture d'écran, puis envoyée dans HubSpot.

🎥 Vidéo de démonstration (3 min, prototype réel ; le lien télécharge la vidéo) :
https://github.com/saponealexis1-netizen/Projet_hackathon/raw/main/docs/checkpoint-3/video-finale-livrable-3.mp4

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
| Le formulaire Eugenia demande un fichier vidéo, pas un lien | Télécharger `video-finale-livrable-3.mp4` avec le lien ci-dessus, puis la joindre |
| Le formulaire a des rubriques précises | Copier-coller depuis [fiche-projet.md](fiche-projet.md), rubrique par rubrique |
| Un lien du prototype ne s'ouvre pas | Prévenir l'équipe immédiatement ; la vidéo montre tout le prototype en fonctionnement réel |
