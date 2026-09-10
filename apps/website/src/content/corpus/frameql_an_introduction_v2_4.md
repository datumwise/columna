---
title: "Frame-QL: An Introduction"
subtitle: "Query by Declaring the Result"
author: "Huayin Wang"
date: "Version 2.4 - 8 September 2026"
version: "2.4"
doi: "10.5281/zenodo.22661455"
license: "CC BY 4.0"
lang: en-US
papersize: letter
geometry: margin=0.82in
fontsize: 11pt
subject: "An introduction to Frame-QL as a storage-independent query language for governed analytical results"
keywords:
  - Frame-QL
  - analytical query language
  - storage-independent query language
  - analytical data ontology
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
**DOI:** [10.5281/zenodo.22661455](https://doi.org/10.5281/zenodo.22661455)  
**Supersedes:** Version 2.3, DOI [10.5281/zenodo.22071910](https://doi.org/10.5281/zenodo.22071910).  
**Analytical foundation:** *The Theory of Data*, Version 7.1, DOI [10.5281/zenodo.22649945](https://doi.org/10.5281/zenodo.22649945).

This paper explains Frame-QL's analytical design. It is not a complete grammar, an adoption announcement for proposed syntax, or a conformance report for a software release. The fourteen query examples are retained from the preceding edition and have not been re-executed for this edition.

## Abstract

Frame-QL is a **storage-independent query language** for declaring a governed analytical result. The requester names the analytical quantities to be returned, declares the final anchor at which the result frame should exist, and states conditions that shape the request. The requester does not prescribe the relational operations or physical commands used to produce the result.

This storage independence rests on the published *Theory of Data*, Version 7.1: a theory of analytical data whose identity and laws are defined independently of physical storage. A **measure family** is a uniquely governed analytical family such as Revenue. A **measure** is that family at one anchor:

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

Frame-QL uses two anchor spellings for different structural responsibilities. Query-level `AT` is mandatory and declares the one final output anchor of the frame. Expression-local `@ {…}` pins the anchor at which a subexpression is to be established for use by an enclosing operation.

Conceptually, an expression such as `revenue @ {order}` denotes Revenue at Order for that use, but `@` does not replace `AT` as an output declaration.

This paper develops the central idea of Frame-QL: **the output frame is the query**. It explains why rows, tables, joins, and `GROUP BY` are not primitives of the request interface; how a governed family name and an anchored measure differ from a physical column; how ambiguity becomes clarification rather than silent choice; and why Frame-QL provides a natural analytical-intent boundary for AI-assisted analytics.

ToD defines analytical identity and lawful transformation. The Frame-QL specification defines how a request expresses that meaning, through its versioned grammar and semantics. Implementations separately demonstrate their coverage. Language design need not wait for implementation, and implementation behavior cannot redefine the analytical target.

## Terminology and scope

This is an introduction to the idea behind Frame-QL, not a complete grammar reference or a release capability catalog. It develops one proposition:

> **A Frame-QL query declares the output data. It does not prescribe the process used to produce it.**

The theory reference uses the following vocabulary:

- **measure family** — a governed analytical family such as Revenue;
- **measure** — that family at one anchor, written $F@A$;
- **anchor** — a governed partition of a universe;
- **reducer** — a lawful contraction from a strictly finer source anchor to a coarser target anchor;
- **sufficient state** — a target-relative relationship among measure families whose measures supply an admitted construction; retained continuation capability remains law-specific;
- **analytical lineage** — constitutive ancestry among measure families.

A language specification can adopt a sound expression of a ToD law before a particular engine implements it. That adoption is a language-design decision: its syntax, meaning, and validity conditions must be specified and reviewed. Publication of a new theory edition does not automatically choose a new grammar, and parser acceptance does not establish analytical validity.

An implementation manual has a different responsibility. It should explain the intended semantics, what the identified release implements, what remains unimplemented, and where actual behavior differs. An unsupported capability need not be an invalid analytical request; an accepted expression need not be a conforming realization.

The examples use the established Frame-QL envelope and anchor notation. They illustrate the declared result, assuming the named quantities, anchors, and relevant contracts are governed. They are not evidence that every backend supports the depicted request.

The language is concise because responsibility has been divided, not because the omitted work has disappeared.

# 1. The result is the query

Consider a request for revenue by customer and month:

```frameql
FROM retail_manifold
SELECT revenue
AT {customer, cal.month}
```

The surface is deliberately familiar. A SQL-literate reader can see a source, a selected quantity, and an output location. But the statement is not a compressed relational program.

Under the family/measure distinction, `revenue` is a governed family name. `AT {customer, cal.month}` declares the final anchor of the requested frame. Where the governed model establishes the family and the lawful path, the requested analytical object is:

$$
Revenue@\{Customer,Month\}.
$$

The statement does not name a transaction table. It does not identify a customer key, choose a date column, write a join, specify a grouping procedure, or decide whether the result should come from detail, a materialization, a cache, or an external service. It does not assume that the backend is relational.

The request can still be precise at the analytical level. It states what analytical quantity is wanted and where the result must live.

The core division of responsibility is:

> **The requester declares the result. The governed system owns the derivation.**

# 2. Measure families and requested measures

The Version 5 vocabulary used **measure** for the family and **member** for one governed realization at an analytical location. Version 6 introduced, and Version 7.1 preserves, the distinction:

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

A frame is important to the language because it is the requested result container. It is not a new foundational analytical identity parallel to measure family or measure.

The selected fields may denote governed measures or other analytical expressions admitted by the language, with their analytical status made explicit. The frame assembles them for one requested output location.

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

Version 7.1 retains one **current** anchor per measure. An operation consumes a source measure at its source anchor and produces a result at another anchor if the applicable reducer law allows it. When the operation establishes a genuinely new analytical quantity, the source anchor may remain constitutive through the new family's identity and lineage.

The input-anchor/output-anchor distinction remains real: the constitutive input can change which family is requested, while the final anchor locates its present measure. It does not give one measure two current anchors.

# 3. Why Frame-QL has `@` and `AT`

The two syntax roles are:

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

Not every input anchor must be written. A governed single-valued completion can resolve an omission when it determines one analytical meaning. Several identity-distinct readings require clarification; having only one executable plan does not select the user's intent. Two adequate bases for the same fixed target are instead alternative ways to answer one question. The language specification determines which completions are admitted; an implementation reference reports which of them its release supports.

This is analytical expressiveness without physical procedure.

# 4. The role of the Manifold

Declaring a result does not remove the knowledge needed to interpret it or the evidence needed to establish it. Frame-QL leaves that work to the governed analytical model and the realization environment.

A **Manifold** is a versioned, **governed analytical data model** against which the request is resolved. It is an **analytical data ontology** for a particular domain under ToD: it identifies the analytical objects and laws of that domain. It is also a **storage-independent data model**, because its logical definitions remain separate from the physical bindings used to realize them.

ToD supplies the theory of analytical data; a Manifold supplies a particular governed model under that theory. The Manifold represents analytical definitions as data rather than reconstructing them in every query. Those definitions identify:

- governed names and analytical identities;
- source and requested anchors;
- universe and support information;
- analytical-law declarations and admitted movements;
- sufficient-state requirements;
- relationship functionality and declared face/allocation rules;
- the logical contracts whose evidence must be established.

The broader serving environment also needs private physical bindings, applicable evidence and certification, and available materializations. Those facts have distinct roles. The privileged realization boundary combines the logical publication with its private mapping; physical bindings do not create analytical meaning.

The conceptual question is whether the selected model and its applicable evidence establish the requested identity and a lawful available construction. A retained result need not retain the sufficient state required for every later use.

A SQL expression states relational computation. The Manifold represents the governed analytical definitions against which a Frame-QL request is resolved.

Suppose Revenue is first served from normalized transaction tables and later from a customer-month materialization. The Frame-QL request can remain unchanged:

```frameql
SELECT revenue
AT {customer, cal.month}
```

because the request names the analytical result rather than the current physical realization.

The bounded claim is:

> **A Manifold supplies the governed analytical definitions needed to interpret a request. Current evidence and implementation coverage determine whether a particular realization can establish the result.**

The model does not define ToD itself. Nor does the set of requests an engine can currently execute define what the model or language is allowed to express.

# 5. Analytical identity is independent of storage

ToD defines analytical objects and their lawful transformations independently of physical representation. That gives Frame-QL the foundation for a storage-independent request: it names the analytical result rather than a storage structure. Rows, tables, schemas, and joins remain useful forms of representation and execution, behind the request boundary.

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

The analytical construction must specify which contribution rule applies. The language specification determines how that choice can be expressed; an implementation manual reports supported forms and remaining gaps. The principle is:

> **A join can realize a declared analytical passage; it does not create the passage law merely by existing.**

The same applies to grouping. `AT {customer, cal.month}` declares the output anchor. A physical plan may use `GROUP BY customer, month`, but the grouping expression is an execution mechanism, not the identity of the requested result.

SQL remains important. It simply belongs to a different layer:

> **SQL is declarative about relational processing. Frame-QL is declarative about a governed analytical request.**

# 6. What the statement declares

The Frame-QL envelope contains more syntax than this introduction needs to teach. Four elements carry the governing idea.

## 6.1 `FROM` selects the governed environment

```frameql
FROM retail_manifold
SELECT revenue
AT {region}
```

`FROM` names a Manifold, not a physical table. It selects the governed environment for analytical resolution. Private bindings and current evidence are combined with its logical definitions only by the authorized realization components.

The applicable language specification defines when `FROM` may be omitted in favor of a bound Manifold. The implementation reference describes how a particular interface supplies that binding.

## 6.2 `SELECT` names or constructs result series

```frameql
SELECT revenue, order_count
AT {region, cal.month}
```

A bare governed name resolves the intended family in the selected namespace. Whether evidence and a realization are available for that quantity is a separate question.

An expression can also construct a result series:

```frameql
SELECT (revenue / order_count) AS average_order_value
AT {region, cal.month}
```

The expression and alias do not, by themselves, establish a new canonical ToD measure-family identity called `AverageOrderValue`.

The distinction remains in v7.1. A complete admitted canonical family construction can denote analytical identity without a separate business name. A ratio can also be governed explicitly as an AOV family. But neither arithmetic syntax nor an output alias supplies a missing target specification or family law, and naming an output is not publishing or ratifying a definition.

## 6.3 `AT` declares the frame output anchor

```frameql
SELECT revenue
AT {customer, cal.month}
```

`AT` applies to the whole query. It is mandatory, appears once, and declares the final output anchor shared by the result frame.

The versioned Frame-QL grammar specifies the formal anchor syntax, including products and named levels. Its semantic specification says what those forms denote; a release reference reports their implemented coverage and any differences.

## 6.4 Conditions shape the requested frame

```frameql
FROM retail_manifold
SELECT revenue
AT {customer, cal.month}
WHERE order_status = "completed"
```

The condition restricts the request's input under its declared formation scope; it does not expose a user-authored scan plan. `HAVING` selects already-formed output, while `ORDER BY` and `LIMIT` order or select the frame. A restriction must not silently re-form an already-constituted contextual quantity under a different context.

Resolution must establish that the predicate has an admitted interpretation for the selected expressions. Whether a particular engine can realize that lawful restriction is a separate question. The language specification defines the other clauses—`HAVING`, `ORDER BY`, `LIMIT … PER`, and `WITH`—without turning the statement into a relational execution script.

# 7. Resolution, analytical adjudication, planning, and execution

The brevity of Frame-QL does not mean the system performs little work. It means the work is assigned to other components.

The conceptual responsibilities are:

```text
Frame-QL request
    -> resolve the analytical target and meaning-bearing choices
    -> establish the premises needed by an admitted construction
    -> choose and authorize a faithful available realization
    -> execute, preserving that resolved meaning
    -> return the result with its justified qualifications
```

These are responsibilities, not a mandatory one-pass execution schedule. Evidence checks may themselves require computation. When intent is ambiguous, the system asks for clarification. When an analytical premise or required realization is unavailable, it must report that limitation rather than silently choose another quantity. Exact outcome payloads, reason codes, and error channels belong to the applicable language and interface contracts.

The broader architecture can be described using *Analytical Governance*: a user intention is translated into an explicit analytical request; that request must be supportable and analytically established before bounded cost, security, and result/application risks govern execution and serving.

Frame-QL occupies the **request-language boundary** in one such architecture.

It is not the adjudicator itself.

A conforming realization must preserve the selected family identities, anchor and universe meanings, relationship contracts, and the evidence and state requirements of the chosen construction. Implementations may support different subsets of these constructions. Their references must distinguish an unresolved meaning, an unestablished premise, and an unsupported implementation path instead of collapsing them into one failure.

This distinction also avoids an older overstatement. Frame-QL is not required for analytical governance. A system can independently declare an analytical target and verify candidate SQL against it. Frame-QL is **ToD-native** because its request objects already expose analytical distinctions such as anchor ascription before physical planning.

`EXPLAIN` makes the resolved reading and proposed realization inspectable before the data request is executed:

```frameql
EXPLAIN
FROM retail_manifold
SELECT revenue
AT {customer, cal.month}
```

That is useful to people and agents because interpretation becomes inspectable before physical execution. A data-free explanation does not, by itself, establish every data-dependent support condition or disclosure. The resolved meaning, applicable assurance, proposed plan, and remaining checks must remain distinguishable.

# 8. Same-family reduction, new-family identity, and ordinary result expressions

The Theory of Data distinguishes family-preserving continuation, family formation, and ordinary analytical expressions. Version 7.1 makes the conditions for these judgments explicit rather than deciding them from operator names.

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

The source anchor must be real; the source measure must exist there; the source must refine the target; the edge must be licensed; and required state must be available for this particular continuation. Failure of this plan to obtain an intermediate state does not exclude another adequate derivation of the same target.

## 8.2 New-family establishment

Some operations establish a different analytical quantity.

For example, an average begun over orders can establish a family whose identity differs from an average begun over customers. Likewise `MAX` begun at Order differs from `MAX` begun after Revenue has first been formed at Day.

Constitutive analytical lineage records such family-changing construction. Alternative proof methods or faithful execution paths to the already specified target do not create new identities.

Frame-QL can express the source-anchor distinctions needed by such operations. A family construction is admitted only under the complete ToD contract: a specified target and formation, governed participation and exceptional cases, adequate sufficient-state bases, and coherent continuation over its admitted anchors. An operator token or `AS` alias cannot supply missing law (ToD v7.1, §§3–5).

## 8.3 A computable series need not mint a canonical family

This is a distinction between expression semantics and family admission.

Frame-QL can return an expression under an output key. The existence of that result series does not imply that a new canonical measure family has automatically been added to the governed model.

In compact form:

$$
\text{computable series}
\not\Rightarrow
\text{new governed family identity}.
$$

That keeps query syntax and analytical governance separate. Canonical denotation of a family under an admitted analytical law is not a new publication act, and an `AS` label is not an admission rule.

## 8.4 Governed order and retained capability

Version 7.1 withdraws Version 7.0's categorical exclusion of analytical-point-order-dependent families. A complete governed order may be constitutive of a family law whose sufficient-state combination remains invariant to evidence enumeration. For compound support, complete point orders within its constituent anchors and declared precedence induce the order over the analytical points that actually exist.

FIRST/LAST illustrates the distinction. Suppose an established daily stock series is 10, 20, and 15 in chronological order. LAST is 15, while MAX is 20. The former selects an analytical point by chronology; the latter selects a value by magnitude. Changing the order in which the evidence arrives must change neither result.

The witness-valued family W retains the selected constitutive point and its value; the scalar family L can be constructed by taking that value. A witness may support admitted continuation even when its displayed scalar cannot. The optional retained point–value family R is another sufficient basis, not a mandatory storage stage. The operand must first be established at its constitutive anchor: several carrier rows beneath one analytical point are not competing candidates for LAST. These are mathematical family names, not new Frame-QL syntax (ToD v7.1, §§7–8).

A stored scalar LAST, a retained witness, and a scalar established without identifying a winner are not interchangeable materializations. The artifact must say what it retains, which claim is established and why, and what reuse is justified. A scalar-only argument requires adequate evidence; the particular constant-value argument in ToD v7.1 §9.6 requires a fixed law, known nonemptiness, exhaustive possible-participant coverage, and supported equal values at every possible winner.

These analytical constructions can guide Frame-QL design before an engine supports them. Neither an existing `.last` spelling nor a particular execution path is thereby certified. The language must specify how the governed order is selected; an arbitrary physical sorting convention cannot create it. Output `ORDER BY` only orders the returned frame and does not supply the inner analytical order.

General focal operations such as LAG and rolling still need their contextual contracts. They do not gain continuation merely by being named, and contextual formation does not categorically bar a separately admitted family. Preserving the original formation matters: recomputing a predecessor relation independently inside new groups may change the quantity rather than continue it (ToD v7.1, §§3.3–3.4 and 12.4).

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
Names, anchor relations, analytical laws, and relationship contracts can be governed once rather than reconstructed in each request. Their private physical mappings and current evidence remain separately maintained.

**Physical plans become replaceable.**  
A request can remain stable while tables, materializations, engines, and backends change.

**Ambiguity becomes visible.**  
If `avg(revenue)` admits materially different source anchors, the planner can clarify rather than silently selecting one.

**Results become more inspectable.**  
Canonical expressions, resolved anchors and universes, model identity, findings, and provenance can accompany the result under an explicit interface contract. The implementation reference must state which information it actually exposes.

**Failure becomes more structural.**  
The analytical model distinguishes an unknown name, an unresolved input anchor, an unlicensed relationship, a universe mismatch, unavailable evidence, and an unsupported realization. A release should report these differences rather than reducing every failure to a SQL error.

These are not incidental benefits of short syntax. They follow from changing what the query is allowed to mean.

# 11. Language design and implementation coverage

ToD is independent research. Frame-QL is a language design aligned with its analytical definitions and laws. Columna is an implementation whose coverage must be described separately. The direction of authority is from analytical law to language meaning to realization—not from existing code back into the definition of the quantity.

A construct may enter an adopted Frame-QL specification when its syntax, meaning, and validity conditions have been specified, reviewed, and adopted. An implementation may support it later. A new ToD construction does not automatically choose that syntax, and a working language proposal must remain labeled as proposed until its design is adopted.

The responsibilities are distinct:

| Responsibility | What it establishes |
|---|---|
| **ToD** | Analytical objects, family laws, sufficient-state relationships, and the premises of derivability and consistency |
| **Frame-QL specification** | Versioned grammar, expression and request meanings, resolution, and validity conditions aligned with those laws |
| **Implementation profile** | The capabilities and obligations a particular implementation undertakes |
| **Implementation evidence and manual** | What a release actually realizes, what remains partial or unimplemented, and where behavior differs from the specification |

An implementation manual, including the Columna manual, should state both the intended semantics and the release's relationship to them. An unimplemented requirement belongs in the manual with its status made clear; it must not disappear from the language to make the implementation look complete. A known deviation is documented as a deviation, not adopted silently as the intended meaning.

An unsupported construct and a nonconforming result are different. A system can decline a lawful request that it cannot realize. Accepting the syntax and returning a result that violates its admitted meaning is not equivalent to lacking support.

A useful capability entry therefore identifies the governing specification, implemented scope, and remaining limitations. Profiles are promises; measured build records are evidence of coverage; neither is itself proof of the complete analytical contract.

This introduction states the design and illustrates existing notation. It neither adopts unresolved extension syntax nor certifies a particular build. Concrete implementation evidence may expose a real ambiguity or counterexample in the design; the mere absence of code is not such a counterexample.

# 12. Conclusion

Frame-QL is a storage-independent query language because its requests are grounded in a storage-independent theory of analytical data. ToD defines the analytical objects and laws; a Manifold constitutes a governed analytical data model under those laws; Frame-QL declares the result wanted from that model.

Revenue is not exhausted by one physical column at one grain.

Under the Theory of Data, Revenue is a governed measure family. Revenue at a requested anchor is a measure:

$$
Revenue@A.
$$

A Frame-QL query names the governed result it wants, declares the frame output anchor with `AT`, and can pin meaning-bearing source anchors inside expressions with `@`. The governed model determines the analytical meaning and applicable laws. Current evidence and available realizations determine whether the request can be answered. Trusted components own physical execution.

That is why Frame-QL contains no query-time joins and no `GROUP BY`. Their absence is not a denial of relational execution. It marks the request boundary between analytical declaration and physical manufacture.

Another query language is not justified by shorter syntax alone. It is justified only if it creates a different boundary.

SQL gives the requester a language for relational processing.

A narrow metric/dimension/filter interface can withhold physical authority but may omit analytical distinctions that matter to a particular request.

Frame-QL is designed for the space between them: expressive about the analytical result, bounded with respect to physical execution.

Its claim remains narrow:

> **The query should contain the information required to identify the analytical result, not the information required to physically manufacture it.**

And for AI-assisted analytics:

> **Give the model enough language to state the analytical distinction. Keep analytical authority and physical execution elsewhere.**

## References and further reading

The analytical reference is Wang, Huayin, *The Theory of Data: A Foundation for Analytical Identity, Derivability, and Consistency*, Version 7.1. DOI: [10.5281/zenodo.22649945](https://doi.org/10.5281/zenodo.22649945). The preceding discussion draws particularly on §§2–5 (identity, formation, and bases), §§7–10 (order, evidence, and reuse), and §12.4 (request languages).

For accessible introductions to the published foundation:

- Wang, Huayin. *A Primer on the Theory of Data*. Version 2.3. DOI: [10.5281/zenodo.22651578](https://doi.org/10.5281/zenodo.22651578).
- Wang, Huayin. *The Theory of Data: An Introduction — Analytical Meaning, Lawful Transformation, and Governed Results*. Version 2.3. DOI: [10.5281/zenodo.22651777](https://doi.org/10.5281/zenodo.22651777).

For the neighboring governance argument, see Wang, Huayin, *Analytical Governance: From User Intent to Governed Analytical Execution*, Version 1.1. DOI: [10.5281/zenodo.22046037](https://doi.org/10.5281/zenodo.22046037). It retains its own publication scope. *The Theory of Data Applied*, Version 1.0, DOI [10.5281/zenodo.21959941](https://doi.org/10.5281/zenodo.21959941), supplies further worked context under its stated edition.

The published shorter Frame-QL companion is *A Primer on Frame-QL: Why the Result Can Be the Query*, Version 2.3, DOI [10.5281/zenodo.22661076](https://doi.org/10.5281/zenodo.22661076).

For formal syntax and complete language semantics, consult the applicable versioned Frame-QL specification. For Columna release coverage, unsupported cases, and deviations, consult its implementation manual, profiles, and measured build documentation. Those documents have different responsibilities (§11).

**Revision note.** Version 2.4 succeeds Version 2.3 and aligns its explanation with the published Theory of Data v7.1. It preserves the result-declaration argument and all fourteen query examples while clarifying the Manifold descriptions and the storage-independent theory–model–query relationship. Publication of this introduction changes neither shipped behavior nor the adoption status of proposed language constructs.
