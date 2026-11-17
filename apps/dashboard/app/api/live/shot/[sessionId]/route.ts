/** GET /api/live/shot/[sessionId] — dernière capture d'écran d'un agent Bascule en train de travailler. */
import { fetchCapture, hConfigured, latestScreenshot } from "@/lib/hcompany";
import { isRunId } from "@/lib/supabase";

export const dynamic = "force-dynamic";

export async function GET(_request: Request, { params }: { params: Promise<{ sessionId: string }> }) {
  const { sessionId } = await params;
  if (!isRunId(sessionId)) return new Response("Session invalide.", { status: 400 });
  if (!hConfigured()) return new Response("HAI_API_KEY absente.", { status: 503 });
  try {
    const url = await latestScreenshot(sessionId);
    const img = url ? await fetchCapture(url) : null;
    if (!img) return new Response("Pas encore de capture.", { status: 404 });
    return new Response(img.body, {
      headers: { "Content-Type": img.headers.get("content-type") ?? "image/png", "Cache-Control": "no-store" },
    });
  } catch {
    return new Response("Capture inaccessible.", { status: 502 });
  }
}
