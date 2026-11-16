/**
 * POST /api/migration — appelé par le bouton « Lancer la migration ».
 *
 * - Si ORCHESTRATOR_URL est défini : crée un run_id et demande à l'orchestration (Victoria)
 *   de lancer la migration. L'orchestration écrit ensuite une ligne par fiche dans migration_log.
 * - Sinon : MODE DÉMO (migration simulée).
 *
 * Réponse : { runId, mode, total }
 */
import { randomUUID } from "node:crypto";
import { DEMO_TOTAL, newDemoRunId } from "@/lib/demo";
import { supabaseConfigured } from "@/lib/supabase";

export const dynamic = "force-dynamic";

export async function POST() {
  const orchestrator = process.env.ORCHESTRATOR_URL;

  if (!orchestrator || !supabaseConfigured()) {
    return Response.json({ runId: newDemoRunId(), mode: "demo", total: DEMO_TOTAL });
  }

  const runId = randomUUID();
  try {
    const res = await fetch(orchestrator, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ run_id: runId }),
      cache: "no-store",
    });
    if (!res.ok) throw new Error(`orchestration : HTTP ${res.status}`);
    const body = (await res.json().catch(() => ({}))) as { total?: number };
    const total = body.total ?? Number(process.env.MIGRATION_TOTAL ?? 20);
    return Response.json({ runId, mode: "live", total });
  } catch (e) {
    return Response.json(
      { error: `Impossible de lancer la migration (${(e as Error).message}).` },
      { status: 502 },
    );
  }
}
