"""
columna_server.demo — the packaged demo Manifold + the self-playing three-mood transcript.

The demo data (`demo/benchmark/manifold.cml` + `data.toml` + a small `warehouse/`) ships as
package-data, so `columna-server demo` runs with no path arguments — from a source checkout OR a
clean-venv wheel install. `--play` runs four real asks in-process and pretty-prints the REAL wire
JSON (never a facsimile): clarify -> refuse -> disclose -> serve, ALL FOUR moods in one flow (reframed
for §2c 2026-07-16 — the cross-universe wedge is now a category error, so the tour teaches the moods
through well-posed asks: an underdetermined reduction, a structural out-of-universe refusal, a
served-with-a-material-caveat stock-over-time sum, and a clean serve).
"""
from __future__ import annotations

import json
import os
from importlib.resources import files

from . import tools as T
from .store import ManifoldStore

DEMO_MANIFOLD_ID = "cascadia"
# The recapture wheel (exemplar spec v0.1): clarify E4 -> refuse E2 -> disclose E13 -> serve E5, over the
# Cascadia Manifold. Envelope grammar; `stock`/`buyers` are the Cascadia names (level/visitors retired).
#
# RE-CUT 2026-08-20 (generated-family law, Huayin §9). The four cases are chosen so that the moods are
# distinguished by LAWFULNESS, which is what the reader is actually being taught:
#     serve     lawful, no material condition requiring disclosure
#     disclose  lawful result, a material approximation condition travels with it
#     clarify   two or more LAWFUL interpretations remain, so the reader chooses
#     refuse    the operation is structurally unlawful — no reading of it exists
# The refuse leg moves from the out-of-universe ask (E8) to the blocked temporal stock sum (E2): both
# are honest refusals, but only one teaches that a perfectly computable number can still be one the
# governed law does not grant. E8 stays in the corpus and in the tests.
CLARIFY_Q  = "SELECT avg(aov) AT {cal.year}"          # an inline reduction with no pinned input anchor (E4)
REFUSE_Q   = "SELECT stock.sum AT {store*cal.month}"  # a stock summed across the blocked calendar lineage (E2)
# DISCLOSE_Q was `SELECT stock.sum AT {store*cal.month}` — a stock summed across the blocked calendar
# lineage, served WITH a critical caveat. RE-WITNESSED 2026-08-20 (generated-family law, Huayin §10):
# that ask now REFUSES, because Disclose exists inside the lawful region and cannot legalize an
# operation the governed law does not possess. The replacement is a cleaner Disclose and a truer one:
# a LAWFUL analytical request whose REALIZATION is approximate. The condition must travel with the
# result; the result is still the reader's to use.
DISCLOSE_Q = "SELECT buyers AT {cal.month}"           # lawful ask, approximate realization (E13)
SERVE_Q    = "SELECT aov AT {cal.month}"              # a well-posed ask over one population (E5)


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

    print("Columna demo — four asks, all four moods (real wire JSON).", file=out)

    # 1) clarify — an inline reduction whose input anchor is underdetermined
    clarify = T.query(store, DEMO_MANIFOLD_ID, CLARIFY_Q)
    emit(f"[1/4] clarify    query: {CLARIFY_Q}",
         "Averaging `aov` to calendar month leaves the grain to resolve `aov` at underdetermined. "
         "Columna names the candidate input anchors as alternatives instead of inventing one:",
         clarify)

    # 2) refuse — a structurally unlawful operation (a stock summed across the blocked time axis)
    refuse = T.query(store, DEMO_MANIFOLD_ID, REFUSE_Q)
    emit(f"[2/4] refuse     query: {REFUSE_Q}",
         "Summing `stock` over days into months adds daily snapshots that do not reconcile: the same "
         "units counted once for every day they sat on the shelf. The arithmetic is perfectly "
         "computable — what is missing is the authority to perform it, which `stock`'s author "
         "withheld by declaring `sum BLOCKED { calendar }`. So no number comes back at all, and the "
         "reason and the lawful edits come back instead. Spelling the same operation differently "
         "— `sum(stock.last@day)`, or hidden inside a derived column — refuses identically:",
         refuse)

    # 3) disclose — served, but WITH a material caveat (a lawful ask, approximately realized)
    disclose = T.query(store, DEMO_MANIFOLD_ID, DISCLOSE_Q)
    emit(f"[3/4] disclose   query: {DISCLOSE_Q}",
         "Distinct buyers per month is a lawful question, and Columna answers it — but it counts "
         "distinct customers from a sketch, not by holding every id in memory. So the numbers come "
         "back WITH a material caveat carrying the estimator and its relative error. Disclose is not "
         "a softer refusal: the ask is sound, and the one condition on the answer travels with it "
         "instead of being left for the reader to discover:",
         disclose)

    # 4) serve — a well-posed ask over one population
    serve = T.query(store, DEMO_MANIFOLD_ID, SERVE_Q)
    emit(f"[4/4] serve      query: {SERVE_Q}",
         "Average order value by calendar month — one population, well posed. Columna serves the "
         "numbers:",
         serve)

    print(_hr("Nothing was guessed away, and nothing was answered outside its contract. "
              "One wire, every surface."), file=out)
    return 0
