"""P1-25 — a refusal saying "there is no pin that rescues this ask" must be TRUE.

`_pin_verdicts` enumerated candidate pins through `_admit_pin` and caught `Refusal`, one class
carrying every jurisdiction. So it could not tell

    "this LEVEL is unlawful"                    — a verdict about the candidate
    "this ASK never became adjudicable"         — a fact about the expression, identical under every pin

apart, and recorded both as verdicts. `max(level) AT {store}` therefore refused:

    every candidate grain is excluded ... category (unknown), customer (unknown), date (unknown),
    day (unknown), ... region (pin_coarser_than_output). Each verdict is the one the pin would earn
    if it were written out, so there is no pin that rescues this ask.

Eight of the nine "verdicts" were the family-member question. Three pins rescue the ask and one
serves. The refusal's central sentence was false.

The repair is structural: a refusal raised by the expression check inside `_admit_pin` is staged as
an `_ExpressionFault` rather than recorded as a candidate's verdict, so the incorrect state is not
representable. What may then be CLAIMED is decided by asking, not by tallying — see
`_any_member_has_a_lawful_pin`.
"""
import pytest

from columna_core.disclosure import ANALYTICAL, CLARIFY, jurisdiction_for
from columna_core.disclosure_wire import wire_frame
from columna_core.envelope import parse_statement


@pytest.fixture(scope="module")
def srv():
    import sys, os
    sys.path.insert(0, os.path.join(os.getcwd(), "docs", "tools"))
    from manual_fixtures import harness
    return harness.servers()["finance_manifold"]


def _w(srv, q):
    w = wire_frame(srv.planner.run_statement(parse_statement(q)), executed=True)
    nr = next((c.get("no_result") for c in w.get("columns", []) if c.get("no_result")), None)
    return w["outcome"], (nr or {}).get("reason"), nr


# ── the false refusal, and the fact that falsified it ─────────────────────────────────────────────
def test_the_ask_that_used_to_refuse_falsely_now_names_the_real_obstacle(srv):
    outcome, reason, nr = _w(srv, "SELECT max(level) AS s AT {store}")
    assert (outcome, reason) == (CLARIFY, "family_member_ambiguous")
    assert "no pin that rescues" not in (nr["detail"] or "")


def test_and_the_claim_it_used_to_make_is_demonstrably_false(srv):
    """The one-line refutation, kept in the suite so the row cannot be re-broken quietly: naming the
    member and pinning the anchor SERVES, so "there is no pin that rescues this ask" was never true
    of this ask."""
    assert _w(srv, "SELECT max(level.max @ {day}) AS s AT {store}")[0] == "serve"


def test_a_family_question_is_never_reported_as_a_verdict_about_a_level(srv):
    """THE INVARIANT. Whatever the disposition, no refusal may attribute the family question to a
    candidate pin — that is the specific manufacture of evidence this row is about."""
    for q in ["SELECT max(level) AS s AT {store}",
              "SELECT sum(level) AS s AT {region}",
              "SELECT max(level) AS s AT {customer}"]:
        _o, _r, nr = _w(srv, q)
        detail = (nr or {}).get("detail") or ""
        assert "(unknown)" not in detail, (q, detail)


# ── the family question itself is now adjudicated, not filed as a vocabulary miss ─────────────────
def test_several_lawful_members_clarify_and_offer_every_one_unranked(srv):
    """v0.2 §12. The measure is known and the ask is well formed; what is under-determined is which
    lawful reduction is meant. §12 also forbids realization from picking one, so every member is
    offered and none is preferred."""
    outcome, reason, nr = _w(srv, "SELECT sum(level) AS s AT {region}")
    assert (outcome, reason) == (CLARIFY, "family_member_ambiguous")
    assert jurisdiction_for(reason) == ANALYTICAL
    tokens = [a["token"] for a in nr["alternatives"]]
    # `level.sum` JOINS THE MENU AND SHOULD NOT BE ON IT — see the xfail below. The list is asserted
    # as OBSERVED, not as ratified: `sum` is declared BLOCKED along the calendar, so `level.sum` at
    # {region} refuses, and offering it makes this clarify a menu with an unlawful item on it. The
    # membership is pinned here so the defect cannot change shape unnoticed while it awaits a ruling.
    assert tokens == ["level.last", "level.sum", "level.max", "level.min", "level.count"], tokens


def test_every_offered_member_is_a_real_member(srv):
    _o, _r, nr = _w(srv, "SELECT sum(level) AS s AT {region}")
    members = set(srv.planner.m.measures["level"].family)
    assert {a["token"].split(".", 1)[1] for a in nr["alternatives"]} == members


# ── the ratified precedence survives: an invariant prohibition still outranks the ambiguity ───────
def test_a_prohibition_that_holds_under_every_member_still_outranks_the_ambiguity(afternoon_server):
    """generated-family ruling §1, ratified: `sum(on_hand)` @ {store, month} must refuse the barred
    temporal sum, NOT ask which member was meant — because no member rescues it. This is the case
    that makes the repair a question rather than a rule: the family IS ambiguous here too, and the
    answer is still the prohibition."""
    w = wire_frame(afternoon_server.frame("store", "month").column("c", "sum(on_hand)").run())
    nr = w["columns"][0]["no_result"]
    assert (nr["kind"], nr["reason"]) == ("refuse", "blocked_reduction")


def test_the_two_cases_differ_only_in_whether_naming_a_member_would_help(srv, afternoon_server):
    """Stated as one assertion because it is the whole rule: the ambiguity wins where a member
    rescues the ask, the prohibition wins where none does."""
    assert _w(srv, "SELECT max(level.max @ {day}) AS s AT {store}")[0] == "serve"      # a member helps
    for m in afternoon_server.m.measures["on_hand"].family:                            # none helps
        w = wire_frame(afternoon_server.frame("store", "month").column("c", f"sum(on_hand.{m})").run())
        assert w["outcome"] in ("refuse", "error", "clarify"), (m, w["outcome"])


@pytest.mark.xfail(strict=True, reason="UNRATIFIED — awaiting a ruling. The family-member clarify "
                                       "menu is not filtered for lawfulness; the input-anchor menu "
                                       "is (ruling 2026-08-20 §9). Same law, one menu.")
def test_the_family_member_menu_offers_only_lawful_readings(srv):
    """A clarify is a menu of readings you may choose between, so every item on it must serve.

    §2.3 states this for the input-anchor menu and the Afternoon gate tests it there
    (`test_beat_4` walks every offered pin and asserts it serves). The family-member menu makes the
    same promise and does not keep it: `SELECT sum(level) AT {region}` offers `level.sum`, and
    `SELECT level.sum AT {region}` refuses `blocked_reduction`, because `sum` is declared BLOCKED
    along the calendar and reducing inventory to region collapses the day axis.

    Invisible until 2026-09-02, when a fixture first declared a BLOCKED lineage at all."""
    _outcome, _reason, nr = _w(srv, "SELECT sum(level) AS s AT {region}")
    for token in [a["token"] for a in nr["alternatives"]]:
        out, _r, _nr = _w(srv, f"SELECT {token} AS s AT {{region}}")
        assert out in ("serve", "disclose"), f"the menu offers an unlawful reading: {token}"
