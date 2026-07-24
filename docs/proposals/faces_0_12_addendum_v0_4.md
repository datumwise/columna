# Faces charter addendum — 0.12 "the triad completes" (v0.4 — degenerate-spine declaration corrected, ruled (1))

*Desk artifact, 2026-07-24. Builds on and defers to:
`multi_universe_processing_notes_v0_1.md` (the theory; ships alongside as the
preamble) and the two-pillars charter (declare-instantiations-never-parameterize;
bare coordinate → menu; events-only licensing for crossed measures). Scope ruled by
Huayin: G1 (triad) + G4 (chain guard) + G5 (distinct-at-faces, verify-then-rule) +
the ledger re-sequencing note. G2/G3 (alignment + carving audits) are 0.13; G6
(generator) behind; G7 (Explorer territory redesign) trails 0.12.*

## 1. The third universe (Cascadia)

- Warehouse gains `category_attributes.parquet`: `category_id, priority,
  alloc_weight` — 12 rows, generated deterministically (regen-script stable-hash
  pattern, byte-reproducible). `priority`: distinct integers 1..12. `alloc_weight`:
  positive values, varied (not uniform), NOT pre-normalized — a raw driver.
- Manifold gains:
  `UNIVERSE category_profile = category BASIS spine` — a one-grain spine, no time
  axis (the degenerate spine; no new basis kind).
  `MEASURE priority ON category_profile FROM category_attributes VALUE priority`
  `    FAMILY { last ORDER category }`
  `MEASURE alloc_weight ON category_profile FROM category_attributes VALUE alloc_weight`
  `    FAMILY { last ORDER category }`
  (CORRECTED per the degenerate-spine proof: bare VALUE does not parse — every
  VALUE measure carries FAMILY; the degenerate one-row-per-member spine declares
  `last ORDER category`, the identity read, per the stock precedent. RULED (1)
  over grammar sugar: an implicit ORDER default would violate the ORDER-mandatory
  ethos ruled this same increment. ROWED, not blocking: profile-spine measures
  served at grains coarser than base yield declared-but-arbitrary values under
  `last`; a base-grain-only family form is wanted eventually.)

## 2. Grammar (parser)

Within the existing `FACES { … }` block on a RELATE:

    FACE <name> = TOUCH
    FACE <name> = ASSIGN BY <measure-ref> ORDER MIN|MAX
    FACE <name> = ALLOC  BY <measure-ref>

- Face names carry ZERO operational meaning (scheme keyword carries the operation);
  any identifier is lawful.
- ORDER is MANDATORY on ASSIGN and has NO DEFAULT (ruled 2026-07-24): "top" is
  ambiguous across driver types (rank-like: MIN wins; score-like: MAX wins), and a
  silent default would be an unrecorded resolution — the precise sin. Precedent:
  stock's `last ORDER day`. A FACE lacking ORDER refuses to publish, naming the
  ambiguity.
- `<measure-ref>` is a declared-measure reference resolved against the manifold at
  publish (never a physical column). Either driver grain is grammatical (frontier
  level or membership base); 0.12's demo exercises the level grain.
- The declared-but-deferred parse refusals for ASSIGN/ALLOC retire.

Cascadia declares (descriptions are COPY — Huayin ratifies the strings):

    RELATE product <-> category VIA product_categories(product_id, category_id)
        FACES {
            touch   = TOUCH            -- (shipped string, unchanged)
            primary = ASSIGN BY priority ORDER MIN      -- DRAFT: "revenue goes to each
                product's top-priority category — single-counted; secondary
                memberships are not represented; totals match the grand total"
            split   = ALLOC BY alloc_weight   -- DRAFT: "revenue splits across a
                product's categories by declared weight — totals reconcile to the
                grand total"
        }

## 3. Adjudication (publish-time, fail-closed, via _prove_face per scheme)

- **assign**: driver measure servable at the frontier grain; present for every
  member appearing in the mapping; orderable; UNIQUE TOP per the DECLARED ORDER
  direction, per member's membership set (v1 satisfies this via global distinctness of the driver across the level's
  members — the trial proves distinctness; a violation names the tied members and
  the products affected). Coverage counted.
- **alloc**: driver non-negative; per-member driver sum strictly positive (a
  member whose memberships all carry zero driver = undefined split → the face does
  not publish). Normalization (driverᵢ / Σ per member) is the declared law, applied
  by the engine — never stored. (Doctrine note for the manual, not an adjudication:
  storing pre-normalized weights is derived truth; declare the raw driver.)
- **acyclicity**: the dependency graph {face → its driver measure → that measure's
  universe → any faces it would require} must be a DAG; proven at publish;
  fail-closed with the cycle named.
- Licensing unchanged: crossed-measure licenses remain events-only, minted at
  publish; driver measures live lawfully on spine universes (ruled).

## 4. Engine

- `_resolve_assign`: restrict the bridge to each member's top-ranked pair (the
  adjudicated designation), then single-row join — no multiplication.
- `_resolve_alloc`: join-multiply by the normalized driver.
- Both reuse the shipped face seam; `_resolve_touch` untouched.

## 5. Wire (additive only)

- `relates[].faces[]` entries gain `scheme` ("touch"|"assign"|"alloc") and
  `driver` (the measure ref; null for touch).
- Assign answers carry the **shadow**: `memberships_unrepresented` (Cascadia: 270)
  alongside inherited coverage.
- Alloc answers carry the **reconciliation badge**:
  `reconciliation: {crossed_total, base_total, delta, tolerance, status:
  "reconciles"|"shortfall"}` — the commutation certificate; shortfall occurs only
  under coverage gaps and is disclosed, never silent.
- Touch's skew disclosure unchanged. All three inherit the crossed-grain absence
  law.

## 6. G4 — the chain guard (in scope, cheap)

Crossing a result that already crossed a face (any multi-hop face path) REFUSES
with a named guard until disclosure-stacking is designed (notes §6.1). DRAFT
message copy: "this ask would cross two declared faces in sequence; chained
crossings are not yet licensed — ask at one frontier at a time." (Huayin ratifies.)

## 7. G5 — distinct-class measures at faces (RULED 2026-07-24: option B)

- VERIFIED (proposal transcript): `buyers AT {category.touch}` today = honest
  refusal — the shipped gate admits VALUE-monoids only; "sketch crossings are
  post-launch." Correct prior ruling; nothing harmful is deferred.
- 0.12 ships the REFUSE-HALF ONLY, and the refusal is the ANCHOR LAW speaking,
  uniformly for all three schemes over raw distinct-class (the shipped
  VALUE-monoid gate already produces it — the build delta is the message).
  DRAFT copy, one string, all three faces: "buyers' distinct anchor is spent at
  product — per-product counts cannot be summed, weighted, or routed. If a
  weighted composite of per-product counts is what you mean, declare it as a
  value measure; if distinct buyers per category is what you mean, that is a
  crossed-population count — coming with the crossing increment."
- TERMINOLOGY RULE (user-facing strings + manual): speak the DECLARATION
  dialect — buyers is exact `distinct(customer_id)`, a reducer; "sketch"/"HLL"
  is the engine's mergeable representation and must not surface in refusals.
- PERMANENT vs DEFERRED, kept distinct in all copy: alloc-over-distinct is
  UNDEFINED under both traversal modes (permanent); touch/assign-over-distinct
  are licensed-but-unbuilt (population-traversal, 0.13). See notes v0.2 §4.
- The SERVE-HALF (distinct rides `.touch` with overlap disclosure; per-member
  sketch reduce; gate relaxation) moves to 0.13 beside P1 — where the
  anchor-exhaustion corollary (notes §6.3) gets proven, not asserted, and the
  mechanics meet the sketch pillar they belong to. Ruled (B) over (A) explicitly;
  the ledger note records the sequencing as chosen, not drifted.

## 8. Exhibits, menu, manual, ledger

- **E11 (assign)**: `revenue AT {category.primary}` — total ≡ grand total to the
  cent; shadow 270. **E12 (alloc)**: `revenue AT {category.split}` — total ≡ grand
  total to the cent; badge on the wire. Both recorded via the standing seed
  pipeline; /case exhibit copy comes to the desk post-build.
- The bare-ask menu goes three-deep with the ratified face descriptions.
- Manual: the triad chapter replaces the deferred-refusal section; the doctrine
  note from §3 rides it. The multi-universe notes queue as the manual's theory
  appendix at 0.13 (when alignment makes them fully true in-product).
- Public ledger: dated re-sequencing note — DRAFT: "2026-07: the RELATE face triad
  (assign/alloc) completes ahead of OF-13 — shipped-surface coherence and the
  crossing menu's completion graded ahead; OF-13 remains the leading language
  increment thereafter, joined by multi-universe alignment (P1)." (Huayin
  ratifies.)

## 9. Release + discipline

- 0.12.0 across core/server/meta; publish-first flip order per the standing
  pattern; suites + recorded numbers byte-stable except where exhibits add.
- PROPOSAL.md commits to the repo at `docs/proposals/0.12-triad-PROPOSAL.md`
  (design history in the open, per the preserved-record ethos); the PR references
  it. Degenerate-spine VALUE path proven FIRST THING in the build.
- PROPOSAL-FIRST: no code before the desk verifies CC's PROPOSAL.md (design
  conformance to this addendum + the notes; file-by-file plan; honest LOC pricing;
  the G5 verification transcript; test plan incl. adjudication-failure cases — a
  tied rank, a zero-sum driver, a cycle) and Huayin speaks. Off-ramp standing: a
  structural surprise or a price far off touch's (~250–350 LOC) returns to the
  desk before any build.
