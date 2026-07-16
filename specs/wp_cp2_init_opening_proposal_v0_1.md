# CP-2 opening — `columna init` + the eval suite: PROPOSED for ratification (v0.1)
**From: Claude Code, 2026-07-16. For: Huayin's ratification (CP-2 rhythm — propose, ratify, then build).**
**Foundation: capture §5 (the frame, the harness thesis, the two-ends principle, the alternating
handshake, the polarity principle) + brief Track 2/3 + the CP-0 rulings. Nothing here is built; this
is the first CP-2 artifact for your ratification.**

CP-2's ratification artifacts arrive in sequence — **(1) this eval benchmark schema list**, then
**(2) the knowledge-package draft** (before any prompt is live), then **(3) init's loop hermetic
against the scripted provider** (before a real model enters). This doc is (1) plus the init-slice
design frame it presupposes.

## 1 · The init slice — design frame (for orientation; details land with the build proposals)
Per capture §5 and the CP-0 rulings, `columna init` is Authoring's **database-context slice** — one
context, the same artifact state machine, two outputs (the manifold + the Map, fused v1). The world
we build (mind rented): the **draft artifact** (schema in CORE — the polarity wall the kernel rejects,
per your Q3), the **tools** (catalog reader + metered sampler through the connector's typed aperture,
the adjudicator — reused unchanged), the **laws** (state machine `scoped→proposed→declared→attested→
published`, publish-as-author's-act, the polarity principle), and the **knowledge** (the prompt +
skills, artifact (2)). The loop is A4: generate → review → revise, publish an author's act; an agent
is a first-class caller; every agent turn sandwiched between human acts.

## 2 · The eval suite — what it measures (the harness thesis's measurement device)
Golden authoring benchmarks are the **ratchet**: deliberately messy schemas with **adjudicated ground
truth**, scoring init's judgment on exactly the **oracle-asymmetric** calls the harness thesis names —
**basis type** (the sharp case), **universe assignment**, **M-leaks** — plus the **polarity law** (init
proposes closures freely and openings NEVER) and the mechanical inferences (FK→edge, numeric→measure,
stock→bar). Each benchmark is `(messy schema + data sample) → the graded proposals init SHOULD emit`.
A benchmark scores per-declaration: did init propose the right closure, grade it correctly, and make
the oracle-asymmetric call **explicit** rather than silent?

## 3 · PROPOSED benchmark schema list (v1 — for your ratification)
Ten schemas, each named with its **trap** and the **adjudicated ground truth** (what init must do).
Marked ◆ = oracle-asymmetric (the load-bearing human calls); ○ = mechanical (gradeable exactly).

| # | Schema (the trap) | Adjudicated ground truth — init MUST… |
|---|---|---|
| B1 ◆ | **Events vs spine ambiguity.** A `daily_inventory` table (one row per store×day) AND an `orders` table (one row per order). | propose `events` basis for orders' universe, `spine` for inventory's; make the call **explicit** in the review checklist (the sharp case — a false events claim is unrefutable). |
| B2 ◆ | **Stock measure hiding as additive.** `inventory_level` column that looks summable. | propose the measure with `sum BLOCKED {calendar}` (the bar) — **over-barring is the safe error**; surface `last` as the period-end reader. Never propose a fertility opening. |
| B3 ◆ | **Universe assignment fork.** A `returns` table joinable to both `transactions` and `stores`. | propose ONE universe with a reasoned assignment, flag it as an oracle-asymmetric review call (not silent). |
| B4 ◆ | **M-leak.** A measure whose grain leaks beyond its key (an `avg_basket` pre-aggregated in a rollup table). | propose the `M_ANCHOR` leak declaration explicitly; flag for review. |
| B5 ○ | **FK → functional edge.** A clean `store.region_id → region.id` FK. | infer the `store → region` edge (grade INFERRED_CATALOG), VIA the FK. |
| B6 ○ | **Observed FD, no FK.** `day → month` derivable from data but no declared key. | propose the edge at INFERRED_SAMPLE grade (data suggested, not catalog-granted); mark for author confirmation. |
| B7 ○ | **Calendar detection.** A date column with daily cadence. | propose calendar levels/edges (day→week→month→…) as a HIERARCHY; the FD test is the adjudicator's, not init's claim. |
| B8 ◆ | **The polarity trap (adversarial).** A schema where a fertility opening is *tempting* (a measure that looks reducible along a lineage). | propose the closure/bar; surface theorem-provable fertility ONLY as the **adjudicator's advice** ("provably fertile; declare if you mean it") — NEVER as an inferred opening. The draft format must make an inferred opening **unexpressible** (well-formedness). |
| B9 ○ | **Numeric → measure, categorical → not.** Mixed columns. | propose additive measures from numerics; propose categoricals as dimensions/attributes, never as `sum`-able. |
| B10 ◆ | **Registry vs product basis.** A `product_catalog` (registry) and a `store×day` spine with a `budget` product table. | propose `registry` for the catalog universe, `product` for the budget; flag the basis calls. |

**Scoring proposal:** each benchmark yields a per-declaration diff (init's proposal vs ground truth),
scored on: closure-correctness (did it bar/assign/leak right?), grade-correctness (INFERRED_CATALOG
vs INFERRED_SAMPLE), and **explicitness** on the ◆ calls (a silent oracle-asymmetric call fails even
if the value is right — the whole point is to summon the short human review). Aggregate = the ratchet
metric across versions.

## 4 · What I need from you (CP-2 checkpoint)
1. **Ratify / revise the benchmark list** — add/cut schemas, adjust the ground truth, retune the ◆/○
   split. Bring it to the shape you want *before* any benchmark is built.
2. **Confirm the scoring axes** (closure · grade · explicitness) and that explicitness-failure on a ◆
   call is a hard fail.
3. Then I bring **(2) the knowledge-package draft** for ratification, then **(3) init's hermetic loop**
   against the scripted provider — each proposed before it goes live, per the CP-2 rhythm.

No code until the list is ratified. Fresh branch `wp-cp2-init` (off CP-1 HEAD; rebases onto `main` once
#35 merges at your gate).
