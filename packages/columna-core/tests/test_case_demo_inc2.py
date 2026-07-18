"""
test_case_demo_inc2.py — Cascadia increment 2 language/engine additions.

 • universe ROW-attributes (`ATTR units, units_returned ON transaction`) — the ruled extension of the
   OF-9 machinery to universes, so a ROW-form ASSERT renders purely logically while the map records the
   binding.
 • the ENGINE resolution of a LOGICAL attribute in a predicate — `day >= store.opened` actually CONFINES
   the population against the physical binding (`stores.opened_date`), carving pre-open snapshots.
"""
import duckdb
import pytest

from columna_core import (ManifoldServer, DuckDBConnector, logical_spec, physical_map)
from columna_core.parser import parse_manifold, ParseError


# ── universe row-attributes ──────────────────────────────────────────────────────────────────────────
_M = """MANIFOLD t VERSION 1
LEVEL day = day BASE
UNIVERSE transaction = day BASIS events
ATTR units, units_returned = tx.returned ON transaction
MEASURE units_sold ON transaction FROM tx AS sum(units)
ASSERT returns_bounded ON transaction WHERE units_returned <= units"""


def test_universe_row_attributes_parse_with_shared_and_explicit_bindings():
    m = parse_manifold(_M)
    attrs = dict(m.universes["transaction"].attributes)
    assert attrs["units"] == "units"            # shared spelling
    assert attrs["units_returned"] == "tx.returned"   # explicit binding


def test_row_assert_renders_logically_binding_lives_on_the_map():
    m = parse_manifold(_M)
    a = logical_spec(m)["asserts"][0]
    assert a["form"]["predicate"] == "units_returned <= units"     # no physical spelling
    rows = {r["logical"]: r["binds_to"] for r in physical_map(m)}
    assert rows["transaction.units"] == "tx.units"                 # shared spelling qualified to the home table
    assert rows["transaction.units_returned"] == "tx.returned"     # explicit binding kept
    # the wall: the logical spec never shows the physical binding
    import json
    assert "tx.returned" not in json.dumps(logical_spec(m))


def test_row_attribute_disambiguates_a_same_named_measure():
    # a measure named `units_returned` AND a row-attribute `units_returned` coexist; the assert names
    # the row-attribute, so it is well-formed (the measure would be rejected as impure).
    cml = _M.replace("MEASURE units_sold ON transaction FROM tx AS sum(units)",
                     "MEASURE units_sold ON transaction FROM tx AS sum(units)\n"
                     "MEASURE units_returned ON transaction FROM tx AS sum(returned)")
    m = parse_manifold(cml)         # parses clean — the row-attribute disambiguates
    assert "units_returned" in m.measures and "units_returned" in dict(m.universes["transaction"].attributes)


def test_attr_on_unknown_universe_is_rejected():
    with pytest.raises(ParseError) as ei:
        parse_manifold("MANIFOLD t VERSION 1\nLEVEL day = day BASE\n"
                        "UNIVERSE u = day BASIS events\nATTR x ON nonesuch\n"
                        "MEASURE m ON u FROM tx AS sum(v)")
    assert "unknown universe 'nonesuch'" in str(ei.value)


# ── the engine carve (logical attribute in a predicate confines the population) ───────────────────────
_CARVE = """MANIFOLD t VERSION 1
LEVEL store = store_id BASE ATTR opened = stores.opened_date
LEVEL region = region_id
LEVEL day = day BASE
UNIVERSE inv = store * day WHERE day >= store.opened BASIS spine
HIERARCHY location { store -> region VIA stores(store_id, region_id) }
MEASURE stock ON inv FROM snap VALUE level
    FAMILY { last ORDER day }"""


def test_logical_attribute_predicate_carves_pre_open_snapshots():
    con = duckdb.connect()
    con.execute("CREATE TABLE stores(store_id VARCHAR, region_id VARCHAR, opened_date VARCHAR)")
    con.executemany("INSERT INTO stores VALUES (?,?,?)",
                    [("S1", "R1", "2024-01-10"), ("S2", "R1", "2024-01-01")])
    con.execute("CREATE TABLE snap(store_id VARCHAR, day VARCHAR, level DOUBLE)")
    con.executemany("INSERT INTO snap VALUES (?,?,?)",
                    [("S1", "2024-01-05", 99.0),      # PRE-open (2024-01-05 < S1.opened 2024-01-10) -> carved
                     ("S1", "2024-01-15", 10.0), ("S2", "2024-01-15", 20.0)])
    s = ManifoldServer(parse_manifold(_CARVE), DuckDBConnector(con))
    r = s.frame("store").column("stock", "stock.last").run()
    got = dict(zip(r.data["store"], r.data["stock"]))
    assert got["S1"] == 10.0 and got["S2"] == 20.0   # the 99.0 pre-open snapshot was carved by day >= store.opened
