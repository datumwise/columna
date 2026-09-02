# Open forks — decisions the code made provisionally, awaiting a ruling

Sibling to [`doctrine_gaps.md`](doctrine_gaps.md). The two are opposite directions of the same seam:

- a **doctrine gap** is *code lagging ruled doctrine* (ruled, not yet built);
- an **open fork** is *code ahead of doctrine* — the implementation had to pick something (a vocabulary
  code, a materiality, a shape) that Huayin has **not yet ruled**, so it used the closest-fitting
  existing choice and flagged it.

**The rule.** Every fork surfaced in a PR gets a row here **before that PR merges** — so nothing open
ever lives only in a PR description (prose no one is obliged to reread). A row carries the provisional
choice actually shipped, the alternatives, a recommendation, and a link to where it came from. It is
struck when Huayin rules, with the ruling and its landing named. The queue is Huayin's; this file is
only its durable form.

| # | opened | fork (the open question) | provisional choice shipped | alternatives | recommendation | source | status |
|---|---|---|---|---|---|---|---|
| ~~OF-1~~ | 2026-07-14 | **Unpinned-inline-reduction clarify reason.** Which reason code carries the engine clarify for an inline reduction with no pinned input anchor (`avg(aov)@month`)? | Reused **`ambiguous_grain`** (CLARIFY/AMBIGUOUS) — the closest fit in the closed `REASON_OUTCOME` vocabulary; no code minted. | (a) keep `ambiguous_grain` — but its gloss reads "attribute keyed at several levels", so reuse broadens it; (b) a new reserved reason `input_anchor_ambiguous`. | Reuse `ambiguous_grain` **and** widen its gloss to cover input-anchor underdetermination — unless a distinct reason aids the agent surface, in which case mint `input_anchor_ambiguous`. | [PR #18](https://github.com/datumwise/columna/pull/18); capture v0.8 §"Reduction OF a derivation"; `disclosure.py` `REASON_OUTCOME` | ~~**RULED (b)** 2026-07-14: mint `input_anchor_ambiguous` (CLARIFY/AMBIGUOUS), sibling to `co_anchor_ambiguous`; `ambiguous_grain` gloss NOT widened. Standing rule set: **one reason per contested dimension**. The clarify names the same dimension OF-2's disclosure records.~~ |
| ~~OF-2~~ | 2026-07-14 | **Pinned-inline-reduction communicative disclosure + the input_anchor-fit finding** (owed to CP-B2). Does an explicitly user-pinned input anchor (`avg(aov@day)`) owe a caveat, and if so which — material or immaterial? | Served with the **immaterial `provenance`** code (category `transport`) naming the reading; **not** the material `input_anchor` caveat. | (a) immaterial `provenance` [shipped]; (b) no disclosure at all; (c) a new reserved communicative code. | **(a).** Finding: an explicitly user-pinned anchor is a deliberate, visible choice, so it owes a *communicative* (immaterial) note — not the material `input_anchor` caveat, which is for an anchor choice imported from a name or defaulted (one the reader must weigh); an explicit pin is the reader's own. | [PR #18](https://github.com/datumwise/columna/pull/18); `disclosure_wire.py` `CATEGORY_TABLE`; CV2-2 in [`design_capture_outcome_pair_v0_1.md`](context/design_capture_outcome_pair_v0_1.md) | ~~**RULED (a)** 2026-07-14: ratified as shipped. **Boundary (durable finding):** material `input_anchor` is for an anchor choice IMPORTED from a name or DEFAULTED (one the reader must weigh); an EXPLICIT pin owes only the immaterial `provenance` note — because the wire's reader may not be the asker.~~ |

| OF-3 | 2026-07-16 | **ASSERT row-form base-row data channel.** How is a row-predicate ASSERT (`ASSERT <n> ON <u> WHERE <pred>`) data-tested at publish — the scan that checks every atom of the universe satisfies the predicate? | **UNTESTABLE** shipped: recorded on authored authority, visible in describe, never exercised. The invariant-form has its full data channel (serve LHS/RHS at the anchor, compare per op); the row-form does not yet. | (a) a bounded base-row scan through the typed connector surface (count atoms failing the predicate at the universe grain), CONTRADICTED if any violate; (b) a materialized-count assertion; (c) leave UNTESTABLE until a row-assert appears in a real manifold. | **(a)** — when a row-assert first needs teeth, through the two-ends aperture (the typed connector calls, never general SQL). **Gates nothing today; must not evaporate** (Huayin's rider, 2026-07-16). | CP-1 increment 3 ([PR #35](https://github.com/datumwise/columna/pull/35)); `adjudication.py` `_prove_assert` row branch | **OPEN** |

| OF-4 | 2026-07-16 | **Query-side `universe` arg / ON-UNIVERSE apply removal (§2c consequence).** §2c makes ON UNIVERSE dead in the query grammar (the expression law deleted its last query-side job), but the server `query(..., universe=)` arg, the wire's `on_universe`→`apply:{universe}` remediation (`disclosure_wire._wire_alternative`, `_UNIVERSE_RE`), and the agent's clarify-PICK (`agent/loop.py` applies `alts[idx].apply.universe`) still exist. | **Kept, dormant:** no §2c reason emits a universe-alternative (co_anchor was the only one, now retired), so the whole apply/pick path is dead code. The core expression/frame laws landed; the SERVER surface removal is a pinned deferral (per Huayin's scope-split ruling, OF-3 precedent). | (a) remove the arg + wire-apply + redesign the agent pick to reformulate the query (pin an input anchor) rather than apply a universe; (b) leave it dormant until a coordinated server/agent pass. | **(a)** in a coordinated server+agent increment (the agent's clarify-pick round-trip moves with it — its relay-and-never-auto-pick behavior is already §2c-correct). | CP-1 §2c ([PR #35](https://github.com/datumwise/columna/pull/35)); `columna_server/tools.py`, `server.py`, `agent/loop.py`; `disclosure_wire._wire_alternative` | **OPEN** |

| OF-5 | 2026-07-16 | **The declared spine-grid — a level's DOMAIN source.** B3 absence is only definable relative to a domain. Two customers both need it: (a) SINGLE-COLUMN events zero-fill (a lone events query has no local domain, so absence is not materialized — only the juxtaposition supplies one); (b) the spine/product COMPLETENESS oracle (internal-contiguity needs the ordered axis's min/max/distinct; boundary completeness needs the full expected grid) — a connector domain-read the typed aperture does not yet expose. | **Absence scoped to the juxtaposition** (the local domain); BASIS adjudication mints **UNTESTABLE** per type (serving follows the declaration regardless — a semantic declaration, not a shortcut). No live spine refutation channel yet. | (a) a declared spine-grid object (a domain source per orderable level) + a typed connector domain-read (min/max/distinct, membership) — unlocks single-column fill AND the spine internal-contiguity CONTRADICTED channel + registry membership; (b) leave absence juxtaposition-scoped and BASIS UNTESTABLE until Authoring declares grids. | **(a)** when the domain source is declarable (Authoring-era / the connector-aperture pass). Huayin (2026-07-16): internal-contiguity is grid-free IN PRINCIPLE (min/max/distinct on an ordered axis), but the connector domain-read it needs IS this grid object. | CP-1 increment 6 ([PR #35](https://github.com/datumwise/columna/pull/35)); `planner.run` absence pass; `adjudication._prove_basis` | **OPEN** |

| OF-6 | 2026-07-16 | **Draft persistence (cross-session serialization).** The A4 authoring loop's human turns (review → revise → declare → publish) will span sessions once a real provider / interactive `columna init` ships — at which point the in-memory `Draft` (proposals + marks + state) needs a serialization to survive between turns. | **In-memory only.** The hermetic loop runs in-process (single session), so no serialization exists; the draft state (grades, review marks, state-machine position) is lost across process boundaries. | (a) serialize the Draft (its own format, or lower-to-.cml-plus-a-review-sidecar) when the interactive loop lands; (b) keep in-memory until then. | **(a)** — its trigger is the NEXT step (wiring a real provider / interactive init is exactly when human turns start spanning sessions), so the row is opened now, not on prophecy (Huayin, 2026-07-16). | CP-2 artifact 3 ([branch `wp-cp2-init`]); `columna_core.draft`, `columna_server.init.loop` | **OPEN** |
| OF-7 | 2026-07-17 | **Package-served Explorer deployment.** The Explorer is built in `apps/website/` as a portable component (binds any describe JSON, zero site coupling). The ruled near-future path — `columna-server` offering the Explorer against a LIVE manifold's describe — is not built. | **Site-instance only.** CP-3 ships the `/explorer` demo-manifold instance; the component is portable by construction, but no package-serving entry point exists yet. | (a) a `columna-server explorer`/HTTP surface serving the component against a live manifold; (b) leave site-only until a product-deployment WP. | **(a)** as a recorded near-future path — a later WP, not CP-3 (Huayin, 2026-07-17: portable by construction now, package-served next). | CP-3 opening proposal (§a C-3, `wp_cp3_opening_proposal_v0_1.md`); capture §6 Posture | **OPEN** |
| OF-8 | 2026-07-17 | **Author-facing provenance surface (FROM/VIA).** A future Explorer layer showing the humans who DECLARED members (FROM/VIA provenance) is conceivable — but its data could NEVER come from describe (describe carries no physical/authorship identity by the §2b insulation guarantee) and would need its OWN governed source. | **Not built, not designed.** Rowed per Huayin's 'row it, don't design it' (2026-07-17): a conceivable layer, deliberately unspecified. | (a) design a governed author-provenance source + surface; (b) never build it (describe-only Explorer is complete). | **Undecided** — a file note only; revisit if/when author-provenance is a product need. Must not leak into C-3 (describe-only). | CP-3 opening proposal (§a ruling 2, `wp_cp3_opening_proposal_v0_1.md`) | **OPEN** |
| OF-9 | 2026-07-17 | **Logical attribute declarations for predicate terms.** C-2 renders universe predicates logically by DROPPING the physical table qualifier (`stores.opened_date` -> `opened_date`), so no STRUCTURAL physical identifier crosses describe — but a bare predicate attribute name still renders as the author wrote it (a residue, not a declared logical name). | **Drop-the-qualifier shipped** (CP-3 C-2): no table names, no qualified `table.column`; predicate attribute names render verbatim. The standing no-physical-identifier test asserts exactly this structural guarantee (not full verification). | (a) a definition-language extension — declared logical names for predicate attributes (a new authoring surface, with init implications); (b) leave drop-the-qualifier as the guarantee. | **(a)** as its OWN WP, NOT improvised before a freeze (Huayin, 2026-07-17). When it lands, describe renders declared names and the standing test tightens from 'no structural identifiers' to full verification. | CP-3 C-2 (`tools.py::_render_ref`); capture §2b insulation guarantee; `test_describe_insulation.py` | **OPEN** |
| OF-10 | 2026-07-17 | **§2c definition-time-population mechanism.** A DERIVED/expression that spans more than one universe is a `cross_universe` error; §2c says the population pin 'lives in definitions', but the grammar has no definition-time universe pin (only `AT <level>`). Its named customer, `sell_through_rate`, was KILLED (S-1 superseded), so the mechanism has no sponsor. | **Not built.** No definition-time population pin exists; a cross-universe derived fails closed. | (a) a definition-time population/universe pin in the DERIVED grammar (a new authoring surface); (b) leave cross-universe derived as fail-closed errors. | **Rowed, no sponsor** (Huayin, 2026-07-17): rows record designs, not sponsors — revisit if a real within-manifold need appears. | CP-3 S-1 superseded (`wp_cp3_opening_proposal_v0_1.md`); planner `_check_single_universe` | **OPEN** |

| ~~OF-16~~ | 2026-07-25 | **Reference manual §26.6 `HIERARCHY` is inverted and stale.** Its status annotation reads "single functional edge: SHIPPED 0.7.8 — via `EDGE <child> -> <parent> ALONG <lineage> VIA <table>(…)`" and "`HIERARCHY` … SCHEDULED". The truth is the exact inverse: EDGE is PURGED (case-demo §2a) and HIERARCHY is the sole shipped surface. §26.6's body also gives the signature as `HIERARCHY <name> <child> -> <parent>` — no braces, no per-hop `VIA` — which the shipped parser rejects. | **Left unchanged.** The purge sweep ([PR #90](https://github.com/datumwise/columna/pull/90)) fixed the fixture, the core README, a benchmark fixture and a test; the MANUAL is ratified content and a §26.6 rewrite is a content pass, not a fixture rewrite, so it was rowed rather than improvised. The purged-grammar CI guard carries a ROWED exemption keyed to this fork — it prints the fossil on every run and FAILS if this row is closed while the file still contains it. | (a) desk rewrites §26.6 (status annotation corrected + body signature to `HIERARCHY <lineage> { <a> -> <b> VIA t(a,b) [-> …] [; <path>] }`); (b) agent drafts the correction for ratification; (c) leave until a manuals-alignment WP. | **(a) or (b)** — the annotation is a factual SHIPPED/SCHEDULED claim that is now false in both directions, which is worse than prose drift: a reader following §26.6 writes grammar the parser rejects. Recommend it not wait for a WP. | [PR #90](https://github.com/datumwise/columna/pull/90); `scripts/check_purged_grammar.py` ROWED; `docs/columna_reference_manual_5e.md` §26.6 | ~~**CLOSED** 2026-07-26~~ · ~~Closed by the desk-drafted correction ([`specs/of16_of17_manual_correction_desk_draft_v0_1.md`](of16_of17_manual_correction_desk_draft_v0_1.md)), applied verbatim: §26.6's status annotation un-inverted (HIERARCHY SHIPPED / verification SCHEDULED) and its body signature corrected to braces + per-hop VIA, with a worked form from the shipped demo. Verified BY EXECUTION against columna-core 0.12.0: both documented forms parse, the old signature is still rejected. The purged-grammar guard's ROWED exemption is removed (the file is clean) and the guard is green.~~ |

| ~~OF-17~~ | 2026-07-25 | **Keyword-set fossils are invisible to the pattern guard.** The Chapter 26 preamble (`docs/columna_reference_manual_5e.md:1476`) lists `EDGE` in the "shipped 0.7.8 keyword set" — a purged keyword named bare, not in its full `EDGE … ALONG … VIA` surface form. `scripts/check_purged_grammar.py` deliberately requires the full shape, so it cannot see this. | **Left as-is; guard NOT widened.** Widening the pattern to catch a bare `EDGE` keyword would false-positive on every legitimate use of the word "edge" (internal taxonomy, prose, `kind="edge"`) and poison a guard with a currently-perfect record. | (a) the OF-16 docs pass, when it lands, sweeps Chapter 26's keyword set BY HAND and closes this row with it; (b) a separate narrower guard for keyword-set lines only. | **(a)** (Huayin, 2026-07-25): guards catch classes, hand-sweeps catch the rest; knowing which is which is the discipline. This row rides OF-16 to closure. | [PR #90] found the class; the preamble instance surfaced in the OF-16 draft ([`specs/of16_manual_26_6_correction_draft_v0_1.md`](of16_manual_26_6_correction_draft_v0_1.md)) | ~~**CLOSED** 2026-07-26~~ · ~~Closed WITH OF-16 per its ruled option (a) — the hand-sweep rode the docs pass. Chapter 26's preamble keyword set now reads the shipped short forms (MANIFOLD · UNIVERSE · LEVEL+ATTR · HIERARCHY · RELATE+faces · MEASURE · DERIVED · ASSERT), derived by execution from the parser's `_KW`. The stale pinned "0.7.8" is dropped in favour of "the shipped keyword set" so the sentence cannot rot at the next release. Note: the ledger link to CC's own draft was DANGLING — that file existed only in an unpushed working tree (0 commits touched it); the desk draft supersedes it and this row now points at the artifact that shipped.~~ |


| OF-18 | 2026-07-26 | **Chapter 26 status-mark audit.** §26.6's SHIPPED/SCHEDULED marks were inverted; nothing has checked whether the chapter's OTHER subsections (`DIMENSION`, `ALIAS`, `ASSERT`, `WITHHOLD`, §26.10) carry stale marks too. A status annotation is a factual claim about what ships, and one was wrong by 180°. | **Not audited.** OF-16 deliberately touched only §26.6 + the preamble; a chapter-wide audit was rowed rather than smuggled into a one-section correction (desk scope discipline, §4 of the correction draft). | (a) audit every §26 status mark against the shipped package by execution, correcting in one pass; (b) audit the whole manual, not just Chapter 26. | **(a)** first — Chapter 26 is where the marks are densest and where one was already proven wrong. A mark that cannot be produced by executing the shipped package is stale by definition. | the OF-16 correction draft §6; [PR for OF-16/OF-17] | **OPEN** · **FORM-PRIMACY IS PART OF THE DEFECT (2026-07-26, external-AI probe):** a model reading the manuals produced a Manifold the shipped parser REJECTS on three construct types (MANIFOLD without VERSION, LEVEL without `= <column>`, MEASURE without `FROM … AS …`) — while getting HIERARCHY right, which is the §26.6 correction working in the wild. Root cause is structural, not typographical: Chapter 26 presents LONG forms as primary and the SHIPPED short forms as parentheticals, so a careful reader learns the wrong one. The audit must therefore cover FORM PRIMACY, not only status marks. |

| OF-19 | 2026-07-26 | **Stale pinned version references in the manual.** "0.7.8" appears as a hard-coded version throughout Chapter 26's annotations (and likely beyond). The OF-16 pass dropped it in the one clause it touched, in favour of "the shipped keyword set", precisely so that sentence cannot rot again. | **One clause fixed, the rest left.** Every other pinned "0.7.8" still reads as a live claim about the current release. | (a) sweep pinned versions out of prose where the claim is really "what ships now"; (b) keep the numbers and add them to a release checklist to bump. | **(a)** — a version number in prose is a claim that goes stale silently, and nothing in CI reads prose. Prefer unpinned phrasing over a bump-list nobody runs. | the OF-16 correction draft §6; [PR for OF-16/OF-17] | **OPEN** |

| OF-20 | 2026-07-26 | **Two §26.6 clauses may be spec-ahead-of-code.** The correction PRESERVED, verbatim, two claims neither the desk nor CC could ground in shipped code: that scan parameters `reset`/`within`/`step` resolve along a hierarchy (no such Frame-QL surface found in `frameql.py`), and that redundantly declared diamonds are checked for commuting (no such check found in the shipped adjudicator). | **Preserved as written.** They were carried over because the correction's scope was the inversion + the signature, and silently deleting doctrine is worse than carrying an unverified clause — but they are now flagged rather than assumed true. | (a) verify each against the shipped package; if unimplemented, they are doctrine gaps (DG rows) and the manual should mark them SCHEDULED; (b) leave as aspirational prose. | **(a)** — the manual should not assert as shipped what cannot be executed; that is the exact defect class OF-16 just closed. | surfaced in CC's OF-16 draft (open questions 4 and 5), carried into the desk draft's preserved body | **OPEN** |


| OF-21 | 2026-07-26 | **Should the map layer live in a SEPARATE FILE from the logical Manifold?** A `.cml` document today co-locates two layers: the LOGICAL declarations (what the Manifold is; what agents see over describe) and the MAP clauses (`= <column>`, `FROM <table> AS <agg>(<expr>)`, `VIA <table>(a,b)`, `REJECT …`) which are engine-visible and map-side only. | **Co-located, insulation enforced at the DESCRIBE BOUNDARY.** §2b / C-2: describe emits logical names only — no `realized_by`, no VIA bridge, no FROM table, no expression — and a standing insulation test asserts physical identifiers never cross describe or the wire. So the guarantee holds, but it is TEST-enforced at the boundary rather than STRUCTURAL at the document. | (a) split the map into its own file — insulation at the DOCUMENT boundary (Huayin's stated intent); (b) keep co-located and rely on the describe-boundary test. | **Desk will draft the fork document.** FOR (a): Manifold portability (one logical model, many maps — environments, warehouses, customers), structural rather than test-enforced insulation, and a strong design-partner story. AGAINST: locality (a level's binding no longer sits beside its declaration) and two-file sync. Rowed now so it is not lost. | external-AI probe (2026-07-26); the grammar-page proposal (workstream B); §2b / C-2 insulation + the standing insulation test | **OPEN** |

| OF-22 | 2026-07-26 | **A meta-refresh redirect stub returns HTTP 200, so crawlers can hold retired copy indefinitely.** Two of three external assistants quoted PURGED "metrics engine" positioning — traced to the retired `/launch` page. Nothing on the live site says it (verified; the byte-preserved archive sits unserved in `src/content`). | **Astro `output: 'static'` cannot emit 3xx**, so every configured redirect ships as a 200 stub with meta-refresh + canonical + noindex. Browsers and well-behaved crawlers follow it; the 200 status is what lets stale copy persist in an index or a model's training slice. | (a) real 308s via `vercel.json` edge redirects (AUTHORIZED 2026-07-26, blocked pending owner infra approval); (b) accept the stubs. | **(a).** This finding upgrades the 308 from a nice-to-have to a live misinformation vector: retired positioning is being repeated back to us by third-party assistants. | external-AI probe (2026-07-26); the blocked `vercel.json` PR | **OPEN** |
| OF-23 | 2026-07-26 | **DETERMINISTIC SERVING — two identical asks against identical data should produce identical bytes. They do not.** Found by the flap detector's first real run on `gen_transcript.py`. TWO defects, both in the SERVING path, not the recording path: **(a) ROW ORDER permutes** — the same seeded query returns its coordinates in a different order run to run (`cal.month 2024-09` first, then `2025-07`); **(b) 1-ULP FLOAT DRIFT reaches SERVED VALUES** — `130.30240066225167` vs `130.30240066225164` for the same coordinate, moving the column total. The recording pipeline merely made it VISIBLE. | Nothing. `gen_transcript.py` carries a ROWED exemption in `check_generator_determinism.py`, loud on every run, keyed to this row and failing if this row closes while the instability persists. | (a) canonical coordinate ordering at the WIRE's serialization boundary (likely cheap, likely core); (b) sort-before-aggregate, a declared output precision, or deterministic execution — a design fork needing a desk proposal. | **(a) now, (b) by proposal.** NOTE THE DOCTRINE BOUNDARY: 0.13.1's rule — *a value below the system's declared tolerance is noise, not a finding* — **explicitly does NOT cover (b)**. There is no declared tolerance on a SERVED MEASURE, so collapsing it would be laundering, not canonicalizing. Thread-pinning stays REJECTED as symptom suppression: it would make the RECORDING more deterministic than the ENGINE, which is a lie about the product. **This also touches the REPRODUCIBILITY STORY** — a reader regenerating exhibits meets 1-ULP mismatches against published full-precision floats, so the fix's design must answer for the papers' "regenerable by the reader" claim. | the flap detector, 2026-07-26 (deploys for #104/#105); **Open Planner beat 1 (F4)** — the `split` face reproduces the same class independently (1.4e-16 relative, one ULP, 2 of 12 categories, grand total stable) | **OPEN** — **and now load-bearing for the Open Planner.** Beat 1 records that BYTE-IDENTICAL CERTIFICATES and P-ECON's certified-plan cache ("which also yields deterministic serving") both INHERIT this row's requirement: a kernel that certifies over canonical bytes cannot be built on a serving path whose bytes move. F4 itself is correctly classified as NOISE per the 0.13.1 doctrine — reporting a 1-ULP difference as a wrong number would be false precision — so what this row inherits is the REPRODUCIBILITY consequence, not a correctness one. |
| OF-24 | 2026-07-27 | **The cache annotation wears a semantic name on the semantic channel.** Found by the Open Planner beat's P-BLIND probe (F5): on a FRESH store the first query returns `rollup_severity: none` with no disclosure; every identical ask after it returns `info` plus a **`freshness`** disclosure. Deterministic, reproducible across cold stores. The first asker receives LESS disclosure than the second for the same question on the same data. | **Truthful content, wrong channel and wrong name** (desk root-cause, 2026-07-27): the caveat's content is *"served from cache"* (`engine.py:131,488`), version-checked before serving — so EACH CALL'S DISCLOSURE IS TRUE and the values are identical. The defect is a **mislabeled, mischanneled annotation**: mechanical serving-provenance wearing the semantic name FRESHNESS on the semantic caveat channel. NOT launch-blocking — identical values, truthful content, immaterial grade. | (a) rename and rehome the cache annotation out of the semantic caveat channel; (b) suppress it at same-version; (c) leave it. | **(a).** And the row's DESIGN HALF FEEDS THE PROGRAM: the kernel's disclosure projection gains a **two-channel split** — *semantic* (call-invariant; **P-BLIND's true jurisdiction**) vs *mechanical* (legitimately variant, possibly not wire-worthy at same-version). P-BLIND as formalized forbids dependence on ATTEMPT COUNT; once the channels are split, the semantic channel can satisfy that literally while the mechanical channel is free to vary, because it was never a claim about meaning. | Open Planner beat 1, F5 (`specs/open_planner/BEAT_1_REPORT.md`, `fixtures/d5_p_blind.json`); `engine.py:131,488` | ~~**RULED (a) & LANDED 2026-08-31**: shipped in `columna-core` 0.18.0, wire contract `"3"` -> `"4"`. `Disclosure` now carries two channels. `caveats` is SEMANTIC — call-invariant, and the SOLE input to `outcome`, `rollup_severity` and materiality; `mechanical` is OBSERVATIONAL, carrying `"served from cache"` and nothing else today. Every severity and materiality property reads `caveats` and never `mechanical`, so P-BLIND's jurisdiction is satisfied STRUCTURALLY rather than by discipline — a standing test marks a mechanical caveat `critical` and asserts the frame severity stays `none`. The bump is deliberate: `freshness` MOVED off an existing field for an unchanged utterance, the same break-by-version case as WP-NAME-1. Two coupled repairs shipped with it (ledger P1-04, P1-05): warm TOUCH returned from its cache before coverage and the Φ_v dispositions were computed and so was quieter than cold, dropping a MATERIAL caveat; and the coverage shortfall was graded IMMATERIAL on a wire code whose MATERIAL slot was wired with no producer. Fixing the second without the first would have made the divergence outcome-visible — `disclose` cold, `serve` warm.~~ |
| OF-25 | 2026-07-29 | **Composite input anchor at the ask surface** (F1). An inline reduction's input anchor pins ONE level, not a product of levels: `avg(revenue @ {store*product*cal.month})` refuses at the parser (`planner.py:377`, *"single-level input anchors this build"*). Beat 1 attested that `ColumnEngine.reduce_series_to_anchor` executes composite input grain unmodified — F1 ran through it below the ask. So the restriction is a RECALL row at the ask surface, not a safety issue: an entire class of two-stage statistics is expressible in the engine but not askable from the grammar. | **Nothing.** The refusal ships. Beat 1 (F1) certifies the finding; the recall ledger on the homepage now carries `composite input anchor` (2026-07-29) between `face chains` and the fold, so the gap is public while WP-GRAIN-1 is in flight. | (a) lift the restriction — WP-GRAIN-1 proposal (`specs/wp_grain_1_composite_input_anchor_v0_1.md`) states the pin×output-anchor lattice laws (finer / coarser / same / orthogonal / face-crossing), their refusal codes, and the acceptance criterion (F1 transcript serves with disclosure); (b) leave as-is and carry the ledger row indefinitely. | **(a) as 0.13.4's headline** (Huayin, 2026-07-29). CLI renumbers. Wire contract unchanged (`contract_version` stays `"1"`); doctrine ships alongside the code — laws 1/2/3 in the proposal are the surface's owed refusals; law 4 generalizes the existing OF-2 immaterial provenance note. | Open Planner beat 1 (F1) — `specs/open_planner/BEAT_1_REPORT.md:73`, `attack_b.py:127`, `fixtures/attack_b_ir.json`; the proposal `specs/wp_grain_1_composite_input_anchor_v0_1.md` | ~~**RULED (a) & LANDED 2026-07-30**: WP-GRAIN-1 shipped in `columna-core` 0.13.4. The composite input anchor is a first-class pin; Law 1 mints `pin_coarser_than_output` (REFUSE), Law 2 mints `redundant_pin` (CLARIFY), Law 4 generalizes the OF-2 immaterial note (serve). The F1 transcript now SERVES and agrees with the below-surface IR to float precision (`attack_b.py`). The recall-ledger row `composite input anchor` was STRUCK the same PR, per the ledger's own rule (row down ⇔ code up). Wire contract unchanged (`contract_version` `"1"`). Rowed future finding: the composite-input × FACED-output combinatoric meets the G4 chain guard and refuses `chained_crossing` — not yet served.~~ |
| OF-26 | 2026-07-30 | **Composite pin × faced output — the chain-guard corner (WP-GRAIN-1 residue).** WP-GRAIN-1 shipped the composite input anchor (0.13.4) and struck the `composite input anchor` recall-ledger row — the headline capability serves. But one corner survives: a composite pin that includes a FACED output coordinate — `sum(revenue @ {product*category.touch}) AT {category.touch}` — resolves the inner at a base+faced composite grain, which the existing **G4 chain guard** refuses `chained_crossing`. A lawful shape we cannot yet DERIVE, given a NAMED refusal, never a silent number. Rowed out by the WP-GRAIN-1 scope table before the release; entered here (and as its own dated recall-ledger row `composite pin × faced output`) because a struck row must not silently swallow a surviving sub-gap. | **Nothing — refuses honestly.** The chain guard names it (`chained_crossing`); the plain faced output (`revenue AT {category.touch}`) serves unchanged; no silent number, no regression. | (a) license composite-input × faced-output resolution — new engine work (the crossing propagates to the pin; disclosure-stacking across a face at a base+faced grain is currently undesigned, the same G4 frontier that gates chained face crossings); (b) leave rowed — the corner stays a named refusal until a real case demands it. | **(b) for now** (Huayin, 2026-07-30, at the 0.13.4 gate): doctrine-landed / execution-deferred. Forcing new engine work into a green release to chase one acceptance line is the discipline we keep; the guard doing its job on a rowed-out corner IS the system working. Lift to (a) when a real case arrives. | WP-GRAIN-1 acceptance criterion 4 (Law 3) — `specs/wp_grain_1_composite_input_anchor_v0_1.md`; the G4 chain guard `engine.py` `_resolve_faced` (`chained_crossing`); `test_inline_reduction.py::test_law3_composite_faced_pin_refuses_at_the_chain_guard`; **beat-3 measurement** `specs/open_planner/map2/pilot_c3.py` | **OPEN** — deferred at the 0.13.4 gate; carries a recall-ledger row until derived. **MEASURED BOUNDARY (beat 3, 2026-08-01, ratifier word)**: the C3 CROSS-bearing pilot fixed the corner's edge *by execution* — **a single faced coordinate is the maximal expressible CROSS seam at v1**. Every richer shape refuses `chained_crossing`: a second anchor dimension beside a faced coord (`{category.touch, cal.month}`, `{category.touch, region}`) AND a composite input pin under a faced output (`sum(revenue @ {product*cal.month}) AT {category.touch}`) — all G4. So the vertical-seam pilot necessarily ran *at* this boundary (`revenue AT {category.touch}`: home CROSS + lowered substrate sum) and passed; a richer C3′ becomes expressible only when chained-crossing licensing ships (future WP — the beat-3 handoff wall applies, no improvised transport). The corner stays OPEN as a licensing gap, now with a measured edge. |
| OF-27 | 2026-07-30 | **Column identity elides the input anchor — the pin-eliding default (WP-NAME-1).** The §4 mechanical default names an unaliased single reducer `<reducer>_<measure>` and, in the manual's own words (`docs/frame_ql_manual_v1.md:149`), *"the input anchor does not affect the default name."* Per the Two Anchors law a pinned reduction's identity is (reducer, input anchor, output anchor); the default keeps two of the three and names half the denotation. WP-GRAIN-1 turns the elision from lossy to COLLIDING: the two F1 asks `avg(revenue @ {store*product*cal.month})` and `avg(revenue @ {customer*store*product*day})` both default to `avg_revenue` and the collision guard (correctly, never suffixing) refuses them in one frame — the guard catching the default's lie. | **Nothing yet — proposal filed** (`specs/wp_name_1_column_identity_v0_1.md`), queued behind 0.13.4. The default still ships; WP-GRAIN-1 landed without touching naming, so the collision guard is what currently stands between the default and a wrong label. | (a) retire the default: column identity = canonical expression \| AS-alias, computation provably unaffected (name is metadata), collision guard stands, `contract_version` bumps `"1"`→`"2"` (a changed default key for the same utterance); (b) keep the default and accept the elision + collisions; (c) a narrower fix that appends the pin to the default name (rejected in the filing — it re-introduces the suffix habit the guard forbids). | **(a)** — filed as WP-NAME-1 (2026-07-30). The bump is deliberate: it changes an existing wire field's value for an unchanged utterance, the canonical break-by-version case (contrast WP-GRAIN-1, which added reason codes with no bump). Acceptance = the wire-visible-blast-radius regeneration checklist green end to end, only the name changing. | the WP-GRAIN-1 collision surfaced at 0.13.4; the proposal `specs/wp_name_1_column_identity_v0_1.md`; the Two Anchors law `specs/reference/two_anchors_paper_v1_1.md`; `docs/frame_ql_manual_v1.md:149` | ~~**RULED (a) & LANDED 2026-07-30**: shipped in `columna-core` 0.14.0. The mechanical default is retired; an unaliased series is keyed by its CANONICAL EXPRESSION (`avg(revenue @ {day})`, `revenue`, `revenue.sum` — the dot-to-underscore mangle retired too). All three opens ruled: (1) leaf case uniform — no invented names anywhere, member access ships verbatim `revenue.sub`-style; (2) vehicle = its own minor 0.14.0 (a `contract_version` bump is what a pre-1.0 minor signals), server stays 0.8.2 (wire-schema text lives in core, re-exported); (3) migration note teaches the principle — key on AS aliases, author-owned, never changed by any future rule. `contract_version` `"1"`→`"2"`. Acceptance met: blast-radius regeneration green, only names changed, values byte-identical.~~ |
| OF-28 | 2026-08-23 | **Implementation vocabulary vs the ToD v6.1 terms.** ToD v6.1 §1.2 retires `member` from the core ontology — `measure family` is the family, `measure` is that family at one anchor (`F@A`) — and permits downstream implementations to retain v5 vocabulary during migration. Columna retains `measure`, `member`, `family`, `MeasureColumn`, `FamilyMember` across runtime, wire, and manual. What is unruled is whether that retention is permanent. | **Retention, unchanged.** Ratified by the v6 runtime checkpoint §11 ("No renaming. `MeasureColumn`, `FamilyMember`, `family`, `member` all stay exactly as they are"); the Frame-QL Manual states the seam in prose instead (Preface, *The Theory of Data*), which changes no token. | (a) rename the implementation vocabulary to the v6 terms; (b) an alias bridge, both vocabularies addressable; (c) deliberate permanent retention, the seam documented forever. | **Undecided — and it gates one thing: no public governed-publication authoring surface opens while the implementation vocabulary decision remains unresolved.** **UNIT D OPENED 2026-08-31** (`consolidated_ledger_v0_1.md`) — the v5→v6 crosswalk is exactly this decision, scoped as a document with no implementation authorized. This row is struck when the crosswalk is ruled, not when code moves.** An authoring surface mints governed objects under whichever vocabulary it exposes, and that choice is not reversible by documentation afterwards. Must not evaporate. | `docs/architecture/tod_v6_runtime_reconciliation.md` §§2, 10, 11 (ratified, merge `ffce9c1`, PR #175); *The Theory of Data* v6.1 §1.2 (the DOI pin lives in the Manual's Preface, not here — a fork ledger is not a publication authority); the Manual reconciliation design pass, 2026-08-23 | **OPEN** |
| OF-29 | 2026-08-26 | **The evaluation-spend guard in `run_eval.py`.** The governing rule (Huayin, 2026-08-26) is: registry/corpus/deposits/index changed -> deterministic verification only, zero model spend; agent-facing surface changed (prompt, retrieval behaviour, provider/model, review rubric, or anything else that can materially change generated or reviewed behaviour) -> evaluate once, affected cases only; nothing agent-facing changed -> no evaluation run. Today it is an instruction only, and instructions are the brittle joint — the harness itself has no idea whether the agent changed. | **Nothing shipped.** The rule is written into `services/ask/README.md` and governs by hand. | (a) `run_eval.py` refuses to run unless the agent-facing surface has changed since the last recorded run, with an explicit human override; (b) leave it as an instruction. | **(a), at the next legitimate touch of the eval harness — NOT as its own errand** (Huayin, 2026-08-26). Two riders from the ruling: the override must be EXPLICIT and human-authorised, and it must be VISIBLE IN THE EVALUATION RECORD rather than silent — a rerun that does not say it was a deliberate rerun is exactly the reflex the guard exists to stop. Design note: 'agent-facing surface' should be a recorded digest of the files that can change generated or reviewed behaviour, not a timestamp — a timestamp makes a whitespace edit look like an agent change. | Ask evaluation F (`specs/f_evaluation_report_v0_1.md`); the v1.1 reconciliation (`specs/certainty_v1_1_reconciliation_report_v0_1.md`, PR #232) | **OPEN — banked** |
| OF-30 | 2026-08-31 | **Query-level `count(*)` has no determinate analytical object.** A `UNIVERSE` declares coordinates, **not a fact table** — only a `MEASURE` carries `FROM <table>` — so a bare `count(*)` **as a series in `SELECT`** does not name what is being counted. Three readings are open and they are different numbers: (a) the **physical source-row count**; (b) the count of **existing analytical points**; (c) the count of **observations of some measure**. This is a real architectural fork, not documentation commentary: it decides whether Frame-QL has an implicit relation. | **Nothing shipped, and that is the choice.** The form does not parse into a served series; §4.2 and §6.2 are marked `[ROADMAP — the count(*) series only]` and the Manual states in prose that it does not choose among the three readings. Rowed here 2026-08-31 on Huayin's instruction, because until now the question lived **only** in the Manual with no ledger or fork entry — *"a real architectural fork, not merely documentation commentary"*. | (a) physical source rows; (b) existing analytical points (the universe's realized coordinates); (c) observations of a named measure — i.e. require `count(<measure>)` and refuse the bare form permanently; (d) admit it only where a `FROM`-bearing object is in scope. | **Do not resolve by inheritance.** SQL can answer `count(*)` because a SQL query always has a relation in hand; Frame-QL does not, and adopting the SQL reading would import an implicit analytical object the Manifold never declared — **a fact table by the back door**. Picking one silently is how a number acquires a meaning nobody declared. Note that **`AS count(*)` in a `.cml` MEASURE is a different and established case** and is unaffected: there the source table is declared on the measure. Resolving the query-level form is a language ruling, not a parser fix. | `docs/frame_ql_manual_v2.md` §4.2 / §6.2 (Second-Edition sync, 2026-08-31); *Measure Algebra Design Record v0.3* §11.1 (O6) | **OPEN** |
| OF-31 | 2026-08-31 | **The Manual still names the future multi-input surface "Column Algebra".** Design Record v0.3 **retires** that term — a column is a material carrier, not the governed analytical object — and adopts *Measure Algebra*. The Manual's §2.1 sync note calls the shape *"the leading candidate for the future **Column Algebra** surface"*, so a retired term survives in a shipped document. | **Left as-is, deliberately.** Huayin, 2026-08-31: the wording *"should eventually be reconciled, but I would not interrupt CC's current record-writing work merely to change the label."* No Manual edit was made. | (a) reconcile at the next legitimate touch of that section; (b) a dedicated wording pass; (c) leave until the surface is actually built, and rename with it. | **(a)** — it is a label, the claim under it is correct, and a standalone errand to change one noun is not worth a Manual revision. Fold it into whatever mission next touches §2.1. Note the scope is narrow: this is the *only* live use of the retired term in a shipped surface; the Mission 1 reconciliation and Design Records v0.1/v0.2 keep it as historical record by design. | *Measure Algebra Design Record v0.3* §1.2 statement 5; `docs/frame_ql_manual_v2.md` §2.1 sync note | **OPEN — banked** |


## Authorized work moved

The **authorized-work class** (ruled work tracked to verified completion) lives in
[`doctrine_gaps.md`](doctrine_gaps.md), not here — Huayin's consolidation ruling, 2026-07-25:
**no third ledger**. That file's remit, *"a ruled item leaving scope is a checkpoint event … never a
silent drop"*, is that class verbatim; minting a second home for it was how the fossil ruling
evaporated in the first place.

**This file keeps genuine undecided forks only** — code ahead of doctrine, awaiting a ruling.

## Log
- **OF-6 opened 2026-07-16** (CP-2 artifact 3). Draft persistence: the in-memory Draft needs a
  cross-session serialization once the A4 human turns span sessions — which the very next step (a real
  provider / interactive init) triggers. Opened now per Huayin: "the next step will want it" is a ledger
  row, not a prophecy.
- **OF-5 opened 2026-07-16** (CP-1 increment 6). The declared spine-grid (a level's domain source) is
  the single missing object behind both single-column events fill and the spine/product completeness
  oracle. Per Huayin: internal-contiguity is refutable from the data's own testimony in principle, but
  the connector domain-read (min/max/distinct on the ordered axis) it needs is exactly this grid, so
  the live CONTRADICTED channel rides here; absence is juxtaposition-scoped and BASIS mints UNTESTABLE
  meanwhile (serving always follows the declaration).
- **OF-4 opened 2026-07-16** (CP-1 §2c). The query-side ON-UNIVERSE mechanism (server `universe` arg,
  wire universe-apply, agent clarify-pick) is dormant after §2c retired its last emitter
  (`co_anchor_ambiguous`). Per Huayin's scope-split ruling, the core laws land now and the server-arg
  removal + agent pick-flow redesign are a pinned deferral. `test_clarify_relayed_not_auto_picked`
  asserts the load-bearing relay-and-never-auto-pick; the mechanical pick round-trip moves with this row.
- **OF-1, OF-2 opened 2026-07-14.** Transferred verbatim from PR #18's description into durable form,
  per Huayin's ruling (2026-07-14): "a merged PR's body is neither ledger nor queue… every fork
  surfaced in a PR gets a row [here] before the PR merges." Both were shipped in WP-B.1 (merge
  `a074319`) using the closest-fitting existing codes (no minting); the codes stand until Huayin rules.
- **OF-1 RULED (b) & CLOSED 2026-07-14** (Huayin). Minted reason `input_anchor_ambiguous`
  (CLARIFY/AMBIGUOUS), sibling to `co_anchor_ambiguous`; `ambiguous_grain` gloss left single-meaning.
  Standing rule recorded at `disclosure.py`'s `REASON_OUTCOME`: **one reason per contested dimension**.
  Landed with its test (`test_input_anchor_ambiguous_is_a_distinct_clarify_reason`).
- **OF-2 RULED (a) & CLOSED 2026-07-14** (Huayin). Immaterial `provenance` note ratified as shipped;
  no code change. Boundary recorded here and at the `_resolve_inline_reduction` docstring: material
  `input_anchor` is for imported/defaulted anchor choices; an explicit pin owes only the immaterial
  note, because the wire's reader may not be the asker.
- **OF-3 opened 2026-07-16** (CP-1, on-ramp/Explorer tier-2 WP, [PR #35](https://github.com/datumwise/columna/pull/35)).
  The ASSERT invariant-form ships its full data channel; the **row-form** is recorded UNTESTABLE (no
  base-row scan yet). Ledgered as a durable row per Huayin's rider (2026-07-16): "a later increment is
  where scoped items go to drift." Gates nothing; struck when the row-form's data channel is built or
  ruled unnecessary. Referenced at `adjudication.py::_prove_assert` (row branch).

- **OF-7 opened 2026-07-17** (CP-3, describe + Explorer). The Explorer ships as a portable component in
  `apps/website/` (the `/explorer` demo-manifold instance); the package-served deployment (columna-server
  offering it against a live manifold) is the recorded near-future path, a later WP. Gates nothing.
- **OF-8 opened 2026-07-17** (CP-3). An author-facing provenance surface (FROM/VIA) is a conceivable future
  Explorer layer whose data could never come from describe (the §2b insulation guarantee) — it would need
  its own governed source. Rowed, NOT designed (Huayin: 'row it, don't design it'). C-3 stays describe-only.
- **OF-9 opened 2026-07-17** (CP-3 C-2). Drop-the-qualifier ships as the insulation guarantee: no
  STRUCTURAL physical identifier crosses describe (no table names, no qualified table.column), while a
  bare predicate attribute name renders as authored. The full fix — declared logical names for predicate
  terms — is a definition-language extension (a new authoring surface, init implications), its own WP, not
  improvised before a freeze. The standing test asserts exactly the structural guarantee; it tightens to
  full verification when OF-9 lands. (Huayin: a test that asserts current behavior blesses current bugs —
  the no-physical test is standing and STRUCTURAL, which is why it caught the stores.opened_date leak.)
- **OF-10 opened 2026-07-17** (CP-3, S-1 superseded). The §2c definition-time-population mechanism
  lost its named customer (sell_through_rate killed) — rowed anyway; rows record designs, not sponsors.
- **OF-11 opened 2026-07-17** (CP-3b). The hosted access point: the demo Manifold as a live
  socket with an HTTP plug (direct FrameQL, path e) + an MCP plug (agents) on one API. Rowed,
  not built — post-launch WP; the wire is already the API contract, so the lift is transport + ops.
- **OF-12 opened 2026-07-17** (WP-FrameQL envelope, POST-FLIP beat — Huayin, at the 0.9.0 release-notes
  gate). A `frameql` **grammar-version field advertised in `describe`**, so any external agent can detect
  which grammar a server speaks (the terse fragment vs the 0.9.0 envelope). Additive, transition-friendly;
  its own beat. Explicitly does NOT reopen #49 (the surface-migration increment). The package semver + the
  dated `parse_frameql` tombstone already carry the break; this is the machine-readable advertisement for
  a heterogeneous fleet.

- **OF-13 opened 2026-07-18** (Cascadia case-demo recapture, POST-FLIP fork — Huayin). **Coordinate-value
  predicates in `WHERE`.** The recapture's manager transcript wanted `SELECT revenue, orders AT
  {cal.quarter} WHERE region = west` — slice to one region's value — and it does NOT resolve in this build
  (`unsupported` / BinderException; a query-level `WHERE` cannot filter on a dimension coordinate value,
  base OR rollup). Working construction today: anchor at `{region, cal.quarter}` and read the row (accepted
  for the transcript — honest, realistic agent behavior; ch3's prose shows only the NL answer, no edit).
  But "west only" is bread-and-butter day-one slicing a human WILL type — the case demo exposed a real
  expressiveness gap. Rowed as its own ruled increment, post-flip; not this WP.
  **EVIDENCE UPGRADED (2026-07-18, ch3 take-2):** the gap is not hypothetical — the LIVE query agent hit
  it TWICE in one recording (manager `WHERE region = 'west' AND cal.quarter = '2025-Q4'`; new-hire
  `WHERE cal.year = 2024`), both BinderException, both cascading to a suppressed "couldn't read" reply.
  The WHERE-a-coordinate instinct is UNIVERSAL — it is the SQL reflex; every MCP stranger's agent will
  reach for it. This is now the **leading candidate for the first post-launch language increment.** The
  interim measure is the agent-prompt law **SCOPE BY ANCHOR, NOT WHERE** (ratified 2026-07-18); **when
  OF-13 lands, that prompt law amends** (the anchor-and-read workaround retires as the language grows the
  native filter). Linkage recorded so the two move together.
  **EVIDENCE UPGRADED AGAIN (2026-07-18, ch3 take-3):** with the anchor-and-read law in place, the agent
  stopped failing — but the anchor-and-read serves the WHOLE frame (32 region×quarter rows); the answer
  (west/2025Q4) is present in it but frame-weighted, not isolated. So even the workaround does not yield
  a clean isolated answer. **OF-13 is the PRIMARY fix (language-first doctrine):** a native coordinate
  filter fixes EVERY client — including strangers' agents who will never read our prompt — and it is the
  only fix that yields a clean answer at the language layer. Confirmed the leading candidate for the
  first post-launch language increment. Post-flip.

- **OF-15 opened 2026-07-18** (Cascadia recapture take-3, SECONDARY fork to OF-13 — Huayin). **Agent
  read-then-summarize (a non-terminal `query`).** Today `query` is the agent loop's TERMINAL act: it
  serves the whole frame and ends the turn, so the agent cannot read a served result and report only the
  matching row(s) in prose. A non-terminal read-then-summarize step would let our agent isolate
  "west/2025Q4 = $31,468.78, 402 orders" from the served frame. This is SECONDARY to OF-13: it benefits
  OUR agent only (a stranger's agent gets nothing from it), whereas OF-13's native filter fixes every
  client at the language layer. Consider only if OF-13's design proves slow. Post-flip.

- **OF-14 opened 2026-07-18** (Cascadia recapture take-1, STANDING FACT — Huayin). **The demo has no
  clock.** The frozen-world demo warehouse (2024-2025) has no notion of "today", so relative-time
  phrases — "last quarter", "this year" — do not resolve; the assistant correctly ASKS rather than
  guesses (recorded in ch3 take-1: the manager's "last quarter" drew a clarify, now folded into the
  story as a two-turn exchange). This is a standing fact of the frozen world, NOT a bug. If a future
  increment ever wants relative-time resolution (a declared "as-of" anchor, a clock), it is a design
  fork — rowed here, not owed.

---

## 0.12 "the triad completes" — forks + rowed items (PR #83: 0.12-triad; MERGED + PUBLISHED 2026-07-24)

- **The five user-facing strings — RATIFIED, SEALED, WIRED BYTE-EXACT** (Huayin 2026-07-24, supersede
  all placeholders): the `primary` / `split` face descriptions (`manifold.cml` → menu + wire); the G4
  chain-guard message and the G5 anchor-law refusal (`engine.py`); the ledger re-sequencing note
  (below). No longer a fork — sealed.
- **ROWED (Huayin v0.4, non-blocking, no action this increment):** `last ORDER category` on the
  degenerate `category_profile` spine answers a coarser-than-base ask with a declared-but-arbitrary
  value (`priority` at the `all` grain = the last category's priority). Acceptable for v1 drivers;
  profile-spine measures eventually want a **base-grain-only family form**. Joins the ledger beside the
  crossed-population door.
- **Acyclicity DAG is VACUOUS in 0.12** (fork/observation): a lawful driver is a spine functionally
  servable at the frontier, so the face-driver graph is edgeless — a cycle is unexpressible until a
  driver can be a *crossed* measure (events-derived, 0.13+). The `_prove_faces_acyclic` machinery ships
  and runs (forward guard); the realizable failure this increment is the driver-must-be-a-spine check
  (an un-frozen events driver refuses — `test_adjudication_fails_on_an_unfrozen_events_driver`).
- **G5 SERVE-half deferred to 0.13** (ruled B, on the record, not drifted): distinct-rides-`.touch`
  (per-member sketch reduce + overlap disclosure) lands beside P1/alignment, where the anchor-exhaustion
  corollary (notes §6.3) is proven, not asserted. 0.12 ships the refuse-half only — the anchor law.
- **/case exhibit copy for E11/E12** comes to the desk POST-BUILD (addendum §8); the recapture captions
  are working placeholders, like E10's.
- **Ledger re-sequencing note — SEALED (public ledger, dated); byte-exact, single line:**
  "2026-07: the RELATE face triad (assign/alloc) completes ahead of OF-13 — shipped-surface coherence and the crossing menu's completion graded ahead; OF-13 remains the leading language increment thereafter, joined by multi-universe alignment (P1). The distinct-crossing serve-half was explicitly deferred to the alignment increment — ruled, not drifted."
  The public-website placement rides the publish deploy.
- **Version track — CONFIRMED (Huayin 2026-07-24):** core → 0.12.0, meta → 0.12.0, server → **0.7.0**
  (its own line; "across" = the release spans all three, the track precedent governs).

## 0.13 "the ASSERT retirement" — the public ledger row (ruling §6; MERGED + PUBLISHED 2026-07-26/27)

- **Ledger renumbering note — SEALED (public ledger, dated); byte-exact, single line:**
  "2026-07: 0.13.0 is the ASSERT retirement — ruled, not drifted: the admission test (everything a trial proves is a precondition of something served) removed the one construct that failed it, plus its cascade. Multi-universe alignment (P1), previously 0.13, renumbers to 0.14 unchanged in scope."
- **0.13.1 — the reconciliation delta, and the doctrine it carries.** *A value below the system's
  declared tolerance is noise, not a finding — reporting it as a finding is FALSE PRECISION*, which is
  a species of confident wrong number. The masthead does not say "no *large* wrong numbers." Within
  tolerance the wire now reports at the resolution its own tolerance warrants; outside tolerance a real
  shortfall keeps its exact value and sign, asserted by test so the guard can never launder a finding.
  Wire change NAMED, not silent; no `contract_version` bump.
- **PROVENANCE of the signed-zero row, kept in full because the ledger keeps honest histories:**
  flagged at the **#85 preview** → ordered into the **0.12.1 cargo** → **never landed** (ordered-but-
  unlanded, pre-heartbeat vintage) → resurfaced as a **flap** during the 0.13.0 confirmation re-record,
  ~20% of runs on an identical package and input → **misdiagnosed twice as a signed zero, once by the
  builder and once by the desk**, neither having looked at the number → **measured** (the raw value
  alternates between exactly `0.0` and ±2⁻³¹, decided by float summation order) → **fixed at the true
  cause**. The prescribed fix `x if x != 0 else 0.0` was implemented and *proven not to work* before the
  real one was written.
- **The epistemic record, both directions:** *readings do not verify each other — and a symptom named
  in a report is still a reading.* The desk ruled on a symptom name rather than a measured value. The
  desk is not exempt from the epistemics it enforces.
- **The structural guard** (`check_generator_determinism.py`): every committed-output generator runs
  twice and must be byte-identical, wired into the deploy. Verified in BOTH directions — provoked
  against the unpatched engine, where it fails closed naming the generator and the differing byte.
  A recorded exhibit changes only by re-recording; this enforces that it does not change by *itself*.

**CLOSED 2026-07-24 — Huayin's word arrived, four-in-one (the ch2 forward-reference sentence, the
Figure 1 caption ratification, the merge, the publish), executed publish-first:** columna-core 0.12.0 ·
columna-server 0.7.0 · columna 0.12.0 live on PyPI (OIDC Trusted Publisher + `assert_pypi_versions`
green; per-version endpoints 200); PR #83 merged to `main` (`f0db0e0`, merge-commit — `v0.12.0` tag in
history); Vercel prod deployed via the shipped-coherent wedge (installed 0.12 from PyPI, regenerated
every exhibit from the published package). Live-verified: Figure 1's interim two-universe filter +
`OMITTED UNIVERSE · INTERIM` ghost + `DISCLOSE · INTERIM` caption band, and the ch2 forward-reference
sentence on /case + llms-full. RED 1 (regen-check `_FINANCE_CML`, purged-EDGE fixture — fails
identically on main, untouched by this PR) holds as the dated post-flip micro-PR. **The 0.12 record is
closed.**

## 0.13.2 "the declared Python floor and ceiling" — the launch-eve packaging row (MERGED + PUBLISHED 2026-07-27)

- **The finding, and how close it came.** A Windows fresh-venv pass on launch eve found `pip install
  columna` on Python 3.14 **not failing but BUILDING** — a C++ source build of `datasketches`, which
  core hard-depends on for HLL. `requires-python` was `">=3.10"` on all three packages with **no upper
  bound**, so pip considered us a match, found no wheel, and fell through to a compiler. Checked
  against PyPI, the gap is wider than the report: datasketches 5.x publishes **zero cp314 wheels on
  any platform** (so the ceiling protects Linux and macOS too) and has **never** published a 32-bit
  Windows wheel at any version. Hence the ratified line: *"Requires Python 3.10–3.13, 64-bit."*
- **THE DOCTRINE:** *fail closed with a named reason beats rare success for whoever happens to own a
  compiler.* An unbounded `requires-python` is not permissiveness — it is an untested claim asserting
  support for every future Python, including ones that did not exist when the claim was written.
- **The second, unlooked-for defect — `demo --play` crashed on Windows.** Found by the new
  windows-latest CI leg **on its first run**, which is the entire argument for the leg. Piping or
  redirecting the demo died with `UnicodeEncodeError: 'charmap' codec can't encode` **on the opening
  line, before a single mood printed**. Python writes to a Windows *console* through the wide-char
  API, so an interactive run looks fine; the moment stdout is a pipe or a file it falls back to the
  locale encoding — cp1252 on default en-US Windows — and our output is legitimately non-ASCII (U+2500
  rules, em-dashes, wire JSON dumped `ensure_ascii=False` so non-ASCII labels serve as themselves).
  **THE FIX BELONGS AT THE STREAM, NOT IN THE TEXT.** Stripping the characters to ASCII would have
  made the demo lie about what the wire carries, and would have left the next non-ASCII value to crash
  somewhere quieter. `columna-server` now declares UTF-8 on stdout/stderr for every subcommand.
  Guarded twice: the Windows leg is the real proof, and `test_demo_play_survives_a_cp1252_stdio_locale`
  reproduces the exact failure on **any** platform via `PYTHONIOENCODING=cp1252` — verified by
  neutering the fix and watching it reproduce the identical Windows traceback on Linux. That test
  asserts the rules and em-dashes are still PRESENT, so it fails if anyone "fixes" this by deleting them.
- **The class guard.** `demo wheel install` now runs **windows-latest / py3.13** beside ubuntu /
  py3.10. The class is *a dependency with platform or version wheel gaps*; it was invisible to a
  Linux-only CI, which is how it survived three releases. Both legs run one assertion file
  (`scripts/assert_demo_play.py`) so they cannot drift into proving different things — and that file
  is ASCII-only on purpose: **a guard that can be broken by the condition it guards against is not a
  guard.** (Its first Windows run printed an em-dash only because cp1252 happens to hold one at 0x97;
  U+2500, four lines earlier in the product's own output, does not. That is exactly where the crash
  landed.)
- **THE WEDGE RACE — ROWED, then fixed by choreography, not code.** The deploy resolved **on attempt
  5 of 5**, the final attempt of its retry budget. It went green with no margin. The cause is ORDER,
  not budget: merging to `main` triggers the deploy while publish is triggered by the release cut that
  necessarily *follows* the merge, so the deploy always races the publish. **The fix is the flip
  choreography the house had already proved twice (0.12.0, 0.13.0): tag the release branch BEFORE
  merging — publish fires, the verbatim-pin gate clears, THEN merge, so the deploy finds packages
  already installable.** Recorded as the standing release order in `docs/RELEASE_ORDER.md`; zero code.
  Belt for a Tuesday emergency: the retry budget widened 5 → 8 (~560s), pre-freeze, one integer.
- **THE VANTAGE-POINT CLAUSE, RE-PROVED FROM THE OTHER DIRECTION.** At 0.13.1 a developer machine
  called the pin installable while the CI runner, on another CDN edge, could not resolve it. At 0.13.2
  the disagreement inverted: `/pypi/columna-core/json` reported 0.13.2 **absent** while `/simple/` —
  the index pip actually resolves from — was already serving it. A checker trusting the JSON would
  have declared a live release broken and rolled it back. So the clause is **symmetric**: the JSON API
  is not a slower mirror of the truth, it is a DIFFERENT VANTAGE POINT that can be stale either way.
  *Verify installability by installing*, with the resolver a consumer actually uses — never by reading
  a metadata endpoint that merely describes the package. A convenient observation is still an observation.
- **THE GUARD PATTERN — FOUR GUARDS, FOUR LIVE FINDINGS, NOT ONE EVER RAN CLEAN.**
  *(Ratified in this wording by Huayin, 2026-07-27, over the rounder "four first-run catches."*
  *Precision about our own claims is this house's brand applied to its own mythology: the round*
  *number would not have survived an auditor, and we are the auditor.)*

  The count was **checked, not assumed** — each guard's introducing commit was traced before the
  line was written, and the trace is kept here so the claim stays auditable:

  | guard | introduced | what it found, and when |
  |---|---|---|
  | `check_generator_determinism.py` (flap detector) | `7e9b613` (0.13.1) | caught `gen_transcript.py` flapping on a later run → **OF-23 rowed** (`95f5fb5`). A real catch after introduction. |
  | `latest.ts` fail-closed release rail | `4922fec` | landed **after** `v0.13.1`, and its own commit pre-seeded every entry through 0.13.1 — so **0.13.2 was the first version it had never seen, and it fired**, refusing the build until someone wrote what the release IS. Strict first-run catch. |
  | windows-latest CI leg | `8392372` (0.13.2) | **caught a real product crash on its first run** — the cp1252 `demo --play` death, fixed in `627d8b1`. Strict first-run catch. |
  | `check_purged_grammar.py` | `483fac1` (2026-07-25) | **a different shape, and the record says so**: born *from* a hand-found fossil sweep and born *carrying* a live ROWED exemption (OF-16). It never had a clean first run to catch anything on, because it was already holding a finding at birth. |

  **So: three strict first-run catches, and a fourth guard that arrived already flagging.** The
  pattern is not "guards catch things eventually." It is that **every guard this house has added
  found a live defect at or immediately after introduction — four for four, none ever clean.**
  That is the argument for adding the next guard *before* it is asked for. It is also the warning
  underneath it: **the defects were already there, and the only variable was whether anything was
  looking.** A guard is not what creates the finding; it is what ends the period of not knowing.

## Occurrence conformance — RULED (Huayin 2026-07-24; rides OF-5)

The three-universe Figure 1 (PR #84) draws two inter-universe edge classes from the DECLARATION
(describe): the shared-grain **"=" identity** edges (store, day, declared identical across transaction
and inventory) and the **product↔category frontier + faces**. Their *conformance* is one adjudication
class — **"occurrence conformance"**: frontier-side `bridge ⊆ members` and identity-seam-side
`occurrences ⊆ members` (per universe, per shared grain). It is **NOT in the shipped adjudication** and
is **blocked on OF-5's unbuilt domain-read** (min/max/distinct, membership); BASIS minting `UNTESTABLE`
is the correct interim truth. **Ruling: a dated micro-PR riding OF-5**, not add-now — it lands when the
domain source is declarable. The figure needs no engine change: it depicts declarations, not conformance.

## OF — `in_core` is overloaded (implementation debt, not semantic authority) — ROWED (Huayin 2026-09-01)

`Operator.in_core` carries at least two different facts under one flag, and reading it as a single
realization axis mismeasures.

* For `rolling_sum` / `rolling_mean` it means **the mechanics do not exist**: nothing executes, in any
  position, and the engine answers a governed `unsupported` [ROADMAP].
* For `mean` it means only that **Core does not serve the average as a declared MEASURE FAMILY
  MEMBER**. The inline form `mean(x @ {a})` executes today; the registry entry exists so
  `(operator × lineage)` law has an address, not to gate execution.

Found during the capability-authority reconciliation (2026-09-01): a first measurement that read the
flag alone reported `mean` as *lagging* a Core Profile it actually meets.

**Ruling: implementation debt, not semantic authority. Do not block Manual work on a refactor.**
`docs/tools/capability_authority.py` keeps conformance/profile measurement independent of the flag —
it disambiguates through `SERIES_REDUCERS`, the declared inline-execution vocabulary — and the
overload is rowed here for later cleanup. The flag must not become the authority for what a profile
or the language requires; that is what `specs/frameql_capabilities.toml` and `specs/profiles/` are
for.
