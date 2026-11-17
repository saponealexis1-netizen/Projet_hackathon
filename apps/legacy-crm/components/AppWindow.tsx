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

/** Fenêtre principale du logiciel : barre de titre, menus, contenu, barre d'état. */
export default function AppWindow({ children }: { children: React.ReactNode }) {
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
          <span>CRM Agence 2010 — version 3.1</span>
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
            <MenuBar />
            <main className="content">{children}</main>
            <footer className="statusbar">
              <span>Utilisateur : accueil</span>
              <span>Base locale · installée le 12/03/2010</span>
            </footer>
          </>
        )}
      </div>

      {minimized && (
        <div className="taskbar">
          <button type="button" className="taskbar-item" onClick={() => setMinimized(false)}>
            CRM Agence 2010
          </button>
        </div>
      )}

      {!motdClosed && (
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
          title="CRM Agence 2010"
          icon="❓"
          buttons={[
            {
              label: "Oui",
              onClick: () => {
                setClosing(false);
                router.push("/au-revoir");
              },
            },
            { label: "Non", onClick: () => setClosing(false) },
          ]}
        >
          Voulez-vous vraiment quitter CRM Agence 2010 ?
        </Dialog>
      )}
    </>
  );
}
