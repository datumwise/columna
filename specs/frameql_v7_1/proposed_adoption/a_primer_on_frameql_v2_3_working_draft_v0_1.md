---
title: "A Primer on Frame-QL"
subtitle: "Why the Result Can Be the Query"
author: "Huayin Wang"
date: "Proposed Version 2.3 - Working Draft 0.1 - 7 September 2026"
lang: en-US
papersize: letter
geometry: margin=0.9in
fontsize: 11pt
subject: "An accessible introduction to Frame-QL as an expressive and governed analytical-request boundary"
keywords:
  - Frame-QL
  - analytical query language
  - AI agents
  - text-to-SQL
  - semantic layer
  - input anchor
  - output anchor
  - Theory of Data
  - governed analytics
  - measure family
  - measure
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
    \linespread{0.97}
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
    \fancyhead[L]{\small A Primer on Frame-QL}
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
**Predecessor:** Version 2.2, DOI 10.5281/zenodo.22071833.  
**Theory reference:** [ToD v7.1 Full Manuscript Working Draft 0.4](../reviewed_sources/the_theory_of_data_v7_1_full_manuscript_working_draft_v0_4.md).

This draft updates the conceptual explanation, not shipped syntax or behavior. The three predecessor Frame-QL examples are retained unchanged and were not re-executed.

**Source provenance — three distinct facts, deliberately kept apart.** *During the original editorial pass*, the complete public source was read and recorded in the editorial archive as a normalized transcription, whose recorded checksums identify that transcription and not the deposited original. *Subsequently, on 7 September 2026*, the repository predecessor source was verified byte-identical to the deposited Markdown artifact, and the transcription itself was found byte-identical to that verified source — so for this document the normalization was a no-op. Details, checksums and the verification date are in [the provenance evidence record](PROVENANCE_EVIDENCE.md). That later verification is **not** a claim about what the original pass performed, and it does **not** make this revised successor a byte-identical republication of the deposit. The verification covers the deposited **Markdown** artifact only.

Suppose someone asks:

> **What was average order value by region last quarter?**

Why should that person have to know which warehouse table stores the transactions, which join reaches region, which rows constitute an order, which intermediate aggregate is safe to reuse, and how to write the executable database program?

Frame-QL begins with a separation:

> **The requester should say what analytical result is wanted. A governed system should determine whether that result is established and how it may be produced.**

Frame-QL is a query language for declaring analytical results rather than relational production procedures.

Under the *Theory of Data*, whose v7.1 working manuscript is the reference for this draft, Revenue is a **measure family**. Revenue at one anchor is a **measure**:

$$
Revenue@A.
$$

That makes a Frame-QL request unusually literal.

# The Result Can Be the Query

Consider:

```frameql
FROM retail_manifold
SELECT revenue
AT {customer, cal.month}
```

The statement does not name a transaction table, choose a foreign key, write a join, or say `GROUP BY customer, month`.

It declares the governed environment, the requested analytical quantity, and the final output anchor.

Conceptually, it asks for:

$$
Revenue@\{Customer,Month\}.
$$

The physical result might come from transaction detail, a verified materialization, a cache, an API, or another backend.

The requester does not need to choose the physical source. The system must still establish that the available representation is adequate for the requested quantity and use. A cached average, for example, need not retain the sums and counts required for another exact aggregation.

> **Frame-QL is short because responsibility has moved, not because analytical work has disappeared.**

# Why Output Dimensions Are Not Always Enough

Suppose a governed model establishes Revenue at three source anchors—Order, Line, and Customer—and each source measure reconciles to the same **$250** region-quarter total. There are three orders, six sale lines, and two customers.

The same region-quarter can then support three mechanically correct averages:

- over **orders**: $250/3 = **$83.33**;
- over **lines**: $250/6 = **$41.67**;
- over **customers**: $250/2 = **$125.00**.

The final output anchor is the same.

What changed is the source measure consumed by the average:

$$
Revenue@Order,
\qquad
Revenue@Line,
\qquad
Revenue@Customer.
$$

So a request shape such as:

```text
metric: average_revenue
dimensions: [region, quarter]
```

is sufficient only if `average_revenue` already names one complete governed analytical identity. If the analytical distinction still depends on what is being averaged, the request needs a way to state that distinction or the system must ask.

> **Safety should not be achieved by deleting distinctions that belong to analytical meaning.**

Two different adequate ways to compute one specified average are not two different questions. Conversely, when order-level and customer-level averages remain distinct possible meanings, having data for only one does not tell the system which one the user intended.

# Why Frame-QL Has `@` and `AT`

The shipped language gives the two responsibilities different syntax.

`AT {…}` is the mandatory final output anchor of the frame.

`@ {…}` is the expression-local **input-anchor pin**.

For example:

```frameql
SELECT avg(revenue @ {order})
AT {region, quarter}
```

reads:

> average **Revenue at Order**, returned at Region-Quarter.

Changing the pin changes the question:

```frameql
SELECT avg(revenue @ {customer})
AT {region, quarter}
```

The two queries have the same final output anchor and need not denote the same analytical quantity.

The current Theory of Data no longer says that one measure itself carries two current anchors. A measure has one current anchor. The Frame-QL `@` pin identifies the source measure consumed by the next operation; `AT` identifies where the completed result frame is returned.

That is a cleaner theoretical explanation of the same shipped syntax.

> **`AT` says where the frame is returned. `@` says where an expression must exist when the next operation consumes it.**

The Frame-QL grammar is authoritative for formal syntax. The *Frame-QL Manual, Second Edition* remains authoritative for shipped meaning and behavior.

This draft uses the v7.1 working theory for analytical identity and law. A complete admitted canonical construction can denote a family without a separate business name. An output alias does not supply a missing family law or publish a definition.

Version 7.1 also admits FIRST/LAST families under complete governed analytical-point order and the required sufficient-state law; a scalar LAST answer is not automatically reusable witness state. That theoretical admission does not certify a legacy `.last` implementation. The fuller Introduction explains this distinction without adding syntax here.

Advances in the theory do not enlarge the shipped language, and retained implementation vocabulary does not redefine the theory. The [working language-law candidate](frameql_language_vnext_working_draft_v0_4.md) is the reconciled semantic target; released behavior remains governed by the applicable reference and profile.

# Where the Missing Work Goes

A Frame-QL request is resolved against a **Manifold**, Columna's versioned governed logical analytical model. It supplies names, anchors, universes, analytical laws, and relationship contracts.

The broader serving environment combines that logical publication with separate private physical mappings, applicable evidence, and available materializations. The authored Manifold does not contain physical database bindings as analytical law. Mapping realizes the declared meaning; it does not create it.

Conceptually:

```text
user question
    -> interpretation
    -> Frame-QL candidate
    -> governed resolution / adjudication
    -> trusted planning
    -> backend execution
```

The referenced language presents four serving outcomes: serve, disclose, clarify, and refuse. Exact reason codes, errors, and availability remain version-specific. A syntactically valid request is not guaranteed a number; disclosure does not repair a computation whose analytical premises were never established.

The request language does not need to expose the physical tables and joins because those are not what the requester is declaring.

The physical plan may still contain SQL. Frame-QL does not make relational databases disappear.

It moves physical manufacture behind the analytical request boundary.

# Why This Matters for AI

AI makes the boundary especially visible.

A model is useful for interpreting ordinary language, searching vocabulary, proposing candidate anchors, and asking clarification questions.

Those abilities do not make the model analytically authoritative.

Frame-QL lets a model propose a bounded analytical declaration rather than requiring it to author the final physical program.

That is one useful architecture, not the only possible one. *Analytical Governance* shows that an independently established analytical target can also be paired with candidate SQL and verified before execution.

Frame-QL's narrower advantage is that the request object itself is already shaped around analytical distinctions.

> **Model-authored does not mean authorized.**

# Why Another Query Language?

SQL already exists. Semantic layers already expose governed metrics. Why introduce another query language?

Because another language is justified only when it creates a different boundary.

SQL is declarative about relational processing.

A narrow metric/dimension/filter interface can be safe and effective when the metric name already contains the complete analytical identity.

Frame-QL is designed for requests where the analytical distinction itself must remain expressible—especially source-anchor distinctions—without giving the requester arbitrary physical authority.

The reason is compact:

> **The query should contain the information required to identify the analytical result, not the information required to physically manufacture it.**

# Where to Go Next

For the fuller account in this review set, see [*Frame-QL: An Introduction*, proposed Version 2.4, Working Draft 0.1](frameql_an_introduction_v2_4_working_draft_v0_1.md). Its published predecessor is Version 2.3, DOI 10.5281/zenodo.22071910.

The governing comparison text is [*The Theory of Data*, Version 7.1, Full Manuscript Working Draft 0.4](../reviewed_sources/the_theory_of_data_v7_1_full_manuscript_working_draft_v0_4.md); it remains unpublished. The [companion authority index](frameql_v7_1_authority_and_supersession_index_v0_1.md) identifies the active technical drafts. Exact accepted syntax and shipped behavior remain in the applicable grammar and language reference; profiles and measured build records keep their separate roles.

The published ToD v7.0 (10.5281/zenodo.22289091), ToD Primer v2.2 (10.5281/zenodo.22018549), ToD Introduction v2.2 (10.5281/zenodo.22018598), and Analytical Governance v1.1 (10.5281/zenodo.22046037) retain their own edition scope.

**Revision note.** This proposed Version 2.3 updates the Version 2.2 Primer's theoretical and authority explanation while retaining its section order, central argument, three Frame-QL examples, and numerical averaging example. It is not a language release or a published replacement. No examples were rerun in this pass.
