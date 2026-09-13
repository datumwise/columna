"""§5 — ANALYTICAL REQUEST RESOLUTION, the integration proof's real question.

Can a public Frame-QL request become `AnalyticalIdentity(family_id, anchor)` using governed law
alone — no `model.py` measure/member resolution, no planner identity logic, no `.cml` meaning
lookup, no fuzzy matching, no convenience map, no fixture special case?

These are the controls for that question at the FORMAT level. The deployment-level answer is
different and is recorded in `docs/architecture/successor_integration_recon_v0_1.md`: the shipped
server carries no v2-governed Manifold to opt in, so the slice stops before the server.
"""
from __future__ import annotations

import copy
import json
import pathlib

import pytest
from columna_core.envelope import parse_statement
from columna_core.governed.publication import PublicationFormatRefusal, parse_publication
from columna_core.governed.resolve import resolve_all

from columna_platform import request as rq
from columna_platform import serving
from columna_platform.provider import PlatformExecutionProvider
from columna_platform.refusals import UnsupportedByThisProfile, WantOfLaw

ARTIFACT = (pathlib.Path(__file__).parents[2] / "columna-core" / "tests" / "fixtures_v2"
            / "lighthouse-v2-publication.json")

#: The one family this slice supports, and its governed identity — written out so the test states the
#: expected answer rather than recomputing it from the same source it is checking.
REVENUE_ID = "fam_qv8Ky3mR7bTpZa1LwXcNdg"


@pytest.fixture(scope="module")
def raw():
    return json.loads(ARTIFACT.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def pub(raw):
    return parse_publication(raw)


@pytest.fixture(scope="module")
def views(pub):
    return resolve_all(pub)          # family_id -> the total nine-responsibility Law(F) view


# ══ POSITIVE ═════════════════════════════════════════════════════════════════════════════════════

def test_a_series_token_resolves_to_exactly_one_governed_family(pub):
    """§5.1. `revenue` is a canonical reference in the publication; it names one family_id."""
    got = rq.resolve(pub, parse_statement("SELECT revenue AT {store*day}"))
    assert got.identity.family_id == REVENUE_ID
    assert got.family.canonical_reference == "revenue"


def test_the_anchor_resolves_by_its_GOVERNED_COMPONENTS(pub):
    """§5.2. `AT {store*day}` is matched against the publication's own `anchor` declaration, whose
    components are store and day — so the governed anchor is `sale_at`. The name `sale_at` is never
    typed by the requester and never guessed: it is read off the declaration that carries those
    components."""
    got = rq.resolve(pub, parse_statement("SELECT revenue AT {store*day}"))
    assert got.identity.anchor == "sale_at"
    assert got.identity.anchor == got.family.constitutive_anchor


def test_component_order_is_not_identity(pub):
    """`AT {day*store}` is the same anchor. A product of levels has no order, and treating the
    spelling as identity would make two spellings of one ask two different analytical objects."""
    a = rq.resolve(pub, parse_statement("SELECT revenue AT {store*day}")).identity
    b = rq.resolve(pub, parse_statement("SELECT revenue AT {day*store}")).identity
    assert a == b


def test_an_alias_resolves_by_governed_alias_not_by_similarity(pub, raw):
    """Aliases are a GOVERNED fact the publication declares. Resolution honours a declared alias and
    nothing else — which is the whole difference between a lookup and a guess."""
    mutated = copy.deepcopy(raw)
    for decl in mutated["logical"]["declarations"]:
        if decl["kind"] == "family" and decl["body"]["canonical_reference"] == "revenue":
            decl["body"]["aliases"] = ["turnover"]
    p2 = parse_publication(mutated)
    assert rq.resolve(p2, parse_statement("SELECT turnover AT {store*day}")).identity.family_id == REVENUE_ID
    # …and a name that merely LOOKS like it still does not resolve.
    with pytest.raises(WantOfLaw):
        rq.resolve(p2, parse_statement("SELECT turnovers AT {store*day}"))


def test_the_provider_plans_the_neutral_result_and_touches_no_data(pub, views):
    """§10 positive. `plan()` produces a `FrameResult` with no data and no refusal — the would-be
    serve — and the server, not this path, decides what the wire says about it."""
    p = PlatformExecutionProvider(pub, views, manifold_id="lighthouse")
    fr = p.plan(parse_statement("SELECT revenue AT {store*day}"))
    assert fr.data is None                      # a planned frame carries no data, by construction
    assert [c.name for c in fr.columns] == ["revenue"]
    assert fr.columns[0].refusal is None
    assert fr.outcome == "serve"                # the would-be mood
    assert fr.anchor == ("store", "day")


def test_an_alias_becomes_the_column_name(pub, views):
    p = PlatformExecutionProvider(pub, views)
    fr = p.plan(parse_statement("SELECT revenue AS takings AT {store*day}"))
    assert [c.name for c in fr.columns] == ["takings"]


# ══ NEGATIVE ═════════════════════════════════════════════════════════════════════════════════════

def test_an_unknown_series_token_is_refused_and_not_guessed(pub, views):
    """§5.3 / control 2. `revenu` is one letter from a real family and resolves to nothing."""
    with pytest.raises(WantOfLaw) as e:
        rq.resolve(pub, parse_statement("SELECT revenu AT {store*day}"))
    assert "no governed family answers" in str(e.value)
    fr = PlatformExecutionProvider(pub, views).plan(parse_statement("SELECT revenu AT {store*day}"))
    assert fr.outcome == "refuse"
    assert fr.columns[0].refusal.reason == serving.WANT_OF_LAW
    assert fr.columns[0].name == "revenu"        # reported verbatim, never corrected to `revenue`


def test_two_families_under_one_reference_cannot_EXIST_to_be_chosen_between(raw):
    """§5.4 / control 3 — answered one layer earlier than expected, and better.

    An arbitrary choice between two matches is impossible here because an artifact that offers two
    matches DOES NOT PARSE: §2.2 refuses at read time. The resolver relies on that guarantee instead
    of re-checking it, so this control pins the guarantee itself — if it ever weakens, this fails
    rather than the resolver silently picking the first match."""
    mutated = copy.deepcopy(raw)
    for decl in mutated["logical"]["declarations"]:
        if decl["kind"] == "family" and decl["body"]["canonical_reference"].startswith("count("):
            decl["body"]["aliases"] = ["revenue"]        # a second family answering to `revenue`
    with pytest.raises(PublicationFormatRefusal) as e:
        parse_publication(mutated)
    assert "two families" in str(e.value) and "ambiguous canonical reference" in str(e.value)


def test_an_anchor_with_no_governed_declaration_refuses(pub, views):
    """§5.5 / control 4. `region` is a plausible dimension and no governed anchor is declared over
    it, so there is nothing to resolve to and nothing is invented."""
    with pytest.raises(WantOfLaw) as e:
        rq.resolve(pub, parse_statement("SELECT revenue AT {region}"))
    assert "no governed anchor is declared" in str(e.value)
    assert "sale_at{day*store}" in str(e.value)          # says what IS declared, so the ask is fixable


def test_a_subset_of_the_governed_anchor_is_movement_and_refuses_without_a_licence(pub):
    """`AT {store}` is a proper subset of the constitutive anchor. It is structurally projectable and
    that is exactly why it must refuse: mechanical combinability is not analytical permission."""
    with pytest.raises(WantOfLaw) as e:
        rq.resolve(pub, parse_statement("SELECT revenue AT {store}"))
    assert "no governed anchor is declared" in str(e.value)


def test_the_grand_total_frame_is_movement_and_refuses(pub):
    with pytest.raises(WantOfLaw) as e:
        rq.resolve(pub, parse_statement("SELECT revenue AT {}"))
    assert "MOVEMENT" in str(e.value)


def test_a_multi_series_request_is_UNSUPPORTED_not_unlawful(pub, views):
    """Control 5, and the distinction the ruling insists on: a capability limit may not wear a
    governed jurisdiction. `UnsupportedByThisProfile` is not a `ProofRefusal`, is not caught by the
    planning path, and therefore cannot arrive at the wire as a governed refusal."""
    from columna_platform.refusals import ProofRefusal
    stmt = parse_statement("SELECT revenue, revenue AT {store*day}")
    with pytest.raises(UnsupportedByThisProfile) as e:
        rq.resolve(pub, stmt)
    assert not isinstance(e.value, ProofRefusal)
    with pytest.raises(UnsupportedByThisProfile):
        PlatformExecutionProvider(pub, views).plan(stmt)


@pytest.mark.parametrize("method,args", [("run", ("stmt",)), ("explain", ("stmt",)), ("operators", ())])
def test_unsupported_provider_operations_refuse_honestly_and_never_delegate(pub, views, method, args):
    """Control 5. No Core fallback: the provider says it does not do this, rather than quietly
    handing the request to the runtime it was built to stand beside."""
    p = PlatformExecutionProvider(pub, views)
    with pytest.raises(UnsupportedByThisProfile):
        getattr(p, method)(*args)


def test_published_scope_is_none_which_the_existing_contract_already_allows(pub, views):
    """The one method that answers rather than refusing. `None` is not a stub: the protocol says
    "or None", and both server consumers already branch on it."""
    assert PlatformExecutionProvider(pub, views).published_scope() is None


# ══ ISOLATION ════════════════════════════════════════════════════════════════════════════════════

def test_no_cml_is_consulted_to_determine_analytical_identity(pub, views, tmp_path, monkeypatch):
    """Control 6. Resolution runs to completion from an in-memory publication with the working
    directory moved somewhere that contains no `.cml` at all — and the parser module that reads one
    is not imported by this package (asserted separately, over the static and runtime import
    graphs, in `test_proof_a_findings.py`)."""
    monkeypatch.chdir(tmp_path)
    assert not list(tmp_path.glob("**/*.cml"))
    got = rq.resolve(pub, parse_statement("SELECT revenue AT {store*day}"))
    assert got.identity.family_id == REVENUE_ID


def test_resolution_reads_only_the_governed_projection(pub):
    """The resolver's inputs are the statement and the publication. Nothing it returns carries a
    physical identifier — no table, no column, no connection — because it never saw one."""
    got = rq.resolve(pub, parse_statement("SELECT revenue AT {store*day}"))
    blob = f"{got.identity} {got.family} {got.column_name}"
    # (`amount` is deliberately absent from this list: it occurs in the family's governed
    # PARTICIPATION prose as an English word, which is a governed fact, not a column name.)
    for physical in ("sales_lines", "warehouse", "store_id", "sale_date"):
        assert physical not in blob
