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
DEFAULTS = {
    1: {"model": "Qwen/Qwen3-32B"},
    2: {"model": "Qwen/Qwen3-Next-80B-A3B-Instruct"},  # un autre modèle : un 2e avis indépendant
}


class LLMError(RuntimeError):
    pass


def config(n: int) -> dict:
    return {
        "base_url": os.environ.get(f"SKILL_LLM{n}_BASE_URL", HF_ROUTER).rstrip("/"),
        "api_key": os.environ.get(f"SKILL_LLM{n}_API_KEY") or os.environ.get("HF_TOKEN", ""),
        "model": os.environ.get(f"SKILL_LLM{n}_MODEL", DEFAULTS[n]["model"]),
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


def chat_json(n: int, system: str, user: str, timeout: int = 120) -> dict:
    """Envoie une question à l'IA n°n et renvoie sa réponse JSON."""
    cfg = config(n)
    if not cfg["api_key"]:
        raise LLMError(f"IA n°{n} : clé absente (SKILL_LLM{n}_API_KEY ou HF_TOKEN)")
    body = json.dumps({
        "model": cfg["model"],
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        "temperature": 0,
        "max_tokens": 4000,
    }).encode()
    req = urllib.request.Request(
        f"{cfg['base_url']}/chat/completions", data=body, method="POST",
        headers={"Authorization": f"Bearer {cfg['api_key']}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as res:
            data = json.loads(res.read().decode())
    except urllib.error.HTTPError as e:
        raise LLMError(f"IA n°{n} ({cfg['model']}) : HTTP {e.code} {e.read().decode()[:300]}") from e
    except (urllib.error.URLError, TimeoutError) as e:
        raise LLMError(f"IA n°{n} ({cfg['model']}) injoignable : {e}") from e
    try:
        content = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as e:
        raise LLMError(f"IA n°{n} : réponse inattendue {str(data)[:200]}") from e
    return extract_json(content)
