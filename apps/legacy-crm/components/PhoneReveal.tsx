"use client";

import { useState } from "react";

/** Numéro caché derrière un bouton (obstacle volontaire pour l'agent). */
export default function PhoneReveal({ phone, label }: { phone: string | null; label: string }) {
  const [shown, setShown] = useState(false);
  return shown ? (
    <span className="field field-compact">{phone ?? ""}</span>
  ) : (
    <button type="button" onClick={() => setShown(true)}>
      {label}
    </button>
  );
}
