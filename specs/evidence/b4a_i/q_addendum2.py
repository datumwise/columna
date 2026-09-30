import random, struct, sys
sys.path.insert(0, "/tmp/b4a")
from q_harness import build, items, union_all, N, mode_of, est_A, LGK
from datasketches import hll_sketch, tgt_hll_type as T
from columna_platform.kernel import builtins as KB

def coupon_set(s):
    b = s.serialize_compact(); off = 4 * b[0]
    n = (len(b) - off) // 4
    return tuple(sorted(struct.unpack_from(f"<{n}I", b, off)))

print("\nADDENDUM F — is the coupon SET (not its storage order) route-invariant?")
rng = random.Random(3); ok = True; bytediff = 0
for n in (3, 7, 8, 50, 193, 384):
    base = items(n); ref = coupon_set(build(base)); refb = build(base).serialize_compact()
    for _ in range(10):
        cur = base[:]; rng.shuffle(cur)
        d = build(cur)
        cuts = sorted(rng.sample(range(1, n), min(n - 1, 3))) if n > 1 else []
        parts = [cur[i:j] for i, j in zip([0] + cuts, cuts + [n])]
        st = union_all([build(p) for p in parts])
        ok &= (coupon_set(d) == ref and coupon_set(st) == ref)
        if d.serialize_compact() != refb: bytediff += 1
print(f"    coupon set identical across permutations and staged unions: {ok}")
print(f"    ... while the serialized image differed in {bytediff}/60 cases (storage order only)")

print("\nADDENDUM G — today's HLL_ESTIMATE, same governed input, two lawful routes")
for n in (20000, 50000, 200000):
    base = items(n)
    direct = build(base)
    half = n // 2
    staged = union_all([build(base[:half]), build(base[half:])])
    thirds = union_all([build(base[i::3]) for i in range(3)])
    a = KB._estimate_apply({"HLL_SKETCH": direct}, {})
    b = KB._estimate_apply({"HLL_SKETCH": staged}, {})
    c = KB._estimate_apply({"HLL_SKETCH": thirds}, {})
    same_state = N(direct) == N(staged) == N(thirds)
    print(f"    |input|={n:>7}  governed state identical: {same_state}   "
          f"HLL_ESTIMATE: direct={a:>7}  2-way={b:>7}  3-way={c:>7}   "
          f"spread={max(a,b,c)-min(a,b,c):>5} ({100*(max(a,b,c)-min(a,b,c))/n:.2f}% of truth)")
    print(f"{'':>26}est_A (HIP expelled): {round(est_A(direct)):>7} {round(est_A(staged)):>7} "
          f"{round(est_A(thirds)):>7}   spread={max(round(est_A(x)) for x in (direct,staged,thirds))-min(round(est_A(x)) for x in (direct,staged,thirds))}")
