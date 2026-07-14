# The Columna Reference Manual

*Companion to the Columna Framework manual — the specification layer*

*Fifth Edition — reconciled through ADR-031 (the column-processing foundation: relating columns is **transport** along functional edges in the engine, the backend delivers columns and never combines them, **fan-out** is inexpressible, and a many-to-many aggregate-across is a **Clarify** rather than a defaulted membership). Renamed (framework → **Columna**, the data-space object → **Manifold**, the query language → **Frame-QL**, the definition-language keyword `COFRAME` → `MANIFOLD`) and repositioned through ADR-029.*

<!-- Reconciliation pass (Fifth Edition) against ADR-031 D1–D15, kept consistent with the framework manual Sixth Edition. Substantive changes, each marked inline: Ch 4.3 — relating along a roll-up edge is transport in the engine; the backend delivers columns, never combines them (D1/D9). Ch 19.2 — the membership aggregation over an unresolved many-to-many moved from "Serve, with disclosures" to "Clarify," on the determinacy principle (D10), superseding the ADR-020/025 default-to-membership reading; the B-anchor crossing remains serve-and-disclose. Ch 22.5 — the bare aggregate-across is a clarification; membership served only when chosen; allocation [Pro] (D6/D15). Appendix A — allocation bridges marked Pro (not Core), consistent with the registry chapter; the connector-delivers-never-combines contract stated (D1). Appendix B — transport, fan-out, and the M:N→Clarify reclassification added; watermark advanced to ADR-031. -->

---

## About This Manual

The *Columna Framework* manual explains why the system is built as it is — the ontology, the architecture, the reasoning behind every design choice. This companion does a different job. It sits one level below the conceptual manual and one level above the codebase, and answers the question a working author or integrator asks once the concepts have landed: *what, exactly, are the things — enumerated, categorized, with their precise properties — that I need to know to build and use Manifolds correctly?*

This is the specification layer: catalogs, taxonomies, type rules, behavioral contracts. It does not re-argue the philosophy (the conceptual manual does that) and it does not commit to implementation (the code does that). It specifies the contracts that sit in between, clearly enough to remove confusion for a working author, deliberately stopping short of exhaustive corner-case enumeration — the kind of detail that belongs in code and tests rather than in a manual a person reads.

Throughout, this manual presumes the concepts of the framework manual: columns as functions from a universe's points to values, the complete grain as the pair *(anchor, universe)*, the three operation kinds crossed with the order axis, families as a caching optimization with the fertile/mule distinction governing what can found a family, B-anchor and applicability, M-anchor and missingness, value determination, degeneracy, defining boundaries, and the Manifold as complete structure. Terms are used here as they are defined there. The outcome discipline is the inform-and-serve model throughout (ADR-020): analytical risk is disclosed on served results or dissolved by disclosed route-arounds; a result is withheld only for clarification, absent data, or a human rule. <!-- X1 --> ADR-031 sharpens two things this manual now reflects: relating columns across anchors is **transport** along functional edges *in the engine* (the backend delivers columns and never combines them; Chapter 4.3), and the one place the inform-and-serve default does *not* apply — aggregating a measure across a non-functional edge — is reclassified as a **Clarify**, because the operation is inexpressible (**fan-out**: no single target, hence no single number), not merely risky. The determinacy principle that governs the choice — one number → serve (disclose if risky); no single number → clarify — is specified in Chapter 19.2. <!-- ADR-031 D1/D9/D10 -->

## Contents

- **Part I — Types and Operators.** The logical type system and the operator catalog (with the operator × backend capability matrix as Appendix A).
- **Part II — Anchors and Dimensions.** What an anchor is, how dimensions play their role, how dimension families and roll-up edges are declared and verified — including time-varying functional dependencies.
- **Part III — Applicability, Missingness, and the Universe.** The B-anchor and M-anchor, the column-spec and the operator registry, and the universe: declaration, derivation, co-universality, and verification by basis.
- **Part IV — Degeneracy and Coverage.** Coverage taxonomy, the universe-integrity machinery with co-universality as its object, and how coverage enters query planning.
- **Part V — Composition.** Inheritance and joining, versioning, what composition preserves.
- **Part VI — Integrity.** The layered preconditions (including coordinate totality), the certificate, the outcome discipline — serve, disclose, clarify, inform — and the framing of integrity as data soundness.
- **Part VII — Authoring.** Task and artifacts, and the four categories of authoring work — scoping, decisions and choices (beginning with the universe decision), confirmation, and tools.
- **Part VIII — The Definition Language.** The semantics of every definition construct, the chapter the Frame-QL BNF's §3 points to.
- **Appendices.** The operator × backend capability matrix, and the terminology concordance across the project's renames.

---

## Part I — Types and Operators

### Chapter 1. The Logical Type System

#### 1.1 Columna defines its own types

A value in a Manifold has a type, and Columna's type system is its own. This is a deliberate position, consistent with the framework's architectural stance: the substrate owns its logical concepts and treats the execution engine as an implementation it binds to, not an authority it inherits from. The current implementation executes on Polars, and every Columna logical type maps onto a Polars type for execution — but the logical type is defined by what it *means* in the substrate and how it interacts with families, anchors, and applicability, not by how Polars stores it. If the engine changed, the logical types would not.

This matters in practice because it lets the type system make choices an engine-driven type system cannot. The clearest example is storage width: Polars distinguishes `Int8`, `Int16`, `Int32`, `Int64` because those are different storage layouts, but an analytics author reasoning about a quantity does not care, at the logical level, whether a count is stored in 32 or 64 bits — they care that it is an integer, and perhaps about its range. Storage width is a *binding* concern, resolved when a logical column is bound to physical data, not a *logical* property of the quantity. Columna's logical type system is, where it can be, width-agnostic: it offers logical types that capture meaning, and defers storage representation to the binding layer.

The principle for the whole type system: **a logical type captures what a value means for analysis; representation choices that exist only for storage efficiency belong to binding, not to the logical type.** Where Polars' conventions reflect logical meaning, Columna adopts them. Where they reflect storage mechanics, Columna abstracts them into the binding layer. Where Columna needs types Polars lacks, it defines them outright.

#### 1.2 The scalar logical types

**Integer.** A whole-number quantity. Columna offers a single logical `Integer` type rather than the width-and-signedness family Polars exposes. An author declares a column as `Integer`, optionally with a declared range (which the integrity layer can verify and the binding layer can use to choose a physical width). Signedness and width are binding concerns. At the logical level there is no analytical difference between a count stored as `UInt32` and one stored as `Int64`; the difference is entirely about storage, and surfacing it as a logical-type distinction would force authors to make storage decisions dressed as modeling decisions.

**Decimal.** An exact fixed-point numeric, declared with precision and scale. This is the type for monetary and other quantities where binary floating-point error is unacceptable. Columna treats `Decimal` as logically distinct from `Float` precisely because the distinction is *logical*, not merely representational: a quantity that must be exact (money) is a different kind of thing for analysis than a quantity that is inherently approximate (a measured rate), and conflating them invites real errors. Precision and scale are part of the logical type because they affect meaning (what values are representable, how rounding behaves), unlike integer width which does not.

**Float.** An approximate real-valued quantity. Columna offers a single logical `Float` rather than `Float32`/`Float64`; the precision of the binary representation is a binding concern. `Float` is the type for inherently-approximate measurements, computed ratios, and the like. The logical contract is "real-valued, approximate"; the binding chooses the physical precision.

**Boolean.** A truth value. Adopted as-is; there is no logical/storage tension here.

**String.** A textual value. The general type for free-form text. Where a string-valued column has a *closed, declared domain*, the `Enumerated` type (Chapter 1.3) is preferred — see that section for the relationship.

**Hash.** An opaque equality-comparable identity token — a value used to identify or compare without revealing or interpreting the underlying content. Hashes appear naturally in privacy-sensitive contexts (hashed customer identifiers used as join keys without exposing the raw IDs), in deduplication, and in opaque identity tokens generally. The logical character is equality-only: hashes compare by equality, are not ordered, are not summable, and carry no arithmetic. Their natural reducers are `COUNT`, `COUNT_DISTINCT`, `LAST`/`FIRST`; arithmetic reducers do not apply. Hash is a logical type because its character — opaque equality-only identity — is logical, not merely a storage choice.

**Date, Timestamp, Duration, Time.** Temporal types, adopted in shape from Polars but with precision abstracted. Polars encodes time resolution into the type (`Datetime[μs]`, `Duration[ns]`); Columna treats resolution as a property of a temporal column rather than a distinct logical type, for the same reason it abstracts integer width — resolution is a representation choice. The four temporal types are logically distinct because they *mean* different things: `Date` is a calendar day, `Timestamp` is an instant, `Duration` is an elapsed quantity, `Time` is a time-of-day. `Timestamp` carries an optional time zone as a logical property, because the zone genuinely affects meaning. `Duration` has a special relationship to the ordered operations (it is what time-differences produce and what windows are measured in), noted in the operator catalog.

These scalar types divide, for the purposes of the family machinery, along the line that matters most: which are *quantities that can be aggregated arithmetically* (Integer, Decimal, Float, Duration) and which are *labels or coordinates* (Boolean, String, Enumerated, Hash, Date, Timestamp, Time — though these can be reduced by order-dependent or counting reducers, they are not summed). This division is not a separate type attribute; it falls out of which families a column of each type can sensibly carry, and it is enforced through the family set rather than declared on the type.

#### 1.3 The closed-domain type: Enumerated

A frequent and important case: a column's value space is a *closed, declared set* — region is one of `{NA, EMEA, APAC, LATAM}`, order status is one of `{pending, fulfilled, cancelled}`. This finite-closed-domain property is logical (it affects which values are valid, enables completeness checking, and pairs naturally with the dimension role), and Columna gives it a dedicated logical type:

**Enumerated.** A value drawn from a declared closed set. Each Enumerated column declares its domain — the set of valid values. The framework verifies, at refresh, that the data contains only values from the declared domain (validity checking), and supports completeness checking against the domain (which declared values are present, which are absent).

Enumerated is the appropriate type for dimensions with known finite value sets — which is most dimensions of business categorization (region, status, segment, channel, tier). Such columns can be declared as `String`, but `Enumerated` is the more precise type when the domain is genuinely closed and known, because it lets the framework verify validity and support completeness, neither of which is possible with open-domain `String`.

A note on Polars' Categorical/Enum distinction: Polars distinguishes these as encoding mechanics (both dictionary-encode strings, differing in how the dictionary is managed). Columna's `Enumerated` type captures the *logical* property — a closed declared domain — while the *encoding* choices (how the value is stored physically, which dictionary structure is used) are binding-layer concerns. So Columna's `Enumerated` is not a one-to-one mapping of Polars' `Categorical` or `Enum`; it is the logical type that *uses* one of those encodings as implementation. The logical/storage distinction holds here as elsewhere.

#### 1.4 The nested types

Polars offers `List`, `Array`, and `Struct`. Columna adopts these in shape, but they should be understood for what they are in the substrate — container types for genuinely structured data — rather than as load-bearing machinery for the family system.

**List** is a variable-length sequence of values of one type. **Array** is a fixed-length sequence. **Struct** is a tuple of named typed fields. They are adopted as container types where the source data carries such structures, and they are valid value types for columns whose data is genuinely list-, array-, or struct-shaped.

A point worth clarifying, because an earlier draft of this manual got it wrong: nested types — particularly `Struct` — are *not* the carriers of "mule families." The framework manual establishes that mules are not families (families exist as a caching optimization over the always-correct root-recomputation; mules are computed at presentation from fertile sources and are not materialized as re-aggregable families at all). A mean is not "carried as a Struct(SUM, COUNT) family" — there is no mean family. A mean is computed at presentation from the `SUM` and `COUNT` families, each of which is a fertile family in its own right. Struct does not serve as a mule-family carrier because mule families do not exist. The genuine fertile-family carriers are the sketch types of the next section, which are different — they really are fertile monoids and really do found families.

#### 1.5 The sketch types

Here the type system extends beyond what Polars provides, because the sketch types are Columna's own, defined to serve a specific role: they are the value types that make reducers *that would otherwise be sterile* into *fertile family-bearers*. Exact distinct-count and exact quantiles are mules — they cannot be re-aggregated up the lattice, because re-aggregation would require the full source set. Their *approximate* forms, carried as sketches, are different: the sketch itself is a fertile commutative monoid (sketches merge associatively and commutatively, and the merged sketch is a valid sketch of the union), so a sketch-valued column does found a family that re-aggregates by merging. The estimate is extracted at presentation; the family is sketches all the way through.

Each sketch type specifies three things: its **parameters** (which govern accuracy and size), its **merge semantics** (how two sketches combine — this is the monoid operation that makes the family fertile), and its **presentation** (how a final estimate is extracted from the sketch — the mule produced only at the end).

**HLLSketch** — a HyperLogLog sketch, the carrier for approximate distinct-count. Parameter: precision (governing accuracy/size). Merge: register-wise maximum — idempotent and commutative, making it not merely fertile but *robust to overlap* (merging a sketch with itself changes nothing, so duplicates across partitions do not corrupt the estimate, unlike a sum). Presentation: the bias-corrected cardinality estimate. An `APPROX_DISTINCT` reducer produces a column whose values are `HLLSketch`s; the sketch column founds a fertile family; the estimate is extracted only at presentation.

**TDigestSketch** — a t-digest, the carrier for approximate quantiles (median, percentiles). Parameter: compression (governing accuracy/size). Merge: t-digest merge (combining centroid sets). Presentation: a quantile estimate at any requested rank. An `APPROX_QUANTILE` reducer produces a column of `TDigestSketch`s.

**CountMinSketch** — a count-min sketch, the carrier for approximate frequency/heavy-hitter estimation. Parameters: width and depth (governing accuracy/size). Merge: element-wise addition of the count matrices. Presentation: an estimated frequency for a queried key.

The sketch types share a structural shape that the family machinery exploits: each is a fixed-size carrier with a commutative-monoid merge and an estimator for presentation. This is exactly the (carrier, merge, present) pattern that any fertile family follows — `SUM` is the trivial case where the carrier is the value, merge is addition, and presentation is identity; the sketches are the rich case where the carrier is elaborate and presentation is an estimator. The sketches are, in effect, type-level proof that the carrier-merge-present pattern generalizes to operations whose value-level result would not be re-aggregable.

A note on **sketch parameter compatibility**: two sketches merge only if their parameters are compatible (same HLL precision, compatible t-digest compression). The framework treats sketch parameters as part of the type identity for merge purposes, and verifies compatibility before merging. Where a sketch supports lossy parameter reduction (HLL can reduce precision; t-digest can be further compressed), the framework may reconcile mismatched parameters by reducing the finer to the coarser before merging — making sketch parameters a small refinement order rather than a hard equality. The specifics of automatic reconciliation belong to the operator-level facts the framework carries about each sketch type; the point here is that parameters are part of type identity for merge.

#### 1.6 The complete logical type list

| Logical type | Carries | Notes |
|---|---|---|
| `Integer` | whole-number quantities | width abstracted to binding; optional declared range |
| `Decimal` | exact fixed-point quantities | precision and scale are logical (affect meaning) |
| `Float` | approximate real quantities | binary precision abstracted to binding |
| `Boolean` | truth values | adopted as-is |
| `String` | open-domain textual values | for closed declared domains, prefer `Enumerated` |
| `Enumerated` | values from a declared closed domain | enables validity and completeness checking; natural type for dimensions with known finite value sets |
| `Hash` | opaque equality-only identity tokens | no arithmetic; reducers are equality-based and counting |
| `Date` | calendar days | |
| `Timestamp` | instants | optional time zone is logical; resolution abstracted |
| `Duration` | elapsed quantities | special role in ordered operations |
| `Time` | times of day | |
| `List` | variable-length sequences | container type for genuinely list-valued data |
| `Array` | fixed-length sequences | container type for fixed-length sequence data |
| `Struct` | tuples of typed fields | container type for genuinely structured data |
| `HLLSketch` | HyperLogLog state | fertile-family carrier for approximate distinct-count; overlap-robust |
| `TDigestSketch` | t-digest state | fertile-family carrier for approximate quantiles |
| `CountMinSketch` | count-min state | fertile-family carrier for approximate frequencies |

The divergences from Polars are deliberate and of three kinds: *abstraction* (integer width, float precision, temporal resolution moved to binding); *relocation* (the encoding mechanics of Polars' Categorical/Enum moved to binding, with the logical closed-domain property captured by the dedicated `Enumerated` type); and *extension* (the `Hash` type for opaque identity tokens, and the sketch types as fertile-family carriers, all of which Polars lacks).

---

### Chapter 2. The Operator Catalog

Operators are the concrete functions that realize the operations. The framework manual established the operation *kinds* — map, aggregate, broadcast, crossed with the order axis — and the reducer properties — fertile (founds a family) versus mule (computed at presentation from fertile sources, never materialized as a family). This chapter catalogs the operators themselves, organized by operation kind, each with its property signature.

#### 2.1 Reducers (the aggregate operation)

Reducers are the operators of the aggregate operation: they coarsen the anchor by combining many values into one. The framework manual established that reducers are classified along two independent axes — order-dependence and path-invariance — and that the second determines whether the reducer founds a family. This is the complete catalog by those axes.

**Fertile, order-independent reducers.** These are the commutative monoids: the ideal reducers, family-bearing, re-aggregable up the lattice in any order and any grouping.

| Reducer | Applies to | Notes |
|---|---|---|
| `SUM` | Integer, Decimal, Float, Duration | the canonical fertile reducer; carrier is the value itself |
| `COUNT` | any | counts present values; carrier is an Integer |
| `MAX` | ordered types | idempotent monoid; robust to overlap |
| `MIN` | ordered types | idempotent monoid; robust to overlap |
| `PRODUCT` | Integer, Decimal, Float | fertile but watch for overflow/zero |
| `BOOL_OR` / `BOOL_AND` | Boolean | logical OR / AND monoids |
| `APPROX_DISTINCT` | any | fertile *via* `HLLSketch` carrier; overlap-robust |
| `APPROX_QUANTILE` | ordered types | fertile *via* `TDigestSketch` carrier |
| `APPROX_FREQUENCY` | any | fertile *via* `CountMinSketch` carrier |

The three `APPROX_*` reducers are fertile not because the *estimate* is a monoid (it is not) but because the *sketch* is; they produce sketch-valued columns that carry up the lattice and present the estimate at the end. This is the type-level reason the sketch types exist.

**Order-independent mules.** Order does not matter, but the result is not path-invariant: it cannot be re-aggregated up the lattice. A mule is computed at presentation from fertile sources where possible; it is not materialized as a family.

| Reducer | Computed at presentation from | Notes |
|---|---|---|
| `AVG` | `SUM` and `COUNT` families | the canonical mule; present as `SUM / COUNT` |
| `WEIGHTED_MEAN` | `SUM(value·weight)` and `SUM(weight)` families | present as ratio at the final grain |
| `VARIANCE` / `STDDEV` | `COUNT`, `SUM`, `SUM_OF_SQUARES` families | computed at presentation |
| `COUNT_DISTINCT` (exact) | — | true mule with no fertile decomposition; cannot re-aggregate; use `APPROX_DISTINCT` if re-aggregation needed |
| `MEDIAN` (exact) | — | true mule; use `APPROX_QUANTILE` if re-aggregation needed |
| `MODE` | — | true mule |

The pattern is sharp. A mule whose value-level reduction can be expressed as a function of *fertile* reductions — `AVG` as `SUM / COUNT`, `VARIANCE` from count/sum/sum-of-squares — is handled by computing the fertile parts (each its own family) up to whatever grain the query needs, then computing the mule at that grain at presentation. There is no average family; there is a `SUM` family and a `COUNT` family, and the average is what you get by dividing them at the end. A mule with no fertile decomposition — exact distinct-count, exact median — is a genuine dead end: it is correct at the grain it is first computed and cannot be re-aggregated. For the framework to handle such operations across the lattice, use the approximate counterparts, which have genuine fertile carriers (the sketches).

**Fertile-along-their-order reducers (ordered).** These require an order to be defined, and are path-invariant *along that order*. They are the reducers a semi-additive stock needs for its time-collapse.

| Reducer | Requires | Notes |
|---|---|---|
| `LAST` | an order | the closing value; path-invariant along its order (last-of-lasts is the global last) |
| `FIRST` | an order | the opening value; path-invariant along its order |

`LAST` and `FIRST` are the answer to "how do I collapse a semi-additive stock over time" — the family manual's example of the inventory balance whose `SUM` is forbidden along the time axis (sum B-anchor includes time), but whose `LAST` *is* applicable along time precisely because it respects time's order. They are well-formed only with an explicit order; without one, the missing order is a clarification, asked rather than guessed. <!-- X1: ADR-020 -->

**Order-dependent mules.** Require an order and are not path-invariant by any route — genuinely sterile and order-bound.

| Reducer | Notes |
|---|---|
| `VALUE_AT_MAX` / `VALUE_AT_MIN` | the value of one column at the point where another is extremal; needs the full set; sterile |
| `NTH` | the value at a given ordinal position; sterile |

These have their uses but cannot found families and cannot be re-aggregated; the framework treats them as terminal.

#### 2.2 Map operators (anchor-preserving, order-independent)

Map operators preserve the anchor and transform values point by point, depending only on the inputs at each point. They are the largest and most familiar category. Multi-column maps require their operands to be co-anchored; cross-anchor combination is composition (bring to common anchor first, then map), not a primitive operation.

**Arithmetic** — `+`, `-`, `*`, `/`, `%`, unary `-`. Operate on numeric and (where meaningful) Duration types.

**Comparison** — `=`, `!=`, `<`, `<=`, `>`, `>=`, `between`, `in`. Produce Boolean. Defined on ordered types for the inequalities, on any type for equality.

**Logical** — `and`, `or`, `not`. Operate on Boolean.

**Conditional** — `if(predicate, then, else)`, `case … when … then … else … end`. Select among values by predicate.

**Null/missing handling** — `is_null`, `is_missing`, `coalesce`. Interact with the M-anchor; `is_missing` is the framework's missingness-aware predicate, distinct from a mere null check.

**Numeric functions** — `log`, `exp`, `sqrt`, `abs`, `sign`, `ceil`, `floor`, `round`. Note that several change the additivity character of a quantity — `log` of an extensive quantity is no longer extensive — which the B-anchor-propagation rules account for.

**String functions** — `concat`, `substring`, `lower`, `upper`, `trim`, `length`, and the like.

**Temporal functions** — `year`, `month`, `day`, `week`, `quarter` (extracting coarser temporal components, connecting to dimension-family climbs), `date_diff` (producing a Duration), `date_add`. Operate on temporal types.

A map operator may change a column's composition properties because it can change what kind of quantity the column is — `revenue` is extensive, `revenue / prior_revenue` is intensive. The framework recomputes B-anchor on derived columns rather than inheriting blindly.

#### 2.3 Scan operators (order-dependent maps)

Scans preserve the anchor but compute each point's value from an ordering and from neighboring points. They are well-formed only with an explicit order; the framework derives it from the anchor when the anchor contains an orderable axis (so `cumsum(revenue) @ {customer, day}` partitions by customer and accumulates over day), or takes an explicit order specification otherwise.

| Scan | Produces | Notes |
|---|---|---|
| `cumsum`, `cumprod`, `cummin`, `cummax` | running aggregates | prefix-accumulation of the corresponding fertile reducer |
| `rolling_sum`, `rolling_mean`, `rolling_min`, `rolling_max`, `rolling_count` | windowed aggregates | require a window specification |
| `lag(col, n)`, `lead(col, n)` | shifted values | the value n positions earlier/later in the order |
| `rank`, `dense_rank`, `row_number` | ordinal positions | the position of each point in the order |
| `pct_change` | relative change | the fractional change from the previous point |
| `ewm_mean` | exponentially-weighted mean | a smoothed running average |

#### 2.4 Broadcast (the anchor-refining operation)

Broadcast refines the anchor by making each coarse value available at the finer points beneath it. The dual of aggregate. Its single discipline is **replicate-only**: each finer point receives the *same* coarse value, regardless of whether the value is intensive or extensive.

This is a deliberate narrowing from earlier drafts of this manual, which split broadcast into a "replication" form for intensive values and an "allocation" form that *apportioned* an extensive total across finer points. The v4 operator model drops the apportioning form. Broadcast does not distribute a total; it spreads a value down so it can be *compared against* finer quantities — the canonical use being a share-of-total computation, where a region-grain total is broadcast to store grain and each store's value is divided by it (`store_value / region_total`) to get a share. The result of a broadcast is never summed back up as though it were a finer-grained extensive quantity; doing so would double-count the replicated value once per finer point.

**The double-count guard is structural, not a rule the author must remember.** A broadcast value carries, in the B-anchor of any reducer that would sum it, the dimension family it was broadcast along. Re-aggregating the broadcast region-total back across stores is therefore caught at plan time by the ordinary applicability check (Chapter 6) and can never happen silently — the same critical-disclosure machinery that guards summing a semi-additive stock across time. There is no allocation rule to supply and none to get wrong; the guard is the B-anchor on the broadcast dimension. <!-- X1: ADR-020 -->

**Allocation is a separate mechanism, for many-to-many — not for broadcast.** Apportioning a total by a partition-of-unity weighting still exists in the framework, but it belongs to the many-to-many *aggregate-across* case, not to broadcast. When a fine entity belongs to several coarse buckets (a product in several categories) and per-bucket totals must reconcile to the grand total, the framework supplies the missing functional relationship synthetically by an allocation bridge (Part VII Chapter 22.5):

| Allocation | Behavior |
|---|---|
| `equal_split` | each membership receives an equal share |
| `weighted(expr)` | shares proportional to a declared weight |
| `proportional_to(col)` | shares proportional to another column's values |
| `custom(rule)` | author-supplied weighting, verified to sum to one per fine entity |

Allocation and broadcast are not the same operation and do not share machinery. Broadcast replicates a coarse value down a *functional* (1-to-many) edge for comparison; allocation apportions a value across a *many-to-many* relationship so that totals reconcile. Conflating them — apportioning on a broadcast, or replicating on a many-to-many — is exactly the double-counting error the framework is built to prevent.

#### 2.5 Subsetting (the value-determination operation)

Subsetting restricts a column's domain by a predicate, producing a result restricted to the satisfying points. Per the conceptual manual's clarification, subsetting at query time produces a *restricted query result* — it is an expression operation, not a Manifold-level column state. (The Manifold-level concept of degeneracy is a column-level property of how a Manifold-bound column relates to the Manifold's defining boundaries; see Part IV.)

Subsetting takes a predicate over dimension attributes (which may be reached through hierarchy edges), produces a result carrying the restriction predicate as part of its identity for downstream coverage compatibility, and uses closed-world semantics: points where the predicate cannot be evaluated (because an input is missing) are excluded rather than retained.

#### 2.6 Operator property summary

Every operator's place in the system is fixed by four operator-level facts, which is what the framework needs to know about each operator (and which the operator registry of Part III specifies):

- **Operation kind**: map (preserve), aggregate (coarsen), broadcast (refine), subsetting (restrict).
- **Order-dependence**: independent (most maps; `SUM`, `AVG`, `MAX`) or dependent (scans; `LAST`, `FIRST`).
- **Algebraic signature**: input types, output type, and — for reducers — the fertility classification (fertile, fertile-via-sketch-carrier, mule).
- **B-anchor propagation rule**: how the operator's output B-anchor derives from its inputs' B-anchors.

These four facts are operator-level and apply uniformly regardless of which column the operator is applied to. Column-specific concerns — the actual B-anchor for a particular column under this reducer, the missing-policy override for this (column, reducer), and other per-column behaviors — live in the column-spec, not in the operator. This separation is the subject of Part III Chapter 8.

---

## Part II — Anchors and Dimensions

This is Part II of the reference manual. Part I specified the logical types and the operator catalog. This part specifies anchors and dimensions: what makes a valid anchor, how dimensions play their role, how dimension families and roll-up edges are declared and verified, how multiple hierarchies on one base are handled, and how the prohibition on missing dimension values is met in practice. It presumes Part I and the conceptual manual.

---

### Chapter 3. Anchors

#### 3.1 What an anchor is, precisely

An anchor is a set of dimensions over which a column is defined as a function. The conceptual manual established the idea; the specification adds the precise requirements. (A column's own anchor — its value-domain — is its **V-anchor**, the first of the three anchors it carries; the **M-anchor** and **B-anchor** of Part III are the other two. "Anchor" unqualified is the shared coordinate primitive that all three, and the lattice developed below, are built from.)

An anchor is a *set*, not a sequence: `{customer, day}` and `{day, customer}` are the same anchor. Order of dimensions within an anchor carries no meaning — the anchor identifies points by the combination of coordinate values, and the combination is unordered. (Ordering of *values within a dimension* is a separate matter, relevant to scans and ordered reducers, treated under dimension families below.)

An anchor must satisfy two properties to be sound (the data conditions any correct analysis on the column requires):

**Uniqueness.** Each combination of dimension values identifies at most one point. There are no two distinct points with identical coordinate values. This is what makes the column a *function*: given the coordinates, there is one value (or its explicitly-modeled absence), never two. Data where coordinate combinations repeat is data that does not yet support functional querying — the framework refuses to treat it as if it did.

**Identifying completeness.** Each point's coordinate values are all present — no missing values in any dimension serving in the anchor. This is the prohibition developed in Chapter 5 below; here it is stated as an anchor property: an anchor's coordinate values must be present, because a point with a missing coordinate is not identified, and an unidentified point cannot belong to a function's domain.

Together: an anchor is a set of dimensions whose value-combinations uniquely and completely identify the points of a column's domain. A column is a total or partial function from those identified points to values — total if defined everywhere on the anchor, partial if its M-anchor admits absence at some points, but in either case the *points themselves* are fully and uniquely identified.

#### 3.2 The `{}` anchor

The empty anchor `{}` is well-formed and important. In any given Manifold, `{}` is **the Manifold's defining boundaries taken as a single anchor point — the totality of what this Manifold is bounded by, reduced to one scalar position.** A column anchored on `{}` is a scalar over the Manifold's defining boundaries: one value, the grand total or grand aggregate of whatever the column represents, computed across everything the Manifold is about.

`{}` is therefore Manifold-relative, not a context-free notion of "everything." The `{}` of a US-customer Manifold aggregates over US customers; the `{}` of a global Manifold aggregates over global customers; even though both are written `{}`, they are not the same scalar — they aggregate over different defining boundaries. This is the precise sense in which the universe constituent of the Manifold (the defining boundaries from the framework manual's Manifold definition) is operationalized as a lattice element: `{}` is the lattice's top within the Manifold, the single point at which all coarsening converges, and that single point *is* the data within the Manifold's defining boundaries.

Under composition (Part V), the composed Manifold has its own `{}` that aggregates over the composed (typically intersected or reconciled) defining boundaries — distinct from either parent's `{}`. The reconciliation work that any join requires is, among other things, the work of determining what the composed Manifold's defining boundaries — and therefore its `{}` — refer to.

#### 3.3 The anchor lattice, and where columns root in it

The lattice order is refinement: anchor A is finer than anchor B (A ⊑ B reads "A refines to B" going up, or B is coarser than A) when every point of B corresponds to a set of points of A that collapse into it. Concretely, B is reachable from A by some sequence of drops and climbs.

The lattice is a partial order, not a total one: two anchors may be incomparable. `{customer, day}` and `{customer, region}` are incomparable — neither is finer than the other, because day and region are independent coordinates and neither's points collapse into the other's. Incomparability is the formal reason two columns at such anchors cannot be combined directly: there is no lattice relationship to bring one to the other, so combination requires bringing *both* to a common anchor finer than or equal to each (their meet, if it exists) or coarser than each (a common ancestor).

The lattice's top element is `{}` (the Manifold's defining boundaries as one point); the lattice's *bottom* — its finest possible position — depends on what dimension granularity the Manifold describes.

A crucial point: **the lattice is a single shared structure across the Manifold (built from the Manifold's dimension families), but the *rooting position* — the finest anchor at which a given column is natively defined — is per-column.** Different columns occupy the lattice at different starting positions, and "the root" is not a Manifold-wide concept but a column-specific one.

Concretely: `revenue` may be natively at `{transaction}` — that is `revenue`'s root, the finest anchor where it is observed. `inventory_balance` may be natively at `{warehouse, day}` — that is its root, and `revenue`'s finer transaction-grain has nothing to do with it. `customer_lifetime_value` may root at `{customer}` — finer than that, the data simply does not exist; the column is rooted where the data is observed, not at some artificial common-bottom.

This is what the family-as-optimization framing rests on. Per the conceptual manual: every value of a column is, in principle, always computable by aggregation from that column's root — this is the always-correct fallback that makes families an *optimization* rather than a correctness mechanism. Families cache a column's images at coarser anchors derived from its own root; the cache exists because computing from root every time would be expensive, not because cached intermediates are required for correctness. Cache reuse across grains is licensed by path-invariance (fertile reducers preserve the answer across cache-and-re-aggregate paths). Each column has its own family lattice over its own root, with its own cached images, and its own invalidation behavior tied to refreshes of *its* root data.

So when this manual or the framework manual refers to "the root," it always means the *column's* root. There is no Manifold-wide root. The lattice is shared; the rooting points are per-column; the family optimization is per-column over each column's trajectory from its own root upward.

#### 3.4 Drops and climbs, specified

The two ways to coarsen — established conceptually — have distinct specifications because they have distinct requirements.

A **drop** removes a coordinate entirely. Its requirement is on the *measure being aggregated*: dropping coordinate `c` under reducer `g` is well-formed only if `c`'s dimension family is not in `g`'s B-anchor for that column. Dropping `customer` from a balance under `SUM` is fine; the only check is applicability, since a drop invokes no hierarchy.

A **climb** replaces a coordinate with its parent in a dimension family. Its requirements are two: the hierarchy edge must exist and be sound (a verified functional dependency — Chapter 4), *and* the reducer must be applicable along the climbed axis (the B-anchor check). A climb is more constrained than a drop because it additionally depends on the hierarchy being sound. So: drop checks (axis not in reducer's B-anchor); climb checks (hierarchy edge sound) AND (axis not in reducer's B-anchor).

Most coarsenings in practice decompose into a sequence of drops and climbs, and the framework types each step accordingly. An expression that says only "bring revenue to `{region}`" from `{customer, day}` is resolved by the planner into the necessary drops (day) and climbs (customer → region), each checked.

---

### Chapter 4. Dimensions and Dimension Families

#### 4.1 The dimension role, specified

A dimension is a column in the role of an anchor component for some other column (the conceptual manual's role-not-kind principle). The specification adds: a column is *in the dimension role for a given column C* exactly when it appears in C's anchor. The same column may be in the dimension role for some columns and not others, simultaneously, within one Manifold. There is no flag on a column declaring it "a dimension"; dimensionhood is read off the anchors that use it.

The framework can compute, for any column, the set of columns for which it serves as an anchor component, simply by scanning anchors. This set is what the role-aware integrity checks consult (Chapter 5): the missing-value prohibition applies to a column exactly in those anchors where it serves as a component.

#### 4.2 Dimensions and the Enumerated type

A dimension frequently has a *known, finite set of valid values* — the regions are a fixed list, the product categories are enumerated, the statuses are a closed set. This finite-closed-domain property is logical and is captured by the `Enumerated` type from Part I, paired with the dimension role.

When a dimension's column has the `Enumerated` type, the framework knows the dimension's full value set independent of the data, which enables: validity checking (does the data contain any value outside the declared domain — an integrity violation?), completeness checking (are all declared domain values actually present in the data?), and the principled handling of empty groups by the **empty-bucket rule** (Chapter 9.4): a declared domain value absent in a particular slice is a point that *exists* whenever the destination universe contains it — its `SUM` and `COUNT` are true zeros, its order statistics and means are absent — and over an events-projection destination it is not a point at all and nothing is rendered. In neither case does anything silently vanish, because the resolved (anchor, universe) is disclosed with the result. <!-- X2: ADR-028 / D5; replaces the prior edition's empty-group hedge -->

A dimension need not be `Enumerated` — a `customer` dimension is typically open (the set of customers grows). An open dimension's value set is whatever the data contains; the framework cannot check completeness against a declared domain because there is none. Both kinds are valid; `Enumerated` is declared when the domain genuinely is fixed and known, and it buys the validity and completeness checks.

#### 4.3 Dimension families: roll-up edges

A dimension family is a set of dimensions connected by roll-up maps forming a commuting hierarchy. The specification of a roll-up edge:

An edge `child → parent` (e.g., `day → month`, `customer → region`) is a declared mapping asserting that each child value maps to exactly one parent value. The edge is specified by naming the child dimension, the parent dimension, and the source of the mapping (which physical column or relationship provides it). The edge is a *functional dependency*: child functionally determines parent.

A verified functional edge is what the engine **transports** along — the operation that does the work a join did, on the column foundation. To address a column anchored at the child by the parent, the engine fetches the column at the child, fetches the edge itself as a column-atom (a key→key mapping the connector delivers like any other column), and carries the value along the edge to the parent — *inside the engine*. The backend delivered two columns and never related them: relating is transport, never a generated join, and the connector is asked only to *deliver* columns, never to *combine* them. Transport is defined only along functional edges — the reducing direction, where each value moves to the single point it maps to, without replication — which is exactly why a non-functional edge admits no transport (Chapter 19.2, Chapter 22.5). <!-- ADR-031 D1/D9: relating is transport in the engine; the connector delivers columns, never combines them; transport is defined only along functional edges. -->

The framework *verifies* every declared edge against the data: the mapping must be a total function — every child value present in the data maps to exactly one parent, with no child mapping to two parents and no child mapping to none. A declared edge that fails verification is invalid; the failure is recorded in the integrity certificate with its scope (only climbs along *this* edge are implicated; the rest of the Manifold stands), and a climb along it is routed through detail where a sound route exists, otherwise served carrying the contradiction's specifics at certificate state `CONTRADICTED` (Chapter 19). <!-- X1: ADR-020 -->

The verification is relative to the Manifold's defining boundaries: an edge holds over the set of child values actually present within the Manifold's scope. The same edge might hold over one Manifold's defining boundaries and fail over another's (a customer-region mapping might be functional for US customers but not globally). The certificate records the edge's soundness as a claim about *this* Manifold's defining boundaries, not universally.

#### 4.4 The commuting requirement

A dimension family is more than a collection of edges — the edges must *commute*. If `day → month`, `month → quarter`, and `day → quarter` are all declared, then composing `day → month → quarter` must equal `day → quarter` directly. The commuting property is what makes the hierarchy navigable by any path to the same answer, and the framework verifies it: declared edges that form a diamond must produce consistent composite mappings.

In practice, families are usually declared as a *chain* (`day → month → quarter → year`) rather than with redundant edges, in which case there is one path between any two levels and commuting is automatic. The commuting check bites when an author declares redundant edges, where consistency must be verified.

#### 4.5 Multiple hierarchies on one base

A base dimension may root more than one family. `day` rolls up to calendar `month → quarter → year`, and *also* to ISO `week → iso_year`, and these two hierarchies are independent — `week` and `month` are not functionally related. Each is a valid family on the base `day`; they are *sibling hierarchies*.

A base dimension may participate in multiple declared families, each with its own roll-up chain. Where two sibling hierarchies do not relate, a query that climbs must specify *which* family it climbs — "by month" and "by week" are climbs in different families, and where ambiguity is possible the framework requires the family to be named. The conceptual manual's point that "which hierarchy you climbed is a parameter that does not wash out" is enforced here: the climb is parameterized by the family, and the parameter is required when sibling hierarchies make it ambiguous.

A composite aggregation like "peak monthly revenue versus peak weekly revenue" differs precisely because it climbs different sibling families before applying the outer reducer. The framework treats the choice of sibling hierarchy as part of the composite's specification, the same way it treats the intermediate anchor of any non-commuting composite.

#### 4.6 Ragged and non-strict hierarchies

A hierarchy need not have uniform depth. An organizational hierarchy where some employees report directly to the CEO and others through several layers is *ragged*: the roll-up chain has variable length.

The framework supports ragged hierarchies with a specification caveat: roll-up edges remain valid (each child still maps to one parent), and climbs *along actual parent links* remain well-formed, but "level N" is no longer a well-defined anchor across the whole hierarchy. A query can climb to a *named level* only where the level is well-defined; in a ragged hierarchy, climbs are specified relative to the parent relationship (climb to parent, climb to root) where named levels would be ambiguous. The framework distinguishes strict hierarchies (uniform depth, named levels well-defined, climb-to-level always valid) from ragged ones (variable depth, climb-to-named-level valid only where the level exists, climb-to-parent and climb-to-root always valid) and types climbs accordingly.


#### 4.7 Time-varying functional dependencies (the slowly-changing dimension)

<!-- review §4.3 — new section; the certificate's most common day-one finding in mature warehouses, given its modeling response -->

The hierarchy-integrity machinery treats `customer 19847 → both 'east' and 'west'` as a defect, and often it is. But the most common cause in real warehouses is that *the customer moved*: the mapping is genuinely time-varying, and every mature warehouse carries slowly-changing-dimension machinery for exactly this. The certificate is still right to fire — the declared edge, as declared, is not a function — but the author's correct response is a modeling change, not a data fix, and this section specifies the pattern.

**Recognize it.** A time-varying dependency has a signature a data defect does not: the violations cluster at *transition dates*. Pull the violating children and inspect their conflicting parents against time — a customer whose 'east' rows all precede March and whose 'west' rows all follow it has moved; a customer whose regions interleave randomly is a data defect. The distinction is checkable, and inspecting it is the first remediation step the finding's remedy names.

**Model it.** Two sound shapes, chosen by what the analyses need:

- **Period-qualify the edge.** Declare the dependency over the composite child `{customer, period} → region`: each customer *in each period* maps to exactly one region — a true total function the framework verifies like any other. The dimension becomes effective-dated; the assignment is itself a column at `{customer, period}`.
- **Split current from historical.** Declare `customer → current_region` as a true FD over the registry's present state (verified, navigable), and keep the historical assignment as an ordinary effective-dated column for the analyses that need as-of truth.

**Know what each does to climbs.** The two shapes answer different questions, and a query names which it asks. Climbing by `current_region` applies *today's map to all of history* — right for "how are my current regions performing over time," wrong for "what did each region sell last year." Climbing the period-qualified edge gives *as-of* truth — each transaction credited to the region the customer was in when it happened — right for historical attribution, and it requires the time coordinate to survive to the climb (the planner checks reachability as for any composite-child edge). Both are legitimate; neither is a default; the silent substitution of one for the other is exactly the error class the explicit edge declarations make unrepresentable.

The pattern is philosophically adjacent to scope-bounded attestation (ADR-016): a warrant about a stabilized slice. A contradicted `customer → region` whose violations cluster at transitions is not data that is wrong but a declaration that was coarser than reality — and the framework, having been the messenger, is also the toolbox for the fix.

---

### Chapter 5. Missing Values in Dimensions

#### 5.1 The prohibition, as an anchor property

A column may not have missing values while serving in the dimension role, and the requirement is most precisely a property of the *anchor*: an anchor's coordinate values must be present and identifying. The specification states this as the identifying-completeness condition, and makes concrete what "while serving in the dimension role" means: the prohibition applies to a column's values *as they appear in any anchor that uses the column as a component*. The same column's values, where it serves only as a measure-role attribute (no other column anchored on it there), may be absent under its M-anchor.

The check is role-scoped: the framework identifies, for each column, the anchors in which it serves as a component, and verifies missing-freeness *there*. A `customer` column that anchors `revenue` must be missing-free in revenue's anchor; the same conceptual customer, appearing as a sometimes-missing attribute on a transaction-level report where nothing is anchored on it, is permitted to be absent there.

#### 5.2 Promotion to named values

The prohibition is met not by rejecting incomplete data but by *promoting absence to an explicit named value*. The specification:

When a column is to be used as an anchor component but its source data contains missing values, the author declares a **null-coalescing rule** as part of the column's binding: a mapping from missing/null to an explicit named value (`UNKNOWN`, `ANONYMOUS`, `NOT_APPLICABLE`, or a domain-appropriate label). The rule is applied at binding time, so that by the time the column serves in an anchor, it is missing-free — every formerly-missing value has become the explicit named category.

The promoted value is a first-class dimension value: it appears in the dimension's value set (and, for an `Enumerated` dimension, must be *declared* in the domain so that validity checking permits it), it participates in hierarchies (Chapter 5.3), it forms a legitimate group under aggregation, and it *reconciles* — the `UNKNOWN` group's total sums into the grand total alongside the real groups, where a silent null group would have made totals fail to add up.

The promotion is an explicit, declared act — it is not automatic. The framework does not silently coalesce nulls; it requires the author to declare the coalescing rule, because *how* to name the absence (and whether the absence is genuinely a single "unknown" bucket or several distinguishable kinds of absence) is a modeling decision only the author can make. Absent a declared rule, a column with missing values is simply ineligible for the dimension role, and the framework refuses to anchor on it, reporting the missing values and the remediation.

#### 5.3 Promoted values in hierarchies

A promoted value must have a place in any hierarchy the dimension participates in, or the hierarchy's roll-up edge would fail (the `UNKNOWN` customer would have no region, breaking the `customer → region` functional dependency). When a dimension with promoted values participates in a hierarchy, the promotion must *cascade* — the `UNKNOWN` child maps to an `UNKNOWN` (or designated) parent, keeping the edge total. The author declares the cascade as part of the hierarchy, and the framework verifies that the edge remains a total function including the promoted values.

This cascade is what keeps the hierarchy machinery working in the presence of promoted unknowns, and it is only possible *because* the unknown was promoted to a named value — a raw null could not have a parent at all, but a named `UNKNOWN` can map to a named `UNKNOWN` parent, preserving totality.

#### 5.4 The value-versus-dimension asymmetry

A *value* (a column in its measure role) may be absent, with the absence characterized by the M-anchor — absence-of-value is a coherent state with a mechanism. A *dimension* (a column in its anchor-component role) may not be absent — the absence must be promoted to a named value — because a missing identifier identifies nothing and an unidentified point cannot belong to a domain.

The same physical missing value is treated differently depending on role: a transaction with no identified customer is, in the transaction's measure-role view, a missing `customer` *attribute* (legal, M-anchor-characterized); but to anchor revenue on customer, that same missingness must be promoted to an `ANONYMOUS` customer value (the anchor must be missing-free). The framework applies the appropriate treatment based on the role the column plays in the specific anchor or attribute context. This is not inconsistency; it is the single principle — absence permitted only when explicitly accounted for — taking its two role-appropriate forms: characterized by M-anchor for values, promoted to a named category for dimensions.

---

## Part III — Applicability, Missingness, and the Universe

This is Part III of the reference manual. Parts I–II specified types and operators, anchors and dimensions. This part specifies two of a column's three **anchors** — the qualifier anchors that govern when operations are legitimate: the **B-anchor** (blocked anchor), which records along which axes a column's reducer is *blocked* from rolling up (formerly the non-applicability anchor, NAA), and the **M-anchor** (missingness anchor), which records the mechanism behind a column's missing values (formerly the missing-determinant anchor, MDA). They join the **V-anchor** — the value anchor, a column's domain (Chapter 3) — to complete the triad: *a column is a value plus three anchors, V, M, and B* (where it lives, where it leaks, where it blocks); the closing chapter of this part adds the **universe** the V-anchor addresses — which points exist — completing the grain as the pair *(anchor, universe)*. Two asymmetries set the B-anchor apart from the V- and M-anchor, and both are made precise below: it is **per-family, not per-column** (§6.1), and it is **prohibitive, not locative** — it forbids a roll-up across the named axes rather than pointing at where values exist. Both qualifier anchors are first-class declarations on columns, both propagate through operations by specifiable rules, and both feed the framework's disclosure discipline: what they catch rides to the consumer as findings on served results, never as silence. <!-- X1: ADR-020; X2: ADR-028 -->

This part also specifies the column-spec — the complete declaration of a column — and the operator registry, with a deliberate division of concern: column-specific knowledge (the actual B-anchor values, missing-policy choices, per-(column, reducer) overrides) lives in the column-spec; operator-level knowledge (algebraic signatures, propagation rules, name aliases) lives in the registry. Keeping the two separate keeps each authoritative for what it knows.

This part presumes Parts I and II and the conceptual manual.

---

### Chapter 6. The B-anchor: Applicability

#### 6.1 What the B-anchor records, precisely

The conceptual manual established that the B-anchor is the set of dimension families along which a particular reducer is not applicable for a particular column. The specification adds precision:

The B-anchor is a property of a **family** within a column's family set — that is, it is associated with a (column, reducer) pair, not with the column alone. The same column has different B-anchors for different reducers: `inventory_balance · SUM` has the time family in its B-anchor; `inventory_balance · LAST` does not (`LAST` is applicable along time precisely because it respects the order); `inventory_balance · AVG` has neither (`AVG` is intensive along all axes). Each family in a column's family set carries its own B-anchor as part of itself.

A B-anchor is a **set of dimension families**, not a set of dimensions. Stated in terms of families, the B-anchor is anchor-invariant: it does not need recomputation when the column's anchor changes through aggregation. "Sum of inventory_balance is non-applicable along the time family" remains true whether the column currently sits at `{warehouse, day}`, `{warehouse, month}`, or `{warehouse}` — the family is the stable referent, the specific dimension within it is variable. This is the precise sense in which the B-anchor is the right primitive: it names what stays constant under anchor change.

#### 6.2 The three B-anchor shapes — and why they are not the extensive/intensive axis

A reducer's B-anchor for a column takes one of three shapes, by how much of the family set it covers:

| B-anchor shape | Meaning | Example |
|---|---|---|
| Empty | applicable along every family — reduce freely | revenue under `SUM` |
| Every dimension family | applicable along none — cannot be reduced along any axis | temperature under `SUM` |
| Proper subset | applicable along some axes, not others — semi-applicable | inventory balance under `SUM`: time in the B-anchor, warehouse not |

The B-anchor is strictly more expressive than a three-way label because it names *which* families are non-applicable. The framework operates on the B-anchor directly; any coarser label is, where useful, derived for human display.

**A caution that the v4 operator model makes load-bearing: the B-anchor shape is *not* the extensive/intensive classification, and the two must not be conflated.** An earlier framing presented "extensive ⇒ empty B-anchor, intensive ⇒ full B-anchor, semi-additive ⇒ proper subset" as if applicability and additivity were one axis. They are two orthogonal axes, and treating them as one produces wrong findings and wrong arithmetic:

- **Applicability (the B-anchor)** answers *along which dimension families may this reducer legitimately coarsen?* It is a plan-time check: a reduction along a family in the B-anchor is served only with the critical crossing disclosure (Chapter 6.4), and withheld only under a declared `WITHHOLD`. It is what makes summing a stock across time impossible to do silently. <!-- X1: ADR-020 -->

- **The intensive/extensive bit** answers *does the quantity scale with the size of the set being reduced?* — and it drives missing-data arithmetic, never an outcome gate (Chapter 7.3, Chapter 8.2): an extensive reducer under MCAR skips-and-rescales, an intensive one merely skips.

The counterexample that proves they are distinct is the account balance. A balance is **extensive** (two accounts' balances add; it scales with the set) yet its `SUM` family is **semi-additive** — time is in its B-anchor, because summing the same balance across successive days double-counts a stock. Extensive does *not* imply empty B-anchor. Conversely, a non-rollable reducer like `AVG` is non-rollable because it is a *mule* (the fertility axis, Chapter 2.1), not because of anything in its B-anchor. Applicability, scaling, and fertility are three independent facts about a (column, reducer) family; the B-anchor records only the first.

#### 6.3 How the B-anchor is checked

The B-anchor is consulted at every operation that would coarsen the anchor (a drop or a climb) and at every broadcast that would refine it. The check is structurally simple:

For an **aggregate** with reducer `g` applied to a column: identify which dimension families are being eliminated by the coarsening (dropped axes for a drop; the climbed family for a climb). For each eliminated family, check whether it is in the column's family-set entry for `g` — that is, whether `g`'s B-anchor for this column contains the family. If any eliminated family is in the B-anchor, the crossing fires: the result is served only with the critical disclosure of Chapter 6.4 (or withheld under a declared `WITHHOLD`). <!-- X1: ADR-020 -->

For a **broadcast** refining the anchor: broadcast is replicate-only and needs no allocation, so there is no plan-time check at the broadcast itself. The B-anchor's role here is downstream — the broadcast records the family it spread along in the B-anchor of any reducer that would sum the result, so a later attempt to re-aggregate the broadcast value back across that family is caught by the ordinary coarsening check above and carries the same critical disclosure (the double-count guard of Chapter 2.4).

For a **map**, no B-anchor check is needed at the operation level (anchor preserved), but map can change the resulting column's B-anchor (Chapter 6.5).

For a **scan**, no B-anchor check at the operation level, but the scan's order axis interacts with the B-anchor: a scan that orders by a time axis must, if the underlying column's family has time in its B-anchor, use an ordered reducer whose B-anchor permits time.

#### 6.4 What happens on a violation

When the B-anchor check fails, the operation is caught at plan time and the result, if produced, is served only with a **critical disclosure**: the finding names the column, the reducer, the eliminated family, and the violated B-anchor entry; quantifies the crossing where it can (the double-count or replication factor); and, where the column's family set contains an alternative reducer applicable along the violated axis, surfaces that alternative as the remedy. The crossing is never the engine's grounds for withholding — the result is withheld only where the author has declared `WITHHOLD` on the family entry, in which case the outcome is an *inform* reporting the author's rule (Chapter 19). <!-- X1: ADR-020; ADR-025 -->

A canonical example: `SUM(eom_inventory) @ {store}` from `{store, day}` drops the day axis. The column's `SUM` family has time in its B-anchor. The framework serves the figure carrying the critical finding — "summing a daily stock over the period counts the same inventory once per day" — and notes that the column has a `LAST` family applicable along time. The disclosure is informative, grounded in declared knowledge about *this* column's behavior; an author who never wants the crossing served declares `WITHHOLD` on the `SUM` family entry. <!-- X4: retail vocabulary -->

#### 6.5 B-anchor propagation through operations

The B-anchor of a column produced by an operation is computed from the B-anchors of the inputs and the nature of the operation. The framework does not assume the result inherits an input's B-anchor; it recomputes it.

**Map of one column.** A linear map (multiplication by a constant, addition of a constant) preserves B-anchor. A nonlinear map (`log`, `square`, `exp`) generally produces a column whose extensive/intensive character has changed, and the framework's default is conservative: assume the result is intensive (B-anchor = all families) under `SUM`. The author may override on the derived column's spec where the result has a known specific additivity character.

**Map of multiple co-anchored columns.** Arithmetic combinations preserve extensive character when the operation is additive (extensive + extensive = extensive; B-anchor = intersection of input B-anchors). Multiplication is mixed: extensive × intensive = extensive (revenue × weight stays extensive), extensive × extensive has no clean additivity, intensive × intensive = intensive. Division: extensive / extensive = intensive (a ratio). The framework applies these rules where they are clear and is conservative (assumes intensive) where they are not, with author override available.

**Aggregate.** The result's B-anchor is the input's B-anchor *minus the families that were eliminated by the aggregation* — those families are no longer present in the anchor, so they are vacuously non-applicable.

**Broadcast.** Preserves the input's B-anchor character and *adds* the broadcast family to the B-anchor of any reducer that would sum the result — the column is the same coarse quantity, now replicated to a finer anchor, and must not be summed back across the family it was spread along. This added B-anchor entry is the double-count guard (Chapter 2.4).

**Subsetting.** Subsetting does not change the B-anchor; restricting a column's domain does not change what kind of quantity it is.

These rules are the framework's defaults. Author overrides are permitted on a derived column's spec where the rules would misclassify it.

---

### Chapter 7. The M-anchor: Missingness

#### 7.1 What the M-anchor records

The M-anchor characterizes the *mechanism* of a column's missing values: what coordinates determine whether a value is present or absent. The three principal cases:

| Mechanism | M-anchor shape | Meaning |
|---|---|---|
| MCAR (missing completely at random) | empty | missingness independent of all observed and unobserved values |
| MAR (missing at random, given observed) | a set of dimension families | missingness depends on those observed coordinates; conditionally independent given them |
| MNAR (missing not at random) | a flag indicating dependence on the column's own value | missingness depends on the unobserved value itself; non-correctable from observed data alone |

The MAR case names *which* observed coordinates the missingness depends on. The MNAR case is structurally distinct: it is a flag, not a set of observed coordinates, because it asserts dependence on a quantity that is by construction unobserved.

A column may declare both MAR coordinates *and* the MNAR flag — missingness can depend on observed coordinates *and* on the unobserved value. The default and most permissive case is MCAR; the most restrictive is MNAR.

**The M-anchor's member domain, pinned.** *M ⊆ {dimension families} ∪ {column names, including the column's own}.* A **dimension-family** member is the classical MAR case: missingness depends on observed coordinates. A **measure-column** member — `satisfaction.M = {revenue}` — declares *MAR given that observed column*: missingness depends on another column's observed values, neither a coordinate nor the column's own value, and the framework treats the named column's observed values as the stratification axis where they are preserved and the propagation trigger where they are not, exactly as it treats coordinate members. **Self by name** (`col.name ∈ M`) is the MNAR designation (ADR-024): dependence on the column's own unobserved value. The extension matters twice: it gives the common middle mechanism a representable home — missingness conditioned on another observed column is MAR, correctable in principle — and it is the declaration the Pro estimators condition on (inverse-probability weighting and selection models condition on observed covariates, which are columns, not coordinates). Falsification for measure-column members is specified with the other density checks (Chapter 23.3). <!-- Huayin execution call (1), 2026-06-11; review §4.4 -->

**The jurisdiction rule** (Chapter 9.7) bounds everything in this chapter: the M-anchor governs **value-presence at universe points**; **point-existence** belongs to the column's universe. No mechanism may be declared over the point-existence of an events projection — a purchase that didn't happen is not a point — and the M-anchor's denominators are supplied by the covered universe. <!-- X2: ADR-028 -->

#### 7.2 Checkable versus asserted

The MCAR claim is **partially testable**: it can be falsified (one can check whether missingness is independent of each observed coordinate) but not strictly confirmed. The framework runs a falsification check on declared MCAR and reports violations.

The MAR claim's *observed* coordinates are **checkable for consistency**: given a declared MAR(C) for some set C, the framework can check whether missingness is approximately independent of observed coordinates outside C, conditional on C.

The MNAR flag is **not testable from observed data alone**. This is a theorem of the missing-data literature, not a tooling gap. The framework records the flag as asserted, propagates it faithfully, and never verifies it.

Each M-anchor component carries its *evidential basis* — **checkable** or **asserted** — in the integrity certificate: the MCAR/MAR observed-coordinate claims are checkable (the data can falsify them), the MNAR flag is asserted (the data cannot test it). This basis is distinct from the *verdict* the certificate then reaches on the precondition — the four states of Part VI Chapter 18.

#### 7.3 How the M-anchor governs aggregation: the policy

The M-anchor, combined with the reducer's intensive-or-extensive character, determines how missing values are handled under aggregation. The framework's defaults are drawn from a fixed vocabulary of five behaviors — **skip · skip-and-rescale · stratified · propagate · fill** — and the default table selects among them from two facts: the column's missingness mechanism and the reducer's intensive/extensive bit. <!-- ADR-025: refuse retired from the vocabulary -->

| M-anchor | Reducer kind | Behavior | Result property |
|---|---|---|---|
| Empty (MCAR) | intensive (e.g., `AVG`) | skip | unbiased estimate |
| Empty (MCAR) | extensive (e.g., `SUM`) | skip-and-rescale | unbiased estimate of total |
| MAR(C), aggregating *within* C | intensive | stratified (skip per stratum) | conditionally unbiased |
| MAR(C), aggregating *within* C | extensive | stratified (rescale per stratum) | conditionally unbiased |
| MAR(C), aggregating *across* C | intensive | propagate | biased marginal, carried and flagged |
| MAR(C), aggregating *across* C | extensive | propagate | biased marginal, carried and flagged |
| MNAR flag set | any | serve observed + disclose | observed-data figure; no automatic correction is sound; unknown-direction bias stated at certificate state UNTESTABLE |

The principle: **the framework applies the most permissive behavior that is principled given the declared mechanism and the reducer's character.** Skip is permissive (uses observed values); skip-and-rescale corrects an extensive skip for the missing fraction; stratified applies the right per-stratum correction when missingness depends on observed coordinates; propagate carries a knowingly-biased marginal forward *with a finding* rather than presenting it as clean; and under MNAR, where no principled correction exists, the framework serves the observed-data figure with that fact disclosed rather than presenting any figure as a population estimate.

The MNAR row deserves its own statement, because the prior edition handled it differently. **MNAR is disclosure, never a silent estimate.** When missingness depends on the unobserved value itself, there is no correction the observed data supports — a theorem of the missing-data literature, not a tooling gap — so the framework serves the **observed-data figure** with an `UNTESTABLE`-state finding stating that the bias direction is unknown. What it never does is two things: present the figure as a population estimate, or withhold it on its own analytical judgment. The prior edition's `refuse` here is retired (ADR-020, ADR-025): withholding is not a missing-data treatment, and an author who wants a hard stop has a governance instrument for it — `WITHHOLD`, Chapter 7.5 — reported as the author's rule, never the engine's. **Propagate** remains distinct: it produces the MAR-across marginal tagged as biased, with the direction and bound where determinable, so the caveat travels with the result. <!-- X1: ADR-020; ADR-025 -->

Two cells deserve specific attention because they are the most often wrong in conventional tools:

**Extensive `SUM` under MCAR is skip-and-rescale, not skip.** A bare skip-sum systematically underestimates the total by the missing fraction. The framework multiplies the observed sum by N_total / N_observed to produce an unbiased estimate of the population total. Conventional tools default to skip and silently undercount; Columna's default is the correct one for the question "what's the population total." An author who specifically wants "total of observed only" can override via the column-spec (Chapter 7.5); the framework's default is the principled choice for the question most users actually mean.

**MNAR yields the observed-data figure, disclosed — never a silent number and never a silent estimate** (stated in full above): no correction the observed data supports exists, so the served figure carries the `UNTESTABLE` finding with its unknown-direction bias; the author's hard stop, where policy wants one, is `WITHHOLD` (Chapter 7.5); and any acknowledgment that proceeds past a declared gate is recorded in the annotation and demotes the result's verdict to at most `CORROBORATED` — never silently promoted to a clean answer (Part VI Chapter 18). <!-- X1: ADR-020 -->

#### 7.4 Skip-and-rescale: the precise computation

For an extensive reducer `SUM` applied to a column with N_total points, of which N_observed carry values:

> rescaled sum = `SUM(observed values) × (N_total / N_observed)`

**N_total is the covered universe** (Chapter 9.7): the cardinality of the column's universe within its coverage. The framework knows it because the universe is declared or derived and its points are enumerable — a value's absence at an existing point is distinct from the point not existing, which is exactly the jurisdiction rule. Rescaling estimates the total over the covered points, never beyond them; extrapolation past coverage is coverage's finding to disclose, not the rescale's job to attempt. Where the column's universe is an events projection, point-existence *is* observation and there is no spine to rescale over — the conventional sum ties out against the source by construction — while value-missingness at existing event points (a transaction with an uncaptured amount) rescales over the record count as its denominator. <!-- X2: ADR-028 / D3 -->

The computation is worth seeing plainly, as an identity rather than a theorem: `SUM(observed) × N_total/N_obs` is exactly `SUM(observed) + N_missing × mean(observed)` — fill every hole with the observed average, then sum, collapsed into one multiplication. The disclosure can therefore say what was actually done ("4 missing values estimated at the observed mean of 31.20"), and the estimate's unbiasedness remains conditional on the declared mechanism being true — asserted, never verified. <!-- U.5: mean-substitution identity, at the rescale's first appearance per charter -->

The result carries the rescale finding in its annotation, with the factor (N_total / N_observed) quantified so the figure can be reconciled against a raw source-system sum. Rescaling is applied at the *leaf* — at the first aggregation from a column with missing values — and the result is then unbiased at that coarser anchor. Subsequent fertile aggregations up the lattice operate on already-unbiased values, preserving path-invariance from the rescaling point upward. The framework propagates the finding but does not re-rescale. <!-- X1: ADR-020 (annotation, not lineage flag) -->

#### 7.5 The column-spec's missing-policy field

The framework's default policies (Chapter 7.3) are the principled choices given declared mechanisms. But the right policy for a particular (column, reducer) is sometimes not the default — and the place this is declared is on the **column-spec**, as part of the family entry for that reducer.

Recall that a column's family set is a set of family entries, one per reducer the column supports. Each family entry carries, as part of itself:

| Family entry field | Specifies |
|---|---|
| reducer | the function the family is built on |
| B-anchor | the dimension families along which the reducer is non-applicable for this column |
| missing-policy | how missing values are handled when this reducer is applied to this column |

The missing-policy values are drawn from the same five-behavior vocabulary as the default table (Chapter 7.3), plus `default`:

- `default` — apply the framework's default policy table (Chapter 7.3) given the column's M-anchor and the reducer's intensive/extensive character. The most common choice.
- `skip` — use observed values only, with no rescaling. The right choice when the analyst specifically wants "total of observed" rather than "estimate of population total."
- `skip-and-rescale` — scale the observed reduction by `N_total / N_observed` (Chapter 7.4). Forces the population-estimate behavior even where the default would skip.
- `stratified` — apply the per-stratum correction explicitly, naming the strata.
- `propagate` — compute the marginal but carry it forward flagged as biased; a served number with its finding, never a withholding.
- `fill(constant)` — substitute a fixed constant for missing values before aggregation, e.g. `fill(0)` for "missing means zero in this domain." **`fill` substitutes a constant; it does not estimate.** Recovering a *plausible* value (rather than asserting a fixed one) is what skip-and-rescale and stratified do; `fill` is only for the case where a known constant is the correct modeling choice — and note that most of `fill(0)`'s former population was never a value rule at all but an undeclared universe statement, dissolved by the empty-bucket rule (Chapter 9.4; migration guidance in Chapter 22.1).

There is no `refuse` value, and the absence is deliberate (ADR-025): **withholding is never a missing-data treatment**, and the prior edition's "available as an explicit override anywhere the author wants a hard stop" is superseded. The author's instrument for a hard stop is **`WITHHOLD`** — a governance declaration, not a behavior: on a family entry it forbids serving that (column, reducer); on the column it forbids the column under any reducer. A triggered `WITHHOLD` is an *inform* outcome (Chapter 19) reporting the author's rule, its rationale where given, and the permitted alternative families. Governance and missing-data treatment are different axes, and the definition language (Part VIII) keeps them apart; the four-party control model is specified in the Frame-QL manual's Chapter 7.5. <!-- X1: ADR-020; ADR-025 (refuse retired; WITHHOLD) -->

Note what is *not* on this list: there is no `impute` policy. Earlier drafts folded constant substitution and statistical estimation together under an `impute(rule)` token; the v4 operator model splits them. Constant substitution is `fill`; estimation is what the principled skip-and-rescale and stratified behaviors already do. Collapsing the two invited authors to treat `impute(mean)` (an estimator) and `impute(0)` (a constant) as the same kind of act, when they have different soundness conditions.

The Core/Pro split runs along the estimation boundary, not through a single `impute` token. **Core** supports the constant `fill` and the principled rescale/stratify behaviors — the behaviors whose correctness conditions are stated and checkable. **Pro** adds *sophisticated estimators* — model-based and multiple imputation, inverse-probability weighting, selection-model corrections — but registers each as an additional named behavior in the operator registry (Chapter 8.3) that the missing-policy field may then invoke, not as values smuggled under an `impute` rule. The mechanism is uniform (the missing-policy field selects a registered behavior); only the catalog of available behaviors differs between Core and Pro.

This is the operational form of "column-spec is the single source of truth for column-specific concerns." The missing-policy is per-(column, reducer) because it is genuinely column-and-reducer-specific knowledge — `SUM(revenue)` may use the default skip-and-rescale, `SUM(units_returned)` may use `fill(0)` (missing returns means no returns), `LAST(price)` may use `fill` with a carried-forward constant where the domain warrants it. All of this lives where the column is declared.

#### 7.6 M-anchor propagation through operations

The M-anchor of a result column is computed from the M-anchor of the inputs and the nature of the operation.

**Map of one column.** Inherits the input's M-anchor — present where input is present, missing where absent, with the same mechanism. Exception: a map that produces a defined value at points where the input was absent (a `coalesce` or `if(is_missing(x), default, x)`) produces a column with MCAR-empty M-anchor if every point now has a value.

**Map of multiple co-anchored columns.** Missing at any point where any input is missing — the result's M-anchor is, conservatively, the *union* of the inputs' M-anchors. **MNAR is contagious**: combining an MNAR column with anything else produces an MNAR result.

**Aggregate.** Determined by how the input's M-anchor interacts with the aggregation. MCAR input → MCAR result (with rescaling for extensive). MAR on preserved coordinates → MAR on those coordinates. MAR on eliminated coordinates → policy table applies (propagate the flagged marginal). MNAR → the contagion is faithful: the result is MNAR, served as the observed-data figure carrying the `UNTESTABLE` finding; any acknowledgment that proceeds past a declared gate is recorded in the annotation and demotes the result's verdict to at most CORROBORATED, never a clean number. <!-- X1: ADR-020 -->

**Broadcast.** Preserves the input's M-anchor at each broadcast point.

**Subsetting.** Inherits the source's M-anchor over the restricted domain.

These rules are conservative and may be overridden on a derived column's spec where the conservatism is too coarse.

#### 7.7 M-anchor and dimension-role missing values

An important interaction: the M-anchor governs missingness for a column *in its measure role*. When a column is in the dimension role (an anchor component), the missing-value rules of Part II Chapter 5 apply — the prohibition on missing values in anchors, met by promotion to named values at binding time.

The two regimes coexist on the same physical column: a `customer` column may have missing values governed by its M-anchor in its transaction-attribute use, while the same column, when serving as an anchor component for `revenue @ {customer, day}`, must be missing-free with the absences promoted to a named `ANONYMOUS` value at binding. The promotion is binding-time; after promotion the column-as-dimension is missing-free, while the column-as-attribute may still carry its M-anchor. The framework applies the appropriate regime based on role.

---

### Chapter 8. The Column-Spec and the Operator Registry

The framework's column-and-operator knowledge is split between two places, each authoritative for what it knows:

- The **column-spec** is the single source of truth for *column-specific* knowledge: what a particular column's anchor is, what its M-anchor declares, what its family set contains and what each family entry's B-anchor and missing-policy are. Every piece of knowledge that varies *by column* lives on the column.

- The **operator registry** is the source of *operator-level* knowledge: facts about each operator that hold regardless of which column the operator is applied to. The registry is small by design — only four classes of operator-level fact appear in it.

This separation is the result of careful design. Earlier drafts of this manual had the registry accumulating column-specific overrides, implementation hints, and other things that properly belong elsewhere. The result was duplication and confusion. The simplified design has each fact in exactly one place.

#### 8.1 The column-spec

A complete column-spec records:

**Identity:**
- name
- value_type

**Value determination:**
- anchor
- universe binding (`ON` a declared universe, or the derived events projection for grain-rooted columns — Chapter 9)
- M-anchor (the mechanism declaration, including any MNAR flag)
- coverage declaration (treated in Part IV)

**Composition:**
- family_set: a set of family entries
  - each family entry: (reducer, B-anchor, missing-policy)
- default_family: the family entry that resolves a bare column reference

That is the complete column declaration. Everything about the column's behavior is here — what it is, where its values exist, how each of its reducers behaves including under missingness. Nothing about this column needs to be looked up elsewhere.

#### 8.2 The operator registry

For each operator the registry records exactly four operator-level facts:

**Algebraic signature.** The operation kind (map, aggregate, scan, broadcast, subsetting), order-dependence, input and output type rules, and — for reducers — the fertility classification (fertile, fertile-via-sketch-carrier, mule, ordered-reducer). This is what the planner consults to type-check expressions.

**Intensive/extensive bit** (for reducers), defined operationally as **rescale-corrigibility**. The bit answers one question — *if absent values are skipped, is the reducer's intended quantity biased, and does multiplying by (covered universe / observed) correct it?* — and a reducer is **extensive** exactly when both answers are yes (`SUM`, `COUNT`, `PRODUCT`: skipping undercounts a population quantity and the rescale repairs it) and **intensive** when skipping is already unbiased under MCAR (`AVG`, `MAX`, `MIN`, `LAST`, `FIRST`: a rescale would be wrong, so they merely skip). Exact mules with no fertile decomposition (`COUNT_DISTINCT`, `MEDIAN`) pass neither test — skipping changes their estimand and no multiplicative factor repairs it — so the registry carries them with their missing-value findings stating the residual bias rather than correcting it; and the bit remains independent of the B-anchor (applicability) and of fertility (rollability), three orthogonal facts about a (column, reducer) family per Chapter 6.2. <!-- review §2.9: rewritten as the operational rescale-corrigibility test -->

**B-anchor propagation rule.** An operator-level fact about how the B-anchor of the operator's output derives from the B-anchors of its inputs (per the rules of Chapter 6.5). Linear maps preserve; nonlinear maps go conservative; aggregate eliminates the aggregated families; broadcast preserves and adds the broadcast family to summing reducers' B-anchors; subsetting preserves; arithmetic combinations follow the additivity-character rules. The propagation rule is per-operator (not per-column) because it describes the algebra, not the specific column.

**Name aliases.** A list of names by which the operator can be invoked in queries against a Manifold using this registry. The canonical operator has its standard name (`SUM`, `AVG`, `APPROX_DISTINCT`); the registry may declare aliases for domain-specific vocabulary (`total` as alias for `SUM`, `unique_count` as alias for `APPROX_DISTINCT`, `closing_balance` as alias for `LAST` in a financial context). Aliases are resolved at parse time; they do not change the operator's behavior. A child Manifold (Part V) may extend the parent's aliases with its own without altering the underlying operators.

That is the entire registry. Four fact-classes, all operator-level. The registry does not duplicate the column-spec's B-anchor values (column-specific), does not duplicate the column-spec's missing-policy choices (column-specific), and does not specify implementation details (those live in the codebase, below the manual's level of abstraction).

#### 8.3 Pro extensions to the registry

Pro adds *operators and missing-data behaviors* to the registry — sophisticated estimators (model-based and multiple imputation, inverse-probability weighting, selection-model corrections), custom domain-specific reducers, allocation rules for many-to-many bridges. Each is registered with the same four fact-classes (algebraic signature, intensive/extensive bit, B-anchor propagation, aliases) and, for missing-data behaviors, named so the missing-policy field can select it. A Pro estimator is a *named behavior* the missing-policy field invokes (`model_based(features=[...])`), registered alongside the five Core behaviors `skip` / `skip-and-rescale` / `stratified` / `propagate` / `fill` — not a value smuggled under a generic `impute` token, which the v4 model removed, and not a withholding rule, which is governance (`WITHHOLD`), not a behavior (Chapter 7.5). <!-- ADR-025 -->

This is the principled extension point: Core ships the standard operators and the five default missing-data behaviors; Pro adds operators and estimators by registering them; column-specs select among the registered options by naming them in their family entries. The mechanism is uniform; only the catalog of registered behaviors differs between Core and Pro.

---

### Chapter 9. The Universe

<!-- X2: ADR-028 — new chapter; the specification-layer counterpart of the framework manual's universe chapter. Placed as Part III's closing chapter so that the column-spec remains Part III Chapter 8 (the BNF §3 pointer). Huayin execution call (1) lands in Chapter 7.1; D2–D7 of the universe brief are exercised here and confirmed in ADR-029. -->

#### 9.1 The universe in the column-spec: completing the grain

The framework manual establishes the ontology (its universe chapter): a datum's referent is a **point**; points belong to **universes** — declared point sets with a **basis**; the anchor is the *addressing scheme*, not the referent; and the complete grain everywhere in the framework is the pair ***(anchor, universe)*** — the anchor names the coordinates, the universe defines the points. This chapter specifies the contracts: how universes are declared, how the common cases are derived rather than declared, what the framework verifies about each basis, and the two rules — consequence and empty-bucket — that govern universes at query time.

The chapter completes Part III's account of value determination. The V-anchor (Chapter 3) says what coordinates address a column's points; the universe says which points exist under that addressing; the M-anchor (Chapter 7) says why values are absent at points that exist. The three are disjoint jurisdictions, and §9.7 pins the boundary.

#### 9.2 Declaration semantics: `UNIVERSE`, `BASIS`, `ON`

A universe is a named, Manifold-level object declared with a basis:

```
UNIVERSE active_stores     BASIS registry(store_directory)
UNIVERSE calendar_day      BASIS spine(day, from = 2024-01-01, to = current)
UNIVERSE store_days        BASIS product(active_stores, calendar_day)
-- events projections are derived from grain roots; declarable only for reuse:
UNIVERSE purchase_days     BASIS events(transaction, project = {customer, day})
```

The four bases and their semantics:

| Basis | Points exist because… | Canonical example |
|---|---|---|
| `registry(<entity_list>)` | an enumerated entity list says so | the store directory, a customer panel |
| `spine(<dimension>, …)` | a generator constructs them | the calendar of days, the hours of a year |
| `product(<universe>, …)` | the factors cross | active stores × calendar days |
| `events(<root>[, project = <anchor>])` | something happened | observed transactions; the customer-days on which purchases occurred |

A column binds to a universe with **`ON`** in its column-spec (`COLUMN eom_inventory … V_ANCHOR {store, day} ON store_days`). Three tiers of economy govern when anything is written at all: a column rooted at its own grain key **derives** its events projection and may not declare one (§9.3); an anchor or dimension family may carry a **default universe** its columns inherit (the calendar spine is the canonical case); and any column may **override** with `ON`. Two columns at the same anchor legitimately landing on different universes — `eom_inventory` on the store-day product, `units_sold` on the transaction projection — is the expressiveness the design exists for, now visible as two references to two named objects rather than two private toggles drifting apart in silence. "Sparse" and "dense" survive as teaching vocabulary; the grammar speaks universes and bases.

#### 9.3 The derivation rule

> **A column rooted at its own grain key lands on that root's events projection, by construction — and declaring it is not permitted.** `revenue @ {transaction}` is about transactions; the point exists because the event does; declaring the derivable is noise, and the framework rejects the redundant declaration at definition time.

The consequence is the tie-out property that matters most in practice: for event-rooted data — most of what commerce sums — the framework's total equals the source system's total by default, and reconciliation against the warehouse passes with nothing declared. The estimation machinery of Chapter 7 fires only where an author has *deliberately* declared a dense universe and a missingness mechanism — which is exactly where the conventional sum is the number that should not be trusted.

Where the data leaves the reading open — the same physical table at `{customer, day}` supports both "purchases" and "expected daily activity" — the universe choice is a **declaration, never an inference**: the data cannot settle intent. Processing code is the best *proposer*: a calendar-spine join in the feeding pipeline is a dense tell, a bare GROUP BY over an event table a sparse tell, and Discover proposes universes with that evidence attached while the author decides.

#### 9.4 The consequence rule, query-level `ON`, and the empty-bucket rule

Every ascription is implicitly `expr @ (a, U)`, and the universe component belongs to the **destination**. When `U` is unwritten, the **consequence rule** supplies it: *the output frame's point set is the contributing columns' covered universes, brought to the output anchor* — sparse in, sparse out; no point is manufactured that the data never asserted. When the writer wants a different destination — most often a reporting grid over the full spine — the universe is pinned at the output anchor with the query-level `ON` form:

```
SELECT sum(units_sold @ {transaction}) AS units
AT {store, month} ON store_month_grid
```

Default by disclosure, pin by syntax: the resolved `(anchor, universe)` of every series always rides in the result's annotation, so the defaulted parameter is never a hidden one.

What renders at a bucket no input point feeds is the destination's decision, by one rule stated once:

> **The empty-bucket rule.** Over a declared universe (registry, spine, product), an empty bucket's `SUM` and `COUNT` are **true zeros** — counting nothing is a defined act — while its order statistics and means are **absent**. Over an events projection, the empty bucket is **not a point**, and nothing is rendered.

This is the rule the bracket filter resolves to (the bracket restricts the *event set*; the destination universe decides the rendering), the answer to the empty-group question (the group exists or it doesn't, per the destination; if it exists, sum zero, mean absent — see Chapter 4.2), and the dissolution of most of `fill(0)`'s former population (Part VII Chapter 22.1).

#### 9.5 Co-universality

A common anchor is, in full, a common *(anchor, universe)*. When a query combines columns at a shared anchor, the framework checks **co-universality** — the other half of co-anchoring, and the proper object of the universe-integrity machinery (Chapter 11):

- **Same declared universe** — verified *by reference*: the two columns name the same object. The strongest and cheapest verdict in the framework.
- **Same by declaration, differing point sets in fact** — the drift finding, now stated against a named object rather than a vague expectation, with the divergence quantified.
- **Different universes outright** — an events projection combined with a spine, observation compared against expectation: a *legitimate* combination, served with its permanent asymmetry disclosed; never silently treated as same-points, and never withheld for being what it honestly is.

#### 9.6 Verification by basis

The universe layer's epistemics follow the certificate's standing rules, and what is checkable is proportional to the basis:

| Basis | What the framework verifies | Evidential character |
|---|---|---|
| events projection | nothing about the universe itself ("universe ≡ observed" is the definition); the load shifts entirely to cross-column co-universality checks | the tautology, converted into a checkable cross-column assertion |
| registry | referential integrity, both directions: every point's entity exists in the roster, and every roster entity that should carry points does | checkable |
| spine | density: the fraction of declared points carrying records, and its distribution | checkable |
| product | factor integrity plus density over the cross | checkable |

The universe *choice* itself — events or expected, this registry or that spine — is **asserted in principle** (the same physical shape supports both readings; no data check settles intent) but **corroborable at the code-verified rung**: the spine-join and GROUP-BY tells in the feeding pipeline are exactly what source inspection attests, and Discover attaches them as evidence to its proposals. Density measurement over dense bases is also where a declared MCAR earns its falsification tests (Part VII Chapter 23.3). Throughout, the safety asymmetry holds: a drift, a totality violation, or a registry orphan contradicts; a clean pass corroborates, and never silently verifies an assertion about the world.

#### 9.7 The four-layer factorization and the jurisdiction rule

With the universe named, the framework's treatment of "what's there and what isn't" factors into four layers — the chapter sequence of this manual now mirrors it:

| Layer | Question | Declared where | Integrity machinery |
|---|---|---|---|
| 1. Defining boundaries | what is this data space *about*? | Manifold-level (Chapter 10) | boundary satisfaction checks |
| 2. Coverage | which *region* of the boundaries does this column address? | column-spec (Part IV) | coverage verification, drift |
| 3. Universe | which *points exist* within the covered region? | universe references (this chapter) | basis checks, co-universality, totality |
| 4. M-anchor | why are *values* absent at existing points? | column-spec (Chapter 7) | falsification checks, policy table |

Two pins everything downstream leans on:

> **The jurisdiction rule** *(design principle)*: the M-anchor governs **value-presence at universe points**; **point-existence** belongs to the universe. The two never overlap, and they compose. A transaction that happened with an uncaptured amount is a point that exists with an absent value — real missingness, with the record count as denominator. An expected store-day reading that never arrived is likewise a point with an absent value — real missingness, with the spine product as denominator. A purchase that didn't happen is *not a point*, and no mechanism may be declared over it: asserting one would claim the expected revenue of a non-purchase, the inflation absurdity the rule exists to make unrepresentable.

> **N_total is the covered universe**: the denominator of every estimation behavior (Chapter 7.4) is the cardinality of the column's universe *within its coverage*. Rescaling estimates the total over the covered points, never beyond them; extrapolation past coverage is coverage's finding to disclose, not the rescale's job to attempt.

---


## Part IV — Degeneracy and Coverage

This is Part IV of the reference manual. Parts I–III specified types and operators, anchors and dimensions, and applicability, missingness, and the universe. This part specifies degeneracy and coverage — layer 2 of the four-layer factorization of "what's there and what isn't" (boundaries → coverage → universe → M-anchor, Chapter 9.7) — and the universe-integrity machinery, whose object is co-universality, that makes cross-column soundness tractable. <!-- X2: ADR-028 / D3 -->

The treatment is at framework-contract scope: what coverage *means* for a Manifold, what the framework *promises* about it, what authors and queries can rely on. The operational machinery around coverage — how matrices are persisted, how drift detection produces alerts, how monitoring dashboards consume the data — is platform implementation, addressed in the codebase and platform documentation, not specified here.

The treatment rests on a principle the conceptual manual established: absence is permitted in Columna only when it is explicitly and completely specified. Missing values are permitted under a declared M-anchor; missing dimension values are permitted by promotion to named categories; absent points are permitted as the content of a declared universe; missing *coverage* — a column addressing less than the Manifold's defining boundaries — is permitted only when an explicit degeneration is declared. The four are instances of one rule applied at four levels. <!-- X2 -->

This part presumes the prior parts and the conceptual manual.

---

### Chapter 10. Defining Boundaries and Degeneracy

#### 10.1 What defining boundaries are

The conceptual manual established the Manifold's component set, including its **defining boundaries** — the constraints that define what *this Manifold is about*, shared by every column in the Manifold.

Defining boundaries are typically of two kinds:

**Temporal**: the range of time the Manifold's data covers. "Activity from 2020-01-01 through current refresh." "The most recent twelve months, rolling."

**Dimension-value-subset**: the subset of a global dimension's values the Manifold addresses. "US customers." "The consumer product line." "Internal employee accounts."

Defining boundaries are *constitutive* of the Manifold — they are what the Manifold is *about*, not filters applied to it. A US-only Manifold is not "a Manifold containing globally-bound columns each filtered to US"; it is a Manifold whose defining boundaries *are* US. Every column in it operates within those boundaries by definition. The boundary is not a per-column declaration; it is declared once for the Manifold and applies uniformly.

The `{}` anchor of any Manifold (Part II Chapter 3.2) is precisely the Manifold's defining boundaries taken as a single anchor point. Aggregation to `{}` is aggregation over what the Manifold is about, which is what the defining boundaries declare.

#### 10.2 What degeneracy is, in distinction from boundaries

A column is **degenerate** when it covers less than the Manifold's defining boundaries would otherwise have it cover. Where the defining boundaries are a Manifold-level property shared by all columns, degeneracy is a column-level property describing how a *particular* column relates to those boundaries.

The distinction is structural and worth being precise about:

- **Defining boundaries** describe what the Manifold *is*. Shared by all columns. Constitutive.
- **Degeneracy** describes how a particular column relates to the Manifold's defining boundaries. Per-column. A deviation from "covers the full Manifold scope."

If the Manifold's defining boundaries are "US customers since 2020," then a `revenue` column covering all US customers since 2020 is *complete* (it covers the Manifold's scope). A column covering only "US enterprise customers since 2020" is *filtered* — a further restriction beyond the Manifold's scope, declared as an explicit predicate. A column whose coverage is *unspecified* (incompleteness suspected but not characterized) is *quarantined*.

This is the third coverage taxonomy referred to throughout the manual:

**Complete** — the column covers the Manifold's defining boundaries fully (modulo missing values characterized by M-anchor). The default and most common case for primary columns. The framework verifies completeness against the boundaries and records it in the integrity certificate.

**Filtered** — the column covers a declared subset of the Manifold's defining boundaries, restricted by an explicit predicate. The restriction may be temporal (a column covering only the most recent ninety days within a multi-year Manifold), dimension-value-based (a column covering only enterprise customers within an all-customers Manifold), or a combination. What was earlier called "truncated" coverage (temporal boundary) and "sampled" coverage (sampling design as restriction) both fall into this category — they are filtered with specific kinds of restriction. The framework verifies the data satisfies the restriction and the column's data is declared usable for the analyses scoped within its restriction.

**Quarantined** — the column has unspecified or unusable incompleteness. Either the incompleteness has not been characterized (the data is known or suspected to be incomplete but no restriction has been declared) or the column has a verified defect that makes it unsuitable for analysis. Quarantined columns are not usable in operations; queries touching them in cross-column combination yield an *inform* — the author's standing coverage governance, reported with its remediation — until the incompleteness is addressed (declared with a verified restriction → filtered, or addressed at the binding level → complete). <!-- X1: ADR-020 -->

The taxonomy is the operational form of "absence permitted only when explicitly specified." Complete columns have no absence to specify. Filtered columns have explicit restrictions. Quarantine is the framework's reporting that unspecified incompleteness has not been declared usable — the one coverage state that yields no result, and it is the author's standing governance, not the engine's judgment.

#### 10.3 Coverage is not query-time restriction

A critical distinction: the coverage taxonomy describes *Manifold-level column states* — facts about what data the Manifold's columns contain. It does not describe query-time restrictions.

Frame-QL supports two kinds of query-time restriction — `where` (predicate restriction before aggregation) and `having` (predicate restriction on aggregation results) — and Part I specified the subsetting operation that restricts a column's domain in an expression. These are *expression operations* that produce restricted query results. They are not Manifold-level column states. The Manifold's `revenue` column remains complete after a query writes `where region = 'east'`; the query's result is restricted, but the column itself is unchanged.

This distinction matters because the planning machinery's coverage checks apply to *column states*, not query restrictions. The planner asks "what is each column's coverage type" (complete, filtered, or quarantined) and proceeds accordingly. Query-time restrictions further narrow what an expression operates on, but they do not change column states.

#### 10.4 How coverage is declared

A column's coverage is declared as part of its column-spec — the column-spec field accumulated across the manual. The shape:

For a complete column, the default (no declaration needed, or `coverage: complete` stated explicitly).

For a filtered column, the declaration names the restriction. The restriction may be a predicate (`coverage: filtered(predicate)`), a sampling design (`coverage: filtered(sampling=random, fraction=0.01)`), or a temporal boundary (`coverage: filtered(after=2020-01-01)`).

A column whose coverage is not declared and whose data the framework finds incompletely covers the Manifold's boundaries is treated as quarantined until the author declares it.

#### 10.5 What coverage implies for operations

A column's coverage state affects how it can participate in queries.

**Only complete and filtered columns participate in planning.** Quarantined columns do not participate; the outcome for a combination touching one is an *inform* naming the author's standing coverage governance, and the remediation is to declare coverage or address the underlying defect. <!-- X1: ADR-020 -->

**Combining columns with matching coverage proceeds normally.** Two complete columns combine over the Manifold's defining boundaries. Two filtered columns with the same restriction combine over that restriction. The result inherits the appropriate coverage.

**Combining columns with different filtered coverages requires the framework to check whether the intersection of restrictions is meaningful.** If both columns are filtered — one to "US customers" and another to "since 2020" — the combination is meaningful over the intersection ("US customers since 2020"), which the result's annotation states. If the restrictions are disjoint (a column filtered to "before 2018" combined with one filtered to "after 2020"), no data supports the combination and the framework returns no result, **informing** — a data-gap outcome, not an analytical judgment. <!-- X1: ADR-020 -->

**Sampling restrictions combine differently from predicate restrictions, and the framework says so.** Two columns each filtered by an *independent* random sample intersect, in expectation, on the product of their fractions — two independent 1% samples share about 0.01% of the universe — a statistically different object from a predicate intersection, and rarely the analysis anyone intends. The combination is served over the realized intersection with a **critical** disclosure quantifying the surviving fraction, unless the samples are declared *coordinated* (drawn over the same units), in which case they combine like any shared restriction. <!-- ADR-025 (3): the owed sampling-combination paragraph -->

**Combining a complete column with a filtered column produces a result restricted to the filtered column's restriction.** The complete column is interpreted as covering everything within its scope; restricting to a subset still yields well-defined values; the result's coverage records the inherited filter.

These rules are stated as contracts. The framework owes the author that combinations producing meaningful results are served with their coverage stated, that combinations no data supports yield informs with reasons, and that combinations carrying risk carry it quantified; the specifics of how the planner makes the check are implementation.

---

### Chapter 11. Universe Integrity Across Columns

#### 11.1 The principle

Every column in a Manifold operates within the same defining boundaries. The framework's universe-integrity machinery checks that the data the Manifold is bound to is consistent with this — that columns claiming to cover the Manifold's defining boundaries actually do, that columns claiming filtered coverage actually satisfy their restrictions, and that pairs of columns claimed to address the same population do.

This last check is the most subtle and the most valuable, and it has — since the universe became first-class (Chapter 9) — a named object: **co-universality**. Two columns in the same Manifold, both anchored on `customer`, both declared complete, are presumed to describe the same population of customers. If revenue covers 1.2 million customers and support_tickets covers 800 thousand customers, the columns are not co-universal despite both being declared complete — and any analysis that combines them at the customer grain will be biased by the gap. The check's three verdicts follow Chapter 9.5: same declared universe, verified by reference; declared-same but drifting in fact, the drift finding with the divergence quantified; different universes outright, a legitimate combination served with its permanent asymmetry disclosed.

The framework owes the author: this kind of cross-column population mismatch is detected and surfaced on every result that depends on it. Conventional tools do not detect it; queries against mismatched columns produce numbers whose silent bias is invisible. <!-- X2: U.6 / D3(b) -->

#### 11.2 What the framework maintains

For each dimension that appears in multiple columns' anchors, the framework maintains information about how those columns' populations of that dimension actually compare. Sufficient information is preserved that the planner, the integrity machinery, and (in Pro) operational monitoring can determine whether two columns are addressing compatible populations and whether that has changed over time.

The framework's contract is what authors and queries can rely on:

- For any two columns in the Manifold anchored on a shared dimension, the framework can answer "how do their populations compare on this dimension" — overlap, asymmetric differences, or in the simplest summary, a compatibility judgment.
- This information is computed at refresh, when the underlying data is consulted, and is current to the most recent refresh.
- The information is part of the integrity certificate, queryable by users, the planner, and the agent.

The specifics — what data structure carries the information, how it is persisted, how incremental updates work as columns refresh, how thresholds are set for compatibility judgments — are platform implementation. The contract is the answerability and the certificate-tracking.

#### 11.3 Stratified coverage

A global population-compatibility judgment ("revenue and support_tickets overlap 70% on customer") can mask structural patterns. If the 30% gap is random, it is a sampling artifact; if it is systematic (all enterprise customers, or all customers in one region), it is a structural bias that distorts segment-level analyses.

The framework supports stratified coverage: for declared stratification dimensions (typically the few dimensions along which structural biases are most plausible), the framework computes coverage broken down by stratum. "Revenue/support_tickets coverage by region" reveals whether the gap is uniform or structured.

Stratified coverage is declared per Manifold (which dimensions to stratify on), not computed along every dimension automatically — stratification along all dimensions would be prohibitively expensive at scale. The choice of which dimensions to stratify on is an authoring decision (Part VII).

#### 11.4 Drift detection

The history of cross-column population information is itself analytically valuable. The framework maintains, at each refresh, a snapshot of the coverage state; the history of snapshots reveals **drift** — slow changes in cross-column compatibility over time.

A drift event is a significant change in coverage between refreshes: revenue and support_tickets that historically overlapped 95% on customer suddenly overlapping 70%. The framework detects such transitions and records them in the integrity certificate's event log.

In Core, drift is detected and recorded. In Pro, the operational monitoring infrastructure — alerts, dashboards, escalation — consumes the events and turns them into operational signals. The detection itself is correctness machinery (Core); the operational surfaces around it are operations machinery (Pro). The Core/Pro line falls where the data being verified by Core becomes the data being acted on by Pro.

This is the framework's most distinctive integrity contribution: catching slow-onset universe drift, the kind of corruption that develops over weeks or months as upstream pipelines drift apart, that conventional warehouses surface only when someone notices a dashboard looks wrong. Columna surfaces it the moment it crosses the threshold.

#### 11.5 Coverage in queries

When the query planner builds an execution plan, it consults the coverage information for any combination of columns in the query. The planner's outcomes follow the general taxonomy (Chapter 19), specialized to coverage:

**Serve.** The columns' coverages are compatible; the query executes; the result's coverage records the appropriate inheritance; no coverage finding fires.

**Serve, with the coverage disclosed.** Coverage is restricted or gapped: the query executes and the annotation carries the universe the answer reflects — the intersection served over, the overlap percentage, the asymmetric gap and its bias direction — at a severity that scales with the gap against the Manifold's configured thresholds. Presentation gates on severe findings (acknowledgment before display) are a surface decision, never API-level withholding.

**Inform.** Disjoint restrictions (no data supports the combination — a data gap) or a quarantined column (the author's standing coverage governance, reported as the author's rule with its remediation). These are the only coverage paths that yield no result, and neither is the engine's analytical judgment.

The severity thresholds are configured per Manifold — different domains have different tolerances. Financial reporting may grade gaps critically; exploratory analytics may grade them permissively. The configuration shapes disclosure severity and surface behavior, never whether a determinate, entitled result is produced. <!-- X1: ADR-020 — old proceed/marginal/refuse taxonomy superseded -->

#### 11.6 Coverage and the agent

The Columna agent uses coverage information as part of its clarifying dialogue with users. When a request combines columns across a coverage gap, the agent surfaces the gap in business vocabulary: *"Revenue and support tickets overlap 70% on customer — do you want me to restrict to the overlapping customers, or proceed with the gap and note the resulting bias?"* This is the analyst-grade dialogue the agent's design promises, grounded in evidence the substrate maintains. No conventional tool can ask this question because no conventional tool has the coverage data to ground it in.

---

## Part V — Composition

This is Part V of the reference manual. Parts I–IV specified types and operators, anchors and dimensions, applicability and missingness, and degeneracy and coverage. This part specifies composition — how a Manifold is built from existing Manifolds — at the level of the framework's contracts: what inheritance permits and requires, what joining requires, what versioning provides.

The detailed mechanics of multi-Manifold management — composition graphs across many Manifolds, organization-wide governance, impact analysis, operational coordination across a fleet — are a layer above the framework, deferred to its own treatment when that layer's design is worked through. This part addresses the framework-level composition contracts; the multi-Manifold management layer builds on these but is not specified here.

This part presumes the prior parts and the conceptual manual.

---

### Chapter 12. Composition and the Component Set

#### 12.1 What composition operates on

The conceptual manual establishes that a Manifold's component set comprises:

- **Column set** — both anchors (dimensions) and values (metrics), all the columns the Manifold addresses.
- **Defining boundaries** — what the Manifold is about (typically temporal and dimension-value-subset constraints), shared by all columns.
- **Operator subset** — which operators the Manifold makes available, with their name aliases.
- **Derived columns** — derived metrics and derived dimensions, defined by expressions over the column set.
- **Custom functions and reducers** — extensions to the operator set specific to this Manifold (Pro).

Composition operates on these components. To compose two Manifolds is to derive a new Manifold whose component set is a principled combination of the parents' components, with conflicts resolved by explicit declaration.

#### 12.2 Two composition forms

The framework provides two composition forms:

**Inheritance** is asymmetric. A child Manifold inherits from a parent by adopting the parent's components and adding refinements. The child becomes a Manifold that *narrows or extends* the parent without contradicting it.

**Joining** is symmetric. Two Manifolds are combined into a peer Manifold that contains both their components, with shared elements (typically dimensions) reconciled.

Both forms preserve the closure property: composing Manifolds yields a Manifold, with the same algebraic guarantees, the same integrity machinery, the same queryability. The composed Manifold is, in every sense the framework cares about, a Manifold — and is itself further composable.

---

### Chapter 13. Inheritance

#### 13.1 What inheritance permits

A child Manifold may:

- **Narrow the defining boundaries.** The child's defining boundaries are a subset of the parent's — typically a further restriction (the parent covers all customers; the child covers EU customers only). The framework verifies the narrowing against the data.

- **Add columns.** Both new primary columns (with their own bindings) and derived columns (computed from the parent's columns or the child's additions). New columns are scoped to the child.

- **Extend a parent column's family set.** The child may add new family entries (new reducers with their B-anchor and missing-policy) to a parent column. The parent's existing entries remain.

- **Override missing-policy or other column-spec behaviors.** Per-(column, reducer) overrides declared on the child's view of a parent column are scoped to the child's queries.

- **Add integrity assertions.** New preconditions specific to the child's domain, verified against the child's data.

- **Extend the operator-registry aliases.** New domain-specific names for operators, valid in the child without affecting the parent.

#### 13.2 What inheritance forbids

A child may not:

- **Widen the defining boundaries.** The child's defining boundaries must be a subset of the parent's. A child cannot inherit from a US-customer parent and claim to cover global customers; for that scope, a different parent (or a join) is needed.

- **Remove or contradict parent declarations.** No deleting parent columns, no breaking parent hierarchy edges, no loosening parent B-anchors, no declaring missing-policies that would produce results the parent's declarations forbid.

- **Override verified integrity assertions.** A precondition the parent verified holds in the parent's defining boundaries; the child inherits it as verified, and the child's own data is checked against it within the child's boundaries.

These restrictions enforce the principle that inheritance is *refinement*: the child is a more constrained version of the parent. The parent's contracts hold in the child; the child adds more. This is what makes the parent's correctness guarantees flow to the child without separate re-verification of what the parent already established.

#### 13.3 Verification

The framework verifies the child's declarations relative to the parent: the boundary narrowing against the parent's boundaries and the data, the inherited FD edges against the child's narrower scope, each refinement on its own terms. The child's integrity certificate is *derivative* — it inherits the parent's verified state and adds the child's own verifications. Queries against the child consult the child's certificate, which transitively depends on the parent's.

---

### Chapter 14. Joining

#### 14.1 What joining requires

Joining combines two Manifolds into a peer Manifold containing both their components. Where inheritance is one-direction-constrained, joining is symmetric, and reconciliation is the substantive work.

A join declaration specifies, for each shared element (typically dimensions, possibly columns or operator behaviors), how the two parents' versions are reconciled. The framework requires explicit reconciliation for substantive conflicts; it does not silently choose between parents.

What requires reconciliation:

- **Shared dimensions.** Whether two same-named dimensions in the parents are the same dimension (with compatible hierarchies and domains), are distinct dimensions to be renamed, or are in a hierarchy relationship.

- **Shared dimension hierarchies.** Whether parents' hierarchies on a shared dimension agree, whether one is a refinement of the other, or whether they conflict.

- **Defining boundaries.** What the joined Manifold's defining boundaries are — typically the intersection of the parents' boundaries, optionally narrowed or (where parents' data supports it) more broadly defined.

- **Shared columns.** Same-named columns in the two parents must be reconciled: declared the same (with compatible declarations), renamed to disambiguate, or one selected and the other dropped.

- **Operator behaviors and aliases.** Where the parents have different aliases for the same operator name, or different missing-policy overrides for a shared column, the join declares which prevails.

The framework refuses joins with unresolved reconciliations; the explicit declaration is required, the framework verifies the declaration against the data, and the result is recorded in the joined Manifold's certificate.

#### 14.2 What joining produces

A successful join produces a Manifold whose:

- **Column set** is the union of both parents' columns, with reconciled same-named columns merged or renamed.
- **Defining boundaries** are the declared composition (intersection by default).
- **Dimensions and hierarchies** are the union with shared elements reconciled.
- **Operator subset** is the union with conflicts resolved.
- **Integrity certificate** is derived from both parents' certificates plus the join's reconciliation verifications.

The result is, in every operational sense, a Manifold: it carries all four strata of structure, it has an integrity certificate, it is itself composable. The closure property of composition holds.

#### 14.3 Cross-parent coverage and reconciliation

The cross-column coverage machinery from Part IV plays an operational role here. When two parents' columns are anchored on a shared dimension and the dimensions are declared identical in the join, the framework computes cross-parent coverage on that dimension — how the parents' populations actually compare. This evidence informs the join's reconciliation: a join that declares "customer is the same dimension in both parents" can be checked against actual customer-population overlap, and the composer sees the numbers (85% overlap, with specific asymmetric coverage) before accepting the join.

This is the level at which framework-level composition meets multi-Manifold management: the framework provides the evidence; the composer decides. How the evidence is presented, how impact analysis aggregates it across many composed Manifolds, how governance policies enforce minimum overlap thresholds — these are multi-Manifold management concerns, not specified in this framework manual.

---

### Chapter 15. Versioning

A Manifold is a versioned artifact. Each substantive change to a Manifold's components — adding or removing a column, modifying a B-anchor, modifying a hierarchy edge, changing defining boundaries — produces a new version. The version is part of the Manifold's identity; "the finance Manifold" without a version is underspecified.

Versioning is what makes composition stable and past analyses reproducible. A child Manifold inherits from *a specific version* of the parent; a join references specific versions of its parents; an analysis from last quarter cites the version of the Manifold it was computed against. The framework owes reproducibility: an analysis stated as "from Manifold X version 7, refresh date Y, certificate state Z" must be reproducible by checking out version 7 against the data as of refresh Y.

A version is more than a label — it is the actual set of declarations, integrity preconditions, and operator registry as they stood at that version. Two distinct versions may share most of their declarations and differ only in one column's B-anchor; the framework records the difference and treats them as distinct artifacts.

At the query level, the same identity is addressable in Frame-QL: `FROM <Manifold> VERSION <n>` pins a statement to a version, and a bare `FROM` resolves to the current published version with the resolved identity — `(Manifold, version, refresh, certificate state)` — always recorded in the result's annotation. Default by disclosure, pin by syntax. A consequence worth naming: because the annotation always carries the canonical form of the statement as executed together with the resolved identities, **every result is its own reproduction recipe** — an unpinned analysis from last quarter is exactly reproducible from its own annotation, with no surrounding context required. <!-- ADR-027 -->

The detailed mechanics of version storage, version-difference computation, and version-aware composition resolution are platform concerns. The framework's contract: Manifolds have versions, composition references versions, reproducibility is guaranteed for cited versions — and for uncited ones, recoverable from any result's annotation.

---

### Chapter 16. What Composition Preserves

The closure property — Manifolds compose to Manifolds — is meaningful only if composition preserves the correctness guarantees that make a Manifold valuable. Composition preserves:

**The algebraic guarantees.** Well-formedness rules, B-anchor checking, M-anchor propagation, fertile/mule classification — all apply uniformly in composed Manifolds because they apply to the columns and operators, which carry their declarations forward through composition.

**The integrity certificate.** Derivative: parents' verified preconditions remain verified in the composed Manifold (scoped to the columns and operations that depend on them), and the composition adds its own preconditions (reconciliation verifications) that are verified at composition time.

**Outcome behavior.** A query against the composed Manifold that depends on a precondition violated in either parent (or in the reconciliation) carries that finding — routed around where a sound route exists, served with the contradiction disclosed otherwise, withheld only on the standing governance paths — with the failure named and traceable to its origin (which parent, or the reconciliation step). <!-- X1: ADR-020 -->

What composition does *not* automatically preserve — and what the composer must address — is consistency where the parents' declarations differ substantively. Conflicting hierarchies, divergent missing-policies, mismatched defining boundaries: the composer declares the resolution and the framework verifies it. The result is a composed Manifold that is as correct as its parents and as correct as the composer's resolutions — never silently less correct than either.

---

## Part VI — Integrity

This is Part VI of the reference manual. Parts I–V specified types and operators, anchors and dimensions, applicability and missingness, degeneracy and coverage, and composition. This part specifies integrity: the layered preconditions whose verification makes a Manifold's analytical claims sound, the certificate that records their state, and the outcome discipline — serve, disclose, clarify, inform — that ties them to query behavior.

A point of framing must come first, because it changes how integrity should be understood: **the integrity preconditions are not Columna's conventions about what makes a Manifold well-formed. They are the data conditions that any correct analysis on the data would require, regardless of what tool performs the analysis.** A functional dependency that fails — customer 19847 mapping to two regions — is a defect in the data, present whether you query it through Columna or any other tool. Columna uncovers and reports such defects because it checks; conventional tools do not check and so produce wrong answers silently. The framework's contribution is not adding rules but *verifying rules that have always been there* — and never producing a silent answer against them: where the data lacks what analysis requires, the defect rides the result, named and quantified. <!-- X1: ADR-020 -->

This is why the language of this part avoids "well-formed" and "well-formedness" — those words carry a connotation of "conformance to the system's own conventions" (familiar from query-language well-formedness, where it correctly applies to expression grammar). Integrity is not Columna's conventions; it is the data's soundness for analytical use. The words this part uses are *sound*, *soundness*, *valid*, *validity*, where the prior draft used "well-formed."

The treatment is at framework-contract scope. What the framework promises about integrity belongs here; how it operates continuous monitoring, alerting infrastructure, certificate persistence — these are platform implementation, deferred to their own documents.

---

### Chapter 17. The Layered Preconditions

#### 17.1 What the layers do

A Manifold's analytical claims are sound when all of its declared integrity preconditions are satisfied. Preconditions are *layered*: each governs a specific aspect of data soundness, and the failure of a precondition invalidates a specific *scope* of operations — those that depend on what the precondition governs — rather than the entire Manifold.

The layering matters operationally. Without scoped invalidation, a single broken functional dependency would smear a finding across the entire Manifold. With scoped invalidation, the broken edge implicates only the climbs along that edge; the rest of the Manifold stands; queries against unaffected portions serve clean. This is what makes the disclosure discipline precise rather than noisy: a finding fires for exactly the results that depend on the defect, and nowhere else. <!-- X1: ADR-020 -->

This chapter enumerates the six layers — anchor, co-anchoring, hierarchy, applicability, universe, and coordinate totality — what each governs, what each precondition's failure implicates, and which preconditions are verifiable from data versus asserted by the author.

#### 17.2 The six layers

**Layer 0 — Anchor soundness.** Governs the basic structural validity of the Manifold's columns.

*Preconditions:*
- Each anchor's coordinate combinations uniquely identify its points (Part II 3.1).
- Each column serving in the dimension role contains no missing values in that role; absence has been promoted to named categories where applicable (Part II 5.2).
- Each column is a total or partial function on its anchor, with partiality characterized by its M-anchor.

*Verifiability:* checkable from data. The framework verifies uniqueness, identifying-completeness, and M-anchor-consistent partiality at every refresh.

*Blast radius:* failures of Layer 0 invalidate the affected column entirely — the column cannot serve as the basis for any query until the data defect is addressed.

**Layer 1 — Co-anchoring soundness.** Governs the validity of multi-column operations.

*Preconditions:*
- Columns declared co-anchored actually share their anchor's points (not merely the same anchor specification, but identical observed point sets where the declaration claims identity).

*Verifiability:* checkable from data. Verified by comparing the anchors' value sets across columns.

*Blast radius:* invalidates expressions that combine the mis-anchored columns by map. A column may still be queried in isolation or combined with other columns that *are* validly co-anchored with it.

**Layer 2 — Hierarchy soundness.** Governs the validity of dimension-family roll-up edges.

*Preconditions:*
- Each declared roll-up edge is a total functional dependency over the Manifold's defining boundaries: every child value present maps to exactly one parent value (Part II 4.3).
- Where multiple edges form a commuting diagram, the composition is consistent (Part II 4.4).

*Verifiability:* checkable from data.

*Blast radius:* failure of an edge invalidates climbs along that specific edge. Other edges and other dimensions are unaffected.

**Layer 3 — Applicability soundness.** Governs the validity of declared B-anchor claims for each (column, reducer) pair.

*Preconditions:*
- For each column and each reducer in its family set, the declared B-anchor is consistent with the data's behavior. Specifically: if the B-anchor claims a reducer *is* applicable along an axis (the axis is not in the B-anchor), the data must support that claim.

*Verifiability:* partially checkable. The framework can perform consistency checks (verifying behavior under each reducer is consistent with the declared B-anchor), but cannot fully verify from data alone — the assertion that a quantity is extensive along an axis is partly a modeling claim that data can falsify but cannot strictly confirm.

*Blast radius:* failure invalidates queries that depend on the broken claim — specifically, aggregations using the affected reducer along the disputed axis. The column under other reducers, or along axes where the B-anchor is verified, remains usable.

**Layer 4 — Universe soundness.** Governs the consistency of the Manifold's defining boundaries with its column-level coverage claims, and the compatibility of columns claiming the same universe.

*Preconditions:*
- The Manifold's defining boundaries are satisfied by all column data — every column's data lies within the Manifold's declared scope.
- Each column's coverage declaration (complete or filtered) is consistent with its data (Part IV).
- Columns combined at a shared anchor are **co-universal** as declared (Chapter 9.5): same declared universe verified by reference; declared-same-but-drifting surfaced as the drift finding; different universes preserved with the asymmetry disclosed. <!-- X2: U.6 -->

*Verifiability:* checkable from data for the boundary-satisfaction and coverage-declaration aspects. Cross-column compatibility is data-checkable. The *definition* of the defining boundaries themselves (the declaration that the data is "US customers in 2024") is not verifiable — the framework checks consistency with the declaration but cannot independently confirm the declaration corresponds to a real-world universe.

*Blast radius:* coverage failure invalidates the column for cross-column operations. Cross-column compatibility failure invalidates the specific combinations affected.


**Layer 5 — Coordinate totality (conservation soundness).** Governs the path-independence of fertile families' totals.

*Preconditions:*
- Every root point of a fertile family carries a value for every dimension family any aggregation path traverses: no null coordinates at the root, no orphan children, every traversed child mapping to exactly one parent. (Per-edge functionality is Layer 2's precondition; totality adds that *no root point falls out of any path*.) Together with path-invariance (enforced by type) and one root point set feeding every path (universe references, checked as co-universality under Layer 4), this is the checkable core of the conservation invariant (Chapter 9.7; the framework manual's universe chapter).

*Verifiability:* checkable from data — null-coordinate counts and orphan counts per traversed dimension family, measured at every refresh.

*Blast radius:* a totality violation invalidates the aggregation paths through the deficient dimension and nothing else, with a disclosure that is quantifiable rather than gestural: "the region path excludes 312 transactions (0.4% of total) carrying null region; the customer path includes them." <!-- X2: U.7 / D4 — new layer per charter -->

#### 17.3 Asserted preconditions

In addition to verifiable layers, a Manifold carries preconditions that are *declared, not verifiable*:

- **The MNAR flag on a column's M-anchor**: whether missingness depends on the unobserved value itself is not testable from observed data. The framework records this as asserted, applies the appropriate disclosure (the observed-data figure with the `UNTESTABLE` finding), and notes its status in the certificate. <!-- X1: ADR-020 -->

- **The defining boundaries themselves**: the framework checks that data is consistent with declared boundaries (no non-US customers in a US-declared Manifold), but cannot independently confirm the label corresponds to a real-world category.

- **B-anchor character overrides on derived columns**: where the framework's conservative default propagation is overridden by an author's declared character claim.

Each precondition is tagged by its **evidential basis** — *checkable* (the data can confirm or contradict it) or *asserted* (the data cannot decide it; the framework holds it on the author's word). This basis is a property of the precondition, not a verdict: it answers "can data speak to this at all?" The framework then reaches one of four *verdicts* on each precondition (Chapter 18), and the certificate displays both the basis and the verdict. This is how the framework is honest about what it has confirmed against data versus what it has accepted on the author's word.

---

### Chapter 18. The Certificate

#### 18.1 What the certificate is

The integrity certificate is the framework's record of the Manifold's current state of integrity. It is the answer to "is this Manifold valid right now, over what scope?"

The certificate records, for each precondition the Manifold has declared:

- What is being assessed (which layer, which specific assertion).
- Its **evidential basis**: *checkable* (the data can confirm or contradict it) or *asserted* (taken on the author's word; not decidable from data).
- Its **verdict** — one of four states, never a pass/fail bit and never a numeric score:
  - **VERIFIED** — the data confirms the precondition: it is checkable, and it checks out.
  - **CORROBORATED** — the precondition is consistent with everything the data can show, but the data cannot positively establish it (an asserted claim the evidence is compatible with, or a checkable claim a null finding has not falsified). The strongest verdict an asserted layer can earn.
  - **CONTRADICTED** — the data exhibits a positive defect against the precondition (a functional dependency that splits, a coverage that drifts, an additivity claim the data violates). Never silent: the dependent result is routed around the defect where a sound route exists (the routing disclosed), and otherwise served carrying the contradiction as a quantified finding at this state. <!-- X1: ADR-020 -->
  - **UNTESTABLE** — the precondition is, in principle, not decidable from the data at hand (the MNAR case, and the defining boundaries themselves). The certificate says so plainly rather than implying a clean bill of health.
- The data version against which the verdict was determined.
- For CONTRADICTED preconditions: the specific violation observed.
- For asserted preconditions: an explicit note that the precondition is taken on the author's assertion.

These verdicts obey a deliberate **safety asymmetry**. A positive finding is *sufficient* to **CONTRADICT** a declaration — one customer mapping to two regions is enough to break the dependency. A null finding is *never* sufficient to **VERIFY** an asserted declaration — the absence of a detected defect is at most **CORROBORATED**, never a guarantee. The framework will fail a thing on evidence, but it will not bless a thing for lack of evidence. This is why MNAR and the genuinely-untestable boundaries are **UNTESTABLE**, not VERIFIED: their absence of contradiction is not confirmation.

The certificate is *queryable*: users, query planners, agents, or operations dashboards can ask "what is the certificate state for this Manifold?" and receive structured answers. It is itself a Manifold artifact, derived from the data and the declarations, refreshed alongside the data.

#### 18.2 What the certificate is not

The certificate is not a guarantee of *truth* — it is a statement of *consistency*. The framework certifies that the data has the properties any correct analysis would require, against the declarations the author has made. It does not certify that the data correctly represents reality, nor that the declarations capture every property reality has.

This distinction matters for the certificate's role in trust: it carries the trust the framework can earn (the data is internally sound; declared restrictions are satisfied; the conditions analysis requires are met) without overstating it (the data is true; the model captures everything; nothing has been missed). The framework is precise about what it knows.

#### 18.3 The certificate under refresh

When data refreshes, the framework re-assesses the checkable preconditions and updates the certificate. Asserted preconditions carry forward unchanged — their basis cannot be re-decided by new data — though a precondition that was CORROBORATED can become CONTRADICTED if refreshed data exhibits a positive defect. A checkable precondition may move to **CONTRADICTED** if new data violates it, or remain **VERIFIED** if it continues to check out.

A previously-VERIFIED precondition that becomes CONTRADICTED on refresh produces a *certificate event*: a recorded transition from VERIFIED to CONTRADICTED, with the data version and the specific violation. The blast radius determines what carries the finding: results depending on the contradicted precondition are routed around it or served with the contradiction disclosed; results not depending on it are unaffected. <!-- X1: ADR-020 -->

A CONTRADICTED precondition can return to **VERIFIED** on a subsequent refresh that restores compliance. The certificate records the history of transitions, so that the temporal pattern of contradictions is itself analytical (an FD that has flickered between VERIFIED and CONTRADICTED across recent refreshes is a different operational concern than one stably VERIFIED or stably CONTRADICTED).

#### 18.4 The certificate under composition

A composed Manifold's certificate is derived from the parents' certificates plus the composition's own verifications. Each parent's verified preconditions remain verified in the composed Manifold, scoped to the columns and operations that depend on them. The composition adds its own preconditions (reconciliation verifications) and these are verified at composition time, against the composed Manifold's data.

This derivation makes composition cheap from an integrity standpoint: the framework does not re-verify what the parents verified. It verifies what the composition adds. A child Manifold inheriting from a verified parent inherits the parent's verifications transitively; only the child's refinements need new verification.

---

### Chapter 19. Outcomes in Practice: Serve, Disclose, Clarify, Inform

<!-- X1: ADR-020 — chapter rewritten from the three-outcome (proceed/refuse/warn) model to the four-outcome inform-and-serve model; annotation contract aligned with the Frame-QL manual's Chapter 7. Behavior-changing rewrite; safety asymmetry preserved verbatim. -->

#### 19.1 The dependency cone

When the query planner builds an execution plan, it computes the **dependency cone** of the query: the set of integrity preconditions the query's correctness depends on. This is mechanical and structural — walking the query's operations against the columns they touch enumerates which Layer 0 anchor preconditions apply, which Layer 1 co-anchoring preconditions, which Layer 2 hierarchy edges, which Layer 3 B-anchor claims, which Layer 4 coverage, boundary, and co-universality checks, and which Layer 5 totality conditions the traversed paths rely on.

The dependency cone is the precise specification of what *this query* needs to be sound. It is a subset of the Manifold's full precondition set, and it is what makes scoped disclosure operational: the planner asks the certificate for the verdict on each precondition in the cone. `VERIFIED` and accepted `CORROBORATED` conditions ride silently into the result's provenance; a `CONTRADICTED` condition triggers a route-around where a sound route exists and otherwise a served finding carrying the contradiction's specifics; a load-bearing `UNTESTABLE` condition is disclosed as exactly that, never implied confirmed. Nothing in the cone gates the bytes; everything in it rides with them.

#### 19.2 The four outcomes

For each query, the planner produces exactly one of four outcomes — the same taxonomy the Frame-QL manual specifies from the language side (its Chapter 7):

**Serve, clean.** Every precondition in the cone is `VERIFIED` or `CORROBORATED` and no soundness finding fires. The result is served; the annotation is the single no-risk `OK` finding.

**Serve, with disclosures.** The query is executable and determinate, and one or more soundness findings apply — a B-anchor crossing, a coverage gap, an MNAR exclusion, a contradicted precondition in the cone. The result is served; the findings ride with it. This outcome has a first-class sub-case, **route-around**: where the planner can *dissolve* a risk rather than flag it — recomputing a mule from its fertile sources instead of re-aggregating a cached image; serving from transaction detail when a `CONTRADICTED` or stale pre-aggregate would otherwise be used — it does so and discloses the routing as an `info` finding (`RECOMPUTED_FROM_DETAIL`, `SERVED_FROM_DETAIL`) rather than disclosing a risk that no longer exists. Only when no sound route exists does the risk surface as a `caution` or `critical` finding on the served number.

**Clarify.** The query does not determine one answer — a mule without its input anchor, a missing order, an ambiguous hierarchy path, a name with no defensible default, or **an aggregate-across an unresolved many-to-many edge**. The framework returns no result and opens a structured clarification naming exactly what is underdetermined and what would determine it. How the clarification is conducted is the surface's decision.

The many-to-many case is worth stating precisely, because it is the boundary between this outcome and the one above, and the determinacy principle that draws it governs every outcome. Aggregating a measure *across* a non-functional edge — `revenue` at product grain summed to `category` over an M:N membership — is **fan-out**: the replicate-and-sum has no single target (a value at one product does not map to one category), so the request **denotes no single number at all**. It is therefore not a determinate-but-risky computation to be served with a disclosure, but an *underdetermined* one to be clarified: its legitimate readings — membership ("revenue touching each category"), primary designation, allocation [Pro] — are different questions with different numbers (Chapter 22.5), and the framework names them rather than silently computing one. The principle: **a request that denotes exactly one number is served** (with a disclosure if that number is risky — a B-anchor crossing is the canonical served-and-flagged case); **a request that denotes no single number among legitimate readings is clarified**, never guessed. This supersedes the prior edition's classification of the bare aggregate-across as a served membership aggregation; membership is now served only when it is the *chosen* reading. <!-- ADR-031 D10: M:N aggregate-across reclassified from serve-with-disclosure (membership default) to Clarify, on the determinacy principle. Supersedes ADR-020/025 default-to-membership. The B-anchor crossing remains serve-and-disclose. -->

**Inform.** The query is well-formed but no result can or may be produced for a non-analytical reason: the data is not there (an empty realized support, disjoint filtered restrictions); a column is quarantined (the author's standing coverage governance); a declared `WITHHOLD` fires (the author's hard stop on a column or family entry, reported as the author's rule with its rationale and the permitted alternatives); or the caller is not entitled under the Manifold's access rules. The framework returns no result and states whose rule, why, and the remedy.

There is no fifth outcome, and in particular there is no analytical-risk withholding: any result that is determinate and producible for an entitled caller is produced, with its risk on its face. The engine's only inherent non-serves are the two it structurally cannot do — execute an ambiguous instruction, or serve from nothing; everything else it serves and discloses, executing governance rules it did not author and producing disclosures it does not act on.

A note on **acknowledgment and override**: when an author instructs the framework to proceed past a gate that would otherwise withhold, or a caller acknowledges a finding flagged `requires_acknowledgment`, the act is recorded in the result's annotation, the precondition retains the verdict it earned, and the result is demoted to at most `CORROBORATED`. An acknowledged or overridden finding is never silently promoted to `VERIFIED` — the safety asymmetry is preserved verbatim.

#### 19.3 The annotation contract

Every query returns the pair `(result, annotation)` — the result null in exactly the clarify and inform outcomes, the annotation present on every path. The contract is specified in full in the Frame-QL manual (its Chapter 7.1); the framework-level commitments are these:

- An annotation is a list of targeted **findings** plus a frame-level severity rollup. Each finding carries: a machine-readable `code`; a `severity` (`none < info < caution < critical`); the originating four-state `certificate_state`; a targeted `subject` (the specific metric, column, anchor, or cell — never smeared frame-wide); a plain-language `headline` and `detail`; a `quantification` where one is computable (a caveat with a number is honest; "may be inaccurate" is noise); the bias `direction` and bound where determinable; an actionable `remedy`; a `requires_acknowledgment` flag; and a `provenance_ref` linking the finding to the certificate entry it derives from.
- The annotation **always carries the canonical desugared form of the statement as executed** — the resolved Manifold identity `(Manifold, version, refresh, certificate state)` and the resolved `(anchor, universe)` of every series included — together with a reference to the plan's atom decomposition. Every result is auditable against the exact reading the framework gave the query, at every disclosure level; interpretation is never noise.
- Disclosure levels (`MINIMAL` / `STANDARD` / `FULL`) are a serialization-time view, never a control on what is assessed, and they respect a non-negotiable safety floor: the overall severity, every `critical` finding, and every `requires_acknowledgment` flag are present at every level. Verbosity may trim noise; it may never silence risk.

#### 19.4 What the user sees

A served result is accompanied by its provenance — the dependency cone with each precondition's verdict — and its findings. A finding is designed to be acted on: *"the roll-up edge `customer → region` is CONTRADICTED (customer 19847 maps to both 'east' and 'west'); served from transaction detail, routing disclosed"* tells a person, or an agent in a propose-validate-refine loop, exactly what happened and what to do. The defect named is in the *data*, not in the Manifold's strictness; the framework is the messenger — and now also the courier, since the number travels anyway, wearing the message.

A clarification names the underdetermined choice in actionable terms: *"the inner grain of this mean is underdetermined — name the input anchor (`@ {customer}` and `@ {transaction}` give different answers)."* Or, for a non-functional aggregate-across: *"`revenue by category` crosses a many-to-many edge (`product → category`) — it has no single total; did you mean membership (revenue touching each category, totals overlap), a primary category (a true partition), or an allocation split [Pro]?"*

An inform names whose rule and the remedy: *"`eom_inventory · SUM` is withheld by the Manifold author's declared rule (stock measures are not summed over time in this Manifold); available families: `LAST`, `AVG`-from-fertile-sources."*

#### 19.5 The framework's promise, and where trust comes from

The discipline, applied consistently, produces the property the framework owes its users, stated exactly as strong as the system can honestly make it: **a number from Columna is either sound under conditions the framework has verified, or it carries its exact risk on its face — never silently wrong, because the question asked and the procedure that answers it are one object.** The honest fine print is part of the promise: soundness is conditional on the Manifold's declarations where verification cannot reach (the certificate tags checkable versus asserted); "exact risk" means the annotation's quantified findings; and specification-divergence — asking precisely for the wrong thing — is made visible, not abolished. <!-- X1: headline claim H2 + footnote register -->

This is different from what conventional tools provide. Conventional tools return numbers whose correctness depends on the user having authored the procedure correctly *and* the data happening to satisfy the conditions the procedure implicitly requires — neither verified, both error-prone, and the failure of either silent. Columna returns numbers whose correctness depends on the Manifold author having declared correctly (one place to think carefully instead of every query), with verification of whether the data actually satisfies analysis's required conditions — and whatever the verification could not settle arrives on the face of the number it qualifies. The locus of trust moves; the residual risk travels in the open; and the silent number, the defect that defined an industry's relationship with its own information, has no remaining place to live.

---

## Part VII — Authoring

This is the final part of the reference manual. Parts I–VI specified what the framework *is*. This part specifies how to *author* a Manifold well — the practical decision procedures, disciplines, and choices that turn the framework's machinery into a Manifold that is sound, useful, and maintainable.

Authoring is the act of producing the artifacts that together constitute a Manifold. The framework provides the contracts and the verifications; the author makes the declarations and applies the disciplines that produce well-built declarations.

The treatment is organized around the *task* (what authoring produces) and four categories of *work* (the activities authoring comprises). It is intended for someone about to build their first Manifold, and for return reading when a new authoring decision needs guidance.

---

### Chapter 20. The Task: What Authoring Produces

Authoring produces a Manifold. Concretely, the artifacts are:

- **The defining-boundaries declaration** — the temporal range, dimension-value-subset, or other constraints that define what this Manifold is about.
- **The column set** — each column's complete spec: identity (name, value type), value determination (anchor, M-anchor, coverage), and composition (family set with each family's reducer, B-anchor, and missing-policy; the default family).
- **The dimension family declarations** — hierarchies, roll-up edges, including ragged or sibling hierarchies where applicable.
- **The operator subset** — which operators from the framework are available for queries against this Manifold, plus name aliases for domain-specific vocabulary.
- **Derived column declarations** — derived metrics and derived dimensions, defined by expressions over the column set.
- **Custom functions and reducers** (Pro) — operator extensions specific to the Manifold.
- **Integrity assertions** — additional preconditions the Manifold declares for verification.

This is what an authoring effort delivers. The chapters that follow describe how to produce these artifacts well, organized by the four categories of authoring work: scoping (Chapter 21), making decisions and choices (Chapter 22), confirming with verification (Chapter 23), and using tools (Chapter 24).

---

### Chapter 21. Scoping

Scoping is the first category of authoring work and the one most under-appreciated. A well-scoped Manifold is small enough to own confidently, focused enough to serve its intended use, and structured to grow incrementally. Poor scoping produces Manifolds that are large, vague, and hard to maintain — modeled "in case someone needs it," with no team confident that every declaration matters.

#### 21.1 Scope at the level of area and usage, not exhaustive questions

The first scoping act is to identify the *area* the Manifold serves (revenue analytics, customer engagement, supply chain, marketing performance) and the *usage* (the team that will own it, the questions they need to answer, the surfaces they will query through). The act is at a coarser level than enumerating every specific question — trying to predict every analytical need upfront is a setup for over-modeling.

Articulate the scope as a clear scope statement: "This Manifold supports the marketing analytics team's customer-acquisition and engagement analyses, covering activity from 2022 onward." Specific questions emerge within that scope and drive the column-and-dimension choices, but the scoping act itself is one level up.

#### 21.2 Defining boundaries: declare them explicitly and early

Once the area and usage are clear, declare the defining boundaries: the temporal range, the dimension-value-subsets, the other constraints that constitute what this Manifold is *about*. Defining boundaries are not filters added to columns; they are what the Manifold is, shared by every column.

Declare them first. The columns you bind will be bound within these boundaries; the integrity verifications will operate over the bounded data; everything downstream depends on the boundaries being clear and committed at the start.

A useful test: state the boundaries as a complete sentence. "This Manifold describes US consumer customer activity from 2020 onward." If that sentence comes naturally, the boundaries are clear. If it trails off, the boundaries are not yet declared and you are not ready to bind columns.

#### 21.3 Pre-aggregated anchors when raw grain is not needed

A common authoring temptation is to anchor columns at the finest grain available in the source data — typically transaction-level or event-level. Often the analyses do not need raw grain; they need pre-aggregated grain (customer-day, store-week, region-month). Authoring at the right grain — recognizing that the right grain is frequently coarser than the raw data — has real consequences: less binding work, less storage and processing cost, fewer integrity concerns to verify.

The discipline: for each column, ask *what is the finest grain any question I support actually needs*, and anchor there, with the source-to-anchor aggregation handled at binding. Do not bind at raw grain merely because the source happens to be at raw grain. Pre-aggregated anchors are the right answer more often than authors realize.

#### 21.4 Start small, verify, expand incrementally

Manifolds do not need to be complete upfront — they cannot be, in practice, because the verification cycle only runs against bound data. Start with a minimal viable Manifold: the few columns and dimensions the most pressing questions need, declared with reasonable defaults, bound to data, verified.

The first refresh will reveal what needs adjustment. Then expand: add the next set of columns the next questions require, verify again, iterate. Each iteration builds on a verified foundation. This is meaningfully easier than designing exhaustively upfront, and the result is a Manifold whose every component has been tested against real data and a real question.

#### 21.5 Columna is column-based, not table-based

This is the single most important scoping discipline, and the one most resisted by authors coming from SQL or warehouse backgrounds.

The natural instinct is to think in tables: "I'll bring in the customers table, the transactions table, the products table." But Manifolds are about columns, and most of the columns in any source table are *not relevant* to the analytical scope. The act of scoping is the act of *choosing the columns the questions need and leaving the rest behind* — not bringing in whole tables and treating every column in them as a default candidate.

This is not just an efficiency point; it is structural. A Manifold whose columns were chosen deliberately, each because a question needed it, is a Manifold whose every declaration matters and whose integrity certificate is meaningful. A Manifold whose columns were inherited en masse from source tables accumulates declarations no one understands and integrity claims no one verifies. The column-orientation from the conceptual manual has concrete authoring discipline implications: approach scoping as "which columns, from which sources" not "which tables to load."

---

### Chapter 22. Decisions and Choices

The second category of authoring work: making the substantive declarations that constitute each column, each dimension, each family. Some are mechanical (the value type follows from what the value is); others are real choices the framework cannot make for you.

#### 22.1 The universe decision: the first question

<!-- X2: ADR-028 / D6, D7 — the U.10 authoring procedure as the new first question; fill demotion with the three-population migration note. Worked examples in the retail vocabulary per X4. -->

Before any mechanism or family is declared, every column answers one question, and answering it first makes most of the later declarations easy. The procedure, one question per step:

1. **Rooted at its own grain key?** Events projection, derived, done — and not declarable (Chapter 9.3).
2. **Otherwise, ask the one question:** *if an anchor point has no row, did nothing happen, or did something fail to be captured?* Nothing happened → reference (or declare, for reuse) the events projection. Failed capture → declare the dense universe and name its basis: which registry, which spine, what product.
3. **Then declare the M-anchor as before** — it governs null values at existing points, in either case, with the universe supplying its denominator (the jurisdiction rule, Chapter 9.7).
4. **Expect verification in proportion to the basis** (Chapter 9.6), and expect Discover to have proposed the answer with code-level evidence before the question was asked.

A worked pass over the retail demo's three characteristic columns:

- **`revenue` at `{transaction}`** — rooted at its own grain key: events projection, derived, nothing to write. The consequence is the one that matters to a skeptical adopter: the framework's revenue total ties out against `SELECT SUM(amount)` on the source by construction.
- **`eom_inventory` at `{store, day}`** — a store-day with no row: did nothing happen? No — inventory is a stock; the store existed and had a level; the row failed to arrive. Failed capture → `ON store_days` (the product of the store registry and the calendar spine), and the M-anchor now governs the absent readings with the spine product as denominator. This is precisely where the estimation machinery *should* fire, because here the conventional bare sum is the number that should not be trusted.
- **`units_returned` at `{transaction}`** — a transaction row with a null in this column means *no return happened*: the point set is the transactions (derived events projection), and the value at existing points is a genuine known zero. This is the rare, honest `fill(0)`.

**`fill` after the universe: a demotion, and a migration note.** The universe decision demotes `fill` from a workhorse to a specialist, because `fill(0)`'s former population splits three ways:

- **(a) "Missing row means none."** Never a fill rule — a universe statement in disguise. Once the destination universe is declared, the zeros appear *by semantics* under the empty-bucket rule (Chapter 9.4), with no substitution and nothing to apologize for. This is most of the population, and the right migration is deletion.
- **(b) Genuine known-zero values at existing points** (the `units_returned` case). Keeps `fill`, now rare and honest.
- **(c) Presentation grids** — every customer-month rendered whether or not anything happened. Not column semantics at all, but **ascription to a different destination universe**: the reporting query pins it (`AT {customer, month} ON customer_month_grid`), and the column's declarations stay clean.

When migrating a pre-universe Manifold, walk every `fill(0)` and sort it into (a), (b), or (c); most land in (a) and are simply deleted, along with the confusion they encoded.

#### 22.2 Metrics and dimension families together

Declare metrics and the dimension families their anchors rest on as paired decisions. A metric is anchored on dimensions; those dimensions have hierarchies; the hierarchies determine how the metric can be aggregated. Trying to declare metrics without thinking about the dimension structure produces metrics whose anchors are not what later analyses need.

The sequence: for the area being scoped, identify the dimensions the questions require (which entities are being measured? customers, products, transactions, stores?). For each, decide whether it is open or `Enumerated`, which hierarchies it participates in, whether there are sibling hierarchies. Inspect candidate roll-up edges against the data before declaring them — many edges that look functional at first glance turn out to be many-to-many on inspection, which changes how the dimension is modeled.

Then declare the metrics, with their anchors specified against the established dimensions and their family sets characterizing how each metric composes under each reducer.

#### 22.3 Derived versus stored columns

A frequent decision: when a value is computable from others, do you store it as a primary column with its own binding, or declare it as a derived column?

**Make non-family-bearing metrics derived.** A mule reducer like `AVG` is computed at presentation from fertile sources (`SUM` and `COUNT`); there is no average family to materialize. So `mean_revenue_per_customer` should be a derived column, computed at query time as a function of the fertile `SUM(revenue)` and `COUNT(customers)` families that are bound. Materializing such a column as a primary would store something the framework would correctly never re-aggregate (any attempt is routed back to the fertile sources); declaring it derived puts the framework's family machinery to its right use.

**Make derived dimensions derived too.** If a dimension is computable by formula or lookup — `month` from `day`, `region` from `customer` via a known mapping — declare it as a derived dimension. No need to store what can be computed. The framework will resolve the derivation at query time, consulting the underlying primary.

**Materialize as primary when the derivation has its own analytical character.** Some quantities are derived from others mechanically but are themselves analytically primary — an engagement score combining multiple inputs by a domain-specific weighting, a customer-lifetime-value computed by a non-trivial formula. These warrant their own primary status, with their own M-anchor, family set, and certificate, because they are the quantity analysts actually think about.

The lean toward derived: fewer materialized columns means less binding work, clearer lineage, and less storage. Materialize only when there's a specific reason.

#### 22.4 Fix fixable incompleteness before declaring around it

When a column's data is incomplete, the temptation is to declare it as filtered coverage (with the restriction predicate) or as having missing values with a charitable M-anchor. Often the right move is upstream: fix the binding so the column is actually complete, or address the source data defect that is producing the gaps.

A coverage declaration is appropriate when the column genuinely covers less than the Manifold's defining boundaries by design — a sampling, a deliberate restriction, a column that only exists for part of the boundary period. It is not appropriate as a way to make a fixable binding defect into a declared-feature. The framework's integrity machinery surfaces defects so they can be fixed; declaring around them returns the Manifold to the silent-defect regime conventional tools live in.

If the incompleteness is fixable, fix it; the result is a complete column with a verified certificate, not a filtered column whose restriction is really a band-aid.

#### 22.5 Many-to-many resolution

When a relationship is many-to-many, a bare aggregate-across it is a **clarification, not a number** (Chapter 19.2): it denotes no single total, so the author resolves it ahead of time — or the query resolves it in the moment — by choosing one of three resolutions from the conceptual manual. Choose by what the question requires:

**Membership filter** when the question is about belonging rather than partitioning ("revenue of products in the Fitness category"). The result is an overlapping subset; per-category totals do not sum to the grand total, and shouldn't.

**Primary designation** when each fine entity has a meaningful primary among its multiple memberships. Promote the relationship to a 1:many `primary_*` dimension. This is often the cleanest resolution when the multiplicity is real but one belonging is canonically privileged.

**Bridge with allocation [Pro]** when totals must reconcile. Declare the bridge, choose an allocation rule, accept that per-bucket numbers reflect the allocation's apportionment. Allocation is a Pro capability; in Core, absent a primary designation, the aggregate-across stays a clarification rather than silently allocating. <!-- ADR-031 D6/D15: allocation is Pro. -->

A useful authoring practice: when reaching for an allocation bridge, ask whether a primary designation exists or could be created. Primary designations convert the many-to-many into a clean functional relationship with no allocation arbitrariness to defend later.

#### 22.6 Name aliases for local vocabulary

The operator registry's name-aliases mechanism (Part III) exists precisely so that a Manifold can present a vocabulary tuned to its team. Use it deliberately. If your audience says "total" rather than "SUM," alias it. If they say "unique visitors" rather than "APPROX_DISTINCT," alias it. If they say "closing balance" rather than "LAST over time," alias it.

The default operator names are correct; aliases let them speak the team's language without changing their algebra. This is a real ergonomic gain and a low-cost authoring act. The discipline: don't multiply aliases unnecessarily (too many names for one thing produces confusion), but don't hesitate to add aliases that genuinely match how the team speaks.

In rare cases, the same logic applies to metrics with multiple business names (revenue vs. net sales vs. top line). Choose the canonical name and alias as needed.

---

### Chapter 23. Confirm: Defaults Then Verification

The third category of authoring work: making provisional declarations, letting the framework verify them, then refining. Authoring is iterative; trying to perfect every declaration upfront is neither necessary nor productive.

#### 23.1 Start with defaults

For most declarations, reasonable defaults exist. The default reducer for most extensive measures is `SUM`. The default B-anchor for an extensive measure under `SUM` is empty. The default M-anchor is MCAR (the most permissive). The default coverage is complete. The default missing-policy is `default` (let the framework's table apply). The default universe follows the derivation rule: a column rooted at its own grain key lands on its root's events projection with nothing to declare (and declaration forbidden); any other column must reference or declare its universe — there is deliberately no silent default for the events-versus-expected choice, because the data cannot decide intent (Chapter 9.3), though an anchor or dimension family may carry a default universe its columns inherit, the calendar spine being the canonical case. <!-- X2: D2 tiers -->

Start with the defaults and the obvious specifics. Get the Manifold bound and let the first refresh run. The verification will surface what needs adjustment.

#### 23.2 Don't assume anchor equals table grain

A specific point worth highlighting because it is frequently gotten wrong: do not automatically anchor a column at its source table's grain. The source table is at some physical grain (often transaction-level or row-level); the column's analytical anchor is at whatever grain the analyses require. These are often different, and the binding aggregates from source-grain to analytical-grain.

When declaring a column, the explicit question is: *at what grain is this column's analytical anchor?* The answer should follow from the questions the Manifold supports, not from the shape of the source data. Authors who default to "anchor = table grain" produce Manifolds finer than they need to be, with downstream cost and complexity that pre-aggregated anchoring (Chapter 21.3) would avoid.

#### 23.3 M-anchor and B-anchor need attention because the framework cannot catch your mistakes there

Most of the framework's defaults are *catchable*: if you declare an FD that is not functional, the framework verifies and reports; if you declare a coverage that the data doesn't satisfy, the framework catches it. You can start with provisional declarations confident that the verification will find your errors.

M-anchor and B-anchor are different. They are partly asserted (the MNAR flag entirely so; many B-anchor claims partly so), and the framework cannot catch errors in them by verification alone. A column declared MCAR that is actually MAR will not be flagged; the rescaled extensive sum will silently apply the wrong correction and produce biased numbers. A column declared as having empty B-anchor under `SUM` (extensive) that is actually intensive will produce nonsense sums with no finding firing.

The discipline: take provisional M-anchor and B-anchor declarations to get running, then *return to them* before the Manifold is trusted in production. Inspect the data for missingness patterns and confirm or revise the M-anchor — and where a dense universe is declared, use its **density checks** (Chapter 9.6): the fraction of declared points carrying records, broken down along candidate coordinates, is exactly where a declared MCAR earns its falsification — uniform density corroborates, clustered density contradicts — and where a measure-column member of M (Chapter 7.1) is tested by comparing density across that column's observed strata (missingness in `satisfaction` that concentrates in low-`revenue` strata falsifies MCAR and corroborates `M = {revenue}`). Examine the column's behavior under each reducer and confirm or revise the B-anchor. The framework cannot catch every error here; you must look. The cost of wrong declarations is silent bias that the certificate can tag only as asserted, never flag as false. <!-- D7; Huayin execution call (1) -->

#### 23.4 Treat certificate failures as data feedback, not framework strictness

When the first refresh reports failures, the response is not to weaken the declarations to suppress the failures. It is to address what the failures reveal:

- A hierarchy FD fails → the data has a customer-region pair where the mapping is many-to-many. Investigate the data; if the relationship really is many-to-many, restructure the dimension as a bridge with allocation; if it should be functional, fix the data or the binding.

- A coverage check fails → the column's data doesn't cover the Manifold's defining boundaries as declared. Decide: is the boundary too broad (narrow it), is the column actually filtered (declare it), or is the binding missing data (fix it)?

- A co-anchoring check fails → two columns declared co-anchored don't share their points. Investigate why; either fix the binding to align them or rethink whether they should be combined directly.

The certificate failures are reporting *what the data lacks for analysis to be sound* (per the integrity reframing of Part VI). The author's response is to address the data lack, not to declare the requirement away.

#### 23.5 Iterate

Each refresh after a change produces an updated certificate. Iterate until the checkable preconditions are mostly VERIFIED, the asserted ones sit honestly at CORROBORATED (or UNTESTABLE where the data cannot decide), and the few CONTRADICTED preconditions are deliberate (e.g., a coverage gap is real and the affected combinations should carry the finding — or, where quarantined, yield informs; that's working as intended). <!-- X1: ADR-020 --> A Manifold whose certificate is mostly VERIFIED, with explicitly-accepted assertions where verification can't reach, is a Manifold ready for production use.

---

### Chapter 24. Tools: Code, Data, AI

The fourth category of authoring work is using the tools that make the first three categories tractable. Authoring is not a manual exercise in 2026.

**Code.** Columna declarations are code artifacts. Author them in version-controlled source files. Review them through normal code-review processes. Replay them across environments. Treat the Manifold as software, because it is.

**Data.** Verification is the dialog with reality, and reality is the data. Use data-exploration tools as part of authoring — inspect candidate FD edges before declaring them, examine missingness patterns to ground the M-anchor, look at distributions to confirm or revise the B-anchor character of a column. The framework will verify at refresh; pre-verifying at authoring is faster and catches issues before they hit the certificate.

**AI.** The agent is part of authoring, not just querying. The bilingual translation between analytical intent and formal Manifold declarations — propose-validate-refine against the substrate — applies to the authoring task as much as to the querying task. An AI authoring assistant can: inspect source data and propose candidate column declarations, surface candidate integrity concerns from data patterns, draft column-specs and dimension families for review, suggest missing-policy choices given observed missingness patterns. The author reviews, adjusts, and confirms; the AI accelerates the routine declarations so attention can focus on the substantive choices.

This is the modern authoring loop: code-versioned declarations, data-grounded verification, AI-assisted proposal and refinement. The framework supports it natively; the discipline is using it well.

---

### Chapter 25. What a Good Manifold Looks Like

To close: markers of well-applied authoring practice. These are not framework requirements; they are diagnostic of successful application of the four categories.

**Each column has a question behind it.** Every column traces back to an analytical need the Manifold supports. Columns "in case someone needs them" have been resisted.

**The defining boundaries fit on a sentence.** What the Manifold is about can be stated cleanly. The scope is clear.

**Hierarchies have been inspected, not assumed.** Each declared roll-up edge has been checked against the data before declaration. The framework will verify at refresh; pre-verification at authoring catches the easy cases early.

**Many-to-many relationships are explicit.** Where a relationship is many-to-many, it is declared as a bridge with allocation, or converted to a primary designation, or used only via membership filter. It is not silently treated as a hierarchy.

**M-anchors are characterized honestly.** Where the data has missingness, its mechanism is declared. The temptation to default everything to MCAR for convenience is resisted.

**The certificate is mostly VERIFIED.** A Manifold whose certificate is full of CONTRADICTED preconditions — or whose load-bearing claims sit at CORROBORATED or UNTESTABLE where verification could have reached — has not had attention paid to the data soundness the framework reports on.

**The Manifold is small enough to be owned.** A few dozen columns, a few dimensions, a clear scope. When a Manifold outgrows its team, compose rather than expand.

**Authoring is in code.** The declarations are version-controlled, reviewed, replayable. Production-quality authoring infrastructure.

These markers describe a Manifold that the framework's machinery serves well: a certificate that is trustworthy, queries that are reliable, evolution that is manageable, composition with other Manifolds that is straightforward. The framework rewards good authoring; this part is about what good authoring looks like in practice.

---

## Part VIII — The Definition Language

This is Part VIII of the reference manual, and it is the semantic home the Frame-QL BNF's §3 points to: the definition constructs — `MANIFOLD`, `BOUNDARIES`, `UNIVERSE`, `COLUMN`, `DIMENSION`, `HIERARCHY`, `ALIAS`, `ASSERT`, `WITHHOLD` — specified *as a language*. The BNF is authoritative on definition syntax; this part is authoritative on what each construct means, what the framework does with it, and what may not be expressed at all. It discharges the chapter owed by ADR-025's reconciliation (the dangling "Core Manual Chapter 3" pointer of the second-edition grammar). <!-- ADR-025 Consequences (3): the owed definition-semantics chapter -->

---

### Chapter 26. The Definition Constructs, Specified as a Language

#### 26.1 The document, and the round trip

A textual Manifold-definition document is the **source of truth for a Manifold**. Every authoring surface — structured forms, the agent (which proposes diffs to the document, never silently authoring the stored declarations), a raw text editor — is an editor over this one document, and it round-trips losslessly to the Manifold's stored serialization. Committing the document produces a Manifold version (Chapter 15); the version *is* the document plus the verification state the first refresh mints. The definition language and the query language are separate grammars sharing lexical conventions: one defines a Manifold, the other queries one, and no construct belongs to both.

#### 26.2 `MANIFOLD`, `BOUNDARIES`, and `INHERITS … VERSION`

`MANIFOLD <name>` opens the declaration and names the artifact. `BOUNDARIES <list>` declares the defining boundaries — what this data space is *about* — as a conjunction of constraints (relational, `IN`, `BETWEEN`), frozen at commit. The boundaries are constitutive, not filtering: they are interpreted exactly as Chapter 10 specifies (every column operates within them by definition; `{}` is the boundaries as one anchor point), and they are *not* row-level query restriction — `WHERE` does that, in the other grammar. M-anchor mechanisms, coverage declarations, and missing-behavior are all interpreted relative to this scope.

`INHERITS <parent> VERSION <n>` declares composition by inheritance, against a *pinned* parent version — never "whatever the parent currently is." The child document then contains only refinements, interpreted under the narrow-don't-contradict contract of Chapter 13: narrowed boundaries, added columns and families, added assertions, extended aliases; never a widened boundary, a removed parent column, a loosened B-anchor, or a redefined inherited universe.

#### 26.3 `UNIVERSE … BASIS …`

`UNIVERSE <name> BASIS <basis>` declares a named point set with its account of point provenance, per Chapter 9.2: `registry(<entity_list>)`, `spine(<dimension>, …)`, `product(<universe>, …)`, or `events(<root>[, project = <anchor>])`. The declared universes are Manifold-level, shared objects, referenced by name — which is what makes co-universality verifiable by reference.

The semantics include a prohibition, and it is load-bearing: **a column rooted at its own grain key lands on that root's events projection by derivation, and declaring it is rejected at definition time** (Chapter 9.3) — declaring the derivable is noise, and noise in a source-of-truth document is a defect. The `events(...)` basis form exists for *reuse*: naming a projection (`purchase_days`) so that several columns can reference the same object and be co-universal by reference rather than by coincidence.

#### 26.4 `COLUMN` and the column-spec fields

`COLUMN <name>` opens a column-spec — the complete declaration Chapter 8.1 enumerates — with these fields:

- **`TYPE <type>`** — the logical value type (Part I). Logical, not physical: width, precision, and encoding are binding concerns, and the type grammar exposes only what affects meaning (`Decimal(p, s)`, `Timestamp TZ = …`, `Enumerated(values)`, the sketch types with their accuracy parameters).
- **`V_ANCHOR <anchor>`** — the value anchor: the coordinate set over which the column is defined as a function (Chapter 3). A grain-key dimension is the identity on itself: its V-anchor is its own name, independent of any other members of a composite grain.
- **`ON <universe>`** — the universe binding (Chapter 9.2): which declared point set the column's values land on. Omitted for grain-rooted columns (derived; declaration forbidden) and where an anchor- or family-level default universe applies.
- **`M_ANCHOR <spec>`** — the missingness mechanism: `MCAR`, `MAR {members}`, `MNAR`, or `MAR {members} AND MNAR`, with the member domain of Chapter 7.1 — dimension families, column names (MAR given that observed column), and self-by-name as the MNAR designation. The mechanism drives the registry's default `{mechanism → behavior}` map; it is the primary declaration, of which any `MISSING_POLICY` is the override.
- **`FAMILY_SET { <entries> }`** — the reducers under which the column founds families. Fertile reducers and the sketch reducers found ordinary families; ordered reducers (`last`, `first`) may appear — the family caches the un-ordered slice and applies the ordered reduction at serve time against the declared order (order is never part of a cache key); mule reducers may not appear, because mules found no families and are derived at presentation from fertile sources. Each `<family_entry>` carries its own **`B_ANCHOR {dims}`** (the blocked families for that (column, reducer) — Chapter 6), an optional **`MISSING_POLICY`** (the per-(column, reducer) override, drawn from the five behaviors plus `default` — Chapter 7.5), and an optional **`WITHHOLD`** (§26.9).
- **`DEFAULT_FAMILY <reducer>`** — the family a bare column reference resolves to; must name a reducer present in the `FAMILY_SET`.
- **`FILL <literal>`** — the column's default fill constant: what the `fill` behavior substitutes when no per-policy literal is given. A property of the column, distinct from any reducer's policy — and, after the universe decision, a rare one (Chapter 22.1).
- **`COVERAGE <spec>`** — the column's coverage state against the boundaries: `complete`, `filtered(<restriction>)` with a predicate, sampling design, or parameter bounds, or `quarantined` (Chapter 10.4). Sampling is a kind of filter, never a fourth state.
- **`SOURCE <binding>`** — the physical binding, below the line: the one field queries can never address, and the only field whose contents are not analytical semantics.

#### 26.5 `DIMENSION` and `VALUES`

`DIMENSION <name> TYPE <type> [VALUES {…}]` declares a column expected to serve in the dimension role. `VALUES` declares an `Enumerated` domain, which buys validity checking, completeness checking, and principled empty-bucket handling (Chapter 4.2). Promoted absence values (`UNKNOWN`, `ANONYMOUS` — Chapter 5) must be *declared in the domain*, so that validity checking permits what the binding-time promotion produces. Dimensionhood remains a role conferred by use (Chapter 4.1); the `DIMENSION` keyword is a declaration of intent and a home for the domain, not a type distinction.

#### 26.6 `HIERARCHY`

`HIERARCHY <name> <child> -> <parent> [-> <grandparent> …]` declares a roll-up chain in a dimension family. Each edge asserts a total functional dependency over the Manifold's boundaries, verified at every refresh (Chapter 4.3); chains commute automatically, and redundantly declared diamonds are checked for commuting (Chapter 4.4). An edge is *both* an assertion and a navigable structure: it enters the certificate like any precondition, *and* it licenses climbs, scan parameters (`reset`/`within`/`step` resolve along it), and derived-dimension resolution. Promoted values must cascade along every hierarchy the dimension participates in (Chapter 5.3); the cascade is declared with the hierarchy. Time-varying dependencies are declared in their period-qualified or split form per Chapter 4.7, not forced into an edge the data will contradict.

#### 26.7 `ALIAS`

`ALIAS <name> = <reducer>` declares a domain-vocabulary name for an operator (`ALIAS total = sum`; `ALIAS unique_visitors = approx_distinct`). Aliases are resolved at parse time and change nothing about behavior; they share the column/dimension namespace, so collisions are rejected at definition time. Children may extend a parent's aliases (Chapter 13.1).

#### 26.8 `ASSERT`

`ASSERT` declares an additional integrity precondition for verification, in two forms. The FD form — `ASSERT <child> -> <parent> IS FUNCTIONAL` — asserts a functional dependency *without* declaring a hierarchy edge, and the difference is exactly the difference between checking and navigating: an **assertion** is a certificate entry (verified at refresh, carrying a verdict, available to the dependency cone), while a **hierarchy edge** is an assertion *plus* a navigable structure that licenses climbs. Use `ASSERT … IS FUNCTIONAL` for dependencies whose validity analyses rely on but which no query should climb (an internal key relationship, a staging invariant); use `HIERARCHY` where navigation is wanted. The predicate form — `ASSERT <predicate>` — declares a domain invariant over the bounded data (non-negativity of a measure, a balance identity), verified at refresh like any checkable precondition, with failures entering the certificate at `CONTRADICTED` and riding the cone into the findings of dependent results.

#### 26.9 `WITHHOLD`, and the governance party

`WITHHOLD` is the author's hard stop — the per-Manifold primitive of the author-governance party in the four-party control model (Frame-QL manual, Chapter 7.5). On a `<family_entry>` it forbids serving that (column, reducer); on a `<column_def>` it forbids the column under any reducer. When a query touches a withheld entry, the engine returns no result for it and **informs**, reporting the rule as the author's declaration, its rationale where given, and the permitted alternative families (Chapter 19.2).

The semantics to hold onto: withholding is *never* the engine's analytical judgment — analytical risk is disclosed and served — and `WITHHOLD` exists precisely so that *human* governance retains a hard stop where policy requires one, visibly, attributably, in the source-of-truth document. It is not a missing-data behavior (Chapter 7.5 retired `refuse` from that vocabulary), and it is not access control: per-user entitlement belongs to the same governance party but is declared in the Manifold's access layer, for which the keyword **`ACCESS`** is reserved. <!-- ADR-025 -->

#### 26.10 What the definition language deliberately cannot say

The language's limits are design, and stating them forestalls misuse. It cannot define operators — algebraic signatures, fertility, propagation rules, and the `{mechanism → behavior}` map live in the installation-level operator registry, which the document *references* by reducer name and may alias but never redefine. It cannot express queries — no expression over data appears anywhere in a definition document except derived-column definitions, which are declarations of structure, not requests for results. It cannot address physical schemas except through `SOURCE` binding strings, which carry no analytical meaning. And it cannot declare the derivable: events projections of grain roots, `{}`, and the consequence-rule destination are all supplied by the framework, and redundant declarations are rejected rather than tolerated — in a source-of-truth document, the difference between "said because it must be said" and "said although it is implied" is information, and the language protects it.

---

## Appendix A — Operator × Backend Capability Matrix

<!-- review §5.4 / ADR-025: discharges the pending "union of backend capabilities, not a framework mandate" item by promoting the honesty into the manual. -->

The operator catalog of Chapter 2 is the framework's logical catalog — the union of what the supported stacks can serve — not a mandate that every backend computes every operator natively. What is constant across backends is the *semantics*: an operator means the same thing everywhere, and where a backend lacks a native implementation, the framework computes it above the boundary (in the metric engine or the planner) from what the backend can extract. What varies is *where the work runs*, which affects performance, never meaning. One thing never runs in the backend at all: the *relating* of columns across anchors. The connector is asked only to deliver single-source columns — extract, filter, single-source pre-reduce — and never to combine them; relating is **transport** in the engine (Chapter 4.3), never a generated join. No row of the matrix below is a join, because a join is not in the framework's vocabulary. <!-- ADR-031 D1: connector delivers columns, never combines them. --> The planner consults this matrix at binding time, so an operator unavailable on a stack surfaces when the Manifold is authored — at declaration, with the affected family named — not as a surprise at query time.

Legend: **native** — pushed down to the backend; **framework** — computed above the boundary by the framework (the engine's sketch library for sketch reducers, the planner for presentation-time mules and scans the backend cannot run); **per-connector** — Pro connectors vary, with the connector's own matrix consulted at binding.

| Operator (class) | Polars (Core) | DuckDB (Core) | Pro connectors |
|---|---|---|---|
| `SUM`, `COUNT`, `MIN`, `MAX` | native | native | native |
| `PRODUCT`, `BOOL_OR`, `BOOL_AND` | native | native | per-connector; framework otherwise |
| `APPROX_DISTINCT` (HLL) | framework sketch library | native (HLL), framework merge | per-connector native where the engine exposes mergeable sketches; framework otherwise |
| `APPROX_QUANTILE` (t-digest) | framework sketch library | native approximation, framework merge | per-connector; framework otherwise |
| `APPROX_FREQUENCY` (count-min) | framework sketch library | framework sketch library | framework |
| `AVG`, `WEIGHTED_MEAN`, `VARIANCE`, `STDDEV` | presentation-time from fertile sources (framework), fertile parts pushed native | same | same |
| `COUNT_DISTINCT`, `MEDIAN`, `MODE` (exact mules) | native at computed grain | native at computed grain | per-connector; never re-aggregated anywhere |
| `LAST`, `FIRST` (ordered) | native | native | per-connector; framework applies the ordered reduction at serve where pushdown is unavailable |
| `VALUE_AT_MAX/MIN`, `NTH` | framework | native or framework | framework |
| Scans (`cumsum`, `rolling_*`, `lag`/`lead`, `rank`, `ewm_mean`) | native | native (window functions) | per-connector; framework otherwise |
| Maps (arithmetic, comparison, conditional, string, temporal) | native | native | native |
| Allocation bridges (`equal_split`, `weighted`, `proportional_to`, `custom`) | — | — | Pro, framework-side |
| Pro estimators (model-based, multiple imputation, IPW, selection models) | — | — | Pro, framework-side |

Two rows deserve a note. The **sketch reducers** are engine-native where the backend exposes a mergeable sketch with compatible parameters, and the framework's own sketch library otherwise; either way the *merge* — the operation that makes the family fertile — is governed by the framework's sketch types (Chapter 1.5), so a family's members are mergeable regardless of which side produced them. And the **exact mules** are native everywhere *at the grain they are computed* — the matrix changes nothing about their sterility; no backend capability makes an exact median re-aggregable.

---

## Appendix B — Terminology Concordance

<!-- X3 / review §2.9: the one-page old→new mapping across the project's renames, for readers of earlier editions and the decisions ledger. -->

The project has renamed deliberately and more than once; the ledger records each decision. For a reader holding an earlier edition, a design note, or the ledger itself, the mapping:

| Earlier term | Current term | Where decided / specified |
|---|---|---|
| NAA (non-applicability anchor) | **B-anchor** (blocked anchor) | ADR-024; Chapter 6 |
| MDA (missing-determinant anchor) | **M-anchor** (missingness anchor) | ADR-024; Chapter 7 |
| `ANCHOR` (definition keyword) | **`V_ANCHOR`** | ADR-025; BNF §3 |
| `MDA` / `NAA` (definition keywords) | **`M_ANCHOR`** / **`B_ANCHOR`** | ADR-025; BNF §3 |
| fillup (with extensive-allocate form) | **broadcast**, replicate-only; the allocation form is dropped — allocation lives only on the many-to-many bridge (`WITH allocation`) | ADR-010/015/025; Chapter 2.4 |
| `impute(rule)` | **`fill`** for constants; estimation is `skip-and-rescale` / `stratified`; sophisticated estimators are Pro-registered named behaviors | v4 model; Chapter 7.5 |
| `refuse` (missing-policy value) | retired; withholding is governance — **`WITHHOLD`** on a family entry or column | ADR-020/025; Chapters 7.5, 26.9 |
| `sampled` (coverage state) | **`filtered(sampling_spec)`** — sampling is a kind of restriction, not a fourth state | ADR-025; Chapter 10.4 |
| truncated (coverage state) | **`filtered`** with a temporal restriction | Chapter 10.4 |
| AC, Collection, Analytics Collection | **Manifold** | Chapter 26.1 (the public noun throughout) |
| `ac.yaml` | **the Manifold definition document** | Chapter 26.1 |
| Coframe-QL | **Frame-QL** | this edition (Columna rename); the language of frames |
| Coframe (the framework) | **Columna** | this edition; the framework name |
| coframe, the coframe (the data-space object) | **Manifold** | this edition; Chapter 26.1 |
| `COFRAME` (definition-language keyword) | **`MANIFOLD`** | this edition; Chapter 26.2 |
| "Core Manual Chapter 3" (BNF pointer) | **this manual, Part VIII** | ADR-025; Chapter 26 |
| semantic kind (flow / stock / rate) | retired as a declared component; derivable for display from the B-anchor pattern of the family set | Chapter 8.1 (framework manual Chapter 3) |
| well-formed / well-formedness (of data) | **sound / soundness** — "well-formed" survives only for query-language grammar conformance | Part VI framing |
| refusal taxonomy (planner / QL Ch. 7) | the **four outcomes** — serve clean / serve with disclosures (incl. route-around) / clarify / inform | ADR-020/025; Chapter 19 |
| fail-closed (as identity) | **inform-and-serve** — disclosure as identity; the safety asymmetry preserved verbatim; refusal survives only for clarify / no-data / governance / authorization | ADR-020; Chapter 19 |
| proceed / refuse / warn-and-proceed | serve / serve-with-disclosures / clarify / inform | ADR-020; Chapters 11.5, 19.2 |
| N_total ("anchor points including absent") | **the covered universe** — the cardinality of the column's universe within its coverage | ADR-028; Chapters 7.4, 9.7 |
| sparse / dense (column property) | teaching vocabulary for **universe bases**: sparse = events projection; dense = registry / spine / product | ADR-028; Chapter 9 |
| lineage flag (on results) | **finding in the annotation** — code, severity, certificate state, quantification, remedy | ADR-020; Chapter 19.3 |
| declared / verified (two-state) | **checkable / asserted** evidential basis × **four verdicts** (VERIFIED / CORROBORATED / CONTRADICTED / UNTESTABLE) | ADR-001/006; Chapter 18 |
| "absorbing / compiling joins into the family structure" | **transport** — relating is carried out *in the engine* along a functional edge (the edge is itself a column-atom the connector delivers); the backend delivers columns and never combines them | ADR-031 D1/D9; Chapter 4.3 |
| (no prior term) replicate-and-sum across a non-functional edge | **fan-out** — an inexpressible transport with no valid target; it denotes no single number | ADR-031 D10; Chapters 19.2, 22.5 |
| membership aggregation over an unresolved many-to-many (served with disclosure, ADR-020/025) | **Clarify** — the bare aggregate-across is underdetermined; membership is served only when *chosen*, and allocation is **[Pro]** | ADR-031 D10; Chapters 19.2, 22.5 |

Edition watermarks: each document of the set carries its reconciliation state on its title page ("reconciled through ADR-N"); this edition is reconciled through ADR-031.

---

*End of the Columna Reference Manual, Fifth Edition.*
