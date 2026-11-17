import Link from "next/link";

/** Adresse inconnue (en dehors des deux versions du CRM). */
export default function NotFound() {
  return (
    <main style={{ padding: 24, background: "#d4d0c8", maxWidth: 600, margin: "40px auto" }}>
      <h1>Page introuvable</h1>
      <p>Cette adresse n&apos;existe pas.</p>
      <Link className="button" href="/">
        ◄ Retour à la liste
      </Link>
    </main>
  );
}
