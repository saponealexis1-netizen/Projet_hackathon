import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: "CRM Agence 2010 — Gestion des contacts",
  description:
    "Ancien CRM simulé pour la démo Bascule : pas d'export, pas d'API.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="fr">
      <body>
        <div className="window">
          <div className="titlebar">
            <span>CRM Agence 2010 — version 3.1</span>
            <span className="titlebar-buttons" aria-hidden="true">
              <span>_</span>
              <span>□</span>
              <span>×</span>
            </span>
          </div>

          {/* Menu d'époque : seul « Contacts » fonctionne. Aucun export, volontairement. */}
          <nav className="menubar" aria-label="Menu principal">
            <span className="menu-disabled">Fichier</span>
            <Link href="/">Contacts</Link>
            <span className="menu-disabled">Agenda</span>
            <span className="menu-disabled">Outils</span>
            <span className="menu-disabled">Aide</span>
          </nav>

          <main className="content">{children}</main>

          <footer className="statusbar">
            <span>Utilisateur : accueil</span>
            <span>Base locale · installée le 12/03/2010</span>
          </footer>
        </div>
      </body>
    </html>
  );
}
