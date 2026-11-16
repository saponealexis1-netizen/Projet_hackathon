"use client";

import { useEffect, useState } from "react";
import { UI_LABEL, UI_STATUS, computeBilan, formatDuree, reason } from "@/lib/bilan";
import type { LogRow, RunState } from "@/lib/types";

type Run = { runId: string; mode: "demo" | "live"; total: number };

const POLL_MS = 2000;

export default function SuiviMigration() {
  const [run, setRun] = useState<Run | null>(null);
  const [state, setState] = useState<RunState | null>(null);
  const [launching, setLaunching] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const rows = state?.rows ?? [];
  const total = state?.total ?? run?.total ?? 0;
  const bilan = computeBilan(rows, total);
  const running = run !== null && !bilan.terminee;

  async function lancer() {
    setLaunching(true);
    setError(null);
    setState(null);
    try {
      const res = await fetch("/api/migration", { method: "POST" });
      const body = await res.json();
      if (!res.ok) throw new Error(body.error ?? `HTTP ${res.status}`);
      setRun(body as Run);
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setLaunching(false);
    }
  }

  // Interroge l'état de la migration toutes les 2 s tant qu'elle n'est pas terminée.
  useEffect(() => {
    if (!run) return;
    let stop = false;
    const tick = async () => {
      try {
        const res = await fetch(`/api/migration/${run.runId}?total=${run.total}`, { cache: "no-store" });
        const body = await res.json();
        if (!res.ok) throw new Error(body.error ?? `HTTP ${res.status}`);
        if (stop) return;
        setState(body as RunState);
        if ((body as RunState).rows.length >= (body as RunState).total) stop = true;
      } catch (e) {
        if (!stop) setError((e as Error).message);
      }
    };
    tick();
    const id = setInterval(() => !stop && tick(), POLL_MS);
    return () => {
      stop = true;
      clearInterval(id);
    };
  }, [run]);

  const progress = total ? Math.round((bilan.traitees / total) * 100) : 0;
  const bloquees = rows.filter((r) => UI_STATUS[r.status] === "bloquee");

  return (
    <main className="page">
      <header className="header">
        <div>
          <h1>Bascule</h1>
          <p className="subtitle">Ancien CRM → agent H Company → vérification → HubSpot</p>
        </div>
        {run?.mode === "demo" && <span className="badge-demo">Mode démo : données simulées</span>}
      </header>

      {/* ───────── 1. Lancement ───────── */}
      <section className="card launch">
        <div>
          <h2>Migration des contacts</h2>
          <p className="muted">
            L&apos;agent ouvre chaque fiche de l&apos;ancien CRM, comme un humain. Chaque fiche est vérifiée
            avant d&apos;être envoyée dans HubSpot.
          </p>
        </div>
        <button className="btn" onClick={lancer} disabled={launching || running}>
          {launching ? "Lancement…" : running ? "Migration en cours…" : run ? "Relancer la migration" : "Lancer la migration"}
        </button>
      </section>

      {error && <p className="alert">⚠️ {error}</p>}

      {run && (
        <>
          {/* ───────── 2. Suivi en direct ───────── */}
          <section className="card">
            <div className="progress-head">
              <h2>Suivi en direct</h2>
              <span className="muted">
                {bilan.traitees} / {total} fiches traitées
              </span>
            </div>
            <div className="progress" aria-label={`${progress} %`}>
              <div className="progress-bar" style={{ width: `${progress}%` }} />
            </div>
            <div className="counters">
              <Counter label="Migrées" value={bilan.ok} tone="ok" />
              <Counter label="À vérifier" value={bilan.aVerifier} tone="warn" />
              <Counter label="Bloquées" value={bilan.bloquees} tone="err" />
              <Counter label="Temps moyen / fiche" value={formatDuree(bilan.dureeMoyenneMs)} />
              <Counter label="Crédits utilisés" value={bilan.creditsTotal} />
            </div>

            <table className="table">
              <thead>
                <tr>
                  <th>Fiche</th>
                  <th>Contact</th>
                  <th>Entreprise</th>
                  <th>Statut</th>
                  <th>Anomalies</th>
                  <th>Durée</th>
                  <th>HubSpot</th>
                </tr>
              </thead>
              <tbody>
                {[...rows].reverse().map((r) => (
                  <Ligne key={`${r.legacy_id}-${r.created_at}`} row={r} hubspotUrl={state?.hubspotContactUrl ?? null} />
                ))}
                {rows.length === 0 && (
                  <tr>
                    <td colSpan={7} className="muted center">
                      L&apos;agent ouvre l&apos;ancien CRM…
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </section>

          {/* ───────── 3. Bilan ───────── */}
          <section className={`card bilan ${bilan.terminee ? "done" : ""}`}>
            <h2>{bilan.terminee ? "Bilan de la migration" : "Bilan (provisoire)"}</h2>
            <div className="bilan-grid">
              <Stat label="Fiches envoyées dans HubSpot" value={`${bilan.migrees} / ${bilan.traitees}`} big />
              <Stat label="Taux de réussite" value={bilan.tauxReussite === null ? "—" : `${bilan.tauxReussite} %`} big />
              <Stat label="Durée totale de l'agent" value={formatDuree(bilan.dureeTotaleMs)} />
              <Stat label="Temps moyen par fiche" value={formatDuree(bilan.dureeMoyenneMs)} />
              <Stat label="Crédits Agent API" value={String(bilan.creditsTotal)} />
              <Stat label="Crédits par fiche" value={bilan.creditsParFiche === null ? "—" : String(bilan.creditsParFiche)} />
            </div>

            <div className="bilan-cols">
              <div>
                <h3>Fiches bloquées ({bloquees.length})</h3>
                {bloquees.length === 0 ? (
                  <p className="muted">Aucune.</p>
                ) : (
                  <>
                    <ul className="blocked">
                      {bloquees.map((r) => (
                        <li key={r.legacy_id}>
                          <strong>{r.legacy_id}</strong> {nom(r)} — {reason(r)}
                        </li>
                      ))}
                    </ul>
                    <p className="muted small">
                      Ces fiches n&apos;ont pas été envoyées dans HubSpot : elles sont à corriger à la main.
                    </p>
                  </>
                )}
              </div>
              <div>
                <h3>Anomalies détectées</h3>
                {bilan.anomaliesParType.length === 0 ? (
                  <p className="muted">Aucune.</p>
                ) : (
                  <ul className="anomalies">
                    {bilan.anomaliesParType.map((a) => (
                      <li key={a.code}>
                        <span>{a.label}</span>
                        <span className="pill">{a.count}</span>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            </div>
          </section>
        </>
      )}
    </main>
  );
}

function nom(r: LogRow): string {
  const e = r.extracted;
  if (!e) return "";
  return [e.first_name, e.last_name].filter(Boolean).join(" ");
}

function Ligne({ row, hubspotUrl }: { row: LogRow; hubspotUrl: string | null }) {
  const ui = UI_STATUS[row.status];
  return (
    <tr>
      <td className="mono">{row.legacy_id}</td>
      <td>{nom(row) || <span className="muted">—</span>}</td>
      <td>{row.extracted?.company ?? <span className="muted">—</span>}</td>
      <td>
        <span className={`status status-${ui}`}>{UI_LABEL[ui]}</span>
      </td>
      <td className="small">{reason(row) || <span className="muted">—</span>}</td>
      <td className="mono">{formatDuree(row.duration_ms)}</td>
      <td>
        {row.hubspot_id ? (
          hubspotUrl ? (
            <a href={`${hubspotUrl}${row.hubspot_id}`} target="_blank" rel="noreferrer">
              Ouvrir
            </a>
          ) : (
            "✓"
          )
        ) : (
          <span className="muted">—</span>
        )}
      </td>
    </tr>
  );
}

function Counter({ label, value, tone }: { label: string; value: number | string; tone?: "ok" | "warn" | "err" }) {
  return (
    <div className={`counter ${tone ?? ""}`}>
      <div className="counter-value">{value}</div>
      <div className="counter-label">{label}</div>
    </div>
  );
}

function Stat({ label, value, big }: { label: string; value: string; big?: boolean }) {
  return (
    <div className="stat">
      <div className={big ? "stat-value big" : "stat-value"}>{value}</div>
      <div className="stat-label">{label}</div>
    </div>
  );
}
