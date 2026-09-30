"""
test_b0b_authorized_continuation.py — **B-0b: the constitution decides what may be requested; the cache
decides whether it can fulfill the request.**

    *"MME does not determine whether a family continuation is analytically authorized. MME determines whether
    held family materialization can fulfill an already-authorized continuation request correctly and
    consistently."*  — Huayin, 2026-09-29

        Manifold / Resolver / analytical authorization
                ↓
        Authorized family-continuation request
                ↓
        MME
                ↓
        materialization suitability + execution

THE DESIGN TEST, AND IT IS §J OF THE STOP CONDITION
---------------------------------------------------
    *"Changing a family's continuation region may change which authorized requests are issued. It must not
    require changing MME logic."*

§E below executes that literally: it constructs the same family under three different continuation regions
and shows that which requests exist changes while the engines' code does not. The converse is §F: changing
the cache population changes fulfillment and leaves authorization untouched.

WHAT THIS SUITE PROVES, SECTION BY SECTION
------------------------------------------
    A  the boundary is structural — a request cannot be manufactured (§C of the stop condition)
    B  the constitution left both cache engines (§D, §E)
    C  what remains in MME, and why each is a materialization/execution question (§H)
    D  `not-reachable` stayed; `outside-continuation-region` left (§I)
    E  changing the region changes which requests exist, not MME logic (§J)
    F  provider capability cannot create analytical permission (§K)
    G  `requirement_for` stayed a separate question (§L)
    H  the three constitutional leaks are gone (§D, §F, §G)

NOT EXERCISED, DELIBERATELY: no persistence, no backend, no ADBC, no cache-cost optimizer, no expression
caching, no new DataFusion kernels.
"""
from __future__ import annotations

import ast
import inspect
from dataclasses import replace

import pytest

from columna_platform.columnar import exhibit as CEX
from columna_platform.columnar import mme as columnar_mme_module
from columna_platform.kernel import (
    MME,
    REGISTRY,
    AuthorizedFamilyContinuation,
    AuthorizedStanding,
    ContinuationAuthority,
    ContinuationRegion,
    FamilyPoint,
    FamilyState,
    FoldRequirement,
    KernelRefusal,
    LawRegistry,
    MeasureFamily,
    Retained,
    RetentionKey,
)
from columna_platform.kernel import authorization as authorization_module
from columna_platform.kernel import exhibit as EX
from columna_platform.kernel import mme as kernel_mme_module
from columna_platform.kernel.builtins import IN_MEMORY
from columna_platform.kernel.law import POPULATION, SCALAR, VALUE_BEARING

LOAD = "load:orders@08:00Z"


def _code_only_fn(fn) -> str:
    """One function's executable text, docstring stripped — so a ban on reading the constitution is not
    tripped by the prose explaining that it is not read."""
    tree = ast.parse(inspect.getsource(fn).lstrip())
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            body = node.body
            if (body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant)
                    and isinstance(body[0].value.value, str)):
                node.body = body[1:] or [ast.Pass()]
    return ast.unparse(tree)


def _code_only(module) -> str:
    """Executable text only — docstrings and comments stripped, so a ban cannot be tripped by the prose that
    explains it. Same helper as the E-1/E-3, F-1, R-1 and B-0a suites."""
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
    return EX.build()


@pytest.fixture
def fams():
    revenue, order_count, audited, distinct, on_hand, gauge = EX._families()
    return dict(revenue=revenue, order_count=order_count, audited=audited, distinct=distinct,
                on_hand=on_hand, gauge=gauge)


# ══ A · THE BOUNDARY IS STRUCTURAL, NOT A CONVENTION (§C) ══════════════════════════════════════════
def test_a_request_cannot_be_manufactured_by_assembling_its_fields(mme, fams):
    """**The property the ruling asks for, exactly:**

        *"ordinary MME callers cannot manufacture analytical authority merely by assembling
        `family + target + addition`."*

    So a caller who has every field and assembles them gets a governed refusal naming the component that
    should have minted it — not a usable request. This is structural ownership rather than security theatre:
    the one place able to mint is the one place that reads the constitution, which makes "authorized" and
    "constitutionally checked" the same event."""
    fold = FoldRequirement(execution_mode="grouped", composition="addition",
                           merge_realization="SUM", required_input_value_form=SCALAR,
                           fold_shape=VALUE_BEARING)
    standing = mme.authorizer.authorize_standing(fams["revenue"], EX.BY_DAY).request

    with pytest.raises(KernelRefusal) as refused:
        AuthorizedFamilyContinuation(
            family_id="revenue", target=EX.BY_DAY, instance=mme.instance_of("revenue"),
            data_state=None, fold=fold, standing=standing, build=mme.build.reference,
            witness=mme.witness_of("revenue").digest)
    assert refused.value.code == "unauthorized-continuation"
    assert "ContinuationAuthority.authorize" in refused.value.detail
    assert "is not authorization: it is the shape of authorization without the act" in refused.value.detail


def test_a_standing_cannot_be_manufactured_either(mme):
    """The admission-side twin. A cache that accepted a self-asserted standing could be told anything."""
    with pytest.raises(KernelRefusal) as refused:
        AuthorizedStanding(family_id="on_hand", anchor=EX.BY_STORE, build=mme.build.reference,
                           witness="whatever", at_root=False)
    assert refused.value.code == "unauthorized-standing"


def test_the_mint_is_module_private_and_unexported(mme, fams):
    """The capability is one module-private object. It is not in `__all__`, not on the authority, and not
    reachable from any governed type — so "obtain a mint" is not a move an ordinary caller has."""
    assert "_MINT" not in authorization_module.__all__
    assert not hasattr(ContinuationAuthority, "_MINT")
    granted = mme.authorizer.authorize(fams["revenue"], EX.BY_DAY).request
    assert granted.issued_by is authorization_module._MINT     # the private name, reached deliberately
    assert type(granted.issued_by).__name__ == "_Mint"


def test_a_minted_request_cannot_be_retargeted_by_replacing_its_fields(mme, fams):
    """`dataclasses.replace` re-runs `__post_init__`, so a granted request cannot be edited into one for a
    different location while keeping its authorization. The mark travels with the object, not with the
    caller."""
    granted = mme.authorizer.authorize(fams["revenue"], EX.BY_DAY).request
    retargeted = replace(granted, target=EX.TOTAL)              # still marked — replace keeps `issued_by`
    # …so the guard that matters is the one on ADMISSION: the paired standing no longer covers the target
    assert retargeted.standing.anchor == EX.BY_DAY != retargeted.target
    state = mme.measure(fams["revenue"], EX.TOTAL).value
    refused = mme.put(state, retargeted.standing)
    assert not refused and refused.code == "standing-does-not-cover-this-material"
    assert "An authorization is for one analytical location" in refused.detail


def test_the_cache_door_cannot_be_reached_without_a_standing(mme, fams):
    """`put` has no default for its authorization. There is no ordinary path into the cache that takes raw
    family/target/operation arguments — `measure` and `admit` both mint first, and neither reconstructs the
    permission logic they replaced."""
    import inspect as _inspect

    put = _inspect.signature(MME.put)
    assert "standing" in put.parameters
    assert put.parameters["standing"].default is _inspect.Parameter.empty

    fulfill = _inspect.signature(MME.fulfill)
    assert list(fulfill.parameters) == ["self", "request"]
    with pytest.raises(TypeError):
        mme.fulfill()                                          # type: ignore[call-arg]


# ══ B · THE CONSTITUTION LEFT BOTH CACHE ENGINES (§D, §E) ══════════════════════════════════════════
def test_neither_engine_reads_the_continuation_region(mme):
    """**§E: the fate of `ContinuationRegion` inside MME. It is gone.**

    Every clause of the ruling's §1, as one assertion each. MME must not read `ContinuationRegion`, call
    `region.admits`, receive an entitlement wrapper and evaluate it, reconstruct permission from family law,
    or infer lawful continuation from provider capability."""
    for module in (kernel_mme_module, columnar_mme_module):
        code = _code_only(module)
        for constitutional in ("ContinuationRegion", "region.admits(", "entitlement_holds(",
                               "cumulative_forgotten(", "ContinuationEntitlement"):
            assert constitutional not in code, f"{module.__name__} reads {constitutional}"


def test_the_region_is_read_in_exactly_one_module(mme):
    """Not merely absent from the engines — present in ONE place. Four askers became one, so a region edit
    has one site to be correct at."""
    readers = []
    for name, module in (("kernel.mme", kernel_mme_module),
                         ("columnar.mme", columnar_mme_module),
                         ("kernel.authorization", authorization_module)):
        if "entitlement_holds(" in _code_only(module):
            readers.append(name)
    assert readers == ["kernel.authorization"]


def test_adjudicate_is_a_function_of_the_candidate_and_the_requirements_only(mme):
    """**§H, as a signature.** `adjudicate` took `(candidate, family, target)` and consulted the law, because
    one of its five questions was constitutional. That question left, and with it every reason to know the
    family or the law. What remains cannot re-derive permission because it is not given the material to."""
    import inspect as _inspect

    assert list(_inspect.signature(MME.adjudicate).parameters) == ["self", "candidate", "request"]
    executable = _code_only_fn(MME.adjudicate)
    for law_access in ("self._bound", "self._families", "self.law_of", "law.value_form",
                       "law.region", "law.continuation", "law.name", "law.fold_shape"):
        assert law_access not in executable, law_access
    # the only "law" left is the WORD, inside the provider-limit message, which names a law it was told
    assert "unrealized-law" in executable


def test_the_kernel_import_allowlist_still_holds():
    """`kernel/*.py` may import a fixed stdlib set plus `datasketches`, and `authorization.py` is a new
    kernel module — so this is the guard that could have been broken silently by adding it."""
    allowed = {"__future__", "dataclasses", "typing", "math", "abc", "enum", "functools",
               "itertools", "hashlib", "time"}
    tree = ast.parse(inspect.getsource(authorization_module))
    external = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            external |= {a.name.split(".")[0] for a in node.names}
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            external.add(node.module.split(".")[0])
    assert external <= allowed, external - allowed


# ══ C · WHAT REMAINS IN MME, AND WHY EACH IS A MATERIALIZATION/EXECUTION QUESTION (§H) ══════════════
def _request(mme, family, target):
    authorized = mme.authorizer.authorize(family, target)
    assert authorized, authorized.refusal
    return authorized.request


def _retained(mme, state):
    return Retained(key=RetentionKey(identity=state.point.family_id, anchor=state.anchor,
                                     instance=state.instance, realization=mme.realization),
                    value=state)


def test_the_four_surviving_checks_and_each_ones_jurisdiction(mme, fams):
    """The four, each exercised, with the reason it is not analytical authorization:

        sort              an expression output is not family state — a TYPE fact
        reachability      GEOMETRY: `{store}` cannot reach `{day}`; `{day}` may still be perfectly lawful
        payload adequacy  EXECUTION: a finalized scalar cannot be merged by a sketch composition
        build capability  THIS BUILD cannot run the reducer — lawful and unservable, not unlawful
    """
    revenue, distinct = fams["revenue"], fams["distinct"]

    # reachability
    by_store = mme.measure(revenue, EX.BY_STORE)
    geometric = mme.adjudicate(_retained(mme, by_store.value), _request(mme, revenue, EX.BY_DAY))
    assert geometric.code == "not-reachable"
    assert "the continuation is AUTHORIZED and another seed may well serve it" in geometric.detail

    # payload adequacy
    inadequate = FamilyState(
        point=FamilyPoint("distinct_customers", EX.BY_DAY), law="HLL_SKETCH", value_form=SCALAR,
        cells={("D1",): 4}, instance=mme.instance_of("distinct_customers"),
        forgotten_since_root=frozenset({"store", "order"}))
    payload = mme.adjudicate(_retained(mme, inadequate), _request(mme, distinct, EX.TOTAL))
    assert payload.code == "state-no-longer-sufficient"

    # build capability — the law is realized by the profile or it is not, and that is about the engine
    from columna_platform.kernel.builtins import NO_MEAN

    limited = MME(EX.COMMERCE, REGISTRY, NO_MEAN, manifold=EX.MANIFOLD)
    assert not limited.provider.realizes("MEAN")
    assert mme.provider.realizes("SUM")


def test_the_support_vector_is_consumed_and_never_explained(mme):
    """**§5 of the previous ruling, preserved under §2 of this one.** MME needs to know that a participating
    point is unsupported, because a value-bearing fold cannot produce an established value there. It does not
    need to know WHY the vector says that, and it must not ask whether carrier validity was licensed to
    establish it — that is the realization boundary's question, above.

    So: the refusal names the points and the shape, and says what it is NOT. Nothing in it reasons about
    Arrow nullability."""
    engine, _block = CEX.build(settled=False, data_state=LOAD)
    answer = engine.measure("revenue", CEX.BY_DAY)
    assert not answer.served and answer.refusal.code == "want-of-state"
    assert "not `NA`" in answer.refusal.detail
    assert "nonparticipation" in answer.refusal.detail

    # The ban is on the FULFILLMENT path. `establish`'s `support-without-a-value` guard does read
    # `values.is_valid()`, and legitimately: it runs in the INVERSE direction — refusing when the standing
    # claims MORE support than the carrier can back — which is a broken-representation check, not support
    # derived from validity. That direction is the one Ruling 1 requires; the forbidden one is
    # `support = is_valid(column)`, and it appears nowhere.
    for method in (columnar_mme_module.ColumnarMME.fulfill,
                   columnar_mme_module.ColumnarMME.adjudicate,
                   columnar_mme_module.ColumnarMME.put,
                   kernel_mme_module.MME.fulfill):
        body = _code_only_fn(method)
        for carrier_reasoning in ("is_valid", "is_null", "null_count", "nullable"):
            assert carrier_reasoning not in body, f"{method.__qualname__}: {carrier_reasoning}"

    establish = _code_only_fn(columnar_mme_module.ColumnarMME.establish)
    assert "is_valid" in establish                             # the inverse guard, and only that
    assert "support = " not in establish and "support=pc" not in establish


def test_the_cache_still_owns_selection_lifecycle_and_dependency(mme, fams):
    """The genuinely MME-internal responsibilities, unchanged: which retained instance answers, what becomes
    superseded, what a derived materialization depends on."""
    revenue = fams["revenue"]
    mme.measure(revenue, EX.BY_DAY)
    total = mme.measure(revenue, EX.TOTAL)
    assert total.served

    derived = [m for m in mme.materializations.select("revenue", anchor=EX.TOTAL)][0]
    assert derived.establishment.kind == "continued"
    assert derived.establishment.derived_from                  # it names its parent
    assert mme.materialization(derived.establishment.derived_from[0]) is not None


# ══ D · `not-reachable` STAYED; `outside-continuation-region` LEFT (§I) ════════════════════════════
def test_not_reachable_remains_a_geometric_materialization_suitability_check(mme, fams):
    """**§I, said explicitly as the ruling asks.** `not-reachable` REMAINS in MME and is a physical/geometric
    materialization-suitability check: it reports that the payload held has already forgotten the constituent
    the request needs. Constituent containment is a fact about what a cached value retains, not about what a
    Manifold permits."""
    revenue = fams["revenue"]
    by_store = mme.measure(revenue, EX.BY_STORE)
    verdict = mme.adjudicate(_retained(mme, by_store.value), _request(mme, revenue, EX.BY_DAY))

    assert verdict.code == "not-reachable"
    assert mme.measure(revenue, EX.BY_DAY).served               # the target was lawful all along
    assert mme.authorizer.authorize(revenue, EX.BY_DAY)         # and authorized all along


def test_outside_continuation_region_left_mme_as_expected(mme, fams):
    """**§I's other half.** It disappears from MME *because the authorized request cannot exist* in that
    case, which the ruling says is expected. The proof moved to the authority rather than being preserved
    for its text."""
    assert "outside-continuation-region" not in _code_only(kernel_mme_module)
    assert "outside-continuation-region" not in _code_only(columnar_mme_module)
    assert "outside-continuation-region" in _code_only(authorization_module)

    refused = mme.authorizer.authorize(fams["on_hand"], EX.TOTAL)
    assert not refused and refused.refusal.code == "outside-continuation-region"


def test_one_question_now_has_exactly_one_code(mme, fams):
    """Two spellings existed — `outside-continuation-region` from `adjudicate` and
    `anchor-outside-the-continuation-region` from `admit` — **because two components were asking one
    constitutional question.** One asker, one code; the second spelling is retired rather than kept as a
    synonym nothing can produce."""
    from columna_platform.kernel.observation import UNSUPPORTED_CODES

    assert "anchor-outside-the-continuation-region" not in UNSUPPORTED_CODES
    assert "outside-continuation-region" in UNSUPPORTED_CODES
    for module in (kernel_mme_module, columnar_mme_module, authorization_module):
        # code only: the authority's docstring RECORDS the retired spelling deliberately, because a reader
        # asking "why is there one code now?" needs the answer to be discoverable.
        assert "anchor-outside-the-continuation-region" not in _code_only(module), module.__name__

    continuation = mme.authorizer.authorize(fams["on_hand"], EX.TOTAL)
    standing = mme.authorizer.authorize_standing(fams["on_hand"], EX.BY_STORE)
    assert continuation.refusal.code == standing.refusal.code == "outside-continuation-region"


def test_a_miss_and_an_unauthorized_request_are_different_outcomes(mme, fams):
    """**§7: MME MISS has no analytical meaning.** A miss means only that the cache cannot currently satisfy
    an already-lawful request from what it holds. An unlawful target is not a miss — it never reaches the
    cache — so the two can no longer be confused, which the single old path allowed."""
    cold = MME(EX.COMMERCE, REGISTRY, IN_MEMORY, manifold=EX.MANIFOLD)
    for family in EX._families():
        cold.register_family(family)

    miss = cold.measure(fams["revenue"], EX.BY_DAY)             # lawful, simply not held
    assert not miss.served and miss.refusal.code == "unanswerable"
    assert "must be established at" in miss.refusal.detail

    unlawful = cold.measure(fams["on_hand"], EX.TOTAL)          # not lawful at all
    assert not unlawful.served and unlawful.refusal.code == "outside-continuation-region"
    assert miss.refusal.code != unlawful.refusal.code


def test_an_unauthorized_request_is_observed_as_UNSUPPORTED_and_never_as_a_miss(fams):
    """One observation per request on EVERY path, including the new one. `UNSUPPORTED` is exactly the row a
    cache economist needs — no amount of retention would ever serve this — and recording it as a miss would
    teach a policy to cache its way out of a law."""
    from columna_platform.kernel.observation import RecordingObserver, UNSUPPORTED

    watcher = RecordingObserver()
    engine = MME(EX.COMMERCE, REGISTRY, IN_MEMORY, manifold=EX.MANIFOLD, observer=watcher)
    for family in EX._families():
        engine.register_family(family)
    engine.measure(fams["on_hand"], EX.TOTAL)

    assert len(watcher.records) == 1
    record = watcher.records[0]
    assert record.disposition == UNSUPPORTED
    assert record.refusal_code == "outside-continuation-region"
    assert record.fulfillment.considered == 0                   # no candidate was even looked at


# ══ E · CHANGING THE REGION CHANGES WHICH REQUESTS EXIST, NOT MME LOGIC (§J) ═══════════════════════
def _engine_source_digest() -> str:
    import hashlib

    both = inspect.getsource(kernel_mme_module) + inspect.getsource(columnar_mme_module)
    return hashlib.sha256(both.encode()).hexdigest()


@pytest.mark.parametrize("forgettable,expect_total,expect_by_day", [
    # `R_F` is {store, day, order}, so reaching {day} forgets {store, order} and reaching {} forgets all
    # three. The region is a set of FORGETTABLE constituents and admits a coarsening when it contains
    # everything that coarsening forgets.
    (None, True, True),                                  # everywhere(): both lawful
    (frozenset({"store", "order"}), False, True),        # {day} lawful; {} would also forget `day`
    (frozenset(), False, False),                         # forget nothing: only R_F itself
])
def test_changing_the_region_changes_which_requests_exist(forgettable, expect_total, expect_by_day):
    """**§J, EXECUTED.** One family, three continuation regions, and the only thing that moves is which
    authorizations are granted. The engines' source is byte-identical across all three, because nothing about
    a region reaches them."""
    before = _engine_source_digest()

    region = (ContinuationRegion.everywhere("test") if forgettable is None
              else ContinuationRegion.forgetting_only(forgettable, "a test region"))
    law = replace(REGISTRY.get("SUM"), name="TESTSUM", region=region)
    registry = LawRegistry((*REGISTRY, law), vocabulary="test", version="1")
    profile = replace(IN_MEMORY.of("SUM"), law="TESTSUM")
    from columna_platform.kernel import ProviderProfile

    engine = MME(EX.COMMERCE, registry,
                 ProviderProfile("test", (*(IN_MEMORY.of(n) for n in IN_MEMORY.laws), profile)),
                 manifold=EX.MANIFOLD)
    family = MeasureFamily(family_id="tested", manifold=EX.MANIFOLD, universe="commerce",
                           root=EX.SALE_AT, law="TESTSUM", value_domain="decimal",
                           participation=EX.PARTICIPATION, target="a test family")
    engine.register_family(family)

    assert bool(engine.authorizer.authorize(family, EX.TOTAL)) is expect_total
    assert bool(engine.authorizer.authorize(family, EX.BY_DAY)) is expect_by_day
    assert bool(engine.authorizer.authorize(family, EX.SALE_AT)) is True    # R_F always

    assert _engine_source_digest() == before, "no MME logic may depend on a region"


def test_the_converse_holds_cache_state_moves_fulfillment_and_not_authorization(mme, fams):
    """**§9's second direction.** Change cache population / residency and the fulfillment result may change
    while the authorization does not."""
    revenue = fams["revenue"]
    authorized_before = bool(mme.authorizer.authorize(revenue, EX.TOTAL))
    assert mme.measure(revenue, EX.TOTAL).served

    for m in list(mme.materializations.select("revenue", eligibility=None)):
        mme.materializations.drop(m.id)
    assert len(mme.materializations.select("revenue", eligibility=None)) == 0

    assert not mme.measure(revenue, EX.TOTAL).served            # fulfillment changed …
    assert bool(mme.authorizer.authorize(revenue, EX.TOTAL)) is authorized_before is True  # … authorization did not


# ══ F · PROVIDER CAPABILITY CANNOT CREATE ANALYTICAL PERMISSION (§K) ══════════════════════════════
def test_provider_capability_cannot_create_analytical_permission(mme, fams):
    """**§K.** The in-memory profile realizes `STOCK_LEVEL` perfectly well — it is literally the same
    `addition` as `SUM` — and that buys nothing: `on_hand@TOTAL` stays unauthorized. A backend that could
    compute the number would not thereby make it a lawful Columna materialization."""
    on_hand = fams["on_hand"]
    assert mme.provider.realizes("STOCK_LEVEL")
    assert mme.provider.capability("STOCK_LEVEL", "merge") is not None

    refused = mme.authorizer.authorize(on_hand, EX.TOTAL)
    assert not refused
    assert "what a provider could compute" in refused.refusal.detail

    # and the composition it would use is the SAME one SUM uses, which is authorized at that anchor
    assert REGISTRY.get("STOCK_LEVEL").continuation.token == REGISTRY.get("SUM").continuation.token
    assert mme.authorizer.authorize(fams["revenue"], EX.TOTAL)


def test_the_authority_reads_no_provider_when_deciding_permission(mme):
    """`authorize` consults the law and the geometry. It touches the provider only in `requirement_for`,
    which is a build-capability question about the estate, not a permission question."""
    authorize = _code_only_fn(ContinuationAuthority.authorize)
    assert "self.constitution.provider" not in authorize
    assert "realizes" not in authorize
    assert "self.constitution.provider" in _code_only_fn(ContinuationAuthority.requirement_for)


def test_the_two_capability_keys_are_not_collapsed_into_one(mme, fams):
    """**§4.** E-1 established that analytical law and physical execution capability are not keyed uniformly,
    and the fold requirement preserves that. `SUM`, `COUNT` and `STOCK_LEVEL` are three laws that all reduce
    by `addition`: keying the fold by law name in the GROUPED contract would have invented two capabilities
    the provider does not have."""
    folds = {}
    for family_id in ("revenue", "order_count"):
        request = mme.authorizer.authorize(mme.family(family_id), EX.BY_DAY).request
        folds[family_id] = request.fold

    assert folds["revenue"].composition == folds["order_count"].composition == "addition"
    assert folds["revenue"].merge_realization == "SUM"
    assert folds["order_count"].merge_realization == "COUNT"
    assert folds["revenue"].merge_realization != folds["order_count"].merge_realization

    sketch = mme.authorizer.authorize(mme.family("distinct_customers"), EX.TOTAL).request
    assert sketch.fold.composition == "sketch_union"
    assert sketch.fold.execution_mode == "grouped"


def test_the_execution_mode_vocabulary_agrees_with_E1s():
    """The kernel cannot import `columnar.capability` (the dependency runs the other way), so the two
    vocabularies are asserted to agree rather than shared — otherwise one word becomes two meanings."""
    from columna_platform.columnar.capability import GROUPED, SCAN
    from columna_platform.kernel.authorization import GROUPED_MODE, SCAN_MODE

    assert GROUPED_MODE == GROUPED
    assert SCAN_MODE == SCAN


# ══ G · `requirement_for` STAYED A SEPARATE QUESTION (§L) ══════════════════════════════════════════
def test_requirement_for_is_a_different_object_answering_a_different_question(mme, fams):
    """**§L.** An authorization says *"this is lawful, attempt it from held state"*; a requirement says
    *"held state was not enough, and here is what governed state would be"*. The second follows from
    attempting the first, and they are not one object."""
    revenue = fams["revenue"]
    authorized = mme.authorizer.authorize(revenue, EX.TOTAL)
    requirement = mme.requirement_for(revenue, EX.TOTAL)

    assert authorized and requirement
    assert type(authorized.request) is not type(requirement.requirement)
    assert not isinstance(requirement.requirement, AuthorizedFamilyContinuation)

    # the requirement names standing the authorization does not, and vice versa
    assert requirement.requirement.sufficient_state
    assert requirement.requirement.acceptable                  # which anchors could supply it
    assert not hasattr(authorized.request, "acceptable")
    assert not hasattr(requirement.requirement, "fold")


def test_an_unlawful_target_yields_neither_an_authorization_nor_a_requirement(mme, fams):
    """R-1 §6's load-bearing case, unchanged and now asked by the same component that refuses the
    authorization — which is why the two answers cannot disagree."""
    outcome = mme.requirement_for(fams["on_hand"], EX.BY_STORE)
    assert not outcome and outcome.requirement is None
    assert "NO REALIZATION REQUIREMENT IS EMITTED" in outcome.reason
    assert not mme.authorizer.authorize(fams["on_hand"], EX.BY_STORE)


# ══ H · THE THREE CONSTITUTIONAL LEAKS (§D, §F, §G) ════════════════════════════════════════════════
def test_the_fold_shape_is_declared_on_the_law_and_is_identity_bearing(mme):
    """**§F: the fate of `_POPULATION_LAWS`.** Gone, and not relocated. The fact it encoded is a property of
    the law — whether the reduction reads values or only membership — so the law declares it, and it enters
    every family's constitution witness by subtraction, with no edit to the witness module."""
    from columna_platform.kernel.witness import law_witness

    assert REGISTRY.get("COUNT").fold_shape == POPULATION
    assert REGISTRY.get("SUM").fold_shape == VALUE_BEARING

    moved = replace(REGISTRY.get("COUNT"), fold_shape=VALUE_BEARING)
    assert law_witness(moved).digest != law_witness(REGISTRY.get("COUNT")).digest

    with pytest.raises(KernelRefusal) as refused:
        replace(REGISTRY.get("SUM"), fold_shape="whatever")
    assert refused.value.code == "unknown-fold-shape"


def test_the_shape_reaches_the_provider_from_the_request_not_from_a_name(mme):
    """The columnar fold receives its shape and its composition from the authorized request. Neither is
    looked up in the engine, and `_shape_of` no longer exists."""
    code = _code_only(columnar_mme_module)
    assert "request.fold.fold_shape" in code
    assert "request.fold.composition" in code
    assert "_shape_of" not in code and "_POPULATION_LAWS" not in code

    engine, _block = CEX.build(settled=True, data_state=LOAD)
    counted = engine.measure("order_count", CEX.BY_DAY)
    assert counted.served                                      # a POPULATION fold, end to end


def test_the_approximation_disclosure_is_authored_above_and_only_propagated_below(mme, fams):
    """**§G.** Both engines read `law.approximation` and authored an `approximate` disclosure — a cache
    asserting an analytical fact about a law. The authority decides it now; the engines carry it."""
    sketch = mme.authorizer.authorize(fams["distinct"], EX.TOTAL).request
    assert [d.code for d in sketch.conditions] == ["approximate"]
    assert "HLL_SKETCH is approximate" in sketch.conditions[0].detail

    exact = mme.authorizer.authorize(fams["revenue"], EX.TOTAL).request
    assert exact.conditions == ()

    served = mme.measure(fams["distinct"], EX.TOTAL)
    assert served.served and "approximate" in {d.code for d in served.value.disclosures}

    for module in (kernel_mme_module, columnar_mme_module):
        assert "approximation" not in _code_only(module), module.__name__


def test_the_shape_vocabulary_has_one_definition(mme):
    """`VALUE_BEARING`/`POPULATION` were defined in `columnar/standing.py` AND needed by the law. One
    definition now, in `kernel/law.py`, re-exported where callers already read them."""
    import importlib

    # `columna_platform.columnar` re-exports a FUNCTION named `standing`, which shadows the submodule as an
    # attribute — so the module is reached through importlib rather than attribute access.
    standing_module = importlib.import_module("columna_platform.columnar.standing")
    law_module = importlib.import_module("columna_platform.kernel.law")

    assert standing_module.VALUE_BEARING is law_module.VALUE_BEARING
    assert standing_module.POPULATION is law_module.POPULATION
    code = _code_only(standing_module)
    assert "VALUE_BEARING = " not in code, "a second definition of the vocabulary"
    assert "POPULATION = " not in code, "a second definition of the vocabulary"


# ══ I · NOTHING OUT OF SCOPE ARRIVED ══════════════════════════════════════════════════════════════
def test_none_of_the_excluded_work_arrived():
    """Ruled out by name in §10."""
    code = "".join(_code_only(m) for m in (kernel_mme_module, columnar_mme_module,
                                           authorization_module))
    for banned in ("iceberg", "psycopg", "sqlalchemy", "postgres", "duckdb", "adbc", "sqlite3",
                   "pickle", "json.dump", "open(", "APScheduler", "lru_cache", "cost_of", "score",
                   "optimize", "evict_candidates"):
        assert banned not in code.lower(), banned


def test_the_three_exhibits_still_run_green(capsys):
    from columna_platform.columnar import exhibit as columnar_exhibit
    from columna_platform.frameql import exhibit as frameql_exhibit
    from columna_platform.kernel import exhibit as kernel_exhibit

    for module in (kernel_exhibit, columnar_exhibit, frameql_exhibit):
        module.main() if hasattr(module, "main") else module.run()
    out = capsys.readouterr().out
    assert "ALL CHECKS PASSED" in out
