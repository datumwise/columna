# Theory of Data v6 — runtime reconciliation checkpoint

**Status:** documentation-only checkpoint. **Authorizes no code, grammar, wire, or terminology change.**
**Date:** 2026-08-18
**Sources:** `columna` @ main (`0.15.0-core`, head `2455509`). Reads with *Theory of Data v6.0*
(Zenodo 21958062), *Analytical Governance v1.0* (Zenodo 21959749), *Frame-QL: An Introduction v2.0*
(Zenodo 21960798). The **Frame-QL Manual remains normative** for shipped syntax and behaviour.

## Why this note exists

ToD v6 retires **member** from the core ontology and fixes the analytical identity as:

```
measure = measure family @ anchor
```

The shipped runtime is full of the word `member`. The naive reconciliation — read the runtime
`MeasureColumn.family` as a v6 *measure family* and delete `member` — is **wrong in direction** and
would collapse a distinction ToD v6 §5.1 explicitly forbids collapsing. This note records the correct
reading before anyone renames anything.

---

## 1. The semantic rule (normative for this checkpoint)

> **A runtime member corresponds to a v6 measure-family identity when it denotes a distinct governed
> analytical identity with its own coherent reducer law / constitutive identity. Runtime type names are
> not themselves ontological mappings.**

Deliberately **not** written: `FamilyMember == MeasureFamily`. The inventory below shows the runtime
type is used for two structurally different jobs, only one of which is a family identity.

### The grounding in ToD v6

§3.2 — a measure family has **one declared full reducer law**, and a unique canonical governed name.

§5.1 — *"Two operations both called `SUM` do not necessarily belong to the same family law if their
participation, multiplicity, support, regime, approximation, or other contribution semantics differ."*
And: *"If two analytical directions require genuinely different coherent reducer laws, ToD does not
enlarge the family merely to preserve an everyday label."*

That is precisely the runtime `level` case.

---

## 2. Mapping table

| Runtime structure | ToD v6 reading | Notes |
|---|---|---|
| `Universe` (+ existence law, basis, ratification) | **universe / existence law** | clean |
| `DimensionLevel`, anchor tuple | **anchor** (governed partition) | clean |
| `MeasureColumn` (e.g. `level`) | **not a ToD object** | a governed *namespace + realization container* over one or more families |
| `MeasureColumn.family` (the dict) | **a set of family identities**, not one family | the runtime word `family` isclose to the inverse of the ToD word |
| `FamilyMember` on a MEASURE (e.g. `level.sum`) | **candidate measure-family identity** | when its reducer law/admitted movements differ from its siblings |
| dotted runtime name `level.sum` | **candidate canonical family name** | already injective; see §5 |
| `member @ anchor` (`level.sum @ store`) | **measure** `F@A` | the central v6 identity form |
| `FamilyMember` on a DERIVED (e.g. `aov.mean`) | **NOT an identity** — a *family-coherence claim* | see §4; this is the exception |
| `License` on a derived member | **evidence**, not identity | certification stage, not publication law |
| `BAnchor.blocked_lineages` | the family's **admitted family-preserving movements** | §3 |
| `DerivedColumn.resolution_anchor` (`AT day`) | **constitutive / graft anchor** (§3.4, §6.5) | identity-bearing, not a second current anchor |
| Frame-QL `AT {...}` | **frame output anchor** | one final analytical location |
| Frame-QL `@ {order}` | **source anchor of a consumed measure** | not a second current anchor of one measure |
| scan output (`cumsum(revenue.sum)`) | **result series, mints no canonical family** | Frame-QL Intro §8.3 |

*(The runtime word "family" and the ToD word "family" denote different things. This note does not
rename either.)*

---

## 3. Semi-additivity / the B-anchor has a v6 home

The shipped `level` measure declares:

```cml
MEASURE level ON store_days FROM eom_inventory VALUE level
    FAMILY {
        sum  BLOCKED { calendar }     -- stock summed across time doesn't reconcile
        last ORDER day                -- position = the latest snapshot
    }
```

`level.sum` and `level.last` permit **different analytical movements**: `sum` is barred along the
`calendar` lineage; `last` is an ordered monoid over `day`. Under ToD v6 §5.1 that difference in
admitted movement *is* evidence of **two distinct family-law identities** — not evidence that ToD needs
a `member` primitive.

Lawfulness belongs to the governed reducer law and its contracts over particular source→target
movements. `BAnchor.blocked_lineages` is therefore best read as **the set of family-preserving movements
this family admits**, which ToD already accommodates (§5.1: a family is coherent "over the
family-preserving paths it admits").

**Explicit non-reinterpretation:** the shipped V-anchor / M-anchor / B-anchor vocabulary is *not*
promoted to foundational ToD anchor kinds. Frame-QL Introduction v2.0 declines that reading, and this
note follows it.

---

## 4. The exception the inventory found: derived members are not family identities

`FamilyMember` is constructed at exactly three sites, in two structurally different roles:

| site | role | polarity |
|---|---|---|
| `parser.py:460` | MEASURE, single reducer inferred from `AS agg(...)` → family-of-one | open by default; B-anchor closes |
| `parser.py:483` | MEASURE, explicit `FAMILY { … }` member (b_anchor, order_by, description) | open by default; B-anchor closes |
| `parser.py:392` | DERIVED member from `FAMILY { r FERTILE { … } }`, `license=None` | **closed by default; the license opens travel** |

The first two are family-identity candidates. **The third is not.**

A derived member's fertility claim is adjudicated by comparing, on the attested data:

```
reduce-path      R(finer values of the formula)     e.g. mean of daily aov
recompute-path   the formula evaluated at the coarse anchor
```

CORROBORATED means the two agree — i.e. **the reduction is path-independent within one family**. That
is a runtime enactment of ToD v6 **Theorem 1 (family path independence)**, not the establishment of a
second identity. A derived member is therefore a **coherence certificate on a family edge**, and its
`License` is the *evidence* for it.

The already-recorded false-fertility finding reads correctly under this lens: `sum FERTILE { calendar }`
declared on the **ratio** `aov` was CONTRADICTED with a counterexample, because summing daily AOV is not
the month's AOV. The claim "this movement stays inside one family" was simply false.

> **Measure member → candidate distinct family identity.
> Derived member → a claim of family coherence, whose License is evidence, not identity.**

Two smaller nuances found in the same inventory:

- **Family-of-one containers coincide with their family.** `revenue`, `orders`, `visitors`,
  `med_amount`, `region_label` each declare exactly one reducer, so container and family denote the same
  identity. The rule still holds; the container merely has nothing to disambiguate. Only `level` is
  multi-family in the shipped fixtures.
- **`FamilyMember` mixes three ToD-distinct kinds of field**: identity-bearing (`agg`, `b_anchor`,
  `order_by`), claim (`declared_lineages`), and evidence (`license`) — plus `description`, which is
  prose and identity-bearing in neither theory nor code.

---

## 5. Canonical naming already satisfies ToD

ToD §3.2/§6.7 requires the canonical family name map to be injective within a namespace version, and
allows aliases only if they resolve unambiguously.

The shipped dotted name is already injective: `level.sum` and `level.last` are distinct names for
distinct identities. The bare `level` behaves as an **alias that resolves to no unique family**, and the
runtime already refuses to choose on the user's behalf (`planner.py:1193, 1256, 1282`).

That behaviour is architecturally correct. Only its *classification* is in question — see §6.

---

## 6. Candidate future contract corrections — RECORDED, NOT IMPLEMENTED

Neither of the following is authorized by this checkpoint. Frame-QL Manual behaviour is unchanged.

**C1 — bare name resolving to multiple governed family identities.**
When a bare runtime name resolves to multiple governed measure-family identities *and the user can
choose among them*, that condition is conceptually a **Clarify** under Analytical Governance §7 (the
adjudicator canonicalizes a uniquely determined request; it does not choose among unresolved analytical
meanings). Today it is raised as `Refusal("unknown", …)`, which `disclosure.py:67` classifies as
**ERROR — "vocabulary/capability failure — not an analytical verdict."**

**C2 — order-axis ambiguity.**
Where several *positively admitted* order axes exist and an explicit `by=` can settle the choice, that
is conceptually **Clarify** for the same reason. Today `Planner.plan_order_axis` raises
`Refusal("unknown", …)` for it.

**C2b — a genuinely absent lawful order axis is NOT automatically Clarify.** No user choice settles it,
so it is not the same condition as C2 and must not be folded into it.

Precedent exists in-tree: `ambiguous_grain` (`disclosure.py:173`) and `input_anchor_ambiguous`
(`disclosure.py:185`) are already `(CLARIFY, AMBIGUOUS)`. C1/C2 are the cases that never got classified that way. Any change here is a **public
reason-code contract change** and requires its own ruling.

---

## 7. Servability / certification taxonomy — distinction to preserve

P0.5a's reason codes and authority behaviour are **unchanged** by this note, and closed-by-default
stands: **no positive admission = no execution.**

Going forward, four things must remain separable:

```
1  governed analytical law / identity          (publication)
2  evidence that the current physical realization satisfies the law   (certification)
3  current material support / sufficient state (support)
4  runtime admission                            (PublishedScope)
```

`UNTESTABLE`, `CONTRADICTED`, undeclared law, missing material state, and stale evidence may carry
**different diagnostic meanings even though several ultimately close serving**. This checkpoint
deliberately does **not** force current certification findings into either "analytical establishment" or
"support insufficiency"; the public reason taxonomy is reconciled separately.

---

## 8. P0.5b implications

- **Certification identity must not be built on the runtime word `member`.** Licenses are keyed
  `f"{derived}.{member}"` (`adjudication._snapshot_licenses`). Per §4 a derived member is a *family edge
  claim*, so that key is naming a coherence edge, not a family. Whatever P0.5b freezes should name the
  subject in those terms.
- `EdgeKey(lineage, frm, to)` remains the right shape: logical identity, physical deliberately excluded.
- **Identity vs evidence must not be conflated.** `FamilyMember.license` already mixes them in one
  record (§4). P0.5b binds *evidence* (realization, data attestation, freshness, established_at) and
  should not absorb identity fields, nor vice versa.
- Known independent hazard, already reported and **not** part of this checkpoint: `table_version` is
  `count(*)` (`connector.py:88`), and both the certification attestation and the engine result cache gate
  on it.

## 9. P0.5c implications — a blast-wall finding, not merely field carriage

> **Face/crossing analytical law currently exists only in hand-authored Core `.cml`, while the shared
> authored Manifold cannot express it.**

The shared authored `relationship` carries only `{from, to, functionality, disposition}` with
descriptive prose; an exhaustive search finds no face authoring anywhere in manifold-agent or
columna-studio. Face law (`TOUCH` / `ASSIGN` / `ALLOC`, driver, order) lives only in
`parser.py:270-353`.

Since `.cml` is a **Core-private execution image**, this places genuine analytical law on the wrong side
of the authored-meaning / realization boundary — meaning is presently being *created* at the realization
layer, against *meaning must exist before realization; mapping realizes meaning, it does not create it.*

**P0.5c is therefore a semantic-authoring repair, not compiler field carriage.** The prior constraints
stand: do not copy Core `FACES` syntax wholesale into shared authoring; first identify the smallest
runtime-independent analytical crossing law (preserving the timeless `touch` vs data-dependent
`assign`/`alloc` distinction without depending on `columna_core.model.Face`); physical join facts remain
private mapping.

## 10. Platform terminology under v6

Earlier architecture material describes the future Platform using the retired v5 term, e.g. *"canonical
member identity"*, *"open member format"*. The v6 reading is:

> **canonical measure identity `F@A`** — governed family identity plus anchor — together with sufficient
> state, support/absence, provenance / freshness / certification, and governed cross-domain composition.

This is a terminology reconciliation only; Platform is not redesigned and remains paused. Its gate is
unchanged:

> **Can governed identity, state, and certificate authority survive crossing an execution boundary?**

---

## 11. What this checkpoint deliberately does NOT authorize

- **No renaming.** `MeasureColumn`, `FamilyMember`, `family`, `member` all stay exactly as they are.
- **No Frame-QL grammar change.** `family.member` dotted syntax is untouched.
- **No public reason-code change.** C1/C2 are recorded as candidates only.
- **No change to P0.5a authority behaviour, admission, or refusal ladder.**
- **No wire/contract-version change.**
- **No blanket type equation** `FamilyMember == MeasureFamily`.
- **No V/M/B promotion** to foundational ToD anchor kinds.
- **No P0.5b or P0.5c implementation.**
- **No Platform work.**
- **Not** the data-identity / cache-safety correction (`table_version`), which remains the separately
  intended next code unit.
