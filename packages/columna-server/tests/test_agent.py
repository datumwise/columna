"""
test_agent.py — hermetic tests for the NL query agent (WP-2.4).

All hermetic tests use the `scripted` provider (no API key, no network) against the REAL packaged
demo MCP server over stdio, so the agent loop, the MCP boundary, and wire routing are all exercised
for real — only the LLM is swapped for a fixed script. The live end-to-end test is `@pytest.mark.llm`
and skipped without a key.
"""
import os
import re
import subprocess
import sys

import pytest

from columna_server.agent import ProviderUnavailable, ScriptedProvider
from columna_server.agent.loop import Agent, prompt_example_queries
from columna_server.agent.mcp_client import connect

CLARIFY_Q = "avg(aov) @ cal.month"   # §2c clarify exemplar (input_anchor_ambiguous); the cross-universe
                                     # wedge is now a category error, so the agent's clarify demo moved here


# --- acceptance #1 (part): MCP boundary — the agent never imports the engine ---------------
def test_agent_process_never_imports_columna_core(tmp_path):
    """Run a full scripted wedge conversation in a subprocess and assert columna_core is NOT in
    the AGENT process's sys.modules — it answered purely over the MCP protocol (the child server
    process imports the engine; the agent does not)."""
    script = (
        "import asyncio, sys, json\n"
        "from columna_server.agent.mcp_client import connect\n"
        "from columna_server.agent.loop import Agent\n"
        "from columna_server.agent.providers import ScriptedProvider\n"
        "async def main():\n"
        "    prov = ScriptedProvider(['QUERY: revenue @ region', 'QUERY: " + CLARIFY_Q + "'])\n"
        "    async with connect(None) as conn:\n"
        "        d = await conn.describe_manifold(conn.manifold_id)\n"
        "        a = Agent(conn, prov, d)\n"
        "        await a.run_turn('revenue by region')\n"
        "        await a.run_turn('sell through rate by store and day')\n"
        "asyncio.run(main())\n"
        "assert 'columna_core' not in sys.modules, sorted(m for m in sys.modules if 'columna' in m)\n"
        "print('BOUNDARY OK')\n"
    )
    proc = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True,
                          timeout=120, env=dict(os.environ))
    assert proc.returncode == 0, proc.stderr[-3000:]
    assert "BOUNDARY OK" in proc.stdout


def test_agent_source_has_no_columna_core_import():
    """Static guard: no agent module IMPORTS columna_core (the engine is reached only over MCP).
    Matches import statements, not comments/docstrings that merely name the boundary."""
    import columna_server.agent as pkg

    agent_dir = os.path.dirname(pkg.__file__)
    imp = re.compile(r"^\s*(?:from\s+columna_core|import\s+columna_core)", re.MULTILINE)
    for fn in os.listdir(agent_dir):
        if fn.endswith(".py"):
            src = open(os.path.join(agent_dir, fn), encoding="utf-8").read()
            assert not imp.search(src), f"{fn} imports columna_core — MCP boundary breached"


# --- acceptance #4: material disclosures never dropped -------------------------------------
async def test_material_disclosure_is_surfaced():
    async with connect(None) as conn:
        describe = await conn.describe_manifold(conn.manifold_id)
        agent = Agent(conn, ScriptedProvider(["QUERY: inv: level.sum @ store"]), describe)
        reply = "\n".join(await agent.run_turn("total inventory by store"))
    assert "blocked_reduction" in reply           # the wire code
    assert "material" in reply
    # the plain-language detail is present too
    assert "blocked lineage" in reply or "collapses" in reply


# --- clarify → no silent auto-pick ----------------------------------------------------------
async def test_clarify_relayed_not_auto_picked():
    async with connect(None) as conn:
        describe = await conn.describe_manifold(conn.manifold_id)
        agent = Agent(conn, ScriptedProvider(["QUERY: " + CLARIFY_Q]), describe)

        clarify_reply = "\n".join(await agent.run_turn("average order value trend by month"))
        # the clarify is RELAYED with its candidate alternatives; never auto-picked
        assert "choose" in clarify_reply.lower()
        assert agent._pending is not None            # a choice is genuinely pending
        assert not re.search(r"\d{3,}", clarify_reply)   # no big served figures leaked
    # NOTE (§2c): the mechanical PICK (applying a chosen alternative) rode the universe-apply mechanism
    # — no §2c clarify (input_anchor_ambiguous) carries a universe-apply, so that path is dead code
    # pending OF-4 (server universe-arg removal + the pick-flow redesign). Relay-and-never-auto-pick,
    # the load-bearing behavior, is asserted here; the pick round-trip moves with OF-4.


# --- grounding: every numeral in a served reply comes from the wire ------------------------
async def test_grounding_numerals_subset_of_wire():
    async with connect(None) as conn:
        describe = await conn.describe_manifold(conn.manifold_id)
        agent = Agent(conn, ScriptedProvider(["QUERY: revenue @ region"]), describe)
        reply = "\n".join(await agent.run_turn("revenue by region"))
        wire = await conn.query("revenue @ region")
    wire_blob = repr(wire)
    nums = re.findall(r"-?\d+\.\d+|-?\d+", reply)
    assert nums, "expected served numbers in the reply"
    for n in nums:
        assert n in wire_blob, f"numeral {n} in reply is not present in the wire result (ungrounded)"


async def test_agent_cannot_surface_a_fabricated_number():
    """If the provider emits a bare number/prose (not QUERY:/ASK:), the agent refuses to present it —
    it only ever prints wire-sourced results. Structural grounding."""
    async with connect(None) as conn:
        describe = await conn.describe_manifold(conn.manifold_id)
        agent = Agent(conn, ScriptedProvider(["The total revenue is 999999."]), describe)
        reply = "\n".join(await agent.run_turn("what's the total revenue?"))
    assert "999999" not in reply
    assert "couldn't read" in reply.lower()


# --- refuse explained ----------------------------------------------------------------------
async def test_refuse_is_explained_with_no_invented_value():
    # after the refuse, the agent is permitted ONE reformulation — here it asks the human instead
    script = ["QUERY: i: level.last @ product",
              "ASK: level isn't defined per product; want inventory by store instead?"]
    async with connect(None) as conn:
        describe = await conn.describe_manifold(conn.manifold_id)
        agent = Agent(conn, ScriptedProvider(script), describe)
        replies = await agent.run_turn("inventory by product")
    joined = "\n".join(replies)
    assert "can't be answered" in joined            # the refuse was explained
    assert "universe" in joined.lower()
    assert not re.search(r"\d{3,}", joined)         # no fabricated figure
    assert len(replies) == 2 and replies[1].startswith("level isn't defined")  # one reformulation (an ASK)


# --- nonexistent measure: model asks; engine/formatter backstop ----------------------------
async def test_engine_and_formatter_backstop_a_fabricated_measure():
    """Even if the model fabricates a measure name, the engine rejects it (unknown column) and the
    formatter presents it as an invalid query — no fake number ever reaches the human. This is the
    deterministic backstop behind the live 'model asks instead of inventing' behavior."""
    script = ["QUERY: churn_rate @ region",
              "ASK: I don't have a churn measure — did you mean revenue by region?"]
    async with connect(None) as conn:
        describe = await conn.describe_manifold(conn.manifold_id)
        agent = Agent(conn, ScriptedProvider(script), describe)
        replies = await agent.run_turn("what's the churn rate by region?")
    joined = "\n".join(replies)
    assert "isn't a valid query" in joined         # engine + formatter backstop
    assert "churn_rate" in joined                  # names the unknown column
    assert not re.search(r"\d{3,}", joined)        # no fabricated figure reached the human
    assert replies[-1].startswith("I don't have")  # the one post-refuse reformulation was an ASK


@pytest.mark.llm
@pytest.mark.skipif(not os.environ.get("ANTHROPIC_API_KEY"), reason="no ANTHROPIC_API_KEY")
async def test_live_asks_on_a_plausible_but_fake_metric():
    """A real model, asked for a metric the manifold does not have (customer churn), must NOT invent
    it: it asks which real measure is meant (honest-naming) — or proposes a fake one that the engine
    backstops — but never fabricates a number."""
    from columna_server.agent.providers import AnthropicProvider
    async with connect(None) as conn:
        describe = await conn.describe_manifold(conn.manifold_id)
        agent = Agent(conn, AnthropicProvider(), describe)
        reply = "\n".join(await agent.run_turn("What's the customer churn rate by region?"))
    low = reply.lower()
    assert "here is the answer" not in low                 # did not serve a fabricated metric
    assert not re.search(r"\d{3,}", reply)                 # no invented figure
    assert ("?" in reply or "isn't a valid query" in low   # it asked, or the engine backstopped a fake
            or "don't have" in low or "which" in low or "no " in low)


# --- provider missing key -------------------------------------------------------------------
def test_anthropic_provider_missing_key_errors_to_demo(monkeypatch):
    from columna_server.agent.providers import AnthropicProvider
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    with pytest.raises(ProviderUnavailable) as e:
        AnthropicProvider()
    assert "demo --play" in str(e.value)


# --- prompt/grammar drift guard: every prompt example parses to a non-error outcome ---------
async def test_prompt_examples_parse_against_the_engine():
    examples = prompt_example_queries()
    assert examples, "expected QUERY: examples in system_prompt.md"
    async with connect(None) as conn:
        for q in examples:
            wire = await conn.query(q)
            assert wire["outcome"] != "error", f"prompt example '{q}' no longer parses: {wire}"


# --- live smoke (skipped without a key) ----------------------------------------------------
@pytest.mark.llm
@pytest.mark.skipif(not os.environ.get("ANTHROPIC_API_KEY"), reason="no ANTHROPIC_API_KEY")
async def test_live_wedge_conversation():
    """End-to-end with a real model: it must emit well-formed QUERY:/ASK: lines and let the four
    moods route. The ratio is described in terms the manifold can map (revenue over inventory), so
    the model forms it and the engine clarifies on the cross-universe population."""
    from columna_server.agent.providers import AnthropicProvider
    async with connect(None) as conn:
        describe = await conn.describe_manifold(conn.manifold_id)
        agent = Agent(conn, AnthropicProvider(), describe)
        r1 = "\n".join(await agent.run_turn("How much did each region bring in?"))
        r2 = "\n".join(await agent.run_turn(
            "Now take revenue over the end-of-period inventory level, broken out by store and day."))
    # turn 1 served real numbers (which came from the wire)
    assert any(ch.isdigit() for ch in r1) and "revenue" in r1
    # turn 2 routed a genuine outcome without fabricating a rate: a clarify relay (the expected
    # path — the ratio spans two universes) or an honest ASK; never an invented number.
    low = r2.lower()
    assert ("population" in low or "choose" in low) or low.startswith(("i ", "which", "did", "do "))
