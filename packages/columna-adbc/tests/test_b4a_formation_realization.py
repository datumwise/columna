"""
B-4a, the provider half — **it executes the declared formation and decides nothing about what it means.**

    **The provider may physically construct the root payload from coordinates/participation because the
    governed formation requirement told it to do so. That is not provider inference… The provider performs
    physical computation. It does not decide what the computation means.**  — Huayin, 2026-09-30 (§7)

        BAD   provider knows COUNT        → decides Count means one per row
        GOOD  requirement says formation  → provider realizes that declared formation law

The distance between those two is measurable, and §F below measures it: nothing in the provider module's
code names a law, a fold shape or a value domain. The single governed token it holds is the formation
vocabulary's own constant, imported rather than spelled.

**THE `order_count` COLD→WARM VERTICAL SLICE IS NOT HERE.** Ruled: B-4a establishes the constitutional fact
and closes the measured laundering defect; B-4b is the real vertical proof.
"""
from __future__ import annotations

import ast
import inspect
import textwrap

import b2_exhibit as EX
import b2_revenue_warehouse as W
import pyarrow as pa
import pytest

from columna_adbc import DuckDbFamilyProvider, PhysicalFamilyBinding, duckdb_realization
from columna_platform.columnar import exhibit as CEX
from columna_platform.kernel.geometry import KernelRefusal
from columna_platform.kernel.sorts import DIRECT, PARTICIPATION_CARDINALITY

MANIFOLD = "andfam.commerce"


def _strip_docstrings(tree: ast.AST) -> ast.AST:
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            body = getattr(node, "body", [])
            if (body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant)
                    and isinstance(body[0].value.value, str)):
                node.body = body[1:] or [ast.Pass()]
    return tree


def _code_only(obj) -> str:
    return ast.unparse(_strip_docstrings(ast.parse(textwrap.dedent(inspect.getsource(obj)))))


class _DropRefusalText(ast.NodeTransformer):
    """Refusal message text is prose, not a decision — see the B-3 suite for why this exists."""

    def visit_Call(self, node: ast.Call) -> ast.Call:                     # noqa: N802 - ast API
        self.generic_visit(node)
        name = getattr(node.func, "id", getattr(node.func, "attr", ""))
        if name == "KernelRefusal":
            node.args = [ast.Constant(value="<refusal text>")]
            node.keywords = []
        return node


def _decisions_only(module) -> str:
    tree = _strip_docstrings(ast.parse(textwrap.dedent(inspect.getsource(module))))
    return ast.unparse(ast.fix_missing_locations(_DropRefusalText().visit(tree)))


def _count_binding(**kw):
    """A binding for `order_count`: **coordinates and nothing else.**"""
    return PhysicalFamilyBinding(
        family_id="order_count", schema=W.SCHEMA, table=W.TABLE,
        coordinates={"store": W.STORE_COLUMN, "day": W.DAY_COLUMN, "order": W.ORDER_COLUMN}, **kw)


@pytest.fixture
def world(tmp_path):
    mme, service, source, provider, coordinator = EX.cold_world(W.build(tmp_path))
    mme.authority.register_family({f.family_id: f for f in CEX._families(MANIFOLD)}["order_count"])
    return mme, service, source, provider, coordinator


# ══ F · NO INFERENCE IS POSSIBLE, BECAUSE THE VOCABULARY IS NOT THERE ═════════════════════════════

def test_the_provider_names_no_law_no_fold_shape_and_no_value_domain():
    code = _decisions_only(duckdb_realization)
    for law_name in ("SUM", "COUNT", "HLL_SKETCH", "STOCK_LEVEL", "LAST", "MEAN"):
        assert law_name not in code, law_name
    for shape in ("population", "value-bearing", "VALUE_BEARING", "POPULATION", "FOLD_SHAPES"):
        assert shape not in code, shape
    for domain in ("decimal", "integer", "sketch"):
        assert domain not in code, domain
    assert "_POPULATION_LAWS" not in code


def test_the_only_governed_token_it_holds_is_the_formation_constant_and_it_is_imported():
    code = _decisions_only(duckdb_realization)
    assert "PARTICIPATION_CARDINALITY" in code, "it must be able to tell which formation it was handed"
    assert "'participation-cardinality'" not in code and '"participation-cardinality"' not in code
    assert "from columna_platform.kernel.sorts import PARTICIPATION_CARDINALITY" in inspect.getsource(
        duckdb_realization)


def test_the_provider_holds_no_mapping_from_anything_to_a_formation():
    """It branches ON the declared formation; it derives one from nothing."""
    code = _decisions_only(DuckDbFamilyProvider.realize)
    # It branches ON the carried formation...
    assert "handle.formation == _CARDINALITY" in code
    # ...and on nothing else that could stand in for one.
    assert "handle.law ==" not in code
    assert "fold_shape ==" not in code
    assert "value_form ==" not in code


# ══ D/E · THE CARRIAGE, AND THE TWO REALIZATION BEHAVIOURS ════════════════════════════════════════

def test_the_formation_rides_from_the_requirement_onto_the_handle(world):
    mme, _, source, provider, _ = world
    for family_id, expected in (("revenue", DIRECT), ("order_count", PARTICIPATION_CARDINALITY)):
        family = mme.family(family_id)
        requirement = mme.requirement_for(family, family.root).requirement
        bound = DuckDbFamilyProvider(
            source, W.binding() if family_id == "revenue" else _count_binding())
        proposal = next(iter(bound.propose(requirement)))
        assert proposal.handle.formation == expected
    assert source.fetches == [], "capability discovery opened nothing"


def test_a_DIRECT_root_is_realized_from_its_physical_value_column(world):
    mme, _, source, provider, _ = world
    family = mme.family("revenue")
    requirement = mme.requirement_for(family, family.root).requirement
    offer = provider.realize(next(iter(provider.propose(requirement))))
    assert W.VALUE_COLUMN in source.fetches[0][3]
    assert offer.value.values.to_pylist() == [o[3] for o in W.ORDERS]


def test_a_CARDINALITY_root_is_realized_from_COORDINATES_ONLY(world):
    """**The binding names no value column and the projection asks for none.** The value is the size of
    the governed participating domain, and the domain is what the projection returns."""
    mme, _, source, _, _ = world
    family = mme.family("order_count")
    requirement = mme.requirement_for(family, family.root).requirement
    bound = DuckDbFamilyProvider(source, _count_binding(), name="duckdb-warehouse")
    offer = bound.realize(next(iter(bound.propose(requirement))))

    sql = source.fetches[0][3]
    assert W.VALUE_COLUMN not in sql, sql
    assert sql == 'SELECT "booked_on", "order_ref", "shop_code" FROM "sales"."fact_order"'
    assert isinstance(offer.value.values, (pa.Array, pa.ChunkedArray))
    assert offer.value.values.to_pylist() == [1] * len(W.ORDERS)
    assert offer.value.value_form == "scalar"


def test_the_cardinality_payload_is_counted_and_not_a_hardcoded_one(world):
    """A projection returning two rows for one governed coordinate yields **2**, not 1. The provider
    counts the domain it was given; whether 2 is admissible is the fidelity authority's question."""
    mme, _, source, _, _ = world
    duplicated = W.ORDERS + (W.ORDERS[0],)
    path = W.build(source.path.rsplit("/", 1)[0], filename="dupes.duckdb", orders=duplicated)
    from columna_adbc import DuckDbAdbcSource

    dupe_source = DuckDbAdbcSource(path=path, name="dupes")
    family = mme.family("order_count")
    requirement = mme.requirement_for(family, family.root).requirement
    bound = DuckDbFamilyProvider(dupe_source, _count_binding(), name="duckdb-warehouse")
    offer = bound.realize(next(iter(bound.propose(requirement))))
    assert sorted(offer.value.values.to_pylist()) == [1, 1, 1, 1, 1, 2]


def test_a_counted_root_that_disagrees_with_the_domain_IS_REFUSED_AT_FIDELITY(world):
    """The duplicate-row case, carried through to the authority: the index can hold one position per
    coordinate, so a count of 2 there contradicts the domain the claim covers."""
    mme, _, source, _, _ = world
    duplicated = W.ORDERS + (W.ORDERS[0],)
    path = W.build(source.path.rsplit("/", 1)[0], filename="dupes2.duckdb", orders=duplicated)
    from columna_adbc import DuckDbAdbcSource

    family = mme.family("order_count")
    requirement = mme.requirement_for(family, family.root).requirement
    bound = DuckDbFamilyProvider(DuckDbAdbcSource(path=path, name="d"), _count_binding(),
                                 name="duckdb-warehouse")
    offer = bound.realize(next(iter(bound.propose(requirement))))
    adjudication = mme.realizations.adjudicate(offer)
    assert not adjudication
    assert adjudication.refusal.code == "realization-contradicts-its-formation"


# ══ THE BINDING MUST SUIT THE FORMATION, AND BOTH REFUSALS ARE CONTRADICTIONS ══════════════════════

def test_a_cardinality_binding_that_names_a_value_column_is_refused(world):
    """A second, independent source for a value with exactly one constitution — free to disagree with the
    domain it is supposed to be the size of. That is the laundering surface, refused at the binding."""
    mme, _, source, _, _ = world
    family = mme.family("order_count")
    requirement = mme.requirement_for(family, family.root).requirement
    bound = DuckDbFamilyProvider(source, _count_binding(value_column=W.VALUE_COLUMN))
    with pytest.raises(KernelRefusal) as raised:
        bound.realize(next(iter(bound.propose(requirement))))
    assert raised.value.code == "cardinality-binding-names-a-value-column"
    assert source.fetches == [], "it refused before opening anything"


def test_a_DIRECT_binding_with_no_value_column_is_refused(world):
    mme, _, source, _, _ = world
    family = mme.family("revenue")
    requirement = mme.requirement_for(family, family.root).requirement
    bound = DuckDbFamilyProvider(source, PhysicalFamilyBinding(
        family_id="revenue", schema=W.SCHEMA, table=W.TABLE,
        coordinates={"store": W.STORE_COLUMN, "day": W.DAY_COLUMN, "order": W.ORDER_COLUMN}))
    with pytest.raises(KernelRefusal) as raised:
        bound.realize(next(iter(bound.propose(requirement))))
    assert raised.value.code == "binding-names-no-value-source"
    assert source.fetches == []


def test_a_requirement_with_no_formation_is_refused_never_guessed(world):
    from dataclasses import replace

    mme, _, source, provider, _ = world
    family = mme.family("revenue")
    requirement = replace(mme.requirement_for(family, family.root).requirement, formation="")
    with pytest.raises(KernelRefusal) as raised:
        provider.realize(next(iter(provider.propose(requirement))))
    assert raised.value.code == "requirement-states-no-root-formation"
    assert source.fetches == []


# ══ B-2 IS UNCHANGED ══════════════════════════════════════════════════════════════════════════════

def test_the_b2_revenue_cold_to_warm_behaviour_is_unchanged(world):
    _, service, source, _, _ = world
    cold = service.serve(EX.ASK)
    assert cold.classification == "serve", cold.render()
    assert len(source.fetches) == 1
    warm = service.serve(EX.ASK)
    assert warm.classification == "serve"
    assert len(source.fetches) == 1
    assert warm.frame.rows == cold.frame.rows


def test_the_b2_exhibit_still_runs_green(capsys):
    assert EX.main() == 0
    assert "ALL CHECKS PASSED" in capsys.readouterr().out
