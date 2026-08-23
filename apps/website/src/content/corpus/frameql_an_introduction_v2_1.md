---
title: "Frame-QL: An Introduction"
subtitle: "Query by Declaring the Result"
author: "Huayin Wang"
date: "Version 2.1 - 16 August 2026"
lang: en-US
papersize: letter
geometry: margin=0.82in
fontsize: 11pt
subject: "An introduction to Frame-QL as a query language for governed analytical results"
keywords:
  - Frame-QL
  - analytical query language
  - Theory of Data
  - measure family
  - measure
  - frame
  - Manifold
  - governed analytics
  - analytical intent
  - AI agents
  - SQL
  - analytical adjudication
  - input anchor
  - output anchor
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
    \fancyhead[L]{\small Frame-QL: An Introduction}
    \fancyhead[R]{\small Huayin Wang}
    \fancyfoot[C]{\thepage}
    \renewcommand{\headrulewidth}{0.4pt}
    \setlength{\headheight}{14pt}
  - |
    \urlstyle{same}
---

**datumwise, an independent open-source research project**  
**License:** Creative Commons Attribution 4.0 International (CC BY 4.0)  
**DOI:** 10.5281/zenodo.21966453  
**Previous published version:** Version 2.0, DOI 10.5281/zenodo.21960798

## Abstract

Frame-QL is a query language for declaring a governed analytical result. The requester names the analytical quantities to be returned, declares the final anchor at which the result frame should exist, and states conditions that shape the request. The requester does not prescribe the relational operations or physical commands used to produce the result.

The language is naturally explained using the current *Theory of Data*, Version 6.0. A **measure family** is a uniquely governed analytical family such as Revenue. A **measure** is that family at one anchor:

$$
\boxed{Measure = MeasureFamily @ Anchor}
$$

Thus `Revenue@CustomerMonth` is a measure. A Frame-QL statement such as:

```frameql
FROM retail_manifold
SELECT revenue
AT {customer, cal.month}
```

asks the governed environment for Revenue at the customer-month output anchor without requiring the requester to manufacture the path through physical data.

Frame-QL has two anchor spellings because the shipped language exposes two different structural responsibilities. Query-level `AT` is mandatory and declares the one final output anchor of the frame. Expression-local `@ {…}` is the shipped input-anchor marker: it pins the anchor at which a subexpression must be available when it is consumed by an enclosing operation. Conceptually, an expression such as `revenue @ {order}` denotes Revenue at Order for that use, but `@` does not replace `AT` as an output declaration.

This paper develops the central idea of Frame-QL: **the output frame is the query**. It explains why rows, tables, joins, and `GROUP BY` are not primitives of the request interface; how a governed family name and an anchored measure differ from a physical column; how ambiguity becomes clarification rather than silent choice; and why Frame-QL provides a natural analytical-intent boundary for AI-assisted analytics.

The *Frame-QL Manual, Second Edition* remains authoritative for shipped syntax, canonical form, operators, outcomes, reason codes, and version-specific behavior. This introduction does not import unshipped Theory of Data features into the language. The *Theory of Data*, Version 6.0, is the conceptual reference for analytical identity and lawful transformation.

## Terminology and scope

This is an introduction to the idea behind Frame-QL, not a grammar reference or a catalogue of every shipped feature. It develops one proposition:

> **A Frame-QL query declares the output data. It does not prescribe the process used to produce it.**

The current Theory of Data uses the following vocabulary:

- **measure family** — a governed analytical family such as Revenue;
- **measure** — that family at one anchor, written $F@A$;
- **anchor** — a governed partition of a universe;
- **reducer** — a lawful contraction from a strictly finer source anchor to a coarser target anchor;
- **sufficient state** — state required for lawful exact continuation;
- **analytical lineage** — constitutive ancestry among measure families.

The shipped Frame-QL / Columna implementation also has its own vocabulary—columns, series, family sets, V/M/B anchors, integrity certificates, and reason codes. Those terms retain their Manual-defined implementation meanings. In particular, this introduction does **not** reinterpret the Manual's V-anchor, M-anchor, and B-anchor as three foundational anchor kinds in ToD v6.

Likewise, the public Frame-QL syntax does not become larger merely because ToD v6 is larger. The Theory may distinguish analytical structures that the current language does not expose. The Manual remains the normative boundary for what Frame-QL actually accepts and does.

The language is concise because responsibility has been divided, not because the omitted work has disappeared.

# 1. The result is the query

Consider a request for revenue by customer and month:

```frameql
FROM retail_manifold
SELECT revenue
AT {customer, cal.month}
```

The surface is deliberately familiar. A SQL-literate reader can see a source, a selected quantity, and an output location. But the statement is not a compressed relational program.

Under ToD v6 terminology, `revenue` is a governed family name. `AT {customer, cal.month}` declares the final anchor of the requested frame. Where the governed model establishes the family and the lawful path, the requested analytical object is:

$$
Revenue@\{Customer,Month\}.
$$

The statement does not name a transaction table. It does not identify a customer key, choose a date column, write a join, specify a grouping procedure, or decide whether the result should come from detail, a materialization, a cache, or an external service. It does not assume that the backend is relational.

The request can still be precise at the analytical level. It states what analytical quantity is wanted and where the result must live.

The core division of responsibility is:

> **The requester declares the result. The governed system owns the derivation.**

# 2. Measure families and requested measures

The Version 5 vocabulary used **measure** for the family and **member** for one governed realization at an analytical location. Version 6 simplifies that distinction:

$$
\boxed{Measure = MeasureFamily @ Anchor}
$$

Revenue is a **measure family**.

Revenue at customer-month is a **measure**:

$$
Revenue@CustomerMonth.
$$

This change is important for Frame-QL because it makes the request read almost literally.

```frameql
SELECT revenue
AT {customer, cal.month}
```

asks for the Revenue family at the frame's customer-month anchor.

A physical column may realize that measure. It is not the analytical identity itself. The same Revenue@CustomerMonth measure might be obtained from normalized transaction tables, a monthly materialization, cached sufficient state, an API, or another backend. Conversely, a physical column does not become a governed Revenue measure merely because it is named `revenue` and contains plausible values.

The analytical identity belongs to the governed model.

## 2.1 A frame is an output assembly, not a new foundational identity

A Frame-QL query returns a **frame**: selected result series co-located at one final output anchor.

A frame is important to the language because it is the requested result container. It is not, in ToD v6, a new foundational analytical identity parallel to measure family or measure.

The selected fields may denote governed measures, expressions over governed measures, or implementation-defined result series whose status is carried explicitly. The frame assembles them for one requested output location.

This is why query-level `AT` is so important: it gives the frame one final analytical location.

## 2.2 The final output anchor does not determine every analytical distinction

Consider:

```frameql
SELECT avg(revenue @ {order})
AT {region, quarter}
```

and:

```frameql
SELECT avg(revenue @ {customer})
AT {region, quarter}
```

Both return one result per region-quarter.

Assume the governed model establishes Revenue at both source anchors. The two expressions still need not request the same analytical quantity.

The difference is the source measure consumed by the average:

$$
Revenue@Order
$$

versus:

$$
Revenue@Customer.
$$

Version 6 treats the measure as having one **current** anchor. An operation consumes a source measure at its source anchor and produces a result at another anchor if the applicable reducer law allows it. When the operation establishes a genuinely new analytical quantity, the source anchor may remain constitutive through the new family's identity and lineage.

This is the v6 interpretation of what earlier Frame-QL writing called the "input-anchor/output-anchor" distinction. The distinction remains real; the ontology no longer needs to say that one measure itself carries two current anchors.

# 3. Why Frame-QL has `@` and `AT`

The shipped Manual makes the syntax rule precise:

- `AT {…}` is the **sole query-level output-grain declaration**;
- `@ {…}` is the **input-anchor marker** inside an expression.

Consider:

```frameql
SELECT avg(revenue @ {order}) AS average_order_revenue
AT {region, quarter}
```

`AT {region, quarter}` declares the final output anchor of the frame.

`revenue @ {order}` pins Revenue at Order as the input consumed by `avg`.

Conceptually, the pinned subexpression is the measure:

$$
Revenue@Order.
$$

The syntax role of `@` is nevertheless specific: it supplies an input anchor to the enclosing analytical expression. It does not declare the frame's final output anchor.

Nested expressions make this clearer:

```frameql
SELECT max( sum(revenue @ {transaction}) @ {customer*cal.month} ) AS peak_month
AT {customer}
```

The inner `revenue @ {transaction}` supplies Transaction Revenue to `sum`.

The resulting subexpression is then pinned at `{customer*cal.month}` so that customer-month Revenue becomes the input consumed by `max`.

Finally, `AT {customer}` declares the output anchor of the frame.

The practical rule is therefore:

> **`AT` says where the completed frame is returned. `@` says where an expression must be available when it is consumed by the next operation.**

Not every input anchor must be written. If the shipped planner can determine one unique, immaterial reading under the governed model, it may resolve the omission. Where multiple materially different readings remain, the request is under-specified and the correct shipped outcome is clarification.

This is analytical expressiveness without physical procedure.

# 4. The role of the Manifold

A language can ask only for the result when some other part of the system already knows enough to identify and realize that result.

In Columna, the **Manifold** supplies the governed environment.

The Manifold is one implementation of the broader idea that analytical knowledge can be represented as data rather than reconstructed in every query. Depending on the class of request the implementation supports, it can contain:

- governed names and analytical identities;
- source and requested anchors;
- universe and support information;
- operator and reducer declarations;
- sufficient-state requirements;
- relationship functionality and declared face/allocation rules;
- evidence, provenance, and integrity findings;
- physical bindings and materializations.

In ToD v6 terms, the conceptual question is whether the governed environment contains enough information to establish the requested family identity, source measure, anchor movement, required state, and material support.

A SQL expression describes a procedure. The Manifold represents the governed knowledge against which a Frame-QL request is resolved.

Suppose Revenue is first served from normalized transaction tables and later from a customer-month materialization. The Frame-QL request can remain unchanged:

```frameql
SELECT revenue
AT {customer, cal.month}
```

because the request names the analytical result rather than the current physical realization.

The bounded claim is:

> **A Manifold captures the governed information required to resolve and adjudicate the class of Frame-QL requests the implementation supports.**

It is not the definition of the Theory of Data, and Frame-QL does not require every ToD distinction to be encoded in its current shipped form.

# 5. Analytical identity is independent of storage

Rows, tables, schemas, and joins remain useful forms of representation and execution. Frame-QL places them behind the request boundary.

A physical carrier answers:

> Where can the system obtain these values?

The governed analytical model answers:

> What analytical object are these values supposed to realize?

Frame-QL addresses the second question.

Suppose a product can belong to several categories. A relational join can enumerate product-category pairs. It does not by itself determine what should happen to Product Revenue.

The analysis might require:

- `touch` semantics, where value reaches every match;
- assignment to one declared match;
- allocation across matches;
- filtering at the original product measure;
- or refusal/clarification until an applicable rule is declared.

The current Manual exposes shipped mechanisms for these cases, including the RELATE face semantics and `WITH allocation`. Those are language-specific ways to express governed relationship behavior. The broader principle is independent of the implementation:

> **A join can realize a declared analytical passage; it does not create the passage law merely by existing.**

The same applies to grouping. `AT {customer, cal.month}` declares the output anchor. A physical plan may use `GROUP BY customer, month`, but the grouping expression is an execution mechanism, not the identity of the requested result.

SQL remains important. It simply belongs to a different layer:

> **SQL is declarative about relational processing. Frame-QL is declarative about a governed analytical request.**

# 6. What the statement declares

The complete shipped envelope contains more syntax than this introduction needs to teach. Four elements carry the governing idea.

## 6.1 `FROM` selects the governed environment

```frameql
FROM retail_manifold
SELECT revenue
AT {region}
```

`FROM` names a Manifold, not a physical table. It selects the governed environment in which names, anchors, universes, operator rules, integrity information, and physical bindings are resolved.

The Manual defines exactly when `FROM` may be omitted and how the bound Manifold is represented.

## 6.2 `SELECT` names or constructs result series

```frameql
SELECT revenue, order_count
AT {region, cal.month}
```

A bare governed name can request its corresponding analytical quantity at the frame output anchor when the shipped planner has a unique supported interpretation.

An expression can also construct a result series:

```frameql
SELECT (revenue / order_count) AS average_order_value
AT {region, cal.month}
```

The expression and alias do not, by themselves, establish a new canonical ToD measure-family identity called `AverageOrderValue`.

That distinction matters in Version 6. A stable new family exists only when the governed analytical model establishes the new identity and its lineage. Frame-QL can still return and name an expression under its shipped result rules without pretending that an `AS` alias alone has performed that governance act.

## 6.3 `AT` declares the frame output anchor

```frameql
SELECT revenue
AT {customer, cal.month}
```

`AT` applies to the whole query. It is mandatory, appears once, and declares the final output anchor shared by the result frame.

The Manual is authoritative for the exact anchor grammar, including products and named levels.

## 6.4 Conditions shape the requested frame

```frameql
FROM retail_manifold
SELECT revenue
AT {customer, cal.month}
WHERE order_status = "completed"
```

The condition shapes the requested result. It does not expose a user-authored scan plan.

The planner determines whether the predicate is reachable for the selected expressions under the shipped rules. Other clauses—`HAVING`, `ORDER BY`, `LIMIT … PER`, and `WITH`—likewise have Manual-defined semantics that describe the requested frame without turning the statement into a relational execution script.

# 7. Resolution, analytical adjudication, planning, and execution

The brevity of Frame-QL does not mean the system performs little work. It means the work is assigned to other components.

Conceptually, the shipped planner/engine boundary is closer to:

```text
Frame-QL request
    -> parse / canonicalize / planner validation
       -> clarify / refuse when the request cannot proceed
       -> executable plan when it can
    -> column-engine resolution / computation
       -> serve / disclose
```

The separate `cross_universe` query-error channel and the exact payload of all four shipped moods are defined by the Manual. This introduction does not replace that contract.

The broader architecture can be described using *Analytical Governance*: a user intention is translated into an explicit analytical request; that request must be supportable and analytically established before bounded cost, security, and result/application risks govern execution and serving.

Frame-QL occupies the **request-language boundary** in one such architecture.

It is not the adjudicator itself.

Across the planner and column engine, the shipped implementation determines whether names resolve, required anchors are present, universes are compatible, relationships are traversable, necessary state and support are available, and other implemented obligations hold. The Manual is authoritative about which findings clarify, refuse, serve cleanly, or serve with disclosures.

This distinction also avoids an older overstatement. Frame-QL is not required for analytical governance. A system can independently declare an analytical target and verify candidate SQL against it. Frame-QL is **ToD-native** because its request objects already expose analytical distinctions such as anchor ascription before physical planning.

`EXPLAIN` makes the implementation's resolved reading visible without executing the data request:

```frameql
EXPLAIN
FROM retail_manifold
SELECT revenue
AT {customer, cal.month}
```

That is useful to people and agents because interpretation becomes inspectable before physical execution.

# 8. Same-family reduction, new-family identity, and ordinary result expressions

ToD v6 sharpens a distinction that the earlier Frame-QL Introduction described as "closure."

## 8.1 Same-family reduction

A lawful reducer may move a measure within one coherent family:

$$
Revenue@Transaction
\rightarrow
Revenue@CustomerMonth.
$$

The family stays Revenue if the governed family law licenses the reduction.

The important structural obligations are:

$$
B
\rightarrow
F@B
\rightarrow
B\succ A
\rightarrow
\Gamma(e)
\rightarrow
\text{sufficient state}.
$$

The source anchor must be real; the source measure must exist there; the source must refine the target; the edge must be licensed; and required state must be available.

## 8.2 New-family establishment

Some operations establish a different analytical quantity.

For example, an average begun over orders can establish a family whose identity differs from an average begun over customers. Likewise `MAX` begun at Order differs from `MAX` begun after Revenue has first been formed at Day.

ToD v6 records such family-changing construction in analytical lineage.

Frame-QL can express source-anchor distinctions needed by such operations. The shipped language does not thereby become the complete ToD family-lineage calculus. Whether an expression corresponds to a canonical governed family identity is determined by the governed analytical model, not by the presence of an operator token or `AS` alias.

## 8.3 A computable series need not mint a canonical family

This is an important implementation boundary.

Frame-QL can return a named expression under its shipped rules. The existence of that result series does not imply that a new canonical measure family has automatically been added to the governed ontology.

In compact form:

$$
\text{computable series}
\not\Rightarrow
\text{new governed family identity}.
$$

That keeps query syntax and analytical governance separate.

# 9. Frame-QL as an AI analytical-request boundary

AI agents make this division of responsibility especially useful.

One common pattern is text-to-SQL: a model interprets the question and authors an executable relational program.

Another uses a context or semantic layer to improve the model's understanding.

Another exposes a constrained metric/dimension/filter interface whose compiler owns execution.

Frame-QL represents another architectural choice: the model can propose an **analytical request** rich enough to expose meaning-bearing anchor distinctions while remaining unable to write arbitrary joins, table paths, or physical SQL at the Frame-QL surface.

The important distinction is not that AI must never produce SQL. *Analytical Governance* shows another lawful pattern in which SQL is treated as a candidate realization of an independently established target.

The narrower Frame-QL claim is:

> **If the model is using Frame-QL, the object it authors is an analytical declaration rather than the final physical program.**

That creates a useful separation:

```text
user language
    -> AI interpretation
    -> Frame-QL candidate
    -> governed resolution / adjudication
    -> trusted planning
    -> backend execution
```

The model can search vocabulary, propose anchors, explain alternatives, and ask clarification questions.

It does not become authoritative merely because its proposal is syntactically valid.

> **Model-authored does not mean authorized.**

# 10. Consequences of declaring the output

Once the requested output becomes the unit of declaration, several responsibilities move to more appropriate places.

**Analytical knowledge becomes reusable.**  
Names, anchor relations, support conditions, reducer rules, relationship behavior, and physical bindings can be declared once rather than reconstructed in every query.

**Physical plans become replaceable.**  
A request can remain stable while tables, materializations, engines, and backends change.

**Ambiguity becomes visible.**  
If `avg(revenue)` admits materially different source anchors, the planner can clarify rather than silently selecting one.

**Results become more inspectable.**  
Canonical expressions, resolved anchors/universes, Manifold identity, findings, and provenance can travel with the result under the shipped annotation contract.

**Failure becomes more structural.**  
The system can distinguish an unknown name, missing input anchor, non-functional transport, cross-universe expression, unsupported pin, access refusal, and other documented cases rather than reducing all failure to SQL errors.

These are not incidental benefits of short syntax. They follow from changing what the query is allowed to mean.

# 11. Implementation scope and authority

Frame-QL is one executable language built against a larger analytical theory.

The Theory is broader than the language.

The language is broader than any one backend.

The current implementation supports a defined grammar, operator set, relationship model, outcome vocabulary, canonical form, and annotation contract. Some ToD v6 distinctions are not exposed directly in the shipped Frame-QL surface.

That is acceptable.

A language can implement a sound fragment of a broader theory without implementing all of it.

The governing boundary for this introduction is therefore explicit:

> **The Frame-QL Manual is authoritative for shipped Frame-QL syntax and behavior. The Theory of Data is authoritative for the analytical concepts used to explain why those language distinctions matter.**

Where the two use different vocabulary, this introduction translates between them. It does not rewrite shipped behavior to make the implementation look more theoretically complete than it is.

# 12. Conclusion

Frame-QL begins from a simple consequence of governing analytical data independently of storage.

Revenue is not exhausted by one physical column at one grain.

Under ToD v6, Revenue is a governed measure family. Revenue at a requested anchor is a measure:

$$
Revenue@A.
$$

A Frame-QL query names the governed result it wants, declares the frame output anchor with `AT`, and can pin meaning-bearing source anchors inside expressions with the shipped `@` syntax. The governed environment determines whether the request is known, determinate, supported, and lawful under the implemented rules. Trusted components own physical realization.

That is why Frame-QL contains no query-time joins and no `GROUP BY`. Their absence is not a denial of relational execution. It marks the request boundary between analytical declaration and physical manufacture.

Another query language is not justified by shorter syntax alone. It is justified only if it creates a different boundary.

SQL gives the requester a language for relational processing.

A narrow metric/dimension/filter interface can withhold physical authority but may omit analytical distinctions that matter to a particular request.

Frame-QL is designed for the space between them: expressive about the analytical result, bounded with respect to physical execution.

Its claim remains narrow:

> **The query should contain the information required to identify the analytical result, not the information required to physically manufacture it.**

And for AI-assisted analytics:

> **Give the model enough language to state the analytical distinction. Keep analytical authority and physical execution elsewhere.**

## Implementation and further reading

For a shorter conceptual entry point, see *A Primer on Frame-QL: Why the Result Can Be the Query*. For exact syntax and current behavior, use *The Frame-QL Manual, Second Edition*.

For the current analytical foundation, see:

- Huayin Wang. *The Theory of Data*. Version 6.0. DOI **10.5281/zenodo.21958062**.
- Huayin Wang. *A Primer on the Theory of Data*. Version 2.0. DOI **10.5281/zenodo.21959668**.
- Huayin Wang. *The Theory of Data: An Introduction — Analytical Meaning, Lawful Transformation, and Governed Results*. Version 2.0. DOI **10.5281/zenodo.21960639**.
- Huayin Wang. *The Theory of Data Applied*. Version 1.0. DOI **10.5281/zenodo.21959941**.
- Huayin Wang. *Analytical Governance: From User Intent to Governed Analytical Execution*. Version 1.0. DOI **10.5281/zenodo.21959749**.

This Version 2.1 supersedes *Frame-QL: An Introduction*, Version 2.0, DOI **10.5281/zenodo.21960798**. Version 2.1 corrects the Version 2.0 publication package and contains the intended final reconciled text.
