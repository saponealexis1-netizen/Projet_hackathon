# Voix off de la vidéo de 5 min — calée sur la vidéo

Vidéo : [`bascule-video-5min.mp4`](https://github.com/saponealexis1-netizen/Projet_hackathon/raw/main/docs/checkpoint-3/bascule-video-5min.mp4) (4 min 38, tournée le 19/11 sur le vrai prototype).
Texte : **Inès** (repris de son script [`video-prototype.md`](../demo/video-prototype.md), adapté à l'ordre et aux durées de la vidéo).

## Comment enregistrer

- **Seulement l'audio**, au téléphone (dictaphone), dans un endroit calme, téléphone à 20 cm.
- Lire **les blocs dans l'ordre**, **sans lire les temps**, avec **2 secondes de silence entre chaque bloc** : Claude cale ensuite chaque bloc au début de sa séquence.
- Ton posé : chaque bloc tient dans sa séquence à un rythme calme (2,4 mots par seconde au plus). S'il en dépasse un peu, Claude prolonge l'image.
- En cas d'erreur : pause, puis relire **toute la phrase**. Claude garde la dernière version.
- Envoyer le fichier audio tel quel (m4a, mp3…).

---

## Le texte

**Bloc 1 · 0:00 – 0:07 · Titre**
*À l'écran : le carton « Bascule ».*
> Bonjour, je suis Inès, de l'équipe 8. Voici Bascule : changez de logiciel, sans perdre vos données.

**Bloc 2 · 0:07 – 0:36 · L'ancien logiciel**
*À l'écran : l'ancien CRM v1. Fenêtre « Message du jour » fermée, menu Fichier, fiche C-0004, onglet Coordonnées, bouton « Afficher le numéro ».*
> Une petite agence veut passer sur HubSpot, mais son logiciel de 2010 n'a ni export, ni API. Une fenêtre à fermer au démarrage, un menu Fichier sans aucun export, des informations réparties sur deux onglets, et le numéro de téléphone caché derrière un bouton. Pour trois mille fiches, c'est une centaine d'heures de ressaisie.

**Bloc 3 · 0:36 – 0:53 · Une autre version**
*À l'écran : la v2, autre mise en page, fiche C-0004, bouton « Voir le tél. ».*
> Voici une deuxième version du logiciel, avec une autre mise en page et d'autres libellés. Notre agent lit les deux avec exactement les mêmes consignes. C'est ce qu'un robot classique ne sait pas faire.

**Bloc 4 · 0:53 – 1:17 · Les données de départ**
*À l'écran : Supabase, schéma « hackathon », table legacy_contacts, puis migration_log.*
> Derrière l'ancien logiciel, une base Supabase de cent cinq contacts fictifs, dont cinq fiches pièges : un doublon, un e-mail invalide, un prénom vide, un téléphone incomplet, un nom en majuscules. Et voici le journal où Bascule note chaque fiche migrée.

**Bloc 5 · 1:17 – 1:33 · Le lancement**
*À l'écran : l'écran de suivi, clic sur « Lancer la migration (agent réel) », la barre d'étapes s'anime.*
> Je lance une vraie migration sur six fiches, dont les cinq pièges. L'agent ne connaît rien de ce logiciel : on lui donne seulement son adresse.

**Bloc 6 · 1:33 – 2:07 · Les agents au travail** *(images accélérées)*
*À l'écran : le panneau « Agents en direct », trois écrans d'agents.*
> Trois agents H Company travaillent en parallèle. On voit leur écran en direct : ils ferment la fenêtre, passent les pages, ouvrent chaque fiche et cliquent sur « Afficher le numéro », comme un humain. Chaque fiche lue est aussitôt vérifiée, puis envoyée dans HubSpot si elle est sûre.

**Bloc 7 · 2:07 – 2:23 · Le bilan**
*À l'écran : le bilan remonte, 3 / 6 envoyées, 50 %.*
> Migration terminée en moins de deux minutes. Trois fiches sur six partent dans HubSpot. Les trois autres sont nos pièges : elles sont bloquées.

**Bloc 8 · 2:23 – 2:58 · La vérification et la preuve**
*À l'écran : « Voir » sur C-0004 (capture et champs lus), puis C-0102, l'e-mail invalide relu et bloqué.*
> Chaque donnée est prouvée : à gauche, ce que l'agent a vu à l'écran ; à droite, ce qu'il a lu. Ici, un e-mail invalide : l'agent l'a relu pour confirmer, puis la fiche a été bloquée avec sa raison. Rien de faux n'arrive dans HubSpot : Thomas, le responsable onboarding, ne traite que les cas douteux.

**Bloc 9 · 2:58 – 3:19 · HubSpot**
*À l'écran : HubSpot, la vue « Bascule », puis une fiche contact.*
> Dans HubSpot, les contacts sont là, chacun relié à sa fiche d'origine par son identifiant de l'ancien logiciel. Relancer une migration ne crée jamais de doublon.

**Bloc 10 · 3:19 – 3:33 · Et si HubSpot change ?** *(images accélérées)*
*À l'écran : une nouvelle migration de deux fiches.*
> Et si HubSpot change ? Ici, on casse volontairement un champ : la fonction des contacts part vers une propriété qui n'existe plus.

**Bloc 11 · 3:33 – 4:00 · La réparation automatique**
*À l'écran : la ligne C-0004 « Refusée par HubSpot → skill v2 corrigé par les 2 IA → envoyée après correction », puis « Voir », puis C-0105.*
> HubSpot refuse la fiche. Une première IA lit l'erreur et propose une correction, nos garde-fous la vérifient, une deuxième IA la valide, et la fiche repart. La suivante passe directement. Personne n'a touché au code.

**Bloc 12 · 4:00 – 4:21 · Toute la base**
*À l'écran : la vue complète, 105 fiches et leur bilan.*
> Sur toute la base : cent fiches sur cent exactes, sur deux versions différentes du logiciel, chacune prouvée par sa capture d'écran. Environ vingt secondes par fiche.

**Bloc 13 · 4:21 – 4:38 · Les chiffres et la fin**
*À l'écran : le carton des chiffres, puis le carton de fin.*
> Environ un centime par fiche : trois mille fiches pour vingt-cinq à quarante-cinq dollars, au lieu de cent heures. Thomas n'a rien recopié. Camille travaille déjà dans HubSpot. Merci !

---

**Repris du script d'Inès** : la présentation, le problème, les deux versions, les agents, la vérification, la preuve, HubSpot sans doublon, la réparation (2 IA, garde-fous, « personne n'a touché au code »), les chiffres.
**Ajouté pour coller à la vidéo** : Supabase (bloc 4), le bilan de la démo (bloc 7), la panne volontaire filmée en direct (bloc 10).
**Retiré, faute de temps à l'écran** : le schéma d'architecture, le chiffre de 44 %, la conclusion sur la suite (à garder pour le pitch).
