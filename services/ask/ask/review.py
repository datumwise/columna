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

INSPECT ALL OF THESE, AND SAY SO CONCRETELY — quote the sentence you mean:
  core_support        every datumwise-position claim traces to a CORE source that was actually
                      supplied. A claim resting only on Reference or External is a finding.
  reference_use       reference material informs without silently redefining the current position.
  currency            current vs superseded vs edition-pinned vs historical vs design-stage
                      (ROADMAP) handled correctly. Design-stage material must never read as shipped.
  citation_support    each cited source actually supports the claim attached to it.
  external_claims     external claims are accurate and attributed, where any are made.
  separation          datumwise's claims, external facts, and Ask's own analysis are
                      distinguishable to a reader. Prose may do this; headings are not required.
  overstatement       overclaiming, missing qualification, false precision, invented standing.
  worth_publishing    is this worth preserving publicly at all? A thin, obvious, or duplicative
                      answer is a DO_NOT_PUBLISH even when nothing in it is wrong.

DISPOSITION
  APPROVE         publish the provisional answer as it stands.
  REVISE          publish your proposed answer instead. Use this when the substance is sound but
                  the text is not right for standing publication. Keep the author's voice, keep
                  every citation you can, and do not introduce a claim the sources do not carry.
  DO_NOT_PUBLISH  say why, plainly.

Prefer APPROVE over a cosmetic REVISE. Prefer DO_NOT_PUBLISH over publishing something you had to
argue yourself into.

THE QUESTION:
{question}

THE PROVISIONAL ANSWER:
{answer}

THE SOURCES IT WAS GIVEN (layer tells you the entitlement):
{sources}

EXTERNAL SOURCES IT CLAIMED:
{external}

Reply with ONLY a JSON object:
{{"disposition": "APPROVE" | "REVISE" | "DO_NOT_PUBLISH",
  "findings": {{"core_support": {{"ok": true, "note": "..."}},
               "reference_use": {{"ok": true, "note": "..."}},
               "currency": {{"ok": true, "note": "..."}},
               "citation_support": {{"ok": true, "note": "..."}},
               "external_claims": {{"ok": true, "note": "..."}},
               "separation": {{"ok": true, "note": "..."}},
               "overstatement": {{"ok": true, "note": "..."}},
               "worth_publishing": {{"ok": true, "note": "..."}}}},
  "summary": "one paragraph a human reviewer can act on",
  "changes": ["what you changed and why, one line each; [] unless REVISE"],
  "proposedAnswer": "the full proposed text, or null unless REVISE"}}
"""

_JSON = re.compile(r"\{.*\}", re.S)


def _fmt_sources(sources: list[dict]) -> str:
    if not sources:
        return "  (none — the answer cited nothing)"
    out = []
    for s in sources:
        layer = s.get("layer") or "unknown"
        out.append(f"  [{s['cite']}] layer={layer} · {s.get('label')} — {s.get('heading')}\n"
                   f"        standing: {s.get('standing')}")
    return "\n".join(out)


def review(qa: dict, model: str | None = None) -> dict:
    """Run one review pass. Returns the verdict; NEVER returns a mutated provisional answer."""
    prompt = INSTRUCTION.format(
        question=qa["question"],
        answer=qa["answer"],
        sources=_fmt_sources(qa.get("sources") or []),
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
