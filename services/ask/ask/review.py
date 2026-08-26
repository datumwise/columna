"""Authority review: does this provisional answer deserve datumwise's name on it?

THE CHAIN IS IMMUTABLE (Huayin, 2026-08-26):

    provisional answer  ->  review assessment + proposed revision  ->  human-approved published answer

Nothing in this module rewrites the provisional answer. Not once, not "just formatting". The
provisional text is the evidence of what the agent actually said when asked, and an evidence record
that can be silently edited is not one. What review MAY do — and the first version of this design
wrongly forbade — is PROPOSE a different answer for publication.

Verdict-only was too restrictive, and the reason is practical. A conversational answer can be
correct and still be wrong to publish: too long, slightly imprecise, missing a qualification, badly
organised for standing publication. Refusing the reviewer any way to say "here is what this should
look like" pushes all of that work onto the human, or worse, invites publishing prose that was never
shaped for publication. So review may return:

    APPROVE          publish the provisional answer as it stands
    REVISE           publish THIS proposed answer instead — with the changes and sources named
    DO NOT PUBLISH   and why

Both texts are preserved and the human sees both. The proposal is a proposal: the human publishes
it, edits it, or throws it away.

WHY THE REVIEWER IS A SEPARATE PASS AND NOT A LOUDER PROMPT. The answering model already had the
constitution in front of it and still, on 2026-08-26, cited a [ROADMAP] section as shipped behaviour
and a bibliography as a source. A model checking its own work in the same breath as producing it is
not a check. This runs after, against the same sources, with one job.
"""

from __future__ import annotations

import json
import re

from . import providers

# NINE DIMENSIONS, AND ONE OF THEM IS A RENAME (2026-08-26, after the Anthropic comparison).
#
# The comparison exposed a class of problem broader than citation correctness: an answer can be well
# researched and basically right and still be less trustworthy, because its prose claims more than
# its evidence earns. That wanted a discipline, not five new columns, so it is expressed as ONE new
# dimension and one renamed one:
#
#   factual_grounding  NEW. Facts before interpretation, and verbatim verification of quotations.
#                      The comparison put a direct quote in Anthropic's mouth that could not be
#                      found in the article it cited. Nothing in the old eight named that.
#   claim_calibration  REPLACES `overstatement`, which named only one direction. Both directions
#                      are misrepresentation: an unwarranted universal overclaims, and a settled
#                      Core position hedged into vagueness underclaims. A dimension that can only
#                      see one of them will quietly push every answer toward mush.
#
# The other six keep their names and their stored keys; earlier reviews stay readable as written.
DISPOSITIONS = ("APPROVE", "REVISE", "DO_NOT_PUBLISH")

REVIEW_MODEL = "openai:gpt-5"

INSTRUCTION = """\
You are the authority reviewer for Ask datumwise. A provisional answer has been generated and you \
decide whether datumwise should put its name on it.

You are NOT the author. Do not rewrite the provisional answer in place and do not pretend it said \
something it did not. If it should be published differently, propose a different text and say what \
you changed.

WHAT DATUMWISE'S SOURCE CLASSES ARE ENTITLED TO ESTABLISH
  CORE      — may establish "datumwise holds ...". The ONLY class that may.
  REFERENCE — may explain, contextualise, develop, compare, supply implementation detail. Does NOT
              independently establish the current datumwise position. This is jurisdiction, not
              quality: several reference sources are the highest authority for the thing they
              actually establish.
  EXTERNAL  — describes the outside world; supports comparison, context, criticism. NEVER
              establishes a datumwise position.

THE ANSWER DISCIPLINE YOU ARE ENFORCING
Facts first. Principles clearly. Analysis marked. Claims bounded. No rhetorical inflation.

An answer can be well researched and basically right and still be less trustworthy than it should
be, because its prose claims more than its evidence earns. Most of what you are looking for is that
gap, not outright error.

INSPECT ALL OF THESE, AND SAY SO CONCRETELY — quote the sentence you mean:
  core_support        every datumwise-position claim traces to a CORE source that was actually
                      supplied. A claim resting only on Reference or External is a finding.
  reference_use       reference material informs without silently redefining the current position.
  currency            current vs superseded vs edition-pinned vs historical vs design-stage
                      (ROADMAP) handled correctly. Design-stage material must never read as shipped.
  citation_support    each cited source actually supports the claim attached to it — including
                      specific detail. A named construct, syntax token, version or number attached
                      to a citation that does not carry it is a finding even when the surrounding
                      argument is right.
  factual_grounding   does the prose stay with what the sources establish? Look for: an observation
                      SHARPENED into a stronger proposition than the source supports; an external
                      party interpreted before their own primary source has been described; and
                      above all DIRECT QUOTATIONS — check every quoted sentence verbatim against
                      the source given to you. If it is not there, or is altered, or inverts the
                      original, that is a finding and usually a REVISE. Putting words in a named
                      party's mouth is a different kind of error from getting an argument slightly
                      wrong.
  external_claims     external claims are accurate and attributed to the source that carries them.
  separation          datumwise's claims, external facts, and Ask's own analysis are
                      distinguishable to a reader. Prose may do this; headings are not required and
                      should not be imposed. The specific failure: Ask's own comparison presented
                      as though it were a fact one of the sources stated.
  claim_calibration   is each claim as strong as the evidence earns — NEITHER MORE NOR LESS?
                      Too strong: "there are no ...", "always", "never", "the only ...",
                      "X cannot ..." where the source establishes only a particular architecture,
                      implementation, example or current public account. The bounded form is
                      usually available and costs the argument nothing: "in the architecture
                      Anthropic describes here", "the current public materials emphasise", "in this
                      implementation", "datumwise's current position is".
                      Too weak: a settled Core position hedged into vagueness to sound cautious.
                      False caution about something that IS established misrepresents datumwise
                      just as overclaiming does. Say which direction you found.
  worth_publishing    is this worth preserving publicly at all? A thin, obvious, or duplicative
                      answer is a DO_NOT_PUBLISH even when nothing in it is wrong.

THE DISCIPLINE APPLIES TO YOU TOO. Before you assert that a source does not support something,
SEARCH the passage you were given for it. "Not supported by the provided material" is itself a
factual claim, and asserting it about a term that is present in the text in front of you is the same
failure you are here to catch. When a passage is truncated, say that you could not check rather than
that the claim is unsupported — those are different findings and only one of them is about the
answer.

WHEN YOU PROPOSE A REVISION, prefer the narrowest formulation that fully carries the point. If two
sentences make the same useful argument, take the one needing fewer unsupported assumptions. Do not
flatten the answer into hedging: bounding a claim and weakening it are different acts.

DISPOSITION
  APPROVE         publish the provisional answer as it stands.
  REVISE          publish your proposed answer instead. Use this when the substance is sound but
                  the text is not right for standing publication. Keep the author's voice, keep
                  every citation you can, and do not introduce a claim the sources do not carry.
  DO_NOT_PUBLISH  say why, plainly.

Prefer APPROVE over a cosmetic REVISE. Prefer DO_NOT_PUBLISH over publishing something you had to
argue yourself into. An unverified direct quotation attributed to a named party is never cosmetic.

THE QUESTION:
{question}

THE PROVISIONAL ANSWER:
{answer}

THE SOURCES IT WAS GIVEN, WITH THEIR TEXT (layer tells you the entitlement; the passage is what
the answering model actually had in front of it, so quotations can be checked against it verbatim):
{sources}

EXTERNAL SOURCES IT CLAIMED:
{external}

Reply with ONLY a JSON object:
{{"disposition": "APPROVE" | "REVISE" | "DO_NOT_PUBLISH",
  "findings": {{"core_support": {{"ok": true, "note": "..."}},
               "reference_use": {{"ok": true, "note": "..."}},
               "currency": {{"ok": true, "note": "..."}},
               "citation_support": {{"ok": true, "note": "..."}},
               "factual_grounding": {{"ok": true, "note": "..."}},
               "external_claims": {{"ok": true, "note": "..."}},
               "separation": {{"ok": true, "note": "..."}},
               "claim_calibration": {{"ok": true, "note": "..."}},
               "worth_publishing": {{"ok": true, "note": "..."}}}},
  "summary": "one paragraph a human reviewer can act on",
  "changes": ["what you changed and why, one line each; [] unless REVISE"],
  "proposedAnswer": "the full proposed text, or null unless REVISE"}}
"""

_JSON = re.compile(r"\{.*\}", re.S)


def _fmt_sources(sources: list[dict], evidence: list[dict] | None = None) -> str:
    """Sources with their TEXT where we have it — a quotation cannot be checked against a heading."""
    by_cite = {e["cite"]: e for e in (evidence or [])}
    if not sources and not evidence:
        return "  (none — the answer cited nothing)"
    out = []
    for s in sources or evidence:
        cite = s["cite"]
        layer = s.get("layer") or "unknown"
        head = (f"  [{cite}] layer={layer} · {s.get('label')} — {s.get('heading')}\n"
                f"        standing: {s.get('standing')}")
        ev = by_cite.get(cite)
        if ev and ev.get("text"):
            head += f"\n        passage: {ev['text']}"
        else:
            head += ("\n        passage: (NOT AVAILABLE — you cannot verify a quotation against "
                     "this source; say so rather than assuming it checks out)")
        out.append(head)
    return "\n\n".join(out)


def review(qa: dict, model: str | None = None) -> dict:
    """Run one review pass. Returns the verdict; NEVER returns a mutated provisional answer."""
    prompt = INSTRUCTION.format(
        question=qa["question"],
        answer=qa["answer"],
        sources=_fmt_sources(qa.get("sources") or [], qa.get("evidence") or []),
        external=json.dumps(qa.get("external") or [], indent=1),
    )
    comp = providers.complete([{"role": "user", "content": prompt}], model=model or REVIEW_MODEL,
                              max_tokens=6000)
    text = comp.text.strip()
    m = _JSON.search(text)
    if not m:
        # A reviewer that cannot be parsed must not read as an approval. Fail closed.
        return {"disposition": "DO_NOT_PUBLISH", "findings": {},
                "summary": f"review output could not be parsed: {text[:200]!r}",
                "changes": [], "proposedAnswer": None, "parseError": True,
                "model": f"{comp.provider}:{comp.model}", "costUsd": comp.cost_usd}
    try:
        v = json.loads(m.group(0))
    except json.JSONDecodeError as e:
        return {"disposition": "DO_NOT_PUBLISH", "findings": {},
                "summary": f"review output was not valid JSON: {e}",
                "changes": [], "proposedAnswer": None, "parseError": True,
                "model": f"{comp.provider}:{comp.model}", "costUsd": comp.cost_usd}

    return _normalise_verdict(v, model=f"{comp.provider}:{comp.model}", cost=comp.cost_usd)


def _normalise_verdict(v: dict, model: str, cost: float) -> dict:
    """Fail closed, and refuse the two shapes that would quietly become approvals."""
    disposition = str(v.get("disposition", "")).upper().replace(" ", "_")
    if disposition not in DISPOSITIONS:
        disposition = "DO_NOT_PUBLISH"
    proposed = v.get("proposedAnswer") or None
    if disposition == "REVISE" and not proposed:
        # REVISE with nothing proposed is not a disposition, it is a dropped sentence.
        disposition = "DO_NOT_PUBLISH"
        v["summary"] = (v.get("summary") or "") + \
            " [downgraded: REVISE was returned with no proposed answer]"
    if disposition != "REVISE":
        proposed = None  # a proposal only means something when the reviewer asked to swap the text
    return {
        "disposition": disposition,
        "findings": v.get("findings") or {},
        "summary": v.get("summary") or "",
        "changes": v.get("changes") or [],
        "proposedAnswer": proposed,
        "parseError": False,
        "model": model,
        "costUsd": cost,
    }
