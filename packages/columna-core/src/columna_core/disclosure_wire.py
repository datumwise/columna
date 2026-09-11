"""
columna_core.disclosure_wire — the structured disclosure/outcome WIRE ADAPTER.

ADR-032 D8: one contract on every surface. This module is the single place that serializes the
engine's `Caveat`/`Outcome`/`FrameResult` values into the wire schema (WP-2.2 spec §"Wire
contract"). The MCP server (and any future surface) serialize through here, so the truth an agent
receives is identical to the Python API's. WP-1.3's disclosure adapter collapses into this module.

Design commitments (WP-2.2 ruling A2+):
  * FAITHFUL, never synthesizing. Alternatives on a no-result are re-encoded verbatim from the
    engine's `Outcome.alternatives`; this adapter never invents a resolution the engine did not
    offer. Where an alternative names a universe pin, we additionally derive a machine-usable
    `apply: {"universe": U}` beside the human `token`/`description` (a faithful re-encoding that
    aids mechanical substitution — ruling B), but we add no new alternatives.
  * The category -> (wire code, default materiality) mapping is NORMATIVE and lives here as one
    dict (`CATEGORY_TABLE`). Deviating from it requires sign-off (WP-2.2 invariant 3).
"""
from __future__ import annotations

import re
from typing import Optional

from .disclosure import Caveat, Outcome

# ── CONTRACT "4" -> "5" (2026-09-11, Frame-QL 1.0 expression language) ──────────────────────────
# The expression dialect moved off CPython's `ast` onto the adopted Frame-QL 1.0 grammar
# (specification §15), and with it the CANONICAL SPELLING of an expression. Default column keys are
# canonical expression text (WP-NAME-1), so the key of an unchanged utterance can move:
#
#     avg(revenue@order)        key was `avg(revenue@ {order})`   now `avg(revenue @ {order})`
#     avg( revenue @ {order} )  key was verbatim, spaces and all  now `avg(revenue @ {order})`
#     variance(price, ddof=1)   spelled `ddof=1` in canonical text  now `ddof: 1`  (§15.2: `=`
#                               compares, `:` names an argument; `=` remains compatibility INPUT)
#
# THIS IS A BUMP, NOT AN ADDITION, and for the same reason "1" -> "2" was: a changed default key for
# an unchanged utterance is a breaking wire change, because a name-keyed consumer reads a different
# key. The old canonicalizer was three regular expressions that normalized ANCHORS and left the rest
# of the expression as written (including its whitespace, and including a missing space it inserted
# itself); the canonical form is now the whole expression re-rendered by the grammar's own unparser,
# so it is one spelling rather than "whatever was typed, with the pins tidied".
#
# WHAT ELSE MOVES. An earlier draft of this note claimed that no value moved and that nothing stopped
# parsing. Both were false, and an adversarial review caught them; the corrected scope is below.
# A version is only useful if its scope is honest, and the corpus test that was cited as proof
# (`test_ast_fidelity_over_the_corpus`) is scoped to the expressions IN THIS REPOSITORY — which
# contain no `@` mixed with `*` or `/`, precisely the shape the precedence correction moves.
#
#   · VALUES MOVE where `@` meets arithmetic — and this is the correction, not a side effect. §15
#     puts anchor ascription ABOVE multiplicative, CPython's `MatMult` put it at the same rung:
#
#         SELECT revenue.sum + (revenue.sum / 2 @ {}) AS x AT {store*month}
#           was  672.5, 707.5, ...   read as (revenue/2) @ ()   — CPython's grouping
#           now  135.0, 187.5, ...   read as revenue / (2 @ {}) — §15's grouping
#
#     Both serve. There is no caveat, because on neither reading is anything undisclosed — the two
#     readings are different well-formed asks, and 1.0 says which one the text means. Parentheses
#     around the operand do NOT protect it: the regrouping happens inside them.
#   · MOOD MOVES for a reduction over that shape. `avg(revenue / 2 @ {order})` was a PINNED
#     reduction (the argument was one `@` node under CPython's flat precedence) and served; the
#     argument is now a division whose right operand is pinned, so the unpinned path takes over and
#     it refuses `input_anchor_unavailable`. The refusal is the conformant answer.
#   · A FEW UTTERANCES STOP PARSING — all of them Python-isms the retired substrate admitted only
#     because it WAS Python: `.5` without a leading digit (deliberate: `.` is member access),
#     `1_000` underscore separators, a trailing comma in an argument list, and `#` comments. Frame-QL
#     1.0 has no such forms. `.5` and `1_000` are plausible inside a `DERIVED` formula, so this is
#     worth knowing rather than worth burying.
#
# In the other direction the grammar genuinely IS wider: braces natively, comparisons, `IN`,
# `BETWEEN`, logical operators, subscription, colon-named arguments, and newlines inside an
# expression. `revenue[region = 'east']` now reaches a named refusal (`bracket_is_not_a_filter`,
# §7.5) instead of a raw CPython SyntaxError recommending Python's walrus operator.
#
# Durable advice, unchanged since "2": key on AS aliases. They are author-owned and no rule moves them.
#
# THREE CURRENCY STAMPS WENT STALE AT THIS BUMP AND HAVE SINCE BEEN SWEPT, by the documentation pass
# that owns those files — `docs/frame_ql_build_status.md`, `apps/website/src/content/llms_index.txt`,
# and the `askWire` copy in `apps/website/src/components/ExhibitB.astro`.
# `scripts/check_currency_stamps.py` is GREEN: 11 enrolled claims across 4 files. The staleness is
# recorded here rather than deleted, because a stale contract claim outliving a bump is the exact
# failure that guard was built for: `contract_version "1"` was live on /llms.txt through TWO bumps.
#
# ── CONTRACT "3" -> "4" (2026-08-31, OF-24 ruling (a)) ───────────────────────────────────────────
# The wire gains a second disclosure channel. `disclosures` stays the SEMANTIC channel — what is true
# of the answer, call-invariant, and the sole input to `outcome`, `rollup_severity` and materiality.
# The new `mechanical` array carries observational facts about the particular call, which today means
# exactly one thing: "served from cache".
#
# THIS IS A BUMP, NOT AN ADDITION, because `freshness` MOVED. The same utterance over the same data
# previously emitted `freshness` inside `disclosures` on a warm call and not on a cold one; it now
# never appears there. That is a changed value for an existing field on an unchanged utterance — the
# canonical break-by-version case, and the same reasoning that bumped "1" -> "2" for WP-NAME-1.
#
# WHY IT HAD TO MOVE: OF-24 found that on a fresh store the FIRST asker received less disclosure than
# the second for the same question on the same data. The content was true and the values identical;
# the defect was a mechanical fact wearing a semantic name on the semantic channel. Splitting the
# channels lets the semantic one be call-invariant by construction, and lets the mechanical one vary
# freely, because it was never a claim about meaning.
#
# `mechanical` is emitted on EVERY column and frame, empty when there is nothing to say, so a
# consumer never has to distinguish absence-of-facts from absence-of-support.
CONTRACT_VERSION = "5"
# ── VERSION HISTORY ─────────────────────────────────────────────────────────────────────────────────
# "4" → "5" (Frame-QL 1.0 expression language, 2026-09-11): the expression dialect moved to the
#   adopted Frame-QL 1.0 grammar (specification §15), parsed natively by `columna_core.expr` instead
#   of being hosted on CPython's `ast`, and DEFAULT COLUMN KEYS ARE NOW CANONICAL 1.0 TEXT FOR THE
#   SAME UTTERANCE. An unaliased series is still keyed by its canonical expression (WP-NAME-1, "1" →
#   "2"); what moved is which spelling "canonical" names. `avg(revenue@order)` keys
#   `avg(revenue @ {order})` where it keyed `avg(revenue@ {order})`; `avg( revenue @ {order} )` keys
#   the same thing where it used to carry its author's whitespace; a named analytical argument is
#   written `ddof: 1` where the canonical text said `ddof=1` (§15.2 — `=` compares, `:` names an
#   argument; the `=` spelling remains compatibility INPUT and canonicalizes to the colon form).
#   EXPLAIN's `desugared` and per-series `expr` move with the keys, since they are the same artifact.
#   No value, mood, disclosure, materiality or reason code changed. One reason code was MINTED on the
#   existing extensible channel — `bracket_is_not_a_filter` (§7.5: `revenue[region = 'east']`
#   subscribes by a Boolean and is not analytical filtering; the diagnostic points at WHERE/HAVING).
#   This bumps the contract for exactly the reason "1" → "2" did: a changed default key for an
#   unchanged utterance is a breaking wire change. See the note above `CONTRACT_VERSION`.
# "2" → "3" (S2.2b-2): list_manifolds catalog semantics changed. `manifolds[]` was a runtime-FOLDER
#   inventory (one row per loaded folder, each with name/description/n_measures/universes); it is now a
#   governed publication LINEAGE catalog — one row per governed `manifold_id` with `versions[]` +
#   `latest_version` (publication facts) and per-version `realizable` (an installation fact), PLUS
#   explicitly classified `legacy` / `authority_incomplete` compatibility runtimes (keyed by
#   `runtime_id`, the latter carrying `source_ref` + stable `conditions`). The row meaning and
#   cardinality changed and the per-realization fields were dropped — a breaking catalog-semantics
#   change, so the contract bumps. (NOT caused by b-1's additive resolved manifold_id/version fields —
#   those were compatible under "2".) `CONTRACT_VERSION` is global, so query/check/explain/describe now
#   report "3" too; no analytical behavior changed. See S2.2b-2.
# "1" → "2" (WP-NAME-1, 0.14.0, 2026-07-30): the default column KEY changed for the same utterance.
#   An unaliased series is now keyed by its CANONICAL EXPRESSION, not a mechanical default:
#   `avg_revenue` → `avg(revenue)`, `revenue_sum` → `revenue.sum`. No values, moods, disclosures, or
#   reason codes changed — only the `name` field of unaliased columns. This bumps the contract because
#   a changed default key for an unchanged utterance is a breaking wire change (a name-keyed consumer
#   reads a different key). Durable advice: key on AS aliases — author-owned, and never changed by any
#   future rule. See specs/wp_name_1_column_identity_v0_1.md.
# ── THE IN-TREE CONSUMER INVENTORY (Huayin, 2026-07-26) ────────────────────────────────────────────
# The removal policy for this contract rests on an in-tree-consumers premise: a field may be removed
# without a version bump while every consumer is inside this repo and moves with it. That premise
# requires the consumers to be ENUMERABLE — so they are enumerated here, and the next wire change gets
# a CHECKLIST instead of a grep.
#
# The enumeration must span LANGUAGES. The 0.13.0 ASSERT retirement removed `asserts` from describe and
# a Python-shaped sweep missed `apps/website/src/explorer/manifold-explorer.ts`, which declared the
# field on a TypeScript type and rendered a section from it; the site build caught it, the inventory
# did not. A TypeScript type declaration is a wire consumer.
#
# KNOWN IN-TREE DESCRIBE CONSUMERS (keep current):
#   · apps/website/src/explorer/manifold-explorer.ts   — the Explorer (TypeScript; types + sections)
#   · apps/website/scripts/gen_case.py                 — the /case trial table + seeds
#   · apps/website/scripts/gen_universe_visual.py      — Figure 1 (fails closed on untaught shapes)
#   · packages/columna-server/src/columna_server/agent/ — the demo agents
#   · packages/columna-server/src/columna_server/tools.py — describe itself (the producer)
#
# KNOWN IN-TREE list_manifolds CONSUMERS (added S2.2b-2; the v3 catalog is per-lineage, not per-folder):
#   · packages/columna-server/src/columna_server/agent/mcp_client.py — connect() picks a servable id
#     from governed `manifold_id` + compat `runtime_id` rows
#   · packages/columna-server/tests/test_mcp_server.py, test_demo.py — catalog-shape assertions
#
# KNOWN IN-TREE contract_version LITERAL CONSUMERS (any bump must sweep these):
#   · .github/workflows/ci.yml — the demo --play smoke, which greps for the literal string
#   · scripts/assert_demo_play.py — IMPORTS `CONTRACT_VERSION` and builds the stamp from it, so it
#     needs no edit. Listed anyway: knowing a consumer is self-updating is part of the sweep.
#   · packages/columna-core/tests/  — test_disclosure_wire.py, test_inline_reduction.py,
#     test_generated_family_law.py
#   · packages/columna-server/tests/ — test_mcp_server.py (5 sites), test_demo.py,
#     test_governed_catalog.py (module docstring + a dedicated assertion), test_describe_insulation.py
#   (apps/demo-endpoint-vercel/scripts/generate.py was the third entry of the original list; the
#    endpoint was RETIRED 2026-09-02 under P1-32 and the generator deleted with it. exhibit-b.ts
#    carries no contract literal — it was listed here as "the live-demo query endpoint gate" after
#    that path was already disabled.)
#   (GENERATED, never hand-edited — `apps/website/src/data/*.generated.json` carry the literal but
#    regenerate from the live wire; listed so a reader does not go looking for the edit.
#    `specs/open_planner/fixtures/*.json` are ARCHIVED wires at contract "1" and are historical
#    records; they are not swept, by the same rule that keeps tombstones.)
#
#   THE TEST LITERALS WERE NOT IN THIS LIST BEFORE THE "4" -> "5" BUMP, AND THEY ARE THIRTEEN.
#   The list named two consumers and one of them (assert_demo_play.py) does not need editing. A bump
#   that trusted it would have left the whole test suite red and the enumeration would have been
#   "corrected" by the failure rather than by the checklist — which is precisely what this section
#   exists to stop happening a second time. Added 2026-09-11.
# ───────────────────────────────────────────────────────────────────────────────────────────────────

# Materiality is a fixed vocabulary (structured_disclosure_capture.md: the load-bearing field).
MATERIAL = "material"
IMMATERIAL = "immaterial"

# Approximation is material only when the relative error is large enough to change a decision.
APPROX_MATERIALITY_THRESHOLD = 0.01


def _approx_materiality(rel_error: Optional[float]) -> str:
    return MATERIAL if (rel_error is not None and rel_error >= APPROX_MATERIALITY_THRESHOLD) else IMMATERIAL


# --- THE NORMATIVE TABLE (WP-2.2 spec) -------------------------------------------------------
# engine category -> (wire code, default materiality). One closed vocabulary, one dict.
# `approximation`'s materiality is rel_error-dependent, so its value is a callable(rel_error)->str.
CATEGORY_TABLE = {
    # ── TOMBSTONE (2026-08-20) ── RETAINED and still WIRED, but no longer PRODUCED: a blocked
    #   reduction refuses (reason `blocked_reduction`) instead of serving with this caveat. Kept so
    #   archived wires, recorded transcripts and the deposited manuals still resolve. See the matching
    #   tombstone on `disclosure.B_ANCHOR_CROSSING`.
    "b_anchor_crossing":      ("blocked_reduction",      MATERIAL),
    "data_gap":               ("incomplete_data",        MATERIAL),   # B3 spine/product gap — a RESERVED-slot fill (Q6)
    "zero_fill":              ("zero_filled",            MATERIAL),   # D4 (retired producer): events-basis 0-fill
    # Φ_v fill-rule dispositions (columna#143 step 3) — absence follows the declared member rule
    "declared_fill":          ("filled",                 IMMATERIAL), # declared `zero` — a correct nil, not fictitious
    "unknown_absence":        ("unknown",                MATERIAL),   # declared `unknown` — value existed, unrecorded
    "out_of_population":      ("out_of_population",       IMMATERIAL), # declared `undefined` — outside the population
    "undeclared_absence":     ("undeclared_absence",     MATERIAL),   # NO rule — engine discloses, does not fill
    "over_count":             ("multi_counted",          MATERIAL),   # touch-face M:N crossing: deliberate over-count -> DISCLOSE
    "shadow":                 ("memberships_unrepresented", MATERIAL), # assign-face: single-count drops the non-top memberships -> DISCLOSE
    "reconciliation":         ("reconciliation",         IMMATERIAL), # alloc-face: the commutation certificate (MATERIAL on shortfall — see wire_caveat)
    "coverage":               ("denominator_population", MATERIAL),
    "unconfirmed_assumption": ("input_anchor",           MATERIAL),
    "approximation":          ("approximation",          _approx_materiality),
    "freshness":              ("freshness",              IMMATERIAL),
    "transport":              ("provenance",             IMMATERIAL),   # faithful-step record
}

# Reserved codes for authoring-era disclosures — emit-capable now, produced later. Held so the wire
# vocabulary is closed and stable end to end (WP-2.2 spec; structured_disclosure_capture.md fork B).
#   · `incomplete_data` — the B3 spine/product-gap CAVEAT; wired when absence-semantics lands (a
#     CATEGORY_TABLE entry maps an engine gap category to it).
#   · `conflicting_data` — RETAINED, reserved and UNWIRED as a caveat code (Huayin, 2026-07-15): held
#     for a possible future soft-assert / disclosed-not-cut path, UNRULED and UNSCHEDULED. The B1 cut
#     is a REFUSE mood, not a caveat — its `conflicting_data` reason lives in disclosure.REASON_OUTCOME
#     (one concept, two channels). Reserving costs nothing; un-reserving is the irreversible act.
RESERVED_CODES = frozenset({
    "stock_reading", "distinct_grain", "weighting_grain", "extremum_grain",
    "incomplete_data", "conflicting_data", "other",
})

# An unknown engine category falls back to `other`/immaterial rather than crashing the surface.
_FALLBACK_CODE = "other"


def code_for(category: str) -> str:
    entry = CATEGORY_TABLE.get(category)
    return entry[0] if entry else _FALLBACK_CODE


def materiality_for(category: str, rel_error: Optional[float] = None) -> str:
    """The normative default materiality for a category (rel_error only used by `approximation`)."""
    entry = CATEGORY_TABLE.get(category)
    if entry is None:
        return IMMATERIAL
    rule = entry[1]
    return rule(rel_error) if callable(rule) else rule


def wire_caveat(c: Caveat) -> dict:
    """One engine `Caveat` -> the wire caveat (WP-2.2 spec §"Wire caveat")."""
    recon = dict(c.reconciliation) if c.reconciliation else None
    materiality = materiality_for(c.category, c.rel_error)
    # alloc's reconciliation is an immaterial certificate when it reconciles, MATERIAL on a shortfall
    # (a coverage gap): "disclosed, never silent" (addendum §5).
    if recon is not None and recon.get("status") == "shortfall":
        materiality = MATERIAL
    d = {
        "code": code_for(c.category),
        "materiality": materiality,
        "severity": c.severity,
        "category": c.category,          # engine category preserved alongside the wire code
        "detail": c.detail,
        "remedy": c.remedy,
        "source": c.source,
        "rel_error": c.rel_error,
    }
    # face-crossing structured payloads (additive; contract_version stays "1"):
    if c.shadow is not None:
        d["memberships_unrepresented"] = c.shadow      # assign shadow
    if recon is not None:
        d["reconciliation"] = recon                    # alloc badge {crossed_total, base_total, delta, tolerance, status}
    return d


# A universe pin named inside an alternative's prose, e.g. "... within universe 'transactions'" or
# "pin ON UNIVERSE 'store_days' (...)". Used only to DERIVE the machine-usable `apply` field.
_UNIVERSE_RE = re.compile(r"universe\s+'([^']+)'", re.IGNORECASE)


def _wire_alternative(text: str) -> dict:
    """Re-encode one engine alternative string faithfully as {token, description[, apply]}.

    `description` is the engine's prose verbatim. When the alternative names a universe pin, `token`
    is the substitutable `on_universe('U')` form and `apply` carries {"universe": U} so a caller can
    apply it mechanically (via the `query` tool's `universe` arg). Otherwise `token` echoes the
    engine's text unchanged and no `apply` is derived — we never invent a machine action the engine
    did not express.
    """
    m = _UNIVERSE_RE.search(text)
    if m:
        u = m.group(1)
        return {"token": f"on_universe('{u}')", "description": text, "apply": {"universe": u}}
    return {"token": text, "description": text}


def wire_outcome(o: Outcome) -> dict:
    """An engine `Outcome` (no-result value) -> the wire `no_result` object. `kind`/`discriminator`
    are the planner's classification; `alternatives` are re-encoded verbatim (never synthesized)."""
    oc = o.classified()
    return {
        "kind": oc.kind,
        "discriminator": oc.discriminator,
        "reason": oc.reason,
        "detail": oc.detail,
        "alternatives": [_wire_alternative(a) for a in oc.alternatives],
    }


def _values(frame, value_name: str):
    """Serialize a served column's frame. Scalar when it is a single bare value; otherwise a vector
    of {group-dims..., value} rows."""
    dims = [c for c in frame.columns if c != value_name]
    if not dims and frame.height == 1:
        return "value", frame[value_name][0]
    rows = []
    for r in frame.iter_rows(named=True):
        row = {d: r[d] for d in dims}
        row["value"] = r[value_name]
        rows.append(row)
    return "values", rows


def wire_column(cr) -> dict:
    """One `ColumnResult` -> a wire column object (served value/values, or a no_result)."""
    if cr.refusal is not None:
        oc = cr.refusal.classified()
        return {
            "name": cr.name,
            "status": oc.kind,                       # clarify | refuse | error
            "population": None,
            "disclosures": [],
            "mechanical": [],
            "no_result": wire_outcome(cr.refusal),
        }
    out = {"name": cr.name, "status": "served", "population": cr.disclosure.population,
           "disclosures": [wire_caveat(c) for c in cr.disclosure.caveats],
           # OF-24: the OBSERVATIONAL channel, emitted separately and always present (possibly empty)
           # so a consumer never has to distinguish "no mechanical facts" from "old wire".
           "mechanical": [wire_caveat(c) for c in cr.disclosure.mechanical]}
    if cr.frame is not None:
        kind, payload = _values(cr.frame, cr.name)
        out[kind] = payload
    return out


def _frame_only_caveats(fr) -> tuple:
    """Caveats on the frame-level disclosure that are not attributable to any single served column
    (e.g. the multi-universe `coverage` caveat). Surfaced under `frame.disclosures` so they are not
    lost — the per-column arrays only carry each column's own caveats."""
    col_keys = set()
    for c in fr.columns:
        if c.refusal is None:
            for cav in c.disclosure.caveats:
                col_keys.add((cav.category, cav.detail, cav.source))
    return tuple(cav for cav in fr.disclosure.caveats
                 if (cav.category, cav.detail, cav.source) not in col_keys)


def derive_outcome(fr, material_present: bool) -> str:
    """The wire outcome (WP-2.2 §"Outcome derivation"). A no-result mood dominates and is taken from
    the engine's rollup (refuse > clarify > error). Otherwise the frame is served, and MATERIALITY —
    not severity — decides serve vs disclose: `disclose` iff at least one disclosure (frame- or
    column-scoped) is `material`, else `serve`. One rule, applied on every surface."""
    base = fr.outcome
    if base in ("refuse", "clarify", "error"):
        return base
    return "disclose" if material_present else "serve"


def wire_frame(fr, universe: Optional[str] = None, executed: bool = True,
               fetches_delta: Optional[int] = None) -> dict:
    """A `FrameResult` -> the full wire contract (WP-2.2 spec §"Wire contract").

    `universe` is the population pin the caller supplied (the `query`/`explain` `universe` arg), echoed
    into `frame.universe`. `executed` is emitted on every frame — `true` for an executed run
    (`execute_frame_query`), `false` for a plan (`check_frame_query`/`explain`) — and `fetches_delta`,
    when supplied, is the backend fetch count the call cost (0 asserts the zero-fetch guarantee).
    """
    columns = [wire_column(c) for c in fr.columns]
    frame_disclosures = [wire_caveat(c) for c in _frame_only_caveats(fr)]
    material_present = (
        any(d["materiality"] == MATERIAL for d in frame_disclosures)
        or any(d["materiality"] == MATERIAL for col in columns for d in col["disclosures"])
    )
    out = {
        "contract_version": CONTRACT_VERSION,
        "outcome": derive_outcome(fr, material_present),
        "frame": {
            "anchor": list(fr.anchor),
            "universe": universe,
            "rollup_severity": fr.disclosure.severity,
            "disclosures": frame_disclosures,
            "mechanical": [wire_caveat(c) for c in fr.disclosure.mechanical],
        },
        "columns": columns,
    }
    out["executed"] = executed          # emitted on BOTH paths now: true for a run, false for a plan
    if fetches_delta is not None:
        out["fetches_delta"] = fetches_delta
    return out
