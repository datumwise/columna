# Frame-QL vNext — Authority Reconciliation and Compatibility Rulings

**Working Draft 0.1 — 4 September 2026**  
**Status:** Supervisor architecture/reconciliation note  
**Purpose:** Reconcile the settled Frame-QL vNext semantic-expression rulings with the repository's current four-document Frame-QL authority structure.  
**Not a syntax release. Not an implementation authorization.**

---

## 0. Executive ruling

The repository's 1 September 2026 split of Frame-QL documentation into four authorities is correct and should be preserved:

```text
frame_ql_language.md
    canonical language meaning
    authored

core_profile.md
    what Core undertakes to realize
    authored contract

platform_profile.md
    what Platform adds beyond Core
    authored contract

frame_ql_build_status.md
    what the shipped build actually realizes
    generated / measured
```

This structure is better than the earlier assumption that one monolithic Manual should carry language meaning, profile obligation, and current implementation status together.

Therefore the vNext work should **not** replace the four-document structure with a new monolithic Manual.

The job is now:

> **Reconcile canonical language meaning first; then reconcile profile taxonomy; then let build status continue to report measured reality.**

The current shipped build remains evidence. It does not determine the new semantic architecture.

---

# 1. Governing authority stack

The jurisdictions should be kept explicit.

```text
Theory of Data v7
    analytical objects and laws
        ↓
Columna Data Types
    semantic value types and capabilities
        ↓
Frame-QL language law
    expressions, requests, standing, frame semantics
        ↓
Frame-QL capability registry
    which language capabilities have canonical standing
        ↓
Core / Platform profiles
    which canonical capabilities an implementation undertakes
        ↓
build status
    what one released build actually realizes
```

No lower layer may redefine an upper one.

In particular:

- the fact that the current build executes an operation does not make that operation a ToD measure family;
- the fact that a profile undertakes an operation does not ratify its language semantics;
- the fact that the parser accepts a syntax does not make that syntax canonical language law;
- the fact that a Theory distinction exists does not automatically make its surface syntax part of Frame-QL.

---

# 2. Current-state discovery

The current repository has already solved an important documentation problem that the prior vNext planning note had treated as future work.

The former single Frame-QL book was split on 1 September 2026 because one document could not safely state all three of:

1. what the language means;
2. what an implementation promises to support;
3. what the current build happens to run.

The split should be treated as an architectural gain, not as an incidental documentation refactor.

The current build status reports:

```text
columna        0.19.0
columna-core   0.19.0
columna-server 0.12.0
wire           contract_version "4"
```

The current language law is still reconciled to ToD v6.1 and retains substantial pre-vNext semantics, especially around family-member dot forms, bracket filtering, ordered reducers, and absence/fill behavior.

---

# 3. The semantic surface to reconcile

The vNext semantic expression model distinguishes these language-level sorts:

```text
family reference
measure expression
general anchorable expression
tuple expression
family-forming analytical expression
ordered analytical expression
predicate / standing expression
frame expression
```

These are **language sorts**, not new ToD ontological kinds.

The key rule is:

> Frame-QL may have many expression forms without making each form a measure family.

Only an admitted ToD analytical law or a governed Manifold declaration can establish durable measure-family identity.

---

# 4. R0 — Anchoring: mostly aligned

## Current language

The current language already distinguishes:

```text
E @ {A}
    expression-local/input-position anchor ascription

AT {A}
    the one final output anchor of the frame
```

It also correctly notes that the current ToD measure has one current anchor even though a reduction may be two-anchor in its derivation.

## vNext standing

The semantic core is:

```text
E @ A
    analytical anchoring / location

AT A
    frame output-anchor declaration
```

## Reconciliation ruling

**Retain the shipped `@` / `AT` surface.**

Revise the conceptual explanation so that:

- `@` is the general analytical anchoring operation at expression level;
- `AT` is the frame-level spelling of the unique final output anchoring;
- inner constitutive anchors of family-forming laws remain identity-bearing where the law makes them so;
- the final anchor remains the current analytical location.

No parser change follows merely from this conceptual rewrite.

---

# 5. R1 — Dot syntax

## Current language

The current Manual uses dotted forms such as:

```text
revenue.sum
level.last
category.touch
```

and broadly describes them as member access / family-member syntax.

## vNext semantic ruling

Dot has two surviving semantic jurisdictions:

```text
governed qualified / faced name
typed semantic-value member access
```

Examples:

```text
category.touch
E.attr
E.method(...)
```

Historical family/member forms such as:

```text
revenue.sum
level.last
```

must not remain the conceptual model of family formation or ordered analytics.

## Reconciliation ruling

### Canonical language

Teach:

```text
sum(revenue @ I)
mean(revenue @ I)
max(x @ I)
```

as family-forming analytical laws.

Teach ordered operations separately.

### Compatibility

Existing dotted family/member forms may remain **compatibility syntax** where their normalized meaning is unique and governed.

They must not define the canonical semantic grammar.

### Important normalization rule

Do not normalize a dotted compatibility form by string rewrite alone.

For example:

```text
revenue.sum
```

can normalize to the explicit family-law form only after the governed input-anchor reading has been resolved.

Likewise:

```text
level.last
```

cannot be normalized as though `last` were a ToD family law. It must normalize through the ordered-expression compatibility rule once that rule is settled.

### No backend-property authority

A dot is never licensed because a Python object, SQL type, or backend carrier happens to expose a property of that name.

---

# 6. R2 — Brackets

## Current language

The current language reserves a roadmap form:

```text
revenue[region = "east"]
```

for expression-local analytical filtering.

It is not shipped.

## vNext semantic ruling

```text
E[key]
E[i]
```

is reserved for **semantic-value subscription** where the CDT type supplies subscription.

Analytical restriction belongs to explicit analytical predicate/request semantics.

## Reconciliation ruling

**Retire roadmap analytical bracket filtering now.**

This is the cheapest possible migration point because the form is unshipped.

The canonical language should no longer teach or reserve:

```text
E[predicate]
```

as analytical restriction.

`[]` is reserved for value subscription.

No CDT type need support subscription immediately. Reserving the semantic role does not imply that the current Core profile must execute any subscription form.

If expression-local analytical restriction is later admitted, it must receive syntax that cannot be confused with internal value subscription.

---

# 7. R3 — Ordered analytics: the hard compatibility seam

## Current language

The current language currently has two overlapping arrangements:

1. `first` and `last` are ratified **reducers**, and Core undertakes and the current build executes them.
2. scans such as `lag`, `lead`, `cumsum`, and rolling operations are treated as order-dependent operations; several are implemented even while their language standing remains proposed.

The current Manual permits order to be:

- derived from a naturally ordered axis in the input anchor; or
- named explicitly.

## ToD v7 / vNext ruling

FIRST, LAST, LAG, LEAD, cumulative operations, rolling windows, RANK, top-N, and similar operations are **ordered analytical expressions**, not measure families merely because they return values.

The required semantic contract includes enough of:

```text
operand
peer / partition domain
order key(s)
direction
tie semantics
window / frame
step / offset
```

Query-level `ORDER BY` orders the returned frame only.

It does not silently supply an inner ordered-expression contract.

## Required reclassification

The language taxonomy should become:

```text
family-forming analytical laws
    sum
    count
    min
    max
    mean
    variance
    ...

ordered analytical expressions
    first
    last
    lag
    lead
    cumulative
    rolling
    rank
    ...
```

`max(x @ I)` remains a possible family law because its result is permutation-invariant over the participating analytical points and uses value ordering.

`last(x @ I; order=...)` depends on an ask-selected order over analytical points and is not a ToD family law.

## Compatibility gate O1

The current shipped surface and vNext semantics cannot simply be declared equivalent.

The key question is:

> **May a legacy form such as `level.last` omit the order contract if a single governed order is available, provided canonicalization makes the completed order contract explicit?**

Two possible policies exist.

### O1-A — strict canonical explicitness

Canonical vNext expressions must state the full meaning-bearing order contract.

Legacy `level.last` remains compatibility syntax only and is accepted where it can be expanded mechanically to a unique explicit ordered expression.

The canonical form always shows the completed contract.

### O1-B — governed default completion

The Manifold may declare a single-valued governed default order for a specific ordered operation/domain. Omitted order is then mechanically completed, analogous to a governed single-valued default completion.

Again, canonical form must show the completed order.

This option must not become "time dimension implies chronological LAST."

The default would itself be governed data.

## Recommended direction

Prefer **O1-A as canonical semantics**, while permitting a narrow compatibility completion mechanism for existing shipped syntax.

This preserves the vNext rule that order is part of meaning while avoiding an unnecessary immediate parser break.

A compatibility completion must satisfy all of:

```text
one unique governed order reading
explicit direction
governed tie behavior or uniqueness
canonical form exposes the completion
no use of query-level ORDER BY as ambient order
no backend / physical row-order inference
```

If any item is missing, the expression clarifies or refuses rather than guessing.

## Consequence for capability taxonomy

`first` and `last` should eventually move out of the `reducers` capability category and into an `ordered expressions` category.

The profile may still undertake them.

The build may still execute them.

The category change is semantic, not a claim that current code stopped working.

Do not edit the generated build-status table by hand.

---

# 8. R4 — Point existence, eligibility, support, and value

## Current language

The current language has a strong universe/basis model, but its fill-rule discussion currently lets one compatibility mechanism carry several different meanings:

```text
zero
unknown
undefined
```

This is useful operationally but crosses semantic jurisdictions.

## vNext semantic ruling

For candidate analytical point `a`, the standing order is:

```text
universe existence law
    ↓
point-existence standing
    ↓
anchor point
    ↓
measure eligibility
    ↓
measure support
    ↓
semantic value
```

A missing physical record does not tell us which layer failed.

In particular:

```text
point does not exist
≠
point exists but E is ineligible
≠
point exists, E is eligible, support is unavailable
≠
point exists, E is supported, value is zero
```

## Reconciliation ruling

The language must make standing distinct from semantic value.

Conceptually:

```text
exists(a)
existence_supported(a)

eligible(E)
supported(E)
missing(E)
```

with:

```text
missing(E)
    := eligible(E) AND NOT supported(E)
```

at an established point.

Exact spellings remain a grammar decision.

## Fill-rule compatibility

The existing fill rule should be treated as a **compatibility realization/completion policy**, not as the ontology of point or measure standing.

A future reconciliation should identify which current fill cases correspond to:

- lawful zero completion;
- unsupported standing;
- ineligibility;
- carrier representation.

Do not preserve one enum merely by renaming it if it continues to conflate those cases.

## `is_missing`

`is_missing` is not an ordinary function over `T | Null`.

It is a standing predicate.

## `is_null`

Do not ratify `is_null` as a canonical analytical semantic predicate.

If a profile exposes carrier-null inspection, that is explicitly a carrier/profile concern.

## `coalesce`

Generic SQL-style:

```text
coalesce(E, 0)
```

must not manufacture analytical support.

Turning unsupported standing into a supported value is a governed completion act and requires an explicit completion law.

Because `is_missing`, `is_null`, and `coalesce` are currently proposed rather than ratified, this semantic correction should happen before they acquire shipped-language inertia.

---

# 9. R5 — Manifold promotion

## Current query language

The current language already has the correct negative boundaries:

```text
AS name
    output-column alias

WITH name = expression
    textual/query macro
```

Neither should mint durable analytical identity.

## vNext ruling

A durable object is established by a governed Manifold declaration, not by query syntax.

A promoted derived measure family must satisfy the ToD family contract, including the identity-bearing law and constitutive lineage.

A promoted derived dimension must establish lawful anchor geometry.

An ordered expression may be governably named for reuse without becoming a ToD measure family.

## Reconciliation ruling

Add an explicit **promotion boundary** to the language law:

```text
query expression
    ≠
governed family declaration

AS alias
    ≠
promotion

WITH macro
    ≠
promotion
```

Manifold authoring is a neighboring authority.

The Frame-QL query language may reference promoted objects after they exist; it does not create them by being queried.

A later authoring specification may distinguish:

```text
derived measure family
derived dimension / structural object
named governed non-family expression
```

Do not overload "derived measure" to include ordered expressions that lack family standing.

---

# 10. Capability-registry consequences

The canonical capability registry should eventually express semantic category, not merely callable spelling.

At minimum it will need to distinguish:

```text
family-forming laws
pointwise/value operations
standing predicates
ordered expressions
frame operations
```

This matters because a flat function registry can otherwise make these two look equivalent:

```text
max(...)
last(...)
```

when they have different analytical standing.

## Immediate registry-safe edits

The following can be changed before implementation work:

- retire analytical bracket-filter roadmap standing;
- move `is_missing` from generic map semantics to standing-predicate semantics;
- keep `is_null` non-canonical unless a carrier profile explicitly needs it;
- constrain `coalesce` to governed-completion semantics;
- represent scans as ordered-expression capabilities rather than generic map/reducer operations.

## Deferred registry edit

Do **not** move `first` / `last` out of the current reducer table until compatibility gate O1 is ruled and the profile/build-table generators have a migration plan.

The desired target is clear; the migration mechanics are not yet authorized.

---

# 11. Core Profile consequences

The Core Profile is an authored realization promise.

It should answer:

> Which canonical Frame-QL capabilities must a conforming Core implementation realize?

It should not encode the ontology.

After language reconciliation, Core can continue to undertake:

- order-independent family-forming laws;
- pointwise maps;
- predicates;
- an explicit set of ordered expressions.

The likely target shape is:

```text
Family-forming laws
Pointwise expressions
Standing predicates
Ordered expressions
Frame operations
```

The current promise to execute `first`, `last`, `lag`, `lead`, `cumsum`, etc. need not disappear merely because their semantic category changes.

Category and availability are separate.

---

# 12. Platform Profile consequences

Current Platform additions are correctly stated as:

```text
none
```

Do not invent a Platform-only Frame-QL dialect merely because Platform has a different runtime mission.

Platform should extend Core's Frame-QL capability set only when a language capability genuinely requires or exploits Platform realization.

Distributed identity, custody, cross-domain composition, or certificate transport do not automatically imply new query syntax.

The permanent rule remains:

> Two physical runtimes are acceptable. Two meanings of a measure are not.

---

# 13. Build Status consequences

`frame_ql_build_status.md` remains measured.

Do not hand-edit it to make the build appear conceptually current.

After language/profile changes, the measured table may legitimately show:

```text
conforms
lag
exceed
```

That visibility is a feature.

In particular, if current 0.19.0 executes a legacy form whose canonical standing has changed, build status should report what it does without granting that behavior new semantic authority.

---

# 14. What can be reconciled immediately without implementation authorization

The following are language/document authority work:

1. Adopt the expression-sort model.
2. Rewrite the conceptual `@` / `AT` explanation without changing syntax.
3. Stop teaching dotted family/member syntax as the conceptual grammar.
4. Retire roadmap bracket filtering.
5. Reserve `[]` for value subscription.
6. State the family-forming versus ordered-expression boundary.
7. State that query-level `ORDER BY` never supplies an inner order contract.
8. Reclassify missing/support semantics.
9. Prevent `is_null` and generic `coalesce` from acquiring incorrect canonical semantics.
10. State the Manifold promotion boundary.
11. Rewrite the capability taxonomy conceptually.

These edits do not authorize parser or engine changes.

---

# 15. What requires an explicit compatibility ruling before implementation work

## Gate O1 — ordered-expression compatibility

Settle exactly how existing forms such as:

```text
level.last
first(...)
last(...)
```

complete or expose their order contract.

Do not let implementation invent this answer.

## Gate D1 — dotted family compatibility

Settle which historical dotted family forms remain accepted and how they canonicalize after anchor resolution.

The principle is already fixed: compatibility only, not conceptual grammar.

## Gate S1 — standing/fill migration

Map the current fill-rule/runtime states to the vNext standing layers without pretending one old field already expresses the new semantics.

This may become an authoring-schema and wire migration question.

---

# 16. Recommended work sequence

```text
A. Canonical language-law rewrite
   - expression sorts
   - anchoring
   - family laws
   - value access
   - standing
   - ordered expressions
   - promotion boundary

B. Compatibility rulings
   - O1 ordered expressions
   - D1 dotted family syntax
   - S1 standing/fill migration

C. Capability-registry taxonomy
   - update canonical categories
   - no availability claims

D. Profile reconciliation
   - Core obligations mapped to canonical categories
   - Platform remains additive, currently none unless evidence changes

E. Implementation alignment
   - only after explicit authorization
   - build status remains measured

F. Introduction / Primer reconciliation
   - teach the stable semantic model after language law is settled
```

---

# 17. Proposed canonical language-manual structure

The existing four-authority architecture remains.

Within `frame_ql_language.md`, the content should move toward:

```text
Preface — the frame is the query

1. Authority and jurisdictions
2. Query and frame model
3. Expression sorts
4. Families, measures, and anchoring
5. Pointwise and tuple expressions
6. Family-forming analytical laws
7. Semantic values: attributes, methods, subscription
8. Standing predicates: existence, eligibility, support
9. Ordered analytical expressions
10. Frame clauses and frame selection
11. Manifold promotion boundary
12. Types and capabilities
13. Validity, adjudication, and realization
14. Canonicalization and compatibility syntax

Appendix A — capability reference
Appendix B — reserved syntax
Appendix C — SQL-speaker contrasts
Appendix D — historical / compatibility forms
```

The current useful clause-level material should be migrated, not discarded.

---

# 18. Stop-gate

No parser, planner, engine, capability-registry, profile, or wire change is authorized by this document.

The next architectural question is **not** "how should CC implement vNext?"

It is:

> **Do we accept the ordered-expression compatibility policy O1-A — canonical explicit order, with legacy syntax allowed only as mechanically completed compatibility syntax whose canonical form exposes the full governed order contract?**

If yes, the remaining Manual rewrite becomes substantially more mechanical.
