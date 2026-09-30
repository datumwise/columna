"""
B-4a · **root formation becomes first-class governed family constitution.**

    **Root formation says what the root family value is constituted from. Evidence provenance says how
    that root establishment is supported. Physical realization says how the governed formation is
    executed. Continuation says how an already-established family value moves. Keep all four
    separate.**  — Huayin, 2026-09-30 (B-4a, the governing distinction)

B-3 carried the fold shape to the estate and B-4 then could not proceed: a `COUNT` family's root payload
is load-bearing (`continue_grouped` SUMS it), and nothing said what that payload IS. The warehouse cannot
honestly supply it at an individuating root, the provider must not infer it, and no governed object stated
it — while `MeasureFamily.law`'s own docstring had reserved a slot beside itself for exactly this fact.

**THE MEASURED DEFECT THIS CLOSES.** Before this unit, a cold world admitted and served a population
family whose payload disagreed with its own membership: 7 participating points, 11 orders reported, nothing
objecting. §H below is that case, refused at fidelity, with nothing retained.
"""
from __future__ import annotations

import ast
import inspect
import textwrap
from dataclasses import replace

import pyarrow as pa
import pytest

from columna_platform.columnar import exhibit as CEX
from columna_platform.columnar.index import AnchorInstance
from columna_platform.columnar.mme import ColumnarFamilyState, ColumnarMME
from columna_platform.columnar.standing import standing as column_standing
from columna_platform.frameql import FrameQLService
from columna_platform.kernel import IN_MEMORY, MME, REGISTRY
from columna_platform.kernel import exhibit as KEX
from columna_platform.kernel.authorization import ContinuationAuthority
from columna_platform.kernel.geometry import KernelRefusal
from columna_platform.kernel.law import POPULATION, VALUE_BEARING
from columna_platform.kernel.realization import RealizationStanding
from columna_platform.kernel.realization_manager import RealizationOffer
from columna_platform.kernel.sorts import (
    DIRECT,
    FORMATION_LAWS,
    PARTICIPATION_CARDINALITY,
    MeasureFamily,
)
from columna_platform.kernel.witness import FAMILY_SORT, determinant_names

MANIFOLD = "andfam.commerce"


def _code_only(obj) -> str:
    tree = ast.parse(textwrap.dedent(inspect.getsource(obj)))
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            body = getattr(node, "body", [])
            if (body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant)
                    and isinstance(body[0].value.value, str)):
                node.body = body[1:] or [ast.Pass()]
    return ast.unparse(tree)


def _cold(*family_ids: str):
    """A constituted, EMPTY columnar engine over the named families."""
    authority = MME(CEX.COMMERCE, REGISTRY, IN_MEMORY, manifold=MANIFOLD)
    families = {f.family_id: f for f in CEX._families(MANIFOLD)}
    for family_id in family_ids:
        authority.register_family(families[family_id])
    return ColumnarMME(authority), families


# ══ A · THE DECLARATION ════════════════════════════════════════════════════════════════════════════

def test_formation_is_a_family_declaration_field():
    assert "formation" in MeasureFamily.__dataclass_fields__
    assert FORMATION_LAWS == frozenset({DIRECT, PARTICIPATION_CARDINALITY})


def test_the_vocabulary_lives_with_the_family_and_not_with_the_law():
    """**Placement is an argument, not a filing decision.** `VALUE_FORMS`, `DOMAINS` and `FOLD_SHAPES`
    live beside `AnalyticalLaw` because the law asserts them. Formation is asserted by the FAMILY, and
    shelving it beside `FOLD_SHAPES` would have quietly suggested that a law implies a formation."""
    from columna_platform.kernel import law as law_module
    from columna_platform.kernel import sorts as sorts_module

    assert hasattr(sorts_module, "FORMATION_LAWS")
    assert not hasattr(law_module, "FORMATION_LAWS")
    assert not hasattr(law_module, "PARTICIPATION_CARDINALITY")


def test_the_vocabulary_is_open_rather_than_a_closed_ontology():
    """Ruled §8: structured sufficient-state roots will need their own formation laws, and adding one
    must not change what the field MEANS. So the field carries a token from an extensible set — not a
    boolean, and not an enum of 'value vs count'."""
    assert MeasureFamily.__dataclass_fields__["formation"].type in ("str", str)
    assert isinstance(FORMATION_LAWS, frozenset)


# ══ NO SILENT DEFAULT (§9) ════════════════════════════════════════════════════════════════════════

def test_a_family_that_does_not_state_its_formation_is_REFUSED():
    with pytest.raises(KernelRefusal) as raised:
        MeasureFamily(family_id="unstated", manifold=MANIFOLD, universe="commerce", root=KEX.SALE_AT,
                      law="SUM", value_domain="decimal", participation="p", target="t")
    assert raised.value.code == "no-root-formation-declared"
    assert "THERE IS NO DEFAULT" in raised.value.detail


def test_an_undeclared_formation_law_is_refused_too():
    with pytest.raises(KernelRefusal) as raised:
        MeasureFamily(family_id="odd", manifold=MANIFOLD, universe="commerce", root=KEX.SALE_AT,
                      law="SUM", formation="whatever-i-like", value_domain="decimal",
                      participation="p", target="t")
    assert raised.value.code == "unknown-root-formation"


def test_the_refusal_does_not_suggest_DIRECT_as_a_fallback():
    """The pressure is the point: a family nobody can classify is a gap in the constitution."""
    with pytest.raises(KernelRefusal) as raised:
        MeasureFamily(family_id="unstated", manifold=MANIFOLD, universe="commerce", root=KEX.SALE_AT,
                      law="COUNT", value_domain="integer", participation="p", target="t")
    assert "not a gap here" in raised.value.detail


# ══ B · WHICH FAMILY RECEIVES WHICH FORMATION ═════════════════════════════════════════════════════

def test_every_platform_family_states_its_formation_explicitly():
    for families in (KEX._families(), CEX._families(MANIFOLD)):
        for family in families:
            assert family.formation in FORMATION_LAWS, family.family_id


def test_the_classification_is_the_reported_one():
    declared = {f.family_id: f.formation for f in KEX._families()}
    assert declared == {
        "revenue": DIRECT,
        "order_count": PARTICIPATION_CARDINALITY,
        "audited_order_count": PARTICIPATION_CARDINALITY,
        "distinct_customers": DIRECT,
        "on_hand": DIRECT,
        "gauge": DIRECT,
    }


def test_two_count_families_share_a_formation_over_DIFFERENT_domains():
    """Cardinality is `|D(r)|` and `D` is each family's OWN participating domain — which is why one
    formation law serves both `order_count` and the auditor's narrower count."""
    families = {f.family_id: f for f in KEX._families()}
    a, b = families["order_count"], families["audited_order_count"]
    assert a.formation == b.formation == PARTICIPATION_CARDINALITY
    assert a.participation != b.participation


# ══ C · FORMATION ENTERS IDENTITY AUTOMATICALLY ═══════════════════════════════════════════════════

def test_formation_is_a_witness_determinant_by_derivation():
    assert "formation" in determinant_names(FAMILY_SORT, MeasureFamily)


def test_changing_the_formation_changes_the_family_witness():
    """A count formed from cardinality and a count supplied directly are not the same constitution, even
    at the same root under the same law."""
    order_count = {f.family_id: f for f in KEX._families()}["order_count"]
    law = REGISTRY.get("COUNT")
    assert order_count.witness(law).digest != replace(order_count, formation=DIRECT).witness(law).digest


def test_witness_py_needed_no_edit_for_this_to_be_true():
    """`FAMILY_NON_DETERMINANTS` is an EXCLUSION list — *"everything not listed here is a determinant BY
    DERIVATION"* — so the ruling's *"should follow the existing subtraction rule automatically"* is a
    property of that design rather than a change to it."""
    from columna_platform.kernel.witness import FAMILY_NON_DETERMINANTS

    assert "formation" not in FAMILY_NON_DETERMINANTS
    assert FAMILY_NON_DETERMINANTS == frozenset({"family_id", "target", "constitution"})


# ══ D · THE REQUIREMENT CARRIES IT, FROM THE FAMILY ═══════════════════════════════════════════════

def test_the_requirement_carries_the_formation_off_the_family():
    mme, families = _cold("revenue", "order_count")
    for family_id, expected in (("revenue", DIRECT), ("order_count", PARTICIPATION_CARDINALITY)):
        family = families[family_id]
        requirement = mme.requirement_for(family, family.root).requirement
        assert requirement.formation == expected == family.formation


def test_the_authority_reads_formation_off_the_family_and_never_off_the_law():
    code = _code_only(ContinuationAuthority.requirement_for)
    assert "formation=family.formation" in code
    assert "law.formation" not in code
    for banned in ('"COUNT"', "'COUNT'", "PARTICIPATION_CARDINALITY"):
        assert banned not in code, banned


# ══ G/H · THE FIDELITY RULE, AND THE MEASURED DEFECT ══════════════════════════════════════════════

def _cardinality_offer(mme, values):
    """An offer of `order_count@R_F` carrying `values`. Everything else is faithful."""
    authority = mme.authority
    index = CEX._root_index(MANIFOLD)
    instance = authority.instance_of("order_count")
    law = REGISTRY.get("COUNT")
    state = ColumnarFamilyState(
        family_id="order_count", anchor_instance=AnchorInstance(index=index, instance=instance),
        values=pa.array(values, type=pa.int64()),
        standing=column_standing("order_count", instance, n=len(index.coordinates)),
        law="COUNT", value_form=law.value_form, fold_shape=law.fold_shape)
    return RealizationOffer(
        provider="duckdb-warehouse", family_id="order_count", anchor=authority.family("order_count").root,
        value=state, instance=instance,
        realization=RealizationStanding(provider="duckdb-warehouse", carrier="duckdb/adbc→arrow"),
        build=authority.build.reference, witness=authority.witness_of("order_count").digest)


def test_a_faithful_cardinality_root_is_adjudicated():
    mme, _ = _cold("order_count")
    points = len(CEX._root_index(MANIFOLD).coordinates)
    adjudication = mme.realizations.adjudicate(_cardinality_offer(mme, [1] * points))
    assert adjudication, adjudication.refusal
    assert any("formation" in e for e in adjudication.credential.evidence)


def test_a_count_that_disagrees_with_its_domain_FAILS_FIDELITY_IN_A_COLD_WORLD():
    """**THE MEASURED DEFECT (§H).** 7 participating points, a payload summing to 11.

    Before B-4a this was ADMITTED and SERVED. The only thing that would have caught it is
    `duplicate-current-disagreement`, which requires an honest materialization to already be retained —
    *"too late and only works in a warm world."*"""
    mme, _ = _cold("order_count")
    assert mme.holdings() == (), "the world must be cold for this proof to mean anything"
    points = len(CEX._root_index(MANIFOLD).coordinates)
    laundered = [1] * points
    laundered[-1] = 5                                        # 7 members, 11 orders claimed

    adjudication = mme.realizations.adjudicate(_cardinality_offer(mme, laundered))
    assert not adjudication
    assert adjudication.refusal.code == "realization-contradicts-its-formation"
    assert "DISAGREES WITH THE DOMAIN IT IS A COUNT OF" in adjudication.refusal.detail
    assert mme.holdings() == (), "nothing was admitted"


def test_the_refusal_is_fidelity_and_not_the_cache_consistency_guard():
    mme, _ = _cold("order_count")
    points = len(CEX._root_index(MANIFOLD).coordinates)
    bad = [1] * points
    bad[0] = 3
    adjudication = mme.realizations.adjudicate(_cardinality_offer(mme, bad))
    assert adjudication.refusal.code != "duplicate-current-disagreement"


def test_a_DIRECT_root_is_NOT_recomputed_and_that_is_deliberate():
    """`DIRECT` says the value is established rather than derived, so there is no expectation to compare
    against. Silence is the correct answer here, not a gap — and a test says so, so that a future edit
    cannot "fix" it by inventing one."""
    mme, families = _cold("revenue")
    authority = mme.authority
    index = CEX._root_index(MANIFOLD)
    instance = authority.instance_of("revenue")
    law = REGISTRY.get("SUM")
    state = ColumnarFamilyState(
        family_id="revenue", anchor_instance=AnchorInstance(index=index, instance=instance),
        values=pa.array([999.0] * len(index.coordinates), type=pa.float64()),
        standing=column_standing("revenue", instance, n=len(index.coordinates)),
        law="SUM", value_form=law.value_form, fold_shape=law.fold_shape)
    offer = RealizationOffer(
        provider="p", family_id="revenue", anchor=families["revenue"].root, value=state,
        instance=instance, realization=RealizationStanding(provider="p"),
        build=authority.build.reference, witness=authority.witness_of("revenue").digest)
    assert mme.realizations.adjudicate(offer), "a DIRECT root's magnitude is not a fidelity question"


def test_the_fidelity_check_is_substrate_neutral():
    """It is in the KERNEL. A check that reached for `standing.participation` would have made the
    fidelity boundary columnar-only — so it reads B-2's `coordinates` + `cell()` surface instead."""
    from columna_platform.kernel.realization_fidelity import RealizationAuthority

    code = _code_only(RealizationAuthority._formation_holds)
    assert ".coordinates" in code and ".cell(" in code
    for columnar in ("participation", "pyarrow", "pa.", "pc.", "ColumnStanding", "standing."):
        assert columnar not in code, columnar


def test_the_expected_cardinality_is_derived_and_is_not_a_literal_one():
    """Ruled: do not encode `1` as the formation law. The expectation is the number of index positions
    carrying the coordinate — which is 1 because `CoordinateIndex` refuses duplicates, and which would be
    7 unchanged the day a geometry represents multiplicity."""
    from columna_platform.kernel.realization_fidelity import RealizationAuthority

    code = _code_only(RealizationAuthority._formation_holds)
    assert "counts[coordinate] = counts.get(coordinate, 0) + 1" in code
    assert "== 1" not in code and "expected = 1" not in code


# ══ I · FORMATION AND CONTINUATION REMAIN INDEPENDENT ═════════════════════════════════════════════

def test_formation_fold_shape_and_continuation_are_three_facts():
    families = {f.family_id: f for f in KEX._families()}
    order_count, law = families["order_count"], REGISTRY.get("COUNT")
    assert order_count.formation == PARTICIPATION_CARDINALITY     # what Count@R_F IS
    assert law.fold_shape == POPULATION                           # what domain contributes
    assert law.continuation.token == "addition"                   # how an established value moves
    revenue = families["revenue"]
    assert revenue.formation == DIRECT and REGISTRY.get("SUM").fold_shape == VALUE_BEARING


def test_population_continuation_was_NOT_changed_to_counting_rows():
    """Ruled §4: *"Current continuation remains addition over the Count family values."* The tempting
    shortcut — population fold = count contributing rows — is rejected, because a Count family may have a
    coarser root whose established value is genuinely greater than 1."""
    from columna_platform.columnar import provider as columnar_provider

    code = _code_only(columnar_provider.ColumnarProvider.continue_grouped)
    assert "self.capability(GROUPED, composition).execute" in code
    assert "formation" not in code, "formation reached the continuation path"
    # And it still adds: 7 root points, 3 on D1 and 4 on D2.
    mme, _ = CEX.build(MANIFOLD, settled=True)
    rows = dict(FrameQLService(mme).serve("SELECT order_count AT {day}").frame.rows)
    assert rows == {"D1": 3, "D2": 4}


def test_no_component_derives_formation_from_a_law_or_from_a_fold_shape():
    """The three forbidden inference rules, asserted against every component that could hold one."""
    from columna_platform.columnar import mme as columnar_mme
    from columna_platform.columnar import standing as columnar_standing
    from columna_platform.kernel import authorization, mme as kernel_mme, realization_manager

    for module in (kernel_mme, columnar_mme, columnar_standing, authorization, realization_manager):
        code = _code_only(module)
        assert "_POPULATION_LAWS" not in code, module.__name__
        for banned in ('"COUNT"', "'COUNT'"):
            assert banned not in code, (module.__name__, banned)
        # A fold shape may not be turned into a formation anywhere.
        assert "POPULATION" not in code or "PARTICIPATION_CARDINALITY" not in code, module.__name__


# ══ J · EVIDENCE PROVENANCE REMAINS INDEPENDENT OF FORMATION ══════════════════════════════════════

def test_how_a_DIRECT_root_is_evidenced_does_not_change_its_formation_or_its_identity():
    """*"A DIRECT root may be observed, reported, assigned, supplied by an authoritative source, or
    physically computed under a realization contract"* — none of which is the formation law.

    Two worlds establish `revenue@R_F` by different means: one folds occurrences in-process through
    `establish_root`, the other would receive it from a provider. Same declaration, same formation, same
    witness — because provenance is not constitution."""
    in_process = KEX.build()                                  # roots sealed by establish_root
    cold, families = _cold("revenue")
    assert in_process.family("revenue").formation == families["revenue"].formation == DIRECT
    assert (in_process.witness_of("revenue").digest
            == cold.authority.witness_of("revenue").digest)


def test_the_data_state_axis_is_untouched_by_formation():
    """Which established material a value carries is `data_state`, one of P-1's three separate facts.
    Formation added a fourth question and collapsed none of them."""
    from columna_platform.kernel.witness import FAMILY_NON_DETERMINANTS

    mme, families = _cold("order_count")
    requirement = mme.requirement_for(families["order_count"], families["order_count"].root).requirement
    assert requirement.formation == PARTICIPATION_CARDINALITY
    assert requirement.instance.data_state is not None
    assert "formation" not in FAMILY_NON_DETERMINANTS
