# Measure Algebra — Design Finding 2
## Typed Values and Sufficient State — Reconciliation Finding

**Version:** 0.2 · **Date:** 1 September 2026 · *(v0.1: 1 September 2026 — superseded, see §0.1)*
**Type:** design finding + **proposed amendment** to *Measure Algebra Design Record v0.3* §3–§4
**Mandate:** read-only reconciliation. **No type-system implementation, `witness` refactor, Arrow migration, MME/Cache(r) redesign, MME keying change, matrix support, operator change, `mean` repair, covariance/correlation, or Frame-QL extension is authorized.**
**Governing corpus:** ToD v6.1 · **Measure Algebra v1.0 (DOI 10.5281/zenodo.22219691)** · Contract Calculus · Certifiable State · Design Record v0.3 · Finding 1 · the Cache(r) design capture · current Columna.

Governing question, restated per the v0.2 instruction:

> **How should Columna represent the type of an exposed governed value, the type/carrier of sufficient
> state, and the declared law relating those two roles?**

The prior question — *are rich datum values allowed?* — is **settled, affirmatively**, and v0.1 got it wrong.

---

## 0. Verdict

> **The published corpus already admits rich governed values, separates internal value structure from
> analytical location, and makes declared state law — not runtime dispatch — the authority for
> composition. Columna represents value typing and state mechanics through different mechanisms with
> no governed type-level relation connecting them. The Cache(r) adds a concrete realization
> requirement: sufficient state must be materializable and reusable without letting its physical
> carrier, its cache identity, or one consumer's analytical identity redefine what the state means.
> The representation architecture connecting these obligations remains open.**

Sharpened by the evidence, in one line:

> **Accidental independence is not governed independence.** Two mechanisms being separate in the code
> demonstrates two *roles*. It does not supply the *relation* the algebra requires between them.

And the sharpest single fact this reconnaissance produced:

> **Columna's `witness` and the corpus's state-law taxonomy are not two versions of one taxonomy. They
> are taxonomies of different things.** `witness ∈ {VALUE, SKETCH, ORDERED_W, HOLISTIC}` classifies
> **representability** — what fits in a Polars column. ToD §4.7 / MA v1.0 §4.1 classifies **law** —
> what composition the declared state law permits. `mean` and `median` occupy one `witness` bucket on
> entirely different grounds: one has a corpus-declared monoid state Columna cannot carry, the other
> has no corpus text at all.

**Confidence.** High on Parts I–IV (quoted, executed, or both). Moderate on Part V's Arrow reading,
which is classification rather than citation. Part VI enumerates and deliberately scores nothing.

---

## 0.1 What v0.2 retracts from v0.1

v0.1 scoped "the corpus" to ToD v6.1, the Contract Calculus and Certifiable State, and **did not read
the publication of record.** Three conclusions are withdrawn.

**R1 — RETRACTED: "the corpus is SILENT on non-scalar exposed values."**
MA v1.0 §8.1 (L786):

> *"Internal value structure is not analytical location. **A measure may carry a matrix, vector, set,
> sketch, or another composite value.** Internal axes or coordinates belong to the value type; they do
> not become anchor levels of the containing measure."*

**R2 — RETRACTED: "internal-value-axis versus analytical-anchor is unposeable or unanswered."**
The same sentence poses **and answers** it, normatively. MA v1.0 §6 (L728) goes further, giving a case
where internal structure carries *analytical* consequence: *"Pairwise covariance … would form different
support per matrix entry and therefore does not automatically have the same analytical type as
covariance over one common participating population."*

**R3 — RETRACTED: "the corpus is implicitly monistic."**
MA v1.0 is explicitly **pluralistic** about the state↔identity relation: *"Shared sufficient state also
does not merge identity"* (L788); *"several analytical families may reuse one sufficient-state carrier
without sharing family identity"* (L103); and structurally, the family identity signature
$\Sigma(F)=\operatorname{canon}(U_F,R_F,Parents(F),Establish(F),Law(F),Contracts_{id}(F))$ (L764-776)
**contains no state-carrier component at all.**

**What survives, correctly scoped.** The negative evidence remains true *of ToD v6.1 and the Contract
Calculus*: `axis`/`axes` is anchor-side only in CC and **does not occur in ToD v6.1**; zero occurrences
of vector/tensor/covariance; `struct` never appears as a type. v0.2 scopes those to those two texts.
The error was generalizing two texts' silence into the corpus's silence.

**A refinement worth more than the retraction.** MA v1.0 admits and constrains rich values
**architecturally** (§8.1, §6) while **its operational rules never inspect internal structure** — MAP1
and RED1 treat $X$, $Y_\kappa$ as opaque. So:

> Rich values are **admitted and governed at the architectural boundary, and invisible inside the
> typing rules.** That, not silence, is the corpus's actual position.

---

## 0.2 A terminological hazard, carried forward from v0.1

**`S` is overloaded across the corpus and the corpus never flags it.** $S_\kappa$ is the
**sufficient-state carrier** (CC §3.2/§7.2; MA §2.3). $S$ in $C_1=(X,U,A,E,S,\beta,\gamma)$ and in
$S\subseteq E\subseteq P$ is the **observed support set**. Unrelated objects, one letter. Because
Finding 1 is about support and this finding is about state, the two will be read together and the
collision will bite. **This document writes $S_\kappa$ for state and never bare $S$.**

---

# Part I — What the published corpus requires

## 1.1 Rich values: admitted, and bounded by one rule

**ESTABLISHED.** MA v1.0 §8.1 (L786) admits matrices, vectors, sets, sketches and other composite
values, and imposes exactly one constraint on them:

> **Internal axes or coordinates belong to the value type; they do not become anchor levels of the
> containing measure.**

Two further requirements attach:

- **A rich value's type may carry a construction claim** (L796): *"Calling a numeric matrix
  `CovarianceMatrix<Variables,Population>` makes a construction claim about its inputs and population.
  **Two numerically equal matrices may therefore have different analytical status.** Rich values can
  require more than shape checks."* This is the corpus's only type-parameter syntax, and it carries
  **both** an internal-axis set (`Variables`) **and** a governance object (`Population`).
- **Internal structure can carry analytical-type consequence** (L728, quoted in R2). Per-entry support
  divergence changes the *analytical type*, not merely the shape.

**What this does NOT settle.** No formation rule, no typing judgment, no equality, and no registry for
composite value types. MAP1/RED1 never look inside a value.

## 1.2 The capability tuple, and where state lives

**ESTABLISHED.** MA v1.0 §2.3 (L317-326), matching CC §7.2:

$$\kappa = (S_\kappa,\ \oplus_\kappa,\ 0_\kappa,\ \eta_\kappa,\ \rho_\kappa)$$

with, in CC's fuller registry form, **input type $X_\kappa$** and **output type $Y_\kappa$** as separate
slots. The structural fact that matters:

> **Value type and state carrier live in different tuples.** $X$ is a component of the contract
> $C_1=(X,U,A,E,S,\beta,\gamma)$; $S_\kappa$ is a component of the capability $\kappa$. They meet at
> exactly one point — the RED1 side condition $X = X_\kappa$ (MA L245) — and the output contract is
> stamped with $Y_\kappa$ (L256). **Sufficient state is not a component of any contract.**

**State is closed under product, and this is proved, not asserted.** $\widehat S_\kappa = S_\kappa\times
\mathbb N\times\mathbb N$ (MA L379; CC:2104-2145), with *"the product of commutative monoids is a
commutative monoid"* (CC Lemma G1.L2). Note what this demonstrates: the extension `×ℕ×ℕ` changes the
state carrier and **leaves $X$ and $Y_\kappa$ untouched.**

**On independence — the precise verdict.** The corpus **never states** that value type and state type
are independently typed, and **four times demonstrates** it:

| demonstration | citation |
|---|---|
| $S_{\text{mean}}=\mathbb R\times\mathbb N$ while the value is scalar | MA L361; CC:614-634 |
| $\widehat S_\kappa = S_\kappa\times\mathbb N\times\mathbb N$ with $X$, $Y_\kappa$ unchanged | MA L379 |
| one moment state $(N,\Sigma x,\Sigma xx^\top)$ serving several finalizations of differing type | MA L791-794 |
| $S_{\text{sum}}=X$ — the degenerate case where they coincide | CC:604-612 |

So v0.1's "never asks" becomes: **never states, though it four times demonstrates.** And two of the four
($S_{\text{sum}}=X$, $S_{dc}=\mathcal P_{\text{fin}}(X)$) build state carriers *out of* value types —
evidence, but not proof, of a shared ambient algebra. **The relation is genuinely open, and the
architecture is therefore a choice to be made rather than a fact to be discovered.**

## 1.3 Declared state law is the authority; runtime dispatch is not

**ESTABLISHED, and this is the governing rule for Part II.** MA v1.0 §4.1 (L609):

> **The declared state law determines the admissible composition. Current implementation behavior does
> not define the state law.**

§8.2 (L800-820):

> $$\text{analytical impossibility} \neq \text{implementation absence}$$
> *"A build may lack a decomposition that the analytical state law permits. Conversely, a backend may
> execute a terminal calculation for which no reusable compositional state has been declared. **Runtime
> dispatch categories therefore cannot define the Theory's state-law classes.**"*

The four state-law classes (MA L588-604 = ToD §4.7) are: commutative monoid; associative-noncommutative;
ordered/stateful; no declared compositional state. Plus the rider *"Theorems such as $G_0.2$ apply to the
commutative-monoid region. They should not be generalized by operator name to the other regions."*

**Corollary the corpus states and Columna needs:** the taxonomy's fourth class is *"no **declared**
compositional state"* — a fact about a declaration, not about an operator's nature.

## 1.4 Shared state does not merge identity

**ESTABLISHED** (MA L788-794, L103, L40), and grounded structurally: $\Sigma(F)$ carries no state
component (L764-776). Also MA §7 (L738): family preservation vs establishment is determined **ex ante**;
*"agreement among computed outputs cannot create identity after the fact."*

## 1.5 State sufficiency is relative to the continuations claimed

**ESTABLISHED**, MA §5.2 (L707, L718) — and this is the corpus basis for every materialization question
in Part IV:

> **What domain state must survive a materialization is determined by the later operations that
> materialization claims to support.**

> *"A materialization is not required to preserve every future possibility. **It must make clear what
> information it retains and therefore which derivations remain possible** subject to the governing
> contracts, identity, and evidence."*

L718 is **the only disclosure obligation placed on retained state anywhere in the publication.**

## 1.6 What the corpus does NOT settle

| question | status |
|---|---|
| A typed relation between $S_\kappa$ and $X_\kappa$/$Y_\kappa$ | **SILENT** — only the side condition $X=X_\kappa$ |
| $\eta_\kappa$, $\rho_\kappa$ written as signatures | **SILENT** — prose only (MA L323-326) |
| A state-carrier registry | **SILENT** — the word "registry" does not occur in MA v1.0 |
| Well-formedness obligation on $S_\kappa$ | **SILENT** |
| Equivalence relation on $S_\kappa$ ("same state") | **SILENT** — the only equivalence result is contract-level (G1.6) |
| Formation rules for composite value types | **SILENT** |
| median, quantile, percentile, order statistic | **SILENT — zero occurrences in the entire corpus** |
| HLL, sketch state, approximation contracts | **SILENT**; listed as open (MA L867) |
| `corr` / covariance as admitted operators | **EXPLICITLY EXCLUDED** (MA L730) |

### 1.6.1 An unreconciled tension inside MA v1.0 — reported, not resolved

The capability tuple (L317) pairs **exactly one** $\rho_\kappa$ with **one** $S_\kappa$. §8.1 (L794)
asserts a retained moment state *"may support **several** later finalizations under declared laws."*
**MA v1.0 gives no mechanism by which several finalizers attach to one carrier, and does not reconcile
the two statements.**

This is not a defect claim; it is the exact point at which §9's reusable-state question becomes
formally unexpressible. **Flagged for ruling.**

---

# Part II — What Columna currently realizes

## 2.1 Two mechanisms, and the severance is on record as design

Value typing lives in `types.py` — 11 scalar dtypes that **are** Polars dtype name strings, four type
classes, one parametric type (`HLLSketch(p)`), and `dtype_in`. State mechanics live in `operators.py`
as `witness ∈ {VALUE, SKETCH, ORDERED_W, HOLISTIC}` plus `is_monoid`, `combine`, `deliver_sql`.

They meet at exactly **one** field pair — `accepts` / `out_rule` — which describes only the *exposed
value*. No witness field is typed by anything in `types.py`; `types.py` imports nothing and never
mentions "witness".

`projection.py:54-70` states the split as architecture:

> *"An operator's SIGNATURE — the vocabulary the planner typechecks and ROUTES against: name, KIND,
> accepts, out_rule … **The mechanics (witness/combine/deliver_sql/scan_impl) are resolution and stay
> engine-side; the planner never sees them.**"*

## 2.2 The relation audit — §4's four states, applied

The published operation law relates the roles as:

```text
exposed/input value type  --η (construction/deliver)-->  sufficient-state carrier
sufficient-state carrier  --⊕ (declared combine law)-->  sufficient-state carrier
sufficient-state carrier  --ρ (projection/finalize)-->   exposed/output value type
```

Status of each link **in Columna today**:

| link | declared? | type-checkable? | implicit? | absent? |
|---|---|---|---|---|
| **input value type** $X$ | **Yes** — `TYPE <dtype>` on MEASURE, *optional*, silent `Float64` default, non-parametric (`\w+`) | Yes — `signature_ok` at parse/publish; **planner uses bare `not in`, bypassing `dtype_in`** | — | — |
| **η — construction** | No | No | **Yes** — `deliver_sql` lambda (VALUE), hardcoded `arg_max/arg_min` (ORDERED_W), `_build_base_sketches` (SKETCH) | — |
| **state carrier type** | **Only for SKETCH**, and only as a string family marker | **No** — `hll_count` emits unparameterized `out_rule="HLLSketch"`; the parameter is dropped at the operator boundary | VALUE: implicitly `out_rule`; ORDERED_W: two conventionally-named columns | HOLISTIC: no carrier |
| **⊕ — combine law** | No | No | **Yes** — `combine` is a dispatch *tag* (`"sum"`, `"union"`, `"argmax"`), resolved by an `if`-chain (`engine.py:691-701`). Associativity/commutativity/identity are **nowhere recorded** | — |
| **ρ — finalization** | No | No | **Yes** — implicit in the witness branch; `hll_estimate` runs unconditionally on the SKETCH path | No state→finalizer compatibility check exists |
| **output value type** $Y$ | **Yes** — `out_rule` | Yes | — | — |
| **state-law class** | **No — no measure declares one** | No | Read off dispatch kinds | **The declaration is absent** |
| **order requirement** | **Yes** — `FAMILY { last ORDER day }` | Partly — `needs_order` checked | — | The order key's own **type does not exist**: `DimensionLevel` has no dtype field |
| **approximation** | Implicit via `sketch_precision` on the measure | No | Rides into disclosure as RSE | Not a declared law dimension |
| **participation** | No | No | — | **Absent** (Finding 1) |

> **Reading of the table.** The two *endpoints* are typed and checkable. **Every arrow between them is
> implicit or absent.** Columna types what goes in and what comes out, and nothing about the passage.

## 2.3 Accidental independence is not governed independence

The separation is real but is **not** the corpus's relation:

- It is a separation of **visibility** (planner vs engine), not of **jurisdiction** (value law vs state law).
- Of four witness kinds, **exactly one** has a type in `types.py`, and that type is **never worn by a
  running value**: `hll_sketch_t`/`is_hll_sketch`/`hll_precision` have **zero callers in `src/`**;
  `is_dtype` has zero callers anywhere; the precision lives on the measure as an `int` and surfaces only
  as interpolated prose in trace and disclosure strings.
- The ORDERED_W pair `(value, order_key)` is **inexpressible** — there is no product type — and is
  carried as two conventionally-named DataFrame columns, with `_order` **dropped at `engine.py:375`**
  before anything is cached.
- `sketch.py:4-17` claims *"making precision type-identity turns that into a static check."* **There is
  no static check.** `hll_merge_pair` (`sketch.py:61-68`), which holds the precision guard, is **never
  called from `src/`**; the engine calls `hll_merge` directly. `dtype_in` is precision-blind by
  construction: *"A concrete HLLSketch(p) matches an `accepts` set that lists the HLLSketch family."*

> **So the one place Columna has a state type, the type identity that carries the composition law is
> dropped before it can be checked, and the check that would enforce it is dead code.** The invariant
> holds *by construction* — one precision per measure — which is Finding 1's discharge pattern
> (*"declaring earlier lowers the required grade"*) occurring by accident rather than by declaration.

## 2.4 `witness` jurisdiction — the §6 bounded conformance check

**Verdict: MIXED — (A) at every executable site; exactly two (B) sites, both prose, neither on a wire,
neither gating anything.**

**Evidence for (A) — capability/mechanics only.** All nine code reads of `op.witness` are dispatch or
capability gating. The field is structurally excluded from `OperatorSig`, from `describe.py`'s
`operator_properties`, and from every wire; only the bare boolean `is_monoid` crosses. The one refusal
mentioning "holistic" reads *"holistic operator 'mean' **not implemented**"*, reason code `unsupported`,
on the channel `disclosure.py:75` marks *"vocabulary/capability failure — **not an analytical verdict**"*.
The two face-crossing gates say *"post-launch"* — a schedule. `planner.py:1485`'s `is_monoid` gate
**exempts** `mean` rather than denying it. `adjudication.py` returns undecided. And `compile.py:42-47`:

> *"`mean` is excluded on **DEMONSTRATED failure, not on classification**: it parses clean AND checks
> clean, then refuses at execution."*

**The decisive structural argument:** the same operator with the same `witness=HOLISTIC` is **refused on
the declared-member path and served-and-governed on the inline path** (`_SERIES_REDUCE["mean"]`, under
full B-anchor law with no monoid gate; test `test_mean_has_a_law_address_without_becoming_a_monoid`).
**A field that yields opposite answers depending on which code path reads it is functioning as routing.**

**The two (B) sites — named precisely.**

**B-1 · `operators.py:101-103` read with `:30` and `:32`.** The module docstring states a general rule —
*"median, mode — (no finite witness closes it) — (HOLISTIC)"* and *"A holistic reducer carries no finite
witness, so it is reduction-sterile"* — and the `mean` entry then **asserts** *"Its witness is HOLISTIC."*
Composed, the registry asserts `mean` carries no finite sufficient state. That is false: $(\Sigma x, N)$
is proved in this project's own Contract Calculus. *Mitigation:* the docstring's HOLISTIC row names only
`median, mode`; `mean` is not in it, and `:104-108` immediately reframes to build language.

**B-2 · `docs/architecture/core_p1_k0_design_freeze.md:101-104`.** *"`mean` is registered
`witness=HOLISTIC, is_monoid=False, in_core=False`, and **no sufficient-state (`sum + count`) composition
exists anywhere in Core**"* — used to withdraw `core_p1_compiler_input.md` ruling 4's conditional
permission for `mean` to lower through exact sufficient state. *Mitigation:* scoped *"in Core"*, and
`compile.py:42-47` grounds the exclusion in demonstrated failure rather than classification.

**Nothing in the tree denies a lawful composition on the basis of `witness == HOLISTIC`, and nothing
user-facing asserts `mean` lacks compositional state.** The manuals say the opposite —
*"A mean is computed as the ratio of two fertile families — sum and count"* (framework manual 6g:391).

**The qualification that matters most.** Both (B) sites are prose that **survived a ruling already
condemning them**: `column_algebra_reconciliation_m1_v0_1.md §4` (RULED, 2026-08-31) — *"That would
ratify an implementation gap as analytical law"* — and v0.3's *"**Do not promote `witness`**."* This is
therefore **not an unnoticed law claim**; it is two sentences that outlived the ruling that killed them.

> **Reported as a narrow conformance defect against MA v1.0 §4.1/§8.2. No row opened; held for ruling
> per the standing instruction.**

## 2.5 The physical/logical wall (carried forward, unchanged in substance)

`types.py:9-11` claims the connector *"lifts physical→logical at publish."* **No such function exists**;
the only occurrence of the phrase in the tree is the claim itself. The logical type is an unchecked
author assertion; `realize()` compares only 5-valued coarse classes via a substring sniff, and *enforces*
the declaration rather than checking it. Demonstrated: **P1-18**, now rowed separately.

The wire carries **no dtype at all**. Type reaches the outside on exactly one surface —
`"dtype": mc.logical_type` on `describe_measure` — as a **Polars dtype name string on a versioned
external contract.** v0.3 §3's sequencing ruling therefore stands and binds everything downstream:

> **Type observability precedes composite types.**

---

# Part III — The eight stress cases

Attributes: **V** exposed value type · **S** state carrier · **η** construction · **⊕** combine ·
**ρ** finalizer · **B** boundedness/growth/order · **I** identity implications · **C** what the corpus
establishes · **X** what Columna represents / what is open.

### III.1 `sum` — the case that hides the distinction
**V** $X$ (nominal; RevenueUSD ≠ CostUSD over one carrier) · **S** $S_{\text{sum}}=X$ — *state is the
value* · **η** $\mathrm{id}$ · **⊕** $+$, A✓ C✓ id $0$ · **ρ** $\mathrm{id}$ · **B** O(1), unordered ·
**I** preserves family, **unless** a blocked axis is spent (G0.7 — monoid law is *necessary, not
sufficient* for identity preservation) · **C** ESTABLISHED CC:604-612, ToD:970-986 · **X** faithful.
**18 of 26 registry operators carry `witness=VALUE`** — the degenerate case holds for 69% of the
registry, which is precisely why the value/state distinction stayed implicit.

### III.2 `mean` — scalar value, structured state
**V** `Float64` · **S** $\mathbb R\times\mathbb N$ · **η** $x\mapsto(x,1)$ · **⊕** componentwise $+$,
A✓ C✓ id $(0,0)$ · **ρ** $(s,n)\mapsto s/n$ · **B** O(1), unordered · **I** the ratio map *"does not by
itself mint a family identity"* (MA L527) · **C** ESTABLISHED CC:614-634, ToD:988-1006, MA L361; ~13
corpus sites · **X** classified `HOLISTIC`/`is_monoid=False` **on ρ's output rather than on S**.

> **Stated with the required discipline:** a richer **sufficient-state representation** may allow mean's
> known $(\Sigma x, N)$ law to be represented **honestly**, while its exposed datum remains **scalar**.
> This is not a claim that rich datum types make `mean` non-`HOLISTIC`; `mean` stays scalar-valued.

### III.3 HLL — parametric sketch state → scalar value
**V** `Int64` (estimate); carrier `HLLSketch(p)` · **S** register array at precision $p$ · **η**
`hll_count` · **⊕** register-wise union, A✓ C✓ id = empty sketch · **ρ** `hll_estimate` · **B**
**bounded** — $2^p$ registers, fixed; unordered · **I** exact and approximate distinct *"can claim the
same analytical target"* with different certificates (ToD:2056-2058); CS:876-899 separates $c_{merge}$
(mechanical) from $c_{card}$ (statistical) — *"approximate target $\not\Rightarrow$ uniformly approximate
certificate"* · **C** ESTABLISHED · **X** **the only case where Columna carries a non-value carrier**,
and it carries it well — except the parameter is dropped at the operator boundary (§2.3).

### III.4 `first` / `last` — ordered structured state, with a corpus-named rule gap
**V** $X$ · **S** $(\text{order key},\ \text{value})$ + declared order + tie policy · **η** value at the
declared-order extremum · **⊕** argmax/argmin, A✓ C✓ **only given a declared total order and a
deterministic tie rule** · **ρ** take the value component · **B** O(1) state, but requires **declared**
order, *"rather than physical enumeration"* (CC:37) · **I** order is an analytical declaration · **C**
ESTABLISHED CC:641, CC:1590 (G0.11), ToD:1075 — *"`FIRST` or `LAST` **can** be compositional when state
retains an order key, value, and deterministic tie-breaking rule"* · **X** implements the **total** case.

> **The corpus names its own gap here, and it is not median's gap.** CC:4260: *"$G_1$ contains partial
> support and coverage but **explicitly excludes ordered partial reducers**."* CC:4270: *"**This is a
> rule gap, not a proof that the candidate value is wrong.**"* Columna has no counterpart gate.

### III.5 Exact distinct count — the decisive contrast
**V** $\mathbb N$ · **S** $S_{dc}=\mathcal P_{\text{fin}}(X)$ — **a set of governed identities** · **η**
$x\mapsto\{x\}$ · **⊕** $\cup$, A✓ C✓ id $\varnothing$, **and duplication-invariant** · **ρ** $|S|$ ·
**B** **UNBOUNDED — and fully compositional** · **I** same analytical target as HLL, different
certificate; finalized counts are not re-aggregable ($|S_1\cup S_2|\neq|S_1|+|S_2|$) · **C** ESTABLISHED
CC:2967-2988, ToD:1018-1035 · **X** **NOT REPRESENTED.** `distinct` *is* the HLL sketch; there is no
set-valued dtype.

> **This is the finding's sharpest case, and it requires no new law.** The corpus's own worked example
> proves that **unbounded ≠ non-compositional**. Columna offers bounded-approximate (HLL) or
> recompute-from-base, and **no third option** — so it cannot express a measure whose state is
> unbounded but lawful. That is a *representation* limit, not a law limit, and it is the cleanest
> available demonstration that `witness` classifies representability.

### III.6 median — **SILENT**, and it must stay that way
**Corpus search across CC, ToD, CS and MA v1.0:** `median` **0 hits**; `quantile` **0**; `percentile`
**0**; `order statistic` **0**; `t-digest`/`approx_quantile` **0**. And `holistic` occurs **exactly once
in the entire corpus** — CC:289, in the *related-work* section:

> *"Gray et al.'s distributive, algebraic, and **holistic** classification concerns the structure needed
> to combine partial aggregate results."*

CC names Gray's taxonomy and then states what the core does **instead** (CC:291-307): represent a
capability as $(S_\kappa,\oplus_\kappa,0_\kappa,\eta_\kappa,\rho_\kappa)$, *"making staged aggregation a
theorem about state."* **Columna's `HOLISTIC` enum is named after a taxonomy the corpus cites and
declines to adopt.**

Against the four states of affairs:

| | claim | corpus support |
|---|---|---|
| **(i)** no *declared compositional state* | ToD §4.7 row 4 | **NOT ASSERTED** — no corpus text places median in any row; and the row is a property of a *declaration*, of which median has none in the corpus |
| **(ii)** no *bounded/compact* state | a size claim | **NOT ASSERTED** — the corpus never uses state size as a criterion, and III.5 is its own counterexample |
| **(iii)** retained roots or richer state required | ToD §4.7 row 4's remedy | **NOT ASSERTED of median** |
| **(iv)** current implementation lacks a representation | a build fact | **TRUE — and the only supportable statement** |

> Any statement of the form *"median is analytically non-compositional per the corpus"* is
> **unsupported**. `operators.py:30`'s *"no finite witness closes it"* is, by MA L820, a **runtime
> dispatch category**. It records what this build does.

### III.7 Additive vector-valued measure — value rich, state degenerate
**HYPOTHETICAL** — no corpus text constructs one. **V** a vector type with $(|X|,+_X,0_X)$ · **S**
**degenerate: $S=X$** · **η** $\mathrm{id}$ · **⊕** componentwise $+_X$ · **ρ** $\mathrm{id}$ · **B**
O(dim), fixed · **I** internal coordinates are value-type structure, **not anchor levels** (MA L786) ·
**C** ESTABLISHED-as-permitted: MA L786 + CC §21.2 (2997-3033) *additive scalable types* — a commutative
additive monoid plus a $\mathbb Q_{\geq0}$ scalar action, capability $\kappa_X^+$ · **X** not
representable — `DTYPES` is a Polars scalar subset.

> **This case isolates the two axes completely:** rich *value*, degenerate *state*. It is the cleanest
> probe of whether the two universes share one algebra — and the corpus already supplies the algebraic
> requirements a value type must meet (CC §21.2) without ever exercising them.

### III.8 covariance — state published, operator refused
**HYPOTHETICAL.** **V** `CovarianceMatrix<Variables,Population>` · **S** moment state
$N,\ \Sigma x,\ \Sigma xx^\top$ · **η** $x\mapsto(1,x,xx^\top)$ · **⊕** componentwise $+$, A✓ C✓ id
$(0,0,0)$ · **ρ** declared finalization from moments · **B** $O(k^2)$ in variable count, unordered ·
**I** *"Shared sufficient state also does not merge identity … Reuse of one state carrier does not make
the resulting analytical families identical"* (MA L788-794) · **C** MA §8.1 supplies the state; **§6
(L730) refuses the operator**: *"Until such a formation and participation law is declared, `corr` is
**not** an operator of the proved Measure Algebra. It is a candidate extension whose numerical
implementation would not be enough to admit it."* · **X** absent entirely.

> **Covariance is the one case where the corpus publishes the sufficient state and still withholds
> admission — on participation grounds** (MA L728: pairwise covariance forms *different support per
> matrix entry*). Finding 1 §10 owns the harder half: the assembled matrix is not a governed object
> unless something certifies how. Finding 1 §8 further proves the state is not substitutable:
> a moment state computed complete-case and one computed pairwise are **different analytical objects
> at numerically identical values.**

### III.9 Cross-cutting reading

| | corpus taxonomy | Columna `witness` |
|---|---|---|
| classifies | **what the declared state law permits** | **what fits in a Polars column** |
| `mean` | commutative monoid over $\mathbb R\times\mathbb N$ | `HOLISTIC` (no product type to carry it) |
| `median` | **no text** | `HOLISTIC` (no bounded witness) |
| exact distinct | commutative monoid over $\mathcal P_{\text{fin}}(X)$ | **inexpressible** |
| criterion used | declared law | representability |

**Two Columna classifications are keyed on ρ's output rather than on S**: `mean`
(*"a displayed average does not combine associatively"* — a fact about $\rho$, not $S_\kappa$) and
`distinct` (`out_rule="Int64"` on a SKETCH witness). The corpus's boxed rule is
*displayed value ≠ sufficient state ≠ analytical identity ≠ material realization.*

---

# Part IV — Materialization: the Cache(r) as consumer requirement

**Jurisdictional note, held throughout.** The materialization layer **reads** governed law; it does not
write it. Nothing in this Part is treated as authority over type or state law.

## 4.1 Correction: the design exists, and it is the Cache(r)

An earlier reading of ledger row **P5-01** — *"No MME exists. The only hit for `MME` in the tree is the
topology record's own list of claims it does not make"* — is **true about the token and materially
incomplete about the corpus.** The engine is absent; **the doctrine, the role capture, and two ruled
laws are present.**

**`specs/context/design_capture_execution_positions_v0_8.md:249-284` — "The fourth position — the
Cache(r) (sound aggregate navigation)"**, status *"design-stage, to be purpose-built"*:

> *"a cached column at anchor A serves a request at anchor A′ **iff the algebra certifies the reduction
> A→A′** — same criterion that gates a fresh query. **A cache hit is a theorem application.**"*

> **The admission law (RULED, Huayin, 2026-07-14): only the fertile is cached; the fertile is cached as
> components first.** *"Cache the sketch, never the estimate"* and *"cache the components, never the
> derivation" … the cache stores only what may lawfully travel.*

> **The never-substitute law (RULED, Huayin, 2026-07-14): a cache hit may never change the quantity
> asked.**

**This is the single most important connection in Part IV.** The admission law is the **value/state
distinction stated as a caching rule** — *cache the sketch, never the estimate* is
$\text{sufficient state} \neq \text{displayed value}$ in materialization vocabulary — **ruled on
2026-07-14, six weeks before the Measure Algebra was published.** The Cache(r) already encodes the
corpus's distinction; what it lacks is a representation in which to *say* it.

The topology record additionally names identity-keyed materialization as Platform direction in eight
places (`:143`, `:146`, `:156`, `:202`, `:362`, `:432`, `:569`, `:103`), and poses the four
materialization questions at `:532-537` that P5-04/P5-05 answer.

*(Recorded for accuracy: **P5-06's citation "record §22" is unresolvable in-tree** — the topology record
has 17 sections and the text appears nowhere else.)*

## 4.2 The three precursors, and what their identity consists of

| precursor | key | carries state? | survives request? |
|---|---|---|---|
| `WitnessStore` | `(measure, member, base_level)` + `version` field | **yes** — `dict[bucket → hll_sketch]` | yes (process lifetime) |
| `CacheEntry` | `(measure, member, target, universe, where)` + `version` | only for SKETCH; `None` otherwise — **and `CacheEntry.sketches` has no reader** | yes (unbounded — P1-08) |
| `_value` / `_order` columns | **none** | yes, transiently | **no** — `_order` dropped at `engine.py:375` |

## 4.3 The ten semantic obligations — established requirements, current status

Per §9.A. These are **semantic obligations, not a storage schema.** Design Record v0.3 §4 already names
the law-side list (`state_class`, `sufficient_state`, `combine_law`, `order_requirement`, `finalizer`,
`approximation`, `participation`) and grades it **LATENT** — *"the classes exist; the declaration does
not"*, with *"**No measure declares a `state_class` today**; it is read off dispatch kinds, which is
precisely what §4.7's first rider forbids."*

| obligation | status | evidence |
|---|---|---|
| **state type / carrier** | **PARTIAL** — a carrier type exists for the sketch family only, as a string tag | `types.py:52-61`; `witness` is a dispatch kind, disqualified by v0.3 §2.2 |
| **analytical input identity** | **ABSENT from both keys** — identity is by *measure name* and *member name*; `pre_expr`, `distinct_col`, `logical_type` are in the measure record and in **neither** key | `sketch.py:104`; `engine.py:228` |
| **input anchor** | **PRESENT** for the witness (`base_level`); **ABSENT** for the cache — `target` is the *output* anchor | `sketch.py:81`; `engine.py:228` |
| **universe / population** | **PARTIAL, by name only** — cache key carries a `uni` string; **the witness key carries no universe field at all**, enforced only transitively through the version token | `engine.py:228`; `sketch.py:104` |
| **support / participation standing** | **ABSENT from both keys and both payloads.** Confinement is *applied* (P1-01, closed) but the resulting support set is not recorded on the artifact | ledger P5-02 |
| **state-law identity** | **ABSENT.** Nothing records the law the state was built under. **`Witness.precision` has zero readers** — the disclosure reads `meas.sketch_precision` from the *current declaration* | `sketch.py:82`; `engine.py:1165-1166` |
| **construction law** | **ABSENT as data** — encoded only as executable Python (`hll_count`) | `sketch.py:43-49` |
| **combine compatibility** | **DECLARED, NOT ENFORCED ON THE SERVING PATH** — `hll_merge_pair`'s precision check is called only from a demo; `dtype_in` is precision-blind | `sketch.py:61-68`; `engine.py:1028` |
| **finalizer / project compatibility** | **ABSENT as a check; hardwired as dispatch** — nothing associates a stored state with an admissible finalizer *set* | `engine.py:1034` |
| **publication / currency evidence** | **PRESENT — the strongest link.** One token for both artifacts, installed at one boundary. **But data-state only** — not manifold/declaration identity, not admission/scope identity | `engine.py:154-176`; `planner.py:162-166`; cf. P1-06 |

## 4.4 State Type ≠ State Law ≠ State Materialization

Per §9.B, made explicit, with the jurisdiction of each:

```text
State Type            what the carrier IS            semantic/type layer   — ABSENT except for sketches
State Law             how it composes, and to what   semantic/law layer    — LATENT (v0.3 §4)
State Materialization realization, retention,        Cache(r)              — design-stage; two laws RULED
                      eviction, lookup, reuse
Physical carriage     bytes and compute              Polars/DuckDB/Arrow   — present, and see Part V
```

The corpus supplies the first two and assigns the third its obligation (MA §5.2 L707/L718). **Columna
currently has the fourth, part of the third, and almost none of the first two.**

## 4.5 The keying question — a real distinction, and the corpus already rules on soundness

**§9.C answer: YES, the distinction is real, and the shipped keys assume it away.** ESTABLISHED, three
independent ways:

1. **The key is `(measure, member, base_level)`** — and `member` is the *finalizer's name*
   (`"distinct"`, whose `out_rule="Int64"` is the finished estimate). **The state is filed under the
   name of the number it will become.**
2. **The writer forecloses multiplicity by construction**: `engine.py:1075-1080` takes
   `member = next(iter(meas.family))` — the *first* family member. A second sketch-family member on the
   same measure would never get a witness and never find one.
3. **The reader looks up under the requesting member** (`engine.py:1009`). Two finalizers over an
   identical carrier are two lookups into a store that only ever holds one.

Mechanically one sketch *is* the state several projections need — `hll_merge` is finalizer-agnostic.
**Structurally there is no way to address it.**

**And Finding 1 §8 already stated the soundness constraint on any future key:**

> *"A reusable-state cache keyed on **(family, anchor, filter)** alone is **unsound** as soon as two
> participation laws are admissible. The key must carry the participation law and the support contract.
> It must **not** carry the realized support set — that is attestation, it belongs in $E$."*

The shipped keys are `(measure, member, base_level)` and `(measure, member, target, uni, where)` —
**exactly the shape that record calls unsound.** Core is safe today only because it admits **one**
participation law. Corroborated independently by `f0_reconnaissance.md:173`: *"current cache/state
objects are **keyed implementation artifacts, not semantic identity**."*

**No key scheme, store count, or object model is proposed here.** The established finding is only that
*materialization of a governed measure $F@A$* and *materialization of reusable governed state whose
identity cannot be inherited from one arbitrary finalizer* are **different objects**, and that
MA v1.0 §8.1's *"several later finalizations"* is currently unexpressible — which is also where
§1.6.1's tension inside the publication bites.

## 4.6 HLL as the bridge case — §9.D confirmed, and understated

**Nothing in the code distinguishes the two material standings.** P5-04 verified clause by clause:

- *"Result cache adds only `Caveat(FRESHNESS, "served from cache")`"* — **TRUE**, two producers only,
  and it rides the *mechanical* channel, which by design cannot move severity or cleanliness.
- *"witness reuse adds **no marker at all**"* — **TRUE, provable from one line.** `engine.py:247`
  returns `self._disc(...)` identically on the witness-hit and lazy-build paths, and `_disc` never sees
  the witness.

**Stronger than P5-04 states.** The sketch APPROXIMATION caveat is computed from
`meas.sketch_precision` — the **declaration** — not from the artifact's own `precision` field, which has
no reader. So the disclosure cannot say a stored artifact was involved, cannot say *which*, and could in
principle assert the wrong relative standard error, with no type error, because the precision guard is
not on the serving path. Core is protected today only because `publish()` rebuilds witnesses and the
version token folds **data** identity only. **This is P1-06's shape one level down.**

Three further docstring/behaviour divergences found and recorded, not repaired:
`sketch.py:20` claims witnesses are *"built EAGERLY at publish … never lazily on a query"* — contradicted
by the lazy fallback at `engine.py:1013-1017`; `sketch.py:25` claims *"its staleness is a disclosure"* —
**not implemented**, a stale witness is silently bypassed with no caveat; `WitnessStore` has **no
eviction or clear API** (tests reach `_w` directly).

> **§9.D's thesis is therefore established with evidence: state type alone does not determine
> materialization standing.** `HLLSketch(p)` is one type with (at least) two standings, and Columna
> currently marks neither.

## 4.7 Non-interference as a test — §9.E

**What is guaranteed** (`test_witness_non_interference.py`, ten tests, three standing rules): a carved
universe stays carved in materialized state, eager and lazy alike; unknown data identity never reads as
unchanged and never becomes stored state; materialized-state currency uses the **complete computation
dependency set**. These are strong, and rule 2 is notably tested independently of the writer.

**What is absent: any notion of two state instances being interchangeable for a governed continuation.**
What exists is (a) key equality — sameness by *name*; (b) version equality — a data-state fingerprint,
i.e. "same data", not "same analytical object"; (c) runtime dtype family membership, **precision-blind**;
(d) a precision equality check that is never invoked.

> **So non-interference guarantees the state was built under the right population and is not reused when
> the data moved. It guarantees nothing about whether two states are the same analytical object.**

**Per §9.E this finding does not solve reusable-state equivalence.** What is *missing* is nameable
precisely, and the corpus does not supply it: **an equivalence relation on $S_\kappa$** — the corpus is
SILENT (§1.6), Finding 1 §8 supplies a *necessary* condition on the key (participation law + support
contract) but not a sufficient one, and v0.3 §10 holds the question open. That is the sharpest single
gap this finding identifies, and it is upstream of every architecture in Part VI.

---

# Part V — Arrow / Polars as a jurisdiction question

**Reframed per §8. The question is not Arrow-versus-Polars.**

> **Should any Material World engine's dtype vocabulary define Data World logical type identity at all?**

## 5.1 The wall exists in intent, and is breached in the vocabulary itself

Columna's architecture is right and should be preserved: physical types below the connector, and the
planner does not see them. No SQL type name reaches `planner.py`.

**But the logical vocabulary is not merely *modelled on* Polars — it is Polars.** `types.py`'s eleven
dtype strings **are** Polars dtype names; the coupling is **identity, not a mapping table you could
swap.** `Enum` distinct from `Categorical`, `String` rather than `Utf8`, `Duration`/`Time` as first-class
scalars — these are specifically-Polars carve-ups. And that vocabulary is **published**: `"dtype":
mc.logical_type` on a versioned external contract.

> **So a Material World vocabulary is supplying Data World type identity above the connector boundary,
> notwithstanding that no physical type name crosses it.** The wall holds against *type names* and
> leaks at the level of *which distinctions exist*.

Two live consequences, already visible: dictionary encoding is *"a data representation technique"* in
Arrow and **a distinct dtype in Polars** — Columna has already inherited one engine's answer to a
semantic question; and `adjudication.py:170-174` selects exact-vs-tolerance comparison from the
**delivered runtime dtype**, so an analytical verdict already turns on a type DuckDB chose.

## 5.2 Arrow, evaluated in the four permitted roles

- **Interoperability / carriage target** — already true: `pl.from_arrow(...arrow())` is the connector
  boundary. Arrow schemas are constructed and discarded every fetch.
- **Rich physical representation** — genuine: nested types, fixed-size lists, structs.
- **Prior art for structs / vectors / tensors / extension types** — the strongest reason to read it.
  `ARROW:extension:name` + `ARROW:extension:metadata` with a **graceful-degradation guarantee** is a
  defined, portable slot for semantics the carrier does not define. `HLLSketch(p)` is already an
  improvised instance of exactly that pattern — storage, name, parameter — implemented as
  f-string plus `startswith` plus slicing, and §2.3 shows precisely where the improvisation breaks.
  `arrow.fixed_shape_tensor`'s `shape` / `dim_names` / `permutation` is **named-axis semantics layered
  on a layout** — instructive prior art for §III.7/III.8, and *nothing more*.
- **Possible connector / materialization substrate** — plausible; out of scope here.

## 5.3 The jurisdictional verdict

**Arrow's type taxonomy is not the ToD logical type taxonomy, and adopting it as such would move the
dependency rather than remove it.** Arrow's own specification says it *"doesn't have separate notions of
physical types and logical types"* — it **declines the distinction the question is about**. A system
adopting Arrow's list as its semantic vocabulary would inherit `list` vs `large_list`, `date32` vs
`date64`, `string` vs `large_string` as *type* distinctions requiring `accepts` rulings.

Decisively: **none of Part II's defects is a vocabulary defect.** The missing lift, the unenforced
delivery promise, the coarse-class sniff, P1-18, the planner's `dtype_in` bypass, the dropped sketch
parameter, the absent combine law — **not one is caused by the names being `Float64` rather than
`float64`.** Renaming the vocabulary fixes none of them.

> **The Material World must not acquire Data World authority.** The rule is the finding; which carrier
> sits below it is a separate and later question. **No adoption is recommended, and none is authorized.**

---

# Part VI — What genuinely remains open

Per §3's third bucket, and deliberately unscored.

**The four candidate architectures** (carried from v0.1, corrected by MA v1.0):

- **A · One shared type algebra, two roles.** *For:* $S_{\text{sum}}=X$, $S_{dc}=\mathcal
  P_{\text{fin}}(X)$, CS's *"datatype"* of state. *Against:* the corpus's asymmetric obligations; the
  value side's nominal-identity layer (RevenueUSD ≠ CostUSD) has no evident meaning for carriers.
- **B · Two type systems with a common carrier mapping.** *For:* the asymmetry read as deliberate;
  *"type / type / **carrier**"* in one bulleted registry. *Against:* nothing in the corpus builds a state
  carrier except out of value types.
- **C · One value type system + a state *algebra* registry.** State carriers as declared monoid
  structures, typed only through the value types they are built from. *For:* matches the corpus's actual
  construction most closely; explains why value types are registered and carriers are not. *Against:*
  supplies no equivalence relation.
- **D · A state *shape* vocabulary, no state type system.** `none | value | product(T…) | carrier(T) |
  ordered(T,K)` — enough to *say* $\mathbb R\times\mathbb N$ and `(value, order_key)` honestly, and no
  more. *For:* it is v0.3 §4's `sufficient_state` line already sketched; the minimum that retires
  `witness`-as-taxonomy. *Against:* an under-powered vocabulary is how `witness` became a false taxonomy.

**The discriminating evidence** (unchanged in kind, sharpened by Part III):

1. **The vector-valued additive measure** (III.7) — rich value, degenerate state. If nearly free, the
   universes share an algebra (A/C); if it forces a second set of formation rules, they do not (B).
2. **Does state need nominal identity?** Can two structurally identical carriers be *different states*?
   Yes → A collapses toward B. No → C strengthens.
3. **The equivalence relation.** Whichever structure supplies *"the same state"* without inventing it is
   the one the corpus supports. **No candidate currently supplies it** (§4.7) — the sharpest open problem
   here, and upstream of the other three.
4. **`state_schema`.** ToD:2377 declares the field and gives it no schema language. **Whatever fills that
   slot is the answer**, and ToD left it deliberately empty.
5. **Exact distinct count** (III.5) — a case needing **no new law**, only a representation. Whether an
   architecture can express $\mathcal P_{\text{fin}}(X)$ is a cheap and decisive test.

**Open questions that are not architecture choices:**

- **How do several finalizers attach to one carrier?** MA §8.1 asserts it; the capability tuple pairs one
  $\rho$ with one $S_\kappa$ (§1.6.1). Unexpressible today, and it gates §9.C.
- **Ordered *partial* reducers** — a rule gap the corpus names itself (CC:4270), with no Columna
  counterpart gate.
- **Participation for composite values** — MA L728; the reason `corr` is refused admission.

---

# Part VII — Newly exposed, for ruling

**No rows opened. No repairs made. Reported for decision.**

1. **The `mean` / `HOLISTIC` conformance question (§2.4).** MIXED: (A) at every executable site; two
   (B) prose sites — `operators.py:101-103` with `:30`/`:32`, and `core_p1_k0_design_freeze.md:101-104`.
   Both survived the 2026-08-31 *"Do not promote `witness`"* ruling. **Held for ruling per instruction;
   no row opened.**
2. **The MA v1.0 internal tension (§1.6.1)** — one $\rho_\kappa$ per $S_\kappa$ (L317) vs *"several later
   finalizations"* (L794). A question about the publication, not about Columna.
3. **Exact distinct count is inexpressible (III.5)** — a lawful, corpus-worked state carrier Columna
   cannot represent. Needs no new law.
4. **`Witness.precision` has zero readers**; the RSE disclosure reads the current declaration instead
   (§4.6). Latent, not currently reachable.
5. **`hll_merge_pair`'s precision guard is dead code** (§2.3) — the type identity that carries the merge
   law is unenforced on the serving path.
6. **`CacheEntry.sketches` has no reader.**
7. **Three `sketch.py` docstring claims are contradicted by the engine** (§4.6): "never lazily", "staleness
   is a disclosure", "PROVENANCE-bearing".
8. **P1-06 applies to the `WitnessStore` as well as the result cache**, and the row names only the cache.
   `WitnessStore` has no clear API at all.
9. **P5-01 understates the corpus** (§4.1) — the Cache(r) design capture with two RULED laws exists.
   **P5-06's "record §22" citation is unresolvable.**
10. **The published `"dtype"` field is a Polars name on a versioned external contract** (§5.1).

---

# Part VIII — Evidence index

**Governing publication** — Measure Algebra v1.0, read via
`git show ingest/measure-algebra-v1-0:services/ask/deposits/w-measure-algebra.r01.md` (917 lines, read in
full): L40, L46, L79-87, L95, L103, L109-131, L158-160, L204-216, L227, L242-258, L266-276, L300, L314-368,
L374-406, L438-527, L575, L588-609, L657, L663-718, L722-734, L738-778, L784-796, L800-844, L848-873, L901.
*(This publication was absent from v0.1's index. That was the defect v0.2 corrects.)*

**Corpus** (`services/ask/deposits/`) — `w-contract-calculus.r01.md`: 37, 132-136, 148-152, 263-266, 285-320,
352-383, 389-450, 475-493, 517, 578-641, 702-752, 776-842, 960-966, 1013-1086, 1128-1134, 1183-1227,
1396-1404, 1448, 1499-1592, 1930-1952, 1958-2005, 2104-2180, 2436-2466, 2570-2604, 2655-2667, 2940-2996,
2997-3033, 3096-3107, 3784-3800, 4260-4312. `w-theory-of-data.r06.md`: 640-648, 766-798, 944, 956-1035,
1042-1079, 1147-1175, 1286, 1484-1490, 1625, 2036-2060, 2141, 2366-2390, 2506, 2585.
`w-certifiable-state.r01.md`: 215, 324-352, 773-777, 868-900, 922-928, 1013, 1183-1196, 1300-1320, 1371, 1430.

**Records** — `specs/measure_algebra_design_record_v0_3.md`: 217, 251-278, 281-358, 447, 595-636.
`specs/measure_algebra_finding_1_support_participation_v0_1.md`: 262-300, 375-391, 412-421.
`specs/column_algebra_reconciliation_m1_v0_1.md`: 40-42, 80-96.
**`specs/context/design_capture_execution_positions_v0_8.md`: 249-284 (the Cache(r), two RULED laws).**
`specs/context/adr_033_vocabulary_reconciliation.md`: 21.
`docs/architecture/topology_core_platform_delivery_v0_1.md`: 103, 109, 143-156, 197-202, 362, 432, 484-501,
519-537, 569. `docs/architecture/f0_reconnaissance.md`: 64, 108, 142-152, 173-179, 196, 212.
`docs/architecture/core_p1_k0_design_freeze.md`: 101-127. `docs/architecture/core_p1_compiler_input.md`: 216-218.
`docs/architecture/consolidated_ledger_v0_1.md`: P1-01 (closed), P1-03, P1-06, P1-08, P1-09, P1-18, P5-01…P5-06.
`docs/columna_framework_manual_6g.md`: 143, 363, 391, 655-659, 763. `docs/columna_reference_manual_5e.md`: 48-118.

**Tree** (`packages/columna-core/src/columna_core/`) — `types.py`: 1-73. `operators.py`: 9-33, 37, 42-76,
79-159, 174-178, 196-199. `model.py`: 69-78, 153-170, 176-189, 203-215. `engine.py`: 24, 62-78, 116-176,
225-247, 266-272, 312-375, 382-417, 585-616, 691-717, 827-877, 990-1067, 1069-1100, 1156-1167.
`planner.py`: 16, 55-69, 130-172, 453, 788-796, 1479-1519, 1739, 1789, 1806-1814, 1926, 2164-2169.
`connector.py`: 18-34, 90-114, 139-164, 237-305. `sketch.py`: 4-27, 32-74, 77-120. `projection.py`: 54-70.
`parser.py`: 9-29, 462, 478-495, 659-678. `disclosure.py`: 75, 232-241, 313-316. `disclosure_wire.py`: 26-29,
44-61, 221-255. `describe.py`: 104-108. `adjudication.py`: 150-156, 170-174. `compiler/compile.py`: 42-60,
77-110, 130-164. `compiler/emit.py`: 100-126. `frameql.py`: 34, 55, 70.
Tests — `test_witness_non_interference.py` (10 tests, 3 standing rules), `test_generated_family_law.py`: 223-241.
Elsewhere — `columna-server/tools.py`: 207-208, 253-281; `columna-server/demo/benchmark/manifold.cml`: 63;
`demos/build_benchmark.py`: 101-103; `demos/hll_case_study_demo.py`: 24-117; `demos/types_demo.py`: 41-71.

**Executed** — `DuckDBConnector.realize()` probe on `customer_region` (P1-18);
`docs/tools/check_manual_frameql.py` (40 examples, 0 FAIL); corpus term counts for
median/quantile/percentile/order-statistic/holistic (§III.6), re-verified by hand.

**External** — [Arrow Columnar Format](https://arrow.apache.org/docs/format/Columnar.html);
[Extension Types](https://arrow.apache.org/docs/format/Columnar.html#extension-types);
[Canonical Extension Types](https://arrow.apache.org/docs/format/CanonicalExtensions.html).

---

# Part IX — Proposed amendments to Design Record v0.3

Offered as text for a ruling. **Not adopted, not applied.**

**To §3 (Typed datum values) — replace the "LATENT in ToD" framing:**

> **Rich governed values are ADMITTED, and bounded by one published rule.** MA v1.0 §8.1: a measure may
> carry a matrix, vector, set, sketch or other composite value, and *"internal axes or coordinates belong
> to the value type; they do not become anchor levels of the containing measure."* A rich value's type may
> additionally carry a **construction claim** — `CovarianceMatrix<Variables,Population>` — so that two
> numerically equal matrices may have different analytical status. **What remains open is representation,
> not permission.** Note that the corpus admits rich values *architecturally* while its typing rules
> (MAP1, RED1) never inspect internal structure.

**To §4 (State law) — strengthen the `witness` finding:**

> **`witness` is not a weak state taxonomy; it is a taxonomy of a different thing.** It classifies
> **representability** — what fits in a Polars column — where ToD §4.7 / MA §4.1 classifies **law**.
> The proof is internal: `mean` and `median` share a bucket on entirely different grounds, and exact
> distinct count — a commutative monoid over $\mathcal P_{\text{fin}}(X)$, **unbounded and fully
> compositional** — has no bucket at all. **The corpus never uses boundedness as a state criterion and
> supplies its own counterexample.** Recorded additionally: Columna's `HOLISTIC` is named for Gray et
> al.'s classification, which the Contract Calculus **cites once, in related work, and declines to
> adopt** (CC:289).

**Add, as a candidate principle for ruling:**

> **Governed Relation Principle (proposed).** Two mechanisms being separate does not establish the
> relation the algebra requires between them. A system claiming a state law must be able to *state* —
> and check — the construction, combination and finalization arrows connecting a typed exposed value to
> a typed sufficient state. **Columna today types both endpoints and leaves every arrow between them
> implicit or absent.** Accidental independence is not governed independence.

**Add, for the materialization boundary:**

> **State Type ≠ State Law ≠ State Materialization.** The semantic layer supplies the first two; the
> Cache(r) owns realization, retention, eviction, lookup and reuse; Arrow/Polars/DuckDB physically carry
> instances. The Cache(r)'s admission law — *"cache the sketch, never the estimate"*, RULED 2026-07-14 —
> **already encodes the corpus's value/state distinction as a caching rule, six weeks before the algebra
> was published.** What it lacks is a representation in which to say it. And per MA §5.2, a
> materialization *"must make clear what information it retains and therefore which derivations remain
> possible"* — the only disclosure obligation the publication places on retained state, and one Columna
> does not currently discharge.
