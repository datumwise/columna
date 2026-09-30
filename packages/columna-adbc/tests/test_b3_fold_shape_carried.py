"""
B-3, the provider half — **it carries the fold shape and cannot derive one.**

    **The provider does not state or infer fold shape.**  — Huayin, 2026-09-30

The authority half is proved in `columna-platform`. What is proved here is the other end of the arrow: this
provider reads `requirement.fold_shape`, hands it to the state it offers, and contains no route by which a
law NAME could become a shape.

**NO SECOND FAMILY IS REALIZED HERE, DELIBERATELY.** Ruled: *"no second family/backend/expression is added
yet… report back before adding `order_count`."* So the COUNT case is proved as far as it can be without
realizing a second family — a COUNT requirement produces a proposal whose handle carries `population` — and
combined with the structural proof that `realize` reads the shape from nowhere but that handle, and the
Revenue path proving a handle's shape reaches the offered state, the chain is complete without extending
the vertical slice.
"""
from __future__ import annotations

import ast
import inspect
import textwrap

import b2_exhibit as EX
import b2_revenue_warehouse as W
import pytest

from columna_adbc import DuckDbFamilyProvider, duckdb_realization
from columna_platform.columnar import exhibit as CEX
from columna_platform.kernel.geometry import KernelRefusal
from columna_platform.kernel.law import POPULATION, VALUE_BEARING


def _strip_docstrings(tree: ast.AST) -> ast.AST:
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            body = getattr(node, "body", [])
            if (body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant)
                    and isinstance(body[0].value.value, str)):
                node.body = body[1:] or [ast.Pass()]
    return tree


def _code_only(obj) -> str:
    """Source with docstrings removed — a structural test must read CODE, not prose."""
    return ast.unparse(_strip_docstrings(ast.parse(textwrap.dedent(inspect.getsource(obj)))))


class _DropRefusalText(ast.NodeTransformer):
    """Replace every `KernelRefusal(...)` argument list with a placeholder.

    **A LITERAL IN A MESSAGE IS NOT A LITERAL IN A DECISION**, and the first draft of the test below could
    not tell them apart: it failed on the refusal that explains itself by naming *"a value-bearing or a
    population domain"* — which is the refusal doing its job, not the provider inferring anything. Blunting
    the message to satisfy the guard would have been the wrong repair, so the guard learned to read code.

    What survives this transform is every comparison, dict, branch and assignment — so a mapping such as
    `{"COUNT": POPULATION}` or an `if law == "COUNT"` is still caught, which is the property under test."""

    def visit_Call(self, node: ast.Call) -> ast.Call:                     # noqa: N802 - ast API
        self.generic_visit(node)
        name = getattr(node.func, "id", getattr(node.func, "attr", ""))
        if name == "KernelRefusal":
            node.args = [ast.Constant(value="<refusal text>")]
            node.keywords = []
        return node


def _decisions_only(module) -> str:
    """Code with docstrings AND refusal message text removed. What is left is what the module DECIDES."""
    tree = _strip_docstrings(ast.parse(textwrap.dedent(inspect.getsource(module))))
    return ast.unparse(ast.fix_missing_locations(_DropRefusalText().visit(tree)))


@pytest.fixture
def world(tmp_path):
    return EX.cold_world(W.build(tmp_path))


# ══ A · THE PROVIDER CONTAINS NO LAW-NAME → FOLD-SHAPE INFERENCE ═══════════════════════════════════

def test_the_provider_module_names_no_law_and_no_fold_shape_at_all():
    """**The structural heart of the unit.** Not one law name and not one shape literal appears in this
    module's code — it could not build the mapping if it wanted to, because it holds neither vocabulary."""
    code = _decisions_only(duckdb_realization)
    for law_name in ("SUM", "COUNT", "HLL_SKETCH", "STOCK_LEVEL", "LAST"):
        assert law_name not in code, law_name
    for shape in ("population", "value-bearing", "VALUE_BEARING", "POPULATION", "FOLD_SHAPES"):
        assert shape not in code, shape
    assert "_POPULATION_LAWS" not in code
    # And the transform is not doing the work by deleting everything: the method under test is still here.
    assert "fold_shape=handle.fold_shape" in code
    assert "self.source.fetch" in code


def test_the_provider_imports_neither_the_law_registry_nor_the_shape_constants():
    code = _code_only(duckdb_realization)
    assert "law import" not in code
    assert "LawRegistry" not in code
    assert "REGISTRY" not in code


def test_the_offered_shape_comes_from_the_handle_and_from_nowhere_else():
    code = _code_only(DuckDbFamilyProvider.realize)
    assert "fold_shape=handle.fold_shape" in code
    # There is exactly ONE `fold_shape` source in the whole method.
    assert code.count("fold_shape") == code.count("handle.fold_shape") + 1  # +1 for the refusal guard


# ══ B · THE CARRY, END TO END, FOR THE ONE FAMILY B-2 ESTABLISHED ══════════════════════════════════

def test_the_requirements_shape_reaches_the_state_the_provider_offers(world):
    mme, _, _, provider, _ = world
    requirement = mme.requirement_for("revenue", mme.family("revenue").root).requirement
    assert requirement.fold_shape == VALUE_BEARING

    proposal = next(iter(provider.propose(requirement)))
    assert proposal.handle.fold_shape == requirement.fold_shape

    offer = provider.realize(proposal)
    assert offer.value.fold_shape == requirement.fold_shape
    assert offer.value.shape == requirement.fold_shape


def test_a_COUNT_requirement_puts_POPULATION_on_the_handle(world):
    """**As far as this unit goes without realizing a second family.** The provider is handed a COUNT
    requirement and the shape it will supply is `population` — and it learned that from the requirement,
    having no idea that COUNT is a population law."""
    mme, _, source, provider, _ = world
    count_family = {f.family_id: f for f in CEX._families("andfam.commerce")}["order_count"]
    mme.authority.register_family(count_family)
    requirement = mme.requirement_for(count_family, count_family.root).requirement
    assert requirement.law == "COUNT"
    assert requirement.fold_shape == POPULATION

    # Bound to the same physical object, because what is under test is the SHAPE CARRY and not a second
    # family's realization — nothing is fetched, and no COUNT state is established.
    from columna_adbc import PhysicalFamilyBinding

    bound = DuckDbFamilyProvider(source, PhysicalFamilyBinding(
        family_id="order_count", schema=W.SCHEMA, table=W.TABLE,
        coordinates={"store": W.STORE_COLUMN, "day": W.DAY_COLUMN, "order": W.ORDER_COLUMN},
        value_column=W.VALUE_COLUMN))
    proposal = next(iter(bound.propose(requirement)))
    assert proposal.handle.fold_shape == POPULATION
    assert source.fetches == [], "capability discovery fetched nothing; no second family was realized"


def test_one_provider_carries_two_different_shapes_without_a_branch(world):
    """Same code, two shapes, decided elsewhere. If the provider held the mapping, this test would pass
    for the wrong reason — which is why the structural test above is the one that matters."""
    mme, _, source, provider, _ = world
    count_family = {f.family_id: f for f in CEX._families("andfam.commerce")}["order_count"]
    mme.authority.register_family(count_family)
    from columna_adbc import PhysicalFamilyBinding

    both = DuckDbFamilyProvider(source, W.binding(), PhysicalFamilyBinding(
        family_id="order_count", schema=W.SCHEMA, table=W.TABLE,
        coordinates={"store": W.STORE_COLUMN, "day": W.DAY_COLUMN, "order": W.ORDER_COLUMN},
        value_column=W.VALUE_COLUMN))
    shapes = {}
    for family_id in ("revenue", "order_count"):
        family = mme.family(family_id)
        requirement = mme.requirement_for(family, family.root).requirement
        shapes[family_id] = next(iter(both.propose(requirement))).handle.fold_shape
    assert shapes == {"revenue": VALUE_BEARING, "order_count": POPULATION}
    assert source.fetches == []


# ══ C · A REQUIREMENT THAT WILL NOT STATE IT IS REFUSED, NEVER GUESSED ═════════════════════════════

def test_a_requirement_stating_no_fold_shape_is_refused_loudly(world):
    """The same shape of refusal `RealizationAuthority` makes for an offer that will not state its build.
    The alternative is the one thing ruled out: to guess from the law name."""
    from dataclasses import replace

    mme, _, source, provider, _ = world
    requirement = mme.requirement_for("revenue", mme.family("revenue").root).requirement
    silent = replace(requirement, fold_shape="")
    proposal = next(iter(provider.propose(silent)))
    with pytest.raises(KernelRefusal) as raised:
        provider.realize(proposal)
    assert raised.value.code == "requirement-states-no-fold-shape"
    assert "will not infer it from the law's name" in raised.value.detail
    assert source.fetches == [], "it refused before opening anything"


# ══ D · B-2 IS UNCHANGED ══════════════════════════════════════════════════════════════════════════

def test_the_b2_cold_to_warm_behaviour_is_unchanged(world):
    mme, service, source, _, _ = world
    cold = service.serve(EX.ASK)
    assert cold.classification == "serve", cold.render()
    assert len(source.fetches) == 1
    assert len(cold.frame.rows) == len(W.ORDERS)

    warm = service.serve(EX.ASK)
    assert warm.classification == "serve"
    assert len(source.fetches) == 1
    assert warm.frame.rows == cold.frame.rows


def test_the_b2_exhibit_still_runs_green(capsys):
    assert EX.main() == 0
    assert "ALL CHECKS PASSED" in capsys.readouterr().out


def test_no_second_family_backend_or_expression_entered_the_vertical_slice():
    """Ruled: the slice stays one family, one backend, no expressions. Asserted of the exhibit itself."""
    code = _code_only(EX)
    assert "order_count" not in code
    assert code.count("PhysicalFamilyBinding") == 0     # the exhibit uses W.binding() and no other
    for banned in ("average_order_value", "distinct_customers", "postgres", "iceberg", "sqlite"):
        assert banned not in code, banned
