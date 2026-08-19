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

    # ---- P0.5b-0: the data-identity obligation (part of the CONTRACT, not an implementation detail) ----
    def data_identity(self, table: str) -> Optional[str]:
        """An opaque comparable CHANGE/VERSION TOKEN for this table's realized data state.

        CONTRACT (what Core relies on — and deliberately no more):
          · the token is a token the CONNECTOR warrants as trustworthy for REUSE: under the
            connector's own documented guarantee, a change to the realized data or realization that
            could change a served result or an adjudication finding is reflected by a different
            token, to the strength that guarantee provides;
          · it MUST be stable while the data is unchanged, so unchanged data stays reusable;
          · it is NOT analytical identity. `F@A` is unchanged by a data refresh; this token names the
            state that contingent evidence and cached results were derived FROM.

        THE STRENGTH OF THE GUARANTEE IS THE CONNECTOR'S TO STATE, and Core assumes no more than the
        connector documents. Two kinds qualify, and they are not equally strong:

          · a backend-native version/snapshot token — an Iceberg/Delta snapshot id, a catalog
            version, an MVCC/xmin watermark — is a SOURCE-PROVIDED DATA IDENTITY under that
            backend's contract. This is the strongest form and is preferred wherever it exists.
          · a computed CONTENT FINGERPRINT is a CHANGE DETECTOR. Finite digests can collide in
            principle, so a fingerprint is trustworthy-for-reuse, NOT a collision-free identity, and
            must never be documented as one.

        A connector that can supply neither returns `None` — including when it cannot honestly make
        the guarantee above. `None` is not a failure to serve; it is a failure to REUSE: Core then
        declines cache reuse and treats prior realization/data-bound evidence as no longer current,
        rather than manufacture freshness. "Unknown" must never be read as "unchanged".

        ROW COUNT ALONE IS NEVER A VALID IMPLEMENTATION of this method. It cannot see an UPDATE or a
        same-cardinality delete+insert, which is precisely the class of change this exists to catch.
        """
        ...


# The authoring aperture's metered-sample cap (RATIFIED 2026-07-16). Rationale: sampling is a GOVERNED
# aperture, not an open pipe — every read is BOUNDED per call so the model perceives a declared shape,
# never a firehose. 1000 rows is enough to expose a distribution / catch an FK violation while staying a
# metered read; PROFILE-STATS-FIRST is preferred (use `profile` to settle a question, `sample` only when
# stats don't). Session-level budgets and a column-masking policy are DEFERRED (ledgered for the
# enterprise era, capture §5's two-ends precision). Constant and documented, by design.
APERTURE_SAMPLE_CAP = 1000


@runtime_checkable
class CatalogAperture(Protocol):
    """The authoring-side READ surface (the two-ends DATA WALL for `columna init`): catalog metadata,
    profile statistics, and a METERED sample. Like the delivery Connector, no general query composes
    here — every call is a single bounded, typed read from ONE table, so an exfiltrating read is
    structurally impossible (there is no method that takes SQL). `sample` is capped at
    APERTURE_SAMPLE_CAP rows PER CALL; prefer `profile` first and sample only when stats don't settle."""
    def catalog(self) -> list: ...                          # [{table, columns:[{name,type}], keys:[...]}]
    def profile(self, table: str, column: str) -> dict: ...  # {count, distinct, nulls, min, max}
    def sample(self, table: str, n: int) -> pl.DataFrame: ...  # up to min(n, APERTURE_SAMPLE_CAP) rows

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
        self._ddb_ver = None      # P0.5b-0: token namespace, resolved lazily

    # P0.5b-0: the fingerprint ALGORITHM version. Bumped whenever the digest's composition changes,
    # so tokens from different algorithms are never compared as if they meant the same thing.
    _IDENTITY_ALGO = "cdg1"

    def _duckdb_version(self) -> str:
        """The running DuckDB version, cached per connector — part of the token's namespace."""
        v = getattr(self, "_ddb_ver", None)
        if v is None:
            try:
                v = str(self.con.execute("SELECT version()").fetchone()[0])
            except Exception:
                v = "unknown"
            self._ddb_ver = v
        return v

    def data_identity(self, table: str) -> Optional[str]:
        """A CONTENT FINGERPRINT / CHANGE DETECTOR for `table` — NOT a collision-free identity.

        DuckDB is an embedded engine and exposes no MVCC/catalog change token, so there is no
        source-provided data identity to pass through here. What this connector can honestly supply
        is a change detector: one single-table aggregate pass, no join (the B1 seam is preserved),
        over three order-independent aggregates of the row hash:

            count(*)              cardinality
            sum(hash(row))        additive fingerprint
            bit_xor(hash(row))    xor fingerprint

        WHAT IT GIVES. All three are carried because none is sufficient alone. `count` misses
        same-cardinality mutation (the defect this unit repairs). `bit_xor` alone is defeated by
        duplicate rows — inserting an identical PAIR leaves the xor unchanged — so it cannot be
        trusted by itself. Carrying `sum` alongside it closes that cancellation. A change that
        escapes detection must leave all three aggregates simultaneously unmoved.

        WHAT IT DOES NOT GIVE. These are finite aggregates over a 64-bit hash. Agreement is strong
        evidence of sameness, not proof of it: a collision is improbable, NOT impossible. This
        method therefore supplies a token trustworthy for safe REUSE, and nothing in Core may be
        documented as holding a stronger guarantee than that. A backend that publishes a native
        version/snapshot token SHOULD override this method and return it instead — that is a
        source-provided identity under the backend's own contract, and is strictly stronger.

        WHAT IT COVERS. Row CONTENTS, compared POSITIONALLY. Value edits, inserts, deletes at any
        cardinality, and column add/drop all move the token. Schema facts that leave every row's
        hash unmoved — notably a column RENAME — do NOT move it (recorded as an open item on the
        P0.5b-0 review; column NAMES are not part of the digest).

        NAMESPACING. The token carries both the fingerprint algorithm (`cdg1`) and the DuckDB
        version, because DuckDB documents `hash()` as an implementation detail free to change
        between releases. Namespacing makes such a change read as a CONSERVATIVE INVALIDATION — a
        different token, so recompute and re-attest — rather than as an ambiguous comparison between
        two digests that were never comparable.

        COST: O(rows), one pass, per call. Acceptable because Core computes it ONCE PER REQUEST (see
        `PublishedScope.attested_identities`), not once per column.
        """
        try:
            n, s, x = self.con.execute(
                f"SELECT count(*), sum(hash(_dt))::HUGEINT, bit_xor(hash(_dt)) "
                f"FROM {table} AS _dt").fetchone()      # fixed alias: qualified/quoted names bind too
        except Exception:
            return None                       # cannot establish -> caller MUST fail closed for reuse
        return f"{self._IDENTITY_ALGO}/duckdb-{self._duckdb_version()}:{n}:{s}:{x}"

    def table_version(self, table: str) -> str:
        """DEPRECATED (P0.5b-0) — row count is NOT a trustworthy data identity.

        Retained only so an external embedder calling it keeps working; nothing in Core consults it
        any more. It cannot see an UPDATE, or a delete+insert at equal cardinality, so using it to
        validate evidence or a cached result can serve a stale number. Use `data_identity`.
        """
        n = self.con.execute(f"SELECT count(*) FROM {table}").fetchone()[0]
        return f"{table}:{n}"

    # ---- the authoring aperture (catalog / profile / metered sample) — no SQL crosses it ----
    def catalog(self) -> list:
        cols = self.con.execute(
            "SELECT table_name, column_name, data_type FROM information_schema.columns "
            "WHERE table_schema = 'main' ORDER BY table_name, ordinal_position").fetchall()
        tables: dict = {}
        for tname, cname, dtype in cols:
            tables.setdefault(tname, {"table": tname, "columns": [], "keys": []})
            tables[tname]["columns"].append({"name": cname, "type": dtype})
        try:                                        # best-effort declared keys (PK/FK/UNIQUE)
            for t, ctype, ccols in self.con.execute(
                    "SELECT table_name, constraint_type, constraint_column_names "
                    "FROM duckdb_constraints()").fetchall():
                if t in tables:
                    tables[t]["keys"].append({"type": ctype, "columns": list(ccols)})
        except Exception:
            pass
        return list(tables.values())

    def profile(self, table: str, column: str) -> dict:
        r = self.con.execute(
            f'SELECT count(*), count(distinct "{column}"), count(*) - count("{column}"), '
            f'min("{column}"), max("{column}") FROM "{table}"').fetchone()
        return {"count": r[0], "distinct": r[1], "nulls": r[2], "min": r[3], "max": r[4]}

    def sample(self, table: str, n: int) -> pl.DataFrame:
        cap = min(int(n), APERTURE_SAMPLE_CAP)      # metered: a per-call row cap, always enforced
        return self.con.execute(f'SELECT * FROM "{table}" LIMIT {cap}').pl()

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
