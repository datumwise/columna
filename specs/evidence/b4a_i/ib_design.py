"""(i-b') design probe: the cheapest CORRECT normalization route."""
import sys, time, random
sys.path.insert(0, "/data/repos/978ea3c9feee4ad79341d42517782efd/columna/specs/evidence/b4a_i")
from q_harness import build, items, union_all, registers, mode_of, summary, est_A, LGK
from datasketches import hll_sketch, hll_union, tgt_hll_type as T
K = 1 << LGK

def ooo_template(lg):
    """A dense HLL_8 image whose estimator state is already history-free — built entirely
    through the public API by unioning two dense sketches."""
    a = hll_sketch(lg, T.HLL_8, True); b = hll_sketch(lg, T.HLL_8, True)
    for i in range(3 << lg): a.update(f"a{i}")
    for i in range(3 << lg): b.update(f"b{i}")
    u = hll_union(lg); u.update(a); u.update(b)
    return u.get_result(T.HLL_8).serialize_updatable()

def hip_template(lg):
    s = hll_sketch(lg, T.HLL_8, True)
    for i in range(3 << lg): s.update(f"a{i}")
    return s.serialize_updatable()

TO = ooo_template(LGK); TH = hip_template(LGK)
print(f"ooo template OutOfOrder={summary(hll_sketch.deserialize(TO))['OutOfOrder flag']}  "
      f"hip template OutOfOrder={summary(hll_sketch.deserialize(TH))['OutOfOrder flag']}")

def splice(tmpl, regs):
    img = bytearray(tmpl); img[40:40 + K] = bytes(regs)
    return hll_sketch.deserialize(bytes(img))

def route_A(s):   # splice into ooo template, estimate directly -- CHEAPEST
    return splice(TO, registers(s)).get_estimate()
def route_B(s):   # splice into ooo template, then union-force
    c = splice(TO, registers(s)); u = hll_union(LGK); u.update(c); u.update(c)
    return u.get_result(T.HLL_8).get_estimate()
def route_C(s):   # splice into HIP template, then union-force  (probe2's validated route)
    c = splice(TH, registers(s)); u = hll_union(LGK); u.update(c); u.update(c)
    return u.get_result(T.HLL_8).get_estimate()

print("\nis kxq/curMin recomputed on deserialize, or inherited from the template?")
print(f"    {'n':>7} {'route A (no force)':>19} {'route B':>14} {'route C (known good)':>21} {'A==C':>6}")
agree = True
for n in (1, 5, 50, 193, 385, 1000, 20000, 200000):
    s = build(items(n))
    a, b, c = route_A(s), route_B(s), route_C(s)
    agree &= (a == c)
    print(f"    {n:>7} {a:>19.6f} {b:>14.6f} {c:>21.6f} {str(a==c):>6}")
print(f"    -> route A (no forcing union) is correct: {agree}")

print("\nrepresentation independence of the chosen route, incl. HLL_4 and staged")
best = route_A if agree else route_C
ok = True
for n in (1, 5, 50, 193, 300, 385, 1000, 20000, 200000):
    base = items(n)
    reps = [build(base), build(base, full=True), union_all([build(base[i::3]) for i in range(3)]),
            build(base, tgt=T.HLL_4), hll_sketch.deserialize(build(base).serialize_compact())]
    vals = {best(r) for r in reps}
    ok &= len(vals) == 1
print(f"    one answer across 5 representations at every size: {ok}")

print("\nNEGATIVE CONTROL: what happens if the normalization is skipped")
for n in (5, 1000, 20000):
    s = build(items(n))
    print(f"    n={n:<7} library get_estimate()={s.get_estimate():>14.6f}   normalized={best(s):>14.6f}")

print("\nCOST per finalization (item J)")
def bench(fn, carriers, reps=200):
    t = time.perf_counter()
    for _ in range(reps):
        for c in carriers: fn(c)
    return (time.perf_counter() - t) / (reps * len(carriers)) * 1e6
for label, n in (("sparse cell (n=50)", 50), ("dense cell (n=5000)", 5000)):
    payloads = [build(items(n)).serialize_compact() for _ in range(3)]
    old = bench(lambda p: hll_sketch.deserialize(bytes(p)).get_estimate(), payloads)
    new = bench(lambda p: best(hll_sketch.deserialize(bytes(p))), payloads)
    newB = bench(lambda p: route_C(hll_sketch.deserialize(bytes(p))), payloads)
    print(f"    {label:22s} old {old:7.2f} us   new(A) {new:7.2f} us ({new/old:5.1f}x)   "
          f"new(C, union-forced) {newB:7.2f} us ({newB/old:5.1f}x)")
