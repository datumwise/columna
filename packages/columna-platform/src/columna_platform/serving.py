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
from columna_core.governed.publication import CONSTRUCTION, PRIMITIVE, ExplicitNone
from columna_core.governed.resolve import (
    C3_DOMAIN_MOVEMENT, C4_FORMATION, C7_SUFFICIENT_STATE, C8_CONTINUATION, ESTABLISHED,
    EXPLICIT_NONE, resolve_all,
)
from columna_core.compiler.realization import EXACT, load_mapping, require_same_publication
from columna_core.disclosure import Disclosure, Outcome
from columna_core.disclosure_wire import wire_frame
from columna_core.serving_contract import ColumnResult, FrameResult

from . import admission
from .anchors import declared_coordinate_types
from . import request as _request
from . import composite as _composite
from . import formation as _formation
from . import source as _source
from .continuation import continue_to
from .movement import MovementLicence
from .refusals import (ProofRefusal, RealizationContradictsLaw, UnsupportedByThisProfile,
                       WantOfCompatibility, WantOfLaw, WantOfState)
from .state import AnalyticalIdentity, RetainedState, RetainedStateStore, Standing


# `Served`/`Refused` were Proof A's own answer shapes. They are GONE (2026-09-12): the wire
# contract is now reachable, and a local imitation of a wire answer beside the real one is
# exactly the second enumeration this amendment exists to avoid.

def open_publication(path):
    """Read the governed artifact and resolve every family's total law view."""
    pub = parse_publication(json.loads(Path(path).read_text(encoding="utf-8")))
    return pub, resolve_all(pub)


def bind(pub, mapping_path):
    """Load the hand-written claim and CHECK THE BINDING FIRST, before any other work.

    TWO CHECKS, IN THIS ORDER, AND BOTH BEFORE ANY MATERIAL IS TOUCHED. The first asks whether this
    claim is about this publication at all; the second asks whether every family it names is one
    this publication declares. §4 of the realization freeze states the rule — "missing, duplicate and
    UNKNOWN all refuse" — and the successor path discharges it here for the same reason `compile_v2`
    discharges it in input authority: an unknown family is a claim about something that does not
    exist here, which is the binding question one level down."""
    mapping = load_mapping(mapping_path)
    require_same_publication(pub, mapping)     # InputIdentityMismatch if this is not its publication
    declared = {f.family_id for f in pub.families}
    for r in mapping.families:
        if r.family_id not in declared:
            raise WantOfState(
                f"the realization claims family {r.family_id!r}, which publication "
                f"{pub.ref.manifold_id}@{pub.ref.version} does not declare", subject=r.family_id)
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


def constitution_of(pub, family_id: str):
    """The family's governed constitution fingerprint and scheme, READ FROM THE PUBLICATION.

    IT WAS A HARD-CODED LITERAL UNTIL 2026-09-14, AND IT WAS THE WRONG FAMILY'S (OF-39). The proofs
    pinned `fcf-1:c176d2a4…` for revenue; that fingerprint is `count(revenue@sale_at)`'s. Revenue's
    own sat in the same artifact, read by nothing. It never failed a test because
    `Standing.comparable_to` carries the fingerprint SCHEME and not the FINGERPRINT — so the value
    was inert as well as wrong, which is why it survived three proofs.

    Absence is a refusal and never a `None` carried forward. A state that cannot say which
    constitution it was constituted under cannot later be invalidated when that constitution moves,
    which is the same argument `insert` already makes about realization standing."""
    ca = pub.constitution_authority.get(family_id)
    if ca is None:
        raise WantOfLaw(
            f"the publication establishes no constitution authority for {family_id}; there is no "
            f"governed fingerprint to constitute material state under", subject=family_id)
    return ca.constitution_fingerprint, ca.fingerprint_scheme


def require_exact_realization(law_view, realization):
    """The realization's EXACTNESS claim, checked BEFORE any material is read.

    THE FREEZE REQUIRES IT ON EVERY PATH A PROFILE LOWERS (§8, ratified), and this is a path. It is
    checked here rather than at admission on purpose: admission inspects the CARRIER, and this is a
    statement about the CLAIM. The SSE contract draws the same line for realization currency — a
    claim about the source is not answered by looking at the bytes that arrived.

    An approximate claim is a want of STATE, not of law: the governed family is exact and stays
    exact, and what is unavailable is an exact realization of it. Re-realization is the remedy, which
    is precisely what `want_of_state` carries."""
    if realization.exactness != EXACT:
        raise WantOfState(
            f"the realization claims {realization.exactness!r} delivery for a family whose governed "
            f"value domain is exact; this profile serves exact material only, and an undisclosed "
            f"approximation is what the governed contract forbids",
            subject=law_view.canonical_reference)


def require_continuation_conformance(law_view, realization):
    """The realization's CONTINUATION CLAIM against the family's governed C8. All seven cells.

    A GATE, NOT A DISCLOSURE (ruled Huayin, 2026-09-14): if the claim disagrees with governed C8,
    THE MATERIAL PATH DOES NOT PROCEED. A served number carrying a disclosure that its continuation
    claim was wrong is still a served number, and the disclosure channel is not where a conformance
    failure belongs.

    CHECKED HERE, BESIDE `require_exact_realization`, AND NOT AT ADMISSION — for exactly the reason
    that one is: admission inspects the CARRIER, and this is a statement about the CLAIM.
    Conformance is knowable from law and claim alone, so it is answerable before a single row is
    read, and the ordering principle `admit_anchored` states says it therefore must be.

        C8 ESTABLISHED = X   claim X        -> conforming
        C8 ESTABLISHED = X   null / absent  -> WantOfState (the realization is incomplete)
        C8 ESTABLISHED = X   claim Y != X   -> RealizationContradictsLaw
        C8 EXPLICIT_NONE     null / absent  -> conforming
        C8 EXPLICIT_NONE     any operator   -> RealizationContradictsLaw
        C8 UNESTABLISHED     null / absent  -> conforming (no assertion is made)
        C8 UNESTABLISHED     any operator   -> WantOfLaw (no governed meaning to realize)

    THE JURISDICTIONS DIFFER FROM K0v2's ON PURPOSE, AND THE MATRIX DOES NOT. K0v2 raises compiler
    conditions — `MappingIncomplete`, `MappingContradictsLaw`, `LogicalMeaningMissing` — because it
    is lowering; this path raises execution conditions, because it is executing. The row that
    decides is the same row in both profiles, which is the point (OF-47 was opened because one
    profile checked the field and the other did not read it at all). Stated separately rather than
    imported from `compile_v2`: the two profiles have different execution grammars, and a shared
    table would tie their envelopes together silently.

    An ABSENT claim under an ESTABLISHED law is a want of STATE, not of law: the governed family has
    its continuation and what is unavailable is a realization that says how it is delivered —
    re-realization is the remedy, which is what `want_of_state` carries. An ASSERTED claim under an
    UNESTABLISHED law is a want of LAW: there is no governed continuation to realize, and no amount
    of re-realizing supplies one. A CONTRADICTION is neither; see `RealizationContradictsLaw`."""
    cont = law_view[C8_CONTINUATION]
    claimed = realization.continuation_operator
    ref = law_view.canonical_reference
    if cont.standing == ESTABLISHED:
        governed = getattr(cont.value, "name", cont.value)
        if claimed is None:
            raise WantOfState(
                f"the continuation law {governed} is established for {ref} and the realization "
                f"makes no continuation claim; a realization null asserts nothing, and is not a "
                f"claim that the governed continuation is none", subject=ref)
        if claimed.upper() != str(governed).upper():
            raise RealizationContradictsLaw(
                f"{ref} is governed by continuation law {governed}; the realization claims "
                f"{claimed!r}. The realization does not get to choose the law it implements",
                subject=ref)
        return
    if cont.standing == EXPLICIT_NONE:
        if claimed is not None:
            raise RealizationContradictsLaw(
                f"{ref} positively establishes that it has NO continuation; the realization claims "
                f"{claimed!r}. That is not a gap the realization may fill — it is a governed fact "
                f"the realization contradicts", subject=ref)
        return
    if claimed is not None:
        raise WantOfLaw(
            f"the realization claims continuation operator {claimed!r} for {ref}, whose "
            f"continuation is {cont.standing}. There is no governed continuation here to realize, "
            f"and a realization may not manufacture one", subject=ref)


#: THE ADMISSION VIEW: `name -> governed type`. Admission asks a LOOKUP question about a coordinate
#: it already holds from the carrier — "what is this governed as?" — so a mapping is the right shape
#: where movement's ordered tuple is the right shape there.
#:
#: DERIVED, NOT RE-PARSED (2026-09-14). This was one of three parsers of the same `anchor`
#: declaration, and the most permissive: a missing or non-list `components` returned `{}` silently
#: where movement's parser refused. The type it returns was itself only added on 2026-09-14 (OF-48);
#: the malformation policy behind it now comes from `anchors`, which judges it once for everyone.
declared_components = declared_coordinate_types


def component_realizations(mapping, anchor: str) -> dict:
    """governed component name -> its realization, for one anchor. Missing is a refusal."""
    out = {}
    for r in mapping.anchor_components:
        if r.anchor_ref != anchor:
            continue
        if r.component_name in out:
            raise WantOfState(
                f"two realizations for anchor component {anchor}.{r.component_name}",
                subject=anchor)
        out[r.component_name] = r
    return out


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


def materialize_anchored(pub, family, law_view, realization, anchored, *, basis: str,
                        store: RetainedStateStore) -> RetainedState:
    """Admit an ANCHORED carrier and retain it with its standing and its coordinates.

    `currency` IS NOT A PARAMETER, AND THAT IS THE POINT. Realization currency — whether the claim is
    still true of the source — is one of the three jurisdictions the ratified freeze deliberately
    leaves open, and the SSE contract forbids absorbing it into admission, "which checks the carrier,
    not the claim". So the standing records `None`, which CLOSES REUSE and never reads as fresh
    (`state.py`). For a request-local execution that combines nothing, that costs exactly nothing and
    claims exactly nothing — which is the honest discharge of an open jurisdiction rather than a
    waiver of it.

    The constitution is READ FROM THE PUBLICATION, not passed in. A caller that could supply a
    fingerprint could supply the wrong one, which is what happened for three proofs (OF-39)."""
    fingerprint, scheme = constitution_of(pub, family.family_id)
    admitted = admission.admit_anchored(law_view, realization, anchored,
                                        declared_components(pub, family.constitutive_anchor))
    st = RetainedState(
        identity=AnalyticalIdentity(family.family_id, family.constitutive_anchor),
        standing=Standing(
            constitution=fingerprint,
            constitution_scheme=scheme,
            participation=law_view["eligibility_and_participation"].value,
            basis=basis,
            realization=f"{realization.endpoint.connection}:{realization.endpoint.schema}."
                        f"{realization.endpoint.table}.{realization.endpoint.column}"
                        f"/{realization.grain}/{realization.exactness}",
            currency=None,
        ),
        array=admitted.array,
        governed_domain=admitted.governed_domain,
        carrier_type=admitted.carrier_type,
        table=anchored.table,
        anchor_columns=anchored.anchor_columns,
    )
    return store.insert(st)


def operand_family(pub, family):
    """The single operand a constructed family is formed over. One, and refuses otherwise.

    The lineage lives in `formation.operands` (§3.7) and is the governed fact that says WHICH
    family's contributions are folded. It is read, never inferred from the canonical reference —
    `min(revenue@sale_at)` is a NAME, and a profile that parsed it would be resolving meaning from
    spelling, which is the whole thing `request.py` refuses to do at the other end of the path."""
    operands = tuple(family.formation.operands or ())
    if len(operands) != 1:
        raise UnsupportedByThisProfile(
            f"{family.canonical_reference} is formed over {len(operands)} operands; this profile "
            f"forms over exactly one")
    by_id = {f.family_id: f for f in pub.families}
    operand = by_id.get(operands[0])
    if operand is None:
        raise WantOfLaw(
            f"{family.canonical_reference} cites operand {operands[0]!r}, which the publication does "
            f"not declare", subject=family.family_id)
    return operand


def materialize_constructed(pub, family, law_view, operand, operand_view, realization,
                            operand_realization, anchored, *, basis: str,
                            store: RetainedStateStore) -> RetainedState:
    """Admit the OPERAND's material, form the constructed value from it, retain under the CONSTRUCTED
    identity.

    THE ADMISSION IS THE OPERAND'S, AND THAT IS NOT A SHORTCUT. What was delivered is revenue's
    material; what admission asks is whether that material is faithfully the operand's governed
    domain. The constructed family's value is not admitted because it was not delivered — it comes
    into existence here, after admission, from material already known to be governed. Admitting it
    would mean checking a carrier that does not exist.

    So the primitive-only guard in `admit_anchored` is untouched and is still right: this path never
    asks admission about a construction. It asks about the operand, and the operand is primitive."""
    admitted = admission.admit_anchored(
        operand_view, operand_realization, anchored,
        declared_components(pub, operand.constitutive_anchor))

    law = _formation.formation_law(law_view[C4_FORMATION].value, family.canonical_reference)
    # ORDER: the LAW's composition before the PROFILE's operator map. Both refuse as capability
    # limits, and the first is the durable reason — "COUNT declares no composition over operand
    # values" is true of every composing profile, while "not in this build's law map" is contingent
    # on this build. An operator told the contingent reason would reasonably wait for a release.
    fold = _formation.composition_for(law, family.canonical_reference)
    _formation.check_operator_claim(realization, law, family.canonical_reference)
    formed = _formation.form(anchored, law, fold)

    fingerprint, scheme = constitution_of(pub, family.family_id)
    st = RetainedState(
        identity=AnalyticalIdentity(family.family_id, family.constitutive_anchor),
        standing=Standing(
            constitution=fingerprint,
            constitution_scheme=scheme,
            participation=law_view["eligibility_and_participation"].value,
            basis=basis,
            realization=f"{realization.endpoint.connection}:{realization.endpoint.schema}."
                        f"{realization.endpoint.table}.{realization.endpoint.column}"
                        f"/{realization.grain}/{realization.exactness}"
                        f"/{law.name}({operand.canonical_reference})",
            currency=None,
        ),
        array=formed.table.column(formed.value_column).combine_chunks(),
        governed_domain=admitted.governed_domain,
        carrier_type=admitted.carrier_type,
        table=formed.table,
        anchor_columns=formed.anchor_columns,
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


#: reason tokens from the closed registry (`want_of_law`/`want_of_state` minted 2026-09-12;
#: `want_of_compatibility` and `realization_contradicts_law` 2026-09-14). Named here once so a typo
#: is an ImportError rather than an `UnregisteredReason` at the wire.
WANT_OF_LAW = "want_of_law"
WANT_OF_STATE = "want_of_state"
WANT_OF_COMPATIBILITY = "want_of_compatibility"
REALIZATION_CONTRADICTS_LAW = "realization_contradicts_law"

#: The remedy a want-of-state refusal must carry. Rides `Outcome.alternatives`, which the wire
#: re-encodes VERBATIM and never synthesizes.
REMATERIALIZE = "re-realization / re-materialization may resolve this"

#: ── THE CLOSED DISPATCH ─────────────────────────────────────────────────────────────────────────
#:
#: refusal class -> (wire reason, alternatives). NO FALLBACK, BY RULING (Huayin, 2026-09-14).
#:
#: WHAT THIS REPLACES, AND WHY IT WAS A DEFECT. Three sites read
#:
#:     reason = WANT_OF_LAW if isinstance(r, WantOfLaw) else WANT_OF_STATE
#:     alts   = (REMATERIALIZE,) if reason == WANT_OF_STATE else ()
#:
#: — a two-way `if/else` over a growing taxonomy, whose `else` was TOTAL. Measured before the
#: repair (`docs/architecture/cap_v1_evidence/run_refusal_dispatch.txt`): `WantOfCompatibility`
#: reached the wire as `want_of_state` WITH `REMATERIALIZE` OFFERED, against its own docstring's
#: warning, and any contradiction class dropped in would have done the same. The internal taxonomy
#: was honest and the public one was not, which is the worse half of the two.
#:
#: THE MAPPING DETERMINES `alternatives` AS WELL AS THE REASON. Deriving the remedy from the reason
#: — `(REMATERIALIZE,) if reason == WANT_OF_STATE` — is how a remedy gets attached to a condition
#: that never asked for one; here each row states its own, and a row with no lawful remedy states
#: the empty tuple rather than borrowing a misleading one.
_REFUSAL_WIRE = {
    WantOfLaw:            (WANT_OF_LAW,           ()),
    WantOfState:          (WANT_OF_STATE,         (REMATERIALIZE,)),
    WantOfCompatibility:  (WANT_OF_COMPATIBILITY, ()),
}


def _classify(r: ProofRefusal):
    """`ProofRefusal` -> `(reason, alternatives)`, by EXACT CLASS. Fail-closed.

    EXACT CLASS, NOT `isinstance`, AND THAT IS THE GUARD. An `isinstance` walk would silently give a
    future subclass its parent's reason — the same shape of failure as the `else` this replaces, one
    level down. A class with no entry raises, and the completeness control asserts none exists."""
    try:
        return _REFUSAL_WIRE[type(r)]
    except KeyError:                                    # pragma: no cover - the guard, pinned by test
        raise AssertionError(
            f"{type(r).__name__} has no wire classification. Every concrete ProofRefusal subclass "
            f"must have an entry in _REFUSAL_WIRE; there is deliberately no fallback, because a "
            f"fallback is how {WantOfCompatibility.__name__} came to travel as {WANT_OF_STATE!r}."
        ) from None


def _refusal_column(name: str, reason: str, detail: str, alternatives=()) -> ColumnResult:
    """A no-result column carrying a classified refusal — the shape the wire already understands."""
    return ColumnResult(
        name=name, expr=name, frame=None, disclosure=Disclosure.clean(),
        refusal=Outcome(reason=reason, detail=detail, measure=name, alternatives=tuple(alternatives)),
    )


def _served_column(name: str, st: RetainedState) -> ColumnResult:
    """A served column. The value crosses as the GOVERNED decimal, not as a float.

    `pl.from_arrow` is the same doorway Core's own connector uses; the point of admission having run
    first is that what reaches this line is already known to be faithfully carriable.

    THE ANCHOR COORDINATES CROSS WITH IT, WHERE THE STATE HAS THEM (2026-09-14). A retained state at
    `sale_at{store*day}` holds four values at four analytical points, and serving them as four bare
    numbers loses which point each one is of — the wire says only that the frame's anchor is
    `sale_at`. That is law loss AT THE LAST INCH, after admission spent four checks keeping the
    governed meaning intact, and it is the loss P5-03 names. No new wire shape was needed for it:
    `disclosure_wire._values` already emits `{group-dims…, value}` rows whenever the frame carries
    dimensions beside the value, and emits a bare scalar only when it does not. What was missing was
    a frame that carried them.

    The coordinate columns are the GOVERNED component names, because that is what the carrier was
    admitted with — CHECK 4 compared them against the anchor's declared components, so a physical
    column name cannot reach this line."""
    if st.table is not None and st.anchor_columns:
        frame = pl.from_arrow(st.table)
        coords = [c for c in st.anchor_columns if c in frame.columns]
        value_col = [c for c in frame.columns if c not in coords]
        frame = frame.rename({value_col[0]: name}).select([*coords, name])
        return ColumnResult(name=name, expr=name, frame=frame, disclosure=Disclosure.clean())
    series = pl.from_arrow(st.array).alias(name)
    return ColumnResult(name=name, expr=name, frame=pl.DataFrame({name: series}),
                        disclosure=Disclosure.clean())


def _finalized_column(name: str, final) -> ColumnResult:
    """A served column carrying a FINALIZED value. It is served; it is not retained."""
    return ColumnResult(name=name, expr=name,
                        frame=pl.DataFrame({name: pl.Series([final.value])}),
                        disclosure=Disclosure.clean())


def plan_result(pub, views: dict, statement) -> FrameResult:
    """PRE-FLIGHT. The would-be answer to a Frame-QL request, TOUCHING NO DATA and no retained state.

    This is what `check_frame_query` asks for, and the whole of what this slice implements. It reads
    the request, resolves it to a governed `AnalyticalIdentity` (see `request.resolve`), asks whether
    the governed law licenses the ask, and returns the neutral `FrameResult` the server will wire.

    IT DELIBERATELY DOES NOT CONSULT THE STORE. A pre-flight that asked whether material state was
    present would answer a different question — "can this be served right now" rather than "is this
    askable" — and would make the cheap check depend on materialization. `decide_result` is where
    state is consulted; the two are separate on purpose, and the separation is why this path can
    honestly claim to touch nothing.

    The column carries `frame=None`, exactly as Core's own `Planner.plan` does: a planned column has
    no data by construction, and the wire already understands that shape."""
    try:
        req = _request.resolve(pub, statement)

        view = views.get(req.family.family_id)
        if view is None:
            raise WantOfLaw(
                f"the publication declares {req.family.canonical_reference!r} but no resolved law "
                f"view was supplied for {req.family.family_id}; this path does not resolve law on "
                f"the fly", subject=req.family.family_id)

        c7 = view[C7_SUFFICIENT_STATE]
        if c7.standing != ESTABLISHED:
            raise WantOfLaw(f"sufficient-state basis is {c7.standing}",
                            subject=view.canonical_reference)

        col = ColumnResult(name=req.column_name, expr=statement.series[0].expr, frame=None,
                           disclosure=Disclosure.clean())
        return FrameResult(None, Disclosure.clean(), [col], tuple(statement.anchor))

    except RealizationContradictsLaw as c:
        # NOT A GOVERNED VERDICT. The two artifacts disagree, so nothing was executed
        # and there is no finding about the data to report. Caught before the governed
        # handler and never allowed to fall through to it.
        return FrameResult(None, Disclosure.clean(),
                           [_contradiction_column(_planned_name(statement), str(c))],
                           tuple(statement.anchor))
    except ProofRefusal as r:
        # Governed defects only. `UnsupportedByThisProfile` is NOT caught here: a capability limit is
        # not a governed verdict, and dressing it as one is the specific dishonesty §7 forbids.
        reason, alts = _classify(r)
        col = _refusal_column(_planned_name(statement), reason, str(r), alts)
        return FrameResult(None, Disclosure.clean(), [col], tuple(statement.anchor))


#: The wire reason for a PROFILE CAPABILITY LIMIT (ruled Huayin, 2026-09-14). Already registered —
#: `(ERROR, None, REALIZATION)`, "not implemented in this build (capability)" — so this mints
#: nothing, changes no mood and does not move the contract version. It is the honest public name for
#: "the request may be meaningful and this build does not implement what it needs".
UNSUPPORTED = "unsupported"


def _unsupported_column(name: str, detail: str) -> ColumnResult:
    """A capability limit, as the wire outcome it is — and NEVER as a governed refusal.

    The translation happens HERE, at the serving boundary, and nowhere earlier: `UnsupportedByThisProfile`
    is deliberately not a `ProofRefusal` and must not become one, because a capability gap given a
    jurisdiction tells an operator their question was unlawful when it was merely unimplemented. It
    reaches the wire as an ERROR carrying `unsupported`, not as `want_of_law` (which would say the
    governed law refused) and not as `want_of_state` (whose remedy would send them to re-materialize
    against a path that does not exist).

    NO ALTERNATIVES ARE ATTACHED. `alternatives` is re-encoded verbatim by the wire and never
    synthesized, and this profile has no alternative to offer: there is no fallback to Core, by
    construction."""
    return ColumnResult(
        name=name, expr=name, frame=None, disclosure=Disclosure.clean(),
        refusal=Outcome(reason=UNSUPPORTED, detail=detail, measure=name, alternatives=()),
    )


def _contradiction_column(name: str, detail: str) -> ColumnResult:
    """A realization that contradicts governed law, as the wire outcome it is.

    ERROR / REALIZATION, carrying `realization_contradicts_law` — minted 2026-09-14 with the
    realization-claim ruling. Translated HERE and nowhere earlier, for the same reason
    `_unsupported_column` is: `RealizationContradictsLaw` is deliberately not a `ProofRefusal`, so
    the governed handler cannot reach it and cannot hand it a governed jurisdiction.

    NO ALTERNATIVES, AND SPECIFICALLY NOT `REMATERIALIZE`. The fix is to correct or replace the
    realization mapping. `alternatives` is re-encoded verbatim by the wire and never synthesized,
    and this vocabulary has no lawful spelling for that remedy — the nearest string reads
    "re-realization / re-materialization may resolve this", which looks lawful for a mapping fix
    while bundling it with a data re-pull the operator would then actually perform. Ruled: omit
    rather than reuse a misleading one."""
    return ColumnResult(
        name=name, expr=name, frame=None, disclosure=Disclosure.clean(),
        refusal=Outcome(reason=REALIZATION_CONTRADICTS_LAW, detail=detail, measure=name,
                        alternatives=()),
    )


def unsupported_result(statement, detail: str) -> FrameResult:
    """A capability limit as a whole neutral result — for the cases that never reach `run_result`."""
    return FrameResult(None, Disclosure.clean(),
                       [_unsupported_column(_planned_name(statement), detail)],
                       tuple(statement.anchor))


def run_result(pub, views: dict, mapping, bindings, statement) -> FrameResult:
    """MATERIAL EXECUTION — the `execute_frame_query` capability, for one shape of ask.

    THE ORDER IS THE PROPOSITION, and it is the same order the rest of this path already keeps: law
    first, then the claim, then material, then the carrier.

        1. request     -> a governed AnalyticalIdentity, from governed law alone       (no material)
        2. law         -> C7 established; the anchor is the constitutive one           (no material)
        3. claim       -> exactly one realization for this family; exactness is exact  (no material)
        4. material    -> the endpoint resolves through the deployment's source binding
        5. admission   -> domain, grain, coordinates, absence
        6. state       -> retained request-locally, with its standing
        7. serve       -> the neutral FrameResult, coordinates and all

    STEPS 1–3 TOUCH NOTHING. Every refusal that can be reached from law and claim alone is reached
    before a single value is read, which is what "refuse before material access" means and why the
    negative controls can assert it.

    THE STORE IS BUILT HERE, PER REQUEST. No durability, no reuse, no eviction policy — the provider
    holds no store and this function does not give it one. A request-local store cannot serve a
    stale state because it cannot serve a state it did not just constitute, and the honest cost is
    that it re-reads material every time. Persistence is a later proof and is gated on the identity
    and reuse-key questions the register still carries."""
    column = _planned_name(statement)
    try:
        req = _request.resolve(pub, statement)
        column = req.column_name

        view = views.get(req.family.family_id)
        if view is None:
            raise WantOfLaw(
                f"the publication declares {req.family.canonical_reference!r} but no resolved law "
                f"view was supplied for {req.family.family_id}", subject=req.family.family_id)

        c7 = view[C7_SUFFICIENT_STATE]
        if c7.standing != ESTABLISHED:
            raise WantOfLaw(f"sufficient-state basis is {c7.standing}",
                            subject=view.canonical_reference)

        # ── 3. the claim, still touching nothing ────────────────────────────────────────────────
        realization = realize(mapping, req.family.family_id)
        require_exact_realization(view, realization)
        require_continuation_conformance(view, realization)

        c4 = view[C4_FORMATION]
        if c4.standing != ESTABLISHED or not isinstance(c4.value, dict):
            raise WantOfLaw(f"the formation responsibility is {c4.standing}",
                            subject=view.canonical_reference)
        kind = c4.value.get("kind")
        store = RetainedStateStore()

        if kind == PRIMITIVE:
            # INTAKE. The family's own realization names the material; admission decides whether
            # what arrived is faithfully the governed domain.
            anchored = _source.read_anchored(
                bindings, realization,
                component_realizations(mapping, req.family.constitutive_anchor))
            materialize_anchored(pub, req.family, view, realization, anchored,
                                 basis=c7.value, store=store)

        elif kind == CONSTRUCTION:
            # FORMATION. The material is the OPERAND's — a constructed family is not delivered from
            # anywhere — so its claim is resolved and checked first, and the constructed family's own
            # claim is checked to describe the SAME material rather than a second source.
            operand = operand_family(pub, req.family)
            operand_view = views.get(operand.family_id)
            if operand_view is None:
                raise WantOfLaw(
                    f"no resolved law view for operand {operand.family_id}",
                    subject=req.family.family_id)
            operand_realization = realize(mapping, operand.family_id)
            require_exact_realization(operand_view, operand_realization)
            require_continuation_conformance(operand_view, operand_realization)
            if realization.endpoint != operand_realization.endpoint:
                raise WantOfState(
                    f"{req.family.canonical_reference} realizes a different endpoint from its "
                    f"operand {operand.canonical_reference}; a constructed family is formed FROM "
                    f"its operand's contributions, so a second source would be a second family",
                    subject=req.family.family_id)
            if realization.grain != operand_realization.grain:
                raise WantOfState(
                    f"{req.family.canonical_reference} claims grain {realization.grain!r} and its "
                    f"operand claims {operand_realization.grain!r} over the same material; one of "
                    f"the two is wrong and this profile will not choose",
                    subject=req.family.family_id)
            anchored = _source.read_anchored(
                bindings, operand_realization,
                component_realizations(mapping, operand.constitutive_anchor))
            materialize_constructed(pub, req.family, view, operand, operand_view, realization,
                                    operand_realization, anchored, basis=c7.value, store=store)

        else:                                                  # pragma: no cover - closed vocabulary
            raise UnsupportedByThisProfile(
                f"formation kind {kind!r} is not one this profile executes")

        # ── 7. serve ────────────────────────────────────────────────────────────────────────────
        return decide_result(view, store, req.identity, column=column)

    except UnsupportedByThisProfile as u:
        # A CAPABILITY LIMIT, NOT A VERDICT. Caught separately and translated to `unsupported`; it is
        # never allowed to fall through to the governed handler below and borrow a jurisdiction.
        return FrameResult(None, Disclosure.clean(), [_unsupported_column(column, str(u))],
                           tuple(statement.anchor))
    except RealizationContradictsLaw as c:
        # NOT A GOVERNED VERDICT. The two artifacts disagree, so nothing was executed
        # and there is no finding about the data to report. Caught before the governed
        # handler and never allowed to fall through to it.
        return FrameResult(None, Disclosure.clean(), [_contradiction_column(column, str(c))],
                           tuple(statement.anchor))
    except ProofRefusal as r:
        reason, alts = _classify(r)
        return FrameResult(None, Disclosure.clean(),
                           [_refusal_column(column, reason, str(r), alts)],
                           tuple(statement.anchor))


def _planned_name(statement) -> str:
    """The column name for a request that did not resolve — the alias if the author gave one, else
    the series text verbatim. Never a guess at what they meant."""
    if len(statement.series) == 1:
        return statement.series[0].alias or statement.series[0].expr.strip()
    return "?"


def decide_result(law_view, store: RetainedStateStore, identity: AnalyticalIdentity, *,
                  at_anchor: Optional[str] = None, column: str = "revenue",
                  licence: Optional[MovementLicence] = None) -> FrameResult:
    """serve | refuse, as the NEUTRAL `FrameResult` — the successor path's answer, unwired.

    THIS IS THE INTEGRATION SEAM (ruled Huayin, 2026-09-12 §4). `FrameResult` is owned by
    `columna_core.serving_contract`, which belongs to no execution strategy, so a serving surface can
    take this path's answer without either side importing the other's runtime. The result carries no
    `executed` flag and no `contract_version`: BOTH ARE THE WIRE'S TO DECIDE, and the wire is applied
    exactly once, by the server. A second serializer here would be a second contract.

    `decide` (below) is the wrapper that wires this for the standalone proofs. Nothing else in this
    module calls `wire_frame`.

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
            return FrameResult(col.frame, Disclosure.clean(), [col], (identity.anchor,))

        col = _served_column(column, st)
        return FrameResult(col.frame, Disclosure.clean(), [col], (identity.anchor,))

    except RealizationContradictsLaw as c:
        # NOT A GOVERNED VERDICT. The two artifacts disagree, so nothing was executed
        # and there is no finding about the data to report. Caught before the governed
        # handler and never allowed to fall through to it.
        return FrameResult(None, Disclosure.clean(), [_contradiction_column(column, str(c))],
                           (identity.anchor,))
    except ProofRefusal as r:
        reason, alts = _classify(r)
        col = _refusal_column(column, reason, str(r), alts)
        return FrameResult(None, Disclosure.clean(), [col], (identity.anchor,))


def decide(law_view, store: RetainedStateStore, identity: AnalyticalIdentity, *,
           at_anchor: Optional[str] = None, column: str = "revenue",
           licence: Optional[MovementLicence] = None) -> dict:
    """`decide_result`, WIRED — the standalone-proof entry point, unchanged in behaviour.

    Returns the wire dict from `disclosure_wire.wire_frame` — not a Proof-A-shaped imitation of it.
    The proofs assert against the real wire and keep doing so; this wrapper is why the factoring
    below it cost them nothing.

    `executed=True` is right HERE and only here: this function runs the path. The server's check
    surface plans without executing and wires the same neutral result with `executed=False`, which is
    precisely why the flag cannot live inside `decide_result`."""
    return wire_frame(decide_result(law_view, store, identity, at_anchor=at_anchor, column=column,
                                    licence=licence),
                      universe=None, executed=True)
