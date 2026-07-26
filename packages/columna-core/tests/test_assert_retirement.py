"""
test_assert_retirement.py — the 0.13.0 ASSERT retirement, pinned in BOTH directions.

Ruling `specs/assert_retirement_ruling_v0_1.md` (Huayin, 2026-07-26): ASSERT retires from the Manifold
entirely — both shipped forms, plus by CASCADE the standalone `ATTR <names> ON <universe>` whose sole
consumer was the row-form assert. The doctrine is the admission test: *a construct is admitted iff its
prover licenses some serving behavior.*

A retirement is only real if both directions are provoked, so this suite provokes both:

  (1) the teaching refusal FIRES on every retired form, and its MESSAGE names the ruling and the
      0.13.0 release note — a bare `ParseError` would be a syntax complaint, and the point of the
      refusal is that the author made a CATEGORY mistake, not a typo;
  (2) the cascade BOUNDARY holds — inline `LEVEL … ATTR` parses AND serves. It did not retire (a
      universe predicate loads on it, so its prover licenses serving), and it is the one thing a
      careless removal breaks, because it shares the `ATTR` token with the form that did retire.

The tombstoned `conflicting_data` reason has its own pin in test_scope_edit.py.
"""
import duckdb
import pytest

import columna_core
from columna_core import ManifoldServer, DuckDBConnector
from columna_core.parser import parse_manifold, ParseError


_BASE = """MANIFOLD t VERSION 1
LEVEL store = store_id BASE
LEVEL day = day BASE
UNIVERSE sales = store * day BASIS events
MEASURE revenue ON sales FROM tx AS sum(amount)
MEASURE units ON sales FROM tx AS sum(units)
"""

# the three retired forms: row assert, aggregate assert, standalone universe row-attributes
_ROW_ASSERT = "ASSERT nonneg ON sales WHERE units >= 0"
_AGG_ASSERT = "ASSERT recon ON sales AT store HOLDS revenue <= units"
_STANDALONE_ATTR = "ATTR units, units_returned ON sales"


@pytest.mark.parametrize("retired", [_ROW_ASSERT, _AGG_ASSERT, _STANDALONE_ATTR],
                         ids=["row-assert", "aggregate-assert", "standalone-attr"])
def test_the_teaching_refusal_fires_and_names_the_ruling(retired):
    with pytest.raises(ParseError) as ei:
        parse_manifold(_BASE + retired + "\n")
    msg = str(ei.value)
    # it is a TEACHING refusal, not a syntax complaint: the doctrine, the ruling, the release note
    assert "retired in 0.13" in msg
    assert "licenses no serving behavior" in msg
    assert "Ruling 2026-07-26" in msg
    assert "0.13.0 release note" in msg


def test_the_assert_refusal_carries_the_full_doctrine_string():
    # ASSERT gets the FULL refusal (ruling §3, ratified verbatim) — the admission test in one sentence
    # plus where contracts actually belong.
    with pytest.raises(ParseError) as ei:
        parse_manifold(_BASE + _ROW_ASSERT + "\n")
    assert str(ei.value) == (
        "ASSERT was retired in 0.13 — everything a Manifold's trial proves is a precondition of "
        "something it serves, and a data contract licenses no serving behavior. Contracts belong to "
        "the attestation layer, upstream of the Manifold. (Ruling 2026-07-26; see the 0.13.0 release "
        "note.)")


def test_the_standalone_attr_refusal_cites_the_cascade_and_spares_the_inline_form():
    with pytest.raises(ParseError) as ei:
        parse_manifold(_BASE + _STANDALONE_ATTR + "\n")
    msg = str(ei.value)
    assert "CASCADE" in msg and "row-form ASSERT" in msg    # WHY it went: not its own failing, the cascade
    assert "UNAFFECTED" in msg and "LEVEL" in msg           # and WHERE the author's ATTR still works


def test_the_refusal_lands_on_the_retired_line_not_on_its_predecessor():
    # ASSERT left `_KW` (the active grammar) but is still a STATEMENT HEAD for splitting, so a document
    # written against the old grammar meets the refusal AT the retired line instead of dissolving into
    # a confusing complaint about the MEASURE it happens to follow.
    with pytest.raises(ParseError) as ei:
        parse_manifold(_BASE + _AGG_ASSERT + "\n")
    assert "MEASURE" not in str(ei.value) and "bad" not in str(ei.value)


def test_the_construct_left_the_public_surface_entirely():
    # removed, not mothballed (ruling §2): unreachable machinery is where the next fossil grows.
    for gone in ("Assert", "AssertContradiction", "AssertNotWellFormed", "describe_assert"):
        assert not hasattr(columna_core, gone), f"{gone} survived the retirement"
    assert "ASSERT_OPS" not in dir(columna_core.parser)


# ── the CASCADE BOUNDARY: inline `LEVEL … ATTR` did NOT retire ─────────────────────────────────────
_INLINE = """MANIFOLD t VERSION 1
LEVEL store = store_id BASE ATTR opened = stores.opened_date
LEVEL region = region_id
LEVEL day = day BASE
UNIVERSE inv = store * day WHERE day >= store.opened BASIS spine
HIERARCHY location { store -> region VIA stores(store_id, region_id) }
MEASURE stock ON inv FROM snap VALUE level
    FAMILY { last ORDER day }"""


def test_inline_level_attr_still_parses_and_stays_logical():
    m = parse_manifold(_INLINE)
    assert m.levels["store"].attributes == (("opened", "stores.opened_date"),)
    ref = m.universes["inv"].predicate.comparisons[0].right
    assert (ref.table, ref.column) == ("store", "opened")   # the LOGICAL attribute, not the binding


def test_inline_level_attr_still_SERVES_a_universe_predicate_that_loads_on_it():
    # the boundary proven by SERVING, not by parsing: the predicate must still carve the population
    # against the physical binding. This is the prover-licenses-serving case the ruling protects.
    con = duckdb.connect()
    con.execute("CREATE TABLE stores(store_id VARCHAR, region_id VARCHAR, opened_date VARCHAR)")
    con.executemany("INSERT INTO stores VALUES (?,?,?)",
                    [("S1", "R1", "2024-01-10"), ("S2", "R1", "2024-01-01")])
    con.execute("CREATE TABLE snap(store_id VARCHAR, day VARCHAR, level DOUBLE)")
    con.executemany("INSERT INTO snap VALUES (?,?,?)",
                    [("S1", "2024-01-05", 99.0),      # PRE-open -> outside the population, must be carved
                     ("S1", "2024-01-15", 10.0), ("S2", "2024-01-15", 20.0)])
    server = ManifoldServer(parse_manifold(_INLINE), DuckDBConnector(con))
    fr = server.frame("store").column("stock", "stock.last").run()
    assert fr.outcome in ("serve", "disclose") and fr.columns[0].refusal is None
    assert dict(zip(fr.data["store"], fr.data["stock"])) == {"S1": 10.0, "S2": 20.0}
