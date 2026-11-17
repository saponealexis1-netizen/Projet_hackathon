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
  /** Durée réelle (horloge) : du premier agent démarré au dernier terminé, additionnée par lancement. */
  dureeReelleMs: number | null;
  dureeMoyenneMs: number | null;
  creditsTotal: number;
  creditsParFiche: number | null;
  anomaliesParType: { code: string; label: string; count: number }[];
  relues: number; // D13 : fiches dont un champ a été relu par l'agent
  corrigeesParRelecture: number; // … et dont la valeur a changé après relecture
  avecPreuve: number; // D14 : fiches avec une capture d'écran
};

/** Libellés français des champs du contrat commun. */
export const FIELD_LABEL: Record<string, string> = {
  legacy_id: "Identifiant",
  first_name: "Prénom",
  last_name: "Nom",
  email: "E-mail",
  phone: "Téléphone",
  company: "Entreprise",
  job_title: "Poste",
  city: "Ville",
  notes: "Notes",
};

/** Une relecture a-t-elle corrigé la valeur ? */
export function rereadChanged(row: LogRow): boolean {
  const r = row.reread;
  return Boolean(r && !r.error && (r.after ?? "") !== (r.before ?? ""));
}

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
  const dureeReelleMs = dureeReelle(rows);
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
    dureeReelleMs,
    dureeMoyenneMs: traitees ? Math.round(dureeTotaleMs / traitees) : null,
    creditsTotal,
    creditsParFiche: traitees ? Math.round((creditsTotal / traitees) * 10000) / 10000 : null,
    anomaliesParType: [...parCode.entries()]
      .map(([code, n]) => ({ code, label: CODE_LABEL[code] ?? code, count: n }))
      .sort((a, b) => b.count - a.count),
    relues: rows.filter((r) => r.reread).length,
    corrigeesParRelecture: rows.filter(rereadChanged).length,
    avecPreuve: rows.filter((r) => r.screenshot_url).length,
  };
}

/**
 * Les agents travaillent en parallèle : la durée réelle n'est pas la somme de leurs temps.
 * Pour chaque lancement : dernière fin − premier début. Les lancements sont additionnés
 * (ex. 97 fiches puis 3 relancées). null si les horaires ne sont pas connus.
 */
function dureeReelle(rows: LogRow[]): number | null {
  const parRun = new Map<string, { debut: number; fin: number }>();
  for (const r of rows) {
    if (!r.agent_started_at || !r.agent_finished_at) continue;
    const debut = Date.parse(r.agent_started_at);
    const fin = Date.parse(r.agent_finished_at);
    const key = r.run_id ?? "run";
    const cur = parRun.get(key);
    parRun.set(key, cur ? { debut: Math.min(cur.debut, debut), fin: Math.max(cur.fin, fin) } : { debut, fin });
  }
  if (parRun.size === 0) return null;
  return [...parRun.values()].reduce((s, p) => s + (p.fin - p.debut), 0);
}

export function formatDuree(ms: number | null): string {
  if (ms === null) return "—";
  const s = Math.round(ms / 1000);
  if (s < 60) return `${s} s`;
  const m = Math.floor(s / 60);
  return `${m} min ${String(s % 60).padStart(2, "0")} s`;
}
