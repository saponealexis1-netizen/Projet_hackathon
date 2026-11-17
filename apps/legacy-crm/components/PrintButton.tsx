"use client";

export default function PrintButton() {
  return (
    <button type="button" className="button" onClick={() => window.print()}>
      Imprimer
    </button>
  );
}
