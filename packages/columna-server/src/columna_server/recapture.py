"""
columna_server.demo.recapture — the Cascadia recapture: the seeded corpus, built expectation-first
against the desk's ratified exemplar specification (recapture_exemplar_spec v0.1).

The nine exemplars E1-E9 are the DRIFT-GATE corpus: the seeded-count checks and the site's prose
tripwire bind to exactly this set. Moods, reason codes, and shapes are RATIFIED expectations; numbers
are RECORDED at generation, never asserted. Any deviation is FLAGGED with wire evidence, never
harmonized — recorded in `flags` on the generated corpus.
"""
from __future__ import annotations

from . import tools as T

MANIFOLD = "cascadia"

# (id, ch3 beat caption, query, expected mood, expected reason-or-caveat token). `None` reason = a
# clean serve. The caption text is ratified chapter-3 wording (do not paraphrase).
EXEMPLARS = [
    ("E1", "Priya's serve pair",
     "SELECT revenue, orders AT {region*cal.quarter}", "serve", None),
    ("E2", "The first burn, retried",
     "SELECT stock.sum AT {store*cal.month}", "disclose", "b_anchor_crossing"),
    ("E3", "The remedy taken",
     "SELECT stock.last AT {store*cal.month}", "serve", None),
    ("E4", "The ambiguous ask",
     "SELECT avg(aov) AT {cal.year}", "clarify", "input_anchor_ambiguous"),
    ("E5", "The well-posed sibling",
     "SELECT aov AT {cal.month}", "serve", None),
    ("E6", "The question with its reason attached",
     "SELECT revenue AT {category}", "clarify", "non_functional_transport"),
    ("E7", "The returns question, resolved",
     "SELECT return_rate AT {cal.month}", "serve", None),
    ("E8", "A true refuse (the wheel needs one)",
     "SELECT stock.last AT {customer}", "refuse", "out_of_universe"),   # code recorded at seeding, flagged back
    ("E9", "Check before you run",
     "EXPLAIN SELECT stock.sum AT {store*cal.month}", "disclose", "b_anchor_crossing"),   # would-be mood; kind=explain
]

# The demo --play wheel (four moods, story order): clarify -> refuse -> disclose -> serve.
WHEEL = ["E4", "E8", "E2", "E5"]


def _disclosure_tokens(res: dict):
    """Every disclosure category/severity and any no_result reason surfaced on a wire result."""
    out = []
    for c in res.get("columns", []):
        for dis in (c.get("disclosures") or []):
            out.append({"token": dis.get("category") or dis.get("code"),
                        "severity": dis.get("severity"), "detail": dis.get("detail")})
        nr = c.get("no_result")
        if nr:
            out.append({"token": nr.get("reason"), "severity": None, "detail": nr.get("detail")})
    return out


def _row_count(server, query: str):
    """Recompute the served row count from the core planner (the wire carries mood, not the frame body).
    None for explain/clarify/refuse (no served frame) or when the ask does not resolve."""
    if server is None or query.startswith("EXPLAIN"):
        return None
    try:
        from columna_core.envelope import parse_statement
        r = server.planner.run_statement(parse_statement(query))
        return r.data.height if getattr(r, "data", None) is not None else None
    except Exception:
        return None


def generate(store, server=None) -> dict:
    """Run every exemplar against the live manifold; RECORD mood/reason/shape; FLAG any deviation from
    the ratified expectation with its wire evidence. Returns the seeded corpus (numbers recorded)."""
    corpus, flags = [], []
    for eid, caption, query, exp_mood, exp_reason in EXEMPLARS:
        if query.startswith("EXPLAIN"):
            res = T.explain_statement(store, MANIFOLD, query[len("EXPLAIN"):].strip())
            mood = res.get("outcome")                       # the WOULD-BE mood, touching no data
            tokens = []
            for ser in res.get("series", []):
                for dis in ((ser.get("would_be") or {}).get("disclosures") or []):
                    tokens.append({"token": dis.get("category") or dis.get("code"),
                                   "severity": dis.get("severity"), "detail": dis.get("detail")})
            entry = {"id": eid, "caption": caption, "query": query, "kind": "explain",
                     "mood": mood, "disclosures": tokens}
        else:
            res = T.query(store, MANIFOLD, query)
            mood = res.get("outcome")
            tokens = _disclosure_tokens(res)
            entry = {"id": eid, "caption": caption, "query": query, "kind": "query",
                     "mood": mood, "disclosures": tokens}
        # RECORD: row count for serves/discloses (from the core engine when available)
        entry["row_count"] = _row_count(server, query)
        entry["reason_tokens"] = sorted({t["token"] for t in entry["disclosures"] if t["token"]})
        # FLAG (never harmonize): mood or reason that lands off the ratified expectation
        if mood != exp_mood:
            flags.append({"id": eid, "expected_mood": exp_mood, "recorded_mood": mood, "wire": entry})
        if exp_reason and exp_reason not in entry["reason_tokens"]:
            flags.append({"id": eid, "expected_reason": exp_reason,
                          "recorded_reasons": entry["reason_tokens"], "wire": entry})
        corpus.append(entry)
    return {"manifold": MANIFOLD, "exemplars": corpus, "wheel": WHEEL, "flags": flags}
