# ADR-031: Columna Core Architecture — the Column-Processing Foundation

**Status:** Proposed (captured from design session; supersedes the structural decisions of ADR-030)
**Date:** June 2026
**Track:** Runtime / implementation. ADR-030 specified a single-table *kernel* that validated correctness mechanics (disclosure propagation, anchored cache, sketch reaggregation, pre/post-agg boundary, EXPLAIN). This ADR specifies **Columna Core** — the full open-source product — on the correct foundation. The kernel's *techniques* survive; its *structure* (single denormalized table, table-level operations) is replaced.

---

## Context and the correction this ADR records

The ADR-030 kernel assumed a single denormalized table and, to relate tables, would have compiled a frame into one SQL statement and pushed it down. **That is text-to-SQL with a governance wrapper** — the exact architecture Columna exists to replace. Correctness that lives in generated SQL makes us a *linter on a permissive language*; the thesis is that we are the *type system beneath it*. This ADR re-grounds Core so that the column-processing foundation is honored everywhere, not rhetorically.

**The foundational commitment (D1).** The column is the atom. Table-level operations — joins above all — are **not primitives** in Columna; they are *claims about how column-atoms relate* (the relationship/anchor structure). Therefore:

> **The backend is asked only to *deliver* columns, never to *combine* them.** No generated joins, no multi-table SQL at query time. Every relating of columns across anchors happens *inside the column engine*, as an explicit anchor-aligned **transport** operation governed by the relationship structure — where the wrong computation is *inexpressible*, not *caught after the fact*.

The only place table-level reasoning is permitted is **Discovery** (authoring), whose entire job is to *dissolve tables into column-atoms* and produce the Manifold spec. After publish, tables do not exist for the runtime — only column-atoms, anchors, relationships, and universes.

**Why single-backend enables this rather than excusing the opposite.** With one engine and modest data, the column engine can afford to fetch anchored columns and relate them itself — the expensive thing federation cannot afford. Single-backend is the *budget* that lets Core honor the column foundation honestly. It is **not** a license to push joins down. (Federation — moving data between engines — is exactly what Pro adds, and exactly the hard part Core omits.)

---

## The Core / Pro line (sharpened)

**Core is the full framework, restricted to:** one backend at a time (DuckDB first), one machine (self-hosted, single process acceptable), a fixed-but-complete algebra (standard aggregators; the map/reduce/broadcast/ordering operator-kinds; a fixed type set), and a *crude-but-real* cost model. Everything else is in scope: multi-table Manifolds, universes, V/M/B anchors, measure families, relationships with cardinality, coverage/staleness/as-of, full disclosure, Frame-QL, authoring, EXPLAIN.

**Pro adds (out of scope here):** multiple backends / federation; cloud hosting; custom operators and data types; sophisticated cost-based optimization (statistics, adaptive plans, materialization advice, summary-routing); and **allocation** (the declared split that answers "revenue *attributed* across an M:N relationship").

**The non-negotiable:** the differentiator — column-atoms related by transport, with fan-out and bad reaggregation *inexpressible* — is a **Core** commitment, present in the free tier from line one. If joins-pushed-down were Core, then Core would be text-to-SQL and Pro would be "our real idea, later," which is backwards and fatal. *The differentiator must be in the free tier or it is not a differentiator.* "Not optimized" means Core may always do the simple correct thing (e.g. aggregate-at-home-anchor before relating) even when slow.

---

## The Manifold object model

### A Manifold is one closed space over many tables (D2)

**One Manifold spans many tables; it is not one-Manifold-per-table.** `revenue` (from transactions), `region` (from stores), `level` (from eom_inventory) are all column-atoms in *one* Manifold. Tables are merely where atoms physically reside; the Manifold is the unified queryable space.

**A Manifold is a closed, declared vocabulary — an allowlist.** Nothing in the backend is reachable unless the spec names it. This closure is a feature, three ways: (1) it *is* the relocated curation surface (author one Manifold, not bless metrics one-by-one); (2) it makes correctness **decidable** — the engine reasons over a finite declared set of atoms with known anchors and faithfulness rules, which is what lets "the bad answer is inexpressible" be true (an unbounded vocabulary cannot be governed); (3) it is the **access boundary** — a physical column not admitted to the spec is *invisible*, not "available but unused." Availability is defined by **exposure**, not physical existence.

### The spec is a graph of typed objects, seen through two projections (D3)

The spec is **not** a flat column list. It is a graph of typed objects: **anchors** (coordinates), **columns** (atoms: dimension / measure-with-family / attribute / derived), **relationships** (the connection), and **universes** (scoped populations). It is consumed through **two projections via two APIs**:

- **The planner's *vocabulary/shape* projection:** which columns exist and their kind; anchors and their rollups; derived-column defining expressions; types for expression validation; and **enough of the relationship graph to typecheck transport** ("can column X reach anchor Y along functional edges?"). It does **not** expose provenance.
- **The engine's *resolution* projection:** stored-source bindings, per-source caveats, physical column mappings, faithfulness rules, costs.

This is not merely access hygiene. **A layer can only disclose or refuse what its projection lets it see**, so the projection boundary *forces* every disclosure and refusal to be emitted by the epistemically-correct layer (below). It is impossible to put a caveat in the wrong place because the wrong layer lacks the information to fabricate it.

### Anchors (D4)

An anchor is a **named coordinate realized by base column(s)**. `name` is the logical identity in the Manifold's vocabulary; `column(s)` is the physical realization. They differ whenever the physical name is non-business, the same dimension is realized by different columns in different tables, or two anchors share a column type but mean different things (`ship_date` vs `order_date`). Anchors form an **FD rollup hierarchy** (`day → week → month → quarter → year`; `store → region`) — the functional parent each anchor determines, which is what permits coarse-from-fine reduction. *Correction from the kernel:* an anchor is realized by a **tuple of columns** (compound keys), not a single column.

### Columns, and the measure-column with its family (D5)

Columns come in kinds: **dimension** (addressable coordinates), **measure** (quantities), **attribute** (displayed, not addressed), and **derived** (defined by an expression over other columns — first-class members of the same closed vocabulary; a derived column is also a conscious admission to the allowlist).

A **measure-column carries a family of admissible aggregations**, each with its own B-anchor — the column-as-atom thesis made literal. From the `.cf`: `level` is one column whose family is `{ last, avg, sum:non-reconciling }`, each blocked over `day`. A Frame-QL reference is therefore **(measure-column, family-member) @ anchor** — `level.last @ month` is fine; `level.sum @ month` is refused (non-reconciling over the day axis). The kernel's flat "one Metric = one column + one aggregator" is wrong; the correct model is column-centric, and a kernel-style metric is a *compiled view of one family member*.

Two reductions the `.cf` got wrong, now corrected:

- **No stock/flow/rating column *type*.** "Stock vs flow" is a global label pretending a column has one aggregation personality, but additivity is **per-(dimension, operator)** — exactly what the **B-anchor** expresses and the label cannot. The type is not just redundant, it is *less expressive and can be wrong*. Drop it; keep the B-anchor. Measurement scale (ordinal, etc.) likewise collapses into family admissibility — "ordinal ⇒ avg is suspect" is just "the family is `{median, mode}`, not `{avg}`."

- **`M_ANCHOR` is a set of columns, not a label.** Missingness regime is *read off* the set's membership: empty → **MCAR**; other columns → **MAR** (MCAR conditional on them); contains the column itself → **MNAR**. The mechanism is structural, parallel to the B-anchor — don't label the behavior, specify the structure that produces it. MNAR then *automatically* taints any average with a selection-bias disclosure.

### Relationships — functional edges only (D6)

Relationships are edges in the connection graph carrying cardinality. **Only constraining (functional) edges are declared** — `N:1`, `1:1` — the directions that permit faithful transport. **`M:N` is the default**, the *absence* of a functional edge; declaring it would be declaring "nothing is true here." So the graph is sparse (functional edges only), and a non-functional relating is recognized by the *absence* of a functional path. **No allocation operator in Core** — the declared split that would make M:N relating meaningful is a Pro feature; absent it, non-functional transport is simply inexpressible.

### Universes — the domain (D7)

A **universe is the domain on which column-functions are defined**: a set of points, each a tuple of anchor-coordinate values. It is the **product of its anchor-dimensions *restricted by a predicate*** — `store_days = stores × calendar WHERE day >= opened_date`. The predicate is not a filter; it *carves the real population out of the Cartesian grid*. Outside the universe a column is **not defined** (out-of-domain), categorically different from missing-and-imputable. Coverage and missingness operate only *within* the universe; the universe boundary is prior to them.

Invariants:
- **Universes are defined by dimensions and their attributes, never by measures.** A function cannot define its own domain. The predicate may reference dimension attributes (`day >= opened_date`) but never a measured quantity. This independence is what lets coverage/missingness be reasoned about apart from values.
- **One Manifold holds multiple universes that share some anchor-dimensions and differ in others.** `transactions` lives on `customer × store × product × day`; `eom_inventory` on `store × day`. They **share `day`** — and that shared anchor is precisely how a measure on one universe is related to a measure on another (cross-universe relating happens *along shared anchors*). This is the column-term expression of multi-table reality: tables become universes; a shared foreign key becomes a shared anchor-dimension. *(This also corrects the earlier "two Manifolds" error: it is one Manifold, two universes sharing `day`.)*
- **A measure binds to exactly one universe; transport is legal only to anchors that universe contains.** `inventory` (on `store × day`) may be addressed `@store, @day, @month, @region` but **not `@product`** — that is **out-of-domain**, a refusal distinct from the B-anchor's non-reconciling. Universes give a second inexpressibility orthogonal to the B-anchor: the B-anchor refuses *illegal aggregation within the domain*; the universe refuses *addressing outside the domain*.

---

## The layer architecture

```
Surfaces      Frame-QL API · interactive UI · AI-Agent-as-Analyst · MCP
                    │ frame query                              ▲ (frame, disclosure) | structured refusal
Planner       provenance-BLIND. parse sugar → canonical Op(col@in)@out; expand derived
              (recursively); TYPECHECK against vocabulary projection (column/anchor exists,
              transport well-formed, in-universe); request atoms from engine; evaluate
              expression over returned columns; assemble frame; fold disclosures.
              Emits: declared-universe-ambiguity disclosure; static refusals (fan-out,
              out-of-universe, unknown column) — dialog-capable.
                    │ canonical atom requests (col, family-member) @ out_anchor   ▲ (column, disclosure)
Column Engine the CENTER (per-Manifold). cache of anchored column-atoms + resolution
              & TRANSPORT algebra. For each atom: search FAITHFUL paths (cached / stored),
              pick cheapest by a crude cost model, transport along functional edges,
              co-compute the path's disclosure, optionally cache back. Recursive for derived.
              Emits: resolution-time disclosures (coverage misalignment); resolution refusals
              (no faithful path).
                    │ deliver column / relationship-column / keys (SINGLE TABLE only)
Connector     column DELIVERY only. never combines columns. capability-declared.
                    │
Backend       DuckDB (Core). raw data lives here; Columna never replaces or joins it.

— build-time, separate —
Discovery     the ONE table-level phase: dissolve tables into the column-space → Manifold spec.
```

### The connector — column delivery only (D1)

The connector's entire job is **delivering column-shaped things**: a column's values at an anchor; a **relationship-column** (the key→key mapping realizing an anchor rollup or a cross-anchor relation); distinct values; a profile; row keys. It **never combines** columns — no join, no cross-table group, no multi-table SQL. Its surface is small not as a simplification but because *relating is not its job — delivering atoms is*. Supported types are bounded by what the backend can deliver (which is why mergeable sketches the backend can't produce are built in the engine).

### The column engine — resolution and transport (D8, D9)

Per-Manifold. A cache of anchored column-atoms plus an algebra that does three column-processings, all anchor-aligned, none table-level: **aggregate within an anchor** (`Op(col@in)@out`); **transport across anchors** (relate columns along a relationship-column); **operate columns together** (map/reduce/broadcast/ordering).

**The resolution decision (the heart of Core).** For each requested `Op(col@in)@out`, the engine searches *faithful paths* and picks the cheapest:

- **Cached paths:** exact hit; coarse-from-fine reduction of a cached finer column; transport of a cached column along a cached relationship.
- **Stored paths:** deliver some stored column the connector offers (at some anchor), then transport/reduce to the target. Cost includes delivery; disclosure includes the source's caveats. The **raw floor** — a base column at its home grain — is always a deliverable stored path, so there is always ≥1 path (or an honest refusal).

Three properties make this safe and simple:

1. **Faithfulness is a precondition of candidacy, not a post-hoc check.** A cheaper path that would fan out, or sum a non-reconciling stock, **is not in the candidate set at all**. The optimizer only ever ranks *correct* options; it can never be tempted by a fast lie because the lie was never a candidate. If no faithful path exists → **refuse and disclose**.
2. **Disclosure is co-computed with the chosen path.** Different paths carry different caveats (stored → staleness; sketch → approximation; transport-across-unconfirmed-relation → taint). The cost decision and the disclosure are produced together. (Cheapest and cleanest-disclosure can differ; Core's default is cheapest-faithful, disclosing honestly.)
3. **Recursive for derived columns.** Resolving a derived `col@anchor` resolves its sub-columns `@anchor` by the same search — a small DAG, the engine's private business. The planner sees one column; the engine may walk a tree.

**Cached vs stored is the only dichotomy.** *Cached* = in the engine's own memory (warm, near-free). *Stored* = everything in the backend, **base column or pre-aggregated summary alike** — the connector flattens that difference; "table" is not a category the engine possesses. The engine learns the menu of deliverable stored columns (and the anchors/caveats they carry) **from the spec** (the closed allowlist via its resolution projection), not by interrogating the backend at query time. Cost model is **crude** in Core (round-trips, rows scanned — enough to prefer a cache hit over a 300M-row scan); sophisticated optimization is Pro.

**Transport — the move that replaces the join (D9).** To relate `revenue` (anchored at `store`) to `region` (a property of `store`): fetch `revenue` as a column-atom at `store`; fetch the `store→region` **relationship-column**; **transport** `revenue` along it to `region` — inside the engine. The backend delivered two columns and never related them. Transport is **defined only along functional edges** (`N:1`, `1:1` — the reducing direction; the value moves without replication = faithful). Along a **non-functional edge** transport has **no definition** (no single target point) and is therefore **inexpressible** — it does not typecheck. The relationship is itself just a column-atom (a key→key mapping) the engine transports along; relationships live in the column world like any other column.

### The planner — provenance-blind expression & assembly (D11)

Parses Frame-QL sugar into canonical `Op(col, family-member)@out_anchor`; expands derived columns into sub-column requests (recursively); **typechecks** against the vocabulary projection (column and anchor exist; the requested transport is well-formed along functional edges; the target anchor is in the measure's universe); requests atoms from the engine; evaluates the surrounding expression over the returned `(column, disclosure)` pairs; lays columns side-by-side into the output frame; folds per-column disclosures into the frame disclosure. It is **opaque to provenance** — it never knows or asks whether a column came from cache, stored delivery, or derivation; that opacity is what lets the engine change *how* it satisfies a request without affecting the planner. *"Frame = dataframe minus the data"* is literally this: the planner builds a shape from transported, operated column-atoms; the only table-shaped moment is final assembly, which is pure presentation.

### Surfaces and EXPLAIN

Surfaces (API / interactive / agent / MCP) sit on `(frame, disclosure)` and on structured refusals. **EXPLAIN is a first-class Core surface** (promoted), the *trust surface*: it shows, per requested atom, the chosen resolution path (cached / stored / transport / reduction), the faithfulness reasoning, the disclosures incurred, and any refusal with its named alternatives. Trust is the product; EXPLAIN is where it is made inspectable.

---

## Transport, fan-out, and the flagship demo (D9, D10)

**Fan-out** is a measure crossing a `1:N`/`M:N` edge in the expanding direction, so its value is **replicated per match and summed as if the replicas were independent observations** — `$100` across {Electronics, Sale, Clearance} becomes `$300`. It is a **grain violation**: `amount` is defined at exactly one point (its transaction); replication asserts it exists at three. It is therefore not "a join that double-counts" but **a transport with no valid target** along a non-functional edge.

**Fan-out is never a legitimate computation.** The legitimate *questions* nearby mean other, well-defined things: **allocation** (a declared split that conserves the total — Pro, not Core) or **membership** ("revenue *touching* each category" — a filtered measure that never leaves its home grain, where overlap is expected and correct). The framework's job is to refuse replicate-and-sum and force the choice between the honest readings.

**Surfaced at the planner, as a structured refusal (D10).** Fan-out legality is a **static** property of the cardinality graph — knowable from the spec before any data is touched — so it is the **planner's**, by the same epistemics that gave coverage to the engine. It is a **query-formation refusal**, not a disclosure: an inexpressible operation has no value to attach a caveat to. Catching it pre-resolution keeps the engine's contract pure (*every request the engine sees has ≥1 faithful path*) **and** makes it **dialog-capable** — the planner can return, while the user is still in the loop, "this has no faithful answer as posed; did you mean *attributed* (allocation, Pro) or *touching* (membership, rephrase)?" A refusal is first-class and structured — `{reason: non_functional_transport, measure: revenue@transaction, target: category, edge: transaction→category (M:N), alternatives: [allocation(Pro), membership(rephrase)]}` — a sibling of the disclosure type, so any surface can turn it into a conversation.

**The flagship demo.** `revenue by category` over the benchmark's M:N `product_categories`: text-to-SQL (and every governance-wrapper on it) returns **3× real revenue, silently, looking correct**; Columna **refuses with the reason**. Placed beside `revenue by region` (functional `transaction → store → region`, which transports faithfully and conserves the total), the contrast proves the refusal is **structural and surgical** — it refuses exactly the corrupt case and nothing adjacent. The only difference between the two queries is the cardinality of an edge. This is the single clearest screen-level proof that Columna is a different kind of thing than SQL-generation.

---

## Disclosure & refusal — layered emission by epistemics (D12, D13)

Hazards are surfaced by **whichever layer can first know, given its projection** — and in the form its knowledge supports.

**Two disclosure sites:**
- **Planner — declared/shape disclosures.** Visible statically from the spec, e.g. a frame whose columns belong to **different universes that don't coincide** → an *ambiguous-query* disclosure (about *intent*: the population is not well-defined). User-addressable: adding `ON UNIVERSE` discharges it.
- **Engine — resolution/coverage disclosures.** Visible only in resolution, e.g. two columns that nominally share the `customer` anchor but whose universes cover **different sub-populations** (engagement 11,338 / 20,000) → a *coverage* disclosure (about *fact*: the effective N of any cross-column op is the intersection, not the displayed union). **Not** addressable by rewriting — no syntax makes divergent coverage converge.

A frame may carry **both**; they compose. `ON UNIVERSE` discharges the planner's ambiguity but never the engine's coverage fact — an asymmetry that confirms they are different in kind.

**Two refusal sites (the parallel structure):**
- **Planner — statically inexpressible:** fan-out (non-functional transport), out-of-universe addressing, unknown column. Caught before the engine is asked; dialog-capable.
- **Engine — resolution-dependent inexpressible:** no faithful reaggregation/transport path given what is actually available.

**Implications for the object model (build these in):** refusals are first-class, **structured**, and carry **named alternatives** (so surfaces can open a dialog). And each column's disclosure returned by the engine must **name the population/universe it resolved over**, so the planner can fold a frame-level coverage picture from parts it did not (and cannot) compute.

**`ON UNIVERSE` (D13)** is the **population coordinate**, sibling of the `@anchor` addressing coordinate: `@anchor` says *where* the answer is addressed; `ON UNIVERSE` says *over what population* it is evaluated. Implicit when inferable (columns agree); explicit to pin the population or resolve ambiguity, in which case the engine *verifies* each column is transportable into it rather than *inferring*. **Default when universes partially overlap and no `ON UNIVERSE` is given: union-with-coverage-disclosure** — show the full population, mark out-of-domain nulls explicitly, never silently shrink the population the user didn't ask to shrink (silent narrowing to the intersection is itself a classic silent failure).

---

## Discovery — the one table-level phase (D14)

Authoring's Discovery is the **only** phase that operates on tables, *because its purpose is to dissolve tables into column-atoms*: read schemas, keys, FDs, inter-table relationships, profiles, and documentation; decide which columns become anchors, what each measure-column's family and M/B anchors are, which functional relationships connect anchors, and what universes scope the space. The output is the Manifold spec. **After publish, the table structure is fully absorbed; it is never consulted as tables again at query time.** Discovery is where tables go to become atoms.

Disciplines: **ingest-first** (Core v1 parses a written `MANIFOLD` definition and makes it fully queryable end-to-end; automated discovery is a *later* layer that *produces* such a definition — the language is the contract, discovery is a convenience); **progressive** (a minimal Manifold — base columns + catalog-derived anchors — queryable in minutes, enriched incrementally against a live object); **evidence-graded** (every proposed fact carries its grade — declared / proven / inferred-from-sample / inferred-from-docs — and that grade **flows into runtime disclosure**; load-bearing inferred facts require confirmation + a runtime guard); and **maximize the auto-proposed high-confidence fraction** (a measured objective, because "curation relocated, not abolished" is only true if discovery proposes most of the spec and the human confirms a minority).

---

## What survives from the ADR-030 kernel

As **technique, not structure**: the disclosure object + propagation algebra (now extended with the universe/coverage categories and the structured-refusal sibling); the anchored-aggregate cache with coarse-from-fine; the sketch reaggregation tier (HLL) with its error-bound-into-disclosure; the pre/post-aggregation arithmetic (now a property of the measure-family rather than a flat metric); the Polars reaggregation/operate kernel (now strictly *after* delivery — never relating); EXPLAIN; the single-Manifold server. Core wraps a *new front half* — schema/relationship graph, the transport-and-resolution engine, universes, measure-families, the two-projection spec, a definition-language parser, and the layered disclosure/refusal model — around these validated back-half techniques.

---

## Decisions (index)

- **D1** Column-processing foundation: backend delivers columns, never combines them; no table-level ops outside Discovery.
- **D2** One Manifold spans many tables; it is a closed allowlist vocabulary of column-atoms.
- **D3** The spec is a graph of typed objects, consumed via two projections (planner=vocabulary/shape, engine=resolution); the boundary forces epistemically-correct emission.
- **D4** Anchors = named coordinates realized by compound base columns, with an FD rollup hierarchy; `name ≠ column`.
- **D5** Measure-columns carry a *family* of aggregations (each with its B-anchor) and an *M-anchor set* (missingness structure); no stock/flow/rating type; references are `(column, family-member)@anchor`.
- **D6** Relationships declare functional edges only (`N:1`,`1:1`); `M:N` is the default (absence); no allocation in Core.
- **D7** Universes are domains: anchor-dimensions restricted by a predicate over dimensions/attributes (never measures); multiple per Manifold share anchors; a measure binds to one universe; out-of-universe addressing is a refusal.
- **D8** The column engine is the center: per-Manifold cache + cheapest-*faithful*-path resolution over cached/stored, faithfulness a precondition of candidacy, recursive for derived, crude cost model.
- **D9** Transport replaces the join: defined only on functional edges; non-functional transport is inexpressible; relationships are key→key column-atoms.
- **D10** Fan-out is caught at the planner as a structured, dialog-capable refusal naming neighbors; the engine never receives it.
- **D11** The planner is provenance-blind: parse → canonical, expand derived, typecheck, assemble, fold disclosures.
- **D12** Layered emission by epistemics: two disclosure sites (planner=declared/shape, engine=resolution/coverage) and two refusal sites (planner=static, engine=resolution-dependent); refusals are first-class and structured.
- **D13** `ON UNIVERSE` is the population coordinate (sibling of `@anchor`); implicit when inferable; default on partial overlap is union-with-coverage-disclosure.
- **D14** Discovery is the one table-level phase (dissolves tables into atoms); ingest-first; progressive; evidence-grade → disclosure.
- **D15** Core/Pro line: the column-foundation differentiator ships in Core (free tier); Pro = federation, cloud, custom ops/types, sophisticated optimization, allocation.

---

## Open questions / next steps

1. **Manual reconciliation (the immediate next document).** Several decisions here are *ahead of* the reference manual (M-anchor as a set; no stock/flow type; functional-edges-only relationships; measure-family as the central type; universes as first-class domains with `ON UNIVERSE`; the two projections; layered refusal). The next artifact is the **corrected Manifold object model**, and a decision is owed: does the manual become the source of truth the model reconciles *to*, or does this ADR become the new source of truth the manual later reconciles *to*? (Current lean: this ADR leads; the manual is updated to match, since the manual's reductions are what we corrected.)

   **Resolved (June 2026).** Direction confirmed as the lean: **this ADR leads; the manuals were updated to match.** Reconnaissance found the manuals already aligned on most of the list above (the rename/reposition passes had carried M-anchor-as-structure, the retired stock/flow type, universes/`ON UNIVERSE`, and measure-families across; the "two Manifolds" error was already avoided via universes). The reconciliation therefore reduced to: (a) naming **transport** and the connector-**delivers-columns-never-combines** contract (D1/D9), which the manuals expressed only unnamed ("ascription to a common anchor"); (b) naming **fan-out** and stating the **two projections** (D3) and the **differentiator-is-Core** commitment (D15); and (c) **one genuine doctrinal fork** — a many-to-many aggregate-across had been classified by *both* manuals (framework Ch 8; reference Ch 19.2, a deliberate ADR-020/025 inform-and-serve rewrite) as **serve-the-membership-aggregation-with-disclosure**, which **contradicts D10 and the shipping Core code** (which refuse/clarify). Ruled (Huayin): the bare aggregate-across is a **Clarify**, on the **determinacy principle** — *a request denoting exactly one number is served (disclosed if risky, as a B-anchor crossing is); a request denoting no single number among legitimate readings is clarified, never guessed* — with membership served only when *chosen* and allocation **[Pro]**. The detection is the **planner's** (static, from verified-at-publish cardinality); the separate declared-functional-but-data-violates case stays the engine's `CONTRADICTED` path. No code change was needed (the engine already behaves this way). Reconciled artifacts: **framework manual 6e**, **reference manual 5e**, both mutually consistent and consistent with the Core code; audit at `manual_adr031_reconciliation_audit.md`. The *corrected Manifold object model* (the document this question anticipated) remains the natural next write-up, now with the manuals as a reconciled source.
2. **The `.cf` `SUMMARY` reading.** Open from the session: is `SUMMARY` per-measure **V-anchor verification/attestation** (home anchor + defining aggregation + evidence grade) rather than a *materialized summary table*? If so, it folds into the measure-column object and removes the last table-level concept from the spec. To confirm before the object model is written.
3. **Relationship-column delivery.** The connector contract for delivering a key→key relationship-column (and how the engine caches and transports along it) needs concrete specification — the operational core of D9.
4. **Universe representation.** How universes are stored and evaluated (the predicate over dimension attributes), how the engine tests "anchor Y ∈ measure's universe," and how shared-anchor relating across universes is realized in transport.
5. **Measure-family typing and Frame-QL surface syntax** for `(column, family-member)@anchor`, `ON UNIVERSE`, and the structured-refusal/alternatives surface.

---

## Consequences

**Positive.** Core is honestly column-founded end-to-end: the only table-level reasoning is in Discovery; the only optimization in the engine is *choosing among correct paths*. The differentiator ships free. Fan-out becomes the flagship demo rather than a hidden correctness rule. The two-projection spec makes "the planner can't know provenance" a structural fact, not a convention, and makes mis-placed disclosures impossible. Universes give a second, orthogonal inexpressibility (out-of-domain) alongside the B-anchor (non-reconciling) and the relationship graph (fan-out) — three structures, three classes of inexpressible silent failure.

**Costs / risks.** Core is a substantially larger system than the kernel: a real definition-language parser, a relationship/transport engine, universes, measure-families, and the two-projection spec must all be built before it is queryable. The transport operation (D9) is novel engineering and the load-bearing piece. The column-foundation must be held religiously — the temptation to "just let DuckDB join, it's faster" will recur, and *that* is how the principle dies; the discipline is **the backend delivers columns, it never relates them.** "Not optimized" must not be allowed to mean "incorrect by shortcut": Core always has the simple correct path (aggregate-at-home-anchor before relating) available.

**Net.** This is the architecture that makes Columna a different kind of thing than text-to-SQL — column-atoms related by transport, with fan-out, bad reaggregation, and out-of-domain addressing all inexpressible — and it is the *Core*, free-tier commitment. The next move is the corrected Manifold object model, reconciled with the manual, then a module-by-module build reusing the kernel's surviving techniques against this written target.
