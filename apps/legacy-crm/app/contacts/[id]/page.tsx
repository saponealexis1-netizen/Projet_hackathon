import Link from "next/link";
import { notFound } from "next/navigation";
import { connection } from "next/server";
import { getContact, PAGE_SIZE } from "@/lib/contacts";

type Props = {
  params: Promise<{ id: string }>;
};

/**
 * Fiche d'un contact. L'agent H lit cette page à l'écran :
 * chaque champ a un libellé visible et stable, une valeur vide reste vide.
 */
export default async function ContactPage({ params }: Props) {
  await connection();

  const { id } = await params;
  const found = await getContact(id);
  if (!found) notFound();

  const { contact: c, previousId, nextId, position, total } = found;
  const listPage = Math.ceil(position / PAGE_SIZE);

  const fields: [string, string | null][] = [
    ["N° fiche", c.legacy_id],
    ["Prénom", c.first_name],
    ["Nom", c.last_name],
    ["Société", c.company],
    ["Fonction", c.job_title],
    ["Téléphone", c.phone],
    ["E-mail", c.email],
    ["Ville", c.city],
    ["Notes", c.notes],
  ];

  return (
    <>
      <h1>
        Fiche contact — {c.first_name} {c.last_name}
      </h1>

      <div className="toolbar">
        <Link className="button" href={listPage > 1 ? `/?page=${listPage}` : "/"}>
          ◄ Retour à la liste
        </Link>
        <span className="button" aria-disabled="true">
          Modifier
        </span>
        <span className="button" aria-disabled="true">
          Imprimer
        </span>
        <span>
          Fiche {position} sur {total}
        </span>
      </div>

      <fieldset>
        <legend>Informations du contact</legend>
        <table className="form">
          <tbody>
            {fields.map(([label, value]) => (
              <tr key={label}>
                <th scope="row">{label} :</th>
                <td>
                  <span className="field">{value ?? ""}</span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </fieldset>

      <nav className="pagination" aria-label="Navigation entre les fiches">
        {previousId ? (
          <Link className="button" href={`/contacts/${previousId}`}>
            ◄ Fiche précédente
          </Link>
        ) : (
          <span className="button" aria-disabled="true">
            ◄ Fiche précédente
          </span>
        )}
        {nextId ? (
          <Link className="button" href={`/contacts/${nextId}`}>
            Fiche suivante ►
          </Link>
        ) : (
          <span className="button" aria-disabled="true">
            Fiche suivante ►
          </span>
        )}
      </nav>
    </>
  );
}
