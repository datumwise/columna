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
        "resolution_anchor": d.resolution_anchor,
        "denotation_only": not d.family,
        "members": members,
    }
