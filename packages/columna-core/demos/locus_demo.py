"""
locus_demo.py — the B-anchor crossing locus refinement.

Crossing DETECTION moved from the engine (execute time) to the planner (compile time), because a
crossing is a pure SHAPE fact — knowable from the b-anchor's blocked lineages and the path/out-edge
lineages, with no data. The served contract is unchanged: a crossing is still SERVED with the same
critical b_anchor_crossing disclosure naming the alternative reducer, never refused.

What the new locus buys: EXPLAIN-WITHOUT-EXECUTION. Because detection is now static, plan() returns
the would-be annotation — the critical crossing AND the spec-only provenance caveats — touching zero
backend data. An agent sees the wrong-answer warning before spending a single scan.
"""
from build_benchmark import build_manifold, load
from columna_core.connector import DuckDBConnector
from columna_core.frameql import ManifoldServer

PASS = FAIL = 0
def check(name, cond, detail=""):
    global PASS, FAIL
    ok = bool(cond); PASS += ok; FAIL += (not ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  — {detail}" if detail else ""))

def crossings(disc):
    return [c for c in disc.caveats if c.category == "b_anchor_crossing"]

srv = ManifoldServer(build_manifold(), DuckDBConnector(load()))

print("=" * 80)
print("B-ANCHOR LOCUS REFINEMENT — crossing detection hoisted to the planner; EXPLAIN dry-runs")
print("=" * 80)

# ── (1) the served contract is UNCHANGED — level.sum@store still served-with-critical ─
print("\n(1) served contract unchanged — level.sum@store is SERVED with the critical crossing")
res = srv.frame("store").column("inv", "level.sum").run()
col = res.columns[0]
cr = crossings(col.disclosure)
check("level.sum@store is SERVED (not refused) with a critical b_anchor_crossing",
      col.refusal is None and col.frame is not None and len(cr) == 1 and col.disclosure.severity == "critical",
      cr[0].detail[:88] if cr else "")
check("the crossing names the reconciling alternative (.last)", cr and ".last" in cr[0].remedy)

# ── (2) DETECTION now lives in the planner — the engine's own disclosure has no crossing ─
print("\n(2) locus moved — the engine no longer detects the crossing; the planner does")
_frame, edisc = srv.engine.resolve("level", "sum", ("store",))
check("engine.resolve('level','sum',@store) returns a disclosure with NO crossing (engine doesn't detect)",
      len(crossings(edisc)) == 0, "the engine serves; it no longer decides the crossing")
check("the planner's served result DOES carry it (detection is the planner's job now)",
      len(cr) == 1, "same critical crossing, now sourced from the shape projection")

# ── (3) EXPLAIN WITHOUT EXECUTION — plan() shows the would-be crossing, zero fetches ─
print("\n(3) EXPLAIN-without-execution — plan() shows the would-be critical crossing, no data touched")
f0 = srv.fetches
plan = srv.frame("store").column("inv", "level.sum").plan()
fetched = srv.fetches - f0
pcr = crossings(plan.columns[0].disclosure)
check("plan() did ZERO backend fetches", fetched == 0, f"backend fetches during plan = {fetched}")
check("plan() surfaces the would-be critical crossing before any execution",
      plan.columns[0].frame is None and len(pcr) == 1 and plan.columns[0].disclosure.severity == "critical")
check("plan PREDICTS what run SERVES (same crossing detail) — contract unchanged either way",
      pcr and cr and pcr[0].detail == cr[0].detail)

# ── (4) plan() also surfaces spec-only PROVENANCE (HLL approximation) with no fetches ─
print("\n(4) plan() carries spec-only provenance too — HLL approximation, still zero fetches")
f1 = srv.fetches
dplan = srv.frame("region").column("v", "visitors.distinct").plan()
approx = [c for c in dplan.columns[0].disclosure.caveats if c.category == "approximation"]
check("visitors.distinct@region plan shows the HLL approximation caveat, zero fetches",
      srv.fetches - f1 == 0 and len(approx) == 1, f"rel_error {approx[0].rel_error:.4f}" if approx else "")

# ── (5) a clean column plans clean; a refusal still refuses statically, all dry ─
print("\n(5) a clean frame plans clean; a structural refusal still refuses — all without data")
f2 = srv.fetches
clean = srv.frame("region").column("rev", "revenue.sum").plan()
oou = srv.frame("product").column("inv", "level.sum").plan()    # level ∉ product universe
check("revenue.sum@region plans CLEAN (no crossing)", len(crossings(clean.columns[0].disclosure)) == 0)
check("level.sum@product is still REFUSED (out_of_universe) at plan time",
      oou.columns[0].refusal is not None and oou.columns[0].refusal.reason == "out_of_universe")
check("all of (5) touched zero backend data", srv.fetches - f2 == 0, f"fetches = {srv.fetches - f2}")

print("\n" + "=" * 80)
print(f"RESULT: {PASS} passed, {FAIL} failed")
print("=" * 80)
