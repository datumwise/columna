"""Provider boundary. Model selection stays OUT of answer logic, per the brief.

OPENWORKER / AISUITE DECISION (reported here because this is the file where it would have landed).

  · OpenWorker — REJECTED. It is a Tauri desktop shell over a local Python agent server, and its
    value is connectors, workspace roots, file artifacts, and consequence-based approvals. Ask
    datumwise is a public stateless web service that must not touch a filesystem, has no user
    accounts, and needs none of that. Adopting it would make the prototype larger than the product.
    Its permission model also gates on CONSEQUENCE (will this write a file) where ours must gate on
    ENTITLEMENT (is this claim supported) — a different axis that does not come free.

  · aisuite — BORROWED, NOT DEPENDED ON. Its real contribution to us is one good idea: address a
    model as a single `provider:model` string so swapping providers is a config change, not a code
    change. That idea is adopted verbatim below, so a later switch to aisuite is a drop-in. The
    library itself is declined because this repo runs a dependency-cap guard and the boundary we
    actually need is the ~40 lines in this file. If we reach three or four live providers and this
    starts accreting per-provider special cases, aisuite becomes the obvious replacement and the
    model-string convention means that day costs nothing.

CREDENTIALS ACTUALLY PRESENT IN THIS ENVIRONMENT: OpenAI only. Anthropic, Google and xAI adapters
are written and unreachable — they are listed in MISSING so the report can name the exact missing
dependency rather than redesigning around it.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass

DEFAULT_MODEL = os.environ.get("ASK_MODEL", "openai:gpt-5")
EMBED_MODEL = os.environ.get("ASK_EMBED_MODEL", "openai:text-embedding-3-small")
TIMEOUT = int(os.environ.get("ASK_TIMEOUT", "180"))

# Rough public per-1M-token rates, used ONLY to estimate cost in the eval report. Not billing.
# Kept in one place and clearly labelled so nobody mistakes an estimate for an invoice.
PRICES = {
    "gpt-5":            {"in": 1.25, "out": 10.00},
    "gpt-5-mini":       {"in": 0.25, "out": 2.00},
    "gpt-4.1":          {"in": 2.00, "out": 8.00},
    "gpt-4.1-mini":     {"in": 0.40, "out": 1.60},
    "text-embedding-3-small": {"in": 0.02, "out": 0.0},
}


@dataclass
class Completion:
    text: str
    model: str
    provider: str
    prompt_tokens: int
    completion_tokens: int

    @property
    def cost_usd(self) -> float:
        p = PRICES.get(self.model.split(":")[-1], {"in": 0.0, "out": 0.0})
        return round(
            self.prompt_tokens / 1e6 * p["in"] + self.completion_tokens / 1e6 * p["out"], 6
        )


def _post(url: str, payload: dict, key: str, extra: dict | None = None) -> dict:
    body = json.dumps(payload).encode()
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {key}", **(extra or {})}
    req = urllib.request.Request(url, data=body, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"{url} -> HTTP {e.code}: {e.read()[:500].decode(errors='replace')}")


# ── adapters ──────────────────────────────────────────────────────────────────────────────────────
# Each takes (model, messages) and returns Completion. Adding a provider is adding one function and
# one registry line; nothing in answer.py changes.

# Two OpenAI keys exist in the deployment environment and they bill to DIFFERENT accounts:
# OPENAI_ASK is this service's own key, OPENAI_API_KEY is the shared/general one. Both are
# accepted; the service's own key is preferred so this eval's spend lands on this service's
# account, and so a 2026-08-25-style stall (general key valid but credit_balance_exhausted,
# funded key sitting unused beside it) resolves itself instead of halting a 20-minute run.
_OPENAI_ENV = ("OPENAI_ASK", "OPENAI_API_KEY")


def _openai_key() -> str:
    for name in _OPENAI_ENV:
        v = os.environ.get(name)
        if v:
            return v
    raise RuntimeError(f"no OpenAI key set; tried {', '.join(_OPENAI_ENV)}")


def _openai(model: str, messages: list[dict], **kw) -> Completion:
    key = _openai_key()
    payload: dict = {"model": model, "messages": messages}
    # The gpt-5 family takes max_completion_tokens and rejects a custom temperature.
    if model.startswith("gpt-5") or model.startswith("o3") or model.startswith("o4"):
        payload["max_completion_tokens"] = kw.get("max_tokens", 4000)
    else:
        payload["max_tokens"] = kw.get("max_tokens", 4000)
        payload["temperature"] = kw.get("temperature", 0.2)
    d = _post("https://api.openai.com/v1/chat/completions", payload, key)
    u = d.get("usage", {})
    return Completion(
        text=d["choices"][0]["message"]["content"] or "",
        model=model,
        provider="openai",
        prompt_tokens=u.get("prompt_tokens", 0),
        completion_tokens=u.get("completion_tokens", 0),
    )


def _anthropic(model: str, messages: list[dict], **kw) -> Completion:
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise RuntimeError("ANTHROPIC_API_KEY is not set")
    system = "\n\n".join(m["content"] for m in messages if m["role"] == "system")
    rest = [m for m in messages if m["role"] != "system"]
    payload = {
        "model": model, "system": system, "messages": rest,
        "max_tokens": kw.get("max_tokens", 4000),
    }
    d = _post(
        "https://api.anthropic.com/v1/messages", payload, key,
        extra={"anthropic-version": "2023-06-01", "x-api-key": key},
    )
    u = d.get("usage", {})
    return Completion(
        text="".join(b.get("text", "") for b in d.get("content", [])),
        model=model, provider="anthropic",
        prompt_tokens=u.get("input_tokens", 0), completion_tokens=u.get("output_tokens", 0),
    )


def _google(model: str, messages: list[dict], **kw) -> Completion:
    key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("GOOGLE_API_KEY / GEMINI_API_KEY is not set")
    system = "\n\n".join(m["content"] for m in messages if m["role"] == "system")
    contents = [
        {"role": "user" if m["role"] == "user" else "model", "parts": [{"text": m["content"]}]}
        for m in messages if m["role"] != "system"
    ]
    payload = {"contents": contents, "systemInstruction": {"parts": [{"text": system}]}}
    d = _post(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}",
        payload, key,
    )
    u = d.get("usageMetadata", {})
    parts = d["candidates"][0]["content"]["parts"]
    return Completion(
        text="".join(p.get("text", "") for p in parts),
        model=model, provider="google",
        prompt_tokens=u.get("promptTokenCount", 0),
        completion_tokens=u.get("candidatesTokenCount", 0),
    )


def _xai(model: str, messages: list[dict], **kw) -> Completion:
    key = os.environ.get("XAI_API_KEY") or os.environ.get("GROK_API_KEY")
    if not key:
        raise RuntimeError("XAI_API_KEY / GROK_API_KEY is not set")
    payload = {"model": model, "messages": messages, "max_tokens": kw.get("max_tokens", 4000)}
    d = _post("https://api.x.ai/v1/chat/completions", payload, key)
    u = d.get("usage", {})
    return Completion(
        text=d["choices"][0]["message"]["content"] or "",
        model=model, provider="xai",
        prompt_tokens=u.get("prompt_tokens", 0), completion_tokens=u.get("completion_tokens", 0),
    )


ADAPTERS = {"openai": _openai, "anthropic": _anthropic, "google": _google, "xai": _xai}
ENV_FOR = {
    "openai": _OPENAI_ENV,
    "anthropic": ("ANTHROPIC_API_KEY",),
    "google": ("GOOGLE_API_KEY", "GEMINI_API_KEY"),
    "xai": ("XAI_API_KEY", "GROK_API_KEY"),
}


def available() -> dict[str, bool]:
    return {p: any(os.environ.get(e) for e in envs) for p, envs in ENV_FOR.items()}


def complete(messages: list[dict], model: str | None = None, **kw) -> Completion:
    """`provider:model` in, Completion out. The only entry point answer.py knows about."""
    spec = model or DEFAULT_MODEL
    provider, _, name = spec.partition(":")
    if not name:
        raise ValueError(f"model must be 'provider:model', got {spec!r}")
    fn = ADAPTERS.get(provider)
    if not fn:
        raise ValueError(f"unknown provider {provider!r}; known: {sorted(ADAPTERS)}")
    return fn(name, messages, **kw)


def embed(texts: list[str], model: str | None = None) -> list[list[float]]:
    """Unit-normalised embedding vectors. Only OpenAI is wired; the optional path is optional."""
    spec = model or EMBED_MODEL
    provider, _, name = spec.partition(":")
    if provider != "openai":
        raise NotImplementedError(f"embeddings for {provider!r} are not wired")
    key = _openai_key()
    out: list[list[float]] = []
    for i in range(0, len(texts), 256):  # batch, the endpoint has an input cap
        d = _post(
            "https://api.openai.com/v1/embeddings",
            {"model": name, "input": [t[:8000] for t in texts[i : i + 256]]},
            key,
        )
        out.extend(item["embedding"] for item in sorted(d["data"], key=lambda x: x["index"]))
    return out
