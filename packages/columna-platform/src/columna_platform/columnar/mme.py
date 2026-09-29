"""
columna_platform.columnar.mme — **the MME over genuine columnar state.**

    *"The MME kernel remains analytical authority. DataFusion is a provider."* — Huayin, 2026-09-28

THE ARCHITECTURAL CLAIM THIS MODULE MAKES, AND HOW IT IS PROVED
---------------------------------------------------------------
`ColumnarMME` **reuses `kernel.MME.adjudicate` verbatim.** Not a columnar re-implementation of the same
five questions — the same function object, called on columnar state.

That is possible because the adjudication reads only `continuation_bearing`, `anchor`,
`forgotten_since_root` and `value_form` — the analytical facts — and never touches `cells`. So a columnar
family state that carries those facts is adjudicated by the authority that already exists, and the physical
substrate genuinely is realization. A test asserts the identity of the function object, because *"the kernel
remains analytical authority"* is a claim worth being unable to fake.

    ColumnarFamilyState  →  kernel.Retained  →  kernel.MME.adjudicate  →  Adequacy
                                                     ↑ unchanged

THE SORT DISTINCTION SURVIVES THE SUBSTRATE
-------------------------------------------
`ColumnarFamilyState` has `fold_onto_grouped` and `CONTINUATION_BEARING = True`.
`ColumnarExpressionOutput` has **no continuation path at all** and `CONTINUATION_BEARING = False`. Two
types, exactly as in the kernel, so an Arrow array of int64 estimates cannot become family state by being
the same physical shape as an Arrow array of int64 counts.

WANT OF STATE: THE TWO PLACES A VALUE IS *REQUIRED*
---------------------------------------------------
    *"Participation determines the contributing domain. Support determines whether the values required over
    that participating domain are established."* — Huayin, 2026-09-29

So an unsupported participating point is never removed from a fold; it makes the fold **refuse**. This module
asks that question in exactly two places, and they are the two places a value is actually required:

    `measure`      before a grouped continuation — a fold over a domain that is not established REFUSES
                   with `want-of-state`, naming the points and the target points affected.
    `_establish`   before any arithmetic — an expression whose basis role wants state REFUSES with
                   `basis-operand-wants-state`. *"AOV refuses because one required basis operand is not
                   established."*

**Holding is not serving**, so `establish` still records a column that has want of state — with a
`want-of-state` disclosure travelling on every answer that carries it — and `cell` refuses at the individual
point rather than handing back the carrier's null. A `COUNT` is untouched by any of this: it contributes
over participation and requires no value, so three participating Orders are three Orders whatever became of
their amounts.

WHAT IS NOT HERE
----------------
No persistence, no Iceberg, no Parquet, no Postgres, no refresh orchestration, no catalog, no constitution
builder. This is the in-memory columnar data plane and nothing else.

And no pointwise REPRESENTATION of want of state: it is a refusal at the operation, not a third mask value
and not a value in the carrier. Representing it per point — alongside `NA`, known-empty-versus-identity, and
resolved inapplicability — is the applicability/participation/support unit's business, and nothing here
anticipates it by inference from support.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any, Optional

import pyarrow as pa
import pyarrow.compute as pc

from columna_platform.kernel import (
    CACHED,
    CONTINUED,
    EVALUATED,
    MME,
    REFUSED,
    ROOT,
    STRUCTURED,
    Anchor,
    AnalyticalInstance,
    Answer,
    Disclosure,
    GovernedExpression,
    KernelRefusal,
    MeasureFamily,
    Refusal,
)
from columna_platform.kernel.mme import Retained, RetentionKey

from .block import GovernedBlock, value_column_name
from .index import AnchorInstance, CoordinateIndex
from .provider import ColumnarProvider, sketch_parameters
from .standing import ColumnStanding, POPULATION, VALUE_BEARING

#: Which reduction shape a law's own reduction is: a POPULATION law counts membership, everything else
#: needs evidence for a value. Declared here rather than on the law because it is a property of how a
#: provider must read the standing masks, not a semantic fact the law asserts.
_POPULATION_LAWS = frozenset({"COUNT"})


def _shape_of(law_name: str) -> str:
    """The reduction shape of a law. A `COUNT` needs membership; everything else needs values."""
    return POPULATION if law_name in _POPULATION_LAWS else VALUE_BEARING


@dataclass(frozen=True)
class ColumnarFamilyState:
    """**Continuation-bearing family state, carried as an Arrow column.**

    Duck-type compatible with what `kernel.MME.adjudicate` reads — `anchor`, `forgotten_since_root`,
    `value_form`, `CONTINUATION_BEARING` — which is what lets the kernel adjudicate columnar state without
    a line of columnar-specific law."""

    family_id: str
    anchor_instance: AnchorInstance
    values: pa.Array
    standing: ColumnStanding
    law: str
    value_form: str
    forgotten_since_root: frozenset = frozenset()
    disclosures: tuple[Disclosure, ...] = ()
    route: tuple[str, ...] = ()

    CONTINUATION_BEARING = True

    @property
    def anchor(self) -> Anchor:
        return self.anchor_instance.anchor

    @property
    def index(self) -> CoordinateIndex:
        return self.anchor_instance.index

    @property
    def instance(self) -> AnalyticalInstance:
        return self.anchor_instance.instance

    @property
    def at_root(self) -> bool:
        return not self.forgotten_since_root

    @property
    def point(self) -> Any:
        return _Point("family", self.family_id, self.anchor)

    def with_disclosure(self, d: Disclosure) -> "ColumnarFamilyState":
        return replace(self, disclosures=self.disclosures + (d,))

    @property
    def shape(self) -> str:
        """The reduction shape this state's own law has, and therefore what its standing must establish."""
        return _shape_of(self.law)

    @property
    def wants_state(self) -> bool:
        """**Does this state participate somewhere its required value is not established?**"""
        return self.standing.wants_state(self.shape)

    def points_wanting_state(self) -> tuple[tuple, ...]:
        return tuple(self.index.coordinates[i]
                     for i in self.standing.positions_wanting_state(self.shape))

    def cell(self, coordinate: tuple) -> Any:
        """One value, by coordinate. **REFUSES where the point has want of state.**

        A participating point whose required value is not established has no value to return, and returning
        the carrier's `None` there would hand a caller an absence to interpret — which is the whole thing
        the standing masks exist to prevent."""
        position = self.index.position(coordinate)
        if self.standing.want_of_state(self.shape)[position].as_py():
            raise KernelRefusal(
                "want-of-state-at-a-point", f"{self.family_id}@{self.anchor}",
                f"point {coordinate!r} PARTICIPATES in {self.family_id!r} and the value this "
                f"{self.shape} law requires there is not established. There is nothing to return: this is "
                f"want of state, and it is not `NA`, not zero, not a known-empty fibre, and not "
                f"nonparticipation. The carrier's null at this position means nothing.")
        return self.values[position].as_py()

    def __str__(self) -> str:
        return (f"ColumnarFamilyState({self.family_id}@{self.anchor}, {len(self.values)} positions, "
                f"{self.value_form})")


@dataclass(frozen=True)
class ColumnarExpressionOutput:
    """**A finalized expression result, carried as an Arrow column. NO continuation path exists on it.**

    The absence of `fold_onto_grouped` here is the primary enforcement, exactly as in the kernel. An Arrow
    `int64` array of HLL estimates and an Arrow `int64` array of order counts are physically
    indistinguishable; only the TYPE holding them says which may seed."""

    expression_id: str
    anchor_instance: AnchorInstance
    values: pa.Array
    constructor: str
    basis_id: Optional[str] = None
    disclosures: tuple[Disclosure, ...] = ()

    CONTINUATION_BEARING = False

    @property
    def anchor(self) -> Anchor:
        return self.anchor_instance.anchor

    @property
    def index(self) -> CoordinateIndex:
        return self.anchor_instance.index

    @property
    def instance(self) -> AnalyticalInstance:
        return self.anchor_instance.instance

    @property
    def point(self) -> Any:
        return _Point("expression", self.expression_id, self.anchor)

    def with_disclosure(self, d: Disclosure) -> "ColumnarExpressionOutput":
        return replace(self, disclosures=self.disclosures + (d,))

    def cell(self, coordinate: tuple) -> Any:
        return self.values[self.index.position(coordinate)].as_py()

    def __str__(self) -> str:
        return (f"ColumnarExpressionOutput({self.expression_id}@{self.anchor}, "
                f"{len(self.values)} positions, via {self.basis_id})")


@dataclass(frozen=True)
class _Point:
    sort: str
    identity: str
    anchor: Anchor

    @property
    def family_id(self) -> Optional[str]:
        return self.identity if self.sort == "family" else None

    @property
    def expression_id(self) -> Optional[str]:
        return self.identity if self.sort == "expression" else None

    def __str__(self) -> str:
        return f"{self.identity}@{self.anchor}"


class ColumnarMME:
    """The columnar data plane. **Authority is delegated to a `kernel.MME`, not re-implemented.**"""

    def __init__(self, authority: MME, provider: Optional[ColumnarProvider] = None) -> None:
        self.authority = authority
        self.provider = provider or ColumnarProvider()
        self._store: dict[RetentionKey, Retained] = {}

    # ── the delegated facts ──────────────────────────────────────────────────────────────────
    @property
    def manifold(self) -> str:
        return self.authority.manifold

    @property
    def universe(self):
        return self.authority.universe

    def family(self, family_id: str) -> MeasureFamily:
        return self.authority.family(family_id)

    def expression(self, expression_id: str) -> GovernedExpression:
        return self.authority.expression(expression_id)

    def sort_of(self, identity: str) -> Optional[str]:
        return self.authority.sort_of(identity)

    def law_of(self, identity: str):
        return self.authority.law_of(identity)

    @property
    def held(self) -> tuple[RetentionKey, ...]:
        return tuple(self._store)

    # ── establishment from a governed block ──────────────────────────────────────────────────
    def establish(self, block: GovernedBlock, family_id: str, *,
                  at_root: bool = True) -> ColumnarFamilyState:
        """Adopt one of a block's columns as this family's state at the block's anchor.

        **The standing comes from the BLOCK and never from the values.** Nothing here inspects
        `Array.is_valid()`; a position's contribution is decided by the governed masks."""
        family = self.family(family_id)
        law = self.law_of(family_id)
        if block.index.manifold != self.manifold:
            raise KernelRefusal(
                "foreign-manifold-block", family_id,
                f"the block's coordinate index belongs to Manifold {block.index.manifold!r} and this MME "
                f"is the jurisdiction of {self.manifold!r}. Shared physical infrastructure does not share "
                f"analytical authority: a block produced under one Manifold cannot establish state in "
                f"another, even at the same anchor with the same family name.")
        instance = block.instance(family_id)
        if instance != self.authority.instance_of(family_id):
            raise KernelRefusal(
                "block-instance-mismatch", family_id,
                f"the block carries {family_id!r} under analytical instance {instance} and this engine's "
                f"registered constitution gives {self.authority.instance_of(family_id)}. A block does not "
                f"get to declare a family's instance.")
        standing = block.standing(family_id)
        shape = _shape_of(law.name)
        values = block.column(family_id)
        # **THE ONE THING THE CARRIER IS ALLOWED TO CONTRADICT, AND IS NOT.** A null MEANS nothing — but a
        # position the standing declares SUPPORTED and the carrier has no value for is a broken
        # representation contract, and the engine will not pick which of the two to believe. Checked only
        # where the point participates and the law needs a value; elsewhere the carrier is irrelevant.
        if shape == VALUE_BEARING:
            claimed = pc.and_(standing.participation, standing.support).to_pylist()
            missing = [i for i, (c, v) in enumerate(zip(claimed, values.is_valid().to_pylist()))
                       if c and not v]
            if missing:
                raise KernelRefusal(
                    "support-without-a-value", family_id,
                    f"position(s) {missing} participate and are declared SUPPORTED for this "
                    f"{law.name}, and the carrier holds no value there. The standing and the carrier "
                    f"disagree and this engine will not choose between them: either the value is "
                    f"established and must be present, or it is not and support must say so — in which "
                    f"case the honest standing is want of state. Nothing here reads the null as `NA`, as "
                    f"zero, or as nonparticipation.")
        state = ColumnarFamilyState(
            family_id=family_id, anchor_instance=block.anchor_instance(family_id),
            values=values, standing=standing,
            law=law.name, value_form=law.value_form,
            forgotten_since_root=frozenset() if at_root
            else family.root.forgets(block.index.anchor),
            route=(f"established from {block} column {value_column_name(family_id)!r}",))
        # Recording a column is not serving a value: a state may HOLD want of state, and every answer
        # carrying it says so. What may not happen is a reduction or an expression using it as though the
        # missing values were not required — which is refused at both of those two places.
        if state.wants_state:
            state = state.with_disclosure(Disclosure(
                "want-of-state",
                f"{len(state.points_wanting_state())} participating point(s) of {family_id!r} have no "
                f"established value: {[list(p) for p in state.points_wanting_state()]}. The column is held "
                f"with that standing recorded; any {shape} reduction or basis role over this domain is "
                f"refused until the value is established. Not `NA`, not zero, not nonparticipation."))
        self.retain(state)
        return state

    # ── retention. Holding is never authority. ───────────────────────────────────────────────
    def retain(self, value: Any) -> Retained:
        key = RetentionKey(sort=value.point.sort, identity=value.point.identity,
                           anchor=value.anchor, instance=value.instance,
                           provider=self.provider.name)
        retained = Retained(key=key, value=value)
        self._store[key] = retained
        return retained

    def retained(self, sort: str, identity: str, anchor: Anchor,
                 instance: AnalyticalInstance) -> Optional[Retained]:
        return self._store.get(RetentionKey(sort, identity, anchor, instance, self.provider.name))

    def candidates(self, family_id: str) -> tuple[Retained, ...]:
        return tuple(r for r in self._store.values() if r.key.identity == family_id)

    # ── THE AUTHORITY, REUSED VERBATIM ───────────────────────────────────────────────────────
    def adjudicate(self, candidate: Retained, family: MeasureFamily, target: Anchor):
        """**`kernel.MME.adjudicate`, unchanged, over columnar state.**

        This one line is the architectural result of the unit: the five questions — sort, reachability,
        closure over the whole route from `R_F`, adequacy of the value, realization — are asked by the
        analytical authority, and the substrate does not get a vote. The laundering guard therefore holds
        here for free, because it is not reimplemented."""
        return self.authority.adjudicate(candidate, family, target)

    # ── serving a family, columnar ───────────────────────────────────────────────────────────
    def measure(self, family_id: str, anchor: Anchor, *, retain: bool = True) -> Answer:
        family = self.family(family_id)
        law = self.law_of(family_id)
        instance = self.authority.instance_of(family_id)
        considered: list[str] = []

        exact = self.retained("family", family_id, anchor, instance)
        if exact is not None and exact.continuation_bearing:
            return Answer(route=CACHED, value=exact.value, disclosures=exact.value.disclosures,
                          considered=(str(exact.key),))

        # least-work first, falling back toward the root — the kernel's own ordering rule
        pool = sorted((r for r in self.candidates(family_id) if r.key.instance == instance),
                      key=lambda r: len(r.key.anchor.constituents))
        blockers = []
        for candidate in pool:
            considered.append(str(candidate.key))
            verdict = self.adjudicate(candidate, family, anchor)
            if not verdict:
                blockers.append(verdict)
                continue
            state = candidate.value
            if state.anchor != anchor:
                # ── WANT OF STATE, BEFORE THE FOLD ────────────────────────────────────────────
                # *"Participation determines the contributing domain. Support determines whether the
                # values required over that participating domain are established."* — 2026-09-29.
                # A fold whose domain contains a participating point with no established value cannot
                # be performed: the lawful answer is a refusal that says what is missing, NOT a total
                # over the supported remainder. The candidate is not "unreachable" and the point is not
                # removed from the population — the value is owed and absent.
                if state.wants_state:
                    return Answer(route=REFUSED, considered=tuple(considered),
                                  refusal=self._want_of_state(state, anchor))
                state = self._continue(state, family, law, anchor)
            if law.approximation != "exact":
                state = state.with_disclosure(Disclosure(
                    "approximate", f"{law.name} is {law.approximation}; every value served from it "
                                   f"carries that standing"))
            if retain:
                self.retain(state)
            return Answer(route=ROOT if state.anchor == family.root else CONTINUED, value=state,
                          disclosures=state.disclosures, seeded_from=candidate.key,
                          considered=tuple(considered))

        best: dict[str, Any] = {}
        for b in blockers:
            if b.code not in best or len(b.detail) > len(best[b.code].detail):
                best[b.code] = b
        detail = (" · ".join(f"{b.code} — {b.detail}" for b in
                             sorted(best.values(), key=lambda b: b.code == "not-reachable"))
                  or f"no columnar state of {family_id} is held under this analytical instance; a value "
                     f"must be established at {family.root} before it can be continued anywhere")
        return Answer(route=REFUSED, considered=tuple(considered),
                      refusal=Refusal("unanswerable", f"{family_id}@{anchor}", detail))

    def _want_of_state(self, state: ColumnarFamilyState, target: Anchor) -> Refusal:
        """**The refusal a value-bearing reduction owes when its domain is not established.**

        It names the participating points whose values are missing and the target points that therefore
        cannot be folded — and it says explicitly what the refusal is NOT, because every one of those
        readings would be a governed fact the engine had decided on its own."""
        points = state.points_wanting_state()
        affected = sorted({target.project(p, state.anchor) for p in points}, key=lambda c: tuple(map(str, c)))
        return Refusal(
            "want-of-state", f"{state.family_id}@{target}",
            f"{len(points)} participating point(s) {[list(p) for p in points]} of {state.family_id!r} have "
            f"want of state: they are IN the contributing domain of this {state.shape} {state.law} and the "
            f"value it requires there is not established. The fold onto {target} is therefore refused at "
            f"target point(s) {[list(c) for c in affected]}. **THE REDUCTION HAS NOT RUN AND NO TOTAL IS "
            f"REPORTED.** Support validates the participating domain; it does not shrink it — so these "
            f"points were NOT dropped and a sum over the supported remainder would be a number about a "
            f"different population. This refusal is want of state ALONE: it is not `NA`, not a known-empty "
            f"fibre, not nonparticipation, and not a nonexistent point, and nothing here infers any of "
            f"them from support. A population reduction over the same points is unaffected and still "
            f"counts all {len(state.standing.participation.to_pylist())} of them that participate.")

    def _continue(self, state: ColumnarFamilyState, family: MeasureFamily, law,
                  target: Anchor) -> ColumnarFamilyState:
        """Grouped continuation through the provider, onto a governed target index."""
        target_index = self._target_index(state, target)
        shape = _shape_of(law.name)
        result = self.provider.continue_grouped(
            self._block_of(state), state.family_id, composition=law.continuation.token,
            target_index=target_index, shape=shape)
        return ColumnarFamilyState(
            family_id=state.family_id,
            anchor_instance=AnchorInstance(index=target_index, instance=state.instance),
            values=result.values, standing=result.standing, law=state.law,
            value_form=state.value_form,
            forgotten_since_root=state.forgotten_since_root | state.anchor.forgets(target),
            disclosures=state.disclosures,
            route=state.route + result.route)

    def _target_index(self, state: ColumnarFamilyState, target: Anchor) -> CoordinateIndex:
        """**The target index is DERIVED from the existing points, so sparse stays sparse.**

        The coarser anchor's points are exactly the projections of the finer anchor's CONTRIBUTING DOMAIN —
        no Cartesian product, no domain enumeration, and no point that nothing reached.

        **The domain is `participation` for both shapes**, so an unsupported participating point still puts
        its target point in this index. That matters: under the old `participation ∧ support` filter a target
        point reachable only from unsupported sources vanished from the geometry entirely, and the answer
        came back shaped as though that day had never existed."""
        contributing = state.standing.contributing_domain(state.shape).to_pylist()
        cells = {target.project(cell, state.anchor)
                 for cell, keep in zip(state.index.coordinates, contributing) if keep}
        return CoordinateIndex.of(self.manifold, target, cells)

    def _block_of(self, state: ColumnarFamilyState) -> GovernedBlock:
        return GovernedBlock.of(state.index, {state.family_id: state.values},
                                {state.family_id: state.standing})

    # ── evaluating an expression, positionally ───────────────────────────────────────────────
    def evaluate(self, expression_id: str, anchor: Anchor, *,
                 basis_id: Optional[str] = None, retain: bool = True) -> Answer:
        expression = self.expression(expression_id)
        law = self.law_of(expression_id)
        instance = self.authority.instance_of(expression_id)

        exact = self.retained("expression", expression_id, anchor, instance)
        if exact is not None and not exact.continuation_bearing:
            return Answer(route=CACHED, value=exact.value, disclosures=exact.value.disclosures)

        routes = ([b for b in expression.admitted_bases if b.basis_id == basis_id]
                  if basis_id else list(expression.admitted_bases))
        if not routes:
            return Answer(route=REFUSED, refusal=Refusal(
                "no-admitted-basis", f"{expression_id}@{anchor}",
                "this expression admits no sufficient basis: well-formed and not evaluable."))

        failures = []
        for basis in routes:
            attempt = self._establish(expression, law, basis, anchor)
            if attempt.served:
                if retain:
                    self.retain(attempt.value)
                return Answer(route=EVALUATED, value=attempt.value,
                              disclosures=attempt.value.disclosures, seeded_from=basis.basis_id)
            # the INNER code rides in the wrapped detail: a caller branching on "why did every
            # route fail" needs the per-route code, not only the outer one.
            failures.append(f"basis {basis.basis_id!r} [{attempt.refusal.code}]: "
                            f"{attempt.refusal.detail}")
        return Answer(route=REFUSED, refusal=Refusal(
            "no-sufficient-basis-establishes", f"{expression_id}@{anchor}",
            " | ".join(failures) + ". Physical availability is not analytical authority."))

    def _establish(self, expression: GovernedExpression, law, basis, anchor: Anchor) -> Answer:
        subject = f"{expression.expression_id}@{anchor} via {basis.basis_id}"
        states: dict[str, ColumnarFamilyState] = {}
        for role in basis.component_laws:
            served = self.measure(basis.components[role], anchor)
            if not served.served:
                return Answer(route=REFUSED, refusal=Refusal(
                    "role-unfilled", subject,
                    f"role {role!r} is filled by {basis.components[role]!r}, which cannot be served at "
                    f"{anchor}: {served.refusal.detail}"))
            states[role] = served.value

        # ── ALIGNMENT AND COMPATIBILITY, BOTH BEFORE ANY ARITHMETIC ──────────────────────
        roles = list(states)
        reference = states[roles[0]]
        for role in roles[1:]:
            other = states[role]
            if reference.index.identity != other.index.identity:
                return Answer(route=REFUSED, refusal=Refusal(
                    "layouts-differ", subject,
                    f"roles {roles[0]!r} and {role!r} are laid out on different coordinate indexes "
                    f"({reference.index.identity} vs {other.index.identity}). A positional kernel needs "
                    f"one layout, and this path will NOT discover the correspondence by joining the two "
                    f"columns on their coordinate values — that would be relational discovery of "
                    f"analytical alignment. An explicit alignment against a governed target index is the "
                    f"lawful remedy."))
            if basis.requires_common_participation:
                agreement = reference.instance.compatible_with(other.instance)
                if not agreement:
                    return Answer(route=REFUSED, refusal=Refusal(
                        "incompatible-basis", subject,
                        f"roles {roles[0]!r} and {role!r} are position-aligned on ONE coordinate index and "
                        f"are not jointly usable [{agreement.code}]: {agreement.detail}. **THE ARITHMETIC "
                        f"HAS NOT RUN.** Both columns are present, the same length, and perfectly "
                        f"aligned; what is missing is analytical authority to combine them, and no amount "
                        f"of physical readiness supplies it."))

        # ── AND ONLY THEN: IS EVERY REQUIRED OPERAND ESTABLISHED OVER ITS DOMAIN? ─────────
        # Deliberately AFTER compatibility: authority to combine two columns is prior to the evidence
        # for their values, so a jointly-unusable basis refuses on participation even when it also
        # wants state. What this check catches is the basis that is lawful and still not computable —
        # *"AOV refuses because one required basis operand is not established."* (2026-09-29)
        for role, state in states.items():
            if state.wants_state:
                return Answer(route=REFUSED, refusal=Refusal(
                    "basis-operand-wants-state", subject,
                    f"role {role!r} is filled by {state.family_id!r}, which has want of state at "
                    f"{[list(p) for p in state.points_wanting_state()]}: those points participate and the "
                    f"value this basis requires of them is not established. **THE ARITHMETIC HAS NOT "
                    f"RUN.** One required basis operand is not established, so the expression is refused — "
                    f"it is NOT evaluated over the subset of points whose operands happen to be supported, "
                    f"and the other role(s) "
                    f"{[r for r in states if r != role]} are unaffected in their own right: a population "
                    f"operand still counts every participating point. Establish the missing value, or "
                    f"admit a basis that does not require it."))

        kernel = "ratio" if law.name == "MEAN" else "hll_estimate"
        values = self.provider.evaluate_positional(
            {role: states[role].values for role in states}, kernel=kernel)
        output = ColumnarExpressionOutput(
            expression_id=expression.expression_id,
            anchor_instance=AnchorInstance(index=reference.index,
                                           instance=self.authority.instance_of(
                                               expression.expression_id)),
            values=values, constructor=law.name, basis_id=basis.basis_id)
        for state in states.values():
            for d in state.disclosures:
                output = output.with_disclosure(d)
        undefined = values.null_count
        if undefined:
            output = output.with_disclosure(Disclosure(
                "undefined-on-basis",
                f"{undefined} position(s) carry no value: the basis is established there and the "
                f"expression is UNDEFINED on it (ToD v8 §4.3). Distinct from absent and from zero — and "
                f"note that this null is PRODUCED BY THE KERNEL as a governed standing, not read as one."))
        if any(s.value_form == STRUCTURED for s in states.values()):
            params = {role: sketch_parameters(s.values[0].as_py())
                      for role, s in states.items() if s.value_form == STRUCTURED
                      and len(s.values) and s.values[0].as_py() is not None}
            if params:
                output = output.with_disclosure(Disclosure(
                    "sketch-parameters",
                    f"finalized from structured state with parameters {params}. Sketch parameters are "
                    f"COMPATIBILITY-BEARING: two sketches of different lg_k are not mergeable."))
        return Answer(route=EVALUATED, value=output)


__all__ = ["ColumnarExpressionOutput", "ColumnarFamilyState", "ColumnarMME"]
