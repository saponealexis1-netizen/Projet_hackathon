/**
 * Données de l'ancien CRM simulé.
 *
 * - Si SUPABASE_URL et SUPABASE_SERVICE_ROLE_KEY sont définies : lecture de la table
 *   `legacy_contacts` via l'API REST de Supabase (aucune dépendance à installer).
 * - Sinon : lecture du fichier de secours `contacts.fallback.json`
 *   (copie de data/contacts.sample.json, plan B prévu par la décision D5 de CADRAGE.md).
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

export const PAGE_SIZE = 8;

function supabaseConfigured(): boolean {
  return Boolean(process.env.SUPABASE_URL && process.env.SUPABASE_SERVICE_ROLE_KEY);
}

export function dataSource(): "supabase" | "fichier de secours" {
  return supabaseConfigured() ? "supabase" : "fichier de secours";
}

async function fetchFromSupabase(): Promise<Contact[]> {
  const url = new URL("/rest/v1/legacy_contacts", process.env.SUPABASE_URL);
  url.searchParams.set(
    "select",
    "legacy_id,first_name,last_name,email,phone,company,job_title,city,notes",
  );
  url.searchParams.set("order", "legacy_id.asc");

  const key = process.env.SUPABASE_SERVICE_ROLE_KEY!;
  const res = await fetch(url, {
    headers: { apikey: key, Authorization: `Bearer ${key}` },
    cache: "no-store",
  });
  if (!res.ok) throw new Error(`Supabase ${res.status} : ${await res.text()}`);
  return (await res.json()) as Contact[];
}

/** Tous les contacts, triés par numéro de fiche. */
export async function getContacts(): Promise<Contact[]> {
  if (supabaseConfigured()) return fetchFromSupabase();
  return [...(fallback as Contact[])].sort((a, b) => a.legacy_id.localeCompare(b.legacy_id));
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
