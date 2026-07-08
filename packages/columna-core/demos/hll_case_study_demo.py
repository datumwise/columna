"""
hll_case_study_demo.py — a custom TYPE (HLLSketch) + three custom OPERATORS, and a publish-time
witness store, added to Columna Core *without touching the planner*.

It proves four things:
  (a) the new type + operators slot into the umbrella via the registry + engine only — the planner
      and projection layers contain no sketch/HLL code at all;
  (b) STORED-not-cached: after publish, distinct@region is answered by MERGING stored base-grain
      witnesses — with zero base scans at query time (the cache only makes a computation cheaper;
      the witness makes the coarse distinct-count possible without rescanning);
  (c) the sketch carries its precision as TYPE IDENTITY — a raw sketch is opaque to arithmetic
      (numeric ops reject it; you must hll_estimate first), and merging mismatched precisions is a
      type error;
  (d) the HLL approximation rides into the DISCLOSURE from the witness's precision.
"""
from pathlib import Path
import duckdb

import columna_core
from build_benchmark import build_manifold, load
from columna_core.connector import DuckDBConnector
from columna_core.frameql import ManifoldServer
from columna_core.operators import get_operator, output_dtype, signature_ok, REDUCER, MAP
from columna_core.types import (is_hll_sketch, hll_precision, hll_sketch_t, dtype_in,
                                NUMERIC, SKETCH, HLLSKETCH)
from columna_core import sketch as sk
from dataclasses import replace

PASS = FAIL = 0
def check(name, cond, detail=""):
    global PASS, FAIL
    ok = bool(cond); PASS += ok; FAIL += (not ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  — {detail}" if detail else ""))

def server():
    return ManifoldServer(build_manifold(), DuckDBConnector(load()))


print("=" * 80)
print("HLL CASE STUDY — a custom type + three operators + a witness store, planner untouched")
print("=" * 80)

# ── (a) extensibility: registry + engine only, ZERO planner changes ──────────
print("\n(a) the type + three operators slot in via registry + engine — planner is untouched")
src = Path(columna_core.__file__).parent  # resolve the shipped package, cwd-independent
planner_refs = sum((p.read_text().lower().count("sketch") + p.read_text().lower().count("hll"))
                   for p in [src / "planner.py", src / "projection.py"])
check("planner.py + projection.py contain ZERO sketch/HLL references", planner_refs == 0,
      "the planner routes by KIND; it never names the type or its operators")

hc, hm, he = get_operator("hll_count"), get_operator("hll_merge"), get_operator("hll_estimate")
check("hll_count is a REDUCER (deliver: any → HLLSketch)", hc.kind == REDUCER,
      f"accepts any, out '{hc.out_rule}'")
check("hll_merge is a REDUCER monoid (combine: HLLSketch → HLLSketch)",
      hm.kind == REDUCER and hm.is_monoid and HLLSKETCH in hm.accepts, "union, out 'same' (precision preserved)")
check("hll_estimate is a MAP (project: HLLSketch → Int64)",
      he.kind == MAP and he.out_rule == "Int64" and HLLSKETCH in he.accepts)
check("HLLSketch(p) is a recognized parametric type", is_hll_sketch(hll_sketch_t(12)) and hll_precision("HLLSketch(12)") == 12)

# ── (b) stored, not cached: witness merge with NO base scan at query time ─────
print("\n(b) STORED-not-cached — distinct@region merges stored witnesses, no base scan at query time")
srv = server()
n = srv.publish()                                  # eager: build + store base-grain sketches once
check("publish() materialized witnesses (one scan per base dim)", n >= 2,
      f"{n} witnesses; keys e.g. {srv.witnesses.materialized()[:3]}")
mat = srv.witnesses.materialized()
check("witness stored at base 'store' AND 'day' (serves either rollup axis)",
      ("visitors", "distinct", "store") in mat and ("visitors", "distinct", "day") in mat)

base_before = srv.stats.deliveries
res = srv.frame("region").column("visitors", "visitors.distinct").run()
est = {r["region"]: r["visitors"] for r in res.data.iter_rows(named=True)}
base_after = srv.stats.deliveries
check("distinct@region did ZERO base scans at query time (served from witnesses)",
      base_after - base_before == 0, f"base deliveries during query = {base_after - base_before}")

con = load()
truth = {r[0]: r[1] for r in con.execute(
    "SELECT s.region, count(DISTINCT t.customer_id) FROM transactions t "
    "JOIN stores s USING(store_id) GROUP BY 1").fetchall()}
worst = max(abs(est[k] - truth[k]) / truth[k] for k in truth)
check("witness-merged distinct@region ≈ exact distinct (within 5%)", worst < 0.05,
      f"max rel err {worst*100:.1f}%; e.g. {sorted(est)[0]}: est {est[sorted(est)[0]]:.0f} / true {truth[sorted(est)[0]]}")

# contrast: a fresh, UN-published server must scan base rows for the same query
fresh = server()
b0 = fresh.stats.deliveries
fresh.frame("region").column("visitors", "visitors.distinct").run()
check("an UN-published server does a base scan for the same query (the witness made the difference)",
      fresh.stats.deliveries - b0 >= 1, f"base deliveries without witness = {fresh.stats.deliveries - b0}")

# ── (c) precision is type identity; a raw sketch is opaque to arithmetic ──────
print("\n(c) precision is TYPE IDENTITY — raw sketch opaque to numeric ops; mismatch is a type error")
check("'+' REJECTS a raw HLLSketch (a sketch is not a number)",
      not signature_ok(get_operator("+"), hll_sketch_t(12)), "must hll_estimate it to Int64 first")
check("hll_estimate ACCEPTS HLLSketch", signature_ok(he, hll_sketch_t(12)))
check("hll_merge preserves precision (HLLSketch(12) → HLLSketch(12))",
      output_dtype(hm, hll_sketch_t(12)) == hll_sketch_t(12))
check("dtype_in: sketch ∈ SKETCH family but ∉ NUMERIC",
      dtype_in(hll_sketch_t(12), SKETCH) and not dtype_in(hll_sketch_t(12), NUMERIC))

s12a = sk.hll_count(range(1000), 12)
s12b = sk.hll_count(range(500, 1500), 12)
s14  = sk.hll_count(range(1000), 14)
ok_same = sk.hll_merge_pair(s12a, 12, s12b, 12) is not None
check("same-precision sketches merge", ok_same, "HLLSketch(12) ⊕ HLLSketch(12) ✓")
try:
    sk.hll_merge_pair(s12a, 12, s14, 14); mismatch_refused = False
except TypeError as e:
    mismatch_refused = True; msg = str(e)
check("mismatched-precision merge is REFUSED as a type error", mismatch_refused,
      "HLLSketch(12) ⊕ HLLSketch(14) → TypeError")

# ── (d) the approximation rides into the disclosure from the witness precision ─
print("\n(d) the HLL error rides into the DISCLOSURE, carried from the witness's precision")
approx = [c for c in res.columns[0].disclosure.caveats if c.category == "approximation"]
check("distinct@region carries an APPROXIMATION caveat", len(approx) == 1,
      f"rel_error {approx[0].rel_error:.4f} ≈ rse(12) {sk.rse(12):.4f}")
check("the disclosed error equals rse(precision=12)", abs(approx[0].rel_error - sk.rse(12)) < 1e-9)
check("the caveat names the sketch type HLLSketch(12)", "HLLSketch(12)" in approx[0].detail)

# raise precision to 14 → tighter error, and the disclosure follows the type
m = build_manifold()
m.measures["visitors"] = replace(m.measures["visitors"], sketch_precision=14)
srv14 = ManifoldServer(m, DuckDBConnector(load()))
srv14.publish()
res14 = srv14.frame("region").column("visitors", "visitors.distinct").run()
ap14 = [c for c in res14.columns[0].disclosure.caveats if c.category == "approximation"][0]
check("at precision 14 the disclosed error is tighter and equals rse(14)",
      abs(ap14.rel_error - sk.rse(14)) < 1e-9 and sk.rse(14) < sk.rse(12),
      f"rse(14) {sk.rse(14):.4f} < rse(12) {sk.rse(12):.4f}; caveat names {'HLLSketch(14)' if 'HLLSketch(14)' in ap14.detail else '?'}")

print("\n" + "=" * 80)
print(f"RESULT: {PASS} passed, {FAIL} failed")
print("=" * 80)
