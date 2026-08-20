"""
locus_demo.py — the B-anchor crossing locus refinement.

Crossing DETECTION moved from the engine (execute time) to the planner (compile time), because a
crossing is a pure SHAPE fact — knowable from the b-anchor's blocked lineages and the path/out-edge
lineages, with no data. That is the locus point, and it is unchanged.

What the detection now PRODUCES did change. RULED 2026-08-20 (Huayin, the generated-family law),
superseding ADR-020's inform-and-serve for this case: a reduction travelling a lineage its operator
is declared BLOCKED along is REFUSED (`blocked_reduction` / `unsupported`), not served with a
critical `b_anchor_crossing` caveat. Disclose exists inside the lawful region — it may qualify an
admissible result, it may not legalize an operation the governed law does not possess, and a caveat
pinned to a non-reconciling total is not a warning, it is a delivery mechanism. The caveat category
is TOMBSTONED as a producer (kept wired so archived transcripts still resolve), so `crossings()`
below now reads as a NEGATIVE probe: it must come back empty everywhere.

What the locus buys is unchanged and is the point of section (3): EXPLAIN-WITHOUT-EXECUTION. Because
adjudication is static, plan() returns the would-be annotation — now the would-be REFUSAL, plus the
spec-only provenance caveats — touching zero backend data. An agent learns the ask has no lawful
reading before spending a single scan.
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
    """The TOMBSTONED caveat category (retired as a producer 2026-08-20). Kept here as a negative
    probe: after the generated-family law, nothing may ever emit one again."""
    return [c for c in disc.caveats if c.category == "b_anchor_crossing"]

srv = ManifoldServer(build_manifold(), DuckDBConnector(load()))
srv.publish()

print("=" * 80)
print("B-ANCHOR LOCUS REFINEMENT — crossing detection hoisted to the planner; EXPLAIN dry-runs")
print("=" * 80)

# ── (1) the adjudicated contract — level.sum@store is REFUSED, and nothing is disclosed ─
print("\n(1) the contract — level.sum@store is REFUSED (blocked_reduction); no number, no caveat")
res = srv.frame("store").column("inv", "level.sum").run()
col = res.columns[0]
ref = col.refusal
check("level.sum@store is REFUSED (blocked_reduction/unsupported) — never served under a caveat",
      ref is not None and ref.kind == "refuse" and ref.reason == "blocked_reduction"
      and ref.discriminator == "unsupported"
      and col.frame is None and len(crossings(col.disclosure)) == 0,
      ref.detail[:88] if ref else "")
check("the refusal names the reconciling alternative (.last)",
      ref is not None and any(".last" in a for a in ref.alternatives))

# ── (2) ADJUDICATION lives in the planner — the engine attempts, and never judges ─
print("\n(2) locus moved — the engine never detected the crossing; the planner adjudicates it")
# P0.5a: the planner owns route selection — a direct engine drive asks it for the certified plan
_routes, _split = srv.planner.plan_routes("level", ("store",))
_frame, edisc = srv.engine.resolve("level", "sum", ("store",), routes=_routes, split=_split)
check("engine.resolve('level','sum',@store) returns a disclosure with NO crossing (engine doesn't detect)",
      len(crossings(edisc)) == 0, "the engine attempts; it never judged and still does not")
check("the planner's verdict is where the law lands — and it REFUSES (adjudication is the planner's job)",
      ref is not None and ref.reason == "blocked_reduction",
      "same shape fact, sourced from the shape projection; the verdict is refuse, not a caveat")

# ── (3) EXPLAIN WITHOUT EXECUTION — plan() shows the would-be refusal, zero fetches ─
print("\n(3) EXPLAIN-without-execution — plan() shows the would-be REFUSAL, no data touched")
f0 = srv.fetches
plan = srv.frame("store").column("inv", "level.sum").plan()
fetched = srv.fetches - f0
pref = plan.columns[0].refusal
check("plan() did ZERO backend fetches", fetched == 0, f"backend fetches during plan = {fetched}")
check("plan() surfaces the would-be REFUSAL before any execution",
      plan.columns[0].frame is None and pref is not None
      and pref.reason == "blocked_reduction" and pref.kind == "refuse")
check("plan PREDICTS what run REFUSES (same refusal detail) — the verdict is static, not empirical",
      pref is not None and ref is not None and pref.detail == ref.detail)

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
check("revenue.sum@region plans CLEAN (no crossing)", len(crossings(clean.columns[0].disclosure)) == 0
      and clean.columns[0].refusal is None)
check("level.sum@product is still REFUSED (out_of_universe) at plan time",
      oou.columns[0].refusal is not None and oou.columns[0].refusal.reason == "out_of_universe")
check("all of (5) touched zero backend data", srv.fetches - f2 == 0, f"fetches = {srv.fetches - f2}")

print("\n" + "=" * 80)
print(f"RESULT: {PASS} passed, {FAIL} failed")
print("=" * 80)
