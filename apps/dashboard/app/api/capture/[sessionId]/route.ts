/**
 * GET /api/capture/[sessionId] — capture d'écran de la fiche vue par l'agent (preuve visuelle, D14).
 *
 * Les captures de l'Agent API H Company ne se téléchargent qu'avec la clé API : le navigateur
 * ne peut pas les afficher directement. Ce relais, CÔTÉ SERVEUR, ajoute la clé et renvoie l'image.
 * Sécurité : seules les captures enregistrées dans migration_log pour cette session sont servies,
 * et uniquement vers l'hôte de l'Agent API ; la clé n'arrive jamais dans le navigateur.
 */
import { fetchScreenshotUrl, isRunId, supabaseConfigured } from "@/lib/supabase";

export const dynamic = "force-dynamic";

const H_HOSTS = new Set(["agp.eu.hcompany.ai", "agp.hcompany.ai"]);

export async function GET(_request: Request, { params }: { params: Promise<{ sessionId: string }> }) {
  const { sessionId } = await params;
  const key = process.env.HAI_API_KEY;
  if (!isRunId(sessionId)) return new Response("Session invalide.", { status: 400 });
  if (!supabaseConfigured() || !key) return new Response("Captures non configurées.", { status: 503 });

  try {
    const shot = await fetchScreenshotUrl(sessionId);
    if (!shot || !H_HOSTS.has(new URL(shot).hostname)) return new Response("Pas de capture.", { status: 404 });

    const res = await fetch(shot, { headers: { Authorization: `Bearer ${key}` }, cache: "no-store" });
    if (!res.ok || !res.body) return new Response("Capture expirée ou inaccessible.", { status: 404 });
    return new Response(res.body, {
      headers: {
        "Content-Type": res.headers.get("content-type") ?? "image/png",
        "Cache-Control": "private, max-age=3600",
      },
    });
  } catch {
    return new Response("Capture inaccessible.", { status: 502 });
  }
}
