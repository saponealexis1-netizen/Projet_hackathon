"use client";

import { useState } from "react";

/** Numéro caché derrière un bouton (obstacle volontaire pour l'agent). */
export default function PhoneReveal({ phone, label }: { phone: string | null; label: string }) {
  const [shown, setShown] = useState(false);
  return shown ? (
    <span>{phone ?? ""}</span>
  ) : (
    <button type="button" className="v2-btn" onClick={() => setShown(true)}>
      {label}
    </button>
  );
}
