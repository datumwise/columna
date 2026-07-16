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

## Log
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
