import Link from "next/link";

export default function GoodbyePage() {
  return (
    <>
      <h1>Session terminée</h1>
      <p>CRM Agence 2010 a été fermé. Les données n&apos;ont pas été modifiées.</p>
      <Link className="button" href="/">
        Relancer CRM Agence 2010
      </Link>
    </>
  );
}
