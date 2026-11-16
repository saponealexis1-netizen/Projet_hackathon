# Bascule — Parcours utilisateur

> **Version finale du 16/11/2026**, intégrée au livrable du checkpoint 2 ([`docs/checkpoint-2/`](../checkpoint-2/)). Elle applique les décisions D8 à D11 de [CADRAGE.md](../CADRAGE.md).
> Personas : voir [README](../../README.md#personas).

---

## 1. Les deux personnes du parcours

| | **Thomas** — celui qui lance la migration | **Camille** — celle dont les données migrent |
|---|---|---|
| Qui | Responsable onboarding chez un éditeur CRM ou une agence partenaire HubSpot | Gérante d'une petite agence, cliente de Thomas |
| Ce qu'il/elle fait dans Bascule | Lance, suit et valide la migration | Presque rien : elle donne l'adresse de son ancien logiciel et continue à travailler |
| Ce qu'il/elle veut | « La migration ne devrait pas bloquer une vente. » | « Je veux changer d'outil, pas tout recopier. » |
| Sa peur | Une migration longue qui retarde la signature | Perdre des données, ou qu'elles fuient |

## 2. Le parcours en un coup d'œil

```mermaid
flowchart LR
    A["1. Camille veut<br/>changer de CRM mais<br/>bloque sur la migration"] --> B["2. Thomas lance<br/>la migration<br/>dans Bascule"]
    B --> C["3. L'agent H lit<br/>chaque fiche<br/>de l'ancien CRM"]
    C --> D["4. La vérification<br/>classe chaque fiche<br/>ok · à vérifier · bloquée"]
    D --> E["5. Les fiches valides<br/>arrivent dans<br/>HubSpot"]
    D --> F["5 bis. Thomas corrige<br/>à la main les fiches<br/>bloquées"]
    F --> E
    E --> G["6. Bilan :<br/>Camille travaille<br/>dans HubSpot"]
```

## 3. Le parcours de Thomas, étape par étape

| # | Étape | Ce que Thomas fait | Ce que Bascule fait | Écran | Ce que ressent Thomas |
|---|---|---|---|---|---|
| 1 | **Le blocage** | Camille, qu'il démarche, est convaincue par HubSpot, mais son vieux logiciel n'a aucun export | — | — | 😟 La vente risque de tomber |
| 2 | **Préparer la migration** | Ouvre l'écran de suivi de Bascule : l'adresse de l'ancien CRM de Camille et la destination HubSpot sont déjà réglées | — | Écran de suivi (partie haute) | 🤔 « Est-ce que ça va marcher ? » |
| 3 | **Lancer** | Clique sur le bouton « Lancer la migration » | L'agent H ouvre la liste des contacts, puis chaque fiche, comme un humain | Écran de suivi | 😮 Il voit l'agent travailler en direct |
| 4 | **Suivre** | Regarde le tableau de bord | Affiche en direct : fiches lues, fiches par minute, % de champs corrects, coût, anomalies | Écran de suivi | 😌 Il n'a rien à faire |
| 5 | **Traiter les cas douteux** | Lit la raison de chaque fiche bloquée (ex. e-mail mal formé, doublon) et la corrige **à la main**, en dehors de Bascule | Envoie les fiches `ok` et `à vérifier` vers HubSpot ; affiche les fiches bloquées avec leur raison, sans les envoyer | Écran de suivi → liste des anomalies | 🙂 Il ne traite que quelques fiches au lieu de toutes |
| 6 | **Valider** | Ouvre HubSpot et vérifie quelques contacts | Affiche le bilan : fiches migrées, à vérifier, bloquées, durée, coût | Écran de suivi (encadré « Bilan ») + HubSpot | 🎉 La vente est signée, la cliente est opérationnelle |

## 4. Le parcours de Camille

| Moment | Ce que vit Camille | Ce que Bascule lui apporte |
|---|---|---|
| **Avant** | Elle veut passer sur HubSpot mais redoute de recopier ses contacts un par un | La migration est offerte par Thomas |
| **Pendant** | Elle donne l'adresse de son ancien logiciel et **continue à travailler** | L'agent ne fait que lire : aucune donnée n'est modifiée dans son ancien logiciel |
| **Après** | Elle retrouve ses contacts dans HubSpot, propres et dédoublonnés | Un bilan clair : ce qui a été migré, ce qui est à vérifier, ce qui a été bloqué |

## 5. Les écrans

| Écran | Rôle dans le parcours | Qui le construit |
|---|---|---|
| **Ancien CRM simulé** (« logiciel de 2010 ») | Ce que l'agent lit : liste paginée de contacts, une fiche par page, aucun export | Victoria (`apps/legacy-crm/`) |
| **Écran de suivi de migration** | En haut : bouton « Lancer la migration ». Au milieu : tableau de bord en direct et liste des anomalies. En bas : encadré « Bilan » | Inès (`apps/dashboard/`) |
| **HubSpot** | Le nouveau CRM où arrivent les contacts | Réel (compte gratuit, envoi par Alexis) |

### Ce qu'affiche l'écran de suivi

| Indicateur | Source |
|---|---|
| Fiches lues / total | `migration_log` (Supabase) |
| Statut de chaque fiche : ✅ `ok` · ⚠️ `warning` (à vérifier, envoyée dans HubSpot sans note) · ❌ `error` (bloquée, affichée avec sa raison, non envoyée) | Vérification (Inès) |
| Liste des anomalies (doublon, e-mail mal formé, champ vide…) | Vérification (Inès) |
| Temps par fiche et coût par fiche | `migration_log` (`duration_ms`, `credits_used`) |
| Lien vers chaque contact créé dans HubSpot | `migration_log` (`hubspot_id`) |

## 6. Ce que Thomas voit sur une fiche

Les 9 champs du contrat commun ([`shared/contact.schema.json`](../../shared/contact.schema.json)) :

| Champ | Exemple | Obligatoire |
|---|---|---|
| Identifiant ancien CRM | C-0042 | ✅ |
| Prénom | Camille | ✅ |
| Nom | Martin | ✅ |
| E-mail | camille.martin@exemple.fr | |
| Téléphone | +33 6 12 34 56 78 | |
| Entreprise | Agence Lumière | |
| Poste | Gérante | |
| Ville | Lyon | |
| Notes | Client depuis 2019 | |

## 7. Le scénario de la démo (vendredi, ~3 min)

| Temps | Ce qu'on montre | Ce qu'on dit |
|---|---|---|
| 0:00 | L'ancien CRM « 2010 » : on cherche le bouton d'export… il n'y en a pas | « Voilà le logiciel de Camille. Aucun export. Imaginez 3 000 contacts. » |
| 0:30 | Thomas lance la migration dans Bascule | « Thomas n'a qu'à cliquer. » |
| 0:45 | 3 agents H ouvrent des fiches en parallèle, en direct | « L'agent lit l'écran comme un humain. » |
| 1:30 | Le tableau de bord se remplit : fiches, %, coût, anomalies | « Il vérifie chaque fiche et signale les problèmes. » |
| 2:15 | Une fiche bloquée (doublon ou e-mail mal formé) s'affiche avec sa raison | « Thomas ne corrige à la main que les cas douteux. » |
| 2:40 | Les contacts apparaissent dans HubSpot | « Camille travaille déjà dans HubSpot. » |

**Timing réaliste** : on a mesuré **~48 s par fiche** et l'offre gratuite H Company permet **3 agents en parallèle par personne**. En 2 minutes de démo, on migre donc **~5 à 6 fiches en direct**. Les 20 fiches de la démo sont lancées **juste avant le pitch** : on montre le lancement en direct, puis le tableau de bord et HubSpot déjà remplis.

**Plan B** : vidéo enregistrée de la même démo si le réseau ou l'agent lâche (tâche de Victoria, jeudi).

## 8. Décisions prises (CADRAGE.md, D8 à D11)

| # | Décision | Effet sur le parcours |
|---|---|---|
| D8 | Le lancement et le bilan sont deux parties de l'écran de suivi | Un seul écran Bascule pour Thomas : lancer, suivre, voir le bilan |
| D9 | Une fiche bloquée est affichée avec sa raison, sans correction dans l'outil | Thomas corrige à la main, en dehors de Bascule |
| D10 | Les fiches « à vérifier » partent dans HubSpot, sans note | L'anomalie reste visible sur l'écran de suivi et dans `migration_log` |
| D11 | L'ancien CRM n'a pas de mot de passe pour le MVP | Camille donne seulement l'adresse de son ancien logiciel |
