"""The ask pipeline: retrieve -> constitute -> call -> verify -> record.

Model selection is a parameter and appears nowhere in the logic, per the brief. Every step is
inspectable and no step silently repairs another's output.
"""

from __future__ import annotations

import json
import re

from . import providers, retrieve, standing, store, verify
from .skill import build_prompt

# The public/private rule, kept as small and conservative as the brief asks. This decides whether a
# successfully-answered question becomes a PUBLIC cached Q&A. It is not moderation of the answer —
# the reader always gets their answer — it is a decision about republication to strangers.
_PRIVATE_SIGNALS = [
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"), "contains an email address"),
    (re.compile(r"\b(?:\+?\d[\d\s().-]{7,}\d)\b"), "contains what looks like a phone number"),
    (re.compile(r"\b(?:sk-|ghp_|xox[baprs]-|AKIA)[A-Za-z0-9_-]{8,}"), "contains what looks like a credential"),
    (re.compile(r"\b(my|our|we|i)\s+(company|employer|team|client|boss|manager|startup)\b", re.I),
     "appears to describe the asker's own organisation"),
    (re.compile(r"\b(my name is|i am called|i work at|i work for)\b", re.I), "identifies the asker"),
]
_ABUSE = re.compile(r"\b(fuck|shit|cunt|bitch|retard|nigg|faggot)\w*\b", re.I)


def publishability(question: str) -> tuple[bool, str | None]:
    """ELIGIBILITY FOR REVIEW, not for publication (renamed in meaning, 2026-08-26).

    This filter used to decide whether a fresh answer entered the public Q&A collection. It now
    decides something narrower: whether an answer may be put in front of a reviewer at all. A
    private-looking or abusive question should never reach a human's queue; everything that passes
    is a CANDIDATE, and publication is an act a person performs afterwards.

    Conservative and dumb on purpose. Not a moderation research project (brief's words).
    """
    q = question.strip()
    if len(q) < 8:
        return False, "too short to be a useful public question"
    if len(q) > 600:
        return False, "too long to be a useful public question"
    if _ABUSE.search(q):
        return False, "contains abusive language"
    for pat, why in _PRIVATE_SIGNALS:
        if pat.search(q):
            return False, why
    return True, None


# OBSERVED FAILURE, 2026-08-25, and the reason this is two patterns and not one.
#
# The constitution asks the model to close with a ```json fenced block. On the very first
# edition-pinned question asked through the live service, gpt-5 closed with the JSON object and NO
# FENCE. The fenced-only regex missed it, `used` came back empty, and an otherwise excellent answer
# — it correctly said "the route renders v1.1; the current record is v1.2" — was published with ZERO
# source receipts. An answer without receipts defeats the entire point of Ask.
#
# The lesson is not "write a sterner instruction". It is that an output CONTRACT enforced only by
# instruction is the brittle joint, and the repair belongs in the parser: accept both shapes, and
# then stop depending on the block at all (see _resolve_used below).
_JSON_TAIL = re.compile(r"(?:```(?:json)?\s*)?(\{[^{}]*\"used\".*?\})\s*(?:```)?\s*$", re.S)
_INLINE_CITE = re.compile(r"\[(S\d+)\]")


def _split_answer(text: str) -> tuple[str, dict]:
    """Peel the trailing JSON block off, fenced or bare. Report failure rather than guessing."""
    m = _JSON_TAIL.search(text.strip())
    if not m:
        return text.strip(), {"used": [], "external": [], "corpus_settles": None, "_missing": True}
    body = text[: m.start()].strip()
    try:
        return body, json.loads(m.group(1))
    except json.JSONDecodeError:
        return body, {"used": [], "external": [], "corpus_settles": None, "_malformed": True}


def _resolve_used(body: str, meta: dict) -> tuple[list[str], bool]:
    """Which source tokens did the answer actually use?

    THE BLOCK IS THE HINT; THE PROSE IS THE EVIDENCE. `meta["used"]` is what the model SAID it used.
    The inline [S#] markers are what it actually attached to claims, in the text a reader will read.
    We take the union, because either one alone loses receipts:
      · block-only loses everything when the format drifts (the failure above);
      · prose-only loses a source the model leaned on without marking a specific sentence.
    Returns (tokens, recovered) where `recovered` records that the prose rescued citations the
    block did not carry — worth logging, because it is a signal about the output contract.
    """
    declared = [t for t in (meta.get("used") or []) if isinstance(t, str)]
    inline = _INLINE_CITE.findall(body)
    union = sorted(set(declared) | set(inline), key=lambda t: int(t[1:]))
    return union, bool(inline) and not declared


def ask(
    question: str,
    model: str | None = None,
    k: int = 8,
    history: list[dict] | None = None,
    use_cache: bool = True,
) -> dict:
    """Answer one question. Returns everything needed to display, store, and audit it."""
    if use_cache and not history:
        cached = store.find_cached(question)
        if cached:
            return {**cached, "cached": True}

    passages = retrieve.search(question, k=k)
    messages = build_prompt(question, passages, history=history)
    comp = providers.complete(messages, model=model)
    body, meta = _split_answer(comp.text)

    # Map the model's [S#] tokens back to real sources. A token it did not receive is dropped, not
    # invented into a citation — and the drop is recorded.
    by_token = {f"S{i}": p for i, p in enumerate(passages, 1)}
    all_used, recovered = _resolve_used(body, meta)
    used_tokens = [t for t in all_used if t in by_token]
    phantom = [t for t in all_used if t not in by_token]
    sources = [
        {
            "cite": t,
            "label": by_token[t].get("sourceLabel") or by_token[t]["title"],
            "heading": by_token[t]["heading"],
            "url": by_token[t]["url"],
            "route": by_token[t]["route"],
            "role": by_token[t].get("role"),
            # The ENTITLEMENT travels with the citation. The reviewer's first job is deciding
            # whether a datumwise-position claim rests on a Core source, and it cannot do that
            # from a source list that does not say which class each source belongs to.
            "layer": by_token[t].get("layer"),
            "jurisdiction": by_token[t].get("jurisdiction"),
            "standing": by_token[t]["standing"],
            "isHistorical": by_token[t]["isHistorical"],
            "isEditionPinned": by_token[t]["isEditionPinned"],
        }
        for t in used_tokens
    ]

    v = verify.check(body)
    if _INLINE_CITE.search(body) and not sources:
        # Cited in the prose, resolved to nothing. Whatever the cause, the reader would be shown
        # citation markers with no sources behind them. Never publish that.
        v = {**v, "problems": v["problems"] + [{
            "kind": "unresolved-citations",
            "value": ",".join(sorted(set(_INLINE_CITE.findall(body)))),
            "detail": "the answer cites source tokens that resolved to no source",
        }], "ok": False, "fatal": v["fatal"] + 1}
    if phantom:
        v = {**v, "problems": v["problems"] + [
            {"kind": "phantom-citation", "value": t,
             "detail": "cited a source token that was not supplied"} for t in phantom
        ], "ok": False, "fatal": v["fatal"] + len(phantom)}

    return {
        "question": question,
        "answer": body,
        "sources": sources,
        "external": meta.get("external") or [],
        "corpusSettles": meta.get("corpus_settles"),
        "retrieved": [
            {"cite": f"S{i}", "label": p.get("sourceLabel") or p["title"], "heading": p["heading"],
             "url": p["url"], "score": p["score"], "standing": p["standing"]}
            for i, p in enumerate(passages, 1)
        ],
        "verify": v,
        "provider": comp.provider,
        "model": f"{comp.provider}:{comp.model}",
        "promptTokens": comp.prompt_tokens,
        "completionTokens": comp.completion_tokens,
        "costUsd": comp.cost_usd,
        "cached": False,
        "metaMissing": bool(meta.get("_missing") or meta.get("_malformed")),
        "citationsRecoveredFromProse": recovered,
    }


def ask_and_record(question: str, conversation: str, model: str | None = None,
                   history: list[dict] | None = None, parent_id: str | None = None) -> dict:
    """Answer, log the turn, and record it as a PROVISIONAL candidate.

    Nothing here publishes. Until 2026-08-26 a fresh answer that passed the privacy filter entered
    the public collection immediately; now it is stored provisional and unpublished, and the same
    filter decides only whether it is eligible to reach a reviewer.
    """
    res = ask(question, model=model, history=history, use_cache=not history)

    if res.get("cached"):
        # Technical reuse. No view bump: views belong to a published object, and a reused
        # provisional answer is not one. See standing.py.
        store.get(res["id"])
        store.log_turn(conversation=conversation, qa_id=res["id"], question=question,
                       answer=res["answer"], sources=res["sources"], external=res["external"],
                       provider=res["provider"], model=res["model"], cached=True,
                       corpus_settles=res.get("corpusSettles", True))
        return {**res, "standing": res.get("standing", standing.PROVISIONAL),
                "notice": standing.notice(res.get("standing", standing.PROVISIONAL),
                                          res.get("notice", {}).get("reviewedAt"))}

    reviewable, why = publishability(question)
    # An answer that failed the identifier gate does not go to a reviewer. The asker still sees it —
    # with the failure attached — because hiding it would destroy the evidence.
    if reviewable and not res["verify"]["ok"]:
        reviewable, why = False, "failed the source-identifier check"
    # A follow-up in a conversation is context-dependent by construction; it does not stand alone as
    # a public Q&A, so it is not a review candidate either.
    if history:
        reviewable, why = False, "follow-up turn: only meaningful inside its conversation"

    qa_id = store.save_qa(
        question=question, answer=res["answer"], provider=res["provider"], model=res["model"],
        sources=res["sources"], external=res["external"],
        corpus_settles=bool(res.get("corpusSettles", True)), public=reviewable,
        withheld_reason=why, verify=res["verify"], prompt_tokens=res["promptTokens"],
        completion_tokens=res["completionTokens"], cost_usd=res["costUsd"], parent_id=parent_id,
    )
    # Remember it for cheap reuse. A cache entry is not a publication and does not imply one; it
    # expires on its own schedule and carries no reputation. Follow-ups are never cached: they only
    # mean anything inside their conversation.
    if not history:
        store.cache_put(question, qa_id, res["model"])
    store.log_turn(conversation=conversation, qa_id=qa_id, question=question, answer=res["answer"],
                   sources=res["sources"], external=res["external"], provider=res["provider"],
                   model=res["model"], cached=False,
                   corpus_settles=bool(res.get("corpusSettles", True)), verify=res["verify"],
                   prompt_tokens=res["promptTokens"], completion_tokens=res["completionTokens"],
                   cost_usd=res["costUsd"])
    # No view bump on creation. Views are a property of a published object, and nothing is
    # published here.
    return {**res, "id": qa_id, "standing": standing.PROVISIONAL,
            "notice": standing.notice(standing.PROVISIONAL),
            "reviewEligible": reviewable, "withheldReason": why}
