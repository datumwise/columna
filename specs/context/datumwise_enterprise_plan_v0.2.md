# Datumwise enterprise plan v0.2 — Columna Core, Columna Server, and the company surface

**v0.2:** all seven forks ruled (§11 now records the rulings); application named **Columna Server**;
naming ladder Core → Server → (future) Cloud adopted throughout.

Scope: everything in flight — the open-source library, the application around it, the Authoring
Agent, the MCP/agent surfaces, and the Datumwise.ai website — as one coherent build, sequenced into
work packages sized for Claude Code / Cursor, each backed by a spec I write before code is cut.

---

## 0. Code-audit baseline (what exists today, from reading v0.7.7-core)

Answering the "not sure if it already includes" list from the actual tree, not memory:

| target | status in v0.7.7-core |
|---|---|
| column engine on Polars | **EXISTS** — `engine.py`, Polars is the processing substrate; transport-based, no join pushdown |
| planner module | **EXISTS** — `planner.py`, provenance-blind, static fan-out/out-of-universe refusal, four outcomes at one chokepoint (ADR-032 D3/D4, v0.7.4–0.7.7) |
| DuckDB backend | **EXISTS** — `connector.py` `DuckDBConnector`, single-table delivery only |
| Polars backend (no DuckDB) | **MISSING** — connector is DuckDB-only today; a `PolarsConnector` over parquet/CSV is new work |
| Frame-QL API | **EXISTS** — `frameql.py` (`ManifoldServer`, `Frame`, `on_universe` pin) + `parser.py` (textual `.cml` Manifold format) |
| disclosure / refusal objects | **EXISTS** — `disclosure.py`; structured `Outcome` (kind·discriminator·reason·alternatives) as data, never exceptions; severity lattice |
| OperatorRegistry | **EXISTS** — `operators.py` with signatures (`signature_ok`, `output_dtype`), algebraic classes (value/ordered/holistic/sketch); local-override layer is new work |
| custom types + sketches | **EXISTS** — `types.py`, `sketch.py` (HLL via datasketches; witness store; stored-not-cached) |
| retail demo dataset | **EXISTS in substance** — `benchmark.cml` + `build_benchmark.py` against the 299,934-txn benchmark warehouse; needs packaging (bundle or downloader) |
| tests | 124 checks / 11 suites as demo scripts — needs pytest conversion for OSS credibility |
| known open items | ADR-032 **Option B** (true cross-universe confinement); MCP family-triple descriptor; disclosure-category adapter to the benchmark's `{code, materiality}` schema |

Net: **the library is ~80% of target.** The genuinely new builds are: Polars backend, Manifold
management, the Authoring Agent, the query UI, the MCP server + query agent, docs/packaging, and the
website. Nothing in the existing core needs rearchitecting to support them — ADR-032 D7/D8 already
specifies the server topology and "NL agent as MCP client."

---

## 1. Positioning (the strategic spine everything hangs on)

Carrying forward the market finding: the semantic-layer category is crowded and converging on OSI,
and its universal theory of correctness is *governance* — one definition, enforced everywhere. The
open seat is the layer that knows **governance solves drift, not ambiguity**: a governed, versioned,
OSI-compliant metric can still be structurally multi-valued, and no naming discipline touches that.

**Columna's position: the honest metrics engine.** Not another semantic layer — the
verification-and-disclosure engine that sits *beside or under* governed definitions and supplies
what none of them have: structural-ambiguity detection (two anchors, universes, B-anchors), the four
outcomes (serve · disclose · clarify · refuse), and structured, materiality-gated disclosure. The
wedge audience is AI analytics: **the first metrics engine an AI agent can query that can say "it
depends."** The benchmark is the proof asset (models given governed docs still failed on exactly the
averaging family); the MCP server is the demo that makes it visceral.

Interop, not war: an **import path from dbt/OSI semantic definitions** ("point Columna at your
semantic layer; it tells you which of your metrics are structurally ambiguous") is the single
highest-leverage adoption feature on the roadmap — zero-to-value without full authoring.

## 2. Product line and naming

- **Columna Core** — the open-source Python library (`pip install columna-core`). What exists today.
- **Columna Server** [RULED] — the application: Authoring Agent + Manifold library + query workbench
  + MCP endpoint, one deployable (`docker run columna/server` as the canonical quickstart). "Server"
  names the deployable unit, ships its own web console (Grafana/Airflow pattern), and rhymes with a
  future hosted tier the industry-standard way (Server → Cloud). "Studio" survives only as the
  label for the authoring surface *inside* Server, where the word is accurate.
- **Datumwise.ai** — the company surface: site, research corpus, blog, site agent.
- **Future commercial** — Datumwise Cloud (hosted Studio, teams, SSO, governance workflows,
  allocation/Pro features — ADR-032 already reserves "allocation = Pro"). Not built now; the
  boundary is drawn now so the OSS scope is a decision, not an accident.

## 3. Open-source strategy

- **License:** Apache-2.0 for Core and Studio. Infra practitioners distrust BSL for a new
  category-defining engine; the moat is the theory + research corpus + pace, not the license.
  [Fork 3-A.]
- **Open-core boundary:** the Authoring Agent ships open with **BYO LLM key**, and its deterministic
  layers (introspection, FD discovery, attestation) work with **no LLM at all** — LLM-off authoring
  is a first-class mode, not a degraded one. Commercial value accrues later in hosted/teams/scale,
  not by withholding the agent. [Fork 3-B.]
- **Repo:** monorepo `datumwise/columna` — `packages/columna-core`, `packages/columna-studio`,
  `apps/website`, `docs/`, `research/` (papers, Atlas, benchmark pointers). [Fork 3-C.]
- **Launch narrative:** the benchmark finding ("we tested 8 frontier models on governed
  docs; they served numbers with hollow disclosures precisely on the averaging family") + the MCP
  demo. Research corpus (two DOIs + Atlas + benchmark) is the content moat; the datumwise v2
  article is the launch post.

## 4. System architecture (four layers, grounded in ADR-032)

```
L3 surfaces    web UI (authoring wizard · query workbench) | MCP tools | site agent
L2 services    Manifold store · Authoring service · Query service · MCP server
L1 library     columna-core: model · operators · types · projection · planner · engine
               · disclosure · frameql · parser · sketch          [exists, v0.7.7]
L0 backends    DuckDBConnector [exists] · PolarsConnector [new] · capability contract [new]
```

One contract everywhere (ADR-032 D8): every surface — Python API, MCP tool, web workbench, agent —
returns the same `FrameResult` with the same outcome/disclosure structure. No surface gets a
different truth.

**Backend capability contract (new, small):** what a connector must provide (single-table measure
delivery, edge delivery, base rows) and may provide (profiling pushdown: distinct counts, group-by
cardinalities for FD discovery; witness storage). FD-DAG discovery has a pure-engine fallback so no
backend is *required* to implement it.

## 5. The Authoring Agent (the centerpiece new design)

**Doctrine first — this resolves your original no-LLM stance rather than abandoning it:**
**LLM proposes; deterministic layers verify; data attests; the human declares.** Nothing enters a
Manifold on LLM say-so. Every property of every ColumnSpec carries one of three provenance states —
**inferred / declared / data-attested** — and the planner already knows how to surface spec-only
provenance caveats (v0.7.1). Note the continuity: this tri-state is exactly the 3-state
classification the two-anchor paper deferred to "future automated Manifold authoring" — this agent
is that future artifact, and the benchmark's model-proposes/layer-checks result is its empirical
justification.

**Pipeline (matches your flow, with the verification stage made explicit):**
1. **Connect & select** — backend + sources; schemas/tables/files; column selection (dimensions vs
   measures).
2. **Introspect (deterministic, no LLM)** — dtypes, null profiles, cardinalities, key candidates;
   **FD-DAG discovery** (sampled approximate FDs via group-by profiling, full-scan verification on
   acceptance) → candidate functional edges + V-anchors, *data-attested*.
3. **Propose (LLM, optional)** — reads SQL code, docs, quasi-metadata (dbt YAML, dashboard configs,
   column names) → proposes families, family reducers, V/M/B anchors, universes + predicates,
   derived columns, dimension families. Everything it emits is *inferred*.
4. **Attest (deterministic)** — run the checkable subset against data: FD edges verified; universe
   predicates evaluated (population counts, out-of-domain demonstration); V-anchor keying checked;
   family consistency law (members agree under the reducer) spot-checked. Passing items upgrade to
   *data-attested*.
5. **Declare (human, web UI)** — review queue ordered by (materiality × uncertainty); the human
   confirms/overrides; confirmed items become *declared*. The UI shows *why* for every proposal
   (the SQL line, the doc sentence, the profiling result).
6. **Emit** — Manifold artifacts (`.cml` + canonical JSON), per-column specs {family, reducer,
   dtype, V/M/B, permitted/blocked operators, provenance per property}, universe specs, derived
   columns, and a **local OperatorRegistry override** (global registry + per-manifold/per-engine
   additions: custom reducers/functions with signatures {name, input dtypes, output dtype,
   algebraic class, B-implications}).

**The checkability table (goes in the spec verbatim; it is the honesty boundary):**
- *Data-attestable:* functional edges, V-anchors, universe predicates, cardinalities, coverage,
  family consistency.
- *Registry-known:* path-independence/fertility of reducers, operator algebra.
- *Must be declared (cannot be attested):* M-anchor mechanism (MNAR is undetectable from data by
  definition), B-anchor semantics (stock vs flow — inferable from names/docs, never provable),
  extensive/intensive. The agent proposes these; only a human declaration upgrades them.

## 6. MCP server + query agent (the wedge product)

- **Tools:** `list_manifolds`, `describe_manifold`, `describe_measure` — exposing the per-family
  **triple (family-root, member-anchor set, family-reducer)** [the pending descriptor item] —
  `query` (Frame-QL text), `explain` (plan-without-execution, already supported by the library).
- **Response contract = the benchmark's disclosure schema**, productized: outcome ∈ {serve,
  disclose, clarify, refuse, error}; disclosures as `{code, materiality, severity, assumptions,
  detail}` [the pending disclosure-category adapter]; clarifies carry named alternatives so the
  *calling agent* can round-trip the question to its user and re-query. This is the demo: an AI
  asks for AOV, gets `clarify: per order / per line / per customer`, asks its human, re-queries,
  serves with a materiality-gated disclosure. No other metrics MCP server does this.
- **Query agent** = thin NL client over MCP (ADR-032 D8 verbatim). NL → *proposed* Frame-QL →
  planner validates → outcome. The agent never bypasses the planner; the same
  proposes/checks division of labor.

## 7. Datumwise.ai website

- **IA:** Home (wedge message + live "ask it AOV" widget) · Product (Core / Studio / MCP) · Open
  Source (quickstart, GitHub) · **Research** (Atlas DOI, Two-Anchors DOI, benchmark findings — the
  credibility engine, most competitors have nothing like it) · Docs · Blog (launch = datumwise v2
  article) · Company.
- **Site agent:** the query agent pointed at (a) a RAG corpus of docs/papers/manuals and (b) the
  live retail demo Manifold via the public MCP server. Dogfooding is the message: the sales agent
  answers metric questions *through Columna* and visibly clarifies/discloses. One agent, two tools.
- **Design language:** anti-hype, technical-honest; the disclosure aesthetic (caveats as a design
  element, not fine print). Static site + one interactive demo island. [Fork 7-A: stack — rec:
  Astro/Next static + the widget calling a hosted MCP endpoint.]

## 8. Work packages and sequencing

Phases gate on demos, not dates. Each WP gets a written spec from me before code; Claude Code /
Cursor implements against acceptance tests + a demo script.

**Phase 0 — release engineering** (unblocks everything)
- WP-0.1 monorepo layout, packaging (`pyproject`, pypi `columna-core`), CI.
- WP-0.2 convert the 124 checks / 11 demo suites to pytest (keep demos as executable docs).

**Phase 1 — library completion**
- WP-1.1 `PolarsConnector` (parquet/CSV, no DuckDB) + backend capability contract.
- WP-1.2 canonical JSON Manifold serialization (alongside `.cml`), round-trip tested.
- WP-1.3 disclosure-category adapter → `{code, materiality, severity, assumptions, detail}`.
- WP-1.4 ADR-032 Option B (cross-universe confinement) — **deferred, explicitly**, does not block
  launch [Fork 8-A confirms].

**Phase 2 — the wedge (launchable moment)**
- WP-2.1 Manifold store (directory + catalog; a library of Manifolds per installation).
- WP-2.2 MCP server (§6), stdio + HTTP.
- WP-2.3 retail demo packaging (bundled small warehouse + `benchmark.cml` + quickstart:
  pip install → query → see a clarify in 10 minutes).
- WP-2.4 query agent demo (NL over MCP).
→ **OSS launch**: repo + pypi + MCP demo + launch post.

**Phase 3 — authoring**
- WP-3.1 deterministic introspection + FD-DAG discovery (LLM-off authoring works end-to-end).
- WP-3.2 LLM propose layer (BYO key; provider-agnostic; every output provenance-tagged *inferred*).
- WP-3.3 attestation jobs + review-queue backend.
- WP-3.4 authoring web UI (wizard per §5 pipeline).
- WP-3.5 dbt/OSI import path (read their YAML as quasi-metadata into the propose stage).

**Phase 4 — Server assembly**
- WP-4.1 query workbench UI; WP-4.2 docs site (mkdocs/docusaurus) from the manuals.

**Phase 5 — company surface**
- WP-5.1 website; WP-5.2 site agent (RAG + MCP tools).

Sequencing logic: **MCP demo before Authoring Agent.** The demo Manifold is already hand-authored
(`benchmark.cml`); the wedge story needs no authoring UI. Authoring is the growth unlock ("your own
data") and the biggest lift — it lands as the second wave with its own announcement.

## 9. Handoff protocol (how this becomes Claude Code work)

Per WP I produce: **spec.md** (goal, context files to read, interfaces/types, invariants that must
hold, acceptance tests as pytest stubs, demo script, out-of-scope list). Claude Code implements in a
branch; acceptance = tests green + demo runs + no changes outside the WP's stated surface. The specs
cite the manuals/ADRs by section so the implementer inherits the locked vocabulary (planner vs
column engine; measure family; the four outcomes) instead of reinventing it.

## 10. Risks

- **Solo-founder scope.** Mitigation: every phase is independently valuable and shippable; Phase 2
  alone is a launch.
- **LLM in OSS.** Mitigation: LLM-off is first-class (§5); BYO key; provider-agnostic.
- **Crowded-market messaging.** Mitigation: beside-not-against positioning; the import path; the
  research corpus as differentiation no competitor can fast-follow.
- **Name collision** (Core-the-lib vs Core-the-app). Mitigation: Fork 2-A.

## 11. Rulings (all seven forks resolved)

1. **2-A** Application name: **Columna Server** (ladder: Core → Server → future Cloud; "Studio"
   demoted to the authoring surface inside Server). Follow-up task, not a fork: trademark/collision
   scan on "Columna" before the repo goes public.
2. **3-A** License: **Apache-2.0**.
3. **3-B** Authoring Agent: **open, BYO LLM key**; LLM-off authoring first-class.
4. **3-C** **Monorepo.**
5. **8-A** ADR-032 Option B **confirmed deferred** past launch.
6. **7-A** Live MCP widget **in scope for site v1**.
7. **Sequencing:** **MCP-first.**

## 12. Immediate next actions

1. Your rulings on §11.
2. I write **WP-0.1/0.2 spec** (repo + tests) and **WP-2.2 spec** (MCP server — the most
   design-sensitive, since its response contract is the productized disclosure schema) first.
3. Package check: confirm the retail warehouse subset small enough to bundle, or spec the
   downloader (WP-2.3).
