# Skill HubSpot — Bascule

> **Version 1** du 2026-11-17 · Inès (version de départ, écrite à la main)
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

- Aucune pour l'instant.

## 5. Alertes pour l'équipe

- ⚠️ 2026-11-23 — [nouveautés] proposition non appliquée : analyste : IA n°1 (Qwen/Qwen3-32B) : HTTP 429 {"error":{"message":"Provider returned error","code":429,"metadata":{"raw":"qwen/qwen3-32b is temporarily rate-limited upstream. Please retry shortly, or add your own provider key to use your own limits: https://openrouter.ai/workspaces/prod/byok","provider_name":"DeepInfra","is_byok":false,"provide

## 6. Historique

| Version | Date | Déclencheur | Ce qui a changé |
|---|---|---|---|
| 1 | 2026-11-17 | création | Reprise de pipeline/verification/mapping.py et de la leçon d'Alexis sur les e-mails en .example. |
