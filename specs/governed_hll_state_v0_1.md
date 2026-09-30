# Governed HLL state — B-4a″(i) specification

> **SUPERSEDED by `governed_hll_state_v0_2.md`.** Its §1 two-stratum state model is WITHDRAWN: it
> promoted a DataSketches API limitation into analytical constitution. The evidence and every other
> section stand.

**Status: SPECIFICATION + EVIDENCE. No production behaviour changes in this unit.**
Authorized by Huayin, 2026-09-30: *"First determine the governed state. Then make the running system
faithfully realize it. Only then give that law a durable member identity."*

Evidence: `specs/evidence/b4a_i/` (harness + captured run). Runtime: `datasketches` 5.2.0, lg_k = 12.

---

## 0. The boundary

```
physical DataSketches carrier
        ↓ N   (normalization)
governed HLL state
        ↓ ⊔   (continuation)
governed HLL state
        ↓ est (finalization, a different law)
scalar estimate
```

Three identities are kept apart and none of them implies another downward:

```
analytical state identity   ≠   physical object identity   ≠   serialized-byte identity
```

Measured: equal governed state with unequal bytes exists (Q8, Addendum F — 46/60 permutations of one
input produce byte-different images of one state). Equal governed state with unequal library estimate
exists (Q7 — 4/4 pairs). Neither direction of implication survives.

---

## 1. The governed state

For a governed HLL type `HLLSketch⟨lg_k, hash⟩`, the retained state of one cell is a **two-stratum
value**:

```
state  ::=  EXACT    ( coupon set C )          |  REGISTER ( register vector M )
C : a finite set of 32-bit coupons            M : {0 … 2^lg_k − 1} → {0 … 63}
```

with the **demotion homomorphism**

```
reg(EXACT C)     =  ⊔ { register(c) : c ∈ C }      where register(c) = ( c & (2^lg_k − 1) ↦ c >> 26 )
reg(REGISTER M)  =  M
```

`reg` is a join-semilattice homomorphism: `reg(x ⊔ y) = reg(x) ⊔ reg(y)`. The register stratum is a
bounded join-semilattice under pointwise `max` with unit `0`; the exact stratum is a bounded
join-semilattice under set union with unit `∅`; the join of one of each demotes to the register stratum.

**Why two strata and not one.** A single register-only definition was the first proposal. It is rejected
on measurement, not taste: promotion is capacity-triggered inside DataSketches, and the register
estimator is *not reachable* from a coupon-mode carrier through the public API (Addendum B). Forcing
every retained carrier dense would cost 4136 B per cell at lg_k = 12 against 24 B for a 4-value cell —
the storage economics sketches exist to provide. The two-stratum definition keeps them, and is sound
because the stratum turns out to be **a function of the support alone** (§4).

The register stratum remains the **normal form for analytical comparison and proof**: `reg` is total,
cheap (O(2^lg_k)), and cross-stratum. It is NOT the required storage form.

## 2. What is type, what is value, what is neither

| | |
|---|---|
| **type** | `lg_k`; hash function + seed |
| **value** | stratum + payload (coupon set, or register vector) |
| **realization only** | `tgt_type` (HLL_4/6/8) · compact vs updatable encoding · byte image · object identity · serialization preamble/version |
| **estimator artifact — must never enter identity** | `hipAccum` · `oooFlag` · `kxq0`/`kxq1` · `curMin`/`numAtCurMin` |

`tgt_type` is encoding, proved including the HLL_4 auxiliary-exception path (Q5, Addendum D).
`curMin`/`numAtCurMin` are not merely derivable but **observably stale** under HLL_8 (Addendum V2): the
library reports `curMin = 0` where the registers say `3`. A quantity that can be stale is not a
quantity identity may rest on.

**Governance location of `lg_k` and hash/seed is NOT decided here** (ruled open by Huayin, §3 of the
2026-09-30 direction). What this unit reports is only what the *type* requires: both are
compatibility-bearing, both must be equal for `⊔` to be defined, and neither can be defaulted at the
merge site. Whether a use may choose `lg_k` or the Manifold fixes it with the member is a later ruling.

The seed is **not exposed by the Python binding**. `DEFAULT_UPDATE_SEED` is assumed and cannot be read
back off a carrier. Recorded as an unprovable assumption (§6).

## 3. Equivalence

```
c1 ~ c2   iff   lg_k(c1) = lg_k(c2)
          and   hash(c1) = hash(c2)
          and   N(c1) = N(c2)

N(c) = ( lg_k , stratum , canonical payload )
     canonical payload  =  sorted coupon tuple   (EXACT)
                        |  register tuple        (REGISTER)
```

`~` refines the coarser register equivalence `~reg` (`reg(N(c1)) = reg(N(c2))`), which is the relation
used for cross-stratum proof and cross-provider fidelity.

Canonical **identity** is required. Canonical **storage** is not.

## 4. The two realization obligations

A provider claiming to realize this state owes two things that are not implied by "it calls an HLL
library":

> **R1 — stratum is a function of the governed support.** Which stratum a lawful construction lands in
> must depend only on the support and `lg_k`, never on partition, order, or parallelism.

> **R2 — finalization does not consult history.** The estimator must be a function of the governed
> state. `hipAccum` and `oooFlag` are not inputs.

R1 is measured to hold for DataSketches 5.2.0 at lg_k = 12: transitions at 8 (LIST→SET) and 385
(SET→HLL) distinct coupons, and 888 staged-versus-direct comparisons straddling both boundaries found
**zero** mode or state mismatches (Addendum A). It is a *measured property of a realization*, not a
theorem, which is exactly why it is written as an obligation a provider owes rather than an axiom.

R2 is violated by the running system today (§5).

## 5. The defect, stated exactly

`get_estimate()` consumes `hipAccum` when the out-of-order flag is clear. HIP accumulates over the
*update stream*, so it is a function of construction history and not of the governed state. Therefore
today's `HLL_ESTIMATE` is not a function of the family value.

Measured, on one governed input by two lawful routes (Addendum G):

```
|input| = 20 000    governed state identical
   HLL_ESTIMATE  direct = 19 832    two-way = 20 100    three-way = 20 100     spread 268  (1.34%)
   with HIP expelled          20 100          20 100              20 100       spread   0
```

The cost of expelling HIP is, at lg_k = 12, not measurable as a loss: over 40 trials per size the
register estimator's RMS relative error is **0.97×–1.26×** HIP's, against a nominal RSE of 1.625%
(Addendum C). Path-independence is bought for approximately nothing.

## 6. Assumptions that could not be proved from the DataSketches API

1. **Hash seed.** Not readable from a carrier; `DEFAULT_UPDATE_SEED` assumed. Two sketches built under
   different seeds would merge without complaint and mean nothing. Not testable here.
2. **Register decoding** relies on the HLL_8 updatable layout (`4 × preInts` preamble, then one byte per
   register) and the coupon layout (`slot = c & (k−1)`, `value = c >> 26`). Both are validated against
   the library's own accounting — `KxQ0`/`KxQ1` reproduced to the six significant digits it prints (V3),
   and coupon decoding reproduced against HLL-mode builds of the same support (V4) — but they are read
   off the serialization, not from an API contract. `to_string(detail=True)` would be the contract-level
   route and is **unusable**: the binding truncates the string at the first NUL byte, so any register or
   coupon of value 0 ends the output.
3. **R1 is measured, not guaranteed.** A future library version may move a promotion threshold.
4. **`reg` of a coupon-mode carrier is not reachable through the library.** There is no promotion API;
   unioning with an empty full-size sketch does not force it. This is why the estimator is specified per
   stratum rather than on registers alone.

## 7. What this specification does not decide

- governance location of `lg_k` and hash/seed;
- the `HLL_ESTIMATE` law family beyond the single member boundary above;
- mixed-`lg_k` behaviour beyond proving it cannot remain an invisible merge (Q9);
- any law-family/member machinery, any naming, any surface syntax.

## 8. Recorded defects (not separately fixed)

| | |
|---|---|
| D1 | `_sketch_merge` unions at the module constant `_HLL_PRECISION`, ignoring operand `lg_k`. lg_k 12 ⊔ lg_k 14 silently yields lg_k 12; lg_k 14 ⊔ lg_k 14 *also* yields 12 (Q9, Q9b). |
| D2 | `_sketch_contribute` reads `precision` from params; `_sketch_merge` and `_sketch_identity` cannot. |
| D3 | Both providers' continuation calls `hll_union.get_result()` at its **default `tgt_type = HLL_4`**, so contribute produces HLL_8 and merge produces HLL_4 (Addendum E). Governed state is unaffected (Q5) — it is an undeclared carrier change, and it is evidence that `tgt_type` is not governed. |
