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

**Amended 2026-08-31.** This table is left as ratified, but two of its four rows have moved and a
reader should know before using it:

- **P2-02 is not the row it looks like.** The binding *does* distinguish the four images. What the
  reproduction shows is the publication **under-determining its own meaning**, which the receipt was
  deliberately built not to compensate for. It is expected to **dissolve** under P2-03's repair
  rather than be fixed on its own terms.
- **P2-03 now outranks it,** and is the real fourth finding. Merged with the former P2-04 and
  re-graded **VX**: the reducer law is attached to the measure rather than the family — a ToD v5
  ontology fossil, not a field in the wrong file. It is the subject of **Unit D**, and **P1-10** is
  it arriving as a served number.

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

### P1-10 · A family member whose support disagrees with its siblings serves a silent mixed-denominator ratio · **HIGH** · VX

Found 2026-08-31 while testing the P2-03 ontology argument by execution. **It is the v5 family
container producing a number**, which is why it is filed in P1 rather than left inside a P2
ontology row: P1 is where a served figure is at stake.

`count` is registered with `deliver_sql=lambda p: "count(*)"` (`operators.py:84`). So inside one
declared family, `sum` skips nulls and `count` does not — the two members have **different
supports**, and nothing says so.

Reproduced — five rows, one carrying no revenue observation:

```
warehouse           rows = 5 | non-null amount = 4 | sum(amount) = 100.0

MEASURE revenue ON sales FROM sales_lines TYPE Float64 VALUE amount
    FAMILY { sum count min max }

revenue.sum    ->  100.0     (4 observations)
revenue.count  ->    5       (5 rows — count(*), including the row with no revenue)

DERIVED avg_line = revenue.sum / revenue.count
    outcome: serve      value: 20.0      caveats: []
```

Mean per *revenue observation* is 25.0. **20.0 is not flatly wrong** — read as a per-line average it
is defensible — and that is precisely the defect: **which one it is depends on a law nobody
declared.** There is no `Law(F)`, so there is no fact of the matter about the denominator, and the
wire is silent either way.

**Why nothing catches it.** Three guards are adjacent and all miss:

- The **co-anchor guard** (a ratio is determinate only when numerator and denominator resolve over
  one shared population) **passes** — both members resolve over `sales`. The divergence is in
  *support within* the universe, which the guard does not see.
- `Engine.validate_universe_support` (`engine.py:1104`) computes exactly this shortfall. It has
  **zero callers repo-wide** — P2-14 recorded "zero non-demo callers"; it is now zero, full stop.
- `describe` **asserts the grouping** rather than qualifying it (`columna_server/tools.py:276`):
  `"family": {"root": "revenue", "members": [...], "reducer_kind": {...}}`, plus per-member
  `blocked_lineages` / `order_by` / `is_monoid`. Nothing about support. A requester is told `count`
  is a member of the revenue family rooted at revenue, which is the reading that makes the ratio look
  safe.

**Not a new mechanism — a new consequence.** P2-05 class D already recorded `count ≡ count(*)`
(*"rows, not observations — so `revenue_count` counts rows and SQL null-exclusion is silently
reversed"*), but filed it as a law living only in Core source. It had not been connected to a served
figure.

**Coupled to P2-03**, and should not be repaired independently. A local fix — re-typing `count`, or
minting a support caveat on mixed-support ratios — treats the symptom while leaving the container
that groups a row-cardinality with three value reducers under one name. The support caveat is
nonetheless the cheap partial mitigation if Unit D runs long, and `validate_universe_support` already
computes it.

---

### P1-11 · Cross-measure silent population substitution — the served column asserts a population it did not serve · **HIGH** · **FIXED** in Mission A · VX

Found 2026-08-31 in the Column Algebra Mission 1 reconciliation
(`specs/column_algebra_reconciliation_m1_v0_1.md`). **Sibling of P1-10, not the same row**: P1-10 is
support divergence *within* one family (`count(*)` vs null-skipping `sum`); this is support
divergence *across measures*. Same collapse site, two independent causes.

**The defect is not the dropped rows. It is the claim left behind.**

```
universe 'ops' basis spine = 3 stores
revenue   support {s1,s2,s3}      headcount support {s1,s2}

SELECT rev_per_head AT {store}          -- DERIVED revenue / headcount
  frame outcome     : serve
  column population : ops               <-- the assertion
  coordinates served: ['s1','s2']       <-- 2 of 3
  disclosures       : []
```

The same two measures served side by side return 3 rows **and** an `unknown_absence` caveat. Combined
by an operator they return 2 rows and nothing. The disclosure is not merely omitted — the column
positively asserts `population: ops` while serving the intersection.

**Root cause, one line.** `Planner._apply` (`planner.py:1790-1792`):

```python
if lk == "col" and rk == "col":
    j = lp.join(rp, on=keys, how="inner", suffix="_r")
```

An undeclared complete-case (listwise) participation policy, chosen by the substrate. Φ then runs
frame-side at `planner.py:524-547` — *after* the inner join has discarded the very null it would have
typed — so `n_absent == 0`, the pass `continue`s, and the absence disappears.

**The loss is specific to support.** A DERIVED over an HLL measure keeps its `approximation` caveat:
`Disclosure.combine` (`disclosure.py:177-187`) is sound. Provenance disclosures propagate; support
and absence do not, because they are frame-side facts rather than operand-level ones.

**Doctrine contradicted:**

| # | doctrine | locus | how it breaks |
|---|---|---|---|
| 1 | **§2c FRAME LAW** — *"each column keeping its own population semantics"* | `planner.py:504-513` (`how="full"`) | the expression path does the opposite, 1,280 lines later in the same file |
| 2 | **P1-01's aggravating rule** — a disclosure that *claims* one population while delivering another | this ledger, P1-01 | identical shape, reversed direction: claims `ops`, delivers the intersection |
| 3 | **Unit B's ratified wire boundary** — `disclosures` is semantic authority, call-invariant, *what is true of the answer* | contract 4, `disclosure_wire.py:25-44` | `population` is a semantic claim, and it is false |
| 4 | **"disclosed, never silent"** (addendum §5) | `disclosure_wire.py:166` | zero disclosures on a material population change |
| 5 | **the four moods sort by lawfulness** — *disclose* = lawful, a material condition travels | Manual ch. 7 | a material condition exists and does not travel |
| 6 | **ADR-036 determinacy** — served *"with a disclosure if that number is risky"* | Manual `:1210` | risky, undisclosed |
| 7 | **f0 ruling 10** — `LAW -> EXECUTION DIRECTIVE -> SUBSTRATE` | `f0_reconnaissance.md:150`; `:147` already names *"participation/absence"* among ~19 embedded decisions | an un-lifted substrate default |

**Classification.** Not a wrong-number defect in the P1-01/P1-02 sense — the arithmetic over the
surviving coordinates is correct. It is a **silent population substitution**, and it is worse-behaved
than a plain omission in one respect: the wire makes a positive assertion that is false.

**Repair discipline (ruled, Huayin 2026-08-31).** *"Do not cure population substitution merely by
disclosing after an inner join has already discarded an analytical point. Preserve the governed
alignment facts/domain first; only then apply the map's declared/currently established
eligibility-support semantics."* The defect is that substrate alignment chooses participation before
Φ/support law can see the discarded point; the repair must remove that authority from the substrate.


#### Repaired — Mission A, 2026-08-31

**The alignment domain is now declared rather than inherited from the substrate.** `_apply` joins
`how="full"` (`planner.py`), which is the §2c FRAME LAW applied one level down — one alignment law,
not two, and the `LAW -> EXECUTION DIRECTIVE -> SUBSTRATE` shape f0 ruling 10 asks for.

Per Huayin's governing refinement, the repair does **not** disclose after the fact. The coordinate is
preserved first; only then does declared law speak. Each operand's own Φ travels into the map, so the
one distinction current law can make survives:

| absent operand's Φ | the coordinate is | caveat | materiality | mood |
|---|---|---|---|---|
| `undefined` | **ineligible** — outside that operand's population | `out_of_population` | immaterial | `serve` |
| `unknown` | **eligible but unsupported** — a real shortfall | `data_gap` -> `incomplete_data` | MATERIAL | `disclose` |
| `zero` / mixed / none | undetermined — see the missing representation below | `data_gap` | MATERIAL | `disclose` |

**A `zero` rule never fills a divergence gap.** `zero` declares what an absence of *that measure*
denotes; it says nothing about a coordinate where one operand was present and the other absent.
Filling would assert the expression was nil when what is true is that it is undefined. The guard is
conservative by construction — a column carrying any divergence gap is not filled at all, because the
two null-origins are not separable per cell at that point, and not-filling is the only direction that
cannot fabricate a value.

**No wire field, no contract bump.** `DATA_GAP` was already declared and already wired MATERIAL as
`incomplete_data` with zero producers; it now has one. `derive_outcome` supplies the mood flip.

**THE MISSING REPRESENTATION, reported rather than invented** (per the ruling): **nothing declares how
Φ composes through an operator.** `_column_fill_rule` infers a column's Φ by unanimity over its atoms,
which is sound for measure absence and silent about expression absence. Two operands declaring `zero`
do not thereby declare that `a / b` is nil where `b` is absent — that is division by an absent
denominator, not a nil quantity. Mission A therefore refuses to fill and says so on the wire. A
declared Φ-composition law is Mission C's territory, not this one's.

Standing test: `tests/test_alignment_domain.py` (10 cases — equal supports invent nothing; either
side may be short; the population claim now matches what is served; ineligible stays immaterial and
`serve`; `zero` never fills; provenance caveats still ride alongside; warm/cold agree; and the
P1-10 scope boundary is pinned so the coupling claim cannot rot again).

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

### P2-03 · The reducer law is attached to the measure, not the family — a ToD v5 ontology fossil · **CRITICAL** · VX

**Merged row.** This absorbs the former **P2-04** (*"the execution grammar is v5-ontology; the
publication is v6-ontology"*), which was the same finding seen from the other end. They were split,
and the split is what let the finding be re-summarized as a field-placement problem — this row's
previous title was *"`root_evaluator` is identity-bearing Data World information placed below the
governance line,"* and a title that understates its body is the title that gets carried forward.
**Placement is the least of it** (Huayin, 2026-08-31).

#### The claim

Under ToD v6.1 the vocabulary moves `v5 measure -> v6 measure family` and `v5 member -> v6 measure
F@A`. A measure family `F` has one full coherent family law `Law(F)`; `Law(F)` is a constituent of
the identity signature `Σ(F)`; a measure is `F@A` and **inherits** its family's identity and law. The
law belongs to **F**, and is not rediscovered per `F@A`.

Columna associates reducer identity with the individual **measure/member**, through
`root_evaluator`. That is the v5 shape, and it survives as a fossil of an implementation written
while the Theory was still moving. **The correction is not to relocate `root_evaluator` into the
governed publication** — that would preserve the mistake in a better postcode. It is to restore
**family law as canonical**, with the measure inheriting it.

#### What the artifacts actually contain

The four governed members of `firstlight` are **byte-identical except for their names**
(`fixtures/firstlight/governed-publication.json`):

```
member revenue_sum   -> {"anchor":"sale_at","measure":"revenue","universe":"sales"}
member revenue_count -> {"anchor":"sale_at","measure":"revenue","universe":"sales"}
member revenue_min   -> {"anchor":"sale_at","measure":"revenue","universe":"sales"}
member revenue_max   -> {"anchor":"sale_at","measure":"revenue","universe":"sales"}
```

The governed layer does not *under-specify* their meaning — it says **nothing whatsoever** about it.
The string `revenue_count` is the only thing suggesting counting, and a name is not governed content.
Their entire distinguishing meaning is `root_evaluator` in the private mapping
(`fixtures/firstlight/private-core-mapping.json`), which the compiler reads, uses, and discards:
governed member names disappear and the Core family is rebuilt keyed by **operator**
(`manifold.cml`: `FAMILY { count max min sum }`).

The two governed artifacts key the same family differently and **neither carries the association**:

| artifact | family keyed by | contains |
|---|---|---|
| `governed-publication.json` | member **name** | `revenue_sum` … `revenue_max`; no reducers |
| `manifold.cml` | **operator** | `FAMILY { count max min sum }`; no member names |

Core's word *family* and ToD's word *family* are **near-inverses** — Core's is a set of reducers over
one column; ToD's is one law.

#### Why `MEASURE revenue FAMILY { sum count min max }` is not a v6 family

It is a v5-style execution container grouping what v6 may treat as **distinct governed families**:
differing reducer laws establish differing family identities (ToD v6.1 §5.6 —
`revenue@B ==γ_MAX=> max_revenue_B@B` is an identity event even where displayed values coincide). If
MAX over monthly revenue is a genuinely different analytical quantity, it is `MaxMonthlyRevenue`
(root `Revenue@StoreMonth`, reducer law MAX) — a different family, not another entry inside Revenue.
Likewise COUNT is plausibly an `OrderCount` family. **Different operator names do not constitute a
family set; family identity and family law do.**

That this is not merely hygiene is now demonstrated by execution — see **P1-10**, where two members of
this one container carry different denominators and their ratio serves silently.

#### `root_evaluator` may be in the RIGHT file — which changes the shape of the repair

Two bullets this row previously carried are **retired**, and the retirement matters:

- ~~*wrongly placed* — beside the physical endpoint in the private mapping~~
- ~~*outside the receipt binding* (P2-02)~~

The older Theory distinguished two different jobs, and the v6 transfer material preserves the
distinction: **root formation / root evaluator** is the empirical/physical constitution of the native
member, while a **family reducer** is an identity-preserving role under the measure law. If
`root_evaluator` is genuinely the former, the private mapping is the **correct** home for it — it is
physical, and it belongs below the governance line.

The defect is then not a field in the wrong file. It is that **the governed layer has no `Law(F)`
carrier at all**. That makes the repair **additive rather than a relocation**, which materially
shrinks the P2-01 compatibility problem: a new governed slot refuses far less of what compiles today
than a moved required field would.

What survives from the original four bullets, and is now the headline:

- **too weak in type** — a bare operator name is not a full family law. ToD v6.1 §5.1: two operations
  both called `SUM` need not instantiate the same family law if participation, multiplicity, support,
  regime or approximation differ.
- **absent from the shipped runtime unit** and discarded after compilation.

The compiler's own docstring names the boundary it is protecting (`compiler/inputs.py:168-169`):
*"`root_evaluator` is captured, never invented: a compiler that chose a reducer would be
manufacturing analytical law."* It correctly refuses to manufacture the law. It has nowhere governed
to write down the law it was handed.

#### The fossil is narrower than "Core is operator-keyed"

Two facts bound the blast radius, and both were missed by the six audits:

**The shipped demo already does it the v6 way.** `tests/fixtures/benchmark.cml:44-46` declares three
separate measures, not one four-flavoured family:

```
MEASURE revenue  ON transactions FROM transactions AS sum(amount)
MEASURE orders   ON transactions FROM transactions AS count(*)
MEASURE visitors ON transactions FROM transactions AS distinct(customer_id)
```

`orders` is its own measure. The v5 container is concentrated in the **governed fixture**, not in the
execution grammar generally.

**`FAMILY` also does a second, legitimate job, and it is already `Law(F)`-shaped**
(`tests/fixtures/benchmark.cml:52-57`):

```
MEASURE level ON store_days FROM eom_inventory VALUE level
    FAMILY {
        sum  BLOCKED { calendar }
        last ORDER day
    }
```

That is not two flavours of a quantity. It is **one** quantity carrying *per-lineage movement law* —
summing inventory across time is non-reconciling; period-end `last` is the point. Movement law,
closure and blocked lineages are `Law(F)` content, present in the grammar today. So the crosswalk is
not starting from zero, and `FAMILY` must not simply be deleted as a fossil: it **conflates** the v5
member-container with a real delivery/movement grouping, and separating those two jobs is the first
concrete deliverable. The practical cost lives here too — one `.cml` declaration currently yields one
delivery reduced several ways, and a strict family-per-law model needs somewhere for that fertility
grouping to go.

#### What this gates

**OF-28** (`specs/open_forks.md`) is an open stop-gate in its own words: *"no public governed-
publication authoring surface opens while the implementation vocabulary decision remains
unresolved… an authoring surface mints governed objects under whichever vocabulary it exposes, and
that choice is not reversible by documentation afterwards."* The v5→v6 crosswalk **is** that
decision. Unit D therefore unblocks the author → ratify → publish third of the lifecycle rather than
sitting adjacent to it.

**Retired formulations — do not carry forward:** *"root evaluator != family/default reducer"*; and
*"move `root_evaluator` from the private mapping into the governed publication"* (the placement
framing, corrected by Huayin 2026-08-31).

**Sources.** `compiler/inputs.py:176`, required at `:260-264`;
`fixtures/firstlight/private-core-mapping.json`; `fixtures/firstlight/governed-publication.json`;
`governed/firstlight/manifold.cml`; ToD v6.1 §§1.2, 5.1, 5.6; the Three Pillars reconstruction
(Huayin, 2026-08-31).

### P2-04 · *(merged into P2-03, 2026-08-31)*

Kept as a tombstone because the ledger's ids are cited elsewhere and a stable id must not become a
dangling reference. Its content — *"the execution grammar is v5-ontology; the publication is
v6-ontology"* — is the same finding as P2-03 seen from the execution end, and the two are now one
row. **See P2-03.**

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

### P0-18 · The Manual documents Frame-QL forms the shipped planner refuses · **HIGH** · VX

Found 2026-08-31 in the Column Algebra Mission 1 reconciliation. Same defect class as **P0-17**
(operators marked available that do not resolve) and **OF-18**'s form-primacy finding (a careful
reader learns a form the parser rejects).

Verified through the real ask surface (`parse_statement` -> `run_statement` -> `wire_frame`):

```
manual 2.4 / 6.5  bare map (documented)     -> serve   served
manual 2.4        PINNED map operands       -> error   unknown column 'transaction'
manual 2.4        pinned, composite pin     -> error   unsupported expression node Tuple
manual 2.1        multi-input canonical     -> error   'corr' is not a scan operator
multi-arg shipped reducer                   -> error   'avg' takes exactly one column argument
```

Three distinct false claims:

- **`:277`** states the canonical multi-input shape `op(col_1 @ {a_1}, col_2 @ {a_2}, ...)` and adds
  *"The framework parses this form directly, type-checks it, and plans it."* Reducers are
  hard-arity-1 at `planner.py:908`.
- **`:329-331`** shows pinned map operands as executable examples. Both error.
- **`:561`** states *"The framework checks that all input column references resolve to the same input
  anchor."* **No such check exists.** Co-anchoring holds only because `_node` hands both operands the
  identical output anchor (`planner.py:1609-1610`) and joins on it.

A fourth, consequential: the multi-input clarify documented at **`:315`** (`input_anchor_ambiguous`
*"covers the multi-input case"*) is **unreachable** — the arity gate fires first with a generic
`unknown`.

**Why the standing gate did not catch it — the structural finding.**
`docs/tools/check_manual_frameql.py` is **grammar-only by design**, and says so: *"it may still
refuse/clarify at PLAN time; that is semantics, not grammar — this check is grammar only."* Every
example above **parses clean**. The gate proves the manual cannot document syntax its own parser
rejects; it proves nothing about whether the documented form *runs*.

**Recommendation:** extend the standing check to **plan** each example against a fixture manifold,
asserting each either resolves or carries a documented refusal — the same upgrade OF-18 asked for on
status marks, applied to executable form. That is Mission B, not this row.

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

## Unit D — OPEN · scope only · **no implementation authorized**

Opened 2026-08-31 on Huayin's ruling. **This unit's deliverable is a crosswalk, not a change.** No
code, no schema, no artifact edit is authorized by this section, and the acceptance test below is a
document. That constraint is the point: the mistake this unit exists to avoid is answering *"where
should `root_evaluator` live?"* — a question that presupposes the fossil it is trying to remove.

### The question

> **What concepts in current Core correspond to v5 Measure, v5 Member, root evaluator, and family
> reducer — and what should each become under the canonical v6 MeasureFamily / Measure `F@A` /
> `Law(F)` model?**

Only after that crosswalk can it be decided whether `root_evaluator` disappears, survives as a
realization / root-constitution field, is renamed, or moves into a lower-level realization contract.
The one thing already ruled out: **it must not remain the thing that tells a measure which reducer
family it belongs to** (Huayin, 2026-08-31).

### Why it is a crosswalk and not a repair

Columna was built while the Theory was moving, and absorbed both eras. The result is hybrid — a v5
publication ontology, an operator-keyed Core family, `root_evaluator` per old-style member, and
partial v6 terminology. The compiler's behaviour is the fossil in one sentence: it sees governed
`member`s, ignores `root_member`, reads the member's `root_evaluator`, drops the governed member
name, and rebuilds the Core family from operator names. Viewed through v6 that is not one misplaced
field; it is an older ontology still load-bearing.

### Deliverables

| # | deliverable | why it is first |
|---|---|---|
| **D1** | **The v5→v6 crosswalk table.** Every current Core concept — `measure`, `member`, `family`, `MeasureColumn`, `FamilyMember`, `root_member`, `root_evaluator`, `FAMILY {...}`, `K0_REDUCERS` — mapped to its v6 counterpart, or explicitly marked as having none | Everything else is a guess without it |
| **D2** | **Separate `FAMILY`'s two jobs.** It currently conflates the v5 member-container with a *legitimate* per-lineage movement grouping (`sum BLOCKED {calendar}` / `last ORDER day`) that is already `Law(F)`-shaped. Name both; decide which keeps the word | The construct must not be deleted as a fossil when half of it is the thing we want |
| **D3** | **Rule `root_evaluator`'s fate** against D1 — including the live possibility that it stays exactly where it is as root *formation*, and the governed layer gains a `Law(F)` carrier beside it | Determines whether the repair is additive or a migration |
| **D4** | **State the compatibility consequence**, quantified against `firstlight` and the demo corpus: which publications that compile today would stop compiling, under each option | P2-01's coupling is the whole cost, and it is currently an assertion, not a count |

### What this unit does NOT do

- **No implementation.** Not the governed slot, not a compiler change, not a fixture rewrite.
- **No renaming in the runtime.** The v6 runtime checkpoint §11 ratified *"No renaming"* and that
  stands until D1 says otherwise.
- **No deposited bytes edited.** ToD v6.1 is published under a DOI; the crosswalk reads it, and
  a fork ledger is not a publication authority.
- **Not connected to Column Algebra or the current Frame-QL research** — held separate at Huayin's
  explicit instruction (2026-08-31), unless he connects them later.

### Acceptance

A crosswalk document that a reader can use to answer *"what is this concept, under v6?"* for every
row of D1 without consulting a person — plus D4's count. **Green is a document Huayin can rule on,
not a passing test.**

### Rows it governs

**P2-03** (the merged ontology-fossil row) is the subject. **P1-10** is coupled to it and is the
reason the unit has a wrong-number consequence rather than only an ontological one. **P2-01** and
**P2-09** are coupled through Appendix A. **P2-02** is expected to dissolve rather than be repaired:
the receipt binding already distinguishes the four images, and what the four-mappings reproduction
actually shows is the publication under-determining its own meaning — restoring `Law(F)` to the
governed layer removes the under-determination at its source, which adding a mapping digest to the
binding would not.

### What it unblocks

**OF-28**, the open stop-gate on the implementation vocabulary, whose own text makes it a
precondition for opening any public governed authoring surface: *"an authoring surface mints governed
objects under whichever vocabulary it exposes, and that choice is not reversible by documentation
afterwards."* Unit D is that decision, so it stands in front of the author → ratify → publish third
of the governed lifecycle rather than beside it.

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

**Where the packaged half lives:** [PR #251](https://github.com/datumwise/columna/pull/251), carrying
the two README edits alone — a live PR, not a parked commit. It is expected to be red on the
stale-payload gate, and that redness is the row.

**RULED (Huayin, 2026-08-31): ride the next release. Do not mint one.** The reasoning, recorded so
the decision does not have to be re-derived: what remains false is two PyPI front pages — a stale H1
version and a missing `firstlight` mention — which is the quietest surface in the P0 set, and not
comparable to a purchasable tier asserted on two live routes. `release_pins.py` already carries the
house's value against minting releases *"whose only content is a version number."* And waiting is
reversible where a burned version number is not.

**The condition that would flip it**, also recorded: if no code release is expected within roughly a
month, mint `columna-core 0.18.1` + `columna 0.18.1` (lockstep) + `columna-server 0.11.1` rather than
let two false front doors outlive the unit meant to close them.

**What makes waiting safe rather than hopeful.** The P0-08 orphaning is structurally closed here — a
live PR, the reason recorded on it, and P0-11/P0-13 marked PARTLY FIXED rather than struck. Beyond
that, `docs/RELEASE_ORDER.md` gained a **step 0**: sweep `gh pr list --label release-gated` and fold
those PRs in, or decide explicitly not to. #251 carries the label. "The next release will remember"
is not a mechanism; a labelled query is.

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
| **P2-01 + P2-03 + P2-09** | Φ and `root_evaluator` are both *silently dropped* rather than refused. A generic refusal-before-omission rule (P2-01) makes both fail closed immediately, which is correct but will refuse publications that compile today. **Eased 2026-08-31:** P2-03's repair is now understood to be **additive** (a governed `Law(F)` carrier) rather than a relocation of a required field, so the set of publications a refusal rule would reject is materially smaller than this row assumed |
| **P1-10 + P1-11** | ~~A repair at the join addresses both~~ — **CORRECTED 2026-08-31 by execution.** Mission A repaired the join and P1-10 is **unchanged**: `revenue.sum / revenue.count` still serves 20.0 with zero caveats. Both members produce a row at the anchor, so the alignment domain is identical and there is no coordinate for it to preserve. P1-10's divergence lives in the **underlying observation counts**, which needs support as a set of OBSERVATIONS, not of coordinates. The two rows share a collapse site and nothing else. Pinned by `test_alignment_domain.py::test_p1_10_is_not_addressed_by_the_alignment_domain` |
| **P1-10 + P2-03** | P1-10 is the v5 family container producing a number. Re-typing `count` or minting a support caveat treats the symptom and leaves the container. The caveat is the cheap partial mitigation if P2-03 runs long |
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
