"use client";

import { useEffect, useState } from "react";
import { FIELD_LABEL, UI_LABEL, UI_STATUS, computeBilan, formatDuree, reason, rereadChanged } from "@/lib/bilan";
import type { LiveAgent, LogRow, RunState } from "@/lib/types";

type Run = { runId: string; mode: "demo" | "live"; total: number };

const POLL_MS = 2000;
const LIVE_MS = 3000;

export default function SuiviMigration() {
  const [run, setRun] = useState<Run | null>(null);
  const [state, setState] = useState<RunState | null>(null);
  const [launching, setLaunching] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [preuve, setPreuve] = useState<LogRow | null>(null); // fiche ouverte dans la fenêtre « Preuve »
  const [peutLancerReel, setPeutLancerReel] = useState(false); // le bouton déclenche-t-il le vrai agent ?
  const [agents, setAgents] = useState<LiveAgent[]>([]);

  const rows = state?.rows ?? [];
  const total = state?.total ?? run?.total ?? 0;
  const bilan = computeBilan(rows, total);
  const suitDernier = run?.runId === "dernier";
  const running = run !== null && (suitDernier ? agents.length > 0 : !bilan.terminee);
  // Lancement suivi pour le panneau « Agents en direct » (« dernier » est résolu par l'API).
  const liveRunId = state?.resolvedRunId ?? run?.runId ?? null;

  async function lancer() {
    setLaunching(true);
    setError(null);
    setState(null);
    try {
      const res = await fetch("/api/migration", { method: "POST" });
      const body = await res.json();
      if (!res.ok) throw new Error(body.error ?? `HTTP ${res.status}`);
      setRun(body as Run);
      // L'adresse garde le lancement : un rechargement de la page continue de le suivre.
      if (body.mode === "live") window.history.replaceState(null, "", `?run=${body.runId}&total=${body.total}`);
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
        // « dernier » : on continue de suivre (un nouveau lancement peut démarrer).
        if (run.runId !== "dernier" && (body as RunState).rows.length >= (body as RunState).total) stop = true;
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

  // Agents H en train de travailler (captures en direct), tant que la migration réelle tourne.
  const suivreAgents = run?.mode === "live" && liveRunId !== null && liveRunId !== "tout" && (running || suitDernier);
  useEffect(() => {
    if (!suivreAgents || !liveRunId) return;
    let stop = false;
    const tick = async () => {
      try {
        const res = await fetch(`/api/live/${liveRunId}`, { cache: "no-store" });
        const body = (await res.json()) as { agents?: LiveAgent[] };
        if (!stop) setAgents(body.agents ?? []);
      } catch {
        /* le panneau est un bonus : on ignore une erreur passagère */
      }
    };
    tick();
    const id = setInterval(tick, LIVE_MS);
    return () => {
      stop = true;
      clearInterval(id);
    };
  }, [suivreAgents, liveRunId]);

  // Le bouton peut-il lancer le vrai agent (action GitHub configurée) ?
  useEffect(() => {
    fetch("/api/migration", { cache: "no-store" })
      .then((r) => r.json())
      .then((b: { live?: boolean }) => setPeutLancerReel(Boolean(b.live)))
      .catch(() => {});
  }, []);

  // Afficher une migration existante : ?run=tout (toutes les fiches) ou ?run=<identifiant du lancement>
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const param = params.get("run");
    // ?run=dernier : le lancement le plus récent (pratique pendant la démo).
    // L'adresse n'est connue que dans le navigateur : on l'applique juste après l'affichage initial.
    if (param) queueMicrotask(() => setRun({ runId: param, mode: "live", total: Number(params.get("total")) || 0 }));
  }, []);

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
        {run?.mode === "live" && (running || !peutLancerReel) ? (
          // Migration réelle : pas de bouton qui relancerait une simulation par erreur pendant la démo.
          <span className="badge-live">{running ? "Migration réelle en cours…" : "Migration réelle · agent H Company"}</span>
        ) : (
          <button className="btn" onClick={lancer} disabled={launching || running}>
            {launching
              ? "Lancement…"
              : running
                ? "Migration en cours…"
                : peutLancerReel
                  ? "Lancer la migration (agent réel)"
                  : run
                    ? "Relancer la migration"
                    : "Lancer la migration"}
          </button>
        )}
      </section>

      {error && <p className="alert">⚠️ {error}</p>}

      {run && (
        <>
          {/* ───────── Agents en direct (migration réelle) ───────── */}
          {suivreAgents && (
            <AgentsEnDirect agents={agents} attente={rows.length === 0} />
          )}

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
              <Counter label="Coût agent H" value={formatDollars(bilan.creditsTotal, 2)} />
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
                  <th>Preuve</th>
                </tr>
              </thead>
              <tbody>
                {[...rows].reverse().map((r) => (
                  <Ligne
                    key={`${r.legacy_id}-${r.created_at}`}
                    row={r}
                    hubspotUrl={state?.hubspotContactUrl ?? null}
                    onPreuve={() => setPreuve(r)}
                  />
                ))}
                {rows.length === 0 && (
                  <tr>
                    <td colSpan={8} className="muted center">
                      {run.mode === "live" && running
                        ? "L'agent démarre (environ 30 s), puis les fiches arrivent une par une…"
                        : "L'agent ouvre l'ancien CRM…"}
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
              {bilan.dureeReelleMs !== null ? (
                <Stat label="Durée réelle de la migration" value={formatDuree(bilan.dureeReelleMs)} />
              ) : (
                <Stat label="Temps cumulé des agents" value={formatDuree(bilan.dureeTotaleMs)} />
              )}
              <Stat label="Temps moyen par fiche" value={formatDuree(bilan.dureeMoyenneMs)} />
              <Stat label="Coût Agent API" value={formatDollars(bilan.creditsTotal, 2)} />
              <Stat label="Coût par fiche" value={bilan.creditsParFiche === null ? "—" : formatDollars(bilan.creditsParFiche, 3)} />
              <Stat
                label="Champs relus par l'agent (corrigés)"
                value={`${bilan.relues} (${bilan.corrigeesParRelecture})`}
              />
              <Stat label="Fiches avec capture d'écran" value={`${bilan.avecPreuve} / ${bilan.traitees}`} />
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

      {preuve && <FenetrePreuve row={preuve} onClose={() => setPreuve(null)} />}
    </main>
  );
}

/** Ce que voient les agents H en ce moment : une capture par agent, rafraîchie toutes les 3 s. */
function AgentsEnDirect({ agents, attente }: { agents: LiveAgent[]; attente: boolean }) {
  const [t, setT] = useState(0);
  useEffect(() => {
    const id = setInterval(() => setT((x) => x + 1), LIVE_MS);
    return () => clearInterval(id);
  }, []);
  return (
    <section className="card live-agents">
      <div className="progress-head">
        <h2>Agents en direct</h2>
        <span className="muted">{agents.length} agent(s) H Company au travail</span>
      </div>
      {agents.length === 0 ? (
        <p className="muted">
          {attente ? "Démarrage des agents…" : "Aucun agent en cours : toutes les fiches lancées ont été lues."}
        </p>
      ) : (
        <div className="live-grid">
          {agents.map((a) => (
            <figure key={a.sessionId} className="live-agent">
              {/* eslint-disable-next-line @next/next/no-img-element -- capture relayée par le serveur */}
              <img
                src={`/api/live/shot/${a.sessionId}?t=${t}`}
                alt={`Écran de l'agent sur la fiche ${a.legacyId ?? ""}`}
                onError={(e) => (e.currentTarget.style.visibility = "hidden")}
                onLoad={(e) => (e.currentTarget.style.visibility = "visible")}
              />
              <figcaption>
                <span className="mono">{a.legacyId ?? "—"}</span> · l&apos;agent lit la fiche…
              </figcaption>
            </figure>
          ))}
        </div>
      )}
    </section>
  );
}

function nom(r: LogRow): string {
  const e = r.extracted;
  if (!e) return "";
  return [e.first_name, e.last_name].filter(Boolean).join(" ");
}

function Ligne({ row, hubspotUrl, onPreuve }: { row: LogRow; hubspotUrl: string | null; onPreuve: () => void }) {
  const ui = UI_STATUS[row.status];
  return (
    <tr>
      <td className="mono">{row.legacy_id}</td>
      <td>{nom(row) || <span className="muted">—</span>}</td>
      <td>{row.extracted?.company ?? <span className="muted">—</span>}</td>
      <td>
        <span className={`status status-${ui}`}>{UI_LABEL[ui]}</span>
      </td>
      <td className="small">
        {reason(row) || (!row.reread && <span className="muted">—</span>)}
        {row.reread && <Relecture row={row} />}
      </td>
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
      <td>
        {row.screenshot_url || row.extracted ? (
          <button className="link-btn" onClick={onPreuve}>
            {row.screenshot_url ? "📷 Voir" : "Voir"}
          </button>
        ) : (
          <span className="muted">—</span>
        )}
      </td>
    </tr>
  );
}

/** D13 : « relu par l'agent : Téléphone « avant » → « après » ». */
function Relecture({ row }: { row: LogRow }) {
  const r = row.reread!;
  const label = FIELD_LABEL[r.field] ?? r.field;
  if (r.error) return <div className="reread fail">🔁 Relecture de « {label} » impossible : {r.error}</div>;
  return (
    <div className={`reread ${rereadChanged(row) ? "fixed" : ""}`}>
      🔁 {label} relu par l&apos;agent : « {r.before ?? "vide"} » → « {r.after ?? "vide"} »
      {!rereadChanged(row) && " (confirmé)"}
    </div>
  );
}

/** D14 : ce que l'agent a vu (capture) à côté de ce qu'il a lu (champs extraits). */
function FenetrePreuve({ row, onClose }: { row: LogRow; onClose: () => void }) {
  const [imageKo, setImageKo] = useState(false);
  // Les captures H Company demandent la clé API : on passe par le relais serveur /api/capture.
  const capture = row.screenshot_url && row.agent_session_id ? `/api/capture/${row.agent_session_id}` : null;

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [onClose]);

  const ui = UI_STATUS[row.status];
  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal" role="dialog" aria-modal="true" onClick={(e) => e.stopPropagation()}>
        <div className="modal-head">
          <div>
            <h2>
              Preuve · <span className="mono">{row.legacy_id}</span> {nom(row)}
            </h2>
            <span className={`status status-${ui}`}>{UI_LABEL[ui]}</span>
          </div>
          <button className="close" onClick={onClose} aria-label="Fermer">
            ✕
          </button>
        </div>

        <div className="modal-body">
          <div className="shot">
            <h3>Ce que l&apos;agent a vu</h3>
            {capture && !imageKo ? (
              <a href={capture} target="_blank" rel="noreferrer">
                {/* eslint-disable-next-line @next/next/no-img-element -- capture externe (Agent API) */}
                <img src={capture} alt={`Fiche ${row.legacy_id} vue par l'agent`} onError={() => setImageKo(true)} />
              </a>
            ) : (
              <p className="muted">{row.screenshot_url ? "Capture d'écran expirée ou inaccessible." : "Pas de capture pour cette fiche."}</p>
            )}
            {row.agent_session_id && (
              <p className="muted small">
                Session de l&apos;agent : <span className="mono">{row.agent_session_id}</span>
              </p>
            )}
          </div>

          <div>
            <h3>Ce que l&apos;agent a lu</h3>
            <table className="table fields">
              <tbody>
                {Object.keys(FIELD_LABEL).map((f) => (
                  <tr key={f} className={row.reread?.field === f ? "hl" : ""}>
                    <th>{FIELD_LABEL[f]}</th>
                    <td>{row.extracted?.[f] ?? <span className="muted">—</span>}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            {row.reread && <Relecture row={row} />}
            {reason(row) && <p className="small anomalies-txt">⚠️ {reason(row)}</p>}
          </div>
        </div>
      </div>
    </div>
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

function formatDollars(value: number, digits: number): string {
  return `${value.toLocaleString("fr-FR", { minimumFractionDigits: digits, maximumFractionDigits: digits })} $`;
}
