# Organisation de l'équipe — mardi → vendredi

Ce document dit **qui fait quoi, quand, dans quel dossier**, et **comment on travaille à plusieurs sur le même dépôt** avec Claude Code sans se marcher dessus.

> Cadrage du produit : voir [CADRAGE.md](CADRAGE.md).

---

## 1. Les règles d'or

1. **Une personne = une conversation Claude Code = une branche par tâche.**
2. **Personne ne fusionne (merge), sauf le chef de projet : Alexis.** Chacun pousse sa branche et ouvre une pull request (PR) vers `main`.
3. **Quand une tâche est finie**, la personne envoie à Alexis le message « PRÊT POUR MERGE » (modèle en section 7), **puis enchaîne directement sur sa tâche suivante** sans attendre.
4. **Chacun reste dans ses dossiers** (section 3). Pour toucher au dossier de quelqu'un d'autre, on prévient d'abord.
5. **Aucun secret dans Git** : clés H Company, HubSpot et Supabase uniquement dans `.env.local` (jamais commité) et dans les variables d'environnement Vercel.
6. **Des petites PR souvent**, plutôt qu'une énorme PR le jeudi soir.
7. **Alexis fusionne régulièrement** (dès qu'un message arrive, ou au moins toutes les heures) pour que personne ne reste bloqué.

## 2. Qui fait quoi

| Membre | Rôle | Responsabilité principale cette semaine |
|---|---|---|
| **Alexis Sapone** | CDO + **chef de projet** | **Fusions**, coordination, jeu de données synthétique, Supabase (2 tables), envoi vers HubSpot via API, mesures |
| **Victoria Ifrah** | CTO | Socle technique (Next.js, Vercel), ancien CRM simulé (fonctionnement + look « vieux logiciel »), **intégration de l'agent H Company**, orchestration, schéma d'architecture, démo live + plan B |
| **Inès Soubran** | CAIO | Instructions de l'agent (ce qu'il doit lire et comment), **vérification IA** (mapping, doublons, anomalies), écran de suivi de migration |
| **Maxime Bazin** | CEO | Parcours utilisateur, pitch, business model, coût de run, Loom de mercredi, vidéo démo, pitch deck, fiche projet |
| Mehdi Zitouni | CPO | ⏸️ **En standby** cette semaine — ses tâches sont réparties ci-dessus |
| Natalia Medrano | CAO | ⏸️ **En standby** — peut rejoindre Maxime (marketing, post LinkedIn) si disponible |

## 3. Qui possède quels dossiers

Chaque dossier a **un seul propriétaire**. C'est ce qui permet de travailler en parallèle sans conflit Git.

```
.
├── apps/
│   ├── legacy-crm/          Victoria  (ancien CRM simulé, fonctionnement + style)
│   └── dashboard/           Inès      (écran de suivi de migration)
├── agent/
│   ├── runner/              Victoria  (appel de l'Agent API, orchestration)
│   └── prompts/             Inès      (instructions données à l'agent)
├── pipeline/
│   ├── verification/        Inès      (mapping, doublons, anomalies)
│   ├── hubspot/             Alexis    (création des contacts via l'API HubSpot)
│   └── metrics/             Alexis    (taux de réussite, temps, coût)
├── data/                    Alexis    (contacts synthétiques)
├── supabase/                Alexis    (schéma SQL des 2 tables)
├── shared/
│   └── contact.schema.json  Alexis    ⚠️ CONTRAT COMMUN — toute modification annoncée à toute l'équipe
└── docs/
    ├── architecture/        Victoria  (schéma d'architecture)
    ├── parcours/            Maxime    (parcours utilisateur)
    ├── pitch/               Maxime    (pitch, business model, coût de run)
    └── checkpoint-2..4/     Maxime    (livrables Eugenia, déposés par Alexis)
```

> Le langage de l'agent (TypeScript ou Python) sera fixé par Victoria **mardi après la session technique H Company (11h)**, selon les exemples officiels.

## 4. Le contrat commun : le format d'un contact

C'est **la première chose à faire mardi matin** (Alexis, validé par Inès et Victoria). Une fois ce format fixé, tout le monde peut avancer en parallèle **sans attendre que l'agent marche** : chacun travaille avec des contacts d'exemple.

Proposition de départ :

```json
{
  "legacy_id": "C-0042",
  "first_name": "Camille",
  "last_name": "Martin",
  "email": "camille.martin@exemple.fr",
  "phone": "+33 6 12 34 56 78",
  "company": "Agence Lumière",
  "job_title": "Gérante",
  "city": "Lyon",
  "notes": "Client depuis 2019"
}
```

Qui produit / qui consomme :

```
Ancien CRM ──(écran)──► Agent H ──► contact JSON ──► Vérification ──► HubSpot
 (Victoria)            (Victoria     (contrat         (Inès)          (Alexis)
                        + Inès)       Alexis)              │
                                                           └──► Supabase migration_log ──► Mesures      + Écran de suivi
                                                                (Alexis)                   (Alexis)       (Inès)
```

## 5. Le planning tâche par tâche

### Mardi 17 — Poser les fondations

| Qui | Tâche | Branche | Terminé quand… |
|---|---|---|---|
| Victoria | Socle Next.js + déploiement Vercel | `victoria/socle` | Une page « Hello » est en ligne sur Vercel |
| Alexis | Contrat `contact.schema.json` + 20 contacts d'exemple | `alexis/contrat-donnees` | Validé par Inès et Victoria, fusionné **avant midi** |
| Alexis | Supabase : tables `legacy_contacts` et `migration_log` + chargement des 20 contacts | `alexis/supabase` | Les 20 contacts sont visibles dans Supabase |
| Victoria | Ancien CRM simulé : liste paginée + fiche détail, sans export, look « vieux logiciel » | `victoria/legacy-crm` | On peut ouvrir chaque fiche dans le navigateur |
| Victoria | Session tech H Company (11h, 15h) → premier agent qui lit **une fiche** | `victoria/agent-v0` | L'agent renvoie les champs d'une fiche |
| Inès | Premières instructions de l'agent (quelle page ouvrir, quoi lire) | `ines/prompts-v0` | Testées avec Victoria sur une fiche |
| Alexis | Compte HubSpot gratuit + test de création d'un contact par API | `alexis/hubspot-v0` | Un contact de test apparaît dans HubSpot |
| Maxime | Business model v1 (qui paie, combien) + suivi des crédits | `maxime/business` | Une page dans `docs/pitch/` |
| Maxime | Premier parcours utilisateur (Camille et Thomas) | `maxime/parcours` | Brouillon dans `docs/parcours/` |

### Mercredi 18 — Premier parcours complet · livrable 17h

| Qui | Tâche | Branche | Terminé quand… |
|---|---|---|---|
| Victoria | Agent qui parcourt **plusieurs fiches** (liste → fiche → retour) | `victoria/agent-multi` | 5 fiches extraites d'affilée |
| Inès | Vérification : mapping, doublons, champs manquants ou mal formés | `ines/verification` | Testée sur les contacts d'exemple |
| Alexis | Envoi des contacts vérifiés vers HubSpot + écriture dans `migration_log` | `alexis/hubspot` | 5 contacts arrivent dans HubSpot |
| Victoria | Orchestration : agent → vérification → HubSpot, en un seul lancement | `victoria/orchestration` | **Parcours complet sur 5 fiches** |
| Victoria | Schéma d'architecture | `victoria/architecture` | Dans `docs/architecture/` |
| Maxime | Parcours utilisateur final + mini pitch Loom (2 min) + roadmap jusqu'à jeudi | `maxime/checkpoint-2` | Dans `docs/checkpoint-2/` |
| **Alexis** | **Fusion et dépôt du livrable 2 avant 17h** | — | Livrable rendu |

### Jeudi 19 — Fiabiliser et mesurer

| Qui | Tâche | Branche | Terminé quand… |
|---|---|---|---|
| Victoria | Passage à **20 fiches**, gestion des erreurs et des relances | `victoria/agent-20` | 20 fiches traitées en un lancement |
| Inès | Cas pièges dans l'ancien CRM (doublon, champ vide, format bizarre) + amélioration des instructions | `ines/cas-pieges` | Les pièges sont détectés et signalés |
| Alexis | Mesures : taux de réussite par fiche et par champ, temps, coût par fiche | `alexis/metrics` | Tableau de chiffres dans `pipeline/metrics/` |
| Inès | Écran de suivi de migration (fiches traitées, anomalies, chiffres) | `ines/dashboard` | Lisible par le jury |
| Victoria | **Plan B démo** : vidéo de secours + jeu de données de secours | `victoria/plan-b` | La démo peut être montrée même si le réseau lâche |
| Maxime | Coût de run, go-to-market, brouillon du pitch deck (8 à 12 slides) | `maxime/pitch-deck` | Brouillon relu par Alexis |
| Tous | **Répétition de démo à 18h** | — | Démo réussie de bout en bout |

### Vendredi 20 — Livrer

| Heure | Qui | Tâche |
|---|---|---|
| avant 9h | Tous | **Gel du code** : plus de nouvelle fonctionnalité, seulement des corrections |
| 9h–11h | Victoria + Alexis | README final : comment tester, lien du prototype, architecture |
| 9h–11h | Maxime + Inès | Vidéo démo (5 min) + fiche projet |
| 9h–11h | Inès | Retours sur l'Agent API : ce qui a marché, ce qui a cassé, ce qui nous a surpris |
| **11h** | **Alexis** | **Dépôt : prototype, fiche projet + repo, vidéo** |
| 11h–15h | Maxime (+ tous) | Pitch deck final, avec les vrais chiffres d'Alexis |
| **15h** | **Alexis** | **Dépôt du pitch deck** |
| après 15h | Maxime | Pitch (6 min) + Q&R (4 min) |

## 6. Le circuit d'une tâche

### C'est quoi une pull request ?

Une **pull request (PR)** est une page GitHub où quelqu'un dit : « Voici mon travail, je propose de l'ajouter à la version officielle (`main`). » Alexis y voit les fichiers modifiés, la description, et un bouton **« Merge pull request »**. Tant qu'il n'a pas cliqué, `main` ne change pas.

```
main (version officielle) ─────────────●───────────►
                         \             ↑
victoria/agent-v0         ●───●───●────┘
                          son travail   la PR = « Alexis, tu peux l'ajouter ? »
```

### Les étapes

```
1. Je pars de main à jour          →  Claude : « repars de main à jour »
2. Je crée ma branche              →  prenom/tache
3. Je travaille avec Claude Code dans MES dossiers
4. C'est fini : Claude committe, pousse ma branche et ouvre une PR vers main (sans fusionner)
5. J'envoie à Alexis le message « PRÊT POUR MERGE »
6. J'ENCHAÎNE tout de suite sur ma tâche suivante (retour à l'étape 1)
7. Alexis relit et fusionne — ou laisse un commentaire et je corrige
```

> Le point de contrôle est la **fusion**, pas le commit ni le push. Pousser souvent sur sa propre branche est conseillé : rien n'est perdu si la session Claude se ferme.

### Enchaîner les tâches

Pour démarrer la tâche suivante, dire à Claude :

> « Tâche suivante : `<nom>`. Repars de `main` à jour, sur une nouvelle branche `<prenom>/<tache>`. »

| Situation | Que faire |
|---|---|
| La tâche suivante ne dépend pas de la précédente | Repartir de `main` à jour (cas normal) |
| Elle dépend de la précédente, **déjà fusionnée** | Repartir de `main` à jour |
| Elle dépend de la précédente, **pas encore fusionnée** | Demander à Alexis de fusionner vite (« ça me bloque »), ou dire à Claude de repartir de sa branche précédente |

### Message « PRÊT POUR MERGE » (à envoyer à Alexis)

```
✅ PRÊT POUR MERGE — <prénom> / <nom de la tâche>
PR : <lien de la pull request>
Ce qui est fait : <2-3 lignes>
Comment vérifier : <1 commande ou 1 lien>
Dossiers touchés : <liste>
Dépend de / bloque : <rien, ou la tâche concernée>
```

### Ce que vérifie Alexis avant de fusionner

- [ ] La PR ne touche que les dossiers de la personne.
- [ ] Aucune clé ni mot de passe dans les fichiers.
- [ ] Le contrat `contact.schema.json` n'a pas changé sans accord.
- [ ] Rien d'autre n'est en cours qui dépend de cette PR.
- [ ] Le site Vercel fonctionne toujours après la fusion.

## 7. Le prompt de départ pour chaque conversation Claude Code

Chacun colle ce modèle au début de sa conversation, en remplaçant les `<…>` :

```
GO — BASCULE / <PRÉNOM> (<RÔLE>) — <NOM DE LA TÂCHE>

CONTEXTE
Lis d'abord README.md, docs/CADRAGE.md et docs/ORGANISATION.md.

BRANCH : <prenom>/<tache>  (créée depuis main à jour)

PURPOSE
<ce que la tâche doit produire, en 1-2 phrases>

ABSOLUTE BOUNDARY
- Travailler uniquement dans : <mes dossiers>.
- Ne pas modifier shared/contact.schema.json sans accord d'Alexis.
- Aucun secret dans Git (utiliser .env.local).
- Ne jamais fusionner. Ne jamais pousser sur main.

DONE WHEN
<critère "terminé quand…" du planning>

FINAL REPORT — FRANÇAIS
- Ce qui est fait, comment le vérifier, fichiers modifiés.
- Committer, pousser ma branche et ouvrir une PR vers main.
- Rédiger le message « PRÊT POUR MERGE » pour Alexis (modèle docs/ORGANISATION.md).

STOP_FOR_USER_DECISION : ne pas fusionner.
```

## 8. Avant mardi matin

- [ ] Ajouter Maxime, Victoria et Inès comme **collaborateurs** du dépôt GitHub.
- [ ] Partager en privé (pas dans Git, pas sur Slack public) : clé Agent API H Company, jeton HubSpot, clés Supabase.
- [ ] Créer un canal d'équipe pour les messages « PRÊT POUR MERGE ».
- [ ] Vérifier que le dépôt est accessible au jury.
