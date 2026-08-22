"""
conftest.py — an MCP client harness that drives the real server over stdio, plus the shared
governed-runtime-unit builder the publication-standing tests assemble their fixtures with.

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


# ── the governed runtime unit ────────────────────────────────────────────────────────────────────
# A governed entry needs a lowering receipt binding THIS publication artifact to THIS execution
# image, and the binding is over the files' bytes as shipped — so a receipt can only be written
# AFTER both files exist, and any later edit to either invalidates it. That ordering is the whole
# point, so the helper enforces it rather than letting each test module re-derive it.
def write_lowering_receipt(folder, ref_id: str, ref_version: str, *,
                           artifact_name: str = "governed-publication.json",
                           image_name: str = "manifold.cml",
                           publication_digest: str = None,
                           image_digest: str = None,
                           established_at: str = "2026-08-22T00:00:00Z",
                           receipt_format_version: str = "1.0") -> dict:
    """Write a receipt binding the artifact + image already on disk in ``folder``; return it.

    Digest overrides exist so a test can construct the failure modes (a receipt for other bytes)
    without hand-computing hashes. Defaults digest the real files, which is what a compiler does.
    """
    import json as _json
    from columna_server.lowering_receipt import LOWERING_RECEIPT, digest_file

    folder = str(folder)
    receipt = {
        "receipt_format_version": receipt_format_version,
        "publication_ref": {"manifold_id": ref_id, "version": ref_version},
        "publication_digest": publication_digest or digest_file(os.path.join(folder, artifact_name)),
        "image_digest": image_digest or digest_file(os.path.join(folder, image_name)),
        "compiler": {"name": "test-harness", "version": "0.0.0", "image_format": "cml/1"},
        "established_at": established_at,
    }
    with open(os.path.join(folder, LOWERING_RECEIPT), "w", encoding="utf-8") as f:
        f.write(_json.dumps(receipt))
    return receipt
