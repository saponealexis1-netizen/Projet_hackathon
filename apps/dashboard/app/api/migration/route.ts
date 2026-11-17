/**
 * POST /api/migration — appelé par le bouton « Lancer la migration ».
 *
 * 1. Si GITHUB_DISPATCH_TOKEN est défini : lance le VRAI agent via l'action GitHub
 *    « Lancer la migration » (.github/workflows/migration.yml), avec un run_id créé ici.
 *    L'écran suit ensuite ce run_id : les fiches arrivent une par une dans migration_log.
 *    Garde-fou : refuse si des agents H travaillent déjà (crédits, démo).
 * 2. Sinon, si ORCHESTRATOR_URL est défini : appelle cette orchestration HTTP.
 * 3. Sinon : MODE DÉMO (migration simulée).
 *
 * Réponse : { runId, mode, total }
 */
import { randomUUID } from "node:crypto";
import { DEMO_TOTAL, newDemoRunId } from "@/lib/demo";
import { basculeBusy, hConfigured } from "@/lib/hcompany";
import { supabaseConfigured } from "@/lib/supabase";

export const dynamic = "force-dynamic";

const REPO = process.env.GITHUB_REPOSITORY ?? "saponealexis1-netizen/Projet_hackathon";
const WORKFLOW = "migration.yml";
// Fiches de la démo : une fiche normale + les 5 pièges (doublon, e-mail invalide, prénom vide, téléphone, majuscules)
const DEMO_IDS = process.env.DEMO_IDS ?? "C-0004,C-0101,C-0102,C-0103,C-0104,C-0105";
const LEGACY_URL = process.env.LEGACY_CRM_URL ?? "https://projet-hackathon-uffi.vercel.app";

export async function POST() {
  const token = process.env.GITHUB_DISPATCH_TOKEN;

  if (token && supabaseConfigured()) {
    if (hConfigured() && (await basculeBusy())) {
      return Response.json({ error: "Des agents travaillent déjà : attendez la fin de la migration en cours." }, { status: 409 });
    }
    const runId = randomUUID();
    const res = await fetch(`https://api.github.com/repos/${REPO}/actions/workflows/${WORKFLOW}/dispatches`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        Accept: "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
      },
      body: JSON.stringify({ ref: "main", inputs: { run_id: runId, ids: DEMO_IDS, url: LEGACY_URL } }),
      cache: "no-store",
    });
    if (!res.ok) {
      return Response.json(
        { error: `Impossible de lancer l'agent (GitHub ${res.status}).` },
        { status: 502 },
      );
    }
    return Response.json({ runId, mode: "live", total: DEMO_IDS.split(",").length });
  }

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

/** GET /api/migration — l'écran demande si le bouton peut lancer le VRAI agent. */
export async function GET() {
  return Response.json({ live: Boolean(process.env.GITHUB_DISPATCH_TOKEN) && supabaseConfigured() });
}
