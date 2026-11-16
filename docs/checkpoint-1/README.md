# Checkpoint 1 — Validation d'idée

**Projet :** Bascule — *Changez de logiciel, sans perdre vos données.*
**Événement :** Hackathon Eugenia 2026 « Build The Future »
**Échéance :** lundi 16 novembre 2026, avant 17h00

📄 **Livrable :** [Bascule_Livrable1_Validation_Idee_CORRIGE.pdf](./Bascule_Livrable1_Validation_Idee_CORRIGE.pdf) (5 slides)

---

## Contenu des slides

| Slide | Titre | Contenu |
|---|---|---|
| 1 | **Bascule** | Nom, slogan et principe : ancien CRM → agent H Company → CRM de destination |
| 2 | **Le problème** | Logiciel fermé, ressaisie manuelle, frein à la migration |
| 3 | **La solution** | Parcours en 4 étapes : CRM ancien simulé → agent H → vérification → CRM cible réel (HubSpot) |
| 4 | **Personas** | Camille (utilisatrice finale) et Thomas (client B2B potentiel) |
| 5 | **Stack et équipe** | Stack technique envisagée et rôles des six membres |

## Conformité aux attentes Eugenia

| Élément demandé | Où | ✓ |
|---|---|---|
| Maximum 5 slides | 5 slides | ✅ |
| Nom + slogan du projet | Slide 1 | ✅ |
| Problème expliqué clairement | Slide 2 | ✅ |
| Solution en une phrase | Slides 1 et 3 | ✅ |
| Personas utilisateurs cibles | Slide 4 | ✅ |
| Stack technique envisagée | Slide 5 | ✅ |
| Répartition des rôles dans l'équipe | Slide 5 | ✅ |

## Choix de cadrage

- **CRM cible réel : HubSpot**, alimenté via son API.
- **Ancien CRM simulé** : interface web sans export ni API, construite par l'équipe.
- **Supabase** (à la place d'Airtable) n'est **pas** le CRM cible : il sert de base cachée à l'ancien CRM et de journal de migration (mesures, anomalies).
- **n8n est exclu du MVP** : le rôle CAO couvre les automatisations et le marketing.
- Le prototype fonctionne uniquement sur **données fictives** (10 à 20 contacts synthétiques).
- Les accès Supabase sont protégés ; aucun secret n'est versionné dans ce dépôt.

## Historique

| Date | Modification |
|---|---|
| 16/11/2026 | Version validée des slides (`_CORRIGE`). |
| 16/11/2026 | Slide 5 : rôle CAO « workflows n8n, marketing » remplacé par « automatisations, marketing », pour refléter l'exclusion de n8n du MVP. |
| 16/11/2026 | Recadrage « Supabase n'est pas un CRM » (voir [CADRAGE.md](../CADRAGE.md)). Slide 3 : CRM cible « Mini-interface CRM connectée à Supabase » → « CRM réel : HubSpot, alimenté via son API ». Slide 5 : Supabase « Base cible, suivi et anomalies » → « Ancien CRM simulé, suivi, mesures ». |

> Les versions précédentes du PDF restent consultables dans l'historique Git du fichier.
