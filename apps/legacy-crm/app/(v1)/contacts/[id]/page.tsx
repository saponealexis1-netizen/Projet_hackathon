import Link from "next/link";
import { notFound } from "next/navigation";
import { connection } from "next/server";
import ContactTabs, { V1_LABELS } from "@/components/ContactTabs";
import PrintButton from "@/components/PrintButton";
import { getContact, PAGE_SIZE } from "@/lib/contacts";

type Props = {
  params: Promise<{ id: string }>;
};

/**
 * Fiche d'un contact, sur 2 onglets (« Identité » / « Coordonnées »), téléphone derrière un bouton.
 * L'agent H lit cette page à l'écran : libellés stables, une valeur vide reste vide.
 */
export default async function ContactPage({ params }: Props) {
  await connection();

  const { id } = await params;
  const found = await getContact(id);
  if (!found) notFound();

  const { contact: c, previousId, nextId, position, total } = found;
  const listPage = Math.ceil(position / PAGE_SIZE);

  return (
    <>
      <h1>
        Fiche contact — {c.first_name} {c.last_name}
      </h1>

      <div className="toolbar">
        <Link className="button" href={listPage > 1 ? `/?page=${listPage}` : "/"}>
          ◄ Retour à la liste
        </Link>
        <Link className="button" href={`/contacts/${c.legacy_id}/modifier`}>
          Modifier
        </Link>
        <PrintButton />
        <span>
          Fiche {position} sur {total}
        </span>
      </div>

      {/* key : l'onglet et le numéro se referment quand on change de fiche */}
      <ContactTabs key={c.legacy_id} contact={c} labels={V1_LABELS} />

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
