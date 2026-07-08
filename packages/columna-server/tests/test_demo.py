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
    assert '"contract_version": "1"' in out
    # the three moods appear, in order (clarify -> refuse -> disclose)
    i_clar = out.find('"outcome": "clarify"')
    i_ref = out.find('"outcome": "refuse"')
    i_disc = out.find('"outcome": "disclose"')
    assert -1 < i_clar < i_ref < i_disc, (i_clar, i_ref, i_disc)
    # the disclose frame carries the material coverage caveat
    assert "denominator_population" in out


async def test_demo_serves_stdio_with_no_path_args():
    params = StdioServerParameters(command=sys.executable, args=["-m", "columna_server", "demo"],
                                   env=dict(os.environ))
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = sorted(t.name for t in (await session.list_tools()).tools)
            res = await session.call_tool("list_manifolds", {})
            manifolds = json.loads(res.content[0].text)["manifolds"]
    assert tools == ["describe_manifold", "describe_measure", "explain", "list_manifolds", "query"]
    assert manifolds[0]["manifold_id"] == "benchmark"
