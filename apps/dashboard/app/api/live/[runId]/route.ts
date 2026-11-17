/** GET /api/live/[runId] — agents H en train de travailler pour ce lancement (panneau « Agents en direct »). */
import { hConfigured, liveAgents } from "@/lib/hcompany";
import { isRunId } from "@/lib/supabase";

export const dynamic = "force-dynamic";

export async function GET(_request: Request, { params }: { params: Promise<{ runId: string }> }) {
  const { runId } = await params;
  if (!isRunId(runId)) return Response.json({ agents: [] });
  if (!hConfigured()) return Response.json({ agents: [], error: "HAI_API_KEY absente" });
  try {
    return Response.json({ agents: await liveAgents(runId) });
  } catch (e) {
    return Response.json({ agents: [], error: (e as Error).message }, { status: 502 });
  }
}
