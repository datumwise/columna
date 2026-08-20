# ADR-036: Generated-family law — generation creates identity, not permission

**Status:** Ratified (Huayin, 2026-08-20; drafted by the design session from Huayin's rulings of 2026-08-19 and 2026-08-20)
**Date:** August 2026
**Track:** Architecture / analytical governance. Supersedes ADR-020's inform-and-serve rule **for structurally prohibited reductions only**. Clarifies ADR-031 D5; does not reverse it.

---

## Context

Columna's constitutional claim is that a governed manifold cannot be talked into producing a number
its declarations forbid. A census run on 2026-08-20 against the shipped 0.15.0 tree found that it
could — not through a hole in the enforcement, but through a hole in what the enforcement was *about*.

The old law walk (`_atoms` → `_crossings`) modelled an expression's applicability law as the law of
its **leaf members**. Every reducer *generated above* a leaf was therefore invisible to it. Measured,
on the Cascadia demo manifold:

```
SELECT stock.sum          AT {store*cal.month}   →  disclose, blocked_reduction   179656.0
SELECT sum(stock.last@day) AT {store*cal.month}  →  serve, CLEAN                  179656.0
```

The identical meaningless number, one syntax away from its own prohibition, with the caveat gone. The
leaf `stock.last` is lawful; the `sum` above it is the thing without authority, and nothing looked at
it. The same bypass was available through unary minus, binary arithmetic, scalar multiplication,
scans, DERIVED columns and the default-member rule — nine spellings of one defect, because in each of
them the leaf stays lawful while the generated reducer does the prohibited travel.

Two further findings framed the ruling. First, ADR-031 D5's own text already said `level.sum @ month`
"is refused"; the shipped behaviour had diverged from the ADR that authorised it, and the divergence
was load-bearing enough to have its own standing instruction elsewhere in the tree. Second, the
inline average had **no law address at all**: `avg`/`mean` was recognised by a hardcoded planner table
and by nothing in the operator registry, so `mean BLOCKED { <lineage> }` was unparseable — the most
common generating reducer was ungovernable by construction.

## D1 — Generation creates identity, not permission (RULED)

> **Family generation creates a new analytical family. It does not create a new operator permission.**
>
> A successor family preserves the applicability law of its governed ancestry unless the
> family-changing operation positively establishes a different successor law.

The default is law preservation. A law change requires governed semantics. This is stated per
**operator × lineage** and does not revive stock/flow/rating as a global type.

## D2 — The law is about the OPERATION, not the leaf (RULED)

For an inline generating reducer `R(inner @ pin)`, adjudicate the applicability of `R` across the
lineages it will traverse, using the **governed ancestry** of `inner`:

```
L(R) ∩ BLOCKED_R ≠ ∅   →   Refuse
```

`R` is **not** required to be the leaf member the expression names, and `on_hand.last` is **not**
collapsed back into the identity of bare `on_hand`. `last` remains its own resolved family; the
question asked is whether a SUM over `on_hand` is permitted along the lineages this reduction crosses.

This makes L1–L5 one implementation rather than five: the check is on `R` against the ancestry, so it
is indifferent to whether the member was written, defaulted, or is the family's only entry, and it
reaches through every carrier because `_atoms` already reaches through them to the ancestry.

The direct (written) case keeps its pre-existing monoid gate — a holistic reducer recomputes from base
and never combines across the axis, so the B-anchor is moot for it. A **generated** reducer is
deliberately not gated that way: it genuinely collapses the resolved series across the axis, which is
the whole operation. That distinction is what gives `mean` a real law address rather than a decorative
one.

## D3 — Disclose cannot legalise (RULED; supersedes ADR-020 for this case)

> **Structurally prohibited analytical operations Refuse. Disclose exists inside the lawful region;
> it cannot legalize an operation the governed law does not possess.**

ADR-020's historical text stands and is not rewritten. Its inform-and-serve doctrine remains correct
for analytical *risk* attached to a lawful result. It was wrong for the B-anchor crossing, and the
mechanism of the wrongness is now visible: a caveat attached to a number that should never have been
produced is what let the same meaningless total keep being served, one wrapper at a time.

The caveat category `b_anchor_crossing` is **tombstoned as a producer** and retained, still wired, so
archived wires, recorded transcripts and the deposited manuals still resolve. Vocabularies grow by
rule and shrink by tombstone, never silently.

## D4 — Two polarities, never flattened (RULED)

There are two authored law forms and they have opposite defaults. A consumer must know which it reads.

| | measure B-anchor | derived FERTILE |
|---|---|---|
| default | **open** | **closed** |
| declaration | `BLOCKED { lineage }` *closes* | `FERTILE { lineage }` *establishes* |
| absence means | no prohibition | no permission |

They are never merged into one accidental default. Only the NEGATIVE polarity is enforced by this
unit: `MeasureShape.blocked` carries it, and the planner reads it. The POSITIVE polarity is
**deferred whole** (D9) — no widened projection is left behind either, so the shape never carries half
a semantics.

## D5 — Clarify is not reachable before lawfulness (RULED)

For an unpinned generated reduction, let `C` be the governed candidate interpretations and `L ⊆ C`
those for which the requested operation is lawful:

```
|L| = 0  →  Refuse      |L| = 1  →  proceed (defaulted, MATERIAL input_anchor caveat)      |L| > 1  →  Clarify over L
```

Never offer a candidate that is already structurally illegal. A clarify is a menu of readings the
asker may choose between; an unlawful reading is not a choice, and offering it is how a reader gets
talked into a laundered answer one keystroke later.

## D9 — FERTILE does not carry successor travel; the boundary is deferred (RULED)

A draft of this correction had the planner read `FERTILE { .. }` as the successor family's travel
permission. Running it proved the reading is unavailable: `FERTILE` is an **equality theorem about
the reduce-path** — "reducing from cached finer values equals recomputing from base" — adjudicated
against attested data by `adjudication._prove_data`. An AT-metric's travel is the opposite of that by
construction, so `mean FERTILE { calendar }` on `daily_aov` is a false claim and publish fails closed
(measured: reduce 131.063… vs recompute 129.787… @ `cal.week=2024-W01`), while `FERTILE { }` would
forbid the metric's own declared meaning and reverse ruling 5. No declaration an author could write
would permit the travel.

The ruling: three boundaries, not one.

> **family law ≠ certification evidence ≠ runtime admission.**

`FERTILE`/`License` currently sits on the second. Using it as the third is not a shortcut but a
category error, and it is not solved by treating the current License as family identity or family
law. Deferred to a dedicated reconciliation (**DG-3**) and deferred WHOLE — no inert projection, no
unreachable branch, no half-registered reason left behind as scaffolding.

## D10 — Map composition preserves by union, and that gap is recorded (RULED)

An anchor-preserving MAP establishes no new reduction permission, so a map-composed successor
preserves the **union** of its operands' restrictions. This may be over-strict — a ratio of two
non-reconciling quantities can be perfectly reconciling — and it is accepted on the asymmetry that it
may withhold a lawful continuation but can never manufacture an unlawful one. Recorded explicitly,
per the ruling:

> **No general mechanism yet positively establishes a different successor law for an ad-hoc
> map-composed family.**

The broader law-synthesis problem is **not** solved here (**DG-6**). Where an author needs a
positively established successor law today, the governed mechanism is an explicitly declared
DERIVED/FAMILY path.

## D6 — ADR-031 D5 is clarified, not reversed (RULED)

> **Operator applicability remains per operator × lineage. Those constraints remain governed across
> family-generating transitions; generation alone does not grant a new permission.**

No stock/flow/rating type. Summing a stock across **stores** stays lawful, because the bar names
`calendar`, not the measure. `avg`, `min`, `max` and `count` over a stock across time stay lawful,
because the author barred `sum` and barred nothing else — that is a declaration, not an oversight the
engine repairs. A correction that also swept those up would be the type system D5 forbids, arriving
by the back door.

## D7 — One canonical operator identity (RULED)

`mean` joins the operator registry so that `(operator × lineage)` law has an address for the inline
average. `avg` is an **alias**, not a second operator: one law subject, so there is exactly one thing
an author would declare. Registering it must not imply that displayed averages combine associatively —
`is_monoid=False`, witness holistic, and the shipped inline-average arithmetic is untouched. The
registry entry gives the operator a governed law address, not a new arithmetic definition.
`SERIES_REDUCERS` binds the executable and governable reducer vocabularies together, asserted by test,
because their drift is precisely how `mean` came to have no law slot.

## D8 — The internal reason registry is closed and fails closed (RULED)

The public wire is unchanged: `CONTRACT_VERSION` stays `"3"` and `no_result.reason` remains an
extensible reason string in shape, so `blocked_reduction` appears on the Refuse channel additively.

Internally, `outcome_for` no longer defaults an unregistered reason to ERROR. That silent default was
not hypothetical: `chained_crossing` and `anchor_spent` both shipped through it for months, classified
ERROR when their call sites plainly mean REFUSE. Both are now registered to their existing intent
(REFUSE/UNSUPPORTED). A vocabulary that grows by rule and shrinks by tombstone cannot also grow by
accident.

## Consequences

- The laundering class closes in every spelling, certified against a real Afternoon fixture that did
  not previously exist in the repository (`tests/fixtures/afternoon.cml` + `afternoon_world.py`). The
  Afternoon's wrong number is unreachable by construction, asserted as a number and not only as a mood.
- **DG-2 closes.** `level.sum @ cal.month` refuses rather than erroring; the everything-classifies
  backstop remains a backstop and this case no longer reaches it.
- The four-mood exhibit's Disclose witness moves from a prohibited reduction to `buyers AT {cal.month}`
  — a lawful ask with an approximate realization. The moods now read cleanly: **Serve** lawful, no
  material condition · **Disclose** lawful, condition travels · **Clarify** several lawful meanings
  remain · **Refuse** no lawful path exists.
- The homepage's four cases are re-cut so the moods are distinguished by **lawfulness**: Serve (lawful,
  no material condition) · Disclose (lawful, a material condition travels) · Clarify (two or more
  lawful interpretations remain) · Refuse (structurally unlawful). The Refuse witness moves from the
  out-of-universe ask to the blocked temporal stock sum — the harder and more useful lesson, that a
  perfectly computable number can still be one the governed law does not grant. The out-of-universe
  case stays in the corpus and the tests.
- **Left open, on the record:** **DG-3** (FERTILE — deferred whole, D9), **DG-4** (open-by-default
  families make silence permission, so an *under-declared* measure still admits a generated reducer),
  **DG-5** (generated families have no canonical runtime identity object; the correction uses a
  deterministic law projection instead, which satisfies the ruling's four conditions without
  materialising one), **DG-6** (no mechanism positively establishes a map-composed successor law, D10).
