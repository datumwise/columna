# The Measure Algebra of the Theory of Data — Design Record v0.3

### *Typed Values, State Laws, Formation, Participation, and Governed Operations*

**Version:** 0.3 · **Date:** 31 August 2026
**Supersedes:** *Column Algebra / Frame-QL Expansion — Design Record v0.2*
**Status:** design record. **No implementation is authorized by this document.**
**Name:** adopted, and **no longer provisional on Unit D / D1 grounds** — that formulation was
retracted 2026-08-31. The name rests directly on ToD v6.1 §1.2; any further change to it is a naming
ruling, not an output of the crosswalk.

---

## 1. Standing, scope, and name

### 1.0 The foundation

> **The Measure Algebra of the Theory of Data is designed directly against canonical ToD v6.1. It is
> not derived from current Columna runtime vocabulary. Columna's migration from its mixed v5/v6
> implementation is a separate Unit D problem.**

```text
Theory of Data v6.1
        |
        v
Measure Algebra            designed directly in canonical v6 terms

  ...separately...

Current Columna Core       mixed v5/v6 vocabulary
        |
        v
Unit D / D1 crosswalk
        |
        v
eventual implementation mapping
```

**The two programs meet at the implementation boundary and nowhere earlier.** If a future Columna
implementation of reusable state has to touch today's `family` / `member` / `root_evaluator`
structures, *that implementation* may need D1 first. **That is an implementation sequencing
constraint, not a dependency of the algebra.** This corrects v0.3's first draft, which made the
record's own theoretical status "pending D1" — an entanglement the standing ruling that Unit D is
*"not connected to Column Algebra or the current Frame-QL research"* forbids in both directions.

### 1.1 Scope

> **The Measure Algebra is the algebra of governed measures `F@A` under their measure-family laws:
> their typed datum values, sufficient state, lawful formation, participation, transformation, and
> derivability.**

Read that sentence carefully, because a shorter one was available and is wrong. This is **not** "an
algebra over measure families."

Family law is **canonical** — it is where law is declared, and a measure inherits its value type, its
state law, its blocked lineages and its order requirement from the family it belongs to. But the
family is not the thing anyone forms, requests, combines or is served. **`F@A` is.** A measure family
`F` is not yet an analytical object with a value; it becomes one when it is resolved at an anchor
`A`. Every question this record is about — *what type is this datum, what state suffices to compute
it, may these two things be combined, which coordinates participate, does this transformation
preserve the law* — is a question about `F@A`, and several of them (participation, formation,
alignment) are **not even askable** at the level of `F` alone, because they concern two objects
meeting at coordinates.

And the values are **governed datums**, not numbers. A served value carries its type, its population,
its support, its provenance and its disclosures; an algebra that treats it as a scalar has already
discarded the facts the governance exists to carry. The three most expensive defects on the ledger
this month (P1-10, P1-11, P1-12) are all the same shape: a correct arithmetic result over a datum
whose governed facts were dropped somewhere upstream of the arithmetic.

`F@A` is ToD v6.1 §1.2's notation, and the succession note there is normative:

> *"The term **member** is retired from the core v6 ontology. What Version 5 called a member of a
> measure is now simply a **measure**: one uniquely governed measure family at one anchor. What
> Version 5 called a measure is now called a **measure family**."*
>
> `measure = measure family @ anchor`

So `F` is a measure family — *Revenue* — and `F@A` is that family at one anchor. **How Columna's v5
`member` and family-reducer machinery map into that is exactly Unit D / D1's question, and this
record does not answer it.** Columna retains `measure`, `member`, `family`, `MeasureColumn`,
`FamilyMember` as v5 vocabulary; ToD v6.1 §1.2 expressly permits that retention during migration, and
whether it is permanent is OF-28 — open.

### 1.2 Five statements of standing

These are stated in the body, not the footnotes, because each of them is a limit on what this
document may later be cited as having established.

1. **This record does not presently claim a theory separate from the Theory of Data.** It is a layer
   *within* ToD, written in ToD's terms, subordinate to ToD's results. Nothing here should be read as
   a competing formalism, and nothing here acquires independent standing by being written down.

2. **It makes explicit a measure-algebra layer substantially already latent in ToD.** The dominant
   finding of Mission 1 was that the layer is *less new than v0.2 assumed at the formation and law
   levels and more new than it assumed at the value-type level*. Most of what follows is exhibition
   of structure ToD already carries, not invention. Where something is genuinely new it is marked
   **NEW LAW**; where it is exhibition it is marked **LATENT**.

3. **Its design is NOT gated on Unit D / D1.** *(Corrected 2026-08-31; the earlier "final status
   remains subject to D1" is retracted.)* The algebra is written in canonical v6 terms, which ToD
   v6.1 already publishes — so there is nothing about it for a v5→v6 crosswalk of *Columna's*
   vocabulary to settle. Unit D's deliverable is *"a crosswalk, not a change"* for **current Core**,
   and it is held *"not connected to Column Algebra or the current Frame-QL research"* by ruling.
   Honouring that separation means not treating D1 as a gate on this record any more than treating
   this record as an input to D1: **the isolation runs both ways.**

   What *is* gated is narrower and strictly downstream: **implementation into today's hybrid Core**,
   wherever it must touch `family` / `member` / `root_evaluator`. That is a sequencing constraint on
   a future build, recorded in §10 as such.

4. **"Data Algebra" is intentionally rejected as too broad.** The name would claim jurisdiction over
   the whole substrate — sources, carriers, transport, the physical image — when the governed
   analytical object is narrower and better defined than that. A name that overclaims scope is the
   same species of error as a planner that overclaims capability (P1-14), and it fails in the same
   way: quietly, by being believed.

5. **"Column Algebra" is retired, not aliased.** Not renamed-with-a-bridge, not kept as a synonym:
   **retired.** A column is a *material carrier* — a named slot in a delivered frame, a serialization
   concern, a thing with a dtype on a wire. It is not the governed analytical object, and building an
   algebra on it puts the law on the wrong noun. The evidence that this is a real error and not a
   stylistic preference is P1-11: the defect was a substrate *column join* silently choosing an
   analytical *participation* policy. When the carrier is the object, carrier defaults become law by
   accident. Retaining "Column Algebra" as an alias would preserve exactly the reading that produced
   the defect. **The term is not to be used as a live term going forward.** Existing artifacts that
   carry it — v0.1, v0.2, and the Mission 1 reconciliation — keep their titles as historical
   record and are cited by version; renaming them would erase the fact that the framing changed,
   which is the opposite of what retiring it is for.

---

## 2. The spine: two profiles, and the wall between them

Everything in this record is organized by one distinction, and it is the distinction v0.2 lacked.

| | **Analytical law profile** | **Realization capability profile** |
|---|---|---|
| answers | *what is true of this object* | *what this build can currently do with it* |
| holds across | every conforming implementation, every release | one build, one release, one deployment |
| changes when | a ruling changes | code changes |
| a violation is | **an error in the theory** | **a gap in the product** |
| the honest response to a limit | narrow the law, or record it as open | **refuse before the ask, and say which** |

**They are two OBJECTS, not two fields of one profile** *(sharpened 2026-08-31).* A single record
with a law half and a build half still invites reading one off the other, which is exactly what
`witness` invites today. **Declared state law** is an object; **realization capability** is a
different object; they are related by *evidence about a build*, not by *containment in a schema*.

The principal boundary of this record follows:

> ### **Analytical impossibility and implementation absence are different facts.**

`median` has **no finite sufficient state** — analytical impossibility. `mean` has one, `(Σx, N)`,
and this build implements no decomposition — implementation absence. Both currently answer
`witness=holistic`. One is a fact about mathematics and one is a fact about a release, and a system
that stores them in the same field will eventually reason from the wrong one.

**Two corollaries, both ruled, both load-bearing:**

> **Lawful does not mean implemented. Implemented does not determine law.**

The first half is P1-15: a composite input grain spanning two hierarchy branches is **analytically
admissible and correctly planned**, and the current engine cannot assemble it. Nothing about the law
is wrong. The second half is `mean`: this build implements no decomposition for it, and that fact has
no bearing whatever on whether `(Σx, N)` is a sufficient state — it is.

**Why this is the spine and not a caveat.** Mission 1 found **five independent admission ladders in
shipped Core that disagree about one operator**, `mean`:

| ladder | verdict on `mean` |
|---|---|
| `witness` dispatch | HOLISTIC — recompute from base |
| `in_core` | `False` — refuses at execution as a declared member |
| `SERIES_REDUCERS` | present — `avg(x @ {a})` **works** |
| `K0_REDUCERS` | excluded — *"accepts, then refuses at execution"* |
| crossing law G5 | not a monoid — refuses at every face |

They disagree because each is a *different question* — two of them law, three of them build — wearing
the same shape. No total order can reconcile them, because **capability is anti-correlated with
admission**: `sum`/`min`/`max` have the *poorest* state (the value is the state) and the *widest*
crossing admission; `distinct`/HLL have the *richest* state and the *narrowest*. Under v0.2's tier
scheme `distinct` is simultaneously Tier 3 and Tier 0.

**So: profiles, not tiers.** Tiers survive only as a *derived reading* ("commutative combine +
identity finalizer ⇒ reusable"), never as a declaration.

### 2.1 The realization capability profile has three rungs, not one

**Recognition, planning and execution are distinct capability claims**, and conflating them is how a
system lies without anyone intending it to.

| rung | claim | failure mode when overclaimed |
|---|---|---|
| **recognized** | the surface parses this form; it is in the registry | a form that parses and has no semantics reads as shipped (P0-18) |
| **plannable** | the adjudicator returns a disposition for it | — |
| **executable** | the engine can produce the value | **a plan-time `serve` that dies in the engine** (P1-14, P1-15) |

This is not a taxonomy for its own sake. Mission B found the docs gate was **grammar-only by design**
and therefore reported *"37 total, 0 FAIL"* while seventeen of those examples died at planning or
execution. A guard that proves a query is well-formed proves nothing about whether it runs, and the
gap between those two is exactly where a manual goes quietly wrong. The gate is now **staged** to the
rung each example claims — which is the general remedy, not a docs trick:

> **A claim is not validated until the stage at which its claimed behaviour is observable.**

And the governing rule that falls out of it, ruled 2026-08-31 as P1-14:

> **A planner must not return a positive Serve/Disclose disposition for a form the current build
> cannot execute.**

### 2.2 What must NOT be promoted to law

Explicitly, and with reasons, because the pressure to promote runs one way:

| present encoding | why it is **not** foundational law |
|---|---|
| `witness` | **realization-capability evidence.** `median` is holistic because no finite sufficient state closes it — *law*. `mean` is holistic because this build implements no decomposition — *build*. One field, two kinds of fact. A taxonomy read off `witness` would have falsified v0.2's own flagship reusable state `(N, Σx, Σxxᵀ)`, whose first customer is `mean`. **Do not promote `witness`;** split it into `sufficient_state` (law) and `decomposition_built` (build). |
| `in_core` | a release fact, sitting in the same dataclass as the law fields. That adjacency is the *mechanism* of the confusion, not an accident of it. |
| `anchor_consumption` | **NOT established law — a design candidate, and not canonized here.** See §2.3. |
| current crossing support | the *set* of operators admitted across a face is a build fact until something rules otherwise. |
| `is_monoid` | closer to law than the others, but it is currently doing double duty as an execution dispatch key; its law content must be re-derived, not inherited. |

> **Rule of construction for this record:** a present build limitation does not become foundational
> law by being the only thing currently written down. Where the profile is unclear, the item is
> marked open — not resolved in whichever direction the code happens to point.

### 2.3 Movement conditions — the requirement, stated without canonizing a mechanism

`anchor_consumption` is **not established law.** It is a **design candidate extracted from today's
hard-coded G5 behaviour**, it has **zero occurrences in Core**, and Mission 1's recommendation to
declare it as a law dimension is **not adopted**. Naming a mechanism this early is the same error as
promoting `witness`: it would freeze one shape of an answer before the question is settled.

What the record states instead is the *requirement*:

> **The analytical law profile must declare whatever movement / transport conditions materially
> constrain continuation. Current Core hard-codes part of this for face crossings.**

And the specific reason not to canonize the candidate: **movement capability may depend on the KIND
of movement, not on a single `preserved | spent` scalar.** Crossing a face, climbing a certified
hierarchy edge, marginalizing an axis away and broadcasting down are different movements, and a
distinct-class measure does not stand in one relation to all of them. A binary field would have to
pick one relation and call it the operator's, which is precisely the flattening that produced five
disagreeing ladders.

So: the requirement is law; the mechanism is open; and the current hard-coding is neither — it is a
build fact that happens to be the only written record of a law nobody has stated yet.

---

## 3. Typed datum values

**Status: NEW runtime machinery; LATENT in ToD.** This is the level at which v0.2 *under*-estimated
the work.

A governed datum has a **value type**, and the type is the unit of the algebra's typing discipline —
not the physical dtype of the carrier column.

**Where the ground truth stands today.** Eleven scalar dtypes; `ANY = DTYPES`; nested/composite types
excluded by construction; **no type registry**, and `is_dtype` has zero callers. One parametric type
exists in spirit (the HLL sketch) and **the parametric type and the operator marker never meet**:
`out_rule="HLLSketch"` is unparameterized, no value is ever tagged `HLLSketch(12)`, and the precision
lives on the measure declaration instead.

**Three distinctions the algebra requires and the runtime half-has:**

1. **value ≠ state ≠ carrier.** The value is what the measure denotes. The state is what suffices to
   compute it compositionally. The carrier is how either is materialized and moved. Today these
   coincide for 18 of 26 operators (the value *is* the state), which is exactly why the distinction
   has been able to stay implicit — and why the first composite type will break it.
2. **Internal axes are type parameters.** `Matrix<Float64, 5, 5>` and `HLLSketch(p)` carry structure
   *inside* the value that is not an anchor level. Nothing composite exists yet, so nothing conflicts
   — cheap to hold now, expensive to retrofit.
3. **The wire is the binding constraint, and it is behind.** The wire carries **no dtype**, and two
   already-declared types (`Decimal`, the temporals) have no serialization path. **Type observability
   precedes composite types**, or `Matrix<Float64,5,5>` becomes the first type to discover the wire
   cannot carry it.

---

## 4. State law

**Status: LATENT — the classes exist; the declaration does not.**

**Sufficient state** is the analytical-law question: *what must be retained, per part, so that the
whole can be computed by combination rather than recomputation?* It is a property of the operation
and its algebra. It is **not** a property of what this build implements.

The law dimensions, stated as law and nothing else. Note that **`state_class` and
`sufficient_state` are two questions, not one** — the class says what regrouping and ordering the
state licenses; the state says what must actually be retained:

```
state_class         ToD v6.1 §4.7's four classes (below)
sufficient_state    the retained quantity itself:
                      none | the value | <witness tuple> | <carrier T>
combine_law         the operation, plus its algebraic facts:
                      associative?  commutative?  identity element?
order_requirement   none | a total order over <axis>
finalizer           identity | <projection>
approximation       exact | bounded(ε) | unbounded
participation       the admissible policy set            (§6)
```

**ToD v6.1 §4.7 already names the class taxonomy**, and this record adopts it unchanged rather than
minting a second one. **It is not Columna's `witness` vocabulary** — `value` / `ordered` / `sketch` /
`holistic` are the runtime's dispatch kinds, they are a *different four*, and the resemblance is the
trap §2.2 is about:

| class | what it licenses |
|---|---|
| **commutative monoid** | regrouping *and* ordering of the same governed contributions preserve state |
| **associative, noncommutative** | regrouping is safe; logical order must be preserved |
| **ordered / stateful composition** | continuation requires an explicit sequence, order key, context, or composition contract |
| **no declared compositional state** | staged reduction is unavailable from summarized state; retained roots or richer state are required |

Two riders from §4.7, both of which this record leans on:

> *"The row is determined by the **declared state law**; operator names alone are insufficient."*

That sentence is the theory's own version of §2's wall: a name is not a law, and neither is a
dispatch key.

> *"A sketch can have a commutative merge law while remaining approximate. **Approximation is
> therefore orthogonal to this table.**"*

Which is why `approximation` is listed above as its own law dimension rather than as a state class.

Three of the four classes have instances in the shipped registry; **associative-noncommutative has
none** — a fact about the registry, not about the theory. **No measure declares a `state_class`
today**; it is read off dispatch kinds, which is precisely what §4.7's first rider forbids.

**The `mean`/`median` pair is the canonical worked example** and belongs in the record permanently,
because it is the cheapest available demonstration that the two profiles are independent:

```
mean     witness=holistic  is_monoid=False  in_core=False   ->  refuses at execution
median   witness=holistic  is_monoid=False  in_core=True    ->  serves
```

Same law-field values; opposite outcomes; and the *reason* they are both marked holistic differs in
kind. `median` has no finite sufficient state — **law**. `mean` has one, `(Σx, N)`, and this build
does not implement the decomposition — **build**.

**`witness` is realization-capability evidence, not authoritative state law** — and the grounding is
now the theory's own, not merely an inference from the `mean`/`median` pair: **§4.7 says the class is
determined by the *declared state law*, and that operator names are insufficient.** `witness` is an
operator-keyed dispatch marker. By §4.7's own test it is not a source for this taxonomy. The declared
state law and the realization capability are **separate objects** (§2), and §2's principal boundary —
*analytical impossibility and implementation absence are different facts* — is what the `mean`/`median`
pair demonstrates rather than what it establishes.

An earlier Mission 1 draft proposed promoting `witness` and the proposal was retracted under ruling. It is recorded here as a
retraction rather than omitted, because the argument for promoting it was good — it is the only field
that currently *looks* like a state taxonomy — and the same argument will be available again.

---

## 5. Formation

**Status: LATENT and CONTRADICTED — the law existed and one of two paths did not obey it.**

### 5.1 The governing rule

> **Expression formation must preserve domain, eligibility and support facts *before* substrate
> combination.**

Stated as a repair discipline by ruling, 2026-08-31: *"Do not cure population substitution merely by
disclosing after an inner join has already discarded an analytical point. Preserve the governed
alignment facts/domain first; only then apply the map's declared/currently established
eligibility-support semantics."*

**This is not a disclosure rule. It is an ordering rule**, and the order is not negotiable: once the
substrate has combined, the facts the law needed are gone and no amount of downstream honesty
recovers them. A caveat attached after the join describes a frame that no longer contains the
evidence for it.

### 5.2 What P1-11 established

`Planner._apply` joined its operands `how="inner"` — **one word that was an undeclared complete-case
participation policy chosen by the substrate.** The §2c FRAME LAW had said the opposite, for
juxtaposition, **1,280 lines up in the same file**: `how="full"`, *"each column keeping its own
population semantics."* Two alignment laws in one planner, and the one nobody wrote down won.

The served consequence was not a wrong number. The arithmetic over the surviving coordinates was
correct. **The column positively asserted `population: ops` while serving the intersection** — a
false semantic claim on a wire whose whole contract is that such claims are true.

Repaired in Mission A by declaring the alignment domain rather than inheriting it: `how="full"`, each
operand's Φ travelling into the map, so that the one distinction current law can draw survives —
`undefined` ⇒ ineligible (immaterial, `serve`), `unknown` ⇒ eligible-but-unsupported (MATERIAL,
`disclose`).

**And what Mission A refused to invent, reported instead:** *nothing declares how Φ composes through
an operator.* Two operands declaring `zero` do not thereby declare that `a / b` is nil where `b` is
absent — that is division by an absent denominator, not a nil quantity. A declared Φ-composition law
is future work; **not-filling is the only direction that cannot fabricate a value.**

### 5.3 What P1-12 establishes, and it is a limit on the algebra

> **Shared coordinates do not establish shared observational support.**

Two *different* measures may both have a row at a coordinate while resting on different underlying
support — `revenue` over 4 observations, `lines` over 5 rows, both at `s1`. Neither alignment repair
sees it: the coordinate exists for both operands, so there is nothing to preserve, and they are not
members of one family, so no shared VALUE makes their supports equal by construction.

**The blocker is representational, not a defect to code around**: the runtime cannot distinguish a
*declared* divergence from an *accidental* one. Support is a scalar cardinality, not a set; the
observation count is consumed inside the SQL aggregate and never returned.

**The consequence for the algebra:** support must be a **first-class fact carried with the datum**,
not a number computed about a frame. Until it is, formation law can be stated correctly and cannot be
enforced at this level, and the record must say so rather than imply a completeness it does not have.

### 5.4 Joint formation and the multi-input surface

**Multi-input reducer syntax is documented roadmap, not shipped semantics.** The Manual stated the
canonical multi-input shape and claimed *"the framework parses this form directly, type-checks it,
and plans it."* That is true of the **single-input** shape and false of the multi-input one: shipped
reducers are **arity-1**, so a reduction over several inputs is refused on arity — with a generic
`unknown` — before any grain question is reached. The multi-input `input_anchor_ambiguous` clarify
the Manual documented for it is therefore **unreachable**.

**v0.2 built on documentation and read it as machinery.** That is P0-18 — **which is still open**;
Mission B repaired four reachable forms and replaced the grammar-only docs gate with a staged
semantic one, and the Manual now carries the retraction in its own sync note, but the row is not
closed.

**Rulings carried forward unchanged:**

- **The future canonical surface is `op(a @ A, b @ A, ...)`.** It is the Manual's own documented
  shape; implementing it **repairs** the language rather than enlarging it. **It requires the
  participation / joint-support law first** (ruled 2026-08-31) — which makes §6 and O1 hard
  prerequisites, not adjacent work.
- **No joint-tuple surface.** `(a, b) @ A` is not adopted. `@ {…}` keeps its one meaning — composite
  analytical **grain** — because one constructor carrying two meanings at the point the algebra most
  needs clarity is precisely the failure mode this record exists to avoid. `ast.Tuple` accordingly
  keeps meaning grain and only grain.
- **Internal joint formation may still be a semantic/planner object beneath that surface.** The
  prohibition is on the *surface*, not on the machinery. A planner may well need a joint-formation
  object to resolve `op(a @ A, b @ A)` — co-anchoring, alignment domain, participation — and nothing
  here forecloses that. What is forbidden is exposing it as a way to *write* an ask.

---

## 6. Participation

**Status: NEW LAW.** Zero occurrences of `participation` / `complete_case` / `listwise` / `pairwise`
in shipped code; one hard-coded policy in the engine.

Participation is the law of **which coordinates take part** when two or more measures meet. It is
identity-bearing: complete-case and pairwise are not two implementations of one operation, they are
**two different analytical objects**, and a system that picks one silently has answered a question
nobody asked. P1-11 is the demonstration — `how="inner"` *is* a complete-case policy, and it was
chosen by a substrate default.

Three requirements, all consequences of law already ratified:

1. **Participation is declared, not defaulted.** LAW → EXECUTION DIRECTIVE → SUBSTRATE. A substrate
   join strategy is a *directive*, never a law.
2. **Ambiguous participation is its own registered Clarify reason.** OF-1's *one reason per contested
   dimension* means this is a **new registered reason**, not a widening of an existing one. The
   alternatives-as-menu carrier already exists and is the right shape for "here are the N lawful
   participation policies."
3. **Participation interacts with support, and support is not yet representable** (§5.3). A
   participation law stated over coordinates alone is under-specified for the P1-12 case. **This is
   the sharpest open dependency in the record.**

---

## 7. Governed operations and admission

### 7.1 One admissibility law

**Status: established 2026-08-31 (P1-13), and it generalizes well beyond the case that produced it.**

> **Explicit and inferred alternatives must share one admissibility law.**

Stated for the case: explicit pin validation and candidate-pin enumeration must use the same
canonical admissibility law. Two functions in one planner held two definitions of "a lawful pin" and
had drifted — enumeration still required a candidate to *reach* the output anchor, a rule execution
had already left behind — so an unpinned reduction **refused "no lawful reading" at an anchor where
six explicit pins served.** The disposition rule was right; the set it was applied to was computed
against a superseded law.

**Both directions of the same error appeared together**, which is what makes this a general principle
rather than a bug report. Enumeration *under*-offered by applying a stale law, and simultaneously
*over*-offered by not applying a current one (§2c), so a Clarify menu listed a reading that refuses
`out_of_universe` the moment it is named.

**The general form:** wherever a system both *validates* something a user writes and *proposes*
alternatives of the same kind, the validator and the proposer are two implementations of one law, and
they will drift. **The remedy is structural — one predicate, both callers — not agreement testing.**
A behavioural spot-check passes under two implementations that happen to agree today, which is
exactly the state P1-13 was found in.

**Three corollaries for this algebra:**

- An offered alternative is a **claim of lawfulness**. Offering an unlawful reading makes Clarify
  reachable *before* lawfulness, which is how a reader is talked into a laundered answer one
  keystroke later.
- A refusal that **every** candidate earns is not *about* any candidate; it is a property of the ask,
  and collapsing it into a generic "no lawful reading" trades a true diagnosis for a vaguer one.
- A refusal must **report** the verdicts it reached rather than **assert** a cause. Asserting one is
  how a message stays plausible and becomes false when the law around it grows.

### 7.2 The admission profile

Per §2: **profiles, not tiers.** The law dimensions are §4's. The build dimensions are §2.1's three
rungs plus `decomposition_built`. The wall between them is the point of the structure, and
`anchor_consumption` sits **on** the wall with its side undecided (§2.2).

### 7.3 Lawful admission may exceed realization capability

**Status: demonstrated (P1-15).**

A composite input grain whose levels are reached by separate hierarchies is analytically admissible,
correctly planned, and **not assemblable by the current engine**. This is the cleanest available
proof that the two profiles are independent objects and not two descriptions of one thing.

It also poses the record's sharpest live tension, and the honest thing is to leave it posed. The
corrected enumeration of §7.1 now *offers* such readings in a Clarify menu — so a reader can be
handed a lawful reading the build cannot execute, which is the P1-14 rule one level removed. **Three
responses exist and only two are honest:** fix the realization gap; or rule on a capability gate that
declares the limit at the ask. **Filtering the menu silently by what the engine can currently
assemble is the third, and it would make a build limitation into an analytical narrowing — precisely
the promotion §2.2 forbids.**

### 7.4 Ergonomics is not analytical law

**Status: open, and deliberately unanswered (P1-17).**

With admissibility corrected, an unpinned reduction can clarify over six lawful candidates. Every one
of them serves when named: **the menu is correct.** Whether a six-item menu is the intended *shape*
of a Clarify is a presentation question, and it must not be answered by narrowing the law.

Ranking, a "reasonable pin" heuristic, or pruning by current engine capability would each mean the
framework quietly choosing among lawful readings — the precise thing a Clarify exists to refuse to
do. **A narrowing that is itself a law** — a declared default input anchor, say — is a different
proposal and would be a legitimate one. The distinction is the record's, not a preference: *changing
which readings are lawful* is analytical law; *changing how lawful readings are presented* is not.

---

## 8. Derivability and transformation

**Status: LATENT, with one closed question and one open one.**

**Closed: family generation does not create permission.** A reduction that travels a lineage its
operator is declared `BLOCKED` along has no lawful reading and is refused **in every spelling** —
written as a declared member, generated by an inline reducer above a lawful sibling, or carried
inside a unary, binary, scalar, scan or `DERIVED` wrapper. *Family generation creates a new analytical
family. It does not create a new operator permission.* Carriers transport an operation; they do not
grant it authority, and analytically equivalent spellings must earn byte-identical verdicts.

**Closed: disclosure composition is sound where it has been tested.** Provenance and approximation
caveats propagate correctly through derivation. **Support and absence do not** — they are frame-side
facts rather than operand-level ones, which is the same root as §5.

**Open: construction-dependent analytical types and result standing.** Some values are what they are
*because of how they were constructed* — an allocated figure, a face-routed total, a sketch-merged
distinct count. Today `License` attaches to members, hierarchies, bases and faces and **never to a
result**; no wire column carries a license, verdict or scope field. So a result cannot presently
state its own standing, and the algebra cannot type a value by its construction. **This is an open
problem, not a design.**

---

## 9. The three-time structure

**Status: already shipped, and it is the record's firmest ground.**

> **Declaration states law → adjudication establishes realization-bound certification and current
> admission → ask time applies admitted law.**

| time | act | what it may do | what it may **not** do |
|---|---|---|---|
| **declaration** | an author declares | state law; make structure *eligible* for certification | make anything executable |
| **adjudication** | publish-time | prove claims against attested data; establish certification and **current** admission | invent law |
| **ask** | plan/run | apply admitted law; resolve; refuse | prove, or manufacture admission |

Two properties worth stating explicitly because they are easy to lose:

- **Adjudication is realization-bound.** Certification is a claim about *this data as attested*, and
  it therefore belongs to neither profile purely — it is the joint where law meets a realization and
  becomes *current admission*. That is why closed-by-default is correct: a declaration makes an edge
  *eligible* for certification, not executable.
- **Φ is declared; absence is computed per ask.** Which cells are absent is only knowable after
  alignment, so it is an ask-time fact derived from a declaration-time law — and §5.1's ordering rule
  is what keeps that derivation possible.

---

## 10. Reusable shared state, and where Unit D actually bites

**Corrected 2026-08-31.** The first draft of this section held reusable-state identity and keying as
**[D1-GATED]** outright. That was too strong, and it is retracted.

> **The algebraic design proceeds now. Only implementation into the current hybrid Core may be
> gated, and only where D1 is actually required.**

- **Reusable shared-state identity and keying — DESIGN OPEN, not gated.** What makes two requests
  *the same state*, how that state is named, and how it is invalidated are questions in canonical v6
  terms, and ToD v6.1 supplies those terms. They can be designed against `F@A` and `Law(F)` without
  reference to `family` / `member` / `root_evaluator` — indeed **they must be**, because designing
  them against the hybrid vocabulary is how the algebra would inherit a migration artifact as a law.
  Held out of Mission 1 for exactly that reason; that was a reconnaissance discipline, not a
  permanent gate.
- **IMPLEMENTATION of the above into today's Core — genuinely sequenced behind D1**, wherever it must
  touch `family` / `member` / `root_evaluator`. One thing is already ruled out for the crosswalk:
  `root_evaluator` *"must not remain the thing that tells a measure which reducer family it belongs
  to."* A reusable-state implementation that keyed off it would be building on a structure already
  ruled out. **That is the whole of the dependency, and it is a build dependency.**
- **The implementation vocabulary decision** (OF-28). Retention of v5 terms is currently ratified as
  unchanged; whether it is permanent is undecided, and it gates one thing absolutely: **no public
  governed-publication authoring surface opens while it is unresolved.** An authoring surface mints
  governed objects under whichever vocabulary it exposes, and that is not reversible by documentation
  afterwards.
- **The v5→v6 crosswalk itself (D1)** — every current Core concept (`measure`, `member`, `family`,
  `MeasureColumn`, `FamilyMember`, `root_member`, `root_evaluator`, `FAMILY {…}`, `K0_REDUCERS`)
  mapped to its v6 counterpart or explicitly marked as having none. One thing is already ruled out:
  `root_evaluator` *"must not remain the thing that tells a measure which reducer family it belongs
  to."* Everything downstream of that mapping is a guess without it.
**A separation, not a dependency.** Unit D is *"not connected to Column Algebra or the current
Frame-QL research"* by ruling, and its acceptance test is *"a document Huayin can rule on, not a
passing test."* This record therefore neither contributes to D1 nor draws on unfinished parts of it;
where it needs a v6 term it uses the published ToD v6.1 text and nothing else. **The isolation runs
both ways** — which is why nothing here is marked as waiting on it.

**No implementation of any of the above is authorized, and no part of this record should be read as
having prepared the ground for one.**

---

## 11. Open problems

Carried as problems, not as designs. Each names what would close it.

| # | problem | closes when |
|---|---|---|
| **O1** | **Support is not representable.** Shared coordinates ≠ shared support; the runtime cannot tell a declared divergence from an accidental one (P1-12). | support becomes a carried fact — a companion carrier per delivery, or a declared support contract per operator |
| **O2** | **Φ-composition through an operator is undeclared.** Two operands declaring `zero` do not declare that `a / b` is nil where `b` is absent. | a declared Φ-composition law |
| **O3** | **Result standing.** No result can state the license, verdict or scope under which it was constructed. | licenses attach to results; the wire carries standing |
| **O4** | **`anchor_consumption`'s profile.** Law or capability — currently hardcoded either way, and declared nowhere. | a ruling places it on one side of the wall. **Not D1's** — D1 is the vocabulary crosswalk and is held separate |
| **O5** | **Lawful-but-unrealizable at the ask.** A correct Clarify may offer a reading this build cannot execute (P1-15 × P1-13). | the realization gap closes, or a capability gate is ruled — **not** by silent pruning |
| **O6** | **Query-level `count(*)`.** Now rowed as **OF-30** — it had lived only in the Manual. | a language ruling among the three readings — **not** by inheriting SQL's |
| **O7** | **Clarify ergonomics** (P1-17). | a *law* that narrows, or an explicit ruling that the menu is correct as-is |

### 11.1 Query-level `count(*)` — unresolved, and it must not be resolved by inheritance

`count(*)` **as a series in `SELECT`** does not ship, and the reason is not a parser gap.

**A `UNIVERSE` declares coordinates, not a fact table.** Only a `MEASURE` carries `FROM <table>`.
So a bare `count(*)` in a query **does not name what is being counted**, and at least three readings
are open: the physical source-row count; the count of existing analytical points; and the count of
observations of some measure. These are different numbers with different meanings.

> **`count(*)` must not inherit SQL's implicit relation semantics.** SQL can answer it because a SQL
> query always has a relation in hand. Frame-QL does not, and adopting the SQL reading would import
> an implicit analytical object the Manifold never declared — a fact table by the back door.

`AS count(*)` **in a `.cml` MEASURE is a different and established case** and is unaffected: there the
source table is declared on the measure, so what is counted is not in question. Resolving the
query-level form is a language ruling.

**Rowed as OF-30 (2026-08-31).** Until now the question existed only in the Manual, with no ledger or
fork entry — and a real architectural fork that lives only in prose is one nobody is obliged to
reread.

### 11.2 The Statistical Bridge boundary

**Status: already shipped, with one leak.**

The jurisdiction is stated by standing rule and this record adds nothing to it:

> *"Columna is **stage one** of the Statistical Bridge — the governed data objects of an analysis:
> universes, measures, members, and the frame. The Bridge's other three stages — the generation of
> possible evidence, inference from realized evidence to formal targets, and the interpretation of
> formal results as world-facing claims — are **out of scope**, by standing rule; **their absence is
> a boundary, not a gap.**"*

**The Measure Algebra lives entirely inside stage one.** It is an algebra of *deterministic
analytical establishment*: what is true of a governed datum given what was declared and attested.
Nothing in it licenses a claim about an unobserved target. Zero hits for p-value / significance /
confidence / bootstrap in shipped code, which is the correct state.

The HLL relative error is **structural** — `1.04/√2^p`, derived from the sketch's own parameter with
zero data fetches — and stays inside the Data World: it is a property of the construction, not an
inference about a population.

**The one leak, on record:** the MNAR string *"averages are selection-biased"* is a claim about an
**unobserved target**, which is inference, and it attaches to `sum` and `count` as well as to
averages. It is a small string and a real boundary crossing, and it is noted here so that it is not
later cited as precedent for the algebra having jurisdiction it does not have.

---

## 12. Evidence index

Everything asserted above traces to one of these. Grades follow the ledger: **VX** reproduced under
the real runtime · **SV** read at file:line · **INF** inferred.

| source | establishes | grade |
|---|---|---|
| **Mission 1** (`specs/column_algebra_reconciliation_m1_v0_1.md`) | the v0.2 reconciliation; five disagreeing ladders; `witness` conflation; profile-not-tiers | VX/SV |
| **Mission A** (P1-11, shipped v0.18.1) | alignment domain declared, not inherited; formation ordering rule | VX |
| **Mission A′** (P1-10, shipped v0.18.1) | one family over one VALUE shares one support | VX |
| **Mission B** (P0-18, **still open**) | the Manual documented forms the planner refused; four reachable forms repaired; the docs gate now checks at the stage the claim becomes observable | VX |
| **P1-12** | shared coordinates ≠ shared observational support; support not representable | VX |
| **P1-13** | one admissibility law for explicit and inferred alternatives | VX |
| **P1-14 / P1-16** | recognition ≠ planning ≠ execution; capability honesty; path convergence | VX |
| **P1-15** | lawful analytical admission can exceed current-build realization capability | VX |
| **P1-17** | Clarify ergonomics is not analytical law | VX |
| **OF-28 / Unit D** | vocabulary retention undecided; the v5→v6 crosswalk gates this record's status | SV |
| **ToD v6.1 §1.2** | `F@A` — `measure = measure family @ anchor`; `member` retired from the core ontology | SV |
| **ToD v6.1 §4.7** | the four state-law classes; *"the row is determined by the declared state law"*; approximation orthogonal | SV |
| **Manual Preface / §4.2 / §2.1** | stage-one jurisdiction; query-level `count(*)`; the multi-input retraction | SV |
| **P0-18** (**CLOSED** 2026-08-31) | the Manual's four false form-claims — two repaired, two retracted; the gate is now staged | VX |
| **OF-30 / OF-31** | `count(*)`'s three readings as an open fork; the Manual's surviving "Column Algebra" label | SV |

---

## 13. Change map from v0.2

**Title and framing**

| v0.2 | v0.3 |
|---|---|
| *Column Algebra / Frame-QL Expansion, Design Record v0.2* | *The Measure Algebra of the Theory of Data — Design Record v0.3* |
| "Column Algebra" as the working name | **retired, not aliased** — columns are material carriers |
| implicit scope, read as spanning the substrate | **explicit scope sentence**; "Data Algebra" rejected as too broad |
| standing not stated | **five standing statements** in §1.2, including D1-gating |
| — | **NEW SPINE:** analytical law profile vs realization capability profile, applied throughout |

**Items 1–6, 10–13 (Mission 1 reconciled)**

| # | v0.2 position | v0.3 |
|---|---|---|
| 1 | multi-input shape treated as **already machinery** ("the framework parses, type-checks and plans it") | **corrected — documented roadmap, not shipped semantics.** The premise was false; the Manual states it and the system refuses it (P0-18) |
| 1b | `(a,b) @ A` as a candidate joint surface | **rejected as a surface.** Canonical remains `op(a @ A, b @ A, …)`; `@ {…}` keeps one meaning. **Internal joint formation stays available as a planner object** |
| 2 | general datum value types | **retained, and re-ordered:** type *observability* (dtype on the wire, `Decimal`/temporal serialization) now precedes composite types |
| 2b | value ≠ state ≠ carrier | retained; recorded that the parametric type and the operator marker **never meet** today |
| 3 | internal axes as type parameters | retained unchanged — theory only, uncontradicted |
| 4 | joint formation as **work to be designed** | **reframed: the law existed and one of two paths disobeyed it** (P1-11), 1,280 lines apart in one file. Now an **ordering rule**: preserve domain/eligibility/support *before* substrate combination |
| 4b | eligible frame ≠ co-supported points | **elevated from principle to demonstrated limit** (P1-12) — and recorded as **not representable** in the current runtime |
| 5 | participation as first-class law | retained as **NEW LAW**; strengthened with P1-11 as its demonstration and a new dependency on O1 |
| 5b | ambiguous participation → Clarify | retained; **must be a newly registered reason**, not a widening (OF-1) |
| 6 | state-law taxonomy read off `witness` | **rejected as a source.** `witness` is realization-capability evidence. v0.3 **adopts ToD v6.1 §4.7's four classes unchanged** rather than minting a taxonomy, and splits `witness` into `sufficient_state` (law) and `decomposition_built` (build). The `mean`/`median` pair becomes the permanent worked example |
| 10 | construction-dependent types | retained, **downgraded to an open problem** (O3): licenses never attach to results |
| 11 | declaration vs ask time | retained and **expanded to three times**, with adjudication named as realization-bound |
| 12 | **operator admission tiers** | **rejected.** Five ladders disagree about `mean`; capability is anti-correlated with admission. **Profiles, not tiers**; tiers survive only as a derived reading |
| 13 | Statistical Bridge boundary | retained; **the MNAR leak recorded** rather than left implicit |

**Items 7–9** — reusable state, semantic state key, invalidation: **design open, not gated.** Mission 1
held them so reconnaissance could not ratify the hybrid vocabulary; that was a reconnaissance
discipline. v0.3 records that the *algebraic* design proceeds now in canonical v6 terms, and that only
*implementation into today's Core* is sequenced behind D1 (§10). No position is taken on their content
here — the correction is about standing, not substance.

**New in v0.3, with no v0.2 antecedent**

- §2.1 recognition / planning / execution as three distinct capability claims, and the rule that a
  claim is not validated until the stage at which its behaviour is observable.
- §2.2 the explicit do-not-promote list, with `anchor_consumption`'s profile left **open** — this
  declines Mission 1's own recommendation to declare it as law.
- §7.1 **one admissibility law** for explicit and inferred alternatives, generalized from P1-13, with
  the structural (not test-based) remedy.
- §7.3 lawful admission exceeding realization capability, and the ruling that silent pruning is not
  an available response.
- §7.4 ergonomics is not analytical law.
- §11.1 query-level `count(*)` must not inherit SQL's implicit relation semantics.
- §11 the seven-item open-problem register with closure conditions.
- §5.4's dependency edge: the multi-input surface **requires the participation / joint-support law
  first**, which makes §6 and O1 prerequisites rather than parallel tracks.
- §9's three-time structure named as such, with adjudication identified as **realization-bound** —
  the joint where law meets a realization and becomes *current admission*.
- §1.1's explicit statement that how v5 `member` maps into `F@A` is **D1's question, not this
  record's**, and §10's separation clause.

**Corrections applied to v0.3 after the citation pass (2026-08-31), recorded rather than folded in**

| was | is |
|---|---|
| the record's status "pending Unit D / D1"; the name provisional on D1 grounds | **retracted.** §1.0: the algebra is designed directly against canonical ToD v6.1; **the isolation from Unit D runs both ways.** Only *implementation into today's hybrid Core* is sequenced behind D1 |
| items 7–9 **[D1-GATED]** | **design open, not gated** (§10). The algebraic design proceeds now; the gate is on implementation, where D1 is actually required |
| `anchor_consumption` as an open-but-named law dimension | **not canonized** (§2.3). It is a design candidate extracted from hard-coded G5 behaviour. The record states the *requirement* — declare whatever movement/transport conditions materially constrain continuation — and notes that capability may depend on the **kind** of movement, not a `preserved \| spent` scalar |
| law and build as two halves of one profile | **two OBJECTS** (§2), with the record's principal boundary stated: **analytical impossibility and implementation absence are different facts.** `witness`'s rejection is now grounded in ToD §4.7's own rider, not only in the `mean`/`median` pair |

**Corrections of fact carried from Mission 1** — three v0.2 premises were wrong: the multi-input
premise (§3.2), the reading of the Manual as evidence of machinery (C2), and the assumption that
§4.2.1 described a principle to adopt when it described **a defect Columna had** (P1-11).

---

*End of Design Record v0.3. No implementation is authorized by this document.*
