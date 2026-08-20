"""
conftest.py — shared test configuration for columna-core.

Two responsibilities:

1. sys.path wiring (WP-0 rider 1: explicit, documented, NO implicit cwd dependence). The demo suites
   double as the test harness: `build_benchmark.py` defines `load()`, `build_manifold()`, and
   `run_validations()` that both the demos and the in-process fixtures below reuse (Option 1 — a
   single source of truth for the benchmark Manifold, no duplication). Because those modules live in
   `packages/columna-core/demos/` — a sibling of this `tests/` dir, importable by neither package
   name nor cwd — we insert that directory onto `sys.path` explicitly and unconditionally here.
   `src/` is inserted too so `import columna_core` works from a bare checkout without an editable
   install. Both paths are absolute, derived from this file's location.

2. Fixtures (spec §"Test conversion" pt 4): a fixture-warehouse `DuckDBConnector`, the parsed demo
   Manifold (from `benchmark.cml`), and a `ManifoldServer` over the fixture.

3. The `warehouse` marker (spec §CI): full-real-warehouse validations, opt-in via
   COLUMNA_BENCH_WAREHOUSE, excluded in CI.
"""
import glob
import os
import sys

import pytest

_TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
_PKG_ROOT = os.path.dirname(_TESTS_DIR)                      # packages/columna-core
_SRC = os.path.join(_PKG_ROOT, "src")                       # the columna_core package
_DEMOS = os.path.join(_PKG_ROOT, "demos")                   # the demo suites + shared harness
_FIXTURE_WAREHOUSE = os.path.join(_TESTS_DIR, "fixtures", "mini_warehouse")

_FIXTURES = os.path.join(_TESTS_DIR, "fixtures")             # afternoon_world and friends

# --- rider 1: explicit, documented sys.path insertion (no cwd reliance) ---
for _p in (_SRC, _DEMOS, _FIXTURES):
    if _p not in sys.path:
        sys.path.insert(0, _p)


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "warehouse: full real-warehouse validation; runs only when COLUMNA_BENCH_WAREHOUSE is set "
        "(the 10 real-data proofs, ×2 for hand-built + parsed). Excluded in CI.",
    )


# ----------------------------------------------------------------------------
# In-process fixtures over the mini-warehouse (spec pt 4).
# ----------------------------------------------------------------------------
def _load(warehouse_dir: str):
    import duckdb

    con = duckdb.connect()
    for f in sorted(glob.glob(os.path.join(warehouse_dir, "*.parquet"))):
        t = os.path.basename(f)[:-8]
        con.execute(f"CREATE TABLE {t} AS SELECT * FROM read_parquet('{f}')")
    return con


@pytest.fixture(scope="session")
def fixture_warehouse_dir() -> str:
    assert os.path.isdir(_FIXTURE_WAREHOUSE), (
        f"mini-warehouse missing at {_FIXTURE_WAREHOUSE}; run tests/fixtures/make_fixture.py"
    )
    return _FIXTURE_WAREHOUSE


@pytest.fixture
def fixture_connector(fixture_warehouse_dir):
    """A DuckDBConnector over the checked-in mini-warehouse."""
    from columna_core import DuckDBConnector

    return DuckDBConnector(_load(fixture_warehouse_dir))


# ----------------------------------------------------------------------------
# The AFTERNOON fixture (2026-08-20) — the world DG-2 invariant 5 is certified against.
# ----------------------------------------------------------------------------
@pytest.fixture
def afternoon_server():
    """A PUBLISHED ManifoldServer over the Afternoon world (`fixtures/afternoon.cml`).

    Built in-process from `fixtures/afternoon_world.py` rather than from committed parquet, so the
    data, the arithmetic and the assertions are one readable artifact. `publish()` runs the real
    lifecycle (adjudicate, then witnesses) — the fixture is subject to the same certification law as
    production, not exempt from it."""
    import duckdb

    from columna_core import DuckDBConnector, ManifoldServer
    from columna_core.parser import parse_file

    import afternoon_world

    con = afternoon_world.build(duckdb.connect())
    m = parse_file(os.path.join(_TESTS_DIR, "fixtures", "afternoon.cml"))
    srv = ManifoldServer(m, DuckDBConnector(con))
    srv.publish()
    return srv


@pytest.fixture
def hand_manifold():
    """The hand-built benchmark Manifold — the single source of truth (imported from demos)."""
    from build_benchmark import build_manifold

    return build_manifold()


@pytest.fixture
def parsed_manifold():
    """The Manifold parsed from benchmark.cml (ingest-first path)."""
    from columna_core.parser import parse_file

    return parse_file(os.path.join(_DEMOS, "benchmark.cml"))


@pytest.fixture
def fixture_server(fixture_connector, hand_manifold):
    """A PUBLISHED ManifoldServer over the mini-warehouse, ready to answer frames.

    P0.5a (ruling 2026-08-11): this fixture now runs the same lifecycle production runs — construct,
    then `publish()` (the first-birth act: adjudicate strictly, then build witnesses). Before P0.5a it
    served unpublished, which under closed-by-default would mean no certified transport at all; and
    because the hand-built manifold used to carry no hierarchies, its edges were ungated and the whole
    fixture-backed suite was exempt from the certification law it is meant to police."""
    from columna_core import ManifoldServer

    srv = ManifoldServer(hand_manifold, fixture_connector)
    srv.publish()
    return srv


@pytest.fixture
def unpublished_fixture_server(fixture_connector, hand_manifold):
    """The same server BEFORE publish — for tests that must observe the pre-adjudication state
    (closed-by-default refusals, license=None on parse, the mint-at-publish transition)."""
    from columna_core import ManifoldServer

    return ManifoldServer(hand_manifold, fixture_connector)
