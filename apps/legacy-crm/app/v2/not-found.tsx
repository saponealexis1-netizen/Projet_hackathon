import Link from "next/link";

export default function V2NotFound() {
  return (
    <>
      <h2 className="v2-title">Client introuvable</h2>
      <p>Aucun client ne correspond à cette référence.</p>
      <Link href="/v2">‹ Revenir au répertoire</Link>
    </>
  );
}
