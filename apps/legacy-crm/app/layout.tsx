import type { Metadata } from "next";
import AppWindow from "@/components/AppWindow";
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
        <AppWindow>{children}</AppWindow>
      </body>
    </html>
  );
}
