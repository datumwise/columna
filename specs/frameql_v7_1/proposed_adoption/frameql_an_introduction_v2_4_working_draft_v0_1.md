---
title: "Frame-QL: An Introduction"
subtitle: "Query by Declaring the Result"
author: "Huayin Wang"
date: "Proposed Version 2.4 - Working Draft 0.1 - 7 September 2026"
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
**Status:** Working successor for review; not published, no DOI assigned.  
**Predecessor:** Version 2.3, DOI 10.5281/zenodo.22071910.  
**Theory reference:** [ToD v7.1 Full Manuscript Working Draft 0.4](../reviewed_sources/the_theory_of_data_v7_1_full_manuscript_working_draft_v0_4.md).

This draft revises the explanation, not shipped syntax or behavior. The predecessor's Frame-QL code examples are retained unchanged and were not re-executed in this pass.

**Source provenance — three distinct facts, deliberately kept apart.** *During the original editorial pass*, the predecessor was read as public repository text and recorded in the editorial archive as a normalized transcription; direct deposit download was not available to that pass, so its recorded checksums identify that transcription and not the deposited original. *Subsequently, on 7 September 2026*, the repository predecessor source was verified byte-identical to the deposited Markdown artifact; the record IDs, artifact names, checksums, pinned repository paths and verification date are in [the provenance evidence record](PROVENANCE_EVIDENCE.md). That later verification is **not** a claim about what the original pass performed, and it does **not** make this revised successor a byte-identical republication of the deposit — this draft revises the predecessor's explanation. *As to differences*: the transcription of this document introduced three paragraph splits with no word changed; two of them are inherited here and are **retained as editorial changes**, itemised in the evidence record. The verification covers the deposited **Markdown** artifact only.

## Abstract

Frame-QL is a query language for declaring a governed analytical result. The requester names the analytical quantities to be returned, declares the final anchor at which the result frame should exist, and states conditions that shape the request. The requester does not prescribe the relational operations or physical commands used to produce the result.

This working successor explains the language using *The Theory of Data*, Version 7.1, Full Manuscript Working Draft 0.4. A **measure family** is a uniquely governed analytical family such as Revenue. A **measure** is that family at one anchor:

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

Frame-QL has two anchor spellings because the shipped language exposes two different structural responsibilities. Query-level `AT` is mandatory and declares the one final output anchor of the frame. Expression-local `@ {…}` is the shipped input-anchor marker: it pins the anchor at which a subexpression must be available when it is consumed by an enclosing operation.

Conceptually, an expression such as `revenue @ {order}` denotes Revenue at Order for that use, but `@` does not replace `AT` as an output declaration.

This paper develops the central idea of Frame-QL: **the output frame is the query**. It explains why rows, tables, joins, and `GROUP BY` are not primitives of the request interface; how a governed family name and an anchored measure differ from a physical column; how ambiguity becomes clarification rather than silent choice; and why Frame-QL provides a natural analytical-intent boundary for AI-assisted analytics.

The Frame-QL grammar is authoritative for formal syntax. The *Frame-QL Manual, Second Edition* remains authoritative for shipped semantics, canonical form, operators, outcomes, reason codes, implementation terminology, and version-specific behavior. This introduction does not import unshipped Theory of Data features into the language.

The theory reference for this draft is the reviewed v7.1 working manuscript, not a claim that the shipped language implements all of it. The [reconciled language-law candidate](frameql_language_vnext_working_draft_v0_4.md) supplies the companion semantic target. Applicable versioned grammar and shipped references remain the source for released behavior.

## Terminology and scope

This is an introduction to the idea behind Frame-QL, not a grammar reference or a catalogue of every shipped feature. It develops one proposition:

> **A Frame-QL query declares the output data. It does not prescribe the process used to produce it.**

The theory reference uses the following vocabulary:

- **measure family** — a governed analytical family such as Revenue;
- **measure** — that family at one anchor, written $F@A$;
- **anchor** — a governed partition of a universe;
- **reducer** — a lawful contraction from a strictly finer source anchor to a coarser target anchor;
- **sufficient state** — a target-relative relationship among measure families whose measures supply an admitted construction; retained continuation capability remains law-specific;
- **analytical lineage** — constitutive ancestry among measure families.

The shipped Frame-QL / Columna implementation also has its own vocabulary—columns, series, family sets, V/M/B anchors, integrity certificates, and reason codes. Those terms retain their Manual-defined implementation meanings. In particular, this introduction does **not** reinterpret the Manual's V-anchor, M-anchor, and B-anchor as three foundational anchor kinds in the Theory of Data.

The predecessor explained the vocabulary boundary against ToD v6.1. This draft carries that separation forward to the v7.1 working theory: analytical identity and admission come from the selected governed laws; versioned grammar and reference documentation define accepted syntax and shipped behavior. Retained implementation vocabulary is not a theoretical primitive.

Neither direction transfers authority: advances in the Theory do not enlarge the shipped language, and retained implementation vocabulary does not redefine the Theory. The Theory may distinguish analytical structures that the current language does not expose. The applicable grammar and shipped reference remain the boundary for what a released Frame-QL version accepts and does.

The language is concise because responsibility has been divided, not because the omitted work has disappeared.

# 1. The result is the query

Consider a request for revenue by customer and month:

```frameql
FROM retail_manifold
SELECT revenue
AT {customer, cal.month}
```

The surface is deliberately familiar. A SQL-literate reader can see a source, a selected quantity, and an output location. But the statement is not a compressed relational program.

Under the retained family/measure distinction, `revenue` is a governed family name. `AT {customer, cal.month}` declares the final anchor of the requested frame. Where the governed model establishes the family and the lawful path, the requested analytical object is:

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

Version 7.1 retains one **current** anchor per measure. An operation consumes a source measure at its source anchor and produces a result at another anchor if the applicable reducer law allows it. When the operation establishes a genuinely new analytical quantity, the source anchor may remain constitutive through the new family's identity and lineage.

The input-anchor/output-anchor distinction remains real: the constitutive input can change which family is requested, while the final anchor locates its present measure. It does not give one measure two current anchors.

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

Not every input anchor must be written. A governed single-valued completion can resolve an omission when it determines one analytical meaning. Several identity-distinct readings require clarification; having only one executable plan does not select the user's intent. Two adequate bases for the same fixed target are instead alternative ways to answer one question. The applicable release reference specifies which completions the shipped planner supports.

This is analytical expressiveness without physical procedure.

# 4. The role of the Manifold

A language can ask only for the result when some other part of the system already knows enough to identify and realize that result.

In Columna, the **Manifold** supplies the governed environment.

The Manifold is one implementation of the broader idea that analytical knowledge can be represented as data rather than reconstructed in every query. The authored Manifold is logical-only. Its governing definitions can identify:

- governed names and analytical identities;
- source and requested anchors;
- universe and support information;
- analytical-law declarations and admitted movements;
- sufficient-state requirements;
- relationship functionality and declared face/allocation rules;
- the logical contracts whose evidence must be established.

The broader serving environment also needs private physical bindings, applicable evidence and certification, and available materializations. Those facts have distinct roles. The privileged realization boundary combines the logical publication with its private mapping; physical bindings do not create analytical meaning.

The conceptual question is whether the selected model and its applicable evidence establish the requested identity and a lawful available construction. A retained result need not retain the sufficient state required for every later use.

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

The applicable reference and profile state which relationship mechanisms are available, including their exact face or allocation surfaces. This working introduction does not enlarge that coverage. The broader principle is independent of the implementation:

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

`FROM` names a Manifold, not a physical table. It selects the governed environment for analytical resolution. Private bindings and current evidence are combined with its logical definitions only by the authorized realization components.

The Manual defines exactly when `FROM` may be omitted and how the bound Manifold is represented.

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

The Frame-QL grammar is authoritative for the formal anchor syntax, including products and named levels; the Manual is authoritative for the shipped meaning and behavior of those anchor forms.

## 6.4 Conditions shape the requested frame

```frameql
FROM retail_manifold
SELECT revenue
AT {customer, cal.month}
WHERE order_status = "completed"
```

The condition restricts the request's input under its declared formation scope; it does not expose a user-authored scan plan. `HAVING` selects already-formed output, while `ORDER BY` and `LIMIT` order or select the frame. A restriction must not silently re-form an already-constituted contextual quantity under a different context.

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

That keeps query syntax and analytical governance separate. Canonical denotation of a family under an admitted analytical law is not a new publication act, and an `AS` label is not an admission rule.

## 8.4 Governed order and retained capability

Version 7.1 withdraws Version 7.0's categorical exclusion of analytical-point-order-dependent families. A complete governed order may be constitutive of a family law whose sufficient-state combination remains invariant to evidence enumeration. For compound support, complete point orders within its constituent anchors and declared precedence induce the order over the analytical points that actually exist.

FIRST/LAST illustrates the distinction. The witness-valued family W retains the selected constitutive point and its value; the scalar family L can be constructed by taking that value. A witness may support admitted continuation even when its displayed scalar cannot. The optional retained point–value family R is another sufficient basis, not a mandatory storage stage. These are mathematical family names, not new Frame-QL syntax.

A stored scalar LAST, a retained witness, and a scalar established without identifying a winner are not interchangeable materializations. The artifact must say what it retains, which claim is established and why, and what reuse is justified. A scalar-only argument requires adequate evidence; the particular constant-value example in T requires a fixed law, known nonemptiness, exhaustive possible-participant coverage, and supported equal values at every possible winner.

None of this certifies a legacy `.last` implementation or prescribes its replacement syntax. General focal operations such as LAG and rolling still need their contextual contracts. They do not gain continuation merely by being named, and contextual formation does not categorically bar a separately admitted family.

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
Canonical expressions, resolved anchors/universes, Manifold identity, findings, and provenance can travel with the result under the shipped annotation contract.

**Failure becomes more structural.**  
The system can distinguish an unknown name, missing input anchor, non-functional transport, cross-universe expression, unsupported pin, access refusal, and other documented cases rather than reducing all failure to SQL errors.

These are not incidental benefits of short syntax. They follow from changing what the query is allowed to mean.

# 11. Implementation scope and authority

Frame-QL is one executable language built against a larger analytical theory.

The Theory is broader than the language.

The language is broader than any one backend.

The current implementation supports a defined grammar, operator set, relationship model, outcome vocabulary, canonical form, and annotation contract. The reviewed v7.1 target goes beyond what this introduction can claim for a particular shipped build.

That is acceptable.

A language can implement a sound fragment of a broader theory without implementing all of it.

The governing boundary for this introduction is therefore explicit:

> **The Frame-QL grammar is normative for shipped syntax. The Frame-QL Manual is authoritative for shipped behavior, outcomes, and canonical form. The Theory of Data is authoritative for the analytical concepts used to explain why those language distinctions matter.**

This working edition translates analytical concepts while retaining the released syntax boundary. The [language-law candidate](frameql_language_vnext_working_draft_v0_4.md) describes the reconciled semantic target; Core/Platform profiles state authored obligations, and build-status records report measured coverage. Neither is a blanket proof of v7.1 conformance. No capability promise or generated measurement is changed by this introduction.

# 12. Conclusion

Frame-QL begins from a simple consequence of governing analytical data independently of storage.

Revenue is not exhausted by one physical column at one grain.

Under the Theory of Data, Revenue is a governed measure family. Revenue at a requested anchor is a measure:

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

For the shorter companion in this review set, see [*A Primer on Frame-QL*, proposed Version 2.3, Working Draft 0.1](a_primer_on_frameql_v2_3_working_draft_v0_1.md). Its published predecessor is Version 2.2, DOI 10.5281/zenodo.22071833.

The fixed analytical reference is [*The Theory of Data*, Version 7.1, Full Manuscript Working Draft 0.4](../reviewed_sources/the_theory_of_data_v7_1_full_manuscript_working_draft_v0_4.md). It is not a published edition and has no confirmed assigned DOI in this packet. Version 7.0, DOI 10.5281/zenodo.22289091, and Version 6.1, DOI 10.5281/zenodo.22013410, remain historical publications under their own versioned positions.

For the reconciled technical account, use [Language-Law Candidate 0.4](frameql_language_vnext_working_draft_v0_4.md) and its [authority index](frameql_v7_1_authority_and_supersession_index_v0_1.md). For actual formal syntax and released behavior, use the applicable grammar, language reference, profiles, and build record. These working documents do not enlarge the shipped language.

Other useful published companions remain *A Primer on the Theory of Data* v2.2 (10.5281/zenodo.22018549), *Introduction to the Theory of Data* v2.2 (10.5281/zenodo.22018598), *The Theory of Data Applied* v1.0 (10.5281/zenodo.21959941), and *Analytical Governance* v1.1 (10.5281/zenodo.22046037). Their publication versions remain explicit; they are not all silently relabeled v7.1.

**Revision note.** This proposed Version 2.4 succeeds the explanation in Version 2.3, DOI 10.5281/zenodo.22071910, for review purposes only. It updates the theory reference, separates logical definition from realization, clarifies family denotation and target resolution, and adds a bounded order/reuse explanation. All predecessor `frameql` code blocks are retained unchanged. No example was rerun and no syntax, outcome, implementation, repository, or publication was changed.
