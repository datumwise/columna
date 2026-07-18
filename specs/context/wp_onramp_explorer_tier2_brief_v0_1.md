# WP — On-ramp + Explorer tier 2, ONE MOTION (v0.1)
**From: Huayin (drafted by the design session, 2026-07-15). For: Claude Code.**
**Foundation: `specs/context/design_capture_onramp_explorer_v0_1.md` — COMPLETE and
ratified; every fork in its §7 is RULED; read the whole capture before CP-0, especially
§2a–§2c (formal semantics + grammar), §3 (the Map doctrine), §5 (the frame, the harness
thesis, the two-ends principle, the polarity principle), §6 (Explorer scope as amended —
ALIAS is CUT per §7 C1), and §7 (the rulings this brief transcribes). This brief adds
mechanics only; where brief and capture could ever disagree, the capture wins and the
disagreement is a checkpoint event.**

## Why one motion (standing ruling)
The Explorer displays what the Manifold declares; the on-ramp is what gets Manifolds
declared. Surface and supply ship together.

## The four tracks

### Track 1 — Certificate customers (B): ASSERT, HIERARCHY verification, UNIVERSE BASIS
- **Kernel reuse is a hard constraint:** `License` and the adjudication path are reused
  UNCHANGED; any schema change is a named checkpoint fork, never a silent extension
  (ADR-034 consequence — this is the kernel's generality test).
- **ASSERT** (capture §7 B1): row-level predicates on a universe + aggregate invariants
  at an anchor. Data channel only; UNTESTABLE stands asserted-and-disclosed;
  CONTRADICTED fails publish closed. **Violation on re-attestation is an authoring
  event that EDITS THE PUBLISHED SCOPE**: cut at declaration granularity (the measures
  the expression reads + their derived cone); queries into the cut refuse; everything
  else serves untouched. The refusal's wire vocabulary: CHECK THE TABLES — the reserved
  `conflicting_data` slot is the expected fit; report the finding, Huayin confirms
  (S1a discipline; no minting). Region cuts (coordinate-scoped) are the designed
  refinement, NOT in scope — but the adjudicator records counterexample coordinates now
  so the refinement inherits its data.
- **HIERARCHY verification** (§7 B2): chains desugar to EDGEs (existing); the new
  content is the functional-dependence test → verdict; CONTRADICTED fails publish.
- **UNIVERSE BASIS** (§7 B3 — absence-semantics is LAW): events → absence is ZERO
  (lawful zero-fill); spine → absence is a GAP (`incomplete_data` material caveat;
  window edges inherit); product → absence always a gap; registry → membership
  checkable, unknown entities refute. Wire the engine to the law. Adjudication per
  type: spine gaps refute; registry corroborates against source.
- **The scope-edit law governs all three:** adjudication events edit the published
  scope; serving never outruns the verdicts. Licenses degrade to recompute; asserts
  degrade to cut.

### Track 2 — `columna init` (the on-ramp; A rulings)
- **A1:** reads catalog + scoping, attempts sampled data; proposals carry the grade
  their evidence earns (INFERRED_CATALOG vs INFERRED_SAMPLE). Output is a DRAFT.
- **A3:** the draft CANNOT publish. Publish is an explicit act, and per **A4** it is an
  author's act inside an iterate loop (generate → review → revise). An agent is a
  first-class caller of the loop; the publish act is never the agent's.
- **A5 — the polarity principle, enforced as ARTIFACT well-formedness, not prompt:**
  data may suggest walls, never doors. The draft format has NO legal way to express an
  inferred opening — a FERTILE clause without an author-declaration mark is a
  well-formedness error the kernel rejects. Init proposes closures freely and
  aggressively (B-anchor bars on stock-smelling measures — over-barring is the safe
  error; RELATE; universe predicates; descriptions) and proposes openings NEVER.
  Theorem-provable fertility surfaces as the ADJUDICATOR'S ADVICE inside the loop
  ("these members are provably fertile; declare them if you mean them") — acceptance is
  the declaration.
- **The review checklist:** publish requires per-declaration review marks; the
  checklist's first line per measure is additivity; the checklist CONCENTRATES on the
  oracle-asymmetric calls (basis type — the sharp case; universe assignment; M-leaks).
  Short, differentiated review is the automation-bias defense.
- **Two outputs** (capture §1): the manifold and the Map. v1: today's fused `.cml` (the
  Map's v0 form is the inline binding); the artifact split is the Authoring-era WP's.
- **The aperture (two-ends principle):** init touches data ONLY through the connector's
  typed calls + catalog — general SQL is structurally uncomposable. Metered sampling;
  profile-stats-first where they suffice. (The sampling-policy/masking knob is ledgered
  for the enterprise era — do not build it now; do not foreclose it.)

### Track 3 — The knowledge package + the eval suite (the frame's two new deliverables)
- **Knowledge package:** the authoring agent's system prompt and skill documents are
  DOCTRINE under the copy law — versioned, PROPOSED for Huayin's ratification, edited
  only by ruling. Sourced from the manuals, the captures, and describe. A prompt edit
  is a ruling, not a tweak.
- **Eval suite:** golden authoring benchmarks — deliberately messy schemas with
  adjudicated ground truth (does the draft find the stock measure and propose the bar?
  grade the FK-inferred edge correctly? make the basis call explicit rather than
  silent?). This is the measurement device for the harness thesis; treat its design as
  a first-class deliverable, not test scaffolding. Bring the benchmark schema list to
  CP-2 for Huayin's review.

### Track 4 — Explorer tier 2 (§6 as amended)
- **Data path:** extend the existing build-time capture pipeline (`gen_transcript.py`
  precedent) — the Explorer remains structurally incapable of showing a manifold the
  shipped package didn't describe. **Wire-strings coverage check** ships as a
  build-time assertion: every shipped reason/code has a friendly string
  (`input_anchor_ambiguous` is the known gap; whatever Track 1 adds joins the check).
- **Scope IN:** (a) licenses + verdicts on derived members — VERIFIED (timeless) ·
  CORROBORATED (watermark shown) · UNTESTABLE (asserted, says so); (b) fertility made
  visible per member per lineage — askability vs travel, extending the shipped
  legal-cone display; (c) STRUCK — ALIAS cut; (d) resolution anchors on `AT` metrics;
  (e) the Operator Registry panel (kind, monoid, linear — the adjudicator's own facts);
  (f) **declare `sell_through_rate` properly** in the demo manifold as a DERIVED with
  its family and its declaration-time population (§2c — the pin lives in definitions),
  retiring tier 1's provenance-labeled workaround and putting a live verdict badge on
  the demo's own metric; (g) published-scope vs cut-region display (B1 consequence).
- **Posture (RULED): working-user-first.** The Explorer is a COMPONENT of the product;
  the site's `/explorer` is its demo-manifold instance. Hard design constraint: the
  component binds to any describe artifact — zero site-specific coupling (the
  package-served deployment against a live manifold is the recorded next path). IA:
  reference-first, measure-first entry, searchable; every fact links to its law, its
  trial, and its demonstration — "copy as query" primary, demo-player wiring on the
  site instance only.
- **Home:** standalone `/explorer` page; the homepage exhibit keeps a compact entry
  point. Page copy is corpus-sourced under the copy law — drafts to Huayin at CP-3;
  NOTHING merges to `apps/website/**` without his explicit go, and the page's
  before-freeze-or-after-launch sequencing is HIS call at CP-3.
- **Describe (D1, closed by assembly):** extend the shipped per-kind shape ADDITIVELY —
  License blocks verbatim across fertility/hierarchy/assert; signature addressing
  (universe-qualified where duplication exists); basis type + absence semantics;
  scope/cut state; operator properties. No alias block. Additive under the tool-surface
  discipline; any shape question at CP is a CV-ledger line.

## Also in scope, small
- The §2c universe-resolution machinery: the (metric, level)→one-universe
  well-formedness check (⊤ included in every metric's combo set), suffix addressing
  with universe-qualified metrics (`universe.metric`), the expression law
  (cross-universe expressions → the ERROR channel with the two-path remedy: juxtapose,
  or declare), the frame juxtaposition law (same-OBJECT anchors), single-universe
  ceremony sugar.
- The ADR-034 amendment: D2 superseded (ALIAS cut; the promise's fulfillment mechanism
  recorded) — one paragraph, rides this WP's first specs commit.

## Out of scope, explicitly
ALIAS (cut) · region cuts (coordinates-scoped assert violations — refinement recorded,
not built) · the Law/Map artifact split (Authoring-era) · the sampling-policy/masking
knob (ledgered) · multi-context Authoring modules (code/docs/semantic-layer ingestion) ·
WITHHOLD/ACCESS, INHERITS (ADR-034 D3/D4) · the visual anchor-lattice map · live
compute · the comma retirement and any demo renames (post-launch hygiene sweep) ·
Cacher factoring and THE rename (its own WP, after this one).

## Checkpoints
- **CP-0** — you read the capture end-to-end and return a mapping: every ruled item →
  its intended code home (the WP-anchor-grammar checkpoint pattern), plus any layering
  questions. No code before my answers.
- **CP-1** — syntax + adjudication (Track 1): parser additions, License reuse
  demonstrated UNCHANGED, the `conflicting_data` table-check finding, absence-semantics
  wiring design.
- **CP-2** — init (Track 2) + the eval suite's benchmark list and knowledge-package
  draft (Track 3) for my ratification.
- **CP-3** — describe + Explorer (Track 4), with the `/explorer` copy drafts and the
  sequencing question.
  - *Note (added 2026-07-16, increment 6):* the CP-3 site beat should CONSIDER adding **BASIS to the
    demo manifold** — the honest zero in a juxtaposition (events absence rendered as 0, alongside a
    spine gap) is strong exhibit material for the four moods / the Certificate layer. Decided at CP-3,
    under Huayin's go, as **one recapture** (adding BASIS moves seeded numbers; the drift-guard is the
    tripwire, Q5 rider ii). Absence semantics is shipped and inert on the basis-less demo today.
- **CP-4** — full diff, per-package green suites, the eval suite's first run results.
- Draft PRs throughout; my approving review per branch protection; forks get durable
  `open_forks.md` rows BEFORE their PR merges; a ruled item leaving scope is a
  checkpoint event BEFORE merge; no deploys from this WP except the `/explorer` page
  merge, which holds for my explicit go.
