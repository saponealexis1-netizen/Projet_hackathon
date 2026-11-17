-- Bascule — nos tables passent dans le schéma « hackathon », pour ne pas les mélanger
-- avec les tables d'un autre projet présentes dans « public ».
-- Les données, index, contraintes, RLS et droits suivent la table.
-- PRÉREQUIS : ajouter « hackathon » dans Supabase › Project Settings › Data API › Exposed schemas.
-- Le code envoie l'en-tête Accept-Profile / Content-Profile: hackathon (variable SUPABASE_SCHEMA).

create schema if not exists hackathon;
grant usage on schema hackathon to service_role;

alter table public.legacy_contacts set schema hackathon;
alter table public.migration_log set schema hackathon;

grant select on hackathon.legacy_contacts to service_role;
grant select, insert on hackathon.migration_log to service_role;
grant usage, select on all sequences in schema hackathon to service_role;
