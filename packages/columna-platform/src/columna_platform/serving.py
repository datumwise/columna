"""The successor execution path, end to end — and the exact line where it stops.

    lighthouse v2 publication
      -> parse_publication            governed artifact reader, unchanged
      -> resolve_all                  total Law(F)
      -> load_mapping                 the HAND-WRITTEN realization claim, read-only
      -> require_same_publication     binding, BEFORE anything else
      -> carrier                      synthetic, in memory, from no source
      -> admission.admit              two checks, both refusing
      -> RetainedState                analytical identity + standing
      -> decide                       serve / refuse
      -> [WIRE]                       *** NOT REACHED — see FINDING 1 below ***

FINDING 1 — THE WIRE IS UNREACHABLE INSIDE THE APPROVED BOUNDARY.

`disclosure_wire.wire_frame` takes a `FrameResult`. `FrameResult` and `ColumnResult` are defined in
`columna_core.planner`, and importing that module executes

    from .projection import PlannerView
    from .engine import ColumnEngine
    from .model import parse_faced, EdgeKey
    from .frameql import FrameQLSyntaxError
    from .expr import ...

— the whole legacy stack the boundary excludes. So "use the existing disclosure/wire" and "no legacy
planner / engine" cannot both be honoured: the wire contract's DATA TYPES are owned by the module
that also owns the legacy execution behaviour.

This is a RESPONSIBILITY defect, not a packaging inconvenience. `FrameResult`/`ColumnResult` carry no
planner logic — they are plain dataclasses — but they sit behind an import wall that makes the
disclosure surface reachable only through the engine. Any successor path must therefore either import
the excluded stack or restate the result types, and restating them would be a SECOND enumeration of
the wire contract, free to drift from the one CI checks.

Proof A does neither. It stops at `decide()` and reports. Re-implementing the wire here to make the
proof "complete" would have produced exactly the false agreement the candidate discipline forbids.

FINDING 2 — THE CLOSED REASON REGISTRY CANNOT EXPRESS A WANT-OF-STATE REFUSAL.

`disclosure.REASON_OUTCOME` is closed and fail-closed: `outcome_for` raises `UnregisteredReason`
rather than defaulting, by ruling. Of its 28 reasons, the four in the `realization` jurisdiction are
ALL `error`:

    chained_crossing, filter_unsupported, mixed_faced_anchor, unsupported   -> (error, None, realization)

There is no `refuse` reason in the realization jurisdiction at all — no way to say *the law licenses
this, the state is not here, and re-realization would resolve it*. The analytical `refuse` reasons
exist to their own planner intents (`input_anchor_unavailable` is the |R|=0 branch of the input-anchor
split; `anchor_spent` is the G5 frontier prohibition), and borrowing one would recreate precisely the
conflation the registry was repaired to end — the module's own note records `input_anchor_unavailable`
being split out of `blocked_reduction` because "one reason carried two analytical conditions and a
reader branching on it was told a lineage was blocked when none was".

Minting a reason is a ruling, not an implementation decision. Proof A therefore raises its own
un-collapsed refusals (`refusals.py`) and does not touch the registry.

CONSEQUENCE FOR THE SSE CONTRACT CANDIDATE: its `refuse` row requires a refusal to name want-of-law or
want-of-state, and requires a want-of-state refusal to carry that re-realization would resolve it.
The existing wire vocabulary cannot express that distinction. The candidate is not wrong; the
vocabulary is missing. Reported, not patched.
"""
from __future__ import annotations
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from columna_core.governed.publication import parse_publication
from columna_core.governed.resolve import (
    C3_DOMAIN_MOVEMENT, C7_SUFFICIENT_STATE, ESTABLISHED, resolve_all,
)
from columna_core.compiler.realization import load_mapping, require_same_publication

from . import admission
from .refusals import ProofRefusal, WantOfLaw, WantOfState
from .state import AnalyticalIdentity, RetainedState, RetainedStateStore, Standing


@dataclass(frozen=True)
class Served:
    """A served answer, with standing READ OFF the retained state rather than recomputed."""

    identity: AnalyticalIdentity
    standing: Standing
    governed_domain: str
    carrier_type: str
    row_count: int
    mood: str = "serve"


@dataclass(frozen=True)
class Refused:
    """A refusal as a VALUE — the condition, its jurisdiction, and its remedy if it has one."""

    condition: str
    jurisdiction: str
    detail: str
    remedy: Optional[str]
    mood: str = "refuse"

    @classmethod
    def of(cls, r: ProofRefusal) -> "Refused":
        return cls(condition=r.condition, jurisdiction=r.jurisdiction,
                   detail=str(r), remedy=r.remedy)


def open_publication(path):
    """Read the governed artifact and resolve every family's total law view."""
    pub = parse_publication(json.loads(Path(path).read_text(encoding="utf-8")))
    return pub, resolve_all(pub)


def bind(pub, mapping_path):
    """Load the hand-written claim and CHECK THE BINDING FIRST, before any other work."""
    mapping = load_mapping(mapping_path)
    require_same_publication(pub, mapping)     # InputIdentityMismatch if this is not its publication
    return mapping


def realize(mapping, family_id: str):
    """The one realization claim for a family; missing is a refusal, never a default."""
    hits = [r for r in mapping.families if r.family_id == family_id]
    if not hits:
        raise WantOfState(f"no realization claim for {family_id}", subject=family_id)
    if len(hits) > 1:
        raise WantOfState(f"{len(hits)} realization claims for {family_id}; exactly one is required",
                          subject=family_id)
    return hits[0]


def materialize(family, law_view, realization, carrier_obj, *, basis: str,
                constitution: Optional[str], constitution_scheme: Optional[str],
                currency: Optional[str], store: RetainedStateStore) -> RetainedState:
    """Admit a carrier and retain it with its standing.

    `basis` is a RUNTIME PROJECTION derived by the governed layer from C7 and passed in as EXECUTION
    INPUT. This function does not re-derive it — the SSE executes sufficient-state law, it does not
    rediscover why a state is sufficient."""
    admitted = admission.admit(law_view, realization, carrier_obj)
    st = RetainedState(
        identity=AnalyticalIdentity(family.family_id, family.constitutive_anchor),
        standing=Standing(
            constitution=constitution,
            constitution_scheme=constitution_scheme,
            participation=law_view["eligibility_and_participation"].value,
            basis=basis,
            realization=f"{realization.endpoint.connection}:{realization.endpoint.schema}."
                        f"{realization.endpoint.table}.{realization.endpoint.column}"
                        f"/{realization.grain}/{realization.exactness}",
            currency=currency,
        ),
        array=admitted.array,
        governed_domain=admitted.governed_domain,
        carrier_type=admitted.carrier_type,
    )
    return store.insert(st)


def decide(law_view, store: RetainedStateStore, identity: AnalyticalIdentity, *,
           at_anchor: Optional[str] = None):
    """serve | refuse — the decision, with the mood the wire WOULD carry if it were reachable.

    The order matters and is not incidental: LAW IS ASKED FIRST. A want-of-law must not be reported
    as a want-of-state merely because the state also happens to be absent, or an operator is sent to
    re-materialize against a question the law was never going to answer."""
    try:
        # ── law first ───────────────────────────────────────────────────────────────────────────
        if at_anchor is not None and at_anchor != identity.anchor:
            movement = law_view[C3_DOMAIN_MOVEMENT]
            if movement.standing != ESTABLISHED:
                raise WantOfLaw(
                    f"the ask moves from {identity.anchor!r} to {at_anchor!r} and governed movement "
                    f"is {movement.standing}; no re-realization can supply a licence",
                    subject=law_view.canonical_reference)

        c7 = law_view[C7_SUFFICIENT_STATE]
        if c7.standing != ESTABLISHED:
            raise WantOfLaw(f"sufficient-state basis is {c7.standing}",
                            subject=law_view.canonical_reference)

        # ── then state ──────────────────────────────────────────────────────────────────────────
        held = store.retrieve(identity)
        if not held:
            raise WantOfState(f"no retained state for {identity.family_id} @ {identity.anchor}",
                              subject=law_view.canonical_reference)
        if len(held) > 1:
            raise WantOfState(
                f"{len(held)} retained states of one identity in different standings; serving "
                f"requires one and MERGING THEM HERE IS NOT PERMITTED",
                subject=law_view.canonical_reference)

        st = held[0]
        if st.finalized:
            raise WantOfLaw("a finalized value is not sufficient state",
                            subject=law_view.canonical_reference)

        return Served(identity=st.identity, standing=st.standing,
                      governed_domain=st.governed_domain, carrier_type=st.carrier_type,
                      row_count=len(st.array))
    except ProofRefusal as r:
        return Refused.of(r)
