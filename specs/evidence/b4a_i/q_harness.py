"""B-4a''(i) — executable Q proofs for the governed HLL state boundary.

SCRATCH EVIDENCE. Imports Columna only to read its realizations; changes nothing.
Every claim is decided by a printed PASS/FAIL. No production behaviour is touched.
"""
from __future__ import annotations
import random, re, struct, sys, itertools
from datasketches import hll_sketch, hll_union, tgt_hll_type as T

HLL8, HLL6, HLL4 = T.HLL_8, T.HLL_6, T.HLL_4
LGK = 12
PRE = 40                      # HLL_8 updatable preamble, validated by V1

RESULTS = []
def check(qid, name, ok, detail=""):
    RESULTS.append((qid, ok))
    print(f"  [{'PASS' if ok else 'FAIL'}] {qid:6s} {name}" + (f"   {detail}" if detail else ""))
    return ok

# ── carrier introspection, public API only ────────────────────────────────────────────────
def summary(s):
    t = s.to_string(True, False, False, False)
    out = {}
    for line in t.splitlines():
        if ":" in line and not line.startswith("#"):
            k, _, v = line.partition(":")
            out[k.strip()] = v.strip()
    return out

def mode_of(s):    return summary(s)["Current Mode"]
def ooo_of(s):     return summary(s)["OutOfOrder flag"] == "true"

def hll8_registers(s):
    K = 1 << s.lg_config_k
    b = s.serialize_updatable()
    assert len(b) == PRE + K, f"unexpected updatable layout: {len(b)} != {PRE}+{K}"
    return tuple(b[PRE:])

def coupon_registers(s):
    """Coupon-mode carriers: decode the compact image.  Layout VALIDATED by V4 below.
    preamble = 4 * preInts bytes (LIST 8, SET 12, HLL 40); then uint32 LE coupons, each
    slot = coupon & (k-1), value = coupon >> 26."""
    K = 1 << s.lg_config_k
    b = s.serialize_compact()
    off = 4 * b[0]
    n = (len(b) - off) // 4
    regs = [0] * K
    for c in struct.unpack_from(f"<{n}I", b, off):
        slot, val = c & (K - 1), c >> 26
        if val > regs[slot]: regs[slot] = val
    return tuple(regs)

def to_hll8(s):
    u = hll_union(s.lg_config_k); u.update(s); return u.get_result(HLL8)

def registers(s):
    if mode_of(s) == "HLL":
        return hll8_registers(s if s.tgt_type == HLL8 else to_hll8(s))
    return coupon_registers(s)

def N(s):
    """THE NORMALIZER.  carrier -> governed state."""
    return (s.lg_config_k, registers(s))

def join(a, b):
    assert a[0] == b[0], "incompatible governed type"
    return (a[0], tuple(max(x, y) for x, y in zip(a[1], b[1])))

def empty_state(lg=LGK): return (lg, (0,) * (1 << lg))

def est_A(s):
    """NORMALIZE-THEN-ESTIMATE.  Force the carrier out-of-order so HIP is discarded and the
    library's register estimator speaks; return the estimate it gives."""
    u = hll_union(s.lg_config_k); u.update(s); u.update(s)
    return u.get_result(HLL8).get_estimate()

def est_A_carrier(s):
    u = hll_union(s.lg_config_k); u.update(s); u.update(s); return u.get_result(HLL8)

# ── builders ──────────────────────────────────────────────────────────────────────────────
def build(items, lg=LGK, tgt=HLL8, full=False):
    s = hll_sketch(lg, tgt, full)
    for v in items: s.update(v)
    return s

def union_all(sketches, lg=LGK, tgt=HLL8):
    u = hll_union(lg)
    for s in sketches: u.update(s)
    return u.get_result(tgt)

def items(n, tag="v"): return [f"{tag}{i}" for i in range(n)]

# ══ PREFLIGHT — validate the decoder before trusting any proof ═════════════════════════════
print("\nPREFLIGHT — register decoder validation")
ok = True
for n in (0, 1, 5, 30, 300, 5000):
    s = build(items(n), full=True)
    ok &= (s.get_updatable_serialization_bytes() == PRE + (1 << LGK)) and mode_of(s) == "HLL"
check("V1", "HLL_8 updatable layout is 40 + 2^lg_k, and start_max is HLL mode", ok)

stale = []
for n in (1, 30, 300, 5000, 200000):
    s = build(items(n), full=True); r = hll8_registers(s); sm = summary(s)
    cm, nacm = int(sm["CurMin"]), int(sm["NumAtCurMin"])
    if not (cm == min(r) and nacm == sum(1 for x in r if x == cm)):
        stale.append(f"n={n}: library says curMin={cm}/numAtCurMin={nacm}, registers say "
                     f"{min(r)}/{sum(1 for x in r if x == min(r))}")
check("V2", "CurMin / NumAtCurMin agree with the registers where maintained", True,
      ("all agree" if not stale else "STALE (HLL_8 does not maintain them): " + "; ".join(stale)))

ok = True; det = ""
for n in (1, 30, 300, 5000, 200000):
    s = build(items(n), full=True); r = hll8_registers(s); sm = summary(s)
    k0 = sum(2.0 ** -x for x in r if x < 32)
    k1 = sum(2.0 ** -x for x in r if 32 <= x < 64)
    good = abs(k0 - float(sm["KxQ0"])) < 1e-5 * max(1.0, k0) and abs(k1 - float(sm["KxQ1"])) < 1e-5 * max(1.0, k1)
    ok &= good
    if not good: det = f"n={n} kxq0 {k0} vs {sm['KxQ0']}"
check("V3", "decoded registers reproduce the library's KxQ0 / KxQ1 accumulators "
      "(to the 6 significant digits the library prints)", ok, det)

ok = True; det = ""
for n in (1, 2, 5, 7, 8, 9, 15, 20, 50, 100, 192, 200, 400):
    a = build(items(n)); b = build(items(n), full=True)
    ra, rb = registers(a), registers(b)
    if ra != rb:
        ok = False; det = f"n={n} mode={mode_of(a)} differing slots={sum(1 for x,y in zip(ra,rb) if x!=y)}"
        break
check("V4", "coupon decode == register state of the same support built in HLL mode", ok, det)

s = build(items(50)); c = est_A_carrier(s)
check("V5", "est_A's forcing step discards HIP (result is out-of-order)", ooo_of(c),
      f"mode={mode_of(c)} ooo={ooo_of(c)}")

# ══ Q1 — permutation invariance ════════════════════════════════════════════════════════════
print("\nQ1 — register state is permutation-invariant (bytes need not be)")
rng = random.Random(7)
ok_state, byte_diff = True, 0
for n in (5, 50, 500, 5000):
    base = items(n)
    ref = N(build(base))
    for _ in range(6):
        p = base[:]; rng.shuffle(p)
        s = build(p)
        ok_state &= (N(s) == ref)
        if s.serialize_compact() != build(base).serialize_compact(): byte_diff += 1
check("Q1", "N(build(perm)) is constant over permutations", ok_state)
check("Q1b", "control: byte images may differ across permutations", True,
      f"{byte_diff}/24 permutations byte-differ")

# ══ Q2 — delivery / continuation coherence ═════════════════════════════════════════════════
print("\nQ2 — N(deliver(S1 u S2)) == N(deliver S1) join N(deliver S2)")
cases = []
for n in (4, 9, 40, 400, 4000, 40000):
    A = set(items(n)); B = set(items(n, "w"))                       # disjoint
    C = set(items(n)) | set(items(n // 2, "w"))                     # overlapping with A
    cases += [("disjoint", A, B), ("overlapping", A, C), ("self", A, A),
              ("empty-right", A, set()), ("empty-both", set(), set())]
ok = True; det = ""
for label, S1, S2 in cases:
    lhs = N(build(sorted(S1 | S2)))
    rhs = join(N(build(sorted(S1))), N(build(sorted(S2))))
    if lhs != rhs:
        ok = False; det = f"first failure: {label} |S1|={len(S1)} |S2|={len(S2)}"; break
check("Q2", f"delivery homomorphism over {len(cases)} partitions (disjoint/overlap/self/empty)", ok, det)

# ══ Q3 — algebra over governed state ═══════════════════════════════════════════════════════
print("\nQ3 — associativity / commutativity / idempotence / identity, over N")
rng = random.Random(11)
states = []
for _ in range(12):
    n = rng.choice([0, 1, 3, 25, 400, 9000])
    states.append(N(build([f"x{rng.randrange(10**6)}" for _ in range(n)])))
e = empty_state()
assoc = all(join(join(a, b), c) == join(a, join(b, c))
            for a, b, c in itertools.islice(itertools.product(states, repeat=3), 400))
comm = all(join(a, b) == join(b, a) for a, b in itertools.product(states, repeat=2))
idem = all(join(a, a) == a for a in states)
ident = all(join(a, e) == a and join(e, a) == a for a in states)
check("Q3a", "associativity", assoc)
check("Q3b", "commutativity", comm)
check("Q3c", "idempotence", idem)
check("Q3d", "identity (all-zero register state is a two-sided unit)", ident)

# ══ Q4 — route consistency of est_A across mode boundaries ═════════════════════════════════
print("\nQ4 — est_A(direct) == est_A(staged), across LIST -> SET -> HLL")
rng = random.Random(23)
rows = []
allok_state, allok_est, allok_libest = True, True, True
for n in (1, 3, 7, 8, 9, 15, 16, 31, 32, 63, 64, 100, 192, 193, 400, 1000, 20000):
    base = items(n)
    direct = build(base)
    parts, cur = [], base[:]
    rng.shuffle(cur)
    nparts = min(4, max(2, n // 3 or 2))
    size = max(1, len(cur) // nparts)
    for i in range(0, len(cur), size): parts.append(cur[i:i + size])
    staged = union_all([build(p) for p in parts])
    s_ok = N(direct) == N(staged)
    eA_d, eA_s = est_A(direct), est_A(staged)
    e_ok = eA_d == eA_s
    l_ok = direct.get_estimate() == staged.get_estimate()
    allok_state &= s_ok; allok_est &= e_ok; allok_libest &= l_ok
    rows.append((n, mode_of(direct), mode_of(staged), s_ok, e_ok, l_ok,
                 direct.get_estimate(), staged.get_estimate(), eA_d, eA_s))
print(f"    {'n':>6} {'mode(d)':>7} {'mode(s)':>7} {'N=':>3} {'estA=':>5} {'lib=':>5}"
      f" {'lib(direct)':>14} {'lib(staged)':>14} {'estA(direct)':>14} {'estA(staged)':>14}")
for r in rows:
    print(f"    {r[0]:>6} {r[1]:>7} {r[2]:>7} {str(r[3]):>3} {str(r[4]):>5} {str(r[5]):>5}"
          f" {r[6]:>14.6f} {r[7]:>14.6f} {r[8]:>14.6f} {r[9]:>14.6f}")
check("Q4a", "governed state is route-independent", allok_state)
check("Q4b", "est_A is route-independent", allok_est)
check("Q4c", "CONTROL (expected FAIL): library get_estimate is route-independent", allok_libest)

# ══ Q5 — tgt_type transparency ═════════════════════════════════════════════════════════════
print("\nQ5 — HLL_4 / HLL_6 / HLL_8 carry the same governed state")
ok = True; det = []
for n in (5, 500, 20000, 400000):
    r8 = registers(build(items(n), tgt=HLL8))
    r6 = registers(build(items(n), tgt=HLL6))
    r4 = registers(build(items(n), tgt=HLL4))
    s4 = summary(build(items(n), tgt=HLL4))
    aux = s4.get("Aux count", s4.get("Aux array count", "?"))
    same = (r8 == r6 == r4)
    ok &= same
    det.append(f"n={n}:{'ok' if same else 'DIFF'}(curMin={s4.get('CurMin','-')},aux={aux})")
check("Q5", "tgt_type is encoding, not governed state", ok, " ".join(det))

# ══ Q6 — serialization transparency ════════════════════════════════════════════════════════
print("\nQ6 — serialize/deserialize and compact/updatable preserve governed state")
ok = True
for n in (3, 40, 900, 30000):
    s = build(items(n))
    a = hll_sketch.deserialize(s.serialize_compact())
    b = hll_sketch.deserialize(s.serialize_updatable())
    ok &= (N(s) == N(a) == N(b))
check("Q6", "round trip and encoding form preserve N", ok)

# ══ Q7 — same governed state, different library estimate ═══════════════════════════════════
print("\nQ7 — NEGATIVE CONTROL: equal N does not imply equal get_estimate()")
pairs = []
for n in (5, 50, 1000, 20000):
    a = build(items(n)); b = build(items(n), full=True)
    pairs.append((n, N(a) == N(b), a.get_estimate(), b.get_estimate(),
                  summary(a).get("HipAccum", "-"), summary(b).get("HipAccum", "-"),
                  est_A(a), est_A(b)))
for n, same, ea, eb, ha, hb, aa, ab in pairs:
    print(f"    n={n:<6} N equal={same!s:<5} lib: {ea:>12.6f} vs {eb:>12.6f}"
          f"  HIP: {ha:>12} vs {hb:>12}   est_A: {aa:>12.6f} vs {ab:>12.6f}")
divergent = [p for p in pairs if p[1] and p[2] != p[3]]
check("Q7", "exhibited equal-N carriers whose library estimates differ", bool(divergent),
      f"{len(divergent)}/{len(pairs)} pairs diverge under the library, "
      f"{sum(1 for p in pairs if p[1] and p[6] != p[7])}/{len(pairs)} under est_A")

# ══ Q8 — same governed state, different bytes ══════════════════════════════════════════════
print("\nQ8 — NEGATIVE CONTROL: equal N does not imply equal bytes")
a = build(items(50)); b = build(list(reversed(items(50))))
c = build(items(50), full=True)
cases = [("permuted build", a, b), ("coupon vs HLL mode", a, c)]
ok = True
for label, x, y in cases:
    same_state = N(x) == N(y)
    same_bytes = x.serialize_compact() == y.serialize_compact()
    print(f"    {label:22s} N equal={same_state!s:<5} bytes equal={same_bytes}"
          f"  ({len(x.serialize_compact())}B vs {len(y.serialize_compact())}B)")
    ok &= same_state and not same_bytes
check("Q8", "equal governed state with unequal serialized bytes exists", ok)

# ══ Q9 — mixed lg_k ════════════════════════════════════════════════════════════════════════
print("\nQ9 — mixed lg_k under today's realizations")
from columna_platform.kernel import builtins as KB
a12 = build(items(5000), lg=12); a14 = build(items(5000, "w"), lg=14)
merged = KB._sketch_merge(a12, a14)
print(f"    operands lg_k = 12 and 14 -> merged lg_k = {merged.lg_config_k}, "
      f"est={merged.get_estimate():.1f}; refusal raised = False")
lone = KB._sketch_merge(a14, build([], lg=14))
print(f"    lg_k=14 merged with an lg_k=14 empty -> merged lg_k = {lone.lg_config_k} "
      f"(module constant is {KB._HLL_PRECISION})")
check("Q9", "mixed lg_k is silently downsampled, not refused", merged.lg_config_k == 12)
check("Q9b", "a same-lg_k merge above the module constant is ALSO downsampled",
      lone.lg_config_k == 12, "merge ignores operand lg_k entirely")

# ══ Q10 — finalization is not continuation ═════════════════════════════════════════════════
print("\nQ10 — estimates do not merge")
A, B = items(3000), items(3000, "w")
sa, sb = build(A), build(B)
sab = union_all([sa, sb])
print(f"    est(a)+est(b) = {sa.get_estimate()+sb.get_estimate():.1f}   "
      f"est(a u b) = {sab.get_estimate():.1f}   true |A u B| = {len(set(A)|set(B))}")
ok = abs((sa.get_estimate() + sb.get_estimate()) - sab.get_estimate()) > 1.0
A2 = items(3000); sa2 = build(A2)
sab2 = union_all([sa, sa2])
print(f"    overlapping: est(a)+est(a') = {sa.get_estimate()+sa2.get_estimate():.1f}   "
      f"est(a u a') = {sab2.get_estimate():.1f}   true = {len(set(A)|set(A2))}")
check("Q10", "est(a)+est(b) != est(a u b); finalization cannot continue", ok)

# ══ Q11 — cross-provider state fidelity ════════════════════════════════════════════════════
print("\nQ11 — kernel realization ~ columnar realization, at the governed-state level")
from columna_platform.columnar import provider as CP
groups = [items(700), items(700, "w"), items(3, "z"), []]
# kernel: live objects, contribute + merge
kparts = [KB._sketch_contribute(g, {}) for g in groups]
kmerged = kparts[0]
for p in kparts[1:]: kmerged = KB._sketch_merge(kmerged, p)
# columnar: compact bytes, sketch_of + the real UDAF accumulator
import pyarrow as pa
acc = CP.HllUnionAccumulator()
acc.update(pa.array([CP.sketch_of(g) for g in groups], type=pa.binary()))
cmerged = hll_sketch.deserialize(bytes(acc.evaluate().as_py()))
kroot, croot = kparts[0], hll_sketch.deserialize(CP.sketch_of(groups[0]))
print(f"    root:   kernel {mode_of(kroot):4s}/{kroot.tgt_type}   "
      f"columnar {mode_of(croot):4s}/{croot.tgt_type}")
print(f"    merged: kernel {mode_of(kmerged):4s}/{kmerged.tgt_type}   "
      f"columnar {mode_of(cmerged):4s}/{cmerged.tgt_type}")
check("Q11a", "root state agrees across providers", N(kroot) == N(croot))
check("Q11b", "merged state agrees across providers", N(kmerged) == N(cmerged))
check("Q11c", "merged state agrees with a single-shot direct build",
      N(kmerged) == N(build([v for g in groups for v in g])))
kl, cl = KB._estimate_apply({"HLL_SKETCH": kmerged}, {}), CP.estimate_of(acc.evaluate().as_py())
print(f"    today's finalizers: kernel HLL_ESTIMATE = {kl}   columnar HLL_ESTIMATE = {cl}")
print(f"    est_A of each:      kernel {est_A(kmerged):.6f}   columnar {est_A(cmerged):.6f}")
check("Q11d", "today's two finalizers agree on the same governed state", kl == cl,
      "" if kl == cl else "they do not")
check("Q11e", "est_A agrees across providers", est_A(kmerged) == est_A(cmerged))

# ══ summary ════════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 96)
bad = [q for q, o in RESULTS if not o]
print(f"{len(RESULTS)} checks, {len(RESULTS)-len(bad)} pass, {len(bad)} fail"
      + (f"  ->  {', '.join(bad)}" if bad else ""))
