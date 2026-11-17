import Link from "next/link";

export default function V2NotFound() {
  return (
    <>
      <h1>Client introuvable</h1>
      <p>Aucun client ne correspond à cette référence.</p>
      <Link className="button" href="/v2">
        ‹ Revenir au répertoire
      </Link>
    </>
  );
}
