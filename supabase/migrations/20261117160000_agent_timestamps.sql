-- Bascule — début et fin de chaque session d'agent (appliquée le 17/11/2026).
-- Durée réelle d'une migration = max(agent_finished_at) - min(agent_started_at), lancement par lancement.

alter table public.migration_log
  add column if not exists agent_started_at timestamptz,
  add column if not exists agent_finished_at timestamptz;
