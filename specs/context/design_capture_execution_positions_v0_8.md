# Design capture — execution positions: where Columna computes, combines, and governs
**v0.8 · ratified rulings (Huayin, 2026-07-12 and 2026-07-14) · v0.2 Polars dual-role ·
v0.3 the Cache(r), per-Manifold engine, layered cache · v0.4 the derivation duty · v0.5 the
transformation part · v0.6 closes the naming fork: the OPERATOR framing, no third member;
the Registry belongs to the Combiner · v0.7 aligns naming to the historical term **Operator
Registry** (Huayin) · **v0.8 (2026-07-14, Huayin): the resolution-time trichotomy is STRUCK,
replaced by the denotation rule; FERTILITY ratified (term + declared-and-adjudicated
ruling, Certificate-kernel verdicts); family clarified (askability vs travel; derived
families by declaration only); the declared resolution anchor + the resolution ladder; the
cache admission law + the never-substitute law. Editorial: derivation-duty prose reconciled
to the struck trichotomy — no rulings beyond the listed amendments.** · feeds: enterprise
plan, the eventual "sits beside your stack" page, WP-5.2 positioning doc, WP-B**

## The three functions, and where they live

Naming (ratified): the metric-engine layer decomposes into **Compute**, **Combine**, and
**Cache** — plus the rejected **Pushdown**. The **Metric Engine = Combine(r) + Cache(r)**:
the correctness member and the optimization member. Each Manifold has its data scope and
its own Metric Engine instance — one Manifold, one engine — to avoid conflict.

1. **Grammar Layer + Combiner: bundled, always.** The Manifold spec, Frame-QL, and the
   Planner (judgment) ship inseparably with the Combiner (the execution of combination:
   cross-column operations, transport, final reductions, two-projection arithmetic, the
   disclosure-bearing steps). The Combiner's formal responsibility is **heavy-duty** — it is
   real execution over potentially large reduced columns, not bookkeeping — which is why it
   is implemented on Polars. There is no "grammar-only" deployment tier: verdicts without a
   trusted combiner would leave the semantically delicate work to uncertified hands, which
   contradicts the promise. The bundle IS Columna.

2. **Columna is NEVER the raw Compute.** Per-column heavy lifting — scan, filter, reducing a
   single column toward the plan's grain — is always delegated to a backend engine. This is
   true today (DuckDB, Polars, SQLite as backends) and remains true at enterprise scale
   (Databricks, Snowflake, ClickHouse, ...). **Polars plays two roles, as two instances:**
   one Polars instance is the Combiner's implementation substrate (Columna's own layer);
   another appears as a backend engine among backends. Same library, different roles —
   the role, not the library, defines the position. The Combiner's authority would not
   change if its substrate were swapped; a backend Polars instance acquiring combination
   duties without certification would violate the seam. Consequence: Columna never competes
   with the warehouse for horsepower; it is the warehouse's best-behaved client, asking only
   for columns at grains. Only reduced columns egress — data gravity respected, movement
   minimized.

3. **Pushdown of the Combine: NO — hard NO** — with exactly one exception: a backend may
   host combination only by **re-implementing the Combiner and certifying against the
   reference implementation**. The exception is not a relaxation; it is the rule wearing the
   backend's clothes. The algebra may travel; the authority does not.

The seam is therefore FIXED, not tunable, and it is the ADR-031 boundary: *the backend
delivers columns, never combines them.* This pins the semantic-fidelity surface to
per-column operations only — a small, certifiable contract — because the treacherous part
(combining) never leaves home.

## The multi-source doctrine (the BI-altitude position)

Business use context crosscuts databases. Real use cases routinely span the main warehouse
PLUS other engines, data APIs, spreadsheets, user-provided files. This is why BI tools never
married a single database — and Columna occupies the same altitude: **governance of business
context, close to BI; beside the warehouses, above the SQL, married to none.** **Backend
agnostic** (ratified term): works smoothly with every backend; depends on none.

Architectural corollary (not a feature — a consequence of the seam): because combination was
never any backend's job, cross-source is not a special case. A column from Databricks, a
column from an API, and a column from a spreadsheet are the same kind of citizen — each
arrives with its anchors; the Combiner governs and discloses provenance like any other fact.

Doctrinal extension (approved metaphor): the Thesis says "the tables were only ever one
chart on it." At enterprise scale: **each database is only one chart on the enterprise
Manifold.** (Terminology caution: "Atlas" is reserved by the Silent Failure Atlas — say
"charts"; do not coin "enterprise atlas.")

Catalog relationship (e.g., Unity Catalog): read-and-attest. The platform catalog remains
the system of record for what exists; the Manifold is the system of record for what is
legal. No write-back dependency; any deeper integration is a partnership decision, not an
architectural need.

## Certification (narrowed by the rulings)

- **Column-delivery certification** (the standing program): every backend adapter must
  reproduce the reference semantics for per-column operations — nulls/missingness, numeric
  behavior, grain reduction — via a golden parity suite against the reference
  implementation.
- **Combiner-port certification** (the exception path, hard-gated): a re-implemented
  Combiner must pass the full algebra parity suite, version-pinned, before it may carry
  combination.
- **Execution honesty on the wire:** backend/port certification status is disclosable like
  any other assumption. The ladder, applied to execution: reference · certified · disclosed.
  A number computed via an uncertified path arrives saying so.

## The known edge (recorded honestly)

Hard-NO pushdown means combination executes in Columna's process. At aggregated combine
grains (the normal metric case) intermediates are small and this is a non-issue. When a plan
legitimately combines at a fine grain across large sources, the Combiner is the bottleneck —
by design, no warehouse can rescue it. The Polars substrate is why the practical ceiling is
high; the ceiling nonetheless exists. Posture: a knowable, disclosable limit (plan-time
estimate of combine-grain cardinality), with the certified Combiner-port as the designed
escape hatch. Not a flaw; an edge the system should know out loud.

## The Combiner's derivation duty — derived columns, denotation, and fertility

**Derived columns are columns.** Derived dimensions (week/month/year from date; a
parametric currency conversion from amount + rate) and derived metrics (profit =
revenue − cost; conversion rate = conversions ÷ visits) are not stored data; they are
generated from stored columns through formulas or defined processes. The structural rule:
the algebra is **closed** over derivation. A derived column's V/M/B hazard anchors are
*inferred through the formula from its inputs* — type inference for substance. Profit's
anchors come from aligning its inputs' (with transport where grains differ); a ratio's
B-anchor acquires barred directions its inputs lacked (a rate must not be re-summed). The
derived column re-enters the algebra first-class — askable everywhere its components
lawfully reach; its *travel* is governed by declared fertility (below). Anchor propagation
— not the value — is the derivation's real product; this is what separates it from
semantic-layer "formula fields," which hold the formula and infer nothing about what the
result may legally do next.

**Denotation rule (RULED, Huayin, 2026-07-14; SUPERSEDES the v0.4–v0.7 resolution-time
trichotomy, which is struck):** a derived name at an anchor denotes its formula evaluated
over co-anchored atoms at that anchor — deterministic; serve-clean is correct. There is no
engine-side clarify for this family: the Frame-QL expression is unambiguous even where the
English sentence is not; sentence-level underdetermination is the translation layer's to
resolve, armed by the describe surface. (Origin: the design session itself committed the
semantic-import error on `aov @ cal.month` while auditing it; the denotation is what caught
it. See the launch-post confession sequence, entry four.)

**Fertility (ratified term):** a derivation member is *fertile along a lineage* iff its
reduction there commutes (mathematical gate) and is permitted (declared gate) — the
member×lineage-grained mirror of the B-anchor: measures are open by default and B-anchors
close directions; derivations are closed by default and fertility declarations open them.

**RULED (Huayin, 2026-07-14): fertility is declared.** Rationale: unlike user intent
(irrefutable by data), a fertility claim is refutable by data — but data cannot grant it:
a counterexample refutes forever; no number of confirmations proves. The constitutional
sentence: *authority is declared; mathematics may verify; data may only refute or
corroborate; the default is closed.*

**Adjudication (publish time, Certificate-kernel shape per reference manual Part VI):**
VERIFIED — symbolic proof from the formula and operator algebraic properties; timeless.
CORROBORATED — refutation-tested against attested data, no counterexample; watermarked to
its attestation; re-adjudicated on re-attestation; may flip. CONTRADICTED — counterexample;
fails closed: the manifold does not publish. UNTESTABLE — stands on authored authority,
disclosed as asserted. Fertility is the Certificate layer's first customer; Fork 5 (the
rest of that layer) remains open.

**Degradation direction:** a revoked license drops the derivation back to
recompute-from-components — the infertile default never left, so the system degrades
toward correctness, never away from it.

**Family, clarified (RULED, Huayin, 2026-07-14):** a family of one is a family (shipping
precedent: `med_amount`, holistic family of one). On measures, family grants *askability*
and fertility grants *travel* — deliberately distinct: infertile members (holistic,
distinct) remain askable via recompute or via fertile carriers (the sketch doctrine is
exactly an infertile member given a fertile carrier). On derived columns, family members
are created only by adjudicated fertility declarations — there askability and travel
coincide by construction, and the default family is empty.

**Declared resolution anchor.** The alternative reading (e.g. mean of daily rates) is
expressible as a DISTINCT metric whose meaning embeds its resolution anchor (`AT day`,
reduced by its declared member). Infertility bars silent reduction; it never bars reduction
that is the declared meaning. With this, the struck trichotomy's three concerns are fully
rehoused: default denotation (above), licensed travel (fertility), declared resolution
(this).

**The resolution ladder (RULED, Huayin, 2026-07-14)** — how a derived name at anchor A is
served: **(1)** identical-hit lookup at A → serve (with upstream-resolution provenance
when the hit is a materialized metric); **(2)** recompute from components at A — the
denotation, the default, exact, available whenever the components lawfully reach A;
**(3)** reduce cached finer values to A — ONLY under a fertile license, and then purely as
an optimization, since the license is exactly the theorem that path 3 equals path 2.
Infertility deletes path 3; it never creates a refusal that paths 1–2 could have served.
A **materialized** metric (pre-resolved values, no formula) has no path 2: travel requires
a licensed family member along the lineage, else refuse disclosing the block — which is
the shipped `blocked_reduction` measure semantics, now recognized as the infertility
refusal it always was.

**Reduction OF a derivation** (e.g. `avg(aov) @ cal.month`): unpinned, the input anchor is
underdetermined IN STRUCTURE — a genuine engine clarify, enumerating candidate input
anchors (the mean-of-daily family does yield an engine ask-back, exactly where the
ambiguity is visible in the expression rather than imported from a name). Pinned
(`avg(aov@day) @ month`), it is a definite quantity: fertile → any path may serve it,
including a pooled lookup (that equality is what the license asserts); infertile →
compute what was asked from components, or refuse with the reason where components
cannot reach. **Never substitute** — see the cache admission law below.

**Derived dimensions are the lattice-builders.** A derived dimension adds a *reduction
direction*, not merely a column — the anchor lattice the Cache(r) navigates is largely made
of them. Their parameters are load-bearing in the classically silent way (ISO vs. US week;
calendar vs. fiscal year; which rate table, as-of when): parametric derived columns give
the parameter a field and therefore a disclosure on the wire. Note the currency case spans
both worlds: a fixed rate is a scalar map; a daily-rate parameter is itself a column,
making the derivation cross-column — constitutionally Combiner work.

**Consequences.**
1. *Cache policy:* governed by the admission law (Cache(r) section below) — only the
   fertile is cached; the fertile is cached as components first. (The v0.7 wording of this
   item derived cache policy from the struck trichotomy; the admission law supersedes it.)
2. *The seam, refined:* derived-DIMENSION scalar maps applied during scan are per-column
   operations — backends may execute them under the certified-delivery contract (the
   formula may travel; the authority does not). Derived-METRIC resolution is cross-column
   and therefore Combiner-only, always. Derivation *is* combination, formula-shaped — which
   is why this duty lives in the Combiner.

## The Operator Registry — sketch, window, and inference operators

**Implemented (Huayin, 2026-07-12):** hll_merge / hll_estimate and sketch/probabilistic
operators generally; windowing functions; probabilistic inference producing unbiased
estimates as output metrics.

**Sketches repair the lattice.** Distinct count is the canonical navigation dead-end (does
not re-aggregate; a cached distinct count is a leaf). The sketch fixes this structurally:
hll_merge is associative, commutative, idempotent — a lawful family reducer — so the sketch
column is freely reducible where the raw measure was barred. Formally two columns: the
**sketch column** (values in sketch space; reducer = merge; rich descendant cone) and the
**estimate column** (hll_estimate as a mapper out of sketch space; resolution time = output
anchor ALWAYS — estimates must not be merged; the estimate's B-anchor bars further
reduction). Corollary of the ratified cache rule: **cache the sketch, never the estimate.**
Layered-cache application: department sketches merge at the enterprise layer into org-wide
distinct counts — tiny, shareable, identity-certified. Estimate error rides the existing
wire caveat field (rel_error): probabilistic metrics need no new honesty vocabulary.

**Windows are anchor-preserving, order-dependent mappers.** A window function consumes a
column at anchor A and produces a column at the SAME anchor A whose values depend on an
ordered neighborhood — not a reduction. Structural requirements the grammar checks: the
anchor must carry an order; **the M-anchor's leak IS the window frame** (declared, e.g.,
d−6..d for a 7-day MA). Grammar-visible silent failures: partial windows at series edges;
frames crossing universe boundaries (entity enters/leaves mid-window) — both
disclosure-shaped. Cache posture: windowed columns cache poorly (order-dependent,
edge-effected); cache the base series, window on demand.

**Unbiased estimators: a ladder promotion into layer I (Atlas F6).** The split runs through
the estimator: **the estimator's mathematical properties are certifiable; its assumptions
are not.** Unbiasedness given a sampling design is a theorem (grammar); whether the design
held in reality is a fact about the world (disclosure — the assumptions ride the wire as
material caveats). This promotes a real band of F6 failures from disclosable-only to
certifiable-conditional-on-disclosed-assumptions — a genuine ladder promotion achieved
without moving the Seam's ceiling: the estimator's math was always on the syntax side;
nobody had put it there before.

**The operator onboarding contract (proposed doctrine, independent of the naming fork):**
every operator class enters through the grammar — new value domains receive anchor
semantics; new operators receive legality theorems; new outputs receive their disclosure
hooks — or it does not enter.

**RULED (Huayin, 2026-07-12): the Operator framing.** No third Metric Engine member; the
Metric Engine remains Combine(r) + Cache(r). Sketches, windows, and estimators are
**operator classes in the Combiner's Operator Registry** — the algebra's standard library —
entering via the onboarding contract above. Rationale: simpler and practical, no new seam,
no functionality sacrificed. Mappers and reducers are what the Combiner executes; these are
mappers and reducers.

## The fourth position — the Cache(r) (sound aggregate navigation)

**What it is.** Grown organically from three capabilities — caching, column selection (pick
the column family at its best input anchor), and usage-driven dynamic optimal caching — the
Cache(r) is the sound version of the role OLAP called the aggregate navigator: answer a
query from an already-materialized column whenever a lawful path exists. The difference
from thirty years of prior art is the proof obligation: a cached column at anchor A serves
a request at anchor A′ **iff the algebra certifies the reduction A→A′** — same criterion
that gates a fresh query. **A cache hit is a theorem application.** The same anchors that
block illegal queries certify legal shortcuts: the governance metadata pays for itself in
round-trips saved.

**The admission law (RULED, Huayin, 2026-07-14): only the fertile is cached; the fertile
is cached as components first.** "Cache the sketch, never the estimate" and "cache the
components, never the derivation" are both instances: the cache stores only what may
lawfully travel, and fertility verdicts are the theorems behind "every cache hit is a
theorem application." CORROBORATED-licensed entries carry the attestation watermark and
invalidate on re-attestation; VERIFIED licenses are timeless. Components-first is retained
as policy within the licensed region (license and economics are separate questions).
Naming: "Fertile Cacher" REJECTED — the law belongs to the columns; the component's name
stays inside Fork 1's blast radius.

**The never-substitute law (RULED, Huayin, 2026-07-14): a cache hit may never change the
quantity asked.** Serving a pooled value for a requested mean-of-finer is a silent
substitution — the `order→transaction` genus from the confession sequence. Fertility is
the theorem that a shortcut serves the SAME number; the admission law therefore deletes
the substitution hazard from the cache by construction — an infertile value in the cache
is the precondition for every substitution, and it is never admitted.

**Rulings (2026-07-12).**
- **Name: Cache(r)** — sibling to Combine(r); role-named per the labeling discipline.
- **Substrate: Polars** — same dual-role rule as the Combiner: the library is
  incidental; the role is what is fixed.
- **Freshness & hot/cold consistency:** general caching obligations, nothing
  Columna-specific — discharged through the Manifold's existing contract component (data
  attestation, universe definitions). The cache inherits its obligations from the contract;
  it does not invent doctrine. Natural test expression: a hot/cold parity suite — cache-hit
  and cold computation produce identical wire responses modulo freshness metadata.
- **Status: design-stage, to be purpose-built** — including the telemetry posture
  (usage-driven optimization consumes query logs; scope, retention, and locality of usage
  stats are part of the deliberate build-out, stated before the role is marketed).

**Optimization space (recorded).** The candidate set is structured by the Manifold —
(family, anchor) pairs — and pruned by legality: fertile members at coarse anchors have
rich legal descendant cones (load-bearing cache entries); an infertile member's value can
serve only itself (a leaf, admissible only as an identical hit). Cache at the anchors with
the richest lawful descendant cones, weighted by observed usage.

**The layered Cache(r) (large installations serving many Manifolds).** Per-Manifold engines
remain the rule; atop them, shared cache layers — enterprise, department, project — are
possible *because of* the grammar: a cached column's identity is its semantic identity
(family, input anchor, universe, attestation lineage), checkable by the algebra, so sharing
is a theorem about column identity rather than a trust arrangement between teams. Names
cannot fragment the cache — a metadata-independence dividend: communicative metadata varies
freely while cache keys ride only the load-bearing kind. Promotion into a shared layer is
gated by the same vetting/certification machinery that gates everything else.

Governance consequences (recorded, to shape the build-out):
1. **The shareable cache is exactly as large as the shared *fertile* grammar** — sharing
   presupposes common (or explicitly mapped) families and universes at the sharing layer;
   the enterprise cache's performance payoff becomes the standing economic incentive for
   semantic convergence across departments.
2. **Layer visibility follows data scope; invalidation flows down.** A Manifold reads a
   shared-layer column only where its scope and universe legitimately contain it; the cache
   hierarchy respects the scope lattice as well as the reduction lattice. Attestation
   changes at a shared layer propagate invalidation to every inheriting layer — riding the
   contract machinery, with the propagation paths made explicit.

**Origin note (for the eventual public telling).** The role was not designed from the OLAP
angle; it precipitated out of the algebra — sound by construction — because the grammar was
already carrying exactly the information navigation needs. The container world bolted
navigation on and prayed; in the substance world it condenses for free.

## Fork rulings (closes the five forks from the 2026-07-12 evaluation)

1. Pushdown boundary — RULED: fixed at the column boundary; per-column compute to backends,
   combination never (exception: certified Combiner port).
2. Certification governance — program narrowed to column-delivery parity + hard-gated
   Combiner ports; suite versioned with the reference engine; per-backend-version pinning.
   (Operational ownership: to be assigned when the first external adapter lands.)
3. Engine-optional deployments — RULED OUT: grammar layer and Combiner are inseparable;
   "grammar-only" is a contradiction, not a tier.
4. Catalog relationship — RULED: read-and-attest.
5. Public sequencing — unchanged and binding: no "sits beside your stack" claim ships until
   pinned to what the shipped code does that day; the site integrity rule covers
   architecture claims.

## Ratified-terms ledger (standing)
backend agnostic · outcome pair · Operator Registry · **fertile / fertility (2026-07-14)**
— one everyday word for "commutes with reduction along the lineage and is permitted there."

## One-sentence summary

The Planner decides what may be computed; backends supply per-column horsepower wherever the
data already lives; the Combiner — Columna's own, always — makes many charts one governed
answer; the Cacher makes the lawful path the fast path — and only the fertile travels; and
the wire says what was done.
