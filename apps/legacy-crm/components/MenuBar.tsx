"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useRef, useState } from "react";
import Dialog from "./Dialog";

type Item =
  | { label: string; href: string }
  | { label: string; action: "print" | "quit" }
  | { separator: true };

/** Menus d'époque. Volontairement : aucune entrée « Exporter ». */
const MENUS: { label: string; items: Item[] }[] = [
  {
    label: "Fichier",
    items: [
      { label: "Nouveau contact", href: "/contacts/nouveau" },
      { label: "Imprimer…", action: "print" },
      { separator: true },
      { label: "Quitter", action: "quit" },
    ],
  },
  {
    label: "Contacts",
    items: [
      { label: "Liste des contacts", href: "/" },
      { label: "Nouveau contact", href: "/contacts/nouveau" },
    ],
  },
  {
    label: "Agenda",
    items: [{ label: "Agenda du mois", href: "/agenda" }],
  },
  {
    label: "Outils",
    items: [
      { label: "Options…", href: "/outils" },
      { label: "Informations sur la base", href: "/outils#base" },
    ],
  },
  {
    label: "Aide",
    items: [
      { label: "Sommaire de l'aide", href: "/aide" },
      { separator: true },
      { label: "À propos de CRM Agence 2010", href: "/aide#a-propos" },
    ],
  },
];

export default function MenuBar() {
  const [open, setOpen] = useState<string | null>(null);
  const [quitting, setQuitting] = useState(false);
  const ref = useRef<HTMLElement>(null);
  const router = useRouter();

  // Ferme le menu ouvert quand on clique ailleurs.
  useEffect(() => {
    const close = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(null);
    };
    document.addEventListener("mousedown", close);
    return () => document.removeEventListener("mousedown", close);
  }, []);

  return (
    <>
      <nav className="menubar" aria-label="Menu principal" ref={ref}>
        {MENUS.map((menu) => (
          <div key={menu.label} className="menu">
            <button
              type="button"
              className={`menu-title${open === menu.label ? " menu-open" : ""}`}
              aria-haspopup="true"
              aria-expanded={open === menu.label}
              onClick={() => setOpen(open === menu.label ? null : menu.label)}
              onMouseEnter={() => open && setOpen(menu.label)}
            >
              {menu.label}
            </button>
            {open === menu.label && (
              <div className="menu-dropdown" role="menu">
                {menu.items.map((item, i) =>
                  "separator" in item ? (
                    <hr key={i} />
                  ) : "href" in item ? (
                    <Link key={item.label} href={item.href} role="menuitem" onClick={() => setOpen(null)}>
                      {item.label}
                    </Link>
                  ) : (
                    <button
                      key={item.label}
                      type="button"
                      role="menuitem"
                      onClick={() => {
                        setOpen(null);
                        if (item.action === "print") window.print();
                        else setQuitting(true);
                      }}
                    >
                      {item.label}
                    </button>
                  ),
                )}
              </div>
            )}
          </div>
        ))}
      </nav>

      {quitting && (
        <Dialog
          title="CRM Agence 2010"
          icon="❓"
          buttons={[
            {
              label: "Oui",
              onClick: () => {
                setQuitting(false);
                router.push("/au-revoir");
              },
            },
            { label: "Non", onClick: () => setQuitting(false) },
          ]}
        >
          Voulez-vous vraiment quitter CRM Agence 2010 ?
        </Dialog>
      )}
    </>
  );
}
