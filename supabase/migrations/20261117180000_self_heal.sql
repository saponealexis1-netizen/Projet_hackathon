-- Fallback en direct (Inès, accord d'Alexis le 17/11) :
-- quand HubSpot refuse une fiche, les 2 IA corrigent le skill HubSpot et la fiche est renvoyée.
-- Le compte rendu de cette réparation est gardé ici, pour l'écran de suivi.
-- À lancer une seule fois : Supabase → SQL Editor → New query → coller → Run.
alter table public.migration_log
  add column if not exists self_heal jsonb;

comment on column public.migration_log.self_heal is
  'Réparation automatique : erreur HubSpot, résumé de la correction du skill, version du skill, résultat (envoyée / bloquée / non corrigée).';
