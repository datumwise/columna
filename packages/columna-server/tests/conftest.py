"""
conftest.py — an MCP client harness that drives the real server over stdio.

The client is exposed as an async context-manager *factory* (`mcp_session`) rather than a yield
fixture: `stdio_client`/`ClientSession` open anyio cancel scopes that must be entered and exited in
the same task, so each test enters them itself via `async with mcp_session() as client:`. Tool
results come back as a JSON content block; `client.call(...)` parses it into the wire dict.
"""
import json
import os
import sys
from contextlib import asynccontextmanager

import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

_HERE = os.path.dirname(os.path.abspath(__file__))
FIXTURE_MANIFOLDS = os.path.join(_HERE, "fixtures", "manifolds")


class Client:
    def __init__(self, session: ClientSession):
        self._s = session

    async def list_tools(self):
        return [t.name for t in (await self._s.list_tools()).tools]

    async def call(self, name: str, **args) -> dict:
        res = await self._s.call_tool(name, args)
        return json.loads(res.content[0].text)

    async def call_raw(self, name: str, **args):
        return await self._s.call_tool(name, args)


@asynccontextmanager
async def _mcp_session():
    params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "columna_server", "mcp", "--manifolds", FIXTURE_MANIFOLDS],
        env=dict(os.environ),
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            yield Client(session)


@pytest.fixture
def mcp_session():
    """Returns the async context-manager factory; a test does `async with mcp_session() as client`."""
    return _mcp_session
