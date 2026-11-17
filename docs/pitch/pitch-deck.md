# Bascule — Pitch deck (brouillon)

> **Brouillon du 17/11/2026**, à relire par Alexis. Version finale vendredi avant 15h, avec les vrais chiffres de `pipeline/metrics/`.
> **Format demandé** : 8 à 12 slides, dans cet ordre : problème, solution, démo, business model, go-to-market, architecture technique, limites et roadmap, coût de run.
> **Temps de parole** : 6 min de pitch + 4 min de questions.

**Légende** : ✅ mesuré ou testé · 📚 source externe · 🔎 hypothèse · `[à remplir]` = à compléter avant vendredi

**Règle de mise en forme** : **15 mots maximum à l'écran par slide** (hors tableaux de chiffres). Le reste se dit à l'oral.

---

## Vue d'ensemble

| # | Slide | Temps |
|---|---|---|
| 1 | Accroche et titre | 0:20 |
| 2 | Problème | 0:35 |
| 3 | Solution | 0:30 |
| 4 | Démo live | 2:00 |
| 5 | Business model | 0:30 |
| 6 | Go-to-market | 0:20 |
| 7 | Architecture technique et Agent API | 0:40 |
| 8 | Limites et roadmap | 0:25 |
| 9 | Coût de run | 0:25 |
| 10 | Équipe et conclusion | 0:15 |
| | **Total** | **6:00** |

---

## Slide 1 — Accroche et titre

**À l'écran** : une capture de l'ancien CRM « 2010 », puis le titre.
- **Bascule** — « Changez de logiciel, sans perdre vos données. »

**Ce qu'on dit**
> « Camille dirige une petite agence. Dans son logiciel installé en 2010, il y a 3 000 fiches clients. Elle veut passer sur HubSpot. Elle cherche le bouton “exporter”… il n'existe pas. Nous sommes Bascule, et nous avons construit l'agent qui la sort de là. »

---

## Slide 2 — Problème

**À l'écran**
- **44 %** des PME : la migration est le premier obstacle 📚
- **3 000 fiches = 100 heures** de ressaisie 🔎
- Pas d'API, pas d'export : **aucun outil de migration ne marche**

**Ce qu'on dit**
> « Camille n'est pas un cas isolé : pour 44 % des PME, la migration des données est le premier obstacle au changement de CRM. Sans export, il reste une option : tout recopier. 3 000 fiches, c'est 100 heures. Et pour Thomas, qui vend HubSpot à Camille, c'est la dernière objection avant la signature. Souvent, la vente tombe. »

---

## Slide 3 — Solution

**À l'écran** : 4 étapes

| 1. Lire | 2. Vérifier | 3. Écrire | 4. Suivre |
|---|---|---|---|
| L'agent lit chaque fiche à l'écran | ok / à vérifier / bloquée | Création dans HubSpot | Migration en direct + bilan |

**Ce qu'on dit**
> « Bascule commence là où les outils de migration s'arrêtent. Pas d'API ? Pas d'export ? Notre agent lit l'écran, comme un humain. Notre application vérifie chaque fiche, n'envoie dans HubSpot que celles qui sont sûres, et Thomas ne traite que les cas douteux. »

---

## Slide 4 — Démo live (2 min)

**À l'écran** : on bascule sur les vraies applications. Scénario détaillé : [parcours utilisateur, section 7](../parcours/parcours-utilisateur.md).

| Temps | On montre |
|---|---|
| 0:00 | L'ancien CRM : on cherche le bouton d'export… il n'y en a pas |
| 0:20 | Thomas clique sur « Lancer la migration » dans l'écran de suivi |
| 0:35 | Les agents H ouvrent les fiches en direct |
| 1:10 | Le tableau de bord se remplit ; une fiche bloquée s'affiche avec sa raison |
| 1:40 | Les contacts sont dans HubSpot |

**À préparer** : les 20 fiches sont lancées **juste avant le pitch** (✅ ~48 s par fiche, 3 agents en parallèle par personne). On montre le lancement en direct, puis le résultat déjà rempli.

**Plan B** : vidéo enregistrée de la même démo.

---

## Slide 5 — Business model

**À l'écran**
- **Qui paie** : l'éditeur ou l'agence qui vend le nouveau CRM
- **990 €** par client migré (jusqu'à 10 000 fiches) 🔎
- 🗣️ `[citation d'interview à remplir — voir « Interviews à faire » en bas]`

**Ce qu'on dit**
> « Ce n'est pas Camille qui paie, c'est Thomas. Chaque migration réussie lui débloque un abonnement, et il facture déjà l'onboarding : entre 1 500 et 3 500 dollars chez HubSpot. Nous lui vendons la migration 490 euros jusqu'à 2 000 fiches, 990 euros jusqu'à 10 000. Pour 3 000 fiches, c'est trois fois moins cher que la ressaisie, et quelques heures au lieu de trois semaines. »

Grille complète (à la fiche, forfait, partenaire) : [business-model.md](business-model.md).

---

## Slide 6 — Go-to-market

**À l'écran**
1. Agences partenaires HubSpot (France)
2. Éditeurs de logiciels métier
3. Application sur la marketplace HubSpot

**Ce qu'on dit**
> « On commence par les agences partenaires HubSpot : elles font l'onboarding des clients et butent sur les migrations chaque semaine. Il y en a entre 6 000 et 7 500 dans le monde, et elles sont toutes listées dans l'annuaire HubSpot. »

---

## Slide 7 — Architecture technique et Agent API

**À l'écran** : le schéma de Victoria (`docs/architecture/`). En attendant, celui de [CADRAGE.md](../CADRAGE.md) :

```
Ancien CRM ──écran──► Agents H Company ──JSON──► Vérification ──API──► HubSpot
                                                       │
                                                       ▼
                                          Supabase ──► Écran de suivi
```

**Ce qu'on utilise de l'Agent API de H Company**

| Fonction | Ce qu'elle nous apporte | État |
|---|---|---|
| Agent qui navigue à l'écran (`h/web-surfer-flash`) | Lire un logiciel sans API ni export | ✅ testé |
| Sortie JSON structurée (schéma imposé à la réponse) | Chaque fiche arrive au format du contrat commun, prête à vérifier | ✅ testé |
| Plusieurs agents en parallèle | 3 fiches lues en même temps (10 avec l'offre Builder) | ✅ testé |
| Suivi des sessions (étapes, coût, statut) | Le coût et le temps par fiche affichés en direct | ✅ testé |
| Nombre maximal d'étapes par fiche | Un agent bloqué n'immobilise pas la migration | `[à confirmer par Victoria]` |

**Ce qu'on dit**
> « L'agent H est utilisé là où il est indispensable : lire un logiciel fermé. On lui impose un format de réponse, on en lance plusieurs en parallèle, et on suit le coût de chaque fiche en direct. Côté HubSpot, on passe par son API : c'est plus fiable. »

---

## Slide 8 — Limites et roadmap

**À l'écran**

| Aujourd'hui (MVP) | Ensuite |
|---|---|
| Contacts uniquement | Notes et pièces jointes |
| Ancien CRM sans mot de passe | Connexion sécurisée (coffre-fort H Company) |
| HubSpot uniquement | Salesforce, Pipedrive, Zoho |

**Ce qu'on dit**
> « Notre MVP migre les contacts, sur un ancien CRM sans mot de passe, vers HubSpot. Les fiches bloquées se corrigent encore à la main. La suite : les notes et pièces jointes, la connexion sécurisée avec le coffre-fort de H Company, et d'autres CRM cibles. »

---

## Slide 9 — Coût de run

**À l'écran**

| | Valeur |
|---|---|
| Coût par fiche | **~0,02 $** ✅ `[à remplir : mesure jeudi sur 20 fiches]` |
| Taux de réussite | **3 / 3** ✅ `[à remplir : x / 20]` |
| Marge sur un forfait de 990 € | **~92 %** |

**Ce qu'on dit**
> « Chaque fiche nous coûte environ deux centimes, en environ 48 secondes. Pour 3 000 fiches, c'est 75 dollars de coût pour 990 euros de chiffre d'affaires. Même si ce coût était cinq fois plus élevé, la marge resterait au-dessus de 60 %. »

---

## Slide 10 — Équipe et conclusion

**À l'écran**

| Maxime Bazin | Victoria Ifrah | Inès Soubran | Alexis Sapone | Mehdi Zitouni | Natalia Medrano |
|---|---|---|---|---|---|
| CEO | CTO | CAIO | CDO + chef de projet | CPO | CAO |

- « Changez de logiciel, sans perdre vos données. »

**Ce qu'on dit**
> « Bascule, c'est la migration qui ne bloque plus la vente. Merci ! »

---

## Questions probables du jury

| Question | Réponse courte |
|---|---|
| « Pourquoi un agent plutôt qu'un script ? » | Pas d'API, pas d'export : la seule porte d'entrée est l'écran. |
| « Et si l'agent se trompe ? » | Chaque fiche est classée ok / à vérifier / bloquée ; les fiches bloquées ne partent pas dans HubSpot. |
| « Et la sécurité ? » | L'agent ne fait que lire. Serveurs européens de H Company. Coffre-fort à mots de passe prévu après le MVP. |
| « Qui paie, et pourquoi ? » | L'éditeur ou l'agence : il facture déjà l'onboarding, et la migration bloque ses ventes. |
| « Avez-vous parlé à des clients ? » | `[à remplir avec les interviews]` |
| « Qu'avez-vous appris sur l'Agent API ? » | `[à remplir avec les retours d'Inès vendredi]` |

---

## Interviews à faire d'ici jeudi (Maxime)

**Objectif** : une vraie citation pour la slide 5 et une réponse à « Avez-vous parlé à des clients ? ».

**Qui appeler** : 2 ou 3 agences partenaires HubSpot en France (annuaire des partenaires HubSpot, LinkedIn), ou des responsables onboarding d'éditeurs de CRM.

**L'appel en 5 minutes**

1. « Quand un nouveau client arrive avec un vieux logiciel, comment récupérez-vous ses données ? »
2. « Ça vous est déjà arrivé qu'un logiciel n'ait aucun export ? Qu'avez-vous fait ? »
3. « Combien de temps ça vous prend, en moyenne ? »
4. « Une migration faite par un agent IA en quelques heures, à environ 1 000 € par client : ça vous intéresserait ? »
5. « Je peux citer votre réponse, avec ou sans votre nom ? »

**À noter après chaque appel** : le nom de l'agence (si accord), la phrase la plus forte mot pour mot, et la réponse à la question 4.

---

## À faire avant vendredi 15h

- [ ] 2 ou 3 interviews → citation de la slide 5 et réponse à « Avez-vous parlé à des clients ? » (Maxime)
- [ ] Remplir les `[à remplir]` de la slide 9 avec les mesures d'Alexis (jeudi)
- [ ] Remplacer le schéma de la slide 7 par celui de Victoria, et confirmer la ligne « nombre maximal d'étapes »
- [ ] Ajouter les captures : ancien CRM, écran de suivi, HubSpot
- [ ] Mettre en forme les slides (15 mots maximum à l'écran)
- [ ] Chronométrer le pitch à voix haute : 6 min maximum
