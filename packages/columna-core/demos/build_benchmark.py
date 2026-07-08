"""
build_benchmark.py — Columna Core against the real benchmark warehouse.

Proves the column-foundation architecture end-to-end:
  - TRANSPORT replaces the join (revenue@region from single-table deliveries),
  - FAN-OUT is inexpressible (revenue@category refused at the planner),
  - the B-anchor blocks per-lineage (level.sum across time SERVED with a critical disclosure; across stores clean),
  - the pre/post-agg boundary holds (aov correct, not avg-of-avgs),
  - distinct reaggregates by sketch,
  - out-of-universe addressing is a distinct refusal.

Run:  python3 build_benchmark.py
"""
import sys, glob, os
import duckdb, polars as pl

from columna_core import (Manifold, Universe, DimensionLevel, FunctionalEdge,
                          MeasureColumn, FamilyMember, BAnchor, DerivedColumn,
                          ADDITIVE, SKETCH, HOLISTIC, PROVEN,
                          DuckDBConnector, ManifoldServer, Refusal, A)
from columna_core.parser import parse_predicate

# The benchmark warehouse ships with the demos (packages/columna-core/demos/warehouse).
# Override with COLUMNA_BENCH_WAREHOUSE to point at another instance directory.
# NOTE: demo-scope path resolution only — no library module is affected.
WAREHOUSE = os.path.abspath(os.environ.get(
    "COLUMNA_BENCH_WAREHOUSE",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "warehouse"),
))  # resolve at read time: a relative env value must not depend on the eventual cwd

_P, _F = 0, 0
def check(name, cond, detail=""):
    global _P, _F
    ok = bool(cond); _P += ok; _F += (not ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  — {detail}" if detail else ""))

def load():
    con = duckdb.connect()
    for f in glob.glob(f"{WAREHOUSE}/*.parquet"):
        con.execute(f"CREATE TABLE {os.path.basename(f)[:-8]} AS SELECT * FROM read_parquet('{f}')")
    return con

def build_manifold():
    universes = {
        "transactions": Universe("transactions", frozenset({"customer","store","product","day"})),
        "store_days":   Universe("store_days", frozenset({"store","day"}),
                                 predicate=parse_predicate("day >= stores.opened_date")),
    }
    levels = {
        "customer": DimensionLevel("customer","customer_id",is_base=True),
        "store":    DimensionLevel("store","store_id",is_base=True),
        "product":  DimensionLevel("product","product_id",is_base=True),
        "day":      DimensionLevel("day","day",is_base=True),
        "region":   DimensionLevel("region","region"),
        "cal.week": DimensionLevel("cal.week","week"),
        "cal.month":DimensionLevel("cal.month","month"),
        "cal.quarter":DimensionLevel("cal.quarter","quarter"),
        "cal.year": DimensionLevel("cal.year","year"),
        "category": DimensionLevel("category","category_id"),
    }
    edges = [
        FunctionalEdge("store","region","store_geo","stores","store_id","region"),
        FunctionalEdge("day","cal.week","calendar","calendar","day","week"),
        FunctionalEdge("day","cal.month","calendar","calendar","day","month"),
        FunctionalEdge("day","cal.quarter","calendar","calendar","day","quarter"),
        FunctionalEdge("day","cal.year","calendar","calendar","day","year"),
    ]
    measures = {
        "revenue": MeasureColumn("revenue","transactions","transactions","amount",
                       logical_type="Float64",
                       family={"sum": FamilyMember("sum", BAnchor())}),
        "orders":  MeasureColumn("orders","transactions","transactions","1",
                       logical_type="Int64",
                       family={"count": FamilyMember("count", BAnchor())}),
        "visitors":MeasureColumn("visitors","transactions","transactions","customer_id",
                       logical_type="String",
                       family={"distinct": FamilyMember("distinct", BAnchor())},
                       distinct_col="customer_id"),
        # semi-additive stock. sum: blocked over calendar (non-reconciling). last: ORDERED monoid
        # over day. pre_expr is the RAW column 'level' (VARCHAR in the source); logical_type Float64
        # is the promise the CONNECTOR honors with a TRY_CAST at delivery — the author writes no cast.
        "level":   MeasureColumn("level","store_days","eom_inventory","level",
                       logical_type="Float64",
                       family={"sum":  FamilyMember("sum",  BAnchor(frozenset({"calendar"}))),
                               "last": FamilyMember("last", BAnchor(), order_by="day")}),
        # holistic measure: median basket amount — non-monoid, recompute-from-base
        "med_amount": MeasureColumn("med_amount","transactions","transactions","amount",
                       logical_type="Float64",
                       family={"median": FamilyMember("median", BAnchor())}),
        # a CATEGORICAL measure — only count/distinct/mode are well-typed over it (never sum/median)
        "region_label": MeasureColumn("region_label","transactions","transactions","customer_region",
                       logical_type="String",
                       family={"mode": FamilyMember("mode", BAnchor())}),
    }
    derived = {"aov": DerivedColumn("aov", "revenue / orders")}
    non_functional = [("product","category","a product belongs to up to 3 categories")]
    return Manifold("benchmark", 1, universes, levels, edges, measures, derived, non_functional)

def run_validations(con, srv):
    global _P, _F
    _P, _F = 0, 0

    # ---------------------------------------------------------------------
    print("\n(1) TRANSPORT replaces the join — revenue@region from single-table deliveries")
    res = srv.frame("region").column("revenue", "revenue.sum").run()
    got = {r["region"]: r["revenue"] for r in res.data.iter_rows(named=True)}
    truth = {r[0]: r[1] for r in con.execute(
        "SELECT s.region, sum(t.amount) FROM transactions t JOIN stores s USING(store_id) "
        "GROUP BY 1").fetchall()}
    check("revenue@region == ground truth (transported store→region, no join pushdown)",
          all(abs(got[k]-truth[k])<1e-3 for k in truth),
          f"{len(got)} regions; e.g. {sorted(got)[0]}={got[sorted(got)[0]]:.0f}")

    print("\n(2) the SAME transport does coordinate rollup — revenue@cal.month (day→month)")
    res = srv.frame("cal.month").column("revenue","revenue.sum").run()
    got = {r["cal.month"]: r["revenue"] for r in res.data.iter_rows(named=True)}
    truth = {r[0]: r[1] for r in con.execute(
        "SELECT c.month, sum(t.amount) FROM transactions t JOIN calendar c USING(day) GROUP BY 1").fetchall()}
    check("revenue@cal.month == ground truth (transported day→month)",
          all(abs(got[k]-truth[k])<1e-3 for k in truth), f"{len(got)} months")

    # ---------------------------------------------------------------------
    print("\n(3) ★ FLAGSHIP ★ fan-out is INEXPRESSIBLE — revenue@category refused, revenue@region works")
    res = srv.frame("category").column("revenue","revenue.sum").run()
    ref = res.columns[0].refusal
    check("revenue@category is REFUSED (non-functional M:N transport)",
          ref is not None and ref.reason == "non_functional_transport")
    # what text-to-SQL would have returned (the silent 3× inflation):
    naive = con.execute(
        "SELECT sum(t.amount) FROM transactions t JOIN product_categories pc USING(product_id)").fetchone()[0]
    real = con.execute("SELECT sum(amount) FROM transactions").fetchone()[0]
    check("(for contrast) the naive join silently inflates revenue", naive > 1.3*real,
          f"naive=${naive/1e6:.1f}M vs real=${real/1e6:.1f}M ({naive/real:.2f}× — a {(naive/real-1)*100:.0f}% silent overcount)")
    print("    refusal:", str(ref))
    print("    EXPLAIN:")
    for line in res.explain().splitlines():
        print("    " + line)

    # ---------------------------------------------------------------------
    print("\n(4) B-anchor blocks per-LINEAGE — level.sum clean over stores, SERVED-with-disclosure over time")
    # allowed: collapse store→region, keep day (store_geo lineage, not blocked)
    res = srv.frame("region","day").column("inv","level.sum").run()
    truth = {(r[0],r[1]): r[2] for r in con.execute(
        "SELECT s.region, e.day, sum(TRY_CAST(e.level AS DOUBLE)) "
        "FROM eom_inventory e JOIN stores s USING(store_id) GROUP BY 1,2").fetchall()}
    got = {(r["region"],r["day"]): r["inv"] for r in res.data.iter_rows(named=True)}
    check("level.sum@(region,day) is CLEAN — additive over the store axis (no crossing)",
          res.data is not None and all(abs(got[k]-truth[k])<1e-3 for k in truth)
          and res.columns[0].disclosure.severity in ("none","info"),
          f"{len(got)} (region,day) cells")
    # crossing: collapse day (calendar lineage, blocked) → SERVED with a critical disclosure (ADR-020)
    res2 = srv.frame("store").column("inv","level.sum").run()
    col = res2.columns[0]
    crossing = [c for c in col.disclosure.criticals if c.category == "b_anchor_crossing"]
    check("level.sum@store is SERVED with a CRITICAL B-anchor crossing disclosure "
          "(summing a stock across days) — inform-and-serve, not refused",
          col.refusal is None and col.frame is not None
          and len(crossing) >= 1 and col.disclosure.severity == "critical",
          crossing[0].render() if crossing else "")

    # ---------------------------------------------------------------------
    print("\n(5) pre/post-agg boundary — aov = revenue/orders (post-agg), not avg-of-avgs")
    res = srv.frame("cal.month").column("aov","revenue / orders").run()
    got = {r["cal.month"]: r["aov"] for r in res.data.iter_rows(named=True)}
    truth = {r[0]: r[1] for r in con.execute(
        "SELECT c.month, sum(t.amount)/count(*) FROM transactions t JOIN calendar c USING(day) "
        "GROUP BY 1").fetchall()}
    check("aov@cal.month == sum(amount)/count (correct AOV)",
          all(abs(got[k]-truth[k])<1e-2 for k in truth), f"{len(got)} months")

    # ---------------------------------------------------------------------
    print("\n(6) distinct reaggregates by SKETCH — visitors@cal.quarter via HLL merge")
    res = srv.frame("cal.quarter").column("visitors","visitors.distinct").run()
    got = {r["cal.quarter"]: r["visitors"] for r in res.data.iter_rows(named=True)}
    truth = {r[0]: r[1] for r in con.execute(
        "SELECT c.quarter, count(distinct t.customer_id) FROM transactions t JOIN calendar c USING(day) "
        "GROUP BY 1").fetchall()}
    naive = {r[0]: r[1] for r in con.execute(
        "SELECT q, sum(d) FROM (SELECT c.quarter q, t.day, count(distinct t.customer_id) d "
        "FROM transactions t JOIN calendar c USING(day) GROUP BY 1,2) GROUP BY 1").fetchall()}
    check("HLL-merged visitors@quarter ≈ true distinct (within 5%)",
          all(abs(got[k]-truth[k])/truth[k] < 0.05 for k in truth),
          "  ".join(f"{k}:est{got[k]:.0f}/true{truth[k]}" for k in sorted(truth)[:2]))
    check("(naive sum-of-daily-distincts would overcount)",
          all(naive[k] > 1.3*truth[k] for k in truth))

    # ---------------------------------------------------------------------
    print("\n(7) out-of-universe is a DISTINCT refusal — level@product (product ∉ store_days)")
    res = srv.frame("product").column("inv","level.sum").run()
    r = res.columns[0].refusal
    check("level.sum@product is REFUSED as out_of_universe (undefined, not missing)",
          r is not None and r.reason == "out_of_universe", str(r) if r else "")

    print("\n" + "="*80)
    print(f"engine: {srv.stats.deliveries} single-table deliveries, {srv.stats.transports} transports, "
          f"{srv.stats.cache_hits} cache-hits, {srv.fetches} backend fetches (all single-table)")
    print(f"RESULT: {_P} passed, {_F} failed")
    print("="*80)
    return _F

def main():
    print("="*80)
    print("COLUMNA CORE — against the real benchmark warehouse (299,934 transactions)")
    print("  [Manifold: hand-built object]")
    print("="*80)
    con = load()
    srv = ManifoldServer(build_manifold(), DuckDBConnector(con))
    sys.exit(1 if run_validations(con, srv) else 0)

if __name__ == "__main__":
    main()
