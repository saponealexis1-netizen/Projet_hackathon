"use client";

import { useRouter } from "next/navigation";
import { useState, useSyncExternalStore } from "react";
import Dialog from "./Dialog";
import MenuBar from "./MenuBar";

const MOTD_KEY = "motd-ferme";
function subscribeMotd(callback: () => void) {
  window.addEventListener(MOTD_KEY, callback);
  return () => window.removeEventListener(MOTD_KEY, callback);
}

const VERSIONS = {
  v1: {
    appName: "CRM Agence 2010",
    title: "CRM Agence 2010 — version 3.1",
    status: ["Utilisateur : accueil", "Base locale · installée le 12/03/2010"],
    motd: true,
  },
  v2: {
    appName: "GestiContacts",
    title: "GestiContacts 2.4 — Répertoire clients",
    status: ["Poste : accueil-02", "Licence consultation · © 2008"],
    motd: false,
  },
} as const;

/** Fenêtre principale du logiciel : barre de titre, menus, contenu, barre d'état. */
export default function AppWindow({
  children,
  variant = "v1",
}: {
  children: React.ReactNode;
  variant?: "v1" | "v2";
}) {
  const v = VERSIONS[variant];
  const [minimized, setMinimized] = useState(false);
  const [maximized, setMaximized] = useState(false);
  const [closing, setClosing] = useState(false);
  const router = useRouter();

  // « Message du jour » : s'affiche à l'arrivée sur le site, une fois par session (obstacle volontaire pour l'agent).
  const motdClosed = useSyncExternalStore(
    subscribeMotd,
    () => sessionStorage.getItem(MOTD_KEY) === "1",
    () => true, // côté serveur : pas de fenêtre
  );
  const closeMotd = () => {
    sessionStorage.setItem(MOTD_KEY, "1");
    window.dispatchEvent(new Event(MOTD_KEY));
  };

  return (
    <>
      <div className={`window${maximized ? " window-max" : ""}`}>
        <div className="titlebar" onDoubleClick={() => setMaximized(!maximized)}>
          <span>{v.title}</span>
          <span className="titlebar-buttons">
            <button type="button" aria-label="Réduire" title="Réduire" onClick={() => setMinimized(true)}>
              _
            </button>
            <button
              type="button"
              aria-label={maximized ? "Restaurer" : "Agrandir"}
              title={maximized ? "Restaurer" : "Agrandir"}
              onClick={() => setMaximized(!maximized)}
            >
              □
            </button>
            <button type="button" aria-label="Fermer" title="Fermer" onClick={() => setClosing(true)}>
              ×
            </button>
          </span>
        </div>

        {!minimized && (
          <>
            <MenuBar variant={variant} appName={v.appName} />
            <main className="content">{children}</main>
            <footer className="statusbar">
              <span>{v.status[0]}</span>
              <span>{v.status[1]}</span>
            </footer>
          </>
        )}
      </div>

      {minimized && (
        <div className="taskbar">
          <button type="button" className="taskbar-item" onClick={() => setMinimized(false)}>
            {v.appName}
          </button>
        </div>
      )}

      {v.motd && !motdClosed && (
        <Dialog title="Message du jour" icon="💡" buttons={[{ label: "Fermer", onClick: closeMotd }]}>
          <p style={{ margin: "0 0 6px" }}>
            <b>Le saviez-vous ?</b> Vous pouvez parcourir vos fiches une à une avec les boutons
            « Fiche précédente » et « Fiche suivante ».
          </p>
          <p style={{ margin: 0 }}>Rappel : la sauvegarde hebdomadaire de la base est prévue vendredi à 18h.</p>
        </Dialog>
      )}

      {closing && (
        <Dialog
          title={v.appName}
          icon="❓"
          buttons={[
            {
              label: "Oui",
              onClick: () => {
                setClosing(false);
                router.push(variant === "v2" ? "/v2/au-revoir" : "/au-revoir");
              },
            },
            { label: "Non", onClick: () => setClosing(false) },
          ]}
        >
          Voulez-vous vraiment quitter {v.appName} ?
        </Dialog>
      )}
    </>
  );
}
