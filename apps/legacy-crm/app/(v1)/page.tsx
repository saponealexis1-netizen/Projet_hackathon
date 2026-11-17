import Link from "next/link";
import { connection } from "next/server";
import PrintButton from "@/components/PrintButton";
import { getContacts, PAGE_SIZE } from "@/lib/contacts";

type Props = {
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>;
};

/** Liste paginée des contacts. Aucun bouton d'export : c'est tout l'enjeu de la démo. */
export default async function ContactList({ searchParams }: Props) {
  await connection(); // toujours lire les données à jour, jamais une page figée

  const contacts = await getContacts();
  const pageCount = Math.max(1, Math.ceil(contacts.length / PAGE_SIZE));
  const raw = Number((await searchParams).page);
  const page = Number.isInteger(raw) && raw >= 1 && raw <= pageCount ? raw : 1;
  const rows = contacts.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE);

  return (
    <>
      <h1>Contacts</h1>

      <div className="toolbar">
        <Link className="button" href="/contacts/nouveau">
          Nouveau contact
        </Link>
        <PrintButton />
        <span>
          {contacts.length} contacts au total
        </span>
      </div>

      <table className="grid">
        <thead>
          <tr>
            <th scope="col">N° client</th>
            <th scope="col">Nom</th>
            <th scope="col">Prénom</th>
            <th scope="col">Société</th>
            <th scope="col">Ville</th>
            <th scope="col">Action</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((c) => (
            <tr key={c.legacy_id}>
              <td>{c.legacy_id}</td>
              <td>{c.last_name}</td>
              <td>{c.first_name}</td>
              <td>{c.company ?? ""}</td>
              <td>{c.city ?? ""}</td>
              <td>
                <Link href={`/contacts/${c.legacy_id}`}>Voir la fiche</Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <nav className="pagination" aria-label="Pagination">
        {page > 1 ? (
          <Link className="button" href={`/?page=${page - 1}`}>
            ◄ Page précédente
          </Link>
        ) : (
          <span className="button" aria-disabled="true">
            ◄ Page précédente
          </span>
        )}
        <span>
          Page {page} / {pageCount}
        </span>
        {page < pageCount ? (
          <Link className="button" href={`/?page=${page + 1}`}>
            Page suivante ►
          </Link>
        ) : (
          <span className="button" aria-disabled="true">
            Page suivante ►
          </span>
        )}
      </nav>
    </>
  );
}
