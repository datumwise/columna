# Ruling — 2026-09-14 — a realization null makes **no assertion**

**Status:** **RATIFIED** by Huayin, 2026-09-14, and amended the same day with the refusal taxonomy,
the `endpoint.schema` exception, the format-version ruling and the Platform gate ruling. **Not yet
implemented** — the defect it corrects is rowed as **OF-47** and stands against live `main`.

**Implementation order (ruled):** this repair, together with coordinate type/nullity admission
(OF-48), is the **pre-ingress conformance work**. `columna-adbc` is implemented only after both are
green and merged.

---

## 1. The ruling

> **A realization null means no realization assertion. It is not a positive assertion of "none,"
> except where a field-specific contract explicitly says otherwise.**

For `continuation_operator` specifically:

| family's C8 continuation standing | the realization claim must be |
|---|---|
| **ESTABLISHED** | **present, and must match the governed continuation operator** |
| **EXPLICIT_NONE** | **null / absent** |
| **UNESTABLISHED** | **null / absent** — and the profile may not invent a continuation |

> **The rule applies equally to primitive and constructed families, including entailed C8.**

And generally:

> **The same null interpretation applies to every optional realization field, unless that field's
> ratified contract explicitly assigns another meaning.**

### What the ruling turns on

> **The realization claim is implementation agreement with governed law. It is not the authority that
> creates the law.**

A mapping that says nothing has not agreed to anything. Reading its silence as *"the governed fact is
none"* would let the private mapping settle a governed question by declining to answer it — which is
the direction of authority reversed. Under the ruling, silence where the law has spoken is a
**missing agreement**, and it refuses.

**This deliberately removes the current null exemption when C8 is established.**

---

## 2. What was true before the ruling

Recorded because a conformance ledger must not lose it once the repair makes it false. Full account in
**OF-47**; the measurements, on the shipped compiler at `main` = `e686d41`:

| mutation of the realization's `continuation_operator` | today |
|---|---|
| `revenue` (C8 ESTABLISHED = SUM) — claim **removed** | compiles, image **byte-identical** |
| `revenue` — claim **null** | compiles, image **byte-identical** |
| `revenue` — claim `"wildly_wrong"` | refuses |
| `count(revenue@sale_at)` (constructed) — claim `"wildly_wrong"` | compiles, image **byte-identical** |
| `min(revenue@sale_at)` (constructed) — claim `"sum"`, against its entailed C8 of MIN | compiles, image **byte-identical** |
| `max(revenue@sale_at)` (constructed) — claim **null** | compiles, image **byte-identical** |

The field is read in exactly one place in the repository — `compile_v2.py:437`,
`if real.continuation_operator not in (None, op)` — inside `if cont.standing == ESTABLISHED`, on the
primitive branch. `columna-platform` does not read it at all.

---

## 3. The consequence nobody has looked at yet: **three fixtures become non-conformant**

This is not an abstract tightening. The lighthouse families' resolved C8, measured:

| family | C8 | formation claim today | continuation claim today | **required after the ruling** |
|---|---|---|---|---|
| `revenue` | ESTABLISHED **SUM** | — (primitive) | `"sum"` ✅ | `"sum"` — **already conformant** |
| `count(revenue@sale_at)` | ESTABLISHED **SUM** | `"count"` | *absent* ❌ | **`"sum"`** |
| `min(revenue@sale_at)` | ESTABLISHED **MIN** | `"min"` | *absent* ❌ | **`"min"`** |
| `max(revenue@sale_at)` | ESTABLISHED **MAX** | `"max"` | *absent* ❌ | **`"max"`** |

> **`count` is the case that proves the field is not redundant with `formation_operator`, and it
> should be the fixture the controls are written around.** COUNT's formation **counts** and its
> continuation **SUMS** (§5.2 — the distinction `_check_continuation_conformance` already exists to
> police on the mechanics side). So `count(revenue@sale_at)`'s realization must carry
> `formation_operator: "count"` **and** `continuation_operator: "sum"` — two different operators, two
> different governed facts, one artifact. For `min` and `max` the two claims happen to coincide, which
> is precisely why a repair validated only on those two would look finished and prove nothing.

Affected artifacts: `columna-core/tests/fixtures_v2/lighthouse.py` and
`columna-platform/fixtures/proof_a/private-core-mapping-v2.json` (the only two mapping artifacts in
the tree).

---

## 3a. The continuation matrix — **RATIFIED 2026-09-14, all seven cells**

**Do not collapse the cases.** The complete matrix, as ruled:

| governed C8 | realization claim | outcome |
|---|---|---|
| **ESTABLISHED = *X*** | claim *X* | **conforming** |
| **ESTABLISHED = *X*** | null / absent | **mapping incomplete** |
| **ESTABLISHED = *X*** | claim *Y* ≠ *X* | **realization contradicts governed law** |
| **EXPLICIT_NONE** | null / absent | **conforming** |
| **EXPLICIT_NONE** | any operator claim | **realization contradicts governed law** |
| **UNESTABLISHED** | null / absent | **no realization assertion; the profile may not invent continuation** |
| **UNESTABLISHED** | any operator claim | **logical meaning unestablished; the realization may not invent it** |

> ### The EXPLICIT_NONE / UNESTABLISHED distinction is load-bearing
>
> Ruled, and it is the reason the last four rows are four rows and not two:
>
> - **`EXPLICIT_NONE` is a positive governed negative, and can therefore be CONTRADICTED.** The
>   publication has spoken: there is no continuation. A realization that names one is asserting
>   against a fact that exists.
> - **`UNESTABLISHED` supplies no governed continuation fact for the realization to contradict.** The
>   defect is different in kind: the realization is attempting to **manufacture analytical meaning**.
>   There is nothing to disagree with, and that is precisely the problem.
>
> Two wrong claims, two different wrongs, two different people to tell. Collapsing them would file a
> manufactured law as a disagreement, and send whoever reads it looking for a governed fact that was
> never there.

**Cell 4 — `ESTABLISHED = X` with a claim of `Y` — is ruled a contradiction** (2026-09-14), *"not
mapping incompleteness and not want-of-state"*. It is the only cell that refuses today, and it
refuses as `MappingIncomplete`; correcting it is part of this repair.

### The vocabulary inspection the ruling required

> *"Before implementation, inspect the existing exception/refusal vocabulary for an exact
> contradiction category. If one exists, use it."*

**Done. There is none, in any of the three vocabularies.**

**`columna_core.compiler.refusals` — five categories, none exact.**

| category | why it is not this |
|---|---|
| `InputIdentityMismatch` | *is* a mapping-vs-publication contradiction, but at the **identity** level — "this mapping is not for this publication" — and checked before lowering begins. Not a per-fact contradiction. |
| `LogicalMeaningMissing` (**L**) | "the publication does not carry meaning the compiler needs". Under EXPLICIT_NONE the publication **does** carry the meaning; it positively says *none*. Nothing is missing. |
| `MappingIncomplete` (**M**) | "the realization is **absent or ambiguous**". A contradicting claim is **present and wrong**, which is neither. |
| `UnsupportedCoreCapability` (**C**) | a capability gap. |
| `ExecutionRepresentationGap` (**G**) | a representation gap. |

**`columna_platform.refusals` — four conditions, none exact.** `WantOfLaw` (the law does not license
it — but here it does, and says the opposite of the claim); `WantOfState` (the material is not
admissible, remedy **re-materialization** — which would not help, the mapping is wrong);
`WantOfCompatibility` (two *states*' standings may not be combined — right shape, wrong subject);
`UnsupportedByThisProfile` (a capability limit, and explicitly not a governed verdict).

**The closed wire registry — 30 registered reasons, none exact.** The nearest is `contradicted_edge`
*("data violates a declared functional edge (tested+refuted)")* — a genuine contradiction category,
but its subject is **data against a declaration**, not **a realization claim against governed law**.

### Therefore: the smallest explicitly named contradiction refusal, plus a minted wire reason

**Core — a sixth category.**

```
MappingContradictsLaw  (X)   the private mapping asserts a fact the governed publication
                             positively denies -- present and wrong, not absent or ambiguous.
                             Fix belongs in the private mapping (same owner as M, different
                             condition). Added to refusals.CATEGORIES, which a completeness
                             test already pins against the class set.
```

Keeping the `Mapping…` prefix is deliberate: **the owner is the same as `MappingIncomplete`** — the
mapping author — and only the condition differs. A name like `RealizationContradiction` would put the
same person's defect under a different noun for no gain.

**Platform — a fourth `ProofRefusal`.**

```
RealizationContradictsLaw    jurisdiction = "realization"
                             remedy = "the realization claim must be corrected to the governed
                                       law; RE-MATERIALIZATION CANNOT RESOLVE IT"
```

The remedy clause is the whole reason it is not `WantOfState`: `WantOfState` promises that
re-realizing the **material** fixes it, and here nothing about the material is wrong.

`LogicalMeaningMissing` (the UNESTABLISHED-with-a-claim row) needs **one clause added to its
docstring**, not a new category: it currently reads *"the publication does not carry meaning the
compiler needs"*, and must also cover *"…and the realization attempted to MANUFACTURE it, which no
profile may accept."*

### The wire reason — **MINTED 2026-09-14**

Ruled and **already added to the closed registry** (`columna_core/disclosure.py`), because minting is
a ruling and the registry is where rulings about this vocabulary live:

```python
"realization_contradicts_law": (ERROR, None, REALIZATION),
```

| | |
|---|---|
| **meaning** | the realization artifact asserts an execution fact **incompatible with a positive governed fact** in the publication |
| **mood** | `ERROR` |
| **jurisdiction** | `REALIZATION` |
| **explicitly not** | `want_of_state`, `want_of_law`, `unsupported` |
| **alternatives** | **none — deliberately omitted** |

**On the omitted remedy.** *"Do not offer ordinary `REMATERIALIZE` as the remedy. Re-materializing the
same data cannot repair a realization claim that contradicts the governing law. If the existing
alternatives vocabulary has no already-lawful spelling for 'correct/replace the realization mapping,'
omit an alternative rather than reuse a misleading one."* **It has none.** The Platform's only remedy
constant is `REMATERIALIZE = "re-realization / re-materialization may resolve this"` — and that
string is the trap rather than the near-miss: it *says* "re-realization", which reads lawful for a
mapping fix, while bundling it with a data re-pull that the operator will then perform. So:
`alternatives = ()`.

**The detail should name** the family / canonical reference, the governed C8 fact, the realization
claim, and the contradiction — **without exposing internal implementation identifiers
unnecessarily.** (Opaque `family_id`s and module paths are implementation; `revenue`, `SUM` and the
claimed operator are the fact.)

**No emitter yet, and that is not an oversight.** The checks that raise it are gated behind
ratification of this candidate set. `outcome_for` is a keyed lookup, so an entry with no emitter
changes no behaviour — and the classification is pinned by a control in the vocabulary's own suite
(`test_realization_contradicts_law_is_classified_and_is_not_want_of_state`), so when the checks land
they inherit the ruled verdict rather than choosing one.

### ⚠ The dispatch defect this repair must close — **measured**

All three Platform-refusal→wire translation sites read:

```python
reason = WANT_OF_LAW if isinstance(r, WantOfLaw) else WANT_OF_STATE
alts   = (REMATERIALIZE,) if reason == WANT_OF_STATE else ()
```

**A two-way `if/else` over a four-class taxonomy.** Anything that is not a `WantOfLaw` is labelled
`want_of_state` on the wire and offered `REMATERIALIZE`. So:

**Measured, not argued** (`cap_v1_evidence/run_refusal_dispatch.txt` — the expression is read out of
`serving.py` at runtime rather than restated, so the probe cannot drift from the code it reports on):

```
WantOfLaw                -> reason='want_of_law'      alternatives=()
WantOfState              -> reason='want_of_state'    alternatives=(REMATERIALIZE,)
WantOfCompatibility      -> reason='want_of_state'    alternatives=(REMATERIALIZE,)   <-- COLLAPSED
_StandInContradiction    -> reason='want_of_state'    alternatives=(REMATERIALIZE,)   <-- COLLAPSED
```

So a `RealizationContradictsLaw` dropped into today's code would reach the wire **as `want_of_state`
with `REMATERIALIZE` offered** — precisely the misdirection the ruling forbids. `WantOfCompatibility`
already meets that branch, against its own docstring's warning. (Whether `WantOfCompatibility`
*reaches* a live translation site on a served request is a separate question — it is raised from
`store.combine`, which is not on the single-request path — and is **not** claimed here.)

**Closing it is part of this repair, and the mechanism is specified rather than left to taste:**

1. the translation becomes an **exhaustive mapping keyed on the refusal class**, not an `if/else` on
   one of them;
2. a **completeness pin** asserts every `ProofRefusal` subclass has an entry — the same discipline
   `refusals.CATEGORIES` and `REASON_OUTCOME` already carry, where *"a category that exists but is not
   enumerated is a condition that vanishes from the report rather than surfacing in it"*;
3. `alternatives` is derived from the mapping, so `REMATERIALIZE` cannot be attached to a reason that
   did not ask for it.

With (1) and (2), a future refusal class with no wire reason **fails the build** instead of silently
inheriting `want_of_state`. That is the executable proof, and it lands with the repair.

**`WantOfCompatibility` is the second beneficiary and should be fixed in the same change** — it is
already mis-labelled by the same expression, and repairing the dispatch for one class while leaving
the other in the `else` would be the same defect with one fewer instance.

---

## 4. Implementation plan

### 4.1 Order

1. **K0v2 and the Platform profile are repaired in the same landing.** Not sequenced, not split across
   PRs. A field checked in one profile and absent from the other is the same silent divergence one
   layer up, and it is the condition OF-47 was opened about.
2. Fixtures updated to conformance (§3) **in that landing**, so the positive path is green for the
   right reason.
3. Mutation controls added **in that landing** (§4.4), because every mutation in §2 compiles today and
   a repair without them cannot be shown to have changed anything.

### 4.2 K0v2 (`columna-core/compiler/compile_v2.py`)

**The primitive branch.** The check must move **out** of `if cont.standing == R.ESTABLISHED:`, which
is the structural cause of consequence (iii) in OF-47 — a guard inside a conditional cannot police the
conditional's other branches. Shape:

- C8 ESTABLISHED → the claim must be **non-null** and must equal the operator this profile realizes
  that law as. Absent/null refuses with a message in the register CHECK 3 already uses for its twin
  (*"makes no delivery claim"*), naming the established law.
- C8 EXPLICIT_NONE or UNESTABLISHED → the claim must be **null or absent**. A present claim refuses:
  the mapping is asserting a continuation the governing law does not establish.

**The constructed branch.** A new check, beside CHECK 3 and **not inside**
`_check_continuation_conformance`. That helper is correctly named for what it does — Core's engine
mechanics against governed law — and folding the realization-claim check into it would merge two
jurisdictions into one function, which is the shape of the defect being repaired.

The constructed check reads `creal.continuation_operator` against `cview[C8_CONTINUATION]` under the
same three-way rule. It must **not** compare against the formation operator: for COUNT they differ.

**Jurisdiction.** `MappingIncomplete` for a missing required claim (the twin of CHECK 3's refusal, and
the mapping is literally incomplete). `MappingIncomplete` for a mismatched claim, matching the existing
primitive-branch refusal. A *present* claim where the law establishes none is arguably
`LogicalMeaningMissing` rather than `MappingIncomplete` — **open, see §5**.

### 4.3 The Platform profile (`columna-platform`)

Platform has **no** continuation conformance today. It must acquire the same three-way rule, stated
separately in its own module rather than imported from `compile_v2`:

- the two profiles have different execution grammars, and a shared table would tie their envelopes
  together silently — the divergence hazard in the other direction;
- Platform's refusals carry **its** jurisdictions (`WantOfLaw` / `WantOfState` /
  `UnsupportedByThisProfile`), not Core's compiler refusals.

Placement: alongside the existing `exactness` check in `serving.py`, which is already the site that
checks a realization **claim** against governed law before material is reached. Continuation
conformance is knowable from law and claim alone, so it belongs there and not at admission — the
ordering principle `admit_anchored` already states.

> **IT IS A GATE, NOT A DISCLOSURE (ruled 2026-09-14).** If the realization claim disagrees with
> governed C8, **the material path does not proceed.** Do not serve with a caveat. A served number
> carrying a disclosure that its continuation claim was wrong is still a served number, and the
> disclosure channel is not where a conformance failure belongs.

### 4.4 Controls — the part that is not optional

One test per cell, each **failing on `main` today**:

| # | control |
|---|---|
| 1 | primitive, C8 ESTABLISHED, claim absent → **refuses** |
| 2 | primitive, C8 ESTABLISHED, claim `null` → **refuses** |
| 3 | primitive, C8 ESTABLISHED, claim mismatched → refuses *(passes today; pins the one direction that already worked)* |
| 4 | primitive, C8 ESTABLISHED, claim correct → **serves** |
| 5 | constructed, C8 ESTABLISHED, claim absent → **refuses** |
| 6 | constructed, C8 ESTABLISHED, claim mismatched → **refuses** — written on **`count`**, whose continuation (`sum`) differs from its formation (`count`), and asserting that claiming `"count"` refuses |
| 7 | constructed, C8 ESTABLISHED (**entailed**), claim mismatched → **refuses** — written on `min`, so the "including entailed C8" clause is pinned by a test and not only by prose |
| 8 | C8 not ESTABLISHED, claim present → **refuses** |
| 9 | the same matrix, on the **Platform** path, through the public wire |
| 10 | a **byte-identity** control: two mappings differing only in `continuation_operator` must not compile to the same image — stated as an invariant, because "byte-identical" is how this defect was found and is the only evidence that will notice it returning |
| 11 | **`EXPLICIT_NONE` + an operator claim** refuses as a **contradiction**, and **`UNESTABLISHED` + an operator claim** refuses as **manufactured meaning** — two controls, asserting *different* categories, so the load-bearing distinction is pinned by the build and not only by §3a's prose |
| 12 | **the wire face**: a contradiction refusal reaches the wire as `realization_contradicts_law`, `ERROR` / `REALIZATION`, **with `alternatives == ()`** — asserted positively, and asserted *negatively* against `want_of_state` and against `REMATERIALIZE` appearing anywhere in the payload |
| 13 | **the completeness pin**: every `ProofRefusal` subclass has a wire-reason entry. A new class with none must **fail the build**, not inherit `want_of_state` |
| 14 | `WantOfCompatibility` no longer reaches the wire as `want_of_state` — the second beneficiary of control 13, pinned so the dispatch repair is not done for one class only |

### 4.5 `endpoint.schema` — the field-specific exception, **CONFIRMED**

> **RULED 2026-09-14.** `endpoint.schema = null` is a **positive realization statement that no schema
> qualification applies.** This is an explicit exception to the general optional-field rule above.
> **Do not reinterpret schema-null as "no assertion."** The realization freeze already gave `schema`
> this meaning; preserve it.

This is the *"unless a field's ratified contract explicitly assigns another meaning"* carve-out, and
it is load-bearing for R2: `source.py` selects objects on `(schema, table)` where `None` and `"sales"`
are **different keys**, and K0v2 *refuses* a non-null schema because its execution grammar cannot
represent one. A uniform application of the null rule would break both.

### 4.6 Frozen profile / format version — **NOT a version event (ruled)**

> **Tightening these checks is not a realization-format version event.** The serialized shape is
> unchanged. This is conformance repair against already-ratified meaning. **Do not bump the
> mapping-format major merely because previously-ignored facts begin to be checked correctly.**
> (Huayin, 2026-09-14.)

`mapping_format_version` stays `"2"`. What changes is that a field already in the frozen shape is
finally read.

### 4.7 The rest of the generalization still needs its own audit

The ruling extends to *every* optional realization field. Applying it needs each field's current
null-handling read, not a blanket edit. The v2 shape's optional fields are `formation_operator`,
`continuation_operator`, `endpoint.schema` (**ruled an exception**, §4.5) and `endpoint.column`.

`endpoint.column` is the remaining one to read: it is already refused as absent on both the K0v2
primitive path and the Platform material path, so the general rule may already hold there — but *may
already hold* is not *checked*, and this ruling is what makes the difference matter.

---

## 5. Ruled, 2026-09-14 — and what remains

### Ruled and folded in

| | ruling |
|---|---|
| **The null rule** | A realization null means **no realization assertion**. Not a positive assertion of *"none"*, except where a field-specific contract explicitly says otherwise. (§1) |
| **C8 cells** | ESTABLISHED → claim required and must match; EXPLICIT_NONE → claim absent/null; UNESTABLISHED → claim absent/null and the profile may not invent continuation. Primitive and constructed alike, **including entailed C8**. (§1) |
| **Taxonomy** | Do not collapse the cases. Inspect the existing vocabulary first; if no exact contradiction category exists, introduce the smallest explicitly named one rather than misusing `MappingIncomplete` or `LogicalMeaningMissing`. (§3a — **none exists; two are proposed**) |
| **`endpoint.schema`** | `null` is a **positive** statement that no schema qualification applies — an explicit exception. Do not reinterpret it. (§4.5) |
| **Format version** | Not a version event. The serialized shape is unchanged; this is conformance repair against already-ratified meaning. (§4.6) |
| **Platform behaviour** | A **gate, not a disclosure.** If the claim disagrees with governed C8, the material path does not proceed. Do not serve with a caveat. (§4.3) |

### Also ruled 2026-09-14

| | ruling |
|---|---|
| **Cell 4** | `C8 ESTABLISHED = X` + a claim of `Y ≠ X` is **realization contradiction** — not mapping incompleteness and not want-of-state. (§3a) |
| **The full matrix** | Seven cells, ratified. The `EXPLICIT_NONE` / `UNESTABLISHED` distinction is **load-bearing**: a positive governed negative can be contradicted; an unestablished fact cannot, and the defect there is manufacture. (§3a) |
| **Wire reason** | `realization_contradicts_law` **minted** — `ERROR` / `REALIZATION`, not `want_of_state`, not `want_of_law`, not `unsupported`, **no alternatives**. (§3a) |

### Nothing open in this ruling

Both prior open items are ruled. What remains is implementation, which is gated behind ratification of
the candidate set — and which must include the dispatch repair above, or the ratified taxonomy will be
honest internally and wrong on the wire.
