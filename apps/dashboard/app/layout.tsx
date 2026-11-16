import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Bascule — suivi de migration",
  description: "Lancement, suivi en direct et bilan de la migration de l'ancien CRM vers HubSpot.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="fr">
      <body>{children}</body>
    </html>
  );
}
