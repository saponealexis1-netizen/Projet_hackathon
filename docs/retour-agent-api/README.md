# Retour d'expérience — Agent API H Company

Propriétaire : **Inès (CAIO)** · **Brouillon du mardi 17/11**, à compléter jeudi (tests sur les pièges et la 2e version du CRM) et à finaliser vendredi avant 11h.

> Sources : tests d'Alexis dans [`agent/runner/README.md`](../../agent/runner/README.md), mesures de Maxime dans [`docs/pitch/business-model.md`](../pitch/business-model.md), journal `migration_log` (Supabase).

---

## 1. En une phrase

**L'agent H Company sait lire un logiciel qu'il n'a jamais vu, sans configuration, mais il ne faut jamais le croire sur parole : ce sont les garde-fous autour de lui (format imposé, contrôle d'identité, vérification, relecture, capture d'écran) qui ont transformé 1 fiche exacte sur 5 en 100 sur 100.**

## 2. Les chiffres clés

| Mesure | Valeur | Source |
|---|---|---|
| Fiches migrées de l'ancien CRM vers HubSpot | **100 / 100** | Migration complète du 17/11 |
| Fiches 100 % exactes (9 champs sur 9) | **100 / 100** | idem |
| Temps moyen de lecture d'une fiche | **31 s** (médiane 29 s) | idem |
| Coût moyen par fiche | **~0,015 $** (1,53 $ pour 100 fiches) | Métriques renvoyées par l'API |
| Agents en parallèle | 3 (limite de l'offre gratuite) | Documentation H Company |
| Durée réelle pour 100 fiches | 33 min mesurées, ~17 min après correction de notre code | `agent/runner` |
| Premier essai sur 5 fiches, avant les garde-fous | **1 / 5** seulement | 17/11 |

## 3. Ce qui a marché

| Constat | Ce que ça nous apporte |
|---|---|
| **Zéro configuration (D12)** : l'agent ne reçoit que l'adresse et l'identifiant de la fiche. Il trouve seul la liste, la pagination, les onglets, ferme la fenêtre « Message du jour » et clique sur « Afficher le numéro ». | C'est l'argument face à un script ou un robot RPA : un autre logiciel ne demande aucun code. |
| **Le même agent lit les deux versions de l'ancien CRM** (mise en page et libellés différents : « Société » / « Entreprise »…). | Preuve que l'agent comprend le sens des libellés, pas leur position. |
| **Format de réponse imposé** (`answer_format` : un objet JSON avec nos 9 champs + « error »). | La réponse arrive directement au format du contrat commun. |
| **Mode visuel + texte de la page** (`markdown: true`). | L'agent navigue en regardant l'écran, mais recopie les caractères exacts : plus d'erreurs de lecture de chiffres. |
| **Coût et durée renvoyés par l'API** pour chaque session. | Mesures de coût par fiche sans calcul de notre côté. |
| **Captures d'écran de chaque étape.** | Preuve pour l'utilisateur (D14) et outil de débogage : c'est grâce à elles qu'on a compris les erreurs. |
| **Plusieurs agents en parallèle.** | 3 fiches lues en même temps ; 10 avec l'offre Builder (20 $/mois). |

## 4. Ce qui a cassé, et comment on l'a réparé

| # | Problème observé | Pourquoi | Ce qu'on a changé | Résultat |
|---|---|---|---|---|
| 1 | **Téléphone inventé** : le numéro était caché derrière un bouton « Afficher », l'agent a renvoyé un numéro plausible sans cliquer. | L'agent préfère compléter plutôt que laisser vide. Le format était correct : notre vérification ne pouvait pas le voir. | Consigne : « une valeur n'est valable que si tu la vois écrite à l'écran ; si un champ affiche un bouton, clique dessus ». | 9/9 sur la même fiche |
| 2 | **Chiffre mal lu** : « 39 » lu « 99 » sur la 2e version du CRM. | Lecture de l'image seule. | Texte de la page transmis en plus de la capture (`markdown: true`). | 9/9 sur les deux versions |
| 3 | **Mauvaise fiche ouverte** : C-0007 au lieu de C-0070 (3 fiches sur 100). | Identifiants qui se ressemblent. | Consigne « l'identifiant doit être exactement {legacy_id}, caractère par caractère » + contrôle de l'identifiant renvoyé + **une relance automatique**. | Aucune mauvaise fiche envoyée dans HubSpot ; 3/3 exactes après relance |
| 4 | **Réponse mal rangée** : toute la fiche en JSON dans le champ « notes », le mot « None » écrit comme erreur. | Format « texte ou null » trop compliqué pour l'agent. | Champs en texte uniquement (chaîne vide si absent) ; nettoyage de la réponse côté code. | Passage de 1/5 à 5/5 |
| 5 | **Relecture sur une fiche vide** → l'agent a produit « User User ». | Relecture lancée alors que la première lecture avait échoué. | Pas de relecture si la fiche est vide. | — |
| 6 | **~20 s perdues par fiche** après la réponse de l'agent. | Notre code attendait encore une confirmation de l'API (attente longue) après la fin de la session. | Arrêt dès que la session est terminée et la réponse reçue. | 100 fiches : ~33 min → ~17 min (projection) |

## 5. Ce qui nous a surpris

- **L'agent « veut » répondre** : face à une information cachée, il invente une valeur crédible plutôt que de dire qu'il ne la voit pas. Il faut lui dire explicitement que le vide vaut mieux qu'une invention.
- **Une erreur « parfaite » ne se voit pas** : un faux numéro bien formaté passe toutes les règles de vérification. Seule la **capture d'écran** a permis de comprendre ce qui s'était passé.
- **Les consignes en français simple suffisent** : pas besoin de décrire le logiciel, seulement le but et les règles.
- **La moitié du travail est autour de l'agent**, pas dans l'agent : format imposé, contrôles, relances, mesures.

## 6. Les garde-fous qu'on a mis autour de l'agent

| Garde-fou | Où | Il protège contre… |
|---|---|---|
| Format de réponse imposé (9 champs + « error ») | `agent/runner/prompts.py` | Les réponses mal rangées |
| Règles strictes : ne rien inventer, lecture seule, ne rien corriger | `agent/runner/prompts.py` | Les valeurs inventées, les modifications dans l'ancien CRM |
| Contrôle d'identité + une relance | `agent/runner/run.py` | La mauvaise fiche ouverte |
| Vérification (ok / à vérifier / bloquée) | `pipeline/verification/` | E-mails invalides, champs obligatoires vides, doublons |
| Relecture ciblée d'un champ suspect (D13) | `agent/runner/run.py` | Les erreurs de lecture d'un champ précis |
| Capture d'écran gardée pour chaque fiche (D14) | `migration_log` + écran de suivi | Les erreurs invisibles : on peut toujours vérifier |
| Upsert sur `bascule_legacy_id` | `pipeline/hubspot/` | Les doublons dans HubSpot en cas de relance |

## 7. Nos conseils à une équipe qui démarre avec l'Agent API

1. **Imposer un format de réponse simple** (texte uniquement, chaîne vide si absent) dès le premier test.
2. **Activer le texte de la page** (`markdown: true`) dès qu'il faut recopier des chiffres ou des identifiants.
3. **Écrire noir sur blanc « ne devine jamais »** et dire quoi faire quand une information est cachée.
4. **Garder les captures d'écran** : c'est le meilleur outil pour comprendre une erreur.
5. **Ne jamais faire confiance à la réponse** : vérifier l'identifiant, le format, et relire en cas de doute.
6. **Une session par fiche** plutôt qu'une longue session : plus facile à relancer, à mesurer et à paralléliser.
7. **Arrêter d'attendre dès que la réponse est là** : sinon on perd du temps à chaque fiche.

## 8. À compléter jeudi et vendredi

- [ ] Migration complète sur la **2e version** de l'ancien CRM (zéro configuration à grande échelle).
- [ ] Résultat sur les **fiches pièges** (doublons, champs vides, e-mails invalides) : bloquées par la vérification ?
- [ ] Part des anomalies **corrigées par la relecture** (D13), lue sur l'écran de suivi.
- [ ] Durée réelle des 100 fiches **après correction** (mesurée, pas projetée).
- [ ] Ce qui s'est passé pendant la **démo live** de vendredi.
