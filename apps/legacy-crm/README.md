# Ancien CRM simulé (`apps/legacy-crm`)

Application Next.js qui joue le rôle du **vieux CRM sans export ni API** que l'agent H Company doit lire à l'écran.
Propriétaire : Victoria (voir [docs/ORGANISATION.md](../../docs/ORGANISATION.md)). Liste et fiches réalisées par Maxime en remplacement le 17/11.

En ligne : https://projet-hackathon-uffi.vercel.app

## Ce que contient l'application

| Page | Adresse | Contenu |
|---|---|---|
| Liste des contacts | `/` (et `/?page=2`, `/?page=3`) | 8 contacts par page : n° de fiche, nom, prénom, société, ville, lien « Ouvrir la fiche » |
| Fiche contact | `/contacts/C-0001` | Les 9 champs du contrat [`shared/contact.schema.json`](../../shared/contact.schema.json), chacun avec un libellé visible ; boutons « Retour à la liste », « Fiche précédente », « Fiche suivante » |
| Fiche inconnue | `/contacts/C-9999` | Page « Fiche introuvable » (code 404) |
| Nouveau contact / Modifier | `/contacts/nouveau`, `/contacts/C-0001/modifier` | Formulaire de saisie ; « Enregistrer » affiche l'erreur « base en lecture seule » (rien n'est modifié) |
| Agenda | `/agenda` (et `/agenda?mois=2026-12`) | Vue du mois avec de faux rendez-vous reliés aux contacts de la base ; un clic ouvre la fiche |
| Outils | `/outils` | Options d'affichage (non enregistrables), vérification des mises à jour, informations sur la base |
| Aide | `/aide` | Sommaire, questions fréquentes (dont « Comment exporter ? » → non disponible), à propos |
| Fermeture | `/au-revoir` | Écran « Session terminée » après Fichier › Quitter ou le bouton × |

Choix volontaires pour la démo :

- **Aucun bouton d'export**, aucune API publique (c'est tout l'enjeu de Bascule).
- **Pas de mot de passe** (décision D11 de [CADRAGE.md](../../docs/CADRAGE.md)).
- Look « logiciel de 2010 » : fenêtre grise, menus déroulants d'époque (Fichier, Contacts, Agenda, Outils, Aide), boutons de fenêtre réduire / agrandir / fermer, boîtes de dialogue.
- **Base en lecture seule** : on peut tout ouvrir et cliquer, mais rien ne se modifie (aucun risque de casser les données de la démo).
- Fonctionne avec n'importe quel nombre de contacts : la pagination, la navigation entre fiches et l'agenda s'adaptent (testé avec 100).
- Une valeur vide reste vide à l'écran : l'agent ne doit rien inventer.

## D'où viennent les données

| Situation | Source |
|---|---|
| `SUPABASE_URL` et `SUPABASE_SERVICE_ROLE_KEY` définies | Table `legacy_contacts` de Supabase, lue **côté serveur** (l'agent n'y a pas accès) |
| Variables absentes | `lib/contacts.fallback.json`, copie de [`data/contacts.sample.json`](../../data/contacts.sample.json) (plan B, décision D5) |

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
