"""The Afternoon v0.13 page gate, hermetic — the five statements the essay actually prints.

WHY THIS EXISTS SEPARATELY FROM THE LAUNDERING MATRIX. `test_generated_family_law.py` certifies the
GENERATED-FAMILY LAW: every spelling of "sum a stock across calendar" refuses identically and cannot
return the wrong number. That is DG-2 forward invariant 5's evidence and it stays where it is.

This file certifies something different and narrower: that the five executable Frame-QL statements
printed in *The Theory of Data in One Afternoon* v0.13 (ledger CT-1) earn, verbatim, the verdicts the
essay claims for them. The essay is a promise about this system; a promise nothing runs is prose.

Only ONE of the five (beat 5) is a laundering case. The other four are the lawful register the refusal
is read against — a system that refused everything would satisfy the matrix and betray the essay.

SYNTAX IS PART OF THE CLAIM. Every beat goes through `parse_statement`, not the `.column()` builder.
Beat 2's braced composite pin `avg(revenue @ {order})` is rejected by the builder outright, and a gate
that rewrote it into builder-acceptable syntax would certify a question no reader can copy off the
page. `scripts/afternoon_five.py` runs these same five with explicit engine provenance (source vs
installed); this file is the CI-resident copy that runs on every PR.
"""
import os
import sys

import duckdb
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "fixtures"))    # noqa: E402
import afternoon_world                                                     # noqa: E402
from columna_core import DuckDBConnector, ManifoldServer                   # noqa: E402
from columna_core.disclosure_wire import wire_frame                        # noqa: E402
from columna_core.envelope import parse_statement                          # noqa: E402
from columna_core.parser import parse_file                                 # noqa: E402

_FIXTURE = os.path.join(os.path.dirname(__file__), "fixtures", "afternoon.cml")


@pytest.fixture(scope="module")
def afternoon():
    m = parse_file(_FIXTURE)
    srv = ManifoldServer(m, DuckDBConnector(afternoon_world.build(duckdb.connect())))
    srv.publish()
    return srv


def _ask(srv, statement):
    """The real ask surface — the exact syntax the page prints, through the statement parser."""
    return wire_frame(srv.planner.run_statement(parse_statement(statement)))


def _column(wire):
    return wire["columns"][0]


def _rows(wire):
    return _column(wire).get("values") or []


def _pinned_levels(wire):
    """The levels an `input_anchor_ambiguous` clarify offers, read out of its own alternatives."""
    nr = _column(wire).get("no_result") or {}
    out = []
    for a in nr.get("alternatives") or []:
        d = a.get("description") or ""
        if "pin the input anchor to '" in d:
            out.append(d.split("pin the input anchor to '", 1)[1].split("'", 1)[0])
    return sorted(out)


# ── beat 1 ───────────────────────────────────────────────────────────────────────────────────────
def test_beat_1_the_flow_at_its_own_grain_serves(afternoon):
    """`SELECT revenue AT {store, month}` -> Serve. The control: the system is not simply cautious."""
    w = _ask(afternoon, "SELECT revenue AT {store, month}")
    assert w["outcome"] == "serve"
    rows = _rows(w)
    assert len(rows) == 6
    s1_jan = next(r["value"] for r in rows if r["store"] == "S1" and r["month"] == "2025-01")
    assert s1_jan == afternoon_world.S1_JAN_REVENUE     # 120 + 80 + 100, summed lawfully along calendar


# ── beat 2 ───────────────────────────────────────────────────────────────────────────────────────
def test_beat_2_pinned_inline_average_across_two_lineages_serves(afternoon):
    """`SELECT avg(revenue @ {order}) AT {region, quarter}` -> Serve.

    The braced composite pin is the page's own syntax and only the statement path accepts it; pinning
    the input anchor is precisely what turns beat 4's ambiguity into a definite quantity.
    """
    w = _ask(afternoon, "SELECT avg(revenue @ {order}) AT {region, quarter}")
    assert w["outcome"] == "serve"
    by_region = {r["region"]: r["value"] for r in _rows(w)}
    assert set(by_region) == {"north", "south"}
    assert by_region["north"] == pytest.approx(afternoon_world.NORTH_Q1_AVG_ORDER)   # 890 / 6 orders
    assert by_region["south"] == pytest.approx(afternoon_world.SOUTH_Q1_AVG_ORDER)   # 275 / 2 orders


def test_beat_2_syntax_is_load_bearing_the_builder_cannot_express_it(afternoon):
    """The braced pin is why this gate uses the statement parser: the builder API rejects it.

    Pinned so the gate can never be "simplified" into the builder path — that would silently certify
    a different question than the one printed on the page.
    """
    w = wire_frame(afternoon.frame("region", "quarter").column("c", "avg(revenue @ {order})").run())
    assert w["outcome"] == "error"
    assert "illegal expression construct" in ((_column(w).get("no_result") or {}).get("detail") or "")


# ── beat 3 ───────────────────────────────────────────────────────────────────────────────────────
def test_beat_3_the_flow_coarsened_both_ways_serves(afternoon):
    """`SELECT revenue AT {region, quarter}` -> Serve. Transport up both hierarchies at once."""
    w = _ask(afternoon, "SELECT revenue AT {region, quarter}")
    assert w["outcome"] == "serve"
    by_region = {r["region"]: r["value"] for r in _rows(w)}
    assert by_region == {"north": afternoon_world.NORTH_Q1_REVENUE,
                         "south": afternoon_world.SOUTH_Q1_REVENUE}


# ── beat 4 ───────────────────────────────────────────────────────────────────────────────────────
def test_beat_4_unpinned_max_clarifies_over_exactly_the_lawful_grains(afternoon):
    """`SELECT max(revenue) AT {region, month}` -> Clarify / input_anchor_ambiguous.

    The ratified witness (Huayin, 2026-08-20): a GENUINE two-lawful-candidate ask. Clarify is for
    unresolved choice among LAWFUL meanings — never a softer way to refuse. The alternative set is
    asserted exactly, because a clarify that enumerated an unlawful grain would be offering a way in.
    """
    w = _ask(afternoon, "SELECT max(revenue) AT {region, month}")
    assert w["outcome"] == "clarify"
    nr = _column(w)["no_result"]
    assert nr["reason"] == "input_anchor_ambiguous"
    assert nr["kind"] == "clarify"
    assert _pinned_levels(w) == ["day", "store"]           # exactly two, exactly these
    assert _rows(w) == []                                  # a clarify hands back no numbers


# ── beat 5 ───────────────────────────────────────────────────────────────────────────────────────
def test_beat_5_the_burn_refuses_with_no_values(afternoon):
    """`SELECT sum(on_hand) AT {store, month}` -> Refuse / blocked_reduction.

    The Afternoon's own case. The assertion that matters is not the mood but the ABSENCE of the
    number: 1410 is the same units counted once per day they sat on the shelf, and no caveat makes it
    a quantity of anything.
    """
    w = _ask(afternoon, "SELECT sum(on_hand) AT {store, month}")
    assert w["outcome"] == "refuse"
    nr = _column(w)["no_result"]
    assert nr["reason"] == "blocked_reduction"
    assert nr["kind"] == "refuse"
    assert _rows(w) == []
    assert nr.get("alternatives"), "a refusal must name the lawful neighbours"


def test_beat_5_never_returns_the_afternoons_wrong_number(afternoon):
    """The number, not the mood. Asserted as a value so a future 'helpful' disclosure cannot restore it."""
    w = _ask(afternoon, "SELECT sum(on_hand) AT {store, month}")
    assert afternoon_world.S1_JAN_STOCK_SUM not in [r.get("value") for r in _rows(w)]


# ── the gate as a whole ──────────────────────────────────────────────────────────────────────────
FIVE = [
    ("SELECT revenue AT {store, month}",                   "serve",   None),
    ("SELECT avg(revenue @ {order}) AT {region, quarter}", "serve",   None),
    ("SELECT revenue AT {region, quarter}",                "serve",   None),
    ("SELECT max(revenue) AT {region, month}",             "clarify", "input_anchor_ambiguous"),
    ("SELECT sum(on_hand) AT {store, month}",              "refuse",  "blocked_reduction"),
]


@pytest.mark.parametrize("statement,outcome,reason", FIVE,
                         ids=["1-serve", "2-serve-pinned", "3-serve-coarse", "4-clarify", "5-refuse"])
def test_the_five_earn_the_verdicts_the_essay_claims(afternoon, statement, outcome, reason):
    """The whole gate in one table — the five statements, the five verdicts, nothing else."""
    w = _ask(afternoon, statement)
    assert w["outcome"] == outcome
    nr = _column(w).get("no_result") or {}
    assert nr.get("reason") == reason
    if outcome in ("clarify", "refuse"):
        assert _rows(w) == [], f"{outcome} must return no values"
    else:
        assert _rows(w), "serve must return rows"


def test_the_script_gate_certifies_the_same_five_statements():
    """`scripts/afternoon_five.py` and this file must not drift apart.

    The script is what runs against the SHIPPED artifact after publication; this file is what runs in
    CI. If they ever certified different statements, the shipped-package gate would be attesting
    something CI never checked — so the statement list itself is the thing pinned.
    """
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    script = os.path.join(root, "scripts", "afternoon_five.py")
    if not os.path.exists(script):                       # installed-from-wheel tree: no repo scripts
        pytest.skip("scripts/afternoon_five.py is not present (running outside a source checkout)")
    text = open(script, encoding="utf-8").read()
    for statement, _, _ in FIVE:
        assert statement in text, f"the script gate no longer certifies: {statement}"
