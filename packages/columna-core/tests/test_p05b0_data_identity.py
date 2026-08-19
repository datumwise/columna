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
from columna_core.adjudication import scope_is_current, realized_tables
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
    assert lic.attestation is None or "cdg1/" in lic.attestation or "unavailable" in lic.attestation


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
    assert tok.startswith("cdg1/duckdb-"), tok
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
