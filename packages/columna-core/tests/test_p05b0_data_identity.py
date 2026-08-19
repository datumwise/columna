"""
test_p05b0_data_identity.py — realization/data identity and cache safety (P0.5b-0).

The defect this pins closed: `table_version` was `f"{table}:{row_count}"`, and BOTH the
certification attestation and the engine result cache gated on it. A same-cardinality mutation —
an UPDATE, or a delete+insert of equal size — was therefore invisible: a CORROBORATED license
survived data that would have refuted it, and a cached frame could be served for data that no
longer existed.

The invariant:

> Any change to the realized data or realization that can change an adjudication finding or a
> served result must change the token used to validate that evidence and any cached result derived
> from it — to the strength of the guarantee the connector documents for that token. A native
> snapshot/version token is a source-provided identity; the DuckDB fallback is a content
> fingerprint / change detector, trustworthy for reuse but not collision-free.

That identity is NOT analytical identity: `F@A` is unchanged by a data refresh.
"""
import duckdb

from columna_core import ManifoldServer, DuckDBConnector
from columna_core.model import CORROBORATED, VERIFIED
from columna_core.adjudication import (scope_is_current, realized_tables, stale_capabilities,
                                       live_identities, scope_from_report, _route_tables)
from columna_core.parser import parse_manifold

_M = """
MANIFOLD di VERSION 1
UNIVERSE sales = day
LEVEL day   = day   BASE
LEVEL month = month
HIERARCHY calendar { day -> month VIA cal(day, month) }
MEASURE revenue ON sales FROM tx AS sum(amount)
"""


def _srv(rows=None, cal=None):
    con = duckdb.connect()
    con.execute("CREATE TABLE tx(day VARCHAR, amount DOUBLE)")
    con.executemany("INSERT INTO tx VALUES (?,?)", rows or [("d1", 10.0), ("d2", 20.0)])
    con.execute("CREATE TABLE cal(day VARCHAR, month VARCHAR)")
    con.executemany("INSERT INTO cal VALUES (?,?)", cal or [("d1", "m1"), ("d2", "m1")])
    srv = ManifoldServer(parse_manifold(_M), DuckDBConnector(con))
    srv.publish()
    return srv, con


def _total(srv, anchor="month"):
    fr = srv.frame(anchor).column("revenue", "revenue").run()
    if fr.data is None:
        return None
    return sum(float(r["revenue"]) for r in fr.data.iter_rows(named=True))


# ══ the connector contract ════════════════════════════════════════════════════════════════════
def test_row_count_alone_is_never_the_identity():
    """The headline defect, at the primitive. A same-cardinality UPDATE must move the identity;
    row count cannot see it, so row count is not a trustworthy fallback."""
    con = duckdb.connect()
    con.execute("CREATE TABLE tx(day VARCHAR, amount DOUBLE)")
    con.executemany("INSERT INTO tx VALUES (?,?)", [("d1", 10.0), ("d2", 20.0)])
    c = DuckDBConnector(con)

    before_id, before_count = c.data_identity("tx"), c.table_version("tx")
    con.execute("UPDATE tx SET amount = 999.0 WHERE day = 'd1'")
    after_id, after_count = c.data_identity("tx"), c.table_version("tx")

    assert before_count == after_count, "precondition: row count is blind to this change"
    assert after_id != before_id, "the change token must move when the content moves"


def test_same_cardinality_delete_insert_moves_the_identity():
    con = duckdb.connect()
    con.execute("CREATE TABLE tx(day VARCHAR, amount DOUBLE)")
    con.executemany("INSERT INTO tx VALUES (?,?)", [("d1", 10.0), ("d2", 20.0)])
    c = DuckDBConnector(con)
    before = c.data_identity("tx")
    con.execute("DELETE FROM tx WHERE day='d2'")
    con.execute("INSERT INTO tx VALUES ('d3', 20.0)")          # same cardinality, different content
    assert c.table_version("tx") == "tx:2"                     # row count unchanged
    assert c.data_identity("tx") != before


def test_unchanged_data_gives_a_stable_identity():
    """Reuse must remain possible: a stable identity over unchanged data is the whole point of
    having one rather than disabling caching outright."""
    con = duckdb.connect()
    con.execute("CREATE TABLE tx(day VARCHAR, amount DOUBLE)")
    con.executemany("INSERT INTO tx VALUES (?,?)", [("d1", 10.0), ("d2", 20.0)])
    c = DuckDBConnector(con)
    assert c.data_identity("tx") == c.data_identity("tx")


def test_duplicate_rows_do_not_cancel_the_digest():
    """An xor-only digest is defeated by duplicate rows: inserting an identical PAIR leaves the xor
    unchanged. The identity must carry more than xor, or it would be trivially forgeable."""
    con = duckdb.connect()
    con.execute("CREATE TABLE u(a VARCHAR)")
    con.executemany("INSERT INTO u VALUES (?)", [("p",), ("q",)])
    c = DuckDBConnector(con)
    before = c.data_identity("u")
    con.executemany("INSERT INTO u VALUES (?)", [("r",), ("r",)])   # xor-cancelling pair
    assert c.data_identity("u") != before


def test_identity_unavailable_returns_none_not_a_guess():
    """A source that cannot be identified yields None — the signal to fail closed for REUSE. It must
    never manufacture a token (e.g. fall back to row count)."""
    con = duckdb.connect()
    c = DuckDBConnector(con)
    assert c.data_identity("no_such_table") is None


# ══ cache safety ══════════════════════════════════════════════════════════════════════════════
def test_same_cardinality_mutation_cannot_serve_a_stale_cached_number():
    """The end-to-end defect. Warm the cache, mutate at equal cardinality, ask again. Before this
    unit the second answer was the FIRST answer, served from cache under an unchanged row count.

    The assertion is the RECOMPUTED VALUE, not merely "different": a refusal would also be
    "different", and would pass a weaker test while proving nothing about cache invalidation."""
    srv, con = _srv()
    assert _total(srv) == 30.0                                  # warm the cache
    before_count = srv.engine.con.table_version("tx")

    con.execute("UPDATE tx SET amount = 200.0 WHERE day = 'd2'")   # 30 -> 210, row count unchanged
    assert srv.engine.con.table_version("tx") == before_count      # the old primitive is blind

    fr = srv.frame("month").column("revenue", "revenue").run()
    assert fr.outcome in ("serve", "disclose"), f"expected a recomputed answer, got {fr.outcome}"
    assert _total(srv) == 210.0, "served a stale cached number after a same-cardinality mutation"


def test_a_table_no_proof_read_does_not_close_a_capability():
    """Currency is PER CAPABILITY. The hierarchy's evidence rests on `cal`; `tx` moving says nothing
    about whether day->month is still functional, so transport must stay admitted and simply
    recompute. (An early draft of this unit closed everything on any data change — over-broad.)"""
    srv, con = _srv()
    _total(srv)
    con.execute("UPDATE tx SET amount = 200.0 WHERE day = 'd2'")
    fr = srv.frame("month").column("revenue", "revenue").run()
    assert fr.outcome in ("serve", "disclose")
    assert srv.published_scope.edge_evidence, "edge evidence provenance was not recorded"
    assert all("tx" not in tabs for tabs in srv.published_scope.edge_evidence.values())


def test_an_unidentifiable_source_fails_closed_for_reuse():
    """A source that cannot provide a trustworthy version/change token must not have freshness
    manufactured for it. Reuse fails closed in BOTH consumers: nothing is cached (there is no token
    to validate a future hit against), and contingent evidence cannot be treated as current, so the
    capability closes and requires re-adjudication.

    This is the deliberate posture, not an accident: 'unknown' must never be read as 'unchanged'."""
    srv, con = _srv()
    _total(srv)
    srv.engine.cache.clear()
    srv.engine.con.data_identity = lambda table: None            # the source can no longer identify

    fr = srv.frame("month").column("revenue", "revenue").run()
    assert srv.engine.cache == {}, "stored a cache entry with no identity to validate it against"
    assert fr.outcome == "refuse", "treated an unidentifiable source as still-certified"
    assert fr.columns[0].refusal.classified().reason == "uncertified_edge"


# ══ evidence currency ═════════════════════════════════════════════════════════════════════════
def test_scope_records_the_identity_its_evidence_was_established_against():
    srv, _con = _srv()
    ids = srv.published_scope.attested_identities
    assert set(ids) == set(realized_tables(srv.m)) == {"cal", "tx"}
    assert all(v is not None for v in ids.values())
    assert scope_is_current(srv.published_scope, srv.engine.con)


def test_evidence_cannot_silently_remain_current_after_the_data_moves():
    """Contingent evidence may not outlive the data identity it was established against. After a
    same-cardinality change the scope is no longer current, and the capability closes through the
    EXISTING P0.5a ladder — no new reason code."""
    srv, con = _srv()
    assert _total(srv) == 30.0

    con.execute("UPDATE cal SET month = 'm2' WHERE day = 'd2'")   # the ATTESTED edge table moved
    assert not scope_is_current(srv.published_scope, srv.engine.con)

    fr = srv.frame("month").column("revenue", "revenue").run()
    assert fr.outcome == "refuse", "stale evidence still admitted transport"
    assert fr.columns[0].refusal.classified().reason == "uncertified_edge"


def test_re_attestation_restores_service_and_refreshes_the_identity():
    """Fail-closed must be recoverable, not a ratchet: re-attesting against the moved data
    re-establishes evidence and a new identity, and serving returns."""
    srv, con = _srv()
    _total(srv)
    before = dict(srv.published_scope.attested_identities)

    con.execute("UPDATE cal SET month = 'm2' WHERE day = 'd2'")
    assert srv.frame("month").column("revenue", "revenue").run().outcome == "refuse"

    srv.reattest()
    assert srv.published_scope.attested_identities != before
    assert scope_is_current(srv.published_scope, srv.engine.con)
    assert _total(srv) == 30.0                                   # same total, now lawfully re-established


def test_certification_and_cache_share_one_notion_of_identity():
    """Not two independent freshness heuristics: the engine's cache token for a table IS the
    identity the scope's evidence was established against."""
    srv, _con = _srv()
    _total(srv)
    for table, token in srv.published_scope.attested_identities.items():
        assert srv.engine.data_version(table) == token


def test_attestation_string_carries_the_data_identity_not_the_row_count():
    srv, _con = _srv()
    lic = srv.m.hierarchies[0].license
    assert lic.attestation is None or "cdg2/" in lic.attestation or "unavailable" in lic.attestation


# ══ what the token IS, and what it is namespaced by ═══════════════════════════════════════════
def test_the_token_is_namespaced_by_algorithm_and_duckdb_version():
    """The DuckDB token is a CONTENT FINGERPRINT, and DuckDB documents `hash()` as free to change
    between releases. Namespacing by fingerprint algorithm AND engine version makes such a change
    read as a conservative invalidation (a different token -> recompute), never as an ambiguous
    comparison of two digests that were never comparable."""
    import duckdb as _d
    con = duckdb.connect()
    con.execute("CREATE TABLE t(a INT)")
    tok = DuckDBConnector(con).data_identity("t")
    assert tok.startswith("cdg2/duckdb-"), tok
    assert _d.__version__ in tok or "unknown" in tok


def test_a_schema_qualified_table_can_still_be_identified():
    """A qualified (or quoted) binding must still yield a token. It returns None only when identity
    genuinely cannot be established — and `None` closes REUSE hard (no cache, and every capability
    resting on the table stops being current), so a name-parsing accident would take service down
    for a table that is perfectly identifiable."""
    con = duckdb.connect()
    con.execute("CREATE TABLE tx(a VARCHAR, b DOUBLE)")
    con.executemany("INSERT INTO tx VALUES (?,?)", [("d1", 10.0), ("d2", 20.0)])
    c = DuckDBConnector(con)
    plain, qualified = c.data_identity("tx"), c.data_identity("main.tx")
    assert qualified is not None, "a qualified table name yielded no identity"
    assert qualified == plain, "the same table identified differently under a qualified name"
    con.execute('CREATE TABLE "odd name"(a INT)')
    assert c.data_identity('"odd name"') is not None, "a quoted table name yielded no identity"


# ══ schema is part of the realized table state ════════════════════════════════════════════════
def test_a_column_name_permutation_moves_the_token():
    """THE REPRODUCED STALE-SERVE (review, 2026-08-19). Row hashing compares values POSITIONALLY,
    so permuting two column NAMES leaves every row hash — and therefore a content-only digest —
    byte-for-byte identical, while `sum(amount)` goes 30.0 -> 3.0. The change detector must see the
    realized table's ORDERED SCHEMA as well as its rows, or it certifies a table whose columns now
    mean something else."""
    con = duckdb.connect()
    con.execute("CREATE TABLE tx(amount DOUBLE, qty DOUBLE)")
    con.executemany("INSERT INTO tx VALUES (?,?)", [(10.0, 1.0), (20.0, 2.0)])
    c = DuckDBConnector(con)
    before = c.data_identity("tx")
    assert con.execute("SELECT sum(amount) FROM tx").fetchone()[0] == 30.0

    con.execute("ALTER TABLE tx RENAME amount TO _t")      # a pure name permutation: no row moves
    con.execute("ALTER TABLE tx RENAME qty TO amount")
    con.execute("ALTER TABLE tx RENAME _t TO qty")

    assert con.execute("SELECT sum(amount) FROM tx").fetchone()[0] == 3.0, "precondition: the served number moved"
    assert c.data_identity("tx") != before, "a column-name permutation left the token unmoved"


def test_a_type_widening_that_does_not_move_row_hashes_still_moves_the_token():
    """INT -> BIGINT leaves every row hash unchanged. It is still a change to the realized table
    state, and the schema half of the token is what catches it."""
    con = duckdb.connect()
    con.execute("CREATE TABLE ty(a INTEGER)")
    con.executemany("INSERT INTO ty VALUES (?)", [(10,), (20,)])
    c = DuckDBConnector(con)
    before = c.data_identity("ty")
    con.execute("ALTER TABLE ty ALTER a TYPE BIGINT")
    assert c.data_identity("ty") != before


def test_the_schema_half_does_not_make_unchanged_data_unstable():
    """Reuse must survive: schema in the token must not cost the stability that makes reuse possible."""
    con = duckdb.connect()
    con.execute("CREATE TABLE t(a VARCHAR, b DOUBLE)")
    con.executemany("INSERT INTO t VALUES (?,?)", [("d1", 10.0)])
    c = DuckDBConnector(con)
    assert c.data_identity("t") == c.data_identity("t")


# ══ evidence carries ITS OWN dependencies ═════════════════════════════════════════════════════
# The invariant (Huayin, 2026-08-19): contingent evidence must explicitly carry the data
# dependencies on which that evidence was established — reported BY the proof, not reconstructed
# from declarations afterwards. Serving also closes a moved edge first, but that is defence in
# depth; it is not the representation of a face proof's own currency.
_FACED = """
MANIFOLD shop VERSION 1
UNIVERSE sales = product * day BASIS events
UNIVERSE category_profile = category BASIS spine
LEVEL product = product_id BASE
LEVEL day = day BASE
LEVEL category = category_id BASE
LEVEL month = month
HIERARCHY calendar { day -> month VIA cal(day, month) }
RELATE product <-> category VIA product_categories(product_id, category_id)
    FACES {
        reach   = TOUCH -- "reaches every category"
        primary = ASSIGN BY priority ORDER MIN -- "top-priority, single-counted"
    }
MEASURE revenue ON sales FROM transactions AS sum(amount)
MEASURE priority ON category_profile FROM category_attributes VALUE priority FAMILY { last ORDER category }
"""
_PRIMARY = "product<->category.primary"
_REACH = "product<->category.reach"


def _faced_srv():
    con = duckdb.connect()
    con.execute("CREATE TABLE transactions AS SELECT * FROM (VALUES "
                "('p1','d1',60.0),('p2','d1',40.0)) AS t(product_id,day,amount)")
    con.execute("CREATE TABLE product_categories AS SELECT * FROM (VALUES "
                "('p1','c1'),('p1','c2'),('p2','c2')) AS t(product_id,category_id)")
    con.execute("CREATE TABLE category_attributes AS SELECT * FROM (VALUES "
                "('c1',1),('c2',2)) AS t(category_id,priority)")
    con.execute("CREATE TABLE cal AS SELECT * FROM (VALUES ('d1','m1')) AS t(day,month)")
    srv = ManifoldServer(parse_manifold(_FACED), DuckDBConnector(con))
    srv.publish()
    return srv, con


def test_evidence_records_the_tables_its_own_proof_read():
    """Not a superset reconstructed from the declarations: the exact read set each prover reported."""
    srv, _con = _faced_srv()
    sc = srv.published_scope
    assert sc.face_evidence[_PRIMARY] == ("category_attributes", "product_categories"), \
        "the assign proof read the bridge and its driver's home table — and must say so"
    assert sc.face_evidence[_REACH] == (), \
        "a TOUCH license is timeless (exact arithmetic, no data read), so it has NO data dependency"
    assert list(sc.edge_evidence.values()) == [("cal",)], \
        "the FD proof read the hop's provider table — and only that"


def test_a_face_goes_stale_through_its_own_recorded_dependency():
    """The face's driver home table moves. Its evidence must close BECAUSE THE FACE RECORDED THAT
    DEPENDENCY — not because some other capability happened to close first. Here nothing else can
    mask it: the hierarchy's own evidence (`cal`) is untouched and stays current."""
    srv, con = _faced_srv()
    sc = srv.published_scope
    con.execute("UPDATE category_attributes SET priority = 9 WHERE category_id = 'c1'")

    live = live_identities(srv.engine.con, sorted(sc.attested_identities))
    stale_e, stale_f = stale_capabilities(sc, live)
    assert _PRIMARY in stale_f, "the face outlived the data state its proof was established on"
    assert "category_attributes" in sc.face_evidence[_PRIMARY]      # through its OWN dependency
    assert not stale_e, "a driver-table move closed a hierarchy whose proof never read it"
    assert _REACH not in stale_f, "a timeless TOUCH license was closed by a data move"

    fr = srv.frame("category.primary").column("revenue", "revenue").run()
    assert fr.outcome == "refuse"
    assert fr.columns[0].refusal.classified().reason == "uncertified_face"


def test_a_hierarchy_move_does_not_close_a_face_that_never_read_it():
    """The other direction — capability-scoped, never global invalidation."""
    srv, con = _faced_srv()
    sc = srv.published_scope
    con.execute("UPDATE cal SET month = 'm2' WHERE day = 'd1'")

    stale_e, stale_f = stale_capabilities(sc, live_identities(srv.engine.con,
                                                             sorted(sc.attested_identities)))
    assert stale_e, "the hierarchy's own provider table moved and its evidence stayed current"
    assert not stale_f, "a hierarchy move closed a face whose proof never read that table"


def test_a_driver_route_provider_table_would_be_part_of_the_face_read_set():
    """The driver lemma pins a driver at the frontier grain, so TODAY a lawful face proof plans a
    route that crosses no edge (verified: the planned route's edge tuple is empty). The dependency
    threading must not therefore be untested — the day the lemma loosens, a route provider table is
    data the proof read. This pins the mechanism directly: a route WITH edges contributes its
    provider tables, and an absent route reports UNKNOWN (never an empty dependency set)."""
    srv, _con = _faced_srv()
    m = srv.m
    assert srv.planner.plan_routes("priority", ("category",))[0][("priority", "category")][1] == (), \
        "precondition: today's driver route crosses no edge"

    edge_key = next(e.key for e in m.edges)                        # the calendar day->month hop
    routes = {("priority", "category"): ("day", (edge_key,))}
    assert _route_tables(m, routes, "priority", "category") == ("cal",)
    assert _route_tables(m, {}, "priority", "category") is None, \
        "an unplanned route must read as UNKNOWN, so the caller can fall back conservatively"


def test_an_unreported_dependency_set_is_conservative_never_empty():
    """"Unknown dependency" must never collapse to "depends on nothing". A report carrying verdicts
    but no read sets (an older prover, a partial report) makes every certified capability depend on
    every realized table — over-invalidating, which is the safe direction."""
    srv, _con = _faced_srv()
    bare = {"_hierarchies": {"calendar": CORROBORATED},
            "_faces": {_PRIMARY: CORROBORATED, _REACH: VERIFIED}}
    sc = scope_from_report(srv.m, bare)
    every = tuple(realized_tables(srv.m))
    assert sc.face_evidence[_PRIMARY] == every
    assert sc.face_evidence[_REACH] == every
    assert all(v == every for v in sc.edge_evidence.values())


# ══ cache currency ≠ evidence currency ════════════════════════════════════════════════════════
# Two dependency sets over one primitive (Huayin, 2026-08-19):
#   evidence      — what a PROOF read; decides whether a finding is still current.
#   computation   — what a COMPUTATION read; decides whether a RESULT may be reused.
# TOUCH is the case that separates them: its license is timeless (no data read, empty evidence
# set), while its result depends on the M:N bridge. Keyed on the measure home table alone, a bridge
# edit re-served the pre-edit frame under a correctly-current license.
_TOUCH_M = """
MANIFOLD shop VERSION 1
UNIVERSE sales = product * day BASIS events
LEVEL product = product_id BASE
LEVEL day = day BASE
LEVEL category = category_id BASE
RELATE product <-> category VIA product_categories(product_id, category_id)
    FACES { reach = TOUCH -- "reaches every category" }
MEASURE revenue ON sales FROM transactions AS sum(amount)
"""


def _touch_srv(bridge="('p1','c1'),('p2','c2')"):
    con = duckdb.connect()
    con.execute("CREATE TABLE transactions AS SELECT * FROM (VALUES "
                "('p1','d1',100.0),('p2','d1',40.0)) AS t(product_id,day,amount)")
    con.execute(f"CREATE TABLE product_categories AS SELECT * FROM (VALUES {bridge}) "
                f"AS t(product_id,category_id)")
    srv = ManifoldServer(parse_manifold(_TOUCH_M), DuckDBConnector(con))
    srv.publish()
    return srv, con


def _touched(srv):
    fr = srv.frame("category.reach").column("revenue", "revenue").run()
    assert fr.outcome in ("serve", "disclose"), fr.outcome
    return {r["category.reach"]: float(r["revenue"]) for r in fr.data.iter_rows(named=True)
            if r["revenue"] is not None}


def test_a_bridge_edit_cannot_serve_a_cached_crossing():
    """THE REGRESSION. Serve through a TOUCH crossing, mutate ONLY the bridge at equal cardinality,
    ask again. The license stays current (correctly — it is timeless), so nothing else closes and
    nothing else can mask a cache hit: the result cache itself must see the bridge move."""
    srv, con = _touch_srv()
    assert _touched(srv) == {"c1": 100.0, "c2": 40.0}
    before = srv.engine.data_version("transactions")

    con.execute("UPDATE product_categories SET category_id = 'c3' WHERE product_id = 'p2'")
    assert srv.engine.con.data_identity("transactions") == before, \
        "precondition: the measure's own table did not move"
    assert srv.published_scope.face_evidence["product<->category.reach"] == (), \
        "precondition: the TOUCH license is timeless and stays current"

    assert _touched(srv) == {"c1": 100.0, "c3": 40.0}, "served a cached crossing across a moved bridge"


def test_an_unchanged_bridge_still_permits_reuse():
    """The control. Widening the dependency set must not disable reuse — a second identical request
    over unchanged data is still a cache hit."""
    srv, _con = _touch_srv()
    assert _touched(srv) == {"c1": 100.0, "c2": 40.0}
    hits = srv.engine.stats.cache_hits
    assert _touched(srv) == {"c1": 100.0, "c2": 40.0}
    assert srv.engine.stats.cache_hits == hits + 1, "unchanged computation dependencies stopped reuse"


def test_the_cache_token_carries_every_computation_dependency():
    """The token is the whole dependency set, not one table: both the measure home table and the
    bridge participate, so either one moving invalidates."""
    srv, _con = _touch_srv()
    _touched(srv)
    tok = next(iter(srv.engine.cache.values())).version
    assert "transactions@" in tok and "product_categories@" in tok, tok


_CARVE = """MANIFOLD t VERSION 1
LEVEL store = store_id BASE ATTR opened = stores.opened_date
LEVEL region = region_id
LEVEL day = day BASE
UNIVERSE inv = store * day WHERE day >= store.opened BASIS spine
HIERARCHY location { store -> region VIA stores(store_id, region_id) }
MEASURE stock ON inv FROM snap VALUE level
    FAMILY { last ORDER day }"""


def _carve_srv():
    con = duckdb.connect()
    con.execute("CREATE TABLE stores(store_id VARCHAR, region_id VARCHAR, opened_date VARCHAR)")
    con.executemany("INSERT INTO stores VALUES (?,?,?)", [("S1", "R1", "2024-01-10")])
    con.execute("CREATE TABLE snap(store_id VARCHAR, day VARCHAR, level DOUBLE)")
    con.executemany("INSERT INTO snap VALUES (?,?,?)",
                    [("S1", "2024-01-05", 99.0), ("S1", "2024-01-15", 10.0)])
    srv = ManifoldServer(parse_manifold(_CARVE), DuckDBConnector(con))
    srv.publish()
    return srv, con


def test_a_predicate_attribute_table_is_a_computation_dependency():
    """The same defect class beyond TOUCH: a universe predicate confines the population by reading
    an ATTRIBUTE PROVIDER (`day >= store.opened` -> `stores.opened_date`). That table is not the
    measure's home table and not on any transport route, so a home-table-only cache key could
    re-serve a carve that no longer holds."""
    srv, con = _carve_srv()
    def stock():
        fr = srv.frame("store").column("stock", "stock.last").run()
        return dict(zip(fr.data["store"], fr.data["stock"]))
    assert stock() == {"S1": 10.0}                    # the pre-open 99.0 snapshot is carved
    before = srv.engine.data_version("snap")

    con.execute("UPDATE stores SET opened_date = '2024-01-01'")   # S1 now opened before both snaps
    assert srv.engine.con.data_identity("snap") == before, "precondition: the measure's table is unmoved"
    tok = next(iter(srv.engine.cache.values())).version
    assert "stores@" in tok, "the carve's attribute provider is not in the cache token"

    assert stock() == {"S1": 10.0}, "last-by-day is still the 2024-01-15 snapshot"
    assert srv.engine.stats.cache_hits == 0, "reused a result across a moved predicate dependency"


def _tapped_reads(srv, run):
    """Run `run` with the connector's whole delivery surface tapped; return (tables actually read,
    tables the engine declared the cached result depends on)."""
    eng = srv.engine
    real, seen = eng.con, set()

    class _Tap:
        def __getattr__(self, name):
            attr = getattr(real, name)
            if not name.startswith("deliver_"):
                return attr
            def tapped(table, *a, **k):
                seen.add(table)
                return attr(table, *a, **k)
            return tapped

    eng.cache.clear()
    eng.con = _Tap()
    try:
        run()
    finally:
        eng.con = real
    declared = {d.split("@", 1)[0] for d in next(iter(eng.cache.values())).version.split("|")}
    return seen, declared


def test_the_declared_computation_set_is_what_the_computation_actually_reads():
    """COMPLETENESS, pinned empirically rather than argued. The dependency set is composed from the
    plan (home table · planned-route provider tables · faced bridge · universe-predicate attribute
    providers). These tap the connector's whole delivery surface across the three shapes that read
    beyond the home table, and assert that what the computation READ is exactly what the engine
    declared it depends on — so a future read path that escapes the declaration fails HERE instead
    of silently under-invalidating a cached result."""
    touch_srv, _c1 = _touch_srv()
    seen, declared = _tapped_reads(touch_srv, lambda: _touched(touch_srv))
    assert seen == declared == {"transactions", "product_categories"}, (seen, declared)

    hier_srv, _c2 = _srv()                                   # day -> month, one transport hop
    seen, declared = _tapped_reads(hier_srv, lambda: _total(hier_srv))
    assert seen == declared == {"tx", "cal"}, (seen, declared)

    carve_srv, _c3 = _carve_srv()                            # universe predicate over an attribute
    seen, declared = _tapped_reads(
        carve_srv, lambda: carve_srv.frame("store").column("stock", "stock.last").run())
    assert seen == declared == {"snap", "stores"}, (seen, declared)
