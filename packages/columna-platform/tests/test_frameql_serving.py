"""
test_frameql_serving.py — real Frame-QL text, served through the v8-native Platform MME.

    *"Stop when actual Frame-QL text is parsed as syntax, resolved against the Platform kernel, and
    served through the running MME. The authority path should be: Frame-QL syntax → Platform request
    interpretation → family or expression target → MME adjudication → Answer / classified refusal."*
        — Huayin, 2026-09-28

Every query in this file is a STRING. Nothing on the request side is constructed programmatically.
"""
from __future__ import annotations

import pytest

from columna_platform.frameql import FrameQLService, RequestInterpretationRefusal, interpret, parse
from columna_platform.frameql import exhibit as FQ
from columna_platform.frameql.serving import (
    DISCLOSE,
    REFUSE,
    SERVE,
    SYNTAX,
    UNRESOLVED,
    UNSUPPORTED,
)
from columna_platform.kernel import STRUCTURED
from columna_platform.kernel import exhibit as WORLD


@pytest.fixture
def service():
    return FrameQLService(WORLD.build())


def _cells(outcome):
    """The frame as `{coordinate tuple: value}` for a single-series ask."""
    return {row[:-1]: row[-1] for row in outcome.frame.rows}


# ══ 0 · THE BOUNDARY. The architectural claim, measured three ways. ═══════════════════════════════
def test_the_kernel_still_imports_nothing_from_columna_core():
    """Unchanged by this unit: `columna_platform.kernel` reaches Core nowhere. The serving layer sits
    OUTSIDE the kernel precisely so that this stays true."""
    import ast
    import pathlib

    import columna_platform.kernel as pkg

    offenders = []
    for path in sorted(pathlib.Path(pkg.__file__).parent.glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            names = ([a.name for a in node.names] if isinstance(node, ast.Import)
                     else [node.module or ""] if isinstance(node, ast.ImportFrom) else [])
            offenders += [f"{path.name}:{node.lineno} {n}" for n in names
                          if n.split(".")[0] == "columna_core"]
    assert not offenders, "\n".join(offenders)


def test_the_serving_layer_imports_exactly_one_core_module_and_it_is_the_grammar():
    """**THE LIFT, PINNED.** `columna_core.envelope` is the one Core import in Platform's v8-native
    path, it appears in exactly one file, and it is a grammar."""
    import ast
    import pathlib

    import columna_platform.frameql as pkg

    found: dict[str, set[str]] = {}
    for path in sorted(pathlib.Path(pkg.__file__).parent.glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            names = ([a.name for a in node.names] if isinstance(node, ast.Import)
                     else [node.module or ""] if isinstance(node, ast.ImportFrom) else [])
            for n in names:
                if n.split(".")[0] == "columna_core":
                    found.setdefault(path.name, set()).add(n)
    assert found == {"syntax.py": {"columna_core.envelope"}}, found


def test_the_lifted_grammar_is_PROVABLY_syntax_and_reaches_no_core_semantics():
    """**The claim that makes the import legitimate rather than convenient**, and the reason a 443-line
    copy was not made: importing the envelope pulls in TWO modules — the package's lazy `__init__` and
    the parser — and no Core analytical semantics, planner law, family/member model, generated-family
    doctrine or Operator Registry is reachable from it.

    Measured in a SUBPROCESS, because this interpreter has the whole estate loaded by other tests. The day
    someone adds a semantic import to the envelope, this fails loudly instead of quietly becoming false."""
    import subprocess
    import sys

    probe = (
        "import sys;"
        "before = set(sys.modules);"
        "import columna_core.envelope;"
        "after = sorted(m for m in set(sys.modules) - before if m.split('.')[0] == 'columna_core');"
        "print('CLOSURE:' + ','.join(after))"
    )
    result = subprocess.run([sys.executable, "-c", probe], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    closure = result.stdout.split("CLOSURE:")[1].strip().split(",")
    assert sorted(closure) == ["columna_core", "columna_core.envelope"], closure


def test_no_syntax_object_reaches_the_kernel_or_the_serving_path():
    """The AST stops in `syntax.py`. `Statement` is mentioned in exactly one Platform module, so a
    grammar fact cannot become a semantic one by being carried along."""
    import ast
    import pathlib

    import columna_platform.frameql as fq
    import columna_platform.kernel as kern

    mentions = []
    for pkg in (fq, kern):
        for path in sorted(pathlib.Path(pkg.__file__).parent.glob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Name) and node.id == "Statement":
                    mentions.append(path.name)
                if isinstance(node, ast.Attribute) and node.attr == "Statement":
                    mentions.append(path.name)
    assert set(mentions) <= {"syntax.py"}, sorted(set(mentions))


def test_no_rule_requires_a_basis_component_to_be_formed_by_the_component_law():
    """**RULING OF 2026-09-28, PINNED SO IT CANNOT REAPPEAR.** *"Do not add a rule that a basis operand
    must be identified by the law that 'formed' its family value. Root formation and family continuation
    stay separate. Expression basis roles bind governed analytical identities — for example Revenue and
    OrderCount — not root-formation operators."*

    The V8-1 report recommended exactly that rule and it was declined. Measured two ways: the basis binds
    identities whose own laws do NOT match the slot labels, and it resolves anyway."""
    mme = WORLD.build()
    aov = mme.expression("average_order_value")
    basis = aov.admitted_bases[0]
    # the COUNT slot is filled by `order_count`, whose own law is COUNT — but the SUM slot is filled by
    # `revenue`, whose law is SUM. Both happen to align here, so the real proof is the next one.
    assert basis.components == {"SUM": "revenue", "COUNT": "order_count"}

    # A basis whose slot labels do NOT match the bound families' laws still binds and still resolves,
    # because the slot is a BASIS ROLE and the family is a governed IDENTITY.
    from columna_platform.kernel import GovernedExpression, Operand, SufficientBasis

    swapped = mme.register_expression(GovernedExpression(
        expression_id="ratio_by_identity", universe="commerce", constructor="MEAN",
        operands=(Operand("operand", "revenue"),), participation=WORLD.PARTICIPATION,
        admitted_bases=(SufficientBasis(
            "b_identities", {"SUM": "revenue", "COUNT": "order_count"}, True),)))
    assert mme.evaluate(swapped, WORLD.TOTAL).served

    # and no module in the kernel or the serving path compares a family's law to a basis role
    import ast
    import pathlib

    import columna_platform.frameql as fq
    import columna_platform.kernel as kern

    for pkg in (kern, fq):
        for path in sorted(pathlib.Path(pkg.__file__).parent.glob("*.py")):
            src = path.read_text(encoding="utf-8")
            tree = ast.parse(src, filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Compare):
                    text = ast.get_source_segment(src, node) or ""
                    assert not (".law" in text and "role" in text), f"{path.name}: {text}"


def test_measure_family_law_means_the_continuation_law():
    """**RULING OF 2026-09-28.** *"If `MeasureFamily.law` in the new kernel means continuation law, keep
    it that way."* It is validated as continuation-bearing, so that is what it names."""
    mme = WORLD.build()
    for family_id in mme.families:
        law = mme.law_of(family_id)
        assert law.continuation_bearing and law.may_found_a_family
    assert not hasattr(mme.family("revenue"), "root_evaluator")


# ══ 1 · DIRECT FAMILY ═════════════════════════════════════════════════════════════════════════════
def test_a_family_serves_at_its_root_through_real_frameql(service):
    outcome = service.serve("SELECT revenue AT {store * day * order}")
    assert outcome.classification == SERVE
    assert outcome.sorts == {"revenue": "family"}
    assert outcome.frame.columns[0].route in ("root", "cached")


def test_a_family_serves_at_a_coarser_anchor_through_CONTINUATION(service):
    outcome = service.serve("SELECT revenue AT {day}")
    assert outcome.classification == SERVE
    assert outcome.frame.columns[0].sort == "family"
    assert outcome.frame.columns[0].route == "continued"
    assert _cells(outcome) == {("D1",): 175.0, ("D2",): 325.0}


def test_the_grand_total_is_a_declared_location(service):
    outcome = service.serve("SELECT revenue AT {}")
    assert outcome.frame.coordinates == ()
    assert outcome.frame.rows == ((500.0,),)


def test_several_series_at_one_anchor_come_back_as_one_frame(service):
    outcome = service.serve("SELECT revenue, order_count AT {day}")
    assert outcome.classification == SERVE
    assert [c.alias for c in outcome.frame.columns] == ["revenue", "order_count"]
    assert outcome.frame.rows == (("D1", 175.0, 2), ("D2", 325.0, 4))


def test_an_alias_is_honoured(service):
    outcome = service.serve("SELECT revenue AS takings AT {day}")
    assert [c.alias for c in outcome.frame.columns] == ["takings"]
    assert outcome.frame.columns[0].token == "revenue"


def test_the_canonical_request_form_is_syntax_free(service):
    request = interpret("SELECT revenue AT {day * store}",
                        universe_references=service.mme.universe.references)
    assert request.tokens == ("revenue",)
    assert request.anchor_constituents == frozenset({"day", "store"})
    assert "AT {day*store}" in request.canonical_syntax


# ══ 2 · STRUCTURED-FAMILY FINALIZATION ════════════════════════════════════════════════════════════
def test_the_sketch_family_continues_and_is_served_as_a_structured_value(service):
    outcome = service.serve("SELECT distinct_customers AT {day}")
    assert outcome.classification == DISCLOSE
    assert outcome.frame.columns[0].route == "continued"
    assert all(hasattr(v, "get_estimate") for v in _cells(outcome).values())
    assert service.mme.law_of("distinct_customers").value_form == STRUCTURED


def test_a_structured_family_value_is_rendered_opaquely_and_disclosed(service):
    """A sketch's `str()` emits a debug summary containing an `Estimate:` line. Rendering it naively would
    print a cardinality THROUGH THE FAMILY PATH, in a column labelled with the family's name, bypassing
    the expression that is the only lawful way to obtain one."""
    outcome = service.serve("SELECT distinct_customers AT {day}")
    assert "⟨hll_sketch⟩" in outcome.frame.render()
    assert "Estimate" not in outcome.frame.render()
    disclosure = next(d for d in outcome.disclosures if d.code == "structured-family-value")
    assert "has no display form" in disclosure.detail
    assert "HLL_ESTIMATE" in disclosure.detail


def test_the_user_asks_for_the_estimate_and_it_resolves_as_an_EXPRESSION(service):
    outcome = service.serve("SELECT distinct_customer_estimate AT {day}")
    assert outcome.sorts == {"distinct_customer_estimate": "expression"}
    assert outcome.frame.columns[0].route == "evaluated"
    assert outcome.frame.columns[0].via == "b_sketch"
    assert _cells(outcome) == {("D1",): 2, ("D2",): 3}


def test_the_estimates_scalar_cannot_seed_family_continuation_after_being_served(service):
    """**The flagship, reached through real Frame-QL.** The user's query cached an expression result; the
    engine will not let it become family state."""
    assert service.serve("SELECT distinct_customer_estimate AT {day}").served
    expression = service.mme.expression("distinct_customer_estimate")
    held = service.mme.retained(expression.at(WORLD.BY_DAY), expression.instance())
    assert held is not None and not held.continuation_bearing
    verdict = service.mme.adjudicate(held, service.mme.family("distinct_customers"), WORLD.BY_DAY)
    assert not verdict and verdict.code == "not-continuation-bearing"
    assert "never becomes family continuation state" in verdict.detail


def test_the_approximation_survives_the_serving_layer(service):
    for query in ("SELECT distinct_customers AT {day}",
                  "SELECT distinct_customer_estimate AT {day}"):
        outcome = service.serve(query)
        assert outcome.classification == DISCLOSE
        assert any(d.code == "approximate" for d in outcome.disclosures)


# ══ 3 · GOVERNED EXPRESSION ═══════════════════════════════════════════════════════════════════════
def test_aov_resolves_as_an_expression_and_serves_the_pooled_result(service):
    day = service.serve("SELECT average_order_value AT {day}")
    assert day.sorts == {"average_order_value": "expression"}
    assert _cells(day) == {("D1",): pytest.approx(87.5), ("D2",): pytest.approx(81.25)}
    total = service.serve("SELECT average_order_value AT {}")
    assert total.frame.rows[0][0] == pytest.approx(500 / 6)


def test_the_pooled_result_is_not_the_mean_of_the_daily_means(service):
    day = _cells(service.serve("SELECT average_order_value AT {day}"))
    pooled = service.serve("SELECT average_order_value AT {}").frame.rows[0][0]
    mean_of_means = (day[("D1",)] + day[("D2",)]) / 2
    assert mean_of_means == pytest.approx(84.375)
    assert abs(pooled - mean_of_means) > 1.0


def test_no_mean_family_exists_to_have_served_it(service):
    assert "mean_order_value" not in service.mme.families
    assert service.mme.sort_of("average_order_value") == "expression"


def test_explain_reports_the_authority_path_and_serves_nothing(service):
    outcome = service.serve("EXPLAIN SELECT average_order_value AT {}")
    assert outcome.frame is None
    plan = "\n".join(outcome.plan)
    assert "GOVERNED EXPRESSION" in plan and "MME.evaluate()" in plan
    assert "basis b_revenue_ordercount: COUNT→order_count, SUM→revenue" in plan
    assert "NOT EXECUTED" in plan


def test_explain_over_a_family_shows_every_candidate_and_its_adjudication(service):
    service.serve("SELECT revenue AT {day}")
    outcome = service.serve("EXPLAIN SELECT revenue AT {}")
    plan = "\n".join(outcome.plan)
    assert "FAMILY, R_F=commerce{day, order, store}" in plan
    assert "MME.measure()" in plan
    assert "ADMITTED" in plan


# ══ 4 · COMPATIBILITY REFUSAL ═════════════════════════════════════════════════════════════════════
def test_both_operands_serve_individually(service):
    outcome = service.serve("SELECT revenue, audited_order_count AT {day}")
    assert outcome.classification == SERVE
    assert outcome.frame.rows == (("D1", 175.0, 2), ("D2", 325.0, 2))


def test_the_expression_over_incompatible_operands_refuses_with_the_existing_reason(service):
    outcome = service.serve("SELECT average_order_value_audited AT {day}")
    assert outcome.classification == REFUSE
    detail = str(outcome.refusal)
    assert "different-participation" in detail
    assert "ESTABLISHED AND AVAILABLE" in detail
    assert "jointly meaningless" in detail
    assert "physical availability is not analytical authority" in detail


def test_the_refusal_names_the_series_it_came_from(service):
    outcome = service.serve("SELECT average_order_value_audited AS aov AT {day}")
    assert "series 'aov'" in outcome.refusal.detail


def test_a_frame_with_a_refused_column_is_not_served_partially(service):
    outcome = service.serve("SELECT revenue, average_order_value_audited AT {day}")
    assert outcome.classification == REFUSE
    assert outcome.frame is None


# ══ 5 · CONTINUATION-REGION REFUSAL, INCLUDING THE LAUNDERING CASE ════════════════════════════════
def test_a_stock_composes_across_stores_through_real_frameql(service):
    outcome = service.serve("SELECT on_hand AT {day}")
    assert outcome.classification == SERVE
    assert _cells(outcome) == {("D1",): 17, ("D2",): 21}


def test_a_stock_refuses_across_time(service):
    outcome = service.serve("SELECT on_hand AT {store}")
    assert outcome.classification == REFUSE
    assert "outside-continuation-region" in str(outcome.refusal)
    assert "does NOT compose ACROSS TIME" in str(outcome.refusal)


def test_the_laundering_case_refuses_through_the_serving_path(service):
    """The intermediate is served by a real query first, so the held state genuinely exists when the
    second query asks for the total."""
    assert service.serve("SELECT on_hand AT {day}").served
    outcome = service.serve("SELECT on_hand AT {}")
    assert outcome.classification == REFUSE
    assert "cannot launder an edge the law does not admit" in str(outcome.refusal)
    assert any(k.identity == "on_hand" and k.anchor == WORLD.BY_DAY for k in service.mme.held)


def test_the_flow_family_is_unaffected_by_the_stocks_restriction(service):
    assert service.serve("SELECT revenue AT {store}").served
    assert service.serve("SELECT revenue AT {}").served


# ══ the refusal taxonomy ══════════════════════════════════════════════════════════════════════════
def test_an_unknown_name_is_UNRESOLVED_and_not_a_claim_about_families(service):
    outcome = service.serve("SELECT profit AT {day}")
    assert outcome.classification == UNRESOLVED
    assert outcome.sorts == {"profit": None}
    detail = str(outcome.refusal)
    assert "not a claim that no FAMILY answers to the name" in detail
    assert "no near match is guessed" in detail


@pytest.mark.parametrize("query,clause", [
    ("SELECT revenue AT {day} WHERE store = 'S1'", "where"),
    ("SELECT revenue AT {day} HAVING revenue > 1", "having"),
    ("SELECT revenue AT {day} ORDER BY revenue", "order by"),
    ("SELECT revenue AT {day} LIMIT 1", "limit"),
    ("WITH r = revenue SELECT r AT {day}", "with"),
    ("FROM commerce SELECT revenue AT {day}", "from"),
])
def test_every_unimplemented_clause_refuses_by_name_and_nothing_is_ignored(service, query, clause):
    outcome = service.serve(query)
    assert outcome.classification == UNSUPPORTED
    assert clause.upper() in str(outcome.refusal)
    assert "CAPABILITY limit, not a governed one" in str(outcome.refusal)


def test_an_arithmetic_series_is_refused_because_this_profile_is_expression_first(service):
    outcome = service.serve("SELECT revenue / order_count AT {day}")
    assert outcome.classification == UNSUPPORTED
    assert "EXPRESSION-FIRST" in str(outcome.refusal)
    assert "Declare the composition as a governed expression" in str(outcome.refusal)


def test_a_dotted_series_and_a_dotted_anchor_level_both_refuse(service):
    assert service.serve("SELECT revenue.sum AT {day}").classification == UNSUPPORTED
    assert "dotted-series-token" in str(service.serve("SELECT revenue.sum AT {day}").refusal)
    assert "dotted-anchor-level" in str(service.serve("SELECT revenue AT {cal.day}").refusal)


def test_an_unknown_anchor_constituent_is_reported_where_the_query_is_still_in_hand(service):
    outcome = service.serve("SELECT revenue AT {region}")
    assert outcome.classification == UNSUPPORTED
    assert "unknown-anchor-constituent" in str(outcome.refusal)
    assert "day" in str(outcome.refusal) and "store" in str(outcome.refusal)


def test_a_repeated_anchor_constituent_refuses_because_an_anchor_is_a_SET(service):
    outcome = service.serve("SELECT revenue AT {day * day}")
    assert outcome.classification == UNSUPPORTED
    assert "more than once" in str(outcome.refusal)


def test_malformed_text_is_a_SYNTAX_outcome_and_never_an_exception(service):
    for bad in ("SELECT revenue FROM WHERE", "revenue @ day", "", "SELECT AT {day}"):
        outcome = service.serve(bad)
        assert outcome.classification == SYNTAX, bad
        assert outcome.refusal.code == "frameql_syntax"


def test_a_realization_limit_reaches_the_caller_as_UNSUPPORTED_not_as_a_refusal():
    """A backend's inability does not remove a law, so it must not arrive as a governed `no`."""
    from columna_platform.kernel import MME, REGISTRY
    from columna_platform.kernel.builtins import NO_MEAN

    mme = MME(WORLD.COMMERCE, REGISTRY, NO_MEAN)
    revenue, order_count, *_ = WORLD._families()
    mme.register_family(revenue)
    mme.register_family(order_count)
    aov, *_ = WORLD._expressions()
    mme.register_expression(aov)
    mme.establish_root(revenue, WORLD.ORDERS)
    mme.establish_root(order_count, WORLD.ORDERS)
    outcome = FrameQLService(mme).serve("SELECT average_order_value AT {}")
    assert outcome.classification == UNSUPPORTED
    assert "no realization in provider profile" in str(outcome.refusal)


def test_the_grammar_is_reused_and_not_reimplemented():
    """`parse` is the ratified envelope parser, unmodified. Its full clause set still parses even though
    this profile serves a subset — proof that the grammar was not redesigned."""
    statement = parse("EXPLAIN FROM m WITH r = revenue SELECT r AS x AT {a * b} "
                      "WHERE p HAVING q ORDER BY x DESC LIMIT 5 PER {a}")
    assert statement.explain and statement.from_manifold == "m"
    assert statement.anchor == ("a", "b") and statement.limit.n == 5
    with pytest.raises(RequestInterpretationRefusal):
        interpret("SELECT revenue AT {day} LIMIT 1")


# ══ the exhibit runs ══════════════════════════════════════════════════════════════════════════════
def test_the_frameql_exhibit_runs_green(capsys):
    assert FQ.main() == 0
    out = capsys.readouterr().out
    assert "ALL CHECKS PASSED" in out and "✗" not in out
    for proof in ("PROOF 1 ·", "PROOF 2 ·", "PROOF 3 ·", "PROOF 4 ·", "PROOF 5 ·"):
        assert proof in out
