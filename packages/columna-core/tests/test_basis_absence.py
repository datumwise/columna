"""
test_basis_absence.py — B3 absence semantics (WP on-ramp/Explorer tier-2, CP-1 increment 6).

The basis type determines what ABSENCE means, and serving follows the DECLARATION (like a B-anchor
bar, independent of any License). Absence is only definable relative to a DOMAIN; the juxtaposition
(the full-outer align of columns from different universes) supplies one locally, so a column's null
cells take meaning from THAT column's own universe basis:
  · events   -> absence is the honest ZERO (zero-fill + an immaterial note)
  · spine/product -> absence is a GAP (a material `incomplete_data` caveat)
  · registry / undeclared -> no serving change
One characterization pin per basis type (rider i). Adjudication mints an UNTESTABLE testedness record
per type; the live refutation channels (spine internal-contiguity, completeness) ride the spine-grid
(open_forks OF-5). The demo stays basis-less this increment (rider ii).
"""
import duckdb
import polars as pl

from columna_core import ManifoldServer, DuckDBConnector, UNTESTABLE, adjudicate
from columna_core import disclosure_wire as dw
from columna_core.parser import parse_manifold


def _lit(v):
    return "'" + v.replace("'", "''") + "'" if isinstance(v, str) else repr(v)


def _server(text, tables):
    con = duckdb.connect()
    for name, (cols, rows) in tables.items():
        values = ", ".join("(" + ", ".join(_lit(v) for v in r) + ")" for r in rows)
        con.execute(f"CREATE TABLE {name} AS SELECT * FROM (VALUES {values}) AS t({', '.join(cols)})")
    return ManifoldServer(parse_manifold(text), DuckDBConnector(con))


def _mk(ev_basis="events", sp_basis="spine"):
    return f"""
MANIFOLD b VERSION 1
UNIVERSE ev = store * day BASIS {ev_basis}
UNIVERSE sp = store * day BASIS {sp_basis}
LEVEL store = store_id BASE
LEVEL day   = day      BASE
MEASURE orders ON ev FROM tx  AS count(*)
MEASURE level  ON sp FROM inv AS sum(lvl)
"""


# tx has (s1,d1); inv has (s1,d2) — so the juxtaposed align has a null in each column at the other cell.
_TABLES = {"tx":  (["store_id", "day"], [("s1", "d1")]),
           "inv": (["store_id", "day", "lvl"], [("s1", "d2", 5.0)])}


def _cell(data, day, colname):
    return data.filter((pl.col("store") == "s1") & (pl.col("day") == day))[colname][0]


def test_events_absence_is_zero_filled_with_an_immaterial_note():
    fr = _server(_mk(), _TABLES).frame("store", "day").column("orders", "orders").column("level", "level").run()
    ocol = next(c for c in fr.columns if c.name == "orders")
    # the absent (s1,d2) events cell is rendered as 0 (the honest zero), not null
    assert _cell(fr.data, "d2", "orders") == 0
    note = [cav for cav in ocol.disclosure.caveats if "rendered as 0 per events basis" in cav.detail]
    assert note and note[0].severity != "critical"          # immaterial, agent-legible


def test_spine_absence_is_a_material_gap():
    fr = _server(_mk(), _TABLES).frame("store", "day").column("orders", "orders").column("level", "level").run()
    lcol = next(c for c in fr.columns if c.name == "level")
    assert any(cav.category == "data_gap" for cav in lcol.disclosure.caveats)
    # a MATERIAL gap caveat drives the wire outcome to disclose (materiality, not severity)
    assert dw.wire_frame(fr)["outcome"] == "disclose"


def test_product_basis_shares_spines_gap_semantics():
    fr = _server(_mk(sp_basis="product"), _TABLES).frame("store", "day").column(
        "orders", "orders").column("level", "level").run()
    lcol = next(c for c in fr.columns if c.name == "level")
    assert any(cav.category == "data_gap" for cav in lcol.disclosure.caveats)


def test_registry_and_undeclared_basis_do_not_touch_serving():
    for sp in ("registry", "events"):     # registry: no gap/fill; events on both: no gap (zero instead)
        fr = _server(_mk(sp_basis=sp), _TABLES).frame("store", "day").column(
            "orders", "orders").column("level", "level").run()
        lcol = next(c for c in fr.columns if c.name == "level")
        assert not any(cav.category == "data_gap" for cav in lcol.disclosure.caveats)


def test_single_column_frame_has_no_absence_edit():
    # no juxtaposition -> no local domain -> no null cells -> no fill/gap (absence rides the spine-grid).
    fr = _server(_mk(), _TABLES).frame("store", "day").column("orders", "orders").run()
    ocol = next(c for c in fr.columns if c.name == "orders")
    assert not any("events basis" in cav.detail for cav in ocol.disclosure.caveats)


def test_basis_adjudication_mints_untestable_per_type():
    srv = _server(_mk(), _TABLES)
    report = adjudicate(srv)
    assert report["_basis"] == {"ev": UNTESTABLE, "sp": UNTESTABLE}
    assert srv.m.universes["ev"].basis_license.verdict == UNTESTABLE
    assert "events basis asserted" in srv.m.universes["ev"].basis_license.basis
