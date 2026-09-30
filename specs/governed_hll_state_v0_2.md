# Governed HLL state — v0.2, under the Analytical Law Catalogue model

**Status: SPECIFICATION + EVIDENCE. Design only. No production behaviour changes.**
Supersedes `governed_hll_state_v0_1.md`. Evidence: `specs/evidence/b4a_i/`.
Authorized by Huayin, 2026-09-30: *"Control the leak at the law-member boundary."*

---

## 0. What changed from v0.1, and why

v0.1 defined the governed state as two strata, `{EXACT, REGISTER}`, because the DataSketches Python
API cannot evaluate the register estimator on a coupon-mode carrier. **That is withdrawn.** It took a
provider limitation and made it analytical constitution — precisely the realization leak this
architecture exists to prevent. The limitation is also not real: it is reachable through the public
API (§3).

```
WITHDRAWN   governed state = ( lg_k , stratum , payload )
STANDS      governed state = ( lg_k , hash , register vector )
```

Sparse/coupon/register, LIST/SET/HLL, HLL_4/6/8 and compact/updatable are **provider-internal
representation facts**. They are named `SPARSE` where a name is needed; `EXACT` is retired, because
this system has a separate analytical concept of an exact `distinct_set` and the two must not collide.

## 1. The governed state

```
HLLSketch⟨lg_k, hash⟩        governed value type
state                        M : {0 … 2^lg_k − 1} → {0 … 63}
equivalence   c1 ~ c2   iff  lg_k, hash equal  and  N(c1) = N(c2)
N(c)                         the register vector of c, however c is represented
continuation                 pointwise max; associative, commutative, idempotent, unit = all-zero
inverse                      NONE. There is no subtraction and no differencing continuation.
coherence                    deliver(S1 ∪ S2)  ~  deliver(S1) ⊔ deliver(S2)
finalization                 a function of M alone. HIP is not an input.
approximation                RSE = 1.04 / sqrt(2^lg_k), at EVERY cardinality including small.
```

**No exactness guarantee at low cardinality.** This is deliberate and it is what keeps sparse
representation invisible: a member that promised exactness below some bound would bind every future
provider to reproduce that bound regardless of its own internal thresholds. A later member may promise
it, with a *governed* bound. Member 1 does not.

## 2. Realization obligations

> **R2** — finalization does not consult construction history.
> **R3** — a change of internal representation, holding the governed input fixed, does not change the
> governed result.

R1 of v0.1 ("stratum is a function of the support") is **retired**: with stratum below the boundary,
a provider may promote wherever it likes. R3 subsumes what R1 was protecting, at the right altitude.

## 3. Representation-independent finalization is reachable (item K)

Provider-internal recipe, public API only, no second estimator:

```
1. decode the carrier's register vector                (validated decoder, v0.1 §6.2)
2. hand it back to the library as a dense carrier      (per-lg_k template image + our register bytes)
3. force history out                                   (LOAD-BEARING — see below)
4. the LIBRARY'S OWN estimator answers
```

Measured (`run_k_probe.txt`): identical to the last digit across sparse / dense-from-first-update /
staged-union / HLL_4 carriers of one governed input, at n = 1 … 200 000, and equal to a natively dense
build's register estimate. Retention is untouched — a 1-value cell still costs 12 B, not 4136 B.

Step 3 is not optional. The template preamble carries the template's `hipAccum`, and without the
forcing step **every answer becomes the template's cardinality** — 9956.12 for every input tested.
That negative control belongs in the conformance suite.

Two risks to declare rather than hide:
- step 2 couples the provider to the DataSketches binary layout. Confined to the provider, guarded by
  conformance, and the clean long-term fix is an upstream register accessor or promote API.
- the route was rejected of computing the sparse estimate ourselves in closed form: the library's
  register estimator is **not** linear counting (0.0122% apart at n = 1, 1.39% at n = 6000), so that
  would have been a second estimator implementation by the back door, and the §P divergence problem
  with it.

## 4. Where lg_k, hash and seed belong

| | |
|---|---|
| hash + seed | **member constitution.** Not use-selectable. The seed is not readable back off a carrier, so a use-level choice could never be verified, and two uses at different hashes would produce values that can never merge and nothing in the vocabulary would say so. |
| `lg_k` | a genuine analytical parameter — it *is* the error contract — whose **governance location is member-level for member 1**, because it is compatibility-bearing. A use-level `lg_k` creates values that look like one type and cannot merge. It may move to use level in a member that also declares the cross-`lg_k` compatibility relation. |

## 5. Retained from v0.1

Everything else: the three-way identity distinction, the type/value/artifact table, `tgt_type`
transparency including the HLL_4 aux path, the staleness of `curMin`/`numAtCurMin`, the unprovable
assumptions, and defects D1/D2/D3.
