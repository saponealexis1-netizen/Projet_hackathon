# Script de l'oral — vendredi 20/11

**Sur scène :** Maxime (slides 1 à 9), Inès et Mehdi (démo, slide 10).
**Support :** [Bascule_Pitch_Deck.pdf](Bascule_Pitch_Deck.pdf), puis la vidéo **sans son** [`video-sans-voix-pour-oral.mp4`](../checkpoint-3/video-sans-voix-pour-oral.mp4), **lue en vitesse ×1,5**.
**Durée visée :** environ 6 min (≈ 2 min 50 de slides, ≈ 3 min 05 de vidéo à ×1,5, 5 s de conclusion), puis les questions. Les textes sont calibrés pour un débit posé (2,5 mots par seconde au plus) : si vous débordez en répétition, raccourcissez d'abord les slides 6 et 8.

## Avant de commencer

- Ouvrir la vidéo à l'avance dans le lecteur (VLC : *Lecture › Vitesse › Plus rapide* jusqu'à **1,5×** ; navigateur : clic droit › vitesse, ou l'outil du lecteur). Plein écran, son coupé, **mise en pause sur la première image**.
- Qui lance la vidéo : **Mehdi** (au clavier), au moment où Maxime dit « Inès, Mehdi ».
- Le compteur du lecteur affiche le **temps de la vidéo**, pas le temps réel : les repères ci-dessous (`0:52`, `2:58`…) sont ceux du compteur. À ×1,5, chaque séquence défile 1,5 fois plus vite que son temps affiché.
- Les textes de la démo reprennent la voix off d'Inès de la vidéo du livrable 3, raccourcis pour tenir à ×1,5.

---

## Partie 1 — Maxime, slides 1 à 9 (≈ 2 min 50)

**Slide 1 · Bascule** *(≈ 15 s)*
> Camille dirige une petite agence : trois mille fiches clients dans un logiciel de 2010. Elle veut passer sur HubSpot, cherche le bouton « exporter »… il n'existe pas. Nous sommes Bascule, l'agent qui la sort de là.

**Slide 2 · Le problème** *(≈ 25 s)*
> Camille n'est pas un cas isolé : pour 44 % des PME, la migration est le premier obstacle au changement de CRM. Sans export et sans API, aucun outil de migration ne marche : il reste à tout recopier. Trois mille fiches, c'est cent heures. Et pour Thomas, qui vend HubSpot à Camille, c'est souvent la vente qui tombe.

**Slide 3 · L'équipe** *(≈ 11 s)*
> Nous sommes la Team 8, six rôles. Aujourd'hui, je suis Maxime, CEO, avec Inès, responsable IA, et Mehdi, responsable produit, qui vont vous montrer la démo.

**Slide 4 · La solution** *(≈ 17 s)*
> Bascule commence là où les outils de migration s'arrêtent. Nos agents H Company lisent l'écran de l'ancien logiciel, comme un humain. Seules les fiches vérifiées sont créées dans HubSpot, avec une capture de chacune. Et si HubSpot change, Bascule se répare.

**Slide 5 · Business model** *(≈ 23 s)*
> Ce n'est pas la PME qui paie, c'est l'éditeur ou l'agence qui vend le nouveau CRM : il facture déjà l'onboarding, mille cinq cents à trois mille cinq cents dollars chez HubSpot. Nous lui vendons la migration quatre cent quatre-vingt-dix euros jusqu'à deux mille fiches, neuf cent quatre-vingt-dix au-delà. Des prix encore à tester auprès d'agences.

**Slide 6 · Go-to-market** *(≈ 20 s)*
> On commence par les agences partenaires HubSpot en France : elles butent sur des migrations chaque semaine. Il y en a six à sept mille cinq cents dans le monde, toutes dans l'annuaire HubSpot. Ensuite, les éditeurs de logiciels métier, puis une application sur la marketplace HubSpot.

**Slide 7 · Architecture et Agent API** *(≈ 25 s)*
> L'agent H Company est utilisé là où il est indispensable : lire un logiciel fermé. Il ne reçoit que l'adresse : le même agent a migré deux logiciels différents sans rien reconfigurer. Autour de lui, des garde-fous : réponse imposée, contrôle de la fiche ouverte, relecture, et une capture d'écran de chaque fiche. Vers HubSpot, on passe par son API.

**Slide 8 · Limites et roadmap** *(≈ 16 s)*
> Notre MVP migre des contacts, depuis un logiciel sans mot de passe, vers HubSpot, sur des données fictives. La suite : les notes et pièces jointes, la connexion sécurisée, d'autres CRM, et un pilote avec une agence partenaire.

**Slide 9 · Coût de run** *(≈ 16 s)*
> Faire tourner Bascule coûte environ un centime par fiche, mesuré sur plus de deux cents fiches. Trois mille fiches, c'est vingt-cinq à quarante-cinq dollars de crédits, pour neuf cent quatre-vingt-dix euros facturés : environ 95 % de marge.

**Slide 10 · Démo** *(≈ 5 s)*
> Assez de slides : voici le vrai prototype, filmé hier. Inès, Mehdi.

*Mehdi lance la vidéo (×1,5).*

---

## Partie 2 — Inès, vidéo de 0:00 à 0:52 (≈ 35 s réelles)

| Compteur | À l'écran | Texte d'Inès |
|---|---|---|
| **0:00** | Carton « Bascule » | « Tout ce que vous allez voir est réel, sans trucage. » |
| **0:07** | Ancien CRM v1 : fenêtre fermée, menu Fichier, fiche, bouton « Afficher le numéro » | « Voici le logiciel de Camille, version 2010. Une fenêtre à fermer, un menu Fichier sans aucun export, une fiche sur deux onglets, et le téléphone caché derrière un bouton. » |
| **0:36** | Ancien CRM v2 : autre mise en page, « Voir le tél. » | « Et voici une deuxième version, avec une autre mise en page. Notre agent lit les deux avec exactement les mêmes consignes. Mehdi. » |

---

## Partie 3 — Mehdi, vidéo de 0:52 à 2:58 (≈ 1 min 24 réelles)

Version en temps réel, pour le chronomètre : [script-mehdi.md](script-mehdi.md).

| Compteur | À l'écran | Texte de Mehdi |
|---|---|---|
| **0:52** | Supabase : table `legacy_contacts`, puis `migration_log` | « Derrière l'ancien logiciel, une base Supabase de cent cinq contacts fictifs, dont cinq fiches pièges : un doublon, un e-mail invalide, un prénom vide, un téléphone incomplet. Et voici le journal où Bascule note chaque fiche migrée. » |
| **1:17** | Écran de suivi : clic sur « Lancer la migration (agent réel) », la barre d'étapes s'anime | « On lance une vraie migration sur six fiches, dont les cinq pièges. L'agent ne reçoit que l'adresse du logiciel. » |
| **1:33** | Panneau « Agents en direct » : trois écrans d'agents (accéléré) | « Trois agents H Company travaillent en parallèle. On voit leur écran en direct : ils ferment la fenêtre, ouvrent chaque fiche, cliquent sur « Afficher le numéro », comme un humain. Chaque fiche lue est aussitôt vérifiée. » |
| **2:07** | Le bilan remonte : 3 / 6, 50 % | « Migration terminée en moins de deux minutes. Trois fiches partent dans HubSpot ; les trois autres sont nos pièges, et elles sont bloquées. » |
| **2:23** | « Voir » sur C-0004, puis C-0102 (e-mail invalide relu et bloqué) | « Chaque donnée est prouvée : à gauche ce que l'agent a vu, à droite ce qu'il a lu. Ici, un e-mail invalide : l'agent l'a relu pour confirmer, puis la fiche a été bloquée avec sa raison. Rien de faux n'arrive dans HubSpot. Inès. » |

---

## Partie 4 — Inès, vidéo de 2:58 à la fin (≈ 1 min 06 réelles)

| Compteur | À l'écran | Texte d'Inès |
|---|---|---|
| **2:58** | HubSpot : la vue « Bascule », puis une fiche contact | « Dans HubSpot, les contacts sont là, chacun relié à sa fiche d'origine par son identifiant. Relancer une migration ne crée jamais de doublon. » |
| **3:19** | Nouvelle migration de deux fiches (accéléré) | « Et si HubSpot change ? Ici, on casse volontairement un champ : il n'existe plus. » |
| **3:33** | Ligne C-0004 « Refusée par HubSpot → skill v2 corrigé par les 2 IA → envoyée après correction » | « HubSpot refuse la fiche. Une première IA lit l'erreur et propose une correction, nos garde-fous la vérifient, une deuxième IA la valide, et la fiche repart. Personne n'a touché au code. » |
| **4:00** | La vue complète : 105 fiches, bilan | « Sur toute la base : cent fiches sur cent exactes, sur deux logiciels différents, chacune prouvée par sa capture d'écran. » |
| **4:21** | Cartons des chiffres, puis de fin | « Environ un centime par fiche. Thomas n'a rien recopié, et Camille travaille déjà dans HubSpot. » |

---

## Partie 5 — Maxime, conclusion (≈ 5 s)

> Bascule, c'est la migration qui ne bloque plus la vente. Merci ! Place à vos questions.

---

## Questions probables (réponses courtes)

| Question | Qui | Réponse |
|---|---|---|
| « Et si l'agent se trompe ? » | Inès | Il a ouvert la mauvaise fiche 4 fois sur 205 : notre contrôle les a bloquées, puis l'agent les a relues. Aucune mauvaise fiche n'est partie, et chacune a sa capture d'écran. |
| « Pourquoi pas un script ou un robot RPA ? » | Inès | Pas d'API ni d'export, et aucun réglage : le même agent a migré deux logiciels différents. Un robot RPA aurait dû être reconfiguré. |
| « Et la sécurité des données ? » | Maxime | L'agent ne fait que lire, sur les serveurs européens de H Company. La connexion par mot de passe passera par le coffre-fort de H Company. |
| « Avez-vous parlé à des clients ? » | Maxime | Pas encore : cette semaine, on a prouvé que la technologie marche. Nos prix sont des hypothèses ; la prochaine étape, ce sont des entretiens avec des agences partenaires HubSpot. |
| « Combien de temps pour une vraie migration ? » | Mehdi | 105 fiches en 17 minutes avec 3 agents. 3 000 fiches : environ 8 h, ou 2 h 30 avec 10 agents. |
