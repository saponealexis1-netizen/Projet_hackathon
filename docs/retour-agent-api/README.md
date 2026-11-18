# Retour d'expérience — Agent API H Company

Propriétaire : **Inès (CAIO)** · **Version 6 du mercredi 18/11**. Reste à ajouter ce qui se passe pendant la démo live (section 14), puis à finaliser vendredi avant 11h.

> Sources : tests d'Alexis dans [`agent/runner/README.md`](../../agent/runner/README.md), mesures de Maxime dans [`docs/pitch/business-model.md`](../pitch/business-model.md), journal `migration_log` (Supabase).

---

## 1. En une phrase

**L'agent H Company sait lire un logiciel qu'il n'a jamais vu, sans configuration, mais il ne faut jamais le croire sur parole : ce sont les garde-fous autour de lui (format imposé, contrôle d'identité, vérification, relecture, capture d'écran) qui ont transformé 1 fiche exacte sur 5 en 100 sur 100.**

## 2. Les chiffres clés

Deux migrations complètes, **sur deux versions différentes de l'ancien CRM** (mise en page et libellés différents), avec **le même agent et les mêmes consignes**.

| Mesure | Ancien CRM **v1** | Ancien CRM **v2** |
|---|---|---|
| Fiches lues par l'agent | 100 / 100 | **105 / 105** (100 + 5 pièges) |
| Fiches 100 % exactes (9 champs sur 9) | **100 / 100** | **100 / 100** |
| Fiches pièges traitées comme prévu | — | **5 / 5** |
| Mauvaise fiche ouverte, rattrapée par le contrôle d'identité | 3 (relancées → exactes) | 1 : C-0009 au lieu de C-0090 (relancée automatiquement) |
| Mauvaise fiche envoyée dans HubSpot | **0** | **0** |
| Temps par fiche | 31 s (médiane 29 s) | **médiane 21 s** |
| Durée réelle, 3 agents en parallèle | 33 min (avant correction de notre code) | **16,9 min mesurées** (après correction) |
| Coût total de l'agent H | 1,53 $ (~0,015 $ par fiche) | **0,87 $** (~0,008 $ par fiche) |

Avant les garde-fous, le premier essai sur 5 fiches donnait **1 fiche exacte sur 5**.

## 3. La progression, test après test

| Étape (17/11) | Fiches exactes | Ce qui a fait la différence |
|---|---|---|
| 1re lecture d'une fiche (page GitHub, avant l'ancien CRM) | 1 / 1 (12 s, 0,004 $) | Format de réponse imposé dès le départ |
| Ancien CRM v1, fiche avec numéro caché, consignes v1 | 8 / 9 champs | — (téléphone inventé) |
| Même fiche, consignes « ne devine jamais, clique sur Afficher » | 9 / 9 | Consignes anti-invention |
| Ancien CRM v2, image seule | 8 / 9 champs | — (« 39 » lu « 99 ») |
| v1 et v2 avec le texte de la page | 9 / 9 et 9 / 9 | `markdown: true` |
| 1er parcours complet, 5 fiches, 3 agents | **1 / 5** | — (réponses mal rangées) |
| Même parcours, format texte simple + nettoyage | **5 / 5** | Format simplifié |
| Migration des 100 fiches | 97 / 100, **0 erreur envoyée dans HubSpot** | Le contrôle d'identité a bloqué les 3 mauvaises fiches |
| Relance automatique des 3 fiches | **100 / 100** | Relance une fois si la fiche n'est pas la bonne |
| 5 fiches pièges + 1 fiche normale | **5 / 5 pièges traités comme prévu** | Vérification + relecture ciblée (D13) |
| **Migration complète de la v2** (105 fiches, autre mise en page, autres libellés) | **100 / 100 exactes, 5 / 5 pièges, en 16,9 min** | Aucun réglage : mêmes consignes, même agent |

## 4. Ce qui a marché

| Constat | Ce que ça nous apporte |
|---|---|
| **Zéro configuration (D12)** : l'agent ne reçoit que l'adresse et l'identifiant de la fiche. Il trouve seul la liste, la pagination, les onglets, ferme la fenêtre « Message du jour » et clique sur « Afficher le numéro ». | C'est l'argument face à un script ou un robot RPA : un autre logiciel ne demande aucun code. |
| **Le même agent, sans aucun réglage, a migré les deux versions de l'ancien CRM** : 100/100 exactes sur la v1, puis 100/100 exactes (et 5/5 pièges) sur la v2, qui a une autre mise en page et d'autres libellés (« Société » / « Entreprise »…). | L'agent comprend le sens des libellés, pas leur position : un autre logiciel ne demande aucun code. |
| **Format de réponse imposé** (`answer_format` : un objet JSON avec nos 9 champs + « error »). | La réponse arrive directement au format du contrat commun. |
| **Mode visuel + texte de la page** (`markdown: true`). | L'agent navigue en regardant l'écran, mais recopie les caractères exacts : plus d'erreurs de lecture de chiffres. |
| **Coût et durée renvoyés par l'API** pour chaque session. | Mesures de coût par fiche sans calcul de notre côté. |
| **Captures d'écran de chaque étape.** | Preuve pour l'utilisateur (D14) et outil de débogage : c'est grâce à elles qu'on a compris les erreurs. |
| **Plusieurs agents en parallèle.** | 3 fiches lues en même temps ; 10 avec l'offre Builder (20 $/mois). |

## 5. Ce qui a cassé, et comment on l'a réparé

| # | Problème observé | Pourquoi | Ce qu'on a changé | Résultat |
|---|---|---|---|---|
| 1 | **Téléphone inventé** : le numéro était caché derrière un bouton « Afficher », l'agent a renvoyé un numéro plausible sans cliquer. | L'agent préfère compléter plutôt que laisser vide. Le format était correct : notre vérification ne pouvait pas le voir. | Consigne : « une valeur n'est valable que si tu la vois écrite à l'écran ; si un champ affiche un bouton, clique dessus ». | 9/9 sur la même fiche |
| 2 | **Chiffre mal lu** : « 39 » lu « 99 » sur la 2e version du CRM. | Lecture de l'image seule. | Texte de la page transmis en plus de la capture (`markdown: true`). | 9/9 sur une fiche de chaque version |
| 3 | **Mauvaise fiche ouverte** : C-0007 au lieu de C-0070 (3 fiches sur 100). | Identifiants qui se ressemblent. | Consigne « l'identifiant doit être exactement {legacy_id}, caractère par caractère » + contrôle de l'identifiant renvoyé + **une relance automatique**. | Aucune mauvaise fiche envoyée dans HubSpot ; 3/3 exactes après relance |
| 4 | **Réponse mal rangée** : toute la fiche en JSON dans le champ « notes », le mot « None » écrit comme erreur. | Format « texte ou null » trop compliqué pour l'agent. | Champs en texte uniquement (chaîne vide si absent) ; nettoyage de la réponse côté code. | Passage de 1/5 à 5/5 |
| 5 | **Relecture sur une fiche vide** → l'agent a produit « User User ». | Relecture lancée alors que la première lecture avait échoué. | Pas de relecture si la fiche est vide. | — |
| 6 | **~20 s perdues par fiche** après la réponse de l'agent. | Notre code attendait encore une confirmation de l'API (attente longue) après la fin de la session. | Arrêt dès que la session est terminée et la réponse reçue. | 33 min mesurées avant → **16,9 min mesurées après** (migration de la v2, 105 fiches) |
| 7 | **Relecture qui efface la fiche** : la relecture de l'e-mail n'a renvoyé que l'e-mail, et le code a remplacé toute la fiche (prénom et nom perdus). | Notre code reprenait toute la réponse de la relecture. | Une relecture ne remplace plus que le champ relu (2 tests ajoutés). | Fiches pièges : prénom et nom conservés |

## 6. Les fiches pièges : l'agent face à des données fausses

5 fiches piégées ont été ajoutées à l'ancien CRM (C-0101 à C-0105) et migrées avec C-0004, dont l'une est le doublon (6 fiches en 102 s).

| Fiche | Piège | Ce qu'a fait Bascule |
|---|---|---|
| C-0101 | Doublon de C-0004 (même e-mail) | ❌ **Bloquée** : « doublon possible de C-0004 » |
| C-0102 | E-mail invalide | 🔁 Relue par l'agent, valeur **confirmée**, puis ❌ **bloquée** : « e-mail invalide » |
| C-0103 | Prénom « - » | 🔁 Relue, puis ❌ **bloquée** : « champ obligatoire vide » |
| C-0104 | Téléphone incomplet | 🔁 Relue, valeur **confirmée**, puis ⚠️ **à vérifier**, envoyée dans HubSpot |
| C-0105 | `MARCHETTI`, `toulouse` | ⚠️ Corrigée (Marchetti, Toulouse), envoyée dans HubSpot |

**Ce qu'on en retient**
- **La vérification fait son travail** : les 3 fiches qui ne doivent pas partir (doublon, e-mail invalide, prénom vide) restent hors de HubSpot, avec leur raison affichée.
- **La relecture (D13) sait dire « c'est bien écrit comme ça »** : quand la donnée est fausse dans l'ancien CRM, l'agent la confirme au lieu d'inventer une correction. C'est le comportement voulu : Bascule recopie, il ne corrige pas les données du client.
- **Les tests de pièges ont trouvé un bug de notre code** (n° 7 ci-dessus), corrigé avant la démo.

## 7. Bascule se répare tout seul quand HubSpot change (fallback)

Principe expliqué par notre professeur : quand une action échoue, le système revient en arrière, se met à jour et réessaie, et on le voit dans les journaux. Côté ancien CRM, l'agent H s'adapte déjà seul (deux versions migrées sans réglage). Côté HubSpot, ce que Bascule sait (où ranger chaque champ, ce qui est refusé) est rangé dans un **skill** que **deux IA Hugging Face** tiennent à jour ([`pipeline/hubspot_skill/`](../../pipeline/hubspot_skill/README.md)).

**Le cycle** : ❌ HubSpot refuse une fiche → 🧠 IA n°1 (Qwen3) lit l'erreur et propose une correction du skill → 🛡️ garde-fous du code → 🔍 IA n°2 valide → 🔁 la fiche repart une fois → ✅ résultat visible sur l'écran de suivi (🩹).

**Les essais réels (18/11)**, avec une panne volontaire : la fonction des contacts envoyée vers une propriété qui n'existe plus (`jobtitle_ancien`).

| Essai | Ce qui s'est passé | Ce qu'on a changé |
|---|---|---|
| **Run 4** (1er essai réel) | HubSpot refuse bien, la réparation se déclenche, mais l'IA n°1 écrit la correspondance **à l'envers** (`{"jobtitle_ancien": "jobtitle"}` au lieu de `{"job_title": "jobtitle"}`). Les garde-fous la bloquent (« champs inconnus du contrat ») : **rien de faux ne part**, résultat « non corrigée ». La raison était enregistrée dans `migration_log.self_heal`, mais **pas affichée dans le journal de l'action** | Raison affichée dans le journal, diagnostic en un clic, modèles de secours, messages d'erreur clairs ; le code remet la correspondance dans le bon sens avant les garde-fous ; consigne de l'IA avec la règle clés / valeurs et l'exemple exact |
| **Run 6** | ✅ **Réussi** : HubSpot refuse C-0004, les IA proposent `jobtitle`, garde-fous et IA n°2 valident, skill v2, **« envoyée après correction »**. C-0105 passe **directement** avec le skill réparé. Les 2 fiches sont dans HubSpot. Diagnostic entièrement vert | — |
| **Run 7** | ✅ **Réussite confirmée avec la version finale du code** (#55) : C-0004 « envoyée après correction », C-0105 envoyée directement, les 2 dans HubSpot. [Voir le résultat](https://projet-hackathon-jow2.vercel.app/?run=59f6de90-7885-42ea-abae-d6cffbc4f32b&total=2) | — |

**Ce qu'on en retient**
- **Une IA qui écrit du JSON se trompe de sens** : clés et valeurs inversées. La consigne seule ne suffit pas ; il faut **un code qui remet en forme** et **des garde-fous qui vérifient**.
- **Les garde-fous ont fait leur travail dès le 1er essai** : la réparation a échoué, mais **aucune donnée fausse** n'est partie.
- **Une raison enregistrée ne suffit pas, il faut qu'elle soit visible** : au run 4, la cause était dans la base de données mais pas dans le journal de l'action. L'afficher là où l'équipe regarde a transformé « ça ne marche pas » en « l'IA inverse la correspondance ».
- **Plusieurs barrières valent mieux qu'une** : l'IA n°2 ne voit la proposition qu'après les garde-fous du code ; sur tous les essais, rien de faux n'est passé.

## 8. Ce qui nous a surpris

- **L'agent « veut » répondre** : face à une information cachée, il invente une valeur crédible plutôt que de dire qu'il ne la voit pas. Il faut lui dire explicitement que le vide vaut mieux qu'une invention.
- **Une erreur « parfaite » ne se voit pas** : un faux numéro bien formaté passe toutes les règles de vérification. Seule la **capture d'écran** a permis de comprendre ce qui s'était passé.
- **Les consignes en français simple suffisent** : pas besoin de décrire le logiciel, seulement le but et les règles.
- **La moitié du travail est autour de l'agent**, pas dans l'agent : format imposé, contrôles, relances, mesures.

## 9. Les garde-fous qu'on a mis autour de l'agent

| Garde-fou | Où | Il protège contre… |
|---|---|---|
| Format de réponse imposé (9 champs + « error ») | `agent/runner/prompts.py` | Les réponses mal rangées |
| Règles strictes : ne rien inventer, lecture seule, ne rien corriger | `agent/runner/prompts.py` | Les valeurs inventées, les modifications dans l'ancien CRM |
| Contrôle d'identité + une relance | `agent/runner/run.py` | La mauvaise fiche ouverte |
| Vérification (ok / à vérifier / bloquée) | `pipeline/verification/` | E-mails invalides, champs obligatoires vides, doublons |
| Relecture ciblée d'un champ suspect (D13) | `agent/runner/run.py` | Les erreurs de lecture d'un champ précis |
| Capture d'écran gardée pour chaque fiche (D14) | `migration_log` + écran de suivi | Les erreurs invisibles : on peut toujours vérifier |
| Upsert sur `bascule_legacy_id` | `pipeline/hubspot/` | Les doublons dans HubSpot en cas de relance |

## 10. Nos conseils à une équipe qui démarre avec l'Agent API

1. **Imposer un format de réponse simple** (texte uniquement, chaîne vide si absent) dès le premier test.
2. **Activer le texte de la page** (`markdown: true`) dès qu'il faut recopier des chiffres ou des identifiants.
3. **Écrire noir sur blanc « ne devine jamais »** et dire quoi faire quand une information est cachée.
4. **Garder les captures d'écran** : c'est le meilleur outil pour comprendre une erreur.
5. **Ne jamais faire confiance à la réponse** : vérifier l'identifiant, le format, et relire en cas de doute.
6. **Une session par fiche** plutôt qu'une longue session : plus facile à relancer, à mesurer et à paralléliser.
7. **Arrêter d'attendre dès que la réponse est là** : sinon on perd du temps à chaque fiche.

## 11. Nos retours à H Company

Ce qui nous aurait fait gagner du temps, à transmettre à l'équipe H Company :

| Suggestion | Pourquoi |
|---|---|
| Une option pour que l'agent **réponde « non visible »** plutôt que de compléter une valeur | Notre seule erreur grave (le téléphone inventé) venait de là, et elle passait toutes nos règles |
| Mettre en avant **`markdown: true`** dans la documentation pour les tâches de recopie | Il a supprimé les erreurs de lecture de chiffres ; nous l'avons découvert en cherchant |
| Un exemple officiel de **fin de session** (« la réponse est là, arrête d'attendre ») | Notre code perdait ~20 s par fiche à attendre une confirmation inutile |
| Des **captures d'écran durables** (ou un export) | Elles sont notre preuve pour l'utilisateur ; nous avons dû les faire relayer par notre serveur |
| Plus d'**agents en parallèle** sur l'offre gratuite pendant un hackathon | Avec 3 agents, 105 fiches prennent 16,9 min (mesuré) ; une démo live en montre 5 ou 6 |

## 12. Pour le pitch et les questions du jury

**Trois messages à retenir**
1. **Le même agent, sans aucun réglage, a migré deux logiciels différents** : il ne reçoit que l'adresse. 100/100 fiches exactes sur la v1, 100/100 sur la v2 (autre mise en page, autres libellés).
2. **Il ne fait jamais seul** : 1 fiche exacte sur 5 sans garde-fous, 100 sur 100 avec.
3. **Chaque donnée est prouvée** : capture d'écran de la fiche d'origine pour chaque contact migré.
4. **Bascule se répare tout seul quand HubSpot change** : HubSpot refuse une fiche, deux IA corrigent le skill, la fiche repart, et la suivante passe directement (essai réel du 18/11).

**Réponses courtes aux questions probables**

| Question | Réponse |
|---|---|
| « Qu'avez-vous appris sur l'Agent API ? » | Qu'il sait naviguer seul dans un logiciel inconnu, mais qu'il préfère inventer une valeur crédible plutôt que laisser vide. On le lui interdit, et on vérifie tout derrière lui. |
| « Et si l'agent se trompe ? » | Il s'est trompé de fiche 3 fois sur la v1 et 1 fois sur la v2 (C-0009 au lieu de C-0090) : notre contrôle d'identité les a bloquées avant HubSpot, puis l'agent les a relues. Aucune mauvaise fiche n'est partie. Chaque fiche a sa capture d'écran. |
| « Pourquoi pas un script ou un robot RPA ? » | Pas d'API ni d'export, et aucune configuration : on l'a prouvé en migrant deux versions différentes du logiciel avec exactement les mêmes consignes. Un robot RPA aurait dû être réenregistré. |
| « Combien ça coûte ? » | Entre ~0,008 $ (v2) et ~0,015 $ (v1) par fiche, mesuré sur plus de 200 fiches : de ~25 à ~46 $ pour 3 000 fiches. |
| « Et si HubSpot change ? » | Ce que Bascule sait de HubSpot est dans un skill que deux IA tiennent à jour. On l'a testé en vrai (runs 6 et 7) : un champ HubSpot disparu, HubSpot refuse la fiche, les IA réparent, la fiche repart, la suivante passe directement. Une veille quotidienne lit aussi les nouveautés de HubSpot. |
| « Qu'est-ce qui a été le plus difficile ? » | Rendre l'agent fiable, pas le faire marcher : la première lecture a réussi tout de suite, les garde-fous ont pris le reste de la journée. |

## 13. Limites actuelles

- **Pas de connexion par mot de passe** dans l'ancien CRM (D11) : l'agent n'a pas encore été testé derrière un écran de connexion.
- **3 agents en parallèle** sur l'offre gratuite : une grosse migration prend plusieurs heures.
- **Les captures d'écran dépendent de H Company** : il faudra les copier chez nous pour les garder.
- **Données fictives uniquement** : pas encore testé sur un vrai vieux logiciel de client.

## 14. À compléter jeudi et vendredi

- [x] Migration complète sur la **2e version** : 105/105 lues, 100/100 exactes, 5/5 pièges, 16,9 min (section 2).
- [x] Résultat sur les **fiches pièges** : 5 / 5 traités comme prévu (section 6).
- [ ] Part des anomalies **corrigées par la relecture** (D13) sur une vraie erreur de lecture de l'agent. Sur les pièges, aucune des 3 relectures n'a inventé de correction (2 ont explicitement confirmé la donnée de l'ancien CRM) : c'était la donnée qui était fausse, pas la lecture.
- [x] Durée réelle **après correction**, mesurée : 16,9 min pour 105 fiches avec 3 agents, médiane 21 s par fiche.
- [ ] Ce qui s'est passé pendant la **démo live** de vendredi.
