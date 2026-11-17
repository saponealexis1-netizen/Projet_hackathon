import { notFound } from "next/navigation";
import { connection } from "next/server";
import ContactForm from "@/components/ContactForm";
import { getContact } from "@/lib/contacts";

type Props = {
  params: Promise<{ id: string }>;
};

export default async function EditContactPage({ params }: Props) {
  await connection();

  const { id } = await params;
  const found = await getContact(id);
  if (!found) notFound();
  const c = found.contact;

  return (
    <>
      <h1>
        Modifier la fiche — {c.first_name} {c.last_name}
      </h1>
      <ContactForm contact={c} cancelHref={`/contacts/${c.legacy_id}`} />
    </>
  );
}
