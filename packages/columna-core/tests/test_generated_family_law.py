"""The generated-family law, certified against the Afternoon fixture.

RULING (Huayin, 2026-08-20). This file is the regression matrix for the correction that closed the
laundering class, and it supersedes ADR-020's inform-and-serve rule for structurally prohibited
reductions. The governing sentence:

    Family generation creates a new analytical family. It does NOT create a new operator permission.
    A successor family preserves the applicability law of its governed ancestry unless the
    family-changing operation POSITIVELY establishes a different successor law.

WHAT WAS WRONG. The old law walk modelled an expression's law as the law of its LEAF members, so
every reducer GENERATED above a leaf was invisible to it. `on_hand.sum` was caught and served with a
critical caveat; `sum(on_hand.last@day)` — the same prohibited temporal-stock-sum, one syntax away —
served CLEAN, with the identical meaningless number. Unary, binary, scalar, scan, DERIVED and
default-member spellings were all carriers for the same bypass, because in each of them the leaf
stayed lawful while the generated reducer did the prohibited travel.

WHY THE FIXTURE IS THE AFTERNOON. `specs/doctrine_gaps.md` DG-2 forward invariant 5 requires that the
system EXPRESS the Afternoon case: attempt a temporal SUM of a base stock, find no lawful reading,
REFUSE with the reason and the lawful neighbours. Until 2026-08-20 no fixture existed in this
repository to run that against, so the invariant could be asserted but not certified. `1410` is the
Afternoon's wrong number — the same units counted once per day they sat on the shelf — and the whole
point of the matrix is that no spelling covered by the laundering class can return it.

THIS FILE IS DG-2 INVARIANT 5's EVIDENCE, and its only evidence. Its sibling
`test_afternoon_page_gate.py` (with `scripts/afternoon_five.py`) certifies something different:
that the five executable statements *The Theory of Data in One Afternoon* v0.12 prints earn the
verdicts the essay claims. That gate certifies the ESSAY; this matrix certifies the LAW. Only one
of the essay's five is a laundering case, so neither file subsumes the other.
"""
import pytest

from columna_core.disclosure_wire import wire_frame

import afternoon_world as W          # tests/fixtures is on sys.path via conftest


# ── helpers ──────────────────────────────────────────────────────────────────────────────────────
def _wire(srv, anchor, expr, name="c"):
    return wire_frame(srv.frame(*anchor).column(name, expr).run())


def _col(srv, anchor, expr, name="c"):
    return _wire(srv, anchor, expr, name)["columns"][0]


def _verdict(srv, anchor, expr):
    """(outcome, reason) — the pair the reader actually receives."""
    w = _wire(srv, anchor, expr)
    return w["outcome"], (w["columns"][0].get("no_result") or {}).get("reason")


def _values(srv, anchor, expr, name="c"):
    """The served numbers. The wire keys each cell's measurement as `value`, alongside the anchor
    coordinates — so a test asserting on numbers reads `value`, not the column's own name."""
    return [v.get("value") for v in (_col(srv, anchor, expr, name).get("values") or [])]


def _s1_jan(srv, expr):
    vals = [v["value"] for v in _col(srv, ("store", "month"), expr)["values"]
            if v["store"] == "S1" and v["month"] == "2025-01"]
    assert len(vals) == 1, f"{expr}: expected exactly one S1/2025-01 cell, got {vals}"
    return vals[0]


# ══ DIRECT STRUCTURAL PROHIBITION ════════════════════════════════════════════════════════════════
def test_direct_blocked_member_refuses_with_no_values(afternoon_server):
    """The declared bar is now a REFUSAL, not a served caveat. Disclose exists inside the lawful
    region; it cannot legalize an operation the governed law does not possess."""
    col = _col(afternoon_server, ("store", "month"), "on_hand.sum")
    nr = col["no_result"]
    assert (nr["kind"], nr["reason"], nr["discriminator"]) == ("refuse", "blocked_reduction", "unsupported")
    assert "calendar" in nr["detail"]
    assert not col.get("values"), "a refused column carries no numbers — that is the whole point"
    assert not col.get("disclosures"), "nothing rides the disclosure channel for an unlawful ask"
    assert any(".last" in (a.get("description") or "") for a in nr["alternatives"]), \
        "a refusal must name the lawful neighbour (DG-2 invariant 5)"


# ══ INLINE LAUNDERING — the class this correction closes ═════════════════════════════════════════
_LAUNDERING = [
    # (id, expression) — every spelling of "sum a stock across calendar" the language admits
    ("declared-member",      "on_hand.sum"),
    ("inline-unmembered",    "sum(on_hand@day)"),          # L4: the member is never even named
    ("inline-lawful-kin",    "sum(on_hand.last@day)"),     # L1: leaf lawful, generated reducer is not
    ("inline-blocked-kin",   "sum(on_hand.sum@day)"),
    ("carrier-binary",       "sum(stock_pair@day)"),       # L2/L3: DERIVED over a binary MAP
    ("carrier-unary",        "sum((-on_hand.last)@day)"),
    ("carrier-scalar",       "sum((on_hand.last * 2)@day)"),
    ("carrier-scan",         "sum(cumsum(on_hand.last)@day)"),
    ("unpinned",             "sum(on_hand)"),              # L5: no lawful candidate survives
]


@pytest.mark.parametrize("case,expr", _LAUNDERING, ids=[c for c, _ in _LAUNDERING])
def test_every_laundering_spelling_refuses_identically(afternoon_server, case, expr):
    """One defect, not nine. Each row is a different SYNTAX for the same prohibited OPERATION, and a
    correction that closed some of them while leaving the others would be a spelling rule, not a law.
    They must land on the same verdict for the same reason."""
    assert _verdict(afternoon_server, ("store", "month"), expr) == ("refuse", "blocked_reduction")


@pytest.mark.parametrize("case,expr", _LAUNDERING, ids=[c for c, _ in _LAUNDERING])
def test_every_refusal_names_a_lawful_neighbour(afternoon_server, case, expr):
    """DG-2 forward invariant 5: refuse "with reason and lawful neighbours". A refusal that leaves the
    reader with nowhere to go is a wall, not governance — and a wall is what people route around."""
    nr = _col(afternoon_server, ("store", "month"), expr)["no_result"]
    alts = [a.get("description") or "" for a in (nr.get("alternatives") or [])]
    assert alts, f"{expr}: refused without naming a remedy"
    assert any(".last" in a for a in alts), \
        f"{expr}: the remedy must name the reducer that IS applicable, got {alts}"


@pytest.mark.parametrize("case,expr", _LAUNDERING, ids=[c for c, _ in _LAUNDERING])
def test_no_laundering_spelling_can_return_the_wrong_number(afternoon_server, case, expr):
    """The concrete negative witness. 1410 is not a quantity of anything — it is S1's January stock
    counted once per day it sat on the shelf. No spelling covered by the laundering class may return
    it. This assertion is deliberately about the NUMBER, not the mood: a future refactor that finds
    some new way to serve it would still be caught here."""
    assert W.S1_JAN_STOCK_SUM not in _values(afternoon_server, ("store", "month"), expr)


def test_carriers_do_not_alter_the_projected_law(afternoon_server):
    """DETERMINISM / EQUIVALENCE (ruling §1). A carrier transports an operation; it does not grant it
    authority, and it must not change the law the planner projects. Syntactically different but
    analytically equivalent spellings therefore earn byte-identical verdicts."""
    verdicts = {expr: _verdict(afternoon_server, ("store", "month"), expr)
                for _c, expr in _LAUNDERING}
    assert len(set(verdicts.values())) == 1, f"carriers changed the verdict: {verdicts}"


def test_the_law_is_stable_across_repeated_resolution(afternoon_server):
    """DETERMINISM (ruling §4). The applicability projection is derived from the expression plus the
    governed declarations — never from a value, a row count, a cache state or an execution path — so
    the same expression cannot acquire a different law on a second pass. Run each case twice, with a
    LAWFUL query interleaved to populate the engine cache in between."""
    for _c, expr in _LAUNDERING:
        first = _verdict(afternoon_server, ("store", "month"), expr)
        _values(afternoon_server, ("store", "month"), "on_hand.last")     # warm the cache
        assert _verdict(afternoon_server, ("store", "month"), expr) == first


# ══ UNPINNED: the |L| trichotomy (ruling §9) ═════════════════════════════════════════════════════
def test_unpinned_with_no_lawful_candidate_refuses(afternoon_server):
    """|L| = 0. Never offer a candidate that is already structurally illegal: a clarify is a menu of
    readings the asker may choose between, and an unlawful reading is not a choice. Offering it would
    make Clarify reachable before lawfulness — which is how a reader gets talked into a laundered
    answer one keystroke later."""
    col = _col(afternoon_server, ("store", "month"), "sum(on_hand)")
    nr = col["no_result"]
    assert (nr["kind"], nr["reason"]) == ("refuse", "blocked_reduction")
    assert not any("pin the input anchor" in (a.get("description") or "") for a in nr["alternatives"]), \
        "an unlawful pin must never be offered as a remedy"


def test_unpinned_with_one_lawful_candidate_defaults_and_discloses(afternoon_server):
    """|L| = 1. Nothing is contested, so there is no choice to put to the reader — but the reader did
    not make this choice either, so the defaulted anchor rides as a MATERIAL caveat. Disclosed, never
    silent."""
    w = _wire(afternoon_server, ("store", "month"), "avg(on_hand.last@day)")
    assert w["outcome"] == "serve"                       # explicitly pinned: no default was taken
    w2 = _wire(afternoon_server, ("store", "month"), "avg(on_hand.last)")
    assert w2["outcome"] == "disclose"
    codes = {(d["code"], d["materiality"]) for d in w2["columns"][0]["disclosures"]}
    assert ("input_anchor", "material") in codes
    assert _s1_jan(afternoon_server, "avg(on_hand.last)") == W.S1_JAN_MEAN, \
        "the defaulted reading must be the same number the explicit pin gives"


# ══ AXIS-SPECIFIC LAW — the bar names a LINEAGE, not a measure ═══════════════════════════════════
def test_summing_a_stock_across_stores_is_lawful(afternoon_server):
    """The same reducer, the same measure, the opposite verdict — decided by the AXIS. This is what
    it means for applicability to be per operator x lineage (ADR-031 D5), and it is why the fix could
    not be a stock/flow type: a type would have killed this lawful reading too."""
    w = _wire(afternoon_server, ("month",), "sum(on_hand.last@store)")
    assert w["outcome"] == "serve"
    jan = [v["value"] for v in w["columns"][0]["values"] if v["month"] == "2025-01"]
    assert jan == [W.JAN_POSITION_ACROSS_STORES]


@pytest.mark.parametrize("reducer,expected", [
    ("avg",   W.S1_JAN_MEAN),
    ("max",   W.S1_JAN_MAX),
    ("min",   W.S1_JAN_MIN),
    ("count", W.S1_JAN_DAYS),
])
def test_other_reducers_over_the_stock_remain_lawful(afternoon_server, reducer, expected):
    """Ruling §6: do NOT infer a global stock personality. The author barred `sum` along `calendar`
    and barred nothing else. Averaging, extremising and counting a position over time stay lawful and
    keep their shipped numbers — the correction tightens exactly one thing, and a change that also
    swept these up would be the type system D5 forbids, arriving by the back door."""
    expr = f"{reducer}(on_hand.last@day)"
    assert _verdict(afternoon_server, ("store", "month"), expr)[0] == "serve"
    assert _s1_jan(afternoon_server, expr) == expected


# ══ LAWFUL FAMILY GENERATION — the correction must not be a blanket ban ═════════════════════════
def test_the_lawful_neighbour_still_serves(afternoon_server):
    """The remedy the refusal names must actually work. A refusal that leaves the reader with nowhere
    to go is a wall, not governance."""
    assert _verdict(afternoon_server, ("store", "month"), "on_hand.last")[0] == "serve"
    assert _s1_jan(afternoon_server, "on_hand.last") == W.S1_JAN_POSITION


def test_a_flow_sums_lawfully_at_coarser_anchors(afternoon_server):
    """The control. `revenue` declares no bar, so it adds along every axis — as it always did."""
    assert _verdict(afternoon_server, ("store", "month"), "revenue")[0] == "serve"
    assert _s1_jan(afternoon_server, "revenue") == W.S1_JAN_REVENUE


@pytest.mark.parametrize("anchor,expr", [
    (("region", "month"), "avg(revenue@order)"),   # the generating reducer establishes a new family
    (("month",),          "sum(revenue@day)"),
    (("region",),         "sum(revenue@store)"),
])
def test_lawful_family_generation_serves(afternoon_server, anchor, expr):
    """Generation itself is not the offence. A generated family whose governed ancestry declares no
    bar on the generating operator serves exactly as before — the law is about PERMISSION, not about
    whether a family was generated."""
    assert _verdict(afternoon_server, anchor, expr)[0] == "serve"


def test_mean_has_a_law_address_without_becoming_a_monoid(afternoon_server):
    """Ruling §4. `avg` is the surface spelling; `mean` is the canonical governed operator — ONE law
    subject, so there is exactly one thing an author would declare. Registering it gives the inline
    average a governable `(operator x lineage)` address; it must NOT imply that displayed averages
    combine associatively."""
    from columna_core.operators import ALIASES, REGISTRY, SERIES_REDUCERS, canonical

    assert canonical("avg") == "mean" and ALIASES["avg"] == "mean"
    assert "avg" not in REGISTRY, "one canonical operator, several spellings — not two operators"
    assert REGISTRY["mean"].kind == "reducer"
    assert REGISTRY["mean"].is_monoid is False, "mean-of-means is not a mean"
    # sorted: the frame's row order is not part of the contract, the numbers are
    assert sorted(_values(afternoon_server, ("store", "month"), "avg(on_hand.last@day)")) == \
           sorted(_values(afternoon_server, ("store", "month"), "mean(on_hand.last@day)"))

    from columna_core.engine import ColumnEngine
    assert set(ColumnEngine._SERIES_REDUCE) == set(SERIES_REDUCERS), \
        "the EXECUTABLE and GOVERNABLE reducer vocabularies must not drift — that drift is how " \
        "`mean` came to have no law slot at all"


# ══ VOCABULARY INTEGRITY (ruling §7) ═════════════════════════════════════════════════════════════
def test_the_reason_registry_is_closed_and_fails_closed():
    """An unregistered reason used to acquire ERROR from a silent `.get` default. That is not
    hypothetical — `chained_crossing` and `anchor_spent` both shipped that way, classified ERROR when
    their call sites plainly mean REFUSE. A vocabulary that grows by rule and shrinks by tombstone
    cannot also grow by accident."""
    from columna_core.disclosure import (REASON_OUTCOME, REFUSE, UNSUPPORTED,
                                         UnregisteredReason, outcome_for)

    assert REASON_OUTCOME["blocked_reduction"] == (REFUSE, UNSUPPORTED)
    assert REASON_OUTCOME["chained_crossing"] == (REFUSE, UNSUPPORTED)
    assert REASON_OUTCOME["anchor_spent"] == (REFUSE, UNSUPPORTED)
    with pytest.raises(UnregisteredReason):
        outcome_for("a_reason_nobody_registered")


def test_the_b_anchor_caveat_is_tombstoned_not_deleted(afternoon_server):
    """Vocabularies shrink by tombstone. The category stays wired so archived wires, recorded
    transcripts and the deposited manuals still resolve — but nothing produces it any more."""
    from columna_core.disclosure_wire import CATEGORY_TABLE, code_for

    assert code_for("b_anchor_crossing") == "blocked_reduction"      # still resolvable
    assert "b_anchor_crossing" in CATEGORY_TABLE
    for _c, expr in _LAUNDERING:
        col = _col(afternoon_server, ("store", "month"), expr)
        assert not [d for d in (col.get("disclosures") or [])
                    if d.get("category") == "b_anchor_crossing"], \
            f"{expr}: the retired caveat was produced afresh"


def test_the_wire_contract_did_not_move():
    """Ruling §7: `no_result.reason` is an extensible reason string in shape, so a new reason on the
    refusal channel is additive. This is an INTERNAL vocabulary correction, not a wire break."""
    from columna_core.disclosure_wire import CONTRACT_VERSION

    assert CONTRACT_VERSION == "3"


# ══ PLAN PREDICTS WHAT RUN DOES ══════════════════════════════════════════════════════════════════
@pytest.mark.parametrize("case,expr", _LAUNDERING, ids=[c for c, _ in _LAUNDERING])
def test_explain_predicts_the_refusal_without_touching_data(afternoon_server, case, expr):
    """The promise EXPLAIN makes is that the would-be annotation IS the annotation. A structural
    refusal is knowable at compile time — it reads declarations and shape, never a value — so an
    agent must be able to see it before spending a scan."""
    before = afternoon_server.engine.con.fetch_count
    planned = afternoon_server.planner.plan(("store", "month"), [("c", expr)])
    assert afternoon_server.engine.con.fetch_count == before, "EXPLAIN must touch no data"
    assert wire_frame(planned)["outcome"] == "refuse"
    assert _verdict(afternoon_server, ("store", "month"), expr)[0] == "refuse"
