import Link from "next/link";

export default function NotFound() {
  return (
    <>
      <h1>Fiche introuvable</h1>
      <p>Cette fiche n&apos;existe pas ou a été supprimée.</p>
      <Link className="button" href="/">
        ◄ Retour à la liste
      </Link>
    </>
  );
}
