"""
columna_server.init.providers — the init provider layer. `scripted` (hermetic, the default everywhere)
+ `anthropic` (the real mind, which runs ONLY on an explicit go). The provider reads the aperture,
assembles a prompt from the FROZEN knowledge package (system_prompt.md), and parses the model's response
into proposal specs. It cannot open a door: the prompt forbids it and the draft schema refuses it.
"""
from __future__ import annotations

import json
import os
from importlib.resources import files

DEFAULT_MODEL = "claude-opus-4-8"
MODEL_ENV = "COLUMNA_INIT_MODEL"
KEY_ENV = "ANTHROPIC_API_KEY"


class ProviderUnavailable(RuntimeError):
    """The real provider cannot run (no key / SDK) — hermetic runs use the scripted provider."""


def system_prompt() -> str:
    """The live, versioned authoring prompt (rendered from the ratified knowledge package §A)."""
    return files("columna_server.init").joinpath("system_prompt.md").read_text(encoding="utf-8")


def aperture_context(aperture) -> str:
    """The schema context init reads — CATALOG only here (profile/sample are the model's follow-up
    calls via the aperture in a real run). No data values leak into the prompt at this step."""
    lines = ["Catalog:"]
    for t in aperture.catalog():
        cols = ", ".join(f"{c['name']}:{c['type']}" for c in t["columns"])
        keys = f"  keys={t['keys']}" if t["keys"] else ""
        lines.append(f"  {t['table']}({cols}){keys}")
    return "\n".join(lines)


def parse_proposals(text: str) -> list:
    """The model's response → proposal specs. It must be a JSON array of {kind, target, body, ...};
    prose or the wrong shape is a hard error (grounding — the harness never guesses the mind's intent).
    A spec that tries to open a door (`opens_fertility`/`author_declared`) is stripped of those keys —
    the wall is not negotiable from the response side either."""
    data = json.loads(text)
    if not isinstance(data, list):
        raise ValueError("init provider response must be a JSON array of proposal specs")
    out = []
    for s in data:
        if not isinstance(s, dict) or "kind" not in s or "body" not in s:
            raise ValueError(f"malformed proposal spec: {s!r}")
        s = {k: v for k, v in s.items() if k not in ("opens_fertility", "author_declared")}
        out.append(s)
    return out


class AnthropicProvider:
    """The real mind — one `messages.create` per turn, guided by the frozen knowledge package. Runs
    ONLY when a key is present AND the caller opts in (rider 3: the first real-model run waits for the
    explicit go). Deps live in the `[agent]` extra."""

    name = "anthropic"

    def __init__(self, model: str | None = None):
        self.model = model or os.environ.get(MODEL_ENV, DEFAULT_MODEL)
        if not os.environ.get(KEY_ENV):
            raise ProviderUnavailable(
                f"{KEY_ENV} not set — the real mind runs only on an explicit go; hermetic runs use the "
                f"scripted provider.")
        try:
            import anthropic
        except ModuleNotFoundError as e:
            raise ProviderUnavailable("the anthropic SDK is not installed (the [agent] extra).") from e
        self._client = anthropic.Anthropic()

    def _call(self, aperture, draft) -> list:
        resp = self._client.messages.create(
            model=self.model, max_tokens=2048, system=system_prompt(),
            messages=[{"role": "user", "content": aperture_context(aperture)}])
        text = "".join(b.text for b in resp.content if b.type == "text").strip()
        return parse_proposals(text)

    def propose(self, aperture, draft):
        return self._call(aperture, draft)

    def revise(self, aperture, draft):
        return self._call(aperture, draft)
