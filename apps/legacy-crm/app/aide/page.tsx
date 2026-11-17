export default function HelpPage() {
  return (
    <>
      <h1>Aide de CRM Agence 2010</h1>

      <fieldset>
        <legend>Sommaire</legend>
        <ol className="help">
          <li>
            <b>Consulter la liste des contacts</b> : menu <i>Contacts › Liste des contacts</i>. Utilisez
            « Page suivante » et « Page précédente » pour parcourir la base.
          </li>
          <li>
            <b>Ouvrir une fiche</b> : cliquez sur « Ouvrir la fiche » sur la ligne du contact.
          </li>
          <li>
            <b>Créer ou modifier un contact</b> : boutons « Nouveau contact » et « Modifier ».
            Nécessite une licence « Édition ».
          </li>
          <li>
            <b>Imprimer</b> : menu <i>Fichier › Imprimer…</i> ou bouton « Imprimer ».
          </li>
          <li>
            <b>Agenda</b> : menu <i>Agenda › Agenda du mois</i>. Cliquez sur un rendez-vous pour ouvrir la
            fiche du contact.
          </li>
        </ol>
      </fieldset>

      <fieldset>
        <legend>Questions fréquentes</legend>
        <p className="help">
          <b>Comment exporter mes contacts vers un autre logiciel ?</b>
          <br />
          Cette fonction n&apos;est pas disponible dans votre version de CRM Agence 2010.
        </p>
        <p className="help">
          <b>Comment contacter le support ?</b>
          <br />
          Le support éditeur a pris fin le 31/12/2015.
        </p>
      </fieldset>

      <fieldset id="a-propos">
        <legend>À propos</legend>
        <p className="help">
          <b>CRM Agence 2010</b> — version 3.1 (build 2010.03)
          <br />
          Licence : Consultation (lecture seule)
          <br />
          © 2010. Tous droits réservés.
        </p>
        <p className="help" style={{ color: "#555" }}>
          Logiciel fictif, créé pour la démonstration du projet Bascule.
        </p>
      </fieldset>
    </>
  );
}
