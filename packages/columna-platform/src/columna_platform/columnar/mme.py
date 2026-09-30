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

**WHOLE-COLUMN REFUSAL IS THIS SERVING PROFILE'S LIMITATION AND NOT ToD SEMANTICS** (ruled Huayin,
2026-09-29; recorded as `DG-7` in `specs/doctrine_gaps.md`):

    *"Whole-column refusal is a current Platform/profile limitation, not ToD semantics… Later we may
    represent, for example: D1 → want of state, D2 → established value, without invalidating the whole
    analytical column. Do not let 'one unsupported target means whole-column refusal' become family
    doctrine."*

`Revenue@{day}` refuses entirely here even though `D2`'s fold is fully established, because a columnar family
state is one value array plus two masks and has **nowhere to put "this point wants state"** in what it
serves. Want of state is owed POINTWISE; refusing the whole request is the conservative thing available to a
surface that cannot carry it, which is why the refusal names the affected target points. When a result
surface can represent per-point standing, the remedy is that surface — **not** a weakening of the refusal,
and not a rule that a column dies with one point.

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

import time

from dataclasses import dataclass, replace
from typing import Any, Optional

import pyarrow as pa
import pyarrow.compute as pc

from columna_platform.kernel import (
    CACHED,
    CONTINUED,
    MME,
    REFUSED,
    ROOT,
    Anchor,
    AnalyticalInstance,
    Answer,
    Disclosure,
    GovernedExpression,
    KernelRefusal,
    MeasureFamily,
    Refusal,
)
from columna_platform.kernel import RealizationStanding, UNSTATED_DATA_STATE
from columna_platform.kernel.materialization import (
    AT_ROOT,
    CONTINUED as CONTINUED_FROM,
    CURRENT,
    INDEPENDENT,
    SUPERSEDED,
    Admission,
    Establishment,
    FamilyMaterialization,
    MaterializationId,
    MaterializationStore,
    TransitionIntent,
)
from columna_platform.kernel.mme import Retained, RetentionKey, Staleness
from columna_platform.kernel.observation import (
    FamilyRequest,
    Fulfillment,
    ObservationSink,
    READY,
    WANT_OF_STATE,
    NEED,
    WorkloadObserver,
    disposition_for,
    observe_request,
)

from .block import GovernedBlock, value_column_name
from .index import AnchorInstance, CoordinateIndex
from .provider import ColumnarProvider
from .standing import ColumnStanding, VALUE_BEARING

# **A RETIRED CLAIM, CORRECTED (B-0b).** This module used to say the reduction shape was *"declared here
# rather than on the law because it is a property of how a provider must read the standing masks, not a
# semantic fact the law asserts."* That was wrong in both halves. Whether a reduction reads values or only
# membership is exactly a semantic fact — it is why `OrderCount` serves 3 at D1 where `Revenue` wants state
# over the same seven orders — and a provider reading masks is the CONSEQUENCE of it, not its home.
# `_POPULATION_LAWS = frozenset({"COUNT"})` and `_shape_of(law_name)` lived here and are GONE (B-0b).
#
#     *"MME must not hardcode `COUNT → population-shaped` or any equivalent law-name enumeration. The
#     authorized request should carry the already-resolved fold shape."*  — Huayin, 2026-09-29
#
# They were a cache engine deciding, from a hardcoded set of law NAMES, what a reduction contributes over —
# constitutional knowledge in the one component ruled to hold none. Relocating the set would have satisfied
# the letter and kept the defect, so instead the fact moved to where it belongs: `AnalyticalLaw.fold_shape`
# is DECLARED (`COUNT` says `POPULATION` of itself), it enters every family's `ConstitutionWitness` by
# subtraction, and this engine now reads it off the state it holds or the authorized request it was handed.


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
    #: **What this state's reduction contributes over**, carried rather than inferred (B-0b). Set from the
    #: law's own declaration by whoever had the law; this engine never maps a law NAME onto a shape.
    fold_shape: str = VALUE_BEARING
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
        """The reduction shape this state's own law declared, and therefore what its standing must
        establish. **Carried, not derived from the law's name** (B-0b)."""
        return self.fold_shape

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

    def __init__(self, authority: MME, provider: Optional[ColumnarProvider] = None, *,
                 carrier: str = "in-memory-arrow",
                 observer: Optional[WorkloadObserver] = None) -> None:
        self.authority = authority
        self.provider = provider or ColumnarProvider()
        #: **Realization standing** — the third of P-1's three facts, and an axis of the key alone. The
        #: carrier is named separately from the provider so that "the same value, carried differently" is
        #: representable without touching either the constitution witness or the analytical instance.
        self.realization = RealizationStanding(provider=self.provider.name, carrier=carrier)
        #: **The columnar engine's own family-materialization cache**, under the authority's build. Its own,
        #: because this engine holds different material; the authority's build, because a cache belongs to
        #: one semantic world and `constitution_context = ManifoldBuildId`.
        self.build = authority.build
        self.materializations = authority.attach_store(MaterializationStore(self.build))
        #: **The workload observation seam** (ruled M-2 §4). Its OWN sink, not the authority's: this engine
        #: is a distinct request boundary serving distinct material, and merging the two logs would make
        #: "which substrate answered" unrecoverable from a record whose whole purpose is cost.
        self.observations = ObservationSink(observer)

    # ── the delegated facts ──────────────────────────────────────────────────────────────────
    @property
    def manifold(self) -> str:
        return self.authority.manifold

    @property
    def universe(self):
        return self.authority.universe

    def family(self, family_id: str) -> MeasureFamily:
        return self.authority.family(family_id)

    def subject(self, family_or_id: Any) -> MeasureFamily:
        """One family, however the caller named it. Delegated — the registry is the authority's."""
        return self.authority.subject(family_or_id)

    def expression(self, expression_id: str) -> GovernedExpression:
        return self.authority.expression(expression_id)

    def sort_of(self, identity: str) -> Optional[str]:
        return self.authority.sort_of(identity)

    def law_of(self, identity: str):
        return self.authority.law_of(identity)

    @property
    def held(self) -> tuple[RetentionKey, ...]:
        """Descriptors of everything held. A descriptor REPORTS the analytical attributes; it is not an
        identity and nothing is looked up by it — a materialization is located by its opaque id."""
        return tuple(self._descriptor(m) for m in self.materializations.all())

    def holdings(self) -> tuple[Retained, ...]:
        return tuple(Retained(key=self._descriptor(m), value=m.value)
                     for m in self.materializations.all() if m.has_payload)

    def materialization(self, mid: MaterializationId) -> Optional[FamilyMaterialization]:
        return self.materializations.get(mid)

    def _descriptor(self, m: FamilyMaterialization) -> RetentionKey:
        return RetentionKey(identity=m.family_id, anchor=m.anchor,
                            instance=m.instance, realization=m.realization,
                            constitution=m.build.reference)

    # ── establishment from a governed block ──────────────────────────────────────────────────
    def establish(self, block: GovernedBlock, family_id: str, *,
                  at_root: bool = True,
                  data_state: str = UNSTATED_DATA_STATE,
                  intent: Optional[TransitionIntent] = None) -> ColumnarFamilyState:
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
        declared = self.authority.instance_of(family_id)
        instance = block.instance(family_id)
        if not instance.same_but_for_data_state(declared):
            raise KernelRefusal(
                "block-instance-mismatch", family_id,
                f"the block carries {family_id!r} under analytical instance {instance} and this engine's "
                f"registered constitution gives {declared}. A block does not get to declare a family's "
                f"instance. **WHAT A BLOCK MAY DECLARE IS THE DATA STATE** — which established material it "
                f"carries — and that is passed to `establish`, not read off the standing; every governed "
                f"axis must agree with the registered declaration.")
        standing = block.standing(family_id)
        shape = law.fold_shape
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
        # **THE ONE PLACE THE EVIDENCE STATE IS STAMPED.** The constitution witness comes from the
        # registered declaration and the realization from the provider; what establishment contributes is
        # which established material this is — the third axis, set here and nowhere else.
        anchor_instance = replace(block.anchor_instance(family_id),
                                  instance=declared.with_data_state(data_state))
        at_the_root = block.index.anchor == family.root
        state = ColumnarFamilyState(
            family_id=family_id, anchor_instance=anchor_instance,
            values=values, standing=replace(standing, instance=anchor_instance.instance),
            law=law.name, value_form=law.value_form, fold_shape=law.fold_shape,
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
        admission = self.admit(state, intent=intent, establishment=Establishment(
            AT_ROOT if at_the_root else INDEPENDENT))
        if not admission:
            raise KernelRefusal(admission.code, family_id, admission.detail)
        return state

    def stale_states(self) -> tuple[Staleness, ...]:
        """**Which materializations stopped being current because a declaration moved**, asked of the
        authority. Not reimplemented here for the same reason `adjudicate` is not: whether a constitution
        has moved is an analytical question, and the substrate does not get a second opinion about it."""
        return self.authority.stale_states()

    # ── admission. Holding is never authority. ───────────────────────────────────────────────
    def admit(self, value: Any, *, establishment: Optional[Establishment] = None,
              intent: Optional[TransitionIntent] = None, residency: str = "resident",
              note: str = "") -> Admission:
        """**Offer one columnar family value to the cache.** Mints a standing, then `put`s.

        The kernel twin's docstring applies verbatim, including why this method is the authority half's.
        The constitutional reading is the SHARED authority's: `self.authority` is the kernel engine, so both
        engines authorize through one `ContinuationAuthority` over one constitution. Two caches, one
        Manifold — which is the right shape, because a family's lawful anchors cannot depend on which
        substrate is holding its values."""
        authorized = self.authority.authorizer.authorize_standing(
            value.point.identity, value.anchor)
        if not authorized:
            return Admission(False, code=authorized.refusal.code, detail=authorized.refusal.detail)
        return self.put(value, authorized.request, establishment=establishment, intent=intent,
                        residency=residency, note=note)

    def put(self, value: Any, standing: Any, *, establishment: Optional[Establishment] = None,
            intent: Optional[TransitionIntent] = None, residency: str = "resident",
            note: str = "") -> Admission:
        """**THE COLUMNAR CACHE DOOR. No constitution is read here.**

        Identical in substance to `kernel.MME.put`; see that docstring for why each check is a comparison
        rather than an interpretation. The only columnar difference is that identity is read as
        `value.point.identity`, because `_Point` is a three-field record whose `family_id` is derived."""
        family_id = value.point.identity
        if standing.family_id != family_id or standing.anchor != value.anchor:
            return Admission(
                False, code="standing-does-not-cover-this-material",
                detail=f"the authorization covers {standing.subject} and the material offered is "
                       f"{family_id}@{value.anchor}. An authorization is for one analytical location.")
        if establishment is None:
            establishment = Establishment(AT_ROOT if standing.at_root else INDEPENDENT)
        return self.materializations.admit(
            point=value.point, instance=value.instance, value=value, establishment=establishment,
            realization=self.realization, intent=intent, residency=residency, note=note)

    def retain(self, value: Any) -> Retained:
        """Hold one **governed columnar family value**, and nothing else (ruled M-2 §1).

        The expression branch that used to be here — and the keyed `_store` it wrote into — are gone. A
        `ColumnarExpressionOutput` offered here is refused by a governed reason, not by an obscure failure
        two calls later."""
        if value.point.sort != "family":
            raise KernelRefusal(
                "not-a-family-materialization", str(value.point.identity),
                f"{value.point} is an EXPRESSION output and this engine manages family materializations "
                f"only (M-2 §1). There is no expression store here to put it in: MME v1 does not cache "
                f"`E@A`, and a columnar expression is re-evaluated from a sufficient basis by "
                f"`columnar.expression.ColumnarExpressionEvaluator`, above this engine.")
        admission = self.admit(value)
        if not admission:
            raise KernelRefusal(admission.code, value.point.identity, admission.detail)
        return Retained(key=self._descriptor(self.materializations.get(admission.id)), value=value)

    def retained(self, family_id: str, anchor: Anchor,
                 instance: AnalyticalInstance) -> Optional[Retained]:
        """The CURRENT columnar materialization at this point, if one is held.

        **THE `sort` PARAMETER IS GONE** (M-2 §2). It existed to dispatch between two stores; there is one
        store, and it holds families."""
        held = self.materializations.select(family_id, anchor=anchor, instance=instance,
                                            serviceable=True)
        if not held:
            return None
        best = min(held, key=lambda m: (-m.admitted_seq,))
        return Retained(key=self._descriptor(best), value=best.value)

    def candidates(self, family_id: str) -> tuple[Retained, ...]:
        return tuple(Retained(key=self._descriptor(m), value=m.value)
                     for m in self.materializations.select(family_id, eligibility=None)
                     if m.has_payload)

    # ── THE AUTHORITY, REUSED VERBATIM ───────────────────────────────────────────────────────
    def adjudicate(self, candidate: Retained, request: Any):
        """**`kernel.MME.adjudicate`, unchanged, over columnar state.**

        This one line is still the architectural result: the questions are asked by one implementation and
        the substrate does not get a vote. **What changed at B-0b is that there are now FOUR of them, not
        five** — sort, reachability, payload adequacy, build capability. The fifth was closure over the route
        from `R_F`, and it is gone from both engines because no authorized request exists where it would
        fail. The laundering guard still holds here for free, and now for a stronger reason: it is not
        reimplemented AND it is not applied — it is upstream of the request."""
        return self.authority.adjudicate(candidate, request)

    # ── serving a family, columnar ───────────────────────────────────────────────────────────
    def requirement_for(self, family: Any, target: Anchor, *, data_state: Optional[str] = None,
                        note: str = ""):
        """**What governed family state would satisfy a request here?** Delegated to the authority, which
        is where analytical requirements are stated (R-1 §2).

        It exists on this engine so that a consumer above the two substrates never has to reach through
        `.authority` — reaching through would be a component knowing which engine it holds."""
        return self.authority.requirement_for(family, target, data_state=data_state, note=note)

    def measure(self, family_id: Any, anchor: Anchor, *, retain: bool = True,
                data_state: Optional[str] = None, on_behalf_of: str = "") -> Answer:
        """**Serve `F@A` over columnar state: authorize, then fulfill.** The kernel twin's shape exactly.

        **EITHER SPELLING** — see `kernel.MME.subject`. The two engines' `measure` signatures had diverged
        (`MeasureFamily` here, `family_id` there), so no component above both could call either without
        knowing which engine it held."""
        started_ns = time.perf_counter_ns()
        authorized = self.authority.authorizer.authorize(
            family_id, anchor, data_state=data_state, retain=retain, on_behalf_of=on_behalf_of)
        if not authorized:
            # See the kernel twin: the request boundary observes an unauthorized continuation as
            # UNSUPPORTED, and never as a cache miss.
            subject = self.authority.subject(family_id)
            observe_request(
                self.observations,
                FamilyRequest(manifold=self.manifold, build=self.build.reference,
                              family_id=subject.family_id, target=anchor, data_state=data_state,
                              on_behalf_of=on_behalf_of),
                started_ns=started_ns, route=REFUSED,
                refusal_code=authorized.refusal.code,
                disposition=disposition_for(authorized.refusal.code),
                fulfillment=Fulfillment(considered=0))
            return Answer(route=REFUSED, refusal=authorized.refusal)
        return self.fulfill(authorized.request)

    def fulfill(self, request: Any) -> Answer:
        """**Can this ALREADY-AUTHORIZED continuation be performed from columnar state held here?**

        Exactly one `RequestObservation` per call, on every path. The columnar engine is where
        `WANT_OF_STATE` actually arises as a disposition: a fold whose participating domain contains a point
        with no established value is not a cache miss, and a policy told it was one would try to solve an
        evidence problem with residency.

        Reads no constitution: no `region`, no `admits`, no law-name enumeration. The fold's shape and its
        composition arrive on the request."""
        started_ns = time.perf_counter_ns()
        anchor, family_id = request.target, request.family_id
        family = self.authority.subject(family_id)
        observed = FamilyRequest(manifold=self.manifold, build=request.build,
                                 family_id=family_id, target=anchor,
                                 data_state=request.data_state, on_behalf_of=request.on_behalf_of)
        considered: list[str] = []

        # **CANDIDATE SELECTION IS THE MME'S, NEVER THE CALLER'S** (ruled 2026-09-29 §2). Only CURRENT,
        # payload-bearing materializations are candidates; the cheapest lawful one answers.
        pool = self.materializations.candidates_for(family_id, anchor, request.instance,
                                                   data_state=request.data_state)

        exact = next((m for m in pool if m.anchor == anchor), None)
        if exact is not None:
            observe_request(self.observations, observed, started_ns=started_ns, route=CACHED,
                            disposition=READY,
                            fulfillment=Fulfillment(directly_held=True, selected=(exact.id,),
                                                    considered=1))
            return Answer(route=CACHED, value=exact.value, disclosures=exact.value.disclosures,
                          considered=(str(self._descriptor(exact)),))

        blockers = []
        for materialization in pool:
            candidate = Retained(key=self._descriptor(materialization), value=materialization.value)
            considered.append(str(candidate.key))
            verdict = self.adjudicate(candidate, request)
            if not verdict:
                blockers.append(verdict)
                continue
            state = candidate.value
            if state.anchor != anchor:
                # ── WANT OF STATE, BEFORE THE FOLD ────────────────────────────────────────────
                # *"Participation determines the contributing domain. Support determines whether the
                # values required over that participating domain are established."* — 2026-09-29.
                # A fold whose domain contains a participating point with no established value cannot be
                # performed: the lawful answer is a refusal that says what is missing, NOT a total over
                # the supported remainder.
                #
                # **AND THIS IS A CACHE/EXECUTION FACT, NOT AN ANALYTICAL ONE** (B-0b §2). The continuation
                # is authorized; what is absent is evidence the fold needs. The engine reads the SUPPORT
                # VECTOR it was given and never asks why that vector says what it says — whether carrier
                # validity was licensed to establish it is the realization boundary's question, above.
                if state.wants_state:
                    observe_request(self.observations, observed, started_ns=started_ns, route=REFUSED,
                                    refusal_code="want-of-state", disposition=WANT_OF_STATE,
                                    fulfillment=Fulfillment(selected=(materialization.id,),
                                                            seeded_from=materialization.anchor,
                                                            considered=len(considered)))
                    return Answer(route=REFUSED, considered=tuple(considered),
                                  refusal=self._want_of_state(state, anchor))
                state = self._continue(state, request, anchor)
            # **CONDITIONS ARE PROPAGATED, NEVER DERIVED** (B-0b). `law.approximation` was read here to
            # author an `approximate` disclosure — a cache asserting an analytical fact about a law.
            for condition in request.conditions:
                state = state.with_disclosure(condition)
            admitted: tuple[MaterializationId, ...] = ()
            if request.retain:
                # the dependency edge, recorded where the continuation happens and nowhere else; retained
                # under the standing the authorization already paired with this target
                admission = self.put(state, request.standing, establishment=(
                    Establishment(CONTINUED_FROM, (materialization.id,))
                    if state.anchor != materialization.anchor else Establishment(AT_ROOT)))
                if not admission:
                    observe_request(self.observations, observed, started_ns=started_ns, route=REFUSED,
                                    refusal_code=admission.code,
                                    fulfillment=Fulfillment(selected=(materialization.id,),
                                                            considered=len(considered)))
                    return Answer(route=REFUSED, considered=tuple(considered),
                                  refusal=Refusal(admission.code, f"{family_id}@{anchor}",
                                                  admission.detail))
                admitted = (admission.id,)
            route = ROOT if state.anchor == family.root else CONTINUED
            observe_request(self.observations, observed, started_ns=started_ns, route=route,
                            disposition=READY,
                            fulfillment=Fulfillment(
                                directly_held=False, selected=(materialization.id,),
                                seeded_from=materialization.anchor,
                                folded=len(candidate.value.index) or None,
                                considered=len(considered), admitted=admitted))
            return Answer(route=route, value=state,
                          disclosures=state.disclosures, seeded_from=candidate.key,
                          considered=tuple(considered))

        # **THE MISS, AND IT CARRIES NO ANALYTICAL MEANING** (ruled §7). It means exactly one thing: this
        # cache cannot currently satisfy an already-lawful request from the columnar state it holds. An
        # unlawful target never arrives here at all — it has no authorized request — so a miss can no longer
        # be confused with a governed refusal, which is the confusion the old single path allowed.
        best: dict[str, Any] = {}
        for b in blockers:
            if b.code not in best or len(b.detail) > len(best[b.code].detail):
                best[b.code] = b
        ordered = sorted(best.values(), key=lambda b: b.code == "not-reachable")
        detail = (" · ".join(f"{b.code} — {b.detail}" for b in ordered)
                  or f"no columnar state of {family_id} is held under this analytical instance; a value "
                     f"must be established at {family.root} before it can be continued anywhere"
                  ) + self._also_held(family_id)
        # WHICH KIND of miss — NEED (retention would have helped) versus UNSUPPORTED (this build cannot
        # execute the composition and never will). See the same note in `kernel.MME.fulfill`.
        blocking = ordered[0].code if ordered else ""
        observe_request(self.observations, observed, started_ns=started_ns, route=REFUSED,
                        refusal_code=blocking or "unanswerable",
                        disposition=(disposition_for(blocking) if blocking else NEED),
                        fulfillment=Fulfillment(considered=len(considered)))
        return Answer(route=REFUSED, considered=tuple(considered),
                      refusal=Refusal("unanswerable", f"{family_id}@{anchor}", detail))

    def _also_held(self, family_id: str) -> str:
        """What IS held and could not answer, so a refusal never pretends the cache is empty."""
        parts = []
        not_current = self.materializations.select(family_id, eligibility=SUPERSEDED)
        if not_current:
            parts.append(f"{len(not_current)} retained materialization(s) of {family_id!r} are held and are "
                         f"NOT CURRENT (superseded): {[f'{m.id}@{m.anchor}' for m in not_current]}. "
                         f"Residency never creates analytical authority.")
        unusable = [m for m in self.materializations.select(family_id, eligibility=CURRENT)
                    if not m.serviceable]
        if unusable:
            parts.append(f"{len(unusable)} current materialization(s) are unusable by POLICY "
                         f"({[f'{m.id}:{m.residency}' for m in unusable]}). That is OUR absence, not the "
                         f"world's: the remedy is to establish the state again.")
        return (" " + " ".join(parts)) if parts else ""

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

    def _continue(self, state: ColumnarFamilyState, request: Any,
                  target: Anchor) -> ColumnarFamilyState:
        """Grouped continuation through the provider, onto a governed target index.

        **BOTH EXECUTION FACTS ARRIVE ON THE REQUEST** (B-0b), and neither is looked up here. The
        composition token is the GROUPED capability key — the provider's table is keyed by it, which is why
        `SUM`, `COUNT` and `STOCK_LEVEL` share one `addition` capability instead of inventing three — and
        the fold shape is the law's own declaration. This method used to take the law and read
        `law.continuation.token` plus a law-name-to-shape mapping; it now takes neither."""
        target_index = self._target_index(state, target)
        result = self.provider.continue_grouped(
            self._block_of(state), state.family_id, composition=request.fold.composition,
            target_index=target_index, shape=request.fold.fold_shape)
        return ColumnarFamilyState(
            family_id=state.family_id,
            anchor_instance=AnchorInstance(index=target_index, instance=state.instance),
            values=result.values, standing=result.standing, law=state.law,
            value_form=state.value_form, fold_shape=state.fold_shape,
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
        # The standing is re-stamped with the state's own instance so a continuation's result carries the
        # evidence state it was folded FROM. A block assembled here is scratch material for one provider
        # call; it must not silently become the place a data state is lost.
        return GovernedBlock.of(state.index, {state.family_id: state.values},
                                {state.family_id: replace(state.standing, instance=state.instance)})

    # ── evaluating an expression — NOT HERE ANY MORE ─────────────────────────────────────────
    #
    # `evaluate` and `_establish` moved OUT in M-2, to `columnar.expression.ColumnarExpressionEvaluator`.
    # Ruled §1: expressions *"consume family state supplied by MME and are evaluated above it."* No
    # delegating shim is left behind — see the same note in `kernel.mme`, and for the same reason.

__all__ = ["ColumnarExpressionOutput", "ColumnarFamilyState", "ColumnarMME"]
