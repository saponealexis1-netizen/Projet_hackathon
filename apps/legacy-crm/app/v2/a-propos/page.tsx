import Link from "next/link";

export default function V2AboutPage() {
  return (
    <>
      <h1>À propos de GestiContacts</h1>
      <fieldset>
        <legend>GestiContacts</legend>
        <p className="help">
          <b>GestiContacts</b> — version 2.4
          <br />
          Licence : consultation · aucune exportation disponible
          <br />
          © 2008. Tous droits réservés.
        </p>
        <p className="help" style={{ color: "#555" }}>
          Logiciel fictif, créé pour la démonstration du projet Bascule.
        </p>
      </fieldset>
      <Link className="button" href="/v2">
        ‹ Revenir au répertoire
      </Link>
    </>
  );
}
