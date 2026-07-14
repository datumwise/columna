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

## Log
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
  note, because the wire's reader may not be the asker. **No open forks remain.**
