import Link from "next/link";

export default function V2GoodbyePage() {
  return (
    <>
      <h1>Session terminée</h1>
      <p>GestiContacts a été fermé. Les données n&apos;ont pas été modifiées.</p>
      <Link className="button" href="/v2">
        Relancer GestiContacts
      </Link>
    </>
  );
}
