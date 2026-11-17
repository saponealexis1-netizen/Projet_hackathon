/**
 * Lecture de migration_log via l'API REST de Supabase (aucune dépendance à installer).
 * CÔTÉ SERVEUR UNIQUEMENT : la clé service_role ne doit jamais arriver dans le navigateur.
 */
import type { LogRow } from "./types";

export function supabaseConfigured(): boolean {
  return Boolean(process.env.SUPABASE_URL && process.env.SUPABASE_SERVICE_ROLE_KEY);
}

const COLUMNS =
  "legacy_id,status,extracted,anomalies,hubspot_id,duration_ms,credits_used,error,created_at," +
  "run_id,agent_started_at,agent_finished_at";
const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

export function isRunId(value: string): boolean {
  return UUID.test(value);
}

async function query(params: Record<string, string>): Promise<LogRow[]> {
  const url = new URL("/rest/v1/migration_log", process.env.SUPABASE_URL);
  url.searchParams.set("select", COLUMNS);
  for (const [k, v] of Object.entries(params)) url.searchParams.set(k, v);

  const key = process.env.SUPABASE_SERVICE_ROLE_KEY!;
  // Les nouvelles clés Supabase (sb_secret_…) ne sont pas des JWT : seulement dans « apikey ».
  const headers: Record<string, string> = key.startsWith("sb_")
    ? { apikey: key }
    : { apikey: key, Authorization: `Bearer ${key}` };
  const res = await fetch(url, { headers, cache: "no-store" });
  if (!res.ok) throw new Error(`Supabase ${res.status} : ${await res.text()}`);
  return (await res.json()) as LogRow[];
}

/** Les fiches d'un lancement précis. */
export async function fetchRunRows(runId: string): Promise<LogRow[]> {
  if (!isRunId(runId)) throw new Error("Identifiant de migration invalide.");
  return query({ run_id: `eq.${runId}`, order: "created_at.asc" });
}

/**
 * Vue « tout » : l'état de chaque fiche migrée, tous lancements confondus
 * (la lecture la plus récente de chaque fiche, triée par numéro de fiche).
 */
export async function fetchLatestPerRecord(): Promise<LogRow[]> {
  const rows = await query({ order: "created_at.desc", limit: "5000" });
  const latest = new Map<string, LogRow>();
  for (const r of rows) if (!latest.has(r.legacy_id)) latest.set(r.legacy_id, r);
  return [...latest.values()].sort((a, b) => a.legacy_id.localeCompare(b.legacy_id));
}
