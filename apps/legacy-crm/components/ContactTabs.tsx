"use client";

import { useState } from "react";
import type { Contact } from "@/lib/contacts";

/** Libellés d'un champ, pour que la v1 et la v2 n'utilisent pas les mêmes mots (décision D12). */
export type Labels = {
  identityTab: string;
  contactTab: string;
  legacyId: string;
  firstName: string;
  lastName: string;
  company: string;
  jobTitle: string;
  notes: string;
  email: string;
  phone: string;
  city: string;
  showPhone: string;
};

export const V1_LABELS: Labels = {
  identityTab: "Identité",
  contactTab: "Coordonnées",
  legacyId: "N° client",
  firstName: "Prénom",
  lastName: "Nom",
  company: "Société",
  jobTitle: "Fonction",
  notes: "Commentaires",
  email: "E-mail",
  phone: "Téléphone",
  city: "Ville",
  showPhone: "Afficher le numéro",
};

/**
 * Fiche sur 2 onglets (obstacles volontaires pour l'agent, CADRAGE.md) :
 * - seul l'onglet actif est affiché : il faut cliquer sur « Coordonnées » pour voir e-mail, téléphone et ville ;
 * - le téléphone est caché derrière un bouton « Afficher le numéro ».
 * L'onglet et le numéro se referment quand on change de fiche.
 */
export default function ContactTabs({ contact: c, labels: l }: { contact: Contact; labels: Labels }) {
  const [tab, setTab] = useState<"identity" | "contact">("identity");
  const [phoneShown, setPhoneShown] = useState(false);

  const identity: [string, string | null][] = [
    [l.legacyId, c.legacy_id],
    [l.firstName, c.first_name],
    [l.lastName, c.last_name],
    [l.company, c.company],
    [l.jobTitle, c.job_title],
    [l.notes, c.notes],
  ];

  return (
    <fieldset>
      <legend>Informations du contact</legend>
      <div className="tabs">
      <div className="tab-list" role="tablist">
        <button
          type="button"
          role="tab"
          aria-selected={tab === "identity"}
          className={tab === "identity" ? "tab tab-active" : "tab"}
          onClick={() => setTab("identity")}
        >
          {l.identityTab}
        </button>
        <button
          type="button"
          role="tab"
          aria-selected={tab === "contact"}
          className={tab === "contact" ? "tab tab-active" : "tab"}
          onClick={() => setTab("contact")}
        >
          {l.contactTab}
        </button>
      </div>

      <div className="tab-panel" role="tabpanel">
        <table className="form">
          <tbody>
            {tab === "identity" ? (
              identity.map(([label, value]) => (
                <tr key={label}>
                  <th scope="row">{label} :</th>
                  <td>
                    <span className="field">{value ?? ""}</span>
                  </td>
                </tr>
              ))
            ) : (
              <>
                <tr>
                  <th scope="row">{l.email} :</th>
                  <td>
                    <span className="field">{c.email ?? ""}</span>
                  </td>
                </tr>
                <tr>
                  <th scope="row">{l.phone} :</th>
                  <td>
                    {phoneShown ? (
                      <span className="field">{c.phone ?? ""}</span>
                    ) : (
                      <button type="button" onClick={() => setPhoneShown(true)}>
                        {l.showPhone}
                      </button>
                    )}
                  </td>
                </tr>
                <tr>
                  <th scope="row">{l.city} :</th>
                  <td>
                    <span className="field">{c.city ?? ""}</span>
                  </td>
                </tr>
              </>
            )}
          </tbody>
        </table>
      </div>
      </div>
    </fieldset>
  );
}
