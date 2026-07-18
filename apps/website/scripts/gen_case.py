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
from columna_core import logical_spec, physical_map, no_physical_leak

CASCADIA = os.path.join(os.path.dirname(columna_server.__file__), "demo", "cascadia")
WAREHOUSE = os.path.join(CASCADIA, "warehouse")

# ch1's schema-and-rows: the raw tables the team actually has (two facts + the reference tables), and
# a couple of the stale summaries that will be REJECTED — the situation any solution would face.
CH1_TABLES = ["transactions", "eom_inventory", "stores", "calendar", "product_categories",
              "daily_revenue_summary"]


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


def ch1_schema_and_rows() -> list:
    """ch1: each raw table's columns + a few real sample rows, read straight from the bundled warehouse."""
    import duckdb
    con = duckdb.connect()
    tables = []
    for t in CH1_TABLES:
        path = os.path.join(WAREHOUSE, f"{t}.parquet")
        cols = [r[0] for r in con.execute(f"DESCRIBE SELECT * FROM read_parquet('{path}')").fetchall()]
        n = con.execute(f"SELECT count(*) FROM read_parquet('{path}')").fetchone()[0]
        rows = con.execute(f"SELECT * FROM read_parquet('{path}') LIMIT 3").fetchall()
        tables.append({"table": t, "columns": cols, "row_count": n,
                       "sample": [[str(v) for v in row] for row in rows]})
    return tables


def ch2_two_artifacts(m) -> dict:
    """ch2: the two projections of the one authored graph — the purely-logical spec everyone reads, and
    the many-to-one physical->logical map with its rejects. The WALL is asserted: no physical leak."""
    leaks = no_physical_leak(m)
    if leaks:
        raise RuntimeError(f"BLAST WALL BREACH — physical identifiers leaked into the logical spec: {leaks}")
    return {"logical_spec": logical_spec(m), "physical_map": physical_map(m), "wall_holds": True}


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
        "ch1_tables": ch1_schema_and_rows(),
        "ch2_artifacts": ch2_two_artifacts(lm.manifold),
        "trial_table": trial_table(lm.manifold),
        "exemplars": corpus["exemplars"],
        "wheel": corpus["wheel"],
    }
    json.dump(out, sys.stdout, indent=2, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
