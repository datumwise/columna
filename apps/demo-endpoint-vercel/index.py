"""
The read-only Columna demo endpoint (single Vercel entrypoint, routed by path).

  POST /query (or /api/query)   {"frameql": "<q>", "universe": <str|null>}  -> disclosure wire JSON
  GET  /query                                                               -> {ok, contract, ...}
  GET  /healthz                                                             -> ok
  GET  /                                                                    -> {ok, ...} (info)

It serves REAL shipped-package wire (captured in _wire/precomputed.json by scripts/generate.py
running the actual engine). The full engine can't run here — polars+pyarrow+duckdb exceed Vercel's
250MB limit — so we serve genuine captured wire, never a facsimile. The fool-it surface
("<name> @ store, day") is finite and fully covered:

  * exact match against a captured query  -> that real wire
  * a single unknown measure name         -> the engine's real unknown-column error wire, with the
                                             user's own typed token substituted (deterministic
                                             "unknown column '<token>'" — the engine's own format)
  * an envelope violation (e.g. SQL)       -> the real Frame-QL syntax-error wire (vendored parser)
  * anything else we did not precompute    -> an honest "not available on this static endpoint"
                                             error (never a fabricated number)

Read-only by construction; no token; no write path. CORS scoped to the site origins.
"""
from __future__ import annotations

import json
import os
import re
import sys
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "vendor"))

from frameql import FrameQLSyntaxError, parse_frameql  # noqa: E402  (vendored, pure stdlib)

with open(os.path.join(ROOT, "_wire", "precomputed.json"), encoding="utf-8") as _f:
    _DB = json.load(_f)

_ENTRIES = _DB["entries"]
_UNKNOWN = _DB["unknown_template"]
_SENTINEL = _UNKNOWN["token_sentinel"]
_META = _DB["meta"]
_CONTRACT = _META["contract_version"]
_MEASURE_INDEX = set(_META["measure_index"])

_ALLOWED_ORIGIN = re.compile(
    r"^(https://datumwise\.ai|https://[a-z0-9-]+\.vercel\.app|http://(localhost|127\.0\.0\.1)(:\d+)?)$")


def _key(frameql: str, universe):
    return f"{universe or ''}||{(frameql or '').strip()}"


def _syntax_error_wire(detail: str, universe):
    return {"contract_version": _CONTRACT, "outcome": "error",
            "frame": {"anchor": [], "universe": universe, "rollup_severity": "none", "disclosures": []},
            "columns": [], "error": {"reason": "frameql_syntax", "detail": detail}}


def _unavailable_wire(detail: str, universe):
    return {"contract_version": _CONTRACT, "outcome": "error",
            "frame": {"anchor": [], "universe": universe, "rollup_severity": "none", "disclosures": []},
            "columns": [], "error": {"reason": "not_precomputed", "detail": detail}}


def _substitute(obj, token: str):
    """Deep-copy the unknown-column template, replacing the sentinel with the user's typed token."""
    if isinstance(obj, str):
        return obj.replace(_SENTINEL, token)
    if isinstance(obj, list):
        return [_substitute(x, token) for x in obj]
    if isinstance(obj, dict):
        return {k: _substitute(v, token) for k, v in obj.items()}
    return obj


def resolve(frameql: str, universe) -> dict:
    # 1) exact captured wire
    hit = _ENTRIES.get(_key(frameql, universe))
    if hit is not None:
        return hit["wire"]

    # 2) parse the envelope (vendored real parser) — honest SQL / syntax rejection
    try:
        anchor, columns = parse_frameql(frameql)
    except FrameQLSyntaxError as e:
        return _syntax_error_wire(str(e), universe)

    # 3) the fool-it shape: a single bare measure over the "store, day" anchor
    if (not universe and len(columns) == 1 and anchor == ("store", "day")):
        name, expr = columns[0]
        token = expr.strip()
        # a bare, simple identifier that isn't a real measure -> the real unknown-column refusal
        if name == expr and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", token) and token not in _MEASURE_INDEX:
            return _substitute(_UNKNOWN["wire"], token)

    # 4) uncovered by this static endpoint — honest, no fabricated result
    return _unavailable_wire(
        "this static demo endpoint serves the packaged benchmark manifold's precomputed wire; "
        "this query is outside its captured surface (live arbitrary-query compute is the Fly upgrade)",
        universe)


class handler(BaseHTTPRequestHandler):
    def _cors(self):
        origin = self.headers.get("Origin", "")
        if _ALLOWED_ORIGIN.match(origin):
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Vary", "Origin")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Accept")
        self.send_header("Access-Control-Max-Age", "86400")

    def _text(self, code: int, body: str, ctype="text/plain; charset=utf-8"):
        raw = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Cache-Control", "no-store")
        self._cors()
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def _json(self, code: int, payload: dict):
        self._text(code, json.dumps(payload, ensure_ascii=False), "application/json; charset=utf-8")

    def _path(self) -> str:
        return urlparse(self.path).path.rstrip("/") or "/"

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        path = self._path()
        if path == "/healthz":
            return self._text(200, "ok\n")
        # info surface for / and /query and /api/query
        return self._json(200, {"ok": True, "contract_version": _CONTRACT, "manifold": _META["manifold"],
                                "measures": _META["measure_index"], "note": _META["note"]})

    def do_POST(self):
        path = self._path()
        if path not in ("/query", "/api/query", "/"):
            return self._json(404, {"error": {"reason": "not_found", "detail": f"no route {path}"}})
        try:
            length = int(self.headers.get("Content-Length") or 0)
            raw = self.rfile.read(length) if length else b"{}"
            req = json.loads(raw or b"{}")
        except (ValueError, TypeError):
            return self._json(400, {"error": {"reason": "bad_request", "detail": "body must be JSON"}})

        frameql = req.get("frameql")
        universe = req.get("universe")
        if not isinstance(frameql, str) or not frameql.strip():
            return self._json(400, {"error": {"reason": "bad_request", "detail": "'frameql' (string) is required"}})
        if universe is not None and not isinstance(universe, str):
            return self._json(400, {"error": {"reason": "bad_request", "detail": "'universe' must be a string or null"}})

        return self._json(200, resolve(frameql, universe))
