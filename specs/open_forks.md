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
