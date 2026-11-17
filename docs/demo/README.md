# Démo live de vendredi 20/11 — mode d'emploi

> **Mehdi au clavier** (il remplace Alexis, absent vendredi) · **Maxime à la parole**.
> Slide 4 du pitch : **2 minutes**. Principe : on lance **le vrai agent H Company** sur 6 fiches, dont les 5 pièges, et on montre le résultat déjà obtenu sur toute la base.
> **Rien à installer** : tout se fait depuis un navigateur.

---

## 1. Les liens (onglets à ouvrir dans cet ordre)

| # | Onglet | Adresse |
|---|---|---|
| 1 | **Écran de suivi** (le bouton est ici) | https://projet-hackathon-jow2.vercel.app/?run=tout |
| 2 | **Ancien CRM** v1 | https://projet-hackathon-uffi.vercel.app |
| 3 | **HubSpot**, vue « Bascule » | (compte HubSpot de l'équipe) |
| 4 | Plan B : l'action GitHub | GitHub › onglet **Actions** › « Lancer la migration » |

## 2. Le déroulé, seconde par seconde

> Le vrai agent met **~30 s à démarrer**, puis **~100 s** pour les 6 fiches. On clique donc **dès le début**, et on parle de l'ancien CRM pendant qu'il démarre.

| Temps | À l'écran | Ce que dit Maxime | Ce que fait Mehdi |
|---|---|---|---|
| **0:00** | Écran de suivi | « On lance Bascule sur 6 fiches. L'agent ne connaît rien de ce logiciel : on lui donne seulement l'adresse. » | Clique sur **« Lancer la migration (agent réel) »** |
| **0:05** | **Ancien CRM** v1, fenêtre « Message du jour » | « Voici le logiciel de Camille, installé en 2010. Aucun export, aucune API. Le numéro est même caché derrière un bouton. » | Ferme la fenêtre, ouvre **Fichier** (aucun export), ouvre une fiche, onglet **Coordonnées**, clique sur **Afficher le numéro** |
| **0:35** | Écran de suivi, panneau **« Agents en direct »** | « Voilà les agents H Company : chacun voit l'écran, ferme la fenêtre, passe les pages, clique sur Afficher… comme un humain. » | Revient sur l'onglet 1 : 3 agents travaillent, leur écran se rafraîchit toutes les 3 s |
| **1:00** | Écran de suivi, les fiches arrivent une par une | « Chaque fiche est vérifiée avant HubSpot. Le doublon est bloqué, l'e-mail invalide est relu puis bloqué, le nom en majuscules est corrigé. » | Clique sur **📷 Voir** d'une fiche : capture + champs lus côte à côte |
| **1:30** | **HubSpot**, vue « Bascule » | « Les contacts sont dans HubSpot, chacun relié à sa fiche d'origine. Rien de faux n'y est arrivé. » | Ouvre la vue, montre la colonne « Bascule - ID ancien CRM » |
| **1:45** | Écran de suivi `?run=tout` | « Et sur toute la base : 100 fiches sur 100 exactes, chacune prouvée par sa capture d'écran. » | Ouvre l'adresse `?run=tout` (bilan complet) |
| **2:00** | — | « Thomas n'a rien recopié. Camille travaille déjà dans HubSpot. » | — |

**Ce qu'on doit voir pour les 6 fiches**

| Fiche | Piège | Résultat attendu |
|---|---|---|
| C-0004 | Fiche normale (Élodie Garnier) | ✅ Migrée |
| C-0101 | Doublon d'Élodie Garnier | ⛔ Bloquée (doublon) |
| C-0102 | E-mail sans domaine complet | ⛔ Bloquée, après relecture par l'agent |
| C-0103 | Prénom vide | ⛔ Bloquée (champ obligatoire) |
| C-0104 | Téléphone incomplet | ⚠️ Envoyée « à vérifier » |
| C-0105 | MARCHETTI / toulouse | ⚠️ Envoyée, majuscules corrigées |

> L'ordre d'arrivée peut changer : si C-0101 arrive **avant** C-0004, le doublon est détecté sur C-0004 à la place. C'est normal, et ça se dit : « la première arrivée passe, la seconde est bloquée ».

## 3. Préparation

### Jeudi (répétition de 18h)
- [ ] Mehdi fait la démo **en entier** une fois, avec le bouton.
- [ ] Mehdi se connecte à **GitHub** (accès au dépôt) et à **HubSpot** sur l'ordinateur de la démo.
- [ ] Enregistrer la **vidéo de secours** de la démo (Inès).

### Vendredi, 15 minutes avant le pitch
- [ ] Ouvrir les 4 onglets du tableau 1. Zoom du navigateur à **125 %**.
- [ ] Ancien CRM : recharger la page pour que la fenêtre « Message du jour » soit visible.
- [ ] Vérifier sur l'écran de suivi que le bouton dit **« Lancer la migration (agent réel) »**. S'il dit seulement « Lancer la migration », la configuration manque : voir section 6 (sinon, plan B).
- [ ] **Ne pas cliquer** avant le début de la démo : le bouton remet lui-même les 6 fiches à zéro dans HubSpot.

## 4. Plans B

| Problème | Ce qu'on fait |
|---|---|
| Le bouton affiche une erreur | GitHub › **Actions** › « Lancer la migration » › **Run workflow** (les valeurs par défaut sont les bonnes), puis ouvrir le lien « Suivi en direct » affiché dans le résumé de l'action, ou `?run=dernier` |
| « Des agents travaillent déjà » | Une migration tourne encore : attendre 1 à 2 min, ou montrer `?run=dernier` |
| L'agent est lent / le réseau lâche | Rester sur `?run=tout` (100 fiches déjà migrées, preuves, bilan) et HubSpot : **tout est déjà réel** |
| Une fiche échoue en direct | C'est un argument : « elle est bloquée avec sa raison, rien de faux n'arrive dans HubSpot » |
| Plus de crédits H Company | Remplacer le secret `HAI_API_KEY` par la clé d'Inès (section 6) |
| Plus aucun réseau | Vidéo de secours |

## 5. Les chiffres à dire (réels, mesurés)

| Ce qu'on dit | Source |
|---|---|
| **100 / 100** fiches exactes, **5 / 5** pièges traités comme prévu | Migration de l'ancien CRM v2, 105 fiches |
| **~21 s** par fiche (médiane), 3 agents en parallèle | idem |
| **~0,008 $** par fiche, **0,87 $** pour 105 fiches | Coût mesuré par l'Agent API |
| **3 000 fiches ≈ 25 $** | Extrapolation |
| Fonctionne sur **deux logiciels différents** (v1 et v2) **sans rien reconfigurer** | v1 : 100/100 · v2 : 100/100 |

## 6. Configuration (Alexis, avant jeudi soir)

**a) Secrets de l'action GitHub** — dépôt › Settings › Secrets and variables › **Actions** › New repository secret :

| Nom | Valeur |
|---|---|
| `HAI_API_KEY` | Clé Agent API H Company |
| `HUBSPOT_TOKEN` | Jeton de l'application privée HubSpot |
| `SUPABASE_URL` | Adresse du projet Supabase |
| `SUPABASE_SERVICE_ROLE_KEY` | Clé secrète Supabase (`sb_secret_…`) |

**b) Jeton pour le bouton** — github.com › Settings › Developer settings › **Fine-grained tokens** › Generate new token :
- Expiration : **7 jours** ; Repository access : **Only select repositories** › `Projet_hackathon` ;
- Permissions › Repository › **Actions : Read and write** (rien d'autre).

**c) Vercel, projet de l'écran de suivi (jow2)** › Settings › Environment Variables :
- `GITHUB_DISPATCH_TOKEN` = le jeton du b) ;
- `HAI_API_KEY` = la clé H Company (captures et agents en direct) ;
- puis **Deployments › Redeploy**.

**d) Accès de Mehdi** : collaborateur du dépôt GitHub (droit d'écriture, pour lancer l'action et fusionner) et utilisateur HubSpot.

**Test** : cliquer une fois sur le bouton jeudi. Coût : ~0,05 $.

## 7. Vendredi, les dépôts (Mehdi)

| Heure | Dépôt | Contenu |
|---|---|---|
| **11h** | Prototype + dépôt GitHub + vidéo de 5 min | Lien du dépôt (branche `main`), liens de l'écran de suivi et de l'ancien CRM, vidéo |
| **15h** | Pitch deck | PDF de Maxime, relu |

Avant 11h : vérifier qu'aucune PR utile n'est restée ouverte, fusionner celles marquées **« PRÊT POUR MERGE »**, puis vérifier que les 3 liens s'ouvrent.

## 8. Après le hackathon

Régénérer les clés HubSpot et Supabase, et supprimer le jeton GitHub du b).
