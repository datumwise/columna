"""columna_core.describe — the license/derived describe interface (WP-B B-5).

Defined in CORE, once: the serialization the Explorer tier-2 describe surface renders AND the future
Cacher consumes as its admission oracle are the SAME interface — a member's adjudicated License, read
off the manifold after publish. A member with `license=None` is unadjudicated (the manifold has not
been published); a denotation-only derived (empty family) carries no travel at all.
"""
from __future__ import annotations

from typing import Optional


def license_to_dict(lic) -> Optional[dict]:
    """A License → the wire/describe dict, or None when unadjudicated. `verdict` is the Certificate
    kernel's authority (verified | corroborated | untestable); `attestation` is the data watermark
    (present only for corroborated — the verdict re-adjudicates when it changes); `basis` states what
    proved/tested/asserted it; `lineages` are the fertile lineages the license opens."""
    if lic is None:
        return None
    return {
        "verdict": lic.verdict,
        "lineages": sorted(lic.lineages),
        "basis": lic.basis,
        "attestation": lic.attestation,
        "timeless": lic.attestation is None and lic.verdict == "verified",
    }


def describe_derived(m, name: str) -> dict:
    """Describe one NAMED derived metric: its formula, resolution anchor (if any), and each family
    member with its declared fertile lineages and adjudicated license. Denotation-only derived (no
    family) report `denotation_only: true` and no members — a bare formula, no travel."""
    d = m.derived[name]
    members = {
        member: {
            "declared_lineages": sorted(fm.declared_lineages),
            "license": license_to_dict(fm.license),
        }
        for member, fm in d.family.items()
    }
    return {
        "name": d.name,
        "formula": d.formula,
        "description": d.description,        # folklore (case-demo b) — LOGICAL, flows to describe/wire
        "resolution_anchor": d.resolution_anchor,
        "denotation_only": not d.family,
        "members": members,
    }


# ---- CP-3 C-1: the D1 describe extension (additive) ------------------------------------------------
# Additive to the shipped per-kind shape (capture §7 D1): License blocks verbatim across
# fertility/hierarchy/assert; basis + absence semantics on universes; operator properties. No alias block.
# The §2b insulation guarantee is C-2's wall (no physical identifier crosses describe) — these serializers
# carry only logical facts; a physical leak is a describe bug the standing test catches, never here.

_ABSENCE = {
    "events":   "absence is a lawful ZERO (zero-fill; immaterial)",
    "spine":    "absence is a GAP (incomplete_data — material)",
    "product":  "absence is a GAP (cartesian product; material)",
    "registry": "membership is a checkable fact (present vs absent)",
}


def absence_semantics(basis) -> str:
    """The absence meaning a BASIS fixes (B3). None = undeclared (the wiring is inert until declared)."""
    if basis is None:
        return "undeclared (absence-semantics inert until a basis is declared)"
    return _ABSENCE.get(basis, f"unknown basis '{basis}'")


def describe_universe(u, predicate_str) -> dict:
    """A Universe → describe dict: base dims, the LOGICALLY-rendered predicate (insulation — the caller
    renders it), basis type + its absence semantics (B3), and the basis License (describe/trust only —
    serving follows the DECLARATION regardless; the license records testedness)."""
    return {
        "name": u.name,
        "base_dimensions": sorted(u.base_dimensions),
        "predicate": predicate_str,
        "attributes": [a for a, _ in u.attributes],   # logical row-attribute NAMES only (case-demo c ext)
        "description": u.description,        # folklore (case-demo b) — LOGICAL, flows to describe/wire
        "basis": u.basis,
        "absence": absence_semantics(u.basis),
        "basis_license": license_to_dict(u.basis_license),
    }


def describe_assert(a, predicate_str=None) -> dict:
    """An Assert → describe dict with its adjudicated License (Certificate-kernel reuse, byte-identical).
    Row-form carries the LOGICALLY-rendered predicate (caller-supplied); invariant-form the measure
    relation. No physical identifier crosses (§2b)."""
    form = ({"kind": "row", "predicate": predicate_str} if a.kind == "row"
            else {"kind": "invariant", "anchor": list(a.anchor), "left": a.left, "op": a.op, "right": a.right})
    return {"name": a.name, "universe": a.universe, "form": form,
            "description": a.description,   # folklore (case-demo b) — LOGICAL, flows to describe/wire
            "license": license_to_dict(a.license)}


def describe_hierarchy(h) -> dict:
    """A Hierarchy → describe dict: lineage, the level chain, and its adjudicated License. The VIA table
    is a PHYSICAL identifier and does NOT cross describe (§2b) — provenance the wire never needs."""
    return {"lineage": h.lineage, "paths": [list(c) for c in h.paths],
            "chain": list(h.chain),        # `chain` = primary path (back-compat)
            "description": h.description,   # lineage folklore (case-demo b) — LOGICAL, flows to describe/wire
            "license": license_to_dict(h.license)}


def operator_properties(sig) -> Optional[dict]:
    """An OperatorSig → its describe properties (registry describe): the algebraic/routing properties the
    planner typechecks against — never the engine mechanics. None when the reducer is unknown."""
    if sig is None:
        return None
    return {"kind": sig.kind, "is_monoid": sig.is_monoid, "linear": sig.linear,
            "needs_order": sig.needs_order, "needs_window": sig.needs_window}
