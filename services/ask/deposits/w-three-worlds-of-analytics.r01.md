# The Three Worlds of Analytics

## Why Business Meaning, Data, and Material Data Need Different Governance

### Version 1.0

**Huayin Wang**\
**DOI:** 10.5281/zenodo.22143530\
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
consistency, and data identity exist under analytical law.

The **Material Data World** is where numbers, strings, blobs, records,
rows, columns, dataframes, tables, schemas, files, databases,
partitions, indexes, and execution plans are represented, stored,
changed, moved, and computed.

These are not merely three layers of one software stack. They differ in
their objects and ontology; processes and operations; technologies;
languages and codes; governance rules and instruments; clients and
expertise; and jurisdiction.

Analytics is unusual because ordinary analytical work repeatedly crosses
all three. A business question must become an data object. That object
must be realized through material data and computation. The result must
return as an data result and often cross again into business
interpretation, claims, decisions, and action.

> **The crossings happen all the time. The authority on each side is not
> the same.**

## Three worlds, three jurisdictions

### The Business World

The business world is the world of domain meaning. Its central question
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
model may contain joins, aggregation declarations, physical bindings, or
other computational instructions. That does not erase the jurisdictional
distinction: carrying a computation declaration does not by itself
confer authority over data identity or data law.

Business authority is authority over business meaning. It is not
automatically authority over analytical law or physical representation.

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

Its central question is: **What physical data exists, and how is it
represented, stored, changed, retrieved, and computed?**

Its processes include create, read, insert, update, delete, populate,
copy, extract, load, transform, ETL and ELT, filter, join, aggregate,
sort, materialize, index, partition, persist, replicate, query, and
execute. Its technologies include databases, warehouses, lakehouses,
dataframe systems, query engines, storage engines, ETL tools,
orchestration systems, and computational infrastructure. Its languages
include SQL, DDL and DML, relational algebra, dataframe APIs, ETL
specifications, database APIs, engine configuration, and physical plans.
Its governance instruments include schemas, data types, keys,
constraints, transactions, permissions, storage policies, orchestration
controls, data-quality checks, execution correctness, reliability, and
security.

Material existence is not data identity. A row can physically exist
without constituting the data object a question requires. A row can
physically fail to exist without establishing that the analytical value
is zero.

## The differences are structural

  -----------------------------------------------------------------------
  Dimension         Business world    Analytical data   Physical data
                                      world             world
  ----------------- ----------------- ----------------- -----------------
  Objects and       customers,        measures,         numbers, strings,
  ontology          products, stores, families,         blobs, records,
                    policies, KPIs,   anchors,          rows, columns,
                    domain            universes,        dataframes,
                    relationships     lineage, support, tables, schemas,
                                      analytical        files, databases
                                      identities        

  Processes and     define, classify, constitute,       create, read,
  operations        relate,           anchor, map,      update, delete,
                    interpret,        reduce, derive,   populate, ETL,
                    approve, map      move, validate    filter, join,
                                                        aggregate,
                                                        materialize

  Technologies      ontologies,       analytical        databases,
                    semantic layers,  constitutions,    warehouses,
                    catalogs, metric  analytical        dataframe
                    systems           languages,        systems, query
                                      validation        engines, ETL
                                      systems           tools

  Languages and     ontology          governed          SQL, DDL/DML,
  codes             languages,        analytical        dataframe APIs,
                    semantic models,  expressions,      ETL definitions,
                    metric            lineage and       physical plans
                    definitions,      derivation        
                    business rules    representations   

  Governance        ownership,        identity, reducer schemas, types,
                    definitions,      law, movement     constraints,
                    domain authority, law, existence,   transactions,
                    taxonomy, policy  support,          permissions, data
                                      derivability,     quality,
                                      consistency       execution
                                                        correctness

  Clients and       business users,   analysts,         applications,
  expertise         domain experts,   statisticians,    data engineers,
                    semantic modelers analytical        DBAs, platform
                                      engineers,        engineers,
                                      analytical        compute engines
                                      services          
  -----------------------------------------------------------------------

## Scope: worlds are jurisdictions, not the three foundations

The three worlds are not a decomposition of **Data · Certainty ·
Intelligence**, and they are not stages of analytical service.

They distinguish ontological and governance jurisdictions.

Questions of evidence, certainty, claims, inference, interpretation, and
standing can arise as objects move within and across these
jurisdictions. Evidence is therefore not a fourth world, and
Intelligence is not a layer to be inserted above the diagram. The
purpose here is narrower: to identify the different kinds of objects and
authority that analytics repeatedly composes.

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

Theory of Data develops a richer interior vocabulary --- including
families, anchors, lineage, movement, and reducer classes --- but those
terms refine the jurisdiction rather than create it.

## Why the middle is the Data World

A measure may have governed identity and law before any table stores its
values.

The word *data* is pulled in two directions. Business and semantic
systems pull it upward toward the world it describes. Database and
computational systems pull it downward toward the material forms that
carry it.

The Data World is neither of those things.

A governed data object can exist without being materialized. A measure
may have identity, anchor, family, lineage, reducer law, and derivation
even when no table currently stores its values. The same data object may
later be realized as a dataframe, a database relation, a Parquet file,
an Arrow array, an API response, or an in-memory value without becoming
a different data object merely because its materialization changed.

The converse also holds. A stored number, row, or column can exist
without establishing which governed data object it realizes, at what
anchor, over what universe, with what lineage, or under which laws.

So two facts can hold at once:

> **Data can exist without being materialized.**
>
> **Material data can exist without establishing data identity.**

This is why the Material Data World is not the Data World proper.
Material data carries, stores, moves, and computes data. It does not
exhaust what data is.

The dividing criterion is not syntax versus semantics. Material data may
carry rich semantics and still be a materialization. The deeper
distinction is ontological identity.

> **Data is neither the world it describes nor the materialization that
> carries it.**

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

The Theory of Data describes its ontology and governing laws. Analytics
then has a structural fact to deal with: useful work must cross between
this independently existing Data World and its two neighboring worlds.

That causal order matters:

> **Data World → theory → governance problem → architecture**

not:

> architecture → invented middle layer.

Any architecture may take advantage of this structure. Columna is one
engineered consequence, not the owner of the distinction.

## Three worlds imply two governed interfaces

The three worlds imply two crossings: **Business World ⇄ Data World**
and **Data World ⇄ Material Data World**. They are interfaces between
jurisdictions, not additional worlds.

This also locates two familiar Analytical Governance problems without
turning the worlds into a service pipeline. The **intent gap** lies
primarily over the upper crossing: has business intent been constituted
as the correct Data World object? The **servability gap** lies primarily
over the lower crossing: does available material realization establish
enough to serve that governed request?

## Analytics crosses all three

Consider: *What was average revenue per open store yesterday?*

*Open store* begins as business meaning. The requested average belongs
to the Data World: it has a population, anchor, measure identity,
reducer, and support requirements. The observations used to realize it
belong to the Material Data World.

An ordinary analytical path therefore looks like:

> business meaning → analytical constitution → physical realization →
> data result → business claim or action.

## Intermingling hides the crossings

For much of analytics history, people carried these crossings
implicitly. That allowed familiar substitutions: business meaning for
metric definition; metric definition for SQL; schema for data ontology;
material row existence for data existence; missing row for analytical
zero; query success for analytical validity; business name for data
identity; data quality for analytical support.

Each substitution can work in some circumstances. None is a general law.
The problem begins when one world silently answers a question that
belongs to another.

## The 47, 48, and 50 problem

Suppose a company has 50 stores. Forty-eight were open yesterday.
Revenue rows arrived for 47.

The Business World may establish that 48 stores were open. The Material
Data World may establish that revenue observations arrived for 47. A
database can correctly sum those 47 rows and divide by 47.

But the analytical question asks for average revenue over the population
of open stores. What happened to the forty-eighth store? Was its revenue
zero? Was the observation missing? Did the feed fail?

The material observations cannot settle those questions by themselves.
Nor can the business definition of *open store*. The data result depends
on a relationship among business meaning, analytical population, and
physical support.

## Governance becomes confused when jurisdiction is confused

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
legitimate Material Data World changes. They may improve physical
integrity. They do not, by themselves, establish the governed population
of a measure or prove that analytical support is complete.

The question **who is authoritative?** therefore has no single
organizational answer. Authority follows the object and jurisdiction
being governed.

## Intelligent agents raise the stakes

Intelligent agents can now interpret business intent, resolve semantic
concepts, choose analytical operations, find data, generate queries,
execute tools, interpret results, and recommend actions. One
probabilistic component can cross all three worlds in seconds.

Those are multiple crossings between jurisdictions, not one decision.
The more capable the agent becomes, the more important it becomes to
know where one authority ends and another begins.

## Closing

The three worlds need one another. They are still different worlds.

Analytics binds them together. That is its power. It is also one of its
deepest governance challenges.

The task is not to eliminate the crossings.

> **It is to stop treating a crossing as though nothing changed when we
> crossed it.**
