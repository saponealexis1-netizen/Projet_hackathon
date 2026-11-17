import type { Metadata } from "next";
import AppWindow from "@/components/AppWindow";

export const metadata: Metadata = {
  title: "CRM Agence 2010 — Gestion des contacts",
  description:
    "Ancien CRM simulé pour la démo Bascule : pas d'export, pas d'API.",
};

export default function V1Layout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return <AppWindow>{children}</AppWindow>;
}
