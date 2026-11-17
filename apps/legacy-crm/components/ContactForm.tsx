"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import type { Contact } from "@/lib/contacts";
import Dialog from "./Dialog";

const FIELDS: { key: keyof Contact; label: string; multiline?: boolean }[] = [
  { key: "legacy_id", label: "N° fiche" },
  { key: "first_name", label: "Prénom" },
  { key: "last_name", label: "Nom" },
  { key: "company", label: "Société" },
  { key: "job_title", label: "Fonction" },
  { key: "phone", label: "Téléphone" },
  { key: "email", label: "E-mail" },
  { key: "city", label: "Ville" },
  { key: "notes", label: "Notes", multiline: true },
];

/**
 * Formulaire de saisie d'un contact. La base de démo est en lecture seule :
 * « Enregistrer » affiche le message d'erreur du logiciel, rien n'est modifié.
 */
export default function ContactForm({
  contact,
  cancelHref,
}: {
  contact?: Contact;
  cancelHref: string;
}) {
  const router = useRouter();
  const [blocked, setBlocked] = useState(false);

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        setBlocked(true);
      }}
    >
      <fieldset>
        <legend>Informations du contact</legend>
        <table className="form">
          <tbody>
            {FIELDS.map(({ key, label, multiline }) => (
              <tr key={key}>
                <th scope="row">
                  <label htmlFor={key}>{label} :</label>
                </th>
                <td>
                  {multiline ? (
                    <textarea id={key} name={key} rows={3} defaultValue={contact?.[key] ?? ""} />
                  ) : (
                    <input
                      id={key}
                      name={key}
                      defaultValue={contact?.[key] ?? ""}
                      readOnly={key === "legacy_id"}
                      placeholder={key === "legacy_id" && !contact ? "Attribué automatiquement" : undefined}
                    />
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </fieldset>

      <div className="toolbar">
        <button type="submit">Enregistrer</button>
        <button type="button" onClick={() => router.push(cancelHref)}>
          Annuler
        </button>
      </div>

      {blocked && (
        <Dialog
          title="CRM Agence 2010 — Erreur"
          icon="⚠️"
          buttons={[{ label: "OK", onClick: () => setBlocked(false) }]}
        >
          <p style={{ margin: "0 0 6px" }}>
            Impossible d&apos;enregistrer : la base est ouverte en <b>lecture seule</b>.
          </p>
          <p style={{ margin: 0 }}>
            Licence « Consultation » (code erreur 0x80040E09). Contactez votre administrateur.
          </p>
        </Dialog>
      )}
    </form>
  );
}
