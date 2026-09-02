"""P1-13 — explicit pin validation and candidate-pin enumeration are ONE law.

THE GOVERNING INVARIANT (ruled Huayin, 2026-08-31):

    Explicit pin validation and candidate-pin enumeration must use the same canonical
    admissibility law.

They had drifted. `_pin_input_grain` (execution) implemented WP-GRAIN-1 — a pin need not REACH the
output anchor, because the anchor's orthogonal levels join the input grain — while `_lawful_pins`
(enumeration) still applied the pre-WP-GRAIN-1 test that the pin must reach it. So an unpinned
reduction REFUSED "this ask has no reading to serve" at an anchor where six explicit pins served: a
confident wrong disposition, and the same shape as the Mission B A1 defect (a generalization landed
in one dispatcher and not in the sibling that has to agree with it).

The repair is NOT "delete the reachability filter". It replaces that filter with the law it
contradicted, and adds the §2c universe filter the enumeration never had — both already ratified —
by routing BOTH paths through one predicate, `_admit_pin`. The tests below are written against the
INVARIANT rather than against a candidate count, because a count is what went stale last time.
"""
import ast
import re

import duckdb
import pytest

from columna_core import ManifoldServer
from columna_core.connector import DuckDBConnector
from columna_core.disclosure_wire import wire_frame
from columna_core.parser import parse_manifold

# `region` is reached from `customer`; `day` reaches NEITHER output level and is the WP-GRAIN-1 case.
# `warehouse` is the §2c case, and it is built to be a HARD one: it REACHES `region` through its own
# hierarchy, so it passes the structural test and both pin-lattice laws, and is excluded only by the
# universe filter. A `warehouse` that reached nothing would have been dropped by the superseded rule
# too, and the test would prove nothing.
_CML = """
MANIFOLD w VERSION 1
UNIVERSE sales     = customer * day BASIS events
UNIVERSE inventory = warehouse * day BASIS spine
LEVEL customer  = customer_id  BASE
LEVEL day       = day          BASE
LEVEL warehouse = warehouse_id BASE
LEVEL region    = region
HIERARCHY geo   { customer  -> region VIA customers(customer_id, region) }
HIERARCHY whgeo { warehouse -> region VIA warehouses(warehouse_id, region) }
MEASURE revenue ON sales     FROM txns AS sum(amount)
MEASURE orders  ON sales     FROM txns AS count(*)
MEASURE stock   ON inventory FROM inv  VALUE units FAMILY { last ORDER day }
DERIVED aov = revenue / orders
"""


@pytest.fixture(scope="module")
def srv():
    con = duckdb.connect()
    con.execute("CREATE TABLE customers (customer_id VARCHAR, region VARCHAR)")
    con.executemany("INSERT INTO customers VALUES (?, ?)", [("C1", "east"), ("C2", "west")])
    con.execute("CREATE TABLE txns (customer_id VARCHAR, day VARCHAR, amount DOUBLE)")
    con.executemany("INSERT INTO txns VALUES (?, ?, ?)",
                    [("C1", "2024-01-05", 120.0), ("C1", "2024-02-02", 80.0), ("C2", "2024-02-02", 200.0)])
    con.execute("CREATE TABLE warehouses (warehouse_id VARCHAR, region VARCHAR)")
    con.executemany("INSERT INTO warehouses VALUES (?, ?)", [("W1", "east"), ("W2", "west")])
    con.execute("CREATE TABLE inv (warehouse_id VARCHAR, day VARCHAR, units BIGINT)")
    con.executemany("INSERT INTO inv VALUES (?, ?, ?)",
                    [("W1", "2024-01-05", 10), ("W1", "2024-02-02", 12), ("W2", "2024-02-02", 5)])
    s = ManifoldServer(parse_manifold(_CML), connector=DuckDBConnector(con))
    s.publish()
    return s


def _plan(srv, anchor, expr):
    return wire_frame(srv.planner.plan(anchor, [("c", expr)]), executed=False)


def _run(srv, anchor, expr):
    return wire_frame(srv.planner.run(anchor, [("c", expr)]))


def _menu(w):
    """The candidate LEVELS a clarify offers, read out of its own alternatives."""
    nr = w["columns"][0].get("no_result") or {}
    return sorted(m.group(1) for a in (nr.get("alternatives") or [])
                  if (m := re.search(r"to '([\w.]+)'", a.get("description") or "")))


def _reason(w):
    return next((c["no_result"]["reason"] for c in w["columns"] if c.get("no_result")), None)


# ── the invariant itself ────────────────────────────────────────────────────────────────────────
def test_one_predicate_adjudicates_both_paths(srv):
    """STRUCTURAL, not behavioural. The two paths cannot drift again only if there is one law to
    drift from, so this asserts the shape of the code and not a sampled agreement: `_admit_pin` is
    what the explicit path calls and what the enumeration filters through.

    A behavioural spot-check would pass under two implementations that happen to agree today, which
    is exactly the state P1-13 was found in."""
    import inspect

    from columna_core.planner import Planner

    assert "_admit_pin" in inspect.getsource(Planner._infer)          # the explicit pin
    assert "_admit_pin" in inspect.getsource(Planner._pin_verdicts)   # every enumerated candidate
    # and the superseded rule is gone: enumeration no longer asks whether a pin REACHES the anchor.
    assert "find_path" not in inspect.getsource(Planner._pin_candidates)


def test_every_offered_candidate_survives_the_explicit_pin_law(srv):
    """THE INVARIANT, checked over the whole ask surface rather than on one witness. Whatever the
    menu contains, naming it must not be refused — a clarify is a menu of readings the asker may
    choose between, and an unlawful reading is not a choice."""
    checked = 0
    for expr in ("sum(revenue)", "avg(aov)", "max(revenue)", "sum(stock.last)"):
        for anchor in (("customer",), ("region",), ("day",), ("region", "day"), ("customer", "day")):
            w = _plan(srv, anchor, expr)
            if _reason(w) != "input_anchor_ambiguous":
                continue
            for L in _menu(w):
                red, inner = expr.split("(", 1)
                named = _plan(srv, anchor, f"{red}({inner.rsplit(')', 1)[0]}@{L})")
                assert named["outcome"] in ("serve", "disclose"), \
                    f"{expr} AT {anchor} offered '{L}', which the planner then refuses"
                checked += 1
    assert checked, "the sweep must actually exercise some menus"


# ── WP-GRAIN-1: a pin need not reach the output anchor ──────────────────────────────────────────
def test_a_pin_that_reaches_no_output_level_is_a_lawful_reading(srv):
    """THE P1-13 DEFECT ITSELF. `day` reaches neither `customer` nor anything above it, so the
    superseded enumeration dropped it and the ask refused "no lawful reading". WP-GRAIN-1 joins the
    anchor's orthogonal levels into the input grain, so `avg(aov @ {day}) AT {customer}` resolves at
    `(day, customer)` — which is why naming the pin has always served. Enumeration now agrees."""
    served = _run(srv, ("customer",), "avg(aov@day)")
    assert served["outcome"] in ("serve", "disclose")            # the pin serves, and always did
    w = _plan(srv, ("customer",), "avg(aov)")
    assert w["outcome"] != "refuse", "the unpinned form must not refuse where an explicit pin serves"
    assert w["outcome"] == "disclose"                  # `day` is the ONE lawful reading, so it defaults
    assert srv.planner._lawful_pins("mean", ast.parse("aov", mode="eval").body, ("customer",)) == ["day"]


# ── §2c: candidates must remain inside the resolved universe ────────────────────────────────────
def test_an_out_of_universe_candidate_is_never_offered(srv):
    """The filter the enumeration never had. `warehouse` is a declared level, and it is NOT in
    `revenue`'s universe — naming it REFUSES `out_of_universe`. Before the repair, enumeration
    applied only the pin-lattice and lineage laws, so on the Manual fixture `sum(revenue) AT {region}`
    offered `store` and the reader could pick a reading that refuses on the next keystroke."""
    # `warehouse` REACHES `region`, so the superseded enumeration kept it — this is the observed
    # `store` case, reproduced.
    assert srv.planner.m.find_path({"warehouse"}, "region") is not None
    named = _plan(srv, ("region",), "sum(revenue@warehouse)")
    assert named["outcome"] == "refuse" and _reason(named) == "out_of_universe"
    for anchor in (("region",), ("customer",), ("day",)):
        assert "warehouse" not in _menu(_plan(srv, anchor, "sum(revenue)"))


# ── the 0 / 1 / >1 disposition law is untouched ─────────────────────────────────────────────────
def test_the_disposition_trichotomy_is_unchanged(srv):
    """§9 is not what was wrong: |L| = 1 defaults and discloses, |L| > 1 clarifies, |L| = 0 refuses.
    The repair corrected L, not the rule applied to it.

    THE RULE NOW COUNTS READINGS, NOT SPELLINGS (ruled Huayin, 2026-09-01), so this carries the
    trichotomy on an UNCERTIFIED capability. `max` is deliberate: its lawful set here is identical to
    `sum`'s, so the only thing that differs is the re-entry certification — which is exactly the
    variable under test. `sum` collapsing is asserted separately, below."""
    from columna_core.planner import Planner

    pl = srv.planner
    lawful = {a: pl._lawful_pins("max", ast.parse("revenue", mode="eval").body, a)
              for a in (("region",), ("customer",), ("customer", "day"))}
    assert len(lawful[("customer", "day")]) == 0                  # nothing left to pin
    assert len(lawful[("region",)]) > 1                           # a real menu
    assert _plan(srv, ("region",), "max(revenue)")["outcome"] == "clarify"
    assert isinstance(Planner._lawful_pins(pl, "max", ast.parse("revenue", mode="eval").body, ("region",)), list)


def test_a_single_lawful_reading_defaults_and_discloses(srv):
    """|L| = 1 PROCEEDS: one reading is not a contested choice. The defaulting is a decision the
    READER did not make, so it rides as a MATERIAL `input_anchor` caveat — never a silent serve.

    Deliberately the WP-GRAIN-1 anchor: at `{customer}` the single lawful reading is `day`, which
    reaches nothing in the anchor. The superseded enumeration found ZERO here and REFUSED, so this
    test carries the |L| = 1 rule and the P1-13 correction on the same witness."""
    w = _run(srv, ("customer",), "sum(revenue)")
    assert w["outcome"] == "disclose"
    codes = {(d["code"], d["materiality"]) for d in (w["columns"][0].get("disclosures") or [])}
    assert ("input_anchor", "material") in codes
    detail = next(d["detail"] for d in w["columns"][0]["disclosures"] if d["code"] == "input_anchor")
    assert "DEFAULTED to 'day'" in detail


# ── a refusal every candidate earns is not ABOUT any candidate ──────────────────────────────────
def test_a_unanimous_refusal_is_re_raised_rather_than_generalized(srv):
    """|L| = 0 where the whole set fails for ONE reason. That reason is a property of the ASK — here
    the OUTPUT anchor, which sits in every candidate's input grain — so the precise diagnosis is
    re-raised instead of being replaced by "no lawful input anchor". Trading a true answer for a
    vaguer one is the same class of loss P1-14 was about."""
    named = _plan(srv, ("region", "warehouse"), "sum(revenue@day)")
    w = _plan(srv, ("region", "warehouse"), "sum(revenue)")
    assert _reason(named) == "out_of_universe"          # `warehouse` is in the OUTPUT, under every pin
    assert _reason(w) == _reason(named), "the unpinned form must say what the pinned form says"


def test_a_mixed_refusal_reports_the_verdicts_instead_of_asserting_a_cause(srv):
    """|L| = 0 where the candidates DISAGREE about why. The detail used to state that every candidate
    "would reduce across a lineage the governed law blocks for it" — true when the lineage law was
    the only filter, and false once §2c and transport joined it. A refusal that names the wrong cause
    sends the reader to fix the wrong thing.

    THE REASON MOVED TOO (ruled Huayin, 2026-09-02). This case used to report `blocked_reduction`,
    so the detail told the truth while the reason it travelled under did not: no lineage is blocked
    here, the candidates simply all failed adjudication for reasons that disagree. That is
    `input_anchor_unavailable` — §2.3's |R| = 0 branch, sibling to `input_anchor_ambiguous`.
    `blocked_reduction` now names only the condition it describes: a governed BLOCKED lineage."""
    w = _plan(srv, ("customer", "day"), "sum(revenue)")
    assert w["outcome"] == "refuse" and _reason(w) == "input_anchor_unavailable"
    detail = w["columns"][0]["no_result"]["detail"]
    assert "no lawful input anchor" in detail
    assert w["columns"][0]["no_result"].get("alternatives"), \
        "a refusal owes the reader a lawful neighbour (DG-2 invariant 5)"


# ── no ranking, no heuristic, no hidden pruning ─────────────────────────────────────────────────
def test_the_menu_is_the_lawful_set_in_level_order(srv):
    """Ruled explicitly (Huayin, 2026-08-31): the repair returns the lawful set and applies the
    unchanged 0/1/>1 rule to it. Whether a long menu is the right ERGONOMICS is a separate design
    question; answering it here would mean the framework quietly choosing among lawful readings,
    which is the thing the Clarify exists to refuse to do."""
    w = _plan(srv, ("region",), "max(revenue)")
    menu = _menu(w)
    assert menu == sorted(menu) and len(menu) == len(set(menu))
    assert menu == srv.planner._lawful_pins("max", ast.parse("revenue", mode="eval").body, ("region",))


# ── re-entry certification: several lawful spellings, one analytical reading ─────────────────────
def test_certified_re_entry_collapses_lawful_anchors_to_one_reading(srv):
    """Ruled (Huayin, 2026-09-01): candidate anchors proven equivalent under governed analytical law
    are ONE reading, so the 0/1/many rule counts readings rather than raw candidates.

    `sum` carries `re_entrant=True` — finalizing at a lawful intermediate partition and re-applying
    denotes the same result. Two lawful pins therefore collapse and the ask SERVES where it used to
    offer a menu. And because no analytical choice was made, NO material input-anchor disclosure is
    owed: realization merely picked a representative."""
    lawful = srv.planner._lawful_pins("sum", ast.parse("revenue", mode="eval").body, ("region",))
    assert len(lawful) > 1, "the collapse is only meaningful with a real menu behind it"

    w = _run(srv, ("region",), "sum(revenue)")
    assert w["outcome"] in ("serve", "disclose"), "certified re-entry must not clarify"
    codes = {(d["code"], d.get("materiality")) for d in (w["columns"][0].get("disclosures") or [])}
    assert ("input_anchor", "material") not in codes, \
        "no meaning-bearing choice was made, so no MATERIAL input-anchor caveat is owed"


def test_uncertified_capabilities_still_clarify(srv):
    """The certification is a DECLARATION, not an algebraic guess. `max` is idempotent and `count`
    combines additively — both would pass a plausibility test, and both stay uncertified because no
    governed contract establishes re-entry for them. Undeclared means Clarify."""
    for reducer in ("max", "count", "mean"):
        w = _plan(srv, ("region",), f"{reducer}(revenue)")
        assert w["outcome"] == "clarify", f"{reducer} is uncertified and must still clarify"


def test_the_collapse_requires_the_SAME_continuation(srv):
    """The law quantifies over ONE kappa: re-entry through the *same* continuation. `sum(revenue)`
    collapses because revenue's family member IS `sum`, so inner delivery and outer reduction are
    the same capability. `max(revenue)` must not borrow that certification: revenue's family is
    (sum), so the inner delivers SUMS and the outer takes a max OF SUMS — a different analytical
    object at each candidate grain."""
    pl = srv.planner
    inner = ast.parse("revenue", mode="eval").body
    assert pl._re_entrant("sum", inner) is True
    assert pl._re_entrant("max", inner) is False, \
        "max must not inherit sum's certification just because sum delivers its input"
