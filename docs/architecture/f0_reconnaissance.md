<!-- Durable architecture record. FROZEN: this is the F0 reconnaissance as reviewed,
     not a living design doc. S1.x / Core-P1 / Platform design lives elsewhere. -->

# F0 — Architecture-Split Reconnaissance (integrated report)

Reconnaissance only. No structural code. Current `main` is authority.

## Rulings incorporated (Huayin, 2026-08-12)

1. **`.cml` is a Core-private execution image, NOT the shared↔Core contract.** The shared boundary is a **governed logical publication** (logical Manifold + identity/version + ratified law + governance/provenance) with **private realization attachment(s)**; below it sit the Core compiler→`.cml`/runtime image and, separately, a Platform provider→identity runtime. Do not promote `manifold.columna.yaml` to the shared contract.
2. **The missing lowerer is a *Core compiler*** (governed publication + private Core realization → Core execution image). It belongs to Core because its output is a Core representation, but it **consumes a stable governed publication contract, does not import Studio**, and must not put authored-Manifold semantics into `ColumnEngine` nor Core-execution semantics into Studio. Exact placement (likely a separate compiler module in the `columna` codebase, not literally `columna_core.lower`) is a Core-P1 decision.
3. **Two publication artifacts stay conceptually distinct** — *governed logical publication* (what it means + identity + ratification) vs *private realization* (how it's realized for a given provider). May bundle operationally; Core and Platform may realize the **same** logical publication differently. Authored Manifold stays physical-clean.
4. **`draft.lower_to_cml` is a Core-local bootstrap path, not the production compiler.** There must ultimately be **one** semantic route into a governed Core execution image; whether draft feeds that same compiler or stays a dev convenience is deferred to Core-P1.
5. **`manifold.columna.yaml` = dead-end scaffolding today** — do not remove during seam work, do not design around it; Core-P1 either justifies or retires it.
6. **S1 is the next unit, not Core-P1.** The serving surface must stop knowing its provider is `ManifoldServer + ColumnEngine` before a second runtime exists. First provider = adapter over today's Core, **no behavior change, no semantic-law movement.**
7. **S2 registry is defined around the governed publication, not `.cml`.** Registry answers *WHICH governed Manifold* (`ManifoldRef{manifold_id, version}` + lifecycle); provider answers *HOW served*. Neither the folder-with-`manifold.cml` convention nor the Studio library layout is the shared abstraction.
8. **Core-P1 begins only after S1/S2** — then the old P1 findings are Core-P1 input (compiler placement, input schema, attribute/predicate/measure/hierarchy/boundary realization, refusal report, disposition of `manifold.columna.yaml` and `draft.lower_to_cml`).
9. **Platform-P1 is independent and does not start from `.cml`** — first unit is the certificate/identity-survival crossing spike.
10. **Polars→DuckDB: C2 before C3, approved.** Rule: *make the semantic decision explicit independently of the substrate, then let the substrate implement it* (LAW → EXECUTION DIRECTIVE → SUBSTRATE, e.g. "alignment domain = full outer" → `FULL_OUTER_JOIN` → Polars now / DuckDB later). The substrate interface emerges from ruled operations, not from wrapping dataframe APIs. **Corrected wording:** "execution can move all the way to the source freely" was too strong — see the revised Spine answer below.
11. **Ownership wording corrected:** the semantic spine is **SEMANTIC AUTHORITY: SHARED**, but its **current implementation location spans packages** (manifold-agent + planner + adjudication + ColumnEngine). It need not move now; future Core and Platform must **consume the same authority**, never reimplement it. *Two physical runtimes are acceptable; two meanings of a measure are not.*
12. **Canonical identity (J_m) accepted as a negative result** — absent today; cache/witness keys and the overloaded `member` are not identity; the present mechanisms are valuable **seeds**; Platform's identity runtime is genuinely new architecture (which strengthens the split).

Read the ownership map (§3) and completion answer #1 with ruling #11's wording: "SHARED" = *semantic authority shared*, implementation currently distributed across packages.

## 0. Reproducibility (repo hygiene)

| repo | main @ | note |
|---|---|---|
| datumwise/columna | `164d3d1` | P0(c) spec refresh #157 merged |
| datumwise/columna-studio | `d4d57d3` | P0(c) governed gate merged as **#11** |
| datumwise/manifold-agent | `9a77765` | one **untracked** local test `tests/test_p0c_governance.py` (not on main; ignored) |
| datumwise/manifold-eval | n/a | **out-of-path**: authoring-instruction eval harness; imports `manifold_agent` only to validate model output (`measure.py:29-30`) |

Local working state that is NOT authority: studio was on `p0c-governed-publish` (the pre-squash source of #11 — same content); columna was on the docs branch. Both reset to `main`. All findings below reproduce from `main`.

**Historical note (F0 closeout):** research scripts under `specs/open_planner/` reference the pre-S1.1 `LoadedManifold.server` API and are **intentionally not migrated** — they document the API that existed when those experiments were run. No compatibility obligation should be inferred from them.

Package-dependency DAG (from pyprojects; import-verified):

```
authoring:   columna-studio ──→ manifold-agent @ v0.11.0 (git tag pin)
execution:   columna (meta) ──→ columna-core ←── columna-server
             columna-core ──→ polars, duckdb, pyarrow   (self-contained)
             manifold-agent ──→ duckdb (gates/profiling)
```

- `columna-studio` imports **no** `columna_core` (grep empty). `columna` (core/server) imports **no** `manifold_agent`/`columna_studio` (grep empty). The two trees are import-disjoint.
- `columna-core/pyproject.toml` names a future `PolarsConnector` / optional-duckdb restructure ("WP-1.1"). Treated here as **design-intent evidence only** — the call-path trace is authoritative.

## 0.1 Discrepancy resolved: the artifact handoff is INCOMPLETE

An earlier interim note called the Studio↔Core bridge "`.cml` written at publish." That was imprecise and is **corrected**. Verified on main:

- Studio/manifold-agent write `manifold.yaml` (logical superset), `manifold.columna.yaml` (logical downgrade via `to_engine_yaml`), `mapping.yaml` (private realization). **They never write `.cml`** (only docstrings mention a future "real .cml lowering": `manifold.py:288,345`).
- **`manifold.columna.yaml` has no reader** anywhere in the three repos — write-only/dead-end.
- The engine consumes **`manifold.cml`** (`store.py:8,61` `parse_file`), produced by `columna_core.draft.lower_to_cml` (`draft.py:106` ← `init/loop.py:117`) or hand/demo fixtures — **never from the authored Manifold + mapping**.

```
AUTHORING TREE                         ENGINE TREE
Studio → manifold-agent                .cml + data.toml
      ↓                                      ↓
manifold.yaml (superset)              columna-core / columna-server
manifold.columna.yaml (downgrade)            ↓
mapping.yaml (private)                 Polars / DuckDB(source) / Arrow
      │
      └───────── ⌀ NO HANDOFF ─────────────┘   ← the Core compiler/lowering boundary is MISSING
```

**Architectural consequence:** the split does not require untangling a dependency knot — it requires *defining the contract that is currently absent* between two already-separated domains.

## 1. Headline

1. **The Core compiler is not decoupled — it does not exist yet.** No code turns (authored Manifold + mapping) into the runtime `.cml` the engine reads. Studio's governed lowering emits a dead-end YAML; the engine runs a `.cml` with no governed/authored source.
2. **Analytical meaning is decided in `columna-core`** — the planner's static adjudication, the engine's runtime governance (ASSIGN/ALLOC/TOUCH, Φ absence, confinement, series-reduce), and the adjudication Certificate kernel — plus, at ~19 sites, **inside the Polars expressions themselves** (directive-7). It is NOT decided in the connector/source, and NOT in any identity runtime (that layer is a target).
3. **The governed wire is already a clean provider seam;** the couplings to break are above it (`store` construction, `ManifoldServer`→`ColumnEngine`) and one metric below it (`fetch_count`).
4. **Multi-Manifold "lifecycle" exists on the authoring side and is thrown away at serving.** The server only scans folders.
5. **The identity layer (member store, J_m, dual bitmaps) is a Platform TARGET, not present** — today's cache/witness keys are implementation keys whose `member` is an aggregation operator, not entity identity.

## 2. End-to-end traces

### 2.1 Authoring → publish (manifold-agent + columna-studio)
Authored Manifold = logical-only `Declaration(kind,name,body,…)`; physical identity forbidden in `body` (`validate.py:130,241-244`, `PHYSICAL_IDENTITY`). Private realization = `Mapping/Binding` (`mapping.py:35-97`: member·connection·schema·table·column·grain·`root_evaluator`). Folder per manifold: `studio.json` (only Studio-authored) + `manifold.yaml` + `manifold.columna.yaml` + `mapping.yaml` + `audit.json` (`workspace.py:9-38`).
Path: author → `apply_to_folder` writes superset + re-lowers downgrade (`apply.py:87-89`); binding proposal writes `mapping.yaml` only (`apply.py:100`). Logical resolution `resolve_references` never consults mapping (`validate.py:299-306,352-386`). Ratification is the one human mint path `ratify_existence_law` → writes superset only (`apply.py:164-187`). Publish → `plan_publish` (diff→`bump_version`, `publishing.py:96-116,223-235`) → **governed lowering** `stamp_source_identity` runs P0(c) `assert_existence_law_complete` per universe (`apply.py:152-153`), stamps source id, re-serializes superset + downgrade (`apply.py:159-160`); refuses if id/version absent (`GovernedLoweringError`). Retention `Library.publish` → `library/<id>/<version>/` (`library.py:103-161`). **No physical realization at lowering** — `to_engine_dict` emits `{name,**body}` per declaration + source id; mapping never opened (`manifold.py:340-360`).

### 2.2 Serving (Frame-QL → result)
`ManifoldStore.__init__` `os.listdir`s the manifolds dir, `_load_one` per `<id>/manifold.cml`: `parse_file` (`store.py:35,77`) → `manifold.check()` → `_load_duckdb` `CREATE TABLE … read_parquet` → `ManifoldServer(manifold, DuckDBConnector(con))` → `adjudicate` fail-closed (`store.py:88-98`). Request: MCP tool `execute_frame_query` (`tools.py:168`) → `parse_statement` → `lm.server.planner.run_statement` (`planner.py:625`) → per-series `ColumnEngine.resolve` (`engine.py:85`) → connector `deliver_*` → **SQL runs only inside `DuckDBConnector` `.execute().arrow()`→`pl.from_arrow`** (`connector.py:155-189`); all cross-table transport/relate is post-fetch in the engine over Polars → `FrameResult` → `disclosure_wire.wire_frame` (`disclosure_wire.py:235-264`) → MCP/HTTP/agent. Wire `CONTRACT_VERSION="2"` (decoupled from pkg `0.15.0-core`).

## 3. Ownership map — SHARED / CORE / PLATFORM / UNRESOLVED

| component (file) | responsibility | owner | evidence | coupling/risk |
|---|---|---|---|---|
| `manifold_agent.manifold/validate/logical/ratification` | authored logical Manifold model, resolution, P0(c) ratification | **SHARED** | logical-only, physical-clean enforced (`validate.py:241-244`) | the one governed semantic source-of-truth; must not gain physical keys |
| `manifold_agent.mapping.Binding` | private realization (physical binding + `root_evaluator`) | **CORE** (private realization) + PLATFORM-seed | `mapping.py:35-97` | identity-bearing fields (`grain`,`root_evaluator`) are a Platform seed |
| `columna_studio.*` (workbench/apply/publishing/library/portfolio/workspace) | authoring, ratify, publish, multi-manifold lifecycle | **SHARED** (Studio belongs to Core+shared) | imports only manifold_agent | multi-manifold lifecycle lives here, unused by serving |
| `columna_core.model/parser` (`.cml`) | Core execution image grammar | **CORE** | `parser.py`, `model.py` | a Core execution artifact, not the universal ontology |
| `columna_core.adjudication` (Certificate kernel) | verdicts, licenses, scope, watermark | **SHARED** semantic law | `adjudication.py:578-657` | pure semantic authority; must have exactly one implementation |
| `columna_core.planner` | static adjudication (addressability, universe law, pin laws, Φ driver, typecheck) | **SHARED** semantic law | `planner.py` §-laws | decides meaning before execution |
| `columna_core.engine` (ColumnEngine) | runtime governance (crossing dispatch, confinement, series-reduce) **+** Polars mechanical compute | **split** — governance=SHARED, compute=CORE-substrate | `engine.py` (see §4) | do NOT assign whole module; classify inside |
| `columna_core.connector` (Connector Protocol + DuckDBConnector) | source execution (deliver columns, never combine) | **CORE** (source-execution) | `connector.py:17-33` | single impl today; Protocol additive |
| `columna_core.disclosure_wire` | governed wire contract | **SHARED** | duck-typed; imports no engine (`disclosure_wire.py:23`) | already the provider seam |
| `columna_core.sketch.WitnessStore` | published sketch materialization | **CORE** cache + PLATFORM-seed | `sketch.py:87-111` | drawn "so a durable backend drops in later" |
| `columna_server.store.ManifoldStore` | folder discovery, load, connect | **CORE** | `store.py:109-134` | registry-half + core-runtime constructor |
| `columna_server.tools` (14 MCP tools) | serving surface | **SHARED** on output (wire), **CORE**-coupled on input | `tools.py:181` `planner.run_statement` | no provider interface between tools and Core |
| `columna_server.agent.*` (MCP client) | query agent | **SHARED** | spawns server over stdio; imports no core (`mcp_client.py:5-6`) | the only already-clean consumer |
| `columna_core.draft.lower_to_cml` | init-interview → `.cml` | **CORE** (or UNRESOLVED) | `draft.py:106` | a *second* engine-side authoring path disjoint from Studio |
| **the mapping-consuming `.cml`/runtime lowerer** | authored+mapping → execution image | **UNRESOLVED** (missing) | does not exist | the F0 headline; owner is the split's key ruling |

## 4. Metric Engine responsibility decomposition (inside `engine`/`planner`/`adjudication`, not by module)

- **SEMANTIC/GOVERNANCE (the bulk):** `canonical_delta` (within-tolerance Δ≡0, `engine.py:31-59`); fan-out refusal (`engine.py:107-116`, `planner.py:162-203`); faced-crossing dispatch + anchor law (`engine.py:281-325`); ASSIGN/ALLOC/TOUCH disposition laws (`engine.py:338-553`); series-reduce = the metric's declared meaning, never mean-of-means (`engine.py:584-652`); universe confinement (`engine.py:730-805`); dependent-attribute partition (`engine.py:660-669`); holistic recompute-from-base (`engine.py:681-727`); one-universe law + addressability + blocked-transport + Φ driver + pin laws + typecheck (`planner.py:113-355,739-1093`); the whole Certificate kernel — math proof, data refutation, hierarchy FD, face licenses, basis testedness, published scope (`adjudication.py:119-657`).
- **IDENTITY/STATE (thin):** published serving scope on planner (`planner.py:110-111`); attestation watermark = table-version identity, NOT member identity (`adjudication.py:271-301`); source-manifold id (`model.py:292-293`).
- **SOURCE EXECUTION:** delegated to `Connector` (single-table group-by/distinct only; never joins) (`connector.py:17-33`).
- **INTERNAL COMPUTE SUBSTRATE:** Polars, operator-explicit (see §5).
- **CACHE/MATERIALIZATION:** exact-atom cache + `CacheEntry` (`engine.py:63-144`); `WitnessStore` (`sketch.py:87-111`).
- **TRANSPORT/WIRE:** disclosure builders + four-outcome surfacing (`engine.py:977-998`, `planner.py:66-86`).
- **PRESENTATION/TEST:** `EngineStats`, trace, `_fmt_anchor`.

## 5. Polars inventory — the compute-substrate seam evidence

Polars imported at 3 sites only: `engine.py:21`, `planner.py:15`, `adjudication.py:40` (`sketch.py` uses datasketches, not Polars). The code itself marks the boundary — directive-7: "Polars EXECUTES what the planner already adjudicated; a Polars default is never an accidental law" (`planner.py:549-555`, `engine.py:623,675-676`).

- **CONTAINER/INTERCHANGE (safe):** `CacheEntry.frame`, `ColumnResult.frame`/`FrameResult.data`, result assembly/rename/select (`engine.py:64,278,882`; `planner.py:1120`).
- **COMPUTE (swap-safe mechanics):** monoid group-by reduce, transport join+group_by, holistic median/mode, scan window ops, casts, map arithmetic, HAVING/LIMIT/sort (`engine.py:197-200,255,565-727`; `planner.py:536,587,1269-1275`).
- **SEMANTICS — analytical decision embedded (a naive Polars→DuckDB swap ERASES it); grouped by your risk axes:**
  - *participation/absence:* ASSIGN anti-join drops uncovered keys (`engine.py:364-366`); left-join-then-null for Φ, not self-fill (`engine.py:375-377,431-432,538-550`); `fill_null(0)` gated on Φ∈{zero,unknown} (`engine.py:543`); §2c full-outer juxtaposition creates the local absence domain (`planner.py:319`); null-detect + zero-fill (`planner.py:336-341`); universe confinement filter (`engine.py:755-759`).
  - *reducer/state:* ordered witness `sort_by("_order").last()/.first()` = state-at-time (`engine.py:569-573`); ALLOC partition-of-unity normalization (`engine.py:417`); TOUCH deliberate over-count with no dedup (`engine.py:526`); driver forced `Float64` precision (`engine.py:336`).
  - *ordering:* `nulls_last=True` B3 ruling (`planner.py:560-561`); LIMIT PER `group_by(maintain_order=True).head(n)` determinism (`planner.py:583`); deterministic summation order in reduce-path replay (`adjudication.py:195-198`).
  - *functionality/refusal/disclosure:* hierarchy FD verdict `n_unique>1` (`adjudication.py:333`); face proofs (tie-at-top / negative-or-zero driver → fail closed) (`adjudication.py:505-525`); verdict tolerance policy int/decimal exact vs float rtol (`adjudication.py:172-173`); reduce-vs-recompute counterexample (`adjudication.py:204-222`).

**Seam implication:** a substrate seam must lift these ~19 decisions ABOVE the substrate (planner-emitted explicit directives: join-type, null-ordering, maintain-order, fill policy, tolerance), so DuckDB executes ruled directives, not Polars defaults. That is C2 (separation) strictly before C3 (swap).

## 6. Multi-Manifold — "loads folders" vs "real lifecycle"

- **Serving = implementation capability only.** `ManifoldStore` = one-shot `os.listdir`→dict, keyed by directory name; **no version field anywhere**, no resolve-by-version, no reload/unload/refresh, DuckDB connection held for process life (`store.py:109-134,50`). manifold_id = folder name (`store.py:117-120`).
- **Authoring = a real lifecycle, but siloed.** Studio has draft/published state (`workbench.py:1027-1033`), semantic versioning (`publishing.py:96-116`), retained versions `library/<id>/<version>/index.json` (`library.py:115-156`), a `Portfolio` Manage view with cross-manifold overlap detection (`portfolio.py:109-177`), a `registry`→`ManifoldEntry` list (`workspace.py:153-160`), SQLite session state (`session.py:97-107`).
- **The gap:** the lifecycle (identity, version, draft/published, retention) is authored richly on the Studio side and **entirely discarded at the serving boundary** — the server re-derives identity from a folder name and has no version at all. Making multi-Manifold a first-class shared capability = promoting Studio's lifecycle vocabulary into a shared registry both sides honor.

## 7. Runtime-artifact reclassification (authored / private / execution image)

Three distinct `Manifold` types, correctly kept apart: `manifold_agent.manifold.Manifold` (authored, logical), `columna_studio.models.Manifold` (read-only view), `columna_core.model.Manifold` (execution image). Places the **execution image is treated as the authored ontology**:
1. `store.py:60-80` — `manifold.cml` is the server's canonical source of truth; hand/demo-authored, no `source_manifold_id` required, no ratification check.
2. `parser.py:14,160-181` — a source-identity-less `.cml` is fully legitimate (`None` defaults); an engine image with no authored source runs.
3. `draft.lower_to_cml` (`draft.py:106-112`) — a second authoring surface *inside the engine package*, disjoint from the authored Manifold.
4. `demo.py`/`init/loop.py:115-117` — `.cml` shipped/generated as the primary artifact with no upstream authored Manifold.
5. **Naming conflation:** docstrings call `manifold.columna.yaml` "the downgrade the engine loads" (`manifold.py:10`, `apply.py:158`) — **false on main**; the engine loads `manifold.cml`.

## 8. Platform-seed inventory (evidentiary discipline)

- **IDENTITY ALREADY PRESENT (semantic role today):** sufficient-state monoid combination (witness+combine; ordered witness last/first = retained state-at-time, `engine.py:564-573`, `operators.py:47-106`); coverage/absence decisions (Φ, shadow/coverage, columna#149, `engine.py:364-550`); grain-lattice **coordinate** navigation (`find_path` `model.py:302-319`). All keyed by **grain buckets / coordinates**, not member identity.
- **PLATFORM SEED (plausibly the future identity runtime):** eligibility as a confinement predicate (`engine.py:745-762`); observed support (`validate_universe_support` `engine.py:925-975`); attestation identity (`adjudication.py:271-301`); source-manifold identity (`model.py:292-293`); `WitnessStore` drawn for a future durable backend (`sketch.py:87-111`); `Binding.grain`/`root_evaluator`.
- **PLATFORM TARGET (absent today):** canonical member identity **J_m** — the cache key `(measure,member,target,uni,where)` (`engine.py:127`) and witness key `(measure,member,base_level)` (`sketch.py:97`) are **implementation keys**, and `member` is a *family aggregation operator* (`engine.py:91`), not entity identity; dual bitmaps as a governed structure (concepts exist as predicate + counts, no bitmap object); a member-identity runtime navigating the lattice (navigation is over coordinates, not members). **Verdict on your caution #4: current cache/state objects are keyed implementation artifacts, not semantic identity.**

## 9. DuckDB's three roles (kept distinct)

- **SOURCE backend — the only role in code today:** connector target over the user's parquet warehouse (`connector.py:83`, `store.py:47-88`); logical→physical type bridge `TRY_CAST` (`connector.py:128-141`); manifold-agent gates profile the warehouse via DuckDB.
- **Internal compute substrate — NOT DuckDB today (it is Polars):** all intermediate transport/relate/reduce is Polars in-engine; DuckDB does only the bounded single-table read (`connector.py:155-189`). Future direction only.
- **Platform/enclave host — absent:** no enclave/kernel abstraction exists.

## 10. Three proposed seams

### S1 — execution-provider seam (needed before Core-P1 AND Platform-P1)
- **Belongs:** between `columna_server.tools` and the concrete `ManifoldServer`. The **output** contract already exists and is clean — `disclosure_wire.wire_frame/wire_column` duck-types `FrameResult`/`ColumnResult`, imports no engine (`disclosure_wire.py:23,192-264`). Formalize the **input** side: an interface exposing `list/describe/status/query/explain` whose natural anchor is `LoadedManifold` (`.manifold` introspection + `.server` execution) (`store.py:38-45`).
- **Removes coupling:** `tools.py` reaching into `lm.server.planner.run_statement` (`tools.py:181`); `store.py` constructing `ManifoldServer`/`ColumnEngine`/`DuckDBConnector` (`store.py:34,88`).
- **Must not cross/hide:** the four moods, per-field status, canonical query, anchor — all already in the wire. **One leak to fix:** `fetch_count`→`fetches_delta` assumes a connector counter through `engine.con.fetch_count` (`frameql.py:103`, `tools.py:175`); generalize to a provider-supplied metric.
- **Risk:** low; first impl adapts today's Core with no semantic change.

### S2 — Manifold lifecycle/registry seam (shared; needed for multi-Manifold)
- **Belongs:** a shared registry contract both Studio and server honor: identity + **version** + draft/published + resolve/active + provenance. Studio already has the vocabulary (`workspace.registry`, `library` versions, `portfolio`); the server has only `ManifoldStore.get/_load_one`.
- **Removes coupling:** serving identity from a bare folder name; the total absence of a serving-side version.
- **Must not hide:** ratification/published-scope/source-identity provenance.
- **Risk:** medium — requires a serving-side version notion that does not exist today.

### S3 — compute-substrate seam (Core-only; justified, but AFTER C2)
- **Belongs:** below the Metric Engine's mechanical compute, above Polars. **Justified** by §5 (Polars localized to 3 modules) — but the ~19 SEMANTICS sites mean the seam is only safe once those decisions are lifted into explicit planner directives.
- **Removes coupling:** direct Polars-default reliance for join-type/null-order/maintain-order/fill/tolerance.
- **Must not erase:** any of the §5 SEMANTICS decisions.
- **Risk:** high if attempted before C2; do not build a generic dataframe abstraction now.

## 11. Unresolved decisions + stop-conditions

**UNRESOLVED (need rulings):**
1. **Who owns the missing Core lowerer** (authored+mapping → execution image), and **what is the execution image** — is it still `.cml`, or a private runtime object? (The old P1 `columna_core.lower(...)` is now only *one* candidate.)
2. **Is `.cml` the shared↔Core interface, or Core-internal?** The docs lean Core-internal; the code currently makes `.cml` the *only* thing the engine reads.
3. **Reconcile the two engine-side authoring paths** — `draft.lower_to_cml` (init) vs the Studio authored Manifold. Two "authored ontologies" exist.
4. **Serving-side Manifold version** — none exists; S2 must introduce one.

**Stop-conditions triggered (bringing back, not resolving):**
- **`.cml` carries law with no authored logical source — CONFIRMED.** `store.py:60-80` + `parser.py:14` accept an ungoverned `.cml`; `assert_existence_law_complete` runs only in Studio's authoring lowering (`apply.py:152-153`), never on the artifact the engine reads. Existence-law governance does not reach the runtime today.
- **Blast-wall refactor risk:** the ratification fingerprint is logical-only (`ratification.py:90-161`). Any lowerer that folds mapping/physical facts into the authored `body` trips `PHYSICAL_IDENTITY` and silently stales every ratification. The P0(c) gate is load-bearing on exactly one call site; a Core-side lowerer must re-assert it or governed universes lower ungoverned.
- **Substrate stop-condition:** §5's ~19 sites are Polars ops that *are* rulings; a substrate abstraction built before C2 would erase them.

## 12. Recommended PR sequence (do not implement yet)

**F0 → S1 → S2**
- **F0 (this):** report + rulings on §11.
- **S1.1** define `ExecutionProvider` interface at the `LoadedManifold` boundary; adapt today's Core behind it (no semantic change); route `tools.py` through it. **S1.2** move `fetches_delta` onto the provider (kill the `fetch_count` leak). Gate: existing Core tests + e2e pass byte-identical through the seam.
- **S2.1** shared `ManifoldRef` (identity+version+state) + registry contract; server resolves by it; Studio publishes into it. **S2.2** serving-side version from the published `source_manifold_version`. Gate: one multi-Manifold e2e without per-manifold process assumptions.

**Entry points after the seams:**
- **Core-P1 (C1)** begins at the **missing lowerer** — a Core-owned compiler `(authored Manifold + mapping) → Core execution image`, re-asserting `assert_existence_law_complete`, consuming `mapping.yaml` (whose `root_evaluator`/grain are ready), emitting whatever the S1 provider serves. My prior P1 mapping/capability trace is the input; its `columna_core.lower(...)` shape is now *a candidate*, not the ruling.
- **Metric-Engine substrate separation (C2)** begins at §5: lift the ~19 SEMANTICS decisions into explicit planner directives; then C3 (DuckDB substrate via parity).
- **Platform-P1** begins at the **certificate-survival spike** — can the `disclosure_wire` per-field status + canonical identity ride a Substrait/Arrow crossing? Independent of Core; do not fork `ColumnEngine`.

## 13. The ten completion questions, answered

1. **One shared semantic spine today?** The authored Manifold model (manifold-agent) + the planner's static adjudication + the adjudication Certificate kernel + the disclosure/wire contract. Meaning is defined and adjudicated there.
2. **Where does Core-specific physical execution begin?** At the `Connector` Protocol call (`connector.py:17-33`); SQL runs only inside `DuckDBConnector`. Everything above is logical/Polars.
3. **Where are physical assumptions leaking upward?** `store.py` (`.cml`+duckdb+parquet construction), `ManifoldServer`→concrete `ColumnEngine` (`frameql.py:13-14`), and `fetch_count`→`fetches_delta` on the wire (`frameql.py:103`, `tools.py:175`). `describe` is clean (insulation test).
4. **What does ColumnEngine actually own?** Runtime governance of crossings/absence/series-reduction/confinement (SHARED law) **co-located with** Polars mechanical compute (substrate) — a split module, not one owner.
5. **Which of those are law/identity vs mechanical compute?** Law: §4 SEMANTIC/GOVERNANCE + the ~19 §5 SEMANTICS sites. Mechanical: the COMPUTE/CONTAINER Polars sites. Identity/state: thin (scope, watermark, source id) — no member identity.
6. **How real is multi-Manifold today?** Serving: folder-scan only, no version/lifecycle. Authoring: a real lifecycle (version/draft/published/library/portfolio) that serving discards.
7. **What must become shared to make it first-class?** A registry contract (identity+version+state+resolve) both sides honor — promote Studio's lifecycle vocabulary; give serving a version (S2).
8. **Smallest seams that let Core continue without dictating Platform?** S1 execution-provider (already 90% present in the wire) and S2 registry; both adapt today's Core with no semantic change and make no Platform commitment.
9. **Genuine Platform seeds vs superficially similar?** Genuine seeds: sufficient-state monoid, coverage/absence, eligibility/support, attestation identity, WitnessStore. Superficial (NOT identity): cache/witness keys (`member` = aggregation op), grain buckets. J_m / dual bitmaps / member runtime are targets.
10. **First safe PRs after F0?** S1.1/S1.2 (provider seam + fetch-count fix), then S2.1/S2.2 (registry + serving version). All behavior-preserving, all `SHARED`/`CORE`, no Platform, no substrate abstraction.

## Spine answer — where meaning is decided, and how far down execution can move

Analytical meaning is decided in the **shared semantic core**: the authored Manifold's logical laws, the planner's static adjudication, the engine's runtime governance, and the Certificate kernel — and, dangerously co-located, inside ~19 Polars expressions.

**Mechanical execution may move downward whenever the lower layer can faithfully execute an already-adjudicated operation without acquiring decision authority.** The `Connector`'s no-join discipline is strong evidence of the current separation, and it lets Core add/multiply source backends — but moving *more* computation source-side still requires preserving operator, state, absence, ordering, and certificate semantics, so it is not unconditional. Execution **cannot** move into a swapped internal substrate until each of the ~19 embedded decisions is made explicit as a ruled directive *above* the substrate (LAW → DIRECTIVE → SUBSTRATE); until then the substrate would acquire (or silently duplicate) decision authority. And the identity/composition authority the vision wants downward **does not exist yet** to move: it must be *authored into being* (the missing Core compiler; a real member-identity layer), not extracted from today's implementation keys.

**One-line:** the split is not a disentangling problem — it is a *contract-definition* problem across domains that are already separated, with one contract entirely missing (the Core compiler) and one decision-locus (the ~19 Polars sites) that must be hoisted before any substrate moves.
