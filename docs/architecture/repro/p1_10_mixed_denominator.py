#!/usr/bin/env python3
"""P1-10 — a family member whose support disagrees with its siblings, and the ratio that serves.

Reproduction for the ledger row of the same name (`docs/architecture/consolidated_ledger_v0_1.md`).
Kept as a script rather than a test because the row is OPEN: a test would have to assert the defect,
and a green suite asserting a defect is a worse artifact than a script that shows one. When P1-10 is
repaired this becomes a standing test and the assertion flips.

    python docs/architecture/repro/p1_10_mixed_denominator.py

WHAT IT SHOWS. `count` is registered `deliver_sql=lambda p: "count(*)"` (operators.py:84). Inside one
declared family, `sum` skips nulls and `count` does not, so two members carry different SUPPORTS.
Their ratio serves with no caveat, and which figure is "right" depends on a law nobody declared —
which is the P2-03 argument arriving as a number.
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
   mean per revenue OBSERVATION : {total} / {obs} = {total / obs}
   mean per LINE                : {total} / {rows} = {total / rows}   <- what serves

Neither is wrong on its face. Which one the number IS depends on a family law that
nothing declares, and the wire says nothing either way. See P2-03.""")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
