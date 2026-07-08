"""
columna_server.demo — the packaged demo Manifold + the self-playing three-mood transcript.

The demo data (`demo/benchmark/manifold.cml` + `data.toml` + a small `warehouse/`) ships as
package-data, so `columna-server demo` runs with no path arguments — from a source checkout OR a
clean-venv wheel install. `--play` runs the proven wedge in-process and pretty-prints the REAL wire
JSON (never a facsimile): clarify -> refuse -> disclose, three of the four moods in one flow.
"""
from __future__ import annotations

import json
import os
from importlib.resources import files

from . import tools as T
from .store import ManifoldStore

DEMO_MANIFOLD_ID = "benchmark"
WEDGE = "sell_through_rate: revenue / level.last @ store, day"
SEPARATE = "revenue: revenue, inv: level.last @ store, day"


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

    print("Columna demo — one question, three of the four moods (real wire JSON).", file=out)

    # 1) clarify — a rate over two populations has no single determinate value
    clarify = T.query(store, DEMO_MANIFOLD_ID, WEDGE)
    emit(f"[1/3] clarify   query: {WEDGE}",
         "The rate spans two populations, so its population is ambiguous. Columna names the "
         "candidate populations as substitutable alternatives instead of inventing a number:",
         clarify)

    # 2) refuse — apply a pin token; the other operand is out-of-domain there
    pin = clarify["columns"][0]["no_result"]["alternatives"][0]["apply"]["universe"]
    refuse = T.query(store, DEMO_MANIFOLD_ID, WEDGE, universe=pin)
    emit(f"[2/3] refuse    query: {WEDGE}  ON UNIVERSE '{pin}'",
         f"Pinning '{pin}' makes the other operand out-of-domain — so there is no faithful rate "
         "over that population. Columna refuses with the reason (still no guess):",
         refuse)

    # 3) disclose — reformulate into separate columns over the union population
    disclose = T.query(store, DEMO_MANIFOLD_ID, SEPARATE)
    emit(f"[3/3] disclose  query: {SEPARATE}",
         "Reformulated as separate columns over the union population: the numbers are SERVED, with "
         "a material coverage caveat riding on the frame (materiality, not severity, makes this "
         "`disclose`):",
         disclose)

    print(_hr("The ambiguity was never guessed away. One contract, every surface."), file=out)
    return 0
