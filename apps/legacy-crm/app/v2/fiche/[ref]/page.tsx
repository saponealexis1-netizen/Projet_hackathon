import Link from "next/link";
import { notFound } from "next/navigation";
import { connection } from "next/server";
import PhoneReveal from "@/components/PhoneReveal";
import { getContact, PAGE_SIZE } from "@/lib/contacts";

type Props = {
  params: Promise<{ ref: string }>;
};

/**
 * Fiche client de la v2 : une seule page en deux colonnes (pas d'onglets),
 * libellés différents de la v1 (« Raison sociale », « Tél. », « Courriel »…), téléphone derrière un bouton.
 */
export default async function V2Fiche({ params }: Props) {
  await connection();

  const { ref } = await params;
  const found = await getContact(ref);
  if (!found) notFound();

  const { contact: c, previousId, nextId, position } = found;
  const listPage = Math.ceil(position / PAGE_SIZE);

  const left: [string, string | null][] = [
    ["Réf.", c.legacy_id],
    ["Nom de famille", c.last_name],
    ["Prénom", c.first_name],
    ["Raison sociale", c.company],
    ["Poste occupé", c.job_title],
  ];

  return (
    <>
      <p className="v2-crumbs">
        <Link href={listPage > 1 ? `/v2?p=${listPage}` : "/v2"}>‹ Revenir au répertoire</Link>
      </p>
      <h2 className="v2-title">
        {c.last_name.toUpperCase()} {c.first_name}
      </h2>

      <div className="v2-card">
        <dl className="v2-dl">
          {left.map(([label, value]) => (
            <div key={label}>
              <dt>{label}</dt>
              <dd>{value ?? ""}</dd>
            </div>
          ))}
        </dl>
        <dl className="v2-dl">
          <div>
            <dt>Courriel</dt>
            <dd>{c.email ?? ""}</dd>
          </div>
          <div>
            <dt>Tél.</dt>
            <dd>
              <PhoneReveal key={c.legacy_id} phone={c.phone} label="Voir le tél." />
            </dd>
          </div>
          <div>
            <dt>Localité</dt>
            <dd>{c.city ?? ""}</dd>
          </div>
          <div>
            <dt>Observations</dt>
            <dd>{c.notes ?? ""}</dd>
          </div>
        </dl>
      </div>

      <nav className="v2-pages" aria-label="Clients voisins">
        {previousId ? (
          <Link href={`/v2/fiche/${previousId}`}>‹ Client précédent</Link>
        ) : (
          <span className="v2-off">‹ Client précédent</span>
        )}
        {nextId ? (
          <Link href={`/v2/fiche/${nextId}`}>Client suivant ›</Link>
        ) : (
          <span className="v2-off">Client suivant ›</span>
        )}
      </nav>
    </>
  );
}
