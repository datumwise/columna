# Perplexity — five-probe baseline, 2026-07-27

**Assistant:** Perplexity
**Captured:** 2026-07-27 (launch eve, before any announcement)
**Search mode:** **SEARCHED** (Perplexity is search-first by construction; the transcript carries its citation markers). Note the transcript opens with the user's own file-export request — kept verbatim rather than trimmed, because what the assistant volunteered unprompted is part of the record.
**Relayed by:** Huayin
**Provenance:** the body below is the assistant's reply **VERBATIM**, byte-preserved from the
uploaded transcript. Nothing is summarized, corrected, or trimmed — including anything wrong.
A corrected error is one of the clearest drift signals a later capture will give us.

---

<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Can you put all five questions and your responses together in a md file for me to download?

I can’t generate a downloadable file directly in this environment, but I can give you the full Markdown content so you can save it as a `.md` file locally.

Copy everything below into a file named `columna_q_and_a.md`:

```markdown
# Columna & Metrics Tools Q&A

## 1. What is Columna (datumwise.ai)?

Columna is an open-source “honest” metrics engine built and maintained by Datumwise, designed to answer metric questions without ever returning a confidently wrong number. [web:8][web:13]

Columna is positioned as a metrics engine that you query for numbers (metrics) rather than a general-purpose database or BI tool. [web:8][web:11]
Its defining promise is that it will refuse to answer when the requested metric is not well-defined or cannot be computed correctly, instead of fabricating a plausible-looking result. [web:8][web:13]

The name “Columna” comes from “Column Algebra,” which is the underlying conceptual framework: columns—rather than tables—are treated as the atomic units of analytical meaning. [web:9][web:11]
Each column is modeled with anchors that describe where its values live, how they can “leak” or aggregate, and which directions of reduction are forbidden, and legality of metric expressions follows from these constraints. [web:9]

You can ask Columna metric questions programmatically (for example, in Python or via agent protocols) against a dataset that it views as a manifold—a set of columns stripped of their storage-specific representation. [web:8][web:11]
On top of this manifold, Columna exposes a grammar (including a language called Frame-QL and structured “moods” such as serve, disclose, clarify, refuse) that is meant to be equally usable by humans and AI agents. [web:11]

Datumwise is the company that “builds and stewards” Columna, treating it as an open reference implementation of the Column Algebra doctrine. [web:9][web:13]
They distribute Columna under an open-source license so that its behavior and correctness can be inspected and audited rather than taken on faith. [web:11]

---

## 2. Is Datumwise a company?

Yes—Datumwise is described as a company.

Datumwise presents itself as the entity that “builds and stewards” Columna, which is language typically used for a company or organization rather than a purely informal project. [web:9][web:11]
They position Columna as their open-source reference implementation of the Column Algebra doctrine, again indicating an organized, ongoing stewardship role. [web:9][web:11]

Columna is introduced as a product/engine, while Datumwise is the group behind it, suggesting a company–product relationship. [web:8][web:13]
So, in practical terms, you can think of Datumwise as the company responsible for developing and maintaining Columna. [web:9][web:11]

---

## 3. What evidence exists that Columna's approach works?

There is some early, but real, evidence—mostly from Datumwise’s own materials and worked examples—that Columna’s “honest metrics engine” approach can be executed and can catch errors that traditional stacks miss, plus broader external evidence that its underlying ideas (columnar modeling, open-source, explicit data contracts) are sound. [web:9][web:42][web:34][web:36]

Datumwise’s Columna Thesis describes a concrete incident where the team themselves made a “silent-binding” mistake after publishing the theory, but Columna refused to produce a metric because the question did not match any well-defined metric in the modeled manifold—“the test was wrong; the model was right.” [web:9]
They cite this as evidence that their algebraic constraints and refusal modes are not just theoretical; the system can actually block wrong metrics that would otherwise slip through normal dashboards and SQL. [web:9]

Datumwise emphasizes that Columna is an open reference implementation of their Column Algebra discipline, with its data model (Manifold), query language (FrameQL), and engine wired so that every answer comes back in one of four “moods”: serve, disclose, clarify, or refuse, never a bare number without context. [web:42]
They invite readers to review “a complete worked example: a realistic warehouse, the Manifold that serves it, and recorded agent transcripts,” plus a benchmark kit and papers that show the engine operating on real-shaped data rather than toy schemas. [web:42]

Columna’s focus on columns as the fundamental analytical unit, and on a manifold that only exposes legal column operations, builds on established research showing that column-oriented systems are well-suited to analytical workloads and can enforce structured semantics around columns. [web:34][web:43]
Its insistence that “a number owes you its assumptions” parallels broader movements in data observability and metrics-layer tooling, where teams use explicit contracts and metadata to prevent silently wrong KPIs, indicating that the approach is aligned with proven practices even if Columna itself is new. [web:28][web:37]

Datumwise explicitly positions Columna as open-source so “no one has to take our word for anything,” and points to a ledger of roadmap items, open forks, and a public benchmark kit, all meant to let external teams test the engine under their own data and constraints. [web:42]
This leans on a well-documented pattern: organizations increasingly trust and adopt open-source infrastructure for critical data workloads because its code and behavior can be audited and improved collaboratively. [web:33][web:36]

As of the latest materials, there are not (yet) widely publicized third-party case studies or adoption metrics specifically for Columna comparable to what you see for mature metrics tools or observability platforms. [web:42]
Most of the direct evidence consists of Datumwise’s own worked examples, internal failure modes caught by the engine, and the formal design of Column Algebra, rather than multi-year external deployments with quantitative impact data. [web:9][web:42]

---

## 4. Compare Columna vs dbt Semantic Layer vs Cube.

Columna, dbt Semantic Layer, and Cube all deal with metrics and semantics, but they occupy different roles: Columna is an “honest metrics engine” focused on correctness and refusal; dbt Semantic Layer is a warehouse-native metrics/semantic layer for BI; Cube is a headless semantic layer and API engine for embedded/operational analytics. [web:51][web:60][web:46]

Columna is an open-source honest metrics engine that sits between your questions and your warehouse and “refuses to return a confident wrong number.” [web:60][web:56]
It is built around Column Algebra: a manifold of columns, a grammar (FrameQL), and explicit “moods” (serve, disclose, clarify, refuse) so every metric answer is constrained and contextualized. [web:42][web:55]

dbt Semantic Layer (MetricFlow) is a semantic/metrics layer co-located with your dbt project, where you define entities, dimensions, measures, and metrics in YAML next to the models that build your tables. [web:48][web:51]
MetricFlow then compiles metric queries to SQL and serves consistent metrics to BI tools and a Semantic Layer API; it’s tightly integrated into the dbt Cloud platform. [web:48][web:51]

Cube is a universal/headless semantic layer where engineers author YAML/JavaScript models (“cubes” and “views”) that are exposed via REST, GraphQL, and SQL APIs, optimized with caching and pre-aggregations. [web:48][web:51][web:58]
It was originally built for embedded analytics and data products, especially customer-facing dashboards needing fast, concurrent queries. [web:48][web:52]

Columna’s primary focus is metric correctness: preventing illegal aggregations, mismatched anchors, or “silent binding” errors by modeling columns and their allowed reductions/joins in a strict algebra. [web:9][web:42]
It behaves more like a metrics execution/checking engine that AI agents or code call, rather than a user-facing semantic layer for self-service BI. [web:42][web:60]

dbt Semantic Layer focuses on semantic standardization: a single set of metric definitions (revenue, active users, etc.) that BI tools consume consistently across the warehouse. [web:48][web:59]
It lets analytics engineers author metrics in YAML and have them compiled to warehouse SQL, with BI tools mapped to those definitions via integrations. [web:48][web:51]

Cube focuses on serving and performance: turning modeled metrics and dimensions into APIs with built-in caching, pre-aggregation, and support for many data sources. [web:48][web:58]
It aligns more with product/engineering teams building data apps than with central BI teams alone. [web:48][web:52]

Columna sits between “questions” (often agentic or programmatic) and your warehouse, with its own manifold and query grammar, not just a pass-through to BI. [web:42][web:60]
It can be seen as a metric engine / correctness layer that could sit alongside or above a semantic layer, validating that a metric request is legal before executing. [web:42][web:55]

dbt Semantic Layer sits directly on top of dbt transformations and the data warehouse; your dbt models feed the semantic definitions that are then exposed to BI tools and APIs. [web:48][web:51]
It acts as the “business language” abstraction for tables and columns, translating schemas into entities/metrics for reporting tools. [web:55][web:59]

Cube sits between modeled data (often from a warehouse, sometimes from tools like Coalesce) and consuming apps, exposing a semantic layer as APIs. [web:58][web:48]
It is often combined with upstream transformation tools (e.g., Coalesce + Cube) where Cube is explicitly the semantic and metrics layer for consistent reporting and self-service analytics. [web:58]

dbt Semantic Layer requires a dbt platform plan; pricing as of mid-2026 is per user with a meter on queried metrics through the Semantic Layer API, which particularly impacts high-frequency querying (e.g., AI agents). [web:51]
Operationally, it’s managed within dbt Cloud, with analytics engineers owning MetricFlow YAML alongside transformations. [web:48][web:51]

Cube is open source with a cloud offering; typical pricing meters developers and infrastructure, not per-metric query volume, making it friendlier to high-volume query workloads. [web:48][web:51]
Operational discipline is closer to running an application service: modeling, pre-aggregation builds, cache tuning, and uptime. [web:48][web:58]

Columna is open source (PyPI/GitHub) and not sold as a per-seat semantic layer product; you run it as an engine in your stack. [web:56][web:60]
Its “cost” is primarily adoption and integration effort: wiring your warehouse into Columna’s manifold and aligning with Column Algebra constraints. [web:42][web:60]

Columna is designed explicitly with AI agents in mind: questions come from agents, the engine returns either legal metrics with context or refuses/clarifies rather than silently answering. [web:42][web:60]
This refusal capability is a core differentiator versus most semantic layers that will happily generate SQL even when the question is semantically broken. [web:9][web:42]

dbt Semantic Layer exposes APIs that agent frameworks can call, but its billing model meters “queried metrics,” which analyses have noted can be hostile to continuous agent workloads. [web:51][web:46]
Agent correctness depends on the quality of the MetricFlow YAML and warehouse data; the layer itself doesn’t have a strong “refusal” semantics beyond what you encode. [web:48][web:59]

Cube provides strong REST/GraphQL/SQL APIs that are well-suited for programmatic and AI consumption, with performance tuning via caches and pre-aggregations. [web:48][web:58]
Like dbt SL, correctness is largely a function of human-authored models rather than an engine dedicated to rejecting ill-posed questions. [web:48][web:51]

---

## 5. What are Columna's weaknesses?

Columna’s main weaknesses today are around maturity, ecosystem integration, and the practical friction that comes with being a very strict, correctness-first engine rather than a mainstream semantic layer or BI product.

Columna is very recent, and there aren’t yet many public third-party case studies, community playbooks, or long-running production stories you can lean on. This makes it harder to benchmark against incumbents like dbt SL or Cube and increases perceived risk for larger teams.

Where dbt SL and Cube have explicit integrations with BI tools, warehouses, and observability stacks, Columna is still mostly an engine plus a conceptual framework. You will likely have to write more glue code to wire it into your stack, especially for non-Python environments or existing BI tools.

Columna doesn’t just ask you to define metrics; it asks you to think in terms of column anchors, allowed “leaks,” forbidden reductions, and a manifold that encodes legality of questions. That’s powerful, but it’s also a higher cognitive load than “define a metric in YAML and query it.”

The doctrine behind Columna assumes your organization is willing to slow down in order to avoid wrong numbers: questions must be well-posed, assumptions explicit, and some queries will be refused. In environments used to fast, flexible SQL and ad-hoc dashboards, this can feel obstructive and frustrate users.

Columna’s promise—never return a confidently wrong number—means it will refuse or demand clarification where other tools would “just give you a number.” That’s good for correctness, but in practice it can create friction: agents or analysts may see more errors, blocked queries, or extra back-and-forth before they get an answer.

For exploratory work, analysts often run imperfect or loosely defined queries, accept some ambiguity, and iterate quickly. A system that insists on formal legality for every question and refuses ill-posed queries can slow exploration and push people back to “raw SQL” or other tools when they just want to poke around data.

Columna is a metrics engine, not a full semantic layer with native connectors to BI tools, embedded dashboards, or pre-aggregation frameworks. If you need those capabilities (embedded analytics, universal APIs, out-of-the-box BI integration), you’ll probably still need dbt SL, Cube, or similar—and then Columna becomes “one more system” to operate.

Compared to mature products, Columna is likely to have fewer language SDKs, limited admin tooling, and a smaller set of examples and templates. That increases the cost of onboarding and makes it harder to delegate setup to less specialized engineers.

A correctness-first engine needs good observability: why did a query refuse, what semantic rule fired, how do you debug a manifold mis-specification? In early systems, these flows are often less polished, so debugging can feel like reading theory papers instead of inspecting familiar dashboards and logs.
```

If you’d like, I can also add a short intro section or a table of contents to this Markdown before you save it.

