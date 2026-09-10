---
title: "A Primer on Frame-QL"
subtitle: "Why the Result Can Be the Query"
author: "Huayin Wang"
date: "Version 2.3 - 8 September 2026"
version: "2.3"
doi: "10.5281/zenodo.22661076"
license: "CC BY 4.0"
lang: en-US
papersize: letter
geometry: margin=0.9in
fontsize: 11pt
subject: "An accessible introduction to Frame-QL as a storage-independent query language for governed analytical results"
keywords:
  - Frame-QL
  - analytical query language
  - storage-independent query language
  - analytical data ontology
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
**DOI:** [10.5281/zenodo.22661076](https://doi.org/10.5281/zenodo.22661076)  
**Supersedes:** Version 2.2, DOI [10.5281/zenodo.22071833](https://doi.org/10.5281/zenodo.22071833).  
**Analytical foundation:** *The Theory of Data*, Version 7.1, DOI [10.5281/zenodo.22649945](https://doi.org/10.5281/zenodo.22649945).

This is a conceptual introduction, not a complete grammar or a release-conformance report. The three Frame-QL examples have not been re-executed for this edition.

Suppose someone asks:

> **What was average order value by region last quarter?**

Why should that person have to know which warehouse table stores the transactions, which join reaches region, which rows constitute an order, which intermediate aggregate is safe to reuse, and how to write the executable database program?

Frame-QL begins with a separation:

> **The requester should say what analytical result is wanted. A governed system should determine whether that result is established and how it may be produced.**

Frame-QL is a **storage-independent query language** for declaring analytical results. Its requests describe analytical quantities and locations rather than the tables, joins, or physical commands used to produce them.

This is possible because the *Theory of Data* defines analytical data independently of storage. It establishes what a quantity is, where it lives, and which transformations preserve its meaning without making a physical representation the source of that meaning. Frame-QL expresses requests in terms of that foundation.

Under the published *Theory of Data*, Version 7.1, Revenue is a **measure family**. Revenue at one anchor is a **measure**:

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

Assume the declared averaging laws include all those points and their Revenue values are supported. The same region-quarter can then support three different averages:

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

Frame-QL gives the two responsibilities different syntax.

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

A measure has one current anchor. The Frame-QL `@` pin identifies the source measure consumed by the next operation; `AT` identifies where the completed result frame is returned. When the source anchor changes the quantity being formed, it belongs to that new family’s identity—not to a second current anchor.

> **`AT` says where the frame is returned. `@` says where an expression must exist when the next operation consumes it.**

ToD establishes analytical identity and law; the Frame-QL specification states how requests express them. A complete admitted construction can denote a family without a separate business name. An output alias does not supply a missing law or publish a definition.

Version 7.1 also admits FIRST/LAST families under a complete governed order over analytical points and an adequate sufficient-state law. With chronological stock values 10, 20, and 15, LAST is 15 while MAX is 20. Retaining just 15 can lose the selecting day required for further LAST continuation. Knowing an answer and retaining what is needed for another use are different achievements.

Language design does not have to wait for an engine to implement it. Its syntax and meaning still need explicit specification and adoption. Implementation manuals should then state which parts are supported, which remain unimplemented, and where the release behaves differently. An implementation gap must not silently become a restriction on the language's meaning.

# Where the Missing Work Goes

A Frame-QL request is resolved against a **Manifold**: a versioned, **governed analytical data model**. It is an **analytical data ontology** for a particular domain, defining its universes, anchors, measure families, and governing laws under ToD. It is also a **storage-independent data model**: its definitions describe analytical meaning, not a physical database layout.

ToD supplies the general theory; a Manifold supplies a particular governed model under it. Frame-QL expresses a request against that model.

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

A governed response may provide a result, disclose a justified limitation, ask for clarification, or refuse an unestablished computation. Exact response forms and implementation coverage belong in their applicable specifications and manuals. A valid request is not guaranteed an available answer; disclosure does not repair a computation whose analytical premises were never established.

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

Frame-QL makes those analytical distinctions expressible—especially source-anchor distinctions—without giving the requester arbitrary physical authority. Its storage independence rests on the model and laws that give the request meaning, not merely on hiding a table name.

The reason is compact:

> **The query should contain the information required to identify the analytical result, not the information required to physically manufacture it.**

# Where to Go Next

For the fuller language argument, the published *Frame-QL: An Introduction — Query by Declaring the Result*, Version 2.3, is available at DOI [10.5281/zenodo.22071910](https://doi.org/10.5281/zenodo.22071910). The paper edition is not a software-release number.

The current analytical foundation is *The Theory of Data*, Version 7.1, DOI [10.5281/zenodo.22649945](https://doi.org/10.5281/zenodo.22649945). Two published companions offer shorter routes into it: *A Primer on the Theory of Data*, Version 2.3, DOI [10.5281/zenodo.22651578](https://doi.org/10.5281/zenodo.22651578), and *The Theory of Data: An Introduction*, Version 2.3, DOI [10.5281/zenodo.22651777](https://doi.org/10.5281/zenodo.22651777).

For the governance architecture discussed above, see *Analytical Governance: From User Intent to Governed Analytical Execution*, Version 1.1, DOI [10.5281/zenodo.22046037](https://doi.org/10.5281/zenodo.22046037), under that work's own edition scope.

Use the applicable Frame-QL specification for complete syntax and meaning. Use a Columna release manual for its implemented coverage and differences. Neither a shorter explanation nor a passing execution replaces the analytical contract.

**Revision note.** Version 2.3 updates the Version 2.2 Primer against published ToD v7.1. It retains the section progression, three Frame-QL examples, numerical averaging example, and LAST-versus-MAX illustration. It makes Frame-QL’s storage independence and its foundation in ToD explicit, and describes a Manifold as a governed analytical data model, an analytical data ontology, and a storage-independent data model. It preserves the separation between language design and implementation coverage. Publication of this paper does not by itself adopt new syntax or establish implementation conformance. The query examples have not been re-executed for this edition.
