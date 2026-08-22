"""
columna_core.compiler.compile — the K0 compile boundary.

    compile_k0(publication, mapping) -> ClosedExecutionImage

TWO INPUTS. ONLY TWO. The compiler consumes the governed publication and the private core mapping,
and it may not reach into Studio session state, `Declaration.evidence`, audit/profile objects,
`manifold.columna.yaml`, or `draft.lower_to_cml` output — nor repair a missing input from any of
them. There is no code here that could: neither reader can see those things.

THE OUTPUT IS CLOSED. Compilation answers "can governed law be faithfully translated into the Core
execution representation?" Certification answers "is this path licensed on this realization and data
state?" — a different question, asked later by the adjudicator. `compile_k0` therefore never raises
`GovernedCertificationMissing`, and nothing it emits implies admission.

REFUSAL BEFORE OMISSION. An out-of-scope construct in the publication is a refusal with a named
category, never an image that quietly lacks it. A silently-dropping compiler would make the receipt
bind a publication to an image that does not carry its meaning — which is the exact failure the
binding was introduced to prevent.

K0 SCOPE (ratified): measure . member . anchor, plus the unrestricted UNIVERSE and base LEVEL
declarations required for a well-formed image. Reducers: sum . count . min . max.
"""
from __future__ import annotations

from dataclasses import dataclass

from ..operators import REGISTRY, signature_ok
from . import emit
from .inputs import (
    GovernedPublication,
    PrivateCoreMapping,
    require_same_publication,
)
from .refusals import (
    ExecutionRepresentationGap,
    LogicalMeaningMissing,
    MappingIncomplete,
    UnsupportedCoreCapability,
)

#: The ratified K0 reducer allow-list. Not "the reducers Core has" — the reducers K0 emits.
#:
#: All four are VALUE-witness monoids Core executes exactly, verified end to end against this pin
#: (parse, check(), publish(), leaf-grain serve, and rolled-up serve exercising the monoid combine).
#: `mean` is excluded on DEMONSTRATED failure, not on classification: it parses clean AND checks
#: clean, then refuses at execution, because `in_core` is consulted only on the scan path.
K0_REDUCERS = frozenset({"sum", "count", "min", "max"})

#: Reducers deliberately held out, each with the reason a refusal should say out loud. Nothing is
#: excluded merely for tidiness — that was the lesson of the min/max verification.
_WHY_NOT = {
    "mean": ("shipped Core accepts `mean` as a declared member and then refuses it at execution "
             "('holistic operator not implemented'); emitting it would produce an image that "
             "validates and then fails at query time"),
    "avg": ("`avg` is an alias Core never canonicalizes in well-formedness, so it is a hard parse "
            "error as a declared member; see `mean`"),
    "median": ("held out of K0 for scope minimality; shipped Core does execute it, and its compiler "
               "classification is deferred rather than settled"),
    "mode": ("held out of K0 for scope minimality; shipped Core does execute it, and its compiler "
             "classification is deferred rather than settled"),
    "last": ("requires `ORDER <level>`, which Core does not validate at parse — the obligation "
             "would fall on the compiler, and K0 does not carry it"),
    "first": ("requires `ORDER <level>`, which Core does not validate at parse — the obligation "
              "would fall on the compiler, and K0 does not carry it"),
    "distinct": ("sketch witness, and single-target-level only in this build"),
}

#: governed `value_type` -> Core logical dtype. FROZEN and TOTAL on the governed vocabulary: an
#: unrecognised type refuses rather than defaulting, because defaulting would substitute the
#: compiler's guess for the author's declaration.
#:
#: `decimal` -> Float64 is the one lossy edge and it is deliberate: the governed vocabulary folds
#: DECIMAL/NUMERIC/DOUBLE/REAL/FLOAT/MONEY into one token, so it does not currently draw the
#: fixed-point-vs-binary-float distinction that choosing Core's `Decimal` would require. Recorded as
#: a K1 question rather than guessed at here.
_VALUE_TYPE_TO_DTYPE = {
    "integer": "Int64",
    "decimal": "Float64",
    "text": "String",
    "boolean": "Boolean",
    "date": "Date",
    "timestamp": "Datetime",
    "time": "Time",
}

#: The honest mid-authoring placeholder. It is a legitimate authoring state and an illegitimate
#: PUBLISHED one: a placeholder that reaches a compiled image is exactly the silence to close.
_PLACEHOLDER_VALUE_TYPE = "unknown"

#: Declaration kinds K0 refuses, and the category each refusal carries.
_OUT_OF_SCOPE = {
    "relationship": (UnsupportedCoreCapability,
                     "relationship is out of K0 scope: a bare crossing must stay non-functional "
                     "transport, and a faced crossing needs governed certification that is not "
                     "carried across the boundary yet"),
    "hierarchy": (UnsupportedCoreCapability,
                  "hierarchy is out of K0 scope: functional transport is certification-dependent, "
                  "and K0 emits no edges"),
    "attribute": (UnsupportedCoreCapability,
                  "attribute is out of K0 scope: co-located attachment needs a keyed-at-grain proof "
                  "and cross-table attachment needs a governed route, neither of which is in this "
                  "unit"),
    "boundary": (ExecutionRepresentationGap,
                 "boundary cannot be represented: `across` has no slot anywhere in the Core "
                 "execution grammar, and product-scoped forbiddance collapses in `blocked_lineages`"),
    "crosswalk": (LogicalMeaningMissing,
                  "crosswalk lacks the shared correspondence semantics needed to choose a faithful "
                  "lowering; it is not sugar over HIERARCHY or RELATE"),
}


@dataclass(frozen=True)
class ClosedExecutionImage:
    """The compile product: a closed image plus the identity it must be bound to.

    `text` is the `.cml`. `publication_ref` is what a receipt must bind it to. Nothing here is a
    licence, and nothing here is a runtime admission."""

    manifold_id: str
    version: str
    text: str

    def encode(self) -> bytes:
        """The image AS SHIPPED — the exact bytes a digest is taken over."""
        return self.text.encode("utf-8")


def _dtype_for(measure_name: str, body: dict) -> str:
    vt = body.get("value_type")
    if not isinstance(vt, str) or not vt:
        raise LogicalMeaningMissing("measure declares no value_type",
                                    subject=f"measure {measure_name}")
    if vt == _PLACEHOLDER_VALUE_TYPE:
        raise LogicalMeaningMissing(
            "measure's value_type is still the authoring placeholder 'unknown' — a placeholder that "
            "reaches a compiled image is a silence, not a type",
            subject=f"measure {measure_name}")
    dtype = _VALUE_TYPE_TO_DTYPE.get(vt)
    if dtype is None:
        raise ExecutionRepresentationGap(
            f"governed value_type {vt!r} has no Core logical dtype; K0 will not guess one",
            subject=f"measure {measure_name}")
    return dtype


def _check_reducer(agg: str, dtype: str, subject: str) -> None:
    if agg not in K0_REDUCERS:
        why = _WHY_NOT.get(agg)
        detail = (f"reducer {agg!r} is not in the K0 allow-list {sorted(K0_REDUCERS)}")
        if why:
            detail += f" — {why}"
        elif agg in REGISTRY:
            detail += " — Core registers it, but K0 does not emit it"
        else:
            detail += " — Core does not register it as a reducer at all"
        raise UnsupportedCoreCapability(detail, subject=subject)
    # Self-verification against Core's own signature law, so the compiler refuses rather than
    # emitting a document whose own `check()` would reject it.
    op = REGISTRY[agg]
    if not signature_ok(op, dtype):
        raise UnsupportedCoreCapability(
            f"reducer {agg!r} does not accept a {dtype} measure (accepts {sorted(op.accepts)})",
            subject=subject)


def compile_k0(publication: GovernedPublication,
               mapping: PrivateCoreMapping) -> ClosedExecutionImage:
    """Compile a governed publication + its private realization into a CLOSED Core image."""
    # ── 0. input authority, before any lowering ──────────────────────────────────────────────────
    require_same_publication(publication, mapping)

    # ── 1. scope gate: refuse, never omit ────────────────────────────────────────────────────────
    for kind, (exc, why) in _OUT_OF_SCOPE.items():
        present = publication.of_kind(kind)
        if present:
            raise exc(why, subject=f"{kind} '{present[0].name}'")

    anchors = publication.of_kind("anchor")
    universes = publication.of_kind("universe")
    measures = publication.of_kind("measure")
    members = publication.of_kind("member")
    if not measures:
        raise LogicalMeaningMissing("publication declares no measure; K0 compiles nothing")

    # ── 2. anchor components: named, complete, unambiguous ───────────────────────────────────────
    declared: dict = {}
    for a in anchors:
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
                f"anchor {r.anchor_ref!r} declares no component {r.component_name!r} "
                f"(declared: {declared[r.anchor_ref]})",
                subject=f"anchor_component {r.anchor_ref}.{r.component_name}")
        key = (r.anchor_ref, r.component_name)
        if key in realized:
            raise MappingIncomplete(
                "component is realized twice — one component, one realization; tuple position is "
                "not identity", subject=f"anchor_component {r.anchor_ref}.{r.component_name}")
        realized[key] = r.endpoint

    for aname, comps in declared.items():
        for cn in comps:
            if (aname, cn) not in realized:
                raise MappingIncomplete(
                    "component has no realization — every authored component maps to exactly one",
                    subject=f"anchor_component {aname}.{cn}")

    # one LEVEL per component name; a name meaning two different columns is not a level
    level_column: dict = {}
    for (aname, cn), ep in sorted(realized.items()):
        prior = level_column.get(cn)
        if prior is not None and prior != ep.column:
            raise ExecutionRepresentationGap(
                f"component name {cn!r} realizes both {prior!r} and {ep.column!r}; one Core LEVEL "
                f"cannot carry two columns", subject=f"level {cn}")
        level_column[cn] = ep.column

    # ── 3. universes: unrestricted only ──────────────────────────────────────────────────────────
    universe_dims: dict = {}
    universe_lines = []
    for u in sorted(universes, key=lambda d: d.name):
        if u.body.get("restriction") is not None:
            raise UnsupportedCoreCapability(
                "universe carries a restriction; K0 emits unrestricted universes only, because "
                "restriction lowering is compiler composition over coordinate realizations and that "
                "composition is not in this unit", subject=f"universe {u.name}")
        aref = u.body.get("anchor")
        if not isinstance(aref, str) or not aref:
            raise LogicalMeaningMissing("universe names no anchor", subject=f"universe {u.name}")
        if aref not in declared:
            raise LogicalMeaningMissing(f"universe names anchor {aref!r}, which is not declared",
                                        subject=f"universe {u.name}")
        dims = tuple(declared[aref])
        universe_dims[u.name] = dims
        basis = u.body.get("basis")
        universe_lines.append(emit.universe_line(u.name, dims,
                                                 basis if isinstance(basis, str) else None))

    # ── 4. members grouped onto their measure ────────────────────────────────────────────────────
    by_member = {m.member_ref: m for m in mapping.members}
    if len(by_member) != len(mapping.members):
        raise MappingIncomplete("a member is realized more than once")

    grouped: dict = {}
    for d in members:
        mref = d.body.get("measure")
        if not isinstance(mref, str) or not mref:
            raise LogicalMeaningMissing("member names no measure", subject=f"member {d.name}")
        r = by_member.get(d.name)
        if r is None:
            raise MappingIncomplete("member has no realization", subject=f"member {d.name}")
        if r.measure_ref != mref:
            raise MappingIncomplete(
                f"mapping realizes member of measure {r.measure_ref!r}, but the publication "
                f"declares it on {mref!r}", subject=f"member {d.name}")
        uref = d.body.get("universe")
        if isinstance(uref, str) and uref and r.universe_ref != uref:
            raise MappingIncomplete(
                f"mapping realizes member against universe {r.universe_ref!r}, but the publication "
                f"declares it on {uref!r}", subject=f"member {d.name}")
        grouped.setdefault(mref, []).append((d, r))

    # ── 5. measures ──────────────────────────────────────────────────────────────────────────────
    measure_blocks = []
    used_levels = set()
    for md in sorted(measures, key=lambda d: d.name):
        pairs = grouped.get(md.name)
        if not pairs:
            raise LogicalMeaningMissing(
                "measure has no member; a measure with no member declares no reduction and cannot "
                "be served", subject=f"measure {md.name}")
        dtype = _dtype_for(md.name, md.body)

        tables = {r.endpoint.table for _, r in pairs}
        columns = {r.endpoint.column for _, r in pairs}
        if len(tables) != 1 or len(columns) != 1:
            raise ExecutionRepresentationGap(
                f"members of this measure realize {sorted(tables)} / {sorted(columns)}; a Core "
                f"measure has exactly one home table and one value expression",
                subject=f"measure {md.name}")
        table = tables.pop()
        column = columns.pop()
        if column is None:
            raise MappingIncomplete("measure's members realize no value column",
                                    subject=f"measure {md.name}")

        uref = {r.universe_ref for _, r in pairs}
        if len(uref) != 1:
            raise ExecutionRepresentationGap(
                f"members of this measure span universes {sorted(uref)}; a Core measure binds one",
                subject=f"measure {md.name}")
        universe = uref.pop()
        if universe not in universe_dims:
            raise LogicalMeaningMissing(f"measure binds universe {universe!r}, which is not declared",
                                        subject=f"measure {md.name}")
        used_levels.update(universe_dims[universe])

        aggs = []
        for d, r in sorted(pairs, key=lambda p: p[0].name):
            _check_reducer(r.root_evaluator, dtype, subject=f"member {d.name}")
            if r.root_evaluator in aggs:
                raise ExecutionRepresentationGap(
                    f"two members realize the same reducer {r.root_evaluator!r}; a Core family is "
                    f"keyed by operator and cannot hold both", subject=f"measure {md.name}")
            aggs.append(r.root_evaluator)

        measure_blocks.append(emit.measure_block(md.name, universe, table, column,
                                                 tuple(sorted(aggs)), dtype))

    # ── 6. render, deterministically ─────────────────────────────────────────────────────────────
    level_lines = [emit.level_line(n, level_column[n]) for n in sorted(used_levels)]
    text = emit.render(publication.ref.manifold_id, publication.ref.version,
                       tuple(universe_lines), tuple(level_lines), tuple(measure_blocks))
    return ClosedExecutionImage(publication.ref.manifold_id, publication.ref.version, text)
