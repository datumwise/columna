"""
universe_check_demo.py — the universe-support consistency check.

A universe is ONE population. If you reduce every measure bound to a universe down to
that universe and they DON'T reconcile to the same support (the same set of base points),
then some of those measures don't actually belong to the same universe. This turns a
modelling mistake — "I declared two measures as sharing a population when they don't" —
into a decidable, structural check.

  POSITIVE: the benchmark Manifold is consistent — the transactions-universe measures all
            reduce to the same support.
  NEGATIVE: a measure mis-declared onto store_days (but sourced from a different table) is
            FLAGGED, because its support doesn't reconcile with the real store_days measure.

Run:  python3 universe_check_demo.py
"""
import sys
from columna_core import (ManifoldServer, DuckDBConnector,
                          MeasureColumn, FamilyMember, BAnchor)
from build_benchmark import load, build_manifold

_P, _F = 0, 0
def check(name, cond, detail=""):
    global _P, _F
    ok = bool(cond); _P += ok; _F += (not ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  — {detail}" if detail else ""))

def main():
    print("="*80)
    print("COLUMNA CORE — universe-support consistency (reduce-to-universe, compare supports)")
    print("="*80)
    con = load()

    # ── POSITIVE: the benchmark is consistent ──
    print("\n(1) the benchmark Manifold — measures on a universe must share support")
    srv = ManifoldServer(build_manifold(), DuckDBConnector(con))
    findings = srv.engine.validate_universe_support()
    check("benchmark is universe-consistent (transactions' measures reconcile to one support)",
          not findings, "no findings")
    for f in findings:
        print("      unexpected:", f)

    # ── NEGATIVE: mis-declare a measure onto store_days from a SPARSE source ──
    print("\n(2) inject a mis-declared measure: 'sparse_lvl' claims store_days but is sourced")
    print("    from a table covering only ~half the store-days — a different population")
    con.execute("CREATE TABLE sparse_inv AS "
                "SELECT * FROM eom_inventory USING SAMPLE 50 PERCENT (bernoulli)")
    n_sparse = con.execute("SELECT count(*) FROM sparse_inv").fetchone()[0]
    n_full = con.execute("SELECT count(*) FROM eom_inventory").fetchone()[0]
    print(f"    (sparse_inv has {n_sparse} of {n_full} store-day rows)")
    m2 = build_manifold()
    m2.measures["sparse_lvl"] = MeasureColumn(
        "sparse_lvl", "store_days", "sparse_inv", "TRY_CAST(level AS DOUBLE)",
        family={"sum": FamilyMember("sum", BAnchor(frozenset({"calendar"})))})
    srv2 = ManifoldServer(m2, DuckDBConnector(con))
    findings2 = srv2.engine.validate_universe_support()
    check("mis-declared measure is FLAGGED — supports on store_days don't reconcile",
          len(findings2) > 0, f"{len(findings2)} finding(s)")
    for f in findings2:
        print("      →", f)
    check("the flag names a base-point support mismatch (different populations)",
          any("base points" in f for f in findings2))

    print("\n" + "="*80)
    print(f"RESULT: {_P} passed, {_F} failed")
    print("="*80)
    sys.exit(1 if _F else 0)

if __name__ == "__main__":
    main()
