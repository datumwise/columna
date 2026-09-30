"""Route 2 validated: normalize ANY carrier to register state, then let the LIBRARY'S OWN
estimator answer.  No second estimator implementation.  Feasibility evidence for item K."""
import random, sys
sys.path.insert(0, "/data/repos/978ea3c9feee4ad79341d42517782efd/columna/specs/evidence/b4a_i")
from q_harness import build, items, union_all, N, registers, mode_of, est_A, LGK
from datasketches import hll_sketch, hll_union, tgt_hll_type as T
K = 1 << LGK
_TEMPLATE = build(items(9999), full=True).serialize_updatable()   # any dense image of this lg_k

def to_register_carrier(s):
    """Provider-internal: hand the library back a carrier holding exactly this register state."""
    img = bytearray(_TEMPLATE)
    img[40:40 + K] = bytes(registers(s))
    return hll_sketch.deserialize(bytes(img))

def finalize(s):
    """The candidate representation-independent finalizer: normalize, force history out,
    then the LIBRARY estimates.  Nothing of DataSketches' estimator is reimplemented."""
    c = to_register_carrier(s)
    u = hll_union(c.lg_config_k); u.update(c); u.update(c)
    return u.get_result(T.HLL_8).get_estimate()

print("A — is the constructed carrier's register state exactly the input's?")
bad = [n for n in (0,1,5,50,193,384,385,1000,9000,50000)
       if registers(to_register_carrier(build(items(n)))) != registers(build(items(n)))]
print(f"    register state preserved for every size tested: {not bad}  {bad if bad else ''}")

print("\nB — does finalize() agree across EVERY representation of one governed state?")
print(f"    {'n':>6} {'sparse':>14} {'dense':>14} {'staged union':>14} {'HLL_4 carrier':>14} {'all agree':>10}")
allok = True
for n in (1, 5, 50, 193, 300, 384, 385, 500, 1000, 20000, 200000):
    base = items(n)
    a = build(base)                                   # library default (sparse when small)
    b = build(base, full=True)                        # dense from the first update
    c = union_all([build(base[i::3]) for i in range(3)])   # staged
    d = build(base, tgt=T.HLL_4)                      # a different encoding
    vals = [finalize(x) for x in (a, b, c, d)]
    ok = len(set(vals)) == 1
    allok &= ok
    print(f"    {n:>6} {vals[0]:>14.6f} {vals[1]:>14.6f} {vals[2]:>14.6f} {vals[3]:>14.6f} {str(ok):>10}")
print(f"    -> representation-independent across sparse/dense/staged/encoding: {allok}")

print("\nC — the forcing step is REQUIRED (the template's history must not be inherited)")
for n in (5, 50, 1000):
    c = to_register_carrier(build(items(n)))
    print(f"    n={n:<6} unforced get_estimate() = {c.get_estimate():>12.6f}   "
          f"forced = {finalize(build(items(n))):>12.6f}   "
          f"(template was built from 9999 values)")

print("\nD — and it is the same number a natively dense carrier gives")
bad = [n for n in (1,5,50,193,384,385,1000,20000) if finalize(build(items(n))) != est_A(build(items(n), full=True))]
print(f"    finalize(any carrier) == library register estimate of a native dense build: {not bad} {bad if bad else ''}")

print("\nE — storage is untouched: what the provider RETAINS is still sparse")
for n in (1, 4, 50, 400):
    print(f"    cell of {n:>4} values: retained {len(build(items(n)).serialize_compact()):>5} B "
          f"(dense would be {len(build(items(n), full=True).serialize_compact())} B)")
