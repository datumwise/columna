# Frame-QL vNext — M2 Reconciliation Reconnaissance (full record)

**Repo:** `datumwise/columna` @ `17e3b6b` (`main`, clean) · **Run date:** 2026-09-06 · **Mode:** read-only reconnaissance — nothing edited, no code change proposed here.

Complete written record of the M2 reconnaissance run: the synthesis delivered in the room, the two interim probe findings that preceded it, and all eight inspector reports in full. Part 1 is the document to read first; Part 3 is its evidence base, reproduced verbatim as each inspector returned it.

Target-design documents under review (working copies at `/tmp/m2recon/`):

| Doc | Inspected in |
|---|---|
| `frameql_vnext_r4_standing_amendment_v0_2.md` | §3.1 |
| `frameql_vnext_capability_profile_reconciliation_plan_v0_1.md` | §3.2 |
| `frameql_language_vnext_working_draft_v0_3.md` | §3.3, §3.4 |
| `frameql_vnext_m1_semantic_review_v0_1.md` | §3.5 |
| `frameql_vnext_o1_ordered_expression_compatibility_ruling_v0_1.md` | §3.6 |
| `frameql_vnext_authority_reconciliation_v0_1.md` | §3.7 |
| `frameql_vnext_current_manual_migration_matrix_v0_1.md` | §3.8 |

## Contents

- **Part 1** — Synthesis: M2 reconciliation reconnaissance
- **Part 2** — Interim findings surfaced during the run
- **Part 3** — Inspector reports (verbatim)
  - 3.1 R4 standing amendment vs. current implementation (placement loss, lost records)
  - 3.2 Capability authority — schema, generators, Core/Platform profile coupling
  - 3.3 Parser & expression grammar
  - 3.4 Canonicalizer / desugaring layer
  - 3.5 Planner / adjudication, broadcast, WHERE
  - 3.6 Ordered-expression machinery
  - 3.7 Manifold authoring + authority reconciliation
  - 3.8 Category-change blast radius (test surface)

---

# Part 1 — Synthesis

## Frame-QL vNext — M2 Reconciliation Reconnaissance

Reconnaissance only. Nothing edited, no PR. Eight read-only inspectors plus direct probes of the running engine; claims below are file:line (SV) or reproduced (VX) and marked where it matters.

---

### 1. Executive conclusion

**Reconcilable incrementally — with one exception that is not a migration at all.**

Eleven of the twelve surfaces move by renaming, adding a field, or deleting prose. The exception is **standing**: the current architecture cannot represent the R4 distinctions, and on one of them it is not merely silent but actively wrong. That is an architectural addition, not a reclassification, and it should be sequenced last and separately.

Three findings shape everything else:

**(a) The capability spec is not a routing authority, so the taxonomy change is nearly free.** `specs/frameql_capabilities.toml` is read by exactly three tools under `docs/tools/`; nothing under `packages/` imports it. Adding `semantic_class` cannot create a second routing authority because the TOML is not one today.

**(b) The real authority is `Operator.kind`, and it does three jobs at once.** It is the semantic category (`operators.py:40`), the routing discriminant (`planner.py:1830, 2038, 2448`; `engine.py:299`), **and** the publish-time admission rule for measure families — `parser.py:686-692`, *"only reducers found families"*. vNext separates the first from the second; the third is the chokepoint.

**(c) The `first`/`last` reclassification is therefore cheap in the spec and expensive in the registry.** Spec-side: a category string. Registry-side: three shipped `.cml` families stop publishing (`cascadia/manifold.cml:59-60` `FAMILY { last ORDER category }`, plus `stock`), six test files fail at fixture-parse time, the B-anchor crossing law loses the operator it names as the lawful remedy, and `describe_measure.family.reducer_kind` returns a different string on an unchanged utterance — a wire bump under the file's own rule.

Everything else divides cleanly: **brackets are free** (not parsed, zero tests, documentation-only), **dot is a wire-naming question** not a grammar question, **broadcast and WHERE are already vNext-shaped** and need terminology plus one jurisdiction ruling, and **ordered expressions need five new fields that do not exist anywhere**.

---

### 2. Verified current state

| | |
|---|---|
| repo | `datumwise/columna`, branch `main`, HEAD **`17e3b6b`** (2026-09-02), clean, in sync with origin |
| packages | `columna` 0.19.0 · `columna-core` 0.19.0 · `columna-server` 0.12.0 · wire `CONTRACT_VERSION = "4"` |
| four authorities | all present and current — `docs/frame_ql_language.md`, `docs/core_profile.md`, `docs/platform_profile.md`, `docs/frame_ql_build_status.md`, over `specs/frameql_capabilities.toml` + `specs/profiles/*.toml` |
| capability measurement | live: **86 canonical (22 ratified) · core profile 30 realized · build deltas 0 (0 lag, 0 exceed) · platform +0** |
| tests | 1075 collected (766 core / 309 server) across 89 files |
| sibling repos present locally | `manifold-agent` (`d9ea705`), `columna-studio` (`244fd34`), `manifold-eval`, `gatework` |

**Changed facts since the attached matrix: none in the repo — but the matrix does not index it.** `main` has not moved since 2026-09-02, i.e. before the package was written, so nothing changed underneath you. However the matrix's line ranges drift progressively against the shipped Manual (§1.1 *"What a query is"* 60–66 vs actual 76; §2.4 365–383 vs 446; §2.8 445–455 vs 539, where the heading is *"Subsetting and scans"*). Offset grows +8 → +94. **Do the clause migration by heading, not by line.** Also: the four-document split is `a38ab4c`, dated 2026-09-02, not 1 September.

---

### 3. Coupling map — where the categories are actually consumed

```
LANGUAGE LAW            docs/frame_ql_language.md  (prose only; no code reads it)
        │
CAPABILITY SCHEMA       specs/frameql_capabilities.toml   category · position · standing
        │                     │                                 · re_entry_certified
        │                     └──► docs/tools/ ONLY  ─── regen_capability_tables.py  (category → _SECTIONS)
        │                                            ├── capability_authority.py     (position → measurement path)
        │                                            └── check_manual_frameql.py     (spellings → Appendix A)
        │                              ✗ NO import path into packages/
PROFILES                specs/profiles/*.toml   ── capability ids + level only; class-agnostic
        │
════════ the spec stops here. Everything below runs off a SECOND, UNLINKED authority ════════
        │
RUNTIME TAXONOMY        operators.py  Operator.kind {reducer,scan,map} · witness · re_entrant · needs_order
        ├── parser.py:686-692     kind == REDUCER  ⇒  may found a measure family     ← the chokepoint
        ├── planner.py:1830       kind == scan     ⇒  scan call admitted
        ├── planner.py:2448       kind == map      ⇒  pointwise apply
        ├── planner.py:2038       kind == reducer ∧ is_monoid ⇒ B-anchor crossing
        └── engine.py:238-246     witness          ⇒  VALUE / ORDERED / SKETCH dispatch
        │
WIRE                    disclosure_wire.py CONTRACT_VERSION "4" · CATEGORY_TABLE (closed)
BUILD STATUS            measured by importing the installed package
```

Two parallel unlinked claims already exist across that gap, with **no gate comparing them**: `category`(spec) ↔ `kind`(registry), and `re_entry_certified`(spec, read by nothing) ↔ `re_entrant`(registry, read by `planner.py:1514-1551`). A third would be added by any `semantic_class` that is not cross-checked.

---

### 4. Semantic mismatch matrix

| Area | Current | vNext target | Jurisdiction | Size | Compat risk |
|---|---|---|---|---|---|
| **dot** | `Attribute(Name, attr)` = measure·member, one dot only (`planner.py:1322-1329`); the dotted text **is** the canonical column key (`:776`). `.` carries **four** position-dependent meanings | `revenue.sum` → family law; `level.last` → ordered expression; compatibility where unique | language + wire | small in grammar, **wire bump** if the key changes | high — `columns[].name` is the literal precedent for `"1"→"2"` |
| **brackets** | `ast.Subscript` not in `_ALLOWED`; no production consumes a bracket; **zero tests**; `[ROADMAP]` in the Manual | `[]` = value subscription; predicate filtering retired | language | **trivial** | none — but `check_purged_grammar.py` matches only the `EDGE…ALONG…VIA` form and will not guard the retirement |
| **family laws** | family = operator token + home table; `mean` registered but `in_core=False` and rejected as a family member (`parser.py:687`); `variance`/`covariance` absent from the registry; arity hard-wired to 1 (`planner.py:1367`) | law-formed identity with constitutive inner anchor | ToD + Manifold + language | large, mostly **absent seams** | low — nothing to break |
| **first / last** | `kind=REDUCER`, `ratified`, `execute` in Core; found families at publish; `witness=ORDERED_W`; direction smuggled into `combine="argmax"/"argmin"` | ordered expressions, not families | spec + registry + Manifold + wire | **largest** | **highest** — 3 shipped families, 6 fixture files, `reducer_kind` wire field |
| **scans** | `proposed` standing, `execute` in Core (already an admitted exceedance); params `n=`, `by="…"`, `window=` refused | ordered-expression layer, governed order contract | language + registry | medium | low — already `proposed` |
| **broadcast** | only `@ {}`; collapses to kind `"scalar"` and **erases the frame** (`planner.py:2489-2504`); any non-scalar coarse operand → `co_anchor_required` | structural alignment preserving coarse identity | language + planner | medium | low — satisfies the target by erasure, not representation |
| **WHERE** | per-series, pre-reduction, macro-expanded, never a carve — **already correct** (`planner.py:829-845, 1079, 570-573`) | analytical restriction | language + jurisdiction | terminology only… | …**except** `filter_unsupported` is deliberately pinned REALIZATION by `test_jurisdiction_seam.py` / `test_filter_jurisdiction.py`; moving it mints a `_KNOWN_INVERSIONS` entry **by design** |
| **standing / fill** | one axis, four Φ dispositions, dispatched off `null_count()`; no existence, no placement, no eligibility-unresolved | six-layer standing | ToD + language + wire | **architectural** | **bump** — the four absence codes cross the wire |
| **promotion** | `AS` and `WITH` mint nothing (`planner.py:766-771, 798`); `DERIVED` with empty FAMILY is a named non-family expression, distinguished only by an empty dict; **no kind for it in the governed publication** | promotion belongs to Manifold authoring | Manifold | small | none |
| **capability taxonomy** | `category` read by one generator; `_SECTIONS` hardcoded to the three implementation-shaped values — an unrecognised value is **silently dropped from all four tables with a green gate** | `semantic_class` beside `position` | spec + generators | small | medium — silent-drop hazard |

---

### 5. Recommended migration sequence

Independently reviewable, each with a stop-gate.

1. **Retire the bracket filter.** Documentation-only: Manual §2.8/§6.7 and line 215. Zero code, zero tests. *Stop-gate:* add a `check_purged_grammar.py` pattern so the retirement is class-guarded, or it silently regrows.
2. **Schema evolution — add `semantic_class`, populate nothing yet.** Generalize `_SECTIONS`/`_by_category` first so an unknown class fails loudly instead of vanishing. *Stop-gate:* `capability-tables --check` byte-identical; profile promises unchanged (they are id-only, so this is provable).
3. **Reclassify in the spec only** — `first`/`last` → `ordered_expression`, keep ids, keep `ratified`, keep Core `execute`. Registry untouched, runtime untouched. *Stop-gate:* `capability_authority` reports the same 86/22/30/0; `frame_ql_build_status.md` regenerates with identical build columns.
4. **Add the spec↔runtime cross-check** (see §8-D). This is the slice that stops the divergence you are about to widen.
5. **Ordered-expression contract as an EXPLAIN payload block** — `order_contract: {axis, direction, ties, peer}` beside `cone` in `frameql.py:96-108`, populated from `plan_order_axis` and `FamilyMember.order_by`. Additive, no grammar change, no `render_canonical` change. *Stop-gate:* `desugared` string unchanged.
6. **Declare direction and tie rule** on ordered members. Precedent exists and is fail-closed: `FACE … ASSIGN BY <m> ORDER MIN|MAX` is mandatory with no default (`parser.py:299-318`; tie → `FaceContradiction`). *Stop-gate:* `arg_max` tie-breaking stops being DuckDB's.
7. **Then, and only then, the `first`/`last` registry move** — behind a ruling on what happens to `FAMILY { last ORDER … }`.
8. **Standing, as its own mission.** Do not attach it to the expression work.

---

### 6. Schema options

**A — new `semantic_class` axis, keep `category` as deprecated-but-emitted.** Both fields present; generators read `semantic_class` with `category` as fallback. Zero-risk rollout, but two category fields coexist and the stale one will be copied by the next author.

**B — rename `category` → `semantic_class` with the new value set, in one pass.** Single axis, no duplication. Requires all 86 rows edited and `_SECTIONS` rewritten in the same commit; the generated tables change shape once, visibly, under `--check`.

**C — `semantic_class` plus a `realization_kind` mirroring `Operator.kind`, cross-checked by a gate.** Makes the spec↔runtime relationship explicit and checkable instead of conventional.

**Recommend B, plus the cross-check from C as a separate gate (slice 4) rather than a third field.** B because the plan's own conceptual split (`capability identity / semantic class / surface position / canonical standing / profile realization / build realization`) is already six clean axes and a deprecated seventh helps nobody; `position` stays as the surface axis untouched, which leaves `capability_authority.py:116` alone. The cross-check belongs in a gate, not a field, because `Operator.kind` is a *build* fact and duplicating it into the canonical authority would let a spec edit contradict the runtime silently — the failure mode `re_entry_certified` already demonstrates.

---

### 7. Compatibility strategy

**Accepted unchanged:** `revenue.sum` / `level.last` (parse and canonical key unchanged); `@ {…}` pins; `by="level"`; `AS`/`WITH`; every `FILL` rule; the whole envelope.

**Needs canonical re-normalization:** the `avg`→`mean` split — `operators.py:219-223` states plainly that `canonical()` is *not* wired into member lookup, so `desugared` still spells `avg` while governed identity is `mean`. **Two canonicalizers disagree today**; any order work keyed on operator identity hits this first.

**Unshipped, retire freely:** the bracket predicate filter; `window=`; `reset`/`within`/`step` (documented at `frame_ql_language.md:559-563`, no code representation at all); `rank`/`dense_rank`/`row_number` (in the TOML, absent from the registry).

**Cannot be compatibility-only:** `FAMILY { last ORDER … }`. It is a *declaration*, not a query spelling — accepting it while `last` is no longer a reducer requires the publish gate at `parser.py:686-692` to admit a non-reducer family founder, which is a semantic change to the authoring language, not a compatibility affordance.

---

### 8. Questions requiring your ruling

**A · Where does a completed ordered contract live?** O1 requires canonicalization to expose the completion. But `test_envelope_parser.py:136` pins `parse_statement(render_canonical()) == st`, so **any rendered canonical field becomes surface syntax by construction**; and if it is not rendered, `test_envelope_explain.py:17-21`'s `desugared == the consumed artifact` becomes false. *Choices:* (i) EXPLAIN payload block, no grammar change — round-trip law intact, but the in-process artifact `run_statement` consumes is still string-only; (ii) amend the round-trip law and put it on `Statement`; (iii) new surface syntax. **Recommend (i)** for M2 and defer (ii). Code cannot decide this: it is a law about what canonical form *is*.

**B · What happens to `FAMILY { last ORDER category }` when `last` stops being a reducer?** *Choices:* (i) keep `last`/`first` as reducers in the registry indefinitely and let the spec category diverge deliberately, documented; (ii) admit non-reducer family founders at `parser.py:686`, which makes "ordered expression" and "family member" overlap — the thing vNext §10.3 says must not be erased; (iii) migrate the three shipped families to a different declaration and accept the break. **Recommend (i) for M2**, ruled explicitly as a *stated* divergence with the cross-check gate reporting it, so it cannot rot into an accident.

**C · Does `filter_unsupported` stay REALIZATION?** vNext calls WHERE analytical restriction. The current split is deliberate and tested: reachability failures are ANALYTICAL, push-down failures are REALIZATION (`test_filter_jurisdiction.py`), and `test_jurisdiction_seam.py::test_the_only_reason_level_inversions_are_the_ones_the_ledger_rows` asserts `_KNOWN_INVERSIONS = {}`. I read the current split as *already* implementing M1-B correctly — the restriction is analytical, the push-down gap is a build fact. **Recommend: no change**, and say so in the Manual so a future reader does not "fix" it.

**D · Do you want the first spec↔runtime cross-check?** Evidence: `category`↔`kind` and `re_entry_certified`↔`re_entrant` are parallel claims with nothing keeping them in step. Code cannot decide whether that is acceptable — it is a question about how much authority the canonical registry has over the build. **Recommend yes**, as a report-only gate first.

---

### 9. Suggested first slice

**Slice 2 above — the schema evolution, with no reclassification.** Add `semantic_class` to `frameql_capabilities.toml`, generalize `_by_category`/`_SECTIONS` so an unrecognised class **fails loudly instead of vanishing from four manuals under a green gate**, and leave every row's value equal to its current `category`. Byte-identical generated tables, zero runtime touch, zero wire touch, fully reviewable. It buys the axis and closes the silent-drop hazard before anything is reclassified through it.

---

### Defects found en route (not in the brief; you will want them)

1. **Placement loss is served silently at a fabricated coordinate (VX).** Four records, one with its `day` lost: `AT {store}` → `100.0`, exactly right; `AT {store, day}` → a row `day=None, revenue=70.0` with **no disclosure of any kind**, alongside a value-loss row that *is* disclosed (`undeclared_absence`). R4 §7.3's decisive case, landing as an invented anchor point. The crossing path does the same thing deliberately (`engine.py:552-553, 738-750`): it manufactures an anchor point per bridge category and Φ-fills it.
2. **`check_frame_query` raises where its documented contract promises a wire (VX).** `tools.py:401` says *"A syntax error is an `error` wire"*. Measured: `execute_frame_query` returns `frameql_syntax` correctly; **`check_frame_query` raises `FrameQLSyntaxError` uncaught** for the same statement. The cheap pre-flight and the executing counterpart disagree at the MCP boundary — the plan/run divergence the tree already records as a repeat failure mode.
3. **Build-status measurement degrades silently.** `capability_authority.measure_build` swallows `ImportError` and returns `{}` (`:109-110`), so in an environment without the package the "measured" table regenerates to all-`—` with a green gate. Measured-ness is environment-dependent and fails open.
4. **`_atoms` defaults the family member unguarded** — `planner.py:1900` `next(iter(family))` where every other call site Clarifies on `|family| > 1`; it feeds the EXPLAIN wire atoms and `_column_fill_rule`.
5. **`describe` publishes a retired doctrine** — `describe.py:57-62` still maps `events → "absence is a lawful ZERO"`, which serving stopped implementing (`model.py:50-53`).
6. **`arg_max`/`arg_min` tie-breaking is DuckDB's** (`engine.py:325-329`), and the same operation ties differently at the combine boundary (Polars sort stability, `engine.py:769-773`). O1 §7 rules this non-canonical; there is no tie field anywhere to fix it with.

Stopping here as instructed. No code, no schema, no PR — and no first slice started.

---

# Part 2 — Interim findings surfaced during the run

## 2.1 Dispatch note

Target read. Eight inspectors are out across the twelve surfaces; I'll synthesize when they land.

Three things I can already state from direct inspection, all bearing on §2 of your deliverable:

**Current `main` has not moved since the package was written.** HEAD is `17e3b6b` (2026-09-02), clean, in sync with origin, `columna`/`columna-core` 0.19.0, `columna-server` 0.12.0. All four Frame-QL authorities are present and current — `docs/frame_ql_language.md`, `docs/core_profile.md`, `docs/platform_profile.md`, `docs/frame_ql_build_status.md`, over `specs/frameql_capabilities.toml` + `specs/profiles/*.toml`. The split commit is `a38ab4c` (2026-09-02, not 1 September as the matrix says).

**But the migration matrix does not index current `main`.** Its line ranges drift progressively against the shipped Manual — *"1.1 What a query is"* 60–66 vs actual 76; *"2.4 map expressions"* 365–383 vs actual 446; *"2.8 bracket filtering"* 445–455 vs actual 539, where §2.8 is titled *"Subsetting and scans"*. The offset grows from ~+8 to ~+94, so content was inserted after the copy the matrix was built from. Clause identification for the migration must be by **heading**, not by line.

**Brackets and scans are both already `[ROADMAP]`/`[SCHEDULED]` in the shipped Manual** (§2.8), which is the cheapest possible starting condition for the "retire the bracket filter" ruling — if the parser agrees, retirement is documentation-only. One thing to flag early: that same section currently teaches *"The order comes from an orderable axis in the anchor, such as day, or is named explicitly"* — which is precisely the inference vNext §9.9 forbids. Whether the **planner** does that or only the **prose** does is one of the questions out with the inspectors.

[eta task=8m request=25m] [focus: Frame-QL vNext M2 reconnaissance across 12 surfaces]

## 2.2 First probe results — placement loss reproduced

Three of eight in. Two findings from my own probes worth surfacing now, because both are load-bearing for the report and neither is a documentation issue.

**1 · Placement loss is served silently, and I reproduced it.** A four-record fixture: one record has its `day` coordinate lost, one has its value lost.

```
AT {store}          revenue = 100.0                     ← exactly right, all four records
AT {store, day}     day=None      revenue = 70.0        ← no disclosure of any kind
                    2024-01-01    revenue = 10.0
                    2024-01-02    revenue = 20.0
                    2024-01-03    revenue = None        ← undeclared_absence (caution) fires
```

Value loss **is** disclosed — `undeclared_absence`, or `unknown_absence` under `FILL unknown`. Placement loss is not disclosed at all: the lost-`day` record is served as an ordinary anchor point at a **fabricated `NULL` coordinate**, carrying a real value. That is R4 §7.3's decisive case ("value survives, placement does not") landing in the worst available way — the total stays exact while the daily frame silently invents a coordinate, and nothing in the wire says so.

**2 · The capability spec is not a routing authority, and that is why `first`/`last` are the hard part.** `specs/frameql_capabilities.toml` is read by exactly three tools, all under `docs/tools/`; no module under `packages/` imports it. Routing runs off a **second, unlinked** classification — `Operator.kind` in `operators.py` — and `parser.py:679-690` lets **only `kind == REDUCER` found a measure family**. So reclassifying `first`/`last` to ordered expressions in the spec is free, and changing them in the registry is not:

```
cascadia/manifold.cml:59   MEASURE priority     ... FAMILY { last ORDER category }
cascadia/manifold.cml:60   MEASURE alloc_weight ... FAMILY { last ORDER category }
                           stock                ... FAMILY { sum, last }
```

Three shipped families would fail to publish. The same unlinked-pair pattern already exists between `re_entry_certified` (spec, read by nothing) and `re_entrant` (registry, read by the planner) — so the migration's real question is whether to add the first spec↔runtime cross-check rather than leave a third parallel claim.

Five inspectors still out — parser, canonicalizer, ordered expressions, Manifold/wire, tests. I'll hold the synthesis until they land.

[eta task=6m request=15m] [focus: Frame-QL vNext M2 reconnaissance — awaiting 5 of 8 inspectors]

---

# Part 3 — Inspector reports (verbatim)


---

## 3.1 R4 standing amendment vs. current implementation (placement loss, lost records)

*Inspector `agent-ae0e557be629b51af` · primary target doc: `frameql_vnext_r4_standing_amendment_v0_2.md`*

### R4 Standing Amendment vs. current implementation — reconnaissance

All paths under `/data/repos/978ea3c9feee4ad79341d42517782efd/columna/packages/columna-core/src/columna_core/`.

#### Preliminary: what the system actually has

There is **no point-existence layer**. A frame's row set is whatever `SELECT keys, aggs FROM table GROUP BY keys` returns (`connector.py:259-271`), optionally filtered by the universe predicate (`engine.py:344-354`, `engine.py:965-981`). A universe is a *predicate over delivered carrier rows*, never a materialized domain (`model.py:44-48`). Consequently **a point exists iff a carrier row survives the predicate**. Absence is only visible when some *other* structure supplies a domain: the juxtaposition full-outer join (`planner.py:617-625`), the expression alignment join (`planner.py:2834`), or a crossing's bridge domain (`engine.py:552-553`, `engine.py:612-613`, `engine.py:738-740`). `planner.py:630` states this outright: "A single-column frame (no nulls) is untouched."

#### The table

| Target layer | Current representation(s) (file:line) | Faithful? | Gap? |
|---|---|---|---|
| **point existence** | Implicit only: carrier row survives `deliver_measure` GROUP BY (`connector.py:259-271`) then `_confine` predicate filter (`engine.py:350-354`, `965-981`). `Universe.predicate` (`model.py:47`), `Universe.basis` (`model.py:49-55`, `parser.py:50` `BASIS_TYPES={events,spine,product,registry}`). | **No** | No `Exist`/`nonexistent`/`existence-unsupported` trichotomy anywhere. Absent row = nonexistent point = unsupported existence, all one state (row not present). No spine/registry materialization: `basis` is inert for serving (`model.py:50-53`). |
| **point-existence support** | **Not represented.** Nearest artifacts: `MeasureColumn.m_anchor` → `missingness` MCAR/MAR/MNAR (`model.py:187`, `197-200`, `parser.py:486-488`), which is a *declared* selection-bias annotation, emitted only as an `UNCONFIRMED` caveat for MNAR (`engine.py:1233-1235`). `validate_universe_support` (`engine.py:1177-1226`) compares base-point *counts* across sibling measures — an authoring lint, not a runtime standing. | **No** | Nothing distinguishes "we know this event occurred but hold no row" from "no event". §7.4 / §14 (denominator 100 vs 99) has no representation: the denominator is always the observed row count. |
| **anchor placement** | **Not represented as standing.** Placement is realized as (a) the key columns of the group-by (`engine.py:344-357`) and (b) transport along certified functional edges — `_check_addressable` (`planner.py:417-500`), `_route`/`find_path` (`planner.py:380-392`), `ShapeEdge` (`projection.py:~108-121`). A NULL coordinate value in a carrier key column becomes its own SQL group with key NULL and flows through as an ordinary anchor point (no `drop_nulls`/`is_null` guard exists on any key column — grep over `engine.py`/`planner.py` returns null handling only on *values*, `planner.py:639,656,2837-2838`; `engine.py:743`). | **No** | π_A(ω) is assumed total and evidence-free. |
| **placement support** | **Not represented at all.** | — | This is the amendment's central object and it has no carrier. Failures near it are *geometry* failures, not *evidence* failures: `out_of_universe` (`disclosure.py:404`; raised `planner.py:404-408`, `495-499`), `uncertified_edge` (`disclosure.py:409`, `planner.py:485-494`), `contradicted_edge` (`disclosure.py:408`), `pin_coarser_than_output` (`disclosure.py:405`), `input_anchor_unavailable` (`disclosure.py:373`). All say "no lawful route from A to B", none say "this point's placement under A is unestablished". |
| **eligibility** | Two proxies, neither a predicate: `FILL undefined` → `OUT_OF_POPULATION` (`disclosure.py:57-58`; `planner.py:664-666`; `_DIVERGENCE["undefined"]` at `planner.py:2782-2784` explicitly "the point is INELIGIBLE"); and universe membership via the predicate (`engine.py:965-981`). | Partially | `FILL undefined` is a **column-wide constant**, declared per measure (`parser.py:430-437`, `model.py:180-185`), not per point. There is no per-point eligibility evaluation, so §8's three-valued eligibility cannot exist. |
| **eligibility support** | **Not represented.** | — | No third state. `FILL_RULES = frozenset({"zero","unknown","undefined"})` (`parser.py:53`) plus `None`=undeclared; none of the four means "eligibility unresolved". `UNDECLARED_ABSENCE` (`disclosure.py:59`) means *the author declared no rule*, not *the evidence is unresolved* — an authoring gap, not a data-standing gap. |
| **measure support** | Best-served layer. `UNKNOWN_ABSENCE` (`disclosure.py:55`, produced `planner.py:660-663`, `engine.py:750-752`), `DATA_GAP` (`disclosure.py:47`, `planner.py:2785-2787`), `UNDECLARED_ABSENCE` (`disclosure.py:59`, `planner.py:650-654`, `667-670`), `COVERAGE` (`disclosure.py:33`; `engine.py:570-573`, `718-722`), `SHADOW`/`OVER_COUNT` (`disclosure.py:60-66`). Wire codes at `disclosure_wire.py:114-127`. | Mostly | Represented as **column-level counted caveats** (`n_absent`), never as a per-cell standing. A reader cannot ask "is *this cell* supported"; only "N cells in this column were absent, and here is the column's rule". |
| **semantic value** | The Polars value column `_value`/named column; supported zero via `FILL zero` → `DECLARED_FILL` (`disclosure.py:53-54`, `planner.py:655-659`, `engine.py:742-746`), wired `("filled", IMMATERIAL)` (`disclosure_wire.py:117`). | Yes for declared-zero | Faithful only where `FILL zero` is declared *and* the domain-supplying join exists. Otherwise there is no zero/absent distinction to make. |
| **carrier null** | Polars null, undistinguished. `null_count()` (`planner.py:639`), `fill_null(0)` (`planner.py:656`, `engine.py:743`), `is_null()` (`planner.py:2837-2838`). Only special-cased for ORDERED ops, which *exclude* carrier nulls (`engine.py:337-342`). Connector `profile()` reports a `nulls` count (`connector.py:87`, `231`) — authoring only. | **No** | Carrier NULL is the sole substrate for every semantic distinction §11 forbids collapsing. |

#### 1. R4 §16 acceptance cases against the current architecture

| Case | Can current architecture represent it? | If not: what collapses into what |
|---|---|---|
| event known not to have occurred → nonexistent | **No** | "Nonexistent" collapses into "no carrier row", which is the same state as unsupported existence and as never-asked-about. |
| no record, no evidence → existence unsupported | **No** | Collapses into **nonexistence**. `connector.py:259-271` + `engine.py:350-354`: no row, no point, no trace. |
| Revenue lost, date retained → point exists, placement established, Revenue missing | **Partially** | Only if a *second* column or a bridge supplies the alignment domain (`planner.py:617-625`) **and** `FILL unknown` is declared (`planner.py:660`). Alone in a single-column frame, the cell simply does not exist (`planner.py:630`). If the carrier holds a row with NULL revenue, SQL `sum()` yields NULL/`count(*)` yields the row — no missingness is recorded at all. |
| whole record lost → point exists; lost coordinates unsupported placement; measures separately unsupported | **No** | Both failures collapse into **one absent row**. There is no channel that says "placement unsupported" and no channel that separates it from "measure unsupported". |
| Revenue preserved elsewhere, date lost → total establishable, Revenue@day not | **No** | This is the amendment's decisive case and the architecture has no expression for it. Two collapses: (a) if the row is dropped, the *unanchored total* silently loses the transaction too — the opposite of the required behaviour; (b) if the row is retained with a NULL `day`, `deliver_measure`'s `GROUP BY day` (`connector.py:270`) emits a **NULL day group** that is presented as an ordinary anchor point, so "unsupported placement" collapses into **a fabricated anchor point named NULL**. |
| operating-calendar store-day exists, no sales row, governed zero → supported zero | **Yes, conditionally** | `FILL zero` + `DECLARED_FILL` (`planner.py:655-659`, `disclosure_wire.py:117`) does exactly this — **but only where an alignment/bridge domain exists**. There is no operating-calendar spine to join against; `BASIS spine` no longer materializes anything (`model.py:50-53`). So the store-day that has no row anywhere is invisible, and the governed zero is never produced. |
| operating-calendar store-day exists, feed failed → eligible, missing | Same conditional as above, with `FILL unknown` | Same gap: without a domain the point does not appear, so `UNKNOWN_ABSENCE` is never emitted. |
| customer known, day unknown → customer claims possible, day claims blocked | **No** | No anchor-relative placement standing. `planner.py:2292-2299` resolves Φ per *column*, never per (point, anchor). Everything about the point is either wholly present or wholly gone. |
| point exists, metric not applicable → ineligible, not missing | **Partially** | `FILL undefined` → `OUT_OF_POPULATION`, IMMATERIAL (`planner.py:664-666`, `disclosure_wire.py:119`) is the right shape, but it is a **measure-wide declaration**, so it cannot say "ineligible *here*, eligible *there*". |
| applicability evidence unavailable → eligibility unsupported | **No** | Collapses into either `undefined` (ineligible) or `unknown`/undeclared (missing) — precisely the coercion §15.4 prohibits. The undeclared case (`UNDECLARED_ABSENCE`, `planner.py:667-670`) *looks* like the third state but means "author declared no rule". |
| carrier SQL NULL → no semantic judgment | **No** | Every fill disposition is triggered by `null_count()` on the aligned frame (`planner.py:639`) — i.e. the semantic judgment **is** read off the carrier representation, exactly what §11 forbids. |
| numeric parse failure → realization failure, not missing | **No** | No conversion-failure channel on the value path. A cast/parse failure produces a null and enters the same Φ dispatch, so it collapses into `unknown_absence`/`undeclared_absence`. (`type_error`, `disclosure.py:438`, is a *request* typecheck, not a per-cell conversion outcome.) |
| 100 known events, 99 supported → denominator stays 100 | **No** | Denominator is always the observed row count (`engine.py:357` group-by, `engine.py:873`). The 100/99 distinction has no carrier. The only nearby artifact is the `COVERAGE` caveat for crossings (`engine.py:718-722`), which reports *bridge* non-coverage, not lost events. |
| one known event has unknown day → daily frame cannot claim complete support | **No** | The frame carries no completeness claim to defect. Frame-level population caveats were **retired** (`planner.py:672-674`: "the old multi-universe `coverage` caveat is RETIRED"). §13's "support defect upstream of any displayed cell" has no representation whatsoever. |
| existence unsupported → do not create N missing flags | **Vacuously satisfied** | The system creates no flags, but only because it creates no point. Right output, wrong reason. |
| `mean(revenue)` with several identity-bearing inner anchors → Clarify | **Yes** | `input_anchor_ambiguous` (CLARIFY/AMBIGUOUS/ANALYTICAL) `disclosure.py:241`, raised `planner.py:1796-1810`; served-with-assumption path is `UNCONFIRMED` → wire `input_anchor` (`planner.py:2730`, `disclosure_wire.py:125`). Correctly *not* missing data. |
| `E @ A` where A is not a governed anchor | **Yes** | `out_of_universe` REFUSE/UNSUPPORTED/ANALYTICAL (`disclosure.py:404`; `planner.py:404-408`, `495-499`), message literally "out of domain — undefined, not missing". Distinct from `uncertified_edge` (`planner.py:485-494`). No placement or missingness is evaluated. This is the one case §2.1 requires that is cleanly implemented. |
| coordinate tuple nameable but no root point occupies it | **No — and it is violated** | `engine.py:552-553`, `612-613`, `738-740` do `domain = bridge.select(_to).unique()` then `domain.join(..., how="left")` — the crossing **manufactures an anchor point from every bridge category**, then hands it to Φ, which under `FILL zero` fills 0 (`engine.py:742-746`). That is exactly "a coordinate tuple treated as proof that an analytical point exists" (§4.3). |

#### 2. Absence vocabulary actually in the code

**Fill rules (authoring, `parser.py:51-53`)** — `FILL_RULES = frozenset({"zero", "unknown", "undefined"})`, plus `None` = undeclared. Stored on `MeasureColumn.fill_rule` (`model.py:180-185`), projected to the planner as `MeasureShape.fill_rule` (`projection.py:51-52`), resolved per column at `planner.py:2292-2299` (**conflict between atoms silently degrades to `None`/undeclared**).

**Caveat categories (engine vocabulary, `disclosure.py:31-67`)** — `APPROXIMATION`(31), `FRESHNESS`(32), `COVERAGE`(33), `UNCONFIRMED`(34), `TRANSPORT`(35), `B_ANCHOR_CROSSING`(36, tombstoned producer), `DATA_GAP`(47), `ZERO_FILL`(48, **retired producer**), `DECLARED_FILL`(53), `UNKNOWN_ABSENCE`(55), `OUT_OF_POPULATION`(57), `UNDECLARED_ABSENCE`(59), `OVER_COUNT`(60), `SHADOW`(63), `RECONCILIATION`(66).

**Wire codes (`disclosure_wire.py:107-128`)** — `incomplete_data`, `zero_filled`(retired), `filled`, `unknown`, `out_of_population`, `undeclared_absence`, `multi_counted`, `memberships_unrepresented`, `reconciliation`, `denominator_population`, `input_anchor`, plus materiality `material|immaterial` (`disclosure_wire.py:93-94`). Reserved-unwired: `incomplete_data`, `conflicting_data`, `other` (`disclosure_wire.py:151-154`).

**Basis (`parser.py:50`)** — `BASIS_TYPES = {"events","spine","product","registry"}`; `describe.py:57-62` `_ABSENCE` still maps `events → "absence is a lawful ZERO (zero-fill; immaterial)"` and `spine → "absence is a GAP"`. **This is stale**: serving no longer keys absence on basis (`model.py:50-53`, `planner.py:626-628`), so `describe` publishes an absence doctrine the engine does not implement.

**Missingness structure (`model.py:187,197-200`, `parser.py:486-488`)** — `MCAR | MAR | MNAR` from `m_anchor`. Read only at `engine.py:1221` (lint) and `engine.py:1233-1235` (MNAR → `UNCONFIRMED` caveat).

**Refusal reasons touching absence (`disclosure.py:230-441`)** — `out_of_universe`, `uncertified_edge`, `contradicted_edge`, `uncertified_face`, `input_anchor_unavailable`, `input_anchor_ambiguous`, `pin_coarser_than_output`, `blocked_reduction`, `chained_crossing`, `anchor_spent`, `unsupported`, `type_error`, `unknown`; jurisdictions `LANGUAGE|ANALYTICAL|REALIZATION|UNRULED` (`disclosure.py:101-113`).

**Not present anywhere**: `no_data`, `absent` as an enum, `missing` as an enum, coverage `Any`/`Complete` modes (grep for `coverage_mode`/`CoverageMode`/`COMPLETE` returns nothing but unrelated prose), any `exists`/`placed`/`supported` predicate.

#### 3. Does anything conflate "eligible but unsupported" with "carrier NULL"?

**Yes, structurally — it is the sole mechanism.**

- `planner.py:639` `n_absent = data[c.name].null_count()` — the count of Polars nulls **is** the count of unsupported points. `planner.py:642-670` then dispatches the entire semantic vocabulary (`DECLARED_FILL` / `UNKNOWN_ABSENCE` / `OUT_OF_POPULATION` / `UNDECLARED_ABSENCE`) off that number.
- `planner.py:2837-2838` does the same for expressions: `l_absent = pl.col(_V).is_null() & pl.col(f"{_V}_r").is_null().not_()`, feeding `_divergence_caveats` (`planner.py:2793-2809`), whose `_DIVERGENCE` table (`planner.py:2781-2787`) maps carrier-null-origin directly to "the point is INELIGIBLE" vs "ELIGIBLE there but not observed".
- `engine.py:743` `touched.with_columns(pl.col("_value").fill_null(0))` — a carrier null becomes a supported zero.
- The reverse conflation also holds and is worse: a **carrier row present with a NULL measure value** never reaches Φ at all, because `sum()`/`count(*)` in `connector.py:265-266` absorb it in the backend. So "eligible but unsupported at an existing point" silently becomes **supported zero** (for `sum`) or **supported N** (for `count(*)`), with no caveat of any kind. `engine.py:337-342` is the only place carrier nulls are treated as meaningful, and only to make `last`/`first` land on a real observation.

The code is aware of one narrow version of this and refuses to guess (`planner.py:643-654`: a `zero`-declared column carrying a `DATA_GAP` is not filled, because "the two null-origins are not distinguishable per cell at this point"). That comment is the accurate general statement of the architecture.

#### 4. Is BASIS load-bearing at runtime?

**Almost entirely declarative.** `model.py:50-53` states it directly: "As of columna#143 step 3 basis NO LONGER [drives absence semantics] … Absence now follows the per-member fill rule Φ_v." `adjudication.py:595-615` `_prove_basis` mints a `basis_license`, and the comment says "serving follows the DECLARATION, not this license" (`adjudication.py:596-597`); `model.py:56-57` repeats it. `ZERO_FILL` is a retired producer (`disclosure.py:48-50`).

Two residual runtime uses:
- **`crossing_basis_not_events`** (`disclosure.py:323-334`), raised at `engine.py:~455-461`: crossing a non-events basis refuses because replication would corrupt grid completeness. Genuinely load-bearing.
- **`_prove_derived_driver`** (`adjudication.py:664-670`): a face driver must be on a `spine` universe. Adjudication-time, load-bearing.

Everything else — `describe.py:65-83` absence semantics, `documents.py:169`, `projection.py:79` — is describe/trust surface. And `describe.py:57-62` still advertises the retired basis→absence mapping.

#### 5. Is "point exists but its placement under anchor A is unsupported" representable?

**No. Plainly: there is no such representation, at any layer.**

- No field on `Universe`, `MeasureColumn`, `FamilyMember`, `ShapeEdge`, `UniverseShape`, `MeasureShape` (`model.py:44-58`, `170-200`; `projection.py:44-121`).
- No `Caveat` category (`disclosure.py:31-67`) and no wire code (`disclosure_wire.py:107-154`).
- No refusal reason (`disclosure.py:230-441`). The nearest reasons are all *geometry* claims — "A is not reachable / not certified / not addressable" — asserted about the **anchor**, never about **a point's evidence for its placement under that anchor**.
- Structurally, placement is realized as the SQL group-by key (`connector.py:270`) and is therefore **total by construction**: every delivered row has a value in every key column, and a NULL key becomes a NULL-named anchor point rather than an unplaced point.

The distinction the amendment calls anchor-placement standing therefore collapses, in the current system, into one of exactly two outcomes depending on the carrier: **the row disappears entirely** (indistinguishable from point nonexistence and from unsupported existence), **or the point is placed at a fabricated NULL coordinate** and reported as ordinary supported data.


---

## 3.2 Capability authority — schema, generators, Core/Platform profile coupling

*Inspector `agent-a829c7916f75e050a` · primary target doc: `frameql_vnext_capability_profile_reconciliation_plan_v0_1.md`*

### Capability authority — reconnaissance report

Repo `columna` @ `17e3b6b`. All paths absolute below.

---

#### 1. Schema of a `[[capability]]` entry

Declared prose schema: `/data/repos/978ea3c9feee4ad79341d42517782efd/columna/specs/frameql_capabilities.toml:17-26` (the "WHAT BELONGS HERE" block). There is **no schema validator** — no JSON-schema, no enum check, no field-presence check anywhere. Requiredness is whatever a consumer's `[]` access happens to raise on.

| field | type | actually required by | evidence |
|---|---|---|---|
| `id` | str | **hard** — `KeyError`/duplicate check | `docs/tools/capability_authority.py:50-52` (`raise SystemExit` on duplicate id) |
| `spellings` | list[str] | optional; defaults to `[id]` | `docs/tools/capability_authority.py:59`, `docs/tools/regen_capability_tables.py:85` (`c.get("spellings", [cid])`) |
| `position` | `"series"｜"predicate"` | **hard in the table generator** (`c["position"]`), soft in the authority tool (`.get`) | `docs/tools/regen_capability_tables.py:73,75` vs `docs/tools/capability_authority.py:116` |
| `category` | `"reducer"｜"scan"｜"map"` | **hard in the table generator only** (`c["category"]`) | `docs/tools/regen_capability_tables.py:71` |
| `standing` | `"ratified"｜"proposed"｜"retired"` | **hard** (`c["standing"]` in both) | `docs/tools/regen_capability_tables.py:101`, `docs/tools/capability_authority.py:208` |
| `re_entry_certified` | bool | **read by nothing** (see §4) | present only on reducer rows, `specs/frameql_capabilities.toml:77,87,97,107,117,127,137,147,157,167` |
| `source` | str | read by nothing | e.g. `specs/frameql_capabilities.toml:78` |
| `note` | str | read by nothing | e.g. `specs/frameql_capabilities.toml:79` |
| `schema_version = 1` | int, file-level | **read by nothing** — grep across repo returns only the declaration | `specs/frameql_capabilities.toml:67` |

Enum values are enforced only by **omission**: `_by_category` (`docs/tools/regen_capability_tables.py:69-77`) plus the hardcoded `_SECTIONS` (`:80-81`) mean a row with any `category` outside `{reducer, scan, map}`, or any `position` outside `{series, predicate}`, is **silently dropped from all four generated tables with no error**. The only table that would still show it is the "Realization ahead of canonical standing" grid (`:142-149`), which iterates `standing_exceeded` over all caps regardless of category.

86 capabilities, 22 ratified (measured live: `python docs/tools/capability_authority.py`).

---

#### 2. What depends on `category = reducer | scan | map`

**(c) Parser/planner/engine ROUTING: nothing. No runtime module reads this file at all.**

Exhaustive consumer set of `specs/frameql_capabilities.toml` (grep for the filename + every public function of `capability_authority`, whole tree minus `.git`):

```
docs/tools/capability_authority.py
docs/tools/regen_capability_tables.py
docs/tools/check_manual_frameql.py
scripts/gates.toml
specs/profiles/{core,platform}_profile.toml   (by reference)
docs/{README,frame_ql_language,core_profile,platform_profile,frame_ql_build_status,columna_reference_manual_5e}.md
specs/open_forks.md
```

Nothing under `packages/`, `apps/`, `services/`, `scripts/` imports it or `capability_authority`. **No test anywhere reads it.**

**(a) Generated documentation only — the sole consumer of `category`:**
- `docs/tools/regen_capability_tables.py:69-77` `_by_category`, `:80-81` `_SECTIONS`, used at `:100-102` (canonical), `:108-111` (core contract), `:131-141` (build status). That is 100% of `category`'s reach.
- `docs/tools/capability_authority.py` **never reads `category`** (confirmed by grep).

**(b) Validation: none keyed on `category`.** The two gates validate id-uniqueness (`capability_authority.py:50-51`), profile→canonical id membership (`:90-95`), and platform-extends-core level monotonicity (`:182-186`). None inspects `category`.

**Real routing is a second, independent classification in the runtime** — `Operator.kind`, unrelated to and never cross-checked against the TOML:
- definition `packages/columna-core/src/columna_core/operators.py:40` (`REDUCER, SCAN, MAP = "reducer","scan","map"`), `:50` (`kind` field), registry `:122-198`
- routing doc `packages/columna-core/src/columna_core/operators.py:6-13`
- planner SCAN gate `packages/columna-core/src/columna_core/planner.py:1830-1834` (`if sig.kind != "scan": raise`)
- planner MAP gate `packages/columna-core/src/columna_core/planner.py:2447-2448` (`if sig is None or sig.kind != "map"`)
- planner REDUCER/monoid gate `packages/columna-core/src/columna_core/planner.py:2038`
- parser family-founding gate `packages/columna-core/src/columna_core/parser.py:680-690` — **only `kind == REDUCER` may found a measure family**
- engine scan dispatch on `scan_impl`, not kind: `packages/columna-core/src/columna_core/engine.py:301`
- mirror of `kind` into the planner-facing projection: `packages/columna-core/src/columna_core/projection.py:62,172`

So `category` in the TOML and `kind` in `operators.py` are two authorities that currently agree by hand, with **no gate comparing them**.

---

#### 3. What depends on `position = series | predicate`

Two call sites, both in `docs/tools/`:

1. **Documentation grouping** — `docs/tools/regen_capability_tables.py:73-75` (splits maps into "Maps — series position" / "Predicate position", and excludes predicates from the un-positioned sections).
2. **Build measurement path selection** — `docs/tools/capability_authority.py:116-119`: `position == "predicate"` routes measurement to the planner's comparison table `Planner._CMP` (`packages/columna-core/src/columna_core/planner.py:687`) plus a hardcoded `"and"`; everything else is measured against `columna_core.operators.REGISTRY`. Docstring explicitly disclaims this as semantic authority (`capability_authority.py:100-105`).

The parser/grammar does **not** consult `position`; predicate-vs-series admissibility is grammar structure in `parser.py`/`planner.py` with no link to the TOML.

---

#### 4. What depends on `re_entry_certified`

**Nothing. No evidence of any reader.** Grep over `*.py`/`*.toml`/`*.md` returns only the declaration lines and its two comment blocks in the authority file itself (`specs/frameql_capabilities.toml:26,45-48,77-167`). It is not rendered by `regen_capability_tables.py` (no table column emits it) and not read by `capability_authority.py`.

The runtime has a **parallel, unlinked** declaration of the same fact:
- `packages/columna-core/src/columna_core/operators.py:67` `re_entrant: bool`, prose `:70-110`, set `re_entrant=True` on `sum` only at `:124`
- mirrored `packages/columna-core/src/columna_core/projection.py:71,174`
- consumed for real by the planner: `packages/columna-core/src/columna_core/planner.py:1514-1551` (`_re_entrant`), used at `:1567`
- tested: `packages/columna-core/tests/test_pin_admissibility.py:270-271`

So `re_entry_certified` (spec) and `re_entrant` (build) encode the same claim in two places with **no gate keeping them in step** — a live instance of the P0-17 class the file was written to close.

---

#### 5. Profiles: re-declare or reference?

**Reference by capability ID only.** No profile carries `category`, `position`, `standing`, or any semantic field.

- `specs/profiles/core_profile.toml:40-143` — 30 rows of `[[realizes]] capability = "<id>" / level = "execute"|"plan"` plus optional `note`. Levels enumerated at `:31-33`.
- Enforced: a profile may not name a non-canonical id — `docs/tools/capability_authority.py:90-95` (`profile_errors`).
- The comment headers grouping rows as "reducers"/"scans"/"predicate position" (`core_profile.toml:39,72,89,112`) are **comments only**, invisible to every consumer.

**`Platform extends Core; adds = []` is literally true in the file:** `specs/profiles/platform_profile.toml:30` `extends = "core"`, `:33` `adds = []`. Verified live: `platform profile: extends core, 0 addition(s) over it`. Inheritance semantics: `docs/tools/capability_authority.py:66-81`; the "extension must not drop the base" check: `:182-186`. Generated projection renders `_(none)_`: `docs/platform_profile.md:24-33`.

---

#### 6. IDs for `first`/`last`, the scans, the maps — and string coupling

- `first` `specs/frameql_capabilities.toml:152`, `last` `:142` — both `category = "reducer"`, `standing = "ratified"`, `re_entry_certified = false`.
- Scans (16, all `category = "scan"`, all `standing = "proposed"`), `specs/frameql_capabilities.toml:649-781`: `cumsum, cumprod, cummin, cummax, rolling_sum, rolling_mean, rolling_min, rolling_max, rolling_count, lag, lead, rank, dense_rank, row_number, pct_change, ewm_mean`.
- Maps: series-position ids `specs/frameql_capabilities.toml:270-542` (`add, subtract, multiply, divide, negate, modulo, if, case, is_null, is_missing, coalesce, log, exp, sqrt, abs, sign, ceil, floor, round, concat, substring, lower, upper, trim, length, year, month, day, week, quarter, date_diff, date_add, is_type, cast`); predicate-position ids `:550-640` (`eq, ne, lt, le, gt, ge, conjunction, disjunction, negation, between, membership`); allocation-bridge maps `:785-819` (`equal_split, weighted, proportional_to, custom`).

**ID string coupling:**
- IDs are referenced by string **only** in `specs/profiles/*.toml` (`capability = "..."`). A rename there without the profile is caught loudly by `capability_authority.py:90-95` — not silent.
- IDs also surface as literal text in two generated tables (`regen_capability_tables.py:115,149` print `cid`), so a rename changes committed docs and trips the `capability-tables --check` drift gate.
- **`spellings` are the real fragile coupling**, not ids: `measure_build` matches spelling strings against `columna_core.operators.REGISTRY` keys (`capability_authority.py:113-136`) and `check_manual_frameql.py:272-273,318` resolves Manual table cells through `spelling_index`. Renaming a spelling silently changes measurement (row drops to `none` → reported as `lag`, not as an error).
- Note the asymmetry already present: TOML id `approx_distinct` with `spellings = ["approx_distinct","distinct"]` (`:162-163`) vs registry key `distinct` (`operators.py:157`), reconciled only because `measure_build` iterates all spellings.
- No `packages/` code or test references any TOML capability id as a spec id; runtime strings (`"first"`, `"cumsum"`) are registry keys (`operators.py:166,168,190`, `compiler/compile.py:62,64`) that coincide with ids.

---

#### 7. Hand-editable vs regenerated; what enforces "measured, not hand-authored"

Fully regenerated, block-scoped. Four target documents, one block each: `docs/tools/regen_capability_tables.py:48-53` → `docs/frame_ql_language.md:1573-…`, `docs/core_profile.md:38-…`, `docs/platform_profile.md:24-…`, `docs/frame_ql_build_status.md:79-…`, delimited by `<!-- BEGIN/END GENERATED: capability-reference -->` (`:34-35`) and stamped do-not-edit (`:57-58`).

Enforcement stack:
1. `scripts/gates.toml:140-143` gate `capability-authority` → `python docs/tools/capability_authority.py`; `:146-149` gate `capability-tables` → `regen_capability_tables.py --check`. Both `workflow = "docs.yml"`, `local = true`.
2. CI executes *through* the runner: `.github/workflows/docs.yml:52-62` (`python scripts/gates.py --gate capability-authority` / `--gate capability-tables`), and `scripts/gates.py:55,237` + `.github/workflows/ci.yml:260` make it a meta-gate failure for a workflow to invoke a gate script directly.
3. `--check` regenerates in memory and fails on any byte difference: `regen_capability_tables.py:159-171,191-194`.
4. **Orphan guard** — a `.md` carrying the markers but not in `TARGETS` fails: `regen_capability_tables.py:174-184`.
5. "Measured" for the build column means importing the installed package: `capability_authority.py:107-110`, and structurally only (registry membership + `in_core` + `SERIES_REDUCERS`), never a value probe — `capability_authority.py:24-27,123-134`.
6. Prose scope guard — a hand-maintained vocabulary table reappearing outside the generated block in Manual Appendix A is a gate failure: `docs/tools/check_manual_frameql.py:250-327` (reason string `hand-maintained-vocabulary-table`, and `operator-not-a-canonical-capability`).

**Hazard (verified, not inferred):** `measure_build` swallows `ImportError` and returns `{}` (`capability_authority.py:109-110`). In this checkout `columna_core` is not importable, so the gate reports every capability as `build=none` / 30 `lag` and `regen … --check` would rewrite `frame_ql_build_status.md` to an all-`—` table. The committed table says "Measured from the installed `columna-core` **0.19.0**" (`docs/frame_ql_build_status.md:79`, matching `packages/columna-core/pyproject.toml:9`), i.e. the "measured" property is only as good as the environment the gate runs in, and degrades silently rather than failing.

---

#### 8. Can semantic classification be split from realization routing without a second authority?

**Structurally easy; the only real coupling is presentational.** Evidence:

- Routing never reads the spec. Dispatch reads `Operator.kind` (`operators.py:50`) → `OperatorSig.kind` (`projection.py:62,172`) → `planner.py:1830,2038,2448` / `parser.py:688`. Zero import path from `specs/frameql_capabilities.toml` into `packages/`. Adding `semantic_class` to the TOML therefore cannot create a second routing authority, because the TOML is not a routing authority today.
- The one place `category` is load-bearing: `docs/tools/regen_capability_tables.py:69-81`. `_SECTIONS` is a hardcoded 4-tuple list keyed on the three implementation-shaped values; `_by_category` filters by equality and drops non-matching rows silently. A `semantic_class` axis needs `_SECTIONS` restructured (or a second section list) or new-class rows vanish from `frame_ql_language.md`, `core_profile.md` and `frame_ql_build_status.md` with a green gate.
- Second coupling, smaller: `position == "predicate"` selects the measurement path in `capability_authority.py:116`. If `position` stays the surface-placement axis (as the plan proposes, `/tmp/m2recon/frameql_vnext_capability_profile_reconciliation_plan_v0_1.md:142-150`), this site is untouched.
- Third coupling, latent and the one that actually bites: reclassifying `first`/`last` to `ordered_expression` in the spec would leave `operators.py:166,168` at `kind=REDUCER`, which is what licenses them to found measure families (`parser.py:680-690`) and to be reduced/pinned as reducers. Spec and runtime would then disagree in substance with **no gate detecting it** — the same undetected divergence already present for `re_entry_certified` vs `re_entrant` (§4).
- Profiles are already class-agnostic (§5), so a semantic reclassification cannot perturb Core/Platform promises: `core_profile.toml` names ids only, and `capability_authority.profile()` is a pure id→level map.

One-sentence read: the split is cheap because routing and spec are already disjoint, and the work is (i) generalizing `_SECTIONS`/`_by_category` and (ii) deciding whether to add the first-ever spec↔runtime cross-check rather than leaving `category`/`kind` and `re_entry_certified`/`re_entrant` as parallel unlinked claims.


---

## 3.3 Parser & expression grammar

*Inspector `agent-a4fc8ae2573f454a4` · primary target doc: `frameql_vnext_language_vnext_working_draft_v0_3.md`*

### Frame-QL parser & expression grammar — reconnaissance report

#### 0. The layer map (this is the load-bearing fact)

There is **no dedicated expression parser and no lexer/grammar module**. The expression grammar is *hosted on CPython's `ast`*. Three separate parsers exist, at three layers:

| Layer | File | What it owns |
|---|---|---|
| Manifold definition language (`.cml`) | `packages/columna-core/src/columna_core/parser.py` (761 lines) | `MANIFOLD/UNIVERSE/LEVEL/MEASURE/DERIVED/HIERARCHY/RELATE` — pure regex, statement-oriented. **Not** the query surface. |
| Query envelope | `.../envelope.py` (386 lines) | Clause structure only: `[EXPLAIN][FROM][WITH] SELECT … AT {…} [WHERE][HAVING][ORDER BY][LIMIT]`. Series expression text is captured **verbatim** (`envelope.py:50-56`) and never inspected. |
| Expression | `.../planner.py` — `_parse_expr` (`planner.py:43-58`) + `_ALLOWED` (`planner.py:61-66`) + `_infer` (`:2342`) / `_node` (`:2462`) | `ast.parse(src, mode="eval")`, then an allow-list walk, then two hand-written AST dispatchers. |

Retired fragment parser `parse_frameql` (`frameql.py:202-250`) is a dated tombstone, called by no shipped surface (`frameql.py:206-211`).

The substrate boundary (`planner.py:26-58`, "P1-26") converts CPython `SyntaxError` → `FrameQLSyntaxError`. It explicitly disclaims naming semantics (`planner.py:37-41`).

`_ALLOWED` is the *entire* expression grammar:
```
Expression, BinOp, UnaryOp, Name, Attribute, Load, Constant,
Add, Sub, Mult, Div, USub, MatMult, Tuple, Call, keyword     # planner.py:61-66
```
Anything else → `Refusal("unknown", "illegal expression construct: <Node>")`, raised at three separate copies of the same walk: `planner.py:579-581` (run), `:1301-1303` (`_eval`), `:2317-2319` (plan).

---

#### 1. Per-form trace

##### `revenue.sum`, `level.last` — dotted family/member
- **(a) ACCEPTED.** `ast.Attribute(value=Name, attr=str)`. Recognized at `planner.py:1322-1329` (`_measure_ref`): *"Name('revenue') -> (revenue, default-member). Attribute(level, 'sum') -> (level, sum)."*
- **(c) Does NOT normalize away.** Since WP-NAME-1 the canonical column key *is* the dotted text: `planner.py:776-777` returns `f"{body.value.id}.{body.attr}"` — *"member access: verbatim dotted, no mangle"*.
- **(d) SEMANTICS IN THE PARSER SHAPE — yes, decisively.** `_measure_ref` requires `isinstance(node.value, ast.Name)`, i.e. **exactly one dot level**. `revenue.a.b` returns `(None, None)` and dies at `planner.py:2460` `unsupported expression node Attribute`. The shape `Attribute(Name, attr)` *is* the "measure . family-member" judgement; nothing downstream re-decides it.
- Member resolution then runs against the measure's declared `family` dict (`planner.py:2418-2432` in `_infer`, mirrored `:2551-2578` in `_node`), with alias canonicalization (`_resolve_member`, `planner.py:1307-1321`; `operators.ALIASES` `operators.py:~230`).
- `last`/`first` are ordinary `REDUCER`s in the same registry as `sum` (`operators.py`: `"last": Operator("last", REDUCER, ORDERED_W, …, needs_order=True)`, `"first": … combine="argmin", needs_order=True`). **The `revenue.sum` vs `level.last` distinction the target doc §7.4 insists on ("family-forming law" vs "ordered analytics") does not exist anywhere in the grammar or the dispatch** — both are `Attribute(Name, attr)` → family-member lookup. The only trace of the difference is the `needs_order`/`ORDERED_W` flags and the optional `ORDER <level>` clause in the `.cml` FAMILY block (`parser.py:475-484`).

##### `E.member` / `E.method(...)` generally
- `E.member` where `E` is not a Name: **rejected** at `_infer`/`_node` fallthrough (`planner.py:2460`, `:2603`) — `unsupported expression node Attribute`. Grammar-legal (`ast.Attribute` in `_ALLOWED`), planner-refused. **(b)**
- `E.method(...)`: `ast.Call` with `func=ast.Attribute`. Both call recognizers hard-require `func` to be a `Name`: `_reduction_call` `planner.py:1361`, `_scan_call` `planner.py:1817`. So it falls through to `unsupported expression node Call` (`planner.py:2460`/`:2603`). **(b) — grammar-recognized, planner-refused, with a generic message.** There is no value-layer method dispatch anywhere in the tree.

##### `E[key]` / `E[predicate]` — brackets
- `ast.Subscript` is **absent from `_ALLOWED`**. Verified AST shapes:
  - `revenue[region]` → `Subscript` → `Refusal("unknown", "illegal expression construct: Subscript")` → **ERROR** mood (`disclosure.py:439`).
  - `revenue[region == "east"]` → `Subscript`+`Compare`+`Eq` → same refusal.
  - `revenue[region = "east"]` (the documented roadmap spelling, `docs/frame_ql_language.md:215,545,1137`) → **CPython `SyntaxError`** → converted to `FrameQLSyntaxError` by `planner.py:43-52`.
- **Brackets ARE tracked by every bracket-counting scanner** — `envelope.py:120-131` (`_check_balance`), `:133-144` (`_split_top`), `:147-164`, `:173-195`; `frameql.py:168-199`; `parser.py:357-368` (`_split_top_at`). They are depth-neutral separators only. **This is dead scaffolding for `[]`-as-anything**: no production consumes a bracket, no AST node for it is admitted.
- **Only textual scaffolding**: `planner.py:757` (`_default_name` docstring: "A composite/nested/map/**bracket** expression is still REFUSED for a name") and the P1-26 comment `planner.py:31`. No code path.

> **Finding (divergence, SV — read at file:line, not executed; duckdb absent so I could not run the planner).** `revenue[region = "east"]` produces **two different errors depending on whether you wrote `AS`**:
> - **No alias** → `desugar` calls `_default_name` (`planner.py:820`) → `_parse_expr` (`:761`) → `FrameQLSyntaxError` escapes `run_statement` → server maps it to wire reason `frameql_syntax` (`columna-server/src/columna_server/tools.py:357,387,409`).
> - **With `AS x`** → `_default_name` is skipped (`planner.py:820`), the text reaches `run()`'s `_parse_expr` at `planner.py:578`, **inside the try**. `FrameQLSyntaxError` is a `ValueError`, not a `Refusal`, so it is swallowed by the catch-all backstop at `planner.py:597-604` and reported as
> `Refusal("unsupported", "this frame could not be resolved in the engine (FrameQLSyntaxError); the ask is not supported in this build.")` — a **realization/capability** verdict for a **language** failure. The P1-26 message ("See Chapter 2 … §2.8") never reaches the reader on that path.
> `docs/frame_ql_revision_history.md:59-62` asserts the bracket filter "is accepted by the statement grammar and refused at planning" — that is true only for the `==` spelling, not the `=` spelling the same sentence quotes.

##### `sum(E @ A)` — inline reduction with inner anchor
- **(a) ACCEPTED, and it is the most developed form in the grammar.** `_reduction_call` (`planner.py:1354-1379`): `Call(Name(R), [BinOp(left, MatMult, right)])` where `R` resolves through `_inline_reducer` (`:1339-1343`) → `canonical_op` ∩ `SERIES_REDUCERS` = `{sum, mean, min, max, count}` (`operators.py` `SERIES_REDUCERS`).
- **(c) Normalizes heavily before the AST is built.** The canonical surface `@ {a*b}` **cannot be parsed by the substrate** (Python would read `{a*b}` as a set literal), so it is *textually rewritten* first:
  - `_convert_input_anchor` (`planner.py:716-743`): `@ {x}` → `@ x`; `@ {a*b}` → `@ (a, b)`; `@ {}` → `@ ()`.
  - `_canon_expr` (`planner.py:781-791`) does the reverse for display.
  - `_engine_columns` (`planner.py:1244-1248`) calls this the "AST-substrate adapter".
  - Consequence, pinned by test: the **builder API cannot express the canonical pin** — `frame(...).column("c", "avg(revenue @ {order})")` yields `illegal expression construct` (`packages/columna-core/tests/test_afternoon_page_gate.py:94-102`).
- **(d) SEMANTICS IN THE SHAPE — yes.** Whether `@` means *constitutive inner anchor of a reduction* or *map-operand grain declaration* is decided purely by whether the `MatMult` sits directly under a reducer `Call`: `_reduction_call` `planner.py:1370-1378` vs the map-operand branch `_infer` `planner.py:2371-2375` / `_node` `planner.py:2488-2506`. Same operator, two branches, positional discrimination.
- Unpinned `sum(E)` → `_unpinned_disposition` (`planner.py:1571`) → clarify/refuse/default.

##### Multi-input functions (`covariance(x, y)`) — 2+ args
- **(a) Parses** (`ast.Call` is allowed); **(b) refused at planning, in three different ways depending on the callee name:**
  - Name is a series reducer → `planner.py:1366-1369`: `"inline reduction 'sum' takes exactly one column argument"`. Note this **also rejects all keywords** (`if len(node.args) != 1 or node.keywords`).
  - Name is a registered scan → `planner.py:1836`: `"scan 'lag' takes one input expression and keyword params (n=, by=)"`.
  - Name is a registered non-scan (e.g. `median`, `last`) → `planner.py:1832-1834`: `"'last' is a reducer, not a scan, and cannot be called here"`.
  - **Name is unregistered (`covariance`)** → `planner.py:1826-1830`: `"there is no operator named 'covariance' in the registry — Frame-QL's vocabulary is the installed operator registry (Appendix A), and it is not extended by writing a call the substrate happens to parse"`.
- All are `Refusal("unknown")` → **ERROR** mood (`disclosure.py:439`). **Arity 1 is hard-wired at both call recognizers**; there is no n-ary function position in the language at all.

##### Tuple `(x, y)`
- **(a) Parses; in `_ALLOWED` (`planner.py:64-65`) — but only as a pin payload.** The comment is explicit: *"a COMPOSITE input anchor `@ {a*b}` desugars to `@ (a, b)`; a Tuple anywhere else is caught semantically by `_infer` ('unsupported node')"*.
- **(b)** A top-level `(x, y)` → `unsupported expression node Tuple` (`planner.py:2460`).
- Consumed only by `_pin_levels` (`planner.py:1380-1391`), which walks `right.elts` and demands every element be `Name` or `Attribute(Name, attr)` (`_level_name`, `planner.py:1345-1352`).
- **Explicitly ruled out as a joint-operand surface**: `planner.py:2484-2486` — *"DELIBERATELY NOT A JOINT-OPERAND SURFACE (ruled Huayin, 2026-08-31): `@ {a,b}` keeps its one meaning, composite analytical GRAIN. Nothing here introduces `(a,b) @ A` or enlarges reducer arity."*

##### `first` / `last`
- As a **bare name** → `Name('last')` → `_measure_ref` returns `('last', None)` → not in `derived` or `measures` → `Refusal("unknown", "unknown column 'last'")` (`planner.py:2396`).
- As a **member** `level.last` → serves; ordered reducer with `needs_order=True`, `witness=ORDERED_W`, `combine="argmax"` (`operators.py`), `re_entrant=False` (documented at `operators.py`: *"last, first NOT certified — the witness is (value, order_key), not the finalized value"*).
- As a **call** `last(E)` → `_inline_reducer` rejects it (not in `SERIES_REDUCERS`), then `_scan_call` → `planner.py:1832-1834` `"'last' is a reducer, not a scan, and cannot be called here"`. **The doc §3.6 form `last(x @ I; order = ...)` is unreachable in every spelling.**
- Declared order for a member: `ORDER <level>` in the `.cml` FAMILY block only (`parser.py:475-484` → `FamilyMember.order_by`).

##### Scan parameters / `by =` / named arguments
- `ast.keyword` is admitted (`planner.py:66`) **solely** for scans. `_scan_call` (`planner.py:1812-1875`):
  - `n=` must be an integer `Constant`, bool excluded (`planner.py:1846-1852`).
  - `by=` must be a **quoted string** `Constant` — a bare level name is refused with `"by= names the order axis as a quoted level, e.g. by=\"day\" — not a bare 'day'"` (`planner.py:1853-1859`).
  - `window=` is recognized-but-unimplemented: `Refusal("unsupported", …[ROADMAP])` (`planner.py:1860-1873`).
  - Anything else → `"unknown parameter '<x>' (accepts n=, by=, window=)"` (`planner.py:1874-1876`).
- `by=` **validation** is a separate, recently hardened law: `plan_order_axis` (`planner.py:293-365`) — *"Explicit `by=` may SELECT governed order standing. It may not CREATE it"* (P1-24). Not-a-level → `Refusal("unknown")` (ERROR/language); level with no governed order → `Refusal("order_not_governed")` (analytical).
- **Reducers accept no keywords at all** (`planner.py:1366`). `by =` in the doc's `first/last(…; order=…)` sense has no parse position.
- `reset=` / `step=` are documented roadmap only (`docs/frame_ql_revision_history.md:73-74`) — they hit the `unknown parameter` refusal.

##### `@` versus `AT`
- **Two entirely distinct constructs at two layers, sharing no code.**
  - `AT` is a **clause keyword**, whole-word, case-insensitive, matched at bracket depth 0 only: `envelope.py:39-40` (`_CLAUSE_ORDER`, `_SINGLE_KW`), `_clause_spans` `envelope.py:173-195`; body parsed by `_parse_anchor_braces` (`envelope.py:207-220`). It never reaches an AST. (Note `envelope.py:176`: *"A non-keyword word is skipped whole (so `at_risk_count` never trips `AT`)"*.)
  - `@` is **`ast.MatMult`**, admitted at `planner.py:63`, only ever inside series expression text which the envelope passes through verbatim (`envelope.py:17-21`).
  - A *third*, unrelated `AT` exists in the definition language: `_split_top_at` (`parser.py:357-374`) splits a `DERIVED` formula at a depth-0 ` AT ` for the resolution anchor. Its docstring names the interaction explicitly: *"a dotted family reference (`level.last`) and `AT day` compose unambiguously."*
  - The retired fragment parser used `@` for the **output** anchor (`frameql.py:223-233`); that is tombstoned (`frameql.py:206-211`).
- **Within `@` itself: one operator, two roles**, disambiguated positionally (see `sum(E @ A)` above). Both roles are pins/grain declarations, never output anchoring.

---

#### 2. Answers

##### 1. Where are dotted family/member assumptions baked into the *grammar*?
Not in a grammar file — in the AST shape tests, which are the grammar. Five sites:

1. **`planner.py:1322-1329` `_measure_ref`** — the definitional one. `Attribute(Name, attr)` ⇒ `(measure, member)`. One dot, no more.
2. **`planner.py:1345-1352` `_level_name`** — the *same* shape is also read as a dotted **level** name (`cal.month`) in pin position. The identical syntax means two different things by position.
3. **`planner.py:776-777` `_default_name`** — the dotted text is the canonical column key, verbatim.
4. **`planner.py:1667` and `planner.py:2133`** — the planner **synthesizes** `ast.Attribute(value=ast.Name(...), attr=member)` nodes to probe member lawfulness. Dotted family/member is the planner's *internal* representation of a measure atom, not merely a surface form. This is the strongest lock-in.
5. **`parser.py:664-676`** (definition language well-formedness) — the derived-formula closure check deliberately validates only the **dotted head**, with a comment stating the rule: *"a reference like `level.last` names the column `level` with a family-member selector `.last` — only the head is a column name, and member validity is the planner's job."*

Plus a **third, competing** dot semantics in the *anchor* namespace: `resolve_anchor` (`planner.py:507-556`) splits an anchor token at the first dot as `family.level`, then falls back to `coordinate.face` (`parse_faced`, `planner.py:544-548`). The `.cml` parser has a fail-closed check for the collision between literal dotted level names and the `family.level` split (`parser.py:745-755`). So `.` currently carries **four** meanings by position: measure.member, dotted-level-name, family.level anchor qualification, coordinate.face.

##### 2. Could `[]` be reassigned to value subscription without ambiguity? Is `E[predicate]` parsed?
- **Yes, cleanly.** `ast.Subscript` is currently reachable from the substrate but **rejected by allow-list only** (`planner.py:61-66`). No production in `envelope.py`, `parser.py`, or `planner.py` consumes a bracket for meaning; all bracket handling is depth counting (`envelope.py:120-144`, `frameql.py:168-199`, `parser.py:357-368`). Admitting `ast.Subscript` to `_ALLOWED` plus a `_node`/`_infer` branch introduces **zero** grammar conflicts.
- **Caveat:** `E[key = value]` cannot ever be parsed by the current substrate — CPython rejects `=` inside `[]`. Subscription by `E["key"]` / `E[0]` / `E[name]` is free; anything with a bare `=` inside brackets requires abandoning `ast.parse` or pre-lexing.
- **`E[predicate]` is not parsed and is not scaffolding — it is documentation-only.** It exists in `docs/frame_ql_language.md:215,545,1137` and `docs/columna_framework_manual_6{e,f,g}.md:~425-439`, and as two comments (`planner.py:31`, `:757`). There is no dead code path, no retired branch, nothing to delete.

##### 3. Does `(x, y)` conflict with another production?
**No conflict with grouping parens** — CPython folds `(x + y)` to the inner node; only a comma produces `ast.Tuple`. **No conflict with argument lists** — those are `Call.args`, a different node.

The **one occupancy** is: `ast.Tuple` is currently reserved as the *internal desugared spelling of a composite input anchor* (`planner.py:64-65`, produced by `_convert_input_anchor` `planner.py:716-743`, consumed by `_pin_levels` `planner.py:1380-1391`). It is only ever read in `BinOp(MatMult).right` position, so a Tuple in **operand** position is free — `_infer`/`_node` currently reject it generically at `planner.py:2460`/`:2603`.

Two textual hazards if tuples go live:
- `_canon_expr` (`planner.py:786-789`) does a **regex** rewrite `@\s*\(([^)]*)\)` → `@ {a*b*…}`. It is not paren-aware and would mangle `x @ (a + b)`-shaped text.
- `_convert_input_anchor` (`planner.py:716`) is also regex (`@\s*\{([^}]*)\}`), non-nesting.

##### 4. Is `@` one operator with two meanings, or two constructs?
**One operator (`ast.MatMult`) with two positionally-discriminated roles; `AT` is a wholly separate construct at a different layer.**
- Role A — constitutive inner anchor of a reduction: only when the `MatMult` is the sole argument of a reducer `Call` (`planner.py:1370-1378`).
- Role B — map-operand grain declaration: any other position (`planner.py:2371-2375` static, `planner.py:2488-2506` resolution). The comment at `planner.py:2478-2483` is explicit that this "selects nothing the context has not already fixed; it STATES it".
- Role B has a **third sub-meaning**: `@ {}` (empty pin) is the Manifold-wide scalar / broadcast (`planner.py:722-730`, `planner.py:2489-2505`).
- `AT` never reaches the expression parser (`envelope.py:39,173-195`). This matches target-doc §4.2's intent, but by *layer separation* rather than by a shared anchoring notion.

##### 5. What does each unsupported form produce today?

| Form | Failure | Mood |
|---|---|---|
| `E.method(...)` | `Refusal("unknown", "unsupported expression node Call")` — `planner.py:2460`/`:2603` | ERROR (language) — `disclosure.py:439` |
| `E1.E2.member` | `Refusal("unknown", "unsupported expression node Attribute")` — same lines | ERROR |
| `revenue[key]`, `revenue[a == b]` | `Refusal("unknown", "illegal expression construct: Subscript")` — `planner.py:581`/`:1303`/`:2319` | ERROR |
| `revenue[region = "east"]` | **Substrate `SyntaxError`** → `FrameQLSyntaxError` (`planner.py:43-52`). **Unaliased** → escapes as wire `frameql_syntax` (`tools.py:357,387,409`). **Aliased** → swallowed by the backstop at `planner.py:597-604` and mis-reported as `Refusal("unsupported", "…could not be resolved in the engine (FrameQLSyntaxError)…")` | frame ERROR / column ERROR-as-realization |
| `count(*)` | `SyntaxError` "Invalid star expression" → `FrameQLSyntaxError` (`planner.py:26-33` names this case explicitly) | ERROR |
| `covariance(x, y)` | `Refusal("unknown", "there is no operator named 'covariance' in the registry…")` — `planner.py:1826-1830` | ERROR |
| `sum(x, y)` | `Refusal("unknown", "inline reduction 'sum' takes exactly one column argument")` — `planner.py:1366-1369` | ERROR |
| `last(x)` | `Refusal("unknown", "'last' is a reducer, not a scan, and cannot be called here")` — `planner.py:1832-1834` | ERROR |
| `(x, y)` top-level | `Refusal("unknown", "unsupported expression node Tuple")` — `planner.py:2460` | ERROR |
| bare `last` / `first` | `Refusal("unknown", "unknown column 'last'")` — `planner.py:2396` | ERROR |
| `lag(x, reset="week")` | `Refusal("unknown", "scan 'lag': unknown parameter 'reset' (accepts n=, by=, window=)")` — `planner.py:1874-1876` | ERROR |
| `rolling_sum(x, window=3)` | `Refusal("unsupported", "…registered as contract but not implemented in this build [ROADMAP]")` — `planner.py:1866-1873` | ERROR (realization) — `disclosure.py:437` |
| `by="customer"` (ungoverned) | `Refusal("order_not_governed", …)` — `planner.py:337-350` | analytical refuse |
| unaliased unnameable expr | `FrameQLSyntaxError` via `_synerr` — `planner.py:762`, `:772`, `:778` | wire `frameql_syntax` |
| `avg(revenue @ {order})` via builder API (not the statement path) | `Refusal("unknown", "illegal expression construct: Set")` — `planner.py:581`; pinned by `tests/test_afternoon_page_gate.py:94-102` | ERROR |

**Pattern worth flagging to the parent:** *every* vNext expression sort that current Core does not implement collapses into the same bucket — `Refusal("unknown", …)`, mood ERROR, jurisdiction `language` (`disclosure.py:439`). There is no way today to say "this is a well-formed Frame-QL expression whose sort this build does not serve". The one exception (`unsupported`, `disclosure.py:437`) is stamped `REALIZATION`, and the bracket-with-`=` case above shows it already being applied to a language failure by accident.


---

## 3.4 Canonicalizer / desugaring layer

*Inspector `agent-a394b6d940c73257e` · primary target doc: `frameql_vnext_language_vnext_working_draft_v0_3.md`*

### Canonicalizer / Desugaring Layer — vNext Reconnaissance

Root: `/data/repos/978ea3c9feee4ad79341d42517782efd/columna` (main, 17e3b6b). All paths below are absolute-relative to that root; I write them in full on first mention per section.

---

#### 0. Where the layer is

The EXPLAIN path leads back to exactly one named transform:

- `.../packages/columna-server/src/columna_server/tools.py:371-386` — `explain_statement` wire tool
- `.../packages/columna-core/src/columna_core/frameql.py:74-110` — `ManifoldServer.explain_statement`; `frameql.py:86` `d = p.desugar(stmt)  # rider 1: the consumed artifact`; `frameql.py:109` `"desugared": d.render_canonical()`
- `.../packages/columna-core/src/columna_core/planner.py:793-838` — **`Planner.desugar`**, "THE desugaring transform … the exact artifact EXPLAIN emits (never a reconstruction)"
- `.../packages/columna-core/src/columna_core/envelope.py:90-117` — `Statement.render_canonical`

---

#### 1. What the canonical form concretely IS

**A shallow dataclass wrapper around verbatim expression TEXT — not an AST.**

`envelope.py:76-88`:
```python
@dataclass
class Statement:
    series: list        # [Series]  (>=1)
    anchor: tuple       # levels of AT {…}; () is the grand-total frame
    explain: bool = False
    from_manifold: Optional[str] = None
    bindings: list = field(default_factory=list)   # emptied by desugar
    where: list = field(default_factory=list)      # [str]
    having: list = field(default_factory=list)     # [str]
    order_by: list = field(default_factory=list)   # [OrderKey]
    limit: Optional[Limit] = None
```
`envelope.py:49-57`:
```python
@dataclass
class Series:
    expr: str            # verbatim expression text
    alias: Optional[str] = None
```
`envelope.py:66-73`: `OrderKey(column: str, descending: bool)`, `Limit(n: int, per: tuple)`.

The whole meaning-bearing payload of a series is **one string**. The CPython `ast` is derived on demand at plan time (`planner.py:44-63` `_parse_expr`, the sole substrate crossing) and discarded; it is never the canonical artifact. `planner.py:1244-1248` `_engine_columns` even de-canonicalizes on the way to the engine (`@ {level}` → `@ level`) because "Python's ast can't hold a `{…}` set literal as an anchor".

Canonicalizations performed by `desugar` (`planner.py:793-838`): WITH inlined (`_apply_subs` `planner.py:693-699`, `_expand_total` `planner.py:840-860` proving substitution is a fixed point), input anchors braced (`_canon_expr` `planner.py:782-791`), series names resolved (`_default_name` `planner.py:744-780`), anchor resolved to declared levels (`resolve_anchor` `planner.py:508`). HAVING / ORDER BY are deliberately **not** expanded (`planner.py:822-836`).

---

#### 2. The eight assumptions, with file:line and vNext classification

##### (a) Reducer atom — **semantic data model change**
- `operators.py:8-13` — the three-kind routing table; `operators.py:40` `REDUCER, SCAN, MAP = "reducer","scan","map"`; `operators.py:50` `kind` is "the umbrella discriminant".
- `operators.py:167-170` — **`last` and `first` are registered as `REDUCER`** with `witness=ORDERED_W`, `combine="argmax"/"argmin"`, `needs_order=True`.
- `engine.py:96` "public: resolve one canonical atom"; `engine.py:228` the atom identity/cache key `key = (measure, member, target, uni, where)`; second copy `engine.py:669`.
- `planner.py:1878-1903` `_atoms` — an expression's meaning is a bag of `(measure, member)`; scans reduce to their underlying member (`planner.py:1889-1892`).
- `planner.py:1276-1278` → `frameql.py:96-101` — the EXPLAIN wire atom is `{"measure","member","universe"}` (+ server-enriched `license`).
- `projection.py:57-62` — the planner's view of an operator is `name/kind/accepts/out_rule` + order/window/core flags.

Why more than a rename: the atom identity **is** the memo key (`engine.py:228`) and it carries no order dimension. Two different completed order contracts over the same `(measure, member, target, uni, where)` collide today. `kind` is simultaneously the semantic category, the routing discriminant and the availability answer — the exact conflation O1 §13 forbids.

##### (b) Map expression — **rename/reclassification only**
- `operators.py:187-192` — `+ - * / neg` as `MAP`; `operators.py:181` `hll_estimate` as `MAP`.
- `operators.py:12-13` — MAP mechanics live planner-side; `planner.py:2811+` `_apply` is the pointwise evaluator.
- `planner.py:1410-1445` `_check_map_operand_pin` — map operands must be co-anchored (`co_anchor_required`), with the `@ {}` broadcast exemption at `planner.py:1418-1428`.
- Canonical form holds maps as raw infix text inside `Series.expr`; nothing structured. `planner.py:766-772` refuses to name a composite/map series (author must use `AS`).
- Bracket filter `revenue[region="east"]` is already not in the grammar (`planner.py:31-35`), agreeing with draft §10.4.

MAP → `pointwise` in the O1 §13 taxonomy is a label change; no behaviour or field moves.

##### (c) Scan — **new canonical field**
- `operators.py:185-201` — scan registry; `operators.py:63-65` `needs_order`, `needs_window`, `scan_impl`.
- `planner.py:1812-1877` `_scan_call` — the **entire** surface contract is `n=<int>`, `by="<level>"` (`planner.py:1856-1862`, quoted string only), `window=` (refused, `planner.py:1864-1873`). No direction, no tie rule, no peer/partition parameter.
- `planner.py:293-367` `plan_order_axis` (below).
- `engine.py:256-310` `scan`; **`engine.py:296` `partition = [d for d in target if d != order_axis]`** — the peer domain is mechanically derived from the output anchor, precisely what O1 §8 / draft §9.4 forbid ("not automatically the output frame").
- `engine.py:297` `frame.sort(partition + [order_axis])` — **ascending only; there is no descending scan anywhere.**
- `planner.py:995-1019` `_scan_order_standing` + `planner.py:1059-1065` — the plan-side pre-flight for scan order.

Peer domain, direction and tie behaviour do not exist as data anywhere. They must be added.

##### (d) Default reducer — **compatibility normalization**
- `planner.py:1322-1327` `_measure_ref` docstring: "`Name('revenue')` -> (revenue, **default-member**)".
- Guarded completions (clarify when |family| > 1): `planner.py:2415-2419`, `planner.py:2550-2553`, `planner.py:2524-2527`, `planner.py:2030-2033`, `planner.py:1545-1547`.
- **Unguarded** first-declared-member picks: `planner.py:1900` (`_atoms`), `engine.py:505`, `engine.py:1150`, `documents.py:80`.
- `engine.py:413` — the answer "moved when the DECLARATION ORDER of" the family changed; `disclosure.py:306` — "`next(iter(family))` was a realization".
- Canonical form never writes the completion back: `_default_name` (`planner.py:744-780`) returns the expression verbatim, so `SELECT revenue` canonicalizes to `revenue`, never to `revenue.sum`.

Draft §10.1 lists "governed default family completion" as a canonicalization case; the machinery exists but the completion is invisible in canonical form. **Live inconsistency to flag:** `_atoms` (`planner.py:1900`) silently defaults where `_infer`/`_node` Clarify, and `_atoms` feeds both the EXPLAIN wire atoms (`planner.py:1276`) and `_column_fill_rule` (`planner.py:2297`).

##### (e) Family member — **semantic data model change**
- `model.py:154-170` `FamilyMember(agg, b_anchor, order_by, description, declared_lineages, license)`; `model.py:164` `order_by: Optional[str] = None  # for ORDERED operators (last/first): the level to order by`.
- `parser.py:475-484` — the FAMILY-block grammar `<agg> [BLOCKED {…}] [ORDER <level>]`.
- `parser.py:678-692` — **"only reducers found families (scans are applied in queries…)"**: a non-REDUCER operator is a parse error in a FAMILY block. Reclassifying `first`/`last` out of REDUCER therefore *removes* them from every declared family unless this admission rule is rewritten.
- `parser.py:358-362`, `parser.py:663-670` — the dotted `level.last` carve-out in derived-formula well-formedness.
- `planner.py:1307-1320` `_resolve_member` (surface-spelling canonicalization, `approx_distinct`→`distinct`).
- `planner.py:2147` — "Several lawful family members and no authorized default -> CLARIFY".

Draft §10.3: "A generic 'family member' abstraction must not erase that difference." Removing `last`/`first` from `family` dicts changes the declaration model, the parser's admission rule, and every `next(iter(family))` default in (d).

##### (f) Input pin (inner anchor pinning) — **no change**
- Canonical spelling: `planner.py:782-791` `_canon_expr` (`@ {…}` canonical, bare / tuple accepted); `planner.py:715-741` `_convert_input_anchor` (incl. `@ {}` → `@ ()` scalar grain, `planner.py:723-731`).
- `planner.py:1354-1378` `_reduction_call`; `planner.py:1380-1392` `_pin_levels`; `planner.py:1394-1398` `_fmt_pin`; `planner.py:1399-1409` `_pin_input_grain`.
- Pin laws: `planner.py:1446-1485` `_check_pin_laws` (Law 1 `pin_coarser_than_output` REFUSE, Law 2 `redundant_pin` CLARIFY); reason set at `planner.py:82`.
- Completion machinery: `planner.py:2236-2247` `_pin_candidates`, `planner.py:2249-2271` `_pin_verdicts`, `planner.py:1571-1592` `_unpinned_disposition` (the **0 → Refuse / 1 → proceed / >1 → Clarify** rule), `planner.py:2661-2664` + `planner.py:2721-2735` `_defaulted_anchor_caveat`.

This is already the exact shape O1 §10 asks for on order ("under the existing input-anchor discipline"). It needs no semantic move — but see Q4: the completed pin is **not** written into `desugar`'s output.

##### (g) Fill rule — **new canonical field**
- Declaration: `parser.py:51` (Φ_v comment), `parser.py:430-437` (`FILL_RULES` closed vocabulary), `parser.py:513`.
- Model: `model.py:181-188` — `fill_rule` sits on **`MeasureColumn`, per-measure**, despite `planner.py:103` describing it as "resolved from the member contract".
- Resolution: `planner.py:2292-2299` `_column_fill_rule` — collapses to `None` (undeclared) on any disagreement between atoms.
- Application: `planner.py:626-670`; `engine.py:730-752`.
- Φ-composition through a map is explicitly **undeclared**: `planner.py:2775-2791`.
- Canonical form carries no Φ at all — it rides `ColumnResult.fill_rule` (`planner.py:103`) and the disclosure channel.

Draft §6.5 puts "empty / undefined / exceptional cases" inside the family-law contract that canonical form must fix, and §6.6 makes sufficient-state basis part of it. Today Φ is a post-hoc per-measure attribute.

##### (h) Natural or derived order — **semantic data model change**
- **`projection.py:223`** `TEMPORAL_LINEAGES = frozenset({"calendar", "fiscal"})` — hardcoded lineage names.
- **`projection.py:225-235`** `orderable_levels()` — docstring: *"Levels carrying a **natural (temporal) order**, over ADMITTED edges only… The manual's 'typically a temporal dimension'"*. This is verbatim the wording O1 §5 retires.
- `planner.py:293-367` `plan_order_axis` — the five cases; `planner.py:328-329` `governed = orderable_levels(); in_anchor = governed & set(anchor)`; `planner.py:351-352` one → proceed; `planner.py:353-361` none → `order_not_governed`; `planner.py:362-367` several → `order_axis_ambiguous`. Note `planner.py:321-327` already concedes the set "may later widen".
- Order key for family `last`/`first`: `parser.py:481` `order_by = mm.group(3)`, `model.py:164`, consumed at `engine.py:321-324`.
- **Direction is hardcoded into the operator identity**: `operators.py:167-170` `combine="argmax"/"argmin"` → `engine.py:324-327` `argfn = "arg_max" if op.combine == "argmax" else "arg_min"`. It is not a declarable or canonical field.
- **Ties are backend-arbitrary**: `engine.py:325-327` `arg_max(realized, order_phys)` — DuckDB picks. O1 §7 rules this non-canonical.
- Peer domain: `engine.py:296` (scans), `engine.py:333-335` `grain` (family last/first).
- Output `ORDER BY` is already correctly walled off from inner order: `planner.py:869-880` `_validate_clause_refs`, `planner.py:961-966` `_sort_frame`, `planner.py:981-990`. **O1 §9 is already satisfied.**
- `engine.py:250-254` records that engine-side order derivation was already retired once (2026-08-13) for exactly this class of reason.

Also: `by=` must name an **anchor coordinate** (`planner.py:337-349`), conflating the order axis with the output grain — incompatible with O1 §8/§9.

---

#### 3. Q2 — Is canonical form stable/serialized? What breaks on a new field?

**Serialized in four places:**
1. **Wire.** `frameql.py:109` `"desugared": d.render_canonical()` inside the EXPLAIN payload; surfaced by `tools.py:371-386`, MCP-exposed (`agent/providers.py:105`). Version gate: `disclosure_wire.py:41` `CONTRACT_VERSION = "4"`, re-exported `tools.py:57`.
2. **Tests pinning the exact string.** `.../packages/columna-core/tests/test_envelope_explain.py:17-23` (`ex["desugared"] == consumed`; `"avg(aov @ {day})" in ex["desugared"]`; `" AS " not in ex["desugared"]`); `.../packages/columna-core/tests/test_envelope_sugars.py:43,48-49` (canonical is a fixed point: `d1.render_canonical() == d2.render_canonical()`), `:128`; `.../packages/columna-core/tests/test_envelope_parser.py:136` **`parse_statement(st.render_canonical()) == st`** — a full round-trip identity; `.../packages/columna-server/tests/test_mcp_server.py:200`.
3. **Generated docs.** `tools.py:427-431` `frame_ql_grammar()` serves `envelope.__doc__` verbatim (`envelope.py:1-27`) as the wire answer for "what language is this".
4. **Conformance regime.** `.../packages/columna-core/tests/test_canonical_conformance.py:1-24` — "The realization must answer the canonical request that was actually submitted"; invariant, not regression.

**NOT serialized:** cache keys. `engine.py:228` and `engine.py:669` key on `(measure/member/agg, target, uni, where)` — the canonical statement text is never hashed. Lowering receipts are byte digests with **no canonicalization by design**: `.../packages/columna-server/src/columna_server/lowering_receipt.py:83-84`, `compiler/receipt.py:18` ("Canonical-form digests need a canonicalizer on both sides"), `compiler/emit.py:9`.

**What a new field would break:**
- `render_canonical` (`envelope.py:90-117`) must emit it, or canonical form stops being total. But `test_envelope_parser.py:136` requires `parse_statement(render_canonical()) == st` — so **any new canonical field that is rendered becomes surface grammar by construction.** This is the central structural blocker against O1 §4 ("explicit does not mean typed by the user").
- If instead the field is *not* rendered, the EXPLAIN identity `desugared == the consumed artifact` (`test_envelope_explain.py:17-21`, `frameql.py:75-77`) becomes false: the artifact would carry meaning the string does not.
- Wire: a changed `desugared` string for an unchanged utterance is the same class as WP-NAME-1, which bumped `"1"→"2"` (`disclosure_wire.py:52-58`). Expect `"4"→"5"`.
- The cache (`engine.py:228`) would need the new field folded in or two distinct completed contracts will alias to one memo entry.

---

#### 4. Q3 — Can canonical form expose a COMPLETED ordered-expression contract without new surface syntax?

**Not on `Statement` as it stands; yes on the EXPLAIN payload.**

- `Series` is `(expr: str, alias: str)` (`envelope.py:49-57`). There is no structured slot. Encoding order axis / direction / tie rule / peer domain into `expr` puts them through `parse_statement` (round-trip law, `test_envelope_parser.py:136`) — i.e. it *is* new surface syntax.
- Two existing precedents hang *completions* on the **disclosure** channel rather than on canonical form: `planner.py:2721-2735` `_defaulted_anchor_caveat` ("input anchor was not given and was DEFAULTED to '…'") and `engine.py:305-308` `Caveat(TRANSPORT, f"scan {scan_op} over order '{order_axis}' within {partition}")`. These already *compute* peer domain and order axis — but disclosures are not the canonical form, and `frameql.py:104-110` keeps `desugared` and `series[].would_be.disclosures` as separate fields.
- **The available hook:** `frameql.py:96-108` already builds a per-series dict `{"name", "expr", "cone": {"atoms","derived","edges","scope"}, "would_be": {…}}`. An additive `"order_contract": {...}` block beside `"cone"` — populated from `plan_order_axis` (`planner.py:293-367`) and `FamilyMember.order_by` (`model.py:164`) — exposes the completion with **zero grammar change** and zero `render_canonical` change. Precedent for additive-without-bump exists (`.../packages/columna-server/tests/test_describe_insulation.py:82-83`).
- Caveat: that satisfies "canonicalization exposes the completed contract" for the *wire*, not for the in-process artifact `run_statement` consumes (`planner.py:1251-1262`), which is still the string-only `Statement`.

---

#### 5. Q4 — Does canonicalization ELIMINATE any anchor?

**Yes — but at resolution time, not in `desugar`, and it is invisible in canonical form.**

- `planner.py:1553-1569` `_distinct_readings` — "Quotient the lawful SYNTACTIC pins by governed analytical equivalence… Candidate anchors that are syntactically distinct but provably equivalent under governed analytical law do not constitute multiple analytical readings." Returns `[list(lawful)]` (one class) when `_re_entrant`, else one class per pin.
- `planner.py:1594-1601` `_unpinned_reading` — with one class, returns `(klass[0],)`, i.e. **an arbitrary representative**, with `meaning_bearing = len(klass) == 1`.
- `planner.py:2717-2718` — when `meaning_bearing` is False the material `input_anchor` caveat is **suppressed**: the eliminated anchors are disclosed nowhere.

**Premises (all four required)** — `planner.py:1538-1552` `_re_entrant`:
1. `len(self._atoms(inner, ())) == 1` — single atom, not a derivation/compound;
2. the measure's family has exactly one member;
3. that member `== reducer` (same continuation);
4. `Operator.re_entrant is True`.

`re_entrant` is fail-closed and today **`sum` only** (`operators.py:130`); the doctrine is at `operators.py:73-107` (`rho((+)_i eta(rho(s_i))) == rho((+)_i s_i)`; "strictly stronger than monoidality"; `count` excluded for its non-identity lift).

Two adjacent eliminations:
- `planner.py:2678-2679` `if anchor == tuple(pinned): served = frame` — the travel stage is elided when pin equals output anchor.
- `planner.py:1399-1409` `_pin_input_grain` silently **widens** the input grain with output levels orthogonal to the pin. Not visible in canonical form either.

Draft §10.1 states the target rule: "Different spellings or **intermediate anchors** do not create several readings where governance proves them analytically equivalent." The build implements the rule; the gap is that the surviving representative is never written back into the `desugared` artifact.

---

#### 6. Q5 — One canonicalization entry point, or several?

**Six, in three jurisdictions, plus one unrelated homonym.**

| # | Jurisdiction | Site | What it canonicalizes |
|---|---|---|---|
| 1 | parser-side | `envelope.py:207-221` `_parse_anchor_braces`; `envelope.py:38` `_CLAUSE_ORDER`; `envelope.py:341-352` | comma → `*` anchor product; clause order |
| 2 | planner-side (**the** transform) | `planner.py:793-838` `desugar` + `_canon_expr` `782-791`, `_convert_input_anchor` `715-741`, `_default_name` `744-780`, `_expand_total` `840-860`, `resolve_anchor` `508` | WITH inlining, `@ {…}` braces, series names, anchor levels |
| 3 | substrate adapter (**de**-canonicalizing) | `planner.py:1244-1248` `_engine_columns` | canonical `@ {level}` → `@ level` for CPython `ast` |
| 4 | operator-identity | `operators.py:224-229` `ALIASES` / `canonical()`; `projection.py:135-136` `canonical_op`; `planner.py:1307-1320` `_resolve_member`; `planner.py:1339-1342` `_inline_reducer` | surface spelling → canonical operator (`avg`→`mean`, `approx_distinct`→`distinct`) |
| 5 | render/wire-side | `envelope.py:90-117` `render_canonical`; `planner.py:85-91` `_fmt_anchor`; `planner.py:1394-1398` `_fmt_pin` | emitted spelling |
| 6 | eval harness (unrelated) | `.../packages/columna-server/src/columna_server/init/eval.py:134-150` `_desugar` | `HIERARCHY a->b->c` → edges; declaration-side, not query-side |

**Finding:** #4 is *not* reflected in #2 or #5. `operators.py:219-223` says so explicitly — "`canonical()` is not wired into member/operator lookup (the live call-position table is `Planner._INLINE_REDUCERS`)". So `SELECT avg(x @ {day})` canonicalizes to a `desugared` string still spelling `avg`, while the governed operator identity is `mean` (`operators.py:204-210`). Two canonicalizers disagree about the canonical form today; any vNext order-contract work that keys off operator identity will hit this first.

---

#### 7. Classification summary

| Assumption | Move required |
|---|---|
| reducer atom | semantic data model change |
| map expression | rename/reclassification only |
| scan | new canonical field |
| default reducer | compatibility normalization |
| family member | semantic data model change |
| input pin | no change |
| fill rule | new canonical field |
| natural / derived order | semantic data model change |

**Three findings worth escalating beyond the brief:**
1. `planner.py:1900` — `_atoms` defaults the family member with an **unguarded** `next(iter(family))`, feeding both the EXPLAIN wire atoms (`planner.py:1276`) and `_column_fill_rule` (`planner.py:2297`), where every other call site Clarifies on |family| > 1.
2. `engine.py:325-327` — `arg_max`/`arg_min` tie-breaking is delegated to DuckDB. O1 §7 rules this unlawful as canonical; there is no tie field anywhere in the model to fix it with.
3. `test_envelope_parser.py:136` (`parse_statement(render_canonical()) == st`) is the hard constraint: under the current design **any rendered canonical field is surface syntax**. Either that law is amended, or the completed order contract lives on the EXPLAIN payload (`frameql.py:96-108`) rather than in `Statement`.


---

## 3.5 Planner / adjudication, broadcast, WHERE

*Inspector `agent-ab8e6bbbe35e99ade` · primary target doc: `frameql_vnext_m1_semantic_review_v0_1.md`*

I have enough evidence. Report follows.

---

### M2 Reconnaissance — planner / adjudication, broadcast, WHERE

Root: `/data/repos/978ea3c9feee4ad79341d42517782efd/columna`. All paths absolute; line numbers at HEAD `17e3b6b`.

**Orientation fact first:** there is no query-time `adjudication/` module. `/data/repos/978ea3c9feee4ad79341d42517782efd/columna/packages/columna-core/src/columna_core/adjudication.py` is **publish-time proof/certification** (licenses, edge/face admission, `_prove_data`, `_prove_hierarchy`, `PublishedScope` at :374, `adjudicate()` at :797). All request-time adjudication lives in `planner.py` + the reason→verdict table in `disclosure.py:227-440`.

---

#### PART 1 — reason-code trace

The reason→verdict policy table is `REASON_OUTCOME` at `/data/repos/978ea3c9feee4ad79341d42517782efd/columna/packages/columna-core/src/columna_core/disclosure.py:227`, closed and fail-closed via `outcome_for` at `disclosure.py:447` (`UnregisteredReason`, `disclosure.py:443`).

| code | exists | registered | raised at | evidence consumed |
|---|---|---|---|---|
| `input_anchor_ambiguous` | yes | `disclosure.py:241` CLARIFY/AMBIGUOUS/ANALYTICAL | `planner.py:1806` in `_unpinned_reduction_refusal` (`planner.py:1793`), reached from `_unpinned_reading` `planner.py:1603` | `_pin_verdicts` `planner.py:2249` → `lawful` set → `_distinct_readings` `planner.py:1553` equivalence classes; `len(readings) > 1` |
| `input_anchor_unavailable` | yes | `disclosure.py:370` REFUSE/UNSUPPORTED/ANALYTICAL | `planner.py:1766` and `planner.py:1787` in `_no_lawful_pin_refusal` (`planner.py:1697`) | `refused` list of `(level, Refusal)` from `_pin_verdicts`; fires when the surviving verdicts **disagree** (`planner.py:1736-1737` unanimity test excluding `_PIN_SHAPE_REASONS`), or when no candidate was even enumerable (`planner.py:1775-1787`) |
| `redundant_pin` | yes | `disclosure.py:245` CLARIFY/AMBIGUOUS | `planner.py:1479` in `_check_pin_laws` (WP-GRAIN-1 Law 2) | pure lattice: `self.m.find_path({pi}, pj) is not None` over certified edges (`projection.py:258`) for two pin levels |
| `pin_coarser_than_output` | yes | `disclosure.py:385` REFUSE/UNSUPPORTED | `planner.py:1461` in `_check_pin_laws` (Law 1) | `find_path({a}, p)` where `a ∈ anchor`, `p ∈ pinned` |
| `order_axis_ambiguous` | yes | `disclosure.py:347` CLARIFY/AMBIGUOUS | `planner.py:362` in `plan_order_axis` | `self.m.orderable_levels() & set(anchor)`, size > 1 |
| `order_not_governed` | yes | `disclosure.py:339` REFUSE/UNSUPPORTED | `planner.py:341` (explicit `by=` not in the governed∩anchor set) and `planner.py:354` (no `by=`, empty set) | same `orderable_levels() & set(anchor)` |
| broadcast | **no reason code** — a served path, not a refusal | — | `planner.py:1422-1429` (`_check_map_operand_pin`, `pinned == ()` exempt from co-anchoring) and `planner.py:2487-2504` (`_node` MatMult branch) | `_pin_levels(node.right) == ()`; then `payload.height != 1` → `Refusal("unsupported", planner.py:2501)`. The neighbouring refusal for a non-scalar coarse operand is `co_anchor_required` (`planner.py:1438`, registered `disclosure.py:315`) |
| `cross_universe` | yes | `disclosure.py:236` **ERROR / LANGUAGE** (not a mood) | `planner.py:278` in `_check_single_universe`; called from `run` `planner.py:590` and `_where_reachability` `planner.py:1128` | `{self.m.measures[mm].universe for (mm,_) in self._atoms(node, anchor)}`, `len(unis) > 1` |
| filter reachability | yes, three codes | `filter_unreachable` `disclosure.py:270` REFUSE/ANALYTICAL; `filter_unsupported` `disclosure.py:252` ERROR/REALIZATION; `unknown` `disclosure.py:439` ERROR/LANGUAGE | `_where_reachability` `planner.py:1079`: Stage A `unknown` at `planner.py:1118`; Stage B `filter_unreachable` at `planner.py:1164`; `_where_unsupported` `planner.py:1203` → `filter_unsupported` at `planner.py:1235` | `self._predicate_column(p)` (`planner.py:920`); `self.m.levels`; per-series `universes[uni].base_dimensions`; `find_path(base, lvl)` |
| family/member selection | yes | `family_member_ambiguous` `disclosure.py:280` CLARIFY/AMBIGUOUS | built in `_family_member_clarify` `planner.py:2168`; raised at `planner.py:2527` (scan input), `planner.py:2552` (`_node` measure ref), `planner.py:2417` (`_infer`); re-offered at output anchor `planner.py:1641`/`_reoffer_at_output_anchor` `planner.py:1676` | `len(meas.family) != 1`; then `_lawful_family_members` `planner.py:2115` re-adjudicates each member through `_check_expression_law` and drops **only** those earning `blocked_reduction` (`planner.py:2138`) |
| `blocked_reduction` | yes | `disclosure.py:356` REFUSE/UNSUPPORTED | `planner.py:1741`, `planner.py:1754`, `planner.py:1778` (`_no_lawful_pin_refusal`), `planner.py:2161`; underlying test `_travel_violation` `planner.py:2073` over `_Travel` tuples (`planner.py:70-80`) | `_law_travels` `planner.py:1973` / `_generated_travel` `planner.py:2052`; the measure's `BAnchor.blocked_lineages` (`model.py:151`) vs the lineages the reduction traverses (`_traversed_lineages` `planner.py:1946`) |
| standing / fill / support | **split across three unrelated mechanisms, no unified code** | fill is a *caveat* vocabulary, not a reason: `DATA_GAP` `disclosure.py:47`, `DECLARED_FILL` :53, `UNKNOWN_ABSENCE` :55, `OUT_OF_POPULATION` :57, `UNDECLARED_ABSENCE` :59 | (a) frame-level Φ pass `planner.py:635-670`; (b) expression-level divergence `_divergence_caveats` `planner.py:2793` from `_apply`'s full-outer align `planner.py:2836-2841`; (c) engine crossed-grain Φ `engine.py:736-750`. "Standing" as a *name* means something else entirely: `_realization_standing` `planner.py:1021`, `_scan_order_standing` `planner.py:995`, `engine.face_crossing_standing` `engine.py:383` — pre-flight *capability* standing, not point standing | `Measure.fill_rule` (`planner.py:103` comment, `_column_fill_rule` `planner.py:2292`); null counts on the aligned frame (`planner.py:639`, `planner.py:2839`) |

Nothing in the tree emits a code for *point existence*, *placement under A*, or *measure eligibility* as distinct conditions. Absence is one undifferentiated `null` disambiguated only post-hoc by declared Φ.

---

##### 1. Is zero/one/many centralized?

**Scattered — five independent implementations, none sharing a helper.**

1. Input anchor: `_unpinned_reading` `planner.py:1594`, over `_distinct_readings` `planner.py:1553`. This is the only site that quotients readings by governed equivalence (`_re_entrant` `planner.py:1514`, reading `Operator.re_entrant` `operators.py:70`).
2. Order axis: `plan_order_axis` `planner.py:351-367` — the 1/0/many branch is written inline against `in_anchor`.
3. Family member: `_family_member_clarify` `planner.py:2146` + `_lawful_family_members` `planner.py:2115`; the zero case falls back to a refusal at `planner.py:2160-2163`. The one-member case is a bare `len(meas.family) != 1` guard duplicated at `planner.py:2417`, `planner.py:2525`, `planner.py:2551`.
4. Face driver: `engine.face_crossing_standing` `engine.py:383` → `face_driver_ambiguous` (`disclosure.py:302`).
5. WHERE dimensions: `_where_reachability` `planner.py:1079` deliberately does **not** use the rule — P1-22 removed a Clarify there on the ground that its "alternatives" were rewrites of the ask, not readings (`planner.py:1085-1097`).

The only shared artifact is the *classification* chokepoint, one level below the rule: `Refusal.classified()` → `outcome_for` `disclosure.py:447`. That maps reason→mood; it does not count readings.

Could it generalize? The pieces exist: each site already computes a candidate set and each already has a lawfulness filter it applies *before* counting (`_lawful_pins` `planner.py:2274`, `_lawful_family_members` `planner.py:2115`, `orderable_levels() & anchor`). What only site 1 has is the **quotient** step — `_distinct_readings` — and its authority (`re_entrant`) is reducer-specific, so a general rule would need a per-dimension equivalence predicate. The `_PIN_SHAPE_REASONS` carve-out at `planner.py:82` and `planner.py:1736` also shows the counting is not purely set-cardinality: some verdicts are excluded from voting. That exclusion logic is local to one site today.

##### 2. Where does order-axis derivation get its authority?

**A hardcoded set of lineage *names*, gated on certification. Not declared `order_by`, not physical row order.**

```
projection.py:224   TEMPORAL_LINEAGES = frozenset({"calendar", "fiscal"})
projection.py:225   def orderable_levels(self) -> frozenset:
projection.py:232       if e.lineage in self.TEMPORAL_LINEAGES and self._admitted(e):
projection.py:233           lv.add(e.frm); lv.add(e.to)
```

Consumed at `planner.py:328` (`governed = self.m.orderable_levels()`), and nowhere else for scans. The engine is deliberately blind: `engine.py:250-254` records the retirement of its own copy, and `engine.py:288-294` refuses if `order_axis is None` rather than inferring.

There **is** a declared order surface, and `plan_order_axis` never reads it: `FamilyMember.order_by` (`model.py:164`), parsed from `FAMILY { last ORDER <level> }` at `parser.py:476-484`, is consumed only by the ORDERED-witness delivery path at `engine.py:322-328` (`arg_max(value, order_phys)`). So `last`/`first` order by a *declared key*; `cumsum`/`lag` order by *chronology-by-lineage-name*. Two authorities, no reconciliation.

Physical row order is never an authority: `engine.py:297` sorts explicitly by `partition + [order_axis]`.

##### 3. Can the planner distinguish "exactly one governed order completion" from "there is a time dimension, so chronology"?

**No — today they are the same computation, by construction.** `plan_order_axis` at `planner.py:351` (`if len(in_anchor) == 1`) applies a cardinality test to a set (`orderable_levels()`) whose *sole* membership criterion is "on an admitted edge whose lineage string is `calendar` or `fiscal`" (`projection.py:232`). The |L|=1 branch cannot fire for a non-temporal reason, so the two claims are indistinguishable in the current output. The code says so at `planner.py:321-327`: "a temporal level is 'one common source of governed order, not the definition of order', so that set may later widen."

**Does it have the data to separate them without new Manifold fields?** Partially, and unevenly:

- Available: `FunctionalEdge.lineage` (`model.py:85`) and the full admitted-edge graph; `FamilyMember.order_by` (`model.py:164`) — a *declared* order key already parsed and stored, currently unread by this path; `Face.order` (`model.py:250`, `FACE_ORDERS`, `parser.py:317`) — a declared ORDER direction for assign faces; operator `needs_order` (`operators.py:64`).
- Not available: any per-level or per-lineage "confers order" declaration. `TEMPORAL_LINEAGES` is a Python literal, not Manifold-declared, so a manifold cannot today *declare* a third ordered lineage without a code edit — that is the concrete gap, and it is in `projection.py`, not in the Manifold schema.
- `order_by` is per-*family-member*, not per-anchor, so using it as the completion source would change the quantification (member-scoped, not frame-scoped) — a semantic move, not a plumbing one.

##### 4. What structure represents broadcast?

**Broadcast is not a structure. It is a kind-collapse to `"scalar"`, and it exists only for the empty pin `@ {}`.**

`planner.py:2487-2504`:

```
2489  if self._pin_levels(node.right) == ():
2497      k, payload, disc, dtype = self._node(node.left, (), where, trace)
2500      if payload.height != 1: raise Refusal("unsupported", ...)
2504      return "scalar", payload[_V][0], disc, dtype
```

The stated rationale is at `planner.py:2490-2496`: reuse the scalar kind "the same one a literal arrives as." Consequences visible in the code:

- **The value is stripped of its frame and its coordinates.** After line 2504 it is a bare Python float. `_apply` `planner.py:2843-2846` then does `lp.with_columns(f(pl.col(_V), rp))` — the scalar is fused into the finer operand's frame with no join and no key. There is no carrier for "this number came from `{}`".
- **Analytical identity is not re-tagged as the finer anchor either** — because nothing is tagged at all. The dtype survives (`dtype` returned at :2504) and the `Disclosure` survives (merged in `Disclosure.combine` `disclosure.py:198`), but the anchor does not. The doc's requirement ("makes the already-established value available there *without changing its analytical identity*") is satisfied by accident of erasure, not by representation: after 2504 nothing downstream can assert *either* identity.
- The exemption is declared, not incidental: `planner.py:1422-1429` returns early from `_check_map_operand_pin` for `pinned == ()`, skipping both `_check_pin_laws` and the co-anchoring equality at `planner.py:1431`.
- **Any coarser-but-not-scalar operand is refused**, not broadcast: `co_anchor_required` at `planner.py:1438`, telling the asker to write an explicit reduction. So `revenue @ {region}` inside a `{store}` expression has no broadcast path today.
- The word "broadcast" elsewhere in the tree means something different — physical attribute replication onto raw rows during transport (`engine.py:892`, `engine.py:922-935`, `engine.py:1018-1024`, `model.py:31`). These are unrelated mechanisms sharing a name.

##### 5. Where does WHERE restriction enter the plan?

**Per-series, pre-reduction, threaded as an opaque predicate string. It is documented per-series and is implemented per-series.**

- Parsed per-series: `envelope.py:85` (`where: list  # [str] per-series predicates`), `envelope.py:374`.
- Macro-expanded and proven total: `desugar` `planner.py:829` → `_expand_total` `planner.py:840`. The comment at `planner.py:836-845` states the reason WHERE is expanded while HAVING/ORDER BY are not: "WHERE is different in kind: it binds PRE-reduction, over the series' own input."
- Adjudicated per-series for reachability: `_where_reachability` `planner.py:1079`, keyed `{series_name: Outcome}`; delivered at `planner.py:1258`.
- Applied per-series at `run`: `planner.py:570-573` short-circuits only the series that cannot bind, "so reachable siblings still serve (the juxtaposition model)".
- Normalized to SQL once: `_to_backend_predicate` `planner.py:563` / `planner.py:1182`.
- Reaches the substrate as a scan-level filter: `engine.py:339-344` (`where_eff`), `engine.py:344` `con.deliver_measure(..., where_eff)`; holistic path `engine.py:911`.

**Does anything treat it as a universe carve? No — and the carve is a separate, declared mechanism.** The universe predicate is `self.m.universes[meas.universe].predicate` (`engine.py:332`, `engine.py:918-919`), applied by `_confine` `engine.py:965`, and it is structurally distinct from `where` at every call site. `UniverseShape` explicitly carries no predicate: `projection.py:78` `base_dimensions: frozenset    # NO predicate (confinement is an engine/resolution concern)`. Two soft spots worth noting, neither a carve:

- `engine.py:228` — `key = (measure, member, target, uni, where)`. WHERE is part of the *cache* key alongside the universe, so a filtered result never aliases an unfiltered one; but `uni` is still the measure's declared universe. Correct, if adjacent to the confusion.
- `engine.py:1082` — the sketch path bypasses its witness when `where is not None` (`why = "filtered query"`, `engine.py:1088`), i.e. WHERE invalidates a precomputed support. That is restriction changing values, exactly as M1-B says it may.
- `planner.py:672-674` records that the frame-level population caveat and `ON UNIVERSE` in query position are retired; the surviving `population` argument (`planner.py:2405-2416`) is an assertion *about which declared universe*, never a new one.

##### 6. Which emitted reason codes would be semantically wrong under existence / placement / eligibility / support?

Ordered by severity of the conflation:

1. **`out_of_universe`** (`planner.py:495`, registered `disclosure.py:384`). Message: *"'T' is not addressable in universe 'uni' (out of domain — undefined, not missing)"*. This is raised for *addressability of a dimension*, i.e. a **placement** failure (no governed π_A), but its wording asserts a claim about the **measure's eligibility/domain**. Under the four-way split these are different findings with different remedies.

2. **`input_anchor_unavailable`** (`planner.py:1766`). Its detail enumerates verdicts that mix jurisdictions on purpose — `planner.py:1768-1770` names "out of universe, non-functional transport, coarser-than-output" as jointly constituting "nowhere to stand". Placement, structural-alignment shape and eligibility are being summed into a single cardinality-zero claim. The code already knows they disagree (that disagreement is literally the trigger) and still emits one reason.

3. **The Φ-fill caveat family** — `DECLARED_FILL` / `UNKNOWN_ABSENCE` / `OUT_OF_POPULATION` / `UNDECLARED_ABSENCE` at `planner.py:650-670`. All four are selected by one switch on `c.fill_rule` over one input: `data[c.name].null_count()` (`planner.py:639`). A null there can be *point absent from the alignment domain*, *point present but measure unsupported*, or *point outside the member's population* — three of the four target distinctions — and the discriminator is a per-*measure* declaration, not per-cell evidence. `planner.py:646-649` admits this directly: "the two null-origins are not distinguishable per cell at this point". `OUT_OF_POPULATION` in particular *asserts* eligibility-ineligibility from a declaration while the actual cell may be a support gap.

4. **`_divergence_caveats`** `planner.py:2793-2808`. The text asserts *"these coordinates are IN the frame and carry no value"* — a point-existence claim plus a support claim, minted from a full-outer join null (`planner.py:2837-2839`). Correct today only because the alignment domain is declared at `planner.py:2836`; it is not derived from any governed statement about π_A.

5. **`blocked_reduction`** (`planner.py:1741`/:1754/:1778). Eligibility-of-operator-along-lineage. Semantically the *cleanest* of the set — it is genuinely an eligibility verdict — but it is emitted from `_no_lawful_pin_refusal`, i.e. from a placement-enumeration routine, and `disclosure.py:356-369` notes it shares its spelling with a tombstoned *caveat* code ("one concept, two channels"). Under a split model the same string would need to name a channel-independent eligibility fact.

6. **`filter_unreachable`** (`planner.py:1164`). Wording — "the pre-reduction filter has no grain to bind to" — is a placement claim about the *predicate*, correctly ANALYTICAL. Not wrong, but it is the only place the codebase distinguishes placement cleanly, and it does so ad hoc rather than by a shared law.

Codes that would survive unchanged: `redundant_pin`, `pin_coarser_than_output`, `order_axis_ambiguous`, `order_not_governed`, `cross_universe`, `family_member_ambiguous`, `input_anchor_ambiguous`, `filter_unsupported` — these are about the *ask's* shape or under-determination, not about points.

---

#### PART 2 — seams, by canonical form

Legend: **E** exists · **P** partial · **✗** absent.

##### `mean(revenue @ order)`

| seam | | evidence |
|---|---|---|
| language grammar | **E** | `_reduction_call` `planner.py:1354`; `mean` reaches it via `_inline_reducer` `planner.py:1339` → `SERIES_REDUCERS` `operators.py:236`; `@` allowed by `_ALLOWED` `planner.py:62` |
| canonical identity | **E** | `desugar` normalizes to `@ {order}` (`planner.py:793-806`); reading string `f"{reducer} of {ast.unparse(inner)}@{pin_str}"` `planner.py:2675`; `avg`→`mean` via `ALIASES` `operators.py:224` |
| Manifold law admission | **P** | `mean` is registered with a law address — `operators.py:155-157`, `in_core=False` — so `mean BLOCKED {lineage}` parses and `_travel_violation` `planner.py:2073` can bar it. But `in_core=False` + `parser.py:687-691` mean it cannot be a *served declared family member*; the note at `operators.py:150-154` states the entry exists "NOT to define new arithmetic" |
| co-participation | n/a | single operand |
| planner capability | **E** | `_resolve_inline_reduction` `planner.py:2643`; admissibility `_admit_pin` `planner.py:2175` |
| engine realization | **E** | `_SERIES_REDUCE["mean"]` `engine.py:786`; `reduce_series_to_anchor` `engine.py:823` |

##### `variance(price @ transaction)`

| seam | | evidence |
|---|---|---|
| language grammar | **✗** | `_inline_reducer` `planner.py:1339-1342` returns None (`variance` ∉ `SERIES_REDUCERS` `operators.py:236`), so the node is not a reduction call; it falls through `_infer` to `Refusal("unknown", ...)` `planner.py:2460` |
| canonical identity | **✗** | no reducer ⇒ no `reading` string is built; `_default_name` `planner.py:744` would name the raw spelling only |
| Manifold law admission | **✗** | not in `REGISTRY` `operators.py:121-200`; `get_operator` raises `KeyError` `operators.py:240`; a `FAMILY { variance }` is rejected at `parser.py:683-685` |
| co-participation | n/a | single operand |
| planner capability | **✗** | no `Operator` ⇒ no `kind`, no `accepts`, no `witness`, no `re_entrant` ⇒ `_re_entrant` `planner.py:1550` and `_reducer_out_dtype` `planner.py:1495` have nothing to read |
| engine realization | **✗** | absent from `_SERIES_REDUCE` `engine.py:784-790` and from the witness dispatch `engine.py:238-246`; would be HOLISTIC-shaped, and `_recompute_holistic` `engine.py:901` currently serves median/mode only (`operators.py:153`) |

##### `covariance(price @ order, quantity @ order)`

| seam | | evidence |
|---|---|---|
| language grammar | **✗** | arity is hard-refused before the operator is even looked up: `_reduction_call` `planner.py:1367-1370` — `if len(node.args) != 1 or node.keywords: raise Refusal("unknown", "... takes exactly one column argument")` |
| canonical identity | **✗** | as above; no two-operand reading form exists anywhere |
| Manifold law admission | **✗** | `Operator` `operators.py:52-71` has no arity field at all; `accepts` is a single dtype set, `out_rule` a single rule |
| co-participation | **✗** | zero occurrences of any co-participation concept in `columna_core` (grep for co.participation / multi-input / joint operand: no hits). The nearest constructs are (a) `co_anchor_required` `planner.py:1438` / `disclosure.py:315`, which *refuses* differently-anchored operands, and (b) the retired `co_anchor_ambiguous` tombstone `disclosure.py:230-235`. `planner.py:2484-2486` rules the surface out explicitly: *"DELIBERATELY NOT A JOINT-OPERAND SURFACE (ruled Huayin, 2026-08-31): `@ {a,b}` keeps its one meaning, composite analytical GRAIN. Nothing here introduces `(a,b) @ A` or enlarges reducer arity."* |
| planner capability | **✗** | `_admit_pin` `planner.py:2175`, `_pin_verdicts` `planner.py:2249`, `_law_travels` `planner.py:1973` all thread a single `inner` node |
| engine realization | **✗** | `_SERIES_REDUCE` `engine.py:784` maps to single-column Polars aggs (`lambda c: ...`) |

##### `(revenue, cost) @ order`

| seam | | evidence |
|---|---|---|
| language grammar | **P — parses, then dies** | `ast.Tuple` is in `_ALLOWED` `planner.py:63-64`, but only for the *right* side of `@`: the comment reads "a Tuple anywhere else is caught semantically by `_infer`". `_check_map_operand_pin` `planner.py:1410` inspects only `node.right`, so a left-hand tuple passes the pin law; then `_node` `planner.py:2505` recurses into the Tuple and reaches `Refusal("unknown", "unsupported expression node Tuple")` `planner.py:2603` (and `_infer` `planner.py:2460` on the plan path) |
| canonical identity | **✗** | `_pin_levels` `planner.py:1380` reads tuples only as *pin* level lists; there is no tuple-valued expression identity |
| Manifold law admission | **✗** | no tuple/product value domain: `types.py` (73 lines) carries scalar dtype classes only; `Measure.logical_type` is a single tag (`model.py`) |
| co-participation | **✗** | same as covariance — the ruling at `planner.py:2484-2486` names this exact form as out of scope |
| planner capability | **✗** | `_apply` `planner.py:2811` is strictly binary-scalar/column; kinds are `"scalar"` or `"col"` only (`planner.py:2464`, `:2504`, `:2537`) |
| engine realization | **✗** | every engine return is a single `_value` column (`engine.py:319`, `engine.py:820`); `ColumnResult.frame` `planner.py:95` is one named column |

---

##### Two cross-cutting observations worth carrying into M2 planning (evidence, not proposals)

- **`(revenue, cost) @ order` is the only one of the four forms that reaches the planner's pin machinery before failing.** Its refusal is emitted by the generic node fallback (`planner.py:2603`), not by a law, so it currently classifies as `unknown`/ERROR/LANGUAGE (`disclosure.py:439`) — the same bucket as a typo.
- **`plan()` and `run()` reach these seams through different dispatchers** — `_infer` `planner.py:2342` vs `_node` `planner.py:2462` — and the tree records this as a repeat failure mode (`planner.py:1413-1416`, `planner.py:2470-2476`, `planner.py:2510-2514`). Any seam added on one side without the other reproduces the P0-18 / Mission B defect: parses clean, plans `serve`, dies in the engine.


---

## 3.6 Ordered-expression machinery

*Inspector `agent-a064b0295bb6f8cb9` · primary target doc: `frameql_vnext_o1_ordered_expression_compatibility_ruling_v0_1.md`*

### Ordered-expression machinery — current state (HEAD 17e3b6b)

Doc read: `/tmp/m2recon/frameql_vnext_o1_ordered_expression_compatibility_ruling_v0_1.md`.

---

#### A. Per-operation inventory

| op | exists? | operator registry | capability toml | core profile | classified as | executes how |
|---|---|---|---|---|---|---|
| `first` | yes | `operators.py:168` `Operator("first", REDUCER, ORDERED_W, True, accepts=ANY, combine="argmin", needs_order=True)` | `specs/frameql_capabilities.toml:151-159` `category="reducer"`, `standing="ratified"` | `specs/profiles/core_profile.toml:64-66` `execute` | **measure-family reducer**, witness `ORDERED_W` | delivery `arg_min(value, order_key)` + `min(order_key)` (`engine.py:339-341`); combine on transport = `sort_by("_order").first()` (`engine.py:771-773`) |
| `last` | yes | `operators.py:166` (`combine="argmax"`) | toml `:141-149` `category="reducer"`, `ratified` | `core_profile.toml:61-63` `execute` | same | `arg_max(...)` / `max(order_key)`; combine `sort_by("_order").last()` (`engine.py:768-770`) |
| `lag` | yes | `operators.py:193` `SCAN`, `needs_order=True`, `scan_impl="lag"` | toml `:726-733` `category="scan"`, `standing="proposed"` | `core_profile.toml:126-128` `execute` | **scan** | `pl.col("_value").shift(n)` over derived partition (`engine.py:299-302`) |
| `lead` | yes | `operators.py:194` `scan_impl="lead"` | toml `:734-741` scan/proposed | `core_profile.toml:129-131` `execute` | scan | `.shift(-n)` (`engine.py:300`) |
| `cumsum` (+`cummax`,`cummin`) | yes | `operators.py:190-192` | toml `:649-680` scan/proposed | `core_profile.toml:117-125` `execute` | scan | `v.cum_sum()/cum_max()/cum_min()` (`engine.py:299`) after `frame.sort(partition+[order_axis])` (`engine.py:297`) |
| `rolling_*` | **contract only** | `operators.py:197-200` only `rolling_sum`, `rolling_mean`; `needs_window=True`, `in_core=False` | toml `:681-725` five rows (`rolling_sum/mean/min/max/count`), all scan/proposed, `note="windowed"` | `core_profile.toml:135-142` — only sum/mean, `level="plan"` | scan, not executable | refuses `unsupported` twice: planner `planner.py:1868-1874` (on `window=`), engine `engine.py:266-277` (on `not op.in_core`) |
| `rank` | **does not exist in the build** | ABSENT from `REGISTRY` (no entry in `operators.py:121-201`) | toml `:742-749` `category="scan"`, `standing="proposed"`; siblings `dense_rank` `:750-757`, `row_number` `:758-765` | ABSENT from `core_profile.toml` | canonically a "scan"; unknown to the engine | `rank(x)` hits `planner.py:1826-1830` → `Refusal("unknown", "there is no operator named 'rank' in the registry")` |

Also registry-only, no toml/profile consequence for this task: `pct_change` (`operators.py:195`), `cumprod`/`ewm_mean` are toml-only (`:657-664`, `:774-781`).

Two disjoint execution paths, not one:
- **`first`/`last`** never reach `engine.scan`. They are a *reducer atom* resolved through `_deliver_and_transport_monoid` (`engine.py:311-380`), dispatched at `engine.py:243-246` (`# VALUE or ORDERED — both reduce in witness-space`).
- **scans** go through `Planner._node` → `planner.py:2530-2535` → `engine.scan` (`engine.py:257-310`), the only `engine.scan` call site in the tree.

Surface reachability asymmetry: `last`/`first` are reachable **only as member spellings** (`level.last`), never as function calls. `Planner._inline_reducer` (`planner.py:1339-1342`) admits only `SERIES_REDUCERS = {"sum","mean","min","max","count"}` (`operators.py:236`), so `last(x @ {store,day})` — the ruling's §11 shorthand — does not parse as a reduction today; it falls through to `_scan_call` and refuses `'last' is a reducer, not a scan` (`planner.py:1831-1834`).

---

#### B. Field-by-field representation today

| contract field | current representation | file:line |
|---|---|---|
| **peer domain** | **No declared representation.** Derived implicitly, two different ways. Scans: `partition = [d for d in target if d != order_axis]` — everything in the output anchor minus the order axis | `engine.py:296` |
| | Ordered reducers: the peer domain is whatever the group-by/transport collapses into the output anchor; never named | `engine.py:351-371` |
| **order axis / key — scans** | `order_axis: str` — a *single level name*, planner-chosen, handed down as a kwarg | `planner.py:293-368` (`plan_order_axis`), `engine.py:259`, `engine.py:288-294` |
| **order axis / key — ordered reducers** | `FamilyMember.order_by: Optional[str]` — a single level name declared per family member | `model.py:164`; parsed `parser.py:476-484` (`<agg> [BLOCKED {..}] [ORDER <level>]`); consumed `engine.py:322-324` |
| **direction** | **No representation at all.** Ascending is hardcoded/implicit: `frame.sort(...)` with Polars default ascending (`engine.py:297`); direction for first/last is baked into the *operator name* via `combine="argmax"/"argmin"` (`operators.py:166,168`) and the `argfn/ordfn` selection (`engine.py:325-326`) |
| **tie rule** | **No representation.** Emergent only. Delivery layer: SQL `arg_max/arg_min` tie behaviour is the backend's (`engine.py:328-329`). Combine layer: `sort_by("_order").last()/.first()` — Polars sort stability (`engine.py:769,772`). Scan layer: `frame.sort(...)` stability (`engine.py:297`). Nothing declares, checks, or discloses it |
| **window / bounds** | Recognized as a *keyword name only*; no data shape. `Operator.needs_window: bool` (`operators.py:64`); every `needs_window` op is `in_core=False` (`operators.py:197-200`); the `window=` kwarg is parsed then immediately refused without ever being stored (`planner.py:1866-1874`) |
| **offset** | `n: int`, default 1 — the only ordered-expression parameter with a real value shape. Parsed `planner.py:1849-1856`; threaded `planner.py:2531`; used `engine.py:258`, `engine.py:300-301` |
| **reset / within / step** | **No representation in code.** Documented as language in `docs/frame_ql_language.md:559-563` (`reset = year`, `step = year`) and given a clarification rule at `docs/frame_ql_language.md:980-985`, but `grep` over `packages/columna-core/src/columna_core/` finds no `reset`/`within`/`step` scan parameter. `_scan_call` accepts exactly `n=`, `by=`, `window=` and refuses anything else (`planner.py:1875-1877`) |

**Fields with NO current representation:** peer domain (declared), direction, tie rule, window bounds, reset, within, step. Only *order key* and *offset* have data shapes — and order key has **two incompatible ones**.

Additional structural fact: `MeasureShape.family` is explicitly `member NAMES only — no order_by` (`projection.py:47`). The planner's whole view of the model therefore **cannot see** an ordered reducer's order key; only the engine can (`engine.py:322`). Consequence: `FamilyMember.order_by` is never validated against `orderable_levels()` — `FAMILY { last ORDER category }` publishes fine (`tests/test_p05b0_data_identity.py:313`, `tests/test_relate_triad.py:60-61`) while `cumsum(..., by='category')` would be refused `order_not_governed`. Two order regimes, two governance standards.

---

#### C. Answers

##### 1. Where does `order_by` live, and its data shape?

Three unrelated things share the name; none of them is a shared order contract.

1. **Family-member declaration** — `FamilyMember.order_by: Optional[str]` (`model.py:164`), a bare level name, syntax `<agg> ... [ORDER <level>]` (`parser.py:476`, `parser.py:481-484`). This is the order key for `first`/`last` **only**. Engine-only consumer (`engine.py:322-324`). Dropped from the planner projection (`projection.py:47`).
2. **Scan order axis** — not stored anywhere; computed per query by `Planner.plan_order_axis(scan_op, measure, anchor, by=None) -> str` (`planner.py:293-368`) and passed as a kwarg `order_axis=` (`planner.py:2530-2535` → `engine.py:259`). Surface input is `by='<level>'`, a quoted string (`planner.py:1857-1863`).
3. **Statement-level output ordering** — `Statement.order_by: list[OrderKey]`, `OrderKey(column: str, descending: bool = False)` (`envelope.py:66-69`, `envelope.py:87`), parsed `envelope.py:263-280`, applied post-assembly `planner.py:961-966`, `planner.py:980-982`.

No inner ordered expression reads (3): `_apply_output_clauses` (`planner.py:968-991`) runs after the frame exists, and inner order comes only from `plan_order_axis`/`fam.order_by`. **The ruling's §9 no-ambient-inheritance requirement already holds by construction** — but by accident of layering, not by a declared rule.

##### 2. Are `first`/`last` classified as measure-family reducers? What breaks?

Yes, in four places:
- `operators.py:166-169` — `kind=REDUCER`.
- `specs/frameql_capabilities.toml:145` / `:155` — `category = "reducer"`, `standing = "ratified"` (the only ordered ops with `ratified` standing; all scans are `proposed`).
- `core_profile.toml:61-66` — listed in the *"reducers the profile undertakes to execute"* block.
- **The load-bearing classification site: `parser.py:686-692`** — publish-time validation:
  ```
  if op.kind != REDUCER:
      errs.append(f"measure '{meas.name}': operator '{op_name}' is a {op.kind}, not a reducer
                  — only reducers found families ...")
  ```
  Only `kind == REDUCER` operators may be family members. This is the gate the demo exercises (`demos/operator_umbrella_demo.py:134-138`).

If `first`/`last` stop being reducers, these break:
- **Publish** — every manifold declaring `FAMILY { last ORDER day }` fails at `parser.py:688`. That is the entire stock/level idiom (`tests/test_pin_admissibility.py:48`, `tests/test_case_demo_inc2.py:25`, `tests/test_assert_retirement.py:99`, `tests/test_p05b0_data_identity.py:313,489`, `tests/test_relate_triad.py:60-61`).
- **Execution dispatch** — `engine.resolve` routes on `op.witness` (`engine.py:243-246`); a non-reducer never reaches `_deliver_and_transport_monoid`, so `arg_max` delivery, the `(value, order_key)` witness, and its null-exclusion rule (`engine.py:336-341`) become unreachable.
- **B-anchor crossing law** — `planner.py:2038` gates on `sig.kind == "reducer" and sig.is_monoid`. `last` is the *named remedy* for a blocked `sum` across time (`docs/frame_ql_language.md:961`, `:1451`); if `last` leaves the reducer kind, both the crossing check and the refusal's advice lose their subject.
- **`_family_member_clarify`** — the family-member offer list (`planner.py:2155`) and default-family sugar (`planner.py:2549-2552`) enumerate `meas.family`, which would no longer contain `last`.
- **Signature typecheck** — `signature_ok` is applied only to family members (`parser.py:693-696`).
- **Registry/profile/status projections** — `capability_authority.measure_build` (`docs/tools/capability_authority.py:96-120`) measures by registry membership + `in_core`; `docs/frame_ql_build_status.md:93-94` currently reports `first`/`last` as `executes / executes / conforms`.

##### 3. Any windowing/frame machinery? Is `last` a sort+take?

**No frame machinery exists.** The only `Operator` field naming a frame is `needs_window: bool` (`operators.py:64`) — a boolean, not bounds — and it is a *refusal marker*: every operator carrying it is `in_core=False` (`operators.py:197-200`), and supplying `window=` is refused before any value is read (`planner.py:1868-1874`). There is no frame type, no bound representation, no `preceding/following`, no `range`/`rows` distinction anywhere in `columna-core`.

The closest thing to a frame is `expr.over(partition)` in the scan path (`engine.py:301`) — a partition, applied to a whole-partition cumulative/shift, with no bounds.

`last` is **not** a sort+take at the delivery boundary — it is a pushed-down `arg_max(value, order_key)` aggregate plus a `max(order_key)` witness column (`engine.py:328-329`). But it **is** a sort+take at the *combine* boundary: transporting/regrouping the witness uses `pl.col("_value").sort_by("_order").last()` (`engine.py:769`, `.first()` at `:772`). So the same operation has two mechanisms with two independent tie behaviours.

##### 4. Could one shared semantic descriptor cover all seven?

Yes — nothing forces one mechanism, because the three realization mechanisms are already dispatched off *separate* fields, not off the order information:
- `Operator.kind` routes reducer/scan/map (`operators.py:11-14`, `planner.py:1832`);
- `Operator.witness` routes reducer mechanics (`engine.py:238-246`);
- `Operator.scan_impl` is the engine's scan dispatch tag (`engine.py:299-301`).

A descriptor carrying only *semantics* (peer domain, key, direction, ties, frame, offset, reset) would sit beside these, and each of `arg_max` delivery / `over(partition)` polars / a future window path could consume the subset it needs. `needs_order` / `needs_window` (`operators.py:63-64`) are already the degenerate, boolean-typed version of exactly this idea.

Fields such a descriptor needs **that do not exist today**:
- **peer/partition domain as a declared value** — today it is a derived list computed inside the engine (`engine.py:296`) and *invisible* to the planner for ordered reducers.
- **order key as a list, not a scalar** — both current shapes are a single `str` (`model.py:164`, `plan_order_axis -> str` at `planner.py:293`). No secondary key can be expressed, which is exactly what the ruling's §7 "governed secondary key" requires.
- **direction** — no field anywhere; currently smuggled into operator identity (`argmax` vs `argmin`) and into a Polars sort default (`engine.py:297`).
- **tie rule** — no field, no vocabulary, no refusal code.
- **frame bounds** — `needs_window` is a bool; no bound type exists.
- **reset / within / step** — documented (`docs/frame_ql_language.md:559-563`) but with zero code representation.
- **a completed-contract carrier for canonicalization** — today the only externalization is a prose caveat string, `f"scan {scan_op} over order '{order_axis}'" + f" within {partition}"` (`engine.py:306-308`) and a trace line (`engine.py:303-305`). Ordered *reducers* emit no order disclosure at all. `Statement.render_canonical` (`envelope.py:90-116`) re-emits only surface text and cannot show a completed order contract. `describe.py:108` exposes only `needs_order`/`needs_window` booleans.
- **a shared home** — `MeasureShape` deliberately excludes `order_by` (`projection.py:47`), so today there is no single object the planner and engine both see that could hold the descriptor.

##### 5. Is tie behaviour defined anywhere?

**For ordered expressions: nowhere. Purely emergent, at three separate layers with three different mechanisms.**
- Delivery: whatever DuckDB's `arg_max`/`arg_min` does (`engine.py:328-329`).
- Combine/transport: Polars sort stability via `sort_by("_order").last()/.first()` (`engine.py:769-773`).
- Scans: Polars `frame.sort(...)` stability (`engine.py:297`).

Repo-wide grep for `tie|ties|tiebreak` across `docs/`, `packages/columna-core/src/`, and `specs/frameql_capabilities.toml` finds tie rules **only** in three unrelated places:
- **Output frame** — `docs/frame_ql_language.md:825`: *"Ties break on the remaining `ORDER BY` columns."* Declared, and about `ORDER BY`/`LIMIT PER`, not about `last`. The implementation is `planner.py:961-966` (`nulls_last=True` explicitly set, with the comment at `:962-964` flagging it as *"A deliberate default, FLAGGED for Huayin — not a leaked rule"*).
- **FACE `assign`** — the one place a tie is *adjudicated fail-closed*: `adjudication.py:644` ("yields a UNIQUE TOP per member set (no tie-at-top). A tie fails closed"), raising `FaceContradiction` at `adjudication.py:708`; declared syntax `ASSIGN BY <measure> ORDER MIN|MAX`, **mandatory, no default** (`parser.py:299-318`), documented `docs/frame_ql_language.md:1042`.
- **Fixture authoring note** — `docs/tools/manual_fixtures/manual_world.py:43`.

So the codebase already contains a *precedent* for a declared, mandatory, fail-closed order direction + tie rule (FACE ASSIGN), and it is applied to face allocation — not to `first`/`last`/scans, where the ruling says it is meaning-bearing.


---

## 3.7 Manifold authoring + authority reconciliation

*Inspector `agent-a9edf77e5ac290157` · primary target doc: `frameql_vnext_authority_reconciliation_v0_1.md`*

Findings below. Read-only; nothing modified.

---

### SUBJECT A — MANIFOLD AUTHORING

#### A.0 Where "authoring" actually lives (three authorities, not one)

| Layer | Artifact | Location |
|---|---|---|
| **Governed authoring** (upstream authority) | `Manifold` / `Declaration(kind,name,body)` + `GovernedPublicationArtifact` | `/data/repos/978ea3c9feee4ad79341d42517782efd/manifold-agent/src/manifold_agent/manifold.py:38-91`, `.../publication.py:1-60` |
| **Publication → engine lowering** (K0 compiler) | `compile_k0` → `.cml` text | `packages/columna-core/src/columna_core/compiler/compile.py:21,42-101`, `.../compiler/emit.py:14,101-128` |
| **Engine artifact** (`.cml` grammar) | `parse_manifold` → `model.Manifold` | `packages/columna-core/src/columna_core/parser.py:9-29`, `.../model.py:171-215` |

Sibling repos **both exist locally**: `/data/repos/978ea3c9feee4ad79341d42517782efd/manifold-agent` (HEAD `d9ea705`) and `/data/repos/978ea3c9feee4ad79341d42517782efd/columna-studio` (HEAD `244fd34`, "Studio emits an immutable governed publication artifact"). Also `manifold-eval`, `gatework`. There is **no** authoring surface under `columna/apps/` or `columna/services/` — the only in-repo `.cml` touchers are generators (`apps/website/scripts/gen_grammar.py`, `scripts/check_purged_grammar.py`).

Critical asymmetry for every judgement below: `manifold-agent`'s declaration vocabulary is **richer** than the `.cml` it lowers to, and K0's emit scope is narrower than both — `compile.py:14` (emit.py): *"K0 EMITS EXACTLY: SOURCE_MANIFOLD, UNIVERSE (unrestricted), LEVEL (base), MEASURE (+ FAMILY)"*, and `compile.py:91-101` refuses `relationship`/`hierarchy`/`attribute` outright.

---

#### A.1 Canonical family identity formed by an analytical law — **PARTIALLY REPRESENTABLE**

Evidence:
- `.cml` mints family identity by **operator name against a home table**, not by a law expression: `parser.py:25-28`, `parser.py:440-484`. A `FamilyMember` is `agg` + `BAnchor` + optional `order_by` (`model.py:153-169`). The identity carried is `(measure_name, member_name)` — `planner.py:4` "canonical (measure.member) @ anchor atoms".
- The law-ish content that does exist: `pre_expr` (per-row pre-agg, `model.py:176`) + the operator registry's algebraic properties (`operators.py:47-67`: `kind`, `witness`, `is_monoid`, `linear`, `accepts`, `out_rule`, `re_entrant`).
- Upstream, `manifold-agent` is closer: `REQUIRED_KEYS["measure"] = ("value_type", "root_member")` and `REQUIRED_KEYS["member"] = ("measure", "anchor", "universe")` (`validate.py:84-85`). A member **is** the (measure × anchor × universe) triple — this is much nearer the vNext "law + inner anchor" identity than `.cml`'s bare `agg` token.
- But the reducer itself is deliberately **opaque**: `validate.py:121-126` — *"`default_reduction` … OPAQUE here — the reducer vocabulary is the engine's, so the lowerer validates the value and the manifold only its PLACEMENT."* And the physical reducer is separately `root_evaluator` on the binding (`mapping.py:41-50`).

So `mean(revenue@order)` as a **family** can be declared (measure `mean_revenue` + member with `anchor=order`), but there is **no structure that says the family identity IS that law**: the engine artifact reduces it to `family = {"mean": FamilyMember(...)}` keyed by operator spelling.

Nothing needs to move authority: **this belongs to the Manifold**, and the governed-authoring layer already has 80% of the shape. What is missing is at the *lowering/`.cml`* level.

#### A.2 Constitutive inner anchor as part of family identity — **PARTIALLY (governed layer) / NOT (engine layer)**

- **Governed layer: representable.** `member` requires `anchor` (`validate.py:85`), and the compiler input model carries it: `MemberRealization(measure_ref, member_ref, universe_ref, anchor_ref, endpoint, root_evaluator)` — `compiler/inputs.py:163-176`.
- **Engine layer: not representable.** `FamilyMember` has **no inner-anchor field** (`model.py:153-169`); `MeasureColumn` has one universe + one `home_table` + `m_anchor` (missingness, not analytical input anchor) — `model.py:171-192`. K0's emit drops `anchor_ref` on the floor: `emit.py:101-128` emits only `MEASURE … ON <u> FROM <t> TYPE … VALUE … FAMILY { … }`.
- The inner anchor exists **only as a query-time pin** (`E @ {A}`), never as declared identity: `envelope.py:17`, `planner.py:683`, `planner.py:783-791`. When a reduction has no pinned input anchor the engine *clarifies* (`disclosure.py:241` `input_anchor_ambiguous`) or discloses (`disclosure_wire.py:125` `unconfirmed_assumption → input_anchor`).
- Note `MeasureColumn.m_anchor` (`model.py:187`) is **not** this — it is MCAR/MAR/MNAR missingness structure. Do not confuse the two names.

Verdict: **the constitutive inner anchor survives to the publication artifact and dies at the `.cml` boundary.**

#### A.3 Governed default completion (a source's default law) — **REPRESENTABLE at the governed layer; NOT carried to `.cml`; per-movement/direction NOT representable anywhere**

- The field **already exists and is named**: `KIND_ONLY_CLAUSES = {"fill_rule": "measure", "default_reduction": "measure"}` — `manifold-agent/src/manifold_agent/validate.py:127`, doctrine at `:121-126` ("the governed measure's default reduction family (the lawful default reducer `sum`, `count`, `last`, …) … Persisted so the lowering never invents it (columna#150, P0(a))").
- It is a **single scalar per measure**. There is no per-lineage, per-direction, or per-movement variant: `hierarchy` carries `direction ∈ {rollup, drilldown}` (`validate.py:87`, `ENUMS["direction"]:104`) but `default_reduction` cannot be keyed by it.
- `default_reduction` has **zero consumers in columna**: grep across `packages/` returns only `root_member`/`root_evaluator` hits (compiler tests + `compiler/inputs.py:176`). The compiler never reads it; `emit.py` never emits it. There is no `.cml` clause for it.
- The nearest `.cml` analogue is the **default member** picked mechanically at plan time: `planner.py:1899` `mem = mem or next(iter(self.m.measures[m].family))` — i.e. *insertion order of the FAMILY block*, which is exactly the "invented default" the governed layer was trying to prevent.

Verdict: **partially representable** (measure-scoped only, and unwired); **per-movement/direction: not representable**.

#### A.4 Semantic type capabilities (beyond the current TYPE vocabulary) — **NOT REPRESENTABLE; and this is NOT the Manifold's authority**

- `TYPE` is a closed scalar vocabulary of Polars dtypes: `types.py:24-36` (`DTYPES`), classes at `:39-43`. Validated since P1-18: `parser.py:505-509`; default `Float64` at `parser.py:509` with the open question flagged at `parser.py:503-505`.
- The **only** capability-bearing type today is the parametric sketch: `types.py:52-64` (`HLLSketch(p)`; precision is part of type identity) + `dtype_in` sketch-awareness at `:76-84`. Capability is expressed **not on the type** but on the operator's `accepts`/`out_rule` (`operators.py:63-66`, entries at `:155-162`).
- There is no attribute/method/subscription surface anywhere: no `E.attr`, no `E[key]`. `[]` is only paren-depth bookkeeping in `parser.py:361-365`.
- Governed layer is thinner still: `value_type` is a *string* from a coarser vocabulary (`validate.py:76,84`; `compile.py:70,142` refuses an unmapped `value_type` rather than guessing).

**Authority:** the reconciliation doc puts this in **Columna Data Types**, above Frame-QL and beside the Manifold (`frameql_vnext_authority_reconciliation_v0_1.md:44-56`). The Manifold should *reference* type capability, not define it. Today the only place capability is expressible is `operators.REGISTRY` — a **capability-registry** concern.

#### A.5 Standing distinctions (existence / placement / eligibility / support) — **NOT REPRESENTABLE as distinctions; one conflated field exists**

- The single authored carrier is `FILL_RULES = {"zero","unknown","undefined"}` — `parser.py:51-53`, clause parsed at `parser.py:430-438`, stored `MeasureColumn.fill_rule` (`model.py:180`). Mirrored in the governed layer at `validate.py:110` with identical values.
- The second carrier is universe `BASIS ∈ {events, spine, product, registry}` — `parser.py:49-50,188-194`; `Universe.basis` (`model.py:49`), rendered as prose `absence_semantics()` (`describe.py:65-69`).
- These are exactly the "one enum carrying several jurisdictions" the amendment names (`frameql_vnext_authority_reconciliation_v0_1.md:409-424`; R4 amendment §2.1 A–D at `frameql_vnext_r4_standing_amendment_v0_2.md:143-210`).
- **Placement** has no representation at all. **Eligibility** vs **support** are indistinguishable: both land as `undeclared_absence` (`disclosure.py:59`) or a `FILL_RULES` disposition.
- `m_anchor` (`model.py:187`, `parser.py:486-488`) records missingness *mechanism* (MCAR/MAR/MNAR) — adjacent, but it is a statistical mechanism, not a standing layer.
- Notably **`fill_rule` never crosses the wire** — neither `describe_manifold` (`tools.py:187-244`) nor `describe_measure` (`tools.py:245-283`) emits it; only its query-time *consequence* codes do (`disclosure_wire.py:117-120`). A consumer cannot read a measure's declared standing policy from any tool.

Verdict: **not representable.** Belongs jointly to the Manifold (the declared law) and to Frame-QL language law (the predicates `exists/eligible/supported/missing`, `frameql_vnext_r4_standing_amendment_v0_2.md:661-713`).

#### A.6 Governed default order / ordered-expression completion — **PARTIALLY: one field of ~seven**

The `.cml` **does** have a governed per-member order clause, which is more than the docs assume:
- `parser.py:476` — `(\w+)\s*(?:BLOCKED\s*\{…\})?\s*(?:ORDER\s+([\w.]+))?` → `parser.py:481,484`, stored as `FamilyMember.order_by` (`model.py:164`, *"for ORDERED operators (last/first): the level to order by"*), and it **does** reach the wire: `tools.py:263` `member_anchors[member]["order_by"]`.

Against the vNext ordered contract (`frameql_language_vnext_working_draft_v0_3.md:1540-1550`; `operators.py:63-65`):

| Contract field | Representation today |
|---|---|
| operand | yes (`pre_expr`, member) |
| **order key/axis** | **yes** — `FamilyMember.order_by` (`model.py:164`); for scans derived at plan time by `plan_order_axis` (`planner.py:293-320`) |
| peer / partition domain | **no declaration** — derived mechanically: `partition = [d for d in target if d != order_axis]` (`engine.py:296`) |
| **direction** | **NO** — the grammar is `ORDER <level>`, no ASC/DESC (`parser.py:476`). Direction is implicit in the operator (`combine="argmax"` for `last`, `"argmin"` for `first`, `operators.py:166-169`) |
| tie semantics | **NO** — nothing anywhere; engine sorts and takes `.last()`/`.first()` (`engine.py:769-772`) |
| window / offset | **NO** in the Manifold — query-only `window=` kwarg, and every windowed op is `in_core=False` (`operators.py:203-208`; `planner.py:1859-1871`) |
| reset / step | **NO** |

`plan_order_axis` is the one place a *governed* order is adjudicated, and P1-24 already implements the O1-shaped rule — one governed order → proceed; several → `order_axis_ambiguous`; none → `order_not_governed` (`planner.py:299-320`). That is O1-B machinery already shipped for scans, but the governed order set is `orderable_levels()` (admitted temporal lineages) — i.e. derived from hierarchy admission, **not authored as a default-order declaration**.

Verdict: **partially**. Axis: yes. Direction/tie/peer/window: no. Note the direction gap is genuinely load-bearing — `Face.order` (`model.py:250`, `FACE_ORDERS`) proves the authoring language *can* carry a direction token; it just isn't wired to ordered members.

#### A.7 A named non-family expression — **PARTIALLY (accidentally), with a real trap**

- `DERIVED <name> = <formula> [AT <level>] [FAMILY { … FERTILE { … } }]` — `parser.py:29,396-417`.
- **A `DERIVED` with an empty/absent FAMILY block is exactly a named non-family expression**: `model.py:213` — *"member-name → FamilyMember (each with a License); **empty = denotation-only, no travel**"*. Polarity is positive/closed-by-default: `planner.py:1929-1931` — *"DERIVED FERTILE — POSITIVE. Closed by default … No declaration ⇒ no permission."* So a name that mints **no** family identity is representable today.
- **The trap:** the name still enters the same namespace and the same resolution path as a measure family (`planner.py:1897-1900` resolves `m in self.m.derived` by expanding the formula), and `describe_manifold` emits `derived` beside `measures` (`tools.py:210`). There is no *kind* tag distinguishing "governed named non-family expression" from "derived measure family" — the distinction is inferred from an empty dict.
- The governed layer has **no kind for it at all**: `DECLARATION_KINDS` (`manifold-agent/manifold.py:38-52`) has `measure, member, anchor, universe, relationship, boundary, hierarchy, crosswalk, attribute` — no derived/expression kind. So a named non-family expression **cannot be published**; it can only exist in a hand-written `.cml`.
- The negative boundaries the docs want are already correct in-engine: `AS` alias (`planner.py:766-771`) and `WITH` macro (`planner.py:798`, "the canonical form carries no WITH") mint nothing durable.

Verdict: **partially representable in `.cml`; not representable in the governed publication.**

---

#### A.8 Summary table

| Capability | Governed publication (manifold-agent) | `.cml` / engine model | Right authority |
|---|---|---|---|
| Family identity by analytical law | partial (`measure`+`member` triple, reducer opaque) — `validate.py:84-85,121-126` | **no** (operator token keyed) — `parser.py:476-484` | Manifold |
| Constitutive inner anchor | **yes** (`member.anchor`) — `validate.py:85`, `inputs.py:163-176` | **no** — `model.py:153-169`; dropped by `emit.py:101-128` | Manifold |
| Governed default completion | partial (`default_reduction`, measure-scoped, unwired) — `validate.py:127` | **no** — default = FAMILY insertion order, `planner.py:1899` | Manifold |
| Per-movement/direction default | **no** — `validate.py:127` is one scalar | **no** | Manifold |
| Semantic type capabilities | **no** (`value_type` string) — `validate.py:76,84` | **no** (closed scalar `DTYPES`) — `types.py:24-36` | **Columna Data Types** + capability registry (`operators.py:47-67`), not the Manifold |
| Standing distinctions | **no** (one `fill_rule` enum) — `validate.py:110` | **no** (same enum) — `parser.py:51-53`; not even on the wire | Manifold (declaration) + Frame-QL language law (predicates) |
| Governed default order | **no** | **partial**: axis only — `parser.py:476`, `model.py:164`; no direction/tie/peer/window | Manifold |
| Named non-family expression | **no kind exists** — `manifold.py:38-52` | **partial**: `DERIVED` w/ empty FAMILY — `model.py:213`, `planner.py:1929-1931` | Manifold (needs a kind), boundary stated in Frame-QL law |

---

### SUBJECT B — WIRE AND OUTCOME

#### B.0 `CONTRACT_VERSION` and its bump rule

`CONTRACT_VERSION = "4"` — `packages/columna-core/src/columna_core/disclosure_wire.py:47`.

The bump rule is stated normatively in the version history, `disclosure_wire.py:23-45` and `:49-70`:

> *"THIS IS A BUMP, NOT AN ADDITION, because `freshness` **MOVED**. … That is a **changed value for an existing field on an unchanged utterance** — the canonical break-by-version case"* (`:28-31`)

Three operative rules, all in this file:
1. **Bump** = same utterance over same data yields a *different value for an existing field* (`:28-31`; `"1"→"2"` at `:60-70`: only the default column `name` changed).
2. **Bump** = row meaning / cardinality of an existing array changes (`"2"→"3"`, `:50-58`).
3. **No bump** = purely additive fields, *and* removals are permitted without a bump **while every consumer is in-tree** — the "in-tree consumers premise", `:71-99`, with an enumerated checklist at `:84-99`. Precedents: face payloads added at `:246-250` ("additive; contract_version stays 1"); `asserts` removed with no bump (`tools.py:198-201`).
4. Internal vocabulary integrity is explicitly *not* a wire change: `disclosure.py:458-459` — *"`no_result.reason` remains an extensible reason string in shape, and CONTRACT_VERSION stays '3'."*

`CONTRACT_VERSION` is **global** — one literal stamped on `query`/`check`/`explain`/`describe`/`list_manifolds`/`frame_ql_grammar` (`tools.py:183,240,275,286,292,378,428`), so any bump moves all of them (`disclosure_wire.py:57-58`). Literal consumers that must be swept on a bump: `scripts/assert_demo_play.py`, `.github/workflows/ci.yml` (`:95-99`).

#### B.1 The contract's current assumptions

**Fill rule.** Not on the wire as a declaration; only as four *dispositions* in the closed `CATEGORY_TABLE` — `disclosure_wire.py:116-120`: `declared_fill→filled` (IMMATERIAL), `unknown_absence→unknown` (MATERIAL), `out_of_population→out_of_population` (IMMATERIAL), `undeclared_absence→undeclared_absence` (MATERIAL). Engine-side definitions `disclosure.py:53-59`. The assumption baked in: **absence is one axis with four values, and materiality is a property of the fill rule.** No `describe` tool emits `fill_rule` (verified: zero hits in `columna-server/src/`).

**NULL.** No wire concept. `_values` serializes whatever Polars holds (`disclosure_wire.py:264-275`); `nulls_last=True` in frame sort (`planner.py:966`). `is_null` is not ratified anywhere. There is no field distinguishing carrier-null from analytical missing.

**Missing.** Only via the absence caveat codes above. No per-row/per-cell standing marker: a value row is `{dims…, "value": v}` (`disclosure_wire.py:270-273`) — **there is no slot on a row for standing.**

**Input anchor.** Two channels: served-with-disclosure `unconfirmed_assumption → code "input_anchor"`, MATERIAL (`disclosure_wire.py:125`; produced `engine.py:1232-1234`); and no-result reasons `input_anchor_ambiguous` (CLARIFY/AMBIGUOUS, `disclosure.py:241`), `redundant_pin` (`:245`), `pin_coarser_than_output` (REFUSE, `:385`). Frame-level anchor is `frame.anchor: [levels]` (`disclosure_wire.py:299`).

**Order.** The wire carries **output** order only, implicitly as row sequence — `ORDER BY <col> [ASC|DESC]` (`envelope.py:11,263-271`), applied in `planner.py:961-990`. **No field on the wire states an ordered expression's order contract**; `order_by` appears only in `describe_measure.member_anchors[m]["order_by"]` (`tools.py:263`), as a bare level name. Nothing conveys direction, tie rule, or peer domain.

**Canonical form.** Two distinct places. (a) The unaliased column **key** is the canonical expression — `wire_column` emits `cr.name` (`disclosure_wire.py:278`), produced at `planner.py:746-771` ("the canonical expression IS the identity"), and this is precisely what forced `"1"→"2"` (`disclosure_wire.py:60-70`). (b) `EXPLAIN` returns `"desugared": d.render_canonical()` (`frameql.py:109`, `envelope.py:90-112`) — WITH inlined, `@ {…}` braced, `*` product separator (`planner.py:783-800`).

**Reason codes.** `no_result = {kind, discriminator, reason, detail, alternatives[]}` (`disclosure_wire.py:255-262`). `kind ∈ {clarify, refuse, error}`; the mapping `reason → (kind, discriminator, jurisdiction)` is the closed table `REASON_OUTCOME` (`disclosure.py:227+`), fail-closed since `outcome_for` raises on an unregistered reason (`disclosure.py:447-466`). Jurisdiction is `language | analytical | realization` (`disclosure.py:479-487`) and is **not emitted on the wire**. Alternatives are re-encoded verbatim with an optional derived `apply:{universe}` (`disclosure_wire.py:229-244`).

**Annotation fields.** Caveat: `{code, materiality, severity, category, detail, remedy, source, rel_error}` plus conditional `memberships_unrepresented` / `reconciliation` (`disclosure_wire.py:196-224`). Two channels per column and per frame: `disclosures` (semantic, call-invariant) and `mechanical` (observational, always present, possibly empty) — `disclosure_wire.py:279-285`, `disclosure.py:125-146`. Column: `{name, status, population, disclosures, mechanical, value|values|no_result}` (`disclosure_wire.py:277-289`). Frame: `{contract_version, outcome, frame:{anchor, universe, rollup_severity, disclosures, mechanical}, columns, executed[, fetches_delta]}` (`disclosure_wire.py:294-313`). Outcome derivation: no-result mood dominates, else **materiality** (not severity) decides `disclose` vs `serve` (`disclosure_wire.py:284-292`). Materiality vocabulary is fixed (`disclosure_wire.py:102-104`); `RESERVED_CODES` holds emit-capable-but-unproduced codes so the vocabulary stays closed (`disclosure_wire.py:139-146`).

#### B.2 Foreseeable vNext changes, classified

##### (a) Semantic ADDITIONS that fit contract "4"

| Change | Why it fits | Field / evidence |
|---|---|---|
| New standing/ordered **reason codes** (`order_not_governed`, `order_axis_ambiguous`, `placement_unsupported`, `eligibility_unsupported`) | `no_result.reason` is an open string in shape; adding a `REASON_OUTCOME` row is internal integrity, precedent explicit | `disclosure.py:458-459`; `plan_order_axis` already produces two of these, `planner.py:313-319` |
| New **caveat codes** drawn from `RESERVED_CODES` | reserved precisely so the vocabulary stays closed end-to-end while producers land later | `disclosure_wire.py:139-146` |
| Emitting `fill_rule` / `default_reduction` / an order contract on `describe_measure` | describe additions have repeatedly been additive-without-bump | `tools.py:246-250` precedent; `disclosure_wire.py:71-99` in-tree premise |
| Exposing declaration-level **order contract** fields (direction, tie, peer) beside the existing `member_anchors[…]["order_by"]` | additive keys on an existing object; existing key keeps its value | `tools.py:259-266` |
| Marking `first`/`last` as ordered-expression *category* rather than reducer, in `describe_measure.signatures[m].operator` | `operator_properties` is a describe projection; category is new information, not a changed existing value — **provided `reducer_kind` keeps emitting `"reducer"`** | `tools.py:264,269`; `operators.py:166-169` |
| Adding `jurisdiction` to `no_result` | the field exists internally and is not currently emitted | `disclosure.py:479-487` |

##### (b) Changes that FORCE a wire-VERSION bump

| Change | The field that forces it | Evidence |
|---|---|---|
| **Splitting the fill rule into standing layers** (existence / placement / eligibility / support) | `disclosures[].code` — an utterance that today emits `undeclared_absence` would emit a *different code*, i.e. a changed value for an existing field on an unchanged utterance | `disclosure_wire.py:116-120` vs rule at `:28-31`. Gate S1 (`frameql_vnext_authority_reconciliation_v0_1.md:775-783`) predicts exactly this |
| **Any materiality reclassification** of an absence code (e.g. `undeclared_absence` MATERIAL → IMMATERIAL) | `disclosures[].materiality` → cascades to `outcome` via `derive_outcome` | `disclosure_wire.py:284-292`; `CATEGORY_TABLE` is declared NORMATIVE, deviation needs sign-off, `disclosure_wire.py:16-17` |
| **Any change to canonical column naming** (e.g. `revenue.sum` → `sum(revenue @ {order})` after D1 dot-normalization) | `columns[].name` — this is the *literal* precedent that produced `"1"→"2"` | `disclosure_wire.py:60-70`; producer `planner.py:746-771` |
| **Ordered-shorthand completion surfacing in canonical form** (O1: "canonical form must expose the completion") | `explain.desugared` — a same-statement `EXPLAIN` returns different text | `frameql.py:109`, `envelope.py:90-112`; requirement at `frameql_vnext_authority_reconciliation_v0_1.md:359-370` and draft `:1671-1676` |
| **Per-row/per-cell standing** (a value row that says *why* it has no value) | row shape in `_values` is `{dims…, value}` — adding a standing key changes the meaning/shape of an existing array's rows, the `"2"→"3"` pattern | `disclosure_wire.py:264-275`; precedent `disclosure_wire.py:50-58` |
| **Reclassifying `first`/`last` in `reducer_kind`** (reducer → ordered) | `describe_measure.family.reducer_kind[m]` — an existing key returns a different string | `tools.py:264`; explicitly deferred by the reconciliation as gate O1, `frameql_vnext_authority_reconciliation_v0_1.md:401-411` |
| **Retiring analytical bracket filtering** | **no bump** — the form is unshipped (`parser.py:361-365` treats `[]` only as depth); zero wire fields. Confirming the reconciliation's "cheapest migration point" (`:295-303`) |

##### B.3 The sharp edge

The two changes most likely to be *mistaken* for additions are:
1. **`reducer_kind` for `first`/`last`** (`tools.py:264`) — a pure "semantic category" edit with no runtime behaviour change, which is exactly the shape the reconciliation calls safe (`:427-433` "The category change is semantic, not a claim that current code stopped working"), yet it changes an existing wire field's value under rule 1 (`disclosure_wire.py:28-31`).
2. **Standing layer split** — because `fill_rule` never crosses the wire, it *looks* like an internal-only change; but its four dispositions do cross, as `disclosures[].code`.

Everything else in the standing work can land additively as long as the existing four absence codes keep firing with their current codes and materialities.


---

## 3.8 Category-change blast radius (test surface)

*Inspector `agent-a661b7f7268642396` · primary target doc: `frameql_vnext_current_manual_migration_matrix_v0_1.md`*

### Frame-QL vNext — category-change blast radius

#### Totals

| Package | Collected tests |
|---|---|
| `packages/columna-core/tests` | **766** |
| `packages/columna-server/tests` | **309** |
| **total** | **1075** |

(collected read-only via `pytest --collect-only -q`; `def test_` counts are 525 core / 251 server — the delta is parametrization.)

The single authority everything below hangs off is `/data/repos/978ea3c9feee4ad79341d42517782efd/columna/packages/columna-core/src/columna_core/operators.py` (`REDUCER, SCAN, MAP = "reducer", "scan", "map"`, `REGISTRY`, `ALIASES`, `SERIES_REDUCERS`) and `/data/repos/978ea3c9feee4ad79341d42517782efd/columna/specs/frameql_capabilities.toml` (`category = "reducer" | "map" | "scan"`, `position = "series" | "predicate"`, `standing = "ratified" | "proposed"`).

---

#### A. Reducer / scan / map taxonomy and capability categories

| file::test | class |
|---|---|
| `/…/packages/columna-core/tests/test_generated_family_law.py::test_mean_has_a_law_address_without_becoming_a_monoid` — `assert REGISTRY["mean"].kind == "reducer"`, `is_monoid is False`, `set(ColumnEngine._SERIES_REDUCE) == set(SERIES_REDUCERS)` | semantic-law pin |
| `/…/packages/columna-core/tests/test_describe_extension.py::test_operator_properties_surfaces_registry_facts_not_mechanics` — `operator_properties(sig) == {"kind": "reducer", "is_monoid": …, "linear": …, "needs_order": …, "needs_window": …}` — the describe-surface *shape* of the taxonomy | profile-contract pin |
| `/…/packages/columna-core/tests/test_operator_umbrella.py::test_alias_table_is_the_single_surface_name_authority` — `not hasattr(Planner, "_INLINE_REDUCERS")`, `SERIES_REDUCERS <= set(REGISTRY)`, every alias target registered | implementation-detail pin |
| `/…/packages/columna-core/tests/test_operator_umbrella.py::test_check[*]` (parametrized over `demos/operator_umbrella_demo.py`, which imports `REGISTRY, REDUCER, SCAN, MAP` and does `Counter(op.kind for op in REGISTRY.values())`) | build-measurement pin |
| `/…/packages/columna-core/tests/test_fixture_drift.py::test_*` — `_EXPECTED_COUNTS` pins the exact check count each demo emits (99 total); the umbrella demo's kind-histogram is inside that count | build-measurement pin |
| `/…/docs/tools/capability_authority.py::main` (gate `capability-authority`) — `measure_build()` reads `REGISTRY` + `in_core` + `SERIES_REDUCERS`, `standing_exceeded()` reads `standing == "ratified"` | build-measurement pin |
| `/…/docs/tools/regen_capability_tables.py --check` (gate `capability-tables`) — `_SECTIONS = [("Reducers","reducer",None), ("Maps — series position","map","series"), ("Predicate position","map","predicate"), ("Scans","scan",None)]`; any recategorization rewrites four committed manuals and fails `--check` byte-diff | profile-contract pin |
| `/…/docs/tools/check_manual_frameql.py::operator_reference_drift` (gate `manual-frameql`) — resolves Appendix A names through `CA.spelling_index(caps)`; a name whose capability id/category moves is reported as an unknown capability | profile-contract pin |

`docs/tools/capability_authority.py::profile_errors` / `build_deltas` / the `platform extends core` check are the **profile promises**: `specs/profiles/core_profile.toml` + `platform_profile.toml` name capability ids; renaming or recategorizing a capability makes the profile "realize a capability the canonical authority does not have" → hard `SystemExit`.

---

#### B. `first` / `last` as reducers / family members

`first`/`last` are `Operator(..., REDUCER, ORDERED_W, True, combine="argmax"/"argmin", needs_order=True)` and are declared as measure-family founders via `FAMILY { last ORDER day }`. If they cease to be measure-family reducers, the following break — several at **fixture parse time**, i.e. whole-file collection errors, not single assertions.

| file::test | class |
|---|---|
| `/…/packages/columna-core/tests/test_generated_family_law.py::test_every_laundering_spelling_refuses_identically[inline-lawful-kin]` / `[carrier-unary]` / `[carrier-scalar]` / `[carrier-scan]` — `sum(on_hand.last@day)`, `sum((-on_hand.last)@day)`, `sum((on_hand.last * 2)@day)`, `sum(cumsum(on_hand.last)@day)` | semantic-law pin |
| `/…/packages/columna-core/tests/test_generated_family_law.py::test_every_refusal_names_a_lawful_neighbour[*]`, `::test_no_laundering_spelling_can_return_the_wrong_number[*]`, `::test_explain_predicts_the_refusal_without_touching_data[*]` (same `_LAUNDERING` table) | semantic-law pin |
| `/…/packages/columna-core/tests/test_generated_family_law.py::test_other_reducers_over_the_stock_remain_lawful[min/max/mean]` — `f"{reducer}(on_hand.last@day)"` | semantic-law pin |
| `/…/packages/columna-core/tests/test_inline_reduction.py::test_blocked_reduction_refuses_through_every_carrier[sum(level.last@day)]` and the three carrier rows | semantic-law pin |
| `/…/packages/columna-server/tests/test_mcp_server.py::test_describe_measure_family_triple` — `set(d["family"]["members"]) == {"sum", "last"}`, `d["member_anchors"]["last"]["order_by"] == "day"` | profile-contract pin |
| `/…/packages/columna-server/tests/test_mcp_server.py::test_generated_blocked_reduction_refuses_on_the_wire` — `SELECT sum(level.last) AS inv AT {cal.month, category}` | semantic-law pin |
| `/…/packages/columna-core/tests/test_k0_compiler.py::test_excluded_reducers_refuse_with_a_stated_reason[last-ORDER]` and `[first-ORDER]` — refusal reason text must contain `"ORDER"` | semantic-law pin |
| `/…/packages/columna-core/tests/test_k0_compiler.py::test_the_allow_list_is_exactly_the_ratified_four` — `K0_REDUCERS == frozenset({"sum","count","min","max"})` | profile-contract pin |
| `/…/packages/columna-core/tests/test_pin_admissibility.py` (module-level fixture `MEASURE stock … FAMILY { last ORDER day }`) — **all tests in file** | semantic-law pin |
| `/…/packages/columna-core/tests/test_relate_triad.py` (two `FAMILY {{ last ORDER category }}` measures) — **all tests in file** | semantic-law pin |
| `/…/packages/columna-core/tests/test_p05b0_data_identity.py` (`FAMILY { last ORDER category }`, `FAMILY { last ORDER day }`) — **all tests in file** | semantic-law pin |
| `/…/packages/columna-core/tests/test_assert_retirement.py` (`FAMILY { last ORDER day }` fixture) — **all tests in file** | historical compatibility pin (file's own subject is a retirement) |
| `/…/packages/columna-core/tests/test_case_demo_inc2.py` (`FAMILY { last ORDER day }`) — **all tests in file** | semantic-law pin |
| `/…/packages/columna-core/tests/fixtures/afternoon_world.py` (shared `on_hand … FAMILY { last … }`) → cascades into `test_generated_family_law.py`, `test_afternoon_page_gate.py`, `test_pin_verdict_truthfulness.py::test_a_prohibition_that_holds_under_every_member_still_outranks_the_ambiguity` | semantic-law pin |
| `/…/packages/columna-core/tests/test_afternoon_page_gate.py::test_beat_5_the_burn_refuses_with_no_values`, `::test_beat_5_never_returns_the_afternoons_wrong_number`, `::test_the_five_earn_the_verdicts_the_essay_claims[*]`, `::test_the_script_gate_certifies_the_same_five_statements` (+ `scripts/afternoon_five.py`) | semantic-law pin |
| `/…/packages/columna-core/tests/test_explicit_order_adjudication.py::*` — the whole "governed order standing" file rests on ordered reducers having a governed `ORDER` axis | semantic-law pin |
| `/…/docs/tools/capability_authority.py` + `regen_capability_tables.py --check` — `specs/frameql_capabilities.toml` rows `id = "last"` / `id = "first"` are `category = "reducer"`, `standing = "ratified"`; moving them rewrites the Reducers grid in all four manuals | profile-contract pin |

Also load-bearing fixtures (not tests, but they break collection): `/…/packages/columna-core/demos/locus_demo.py`, `coanchor_demo.py`, `holistic_demo.py`, `build_benchmark.py`, `/…/packages/columna-server/scripts/regen_warehouse.py`, `/…/packages/columna-server/src/columna_server/demo.py`, `/…/packages/columna-server/src/columna_server/recapture.py`.

---

#### C. Dotted member syntax (`revenue.sum`, `level.last`, `on_hand.sum`)

If dotted becomes compatibility-only, these still pass *behaviourally* but fail if the dotted form ceases to be the **canonical/keyed** spelling.

| file::test | class |
|---|---|
| `/…/packages/columna-core/tests/test_derivation.py::test_derived_dotted_member_reference_parses` | historical compatibility pin |
| `/…/packages/columna-core/tests/test_derivation.py::test_fertility_grammar_composes_with_dotted_head_and_at` — `DERIVED x = revenue / level.last AT day FAMILY { mean FERTILE { } }` | historical compatibility pin |
| `/…/packages/columna-core/tests/test_derivation.py::test_parsed_derived_over_family_plans_like_python_built`, `::test_parsed_derived_unknown_family_member_errors_classified` | semantic-law pin |
| `/…/packages/columna-core/tests/test_generated_family_law.py::test_every_laundering_spelling_refuses_identically[declared-member]` (`on_hand.sum`) and `[inline-blocked-kin]` (`sum(on_hand.sum@day)`) | semantic-law pin |
| `/…/packages/columna-core/tests/test_inline_reduction.py::test_blocked_reduction_refuses_through_every_carrier[level.sum]` and `[cumsum(level.sum)]` | semantic-law pin |
| `/…/packages/columna-core/tests/test_pin_verdict_truthfulness.py::test_the_family_member_menu_offers_only_lawful_readings`, `::test_every_offered_member_is_a_real_member`, `::test_several_lawful_members_clarify_and_offer_every_one_unranked` — the clarify **menu** is spelled in members | semantic-law pin |
| `/…/packages/columna-server/tests/test_mcp_server.py::test_generated_blocked_reduction_refuses_on_the_wire` — literal `sum(level.last)` on the wire | historical compatibility pin |
| `/…/docs/tools/regen_examples.py --check` (gate `regen-examples`) — `docs/frame_ql_language.md` §"Member access" states `revenue.sum → revenue.sum` (*"the framework does not rewrite the dot; the key is the expression"*); a compatibility-only dotted form that desugars changes the emitted key and the committed `frameql-output` blocks | historical compatibility pin |
| `/…/docs/tools/check_manual_frameql.py` (gate `manual-frameql`) — every `” ```frameql ”` example carrying a dotted member is executed and its disposition compared | profile-contract pin |
| `/…/apps/website/scripts/check_prose_coherence.py` (gate `prose-coherence`) — parse-only; breaks only if the dotted surface stops **parsing** | historical compatibility pin |

Additional dotted-carrying files whose fixtures/queries use it: `test_frameql_parse.py`, `test_expression_law.py`, `test_envelope_sugars.py`, `test_envelope_planner.py`, `test_connector_protocol.py`, `test_disclosure_wire.py`, `test_alignment_domain.py`, `test_p05a_execution_contract.py`, `packages/columna-server/tests/test_case_demo_trial.py`, `test_agent.py`, `test_provisioner.py`, `test_firstlight_governed_fixture.py`, `test_k0_governed_producer.py`.

---

#### D. Bracket forms (predicate filtering → value subscription)

**No test in either package exercises the bracket form.** The reassignment lands entirely on docs/gates:

| checker::site | class |
|---|---|
| `/…/docs/frame_ql_language.md` §6.7 `” ```frameql-roadmap ”` block `SELECT revenue[region = "east"] AS east_revenue …`, checked by `/…/docs/tools/check_manual_frameql.py` (gate `manual-frameql`) — `roadmap-without-mark` / `roadmap-but-shipped` failure modes | profile-contract pin |
| `/…/docs/frame_ql_language.md:215` "Bracket-filtered column references: `revenue[region = "east"]`" listed under *"Any other expression → no derivable identity, so you must supply `AS`"*; §2.8 "**The bracket filter** restricts a column reference to a subset of its domain … It differs from `WHERE` (§4.1)". Reassignment to value subscription contradicts both; caught by `check_manual_frameql.py` only if the naming law changes, otherwise it is silent prose drift | semantic-law pin (currently **unguarded** — flag this) |
| `/…/docs/frame_ql_revision_history.md:59` "**The bracket filter is not shipped.** … accepted by the statement [parser]" — and `/…/packages/columna-core/src/columna_core/planner.py:757` "A composite/nested/map/bracket expression is still REFUSED for a name" | historical compatibility pin |
| `/…/apps/website/scripts/check_prose_coherence.py` (gate `prose-coherence`) — parse-check over corpus blocks; a grammar change to `[...]` that alters `envelope.py`'s depth tracking (`if ch in "(["`) fails here | build-measurement pin |
| `/…/scripts/check_purged_grammar.py` (gate `purged-grammar`) — matches **only** `EDGE … -> … ALONG … VIA`. It will **not** catch a retired bracket form; if the predicate-bracket is purged, this class guard needs a new pattern | (no break; gap) |

---

#### E. WHERE behaviour and `filter_unsupported`

The current law is **`filter_unsupported` ⇒ (ERROR, None, REALIZATION)`** — a *build* fact, deliberately not analytical (`disclosure.py:252`). "WHERE stated as analytical restriction" inverts exactly this.

| file::test | class |
|---|---|
| `/…/packages/columna-core/tests/test_where_capability_gate.py::test_the_manifold_fact_and_the_build_fact_remain_distinct` — `jurisdiction_for("filter_unsupported") == "realization"` | semantic-law pin |
| `/…/packages/columna-core/tests/test_where_capability_gate.py::test_the_reason_is_specific_and_registered` — `outcome_for("filter_unsupported") == ("error", None)` | semantic-law pin |
| `/…/packages/columna-core/tests/test_where_capability_gate.py::test_a_joined_dimension_is_refused_at_plan_time` | semantic-law pin |
| `/…/packages/columna-core/tests/test_where_capability_gate.py::test_the_two_quote_spellings_of_one_literal_are_one_ask[>=]`/`[==]`, `::test_the_IN_repair_converges_on_quotes_too`, `::test_normalization_is_a_quote_swap_and_not_a_filtering_feature` | build-measurement pin |
| `/…/packages/columna-core/tests/test_where_capability_gate.py::test_plan_and_execution_agree_on_every_where_form` | semantic-law pin |
| `/…/packages/columna-core/tests/test_filter_jurisdiction.py::test_a_reachable_dimension_the_build_cannot_push_is_a_realization_gap` — `reason == "filter_unsupported" and jurisdiction_for(reason) == REALIZATION` | semantic-law pin |
| `/…/packages/columna-core/tests/test_filter_jurisdiction.py::test_the_three_asks_no_longer_share_a_reason`, `::test_a_declared_dimension_the_universe_cannot_reach_is_an_analytical_refusal`, `::test_a_predicate_naming_non_structure_is_a_language_failure[amount]`/`[zzz_not_a_name]` | semantic-law pin |
| `/…/packages/columna-core/tests/test_filter_jurisdiction.py::test_the_unexecutable_dimensions_are_described_not_offered`, `::test_every_named_remedy_dimension_is_at_least_analytically_lawful`, `::test_the_where_path_no_longer_clarifies` | semantic-law pin |
| `/…/packages/columna-core/tests/test_jurisdiction_seam.py::test_outcome_for_is_unchanged_for_existing_callers` — `outcome_for("filter_unsupported") == (ERROR, None)` | historical compatibility pin |
| `/…/packages/columna-core/tests/test_jurisdiction_seam.py::test_the_only_reason_level_inversions_are_the_ones_the_ledger_rows` — `_KNOWN_INVERSIONS = {}`; moving WHERE to ANALYTICAL/ERROR mints a new inversion and this goes red **by design** | semantic-law pin |
| `/…/packages/columna-core/tests/test_jurisdiction_seam.py::test_every_registered_reason_has_a_jurisdiction`, `::test_unruled_is_confined_to_the_reasons_the_architects_left_open`, `::test_no_analytical_reason_hides_in_the_error_umbrella` | semantic-law pin |
| `/…/packages/columna-core/tests/test_jurisdiction_inversion.py::test_the_re_reasoned_laws_are_registered_analytical_and_refuse[*]`, `::test_a_genuine_build_limit_is_left_alone` (`jurisdiction_for("filter_unsupported") == REALIZATION`), `::test_no_analytical_reason_hides_in_the_error_umbrella` | semantic-law pin |
| `/…/packages/columna-core/tests/test_canonical_conformance.py::test_where_is_macro_expanded`, `::test_no_binding_name_survives_into_where`, `::test_a_macro_shadowing_a_level_means_its_expansion_not_the_homonym`, `::test_a_free_macro_in_where_serves_exactly_as_the_hand_written_predicate`, `::test_having_is_not_expanded_by_law` | semantic-law pin |
| `/…/packages/columna-core/tests/test_plan_run_standing.py::*` — the shared plan/run predicate lives in `run_statement`'s pre-branch beside `_where_reachability` | semantic-law pin |
| `/…/packages/columna-server/tests/test_case_demo_recapture.py` (line 239 note: `unsupported`/`filter_unsupported` ride the transitional `error` mood) | historical compatibility pin |

---

#### F. Fill rules / absence vocabulary / disclosure severity

| file::test | class |
|---|---|
| `/…/packages/columna-core/tests/test_basis_absence.py::test_declared_zero_fills_with_an_immaterial_note` (`category == "declared_fill"`) | semantic-law pin |
| `…::test_declared_unknown_is_left_null_and_discloses_materially` (`unknown_absence`) | semantic-law pin |
| `…::test_undeclared_discloses_and_does_not_fill_even_on_events_basis` (`undeclared_absence`, detail `"no declared fill rule"`) | semantic-law pin |
| `…::test_declared_undefined_is_out_of_population_and_immaterial` | semantic-law pin |
| `…::test_basis_is_inert_for_absence_events_and_spine_behave_alike_when_undeclared` | semantic-law pin |
| `…::test_fill_clause_parses_onto_the_measure_and_is_optional`, `::test_a_bad_fill_rule_is_a_parse_error` (`fill_rule ∈ {zero, unknown, undefined, None}`) | implementation-detail pin |
| `…::test_single_column_frame_has_no_absence_edit`, `::test_basis_adjudication_still_mints_untestable_per_type` | semantic-law pin |
| `/…/packages/columna-core/tests/test_disclosure_wire.py::test_category_table_is_the_normative_mapping` — `code_for("b_anchor_crossing") == "blocked_reduction"`, `coverage → denominator_population`, `unconfirmed_assumption → input_anchor` | semantic-law pin |
| `…::test_default_materiality[*]`, `::test_approximation_materiality_is_rel_error_gated`, `::test_reserved_codes_present`, `::test_unknown_category_falls_back_to_other_immaterial` | semantic-law pin |
| `…::test_wire_caveat_full_fields_b_anchor` — `("blocked_reduction","material","critical")` byte-exact | historical compatibility pin |
| `…::test_wire_frame_banchor_served_with_material_critical_caveat`, `::test_outcome_serve_vs_disclose_is_materiality_driven`, `::test_derive_outcome_no_result_moods_dominate` | semantic-law pin |
| `/…/packages/columna-core/tests/test_disclosure_channels.py::test_the_mechanical_channel_cannot_change_the_mood`, `::test_served_from_cache_is_mechanical_not_semantic`, `::test_warm_is_never_quieter_than_fresh`, `::test_the_wire_carries_both_channels_always`, `::test_coverage_is_wired_material`, `::test_a_touch_shortfall_is_material` | semantic-law pin |
| `/…/packages/columna-core/tests/test_alignment_domain.py::test_zero_never_fills_a_divergence_gap`, `::test_eligible_but_unsupported_is_material`, `::test_ineligible_is_not_reported_as_a_support_gap` | semantic-law pin |
| `/…/packages/columna-core/tests/test_family_member_support.py::test_semantic_disclosure_parity_between_members`, `::test_all_value_family_members_share_one_support`, `::test_the_residual_is_not_representable` | semantic-law pin |
| `/…/packages/columna-server/tests/test_mcp_server.py::test_wire_shape_is_stable` (line 221 `_CAVEAT_KEYS`, line 233–235 `rollup_severity ∈ {none,info,caution,critical}`) | profile-contract pin |
| `/…/packages/columna-server/tests/test_case_demo_recapture.py` (line 207 `severity == "caution"`) | historical compatibility pin |

---

#### G. Canonical / desugared form strings

| file::test | class |
|---|---|
| `/…/packages/columna-core/tests/test_envelope_sugars.py::test_desugar_comma_anchor_to_star` — `"AT {product*region}" in d.render_canonical()` | semantic-law pin |
| `…::test_canonical_round_trips_and_is_idempotent` — canonical is a fixed point | semantic-law pin |
| `…::test_composite_input_anchor_desugars_mechanically` — `"avg(aov @ {day*store})" in star.render_canonical()` | semantic-law pin |
| `…::test_desugar_fills_alias_and_braces`, `::test_desugar_inlines_with`, `::test_bare_and_braced_input_anchor_identical`, `::test_unaliased_complex_expr_refused` | semantic-law pin |
| `/…/packages/columna-core/tests/test_envelope_parser.py` (line 136) `parse_statement(st.render_canonical()) == st`; (line 33) `*` canonical / comma accepted-on-input | semantic-law pin |
| `/…/packages/columna-core/tests/test_envelope_explain.py::test_desugared_is_the_consumed_artifact` — `ex["desugared"] == consumed` and `"avg(aov @ {day})" in ex["desugared"]` (WP-NAME-1: key **is** the canonical expression) | semantic-law pin |
| `/…/packages/columna-core/tests/test_inline_reduction.py::test_single_level_note_is_byte_identical`, `::test_composite_pin_serves_with_rider_when_pin_axis_is_in_output`, `::test_single_level_pin_equal_output_is_still_standard_form` | historical compatibility pin |
| `/…/packages/columna-core/tests/test_hierarchy.py::test_hierarchy_desugars_to_edges_indistinguishable_from_hand_edges` | implementation-detail pin |
| `/…/docs/tools/regen_examples.py --check` (gate `regen-examples`) — regenerates every `” ```frameql-output ”` block; any change to a rendered canonical form or note string fails the committed diff | build-measurement pin |

---

#### H. Operator-registry shape / wire contract

| file::test | class |
|---|---|
| `/…/packages/columna-core/tests/test_generated_family_law.py::test_the_reason_registry_is_closed_and_fails_closed` — `REASON_OUTCOME["blocked_reduction"] == (REFUSE, UNSUPPORTED, ANALYTICAL)`, `["chained_crossing"] == (ERROR, None, REALIZATION)`, `["anchor_spent"] == (REFUSE, UNSUPPORTED, ANALYTICAL)`, `UnregisteredReason` on unknown | semantic-law pin |
| `/…/packages/columna-core/tests/test_generated_family_law.py::test_the_b_anchor_caveat_is_tombstoned_not_deleted` — `"b_anchor_crossing" in CATEGORY_TABLE` and never re-emitted | historical compatibility pin |
| `/…/packages/columna-core/tests/test_generated_family_law.py::test_the_wire_contract_did_not_move` — `CONTRACT_VERSION == "4"` | historical compatibility pin |
| `/…/packages/columna-core/tests/test_inline_reduction.py::test_wire_contract_version_is_current` | historical compatibility pin |
| `/…/packages/columna-core/tests/test_inline_reduction.py::test_avg_is_mean_alias`, `::test_pinned_reducers_serve[sum/min/max/mean]` | implementation-detail pin |
| `/…/packages/columna-core/tests/test_inline_reduction.py::test_input_anchor_ambiguous_is_a_distinct_clarify_reason`, `::test_law1_is_its_own_dimension_per_of1`, `::test_law2_is_a_clarify_sibling_of_ambiguous_grain` | semantic-law pin |
| `/…/packages/columna-core/tests/test_expression_law.py::test_collapse_with_blocked_transport_refuses_blocked_reduction`, `::test_co_anchor_ambiguous_is_retired_and_never_emitted` | semantic-law pin / historical compatibility pin |
| `/…/packages/columna-core/tests/test_dependent_pair.py` (line 85 `("refuse","blocked_reduction","unsupported")`) | semantic-law pin |
| `/…/packages/columna-core/tests/test_adjudication.py::test_non_replayable_reducer_untestable` and the `sum`/`median`/`mean` FAMILY fixtures (lines 66–119) — the math channel is gated on `REGISTRY[...].linear` / additive-monoid `sum` | semantic-law pin |
| `/…/packages/columna-server/tests/test_mcp_server.py::test_discovery_lists_askable_measures_and_anchors` — `"sum" in rev["reducers"]` (from `tools.py:441` `"reducers": list(mc.family)`) | profile-contract pin |
| `/…/packages/columna-server/tests/test_mcp_server.py::test_manifold_status_counts` — `s["counts"]["measures"] == 6` | build-measurement pin |
| `/…/packages/columna-core/tests/test_k0_compiler.py::test_every_allowed_reducer_compiles_and_checks_clean[sum/count/min/max]`, `::test_a_reducer_the_measure_type_rejects_refuses_before_emission` (signature law `accepts`) | profile-contract pin |
| `/…/packages/columna-core/tests/test_k0_compiler.py::test_excluded_reducers_refuse_with_a_stated_reason[mean/avg/median/mode/distinct/percentile]` | profile-contract pin |
| `/…/docs/tools/check_no_tier_claims.py` (gate `no-tier-claims`) — enforces the §17.4 vocabulary `ROADMAP / DELIVERY-OPERATIONS / RETIRED`; a new standing word in the manuals fails | profile-contract pin |

---

#### I. Test files whose NAME declares a standing-rule pin

These are the "do not fix by changing behaviour" set — the name is the obligation.

**core** (`/…/packages/columna-core/tests/`):
`test_witness_non_interference.py` (docstring: "STANDING RULES for materialized measure state"), `test_plan_run_standing.py`, `test_pin_admissibility.py`, `test_pin_verdict_truthfulness.py`, `test_map_operand_pin.py`, `test_generated_family_law.py`, `test_expression_law.py`, `test_family_member_support.py`, `test_where_capability_gate.py`, `test_filter_jurisdiction.py`, `test_jurisdiction_seam.py`, `test_jurisdiction_inversion.py`, `test_canonical_conformance.py`, `test_assert_retirement.py`, `test_fixture_drift.py`, `test_disclosure_channels.py`, `test_alignment_domain.py`, `test_explicit_order_adjudication.py`, `test_basis_absence.py`, `test_universe_basis.py`, `test_source_identity.py`, `test_operator_umbrella.py`, `test_p05a_execution_contract.py`, `test_p05b0_data_identity.py`, `test_afternoon_page_gate.py`, `test_track1_adjudication.py`, `test_nonexistent_measure.py`, `test_draft_polarity.py`.

**server** (`/…/packages/columna-server/tests/`):
`test_describe_insulation.py`, `test_from_manifold_governs.py`, `test_lowering_receipt.py`, `test_version_aware_serving.py`, `test_governed_catalog.py`, `test_warehouse_coherence.py`, `test_benchmark_coherence.py`, `test_demo_data_drift.py`, `test_execution_provider.py`.

---

#### Notes / gaps worth flagging to the migration

1. **Bracket reassignment is essentially untested.** Zero test assertions in either package. The only guards are prose-level (`docs/frame_ql_language.md` §2.8 / §6.7 / line 215) plus `check_manual_frameql.py`'s roadmap-mark check. `scripts/check_purged_grammar.py` is narrowly scoped to `EDGE … ALONG … VIA` and will **not** catch a retired bracket form — it needs a second pattern if the predicate-bracket is purged.
2. **`check_prose_coherence.py` is a parse-only tripwire** (`parse_statement`, `EnvelopeSyntaxError`), run with `cwd = apps/website` against the *PyPI-installed* wheel. It never sees semantics — so a category reclassification passes it silently, and it only bites if the surface grammar moves.
3. **`in_core` is already flagged as overloaded** in `docs/tools/capability_authority.py:129` — `mean` is `in_core=False` but in `SERIES_REDUCERS`. Any taxonomy change that touches `in_core` will shift measured levels in `frame_ql_build_status.md` and fail `regen_capability_tables.py --check`.
4. **`standing_exceeded()`** already reports the six scan operators as executing-while-`proposed`. If scans get promoted in the taxonomy, that report changes and `frame_ql_build_status.md` must be regenerated.
5. `scripts/gates.toml` is the single authority for the required gate set; the relevant gate ids are `pytest-core`, `pytest-server`, `regen-examples`, `capability-authority`, `capability-tables`, `manual-frameql`, `no-tier-claims`, `purged-grammar`, `prose-coherence`, `meta-gate`.
