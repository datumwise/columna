"""
columna_core.compiler.compile_v2 — the K0v2 compile boundary.

    compile_v2(publication_v2, private_mapping_v2) -> ClosedExecutionImage

WHAT CHANGED, IN ONE SENTENCE: the Core family is built from **established governed law**, and the
private mapping is **checked against it** rather than read for it.

The v1 compiler assembled `FAMILY {…}` out of `MemberRealization.root_evaluator` — a private
realization field — while its own input reader said of that field *"a compiler that chose a reducer
would be manufacturing analytical law."* It was not manufacturing law; it was importing it from the
wrong side of the boundary. Here the family's formation and continuation come from the resolved
`Law(F)` view, and the mapping's `formation_operator` is a CLAIM this module verifies.

FIVE CHECKS THAT DID NOT EXIST BEFORE, each refusing rather than repairing:

  1. **Family validity.** A record cannot claim to establish a MeasureFamily while its
     identity-bearing constitution is unresolved (`resolve.IDENTITY_BEARING`).
  2. **Grain correspondence.** A mapping claiming its source is FINER than the constitutive anchor
     compiles only if the family's formation establishes how contributions resolve. This is the
     contribution-grain finding: in v1 that law was supplied silently by `root_evaluator`.
  3. **Delivery correspondence.** The claimed backend operator must be the one this profile uses to
     discharge the declared foundation law. A mismatch is a mapping gap, never a re-interpretation.
  4. **Continuation conformance.** Core's own engine mechanics — `operators.REGISTRY[op].combine` —
     must agree with the governed continuation law. A build whose engine combines differently from
     what the publication declares is refused rather than served.
  5. **Movement establishment.** If the emitted image admits any movement at all, every family's
     domain-and-movement must be established. K0 emits no hierarchies, so no movement is reachable
     and `unestablished` is safe here — **that was previously true by accident and is now checked**.

REFUSAL NEVER NARROWS THE LAW (§4.1). `K0_LAWS` is a realization profile: a law outside it refuses
with a named category, and the governed law is untouched.
"""
from __future__ import annotations

from ..governed import resolve as R
from ..governed.publication import COINCIDENT as FORMATION_COINCIDENT
from ..governed.publication import CONSTRUCTION
from ..operators import REGISTRY
from . import emit
from .compile import ClosedExecutionImage
from .realization import COINCIDENT, EXACT, FINER, PrivateCoreMappingV2, require_same_publication
from .refusals import (
    ExecutionRepresentationGap,
    LogicalMeaningMissing,
    MappingIncomplete,
    UnsupportedCoreCapability,
)

#: How THIS profile realizes each foundation law. Realization knowledge, deliberately here and not in
#: the vocabulary: the vocabulary must stay backend-independent, and which operator discharges SUM is
#: a fact about Core, not about SUM.
K0_LAWS = {"SUM": "sum", "COUNT": "count", "MIN": "min", "MAX": "max"}

#: Laws this build knows and will not emit, each with the reason a refusal should say out loud.
_WHY_NOT = {
    "MEAN": ("shipped Core accepts `mean` as a declared member and then refuses it at execution, so "
             "emitting it would produce an image that validates and then fails at query time. The "
             "governed law is untouched by that (§4.1)"),
}

#: Governed value domain -> Core logical dtype. FROZEN and TOTAL over the governed vocabulary: an
#: unrecognised domain refuses rather than defaulting, because defaulting substitutes the compiler's
#: guess for the author's declaration.
_DOMAIN_TO_DTYPE = {
    "integer": "Int64", "decimal": "Float64", "text": "String", "boolean": "Boolean",
    "date": "Date", "timestamp": "Datetime", "time": "Time",
}

#: Declaration kinds out of K0v2 scope, with the category each refusal carries.
_OUT_OF_SCOPE = {
    "relationship": (UnsupportedCoreCapability,
                     "relationship is out of K0 scope: a bare crossing must stay non-functional "
                     "transport, and a faced crossing needs governed certification"),
    "hierarchy": (UnsupportedCoreCapability,
                  "hierarchy is out of K0 scope: functional transport is certification-dependent, "
                  "and K0 emits no edges"),
    "attribute": (UnsupportedCoreCapability,
                  "attribute is out of K0 scope: co-located attachment needs a keyed-at-grain proof"),
    "crosswalk": (LogicalMeaningMissing,
                  "crosswalk lacks the shared correspondence semantics needed to choose a faithful "
                  "lowering"),
}

#: Does the image this compiler emits admit any MOVEMENT? K0 emits SOURCE_MANIFOLD, UNIVERSE, base
#: LEVELs and MEASUREs — and no hierarchy, therefore no edge, therefore nothing to travel along.
#: Named as a constant rather than left implicit because the safety it buys was previously an
#: accident of scope: the moment a profile emits edges, this flips and every family's
#: domain-and-movement must be established before anything compiles.
K0_EMITS_MOVEMENT = False


def _dtype(domain: str, subject: str) -> str:
    dt = _DOMAIN_TO_DTYPE.get(domain)
    if dt is None:
        raise ExecutionRepresentationGap(
            f"governed value domain {domain!r} has no Core logical dtype; K0 will not guess one",
            subject=subject)
    return dt


def _core_operator(law_name: str, subject: str) -> str:
    op = K0_LAWS.get(law_name)
    if op is None:
        why = _WHY_NOT.get(law_name)
        detail = f"foundation law {law_name!r} is not in this profile {sorted(K0_LAWS)}"
        if why:
            detail += f" — {why}"
        raise UnsupportedCoreCapability(detail, subject=subject)
    return op


def _check_continuation_conformance(law_name: str, member_op: str, subject: str) -> None:
    """Core's engine mechanics must agree with the governed continuation law.

    `REGISTRY[op].combine` is how this engine merges partial results. The governed continuation law
    says how values of the family compose. If those disagree, the build would serve a rollup the
    publication does not describe — so it refuses. COUNT is the case that makes this worth checking:
    its formation counts, and its continuation SUMS (§5.2)."""
    op = REGISTRY.get(member_op)
    if op is None:                                          # pragma: no cover - profile guarantees
        raise UnsupportedCoreCapability(f"Core registers no operator {member_op!r}", subject=subject)
    expected = K0_LAWS.get(law_name)
    if op.combine != expected:
        raise UnsupportedCoreCapability(
            f"governed continuation is {law_name} (this profile realizes it as {expected!r}), but "
            f"Core's operator {member_op!r} combines by {op.combine!r}. The engine and the "
            f"publication disagree about how this family composes; serving it would serve a rollup "
            f"the publication does not describe.", subject=subject)


def compile_v2(publication, mapping: PrivateCoreMappingV2) -> ClosedExecutionImage:
    """Compile a v2 governed publication + its v2 realization into a CLOSED Core image."""
    # ── 0. input authority ───────────────────────────────────────────────────────────────────────
    require_same_publication(publication, mapping)

    # ── 1. scope gate: refuse, never omit ────────────────────────────────────────────────────────
    for kind, (exc, why) in _OUT_OF_SCOPE.items():
        present = publication.of_kind(kind)
        if present:
            raise exc(why, subject=f"{kind} '{present[0].name}'")

    if not publication.families:
        raise LogicalMeaningMissing("publication declares no family; K0 compiles nothing")

    # ── 2. resolve every family's law, and require identity to be settled ────────────────────────
    try:
        views = R.resolve_all(publication)
    except R.LawResolutionRefusal as exc:
        raise LogicalMeaningMissing(str(exc)) from exc

    for fid, view in sorted(views.items()):
        problems = view.validity_problems
        if problems:
            raise LogicalMeaningMissing(
                "a record cannot claim to establish a MeasureFamily while its identity-bearing "
                "constitution is unresolved: " + "; ".join(problems),
                subject=f"family {view.canonical_reference} [{fid}]")

    # ── 3. movement: safe only because nothing can travel ────────────────────────────────────────
    if K0_EMITS_MOVEMENT:                                   # pragma: no cover - profile constant
        for fid, view in sorted(views.items()):
            if view.standing(R.C3_DOMAIN_MOVEMENT) == R.UNESTABLISHED:
                raise LogicalMeaningMissing(
                    "this image admits movement, so every family's domain and movement must be "
                    "established; absence of a prohibition is not permission",
                    subject=f"family {view.canonical_reference} [{fid}]")

    # ── 4. anchors and universes (unchanged in intent from v1) ───────────────────────────────────
    declared: dict = {}
    for a in publication.of_kind("anchor"):
        comps = a.body.get("components")
        if not isinstance(comps, list) or not comps:
            raise LogicalMeaningMissing("anchor declares no components", subject=f"anchor {a.name}")
        names = []
        for c in comps:
            cn = c.get("name") if isinstance(c, dict) else None
            if not isinstance(cn, str) or not cn:
                raise LogicalMeaningMissing("anchor component has no name",
                                            subject=f"anchor {a.name}")
            if cn in names:
                raise LogicalMeaningMissing(f"anchor declares component {cn!r} twice",
                                            subject=f"anchor {a.name}")
            names.append(cn)
        declared[a.name] = names

    realized: dict = {}
    for r in mapping.anchor_components:
        if r.anchor_ref not in declared:
            raise MappingIncomplete(
                f"mapping realizes a component of anchor {r.anchor_ref!r}, which the publication "
                f"does not declare", subject=f"anchor_component {r.anchor_ref}.{r.component_name}")
        if r.component_name not in declared[r.anchor_ref]:
            raise MappingIncomplete(
                f"anchor {r.anchor_ref!r} declares no component {r.component_name!r}",
                subject=f"anchor_component {r.anchor_ref}.{r.component_name}")
        key = (r.anchor_ref, r.component_name)
        if key in realized:
            raise MappingIncomplete("component is realized twice",
                                    subject=f"anchor_component {r.anchor_ref}.{r.component_name}")
        realized[key] = r.endpoint
    for aname, comps in declared.items():
        for cn in comps:
            if (aname, cn) not in realized:
                raise MappingIncomplete("component has no realization",
                                        subject=f"anchor_component {aname}.{cn}")

    level_column: dict = {}
    for (aname, cn), ep in sorted(realized.items()):
        prior = level_column.get(cn)
        if prior is not None and prior != ep.column:
            raise ExecutionRepresentationGap(
                f"component name {cn!r} realizes both {prior!r} and {ep.column!r}",
                subject=f"level {cn}")
        level_column[cn] = ep.column

    universe_dims, universe_lines = {}, []
    for u in sorted(publication.of_kind("universe"), key=lambda d: d.name):
        if u.body.get("restriction") is not None:
            raise UnsupportedCoreCapability(
                "universe carries a restriction; K0 emits unrestricted universes only",
                subject=f"universe {u.name}")
        aref = u.body.get("anchor")
        if not isinstance(aref, str) or aref not in declared:
            raise LogicalMeaningMissing(f"universe names anchor {aref!r}, which is not declared",
                                        subject=f"universe {u.name}")
        universe_dims[u.name] = tuple(declared[aref])
        basis = u.body.get("basis")
        universe_lines.append(emit.universe_line(u.name, tuple(declared[aref]),
                                                 basis if isinstance(basis, str) else None))

    # ── 5. families -> Core MEASUREs. The FAMILY set comes from LAW, not from the mapping. ───────
    primitives = [f for f in publication.families if f.is_primitive]
    if not primitives:
        raise LogicalMeaningMissing(
            "publication declares no primitive family; K0 realizes constructions over a primitive "
            "operand and has nothing to deliver from")

    by_parent: dict = {}
    for f in publication.families:
        if f.formation.kind == CONSTRUCTION:
            by_parent.setdefault(f.parents[0], []).append(f)
            if len(f.parents) > 1:
                raise UnsupportedCoreCapability(
                    "multi-parent construction is out of K0 scope: a Core measure delivers one "
                    "operand", subject=f"family {f.canonical_reference}")

    measure_blocks, used_levels = [], set()
    for prim in sorted(primitives, key=lambda f: f.canonical_reference):
        subject = f"family {prim.canonical_reference} [{prim.family_id}]"
        view = views[prim.family_id]
        real = mapping.for_family(prim.family_id)
        if real is None:
            raise MappingIncomplete("primitive family has no realization", subject=subject)
        if real.endpoint.column is None:
            raise MappingIncomplete("primitive family's realization names no value column",
                                    subject=subject)

        # CHECK 2 — grain correspondence against established formation.
        formation = view[R.C4_FORMATION].value
        structure = formation.get("contribution_structure")
        if real.grain == FINER and structure == FORMATION_COINCIDENT:
            raise MappingIncomplete(
                "the realization claims the source grain is FINER than the constitutive anchor, but "
                "the family's formation claims one contribution per analytical point. One of the two "
                "is wrong, and the compiler will not choose.", subject=subject)
        if real.grain == COINCIDENT and structure != FORMATION_COINCIDENT:
            raise MappingIncomplete(
                "the realization claims one source row per analytical point, but the family's "
                "formation establishes a contribution-resolution law — which would have nothing to "
                "resolve", subject=subject)

        universe = prim.universe
        if universe not in universe_dims:
            raise LogicalMeaningMissing(f"family binds universe {universe!r}, which is not declared",
                                        subject=subject)
        used_levels.update(universe_dims[universe])
        dtype = _dtype(view[R.C6_SEMANTIC_VALUES].value, subject)

        # The primitive family's OWN continuation is a Core family member: `revenue.sum` is Revenue
        # continued, not a separate family (the classification test, applied).
        aggs, seen_ops = [], {}
        cont = view[R.C8_CONTINUATION]
        if cont.standing == R.ESTABLISHED:
            op = _core_operator(cont.value.name, subject)
            _check_continuation_conformance(cont.value.name, op, subject)
            if real.continuation_operator not in (None, op):
                raise MappingIncomplete(
                    f"the realization claims continuation operator {real.continuation_operator!r}, "
                    f"but the family's established continuation law {cont.value.name} is realized "
                    f"here as {op!r}", subject=subject)
            aggs.append(op)
            seen_ops[op] = prim.canonical_reference

        # Constructed families over this operand become the remaining Core family members.
        for child in sorted(by_parent.get(prim.family_id, []), key=lambda f: f.canonical_reference):
            csub = f"family {child.canonical_reference} [{child.family_id}]"
            cview = views[child.family_id]
            creal = mapping.for_family(child.family_id)
            if creal is None:
                raise MappingIncomplete("constructed family has no realization", subject=csub)
            if creal.endpoint != real.endpoint:
                raise ExecutionRepresentationGap(
                    "a constructed family realizes a different endpoint from its operand; a Core "
                    "measure has exactly one home table and one value expression", subject=csub)
            law_name = cview[R.C4_FORMATION].value["law_name"]
            op = _core_operator(law_name, csub)
            # CHECK 3 — delivery correspondence. The mapping CLAIMS; the law DECIDES.
            if creal.formation_operator is None:
                raise MappingIncomplete(
                    "constructed family's realization makes no delivery claim: it must name the "
                    "backend operator it claims discharges the declared formation law",
                    subject=csub)
            if creal.formation_operator != op:
                raise MappingIncomplete(
                    f"the realization claims operator {creal.formation_operator!r} discharges "
                    f"formation law {law_name}, but this profile realizes {law_name} as {op!r}. The "
                    f"law decides; the mapping claims; the compiler checks.", subject=csub)
            if creal.exactness != EXACT:
                raise UnsupportedCoreCapability(
                    "K0 emits exact deliveries only; a disclosed approximation needs an explicit "
                    "governed contract and K0 does not invent one", subject=csub)
            # CHECK 4 — Core's mechanics vs the governed continuation.
            ccont = cview[R.C8_CONTINUATION]
            if ccont.standing == R.ESTABLISHED:
                _check_continuation_conformance(ccont.value.name, op, csub)
            if op in seen_ops:
                raise ExecutionRepresentationGap(
                    f"two governed families realize the same Core operator {op!r} over one operand "
                    f"({seen_ops[op]} and {child.canonical_reference}); a Core family is keyed by "
                    f"operator and cannot hold both. The governed layer expresses a family Core "
                    f"cannot represent — which refuses, and does not narrow the law.", subject=csub)
            seen_ops[op] = child.canonical_reference
            aggs.append(op)

        if not aggs:
            raise LogicalMeaningMissing(
                "no family member is established over this operand: the primitive family's "
                "continuation is unestablished and no constructed family cites it", subject=subject)

        measure_blocks.append(emit.measure_block(
            prim.canonical_reference, universe, real.endpoint.table, real.endpoint.column,
            tuple(sorted(aggs)), dtype))

    # ── 6. render, deterministically ─────────────────────────────────────────────────────────────
    level_lines = [emit.level_line(n, level_column[n]) for n in sorted(used_levels)]
    text = emit.render(publication.ref.manifold_id, publication.ref.version,
                       tuple(universe_lines), tuple(level_lines), tuple(measure_blocks))
    return ClosedExecutionImage(publication.ref.manifold_id, publication.ref.version, text)
