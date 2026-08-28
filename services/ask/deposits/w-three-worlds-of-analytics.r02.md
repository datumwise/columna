# The Three Worlds of Analytics

## Why Business Meaning, Data, and Material Data Need Different Governance

### Version 1.1

**Huayin Wang**  
**DOI:** 10.5281/zenodo.22146487  
**Publication date:** 28 August 2026

Analytics is often described as a path from a business question to data
and from data to an answer. That description compresses three different
worlds into one.

The **Business World** is where customers, stores, products,
organizations, policies, classifications, domain relationships, and
concepts such as *active customer* or *recognized revenue* acquire
organizational meaning.

The **Data World** is where measures, measure families, anchors,
universes, lineage, reducers, derivations, support, absence,
consistency, and data identity exist under data law.

The **Material Data World** is where numbers, strings, blobs, records,
rows, columns, dataframes, tables, schemas, files, databases,
partitions, indexes, and execution plans are represented, stored,
changed, moved, and computed.

These are not merely three layers of one software stack. They differ in
their objects and ontology; processes and operations; technologies;
languages and codes; governance rules and instruments; clients and
expertise; and jurisdiction.

Analytics is unusual because ordinary analytical work repeatedly crosses
all three. A business question must become a data object. That object
must be realized through material data and computation. The result must
return as a data result and often cross again into business
interpretation, claims, decisions, and action.

> **The crossings happen all the time. The authority on each side is not
> the same.**

## Three worlds, three jurisdictions

### The Business World

The Business World is the world of domain meaning. Its central question
is: **What does this mean in this organization or domain?**

An organization can decide what counts as an active customer. Finance
can define recognized revenue. Operations can determine what qualifies
as an open store. Its operations include defining, naming, classifying,
relating, interpreting, mapping, approving, and revising business
concepts. Its technologies include business ontologies, semantic layers,
catalogs, metric systems, business-rule systems, and domain models. Its
languages include ontology languages, semantic-model declarations,
metric definitions, taxonomies, controlled vocabularies, and business
rules. Its governance instruments include ownership, domain authority,
definition review, taxonomy, policy, approval, stewardship, and semantic
consistency.

Business-world technologies are often hybrid in practice. A semantic
model may contain joins, aggregation declarations, material bindings, or
other computational instructions. That does not erase the jurisdictional
distinction: carrying a computation declaration does not by itself
confer authority over data identity or data law.

Business authority is authority over business meaning. It is not
automatically authority over data law or material representation.

### The Data World

The Data World contains measures, families, anchors, universes, data
identities, lineage, conceptual mappings among data objects, reducers,
derivations, movement, support, and absence. Its central question is:
**What data object exists, and what follows lawfully from it?**

If the business defines an *open store*, that definition does not by
itself establish whether an average over open stores can be answered
when one open store has no revenue observation. If Finance defines
*revenue*, that authority does not determine whether a movement
duplicates the measure, whether a reducer may lawfully be applied again,
or whether two objects carrying the same display name have the same data
identity.

Its operations include constitution, anchoring, mapping, reduction,
derivation, movement, validation, support evaluation, and consistency
checking. Its governance instruments include identity law, family and
reducer law, movement law, universe and existence law, support,
derivability, and consistency. Its clients include analysts,
statisticians, analytical engineers, analytical services, and
intelligent systems.

### The Material Data World

The Material Data World is the world of representation, storage,
mutation, movement, and computation. Its objects include numbers,
strings, booleans, timestamps, blobs, records, rows, columns, arrays,
dataframes, relations, tables, schemas, files, databases, partitions,
indexes, and execution plans.

Its central question is: **How is data represented, stored, changed,
retrieved, and computed?**

Its processes include create, read, insert, update, delete, populate,
copy, extract, load, transform, ETL and ELT, filter, join, aggregate,
sort, materialize, index, partition, persist, replicate, query, and
execute. Its technologies include databases, warehouses, lakehouses,
dataframe systems, query engines, storage engines, ETL tools,
orchestration systems, and computational infrastructure. Its languages
include SQL, DDL and DML, relational algebra, dataframe APIs, ETL
specifications, database APIs, engine configuration, and execution plans.
Its governance instruments include schemas, data types, keys,
constraints, transactions, permissions, storage policies, orchestration
controls, data-quality checks, execution correctness, reliability, and
security.

Material presence is not data identity. A row may be present in a table
without constituting the data object a question requires. A row may be
absent without establishing that the data value is zero.

## The differences are structural

| Dimension | Business World | Data World | Material Data World |
|---|---|---|---|
| **Objects** | customers, products, stores, contracts, policies, KPIs, domain relationships | measures, families, anchors, universes, lineage, support, data identities | bits, bytes, numbers, strings, blobs, records, rows, columns, arrays, dataframes, tables, schemas, files, streams, databases |
| **Work** | define, classify, relate, interpret, approve | constitute, anchor, map, reduce, derive, move, validate | create, read, update, delete, populate, ETL, filter, join, aggregate, materialize |
| **Technologies** | ontologies, semantic layers, catalogs, metric systems | data constitutions, data languages, validation systems | databases, warehouses, dataframe systems, query engines, ETL tools |
| **Languages** | ontology languages, semantic models, metric definitions, business rules | governed data expressions, lineage and derivation representations | SQL, DDL/DML, dataframe APIs, ETL definitions, execution plans |
| **Governance** | ownership, definitions, domain authority, taxonomy, policy | identity, reducer law, movement law, existence, support, derivability, consistency | schemas, types, constraints, transactions, permissions, material-data quality, execution correctness |
| **Expertise and clients** | business users, domain experts, semantic modelers | analysts, statisticians, analytical engineers, analytical services | applications, data engineers, DBAs, platform engineers, compute engines |

## Scope: worlds are jurisdictions, not the three foundations

The three worlds are not another way of dividing **Data · Certainty · Intelligence**, and they are not stages of an analytical service.

They answer a narrower question:

> **What kinds of things are being governed, and what kind of authority applies to each?**

Questions of evidence, certainty, claims, inference, interpretation, and standing can arise as analytics moves within and across these worlds. Evidence is not a fourth world, and Intelligence is not a layer above the diagram.

## A small vocabulary for the Data World

The Data World does not require a reader to learn an entire formal
calculus before the jurisdiction can be recognized. Five ordinary ideas
are enough to see the distinction:

-   **Identity** --- what data object is this, and what makes it the
    same object across representations?
-   **Population / universe** --- what set of things does the object
    range over?
-   **Reduction** --- what operations may combine values, and under what
    conditions?
-   **Support / absence** --- what observations or grounds are present,
    missing, zero, or ineligible?
-   **Lawful derivation** --- what other data objects may legitimately
    be produced from this one?

*The Theory of Data* develops a richer interior vocabulary --- including
families, anchors, lineage, movement, and reducer classes --- but those
terms refine the jurisdiction rather than create it.

## Why the middle is the Data World

A measure may have governed identity and law before any table stores its values.

That simple fact separates the Data World from the Material Data World.

The word *data* is pulled in two directions. Business and semantic systems pull it toward the world the data describes. Database and computational systems pull it toward the material forms that store and carry it.

The Data World is neither of those things.

A measure can have a governed identity, anchor, family, lineage, reducer law, and derivation even when no table currently stores its values. The same data object may later be realized as a dataframe, a database relation, a Parquet file, an Arrow array, an API response, or an in-memory value without becoming a different data object merely because its material form changed.

The converse also holds. A stored number, row, or column can exist without establishing which governed data object it realizes, at what anchor, over what universe, with what lineage, or under which laws.

It helps to separate three ideas that ordinary speech often compresses into *exists*:

- **a constituted data object** has governed identity even if no values are currently stored;
- **a derivable data object** can be lawfully produced from other governed data;
- **a materialized result** has actually been computed or stored in some material form.

So when we say that data can exist without materialization, we mean that the data object can already have identity and law. We do not mean that an uncomputed value has somehow already been observed.

Two facts can therefore hold at once:

> **Data can exist without being materialized.**
>
> **Material data can exist without establishing data identity.**

Material data carries, stores, moves, and computes data. It does not exhaust what data is.

The distinction is not simply syntax versus semantics. A table or dataframe can carry rich meaning and still be only one materialization of a data object. The deeper question is whether changing the material form changes what data object it is.

> **Data is neither the world it describes nor the materialization that carries it.**

## Business semantics can declare computation without governing data law

The distinction between the Business World and the Data World does not
depend on pretending that semantic layers contain only names and
definitions.

Modern semantic systems can declare aggregation functions, metric
formulas, and join relationships. A semantic model may specify
`SUM(amount)` or define how a metric reaches a table.

Those declarations are important. They are still different from
governing the laws of the resulting data object.

Declaring `SUM(amount)` as a computation instruction does not by itself
establish the reducer's closure class, whether another reduction is
admissible, whether movement across a relationship preserves the
measure, or whether two derivation paths are consistent.

Likewise, declaring a join relationship does not by itself establish the
data consequences of movement across that relationship.

The distinction is therefore not **semantics versus computation**.

It is **business/domain authority versus data-law authority**.

## The causal order

The Data World does not exist because an architecture inserts it between
business meaning and material systems.

It is already there.

*The Theory of Data* describes its ontology and governing laws. Analytics
then has a structural fact to deal with: useful work must cross between
this independently existing Data World and its two neighboring worlds.

That causal order matters:

> **Data World → theory → governance problem → architecture**

not:

> architecture → invented middle layer.

Any architecture may take advantage of this structure. No particular
architecture owns the distinction.

## Three worlds imply two governed interfaces

The three worlds imply two crossings: **Business World ⇄ Data World** and **Data World ⇄ Material Data World**. These are interfaces between worlds, not additional worlds of their own.

This also helps locate two familiar Analytical Governance problems without turning the three worlds into a service pipeline.

The **intent gap** lies primarily over the upper crossing:

> **Does the representation in the Data World correctly capture the user's intent from the Business World?**

The **servability gap** lies primarily over the lower crossing:

> **Can the Material Data World provide what the Data World request requires?**

## Analytics crosses all three

Consider: *What was average revenue per open store yesterday?*

*Open store* begins as business meaning. The requested average belongs
to the Data World: it has a population, anchor, measure identity,
reducer, and support requirements. The observations used to realize it
belong to the Material Data World.

An ordinary analytical path therefore looks like:

> business meaning → data constitution → material realization →
> data result → business claim or action.

## Intermingling hides the crossings

For much of analytics history, people carried these crossings
implicitly. That allowed familiar substitutions: business meaning for
metric definition; metric definition for SQL; schema for data ontology;
material row presence for data existence; missing row for zero; query
success for validity of the data result; business name for data identity;
material-data quality for Data World support.

Each substitution can work in some circumstances. None is a general law.
The problem begins when one world silently answers a question that
belongs to another.

## The 47, 48, and 50 problem

Suppose **50 stores exist. 48 were open yesterday. Revenue observations arrived for 47.**

Someone asks:

> **What was average revenue per open store yesterday?**

The Business World can establish what *open store* means and which stores qualify.

The Material Data World can establish which revenue observations are present.

A database can correctly sum the 47 observations and divide by 47.

But the Data World request asks for an average over the governed population of open stores.

What happened to the forty-eighth store? Was its revenue zero? Was the observation missing? Did the feed fail?

The material observations cannot settle those questions by themselves. Nor can the business definition of *open store*.

The point here is jurisdictional: **three kinds of authority establish different facts**. Business authority establishes what *open* means. Material-data authority establishes what observations are present. Data authority determines what data object those facts jointly establish.

## Governance becomes confused when authority is confused

Modern organizations often place business definitions, semantic
ownership, metric governance, schemas, lineage, access control, data
quality, analytical validation, transformation policy, and AI
permissions under the broad heading of *data governance*. These are all
legitimate concerns. They do not govern the same kinds of objects.

When governance treats the three worlds as one, it becomes difficult to
answer: **Who is authoritative about what?**

## When jurisdiction becomes an ownership conflict

The distinction becomes concrete when something changes.

Suppose Finance changes the approved meaning of *recognized revenue*.
That is a legitimate Business World change. The new meaning may require
data objects to be reconstituted. But Finance's authority over the
definition does not silently authorize a new reducer law or make
previously invalid derivations valid.

Now suppose a platform team changes a column from nullable to
non-nullable, adds a schema constraint, or migrates a table. Those are
legitimate Material Data World changes. They may improve material
integrity. They do not, by themselves, establish the governed population
of a measure or prove that data support is complete.

So the question **who is authoritative?** has no single organizational
answer. Authority follows the kind of object being governed and the
question being asked about it.

## Intelligent agents raise the stakes

Intelligent agents can now interpret business intent, resolve semantic
concepts, choose analytical operations, find data, generate queries,
execute tools, interpret results, and recommend actions. One
probabilistic component can cross all three worlds in seconds.

Those are multiple crossings between different kinds of authority, not one decision.
The more capable the agent becomes, the more important it becomes to
know where one authority ends and another begins.

## Closing

The three worlds need one another. They are still different worlds.

Analytics binds them together. That is its power. It is also one of its
deepest governance challenges.

The task is not to eliminate the crossings.

> **It is to stop treating a crossing as though nothing changed when we
> crossed it.**
