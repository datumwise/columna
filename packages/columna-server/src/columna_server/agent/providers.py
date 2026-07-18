"""
columna_server.agent.providers — the provider layer (WP-agent-hands).

A provider owns ONE model call and returns a STRUCTURED step: either a request to call one or more
tools (`ToolStep`) or a final text answer / question to the human (`TextStep`). It never touches MCP
or the engine — the LOOP owns tool execution (it holds the MCPServerConnection) and feeds results
back. Two implementations: `anthropic` (default, BYO key, native tool-use) and `scripted`
(deterministic, for tests/demos — no network, no key).

The tool phase per turn is driven by the loop: it calls `provider.step(...)`, executes any requested
tools, appends the results to `turn` (Anthropic-format tool_use / tool_result messages), and calls
`step` again — until the model answers with text or runs the terminal `query` tool.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from .conversation import AGENT, ENGINE, Turn

DEFAULT_MODEL = "claude-opus-4-8"
MODEL_ENV = "COLUMNA_AGENT_MODEL"
KEY_ENV = "ANTHROPIC_API_KEY"

# The EXACT toolset the agent may call (WP-agent-hands #3). No list_manifolds (the manifold is fixed
# for the session), no write tools. `manifold_id` is NOT a model-facing argument — the loop injects
# the session's manifold when it executes the call. `query` is the TERMINAL act.
TOOL_NAMES = ("describe_manifold", "describe_measure", "case_manifest", "case_chapter",
              "explain", "query")


# --- the structured step a provider returns -------------------------------------------------
@dataclass(frozen=True)
class ToolCall:
    """One tool_use block the model emitted (id echoed back on the matching tool_result)."""
    id: str
    name: str
    input: dict


@dataclass(frozen=True)
class ToolStep:
    """The model wants to call one or more tools before it answers. `text` is any preamble the
    model wrote alongside the tool calls (kept so the assistant turn round-trips faithfully)."""
    calls: list[ToolCall]
    text: str = ""


@dataclass(frozen=True)
class TextStep:
    """The model's final turn: an answer, or a question back to the human (the ASK). No tool use."""
    text: str


Step = "ToolStep | TextStep"


class ProviderUnavailable(RuntimeError):
    """The requested provider cannot run (e.g. no API key)."""


@runtime_checkable
class Provider(Protocol):
    name: str

    def step(self, system: str, history: list[Turn], user_msg: str,
             turn: list[dict]) -> "ToolStep | TextStep":
        """Return the model's next step given the prior `history`, the current `user_msg`, and this
        turn's tool exchange so far (`turn`: Anthropic-format assistant/tool_result messages)."""
        ...


# --- the anthropic tool schemas (manifold_id is injected by the loop, never by the model) ---
def _tool_schemas() -> list[dict]:
    return [
        {"name": "describe_manifold",
         "description": "Describe the manifold you are querying: dimensions/levels, functional edges "
                        "(with lineage), universes, and the measure index. Touches no data.",
         "input_schema": {"type": "object", "properties": {}, "required": []}},
        {"name": "describe_measure",
         "description": "Describe ONE measure: its folklore/description, family (root, members, "
                        "reducer kinds), per-member anchors (blocked lineages, order-by, monoid), "
                        "dtype, universe, and provenance. Consult it when a turn needs a definition "
                        "(e.g. what a measure means or why a reduction is blocked). Touches no data.",
         "input_schema": {"type": "object",
                          "properties": {"measure": {"type": "string",
                                                     "description": "the measure name, as written"}},
                          "required": ["measure"]}},
        {"name": "case_manifest",
         "description": "The 3-descriptor routing manifest for the case document: which chapter "
                        "answers which kind of 'why'.",
         "input_schema": {"type": "object", "properties": {}, "required": []}},
        {"name": "case_chapter",
         "description": "Fetch ONE case chapter VERBATIM — the on-demand WHY behind this manifold. "
                        "Consult it when relaying a clarify/refuse/material caveat, or when the human "
                        "asks a why / folklore / definition-history question. Not on a plain serve. "
                        "ch1 = the purpose and the requirement; ch2 = the design's reasons; "
                        "ch3 = the behaviors and the moods.",
         "input_schema": {"type": "object",
                          "properties": {"chapter": {"type": "string", "enum": ["ch1", "ch2", "ch3"]}},
                          "required": ["chapter"]}},
        {"name": "explain",
         "description": "EXPLAIN a FrameQL envelope statement WITHOUT executing it — the cheap inner "
                        "loop. Returns the desugared form, atom decomposition, the dependency cone "
                        "with verdicts, and the would-be outcome + disclosures. Touches ZERO data. "
                        "Use it to check a query before you commit to it.",
         "input_schema": {"type": "object",
                          "properties": {"frameql": {"type": "string",
                                                     "description": "a FrameQL SELECT … AT {…} statement"}},
                          "required": ["frameql"]}},
        {"name": "query",
         "description": "Execute a FrameQL envelope statement (SELECT <series> AT {anchor} with "
                        "optional WHERE/HAVING/ORDER BY/LIMIT; never SQL). This is the TERMINAL act: "
                        "running a query ends your tool phase and the system presents the four-mood "
                        "result to the human verbatim. Propose exactly one when you are ready to answer.",
         "input_schema": {"type": "object",
                          "properties": {"frameql": {"type": "string",
                                                     "description": "a FrameQL SELECT … AT {…} statement"}},
                          "required": ["frameql"]}},
    ]


class ScriptedProvider:
    """Deterministic provider: replays a fixed list of steps, one per `step()` call. For tests and
    demos — no network, no key. Script elements may be:

      * a `ToolStep` / `TextStep` (used directly);
      * `"QUERY: <frameql>"`  → a terminal `query` tool call;
      * `"ASK: <question>"`   → a `TextStep` (a question back to the human);
      * `("<tool>", {..})`    → a single tool call;
      * `[("<tool>", {..}), …]` → several tool calls in one step;
      * any other bare string → a `TextStep` (the agent grounding-guards it before presenting).

    Raises if the script runs dry (a sign the conversation went further than the test scripted)."""

    name = "scripted"

    def __init__(self, script: list):
        self._script = list(script)
        self._i = 0
        self._nid = 0

    def _call(self, name: str, inp: dict) -> ToolCall:
        self._nid += 1
        return ToolCall(f"scr_{self._nid}", name, dict(inp))

    def _coerce(self, item) -> "ToolStep | TextStep":
        if isinstance(item, (ToolStep, TextStep)):
            return item
        if isinstance(item, str):
            s = item.strip()
            if s.startswith("QUERY:"):
                return ToolStep([self._call("query", {"frameql": s[len("QUERY:"):].strip()})])
            if s.startswith("ASK:"):
                return TextStep(s[len("ASK:"):].strip())
            return TextStep(s)
        if isinstance(item, tuple):                       # ("tool", {input})
            name, inp = item
            return ToolStep([self._call(name, inp)])
        if isinstance(item, list):                        # [("tool", {input}), …]
            return ToolStep([self._call(name, inp) for (name, inp) in item])
        raise ProviderUnavailable(f"scripted step of unsupported type: {type(item).__name__}")

    def step(self, system: str, history: list[Turn], user_msg: str,
             turn: list[dict]) -> "ToolStep | TextStep":
        if self._i >= len(self._script):
            raise ProviderUnavailable("scripted provider exhausted — the agent asked for more "
                                      "steps than the script supplies")
        item = self._script[self._i]
        self._i += 1
        return self._coerce(item)


class AnthropicProvider:
    """Default provider — native tool-use over the official anthropic SDK. One `messages.create` per
    `step()`; the model may emit tool_use blocks (the loop executes them and calls back) or answer
    with text. Model from COLUMNA_AGENT_MODEL (default claude-opus-4-8); key from ANTHROPIC_API_KEY.
    Deps live in the `[agent]` extra; no key -> a clear error pointing at the packaged demo."""

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
        self._tools = _tool_schemas()

    def _base_messages(self, history: list[Turn], user_msg: str) -> list[dict]:
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
        return _coalesce(messages)

    def step(self, system: str, history: list[Turn], user_msg: str,
             turn: list[dict]) -> "ToolStep | TextStep":
        messages = self._base_messages(history, user_msg) + list(turn)
        resp = self._client.messages.create(
            model=self.model, max_tokens=1024, system=system, tools=self._tools,
            tool_choice={"type": "auto"}, messages=messages,
        )
        tool_uses = [b for b in resp.content if b.type == "tool_use"]
        text = "".join(b.text for b in resp.content if b.type == "text").strip()
        if tool_uses:
            return ToolStep([ToolCall(b.id, b.name, dict(b.input)) for b in tool_uses], text=text)
        return TextStep(text)


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
