---
title: 'The Theory of Data: An Introduction'
subtitle: Analytical Meaning, Lawful Transformation, and Governed Results
author: Huayin Wang
version: '2.3'
date: Version 2.3 — 7 September 2026
license: CC BY 4.0
lang: en-US
subject: A systematic introduction aligned with the published Theory of Data, Version 7.1
doi: 10.5281/zenodo.22651777
papersize: letter
geometry: left=0.85in,right=0.85in,top=0.8in,bottom=0.8in
fontsize: 11pt
keywords:
- Theory of Data
- analytical identity
- datum
- universe
- anchor
- measure family
- family formation
- sufficient state
- analytical order
- coherence
- analytical lineage
- materialization
- governed analytics
---


**datumwise, an independent open-source research project**  
**DOI:** [10.5281/zenodo.22651777](https://doi.org/10.5281/zenodo.22651777)  
**License:** Creative Commons Attribution 4.0 International (CC BY 4.0)  
**Supersedes:** *The Theory of Data: An Introduction*, Version 2.2, DOI [10.5281/zenodo.22018598](https://doi.org/10.5281/zenodo.22018598).  
**Aligned with:** *The Theory of Data*, Version 7.1, DOI [10.5281/zenodo.22649945](https://doi.org/10.5281/zenodo.22649945).

## Abstract

The Theory of Data describes analytical quantities independently of their storage and execution. It asks which analytical points exist, what a quantity means at those points, which transformations preserve its meaning, and what information supports a later calculation. This introduction develops that account through revenue, averages, distinct counts, and closing values. It explains the central reference, a measure family at an anchor, then separates the formation of a quantity from its continuation. It presents sufficient state as a relationship among ordinary measure families, introduces the governed FIRST/LAST construction, and distinguishes a correct answer from retained information adequate for another use. The governing reference is the published Theory of Data v7.1. The examples explain its laws; they do not add new ones or assert implementation coverage.

## About this introduction

This is the systematic companion between [*A Primer on the Theory of Data*](https://doi.org/10.5281/zenodo.22651578) and the foundation itself. It assumes familiarity with reports and basic aggregation, but not with abstract algebra. The important terms are introduced through their work in an example before their fuller consequences are developed.

Throughout, **governed** means that a definition or rule is explicit and has authority for the analytical use. Its mathematical claims and current evidence still need justification. A declaration tells us what is being asserted; it does not prove its own correctness.

References such as `[1, §5]` point to the published v7.1 foundation. The notation here describes analytical objects, not the accepted grammar of a particular query language. [1]

# 1. An analytical request asks for data, not a production procedure

Suppose someone asks for revenue by customer and month. Before writing a calculation, several questions matter: what counts as Revenue, which date assigns a sale to a month, which customer receives it, how returns are treated, and whether a relationship duplicates a contribution.

The person asked for a result. An analyst is often asked to supply all those definitions while also choosing the tables, joins, and aggregation plan. Meaning becomes mixed with the procedure used to produce the answer.

ToD separates them. A customer-month Revenue measure might be derived from transactions, supplied by an aggregate, or obtained from a retained result. Those are possible realizations of the same quantity only when their definitions and evidence support that claim.

The target can therefore be stated before an execution plan is chosen. We will write it as:

\[
Revenue@\{Customer,Month\}.
\]

The left side names the analytical quantity; the right side names where it is being reported. The remaining sections explain what makes that reference well-defined and which calculations are entitled to answer it.

# 2. A datum is a value at an analytical point

Begin with the value `420`. It could be an amount, a count, an identifier, or an error code. A data type alone does not tell us the quantity it represents.

Now state:

```text
Revenue for customer C17 in July 2026 = USD 420
```

Under an identified Revenue definition and customer-period interpretation, this is one analytical assertion. A **datum** is one typed value at one analytical point.

The point is the thing being described: here, the relevant customer-period. A database key can represent it, but physical uniqueness does not establish the business definition, universe, or contribution rule. Conversely, a change of table need not change the analytical point or quantity.

This is the foundation's opening idea: **data is always something about something else**. It starts with the relationship between value and subject, then works backward to establish the subject's analytical location. [1, §§1, 2.2]

# 3. A universe tells us which points exist

A report containing `{Store, Day}` coordinates can describe different analytical worlds. One may contain sales events and group them by store and day. Another may begin with all store-days declared by an operating calendar, including days with no sales.

A **universe** establishes its root-point domain under an **existence law**: what makes a point exist in that analytical world? Occurrence-based laws and declared or generated domains answer that question differently.

The root is relative to the chosen universe. A daily account state can be a primitive point even if another universe models transactions from which it could be reconstructed. “Root” does not mean the smallest physical event anyone could ever observe.

## 3.1 Absence is not self-interpreting

An absent record can correspond to a nonexistent point, an existing point where a measure is ineligible, an eligible but unsupported value, or a supported zero under an applicable completion law. A physical `NULL` does not tell us which one applies.

Suppose independent evidence establishes that a transaction occurred and its record was lost. Its existence is established; the missing record does not remove it from the population. Its amount may be unsupported. If the amount survives elsewhere but the transaction date does not, a total independent of Day placement may remain establishable while a daily breakdown does not.

By contrast, no record and no independent evidence of occurrence do not establish either occurrence or nonoccurrence. The needed evidence depends on the question. These distinctions preserve the intended population instead of replacing it silently with surviving rows. [1, §§2.3, 9]

# 4. An anchor is a partition of a universe

An **anchor** divides the universe's root points into non-overlapping blocks. Every root point belongs to exactly one block. Each block is an **anchor point**.

For a sales universe, Customer groups all root points attributed to the same customer. Month groups them by the declared monthly assignment. `{Customer, Month}` is their common refinement: the existing customer-month intersections.

The compound anchor need not contain every possible customer-month pair. Its point space can be sparse. A coordinate tuple is a way to identify a point, not proof that the point exists.

## 4.1 Refinement

If every point of anchor \(B\) belongs to exactly one point of anchor \(A\), write \(B\succeq A\). When the relation is strict, write \(B\succ A\): \(B\) is finer and \(A\) coarser.

For example, Day can refine Month. But Week and Month generally cross. Day may refine both without either refining the other. Weekly Revenue and monthly Revenue can both be valid measures while exact monthly Revenue is not recoverable from weekly totals alone.

A dimension is a conventional name for a governed partition. Hierarchies describe refinement between partitions. Neither a familiar column name nor a join establishes that relationship by itself.

## 4.2 Relationships, overlap, and anchor construction

Suppose one customer has several tags. The tag groups overlap, so the relation does not directly partition the customer universe. A single-valued assignment can choose one tag. An allocation can split contribution under a declared conservation rule. A membership universe can instead make each customer-tag membership a point, with its contribution semantics explicitly defined.

Full contribution to every membership is another possible law. It is different from conserving the customer's contribution across memberships. The choice must be analytical, not an unnoticed consequence of a physical join. These constructions preserve the partition definition rather than weaken it. [1, §2.1 and Appendix D]

# 5. Measure family, measure, and identity

A **measure family** specifies a governed analytical quantity, its formation, and the measures admitted by its law. A **measure** is that family at one current anchor:

\[
\boxed{F@A.}
\]

Revenue at Transaction, Revenue at Day, and Revenue at `{Customer, Month}` can belong to one additive family. They are different measures because their current anchors differ. Their family definition determines which movements and constructions are lawful.

## 5.1 Specify the target before checking a calculation

A family must say what quantity it asserts. The target may be specified directly over its analytical inputs, or by a nominated defining construction. Alternative sufficient-state bases are then judged against that target; agreement between two formulas cannot supply a missing definition.

For example, a definition of average revenue per order can specify the sum of participating order Revenue divided by the count of those same orders, on the declared nonempty domain. A second method using retained order values must construct that same quantity. Its agreement with the first method is a consequence to establish, not the source of the target's meaning.

The full family contract also covers constitutive inputs, admitted anchors, participation, value domains, sufficient-state bases, continuation, and empty or undefined cases. Familiar names such as “average” do not silently settle those choices. [1, §4]

## 5.2 Identity comes before comparison

A canonical name such as `revenue` resolves to the governed identity. A system may represent that identity with an immutable ID and a canonicalized semantic declaration. The name and the identity are different roles.

Identity includes meaning-bearing formation, anchors, parents, participation, order, and law parameters. It does not include an arbitrary choice of execution route or proof method for an already specified target.

Two exact derivations claiming the same measure under compatible evidence and satisfied contracts must agree. Equal numbers from different definitions do not merge those definitions; different numbers do not allow a system to split an identity retroactively to avoid the consistency obligation.

Changing a meaning-bearing definition establishes a successor identity. A later namespace can keep a familiar name while preserving the distinction. Merely changing a label or physical encoding need not create a new family. [1, §§2.2, 3.9, 6.4]

# 6. Transformation is movement over governed analytical objects

There are two questions to ask of a transformation: where does its result live, and what quantity does that result represent?

A **mapper** preserves the current anchor. A **reducer** contracts a strictly finer anchor to a coarser one within a universe. A ratio calculated from compatible operands at one anchor is a pointwise expression; adding contributions into monthly totals has reduction geometry. These shapes do not themselves confer family identity.

Replication is different again. Making a total available beside each customer's Revenue to calculate a share does not establish that total as each customer's Revenue. Structural availability is not allocation or a new finer measure.

## 6.1 A family can be specified by a construction

A complete admitted analytical law can give identity to a canonical expression such as:

\[
mean(revenue@Order).
\]

Its Order anchor says what is averaged. A measure of that family at Region is:

\[
mean(revenue@Order)@Region.
\]

The inner anchor is part of the family definition; Region is the one current reporting anchor. Replacing Order with Customer can change the quantity even when the output remains Region.

For a concrete illustration, suppose C1 has one order of 100 and C2 has two orders of 150 each. Average order Revenue is \(400/3\). Customer Revenues are 100 and 300, whose average is 200. Neither answer is an erroneous version of the other: they average different analytical inputs.

The canonical family expression does not require a separate business name. Nor does its spelling prove that its law and inputs are established. An alias, saved query, or successful computation cannot supply missing family authority.

## 6.2 Formation precedes information loss

**Formation** establishes the analytical input a law consumes. **Continuation** derives further measures under the same specified family law.

For a weighted mean, a value and its weight must be paired at the required input anchor before their products are summed. Multiplying two separately aggregated totals generally cannot reconstruct those products. Similarly, covariance needs jointly established pairs, not just two marginally supported series with matching-looking coordinates.

The co-participation contract states where operands participate together. Arithmetic syntax does not establish that relation. The principle is that a later operation cannot use a relationship that was neither retained nor reconstructed from governed evidence.

## 6.3 Contextual formation can support a later family

Consider the established series \(100,110,95,105\). Under a fixed predecessor rule, excluding the first day because it has no predecessor in this scope, its three eligible daily changes are \(10,-15,10\). A separately governed SUM family over those already-formed changes has total 5. Any lawful regrouping of the same three contributions preserves it.

If the original series is split into the first two and last two days and changes are recomputed independently inside those groups, the surviving changes are 10 and 10. Their total 20 omits the boundary change of \(-15\). This is changed formation, not another continuation of the same family.

Contextual formation therefore neither automatically creates nor automatically prohibits a family. A contextual family needs a specified target and formation, participation and boundary conditions, an independently justified basis, and coherent admitted continuation without changing the formation. Faithfully recomputing the original input is allowed; redefining its context silently is not. [1, §§3.1–3.6]

# 7. Sufficient state is different from the displayed value

Two groups have Revenue and order counts \((100,1)\) and \((300,2)\). Their displayed averages are 100 and 150. The combined average is \(400/3\), not 125. The displayed values omitted their weights.

Version 7.1 treats **sufficient state as a relationship among ordinary families**. SUM and COUNT measures at the target anchor can construct MEAN there:

\[
mean(x@I)@A=
\frac{sum(x@I)@A}{count(x@I)@A}.
\]

The numerator and denominator must cover the same governed contributions. The initial scalar-MEAN law is defined on a nonempty domain; no observations do not automatically mean an average of zero.

The sum and count are analytical quantities in their own right. They do not become a separate ontological kind because another family uses them as state.

## 7.1 Self-sufficiency and intake are different

An additive family is **self-sufficient** when its own supported values combine under its admitted continuation law. For COUNT, combining established counts 37 and 12 produces 49. Counting those two integers as new observations produces 2. Both use integers; their analytical roles differ.

MIN and MAX are self-sufficient on nonempty supported groups under their corresponding composition. They do not need an invented identity value for the empty case. Empty-result and evidence obligations remain separate from the algebra.

A family may also be sufficient for another target without being self-sufficient. An established variance can supply standard deviation at the same anchor through a square root. It does not follow that finalized variances can be averaged to obtain a coarser variance.

## 7.2 A sufficient basis is neither unique nor sufficient for every use

One exact MEAN basis is matching SUM and COUNT. A retained multiset of the same participating values is another. A multiset preserves multiplicity: `0, 0, 6` has mean 2, while the set `0, 6` has mean 3. Discarding multiplicity changed the construction.

For exact distinct count, a set-valued family is sufficient: combine identity sets by union, then take their cardinality. Two scalar counts do not generally determine overlap. Sets and multisets can be values of ordinary measures; their internal elements are not additional analytical anchors.

A basis must correctly construct the independently specified target throughout its admitted domain. Count alone does not determine MEAN, even though counts themselves combine perfectly. Bases must also be independently establishable: declaring the target sufficient for itself by the identity function proves nothing about continuation.

Different adequate bases need not contain the same information or be available together. Each proposed use has to preserve what that use requires. [1, §5]

## 7.3 FIRST and LAST retain the selecting analytical point

Consider a fixed store with three established participating Day points in one year: 30 January with stock 10, 31 January with stock 20, and 1 February with stock 15. Under declared chronology, LAST returns 15; MAX of the stock values returns 20.

A **witness** retains the selected analytical point with its operand value. January's LAST witness is `(31 January, 20)`; February's is `(1 February, 15)`. Combining them by the original Day order selects February's witness regardless of the order the two inputs arrive.

The foundation defines the witness-valued family \(W\) from the operand, analytical order, and participation law. It then defines the value-returning LAST family \(L\). On the admitted nonempty domain:

\[
L@A=\operatorname{value}(W@A).
\]

The witness family is self-sufficient for its admitted finite continuation. The scalar family can be constructed from it, but the scalar generally loses the selecting point needed for further continuation. FIRST uses the earlier point under the same kind of complete order.

This is the same architecture as MEAN from SUM and COUNT. No special state ontology is required. The point carried inside a witness is part of its value; the witness measure still has only its current anchor.

## 7.4 Analytical order has two levels

For a compound constitutive anchor, the admitted v7.1 construction declares a complete point order within each constituent dimension and a precedence among those dimensions. Compare two points on the highest-priority coordinate where they differ. This induces a complete lexicographic order on the existing analytical points.

Suppose Customer order is \(C_1<C_2\), Day order is \(d_1<d_2<d_3\), and exactly these participating points exist:

| Analytical point | Value |
|---|---:|
| \((C_1,d_3)\) | 80 |
| \((C_2,d_1)\) | 20 |
| \((C_2,d_2)\) | 40 |

Customer-then-Day precedence gives a global LAST of 40. Day-then-Customer gives 80. No absent \((C_2,d_3)\) point is created. Taking LAST separately for each customer gives 80 and 40; summing those gives 120, a different construction from either global selection.

These are meaning-bearing choices, not database tie-breakers. If several carrier rows contribute to one analytical point, they must first establish the operand there. A backend cannot select one of those rows as though it had selected the analytical point.

The order is over points, not the order in which anchors are traversed or fragments processed. Intermediate witnesses retain their original constitutive points; continuing through Month does not restart selection using an unrelated order of Month labels. The published proof covers finite contributing fibers with compatible inputs under the complete declared order. [1, §§7–8, 11.2]

# 8. Family law gives local coherence

Suppose additive Revenue is formed from the same sales under matching participation and contribution accounting. A direct Transaction-to-Month reduction and a staged Transaction-to-Day-to-Month reduction must agree when their contracts and evidence premises hold.

The reason is that daily groups partition the contributing transactions. Associative and commutative combination permits regrouping those same contributions without changing the result. Laws such as MIN and MAX can combine nonempty groups without an identity element. A monoid additionally has a combine identity; whether an empty eligible group has a supported answer remains a separate law-level question.

Composite families inherit coherence through an adequate basis. If matching SUM and COUNT reach the same target values, applying the same admitted MEAN constructor gives the same mean. Alternative bases must each be correct for that target, rather than merely agree with one another.

This is conditional mathematics, not a guarantee that every admitted route is currently executable. A plan consuming a missing intermediate state has not established its inputs. Another adequate argument may still establish the target. Unknown state cannot be replaced by an empty identity to make the first plan run.

Within a coherent instance, FIRST/LAST witness combination satisfies the same finite theorem: the later of the intermediate winning points is the global winner. Analytical order matters to the definition; physical enumeration does not.

If two paths claim the same exact measure and both meet their premises, disagreement indicates a failed premise or realization. Changing the path is not permission to change the family identity. [1, §6 and Propositions 8.1–8.2]

# 9. New analytical identities require lineage

Suppose two days contain order revenues `6, 4` and `7, 0`. A maximum over the four orders is 7. A maximum begun after daily Revenue has been formed is the maximum of 10 and 7, giving 10.

The Order and Day inputs establish different MAX-family constructions. Both can be reported at Month. Their **constitutive analytical lineage** records the input quantity, formation anchor, and law that make them different.

A family can have several parents. An explicitly governed Average Order Value family can be constructed from compatible Revenue and OrderCount measures. A ratio typed in a query does not automatically publish that family, but neither does the use of a ratio prevent an adequately declared family from existing.

Constitutive lineage and sufficient-state dependency answer different questions. The ancestry of `mean(revenue@Order)` says that it is a mean of Revenue at Order. Its SUM/COUNT basis says how a measure of that already specified family can be constructed. An alternative adequate basis does not automatically create another mean family.

The lineage is well-founded: identities cannot depend circularly on themselves. Execution histories may contain different routes and recoveries, but those are not all constitutive ancestry. [1, §§3.7–3.9, 6.5]

# 10. Identity, edge validity, certificate, and metadata

Important information does not all belong in identity. The theory distinguishes four responsibilities:

| Location | Governing question | Example |
|---|---|---|
| **Family identity** | What quantity and law are declared? | Net-of-returns Revenue; the order constituting a LAST family. |
| **Edge validity** | Does this derivation preserve the declared meaning? | Evidence that a relationship preserves contribution multiplicity. |
| **Certificate / materialization** | What does this realization establish or retain? | Exactness, approximation guarantee, evidence context, or retained witness. |
| **Metadata** | What accompanies the object without changing those claims? | A description or display label. |

The subject alone does not determine its location. The order defining a LAST family is constitutive; evidence that an execution preserves that order concerns derivation validity. A witness materialization and a scalar materialization can refer to the same scalar target without retaining the same capability.

Similarly, a changed business participation definition can change the quantity. Checking that an input actually covers the unchanged definition is an evidence obligation. The classification follows what changes, not which software field happens to hold the information. [1, §1.5]

# 11. Materialization is different from analytical identity

A **materialization** is stored analytical content. A measure may have several physical realizations without changing its identity. A monthly Revenue table, a compatible service response, and a newly computed result can all represent the same target.

But availability of a result is not permission for every later use. Two MEAN states, \((10,1)\) and \((1000,100)\), both display 10. Adding the contribution \((20,1)\) gives 15 in the first case and \(1020/101\) in the second. The scalar agreement did not preserve the weights.

## 11.1 Evidence follows the requested law

Suppose the complete participating domain is established as three ordered points \(s_1<s_2<s_3\). The value at \(s_3\) is supported as 30; earlier values are unavailable. LAST is established as 30, because the missing earlier values cannot change the maximal point or its supported value. SUM generally remains unestablished.

The same example shows why an unavailable intermediate does not refute a target. If intermediate groups are \(\{s_1\}\) and \(\{s_2,s_3\}\), the first witness is unavailable. The coarser witness \((s_3,30)\) is nevertheless established through known maximality. A plan specifically requiring both intermediate witnesses fails; another admitted argument succeeds. The unavailable witness is not known empty.

The converse guard matters: if a later eligible point may exist and the evidence does not exclude it, the latest observed value alone does not establish LAST. If the selected eligible point's value is unavailable, replacing it with the last supported observation changes the participation rule. [1, §§9.2–9.5]

## 11.2 A witness can be sufficient without being necessary

Fix a LAST target with two exhaustive possible participants \(p<q\). Participation definitely includes \(p\); inclusion of \(q\) is unresolved. The operand is supported as 7 at both points.

The nonempty scalar answer is 7 either way. The selected point is not established, so neither candidate witness can truthfully be reported as the actual winner.

This particular argument needs all its premises: a fixed law, known nonemptiness, exhaustive coverage of possible participants, and supported equal values at every possible winner. Equal values in surviving records are not enough. The example shows that a witness is a sufficient construction of scalar LAST, not a theorem that every value-only proof must establish the witness. [1, §9.6]

## 11.3 Record what is retained and what it supports

A materialization record must distinguish these cases:

| Retained content | What it can justify |
|---|---|
| An adequately established nonempty witness | The scalar by value projection, and admitted continuation using compatible witnesses. |
| Only a scalar projected from a witness no longer retained or recoverable | That scalar answer, not automatic witness reconstruction. |
| Only a scalar established without identifying a winner | The scalar under its actual justification; for §11.2, the fixed law, known nonemptiness, exhaustive possible participants, and supported equality at every possible winner. No invented witness. |

The last two cases can have the same scalar family identity and value. Proof method does not create another family. An artifact can also hold both the witness and scalar, or retain a witness and derive the scalar on demand.

A retained LAST witness does not generally determine the next winner after its point is excluded, deleted, or assigned another order. Sufficiency for coarsening is not sufficiency for arbitrary filtering or correction. A richer basis or additional governed evidence may support that different request.

Nor does lossy state validate all its original inputs. Suppose \(p<q\): one source supplies \((p,10),(q,20)\), and another supplies \((p,11)\) in what is claimed to be the same context. Compressing the first to \((q,20)\) conceals its conflict at \(p\). Compatibility must be established independently; a winner merge cannot certify everything it discarded.

The practical rule is to retain or reference enough information to establish **what content is available, which target it supports and why, and what later use is justified**. A catalog entry saying only “LAST is available” cannot answer all three questions. [1, §10]

# 12. Governed knowledge has to live somewhere

Organizations often already know the relevant definitions. Someone knows what Revenue includes, what makes an open store-day exist, which customer mapping is authoritative, and which retained totals can be reused. The difficulty is that this knowledge may be scattered across code, semantic models, reports, tests, and people's memory.

A **Manifold** can constitute an enterprise's governed analytical definitions under ToD: its universes, anchors, families, selected orders, and applicable contracts. It is a particular analytical model, not the category-level theory itself and not a synonym for physical storage.

Three responsibilities remain separate. The theory states the structural and mathematical obligations. A governance process selects authoritative definitions. Current evidence establishes the premises needed for a particular derivation. Institutional approval does not prove a mathematical law, and a valid law does not establish that today's source is complete.

An implementation consumes these definitions and reports its coverage. Unimplemented theory does not become invalid, and implemented behavior does not redefine the research. [1, §§1.1, 4, 12.3]

# 13. Query languages can declare the result

Once analytical identity is explicit, a request can identify Revenue and OrderCount at `{Customer, Month}` without giving the requester responsibility for choosing physical joins and intermediate tables.

A request language must still articulate every meaning-bearing choice it undertakes to express. “Average Revenue” may need an Order or Customer input anchor. An ordered construction must resolve its constitutive order. The language can be designed and adopted independently of a particular implementation's coverage.

Input restriction and output selection are different. A restriction affecting which observations form a statistic can change that statistic. Filtering or sorting already-established output points need not change their measure identities. Neither a pushdown optimization nor an output sort establishes an unspoken analytical law.

A resolved explanation and its execution must refer to the same meaning. An explanation based on declarations can identify applicable obligations without pretending that data-dependent evidence has already been checked. These are consequences of the analytical boundary, not a specification of query syntax here. [1, §12.4]

# 14. AI can interpret without becoming analytical authority

A model can help interpret “maximum revenue,” identify candidate definitions, and explain the difference between maximum order Revenue and maximum daily Revenue. It can propose the relevant anchor and ask for clarification.

Those are useful interpretive acts. They do not establish the family contract or authorize a physical computation. If two meanings remain possible and only one has a cached answer, the cache has not resolved the ambiguity.

Conversely, two adequate bases for one fixed target are not two intentions requiring a user decision. Once meaning is fixed, an implementation can select an admitted realization according to its capabilities and constraints, while preserving the target's evidence and reuse requirements.

The value of the theory for analytical agents is an independently stated object to interpret and check. Fluent explanations and executable code cannot substitute for that object's definitions or premises. [1, §§2.2, 3.9, 5, 12]

# 15. Neighboring questions: regime, evidence, and statistics

Observed, forecast, simulated, or intervention-qualified quantities can differ even at the same anchor. A regime is identity-bearing when the declared change of value-generation arrangement changes the analytical quantity. Evidence status describes the support for a premise; it is not a new definition of the quantity whenever evidence changes.

Approximation also has a precise location. An approximate realization can target the same exact distinct count as an exact computation, with an explicit approximation and error contract. That estimate is not an exact sufficient-state basis for the count. Keeping the target identity does not make the estimate exact, and changing a realization's accuracy alone need not create another quantity.

Exact algebra likewise does not prove that every numerical backend preserves it. Finite-precision operations need a realization contract adequate for the promised equality or approximation guarantee. Stable output alone is not conformance.

Finally, a governed descriptive statistic does not establish a claim about a larger population, a future period, or a causal effect. Those crossings require additional assumptions and evidence, developed in the Statistical Bridge. Analytical validity, inferential warrant, and permission to act remain distinct. [1, §§10.9, 12.1, 12.5; 3]

# 16. The change in perspective

The starting point is no longer a table that happens to contain a number. It is a governed analytical quantity at a defined location, supported by a particular body of evidence.

The universe establishes the points. Anchors organize them. Families specify quantities and admitted laws. Formation establishes the inputs; sufficient-state relationships explain which other family measures can construct a target. Coherence states when different admitted paths must agree. Lineage records the choices that actually define a new quantity.

This supports a small but consequential discipline: specify the question before choosing a computation, preserve the information the next law needs, and distinguish a supported answer from a reusable representation. A missing intermediate need not defeat an otherwise established target. A correct stored scalar need not support another calculation.

ToD does not eliminate business judgment, uncertain evidence, or implementation work. It makes their analytical obligations explicit enough that they can be checked without letting storage, syntax, or accidental computation decide what a number means.

## Introductory glossary

| Term | Meaning in this introduction |
|---|---|
| **Datum** | One typed value at an analytical point under the relevant quantity definition. |
| **Universe / existence law** | The governed root-point domain and the rule establishing which points exist. |
| **Anchor / anchor point** | A partition of the universe / one nonempty block of that partition. |
| **Refinement** | A relationship in which each finer point belongs to exactly one coarser point. |
| **Measure family** | A governed analytical identity with specified formation and admitted measures under its law. |
| **Measure \(F@A\)** | Family \(F\) at one current anchor \(A\). |
| **Canonical name / family ID** | A governed handle / an immutable system representation of the analytical identity. |
| **Target specification** | The quantity asserted, fixed directly or by a nominated defining construction before candidate bases are checked. |
| **Constitutive anchor** | An input location that helps define the family, rather than an additional current anchor. |
| **Formation / continuation** | Establishing the analytical input / constructing further measures under the admitted family law without silently changing that formation. |
| **Mapper / reducer** | Anchor-preserving transformation / strict finer-to-coarser contraction. Neither shape alone confers family authority. |
| **Co-participation** | The governed rule establishing where several operands participate together. |
| **Sufficient-state basis** | Ordinary family measures adequate for a particular target construction on an admitted domain. |
| **Self-sufficient family** | A family whose own supported measures combine under its admitted associative and commutative continuation law. |
| **Analytical order** | Governed point orders and dimension precedence inducing the order used by the admitted ordered construction. |
| **Witness family \(W\)** | The ordinary family retaining the selected constitutive point and its operand value, with declared empty-state behavior. |
| **Coherence** | Agreement of admitted derivations when their required compatible contributions and other premises are established. |
| **Analytical lineage** | Well-founded constitutive ancestry of family identities, not every operational route. |
| **Eligibility / support** | Where a quantity applies / where the evidence establishes its value under the law. |
| **Materialization** | Retained analytical content whose established claims and permitted reuse must be distinguished. |
| **Certificate / realization standing** | The evidence, exactness or approximation, retained capability, and other qualifications of a realization. |

## References and reading path

**[1]** Wang, Huayin. *The Theory of Data: A Foundation for Analytical Identity, Derivability, and Consistency*. Version 7.1, 7 September 2026. Zenodo. DOI: [10.5281/zenodo.22649945](https://doi.org/10.5281/zenodo.22649945). The governing foundation, including the Statistical Extension Reference in the same publication record.

**[2]** Wang, Huayin. *The Theory of Data: An Introduction — Analytical Meaning, Lawful Transformation, and Governed Results*. Version 2.2. Zenodo. DOI: [10.5281/zenodo.22018598](https://doi.org/10.5281/zenodo.22018598). The predecessor whose teaching organization this edition retains.

**[3]** Wang, Huayin. *The Statistical Bridge: From Governed Evidence to Inference Certificates and Licensed Claims*. Version 3.0. Zenodo. DOI: [10.5281/zenodo.21979821](https://doi.org/10.5281/zenodo.21979821). Related published work; the discussion here follows its boundary as stated in [1, §12.5].

For a shorter first reading, use *A Primer on the Theory of Data*, Version 2.3, DOI [10.5281/zenodo.22651578](https://doi.org/10.5281/zenodo.22651578). It is aligned with the same published v7.1 foundation.

## Revision note

The sixteen main sections preserve the predecessor's route from analytical requests, datum, universe, and anchor through family identity, transformation, state, coherence, lineage, governance locations, materialization, declarations, request languages, AI, and neighboring questions. The explanations are updated to the published v7.1 contract, with ordinary sufficient-state families, constructive identity, governed FIRST/LAST, contextual formation, and target-relative evidence and reuse. Older graft terminology is absorbed into family formation, and the broader v6.1 state taxonomy is not presented as current family admission. The numerical examples illustrate the foundation's existing laws; this introduction does not extend its function catalog, make additional theoretical admissions, or assert software implementation coverage.
