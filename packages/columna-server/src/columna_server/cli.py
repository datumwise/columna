"""
columna_server.cli — the `columna-server` entry point.

    columna-server mcp --manifolds <dir> [--http HOST:PORT | --http :PORT]

stdio is canonical (Claude Desktop / local agents). `--http` serves streamable-http and is gated by
COLUMNA_MCP_TOKEN: when the env var is set, every request must carry `Authorization: Bearer <token>`
(constant-time compared with hmac.compare_digest); when it is unset, HTTP binds LOOPBACK-ONLY and
warns, never exposing an unauthenticated server on a public interface. stdio needs no auth.
"""
from __future__ import annotations

import argparse
import hmac
import os
import sys
from typing import Optional

from .server import build_server
from .store import ManifoldStore

TOKEN_ENV = "COLUMNA_MCP_TOKEN"


def verify_token(provided: Optional[str], expected: Optional[str]) -> bool:
    """Constant-time bearer check. No token configured -> allow (loopback-only is enforced at bind
    time); token configured -> require an exact match."""
    if not expected:
        return True
    if not provided:
        return False
    return hmac.compare_digest(provided, expected)


def _bearer(authorization: Optional[str]) -> Optional[str]:
    if authorization and authorization.lower().startswith("bearer "):
        return authorization[7:]
    return None


def _parse_http(value: str) -> tuple[str, int]:
    """`:8000` -> ("", 8000); `host:8000` -> ("host", 8000)."""
    host, sep, port = value.rpartition(":")
    if not sep:
        raise SystemExit(f"--http expects HOST:PORT or :PORT, got {value!r}")
    return host, int(port)


def _run_http(mcp, host: str, port: int):
    import uvicorn
    from starlette.middleware.base import BaseHTTPMiddleware
    from starlette.responses import JSONResponse

    token = os.environ.get(TOKEN_ENV)
    app = mcp.streamable_http_app()

    if token:
        bind_host = host or "0.0.0.0"

        class BearerAuth(BaseHTTPMiddleware):
            async def dispatch(self, request, call_next):
                if not verify_token(_bearer(request.headers.get("authorization")), token):
                    return JSONResponse({"error": "unauthorized"}, status_code=401)
                return await call_next(request)

        app.add_middleware(BearerAuth)
        print(f"columna-server: streamable-http on {bind_host}:{port} (bearer auth required)",
              file=sys.stderr)
    else:
        bind_host = "127.0.0.1"     # never expose unauthenticated on a public interface
        print(f"WARNING: {TOKEN_ENV} not set — binding LOOPBACK-ONLY ({bind_host}:{port}), "
              f"no auth. Set {TOKEN_ENV} to serve on a public interface.", file=sys.stderr)

    uvicorn.run(app, host=bind_host, port=port)


def _serve(store, http: Optional[str]):
    print(f"columna-server: loaded manifolds {store.ids()}", file=sys.stderr)
    mcp = build_server(store)
    if http:
        host, port = _parse_http(http)
        _run_http(mcp, host, port)
    else:
        mcp.run(transport="stdio")


def main(argv=None):
    parser = argparse.ArgumentParser(prog="columna-server")
    sub = parser.add_subparsers(dest="command", required=True)

    mcp_cmd = sub.add_parser("mcp", help="run the Columna MCP server over a manifolds directory")
    mcp_cmd.add_argument("--manifolds", required=True, help="directory of <id>/manifold.cml + data.toml")
    mcp_cmd.add_argument("--http", default=None, metavar="HOST:PORT",
                         help="serve streamable-http (default: stdio); gated by COLUMNA_MCP_TOKEN")

    demo_cmd = sub.add_parser(
        "demo", help="run the packaged demo (no path args needed)",
        description="Run the packaged demo Manifold — the benchmark Manifold over a small bundled "
                    "warehouse. With no flags, serves MCP stdio (connect an agent). With --play, "
                    "prints the real clarify -> refuse -> serve wire transcript in-process and exits.")
    demo_cmd.add_argument("--http", default=None, metavar="HOST:PORT",
                          help="serve streamable-http instead of stdio (gated by COLUMNA_MCP_TOKEN)")
    demo_cmd.add_argument("--play", action="store_true",
                          help="print the three-mood wire transcript and exit (no MCP loop)")

    agent_cmd = sub.add_parser(
        "agent", help="natural-language query agent (a true MCP client over the server)",
        description="Chat REPL: your question becomes a proposed Frame-QL query, the server's "
                    "planner disposes, and the four moods drive the conversation. Spawns the MCP "
                    "server over stdio and speaks the protocol — it never touches the engine "
                    "in-process. Defaults to the packaged demo Manifold.")
    agent_cmd.add_argument("--manifolds", default=None,
                           help="directory of <id>/manifold.cml + data.toml (default: packaged demo)")
    agent_cmd.add_argument("--provider", default="anthropic", choices=["anthropic"],
                           help="LLM provider (default: anthropic; needs ANTHROPIC_API_KEY and the "
                                "[agent] extra). The scripted provider is for tests only.")
    agent_cmd.add_argument("--model", default=None,
                           help="override the model (default: $COLUMNA_AGENT_MODEL or claude-opus-4-8)")

    args = parser.parse_args(argv)

    if args.command == "demo":
        from .demo import demo_store, play
        if args.play:
            return play()
        _serve(demo_store(), args.http)
    elif args.command == "agent":
        from .agent.runner import run_agent_cli
        return run_agent_cli(manifolds=args.manifolds, provider_name=args.provider, model=args.model)
    else:
        _serve(ManifoldStore(args.manifolds), args.http)
    return 0


if __name__ == "__main__":
    sys.exit(main())
