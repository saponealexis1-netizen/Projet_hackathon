"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import Dialog from "./Dialog";
import MenuBar from "./MenuBar";

/** Fenêtre principale du logiciel : barre de titre, menus, contenu, barre d'état. */
export default function AppWindow({ children }: { children: React.ReactNode }) {
  const [minimized, setMinimized] = useState(false);
  const [maximized, setMaximized] = useState(false);
  const [closing, setClosing] = useState(false);
  const router = useRouter();

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
