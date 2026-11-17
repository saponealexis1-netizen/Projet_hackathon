"use client";

import { useState } from "react";
import Dialog from "./Dialog";

/** Options d'affichage et vérification des mises à jour (base en lecture seule). */
export default function OptionsForm() {
  const [dialog, setDialog] = useState<"saved" | "update" | null>(null);

  return (
    <>
      <form
        onSubmit={(e) => {
          e.preventDefault();
          setDialog("saved");
        }}
      >
        <fieldset>
          <legend>Affichage</legend>
          <table className="form">
            <tbody>
              <tr>
                <th scope="row">
                  <label htmlFor="per-page">Fiches par page :</label>
                </th>
                <td>
                  <select id="per-page" defaultValue="8">
                    <option>8</option>
                    <option>15</option>
                    <option>25</option>
                  </select>
                </td>
              </tr>
              <tr>
                <th scope="row">
                  <label htmlFor="sort">Tri par défaut :</label>
                </th>
                <td>
                  <select id="sort" defaultValue="fiche">
                    <option value="fiche">N° fiche</option>
                    <option value="nom">Nom</option>
                    <option value="ville">Ville</option>
                  </select>
                </td>
              </tr>
              <tr>
                <th scope="row">Démarrage :</th>
                <td>
                  <label>
                    <input type="checkbox" defaultChecked /> Ouvrir la liste des contacts
                  </label>
                </td>
              </tr>
            </tbody>
          </table>
        </fieldset>

        <div className="toolbar">
          <button type="submit">Enregistrer</button>
          <button type="button" onClick={() => setDialog("update")}>
            Vérifier les mises à jour
          </button>
        </div>
      </form>

      {dialog === "saved" && (
        <Dialog
          title="CRM Agence 2010 — Erreur"
          icon="⚠️"
          buttons={[{ label: "OK", onClick: () => setDialog(null) }]}
        >
          Impossible d&apos;enregistrer les options : la base est ouverte en <b>lecture seule</b>.
        </Dialog>
      )}
      {dialog === "update" && (
        <Dialog
          title="Mise à jour"
          buttons={[{ label: "OK", onClick: () => setDialog(null) }]}
        >
          <p style={{ margin: "0 0 6px" }}>Aucune mise à jour disponible.</p>
          <p style={{ margin: 0 }}>Le support de CRM Agence 2010 a pris fin le 31/12/2015.</p>
        </Dialog>
      )}
    </>
  );
}
