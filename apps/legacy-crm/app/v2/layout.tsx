import type { Metadata } from "next";
import AppWindow from "@/components/AppWindow";

export const metadata: Metadata = {
  title: "GestiContacts 2.4 — Répertoire clients",
  description:
    "2e version de l'ancien CRM simulé (autre mise en page, autres libellés) pour la démo Bascule.",
};

/**
 * Version 2 de l'ancien CRM (décision D12 de CADRAGE.md) : même base de contacts et même style
 * « logiciel à l'ancienne », mais d'autres adresses, d'autres libellés et une autre disposition.
 * L'agent doit savoir la lire sans qu'on change son code.
 */
export default function V2Layout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return <AppWindow variant="v2">{children}</AppWindow>;
}
