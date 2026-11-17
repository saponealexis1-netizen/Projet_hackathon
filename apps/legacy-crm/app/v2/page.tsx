import Link from "next/link";
import { connection } from "next/server";
import { getContacts, PAGE_SIZE } from "@/lib/contacts";

type Props = {
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>;
};

/** Répertoire clients de la v2 : autres colonnes, autre ordre, pagination numérotée. */
export default async function V2List({ searchParams }: Props) {
  await connection();

  const contacts = await getContacts();
  const pageCount = Math.max(1, Math.ceil(contacts.length / PAGE_SIZE));
  const raw = Number((await searchParams).p);
  const page = Number.isInteger(raw) && raw >= 1 && raw <= pageCount ? raw : 1;
  const rows = contacts.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE);

  return (
    <>
      <h2 className="v2-title">Répertoire clients</h2>
      <p className="v2-count">
        {contacts.length} enregistrements · affichage {(page - 1) * PAGE_SIZE + 1} à{" "}
        {(page - 1) * PAGE_SIZE + rows.length}
      </p>

      <table className="v2-table">
        <thead>
          <tr>
            <th scope="col">Raison sociale</th>
            <th scope="col">Nom de famille</th>
            <th scope="col">Prénom</th>
            <th scope="col">Localité</th>
            <th scope="col">Réf.</th>
            <th scope="col" />
          </tr>
        </thead>
        <tbody>
          {rows.map((c) => (
            <tr key={c.legacy_id}>
              <td>{c.company ?? ""}</td>
              <td>{c.last_name}</td>
              <td>{c.first_name}</td>
              <td>{c.city ?? ""}</td>
              <td>{c.legacy_id}</td>
              <td>
                <Link href={`/v2/fiche/${c.legacy_id}`}>Détail ›</Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <nav className="v2-pages" aria-label="Pages">
        {page > 1 ? <Link href={`/v2?p=${page - 1}`}>« Préc.</Link> : <span className="v2-off">« Préc.</span>}
        {Array.from({ length: pageCount }, (_, i) => i + 1).map((n) =>
          n === page ? (
            <b key={n} aria-current="page">
              {n}
            </b>
          ) : (
            <Link key={n} href={`/v2?p=${n}`}>
              {n}
            </Link>
          ),
        )}
        {page < pageCount ? <Link href={`/v2?p=${page + 1}`}>Suiv. »</Link> : <span className="v2-off">Suiv. »</span>}
      </nav>
    </>
  );
}
