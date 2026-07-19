"""
test_relate_touch.py — the TOUCH face executes (RELATE faces, Phase-1, Huayin 2026-07-19).

`SELECT revenue AT {category.touch}` must EXECUTE: the measure join-multiplies through the RELATE's VIA
bridge to the crossed (category) grain — a product's revenue reaches EVERY category it sits in, so the
frame is DELIBERATELY multi-counted (totals exceed the grand total) and served in DISCLOSE. The bare
`{category}` coordinate stays barred; its clarify now LISTS the declared faces as the menu. Absence at
the crossed grain is a lawful ZERO on events basis (and only events).

One M:N bridge (product<->category), a touch face, real duckdb data:
  revenue: p1=100, p2=40, p3=10   (grand total 150)
  bridge:  c1<-{p1,p3}=110 · c2<-{p1,p2,p3}=150 · c3<-{p3}=10 · c4<-{p4}  (p4 has NO revenue -> 0)
"""
import duckdb
import polars as pl

from columna_core import ManifoldServer, DuckDBConnector
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


MANIFOLD = """
MANIFOLD shop VERSION 1
UNIVERSE sales = product * day BASIS events
LEVEL product  = product_id  BASE
LEVEL day      = day         BASE
LEVEL category = category_id
RELATE product <-> category VIA product_categories(product_id, category_id)
    FACES { touch = TOUCH -- "revenue reaches every category a product sits in; totals exceed the grand total" }
    NOTE "a product belongs to up to 3 categories"
MEASURE revenue ON sales FROM transactions AS sum(amount)
"""

TABLES = {
    "transactions": (["product_id", "day", "amount"],
                     [("p1", "d1", 60.0), ("p1", "d2", 40.0),   # p1 = 100
                      ("p2", "d1", 40.0),                        # p2 = 40
                      ("p3", "d1", 10.0)]),                      # p3 = 10   (p4 absent)
    "product_categories": (["product_id", "category_id"],
                           [("p1", "c1"), ("p1", "c2"),
                            ("p2", "c2"),
                            ("p3", "c1"), ("p3", "c2"), ("p3", "c3"),
                            ("p4", "c4")]),                      # c4 touched only by revenue-less p4
}


def _touch():
    return _server(MANIFOLD, TABLES).frame("category.touch").column("revenue", "revenue").run()


def _by(data, col, key, val="revenue"):
    return data.filter(pl.col(col) == key)[val][0]


def test_touch_grain_is_the_faced_token_named_honestly():
    fr = _touch()
    assert fr.data is not None, "the touch frame did not execute"
    assert "category.touch" in fr.data.columns, "the grain is not the honestly-named faced coordinate"
    assert "category" not in fr.data.columns          # bare category is NOT the grain (naming honesty)


def test_touch_multi_counts_through_the_bridge():
    data = _touch().data
    assert _by(data, "category.touch", "c1") == 110.0   # p1 + p3
    assert _by(data, "category.touch", "c2") == 150.0   # p1 + p2 + p3
    assert _by(data, "category.touch", "c3") == 10.0    # p3
    # the whole point: the touched total exceeds the grand total (deliberate over-count)
    touched_total = data["revenue"].sum()
    assert touched_total == 270.0
    assert touched_total > 150.0                        # grand total is 150; touch inflates by construction


def test_touch_zero_fills_absent_crossed_grain_on_events_basis():
    # c4 is in the bridge but touched only by p4, which has no revenue: on events basis absence is a
    # lawful ZERO (Huayin: events-only), so c4 appears as 0 rather than vanishing.
    data = _touch().data
    assert _by(data, "category.touch", "c4") == 0.0


def test_touch_serves_in_disclose_with_the_overcount_folklore():
    fr = _touch()
    wire = dw.wire_frame(fr)
    assert wire["outcome"] == "disclose", "a deliberate over-count must disclose, not silently serve"
    rcol = next(c for c in fr.columns if c.name == "revenue")
    oc = [cav for cav in rcol.disclosure.caveats if cav.category == "over_count"]
    assert oc, "the over-count disclosure is missing"
    assert "multi-counted by construction" in oc[0].detail
    # the wire code is the additive material one
    codes = {d["code"] for d in dw.wire_frame(fr)["columns"][0]["disclosures"]}
    assert "multi_counted" in codes


def test_bare_coordinate_still_clarifies_with_the_face_menu():
    fr = _server(MANIFOLD, TABLES).frame("category").column("revenue", "revenue").run()
    rcol = next(c for c in fr.columns if c.name == "revenue")
    assert rcol.refusal is not None and rcol.refusal.reason == "non_functional_transport"
    menu = rcol.refusal.alternatives
    assert any(a.startswith("category.touch —") for a in menu), f"the face menu is missing: {menu}"


def test_touch_reports_full_coverage_when_no_orphans():
    # every revenue-bearing product (p1,p2,p3) is in the bridge -> full coverage, no shortfall.
    fr = _touch()
    rcol = next(c for c in fr.columns if c.name == "revenue")
    cov = [c for c in rcol.disclosure.caveats if "coverage" in c.detail and c.severity == "info"]
    assert cov and "no shortfall" in cov[0].detail


def test_touch_reports_shortfall_when_a_product_is_uncategorized():
    # the mirror of the over-count: a product with revenue but in NO category is excluded from every
    # cell, so the touch total falls SHORT of the grand total by that product's value.
    tables = {
        "transactions": (["product_id", "day", "amount"],
                         [("p1", "d1", 100.0), ("p9", "d1", 25.0)]),   # p9 has revenue
        "product_categories": (["product_id", "category_id"],
                               [("p1", "c1")]),                        # p9 is in no category
    }
    fr = _server(MANIFOLD, tables).frame("category.touch").column("revenue", "revenue").run()
    rcol = next(c for c in fr.columns if c.name == "revenue")
    short = [c for c in rcol.disclosure.caveats if "falls short" in c.detail]
    assert short, "the uncovered-value shortfall caveat is missing"
    assert "by 25" in short[0].detail and "1 of 2 product" in short[0].detail
    assert fr.data["revenue"].sum() == 100.0                          # p9's 25 never reaches a cell


def test_adjudication_mints_the_face_license_at_publish():
    # polarity law: a face is closed-by-default (license None on parse); the adjudicator is the SOLE
    # constructor at publish. touch = VERIFIED (membership expansion is exact arithmetic).
    from columna_core import adjudicate, VERIFIED
    srv = _server(MANIFOLD, TABLES)
    assert srv.m.non_functional[0].faces[0].license is None       # closed-by-default on parse
    report = adjudicate(srv)
    face = srv.m.non_functional[0].faces[0]
    assert face.license is not None and face.license.verdict == VERIFIED
    assert report["_faces"]["product<->category.touch"] == VERIFIED


def test_undeclared_face_is_a_query_error_not_a_crash():
    from columna_core.frameql import FrameQLSyntaxError
    try:
        _server(MANIFOLD, TABLES).frame("category.made_up").column("revenue", "revenue").run()
        assert False, "an undeclared face should be a FrameQL syntax error"
    except FrameQLSyntaxError:
        pass
