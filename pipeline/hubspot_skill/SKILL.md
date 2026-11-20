# Skill HubSpot — Bascule

> **Version 2** du 2026-11-20 · IA n°1 Qwen/Qwen3-32B (proposition) + IA n°2 Qwen/Qwen3-Next-80B-A3B-Instruct (validation)
> Fichier **généré** à partir de `skill.json` : ne pas le modifier à la main.
> Mis à jour par la veille automatique (2 IA qui se contrôlent), voir [README](README.md).

## 1. Où ranger chaque information

| Champ Bascule | Propriété HubSpot |
|---|---|
| `legacy_id` | `bascule_legacy_id` 🔒 |
| `first_name` | `firstname` |
| `last_name` | `lastname` |
| `email` | `email` |
| `phone` | `phone` |
| `company` | `company` |
| `job_title` | `jobtitle` |
| `city` | `city` |
| `notes` | `bascule_notes` |

## 2. Ce que HubSpot refuse

- E-mails dont l'extension est : `.example` → bloqués dès la vérification.

## 3. Erreurs déjà rencontrées

- **adresse e-mail invalide (e-mail en .example)** (2026-11-17) : HubSpot refuse les domaines réservés en .example → Bloquer ces e-mails dès la vérification (règle refused_email_tlds)

## 4. Nouveautés HubSpot qui nous concernent

- 2026-12-04 — **Sunsetting Pipelines API V1** : L'API Pipelines V1 sera désactivée le 4 décembre 2026. Les intégrations utilisant cette version devront migrer vers la version 2026-03 ou ultérieure. *(impact : alerte)*
- 2026-08-11 — **Validation CRM API Write** : La version 2026-09 de l'API CRM applique des règles de validation plus strictes pour les propriétés requises. Vérifier que les propriétés envoyées correspondent aux paramètres de création de contact. *(impact : alerte)*

## 5. Alertes pour l'équipe

- ⚠️ 2026-11-20 — Surveillance nécessaire : Les changements dans les API CRM et Pipelines pourraient affecter la migration des contacts en 2027.

## 6. Historique

| Version | Date | Déclencheur | Ce qui a changé |
|---|---|---|---|
| 2 | 2026-11-20 | nouveautés | rien à changer |
| 1 | 2026-11-17 | création | Reprise de pipeline/verification/mapping.py et de la leçon d'Alexis sur les e-mails en .example. |
