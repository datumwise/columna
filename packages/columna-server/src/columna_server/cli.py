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


def main(argv=None):
    parser = argparse.ArgumentParser(prog="columna-server")
    sub = parser.add_subparsers(dest="command", required=True)
    mcp_cmd = sub.add_parser("mcp", help="run the Columna MCP server")
    mcp_cmd.add_argument("--manifolds", required=True, help="directory of <id>/manifold.cml + data.toml")
    mcp_cmd.add_argument("--http", default=None, metavar="HOST:PORT",
                         help="serve streamable-http (default: stdio); gated by COLUMNA_MCP_TOKEN")
    args = parser.parse_args(argv)

    store = ManifoldStore(args.manifolds)
    print(f"columna-server: loaded manifolds {store.ids()}", file=sys.stderr)
    mcp = build_server(store)

    if args.http:
        host, port = _parse_http(args.http)
        _run_http(mcp, host, port)
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
