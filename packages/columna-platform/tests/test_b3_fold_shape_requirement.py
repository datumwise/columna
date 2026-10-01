"""
B-3 · **the governed fold shape reaches the estate, and nobody below the law decides it.**

    **The provider does not state or infer fold shape. Analytical authority determines fold shape;
    `FamilyRequirement` carries that governed requirement to the provider.**  — Huayin, 2026-09-30

        governed law / authority  →  determines fold shape
                ↓
        FamilyRequirement.fold_shape
                ↓
        RealizationProvider  →  decides only whether/how it can supply state satisfying that requirement

B-2 exposed the gap: `FamilyRequirement` carried `law`, `value_form`, `sufficient_state`, `approximation`,
`instance`, `build` and `witness` — everything a provider is told about what to supply — and not the shape
its reduction contributes over. The provider therefore took `ColumnarFamilyState`'s dataclass default,
`VALUE_BEARING`, which is right for SUM and silently wrong for COUNT.

**THE FORBIDDEN FIX IS THE INTERESTING ONE.** A provider could have written `COUNT → POPULATION`. That is
verbatim the enumeration B-0b deleted from the columnar cache engine — `_POPULATION_LAWS = frozenset({
"COUNT"})` — and putting it in a provider moves constitutional knowledge one layer FARTHER from the
constitution rather than closer. The fact is a property of the law; the law declares it; everyone else
carries it.
"""
from __future__ import annotations

import ast
import inspect
import textwrap

from columna_platform.columnar import exhibit as CEX
from columna_platform.kernel import IN_MEMORY, MME, REGISTRY
from columna_platform.kernel.authorization import ContinuationAuthority, FoldRequirement
from columna_platform.kernel.law import FOLD_SHAPES, POPULATION, VALUE_BEARING
from columna_platform.kernel.requirement import FamilyRequirement

MANIFOLD = "andfam.commerce"


def _code_only(obj) -> str:
    """Source with docstrings removed — a structural test must read CODE, not prose."""
    tree = ast.parse(textwrap.dedent(inspect.getsource(obj)))
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            body = getattr(node, "body", [])
            if (body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant)
                    and isinstance(body[0].value.value, str)):
                node.body = body[1:] or [ast.Pass()]
    return ast.unparse(tree)


def _world():
    """The commerce world, constituted. `revenue` is SUM; `order_count` is COUNT."""
    mme = MME(CEX.COMMERCE, REGISTRY, IN_MEMORY, manifold=MANIFOLD, build=CEX.BUILD)
    families = CEX._families(MANIFOLD)
    for family in families:
        mme.register_family(family)
    return mme, {f.family_id: f for f in families}


# ══ A · THE LAW DECLARES IT, AND IT IS THE ONLY DECLARATION ════════════════════════════════════════

def test_the_law_is_where_the_fold_shape_is_declared():
    shapes = {law.name: law.fold_shape for law in REGISTRY.family_laws()}
    assert shapes["SUM"] == VALUE_BEARING
    assert shapes["COUNT"] == POPULATION
    assert set(shapes.values()) <= FOLD_SHAPES


# ══ B · THE REQUIREMENT CARRIES IT, FROM THE AUTHORITY ════════════════════════════════════════════

def test_the_requirement_receives_the_fold_shape_from_the_governing_authority():
    mme, families = _world()
    requirement = mme.requirement_for(families["revenue"], families["revenue"].root).requirement
    assert requirement.fold_shape == VALUE_BEARING
    # And it came from the LAW, not from anything the caller said.
    assert requirement.fold_shape == REGISTRY.get(requirement.law).fold_shape


def test_COUNT_produces_POPULATION_and_the_requirement_says_so():
    """**The headline of this unit.** Nothing outside `law.py` knows that COUNT is a population law."""
    mme, families = _world()
    requirement = mme.requirement_for(families["order_count"], families["order_count"].root).requirement
    assert requirement.law == "COUNT"
    assert requirement.fold_shape == POPULATION


def test_ordinary_value_bearing_families_carry_value_bearing():
    mme, families = _world()
    for family_id in ("revenue", "distinct_customers", "on_hand"):
        family = families[family_id]
        requirement = mme.requirement_for(family, family.root).requirement
        assert requirement.fold_shape == VALUE_BEARING, family_id


def test_the_requirement_renders_the_shape_a_provider_must_satisfy():
    """A requirement whose author has to look up the law to read it is one that will be guessed."""
    mme, families = _world()
    assert "population domain" in mme.requirement_for(
        families["order_count"], families["order_count"].root).requirement.render()
    assert "value-bearing domain" in mme.requirement_for(
        families["revenue"], families["revenue"].root).requirement.render()


# ══ C · TWO MESSAGES, ONE FACT — DUPLICATION IN MESSAGES, NOT IN AUTHORITY ═════════════════════════

def test_the_authorized_continuation_and_the_requirement_carry_the_SAME_fact():
    """Ruled: *"It is legitimate for both `AuthorizedFamilyContinuation` and `FamilyRequirement` to carry
    fold shape… That is duplication in messages, not duplication of authority."*

    Two consumers, two messages, one law — so the test that matters is that they AGREE, and that neither
    computed it."""
    mme, families = _world()
    for family_id in ("revenue", "order_count"):
        family = families[family_id]
        authorized = mme.authorizer.authorize(family, family.root)
        assert authorized, authorized.refusal
        required = mme.requirement_for(family, family.root).requirement
        assert authorized.request.fold.fold_shape == required.fold_shape
        assert required.fold_shape == REGISTRY.get(required.law).fold_shape


def test_neither_message_type_computes_the_shape_it_carries():
    """Both are dataclasses that RESTATE. Neither has a law-name enumeration, and neither validates a
    second time — `AnalyticalLaw.__post_init__` already did, and a second asker is the defect B-0a removed."""
    for record in (FamilyRequirement, FoldRequirement):
        code = _code_only(record)
        assert "COUNT" not in code, record
        assert "_POPULATION_LAWS" not in code, record


def test_the_authority_reads_the_shape_off_the_law_and_enumerates_nothing():
    code = _code_only(ContinuationAuthority.requirement_for)
    assert "law.fold_shape" in code
    assert "COUNT" not in code
    assert "POPULATION" not in code


def test_no_engine_reacquired_a_law_name_enumeration():
    """The B-0b repair, still in force in both engines and now in the layer below them too."""
    from columna_platform.columnar import mme as columnar_mme
    from columna_platform.columnar import standing as columnar_standing
    from columna_platform.kernel import mme as kernel_mme

    for module in (kernel_mme, columnar_mme, columnar_standing):
        code = _code_only(module)
        assert "_POPULATION_LAWS" not in code, module.__name__
        assert '"COUNT"' not in code and "'COUNT'" not in code, module.__name__
