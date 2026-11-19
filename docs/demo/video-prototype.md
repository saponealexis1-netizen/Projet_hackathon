# Vidéo du prototype (5 min) — livrable 3, vendredi 11h

> **Remplacé** : la vidéo a été tournée le 19/11 sur le vrai prototype ([livrable 3](../checkpoint-3/)). Le texte à lire, calé sur cette vidéo, est dans [docs/checkpoint-3/voix-off-video-5min.md](../checkpoint-3/voix-off-video-5min.md). Ce script reste ici pour l'historique.

Propriétaire : **Inès** (voix et écran). À enregistrer **jeudi 19/11 entre 14h30 et 17h**, sur le site final (design de Mehdi) ; s'il n'est pas prêt à 15h30, sur le site actuel.

| | |
|---|---|
| Durée | **5 min maximum** (le texte fait ~4 min 30 à voix posée : marge de 30 s) |
| Voix | **Inès**, en direct pendant l'enregistrement. Tu peux lire le texte : c'est normal. |
| Caméra | Facultative (petite bulle dans un coin) |
| Outil | L'enregistreur d'écran (comme le mini-pitch) |
| Coût | 1 clic sur le bouton : ~0,11 $ d'agent H |
| Après | Envoyer la vidéo à Claude : MP4, coupe des temps d'attente, dépôt dans `docs/checkpoint-3/` et lien dans la fiche projet |

> **Différence avec la vidéo de secours** : la vidéo de secours est **muette** et dure 2 min (Maxime parle par-dessus pendant le pitch). Celle-ci est **commentée par toi** et présente **tout le prototype** au jury, qui la regardera seul.

---

## 1. Avant d'enregistrer

1. Message au groupe, **juste avant** : « je lance la migration ».
2. Vérifier que le bouton de l'écran de suivi dit **« Lancer la migration (agent réel) »**.
3. Ouvrir les onglets ci-dessous, zoom **125 %**, notifications coupées, plein écran.
4. Faire une lecture à voix haute avec un chronomètre (sans enregistrer).

| # | Onglet | Adresse |
|---|---|---|
| 1 | Page d'accueil du dépôt, partie « Le problème » | https://github.com/saponealexis1-netizen/Projet_hackathon |
| 2 | Schéma d'architecture | https://github.com/saponealexis1-netizen/Projet_hackathon/blob/main/docs/architecture/architecture.png |
| 3 | **Écran de suivi** (le bouton) | https://projet-hackathon-jow2.vercel.app/?run=tout |
| 4 | **Ancien CRM v1** (fenêtre de navigation privée) | https://projet-hackathon-uffi.vercel.app |
| 5 | Ancien CRM **v2** | https://projet-hackathon-uffi.vercel.app/v2 |
| 6 | **HubSpot**, vue « Bascule » (regarder seulement) | compte HubSpot de l'équipe |
| 7 | Réparation réussie du 18/11 (run 7) | https://projet-hackathon-jow2.vercel.app/?run=59f6de90-7885-42ea-abae-d6cffbc4f32b&total=2 |

---

## 2. Le script

> Les **temps** sont indicatifs. L'agent met ~45 s à envoyer les premières fiches et ~2 min 10 pour la dernière : on clique **tôt** (0:55) et on parle pendant qu'il travaille. Si l'attente est longue, continue de parler ou attends : Claude coupera au montage.

### 0:00 — Présentation · onglet 1
*À l'écran : la page d'accueil du dépôt, titre « Bascule ».*
> « Bonjour, je suis Inès, responsable IA de Bascule, équipe 8. Bascule, c'est un agent IA qui permet de changer de CRM sans perdre ses données, même quand l'ancien logiciel n'a ni export ni API. Je vais vous montrer le prototype en fonctionnement réel. »

### 0:20 — Le problème · onglet 1
*Descends jusqu'au tableau « Le problème ».*
> « Aujourd'hui, une petite agence qui veut quitter son vieux logiciel doit recopier ses fiches clients une par une. Pour 3 000 fiches, c'est environ 100 heures. Pour 44 % des PME, la migration est le premier obstacle au changement de CRM, et pour l'éditeur qui vend le nouveau CRM, c'est souvent la vente qui tombe. »

### 0:40 — La solution · onglet 2
*Le schéma. Suis le chemin avec la souris : ancien CRM → agent → vérification → envoi → HubSpot.*
> « Notre solution : un agent H Company lit l'ancien logiciel à l'écran, comme un humain. Notre application vérifie chaque fiche, la classe ok, à vérifier ou bloquée, puis envoie dans HubSpot celles qui ne sont pas bloquées. Tout est suivi en direct. »

### 0:55 — Lancement · onglet 3
*Clique sur **« Lancer la migration (agent réel) »**.*
> « Je lance une vraie migration sur six fiches, dont cinq pièges. L'agent ne connaît rien de ce logiciel : on lui donne seulement son adresse. »

### 1:05 — L'ancien CRM · onglet 4
*Ferme « Message du jour », ouvre **Fichier** (aucun export), ouvre une fiche, onglet **Coordonnées**, clique sur **Afficher le numéro**.*
> « Voici l'ancien logiciel, version 2010. Une fenêtre à fermer, aucun bouton d'export, des informations réparties sur deux onglets, et le numéro de téléphone caché derrière un bouton. Un script classique ne s'en sort pas. »

### 1:30 — Une autre version · onglet 5
*Montre la v2 quelques secondes : autre mise en page, « Raison sociale », « Voir le tél. ».*
> « Nous avons construit une deuxième version, avec une autre mise en page et d'autres libellés. Le même agent, avec exactement les mêmes consignes, a migré les deux : cent fiches sur cent exactes à chaque fois. C'est ce qu'un robot classique ne sait pas faire. »

### 1:50 — Les agents au travail · onglet 3
*Panneau « Agents en direct ».*
> « Pendant ce temps, trois agents travaillent en parallèle. On voit leur écran en direct : ils ferment la fenêtre, passent les pages, cliquent sur "Afficher", comme un humain. »

### 2:15 — La vérification · onglet 3
*Les fiches arrivent. Montre une ligne **Migrée**, une **Bloquée** (doublon ou e-mail invalide) avec sa raison, une ligne **🔁 relu par l'agent**, et une **À vérifier**.*
> « Chaque fiche est vérifiée avant HubSpot. Le doublon est bloqué. L'e-mail invalide est d'abord relu par l'agent, qui confirme, puis la fiche est bloquée avec sa raison. Le nom écrit en majuscules est corrigé. Rien de faux n'arrive dans HubSpot : Thomas, le responsable onboarding, ne traite que les cas douteux. »

### 2:50 — La preuve · onglet 3
*Clique sur **📷 Voir** d'une fiche migrée. Laisse 4 secondes, ferme.*
> « Et chaque donnée est prouvée : à gauche, ce que l'agent a vu à l'écran ; à droite, ce qu'il a lu. C'est notre réponse à la question "et si l'agent se trompe ?". »

### 3:10 — HubSpot · onglet 6
*Montre les contacts arrivés et la colonne « Bascule - ID ancien CRM ». Ne rien modifier.*
> « Les contacts sont dans HubSpot, chacun relié à sa fiche d'origine. Relancer une migration ne crée jamais de doublon. »

### 3:25 — La réparation automatique · onglet 7
*Montre la ligne **C-0004** (🩹 refusée → skill corrigé → envoyée), clique sur **📷 Voir** (« Erreur HubSpot », « Ce que les IA ont fait »), ferme, montre **C-0105**.*
> « Et si HubSpot change ? Ce que Bascule sait de HubSpot est rangé dans un "skill", tenu à jour par deux IA Hugging Face. Ici, on avait cassé volontairement un champ : HubSpot refuse la fiche, une première IA lit l'erreur et propose une correction, nos garde-fous la vérifient, une deuxième IA la valide, et la fiche repart. La suivante passe directement. Personne n'a touché au code. »

### 4:05 — Les chiffres · onglet 3, adresse `?run=tout`
*Recharge `?run=tout`, descends jusqu'au **Bilan**.*
> « Sur toute la base : cent fiches sur cent exactes, sur deux versions différentes du logiciel. Environ vingt secondes par fiche, et moins de deux centimes : trois mille fiches coûtent entre vingt-cinq et quarante-six dollars, contre une centaine d'heures de ressaisie. »

### 4:30 — Conclusion · onglet 3
*Reste sur le bilan.*
> « La suite : la connexion sécurisée aux logiciels protégés par un mot de passe, les notes et les pièces jointes, et d'autres CRM cibles. Bascule, c'est la migration qui ne bloque plus la vente. Merci ! »

### 4:45 — Fin
*Arrête l'enregistrement.*

---

## 3. Après l'enregistrement

- [ ] Réécoute une fois : chaque étape est visible, la voix est audible, **aucune clé** n'apparaît à l'écran.
- [ ] Envoie la vidéo à Claude (conversion, coupe des attentes, dépôt dans `docs/checkpoint-3/`, lien dans la fiche projet).
- [ ] Préviens Mehdi : c'est lui qui la dépose vendredi à 11h.
