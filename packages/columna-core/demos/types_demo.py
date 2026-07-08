"""
types_demo.py — logical types: the connector bridges logical<->physical, and the PLANNER
typechecks operators against column dtypes at COMPILE time, before the engine is ever asked.

The point: "operator not supported" and "wrong type for this operator" are VOCABULARY errors,
not data errors. They are knowable from the operator registry's signatures plus each column's
declared logical type — no backend, no resolution. So the planner refuses them before issuing
any query to the column engine. Meanwhile a cast that the connector inserts to honor a logical
type is a realization detail, and a cast FAILURE is a coverage fact, not a type error.

Run:  python3 types_demo.py
"""
import sys
from columna_core import (ManifoldServer, DuckDBConnector, MeasureColumn, FamilyMember, BAnchor)
from columna_core.parser import check_wellformed
from build_benchmark import load, build_manifold

_P, _F = 0, 0
def check(name, cond, detail=""):
    global _P, _F
    ok = bool(cond); _P += ok; _F += (not ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  — {detail}" if detail else ""))

def main():
    print("="*80)
    print("COLUMNA CORE — logical types: connector bridge + planner-side typecheck")
    print("="*80)
    con = load()
    cn = DuckDBConnector(con)

    # ── (1) the connector realizes logical->physical (the cast lives here, not in the measure) ──
    print("\n(1) connector maps logical dtype -> physical, supplying casts on THIS backend")
    # this warehouse's loader already cleans types, so create a genuinely VARCHAR-but-numeric
    # column to exercise the bridge (a raw source where the physical type is a dirty string).
    con.execute("CREATE TABLE dirty_t AS SELECT * FROM (VALUES (1,'10.5'),(2,'20'),(3,'oops')) AS t(k, v)")
    amt = cn.realize("transactions", "amount", "Float64")
    dv = cn.realize("dirty_t", "v", "Float64")
    check("amount (physical DOUBLE) realizes as-is for logical Float64", amt == "amount", f"-> {amt}")
    check("v (physical VARCHAR) realizes via TRY_CAST for logical Float64",
          "TRY_CAST" in dv.upper(), f"-> {dv}")
    bad = con.execute(f"SELECT count(*) FROM dirty_t WHERE {dv} IS NULL").fetchone()[0]
    check("a cast FAILURE is a coverage fact, not a type error (uncastable rows are counted, not fatal)",
          bad == 1, f"{bad} uncastable row ('oops') — handled as coverage, not a crash")

    # ── (2) operator-not-supported is refused at the PLANNER, before the engine ──
    print("\n(2) an unknown operator is refused at compile time — the engine is never asked")
    srv = ManifoldServer(build_manifold(), DuckDBConnector(con))
    before = srv.fetches
    res = srv.frame("region").column("x", "revenue.stddev").run()
    ref = res.columns[0].refusal
    check("revenue.stddev refused as operator-not-supported (vocabulary, not data)",
          ref is not None and ref.reason == "unknown" and "not supported" in ref.detail, str(ref) if ref else "")
    check("NO backend fetch happened — refused before the engine", srv.fetches == before,
          f"fetches {before} -> {srv.fetches}")

    # ── (3) a type mismatch is refused at the PLANNER, before the engine ──
    print("\n(3) a type mismatch (arithmetic on a categorical) is refused at compile time")
    m = build_manifold()
    m.measures["cust_region"] = MeasureColumn("cust_region", "transactions", "transactions",
                                              "customer_region", logical_type="Categorical",
                                              family={"mode": FamilyMember("mode")})
    srv2 = ManifoldServer(m, DuckDBConnector(con))
    before = srv2.fetches
    res = srv2.frame("region").column("bad", "revenue / cust_region.mode").run()
    ref = res.columns[0].refusal
    check("revenue / cust_region.mode refused as type_error (mode yields Categorical, '/' needs numeric)",
          ref is not None and ref.reason == "type_error", str(ref) if ref else "")
    check("NO backend fetch happened — type error caught before the engine", srv2.fetches == before,
          f"fetches {before} -> {srv2.fetches}")
    # and a faithful one still flows
    ok = srv2.frame("region").column("top", "cust_region.mode").run()
    check("the categorical measure itself (cust_region.mode) still resolves fine",
          ok.data is not None and ok.data.height > 0)

    # ── (4) publish-time well-formedness: operator/type errors are compile-time, not data ──
    print("\n(4) publish-time well-formedness rejects ill-typed families (before any data)")
    m_sum_cat = build_manifold()
    m_sum_cat.measures["rgn"] = MeasureColumn("rgn", "transactions", "transactions",
                                              "customer_region", logical_type="Categorical",
                                              family={"sum": FamilyMember("sum", BAnchor())})
    errs = check_wellformed(m_sum_cat)
    check("sum on a Categorical measure is rejected at publish",
          any("does not accept logical type 'Categorical'" in e for e in errs),
          next((e for e in errs if "Categorical" in e), ""))

    m_unknown = build_manifold()
    m_unknown.measures["weird"] = MeasureColumn("weird", "transactions", "transactions", "amount",
                                                logical_type="Float64",
                                                family={"stddev": FamilyMember("stddev", BAnchor())})
    errs = check_wellformed(m_unknown)
    check("an unknown operator in a family is rejected at publish",
          any("operator 'stddev' is not in the registry" in e for e in errs),
          next((e for e in errs if "stddev" in e), ""))

    print("\n" + "="*80)
    print(f"RESULT: {_P} passed, {_F} failed")
    print("="*80)
    sys.exit(1 if _F else 0)

if __name__ == "__main__":
    main()
