"""test_j0_jurisdiction_closure.py — **J-0: two builds in one process, and nothing crosses.**

    Ruled (Huayin, 2026-10-01): *"A meaning-bearing declaration has authority in a runtime build only
    when it is the declaration constituted by that build. Nothing acquires analytical authority merely
    by being passed in, by claiming the right Manifold name, or by sharing a process with an
    authority."*

**THE ASYMMETRY J-0 EXISTS TO REMOVE.** Values already carried their jurisdiction: every `FamilyState`
holds an `AnalyticalInstance`, and `same_but_for_data_state` compares manifold, universe, participation,
scope and `constitution_context` at every combination. Declarations carried nothing. A `MeasureFamily`
from another build, handed to `measure`, was authorized against the receiving engine's law and stamped
with the receiving engine's build — and the only jurisdiction check in the kernel, `_require_own`, ran
at registration, which is the one path such an object never takes.

That was survivable only because every engine in the process resolved through one law registry: the
constitution was mixed between identical things. **B-4a″(ii) makes selections differ, and then the same
path authorizes a family against the wrong member's region and algebra.** Hence this unit first.

**THE TEST IS CONSTITUTION, NOT SELF-DESCRIPTION.** `subject()` compares against what this build
registered rather than asking the object which Manifold it claims. That is stronger three ways: it
catches an object that merely claims the right name; it catches a same-Manifold object whose root or
parameters differ from the constituted one — which is exactly what the callers go on to read, and which
a name check waves through; and it needs no new field.

**AND SHARING MUST SURVIVE.** Half of these tests exist to stop the correction going too far. A
`Universe`, an `Anchor`, a `LawRegistry` and a `ProviderProfile` are installation-shared governed
resources; they carry no Manifold and must not acquire one. Two jurisdictions sharing geometry and law
vocabulary is the architecture, not a leak.
"""
from __future__ import annotations

import inspect
from dataclasses import fields, replace

import pytest

from columna_platform.kernel import (
    IN_MEMORY,
    MME,
    REGISTRY,
    Anchor,
    Establishment,
    ExpressionEvaluator,
    KernelRefusal,
    MaterializationStore,
    RealizationStanding,
    Universe,
)
from columna_platform.kernel import exhibit as EX
from columna_platform.kernel import mme as mme_module
from columna_platform.kernel.fulfillment import FulfillmentCoordinator
from columna_platform.kernel.law import LawRegistry
from columna_platform.kernel.materialization import INDEPENDENT, ManifoldBuild
from columna_platform.kernel.realization import ProviderProfile
from columna_platform.kernel.realization_manager import RealizationManager, RealizationOffer

OTHER = "acme.commerce"


@pytest.fixture
def a():
    """Jurisdiction A — the exhibit's own world, warm."""
    return EX.build()


@pytest.fixture
def b():
    """Jurisdiction B — a different Manifold, in this process, over the SAME `Universe`, the SAME
    `LawRegistry` and the SAME `ProviderProfile`. That sharing is the point: it is what makes the
    engines' separation a governed fact rather than a consequence of them not meeting."""
    engine = MME(EX.COMMERCE, REGISTRY, IN_MEMORY, manifold=OTHER, build=EX.BUILD)
    for family in EX._families():
        engine.register_family(replace(family, manifold=OTHER))
    return engine


def _rooted(engine, family_id):
    engine.establish_root(engine.family(family_id), EX.ORDERS)
    return engine.family(family_id)


# ══ 1 · DECLARATIONS DO NOT CROSS ════════════════════════════════════════════════════════════════
def test_a_foreign_family_cannot_be_measured(a, b):
    with pytest.raises(KernelRefusal) as exc:
        a.measure(b.family("revenue"), EX.BY_DAY)
    assert exc.value.code == "foreign-declaration"
    assert "not the declaration build" in exc.value.detail


def test_a_declaration_that_CLAIMS_the_right_manifold_is_still_refused(a):
    """**Why the test is constitution and not `obj.manifold == self.manifold`.** This object names the
    right world and was never constituted in it; a name check admits it, and `authorize` then reads
    `root` off it while taking the law from the local registry."""
    impostor = replace(a.family("revenue"), participation="whatever I say it is")
    assert impostor.manifold == a.manifold
    with pytest.raises(KernelRefusal) as exc:
        a.measure(impostor, EX.BY_DAY)
    assert exc.value.code == "foreign-declaration"


def test_a_foreign_family_cannot_establish_a_root(a, b):
    with pytest.raises(KernelRefusal) as exc:
        a.establish_root(b.family("revenue"), EX.ORDERS)
    assert exc.value.code == "foreign-declaration"


def test_a_foreign_expression_cannot_be_evaluated(a, b):
    for expression in EX._expressions():
        b.register_expression(replace(expression, manifold=OTHER))
    with pytest.raises(KernelRefusal) as exc:
        ExpressionEvaluator(a).evaluate(b.expression("average_order_value"), EX.BY_DAY)
    assert exc.value.code == "foreign-declaration"


def test_a_foreign_family_cannot_be_fulfilled(a, b):
    """The coordinator normalises through `subject`, so the funnel holds one layer up."""
    coordinator = FulfillmentCoordinator(a, realization=RealizationManager())
    with pytest.raises(KernelRefusal) as exc:
        coordinator.fulfill(b.family("revenue"), EX.BY_DAY)
    assert exc.value.code == "foreign-declaration"


def test_an_unconstituted_name_is_told_so_rather_than_called_foreign(a):
    stranger = replace(a.family("revenue"), family_id="nothing_here")
    with pytest.raises(KernelRefusal) as exc:
        a.measure(stranger, EX.BY_DAY)
    assert exc.value.code == "not-constituted"


# ══ 2 · CREDENTIALS DO NOT CROSS ═════════════════════════════════════════════════════════════════
def test_a_standing_minted_by_another_authority_is_refused(a, b):
    _rooted(b, "revenue")
    foreign = b.authorizer.authorize_standing("revenue", EX.SALE_AT).request
    held = a.materializations.select("revenue", anchor=EX.SALE_AT)[0]
    admission = a.put(held.value, foreign)
    assert not admission and admission.code == "foreign-credential"


def test_an_adjudication_by_another_authority_cannot_be_established(a, b):
    _rooted(b, "revenue")
    value = b.materializations.select("revenue", anchor=EX.SALE_AT)[0].value
    offer = RealizationOffer(
        provider="warehouse", family_id="revenue", anchor=EX.SALE_AT, value=value,
        instance=value.instance, realization=RealizationStanding(provider="warehouse"),
        establishment=Establishment(INDEPENDENT),
        build=b.build.reference, witness=b.witness_of("revenue").digest)
    credential = b.realizations.adjudicate(offer)
    assert credential, credential.refusal

    with pytest.raises(KernelRefusal) as exc:
        RealizationManager.establish(a, credential.credential)
    assert exc.value.code == "foreign-credential"
    assert b.realizations.name in exc.value.detail or a.realizations.name in exc.value.detail


def test_each_authority_holds_its_own_mint(a, b):
    assert a.authorizer._mint is not b.authorizer._mint
    assert a.realizations._mint is not b.realizations._mint
    granted = a.authorizer.authorize_standing("revenue", EX.SALE_AT).request
    assert a.authorizer.issued(granted) and not b.authorizer.issued(granted)


# ══ 3 · VALUES DO NOT CROSS ══════════════════════════════════════════════════════════════════════
def test_a_value_established_in_another_build_cannot_be_admitted(a, b):
    _rooted(b, "revenue")
    foreign_value = b.materializations.select("revenue", anchor=EX.SALE_AT)[0].value
    admission = a.admit(foreign_value)
    assert not admission and admission.code == "foreign-material"


def test_a_value_established_in_another_build_cannot_be_retained(a, b):
    _rooted(b, "revenue")
    foreign_value = b.materializations.select("revenue", anchor=EX.SALE_AT)[0].value
    with pytest.raises(KernelRefusal) as exc:
        a.retain(foreign_value)
    assert exc.value.code == "foreign-material"


def test_put_refuses_an_off_build_standing_WITH_THE_KWARGS_OMITTED(a):
    """**The case that passed before J-0.** `put`'s `build`/`witness` guards compare two values the
    offerer supplied against each other, and both default to `None`, so the ordinary path performed no
    build check at all. This asks the question those could not: is the standing for THIS world."""
    successor = MME(EX.COMMERCE, REGISTRY, IN_MEMORY, manifold=EX.MANIFOLD, build="build-2")
    for family in EX._families():
        successor.register_family(family)
    successor.establish_root(successor.family("revenue"), EX.ORDERS)
    held = successor.materializations.select("revenue", anchor=EX.SALE_AT)[0]
    foreign = successor.authorizer.authorize_standing("revenue", EX.SALE_AT).request

    admission = a.put(held.value, foreign)          # no build=, no witness=
    assert not admission
    assert admission.code in ("foreign-credential", "off-build-material")


# ══ 4 · BUILDS DO NOT COLLIDE ════════════════════════════════════════════════════════════════════
def test_an_engine_cannot_be_constructed_without_an_explicit_identity():
    with pytest.raises(TypeError):
        MME(EX.COMMERCE, REGISTRY, IN_MEMORY)
    with pytest.raises(TypeError):
        MME(EX.COMMERCE, REGISTRY, IN_MEMORY, manifold=EX.MANIFOLD)
    signature = inspect.signature(MME.__init__)
    assert signature.parameters["manifold"].default is inspect.Parameter.empty
    assert signature.parameters["build"].default is inspect.Parameter.empty


def test_a_store_from_another_build_cannot_be_attached(a):
    foreign = MaterializationStore(ManifoldBuild(manifold=OTHER, build=EX.BUILD))
    with pytest.raises(KernelRefusal) as exc:
        a.attach_store(foreign)
    assert exc.value.code == "foreign-store"


def test_a_service_cannot_be_wired_to_another_engines_machinery(a, b):
    from columna_platform.frameql.serving import FrameQLService

    with pytest.raises(KernelRefusal) as exc:
        FrameQLService(a, evaluator=ExpressionEvaluator(b))
    assert exc.value.code == "foreign-collaborator"


# ══ 5 · SHARED RESOURCES STAY SHARED — the guard against over-correcting ═════════════════════════
def test_two_jurisdictions_share_one_universe_and_one_law_vocabulary(a, b):
    assert a.universe is b.universe
    assert a.laws is b.laws
    assert a.provider is b.provider
    assert a.measure(a.family("revenue"), EX.BY_DAY).served
    _rooted(b, "revenue")
    assert b.measure(b.family("revenue"), EX.BY_DAY).served


def test_neither_anchors_nor_universes_acquired_a_manifold(a, b):
    """J-0 must not make shared governed geometry jurisdiction-local. Composition inherits a parent's
    universes **by reference** — *"the same named objects, so co-universality is verifiable by
    reference"* — and a manifold field here would break that."""
    assert "manifold" not in {f.name for f in fields(Anchor)}
    assert "manifold" not in {f.name for f in fields(Universe)}
    assert a.universe.anchor({"day"}) == b.universe.anchor({"day"}) == EX.BY_DAY


def test_the_shared_catalogues_are_immutable_by_construction(a):
    """They claimed immutability in prose and had none; one object is shared by every engine."""
    import dataclasses

    with pytest.raises(dataclasses.FrozenInstanceError):
        REGISTRY.version = "2"
    with pytest.raises(dataclasses.FrozenInstanceError):
        IN_MEMORY.name = "impostor"
    assert isinstance(REGISTRY, LawRegistry) and isinstance(IN_MEMORY, ProviderProfile)


# ══ 6 · NO RUNTIME CROSS-MANIFOLD MODE WAS INTRODUCED ════════════════════════════════════════════
def test_there_is_no_runtime_admitted_manifold_set(a, b):
    """**Ruling 1, as a standing guard.** Cross-Manifold use is composition into a new governed build,
    which is a BUILD-TIME act: the composed Manifold constitutes its own declarations and is queried
    like any other. There is therefore no runtime set of additional Manifolds an engine will honour,
    and the only way to widen what a build may interpret is to constitute it in that build.

    If a future change adds an allowlist, this fails — which is the point. Widening belongs in the
    build constitution, not in the runtime jurisdiction predicate."""
    source = inspect.getsource(mme_module)
    for smell in ("admitted_manifolds", "allowed_manifolds", "trusted_manifolds", "parent_manifold"):
        assert smell not in source

    # the only widening there is: constitute it here. A foreign-MANIFOLD declaration is refused even
    # at the one door that does accept declarations.
    with pytest.raises(KernelRefusal) as exc:
        a.register_family(b.family("revenue"))
    assert exc.value.code == "foreign-manifold"

    # and a composed build constitutes its OWN declaration, which is an ordinary registration
    composed = MME(EX.COMMERCE, REGISTRY, IN_MEMORY, manifold="andfam.composed", build="build-1")
    own = replace(a.family("revenue"), manifold="andfam.composed")
    composed.register_family(own)
    assert composed.measure(own, EX.SALE_AT).refusal.code == "unanswerable"   # constituted, not yet rooted
    composed.establish_root(own, EX.ORDERS)
    assert composed.measure(own, EX.BY_DAY).served


def test_frame_ql_still_refuses_to_name_another_manifold(a):
    """Frame-QL 1.0: *"A shared planner routes each statement to exactly one Manifold."* The Platform
    subset refuses `FROM` by name, so there is no cross-Manifold addressing at the user surface."""
    from columna_platform.frameql.serving import FrameQLService

    answer = FrameQLService(a).serve("FROM other_manifold SELECT revenue AT {day}")
    assert answer.frame is None
    assert answer.refusal is not None
    assert "from" in answer.refusal.detail.lower()
