---
title: "A Primer on the Theory of Data"
author: "Huayin Wang"
date: "Version 2.2 - 19 August 2026"
lang: en-US
papersize: letter
geometry: margin=0.9in
fontsize: 11pt
subject: "An accessible primer to the Theory of Data foundational framework"
keywords:
  - Theory of Data
  - analytical data
  - governed analytical data
  - analytical identity
  - datum
  - measure family
  - measure
  - anchor
  - universe
  - existence law
  - sufficient state
  - analytical lineage
  - lawful transformation
  - certification
---

**datumwise, an independent open-source research project**

**Version 2.2 — DOI pending publication assignment**

**Supersedes:** *A Primer on the Theory of Data*, Version 2.1, DOI 10.5281/zenodo.21995124

**Aligned with:** *The Theory of Data: A Foundation for Analytical Identity, Derivability, and Consistency*, Version 6.1, DOI 10.5281/zenodo.22013410

A foundational framework for analytical data can be difficult to enter. Even the "gentle introduction" I wrote assumed too much. Readers did not begin by debating its definitions; they asked more basic questions: What is it for? Why should I read it? What problem is it trying to solve?

Those questions revealed the real starting point. Before the theory can be introduced, the subject itself must be made strange again. So let us begin with the thing we think we already understand: data.

Ask someone what comes to mind when they hear the phrase *theory of data*. The reaction is often puzzlement. The phrase sounds unnecessary. After all, everyone works with data. Surely we already know what it is.

Press for an answer and familiar objects appear: tables, rows, columns, cells, and SQL. This is understandable. These are the things we see and manipulate every day. But they are not yet an account of data itself.

A table is a container. Rows and columns are an arrangement within that container. SQL is a language for manipulating the arrangement. Numbers and strings are representations used to store values. All are useful, but none tells us what makes a data object exist, what gives it meaning, or which transformations preserve that meaning.

That is the territory of a theory of data.

# From a Value to a Datum

Imagine finding the number `42` written on a scrap of paper. Have you found data? Not yet. You have found a value, but not meaningful information. Is 42 an age, a quantity, a temperature, a price, an identifier, or an error code? You do not know what it is a value of, so you do not yet know what it means or what may legitimately be done with it.

Now add a type: `age = 42`, and a subject key: `John's age = 42`. The symbol has become an assertion about something. That binding - between a typed analytical point and a typed value - is the crucial act.

Call this smallest meaningful assertion a **datum**: one typed value at one analytical point. A datum is not merely `42`, and not just an age type. It is `42` presented as the answer to a particular question about a particular thing.

This gives us our first principle:

> **Data is always something about something else.**

# From Datums to Analytical Location

Consider revenue reported for January, February, and March. The values do not float freely. Each belongs somewhere analytically: January revenue, February revenue, March revenue.

The Theory calls the governed partition that supplies such analytical locations an **anchor**.

An anchor can be simple or compound. Revenue may be evaluated by month, by store, or by the pair `{store, month}`. The anchor answers an indispensable question:

> Revenue for what?

For the moment, it is enough to think of an anchor as the governed structure that tells us where a measure lives. Once we introduce the universe, we can say this more precisely: an anchor is a partition of the points that exist in that universe.

Now the outline of data begins to appear without reference to a storage container: typed assertions organized around explicit analytical locations.

# From Analytical Location to a Universe

An anchor tells us how existing points are grouped. It does not tell us which points exist in the first place.

Suppose the analytical coordinates are `{store, day}`. Does every possible store-day exist? Only days on which a sale occurred? Every day the store was open? Every contractual reporting day?

Those are different analytical worlds even though the displayed coordinates look the same.

The Theory calls such a governed analytical world a **universe**. A universe establishes a root-point domain under an explicit **existence law**: the rule that determines what makes a point exist in that universe.

Two especially useful forms of existence law are easy to recognize.

- Under an **occurrence-based** existence law, points exist because occurrences happened and were recorded. Transaction and shipment universes are common examples.
- Under a **declared or generated** existence law, points can exist independently of whether a particular value was observed. Registered customers, scheduled visits, store-days, reporting periods, and future forecast dates are common examples.

These are often described as event and spine universes.

The distinction is compact:

> **Events generate points. Spines establish points and await values.**

This is why a missing row is not self-interpreting. In an occurrence-based universe, absence may mean that no governed point was generated. On a spine, the point may still exist even when the requested value is unavailable.

# Anchors Are Partitions

Once the universe has established which points exist, an anchor partitions those points into analytical locations.

A partition matters because every root point belongs to exactly one block of that anchor. This is what makes ordinary aggregation over an anchor meaningful: the analytical points do not overlap merely because a join or grouping expression happened to produce rows.

For example, `{store, month}` may partition the relevant universe into store-month points. A product-to-category relationship, by contrast, does not automatically define a category anchor if one product may belong to several categories. Overlapping groups are not a partition merely because SQL can `GROUP BY` them after a join.

This gives the anchor a stronger role than "grain" alone. It is not just a description of columns. It is governed analytical geometry.

# From a Measure to a Measure Family

We can now return to revenue.

Suppose `Revenue` is a governed analytical quantity. Revenue at month is one analytical object; Revenue at store is another; Revenue at `{store, month}` is another.

Version 6 writes these objects directly:

\[
Revenue@Month
\]

\[
Revenue@Store
\]

\[
Revenue@\{Store,Month\}.
\]

A **measure family** is a governed analytical family. `Revenue` is the governed name by which we refer to one such family. A **measure** is that family at one anchor.

The compact identity is:

\[
\boxed{Measure = MeasureFamily @ Anchor}
\]

or simply:

\[
F@A.
\]

This wording replaces the older distinction between a *measure* and its anchored *members*. Version 6 retires **member** from the core ontology. The family is the **measure family**; the anchored governed object is the **measure**.

This is more than a renaming. It makes ordinary analytical reference direct. `Revenue@Month` is not a secondary member hanging below Revenue. It is the Revenue measure at the Month anchor.

Different measures in one family may still be related by the family's law. Revenue by store and month may lawfully reduce to revenue by month or revenue by store under an additive family law. But being in the same family does not mean every anchor is reachable from every other anchor. Week and month, for example, may be incomparable partitions even though both support Revenue measures.

# Identity Comes Before Comparison

Suppose two calculations both display `100`. Have we shown that they are the same data object?

No. One may be Revenue before tax and another after tax. One may count an overlapping relationship differently. One may have been formed by taking a maximum over orders while another takes a maximum over days. Their values happen to agree, but they answer different analytical questions.

This gives Version 6.1 an important operational principle:

> **Two numbers can agree and still be different data objects; analytical identity is established by what the quantity means and how it is governed, not by whether today's values happen to match.**

Identity therefore comes before comparison. Once two derivations claim the same governed measure, the family's law and satisfied contracts can require them to agree. Agreement is evidence about the consistency of an identity already claimed; it does not create that identity.

This is the same lesson we encountered at the beginning. A value becomes data only by being about something. A governed analytical quantity likewise becomes a particular data object through its declared analytical meaning, location, law, and lineage.

# Displayed Value Is Not Always Sufficient State

A measure may display one value while requiring more state for lawful continuation.

Suppose a daily average is displayed as `42`. Averaging several displayed daily averages does not generally recover the exact overall average. Exact continuation requires the underlying sufficient state:

\[
(sum,count).
\]

Likewise, the displayed cardinality of an exact distinct count is not enough to continue exact distinct counting across overlapping groups; the identities already counted are part of the required state.

This gives an important distinction:

\[
\boxed{
\text{displayed value}
\neq
\text{sufficient state}
\neq
\text{analytical identity}
}
\]

The value is what may be shown. Sufficient state is what may be needed for lawful continuation. Analytical identity tells us what measure the state belongs to.

# From Structure to Transformation

So far this world looks static: it contains datums, universes, anchors, measure families, and measures. Data work, however, is dynamic. Values are transformed, reduced, aligned, restricted, and sometimes moved into newly established analytical quantities.

The agents of these transformations are governed **operators**.

Two primary value operators are especially useful.

A **mapper** changes values while preserving the anchor.

A **reducer** contracts a measure from a strictly finer anchor to a coarser one under a governed reducer law.

For example, if `{store, day}` is strictly finer than `{month}`, a lawful reducer may establish a movement from a measure at the finer anchor to a measure at the coarser anchor. But the fact that two columns can be grouped together in SQL does not establish that such a reduction is lawful.

This is where familiar rules such as "do not sum inventory through time" become more precise. The issue is not merely that Inventory carries a special `stock` label. The issue is whether the particular reduction from its source anchor to its requested target anchor is licensed under the family's law and contracts.

Each governed transformation therefore carries analytical obligations: the source object must exist, the target must be meaningful, the anchor relation must be lawful where reduction is claimed, and the required contracts and sufficient state must be satisfied.

Ordinary pipelines encode physical execution through SQL, dataframes, and processing logic. The Theory lifts the analytical obligations out of those containers and represents them directly.

A join is not a semantic primitive merely because SQL spells it `JOIN`. A successful calculation is not sufficient evidence that the output preserves the same analytical identity.

# When a New Family Is Established

Not every lawful operation stays inside one measure family.

Suppose we begin with daily Revenue and ask for the maximum daily Revenue in a month. The `MAX` operation does not simply produce another Revenue measure. It establishes a different analytical quantity:

\[
Revenue@Day
\rightsquigarrow
MaxDailyRevenue@Day.
\]

`MaxDailyRevenue` is a new measure family. Its identity remembers where that family was established, because beginning `MAX` at order, day, or store-day can produce different quantities.

This is why identity matters. `MaxOrderRevenue` and `MaxDailyRevenue` may both eventually be reported at month, yet they are not two inconsistent calculations of one measure. They are different measure-family identities. Their governed names help keep that distinction visible; the distinction itself comes from how the families were established.

The Theory records such constitutive ancestry in governed **analytical lineage**.

One useful visual picture is to imagine measure families as clouds. Inside one cloud are the measures of that family at lawful anchors. Directed connections between clouds record how new families were established from existing ones.

The image is only a metaphor, but it captures an important distinction:

> **A measure family governs local analytical coherence. Lineage governs where analytical identities come from.**

# A Neighboring Question: Regime

Once analytical objects and their lawful transformations are explicit, another class of questions comes into view:

> Under what value-generation arrangement does a quantity or claim hold?

For causal, policy, and simulation problems, that distinction may matter even when the universe and anchor remain unchanged. An observed quantity and an intervention target can describe the same population at the same analytical location while differing in how values would be generated.

The broader research program calls this value-generation arrangement a **regime**. Observational and interventional regimes are common examples.

Regime is important, but it is not another kind of anchor or measure family. It is a neighboring structural distinction needed when an analysis moves beyond ordinary analytical derivation into claims about how values arise under different arrangements.

The same is true of evidence status, provenance, and statistical interpretation. These questions matter greatly, but they should not be collapsed into the smaller foundation needed to establish analytical identity and lawful transformation.

# The Vision

Where does this lead?

The Theory of Data offers an ontology of the analytical data world that is independent of storage details. It makes analytical objects and lawful operations explicit and, where the required law is declared, verifiable.

A query can therefore become a declaration of what governed analytical result is wanted rather than merely a procedural account of how tables must be joined to obtain it.

This is not a replacement for business semantic knowledge that defines concepts such as customer, campaign, or revenue. It supplies a logical foundation beneath and across such knowledge: what analytical points exist, how they are partitioned, what measure exists at an anchor, how sufficient state is preserved, which transformations remain inside one family, and when a new analytical identity must be established.

That separation suggests an architectural opportunity. If analytical objects and analytical law can be represented independently of both storage and business vocabulary, they can provide a stable, machine-adjudicable foundation for analytics and AI systems.

The same foundation also connects naturally to neighboring work on missingness, statistical analysis, causal identification, analytical governance, and query languages that declare governed analytical results rather than physical procedures.

The practical ambition is compact:

> **Know which analytical points exist, where a measure lives, which governed family identity it carries, what state its lawful continuation requires, how its family was established, and which transformations preserve that identity.**

# Project references

- Huayin Wang. *The Theory of Data: A Foundation for Analytical Identity, Derivability, and Consistency*. Version 6.1, 2026. DOI: [10.5281/zenodo.22013410](https://doi.org/10.5281/zenodo.22013410).
- Huayin Wang. *A Primer on the Statistical Bridge: Why Statistical Analysis Is Neither Pure Mathematics nor Data Processing*. Version 1.0, 2026. DOI: [10.5281/zenodo.21864434](https://doi.org/10.5281/zenodo.21864434).
- Huayin Wang. *The Statistical Bridge: From Events to Spines, Data Work, and the Interpretation of Results*. Version 1.2, 2026. DOI: [10.5281/zenodo.21863411](https://doi.org/10.5281/zenodo.21863411).
- Huayin Wang. *Regime Has a Contract: Intervention, Observation, and the Data Foundation of Causal Identification*. Version 1.0, 2026. DOI: [10.5281/zenodo.21840854](https://doi.org/10.5281/zenodo.21840854).
- Huayin Wang. *A Contract Calculus for Governed Analytical Transformation: Totality, Partiality, Population, Expansion, and Fan-Out*. Version 1.0, 2026. DOI: [10.5281/zenodo.21752373](https://doi.org/10.5281/zenodo.21752373).


---

## Revision note

**Version 2.2.** This is a light conceptual alignment with *The Theory of Data*, Version 6.1. It preserves the Primer's Version 2.1 teaching sequence and scope while adding one central clarification: analytical identity is established before outputs are compared. It also adjusts a small number of statements so that governed names are treated as references to analytical identity rather than as the source of identity itself. The Primer intentionally leaves family IDs, semantic signatures, conformance declarations, certificate structure, and the broader state-law taxonomy to the Introduction and the canonical foundation.

**DOI:** pending publication assignment.
