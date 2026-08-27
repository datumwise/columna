"""TYPED AUTHORITY — who is entitled to say what a work is called (Huayin, rulings C and D, 2026-08-26).

F1 failed h2, h3 and r6 on BOTH gpt-5 and gpt-4.1 for one structural reason: passages inside other
papers that NAME the work being asked about — reference lists, reading paths, further-reading
pointers — out-ranked the work's own current deposit on questions about identity and currency. On h2
the system told a reader that a superseded edition was datumwise's current position, citing two
other papers' pointer sections as its evidence.

These tests hold the repair from both sides, because a gate is only as good as the case it must NOT
catch:

  · the corpus may not establish publication identity  — the pointer sections are excluded from
    identity questions, and only from identity questions;
  · the registry may not establish doctrine            — it appears only when asked, carries no
    argument, and is never invented for a work that does not exist;
  · an explicitly historical question must REACH the
    preserved record                                    — naming a superseded edition by number
                                                          opens the historical jurisdiction.

They read the LIVE registry and the LIVE index on purpose. If a later ruling moves the Analytical
Governance or Certainty records, these should change with it — unlike the F3 durability fixtures,
which are synthetic precisely so that they cannot.
"""

from __future__ import annotations

import json
from pathlib import Path

from ask import identity, retrieve

H2 = "I'm reading the Analytical Governance v1.1 page on your site. Is that datumwise's current position?"
H4 = "What did version 1.1 of Analytical Governance argue, and what changed in version 2.0?"
R6 = "What is the Analytical Governance paper called, and what version is current?"
S3 = "Which source is authoritative for what Frame-QL actually does?"


# ── the question class ────────────────────────────────────────────────────────────────────────────

def test_only_identity_questions_get_the_registry():
    assert identity.asks_identity(R6) and identity.asks_identity(H2)
    assert not identity.asks_identity("What is a basis?")
    assert not identity.asks_identity("Does datumwise hold that a system that cannot refuse is not governed?")


def test_a_work_is_recognised_by_a_name_it_no_longer_carries():
    """The question this module exists for is asked in the OLD words.

    'Is the Theory of Certainty still current?' names a work whose current title no longer contains
    those words. A name index built from current titles alone would fail to recognise exactly the
    question that needs the registry most.
    """
    assert identity.works_named("Is the Theory of Certainty still current?") == ["w-theory-of-certainty"]
    assert identity.works_named("what is the ground for certainty") == ["w-theory-of-certainty"]


def test_no_card_is_invented_for_a_work_that_does_not_exist():
    """a1's hallucination trap, guarded at the source. There is no Trust Framework in the registry;
    a card for it would be a fabricated publication record, which is worse than none."""
    assert identity.cards_for("Give me the DOI for the Trust Framework") == []
    assert identity.asks_identity("Give me the DOI for the Trust Framework")  # the cue DID fire


def test_the_card_carries_both_titles_and_says_which_is_which():
    card = identity.record_card("w-theory-of-certainty")
    assert card["label"] == "The Ground for Certainty"
    assert "CURRENT RECORD: v1.1" in card["text"]
    assert "10.5281/zenodo.22118479" in card["text"]
    # the superseded record is present, under ITS OWN title, and marked superseded
    assert "SUPERSEDED RECORDS" in card["text"]
    assert '"The Theory of Certainty"' in card["text"]
    assert "10.5281/zenodo.22114802" in card["text"]


def test_the_card_refuses_to_settle_doctrine():
    """It is authority for identity and it says so, in the sentence the agent is told to trust."""
    card = identity.record_card("w-analytical-governance")
    assert "CURRENTLY CALLED" in card["standing"]
    assert "carries no argument" in card["standing"]
    assert "may not be used to settle a question of doctrine" in card["standing"]


# ── the exclusion, and the case it must not catch ────────────────────────────────────────────────

def test_another_papers_pointer_cannot_answer_what_this_work_is_called():
    """h2 and r6, at the point of failure. Both models cited /learn/frameql-primer's 'Where to Go
    Next' and /learn/frameql-an-introduction's 'Implementation and further reading', which name
    'Analytical Governance, Version 1.1' — correct for their own edition, and not authority for what
    AG is called today."""
    for q in (H2, R6):
        hits = retrieve.search(q, k=8)
        offenders = [h for h in hits
                     if retrieve.is_pointer(h) and retrieve.work_of(h) != "w-analytical-governance"]
        assert not offenders, [(h["sourceLabel"], h["heading"]) for h in offenders]


def test_the_same_pointer_section_stays_reachable_for_the_question_it_does_answer():
    """The gate is scoped to ONE question class. s3 asks which source is authoritative for shipped
    meaning — a claim these sections really do make — and must still reach them."""
    hits = retrieve.search(S3, k=8)
    assert any(retrieve.is_pointer(h) for h in hits), (
        "the pointer gate has leaked out of the identity question class")


def test_the_registry_appears_only_when_asked():
    assert [c["label"] for c in retrieve.registry_cards(R6)] == ["Analytical Governance"]
    assert retrieve.registry_cards("What is a basis?") == []
    assert retrieve.registry_cards(S3) == []


# ── ruling D · the preserved record must be REACHABLE, not merely present ────────────────────────

def test_naming_a_superseded_edition_by_number_is_a_historical_question():
    assert identity.names_superseded_edition(H4)
    assert identity.names_superseded_edition(H2)
    # naming the CURRENT version is not a historical question
    assert not identity.names_superseded_edition(R6)
    assert not identity.names_superseded_edition("What does Analytical Governance v2.0 argue?")


def test_h4_actually_retrieves_the_v1_1_material_it_asks_about():
    """The F1 finding: h4 passed deterministically because the strings '1.1' and '2.0' appeared,
    while BOTH models answered that the corpus does not establish what v1.1 argued — because the
    preserved edition was never retrieved. Reachability is the assertion, not the digits."""
    hits = retrieve.search(H4, k=8)
    v11 = [h for h in hits if h["sourceId"] == "s-analytical-governance-v1-1"]
    assert len(v11) >= 3, [(h["sourceLabel"], h["heading"]) for h in hits]
    assert all("PRESERVED HISTORICAL STATE" in h["standing"] for h in v11)
    # it must reach v1.1's own account of what changed, not merely some v1.1 prose
    assert any("revision note" in h["heading"].lower() for h in v11), [h["heading"] for h in hits]


def test_the_preserved_certainty_edition_is_reachable_the_same_way():
    """The real 2026-08-26 transition, as the case. Nothing about this is Analytical-Governance
    specific: it is registry-derived, so a work superseded tomorrow gets the same behaviour."""
    hits = retrieve.search(
        "What did version 1.0 of the Theory of Certainty say about behavioral evidence?", k=8)
    v10 = [h for h in hits if h["sourceId"] == "s-theory-of-certainty-v1-0"]
    assert v10, [(h["sourceLabel"], h["heading"]) for h in hits]
    assert all(h["readableRecordId"] == "w-theory-of-certainty.r01" for h in v10)
    assert all(h["currentRecordId"] == "w-theory-of-certainty.r02" for h in v10)


def test_a_current_position_question_still_cannot_be_settled_by_a_preserved_edition():
    """The other arm of ruling D, and the one that must not be traded away for the first."""
    hits = retrieve.search("what does datumwise hold about analytical identity?", k=8)
    assert hits and all(h["layer"] == "core" for h in hits)
    assert not any(h["isHistorical"] for h in hits)


# ── the prompt actually carries it ───────────────────────────────────────────────────────────────

def test_the_registry_reaches_the_model_in_its_own_namespace():
    from ask.skill import build_prompt
    msgs = build_prompt(R6, retrieve.search(R6, k=4), registry=retrieve.registry_cards(R6))
    user = msgs[-1]["content"]
    assert "[R1] PUBLICATION REGISTRY — Analytical Governance" in user
    assert "PUBLICATION REGISTRY — IDENTITY AND CURRENCY" in user
    # and it is absent, explicitly, when the question did not ask
    plain = build_prompt("What is a basis?", [], registry=[])[-1]["content"]
    assert "[R1]" not in plain
    assert "did not ask about any work's identity or currency" in plain


def test_the_constitution_names_who_may_say_what_a_work_is_called():
    from ask.skill import CONSTITUTION
    assert "FOUR SOURCE CLASSES" in CONSTITUTION
    assert "WHO MAY SAY WHAT A WORK IS CALLED" in CONSTITUTION
    assert "NOT authority for the cited work's" in CONSTITUTION


def test_a_registry_citation_is_evidence_and_not_a_durable_citation():
    """[R#] must not enter `sources`. A durable citation's whole job is to re-resolve its stored
    presentation against the registry later; a citation OF the registry has nothing to re-resolve."""
    src = Path(__file__).resolve().parents[1] / "ask" / "answer.py"
    body = src.read_text()
    assert "reg_by_token" in body and "used_reg" in body
    assert 'for t in used_reg' in body
    # `sources` is built from used_tokens only
    i = body.index("    sources = [")
    j = body.index("        for t in used_tokens", i)
    assert "used_reg" not in body[i:j]


# ── the harness assertion itself (ruling D) ──────────────────────────────────────────────────────

def test_must_cite_fails_an_answer_that_never_reached_the_evidence():
    """The F1 false pass, as a test. An answer containing the digits and citing nothing must fail."""
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "eval"))
    from run_eval import deterministic

    case = {"id": "h4", "must_any": [["1.1"], ["2.0"]],
            "must_cite": ["s-analytical-governance-v1-1"]}
    refused = {"answer": "The corpus does not establish what version 1.1 argued. "
                         "The current record is version 2.0." + " padding." * 40,
               "sources": [{"sourceId": "s-frameql-introduction"}],
               "verify": {"problems": []}}
    got = deterministic(case, refused)
    assert got["pass"] is False
    assert any("did not cite required source" in f for f in got["fails"]), got["fails"]

    reached = {**refused, "sources": [{"sourceId": "s-analytical-governance-v1-1"}]}
    assert deterministic(case, reached)["pass"] is True


def test_the_h4_case_now_carries_the_reachability_assertion():
    cases = json.loads((Path(__file__).resolve().parents[1] / "eval/questions.json").read_text())["cases"]
    h4 = next(c for c in cases if c["id"] == "h4")
    assert h4["must_cite"] == ["s-analytical-governance-v1-1"]
    assert any("corpus does not establish what" in s for s in h4.get("must_not", []))
