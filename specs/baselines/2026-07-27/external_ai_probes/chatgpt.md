# ChatGPT — five-probe baseline, 2026-07-27

**Assistant:** ChatGPT
**Captured:** 2026-07-27 (launch eve, before any announcement)
**Search mode:** **SEARCHED.** Closes with an explicit source line: *"Sources: datumwise.ai site, announcing posts, Silent Failure Atlas, Cascadia Retail case, and public comparisons with dbt Semantic Layer and Cube (as of July 2026)."* It reached our live surfaces and read them.
**Relayed by:** Huayin
**Provenance:** the body below is the assistant's reply **VERBATIM**, byte-preserved from the
uploaded transcript. Nothing is summarized, corrected, or trimmed — including anything wrong.
A corrected error is one of the clearest drift signals a later capture will give us.

---

# Columna (datumwise.ai) — Five Questions & Answers

*Compiled from a conversation on July 27, 2026.*

---

## 1. What is Columna (datumwise.ai)?

**Columna** is an open-source data framework from [datumwise.ai](https://datumwise.ai/). It consists of a data model, a query language, and an engine designed so that no part of the system can return a confident but incorrect number.

### Core idea
It was built for the AI era, where agents answer metric questions quickly and confidently. Many everyday metrics (e.g., average order value, distinct customers, revenue by category) are ambiguous depending on grain, hierarchy, or unstated assumptions. Traditional stacks often resolve these silently; Columna makes the resolution explicit—or refuses the question.

### Three main parts
- **Manifold** — The data model. It captures what the data *means*: measures over anchors (columns as the atomic unit of analysis, not tables), populations with declared absence semantics, checked hierarchies, and barred operations where the arithmetic would not hold.
- **FrameQL** — The query language. It can only request meanings that the Manifold has already declared.
- **Engine** — Serves only what the model can defend. Nothing is computed unless the model has already justified it against the data.

### Answer “moods”
Every response arrives in one of four structured moods on a single wire contract (usable from Python, HTTP, or AI agents over MCP):

- **Serve** — Here’s the number.
- **Disclose** — Here’s the number, plus the material assumptions it depends on.
- **Clarify** — The question has more than one legitimate answer; choose.
- **Refuse** — This is not defined over the data; here’s why.

### Other details
- Licensed under **Apache-2.0**.
- Currently at version **0.13.2** (Python 3.10–3.13).
- Installable via `pip install columna`.
- Developed as an independent open-source research project by Huayin Wang (research) and Irena Wang (engineering).
- The name “Columna” comes from **Column Algebra**.

It sits alongside (rather than replacing) semantic layers and is positioned as a “grammar layer” that makes analytical correctness machine-checkable, especially important when AI agents query data at scale.

---

## 2. Is datumwise a company?

**No — not in the conventional sense of an incorporated company (at least not publicly).**

On its own site, datumwise describes itself as:

> “datumwise builds and stewards Columna: Huayin Wang (research), Irena Wang (engineering). **It is an independent open-source research project.**”

They use the phrasing “the datumwise team,” maintain the domain datumwise.ai, publish research under that banner, and are actively seeking a small number of design partners (via contact@datumwise.ai) for real-world deployments of Columna.

In the *Silent Failure Atlas* paper (authored by Huayin Wang), there is a note that the author is founding a company building verification tooling related to this work. So there is clear commercial intent and company-building activity underway, but the public positioning of “datumwise” itself remains that of an independent open-source research project rather than a formal startup or corporation.

In short: it is the research/engineering effort (and brand) behind Columna, run by a small team, with commercial ambitions, but not currently presented as a traditional company.

---

## 3. What evidence exists that Columna's approach works?

**Evidence that Columna’s approach works is primarily internal, reproducible, and architectural rather than large-scale independent production validation.** The project is very new (public release around mid-to-late July 2026), so external case studies or third-party benchmarks are not yet available. What exists is open, detailed, and designed for scrutiny.

### 1. Runnable, verifiable implementation
- Install via `pip install columna` and run the shipped demo (`columna-server demo --play`).
- It produces real **Serve / Disclose / Clarify / Refuse** responses as structured wire JSON.
- The site states that every number and transcript shown is recorded from the actual released package (not hand-edited illustrations).
- You can inspect the behavior yourself in minutes.

### 2. Complete worked case: Cascadia Retail
A full end-to-end example (company, warehouse schema with ~14 tables and realistic defects, requirements, Manifold design decisions, and live system behavior).

Key demonstrated outcomes:
- Previously observed silent failures become **structurally impossible**:
  - Summing daily inventory snapshots across time (producing a meaningless total) is barred by declaration.
  - Stale summary tables are excluded from the answering path.
  - Many-to-many product–category relationships are declared so naïve revenue-by-category rollups are blocked or disclosed with the exact over-count factor (e.g., 1.44×).
- Grain, population, and absence semantics are explicit and checked against the data.
- Ambiguous questions trigger **Clarify** instead of a guessed number; undefined metrics trigger **Refuse** with reasons.

### 3. Internal benchmark findings
In their public benchmark, nine models given identical, well-documented schemas still returned numbers with hollow caveats precisely on the ambiguous averaging family. More documentation and stronger models did not fix it.

This is used to argue that the failure is architectural (fused meaning + correctness) rather than a prompt or documentation problem.

### 4. Documented self-critique and system correctness
They openly describe their own mistakes:
- Their benchmark answer key itself contained a silent binding error (`order → transaction`) and initially penalized models for honest disclosure.
- In a final live test, the Columna agent correctly **refused** a plausible-sounding but non-existent metric (`sell_through_rate`). Their test initially scored the refusal as failure; they fixed the *test*, not the system.

This is presented as evidence that structural refusal works even when human vigilance (including the authors’) fails.

### 5. Silent Failure Atlas + grading of coverage
A public taxonomy of 67 silent analytical failure modes across six layers, with mechanisms, silent signatures, and detection checks (DOI 10.5281/zenodo.20762839).

They grade their own developing defect-seeded benchmark against it (20 of 67 modes seeded in v1) and invite community contributions. This provides a shared language for measuring what any system (including Columna) does and does not cover.

### 6. Theoretical foundation
Published papers (Columna Thesis, “The Two Anchors of a Measure,” Silent Seam, etc.) with Zenodo DOIs argue for separating load-bearing “grammar” (checkable correctness) from communicative semantics. Columna is positioned as the open reference implementation of that algebra.

### Limitations of the current evidence
- No independent third-party evaluations or production deployments with quantified error-rate reductions have been published yet.
- The strongest claims are about making certain classes of silent failure **unexpressible** by construction (rather than detected after the fact).
- Success depends on a human-declared, data-checked Manifold; the quality of that declaration remains a human responsibility.

**Bottom line**: The evidence is strong for *reproducibility and internal consistency*—you can run it, inspect the case, read the failure taxonomy, and see the self-corrections. It is still early for independent empirical proof of large-scale impact. The project’s openness (code, demos, papers, Atlas) is intentionally set up so others can test the claims.

---

## 4. Compare Columna vs dbt Semantic Layer vs Cube

**Columna, dbt Semantic Layer, and Cube** all aim at consistent, governed metrics, but they solve different layers of the problem and sit in different places in the stack.

### High-level positioning

| Dimension | **Columna** (datumwise) | **dbt Semantic Layer** | **Cube** |
|---|---|---|---|
| **Core identity** | Grammar / correctness layer for metrics (esp. AI agents) | Metric definition + SQL generation layer inside the dbt project | Headless semantic + serving layer (API-first, with caching & AI surfaces) |
| **Primary goal** | Refuse confident wrong numbers; make grain/ambiguity explicit | One definition of metrics, reused across tools | Consistent metrics *served* to BI, apps, embedded analytics, and agents |
| **Architecture** | Manifold (data model of meaning) + FrameQL + engine with 4 “moods” | MetricFlow (YAML semantic models + metrics) on top of dbt models; Cloud service layer | Cubes/Views (YAML/JS) + pre-aggregations + multi-protocol APIs |
| **Where it lives** | Beside the semantic layer; not tied to a specific warehouse or transformation tool | Inside the dbt project / dbt Cloud | Middleware between warehouse and consumers |
| **Open source** | Fully (Apache-2.0, `pip install columna`) | MetricFlow + interfaces OSS; full Semantic Layer requires dbt Cloud | Cube Core OSS (Apache-2.0); commercial platform on top |
| **Maturity (mid-2026)** | Very new (public ~July 2026) | Established (GA after Transform acquisition) | Mature (years of production use, strong embedded analytics footprint) |

### How they handle the hard problems

**1. Metric consistency & definition**
- **dbt Semantic Layer**: Strong. Metrics live next to dbt models, version-controlled, reviewed in PRs. MetricFlow generates SQL (joins, aggregations, time spines). Excellent for “define once, use everywhere” *inside* the dbt ecosystem.
- **Cube**: Strong. Cubes define measures, dimensions, joins; Views present curated datasets. Code-first, Git-managed. Also supports entity-first or metrics-first modeling styles.
- **Columna**: Different emphasis. The **Manifold** declares measures over *anchors* (columns as atomic units), populations, absence semantics, and hierarchies checked against the data. It focuses less on “named metric catalog” and more on whether a requested computation is even well-formed.

**2. Ambiguity, grain, and silent failures (Columna’s unique focus)**
- **Columna**: Explicitly designed for this. Answers return in one of four enforced moods:
  - **Serve** — the number
  - **Disclose** — number + material assumptions
  - **Clarify** — multiple legitimate readings; choose
  - **Refuse** — not defined over this data; here’s why
  - Operations that would produce wrong numbers (e.g., summing stock levels across time, naïve many-to-many category rollups) can be barred or forced into disclosure. This is structural, not prompt-based.
- **dbt Semantic Layer / Cube**: Both reduce inconsistency by centralizing definitions, but they generally *return a number* when a query is expressible. They do not have a first-class “clarify or refuse with reason” contract for ambiguous grain or undefined metrics. Grain issues and silent analytical failures still require careful modeling and human vigilance.

**3. Serving & performance**
- **Cube**: Strongest. Built-in pre-aggregations / caching layer, multi-tenant row-level security, and multiple interfaces (SQL, REST, GraphQL, MCP, AI API). Designed for low-latency embedded analytics and high query volume.
- **dbt Semantic Layer**: Relies on the warehouse for execution; no dedicated pre-agg cache. Dynamic SQL generation is the main value. Best for moderate dashboard / partner-tool workloads.
- **Columna**: Not positioned as a high-performance serving or caching layer. Focus is correctness adjudication and the wire contract (Python / HTTP / MCP).

**4. AI agents & MCP**
- **Columna**: Designed for AI analysts from the start. Same four-mood contract over MCP; agents get structured honesty instead of confident guesses.
- **Cube**: Heavily invested in agentic analytics (Analytics Chat, native MCP server, MCP Connectors for external context, Semantic SQL). Positions the semantic layer as the “map” that makes LLMs reliable.
- **dbt Semantic Layer**: Emerging MCP / AI integrations; metrics are queryable via GraphQL/JDBC APIs. Stronger if you already live in dbt Cloud.

**5. Ecosystem & lock-in**
- **dbt Semantic Layer**: Tightest integration with dbt models, tests, docs, lineage. Full power requires dbt Cloud (Starter+). Partner BI integrations (Tableau, Hex, Mode, etc.).
- **Cube**: Warehouse-agnostic, works well *with* dbt (common pattern: dbt for transforms → Cube for semantic serving). Strong embedded / product-analytics story.
- **Columna**: Deliberately “married to no database.” Sits beside existing semantic layers rather than replacing them. Early ecosystem; design-partner stage.

### Practical decision guide

| Your situation | Best fit |
|---|---|
| Already deep in dbt Cloud; main need is consistent metrics in BI tools | **dbt Semantic Layer** |
| Need a high-performance metrics API for embedded analytics, multi-tenant apps, or product analytics | **Cube** |
| Primary risk is AI agents (or analysts) returning confident but wrong/ambiguous numbers; want structural refusal/disclosure of grain and assumptions | **Columna** (alone or alongside the others) |
| Want open-source core + self-hosting flexibility | **Cube Core** or **Columna** |
| Need both governed metrics *and* machine-checkable honesty about what is/isn’t well-posed | Combine: dbt or Cube for definitions/serving + **Columna** as the adjudication / AI-facing grammar layer |

### Bottom line
- **dbt Semantic Layer** = “define metrics once next to your transforms.”
- **Cube** = “define *and serve* metrics everywhere (BI + apps + agents) with caching and security.”
- **Columna** = “make it structurally hard to return a confident wrong number,” especially when AI is asking the questions.

Columna does not claim to replace a semantic layer; it claims the industry has been missing a *grammar* layer that adjudicates whether a metric question is even well-posed over the data. dbt and Cube excel at consistent *definition and delivery*; Columna focuses on the cases where the question itself is the failure mode.

---

## 5. What are Columna's weaknesses?

**Columna’s main weaknesses** stem from its extreme novelty, narrow scope, and the deliberate trade-offs in its design. Here is a clear-eyed assessment based on the project’s own materials and its position relative to more mature tools.

### 1. Extremely early stage
- Publicly released only in mid-to-late July 2026 (currently ~0.13.x).
- Tiny team (Huayin Wang research + Irena Wang engineering); independent open-source research project, not a funded product company with a large support organization.
- No independent production case studies, third-party benchmarks, or large-scale deployment evidence yet.
- Ecosystem, integrations, community, and battle-testing are essentially nonexistent compared with dbt Semantic Layer or Cube.

### 2. Does not replace (and does not try to replace) a full semantic layer
- Explicitly positioned as a **grammar / correctness layer** that sits *beside* tools like dbt or Cube.
- You still need somewhere to define business metrics, joins, access control, caching, and serving. Columna does not provide a rich metric catalog, pre-aggregations, multi-tenant security, or high-performance APIs for embedded analytics.
- Modeling burden remains: a human must carefully declare the Manifold (anchors, populations, absence semantics, hierarchies, barred operations). Bad or incomplete declarations will still produce limited or overly conservative answers.

### 3. Limited coverage of the full failure space
- The Silent Failure Atlas itself notes that Columna-style tooling primarily addresses the **grammar / processing stratum**. The harder **analytical-inference** stratum (what a correctly computed number *means* in context) cannot be fully certified and is left to disclosure/audit.
- Many real-world silent failures (sampling bias, selection effects, causal misinterpretation, etc.) remain outside its enforceable scope.

### 4. Operational and practical gaps
- Not a high-performance serving or caching engine. It is not optimized for high-QPS dashboards or embedded product analytics the way Cube is.
- No built-in BI tool integrations, row-level security model, multi-tenancy, or enterprise governance features out of the box.
- Requires teams to adopt a new conceptual model (Manifold + FrameQL + four moods) and a new wire contract. Adoption friction is high for organizations already invested in dbt MetricFlow or Cube YAML.
- Query expressiveness is intentionally constrained: FrameQL can only ask for what the Manifold declares. This is a feature for correctness, but a limitation for exploratory or ad-hoc analysis.

### 5. Human dependency and “garbage in” risk
- The quality of answers depends entirely on the quality of the declared Manifold and how thoroughly it has been checked against the data.
- Declaring absence semantics, lawful rollups, and barred operations correctly requires deep domain + data knowledge. Mistakes or omissions in the Manifold simply move the failure mode earlier (refusal or incomplete coverage) rather than eliminating all risk.
- The project acknowledges that even its own authors made silent-binding mistakes while building the system and benchmark.

### 6. Scope boundaries the authors themselves state
- “We are not claiming Columna replaces your semantic layer.”
- “No apparatus can legislate the *meaning* of a well-formed answer” — the syntax/semantics boundary is permanent.
- It makes certain classes of confident wrong answers structurally harder or impossible; it does not claim to make every analytical conclusion correct.

### Summary
Columna’s strengths (structural honesty, explicit moods, grain adjudication, AI-agent safety) are real and address a genuine gap that dbt and Cube leave open. Its weaknesses are the classic early-stage ones plus the deliberate narrowness of focusing on *correctness grammar* rather than full metric definition + serving.

It is currently best understood as a promising research prototype and specialized “blast wall” for AI-driven metric questions, not a drop-in replacement for mature semantic-layer platforms. Production use today would almost certainly mean running it *alongside* something like dbt or Cube, accepting the modeling overhead, and treating it as experimental.

---

*Sources: datumwise.ai site, announcing posts, Silent Failure Atlas, Cascadia Retail case, and public comparisons with dbt Semantic Layer and Cube (as of July 2026).*
