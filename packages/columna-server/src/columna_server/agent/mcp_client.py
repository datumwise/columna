"""
columna_server.agent.mcp_client — the agent's TRUE MCP client (WP-2.4 architecture #1).

The agent answers ONLY by spawning `columna-server mcp/demo` over stdio and speaking the MCP
protocol. This module imports the MCP client SDK and nothing from columna_core — the engine is
reached across the protocol boundary, never in-process. Bypassing this boundary fails the WP.
"""
from __future__ import annotations

import json
import os
import sys
from contextlib import asynccontextmanager

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def _server_args(manifolds: str | None) -> list[str]:
    # Spawn the server as its own process, exactly as any external agent would.
    if manifolds:
        return ["-m", "columna_server", "mcp", "--manifolds", manifolds]
    return ["-m", "columna_server", "demo"]           # the packaged demo, zero path args


class MCPServerConnection:
    """A live MCP session to a columna server. Read-only tool calls; results are the wire JSON."""

    def __init__(self, session: ClientSession):
        self._s = session
        self.manifold_id: str | None = None

    async def _call(self, name: str, **args) -> dict:
        res = await self._s.call_tool(name, args)
        if res.isError:
            text = res.content[0].text if res.content else "tool error"
            raise RuntimeError(f"MCP tool '{name}' error: {text}")
        return json.loads(res.content[0].text)

    async def tool_names(self) -> list[str]:
        return sorted(t.name for t in (await self._s.list_tools()).tools)

    async def list_manifolds(self) -> dict:
        return await self._call("list_manifolds")

    async def describe_manifold(self, manifold_id: str) -> dict:
        return await self._call("describe_manifold", manifold_id=manifold_id)

    async def describe_measure(self, manifold_id: str, measure: str) -> dict:
        return await self._call("describe_measure", manifold_id=manifold_id, measure=measure)

    async def query(self, frameql: str, universe: str | None = None) -> dict:
        args = {"manifold_id": self.manifold_id, "frameql": frameql}
        if universe:
            args["universe"] = universe
        return await self._call("query", **args)

    async def explain(self, frameql: str, universe: str | None = None) -> dict:
        args = {"manifold_id": self.manifold_id, "frameql": frameql}
        if universe:
            args["universe"] = universe
        return await self._call("explain", **args)


@asynccontextmanager
async def connect(manifolds: str | None = None):
    """Spawn a columna server over stdio and yield a connected MCPServerConnection.

    `manifolds=None` connects to the packaged demo (`columna-server demo`); a path connects to
    `columna-server mcp --manifolds <path>`. The packaged demo's own manifold (Cascadia) is selected
    when hosted; otherwise the first hosted manifold.
    """
    # the packaged demo's own manifold (Cascadia), preferred when hosted. A bare STRING, not an import —
    # the agent process is a TRUE MCP client and must never import the engine (demo.py -> tools -> core).
    _DEMO_MANIFOLD = "cascadia"
    params = StdioServerParameters(command=sys.executable, args=_server_args(manifolds),
                                   env=dict(os.environ))
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            conn = MCPServerConnection(session)
            listed = await conn.list_manifolds()
            ids = [m["manifold_id"] for m in listed["manifolds"]]
            conn.manifold_id = _DEMO_MANIFOLD if _DEMO_MANIFOLD in ids else ids[0]
            yield conn
