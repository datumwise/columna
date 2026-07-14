"""
test_inline_reduction.py — WP-B.1: inline reduction of a derivation (capture v0.8; ruling (A)).

Closes doctrine-gap DG-1. Two forms of `R(inner)` in a column expression:

  * PINNED   `avg(aov@day) @ month` — the input anchor is pinned; a definite quantity, served with an
              IMMATERIAL communicative disclosure naming the reading. Identical to the DECLARED
              AT-metric (`daily_aov`) — same reading, two spellings; never the pooled value.
  * UNPINNED `avg(aov) @ month`     — the input anchor is structurally underdetermined ⇒ an engine
              clarify enumerating candidate input anchors, choosing none.

input_anchor-fit finding (owed to CP-B2, pinned here): an EXPLICITLY user-pinned input anchor is a
deliberate, visible choice, so it owes a communicative note (immaterial `provenance`), NOT the
material `input_anchor` caveat. Fork surfaced to Huayin (reason-code reuse; caveat materiality).

Fixtures (`fixture_connector`) come from tests/conftest.py.
"""
import os

import pytest

from columna_core import ManifoldServer
from columna_core.disclosure_wire import wire_frame
from columna_core.parser import parse_manifold

_HERE = os.path.dirname(os.path.abspath(__file__))
_BENCHMARK_CML = os.path.join(_HERE, "fixtures", "benchmark.cml")

_DEFS = ("DERIVED aov = revenue / orders\n"
         "DERIVED daily_aov = revenue / orders AT day\n"
         "    FAMILY {\n        mean FERTILE { }\n    }\n")


def _srv(fixture_connector):
    with open(_BENCHMARK_CML) as f:
        return ManifoldServer(parse_manifold(f.read() + "\n" + _DEFS), fixture_connector)


def _vals(srv, anchor, expr):
    return srv.frame(anchor).column("c", expr).run().data.sort(anchor)["c"].to_list()


# ── PINNED: legal, definite, communicative-disclosed ────────────────────────────────────────
def test_pinned_inline_reduction_serves_with_immaterial_note(fixture_connector):
    s = _srv(fixture_connector)
    w = wire_frame(s.frame("cal.month").column("x", "avg(aov@day)").run())
    assert w["outcome"] == "serve"
    discs = w["columns"][0].get("disclosures") or []
    assert [(d["code"], d["materiality"]) for d in discs] == [("provenance", "immaterial")], \
        "a user-pinned input anchor owes a communicative note (immaterial provenance), not a material caveat"


def test_pinned_inline_equals_declared_at_metric(fixture_connector):
    """The inline pinned reduction is the SAME reading as the declared AT-metric — two spellings of
    'mean of the day-resolved series'."""
    s = _srv(fixture_connector)
    inline = _vals(s, "cal.month", "avg(aov@day)")
    declared = _vals(s, "cal.month", "daily_aov")
    assert inline == pytest.approx(declared)


def test_pinned_inline_is_never_the_pooled_value(fixture_connector):
    """never-substitute: the pinned reading ≠ the pooled `aov@month`."""
    s = _srv(fixture_connector)
    assert _vals(s, "cal.month", "avg(aov@day)") != pytest.approx(_vals(s, "cal.month", "aov"))


def test_pinned_at_its_own_anchor_is_the_denotation(fixture_connector):
    """`avg(aov@day) @ day` — asked AT the pinned anchor, no travel: the day denotation itself."""
    s = _srv(fixture_connector)
    assert _vals(s, "day", "avg(aov@day)") == pytest.approx(_vals(s, "day", "aov"))


def test_avg_is_mean_alias(fixture_connector):
    s = _srv(fixture_connector)
    assert _vals(s, "cal.month", "avg(aov@day)") == pytest.approx(_vals(s, "cal.month", "mean(aov@day)"))


@pytest.mark.parametrize("reducer", ["sum", "min", "max", "mean"])
def test_pinned_reducers_serve(fixture_connector, reducer):
    """Each inline reducer resolves the pinned series and collapses it to the frame anchor."""
    s = _srv(fixture_connector)
    w = wire_frame(s.frame("cal.month").column("c", f"{reducer}(aov@day)").run())
    assert w["outcome"] == "serve"


# ── UNPINNED: engine clarify enumerating candidate input anchors ────────────────────────────
def test_unpinned_inline_reduction_clarifies(fixture_connector):
    s = _srv(fixture_connector)
    fr = s.frame("cal.month").column("y", "avg(aov)").run()
    w = wire_frame(fr)
    assert w["outcome"] == "clarify"
    nr = w["columns"][0].get("no_result") or {}
    # OF-1 ruling: its own reason `input_anchor_ambiguous` (one reason per contested dimension),
    # NOT a reuse of `ambiguous_grain`.
    assert nr.get("reason") == "input_anchor_ambiguous" and nr.get("discriminator") == "ambiguous"
    # candidate input anchors are enumerated (only `day` rolls up to cal.month in this fixture),
    # and the clarify chooses none.
    alts = nr.get("alternatives") or []
    assert alts, "unpinned reduction must enumerate candidate input anchors"
    assert any("day" in (a.get("description") or "") for a in alts)


def test_unpinned_names_a_pinnable_fix(fixture_connector):
    """The clarify's detail points the user at the pin that resolves it."""
    s = _srv(fixture_connector)
    fr = s.frame("cal.month").column("y", "mean(aov)").run()
    detail = (wire_frame(fr)["columns"][0].get("no_result") or {}).get("detail") or ""
    assert "@day" in detail and "does not pin" in detail


# ── OF-1: the minted reason lives in the closed vocabulary, distinct from ambiguous_grain ───
def test_input_anchor_ambiguous_is_a_distinct_clarify_reason():
    """OF-1 ruling: `input_anchor_ambiguous` is its OWN reason (CLARIFY/AMBIGUOUS), sibling to
    `co_anchor_ambiguous` — not a reuse of `ambiguous_grain`, whose gloss stays single-meaning."""
    from columna_core.disclosure import REASON_OUTCOME, CLARIFY, AMBIGUOUS
    assert REASON_OUTCOME["input_anchor_ambiguous"] == (CLARIFY, AMBIGUOUS)
    assert "input_anchor_ambiguous" != "ambiguous_grain"          # one reason per contested dimension


# ── boundary: multi-arg / bad pin refuse cleanly, never a silent number ─────────────────────
def test_bad_input_anchor_pin_refuses(fixture_connector):
    s = _srv(fixture_connector)
    w = wire_frame(s.frame("cal.month").column("z", "avg(aov@nonesuch)").run())
    assert w["outcome"] in ("refuse", "error")
