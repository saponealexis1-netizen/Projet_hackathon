/**
 * Lecture de migration_log via l'API REST de Supabase (aucune dépendance à installer).
 * CÔTÉ SERVEUR UNIQUEMENT : la clé service_role ne doit jamais arriver dans le navigateur.
 */
import type { LogRow } from "./types";

export function supabaseConfigured(): boolean {
  return Boolean(process.env.SUPABASE_URL && process.env.SUPABASE_SERVICE_ROLE_KEY);
}

export async function fetchRunRows(runId: string): Promise<LogRow[]> {
  const url = new URL("/rest/v1/migration_log", process.env.SUPABASE_URL);
  url.searchParams.set(
    "select",
    "legacy_id,status,extracted,anomalies,hubspot_id,duration_ms,credits_used,error,created_at",
  );
  url.searchParams.set("run_id", `eq.${runId}`);
  url.searchParams.set("order", "created_at.asc");

  const key = process.env.SUPABASE_SERVICE_ROLE_KEY!;
  const res = await fetch(url, {
    headers: { apikey: key, Authorization: `Bearer ${key}` },
    cache: "no-store",
  });
  if (!res.ok) throw new Error(`Supabase ${res.status} : ${await res.text()}`);
  return (await res.json()) as LogRow[];
}
