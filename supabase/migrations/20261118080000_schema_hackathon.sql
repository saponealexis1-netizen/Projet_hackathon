-- Bascule — nos tables passent dans le schéma « hackathon », pour ne pas les mélanger
-- avec les tables d'un autre projet présentes dans « public ».
-- Les données, index, contraintes, RLS et droits suivent la table.
-- Appliquée le 17/11/2026 au soir.
-- PRÉREQUIS : ajouter « hackathon » dans Supabase › Project Settings › Data API › Exposed schemas.
-- Le code envoie l'en-tête Accept-Profile / Content-Profile: hackathon (variable SUPABASE_SCHEMA).

create schema if not exists hackathon;
grant usage on schema hackathon to service_role;

alter table public.legacy_contacts set schema hackathon;
alter table public.migration_log set schema hackathon;

grant select on hackathon.legacy_contacts to service_role;
grant select, insert on hackathon.migration_log to service_role;
grant usage, select on all sequences in schema hackathon to service_role;

-- TEMPORAIRE : vues de compatibilité pour les sites pas encore redéployés (lisent encore « public »).
-- security_invoker : la RLS des tables s'applique ; aucun droit pour anon / authenticated.
-- À supprimer après le Redeploy de jow2 et uffi :
--   drop view public.legacy_contacts; drop view public.migration_log;
create view public.legacy_contacts with (security_invoker = true) as select * from hackathon.legacy_contacts;
create view public.migration_log with (security_invoker = true) as select * from hackathon.migration_log;
revoke all on public.legacy_contacts, public.migration_log from anon, authenticated, public;
grant select on public.legacy_contacts to service_role;
grant select, insert on public.migration_log to service_role;
