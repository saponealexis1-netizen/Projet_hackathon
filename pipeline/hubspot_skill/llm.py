"""Appel des deux IA (API compatible OpenAI) : Hugging Face Inference Providers ou Vercel AI Gateway.

Python standard, aucune dépendance. Variables d'environnement (jamais dans Git) :

| Variable                | IA n°1 « l'analyste »                     | IA n°2 « le contrôleur »                  |
|-------------------------|-------------------------------------------|-------------------------------------------|
| SKILL_LLM1_BASE_URL     | défaut : https://router.huggingface.co/v1 | SKILL_LLM2_BASE_URL (même défaut)          |
| SKILL_LLM1_API_KEY      | défaut : HF_TOKEN                         | SKILL_LLM2_API_KEY (défaut : HF_TOKEN)     |
| SKILL_LLM1_MODEL        | défaut : Qwen/Qwen3-32B                   | SKILL_LLM2_MODEL (défaut : un autre modèle)|

Pour passer l'IA n°2 sur les crédits Vercel : SKILL_LLM2_BASE_URL=https://ai-gateway.vercel.sh/v1,
SKILL_LLM2_API_KEY=<clé AI Gateway>, SKILL_LLM2_MODEL=<modèle proposé par la passerelle>.
"""
from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request

HF_ROUTER = "https://router.huggingface.co/v1"
# Si le modèle principal n'est pas servi avec notre clé, on essaie les suivants (dans l'ordre).
DEFAULTS = {
    1: {"model": "Qwen/Qwen3-32B",
        "fallbacks": ["Qwen/Qwen3-235B-A22B-Instruct-2507", "meta-llama/Llama-3.3-70B-Instruct"]},
    2: {"model": "Qwen/Qwen3-Next-80B-A3B-Instruct",  # un autre modèle : un 2e avis indépendant
        "fallbacks": ["meta-llama/Llama-3.3-70B-Instruct", "Qwen/Qwen3-235B-A22B-Instruct-2507"]},
}


class LLMError(RuntimeError):
    pass


# Modèle qui a réellement répondu (le principal ou un modèle de secours), par IA.
last_model: dict[int, str] = {}


def _env(name: str, default: str = "") -> str:
    """Variable d'environnement ; une valeur vide (secret GitHub non rempli) compte comme absente."""
    return (os.environ.get(name) or "").strip() or default


def config(n: int) -> dict:
    fallbacks = _env(f"SKILL_LLM{n}_FALLBACK_MODELS", ",".join(DEFAULTS[n]["fallbacks"]))
    return {
        "base_url": _env(f"SKILL_LLM{n}_BASE_URL", HF_ROUTER).rstrip("/"),
        "api_key": _env(f"SKILL_LLM{n}_API_KEY") or _env("HF_TOKEN"),
        "model": _env(f"SKILL_LLM{n}_MODEL", DEFAULTS[n]["model"]),
        "fallbacks": [m.strip() for m in fallbacks.split(",") if m.strip()],
    }


def available(n: int) -> bool:
    return bool(config(n)["api_key"])


def extract_json(text: str) -> dict:
    """Récupère l'objet JSON d'une réponse (en retirant le raisonnement <think>…</think> de Qwen3)."""
    text = re.sub(r"<think>.*?</think>", "", text or "", flags=re.S).strip()
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip())
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end <= start:
        raise LLMError(f"réponse sans JSON : {text[:200]!r}")
    try:
        return json.loads(text[start:end + 1])
    except ValueError as e:
        raise LLMError(f"JSON illisible : {e}") from e


def _call(cfg: dict, model: str, n: int, system: str, user: str, timeout: int) -> str:
    body = json.dumps({
        "model": model,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        "temperature": 0,
        "max_tokens": 6000,  # Qwen3 réfléchit avant de répondre : on lui laisse de la place
    }).encode()
    req = urllib.request.Request(
        f"{cfg['base_url']}/chat/completions", data=body, method="POST",
        headers={"Authorization": f"Bearer {cfg['api_key']}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as res:
            data = json.loads(res.read().decode())
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")[:300]
        if e.code in (401, 403):
            raise LLMError(f"IA n°{n} : clé refusée (HTTP {e.code}). Vérifier que la clé Hugging Face a le droit "
                           f"« Make calls to Inference Providers » et qu'il reste des crédits. {detail}") from e
        raise ModelError(f"IA n°{n} ({model}) : HTTP {e.code} {detail}", e.code) from e
    except (urllib.error.URLError, TimeoutError, ValueError) as e:
        raise LLMError(f"IA n°{n} ({model}) injoignable : {e}") from e
    try:
        message = data["choices"][0]["message"]
    except (KeyError, IndexError, TypeError) as e:
        raise LLMError(f"IA n°{n} ({model}) : réponse inattendue {str(data)[:200]}") from e
    content = message.get("content") or ""
    if "{" not in content:  # certains fournisseurs rangent tout dans le raisonnement
        content = content + "\n" + (message.get("reasoning_content") or message.get("reasoning") or "")
    if not content.strip():
        raise LLMError(f"IA n°{n} ({model}) : réponse vide (réflexion trop longue ?)")
    return content


class ModelError(LLMError):
    """Le fournisseur refuse ce modèle (non servi, introuvable…) : on peut essayer le suivant."""
    def __init__(self, message: str, status: int):
        super().__init__(message)
        self.status = status


def chat_json(n: int, system: str, user: str, timeout: int = 120) -> dict:
    """Envoie une question à l'IA n°n et renvoie sa réponse JSON.
    Si le modèle n'est pas disponible (HTTP 400/404/422/503…), essaie les modèles de secours."""
    cfg = config(n)
    if not cfg["api_key"]:
        raise LLMError(f"IA n°{n} : clé absente (SKILL_LLM{n}_API_KEY ou HF_TOKEN)")
    errors = []
    for model in [cfg["model"]] + [m for m in cfg["fallbacks"] if m != cfg["model"]]:
        try:
            answer = extract_json(_call(cfg, model, n, system, user, timeout))
            last_model[n] = model
            return answer
        except ModelError as e:
            errors.append(str(e))
            if e.status in (408, 429):  # surcharge : inutile d'insister sur d'autres modèles tout de suite
                break
    raise LLMError(" · ".join(errors))
