"""
test_relate_triad.py — the RELATE face TRIAD executes (0.12 "the triad completes", Huayin 2026-07-24).

Alongside the shipped `touch` (over-count), 0.12 adds:
  · ASSIGN BY <driver> ORDER MIN|MAX — the value single-counts to each member's top-ranked pair; the
    total reconciles to the grand total; the SHADOW (dropped memberships) is disclosed.
  · ALLOC BY <driver> — the value splits by the normalized driver; the total reconciles to the cent;
    the RECONCILIATION badge is the commutation certificate.
Publish-time adjudication is fail-closed per scheme (a tie at the top, a zero-sum driver, an un-frozen
events driver), and the ANCHOR LAW (G5) refuses a distinct-class measure at ANY face, uniformly.

One M:N bridge (product<->category), a driver spine (category_profile), real duckdb data:
  revenue: p1=100, p2=40, p3=10   (grand total 150; p4 has none)
  bridge:  p1∈{c1,c2}, p2∈{c2}, p3∈{c1,c2,c3}, p4∈{c4}     (7 memberships)
  priority (rank, ORDER MIN=top): c1=1, c2=2, c3=3, c4=4
  alloc_weight (raw): c1=3.0, c2=1.5, c3=2.0, c4=1.0
"""
import duckdb
import polars as pl
import pytest

from columna_core import ManifoldServer, DuckDBConnector
from columna_core.parser import parse_manifold, ParseError
from columna_core.adjudication import adjudicate, FaceContradiction


def _lit(v):
    return "'" + v.replace("'", "''") + "'" if isinstance(v, str) else repr(v)


def _server(faces, cat_attrs="('c1',1,3.0),('c2',2,1.5),('c3',3,2.0),('c4',4,1.0)",
            bridge="('p1','c1'),('p1','c2'),('p2','c2'),('p3','c1'),('p3','c2'),('p3','c3'),('p4','c4')"):
    con = duckdb.connect()
    con.execute("CREATE TABLE transactions AS SELECT * FROM (VALUES "
                "('p1','d1',60.0),('p1','d2',40.0),('p2','d1',40.0),('p3','d1',10.0)) AS t(product_id,day,amount)")
    con.execute(f"CREATE TABLE product_categories AS SELECT * FROM (VALUES {bridge}) AS t(product_id,category_id)")
    con.execute(f"CREATE TABLE category_attributes AS SELECT * FROM (VALUES {cat_attrs}) AS t(category_id,priority,alloc_weight)")
    M = f"""
MANIFOLD shop VERSION 1
UNIVERSE sales = product * day BASIS events
UNIVERSE category_profile = category BASIS spine
LEVEL product = product_id BASE
LEVEL day = day BASE
LEVEL category = category_id BASE
RELATE product <-> category VIA product_categories(product_id, category_id)
    FACES {{
{faces}
    }}
MEASURE revenue ON sales FROM transactions AS sum(amount)
MEASURE buyers ON sales FROM transactions AS distinct(product_id)
MEASURE priority ON category_profile FROM category_attributes VALUE priority FAMILY {{ last ORDER category }}
MEASURE alloc_weight ON category_profile FROM category_attributes VALUE alloc_weight FAMILY {{ last ORDER category }}
"""
    return ManifoldServer(parse_manifold(M), DuckDBConnector(con))


TRIAD = ('        touch   = TOUCH -- "reaches every category"\n'
         '        primary = ASSIGN BY priority ORDER MIN -- "top-priority, single-counted"\n'
         '        split   = ALLOC BY alloc_weight -- "splits by weight"')


def _by(data, col, key, val="revenue"):
    r = data.filter(pl.col(col) == key)
    return r[val][0] if r.height else None


# ---- ASSIGN executes (single-count, the shadow) ----------------------------------------------------
def test_assign_single_counts_to_the_top_rank_and_totals_reconcile():
    data = _server(TRIAD).frame("category.primary").column("revenue", "revenue").run().data
    # ORDER MIN: p1->c1(1), p2->c2(2), p3->c1(1), p4->(no revenue). Single-count, no multiply.
    assert _by(data, "category.primary", "c1") == 110.0    # p1 + p3
    assert _by(data, "category.primary", "c2") == 40.0     # p2 only (p1,p3 went to c1)
    assert _by(data, "category.primary", "c3") == 0.0      # nobody's top
    assert data["revenue"].sum() == 150.0                  # ≡ the grand total (single-count preserves mass)


def test_assign_states_the_shadow_of_dropped_memberships():
    fr = _server(TRIAD).frame("category.primary").column("revenue", "revenue").run()
    shadow = [c for c in fr.disclosure.caveats if c.category == "shadow"]
    assert shadow and shadow[0].shadow == 3        # 7 memberships - 4 top-picks = 3 unrepresented


def test_assign_order_max_flips_the_pick():
    data = _server(TRIAD.replace("ORDER MIN", "ORDER MAX")).frame("category.primary").column("revenue", "revenue").run().data
    # ORDER MAX: p1->c2(2), p3->c3(3). c1 now gets nobody.
    assert _by(data, "category.primary", "c1") == 0.0
    assert _by(data, "category.primary", "c3") == 10.0     # p3's max-priority category
    assert data["revenue"].sum() == 150.0


# ---- ALLOC executes (split, the reconciliation badge) ----------------------------------------------
def test_alloc_splits_by_normalized_weight_and_reconciles_to_the_cent():
    data = _server(TRIAD).frame("category.split").column("revenue", "revenue").run().data
    # p1{c1,c2} w=3,1.5 -> 66.67,33.33 ; p2{c2}=40 ; p3{c1,c2,c3} w=3,1.5,2 -> 4.615,2.308,3.077
    assert abs(_by(data, "category.split", "c1") - 71.2821) < 1e-3
    assert abs(_by(data, "category.split", "c3") - 3.0769) < 1e-3
    assert abs(data["revenue"].sum() - 150.0) < 1e-9       # mass preserved to the cent


def test_alloc_carries_the_reconciliation_badge():
    fr = _server(TRIAD).frame("category.split").column("revenue", "revenue").run()
    recon = [c for c in fr.disclosure.caveats if c.category == "reconciliation"]
    assert recon
    d = dict(recon[0].reconciliation)
    assert d["status"] == "reconciles" and abs(d["delta"]) < 1e-6


# ---- ORDER is mandatory on ASSIGN (no silent default) ----------------------------------------------
def test_assign_without_order_refuses_to_parse():
    with pytest.raises(ParseError, match="ORDER is mandatory"):
        _server('        p = ASSIGN BY priority -- "x"')


def test_alloc_with_order_refuses_to_parse():
    with pytest.raises(ParseError, match="ORDER does not apply to ALLOC"):
        _server('        s = ALLOC BY alloc_weight ORDER MIN -- "x"')


# ---- the three adjudication-failure cases (publish fails closed) -----------------------------------
def test_adjudication_fails_on_a_tie_at_the_top():
    # c1,c2 share priority 1; p1 has both -> no unique top
    with pytest.raises(FaceContradiction, match="tie at the top"):
        adjudicate(_server('        primary = ASSIGN BY priority ORDER MIN -- "x"',
                           cat_attrs="('c1',1,3.0),('c2',1,1.5),('c3',3,2.0),('c4',4,1.0)"))


def test_adjudication_fails_on_a_zero_sum_driver():
    # p1's categories c1,c2 both weight 0 -> undefined split
    with pytest.raises(FaceContradiction, match="sums to zero"):
        adjudicate(_server('        split = ALLOC BY alloc_weight -- "x"',
                           cat_attrs="('c1',1,0.0),('c2',2,0.0),('c3',3,2.0),('c4',4,1.0)"))


def test_adjudication_fails_on_an_unfrozen_events_driver():
    # revenue is an EVENTS measure — an un-frozen driver; the acyclicity object (derived-then-recorded).
    with pytest.raises(FaceContradiction, match="must be a SPINE"):
        adjudicate(_server('        primary = ASSIGN BY revenue ORDER MAX -- "x"'))


def test_valid_triad_publishes_with_the_right_verdicts():
    rep = adjudicate(_server(TRIAD))
    fv = rep["_faces"]
    assert fv["product<->category.touch"] == "verified"        # symbolic, timeless
    assert fv["product<->category.primary"] == "corroborated"  # data-tested (distinctness)
    assert fv["product<->category.split"] == "corroborated"    # data-tested (non-neg, positive sum)


# ---- G5: the ANCHOR LAW — a distinct-class measure refuses at EVERY face, uniformly ---------------
@pytest.mark.parametrize("face", ["touch", "primary", "split"])
def test_distinct_class_measure_refuses_at_every_face(face):
    fr = _server(TRIAD).frame(f"category.{face}").column("buyers", "buyers").run()
    nr = fr.columns[0].refusal
    assert nr is not None and nr.reason == "anchor_spent"
    # speaks the DECLARATION dialect (distinct), NEVER the engine's sketch/HLL representation
    assert "distinct anchor is spent" in nr.detail
    assert "HLL" not in nr.detail and "sketch" not in nr.detail.lower()
