"""
RETIRED SURFACE — the Columna demo query endpoint (P1-32, 2026-09-02).

This entrypoint answers every request with **410 Gone** and no analytical payload. It computes
nothing, reads no data file, and asserts nothing about current Columna behaviour.

WHY. What used to live here was a precomputed capture: real wire produced on 2026-07-13 by running
columna-core 0.7.8 / columna-server 0.1.0 over the `benchmark` manifold, committed as
`_wire/precomputed.json` and served verbatim. It was built as a LIVE surface — "regenerate on any
package bump" — and then nothing regenerated it. By 2026-09-02 the capture disagreed with the system
in every dimension that mattered: wire contract 1 vs 4; the `benchmark` manifold vs the packaged
demo; the terse `<measure> @ <anchor>` Frame-QL form, retired in 0.9.0, in every recorded query;
four of six advertised measures no longer existing; and `region_label` still served as the NULLs that
P1-18 repaired at the declaration level. Its generator could not even be re-run — it called
`query(..., universe=...)`, an argument the server no longer has.

RULED (Huayin, 2026-09-02): retire the surface; do not migrate it. *"Do not invent current semantics
to preserve a dead demo contract."* The generator, the vendored parser and the 6.9 MB capture were
deleted rather than updated, because a stale generated artifact must not keep authority merely by
being committed and served.

WHAT THIS FILE DELIBERATELY DOES NOT DO. It does not state the current contract version, the current
package versions, or the current demo manifold. A committed file that asserts current facts is the
exact mechanism that failed here: it would be right on the day it was written and quietly wrong
afterwards, with nothing to catch the drift. It states only what is permanently true — that this
surface is retired and what it used to serve — and points at the package for anything current.
"""
from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler

RETIREMENT = {
    "retired": True,
    "surface": "Columna demo query endpoint (precomputed wire)",
    "retired_on": "2026-09-02",
    "row": "P1-32",
    "detail": (
        "This endpoint is retired and serves no analytical result. It formerly replayed wire "
        "captured on 2026-07-13 from columna-core 0.7.8 / columna-server 0.1.0 on wire contract 1, "
        "for the 'benchmark' manifold, in the terse '<measure> @ <anchor>' Frame-QL form retired in "
        "0.9.0. None of that describes current Columna behaviour, and it is not being migrated: a "
        "generated artifact does not acquire authority by being committed and served."
    ),
    "current_behaviour": (
        "install the package — `pip install columna` — or see https://datumwise.ai. This endpoint "
        "deliberately records no version, contract or manifold of its own, so it cannot go stale "
        "a second time."
    ),
}


class handler(BaseHTTPRequestHandler):
    """Every method, every path: 410 Gone with the retirement notice. There is no 200 here."""

    def _gone(self):
        raw = json.dumps(RETIREMENT, ensure_ascii=False, indent=1).encode("utf-8")
        self.send_response(410)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        # Permissive by design: any lingering client should be able to READ why it is gone rather
        # than see a CORS failure. There is no data here to protect.
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Accept")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_OPTIONS(self):
        self._gone()

    def do_GET(self):
        self._gone()

    def do_POST(self):
        self._gone()

    def do_HEAD(self):
        self._gone()
