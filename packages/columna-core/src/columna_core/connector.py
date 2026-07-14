"""
columna_core.connector — single-table column delivery (DuckDB).

The discipline: the backend is asked only to DELIVER columns from ONE table.
  - deliver_measure: a measure aggregated within its home table at a base level (group-by, one table).
  - deliver_edge: a functional key->key mapping from one provider table (distinct, one table).
  - deliver_base_rows: base rows for building sketches (one table).
It NEVER combines columns across tables. All relating happens in the engine (transport).
"""
from __future__ import annotations
from typing import Optional, Protocol, runtime_checkable
import re
import duckdb
import polars as pl


@runtime_checkable
class Connector(Protocol):
    """The five-method column-delivery surface a Core connector must expose (audit §B1 / WP-C).

    The B1 seam ("the backend delivers columns, never combines them") is structurally enforced by
    this surface: every method delivers from ONE table (a single `SELECT ... GROUP BY` / DISTINCT);
    none can join two tables, so combination has no way to be expressed through the API. Today
    `DuckDBConnector` is the one implementation (Core is single-backend by design, ADR-031 D15);
    naming the contract as a `Protocol` is purely additive and gives a future second adapter
    something to implement against, and the parity suite something to range over.
    """

    def deliver_measure(self, table: str, key_cols: list, aggs, where: Optional[str] = None) -> pl.DataFrame: ...
    def deliver_base_values(self, table: str, key_cols: list, value_expr: str, where: Optional[str] = None) -> pl.DataFrame: ...
    def deliver_edge(self, table: str, frm_col: str, to_col: str) -> pl.DataFrame: ...
    def deliver_attribute(self, table: str, key_col: str, attr_col: str) -> pl.DataFrame: ...
    def deliver_base_rows(self, table: str, key_cols: list, value_col: str, where: Optional[str] = None) -> pl.DataFrame: ...

# logical (Polars) dtype -> this backend's (DuckDB) physical type
_LOGICAL_TO_DUCKDB = {
    "Float64": "DOUBLE", "Int64": "BIGINT", "Decimal": "DECIMAL", "Boolean": "BOOLEAN",
    "String": "VARCHAR", "Date": "DATE", "Datetime": "TIMESTAMP", "Time": "TIME",
    "Duration": "INTERVAL", "Categorical": "VARCHAR", "Enum": "VARCHAR",
}

def _phys_class(duckdb_type: str) -> str:
    t = duckdb_type.upper()
    if any(k in t for k in ("DOUBLE", "FLOAT", "REAL", "INT", "DECIMAL", "NUMERIC", "HUGEINT")):
        return "numeric"
    if any(k in t for k in ("VARCHAR", "CHAR", "TEXT")):
        return "string"
    if any(k in t for k in ("DATE", "TIMESTAMP", "TIME", "INTERVAL")):
        return "temporal"
    if "BOOL" in t:
        return "boolean"
    return "other"

def _logical_class(logical: str) -> str:
    if logical in ("Float64", "Int64", "Decimal"): return "numeric"
    if logical in ("String", "Categorical", "Enum"): return "string"
    if logical in ("Date", "Datetime", "Time", "Duration"): return "temporal"
    if logical == "Boolean": return "boolean"
    return "other"


class DuckDBConnector:
    def __init__(self, con: duckdb.DuckDBPyConnection):
        self.con = con
        self.fetch_count = 0

    def table_version(self, table: str) -> str:
        n = self.con.execute(f"SELECT count(*) FROM {table}").fetchone()[0]
        return f"{table}:{n}"

    # ---- logical <-> physical type bridge (this is the connector's job) ----
    def physical_type(self, table: str, col: str) -> Optional[str]:
        r = self.con.execute(
            "SELECT data_type FROM information_schema.columns "
            "WHERE table_name = ? AND column_name = ?", [table, col]).fetchone()
        return r[0] if r else None

    def realize(self, table: str, source_expr: str, logical_type: str) -> str:
        """Realize a measure's declared logical_type from its raw source on THIS backend.
        If source_expr is a bare column whose physical type doesn't match the logical class,
        supply a TRY_CAST; otherwise return it unchanged. Expressions/literals pass through."""
        s = source_expr.strip()
        if not re.match(r"^[A-Za-z_]\w*$", s):
            return source_expr                      # an expression or literal — the author owns it
        phys = self.physical_type(table, s)
        if phys is None:
            return source_expr
        if _phys_class(phys) == _logical_class(logical_type):
            return s                                # already the right class — no cast
        target = _LOGICAL_TO_DUCKDB.get(logical_type, "DOUBLE")
        return f"TRY_CAST({s} AS {target})"         # honor the promise from a mismatched physical type

    def deliver_measure(self, table: str, key_cols: list[str], aggs, where=None) -> pl.DataFrame:
        """SELECT key_cols, <aggs> FROM table GROUP BY key_cols — ONE table.
        `aggs` is a list of (out_name, agg_sql): one witness column for VALUE ops,
        two ((_value, _order)) for ORDERED ops."""
        self.fetch_count += 1
        keys = ", ".join(key_cols)
        agg_sel = ", ".join(f"{sql} AS {name}" for (name, sql) in aggs)
        q = f"SELECT {keys}{',' if key_cols else ''} {agg_sel} FROM {table}"
        if where:
            q += f" WHERE {where}"
        if key_cols:
            q += f" GROUP BY {keys}"
        return pl.from_arrow(self.con.execute(q).arrow())

    def deliver_base_values(self, table: str, key_cols: list[str], value_expr: str,
                            where=None) -> pl.DataFrame:
        """SELECT key_cols, value_expr AS _value FROM table — ONE table, NO aggregation.
        Raw base rows for holistic recompute (median/mode) in-engine."""
        self.fetch_count += 1
        keys = ", ".join(key_cols)
        q = f"SELECT {keys}{',' if key_cols else ''} {value_expr} AS _value FROM {table}"
        if where:
            q += f" WHERE {where}"
        return pl.from_arrow(self.con.execute(q).arrow())

    def deliver_edge(self, table: str, frm_col: str, to_col: str) -> pl.DataFrame:
        """SELECT DISTINCT frm_col, to_col FROM table  — ONE table. The relationship-column."""
        self.fetch_count += 1
        q = f"SELECT DISTINCT {frm_col} AS _frm, {to_col} AS _to FROM {table}"
        return pl.from_arrow(self.con.execute(q).arrow())

    def deliver_attribute(self, table: str, key_col: str, attr_col: str) -> pl.DataFrame:
        """SELECT DISTINCT key_col, attr_col FROM table — ONE table. A dimension attribute
        delivered at its key's anchor, to be broadcast onto a finer grain in-engine."""
        self.fetch_count += 1
        q = f"SELECT DISTINCT {key_col} AS _key, {attr_col} AS _attr FROM {table}"
        return pl.from_arrow(self.con.execute(q).arrow())

    def deliver_base_rows(self, table: str, key_cols: list[str], value_col: str,
                          where: Optional[str] = None) -> pl.DataFrame:
        """Base rows [keys..., _dv] for sketch building — ONE table."""
        self.fetch_count += 1
        keys = ", ".join(key_cols)
        q = f"SELECT {keys}{',' if key_cols else ''} {value_col} AS _dv FROM {table}"
        if where:
            q += f" WHERE {where}"
        return pl.from_arrow(self.con.execute(q).arrow())
