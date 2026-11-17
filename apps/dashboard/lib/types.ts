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
  /** Preuve visuelle (D14) : session de l'agent H et dernière capture d'écran de la fiche. */
  agent_session_id?: string | null;
  screenshot_url?: string | null;
  /** Relecture ciblée (D13) : le champ relu par l'agent, avant / après. */
  reread?: Reread | null;
  /** Durée réelle : lancement et horaires de l'agent. */
  run_id?: string;
  agent_started_at?: string | null;
  agent_finished_at?: string | null;
};

export type Reread = {
  field: string;
  before: string | null;
  after: string | null;
  error?: string | null;
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
