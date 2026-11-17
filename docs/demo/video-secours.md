# Vidéo de secours de la démo (plan B)

Propriétaire : **Inès**. À enregistrer **jeudi 19/11**, avant la répétition de 18h.

**À quoi elle sert** : si le réseau ou l'agent lâche pendant le pitch de vendredi, Maxime lance cette vidéo à la place de la démo en direct (slide 4) et **parle par-dessus**, comme s'il faisait la démo. Elle suit donc exactement le même déroulé que la démo live.

| | |
|---|---|
| Durée visée | **2 min** (la démo live dure 2 min dans le pitch) |
| Son | **Sans voix** : c'est Maxime qui commente en direct. Couper le micro de l'enregistreur. |
| Outil | L'enregistreur d'écran (Loom ne fonctionnait pas mardi) |
| Résultat | Un fichier vidéo envoyé à Claude, converti en MP4 et déposé dans `docs/demo/` |

---

## 1. À préparer avec Alexis (avant d'enregistrer)

⚠️ **On ne relance pas de migration et on ne touche pas à HubSpot sans l'accord d'Alexis.** Lui envoyer :

> « Pour la vidéo de secours, j'ai besoin d'une petite migration de 6 fiches (C-0004 et les pièges C-0101 à C-0105) sur l'ancien CRM v1, pendant que j'enregistre mon écran. Tu peux la lancer à [heure] avec un run_id et me l'envoyer ? Et me dire comment montrer HubSpot sans toucher à la vue « Bascule » ? »

Pourquoi ces 6 fiches : en ~1 min (6 fiches en 62 s avec 3 agents, mesuré), on voit **tous les cas** à l'écran : des fiches migrées, un doublon bloqué, un e-mail invalide bloqué, un prénom vide bloqué, un téléphone « à vérifier », des majuscules corrigées, et des relectures par l'agent.

Ce qu'il faut recevoir d'Alexis :
- l'**identifiant du lancement** (`run_id`) ;
- l'**heure** à laquelle il lance la commande.

## 2. Les onglets à ouvrir (dans cet ordre)

| # | Onglet | Adresse | Réglage avant d'enregistrer |
|---|---|---|---|
| 1 | Ancien CRM v1 | https://projet-hackathon-uffi.vercel.app | Ouvrir dans une **fenêtre de navigation privée**, pour que la fenêtre « Message du jour » s'affiche |
| 2 | Écran de suivi, sur le lancement d'Alexis | `https://projet-hackathon-jow2.vercel.app/?run=<run_id>&total=6` | Ne l'ouvrir **qu'au moment du lancement** (étape 0:25) |
| 3 | HubSpot | Selon la consigne d'Alexis (sa vue « Bascule » ou ta propre vue) | **Ne rien modifier dans la vue « Bascule »** |

Zoom du navigateur à 100 %, fenêtre en plein écran, notifications coupées.

## 3. Le déroulé, seconde par seconde

| Temps | Onglet | Ce que tu fais | Ce que Maxime dira par-dessus |
|---|---|---|---|
| **0:00** | 1 · Ancien CRM | La fenêtre « Message du jour » est ouverte. Attends 2 s, puis ferme-la. | « Voici le logiciel de Camille, installé en 2010. » |
| **0:08** | 1 | Ouvre le menu **Fichier**, puis le menu **Aide** : montre qu'il n'y a pas d'export. | « On cherche le bouton d'export… il n'existe pas. » |
| **0:15** | 1 | Clique sur **« Voir la fiche »** d'un contact. Montre les 2 onglets et le bouton **« Afficher le numéro »** (sans cliquer). | « Les informations sont réparties, le numéro est caché. Un script ne s'en sort pas. » |
| **0:25** | 2 · Écran de suivi | Alexis lance la migration. Ouvre l'onglet 2. | « Thomas lance la migration. L'agent reçoit seulement l'adresse du logiciel. » |
| **0:30 → 1:20** | 2 | **Ne touche à rien** : les fiches arrivent une par une, les compteurs montent. Descends doucement quand le tableau se remplit. | « Trois agents lisent les fiches en même temps, comme un humain. Chaque fiche est vérifiée. » |
| **1:20** | 2 | Sur une fiche **migrée**, clique sur **« 📷 Voir »** : la capture de l'agent à gauche, les champs lus à droite. Attends 4 s, ferme. | « Pour chaque fiche, on garde la preuve : ce que l'agent a vu, et ce qu'il a lu. » |
| **1:30** | 2 | Montre une ligne **« Bloquée »** (doublon ou e-mail invalide) et sa raison, puis une ligne avec **« 🔁 relu par l'agent »**. | « Les fiches douteuses ne partent pas : Thomas les corrige à la main. » |
| **1:40** | 2 | Descends jusqu'à l'encadré **« Bilan »**. | « Le bilan : fiches envoyées, temps, coût. » |
| **1:50** | 3 · HubSpot | Montre les contacts arrivés (sans rien modifier). | « Et Camille travaille déjà dans HubSpot. » |
| **2:00** | — | Arrête l'enregistrement. | — |

Si la migration est plus lente que prévu : reste sur l'écran de suivi jusqu'à ce que les 6 fiches soient arrivées. On coupera le temps d'attente au montage (Claude peut accélérer ou couper un passage).

## 4. Après l'enregistrement

1. Regarde la vidéo une fois en entier : chaque étape est-elle visible et lisible ?
2. Vérifie qu'**aucune clé ni mot de passe** n'apparaît à l'écran (barre d'adresse, onglets, notifications).
3. Envoie le fichier à Claude : conversion en MP4, accélération des temps morts si besoin, dépôt dans `docs/demo/` et lien dans le README.
4. Préviens Maxime et Alexis que le plan B est prêt, et **mets la vidéo sur l'ordinateur du pitch**, pour pouvoir la lire **sans Internet**.

## 5. Checklist

- [ ] Accord d'Alexis et `run_id` reçus
- [ ] Les 3 onglets prêts, fenêtre privée pour l'ancien CRM
- [ ] Micro coupé
- [ ] Vidéo enregistrée (~2 min)
- [ ] Relue : tout est lisible, aucune clé à l'écran
- [ ] Déposée dans `docs/demo/` et copiée sur l'ordinateur du pitch
- [ ] Testée **sans Internet** pendant la répétition de 18h
