"""Deterministic verbatim-quote verification. A mechanical fact, computed mechanically.

WHY THIS IS CODE AND NOT A REVIEW CRITERION (Huayin, 2026-08-26). The reviewer was asked to check
every direct quotation verbatim against the sources. It could not do it reliably: on the Anthropic
comparison it reported that a quoted phrase "cannot be verified from the supplied excerpt" when the
phrase was present in the excerpt it had been handed, and reported the same about four other terms
that were also present. Searching a 24,000-character passage for a literal string is not a judgement
call and should never have been one.

So this module answers only the mechanical question — IS THIS STRING IN THAT TEXT — and hands the
answer to the reviewer as a fact. The reviewer keeps the judgements that are actually judgements:
whether the quotation is used fairly, whether a paraphrase preserves meaning, whether the claim is
bounded. This is deliberately NOT general claim-support verification; literal matching is tractable
and claim support is not, and conflating them would build a machine that quietly decides which
arguments are true.

THREE VERDICTS, AND THE THIRD ONE MATTERS:

    true      the quoted span appears in the cited source under minimal normalisation.
    false     it does not. The answer should paraphrase without quotation marks, or quote an exact
              span. An edited quotation is not a small problem: it puts words in a named party's
              mouth.
    unknown   the evidence is genuinely insufficient — the passage was not preserved, or it was
              truncated and the quote was not found in what survives. Absence in a truncated text
              proves nothing, and reporting it as `false` would be the same overreach this module
              exists to remove.

MINIMAL NORMALISATION, LISTED IN FULL, because every entry is a decision about what counts as the
same sentence: whitespace collapsed; curly quotes, apostrophes and dashes folded to ASCII;
non-breaking spaces folded; case ignored. That is all. NOT normalised away: different words, dropped
clauses, reordered text, and ellipses.

ELLIPSIS IS NEVER SILENTLY VERBATIM. A quote containing "..." is checked fragment by fragment and
reported as `false` with the per-fragment results attached, however well the fragments match.

The Anthropic quote is exactly why, and it drifted in two ways at once: "There's often only a single
correct answer ... with no deterministic way of proving the correctness" elides "using a single
correct source", which carries part of the original point, AND rewrites "in which there's" as
"with". Reading the article by eye I reported that both fragments were findable. They are not: the
first is, the second was reworded. A careful human read caught one of the two drifts; the string
comparison caught both, instantly, which is the whole argument for doing this in code.
"""

from __future__ import annotations

import re
import unicodedata

# A quoted span must look like prose, not a scare-quoted term. Both thresholds are here to stop this
# module reporting on "servability" and "serve with disclosures", which are vocabulary, not quotation.
MIN_QUOTE_CHARS = 30
MIN_QUOTE_WORDS = 5

# How far after a closing quote a citation may sit and still be its attribution. Same line only.
# 300 rather than 160 because a real quotation in this corpus is routinely followed by a clause of
# gloss before the citation arrives — "…required to agree," aiming at plan-independent, canonical
# identity; even for approximate plans … [S2][S1]. At 160 that quotation came back unattributed and
# went unchecked. Widening also pulls in quoted PARAPHRASES sitting next to citations, and that is
# a feature: quotation marks around a sentence the cited source did not write is the same act as
# quoting it wrongly, and the check should say so.
CITE_WINDOW = 300

_QUOTED = re.compile(r'[“"]([^“”"]{%d,})[”"]' % MIN_QUOTE_CHARS)
_CITE = re.compile(r"\[([SX]\d+)\]")
_ELLIPSIS = re.compile(r"\.\.\.|…")

_FOLD = {
    "‘": "'", "’": "'", "‚": "'", "‛": "'",
    "“": '"', "”": '"', "„": '"', "‟": '"',
    "–": "-", "—": "-", "−": "-", " ": " ",
}


def normalise(s: str) -> str:
    """Whitespace, quote/dash/apostrophe shape, and case. Nothing else."""
    s = unicodedata.normalize("NFKC", s)
    s = "".join(_FOLD.get(ch, ch) for ch in s)
    return re.sub(r"\s+", " ", s).strip().lower()


def extract(answer: str) -> list[dict]:
    """Direct quotations in the answer, with the citations attached to them."""
    out = []
    for m in _QUOTED.finditer(answer):
        text = m.group(1).strip()
        if len(text.split()) < MIN_QUOTE_WORDS:
            continue
        # ATTRIBUTION STOPS AT THE LINE. The window used to run on past a newline and pick up the
        # citation belonging to the NEXT bullet, which attributed a datumwise quotation to the
        # Anthropic article. A quotation and its citation live in the same sentence or not at all.
        after = answer[m.end(): m.end() + CITE_WINDOW].split("\n")[0]
        before = answer[max(0, m.start() - CITE_WINDOW): m.start()].rsplit("\n", 1)[-1]
        cites = _CITE.findall(after) or _CITE.findall(before)
        out.append({"quote": text, "cites": list(dict.fromkeys(cites)),
                    "hasEllipsis": bool(_ELLIPSIS.search(text))})
    return out


_TRAILING = " .,;:"


def _find(needle: str, haystacks: dict[str, str]) -> tuple[list[str], bool]:
    """(where it was found, whether terminal punctuation had to be ignored to find it).

    A quotation's LAST character is usually the host sentence's punctuation rather than the source's
    word: an answer writing `"... required to agree," aiming at ...` has spliced a comma where the
    paper had a full stop. Treating that as an edited quotation would be pedantry that buries the
    real findings, so a terminal-punctuation-only difference matches — and is REPORTED as such,
    which is the difference between a minimal normalisation and a silent one. Internal punctuation
    is never touched.
    """
    n = normalise(needle)
    if not n:
        return [], False
    exact = [cite for cite, text in haystacks.items() if n in text]
    if exact:
        return exact, False
    trimmed = n.rstrip(_TRAILING)
    if trimmed != n and trimmed:
        loose = [cite for cite, text in haystacks.items() if trimmed in text]
        if loose:
            return loose, True
    return [], False


def verify(answer: str, evidence: list[dict]) -> list[dict]:
    """One verification fact per direct quotation. Never a judgement — only presence or absence."""
    texts = {e["cite"]: normalise(e.get("text") or "") for e in evidence if e.get("cite")}
    truncated = {e["cite"] for e in evidence if e.get("truncated")}
    facts = []
    for q in extract(answer):
        # A QUOTED PHRASE WITH NO CITATION IS NOT AN ATTRIBUTED QUOTATION. Answers use quotation
        # marks for their own framing too — "find the right tables and write SQL" is the writer
        # contrasting two postures, not reporting what anyone said. Searching the corpus for it and
        # reporting NOT VERBATIM would manufacture a finding out of ordinary prose, and the reviewer
        # would have no way to tell that finding from a real one.
        if not q["cites"]:
            facts.append({**q, "verbatimMatch": None, "attributed": False,
                          "reason": "no citation attached — treat as the answer's own phrasing "
                                    "unless it reads as a quotation, in which case it needs one"})
            continue
        scope = {c: texts[c] for c in q["cites"] if c in texts}
        missing_evidence = not scope or all(not t for t in scope.values())

        if q["hasEllipsis"]:
            # Checked, reported, and never called verbatim — see the module docstring.
            frags = [f.strip(" ,;:") for f in _ELLIPSIS.split(q["quote"]) if f.strip(" ,;:")]
            results = [{"text": f, "foundIn": _find(f, scope)[0]} for f in frags]
            all_found = all(r["foundIn"] for r in results)
            facts.append({
                **q, "verbatimMatch": False, "fragments": results,
                "reason": ("ellipsis-compressed: every fragment is present, but the compressed "
                           "sentence is not what the source says" if all_found else
                           "ellipsis-compressed, and not every fragment is present"),
            })
            continue

        found, loose = _find(q["quote"], scope)
        if found:
            facts.append({**q, "verbatimMatch": True, "foundIn": found,
                          "reason": ("exact match, except the quotation's terminal punctuation, "
                                     "which belongs to the sentence hosting it" if loose
                                     else "exact match")})
        elif missing_evidence or (set(scope) & truncated):
            facts.append({**q, "verbatimMatch": None,
                          "reason": ("the cited source's text was not preserved" if missing_evidence
                                     else "not found, but the cited source is truncated — absence "
                                          "in a truncated text proves nothing")})
        else:
            facts.append({**q, "verbatimMatch": False,
                          "reason": "not present in the cited source under minimal normalisation"})
    return facts


def format_facts(facts: list[dict]) -> str:
    """The block handed to the reviewer. Says what was checked, so silence is not mistaken for OK."""
    if not facts:
        return ("  (no direct quotations of 5+ words were found in this answer, so there is nothing "
                "for this check to report)")
    lines = []
    for f in facts:
        verdict = {True: "VERBATIM MATCH", False: "NOT VERBATIM",
                   None: "UNKNOWN"}[f["verbatimMatch"]]
        if f.get("attributed") is False:
            verdict = "UNATTRIBUTED"
        cites = ", ".join(f["cites"]) or "(no citation attached)"
        lines.append(f'  {verdict} — attributed to {cites}\n'
                     f'    quoted: "{f["quote"]}"\n'
                     f'    fact:   {f["reason"]}')
        for fr in f.get("fragments", []):
            where = ", ".join(fr["foundIn"]) or "not found"
            lines.append(f'      fragment {fr["text"][:70]!r}: {where}')
    return "\n".join(lines)
