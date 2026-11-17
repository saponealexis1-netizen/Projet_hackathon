# Bascule — Business model

> **Version du 16/11/2026.** Les chiffres « coût de fonctionnement » seront mis à jour jeudi avec les mesures complètes d'Alexis (`pipeline/metrics/`).

**Légende des chiffres** : ✅ mesuré par l'équipe · 📚 source externe (liens en bas de page) · 🔎 hypothèse à valider en interview

---

## 1. En une phrase

**Bascule est payé par ceux qui vendent le nouveau CRM** (éditeurs et agences d'intégration) : ils offrent la migration à leurs prospects bloqués par un vieux logiciel sans export, et signent plus vite.

## 2. Le problème, en chiffres

- 📚 **La migration des données est le premier obstacle** à la mise en place d'un nouveau CRM : citée par **44 %** des PME interrogées au Royaume-Uni (enquête Workbooks).
- 📚 Les éditeurs facturent déjà l'onboarding d'un nouveau client : **1 500 $** (Professional) à **3 500 $** (Enterprise) chez HubSpot pour Sales Hub ou Service Hub (source tierce).
- 🔎 Une agence avec **3 000 fiches** dans un logiciel sans export : ~2 min par fiche → **~100 h** de ressaisie, soit **~3 000 €** (à 30 €/h chargé) et **2 à 3 semaines** d'équipe bloquée.

## 3. Clients : qui paie, qui utilise, qui en profite

| | Qui | Ce qu'il gagne |
|---|---|---|
| 💶 **Paie** | **Thomas**, responsable onboarding chez un éditeur CRM ou dans une **agence partenaire HubSpot** | Des ventes qui ne tombent plus à cause de la migration, un onboarding plus court |
| 🖥️ **Utilise** | L'équipe onboarding | Ne traite que les cas douteux au lieu de tout ressaisir |
| 🙂 **En profite** | **Camille**, gérante d'une petite agence | Change d'outil sans tout recopier ni perdre de données |

**Pourquoi ce sont eux qui paient, et pas la PME ?**
- Ils ont **plusieurs migrations par mois** : un besoin récurrent, pas ponctuel.
- Chaque migration réussie **débloque un abonnement** : leur retour sur investissement est direct.
- Ils **facturent déjà l'onboarding** : Bascule s'insère dans un budget qui existe.

**Pour la démo**, le nouveau CRM est **HubSpot** (voir [CADRAGE.md](../CADRAGE.md)).

## 4. Proposition de valeur

| Pour l'éditeur / l'agence | Pour la PME |
|---|---|
| Lever la dernière objection avant la signature | Garder toutes ses données |
| Proposer « migration offerte » comme argument commercial | Ne rien ressaisir |
| Onboarding en heures au lieu de semaines | Continuer à travailler pendant la migration |
| Ne traiter que les cas douteux, signalés automatiquement | Des données vérifiées : doublons et anomalies signalés |

## 5. Concurrence et différenciation

| Solution | Comment ça marche | Limite face à notre cas |
|---|---|---|
| Ressaisie interne | Un salarié ou un stagiaire recopie | Lent (~100 h pour 3 000 fiches), erreurs |
| Prestataire de saisie (souvent offshore) | Facturé à l'heure ou à la fiche | Accès aux données confié à un tiers, délais, qualité variable |
| Outils de migration (MigrateMyCRM, ex-Data2CRM) | 📚 Forfaits de ~300 à 3 000 $ | **Besoin d'une API ou d'un export** : inutilisables sur un vieux logiciel fermé |
| Robots logiciels classiques (RPA) | Scripts qui rejouent des clics | À reprogrammer pour chaque logiciel, cassent si l'écran change |
| **Bascule** | Un agent IA qui **lit l'écran comme un humain** | — |

> **Notre angle** : les outils de migration ont besoin d'une API ou d'un export. **Bascule commence là où ils s'arrêtent.**

## 6. Offre et prix

| Offre | Pour qui | Prix 🔎 |
|---|---|---|
| **À la fiche** | Petites migrations (moins de ~1 000 fiches), tests | **0,50 € / fiche**, minimum 250 € |
| **Forfait par client migré** | Éditeur ou agence qui offre la migration | **490 €** jusqu'à 2 000 fiches · **990 €** jusqu'à 10 000 fiches |
| **Partenaire** | Plusieurs migrations par mois | Abonnement mensuel avec volume inclus, sur devis |

**Repère** : pour 3 000 fiches, Bascule coûte **990 €** au lieu de **~3 000 €** de ressaisie, et tourne en **~4 h** au lieu de 3 semaines (voir section 7).

## 7. Coût de fonctionnement et marge

### ✅ Mesure réelle (16/11)

Test de l'agent H Company `h/web-surfer-flash` sur un site public de démonstration (books.toscrape.com), dans les conditions de notre cas : **ouvrir une liste → cliquer sur une fiche → extraire 5 champs en JSON**. 3 agents lancés en parallèle.

| | Fiche 1 | Fiche 2 | Fiche 3 | **Moyenne** |
|---|---|---|---|---|
| Réussite | ✅ | ✅ | ✅ | **3 / 3** |
| Étapes de l'agent | 6 | 8 | 11 | **~8** |
| Durée | 47 s | 49 s | 48 s | **~48 s** |
| Coût H Company | 0,015 $ | 0,019 $ | 0,026 $ | **~0,020 $** |

⚠️ Mesuré sur 3 fiches d'un site de test, pas encore sur notre ancien CRM. À confirmer jeudi sur 20 fiches.

### Coût par fiche

| Poste | Coût |
|---|---|
| ✅ Agent H Company (lecture d'une fiche) | ~0,020 $ |
| ✅ Vérification (règles automatiques, sans modèle d'IA : `pipeline/verification/`) | 0 $ |
| 🔎 Marge de sécurité (relance d'une fiche ratée par l'agent) | ~0,005 $ |
| HubSpot, Supabase, Vercel | Offres gratuites pendant le MVP |
| **Total** | **~0,025 $ par fiche** |

### Marge (exemple : 3 000 fiches, forfait 990 €)

En comptant 1 $ ≈ 1 € pour rester prudent :

| | Montant |
|---|---|
| Prix de vente | 990 € |
| Coût de fonctionnement (3 000 × 0,025) | ~75 € |
| **Marge brute** | **~92 %** |
| Si le coût réel est 5 fois plus élevé | ~375 € → marge **~62 %** |

### Vitesse selon l'offre H Company 📚

| Offre H Company | Prix | Agents en parallèle | Fiches / heure (à ~48 s) | 3 000 fiches en… |
|---|---|---|---|---|
| Free (actuelle) | 0 $ | 3 | ~225 | ~13 h |
| Builder | 20 $ / mois | 10 | ~750 | **~4 h** |
| Startup | 200 $ / mois | 100 | ~7 500 | < 30 min |

→ Dès le premier client, l'offre **Builder (20 $/mois)** suffit pour migrer une agence en une demi-journée.

## 8. Taille du marché 🔎

Estimation volontairement simple, à affiner :

- 📚 On compte **entre 6 000 et 7 500 partenaires HubSpot** dans le monde (estimations tierces).
- 🔎 Si chacun migre **10 clients par an** depuis un vieux logiciel sans export, cela fait **60 000 à 75 000 migrations par an**.
- 🔎 À **490 à 990 €** la migration : **~30 à 75 M€ par an**, sur le seul écosystème HubSpot.

Les autres éditeurs (Salesforce, Pipedrive, Zoho, éditeurs métier) élargissent ce marché.

## 9. Go-to-market (premières étapes)

1. **Agences partenaires HubSpot en France** : ce sont elles qui font l'onboarding des clients et qui butent sur les migrations. Approche directe via LinkedIn et l'annuaire des partenaires HubSpot.
2. **Éditeurs de logiciels métier** (immobilier, artisans, cabinets) : leurs prospects sont souvent sur de vieux logiciels installés en local.
3. **À terme** : une application sur la marketplace HubSpot, pour que la migration se lance depuis HubSpot.

## 10. Suivi des crédits

**Chacun a sa propre organisation H Company, sa clé et ses crédits** (voir [ORGANISATION.md](../ORGANISATION.md), section 8). Ce tableau suit **les crédits de Maxime**.

| Plateforme | Crédit | Consommé | Vérifié le |
|---|---|---|---|
| **H Company** (offre Free, organisation de Maxime) | 60 M tokens / mois, **3 agents en parallèle max par personne** | 4 sessions de test, ~0,065 $ au total | 16/11 |
| **Hugging Face** | 50 € (coupon hackathon) | — | à vérifier |
| **Vercel v0** | Code hackathon | — | à vérifier |
| **HubSpot** | Offre gratuite | — | — |

- Vérifier les tokens H Company restants : onglet **Facturation** de platform.hcompany.ai, ou `GET https://agp.eu.hcompany.ai/api/v2/quota/tokens` avec la clé API.
- ⚠️ **3 agents en parallèle maximum par personne** en offre gratuite : chacun a sa propre limite, personne ne bloque les autres.
- Les crédits du hackathon sont sur le compte d'équipe Eugenia.

## 11. Hypothèses à valider en interview

| # | Question | Pour valider |
|---|---|---|
| 1 | Perdez-vous des ventes à cause de la migration ? Combien par mois ? | Le problème |
| 2 | Combien vous coûte aujourd'hui l'onboarding d'un client ? | Le budget existant |
| 3 | Paieriez-vous 490 € par client migré ? Ou plutôt à la fiche ? | Le prix |
| 4 | (PME) Combien de fiches dans votre logiciel ? Ne peut-il vraiment rien exporter ? | La cible |
| 5 | (PME) Votre peur n°1 : perdre des données ou qu'elles fuient ? | Le discours sécurité |

## 12. Questions probables du jury

| Question | Réponse courte |
|---|---|
| « Pourquoi pas un simple script ou un outil de migration ? » | Pas d'API, pas d'export : la seule porte d'entrée est l'écran. |
| « Et si l'agent se trompe ? » | Chaque fiche est classée **ok / à vérifier / bloquée** ; les fiches bloquées ne partent pas dans HubSpot. |
| « Et la sécurité des données ? » | Accès en lecture seule, serveurs européens de H Company. Coffre-fort à mots de passe (vault) de H Company **prévu** après le MVP. |
| « Combien ça coûte à faire tourner ? » | ✅ ~0,02 $ par fiche mesuré côté agent ; ~92 % de marge sur un forfait. |
| « Pourquoi les éditeurs paieraient ? » | Ils facturent déjà l'onboarding, et la migration est le premier obstacle à la mise en place d'un nouveau CRM (44 %). |

---

## Sources

- ✅ Mesures H Company : sessions de test du 16/11/2026, champ `metrics` de l'API (`GET /sessions/{id}/changes`).
- Offres et limites H Company : [Plans and limits](https://hub.hcompany.ai/agents-api/plans-and-limits) (documentation officielle, vérifiée le 16/11/2026).
- Obstacle n°1 = migration (44 %) : [Digital Strategy Consulting (enquête Workbooks)](https://digitalstrategyconsulting.com/content/content-marketing/more-than-half-of-british-small-and-medium-businesses-have-changed-crm-supplier/32429).
- Frais d'onboarding HubSpot (source tierce, mise à jour le 12/11/2026) : [INSIDEA](https://insidea.com/blog/hubspot/hubspot-onboarding-cost).
- Partenaires HubSpot (estimations tierces) : [ProvenROI](https://www.provenroi.com/hubspot-partner-agencies-complete-guide/) (« plus de 6 000 »), [INSIDEA](https://insidea.com/blog/hubspot/best-hubspot-partner-agencies) (« plus de 7 500 »).
- Outils de migration : [MigrateMyCRM / Data2CRM sur Capterra](https://www.capterra.com/p/146563/Data2CRM-Migration/pricing/), [SyncMatters](https://support.syncmatters.com/how-much-does-a-migration-cost) (pages à vérifier dans un navigateur : elles bloquent la lecture automatique).
