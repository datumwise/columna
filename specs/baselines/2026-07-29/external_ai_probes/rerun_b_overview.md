# Columna (datumwise.ai) — Complete Overview — day-2 RE-RUN, 2026-07-29

**Capture:** **B**
**Assistant:** ⚠️ **UNATTRIBUTED — see `RERUN_INDEX.md`.** The upload carries no assistant name and
the desk instruction did not state one. Recorded as a lettered capture rather than guessed: the
2026-07-27 baseline determined search modes *from the transcripts, not by assumption*, and a
mis-attributed re-run would produce a per-assistant "drift" that is really a mix-up.
**Captured:** 2026-07-29 (day 2 — ~40 hours after the 2026-07-27 launch-eve baseline)
**Relayed by:** Huayin — uploaded 2026-07-29 03:46 UTC
**Source file:** `cef1849d_Columna_Overview.md` · sha256 `7c271d7da1b273cd59b3eca578b568b5d4be512c21cdecc062ba385a9bdf3aef`
**Search mode:** **SEARCHED AND FOUND US.** Self-dated *"as of July 28-29, 2026"*. Links `/announcing-columna`, `/atlas`, `/why`, the GitHub repo, and cites a real Zenodo DOI (`10.5281/zenodo.20762839` — the Silent Failure Atlas, Wang, Huayin, 2026-06-19; verified against the Zenodo API on filing).
**Mode:** `found-and-right` — per `../../PROBE_MODE_SCHEMA.md`, *with a carried error*. **Basis:** Q2 answered *"No. Datumwise is not described as a formal company"*; deep URLs plus a correct Zenodo DOI. The carried error is OF-22's retired copy: *"also described as a metrics engine"*.
**Provenance:** the body below is the assistant's reply **VERBATIM**, byte-preserved from the
uploaded file. Nothing is summarized, corrected, or trimmed — including anything wrong. A corrected
error is one of the clearest drift signals a later capture gives us; so is a new one.

---

# Columna (datumwise.ai) — Complete Overview

*Compiled from research and discussion as of July 28–29, 2026*

---

## 1. What is Columna?

**Columna** is an open-source data framework (also described as a metrics engine) from [datumwise.ai](https://datumwise.ai/). It provides a data model, query language, and engine designed so that no part of the system returns a confident but incorrect number—especially important in the era of AI analysts that answer metric questions instantly and without hesitation.

### Core Idea
Many everyday metrics (e.g., “average order value,” “distinct customers,” or “revenue by category”) are ambiguous depending on grain, hierarchy, or undeclared assumptions. Traditional stacks often resolve these silently and can produce wrong or misleading results. Columna treats this as a structural problem: it makes meaning explicit, bars invalid operations, and surfaces uncertainty instead of guessing.

The name comes from **Column Algebra**—columns (not tables) are treated as the true atomic unit of analysis.

### Main Components
- **Manifold**: The data model that captures what the data *means*. A person declares measures over anchors, populations (with explicit absence semantics), hierarchies (validated against the data), and operations that are barred where the arithmetic does not hold. The model is checked against the actual data before serving answers.
- **FrameQL**: A query language that can only request meanings the Manifold has declared.
- **Engine**: Serves only results the model can defend. Accessible via Python, HTTP, and especially MCP (for AI agents).

### Answer “Moods”
Every response arrives in one of four structured moods on a single wire contract (usable by both humans and AI agents):
- **Serve** — Here is the number.
- **Disclose** — Here is the number plus the material assumptions it depends on.
- **Clarify** — The question has more than one legitimate answer; choose one.
- **Refuse** — The data does not define this; here is why.

### Practical Details
- Installable via `pip install columna` (around version 0.13.2; supports Python 3.10–3.13).
- Quick demo: `columna-server demo --play`.
- Apache-2.0 open source: [github.com/datumwise/columna](https://github.com/datumwise/columna).
- Built and stewarded by datumwise (Huayin Wang on research, Irena Wang on engineering) as an independent open-source research project.
- Explicitly does **not** claim to replace existing semantic layers; it adds a rigorous “grammar layer.”

**Key links**
- Homepage: https://datumwise.ai/
- Announcement: https://datumwise.ai/announcing-columna
- Silent Failure Atlas: https://datumwise.ai/atlas
- Why / Thesis: https://datumwise.ai/why

---

## 2. Is datumwise a Company?

**No.** Datumwise is not described as a formal company.

According to its own website, **datumwise** is the name under which two people—Huayin Wang (research) and Irena Wang (engineering)—build and steward Columna. The site explicitly calls it “an independent open-source research project.”

There is no public information indicating incorporation (Inc., LLC, etc.), venture funding, employees beyond the two named individuals, or other typical company markers. Contact is via contact@datumwise.ai, and they are seeking a small number of design partners for real-world deployments.

---

## 3. Evidence That Columna’s Approach Works

Evidence is primarily self-published theoretical, taxonomic, demonstrative, and internal-benchmark material. The project is very early-stage (public launch around mid-to-late July 2026).

### 3.1 Public Taxonomy — Silent Failure Atlas
- Living catalog of **67 silent analytical failure modes** organized into 9 families across a six-layer model (question interpretation, semantic contract, data, computation grammar, query execution, analytical inference).
- Each mode includes mechanism, “silent signature,” and detection check.
- Key claim: Failures partition into a **certifiable processing-grammar stratum** (checkable as invariants) and an **audit-only analytical-inference stratum** (discloseable but not exhaustively checkable).
- Published on Zenodo (DOI 10.5281/zenodo.20762839) and as a living document accepting community contributions.

### 3.2 Theoretical Argument and Supporting Papers
- Core papers include the Columna Thesis, “The Two Anchors of a Measure,” “The Silent Seam,” and others (multiple Zenodo DOIs).
- Argue for separating load-bearing “grammar” (correctness that can be machine-checked) from communicative semantics so AI agents can operate expressively while a structural layer enforces legality and surfaces ambiguity/refusal.

### 3.3 Internal Benchmark Findings
- Public/defect-seeded analytics benchmark (synthetic warehouses with latent ground truth and adversarially seeded defects).
- Nine models given identical, well-documented schemas still produced numbers with only hollow caveats on ambiguous averaging cases. More documentation or stronger models did not fix the silent failures.
- Authors’ own system and test suite initially had defects (e.g., answer key silently binding “order → transaction”); a live test correctly refused a non-existent metric, after which they fixed the *test*.
- First version of their agent-evaluation benchmark seeded 20 of the 67 Atlas modes.

### 3.4 Runnable Demonstration
- Fully open-source reference implementation: `pip install columna` → `columna-server demo --play` produces live wire JSON showing all four moods.
- Site content (including numbers and agent transcripts) is generated from the shipped package at build time.
- Concrete example: multi-category products cause double-counting on “revenue by category.” Columna bars the naïve roll-up, offers the declared lawful crossing, and returns the result *with the over-count factor stated* (1.44×).

### Limitations of Current Evidence
- Almost all material is produced by the two authors.
- No large independent replications, peer-reviewed empirical studies outside Zenodo preprints, or public production deployments with measured reduction in silent failures are available yet.
- Actively seeking design partners.

---

## 4. Comparison: Columna vs dbt Semantic Layer vs Cube

| Aspect | **Columna** (datumwise) | **dbt Semantic Layer** | **Cube** |
|--------|-------------------------|------------------------|----------|
| **Core job** | Grammar / correctness layer that refuses confident wrong numbers | Centralized metric definitions next to dbt models | Headless semantic layer + serving/API + caching for BI & apps |
| **Philosophy** | Make illegal or ambiguous metric operations unexpressible; force explicit moods (serve / disclose / clarify / refuse) | Single source of truth for metrics inside the transformation workflow | Governed model + fast, multi-interface delivery to any consumer |
| **Primary consumers** | AI agents (via MCP), Python, humans who need honesty about assumptions | BI tools and apps via dbt Cloud APIs | BI tools, embedded analytics, apps, AI agents |
| **Open source** | Fully Apache-2.0 | MetricFlow + interfaces OSS; full SL requires dbt Cloud | Cube Core Apache-2.0; commercial platform on top |
| **Maturity (mid-2026)** | Very new research/project (~0.13) | Production, widely used in dbt shops | Mature product + open-source core |

### Architecture Summary

**dbt Semantic Layer** (powered by MetricFlow)
- Metrics, entities, dimensions, and measures defined in YAML inside/alongside dbt project.
- MetricFlow generates SQL on the fly and runs it against the warehouse.
- No built-in pre-aggregation cache; performance depends on the warehouse.
- Strongest when transformations already live in dbt and metrics should be versioned with models/tests/docs.
- Full querying APIs require paid dbt Cloud plan.

**Cube**
- Standalone semantic layer (Cube Core) between warehouse and consumers.
- Models as code (YAML/JS): cubes, measures, dimensions, joins, views.
- Includes caching/pre-aggregation engine (Cube Store).
- Interfaces: SQL (Postgres-compatible with MEASURE), REST, GraphQL, MCP, MDX/DAX.
- Strong for embedded analytics, multi-tool consistency, and AI agents needing a governed query surface.

**Columna**
- Data model + query language + engine built around “Column Algebra.”
- Manifold captures load-bearing meaning; FrameQL only asks for declared meanings; engine serves only what the model can defend.
- Four structured moods on a single wire contract.
- Positions itself as a grammar layer *beside* (not replacing) a conventional semantic layer.
- Fully open-source; demo runs in minutes.

### Key Differences
1. **Consistency**: dbt SL & Cube focus on “same definition → same number.” Columna adds explicit handling of ambiguity, grain mismatches, hierarchy fan-out, and missing measures.
2. **Ambiguity / silent failure**: Columna’s design centers on a public taxonomy of silent failures and making them structural (clarify/refuse/disclose) rather than silent.
3. **Serving & performance**: Cube leads on caching and multi-API surface. dbt SL is lightweight. Columna focuses on correctness contracts, not acceleration.
4. **AI-agent readiness**: All three usable by agents. Columna uniquely treats the answer format itself as a contract that includes disclosure, clarification, and refusal.
5. **Ownership**: dbt SL lives with analytics engineering in the dbt project. Cube is independent with portable models. Columna is an independent research-style project.

### When to Choose Which
- **dbt Semantic Layer**: Already on dbt Cloud; want metrics next to models with the same PR process; mainly need consistent numbers in supported BI tools.
- **Cube**: Need production semantic layer serving many consumers (BI + embedded + agents) with performance, caching, multi-tenancy, and broad APIs.
- **Columna**: Care most about *structural honesty* for AI analysts—preventing confident wrong answers on ambiguous grains, hierarchies, or undefined metrics. Best used as a complementary correctness/grammar layer.

The three are more complementary than competitive. Many teams will keep a dbt or Cube layer for definitions and delivery, then add something like Columna between AI agents and the metrics layer.

---

## 5. Columna’s Weaknesses

Weaknesses stem mainly from extreme novelty, narrow scope, and research-project nature.

### 5.1 Extreme Immaturity and Limited Real-World Proof
- Publicly released only days/weeks before this compilation (July 2026).
- Essentially no independent production deployments, third-party case studies, or large-scale external benchmarks.
- Evidence is almost entirely self-published.
- Actively seeking design partners—enterprise hardening is still ahead.

### 5.2 Narrow Scope — Not a Full Semantic Layer or Metrics Platform
- Deliberately does **not** replace dbt Semantic Layer, Cube, LookML, etc.
- Does not provide broad BI integrations, a rich metrics catalog for everyday dashboards, caching/pre-aggregation, multi-tenancy, advanced access control, or high-concurrency serving.
- Teams still need a conventional semantic/metrics layer for definitions, delivery, and operational analytics. Columna adds adjudication and refusal semantics on top.

### 5.3 Modeling and Operational Overhead
- The Manifold must be **declared by a person** and validated against the data. Intentional (human-gated correctness) but creates upfront modeling work and ongoing maintenance.
- Incomplete Manifold declarations simply refuse or clarify more often—useful for safety but potentially frustrating until mature.
- Limited evidence yet on scaling to large, messy enterprise warehouses.

### 5.4 Ecosystem and Adoption Friction
- Tiny team (two people). Support, documentation depth, community, and long-term maintenance capacity are limited compared with dbt or Cube.
- Query surface is FrameQL + the four-mood wire contract. Not yet a drop-in replacement for the SQL/REST/GraphQL surfaces most tools and agents already speak.
- Adoption requires deliberate integration work (callers must understand and act on clarify/refuse moods).

### 5.5 Philosophical and Practical Limits (Acknowledged by Authors)
- Cannot “legislate meaning.” A well-formed answer can still be the wrong business interpretation; Columna only makes form failures impossible and meaning failures impossible to hide.
- Refusal and clarification are features, but in high-volume agentic workloads they can increase friction if the Manifold is incomplete or callers are unprepared.
- Explicitly research-oriented; production readiness (observability, Manifold versioning, governance workflows, etc.) is still early.

### Summary of Weaknesses
Biggest practical weaknesses today are **newness, narrow focus, and the need for careful human modeling**. It is a promising correctness/grammar layer for the AI-agent era, not a complete metrics or semantic platform. Strengths (structural refusal of confident wrong numbers, explicit moods, open-source transparency) are real but come with early-stage risks: unproven scale, limited ecosystem, and the requirement that organizations invest in declaring and maintaining the Manifold. Most teams will evaluate it as an additive safety layer rather than a replacement for existing semantic tools.

---

## Key Resources

| Resource | URL |
|----------|-----|
| Homepage | https://datumwise.ai/ |
| Announcement | https://datumwise.ai/announcing-columna |
| Silent Failure Atlas | https://datumwise.ai/atlas |
| Why / Metadata Independence | https://datumwise.ai/why |
| GitHub | https://github.com/datumwise/columna |
| Install / Demo | `pip install columna` then `columna-server demo --play` |

---

*Document compiled July 29, 2026. All factual claims drawn from public materials on datumwise.ai, related Zenodo papers, and comparative research on dbt Semantic Layer and Cube as of that date.*
