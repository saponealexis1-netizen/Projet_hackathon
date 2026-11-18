/**
 * Accès à l'Agent API H Company, CÔTÉ SERVEUR UNIQUEMENT (clé HAI_API_KEY).
 * Sert au panneau « Agents en direct » : quels agents travaillent, et leur dernière capture.
 */
import type { LiveAgent } from "./types";

const API = process.env.HAI_API_URL ?? "https://agp.eu.hcompany.ai/api/v2";

export function hConfigured(): boolean {
  return Boolean(process.env.HAI_API_KEY);
}

async function h(path: string): Promise<Response> {
  return fetch(API + path, {
    headers: { Authorization: `Bearer ${process.env.HAI_API_KEY}` },
    cache: "no-store",
  });
}

// Le groupe est dans « request » (détail d'une session) ; la consigne est dans « first_message » (liste).
type HSession = {
  id: string;
  status: unknown;
  group_id?: string | null;
  request?: { group_id?: string | null } | null;
  first_message?: unknown;
  objective?: string | null;
};

function statusOf(s: HSession): string {
  return typeof s.status === "string" ? s.status : ((s.status as { status?: string })?.status ?? "inconnu");
}

/** Agents en cours d'un lancement (sessions du groupe « bascule-<runId> »). */
export async function liveAgents(runId: string): Promise<LiveAgent[]> {
  const params = new URLSearchParams({ group_id: `bascule-${runId}`, size: "20" });
  const res = await h(`/sessions?${params}`);
  if (!res.ok) throw new Error(`H Company ${res.status}`);
  const body = (await res.json()) as { items?: HSession[] };
  return (body.items ?? [])
    .map((s) => ({
      sessionId: s.id,
      legacyId: JSON.stringify(s.first_message ?? s.objective ?? "").match(/\b(C-\d{4})\b/)?.[1] ?? null,
      status: statusOf(s),
    }))
    .filter((a) => ["pending", "queued", "running"].includes(a.status));
}

/** Vrai si un agent travaille déjà sur le compte H (évite deux migrations en même temps). */
export async function basculeBusy(): Promise<boolean> {
  const res = await h("/sessions?size=20");
  if (!res.ok) return false;
  const body = (await res.json()) as { items?: HSession[] };
  // La liste ne donne pas le groupe : tout agent en cours sur le compte H de Bascule compte.
  return (body.items ?? []).some((s) => ["pending", "queued", "running"].includes(statusOf(s)));
}

/** Adresse de la dernière capture d'une session Bascule (null si aucune, ou si la session n'est pas à Bascule). */
export async function latestScreenshot(sessionId: string): Promise<string | null> {
  const s = await h(`/sessions/${sessionId}`);
  if (!s.ok) return null;
  const session = (await s.json()) as HSession;
  const group = session.request?.group_id ?? session.group_id;
  if (!group?.startsWith("bascule-")) return null; // seulement nos agents
  // Les captures sont dans les « observation_event » ; les derniers événements peuvent être d'autres types.
  const params = new URLSearchParams({ sort: "-timestamp", type: "AgentEvent", size: "30" });
  const ev = await h(`/sessions/${sessionId}/events?${params}`);
  if (!ev.ok) return null;
  const body = (await ev.json()) as { items?: { data?: { image?: { source?: string } } }[] };
  return body.items?.find((e) => e.data?.image?.source)?.data?.image?.source ?? null;
}

/** Télécharge une capture H (la clé est ajoutée ici, jamais envoyée au navigateur). */
export async function fetchCapture(url: string): Promise<Response | null> {
  const host = new URL(url).hostname;
  if (host !== "agp.eu.hcompany.ai" && host !== "agp.hcompany.ai") return null;
  const res = await fetch(url, { headers: { Authorization: `Bearer ${process.env.HAI_API_KEY}` }, cache: "no-store" });
  return res.ok && res.body ? res : null;
}
