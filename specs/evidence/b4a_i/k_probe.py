"""Is representation-independent finalization reachable through the PUBLIC DataSketches API?
Feasibility probe for reconciliation item K. No production code, no repo change."""
import math, random, sys, struct
sys.path.insert(0, "/data/repos/978ea3c9feee4ad79341d42517782efd/columna/specs/evidence/b4a_i")
from q_harness import build, items, union_all, N, registers, mode_of, est_A, summary, LGK, HLL8
from datasketches import hll_sketch, hll_union, tgt_hll_type as T

K = 1 << LGK

def linear_counting(regs):
    V = sum(1 for r in regs if r == 0)
    return float("inf") if V == 0 else len(regs) * math.log(len(regs) / V)

print("ROUTE 1 — in the sparse regime, is the library's register estimator the table-free")
print("          linear-counting closed form?  (if yes, a provider can answer for a sparse")
print("          carrier without a second implementation of the bias-corrected estimator)")
print(f"    {'n':>6} {'mode':>5} {'V(zeros)':>9} {'library register est':>21} {'k*ln(k/V)':>14} {'rel diff':>11}")
worst = 0.0
for n in (1, 5, 20, 50, 100, 193, 300, 384, 385, 500, 800, 1024, 1500, 2048, 3000, 4096, 6000):
    s = build(items(n), full=True)          # HLL mode from the start, all n
    e = est_A(s)                             # library register estimator, HIP forced out
    lc = linear_counting(registers(s))
    V = sum(1 for r in registers(s) if r == 0)
    rd = abs(e - lc) / max(e, 1e-9)
    worst = max(worst, rd) if n <= 4096 else worst
    print(f"    {n:>6} {mode_of(s):>5} {V:>9} {e:>21.6f} {lc:>14.6f} {rd:>10.4%}")
print(f"    worst relative difference at n <= 4096 (= k): {worst:.4%}")

print("\nROUTE 2 — can a register vector be handed back to the library as a carrier?")
print("          (construct an HLL_8 image from a template preamble + our register bytes)")
tmpl = build(items(3000), full=True).serialize_updatable()
src  = build(items(120))                     # a SPARSE carrier: coupon mode
regs = registers(src)                        # decoded, validated by V4
img  = bytearray(tmpl)
img[40:40 + K] = bytes(regs)
ok, why = True, ""
try:
    rebuilt = hll_sketch.deserialize(bytes(img))
    same_state = registers(rebuilt) == regs
    ref = build(items(120), full=True)       # same support, natively dense
    print(f"    deserialize accepted the constructed image: True")
    print(f"    reconstructed register state matches: {same_state}")
    print(f"    est via constructed image {est_A(rebuilt):.6f}  vs native dense {est_A(ref):.6f}  "
          f"equal={est_A(rebuilt)==est_A(ref)}")
    print(f"    (preamble fields NOT patched: curMin/numAtCurMin/kxq/hip are the template's)")
except Exception as exc:
    ok, why = False, f"{type(exc).__name__}: {exc}"
    print(f"    REFUSED: {why}")

print("\nROUTE 3 — does the sparse/dense split change the ANSWER the user sees?")
print("          member alpha = 'the estimator is a function of the register vector'")
print(f"    {'n':>6} {'sparse carrier':>15} {'dense carrier':>14} {'agree':>6} {'rounded agree':>14}")
dis, rdis = 0, 0
for n in (1, 3, 8, 20, 50, 100, 193, 250, 300, 384):
    a, b = build(items(n)), build(items(n), full=True)
    ea = linear_counting(registers(a))       # provider answers for a sparse carrier, register law
    eb = est_A(b)
    if ea != eb: dis += 1
    if round(ea) != round(eb): rdis += 1
    print(f"    {n:>6} {ea:>15.6f} {eb:>14.6f} {str(abs(ea-eb)<1e-9):>6} {str(round(ea)==round(eb)):>14}")
print(f"    -> exact disagreements {dis}/10, disagreements after the finalizer's rounding {rdis}/10")

print("\nROUTE 4 — the cost of the simplest alternative: dense retention everywhere")
for n in (1, 4, 50, 400, 5000):
    sp = len(build(items(n)).serialize_compact())
    dn = len(build(items(n), full=True).serialize_compact())
    print(f"    cell of {n:>5} distinct values: sparse {sp:>5} B   dense {dn:>5} B   {dn/sp:>6.0f}x")
