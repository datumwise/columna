"""
columna_server.agent.loop — the agent conversation loop (WP-2.4 architecture #2).

user NL → provider proposes ONE Frame-QL query (or an ASK) → the MCP `query` tool → the outcome
routes the turn. The SYSTEM presents every server reply to the human, rendering wire values verbatim
(so the agent never emits a number — grounding is structural). A clarify is relayed to the human and
resolved only by their explicit choice (never auto-picked); a refuse permits ONE reformulation.
"""
from __future__ import annotations

import json
import os
import re

from .conversation import AGENT, ENGINE, USER, Turn
from .providers import Provider

_PROMPT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "system_prompt.md")


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


_NUM = re.compile(r"-?\d+(?:\.\d+)?")


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

        # (B) fresh proposal — allow exactly ONE reformulation after a refuse/error
        reformulations_left = 1
        current = user_msg
        while True:
            line = self.provider.propose(self.system, list(self.history), current)
            self.history.append(Turn(USER, current))
            self.history.append(Turn(AGENT, line))
            kind, body = _parse_line(line)

            if kind == "ask":
                replies.append(body)
                return replies
            if kind == "invalid":
                replies.append("(couldn't read that as a Frame-QL query — try rephrasing your question)")
                return replies

            wire = await self.conn.query(body)
            self.history.append(Turn(ENGINE, self._engine_summary(wire)))
            replies.append(self._present(wire))
            outcome = wire["outcome"]

            if outcome == "clarify":
                self._pending = (self._alternatives(wire), body)
                return replies
            if outcome in ("refuse", "error") and reformulations_left > 0:
                reformulations_left -= 1
                current = ("[reformulate] The previous query was not answerable (see the engine "
                           "note). If a reformulation addresses the reason, propose exactly one; "
                           "otherwise ask the human or stop.")
                continue
            return replies

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

    # ---- engine note (compact context for the model's NEXT proposal) --------
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


def _parse_line(line: str) -> tuple[str, str]:
    s = line.strip()
    if s.startswith("QUERY:"):
        return "query", s[len("QUERY:"):].strip()
    if s.startswith("ASK:"):
        return "ask", s[len("ASK:"):].strip()
    return "invalid", s
