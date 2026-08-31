# Columna — Consolidated Architecture and Implementation Ledger

**Version:** 0.1
**Date:** 29 August 2026
**Repository state:** `mission/topology-authority-repair`, from `9121a42`
**Controlling record:** `docs/architecture/topology_core_platform_delivery_v0_1.md`
**Status:** the governing inventory. Later work is authorized *from* this ledger.

---

## 0. What this is

One ranked inventory consolidating six read-only audits and one deterministic runtime
reproduction. It replaces the six separate debt ledgers. Rows carry stable IDs so later
work can cite them.

**No GitHub issue is opened per row.** This document is the inventory; issues are cut from
it when work is authorized.

### Evidence grades

Every row carries one. This distinction is load-bearing: several claims that survived three
rounds of source reading were **falsified** by execution.

| grade | meaning |
|---|---|
| **VX** | VERIFIED EXECUTION — reproduced under the real runtime (duckdb 1.5.5, polars 1.44.1) |
| **SV** | SOURCE-VERIFIED — read at the cited file:line, not executed |
| **INF** | INFERENCE — a conclusion drawn from source, not observed |

### Priority classes

| class | meaning |
|---|---|
| **P0** | False, stale, or contradictory current user-facing claims |
| **P1** | Current correctness, fail-closed, disclosure, or non-interference defects |
| **P2** | Authority-carrier and ontology contradictions between publication, mapping, image, admission, and served result |
| **P3** | Studio / authoring artifact-and-authority boundary debt |
| **P4** | Execution-placement and backend-portability debt |
| **P5** | Long-horizon Platform, durable material-state, and native-custody work |

### Falsified claims — do not carry forward

Three claims from earlier reporting did not survive execution:

| retired claim | what is actually true | grade |
|---|---|---|
| "A warm cache hit drops disclosures" (general) | **TOUCH path only.** The normal path and the scan path are disclosure-symmetric; warm only *adds* `freshness` | VX |
| "9 un-ledgered laws" / "18 un-ledgered laws" | **26**, in four placement classes | SV |
| "support shortfall is mis-graded" (general) | **Bridge-coverage shortfall only.** The ALLOC *reconciliation* shortfall is correctly MATERIAL (`disclosure_wire.py:146-148`) | VX |

---

## 1. The four findings that outrank everything else

**Two of these serve a wrong number.** That is a different category from the disclosure and
authority debt below, and it is why P1 leads this ledger rather than P0.

| id | finding | grade |
|---|---|---|
| **P1-01** | Witness/sketch construction reads **outside** the declared universe carve, and the disclosure claims the confined population anyway | VX |
| **P1-02** | `data_identity() -> None` is **fail-OPEN** on the witness store — stale sketch reused across a real mutation, zero fetches, no disclosure | VX |
| **P2-01** | "REFUSAL BEFORE OMISSION" is enforced only over five declaration **kinds** — governed law inside a declaration **body**, and whole unknown kinds, are silently dropped while the receipt attests the binding | VX |
| **P2-02** | The lowering receipt binds publication↔image but **not** publication↔mapping — four different meanings of one governed `root_member` under one publication digest, four valid receipts | VX |

---

## P1 — Correctness, fail-closed, disclosure, non-interference

### P1-01 · Universe confinement violated on the witness/sketch path · **CRITICAL** · VX

`_build_base_sketches` (`packages/columna-core/src/columna_core/engine.py:1000-1010`) calls
`deliver_base_rows(meas.home_table, [base_phys], meas.distinct_col, where)` and returns. It
never calls `_confine`, never augments the grain with `_predicate_levels`, and the `where`
it forwards is the *query* WHERE, not the universe predicate. Compare
`_deliver_and_transport_monoid` (`engine.py:314-336`), which does both.

Reproduced: universe `sales = store * day WHERE day >= store.opened`. Confined truth for
`s1` is **1** distinct buyer; the engine serves **3**. The monoid path on the identical
universe confines correctly (`5->3 base points`, revenue `70.0` not `100.0`).

**Aggravating:** the served disclosure asserts `[over sales]` — it *claims* the confined
population while delivering the unconfined one. The only caveat is the routine ±1.6 % HLL
note. Nothing discloses the breach.

**Both the eager published witness and the lazy fallback build are wrong identically** —
one shared defect, not a materialization bug.

Violates topology record §9 and standing rule *"Materialized state must be confined to the
governed universe."*

### P1-02 · `data_identity() -> None` is fail-OPEN on the witness store · **CRITICAL** · VX

`Witness.version` stores `None` (`engine.py:1030`); `WitnessStore.fresh` (`sketch.py:105`)
evaluates `w.version == version` as `None == None -> True`.

Reproduced: a real data mutation (a brand-new distinct customer) is invisible. The answer
stays **2** against a ground truth of **3**, at **zero backend fetches**, with no staleness
disclosure.

**The rule is written down twice and implemented once.** `connector.py:37-68` — *"`None` is
not a failure to serve; it is a failure to REUSE."* `engine.py:154-166` — *"`None` … means
DO NOT REUSE and DO NOT STORE."*

**The asymmetry is the defect's signature.** Same primitive, opposite polarities:

```
result cache  under data_identity()->None:  size 0, hits 0   <- fail-CLOSED, correct
witness store under data_identity()->None:  reused, version=None, fresh()=True  <- fail-OPEN
```

Violates standing rule *"Unknown data identity must fail closed."*

### P1-03 · Witness currency is blind to every dependency but the home table · **HIGH** · VX

`engine.py:967` and `engine.py:1025` both compute `ver = self.data_version(meas.home_table)`.
The result cache on the same request uses `data_version_of(computation_tables(...))`
(`engine.py:124-140`), which includes predicate providers, edge providers, and the M:N bridge.

Reproduced: the predicate table moved; `revenue` correctly re-derived `70.0 -> 100.0`; the
witness stayed `fresh() = True`.

**Coupling constraint — P1-01 and P1-03 must land in one change.** This is latent *only
because* P1-01 exists: the witness never reads the predicate, so its content genuinely
depends on the home table alone. The two defects cancel into a single wrong answer. Fixing
P1-01 without widening the witness key converts P1-03 from latent to active staleness. (INF
on the latency; VX on both underlying behaviours.)

Violates standing rule *"Materialized-state currency must use the complete computation
dependency set."*

### P1-04 · Warm TOUCH hit drops disclosures the cold path emits · **HIGH** · VX

The touch cache check returns `self._touch_disc(...)` + `FRESHNESS` at `engine.py:589`,
**before** the coverage caveat (`:610-619`) and the Φ-fill caveats (`:633-645`) are computed.
`CacheEntry` holds only `frame / sketches / version` (`engine.py:62-66`), so they have
nowhere to be stored.

Dropped cold -> warm:

| dropped caveat | engine category | wire code | materiality |
|---|---|---|---|
| bridge coverage (shortfall **and** full-coverage forms) | `transport` | `provenance` | immaterial |
| crossed-grain absence, `FILL zero` | `declared_fill` | `filled` | immaterial |
| crossed-grain absence, `FILL unknown` | `unknown_absence` | `unknown` | **MATERIAL** |

**Two qualifications that bound the severity, both executed:**

1. **The outcome never degrades.** `over_count` (-> `multi_counted`, MATERIAL) is rebuilt on
   the warm branch, pinning the touch path to `disclose` either way.
2. **The MATERIAL caveat has a planner-side twin that survives** (`planner.py:524-546`), so a
   consumer sees a *different* material disclosure set rather than none — which makes the
   drift harder to notice, not easier.

**The irrecoverable loss is the coverage-shortfall record.** Warm, nothing anywhere states
that the touch total falls short of the grand total. Values identical; honesty gone.

Violates standing rule *"Warm execution must never become quieter than fresh execution."*

**Scope correction:** the normal path (**P1-04a**, VX) and the scan path (**P1-04b**, VX) are
**disclosure-symmetric**. `resolve` returns a freshly recomputed `self._disc(...)` on both
branches (`engine.py:221` warm / `:236` cold); the scan's TRANSPORT caveat is minted
post-cache at `engine.py:288`. Any repair must not assume a general defect.

### P1-05 · Bridge-coverage shortfall is graded IMMATERIAL and cannot trip `disclose` · **HIGH** · VX

`engine.py:611` is commented `# COVERAGE (the second disclosure of the ratified absence law)`
and then constructs `Caveat(TRANSPORT, ...)`. The mis-classification is visible in the
source's own comment.

`TRANSPORT -> provenance -> IMMATERIAL` (`disclosure_wire.py:108`). Counterfactual
re-derivation with only the shortfall caveat yields **`outcome = serve`**.

The correct MATERIAL slot exists and is wired — `COVERAGE = "coverage"` (`disclosure.py:33`)
-> `("denominator_population", MATERIAL)` (`disclosure_wire.py:104`) — and **has no producer
anywhere** (`grep -rn "Caveat(COVERAGE"` -> no hits; `engine.py` does not import `COVERAGE`).
Retired at `planner.py:549-551`.

**Scope correction:** the **ALLOC reconciliation shortfall is correctly MATERIAL**
(`disclosure_wire.py:146-148` upgrades on `status == "shortfall"`). Do not generalise.

In practice the outcome does not currently degrade, because `over_count` (touch) and `shadow`
(assign) are unconditionally MATERIAL co-caveats. The defect is the **materiality
classification**, not a presently mis-mooded frame.

Violates standing rule *"A support shortfall that is material to the request must not be
downgraded to an immaterial provenance note."*

### P1-06 · Cached frame served under narrowed admission · **HIGH** · VX

Reproduced with no data change: narrowing admission to a scope that does **not** admit
lineage `hA` still serves `hA`'s cached frame — `{A:30, B:40}` where the newly-admitted route
computes `{X:10, Y:60}`. The only disclosure is `freshness: served from cache`.

Cache key `(measure, member, target, universe, where)` + data-version token carries **no
admission/scope identity** (`engine.py:216-218`). `Planner.install_scope`
(`planner.py:156-172`) is documented as *the* single installation boundary and carries no
cache-invalidation obligation.

Which shipped entry points clear the cache (VX):

```
adjudicate()            -> cache size: 1     (does not clear)
publish()               -> cache size: 1     (does not clear)
reattest()              -> cache size: 0     (explicit clear, correct — frameql.py:56)
_install_closed_scope() -> cache size: 1     (safe only by accident)
```

`_install_closed_scope` is rescued solely because the empty scope sets
`attested_identities = {}`, driving `data_version -> None` and closing reuse. Where the
narrowed scope makes a request outright inadmissible, the planner refuses **before** the
engine cache is consulted — those legs are correctly fail-closed.

### P1-07 · ASSIGN face serves `null` for a cell its own caveat says was filled · **MEDIUM** · VX

The planner's Φ-fill writes into `FrameResult.data`, but `wire_column` serialises
`ColumnResult.frame`, which was never filled.

```
ASSIGN fr.data (assembled)                 = [... {'category.primary':'c3','revenue': 0.0}]
ASSIGN per-column frame served on the wire = [... {'category.primary':'c3','revenue': None}]
   alongside code=filled "1 absent cell(s) filled with 0 per the declared fill rule"
```

Found incidentally during §6 reproduction; outside the eight briefed scenarios.

### P1-08 · Result cache is unbounded with no eviction · **MEDIUM** · SV

`engine.py:80` (`self.cache: dict = {}`); no eviction anywhere. `ManifoldStore._loaded`
(`store.py:262-267`) parses once at startup, so the engine cache lives for the **process
lifetime across MCP requests**, accumulating every distinct
`(measure, member, anchor, universe, where)` frame.

### P1-09 · TOUCH key uses `fam.agg` where the plain path uses `member` · **MEDIUM** · SV

`engine.py:583` vs `engine.py:216`. Two key vocabularies in one dict; a member/agg divergence
would alias.

---

## P2 — Authority-carrier and ontology contradictions

### P2-01 · "Refusal before omission" is kind-granular only · **CRITICAL** · VX

The doctrine, stated by the compiler itself (`compiler/compile.py:16-19`):

> *"REFUSAL BEFORE OMISSION. An out-of-scope construct in the publication is a refusal with a
> named category, never an image that quietly lacks it. A silently-dropping compiler would
> make the receipt bind a publication to an image that does not carry its meaning — which is
> the exact failure the binding was introduced to prevent."*

Enforcement is a fixed allow-list of five declaration **kinds** (`compile.py:92-110`, looped
at `:174-177`). There is **no body-field check and no unknown-kind check**. The publication
reader accepts any `{kind, name, body}` and stores the body verbatim
(`compiler/inputs.py:119-128`).

Reproduced — all five compile clean and mint a valid receipt:

```
fill_rule=unknown on measure (Phi, MATERIAL)   COMPILED  (silently dropped)
root_member=does_not_exist (dangling ref)      COMPILED  (silently dropped)
default_reduction=median                       COMPILED  (silently dropped)
member.blocked={calendar} (B-anchor law)       COMPILED  (silently dropped)
unknown declaration kind 'invariant'           COMPILED  (silently dropped)
```

**The asymmetry is backwards.** The *mapping* reader refuses unknown realization kinds with
an explicit rationale (`inputs.py:268-272`: *"an unrecognised realization is realization the
compiler cannot carry"*). The *publication* reader — the governed side — does not.

`root_member=does_not_exist` compiling is independently notable: a governed declaration may
name a root member that does not exist and the compiler mints a receipt for it.

### P2-02 · The receipt binds publication↔image but not publication↔mapping · **CRITICAL** · VX

`LoweringBinding` is exactly three fields — `(publication_ref, publication_digest,
image_digest)` (`lowering_receipt.py:117-127`). `mapping_provenance` is excluded by explicit
ruling (`lowering_receipt.py:45-48`, `receipt.py:48-51`), verification never opens the
mapping (`lowering_receipt.py:30-33, 250-276`), and the shipped receipt carries
`{"mapping_format_version": "1"}` — **not even a digest**
(`governed/firstlight/lowering-receipt.json:8-10`).

Reproduced — one publication, four mappings differing only in `root_evaluator`:

```
root_evaluator=sum    pubdigest=e0a2ff4325c750b6  image: ... FAMILY { sum }
root_evaluator=count  pubdigest=e0a2ff4325c750b6  image: ... FAMILY { count }
root_evaluator=min    pubdigest=e0a2ff4325c750b6  image: ... FAMILY { min }
root_evaluator=max    pubdigest=e0a2ff4325c750b6  image: ... FAMILY { max }
```

Four meanings, one governed digest, four valid self-consistent receipts. **The member whose
meaning flips is `revenue_sum` — the measure's declared `root_member`.** A green test
institutionalises the shape (`tests/test_k0_compiler.py:264-272`, and again at `:283`).

### P2-03 · `root_evaluator` is identity-bearing Data World information placed below the governance line · **CRITICAL** · SV

Per the ruling: under ToD v6.1 a measure family `F` has one full coherent family law
`Law(F)`; `Law(F)` is a constituent of the identity signature `Σ(F)`; a measure is `F@A` and
inherits its family identity and law. `root_evaluator` selects the operator/family law that
determines what an old-style governed member means. It is therefore identity-bearing.

Current placement is wrong in four separate ways (`compiler/inputs.py:176`, required at
`:260-264`; `fixtures/firstlight/private-core-mapping.json`):

- **too weak in type** — a bare operator name is not the full family law. ToD v6.1 §5.1: two
  operations both called `SUM` need not instantiate the same family law if participation,
  multiplicity, support, regime or approximation differ;
- **wrongly placed** — beside the physical endpoint in the private mapping;
- **outside the receipt binding** (P2-02);
- **absent from the shipped runtime unit** and discarded after compilation.

The compiler's own docstring names the boundary it is protecting (`inputs.py:168-169`):
*"`root_evaluator` is captured, never invented: a compiler that chose a reducer would be
manufacturing analytical law."* It refuses to manufacture the law; it has nowhere governed to
write down the law it was handed.

**Retired formulation — do not carry forward:** *"root evaluator != family/default reducer."*
The governing fact belongs to the measure family.

### P2-04 · The execution grammar is v5-ontology; the publication is v6-ontology · **CRITICAL** · SV

ToD v6 retires `member` from the core ontology: what v5 called a member of a measure is now
a **measure** (`F@A`); what v5 called a measure is now a **measure family**.

`MEASURE revenue FAMILY { sum count min max }` must **not** be read as one v6 family with
four members. It is a v5-style execution container grouping what v6 may treat as **distinct
governed families** — differing reducer laws establish differing family identities (ToD v6.1
§5.6: `revenue@B ==γ_MAX=> max_revenue_B@B` is an identity event even where displayed values
coincide).

The two artifacts key the same family differently:

| artifact | family is keyed by | contains |
|---|---|---|
| `governed-publication.json` | member **name** | `revenue_sum`, `revenue_count`, `revenue_min`, `revenue_max`; no reducers |
| `manifold.cml` | **operator** | `FAMILY { count max min sum }`; no member names |

Neither governed artifact carries the association. Core's word *family* and ToD's word
*family* are near-inverses — Core's is a set of reducers over one column; ToD's is one law.

### P2-05 · Twenty-six Data World laws live only in Core-private artifacts · **CRITICAL** · SV

Not 9, not 18. Four placement classes:

**A · private mapping only (1):** `root_evaluator`.

**B · declared in the publication, lost or unvalidated in lowering (6):** `root_member`
(never validated — dangling refs compile); `fill_rule` (Φ — **MATERIAL** absence law,
silently dropped); `default_reduction`; `anchor.components[].type`; any unrecognised kind;
`universe.restriction` (refuses — fails closed, correctly).

**C · `.cml`-only, no governed home and no lowering path (13):** `BLOCKED {lineage}` (the
B-anchor law — the flagship demo's entire refuse leg, declared structurally unrepresentable
at `compile.py:104-107`); `M_ANCHOR` (MCAR/MAR/MNAR); `FILL` as realized; `ORDER <level>`;
`pre_expr`; `distinct_col` + `sketch_precision`; descriptions reaching the wire; `HIERARCHY`;
`RELATE … FACES`; `FunctionalEdge.lineage` + evidence; `License` / `basis_license`; `DERIVED`;
`UNIVERSE … WHERE` as realized.

**D · `columna_core` source only (6):** `count ≡ count(*)` (rows, not observations —
so `revenue_count` counts rows and SQL null-exclusion is silently reversed); `min/max/sum`
NULL-skip semantics; `decimal -> Float64` (self-labelled "the one lossy edge",
`compile.py:69-85`); `K0_REDUCERS`; alloc reconciliation tolerance `1e-9`;
`APPROX_MATERIALITY_THRESHOLD = 0.01` and the category->materiality map.

**Consequence:** the governed publication is not a sufficient statement of the world. The
`.cml` is the real source of truth.

### P2-06 · Governed serving answers the declared world from the execution image · **CRITICAL** · SV

`GovernedPublication.logical` is parsed, validated, stored and blast-wall-tested, then read
by **no serving tool** — zero non-test readers repo-wide. Every `describe` / `discovery` /
`status` / `evidence` answer is reconstructed from the `.cml` via `lm.manifold`
(`tools.py:189, 248, 378, 397, 423`). The declared world reaches the requester only as a
version string.

### P2-07 · No canonical governed identity for a measure exists · **HIGH** · SV

`ManifoldRef` (id + concrete semver) is the only placement-stable governed identity and it
names a *publication*, never a *quantity*. `F@A` appears only in prose and comments. The
engine cache key and `WitnessStore` key are the right granularity but are process-local
implementation keys carrying **no publication id and no manifold id** (`engine.py:216-218`,
`sketch.py:96-106`) — isolation between publications is by object instance only.

`ADR-032:87` already requires the opposite: *"The shared cache must key by
Manifold-id-plus-version so a witness from one world is never served into another."*
Unimplemented.

### P2-08 · Result standing is not on the governed return · **HIGH** · SV

`certified_edges`, `certified_faces`, `edge_evidence`, `face_evidence`,
`attested_identities` never cross the wire. Standing is a property of an *installation*,
never of a *result*; on a served frame it appears only negatively, as `uncertified_edge` /
`uncertified_face` refusal reasons. A `serve` frame carries no positive standing at all.

### P2-09 · Typed absence cannot survive lowering · **CRITICAL** · SV

Φ_v is the best-built of the six governance terms in Core — parser, model, four-branch
dispatch, crossed-grain application, four closed wire codes at correct materiality, tested
end to end. And the governed publication has no slot for it, and the compiler has no code
path that reads it (grep of `compiler/` for `fill|absence` returns only `basis`). See P2-01:
it does not even refuse.

### P2-10 · `mapping_provenance` carries no mapping identity · **HIGH** · SV

`governed/firstlight/lowering-receipt.json:8-10`; `receipt.py:64-65`. The one field that could
have named the mapping revision carries a format token. Post-mortem on a meaning drift has no
artifact to consult.

### P2-11 · `data.toml` — the placement decision — is written into the runtime unit but never digested · **HIGH** · SV

`provision.py:59, 189-190, 245`. *"connector choice and warehouse location are operator
decisions, not derivable facts."* The one file that decides **where the computation actually
happens** is outside the only proof the runtime checks. Additionally, `[manifold] name` /
`description` — user-facing identity reaching `list_manifolds` — are read from this
backend-config layer (`store.py:139-143, 243-244`).

### P2-12 · The `.cml` co-locates law and physical plumbing · **CRITICAL** · SV

`demo/cascadia/manifold.cml:19-67` (physical) vs `:11-13, 40-46, 62-66` (law). No artifact
exists at the governance line that carries the full law.

**Sub-defect (MEDIUM):** that file's own header at `:5-6` claims *"Purely logical: the tables
and columns live in the physical→logical map … never here"* — false in the same file at
`:13, 19, 20, 21, 24, 25, 26, 33, 35, 36, 40, 49-56, 59, 60, 62, 67`.

### P2-13 · Adjudicated `License` / `PublishedScope` re-minted at every startup, carried by nothing · **HIGH** · SV

`store.py:170-175`; served at `tools.py:231-240, 421-448`. Absent from publication *and*
receipt.

### P2-14 · Six governance terms — carrier status · **HIGH** · SV

| term | verdict |
|---|---|
| support | PARTIAL — computable, private, mis-graded on the wire (P1-05). `validate_universe_support` has **zero non-demo callers** (`engine.py:1039-1089`) |
| typed absence | PRESENT in Core; ABSENT above the governed boundary (P2-09) |
| freshness | PARTIAL — strong internally, invisible externally, **timeless by design**: no TTL, as-of, watermark or expiry anywhere. One IMMATERIAL `freshness` string, produced only for cache hits |
| provenance | PRESENT for origin; PARTIAL for authority — the `elf-1` ratification fingerprint is **carried, never verified** (`registry.py:250-251`) |
| standing | PRESENT as installation authority; ABSENT as result standing (P2-08) |
| reconciliation | ABSENT in the §4 sense. The word is taken by ALLOC numeric commutation; `crosswalk` is a compile refusal (`compile.py:107-109`) |

### P2-15 · `describe.absence_semantics` teaches a law the engine no longer implements · **MEDIUM** · SV

`describe.py:57-69` still teaches basis-driven absence (`"events" -> "absence is a lawful
ZERO"`), which `model.py:51-53` retired as *"a silent wrong zero for state-valued measures"*
and `tests/test_basis_absence.py:116` pins as inert. It reaches the wire via
`tools.py:196-202`.

---

## P0 — False, stale, or contradictory current user-facing claims

Ranked by exposure × falsity. Full per-line inventory with proposed replacements is in the
current-voice repair; this ledger records the claims and their standing.

### P0-01 · `/docs/frameql` announces a two-tier product in the present tense · **CRITICAL** · **FIXED** in Unit C · SV

`docs/frame_ql_manual_v2.md:62`, rendered live by `apps/website/src/pages/docs/frameql.astro:5`:

> *"Columna ships in two tiers, and this one manual covers both. Constructs available only in
> **Frame-QL Pro** are tagged inline **[Pro]**."*

There is one tier. There is no Pro. All 13 `[Pro]` construct tags in the manual inherit their
falsity from this sentence, which explicitly tells the reader the tags denote purchasable
availability. Retired by topology record §17.5.

### P0-02 · `/docs/reference` carries a "Pro extensions" chapter and a `Pro connectors` matrix · **CRITICAL** · **FIXED** in Unit C · SV

`docs/columna_reference_manual_5e.md:653-657, 1573-1575, 1588-1589`. Includes named,
enumerated capabilities with concrete rule identifiers (`equal_split`, `weighted`,
`proportional_to`) in a matrix whose other rows are true.

### P0-03 · Two live manuals contradict each other about which backends exist · **CRITICAL** · **FIXED** in Unit C · SV

`columna_reference_manual_5e.md:1575` presents a **`Polars (Core)`** column with fifteen rows
of capability entries. `columna_framework_manual_6g.md:640` says *"Core ships **one backend:
DuckDB** [SHIPPED] … A Polars backend [ROADMAP — no connector ships today]"*.
`connector.py:117` defines exactly one concrete connector. `PolarsConnector` exists in six
documents and **zero lines of code**.

### P0-04 · `[Pro]` was emitted on the live wire · **CRITICAL** · **FIXED** in `f62c47a` · VX

Four runtime-reachable strings: `planner.py:361` (the flagship fan-out clarify — the most
exercised governed refusal in the system), `engine.py:256`, `engine.py:259`,
`operators.py:172`. The only false tier claims a user could hit without reading a document.
Each reclassified individually to `[ROADMAP]`; `operators.py:172` additionally dropped "Core
registry" (the registry is shared, not a tier seam). Pinned assertion at
`tests/test_disclosure_wire.py:95` moved in lockstep. Suite green.

### P0-05 · "Columna Core is the shipped open-source engine" · **CRITICAL** · **FIXED** in Unit C · SV

`docs/columna_framework_manual_6g.md:625`, live. The most structurally dangerous P0 because
it is *almost* right: it collapses the architecture/package distinction (record §17.1) and
thereby silently converts everything §3 assigns to the Core architecture — Studio, governed
authoring, multi-Manifold lifecycle — into a claim about what a reader just installed. It
survives inside a chapter otherwise carefully repaired on 2026-08-27.

### P0-06 · A monitoring product described as operating today · **HIGH** · **FIXED** in Unit C · SV

`columna_reference_manual_5e.md:881`: *"In Core, drift is detected and recorded. In Pro, the
operational monitoring infrastructure — alerts, dashboards, escalation — consumes the events."*
Nothing consumes those events. Compounded at `:857`, which folds the nonexistent product into
a sentence about what the framework can determine. Legitimate residue:
**DELIVERY-OPERATIONS**, unbuilt.

### P0-07 · Three nonexistent commercial products in one paragraph · **HIGH** · **FIXED** in Unit C · SV

`docs/columna_framework_manual_6f.md:637` and `6e:633`: *"Pro includes a cloud-hosted service
… as a managed subscription … self-hosted license, cloud subscription, and professional
services give Pro three delivery models."* Not routed by the site, but **neither carries a
standing banner** and `docs/README.md:13` invites a reader to open them. 6g was repaired for
exactly this; 6e/6f were left behind.

### P0-08 · The package-copy repair was reverted and is orphaned · **HIGH** · VX

`7595dda` (2026-08-27) repaired the package copy; `f643711`, **8 minutes later**, reverted
those four files because the build gate correctly refused:

> `STALE PAYLOAD: columna-core==0.16.2 is already on PyPI, and this tree would build a
> DIFFERENT package under that same version`

The repair was parked on `lab/package-copy-repair` — which **points at `7595dda` itself and is
an ancestor of HEAD**, so it carries nothing forward. The repaired bytes are recoverable only
by cherry-picking hunks out of a superseded commit. The block is a version-bump decision that
has not been made. Feeds deliverable F.

### P0-09 · PyPI front page for `columna-core` carries three tier statements · **HIGH** · SV

`packages/columna-core/README.md:45, 90, 94`. `:90` — *"Deliberately out (Pro): …"* — reads as
*withheld from a shipping product*, precisely the "Core is a weakened precursor" framing
record §3 forbids. Blocked behind the same version gate as P0-08.

### P0-10 · README documents a `FAMILY { <agg> [: <tier>] }` clause the parser rejects · **MEDIUM** · SV

`packages/columna-core/README.md:82`; same phantom clause at `parser.py:28`. The regex at
`parser.py:475` has no `: tier` alternative — an author following the documented grammar gets
a bare `ParseError`.

### P0-11 · Package front doors omit the honest typing the website carries · **MEDIUM** · **PARTLY FIXED** in Unit C — the packaged half is RELEASE-GATED · SV

`README.md:11-59` — the ten-minute quickstart is the Cascadia demo end to end, closing *"That
transcript is the product."* No mention of `firstlight`, of `ENTRY_LEGACY`, or of
consume-not-produce. `packages/columna-server/README.md` never names `firstlight` **even
though that package ships it**.

**No document asserts Cascadia is governed.** The site is exemplary here
(`GovernedStanding.astro:5-9`, and `gen_firstlight.py` fails the build closed). The risk is a
reader inferring it from the absence of any contrary signal at the default entry point.

### P0-12 · `/docs/reference` page chrome names two superseded editions · **MEDIUM** · **FIXED** in Unit C · SV

`apps/website/src/pages/docs/reference.astro:15` — *"the framework manual (**6e**) and the
FrameQL manual (**v1**)"*. Current: 6g and v2.

### P0-13 · Stale versions · **MEDIUM/LOW** · **PARTLY FIXED** in Unit C — the `README.md:1` half is RELEASE-GATED · SV

`packages/columna-core/README.md:1` — `# Columna Core (0.7.8-core)` vs actual `0.16.2`, nine
minor versions stale, in the H1 PyPI renders. `docs/README.md:15` says the FrameQL manual is
synced to `columna-core 0.14.0 / wire "2"`; the manual's own currency block says `0.16.2 /
wire "3"` — the index contradicts the manual it indexes.

### P0-14 · `/ask` retrieval index serves the false claims to the site agent · **HIGH** · **FIXED** in Unit C · SV

`services/ask/index/chunks.json` — 27 `Pro` hits across 1400 chunks, built from the three
manuals. **Do not hand-edit.** Fix the source manuals, then rebuild via
`services/ask/ask/index_build.py`.

### P0-15 · `core_p1_compiler_input.md` still reads as unbuilt · **MEDIUM** · **FIXED** in Unit C · SV

`:3` — *"Status: design checkpoint / pre-implementation (no compiler code yet)"* — while
`columna_core/compiler/` has shipped since 2026-08-22. The authoritative placement matrix
reads as speculative; an auditor may discount it.


### P0-17 · The reference manual's operator matrix marks fifteen operators available that do not resolve · **HIGH** · **FIXED** in Unit C · VX

Found while repairing P0-03, in the same table. Appendix A's capability matrix presented every
operator class as `native` on a named backend column. Resolving each through the shipped lookup:

```
shipped registry (columna-core 0.18.0), by execution: 26 operators
  * + - / count cummax cummin cumsum distinct first hll_count hll_estimate hll_merge
  lag last lead max mean median min mode neg pct_change rolling_mean rolling_sum sum

get_operator(...) raises KeyError for all fifteen of:
  AVG  COUNT_DISTINCT  APPROX_DISTINCT  APPROX_QUANTILE  APPROX_FREQUENCY  PRODUCT
  BOOL_OR  BOOL_AND  WEIGHTED_MEAN  VARIANCE  STDDEV  VALUE_AT_MAX  VALUE_AT_MIN
  NTH  rank  ewm_mean
```

No alias rescues them — `get_operator("avg")` and `get_operator("count_distinct")` both raise, so
the near-misses (`mean`, `distinct`) are not reachable under the documented spelling either.

**The manual has a partial defence and it is worth stating**, because it shapes the repair: the
matrix is introduced as *"the framework's logical catalog — the union of what the supported stacks
can serve — not a mandate that every backend computes every operator natively."* As a catalog it is
legitimate. What made it false was the column headers — `Polars (Core)` / `DuckDB (Core)` — which
made a framework claim read as a package claim, next to a `Core` label a reader has just been told
means what they installed.

**Repaired by separating the two claims rather than deleting either.** The matrix keeps its catalog
rows and gains a `Registered (0.18.0)` column stating what `get_operator` resolves; an operator
marked `—` is *catalog, not capability*, and the legend says naming it in a declaration raises rather
than returning a number.

Not in the original inventory — the six audits found the tier claim in this table and stopped there.

### P0-16 · `CLAUDE.md` is stale relative to HEAD · **LOW** · **FIXED** in Unit C · SV

Its "current task" is launch-checklist steps 3-8; it predates the K0 compiler, the lowering
receipt, the provisioner and the firstlight fixture. `store.py:1-3` still calls itself the
"WP-2.1 stub".

---

## P3 — Studio / authoring artifact-and-authority boundary

### P3-01 · The in-repo authoring surface authors the execution image · **CRITICAL** · SV

`InitLoop.publish()` -> `Draft.lower_to_cml()` emits `.cml` text; each LLM `Proposal.body`
**is** a `.cml` grammar fragment (`init/loop.py:113-117`, `draft.py:49-51, 106-113`). Record
§15 — *"Studio authors the declared world. It does not author the execution image"* — is
inverted by the shipped `columna init` on-ramp.

Its output emits no `SOURCE_MANIFOLD`, so it classifies `ENTRY_LEGACY` — permanently outside
governance. **The repo's authoring path terminates in an ungoverned image; the governed path
terminates in an artifact the repo cannot produce. The two do not meet.** The codebase knows:
the compiler is explicitly forbidden from reading `lower_to_cml` output (`compile.py:7-9`).

### P3-02 · The governed publication producer is out of tree · **HIGH** · SV

Nothing in this repository can mint or validate a governed publication. author / ratify /
publish are reachable only through two private checkouts behind a HEAD pin
(`fixtures/firstlight/build.py:61-70, 82-88`); `core_p1_compiler_input.md:7` traces the
producer to `manifold-agent @ d9ea705`.

**§19 stop-gate not cleared:** `datumwise/columna-studio` and `datumwise/manifold-agent` both
404 under the available token. Current remote heads could not be obtained or verified.
**Neither repository was touched.** The existing audit remains typed as mid-August evidence
whose currency cannot be established.

### P3-03 · OF-28 is the open stop-gate · recorded, not debt · SV

`specs/open_forks.md:53`, status OPEN: *"no public governed-publication authoring surface
opens while the implementation vocabulary decision remains unresolved."* This is a ratified
reason, not drift. Consequence: record §7/§11's *"Studio … included in complete Core"* is
**aspirational, not implemented** — correctly so.

### P3-04 · `docs/architecture/f0_reconnaissance.md` documents out-of-tree internals as in scope · **LOW** · SV

`:104, 115` describe `manifold_agent` / `columna-studio` files not in this repository.
Historical evidence; must be reverified before operational reliance.

---

## P4 — Execution-placement and backend-portability

### P4-01 · Every seam is placement-agnostic in shape and welded in fact · **HIGH** · SV

`Connector` and `ExecutionProvider` are real Protocols with a parity-suite hook
(`test_connector_protocol.py:24-28`) and honest docstrings anticipating a second backend. But
`columna_core/__init__.py:11` imports `DuckDBConnector` at package import, `duckdb` is a hard
dependency, `store.py:149-152` refuses any other connector type, and all transport is
`polars.DataFrame`. Even the parity factory is DuckDB-shaped.

### P4-02 · `ExecutionProvider`'s currency is two undeclared Core types · **HIGH** · SV

`run(statement) -> Any` where `statement` is a `columna_core.envelope` parse tree produced
server-side (`tools.py:300`), and the return is duck-typed by `wire_frame`, which reads
`cr.frame` — a `polars.DataFrame` (`disclosure_wire.py:202-213`). The seam concedes the leak
(`provider.py:19-21`): `operators()` / `published_scope()` are **PROVISIONAL**, the logical
description is deliberately excluded, and `ManifoldServer` is imported at module scope — so
importing the *interface* imports Core.

### P4-03 · Six of eleven governed serving tools cannot be served by a non-Core provider · **HIGH** · SV

Direct consequence of P4-02's *"Logical description stays OFF the provider"*
(`provider.py:16-18`).

### P4-04 · No ADBC decision record exists; Arrow is only the DuckDB→Polars hop · **MEDIUM** · SV

Exhaustive grep: six `adbc` hits, all prose, none a decision record. `pyarrow` is pinned but
used only as polars' Arrow bridge. No Arrow-native ingress, no Substrait, no cross-process
Arrow surface. **Conforms** to record §13.

### P4-05 · Three governed kinds have publication slots but no mapping structure · **HIGH** · SV

`relationship` / `hierarchy` / `attribute` — `build_mapping` skips them and join keys are
stranded in `evidence.subject` (`core_p1_compiler_input.md:66, 68, 70`); all three refuse at
`compile.py:93-103`. Using evidence as a realization substitute is forbidden at
`core_p1_compiler_input.md:194-196`.

### P4-06 · Shared provisioner hard-codes the Core execution image · **MEDIUM** · SV

`RUNTIME_FILES` includes `manifold.cml` (`provision.py:59`) and `_SOURCE_MANIFOLD`
re-implements the `.cml` grammar as a regex (`:62-65`). A Platform realization with no `.cml`
cannot be provisioned or admitted by the shared path.

### P4-07 · Governed compile/provision has no CLI; the governed fixture ships unreachable · **HIGH** · SV

`cli.py:118-150` exposes only `mcp`, `demo`, `agent`. `compile_k0` and
`provision_runtime_unit` are library-only, reachable in-repo solely from
`fixtures/firstlight/build.py` and tests. `demo_store()` points at `demo/`, not `governed/`.

### P4-08 · Vendored Frame-QL parser + precomputed wire in the public Vercel endpoint · **MEDIUM** · SV

`apps/demo-endpoint-vercel/index.py:8-22, 37`. Honest about being a replay ("never a
facsimile"), but a second, drifting copy of a shared surface.

### P4-09 · `APERTURE_SAMPLE_CAP = 1000` — a governance policy constant in connector source · **LOW** · SV

`connector.py:79`, self-described *"a GOVERNED aperture"*. A governance limit set below the
governance line and not declarable.

---

## P5 — Long-horizon Platform, durable material state, native custody

**No implementation is authorized.** These are recorded so later work has a referent.

| id | item | grade |
|---|---|---|
| **P5-01** | No MME exists. The only hit for `MME` in the tree is the topology record's own list of claims it does not make (`:493`) | SV |
| **P5-02** | Sufficient state is absent as a governed object. Three partial seeds — `WitnessStore` HLL sketches, connector monoid witness columns, `CacheEntry` — none carries a composable measure state alongside its support and absence typing | SV |
| **P5-03** | No carrier proof can cross an execution boundary without law loss. The closest existing combination is `{publication, receipt, wire_frame}`, which still loses typed absence, support (a *name*), standing, and data-state identity | SV |
| **P5-04** | A cached object is not distinguishable from a sole-holder observation. Result cache adds only `Caveat(FRESHNESS, "served from cache")`; **witness reuse adds no marker at all** | VX |
| **P5-05** | Cache and witness keys cannot be keyed by canonical governed identity — the record's own question at `:535` answers *no* as built | SV |
| **P5-06** | The portability proof is not "two engines returned the same number." Required experiment recorded at record §22: a genuinely non-SQL second connector, full governed wire semantics compared, including decimal, timestamp/time-zone, null/absence, ordered reducers, sketches, and holistic reducers or explicit refusal | — |

---

## Unit B — CLOSED, 2026-08-31

Every row Unit B was authorized to repair is fixed, shipped and installable. Rows are struck here
rather than deleted: the evidence of what was wrong is the reason the standing tests exist.

| row | defect | shipped in | standing test |
|---|---|---|---|
| **P1-01** | witness/sketch read outside the declared universe carve — served 3 where the carve admits 1, while claiming `[over sales]` | 0.17.0 | `test_witness_non_interference.py` |
| **P1-02** | `data_identity() -> None` was fail-OPEN on the witness store — 2 served against a truth of 3, at zero fetches | 0.17.0 | same |
| **P1-03** | witness currency was home-table only; a predicate-provider change left it "fresh" | 0.17.0 | same |
| **P1-04** | warm TOUCH was quieter than cold, dropping a MATERIAL caveat | 0.18.0 | `test_disclosure_channels.py` |
| **P1-05** | coverage shortfall graded IMMATERIAL on a code whose MATERIAL slot had no producer — **both** faces | 0.18.0 | same |
| **OF-24** | a mechanical fact wore a semantic name on the semantic channel | 0.18.0 | same |
| **P0-04** | `[Pro]` reachable on the wire — four runtime strings | 0.17.0 | pinned in `test_disclosure_wire.py` |
| **P0-08/09/10/13** | the orphaned package-copy repair, unblocked by the version decision | 0.17.0 | — |

**Two of these served a confident wrong number** (P1-01, P1-02). The rest are honesty defects: the
system knew something true and did not say it, or said it on the wrong channel.

### What Unit B changed about the architecture, not just the code

The wire now separates **semantic authority** from **mechanical observation**. `disclosures` says
what is true of the answer and is call-invariant; `mechanical` says what happened on this call and
may vary freely. That is the same boundary the Architecture work names — a channel that is allowed
to differ cannot be the one a caller reads to learn what a number means — arriving in the wire
contract rather than only in prose.

### Not closed by Unit B, and deliberately so

**P1-06** (a cached frame served under narrowed admission), **P1-07** (the ASSIGN face serving
`null` for a cell its own caveat says was filled), **P1-08** (unbounded cache) and **P1-09** (two key
vocabularies in one dict) remain open. None is a wrong-number defect; P1-06 is the sharpest and is
gated behind `Planner.install_scope` acquiring a cache-invalidation obligation, which is design work
rather than repair.

---

## Unit C — CLOSED, 2026-08-31

The P0 class: false, stale or contradictory **current user-facing claims**. Authorized directly from
topology record §17.4 (the replacement vocabulary — ROADMAP / DELIVERY-OPERATIONS / RETIRED) and
§17.5 (which retired `[Pro]` as an edition marker outright). **No fork was ruled and none was
needed** — every claim below was already false by a ruling that had landed; only the sentences had
not moved.

| row | claim | where it was | struck by |
|---|---|---|---|
| **P0-01** | *"Columna ships in two tiers"* + 11 `[Pro]` construct tags | `/docs/frameql`, live | §Editions and availability, each construct re-typed |
| **P0-02** | a "Pro extensions" registry chapter + a `Pro connectors` matrix column | `/docs/reference`, live | §8.3 rewritten as the registry extension point; column struck |
| **P0-03** | a `Polars (Core)` column with 15 capability rows, contradicting 6g | `/docs/reference`, live | column struck — `PolarsConnector` is six documents and zero code |
| **P0-05** | *"Columna Core is the shipped open-source engine"* | `/docs/framework`, live | package/architecture distinction stated where the chapter starts |
| **P0-06** | a monitoring product described as operating today | `/docs/reference`, live | typed **[DELIVERY-OPERATIONS — unbuilt]**; "nothing consumes those events" said plainly |
| **P0-07** | three nonexistent commercial products in one paragraph | 6e/6f, unbannered | standing banner naming exactly what is false below it |
| **P0-11** | front doors omit the typing the website carries | repo README **merged**; both *package* READMEs **release-gated** | Cascadia typed `ENTRY_LEGACY`; firstlight named; consume-not-produce stated |
| **P0-12** | page chrome naming editions 6e and v1 | `reference.astro` | 6g, v2 |
| **P0-13** | an index contradicting the manual it indexes | `docs/README.md` **merged**; core README H1 **release-gated** | the index stopped restating the version; H1 0.17.0 → 0.18.0 |
| **P0-14** | the `/ask` index served the false claims to the site agent | `services/ask/index/` | rebuilt from the repaired site build |
| **P0-15** | a shipped compiler whose boundary record read *"no compiler code yet"* | `core_p1_compiler_input.md` | restamped IMPLEMENTED |
| **P0-16** | `CLAUDE.md` current-task predates the compiler, receipt, provisioner | `CLAUDE.md` | current task replaced |
| **P0-17** | 15 operators marked available that `get_operator` does not resolve | `/docs/reference`, live | **found by this repair**; a `Registered (0.18.0)` column separates catalog from capability |

### Two things the repair found that the six audits had not

**The tier marker was hiding shipped capability, not only inventing unshipped capability.** Every
`[Pro]` construct was re-typed against what the package *executes* rather than against the ledger's
description of it. Two came back **shipped**: MNAR exclusion and coverage. Verified by execution — an
`M_ANCHOR { self }` measure serves with `unconfirmed_assumption: '...' is MNAR (missingness depends
on its own value) — averages are selection-biased`, and a touch face with a real shortfall serves
with a `coverage` caveat. So the sentence *"constructs available only in Frame-QL Pro"* was
**withholding, in prose, capability the open package already serves**. A false claim about a product
boundary does not fail in only one direction.

**An enumerated blocklist finds what someone already found.** The check was first written from this
ledger's own inventory and passed on 25 of 32 loci. Widening the last pattern to the bare token
surfaced seven more the six audits had missed: two `(Pro)` parentheticals on capability lines, a
`ROADMAP — Pro/enterprise` tag, and four ADR provenance comments. P0-17 came out of the same pass.
This is the argument for the check being a *check* rather than a longer errand list.

### What makes this class not recur

`docs/tools/check_no_tier_claims.py`, wired into `docs.yml`. Prose was the one surface with no
compiler: the ruling landed 2026-08-27 and the claims were still live on 2026-08-31, because nothing
in CI reads a sentence. Two rules — no current document carries a live tier claim; every preserved
prior-edition record says on its face that it is preserved. Genuinely historical prose is exempted by
an explicit `<!-- tier-history -->` marker, so *"we kept this deliberately"* is greppable and never
confused with *"nobody noticed."*

The path filter was widened at the same time. It read `docs/**` only — the same masking shape Huayin
fixed in this workflow on 2026-07-25 — which would have let a tier claim reappear in a package README
without ever running the job.


### The release gate, and why the packaged half is not in this merge

A package README is the wheel's `long_description`, so editing one changes `*.dist-info/METADATA`.
The build gate refused, correctly:

```
✗ STALE PAYLOAD: columna-core==0.18.0 is already on PyPI, and this tree would build a
  DIFFERENT package under that same version. Differences — changed: *.dist-info/METADATA
✗ STALE PAYLOAD: columna-server==0.11.0 …
```

**This is the same gate that orphaned P0-08 for four days**, and P0-08's row records the failure mode
precisely: the repair was reverted eight minutes later and parked on a branch that is an *ancestor of
HEAD*, so it carried nothing forward and was recoverable only by cherry-picking hunks out of a
superseded commit. The lesson is not *don't defer* — it is *don't defer onto a dead branch*.

**Why the bump is not simply taken here.** `scripts/release_pins.py` binds umbrella and core in
lockstep, and `docs/RELEASE_ORDER.md` (ratified 2026-07-27) fixes the order as **publish, verify the
pin resolves, THEN merge**. So a version bump merged to `main` ahead of a published release does not
merely sit inert — the shipped-coherent deploy wedge pins the exact versions this commit claims and
**fails closed** when they are not on PyPI. Bumping to clear a CI gate would trade a stale README for
a broken production deploy, and would manufacture a release decision inside a documentation repair.

**Where the packaged half lives:** branch `unit-c/package-front-doors`, as an open PR against `main`
carrying the two README edits alone — a live PR, not a parked commit. It is expected to be red on the
stale-payload gate, and that redness is the row: it goes green the moment a release bumps the
versions, and it should ride the next release rather than mint one. The decision it is waiting on is
**a version decision, and it is Huayin's** — the same decision P0-08 waited on, made once in Unit B
when 0.17.0 shipped.

### Not closed by Unit C, and deliberately so

**P2-01 / P2-02 / P2-03 / P2-09 remain open, and are the top of the queue.** They are the two of the
original top-four that Unit B did not reach, and they are a **design fork, not a repair**: Appendix A
records that a generic refusal-before-omission rule *"will refuse publications that compile today,"*
and P2-03 moves `root_evaluator` across the governance line. Neither is mine to rule. P2-02's
sharpest form is worth stating for whoever takes it: the four-mappings-one-digest reproduction is not
really a receipt defect — the binding does distinguish the four images — it is the publication
**under-determining its own meaning** (P2-05), which the receipt was deliberately built not to
compensate for. Fixing P2-03 substantially dissolves P2-02; adding a mapping digest to the binding
would not.

**Q1 of Appendix C is untouched.** Deposited essays rendering retired closure claims on `/thesis`
and `/why` is the one place where *retire from current voice* collides with *do not edit deposited
bytes*. This unit did not edit a single deposited byte, and did not resolve the collision.

---

## Appendix A — Coupling constraints

Rows that **must** be repaired together, or a fix creates a new defect:

| rows | why |
|---|---|
| **P1-01 + P1-03** | P1-03 is latent only because P1-01 exists. Fixing confinement without widening the witness currency key converts latent under-invalidation into active staleness |
| **P1-04 + P1-05** | Both concern what the TOUCH path discloses. Re-grading coverage to MATERIAL while the warm path still drops it means the warm/cold divergence becomes outcome-visible (`disclose` cold, `serve` warm) — a strictly worse failure than today's |
| **P2-01 + P2-03 + P2-09** | Φ and `root_evaluator` are both *silently dropped* rather than refused. A generic refusal-before-omission rule (P2-01) makes both fail closed immediately, which is correct but will refuse publications that compile today |
| **P0-08 + P0-09 + P0-10 + P0-13** | All four are blocked behind one version-bump decision. They must ship as one release or not at all |

## Appendix C — Absorbed from the positioning audit (PR #237, closed as superseded)

`specs/positioning_consistency_audit_v0_1.md` (27 August) found the Pro-tier exposure this ledger
now carries with fuller evidence — its headline findings are P0-07, P0-03 and P0-13. The audit is
closed rather than merged, so that there is one inventory and not two. Two things it carried are
NOT findings and would otherwise have been lost with it.

### C.1 · Four questions the ruling does not settle

Recorded as open. None is a defect; each is a decision nobody has made.

**Q1 · Frozen corpus rendered in current editorial voice.** `/thesis` and `/why` render deposited
essays verbatim, and those contain the closest things on the site to a retired closure claim —
*"Columna is our proof that the discipline can be made executable"*, *"The semantic layer was only
ever half the answer. The other half now exists."* The bytes are frozen and must not be edited, yet
they render on live routes with no edition pin and no disclosure. **This is the only place where
"retire from current voice" collides with "do not edit deposited bytes."** Correct as a rendering,
misleading as a current statement.

**Q2 · `/ladder` exists to be competitor-relative.** A ratified page whose stated purpose is *"how is
this different from X?"*, with `/why` and `/the-argument` both pointing at it — while the positioning
brief forbids competitor-relative claims for Columna. Either `/ladder` is the sanctioned exception (a
measuring stick that grades us too, which is how it is written), or it is now out of doctrine. It
cannot be left in the middle.

**Q3 · "Governed analytical service" already belongs to Analytical Governance.** The ruled Columna
description — *"infrastructure for governed analytical service"* — appears nowhere in the repo, and
its key phrase is currently AG's subject: the deposited record reads *"Analytical Governance is the
discipline governing the legitimacy of the analytical service"*, and the AG page types Columna as
*"an executable consequence of"* that category, explicitly not its definition. Adopting the ruled
sentence is coherent — infrastructure *for* a service the category defines — but it puts Columna and
AG in one noun phrase for the first time. Worth ruling deliberately rather than discovering later.

**Q4 · A deposited public claim is in tension with the manual.** `open_planner_deposit_v1_3.md:45`
(DOI'd, frozen) states *"There is no SQL anywhere in the system"*; `columna_framework_manual_6g.md:132`
states *"Columna's only contact with the physical layer is SQL used narrowly to extract column-wise
data and metadata"*, and `DuckDBConnector` ships. Both are defensible under different readings of
"in the system", and both are public.

### C.2 · A method note worth keeping

The audit recorded a finding that was wrong before it was checked, and said the correction mattered
more than the finding. Two sweeps were scoped to disjoint trees; the one that could not see
`apps/website/src/**` concluded that `Data · Evidence · Intelligence` was the shipped wording,
because inside `specs/` the change existed only as an unimplemented proposal. Production had served
`Data · Certainty · Intelligence` since 2026-08-27.

> **A spec that says "PROPOSED, not implemented" outlives its own execution unless someone closes it.**

`specs/foundations_mission1_recon_v0_1.md` and `specs/foundations_mission1_implementation_plan_v0_1.md`
both still read as pending work that has in fact shipped. That is the same defect class as P0-15 and
P0-16 — a record correct as history, misleading as a current statement — and it is the reason every
row in this ledger carries an evidence grade rather than a citation alone.

---

## Appendix B — What is genuinely sound

Recorded because a ledger of defects misrepresents the system without it.

- **The `firstlight` governed test is unusually honest evidence**: byte-reproducible
  recompile, receipt digests binding shipped bytes, `ENTRY_GOVERNED` with zero load
  conditions, tamper→refuse leaving no half-unit, in-place edit on a running host losing
  standing, and **no shipped code knows the fixture's name** — proven by filesystem walk.
- **Positive-admission discipline is real.** A `SOURCE_MANIFOLD` claim without a receipt is an
  origin claim, not evidence. Missing authority is left `None` rather than fabricated.
- **The planner/engine seam is the healthiest boundary in the repo** — one routing authority,
  no fallback path-finding, and `PlannerView` makes "the planner cannot see provenance"
  structural rather than conventional.
- **The NL agent is fully Core-free** — no `columna_core` import anywhere under `agent/`.
- **The website is exemplary on governed standing** and fails its own build closed if the
  invariants stop holding.
- **`reattest()` clears the cache correctly**, and inadmissible requests refuse *before* the
  engine cache is consulted.
- **The demo is self-verifying and fail-closed** — a leg whose actual outcome differs from its
  declared mood exits 1, a guard added after a real 0.15.0 incident.
