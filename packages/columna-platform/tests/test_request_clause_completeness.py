"""REQUEST COMPLETENESS — no accepted clause may simply be unread (OF-53, OF-55).

THE INVARIANT (ruled Huayin, 2026-09-14): every syntactic part of a request accepted into successor
execution is either CONSUMED by governed resolution or EXPLICITLY REJECTED as unsupported.

WHAT WENT WRONG, SO THE CONTROLS ARE READ AGAINST IT. `Statement` has nine fields and this profile
read two. The other seven were parsed, validated, carried and ignored, so

    SELECT revenue AT {store*day} WHERE store = 'nowhere'

served ALL FOUR ROWS with `outcome: serve` and a clean disclosure. Not a partial answer and not a
silent empty one — an AFFIRMATIVE result for a question nobody asked, indistinguishable on the wire
from the unrestricted ask. `EXPLAIN` was worse in kind: the one clause whose entire meaning is *do
not execute* executed, fetched material and served rows.

THE CLASSIFICATION IS A CAPABILITY LIMIT, NOT A GOVERNED VERDICT. `unsupported` — ERROR, no
jurisdiction — and never `want_of_law`. The public request form may be perfectly lawful and may
execute on another profile; what is missing is a governed interpretation HERE. Calling it a want of
law would tell an operator their question was unlawful and send them to fix a publication that is
not wrong. There is no Core fallback for the same reason: handing the statement to another runtime
would misreport whose semantics produced the number.
"""
from __future__ import annotations

import dataclasses
import json
import pathlib

import pytest
from columna_core.envelope import Statement, parse_statement
from columna_core.governed.publication import parse_publication
from columna_core.governed.resolve import resolve_all

from columna_platform import request as rq
from columna_platform.provider import PlatformExecutionProvider
from columna_platform.refusals import ProofRefusal, UnsupportedByThisProfile

ARTIFACT = (pathlib.Path(__file__).parents[2] / "columna-core" / "tests" / "fixtures_v2"
            / "lighthouse-v2-publication.json")
SUPPORTED = "SELECT revenue AT {store*day}"

#: Every clause form that parses on the public surface and that this profile does not implement.
#: Written as PUBLIC SPELLINGS, not field names, because that is what a caller types.
UNSUPPORTED_ASKS = [
    ("WHERE",       SUPPORTED + " WHERE store = 'east'"),
    ("WHERE-empty", SUPPORTED + " WHERE store = 'nowhere'"),
    ("HAVING",      SUPPORTED + " HAVING revenue > 1000000"),
    ("ORDER BY",    SUPPORTED + " ORDER BY revenue DESC"),
    ("LIMIT",       SUPPORTED + " LIMIT 1"),
    ("LIMIT PER",   SUPPORTED + " LIMIT 1 PER {store}"),
    ("WITH",        "WITH x = 1 " + SUPPORTED),
    ("EXPLAIN",     "EXPLAIN " + SUPPORTED),
]


@pytest.fixture(scope="module")
def pub():
    return parse_publication(json.loads(ARTIFACT.read_text(encoding="utf-8")))


@pytest.fixture(scope="module")
def views(pub):
    return resolve_all(pub)


def _refusal(result):
    return result.columns[0].refusal


# ══ the completeness rule itself ═══════════════════════════════════════════════════════════════

def test_every_statement_field_is_classified_exactly_once():
    """THE PIN. Not "these six clauses are unsupported" — that is a list, and a list is what went
    stale. The rule is over the WHOLE request surface: the statement's field set must partition into
    consumed ∪ consumed-upstream ∪ unsupported, with nothing left over and nothing double-counted.

    This is the test that fails the day someone adds a tenth field to `Statement` without deciding
    what the successor does with it — which is exactly how the first seven got in."""
    fields = {f.name for f in dataclasses.fields(Statement)}
    consumed = rq.CONSUMED_CLAUSES
    upstream = rq.CONSUMED_UPSTREAM
    unsupported = set(rq.UNSUPPORTED_CLAUSES)

    assert consumed | upstream | unsupported == fields, (
        f"unclassified request fields: {sorted(fields - (consumed | upstream | unsupported))}")
    assert not (consumed & unsupported), "a field cannot be both consumed and unsupported"
    assert not (consumed & upstream) and not (upstream & unsupported)


def test_an_unclassified_field_fails_closed_rather_than_being_ignored():
    """The rule ENFORCED, not merely tested. A request surface carrying something this profile has
    not classified is one it cannot honestly execute against, because the unclassified part might
    change the answer. So it refuses — loudly, on every request — instead of proceeding."""
    @dataclasses.dataclass
    class FutureStatement:
        series: tuple = ()
        anchor: tuple = ()
        explain: bool = False
        from_manifold: object = None
        bindings: tuple = ()
        where: tuple = ()
        having: tuple = ()
        order_by: tuple = ()
        limit: object = None
        sample: object = "10%"          # the tenth field nobody classified

    with pytest.raises(UnsupportedByThisProfile) as e:
        rq.require_supported_clauses(FutureStatement())
    assert "sample" in str(e.value)
    assert "has not classified" in str(e.value)


# ══ control 1 · the supported request is unchanged ════════════════════════════════════════════

def test_the_supported_request_still_plans_exactly_as_before(pub, views):
    """Control 1 and control 8. The guard must be invisible to every request that already worked."""
    result = PlatformExecutionProvider(pub, views).plan(parse_statement(SUPPORTED))
    assert _refusal(result) is None
    assert result.columns[0].name == "revenue"
    assert result.anchor == ("store", "day")


def test_an_alias_is_still_honoured(pub, views):
    """Control 8. `AS` rides on `series`, which IS consumed — the guard must not sweep it up."""
    result = PlatformExecutionProvider(pub, views).plan(
        parse_statement("SELECT revenue AS takings AT {store*day}"))
    assert _refusal(result) is None
    assert result.columns[0].name == "takings"


def test_a_governed_refusal_is_still_a_governed_refusal(pub, views):
    """Control 8, the other direction. The guard must not convert a LAW finding into a capability
    limit — an ask off the constitutive anchor is still `want_of_law`, not `unsupported`."""
    result = PlatformExecutionProvider(pub, views).plan(parse_statement("SELECT revenue AT {store}"))
    assert _refusal(result).reason == "want_of_law"


# ══ controls 2, 3, 4 · every unimplemented clause refuses as a capability limit ═══════════════

@pytest.mark.parametrize("label,ask", UNSUPPORTED_ASKS)
def test_an_unimplemented_clause_is_unsupported_and_never_silently_served(pub, views, label, ask):
    """Controls 2, 3 and 4. ERROR / `unsupported`, on both public capabilities, with the clause
    NAMED in the detail so the caller learns which part of their request was not implemented."""
    stmt = parse_statement(ask)
    for capability in ("plan", "run"):
        result = getattr(PlatformExecutionProvider(pub, views), capability)(stmt)
        refusal = _refusal(result)
        assert refusal is not None, f"{label} via {capability} produced no refusal"
        assert refusal.reason == "unsupported", f"{label} via {capability}"
        assert result.data is None
        assert result.columns[0].frame is None


@pytest.mark.parametrize("label,ask", UNSUPPORTED_ASKS)
def test_the_unsupported_detail_names_the_clause_and_says_why(pub, views, label, ask):
    """An `unsupported` with no reason is not an answer. The caller must be able to tell WHICH
    clause and WHY, without reading our source."""
    result = PlatformExecutionProvider(pub, views).plan(parse_statement(ask))
    detail = _refusal(result).detail
    # `LIMIT 1 PER {store}` is the `limit` field; the profile names the CLAUSE (`LIMIT`), not the
    # sub-form, because the field is what it either implements or does not.
    spelling = label.split("-")[0].split(" ")[0]
    assert spelling in detail, f"{label}: detail does not name the clause"
    assert "does not implement" in detail


def test_a_restriction_matching_nothing_is_refused_rather_than_served_entire(pub, views):
    """Control 3, stated as the witness it came from. This exact statement served all four rows.
    The assertion is deliberately narrow: not "it refuses" but "it does not SERVE", because the
    defect was never a wrong refusal — it was a confident, complete, affirmative answer."""
    result = PlatformExecutionProvider(pub, views).plan(
        parse_statement(SUPPORTED + " WHERE store = 'nowhere'"))
    assert result.data is None
    assert _refusal(result) is not None
    assert _refusal(result).reason == "unsupported"


# ══ control 5 · the two public capabilities agree ═════════════════════════════════════════════

def _verdict(result):
    return result.columns[0].refusal.reason if result.columns[0].refusal else "no-refusal"


@pytest.mark.parametrize("label,ask", UNSUPPORTED_ASKS)
def test_check_and_execute_agree_on_capability_support(pub, views, label, ask):
    """Control 5, and the OF-55 repair. `check_frame_query` plans and `execute_frame_query` runs;
    a caller who pre-flights must not get a different verdict — or an exception — where a caller who
    simply ran the query gets an answer. Before the repair, `plan` RAISED on a capability limit that
    `run` reported cleanly."""
    stmt = parse_statement(ask)
    provider = PlatformExecutionProvider(pub, views)
    assert _verdict(provider.plan(stmt)) == _verdict(provider.run(stmt)) == "unsupported", label


def test_plan_and_run_may_differ_only_on_MATERIAL_not_on_capability(pub, views):
    """THE ONE LEGITIMATE DISAGREEMENT, PINNED SO NOBODY "FIXES" IT.

    On a deployment that binds NO material, the supported ask plans fine and does not run: `plan`
    answers "is this askable" and returns no refusal, while `run` reports `unsupported` because
    binding a material source is a deployment act. That asymmetry is by design and is about
    DEPLOYMENT STATE, not about which clauses the profile implements.

    The control 5 rule is therefore precise: check and execute must agree on CAPABILITY SUPPORT.
    They are allowed to differ on whether material happens to be bound, and this test fixes that
    boundary so a future reading of "they must always agree" cannot erase it."""
    provider = PlatformExecutionProvider(pub, views)       # no material binding
    stmt = parse_statement(SUPPORTED)
    assert _verdict(provider.plan(stmt)) == "no-refusal"
    ran = provider.run(stmt)
    assert _verdict(ran) == "unsupported"
    assert "binds no material" in ran.columns[0].refusal.detail


def test_the_planning_path_never_raises_a_capability_limit(pub, views):
    """OF-55 directly. An exception escaping past the server is not an answer; a caller who asked a
    meaningful question learns nothing from a transport-level error."""
    provider = PlatformExecutionProvider(pub, views)
    for _label, ask in UNSUPPORTED_ASKS:
        provider.plan(parse_statement(ask))            # must not raise
    provider.plan(parse_statement("SELECT revenue, revenue AT {store*day}"))


# ══ control 6 · the classification, and no Core fallback ══════════════════════════════════════

@pytest.mark.parametrize("label,ask", UNSUPPORTED_ASKS)
def test_an_unimplemented_clause_is_never_a_governed_verdict(pub, views, label, ask):
    """Control 6, first half, and the distinction the ruling insists on. `want_of_law` would claim
    an analytical-law finding where the condition is a missing profile capability — it would tell an
    operator their question was unlawful and send them to fix a publication that is not wrong."""
    result = PlatformExecutionProvider(pub, views).plan(parse_statement(ask))
    assert _refusal(result).reason not in ("want_of_law", "want_of_state")


def test_the_capability_class_is_not_a_governed_refusal():
    """Structural, not behavioural: the class CANNOT be caught by the governed handler, so it cannot
    be given a jurisdiction by accident."""
    assert not issubclass(UnsupportedByThisProfile, ProofRefusal)


def test_no_core_fallback_is_attempted_for_an_unimplemented_clause(pub, views, monkeypatch):
    """Control 6, second half. The profile says it does not do this. It does not quietly hand the
    statement to the runtime it was built to stand beside — which would make the provider a
    passthrough that misreports whose semantics served the number."""
    import columna_platform.serving as serving_mod

    called = []
    monkeypatch.setattr(serving_mod, "decide_result",
                        lambda *a, **k: called.append(a) or (_ for _ in ()).throw(AssertionError()))
    result = PlatformExecutionProvider(pub, views).plan(
        parse_statement(SUPPORTED + " WHERE store = 'east'"))
    assert _refusal(result).reason == "unsupported"
    assert called == []


def test_the_reason_is_the_already_registered_one_and_mints_nothing():
    """`unsupported` is `(ERROR, None, REALIZATION)` and was registered before this repair. The
    repair introduces no reason, no mood and no contract version."""
    from columna_core.disclosure import REASON_OUTCOME
    assert "unsupported" in REASON_OUTCOME
