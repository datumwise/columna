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


_OPENING_KINDS = {"fertility", "fertile", "opening", "door"}


def parse_proposals(text: str) -> list:
    """The model's response → proposal specs. It must be a JSON array of {kind, target, body, ...};
    prose or the wrong shape is a hard error (grounding — the harness never guesses the mind's intent).
    Any OPENING is DROPPED ENTIRELY (Huayin, ruling 2, 2026-07-16): a spec that opens fertility
    (`opens_fertility`, an opening kind, or a `FERTILE` clause in its body) is not de-flagged — it is
    removed, because fertility talk belongs to the ADJUDICATOR'S ADVICE channel, never to a proposal."""
    data = json.loads(text)
    if not isinstance(data, list):
        raise ValueError("init provider response must be a JSON array of proposal specs")
    out = []
    for s in data:
        if not isinstance(s, dict) or "kind" not in s or "body" not in s:
            raise ValueError(f"malformed proposal spec: {s!r}")
        if (s.get("opens_fertility") or str(s.get("kind", "")).lower() in _OPENING_KINDS
                or "FERTILE" in str(s.get("body", "")).upper()):
            continue                                     # DROP the opening entirely (not the adjudicator's channel)
        out.append({k: v for k, v in s.items() if k not in ("opens_fertility", "author_declared")})
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
        self.retries = 0                                          # malformed-output retries (convergence data)

    def _once(self, content: str) -> list:
        resp = self._client.messages.create(
            model=self.model, max_tokens=2048, system=system_prompt(),
            messages=[{"role": "user", "content": content}])
        self.last_model = getattr(resp, "model", self.model)     # the resolved version (provenance)
        text = "".join(b.text for b in resp.content if b.type == "text").strip()
        # tolerate a fenced code block around the JSON (a common, harmless model habit — recorded, not hidden)
        if text.startswith("```"):
            text = text.strip("`").split("\n", 1)[-1].rsplit("```", 1)[0].strip()
            if text.startswith("json"):
                text = text[4:].strip()
        return parse_proposals(text)

    def _call(self, content: str) -> list:
        try:
            return self._once(content)
        except Exception:                                        # ONE bounded retry on malformed output
            self.retries += 1
            return self._once(content + "\n\n(Your previous reply was not a valid JSON array of "
                                        "proposal specs. Reply with ONLY the JSON array, no prose.)")

    def propose(self, aperture, draft):
        return self._call(aperture_context(aperture))

    def revise(self, aperture, draft):
        from columna_core.draft import STRUCK, PROPOSED
        struck = [p.body for p in draft.proposals if p.review == STRUCK]
        kept = [p.body for p in draft.proposals if p.review not in (STRUCK,)]
        content = (aperture_context(aperture)
                   + "\n\nReview so far — these were STRUCK (do NOT re-propose them):\n  "
                   + ("\n  ".join(struck) or "(none)")
                   + "\nAlready accepted (do not repeat):\n  " + ("\n  ".join(kept) or "(none)")
                   + "\n\nReturn a JSON array of ONLY the NEW/corrected declarations that address the "
                     "struck marks. Do not re-propose a struck or accepted declaration.")
        return self._call(content)
