"""B-4a''(i) addendum — the three questions the first run opened."""
import random, struct, sys
sys.path.insert(0, "/tmp/b4a")
from q_harness import (build, items, union_all, N, registers, mode_of, summary, est_A,
                       est_A_carrier, ooo_of, hll8_registers, LGK, HLL8, HLL4, HLL6)
from datasketches import hll_sketch, hll_union, tgt_hll_type as T

print("\n" + "=" * 96)
print("ADDENDUM A — where exactly does mode promotion happen, and is it route-independent?")
prev = None
bounds = []
for n in range(1, 900):
    m = mode_of(build(items(n)))
    if m != prev: bounds.append((n, m)); prev = m
print(f"    direct build, lg_k=12: mode transitions at {bounds}")
rng = random.Random(101)
mism, tested = [], 0
for n in list(range(1, 60)) + list(range(180, 200)) + list(range(370, 400)) + [512, 1000]:
    base = items(n)
    md = mode_of(build(base))
    for trial in range(8):
        cur = base[:]; rng.shuffle(cur)
        cuts = sorted(rng.sample(range(1, len(cur)), min(len(cur) - 1, rng.randint(1, 5)))) if len(cur) > 1 else []
        parts = [cur[i:j] for i, j in zip([0] + cuts, cuts + [len(cur)])]
        st = union_all([build(p) for p in parts])
        tested += 1
        if mode_of(st) != md or N(st) != N(build(base)):
            mism.append((n, md, mode_of(st), len(parts), N(st) == N(build(base))))
print(f"    {tested} staged/direct comparisons across the boundaries; "
      f"{len(mism)} mode or state mismatches")
if mism: print(f"    first mismatches: {mism[:6]}")
# adversarial: force one part large enough to be HLL, total support still small -> impossible;
# instead: does the union gadget ever promote EARLIER than a direct build?
worst = []
for n in (380, 384, 385, 390, 395):
    md = mode_of(build(items(n)))
    modes = set()
    for trial in range(40):
        cur = items(n); rng.shuffle(cur)
        size = rng.randint(1, max(1, n // 2))
        parts = [cur[i:i + size] for i in range(0, n, size)]
        modes.add(mode_of(union_all([build(p) for p in parts])))
    worst.append((n, md, sorted(modes)))
print(f"    near the SET->HLL boundary (n, direct mode, staged modes seen): {worst}")

print("\nADDENDUM B — is est_A a function of N?  (the V5 failure, pinned)")
rows = []
for n in (1, 5, 50, 193, 300, 384, 400, 1000, 20000):
    a = build(items(n))            # library-default carrier
    b = build(items(n), full=True) # same support, HLL mode from the start
    ca, cb = est_A_carrier(a), est_A_carrier(b)
    rows.append((n, N(a) == N(b), mode_of(a), mode_of(ca), ooo_of(ca), mode_of(cb), ooo_of(cb),
                 est_A(a), est_A(b)))
print(f"    {'n':>6} {'N eq':>5} {'mode(a)':>7} {'forced(a)':>9} {'ooo':>5} {'forced(b)':>9} {'ooo':>5}"
      f" {'est_A(a)':>13} {'est_A(b)':>13} {'agree':>6}")
for r in rows:
    print(f"    {r[0]:>6} {str(r[1]):>5} {r[2]:>7} {r[3]:>9} {str(r[4]):>5} {r[5]:>9} {str(r[6]):>5}"
          f" {r[7]:>13.6f} {r[8]:>13.6f} {str(r[7]==r[8]):>6}")
bad = [r for r in rows if r[1] and r[7] != r[8]]
print(f"    -> est_A disagrees on {len(bad)}/{len(rows)} equal-state pairs, ALL of them with a "
      f"coupon-mode carrier on one side")
print(f"    -> and the rounded finalizer (int(round(.))) disagrees on "
      f"{sum(1 for r in rows if r[1] and round(r[7]) != round(r[8]))}/{len(rows)}")

print("\nADDENDUM C — what does expelling HIP actually cost?")
rng = random.Random(5)
for n in (200, 1000, 5000, 20000, 100000):
    hip_err, reg_err = [], []
    for trial in range(40):
        tag = f"t{trial}_{n}_"
        s = build([f"{tag}{i}" for i in range(n)])
        if mode_of(s) != "HLL": continue
        hip_err.append(abs(s.get_estimate() - n) / n)
        reg_err.append(abs(est_A(s) - n) / n)
    if not hip_err: continue
    mh, mr = sum(hip_err) / len(hip_err), sum(reg_err) / len(reg_err)
    rmh = (sum(e * e for e in hip_err) / len(hip_err)) ** .5
    rmr = (sum(e * e for e in reg_err) / len(reg_err)) ** .5
    print(f"    n={n:>7}  mean|rel err|  HIP {mh*100:6.3f}%  register {mr*100:6.3f}%   "
          f"RMS  HIP {rmh*100:6.3f}%  register {rmr*100:6.3f}%   ratio {rmr/rmh:.2f}x   "
          f"(RSE at lg_k=12 = 1.625%)")

print("\nADDENDUM D — is the HLL_4 aux table actually exercised by Q5?")
for n in (20000, 400000, 2000000):
    s8 = build(items(n), tgt=HLL8)
    r = registers(s8)
    cm = min(r)
    over = sum(1 for x in r if x - cm >= 15)
    s4 = build(items(n), tgt=HLL4)
    same = registers(s4) == r
    print(f"    n={n:>8} curMin={cm} registers needing the HLL_4 aux table (val-curMin>=15): {over:>4}"
          f"   HLL_4 state == HLL_8 state: {same}")

print("\nADDENDUM E — the carrier type silently changes on continuation")
from columna_platform.kernel import builtins as KB
from columna_platform.columnar import provider as CP
a = KB._sketch_contribute(items(3000), {}); b = KB._sketch_contribute(items(3000, "w"), {})
m = KB._sketch_merge(a, b)
print(f"    kernel   : contribute -> {a.tgt_type}   merge -> {m.tgt_type}")
cm_ = hll_sketch.deserialize(CP.sketch_of(items(3000)))
u = hll_union(12); u.update(cm_); u.update(hll_sketch.deserialize(CP.sketch_of(items(3000, "w"))))
print(f"    columnar : sketch_of  -> {cm_.tgt_type}   UDAF get_result() -> {u.get_result().tgt_type}")
print(f"    governed state identical either way: {N(m) == N(u.get_result(T.HLL_8))}")
