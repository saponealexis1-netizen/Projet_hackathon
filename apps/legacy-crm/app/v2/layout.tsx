import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "GestiContacts Web — Répertoire clients",
  description:
    "2e version de l'ancien CRM simulé (autre mise en page, autres libellés) pour la démo Bascule.",
};

/**
 * Version 2 de l'ancien CRM (décision D12 de CADRAGE.md) : même base de contacts,
 * mais une autre mise en page, d'autres adresses et d'autres libellés.
 * L'agent doit savoir la lire sans qu'on change son code.
 */
export default function V2Layout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <div className="v2">
      <header className="v2-header">
        <div className="v2-logo">
          GestiContacts <span>Web</span>
        </div>
        <div className="v2-user">Connecté : poste-accueil · Déconnexion</div>
      </header>
      <div className="v2-body">
        <aside className="v2-side">
          <div className="v2-side-title">Navigation</div>
          <Link href="/v2">Répertoire clients</Link>
          <span className="v2-off">Relances</span>
          <span className="v2-off">Statistiques</span>
          <span className="v2-off">Paramétrage</span>
        </aside>
        <main className="v2-main">{children}</main>
      </div>
      <footer className="v2-footer">GestiContacts Web 2.4 — © 2008 — Aucune exportation disponible avec cette licence</footer>
    </div>
  );
}
