# The Two Pillars — a strategy note for the post-launch ledger (v0.1)

*Written down at the desk, 2026-07-19, from the RELATE discussion with Huayin, so we
don't forget. Status: doctrine + WP seeds; nothing here builds before the launch.*

## The thesis

Two hard analytics query-processing challenges, taken seriously, differentiate
Columna from the semantic-layer crowd outright:

1. **Probabilistic sketch operators** (HLL-class distinct counting, quantile
   sketches, and kin) — the approximate-but-mergeable algebra.
2. **The RELATE processing pattern** — lawful crossing of non-functional (M:N)
   edges: membership, allocation, resolution.

The structural reason these are OUR pillars and not theirs: **a semantic layer is a
compiler to someone else's engine.** It translates declared metrics into SQL and
inherits whatever semantics, precision, and processing patterns the target warehouse
happens to have. Columna owns both the meaning layer AND the execution (the Manifold
adjudicates; Polars executes what the planner ruled). Processing patterns that
require engine cooperation — allocation joins with reconciliation guarantees, sketch
merge-trees with declared error bounds — are patterns a SQL-compiler cannot promise
and we can. The moat is not the declaration language; it is declaration + trial +
EXECUTION under one law.

The shared shape of both pillars — and the house method applied to them:
**barred by default · unlocked by declaration · the declaration stands trial ·
the answer discloses.** Never query-time improvisation. Every BI tool "supports"
M:N joins and approximate counts by silently picking a semantics; we make the
author declare one, adjudicate it, and put the consequence in the answer.

---

## Pillar 1 — the RELATE processing pattern

### The role ruling (2026-07-19, Huayin concurring)

RELATE is LOAD-BEARING and stays in the language. Multiplicity between logical
concepts is SUBSTANCE under §2b″ — the spec must be able to explain its own refusal
("a product belongs to up to 3 categories; a rollup would multi-count") without
citing plumbing, so M:N-ness is Law, not Map. RELATE is the ANTI-EDGE: HIERARCHY
declares "connected, and aggregation survives the trip"; RELATE declares "connected,
and no lawful rollup exists." A meaning-model without the second sentence has a hole
where the most common analytical error lives. It is also the commonest folklore
there is ("category revenue double-counts") — and folklore-into-the-system is the
pitch. Cut candidates, if minimalism ever asks, are a manifold's scope or the
visual — never the language.

Wire consequence (ruled, shipping as columna-server 0.5.0): `relates[]` on
`describe_manifold` — logical names + the NOTE verbatim, nothing physical; additive,
contract "1"; the generator fail-closes on the missing key (the wedge extended to
Figure 1). Future verdicts (multiplicity claims on trial) join additively.

### The use-case taxonomy (six classes + one deferred)

1. **Membership / touch** — each category receives the FULL value of every related
   product; totals deliberately exceed the grand total. (Category performance,
   multi-tag reporting, multi-touch attribution, portfolio lenses.) Treatment: a
   declared unlock minting a measure whose NAME carries the semantics
   (`revenue_touching`), served in DISCLOSE ("multi-counted by construction").
   Already half-exists as E6's deliberate-overlap alternative.
2. **Weighted allocation (apportionment) — the crown.** Value SPLITS across
   categories: equal shares or a declared weight; totals RECONCILE to the grand
   total. (Shared-cost allocation, category P&L, royalty splits, attribution.)
   Treatment: `ALLOCATE equal | ALLOCATE BY <weight>` declared on the RELATE;
   weights-sum-to-1 is an ADJUDICABLE claim (a trial, like returns_bounded);
   reconciliation itself is a checkable, badge-wearing fact. The most
   Columna-shaped class of all.
3. **Assignment (functionalization).** A declared canonical pick collapses the M:N
   into a real functional edge — adjudicable ("exactly one per product" regardless
   of criterion) — after which ordinary hierarchy machinery serves it. FACE name:
   `assign` (ruled 2026-07-19, replacing `primary`): the face names the value's
   DISPOSITION on the trip, never the selection criterion — the criterion lives in
   the declaration (`FACE assign = <selection>`: by primary flag, first-listed,
   max-weight — declared, adjudicated). The canonical face triad is now a
   self-teaching verb system: **touch** (the value reaches every match) ·
   **assign** (the value goes to one) · **alloc** (the value splits across).
   Naming honesty survives: `category.assign` ≠ `category`, marked in the name.
4. **Count and distinct — the cheap class.** Membership counting has no
   value-replication problem. Treatment: OPERATOR-LEVEL LICENSING on non-functional
   edges — count/distinct licensed to cross a RELATE as-is; sum/avg barred unless a
   scheme from 1–3 is declared. Unlocks assortment-breadth and coverage questions
   for free. BUILD FIRST.
5. **The relation as the subject** (basket/affinity, co-occurrence). No new
   machinery — MODELING DOCTRINE: the bridge is a population; declare a universe on
   the membership grain and everything existing applies. Costs a KP paragraph and a
   worked example.
6. **Partial coverage.** Products in no category; enrichment covering half the base
   (exactly why engagement_scores was scoped out in ch2 — this class retroactively
   names that ruling). Treatment: coverage as an ADJUDICATED property of the
   relation (measured %, plus declared handling: excluded-with-disclosure or an
   explicit "uncategorized" bucket). Rides whichever of 1–3 lands first.
7. **Temporal relations — DEFERRED.** As-of membership, SCD-shaped. Real, heavy;
   the frozen demo dodges it honestly; must not gate the others.

Sequencing: 4 → 1 → 3 → 2, with 5 as doctrine and 6 riding along. All post-launch.

### The solution mechanism — FACES (Huayin, 2026-07-19; refined at the desk)

Crossing semantics is addressed as a FACE of the related coordinate:
`revenue AT {category.touch}` / `{category.assign}` / `{category.floor_alloc}` —
the measure-family move applied to the dimension side (stock.sum/stock.last ::
category.touch/category.assign): one related level, faces with different crossing
laws, each licensed, adjudicable, and named for what it does. The semantics belongs
to the TRIP, not the measure — declared once on the relation, inherited by every
crossing measure. Laws:

- **Declare the instantiation, never parameterize the query**: parameters live in
  the declaration (`FACE floor_alloc = ALLOCATE BY floor_space`), adjudicated at
  publish (weights sum to 1 → corroborated), described per the folklore rule;
  queries address names only — EXPLAIN stays static, the cache can key it.
- **The bare coordinate stays uniformly barred**; the clarify lists the declared
  faces with their descriptions — the menu. Same interaction shape as the
  input-anchor clarify: the system lists readings, the human re-issues explicitly.
  Class 4 (count/distinct) rides `.touch`; no bare-crossing exception.
- **Per-basis licensing; v1 = EVENTS ONLY** (Huayin's ruling — code right from the
  beginning): on events the expansion is honest arithmetic; on a spine, replication
  corrupts the grid's own completeness claim — refused with a reason until that
  thinking is done.
- Coverage (class 6) attaches to each face's adjudication; class 5 needs no
  mechanism (the bridge as its own universe); class 7 stays deferred.
- Wire: `relates[].faces[]` joins the 0.5.0 field ADDITIVELY when built — the field
  was born with room.

### The implementation map (traced at the desk, 2026-07-19)

The stock.sum/stock.last analogy is implementation-LITERAL. The three-layer division
(model declares · planner adjudicates · engine executes) carries faces wholesale:
MODEL — `Face` on the Relate mirrors `FamilyMember` nearly field-for-field (name,
scheme, basis-license, DESCRIPTION mandatory, license constructed only by the
adjudicator at publish — the polarity law). PLANNER — the dotted-coordinate
resolution ALREADY EXISTS (`cal.month` splits at the first dot and validates against
edge-derived membership); `category.touch` is the same path with one more membership
source (the RELATE's declared faces), and the planner mints the bare-coordinate
clarify-as-menu. ENGINE — receives pre-adjudicated atoms; faces add transport
strategies (touch join-multiply; allocation split) beside the existing monoid path;
the cache key extends naturally. Bonus findings: `_resolve_sketch` and `scan()`
already live in the engine (pillar 2 has an execution foothold today); the M:N
withholding exists at BOTH planner and engine (defense in depth — faces cannot
bypass a single gate). SHIP-DARK RULE for v1: the clarify-as-menu fires only when
faces are DECLARED; a manifold declaring none (Cascadia — Dana's questions need
none) keeps today's exact clarify — zero case-demo ripple, mechanism proven in
fixtures, requirement-driven scoping honored.

---

## Pillar 2 — sketch operators (the seed; to be developed)

The problem: the most-asked hard metrics are non-additive (distinct customers,
percentiles, funnels). Exact computation can't pre-aggregate or cache; the industry
answer is probabilistic sketches (HLL for distinct, KLL/t-digest for quantiles,
theta for set operations) — approximate summaries that MERGE.

Why this is Columna-shaped, three ways:

- **Sketches are monoids.** Mergeability is exactly the operator registry's
  vocabulary — a sketch is an approximate monoid with an error bound. The registry
  extends: `distinct` gains a sketch-backed member the way `stock` has `sum` and
  `last` — same family, different operator, different license.
- **Approximation is a DISCLOSURE, not a footnote.** A served approximate count
  carries its declared error bound in the answer ("±2% at 95%" as a caveat class) —
  the four-mood temperament extended to precision. The error bound is a CLAIM, and
  claims stand trial (measured error vs declared bound on reference data = an
  adjudication). No one else treats approximation as adjudicated meaning.
- **Sketches are the cache's algebra.** The metric-engine caching item from the
  dream deck and this pillar are one project seen from two sides: mergeable partials
  ARE the incremental cache; the summary-tables doctrine ("performance is the
  cache's job, not a table's") gets paid in sketch coin. `sketch.py` already sits in
  core as the placeholder.

Open design questions for the eventual WP: exact-vs-sketch selection (declared per
measure member, never silent); the wire shape of an approximate answer; whether
sketches serve cross-universe (they're anchor-local summaries — likely yes with the
same laws); adjudicating error bounds honestly.

---

## The convergence

Both pillars are the same sentence at different layers: **extend the operator
algebra, govern the extension by declare–adjudicate–disclose, and execute it in the
engine we own.** Pillar 1 extends WHERE operators may travel (across a declared
non-functional edge, under a declared scheme). Pillar 2 extends WHAT operators may
be (approximate, mergeable, error-bounded, on trial). The semantic-layer crowd can
declare; only an engine-owner can execute-and-guarantee. That is the
differentiation, and it is honest.
