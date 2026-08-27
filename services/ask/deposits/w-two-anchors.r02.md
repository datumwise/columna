---
title: "The Two Anchors of a Measure"
subtitle: "Why Input and Output Anchors Are Part of Analytical Meaning"
author: "Huayin Wang"
date: "Version 2.0 - 11 August 2026"
lang: en-US
papersize: letter
geometry: margin=0.88in
fontsize: 11pt
subject: "Input and output anchors as constitutive parts of analytical meaning"
keywords:
  - analytical measure
  - analytical metric
  - input anchor
  - output anchor
  - grain
  - aggregation
  - sufficient state
  - analytical correctness
  - silent analytical failure
  - Theory of Data
  - Frame-QL
header-includes:
  - |
    \usepackage{microtype}
  - |
    \usepackage{booktabs}
  - |
    \usepackage{longtable}
  - |
    \usepackage{array}
  - |
    \usepackage{enumitem}
  - |
    \usepackage{fancyhdr}
  - |
    \usepackage{url}
  - |
    \setlist{nosep}
  - |
    \setlength{\emergencystretch}{3em}
  - |
    \clubpenalty=10000
    \widowpenalty=10000
    \displaywidowpenalty=10000
  - |
    \pagestyle{fancy}
    \fancyhf{}
    \fancyhead[L]{\small The Two Anchors of a Measure}
    \fancyhead[R]{\small Huayin Wang}
    \fancyfoot[C]{\thepage}
    \renewcommand{\headrulewidth}{0.4pt}
    \setlength{\headheight}{14pt}
  - |
    \urlstyle{same}
---

**datumwise, an independent open-source research project**  
**License:** Creative Commons Attribution 4.0 International (CC BY 4.0)

> **Central claim.** For an important class of analytical quantities, the input anchor and output anchor are not implementation details and not merely metadata. They are part of what the requested quantity means. A system that records only the output location leaves a structural degree of freedom: it may silently choose what was reduced, counted, selected, weighted, or otherwise operated over. That freedom is a recurrent source of analytical failure.

# Abstract

A stored analytical result is conventionally described by one grain: the grain at which the result is reported. That is often sufficient for additive quantities such as total revenue. It is not sufficient in general.

Many common analytical operations involve two distinct analytical locations. The **input anchor** identifies the points over which an operation is formed or reduced. The **output anchor** identifies the points at which the resulting member is reported. Average order value over orders and average revenue over customers can occupy the same output anchor and use the same underlying revenue while denoting different quantities because their input anchors differ. Weighted averages, rates, ratios, counts, extrema, order statistics, and multi-stage reductions expose the same issue in different ways.

Within the *Theory of Data* framework, a measure is a stable governed family and a member is one anchored realization of that family. "Two anchors of a measure" is therefore compact language for a more precise claim: an anchor-sensitive operator instance or derivation may require both an input member at an input anchor and an output member at an output anchor, and the input anchor may be identity-bearing.

Two questions must be kept separate. **Sufficient-state composability** asks whether staged reductions preserve the information required for exact continuation. **Input-anchor sensitivity** asks whether changing the input anchor changes the value or interpretation of the requested quantity. COUNT, for example, composes through additive count state even though reapplying COUNT to displayed counts is wrong; MIN and MAX can compose exactly while still being uninterpretable without knowing what entities they ranged over. This distinction yields a general materialization rule: values, sufficient state, and analytical identity must not be collapsed.

The practical importance is not hypothetical. The companion silent-failure taxonomy classifies five of fourteen planted benchmark defect classes as **anchor freedom** failures, including re-aggregation, semi-additive summation, empty-bucket behavior, and definition ambiguity. In a nine-model text-to-SQL study, the structural failure families persisted despite strong schema documentation. The lesson is architectural: analytical systems need an explicit, structured, verifiable account of anchor-sensitive meaning. Query languages and AI interfaces that can name only a metric, output dimensions, and filters are therefore not expressive enough for every analytical request. A language must either derive the missing input anchor uniquely, ask for it, or represent it explicitly.

# 1. A number that is not one number

Here is a region's sales for a quarter:

| order | customer | lines (each a sale) | order total |
|---|---|---|---:|
| O1 | C1 | $100, $20 | $120 |
| O2 | C1 | $10 | $10 |
| O3 | C2 | $40, $40, $40 | $120 |

Total revenue is $250.

Now answer an ordinary question:

> **What is the average order value?**

There are at least three mechanically simple reductions available:

- averaged over **orders**: $250/3=\$83.33$;
- averaged over **lines**: $250/6=\$41.67$;
- averaged over **customers**: $250/2=\$125.00$.

The output territory is unchanged: the same region and the same quarter. The numerator is unchanged: the same $250 of revenue. The arithmetic in every line is correct.

What changed is the analytical population being ranged over by the denominator.

That difference is not merely "how the query was written." It changes the quantity being denoted.

A table stored at line grain can silently return $41.67 under a column named `avg_order_value`. A customer-level materialization can silently return $125.00 under the same name. A semantic catalog can preserve the name, data type, owner, description, refresh schedule, and physical lineage while still failing to preserve the one fact that distinguishes the three quantities:

> **average over what?**

That missing fact is the **input anchor**.

The grain at which the result is reported is the **output anchor**.

For a large class of analytical operations, both matter.

# 2. What "two anchors" means

The phrase **two anchors of a measure** is deliberately compact. In the *Theory of Data*, the underlying ontology is more precise.

A **datum** is one typed value at one anchor point.

A **member** is a homogeneous typed binding of datums over one anchor in one universe.

A **measure** is the stable governed family whose laws determine which anchored members share one analytical identity.

Thus `revenue` names a measure. Transaction revenue, order revenue, and customer-month revenue may be different members of that measure when the measure law licenses the movements that connect them.

This means that a measure family does not literally have exactly two anchors. It may admit many members at many anchors.

The two-anchor claim concerns an **operator instance or derivation**. In its simplest form:

$$
\rho_f\!\left(m@A_{\mathrm{in}}\right)@A_{\mathrm{out}},
$$

where:

- $m@A_{\mathrm{in}}$ is the input member or input realization;
- $f$ is the selected operator subfamily or transformation;
- $A_{\mathrm{in}}$ is the input anchor;
- $A_{\mathrm{out}}$ is the output anchor;
- the measure law determines whether the derivation preserves the same measure identity, synthesizes another measure, or fails to close as a governed analytical object.

The output anchor answers:

> **At what analytical points should the result exist?**

The input anchor answers a different question:

> **Over what analytical points is this operation defined?**

Those questions can coincide. They often do not.

They are also not the whole analytical contract. Universe, regime, observation, provenance, participation, approximation, and other fields may matter independently. The claim here is narrower: **when an operation is input-anchor-sensitive, omitting the input anchor leaves part of the requested analytical meaning unspecified.**

# 3. The input anchor can be identity-bearing

An output anchor may identify a member completely when the measure has one admitted operator family, one lawful lineage, and one interpretation at that location.

For additive revenue, for example, a request for revenue at customer-month may be determinate because the measure law establishes a unique identity-preserving reduction from finer revenue members.

But consider inventory at store-month. The output anchor `{store, month}` does not distinguish:

- last inventory in the month;
- first inventory in the month;
- maximum daily inventory;
- average observed inventory;
- sum of daily snapshots.

The physical output location is the same. The analytical object is not.

Likewise, `avg(revenue)` at region-quarter does not determine whether the average is over lines, orders, customers, days, stores, or another admissible input member.

A resolved member identity may therefore need to retain the input anchor when the selected operator family is grain-sensitive. Schematically:

$$
I_m =
(\iota_{\mathbb M}, f, A_{\mathrm{in}}, A_{\mathrm{out}}, U, \ldots),
$$

with the measure law deciding whether $A_{\mathrm{in}}$ is identity-bearing or merely derivation history.

This gives the two-anchor claim its strongest form:

> **An input anchor is not extra metadata when changing it changes the value or interpretation of the result. In that case it is part of the identity of the requested analytical member or operator instance.**

# 4. Two independent questions: composability and anchor sensitivity

A common temptation is to use one property - such as path independence or re-aggregability - to decide whether an input anchor can be forgotten. That collapses two different questions.

The first is about whether enough computational state survives for exact continuation. The second is about whether the identity or interpretation of the quantity depends on what analytical entities were operated over.

## 4.1 Sufficient-state composability

An aggregate often has an intermediate state $S$ that retains exactly the information required to continue a reduction lawfully.

A generic order-insensitive aggregate can be represented by:

$$
\mathrm{embed}:X\to S,
\qquad
\mathrm{combine}:S\times S\to S,
\qquad
\mathrm{finalize}:S\to Y.
$$

Staged and direct reductions agree when the sufficient state composes under the registered law.

For SUM, the state is a sum and the combiner is addition.

For COUNT, the state can be the count itself, but **the lawful combiner is addition, not COUNT again**. If one subgroup contains 3 rows and another contains 7, their combined count is $3+7=10$; `COUNT(3,7)=2` is a different operation.

For AVG, the sufficient state is typically:

$$
(\mathrm{sum},\mathrm{count}),
$$

and the displayed mean is obtained only at finalization. A scalar average usually discards the state needed for exact later composition.

For exact distinct count, sufficient state may be the set of distinct identities and combination may be set union; practical systems may instead use an approximate sketch with a separate approximation contract.

The important distinction is:

> **A displayed scalar is not necessarily the sufficient state of the aggregate that produced it.**

## 4.2 Input-anchor sensitivity

A separate question is whether the quantity's meaning depends on what analytical entities were operated over.

COUNT is composable through additive count state, but a count still means **count of what**.

MIN and MAX are exactly composable through extrema state, but "minimum balance" still means **minimum over what set of balances**.

AVG can be both state-sensitive and anchor-sensitive.

Weighted averages can be anchor-sensitive because a pointwise product must be formed before reduction at a particular co-anchored input location.

These are not the same property.

The classification is therefore:

| Operation family | Typical sufficient state | Can exact state be staged? | Can input anchor be meaning-bearing? |
|---|---|---|---|
| SUM | scalar sum | yes, combine by `+` | often no under a unique additive law |
| COUNT | scalar count | yes, combine by `+` | yes: count **of what** |
| MIN / MAX | scalar extremum | yes, combine by `min` / `max` | yes: extremum **over what** |
| AVG | `(sum, count)` | yes in state; not from finalized mean alone | yes |
| weighted AVG | `(sum(wx), sum(w))` plus input co-location law | yes in state | yes |
| exact DISTINCT COUNT | set / exact identity state | yes in state; not from finalized count alone | yes |
| approximate DISTINCT | sketch | yes under sketch law | yes, plus approximation contract |

The practical consequence is broader than a single materialization test:

> **Analytical storage must preserve three things separately: the value, the sufficient state required for lawful continuation, and the identity-bearing contract fields required to know what the value means.**

No one of those substitutes for the other two.

# 5. Average: the denominator reveals the input anchor

Return to the $250 revenue example.

The numerator is additive revenue. Under an admitted additive law it can usually be reduced to the output region-quarter without retaining the intermediate anchor as identity.

The denominator does something different:

$$
\mathrm{count}(\text{input units}@A_{\mathrm{in}})@A_{\mathrm{out}}.
$$

If $A_{\mathrm{in}}$ denotes orders, the count is 3.

If it denotes lines, the count is 6.

If it denotes customers, the count is 2.

Hence:

$$
\mathrm{avg}_{A_{\mathrm{in}}}(\mathrm{revenue})@A_{\mathrm{out}}
=
\frac{\mathrm{revenue}@A_{\mathrm{out}}}
{\mathrm{count}(A_{\mathrm{in}})@A_{\mathrm{out}}}.
$$

The ordinary-language question is again:

> **Average over what?**

That question is not a request for extra display metadata. It selects the denominator population and therefore the quantity.

This is why an average whose input anchor is underdetermined should not be silently executed against whichever physical rows happen to be nearest.

# 6. Weighted averages: the input anchor can enter before reduction

Consider two product lines:

| line | unit price | quantity |
|---|---:|---:|
| A | $10 | 2 |
| B | $5 | 10 |

The quantity-weighted average price is:

$$
\frac{10\cdot2+5\cdot10}{2+10}
=
\frac{70}{12}
=\$5.83.
$$

The plain average of the two price rows is:

$$
\frac{10+5}{2}=\$7.50.
$$

The difference is not caused by a faulty SUM. Both the weighted numerator and denominator ultimately reduce additively.

The crucial operation is the pointwise map:

$$
(\mathrm{price},\mathrm{quantity})
\mapsto
\mathrm{price}\cdot\mathrm{quantity},
$$

which must be formed where price and quantity are lawfully co-anchored **before** reduction.

Once only the reduced factors survive, the necessary pointwise products may be unrecoverable. An average price of $7.50 and a total quantity of 12 do not determine the weighted numerator 70.

The stronger interpretation is therefore not merely that "nonlinearity makes the input grain live."

> **The input anchor can be a typing and co-location requirement of the operation that constructs sufficient state.**

This is why some analytical meaning resides in the structure of the derivation, not in the final scalar.

# 7. MIN and MAX: exact composition does not make meaning self-describing

Take one customer with two accounts over three days:

| day | account A1 | account A2 | customer total |
|---|---:|---:|---:|
| 1 | $5 | $1000 | $1005 |
| 2 | $800 | $60 | $860 |
| 3 | $400 | $50 | $450 |

Ask:

> **What was this customer's minimum balance this week?**

Two natural readings are:

- minimum over **account-days**: $5;
- minimum over **customer-day totals**: $450.

MIN composes exactly: minima of subgroup minima can produce the overall minimum under the same population of underlying values. But that composability does not answer what the underlying values represent.

The scalar $5 does not say whether it is:

- the smallest account balance;
- the smallest customer total;
- the smallest daily balance;
- the smallest month-end balance;
- or another governed member.

This exposes the mistake in treating aggregation safety as the whole problem.

> **A statistic can be perfectly re-composable and still fail to carry its own analytical interpretation.**

For extrema, selection, counts, quantiles, and related operators, the input anchor can remain part of meaning even when the sufficient state composes exactly.

# 8. Materialization: value, state, and identity are different

Materialization is best understood by separating three things that physical storage often collapses.

A materialized analytical field may need to preserve:

1. **value** - the displayed or returned datum values;
2. **sufficient state** - the information required for lawful later composition;
3. **analytical identity** - the contract fields required to know what member or synthesized measure the values represent.

These can differ.

A monthly mean may preserve the displayed value but discard `(sum, count)`.

A count may preserve sufficient state for coarsening while still requiring an input-anchor identity such as orders versus customers.

A MIN may preserve exact compositional state while still requiring the input anchor for interpretation.

An additive revenue sum may, under a uniquely declared additive family, permit the input staging anchor to be projected out of canonical identity while retaining it only in certificate history.

The right question is therefore not:

> Can this number be stored?

It is:

> **What must travel with this materialization so that later use remains both lawful and semantically determinate?**

The answer is measure-specific and operator-specific.

# 9. Anchor freedom is a structural source of silent failure

The importance of two anchors becomes clearest when the distinction is omitted.

The companion position *The Two Great Sources of Silent Analytical Failure* defines **anchor freedom** as silent resolution of aggregation lineage. Its benchmark taxonomy places five of fourteen planted defect classes under that freedom:

| Anchor-freedom defect class | What is silently resolved |
|---|---|
| `mule_reaggregation` | finalized aggregate treated as re-aggregable state |
| `distinct_reaggregation` | distinct scalar treated as composable without identity state |
| `semi_additive_sum` | stock or level summed across a blocked anchor movement |
| `empty_bucket` | algebraic identity / absence / zero resolved without the required contract |
| `ambiguity/stated_resolution` | one of several legitimate analytical definitions selected silently |

The same benchmark places four further classes under universe freedom. Thus nine of fourteen planted classes fall under the two structural freedoms. In a nine-model single-shot text-to-SQL study over documented schemas, those structural failure families persisted across vendors and model scales.

This evidence does not prove that the two-anchor framework is the unique or complete theory of analytical error. It supports a narrower claim:

> **The omitted anchor structure corresponds to a recurrent operational failure family that better documentation alone did not eliminate.**

That matters especially for automated analytical systems. A human analyst may stop and ask what "average order value" means. An agent can bind a plausible input grain in milliseconds and return a confident answer while recording no choice at all.

The error is then not merely that the agent used a bad formula.

The deeper error is that the system allowed an identity-bearing analytical coordinate to remain free.

# 10. Why names are not enough

Practice already knows that input anchors matter. It often encodes them in names.

`ARPU` and `ARPPU` differ because "user" and "paying user" select different denominator populations.

"Per order," "per customer," "daily average," "monthly average," "blended CAC," and similar phrases frequently carry an input or output grain implicitly.

This is useful evidence of the underlying concept. It is also an unreliable representation.

Names fail in three ways.

**They are incomplete.** A name may mention one anchor role but omit another.

**They are role-ambiguous.** "Average order value per customer" can mean average *over customers* or a separate average *reported for each customer*.

**They are not mechanically adjudicable.** A string saying `avg_order_value` cannot establish that an order member exists, that the relevant input anchor is reachable, that the requested reduction is lawful, or that sufficient state survives.

A name is therefore evidence of intent, not a substitute for the analytical contract.

The stronger rule is:

> **Where an input anchor is constitutive of meaning, it should be explicit, structured, and verifiable - or uniquely derivable from an equally explicit governed law.**

# 11. Query-language consequence: a safe surface must still express the question

The two-anchor problem has a direct consequence for analytical query languages and AI interfaces.

A common constrained interface asks an agent to provide:

```text
metric: average_revenue
dimensions: [region, quarter]
filters: [...]
```

This is safer than unrestricted text-to-SQL because the agent does not author an arbitrary physical program.

But the envelope has no general place to distinguish:

```text
average revenue over orders, reported by region-quarter
```

from:

```text
average revenue over customers, reported by region-quarter
```

if both share the same metric name, output dimensions, and filters.

A safe request language therefore faces a requirement that is easy to miss:

> **Safety cannot be purchased by deleting distinctions that belong to analytical meaning.**

A language must do one of three things when the input anchor matters:

1. derive it uniquely from governed measure law;
2. expose it explicitly in the request;
3. ask for clarification rather than choose silently.

Frame-QL makes this distinction visible with the characteristic shape:

```text
operator(measure @ input_anchor) AT output_anchor
```

For example, conceptually:

```text
avg(revenue @ {order}) AT {region, quarter}
```

is a different request from:

```text
avg(revenue @ {customer}) AT {region, quarter}
```

The two anchor positions are not syntactic ornament. They correspond to two different analytical roles.

The input pin need not always be written. Where the measure law establishes that staging is immaterial and the input lineage is uniquely determined, a language may omit it safely. But where the statistic is grain-sensitive, omission is under-specification, not convenience.

This produces a useful design principle for AI-native analytics:

> **Give the agent enough language to state the analytical distinction, but do not give it authority to invent the physical execution that realizes the distinction.**

The first requirement is expressive power. The second is architectural safety. Two anchors are one place where both requirements meet.

# 12. Scope and limitations

This paper makes a narrower claim than its title can suggest.

It does **not** claim that every measure family literally has two fixed anchors. A measure may have many governed members at many anchors.

It does **not** claim that the input anchor is always part of canonical identity. Where sufficient state composes and the measure law establishes input-anchor immateriality, the input anchor may be derivation or certificate history rather than identity.

It does **not** claim that anchors exhaust analytical meaning. A complete member may additionally depend on universe, regime, participation, observation, provenance, approximation, evidence, and other contract fields.

It does **not** claim that every analytical error is an anchor error. The silent-failure taxonomy itself distinguishes anchor freedom from universe, coverage, and freshness freedoms, and the broader Theory distinguishes further failure layers.

It does **not** claim a complete formal theorem for every operator discussed here. The finite Contract Calculus proves sufficient-state staging and related results only for its declared fragments. The broad claim that input anchors can be meaning-bearing is a framework proposition supported by the examples, the implemented Frame-QL semantics, and the benchmark taxonomy.

The paper's contribution is the structural distinction:

> **An output location tells us where a result lives. It does not always tell us what the operation ranged over. When the latter changes the value or interpretation, the input anchor is part of the analytical question and must be governed accordingly.**

# 13. Conclusion

Analytical systems have traditionally treated the reported grain as though it were the complete location of a metric.

For a large class of operations, it is not.

An average is an average **over something**.

A count is a count **of something**.

A minimum is a minimum **among something**.

A weighted statistic is formed from co-located inputs **somewhere before reduction**.

Those "somethings" occupy analytical locations. When changing that location changes the result or what the result means, the location is not implementation detail. It is part of the analytical object being requested.

This is the two-anchor principle:

$$
\boxed{
\text{input anchor}
\;\neq\;
\text{output anchor}
}
$$

and, when the operator is input-anchor-sensitive,

$$
\boxed{
\text{analytical meaning}
\supset
\{A_{\mathrm{in}},A_{\mathrm{out}}\}.
}
$$

The distinction explains why a metric name can hide several legitimate quantities, why a materialized scalar can lose the information needed for lawful reuse, why correct arithmetic can still answer the wrong analytical question, and why automated systems need more than better prompting or richer documentation.

The practical rule is simple:

> **Do not silently choose an anchor that changes what the quantity means. Declare it, derive it under law, or ask.**

# References

Horner, J., and Song, I.-Y. (2005). "A Taxonomy of Inaccurate Summaries and Their Management in OLAP Systems." In *Conceptual Modeling - ER 2005*, Lecture Notes in Computer Science 3716, 433-448. Springer. DOI: 10.1007/11568322_28.

Kimball, R., and Ross, M. (2013). *The Data Warehouse Toolkit: The Definitive Guide to Dimensional Modeling*. 3rd ed. Wiley.

Lenz, H.-J., and Shoshani, A. (1997). "Summarizability in OLAP and Statistical Data Bases." In *Proceedings of the Ninth International Conference on Scientific and Statistical Database Management*, 132-143. IEEE Computer Society. DOI: 10.1109/SSDM.1997.621175.

Mazón, J.-N., Lechtenbörger, J., and Trujillo, J. (2009). "A Survey on Summarizability Issues in Multidimensional Modeling." *Data & Knowledge Engineering* 68(12): 1452-1469.

Wang, Huayin. (2026a). *The Silent Failure Atlas: A Taxonomy of Silent Analytical Failures in Data Analysis*. Version 1.3. Zenodo. DOI: 10.5281/zenodo.20762839.

Wang, Huayin. (2026b). *The Two Great Sources of Silent Analytical Failure*. datumwise position; paper of record on Zenodo. DOI: 10.5281/zenodo.21553379.

Wang, Huayin. (2026c). *A Contract Calculus for Governed Analytical Transformation: Totality, Partiality, Population, Expansion, and Fan-Out*. Version 1.0. Zenodo. DOI: 10.5281/zenodo.21752373.

Wang, Huayin. (2026d). *Technical Supplement Collection for A Contract Calculus for Governed Analytical Transformation*. Version 1.0. Zenodo. DOI: 10.5281/zenodo.21752681.

Wang, Huayin. (2026e). *The Theory of Data: A Foundational Framework for Governed Analytical Data, Lawful Transformation, and Certification*. Version 5.0. Zenodo. DOI: 10.5281/zenodo.21842194.

Wang, Huayin. (2026f). *The Frame-QL Manual*. Second Edition. datumwise. Documentation of the current Frame-QL language and Columna implementation.

