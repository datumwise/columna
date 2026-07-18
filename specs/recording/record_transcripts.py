"""Live recording harness for the two ch3 conversations (Cascadia case demo).

Protocol (ratified): human turns are SCRIPTED verbatim from ch3; agent turns are LIVE (real model via
the AnthropicProvider, real MCP, real tools). The full history (USER/AGENT/ENGINE, incl. every visible
tool call) is captured. Nothing is fabricated. The API key is read from env only; it is never printed.

Take-2 amendment (Huayin, 2026-07-18): the MANAGER is now a TWO-turn conversation — the agent's clarify
is part of the story (the demo world has no clock; the assistant asks rather than guesses), and the
human answers it specifically. New-hire script unchanged.

Run:  ANTHROPIC_API_KEY=... python specs/recording/record_transcripts.py > take2.json
"""
import asyncio
import json
import os
import sys

from columna_server.agent import Agent
from columna_server.agent.mcp_client import connect
from columna_server.agent.providers import AnthropicProvider


def dump_history(history) -> list:
    return [{"role": t.role, "text": t.text} for t in history]


async def conversation(label: str, human_turns: list[str]) -> dict:
    async with connect(None) as conn:            # cascadia demo over stdio MCP
        describe = await conn.describe_manifold(conn.manifold_id)
        agent = Agent(conn, AnthropicProvider(), describe)
        turns = []
        for msg in human_turns:
            replies = await agent.run_turn(msg)
            turns.append({"human": msg, "replies": replies})
        return {"label": label, "manifold": conn.manifold_id,
                "turns": turns, "history": dump_history(agent.history)}


async def main() -> int:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("NO KEY — refusing to fabricate", file=sys.stderr)
        return 2
    out = {}
    # Conversation A — the manager (TWO NL turns; the clarify is part of the story). Turn 1 verbatim
    # from ch3; turn 2 answers the agent's clarify specifically (there is no "today" in the demo world).
    out["manager"] = await conversation(
        "manager", ["How did the west do last quarter?", "West, Q4 2025."])
    # Conversation B — the new hire (two NL turns, scripted verbatim from ch3; unchanged)
    out["new_hire"] = await conversation(
        "new_hire", ["How are we doing on returns?", "By month, this year."])
    json.dump(out, sys.stdout, indent=2, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
