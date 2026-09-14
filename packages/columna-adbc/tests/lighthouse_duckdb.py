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

THE IDENTIFIERS ARE OVERRIDABLE, AND THIS FILE QUOTES THEM WITH ITS OWN `_q`, NOT THE ADAPTER'S.
The adversarial-identifier control would prove nothing if the fixture wrote its DDL through the very
function under test — two implementations of the same mistake agree. `_q` here is deliberately a
separate three-line implementation, and the control does not rest on it either: the decoy object
below is what makes a broken escape VISIBLE IN THE VALUES rather than merely unasserted.

A DECOY OBJECT EXISTS WHEN THE ADVERSARIAL NAMES ARE USED. `sales.decoy` holds a value that appears
nowhere in the governed case. If an identifier carrying `" FROM sales.decoy --` were interpolated
unescaped, the generated SQL would read the decoy and the served value would be the decoy's. So the
control is not "the SQL string looks escaped" — it is "the material that came back is from the
object the realization named".
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


#: an identifier set carrying embedded quotes, for the adversarial-identifier control. The column
#: name is not merely odd — spelled into SQL unescaped it CLOSES the quoted identifier and names a
#: second object, so a broken escape reads `sales.decoy` instead of the realization's column.
EVIL_SCHEMA = 'sa"les'
EVIL_TABLE = 'fact"sale'
EVIL_STORE_COLUMN = 'store"code'
EVIL_DAY_COLUMN = 'sold"on'
EVIL_VALUE_COLUMN = 'amount" FROM sales.decoy --'

#: what `sales.decoy` holds. Present in NO governed row, so its appearance anywhere downstream is
#: proof that a second object was read.
DECOY_VALUE = "999.0000"


def _q(identifier: str) -> str:
    """Quote for DuckDB DDL. Deliberately NOT the adapter's `_quote` — see the module docstring."""
    escaped = identifier.replace('"', '""')
    return '"' + escaped + '"'


def build(dirpath, *, value_sql_type: str = "DECIMAL(18,4)",
          store_sql_type: str = "VARCHAR", day_sql_type: str = "DATE",
          null_store: bool = False, null_value: bool = False,
          filename: str = "warehouse.duckdb",
          schema: str = SCHEMA, table: str = TABLE, store_column: str = STORE_COLUMN,
          day_column: str = DAY_COLUMN, value_column: str = VALUE_COLUMN,
          decoy: bool = False) -> str:
    """Create the deployment's DuckDB database and return its path.

    The `*_sql_type` arguments exist for the NEGATIVE controls: the same governed claim over a
    source that stores the value as `DOUBLE`, or the coordinate as `INTEGER`, is the whole of
    "successful transport does not establish admissibility" made concrete at the source.

    `null_value` puts a NULL in a CAP-COMPATIBLE `DECIMAL(18,4)` column — the carrier is admissible
    by TYPE and the absence is the only thing wrong with it, which is the point.

    The identifier arguments exist for the adversarial-identifier control and for nothing else."""
    import duckdb

    path = str(pathlib.Path(dirpath) / filename)
    con = duckdb.connect(path)
    try:
        con.execute(f"CREATE SCHEMA IF NOT EXISTS {_q(schema)}")
        con.execute(
            f"CREATE OR REPLACE TABLE {_q(schema)}.{_q(table)} ("
            f"  {_q(store_column)} {store_sql_type},"
            f"  {_q(day_column)} {day_sql_type},"
            f"  {_q(value_column)} {value_sql_type},"
            f"  note VARCHAR)")
        if decoy:
            # THE DECOY CARRIES THE GOVERNED PHYSICAL COLUMN NAMES ON PURPOSE. An unescaped
            # `amount" FROM sales.decoy --` closes the quoted identifier and re-points the FROM at
            # this object, commenting out the rest; if the decoy lacked these columns the injected
            # query would merely ERROR, and an error is a weaker result than a wrong answer served
            # confidently. With them, a broken escape returns DECOY_VALUE and the control SEES it.
            con.execute(
                f"CREATE OR REPLACE TABLE {_q(schema)}.decoy ("
                f"  {_q(STORE_COLUMN)} VARCHAR, {_q(DAY_COLUMN)} DATE,"
                f"  {_q(VALUE_COLUMN)} {value_sql_type})")
            con.execute(
                f"INSERT INTO {_q(schema)}.decoy VALUES "
                f"('decoy-store', DATE '1999-12-31', CAST('{DECOY_VALUE}' AS {value_sql_type}))")
        # A NON-TEXT store column needs a value its type can hold. The negative control is about
        # the DELIVERED ARROW TYPE contradicting the governed `text`, not about a failed INSERT.
        numeric_store = store_sql_type.upper() not in ("VARCHAR", "TEXT", "STRING")
        for i, (store, day, amount, note) in enumerate(ROWS):
            literal = str(i + 1) if numeric_store else f"'{store}'"
            store_lit = "NULL" if (null_store and i == 2) else literal
            value_lit = ("NULL" if (null_value and i == 2)
                         else f"CAST('{amount}' AS {value_sql_type})")
            con.execute(
                f"INSERT INTO {_q(schema)}.{_q(table)} VALUES ("
                f"  CAST({store_lit} AS {store_sql_type}),"
                f"  CAST('{day}' AS {day_sql_type}),"
                f"  {value_lit},"
                f"  '{note}')")
    finally:
        con.close()
    return path


def build_wide(dirpath, *, days: int, filename: str = "wide.duckdb") -> str:
    """One store, `days` DISTINCT days — a result large enough that the driver hands it back in more
    than one Arrow record batch, with every analytical point still carrying exactly one contribution.

    Volume is the only thing that differs from `build`. Nothing here asks for streaming, no adapter
    argument changes, and the governed question is the same one: the point is whether the batch
    mechanics the adapter already discharges produce ONE `pa.Table` carrying ALL the material."""
    import duckdb

    path = str(pathlib.Path(dirpath) / filename)
    con = duckdb.connect(path)
    try:
        con.execute(f"CREATE SCHEMA IF NOT EXISTS {_q(SCHEMA)}")
        con.execute(
            f"CREATE OR REPLACE TABLE {_q(SCHEMA)}.{_q(TABLE)} ("
            f"  {_q(STORE_COLUMN)} VARCHAR, {_q(DAY_COLUMN)} DATE,"
            f"  {_q(VALUE_COLUMN)} DECIMAL(18,4), note VARCHAR)")
        # `i + 1` so no value is zero: a dropped or defaulted contribution stays visible in the sum.
        con.execute(
            f"INSERT INTO {_q(SCHEMA)}.{_q(TABLE)} "
            f"SELECT 'east', DATE '2020-01-01' + INTERVAL (i) DAY, "
            f"       CAST(i + 1 AS DECIMAL(18,4)), 'unrequested' "
            f"FROM range({int(days)}) t(i)")
    finally:
        con.close()
    return path
