"""
test_r1_realization_manager_interface.py — **R-1: the Realization Manager interface, and only the
interface.**

    **MME says what governed family state is needed. Realization says what governed family state the
    physical estate can supply. The later Fulfillment Coordinator will decide how to combine those two
    answers.**  — Huayin, 2026-09-29

The ruling's stop-condition letters are the sections:

    A  the final `RealizationRequest` shape
    B  the final capability/proposal shape
    C  the final realized-offer shape
    D  proof that realized state enters ordinary `MME.admit`
    E  proof that backend/provider capability cannot bypass family law
    F  how `NEED` maps into realization requirements
    G  how multiple possible realization anchors/providers are represented WITHOUT choosing among them

WHAT IS NOT EXERCISED, DELIBERATELY: no actual backend, no ADBC, no Fulfillment Coordinator, no cost
model, no provider ranking, no persistence, no Iceberg/Postgres, no expression caching. Ruled out by name.
The providers below are **test doubles** and live here rather than in `src/` precisely so that nothing
shipped can be mistaken for a backend.
"""
from __future__ import annotations

from dataclasses import FrozenInstanceError, fields, replace

import pyarrow as pa
import pytest

from columna_platform.columnar import exhibit as CEX
from columna_platform.kernel import (
    IN_MEMORY,
    MME,
    REGISTRY,
    FamilyRequirement,
    KernelRefusal,
    ProposalSet,
    RealizationManager,
    RealizationOffer,
    RealizationProposal,
    RealizationStanding,
    RecordingObserver,
    RequirementOutcome,
    requirement_from,
)
from columna_platform.kernel import exhibit as KEX
from columna_platform.kernel import mme as kernel_mme_module
from columna_platform.kernel import requirement as requirement_module
from columna_platform.kernel.materialization import CONTINUED, INDEPENDENT, Establishment
from columna_platform.kernel.observation import NEED, READY, UNSUPPORTED, WANT_OF_STATE
from columna_platform.kernel.value import FamilyState


# ══ TEST DOUBLES — not backends, and they live here so they cannot be mistaken for one ════════════
class StaticEstate:
    """**A provider that holds pre-built family state in a dict.**

    It is a stand-in for *"somewhere out there this can be obtained"* and nothing more: no connection, no
    query, no ADBC, no I/O. Its `handle` is a dict key, which is exactly the point of `handle` being opaque
    — a real provider would put a query id or a file reference there and the manager would treat it
    identically, because the manager never looks at it."""

    def __init__(self, name: str, holdings: dict, *, carrier: str = "in-memory"):
        self.name = name
        self.holdings = holdings                     # {(family_id, anchor): value}
        self.carrier = carrier
        self.proposed = 0
        self.realized = 0

    @property
    def standing(self) -> RealizationStanding:
        return RealizationStanding(provider=self.name, carrier=self.carrier)

    def propose(self, requirement):
        self.proposed += 1
        for (family_id, anchor), value in self.holdings.items():
            if family_id != requirement.family_id:
                continue
            yield RealizationProposal(
                provider=self.name, family_id=family_id, anchor=anchor,
                value_form=getattr(value, "value_form", ""), realization=self.standing,
                handle=(family_id, anchor),
                diagnostics=f"{self.name} holds this at {anchor}")

    def realize(self, proposal):
        self.realized += 1
        value = self.holdings[proposal.handle]
        return RealizationOffer(
            provider=self.name, family_id=proposal.family_id, anchor=proposal.anchor,
            value=value, instance=value.instance, realization=self.standing,
            establishment=Establishment(INDEPENDENT), from_proposal=proposal,
            diagnostics=proposal.diagnostics)


class SilentEstate:
    """Offers nothing, ever. A fact about the estate, not an absence of one."""

    name = "silent"

    def propose(self, requirement):
        return ()

    def realize(self, proposal):                                     # pragma: no cover - unreachable
        raise AssertionError("nothing was proposed")


class BrokenEstate:
    """Raises while being ASKED. Capability discovery is advisory; one unreachable provider must not make
    the others invisible."""

    name = "broken"

    def propose(self, requirement):
        raise ConnectionError("the estate is unreachable")

    def realize(self, proposal):                                     # pragma: no cover - unreachable
        raise AssertionError("nothing was proposed")


def _code_only(module) -> str:
    """**The executable text of a module, with every docstring and comment removed.**

    The structural tests below are about what the code DOES, and a naive `inspect.getsource` search finds
    the prose explaining why it does not do it — this file's first draft failed on its own docstrings.
    Stripping them is not a weakening: a ban that a comment can trip is a ban nobody can write about."""
    import ast
    import inspect

    tree = ast.parse(inspect.getsource(module))
    for node in ast.walk(tree):                                   # drop docstrings
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            body = getattr(node, "body", [])
            if (body and isinstance(body[0], ast.Expr)
                    and isinstance(body[0].value, ast.Constant)
                    and isinstance(body[0].value.value, str)):
                node.body = body[1:] or [ast.Pass()]
    return ast.unparse(tree)                                      # comments never survive unparse


def _state(mme, family_id, anchor, cells):
    """A `FamilyState` at an arbitrary anchor, as a provider would hand one over."""
    family = mme.family(family_id)
    return FamilyState(point=family.at(anchor), law=mme.law_of(family_id).name, cells=dict(cells),
                       instance=mme.instance_of(family_id),
                       value_form=mme.law_of(family_id).value_form,
                       forgotten_since_root=frozenset(family.root.constituents - anchor.constituents))


# ── fixtures ─────────────────────────────────────────────────────────────────────────────────────
@pytest.fixture
def mme():
    return KEX.build()


@pytest.fixture
def cold():
    """An engine that is CONSTITUTED and holds nothing — the world in which `NEED` is the answer."""
    engine = MME(KEX.COMMERCE, REGISTRY, IN_MEMORY, manifold=KEX.MANIFOLD,
                 observer=RecordingObserver())
    for family in KEX._families():
        engine.register_family(family)
    return engine


@pytest.fixture
def fams():
    revenue, order_count, audited, distinct, on_hand, gauge = KEX._families()
    return dict(revenue=revenue, order_count=order_count, audited=audited, distinct=distinct,
                on_hand=on_hand, gauge=gauge)


# ══ A · THE REQUIREMENT SHAPE ═════════════════════════════════════════════════════════════════════
def test_a_requirement_is_an_analytical_requirement_and_not_a_fetch_plan(cold, fams):
    """Ruled §2. It must read

        Need lawful Revenue family state sufficient to establish Revenue@Month

    and never `query table sales / group by month / sum amount`."""
    outcome = cold.requirement_for(fams["revenue"], KEX.BY_DAY)
    assert outcome
    requirement = outcome.requirement

    assert requirement.family_id == "revenue"
    assert requirement.target == KEX.BY_DAY
    assert requirement.root == fams["revenue"].root
    assert requirement.manifold == cold.manifold
    assert requirement.build == cold.build.reference
    assert requirement.instance == cold.instance_of("revenue")
    assert "Need lawful revenue family state" in requirement.render()
    assert "sufficient to establish revenue@commerce{day}" in requirement.render()


def test_the_requirement_vocabulary_contains_no_physical_object(cold, fams):
    """**A vocabulary ban, because §2 is a rule about what a requirement may SAY.** Physical route
    planning belongs below the Realization boundary, so no field of the requirement may name a table, a
    column, a query, a predicate, a projection, a pushdown, a file or a connection."""
    physical = {"table", "column", "query", "sql", "predicate", "projection", "pushdown", "filter",
                "file", "path", "connection", "dsn", "schema", "database", "partition", "index",
                "scan", "plan", "join"}
    # WHOLE WORDS: `acceptable` contains "table", which is exactly the kind of false positive that makes
    # a substring ban worse than no ban.
    names = {f.name for f in fields(FamilyRequirement)}
    for name in names:
        assert not (set(name.split("_")) & physical), name

    # and the rendered requirement says nothing physical either
    rendered = cold.requirement_for(fams["revenue"], KEX.BY_DAY).requirement.render().lower()
    assert not any(word in rendered for word in physical)


def test_the_requirement_carries_the_STANDING_the_state_must_have(cold, fams):
    """*"standing requirements"* (§3). The sharpest case is the structured family: an HLL family needs
    **sketches**, and a provider handing back a finalized estimate would be supplying something the law
    cannot merge. The requirement says so before anyone executes anything."""
    revenue = cold.requirement_for(fams["revenue"], KEX.BY_DAY).requirement
    sketch = cold.requirement_for(fams["distinct"], KEX.BY_DAY).requirement

    assert revenue.value_form == "scalar" and revenue.law == "SUM"
    assert sketch.value_form == "structured" and sketch.law == "HLL_SKETCH"
    assert sketch.sufficient_state                       # the law's own words, carried verbatim
    assert sketch.approximation != "exact"               # and its standing rides along


def test_the_requirement_names_the_evidence_state_when_one_was_asked_for(cold, fams):
    named = cold.requirement_for(fams["revenue"], KEX.BY_DAY, data_state="load:orders@08:00Z")
    indifferent = cold.requirement_for(fams["revenue"], KEX.BY_DAY)
    assert named.requirement.data_state == "load:orders@08:00Z"
    assert "load:orders@08:00Z" in named.requirement.render()
    # `None` means INDIFFERENT, not "any mixture will do" — the MME still never merges across states
    assert indifferent.requirement.data_state is None


def test_acceptable_anchors_are_DERIVED_from_the_family_law(cold, fams):
    """§G's substrate: `Revenue@Month` directly, `Revenue@Day` then continue, `Revenue@Order` then
    continue are three lawful shapes of one need, and the list is computed from the law rather than
    supplied by a caller."""
    requirement = cold.requirement_for(fams["revenue"], KEX.TOTAL).requirement
    acceptable = set(requirement.acceptable)

    assert KEX.TOTAL in acceptable                        # directly
    assert KEX.BY_DAY in acceptable                       # then continue
    assert KEX.SALE_AT in acceptable                      # the root, then continue
    assert all(a.constituents <= fams["revenue"].root.constituents for a in acceptable)
    assert all(KEX.TOTAL.constituents <= a.constituents for a in acceptable)
    assert not requirement.acceptable_truncated


def test_a_restricted_continuation_region_shrinks_the_acceptable_set(cold, fams):
    """The intermediate anchor is asked for its own sake: a provider supplying `OnHand@{store}` when the
    law admits no value there is offering material the family may not hold, and lying on a route to an
    admitted target does not launder it."""
    outcome = cold.requirement_for(fams["on_hand"], KEX.BY_DAY)
    assert outcome
    acceptable = set(outcome.requirement.acceptable)
    assert KEX.BY_STORE not in acceptable
    law = cold.law_of("on_hand")
    from columna_platform.kernel.materialization import entitlement_holds

    assert all(entitlement_holds(fams["on_hand"], law, a) for a in acceptable)


def test_acceptable_is_DESCRIPTION_and_never_permission(cold, fams):
    """**The list confers nothing.** An offer at an anchor outside it is adjudicated by `MME.admit` on its
    own merits, by the same rule, rather than refused for being unlisted — which is what keeps the cap on
    the enumeration from ever becoming a false refusal."""
    requirement = cold.requirement_for(fams["revenue"], KEX.TOTAL).requirement
    truncated = replace(requirement, acceptable=(), acceptable_truncated=True)
    assert not truncated.names_anchor(KEX.BY_DAY)          # the report says nothing about it

    cold.establish_root(fams["revenue"], KEX.ORDERS)
    manager = RealizationManager()
    offer = RealizationOffer(
        provider="p", family_id="revenue", anchor=KEX.BY_DAY,
        value=_state(cold, "revenue", KEX.BY_DAY, {("D1",): 175.0, ("D2",): 325.0}),
        realization=RealizationStanding(provider="p"))
    # ADMITTED, despite being outside a (deliberately emptied) `acceptable` list
    assert manager.establish(cold, offer)


def test_the_acceptable_enumeration_is_capped_and_says_so():
    """A 20-constituent universe has a million anchors between a scalar target and its root. The cap is a
    REPORTING limit; `acceptable_truncated` says it bit."""
    assert requirement_module.ACCEPTABLE_ANCHOR_CAP > 0
    from columna_platform.kernel.geometry import Constituent, Universe
    from columna_platform.kernel.sorts import MeasureFamily

    wide = Universe(name="wide", constituents=tuple(
        Constituent(reference=f"c{i}", domain=f"d{i}") for i in range(12)),
        ground="thing", participation_law="every thing")
    family = MeasureFamily(family_id="w", manifold="m", universe="wide",
                           root=wide.root_anchor, law="SUM", target="a wide family",
                           participation="everything", value_domain="a number")
    anchors, truncated = requirement_module.acceptable_anchors(
        family, REGISTRY.get("SUM"), wide.scalar_anchor)
    assert truncated
    assert len(anchors) <= requirement_module.ACCEPTABLE_ANCHOR_CAP


# ══ B · THE CAPABILITY / PROPOSAL SHAPE ═══════════════════════════════════════════════════════════
def test_propose_executes_nothing(cold, fams):
    """Ruled §4. **Capability discovery must be possible without executing the realization** — otherwise
    every future route comparison has to fetch every route in order to choose between them."""
    cold.establish_root(fams["revenue"], KEX.ORDERS)
    estate = StaticEstate("warehouse", {
        ("revenue", KEX.BY_DAY): _state(cold, "revenue", KEX.BY_DAY, {("D1",): 175.0})})
    manager = RealizationManager(estate)

    proposals = manager.propose(cold.requirement_for(fams["revenue"], KEX.BY_DAY).requirement)
    assert len(proposals) == 1
    assert estate.proposed == 1
    assert estate.realized == 0                            # **nothing was fetched**


def test_a_proposal_carries_what_it_WOULD_supply_before_it_supplies_it(cold, fams):
    cold.establish_root(fams["distinct"], KEX.ORDERS, value_key="customer")
    sketch = cold.measure(fams["distinct"], KEX.BY_DAY).value
    estate = StaticEstate("warehouse", {("distinct_customers", KEX.BY_DAY): sketch})
    manager = RealizationManager(estate)

    requirement = cold.requirement_for(fams["distinct"], KEX.BY_DAY).requirement
    proposal = manager.propose(requirement).proposals[0]

    assert proposal.provider == "warehouse"
    assert proposal.anchor == KEX.BY_DAY
    assert proposal.value_form == "structured" == requirement.value_form
    assert proposal.realization.provider == "warehouse"
    assert proposal.establishment_kind == INDEPENDENT
    assert proposal.handle is not None                     # the provider's own, and opaque


def test_the_manager_never_interprets_a_providers_handle(cold, fams):
    """Physical route planning stays below the boundary (§2): the handle is passed back untouched."""
    cold.establish_root(fams["revenue"], KEX.ORDERS)
    sentinel = object()
    state = _state(cold, "revenue", KEX.BY_DAY, {("D1",): 175.0})

    class Opaque(StaticEstate):
        def propose(self, requirement):
            yield RealizationProposal(provider=self.name, family_id="revenue", anchor=KEX.BY_DAY,
                                      handle=sentinel, realization=self.standing)

        def realize(self, proposal):
            assert proposal.handle is sentinel             # byte-identical, never inspected
            return RealizationOffer(provider=self.name, family_id="revenue", anchor=KEX.BY_DAY,
                                    value=state, realization=self.standing, from_proposal=proposal)

    manager = RealizationManager(Opaque("opaque", {}))
    proposal = manager.propose(cold.requirement_for(fams["revenue"], KEX.BY_DAY).requirement).proposals[0]
    assert proposal.handle is sentinel
    assert manager.realize(proposal).anchor == KEX.BY_DAY


def test_a_proposal_cannot_claim_to_have_CONTINUED(cold, fams):
    """A provider supplies a value at an anchor; it holds no retained material and names none, so
    continuation is not a standing available to it (M-1 §8: establishment is never manufactured)."""
    with pytest.raises(KernelRefusal) as refused:
        RealizationProposal(provider="p", family_id="revenue", anchor=KEX.BY_DAY,
                            establishment_kind=CONTINUED)
    assert refused.value.code == "realization-is-not-continuation"


def test_a_provider_that_offers_nothing_is_recorded_rather_than_silent(cold, fams):
    """*"No provider offers `Revenue@Month`"* and *"the one provider that would have was unreachable"* are
    different facts, and a future coordinator reasoning about a root fetch needs both."""
    cold.establish_root(fams["revenue"], KEX.ORDERS)
    manager = RealizationManager(SilentEstate(), BrokenEstate())
    result = manager.propose(cold.requirement_for(fams["revenue"], KEX.BY_DAY).requirement)

    assert len(result) == 0
    assert result.consulted == ("silent", "broken")
    reasons = dict(result.declined)
    assert "offers nothing" in reasons["silent"]
    assert "could not be asked" in reasons["broken"]
    assert "ConnectionError" in reasons["broken"]


def test_one_unreachable_provider_does_not_hide_the_others(cold, fams):
    """Capability discovery is advisory, so it degrades rather than fails."""
    cold.establish_root(fams["revenue"], KEX.ORDERS)
    good = StaticEstate("warehouse", {
        ("revenue", KEX.BY_DAY): _state(cold, "revenue", KEX.BY_DAY, {("D1",): 175.0})})
    manager = RealizationManager(BrokenEstate(), good)
    result = manager.propose(cold.requirement_for(fams["revenue"], KEX.BY_DAY).requirement)

    assert len(result) == 1 and result.proposals[0].provider == "warehouse"
    assert dict(result.declined).keys() == {"broken"}


def test_realizing_is_the_OTHER_verb_and_it_does_execute(cold, fams):
    cold.establish_root(fams["revenue"], KEX.ORDERS)
    estate = StaticEstate("warehouse", {
        ("revenue", KEX.BY_DAY): _state(cold, "revenue", KEX.BY_DAY,
                                        {("D1",): 175.0, ("D2",): 325.0})})
    manager = RealizationManager(estate)
    proposal = manager.propose(cold.requirement_for(fams["revenue"], KEX.BY_DAY).requirement).proposals[0]

    offer = manager.realize(proposal)
    assert estate.realized == 1
    assert offer.from_proposal is proposal


def test_an_offer_must_settle_the_claim_it_was_proposed_as(cold, fams):
    """A coordinator that compared alternatives on the proposal and received something else compared
    nothing."""
    cold.establish_root(fams["revenue"], KEX.ORDERS)
    state = _state(cold, "revenue", KEX.TOTAL, {(): 500.0})

    class Bait(StaticEstate):
        def propose(self, requirement):
            yield RealizationProposal(provider=self.name, family_id="revenue", anchor=KEX.BY_DAY,
                                      realization=self.standing)

        def realize(self, proposal):
            return RealizationOffer(provider=self.name, family_id="revenue", anchor=KEX.TOTAL,
                                    value=state, realization=self.standing)

    manager = RealizationManager(Bait("bait", {}))
    proposal = manager.propose(cold.requirement_for(fams["revenue"], KEX.BY_DAY).requirement).proposals[0]
    with pytest.raises(KernelRefusal) as refused:
        manager.realize(proposal)
    assert refused.value.code == "offer-does-not-match-proposal"


def test_a_proposal_is_executed_by_the_provider_that_made_it(cold, fams):
    """No substitution: two providers offering the same `F@A` are offering two differently realized
    values, and realization standing is an axis of the key."""
    manager = RealizationManager(SilentEstate())
    stray = RealizationProposal(provider="somebody-else", family_id="revenue", anchor=KEX.BY_DAY)
    with pytest.raises(KernelRefusal) as refused:
        manager.realize(stray)
    assert refused.value.code == "unknown-realization-provider"


def test_a_thing_with_only_realize_is_not_a_provider():
    """The two verbs are the interface (§4); an object with one of them is not half a provider."""
    class OnlyExecutes:
        name = "half"

        def realize(self, proposal):                                 # pragma: no cover
            raise AssertionError

    with pytest.raises(KernelRefusal) as refused:
        RealizationManager(OnlyExecutes())
    assert refused.value.code == "not-a-realization-provider"
    assert "without executing the realization" in refused.value.detail


# ══ C · THE REALIZED-OFFER SHAPE ══════════════════════════════════════════════════════════════════
def test_an_offer_carries_the_ruled_fields(cold, fams):
    cold.establish_root(fams["revenue"], KEX.ORDERS)
    state = _state(cold, "revenue", KEX.BY_DAY, {("D1",): 175.0})
    estate = StaticEstate("warehouse", {("revenue", KEX.BY_DAY): state})
    manager = RealizationManager(estate)
    proposal = manager.propose(cold.requirement_for(fams["revenue"], KEX.BY_DAY).requirement).proposals[0]
    offer = manager.realize(proposal)

    assert offer.family_id == "revenue"                                 # family
    assert offer.anchor == KEX.BY_DAY                                   # anchor
    assert offer.value is state                                         # family value / payload
    assert offer.instance == cold.instance_of("revenue")                # analytical instance
    assert offer.establishment.kind == INDEPENDENT                      # establishment
    assert offer.realization == RealizationStanding(provider="warehouse")  # realization standing
    assert offer.provider == "warehouse" and offer.diagnostics          # provider identity/diagnostics


def test_an_offer_cannot_claim_to_have_CONTINUED(cold):
    with pytest.raises(KernelRefusal) as refused:
        RealizationOffer(provider="p", family_id="revenue", anchor=KEX.BY_DAY, value=None,
                         establishment=Establishment(CONTINUED, ()))
    assert refused.value.code in ("realization-is-not-continuation", "continuation-without-a-parent")


def test_an_offer_is_not_a_materialization(cold, fams):
    """It has no cache identity, no residency and no eligibility. Those are minted by admission, if
    admission happens — and whether it happens is not the estate's call."""
    offer = RealizationOffer(provider="p", family_id="revenue", anchor=KEX.BY_DAY, value=None)
    for minted in ("id", "residency", "eligibility", "admitted_seq", "superseded_by"):
        assert not hasattr(offer, minted), minted
    with pytest.raises(FrozenInstanceError):
        offer.provider = "somebody-else"                                # type: ignore[misc]


def test_an_arrow_backed_offer_crosses_the_boundary_unconverted():
    """Ruled §5: Arrow should remain the natural materialization boundary. **No conversion happens here** —
    a columnar provider's Arrow-backed state enters `admit` as the same object it left the provider as."""
    engine, _block = CEX.build(settled=True, data_state="load:orders@08:00Z")
    state = engine.measure("revenue", CEX.BY_DAY).value
    assert isinstance(state.values, pa.Array)

    estate = StaticEstate("arrow-estate", {("revenue", CEX.BY_DAY): state})
    manager = RealizationManager(estate)
    requirement = engine.authority.requirement_for(
        engine.family("revenue"), CEX.BY_DAY).requirement
    offer = manager.realize(manager.propose(requirement).proposals[0])

    assert offer.value is state                                        # the SAME object
    assert isinstance(offer.value.values, pa.Array)                    # still Arrow
    admitted = manager.establish(engine, offer)
    assert admitted
    assert engine.materialization(admitted.id).value.values is state.values


# ══ D · REALIZED STATE ENTERS THE ORDINARY `MME.admit` ════════════════════════════════════════════
def test_establish_is_a_call_to_mme_admit_and_nothing_else(cold, fams):
    """Ruled §1: *"Any realized family materialization must enter through the ordinary MME admission path
    and receive exactly the same adjudication as any other independently established `F@A`."*"""
    cold.establish_root(fams["revenue"], KEX.ORDERS)
    state = _state(cold, "revenue", KEX.BY_DAY, {("D1",): 175.0, ("D2",): 325.0})
    offer = RealizationOffer(provider="warehouse", family_id="revenue", anchor=KEX.BY_DAY,
                             value=state, realization=RealizationStanding(provider="warehouse"))

    seen = {}
    real = cold.admit

    def watched(value, **kwargs):
        seen.update(value=value, **kwargs)
        return real(value, **kwargs)

    cold.admit = watched                                               # type: ignore[method-assign]
    admission = RealizationManager.establish(cold, offer)

    assert admission                                                   # it went in
    assert seen["value"] is state                                      # through `admit`
    assert seen["establishment"].kind == INDEPENDENT
    assert "realized by warehouse" in seen["note"]
    # and the resulting materialization is an ORDINARY one in every respect
    materialization = cold.materialization(admission.id)
    assert materialization.establishment.kind == INDEPENDENT
    assert materialization.eligibility == "current" and materialization.serviceable


def test_the_manager_holds_no_machinery_for_a_privileged_shortcut():
    """**Not a convention kept by care — the absence of the machinery.** The manager cannot reach a store,
    cannot construct a `FamilyMaterialization` and cannot mint a `MaterializationId`."""
    from columna_platform.kernel import realization_manager as module

    manager = RealizationManager()
    for forbidden in ("materializations", "_store", "store", "_by_id"):
        assert not hasattr(manager, forbidden), forbidden

    code = _code_only(module)
    for forbidden in ("MaterializationStore", "FamilyMaterialization", "MaterializationId",
                      "_mint", "admit(point=", "materializations.admit"):
        assert forbidden not in code, forbidden
    assert "mme.admit(" in code                                        # the one door, and it is there


def test_realized_material_is_then_ordinary_in_every_later_respect(cold, fams):
    """It seeds continuations, it supersedes, it evicts, it is adjudicated. Being realized is not a
    standing that survives admission — it becomes `INDEPENDENT` material and is treated as such."""
    cold.establish_root(fams["revenue"], KEX.ORDERS)
    state = _state(cold, "revenue", KEX.STORE_DAY, {("S1", "D1"): 175.0, ("S1", "D2"): 325.0})
    offer = RealizationOffer(provider="warehouse", family_id="revenue", anchor=KEX.STORE_DAY,
                             value=state, realization=RealizationStanding(provider="warehouse"))
    admission = RealizationManager.establish(cold, offer)
    assert admission

    # it can SEED a continuation, like any other lawful non-root materialization
    served = cold.measure(fams["revenue"], KEX.BY_DAY)
    assert served.served
    # it is adjudicated by the ordinary five questions
    from columna_platform.kernel.mme import Retained

    held = cold.materialization(admission.id)
    verdict = cold.adjudicate(Retained(key=cold._descriptor(held), value=held.value),
                              fams["revenue"], KEX.TOTAL)
    assert verdict
    # and the ordinary lifecycle applies to it
    cold.materializations.evict(admission.id)
    assert not cold.materialization(admission.id).serviceable


def test_the_estate_cannot_overwrite_a_held_answer_by_asserting_a_different_one(cold, fams):
    """**M-1's duplicate-current consistency rule applies to realized material unchanged.** A provider
    supplying a value that disagrees with a retained CURRENT one at the same slot is a consistency
    failure, not a cache choice — and coming from a backend does not settle which of two answers to one
    question is right. Neither is discarded and nothing is admitted."""
    cold.establish_root(fams["revenue"], KEX.ORDERS)
    served = cold.measure(fams["revenue"], KEX.BY_DAY)
    assert served.served

    disagreeing = _state(cold, "revenue", KEX.BY_DAY, {("D1",): 999.0, ("D2",): 1.0})
    admission = RealizationManager.establish(
        cold, RealizationOffer(provider="warehouse", family_id="revenue", anchor=KEX.BY_DAY,
                               value=disagreeing,
                               realization=RealizationStanding(provider="warehouse")))
    assert not admission
    assert admission.code == "duplicate-current-disagreement"
    assert "will not pick between two answers to one question" in admission.detail
    # and the held answer is untouched
    assert dict(cold.measure(fams["revenue"], KEX.BY_DAY).value.cells) == dict(served.value.cells)


def test_realized_material_is_subject_to_the_off_build_guard_too(cold, fams):
    """A new Manifold build is a new semantic world, and material does not cross into one by being
    supplied. The guard is `admit`'s, reached through the ordinary door."""
    cold.establish_root(fams["revenue"], KEX.ORDERS)
    state = _state(cold, "revenue", KEX.BY_DAY, {("D1",): 175.0})
    refused = cold.admit(state, establishment=Establishment(INDEPENDENT),
                         witness="some-other-build-digest")
    assert not refused and refused.code == "off-build-material"
    assert "does not cross into one by being present" in refused.detail


# ══ E · PROVIDER CAPABILITY CANNOT BYPASS FAMILY LAW ══════════════════════════════════════════════
def test_a_provider_offering_an_unlawful_anchor_is_REFUSED_by_the_family_law(cold, fams):
    """**The blast wall** (§6): *"A backend being able to compute something does not make it a lawful
    Columna materialization."* `on_hand` admits no value at `{store}`; a provider holding one anyway is
    refused by the same rule, in the same words, as a locally derived value at the same place."""
    cold.establish_root(fams["on_hand"], KEX.LEVELS)
    unlawful = _state(cold, "on_hand", KEX.BY_STORE, {("S1",): 42})
    offer = RealizationOffer(provider="confident-warehouse", family_id="on_hand",
                             anchor=KEX.BY_STORE, value=unlawful,
                             realization=RealizationStanding(provider="confident-warehouse"))

    admission = RealizationManager.establish(cold, offer)
    assert not admission
    assert admission.code == "anchor-outside-the-continuation-region"
    assert "ASKED OF INDEPENDENTLY ESTABLISHED MATERIAL TOO" in admission.detail \
        or "THIS IS ASKED" in admission.detail
    assert not cold.materializations.select("on_hand", anchor=KEX.BY_STORE, eligibility=None)


def test_the_refusal_is_WORD_FOR_WORD_the_one_a_local_value_gets(cold, fams):
    """Not merely 'also refused' — refused by the same code and the same explanation, because it is
    literally the same check. A separate realization-side check would be a second authority."""
    cold.establish_root(fams["on_hand"], KEX.LEVELS)
    unlawful = _state(cold, "on_hand", KEX.BY_STORE, {("S1",): 42})

    local = cold.admit(unlawful)
    realized = RealizationManager.establish(
        cold, RealizationOffer(provider="warehouse", family_id="on_hand", anchor=KEX.BY_STORE,
                               value=unlawful, realization=RealizationStanding(provider="warehouse")))
    assert not local and not realized
    assert local.code == realized.code
    assert local.detail == realized.detail


def test_the_manager_does_not_PRE_FILTER_an_unlawful_proposal(cold, fams):
    """**Reported, not removed** (§1). Filtering would be the manager adjudicating analytical lawfulness,
    which it does not do; the discrepancy travels as a diagnostic and `admit` decides."""
    cold.establish_root(fams["on_hand"], KEX.LEVELS)
    estate = StaticEstate("confident-warehouse", {
        ("on_hand", KEX.BY_STORE): _state(cold, "on_hand", KEX.BY_STORE, {("S1",): 42})})
    manager = RealizationManager(estate)
    requirement = cold.requirement_for(fams["on_hand"], KEX.BY_DAY).requirement

    result = manager.propose(requirement)
    assert len(result) == 1                                   # NOT silently dropped
    assert result.outside_requirement == result.proposals     # and flagged as outside
    assert not requirement.names_anchor(KEX.BY_STORE)
    # the refusal still comes from the family law, at admission
    assert not manager.establish(cold, manager.realize(result.proposals[0]))


def test_no_realization_requirement_is_emitted_for_an_UNSUPPORTED_target(cold, fams):
    """**The sharpest form of the blast wall**, and the reason the refusal lives where the requirement
    would be minted: if `UNSUPPORTED` became a realization request, we would be asking a provider to
    compute an answer the family law forbids — and it very likely could."""
    outcome = cold.requirement_for(fams["on_hand"], KEX.BY_STORE)
    assert not outcome
    assert outcome.requirement is None
    assert "NO REALIZATION REQUIREMENT IS EMITTED" in outcome.reason
    assert "would not thereby make it a lawful Columna materialization" in outcome.reason


def test_a_target_outside_the_family_root_emits_no_requirement_either(cold, fams):
    """A family lives at or below `R_F`. There is no state at a finer location for anyone to supply, and
    this is explicitly **not a gap in the estate**."""
    from columna_platform.kernel.geometry import Constituent, Universe

    outcome = cold.requirement_for(fams["on_hand"], KEX.COMMERCE.anchor({"store", "day", "order"}))
    assert not outcome
    assert "not a gap in the estate" in outcome.reason
    assert Universe and Constituent                            # imported for the reader above


def test_a_provider_cannot_grant_continuation_rights(cold, fams):
    """Ruled §1: *"It does not grant continuation rights."* Realized material is `INDEPENDENT`, so it
    seeds only what the family law admits from where it sits — the adjudication is unchanged."""
    cold.establish_root(fams["on_hand"], KEX.LEVELS)
    # a LAWFUL non-root anchor for this family, supplied by the estate
    lawful = _state(cold, "on_hand", KEX.BY_DAY, {("D1",): 10, ("D2",): 12})
    admission = RealizationManager.establish(
        cold, RealizationOffer(provider="warehouse", family_id="on_hand",
                               anchor=KEX.BY_DAY, value=lawful,
                               realization=RealizationStanding(provider="warehouse")))
    assert admission
    assert cold.materialization(admission.id).establishment.kind == INDEPENDENT
    # the realized material is present and the unlawful target is STILL refused
    refused = cold.measure(fams["on_hand"], KEX.BY_STORE)
    assert not refused.served


# ══ F · HOW `NEED` MAPS INTO REALIZATION REQUIREMENTS ═════════════════════════════════════════════
def test_a_NEED_observation_becomes_a_requirement(cold, fams):
    """§F, end to end: the disposition M-2 emits is the input to the actor R-1 introduces."""
    observer = cold.observations.observer
    refused = cold.measure(fams["revenue"], KEX.BY_DAY)
    assert not refused.served
    observation = observer.records[-1]
    assert observation.disposition == NEED

    outcome = requirement_from(cold, observation)
    assert outcome
    assert outcome.requirement.family_id == "revenue"
    assert outcome.requirement.target == KEX.BY_DAY
    assert f"NEED observed at request #{observation.seq}" in outcome.requirement.note


def test_the_expression_that_caused_the_need_rides_into_the_requirement(cold, fams, mme):
    """M-2's `on_behalf_of` (§8 route/use evidence) survives into R-1: a coordinator eventually choosing
    a route wants to know that this `Revenue@Day` is wanted because someone asked for `AOV@Day`."""
    from columna_platform.kernel import ExpressionEvaluator

    for expression in KEX._expressions():
        cold.register_expression(expression)
    observer = cold.observations.observer
    ExpressionEvaluator(cold).evaluate(KEX._expressions()[0], KEX.BY_DAY)

    need = next(r for r in observer.records if r.disposition == NEED and r.request.on_behalf_of)
    outcome = requirement_from(cold, need)
    assert outcome
    assert "average_order_value" in outcome.requirement.note


def test_READY_produces_no_requirement_and_says_why(mme, fams):
    observer = RecordingObserver()
    mme.observations.observer = observer
    assert mme.measure(fams["revenue"], KEX.BY_DAY).served
    outcome = requirement_from(mme, observer.records[-1])
    assert not outcome
    assert "nothing is needed" in outcome.reason


def test_UNSUPPORTED_produces_no_requirement_and_says_why(mme, fams):
    """**The load-bearing one.** A silent `None` here and at `READY` would have been the same absence for
    two opposite facts."""
    observer = RecordingObserver()
    mme.observations.observer = observer
    assert not mme.measure(fams["on_hand"], KEX.BY_STORE).served
    observation = observer.records[-1]
    assert observation.disposition == UNSUPPORTED

    outcome = requirement_from(mme, observation)
    assert isinstance(outcome, RequirementOutcome)
    assert not outcome
    assert "no lawful route to this target exists" in outcome.reason
    assert "THIS IS NOT A GAP IN THE ESTATE" in outcome.reason


def test_WANT_OF_STATE_is_DEFERRED_explicitly_rather_than_mapped_onto_the_wrong_shape():
    """It is a realizable need and it names POINTS, not an anchor. R-1 does not invent that shape; it
    says so, rather than quietly reusing the anchor-shaped one."""
    engine, _block = CEX.build(settled=False)
    observer = RecordingObserver()
    engine.observations.observer = observer
    assert not engine.measure("revenue", CEX.BY_DAY).served
    observation = observer.records[-1]
    assert observation.disposition == WANT_OF_STATE

    outcome = requirement_from(engine.authority, observation)
    assert not outcome
    assert "DIFFERENT requirement shape" in outcome.reason
    assert "points rather than an anchor" in outcome.reason


def test_only_NEED_is_realizable_in_r1():
    from columna_platform.kernel.realization_manager import REALIZABLE_DISPOSITIONS

    assert REALIZABLE_DISPOSITIONS == (NEED,)


def test_the_full_loop_NEED_to_requirement_to_proposal_to_offer_to_admit_to_served(cold, fams):
    """**R-1's whole point, as one story.**

        measure → NEED → requirement → propose → realize → MME.admit → measure → READY
    """
    observer = cold.observations.observer
    assert not cold.measure(fams["revenue"], KEX.TOTAL).served
    need = observer.records[-1]
    assert need.disposition == NEED

    outcome = requirement_from(cold, need)
    assert outcome

    estate = StaticEstate("warehouse", {
        ("revenue", KEX.BY_DAY): FamilyState(
            point=fams["revenue"].at(KEX.BY_DAY), law="SUM",
            cells={("D1",): 175.0, ("D2",): 325.0}, instance=cold.instance_of("revenue"),
            value_form="scalar",
            forgotten_since_root=frozenset({"order", "store"}))})
    manager = RealizationManager(estate)

    proposals = manager.propose(outcome.requirement)
    assert len(proposals) == 1
    offer = manager.realize(proposals.proposals[0])
    admission = manager.establish(cold, offer)
    assert admission

    served = cold.measure(fams["revenue"], KEX.TOTAL)
    assert served.served and served.cell() == pytest.approx(500.0)
    assert observer.records[-1].disposition == READY
    # and it was DERIVED from the realized material, which the observation records
    assert observer.records[-1].fulfillment.selected == (admission.id,)
    assert observer.records[-1].fulfillment.seeded_from == KEX.BY_DAY


# ══ G · MANY ANCHORS AND PROVIDERS, REPRESENTED WITHOUT CHOOSING ══════════════════════════════════
def _three_route_estate(cold, fams):
    cold.establish_root(fams["revenue"], KEX.ORDERS)
    return {
        ("revenue", KEX.TOTAL): _state(cold, "revenue", KEX.TOTAL, {(): 500.0}),
        ("revenue", KEX.BY_DAY): _state(cold, "revenue", KEX.BY_DAY,
                                        {("D1",): 175.0, ("D2",): 325.0}),
        ("revenue", KEX.SALE_AT): cold.measure(fams["revenue"], KEX.SALE_AT).value,
    }


def test_three_lawful_routes_are_all_represented(cold, fams):
    """Ruled §G, in the ruling's own example:

        Revenue@Month directly · Revenue@Day then continue · Revenue@Order then continue
    """
    manager = RealizationManager(StaticEstate("warehouse", _three_route_estate(cold, fams)))
    result = manager.propose(cold.requirement_for(fams["revenue"], KEX.TOTAL).requirement)

    assert isinstance(result, ProposalSet)
    assert len(result) == 3
    assert set(result.anchors) == {KEX.TOTAL, KEX.BY_DAY, KEX.SALE_AT}
    assert set(result.by_anchor()) == {str(KEX.TOTAL), str(KEX.BY_DAY), str(KEX.SALE_AT)}
    # all three are lawful shapes of this need
    assert all(result.requirement.names_anchor(a) for a in result.anchors)


def test_two_providers_offering_the_same_thing_are_both_kept(cold, fams):
    """§G's second axis. They are not deduplicated: two providers offering one `F@A` are offering two
    differently realized values, and realization standing is an axis of the retention key."""
    holdings = _three_route_estate(cold, fams)
    manager = RealizationManager(StaticEstate("warehouse", holdings),
                                 StaticEstate("lakehouse", holdings, carrier="parquet"))
    result = manager.propose(cold.requirement_for(fams["revenue"], KEX.TOTAL).requirement)

    assert len(result) == 6
    assert set(result.by_provider()) == {"warehouse", "lakehouse"}
    at_total = result.by_anchor()[str(KEX.TOTAL)]
    assert len(at_total) == 2
    assert {p.realization.carrier for p in at_total} == {"in-memory", "parquet"}


def test_nothing_in_the_proposal_surface_CHOOSES(cold, fams):
    """Ruled §7: no route-choice policy yet. **A guard, not a formality** — the temptation in the unit
    that builds the comparison surface is to add the one obvious comparison."""
    manager = RealizationManager(StaticEstate("warehouse", _three_route_estate(cold, fams)))
    result = manager.propose(cold.requirement_for(fams["revenue"], KEX.TOTAL).requirement)

    forbidden = ("best", "cheapest", "preferred", "choose", "select", "rank", "score", "cost",
                 "estimate_cost", "optimal", "recommend", "plan", "prefer")
    for name in forbidden:
        assert not hasattr(result, name), name
        assert not hasattr(manager, name), name
        assert not hasattr(RealizationProposal, name), name
    assert {f.name for f in fields(RealizationProposal)} == {
        "provider", "family_id", "anchor", "value_form", "realization", "establishment_kind",
        "handle", "diagnostics"}


def test_the_proposal_order_is_the_order_offered_and_not_a_preference(cold, fams):
    """Providers are consulted in registration order and their proposals arrive in the order they made
    them. That is a record of what happened, not a ranking of what to do."""
    holdings = _three_route_estate(cold, fams)
    first = RealizationManager(StaticEstate("a", holdings), StaticEstate("b", holdings))
    second = RealizationManager(StaticEstate("b", holdings), StaticEstate("a", holdings))
    requirement = cold.requirement_for(fams["revenue"], KEX.TOTAL).requirement

    assert [p.provider for p in first.propose(requirement)][0] == "a"
    assert [p.provider for p in second.propose(requirement)][0] == "b"
    assert first.providers == ("a", "b") and second.providers == ("b", "a")


def test_the_set_can_be_read_by_anchor_and_by_provider_without_reducing(cold, fams):
    holdings = _three_route_estate(cold, fams)
    manager = RealizationManager(StaticEstate("warehouse", holdings),
                                 StaticEstate("lakehouse", holdings))
    result = manager.propose(cold.requirement_for(fams["revenue"], KEX.TOTAL).requirement)

    assert sum(len(v) for v in result.by_anchor().values()) == len(result)
    assert sum(len(v) for v in result.by_provider().values()) == len(result)
    assert "6 proposal(s)" in result.summary() and "3 anchor(s)" in result.summary()


# ══ THE BOUNDARY, STRUCTURALLY ════════════════════════════════════════════════════════════════════
def test_the_mme_knows_nothing_about_providers():
    """The dependency arrow is the architecture: `mme.py` imports `requirement.py` and NOT
    `realization_manager.py`. An engine that could name a provider would be an engine that could prefer
    one."""
    code = _code_only(kernel_mme_module)
    assert "FamilyRequirement" in code                                 # it states requirements …
    for forbidden in ("realization_manager", "RealizationManager", "RealizationProvider",
                      "RealizationProposal", "RealizationOffer", "ProposalSet"):
        assert forbidden not in code, forbidden                        # … and knows of no estate


def test_the_requirement_module_knows_nothing_about_providers_either():
    code = _code_only(requirement_module)
    for forbidden in ("provider", "Provider", "realize", "propose", "estate", "backend",
                      "RealizationProposal", "RealizationOffer"):
        assert forbidden not in code, forbidden


def test_r1_ships_no_backend_no_adbc_and_no_io():
    """Ruled §8. Held as an import-and-vocabulary ban rather than an intention."""
    from columna_platform.kernel import realization_manager as manager_module

    code = "".join(_code_only(m) for m in (manager_module, requirement_module))
    for banned in ("adbc", "duckdb", "psycopg", "sqlalchemy", "iceberg", "postgres", "sqlite3",
                   "import socket", "import requests", "urllib", "open(", "connect(", "cursor",
                   "SELECT ", "FROM "):
        assert banned not in code.lower() if banned.islower() else banned not in code, banned


def test_no_fulfillment_coordinator_arrived_early():
    """R-1's stop condition. The coordinator's job is to COMBINE the two answers, and combining them is
    exactly what nothing here does."""
    import columna_platform.kernel as kernel_pkg

    for premature in ("FulfillmentCoordinator", "Fulfillment", "Runtime", "ManifoldRuntime"):
        if premature == "Fulfillment":
            # M-2's `Fulfillment` is the observation record's work-performed field — a different thing,
            # and it must not be confused with the coordinator that does not exist yet.
            from columna_platform.kernel.observation import Fulfillment

            assert {f.name for f in fields(Fulfillment)} >= {"directly_held", "selected"}
            continue
        assert not hasattr(kernel_pkg, premature), premature
