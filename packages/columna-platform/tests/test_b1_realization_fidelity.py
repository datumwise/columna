"""
test_b1_realization_fidelity.py — **B-1′: a physical result does not become a governed object by being
produced, labelled, or offered.**

    *"A physical result may be evidence for a governed analytical object. It does not become that object by
    being produced, labelled, or offered. Fidelity between physical result and analytical identity must be
    independently established before cache admission."*  — Huayin, 2026-09-30

        physical provider result
                ↓
        claim: this realizes F@A
                ↓
        faithful-realization adjudication          ← `RealizationAuthority`
                ↓
        adjudicated physical offer                 ← `AdjudicatedRealization`, mint-guarded
                ↓
        ordinary MME admission                     ← `RealizationManager.establish` → `mme.put`
                ↓
        FamilyMaterialization

THREE CLAIMS, AND THEY ARE NOT ONE (§1)
---------------------------------------
    `AuthorizedFamilyContinuation`   this analytical continuation may lawfully be attempted
    `AuthorizedStanding`             a value of this family may stand at this analytical point
    `AdjudicatedRealization`         THIS PARTICULAR PHYSICAL RESULT faithfully realizes that object

§G below pins the first two as preconditions and non-consequences of the third: standing is required for
fidelity, and fidelity grants no continuation.

SECTIONS
--------
    A  the provider cannot self-certify (§3, §E)
    B  what the adjudicator consumes and what it produces (§C, §D, §B)
    C  the five fidelity questions, each a fact about the RESULT (§G)
    D  mismatches land at the layer that owns them (§6, §G)
    E  ordinary admission, with no privileged shortcut (§4, §F)
    F  capability is not fidelity; fidelity is not authorization (§8, §H, §I)
    G  the one governed fact B-1′ found missing, and where it went (§K)

NOT EXERCISED, DELIBERATELY: no DuckDB, no ADBC, no persistence, no cache-cost optimizer, no expression
caching, no new execution kernels. Existing test doubles only.
"""
from __future__ import annotations

import ast
import inspect
from dataclasses import replace

import pytest

from columna_platform.kernel import (
    MME,
    REGISTRY,
    AdjudicatedRealization,
    Establishment,
    FamilyPoint,
    FamilyState,
    KernelRefusal,
    RealizationAuthority,
    RealizationManager,
    RealizationOffer,
    RealizationStanding,
)
from columna_platform.kernel import exhibit as EX
from columna_platform.kernel import realization_fidelity as fidelity_module
from columna_platform.kernel.builtins import IN_MEMORY
from columna_platform.kernel.law import SCALAR, STRUCTURED
from columna_platform.kernel.materialization import INDEPENDENT


def _code_only(module) -> str:
    tree = ast.parse(inspect.getsource(module))
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            body = getattr(node, "body", [])
            if (body and isinstance(body[0], ast.Expr)
                    and isinstance(body[0].value, ast.Constant)
                    and isinstance(body[0].value.value, str)):
                node.body = body[1:] or [ast.Pass()]
    return ast.unparse(tree)


@pytest.fixture
def mme():
    engine = MME(EX.COMMERCE, REGISTRY, IN_MEMORY, manifold=EX.MANIFOLD)
    for family in EX._families():
        engine.register_family(family)
    return engine


@pytest.fixture
def fams():
    revenue, order_count, audited, distinct, on_hand, gauge = EX._families()
    return dict(revenue=revenue, order_count=order_count, audited=audited, distinct=distinct,
                on_hand=on_hand, gauge=gauge)


def _state(mme, family_id, anchor, cells, *, law=None, value_form=None):
    """A `FamilyState` at an arbitrary anchor — a stand-in for whatever a provider hands back."""
    bound = mme.law_of(family_id)
    root = mme.family(family_id).root
    return FamilyState(
        point=FamilyPoint(family_id, anchor), law=law or bound.name,
        value_form=value_form or bound.value_form, cells=cells,
        instance=mme.instance_of(family_id),
        forgotten_since_root=frozenset(root.constituents - anchor.constituents))


def _offer(mme, family_id, anchor, value, *, provider="warehouse", **overrides):
    """A complete claim: what it realizes, and which governed environment it was realized against."""
    fields = dict(
        provider=provider, family_id=family_id, anchor=anchor, value=value,
        instance=value.instance, realization=RealizationStanding(provider=provider),
        establishment=Establishment(INDEPENDENT),
        build=mme.build.reference, witness=mme.witness_of(family_id).digest)
    fields.update(overrides)
    return RealizationOffer(**fields)


# ══ A · THE PROVIDER CANNOT SELF-CERTIFY (§3, §E) ══════════════════════════════════════════════════
def test_the_credential_cannot_be_constructed_outside_the_authority(mme, fams):
    """**§E, structurally.** A provider may return values, its own identity, carrier information, evidence,
    and the analytical identity it CLAIMS to realize. It must not be able to mint the credential that says
    its own output faithfully realizes `F@A`."""
    state = _state(mme, "revenue", EX.BY_DAY, {("D1",): 175.0})
    standing = mme.authorizer.authorize_standing(fams["revenue"], EX.BY_DAY).request

    with pytest.raises(KernelRefusal) as refused:
        AdjudicatedRealization(offer=_offer(mme, "revenue", EX.BY_DAY, state),
                               standing=standing,
                               realization=RealizationStanding(provider="warehouse"))
    assert refused.value.code == "unadjudicated-realization"
    assert "not the provider's to make about its own output" in refused.value.detail
    assert "settle analytical identity by assertion" in refused.value.detail


def test_the_mint_is_module_private_and_unexported():
    """Same instrument as B-0b's, for the same reason and with no cryptography."""
    assert "_MINT" not in fidelity_module.__all__
    assert not hasattr(RealizationAuthority, "_MINT")
    assert type(fidelity_module._MINT).__name__ == "_Mint"


def test_the_door_refuses_a_raw_offer_with_a_governed_message(mme, fams):
    """A caller who hands the provider's own claim straight to admission is told what is missing, rather
    than failing somewhere inside on an attribute."""
    state = _state(mme, "revenue", EX.BY_DAY, {("D1",): 175.0})
    with pytest.raises(KernelRefusal) as refused:
        RealizationManager.establish(mme, _offer(mme, "revenue", EX.BY_DAY, state))
    assert refused.value.code == "unadjudicated-offer-at-the-door"
    assert "A provider's own offer is a CLAIM" in refused.value.detail


def test_a_provider_cannot_reach_the_cache_by_any_other_route(mme):
    """The door's signature is the boundary: `establish` takes only the credential, and there is no second
    entry point on the manager that takes an offer."""
    signature = inspect.signature(RealizationManager.establish)
    assert list(signature.parameters)[:2] == ["mme", "adjudicated"]
    assert signature.parameters["adjudicated"].annotation == "AdjudicatedRealization"

    surface = {n for n in dir(RealizationManager) if not n.startswith("_")}
    assert surface == {"establish", "propose", "providers", "realize", "register"}
    code = _code_only(inspect.getmodule(RealizationManager))
    assert "trusted" not in code and "bypass" not in code


# ══ B · WHAT IT CONSUMES, AND WHAT IT PRODUCES (§B, §C, §D) ════════════════════════════════════════
def test_a_faithful_claim_is_adjudicated_and_the_credential_records_the_evidence(mme, fams):
    """**§C and §D.** The adjudicator consumes the claim — identity, anchor, payload, instance, realization
    standing, build, witness — and produces a credential carrying the offer whole, the standing it was
    checked against, the realization standing, the evidence observed, and any conditions."""
    mme.establish_root(fams["revenue"], EX.ORDERS)
    state = _state(mme, "revenue", EX.BY_DAY, {("D1",): 175.0, ("D2",): 325.0})

    adjudicated = mme.realizations.adjudicate(_offer(mme, "revenue", EX.BY_DAY, state))
    assert adjudicated
    credential = adjudicated.credential

    assert credential.offer.value is state                      # the payload is carried, not copied
    assert credential.standing.subject == f"revenue@{EX.BY_DAY}"
    assert credential.realization.provider == "warehouse"
    assert any("standing:" in e for e in credential.evidence)
    assert any("claim bound to build" in e for e in credential.evidence)
    assert any("value form" in e for e in credential.evidence)
    assert any("instance agrees" in e for e in credential.evidence)
    assert any("realized by warehouse" in e for e in credential.evidence)
    assert credential.conditions == ()
    assert str(credential).startswith("adjudicated(revenue@")


def test_the_claim_must_state_the_governed_environment_it_was_made_against(mme, fams):
    """**§5's binding requirement.** A claim silent about which build or which per-object declaration it
    realized cannot be bound to one. The authority requires both and deliberately compares NEITHER — that is
    `MME.put`'s, and asking twice is the defect B-0a and B-0b removed."""
    state = _state(mme, "revenue", EX.BY_DAY, {("D1",): 1.0})

    no_build = mme.realizations.adjudicate(_offer(mme, "revenue", EX.BY_DAY, state, build=""))
    assert not no_build and no_build.refusal.code == "realization-states-no-build"
    assert "THIS AUTHORITY DOES NOT COMPARE IT" in no_build.refusal.detail

    no_witness = mme.realizations.adjudicate(_offer(mme, "revenue", EX.BY_DAY, state, witness=""))
    assert not no_witness and no_witness.refusal.code == "realization-states-no-witness"

    authority = _code_only(fidelity_module)
    assert "off-build-material" not in authority                # owned by `put`, not restated here


def test_the_authority_reads_the_constitution_through_the_one_existing_reader(mme):
    """It obtains standings from `ContinuationAuthority` rather than re-deriving them, so B-0b's result
    holds: the continuation region is still read in exactly one module."""
    code = _code_only(fidelity_module)
    assert "authorizer.authorize_standing(" in code
    for constitutional in ("region.admits(", "entitlement_holds(", "cumulative_forgotten(",
                           "ContinuationRegion"):
        assert constitutional not in code, constitutional


# ══ C · THE FIVE FIDELITY QUESTIONS — EACH ABOUT THE RESULT (§G) ═══════════════════════════════════
def test_a_payload_naming_another_family_is_not_evidence_for_this_one(mme, fams):
    """A label is not an identity. The offer says `revenue`; the payload's own point says `order_count`."""
    mislabelled = _state(mme, "order_count", EX.BY_DAY, {("D1",): 3})
    refused = mme.realizations.adjudicate(
        _offer(mme, "revenue", EX.BY_DAY, mislabelled,
               witness=mme.witness_of("revenue").digest))
    assert not refused and refused.refusal.code == "realization-is-not-of-the-claimed-family"
    assert "does not become a governed object by being labelled" in refused.refusal.detail


def test_a_payload_at_another_anchor_is_not_evidence_for_this_location(mme, fams):
    """A total is not a daily breakdown, whichever way the offer is addressed."""
    total = _state(mme, "revenue", EX.TOTAL, {(): 500.0})
    refused = mme.realizations.adjudicate(_offer(mme, "revenue", EX.BY_DAY, total))
    assert not refused and refused.refusal.code == "realization-is-not-at-the-claimed-anchor"
    assert "admit a grand total as a daily breakdown" in refused.refusal.detail


def test_a_finalized_value_is_not_the_structured_state_the_family_retains(mme, fams):
    """**The HLL lesson as a fidelity check.** A provider handing back an estimate where the family retains
    a sketch may well have computed the right number — and what the family retains is what later
    continuation composes over, so the substitution is undetectable after admission."""
    finalized = _state(mme, "distinct_customers", EX.BY_DAY, {("D1",): 4}, value_form=SCALAR)
    refused = mme.realizations.adjudicate(_offer(mme, "distinct_customers", EX.BY_DAY, finalized))
    assert not refused and refused.refusal.code == "realization-value-form-mismatch"
    assert "THE PROVIDER MAY WELL HAVE COMPUTED THE RIGHT NUMBER" in refused.refusal.detail
    assert STRUCTURED in refused.refusal.detail


def test_a_realization_may_declare_the_data_state_and_not_the_instance(mme, fams):
    """The one axis a realization MAY declare is which established material it carries. Every other governed
    axis must agree with the registered declaration."""
    state = _state(mme, "revenue", EX.BY_DAY, {("D1",): 1.0})

    # a different DATA STATE is fine — that is the realization's to say
    restated = replace(state, instance=state.instance.with_data_state("load:later@09:00Z"))
    assert mme.realizations.adjudicate(_offer(mme, "revenue", EX.BY_DAY, restated))

    # a different MANIFOLD is not
    foreign = replace(state, instance=replace(state.instance, manifold="acme.commerce"))
    refused = mme.realizations.adjudicate(_offer(mme, "revenue", EX.BY_DAY, foreign))
    assert not refused and refused.refusal.code == "realization-instance-mismatch"
    assert "WHAT IT MAY DECLARE IS THE DATA STATE" in refused.refusal.detail


def test_a_claim_inconsistent_about_its_own_origin_is_not_evidence(mme, fams):
    """Which provider's material this is decides whether it is interchangeable with another's, so an offer
    whose realization standing names someone else cannot be evidence about anything."""
    state = _state(mme, "revenue", EX.BY_DAY, {("D1",): 1.0})
    refused = mme.realizations.adjudicate(
        _offer(mme, "revenue", EX.BY_DAY, state,
               realization=RealizationStanding(provider="somebody-else")))
    assert not refused and refused.refusal.code == "realization-standing-disagrees-with-the-offerer"


# ══ D · MISMATCHES LAND AT THE LAYER THAT OWNS THEM (§6, §G) ═══════════════════════════════════════
def test_an_unlawful_anchor_is_refused_by_STANDING_and_the_refusal_is_not_restated(mme, fams):
    """**§6.** A target outside the continuation region is not a fidelity failure and is not dressed as one:
    the authority delegates the question and returns the standing's refusal verbatim."""
    mme.establish_root(fams["on_hand"], EX.LEVELS)
    unlawful = _state(mme, "on_hand", EX.BY_STORE, {("S1",): 42})

    refused = mme.realizations.adjudicate(_offer(mme, "on_hand", EX.BY_STORE, unlawful))
    assert not refused
    assert refused.refusal.code == "outside-continuation-region"        # the STANDING's code, not ours
    assert not refused.refusal.code.startswith("realization-")

    direct = mme.authorizer.authorize_standing(fams["on_hand"], EX.BY_STORE)
    assert refused.refusal.detail == direct.refusal.detail              # verbatim


def test_a_wrong_build_is_refused_by_ADMISSION_and_not_by_fidelity(mme, fams):
    """**§G.** Build and witness coherence is cache coherence, so `put` owns it. The authority passes both
    down and a faithful claim from the wrong world is caught there."""
    mme.establish_root(fams["revenue"], EX.ORDERS)
    state = _state(mme, "revenue", EX.BY_DAY, {("D1",): 175.0, ("D2",): 325.0})

    stale = mme.realizations.adjudicate(
        _offer(mme, "revenue", EX.BY_DAY, state, build="andfam.commerce@build-99"))
    assert stale                                                       # FAITHFUL — it is what it says
    refused = RealizationManager.establish(mme, stale.credential)
    assert not refused and refused.code == "off-build-material"         # …and refused at admission
    assert "cross into one by being present" in refused.detail


def test_a_stale_witness_is_refused_by_ADMISSION_too(mme, fams):
    """The same, at per-object granularity: a value realized against a declaration that has since moved."""
    mme.establish_root(fams["revenue"], EX.ORDERS)
    state = _state(mme, "revenue", EX.BY_DAY, {("D1",): 175.0, ("D2",): 325.0})
    adjudicated = mme.realizations.adjudicate(
        _offer(mme, "revenue", EX.BY_DAY, state, witness="cw-1:some-earlier-declaration"))
    assert adjudicated
    refused = RealizationManager.establish(mme, adjudicated.credential)
    assert not refused and refused.code == "off-build-material"


def test_want_of_state_is_evidence_and_a_condition_rather_than_a_fidelity_failure(mme):
    """**§G's last row, and the answer is not a refusal.** A provider may faithfully realize a family value
    that participates somewhere its required value is not established — that is what the world says. The
    realization is faithful; the value is held with the standing recorded; any reduction over the affected
    domain is refused where it happens.

    The columnar substrate is where this is representable, and §K records that the in-memory one cannot say
    it at all."""
    from columna_platform.columnar import exhibit as CEX

    engine, _block = CEX.build(settled=False, data_state="load:orders@08:00Z")
    held = engine.materializations.select("revenue", anchor=CEX.SALE_AT)[0]
    assert held.value.wants_state

    offer = RealizationOffer(
        provider="warehouse", family_id="revenue", anchor=CEX.SALE_AT, value=held.value,
        instance=held.value.instance, realization=RealizationStanding(provider="warehouse"),
        establishment=Establishment(INDEPENDENT),
        build=engine.build.reference, witness=engine.authority.witness_of("revenue").digest)

    adjudicated = engine.realizations.adjudicate(offer)
    assert adjudicated, adjudicated.refusal                            # FAITHFUL
    assert [c.code for c in adjudicated.credential.conditions] == ["realized-with-want-of-state"]
    detail = adjudicated.credential.conditions[0].detail
    assert "The realization is FAITHFUL" in detail
    assert "not `NA`, not zero and not nonparticipation" in detail


# ══ E · ORDINARY ADMISSION, NO PRIVILEGED SHORTCUT (§4, §F) ════════════════════════════════════════
def test_the_adjudicated_claim_enters_through_the_ordinary_cache_door(mme, fams):
    """**§F.** One call to `mme.put`, with the standing the adjudication checked against — not a second one
    minted at the door — and with the environment the claim stated so `put` can own coherence."""
    mme.establish_root(fams["revenue"], EX.ORDERS)
    state = _state(mme, "revenue", EX.BY_DAY, {("D1",): 175.0, ("D2",): 325.0})
    adjudicated = mme.realizations.adjudicate(_offer(mme, "revenue", EX.BY_DAY, state))

    seen = {}
    real = mme.put

    def watched(value, standing, **kw):
        seen.update(value=value, standing=standing, **kw)
        return real(value, standing, **kw)

    mme.put = watched                                                  # type: ignore[method-assign]
    admission = RealizationManager.establish(mme, adjudicated.credential)

    assert admission
    assert seen["value"] is state
    assert seen["standing"] is adjudicated.credential.standing
    assert seen["establishment"].kind == INDEPENDENT
    assert seen["build"] == mme.build.reference
    assert seen["witness"] == mme.witness_of("revenue").digest
    assert seen["realization"].provider == "warehouse"


def test_the_realization_axis_finally_records_the_provider_that_realized_it(mme, fams):
    """**The recon's finding, closed.** Every admission used to stamp the ENGINE's `RealizationStanding`, so
    two providers' material landed under one identical token and `RetentionKey`'s realization axis — which
    exists precisely so an approximate provider's value is not interchangeable with an exact one's —
    recorded the wrong thing about every realized value."""
    mme.establish_root(fams["revenue"], EX.ORDERS)
    state = _state(mme, "revenue", EX.STORE_DAY, {("S1", "D1"): 175.0})
    adjudicated = mme.realizations.adjudicate(
        _offer(mme, "revenue", EX.STORE_DAY, state, provider="warehouse-a"))
    admission = RealizationManager.establish(mme, adjudicated.credential)
    assert admission

    held = mme.materialization(admission.id)
    assert held.realization.provider == "warehouse-a"
    assert held.realization.provider != mme.realization.provider       # NOT the engine's
    assert any(k.provider == "warehouse-a" for k in mme.held)


def test_backend_origin_overrides_no_ordinary_check(mme, fams):
    """**§4.** Duplicate-current disagreement, build compatibility, the lifecycle and the entitlement
    question all apply to realized material exactly as to locally derived material."""
    mme.establish_root(fams["revenue"], EX.ORDERS)
    served = mme.measure(fams["revenue"], EX.BY_DAY)
    assert served.served
    before = dict(served.value.cells)

    disagreeing = _state(mme, "revenue", EX.BY_DAY, {("D1",): 999.0, ("D2",): 1.0})
    adjudicated = mme.realizations.adjudicate(_offer(mme, "revenue", EX.BY_DAY, disagreeing))
    assert adjudicated                                                 # the claim is faithful …
    refused = RealizationManager.establish(mme, adjudicated.credential)
    assert not refused and refused.code == "duplicate-current-disagreement"   # … and refused anyway
    assert dict(mme.measure(fams["revenue"], EX.BY_DAY).value.cells) == before


# ══ F · CAPABILITY ≠ FIDELITY ≠ AUTHORIZATION (§8, §H, §I) ═════════════════════════════════════════
def test_backend_capability_does_not_establish_fidelity(mme, fams):
    """**§H.** A provider mechanically capable of producing the value still fails when its particular
    realization is not the claimed object. The estate executed successfully; the claim is still refused."""
    from columna_platform.kernel import RealizationProposal

    class CapableButWrong:
        """Executes perfectly, and hands back the wrong thing — the interesting failure."""

        name = "capable-warehouse"

        def propose(self, requirement):
            yield RealizationProposal(
                provider=self.name, family_id=requirement.family_id, anchor=requirement.target,
                realization=RealizationStanding(provider=self.name),
                handle=(requirement.build, requirement.witness))

        def realize(self, proposal):
            build, witness = proposal.handle
            # a perfectly good TOTAL, offered as a per-day breakdown
            return RealizationOffer(
                provider=self.name, family_id="revenue", anchor=EX.BY_DAY,
                value=_state(mme, "revenue", EX.TOTAL, {(): 500.0}),
                instance=mme.instance_of("revenue"),
                realization=RealizationStanding(provider=self.name),
                establishment=Establishment(INDEPENDENT), build=build, witness=witness)

    estate = CapableButWrong()
    manager = RealizationManager(estate)
    requirement = mme.requirement_for(fams["revenue"], EX.BY_DAY).requirement
    proposals = manager.propose(requirement)
    assert len(proposals) == 1                                         # it CAN do it, it says

    offer = manager.realize(proposals.proposals[0])                    # and it executes without error
    refused = mme.realizations.adjudicate(offer)
    assert not refused and refused.refusal.code == "realization-is-not-at-the-claimed-anchor"


def test_fidelity_does_not_grant_continuation_authorization(mme, fams):
    """**§I.** A faithful realization at `F@A` licenses admission of that value and nothing about what may be
    continued from it. B-0b owns that, and it still says no."""
    mme.establish_root(fams["on_hand"], EX.LEVELS)
    lawful = _state(mme, "on_hand", EX.BY_DAY, {("D1",): 10, ("D2",): 12})

    adjudicated = mme.realizations.adjudicate(_offer(mme, "on_hand", EX.BY_DAY, lawful))
    assert adjudicated                                                 # faithful, at a LAWFUL anchor
    assert RealizationManager.establish(mme, adjudicated.credential)   # and admitted

    # …and continuing from it to an anchor the law does not admit is still unauthorized
    assert not mme.authorizer.authorize(fams["on_hand"], EX.TOTAL)
    assert not mme.measure(fams["on_hand"], EX.TOTAL).served


def test_the_three_claims_are_three_distinct_types(mme, fams):
    """**§J.** Operation authorization ≠ target standing ≠ realization fidelity. Distinct types, distinct
    minters' questions, and the middle one is carried BY the third because fidelity presupposes it."""
    from columna_platform.kernel import AuthorizedFamilyContinuation, AuthorizedStanding

    continuation = mme.authorizer.authorize(fams["revenue"], EX.BY_DAY).request
    standing = mme.authorizer.authorize_standing(fams["revenue"], EX.BY_DAY).request
    state = _state(mme, "revenue", EX.BY_DAY, {("D1",): 1.0})
    credential = mme.realizations.adjudicate(_offer(mme, "revenue", EX.BY_DAY, state)).credential

    assert isinstance(continuation, AuthorizedFamilyContinuation)
    assert isinstance(standing, AuthorizedStanding)
    assert isinstance(credential, AdjudicatedRealization)
    assert len({type(continuation), type(standing), type(credential)}) == 3

    # fidelity CARRIES a standing (it presupposes one) and carries no continuation (it grants none)
    assert isinstance(credential.standing, AuthorizedStanding)
    assert not hasattr(credential, "fold")
    assert not hasattr(credential, "target")


# ══ G · THE ONE GOVERNED FACT B-1′ FOUND MISSING (§K) ══════════════════════════════════════════════
def test_the_requirement_now_tells_a_provider_which_declaration_to_realize_against(mme, fams):
    """**§K.** B-1′ requires a claim to state the governed environment it was made against, and the
    test-double exercise exposed that **a provider could not state it, because nothing ever told it**: the
    requirement carried `manifold`, `build`, `instance`, `law`, `value_form`, `sufficient_state` and
    `approximation` — everything else a provider is told — and not the digest of the declaration it was
    supplying for.

    It was placed on `FamilyRequirement` rather than invented inside the fidelity boundary, because that is
    the object whose whole purpose is telling a provider what governed state would satisfy a lawful request.
    Without it, a real backend could not use this door."""
    requirement = mme.requirement_for(fams["revenue"], EX.BY_DAY).requirement
    assert requirement.build == mme.build.reference
    assert requirement.witness == mme.witness_of("revenue").digest

    # and it is the fact the door compares, so a provider that restates it is admissible
    mme.establish_root(fams["revenue"], EX.ORDERS)
    state = _state(mme, "revenue", EX.BY_DAY, {("D1",): 175.0, ("D2",): 325.0})
    offer = _offer(mme, "revenue", EX.BY_DAY, state,
                   build=requirement.build, witness=requirement.witness)
    assert RealizationManager.establish(mme, mme.realizations.adjudicate(offer).credential)


def test_the_in_memory_substrate_still_cannot_EXPRESS_want_of_state(mme):
    """**The second missing fact, reported and NOT invented** (§9).

    `FamilyState` — the in-memory substrate's family value — carries `cells` and no participation or support
    representation at all. So an in-memory provider cannot express *"this point participates and its
    required value is not established"*; only the columnar substrate can, through `ColumnStanding`.

    B-1′ does not add one. A support representation for the in-memory substrate is a governed decision about
    what that substrate's family value IS, not a detail of this door, and inventing it here would have put
    an analytical fact in a boundary module. Recorded as a test so the gap is discoverable rather than
    folklore."""
    from columna_platform.columnar.mme import ColumnarFamilyState

    in_memory = {f.name for f in FamilyState.__dataclass_fields__.values()}
    columnar = {f.name for f in ColumnarFamilyState.__dataclass_fields__.values()}

    assert "standing" in columnar and "standing" not in in_memory
    assert not hasattr(FamilyState, "wants_state")
    assert hasattr(ColumnarFamilyState, "wants_state")

    state = _state(mme, "revenue", EX.BY_DAY, {("D1",): 1.0})
    assert getattr(state, "wants_state", None) is None                 # nothing to read


# ══ H · NOTHING OUT OF SCOPE ARRIVED ══════════════════════════════════════════════════════════════
def test_no_backend_semantics_entered_any_governed_module():
    """**§7.** After B-1′ the MME still knows nothing about SQL, tables, columns, connection strings, ADBC,
    DuckDB, query plans or provider-specific verification — and neither does the fidelity boundary."""
    from columna_platform.columnar import mme as columnar_mme_module
    from columna_platform.kernel import mme as kernel_mme_module
    from columna_platform.kernel import realization_manager as manager_module

    code = "".join(_code_only(m) for m in (kernel_mme_module, columnar_mme_module,
                                           fidelity_module, manager_module))
    for banned in ("duckdb", "adbc", "psycopg", "sqlalchemy", "sqlite3", "iceberg", "postgres",
                   "connect(", "cursor", "query_plan", "table_name", "connection_string",
                   "pickle", "open("):
        assert banned not in code.lower(), banned
    # SQL is banned in its own casing — `" from "` in lowercase is ordinary English and would make this a
    # test about prose rather than about backend semantics (R-1's ban has the same shape for the same reason)
    for sql in ("SELECT ", " FROM ", "GROUP BY", "JOIN "):
        assert sql not in code, sql


def test_the_three_exhibits_still_run_green(capsys):
    from columna_platform.columnar import exhibit as columnar_exhibit
    from columna_platform.frameql import exhibit as frameql_exhibit
    from columna_platform.kernel import exhibit as kernel_exhibit

    for module in (kernel_exhibit, columnar_exhibit, frameql_exhibit):
        module.main() if hasattr(module, "main") else module.run()
    assert "ALL CHECKS PASSED" in capsys.readouterr().out


# ══ M · FIVE QUESTIONS, FIVE OWNERS ══════════════════════════════════════════════════════════════
#
# Ruled (Huayin, 2026-09-30): the serving ladder is five questions, and the whole B-0a/B-0b/B-1' sequence
# exists so that each is asked ONCE by ONE owner. The ladder is now recorded in `kernel.__doc__`, and a
# recorded architecture nobody measures drifts from the code the week after it is written — so this pins
# both halves: the record names the five in order, and every owner it names is a real callable.


LADDER = (
    ("analytical authorization", "what may be requested"),
    ("physical realization", "what the estate actually produced"),
    ("realization fidelity", "is that result really the claimed `F@A`?"),
    ("MME admission", "may this enter this cache/build?"),
    ("MME fulfillment", "can held state answer the request?"),
)


def test_the_recorded_ladder_names_the_five_questions_in_the_order_they_are_descended():
    import columna_platform.kernel as kernel

    doc = kernel.__doc__
    positions = []
    for question, _ in LADDER:
        assert question in doc, f"the ladder no longer records {question!r}"
        positions.append(doc.index(question))
    assert positions == sorted(positions), (
        "the recorded ladder is out of order. It is DESCENDED: authorization precedes realization "
        "precedes fidelity precedes admission precedes fulfillment, and the order is the architecture")


def test_every_owner_the_ladder_names_is_a_real_distinct_callable():
    """Five questions, five owners, and no owner answering two of them.

    `MME.put` and `MME.fulfill` live on one class — the residual B-0 recorded, since this class is still
    both the Manifold build authority and the cache — but they are two METHODS, and that they are two is
    what keeps admission from consulting held state and fulfillment from admitting anything."""
    from columna_platform.kernel import MME, ContinuationAuthority, RealizationAuthority
    from columna_platform.kernel.realization_manager import RealizationManager

    owners = {
        "analytical authorization": ContinuationAuthority.authorize,
        "physical realization": RealizationManager.realize,
        "realization fidelity": RealizationAuthority.adjudicate,
        "MME admission": MME.put,
        "MME fulfillment": MME.fulfill,
    }
    assert len(owners) == len(LADDER)
    assert all(callable(owner) for owner in owners.values())
    # Five distinct functions. A ladder whose rungs are the same object is one question with five names.
    assert len({id(owner) for owner in owners.values()}) == 5
