"""Client minimal de l'Agent API de H Company (Python standard, aucune dépendance).

Propriétaire : Alexis.
Doc : https://hub.hcompany.ai/agents-api/overview

La clé est lue dans HAI_API_KEY (nom utilisé par la doc et les SDK de H Company).
Elle ne doit jamais être écrite dans le code ni dans Git.
"""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from datetime import datetime

API = os.environ.get("HAI_API_URL", "https://agp.eu.hcompany.ai/api/v2")
TERMINAL = {"completed", "failed", "timed_out", "interrupted"}


class HError(Exception):
    def __init__(self, status: int, body: str):
        super().__init__(f"H Company HTTP {status} : {body[:300]}")
        self.status = status


def _key() -> str:
    key = os.environ.get("HAI_API_KEY")
    if not key:
        raise RuntimeError("Variable HAI_API_KEY absente (clé Agent API H Company).")
    return key


def request(method: str, path: str, body: dict | None = None, timeout: int = 60):
    req = urllib.request.Request(
        API + path,
        data=json.dumps(body).encode("utf-8") if body is not None else None,
        method=method,
        headers={"Authorization": f"Bearer {_key()}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as res:
            raw = res.read().decode("utf-8")
            return (json.loads(raw) if raw else {}), res.status
    except urllib.error.HTTPError as e:
        raise HError(e.code, e.read().decode("utf-8", "replace")) from None


def quota() -> dict:
    return request("GET", "/sessions/quota")[0]


def create_session(task: str, answer_format: dict, start_url: str | None = None,
                   agent: str = "h/web-surfer-flash", max_steps: int = 40,
                   max_time_s: int = 240, group_id: str | None = None) -> str:
    """Lance un agent sur une tâche. Renvoie l'identifiant de session."""
    overrides: dict = {
        "agent.answer_format": answer_format,
        # Mode visuel (captures d'écran : navigation + preuve D14) AVEC le texte de la page :
        # l'agent lit les caractères exacts au lieu de les déchiffrer sur l'image (évite « 39 » lu « 99 »).
        "agent.environments[kind=web].mode": {"type": "visual", "width": 1200, "height": 1200, "markdown": True},
    }
    if start_url:
        overrides["agent.environments[kind=web].start_url"] = start_url
    body = {
        "agent": agent,
        "messages": task,
        "max_steps": max_steps,
        "max_time_s": max_time_s,
        "timezone": "Europe/Paris",
        "overrides": overrides,
    }
    if group_id:
        body["group_id"] = group_id
    return request("POST", "/sessions", body)[0]["id"]


def _ts(value: str | None) -> datetime | None:
    return datetime.fromisoformat(value.replace("Z", "+00:00")) if value else None


def wait(session_id: str, max_wait_s: int = 600) -> dict:
    """Suit une session jusqu'à la fin (long-poll /changes, règles de la doc H).

    Renvoie : status, answer, error_code, error, outcome, steps, cost_usd, duration_ms, screenshots.
    """
    index, deadline = 0, time.time() + max_wait_s
    last: dict = {}
    screenshots: list[str] = []
    while time.time() < deadline:
        # Long-poll de 20 s tant que l'agent travaille ; une fois la session terminée,
        # on ne fait plus que des lectures immédiates (sinon ~20 s perdues par fiche).
        wait_s = 0 if last.get("status") in TERMINAL else 20
        data, code = request(
            "GET", f"/sessions/{session_id}/changes?from_index={index}&wait_for_seconds={wait_s}", timeout=40)
        if code == 204 or not data:
            if last.get("status") in TERMINAL:
                break
            continue
        last = data
        events = data.get("new_events") or []
        for ev in events:
            # Capture d'écran d'une observation : AgentEvent → data.image.source (décision D14)
            image = (ev.get("data") or {}).get("image") if ev.get("type") == "AgentEvent" else None
            if isinstance(image, dict) and image.get("source"):
                screenshots.append(image["source"])
        index = (data.get("first_index") or index) + len(events)
        if data.get("status") in TERMINAL and (not events or data.get("answer") is not None):
            break   # session terminée et réponse reçue : inutile d'attendre davantage
    else:
        raise TimeoutError(f"session {session_id} toujours en cours après {max_wait_s} s")

    if last.get("answer") is None and last.get("status") == "completed":
        last["answer"] = request("GET", f"/sessions/{session_id}")[0].get("latest_answer")

    start, end = _ts(last.get("started_at")), _ts(last.get("finished_at"))
    metrics = last.get("metrics") or {}
    return {
        "session_id": session_id,
        "status": last.get("status"),
        "answer": last.get("answer"),
        "error_code": last.get("error_code"),
        "error": last.get("error"),
        "outcome": last.get("outcome"),
        "steps": metrics.get("steps"),
        "cost_usd": metrics.get("total_cost"),
        "duration_ms": int((end - start).total_seconds() * 1000) if start and end else None,
        "started_at": last.get("started_at"),
        "finished_at": last.get("finished_at"),
        "screenshots": screenshots,
    }
