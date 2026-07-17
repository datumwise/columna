"""
test_envelope_parser.py — the FrameQL ENVELOPE grammar parser (WP-FrameQL increment 1, PARSE ONLY).

Covers the ratified statement form (§§1–7): the clause set + order, `@` input / `AT` output, the
worked example (§7) as the acceptance target, and the four-mood-temperament error paths (§4–5 laws
are plan-time and NOT asserted here — only grammar). No planner, no engine.
"""
import pytest

from columna_core.envelope import (
    parse_statement, Statement, Series, Binding, OrderKey, Limit, EnvelopeSyntaxError,
)


# --- the smallest well-formed statement ----------------------------------------------------------
def test_minimal_select_at():
    st = parse_statement("SELECT revenue AT {region}")
    assert isinstance(st, Statement)
    assert st.series == [Series(expr="revenue", alias=None)]
    assert st.anchor == ("region",)
    assert st.explain is False and st.from_manifold is None
    assert st.bindings == [] and st.where == [] and st.having == [] and st.order_by == [] and st.limit is None


def test_grand_total_frame():
    st = parse_statement("SELECT sum(revenue) AT {}")
    assert st.anchor == ()                      # AT {} is the grand-total frame (§1)


def test_anchor_product_star_and_comma():
    a = parse_statement("SELECT revenue AT {region*store}").anchor
    b = parse_statement("SELECT revenue AT {region, store}").anchor
    assert a == b == ("region", "store")        # `*` canonical, comma accepted-on-input, both desugar the same


def test_case_insensitive_keywords():
    st = parse_statement("select revenue as r at {region}")
    assert st.series == [Series(expr="revenue", alias="r")]
    assert st.anchor == ("region",)


# --- @ is the input anchor; AT is the output -----------------------------------------------------
def test_input_anchor_inside_reduction_is_verbatim():
    st = parse_statement("SELECT avg(aov @ {day}) AS typical AT {region}")
    # the series expression (with its `@ {day}` input anchor) is captured verbatim for the expr parser
    assert st.series == [Series(expr="avg(aov @ {day})", alias="typical")]
    assert st.anchor == ("region",)


def test_at_word_not_matched_inside_identifier():
    # `at_risk_count` must not trip the AT clause (whole-word matching)
    st = parse_statement("SELECT at_risk_count AT {region}")
    assert st.series == [Series(expr="at_risk_count", alias=None)]
    assert st.anchor == ("region",)


# --- multi-series juxtaposition + AS -------------------------------------------------------------
def test_multi_series_with_aliases():
    st = parse_statement("SELECT sum(revenue @ {transaction}) AS gross, avg(aov @ {day}) AS typical AT {region}")
    assert st.series == [
        Series(expr="sum(revenue @ {transaction})", alias="gross"),
        Series(expr="avg(aov @ {day})", alias="typical"),
    ]


def test_comma_inside_call_is_not_a_series_separator():
    st = parse_statement("SELECT lag(revenue, n=1) AS lagged AT {cal.month}")
    assert st.series == [Series(expr="lag(revenue, n=1)", alias="lagged")]


# --- FROM / WITH / EXPLAIN preamble --------------------------------------------------------------
def test_from_optional_and_parsed():
    st = parse_statement("FROM retail SELECT revenue AT {region}")
    assert st.from_manifold == "retail"


def test_with_bindings():
    st = parse_statement("WITH line = revenue @ {transaction} SELECT sum(line) AS gross AT {region}")
    assert st.bindings == [Binding(name="line", expr="revenue @ {transaction}")]


def test_explain_prefix():
    st = parse_statement("EXPLAIN SELECT revenue AT {region}")
    assert st.explain is True and st.series == [Series(expr="revenue", alias=None)]


# --- WHERE / HAVING / ORDER BY / LIMIT PER -------------------------------------------------------
def test_where_and_having_split_on_AND():
    st = parse_statement("SELECT sum(revenue) AS gross AT {region} "
                         "WHERE region = 'west' AND day >= '2024-01-01' HAVING gross > 1000")
    assert st.where == ["region = 'west'", "day >= '2024-01-01'"]
    assert st.having == ["gross > 1000"]


def test_order_by_directions():
    st = parse_statement("SELECT revenue AT {region*store} ORDER BY region, revenue DESC")
    assert st.order_by == [OrderKey(column="region", descending=False),
                           OrderKey(column="revenue", descending=True)]


def test_limit_per():
    st = parse_statement("SELECT revenue AT {region*store} ORDER BY revenue DESC LIMIT 3 PER {region}")
    assert st.limit == Limit(n=3, per=("region",))


def test_limit_bare():
    assert parse_statement("SELECT revenue AT {region} LIMIT 10").limit == Limit(n=10, per=())


# --- THE WORKED EXAMPLE (§7) — the acceptance target ---------------------------------------------
def test_worked_example_top3_per_region():
    q = (
        "FROM retail\n"
        "WITH line = revenue @ {transaction}\n"
        "SELECT sum(line)        AS gross,\n"
        "       avg(aov @ {day}) AS typical\n"
        "AT { region * store }\n"
        "ORDER BY gross DESC\n"
        "LIMIT 3 PER { region }"
    )
    st = parse_statement(q)
    assert st.from_manifold == "retail"
    assert st.bindings == [Binding(name="line", expr="revenue @ {transaction}")]
    assert st.series == [Series(expr="sum(line)", alias="gross"),
                         Series(expr="avg(aov @ {day})", alias="typical")]
    assert st.anchor == ("region", "store")
    assert st.order_by == [OrderKey(column="gross", descending=True)]
    assert st.limit == Limit(n=3, per=("region",))


def test_canonical_round_trip():
    q = "FROM retail WITH line = revenue @ {transaction} SELECT sum(line) AS gross AT {region*store} ORDER BY gross DESC LIMIT 3 PER {region}"
    st = parse_statement(q)
    # re-parsing the canonical rendering yields an equal AST (structure captured, spelling normalized)
    assert parse_statement(st.render_canonical()) == st


# --- four-mood-temperament error paths (grammar only) --------------------------------------------
@pytest.mark.parametrize("bad, needle", [
    ("",                                   "empty query"),
    ("SELECT revenue",                     "AT { … }"),                 # no output grain
    ("AT {region}",                        "SELECT"),                   # no series
    ("SELECT revenue AT region",           "braced anchor"),           # anchor needs braces
    ("SELECT AT {region}",                 "names no series"),
    ("SELECT revenue AT {}extra AT {x}",   "more than once"),          # AT twice
    ("SELECT revenue WHERE x=1 AT {r}",    "out of order"),            # WHERE before AT
    ("SELECT revenue AT {region} LIMIT x", "whole number"),
    ("SELECT revenue AT {region} LIMIT 0", "positive count"),
    ("SELECT (revenue AT {region}",        "unbalanced"),
    ("SELECT revenue AS a AS b AT {r}",    "AS more than once"),
    ("WITH = revenue SELECT x AT {r}",     "malformed WITH"),
    ("EXPLAIN SELECT x AT {r} EXPLAIN",    "more than once"),          # EXPLAIN not leading/duplicated
    ("SELECT x AT {region} HAVING",        "no predicate"),
])
def test_syntax_errors_name_the_remedy(bad, needle):
    with pytest.raises(EnvelopeSyntaxError) as ei:
        parse_statement(bad)
    assert needle in str(ei.value)


def test_explain_must_lead():
    with pytest.raises(EnvelopeSyntaxError) as ei:
        parse_statement("SELECT revenue AT {region} EXPLAIN")
    assert "leading prefix" in str(ei.value) or "more than once" in str(ei.value)
