"""Absence semantics — driven by the DECLARED member fill rule Φ_v (columna#143 step 3), NOT by
universe basis. The basis-keyed default is retired: a 0-fill keyed on basis alone was a silent wrong
number for a state-valued measure (D4). A measure's `FILL` clause now decides what an absent cell means:

  · FILL zero      -> absent cell 0-filled (declared nil) + an IMMATERIAL note (a correct value)
  · FILL unknown   -> LEFT NULL + a MATERIAL note (a value existed but was not recorded)
  · FILL undefined -> LEFT NULL + an IMMATERIAL note (outside the member's population)
  · (no FILL)      -> UNDECLARED: LEFT NULL + a MATERIAL note — the engine discloses, never fills.

Absence is only definable relative to a DOMAIN; the juxtaposition (the full-outer align of two columns
from different universes) supplies one locally, so a column's null cells take meaning from THAT column's
own fill rule. Basis remains a declared universe property (describe/trust, broadcast-safety), but it no
longer drives absence.
"""
import duckdb
import polars as pl
import pytest

from columna_core import ManifoldServer, DuckDBConnector, UNTESTABLE, adjudicate
from columna_core import disclosure_wire as dw
from columna_core.parser import ParseError, parse_manifold


def _lit(v):
    return "'" + v.replace("'", "''") + "'" if isinstance(v, str) else repr(v)


def _server(text, tables):
    con = duckdb.connect()
    for name, (cols, rows) in tables.items():
        values = ", ".join("(" + ", ".join(_lit(v) for v in r) + ")" for r in rows)
        con.execute(f"CREATE TABLE {name} AS SELECT * FROM (VALUES {values}) AS t({', '.join(cols)})")
    return ManifoldServer(parse_manifold(text), DuckDBConnector(con))


def _mk(orders_fill="", level_fill=""):
    """Two universes over the same grain; orders on the events one, level on the spine one. The FILL
    clause on each MEASURE is what now decides absence — basis is declared but inert for absence."""
    of = f" FILL {orders_fill}" if orders_fill else ""
    lf = f" FILL {level_fill}" if level_fill else ""
    return f"""
MANIFOLD b VERSION 1
UNIVERSE ev = store * day BASIS events
UNIVERSE sp = store * day BASIS spine
LEVEL store = store_id BASE
LEVEL day   = day      BASE
MEASURE orders ON ev FROM tx  AS count(*){of}
MEASURE level  ON sp FROM inv AS sum(lvl){lf}
"""


# tx has (s1,d1); inv has (s1,d2) — so the juxtaposed align has a null in each column at the other cell.
_TABLES = {"tx":  (["store_id", "day"], [("s1", "d1")]),
           "inv": (["store_id", "day", "lvl"], [("s1", "d2", 5.0)])}


def _frame(text):
    return _server(text, _TABLES).frame("store", "day").column("orders", "orders").column("level", "level").run()


def _cell(data, day, colname):
    return data.filter((pl.col("store") == "s1") & (pl.col("day") == day))[colname][0]


def _caveats(fr, name):
    col = next(c for c in fr.columns if c.name == name)
    return col.disclosure.caveats


def test_declared_zero_fills_with_an_immaterial_note():
    fr = _frame(_mk(orders_fill="zero", level_fill="zero"))
    # the absent (s1,d2) orders cell is rendered as 0 per the DECLARED rule (not basis)
    assert _cell(fr.data, "d2", "orders") == 0
    note = [c for c in _caveats(fr, "orders") if c.category == "declared_fill"]
    assert note and "existed and was nil" in note[0].detail
    # a declared zero is a correct value — immaterial, so the frame SERVES (both columns declared zero)
    w = dw.wire_frame(fr)
    zf = next(d for col in w["columns"] for d in col["disclosures"] if d["category"] == "declared_fill")
    assert zf["materiality"] == "immaterial"
    assert w["outcome"] == "serve"


def test_declared_unknown_is_left_null_and_discloses_materially():
    fr = _frame(_mk(orders_fill="zero", level_fill="unknown"))
    # the absent (s1,d1) level cell is LEFT NULL — a value existed but was not recorded
    assert _cell(fr.data, "d1", "level") is None
    note = [c for c in _caveats(fr, "level") if c.category == "unknown_absence"]
    assert note and "not filled" in note[0].detail
    w = dw.wire_frame(fr)
    ua = next(d for col in w["columns"] for d in col["disclosures"] if d["category"] == "unknown_absence")
    assert ua["materiality"] == "material" and w["outcome"] == "disclose"


def test_undeclared_discloses_and_does_not_fill_even_on_events_basis():
    # THE D4 FIX: orders is over an events universe but declares NO fill rule. It must NOT silently
    # zero-fill (the retired basis default) — it discloses the absence and leaves it null.
    fr = _frame(_mk(orders_fill="", level_fill="zero"))
    assert _cell(fr.data, "d2", "orders") is None          # left null, NOT 0
    note = [c for c in _caveats(fr, "orders") if c.category == "undeclared_absence"]
    assert note and "no declared fill rule" in note[0].detail
    w = dw.wire_frame(fr)
    ud = next(d for col in w["columns"] for d in col["disclosures"] if d["category"] == "undeclared_absence")
    assert ud["materiality"] == "material" and w["outcome"] == "disclose"


def test_declared_undefined_is_out_of_population_and_immaterial():
    fr = _frame(_mk(orders_fill="zero", level_fill="undefined"))
    assert _cell(fr.data, "d1", "level") is None           # outside the population — a restriction, left null
    note = [c for c in _caveats(fr, "level") if c.category == "out_of_population"]
    assert note and "outside this measure's population" in note[0].detail
    w = dw.wire_frame(fr)
    op = next(d for col in w["columns"] for d in col["disclosures"] if d["category"] == "out_of_population")
    assert op["materiality"] == "immaterial" and w["outcome"] == "serve"


def test_basis_is_inert_for_absence_events_and_spine_behave_alike_when_undeclared():
    # basis no longer drives: an undeclared measure discloses the same way whether its universe is
    # events or spine. (Contrast the retired law, where events zero-filled and spine gapped.)
    fr = _frame(_mk(orders_fill="", level_fill=""))
    for name, day in (("orders", "d2"), ("level", "d1")):
        assert _cell(fr.data, day, name) is None
        assert any(c.category == "undeclared_absence" for c in _caveats(fr, name))


def test_single_column_frame_has_no_absence_edit():
    # no juxtaposition -> no local domain -> no null cells -> no fill/disclosure edit.
    fr = _server(_mk(orders_fill="zero"), _TABLES).frame("store", "day").column("orders", "orders").run()
    ocol = next(c for c in fr.columns if c.name == "orders")
    assert not any(c.category in ("declared_fill", "undeclared_absence") for c in ocol.disclosure.caveats)


def test_fill_clause_parses_onto_the_measure_and_is_optional():
    m = parse_manifold(_mk(orders_fill="zero", level_fill="unknown"))
    assert m.measures["orders"].fill_rule == "zero"
    assert m.measures["level"].fill_rule == "unknown"
    m2 = parse_manifold(_mk())  # no FILL -> undeclared (a legitimate state, not an error)
    assert m2.measures["orders"].fill_rule is None


def test_a_bad_fill_rule_is_a_parse_error():
    with pytest.raises(ParseError, match="bad FILL"):
        parse_manifold(_mk(orders_fill="nil"))   # not zero|unknown|undefined


def test_basis_adjudication_still_mints_untestable_per_type():
    # basis stays a declared universe property (describe/trust) even though it no longer drives absence.
    srv = _server(_mk(), _TABLES)
    report = adjudicate(srv)
    assert report["_basis"] == {"ev": UNTESTABLE, "sp": UNTESTABLE}
    assert srv.m.universes["ev"].basis_license.verdict == UNTESTABLE
    assert "events basis asserted" in srv.m.universes["ev"].basis_license.basis
