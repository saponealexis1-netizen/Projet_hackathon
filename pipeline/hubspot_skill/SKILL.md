# Skill HubSpot — Bascule

> **Version 2** du 2026-11-26 · IA n°1 Qwen/Qwen3-32B (proposition) + IA n°2 Qwen/Qwen3-Next-80B-A3B-Instruct (validation)
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

- 2026-08-11 — **Breaking Change: CRM API Write Validation Enforcement** : Validation des propriétés requises lors de l'écriture via l'API CRM (version 2026-09+). *(impact : alerte)*
- 2026-08-14 — **Pipelines API V1 Sunset** : API Pipelines V1 déconseillée, migration vers 2026-03+ requise d'ici décembre 2026. *(impact : alerte)*

## 5. Alertes pour l'équipe

- ⚠️ 2026-11-26 — Vérifier la compatibilité avec la version API CRM 2026-09+ (validation des propriétés requises).

## 6. Historique

| Version | Date | Déclencheur | Ce qui a changé |
|---|---|---|---|
| 2 | 2026-11-26 | nouveautés | Rien à changer |
| 1 | 2026-11-17 | création | Reprise de pipeline/verification/mapping.py et de la leçon d'Alexis sur les e-mails en .example. |
