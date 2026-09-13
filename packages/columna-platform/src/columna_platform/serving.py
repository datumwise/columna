"""The successor execution path, end to end — and out through the REAL wire.

    lighthouse v2 publication
      -> parse_publication            governed artifact reader, unchanged
      -> resolve_all                  total Law(F)
      -> load_mapping                 the HAND-WRITTEN realization claim, read-only
      -> require_same_publication     binding, BEFORE anything else
      -> carrier                      synthetic, in memory, from no source
      -> admission.admit              two checks, both refusing
      -> RetainedState                analytical identity + standing
      -> decide                       serve / refuse
      -> disclosure_wire.wire_frame   THE REAL WIRE CONTRACT, contract_version "5"

FINDINGS 1 AND 2 ARE CLOSED (2026-09-12, ruled Huayin). Both were accidental seams, and both were
repaired at the seam rather than worked around here:

  1. `FrameResult`/`ColumnResult` MOVED to `columna_core.serving_contract`, an architecture-neutral
     module owned by no execution strategy. `planner` re-exports them, so every existing import keeps
     working and there is exactly ONE definition — no second enumeration of the wire's types.
     Platform still imports no planner/engine/model, and the import-graph test still says so.

  2. `want_of_law` and `want_of_state` MINTED in the closed reason registry. The table previously had
     no REFUSE in the `realization` jurisdiction at all, so a lawful request with no admissible state
     had to be reported as `error` — sending an operator to hunt a bug instead of re-materializing.

A RETRIEVAL MISS IS NOT A REFUSAL. `want_of_state` is not "evicted": where a re-materialization path
exists, an evicted state is re-established transparently and the request SERVES. Refusal is reserved
for the real condition — no currently admissible path or state can establish the target.

RESIDUAL SEAM, REPORTED NOT REPAIRED. `columna_core/__init__.py` imports `planner` (and thus the
execution stack) eagerly, so importing ANY `columna_core.X` submodule loads it at runtime. That is a
pre-existing property of the package's import surface, not something this path introduces, and making
the package lazy is a larger change to a public surface than this proof was authorized to make. The
architectural property that WAS asked for — the wire's types no longer belong to the planner — is
real and is asserted over the static import closure in `tests/test_proof_a_findings.py`.
"""
from __future__ import annotations
import json
import polars as pl
from pathlib import Path
from typing import Optional

from columna_core.governed.publication import parse_publication
from columna_core.governed.publication import ExplicitNone
from columna_core.governed.resolve import (
    C3_DOMAIN_MOVEMENT, C7_SUFFICIENT_STATE, ESTABLISHED, EXPLICIT_NONE, resolve_all,
)
from columna_core.compiler.realization import load_mapping, require_same_publication
from columna_core.disclosure import Disclosure, Outcome
from columna_core.disclosure_wire import wire_frame
from columna_core.serving_contract import ColumnResult, FrameResult

from . import admission
from . import composite as _composite
from .continuation import continue_to
from .movement import MovementLicence
from .refusals import ProofRefusal, WantOfLaw, WantOfState
from .state import AnalyticalIdentity, RetainedState, RetainedStateStore, Standing


# `Served`/`Refused` were Proof A's own answer shapes. They are GONE (2026-09-12): the wire
# contract is now reachable, and a local imitation of a wire answer beside the real one is
# exactly the second enumeration this amendment exists to avoid.

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


#: THE GOVERNING RULE, RECORDED VERBATIM (ruled Huayin, 2026-09-12). A constant, not a comment, for
#: the reason `EMPTY_FIBER_RULING` is one: it is the sentence that makes the guard below non-obvious,
#: and a reader deleting the guard should have to delete this too.
RESPONSIBILITY_STANDING_RULE = (
    "Standing of a responsibility does not imply establishment of every fact that may appear "
    "inside that responsibility."
)


def movement_licence(law_view):
    """The movement fact a C3 standing actually carries, or `None` where it carries none.

    WHY THIS IS NOT `C3.standing == ESTABLISHED`. C3 is `domain AND movement`, and `resolve` marks it
    ESTABLISHED when EITHER is declared:

        elif fam.domain is not None or fam.movement is not None:  ->  ESTABLISHED

    So a family that declares a DOMAIN and no movement resolves ESTABLISHED with
    `{'domain': ..., 'movement': None}`. Proof A's original guard tested the standing, and would
    therefore have served a coarser anchor for such a family with NO LICENCE AT ALL. The control
    passed only because the lighthouse fixture happens not to declare a domain — right by luck of the
    fixture rather than by construction, which is the kind of green that hides a hole.

    Same error class as the empty-fiber finding, one responsibility over: C9 ESTABLISHED did not mean
    absence was governed, and C3 ESTABLISHED does not mean a movement is licensed.

    THREE ANSWERS, KEPT APART:
      · a movement fact          -> returned; the caller may then check it licenses THIS movement
      · an explicit none         -> None; the family has DECLARED that nothing moves
      · absent / domain-only     -> None; nothing was established either way

    The last two both yield `None` because the caller's question is the same — *is there a positive
    licence?* — and the DETAIL of which it was belongs in the refusal text, not in control flow.

    This guard is deliberately narrow: it inspects C3's content for the successor serving path and
    does NOT redesign C3. Whether `resolve` should split domain from movement is a governed question
    and is left open."""
    c3 = law_view[C3_DOMAIN_MOVEMENT]
    if c3.standing == EXPLICIT_NONE:
        return None
    if c3.standing != ESTABLISHED or not isinstance(c3.value, dict):
        return None
    movement = c3.value.get("movement")
    if movement is None or isinstance(movement, ExplicitNone):
        return None
    return movement


def _no_licence_detail(law_view, source: str, target: str) -> str:
    """Say WHICH of the three no-licence cases this is. A refusal that cannot tell 'declared that
    nothing moves' from 'nobody said' is a refusal an operator cannot act on."""
    c3 = law_view[C3_DOMAIN_MOVEMENT]
    if c3.standing == EXPLICIT_NONE:
        why = "the family has DECLARED that no movement is licensed"
    elif c3.standing == ESTABLISHED:
        why = (f"C3 is established by its DOMAIN alone and carries no movement "
               f"(value={c3.value!r}) — standing of a responsibility is not establishment of every "
               f"fact inside it")
    else:
        why = f"governed movement is {c3.standing}"
    return (f"the ask moves from {source!r} to {target!r} and there is no positive movement "
            f"licence: {why}. Mechanical combinability is NOT analytical permission — the "
            f"operator's monoid property says these values CAN be folded, never that this family "
            f"MAY be moved. No re-realization can supply a licence")


#: reason tokens, minted 2026-09-12 in the closed registry. Named here once so a typo is an
#: ImportError rather than an `UnregisteredReason` at the wire.
WANT_OF_LAW = "want_of_law"
WANT_OF_STATE = "want_of_state"

#: The remedy a want-of-state refusal must carry. Rides `Outcome.alternatives`, which the wire
#: re-encodes VERBATIM and never synthesizes.
REMATERIALIZE = "re-realization / re-materialization may resolve this"


def _refusal_column(name: str, reason: str, detail: str, alternatives=()) -> ColumnResult:
    """A no-result column carrying a classified refusal — the shape the wire already understands."""
    return ColumnResult(
        name=name, expr=name, frame=None, disclosure=Disclosure.clean(),
        refusal=Outcome(reason=reason, detail=detail, measure=name, alternatives=tuple(alternatives)),
    )


def _served_column(name: str, st: RetainedState) -> ColumnResult:
    """A served column. The value crosses as the GOVERNED decimal, not as a float.

    `pl.from_arrow` is the same doorway Core's own connector uses; the point of admission having run
    first is that what reaches this line is already known to be faithfully carriable."""
    series = pl.from_arrow(st.array).alias(name)
    return ColumnResult(name=name, expr=name, frame=pl.DataFrame({name: series}),
                        disclosure=Disclosure.clean())


def _finalized_column(name: str, final) -> ColumnResult:
    """A served column carrying a FINALIZED value. It is served; it is not retained."""
    return ColumnResult(name=name, expr=name,
                        frame=pl.DataFrame({name: pl.Series([final.value])}),
                        disclosure=Disclosure.clean())


def decide(law_view, store: RetainedStateStore, identity: AnalyticalIdentity, *,
           at_anchor: Optional[str] = None, column: str = "revenue",
           licence: Optional[MovementLicence] = None) -> dict:
    """serve | refuse, rendered through the REAL wire contract.

    Returns the wire dict from `disclosure_wire.wire_frame` — not a Proof-A-shaped imitation of it.

    ORDER IS LOAD-BEARING: law is asked BEFORE state. A want-of-law reported as a want-of-state sends
    an operator to re-materialize against a question the law was never going to answer."""
    try:
        # ── law first ───────────────────────────────────────────────────────────────────────────
        moving = at_anchor is not None and at_anchor != identity.anchor
        if moving and licence is None:
            # No licence was carried into execution. Before refusing, the GOVERNED slot is consulted
            # — and it is read by CONTENT, not standing (see `movement_licence`). It carries no
            # movement shape today, so in practice this is the refusal path; the check is here so
            # that the day C3 does carry one, this is where it is honoured.
            if movement_licence(law_view) is None:
                raise WantOfLaw(_no_licence_detail(law_view, identity.anchor, at_anchor),
                                subject=law_view.canonical_reference)

        c7 = law_view[C7_SUFFICIENT_STATE]
        if c7.standing != ESTABLISHED:
            raise WantOfLaw(f"sufficient-state basis is {c7.standing}",
                            subject=law_view.canonical_reference)

        # ── then state ──────────────────────────────────────────────────────────────────────────
        held = store.retrieve(identity)
        if not held:
            # A MISS IS NOT A REFUSAL. Try to re-establish before deciding anything.
            established = store.establish(identity)
            if established is None:
                raise WantOfState(
                    f"no admissible state can establish {identity.family_id} @ {identity.anchor} in "
                    f"this execution, and no re-materialization path resolved one",
                    subject=law_view.canonical_reference)
            held = (established,)
        if len(held) > 1:
            raise WantOfState(
                f"{len(held)} retained states of one identity in different standings; serving "
                f"requires one and MERGING THEM HERE IS NOT PERMITTED",
                subject=law_view.canonical_reference)

        st = held[0]
        if st.finalized:
            raise WantOfLaw("a finalized value is not sufficient state",
                            subject=law_view.canonical_reference)

        if moving:
            # THE MOVEMENT. `continue_to` refuses before it folds — the values here are trivially
            # foldable, so asking the law first is the whole proposition.
            st = continue_to(law_view, st, licence, target_anchor=at_anchor)
            identity = st.identity

        if st.composite is not None:
            # PROOF C. The retained state is a matching (SUM, COUNT) basis; what is SERVED is the
            # finalized mean. `finalize` refuses on standing BEFORE it divides, so a corrupted basis
            # is caught by its standing rather than by its answer looking wrong.
            final = _composite.finalize(st.composite)
            col = _finalized_column(column, final)
            return wire_frame(FrameResult(col.frame, Disclosure.clean(), [col], (identity.anchor,)),
                              universe=None, executed=True)

        col = _served_column(column, st)
        return wire_frame(FrameResult(col.frame, Disclosure.clean(), [col], (identity.anchor,)),
                          universe=None, executed=True)

    except ProofRefusal as r:
        reason = WANT_OF_LAW if isinstance(r, WantOfLaw) else WANT_OF_STATE
        alts = (REMATERIALIZE,) if reason == WANT_OF_STATE else ()
        col = _refusal_column(column, reason, str(r), alts)
        return wire_frame(FrameResult(None, Disclosure.clean(), [col], (identity.anchor,)),
                          universe=None, executed=True)
