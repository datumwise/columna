"""
test_witness_non_interference.py — STANDING RULES for materialized measure state.

These test the RULE, not the workaround. Each one states a governed obligation in its name and
fails if that obligation stops holding, however the implementation is later reorganised:

  1. A carved universe stays carved in materialized state — eager and lazy alike.
  2. Unknown data identity never reads as unchanged, and never becomes stored state.
  3. Materialized-state currency uses the COMPLETE computation dependency set.

WHY EACH EXISTS. All three were live defects, reproduced under the real runtime on 2026-08-29:

  · `_build_base_sketches` delivered base rows without confining them, so a distinct count over a
    restricted universe served the UNCONFINED population — 3 where the carve admits 1 — while its
    own disclosure asserted `[over <universe>]`. Values were wrong and nothing said so, because a
    distinct count carries no row a caller could inspect.
  · `WitnessStore.fresh` compared `None == None` and reported a stale witness as current. A real
    data mutation was invisible: the answer stayed 2 against a ground truth of 3, at ZERO backend
    fetches. The result cache, built on the same identity primitive, was fail-CLOSED throughout —
    one primitive, two opposite polarities.
  · Witness currency was `data_version(home_table)` alone, so a change to a universe-predicate
    provider correctly re-derived the monoid answer and left the witness "fresh".

The first two were latent in each other: the witness never read the predicate, so its content
genuinely depended on the home table alone, and the two defects cancelled into one wrong answer.
Fixing confinement without widening currency would have converted a cancelled defect into an
active staleness bug — which is why they are tested together here.
"""
import duckdb
import pytest

from columna_core import ManifoldServer, DuckDBConnector
from columna_core.parser import parse_manifold
from columna_core.sketch import Witness, WitnessStore

# A universe that genuinely carves: s1 opened 2024-01-05, so its first two transactions
# (u1, u2) are OUTSIDE the declared population and u3 is inside it, twice.
MANIFOLD = """
MANIFOLD carve VERSION 1
UNIVERSE sales = store * day WHERE day >= store.opened BASIS events
LEVEL store = store_id BASE ATTR opened = stores.opened_date
LEVEL day = day BASE
LEVEL region = region
HIERARCHY geo { store -> region VIA stores(store_id, region) }
MEASURE revenue ON sales FROM transactions AS sum(amount)
MEASURE buyers  ON sales FROM transactions AS distinct(customer_id)
"""

CONFINED_BUYERS = {"s1": 1, "s2": 1}       # u3 only, at s1
UNCONFINED_BUYERS = {"s1": 3, "s2": 1}     # u1, u2, u3 — what reading outside the carve returns


def _warehouse():
    con = duckdb.connect()
    con.execute("""CREATE TABLE transactions AS SELECT * FROM (VALUES
       ('s1','2024-01-01','u1',10.0),
       ('s1','2024-01-02','u2',20.0),
       ('s1','2024-01-05','u3',30.0),
       ('s1','2024-01-06','u3',40.0),
       ('s2','2024-01-01','u7',7.0))
       AS t(store_id, day, customer_id, amount)""")
    con.execute("""CREATE TABLE stores AS SELECT * FROM (VALUES
       ('s1','2024-01-05','r1'), ('s2','2024-01-01','r1')) AS t(store_id, opened_date, region)""")
    return con


def _server(con, connector=None):
    srv = ManifoldServer(parse_manifold(MANIFOLD), connector or DuckDBConnector(con))
    srv.publish()
    return srv


def _buyers_at_store(srv):
    fr = srv.planner.run(("store",), [("buyers", "buyers")], None)
    assert fr.data is not None, [c.refusal for c in fr.columns]
    return {r["store"]: round(r["buyers"]) for r in fr.data.to_dicts()}


# ── 1. a carved universe stays carved in materialized state ───────────────────────────────────

def test_the_carve_is_observable_at_all():
    """Guards the fixture itself. If confined and unconfined agreed, every test below would pass
    vacuously — which is exactly how a confinement defect survives a green suite."""
    assert CONFINED_BUYERS != UNCONFINED_BUYERS


def test_published_witness_is_confined_to_the_universe():
    """The EAGER path: sketches materialized at publish must hold only in-universe points."""
    srv = _server(_warehouse())
    assert _buyers_at_store(srv) == CONFINED_BUYERS


def test_lazy_sketch_build_is_confined_to_the_universe():
    """The LAZY path (no witness present) must confine identically. Two code paths, one law —
    they were wrong together, so they are tested apart."""
    srv = _server(_warehouse())
    srv.engine.witnesses._w.clear()
    srv.engine.cache.clear()
    assert _buyers_at_store(srv) == CONFINED_BUYERS


def test_sketch_and_monoid_paths_agree_on_the_same_universe():
    """The monoid path always confined. A sketch measure on the SAME universe must not answer a
    different population from a sum measure on it."""
    srv = _server(_warehouse())
    fr = srv.planner.run(("store",), [("revenue", "revenue")], None)
    revenue = {r["store"]: float(r["revenue"]) for r in fr.data.to_dicts()}
    assert revenue == {"s1": 70.0, "s2": 7.0}          # not 100.0 — u1/u2 are outside the carve
    assert _buyers_at_store(srv) == CONFINED_BUYERS


# ── 2. unknown data identity fails closed ─────────────────────────────────────────────────────

class _NoIdentityConnector(DuckDBConnector):
    """A backend that cannot establish a trustworthy identity for its tables. Permitted by the
    connector contract: `None` is not a failure to serve, it is a failure to REUSE."""

    def data_identity(self, table):
        return None


def test_unknown_identity_never_reads_as_fresh():
    """`None == None` must not report currency — the exact comparison that served a stale sketch
    as current, at zero backend fetches.

    `_w` is populated DIRECTLY, bypassing `put`. The two guards are independent obligations and are
    tested independently: `put` refuses to create this state, and `fresh` must still refuse to
    trust it if it arrives by any other route (a durable store, a restored snapshot, a future
    caller). Asserting through `put` would test the wrong guard and pass against the defect."""
    store = WitnessStore()
    unversioned = Witness("m", "distinct", "store", 12, None, {})
    store._w[("m", "distinct", "store")] = unversioned
    assert store.fresh("m", "distinct", "store", None) is False
    assert store.fresh("m", "distinct", "store", "v1") is False


def test_unknown_identity_is_never_stored():
    """Unknown identity closes STORAGE, not merely reuse. A witness stored without a version can
    never be shown stale, so storing one converts a missing identity into a permanent freshness
    claim."""
    store = WitnessStore()
    assert store.put(Witness("m", "distinct", "store", 12, None, {})) is False
    assert len(store) == 0
    assert store.fresh("m", "distinct", "store", None) is False


def test_publish_stores_no_witness_when_identity_is_unavailable():
    con = _warehouse()
    srv = _server(con, connector=_NoIdentityConnector(con))
    assert len(srv.engine.witnesses) == 0


def test_unknown_identity_does_not_serve_a_stale_number():
    """The end-to-end rule. With no trustworthy identity the engine must recompute rather than
    reuse — a mutation must become visible, at the cost of a fetch."""
    con = _warehouse()
    srv = _server(con, connector=_NoIdentityConnector(con))
    assert _buyers_at_store(srv) == CONFINED_BUYERS

    # a genuinely new in-universe distinct customer at s1
    con.execute("INSERT INTO transactions VALUES ('s1','2024-01-07','u9',5.0)")
    srv.engine.cache.clear()
    assert _buyers_at_store(srv) == {"s1": 2, "s2": 1}


# ── 3. currency uses the complete computation dependency set ──────────────────────────────────

def test_witness_currency_covers_the_predicate_provider():
    """A restricted universe makes the witness depend on the predicate's provider table. Moving
    that table must stale the witness, exactly as it stales the result cache."""
    con = _warehouse()
    srv = _server(con)
    assert _buyers_at_store(srv) == CONFINED_BUYERS

    # widen s1's carve by moving the PREDICATE PROVIDER only; transactions is untouched.
    con.execute("UPDATE stores SET opened_date = '2024-01-01' WHERE store_id = 's1'")
    srv.planner._refresh_scope_currency()
    srv.engine.cache.clear()
    assert _buyers_at_store(srv) == UNCONFINED_BUYERS   # now genuinely in-universe, not stale reuse


def test_witness_version_is_the_result_cache_token_not_the_home_table_token():
    """THE RULE, not the workaround: one currency notion for both kinds of materialized state.

    Asserted structurally rather than by value, so a later reorganisation that keeps the rule
    still passes and one that quietly narrows the witness back to its home table still fails."""
    srv = _server(_warehouse())
    meas = srv.engine.m.measures["buyers"]
    w = srv.engine.witnesses.get("buyers", "distinct", "store")
    assert w is not None
    expected = srv.engine.data_version_of(srv.engine.computation_tables(meas))
    assert w.version == expected
    # and the dependency set is genuinely wider than the home table alone
    assert srv.engine.computation_tables(meas) > {meas.home_table}
    assert w.version != srv.engine.data_version(meas.home_table)
