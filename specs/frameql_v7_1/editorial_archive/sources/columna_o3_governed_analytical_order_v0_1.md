# O3 — Governed Analytical Order
## Declaration, comparison, identity, and realization

**Working architecture proposal 0.1 — 6 September 2026**  
**Program:** Theory of Data v7.1 / Frame-QL vNext / Columna  
**Basis:** the agreed two-level order construction in the ToD v7.1 amendment 0.2 and its O2 reconciliation.  
**Status:** design for review. No repository, syntax, publication, or implementation change is authorized by this document.

> **The Manifold governs the order of analytical points. Columna Data Types supplies the value semantics used to realize that order. An ordered family selects that governed order as part of its law. Execution preserves it.**

# 0. What this proposal does

The agreed construction has two levels: complete point order within each constituent anchor dimension, and comparison precedence among those dimensions. Their lexicographic composition determines the order of points of the support anchor. FIRST and LAST consume that ordered analytical space after the operand has been established at its constitutive anchor. They do not select arbitrary carrier records. [S1, §§3–11]

O3 proposes where those facts belong, how they are referenced, what the type layer must supply, and what an implementation must establish before using them. It does not introduce another definition of analytical order or a generic tie-selection mechanism.

The source-derived commitments and the new proposals are deliberately separate:

| Standing | Content |
|---|---|
| Inherited from the current working amendment | Complete constituent point orders; explicit dimension precedence; analytical order distinct from enumeration; FIRST/LAST family standing conditional on the family contract. |
| Inherited from the architectural handoff | Logical-only authored Manifold; separate private realization; publication, certification, and serving admission are different authorities. |
| Proposed here | Reusable logical order declarations; typed realization obligations; explicit family/order binding; order-relative state compatibility; a resolved order contract shared by explanation and execution. |
| Not decided here | Concrete Manifold schema, CDT capability names, query syntax, wire shape, operator-kind migration, or the full standing representation. |

The engineering baseline in the inspector reports is `bfb3cfe`. Statements about that implementation below are attributed to those reports, not presented as a new inspection of current `main`. The separate CDT v0.5 specification was not retrieved in this pass; the CDT section states requirements, not a claim that its existing API already satisfies them. [S3–S6]

# 1. The anchor remains a partition

Let the governed constituent anchor dimensions be

\[
A_1,\ldots,A_n.
\]

Let their common refinement be the constitutive support anchor \(S\). A point \(s\in S\) has a projection \(q_i(s)\in A_i\) for every constituent dimension. These projections jointly identify the point:

\[
\bigl(\forall i,\ q_i(s)=q_i(t)\bigr)\Longrightarrow s=t.
\]

**Precision correction to amendment 0.2, §3.** Its schematic product notation and the word “independent” must not imply that every Cartesian combination exists, that the dimensions are statistically independent, or that an anchor has a uniquely discoverable factorization. The earlier ToD partition account defines a compound anchor through nonempty intersections over its governed universe. That account is preserved here. [S7, §2.7]

Thus the point coordinates embed \(S\) into a product:

\[
q:S\hookrightarrow\prod_i A_i,
\]

but the image need not be the entire product. An order on the coordinate product restricts to the analytical points that actually exist. Ordering never generates missing combinations.

The declaration identifies the constituent structure it uses. It does not ask an engine to discover “independent dimensions” from currently observed rows. Redundant coordinate spellings can be normalized only through established partition equivalence. No general factorization algorithm is required for O3.

In this document, **support anchor** retains the amendment's meaning of *constitutive input anchor*. It must not be confused with the subset of points whose operand values currently have evidence support.

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

A differing component exists because the coordinates jointly identify the point. The component comparison determines one direction. Transitivity follows from the first-differing-component rule and the transitivity of the constituent orders. This is the standard lexicographic construction; the external reference [E1] corroborates the mathematical construction only and supplies no Columna governance authority.

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

A family construction selects the governed support order:

\[
G=\operatorname{LAST}_{\mathcal O_S}(F@S).
\]

Its defining contract still includes its operand, participation law, sufficient-state basis, admitted movements, and finalization. A complete support order does not by itself establish the operand or admit every coarser target.

The support order can be reused by FIRST, LAST, or another admitted law. It is therefore more appropriately declared with the analytical geometry than buried inside a physical `last` implementation.

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

The inspector report identified why this interface matters: the inspected build's `ORDERED` set classifies accepted measure dtypes, while coordinate levels have no dtype and no declared comparison operation. That is evidence of the gap, not a template for the successor. [S3, §§F.0–F.1]

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

# 8. The finite sufficient-state law, fully stated

This section makes the complete, finite FIRST/LAST fragment explicit. It is not a full missingness calculus.

Fix one family definition, one governed order, one eligible participation domain \(D\subseteq S\), and one coherent operand evidence instance. Assume every participating point in this fragment has an established value \(f(s)\). For a target point \(a\), the contributing set is

\[
D(a)=D\cap\pi_{S\to A}^{-1}(a).
\]

For the initial finite fragment, every nonempty \(D(a)\) has a unique extremum under the total support order. A total order on an infinite unbounded fiber would not alone guarantee an extremum; such cases are outside this proved fragment, not an invitation to weaken the complete-order requirement.

Define the witness state space

\[
W=\{\bot\}\cup\{(s,f(s)):s\in D\}.
\]

Here \(\bot\) means an empty **contribution state**. It does not mean unsupported existence, an unknown value, zero, or a semantic Null.

For LAST, \(\oplus\) retains the later support-point witness. Define the previously unstated cases as well:

\[
\bot\oplus w=w\oplus\bot=w,
\qquad
w\oplus w=w.
\]

For two distinct support-point witnesses, use their governed support-point comparison. FIRST uses the earlier witness.

Because one coherent operand instance assigns one value to each participating point, two valid witnesses for the same point agree. Conflicting values attributed to the same point and evidence context are not a tie for LAST to resolve; they fail the premise that the input measure is established. Mixing snapshots or differently constituted orders likewise fails state compatibility. Idempotence is not blanket permission to duplicate source contributions in other laws.

Under these premises, \((W,\oplus,\bot)\) is a commutative monoid: an identity exists, swapping operands does not change their extremum, and grouping three operands does not change their common extremum.

For every target point,

\[
w_A(a)=\bigoplus_{s\in D(a)}(s,f(s)).
\]

Partitioning the same set of contributions through \(B\) gives

\[
w_A(a)=
\bigoplus_{b\subseteq a}
\left(\bigoplus_{s\in D\cap\pi_{S\to B}^{-1}(b)}(s,f(s))\right).
\]

Thus direct and staged results agree, provided they retain compatible witnesses, use the same participation rule and evidence, and follow admitted projections. No requirement that the intermediate groups be consecutive has entered the proof.

This proof concerns continuation after the constitutive operand has been established. It does not prove a universal prohibition on all contextually formed families. The broader “projection-fiber locality” claim in the previous stress test should not be expanded into a new general admission theorem merely through O3.

# 9. Declaration completeness is not current evidence completeness

A complete order law can exist while the system lacks the evidence needed to position a particular point under it. The order has not become partial. Its current realization is unsupported for that request.

The request must distinguish the following questions:

| Question | Possible failure |
|---|---|
| Which points exist in the governed domain? | Point existence or population completeness is unsupported. |
| Which support point does the evidence belong to? | Required analytical placement is unsupported. |
| How are established support points compared? | The declared order is incomplete, or a required comparison representation is unavailable. |
| Does the operand apply at the selected point? | Eligibility is unresolved or the measure is ineligible. |
| What is its value there? | The selected eligible value lacks support. |

O3 does not turn these into one `is_null` check or mandate new runtime enums.

In particular, if the latest eligible analytical point exists but its operand value is unavailable, FIRST/LAST must not silently retreat to a different supported point. “LAST over the eligible points” and “LAST over supported observations” use different participation rules. They can be separately governed, but one cannot quietly replace the other.

Likewise, a known point with unresolved Day placement must not be assigned “nulls first” and consumed by a cumulative computation. Dropping it and serving the surviving sequence as the full answer is not a repair either. A separately defined restricted result can sometimes be served with truthful conditions, but a disclosure does not make an undefined ordering determinate.

Not every support defect invalidates every result. A total that does not require Day placement may remain established. Establishing a winner may also require less operand evidence than reconstructing every nonwinning value. Any such optimization needs a specific justification; missing comparison information cannot simply be ignored.

These distinctions refine the containment boundary but do not implement full R4. The inspector report's examples show both selected-value skipping and ordered contributions surviving after final-frame withholding. They remain implementation findings awaiting a bounded disposition. [S4, §§1–3]

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

The successor should remove dependence on the spelling of a lineage name. A label change from `calendar` to another label must not remove chronology when the governed references and definition remain the same. The inspected build's name-based source of order is a reported compatibility gap, not a normative rule to extend. [S3, §F.3]

# 11. One resolved semantic contract, not an explanation-only overlay

A resolved ordered-family request needs to identify its selected family law, operand, support anchor, support-order definition, target anchor, admitted projection, participation rule, and the status of required realization evidence.

That does not mean every field must appear in a canonical query string. Surface round-tripping and resolved meaning are different concerns. The current reconstruction report identifies an additive EXPLAIN location, while also observing that merely placing data there would not make execution consume it. [S5, §§2–4]

The proposed invariant is:

> **Explanation and execution refer to the same resolved semantic order contract. EXPLAIN must not describe an order that the engine later reconstructs independently.**

The planner-facing contract contains logical meaning and established obligations. Engine mechanics remain behind the existing execution boundary. A resolved reference can be shared without copying physical sort implementations into analytical planning.

Preflight can state which order is selected and which obligations are statically established. It cannot claim to have verified current data conditions it has not examined. If a missing order declaration or missing required type capability is already known at planning time, an execution failure must not be postponed and presented as a successful preflight.

No concrete field name or wire-version decision is made here.

# 12. State identity and reuse

A retained extremum witness is interpretable only under the support order and family law that selected it. Safe reuse therefore needs a reference to that semantic context as well as enough point information to compare the winner later.

The exact representation may be a structured analytical point reference, a governed order-preserving encoding, or an equivalent certified representation. O3 does not require storing a complete coordinate tuple in every physical state. It requires that compression preserve the relevant comparison and identity.

A materialization must not compare states from different precedence rules merely because both expose the same scalar dtype. Nor may it silently compare witnesses from incompatible order-definition versions or evidence contexts.

A carrier containing only the displayed FIRST/LAST value generally lacks the selected point witness. A valid recovery rule might reconstruct it in a special case, but recoverability has to be established. The default is not to infer the winner from its value.

This carries forward the existing distinction between analytical identity, sufficient state, and materialized availability; it does not revive an independent information-quotient ontology. [S1, §§14–18; S7, §7.10]

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

# 15. Finite mathematical checks

A local reference calculation tested the formal construction. It did not run Columna, DuckDB, Polars, or any repository tests and made no repository changes.

The model used a two-point dimension and a three-point dimension, both precedence choices, and both orientations of each component order: eight complete orders. It considered every subset of the six-point coordinate product, both FIRST and LAST, every enumeration of each subset, and every nested set partition for staged reduction. Intermediate blocks were not constrained to be contiguous.

| Check | Instances checked | Result |
|---|---:|---|
| Trichotomy of the induced order | 288 | All passed |
| Transitivity of the induced order | 1,728 | All passed |
| Witness-merge commutativity | 784 | All passed |
| Witness-merge associativity | 5,488 | All passed |
| Empty-state identity and witness idempotence | 112 | All passed |
| FIRST/LAST × order × support-subset cases | 1,024 | All passed |
| Enumeration permutations | 31,312 | All passed |
| Direct/staged target-fiber comparisons | 215,856 | All passed |

These checks support the finite construction and guard the examples. The proof in §8, not a finite test count, establishes the stated general finite-fiber result. The checks do not validate source completeness, comparison realizations, any current compiler, or the broader family-admission claims in earlier drafts.

# 16. Review decisions and next unit

The proposed O3 boundary is now small enough to review as one unit:

1. Component point orders are logical declarations attached to their governed anchors.
2. Compound support orders select those orders and state dimension precedence.
3. Family definitions select complete support orders as constitutive law.
4. CDT supplies the required equality/comparison semantics; realization must preserve them.
5. Resolved semantics, explanation, and execution share one order contract.

Before incorporating O3 into a full ToD v7.1 text, amend the earlier schematic product language as noted in §1, state the finite/extremum and empty-state premises, and separately review the breadth of the earlier projection-fiber-locality admission claim. None of those editorial obligations changes the agreed two-level order construction.

The next implementation-facing unit should be **a focused contract review**, not another broad reconnaissance and not a request to build all ordered operations. CC already supplied the relevant implementation evidence. The useful return would map this proposal onto the actual CDT specification, identify the smallest logical publication representation, and identify the consumed resolved-contract seam. Concrete syntax and class names remain CC recommendations subject to the semantic boundary above.

The reproduced current defects remain a separate correctness obligation. They need not wait for a full order-authoring UI or a universal standing model: a system can decline to assert an ordered result whose required point formation or order is not established. Conversely, a small containment patch cannot claim O3 implementation merely because it refuses the known bad cases.

No new CC mission has been sent by this document. No changes to `.cml`, operator kinds, profiles, wire contracts, or public compatibility surfaces are authorized.

# 17. Sources and evidence boundaries

**[S1] Working theory input.** `tod_v7_1_ordered_measure_families_amendment_v0_2.md`, 6 September 2026. Especially §§3–11 (constituents, precedence, family construction), §§14–18 (state, coherence, identity), and §§24–25 (admission and revised boundary). This is an agreed working amendment, not asserted here to be a published v7.1 release.

**[S2] Working language input.** `frameql_vnext_o2_reconciliation_to_tod_v7_1_v0_1.md`, 6 September 2026. Especially §§3–4, 12–18. It identifies the eight O3 questions addressed by this proposal.

**[S3] andFam, order representation and strength inspector.** Attached as `Pasted markdown (3)(9).md`; report headings `F. ORDER RELATION REPRESENTATION` and `G. ORDER STRENGTH / TIES`, reported HEAD `bfb3cfe`. Used for the coordinate-type, comparison, lineage-name, and incomplete legacy-order findings. Its v7.0-era categorical family conclusions are not adopted over S1.

**[S4] andFam, participation and standing inspector.** Attached as `Pasted markdown(20260906-221513).md`; heading `H / O2-Q4 — Participation and standing for ordered expressions (post-R4-C0)`, reported HEAD `bfb3cfe`. Used for lost-placement contamination and operand-skipping evidence. Its runtime probes were reported by andFam, not independently rerun here.

**[S5] andFam, resolved artifact and descriptor inspector.** Attached as `Pasted markdown (4)(4).md`, reported HEAD `bfb3cfe`. Especially §§2–4 and §5.3. Used for the surface/resolved distinction and planner/engine authority boundary.

**[S6] Architectural handoff.** `START_HERE(2).md`, 14 August 2026. Used only for persistent authority boundaries: logical authored Manifold, private mapping, publication/certification/admission, and planner/engine roles. Its operational status is historical, not current.

**[S7] Huayin Wang, The Theory of Data, v6.0.** `theory_of_data_v6_0_zenodo_21958062.md`. Used narrowly for the unchanged partition/common-refinement account in §2.7 and materialization distinction in §7.10, not as a replacement for later theoretical revisions.

**[E1] External mathematical cross-check.** Mathlib, `Mathlib.Data.Prod.Lex`, especially `Prod.Lex.instLinearOrder` and the defining lexicographic comparison. Retrieved 6 September 2026. It supports only the ordinary mathematical fact that lexicographic composition of linear orders is a linear order. It is not a ToD or Columna source. Source address: `https://leanprover-community.github.io/mathlib4_docs/Mathlib/Data/Prod/Lex.html`.

The repository's current live status and a definitive CDT v0.5 interface were not established in this pass. This proposal does not attribute proposed fields or capabilities to an implementation that has not been inspected.
