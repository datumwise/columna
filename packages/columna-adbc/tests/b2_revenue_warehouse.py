"""
B-2's physical fixture — **one DuckDB table at `revenue`'s actual governed root grain.**

    revenue · manifold `andfam.commerce` · root `{store, day, order}` · law SUM · value domain decimal

ONE ROW PER GOVERNED ROOT POINT, AND NO AGGREGATE ANYWHERE (ruled §4). The table IS the independently
established root family state: six accepted orders, six rows, six coordinates. Nothing in the physical path
groups, sums, filters or joins — the projection the crossing generates is a bare `SELECT cols FROM obj`, and
`projection_sql` is structurally incapable of emitting anything else.

THE PHYSICAL NAMES ARE DELIBERATELY NOT THE GOVERNED NAMES. `shop_code` is not `store`, `booked_on` is not
`day`, `order_ref` is not `order`, `net_amount` is not `revenue`. A provider that could only work where the
warehouse happened to use the Manifold's vocabulary would be reverse-inferring analytical identity from
physical columns, which §5 forbids; the binding maps one onto the other in one direction and the test that
renames a column proves the binding is doing the work.

AN UNREQUESTED COLUMN EXISTS ON PURPOSE. `channel` is never bound and must never appear in the generated
SQL — the same control the lighthouse fixture uses, for the same reason: a projection that quietly widens is
a projection nobody is governing.

AMOUNTS ARE `DOUBLE`, NOT `DECIMAL`, AND THAT IS A FIXTURE CHOICE WITH A REASON. The columnar substrate's
own revenue column is `pa.float64()` (`columnar/exhibit.py`), and `projection_sql` cannot carry a cast — it
is a bare projection by design — so a `DECIMAL` warehouse column would arrive as `decimal128` and reach the
frame renderer, whose displayable set is `(int, float, str, bool, None)`. Widening that set is a real
question and it is not B-2's; storing the warehouse column as `DOUBLE` keeps the crossing unconverted and
the slice one family wide. Recorded as a limitation rather than smuggled in as a cast.
"""
from __future__ import annotations

import pathlib
from typing import Optional

#: The physical endpoint. `schema` participates in selection — `sales.fact_order` and
#: `staging.fact_order` are different material and neither answers for the other.
SCHEMA = "sales"
TABLE = "fact_order"

#: governed constituent → physical column. **The only place the two vocabularies meet.**
STORE_COLUMN = "shop_code"
DAY_COLUMN = "booked_on"
ORDER_COLUMN = "order_ref"
VALUE_COLUMN = "net_amount"
#: Bound by nothing, projected by nothing.
UNREQUESTED_COLUMN = "channel"

#: Six accepted orders at `{store, day, order}`. Deliberately UNBALANCED across both store and day, so a
#: continuation that silently used a wrong grouping would produce a visibly wrong number rather than a
#: symmetric one. Totals: D1 175.0, D2 325.0; east 275.0, west 225.0; grand total 500.0.
ORDERS = (
    ("east", "2026-01-01", "O1", 100.0, "web"),
    ("east", "2026-01-01", "O2", 75.0, "store"),
    ("east", "2026-01-02", "O3", 100.0, "web"),
    ("west", "2026-01-02", "O4", 125.0, "web"),
    ("west", "2026-01-02", "O5", 50.0, "phone"),
    ("west", "2026-01-02", "O6", 50.0, "web"),
)

GRAND_TOTAL = 500.0
BY_DAY = {("2026-01-01",): 175.0, ("2026-01-02",): 325.0}


def _q(identifier: str) -> str:
    """The fixture quotes with its OWN escaper, deliberately not the adapter's.

    A fixture that borrowed `duckdb_adbc._quote` would make every escaping test a test of one function
    agreeing with itself."""
    return '"' + identifier.replace('"', '""') + '"'


def build(dirpath, *, filename: str = "commerce.duckdb", schema: str = SCHEMA, table: str = TABLE,
          value_sql_type: str = "DOUBLE", store_column: str = STORE_COLUMN,
          day_column: str = DAY_COLUMN, order_column: str = ORDER_COLUMN,
          value_column: str = VALUE_COLUMN, orders=ORDERS) -> str:
    """Write the warehouse and return its path. **Built through the NATIVE duckdb API, not through ADBC** —
    the crossing under test is the read, and building the fixture with it would make the test circular."""
    import duckdb

    path = str(pathlib.Path(dirpath) / filename)
    con = duckdb.connect(path)
    try:
        con.execute(f"CREATE SCHEMA IF NOT EXISTS {_q(schema)}")
        con.execute(
            f"CREATE OR REPLACE TABLE {_q(schema)}.{_q(table)} ("
            f"  {_q(store_column)} VARCHAR,"
            f"  {_q(day_column)} VARCHAR,"
            f"  {_q(order_column)} VARCHAR,"
            f"  {_q(value_column)} {value_sql_type},"
            f"  {_q(UNREQUESTED_COLUMN)} VARCHAR)")
        con.executemany(
            f"INSERT INTO {_q(schema)}.{_q(table)} VALUES (?, ?, ?, ?, ?)", [list(o) for o in orders])
    finally:
        con.close()
    return path


def binding(*, schema: Optional[str] = SCHEMA, table: str = TABLE, store_column: str = STORE_COLUMN,
            day_column: str = DAY_COLUMN, order_column: str = ORDER_COLUMN,
            value_column: str = VALUE_COLUMN):
    """The deployment's private physical binding for `revenue`. **Injected, never discovered.**"""
    from columna_adbc import PhysicalFamilyBinding

    return PhysicalFamilyBinding(
        family_id="revenue", schema=schema, table=table,
        coordinates={"store": store_column, "day": day_column, "order": order_column},
        value_column=value_column,
        note="this deployment keeps accepted-order value in sales.fact_order")
