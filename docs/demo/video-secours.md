# Vidéo de secours de la démo (plan B)

Propriétaire : **Inès**. À enregistrer **mercredi 18 ou jeudi 19/11, avant la répétition de 18h** (Alexis est absent vendredi : elle doit être prête avant).

**À quoi elle sert** : si le réseau ou l'agent lâche pendant le pitch de vendredi, Mehdi lance cette vidéo à la place de la démo en direct (slide 4) et **Maxime parle par-dessus**, comme s'il faisait la démo. Elle suit donc **le même déroulé que la démo live** ([README de la démo](README.md), section 2).

| | |
|---|---|
| Durée visée | **2 min** (+ 30 s facultatives sur la réparation) |
| Son | **Sans voix** : c'est Maxime qui commente en direct. Couper le micro de l'enregistreur. |
| Outil | L'enregistreur d'écran (Loom ne fonctionnait pas mardi) |
| Résultat | Un fichier vidéo envoyé à Claude, converti en MP4 et déposé dans `docs/demo/` |
| Coût | ~0,11 $ d'agent H (6 fiches) |

---

## 1. Avant d'enregistrer

**Plus besoin qu'Alexis lance la migration** : le bouton **« Lancer la migration (agent réel) »** de l'écran de suivi lance exactement les 6 fiches de la démo (C-0004 et les pièges C-0101 à C-0105) et les remet d'abord à zéro dans HubSpot.

⚠️ **Prévenir Alexis avant de cliquer** : une seule migration à la fois (3 agents maximum sur le compte H Company). Lui envoyer :

> « Je vais enregistrer la vidéo de secours à [heure] : je clique une fois sur "Lancer la migration (agent réel)" (6 fiches, ~0,11 $). Personne d'autre ne lance de migration à ce moment-là ? »

Vérifier aussi que le bouton dit bien **« Lancer la migration (agent réel) »**. S'il dit seulement « Lancer la migration », c'est le mode démo (données simulées) : ne pas enregistrer, prévenir Alexis.

## 2. Les onglets à ouvrir (dans cet ordre)

| # | Onglet | Adresse | Réglage |
|---|---|---|---|
| 1 | **Écran de suivi** (le bouton est ici) | https://projet-hackathon-jow2.vercel.app/?run=tout | — |
| 2 | **Ancien CRM** v1 | https://projet-hackathon-uffi.vercel.app | **Fenêtre de navigation privée**, pour que « Message du jour » s'affiche |
| 3 | **HubSpot**, vue « Bascule » | (compte HubSpot de l'équipe) | **Regarder seulement** : ne rien modifier dans la vue « Bascule » |
| 4 | *(facultatif)* Réparation réussie du 18/11 | https://projet-hackathon-jow2.vercel.app/?run=59f6de90-7885-42ea-abae-d6cffbc4f32b&total=2 | — |

Zoom du navigateur à 125 % (comme vendredi), fenêtre en plein écran, notifications coupées.

## 3. Le déroulé (identique à la démo live)

> Mesuré le 17/11 : les premières fiches arrivent **~45 s** après le clic, la dernière **~2 min 10 s** après. On clique donc **à la première seconde**, et on montre l'ancien CRM pendant que l'agent démarre. Les temps morts seront coupés au montage.

| Temps | Onglet | Ce que tu fais | Ce que Maxime dira par-dessus |
|---|---|---|---|
| **0:00** | 1 · Écran de suivi | Clique sur **« Lancer la migration (agent réel) »** | « On lance Bascule sur 6 fiches. L'agent ne connaît rien de ce logiciel : on lui donne seulement l'adresse. » |
| **0:05** | 2 · Ancien CRM | Ferme « Message du jour », ouvre **Fichier** (aucun export), ouvre une fiche, onglet **Coordonnées**, clique sur **Afficher le numéro** | « Voici le logiciel de Camille, installé en 2010. Aucun export, aucune API. Le numéro est même caché derrière un bouton. » |
| **0:35** | 1 · Écran de suivi, panneau **« Agents en direct »** | Ne touche à rien : les écrans des agents se rafraîchissent | « Voilà les agents H Company : chacun voit l'écran, ferme la fenêtre, passe les pages, clique sur Afficher… comme un humain. » |
| **1:00** | 1 · les fiches arrivent | Clique sur **📷 Voir** d'une fiche migrée (4 s), ferme ; montre une ligne **Bloquée** et une ligne **🔁 relu par l'agent** | « Chaque fiche est vérifiée avant HubSpot. Le doublon est bloqué, l'e-mail invalide est relu puis bloqué, le nom en majuscules est corrigé. » |
| **1:30** | 3 · HubSpot | Montre les contacts arrivés et la colonne « Bascule - ID ancien CRM » (sans rien modifier) | « Les contacts sont dans HubSpot, chacun relié à sa fiche d'origine. Rien de faux n'y est arrivé. » |
| **1:45** | 1 · `?run=tout` | Recharge `?run=tout`, descends jusqu'au **Bilan** | « Et sur toute la base : 100 fiches sur 100 exactes, chacune prouvée par sa capture d'écran. » |
| **2:00** | — | *(sans la partie facultative : arrête l'enregistrement)* | « Thomas n'a rien recopié. Camille travaille déjà dans HubSpot. » |

**Facultatif : la réparation (30 s)**, si on veut pouvoir la montrer aussi sans réseau.

| Temps | Onglet | Ce que tu fais | Ce que Maxime dira par-dessus |
|---|---|---|---|
| **2:00** | 4 · Réparation du 18/11 | Montre la ligne **C-0004** : 🩹 ❌ refusée par HubSpot → 🧠 skill v2 corrigé par les 2 IA → ✅ envoyée après correction | « Et si HubSpot change ? Ici, on avait cassé volontairement un champ. HubSpot refuse la fiche, deux IA réparent le skill, la fiche repart. » |
| **2:15** | 4 | Clique sur **📷 Voir** de C-0004 (« Erreur HubSpot », « Ce que les IA ont fait »), ferme ; montre **C-0105** passée directement | « La fiche suivante passe directement : Bascule a appris, sans toucher au code. » |
| **2:30** | — | Arrête l'enregistrement | — |

Si la migration est plus lente que prévu : reste sur l'écran de suivi jusqu'à ce que les 6 fiches soient arrivées. Claude coupera ou accélérera l'attente au montage.

## 4. Après l'enregistrement

1. Regarde la vidéo une fois en entier : chaque étape est-elle visible et lisible ?
2. Vérifie qu'**aucune clé ni mot de passe** n'apparaît à l'écran (barre d'adresse, onglets, notifications).
3. Envoie le fichier à Claude : conversion en MP4, coupe des temps morts, dépôt dans `docs/demo/` et lien dans le README de la démo.
4. Préviens Maxime, Mehdi et Alexis que le plan B est prêt, et **copie la vidéo sur l'ordinateur du pitch**, pour pouvoir la lire **sans Internet**.

## 5. Checklist

- [ ] Alexis prévenu, aucune autre migration en cours
- [ ] Le bouton dit « Lancer la migration (agent réel) »
- [ ] Les onglets prêts, fenêtre privée pour l'ancien CRM, zoom 125 %
- [ ] Micro coupé
- [ ] Vidéo enregistrée (~2 min, + 30 s de réparation si possible)
- [ ] Relue : tout est lisible, aucune clé à l'écran
- [ ] Déposée dans `docs/demo/` et copiée sur l'ordinateur du pitch
- [ ] Testée **sans Internet** pendant la répétition de 18h
