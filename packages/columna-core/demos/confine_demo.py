"""
confine_demo.py — universe-predicate confinement, shown by injecting out-of-domain rows.

The real eom_inventory is clean, so confinement is a (correct) no-op on it. Here we
inject pre-opening inventory rows (day < opened_date) — points OUTSIDE the store_days
universe — and show:
  * WITH the universe predicate, the engine confines at the base grain (broadcasting
    stores.opened_date in-engine, no join pushdown) and EXCLUDES them,
  * WITHOUT it, the engine would silently include the bogus stock (the failure),
and that the universe filter is logically prior to a query WHERE.

Run:  python3 confine_demo.py
"""
import sys, copy
from columna_core import (Manifold, Universe, DimensionLevel, FunctionalEdge,
                          MeasureColumn, FamilyMember, BAnchor, SKETCH, ADDITIVE, HOLISTIC,
                          DuckDBConnector, ManifoldServer)
from columna_core.parser import parse_predicate
from build_benchmark import load, build_manifold

_P, _F = 0, 0
def check(name, cond, detail=""):
    global _P, _F
    ok = bool(cond); _P += ok; _F += (not ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  — {detail}" if detail else ""))

def main():
    print("="*80)
    print("COLUMNA CORE — universe-predicate confinement (inject out-of-domain points)")
    print("="*80)
    con = load()

    # pick a store that opened after the first calendar day; inject pre-opening stock
    store, opened = con.execute(
        "SELECT store_id, opened_date FROM stores WHERE opened_date > '2024-01-02' "
        "ORDER BY opened_date LIMIT 1").fetchone()
    region = con.execute("SELECT region FROM stores WHERE store_id = ?", [store]).fetchone()[0]
    bogus_day = "2024-01-01"   # strictly before `opened` -> OUTSIDE store_days
    BOGUS = 1_000_000.0
    con.execute("INSERT INTO eom_inventory VALUES (?, ?, ?)", [store, bogus_day, str(int(BOGUS))])
    print(f"injected: store {store} (opened {opened}, region {region}) gets a bogus "
          f"{BOGUS:.0f} stock on {bogus_day} — a point OUTSIDE store_days")

    # ground truth for the affected (region, bogus_day) cell, both ways
    cell_confined = con.execute(
        "SELECT sum(try_cast(e.level as double)) FROM eom_inventory e JOIN stores s USING(store_id) "
        "WHERE s.region = ? AND e.day = ? AND e.day >= s.opened_date", [region, bogus_day]).fetchone()[0] or 0.0
    cell_unconfined = con.execute(
        "SELECT sum(try_cast(e.level as double)) FROM eom_inventory e JOIN stores s USING(store_id) "
        "WHERE s.region = ? AND e.day = ?", [region, bogus_day]).fetchone()[0] or 0.0
    print(f"ground truth cell (region={region}, day={bogus_day}): "
          f"confined={cell_confined:.0f}  unconfined={cell_unconfined:.0f}  "
          f"(difference = the {BOGUS:.0f} bogus stock)")

    def cell(srv):
        res = srv.frame("region", "day").column("inv", "level.sum").run()
        rows = [r for r in res.data.iter_rows(named=True) if r["region"] == region and r["day"] == bogus_day]
        return (rows[0]["inv"] if rows else 0.0), res

    # (A) WITH the universe predicate — confinement excludes the bogus point
    srv = ManifoldServer(build_manifold(), DuckDBConnector(con))
    got_conf, res = cell(srv)
    check("WITH predicate: engine EXCLUDES the out-of-domain stock (matches confined truth)",
          abs(got_conf - cell_confined) < 1e-3, f"engine={got_conf:.0f}  truth={cell_confined:.0f}")

    print("\n  EXPLAIN (the confinement step is in-engine — broadcast + filter, no join pushdown):")
    for line in res.explain().splitlines():
        if "level" in line.lower() or "confine" in line or "broadcast" in line or "deliver" in line or "transport" in line:
            print("    " + line)

    # (B) WITHOUT the predicate — the silent failure: bogus stock included
    m2 = build_manifold()
    m2.universes["store_days"] = Universe("store_days", frozenset({"store", "day"}), predicate=None)
    srv2 = ManifoldServer(m2, DuckDBConnector(con))
    got_unconf, _ = cell(srv2)
    check("WITHOUT predicate: engine SILENTLY INCLUDES the bogus stock (the failure confinement prevents)",
          abs(got_unconf - cell_unconfined) < 1e-3, f"engine={got_unconf:.0f}  inflated truth={cell_unconfined:.0f}")
    check("confinement removed exactly the injected out-of-domain mass",
          abs((got_unconf - got_conf) - BOGUS) < 1e-3, f"removed {got_unconf-got_conf:.0f}")

    # ── (D) typed-predicate coercion — the contract is GENERAL, not string-date-only ──
    print("\n(D) typed-predicate coercion — numeric / real-Date / AND predicates confine in-engine")
    import polars as pl
    from columna_core.model import Predicate, Comparison, Ref
    eng = srv.engine
    typed = (pl.DataFrame({"k": ["a", "b", "c", "d"], "qty": [5, 15, 25, 35],
                           "d_str": ["2024-01-01", "2024-06-01", "2024-09-01", "2024-12-01"]})
             .with_columns(d=pl.col("d_str").str.to_date()).drop("d_str"))

    # numeric literal: qty >= 10  (Ref.value is the STRING "10" -> must coerce to Int64)
    pnum = Predicate((Comparison(Ref(False, column="qty"), ">=", Ref(True, value="10")),))
    out_num = eng._confine(typed, None, pnum, None)
    check("numeric predicate 'qty >= 10' confines (string literal coerced to Int64; was a ComputeError before)",
          sorted(out_num["qty"].to_list()) == [15, 25, 35], f"kept qty={sorted(out_num['qty'].to_list())}")

    # date-typed literal: d >= 2024-06-01  (real Date column vs string literal -> coerce to Date)
    pdate = Predicate((Comparison(Ref(False, column="d"), ">=", Ref(True, value="2024-06-01")),))
    out_date = eng._confine(typed, None, pdate, None)
    check("date predicate 'd >= 2024-06-01' confines (string literal coerced to Date)",
          out_date.height == 3 and out_date["d"].min().isoformat() == "2024-06-01",
          f"kept {out_date.height} rows from {out_date['d'].min()}")

    # multi-comparison AND: qty >= 10 AND qty < 25  -> the intersection
    pand = Predicate((Comparison(Ref(False, column="qty"), ">=", Ref(True, value="10")),
                      Comparison(Ref(False, column="qty"), "<",  Ref(True, value="25")),))
    out_and = eng._confine(typed, None, pand, None)
    check("AND predicate 'qty >= 10 AND qty < 25' confines to the intersection",
          out_and["qty"].to_list() == [15], f"kept qty={out_and['qty'].to_list()}")

    # ── (E) _attr_anchor hardening — a multi-grain provider table is pinned, or refused ──
    print("\n(E) attribute-anchor resolution — a multi-grain provider table is pinned by the frame, else refused")
    from columna_core.model import Manifold, FunctionalEdge, DimensionLevel
    from columna_core.engine import ColumnEngine
    from columna_core.disclosure import Refusal as _Refusal, CLARIFY, ERROR, AMBIGUOUS
    geo = [FunctionalEdge("store", "region", "store_geo", "geo", "store_id", "region"),
           FunctionalEdge("region", "country", "geo_ctry", "geo", "region", "country")]  # ONE table, TWO grains
    mm = Manifold("geo_test", 1, universes={},
                  levels={"store": DimensionLevel("store", "store_id", True),
                          "region": DimensionLevel("region", "region"),
                          "country": DimensionLevel("country", "country")},
                  edges=geo, measures={})
    geng = ColumnEngine(mm, con)

    def classify(fn):
        """Return the planner-classified no-result a path raises (or None if it returns a value)."""
        try: fn(); return None
        except _Refusal as r: return r.classified()

    sa = eng._attr_anchor("stores")   # benchmark: stores keyed at one grain
    check("single-grain table ('stores') resolves unambiguously to its grain",
          isinstance(sa, tuple) and len(sa) == 2 and isinstance(sa[0], str), f"{sa}")
    check("multi-grain 'geo' pinned by a store-grain frame -> store",
          geng._attr_anchor("geo", available={"store", "day"}) == ("store", "store_id"))
    check("multi-grain 'geo' pinned by a region-grain frame -> region",
          geng._attr_anchor("geo", available={"region"}) == ("region", "region"))
    rb = classify(lambda: geng._attr_anchor("geo", available={"store", "region"}))
    check("multi-grain 'geo', BOTH levels present -> CLARIFY (ambiguous; engine reports, planner classifies)",
          rb is not None and rb.kind == CLARIFY and rb.discriminator == AMBIGUOUS
          and "multiple levels" in rb.detail and len(rb.alternatives) == 2,
          f"{rb.kind}/{rb.discriminator} alts={list(rb.alternatives)}" if rb else "no no-result")
    rn = classify(lambda: geng._attr_anchor("geo"))
    check("multi-grain 'geo', no frame to pin it -> CLARIFY (ambiguous)",
          rn is not None and rn.kind == CLARIFY and rn.discriminator == AMBIGUOUS and "multiple levels" in rn.detail,
          f"{rn.kind}/{rn.discriminator}" if rn else "no no-result")
    re = classify(lambda: geng._attr_anchor("nonexistent"))
    check("attribute table with no providing edge -> ERROR (vocabulary, not an analytical verdict)",
          re is not None and re.kind == ERROR and "no functional edge" in re.detail,
          f"{re.kind}" if re else "no no-result")

    print("\n" + "="*80)
    print(f"RESULT: {_P} passed, {_F} failed")
    print("="*80)
    sys.exit(1 if _F else 0)

if __name__ == "__main__":
    main()
