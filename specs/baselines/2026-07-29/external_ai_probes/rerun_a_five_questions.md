# Columna and datumwise.ai: Five Questions — day-2 RE-RUN, 2026-07-29

**Capture:** **A**
**Assistant:** ⚠️ **UNATTRIBUTED — see `RERUN_INDEX.md`.** The upload carries no assistant name and
the desk instruction did not state one. Recorded as a lettered capture rather than guessed: the
2026-07-27 baseline determined search modes *from the transcripts, not by assumption*, and a
mis-attributed re-run would produce a per-assistant "drift" that is really a mix-up.
**Captured:** 2026-07-29 (day 2 — ~40 hours after the 2026-07-27 launch-eve baseline)
**Relayed by:** Huayin — uploaded 2026-07-29 03:46 UTC
**Source file:** `cd5fac47_columna_five_questions_and_answers.md` · sha256 `3b55b18daa6620b5fe4da2ffbaea8b65554739b98063c3fea302a1121e03a3dc`
**Search mode:** **SEARCHED AND FOUND US.** Carries inline `Source:` lines to five distinct datumwise.ai deep URLs — `/thesis`, `/how-these-documents-relate`, `/why` (×3), `/atlas` (×2), and the root.
**Mode:** `found-and-right` — per `../../PROBE_MODE_SCHEMA.md`. **Basis:** Q2 answered *"No—not as it is publicly presented… an independent open-source research project"*; five distinct datumwise.ai deep URLs cited inline.
**Provenance:** the body below is the assistant's reply **VERBATIM**, byte-preserved from the
uploaded file. Nothing is summarized, corrected, or trimmed — including anything wrong. A corrected
error is one of the clearest drift signals a later capture gives us; so is a new one.

---

# Columna and datumwise.ai: Five Questions

## Table of Contents

1. [What is Columna (datumwise.ai)?](#1-what-is-columna-datumwiseai)
2. [Is datumwise a company?](#2-is-datumwise-a-company)
3. [What evidence exists that Columna's approach works?](#3-what-evidence-exists-that-columnas-approach-works)
4. [Columna vs dbt Semantic Layer vs Cube](#4-columna-vs-dbt-semantic-layer-vs-cube)
5. [What are Columna's weaknesses?](#5-what-are-columnas-weaknesses)

---

# 1. What is Columna (datumwise.ai)?

**Columna is an open-source analytical correctness framework for humans and AI agents.** It is designed to sit between a question and the underlying data system so that an agent cannot simply generate plausible SQL, execute it, and confidently report a misleading number.

**datumwise** is the independent research project that develops and stewards Columna. “Columna” stands for **Column Algebra**: its central idea is that analytical meaning belongs to columns—what each measure says and what it is about—not merely to the tables in which the data happens to be stored.

Source: [datumwise thesis](https://datumwise.ai/thesis)

## How Columna works

Columna has three principal parts:

### 1. The Manifold

A declared model of the dataset containing its analytically significant columns, measures, populations, grains, relationships, and operational constraints. These declarations can be checked against the actual data before being published.

### 2. FrameQL

A constrained query language that references meanings declared in the Manifold. The model does not invent joins or write arbitrary SQL against database tables.

### 3. The engine

A deterministic layer that adjudicates the requested analysis and returns one of four outcomes:

- **Serve** — return the result.
- **Disclose** — return it with material assumptions attached.
- **Clarify** — identify multiple legitimate interpretations and ask the caller to choose.
- **Refuse** — explain why the requested result is not defined or defensible.

The same structured response contract can be used by Python applications, HTTP clients, or AI agents through MCP.

Source: [How these documents relate](https://datumwise.ai/how-these-documents-relate)

## The problem it addresses

A normal text-to-SQL system might receive:

> “What was average order value by month?”

It can generate valid SQL and return a plausible number without resolving questions such as:

- Is the stored value already an average?
- At what grain was it originally computed?
- Should monthly results be recomputed from orders or averaged from daily averages?
- Which customer or transaction population is included?

All of those queries may run successfully while producing materially different answers.

Columna attempts to move these decisions out of model improvisation and into a declared, machine-checkable grammar. The model may help interpret the user’s language, but it cannot override the analytical rules. In the project’s formulation, the model proposes; the grammar disposes; a human chooses when more than one legitimate meaning remains.

Source: [Why Columna](https://datumwise.ai/why)

## What makes it different

Columna is not primarily:

- a chatbot;
- a general-purpose SQL generator;
- a conventional BI dashboard;
- or merely a catalog of metric descriptions.

It is better understood as a **governed reasoning and verification boundary** between semantic interpretation and data execution.

Traditional semantic layers usually help define known metrics. Columna goes further by trying to determine whether a requested operation is lawful, whether the question is ambiguous, which assumptions must accompany the result, and when the system should decline to provide a number.

It also makes a deliberately limited promise: a grammar can certify certain structural properties of a computation, but it cannot mechanically determine every question of business meaning or analytical inference. Where correctness cannot be certified, the architecture emphasizes disclosure, clarification, and human judgment rather than silent confidence.

## In one sentence

**Columna is an executable trust boundary for data analysis: AI handles language and proposes an interpretation, while a declared column algebra determines what can be computed, what must be disclosed, and what should be clarified or refused.**

As of July 28, 2026, Columna is published under Apache-2.0, and the datumwise site lists version **0.13.2** as the current release.

Source: [datumwise.ai](https://datumwise.ai/)

---

# 2. Is datumwise a company?

**No—not as it is publicly presented.** datumwise describes itself as an **independent open-source research project**, not a commercial company. It is maintained by **Huayin Wang (research)** and **Irena Wang (engineering)** and exists to build and steward Columna.

Source: [datumwise.ai](https://datumwise.ai/)

That does not prove that no legal entity has ever been registered under the name, but the public site does not position datumwise as a startup, vendor, or incorporated business.

---

# 3. What evidence exists that Columna's approach works?

There is **credible proof-of-mechanism**, but not yet strong evidence of broad real-world effectiveness.

## Evidence currently available

| Evidence | What it establishes | Main limitation |
|---|---|---|
| **A runnable open-source implementation** | Columna is more than a proposal. The published package accepts FrameQL requests and returns structured `serve`, `disclose`, `clarify`, or `refuse` outcomes. Its packaged demo includes ambiguous averaging, an invalid dimensional request, an unsafe stock aggregation, and a well-formed metric request. | Demonstrating designed examples does not establish performance across arbitrary enterprise warehouses. |
| **Automated tests and reproducible fixtures** | The repository provides test commands for the core engine and MCP server. It also includes a schema-identical miniature warehouse for CI and describes a larger warehouse containing 299,934 transactions for data-backed tests. | The tests and fixtures are authored by the same project that implements the system. They are not an independent evaluation. |
| **A recorded live-agent test** | In one documented test, an LLM was asked for a plausible metric that did not exist. The agent asked for clarification, and the engine independently rejected any fabricated measure as an unknown column. Both behaviors are reportedly covered by tests. | This is one narrow case using the project’s own demo Manifold and test setup. |
| **A nine-model text-to-SQL study** | datumwise reports that nine models given identical, documented schemas continued to silently choose interpretations for ambiguous averaging questions. This supports the claim that documentation and stronger models alone do not reliably solve the problem Columna targets. | This primarily proves that the **problem exists**. It does not by itself prove that Columna performs better in an end-to-end comparison. |
| **A formal account of aggregation ambiguity** | *The Two Anchors of a Measure* argues formally that some measures depend on both an output grain and an often-unrecorded input grain, and that the resulting value cannot reveal the missing grain after the fact. That supplies a theoretical foundation for representing anchors explicitly. | A valid formal argument establishes that the representation is necessary for certain cases, not that the complete software system is sufficient for practice. |
| **A public failure taxonomy** | The Silent Failure Atlas identifies 67 analytical failure modes and gives detection checks. The project openly states that its initial benchmark covers only 20 of those 67 modes and names the uncovered regions. | The taxonomy, benchmark, and implementation all originate from datumwise. Coverage is explicitly partial. |

Sources:

- [Columna GitHub repository](https://github.com/datumwise/columna)
- [Recorded nonexistent-measure transcript](https://github.com/datumwise/columna/blob/main/packages/columna-server/demos/agent_nonexistent_measure_transcript.md)
- [Why Columna](https://datumwise.ai/why)
- [How these documents relate](https://datumwise.ai/how-these-documents-relate)
- [Silent Failure Atlas](https://datumwise.ai/atlas)

## The strongest claim the evidence supports

The evidence supports this statement reasonably well:

> **When analytical legality has been correctly declared in a Columna Manifold, the engine can mechanically prevent, expose, or request clarification for certain classes of ambiguity and invalid aggregation rather than allowing an LLM to resolve them silently.**

That result follows largely from the architecture. An LLM may propose a nonexistent measure or an illegal reduction, but the deterministic engine does not have to accept it. The model is therefore no longer the final authority on whether the operation is valid. The public demo and recorded tests illustrate this behavior.

## What has not yet been demonstrated

As of **July 28, 2026**, the public evidence does not establish:

- independent third-party replication;
- peer-reviewed evaluation of Columna itself;
- published production deployments or customer case studies;
- comparison against semantic layers, constrained SQL agents, or other guardrail systems on the same benchmark;
- measured reductions in incorrect business answers;
- false-positive and false-negative rates for `clarify`, `disclose`, and `refuse`;
- authoring and maintenance costs for large, changing warehouses;
- performance, scalability, or operational-reliability results.

The project is also extremely new and shows limited external adoption signals on GitHub, although packaged versions are available through Python package infrastructure.

## Bottom line

**Columna has passed the “can this idea be made executable?” test. It has not yet passed the “does this materially improve analytical correctness across independent, real-world deployments?” test.**

It is best characterized as a **technically substantive and falsifiable early-stage research system**. Its architecture gives a convincing reason that it should block the failure modes it can express, and the open implementation makes those claims inspectable. But the current evidence is still mostly first-party, example-driven, and limited to proof-of-concept and benchmark construction—not external validation of general effectiveness.

---

# 4. Columna vs dbt Semantic Layer vs Cube

Columna, dbt Semantic Layer, and Cube all put a governed model between consumers and warehouse tables, but they optimize for different problems:

- **dbt Semantic Layer:** centrally define and reuse business metrics.
- **Cube:** serve governed analytics quickly and securely to many applications.
- **Columna:** determine whether an analytical request is defensible, ambiguous, assumption-dependent, or invalid.

## Comparison

| Dimension | Columna | dbt Semantic Layer | Cube |
|---|---|---|---|
| **Primary goal** | Analytical correctness and explicit handling of uncertainty | Consistent metric definitions across downstream tools | Production semantic serving for BI, embedded analytics, applications, and AI |
| **Central abstraction** | Columns, populations, grains, anchors, and permitted analytical operations in a **Manifold** | Semantic models connected by entities, with dimensions and metrics | Entity-oriented **cubes** containing dimensions, measures, joins, and pre-aggregations; curated **views** for consumers |
| **Query model** | Constrained **FrameQL** | MetricFlow metric queries through CLI and dbt Semantic Layer APIs | Postgres-compatible Semantic SQL, REST, GraphQL, and other APIs |
| **Main question answered** | “Is this requested computation defensible?” | “How is this governed metric calculated and sliced?” | “How can this governed dataset be queried and served efficiently?” |
| **Ambiguity behavior** | First-class `clarify`, `disclose`, and `refuse` outcomes | Usually expects the requested metric and dimensions to resolve to a defined query; invalid requests produce errors | Validates queries against the model, but generally executes one modeled interpretation |
| **Aggregation safety** | Models the input and output anchors of measures and can reject or clarify unsafe reductions | Supports governed aggregation types and non-additive dimensions | Supports aggregation types, fixed-granularity and multi-stage measures, and join-row-multiplication handling |
| **Join handling** | Exposes only relationships and dimensional requests the Manifold permits | Builds joins through an entity graph and chooses legal paths between semantic models | Generates joins from declared cube relationships; views can pin exact join paths |
| **Performance layer** | Not its principal purpose | Primarily generates metric SQL for execution in the data platform; exports can persist results | A major focus: pre-aggregations, caching, partitioning, incremental refresh, and Cube Store |
| **Security and tenancy** | Not a major advertised subsystem in the current public implementation | Generally works with dbt-platform and warehouse governance | Built-in semantic-layer access policies, including row-, member-, and tenant-level controls |
| **AI-agent interface** | MCP and APIs return the same structured four-mood contract | Agents and applications can query governed metric metadata and APIs | MCP and AI interfaces expose governed views and Semantic SQL |
| **Maturity** | Early-stage open-source research implementation | Established component of the dbt ecosystem | Established semantic-layer and analytics-serving platform |

Sources:

- [datumwise.ai](https://datumwise.ai/)
- [dbt: About MetricFlow](https://docs.getdbt.com/docs/build/about-metricflow)
- [Cube: Data modeling with cubes](https://docs.cube.dev/docs/data-modeling/cubes)

## The most important difference

Consider this question:

> What is average order value by month?

### dbt Semantic Layer

A dbt project might define `average_order_value` as a governed metric. MetricFlow then determines the appropriate semantic model, joins, time dimension, and SQL.

This gives every connected tool the **same definition** of average order value.

If the metric author has correctly defined the relevant aggregation behavior, dbt can protect against important problems such as aggregating a non-additive measure across an invalid dimension. MetricFlow explicitly supports non-additive dimensions for values such as account balances.

Source: [dbt measures documentation](https://docs.getdbt.com/docs/build/measures)

The normal contract is:

> The metric is defined; calculate it using the declared model.

### Cube

Cube might expose an `average_order_value` measure through an `orders` cube or curated sales view. It would generate the joins and SQL, enforce access policies, and potentially answer from a pre-aggregation rather than scanning the warehouse.

Cube is particularly strong when that metric must support:

- interactive dashboards;
- customer-facing embedded analytics;
- many concurrent applications;
- tenant-specific access;
- low-latency queries;
- predictable warehouse costs.

Cube automatically matches eligible queries to materialized pre-aggregations and otherwise queries the upstream data source.

Source: [Cube pre-aggregations](https://docs.cube.dev/docs/pre-aggregations/using-pre-aggregations)

Its normal contract is:

> The governed analytical surface is defined; serve the requested query efficiently and securely.

### Columna

Columna asks whether “average order value by month” is sufficiently specified in the first place.

For example:

- Is `aov` a raw order-level value or an already aggregated daily average?
- If it is already averaged, from which input grain may it be averaged again?
- Does the data contain an actual order population?
- Are several valid input grains available?
- Must a population substitution or other assumption be disclosed?

Where more than one materially different interpretation remains, Columna can return `clarify` rather than selecting one. Where the request is legal only under an important assumption, it can return `disclose`. Where the requested relationship or measure is not defined, it can return `refuse`.

Its contract is:

> Before calculating, establish whether the question has one defensible computational meaning.

## Where dbt and Cube are stronger

Columna should not presently be treated as a feature-for-feature replacement for either system.

### dbt Semantic Layer is stronger for metric governance inside dbt

dbt is the natural choice when:

- transformations already live in dbt;
- metrics should be versioned beside dbt models;
- teams want a shared metric graph;
- downstream tools need standard metric integrations;
- analysts need derived, ratio, conversion, cumulative, or time-shifted metrics.

MetricFlow supports derived and ratio metrics and uses entities to generate joins across semantic models.

Source: [dbt join logic](https://docs.getdbt.com/docs/build/join-logic)

### Cube is stronger as an operational serving layer

Cube is the natural choice when:

- analytics is part of a customer-facing product;
- latency and concurrency matter;
- pre-aggregations are necessary;
- REST, GraphQL, or SQL compatibility is required;
- tenant-aware access control must be enforced centrally;
- BI, applications, and agents need the same governed interface.

Cube explicitly combines modeling, access control, caching, and APIs as the four pillars of its semantic-layer architecture.

Source: [Cube introduction](https://docs.cube.dev/docs/introduction)

## Where Columna is distinct

Columna’s differentiator is not that it has metrics, dimensions, or generated queries. dbt and Cube already provide sophisticated versions of those capabilities.

Its distinctive features are:

### 1. Ambiguity is a valid result

In most query systems, success means returning rows and failure means returning an error.

In Columna, `clarify` is a successful adjudication: the engine has determined that the request has multiple legitimate meanings and identifies the choice a human must make.

### 2. Assumptions travel with the answer

`disclose` treats important qualifications as part of the machine-readable result contract rather than documentation that a consumer may never see.

### 3. The model’s freedom is deliberately restricted

Cube’s Semantic SQL retains substantial SQL expressiveness over governed objects. MetricFlow generates SQL from requested metrics and dimensions. FrameQL is intentionally narrower: it can ask only for analytical meaning admitted by the Manifold.

Cube describes this SQL flexibility as a benefit; Columna treats some forms of expressiveness as a correctness risk.

Source: [Cube SQL API query format](https://docs.cube.dev/reference/core-data-apis/sql-api/query-format)

### 4. Correctness metadata is separated from descriptive meaning

Columna’s thesis is that machine-checkable facts determining whether a calculation is legal should form a small grammar distinct from descriptions, business glossaries, and other communicative metadata. Its column algebra therefore concentrates on properties such as anchors and populations that alter the legality or result of a computation.

## Important overlap

The distinction should not be overstated. dbt and Cube do more than merely give metrics consistent names.

**dbt provides correctness controls**, including entity-aware join generation, limits designed to avoid ambiguous multi-hop paths, non-additive dimensions, and validation of semantic models.

**Cube provides correctness controls**, including declared relationship cardinalities, curated join paths, measure-aware SQL semantics, and handling for row multiplication across joins.

Sources:

- [dbt join logic](https://docs.getdbt.com/docs/build/join-logic)
- [Cube views](https://docs.cube.dev/docs/data-modeling/views)

The difference is primarily the **scope and runtime contract**:

- dbt and Cube are designed principally to resolve valid queries against a governed model.
- Columna is designed principally to adjudicate whether the requested analytical statement should be resolved at all.

## Practical selection

Choose **dbt Semantic Layer** when the main problem is:

> “Different tools and teams calculate the same business metric differently.”

Choose **Cube** when the main problem is:

> “We need a governed, secure, high-performance analytics API for dashboards, products, and agents.”

Choose **Columna** when the main problem is:

> “A valid-looking query may still silently choose the wrong grain, population, relationship, or interpretation.”

A plausible combined architecture is:

```text
Human or AI agent
        │
        ▼
Columna correctness/adjudication boundary
        │
        ▼
dbt Semantic Layer or Cube governed metric model
        │
        ▼
Warehouse and serving infrastructure
```

That combination is an architectural inference rather than a documented turnkey integration. Columna could govern whether a request is defensible, while dbt supplies organization-wide metric definitions or Cube supplies secure, low-latency execution.

The practical challenge would be avoiding duplicate semantic declarations and establishing which layer is authoritative for measures, joins, grains, and populations.

## Bottom line

**dbt Semantic Layer is metric-centric. Cube is serving-centric. Columna is adjudication-centric.**

dbt and Cube primarily make governed analysis **consistent and operational**. Columna attempts to make the boundary between a defensible answer and an unjustified answer **explicit and executable**.

Today, Columna is much earlier and narrower, while dbt and Cube provide substantially broader production capabilities and integrations. Its value proposition is therefore not “a better dbt or Cube,” but a correctness discipline those systems do not currently expose through an equivalent `serve / disclose / clarify / refuse` contract.

---

# 5. What are Columna's weaknesses?

Columna’s central strength—constraining analysis to a declared grammar—is also the source of its largest weaknesses.

## 1. It can only verify what the Manifold correctly declares

Columna does not independently know the business, the real-world population, or what the warehouse *should* contain. It adjudicates a request against the Manifold and the data available to it.

If an author incorrectly declares:

- the population represented by a table;
- the grain of a measure;
- a permitted relationship;
- an aggregation anchor;
- or the meaning of a missing row,

then Columna may enforce the incorrect declaration consistently.

The project’s own Atlas calls this a **semantic-contract failure**: the declared meaning can diverge from what the data actually holds. datumwise also documents mistakes in its own benchmark and interpretation of “order,” demonstrating that the authors of a correctness system are not immune to incorrect bindings.

Source: [Silent Failure Atlas](https://datumwise.ai/atlas)

In other words:

> Columna can make an incorrect contract executable; it cannot guarantee that the contract is true.

This is probably its most important weakness.

## 2. Correct Manifold authoring is expensive

The Manifold requires more than friendly metric descriptions. Someone must identify and correctly declare populations, universes, grains, anchors, reduction barriers, lineage, relationships, and other mechanically significant properties.

datumwise explicitly describes this grammar-authoring layer as **“small expensive,” data-attested, and human-gated**.

Source: [Why Columna](https://datumwise.ai/why)

That creates practical questions:

- Who has enough business and data-engineering knowledge to author it?
- How are declarations reviewed?
- How are changes synchronized with warehouse migrations?
- How much of a large warehouse can realistically be modeled?
- What happens when the authoritative knowledge is divided among several teams?

The approach moves analytical work from runtime improvisation to build-time modeling. That is often desirable, but it does not eliminate labor; it concentrates that labor into a specialized and potentially scarce role.

## 3. Its correctness boundary is necessarily incomplete

Columna’s theory acknowledges that a grammar can govern the **form of a computation**, but cannot establish every conclusion drawn from a correctly computed number.

For example, it cannot mechanically determine:

- whether survey nonresponse makes an average misleading;
- whether an observed association is causal;
- whether an omitted subgroup reverses a trend;
- whether the available data accurately represents the real world;
- whether a business question contains an unstated but important contextual assumption.

The Atlas explicitly separates mechanically checkable failures from analytical-inference failures that admit only audit and disclosure. It also states that the mechanism behind missing data may be unverifiable from the data itself.

Thus, “Columna-approved” must not be interpreted as:

> This analysis is true, unbiased, and suitable for every decision.

At most, it means that the computation satisfies the particular structural contract and that known disclosures have been attached.

## 4. The demonstrated failure coverage remains narrow

The public benchmark currently seeds **20 of the Atlas’s 67 identified failure modes**. Its strongest coverage is concentrated around aggregation mechanics and unsafe questions, while linkage problems, semantic drift, numerical behavior, inference failures, and much of the execution layer remain open territory.

Benchmark coverage is not identical to product capability, but it indicates the extent of the publicly demonstrated evidence.

There is a significant difference between:

- proving that ambiguous averaging and semi-additive inventory can be handled;
- and showing dependable protection across the full range of enterprise analytical failures.

The project openly acknowledges that its taxonomy is not complete and that some boundaries and frequency claims remain judgment-based.

## 5. Constraint may become user friction

FrameQL deliberately exposes a smaller analytical surface than raw SQL. The current MCP server offers five read-only tools, with no direct SQL or write interface. Queries are limited to meanings declared in a Manifold.

Source: [Columna server README](https://github.com/datumwise/columna/blob/main/packages/columna-server/README.md)

That design prevents many unsafe operations, but it may also make legitimate exploratory work difficult:

- Novel questions may fall outside the modeled domain.
- Analysts may need an operation that FrameQL cannot yet express.
- A request may produce repeated clarification rather than an immediate result.
- Users may bypass Columna when they need flexibility.
- Manifold coverage may lag behind rapidly changing analytical needs.

This is the familiar safety–expressiveness trade-off. An operation that cannot be expressed cannot silently fail—but it also cannot produce useful new analysis.

The practical risk is that governed analysis happens through Columna while difficult or urgent analysis moves back to notebooks and raw SQL, recreating an ungoverned region around the system.

## 6. The four moods still require policy judgments

`Serve`, `disclose`, `clarify`, and `refuse` are valuable distinctions, but deciding among them is not purely mathematical in every case.

Someone must determine:

- which assumptions are material;
- how much uncertainty is tolerable;
- when disclosure is sufficient;
- when an operation must be refused;
- how approximate results should be classified;
- which alternatives deserve presentation to the user.

The current implementation describes its `serve`/`disclose` decision as materiality-driven.

Source: [Columna project notes](https://github.com/datumwise/columna/blob/main/CLAUDE.md)

Materiality is partly contextual. A 1% discrepancy might be irrelevant in exploratory marketing analysis but unacceptable in regulatory reporting. Columna can encode and consistently apply such decisions, but it cannot eliminate the governance judgment behind them.

A related concern is that users may ignore disclosures. Returning a questionable inventory sum with a warning is more honest than silently returning it, but downstream agents, dashboards, or humans might still extract and repeat only the number.

## 7. It is currently a wedge, not a complete analytics platform

The public implementation centers on:

- a Python engine;
- a directory of Manifold files;
- an MCP server;
- a natural-language agent;
- and a shared response contract.

The project itself calls the MCP server a **“wedge product.”** The current Manifold store is directory-based and parsed at startup; its project notes say a dedicated catalog will be needed when multi-Manifold management becomes more substantial.

The public documentation does not presently describe mature equivalents of many production-platform capabilities, such as:

- enterprise identity and role-based access control;
- fine-grained row or tenant security;
- distributed caching and query acceleration;
- high-availability deployment;
- large-scale catalog management;
- lineage synchronization with existing data tools;
- usage analytics and governance workflows;
- polished BI-tool integrations;
- change-management and migration tooling.

This means adopting Columna may require building substantial surrounding infrastructure or operating it alongside dbt, Cube, BI systems, catalogs, and warehouse-security controls.

## 8. Integration may duplicate existing semantic work

Organizations already using dbt Semantic Layer, Cube, LookML, or another governed modeling system may have definitions for metrics, dimensions, joins, and grains.

Introducing Columna creates potential duplication:

```text
Existing semantic model
        +
Columna Manifold
        =
two partially overlapping declarations
```

Unless one can be generated reliably from the other, teams must decide:

- which layer is authoritative;
- how conflicts are detected;
- how changes propagate;
- whether a measure must be modeled twice;
- and whether the correctness properties can survive translation between systems.

Columna’s distinctions—especially populations and input anchors—may not map cleanly onto existing semantic-layer metadata. That is intellectually part of its value, but operationally it raises adoption cost.

## 9. Evidence is still primarily first-party

The repository contains runnable demonstrations, tests, an MCP transcript, and a benchmark warehouse. That establishes that the architecture is executable. The current public demonstration includes four carefully selected asks representing the four moods, and the fuller example warehouse contains 299,934 transactions.

However, the public record remains weak on:

- independent replications;
- external benchmark comparisons;
- production case studies;
- measured false-refusal or false-clarification rates;
- analyst productivity impact;
- large-warehouse performance;
- Manifold-maintenance cost;
- and evidence that users act appropriately on disclosures.

The visible external adoption remains very limited.

That does not mean the approach fails. It means the available evidence supports **proof of mechanism**, not yet proven product-market or enterprise-scale effectiveness.

## 10. Early technical limitations remain

The current package supports Python 3.10–3.13 on 64-bit systems. Python 3.14 and 32-bit environments are excluded because of a dependency on available `datasketches` binaries.

The natural-language agent also currently uses an Anthropic provider by default, while scripted behavior is used for hermetic testing.

These are not conceptual failures, but they reinforce that Columna is currently an early technical system rather than a broadly portable, vendor-neutral enterprise standard.

## Overall assessment

Columna’s weaknesses fall into three layers:

| Layer | Principal weakness |
|---|---|
| **Theory** | A grammar cannot certify real-world truth or analytical inference. |
| **Modeling** | Correctness depends on costly, accurate, continuously maintained Manifold declarations. |
| **Product** | The current implementation and independent evidence are still narrow and early. |

The sharpest critique is:

> **Columna relocates trust from the AI-generated query into the human-authored Manifold. That is probably a better place for trust, but it remains trust.**

Its long-term success will depend less on whether the four moods work in a demo—they do—and more on whether organizations can accurately author, test, maintain, integrate, and govern Manifolds at realistic scale without analysts routing around them.

---

*Compiled July 28, 2026.*
