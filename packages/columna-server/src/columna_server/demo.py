"""
columna_server.demo — the packaged demo Manifold + the self-playing three-mood transcript.

The demo data (`demo/benchmark/manifold.cml` + `data.toml` + a small `warehouse/`) ships as
package-data, so `columna-server demo` runs with no path arguments — from a source checkout OR a
clean-venv wheel install. `--play` runs three real asks in-process and pretty-prints the REAL wire
JSON (never a facsimile): clarify -> refuse -> serve, three of the four moods in one flow (reframed
for §2c 2026-07-16 — the cross-universe wedge is now a category error, so the tour teaches the moods
through well-posed asks: an underdetermined reduction, a structural out-of-universe refusal, and a
clean serve).
"""
from __future__ import annotations

import json
import os
from importlib.resources import files

from . import tools as T
from .store import ManifoldStore

DEMO_MANIFOLD_ID = "benchmark"
CLARIFY_Q = "avg(aov) @ cal.month"      # an inline reduction with no pinned input anchor
REFUSE_Q  = "level.last @ customer"     # inventory has no customers — out of the contracted space
SERVE_Q   = "aov @ cal.month"           # a well-posed ask over one population


def demo_dir() -> str:
    """Filesystem path to the packaged demo manifolds directory.

    pip installs wheels UNZIPPED, so the resource is a concrete directory and we can use its path
    directly — no `as_file` directory extraction, which is only supported for zipped resources on
    3.12+. This keeps the packaged demo working on Python 3.10 (proven by the clean-venv wheel smoke
    in CI). A zipped/zipimport install is unsupported and fails loudly here."""
    path = os.fspath(files("columna_server").joinpath("demo"))
    if not os.path.isdir(path):
        raise RuntimeError(
            f"packaged demo data not found at {path!r} — install columna-server normally "
            f"(pip installs unzipped; a zipimport/zipapp install is unsupported)."
        )
    return path


def demo_store() -> ManifoldStore:
    return ManifoldStore(demo_dir())


def _hr(title: str) -> str:
    return f"\n{'─' * 78}\n{title}\n{'─' * 78}"


def play(out=None) -> int:
    """Run the three-mood wedge in-process and pretty-print the real wire JSON. Returns 0."""
    import sys
    out = out or sys.stdout
    store = demo_store()

    def emit(title, note, wire):
        print(_hr(title), file=out)
        print(note, file=out)
        print(json.dumps(wire, indent=2, ensure_ascii=False), file=out)

    print("Columna demo — three asks, three of the four moods (real wire JSON).", file=out)

    # 1) clarify — an inline reduction whose input anchor is underdetermined
    clarify = T.query(store, DEMO_MANIFOLD_ID, CLARIFY_Q)
    emit(f"[1/3] clarify   query: {CLARIFY_Q}",
         "Averaging `aov` to calendar month leaves the grain to resolve `aov` at underdetermined. "
         "Columna names the candidate input anchors as alternatives instead of inventing one:",
         clarify)

    # 2) refuse — an ask outside the contracted space (inventory has no customers)
    refuse = T.query(store, DEMO_MANIFOLD_ID, REFUSE_Q)
    emit(f"[2/3] refuse    query: {REFUSE_Q}",
         "Inventory is keyed by store and day — it has no customers. The ask addresses outside the "
         "contracted space, so Columna refuses with the reason (never an invented zero):",
         refuse)

    # 3) serve — a well-posed ask over one population
    serve = T.query(store, DEMO_MANIFOLD_ID, SERVE_Q)
    emit(f"[3/3] serve     query: {SERVE_Q}",
         "Average order value by calendar month — one population, well posed. Columna serves the "
         "numbers:",
         serve)

    print(_hr("Nothing was guessed away, and nothing was answered outside its contract. "
              "One wire, every surface."), file=out)
    return 0
