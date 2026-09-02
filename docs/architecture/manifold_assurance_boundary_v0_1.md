# The Manifold-assurance boundary

**Version:** 0.1
**Date:** 2 September 2026
**Status:** RULED (Huayin, 2026-09-02). Recorded as stated; nothing is designed or implemented here.
**Related:** `consolidated_ledger_v0_1.md` (P1-18, P1-31), `topology_core_platform_delivery_v0_1.md`

---

## 0. Why this record exists

Two different problem domains had begun to bleed into each other, and P1-18 made the bleed visible:
a Manifold-authoring defect (two authoritative representations disagreeing) was found *through* a
query result, and the tempting repairs all ran downstream of where the defect actually lived. This
document records the separation. It is a doctrine record, not a work item: no mechanism is proposed,
no row is opened, no code is changed by it.

## 1. The ruling

> **From now on, separate Manifold assurance from analytics over an assured Manifold.**
>
> Manifold assurance owns authoring, declaration validity, parity, attestation, contradiction,
> certification, and what happens when those fail.
>
> Frame-QL / Measure Algebra / Core / Platform reasoning owns what can be derived, adjudicated, and
> realized **once the required Manifold standing exists**.
>
> Do not use downstream analytical execution to compensate for an incorrect Manifold, and do not let
> physical execution redefine Manifold declarations.
>
> — Huayin, 2026-09-02

## 2. The lifecycle and the boundary

```text
Author / construct Manifold
        ↓
Validate declarations
        ↓
Attest claims against governed evidence
        ↓
Manifold obtains standing
        ═══════════════════════  boundary
        ↓
Interpret analytical request
        ↓
Derive / adjudicate under the Manifold
        ↓
Realize in Core / Platform / backend
```

**Above the boundary the question is:** can we trust this Manifold as the governed description we
are going to reason from?

**Below it:** assuming that governed description, what follows from it and what can we realize?

### 2.1 Above — Manifold correctness / assurance

How a Manifold is authored correctly; whether a declaration is well formed; whether `TYPE String`
names a valid logical type; whether a declared hierarchy actually holds in the data; whether a
declared face satisfies its claimed relationship; whether two representations of the same Manifold
agree; whether a declared logical type contradicts what the current realization can support; how
drift between `.cml`, generated declarations, code-built fixtures and attested data is detected; and
what happens when a declaration is wrong.

Its output is **a Manifold whose declarations have the required standing to be used**. This happens
*before* anyone asks what analytics are possible under it.

### 2.2 Below — derivability, admissibility, realization

Whether a requested measure is derivable; which anchors are lawful; whether candidate readings are
equivalent; whether a reduction is blocked; whether an operator satisfies the family law; whether a
measure can travel across a relationship; whether a query is ambiguous; whether it Serves, Discloses,
Clarifies or Refuses; what Core can realize; what Platform can realize of the same canonical meaning;
what state can be reused or composed; what a particular backend can execute.

These take the declarations as **governed premises**. They are not responsible for deciding whether
the declaration was good in the first place.

## 3. Error handling belongs to assurance

What to do when an error is found is part of Manifold assurance, not an afterthought below the line.
A Manifold error has different consequences by kind:

| kind | consequence |
|---|---|
| syntactically / structurally invalid | cannot become a Manifold |
| declaration contradicted by evidence | cannot obtain or retain the relevant certification |
| two authoritative representations disagree | parity failure — repair the declarations |
| attested data changes and invalidates a certified claim | withdraw / recompute standing |
| the author omitted something | per the law, remain **undeclared** rather than silently inventing a declaration |

The remedy is generally **repair, or withdraw standing** — never "make the query engine accommodate
the mistake."

## 4. The two questions this separates

> **Was the declaration wrong?**  (above the boundary)
>
> **Did execution fail to honor a correct declaration?**  (below it)

Those need different remedies, and conflating them is what produces a second Manifold validator
inside the query path.

## 5. How the current rows classify

**P1-18 — ABOVE the boundary.** The `.cml` and the code twin disagreed about the Manifold, and the
parity check failed to detect the disagreement. A Manifold assurance defect, repaired where it lived:
the parity guard now measures the governed declaration surface (A), and the lost declarations were
restored from the authoritative code twin (B). D — rejecting an unknown `TYPE` token at the
logical-type vocabulary boundary — is assurance too: a declaration that does not name a governed
logical type is not a well-formed declaration.

This classification is also why `buyers` and `unique_visitors` were left untouched: with no
authoritative twin declaration, changing them from physical evidence would be exactly the prohibited
direction — physical execution redefining a Manifold declaration.

**P1-31 — BELOW the boundary.** Once a Manifold has standing, a realization can still fail to honor
it and manufacture a misleading NULL that then enters ordinary absence semantics. That is not a
declaration defect; it is realization falsifying the governed meaning it received. Its control case
(a legitimate numeric-as-text declaration whose `TRY_CAST` at delivery is the declared behaviour)
stays with it, and it remains parked.

**Corollary, applied.** We should be reluctant to compensate above-the-boundary defects with
below-the-boundary cleverness — teaching query execution to notice that a Manifold was probably
authored incorrectly turns downstream analytics into a second Manifold validator.

## 6. Standing consequence

Some things currently called "adjudication" may on inspection belong to Manifold
publication/assurance, with query adjudication a separate later act. **That reconciliation is not
performed here**, and this record authorizes no work. It fixes the vocabulary and the boundary so
that the next mission can be chosen deliberately rather than inherited from whatever the last repair
uncovered.
