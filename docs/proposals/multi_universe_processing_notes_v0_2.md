# Multi-Universe Processing — working notes v0.2

*Desk artifact, 2026-07-24 (v0.2: traversal-modes settlement folded; §6.3 resolved). Two hats: the spine of the paper that follows "The Two
Anchors of a Measure," and the preamble of the faces charter addendum (assign/alloc,
0.12). Every construct named here either ships in Columna today or is the increment
under design; claims are checkable against the Cascadia manifold
(`manifold.cml`) and the public benchmark kit.*

---

## 0. The claim

Analytics practice treats "the data model" as one space: facts, dimensions, joins.
This is false, and the falseness is where silent failures breed. A warehouse is a
**federation of universes** — territories of functional reachability — and every
metric question either lives inside one territory or must pass a frontier. Inside a
territory, meaning composes freely. At a frontier, meaning does not compose unless a
law is declared. Multi-universe processing is the discipline of (i) finding the true
frontiers, (ii) enumerating the lawful passages, and (iii) refusing everything else.

The industry has one great tacit success here (conformed dimensions / drill-across)
and one great tacit failure (the bridge table with ETL-applied "weighting factors").
Both are cases of the same theory, stated below.

## 1. Universes are carved, not chosen

**Definition.** A *universe* is a population (a base) together with everything
functionally reachable from it: the maximal closure of the base under M:1 edges.
Its *lattice* is the set of grains so reached; its measures are declared on the base
and served at any grain in the lattice under the measure's own laws.

**The carving principle.** Universe boundaries are not an authoring preference; they
are determined by the functional structure of the data. The author's job is to
*record* the boundary, not to invent it.

Two corollaries, which are the day's two insights:

- **Expansion (M:1).** If level c₁ maps M:1 to level c₂, then c₂ belongs to c₁'s
  universe — the universe literally expands to absorb it, along with every attribute
  c₂ carries. Nothing is imported; the territory was always that large. *Cascadia:*
  store → region is functional, so region is simply a coarser grain of the
  transaction universe; `revenue` by region needs no ceremony.
- **Fission (M:N).** If the mapping is M:N, no functional path exists; the level on
  the far side — and every attribute it determines — is *another universe's*
  material. *Cascadia:* product ↔ category (a product sits in up to 3 categories).
  Category cannot be a grain of the transaction universe; "revenue by category" has
  no innocent answer; category's own attributes (a priority, an allocation driver)
  live at category grain in their own territory.

**The minimal pair.** `region` and `category` differ by one bridge table's
cardinality — and that single bit flips region into a LEVEL on a HIERARCHY and
category into a RELATE with FACES. This pair is the whole theory in miniature and
the recommended opening example of the paper.

## 2. Two bases, and the normalization procedure

**Basis kinds.** Two suffice (a deliberate economy; proposals for a third have so
far normalized away):

- **events** — the population is occurrences; measures aggregate along the basis
  (transaction: revenue = sum of amounts over sale lines).
- **spine** — the population is a lattice of positions; measures are states read at
  positions, governed by family law (inventory: stock VALUE, `sum` blocked across
  calendar, `last` ordered by day). A one-grain spine with no time axis is still a
  spine (the category profile: twelve rows, a priority and a driver per category) —
  the "reference/dim table" of industry practice is this degenerate spine, not a
  third kind.

**Normalization (closure-first).** Before classifying any inter-universe situation:

1. Close every universe under all M:1 edges (expansion).
2. Identify levels related 1:1 across universes: these are *the same level under
   two names* — an atlas-merge event, resolved by conforming, not by passage.
3. What remains between universes is then exactly: **shared grains** (identical
   declared levels in both lattices) and **genuinely M:N mappings**. Nothing else
   can survive closure.

This procedure is what eliminates most of the apparent case explosion (below).

## 3. The Frontier Theorem

**Statement.** After normalization, exactly two passages exist between universes:

- **P1 · Alignment (at a shared grain).** Each universe serves its own measures at
  the shared grain (or any common coarsening) under its own internal law; results
  compose by coordinate equality. No new semantics is created, so no new
  declaration is needed beyond the shared grain atlas itself. *Cascadia:* `revenue`
  beside `stock.last` at store × month. This is drill-across, re-founded: what makes
  the composition lawful is the *declared identity of grains*, not a naming
  convention.
- **P2 · Crossing (through a declared face).** Where the frontier is M:N, passage
  exists only through a FACE declared on the RELATE: a **driver × combinator**
  pair, adjudicated at publish, licensed, named for what it does. The measure's
  value is carried across the mapping under the face's law, and the answer states
  what the law did to it.

**Completeness clause (the Columna sentence).** There is no third passage. An ask
that is neither aligned nor licensed by a declared face **refuses**, and the refusal
names the frontier. The theory's force is exactly this closed-world claim: every
silent fan-out, every ETL-buried weighting, every "primary" chosen by an unrecorded
rule is an attempt to take a third passage that does not exist.

**Case-grid collapse.** The apparent eight-axis situation space (A/B each
events-or-spine; the frontier level in or out of each base; M:1 in either
direction; compounds) reduces as follows:

| Situation (after stating the frontier level c) | Resolution |
|---|---|
| c(A)→c(B) M:1, or c(B)→c(A) M:1 | Not a frontier: **expansion** absorbs it (normalization step 1) |
| M:1 both directions (1:1) | Same level twice: **atlas merge** (step 2) |
| c shared, any E/S combination | **P1 alignment** — E/S affects only each side's route to c |
| c–c′ genuinely M:N, any E/S combination, any basis-membership | **P2 crossing** — E/S and basis-membership affect only the pre-frontier route |
| Compound cases | Decompose per pairwise frontier; each normalizes independently |

**Why the E/S matrix collapses.** The basis kind governs *how a value reaches the
frontier* — an events universe aggregates along its basis to c; a spine projects or
applies family law — but by the frontier both present the identical interface: *a
value at a grain, carrying its anchors*. The crossing law is therefore
basis-agnostic. (Product↔category is E-meets-S not because that combination is
special but because spines are where drivers naturally live — see §4.)
Basis-membership of c (in the base vs merely reachable) likewise changes only the
length and lawfulness of the internal path — governed by family and anchor rules
(stock cannot reach a calendar coarsening via `sum`; a distinct-class measure
arrives with its decomposability spent) — never the passage taxonomy.

## 4. Drivers are spines; faces are driver × combinator

**Face =** (driver, combinator), declared on the RELATE, never parameterized in the
query:

- **touch** = (∅, take-all) — the value reaches every match.
- **assign** = (rank driver, take-top) — the value goes to exactly one.
- **alloc** = (weight driver, take-proportional) — the value splits, normalized per
  member.

**The driver lemma.** A driver must be single-valued per member at the frontier
grain — which *is* the spine property at that grain. Hence: **every lawful driver
is a spine at the frontier**, whatever universe it originates in. A driver at
category grain (priority, weight: the twelve-row profile) is a spine natively. A
driver at pair grain (shelf facings per membership) is a spine over the membership
population. An *events-derived* driver ("allocate by last year's revenue share")
is lawful precisely by first being served and frozen as a spine at the frontier
grain — derived-then-recorded — which gives the acyclicity law a concrete object:
the dependency graph of faces and their driver measures must be a DAG, adjudicated
at publish, fail-closed.

**Traversal modes and reducer classes (settled 2026-07-24, three-round check).**
The face shortcut `m AT {face}` has ONE uniform meaning — *value-traversal*: m
resolves at the frontier grain, and the resolved values travel under the face's
law (all / top / scaled). Legality is the measure's output anchor speaking, the
same law for all three schemes, no scheme carve-outs:

- *Additive monoids* pass — distributivity makes the shortcut exact.
- *Distinct-class* refuses uniformly — the anchor is spent at the frontier
  grain; per-member counts cannot be summed, routed, or scaled (a customer
  buying two products would count as 1.6 people under a 0.6/1.0 split; as 2
  under routing or union). One statute (Two Anchors), new instance.
- *Sketch-valued mergeables* (the engine's representation for distinct — an
  implementation layer, not the declared semantics): union and routing are
  mechanically sound (merge = population union); scaling is undefined
  (sketch × scalar has no operation, a permanent mechanical refusal).

*Population-traversal* is the second, distinct operation with its own spelling:
a DECLARED crossed-population measure re-evaluates the reducer over the
face-constructed population — union for touch, routed restriction for assign —
exact and meaningful for distinct-class. Alloc has no population form:
fractional set-membership is undefined, so alloc-over-distinct refuses
PERMANENTLY under both modes, while touch/assign-over-distinct are merely
UNBUILT (licensed by this theory; shipped with the crossing increment). The
refusal messages must keep undefined and unbuilt distinct — conflating them is
its own small dishonesty.

*The two authoring doors* (what the refusal teaches): the composite door —
declare per-member counts as a VALUE measure (anchors spent BY DECLARATION;
every face serves it; the author may restrict schemes via B-anchor blocking, a
future BLOCKED-in-face-context extension); the population door — the crossed-
population declaration above. Every operation in the space has exactly one
honest spelling; no spelling is ambiguous between two arithmetics.

**Adjudication (publish-time, all fail-closed).** touch: mapping well-formed
(pair-unique), coverage counted. assign: driver present and orderable on the
member set; a unique top per member (v1: globally distinct ranks make this
trivial; the minimal law is no tie-at-top within any member set, and the failure
message names the tied members). alloc: driver non-negative; per-member driver sum
strictly positive; normalization is the declared law, so stored pre-normalized
weights are rejected as derived truth.

**Disclosure (on the answer, always).** touch: the skew stated (total = k× the
grand total, k = the realized fan-out) and coverage. assign: the shadow (how many
memberships were not represented). alloc: the driver's name, and the
**reconciliation badge** — see §5. All three inherit the crossed-grain absence law
(uncovered shortfall travels).

## 5. The commutation classification

Draw the frontier square for a measure m and face f: aggregate-then-align (the
grand total) versus cross-then-aggregate (the per-member totals, summed).

- **touch — EXCEEDS.** The square deliberately does not commute; the face's honesty
  is *stating the excess as the fan-out it is*. Cascadia E10: touch total = 1.44 ×
  grand total = 870 memberships / 600 products, exactly.
- **assign — REDISTRIBUTES.** The square commutes in total (single-counting
  preserves mass) while moving value between members; the honesty is the shadow
  (Cascadia: 270 memberships unrepresented).
- **alloc — COMMUTES.** Where the driver covers, splitting preserves mass
  everywhere; the badge is a **commutation certificate**, provable per answer.

This is the paper's central figure: the three faces are not an arbitrary verb list
but **the three canonical answers to "does the frontier square commute?" — exceed,
redistribute, commute.** (Class-4/distinct measures ride `.touch` because their
anchor is exhausted at the member set — a corollary to prove, not a rule to
assert.)

## 6. Open residue (honest, and the paper says so)

1. **Face chains.** A crossed result crossing a second frontier: anchor rewriting
   composes mechanically; disclosure *stacking* (a skew atop a badge) needs design
   before multi-hop crossings are licensed.
2. **Conformity drift.** P1's failure mode: two levels declared shared that are
   almost-but-not identical. Alignment needs its own adjudication (conformance
   proofs at publish), or drift reintroduces silent failure through the front door.
3. **Distinct-class measures at frontiers — RESOLVED (2026-07-24)** by the
   traversal-modes settlement in §4 (value-traversal refused by spent anchor;
   population-traversal licensed for union/route, undefined for scale). What
   remains is only the formal write-up as the companion paper's second lemma.
4. **The face generator.** Declaration-by-pattern over declared driver measures,
   expanded and adjudicated at publish (never resolved at query time): the lawful
   form of dynamic vocabulary. Designed; rows for 0.13.

## 7. What ships against these notes (the addendum's contract)

0.12: the third Cascadia universe (`category_profile` = category, BASIS spine;
measures `priority`, `alloc_weight` VALUE-style) · FACE grammar `<name> = ASSIGN BY
<measure-ref>` / `ALLOC BY <measure-ref>` (names carry no operational meaning;
drivers are measure references, either grain) · publish-time adjudication and
acyclicity per §4 · disclosures per §4–5 including the reconciliation badge on the
wire · exhibits E11 (assign: total ≡ grand total; shadow 270) and E12 (alloc:
total ≡ grand total to the cent; badge) beside E10's 1.44× · the three-deep clarify
menu on the bare ask · manual: the triad chapter replaces the declared-but-deferred
refusals · ledger: dated re-sequencing note (triad completion ahead of OF-13, with
reasons) and a new row for these notes as the Two-Anchors sequel.

*— the desk*
