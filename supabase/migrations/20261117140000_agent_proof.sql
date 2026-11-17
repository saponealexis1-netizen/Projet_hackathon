-- Bascule — preuves de l'agent dans le journal (décisions D13 et D14).
-- Appliquée le 17/11/2026. Relançable sans risque.

alter table public.migration_log
  add column if not exists agent_session_id text,
  add column if not exists screenshot_url text,
  add column if not exists reread jsonb;

comment on column public.migration_log.agent_session_id is 'Session de l''agent H Company qui a lu la fiche (preuve, D14).';
comment on column public.migration_log.screenshot_url is 'Dernière capture d''écran de la fiche vue par l''agent (preuve visuelle, D14).';
comment on column public.migration_log.reread is 'Relecture ciblée (D13) : champ, valeur avant, valeur après.';
