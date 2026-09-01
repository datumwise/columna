# Measure Algebra — Design Finding 2
## Typed Values and Sufficient State — Reconciliation Finding

**Version:** 0.1 · **Date:** 1 September 2026
**Type:** design finding + **proposed amendment** to *The Measure Algebra of the Theory of Data — Design Record v0.3* §3–§4
**Mandate:** reconnaissance only. **No implementation, schema change, registry redesign, Arrow adoption, operator reclassification, ledger row, or Unit D work is authorized by this document.**
**Written in:** canonical ToD v6 terms. No Core vocabulary migration; no Unit D dependency.

Governing question, as given:

> What type structure is already implied by ToD, Measure Algebra / Contract Calculus, Frame-QL, and
> current Columna for **(a) exposed datum values** and **(b) sufficient state**, and what relationship
> should exist between those two typed universes?

---

## 0. Verdict

**The corpus supplies the machinery and withholds the ruling. Columna implements the machinery twice,
in two vocabularies that do not meet, and the severance is deliberate.**

This finding does **not** repeat Finding 1's shape. Finding 1 concluded that a proved theorem was being
contradicted. Here there is no theorem to contradict:

> **The relationship between the two typed universes is genuinely OPEN in the corpus — not deferred,
> not implied, not answered. It is never asked.** What *is* established is an asymmetry of obligation:
> the value side is registered, well-formedness-checked and carried in the contract; the state side has
> **no registry, no well-formedness obligation, no equivalence relation, and no presence in any contract.**

Four findings, in descending order of consequence:

1. **The independence claim is NOT established, and the corpus leans the other way.** The capability
   tuple names $X_\kappa$, $Y_\kappa$, $S_\kappa$ as three separate slots — but two of the corpus's
   own worked state carriers are *built out of value types*: $S_{\mathrm{sum}}=X$ and
   $S_{\mathrm{dc}}=\mathcal P_{\mathrm{fin}}(X)$. The single explicit relational sentence is an
   **ordering**, not an independence: nominal value typing comes *"before aggregate-state construction."*
2. **Columna's two type systems are severed by design, and the design is on record.** `projection.py`
   classifies `witness` / `combine` / `deliver_sql` as *"mechanics … the planner never sees them"* while
   `accepts` / `out_rule` are *"vocabulary."* The value type system is planner-visible; the state
   taxonomy is engine-only. This is not drift.
3. **`witness` is a dispatch discriminant, not a state type — and the tree already says so.** Of four
   witness kinds, exactly one has a type in `types.py`, and that type is never worn by a running value.
   The `(value, order_key)` pair is **inexpressible** in the value vocabulary, because there is no
   product type.
4. **The physical→logical wall is asserted and not built.** `types.py` claims the connector *"lifts
   physical→logical at publish."* **No such function exists.** The logical type is an unchecked author
   assertion, and a wrong one is executed faithfully and silently — demonstrated below on a shipped
   fixture.

**What this means for the "how do we add matrices?" framing.** The framing is too narrow, and the
narrower question is not the blocker. Matrices are downstream of a prior absence: **the state side has
no type discipline at all, in either the corpus or the tree.** A matrix-shaped exposed value is
additionally *new corpus territory* — but a matrix-shaped sufficient state is the shape of machinery
the corpus has already proved four times over.

**Confidence.** High on §§1–5 (quoted or executed). Moderate on §6's Arrow reading, which is
classification rather than citation. §9's alternatives are enumerated, deliberately not scored.

---

## 0.1 A terminological hazard that must be held first

**`S` is overloaded across the corpus, and the corpus never flags it.**

| symbol | in | means |
|---|---|---|
| $S_\kappa$ | CC §3.2, §7.2; ToD §4.5 | the **sufficient-state carrier** |
| $S$ in $C_1=(X,U,A,E,S,\beta,\gamma)$ | CC §14.4 | the **observed support set** |
| $S$ in $S\subseteq E\subseteq P$ | CC G1.D4 | the **observed support set** |

These are unrelated objects. Because Finding 1 is *about* support and this finding is *about* state,
the two documents will be read together and the collision will bite. **This finding writes $S_\kappa$
for state and never bare $S$.**

---

## 1. What the corpus already supplies

### 1.1 The capability tuple — the whole state machinery, in one place

Contract Calculus §7.2 (`w-contract-calculus.r01.md:816-842`). A capability $\kappa\in\mathsf{AggCap}$ contains:

- input **type** $X_\kappa$;
- output **type** $Y_\kappa$;
- state **carrier** $S_\kappa$;
- $\oplus_\kappa:S_\kappa\times S_\kappa\to S_\kappa$ (commutative);
- $0_\kappa\in S_\kappa$;
- $\eta_\kappa:X_\kappa\to S_\kappa$ — *"input embedding"*;
- $\rho_\kappa:S_\kappa\to Y_\kappa$ — *"finalizer."*

Composed (`:584-599`):

$$g_\kappa(M)=\rho_\kappa\!\left(\bigoplus_{x\in M}\eta_\kappa(x)\right)$$

> *"The aggregate function is not itself a monoid. Its sufficient-state combination may form a
> commutative monoid."*

ToD v6.1 §4.5 states the same shape in different letters, $(S,\eta,\oplus,e,\phi)$
(`w-theory-of-data.r06.md:956-968`) — and **never gives a signature for $\eta$ or $\phi$.** ToD applies
them; it does not type them.

**Vocabulary note.** The corpus says *"finalizer"/"finalizes"* and *"embedding"/"embeds"*. It never says
lift, deliver, prepare, project, expose, or display for these arrows. Columna says *deliver / combine /
project*. The mapping is unstated anywhere.

### 1.2 The corpus types non-scalar state, repeatedly and formally

| carrier | shape | citation |
|---|---|---|
| $S_{\mathrm{sum}}=X$, $\eta=\rho=\mathrm{id}$ | the value itself | CC:603-611 |
| $S_{\mathrm{mean}}=\mathbb R\times\mathbb N$, $\rho(s,n)=s/n$ | **product** | CC:613-635; ToD:992-1016 |
| $S_{\mathrm{dc}}=\mathcal P_{\mathrm{fin}}(X)$, $\rho(S)=\lvert S\rvert$ | **powerset of a value type** | CC:2967-2982; ToD:1020-1035 |
| $\widehat S_\kappa=S_\kappa\times\mathbb N\times\mathbb N$ | **triple** | CC:2104-2145 |
| $\widehat S_{\kappa,h}=S_\kappa\times D_h$ | **parameterized product** | CC:1930-1935 |
| $(\theta,S)$ (theta sketch) | pair | CS:922-928 |

**The state universe is closed under product, and the corpus proves it:** *"Lemma G1.L2 … The product of
commutative monoids is a commutative monoid"* (CC:2149-2158).

And the components of a state tuple are typed **by governance role** (CC:2180):

> *"The first component contains sufficient state for observed values only. The second and third
> components carry the analytical domain facts needed to decide eligibility and support."*

This is the only place in the corpus where structure *internal to a carried object* is given a
governance reading. It is inside a **state** tuple. CC never generalizes it.

### 1.3 `(sum, count)` is not folklore — it is written down, ~13 times, in this project's own corpus

CC:132-136 (*"Exact composition requires at least $(\operatorname{sum},\operatorname{count})$"*);
CC:613-635; **CC:1217** (*"why mean composes through `(sum, count)` rather than through displayed means"*);
ToD:992-1016; ToD:1286; ToD:2141; CS:215; CS:348-352; CS:773-777; CS:1183; CS:1196; CS:1300; CS:1371.

And the discipline that makes it matter (CC:1128-1134, Corollary G0.3 at :1215):

> *"A schedule is **state disciplined** when: every nonfinal stage carries $S_\kappa$-state; states
> combine using $\oplus_\kappa$; $\rho_\kappa$ is applied only after the final stage of that reducer."*

### 1.4 The type/carrier distinction the corpus **does** commit to

CC:316-320 — the strongest type-theoretic commitment in the corpus:

> *"Units-of-measure type systems show that physically similar carriers can support different legal
> operations because their dimensions or nominal identities differ (Kennedy, 1996). … **Equality of
> carriers does not identify types**, and a pointwise function must be declared on its nominal input
> types."*

with the worked case (CC:359-372): $\lvert\mathrm{RevenueUSD}\rvert=\lvert\mathrm{CostUSD}\rvert=\mathbb R$
while $\mathrm{RevenueUSD}\neq\mathrm{CostUSD}$.

**This is a nominal-identity distinction, not an encoding distinction.** It says two types may share a
carrier set. It does **not** address bit layout, precision, or serialization. Reading it as ToD's
answer to "semantic type vs physical encoding" is an over-reading — it answers a *different* and
narrower question, and answers it well.

### 1.5 What ToD means by "governed typed value" — thinner than expected

> *"A **datum** is one governed typed value at one anchor point."* — ToD:640, repeated verbatim at :2506
> *"The point and value type are part of the meaning. `42` and `age = 42 at John` are different
> analytical assertions."* — ToD:642-648

ToD gives the value side a symbol **once** — $m_{F,A}:S_{F,A}\to V_F$ (ToD:766) — and $V_F$ **never
appears again anywhere in ToD.** It is not defined, not constrained, not decomposed, and absent from
the Compact Formal Summary and the conformance surface.

**The family conformance declaration has no `value_type` field at all** (ToD:2366-2390). It has
`state_schema`, `combine_law`, `finalizer`, `ordering_semantics`, `admitted_reductions` — and on the
identity side `unit_or_currency`, classified as an *identity contract*, not a type.

> **ToD requires that a datum be typed and never says what a type is. The type discipline is entirely
> the Contract Calculus's.** And `state_schema` is a declared YAML field with **no schema language, no
> type, and no example value anywhere in the paper.**

---

## 2. The asymmetry of obligation — the core structural finding

This is the finding's spine. Both universes exist in the corpus; only one carries obligations.

| | value side | state side |
|---|---|---|
| what it is called | *"input **type** $X_\kappa$; output **type** $Y_\kappa$"* (CC:824-825) | *"state **carrier** $S_\kappa$"* (CC:826) |
| prose | *"accepted input type, output type, sufficient-state **algebra**"* (CC:385) | — |
| registry | *"$X$ is a registered value type"* (CC:1988); registries list *"nominal value types"* (CC:776-782) | **none** — a *field of* a capability, never a registry entry |
| well-formedness | 6 obligations (CC:1986-1996); *"source values inhabit $\lvert X\rvert$"* (CC:1404) | **none** |
| in the contract | $C_0=(X,A,\beta)$; $C_1=(X,U,A,E,S,\beta,\gamma)$ | **absent** — reachable only through $\kappa$ |
| equivalence | $\equiv_C$ (CC:726-752), $\equiv_{C_1}$ (CC:1998-2005) | **undefined** |
| certified atom | $(v,C_1)$ with $v:S\to\lvert X\rvert$ — the type is $X$ **alone** (CC:1966-1975) | — |

**Consequence.** A certified atom's *type* is its value type. The state carrier that produced it is not
part of what was certified, not part of what is compared for equivalence, and not part of what
well-formedness checks. In Finding 1's vocabulary: **the state carrier is a schema-level object the
corpus never made schema-level.**

### 2.1 The three readings, and which the evidence actually supports

- **(a) independently typed — NOT SUPPORTED.** No passage asserts it. The three-slot signature
  establishes that $S_\kappa$ is *separately named* and not *forced* to equal $X_\kappa$ or $Y_\kappa$.
  That is weaker than independence. The one explicit relational sentence is an ordering (CC:320):
  *"It places nominal value typing **before** aggregate-state construction and contract inheritance."*
- **(b) one shared type algebra — SUPPORTED BY CONSTRUCTION, NEVER STATED.** $S_{\mathrm{sum}}=X$
  (CC:606) puts a nominal value type in the state slot. $S_{\mathrm{dc}}=\mathcal P_{\mathrm{fin}}(X)$
  (CC:2970) applies a constructor *to a value type* to make a state carrier. Certifiable State
  attributes a **"datatype"** to state (CS:1013). Three independent constructions consistent with one
  ambient algebra — and **no sentence says so.**
- **(c) OPEN / never addressed — THIS IS WHAT IS ESTABLISHED.** The corpus never writes
  "independently typed," "two type systems," "one type algebra," or any equivalent. It never states or
  denies $S_\kappa\in\mathsf{Type}$. It gives no formation rules, equality, or registry for state
  carriers. Its own boundary notes concede the discipline is unfinished: *"This is nominal equivalence
  for the proved fragment. The full framework will require richer equivalence and refinement
  relations"* (CC:752); *"It does not claim that the complete governed framework has already been
  reduced to a categorical model"* (CC:338).

> **The honest reading: the corpus is implicitly monistic and explicitly uncommitted.** One ambient
> carrier algebra, with the value side additionally carrying a nominal-identity layer the state side
> lacks. That is an interpretation of construction and word choice, not a quotation — and it is flagged
> as such.

**This is good news for the mission.** The architecture is a choice to be *made*, not a fact to be
*discovered*. §9 enumerates the candidates.

---

## 3. What Columna materially has — two type systems, severed

### 3.1 The severance is on record as a design decision

`projection.py:54-70`, the `OperatorSig` the planner is given:

> *"An operator's SIGNATURE — the vocabulary the planner typechecks and ROUTES against: name, KIND,
> accepts, out_rule, and the order/window/core flags it needs to route. **The mechanics
> (witness/combine/deliver_sql/scan_impl) are resolution and stay engine-side; the planner never sees
> them.**"*

So: **`accepts`/`out_rule` are "vocabulary" and planner-visible; `witness`/`combine` are "mechanics" and
engine-only.** The value type system is the planner's; the state taxonomy is the engine's. `is_monoid` is
the single state-ish bit promoted across, and the docstring justifies it separately.

**Law-vs-build note.** Calling the witness *"mechanics"* is a build claim — *this build* resolves
witnesses engine-side — stated as a category fact (*"are resolution and stay engine-side"*). What a
state's representation *is* is exactly what a state type system would call vocabulary.

Reinforced at `planner.py:1479-1487`:

> *"**Deliberately NOT extended into a signature check**: registering `mean` gives the operator a law
> address, not new arithmetic or **new typing**."*

### 3.2 Direction of reference: one way, and only on the value axis

- `operators.py:37` imports `NUMERIC, TEMPORAL, ORDERED, ANY, DURATION, HLLSKETCH, dtype_in` from
  `types.py`. **Every one feeds `accepts` or `out_rule`** — the *exposed value* signature.
- **No witness field is typed by anything in `types.py`.** `witness` is `str`; its four inhabitants are
  string literals at `operators.py:43`; `types.py` never mentions the word "witness."
- `types.py` imports **nothing** (`from __future__ import annotations` only). The value type system is
  unaware a state taxonomy exists.

The name collision is real and acknowledged in-tree: `types.ORDERED` is a **type class**, `ORDERED_W` is
a **witness kind**, and `engine.py:24` imports the latter aliased as `ORDERED` — so inside `engine.py`
the identifier means the witness kind, and inside `operators.py` it means the type class.

### 3.3 Witness by witness — what is typed and what is not

| witness | has a type in `types.py`? | what the running state actually is |
|---|---|---|
| **VALUE** (18 of 26 operators) | incidentally — it *is* the value, so `out_rule` types it | one column `_value` (`engine.py:314`) |
| **SKETCH** | yes in vocabulary (`HLLSketch`, `HLLSketch(p)`) — **never worn by a value** | `dict[key → datasketches.hll_sketch]` + an `int` precision (`engine.py:1009-1028`) |
| **ORDERED_W** | **no — inexpressible; there is no product type** | two conventionally-named columns `_value` + `_order` (`engine.py:316-323`) |
| **HOLISTIC** | n/a — no witness | raw base rows, or the whole finer series |

**v0.3 §3's count is confirmed:** 18 of 26 registry operators carry `witness=VALUE`, i.e. the value *is*
the state. That is the corpus's $S_{\mathrm{sum}}=X$ degenerate case holding for 69% of the registry —
**and it is exactly why the distinction has been able to stay implicit.**

### 3.4 `HLLSketch(p)` — a fully specified type that no value ever wears

`types.py:49-62` defines the parametric constructor and states the law: *"the precision p is part of the
type identity … only same-precision sketches merge."* `sketch.py:4-17` goes further:

> *"Precision is part of the TYPE … **making precision type-identity turns that into a static check.**"*

**There is no static check.** Specifically:

1. `hll_sketch_t` / `is_hll_sketch` / `hll_precision` have **zero callers in `src/`** — only
   `demos/hll_case_study_demo.py`. `is_dtype` has **zero callers anywhere.**
2. `hll_count` emits `out_rule="HLLSketch"` — the **family marker, unparameterized**. The parameter is
   dropped at the moment of construction.
3. The precision lives on the measure as an `int` (`model.py:189`), whose comment asserts *"the sketch
   type is HLLSketch(p)"* — while the field is an int.
4. `HLLSketch(p)` reaches the outside world **only as interpolated prose** in trace and disclosure
   strings (`engine.py:1012, 1017, 1031, 1035, 1099, 1165`).
5. The dynamic guard that *would* enforce it — `hll_merge_pair`, `sketch.py:61-68`, raising `TypeError`
   on precision mismatch — is **never called from `src/`**; the engine calls `hll_merge` directly with
   the single `p` off the measure.
6. The planner's five typecheck sites use bare `dtype not in sig.accepts`, **not** the sketch-aware
   `dtype_in`. So `"HLLSketch(12)" not in frozenset({"HLLSketch"})` would **fail** against an operator
   that lists the family. The parametric branch of `dtype_in` is **unreachable from the query path**.
   `signature_ok` is called only at `parser.py:675` and `compiler/compile.py:161`.

> **The one parametric type in the system loses its parameter at the operator boundary, and the
> parameter is the part that carries the composition law.** The invariant currently holds *by
> construction* — one precision per measure — not by checking. That is Finding 1's discharge pattern
> (*"declaring earlier lowers the required grade"*) appearing on the value side, unremarked.

### 3.5 The ORDERED_W pair — inexpressible, and asymmetrically discarded

The witness is documented as `(value, order_key)` (`operators.py:29`). In execution it is two columns,
`_value` and `_order` (`engine.py:322-323`), combined together (`engine.py:695-700`), rendered for the
trace as the *string* `"(value,order)"` (`engine.py:342`), and **projected away at `engine.py:375`** —
`frame.select(list(target) + ["_value"])`.

Two consequences the taxonomy does not record:

- **The order key has no type available even in principle.** `FamilyMember.order_by` names a *level*;
  `DimensionLevel` (`model.py:69-78`) has **no dtype field**. Dimension coordinates are untyped in this
  system. So `min`/`max`'s `accepts=ORDERED` constraint is never applied to the thing actually being
  min/max'd.
- **SKETCH witnesses persist into the cache; ORDERED_W witnesses do not.** `CacheEntry(frame, sk, ver)`
  for sketches (`engine.py:239`) vs `CacheEntry(frame, None, ver)` for ordered (`engine.py:246`), where
  the cached frame is the *post-projection* one. So the cached artifact for an ORDERED_W reducer is the
  answer, not the witness. **Nothing in the witness taxonomy records this difference**, because the
  taxonomy has no notion of a state's carrier.

---

## 4. Capability expressed as state law — inventory

Each entry separates the **law claim** from the **build claim**.

### 4.1 `mean` — the canonical case, and the tree self-diagnoses it

`operators.py:101-113`:

> *"`mean` is a REDUCER in the governance sense … but it is deliberately NOT a monoid: a displayed
> average does not combine associatively, and mean-of-means is not a mean. **Its witness is HOLISTIC**
> (recompute in one pass over the remapped series)."*

- **Law (sound):** a displayed mean does not combine associatively. The corpus agrees — *"A displayed
  mean is not the sufficient state"* (CC:637).
- **Build, stated as law:** *"Its witness is HOLISTIC."* The registry's own rule for HOLISTIC is
  *"(no finite witness closes it)"* — which is true of `median`/`mode` and **false of `mean`**, whose
  finite witness $\mathbb R\times\mathbb N$ is proved in this project's own Contract Calculus. The
  parenthetical gives it away: *"recompute in one pass"* is an **execution strategy**, not a witness.

**The tree already knows.** `compiler/compile.py:42-47`:

> *"`mean` is excluded on **DEMONSTRATED failure, not on classification**: it parses clean AND checks
> clean, then refuses at execution, because `in_core` is consulted only on the scan path."*

And `engine.py:713` has a **live mean**: `_SERIES_REDUCE["mean"] = lambda c: c.mean()`. So `mean` is
executable over an already-resolved series in the same file that files it HOLISTIC. Four flags disagree
about one operator: `is_monoid=False`, `deliver_sql` populated but never called, present in
`SERIES_REDUCERS`, `in_core=False`.

> **Stated with the required discipline:** this is *not* a claim that richer datum types would make
> `mean` non-HOLISTIC. The sharper claim is that **a richer sufficient-state type representation may
> allow the known $(\Sigma x, N)$ law of mean to be represented honestly while its exposed datum
> remains scalar.** `mean`'s exposed value is `Float64` and would stay `Float64`. What is missing is a
> place to *say* $\mathbb R\times\mathbb N$ — and `witness`, a four-valued dispatch enum, is not that
> place. `median` and `mean` currently share a bucket for reasons that differ **in kind**.

### 4.2 Nested types excluded — with a law claim smuggled into the justification

`types.py:16-17`: *"Nested dtypes (List/Struct/Array/Binary/Object) are out of Core scope **(you don't
aggregate a struct here)**."*

- **Build (honest):** nested dtypes are out of Core scope.
- **Law smuggled in:** the parenthetical asserts nested types have no aggregation role. But the system's
  own **state** layer needs exactly one product type — `(value, order_key)` today, $(\Sigma x,N)$ if
  mean were represented honestly. The exclusion is scoped to *aggregating a struct* (a value-layer
  operation) while the need is *holding a witness* (a state-layer one). **The two are conflated because
  there is only one type namespace.**

### 4.3 The G5 "ANCHOR LAW" gate — a schedule inside a law-titled guard

`engine.py:382-417`, guard `if not (op.is_monoid and op.witness == VALUE)`:

- **Law (sound):** the sketch branch — *"per-member counts cannot be summed, weighted, or routed"* — a
  real spent-anchor fact, and the code takes care to speak the declaration dialect.
- **Build wearing the law's name:** the fall-through — *"(ordered/holistic crossings are
  **post-launch**)"*. "Post-launch" is a schedule. An ORDERED_W measure (`last`) **is** a monoid and is
  refused for roadmap reasons under a gate titled ANCHOR LAW (G5). Second copy at `engine.py:585-588`.

### 4.4 The type channel has one reason code for three different situations

`disclosure.py:315` — `"type_error": (ERROR, None)` — is emitted for all of:

1. a genuinely unlawful ask (`sum` of a `String` — no arithmetic exists);
2. a scope decision (`sum` of a `Date` — `types.py:13-15`: *"Temporal arithmetic is NOT modelled …
   correct on what it accepts/rejects **without committing to an algebra**"*);
3. a needs-a-conversion case (raw sketch at a numeric operator — *"you must hll_estimate it to a number
   first"*), where the remedy is a real, expressible operation the message never names.

**There is no `type_unsupported` sibling to `filter_unsupported`.** The system draws exactly this
distinction elsewhere, sharply and recently (`disclosure.py:232-241`, minted 2026-08-31):

> *"unreachable is a fact about the MANIFOLD and the asker can fix it by choosing another dimension;
> unsupported is a fact about the BUILD and no rewording of the ask helps. **Collapsing them would tell
> a reader to fix something that is not theirs to fix.**"*

That sentence is the P1-14 ruling, and it applies verbatim to the type channel. The compiler already
*has* the vocabulary — `UnsupportedCoreCapability` / `ExecutionRepresentationGap` /
`LogicalMeaningMissing` (`compiler/compile.py:92-110`) — and it stops at the compile boundary.

### 4.5 The counter-example — how it looks when done right

Windowed scans (`operators.py:145-154`): *"contract present, mechanics [ROADMAP]"*, given their own flag
(`in_core`), their own refusal text (`engine.py:266-272`, *"not implemented in this build [ROADMAP]"*),
and no taxonomy distortion. **This is the model the other four depart from.** A limitation with its own
name does not corrupt a classification.

---

## 5. The physical→logical wall — what it actually guarantees

### 5.1 The claim, and the missing half

`types.py:9-11`:

> *"physical types (VARCHAR, DOUBLE, …) live in the connector, **which lifts physical→logical at
> publish** and realizes logical→physical at delivery. The planner never sees a physical type."*

**There is no lift.** No function named or shaped like `to_logical` / `physical_to_logical` exists; the
only mapping table, `_LOGICAL_TO_DUCKDB` (`connector.py:91-95`), is one-way. `physical_type()`
(`connector.py:238-242`) returns the raw DuckDB type string and nothing consumes it as a type. The only
occurrence of the phrase *"lifts physical→logical"* in the entire tree is **the claim itself.**

The logical type is therefore an **unchecked author assertion**, defaulted when omitted
(`parser.py:489-491`, default `"Float64"`), on a declaration surface that is a single
`re.search(r"\bTYPE\s+(\w+)")` — so **no parametric type is writable**: `Decimal(18,2)`,
`HLLSketch(12)`, `Matrix<Float64,5,5>` cannot be spelled.

### 5.2 What the realization actually compares

`realize()` (`connector.py:244-257`) interposes a `TRY_CAST` only when a **bare column's coarse class**
disagrees. Both classes are 5-valued hand-rolled buckets; `_phys_class` (`connector.py:97-107`) is a
**substring sniff on an uppercased string** — `INTERVAL` contains `INT` and is tested by the numeric
branch first. A second, differently-spelled sniffer exists independently at
`columna-server/init/eval.py:281-284`. **Two physical-class taxonomies that can disagree.**

And nothing casts on the way out: every delivery ends `pl.from_arrow(self.con.execute(q).arrow())`
(`connector.py:271` et al.). **The declared "representation promise" (`model.py:178`) is never enforced
on the returned frame.**

### 5.3 The wall's failure, demonstrated on a shipped fixture

`packages/columna-server/src/columna_server/demo/benchmark/manifold.cml:63`:

```
# a CATEGORICAL measure — only count/distinct/mode are well-typed over it (never sum/median)
MEASURE region_label ON transactions FROM transactions AS mode(customer_region)
```

No `TYPE` clause → `logical_type` defaults to `Float64`. The Python-built twin declares it correctly
(`demos/build_benchmark.py:101-103`, `logical_type="String"`). Executed against DuckDB:

```
physical_type(customer_region) = VARCHAR
realize under declared Float64 -> TRY_CAST(customer_region AS DOUBLE)   SELECT -> [(None,)]
realize under declared String  -> customer_region                       SELECT -> [('North',)]
```

**A comment declaring the measure CATEGORICAL sits one line above a declaration that types it
`Float64`, and the wall casts a region name to `DOUBLE` and serves `NULL`.** `check()` does not catch it
because `mode` is `accepts=ANY`.

### 5.4 "The planner never sees a physical type" — true in letter, false in operation

No SQL type-name string reaches `planner.py`. But `planner.py:16` imports Polars; `ColumnResult.frame`
and `FrameResult.data` are `pl.DataFrame`; those frames' dtypes are **DuckDB's choice, transported
through Arrow, inferred by `pl.from_arrow`**, and never reconciled with `logical_type`. The static
typecheck at `planner.py:1789`/`:1926` is therefore a check on a **claim**, not on the data.

Worse, one analytical verdict already turns on a runtime dtype: `adjudication.py:170-174` `_tol_for`
selects exact-vs-tolerance comparison from `recompute_df[name].dtype` — the delivered Polars dtype, not
the declared one. Combined with §5.2 (declare `Float64`, receive `Decimal(38,2)`), **the reduce-vs-
recompute tolerance policy is selected by DuckDB's column type.**

### 5.5 The wire carries no type at all

`disclosure_wire.py:235-255` — a served column carries `name`, `status`, `population`, `disclosures`,
`mechanical`, `value`/`values`. **No `dtype`, no `unit`.** The planner computes `out_dtype` at every node
and discards it at the wire boundary. `Decimal` and the four temporals have no serialization path.

This confirms v0.3 §3's sequencing ruling, and it is the hardest constraint in this finding:

> **Type observability precedes composite types**, or `Matrix<Float64,5,5>` becomes the first type to
> discover the wire cannot carry it.

Type reaches the outside on exactly one surface: `"dtype": mc.logical_type` on `describe_measure`
(`columna-server/tools.py:275`) — a **Polars dtype name string, on a versioned external contract.**
`describe_manifold` omits it; operator `accepts`/`out_rule` are dropped from `describe`
(`describe.py:104-108`), so a consumer cannot predict a `type_error` without hardcoding the registry.

### 5.6 A manual-ahead-of-code gap of significant size, not currently rowed

`docs/columna_reference_manual_5e.md` Ch. 1 specifies a **17-type** logical system — including
`Enumerated`, `Hash`, `List`, `Array`, `Struct`, `TDigestSketch`, `CountMinSketch` — and a parametric
declaration grammar (`Decimal(p,s)`, `Timestamp TZ = …`, `Enumerated(values)`), marking `TYPE` as
**SHIPPED**. Core has 11 scalar types and no parametric syntax. Separately, the Frame-QL manual
documents `cast(col, <type>)` and `is_<type>` predicates (`frame_ql_manual_v2.md:1238-1241`) **with no
`[ROADMAP]` marker**, unlike every other unshipped construct in that appendix — while `§5.3` prescribes
*"a cast"* as the remedy for a type mismatch. **The system tells the user to write a cast; the language
has no cast.** Noted as an observation; no ledger row is created by this document.

---

## 6. Arrow — carrier, not vocabulary

**Instruction honoured: this finding does not assume Arrow types should become ToD logical types.**

### 6.1 What Arrow says about itself

> *"Unlike other type systems such as Apache Parquet's, the Arrow type system **doesn't have separate
> notions of physical types and logical types**."* — [Arrow Columnar Format](https://arrow.apache.org/docs/format/Columnar.html)

That single sentence is the most important external fact in this finding. **Arrow declines the very
distinction ToD's question is about.**

### 6.2 The three buckets

- **(a) Semantic:** `timestamp(tz=…)` vs naive; `date32` vs `timestamp`; `duration` vs `int64`;
  `month_day_nano_interval` vs `duration`; `decimal128(p,s)` vs `float64`; **`Map` vs
  `List<Struct<k,v>>`** (identical layout, `Map` asserts key semantics) ; `null`; `Union`.
- **(b) Encoding-only:** `list`/`large_list`/`list_view`; `string`/`large_string`/`string_view`;
  `date32` vs `date64`; `time32`/`time64`; int/float widths; **dictionary encoding** (spec: *"a data
  representation technique"*); `run_end_encoded`; dense vs sparse union.
- **(c) Extension types:** storage type + `ARROW:extension:name` + `ARROW:extension:metadata`, with a
  **graceful-degradation guarantee** — an unrecognizing consumer falls back to the storage type *while
  preserving the metadata*.

Note the direct divergence in (b): dictionary encoding is *not a type* in Arrow, while `Categorical` and
`Enum` **are** distinct dtypes in Polars and therefore in `types.py`. Columna's current vocabulary has
already inherited one carrier's answer to a semantic question.

### 6.3 The precedent that matters most

Arrow's canonical extension registry includes **`arrow.fixed_shape_tensor`** (storage `FixedSizeList`;
metadata carries `shape`, `dim_names`, `permutation`) and **`arrow.variable_shape_tensor`**, plus
`arrow.json`, `arrow.uuid`, `arrow.bool8`, and `arrow.opaque` — *"a type that an Arrow-based system
received from an external system, but that it cannot interpret."*

> **Arrow could not express named, permutable tensor axes in its type system proper and reached for the
> extension mechanism to do it.** That is a structurally informative precedent for §8's question,
> whatever one concludes from it. Note also that `arrow.opaque` is a named slot for **admitted semantic
> ignorance** — a governance move, in a carrier format.

### 6.4 The proposition, tested as instructed

> *"Replacing Polars dtypes with Arrow dtypes as Columna's LOGICAL vocabulary would merely move the
> carrier dependency rather than remove it."*

**For.** Arrow disclaims being a logical type system (§6.1). The inherited encoding-variant surface is
*larger*, not smaller — ~40 built-ins, many in bucket (b), each needing an `accepts` ruling that
Polars' scalar subset already collapsed. Arrow is **already the wire** (`pl.from_arrow(...arrow())`), so
adopting its names makes logical vocabulary identical to carrier vocabulary at precisely the seam the
wall is meant to separate. And decisively: **none of §5's defects is a vocabulary defect.** The missing
lift, the unenforced delivery, the coarse-class sniff, the `region_label` null, the planner's `dtype_in`
bypass, the tolerance-from-runtime-dtype — every one is a missing *enforcement point*. Renaming fixes
zero of them. The ~19 Polars-embedded rulings already inventoried in
`docs/architecture/f0_reconnaissance.md:146-152` are *behaviours*, not type names.

**Against.** Arrow is a **versioned specification with a governance process**; Polars is a library whose
dtype set moves with releases. More sharply: **extension types are a mechanism Polars structurally
lacks**, and Columna already needs one. `HLLSketch(p)` *is* an extension type — storage (a serialized
sketch), name, parameter — implemented as `f"HLLSketch({p})"` plus `startswith` plus slicing, and that
improvisation is *exactly* where the planner's check breaks (§3.4.6). Ad-hoc parametric encoding in a
printed name demands an ad-hoc membership predicate that not every call site remembers to use. Arrow
supplies a serialization contract and a degradation guarantee for that slot. Finally, the published
`"dtype"` on the describe wire is currently a **Polars name an external consumer must know Polars to
read.**

**Verdict: both readings are defensible, and which dominates turns on what "carrier dependency" means.**
If it means *the vocabulary's provenance*, the proposition is strong. If it means *the enforcement
mechanism the vocabulary enables*, it is weakest — Arrow has one, Polars has none, and **Columna
currently has neither.** No recommendation is made.

**What is inherited either way:** every §5 enforcement gap; the substring sniffers; the
planner/`signature_ok` divergence; the ~19 embedded rulings; `pl.DataFrame` as the planner's result
type; and the *necessity* of a curation step separating meaning-bearing from encoding-bearing
distinctions. Only the size and shape of that curation differ.

---

## 7. The five stress cases

| case | exposed value type | sufficient state | state expressible in `types.py`? | what it stresses |
|---|---|---|---|---|
| **`sum`** | `same` as input | $S=X$; $\eta=\rho=\mathrm{id}$ | **yes, degenerately** — state *is* the value | the baseline that hides the distinction (18/26 operators) |
| **`mean`** | `Float64` (scalar) | $\mathbb R\times\mathbb N$, proved at CC:613 | **no** — no product type | scalar value, structured state — the pair is **not** the same question |
| **HLL** | `Int64` | sketch, monoid under union; precision is type identity | **named, never instantiated** | a parametric state type whose parameter carries the law |
| **`first`/`last`** | `same` as input | $(\text{value},\text{order\_key})$ | **no** — and the key's own type does not exist (`DimensionLevel` has no dtype) | ordered state; a component with no type at all |
| **covariance** | **matrix** | $(\Sigma x_i,\Sigma x_j,\Sigma x_ix_j,n)$ per pair + participation | **no**, on both sides | the only case where the **value** side is also new |

**The asymmetry across the row is the finding.** Four of five cases stress only the *state* side, and
for four of five the corpus has already proved the shape of machinery required. Covariance is the sole
case that is *also* new corpus territory — and it is new on the **value** side, where the corpus is
silent (§8), not on the state side, where it is not.

**Vector-valued additive measure** is the cleanest probe available, and it is worth stating why: it is
the one case where the value is non-scalar and the state is *degenerate* ($S=X$, componentwise $+$). It
therefore isolates **value-type richness from state-type richness completely** — if the two universes
are one algebra, this case is nearly free; if they are two, it is the case that shows where the seam is.

---

## 8. Internal value axes vs anchors — the corpus cannot reach the question

**SILENT, and more completely than expected.**

- `axis`/`axes` in the Contract Calculus is **exclusively anchor-side**. The definition: *"Let
  $\mathsf{Axis}$ be a finite set of axes. Each axis $\alpha$ has a finite rooted tree of levels"*
  (CC:389-399); *"An axis is spent when the map removes distinctions along that axis"* (CC:517).
- **The word does not occur at all in ToD v6.1.**
- In Certifiable State it occurs once, metaphorically (*"a second axis"* = a dimension of concern).
- Zero occurrences of vector / tensor / covariance across ToD and CC. The two "matrix" hits are
  certificate **tables**; `struct` appears **zero** times as a type.

> **There is no notion of structure internal to a value anywhere in the corpus.** A matrix's row/column
> axes versus analytical anchors is therefore **not a question the published vocabulary can pose** — let
> alone answer.

Two near-misses that must not be mistaken for the distinction:

- CC:285 — *"a capability is available **over the value carrier** while blocked from **spending
  particular axes**"* — separates carrier-admissibility from anchor-governance. It is **not** a claim
  that a value has axes. Reading it so would be over-reading.
- CC:2180 — the $(s,e,o)$ component gloss — types components *inside a state tuple* by governance role.
  It is the corpus's only instance of the move, and it is on the state side.

**And the tree is in the same position**: `DimensionLevel` carries no dtype, so anchor coordinates are
untyped, while measure values are typed. The two sides of the anchor/value boundary are typed by
*different amounts*, and neither by a discipline that could distinguish an internal axis from an anchor.

v0.3 §3 already holds the right placeholder — *"Internal axes are type parameters. `Matrix<Float64,5,5>`
and `HLLSketch(p)` carry structure inside the value that is not an anchor level"* — and this finding
**confirms it is uncontradicted, because nothing in the corpus speaks to it at all.** The observation
that it is *"cheap to hold now, expensive to retrofit"* is strengthened, not weakened, by the silence.

---

## 9. The architectural alternatives — enumerated, not chosen

**No choice is made or recommended.** The evidence leaves four live structures.

**A · One shared type algebra, used in two roles.** $\mathsf{Type}$ closed under products, powersets and
parameters; $S_\kappa$ and $X_\kappa/Y_\kappa$ both drawn from it; the roles distinguished by *position*
in the capability, not by *kind*.
*For:* $S_{\mathrm{sum}}=X$, $S_{\mathrm{dc}}=\mathcal P_{\mathrm{fin}}(X)$, CS's *"datatype"* of state.
*Against:* the corpus's asymmetric obligations (§2) would have to be explained away as accident, and the
value side's nominal-identity layer (RevenueUSD ≠ CostUSD) has no evident meaning for state carriers.

**B · Two type systems with a common carrier mapping.** Separate value and state universes, each with
its own formation rules, related only by $\eta:X\to S$ and $\rho:S\to Y$ and a shared notion of carrier.
*For:* the §2 asymmetry read as deliberate; the corpus's own vocabulary split (*"type"/"type"/"carrier"*,
*"type, type, algebra"*).
*Against:* nothing in the corpus builds a state carrier *except* out of value types.

**C · One value type system + a state *algebra* registry.** State carriers are not types at all but
*declared monoid structures* — $(S,\oplus,0)$ with $\eta,\rho$ — registered as capabilities are, and
typed only through the value types they are built from.
*For:* matches the corpus's actual construction most closely; `state_class` and `sufficient_state` are
already two questions in v0.3 §4; explains why the corpus registers value types and not state carriers.
*Against:* leaves *"what makes two states the same state"* — the reusable-state identity question v0.3
§10 holds open — with no equivalence relation to answer it.

**D · The smaller intermediate: a state *shape* vocabulary, no state type system.** Not a type algebra,
but a closed vocabulary of witness shapes — `none | value | product(T…) | carrier(T) | ordered(T, K)` —
sufficient to *say* $\mathbb R\times\mathbb N$ and `(value, order_key)` honestly, and nothing more.
*For:* this is what v0.3 §4's `sufficient_state: none | the value | <witness tuple> | <carrier T>` line
already sketches; it is the minimum that would let §4.1's `mean` be represented without redefining
anything; it is the cheapest thing that retires `witness`-as-taxonomy.
*Against:* an under-powered vocabulary is exactly how `witness` became a false taxonomy in the first
place, and a shape vocabulary with no equivalence relation cannot answer state identity either.

### 9.1 What evidence would distinguish them

Deliberately stated as tests, not preferences.

1. **The vector-valued additive measure** (§7). If a non-scalar value with degenerate state is nearly
   free, the universes share an algebra (A/C). If it forces a second set of formation rules, they do not
   (B).
2. **Does state need nominal identity?** RevenueUSD ≠ CostUSD over one carrier is proved for values. Ask
   whether two structurally identical state carriers can be *different states*. If yes → the state side
   needs its own nominal layer, and A collapses toward B. If no → C strengthens.
3. **The state-identity question from v0.3 §10.** Whichever structure supplies an equivalence relation
   for *"the same state"* without inventing one is the one the corpus supports. **Today no candidate
   supplies it, which is itself the sharpest open problem here.**
4. **`state_schema`.** ToD:2377 declares the field and gives it no schema language. Whatever fills that
   field *is* the answer to this question, and ToD left the slot deliberately empty.
5. **Covariance participation.** Whether the matrix's exposed structure needs to carry participation and
   population (Finding 1 §10) determines whether an exposed value can ever be a governance-bearing
   object, or must always be inert.

---

## 10. Consequences — noted, not proposed

**No implementation proposal is made. These are consequences to hold, not work to schedule.**

### 10.1 Matrices and statistics

- A covariance matrix as an **exposed value** is the first object that would require the corpus to type
  a non-scalar value — territory where it is silent (§8), not merely incomplete.
- Finding 1 §10 already establishes the harder half: an assembled matrix *"is not a single governed
  analytical object at all unless something certifies how"*, and its `Population` is not the universe.
  **The type is the smaller question; the governed identity is the larger one**, and Finding 1 owns it.
- Its **sufficient state** is a product of already-proved shapes. Nothing new is needed on that side
  except somewhere to write it down.
- A pairwise covariance carries per-pair support, which is P1-12 at matrix scale: $\binom{n}{2}$
  divergence witnesses, not one.

### 10.2 Arrow compatibility

- Arrow is **already the carrier** at the connector seam, and its schema is constructed and discarded
  every fetch. Any future type observability would be checkable against a thing that already exists.
- The wire, not the vocabulary, is the binding constraint (§5.5, v0.3 §3). No Arrow question is
  reachable before the wire carries a type at all.
- `arrow.fixed_shape_tensor`'s `dim_names`/`permutation` is a **named-axis vocabulary layered on a
  layout** — the closest external analogue to §8's unposed question. Precedent, not template.
- The `Categorical`/`Enum`/dictionary divergence (§6.2) shows Columna has already inherited one
  carrier's answer to a semantic question. That is worth knowing *before* choosing a second carrier.

### 10.3 Relation to the standing records

- **v0.3 §3** is confirmed and strengthened on every checkable claim (no type registry, `is_dtype` zero
  callers, parametric type and operator marker never meet, wire carries no dtype). This finding adds the
  corpus-side ground: **CC G1.D5 requires *"$X$ is a registered value type"*, and Columna has no type
  registry.** That is a doctrine↔code gap on the value side. **No row is created by this document.**
- **v0.3 §4** is confirmed: `witness` is not the ToD §4.7 taxonomy and must not be promoted. This finding
  supplies the *structural* reason the earlier retracted proposal was right to retract — `witness` is not
  merely a *different* four, it is **not a type system at all** (§3.3), and `projection.py` says so.
- **Finding 1** is adjacent, not overlapping: it asks what evidence must be *retained*; this asks what
  the retained thing may *be*. §0.1's `S`-collision is the seam between them and should be stated
  wherever both are cited.

---

## 11. Evidence index

**Corpus** (`services/ask/deposits/`) — `w-contract-calculus.r01.md`: 132-136, 285, 292-302, 316-320,
352-383, 389-450, 475-493, 517, 578, 584-611, 613-635, 637, 702-752, 776-782, 816-842, 960-966,
1013-1028, 1042-1086, 1128-1134, 1183-1217, 1396-1404, 1930-1952, 1958-2005, 2104-2180, 2436-2466,
2570-2604, 2655-2667, 2967-2995, 3784-3800. `w-theory-of-data.r06.md`: 640-648, 766-798, 956-968,
992-1035, 1042-1058, 1147-1175, 1286, 1484-1490, 1625, 2141, 2366-2390, 2506, 2585.
`w-certifiable-state.r01.md`: 215, 348-352, 773-777, 870, 922-928, 1013, 1183-1196, 1300-1320, 1371, 1430.

**Tree** (`packages/columna-core/src/columna_core/`) — `types.py`: 1-18, 21-42, 45, 49-73.
`operators.py`: 9-33, 37, 42-44, 47-76, 79-159, 174-178, 196-199. `model.py`: 69-78, 153-170, 177-178,
189, 203-215. `engine.py`: 24, 236-247, 266-272, 312-375, 382-417, 585-588, 691-717, 828-874, 994-1036,
1163-1166. `planner.py`: 16, 55-69, 788-796, 1479-1487, 1739, 1789, 1806-1814, 1926, 2164-2169.
`connector.py`: 18-34, 90-114, 237-257, 259-305. `sketch.py`: 4-17, 32, 61-73, 77-84. `projection.py`:
54-70. `parser.py`: 9-29, 462, 478-495, 659-678. `disclosure.py`: 232-241, 313-316. `disclosure_wire.py`:
44-61, 221-255. `describe.py`: 104-108. `adjudication.py`: 170-174, 203, 246. `compiler/compile.py`:
42-60, 77-110, 130-164. `compiler/emit.py`: 100-126.
Elsewhere — `columna-server/tools.py`: 207-208, 273-281; `columna-server/init/providers.py`: 30-35;
`columna-server/init/eval.py`: 281-284; `columna-server/demo/benchmark/manifold.cml`: 62-63;
`demos/build_benchmark.py`: 101-103; `demos/hll_case_study_demo.py`: 24-109;
`docs/frame_ql_manual_v2.md`: 677-697, 1084-1089, 1238-1256; `docs/columna_reference_manual_5e.md`:
48-118, 1512-1529; `docs/architecture/f0_reconnaissance.md`: 64, 108, 142-152, 176-179, 196, 212;
`specs/measure_algebra_design_record_v0_3.md`: 251-278, 281-358, 595-636;
`specs/measure_algebra_finding_1_support_participation_v0_1.md`: 262-300, 412-421;
`specs/column_algebra_reconciliation_m1_v0_1.md`: 40-42.

**Executed** — `docs/tools/check_manual_frameql.py` (40 examples, 0 FAIL);
`DuckDBConnector.realize()` probe on `customer_region` (§5.3), throwaway in-memory DuckDB, no repo state
touched.

**External** — [Arrow Columnar Format](https://arrow.apache.org/docs/format/Columnar.html);
[Arrow Extension Types](https://arrow.apache.org/docs/format/Columnar.html#extension-types);
[Arrow Canonical Extension Types](https://arrow.apache.org/docs/format/CanonicalExtensions.html).

---

## 12. Proposed amendment to Design Record v0.3

Offered as text for a ruling, not as an adopted change.

**To §3 (Typed datum values), add:**

> **The two universes are not symmetric in the corpus, and the asymmetry is the evidence.** The value
> side is registered (*"$X$ is a registered value type"*), well-formedness-checked, carried in the
> contract, and given an equivalence relation. The state carrier has **none of the four**. Whether that
> asymmetry is a design position or an artifact of an unfinished fragment is **open, and the corpus never
> poses the question.** Columna must therefore *choose* this relationship rather than inherit it.

**To §4 (State law), add:**

> **`witness` is not a weak state taxonomy; it is not a state taxonomy at all.** Of four witness kinds,
> one has a type in `types.py` and that type is never worn by a running value; one is a product the value
> vocabulary cannot express; one has no witness. `projection.py` classifies the field as *"mechanics"*
> withheld from the planner. **A dispatch discriminant cannot be promoted into a law taxonomy, and the
> retraction that already stands is thereby strengthened, not merely upheld.**

**Add, as a candidate principle for ruling:**

> **Representability Principle (proposed).** A sufficient state whose law is known must be *expressible*
> in the system that claims the law, or the claim degrades into a dispatch label. `mean` is the standing
> instance: its $(\Sigma x,N)$ law is proved in this corpus and unrepresentable in this build, so it is
> filed beside `median`, whose law is genuinely different in kind.
>
> **Stated with the discipline this finding was given:** a richer sufficient-state type representation
> may allow the known $(\Sigma x, N)$ law of mean to be represented **honestly** — while its exposed
> datum remains **scalar**. It would not make `mean` "non-holistic"; it would make the current
> classification *say something true*.
