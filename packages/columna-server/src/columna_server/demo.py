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

# THE SEED->MOOD CONTRACT, and the gate that enforces it (Huayin, 2026-08-20, after the v0.15.0
# release incident). Each leg below DECLARES a mood in its own heading. Until now nothing checked
# that the query still EARNS it: `columna-server demo --play` printed
#
#     [3/4] disclose   query: SELECT stock.sum AT {store*cal.month}
#     "outcome": "refuse"
#
# and exited 0. That was the published columna-server 0.8.2 (whose seeds predate the generated-family
# law) running against columna-core 0.15.0 (which refuses the ask) — the flagship first-run tour,
# publicly self-contradicting, with no non-zero exit anywhere to notice it.
#
# The first-run surface is the one place a stranger meets the four moods. If it can lie, nothing
# downstream matters. So the demo now VERIFIES itself: a leg whose actual outcome differs from its
# declared mood fails the command. `scripts/assert_demo_play.py` and the website transcript
# generator stay fail-closed too — this is the first line, not the only one.
SEED_MOODS = (
    ("clarify",  CLARIFY_Q),
    ("refuse",   REFUSE_Q),
    ("disclose", DISCLOSE_Q),
    ("serve",    SERVE_Q),
)


def seed_integrity(store=None) -> list:
    """Run every seeded leg and return the mismatches: [(declared, query, actual), ...].

    Empty means the four-mood contract holds. Importable so tests and release gates can assert it
    without parsing printed output — the printed transcript is for humans, this is for machines.
    """
    store = store or demo_store()
    bad = []
    for declared, q in SEED_MOODS:
        got = T.query(store, DEMO_MANIFOLD_ID, q).get("outcome")
        if got != declared:
            bad.append((declared, q, got))
    return bad


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
    """Run the four-mood wedge in-process, pretty-print the real wire JSON, and VERIFY it.

    Returns 0 when every leg earned the mood its heading declares, 1 otherwise. The non-zero exit is
    load-bearing: this command is the first-run surface, and a first-run surface that can print a
    contradiction while succeeding is worse than no demo at all.
    """
    import sys
    out = out or sys.stdout
    store = demo_store()
    mismatches = []

    def emit(title, note, wire, declared=None):
        print(_hr(title), file=out)
        print(note, file=out)
        print(json.dumps(wire, indent=2, ensure_ascii=False), file=out)
        if declared is not None and wire.get("outcome") != declared:
            mismatches.append((declared, wire.get("outcome")))

    print("Columna demo — four asks, all four moods (real wire JSON).", file=out)

    # 1) clarify — an inline reduction whose input anchor is underdetermined
    clarify = T.query(store, DEMO_MANIFOLD_ID, CLARIFY_Q)
    emit(f"[1/4] clarify    query: {CLARIFY_Q}",
         "Averaging `aov` to calendar month leaves the grain to resolve `aov` at underdetermined. "
         "Columna names the candidate input anchors as alternatives instead of inventing one:",
         clarify, declared="clarify")

    # 2) refuse — a structurally unlawful operation (a stock summed across the blocked time axis)
    refuse = T.query(store, DEMO_MANIFOLD_ID, REFUSE_Q)
    emit(f"[2/4] refuse     query: {REFUSE_Q}",
         "Summing `stock` over days into months adds daily snapshots that do not reconcile: the same "
         "units counted once for every day they sat on the shelf. The arithmetic is perfectly "
         "computable — what is missing is the authority to perform it, which `stock`'s author "
         "withheld by declaring `sum BLOCKED { calendar }`. So no number comes back at all, and the "
         "reason and the lawful edits come back instead. Spelling the same operation differently "
         "— `sum(stock.last@day)`, or hidden inside a derived column — refuses identically:",
         refuse, declared="refuse")

    # 3) disclose — served, but WITH a material caveat (a lawful ask, approximately realized)
    disclose = T.query(store, DEMO_MANIFOLD_ID, DISCLOSE_Q)
    emit(f"[3/4] disclose   query: {DISCLOSE_Q}",
         "Distinct buyers per month is a lawful question, and Columna answers it — but it counts "
         "distinct customers from a sketch, not by holding every id in memory. So the numbers come "
         "back WITH a material caveat carrying the estimator and its relative error. Disclose is not "
         "a softer refusal: the ask is sound, and the one condition on the answer travels with it "
         "instead of being left for the reader to discover:",
         disclose, declared="disclose")

    # 4) serve — a well-posed ask over one population
    serve = T.query(store, DEMO_MANIFOLD_ID, SERVE_Q)
    emit(f"[4/4] serve      query: {SERVE_Q}",
         "Average order value by calendar month — one population, well posed. Columna serves the "
         "numbers:",
         serve, declared="serve")

    if mismatches:
        # Fail closed, naming both sides. The likely cause is a package-set incoherence: a
        # columna-server whose seeds were chosen against a different columna-core than the one
        # installed. Print the versions so the reader can see the mismatch rather than infer it.
        print(_hr("DEMO INTEGRITY FAILURE — a leg did not earn the mood it declares"), file=out)
        for declared, got in mismatches:
            print(f"  declared '{declared}' but the engine returned '{got}'", file=out)
        try:
            from importlib.metadata import version as _v
            print(f"\n  columna-server {_v('columna-server')} / columna-core {_v('columna-core')}",
                  file=out)
        except Exception:                                    # pragma: no cover - metadata absent
            pass
        print("\n  These two packages disagree about what the demo demonstrates. Install a coherent\n"
              "  set (`pip install -U columna`) rather than trusting either half of this transcript.",
              file=out)
        return 1

    print(_hr("Nothing was guessed away, and nothing was answered outside its contract. "
              "One wire, every surface."), file=out)
    print("demo seed integrity OK - four legs, four declared moods, all earned.", file=out)
    return 0
