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

CONTRACT_VERSION = "1"

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
    "b_anchor_crossing":      ("blocked_reduction",      MATERIAL),
    "data_gap":               ("incomplete_data",        MATERIAL),   # B3 spine/product gap — a RESERVED-slot fill (Q6)
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
    return {
        "code": code_for(c.category),
        "materiality": materiality_for(c.category, c.rel_error),
        "severity": c.severity,
        "category": c.category,          # engine category preserved alongside the wire code
        "detail": c.detail,
        "remedy": c.remedy,
        "source": c.source,
        "rel_error": c.rel_error,
    }


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
            "no_result": wire_outcome(cr.refusal),
        }
    out = {"name": cr.name, "status": "served", "population": cr.disclosure.population,
           "disclosures": [wire_caveat(c) for c in cr.disclosure.caveats]}
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
    into `frame.universe`. `executed=False` (from `explain`) and `fetches_delta` annotate the
    zero-fetch guarantee for the EXPLAIN surface.
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
        },
        "columns": columns,
    }
    if not executed:
        out["executed"] = False
    if fetches_delta is not None:
        out["fetches_delta"] = fetches_delta
    return out
