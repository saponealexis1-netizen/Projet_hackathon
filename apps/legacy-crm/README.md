# Ancien CRM simulé (`apps/legacy-crm`)

Application Next.js qui joue le rôle du **vieux CRM sans export ni API** que l'agent H Company doit lire à l'écran.
Propriétaire : Victoria (voir [docs/ORGANISATION.md](../../docs/ORGANISATION.md)). Liste, fiches, menus et version 2 réalisés par Maxime en remplacement le 17/11.

En ligne : https://projet-hackathon-uffi.vercel.app

## Ce que contient l'application

Deux versions du même ancien CRM, sur **la même base de 100 contacts** (décision D12 de [CADRAGE.md](../../docs/CADRAGE.md)) : l'agent doit savoir lire les deux sans changer son code.

### Version 1 — « CRM Agence 2010 » (adresse `/`)

| Page | Adresse | Contenu |
|---|---|---|
| Liste des contacts | `/` (puis `/?page=2` … `/?page=10`) | **10 contacts par page** : N° client, Nom, Prénom, Société, Ville, lien « Voir la fiche » ; boutons « Page précédente » / « Page suivante » |
| Fiche contact | `/contacts/C-0001` | **2 onglets** : « Identité » (N° client, Prénom, Nom, Société, Fonction, Commentaires) et « Coordonnées » (E-mail, Téléphone, Ville). Le **téléphone est caché** derrière « Afficher le numéro ». Boutons « Retour à la liste », « Fiche précédente », « Fiche suivante » |
| Nouveau contact / Modifier | `/contacts/nouveau`, `/contacts/C-0001/modifier` | Formulaire ; « Enregistrer » affiche l'erreur « base en lecture seule » (rien n'est modifié) |
| Agenda | `/agenda` (et `/agenda?mois=2026-12`) | Vue du mois, faux rendez-vous reliés aux contacts ; un clic ouvre la fiche |
| Outils | `/outils` | Options (non enregistrables), vérification des mises à jour, informations sur la base |
| Aide | `/aide` | Sommaire, questions fréquentes (dont « Comment exporter ? » → non disponible), à propos |
| Fermeture | `/au-revoir` | Après Fichier › Quitter ou le bouton × |

À l'arrivée sur le site, une fenêtre **« Message du jour »** s'ouvre et doit être fermée (une fois par session du navigateur).

Libellés = ceux des instructions de l'agent d'Inès (`agent/prompts/`) : « N° client », « Prénom », « Nom », « E-mail », « Téléphone », « Société », « Fonction », « Ville », « Commentaires », « Page suivante », « Retour à la liste ».

### Version 2 — « GestiContacts 2.4 » (adresse `/v2`)

Même style « logiciel à l'ancienne » que la v1, mais une autre disposition (colonnes dans un autre ordre, pages numérotées, fiche en 2 encadrés « Société » / « Joindre le client » sans onglets), d'autres menus (Fichier, Répertoire, ?), d'autres adresses et **d'autres libellés** :

| v1 | v2 |
|---|---|
| N° client | Réf. |
| Nom | Nom de famille |
| Société | Raison sociale |
| Fonction | Poste occupé |
| E-mail | Courriel |
| Téléphone (« Afficher le numéro ») | Tél. (« Voir le tél. ») |
| Ville | Localité |
| Commentaires | Observations |
| Voir la fiche | Détail › |
| Page suivante | Suiv. » (pages numérotées) |
| Retour à la liste | ‹ Revenir au répertoire |

Adresses : liste `/v2` (puis `/v2?p=2`…), fiche `/v2/fiche/C-0001`, à propos `/v2/a-propos`.

### Obstacles volontaires pour l'agent (CADRAGE.md)

| Obstacle | v1 | v2 |
|---|---|---|
| Pagination | « Page suivante » | Pages numérotées « Suiv. » |
| Infos réparties | 2 onglets à ouvrir | 2 encadrés côte à côte |
| Téléphone caché | « Afficher le numéro » | « Voir le tél. » |
| Fenêtre à fermer | « Message du jour » | — |

### Choix volontaires pour la démo

- **Aucun bouton d'export**, aucune API publique (c'est tout l'enjeu de Bascule).
- **Pas de mot de passe** (décision D11).
- **Base en lecture seule** : on peut tout ouvrir et cliquer, mais rien ne se modifie.
- Une valeur vide reste vide à l'écran : l'agent ne doit rien inventer.

## D'où viennent les données

| Situation | Source |
|---|---|
| `SUPABASE_URL` et `SUPABASE_SERVICE_ROLE_KEY` définies | Table `legacy_contacts` de Supabase, lue **côté serveur** (l'agent n'y a pas accès) |
| Variables absentes | `lib/contacts.fallback.json`, copie de [`data/contacts.legacy.json`](../../data/contacts.legacy.json) : les mêmes 100 contacts (plan B, décision D5) |
| Supabase configuré mais injoignable (adresse ou clé fausse, réseau) | Bascule automatiquement sur le fichier de secours, avec un message dans les journaux du serveur : la démo ne casse pas |

Les pages sont toujours générées à la demande : une modification dans Supabase apparaît au rechargement.

## Lancer en local

```bash
cd apps/legacy-crm
npm install
cp .env.example .env.local   # facultatif : sans valeurs, les contacts de secours s'affichent
npm run dev                  # http://localhost:3000
```

Avant tout commit, vérifier que les clés sont bien ignorées :

```bash
git check-ignore -v apps/legacy-crm/.env.local
```

## Déployer sur Vercel

- **Root Directory : `apps/legacy-crm`** (déjà configuré).
- Variables d'environnement : `SUPABASE_URL` et `SUPABASE_SERVICE_ROLE_KEY` (sinon, les contacts de secours s'affichent), et `H_COMPANY_API_KEY` = la clé de Victoria (voir section 8 de `docs/ORGANISATION.md`).
