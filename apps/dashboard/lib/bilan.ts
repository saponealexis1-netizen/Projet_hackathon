import type { LogRow, LogStatus, UiStatus } from "./types";

/**
 * Correspondance statut du journal → statut affiché.
 * Décisions D9 et D10 (docs/CADRAGE.md) :
 *  - « à vérifier » (partial) : envoyée dans HubSpot, anomalie affichée ;
 *  - « bloquée » (failed, duplicate) : non envoyée, affichée avec sa raison, pas corrigeable ici.
 */
export const UI_STATUS: Record<LogStatus, UiStatus> = {
  success: "ok",
  partial: "a_verifier",
  failed: "bloquee",
  duplicate: "bloquee",
  skipped: "ignoree",
};

export const UI_LABEL: Record<UiStatus, string> = {
  ok: "Migrée",
  a_verifier: "À vérifier",
  bloquee: "Bloquée",
  ignoree: "Ignorée",
};

/** Raison lisible d'une fiche : seulement les erreurs s'il y en a, sinon les avertissements. */
export function reason(row: LogRow): string {
  if (row.error) return row.error;
  const anomalies = row.anomalies ?? [];
  const errors = anomalies.filter((a) => a.severity === "error");
  return (errors.length ? errors : anomalies).map((a) => a.message).join(" · ");
}

export type Bilan = {
  total: number;
  traitees: number;
  terminee: boolean;
  migrees: number; // ok + à vérifier = envoyées dans HubSpot
  ok: number;
  aVerifier: number;
  bloquees: number;
  ignorees: number;
  tauxReussite: number | null; // migrées / traitées, en %
  dureeTotaleMs: number;
  dureeMoyenneMs: number | null;
  creditsTotal: number;
  creditsParFiche: number | null;
  anomaliesParType: { code: string; label: string; count: number }[];
};

const CODE_LABEL: Record<string, string> = {
  missing_required: "Champ obligatoire vide",
  bad_legacy_id: "Identifiant invalide",
  bad_email: "E-mail invalide",
  duplicate_id: "Doublon (identifiant)",
  duplicate_email: "Doublon (e-mail)",
  duplicate_person: "Doublon (même personne)",
  duplicate_phone: "Doublon (téléphone)",
  missing_email: "E-mail absent",
  bad_phone: "Téléphone non reconnu",
  case_fixed: "Majuscules corrigées",
  missing_optional: "Entreprise ou ville vide",
  unknown_field: "Champ inconnu ignoré",
};

export function computeBilan(rows: LogRow[], total: number): Bilan {
  const count = (s: UiStatus) => rows.filter((r) => UI_STATUS[r.status] === s).length;
  const ok = count("ok");
  const aVerifier = count("a_verifier");
  const bloquees = count("bloquee");
  const ignorees = count("ignoree");
  const traitees = rows.length;
  const migrees = ok + aVerifier;

  const dureeTotaleMs = rows.reduce((s, r) => s + (r.duration_ms ?? 0), 0);
  const creditsTotal = rows.reduce((s, r) => s + Number(r.credits_used ?? 0), 0);

  const parCode = new Map<string, number>();
  for (const r of rows) for (const a of r.anomalies ?? []) parCode.set(a.code, (parCode.get(a.code) ?? 0) + 1);

  return {
    total,
    traitees,
    terminee: total > 0 && traitees >= total,
    migrees,
    ok,
    aVerifier,
    bloquees,
    ignorees,
    tauxReussite: traitees ? Math.round((migrees / traitees) * 100) : null,
    dureeTotaleMs,
    dureeMoyenneMs: traitees ? Math.round(dureeTotaleMs / traitees) : null,
    creditsTotal,
    creditsParFiche: traitees ? Math.round((creditsTotal / traitees) * 10000) / 10000 : null,
    anomaliesParType: [...parCode.entries()]
      .map(([code, n]) => ({ code, label: CODE_LABEL[code] ?? code, count: n }))
      .sort((a, b) => b.count - a.count),
  };
}

export function formatDuree(ms: number | null): string {
  if (ms === null) return "—";
  const s = Math.round(ms / 1000);
  if (s < 60) return `${s} s`;
  const m = Math.floor(s / 60);
  return `${m} min ${String(s % 60).padStart(2, "0")} s`;
}
