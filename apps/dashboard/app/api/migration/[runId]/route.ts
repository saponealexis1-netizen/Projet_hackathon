/**
 * GET /api/migration/[runId]?total=20 — état d'une migration, interrogé toutes les 2 s par l'écran.
 * Lit migration_log dans Supabase (ou la simulation en mode démo).
 */
import { DEMO_TOTAL, demoRows, isDemoRunId } from "@/lib/demo";
import { fetchRunRows, supabaseConfigured } from "@/lib/supabase";
import type { RunState } from "@/lib/types";

export const dynamic = "force-dynamic";

export async function GET(request: Request, { params }: { params: Promise<{ runId: string }> }) {
  const { runId } = await params;
  const hubspotContactUrl = process.env.HUBSPOT_CONTACT_URL || null;

  if (isDemoRunId(runId)) {
    const state: RunState = { runId, mode: "demo", total: DEMO_TOTAL, rows: demoRows(runId), hubspotContactUrl: null };
    return Response.json(state);
  }

  if (!supabaseConfigured()) {
    return Response.json({ error: "Supabase n'est pas configuré." }, { status: 500 });
  }

  const totalParam = Number(new URL(request.url).searchParams.get("total"));
  const total = totalParam > 0 ? totalParam : Number(process.env.MIGRATION_TOTAL ?? 20);
  try {
    const rows = await fetchRunRows(runId);
    const state: RunState = { runId, mode: "live", total, rows, hubspotContactUrl };
    return Response.json(state);
  } catch (e) {
    return Response.json({ error: (e as Error).message }, { status: 502 });
  }
}
