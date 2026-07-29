# Open Planner — Artifact A1: the extracted Plan IR + the Cascadia attack set (v0.3)

*Desk artifact, 2026-07-27, v0.2. ERRATA (F3, found by the execution beat):
v0.1's Part 2 misdescribed the shipped model from desk recall — inventory is
`store * day` (no product axis); the measure is `stock`, not `stock_units`;
revenue is `FROM transactions`, not `FROM sales`. Three wrong facts, one
broken exhibit; the published deposit is unaffected (generic wording,
verified). Corrections below; the broken Attack A is RECLASSIFIED as the
out-of-domain lawfulness exhibit. Written-from-recall is the cause; write
from the artifact. F3b (v0.3): the v0.2 errata itself carried one more
recall-fact — the measure is `units_sold`, not `units` — caught by the
beat at execution. The errata containing its own instance of the disease
it documents is the strongest argument yet for the rule. Delivered under the artifact gate. Method:
extraction from the shipped `columna-core` 0.13.x source (file:line pinned),
not invention. CC's verification beat is specced in Part 3; claims marked
[EXEC] await execution, per the reassignment (desk constructs, CC verifies).*

---

## Part 1 · The Plan IR, extracted from the planner's internals

### 1.0 The finding first: there is no plan object today — and there are two implicit planners

The shipped system has no reified plan. What exists (`planner.py`):
`FrameResult` holds per-column `ColumnResult(name, expr, frame, disclosure,
…)` plus rendered transport strings for the human tree (`planner.py:87–93`);
the anchor is an argument (`plan(anchor, columns, where, population)`,
`planner.py:828`); and — the discovery — **the transports are computed
twice**: the planner derives the edges a column's transport crosses *for the
certificate/disclosure side* (`planner.py:604`), and the docstring at
`planner.py:689` states it outright: the projection's edges are *"the
planner's remit; **the engine mirrors this** for the actual transport."* Two
independent derivations of the same semantic fact, agreeing **by co-design,
certified by nothing**. That is a lawfulness/faithfulness seam already
shipping — benign today because both sides are one codebase, but exactly the
class of implicit agreement the kernel exists to make explicit. **The Open
Planner is therefore not adding a checker to a clean system; reifying the
Plan IR closes an existing uncertified dual-computation seam.** (This also
answers P-REWRITE's "is this new risk?" — no: the seam predates us.)

### 1.1 The node inventory (each pinned to the code that implies it)

| # | IR node | extracted from |
|---|---|---|
| 1 | `ANCHOR(coords…)` — the frame's output grain | `plan(anchor: tuple, …)` planner.py:828 |
| 2 | `CARVE(universe, predicate?)` — population selection | `where`/`population` args planner.py:828; universe predicates engine-resolved |
| 3 | `COLUMN(name, measure_ref, family_op)` — one asked series | `ColumnResult` planner.py:40; `E.Series(expr, alias)` planner.py:435 |
| 4 | `TRANSPORT(frm → to, lineage)` — functional climb along a corroborated hierarchy edge | blocked-edge check planner.py:105–131; edge derivation planner.py:604, 628 |
| 5 | `CROSS(relate, face)` — lawful M:N passage spending a declared face | B_ANCHOR_CROSSING caveats planner.py:792–808 |
| 6 | `REDUCE(family_op @ coordinate)` — collapse to the anchor under family law | the classify-collapse path planner.py:296 (incl. its recorded doctrine-gap) |
| 7 | `ALIGN(shared_anchor)` — full-outer juxtaposition of columns on the shared anchor | planner.py:318–323 (locally scoped null semantics) |
| 8 | `DERIVE(expr over columns)` — arithmetic over aligned series | `E.sub` usage; derived planning paths planner.py:265–301 |

Anchor-spend accounting (M_ANCHOR licensing) rides nodes 5–6 as an
obligation, not a node: the certificate must track spends, the IR needn't
represent them as steps. Eight node types; nothing in the served grammar
appears to require a ninth [EXEC: CC replays the full battery through an
IR-emitting shim to confirm closure — P-IR's first test].

### 1.2 Two structural observations for the kernel design

- **The IR is a DAG per column joined at ALIGN**, not a tree: columns share
  CARVE and ANCHOR, diverge through TRANSPORT/CROSS/REDUCE, and rejoin at
  ALIGN/DERIVE. Canonical serialization (P-EQUIV) should serialize the DAG
  with columns sorted by name and coordinates in declared-lattice order.
- **Disclosure is a projection of the plan, not an addition**: every caveat
  the planner emits today (crossing skews, discarded memberships, alignment
  nulls) corresponds 1:1 to an IR node with a declared consequence — which
  means the certificate can GENERATE the disclosure, unifying "what the
  kernel proved" with "what the answer admits." One artifact, two readers.

## Part 2 · The Cascadia attack set (Classes A/B/C, against the real model)

The model, as shipped (v0.2, verified against `manifold.cml` AND runtime by
the beat): universes `transaction` (customer·store·product·day), `inventory`
(`store * day` — NO product axis), `category_profile`; `revenue FROM
transactions AS sum(amount)` on transaction; `stock` on inventory; the
product↔category crossing with faces `touch` / `primary` (ASSIGN BY
priority) / `split` (ALLOC BY alloc_weight); `location: store → region`.

**Attack A v2 — lawful substitution (establishes lawfulness ⊅
faithfulness).** ASK: `revenue.sum @ category` (face: split). PLAN:
CARVE(transaction) · COLUMN(**units_sold**, sum) · CROSS(product↔category,
split) · REDUCE(@ category) — identical to the faithful plan in every node
but one field: the measure reference. Both asks are servable from the ask
surface; the attack is serving plan-for-ask-2 against ask-1. Kernel
obligation exposed: bind `COLUMN.measure_ref` to the ask's measure atom —
one rule, which is the point. **The v0.1 exhibit, reclassified — the
OUT-OF-DOMAIN refusal**: v0.1's plan (CARVE(inventory) · stock · CROSS to
category) does not compose — inventory has no product axis, and the engine
refuses `stock.sum AT {category}` as *"not addressable in universe
'inventory' (out of domain — undefined, not missing)"*. That is obligation
A catching a category error before faithfulness is even reached: kept as
the lawfulness-refusal exhibit, not an attack.

**Attack B — semantically adjacent (the input-grain attack; the Two Anchors
subject, weaponized).** ASK: `revenue.mean @ cal.month`. FAITHFUL PLAN:
REDUCE(mean @ cal.month) over transaction atoms — the family's mean over the
input grain, the FrameQL denotation. UNFAITHFUL PLAN: TRANSPORT(day →
cal.month) · REDUCE(sum @ store·product·month) · then REDUCE(mean @
cal.month) — a mean of monthly-store-product *sums*: every node lawful
(sum is the extensive family's transport; mean is a legal reducer), the
composition denotes a different statistic. This is the attack class the
kernel's obligation language must be *structural* to catch: the faithfulness
rule is that REDUCE's input grain must be the denotation's input grain —
intermediate collapses are unfaithful unless the ask's semantics licenses
them. [EXEC: CC computes both against the demo warehouse; the numbers must
differ, making the attack concrete with a printed delta.]

**Attack C — observationally equivalent trap (why output-testing can never
certify).** Construction requires a data-coincidence, and the honest note is
that a *natural* one in Cascadia must be found or minted: the candidate is a
carve to single-membership products, where `touch` and `primary` plans
coincide — but there they coincide *semantically*, which makes it
equivalence, not an attack. The attack needs coincidence **by data, not by
meaning**: [EXEC] CC's beat either (a) audits the demo warehouse for a
dimension pair that happens to induce identical groupings this seed (e.g., a
region whose stores coincide with a promo flag), or (b) mints a fixture
where `alloc_weight` values make the `split` plan numerically equal the
`primary` plan on the current data while denoting a different question — then
the exhibit is: two plans, identical outputs, different denotations, and only
plan ⊨ ask separates them. Class C's deliverable is that printed pair.

## Part 3 · CC's verification beat (the execution half of the reassignment)

1. **IR closure** [P-IR]: an IR-emitting shim on the planner; replay the
   111-ask battery; assert every served ask emits only nodes 1–8; any ninth
   node type is a finding, not a failure.
2. **Attack B executed**: both plans computed on the demo warehouse; print
   the delta; freeze both IR documents as fixtures.
3. **Attack C constructed**: per Part 2(C); freeze the pair.
4. **The dual-computation seam**: write the test that asserts
   planner-derived edges ≡ engine-mirrored transports on the full battery —
   the seam's first certificate, and the kernel's first real obligation
   discharged against the shipped system.
5. All four land as fixtures under `specs/open_planner/` with a dated
   README, per commit-on-creation.

*Status after this artifact: desk's owed items — IR strawman DELIVERED
(extraction-grounded, closure pending [EXEC]); attack set DELIVERED (A
complete, B constructed pending execution, C specced with two construction
routes). External searcher's owed item: the prior-art sweep, citations.
The artifact gate holds.*
