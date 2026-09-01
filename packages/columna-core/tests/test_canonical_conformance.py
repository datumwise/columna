"""Step 0 of the jurisdiction repair — CANONICAL CONFORMANCE (P1-19, P1-27).

The governing invariant, ruled 2026-09-01:

    The realization must answer the canonical request that was actually submitted.

These are INVARIANT tests, not regression tests. Each states a property over the whole canonical
form rather than pinning one statement's disposition, because the two rows they close were both
cases of something OUTSIDE the canonical statement deciding which request got answered:

  * P1-27 — `desugar` inlined WITH bindings into the series and copied WHERE verbatim, so a macro in
    WHERE reached the planner unexpanded. Where the macro's name collided with a declared level the
    unexpanded name resolved to the HOMONYM, and a different question was answered and SERVED clean
    with no disclosure.
  * P1-19 — no consumer of `stmt.from_manifold` existed anywhere in the tree, so an explicitly named
    Manifold was silently replaced by the surface binding.

Ruling v0.2 §9: "Binding may supply omitted context. It may not override explicit canonical meaning."
§14: realization "may not reinterpret explicit canonical meaning after adjudication."

Deliberately NOT tested here, because it is the law rather than an omission: HAVING and ORDER BY are
not macro-expanded. `_validate_clause_refs` states the §5 clause-reference law — they "reference the
output frame's OWN columns only" — and a macro's name survives its own inlining as the series name,
so `HAVING profit > 0` over a bare-macro series is an output-column reference. Expanding it would
break §6.14 by violating the law that makes §6.14 work. See `test_having_is_not_expanded_by_law`.
"""
import duckdb
import pytest

from columna_core import ManifoldServer
from columna_core.connector import DuckDBConnector
from columna_core.envelope import parse_statement
from columna_core.frameql import FrameQLSyntaxError
from columna_core.parser import parse_manifold

# `day` is BASE; `month` and `region` are reached across a hierarchy, so a WHERE on either is lawful
# but not push-down-executable on this build (P1-14's `filter_unsupported`). That asymmetry is what
# makes the shadowing test meaningful: the shadowed spelling used to SERVE while its own expansion
# could not, which is exactly "a different question was answered".
_CML = """
MANIFOLD w VERSION 1
UNIVERSE sales = customer * day BASIS events
LEVEL customer = customer_id BASE
LEVEL day      = day         BASE
LEVEL month    = month
LEVEL region   = region
HIERARCHY cal { day -> month VIA days(day, month) }
HIERARCHY geo { customer -> region VIA customers(customer_id, region) }
MEASURE revenue ON sales FROM txns AS sum(amount)
MEASURE cost    ON sales FROM txns AS sum(spend)
"""


@pytest.fixture(scope="module")
def manual_server():
    con = duckdb.connect()
    con.execute("CREATE TABLE customers (customer_id VARCHAR, region VARCHAR)")
    con.executemany("INSERT INTO customers VALUES (?, ?)", [("C1", "east"), ("C2", "west")])
    con.execute("CREATE TABLE days (day VARCHAR, month VARCHAR)")
    con.executemany("INSERT INTO days VALUES (?, ?)",
                    [("2024-01-05", "2024-01"), ("2024-02-02", "2024-02")])
    con.execute("CREATE TABLE txns (customer_id VARCHAR, day VARCHAR, amount DOUBLE, spend DOUBLE)")
    con.executemany("INSERT INTO txns VALUES (?, ?, ?, ?)",
                    [("C1", "2024-01-05", 120.0, 30.0), ("C1", "2024-02-02", 80.0, 20.0),
                     ("C2", "2024-02-02", 200.0, 90.0)])
    s = ManifoldServer(parse_manifold(_CML), connector=DuckDBConnector(con))
    s.publish()
    return s


def _desugar(srv, q):
    return srv.planner.desugar(parse_statement(q))


# ── P1-27 · the canonical form is TOTAL ────────────────────────────────────────────────────────────
def test_where_is_macro_expanded(manual_server):
    """A macro in WHERE reaches the planner as its expansion, not as its name."""
    d = _desugar(manual_server, "WITH d = day SELECT revenue AT {customer} WHERE d >= '2024-01-01'")
    assert d.where == ["day >= '2024-01-01'"], d.where
    assert d.bindings == []


def test_no_binding_name_survives_into_where(manual_server):
    """THE INVARIANT, stated over the clause rather than over one statement: after desugaring, no
    WITH binding's name may appear in any WHERE predicate. This is what makes the wrong-question
    state unreachable instead of merely repaired."""
    q = ("WITH d = day, r = region SELECT revenue AT {customer} "
         "WHERE d >= '2024-01-01' AND r == 'east'")
    stmt = parse_statement(q)
    names = {b.name for b in stmt.bindings}
    d = manual_server.planner.desugar(stmt)
    import re
    for pred in d.where:
        for n in names:
            assert not re.search(rf"\b{re.escape(n)}\b", pred), (n, pred, d.where)


def test_a_macro_shadowing_a_level_means_its_expansion_not_the_homonym(manual_server):
    """P1-27 condition 2, the reason the row was CRITICAL: `WITH day = month` + `WHERE day >= …`
    used to SERVE a plausible number by resolving `day` to the declared level. It must now mean what
    the Manual says it means (§4.5: "the canonical form of a statement is the canonical form of its
    full expansion") — which on this build is a filter the engine cannot push, i.e. NOT a serve."""
    shadowed = "WITH day = month SELECT revenue AT {customer} WHERE day >= '2024-02'"
    expansion = "SELECT revenue AT {customer} WHERE month >= '2024-02'"
    d = _desugar(manual_server, shadowed)
    assert d.where == ["month >= '2024-02'"], d.where
    got = manual_server.planner.run_statement(parse_statement(shadowed))
    want = manual_server.planner.run_statement(parse_statement(expansion))
    assert got.outcome == want.outcome
    assert got.outcome != "serve", "the shadowed spelling must not serve where its expansion cannot"


def test_a_free_macro_in_where_serves_exactly_as_the_hand_written_predicate(manual_server):
    """P1-27 condition 1: the unexpanded name used to produce a `filter_unreachable` CLARIFY that
    offered, as its remedy, the very level the macro was bound to."""
    macro = manual_server.planner.run_statement(parse_statement(
        "WITH d = day SELECT revenue AT {customer} WHERE d >= '2024-01-01'"))
    hand = manual_server.planner.run_statement(parse_statement(
        "SELECT revenue AT {customer} WHERE day >= '2024-01-01'"))
    assert macro.outcome == hand.outcome == "serve"
    assert macro.data.sort("customer").equals(hand.data.sort("customer"))


@pytest.mark.parametrize("q", [
    "WITH x = (x + 1) SELECT revenue AT {customer} WHERE x > 0",                  # self-referential
    "WITH a = (b + 1), b = (a + 1) SELECT revenue AT {customer} WHERE a > 0",     # mutually referential
])
def test_a_non_terminating_expansion_is_a_language_failure_not_a_wrong_answer(manual_server, q):
    """If a binding reintroduces a bound name the statement has no total canonical form. It cannot be
    adjudicated, so it is refused as a language failure rather than half-expanded and answered.

    This is the fixed-point check doing the work the substitution cannot: the substitution makes the
    common case right, the assertion makes the uncommon case impossible."""
    with pytest.raises(FrameQLSyntaxError, match="no total canonical form"):
        _desugar(manual_server, q)


def test_an_identity_binding_is_a_fixed_point_and_is_left_alone(manual_server):
    """The dual of the test above, and the reason it is a FIXED-POINT check rather than a
    contains-a-bound-name check: `WITH day = day` is harmless, expands to itself, and must not be
    mistaken for non-termination."""
    d = _desugar(manual_server, "WITH day = day SELECT revenue AT {customer} WHERE day >= '2024-02'")
    assert d.where == ["day >= '2024-02'"]


def test_having_is_not_expanded_by_law(manual_server):
    """NOT a defect, and pinned so a later reader does not "fix" it: §5's clause-reference law makes
    HAVING an output-frame reference, and a macro's name survives its own inlining as the series
    name. §6.14 works BECAUSE of that, not by coincidence."""
    q = "WITH profit = (revenue - cost) SELECT profit AT {customer} HAVING profit > 0"
    d = _desugar(manual_server, q)
    assert d.having == ["profit > 0"]
    assert [s.alias for s in d.series] == ["profit"]
    assert manual_server.planner.run_statement(parse_statement(q)).outcome == "serve"
