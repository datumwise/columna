#!/usr/bin/env python3
"""P1-10 — a family member whose support disagrees with its siblings, and the ratio that serves.

Reproduction for the ledger row of the same name (`docs/architecture/consolidated_ledger_v0_1.md`).
REPAIRED 2026-08-31 (Mission A'). Kept as the reproduction of what was wrong — running it now shows
the CORRECTED behaviour, which is the point: `revenue.count` is 4, not 5, and the ratio is 25.0. The
assertion flipped into a standing test, as this note said it would:
`packages/columna-core/tests/test_family_member_support.py`.

    python docs/architecture/repro/p1_10_mixed_denominator.py

WHAT IT SHOWED. `count` was registered `deliver_sql=lambda p: "count(*)"`, discarding its operand, so
inside one declared family `sum` skipped nulls and `count` did not: two members, two supports. Their
ratio served 20.0 with no caveat, where the mean per revenue observation was 25.0, and which figure
was "right" depended on a law nobody declared. The operand is now passed through, so a family member
over a declared VALUE counts that value's observations and the supports agree by construction.
"""
import duckdb

from columna_core import ManifoldServer
from columna_core.connector import DuckDBConnector
from columna_core.parser import parse_manifold

MANIFOLD = """
MANIFOLD probe VERSION 1
UNIVERSE sales = store BASIS events
LEVEL store = store_id BASE
MEASURE revenue ON sales FROM sales_lines TYPE Float64 VALUE amount
    FAMILY {
        sum
        count
        min
        max
    }
DERIVED avg_line = revenue.sum / revenue.count
"""


def main() -> int:
    con = duckdb.connect()
    # five rows; ONE carries no revenue observation at all
    con.execute("""CREATE TABLE sales_lines AS SELECT * FROM (VALUES
        ('s1', 10.0), ('s1', 20.0), ('s1', NULL), ('s1', 30.0), ('s1', 40.0))
        AS t(store_id, amount)""")

    srv = ManifoldServer(parse_manifold(MANIFOLD), DuckDBConnector(con))
    srv.publish()

    rows = con.execute("SELECT count(*) FROM sales_lines").fetchone()[0]
    obs = con.execute("SELECT count(amount) FROM sales_lines").fetchone()[0]
    total = con.execute("SELECT sum(amount) FROM sales_lines").fetchone()[0]
    print(f"warehouse:  rows = {rows} | revenue observations = {obs} | sum(amount) = {total}")

    print("\nthe one declared family, at {store}:")
    for member in ("sum", "count", "min", "max"):
        fr = srv.planner.run(("store",), [(f"revenue.{member}", f"revenue.{member}")], None)
        col = fr.columns[0]
        val = "REFUSED" if col.refusal else col.frame.rows()[0][1]
        print(f"   revenue.{member:<6} -> {val}")

    fr = srv.planner.run(("store",), [("avg_line", "avg_line")], None)
    col = fr.columns[0]
    print(f"\nDERIVED avg_line = revenue.sum / revenue.count")
    print(f"   outcome  : {fr.outcome}")
    print(f"   value    : {col.frame.rows()[0][1] if not col.refusal else col.refusal.detail}")
    print(f"   caveats  : {[(c.category, c.detail) for c in col.disclosure.caveats]}")

    print(f"""
   mean per revenue OBSERVATION : {total} / {obs} = {total / obs}   <- what serves now
   mean per LINE                : {total} / {rows} = {total / rows}   <- what served before the repair

REPAIRED. `revenue.count` counts observations of the declared VALUE, so every member of the family
is about the same support and the ratio has one denominator. Row-counting is still fully available
and separately addressable as `MEASURE lines ... AS count(*)` — the ambiguity was removed, not the
choice. See the ledger row P1-10 and tests/test_family_member_support.py.""")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
