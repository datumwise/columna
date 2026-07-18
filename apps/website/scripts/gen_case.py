#!/usr/bin/env python3
"""Integrity generator for the /case section — built by running the SHIPPED package (never hand-written).

Emits JSON on stdout: the chapter-3 TRIAL TABLE (real adjudicated verdicts) and the E1-E9 exemplar
corpus (moods, reason codes, recorded counts, wheel marking) — the same drift-gate seeds the tests bind
to. Exits non-zero on any failure so the build fails closed (never ships a stale or fabricated table).
"""
import json
import os
import sys
from importlib.metadata import version

import columna_server
from columna_server.store import _load_one
from columna_server import recapture

CASCADIA = os.path.join(os.path.dirname(columna_server.__file__), "demo", "cascadia")


class _Store:
    def __init__(self, lm):
        self._lm = lm

    def get(self, mid):
        if mid != "cascadia":
            raise KeyError(mid)
        return self._lm


def trial_table(m) -> list:
    """The chapter-3 verdict table, read off the adjudicated manifold (verdicts are load-bearing data)."""
    rows = []
    for h in m.hierarchies:
        rows.append({"claim": f"`{h.lineage}` hierarchy — every hop functional",
                     "verdict": h.license.verdict if h.license else None})
    for a in m.asserts:
        rows.append({"claim": f"ASSERT `{a.name}`",
                     "verdict": a.license.verdict if a.license else None})
    for u in m.universes.values():
        rows.append({"claim": f"`{u.name}` BASIS {u.basis}",
                     "verdict": u.basis_license.verdict if u.basis_license else None})
    # product<->category is RECORDED (a declared relationship, not a tried claim) — ch3 v0.4
    if m.non_functional:
        rows.append({"claim": "product ↔ category (many-to-many)", "verdict": "recorded"})
    return rows


def main() -> int:
    lm = _load_one("cascadia", CASCADIA)
    lm.server.publish()
    corpus = recapture.generate(_Store(lm), lm.server)
    if corpus["flags"]:
        print(f"case generation FAILED — exemplar drift: {corpus['flags']}", file=sys.stderr)
        return 1
    out = {
        "generated_by": f"columna-core {version('columna-core')} / columna-server {version('columna-server')}",
        "manifold": "cascadia",
        "trial_table": trial_table(lm.manifold),
        "exemplars": corpus["exemplars"],
        "wheel": corpus["wheel"],
    }
    json.dump(out, sys.stdout, indent=2, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
