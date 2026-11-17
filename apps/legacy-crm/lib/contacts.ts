/**
 * Données de l'ancien CRM simulé.
 *
 * - Si SUPABASE_URL et SUPABASE_SERVICE_ROLE_KEY sont définies : lecture de la table
 *   `legacy_contacts` via l'API REST de Supabase (aucune dépendance à installer).
 * - Sinon : lecture du fichier de secours `contacts.fallback.json`
 *   (copie de data/contacts.legacy.json : les mêmes 100 contacts, plan B de la décision D5 de CADRAGE.md).
 *
 * CÔTÉ SERVEUR UNIQUEMENT : la clé service_role ne doit jamais arriver dans le navigateur.
 * L'agent H n'a pas accès à ces données : il ne voit que les pages HTML.
 */
import fallback from "./contacts.fallback.json";

/** Format du contrat commun shared/contact.schema.json. */
export type Contact = {
  legacy_id: string;
  first_name: string;
  last_name: string;
  email: string | null;
  phone: string | null;
  company: string | null;
  job_title: string | null;
  city: string | null;
  notes: string | null;
};

export const PAGE_SIZE = 10;

function supabaseConfigured(): boolean {
  return Boolean(process.env.SUPABASE_URL && process.env.SUPABASE_SERVICE_ROLE_KEY);
}

export function dataSource(): "supabase" | "fichier de secours" {
  return supabaseConfigured() ? "supabase" : "fichier de secours";
}

// Schéma Postgres de nos tables (« hackathon », pour ne pas les mélanger avec d'autres projets).
const SCHEMA = process.env.SUPABASE_SCHEMA || "hackathon";

async function fetchFromSupabase(): Promise<Contact[]> {
  const url = new URL("/rest/v1/legacy_contacts", process.env.SUPABASE_URL);
  url.searchParams.set(
    "select",
    "legacy_id,first_name,last_name,email,phone,company,job_title,city,notes",
  );
  url.searchParams.set("order", "legacy_id.asc");

  const key = process.env.SUPABASE_SERVICE_ROLE_KEY!;
  // Les nouvelles clés Supabase (sb_secret_…) ne sont pas des JWT : elles passent seulement dans « apikey ».
  const headers: Record<string, string> = key.startsWith("sb_")
    ? { apikey: key, "Accept-Profile": SCHEMA }
    : { apikey: key, Authorization: `Bearer ${key}`, "Accept-Profile": SCHEMA };
  const res = await fetch(url, { headers, cache: "no-store" });
  if (!res.ok) throw new Error(`Supabase ${res.status} : ${await res.text()}`);
  return (await res.json()) as Contact[];
}

function fromFallback(): Contact[] {
  return [...(fallback as Contact[])].sort((a, b) => a.legacy_id.localeCompare(b.legacy_id));
}

/**
 * Tous les contacts, triés par numéro de fiche.
 * Si Supabase est configuré mais ne répond pas (adresse ou clé fausse, réseau),
 * on bascule sur le fichier de secours au lieu de casser la page pendant la démo.
 */
export async function getContacts(): Promise<Contact[]> {
  if (!supabaseConfigured()) return fromFallback();
  try {
    return await fetchFromSupabase();
  } catch (error) {
    console.error("[legacy-crm] Supabase indisponible, fichier de secours utilisé :", error);
    return fromFallback();
  }
}

/** Une fiche, avec la précédente et la suivante pour la navigation. */
export async function getContact(legacyId: string) {
  const all = await getContacts();
  const index = all.findIndex((c) => c.legacy_id === legacyId);
  if (index === -1) return null;
  return {
    contact: all[index],
    previousId: index > 0 ? all[index - 1].legacy_id : null,
    nextId: index < all.length - 1 ? all[index + 1].legacy_id : null,
    position: index + 1,
    total: all.length,
  };
}
