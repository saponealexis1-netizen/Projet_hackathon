-- Bascule — tables Supabase (tâche alexis/supabase)
-- À lancer une seule fois dans Supabase : SQL Editor → New query → coller → Run.

-- ────────────────────────────────────────────────────────────────
-- 1. legacy_contacts : la base « cachée » de l'ancien CRM simulé.
--    Seule l'application de l'ancien CRM la lit (côté serveur).
--    L'agent H n'y a PAS accès : il doit passer par l'écran.
--    Colonnes = contrat shared/contact.schema.json.
-- ────────────────────────────────────────────────────────────────
create table if not exists public.legacy_contacts (
  legacy_id   text primary key check (legacy_id ~ '^C-[0-9]{4}$'),
  first_name  text not null check (length(first_name) > 0),
  last_name   text not null check (length(last_name) > 0),
  email       text,
  phone       text,
  company     text,
  job_title   text,
  city        text,
  notes       text,
  created_at  timestamptz not null default now()
);

comment on table public.legacy_contacts is
  'Base cachée de l''ancien CRM simulé. Format = shared/contact.schema.json. L''agent n''y accède pas directement.';

-- ────────────────────────────────────────────────────────────────
-- 2. migration_log : une ligne par fiche traitée lors d'une migration.
--    Sert aux mesures (taux de réussite, temps, coût) et à l'écran de suivi.
-- ────────────────────────────────────────────────────────────────
create table if not exists public.migration_log (
  id            bigint generated always as identity primary key,
  run_id        uuid not null,                       -- un lancement de migration = un run_id
  legacy_id     text not null,                       -- fiche source (C-0001…)
  status        text not null
                check (status in ('success', 'partial', 'failed', 'duplicate', 'skipped')),
  extracted     jsonb,                               -- contact tel que lu par l'agent (format du contrat)
  anomalies     jsonb not null default '[]'::jsonb,  -- liste des anomalies détectées par la vérification
  hubspot_id    text,                                -- identifiant du contact créé dans HubSpot
  duration_ms   integer check (duration_ms >= 0),    -- temps de traitement de la fiche
  credits_used  numeric check (credits_used >= 0),   -- crédits Agent API consommés
  error         text,                                -- message d'erreur éventuel
  created_at    timestamptz not null default now()
);

create index if not exists migration_log_run_id_idx    on public.migration_log (run_id);
create index if not exists migration_log_legacy_id_idx on public.migration_log (legacy_id);

comment on table public.migration_log is
  'Journal de migration : une ligne par fiche traitée. Alimente les mesures et l''écran de suivi.';

-- ────────────────────────────────────────────────────────────────
-- 3. Sécurité : RLS activée, AUCUNE politique publique.
--    → Les clés publiques (anon / publishable) ne voient rien.
--    → Seul le serveur, avec la clé service_role (ou secret), lit et écrit.
--    Cette clé reste dans .env.local et dans Vercel, jamais dans le navigateur.
-- ────────────────────────────────────────────────────────────────
alter table public.legacy_contacts enable row level security;
alter table public.migration_log   enable row level security;
