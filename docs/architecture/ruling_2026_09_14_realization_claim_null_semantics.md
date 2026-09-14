# Ruling — 2026-09-14 — a realization null makes **no assertion**

**Status:** ruled by Huayin, 2026-09-14. Recorded here with its consequences and an implementation
plan. **Not yet implemented** — the defect it corrects is rowed as **OF-47** and stands against live
`main`.

---

## 1. The ruling

> **A realization null means no realization assertion is made. It is never a positive claim that the
> governed fact is "none."**

For `continuation_operator` specifically:

| family's C8 continuation standing | the realization claim must be |
|---|---|
| **ESTABLISHED** | **present, and must name the matching operator** |
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

### 4.5 The generalization needs its own audit, not an assumption

The ruling extends to *every* optional realization field. Applying it needs each field's current
null-handling read, not a blanket edit. The v2 shape's optional fields are `formation_operator`,
`continuation_operator`, `endpoint.schema`, `endpoint.column`. **`endpoint.schema` is the one to look
at first and is likely an EXCEPTION**: `None` there is already documented as *"a POSITIVE claim that
no schema qualification applies and never a dropped one"* (`source.py`), which is exactly the
*"unless a field's ratified contract explicitly assigns another meaning"* carve-out. That reading is
load-bearing for R2 and should be **confirmed as an explicit exception in the ratified contract**
rather than left to be rediscovered — otherwise a future reader applying this ruling uniformly will
break schema selection.

---

## 5. Open, for ratification

1. **Jurisdiction for a claim present where the law establishes none.** `MappingIncomplete` (the
   mapping is wrong) or `LogicalMeaningMissing` (the mapping asserts law that does not exist)? The
   second reads truer; the first matches the neighbouring refusals.
2. **Compatibility.** This **tightens** a ratified conformance check: every existing v2 mapping that
   omitted `continuation_operator` for an ESTABLISHED C8 now refuses. Only two artifacts exist in this
   tree, but the realization profile is **frozen** — is tightening a frozen profile's check a format
   version event, or a conformance repair that leaves the format alone? *(Recommendation: a
   conformance repair. The shape does not change; what changes is that a field already in the shape is
   finally read. But it should be said, not assumed.)*
3. **`endpoint.schema` as a named exception** under §4.5 — confirm, or reopen?
4. **Does the Platform's continuation check gate serving, or only disclose?** Recommendation: gate, on
   the same reasoning as `exactness` — but Platform has not previously refused on a continuation fact
   at all, so it is a new refusal on a live path.
