"""
columna_server.agent.providers — the tiny provider layer (WP-2.4 ruling 3-B).

`propose(system, history, user_msg) -> str` returns the model's next line — either `QUERY: <frameql>`
or `ASK: <question>`. The provider ONLY produces text; it never touches MCP or the engine. Two
implementations: `anthropic` (default, BYO key) and `scripted` (deterministic, for tests/demos).
"""
from __future__ import annotations

import os
from typing import Protocol, runtime_checkable

from .conversation import AGENT, ENGINE, Turn

DEFAULT_MODEL = "claude-opus-4-8"
MODEL_ENV = "COLUMNA_AGENT_MODEL"
KEY_ENV = "ANTHROPIC_API_KEY"


class ProviderUnavailable(RuntimeError):
    """The requested provider cannot run (e.g. no API key)."""


@runtime_checkable
class Provider(Protocol):
    name: str

    def propose(self, system: str, history: list[Turn], user_msg: str) -> str:
        """Return the next agent line: 'QUERY: <frameql>' or 'ASK: <question>'."""
        ...


class ScriptedProvider:
    """Deterministic provider: replays a fixed list of lines, one per call. For tests and demos —
    no network, no key. Raises if the script runs dry (a sign the conversation went further than
    the test scripted)."""

    name = "scripted"

    def __init__(self, script: list[str]):
        self._script = list(script)
        self._i = 0

    def propose(self, system: str, history: list[Turn], user_msg: str) -> str:
        if self._i >= len(self._script):
            raise ProviderUnavailable("scripted provider exhausted — the agent asked for more "
                                      "proposals than the script supplies")
        line = self._script[self._i]
        self._i += 1
        return line


class AnthropicProvider:
    """Default provider — one `messages.create` per turn via the official anthropic SDK. Model from
    COLUMNA_AGENT_MODEL (default claude-opus-4-8); key from ANTHROPIC_API_KEY. Deps live in the
    `[agent]` extra; no key -> a clear error pointing at the packaged demo."""

    name = "anthropic"

    def __init__(self, model: str | None = None):
        self.model = model or os.environ.get(MODEL_ENV, DEFAULT_MODEL)
        if not os.environ.get(KEY_ENV):
            raise ProviderUnavailable(
                f"{KEY_ENV} is not set. Set it to use the natural-language agent, or try the "
                f"no-key packaged demo: `columna-server demo --play`."
            )
        try:
            import anthropic
        except ModuleNotFoundError as e:
            raise ProviderUnavailable(
                "the anthropic SDK is not installed — install the agent extra: "
                "`pip install -e \"packages/columna-server[agent]\"`."
            ) from e
        self._client = anthropic.Anthropic()

    def propose(self, system: str, history: list[Turn], user_msg: str) -> str:
        # Render the conversation as alternating user/assistant messages. The engine notes and the
        # human turns become `user` content (context for the model); the agent's own prior lines
        # become `assistant` content. The system prompt is passed separately.
        messages = []
        for t in history:
            if t.role == AGENT:
                messages.append({"role": "assistant", "content": t.text})
            else:  # USER or ENGINE — both are context the model reads
                prefix = "[engine] " if t.role == ENGINE else ""
                messages.append({"role": "user", "content": prefix + t.text})
        messages.append({"role": "user", "content": user_msg})

        resp = self._client.messages.create(
            model=self.model, max_tokens=512, system=system, messages=_coalesce(messages),
        )
        return "".join(b.text for b in resp.content if b.type == "text").strip()


def _coalesce(messages: list[dict]) -> list[dict]:
    """The Messages API requires the first message to be `user` and forbids empty history. Merge
    consecutive same-role messages so a run of engine+user notes stays one turn."""
    out: list[dict] = []
    for m in messages:
        if out and out[-1]["role"] == m["role"]:
            out[-1]["content"] = out[-1]["content"] + "\n" + m["content"]
        else:
            out.append(dict(m))
    if not out or out[0]["role"] != "user":
        out.insert(0, {"role": "user", "content": "(begin)"})
    return out


def make_provider(name: str, model: str | None = None) -> Provider:
    if name == "scripted":
        raise ProviderUnavailable("the scripted provider requires an explicit script; "
                                  "construct ScriptedProvider(script) directly")
    if name == "anthropic":
        return AnthropicProvider(model=model)
    raise ProviderUnavailable(f"unknown provider '{name}' (have: anthropic, scripted)")
