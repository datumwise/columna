"""
operator_umbrella_demo.py — the operator registry is ONE umbrella (reducer / scan / map), and
it is the planner's contract with the engine: the planner reads names+kinds+signatures to
TYPECHECK and ROUTE, the engine (and, for maps, the planner's point-wise evaluator) holds the
mechanics.

  (A) the registry holds all three KINDS, each with a signature
  (B) the planner ROUTES by kind in one frame: reducer -> atom; map -> inline; scan -> engine
  (C) a SCAN executes for real (cumsum / lag / pct_change), order derived from the anchor
  (D) order derivation: no temporal axis -> a clarification naming by=
  (E) a scan over a B-anchor-blocked reduction INHERITS the critical disclosure (inform-and-serve)
  (F) a windowed scan (rolling_*) is recognized by the planner but is Pro -> clarified, not crashed
  (G) only REDUCERS found families: a measure declaring a scan as a family member is rejected at publish

Run:  python3 operator_umbrella_demo.py
"""
import sys
from collections import Counter
from columna_core import (ManifoldServer, DuckDBConnector, Manifold, Universe,
                          DimensionLevel, FunctionalEdge, MeasureColumn, FamilyMember, BAnchor)
from columna_core.operators import REGISTRY, REDUCER, SCAN, MAP
from columna_core.parser import check_wellformed
from build_benchmark import load, build_manifold

_P = _F = 0
def check(name, cond, detail=""):
    global _P, _F
    ok = bool(cond); _P += ok; _F += (not ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  — {detail}" if detail else ""))

def main():
    print("=" * 80)
    print("COLUMNA CORE — the operator umbrella (reducer / scan / map) as the planner's contract")
    print("=" * 80)
    con = load()
    srv = ManifoldServer(build_manifold(), DuckDBConnector(con))

    # ── (A) one registry, three kinds, each with a signature ────────────────
    print("\n(A) the registry is one umbrella with three kinds")
    kinds = Counter(op.kind for op in REGISTRY.values())
    check("registry holds reducers, scans, AND maps under one roof",
          kinds[REDUCER] >= 9 and kinds[SCAN] >= 6 and kinds[MAP] >= 4,
          f"{kinds[REDUCER]} reducers, {kinds[SCAN]} scans, {kinds[MAP]} maps")
    view = srv.planner.m
    check("the planner's shape-view carries each operator's KIND (so it can route) but no mechanics",
          all(hasattr(s, "kind") for s in view.operators.values())
          and not any(hasattr(s, "deliver_sql") or hasattr(s, "combine") for s in view.operators.values()),
          "planner sees names+kinds+signatures; deliver_sql/combine stay engine-side")

    # ── (B)+(C) route by kind in ONE frame; the scan computes for real ──────
    print("\n(B/C) one frame, three kinds routed: revenue.sum (reducer), aov (map), cumsum (scan)")
    res = (srv.frame("cal.month")
              .column("rev", "revenue.sum")
              .column("aov", "aov")
              .column("rev_cum", "cumsum(revenue.sum)")
              .run())
    got = {r["cal.month"]: (r["rev"], r["rev_cum"]) for r in res.data.iter_rows(named=True)}
    truth = {r[0]: (r[1], r[2]) for r in con.execute(
        "WITH m AS (SELECT c.month AS month, sum(t.amount) AS rev "
        "           FROM transactions t JOIN calendar c USING(day) GROUP BY 1) "
        "SELECT month, rev, sum(rev) OVER (ORDER BY month "
        "       ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cum FROM m").fetchall()}
    check("the SCAN cumsum(revenue.sum)@cal.month == DuckDB running SUM() OVER(ORDER BY month)",
          got and all(abs(got[k][1] - truth[k][1]) < 1e-3 for k in truth),
          f"{len(got)} months; final cumulative = {max(v[1] for v in got.values()):.0f}")
    check("the reducer and map columns in the same frame are unaffected (revenue.sum exact)",
          all(abs(got[k][0] - truth[k][0]) < 1e-3 for k in truth))
    print("    EXPLAIN (note each column's routing — atom vs inline map vs engine-walked scan):")
    for line in res.explain().splitlines():
        if any(w in line for w in ("rev", "aov", "cumsum", "scan", "transport")):
            print("      " + line)

    # lag + pct_change, ordered by month
    print("\n(C') lag and pct_change route to the engine too")
    res2 = (srv.frame("cal.month")
               .column("prev", "lag(revenue.sum, n=1)")
               .column("mom", "pct_change(revenue.sum)")
               .run())
    rows = sorted(res2.data.iter_rows(named=True), key=lambda r: r["cal.month"])
    check("lag(revenue.sum,n=1) shifts the series by one month (first month has no predecessor)",
          rows[0]["prev"] is None
          and abs(rows[1]["prev"] - got[rows[0]["cal.month"]][0]) < 1e-3,
          "month[1].prev == month[0].rev")
    check("pct_change(revenue.sum) is month-over-month growth (first is null)",
          rows[0]["mom"] is None and rows[1]["mom"] is not None)

    # ── (D) order derivation: no temporal axis -> clarification ─────────────
    print("\n(D) a scan with no orderable axis in the anchor is a clarification (name by=)")
    res3 = srv.frame("region").column("c", "cumsum(revenue.sum)").run()
    ref = res3.columns[0].refusal
    check("cumsum(revenue.sum)@region has no temporal axis -> refused (clarify), names by=",
          ref is not None and "order axis" in ref.detail and "by=" in ref.detail,
          str(ref)[:96] if ref else "")

    # ── (E) a scan over a blocked reduction INHERITS the critical disclosure ─
    print("\n(E) cumsum over a B-anchor-blocked reduction inherits the served critical disclosure")
    res4 = srv.frame("store", "cal.month").column("inv_cum", "cumsum(level.sum)").run()
    col = res4.columns[0]
    crossing = [c for c in col.disclosure.criticals if c.category == "b_anchor_crossing"]
    check("the scan is SERVED (not refused) and carries the underlying sum's critical crossing",
          col.refusal is None and col.frame is not None and len(crossing) >= 1
          and col.disclosure.severity == "critical",
          "inform-and-serve rides through the scan")

    # ── (F) windowed scan: recognized by the planner, but Pro ───────────────
    print("\n(F) a windowed scan (rolling_sum) is recognized but Pro — clarified, not crashed")
    res5 = srv.frame("cal.month").column("roll", "rolling_sum(revenue.sum)").run()
    ref5 = res5.columns[0].refusal
    check("rolling_sum is in the registry (planner knows it) but in_core=False -> Pro clarification",
          ref5 is not None and "window" in ref5.detail.lower(),
          str(ref5)[:96] if ref5 else "")

    # ── (G) only reducers found families (publish-time) ─────────────────────
    print("\n(G) only REDUCERS found families — a scan as a family member is rejected at publish")
    bad = build_manifold()
    bad.measures["bad"] = MeasureColumn("bad", "transactions", "transactions", "amount",
                                        logical_type="Float64",
                                        family={"cumsum": FamilyMember("cumsum", BAnchor())})
    errs = check_wellformed(bad)
    check("a measure whose family declares a scan ('cumsum') is rejected at publish",
          any("cumsum" in e and "not a reducer" in e for e in errs),
          next((e for e in errs if "cumsum" in e), "")[:96])

    print("\n" + "=" * 80)
    print(f"RESULT: {_P} passed, {_F} failed")
    print("=" * 80)
    return 1 if _F else 0

if __name__ == "__main__":
    sys.exit(main())
