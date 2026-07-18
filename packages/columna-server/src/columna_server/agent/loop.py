"""
columna_server.agent.loop — the agent conversation loop (WP-agent-hands).

The agent has HANDS: within a turn it can call the read-only MCP tools (describe_manifold,
describe_measure, case_manifest, case_chapter, explain) to investigate, then runs the TERMINAL
`query` tool to answer. The provider owns the model call and returns a structured step (a tool
request, or final text); the LOOP owns tool execution (it holds the MCPServerConnection) and feeds
results back, bounded by a small per-turn cycle cap.

The SYSTEM presents every query reply to the human, rendering wire values verbatim (so the agent
never emits a number — grounding is structural; the model's own prose is grounding-guarded). A
clarify is relayed to the human and resolved only by their explicit choice (never auto-picked); a
refuse is fed back so the model may reformulate, still bounded by the cycle cap.
"""
from __future__ import annotations

import json
import os
import re

from .conversation import AGENT, ENGINE, USER, Turn
from .providers import Provider, TextStep, ToolStep

_PROMPT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "system_prompt.md")

# Bound the tool-call cycles per user turn so a runaway (a model that keeps requesting tools, or
# keeps reformulating a refused query) stops gracefully instead of looping forever.
MAX_TOOL_CYCLES = 6

# Cap tool_result payloads handed back to the model (case chapters are a few KB; a describe could be
# larger). Generous enough to deliver a chapter verbatim, bounded against a pathological payload.
_RESULT_CAP = 20000


def load_system_prompt() -> str:
    with open(_PROMPT_PATH, encoding="utf-8") as f:
        return f.read()


def prompt_example_queries() -> list[str]:
    """Every `QUERY:` example line in the system prompt (for the drift-guard parse test)."""
    out = []
    for line in load_system_prompt().splitlines():
        s = line.strip().lstrip("- ").strip()
        if s.startswith("QUERY:"):
            out.append(s[len("QUERY:"):].strip())
    return out


def render_manifold_context(describe: dict) -> str:
    lines = [f"Manifold: {describe['manifold_id']}"]
    lines.append("Universes (a measure lives in exactly one):")
    for u in describe["universes"]:
        pred = f"  WHERE {u['predicate']}" if u["predicate"] else ""
        lines.append(f"  - {u['name']}: over {', '.join(u['base_dimensions'])}{pred}")
    lines.append("Dimension levels (anchors you may address at):")
    lines.append("  " + ", ".join(sorted(d["level"] for d in describe["dimensions"])))
    if describe["edges"]:
        lines.append("Functional edges (finer -> coarser, along a lineage):")
        for e in describe["edges"]:
            lines.append(f"  - {e['frm']} -> {e['to']} ({e['lineage']})")
    lines.append("Measures (name — family members — universe):")
    for m in describe["measures"]:
        fam = "/".join(m["family"]) if m["family"] else "(single)"
        lines.append(f"  - {m['name']}  [{fam}]  on {m['universe']}")
    return "\n".join(lines)


class Agent:
    """Drives one conversation. `run_turn(user_msg)` returns the human-facing replies for the turn.

    Not an MCP server itself — it holds an `MCPServerConnection` and calls tools across the wire.
    """

    def __init__(self, conn, provider: Provider, describe: dict):
        self.conn = conn
        self.provider = provider
        self.system = load_system_prompt().replace("{MANIFOLD_CONTEXT}", render_manifold_context(describe))
        self.history: list[Turn] = []
        self._pending: tuple[list[dict], str] | None = None   # (alternatives, frameql) awaiting a choice

    # ---- turn routing -------------------------------------------------------
    async def run_turn(self, user_msg: str) -> list[str]:
        replies: list[str] = []

        # (A) a clarify is open — this message is the human's CHOICE (never auto-picked)
        if self._pending is not None:
            alts, frameql = self._pending
            self._pending = None
            idx = self._resolve_choice(user_msg, alts)
            self.history.append(Turn(USER, user_msg))
            if idx is None:
                replies.append("I didn't catch which option — reply with its number, or ask something new.")
                # fall through and treat this message as a fresh request
            else:
                universe = (alts[idx].get("apply") or {}).get("universe")
                wire = await self.conn.query(frameql, universe=universe)
                self.history.append(Turn(ENGINE, self._engine_summary(wire)))
                replies.append(self._present(wire, chosen_universe=universe))
                return replies

        # (B) the tool loop — the model investigates, then runs the terminal `query`
        record: list[Turn] = [Turn(USER, user_msg)]   # history additions, committed at the end
        turn: list[dict] = []                          # Anthropic-format tool_use / tool_result msgs
        wire_blob = ""                                 # every query wire seen this turn (grounding source)

        for _ in range(MAX_TOOL_CYCLES):
            step = self.provider.step(self.system, list(self.history), user_msg, turn)

            if isinstance(step, TextStep):
                record.append(Turn(AGENT, step.text or "(no reply)"))
                replies.append(self._ground_text(step.text, wire_blob))
                self.history.extend(record)
                return replies

            # --- a ToolStep: append the assistant turn, then execute each call -------------
            assistant_content: list[dict] = []
            if step.text:
                assistant_content.append({"type": "text", "text": step.text})
                record.append(Turn(AGENT, step.text))
            for c in step.calls:
                assistant_content.append({"type": "tool_use", "id": c.id, "name": c.name, "input": c.input})
                record.append(Turn(AGENT, f"[call {c.name} {json.dumps(c.input, sort_keys=True)}]"))
            turn.append({"role": "assistant", "content": assistant_content})

            results: list[dict] = []
            for c in step.calls:
                if c.name == "query":
                    frameql = c.input.get("frameql", "")
                    wire = await self.conn.query(frameql)
                    wire_blob += repr(wire)
                    record.append(Turn(ENGINE, self._engine_summary(wire)))
                    replies.append(self._present(wire))
                    outcome = wire["outcome"]
                    if outcome == "clarify":
                        self._pending = (self._alternatives(wire), frameql)
                        self.history.extend(record)
                        return replies
                    if outcome in ("serve", "disclose"):
                        self.history.extend(record)
                        return replies
                    # refuse / error — feed the engine note back so the model may reformulate once
                    results.append(self._result_block(c.id, self._engine_summary(wire), is_error=True))
                else:
                    out, is_error = await self._exec_tool(c)
                    record.append(Turn(ENGINE, self._tool_note(c.name, out, is_error)))
                    results.append(self._result_block(c.id, json.dumps(out), is_error=is_error))

            turn.append({"role": "user", "content": results})

        # cycle cap hit — stop gracefully
        record.append(Turn(AGENT, "[tool-call limit reached]"))
        replies.append("(stopped — I reached the tool-call limit for this turn without an answer. "
                       "Try narrowing the question.)")
        self.history.extend(record)
        return replies

    # ---- tool execution (the loop holds the MCP connection) -----------------
    async def _exec_tool(self, call) -> tuple[dict, bool]:
        """Run a NON-terminal tool over the wire; `manifold_id` is injected here (session-fixed).
        Returns (result_dict, is_error) — a wire error becomes a tool_result the model can recover from."""
        mid = self.conn.manifold_id
        try:
            if call.name == "describe_manifold":
                return await self.conn.describe_manifold(mid), False
            if call.name == "describe_measure":
                return await self.conn.describe_measure(mid, call.input["measure"]), False
            if call.name == "case_manifest":
                return await self.conn.case_manifest(), False
            if call.name == "case_chapter":
                return await self.conn.case_chapter(call.input["chapter"]), False
            if call.name == "explain":
                return await self.conn.explain(call.input["frameql"]), False
            return {"error": f"unknown tool '{call.name}'"}, True
        except KeyError as e:
            return {"error": f"missing argument {e} for tool '{call.name}'"}, True
        except RuntimeError as e:                       # an MCP tool error (e.g. unknown measure)
            return {"error": str(e)}, True

    @staticmethod
    def _result_block(tool_use_id: str, text: str, is_error: bool) -> dict:
        return {"type": "tool_result", "tool_use_id": tool_use_id,
                "content": text[:_RESULT_CAP], "is_error": is_error}

    @staticmethod
    def _tool_note(name: str, out: dict, is_error: bool) -> str:
        """A compact, human-readable record of a tool result for the transcript/history."""
        if is_error:
            return f"[tool {name} error: {out.get('error', 'unknown')}]"
        if name == "case_chapter":
            return f"[tool case_chapter -> {out.get('chapter')} \"{out.get('descriptor')}\" " \
                   f"({len(out.get('text', ''))} chars)]"
        if name == "case_manifest":
            return f"[tool case_manifest -> {sorted((out.get('chapters') or {}))}]"
        if name == "describe_measure":
            return f"[tool describe_measure -> {out.get('measure')} on {out.get('universe')}]"
        if name == "describe_manifold":
            return f"[tool describe_manifold -> {len(out.get('measures', []))} measures]"
        if name == "explain":
            return f"[tool explain -> would-be outcome {out.get('outcome')}]"
        return f"[tool {name}]"

    # ---- grounding guard on the model's own prose ---------------------------
    @staticmethod
    def _ground_text(text: str, wire_blob: str) -> str:
        """The agent may relay questions/context, but NEVER surface a figure it didn't get from a
        query. Any multi-digit run in the model's prose that isn't present in this turn's wire
        results is ungrounded — suppress the whole line rather than leak a fabricated number."""
        for num in re.findall(r"\d{2,}", text or ""):
            if num not in wire_blob:
                return ("(couldn't read that as a grounded reply — the agent may only surface "
                        "figures from a query result. Try rephrasing your question.)")
        return text if text else "(no reply)"

    # ---- presentation (verbatim from the wire; the agent adds no numbers) ---
    def _present(self, wire: dict, chosen_universe: str | None = None) -> str:
        outcome = wire["outcome"]
        if outcome in ("serve", "disclose"):
            parts = []
            if chosen_universe:
                parts.append(f"[over universe '{chosen_universe}']")
            for col in wire["columns"]:
                if col["status"] != "served":
                    continue
                parts.append(f"{col['name']}: {_render_values(col)}")
                for d in col["disclosures"]:
                    parts.append(f"  · disclosure [{d['code']}, {d['materiality']}]: {d['detail']}")
            for d in wire["frame"]["disclosures"]:
                parts.append(f"· disclosure [{d['code']}, {d['materiality']}]: {d['detail']}")
            head = "Here is the answer:" if outcome == "serve" else "Answer (with caveats):"
            return head + "\n" + "\n".join(parts)

        if outcome == "clarify":
            col = next(c for c in wire["columns"] if c["status"] == "clarify")
            nr = col["no_result"]
            lines = [f"That question is ambiguous: {nr['detail']}", "Please choose:"]
            for i, a in enumerate(self._alternatives(wire), 1):
                lines.append(f"  [{i}] {a['description']}")
            lines.append("Reply with the number of your choice.")
            return "\n".join(lines)

        # refuse / error
        col = next((c for c in wire["columns"] if c["status"] in ("refuse", "error")), None)
        if col is not None:
            nr = col["no_result"]
            verb = "can't be answered" if outcome == "refuse" else "isn't a valid query"
            return f"That {verb}: {nr['detail']}"
        err = wire.get("error", {})
        return f"That isn't a valid query: {err.get('detail', 'unknown error')}"

    # ---- engine note (compact context for the model's NEXT step) ------------
    def _engine_summary(self, wire: dict) -> str:
        outcome = wire["outcome"]
        if outcome in ("serve", "disclose"):
            cols = ", ".join(c["name"] for c in wire["columns"] if c["status"] == "served")
            mats = [d["code"] for c in wire["columns"] for d in c["disclosures"] if d["materiality"] == "material"]
            mats += [d["code"] for d in wire["frame"]["disclosures"] if d["materiality"] == "material"]
            extra = f"; material disclosures: {mats}" if mats else ""
            return f"engine: outcome={outcome}; served columns [{cols}]{extra}. (values shown to the human)"
        col = next((c for c in wire["columns"] if c["status"] in ("clarify", "refuse", "error")), None)
        nr = col["no_result"] if col else {}
        alts = [a.get("token", a.get("description", "")) for a in self._alternatives(wire)]
        tail = f"; alternatives: {alts}" if alts else ""
        return (f"engine: outcome={outcome}; reason={nr.get('reason')}; detail={nr.get('detail')}"
                f"{tail}. (shown to the human; you do not restate it)")

    # ---- helpers ------------------------------------------------------------
    @staticmethod
    def _alternatives(wire: dict) -> list[dict]:
        for c in wire["columns"]:
            if c.get("no_result") and c["no_result"].get("alternatives"):
                return c["no_result"]["alternatives"]
        return []

    @staticmethod
    def _resolve_choice(user_msg: str, alts: list[dict]) -> int | None:
        s = user_msg.strip().lower()
        m = re.search(r"\d+", s)
        if m:
            i = int(m.group()) - 1
            if 0 <= i < len(alts):
                return i
        for i, a in enumerate(alts):
            uni = (a.get("apply") or {}).get("universe", "")
            if uni and uni.lower() in s:
                return i
        return None


def _render_values(col: dict) -> str:
    if "value" in col:
        return _s(col["value"])
    rows = col.get("values", [])
    out = []
    for r in rows:
        dims = " ".join(f"{k}={_s(v)}" for k, v in r.items() if k != "value")
        out.append(f"{dims}={_s(r['value'])}" if dims else _s(r["value"]))
    return "; ".join(out) if out else "(no rows)"


def _s(v) -> str:
    """Verbatim stringification — no rounding, so grounding matches strictly."""
    return json.dumps(v) if isinstance(v, str) else str(v)
