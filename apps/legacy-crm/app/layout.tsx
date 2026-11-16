import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Bascule — ancien CRM (simulé)",
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
      <body>{children}</body>
    </html>
  );
}
