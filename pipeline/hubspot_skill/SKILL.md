# Skill HubSpot — Bascule

> **Version 2** du 2026-11-21 · IA n°1 Qwen/Qwen3-32B (proposition) + IA n°2 Qwen/Qwen3-Next-80B-A3B-Instruct (validation)
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

- 2026-09-15 — **Legacy APIs and Apps: What's Going Unsupported** : Fin du support des APIs v1-v3 et des apps legacy en septembre 2027. *(impact : alerte)*

## 5. Alertes pour l'équipe

- ⚠️ 2026-11-21 — Vérifier que Bascule utilise une version d'API CRM compatible avec les nouvelles règles de validation (2026-09+).

## 6. Historique

| Version | Date | Déclencheur | Ce qui a changé |
|---|---|---|---|
| 2 | 2026-11-21 | nouveautés | Rien à changer : les mises à jour HubSpot ne modifient pas les propriétés utilisées par Bascule ou les règles de validation actuelles. |
| 1 | 2026-11-17 | création | Reprise de pipeline/verification/mapping.py et de la leçon d'Alexis sur les e-mails en .example. |
