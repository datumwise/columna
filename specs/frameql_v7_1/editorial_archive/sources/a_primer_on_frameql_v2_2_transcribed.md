---
title: "A Primer on Frame-QL"
subtitle: "Why the Result Can Be the Query"
author: "Huayin Wang"
date: "Version 2.2 - 23 August 2026"
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
**DOI:** 10.5281/zenodo.22071833  
**Previous published version:** Version 2.1, DOI 10.5281/zenodo.22071619

Suppose someone asks:

> **What was average order value by region last quarter?**

Why should that person have to know which warehouse table stores the transactions, which join reaches region, which rows constitute an order, which intermediate aggregate is safe to reuse, and how to write the executable database program?

Frame-QL begins with a separation:

> **The requester should say what analytical result is wanted. A governed system should determine whether that result is established and how it may be produced.**

Frame-QL is a query language for declaring analytical results rather than relational production procedures.

Under the current *Theory of Data*, Revenue is a **measure family**. Revenue at one anchor is a **measure**:

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

The requester does not need to choose.

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

The current *Theory of Data*, Version 6.1, defines the theoretical vocabulary and governing laws of analytical data; the shipped language may retain earlier vocabulary with Manual-defined meanings under its compatibility provision. Advances in the Theory do not enlarge the language, and retained vocabulary does not redefine the Theory; the Manual states this relationship normatively.

# Where the Missing Work Goes

A Frame-QL request is resolved against a **Manifold**, Columna's versioned governed analytical environment.

The Manifold can contain the information needed by the implementation to resolve names, anchors, universes, operator rules, sufficient-state requirements, relationship semantics, support, evidence, and physical bindings.

Conceptually:

```text
user question
    -> interpretation
    -> Frame-QL candidate
    -> governed resolution / adjudication
    -> trusted planning
    -> backend execution
```

Adjudication has four shipped outcomes: the system can serve the result, serve it with disclosures, ask for clarification, or refuse with a stated reason. A syntactically valid request is not guaranteed a number.

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

For the fuller language account, see *Frame-QL: An Introduction — Query by Declaring the Result*, Version 2.2, DOI **10.5281/zenodo.22071508**. For formal syntax, use the Frame-QL grammar; for shipped meaning and behavior, use *The Frame-QL Manual, Second Edition*.

For the analytical foundation and architecture:

- *The Theory of Data*, Version 6.1 — DOI **10.5281/zenodo.22013410**
- *A Primer on the Theory of Data*, Version 2.2 — DOI **10.5281/zenodo.22018549**
- *Introduction to the Theory of Data*, Version 2.2 — DOI **10.5281/zenodo.22018598**
- *Analytical Governance: From User Intent to Governed Analytical Execution*, Version 1.1 — DOI **10.5281/zenodo.22046037**

This Version 2.2 supersedes *A Primer on Frame-QL*, Version 2.1, DOI **10.5281/zenodo.22071619**. Version 2.2 corrects the formal-syntax authority wording to distinguish the Frame-QL grammar from the Manual and updates the companion reference to *Introduction to the Theory of Data*, Version 2.2. Shipped Frame-QL syntax and behavior are unchanged.
