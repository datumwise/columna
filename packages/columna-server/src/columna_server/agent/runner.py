"""columna_server.agent.runner — the `columna-server agent` REPL."""
from __future__ import annotations

import asyncio
import sys

from .loop import Agent
from .mcp_client import connect
from .providers import ProviderUnavailable, make_provider


async def _run(manifolds, provider):
    async with connect(manifolds) as conn:
        describe = await conn.describe_manifold(conn.manifold_id)
        agent = Agent(conn, provider, describe)
        print(f"Columna agent — manifold '{conn.manifold_id}', provider '{provider.name}'. "
              f"Ask a question; Ctrl-D to exit.", file=sys.stderr)
        while True:
            try:
                line = input("you> ")
            except EOFError:
                print(file=sys.stderr)
                break
            if not line.strip():
                continue
            for reply in await agent.run_turn(line):
                print(reply)
                print()


def run_agent_cli(manifolds: str | None = None, provider_name: str = "anthropic",
                  model: str | None = None) -> int:
    try:
        provider = make_provider(provider_name, model=model)
    except ProviderUnavailable as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    asyncio.run(_run(manifolds, provider))
    return 0
