# O3 — Governed Analytical Order
## Declaration, comparison, identity, and realization

**Working Draft 0.2 — 7 September 2026**  
**Status:** Order-interface proposal subordinate to [ToD v7.1 Full Manuscript Draft 0.4](the_theory_of_data_v7_1_full_manuscript_working_draft_v0_4.md) (**T**) and [Language-Law Candidate 0.4](frameql_language_vnext_working_draft_v0_4.md).  
**No schema, syntax, runtime, publication, or implementation authorization.**

# 0. Scope and authority

This revision preserves O3's two-level order construction, sparse partition geometry, logical declaration proposal, and comparison/realization separation. It replaces the older witness-proof and evidence summaries with references to T §§7–10 so that those laws have one source.

The existing order-interface proposal supplies two kinds of logical order fact and one family binding, not necessarily three new classes or registries. The actual CDT v0.5 API has not been inspected in this revision. Requirements below do not imply that a type literally named `Witness` must be added or that no existing structure can implement them.

Historical inspector statements concern the recorded `bfb3cfe` baseline and are not a fresh repository audit. This revision does not repeat or close their runtime probes. The [active-source index](frameql_v7_1_authority_and_supersession_index_v0_1.md) distinguishes current semantic guidance, historical implementation evidence, and superseded recommendations.

# 1. The anchor remains a partition

Let the governed constituent anchor dimensions be

\[
A_1,\ldots,A_n.
\]

Let their common refinement be the constitutive support anchor \(S\). A point \(s\in S\) has a projection \(q_i(s)\in A_i\) for every constituent dimension. These projections jointly identify the point:

\[
\bigl(\forall i,\ q_i(s)=q_i(t)\bigr)\Longrightarrow s=t.
\]

**Sparse compound geometry (T §2.1.3).** Constituent coordinates must not imply that every Cartesian combination exists, that the dimensions are statistically independent, or that an anchor has a uniquely discoverable factorization. A compound anchor is the common refinement through nonempty intersections over the governed universe.

Thus the point coordinates embed \(S\) into a product:

\[
q:S\hookrightarrow\prod_i A_i,
\]

but the image need not be the entire product. An order on the coordinate product restricts to the analytical points that actually exist. Ordering never generates missing combinations.

The declaration identifies the constituent structure it uses. It does not ask an engine to discover “independent dimensions” from currently observed rows. Redundant coordinate spellings can be normalized only through established partition equivalence. No general factorization algorithm is required for O3.

In this document, **support anchor** means the *constitutive input anchor* of T §§7–8. It is not another anchor kind and must not be confused with the subset of points whose operand values currently have evidence support.

# 2. The two levels of order

For each constituent dimension \(A_i\), governance supplies a complete point order \(<_i\). Here “complete order” means a total order over the declared analytical point domain: distinct points are comparable, and the comparison is transitive and consistent with point identity. It does not mean an order-theoretic completeness property such as the existence of a supremum for every subset.

Governance also supplies a precedence permutation

\[
\sigma=(\sigma(1),\ldots,\sigma(n)).
\]

The first entry has the highest comparison priority. Every constituent appears exactly once in this initial construction. Precedence is part of the declared order, not a property of the order in which a query lists its output coordinates.

For distinct \(s,t\in S\), let \(k\) be the first position for which

\[
q_{\sigma(k)}(s)\ne q_{\sigma(k)}(t).
\]

Then

\[
s<_S t
\quad\Longleftrightarrow\quad
q_{\sigma(k)}(s)<_{\sigma(k)}q_{\sigma(k)}(t).
\]

A differing component exists because the coordinates jointly identify the point. The component comparison determines one direction. Transitivity follows from the first-differing-component rule and the transitivity of the constituent orders. This is the lexicographic construction admitted by T §7.1. The mathematical order argument and the institutional authority selecting its definitions remain different questions.

For a one-dimensional support anchor, precedence is trivial. For several dimensions, omitting precedence leaves the analytical order incomplete. Omitting one constituent point order likewise fails to establish this declared complete-order construction. Coincidental equality of current results does not fill either omission.

# 3. The smallest logical declaration model

O3 needs two kinds of order fact and one family binding. These are semantic requirements, not a demand for three new storage classes or registries.

## 3.1 A point-order declaration for a constituent anchor

A logical point-order declaration identifies the anchor whose points it orders, the governing order rule, and the scope in which that rule is authoritative. Point identity and equality come from that anchor's governed structure; display labels do not replace them.

Conceptually, the declaration carries:

| Fact | Meaning |
|---|---|
| Anchor reference | The particular constituent anchor and its governing universe/context. |
| Order definition | A complete ordering rule over that anchor's analytical points. |
| Semantic dependencies | The logical point representation and comparison semantics needed by the rule. |
| Definition reference | A version-resolved reference when the order is named or reused. |

Normal Manifold authority and publication rules apply. There is no order-specific exemption from ratification or evidence requirements.

The order definition can be represented in two initial ways without changing its meaning. A rule-defined order compares a complete logical point representation under declared value semantics, as chronology compares fully identified Day points. An explicitly declared order lists a finite governed domain's point identities in their intended sequence. These are alternative representations of a point order, not two new ontological kinds.

An explicit sequence must cover its declared point domain without duplicate identities. A rule-defined order need not enumerate an unbounded domain, but its rule must cover that domain. A newly encountered point is not automatically appended to an explicit list. Either the declared rule already determines its position or the order is not established for that enlarged scope.

## 3.2 An order declaration for the compound support anchor

The support-order declaration binds the constituent structure of \(S\) to the selected point-order definitions and records their precedence.

Its semantic content is:

\[
\mathcal O_S=
\bigl(S,\ (A_i,O_i)_{i=1}^n,\ \sigma,\ \mathrm{lex}\bigr).
\]

Here \(O_i\) is the selected governed point order on \(A_i\), not a backend sort function. The symbol `lex` records the already-agreed composition law; it is not an invitation to add an open-ended catalogue of composition operators in this slice.

Precedence belongs to this support-order declaration. It is not a universal rule that Customer always outranks Day throughout the Manifold. Another declared support order can use the same constituent orders in another precedence.

Orders may be inline in governed definitions or named for reuse. The requirement is complete, version-resolved meaning, not a new naming ceremony for every order. A standalone order registry is not required by this proposal.

## 3.3 The ordered family's binding

A family construction selects a fully resolved governed support order and its constitutive operand. The full target specification and family contract remain T §4: neither a complete order nor a callable FIRST/LAST spelling supplies the remaining obligations.

For the finite construction in T §8, W is constituted from operand, order, and participation with its own witness-selection and continuation law. Scalar L has an admitted construction by value projection from W. An optional rich retained family R supplies an alternative basis with an exact compatible-union compression to W. These names denote ordinary analytical families, not mandatory public declaration kinds or engine types.

A declaration must identify whether the referenced analytical object is the scalar target, witness-valued family, or another admitted family. It must not grant a scalar materialization the continuation capability of the witness solely because both concern LAST.

The order can be reused by another admitted analytical law. A human-readable name is optional where canonical construction already resolves identity. Institutional publication and ratification remain separate from denotation.

# 4. What CDT supplies, and what it does not

**CDT supplies comparison semantics. The Manifold supplies the analytical use of those semantics.**

For example, a type specification may supply equality and chronological comparison for fully identified calendar dates. The Manifold must still establish which logical values identify its Day points and select that comparison as the Day order. A sortable Customer identifier is not, by that fact alone, the governed Customer order.

Where a constituent point order is realized through values, let

\[
r_i:\operatorname{Pts}(A_i)\to T_i
\]

be the declared logical representation used by its comparator. A sufficient contract is that \(r_i\) is total over the declared point domain, distinguishes its analytical point identities, and uses a total comparator consistent with the type's semantic equality. Then

\[
x<_i y\quad\Longleftrightarrow\quad
\operatorname{compare}_{T_i}(r_i(x),r_i(y))<0.
\]

This realizes an order **on points** through their governed representations. It does not redefine the order as “sort whatever values happen to be in a database column.”

If two different Customer points have the same priority value, that value alone does not realize a complete Customer point order. If two Day points have the same display string because the year was omitted, that display string is not their complete point identity. In neither case should the engine append a row ID, storage address, or lexical identifier as an improvised tie-breaker.

The declaration must already define a complete order. A realization that collapses distinct ordered points fails that declaration.

For the first implementation contract, CDT must be able to express the relevant value domain, equality, comparison law, and any meaning-bearing parameters. Conversion into that representation is a separate obligation: failed conversion is not a new position in the order. The exact capability name and type catalogue remain a CDT reconciliation question.

The earlier O2 inspector report identified a gap at its recorded baseline: the `ORDERED` accept-set concerned measure dtypes while coordinate levels lacked a declared semantic comparator. That observation is historical implementation evidence, not a claim about the uninspected CDT specification or the current build. The successor contract must be established against the actual type specification before conformance is claimed.

# 5. A complete example without new query syntax

The following is a semantic ledger, **not proposed Manifold or Frame-QL grammar**.

```text
Day point order
    anchor: Day
    rule: declared chronology over complete Day identities

Customer point order
    anchor: Customer
    declared domain in this example: C1, C2
    order: C1 before C2

Support order O_customer_day
    anchor: {Customer, Day}
    precedence: Customer, then Day
    component orders: Customer point order; Day point order

Support order O_day_customer
    anchor: {Customer, Day}
    precedence: Day, then Customer
    component orders: Day point order; Customer point order

Two family constructions
    LAST under O_customer_day of F at {Customer, Day}
    LAST under O_day_customer of F at {Customer, Day}
```

Assume the governed support contains exactly these three points and the operand is supported at each:

| Customer | Day | F |
|---|---|---:|
| C1 | d3 | 80 |
| C2 | d1 | 20 |
| C2 | d2 | 40 |

Let \(d1<d2<d3\). Customer-first precedence selects `(C2,d2)` for a global LAST and returns 40. Day-first precedence selects `(C1,d3)` and returns 80. No `(C2,d3)` point is manufactured to complete the coordinate product.

At a target anchor that retains Customer, both constructions happen to return 80 for C1 and 40 for C2. That local agreement does not make the family identities equal: their governed global orders still differ.

Also, a global LAST selecting one Customer-Day value is not the same construction as adding the per-customer LAST values. The latter yields 120 in this example and would need its own lawful composition. O3 must not call every such expression “closing balance” or “closing stock” as though the business identity followed automatically from LAST.

# 6. Multiple orders, defaults, and family identity

Several governed orders can coexist on one anchor without ambiguity in a family definition. The family binds one of them.

A request can name an existing family, explicitly select a governed order where the language permits it, or use a uniquely declared default. It cannot have an engine choose among several orders because one resembles a conventional sort.

The family signature must preserve the operand identity, support-anchor identity, selected support-order definition, and other constitutive law parameters. A separately requested current anchor remains the measure's location; physical sort strategy, partitioning, and row order are not family identity.

Changing precedence or changing a declared point-order rule requires identity succession wherever the analytical meaning changes. Renaming a label while preserving its governed identity and definition does not. Replacing one physical order implementation with an equivalent implementation does not.

Two order descriptions may be treated as equivalent only when their semantic equivalence is established over their governed scope. Equality of winners on today's records is insufficient. O3 does not require a universal equivalence prover or a canonical minimal factorization algorithm.

A rule-defined domain can acquire new points under the same unchanged order rule. That ordinarily changes the evidence population, not the rule definition. By contrast, editing an explicitly declared Customer priority sequence changes the order definition. Reusable state must remain tied to the applicable order and evidence scope in either case.

Live, mutable priority measures raise a further question: whether the order depends on an explicit evaluation context or a frozen declaration. **The initial O3 contract does not silently admit mutable ranking data as immutable order.** Such a use requires a separately specified context/version binding before materialized winners can be reused safely.

# 7. Hierarchies: projection and order are separate facts

A hierarchy establishes where finer points project. It does not, by itself, establish their point order. Conversely, knowing the order on Day does not make every coarser partition's labels chronologically ordered.

For FIRST/LAST continuation, the required order remains the order on the original support points. Let

\[
S\succeq B\succeq A.
\]

An intermediate state at \(b\in B\) retains the winning \(S\)-point. Continuing to \(A\) compares those retained \(S\)-points under \(\mathcal O_S\). It need not invent an order over the points of \(B\).

This matters even when the intermediate groups are not contiguous under the support order. Suppose

\[
s_1<s_2<s_3<s_4,
\]

with intermediate groups `{s1,s4}` and `{s2,s3}`. Their LAST witnesses are `s4` and `s3`; comparing them under the original order still selects `s4`. Ordering the group labels instead could select the wrong witness.

If a **new** family starts at \(B\), and its law requires an order on \(B\)-points, that order must be established for \(B\). It is not supplied by the mere availability of winning \(S\)-point witnesses from a different family.

An inherited order on coarser blocks may be justified where the partition and the original order support a suitable quotient—for example, noninterleaving ordered blocks with a proved correspondence. This is an optional derived-order law, not a prerequisite for FIRST/LAST witness continuation, and not something O3 assumes for every hierarchy.

The same distinction prevents coordinate normalization from silently changing precedence. Adding a redundant `Month` display coordinate to `{Customer,Day}` must not cause an engine to invent a new order or a monthly reset.

# 8. The family proof remains in the theory

T §§8.1–8.6 is the sole mathematical account used here. Its propositions define coherent-instance witness composition and show that extracting an extremum witness from compatible finite point–value sets preserves the admitted union/combine operation. No parallel witness theorem is introduced in this interface note.

The complete finite-input fragment fixes coherent operand instance f, order, and contribution domain. Known-empty contribution supplies the identity; an unsupported contribution is not that identity. Two conflicting values for one analytical point do not satisfy the coherent-instance premise.

A representation must preserve original point identity, declared order comparison, the associated operand value where required, and the distinction between known-empty and unavailable state. It may use a typed record, coordinate tuple, governed point reference, or a faithful encoding. A nominal built-in type called `Witness` is not required.

R is an optional sufficient basis, not a prerequisite to serving W or L. A direct implementation can establish W without retaining the full pair set if its evidence establishes the winning-point claim. An adequately justified scalar may be available without an identified winner. These possibilities are not a mandatory `R → W → L` runtime pipeline.

The family law is uniform across coherent instances; the instance-relative carrier does not create a new family identity for each snapshot. Whether two materializations are compatible instances for a proposed use is an evidence/reuse question, not a fact certified by a local winner comparison.

# 9. Declaration completeness is not current evidence completeness

A complete declared order does not prove that a current materialization can place every required point or recover its comparison representation. Conversely, loss of an irrelevant operand value need not make a target unavailable. Evidence obligations depend on the requested law.

The following distinctions from T §9 must remain visible in a resolved order contract and its supporting evidence:

- A known domain `s1 < s2 < s3` with supported maximal value 30 can establish the coarser witness `(s3,30)` even when a finer intermediate witness at s1 cannot be obtained. Do not replace that unavailable intermediate by empty state.
- A fixed LAST law can establish scalar 7 without identifying the winner only under an adequate argument; T §9.6's example requires known nonemptiness, exhaustive possible-participant coverage, and supported equal values at every possible winner. Equal values among observed rows alone are insufficient.
- Missing selected value, unknown possible later participation, incomplete point placement, and incomplete declared order are different failures. “Last supported value” cannot replace “last participating point's value” silently.

No order-specific standing enum is introduced here. The needed claim, its dependencies, and the evidence supporting it must be distinguished however the concrete implementation represents them.

A false number is not made lawful by adding disclosure later. A late frame filter does not repair an earlier ordered walk that consumed an unplaceable contribution. Exact outcome policy and current containment remain separately authorized engineering work.

# 10. Authored meaning, admission, and execution

The order declaration belongs in the logical Manifold. It identifies analytical anchors, point identities, order rules, and semantic comparison dependencies. It does not contain physical table/column paths, database collation defaults, Polars sort flags, or an engine-specific expression.

The private mapping realizes those facts. A compiler may lower a declared chronological comparison to a suitable engine operation, but it may not decide that an unknown coordinate should sort first, or that an identifier should supply undeclared precedence.

The existing lifecycle separation applies:

```text
logical order declaration
    -> authorized versioned publication
    -> realization against private mapping
    -> evidence / certification of relevant obligations
    -> admitted ordered capability
    -> execution of the resolved contract
```

These stages need not become separate services. They are distinct sources of authority. Logical totality, adequate type semantics, mapping fidelity, and current data completeness are different claims. Some can be established by construction; others depend on a current attestation. [S6]

A fresh scan that happens to contain no collisions does not prove that a declared comparator distinguishes every point in a larger intended domain. Conversely, a definition that establishes totality mathematically does not prove the current source retained every point or value.

The successor should remove dependence on the spelling of a lineage name. A label change from `calendar` to another label must not remove chronology when the governed references and definition remain the same. The inspected build's name-based source of order is a reported compatibility gap, not a normative rule to extend. [historical source S3 in archived O3 v0.1]

# 11. One resolved semantic contract, not an explanation-only overlay

A resolved ordered-family request needs to identify its selected family law, operand, support anchor, support-order definition, target anchor, admitted projection, participation rule, and the status of required realization evidence.

That does not mean every field must appear in a canonical query string. Surface round-tripping and resolved meaning are different concerns. The current reconstruction report identifies an additive EXPLAIN location, while also observing that merely placing data there would not make execution consume it. [historical source S5 in archived O3 v0.1]

The proposed invariant is:

> **Explanation and execution refer to the same resolved semantic order contract. EXPLAIN must not describe an order that the engine later reconstructs independently.**

The planner-facing contract contains logical meaning and established obligations. Engine mechanics remain behind the existing execution boundary. A resolved reference can be shared without copying physical sort implementations into analytical planning.

Preflight can state which order is selected and which obligations are statically established. It cannot claim to have verified current data conditions it has not examined. If a missing order declaration or missing required type capability is already known at planning time, an execution failure must not be postponed and presented as a successful preflight.

No concrete field name or wire-version decision is made here.

# 12. State identity and reuse

T §10.7 governs the materialization interface. The retained artifact must distinguish what it holds, which target claim is established and why, and what later use that information justifies.

A retained nonempty W can construct scalar L and supply admitted witness continuation. A retained L after W was discarded and an L established without a winner may share the same scalar family identity and value while carrying different establishment records. Neither implies retained W. A trace recording historical witness use is not present recoverability.

Compatibility must be established before invoking the lossy-composition theorem. With `p < q`, a source claiming `(p,10),(q,20)` can compress to `(q,20)` and conceal conflict with another source's `(p,11)`. Equal-point conflict checks on compressed winners are not a global validator. A matching context identifier must refer to adequate evidence rather than act as assurance by itself.

Reordering the governed constituent definitions or changing their precedence can change family identity. Physical serialization can change without changing that identity if its semantic representation remains faithful. Evidence refresh can change availability without creating another family, but mixing incompatible instances is not authorized by a common family name.

Coarsening sufficiency does not automatically cover deleting the winner, restricting it out, or re-forming a contextual input under different conditions. Each reuse needs the information and compatible premises required by that use. The concrete catalog and certificate schema remain outside this note.

# 13. Scope boundaries

The following boundaries prevent O3 from growing into a second query language.

**No generic tie policy for the foundational family.** Complete component orders and complete precedence define the comparison. Missing definition, conflicting operand evidence, and loss of a comparison representation have their own diagnoses.

**No automatic global order from fiber-local orders.** Day order inside each fixed Customer context does not, by itself, supply Customer order across contexts. A global `{Customer,Day}` support order needs the user's full two-level construction. A deliberately narrower scoped family does not gain cross-context continuation merely because the physical carrier includes both customers.

**No automatic family classification by operator name or execution cell.** An order declaration can support an admitted ordered family. It can also supply order to a general focal expression with further context requirements. O3 establishes the order interface, not a family-admission shortcut.

**No automatic neighborhood semantics.** A complete point order establishes relative position. It does not define what “seven days” means as a distance/window, which peers a rank compares, or whether a missing observation is skipped. Those remain additional laws of the general-expression branch.

**No forced legacy mechanism.** Public `.last` references can be preserved through truthful resolution where the necessary meaning exists. A legacy `ORDER day` declaration is not mechanically upgraded to a complete multidimensional support order. Missing constituent orders or precedence must remain visible.

# 14. Acceptance cases

These are semantic requirements for the proposed interface. They are not claims about current Core behavior.

| Case | Expected determination |
|---|---|
| One-dimensional Day anchor with complete declared chronology | Ordered support is defined; precedence is trivial. |
| Customer and Day orders complete, no declared precedence | No complete compound order has been selected. |
| Precedence complete, Customer point order absent | Compound ordered support is not established. |
| Both orders and precedence complete | Lexicographic point order is determined. |
| Anchor written with coordinates in another display order | Selected support order remains unchanged. |
| Sparse `{Customer,Day}` universe | Only existing analytical points participate; no Cartesian filling. |
| Two Day labels repeat because year is omitted | Display label is insufficient as a complete point representation. |
| Two Customer points share an alleged unique rank | That representation fails the declared complete Customer order. |
| Several carrier records belong to one support point | Establish the operand at that point under its own law before selection. |
| Same support point has conflicting values under one evidence context | Input inconsistency; not a FIRST/LAST tie. |
| Two governed precedence choices produce the same current winner | No automatic equivalence of order/family identity. |
| Complete order definition, required coordinate lost | Definition remains complete; current realization/support is deficient. |
| Latest eligible point known, operand missing | Do not silently return the previous supported value. |
| Lost Day placement, non-ordered total independent of Day | Preserve the independently lawful total. |
| Lost placement consumed by a scan before row withholding | Result fails the ordered-domain obligation; final-row filtering is insufficient. |
| Direct versus staged LAST through arbitrary admitted groups | Same support-point witness under unchanged order and contributions. |
| Intermediate group labels sort differently from their support witnesses | Compare retained support witnesses, not group labels. |
| New family starts at a coarser anchor | Establish that new support anchor's required point order. |
| Mixed order-definition versions in a cache merge | No silent merge; prove compatibility or decline reuse. |
| Physical permutation of identical governed evidence | Same result and same relevant analytical determination. |
| Output `ORDER BY` reverses display | Inner family order and result remain unchanged. |
| EXPLAIN names an order different from execution's | Invalid realization of the resolved request. |
| New point outside an explicitly ordered closed domain | No inferred append position; resolve governed scope/version. |
| A business-priority field changes during execution | No silently mutable relation; bind the required context first. |

# 15. Validation status

The finite mathematical checks reported in O3 v0.1 remain historical results of that earlier proposal. They were not rerun or extended for this document reconciliation and do not verify the present Columna or CDT implementation.

This revision defers mathematical propositions to the unchanged T Draft 0.4. The current acceptance cases are semantic review obligations, not a claim that every case has an implementation or that a document check proves conformance.

# 16. Remaining specification work

The order structure remains settled as a working theory input. The remaining interface review should determine whether the actual CDT specification can supply the required equality, point representation, and comparison semantics; how logical publication carries the selected constituent orders and precedence; and how the same resolved meaning reaches explanation and execution.

This task must not use legacy FIRST/LAST internals as the definition of the target. Nor should it introduce a new authoring kind, registry, or wire field merely because the requirements are listed separately. Recommend the smallest faithful representation after inspecting the relevant interfaces.

No such implementation or schema work is authorized here. The [capability/profile reconciliation plan](frameql_vnext_capability_profile_reconciliation_plan_v0_2.md) states the separate adoption boundaries.

# 17. Sources and evidence boundaries

The fixed theoretical source is [T, Full Manuscript Working Draft 0.4](the_theory_of_data_v7_1_full_manuscript_working_draft_v0_4.md), especially §§2.1.3, 4–10, and 12. The language account is [Language-Law Candidate 0.4](frameql_language_vnext_working_draft_v0_4.md). Both are working documents, not published v7.1 or shipped-language certification.

**[S6] Historical architecture handoff.** `START_HERE(2).md`, 14 August 2026, identified as source S6 in O3 v0.1 §17. Section 10 cites it only for the persistent separation of logical publication, private mapping, certification, serving admission, and planner/engine responsibility. Its operational status is historical, not current.

The full original O3 v0.1 is retained in the editorial archive, including its sources, historical inspector references, and previous validation record. Its opening source hierarchy and duplicated witness/evidence summaries are replaced by this note; unchanged declaration and geometry content is retained where consistent with T.

The [source/supersession index](frameql_v7_1_authority_and_supersession_index_v0_1.md) identifies the active note, historical inputs, and withdrawn recommendations. No source byte, publication, or runtime was changed by this revision.
