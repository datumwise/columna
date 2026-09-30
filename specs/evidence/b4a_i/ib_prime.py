"""Can the UNION absorb a sparse carrier directly, if the gadget is first forced into register
form by an analytically-empty register-form carrier?  That removes the per-cell coupon decode."""
import time
from datasketches import hll_sketch, hll_union, tgt_hll_type as T
from columna_platform.kernel.hll_carrier import _history_free_preamble, governed_estimate
LG = 12; K = 1 << LG

def zero_carrier(lg):
    """Register form, non-empty flag, all registers zero: forces the gadget dense, adds nothing."""
    return hll_sketch.deserialize(_history_free_preamble(lg) + bytes(K))

Z = zero_carrier(LG)
def summary(s):
    return {k.strip(): v.strip() for k, v in
            (l.partition(":")[::2] for l in s.to_string(True, False, False, False).splitlines() if ":" in l)}
print(f"zero carrier: mode={summary(Z)['Current Mode']} is_empty={Z.is_empty()} est={Z.get_estimate()}")

def primed(s):
    u = hll_union(s.lg_config_k)
    u.update(zero_carrier(s.lg_config_k))
    u.update(s)
    return u.get_estimate()

def build(items, lg=LG, tgt=T.HLL_8, full=False):
    s = hll_sketch(lg, tgt, full)
    for v in items: s.update(v)
    return s
def items(n, t="v"): return [f"{t}{i}" for i in range(n)]
def staged(base, parts, lg=LG):
    u = hll_union(lg)
    for i in range(parts): u.update(build(base[i::parts], lg))
    return u.get_result(T.HLL_8)

print("\nagreement with the committed normalizer, across representations")
ok = True
for n in (0, 1, 5, 8, 50, 193, 384, 385, 400, 1000, 20000, 200000):
    base = items(n)
    reps = [build(base), build(base, full=True), staged(base, 2), staged(base, 3),
            build(base, tgt=T.HLL_4), build(base, tgt=T.HLL_6)]
    vp = {primed(r) for r in reps}
    vg = {governed_estimate(r) for r in reps}
    good = len(vp) == 1 and vp == vg
    ok &= good
    print(f"    n={n:<7} primed: {len(vp)} distinct {next(iter(vp)):>14.6f}   committed: "
          f"{next(iter(vg)):>14.6f}   agree={good}")
print(f"    -> primed route is representation-independent AND identical to the committed one: {ok}")

print("\ncost")
def t(fn, reps=1500):
    a = time.perf_counter()
    for _ in range(reps): fn()
    return (time.perf_counter()-a)/reps*1e6
for lbl, n in (("n=5", 5), ("n=50", 50), ("n=380", 380), ("n=5000", 5000), ("n=200000", 200000)):
    p = build(items(n)).serialize_compact()
    old = t(lambda: int(round(hll_sketch.deserialize(bytes(p)).get_estimate())))
    cur = t(lambda: governed_estimate(hll_sketch.deserialize(bytes(p))))
    new = t(lambda: primed(hll_sketch.deserialize(bytes(p))))
    newc = t(lambda: (lambda u: (u.update(Z), u.update(hll_sketch.deserialize(bytes(p))), u.get_estimate())[2])(hll_union(LG)))
    print(f"    {lbl:>9}  old {old:6.2f}   committed(decode) {cur:7.2f}   primed {new:6.2f}   "
          f"primed+cached Z {newc:6.2f} us")
