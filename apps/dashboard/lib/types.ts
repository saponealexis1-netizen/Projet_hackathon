/** Une ligne de la table Supabase migration_log (voir supabase/migrations/). */
export type LogStatus = "success" | "partial" | "failed" | "duplicate" | "skipped";

export type Anomaly = {
  field: string | null;
  code: string;
  severity: "warning" | "error";
  message: string;
};

export type LogRow = {
  legacy_id: string;
  status: LogStatus;
  extracted: Record<string, string | null> | null;
  anomalies: Anomaly[];
  hubspot_id: string | null;
  duration_ms: number | null;
  credits_used: number | null;
  error: string | null;
  created_at: string;
  run_id?: string;
  agent_started_at?: string | null;
  agent_finished_at?: string | null;
};

/** Statut affiché à Thomas sur l'écran de suivi. */
export type UiStatus = "ok" | "a_verifier" | "bloquee" | "ignoree";

/** Réponse de GET /api/migration/[runId]. */
export type RunState = {
  runId: string;
  mode: "demo" | "live";
  total: number;
  rows: LogRow[];
  hubspotContactUrl: string | null;
};
