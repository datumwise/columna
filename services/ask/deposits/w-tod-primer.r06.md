---
title: A Primer on the Theory of Data
author: Huayin Wang
version: '2.3'
date: Version 2.3 — 7 September 2026
doi: 10.5281/zenodo.22651578
license: CC BY 4.0
lang: en-US
subject: An accessible first reading of the Theory of Data, aligned with Version 7.1
papersize: letter
geometry: left=0.85in,right=0.85in,top=0.8in,bottom=0.8in
fontsize: 11pt
keywords:
- Theory of Data
- analytical data
- datum
- universe
- anchor
- measure family
- analytical identity
- sufficient state
- analytical order
- materialization
---


**datumwise, an independent open-source research project**  
**DOI:** [10.5281/zenodo.22651578](https://doi.org/10.5281/zenodo.22651578)  
**License:** Creative Commons Attribution 4.0 International (CC BY 4.0)  
**Supersedes:** *A Primer on the Theory of Data*, Version 2.2, DOI [10.5281/zenodo.22018549](https://doi.org/10.5281/zenodo.22018549).  
**Aligned with:** *The Theory of Data*, Version 7.1, DOI [10.5281/zenodo.22649945](https://doi.org/10.5281/zenodo.22649945).

A theory of data can sound unnecessary. We already work with data: we put it in tables, calculate totals, compare results, and make charts. What is left to explain?

Consider a report containing two daily averages. Each average can be correct while their average gives the wrong answer for the whole period. Or consider a missing sales record. It might mean no sale occurred, or that a sale occurred and its evidence was lost. The arithmetic and the storage format cannot settle either question by themselves.

The Theory of Data starts with those distinctions. It asks what a quantity is about, which points it describes, and what makes a later calculation a valid use of it. Tables and query languages remain useful. The analytical meaning is something they must preserve, rather than something they create merely by producing a number.

This primer follows the published Version 7.1. It introduces the ideas through familiar examples; the foundation supplies their full definitions and proofs. Here, **governed** means that the relevant definitions and rules are explicit and have authority for the analysis. Evidence must still establish their applicable premises. Writing down a rule does not make its mathematics or its inputs correct.

# From a Value to a Datum

Imagine finding `42` written on a scrap of paper. You have a value, but you do not know what it represents. It could be an age, a temperature, a quantity, or an identifier. Even sensible arithmetic depends on which it is.

Now write `John's age = 42 years`, with John and the relevant observation identified. The value has become an assertion about something. The Theory calls a typed value at an analytical point a **datum**.

The point is what the value describes. It might identify a person, a transaction, or one store on one day. A key can encode that point, and a table row can carry the value, but neither tells the entire analytical story.

> **Data is always something about something else.**

This is the starting question to keep asking as the examples grow: what, exactly, is this value about?

# From Datums to Analytical Location

Revenue for January and Revenue for February describe different analytical points. Revenue for one store in January is more specific again.

The Theory calls the structure organizing these locations an **anchor**. `Month` is an anchor when it supplies the governed monthly groups. `{Store, Month}` identifies the store–month groups. In ordinary language, the anchor answers “Revenue for what?”

The notation `Revenue@Month` means Revenue at the Month anchor. The `@` reads as “at”; it is analytical notation here, not a command for a particular program.

Before we can define an anchor fully, however, we need to settle something earlier: which points are there to organize?

# From Analytical Location to a Universe

Suppose a report uses store–day coordinates. Does its analytical world contain only days on which sales occurred, or every day the store was scheduled to open?

These are different **universes**. A universe states what makes its root points exist. The Theory calls that rule its **existence law**.

In a transaction universe, a point may exist because a qualifying transaction occurred. In an operating-calendar universe, an open store-day exists because the calendar declares it, independently of a sales observation. The root is relative to that analytical world: a daily state can be a starting point in one universe, while another models individual events.

This makes an absent record a question rather than an answer. A missing sales row does not establish that no sale occurred. Accepted evidence that a particular transaction record was lost can establish the event's existence even though its amount is unavailable. On an operating-calendar day, no sales might justify zero only when the applicable evidence and rule establish that conclusion.

We therefore keep apart a point that does not exist, an existing point where a quantity does not apply, a missing value for an applicable quantity, and a supported value of zero. A database may encode several of these in the same way. The analytical meaning is different. [1, §2.3]

# Anchors Are Partitions

An anchor is a **partition of the universe**: it divides the root points into non-overlapping groups, with each root point in exactly one group. Those groups are the anchor's analytical points.

If each sale belongs to one store and one month, `{Store, Month}` organizes the sales accordingly. It does not create every conceivable store–month combination. Only the points established by the universe contribute to that partition.

Some anchors fit inside others. Each Day can belong to one Month, so daily Revenue can contribute to monthly Revenue under its additive law. Other anchors do not nest: a calendar week can cross a month boundary. Weekly totals alone do not generally tell us the exact monthly totals.

Overlap raises a different issue. A product can belong to several categories. Joining those memberships to its Revenue does not create permission to count that Revenue repeatedly. A rule must establish whether the analysis uses one assigned category, apportions contribution, or deliberately measures memberships. Those choices can all be useful, but they describe different quantities.

# From a Measure to a Measure Family

We can now put the two parts of an analytical reference together. The **measure family** specifies the quantity and its law. The **anchor** specifies its current analytical location. A **measure** is the family at that anchor:

\[
\boxed{\text{measure}=\text{measure family}@\text{anchor}.}
\]

Revenue at Month and Revenue at `{Store, Month}` are different measures of one Revenue family when the same definition and its admitted laws apply. The family is more than the word “Revenue.” Its definition must specify the target quantity, what contributes to it, and how its measures may be constructed and continued.

A useful declaration might specify sales revenue net of returns, in a particular currency, attributed by the declared sale date. Another definition may be legitimate but different. The name helps us refer to the quantity; it does not replace that definition.

A family can also be referred to through its construction. `mean(revenue@Order)` can identify average order-level Revenue under a complete admitted MEAN law. A separate business name is optional. Merely writing the expression does not establish missing definitions or evidence.

# Identity Comes Before Comparison

Two reports both displaying `100` have not thereby established the same analytical object. One may include tax and the other exclude it. A maximum of individual sales and a maximum of daily sales totals might happen to agree this month and diverge next month.

The definitions determine whether the reports claim the same quantity. Only then do we ask whether their results should agree. For exact results, agreement is required when both derivations establish the same measure under compatible evidence and satisfied contracts. Different dates of extraction, populations, or definitions cannot be ignored just because both columns have the same heading.

This is why identity matters before a discrepancy appears. It tells us which comparisons are meaningful and which differences are legitimate. It also prevents a system from responding to disagreement by quietly declaring that the calculations must have meant different things.

# Displayed Value Is Not Always Sufficient State

Consider the average revenue per order over two days. All three orders in this example are known and their Revenue is supported under the same definition:

| Day | Revenue total | Order count | Revenue per order |
|---|---:|---:|---:|
| Day 1 | 100 | 1 | 100 |
| Day 2 | 300 | 2 | 150 |

Averaging the displayed daily averages gives 125. The average over the three orders is instead:

\[
\frac{100+300}{1+2}=\frac{400}{3}\approx133.33.
\]

The daily averages lost the weights. Keeping the totals and counts preserves the information needed for this calculation.

The Theory calls such information **sufficient state for the target**. In v7.1 it is carried by ordinary measures: SUM and COUNT families can supply a basis for MEAN. There is no mysterious second kind of data hiding behind the average. There are other analytical quantities whose established values are enough to construct it.

Exact distinct count illustrates the same distinction. Two groups can each contain three customers without their union containing six. Retaining the customer identity sets allows an exact union and count; retaining only the two cardinalities generally does not. A set can be the value of one measure. Its elements do not become that measure's reporting anchor.

Sufficiency is also specific to a use. State adequate for combining an average is not automatically adequate for filtering the original observations. And a correct displayed answer can still be stored and used as that answer, even when the state for a different calculation has not been retained. [1, §§5, 10.7]

# From Structure to Transformation

Some transformations preserve analytical location. Calculating a ratio from two supported, compatible quantities at the same anchor is one example. Other operations combine finer points into coarser ones. In the Theory, these shapes are called a **mapper** and a **reducer** respectively. Shape alone does not determine what quantity the result represents.

For additive Revenue, summing the same correctly accounted sales directly to Month must agree with first summing them to Day and then to Month, under the applicable laws. The intermediate grouping changes the work, not the target. The Theory calls this **family coherence**.

That is a conditional result. It assumes the same contributions, their proper multiplicity, compatible evidence, and the required state. A correct formula does not turn a lost input into zero, and a possible route does not guarantee that the information needed to execute it is available.

## When “last” has an analytical meaning

Consider a fixed store with exactly three participating daily stock observations in one year:

| Analytical day | Stock |
|---|---:|
| 30 January | 10 |
| 31 January | 20 |
| 1 February | 15 |

Under declared chronological order, the latest day's value is 15. The greatest stock value is 20. LAST orders the **analytical points**; MAX compares the **values**.

To continue LAST through monthly summaries, one sufficient representation keeps the winning day with its value. January retains `(31 January, 20)`; February retains `(1 February, 15)`. Comparing the retained days selects February's 15 regardless of the order in which those summaries arrive.

Version 7.1 establishes FIRST and LAST families under a complete analytical law of this kind. The retained point-and-value is called a **witness**. Such witnesses are the values of an ordinary measure family; projecting their operand values supplies the scalar results. They generally retain continuation information that the scalars alone lose.

For a multidimensional anchor, such as `{Customer, Day}`, the construction also needs an order within each constituent dimension and a declared precedence among the dimensions. Chronology alone does not establish which customer comes first. These definitions govern analytical order; physical row order supplies none of them.

If the latest eligible day's value is unavailable, the same LAST definition cannot silently retreat to an earlier observation. Conversely, if all participating days are known and the latest value is supported, unavailable earlier values need not prevent LAST. Those earlier values would still matter to a SUM. Evidence requirements follow the requested quantity. [1, §§7–9]

# When a New Family Is Established

An operation sometimes changes the question rather than continuing the same quantity. Suppose two days contain order revenues `6, 4` and `7, 0`. The largest order is 7. Daily Revenue totals are 10 and 7, so the largest daily Revenue is 10.

The difference is where MAX begins. `max(revenue@Order)` and `max(revenue@Day)` can denote different families even when both are reported at Month. The input anchor helps specify **what is being compared**; the output anchor says **where the result is reported**. The measure still has one current anchor.

The Theory records this meaning-bearing ancestry as **analytical lineage**. It records how a family was constituted, rather than every execution step that happened to produce it. Staging an unchanged Revenue sum through Day does not create another Revenue identity. Forming a maximum over daily totals does create a different quantity when its law establishes that family.

A family therefore governs the measures that belong to one analytical quantity. Lineage explains where a new quantity came from. Keeping both makes it possible to distinguish a different calculation of the same target from a calculation of a different target.

# A Neighboring Question: Regime

Analytical structure is not the whole explanation of a result. Observed Revenue, forecast Revenue, and Revenue under a proposed intervention can concern the same customer and period while making different claims. The value-generation arrangement is often called a **regime**; it is identity-bearing where changing it changes the declared quantity.

Evidence and statistical inference have related but separate jobs. A correctly constructed average over a known dataset does not by itself justify a claim about next year or a wider population. That further claim needs its own assumptions and evidence.

Approximation is another distinct question. An estimate may target the same exact customer count as an exact calculation, while establishing less about its value. Its error guarantee and retained capabilities must remain explicit. Using the same target name does not make the estimate exact, and a different approximation method does not automatically create another quantity. [1, §§1.5, 10.9, 12.5]

# The Vision

The practical goal is to make analytical data identifiable before a program chooses how to produce it. A person can ask for a quantity at an anchor. A system can then determine which definitions apply, whether the required evidence is available, and which realizations preserve the intended result.

This requires business knowledge and evidence; it does not replace them. The research provides a common structure in which those definitions and obligations can be stated. A table, semantic model, query language, or analytical engine can use that structure without becoming its source of authority.

The key distinction is between **knowing an answer** and **having enough retained information for another use**. A stored average may be a perfectly good answer at its original anchor without being a valid input to an average of a larger population. The remedy is to preserve or obtain the information the next law needs, not to declare the original answer meaningless.

ToD gives those questions explicit objects: a universe, an anchor, a measure family, a measure, and lawful constructions among them. That is the foundation for asking not only whether a number can be computed, but what it establishes and what may be done with it next.

# References and reading path

**[1]** Wang, Huayin. *The Theory of Data: A Foundation for Analytical Identity, Derivability, and Consistency*. Version 7.1, 7 September 2026. Zenodo. DOI: [10.5281/zenodo.22649945](https://doi.org/10.5281/zenodo.22649945). This is the governing foundation for the explanations in this primer.

**Predecessor:** Wang, Huayin. *A Primer on the Theory of Data*. Version 2.2. Zenodo. DOI: [10.5281/zenodo.22018549](https://doi.org/10.5281/zenodo.22018549).

## Revision note

Version 2.3 preserves the v2.2 teaching path from values through analytical location, universes, partitions, families, identity, retained information, transformation, lineage, and neighboring questions. It replaces obsolete version-specific explanations with the published v7.1 account and adds numerical examples for averages and ordered selection. It leaves proof details, representation schemas, and implementation coverage to their proper references. The new examples are illustrations of the cited laws, not empirical observations or newly admitted family laws.
