# Frame-QL Build Conformance Matrix v0.1

**Measured at commit:** `f18ba061967aa7e13c461af6debabcc249485656`
(branch `reconciliation/family-law-capability-state`; `f18ba06 Reconciliation v0.2 — ratifications recorded, FAMILY/beta corrected, Q5 de-canonized`)

**Date measured:** 1 September 2026

**Package under test:** `packages/columna-core` — `pyproject.toml:9` declares `version = "0.18.1"`; `columna_core/__init__.py:47` declares `__version__ = "0.16.0-core"`. *(These disagree in the tree as measured; the Manual cites "columna-core 0.18.1". Recorded, not resolved.)*

**Python / environment:** `/tmp/fqvenv/bin/python` — CPython 3.12.14 (GCC 14.2.0), Linux 6.12.91-fly.
Installed: `duckdb 1.5.5`, `polars 1.44.1`, `datasketches 5.2.0`, `numpy 2.5.2`, `pytest 9.1.1`, and **`pyarrow 25.0.1`, which I had to install** — without it `docs/tools/manual_fixtures/harness.servers()` cannot publish (`connector.py:271` calls `pl.from_arrow(...)`), so `publish()` failed closed with `FaceContradiction: ... driver 'category_rank' is not servable at 'category': No module named 'pyarrow'` and *nothing* — not the gate, not the probe, not 9 of the test modules — could run. Every result below was taken with `pyarrow` present.
`PYTHONPATH=/data/repos/978ea3c9feee4ad79341d42517782efd/columna/packages/columna-core/src`, `PYTHONDONTWRITEBYTECODE=1`, and `__pycache__` cleared before the recorded runs.

---

## How this was measured

Nothing in this matrix is inferred from the Manual's prose. Every `grammar recognition`, `parse result`,
`planner support`, `execution support` and `verbatim reason` cell is a value I captured by running the
shipped code at this commit. The instrument is `/tmp/conformance_probe.py`: for each of the **99 forms**
below it calls `columna_core.envelope.parse_statement`, then `ManifoldServer.planner.plan_statement`,
then `ManifoldServer.planner.run_statement`, wrapping each stage so an exception is *recorded* rather
than fatal, and reads the disposition off `columna_core.disclosure_wire.wire_frame`. It plans against the
**real, adjudicated Manual fixtures** — `docs/tools/manual_fixtures/harness.py`, the same `servers()` /
`server_for()` wiring the standing gate uses, with `publish()` actually run so transport edges and M:N
faces are certified (P0.5a is closed-by-default; an unpublished fixture would answer `uncertified_edge`
to most of the Manual and every finding would be a fixture artifact). Forms drawn from the Manual are
routed to the fixture the Manual's own `FROM` names. Where a form needed a follow-up to attribute a
reason string to its real cause, I ran the variant too and recorded it as an `X-` row; `/tmp/probe_detail.py`
dumped full `no_result` / `disclosures` payloads and the returned frames.

Alongside the probe I ran, at this commit and in fresh processes:

```
docs/tools/check_manual_frameql.py                    → exit 0; "40 total — 27 shipped, 11 roadmap, 1 marked ill-formed, 1 schematic, 0 FAIL"
pytest packages/columna-core/tests -q                 → 669 passed, 21 skipped
pytest <the 11 Frame-QL test modules> -q              → 235 passed
```

A first `pytest` run *before* `pyarrow` was installed collapsed at collection (`9 errors`); that result is
discarded as an environment artifact and is not recorded anywhere in the matrix. Nothing below is a
"does-not-work" cell taken from a stale-bytecode or missing-dependency run.

The Manual forms were enumerated mechanically, not by eye: I re-used the gate's own `_fenced_blocks` /
`_statements` / `sections` functions to walk every fenced block in `docs/frame_ql_manual_v2.md` at this
working-tree state, which yields **44 fenced blocks / 49 statements**. The gate reads 35 of those blocks
(the 40 examples its summary line counts) and skips 9 blocks entirely (see D4 in §5). Every Ch1–Ch6 block is in the matrix, marked or unmarked, statement or
fragment, plus §5.6's `RELATE` declaration, §8.2's alias example and Appendix D's retired form, plus the
20 named forms probed in isolation, plus 11 attribution probes.

---

## Axis vocabulary, and how it aligns to the Core Profile draft

The requester specified ten independent axes. The **Frame-QL Core Profile Working Draft 0.2** arrived after
I began and its §25 is titled *"First Core conformance matrix"* — but §25 is an **architectural**
concern-level table (`Concern | Canonical/shared semantics | Core Profile`, rows such as *Query meaning*,
*Build limitation*, *New syntax*), explicitly prefaced *"This matrix describes architectural standing, not
one release's shipped feature inventory."* Its axes are therefore **not per-form** and cannot be adopted as
this document's columns. WD 0.2 §27.3 asks for exactly the artefact below — *"create a version-specific Core
build conformance matrix separate from this architectural profile"* — so this matrix keeps the requester's
ten per-form axes as primary and **aligns its vocabulary**, not its column names, to the draft:

| This matrix's column | Vocabulary source |
|---|---|
| **canonical status** — `admitted` / `roadmap` / `negative-example` (+ `admitted-as-fragment`, `admitted-as-schematic`, `n-a`) | `docs/frame_ql_manual_v2.md` section marks and fence kinds; cited per row |
| **Core Profile architectural compatibility** — `compatible` / `incompatible` / `n-a-not-canonical` / `n-a` | Core Profile WD 0.2 §3.1 (canonical form vs Core lowering), §16 (profile/build capability), §22 (current mechanisms are evidence, not profile law), §25 |
| **current Core build support** — `supported` / `unsupported-by-this-build` / `conditionally-supported` / `n-a` | **verbatim from Core Profile WD 0.2 §16**, which enumerates exactly these three build reports |
| **disposition-label judgement** — `n-a` / `OK-realization` / `MISLABELLED` / `CONTESTED` | Canonical Disposition Ruling v0.1 §4 and §14 |
| grammar recognition · parse result · planner support · execution support · semantic-gate result · verbatim reason · evidence | the requester's axes; measured |

**Axes I added beyond the requester's ten, and why:** (1) *disposition-label judgement*, at the coordinator's
instruction, giving Ruling §4/§14 a column of its own rather than a footnote; (2) *semantic-gate coverage*
is reported as a value in the gate column (including `NOT COVERED`), because nine Manual blocks are invisible
to the gate and that is itself a finding.

**The two independence rules I held to.** *Core Profile architectural compatibility* answers "does the
profile's **architecture** admit this form?" — it is a statement about WD 0.2, and a form this build cannot
execute is **not** thereby incompatible (§16: *canonical meaning exists + Core build lacks realization →
`unsupported`*, **not** *→ analytically invalid*). *Current Core build support* answers "does **this build**
realize it?" Twelve rows below read `compatible` / `unsupported-by-this-build`; that pairing is the normal,
correct state of affairs, not a defect. Separately, `n-a-not-canonical` marks forms whose **canonical meaning
is not yet fixed** (query-level `count(*)`, `WITH allocation`, the bracket filter, operator aliases) — for
those the profile question does not arise at all, and §25's *"New syntax | Canonical admission only | Cannot
invent"* is why Core may not settle them by shipping something.

**Where the Core Profile lives.** The Core Profile and Platform Profile drafts are **NOT in the repository
tree**. `grep -rni "core profile"` over the whole repo returns exactly three hits, all in
`specs/family_law_capability_reusable_state_reconciliation_v0_2.md` (`:56`, `:69`, `:75` — ratification R2,
*"Frame-QL Core Profile records what Columna Core can currently realize under canonical semantics"*). The
per-form authority used here is the working draft supplied as an attachment at
`/data/repos/978ea3c9feee4ad79341d42517782efd/attachments/fcf53af6_frameql_core_profile_working_draft_v0_2.md`,
with the ruling at `.../011fbc21_frameql_canonical_disposition_ruling_v0_1.md`. Cited as `WD 0.2 §n` /
`Ruling §n`. **If those attachments are not part of the record, every Core-Profile cell reverts to
`n-a-not-in-tree`.**

**One vocabulary trap, avoided deliberately.** `columna_core/disclosure.py:80` defines
`UNSUPPORTED = "unsupported"  # the data cannot support a result -> REFUSE` — in this codebase that
identifier is a *discriminator* carrying the **analytical** verdict, the exact opposite of the Ruling's
realization-layer `unsupported`. Rows whose no-result carries that discriminator (`blocked_reduction`,
`out_of_universe`, `pin_coarser_than_output`, `uncertified_edge`, `uncertified_face`) are analytical
Refusals, not build gaps. The *reason string* `"unsupported"` registered at `disclosure.py:314`
(`(ERROR, None)`, *"not implemented in this build (capability)"*) is the realization one. They are not the
same thing and are never conflated below.

---
## 1. Counts per axis (99 forms)

**canonical status**

| value | forms |
|---|---|
| `admitted` | 57 |
| `roadmap` | 19 |
| `negative-example` | 8 |
| `admitted-as-fragment` | 6 |
| `admitted-as-schematic` | 2 |
| `n-a` | 2 |
| `diagnostic` | 2 |
| `metasyntax` | 1 |
| `clause fragment` | 1 |
| `admitted-by-name` | 1 |

**grammar recognition**

| value | forms |
|---|---|
| `recognized` | 87 |
| `not-recognized` | 12 |

**planner support**

| value | forms |
|---|---|
| `plans (serve)` | 55 |
| `refuses — error` | 19 |
| `not-exercised` | 12 |
| `raises (outside the wire)` | 9 |
| `refuses — clarify` | 3 |
| `plans (disclose)` | 1 |

**execution support**

| value | forms |
|---|---|
| `executes` | 51 |
| `not-executed (error)` | 24 |
| `not-exercised` | 21 |
| `not-executed (clarify)` | 3 |

**Core Profile architectural compatibility**

| value | forms |
|---|---|
| `compatible` | 84 |
| `n-a-not-canonical` | 8 |
| `n-a` | 5 |
| `compatible in principle` | 2 |

**current Core build support**

| value | forms |
|---|---|
| `supported` | 55 |
| `unsupported-by-this-build` | 27 |
| `n-a` | 17 |

**disposition-label judgement**

| value | forms |
|---|---|
| `n-a` | 70 |
| `MISLABELLED` | 20 |
| `OK-realization` | 8 |
| `CONTESTED` | 1 |


## 2. Table A — canonical / profile / build standing

*Read with Table B, which carries the measured pipeline for the same IDs.*

| ID | Form | Canonical status (cited) | Core Profile arch. compat. (WD 0.2) | Current Core build support (WD 0.2 §16) | Disposition-label judgement (Ruling §4/§14) |
|---|---|---|---|---|---|
| `M-L117` | Ch1.2 envelope skeleton (metasyntax, bare fence) | metasyntax, not a form (docs/frame_ql_manual_v2.md:117-127) | n-a (metasyntax) | n-a — not a statement | n-a |
| `M-L137` | Ch1.3 FROM clause fragment (```text fence) | clause fragment (docs/frame_ql_manual_v2.md:137-139, ```text fence) | n-a (fragment) | n-a — not a whole statement | n-a |
| `M-L158` | Ch1.4 two pinned reducers at one anchor | admitted (docs/frame_ql_manual_v2.md:158-162, unmarked ```frameql) | compatible | supported | n-a |
| `M-L202` | Ch1.6 AS alias + map series | admitted (docs/frame_ql_manual_v2.md:202-206) | compatible | supported | n-a |
| `M-L250` | Ch1.7 EXPLAIN statement | admitted (docs/frame_ql_manual_v2.md:250-255) | compatible — `EXPLAIN` may expose the Core lowering ({CP} §3.1) | supported | n-a |
| `M-L276` | Ch2.1 multi-input reducer SCHEMATIC (metasyntactic template) | admitted-as-schematic (docs/frame_ql_manual_v2.md:276-279, ```frameql-schematic; §2.1) | compatible (shape, not a query) | n-a — a template, nothing to run | n-a (gate stops at grammar; planning it is out of scope) |
| `M-L315a` | Ch2.3 single reducer sum, explicit input pin | admitted (docs/frame_ql_manual_v2.md:315-319) | compatible | supported | n-a |
| `M-L315b` | Ch2.3 single reducer max, explicit input pin (non-family/generated reducer) | admitted (docs/frame_ql_manual_v2.md:315-319) | compatible — generated family ({CP} §18) | supported | n-a |
| `M-L315c` | Ch2.3 single reducer avg on a DERIVED column, explicit input pin | admitted (docs/frame_ql_manual_v2.md:315-319) | compatible | supported | n-a |
| `M-L325` | Ch2.3 unpinned reducer on a derived column (documented clarify) | admitted, documented `-- clarify: input_anchor_ambiguous` (docs/frame_ql_manual_v2.md:325-327) | compatible — Clarify is canonical ({RUL} §2, §14) | supported (realizes the canonical Clarify) | n-a — Clarify, correctly |
| `M-L374a` | Ch2.4 map of two pinned columns | admitted (docs/frame_ql_manual_v2.md:374-377) | compatible | supported | n-a |
| `M-L374b` | Ch2.4 map ratio of two pinned columns | admitted (docs/frame_ql_manual_v2.md:374-377) | compatible | supported | n-a |
| `M-L389` | Ch2.5 two universes juxtaposed in one frame | admitted (docs/frame_ql_manual_v2.md:389-393) | compatible | supported | n-a |
| `M-L401` | Ch2.6 broadcast: `@ {}` scalar input anchor | admitted (docs/frame_ql_manual_v2.md:401-403) | compatible | supported | n-a |
| `M-L413` | Ch2.7 composite reduction (nested pin) | admitted (docs/frame_ql_manual_v2.md:413-415) | compatible | supported | n-a |
| `M-L474` | Ch3.1 default-family sugar FRAGMENT (no SELECT keyword) | admitted-as-fragment (docs/frame_ql_manual_v2.md:474-477); the sugar itself is admitted (§3.1) | compatible ({RUL} §5 authorized default) | n-a — not a whole statement (see P-01, which is the same sugar inside a statement: supported) | n-a |
| `M-L474b` | Ch3.1 sugar fragment, canonical half | admitted-as-fragment (docs/frame_ql_manual_v2.md:474-477) | compatible | n-a — not a whole statement (see P-03) | n-a |
| `M-L495` | Ch3.2 omit-root sugar FRAGMENT (no SELECT keyword) | admitted-as-fragment (docs/frame_ql_manual_v2.md:495-498) | compatible ({RUL} §5) | n-a — not a whole statement; see M-L325/P-01 for the in-statement behaviour | n-a |
| `M-L524` | Ch4.1 WHERE on a base dimension (sugared series) | admitted (docs/frame_ql_manual_v2.md:524-527, in the §4.1 correction note) | compatible | supported | n-a |
| `M-L537` | Ch4.1 WHERE on a base dimension (canonical series) | admitted (docs/frame_ql_manual_v2.md:537-541) | compatible | supported | n-a |
| `M-L560` | Ch4.1.1 WHERE through a relationship-derived dimension [SCHEDULED] | roadmap — **[SCHEDULED]** (docs/frame_ql_manual_v2.md:551, §4.1.1); prose calls it *lawful and not executable in this build* (docs/frame_ql_manual_v2.md:553-556) | compatible — canonical meaning exists, Core lacks realization (frameql_core_profile_working_draft_v0_2.md §16) | unsupported-by-this-build | OK-realization — `filter_unsupported` is registered `(ERROR, None)` and its detail says *the ask is lawful; the build cannot execute it* (`disclosure.py:232`) |
| `M-L579` | Ch4.2 HAVING + query-level count(*) [ROADMAP] | roadmap — **[ROADMAP — the `count(*)` series only]** (docs/frame_ql_manual_v2.md:573, 579-585) | n-a-not-canonical — the Manual states the analytical object is undetermined (docs/frame_ql_manual_v2.md:586-596); frameql_core_profile_working_draft_v0_2.md §25 *New syntax: Core cannot invent* | unsupported-by-this-build | **MISLABELLED (no disposition at all)** — a raw CPython `SyntaxError: Invalid star expression` escapes `plan_statement`; the four-mood wire is never reached, so the caller gets neither Refuse nor `unsupported` |
| `M-L609` | Ch4.3 ORDER BY clause FRAGMENT | admitted-as-fragment (docs/frame_ql_manual_v2.md:609-611) | compatible | n-a — not a whole statement (see P-10) | n-a |
| `M-L621` | Ch4.4 LIMIT clause FRAGMENT | admitted-as-fragment (docs/frame_ql_manual_v2.md:621-624) | compatible | n-a — not a whole statement (see P-11) | n-a |
| `M-L630` | Ch4.4 LIMIT n PER {dims} FRAGMENT | admitted-as-fragment (docs/frame_ql_manual_v2.md:630-633) | compatible | n-a — not a whole statement (see M-L924) | n-a |
| `M-L665` | Ch4.5 WITH macro binding | admitted (docs/frame_ql_manual_v2.md:665-669) | compatible | supported | n-a |
| `M-L747` | Ch5.6 RELATE ... FACES declaration (CML, not Frame-QL) | n-a — a `.cml` RELATE declaration, not Frame-QL (docs/frame_ql_manual_v2.md:747-755) | n-a (declaration language) | n-a — not a Frame-QL statement | n-a |
| `M-L756a` | Ch5.6 many-to-many face: TOUCH | admitted, documented `-- disclose: multi_counted` (docs/frame_ql_manual_v2.md:756-760) | compatible | supported | n-a |
| `M-L756b` | Ch5.6 many-to-many face: ASSIGN | admitted, documented `-- disclose: memberships_unrepresented` (docs/frame_ql_manual_v2.md:756-760) | compatible | supported | n-a |
| `M-L756c` | Ch5.6 many-to-many face: ALLOC | admitted, documented `-- serve` (docs/frame_ql_manual_v2.md:756-760) | compatible | supported | n-a |
| `M-L795` | Ch6.1 simple aggregation (default-family sugar) | admitted (docs/frame_ql_manual_v2.md:795-798) | compatible | supported | n-a |
| `M-L806` | Ch6.2 multiple metrics + query-level count(*) [ROADMAP] | roadmap — **[ROADMAP — the `count(*)` series only]** (docs/frame_ql_manual_v2.md:804, 806-812) | n-a-not-canonical (docs/frame_ql_manual_v2.md:816-826) | unsupported-by-this-build | **MISLABELLED (no disposition at all)** — raw CPython `SyntaxError: Invalid star expression` escapes the planner |
| `M-L833` | Ch6.3 composite reduction with explicit intermediate anchor | admitted (docs/frame_ql_manual_v2.md:833-837) | compatible | supported | n-a |
| `M-L843` | Ch6.4 mean with explicit input anchor | admitted (docs/frame_ql_manual_v2.md:843-846) | compatible | supported | n-a |
| `M-L852` | Ch6.5 map of co-anchored columns | admitted (docs/frame_ql_manual_v2.md:852-855) | compatible | supported | n-a |
| `M-L861` | Ch6.6 ratio across grains (`@ {}` denominator) | admitted (docs/frame_ql_manual_v2.md:861-865) | compatible | supported | n-a |
| `M-L874` | Ch6.7 bracket filter on a column [ROADMAP] | roadmap — **[ROADMAP]** (docs/frame_ql_manual_v2.md:869, 874-879); §2.8 says *the bracket filter is not shipped at all … does not parse* (docs/frame_ql_manual_v2.md:426) | n-a-not-canonical — a grow-by-ruling surface ({MAN}:419-421, ADR-035 D1) | unsupported-by-this-build | **MISLABELLED (no disposition at all)** — raw CPython `SyntaxError: invalid syntax. Maybe you meant '==' or ':=' instead of '='?` escapes the planner; a Python diagnostic is shown to a Frame-QL author |
| `M-L887` | Ch6.8 WHERE on a base dimension | admitted (docs/frame_ql_manual_v2.md:885-891) | compatible | supported | n-a |
| `M-L903` | Ch6.8a WHERE joined dimension + IN (...) [SCHEDULED] | roadmap — **[SCHEDULED]** (docs/frame_ql_manual_v2.md:897, 903-907) | compatible (frameql_core_profile_working_draft_v0_2.md §16) | unsupported-by-this-build | OK-realization — `filter_unsupported` (`disclosure.py:232`, `(ERROR, None)`) |
| `M-L914` | Ch6.9 HAVING on an output column | admitted (docs/frame_ql_manual_v2.md:912-918) | compatible | supported | n-a |
| `M-L924` | Ch6.10 top-N per group (ORDER BY + LIMIT n PER) | admitted (docs/frame_ql_manual_v2.md:922-929) | compatible | supported | n-a |
| `M-L940` | Ch6.11 scan: cumsum running total [ROADMAP] | roadmap — **[ROADMAP]** (docs/frame_ql_manual_v2.md:933, 940-944); prose: *Parses and plans; does not execute* (docs/frame_ql_manual_v2.md:935) | compatible | **supported — and the Manual says otherwise** | n-a — it serves; the defect is the Manual's claim, not a reason string |
| `M-L955` | Ch6.12 WITH allocation ... [marked frameql-illformed] | negative-example — ```frameql-illformed (docs/frame_ql_manual_v2.md:955-959) | n-a-not-canonical — `WITH allocation` is a grow-by-ruling surface ({MAN}:951-953) | n-a — must not parse, and does not | n-a — an `EnvelopeSyntaxError` naming the remedy is the intended behaviour |
| `M-L970` | Ch6.13a scan with family-aware `reset =` [ROADMAP] | roadmap — **[ROADMAP]** (docs/frame_ql_manual_v2.md:963, 970-974); prose: *these two do not even plan* (docs/frame_ql_manual_v2.md:965-968) | compatible | unsupported-by-this-build | **MISLABELLED** — reported as reason `unknown` (*unknown column / operator / construct*, `disclosure.py:316`) with the detail *unknown parameter 'reset'*; the Manual documents `reset` ({MAN}:1235) and §2.8 calls it *not implemented*, so the cause is realization, and the registered realization code is `unsupported` (`disclosure.py:314`) |
| `M-L978` | Ch6.13b scan with family-aware `step =` (lag) [ROADMAP] | roadmap — **[ROADMAP]** (docs/frame_ql_manual_v2.md:963, 978-982) | compatible | unsupported-by-this-build | **MISLABELLED** — reason `unknown`, detail *scan 'lag' takes one input expression and keyword params (n=, by=)*; `step=` is documented ({MAN}:1235) and unimplemented, i.e. realization |
| `M-L988` | Ch6.14 macro + HAVING + ORDER BY + LIMIT | admitted (docs/frame_ql_manual_v2.md:986-995) | compatible | supported | n-a |
| `M-L1008` | Ch6.15 the envelope end to end [SCHEDULED] | roadmap — **[SCHEDULED]** (docs/frame_ql_manual_v2.md:999, 1008-1016); prose: *Plans; does not execute on this build* (docs/frame_ql_manual_v2.md:1001) | compatible (frameql_core_profile_working_draft_v0_2.md §16 — canonical meaning exists, build lacks realization) | unsupported-by-this-build (PARTIAL: `gross` serves, `typical` fails) | OK-realization — reason `unsupported`, *the ask is not supported in this build* (`disclosure.py:314`) |
| `M-L1027` | Ch6.16 composite input anchor, two-stage statistic [SCHEDULED] | roadmap — **[SCHEDULED]** (docs/frame_ql_manual_v2.md:1020, 1027-1031) | compatible (frameql_core_profile_working_draft_v0_2.md §16) | unsupported-by-this-build | OK-realization — reason `unsupported` |
| `M-L1168` | Ch8.2 operator name aliases [ROADMAP] | roadmap — **[ROADMAP]** (docs/frame_ql_manual_v2.md:1159, 1168-1171) | n-a-not-canonical — no authoring surface is canonically admitted (docs/frame_ql_manual_v2.md:1161-1164); frameql_core_profile_working_draft_v0_2.md §25 *Core cannot invent syntax* | unsupported-by-this-build | **MISLABELLED (mis-attributed)** — as written the planner reports *series 'total(revenue)' has no derivable name — give it one with AS*, a NAMING complaint. Supplying `AS t` (form X-01) reveals the real cause: reason `unknown`, detail *'total' is not a scan operator*. Neither string says what §8.2 says (no alias surface ships). |
| `M-L1283` | App.D retired terse trailing-@ fragment (negative example) | negative-example — the retired trailing-`@` output form (docs/frame_ql_manual_v2.md:1279-1287, App. D; *retired*, docs/frame_ql_manual_v2.md:1253) | n-a — retired from the canonical language | n-a — must not parse, and does not | n-a — `EnvelopeSyntaxError` is the intended behaviour |
| `P-01` | single reducer, sugared, no FROM | admitted — §3.1 default-family sugar (docs/frame_ql_manual_v2.md:468-477) | compatible | supported | n-a |
| `P-02` | map of two bare (sugared) columns | admitted — §2.4 maps (docs/frame_ql_manual_v2.md:370-377) | compatible | supported | n-a |
| `P-03` | explicit input pin, single level | admitted — §2.3 explicit input pin (docs/frame_ql_manual_v2.md:311-319) | compatible | supported | n-a |
| `P-04` | composite input anchor (product pin) on finance fixture | admitted — §2.3 composite input anchor / WP-GRAIN-1 (docs/frame_ql_manual_v2.md:311-319, 461) | compatible | supported | n-a |
| `P-04b` | composite input anchor with `*` product spelling | admitted — the `*` anchor product (docs/frame_ql_manual_v2.md:1253-1255) | compatible | supported | n-a |
| `P-05` | `@ {}` empty input anchor alone | admitted — §2.6 broadcast `@ {}` (docs/frame_ql_manual_v2.md:397-403) | compatible | **unsupported-by-this-build** | OK-realization — reason `unsupported`, detail *this frame could not be resolved in the engine (AttributeError); the ask is not supported in this build.* The leaked exception CLASS in a user-facing string is a hygiene defect, not a mislabel. |
| `P-05b` | `AT {}` empty OUTPUT anchor with sugared series | admitted — `AT {}` is the grand total (docs/frame_ql_manual_v2.md:1255) | compatible | supported | n-a |
| `P-06` | WHERE on base dimension, single-quoted literal | admitted — §4.1, either quote spelling (docs/frame_ql_manual_v2.md:531-535, 549) | compatible | supported | n-a |
| `P-07` | WHERE on a relationship-derived dimension, alone | roadmap — §4.1.1 **[SCHEDULED]** (docs/frame_ql_manual_v2.md:551-558) | compatible (frameql_core_profile_working_draft_v0_2.md §16) | unsupported-by-this-build | OK-realization — `filter_unsupported`, `(ERROR, None)` at `disclosure.py:232`; guard at `planner.py:931-938` |
| `P-08` | IN (...) on a BASE dimension | admitted — `in` is a Manual map function (docs/frame_ql_manual_v2.md:1222) | compatible | supported | n-a |
| `P-08b` | IN (...) on a JOINED dimension | roadmap — §6.8a **[SCHEDULED]** (docs/frame_ql_manual_v2.md:897-907) | compatible (frameql_core_profile_working_draft_v0_2.md §16) | unsupported-by-this-build | OK-realization — `filter_unsupported` |
| `P-08c` | WHERE on a dimension not in the manifold at all | admitted — §4.1's per-series reachability law (docs/frame_ql_manual_v2.md:566-568); catalogued at docs/frame_ql_manual_v2.md:1091 (§7.3) | compatible | supported (realizes a Clarify) | **CONTESTED** — registered `(CLARIFY, AMBIGUOUS)` at `disclosure.py:243`, but the detail reads like \|L(Q)\|=0 (*has no grain to bind to*), which frameql_canonical_disposition_ruling_v0_1.md §14 makes Refuse. Left to the disposition audit. |
| `P-09` | HAVING alone, threshold that keeps rows | admitted — §4.2/§6.9 (docs/frame_ql_manual_v2.md:598-604, 912-918) | compatible | supported | n-a |
| `P-10` | ORDER BY alone on an alias | admitted — §4.3 (docs/frame_ql_manual_v2.md:605-615) | compatible | supported | n-a |
| `P-10b` | ORDER BY an anchor coordinate | admitted — §4.3 (anchor dimensions are orderable, docs/frame_ql_manual_v2.md:613) | compatible | supported | n-a |
| `P-11` | flat LIMIT n | admitted — §4.4 flat `LIMIT n` (docs/frame_ql_manual_v2.md:617-624) | compatible | supported | n-a |
| `P-11b` | LIMIT n PER {} (documented degenerate empty PER) | admitted — §4.4 *the empty `PER` set is permitted* (docs/frame_ql_manual_v2.md:645) | compatible | supported | n-a |
| `P-11c` | LIMIT n PER {dim} where PER key is NOT an ORDER BY key (documented refusal) | negative-example — §4.4 *the `PER` dimensions must be a subset of the `ORDER BY` columns* (docs/frame_ql_manual_v2.md:641) | compatible — a canonical well-formedness law | supported (the law is enforced) | n-a — a well-formedness refusal, correctly analytical; but it is raised as `FrameQLSyntaxError` OUTSIDE the four-mood wire rather than as a Refuse |
| `P-11d` | LIMIT n PER {alias} — PER key is a series alias, not a coordinate (documented refusal) | negative-example — §6.15 *`PER {typical}` would refuse (an alias, not a coordinate)* (docs/frame_ql_manual_v2.md:1018) | compatible — a canonical well-formedness law | supported (the law is enforced) | n-a — correctly analytical; same channel caveat as P-11c |
| `P-12` | macro binding referenced in SELECT and HAVING | admitted — §4.5 macro bindings (docs/frame_ql_manual_v2.md:649-675) | compatible | supported | n-a |
| `P-12b` | macro binding used in WHERE | admitted — §4.5: *a macro may be referenced in `SELECT`, `WHERE`, `HAVING`, `ORDER BY`* (docs/frame_ql_manual_v2.md:659) | compatible | **unsupported-by-this-build** | **MISLABELLED** — the macro is NOT expanded in `WHERE`: the planner reports `filter_unreachable` on the *binding name* `d` (*'d' is not addressable in that series' universe 'sales'*). The Manual's §4.5 explicitly admits a macro in `WHERE`; the asker is told to fix a dimension that does not exist. |
| `P-13` | scan: cumsum, order-only, executed | roadmap — §2.8 / §6.11 **[ROADMAP]** (docs/frame_ql_manual_v2.md:419, 425-431, 933-944) | compatible | **supported — contradicting docs/frame_ql_manual_v2.md:428 (*Scan execution is not available in the current Core build*)** | n-a |
| `P-13b` | scan: lag with n= | roadmap — §2.8 (docs/frame_ql_manual_v2.md:425-431) | compatible | **supported** (executes; discloses `undeclared_absence` for the 3 leading nulls) | n-a |
| `P-13c` | scan: rolling_mean (registry in_core=False) | roadmap — Appendix A lists `window` as a scan parameter (docs/frame_ql_manual_v2.md:1235); `rolling_mean` carries `in_core=False` in `operators.py` | compatible | unsupported-by-this-build | **MISLABELLED** — reason `unknown` with detail *scan 'rolling_mean': unknown parameter 'window' (accepts n=, by=)*. `operators.py` declares `rolling_mean` with `needs_window=True, in_core=False`, i.e. the parameter is KNOWN and the mechanics are absent — a realization gap reported as a vocabulary error. |
| `P-13d` | scan: rank (in Manual Appendix A, NOT in registry) | n-a-not-in-registry — Appendix A lists `rank` (docs/frame_ql_manual_v2.md:1233) but `operators.REGISTRY` has no entry | compatible in principle; the operator is not registered, so the profile question does not yet arise | unsupported-by-this-build | **MISLABELLED** — *'rank' is not a scan operator (registry scans: [...])*. `rank` is exactly the kind of operator the Manual's §7.3 *Unknown operator* clarification is for; the message instead asserts a kind-mismatch and offers a menu of scans. |
| `P-14` | bracket filter, minimal | roadmap — §2.8 / §6.7 **[ROADMAP]** (docs/frame_ql_manual_v2.md:419, 424, 869-879) | n-a-not-canonical (grow-by-ruling) | unsupported-by-this-build | **MISLABELLED (no disposition at all)** — raw CPython `SyntaxError` escapes the planner. Also corrects the Manual: §2.8 says the form *does not parse*, but the ENVELOPE parser accepts it (series text is captured verbatim); it dies in the plan-time expression parser. |
| `P-15` | multi-input reducer, concrete (two operands in one reducer) | admitted-as-schematic — §2.1's canonical form is `op(col_1 @ {a_1}, col_2 @ {a_2}, …)` (docs/frame_ql_manual_v2.md:276-279) | compatible in principle — the canonical form admits it; no Core lowering exists | unsupported-by-this-build | **MISLABELLED** — reason `unknown`, detail *inline reduction 'sum' takes exactly one column argument*. The Manual's own canonical form is multi-input; this is a build limit stated as a language rule. |
| `P-16` | query-level count(*) as the only series | roadmap — §4.2/§6.2 **[ROADMAP — the `count(*)` series only]** (docs/frame_ql_manual_v2.md:573, 804, 816-826) | n-a-not-canonical — *at least three readings are open… the Manual does not choose among them* (docs/frame_ql_manual_v2.md:820-824) | unsupported-by-this-build | **MISLABELLED (no disposition at all)** — raw CPython `SyntaxError: Invalid star expression` |
| `P-16b` | query-level count(*) unaliased | roadmap — as P-16 | n-a-not-canonical | unsupported-by-this-build | **MISLABELLED (mis-attributed)** — *cannot name series 'count(\*)' — give it a name with AS*: a naming complaint standing in front of an unresolved-architecture form |
| `P-17` | declared distinct/HLL measure (unique_visitors = distinct(customer_id)) | admitted — Appendix A: *the distinct family … Ships (`HLLSketch(p)`)* (docs/frame_ql_manual_v2.md:1191, 1209) | compatible — state construction/combination/finalization, *Core may realize* (frameql_core_profile_working_draft_v0_2.md §25) | supported (Disclose / `approximation`, rel_error 0.01625) | n-a |
| `P-17b` | inline approx_distinct (Manual Appendix A reducer name) | admitted-by-name — Appendix A reducer table lists `approx_distinct` as *fertile via HLL … Ships* (docs/frame_ql_manual_v2.md:1209) | compatible | **unsupported-by-this-build — the Appendix-A spelling is not a registry name** | **MISLABELLED** — *'approx_distinct' is not a scan operator*. The registry spells it `distinct` / `hll_count` / `hll_merge` / `hll_estimate`; the Manual's Appendix A spells it `approx_distinct`. A vocabulary drift reported as a kind error. |
| `P-17c` | inline distinct reducer by its registry name | admitted — `distinct` is a registered REDUCER (`operators.py` REGISTRY) | compatible | unsupported-by-this-build as an INLINE reducer (it works as a declared measure family — see P-17) | **MISLABELLED** — *'distinct' is not a scan operator*: `distinct` IS in the operator registry, as a REDUCER. The message denies a registered operator. |
| `P-18` | generated reducer: sum over a stock declared FAMILY {last,max,min,count} (DG-4 under-declared case) | admitted — the DG-4 under-declared case (specs/family_law_capability_reusable_state_reconciliation_v0_2.md:207-211) | compatible | n-a — the ask is under-specified, not unsupported | n-a — *'level' has a family [...] — specify a member* is a correct well-formedness message, though it is emitted as reason `unknown` rather than a Clarify |
| `P-18b` | generated reducer: max over a measure whose family is {sum} only | admitted — generated family (specs/family_law_capability_reusable_state_reconciliation_v0_2.md:207-211; ADR-036) | compatible | supported | n-a |
| `P-18c` | generated reducer: median (HOLISTIC witness) inline | admitted — Appendix A lists `median` as a mule reducer (docs/frame_ql_manual_v2.md:1205) | compatible | unsupported-by-this-build as an INLINE reducer (`SERIES_REDUCERS = {sum, mean, min, max, count}`) | **MISLABELLED** — *'median' is not a scan operator*: `median` IS a registered REDUCER in `operators.py`. The message denies a registered operator and offers a menu of scans. |
| `P-18d` | generated reducer: declared family member by dotted spelling (level.last) | admitted — §2.5 dotted family-member access (docs/frame_ql_manual_v2.md:389-393) | compatible | supported | n-a |
| `P-19` | anchor product with `*` in AT | admitted — the anchor product (docs/frame_ql_manual_v2.md:1253-1255) | compatible | **unsupported-by-this-build ON THE RETAIL FIXTURE** | OK-realization — reason `unsupported` (*ColumnNotFoundError*) |
| `P-20` | no AT clause at all (Ch3.3: output anchor never inferred) | negative-example — §3.3 *a query without `AT` is ill-formed and refused* (docs/frame_ql_manual_v2.md:507) | compatible — a canonical well-formedness law | n-a — must not parse, and does not | n-a — `EnvelopeSyntaxError` naming the remedy |
| `X-01` | operator alias with AS supplied (isolates naming from unknown-operator) | diagnostic probe (isolates M-L1168's cause) | n-a | unsupported-by-this-build | **MISLABELLED** — *'total' is not a scan operator*: the real fact is that no operator-alias surface ships (docs/frame_ql_manual_v2.md:1161) |
| `X-02` | generated reducer sum over a declared family MEMBER (level.last) | admitted — DG-4 lawful generated reduction (specs/family_law_capability_reusable_state_reconciliation_v0_2.md:207-211) | compatible | supported | n-a |
| `X-03` | generated reducer max over a declared family MEMBER (level.last) | admitted — generated family (specs/family_law_capability_reusable_state_reconciliation_v0_2.md:207-211) | compatible | supported | n-a |
| `X-04` | declared family member that does not exist (level.sum) | negative-example — a family member that was never declared | compatible | n-a — correctly rejected | n-a — *'level' has no family member 'sum' (have [...])* is accurate; emitted as reason `unknown` |
| `X-05` | median unpinned | diagnostic probe (median, unpinned) | compatible | unsupported-by-this-build | **MISLABELLED** — same *not a scan operator* string as P-18c |
| `X-06` | generated reducer sum of a stock across STORES (DG-4 lawful case) | admitted — DG-4 lawful case at store grain (specs/family_law_capability_reusable_state_reconciliation_v0_2.md:207-211) | compatible | supported | n-a |
| `X-07` | inline count reducer (SERIES_REDUCERS member) | admitted — `count` is in `SERIES_REDUCERS` | compatible | supported | n-a |
| `X-08` | inline mean reducer (SERIES_REDUCERS member) | admitted — `mean` is in `SERIES_REDUCERS` | compatible | supported | n-a |
| `X-09` | scan with no derivable order axis | admitted — §2.8: *an order-dependent operation whose order is neither derivable nor named is a clarification* (docs/frame_ql_manual_v2.md:432) | compatible | unsupported-by-this-build | **MISLABELLED** — the Manual and frameql_canonical_disposition_ruling_v0_1.md §7 both say a missing order is a CLARIFY (several/no governed order); the build emits reason `unknown` → outcome `error`, i.e. neither Clarify nor Refuse. The detail string itself is excellent. |
| `X-10` | unknown column | negative-example — §7.3 *Unknown operator* / unknown column (docs/frame_ql_manual_v2.md:1089) | compatible | n-a — correctly rejected | n-a — *unknown column 'nosuchmeasure'* is accurate |
| `X-11` | unregistered operator name | negative-example — §7.3 *Unknown operator* (docs/frame_ql_manual_v2.md:1089) | compatible | n-a — correctly rejected | **MISLABELLED** — the CORRECT outcome for an unregistered operator, delivered with the WRONG reason string: *'frobnicate' is not a scan operator*, which asserts a kind the asker never claimed. |

## 3. Table B — the measured pipeline

| ID | Query (as run) | Grammar | Parse result | Planner support | Execution support | Verbatim reason / disposition | Semantic gate | Evidence |
|---|---|---|---|---|---|---|---|---|
| `M-L117` | `[EXPLAIN] [FROM <manifold>] [WITH <name> = <expression> [, ...]] SELECT <series_1> [AS <alias_1>], <series_2> [AS <alias_2>], ... AT { <output_anchor>` | not-recognized | EnvelopeSyntaxError: AT needs a braced anchor — write AT { level } (the braces say the anchor is a product of levels), e.g. AT {region*store}; got '{ <output_an | not-exercised (did not parse) | not-exercised | `EnvelopeSyntaxError: AT needs a braced anchor — write AT { level } (the braces say the anchor is a product of levels), e.g. AT {region*store}; got '{ <output_anchor> }\n[WHERE  <per-series predicate> [AND ...]]\n[HAVING <output-frame predicate> [AND ...]]\n[ORDER BY <output-frame column> [ASC\|DESC] [, ...]]\n[LIMIT  n [PER { <anchor coordinates> }]]'` | NOT COVERED — bare/`text` fence whose first line is not EXPLAIN/FROM/WITH/SELECT, so the gate skips it entirely | `/tmp/conformance_probe.py` |
| `M-L137` | `FROM finance_manifold` | not-recognized | EnvelopeSyntaxError: a query must SELECT at least one series — e.g. SELECT revenue AT {region} | not-exercised (did not parse) | not-exercised | `EnvelopeSyntaxError: a query must SELECT at least one series — e.g. SELECT revenue AT {region}` | NOT COVERED — bare/`text` fence whose first line is not EXPLAIN/FROM/WITH/SELECT, so the gate skips it entirely | `/tmp/conformance_probe.py` |
| `M-L158` | `SELECT sum(revenue @ {transaction}), sum(cost @ {transaction}) AT {customer}` | recognized | series=['sum(revenue @ {transaction})'; 'sum(cost @ {transaction})'] anchor=('customer',) | plans (`serve`) | **executes** (`serve`) | exec `provenance`: `'sum of revenue@transaction' reduced to customer — the sum of revenue@transaction reading (input anchor pinned to 'transaction'), not the pooled value at customer` | shipped fence: gate PLANS and EXECUTES it; PASS | `/tmp/conformance_probe.py`; gate L158; test_envelope_planner.py::test_multi_series_juxtaposition |
| `M-L202` | `SELECT revenue AS total_revenue, (revenue - cost) AS profit AT {customer}` | recognized | series=['revenue' AS total_revenue; '(revenue - cost)' AS profit] anchor=('customer',) | plans (`serve`) | **executes** (`serve`) | — (no reason: the form serves) | shipped fence: gate PLANS and EXECUTES it; PASS | `/tmp/conformance_probe.py`; gate L202; test_envelope_planner.py::test_as_alias_names_the_column |
| `M-L250` | `EXPLAIN FROM finance_manifold SELECT max( sum(revenue @ {transaction}) @ {customer, month} ) AS peak_month AT {customer}` | recognized | EXPLAIN FROM=finance_manifold series=['max( sum(revenue @ {transaction}) @ {customer, month} )' AS peak_month] anchor=('customer',) | plans (`serve`) | **executes** (`serve`) | exec `provenance`: `'sum of revenue@transaction' reduced to customer*month — the sum of revenue@transaction reading (input anchor pinned to 'transaction'), not the pooled value at customer*month` | shipped fence: gate PLANS and EXECUTES it; PASS | `/tmp/conformance_probe.py`; gate L250; test_envelope_explain.py::test_desugared_is_the_consumed_artifact |
| `M-L276` | `SELECT op( col_1 @ {a_1}, col_2 @ {a_2}, ... ) AS name AT { A }` | recognized | series=['op( col_1 @ {a_1}, col_2 @ {a_2}, ... )' AS name] anchor=('A',) | refuses (`error` / `unknown`) | not-executed (`error`) | plan `unknown`: `'op' is not a scan operator (registry scans: ['cummax', 'cummin', 'cumsum', 'lag', 'lead', 'pct_change', 'rolling_mean', 'rolling_sum'])` | ```frameql-schematic: gate asserts GRAMMAR ONLY (parses); PASS | `/tmp/conformance_probe.py`; gate L276 |
| `M-L315a` | `SELECT sum(revenue @ {transaction}) AS gross AT {customer}` | recognized | series=['sum(revenue @ {transaction})' AS gross] anchor=('customer',) | plans (`serve`) | **executes** (`serve`) | exec `provenance`: `'sum of revenue@transaction' reduced to customer — the sum of revenue@transaction reading (input anchor pinned to 'transaction'), not the pooled value at customer` | shipped fence: gate PLANS and EXECUTES it; PASS | `/tmp/conformance_probe.py`; gate L315; test_inline_reduction.py::test_pinned_reducers_serve |
| `M-L315b` | `SELECT max(revenue @ {transaction}) AS peak_txn AT {customer}` | recognized | series=['max(revenue @ {transaction})' AS peak_txn] anchor=('customer',) | plans (`serve`) | **executes** (`serve`) | exec `provenance`: `'max of revenue@transaction' reduced to customer — the max of revenue@transaction reading (input anchor pinned to 'transaction'), not the pooled value at customer` | shipped fence: gate PLANS and EXECUTES it; PASS | `/tmp/conformance_probe.py`; gate L315; test_generated_family_law.py::test_lawful_family_generation_serves |
| `M-L315c` | `SELECT avg(aov @ {day}) AS typical AT {customer}` | recognized | series=['avg(aov @ {day})' AS typical] anchor=('customer',) | plans (`serve`) | **executes** (`serve`) | exec `provenance`: `'mean of aov@day' reduced to customer — the mean of aov@day reading (input anchor pinned to 'day'), not the pooled value at customer` | shipped fence: gate PLANS and EXECUTES it; PASS | `/tmp/conformance_probe.py`; gate L315; test_inline_reduction.py::test_avg_is_mean_alias |
| `M-L325` | `SELECT avg(aov) AT {region}` | recognized | series=['avg(aov)'] anchor=('region',) | plans → refuses to answer (`clarify` / `input_anchor_ambiguous`) | not-executed (`clarify`) | plan `input_anchor_ambiguous`: `inline reduction 'mean(aov)' does not pin its input anchor — the grain to resolve 'aov' at before reducing to region is underdetermined; pin it, e.g. 'mean(aov@customer)'` | shipped fence: gate PLANS and EXECUTES it; PASS | `/tmp/conformance_probe.py`; gate L325; test_inline_reduction.py::test_input_anchor_ambiguous_is_a_distinct_clarify_reason |
| `M-L374a` | `SELECT (revenue @ {customer, day}) - (cost @ {customer, day}) AS profit AT {customer, day}` | recognized | series=['(revenue @ {customer, day}) - (cost @ {customer, day})' AS profit] anchor=('customer', 'day') | plans (`serve`) | **executes** (`serve`) | — (no reason: the form serves) | shipped fence: gate PLANS and EXECUTES it; PASS | `/tmp/conformance_probe.py`; gate L374; test_map_operand_pin.py::test_single_level_pin_on_map_operands_serves |
| `M-L374b` | `SELECT (revenue @ {transaction}) / (orders @ {transaction}) AS aov AT {transaction}` | recognized | series=['(revenue @ {transaction}) / (orders @ {transaction})' AS aov] anchor=('transaction',) | plans (`serve`) | **executes** (`serve`) | — (no reason: the form serves) | shipped fence: gate PLANS and EXECUTES it; PASS | `/tmp/conformance_probe.py`; gate L374 |
| `M-L389` | `SELECT revenue AS revenue, level.last AS inv AT {region}` | recognized | series=['revenue' AS revenue; 'level.last' AS inv] anchor=('region',) | plans (`serve`) | **executes** (`serve`) | — (no reason: the form serves) | shipped fence: gate PLANS and EXECUTES it; PASS | `/tmp/conformance_probe.py`; gate L389; test_envelope_planner.py::test_multi_series_juxtaposition |
| `M-L401` | `SELECT (revenue @ {customer}) / (revenue @ {}) AS share_of_total AT {customer}` | recognized | series=['(revenue @ {customer}) / (revenue @ {})' AS share_of_total] anchor=('customer',) | plans (`serve`) | **executes** (`serve`) | — (no reason: the form serves) | shipped fence: gate PLANS and EXECUTES it; PASS | `/tmp/conformance_probe.py`; gate L401; test_map_operand_pin.py::test_the_scalar_input_anchor_broadcasts |
| `M-L413` | `SELECT max( sum(revenue @ {transaction}) @ {customer, month} ) AS peak_month AT {customer}` | recognized | series=['max( sum(revenue @ {transaction}) @ {customer, month} )' AS peak_month] anchor=('customer',) | plans (`serve`) | **executes** (`serve`) | exec `provenance`: `'sum of revenue@transaction' reduced to customer*month — the sum of revenue@transaction reading (input anchor pinned to 'transaction'), not the pooled value at customer*month` | shipped fence: gate PLANS and EXECUTES it; PASS | `/tmp/conformance_probe.py`; gate L413 |
| `M-L474` | `revenue AT {customer}` | not-recognized | EnvelopeSyntaxError: a query must SELECT at least one series — e.g. SELECT revenue AT {region} | not-exercised (did not parse) | not-exercised | `EnvelopeSyntaxError: a query must SELECT at least one series — e.g. SELECT revenue AT {region}` | NOT COVERED — bare/`text` fence whose first line is not EXPLAIN/FROM/WITH/SELECT, so the gate skips it entirely | `/tmp/conformance_probe.py`; test_envelope_sugars.py::test_desugar_fills_alias_and_braces |
| `M-L474b` | `sum(revenue @ {transaction}) AT {customer}` | not-recognized | EnvelopeSyntaxError: a query must SELECT at least one series — e.g. SELECT revenue AT {region} | not-exercised (did not parse) | not-exercised | `EnvelopeSyntaxError: a query must SELECT at least one series — e.g. SELECT revenue AT {region}` | NOT COVERED — bare/`text` fence whose first line is not EXPLAIN/FROM/WITH/SELECT, so the gate skips it entirely | `/tmp/conformance_probe.py` |
| `M-L495` | `sum(revenue) AT {customer}` | not-recognized | EnvelopeSyntaxError: a query must SELECT at least one series — e.g. SELECT revenue AT {region} | not-exercised (did not parse) | not-exercised | `EnvelopeSyntaxError: a query must SELECT at least one series — e.g. SELECT revenue AT {region}` | NOT COVERED — bare/`text` fence whose first line is not EXPLAIN/FROM/WITH/SELECT, so the gate skips it entirely | `/tmp/conformance_probe.py`; test_envelope_sugars.py::test_omitted_input_anchor_defaults_and_discloses_when_one_lawful_reading |
| `M-L524` | `FROM finance_manifold SELECT revenue AT {customer} WHERE day >= "2024-01-01"` | recognized | FROM=finance_manifold series=['revenue'] anchor=('customer',) where=['day >= "2024-01-01"'] | plans (`serve`) | **executes** (`serve`) | — (no reason: the form serves) | shipped fence: gate PLANS and EXECUTES it; PASS | `/tmp/conformance_probe.py`; gate L524; test_where_capability_gate.py::test_a_base_dimension_predicate_still_serves |
| `M-L537` | `FROM finance_manifold SELECT sum(revenue @ {transaction}) AT {customer} WHERE day >= "2024-01-01"` | recognized | FROM=finance_manifold series=['sum(revenue @ {transaction})'] anchor=('customer',) where=['day >= "2024-01-01"'] | plans (`serve`) | **executes** (`serve`) | exec `provenance`: `'sum of revenue@transaction' reduced to customer — the sum of revenue@transaction reading (input anchor pinned to 'transaction'), not the pooled value at customer` | shipped fence: gate PLANS and EXECUTES it; PASS | `/tmp/conformance_probe.py`; gate L537; test_where_capability_gate.py::test_plan_and_execution_agree_on_every_where_form |
| `M-L560` | `FROM finance_manifold SELECT sum(revenue @ {transaction}) AT {customer} WHERE region = "east" AND date >= "2024-01-01"` | recognized | FROM=finance_manifold series=['sum(revenue @ {transaction})'] anchor=('customer',) where=['region = "east"', 'date >= "2024-01-01"'] | refuses (`error` / `filter_unsupported`) | not-executed (`error`) | plan `filter_unsupported`: `WHERE dimension 'region' is addressable in universe 'sales' but is not one of its base dimensions (customer, day, transaction), and this build pushes the filter to the measure's own source, which carries the base coordinates only. The ask is lawful; the build cannot execute it.` | roadmap fence: gate asserts only the [ROADMAP]/[SCHEDULED] section mark, never the behaviour; PASS | `/tmp/conformance_probe.py`; test_where_capability_gate.py::test_a_joined_dimension_is_refused_at_plan_time; ::test_the_reason_is_specific_and_registered |
| `M-L579` | `FROM finance_manifold SELECT sum(revenue) AS total_revenue, count(*) AS transaction_count AT {customer} HAVING total_revenue > 10000` | recognized | FROM=finance_manifold series=['sum(revenue)' AS total_revenue; 'count(*)' AS transaction_count] anchor=('customer',) having=['total_revenue > 10000'] | **raises** — `SyntaxError` outside the four-mood wire | not-exercised | PLAN RAISES `SyntaxError`: `Invalid star expression (<unknown>, line 1)` | roadmap fence: gate asserts only the [ROADMAP]/[SCHEDULED] section mark, never the behaviour; PASS | `/tmp/conformance_probe.py` |
| `M-L609` | `ORDER BY total_revenue DESC, customer ASC` | not-recognized | EnvelopeSyntaxError: a query must SELECT at least one series — e.g. SELECT revenue AT {region} | not-exercised (did not parse) | not-exercised | `EnvelopeSyntaxError: a query must SELECT at least one series — e.g. SELECT revenue AT {region}` | NOT COVERED — bare/`text` fence whose first line is not EXPLAIN/FROM/WITH/SELECT, so the gate skips it entirely | `/tmp/conformance_probe.py`; test_envelope_parser.py::test_order_by_directions |
| `M-L621` | `ORDER BY total_revenue DESC LIMIT 100` | not-recognized | EnvelopeSyntaxError: a query must SELECT at least one series — e.g. SELECT revenue AT {region} | not-exercised (did not parse) | not-exercised | `EnvelopeSyntaxError: a query must SELECT at least one series — e.g. SELECT revenue AT {region}` | NOT COVERED — bare/`text` fence whose first line is not EXPLAIN/FROM/WITH/SELECT, so the gate skips it entirely | `/tmp/conformance_probe.py`; test_envelope_parser.py::test_limit_bare |
| `M-L630` | `ORDER BY region, total_revenue DESC LIMIT 5 PER {region}` | not-recognized | EnvelopeSyntaxError: a query must SELECT at least one series — e.g. SELECT revenue AT {region} | not-exercised (did not parse) | not-exercised | `EnvelopeSyntaxError: a query must SELECT at least one series — e.g. SELECT revenue AT {region}` | NOT COVERED — bare/`text` fence whose first line is not EXPLAIN/FROM/WITH/SELECT, so the gate skips it entirely | `/tmp/conformance_probe.py`; test_envelope_parser.py::test_limit_per |
| `M-L665` | `FROM finance_manifold WITH profit = (revenue - cost) SELECT profit AT {customer, month}` | recognized | FROM=finance_manifold series=['profit'] anchor=('customer', 'month') bindings=[Binding(name='profit', expr='(revenue - cost)')] | plans (`serve`) | **executes** (`serve`) | — (no reason: the form serves) | shipped fence: gate PLANS and EXECUTES it; PASS | `/tmp/conformance_probe.py`; gate L665; test_envelope_planner.py::test_with_binding_substitutes |
| `M-L747` | `RELATE product <-> category VIA product_categories(product_id, category_id) FACES { touch = TOUCH assign = ASSIGN BY category_rank ORDER MIN alloc = A` | not-recognized | EnvelopeSyntaxError: a query must SELECT at least one series — e.g. SELECT revenue AT {region} | not-exercised (did not parse) | not-exercised | `EnvelopeSyntaxError: a query must SELECT at least one series — e.g. SELECT revenue AT {region}` | NOT COVERED — bare/`text` fence whose first line is not EXPLAIN/FROM/WITH/SELECT, so the gate skips it entirely | `/tmp/conformance_probe.py`; the same declaration is live in `docs/tools/manual_fixtures/finance_manifold.cml` |
| `M-L756a` | `SELECT revenue AT {category.touch}` | recognized | series=['revenue'] anchor=('category.touch',) | plans (`serve`) | **executes** (`disclose`) | exec `multi_counted`: `multi-counted by construction across product<->category: revenue reaches every category a product sits in — multi-counted; totals exceed the grand total` | shipped fence: gate PLANS and EXECUTES it; PASS | `/tmp/conformance_probe.py`; gate L756 |
| `M-L756b` | `SELECT revenue AT {category.assign}` | recognized | series=['revenue'] anchor=('category.assign',) | plans (`serve`) | **executes** (`disclose`) | exec `memberships_unrepresented`: `single-counted to each product's ORDER min category_rank category: 1 memberships unrepresented (the shadow). revenue lands in the product's single primary category; the rest disclosed as the shadow` | shipped fence: gate PLANS and EXECUTES it; PASS | `/tmp/conformance_probe.py`; gate L756 |
| `M-L756c` | `SELECT revenue AT {category.alloc}` | recognized | series=['revenue'] anchor=('category.alloc',) | plans (`serve`) | **executes** (`serve`) | exec `reconciliation`: `allocated by normalized category_weight: crossed total 550.00 reconciles to the grand total 550.00 (delta 0.0000). revenue splits across a product's categories by weight; totals reconcile to the grand total` | shipped fence: gate PLANS and EXECUTES it; PASS | `/tmp/conformance_probe.py`; gate L756 |
| `M-L795` | `FROM finance_manifold SELECT revenue AT {customer}` | recognized | FROM=finance_manifold series=['revenue'] anchor=('customer',) | plans (`serve`) | **executes** (`serve`) | — (no reason: the form serves) | shipped fence: gate PLANS and EXECUTES it; PASS | `/tmp/conformance_probe.py`; gate L795 |
| `M-L806` | `FROM finance_manifold SELECT revenue, cost, count(*) AS transaction_count AT {customer, month}` | recognized | FROM=finance_manifold series=['revenue'; 'cost'; 'count(*)' AS transaction_count] anchor=('customer', 'month') | **raises** — `SyntaxError` outside the four-mood wire | not-exercised | PLAN RAISES `SyntaxError`: `Invalid star expression (<unknown>, line 1)` | roadmap fence: gate asserts only the [ROADMAP]/[SCHEDULED] section mark, never the behaviour; PASS | `/tmp/conformance_probe.py` |
| `M-L833` | `FROM finance_manifold SELECT max( sum(revenue @ {transaction}) @ {customer, month} ) AS max_monthly_revenue AT {customer}` | recognized | FROM=finance_manifold series=['max( sum(revenue @ {transaction}) @ {customer, month} )' AS max_monthly_revenue] anchor=('customer',) | plans (`serve`) | **executes** (`serve`) | exec `provenance`: `'sum of revenue@transaction' reduced to customer*month — the sum of revenue@transaction reading (input anchor pinned to 'transaction'), not the pooled value at customer*month` | shipped fence: gate PLANS and EXECUTES it; PASS | `/tmp/conformance_probe.py`; gate L833 |
| `M-L843` | `FROM product_manifold SELECT mean( engagement_score @ {customer, week} ) AT {customer}` | recognized | FROM=product_manifold series=['mean( engagement_score @ {customer, week} )'] anchor=('customer',) | plans (`serve`) | **executes** (`serve`) | exec `provenance`: `'mean of engagement_score@{customer*week}' reduced to customer — pin fixes customer, reduces over week` | shipped fence: gate PLANS and EXECUTES it; PASS | `/tmp/conformance_probe.py`; gate L843; test_inline_reduction.py::test_avg_is_mean_alias |
| `M-L852` | `FROM finance_manifold SELECT (revenue - cost) AS profit AT {customer, day}` | recognized | FROM=finance_manifold series=['(revenue - cost)' AS profit] anchor=('customer', 'day') | plans (`serve`) | **executes** (`serve`) | — (no reason: the form serves) | shipped fence: gate PLANS and EXECUTES it; PASS | `/tmp/conformance_probe.py`; gate L852 |
| `M-L861` | `FROM finance_manifold SELECT ( revenue @ {customer} ) / ( revenue @ {} ) AS share_of_total AT {customer}` | recognized | FROM=finance_manifold series=['( revenue @ {customer} ) / ( revenue @ {} )' AS share_of_total] anchor=('customer',) | plans (`serve`) | **executes** (`serve`) | — (no reason: the form serves) | shipped fence: gate PLANS and EXECUTES it; PASS | `/tmp/conformance_probe.py`; gate L861 |
| `M-L874` | `FROM finance_manifold SELECT revenue[region = "east"] AS east_revenue, revenue AS total_revenue AT {customer}` | recognized | FROM=finance_manifold series=['revenue[region = "east"]' AS east_revenue; 'revenue' AS total_revenue] anchor=('customer',) | **raises** — `SyntaxError` outside the four-mood wire | not-exercised | PLAN RAISES `SyntaxError`: `invalid syntax. Maybe you meant '==' or ':=' instead of '='? (<unknown>, line 1)` | roadmap fence: gate asserts only the [ROADMAP]/[SCHEDULED] section mark, never the behaviour; PASS | `/tmp/conformance_probe.py` |
| `M-L887` | `FROM finance_manifold SELECT revenue AT {customer} WHERE day >= "2024-01-01"` | recognized | FROM=finance_manifold series=['revenue'] anchor=('customer',) where=['day >= "2024-01-01"'] | plans (`serve`) | **executes** (`serve`) | — (no reason: the form serves) | shipped fence: gate PLANS and EXECUTES it; PASS | `/tmp/conformance_probe.py`; gate L887; test_where_capability_gate.py::test_a_base_dimension_predicate_still_serves |
| `M-L903` | `FROM finance_manifold SELECT revenue AT {customer} WHERE date >= "2024-01-01" AND region IN ("east", "west")` | recognized | FROM=finance_manifold series=['revenue'] anchor=('customer',) where=['date >= "2024-01-01"', 'region IN ("east", "west")'] | refuses (`error` / `filter_unsupported`) | not-executed (`error`) | plan `filter_unsupported`: `WHERE dimension 'date' is addressable in universe 'sales' but is not one of its base dimensions (customer, day, transaction), and this build pushes the filter to the measure's own source, which carries the base coordinates only. The ask is lawful; the build cannot execute it.` | roadmap fence: gate asserts only the [ROADMAP]/[SCHEDULED] section mark, never the behaviour; PASS | `/tmp/conformance_probe.py`; test_where_capability_gate.py::test_the_IN_repair_converges_on_quotes_too |
| `M-L914` | `FROM finance_manifold SELECT revenue AS total_revenue AT {customer} HAVING total_revenue > 50000` | recognized | FROM=finance_manifold series=['revenue' AS total_revenue] anchor=('customer',) having=['total_revenue > 50000'] | plans (`serve`) | **executes** (`serve`) | — (no reason: the form serves) | shipped fence: gate PLANS and EXECUTES it; PASS | `/tmp/conformance_probe.py`; gate L914; test_envelope_planner.py::test_having_by_name_filters |
| `M-L924` | `FROM product_manifold SELECT product_revenue AT {category, product} ORDER BY category, product_revenue DESC LIMIT 5 PER {category}` | recognized | FROM=product_manifold series=['product_revenue'] anchor=('category', 'product') order_by=[OrderKey(column='category', descending=False), OrderKey(column='produc | plans (`serve`) | **executes** (`serve`) | — (no reason: the form serves) | shipped fence: gate PLANS and EXECUTES it; PASS | `/tmp/conformance_probe.py`; gate L924; test_envelope_planner.py::test_limit_per_anchor_coordinate |
| `M-L940` | `FROM finance_manifold SELECT cumsum( revenue @ {customer, day} ) AS revenue_to_date AT {customer, day}` | recognized | FROM=finance_manifold series=['cumsum( revenue @ {customer, day} )' AS revenue_to_date] anchor=('customer', 'day') | plans (`serve`) | **executes** (`serve`) | exec `provenance`: `scan cumsum over order 'day' within ['customer']` | roadmap fence: gate asserts only the [ROADMAP]/[SCHEDULED] section mark, never the behaviour; PASS | `/tmp/conformance_probe.py` (executed, returned a correct running total: C1 120→200); `/tmp/probe_detail.py` |
| `M-L955` | `FROM product_manifold WITH allocation product_to_category = proportional_to(category_weight) SELECT sum( revenue @ {product} ) AT {category}` | not-recognized | EnvelopeSyntaxError: expected a single name for a WITH name, got 'allocation product_to_category' | not-exercised (did not parse) | not-exercised | `EnvelopeSyntaxError: expected a single name for a WITH name, got 'allocation product_to_category'` | ```frameql-illformed: gate asserts it must NOT parse; PASS | `/tmp/conformance_probe.py`; gate L955 |
| `M-L970` | `FROM finance_manifold SELECT cumsum( revenue @ {customer, day}, reset = year ) AS revenue_ytd AT {customer, day}` | recognized | FROM=finance_manifold series=['cumsum( revenue @ {customer, day}, reset = year )' AS revenue_ytd] anchor=('customer', 'day') | refuses (`error` / `unknown`) | not-executed (`error`) | plan `unknown`: `scan 'cumsum': unknown parameter 'reset' (accepts n=, by=)` | roadmap fence: gate asserts only the [ROADMAP]/[SCHEDULED] section mark, never the behaviour; PASS | `/tmp/conformance_probe.py` |
| `M-L978` | `FROM finance_manifold SELECT ( revenue - lag(revenue, 1, step = year) ) / lag(revenue, 1, step = year) AS yoy_growth AT {customer, month}` | recognized | FROM=finance_manifold series=['( revenue - lag(revenue, 1, step = year) ) / lag(revenue, 1, step = year)' AS yoy_growth] anchor=('customer', 'month') | refuses (`error` / `unknown`) | not-executed (`error`) | plan `unknown`: `scan 'lag' takes one input expression and keyword params (n=, by=)` | roadmap fence: gate asserts only the [ROADMAP]/[SCHEDULED] section mark, never the behaviour; PASS | `/tmp/conformance_probe.py` |
| `M-L988` | `FROM finance_manifold WITH profit = (revenue - cost) SELECT profit AT {customer, month} HAVING profit > 0 ORDER BY profit DESC LIMIT 10` | recognized | FROM=finance_manifold series=['profit'] anchor=('customer', 'month') bindings=[Binding(name='profit', expr='(revenue - cost)')] having=['profit > 0'] order_by=[ | plans (`serve`) | **executes** (`serve`) | — (no reason: the form serves) | shipped fence: gate PLANS and EXECUTES it; PASS | `/tmp/conformance_probe.py`; gate L988 |
| `M-L1008` | `FROM retail WITH line = revenue @ {transaction} SELECT sum(line) AS gross, avg(aov @ {day}) AS typical AT { region * store } ORDER BY region, gross DE` | recognized | FROM=retail series=['sum(line)' AS gross; 'avg(aov @ {day})' AS typical] anchor=('region', 'store') bindings=[Binding(name='line', expr='revenue @ {transaction} | plans (`serve`) | not-executed (`error`) | exec `unsupported`: `this frame could not be resolved in the engine (ColumnNotFoundError); the ask is not supported in this build.` | roadmap fence: gate asserts only the [ROADMAP]/[SCHEDULED] section mark, never the behaviour; PASS | `/tmp/conformance_probe.py`; `/tmp/probe_detail.py` (frame returns `gross` for 2 rows, `typical` carries the no_result) |
| `M-L1027` | `FROM retail SELECT avg( revenue @ {store*product*cal.month} ) AS avg_monthly_product_revenue AT {store}` | recognized | FROM=retail series=['avg( revenue @ {store*product*cal.month} )' AS avg_monthly_product_revenue] anchor=('store',) | plans (`serve`) | not-executed (`error`) | exec `unsupported`: `this frame could not be resolved in the engine (ColumnNotFoundError); the ask is not supported in this build.` | roadmap fence: gate asserts only the [ROADMAP]/[SCHEDULED] section mark, never the behaviour; PASS | `/tmp/conformance_probe.py`; test_inline_reduction.py::test_composite_pin_serves_with_rider_when_pin_axis_is_in_output (the form itself is exercised on a fixture where it does resolve) |
| `M-L1168` | `FROM retail_manifold SELECT total(revenue), unique_visitors AT {store}` | recognized | FROM=retail_manifold series=['total(revenue)'; 'unique_visitors'] anchor=('store',) | **raises** — `FrameQLSyntaxError` outside the four-mood wire | not-exercised | PLAN RAISES `FrameQLSyntaxError`: `series 'total(revenue)' has no derivable name — give it one with AS (e.g. SELECT total(revenue) AS my_name)` | roadmap fence: gate asserts only the [ROADMAP]/[SCHEDULED] section mark, never the behaviour; PASS | `/tmp/conformance_probe.py`; see X-01 |
| `M-L1283` | `aov @ cal.month` | not-recognized | EnvelopeSyntaxError: a query must SELECT at least one series — e.g. SELECT revenue AT {region} | not-exercised (did not parse) | not-exercised | `EnvelopeSyntaxError: a query must SELECT at least one series — e.g. SELECT revenue AT {region}` | NOT COVERED — bare/`text` fence whose first line is not EXPLAIN/FROM/WITH/SELECT, so the gate skips it entirely | `/tmp/conformance_probe.py` |
| `P-01` | `SELECT revenue AT {customer}` | recognized | series=['revenue'] anchor=('customer',) | plans (`serve`) | **executes** (`serve`) | — (no reason: the form serves) | not covered (probe-only form; the gate reads Manual fenced blocks only) | `/tmp/conformance_probe.py`; test_envelope_planner.py::test_bare_measure_names_itself |
| `P-02` | `SELECT (revenue - cost) AS profit AT {customer}` | recognized | series=['(revenue - cost)' AS profit] anchor=('customer',) | plans (`serve`) | **executes** (`serve`) | — (no reason: the form serves) | not covered (probe-only form; the gate reads Manual fenced blocks only) | `/tmp/conformance_probe.py` |
| `P-03` | `SELECT sum(revenue @ {transaction}) AT {customer}` | recognized | series=['sum(revenue @ {transaction})'] anchor=('customer',) | plans (`serve`) | **executes** (`serve`) | exec `provenance`: `'sum of revenue@transaction' reduced to customer — the sum of revenue@transaction reading (input anchor pinned to 'transaction'), not the pooled value at customer` | not covered (probe-only form; the gate reads Manual fenced blocks only) | `/tmp/conformance_probe.py`; test_inline_reduction.py::test_pinned_inline_reduction_serves_with_immaterial_note |
| `P-04` | `SELECT avg( revenue @ {customer, day} ) AS typical_day AT {customer}` | recognized | series=['avg( revenue @ {customer, day} )' AS typical_day] anchor=('customer',) | plans (`serve`) | **executes** (`serve`) | exec `provenance`: `'mean of revenue@{customer*day}' reduced to customer — pin fixes customer, reduces over day` | not covered (probe-only form; the gate reads Manual fenced blocks only) | `/tmp/conformance_probe.py`; test_inline_reduction.py::test_composite_pin_serves_with_standard_note_when_no_pin_axis_in_output |
| `P-04b` | `SELECT avg( revenue @ {customer*day} ) AS typical_day AT {customer}` | recognized | series=['avg( revenue @ {customer*day} )' AS typical_day] anchor=('customer',) | plans (`serve`) | **executes** (`serve`) | exec `provenance`: `'mean of revenue@{customer*day}' reduced to customer — pin fixes customer, reduces over day` | not covered (probe-only form; the gate reads Manual fenced blocks only) | `/tmp/conformance_probe.py`; test_envelope_sugars.py::test_composite_input_anchor_desugars_mechanically |
| `P-05` | `SELECT (revenue @ {}) AS grand AT {}` | recognized | series=['(revenue @ {})' AS grand] anchor=() | plans (`serve`) | not-executed (`error`) | exec `unsupported`: `this frame could not be resolved in the engine (AttributeError); the ask is not supported in this build.` | not covered (probe-only form; the gate reads Manual fenced blocks only) | `/tmp/conformance_probe.py`; contrast M-L401/M-L861 where the same `@ {}` operand inside a ratio DOES execute |
| `P-05b` | `SELECT revenue AT {}` | recognized | series=['revenue'] anchor=() | plans (`serve`) | **executes** (`serve`) | — (no reason: the form serves) | not covered (probe-only form; the gate reads Manual fenced blocks only) | `/tmp/conformance_probe.py`; test_envelope_parser.py::test_grand_total_frame |
| `P-06` | `FROM finance_manifold SELECT revenue AT {customer} WHERE day >= '2024-01-01'` | recognized | FROM=finance_manifold series=['revenue'] anchor=('customer',) where=["day >= '2024-01-01'"] | plans (`serve`) | **executes** (`serve`) | — (no reason: the form serves) | not covered (probe-only form; the gate reads Manual fenced blocks only) | `/tmp/conformance_probe.py`; test_where_capability_gate.py::test_the_two_quote_spellings_of_one_literal_are_one_ask |
| `P-07` | `FROM finance_manifold SELECT revenue AT {customer} WHERE region = "east"` | recognized | FROM=finance_manifold series=['revenue'] anchor=('customer',) where=['region = "east"'] | refuses (`error` / `filter_unsupported`) | not-executed (`error`) | plan `filter_unsupported`: `WHERE dimension 'region' is addressable in universe 'sales' but is not one of its base dimensions (customer, day, transaction), and this build pushes the filter to the measure's own source, which carries the base coordinates only. The ask is lawful; the build cannot execute it.` | not covered (probe-only form; the gate reads Manual fenced blocks only) | `/tmp/conformance_probe.py`; test_where_capability_gate.py::test_a_joined_dimension_is_refused_at_plan_time |
| `P-08` | `FROM finance_manifold SELECT revenue AT {customer} WHERE day IN ("2024-01-05", "2024-01-19")` | recognized | FROM=finance_manifold series=['revenue'] anchor=('customer',) where=['day IN ("2024-01-05", "2024-01-19")'] | plans (`serve`) | **executes** (`serve`) | — (no reason: the form serves) | not covered (probe-only form; the gate reads Manual fenced blocks only) | `/tmp/conformance_probe.py`; test_where_capability_gate.py::test_an_IN_predicate_on_a_base_dimension_still_serves |
| `P-08b` | `FROM finance_manifold SELECT revenue AT {customer} WHERE region IN ("east", "west")` | recognized | FROM=finance_manifold series=['revenue'] anchor=('customer',) where=['region IN ("east", "west")'] | refuses (`error` / `filter_unsupported`) | not-executed (`error`) | plan `filter_unsupported`: `WHERE dimension 'region' is addressable in universe 'sales' but is not one of its base dimensions (customer, day, transaction), and this build pushes the filter to the measure's own source, which carries the base coordinates only. The ask is lawful; the build cannot execute it.` | not covered (probe-only form; the gate reads Manual fenced blocks only) | `/tmp/conformance_probe.py`; test_where_capability_gate.py::test_the_IN_repair_converges_on_quotes_too |
| `P-08c` | `FROM finance_manifold SELECT revenue AT {customer} WHERE warehouse = "W1"` | recognized | FROM=finance_manifold series=['revenue'] anchor=('customer',) where=['warehouse = "W1"'] | plans → refuses to answer (`clarify` / `filter_unreachable`) | not-executed (`clarify`) | plan `filter_unreachable`: `WHERE dimension 'warehouse' cannot lawfully reach series 'revenue' — 'warehouse' is not addressable in that series' universe 'sales', so the pre-reduction filter has no grain to bind to; the answer would be silently partial.` | not covered (probe-only form; the gate reads Manual fenced blocks only) | `/tmp/conformance_probe.py`; test_envelope_planner.py::test_where_unreachable_clarifies |
| `P-09` | `FROM finance_manifold SELECT revenue AS total_revenue AT {customer} HAVING total_revenue > 100` | recognized | FROM=finance_manifold series=['revenue' AS total_revenue] anchor=('customer',) having=['total_revenue > 100'] | plans (`serve`) | **executes** (`serve`) | — (no reason: the form serves) | not covered (probe-only form; the gate reads Manual fenced blocks only) | `/tmp/conformance_probe.py`; test_envelope_planner.py::test_having_by_name_filters |
| `P-10` | `FROM finance_manifold SELECT revenue AS total_revenue AT {customer} ORDER BY total_revenue DESC` | recognized | FROM=finance_manifold series=['revenue' AS total_revenue] anchor=('customer',) order_by=[OrderKey(column='total_revenue', descending=True)] | plans (`serve`) | **executes** (`serve`) | — (no reason: the form serves) | not covered (probe-only form; the gate reads Manual fenced blocks only) | `/tmp/conformance_probe.py`; test_envelope_planner.py::test_order_by_frame_column |
| `P-10b` | `FROM finance_manifold SELECT revenue AS total_revenue AT {customer} ORDER BY customer ASC` | recognized | FROM=finance_manifold series=['revenue' AS total_revenue] anchor=('customer',) order_by=[OrderKey(column='customer', descending=False)] | plans (`serve`) | **executes** (`serve`) | — (no reason: the form serves) | not covered (probe-only form; the gate reads Manual fenced blocks only) | `/tmp/conformance_probe.py` |
| `P-11` | `FROM finance_manifold SELECT revenue AS total_revenue AT {customer} ORDER BY total_revenue DESC LIMIT 2` | recognized | FROM=finance_manifold series=['revenue' AS total_revenue] anchor=('customer',) order_by=[OrderKey(column='total_revenue', descending=True)] limit=Limit(n=2, per | plans (`serve`) | **executes** (`serve`) | — (no reason: the form serves) | not covered (probe-only form; the gate reads Manual fenced blocks only) | `/tmp/conformance_probe.py`; test_envelope_planner.py::test_limit_bare |
| `P-11b` | `FROM finance_manifold SELECT revenue AS total_revenue AT {customer} ORDER BY total_revenue DESC LIMIT 2 PER {}` | recognized | FROM=finance_manifold series=['revenue' AS total_revenue] anchor=('customer',) order_by=[OrderKey(column='total_revenue', descending=True)] limit=Limit(n=2, per | plans (`serve`) | **executes** (`serve`) | — (no reason: the form serves) | not covered (probe-only form; the gate reads Manual fenced blocks only) | `/tmp/conformance_probe.py`. NOTE: the parser normalises `PER {}` to `per=()`, i.e. flat LIMIT — exactly what §4.4 specifies |
| `P-11c` | `FROM product_manifold SELECT product_revenue AT {category, product} ORDER BY product_revenue DESC LIMIT 5 PER {category}` | recognized | FROM=product_manifold series=['product_revenue'] anchor=('category', 'product') order_by=[OrderKey(column='product_revenue', descending=True)] limit=Limit(n=5,  | **raises** — `FrameQLSyntaxError` outside the four-mood wire | not-exercised | PLAN RAISES `FrameQLSyntaxError`: `PER {category} is not in ORDER BY — PER groups and ORDER BY ranks within each group, so the partition key must also sort; add 'category' to ORDER BY (e.g. ORDER BY category, …)` | not covered (probe-only form; the gate reads Manual fenced blocks only) | `/tmp/conformance_probe.py`; test_envelope_planner.py::test_per_not_in_order_by_refused |
| `P-11d` | `FROM product_manifold SELECT product_revenue AS pr AT {category, product} ORDER BY category, pr DESC LIMIT 5 PER {pr}` | recognized | FROM=product_manifold series=['product_revenue' AS pr] anchor=('category', 'product') order_by=[OrderKey(column='category', descending=False), OrderKey(column=' | **raises** — `FrameQLSyntaxError` outside the four-mood wire | not-exercised | PLAN RAISES `FrameQLSyntaxError`: `PER {pr} names 'pr', an output column — PER takes ANCHOR coordinates only; put 'pr' in the anchor to partition by it` | not covered (probe-only form; the gate reads Manual fenced blocks only) | `/tmp/conformance_probe.py`; test_envelope_planner.py::test_per_alias_refused |
| `P-12` | `FROM finance_manifold WITH profit = (revenue - cost) SELECT profit AT {customer} HAVING profit > 0` | recognized | FROM=finance_manifold series=['profit'] anchor=('customer',) bindings=[Binding(name='profit', expr='(revenue - cost)')] having=['profit > 0'] | plans (`serve`) | **executes** (`serve`) | — (no reason: the form serves) | not covered (probe-only form; the gate reads Manual fenced blocks only) | `/tmp/conformance_probe.py`; test_envelope_planner.py::test_with_binding_substitutes |
| `P-12b` | `FROM finance_manifold WITH d = day SELECT revenue AT {customer} WHERE d >= "2024-01-01"` | recognized | FROM=finance_manifold series=['revenue'] anchor=('customer',) bindings=[Binding(name='d', expr='day')] where=['d >= "2024-01-01"'] | plans → refuses to answer (`clarify` / `filter_unreachable`) | not-executed (`clarify`) | plan `filter_unreachable`: `WHERE dimension 'd' cannot lawfully reach series 'revenue' — 'd' is not addressable in that series' universe 'sales', so the pre-reduction filter has no grain to bind to; the answer would be silently partial.` | not covered (probe-only form; the gate reads Manual fenced blocks only) | `/tmp/conformance_probe.py` — compare P-06, the identical predicate written out longhand, which serves |
| `P-13` | `FROM finance_manifold SELECT cumsum( revenue @ {customer, day} ) AS rtd AT {customer, day}` | recognized | FROM=finance_manifold series=['cumsum( revenue @ {customer, day} )' AS rtd] anchor=('customer', 'day') | plans (`serve`) | **executes** (`serve`) | exec `provenance`: `scan cumsum over order 'day' within ['customer']` | not covered (probe-only form; the gate reads Manual fenced blocks only) | `/tmp/conformance_probe.py`; `/tmp/probe_detail.py` shows real running totals; `operators.py` gives `cumsum` `scan_impl="cumsum"`, `in_core=True` |
| `P-13b` | `FROM finance_manifold SELECT lag( revenue @ {customer, day}, n = 1 ) AS prev AT {customer, day}` | recognized | FROM=finance_manifold series=['lag( revenue @ {customer, day}, n = 1 )' AS prev] anchor=('customer', 'day') | plans (`serve`) | **executes** (`disclose`) | exec `provenance`: `scan lag over order 'day' within ['customer']` | not covered (probe-only form; the gate reads Manual fenced blocks only) | `/tmp/conformance_probe.py` |
| `P-13c` | `FROM finance_manifold SELECT rolling_mean( revenue @ {customer, day}, window = 2 ) AS rm AT {customer, day}` | recognized | FROM=finance_manifold series=['rolling_mean( revenue @ {customer, day}, window = 2 )' AS rm] anchor=('customer', 'day') | refuses (`error` / `unknown`) | not-executed (`error`) | plan `unknown`: `scan 'rolling_mean': unknown parameter 'window' (accepts n=, by=)` | not covered (probe-only form; the gate reads Manual fenced blocks only) | `/tmp/conformance_probe.py` |
| `P-13d` | `FROM finance_manifold SELECT rank( revenue @ {customer, day} ) AS r AT {customer, day}` | recognized | FROM=finance_manifold series=['rank( revenue @ {customer, day} )' AS r] anchor=('customer', 'day') | refuses (`error` / `unknown`) | not-executed (`error`) | plan `unknown`: `'rank' is not a scan operator (registry scans: ['cummax', 'cummin', 'cumsum', 'lag', 'lead', 'pct_change', 'rolling_mean', 'rolling_sum'])` | not covered (probe-only form; the gate reads Manual fenced blocks only) | `/tmp/conformance_probe.py` |
| `P-14` | `SELECT revenue[region = "east"] AS east AT {customer}` | recognized | series=['revenue[region = "east"]' AS east] anchor=('customer',) | **raises** — `SyntaxError` outside the four-mood wire | not-exercised | PLAN RAISES `SyntaxError`: `invalid syntax. Maybe you meant '==' or ':=' instead of '='? (<unknown>, line 1)` | not covered (probe-only form; the gate reads Manual fenced blocks only) | `/tmp/conformance_probe.py` |
| `P-15` | `SELECT sum(revenue @ {transaction}, cost @ {transaction}) AS both AT {customer}` | recognized | series=['sum(revenue @ {transaction}, cost @ {transaction})' AS both] anchor=('customer',) | refuses (`error` / `unknown`) | not-executed (`error`) | plan `unknown`: `inline reduction 'sum' takes exactly one column argument (e.g. sum(aov@day) to pin the input anchor)` | not covered (probe-only form; the gate reads Manual fenced blocks only) | `/tmp/conformance_probe.py` |
| `P-16` | `FROM finance_manifold SELECT count(*) AS n AT {customer}` | recognized | FROM=finance_manifold series=['count(*)' AS n] anchor=('customer',) | **raises** — `SyntaxError` outside the four-mood wire | not-exercised | PLAN RAISES `SyntaxError`: `Invalid star expression (<unknown>, line 1)` | not covered (probe-only form; the gate reads Manual fenced blocks only) | `/tmp/conformance_probe.py` |
| `P-16b` | `FROM finance_manifold SELECT count(*) AT {customer}` | recognized | FROM=finance_manifold series=['count(*)'] anchor=('customer',) | **raises** — `FrameQLSyntaxError` outside the four-mood wire | not-exercised | PLAN RAISES `FrameQLSyntaxError`: `cannot name series 'count(*)' — give it a name with AS` | not covered (probe-only form; the gate reads Manual fenced blocks only) | `/tmp/conformance_probe.py` |
| `P-17` | `FROM retail_manifold SELECT unique_visitors AT {store}` | recognized | FROM=retail_manifold series=['unique_visitors'] anchor=('store',) | plans (`disclose`) | **executes** (`disclose`) | plan `approximation`: `unique_visitors.distinct: HLL distinct estimate [HLLSketch(12)]` | not covered (probe-only form; the gate reads Manual fenced blocks only) | `/tmp/conformance_probe.py`; test_hll_case_study.py::test_check; test_operator_umbrella.py::test_check |
| `P-17b` | `FROM retail_manifold SELECT approx_distinct( revenue @ {transaction} ) AS ad AT {store}` | recognized | FROM=retail_manifold series=['approx_distinct( revenue @ {transaction} )' AS ad] anchor=('store',) | refuses (`error` / `unknown`) | not-executed (`error`) | plan `unknown`: `'approx_distinct' is not a scan operator (registry scans: ['cummax', 'cummin', 'cumsum', 'lag', 'lead', 'pct_change', 'rolling_mean', 'rolling_sum'])` | not covered (probe-only form; the gate reads Manual fenced blocks only) | `/tmp/conformance_probe.py` |
| `P-17c` | `FROM retail_manifold SELECT distinct( revenue @ {transaction} ) AS d AT {store}` | recognized | FROM=retail_manifold series=['distinct( revenue @ {transaction} )' AS d] anchor=('store',) | refuses (`error` / `unknown`) | not-executed (`error`) | plan `unknown`: `'distinct' is not a scan operator (registry scans: ['cummax', 'cummin', 'cumsum', 'lag', 'lead', 'pct_change', 'rolling_mean', 'rolling_sum'])` | not covered (probe-only form; the gate reads Manual fenced blocks only) | `/tmp/conformance_probe.py` |
| `P-18` | `SELECT sum(level @ {store, day}) AS s AT {region}` | recognized | series=['sum(level @ {store, day})' AS s] anchor=('region',) | refuses (`error` / `unknown`) | not-executed (`error`) | plan `unknown`: `'level' has a family ['last', 'max', 'min', 'count'] — specify a member` | not covered (probe-only form; the gate reads Manual fenced blocks only) | `/tmp/conformance_probe.py`; the DG-4 case itself is X-02/X-06, which SERVE |
| `P-18b` | `SELECT max(revenue @ {transaction}) AS m AT {customer}` | recognized | series=['max(revenue @ {transaction})' AS m] anchor=('customer',) | plans (`serve`) | **executes** (`serve`) | exec `provenance`: `'max of revenue@transaction' reduced to customer — the max of revenue@transaction reading (input anchor pinned to 'transaction'), not the pooled value at customer` | not covered (probe-only form; the gate reads Manual fenced blocks only) | `/tmp/conformance_probe.py`; test_generated_family_law.py::test_other_reducers_over_the_stock_remain_lawful |
| `P-18c` | `SELECT median(revenue @ {transaction}) AS md AT {customer}` | recognized | series=['median(revenue @ {transaction})' AS md] anchor=('customer',) | refuses (`error` / `unknown`) | not-executed (`error`) | plan `unknown`: `'median' is not a scan operator (registry scans: ['cummax', 'cummin', 'cumsum', 'lag', 'lead', 'pct_change', 'rolling_mean', 'rolling_sum'])` | not covered (probe-only form; the gate reads Manual fenced blocks only) | `/tmp/conformance_probe.py`; test_holistic.py exercises the holistic path for DECLARED median |
| `P-18d` | `SELECT level.last AS inv AT {region}` | recognized | series=['level.last' AS inv] anchor=('region',) | plans (`serve`) | **executes** (`serve`) | — (no reason: the form serves) | not covered (probe-only form; the gate reads Manual fenced blocks only) | `/tmp/conformance_probe.py`; test_envelope_planner.py::test_member_access_key_is_verbatim_dotted |
| `P-19` | `FROM retail SELECT revenue AT { region * store }` | recognized | FROM=retail series=['revenue'] anchor=('region', 'store') | plans (`serve`) | not-executed (`error`) | exec `unsupported`: `this frame could not be resolved in the engine (ColumnNotFoundError); the ask is not supported in this build.` | not covered (probe-only form; the gate reads Manual fenced blocks only) | `/tmp/conformance_probe.py`. This isolates §6.15's residual: it is NOT the macro, the two grains or `PER` — a bare `SELECT revenue AT {region * store}` already fails when the two levels are reached by separate hierarchies. Anchor products elsewhere (M-L374a `AT {customer, day}`) execute. |
| `P-20` | `SELECT revenue` | not-recognized | EnvelopeSyntaxError: a query must declare its output grain with AT { … } — name the levels the frame stands at, e.g. SELECT revenue AT {region} (AT {} is the gr | not-exercised (did not parse) | not-exercised | `EnvelopeSyntaxError: a query must declare its output grain with AT { … } — name the levels the frame stands at, e.g. SELECT revenue AT {region} (AT {} is the grand total)` | not covered (probe-only form; the gate reads Manual fenced blocks only) | `/tmp/conformance_probe.py`; test_envelope_parser.py::test_syntax_errors_name_the_remedy |
| `X-01` | `FROM retail_manifold SELECT total(revenue) AS t, unique_visitors AT {store}` | recognized | FROM=retail_manifold series=['total(revenue)' AS t; 'unique_visitors'] anchor=('store',) | refuses (`error` / `unknown`) | not-executed (`error`) | plan `unknown`: `'total' is not a scan operator (registry scans: ['cummax', 'cummin', 'cumsum', 'lag', 'lead', 'pct_change', 'rolling_mean', 'rolling_sum'])` | not covered (probe-only form; the gate reads Manual fenced blocks only) | `/tmp/conformance_probe.py` |
| `X-02` | `SELECT sum(level.last @ {store, day}) AS s AT {region}` | recognized | series=['sum(level.last @ {store, day})' AS s] anchor=('region',) | plans (`serve`) | **executes** (`serve`) | exec `provenance`: `'sum of level.last@{store*day}' reduced to region — the sum of level.last@{store*day} reading (input anchor pinned to '{store*day}'), not the pooled value at region` | not covered (probe-only form; the gate reads Manual fenced blocks only) | `/tmp/conformance_probe.py`; test_generated_family_law.py::test_summing_a_stock_across_stores_is_lawful |
| `X-03` | `SELECT max(level.last @ {store, day}) AS m AT {region}` | recognized | series=['max(level.last @ {store, day})' AS m] anchor=('region',) | plans (`serve`) | **executes** (`serve`) | exec `provenance`: `'max of level.last@{store*day}' reduced to region — the max of level.last@{store*day} reading (input anchor pinned to '{store*day}'), not the pooled value at region` | not covered (probe-only form; the gate reads Manual fenced blocks only) | `/tmp/conformance_probe.py`; test_generated_family_law.py::test_other_reducers_over_the_stock_remain_lawful |
| `X-04` | `SELECT level.sum AS s AT {region}` | recognized | series=['level.sum' AS s] anchor=('region',) | refuses (`error` / `unknown`) | not-executed (`error`) | plan `unknown`: `'level' has no family member 'sum' (have ['last', 'max', 'min', 'count'])` | not covered (probe-only form; the gate reads Manual fenced blocks only) | `/tmp/conformance_probe.py` |
| `X-05` | `SELECT median(revenue) AS md AT {customer}` | recognized | series=['median(revenue)' AS md] anchor=('customer',) | refuses (`error` / `unknown`) | not-executed (`error`) | plan `unknown`: `'median' is not a scan operator (registry scans: ['cummax', 'cummin', 'cumsum', 'lag', 'lead', 'pct_change', 'rolling_mean', 'rolling_sum'])` | not covered (probe-only form; the gate reads Manual fenced blocks only) | `/tmp/conformance_probe.py` |
| `X-06` | `SELECT sum(level.last @ {store, day}) AS s AT {store}` | recognized | series=['sum(level.last @ {store, day})' AS s] anchor=('store',) | plans (`serve`) | **executes** (`serve`) | exec `provenance`: `'sum of level.last@{store*day}' reduced to store — pin fixes store, reduces over day` | not covered (probe-only form; the gate reads Manual fenced blocks only) | `/tmp/conformance_probe.py` |
| `X-07` | `SELECT count(revenue @ {transaction}) AS n AT {customer}` | recognized | series=['count(revenue @ {transaction})' AS n] anchor=('customer',) | plans (`serve`) | **executes** (`serve`) | exec `provenance`: `'count of revenue@transaction' reduced to customer — the count of revenue@transaction reading (input anchor pinned to 'transaction'), not the pooled value at customer` | not covered (probe-only form; the gate reads Manual fenced blocks only) | `/tmp/conformance_probe.py` |
| `X-08` | `SELECT mean(revenue @ {transaction}) AS n AT {customer}` | recognized | series=['mean(revenue @ {transaction})' AS n] anchor=('customer',) | plans (`serve`) | **executes** (`serve`) | exec `provenance`: `'mean of revenue@transaction' reduced to customer — the mean of revenue@transaction reading (input anchor pinned to 'transaction'), not the pooled value at customer` | not covered (probe-only form; the gate reads Manual fenced blocks only) | `/tmp/conformance_probe.py` |
| `X-09` | `SELECT cumsum( revenue @ {customer} ) AS c AT {customer}` | recognized | series=['cumsum( revenue @ {customer} )' AS c] anchor=('customer',) | plans (`serve`) | not-executed (`error`) | exec `unknown`: `scan 'cumsum' @ ('customer',) has no derivable order axis (no CERTIFIED temporal level in the anchor); name it with by=<level>. A declared-but-uncertified hierarchy confers no order axis — declaration makes structure eligible for certification, not executable.` | not covered (probe-only form; the gate reads Manual fenced blocks only) | `/tmp/conformance_probe.py` |
| `X-10` | `SELECT nosuchmeasure AT {customer}` | recognized | series=['nosuchmeasure'] anchor=('customer',) | refuses (`error` / `unknown`) | not-executed (`error`) | plan `unknown`: `unknown column 'nosuchmeasure'` | not covered (probe-only form; the gate reads Manual fenced blocks only) | `/tmp/conformance_probe.py`; test_nonexistent_measure.py::test_unknown_measure_is_error_not_silent |
| `X-11` | `SELECT frobnicate(revenue @ {transaction}) AS f AT {customer}` | recognized | series=['frobnicate(revenue @ {transaction})' AS f] anchor=('customer',) | refuses (`error` / `unknown`) | not-executed (`error`) | plan `unknown`: `'frobnicate' is not a scan operator (registry scans: ['cummax', 'cummin', 'cumsum', 'lag', 'lead', 'pct_change', 'rolling_mean', 'rolling_sum'])` | not covered (probe-only form; the gate reads Manual fenced blocks only) | `/tmp/conformance_probe.py` |

---

## 4. Subsections for the forms the table cannot carry

### 4.1 Scans — the Manual understates the build (`M-L940`, `P-13`, `P-13b`)

- **canonical status:** roadmap — §6.11 is fenced ```` ```frameql-roadmap ```` under a **[ROADMAP]** heading (`docs/frame_ql_manual_v2.md:933`), and §2.8 states *"Scan execution is not available in the current Core build"* (`:428`) and *"Parses and plans; does not execute"* (`:935`).
- **grammar recognition:** recognized.
- **parse result:** `series=['cumsum( revenue @ {customer, day} )' AS revenue_to_date] anchor=('customer','day')`.
- **planner support:** plans `serve`.
- **execution support:** **executes**, `serve`, with an immaterial `provenance` disclosure *"scan cumsum over order 'day' within ['customer']"*, and returns arithmetically correct running totals — `C1 2024-01-05 → 120.0`, `C1 2024-01-19 → 200.0`, `C2 → 200.0`, `C3 → 150.0`. `lag(… , n = 1)` likewise executes (`disclose`, with `undeclared_absence` for the three leading nulls).
- **Core Profile architectural compatibility:** compatible.
- **current Core build support:** **`supported`** — contradicting the Manual.
- **semantic-gate result:** the roadmap fence means the gate asserts only the section mark. It is *designed* not to pin today's behaviour, precisely so that shipping a capability does not turn the gate red — which is why the gate is green while the Manual is stale in the other direction.
- **disposition/reason:** none; it serves.
- **evidence:** `/tmp/conformance_probe.py` rows `M-L940`, `P-13`, `P-13b`; `/tmp/probe_detail.py` for the returned frames; `operators.py` registers `cumsum`/`cummax`/`cummin`/`lag`/`lead`/`pct_change` with `scan_impl=…` and `in_core=True` (only `rolling_sum`/`rolling_mean` carry `in_core=False`).
- **note:** §2.8's finer claim — that `reset =` / `step =` are unimplemented, so §6.13's two examples *"do not even plan"* — **is confirmed** (`M-L970`, `M-L978`). The stale claim is the blanket one about scan *execution*.

### 4.2 The envelope end to end (`M-L1008`) and what actually blocks it (`P-19`)

- **canonical status:** roadmap — **[SCHEDULED]** (`:999`), prose *"Plans; does not execute on this build … assembling a frame whose pinned levels are reached by separate hierarchies still fails in the engine"* (`:1001-1004`).
- **planner support:** plans `serve` (both series).
- **execution support:** **partial** — the frame comes back with `gross` computed for two rows (`east/S1 200.0`, `west/S2 200.0`) and a `provenance` disclosure, while `typical` carries `no_result` reason `unsupported`, detail *"this frame could not be resolved in the engine (ColumnNotFoundError); the ask is not supported in this build."*
- **the attribution the Manual does not make:** `P-19` reduces the example to `FROM retail SELECT revenue AT { region * store }` — no macro, no second grain, no `PER` — and it **still** fails with the same `unsupported`/`ColumnNotFoundError`. The residual is therefore *not* the composite input anchor, the two juxtaposed grains, or `PER ⊆ ORDER BY`; a bare anchor product whose levels are reached by separate hierarchies already fails. Anchor products elsewhere (`AT {customer, day}` on the finance fixture, `M-L374a`) execute normally. This narrows the rowed capability gap considerably.
- **Core Profile / build:** `compatible` / `unsupported-by-this-build`.
- **disposition judgement:** `OK-realization` — `unsupported` is registered `(ERROR, None)` at `disclosure.py:314` and is exactly the code Ruling §4 wants here. The leaked exception class name (`ColumnNotFoundError`, `AttributeError`) inside a user-facing detail string is a hygiene defect, not a jurisdiction error.

### 4.3 Query-level `count(*)` (`M-L579`, `M-L806`, `P-16`, `P-16b`)

- **canonical status:** roadmap, and more precisely **not canonically settled** — *"at least three readings are open … The Manual does not choose among them"* (`:820-824`); *"Resolving it is a language ruling, not a parser fix."*
- **grammar recognition:** **recognized** — the envelope parser accepts `count(*)` as verbatim series text.
- **planner support:** **raises**. `plan_statement` propagates a raw CPython `SyntaxError: Invalid star expression (<unknown>, line 1)`. The four-mood wire is never reached: the caller gets neither a Refuse, nor a Clarify, nor `unsupported`.
- **Core Profile architectural compatibility:** `n-a-not-canonical` — WD 0.2 §25 *"New syntax | Canonical admission only | **Cannot invent**"*. Core is right not to pick a reading; it is wrong to pick a Python traceback.
- **disposition judgement:** **MISLABELLED (no disposition at all)** — the worst cell in the matrix, because it is not a mis-chosen label but an absent one.
- **variant:** unaliased (`P-16b`), the planner gets one step further and reports *"cannot name series 'count(\*)' — give it a name with AS"* — a **naming** complaint standing in front of an unresolved-architecture form.

### 4.4 The bracket filter (`M-L874`, `P-14`) — and a Manual claim that is itself wrong

- **canonical status:** roadmap — §6.7 **[ROADMAP]**; §2.8 asserts *"The bracket filter is not shipped at all. `revenue[region = "east"]` **does not parse**."* (`:424`).
- **grammar recognition:** **recognized.** The envelope parser accepts it: `series=['revenue[region = "east"]' AS east_revenue; 'revenue' AS total_revenue]`. §2.8's claim is false as stated — series-internal text is captured verbatim by the envelope grammar and delegated to the expression parser at plan time, so "does not parse" is true only of the *expression* parser, one stage later.
- **planner support:** **raises** — CPython `SyntaxError: invalid syntax. Maybe you meant '==' or ':=' instead of '='? (<unknown>, line 1)`. A Python diagnostic, offering Python's walrus operator, shown to a Frame-QL author.
- **disposition judgement:** **MISLABELLED (no disposition at all)**.

### 4.5 The one reason string that is wrong about the shipped registry (`P-17b`, `P-17c`, `P-18c`, `P-13d`, `X-01`, `X-05`, `X-11`, `M-L276`)

Every unresolvable call in a series lands on one fallback message:

> ``'<name>' is not a scan operator (registry scans: ['cummax', 'cummin', 'cumsum', 'lag', 'lead', 'pct_change', 'rolling_mean', 'rolling_sum'])``

I probed it with seven different names to establish what it actually means:

| probed name | what it really is | what the message says |
|---|---|---|
| `median` | a **registered REDUCER** in `operators.REGISTRY`, documented in Appendix A (`:1205`) | "is not a scan operator" |
| `distinct` | a **registered REDUCER**, the friendly spelling of the shipped HLL family | "is not a scan operator" |
| `approx_distinct` | the Manual's own Appendix-A spelling (`:1209`, *"Ships"*); the registry spells it `distinct`/`hll_*` | "is not a scan operator" |
| `rank` | in Appendix A's scan list (`:1233`), **absent from the registry** | "is not a scan operator" |
| `total` | §8.2's alias example; no alias surface ships (`:1161`) | "is not a scan operator" |
| `frobnicate` | genuinely unregistered | "is not a scan operator" |
| `op` | the §2.1 schematic's metasyntactic placeholder | "is not a scan operator" |

The string asserts a **kind mismatch the asker never claimed**, offers a menu of the wrong kind, and — for `median` and `distinct` — **denies a registered operator**. The Manual's §7.3 already specifies the right clarification (*"Unknown operator … What to clarify: a registered operator, or an extension of the registry"*, `:1089`) and distinguishes it from *"Family not declared"*; the shipped message matches neither. All seven are flagged **MISLABELLED**. (The *outcome* is defensible in most of these cases; it is the reason string that is analytically wrong.)

### 4.6 A macro in `WHERE` is not expanded (`P-12b`)

- **canonical status:** **admitted**. §4.5: *"A macro may be referenced in `SELECT` series, `WHERE`, `HAVING`, `ORDER BY`, and later `WITH` bindings"* (`:659`); *"Expansion is textual and happens before desugaring and type-checking"* (`:657`).
- **measured:** `FROM finance_manifold WITH d = day SELECT revenue AT {customer} WHERE d >= "2024-01-01"` plans and executes `clarify`, reason `filter_unreachable`, detail *"WHERE dimension 'd' cannot lawfully reach series 'revenue' — 'd' is not addressable in that series' universe 'sales' …"*, offering to fix it by choosing among `(customer, date, day, month, product, region, transaction, year)`.
- The identical predicate written out longhand (`P-06`, `WHERE day >= '2024-01-01'`) **serves**. So the binding is simply not substituted into `WHERE`, and the asker is told to repair a dimension that does not exist.
- **current Core build support:** `unsupported-by-this-build`. **disposition judgement: MISLABELLED** — a build gap (no expansion in `WHERE`) delivered as an analytical statement about the Manifold's reachability.

### 4.7 The `WHERE` axis, reconciled against the stack tip

My probe **agrees with the confirmed facts** in every particular and I found no disagreement to report:
`WHERE` on a base dimension plans `serve` **and executes** in both quote spellings (`M-L524`, `M-L537`, `M-L887`, `P-06`); `IN (…)` on a base dimension serves (`P-08`); a relationship-derived dimension is refused **before** execution with `filter_unsupported`, plan and run agreeing (`M-L560`, `M-L903`, `P-07`, `P-08b`), the detail ending *"The ask is lawful; the build cannot execute it."*; `filter_unsupported` is `(ERROR, None)` at `disclosure.py:232` and `filter_unreachable` is `(CLARIFY, AMBIGUOUS)` at `:243`. Per instruction, `filter_unsupported` is scored **OK-realization** and `filter_unreachable` **CONTESTED**, with the adjudication left to the disposition audit.

**A documentation gap in the same area:** `filter_unsupported` appears in the Manual only in the §4.1 sync note (`:531`), §4.1.1 (`:557`) and §6.8a (`:899`). Chapter 7's clarification/refusal catalogue names `filter_unreachable` (`:1091`) and **never learned `filter_unsupported`** — the catalogue readers are pointed at is missing the code the build actually emits for the §4.1.1 form.

### 4.8 Forms that could not be expressed without a fixture I do not have

Recorded honestly rather than guessed:

- **A declared `BLOCKED` lineage / the `blocked_reduction` refusal.** None of the three Manual fixtures declares `BLOCKED`, so the declared-bar half of DG-4 (`specs/family_law_capability_reusable_state_reconciliation_v0_2.md:207-211`) is **not-exercised by this probe**. It is exercised by the repo's own suite — `test_generated_family_law.py::test_direct_blocked_member_refuses_with_no_values`, `::test_every_laundering_spelling_refuses_identically` (both passing at this commit) — and that is the evidence cited, not a probe row. The *under-declared* half **is** probe-exercised and serves (`X-02`, `X-03`, `X-06`).
- **`WITHHOLD` / author hard stop, quarantined columns, authorization** (§7.3): no fixture declares them; **not-exercised**.
- **`variance`, `stddev`, `weighted_mean`, `mode`, `value_at_max/min`, `approx_quantile`, `approx_frequency`, `cumprod`, `ewm_mean`, `rolling_min/max/count`, `dense_rank`, `row_number`** — Appendix A names them; several are absent from `operators.REGISTRY` entirely. Only the ones listed in Table B were run; the rest are **not-exercised**.
- **`window = 7d`** (§2.8's duration literal): not probed; `P-13c` used `window = 2` and never reached window handling.

---

## 5. The discrepancies that matter

**D1 — canonical status `admitted`, current Core build support `no`.** Eight forms (Table A):
`P-05` (`SELECT (revenue @ {}) AS grand AT {}` — §2.6 broadcast, `unsupported`/`AttributeError`, while the same `@ {}` operand inside a ratio executes fine at `M-L401`/`M-L861`);
`P-12b` (macro in `WHERE`, §4.5 admits it explicitly — see §4.6);
`P-15` (multi-input reducer, which is §2.1's *canonical form*: *"inline reduction 'sum' takes exactly one column argument"*);
`P-17b`/`P-17c` (`approx_distinct` / `distinct` as inline reducers, Appendix A says the distinct family *Ships*);
`P-18c` (`median` inline — Appendix A lists it, `SERIES_REDUCERS` does not);
`P-19` (anchor product across separate hierarchies);
`X-09` (a scan with no derivable order axis, which §2.8 says *"is a clarification"* and the build reports as `error`/`unknown`).
None of these is architecturally incompatible with the Core Profile; all eight are §16 *"canonical meaning exists + Core build lacks realization → `unsupported`"*.

**D2 — canonical status `roadmap`, current Core build support `yes`.** Three forms — `M-L940`, `P-13`, `P-13b`. The Manual asserts twice, in §2.8 and §6.11, that scan **execution** is unavailable; `cumsum` and `lag` execute and return correct values. The gate cannot catch this by construction (roadmap fences assert the mark, never the behaviour), so the Manual can drift *understating* capability indefinitely. This is the mirror image of the failure Mission B closed and the gate has no guard for it.

**D3 — 20 forms carry an analytically wrong reason string.** Broken down: **seven** are the single "is not a scan operator" fallback misdescribing registered reducers, unregistered names, and a metasyntactic placeholder alike (§4.5); **four** are raw CPython `SyntaxError`s escaping the planner entirely, so no disposition is issued at all (`count(*)` ×3, bracket filter ×2 — `M-L579`, `M-L806`, `P-16`, `M-L874`, `P-14`); **three** report a *build* gap as a *vocabulary* gap (`reset=`, `step=`, `window=` → reason `unknown`, *"unknown parameter"*, when `operators.py` declares those parameters and marks the mechanics absent); **two** mis-attribute (`M-L1168`/`P-16b` answer a naming question in front of an unknown-operator / unresolved-architecture one); **one** reports a missing expansion as unreachability (`P-12b`); **one** contradicts §2.8's own Clarify rule for a missing order (`X-09`).

**D4 — the gate has nine blind spots.** `check_manual_frameql.py` covers 40 of the Manual's 44 fenced blocks; it skips every block whose first line is not `EXPLAIN`/`FROM`/`WITH`/`SELECT` — the §1.2 skeleton (`L117`), the §1.3 `FROM` fragment (`L137`, ```` ```text ````), both sugar illustrations (`L474`, `L495`), all three clause fragments (`L609`, `L621`, `L630`), §5.6's `RELATE` declaration (`L747`) and Appendix D's retired form (`L1283`). Two of those are load-bearing teaching: the §3.1/§3.2 sugar pairs are the language's *only* worked statement of what the default-family and omit-root sugars expand to, and nothing checks them. (I ran all nine anyway; they behave as fragments should.)

**D5 — three smaller ones.** (a) `pyproject.toml` says `0.18.1`, `__init__.py` says `0.16.0-core`; the Manual cites `0.18.1` in four places. (b) Chapter 7's catalogue never learned `filter_unsupported` (§4.7). (c) §2.8's *"the bracket filter … does not parse"* is false at the envelope layer (§4.4).

**What is NOT wrong.** `filter_unsupported`, `unsupported`, and the whole §4.1/§4.1.1 split are correctly jurisdictioned and should not be touched. The M:N face trio (`M-L756a/b/c`) plans, executes, and discloses exactly what §5.6 documents. The `PER` laws (`P-11c`, `P-11d`) are enforced with genuinely good remedy strings. The HLL/distinct family (`P-17`) executes and discloses `approximation` with a quantified `rel_error` — WD 0.2 §25's *"state construction / combination / finalization: Core may realize"*, realized.

---

## Appendix A — verbatim output of `/tmp/conformance_probe.py`

Command (run at the repo root):

```
PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH=/data/repos/978ea3c9feee4ad79341d42517782efd/columna/packages/columna-core/src \
  /tmp/fqvenv/bin/python /tmp/conformance_probe.py
```

One JSON object per form, exactly as printed (exit 0, empty stderr):

```json
{"id": "M-L117", "label": "Ch1.2 envelope skeleton (metasyntax, bare fence)", "query": "[EXPLAIN] [FROM <manifold>] [WITH <name> = <expression> [, ...]] SELECT <series_1> [AS <alias_1>], <series_2> [AS <alias_2>], ... AT { <output_anchor> } [WHERE <per-series predicate> [AND ...]] [HAVING <output-frame predicate> [AND ...]] [ORDER BY <output-frame column> [ASC|DESC] [, ...]] [LIMIT n [PER { <anchor coordinates> }]]", "grammar": "not-recognized", "parse": "EnvelopeSyntaxError: AT needs a braced anchor \u2014 write AT { level } (the braces say the anchor is a product of levels), e.g. AT {region*store}; got '{ <output_anchor> }\\n[WHERE  <per-series predicate> [AND ...]]\\n[HAVING <output-frame predicate> [AND ...]]\\n[ORDER BY <output-frame column> [ASC|DESC] [, ...]]\\n[LIMIT  n [PER { <anchor coordinates> }]]'", "manifold": null, "plan": "not-exercised", "plan_reason": null, "plan_message": null, "exec": "not-exercised", "exec_reason": null, "exec_message": null}
{"id": "M-L137", "label": "Ch1.3 FROM clause fragment (```text fence)", "query": "FROM finance_manifold", "grammar": "not-recognized", "parse": "EnvelopeSyntaxError: a query must SELECT at least one series \u2014 e.g. SELECT revenue AT {region}", "manifold": null, "plan": "not-exercised", "plan_reason": null, "plan_message": null, "exec": "not-exercised", "exec_reason": null, "exec_message": null}
{"id": "M-L158", "label": "Ch1.4 two pinned reducers at one anchor", "query": "SELECT sum(revenue @ {transaction}), sum(cost @ {transaction}) AT {customer}", "grammar": "recognized", "parse": "series=['sum(revenue @ {transaction})'; 'sum(cost @ {transaction})'] anchor=('customer',)", "manifold": "finance_manifold", "plan": "serve", "plan_reason": null, "plan_message": "", "exec": "executes:serve", "exec_reason": "provenance", "exec_message": "'sum of revenue@transaction' reduced to customer \u2014 the sum of revenue@transaction reading (input anchor pinned to 'transaction'), not the pooled value at customer"}
{"id": "M-L202", "label": "Ch1.6 AS alias + map series", "query": "SELECT revenue AS total_revenue, (revenue - cost) AS profit AT {customer}", "grammar": "recognized", "parse": "series=['revenue' AS total_revenue; '(revenue - cost)' AS profit] anchor=('customer',)", "manifold": "finance_manifold", "plan": "serve", "plan_reason": null, "plan_message": "", "exec": "executes:serve", "exec_reason": null, "exec_message": ""}
{"id": "M-L250", "label": "Ch1.7 EXPLAIN statement", "query": "EXPLAIN FROM finance_manifold SELECT max( sum(revenue @ {transaction}) @ {customer, month} ) AS peak_month AT {customer}", "grammar": "recognized", "parse": "EXPLAIN FROM=finance_manifold series=['max( sum(revenue @ {transaction}) @ {customer, month} )' AS peak_month] anchor=('customer',)", "manifold": "finance_manifold", "plan": "serve", "plan_reason": null, "plan_message": "", "exec": "executes:serve", "exec_reason": "provenance", "exec_message": "'sum of revenue@transaction' reduced to customer*month \u2014 the sum of revenue@transaction reading (input anchor pinned to 'transaction'), not the pooled value at customer*month"}
{"id": "M-L276", "label": "Ch2.1 multi-input reducer SCHEMATIC (metasyntactic template)", "query": "SELECT op( col_1 @ {a_1}, col_2 @ {a_2}, ... ) AS name AT { A }", "grammar": "recognized", "parse": "series=['op( col_1 @ {a_1}, col_2 @ {a_2}, ... )' AS name] anchor=('A',)", "manifold": "finance_manifold", "plan": "error", "plan_reason": "unknown", "plan_message": "'op' is not a scan operator (registry scans: ['cummax', 'cummin', 'cumsum', 'lag', 'lead', 'pct_change', 'rolling_mean', 'rolling_sum'])", "exec": "executes:error", "exec_reason": "unknown", "exec_message": "'op' is not a scan operator (registry scans: ['cummax', 'cummin', 'cumsum', 'lag', 'lead', 'pct_change', 'rolling_mean', 'rolling_sum'])"}
{"id": "M-L315a", "label": "Ch2.3 single reducer sum, explicit input pin", "query": "SELECT sum(revenue @ {transaction}) AS gross AT {customer}", "grammar": "recognized", "parse": "series=['sum(revenue @ {transaction})' AS gross] anchor=('customer',)", "manifold": "finance_manifold", "plan": "serve", "plan_reason": null, "plan_message": "", "exec": "executes:serve", "exec_reason": "provenance", "exec_message": "'sum of revenue@transaction' reduced to customer \u2014 the sum of revenue@transaction reading (input anchor pinned to 'transaction'), not the pooled value at customer"}
{"id": "M-L315b", "label": "Ch2.3 single reducer max, explicit input pin (non-family/generated reducer)", "query": "SELECT max(revenue @ {transaction}) AS peak_txn AT {customer}", "grammar": "recognized", "parse": "series=['max(revenue @ {transaction})' AS peak_txn] anchor=('customer',)", "manifold": "finance_manifold", "plan": "serve", "plan_reason": null, "plan_message": "", "exec": "executes:serve", "exec_reason": "provenance", "exec_message": "'max of revenue@transaction' reduced to customer \u2014 the max of revenue@transaction reading (input anchor pinned to 'transaction'), not the pooled value at customer"}
{"id": "M-L315c", "label": "Ch2.3 single reducer avg on a DERIVED column, explicit input pin", "query": "SELECT avg(aov @ {day}) AS typical AT {customer}", "grammar": "recognized", "parse": "series=['avg(aov @ {day})' AS typical] anchor=('customer',)", "manifold": "finance_manifold", "plan": "serve", "plan_reason": null, "plan_message": "", "exec": "executes:serve", "exec_reason": "provenance", "exec_message": "'mean of aov@day' reduced to customer \u2014 the mean of aov@day reading (input anchor pinned to 'day'), not the pooled value at customer"}
{"id": "M-L325", "label": "Ch2.3 unpinned reducer on a derived column (documented clarify)", "query": "SELECT avg(aov) AT {region}", "grammar": "recognized", "parse": "series=['avg(aov)'] anchor=('region',)", "manifold": "finance_manifold", "plan": "clarify", "plan_reason": "input_anchor_ambiguous", "plan_message": "inline reduction 'mean(aov)' does not pin its input anchor \u2014 the grain to resolve 'aov' at before reducing to region is underdetermined; pin it, e.g. 'mean(aov@customer)'", "exec": "executes:clarify", "exec_reason": "input_anchor_ambiguous", "exec_message": "inline reduction 'mean(aov)' does not pin its input anchor \u2014 the grain to resolve 'aov' at before reducing to region is underdetermined; pin it, e.g. 'mean(aov@customer)'"}
{"id": "M-L374a", "label": "Ch2.4 map of two pinned columns", "query": "SELECT (revenue @ {customer, day}) - (cost @ {customer, day}) AS profit AT {customer, day}", "grammar": "recognized", "parse": "series=['(revenue @ {customer, day}) - (cost @ {customer, day})' AS profit] anchor=('customer', 'day')", "manifold": "finance_manifold", "plan": "serve", "plan_reason": null, "plan_message": "", "exec": "executes:serve", "exec_reason": null, "exec_message": ""}
{"id": "M-L374b", "label": "Ch2.4 map ratio of two pinned columns", "query": "SELECT (revenue @ {transaction}) / (orders @ {transaction}) AS aov AT {transaction}", "grammar": "recognized", "parse": "series=['(revenue @ {transaction}) / (orders @ {transaction})' AS aov] anchor=('transaction',)", "manifold": "finance_manifold", "plan": "serve", "plan_reason": null, "plan_message": "", "exec": "executes:serve", "exec_reason": null, "exec_message": ""}
{"id": "M-L389", "label": "Ch2.5 two universes juxtaposed in one frame", "query": "SELECT revenue AS revenue, level.last AS inv AT {region}", "grammar": "recognized", "parse": "series=['revenue' AS revenue; 'level.last' AS inv] anchor=('region',)", "manifold": "finance_manifold", "plan": "serve", "plan_reason": null, "plan_message": "", "exec": "executes:serve", "exec_reason": null, "exec_message": ""}
{"id": "M-L401", "label": "Ch2.6 broadcast: `@ {}` scalar input anchor", "query": "SELECT (revenue @ {customer}) / (revenue @ {}) AS share_of_total AT {customer}", "grammar": "recognized", "parse": "series=['(revenue @ {customer}) / (revenue @ {})' AS share_of_total] anchor=('customer',)", "manifold": "finance_manifold", "plan": "serve", "plan_reason": null, "plan_message": "", "exec": "executes:serve", "exec_reason": null, "exec_message": ""}
{"id": "M-L413", "label": "Ch2.7 composite reduction (nested pin)", "query": "SELECT max( sum(revenue @ {transaction}) @ {customer, month} ) AS peak_month AT {customer}", "grammar": "recognized", "parse": "series=['max( sum(revenue @ {transaction}) @ {customer, month} )' AS peak_month] anchor=('customer',)", "manifold": "finance_manifold", "plan": "serve", "plan_reason": null, "plan_message": "", "exec": "executes:serve", "exec_reason": "provenance", "exec_message": "'sum of revenue@transaction' reduced to customer*month \u2014 the sum of revenue@transaction reading (input anchor pinned to 'transaction'), not the pooled value at customer*month"}
{"id": "M-L474", "label": "Ch3.1 default-family sugar FRAGMENT (no SELECT keyword)", "query": "revenue AT {customer}", "grammar": "not-recognized", "parse": "EnvelopeSyntaxError: a query must SELECT at least one series \u2014 e.g. SELECT revenue AT {region}", "manifold": null, "plan": "not-exercised", "plan_reason": null, "plan_message": null, "exec": "not-exercised", "exec_reason": null, "exec_message": null}
{"id": "M-L474b", "label": "Ch3.1 sugar fragment, canonical half", "query": "sum(revenue @ {transaction}) AT {customer}", "grammar": "not-recognized", "parse": "EnvelopeSyntaxError: a query must SELECT at least one series \u2014 e.g. SELECT revenue AT {region}", "manifold": null, "plan": "not-exercised", "plan_reason": null, "plan_message": null, "exec": "not-exercised", "exec_reason": null, "exec_message": null}
{"id": "M-L495", "label": "Ch3.2 omit-root sugar FRAGMENT (no SELECT keyword)", "query": "sum(revenue) AT {customer}", "grammar": "not-recognized", "parse": "EnvelopeSyntaxError: a query must SELECT at least one series \u2014 e.g. SELECT revenue AT {region}", "manifold": null, "plan": "not-exercised", "plan_reason": null, "plan_message": null, "exec": "not-exercised", "exec_reason": null, "exec_message": null}
{"id": "M-L524", "label": "Ch4.1 WHERE on a base dimension (sugared series)", "query": "FROM finance_manifold SELECT revenue AT {customer} WHERE day >= \"2024-01-01\"", "grammar": "recognized", "parse": "FROM=finance_manifold series=['revenue'] anchor=('customer',) where=['day >= \"2024-01-01\"']", "manifold": "finance_manifold", "plan": "serve", "plan_reason": null, "plan_message": "", "exec": "executes:serve", "exec_reason": null, "exec_message": ""}
{"id": "M-L537", "label": "Ch4.1 WHERE on a base dimension (canonical series)", "query": "FROM finance_manifold SELECT sum(revenue @ {transaction}) AT {customer} WHERE day >= \"2024-01-01\"", "grammar": "recognized", "parse": "FROM=finance_manifold series=['sum(revenue @ {transaction})'] anchor=('customer',) where=['day >= \"2024-01-01\"']", "manifold": "finance_manifold", "plan": "serve", "plan_reason": null, "plan_message": "", "exec": "executes:serve", "exec_reason": "provenance", "exec_message": "'sum of revenue@transaction' reduced to customer \u2014 the sum of revenue@transaction reading (input anchor pinned to 'transaction'), not the pooled value at customer"}
{"id": "M-L560", "label": "Ch4.1.1 WHERE through a relationship-derived dimension [SCHEDULED]", "query": "FROM finance_manifold SELECT sum(revenue @ {transaction}) AT {customer} WHERE region = \"east\" AND date >= \"2024-01-01\"", "grammar": "recognized", "parse": "FROM=finance_manifold series=['sum(revenue @ {transaction})'] anchor=('customer',) where=['region = \"east\"', 'date >= \"2024-01-01\"']", "manifold": "finance_manifold", "plan": "error", "plan_reason": "filter_unsupported", "plan_message": "WHERE dimension 'region' is addressable in universe 'sales' but is not one of its base dimensions (customer, day, transaction), and this build pushes the filter to the measure's own source, which carries the base coordinates only. The ask is lawful; the build cannot execute it.", "exec": "executes:error", "exec_reason": "filter_unsupported", "exec_message": "WHERE dimension 'region' is addressable in universe 'sales' but is not one of its base dimensions (customer, day, transaction), and this build pushes the filter to the measure's own source, which carries the base coordinates only. The ask is lawful; the build cannot execute it."}
{"id": "M-L579", "label": "Ch4.2 HAVING + query-level count(*) [ROADMAP]", "query": "FROM finance_manifold SELECT sum(revenue) AS total_revenue, count(*) AS transaction_count AT {customer} HAVING total_revenue > 10000", "grammar": "recognized", "parse": "FROM=finance_manifold series=['sum(revenue)' AS total_revenue; 'count(*)' AS transaction_count] anchor=('customer',) having=['total_revenue > 10000']", "manifold": "finance_manifold", "plan": "raises", "plan_reason": "SyntaxError", "plan_message": "Invalid star expression (<unknown>, line 1)", "exec": "not-exercised", "exec_reason": null, "exec_message": null}
{"id": "M-L609", "label": "Ch4.3 ORDER BY clause FRAGMENT", "query": "ORDER BY total_revenue DESC, customer ASC", "grammar": "not-recognized", "parse": "EnvelopeSyntaxError: a query must SELECT at least one series \u2014 e.g. SELECT revenue AT {region}", "manifold": null, "plan": "not-exercised", "plan_reason": null, "plan_message": null, "exec": "not-exercised", "exec_reason": null, "exec_message": null}
{"id": "M-L621", "label": "Ch4.4 LIMIT clause FRAGMENT", "query": "ORDER BY total_revenue DESC LIMIT 100", "grammar": "not-recognized", "parse": "EnvelopeSyntaxError: a query must SELECT at least one series \u2014 e.g. SELECT revenue AT {region}", "manifold": null, "plan": "not-exercised", "plan_reason": null, "plan_message": null, "exec": "not-exercised", "exec_reason": null, "exec_message": null}
{"id": "M-L630", "label": "Ch4.4 LIMIT n PER {dims} FRAGMENT", "query": "ORDER BY region, total_revenue DESC LIMIT 5 PER {region}", "grammar": "not-recognized", "parse": "EnvelopeSyntaxError: a query must SELECT at least one series \u2014 e.g. SELECT revenue AT {region}", "manifold": null, "plan": "not-exercised", "plan_reason": null, "plan_message": null, "exec": "not-exercised", "exec_reason": null, "exec_message": null}
{"id": "M-L665", "label": "Ch4.5 WITH macro binding", "query": "FROM finance_manifold WITH profit = (revenue - cost) SELECT profit AT {customer, month}", "grammar": "recognized", "parse": "FROM=finance_manifold series=['profit'] anchor=('customer', 'month') bindings=[Binding(name='profit', expr='(revenue - cost)')]", "manifold": "finance_manifold", "plan": "serve", "plan_reason": null, "plan_message": "", "exec": "executes:serve", "exec_reason": null, "exec_message": ""}
{"id": "M-L747", "label": "Ch5.6 RELATE ... FACES declaration (CML, not Frame-QL)", "query": "RELATE product <-> category VIA product_categories(product_id, category_id) FACES { touch = TOUCH assign = ASSIGN BY category_rank ORDER MIN alloc = ALLOC BY category_weight } NOTE \"a product belongs to up to 3 categories\"", "grammar": "not-recognized", "parse": "EnvelopeSyntaxError: a query must SELECT at least one series \u2014 e.g. SELECT revenue AT {region}", "manifold": null, "plan": "not-exercised", "plan_reason": null, "plan_message": null, "exec": "not-exercised", "exec_reason": null, "exec_message": null}
{"id": "M-L756a", "label": "Ch5.6 many-to-many face: TOUCH", "query": "SELECT revenue AT {category.touch}", "grammar": "recognized", "parse": "series=['revenue'] anchor=('category.touch',)", "manifold": "finance_manifold", "plan": "serve", "plan_reason": null, "plan_message": "", "exec": "executes:disclose", "exec_reason": "multi_counted", "exec_message": "multi-counted by construction across product<->category: revenue reaches every category a product sits in \u2014 multi-counted; totals exceed the grand total"}
{"id": "M-L756b", "label": "Ch5.6 many-to-many face: ASSIGN", "query": "SELECT revenue AT {category.assign}", "grammar": "recognized", "parse": "series=['revenue'] anchor=('category.assign',)", "manifold": "finance_manifold", "plan": "serve", "plan_reason": null, "plan_message": "", "exec": "executes:disclose", "exec_reason": "memberships_unrepresented", "exec_message": "single-counted to each product's ORDER min category_rank category: 1 memberships unrepresented (the shadow). revenue lands in the product's single primary category; the rest disclosed as the shadow"}
{"id": "M-L756c", "label": "Ch5.6 many-to-many face: ALLOC", "query": "SELECT revenue AT {category.alloc}", "grammar": "recognized", "parse": "series=['revenue'] anchor=('category.alloc',)", "manifold": "finance_manifold", "plan": "serve", "plan_reason": null, "plan_message": "", "exec": "executes:serve", "exec_reason": "reconciliation", "exec_message": "allocated by normalized category_weight: crossed total 550.00 reconciles to the grand total 550.00 (delta 0.0000). revenue splits across a product's categories by weight; totals reconcile to the grand total"}
{"id": "M-L795", "label": "Ch6.1 simple aggregation (default-family sugar)", "query": "FROM finance_manifold SELECT revenue AT {customer}", "grammar": "recognized", "parse": "FROM=finance_manifold series=['revenue'] anchor=('customer',)", "manifold": "finance_manifold", "plan": "serve", "plan_reason": null, "plan_message": "", "exec": "executes:serve", "exec_reason": null, "exec_message": ""}
{"id": "M-L806", "label": "Ch6.2 multiple metrics + query-level count(*) [ROADMAP]", "query": "FROM finance_manifold SELECT revenue, cost, count(*) AS transaction_count AT {customer, month}", "grammar": "recognized", "parse": "FROM=finance_manifold series=['revenue'; 'cost'; 'count(*)' AS transaction_count] anchor=('customer', 'month')", "manifold": "finance_manifold", "plan": "raises", "plan_reason": "SyntaxError", "plan_message": "Invalid star expression (<unknown>, line 1)", "exec": "not-exercised", "exec_reason": null, "exec_message": null}
{"id": "M-L833", "label": "Ch6.3 composite reduction with explicit intermediate anchor", "query": "FROM finance_manifold SELECT max( sum(revenue @ {transaction}) @ {customer, month} ) AS max_monthly_revenue AT {customer}", "grammar": "recognized", "parse": "FROM=finance_manifold series=['max( sum(revenue @ {transaction}) @ {customer, month} )' AS max_monthly_revenue] anchor=('customer',)", "manifold": "finance_manifold", "plan": "serve", "plan_reason": null, "plan_message": "", "exec": "executes:serve", "exec_reason": "provenance", "exec_message": "'sum of revenue@transaction' reduced to customer*month \u2014 the sum of revenue@transaction reading (input anchor pinned to 'transaction'), not the pooled value at customer*month"}
{"id": "M-L843", "label": "Ch6.4 mean with explicit input anchor", "query": "FROM product_manifold SELECT mean( engagement_score @ {customer, week} ) AT {customer}", "grammar": "recognized", "parse": "FROM=product_manifold series=['mean( engagement_score @ {customer, week} )'] anchor=('customer',)", "manifold": "product_manifold", "plan": "serve", "plan_reason": null, "plan_message": "", "exec": "executes:serve", "exec_reason": "provenance", "exec_message": "'mean of engagement_score@{customer*week}' reduced to customer \u2014 pin fixes customer, reduces over week"}
{"id": "M-L852", "label": "Ch6.5 map of co-anchored columns", "query": "FROM finance_manifold SELECT (revenue - cost) AS profit AT {customer, day}", "grammar": "recognized", "parse": "FROM=finance_manifold series=['(revenue - cost)' AS profit] anchor=('customer', 'day')", "manifold": "finance_manifold", "plan": "serve", "plan_reason": null, "plan_message": "", "exec": "executes:serve", "exec_reason": null, "exec_message": ""}
{"id": "M-L861", "label": "Ch6.6 ratio across grains (`@ {}` denominator)", "query": "FROM finance_manifold SELECT ( revenue @ {customer} ) / ( revenue @ {} ) AS share_of_total AT {customer}", "grammar": "recognized", "parse": "FROM=finance_manifold series=['( revenue @ {customer} ) / ( revenue @ {} )' AS share_of_total] anchor=('customer',)", "manifold": "finance_manifold", "plan": "serve", "plan_reason": null, "plan_message": "", "exec": "executes:serve", "exec_reason": null, "exec_message": ""}
{"id": "M-L874", "label": "Ch6.7 bracket filter on a column [ROADMAP]", "query": "FROM finance_manifold SELECT revenue[region = \"east\"] AS east_revenue, revenue AS total_revenue AT {customer}", "grammar": "recognized", "parse": "FROM=finance_manifold series=['revenue[region = \"east\"]' AS east_revenue; 'revenue' AS total_revenue] anchor=('customer',)", "manifold": "finance_manifold", "plan": "raises", "plan_reason": "SyntaxError", "plan_message": "invalid syntax. Maybe you meant '==' or ':=' instead of '='? (<unknown>, line 1)", "exec": "not-exercised", "exec_reason": null, "exec_message": null}
{"id": "M-L887", "label": "Ch6.8 WHERE on a base dimension", "query": "FROM finance_manifold SELECT revenue AT {customer} WHERE day >= \"2024-01-01\"", "grammar": "recognized", "parse": "FROM=finance_manifold series=['revenue'] anchor=('customer',) where=['day >= \"2024-01-01\"']", "manifold": "finance_manifold", "plan": "serve", "plan_reason": null, "plan_message": "", "exec": "executes:serve", "exec_reason": null, "exec_message": ""}
{"id": "M-L903", "label": "Ch6.8a WHERE joined dimension + IN (...) [SCHEDULED]", "query": "FROM finance_manifold SELECT revenue AT {customer} WHERE date >= \"2024-01-01\" AND region IN (\"east\", \"west\")", "grammar": "recognized", "parse": "FROM=finance_manifold series=['revenue'] anchor=('customer',) where=['date >= \"2024-01-01\"', 'region IN (\"east\", \"west\")']", "manifold": "finance_manifold", "plan": "error", "plan_reason": "filter_unsupported", "plan_message": "WHERE dimension 'date' is addressable in universe 'sales' but is not one of its base dimensions (customer, day, transaction), and this build pushes the filter to the measure's own source, which carries the base coordinates only. The ask is lawful; the build cannot execute it.", "exec": "executes:error", "exec_reason": "filter_unsupported", "exec_message": "WHERE dimension 'date' is addressable in universe 'sales' but is not one of its base dimensions (customer, day, transaction), and this build pushes the filter to the measure's own source, which carries the base coordinates only. The ask is lawful; the build cannot execute it."}
{"id": "M-L914", "label": "Ch6.9 HAVING on an output column", "query": "FROM finance_manifold SELECT revenue AS total_revenue AT {customer} HAVING total_revenue > 50000", "grammar": "recognized", "parse": "FROM=finance_manifold series=['revenue' AS total_revenue] anchor=('customer',) having=['total_revenue > 50000']", "manifold": "finance_manifold", "plan": "serve", "plan_reason": null, "plan_message": "", "exec": "executes:serve", "exec_reason": null, "exec_message": ""}
{"id": "M-L924", "label": "Ch6.10 top-N per group (ORDER BY + LIMIT n PER)", "query": "FROM product_manifold SELECT product_revenue AT {category, product} ORDER BY category, product_revenue DESC LIMIT 5 PER {category}", "grammar": "recognized", "parse": "FROM=product_manifold series=['product_revenue'] anchor=('category', 'product') order_by=[OrderKey(column='category', descending=False), OrderKey(column='product_revenue', descending=True)] limit=Limit(n=5, per=('category',))", "manifold": "product_manifold", "plan": "serve", "plan_reason": null, "plan_message": "", "exec": "executes:serve", "exec_reason": null, "exec_message": ""}
{"id": "M-L940", "label": "Ch6.11 scan: cumsum running total [ROADMAP]", "query": "FROM finance_manifold SELECT cumsum( revenue @ {customer, day} ) AS revenue_to_date AT {customer, day}", "grammar": "recognized", "parse": "FROM=finance_manifold series=['cumsum( revenue @ {customer, day} )' AS revenue_to_date] anchor=('customer', 'day')", "manifold": "finance_manifold", "plan": "serve", "plan_reason": null, "plan_message": "", "exec": "executes:serve", "exec_reason": "provenance", "exec_message": "scan cumsum over order 'day' within ['customer']"}
{"id": "M-L955", "label": "Ch6.12 WITH allocation ... [marked frameql-illformed]", "query": "FROM product_manifold WITH allocation product_to_category = proportional_to(category_weight) SELECT sum( revenue @ {product} ) AT {category}", "grammar": "not-recognized", "parse": "EnvelopeSyntaxError: expected a single name for a WITH name, got 'allocation product_to_category'", "manifold": null, "plan": "not-exercised", "plan_reason": null, "plan_message": null, "exec": "not-exercised", "exec_reason": null, "exec_message": null}
{"id": "M-L970", "label": "Ch6.13a scan with family-aware `reset =` [ROADMAP]", "query": "FROM finance_manifold SELECT cumsum( revenue @ {customer, day}, reset = year ) AS revenue_ytd AT {customer, day}", "grammar": "recognized", "parse": "FROM=finance_manifold series=['cumsum( revenue @ {customer, day}, reset = year )' AS revenue_ytd] anchor=('customer', 'day')", "manifold": "finance_manifold", "plan": "error", "plan_reason": "unknown", "plan_message": "scan 'cumsum': unknown parameter 'reset' (accepts n=, by=)", "exec": "executes:error", "exec_reason": "unknown", "exec_message": "scan 'cumsum': unknown parameter 'reset' (accepts n=, by=)"}
{"id": "M-L978", "label": "Ch6.13b scan with family-aware `step =` (lag) [ROADMAP]", "query": "FROM finance_manifold SELECT ( revenue - lag(revenue, 1, step = year) ) / lag(revenue, 1, step = year) AS yoy_growth AT {customer, month}", "grammar": "recognized", "parse": "FROM=finance_manifold series=['( revenue - lag(revenue, 1, step = year) ) / lag(revenue, 1, step = year)' AS yoy_growth] anchor=('customer', 'month')", "manifold": "finance_manifold", "plan": "error", "plan_reason": "unknown", "plan_message": "scan 'lag' takes one input expression and keyword params (n=, by=)", "exec": "executes:error", "exec_reason": "unknown", "exec_message": "scan 'lag' takes one input expression and keyword params (n=, by=)"}
{"id": "M-L988", "label": "Ch6.14 macro + HAVING + ORDER BY + LIMIT", "query": "FROM finance_manifold WITH profit = (revenue - cost) SELECT profit AT {customer, month} HAVING profit > 0 ORDER BY profit DESC LIMIT 10", "grammar": "recognized", "parse": "FROM=finance_manifold series=['profit'] anchor=('customer', 'month') bindings=[Binding(name='profit', expr='(revenue - cost)')] having=['profit > 0'] order_by=[OrderKey(column='profit', descending=True)] limit=Limit(n=10, per=())", "manifold": "finance_manifold", "plan": "serve", "plan_reason": null, "plan_message": "", "exec": "executes:serve", "exec_reason": null, "exec_message": ""}
{"id": "M-L1008", "label": "Ch6.15 the envelope end to end [SCHEDULED]", "query": "FROM retail WITH line = revenue @ {transaction} SELECT sum(line) AS gross, avg(aov @ {day}) AS typical AT { region * store } ORDER BY region, gross DESC LIMIT 3 PER { region }", "grammar": "recognized", "parse": "FROM=retail series=['sum(line)' AS gross; 'avg(aov @ {day})' AS typical] anchor=('region', 'store') bindings=[Binding(name='line', expr='revenue @ {transaction}')] order_by=[OrderKey(column='region', descending=False), OrderKey(column='gross', descending=True)] limit=Limit(n=3, per=('region',))", "manifold": "retail_manifold", "plan": "serve", "plan_reason": null, "plan_message": "", "exec": "executes:error", "exec_reason": "unsupported", "exec_message": "this frame could not be resolved in the engine (ColumnNotFoundError); the ask is not supported in this build."}
{"id": "M-L1027", "label": "Ch6.16 composite input anchor, two-stage statistic [SCHEDULED]", "query": "FROM retail SELECT avg( revenue @ {store*product*cal.month} ) AS avg_monthly_product_revenue AT {store}", "grammar": "recognized", "parse": "FROM=retail series=['avg( revenue @ {store*product*cal.month} )' AS avg_monthly_product_revenue] anchor=('store',)", "manifold": "retail_manifold", "plan": "serve", "plan_reason": null, "plan_message": "", "exec": "executes:error", "exec_reason": "unsupported", "exec_message": "this frame could not be resolved in the engine (ColumnNotFoundError); the ask is not supported in this build."}
{"id": "M-L1168", "label": "Ch8.2 operator name aliases [ROADMAP]", "query": "FROM retail_manifold SELECT total(revenue), unique_visitors AT {store}", "grammar": "recognized", "parse": "FROM=retail_manifold series=['total(revenue)'; 'unique_visitors'] anchor=('store',)", "manifold": "retail_manifold", "plan": "raises", "plan_reason": "FrameQLSyntaxError", "plan_message": "series 'total(revenue)' has no derivable name \u2014 give it one with AS (e.g. SELECT total(revenue) AS my_name)", "exec": "not-exercised", "exec_reason": null, "exec_message": null}
{"id": "M-L1283", "label": "App.D retired terse trailing-@ fragment (negative example)", "query": "aov @ cal.month", "grammar": "not-recognized", "parse": "EnvelopeSyntaxError: a query must SELECT at least one series \u2014 e.g. SELECT revenue AT {region}", "manifold": null, "plan": "not-exercised", "plan_reason": null, "plan_message": null, "exec": "not-exercised", "exec_reason": null, "exec_message": null}
{"id": "P-01", "label": "single reducer, sugared, no FROM", "query": "SELECT revenue AT {customer}", "grammar": "recognized", "parse": "series=['revenue'] anchor=('customer',)", "manifold": "finance_manifold", "plan": "serve", "plan_reason": null, "plan_message": "", "exec": "executes:serve", "exec_reason": null, "exec_message": ""}
{"id": "P-02", "label": "map of two bare (sugared) columns", "query": "SELECT (revenue - cost) AS profit AT {customer}", "grammar": "recognized", "parse": "series=['(revenue - cost)' AS profit] anchor=('customer',)", "manifold": "finance_manifold", "plan": "serve", "plan_reason": null, "plan_message": "", "exec": "executes:serve", "exec_reason": null, "exec_message": ""}
{"id": "P-03", "label": "explicit input pin, single level", "query": "SELECT sum(revenue @ {transaction}) AT {customer}", "grammar": "recognized", "parse": "series=['sum(revenue @ {transaction})'] anchor=('customer',)", "manifold": "finance_manifold", "plan": "serve", "plan_reason": null, "plan_message": "", "exec": "executes:serve", "exec_reason": "provenance", "exec_message": "'sum of revenue@transaction' reduced to customer \u2014 the sum of revenue@transaction reading (input anchor pinned to 'transaction'), not the pooled value at customer"}
{"id": "P-04", "label": "composite input anchor (product pin) on finance fixture", "query": "SELECT avg( revenue @ {customer, day} ) AS typical_day AT {customer}", "grammar": "recognized", "parse": "series=['avg( revenue @ {customer, day} )' AS typical_day] anchor=('customer',)", "manifold": "finance_manifold", "plan": "serve", "plan_reason": null, "plan_message": "", "exec": "executes:serve", "exec_reason": "provenance", "exec_message": "'mean of revenue@{customer*day}' reduced to customer \u2014 pin fixes customer, reduces over day"}
{"id": "P-04b", "label": "composite input anchor with `*` product spelling", "query": "SELECT avg( revenue @ {customer*day} ) AS typical_day AT {customer}", "grammar": "recognized", "parse": "series=['avg( revenue @ {customer*day} )' AS typical_day] anchor=('customer',)", "manifold": "finance_manifold", "plan": "serve", "plan_reason": null, "plan_message": "", "exec": "executes:serve", "exec_reason": "provenance", "exec_message": "'mean of revenue@{customer*day}' reduced to customer \u2014 pin fixes customer, reduces over day"}
{"id": "P-05", "label": "`@ {}` empty input anchor alone", "query": "SELECT (revenue @ {}) AS grand AT {}", "grammar": "recognized", "parse": "series=['(revenue @ {})' AS grand] anchor=()", "manifold": "finance_manifold", "plan": "serve", "plan_reason": null, "plan_message": "", "exec": "executes:error", "exec_reason": "unsupported", "exec_message": "this frame could not be resolved in the engine (AttributeError); the ask is not supported in this build."}
{"id": "P-05b", "label": "`AT {}` empty OUTPUT anchor with sugared series", "query": "SELECT revenue AT {}", "grammar": "recognized", "parse": "series=['revenue'] anchor=()", "manifold": "finance_manifold", "plan": "serve", "plan_reason": null, "plan_message": "", "exec": "executes:serve", "exec_reason": null, "exec_message": ""}
{"id": "P-06", "label": "WHERE on base dimension, single-quoted literal", "query": "FROM finance_manifold SELECT revenue AT {customer} WHERE day >= '2024-01-01'", "grammar": "recognized", "parse": "FROM=finance_manifold series=['revenue'] anchor=('customer',) where=[\"day >= '2024-01-01'\"]", "manifold": "finance_manifold", "plan": "serve", "plan_reason": null, "plan_message": "", "exec": "executes:serve", "exec_reason": null, "exec_message": ""}
{"id": "P-07", "label": "WHERE on a relationship-derived dimension, alone", "query": "FROM finance_manifold SELECT revenue AT {customer} WHERE region = \"east\"", "grammar": "recognized", "parse": "FROM=finance_manifold series=['revenue'] anchor=('customer',) where=['region = \"east\"']", "manifold": "finance_manifold", "plan": "error", "plan_reason": "filter_unsupported", "plan_message": "WHERE dimension 'region' is addressable in universe 'sales' but is not one of its base dimensions (customer, day, transaction), and this build pushes the filter to the measure's own source, which carries the base coordinates only. The ask is lawful; the build cannot execute it.", "exec": "executes:error", "exec_reason": "filter_unsupported", "exec_message": "WHERE dimension 'region' is addressable in universe 'sales' but is not one of its base dimensions (customer, day, transaction), and this build pushes the filter to the measure's own source, which carries the base coordinates only. The ask is lawful; the build cannot execute it."}
{"id": "P-08", "label": "IN (...) on a BASE dimension", "query": "FROM finance_manifold SELECT revenue AT {customer} WHERE day IN (\"2024-01-05\", \"2024-01-19\")", "grammar": "recognized", "parse": "FROM=finance_manifold series=['revenue'] anchor=('customer',) where=['day IN (\"2024-01-05\", \"2024-01-19\")']", "manifold": "finance_manifold", "plan": "serve", "plan_reason": null, "plan_message": "", "exec": "executes:serve", "exec_reason": null, "exec_message": ""}
{"id": "P-08b", "label": "IN (...) on a JOINED dimension", "query": "FROM finance_manifold SELECT revenue AT {customer} WHERE region IN (\"east\", \"west\")", "grammar": "recognized", "parse": "FROM=finance_manifold series=['revenue'] anchor=('customer',) where=['region IN (\"east\", \"west\")']", "manifold": "finance_manifold", "plan": "error", "plan_reason": "filter_unsupported", "plan_message": "WHERE dimension 'region' is addressable in universe 'sales' but is not one of its base dimensions (customer, day, transaction), and this build pushes the filter to the measure's own source, which carries the base coordinates only. The ask is lawful; the build cannot execute it.", "exec": "executes:error", "exec_reason": "filter_unsupported", "exec_message": "WHERE dimension 'region' is addressable in universe 'sales' but is not one of its base dimensions (customer, day, transaction), and this build pushes the filter to the measure's own source, which carries the base coordinates only. The ask is lawful; the build cannot execute it."}
{"id": "P-08c", "label": "WHERE on a dimension not in the manifold at all", "query": "FROM finance_manifold SELECT revenue AT {customer} WHERE warehouse = \"W1\"", "grammar": "recognized", "parse": "FROM=finance_manifold series=['revenue'] anchor=('customer',) where=['warehouse = \"W1\"']", "manifold": "finance_manifold", "plan": "clarify", "plan_reason": "filter_unreachable", "plan_message": "WHERE dimension 'warehouse' cannot lawfully reach series 'revenue' \u2014 'warehouse' is not addressable in that series' universe 'sales', so the pre-reduction filter has no grain to bind to; the answer would be silently partial.", "exec": "executes:clarify", "exec_reason": "filter_unreachable", "exec_message": "WHERE dimension 'warehouse' cannot lawfully reach series 'revenue' \u2014 'warehouse' is not addressable in that series' universe 'sales', so the pre-reduction filter has no grain to bind to; the answer would be silently partial."}
{"id": "P-09", "label": "HAVING alone, threshold that keeps rows", "query": "FROM finance_manifold SELECT revenue AS total_revenue AT {customer} HAVING total_revenue > 100", "grammar": "recognized", "parse": "FROM=finance_manifold series=['revenue' AS total_revenue] anchor=('customer',) having=['total_revenue > 100']", "manifold": "finance_manifold", "plan": "serve", "plan_reason": null, "plan_message": "", "exec": "executes:serve", "exec_reason": null, "exec_message": ""}
{"id": "P-10", "label": "ORDER BY alone on an alias", "query": "FROM finance_manifold SELECT revenue AS total_revenue AT {customer} ORDER BY total_revenue DESC", "grammar": "recognized", "parse": "FROM=finance_manifold series=['revenue' AS total_revenue] anchor=('customer',) order_by=[OrderKey(column='total_revenue', descending=True)]", "manifold": "finance_manifold", "plan": "serve", "plan_reason": null, "plan_message": "", "exec": "executes:serve", "exec_reason": null, "exec_message": ""}
{"id": "P-10b", "label": "ORDER BY an anchor coordinate", "query": "FROM finance_manifold SELECT revenue AS total_revenue AT {customer} ORDER BY customer ASC", "grammar": "recognized", "parse": "FROM=finance_manifold series=['revenue' AS total_revenue] anchor=('customer',) order_by=[OrderKey(column='customer', descending=False)]", "manifold": "finance_manifold", "plan": "serve", "plan_reason": null, "plan_message": "", "exec": "executes:serve", "exec_reason": null, "exec_message": ""}
{"id": "P-11", "label": "flat LIMIT n", "query": "FROM finance_manifold SELECT revenue AS total_revenue AT {customer} ORDER BY total_revenue DESC LIMIT 2", "grammar": "recognized", "parse": "FROM=finance_manifold series=['revenue' AS total_revenue] anchor=('customer',) order_by=[OrderKey(column='total_revenue', descending=True)] limit=Limit(n=2, per=())", "manifold": "finance_manifold", "plan": "serve", "plan_reason": null, "plan_message": "", "exec": "executes:serve", "exec_reason": null, "exec_message": ""}
{"id": "P-11b", "label": "LIMIT n PER {} (documented degenerate empty PER)", "query": "FROM finance_manifold SELECT revenue AS total_revenue AT {customer} ORDER BY total_revenue DESC LIMIT 2 PER {}", "grammar": "recognized", "parse": "FROM=finance_manifold series=['revenue' AS total_revenue] anchor=('customer',) order_by=[OrderKey(column='total_revenue', descending=True)] limit=Limit(n=2, per=())", "manifold": "finance_manifold", "plan": "serve", "plan_reason": null, "plan_message": "", "exec": "executes:serve", "exec_reason": null, "exec_message": ""}
{"id": "P-11c", "label": "LIMIT n PER {dim} where PER key is NOT an ORDER BY key (documented refusal)", "query": "FROM product_manifold SELECT product_revenue AT {category, product} ORDER BY product_revenue DESC LIMIT 5 PER {category}", "grammar": "recognized", "parse": "FROM=product_manifold series=['product_revenue'] anchor=('category', 'product') order_by=[OrderKey(column='product_revenue', descending=True)] limit=Limit(n=5, per=('category',))", "manifold": "product_manifold", "plan": "raises", "plan_reason": "FrameQLSyntaxError", "plan_message": "PER {category} is not in ORDER BY \u2014 PER groups and ORDER BY ranks within each group, so the partition key must also sort; add 'category' to ORDER BY (e.g. ORDER BY category, \u2026)", "exec": "not-exercised", "exec_reason": null, "exec_message": null}
{"id": "P-11d", "label": "LIMIT n PER {alias} \u2014 PER key is a series alias, not a coordinate (documented refusal)", "query": "FROM product_manifold SELECT product_revenue AS pr AT {category, product} ORDER BY category, pr DESC LIMIT 5 PER {pr}", "grammar": "recognized", "parse": "FROM=product_manifold series=['product_revenue' AS pr] anchor=('category', 'product') order_by=[OrderKey(column='category', descending=False), OrderKey(column='pr', descending=True)] limit=Limit(n=5, per=('pr',))", "manifold": "product_manifold", "plan": "raises", "plan_reason": "FrameQLSyntaxError", "plan_message": "PER {pr} names 'pr', an output column \u2014 PER takes ANCHOR coordinates only; put 'pr' in the anchor to partition by it", "exec": "not-exercised", "exec_reason": null, "exec_message": null}
{"id": "P-12", "label": "macro binding referenced in SELECT and HAVING", "query": "FROM finance_manifold WITH profit = (revenue - cost) SELECT profit AT {customer} HAVING profit > 0", "grammar": "recognized", "parse": "FROM=finance_manifold series=['profit'] anchor=('customer',) bindings=[Binding(name='profit', expr='(revenue - cost)')] having=['profit > 0']", "manifold": "finance_manifold", "plan": "serve", "plan_reason": null, "plan_message": "", "exec": "executes:serve", "exec_reason": null, "exec_message": ""}
{"id": "P-12b", "label": "macro binding used in WHERE", "query": "FROM finance_manifold WITH d = day SELECT revenue AT {customer} WHERE d >= \"2024-01-01\"", "grammar": "recognized", "parse": "FROM=finance_manifold series=['revenue'] anchor=('customer',) bindings=[Binding(name='d', expr='day')] where=['d >= \"2024-01-01\"']", "manifold": "finance_manifold", "plan": "clarify", "plan_reason": "filter_unreachable", "plan_message": "WHERE dimension 'd' cannot lawfully reach series 'revenue' \u2014 'd' is not addressable in that series' universe 'sales', so the pre-reduction filter has no grain to bind to; the answer would be silently partial.", "exec": "executes:clarify", "exec_reason": "filter_unreachable", "exec_message": "WHERE dimension 'd' cannot lawfully reach series 'revenue' \u2014 'd' is not addressable in that series' universe 'sales', so the pre-reduction filter has no grain to bind to; the answer would be silently partial."}
{"id": "P-13", "label": "scan: cumsum, order-only, executed", "query": "FROM finance_manifold SELECT cumsum( revenue @ {customer, day} ) AS rtd AT {customer, day}", "grammar": "recognized", "parse": "FROM=finance_manifold series=['cumsum( revenue @ {customer, day} )' AS rtd] anchor=('customer', 'day')", "manifold": "finance_manifold", "plan": "serve", "plan_reason": null, "plan_message": "", "exec": "executes:serve", "exec_reason": "provenance", "exec_message": "scan cumsum over order 'day' within ['customer']"}
{"id": "P-13b", "label": "scan: lag with n=", "query": "FROM finance_manifold SELECT lag( revenue @ {customer, day}, n = 1 ) AS prev AT {customer, day}", "grammar": "recognized", "parse": "FROM=finance_manifold series=['lag( revenue @ {customer, day}, n = 1 )' AS prev] anchor=('customer', 'day')", "manifold": "finance_manifold", "plan": "serve", "plan_reason": null, "plan_message": "", "exec": "executes:disclose", "exec_reason": "provenance", "exec_message": "scan lag over order 'day' within ['customer']"}
{"id": "P-13c", "label": "scan: rolling_mean (registry in_core=False)", "query": "FROM finance_manifold SELECT rolling_mean( revenue @ {customer, day}, window = 2 ) AS rm AT {customer, day}", "grammar": "recognized", "parse": "FROM=finance_manifold series=['rolling_mean( revenue @ {customer, day}, window = 2 )' AS rm] anchor=('customer', 'day')", "manifold": "finance_manifold", "plan": "error", "plan_reason": "unknown", "plan_message": "scan 'rolling_mean': unknown parameter 'window' (accepts n=, by=)", "exec": "executes:error", "exec_reason": "unknown", "exec_message": "scan 'rolling_mean': unknown parameter 'window' (accepts n=, by=)"}
{"id": "P-13d", "label": "scan: rank (in Manual Appendix A, NOT in registry)", "query": "FROM finance_manifold SELECT rank( revenue @ {customer, day} ) AS r AT {customer, day}", "grammar": "recognized", "parse": "FROM=finance_manifold series=['rank( revenue @ {customer, day} )' AS r] anchor=('customer', 'day')", "manifold": "finance_manifold", "plan": "error", "plan_reason": "unknown", "plan_message": "'rank' is not a scan operator (registry scans: ['cummax', 'cummin', 'cumsum', 'lag', 'lead', 'pct_change', 'rolling_mean', 'rolling_sum'])", "exec": "executes:error", "exec_reason": "unknown", "exec_message": "'rank' is not a scan operator (registry scans: ['cummax', 'cummin', 'cumsum', 'lag', 'lead', 'pct_change', 'rolling_mean', 'rolling_sum'])"}
{"id": "P-14", "label": "bracket filter, minimal", "query": "SELECT revenue[region = \"east\"] AS east AT {customer}", "grammar": "recognized", "parse": "series=['revenue[region = \"east\"]' AS east] anchor=('customer',)", "manifold": "finance_manifold", "plan": "raises", "plan_reason": "SyntaxError", "plan_message": "invalid syntax. Maybe you meant '==' or ':=' instead of '='? (<unknown>, line 1)", "exec": "not-exercised", "exec_reason": null, "exec_message": null}
{"id": "P-15", "label": "multi-input reducer, concrete (two operands in one reducer)", "query": "SELECT sum(revenue @ {transaction}, cost @ {transaction}) AS both AT {customer}", "grammar": "recognized", "parse": "series=['sum(revenue @ {transaction}, cost @ {transaction})' AS both] anchor=('customer',)", "manifold": "finance_manifold", "plan": "error", "plan_reason": "unknown", "plan_message": "inline reduction 'sum' takes exactly one column argument (e.g. sum(aov@day) to pin the input anchor)", "exec": "executes:error", "exec_reason": "unknown", "exec_message": "inline reduction 'sum' takes exactly one column argument (e.g. sum(aov@day) to pin the input anchor)"}
{"id": "P-16", "label": "query-level count(*) as the only series", "query": "FROM finance_manifold SELECT count(*) AS n AT {customer}", "grammar": "recognized", "parse": "FROM=finance_manifold series=['count(*)' AS n] anchor=('customer',)", "manifold": "finance_manifold", "plan": "raises", "plan_reason": "SyntaxError", "plan_message": "Invalid star expression (<unknown>, line 1)", "exec": "not-exercised", "exec_reason": null, "exec_message": null}
{"id": "P-16b", "label": "query-level count(*) unaliased", "query": "FROM finance_manifold SELECT count(*) AT {customer}", "grammar": "recognized", "parse": "FROM=finance_manifold series=['count(*)'] anchor=('customer',)", "manifold": "finance_manifold", "plan": "raises", "plan_reason": "FrameQLSyntaxError", "plan_message": "cannot name series 'count(*)' \u2014 give it a name with AS", "exec": "not-exercised", "exec_reason": null, "exec_message": null}
{"id": "P-17", "label": "declared distinct/HLL measure (unique_visitors = distinct(customer_id))", "query": "FROM retail_manifold SELECT unique_visitors AT {store}", "grammar": "recognized", "parse": "FROM=retail_manifold series=['unique_visitors'] anchor=('store',)", "manifold": "retail_manifold", "plan": "disclose", "plan_reason": "approximation", "plan_message": "unique_visitors.distinct: HLL distinct estimate [HLLSketch(12)]", "exec": "executes:disclose", "exec_reason": "approximation", "exec_message": "unique_visitors.distinct: HLL distinct estimate [HLLSketch(12)]"}
{"id": "P-17b", "label": "inline approx_distinct (Manual Appendix A reducer name)", "query": "FROM retail_manifold SELECT approx_distinct( revenue @ {transaction} ) AS ad AT {store}", "grammar": "recognized", "parse": "FROM=retail_manifold series=['approx_distinct( revenue @ {transaction} )' AS ad] anchor=('store',)", "manifold": "retail_manifold", "plan": "error", "plan_reason": "unknown", "plan_message": "'approx_distinct' is not a scan operator (registry scans: ['cummax', 'cummin', 'cumsum', 'lag', 'lead', 'pct_change', 'rolling_mean', 'rolling_sum'])", "exec": "executes:error", "exec_reason": "unknown", "exec_message": "'approx_distinct' is not a scan operator (registry scans: ['cummax', 'cummin', 'cumsum', 'lag', 'lead', 'pct_change', 'rolling_mean', 'rolling_sum'])"}
{"id": "P-17c", "label": "inline distinct reducer by its registry name", "query": "FROM retail_manifold SELECT distinct( revenue @ {transaction} ) AS d AT {store}", "grammar": "recognized", "parse": "FROM=retail_manifold series=['distinct( revenue @ {transaction} )' AS d] anchor=('store',)", "manifold": "retail_manifold", "plan": "error", "plan_reason": "unknown", "plan_message": "'distinct' is not a scan operator (registry scans: ['cummax', 'cummin', 'cumsum', 'lag', 'lead', 'pct_change', 'rolling_mean', 'rolling_sum'])", "exec": "executes:error", "exec_reason": "unknown", "exec_message": "'distinct' is not a scan operator (registry scans: ['cummax', 'cummin', 'cumsum', 'lag', 'lead', 'pct_change', 'rolling_mean', 'rolling_sum'])"}
{"id": "P-18", "label": "generated reducer: sum over a stock declared FAMILY {last,max,min,count} (DG-4 under-declared case)", "query": "SELECT sum(level @ {store, day}) AS s AT {region}", "grammar": "recognized", "parse": "series=['sum(level @ {store, day})' AS s] anchor=('region',)", "manifold": "finance_manifold", "plan": "error", "plan_reason": "unknown", "plan_message": "'level' has a family ['last', 'max', 'min', 'count'] \u2014 specify a member", "exec": "executes:error", "exec_reason": "unknown", "exec_message": "'level' has a family ['last', 'max', 'min', 'count'] \u2014 specify a member"}
{"id": "P-18b", "label": "generated reducer: max over a measure whose family is {sum} only", "query": "SELECT max(revenue @ {transaction}) AS m AT {customer}", "grammar": "recognized", "parse": "series=['max(revenue @ {transaction})' AS m] anchor=('customer',)", "manifold": "finance_manifold", "plan": "serve", "plan_reason": null, "plan_message": "", "exec": "executes:serve", "exec_reason": "provenance", "exec_message": "'max of revenue@transaction' reduced to customer \u2014 the max of revenue@transaction reading (input anchor pinned to 'transaction'), not the pooled value at customer"}
{"id": "P-18c", "label": "generated reducer: median (HOLISTIC witness) inline", "query": "SELECT median(revenue @ {transaction}) AS md AT {customer}", "grammar": "recognized", "parse": "series=['median(revenue @ {transaction})' AS md] anchor=('customer',)", "manifold": "finance_manifold", "plan": "error", "plan_reason": "unknown", "plan_message": "'median' is not a scan operator (registry scans: ['cummax', 'cummin', 'cumsum', 'lag', 'lead', 'pct_change', 'rolling_mean', 'rolling_sum'])", "exec": "executes:error", "exec_reason": "unknown", "exec_message": "'median' is not a scan operator (registry scans: ['cummax', 'cummin', 'cumsum', 'lag', 'lead', 'pct_change', 'rolling_mean', 'rolling_sum'])"}
{"id": "P-18d", "label": "generated reducer: declared family member by dotted spelling (level.last)", "query": "SELECT level.last AS inv AT {region}", "grammar": "recognized", "parse": "series=['level.last' AS inv] anchor=('region',)", "manifold": "finance_manifold", "plan": "serve", "plan_reason": null, "plan_message": "", "exec": "executes:serve", "exec_reason": null, "exec_message": ""}
{"id": "P-19", "label": "anchor product with `*` in AT", "query": "FROM retail SELECT revenue AT { region * store }", "grammar": "recognized", "parse": "FROM=retail series=['revenue'] anchor=('region', 'store')", "manifold": "retail_manifold", "plan": "serve", "plan_reason": null, "plan_message": "", "exec": "executes:error", "exec_reason": "unsupported", "exec_message": "this frame could not be resolved in the engine (ColumnNotFoundError); the ask is not supported in this build."}
{"id": "P-20", "label": "no AT clause at all (Ch3.3: output anchor never inferred)", "query": "SELECT revenue", "grammar": "not-recognized", "parse": "EnvelopeSyntaxError: a query must declare its output grain with AT { \u2026 } \u2014 name the levels the frame stands at, e.g. SELECT revenue AT {region} (AT {} is the grand total)", "manifold": null, "plan": "not-exercised", "plan_reason": null, "plan_message": null, "exec": "not-exercised", "exec_reason": null, "exec_message": null}
{"id": "X-01", "label": "operator alias with AS supplied (isolates naming from unknown-operator)", "query": "FROM retail_manifold SELECT total(revenue) AS t, unique_visitors AT {store}", "grammar": "recognized", "parse": "FROM=retail_manifold series=['total(revenue)' AS t; 'unique_visitors'] anchor=('store',)", "manifold": "retail_manifold", "plan": "error", "plan_reason": "unknown", "plan_message": "'total' is not a scan operator (registry scans: ['cummax', 'cummin', 'cumsum', 'lag', 'lead', 'pct_change', 'rolling_mean', 'rolling_sum'])", "exec": "executes:error", "exec_reason": "unknown", "exec_message": "'total' is not a scan operator (registry scans: ['cummax', 'cummin', 'cumsum', 'lag', 'lead', 'pct_change', 'rolling_mean', 'rolling_sum'])"}
{"id": "X-02", "label": "generated reducer sum over a declared family MEMBER (level.last)", "query": "SELECT sum(level.last @ {store, day}) AS s AT {region}", "grammar": "recognized", "parse": "series=['sum(level.last @ {store, day})' AS s] anchor=('region',)", "manifold": "finance_manifold", "plan": "serve", "plan_reason": null, "plan_message": "", "exec": "executes:serve", "exec_reason": "provenance", "exec_message": "'sum of level.last@{store*day}' reduced to region \u2014 the sum of level.last@{store*day} reading (input anchor pinned to '{store*day}'), not the pooled value at region"}
{"id": "X-03", "label": "generated reducer max over a declared family MEMBER (level.last)", "query": "SELECT max(level.last @ {store, day}) AS m AT {region}", "grammar": "recognized", "parse": "series=['max(level.last @ {store, day})' AS m] anchor=('region',)", "manifold": "finance_manifold", "plan": "serve", "plan_reason": null, "plan_message": "", "exec": "executes:serve", "exec_reason": "provenance", "exec_message": "'max of level.last@{store*day}' reduced to region \u2014 the max of level.last@{store*day} reading (input anchor pinned to '{store*day}'), not the pooled value at region"}
{"id": "X-04", "label": "declared family member that does not exist (level.sum)", "query": "SELECT level.sum AS s AT {region}", "grammar": "recognized", "parse": "series=['level.sum' AS s] anchor=('region',)", "manifold": "finance_manifold", "plan": "error", "plan_reason": "unknown", "plan_message": "'level' has no family member 'sum' (have ['last', 'max', 'min', 'count'])", "exec": "executes:error", "exec_reason": "unknown", "exec_message": "'level' has no family member 'sum' (have ['last', 'max', 'min', 'count'])"}
{"id": "X-05", "label": "median unpinned", "query": "SELECT median(revenue) AS md AT {customer}", "grammar": "recognized", "parse": "series=['median(revenue)' AS md] anchor=('customer',)", "manifold": "finance_manifold", "plan": "error", "plan_reason": "unknown", "plan_message": "'median' is not a scan operator (registry scans: ['cummax', 'cummin', 'cumsum', 'lag', 'lead', 'pct_change', 'rolling_mean', 'rolling_sum'])", "exec": "executes:error", "exec_reason": "unknown", "exec_message": "'median' is not a scan operator (registry scans: ['cummax', 'cummin', 'cumsum', 'lag', 'lead', 'pct_change', 'rolling_mean', 'rolling_sum'])"}
{"id": "X-06", "label": "generated reducer sum of a stock across STORES (DG-4 lawful case)", "query": "SELECT sum(level.last @ {store, day}) AS s AT {store}", "grammar": "recognized", "parse": "series=['sum(level.last @ {store, day})' AS s] anchor=('store',)", "manifold": "finance_manifold", "plan": "serve", "plan_reason": null, "plan_message": "", "exec": "executes:serve", "exec_reason": "provenance", "exec_message": "'sum of level.last@{store*day}' reduced to store \u2014 pin fixes store, reduces over day"}
{"id": "X-07", "label": "inline count reducer (SERIES_REDUCERS member)", "query": "SELECT count(revenue @ {transaction}) AS n AT {customer}", "grammar": "recognized", "parse": "series=['count(revenue @ {transaction})' AS n] anchor=('customer',)", "manifold": "finance_manifold", "plan": "serve", "plan_reason": null, "plan_message": "", "exec": "executes:serve", "exec_reason": "provenance", "exec_message": "'count of revenue@transaction' reduced to customer \u2014 the count of revenue@transaction reading (input anchor pinned to 'transaction'), not the pooled value at customer"}
{"id": "X-08", "label": "inline mean reducer (SERIES_REDUCERS member)", "query": "SELECT mean(revenue @ {transaction}) AS n AT {customer}", "grammar": "recognized", "parse": "series=['mean(revenue @ {transaction})' AS n] anchor=('customer',)", "manifold": "finance_manifold", "plan": "serve", "plan_reason": null, "plan_message": "", "exec": "executes:serve", "exec_reason": "provenance", "exec_message": "'mean of revenue@transaction' reduced to customer \u2014 the mean of revenue@transaction reading (input anchor pinned to 'transaction'), not the pooled value at customer"}
{"id": "X-09", "label": "scan with no derivable order axis", "query": "SELECT cumsum( revenue @ {customer} ) AS c AT {customer}", "grammar": "recognized", "parse": "series=['cumsum( revenue @ {customer} )' AS c] anchor=('customer',)", "manifold": "finance_manifold", "plan": "serve", "plan_reason": null, "plan_message": "", "exec": "executes:error", "exec_reason": "unknown", "exec_message": "scan 'cumsum' @ ('customer',) has no derivable order axis (no CERTIFIED temporal level in the anchor); name it with by=<level>. A declared-but-uncertified hierarchy confers no order axis \u2014 declaration makes structure eligible for certification, not executable."}
{"id": "X-10", "label": "unknown column", "query": "SELECT nosuchmeasure AT {customer}", "grammar": "recognized", "parse": "series=['nosuchmeasure'] anchor=('customer',)", "manifold": "finance_manifold", "plan": "error", "plan_reason": "unknown", "plan_message": "unknown column 'nosuchmeasure'", "exec": "executes:error", "exec_reason": "unknown", "exec_message": "unknown column 'nosuchmeasure'"}
{"id": "X-11", "label": "unregistered operator name", "query": "SELECT frobnicate(revenue @ {transaction}) AS f AT {customer}", "grammar": "recognized", "parse": "series=['frobnicate(revenue @ {transaction})' AS f] anchor=('customer',)", "manifold": "finance_manifold", "plan": "error", "plan_reason": "unknown", "plan_message": "'frobnicate' is not a scan operator (registry scans: ['cummax', 'cummin', 'cumsum', 'lag', 'lead', 'pct_change', 'rolling_mean', 'rolling_sum'])", "exec": "executes:error", "exec_reason": "unknown", "exec_message": "'frobnicate' is not a scan operator (registry scans: ['cummax', 'cummin', 'cumsum', 'lag', 'lead', 'pct_change', 'rolling_mean', 'rolling_sum'])"}
```

### A.2 — verbatim output of `/tmp/probe_detail.py` (full `no_result` / `disclosures` payloads and returned frames)

```
====================================================================================================
[M-L276] SELECT op( col_1 @ {a_1}, col_2 @ {a_2}, ... ) AS name AT { A }
  PLAN outcome: error
   col name | no_result: {"kind": "error", "discriminator": null, "reason": "unknown", "detail": "'op' is not a scan operator (registry scans: ['cummax', 'cummin', 'cumsum', 'lag', 'lead', 'pct_change', 'rolling_mean', 'rolling_sum'])", "alternatives": []} | disclosures: []
   frame disclosures: []
  EXEC outcome: error
   col name | no_result: {"kind": "error", "discriminator": null, "reason": "unknown", "detail": "'op' is not a scan operator (registry scans: ['cummax', 'cummin', 'cumsum', 'lag', 'lead', 'pct_change', 'rolling_mean', 'rolling_sum'])", "alternatives": []} | disclosures: []
   DATA: None
====================================================================================================
[M-L560] FROM finance_manifold SELECT sum(revenue @ {transaction}) AT {customer} WHERE region = "east" AND date >= "2024-01-01"
  PLAN outcome: error
   col sum(revenue @ {transaction}) | no_result: {"kind": "error", "discriminator": null, "reason": "filter_unsupported", "detail": "WHERE dimension 'region' is addressable in universe 'sales' but is not one of its base dimensions (customer, day, transaction), and this build pushes the filter to the measure's own source, which carries the base coordinates only. The ask is lawful; the build cannot execute it.", "alternatives": [{"token": "filter on a base dimension (customer, day, transaction)", "description": "filter on a base dimension (customer, day, transaction)"}]} | disclosures: []
   frame disclosures: []
  EXEC outcome: error
   col sum(revenue @ {transaction}) | no_result: {"kind": "error", "discriminator": null, "reason": "filter_unsupported", "detail": "WHERE dimension 'region' is addressable in universe 'sales' but is not one of its base dimensions (customer, day, transaction), and this build pushes the filter to the measure's own source, which carries the base coordinates only. The ask is lawful; the build cannot execute it.", "alternatives": [{"token": "filter on a base dimension (customer, day, transaction)", "description": "filter on a base dimension (customer, day, transaction)"}]} | disclosures: []
   DATA: None
====================================================================================================
[M-L903] FROM finance_manifold SELECT revenue AT {customer} WHERE date >= "2024-01-01" AND region IN ("east", "west")
  PLAN outcome: error
   col revenue | no_result: {"kind": "error", "discriminator": null, "reason": "filter_unsupported", "detail": "WHERE dimension 'date' is addressable in universe 'sales' but is not one of its base dimensions (customer, day, transaction), and this build pushes the filter to the measure's own source, which carries the base coordinates only. The ask is lawful; the build cannot execute it.", "alternatives": [{"token": "filter on a base dimension (customer, day, transaction)", "description": "filter on a base dimension (customer, day, transaction)"}]} | disclosures: []
   frame disclosures: []
  EXEC outcome: error
   col revenue | no_result: {"kind": "error", "discriminator": null, "reason": "filter_unsupported", "detail": "WHERE dimension 'date' is addressable in universe 'sales' but is not one of its base dimensions (customer, day, transaction), and this build pushes the filter to the measure's own source, which carries the base coordinates only. The ask is lawful; the build cannot execute it.", "alternatives": [{"token": "filter on a base dimension (customer, day, transaction)", "description": "filter on a base dimension (customer, day, transaction)"}]} | disclosures: []
   DATA: None
====================================================================================================
[P-08c] FROM finance_manifold SELECT revenue AT {customer} WHERE warehouse = "W1"
  PLAN outcome: clarify
   col revenue | no_result: {"kind": "clarify", "discriminator": "ambiguous", "reason": "filter_unreachable", "detail": "WHERE dimension 'warehouse' cannot lawfully reach series 'revenue' \u2014 'warehouse' is not addressable in that series' universe 'sales', so the pre-reduction filter has no grain to bind to; the answer would be silently partial.", "alternatives": [{"token": "restrict the predicate to a reachable dimension (customer, date, day, month, product, region, transaction, year)", "description": "restrict the predicate to a reachable dimension (customer, date, day, month, product, region, transaction, year)"}, {"token": "change series 'revenue' to an input anchor that reaches 'warehouse'", "description": "change series 'revenue' to an input anchor that reaches 'warehouse'"}]} | disclosures: []
   frame disclosures: []
  EXEC outcome: clarify
   col revenue | no_result: {"kind": "clarify", "discriminator": "ambiguous", "reason": "filter_unreachable", "detail": "WHERE dimension 'warehouse' cannot lawfully reach series 'revenue' \u2014 'warehouse' is not addressable in that series' universe 'sales', so the pre-reduction filter has no grain to bind to; the answer would be silently partial.", "alternatives": [{"token": "restrict the predicate to a reachable dimension (customer, date, day, month, product, region, transaction, year)", "description": "restrict the predicate to a reachable dimension (customer, date, day, month, product, region, transaction, year)"}, {"token": "change series 'revenue' to an input anchor that reaches 'warehouse'", "description": "change series 'revenue' to an input anchor that reaches 'warehouse'"}]} | disclosures: []
   DATA: None
====================================================================================================
[P-12b] FROM finance_manifold WITH d = day SELECT revenue AT {customer} WHERE d >= "2024-01-01"
  PLAN outcome: clarify
   col revenue | no_result: {"kind": "clarify", "discriminator": "ambiguous", "reason": "filter_unreachable", "detail": "WHERE dimension 'd' cannot lawfully reach series 'revenue' \u2014 'd' is not addressable in that series' universe 'sales', so the pre-reduction filter has no grain to bind to; the answer would be silently partial.", "alternatives": [{"token": "restrict the predicate to a reachable dimension (customer, date, day, month, product, region, transaction, year)", "description": "restrict the predicate to a reachable dimension (customer, date, day, month, product, region, transaction, year)"}, {"token": "change series 'revenue' to an input anchor that reaches 'd'", "description": "change series 'revenue' to an input anchor that reaches 'd'"}]} | disclosures: []
   frame disclosures: []
  EXEC outcome: clarify
   col revenue | no_result: {"kind": "clarify", "discriminator": "ambiguous", "reason": "filter_unreachable", "detail": "WHERE dimension 'd' cannot lawfully reach series 'revenue' \u2014 'd' is not addressable in that series' universe 'sales', so the pre-reduction filter has no grain to bind to; the answer would be silently partial.", "alternatives": [{"token": "restrict the predicate to a reachable dimension (customer, date, day, month, product, region, transaction, year)", "description": "restrict the predicate to a reachable dimension (customer, date, day, month, product, region, transaction, year)"}, {"token": "change series 'revenue' to an input anchor that reaches 'd'", "description": "change series 'revenue' to an input anchor that reaches 'd'"}]} | disclosures: []
   DATA: None
====================================================================================================
[M-L970] FROM finance_manifold SELECT cumsum( revenue @ {customer, day}, reset = year ) AS revenue_ytd AT {customer, day}
  PLAN outcome: error
   col revenue_ytd | no_result: {"kind": "error", "discriminator": null, "reason": "unknown", "detail": "scan 'cumsum': unknown parameter 'reset' (accepts n=, by=)", "alternatives": []} | disclosures: []
   frame disclosures: []
  EXEC outcome: error
   col revenue_ytd | no_result: {"kind": "error", "discriminator": null, "reason": "unknown", "detail": "scan 'cumsum': unknown parameter 'reset' (accepts n=, by=)", "alternatives": []} | disclosures: []
   DATA: None
====================================================================================================
[M-L978] FROM finance_manifold SELECT ( revenue - lag(revenue, 1, step = year) ) / lag(revenue, 1, step = year) AS yoy_growth AT {customer, month}
  PLAN outcome: error
   col yoy_growth | no_result: {"kind": "error", "discriminator": null, "reason": "unknown", "detail": "scan 'lag' takes one input expression and keyword params (n=, by=)", "alternatives": []} | disclosures: []
   frame disclosures: []
  EXEC outcome: error
   col yoy_growth | no_result: {"kind": "error", "discriminator": null, "reason": "unknown", "detail": "scan 'lag' takes one input expression and keyword params (n=, by=)", "alternatives": []} | disclosures: []
   DATA: None
====================================================================================================
[M-L1008] FROM retail WITH line = revenue @ {transaction} SELECT sum(line) AS gross, avg(aov @ {day}) AS typical AT { region * store } ORDER BY region, gross DESC LIMIT 3 PER { region }
  PLAN outcome: serve
   col gross | no_result: null | disclosures: []
   col typical | no_result: null | disclosures: []
   frame disclosures: []
  EXEC outcome: error
   col gross | no_result: null | disclosures: [{"code": "provenance", "materiality": "immaterial", "severity": "info", "category": "transport", "detail": "'sum of revenue@transaction' reduced to region*store \u2014 the sum of revenue@transaction reading (input anchor pinned to 'transaction'), not the pooled value at region*store", "remedy": null, "source": "transaction->region*store", "rel_error": null}]
   col typical | no_result: {"kind": "error", "discriminator": null, "reason": "unsupported", "detail": "this frame could not be resolved in the engine (ColumnNotFoundError); the ask is not supported in this build.", "alternatives": []} | disclosures: []
   DATA: shape: (2, 3)
┌────────┬───────┬───────┐
│ region ┆ store ┆ gross │
│ ---    ┆ ---   ┆ ---   │
│ str    ┆ str   ┆ f64   │
╞════════╪═══════╪═══════╡
│ east   ┆ S1    ┆ 200.0 │
│ west   ┆ S2    ┆ 200.0 │
└────────┴───────┴───────┘
====================================================================================================
[M-L1027] FROM retail SELECT avg( revenue @ {store*product*cal.month} ) AS avg_monthly_product_revenue AT {store}
  PLAN outcome: serve
   col avg_monthly_product_revenue | no_result: null | disclosures: []
   frame disclosures: []
  EXEC outcome: error
   col avg_monthly_product_revenue | no_result: {"kind": "error", "discriminator": null, "reason": "unsupported", "detail": "this frame could not be resolved in the engine (ColumnNotFoundError); the ask is not supported in this build.", "alternatives": []} | disclosures: []
   DATA: None
====================================================================================================
[P-19] FROM retail SELECT revenue AT { region * store }
  PLAN outcome: serve
   col revenue | no_result: null | disclosures: []
   frame disclosures: []
  EXEC outcome: error
   col revenue | no_result: {"kind": "error", "discriminator": null, "reason": "unsupported", "detail": "this frame could not be resolved in the engine (ColumnNotFoundError); the ask is not supported in this build.", "alternatives": []} | disclosures: []
   DATA: None
====================================================================================================
[P-05] SELECT (revenue @ {}) AS grand AT {}
  PLAN outcome: serve
   col grand | no_result: null | disclosures: []
   frame disclosures: []
  EXEC outcome: error
   col grand | no_result: {"kind": "error", "discriminator": null, "reason": "unsupported", "detail": "this frame could not be resolved in the engine (AttributeError); the ask is not supported in this build.", "alternatives": []} | disclosures: []
   DATA: None
====================================================================================================
[P-13c] FROM finance_manifold SELECT rolling_mean( revenue @ {customer, day}, window = 2 ) AS rm AT {customer, day}
  PLAN outcome: error
   col rm | no_result: {"kind": "error", "discriminator": null, "reason": "unknown", "detail": "scan 'rolling_mean': unknown parameter 'window' (accepts n=, by=)", "alternatives": []} | disclosures: []
   frame disclosures: []
  EXEC outcome: error
   col rm | no_result: {"kind": "error", "discriminator": null, "reason": "unknown", "detail": "scan 'rolling_mean': unknown parameter 'window' (accepts n=, by=)", "alternatives": []} | disclosures: []
   DATA: None
====================================================================================================
[P-13d] FROM finance_manifold SELECT rank( revenue @ {customer, day} ) AS r AT {customer, day}
  PLAN outcome: error
   col r | no_result: {"kind": "error", "discriminator": null, "reason": "unknown", "detail": "'rank' is not a scan operator (registry scans: ['cummax', 'cummin', 'cumsum', 'lag', 'lead', 'pct_change', 'rolling_mean', 'rolling_sum'])", "alternatives": []} | disclosures: []
   frame disclosures: []
  EXEC outcome: error
   col r | no_result: {"kind": "error", "discriminator": null, "reason": "unknown", "detail": "'rank' is not a scan operator (registry scans: ['cummax', 'cummin', 'cumsum', 'lag', 'lead', 'pct_change', 'rolling_mean', 'rolling_sum'])", "alternatives": []} | disclosures: []
   DATA: None
====================================================================================================
[P-15] SELECT sum(revenue @ {transaction}, cost @ {transaction}) AS both AT {customer}
  PLAN outcome: error
   col both | no_result: {"kind": "error", "discriminator": null, "reason": "unknown", "detail": "inline reduction 'sum' takes exactly one column argument (e.g. sum(aov@day) to pin the input anchor)", "alternatives": []} | disclosures: []
   frame disclosures: []
  EXEC outcome: error
   col both | no_result: {"kind": "error", "discriminator": null, "reason": "unknown", "detail": "inline reduction 'sum' takes exactly one column argument (e.g. sum(aov@day) to pin the input anchor)", "alternatives": []} | disclosures: []
   DATA: None
====================================================================================================
[P-17b] FROM retail_manifold SELECT approx_distinct( revenue @ {transaction} ) AS ad AT {store}
  PLAN outcome: error
   col ad | no_result: {"kind": "error", "discriminator": null, "reason": "unknown", "detail": "'approx_distinct' is not a scan operator (registry scans: ['cummax', 'cummin', 'cumsum', 'lag', 'lead', 'pct_change', 'rolling_mean', 'rolling_sum'])", "alternatives": []} | disclosures: []
   frame disclosures: []
  EXEC outcome: error
   col ad | no_result: {"kind": "error", "discriminator": null, "reason": "unknown", "detail": "'approx_distinct' is not a scan operator (registry scans: ['cummax', 'cummin', 'cumsum', 'lag', 'lead', 'pct_change', 'rolling_mean', 'rolling_sum'])", "alternatives": []} | disclosures: []
   DATA: None
====================================================================================================
[P-17c] FROM retail_manifold SELECT distinct( revenue @ {transaction} ) AS d AT {store}
  PLAN outcome: error
   col d | no_result: {"kind": "error", "discriminator": null, "reason": "unknown", "detail": "'distinct' is not a scan operator (registry scans: ['cummax', 'cummin', 'cumsum', 'lag', 'lead', 'pct_change', 'rolling_mean', 'rolling_sum'])", "alternatives": []} | disclosures: []
   frame disclosures: []
  EXEC outcome: error
   col d | no_result: {"kind": "error", "discriminator": null, "reason": "unknown", "detail": "'distinct' is not a scan operator (registry scans: ['cummax', 'cummin', 'cumsum', 'lag', 'lead', 'pct_change', 'rolling_mean', 'rolling_sum'])", "alternatives": []} | disclosures: []
   DATA: None
====================================================================================================
[P-18] SELECT sum(level @ {store, day}) AS s AT {region}
  PLAN outcome: error
   col s | no_result: {"kind": "error", "discriminator": null, "reason": "unknown", "detail": "'level' has a family ['last', 'max', 'min', 'count'] \u2014 specify a member", "alternatives": []} | disclosures: []
   frame disclosures: []
  EXEC outcome: error
   col s | no_result: {"kind": "error", "discriminator": null, "reason": "unknown", "detail": "'level' has a family ['last', 'max', 'min', 'count'] \u2014 specify a member", "alternatives": []} | disclosures: []
   DATA: None
====================================================================================================
[P-18c] SELECT median(revenue @ {transaction}) AS md AT {customer}
  PLAN outcome: error
   col md | no_result: {"kind": "error", "discriminator": null, "reason": "unknown", "detail": "'median' is not a scan operator (registry scans: ['cummax', 'cummin', 'cumsum', 'lag', 'lead', 'pct_change', 'rolling_mean', 'rolling_sum'])", "alternatives": []} | disclosures: []
   frame disclosures: []
  EXEC outcome: error
   col md | no_result: {"kind": "error", "discriminator": null, "reason": "unknown", "detail": "'median' is not a scan operator (registry scans: ['cummax', 'cummin', 'cumsum', 'lag', 'lead', 'pct_change', 'rolling_mean', 'rolling_sum'])", "alternatives": []} | disclosures: []
   DATA: None
====================================================================================================
[P-17] FROM retail_manifold SELECT unique_visitors AT {store}
  PLAN outcome: disclose
   col unique_visitors | no_result: null | disclosures: [{"code": "approximation", "materiality": "material", "severity": "info", "category": "approximation", "detail": "unique_visitors.distinct: HLL distinct estimate [HLLSketch(12)]", "remedy": null, "source": null, "rel_error": 0.01625}]
   frame disclosures: []
  EXEC outcome: disclose
   col unique_visitors | no_result: null | disclosures: [{"code": "approximation", "materiality": "material", "severity": "info", "category": "approximation", "detail": "unique_visitors.distinct: HLL distinct estimate [HLLSketch(12)]", "remedy": null, "source": null, "rel_error": 0.01625}]
   DATA: shape: (2, 2)
┌───────┬─────────────────┐
│ store ┆ unique_visitors │
│ ---   ┆ ---             │
│ str   ┆ f64             │
╞═══════╪═════════════════╡
│ S1    ┆ 1.0             │
│ S2    ┆ 1.0             │
└───────┴─────────────────┘
====================================================================================================
[M-L940] FROM finance_manifold SELECT cumsum( revenue @ {customer, day} ) AS revenue_to_date AT {customer, day}
  PLAN outcome: serve
   col revenue_to_date | no_result: null | disclosures: []
   frame disclosures: []
  EXEC outcome: serve
   col revenue_to_date | no_result: null | disclosures: [{"code": "provenance", "materiality": "immaterial", "severity": "info", "category": "transport", "detail": "scan cumsum over order 'day' within ['customer']", "remedy": null, "source": null, "rel_error": null}]
   DATA: shape: (4, 3)
┌──────────┬────────────┬─────────────────┐
│ customer ┆ day        ┆ revenue_to_date │
│ ---      ┆ ---        ┆ ---             │
│ str      ┆ str        ┆ f64             │
╞══════════╪════════════╪═════════════════╡
│ C1       ┆ 2024-01-05 ┆ 120.0           │
│ C1       ┆ 2024-01-19 ┆ 200.0           │
│ C2       ┆ 2024-02-02 ┆ 200.0           │
│ C3       ┆ 2023-02-03 ┆ 150.0           │
└──────────┴────────────┴─────────────────┘
====================================================================================================
[P-13b] FROM finance_manifold SELECT lag( revenue @ {customer, day}, n = 1 ) AS prev AT {customer, day}
  PLAN outcome: serve
   col prev | no_result: null | disclosures: []
   frame disclosures: []
  EXEC outcome: disclose
   col prev | no_result: null | disclosures: [{"code": "provenance", "materiality": "immaterial", "severity": "info", "category": "transport", "detail": "scan lag over order 'day' within ['customer']", "remedy": null, "source": null, "rel_error": null}, {"code": "undeclared_absence", "materiality": "material", "severity": "caution", "category": "undeclared_absence", "detail": "3 absent cell(s) with no declared fill rule \u2014 the engine dis
   DATA: shape: (4, 3)
┌──────────┬────────────┬───────┐
│ customer ┆ day        ┆ prev  │
│ ---      ┆ ---        ┆ ---   │
│ str      ┆ str        ┆ f64   │
╞══════════╪════════════╪═══════╡
│ C1       ┆ 2024-01-05 ┆ null  │
│ C1       ┆ 2024-01-19 ┆ 120.0 │
│ C2       ┆ 2024-02-02 ┆ null  │
│ C3       ┆ 2023-02-03 ┆ null  │
└──────────┴────────────┴───────┘
====================================================================================================
[P-05b] SELECT revenue AT {}
  PLAN outcome: serve
   col revenue | no_result: null | disclosures: []
   frame disclosures: []
  EXEC outcome: serve
   col revenue | no_result: null | disclosures: []
   DATA: shape: (1, 1)
┌─────────┐
│ revenue │
│ ---     │
│ f64     │
╞═════════╡
│ 550.0   │
└─────────┘
```

### A.3 — verbatim output of `/tmp/probe_extra.py` (the attribution variants, run separately first)

```
==========================================================================================
[X-alias-AS] FROM retail_manifold SELECT total(revenue) AS t, unique_visitors AT {store}
  PLAN: error [('t', 'unknown', "'total' is not a scan operator (registry scans: ['cummax', 'cummin', 'cumsum', 'lag', 'lead', 'pct_change', 'rolling_mean', 'rolling_sum'])"), ('unique_visitors', None, None)]
  EXEC: error [('t', 'unknown', "'total' is not a scan operator (registry scans: ['cummax', 'cummin', 'cumsum', 'lag', 'lead', 'pct_change', 'rolling_mean', 'rolling_sum'])"), ('unique_visitors', None, None)]
  DATA: shape: (2, 2) ┌───────┬─────────────────┐ │ store ┆ unique_visitors │ │ --- ┆ --- │ │ str ┆ f64 │ ╞═══════╪═════════════════╡ │ S1 ┆ 1.0 │ │ S2 ┆ 1.0 │ └───────┴─────────────────┘
==========================================================================================
[X-gen-last] SELECT sum(level.last @ {store, day}) AS s AT {region}
  PLAN: serve [('s', None, None)]
  EXEC: serve [('s', None, None)]
  DATA: shape: (2, 2) ┌────────┬─────┐ │ region ┆ s │ │ --- ┆ --- │ │ str ┆ i64 │ ╞════════╪═════╡ │ east ┆ 930 │ │ west ┆ 300 │ └────────┴─────┘
==========================================================================================
[X-gen-max] SELECT max(level.last @ {store, day}) AS m AT {region}
  PLAN: serve [('m', None, None)]
  EXEC: serve [('m', None, None)]
  DATA: shape: (2, 2) ┌────────┬─────┐ │ region ┆ m │ │ --- ┆ --- │ │ str ┆ i64 │ ╞════════╪═════╡ │ east ┆ 500 │ │ west ┆ 300 │ └────────┴─────┘
==========================================================================================
[X-level-sum-member] SELECT level.sum AS s AT {region}
  PLAN: error [('s', 'unknown', "'level' has no family member 'sum' (have ['last', 'max', 'min', 'count'])")]
  EXEC: error [('s', 'unknown', "'level' has no family member 'sum' (have ['last', 'max', 'min', 'count'])")]
  DATA: None
==========================================================================================
[X-median-unpinned] SELECT median(revenue) AS md AT {customer}
  PLAN: error [('md', 'unknown', "'median' is not a scan operator (registry scans: ['cummax', 'cummin', 'cumsum', 'lag', 'lead', 'pct_change', 'rolling_mean', 'rolling_sum'])")]
  EXEC: error [('md', 'unknown', "'median' is not a scan operator (registry scans: ['cummax', 'cummin', 'cumsum', 'lag', 'lead', 'pct_change', 'rolling_mean', 'rolling_sum'])")]
  DATA: None
==========================================================================================
[X-sum-level-store] SELECT sum(level.last @ {store, day}) AS s AT {store}
  PLAN: serve [('s', None, None)]
  EXEC: serve [('s', None, None)]
  DATA: shape: (2, 2) ┌───────┬─────┐ │ store ┆ s │ │ --- ┆ --- │ │ str ┆ i64 │ ╞═══════╪═════╡ │ S1 ┆ 930 │ │ S2 ┆ 300 │ └───────┴─────┘
==========================================================================================
[X-count-inline] SELECT count(revenue @ {transaction}) AS n AT {customer}
  PLAN: serve [('n', None, None)]
  EXEC: serve [('n', None, None)]
  DATA: shape: (3, 2) ┌──────────┬─────┐ │ customer ┆ n │ │ --- ┆ --- │ │ str ┆ u32 │ ╞══════════╪═════╡ │ C1 ┆ 2 │ │ C2 ┆ 1 │ │ C3 ┆ 1 │ └──────────┴─────┘
==========================================================================================
[X-mean-inline] SELECT mean(revenue @ {transaction}) AS n AT {customer}
  PLAN: serve [('n', None, None)]
  EXEC: serve [('n', None, None)]
  DATA: shape: (3, 2) ┌──────────┬───────┐ │ customer ┆ n │ │ --- ┆ --- │ │ str ┆ f64 │ ╞══════════╪═══════╡ │ C1 ┆ 100.0 │ │ C2 ┆ 200.0 │ │ C3 ┆ 150.0 │ └──────────┴───────┘
==========================================================================================
[X-cumsum-noorder] SELECT cumsum( revenue @ {customer} ) AS c AT {customer}
  PLAN: serve [('c', None, None)]
  EXEC: error [('c', 'unknown', "scan 'cumsum' @ ('customer',) has no derivable order axis (no CERTIFIED temporal level in the anchor); name it with by=<level>. A declared-but-uncertified hierarchy confers no order axis — declaration makes structure eligible for certification, not executable.")]
  DATA: None
==========================================================================================
[X-unknown-measure] SELECT nosuchmeasure AT {customer}
  PLAN: error [('nosuchmeasure', 'unknown', "unknown column 'nosuchmeasure'")]
  EXEC: error [('nosuchmeasure', 'unknown', "unknown column 'nosuchmeasure'")]
  DATA: None
==========================================================================================
[X-unknown-op] SELECT frobnicate(revenue @ {transaction}) AS f AT {customer}
  PLAN: error [('f', 'unknown', "'frobnicate' is not a scan operator (registry scans: ['cummax', 'cummin', 'cumsum', 'lag', 'lead', 'pct_change', 'rolling_mean', 'rolling_sum'])")]
  EXEC: error [('f', 'unknown', "'frobnicate' is not a scan operator (registry scans: ['cummax', 'cummin', 'cumsum', 'lag', 'lead', 'pct_change', 'rolling_mean', 'rolling_sum'])")]
  DATA: None
```

## Appendix B — verbatim output of the semantic gate

```
$ PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.../packages/columna-core/src \
    /tmp/fqvenv/bin/python docs/tools/check_manual_frameql.py --verbose
  L158   execute  serve     provenance             SELECT sum(revenue @ {transaction}), sum(cost @ {transaction
  L202   execute  serve                            SELECT revenue AS total_revenue, (revenue - cost) AS profit 
  L250   execute  serve     provenance             EXPLAIN FROM finance_manifold SELECT max( sum(revenue @ {tra
  L315   execute  serve     provenance             SELECT sum(revenue @ {transaction}) AS gross AT {customer}
  L315   execute  serve     provenance             SELECT max(revenue @ {transaction}) AS peak_txn AT {customer
  L315   execute  serve     provenance             SELECT avg(aov @ {day}) AS typical AT {customer}
  L325   plan     clarify   input_anchor_ambiguous SELECT avg(aov) AT {region}
  L374   execute  serve                            SELECT (revenue @ {customer, day}) - (cost @ {customer, day}
  L374   execute  serve                            SELECT (revenue @ {transaction}) / (orders @ {transaction}) 
  L389   execute  serve                            SELECT revenue AS revenue, level.last AS inv AT {region}
  L401   execute  serve                            SELECT (revenue @ {customer}) / (revenue @ {}) AS share_of_t
  L413   execute  serve     provenance             SELECT max( sum(revenue @ {transaction}) @ {customer, month}
  L524   execute  serve                            FROM finance_manifold SELECT revenue AT {customer} WHERE day
  L537   execute  serve     provenance             FROM finance_manifold SELECT sum(revenue @ {transaction}) AT
  L665   execute  serve                            FROM finance_manifold WITH profit = (revenue - cost) SELECT 
  L756   execute  disclose  multi_counted          SELECT revenue AT {category.touch}
  L756   execute  disclose  memberships_unrepresented SELECT revenue AT {category.assign}
  L756   execute  serve     reconciliation         SELECT revenue AT {category.alloc}
  L795   execute  serve                            FROM finance_manifold SELECT revenue AT {customer}
  L833   execute  serve     provenance             FROM finance_manifold SELECT max( sum(revenue @ {transaction
  L843   execute  serve     provenance             FROM product_manifold SELECT mean( engagement_score @ {custo
  L852   execute  serve                            FROM finance_manifold SELECT (revenue - cost) AS profit AT {
  L861   execute  serve                            FROM finance_manifold SELECT ( revenue @ {customer} ) / ( re
  L887   execute  serve                            FROM finance_manifold SELECT revenue AT {customer} WHERE day
  L914   execute  serve                            FROM finance_manifold SELECT revenue AS total_revenue AT {cu
  L924   execute  serve                            FROM product_manifold SELECT product_revenue AT {category, p
  L988   execute  serve                            FROM finance_manifold WITH profit = (revenue - cost) SELECT 
manual FrameQL examples: 40 total — 27 shipped (planned, and executed where they plan to serve/disclose), 11 roadmap, 1 marked ill-formed, 1 schematic, 0 FAIL
EXIT=0
```

### B.1 — gate coverage map (which Manual fenced blocks the gate does and does not see)

Produced by re-using the gate's own `_fenced_blocks` / `_statements` / `sections` / `owning_section` functions:

```
L117   covered=False kind=(bare)             mark=None      n_stmts=1  §1.2 The skeleton
L137   covered=False kind=text               mark=None      n_stmts=1  §1.3 The `FROM` clause
L158   covered=True  kind=frameql            mark=None      n_stmts=1  §1.4 The `SELECT` clause and the output ancho
L202   covered=True  kind=frameql            mark=None      n_stmts=1  §1.6 Series names and the `AS` alias
L250   covered=True  kind=frameql            mark=None      n_stmts=1  §1.7 Statements: queries and `EXPLAIN`
L276   covered=True  kind=frameql-schematic  mark=None      n_stmts=1  §2.1 The shape of the canonical form
L315   covered=True  kind=frameql            mark=None      n_stmts=3  §2.3 Single-series reducers and the input pin
L325   covered=True  kind=frameql            mark=None      n_stmts=1  §2.3 Single-series reducers and the input pin
L374   covered=True  kind=frameql            mark=None      n_stmts=2  §2.4 Map expressions
L389   covered=True  kind=frameql            mark=None      n_stmts=1  §2.5 One expression, one universe
L401   covered=True  kind=frameql            mark=None      n_stmts=1  §2.6 Broadcast
L413   covered=True  kind=frameql            mark=None      n_stmts=1  §2.7 Composite reductions
L474   covered=False kind=(bare)             mark=None      n_stmts=1  §3.1 Sugar: default-family reduction implicit
L495   covered=False kind=(bare)             mark=None      n_stmts=1  §3.2 Sugar: omitting `@ root(col)` for direct
L524   covered=True  kind=frameql            mark=None      n_stmts=1  §4.1 The `WHERE` clause: pre-query input filt
L537   covered=True  kind=frameql            mark=None      n_stmts=1  §4.1 The `WHERE` clause: pre-query input filt
L560   covered=True  kind=frameql-roadmap    mark=SCHEDULED n_stmts=1  §4.1.1 Filtering through a relationship-deriv
L579   covered=True  kind=frameql-roadmap    mark=ROADMAP   n_stmts=1  §4.2 The `HAVING` clause: post-query output f
L609   covered=False kind=(bare)             mark=None      n_stmts=1  §4.3 The `ORDER BY` clause
L621   covered=False kind=(bare)             mark=None      n_stmts=1  §4.4 The `LIMIT n` clause and `LIMIT n PER {d
L630   covered=False kind=(bare)             mark=None      n_stmts=1  §4.4 The `LIMIT n` clause and `LIMIT n PER {d
L665   covered=True  kind=frameql            mark=None      n_stmts=1  §4.5 The `WITH` clause: named bindings
L747   covered=False kind=(bare)             mark=None      n_stmts=1  §5.6 Many-to-many
L756   covered=True  kind=frameql            mark=None      n_stmts=3  §5.6 Many-to-many
L795   covered=True  kind=frameql            mark=None      n_stmts=1  §6.1 Simple aggregation
L806   covered=True  kind=frameql-roadmap    mark=ROADMAP   n_stmts=1  §6.2 Multiple metrics at a shared anchor **[R
L833   covered=True  kind=frameql            mark=None      n_stmts=1  §6.3 Composite reduction with explicit interm
L843   covered=True  kind=frameql            mark=None      n_stmts=1  §6.4 Mean with explicit input anchor
L852   covered=True  kind=frameql            mark=None      n_stmts=1  §6.5 Map of co-anchored columns
L861   covered=True  kind=frameql            mark=None      n_stmts=1  §6.6 Ratio across grains
L874   covered=True  kind=frameql-roadmap    mark=ROADMAP   n_stmts=1  §6.7 Bracket filter on a column **[ROADMAP]**
L887   covered=True  kind=frameql            mark=None      n_stmts=1  §6.8 WHERE: pre-query filtering on a base dim
L903   covered=True  kind=frameql-roadmap    mark=SCHEDULED n_stmts=1  §6.8a WHERE through a relationship-derived di
L914   covered=True  kind=frameql            mark=None      n_stmts=1  §6.9 HAVING: post-query filtering
L924   covered=True  kind=frameql            mark=None      n_stmts=1  §6.10 Top N per group
L940   covered=True  kind=frameql-roadmap    mark=ROADMAP   n_stmts=1  §6.11 Scan for running total **[ROADMAP]**
L955   covered=True  kind=frameql-illformed  mark=ROADMAP   n_stmts=1  §6.12 Many-to-many with allocation `[ROADMAP]
L970   covered=True  kind=frameql-roadmap    mark=ROADMAP   n_stmts=1  §6.13 Time intelligence: year-to-date and yea
L978   covered=True  kind=frameql-roadmap    mark=ROADMAP   n_stmts=1  §6.13 Time intelligence: year-to-date and yea
L988   covered=True  kind=frameql            mark=None      n_stmts=1  §6.14 Macro bindings for reuse
L1008  covered=True  kind=frameql-roadmap    mark=SCHEDULED n_stmts=1  §6.15 The envelope, end to end **[SCHEDULED]*
L1027  covered=True  kind=frameql-roadmap    mark=SCHEDULED n_stmts=1  §6.16 Composite input anchor: a two-stage sta
L1168  covered=True  kind=frameql-roadmap    mark=ROADMAP   n_stmts=1  §8.2 Name aliases **[ROADMAP]**
L1283  covered=False kind=(bare)             mark=None      n_stmts=1  §Appendix D: Lineage — the retired terse `@`-

44 fenced blocks / 49 statements walked; 35 blocks covered by the gate, 9 skipped (covered=False).
```

## Appendix C — test runs at this commit

```
$ pytest packages/columna-core/tests -q
669 passed, 21 skipped in 32.49s

$ pytest packages/columna-core/tests/{test_where_capability_gate,test_frameql_parse,test_envelope_planner,
         test_envelope_parser,test_envelope_sugars,test_pin_admissibility,test_inline_reduction,
         test_map_operand_pin,test_generated_family_law,test_hll_case_study,test_operator_umbrella}.py -q
235 passed in 17.41s

No failures. No test in the suite is red at this commit, in a fresh process with __pycache__ cleared,
PYTHONDONTWRITEBYTECODE=1 and pyarrow installed. Every "unsupported"/"error" cell above therefore
records shipped behaviour that the suite does not consider a defect -- not a broken environment.

DISCARDED (environment artifact, recorded so it is not mistaken for evidence):
the first run of the full suite, before pyarrow was installed, gave "9 errors during collection"
(test_coanchor, test_confine, test_hll_case_study, test_holistic, test_locus, test_operator_umbrella,
test_projection, test_types, test_universe_check -- all "RuntimeError: demo batch ..." rooted in
ModuleNotFoundError: No module named pyarrow). No cell in this matrix derives from that run.
```
