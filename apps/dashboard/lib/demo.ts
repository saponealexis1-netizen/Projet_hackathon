/**
 * MODE DÉMO : simule une migration quand Supabase / l'orchestration ne sont pas configurés.
 * Les fiches viennent de lib/demo-data.json (contacts d'exemple + cas pièges, passés par la
 * vraie vérification Python). Rien n'est stocké : l'heure de départ est encodée dans le run_id,
 * ce qui fonctionne aussi sur Vercel.
 */
import demoData from "./demo-data.json";
import type { LogRow } from "./types";

/** Délai simulé entre deux fiches (la vraie durée d'une fiche est ~48 s). */
export const DEMO_STEP_MS = 1200;

const DEMO_PREFIX = "demo-";

export function newDemoRunId(now = Date.now()): string {
  return `${DEMO_PREFIX}${now}`;
}

export function isDemoRunId(runId: string): boolean {
  return runId.startsWith(DEMO_PREFIX);
}

export const DEMO_TOTAL = demoData.length;

export function demoRows(runId: string, now = Date.now()): LogRow[] {
  const start = Number(runId.slice(DEMO_PREFIX.length));
  if (!Number.isFinite(start)) return [];
  const done = Math.min(DEMO_TOTAL, Math.max(0, Math.floor((now - start) / DEMO_STEP_MS)));
  return (demoData as Omit<LogRow, "hubspot_id" | "error" | "created_at">[])
    .slice(0, done)
    .map((r, i) => ({
      ...r,
      // Coût simulé = coût réel mesuré sur les 100 fiches de l'ancien CRM (~0,015 $ par fiche).
      credits_used: 0.015,
      anomalies: r.anomalies ?? [],
      hubspot_id: r.status === "success" || r.status === "partial" ? `demo-${1000 + i}` : null,
      error: null,
      created_at: new Date(start + (i + 1) * DEMO_STEP_MS).toISOString(),
    }));
}
