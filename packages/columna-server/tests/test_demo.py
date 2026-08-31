"""
test_demo.py — the packaged demo: `demo --play` prints the three-mood transcript, and `demo` serves
MCP stdio with zero path arguments.
"""
import json
import os
import subprocess
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def test_demo_play_prints_three_moods_in_order():
    proc = subprocess.run([sys.executable, "-m", "columna_server", "demo", "--play"],
                          capture_output=True, text=True, timeout=120, env=dict(os.environ))
    assert proc.returncode == 0, proc.stderr[-2000:]
    out = proc.stdout
    assert '"contract_version": "4"' in out
    # the three moods appear, in order (clarify -> refuse -> serve; §2c reframe 2026-07-16)
    i_clar = out.find('"outcome": "clarify"')
    i_ref = out.find('"outcome": "refuse"')
    i_serve = out.find('"outcome": "serve"')
    assert -1 < i_clar < i_ref < i_serve, (i_clar, i_ref, i_serve)


async def test_demo_serves_stdio_with_no_path_args():
    params = StdioServerParameters(command=sys.executable, args=["-m", "columna_server", "demo"],
                                   env=dict(os.environ))
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = sorted(t.name for t in (await session.list_tools()).tools)
            res = await session.call_tool("list_manifolds", {})
            manifolds = json.loads(res.content[0].text)["manifolds"]
    assert tools == ["case_chapter", "case_manifest", "check_frame_query", "describe_manifold",
                     "describe_measure", "discovery", "execute_frame_query", "explain",
                     "frame_ql_grammar", "get_evidence", "list_manifolds", "manifold_status", "query"]
    # the case demo's cascadia .cml carries no SOURCE_MANIFOLD → a legacy runtime row (runtime_id)
    assert "cascadia" in [m.get("runtime_id") for m in manifolds]


# ---- THE cp1252 CLASS GUARD (0.13.2) -----------------------------------------------------------
#
# The windows-latest CI leg, on its FIRST run, found `demo --play` dying with UnicodeEncodeError on
# its opening line — before a single mood printed. Cause: our output is legitimately non-ASCII (the
# rules are U+2500, the prose uses em-dashes, and the wire JSON is dumped `ensure_ascii=False` on
# purpose), while Python falls back to the LOCALE encoding — cp1252 on default en-US Windows — the
# moment stdout is a pipe rather than a console. An interactive run looked fine; every piped one died.
#
# This test reproduces that WITHOUT NEEDING WINDOWS. PYTHONIOENCODING is exactly the knob Python uses
# to pick the stdio codec, so forcing it to cp1252 on any platform recreates the failing condition.
# The Windows leg still runs in CI and is the real proof; this is the fast guard that fails in the
# unit suite, on every developer's machine, in under a second — so the class cannot come back
# silently between full CI runs.

def test_demo_play_survives_a_cp1252_stdio_locale():
    """The whole transcript must survive a legacy-codepage stdout, not just its ASCII prefix."""
    env = dict(os.environ, PYTHONIOENCODING="cp1252")
    proc = subprocess.run([sys.executable, "-m", "columna_server", "demo", "--play"],
                          capture_output=True, timeout=120, env=env)

    assert proc.returncode == 0, (
        "demo --play died under a cp1252 stdio locale — the Windows piped-stdout case:\n"
        + proc.stderr.decode("utf-8", "replace")[-2000:])

    # Decodes as UTF-8 because the CLI DECLARES utf-8 on stdout rather than inheriting the locale.
    out = proc.stdout.decode("utf-8")

    # The non-ASCII characters that caused the crash must actually still be there. Asserting only
    # "it exited 0" would pass just as well if someone "fixed" this by stripping them to ASCII —
    # which would make the demo lie about what the wire carries.
    assert "─" in out, "the U+2500 rules are gone — stripped, not fixed"
    assert "—" in out, "the em-dashes are gone — stripped, not fixed"

    # And the transcript is whole: all four moods, in contract order.
    positions = [out.find('"outcome": "%s"' % mood)
                 for mood in ("clarify", "refuse", "disclose", "serve")]
    assert -1 not in positions, positions
    assert positions == sorted(positions), positions


# ── the seed→mood gate (2026-08-20, after the v0.15.0 release incident) ──────────────────────────
# The published columna-server 0.8.2 running against columna-core 0.15.0 printed
#     [3/4] disclose   query: SELECT stock.sum AT {store*cal.month}
#     "outcome": "refuse"
# and EXITED 0. Every leg's heading declares a mood; nothing checked that the query still earns it.
# `test_demo_play_prints_three_moods_in_order` above could not catch it either — it asserts that the
# four mood STRINGS appear in order anywhere in the output, which a refusing disclose leg still
# satisfies as long as some other leg happens to print each word.

def test_every_seeded_leg_earns_the_mood_it_declares():
    """The four-mood contract, asserted per leg rather than by counting words in the transcript."""
    from columna_server.demo import seed_integrity

    assert seed_integrity() == [], (
        "a seeded demo leg no longer returns its declared mood — the shipped four-mood tour would "
        "print a contradiction. Re-cut the seed or fix the law, but do not let them disagree."
    )


def test_play_exits_non_zero_when_a_seed_no_longer_earns_its_mood(monkeypatch):
    """The gate must FAIL the command, not just report. This is the regression for the incident.

    Rather than fabricating a stale package, we point one seed at a query that earns a different
    mood — the same shape of disagreement the stale 0.8.2 seeds produced against 0.15.0.
    """
    import io

    from columna_server import demo

    # `SELECT stock.sum AT {store*cal.month}` REFUSES under the generated-family law — exactly the
    # ask the stale 0.8.2 package still declared as its `disclose` witness.
    monkeypatch.setattr(demo, "DISCLOSE_Q", "SELECT stock.sum AT {store*cal.month}")
    buf = io.StringIO()
    rc = demo.play(out=buf)
    text = buf.getvalue()

    assert rc == 1, "a demo leg that does not earn its mood must fail the command"
    assert "DEMO INTEGRITY FAILURE" in text
    assert "declared 'disclose' but the engine returned 'refuse'" in text


def test_seed_integrity_names_both_sides_of_a_mismatch(monkeypatch):
    """A failure has to be actionable: which leg, which query, and what it actually returned."""
    from columna_server import demo

    monkeypatch.setattr(demo, "SEED_MOODS",
                        (("disclose", "SELECT stock.sum AT {store*cal.month}"),))
    bad = demo.seed_integrity()
    assert bad == [("disclose", "SELECT stock.sum AT {store*cal.month}", "refuse")]


def test_a_coherent_play_says_so_explicitly():
    """Silence is not evidence. A passing run states that the contract held."""
    import io

    from columna_server.demo import play

    buf = io.StringIO()
    assert play(out=buf) == 0
    assert "demo seed integrity OK" in buf.getvalue()
