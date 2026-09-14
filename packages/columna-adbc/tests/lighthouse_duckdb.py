"""The DEPLOYMENT's DuckDB database for the lighthouse unit — a fixture, not package source.

WHICH DATABASE `warehouse` MEANS IS A DEPLOYMENT FACT. A package that shipped it would be
hard-coding the meaning of a connection token, which is exactly what the source binding exists to
avoid — so this lives in `tests/`, like `lighthouse_material.py` does for the in-memory slice.

THE PHYSICAL NAMES ARE NOT THE GOVERNED ONES, AND THAT IS THE POINT. The publication declares
`sale_at{store, day}` and the family `revenue`; this table has `store_code`, `sold_on` and `amount`.
The mapping's realizations are what claim that one realizes the other. If the two vocabularies were
spelled alike, a path that ignored the realization entirely would pass every test.

THE VALUES ARE THE PROOF-A SHAPE, NOW REACHED THROUGH A DRIVER. Four points over two stores, two
days each, with the two stores' totals different — chosen so that a fold that dropped rows,
double-counted, or grouped on the wrong column produces a visibly wrong answer rather than an
accidentally right one. `DECIMAL(18,4)`, the carriage CAP v1 admits.

AN EXTRA COLUMN IS PRESENT ON PURPOSE. `note VARCHAR` is never requested by any realization, and its
presence is what makes "extra source columns are irrelevant because they were not requested" a
measured fact rather than an assumption.
"""
from __future__ import annotations

import pathlib

#: what the realization claims, restated here so drift between the two is visible in one place
CONNECTION = "warehouse"
SCHEMA = "sales"
TABLE = "fact_sale"

#: physical column names, as the anchor-component and family realizations name them
STORE_COLUMN = "store_code"
DAY_COLUMN = "sold_on"
VALUE_COLUMN = "amount"

#: east totals 30.0000; west totals 4.9382. Different, and neither a round number by accident.
ROWS = (
    ("east", "2026-01-01", "10.0000", "unrequested"),
    ("east", "2026-01-02", "20.0000", "unrequested"),
    ("west", "2026-01-01", "1.2345", "unrequested"),
    ("west", "2026-01-02", "3.7037", "unrequested"),
)


def build(dirpath, *, value_sql_type: str = "DECIMAL(18,4)",
          store_sql_type: str = "VARCHAR", day_sql_type: str = "DATE",
          null_store: bool = False, filename: str = "warehouse.duckdb") -> str:
    """Create the deployment's DuckDB database and return its path.

    The `*_sql_type` arguments exist for the NEGATIVE controls: the same governed claim over a
    source that stores the value as `DOUBLE`, or the coordinate as `INTEGER`, is the whole of
    "successful transport does not establish admissibility" made concrete at the source."""
    import duckdb

    path = str(pathlib.Path(dirpath) / filename)
    con = duckdb.connect(path)
    try:
        con.execute(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA}")
        con.execute(
            f"CREATE OR REPLACE TABLE {SCHEMA}.{TABLE} ("
            f"  {STORE_COLUMN} {store_sql_type},"
            f"  {DAY_COLUMN} {day_sql_type},"
            f"  {VALUE_COLUMN} {value_sql_type},"
            f"  note VARCHAR)")
        # A NON-TEXT store column needs a value its type can hold. The negative control is about
        # the DELIVERED ARROW TYPE contradicting the governed `text`, not about a failed INSERT.
        numeric_store = store_sql_type.upper() not in ("VARCHAR", "TEXT", "STRING")
        for i, (store, day, amount, note) in enumerate(ROWS):
            literal = str(i + 1) if numeric_store else f"'{store}'"
            store_lit = "NULL" if (null_store and i == 2) else literal
            con.execute(
                f"INSERT INTO {SCHEMA}.{TABLE} VALUES ("
                f"  CAST({store_lit} AS {store_sql_type}),"
                f"  CAST('{day}' AS {day_sql_type}),"
                f"  CAST('{amount}' AS {value_sql_type}),"
                f"  '{note}')")
    finally:
        con.close()
    return path
