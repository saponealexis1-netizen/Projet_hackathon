-- Bascule — droits du rôle serveur (service_role) sur nos tables.
-- Appliquée le 17/11/2026. Sur les projets Supabase récents, les tables créées par script
-- n'accordent plus automatiquement ces droits : sans eux, l'API répond « permission denied » (42501).
-- La clé publique (anon) reste SANS accès ; la RLS reste activée.

grant select on public.legacy_contacts to service_role;
grant select, insert on public.migration_log to service_role;
grant usage, select on all sequences in schema public to service_role;
