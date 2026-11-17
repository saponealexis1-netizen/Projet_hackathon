import Link from "next/link";
import { notFound } from "next/navigation";
import { connection } from "next/server";
import PhoneReveal from "@/components/PhoneReveal";
import PrintButton from "@/components/PrintButton";
import { getContact, PAGE_SIZE } from "@/lib/contacts";

type Props = {
  params: Promise<{ ref: string }>;
};

/**
 * Fiche client de la v2 : deux encadrés côte à côte (pas d'onglets),
 * libellés différents de la v1 (« Raison sociale », « Tél. », « Courriel »…), téléphone derrière un bouton.
 */
export default async function V2Fiche({ params }: Props) {
  await connection();

  const { ref } = await params;
  const found = await getContact(ref);
  if (!found) notFound();

  const { contact: c, previousId, nextId, position, total } = found;
  const listPage = Math.ceil(position / PAGE_SIZE);

  const society: [string, string | null][] = [
    ["Réf.", c.legacy_id],
    ["Raison sociale", c.company],
    ["Nom de famille", c.last_name],
    ["Prénom", c.first_name],
    ["Poste occupé", c.job_title],
  ];

  return (
    <>
      <h1>
        Client {c.last_name.toUpperCase()} {c.first_name}
      </h1>

      <div className="toolbar">
        <Link className="button" href={listPage > 1 ? `/v2?p=${listPage}` : "/v2"}>
          ‹ Revenir au répertoire
        </Link>
        <PrintButton />
        <span>
          Enregistrement {position} / {total}
        </span>
      </div>

      <div className="two-columns">
        <fieldset>
          <legend>Société</legend>
          <table className="form form-compact">
            <tbody>
              {society.map(([label, value]) => (
                <tr key={label}>
                  <th scope="row">{label} :</th>
                  <td>
                    <span className="field field-compact">{value ?? ""}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </fieldset>

        <fieldset>
          <legend>Joindre le client</legend>
          <table className="form form-compact">
            <tbody>
              <tr>
                <th scope="row">Courriel :</th>
                <td>
                  <span className="field field-compact">{c.email ?? ""}</span>
                </td>
              </tr>
              <tr>
                <th scope="row">Tél. :</th>
                <td>
                  <PhoneReveal key={c.legacy_id} phone={c.phone} label="Voir le tél." />
                </td>
              </tr>
              <tr>
                <th scope="row">Localité :</th>
                <td>
                  <span className="field field-compact">{c.city ?? ""}</span>
                </td>
              </tr>
              <tr>
                <th scope="row">Observations :</th>
                <td>
                  <span className="field field-compact">{c.notes ?? ""}</span>
                </td>
              </tr>
            </tbody>
          </table>
        </fieldset>
      </div>

      <nav className="pagination" aria-label="Clients voisins">
        {previousId ? (
          <Link className="button" href={`/v2/fiche/${previousId}`}>
            ‹ Client précédent
          </Link>
        ) : (
          <span className="button" aria-disabled="true">
            ‹ Client précédent
          </span>
        )}
        {nextId ? (
          <Link className="button" href={`/v2/fiche/${nextId}`}>
            Client suivant ›
          </Link>
        ) : (
          <span className="button" aria-disabled="true">
            Client suivant ›
          </span>
        )}
      </nav>
    </>
  );
}
