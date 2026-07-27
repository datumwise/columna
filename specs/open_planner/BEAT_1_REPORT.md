# Open Planner — Beat 1 (the execution beat) — REPORT

**2026-07-27.** Research instrumentation only; zero product-surface change. Every number below came
from a run, not a recollection. Re-derive any of it with the scripts named beside it.

Status ladder: **CONSTRUCTED → EXECUTED → VERIFIED.**

---

## The six deliverables

| # | deliverable | status | script |
|---|---|---|---|
| 1 | IR closure | **EXECUTED** — closed, unfalsified (not proven) | `ir_closure_and_seam.py` |
| 2 | Attack B, engine path | **VERIFIED** (numbers) · **EXECUTED** (both halves) | `attack_b.py` |
| 3 | The seam test | **VERIFIED** — first certificate | `ir_closure_and_seam.py` |
| 4 | Class C construction | **EXECUTED** — pair established | `class_c.py` |
| 5 | P-BLIND | **EXECUTED** — property fails as formalized; cause **reclassified → OF-24** | `p_blind.py` |
| 6 | Beat report | this document | — |
| A | Class A (v2) | **EXECUTED** — pair frozen | `attack_a.py` |

---

## 1 · IR closure — CLOSED, at an honest rank

Zero ninth-node candidates. Reported **per corpus** so no total hides a weak member:

| corpus | asks | served | closed |
|---|---|---|---|
| `recapture_exemplars` | 11 | 8 | ✅ |
| `demo_wheel` | 4 | 2 | ✅ |
| `core_tests` | 58 | 20 | ✅ |
| `server_tests` | 23 | 3 | ✅ |

All eight nodes observed in the wild: ANCHOR/CARVE/COLUMN/REDUCE on every served ask · TRANSPORT 25 ·
DERIVE 8 · CROSS 3 · ALIGN 3.

**Rank: UNFALSIFIED, not proven.** 33 served asks is a modest battery, and most non-served asks are
parser-negative tests. Closure survived every ask we could put through it; that is not the same as
closure being established.

### F2 — the "111-ask battery" does not exist as an executable corpus

The 111 asks are the **Ground Truth benchmark's natural-language questions**. Verified against the
frozen kit: `manifest/questions.jsonl` holds exactly **111** records whose `text` is prose and whose
`ground_truth` is a **precomputed scalar with a tolerance**; the corpus contains **zero** occurrences
of `select`, `frameql`, `sql`, or `at {`. Its warehouse is the kit's own coframe, not Cascadia — so
vendoring could not have produced Cascadia-executable asks even had the forms existed.

**Ruled NL-ONLY.** Closure runs on the in-repo executable corpora; **v1.1 carries a one-line erratum**
replacing the deposit's "111-ask battery" phrase, with the own-coframe finding as its footnote.

---

## 2 · Attack B — three facts of different epistemic rank

**Numbers: VERIFIED.** Twelve of twelve, exact, on an independent path. Overall ratio **1.2100**
against the desk's 1.21×.

| month | desk f/u | direct f/u | IR f/u | ask (`aov`) |
|---|---|---|---|---|
| 2024-01 | 139.91 / 164.03 | ✓ / ✓ | ✓ / ✓ | 139.914394 |
| 2024-02 | 125.81 / 145.22 | ✓ / ✓ | ✓ / ✓ | 125.809543 |
| 2024-03 | 127.25 / 149.38 | ✓ / ✓ | ✓ / ✓ | 127.251435 |
| 2024-04 | 137.91 / 156.09 | ✓ / ✓ | ✓ / ✓ | 137.910982 |
| 2024-05 | 139.14 / 158.48 | ✓ / ✓ | ✓ / ✓ | 139.139002 |
| 2024-06 | 130.56 / 152.41 | ✓ / ✓ | ✓ / ✓ | 130.562459 |

**Faithful half: ENGINE-EXECUTED** via `aov`, coincidence-checked — 19995 transaction rows vs 19994
distinct atoms, exactly one collision, falling outside the published window. Asserting that equality
globally would be wrong; the counts are frozen so a later reader re-checks rather than inherits.

**Unfaithful half: NOT EXPRESSIBLE FROM THE ASK SURFACE (F1)** — `planner.py:371`, single-level input
anchors this build — **and EXECUTED at its native IR layer**, engine unmodified, via
`ColumnEngine.resolve` + `ColumnEngine.reduce_series_to_anchor`.

> **One primitive pair, one changed argument — `input_grain` `customer·store·product·day` vs
> `store·product·cal.month` — a 21% different answer.**

**F1 is a RECALL row, not a safety bug.** And the doctrine it minted:

> An expressible pinned ask is its own denotation — `avg(revenue @ {store*product*month})`, once
> askable, is a different question, faithfully answered. **No ask can be unfaithful to itself;
> unfaithfulness lives only in the gap between a plan and an ask** — which is why obligation B has no
> ask-surface analogue, why the shipped mood contract already CLARIFIES on the underdetermined form,
> and why the kernel begins exactly where the grammar's protection ends: **at the searcher's channel.**

---

## 3 · The seam — FIRST CERTIFICATE

**56 comparisons · 0 disagreements · 0 errors. No live bug.**

Certifies: planner-derived edges (`PlannerView.find_path`, via `cone_atoms_and_edges`
`planner.py:602-630`) ≡ engine-mirrored transports (`Manifold.find_path`, via `ColumnEngine.resolve`
`engine.py:84+`). `planner.py:689`: *"the engine mirrors this."*

**Non-vacuity established BEFORE the claim.** The two are separate BFS bodies over separate edge
collections — provenance-free shape tuples vs physical-carrying edges, `self._out` vs `self.out_edges`
— **not a delegation.** Had it been one, the certificate would have read green and meant nothing.

**Negative control, baked into the artifact.** Tamper one side's lineage → the test disagrees; restore
→ it agrees. `control_valid: true`.

**Perimeter, stated honestly:** shape edges are copy-derived from the Manifold's at
`projection.py:127`, so what is certified is that the two **traversals** agree, *including across that
copy*. A defect in the single upstream declaration parse is outside this seam.

---

## 4 · Class C — the pair, and the audit that preceded it

**Natural-coincidence audit (route (a)) — run first, reported, exhausted:**

- `touch` vs `primary`: exactly **one** natural coincidence, **G11** (301693.50 ≡ 301693.50). Cause:
  G11 holds priority 1, the minimum, so everything touching it has it as primary. **Robust — no
  single row can break it**, because nothing outranks priority 1. Recorded and set aside.
- `split` vs `primary`: **no** coincidence anywhere.
- **No** category has all-single-membership products (every one has 33–46 multi-membership).

Route (a) exhausted ⇒ A1's sanctioned route (b), mint the fixture.

> **CONSTRUCTION LEMMA (ratified 2026-07-27).** A *robust* coincidence is useless for M₀→M₁ **precisely
> because no single row can break it.** G11's coincidence is real and natural, but it rests on
> priority 1 — the minimum — so nothing can outrank it and no perturbation of one row disturbs it.
> **Coincidence-fragility is a requirement of the protocol, not an accident of it.** A Class C
> exhibit must be built on an agreement that one row can destroy; an agreement that survives every
> row is an invariant wearing a coincidence's clothes.

**The pair.** `revenue AT {category.touch}` vs `revenue AT {category.primary}` — genuinely different
denotations (the Manifold's own faces say so: touch *"totals exceed the grand total"*, primary
*"totals match"*).

| | outputs identical? |
|---|---|
| **M₀** — shipped warehouse, memberships collapsed to one per product | **YES**, every row |
| **M₁** — M₀ **+ one row**: `P0022` also in `G06` (priority 12 > G10's 2, so primary is unmoved) | **NO** |

**Divergence: one cell.** `G06` — touch 245854.96 vs primary 176569.50, **delta +69285.46 = exactly
P0022's revenue.**

> Identical outputs on M₀, different on M₁, **from one row** — so no finite set of output observations
> establishes faithfulness. Only `plan ⊨ ask` separates these two, and it separates them on M₀ just as
> surely as on M₁, where the outputs happen to agree.

---

## 5 · P-BLIND — the property fails as formalized; cause reclassified to OF-24

Four provenance wrappers: `W1` static path · `W2` canonical round-trip · `W3` handcrafted AST ·
`W4` shuffled warehouse.

**F5 — ATTEMPT-COUNT DEPENDENCE, the explicitly-forbidden kind.** The formalized claim says
`K(M, P, A)` depends on nothing but the model, plan and ask — *"never on planner identity, confidence,
provenance, token probabilities, search path, **or attempt count**."*

**It depends on attempt count.** On a **fresh** store:

```
call 0:  rollup_severity = none   disclosures = []
call 1:  rollup_severity = info   disclosures = ['freshness']
call 2:  rollup_severity = info   disclosures = ['freshness']
```

Deterministic, and **reproducible across cold stores** (2/2 trials, 3 of the 6 probe asks). **The
first asker gets LESS disclosure than the second, for the same question on the same data.** The caveat
is graded immaterial/info, so this is not a wrong number — it is **the honesty surface varying with
call count**, which is precisely the property the mood contract exists to make invariant.

**This is also what the wrapper comparison first mistook for provenance sensitivity**: `W1` simply ran
first. Two instrument corrections were required before the real finding surfaced, both recorded in the
script rather than quietly fixed:

- **F4 — run-to-run byte-reproducibility.** `revenue AT {category.split}` is not byte-stable across
  repeated identical runs. Magnitude: **1.4e-16 relative — one ULP of float64**, on 2 of 12
  categories; grand total stable. **By the 0.13.1 doctrine this is noise, not a wrong number** —
  calling it one would be false precision. But byte-reproducibility is what byte-identical
  certificates and P-ECON's certified-plan cache ("deterministic serving") would rest on.
- **Digest-of-rounded was the wrong instrument** and was discarded: rounding does not reliably absorb
  1-ULP noise, since two values a hair apart can straddle a rounding boundary. Replaced with a
  structural-exact / numeric-tolerant comparison.

**Had the first draft been reported, it would have said "P-BLIND fails on provenance." That would
have been a confident wrong finding.** The property does fail — for a different, sharper reason.

> **PROVERB (ratified 2026-07-27, from this near-miss).** *The confound wears the hypothesis's
> clothes — rotate the order before attributing.* W1 ran first and W2/W3 ran after it, so call order
> presented itself as provenance sensitivity, wearing exactly the shape the experiment was looking
> for. The tell was that the ONE thing being varied deliberately (provenance) and the one thing
> varying incidentally (position in the sequence) were perfectly confounded — and nothing in the
> result distinguished them until the order was rotated.

> **PROVERB (ratified 2026-07-27, from the seam's negative control).** *A test that has never failed
> has not been shown to be able to fail — bake the tamper-and-restore control into the artifact.*

**Standing standard, ratified:** structural-exact / numeric-tolerant comparison. **Digest-of-rounded
is retired** — rounding cannot reliably absorb sub-tolerance noise, because two values a hair apart
can straddle a boundary and quantize differently.

---

## Findings ledger

| # | finding | rank |
|---|---|---|
| **F1** | Attack B's unfaithful plan is not expressible from the ask surface (`planner.py:371`) | RECALL row, ruled — not a safety bug |
| **F2** | The "111-ask battery" is NL-only; not an executable corpus; own-coframe warehouse | corpus determination; v1.1 erratum |
| **F3** | A1 v0.1 misdescribed the shipped model three ways; Attack A did not compose | desk defect, owned, patched in v0.2 |
| **F3b** | A1 v0.2 names `units`; shipped is `units_sold` | desk defect, owned, patched in v0.3 |
| **F4** | Served values not byte-reproducible for the `split` face (1 ULP) | below tolerance — reproducibility, not correctness |
| **F5** | Adjudication depends on attempt count; first call omits the cache annotation | **RECLASSIFIED → OF-24.** Desk root-cause: the content is *"served from cache"* (`engine.py:131,488`), version-checked, so every call's disclosure is TRUE and values are identical. The defect is a **mislabeled, mischanneled annotation** — mechanical serving-provenance wearing the semantic name FRESHNESS on the semantic channel. **Not launch-blocking.** |

**Four of the six were caught by the beat's own verification layer, including two inside desk
artifacts and two inside this beat's own instruments.** The instrument corrections (F4's digest, F5's
mistaken provenance read) are recorded rather than silently fixed, because an instrument that was
wrong once should say so.

---

## Standing off-ramps — status

- **A ninth IR node** — none found. Closure holds at its stated rank.
- **Seam disagreement** — none. The beat continued, as ruled.
- **Material divergence from the desk's numbers** — none. Twelve of twelve exact.
- **F5 went to the desk and came back reclassified** — not a semantic failure but a channel error,
  **rowed as OF-24**. The row's design half feeds the program: the kernel's disclosure projection
  gains a **two-channel split** — *semantic* (call-invariant, **P-BLIND's true jurisdiction**) vs
  *mechanical* (legitimately variant, possibly not wire-worthy at same-version). Once split, the
  semantic channel can satisfy the attempt-count clause literally, while the mechanical channel is
  free to vary because it was never a claim about meaning.
- **F4's consequence is rowed where it belongs**: OF-23(b) now records that byte-identical
  certificates and P-ECON's certified-plan cache **inherit** its deterministic-serving requirement.
