"""DuckDB through its VENDORED ADBC surface — the first positive material crossing.

THE CROSSING UNDER TEST IS `ADBC API -> Arrow`, and that is worth stating precisely because the
underlying engine library is the same DuckDB binary the native API loads. `duckdb-native` and
`duckdb-adbc` are DISTINCT CROSSINGS WITH DISTINCT FIDELITY RECORDS — the admission study's errata
insists on keeping them apart — and they are NOT DISTINCT DEPENDENCIES. Both statements are true at
once, and conflating them in either direction is a mistake.

THE DRIVER PACKAGE, ACCURATELY (ruled 2026-09-14):

  * there is NO independent `adbc-driver-duckdb` distribution — pip finds none, and
    `importlib.metadata.version("adbc-driver-duckdb")` raises `PackageNotFoundError`;
  * the `duckdb` wheel VENDORS the `adbc_driver_duckdb` package;
  * that surface resolves to the DuckDB shared library;
  * therefore its version IS GOVERNED BY THE PINNED DUCKDB PACKAGE, not by an independently
    versioned driver package;
  * `adbc-driver-manager` is a real distribution and is pinned separately and visibly.

`versions()` below reports exactly that and refuses to invent a driver version that does not exist.

NO ABSOLUTE `.so` PATH, EVER. The admission study's probes hard-coded one (`DUCK_LIB`); that is an
environment fact, not a package fact, and it cannot be pinned. Resolution goes through
`adbc_driver_duckdb.driver_path()`, which is the vendored package's own supported entry point and
uses `importlib.util.find_spec`. Hard-coding the path would trade a versioning risk for a silent
portability failure AND remove the very signal `driver_surface()` exists to raise: a vendored package
that disappeared would stop being detectable at all.

FAIL CLOSED AT CONSTRUCTION. If the vendored surface is absent or unresolvable, that is a DEPLOYMENT
CAPABILITY/SETUP condition, not a governed verdict about anybody's data — so it raises
`DriverSurfaceUnavailable` rather than a Platform refusal, and it raises when the adapter is BUILT
rather than at first fetch, so a dependency bump that drops the surface is a named failure at startup.

SQL IS SOURCE ACCESS, NOT ANALYTICAL AUTHORITY. `projection_sql` generates one projected read from
REALIZATION FACTS ONLY — schema, table, column names. It has no `WHERE`, no `GROUP BY`, no aggregate,
no `JOIN`, no `ORDER BY`, and it never emits `SELECT *`. Ordering is deliberately not part of the
query contract (CAP v1 carries no ordering guarantee), and adding a predicate here would put an
analytical restriction inside transport.
"""
from __future__ import annotations

import importlib
import importlib.metadata as _md
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Tuple

import pyarrow as pa

from columna_platform.source import Material

#: The distribution that vendors the ADBC surface, and the module it vendors. Named as constants so
#: a version report cannot drift from the thing it claims to describe.
DUCKDB_DISTRIBUTION = "duckdb"
ADBC_MANAGER_DISTRIBUTION = "adbc-driver-manager"
VENDORED_ADBC_MODULE = "adbc_driver_duckdb"

#: Quoting policy for identifiers read out of a realization. DuckDB quotes with `"` and escapes an
#: embedded quote by doubling it. Applied to EVERY identifier, including ones that look harmless:
#: a rule with exceptions is a rule somebody will find the exception to.
_IDENT_OK = re.compile(r'^[^\x00]+$')


class DriverSurfaceUnavailable(RuntimeError):
    """The vendored DuckDB ADBC surface is absent or cannot be resolved.

    A DEPLOYMENT CAPABILITY / SETUP CONDITION, deliberately not a Platform refusal. Nothing has been
    asked of anybody's data yet, so there is no governed verdict to report; what is missing is a
    driver this deployment was expected to have. Raised at adapter CONSTRUCTION so that a dependency
    bump which drops the vendored package fails at startup with a name, rather than at first fetch
    with an import error from three frames down."""


@dataclass(frozen=True)
class DriverSurface:
    """The resolved vendored surface, and the version facts that are actually true of it."""

    module: object
    driver_path: str
    duckdb_version: str
    adbc_manager_version: str
    #: ALWAYS None. There is no independent DuckDB-ADBC driver distribution to report a version for,
    #: and reporting one would be the false claim this package is forbidden to make.
    adbc_driver_duckdb_version: Optional[str] = None

    def describe(self) -> Dict[str, Optional[str]]:
        return {
            "duckdb": self.duckdb_version,
            "adbc-driver-manager": self.adbc_manager_version,
            "adbc-driver-duckdb": self.adbc_driver_duckdb_version,
            "adbc_surface": "vendored by the duckdb wheel; no distribution of its own",
            "driver_path_resolved": bool(self.driver_path),
        }


def _distribution_version(name: str) -> str:
    try:
        return _md.version(name)
    except _md.PackageNotFoundError as e:                # pragma: no cover - a broken install
        raise DriverSurfaceUnavailable(
            f"distribution {name!r} is not installed; the DuckDB ADBC surface is vendored by the "
            f"{DUCKDB_DISTRIBUTION} wheel and cannot be resolved without it") from e


def driver_surface() -> DriverSurface:
    """Resolve the vendored ADBC surface through SUPPORTED PACKAGE APIs, or fail closed.

    Supported means: `importlib.import_module` for the vendored package, and that package's own
    public `driver_path()`, which is itself implemented over `importlib.util.find_spec`. Nothing here
    reaches into an unstable internal, and nothing here names a filesystem path."""
    try:
        module = importlib.import_module(VENDORED_ADBC_MODULE)
    except ImportError as e:
        raise DriverSurfaceUnavailable(
            f"the vendored ADBC surface {VENDORED_ADBC_MODULE!r} is not importable. It has no "
            f"distribution of its own and is shipped inside the {DUCKDB_DISTRIBUTION} wheel, so this "
            f"means that wheel is absent or no longer vendors it") from e
    resolver = getattr(module, "driver_path", None)
    if resolver is None:                                 # pragma: no cover - a surface that changed
        raise DriverSurfaceUnavailable(
            f"{VENDORED_ADBC_MODULE!r} exposes no `driver_path()`; this adapter will not guess at a "
            f"shared-library location, and will not reach into the package's internals to find one")
    try:
        path = resolver()
    except Exception as e:
        raise DriverSurfaceUnavailable(
            f"{VENDORED_ADBC_MODULE}.driver_path() could not resolve the DuckDB shared library: "
            f"{type(e).__name__}: {e}") from e
    return DriverSurface(
        module=module,
        driver_path=str(path),
        duckdb_version=_distribution_version(DUCKDB_DISTRIBUTION),
        adbc_manager_version=_distribution_version(ADBC_MANAGER_DISTRIBUTION),
        adbc_driver_duckdb_version=None,
    )


def _quote(identifier: str) -> str:
    if not isinstance(identifier, str) or not identifier or not _IDENT_OK.match(identifier):
        raise ValueError(f"not a usable source identifier: {identifier!r}")
    return '"' + identifier.replace('"', '""') + '"'


def projection_sql(schema: Optional[str], table: str, columns: Sequence[str]) -> str:
    """ONE projected read, generated from realization facts and nothing else.

    A PURE FUNCTION, SO THE TEXT IS TESTABLE WITHOUT A DATABASE. It emits a column list and a
    qualified object name; it cannot emit `SELECT *`, a predicate, an aggregate, a join or an order,
    because there is nowhere in its inputs for any of those to come from. That is the point: the
    absence is structural rather than disciplinary."""
    if not columns:
        raise ValueError("a projection with no columns is not a projection")
    cols = ", ".join(_quote(c) for c in columns)
    obj = f"{_quote(schema)}.{_quote(table)}" if schema is not None else _quote(table)
    return f"SELECT {cols} FROM {obj}"


@dataclass
class DuckDbAdbcSource:
    """One deployment-bound DuckDB source, reached through the vendored ADBC surface.

    CONSTRUCTED BY THE DEPLOYMENT, with configuration. `path` is a DuckDB database location and is a
    DEPLOYMENT FACT: it never appears in a governed realization artifact, which names only a
    `connection` token. Which database `"warehouse"` means is the deployment's to say, and saying it
    is what constructing this object does.

    FAILS CLOSED AT CONSTRUCTION if the vendored surface cannot be resolved."""

    #: deployment-local database location. Not a DSN in a governed artifact; a constructor argument.
    path: str
    #: only so a refusal can say which source could not answer
    name: str = "duckdb-adbc"
    #: EVIDENCE, NOT CONTRACT. Every projection this adapter performed, in order, so a control can
    #: assert ONE fetch happened and assert what it asked for. Nothing reads it to make a decision.
    fetches: List[Tuple[Optional[str], str, Tuple[str, ...], str]] = field(default_factory=list)
    surface: DriverSurface = field(default=None)                          # type: ignore[assignment]

    def __post_init__(self) -> None:
        if self.surface is None:
            self.surface = driver_surface()

    # ── the contract ────────────────────────────────────────────────────────────────────────────
    def fetch(self, *, schema: Optional[str], table: str,
              columns: Sequence[str]) -> Material:
        """`MaterialSource.fetch` — ONE projected request, one Arrow table, one observation.

        NO DEFAULT IS EVER GUESSED. If the realization names an object or a column the source does
        not have, this raises; it does not fall back to another table, another column, or a shorter
        projection. `LookupError` is raised rather than a Platform refusal class because choosing the
        governed jurisdiction is Platform's job and not an adapter's — `read_anchored` translates.

        THE READER HAZARD IS DISCHARGED HERE. `fetch_arrow_table()` returns a materialized
        `pa.Table`; where a driver hands back a `RecordBatchReader` it is read to completion before
        it leaves this method. A consumed-once object must not reach the admission path.

        `data_state=None`, DELIBERATELY. The DuckDB ADBC surface exposes no opaque state identity
        that can be captured as part of THIS material observation, and a second query to manufacture
        one would describe a different moment while looking like the same one. `None` closes reuse
        and never reads as fresh."""
        requested = tuple(columns)
        sql = projection_sql(schema, table, requested)
        self.fetches.append((schema, table, requested, sql))

        dbapi = importlib.import_module(f"{VENDORED_ADBC_MODULE}.dbapi")
        con = dbapi.connect(self.path)
        try:
            cur = con.cursor()
            try:
                cur.execute(sql)
            except Exception as e:
                raise LookupError(
                    f"source {self.name!r} could not read the projection "
                    f"{list(requested)} from {_spell(schema, table)}: {type(e).__name__}: "
                    f"{str(e).strip()[:200]}") from e
            got = cur.fetch_arrow_table()
            if not isinstance(got, pa.Table):            # pragma: no cover - a surface that changed
                got = got.read_all()
        finally:
            con.close()

        # THE PROJECTION IS HONOURED OR IT REFUSES. Never a silently shorter one.
        short = [c for c in requested if c not in got.column_names]
        if short:                                        # pragma: no cover - a surface that changed
            raise LookupError(
                f"source {self.name!r} returned {got.column_names} for a projection of "
                f"{list(requested)} from {_spell(schema, table)}; columns {short} are missing and "
                f"this adapter will not shorten a projection")
        return Material(table=got.select(list(requested)), data_state=None)

    # ── evidence ────────────────────────────────────────────────────────────────────────────────
    def versions(self) -> Dict[str, Optional[str]]:
        """The version facts, stated as they actually are — including the one that does not exist."""
        return self.surface.describe()


def _spell(schema: Optional[str], table: str) -> str:
    return f"{schema}.{table}" if schema is not None else f"{table} (no schema qualification)"
