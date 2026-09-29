"""
columna_platform.frameql.syntax — **the ONE place Frame-QL syntax enters Platform.**

THE LIFT, AND WHY IT IS AN IMPORT RATHER THAN A COPY
-----------------------------------------------------
Ruled (Huayin, 2026-09-28): *"Reuse/lift the existing Frame-QL parser as SYNTAX ONLY. Do not import Core
analytical semantics, planner law, family/member model, generated-family doctrine, or Core Operator
Registry. Prefer the smallest clean way to bring the stable parser/envelope grammar into Platform without
creating a runtime semantic dependency on `columna_core`. Do not redesign Frame-QL grammar in this unit."*

`columna_core.envelope` is **provably syntax**: its own imports are `re`, `dataclasses` and `typing`, and
`import columna_core.envelope` pulls in exactly TWO modules — the package's lazy `__init__` (whose only
imports are `importlib` and `typing`) and the parser itself. **No Core semantic module is reachable from
it.** `test_frameql_serving.py` measures that closure rather than trusting this paragraph, so the day
someone adds a semantic import to the envelope, this claim fails loudly instead of quietly becoming
false.

So the lift is an IMPORT, and that is the smallest clean way: a 443-line copy would be a second grammar
free to drift from the first, which is the opposite of *"do not redesign Frame-QL grammar in this unit."*
There is one grammar, it lives where it already lives, and Platform reads it as text-shaped input.

**THE AST STOPS HERE.** This module is the only one in Platform that may import the envelope or mention a
`Statement`, and it converts to a `PlatformRequest` before returning. Everything downstream — resolution,
adjudication, serving — has never seen a syntax object, so a grammar fact cannot become a semantic one by
being carried along. A test pins the isolation.

WHAT IS INTERPRETED, AND WHAT IS REFUSED AS A CAPABILITY LIMIT
--------------------------------------------------------------
Interpreted: `SELECT <token> [AS <alias>] [, …]`, `AT { <constituents> }`, `EXPLAIN`.
Refused, each by name: `WHERE`, `HAVING`, `ORDER BY`, `LIMIT`, `WITH`, `FROM`, a dotted anchor level, and
a series carrying expression syntax. **Nothing is silently dropped** — a clause ignored rather than
refused makes a query mean something other than what it says, which is the one failure this boundary
exists to prevent.
"""
from __future__ import annotations

from typing import Optional

# THE ONE CORE IMPORT IN PLATFORM'S v8-NATIVE PATH, AND IT IS A GRAMMAR. See the module note; its import
# closure is measured by a test. Nothing else in `columna_platform.frameql` or
# `columna_platform.kernel` imports `columna_core` at all.
from columna_core.envelope import EnvelopeSyntaxError, Statement, parse_statement

from .request import PlatformRequest, RequestInterpretationRefusal, RequestedSeries

#: Envelope clauses this serving profile does not implement, and what each would need. Named
#: individually because "unsupported" without a subject is not a remedy.
_UNSUPPORTED = (
    ("where", "where",
     "per-series predicates restrict PARTICIPATION before reduction, which is a governed fact about a "
     "family's constitution rather than a filter this path may apply to a retained state"),
    ("having", "having",
     "output-frame predicates apply after reduction and need a frame algebra this unit does not build"),
    ("order_by", "order by", "output-frame ordering needs a frame algebra this unit does not build"),
    ("limit", "limit", "truncation needs a frame algebra this unit does not build"),
    ("bindings", "with",
     "macro bindings substitute expression TEXT before interpretation; this profile is expression-FIRST "
     "and resolves declared governed expressions by name, so there is nothing here for a textual "
     "substitution to produce"),
    ("from_manifold", "from",
     "this profile serves one constituted universe held by the engine it was given; selecting among "
     "several is a constitution question and there is no publication layer yet"),
)

#: Characters that make a series something other than a governed NAME. Expression-first: a composition
#: must be a DECLARED `GovernedExpression` the request names, never a tree this path assembles.
_EXPRESSION_CHARS = set("+-*/%()@{}[]<>=!,:'\"")


def parse(text: str) -> Statement:
    """The grammar, unmodified. Exposed so a test can show the syntax layer is not being reimplemented."""
    return parse_statement(text)


def interpret(text: str, *, universe_references: Optional[frozenset[str]] = None) -> PlatformRequest:
    """**Frame-QL text → `PlatformRequest`.** Syntax in, governed ask out, and the AST does not escape.

    `universe_references` is the constituent vocabulary to check `AT {…}` against. Passing it lets an
    unknown coordinate be reported HERE, where the query text is still in hand and the message can quote
    it, rather than at the geometry, which correctly refuses but cannot say which clause asked."""
    statement = parse_statement(text)

    for attribute, clause, why in _UNSUPPORTED:
        value = getattr(statement, attribute)
        if value:
            raise RequestInterpretationRefusal(
                "unsupported-by-this-profile",
                f"the query uses {clause.upper()!r}, which this serving profile does not implement: "
                f"{why}. **This is a CAPABILITY limit, not a governed one** — the clause is lawful "
                f"Frame-QL and the remedy is a build, not a correction to the query.",
                clause=clause)

    series: list[RequestedSeries] = []
    for s in statement.series:
        token = s.expr.strip()
        if not token:
            raise RequestInterpretationRefusal("empty-series", "a SELECT series names nothing.")
        offending = sorted(set(token) & _EXPRESSION_CHARS)
        if offending or " " in token:
            raise RequestInterpretationRefusal(
                "expression-text-in-series",
                f"series {token!r} carries expression syntax {offending or ['whitespace']}. This "
                f"profile is EXPRESSION-FIRST: a composed quantity is served by naming a DECLARED "
                f"governed expression, never by assembling an arithmetic tree over retained states. "
                f"Declare the composition as a governed expression and select it by name.",
                clause="select")
        if "." in token:
            raise RequestInterpretationRefusal(
                "dotted-series-token",
                f"series {token!r} is a dotted path. Dotted access is one shape in the grammar and its "
                f"meaning is a per-context semantic check; this profile resolves a governed name to an "
                f"analytical SORT and has no value-access model to apply a suffix with.",
                clause="select")
        series.append(RequestedSeries(token=token, alias=s.alias or token))

    constituents: list[str] = []
    for level in statement.anchor:
        if "." in level:
            raise RequestInterpretationRefusal(
                "dotted-anchor-level",
                f"anchor level {level!r} is dotted. A Platform anchor is a set of a universe's governed "
                f"CONSTITUENTS; there is no hierarchy or dimension-level model here for a prefix to "
                f"name, and inventing one would make the geometry a function of a spelling.",
                clause="at")
        if universe_references is not None and level not in universe_references:
            raise RequestInterpretationRefusal(
                "unknown-anchor-constituent",
                f"anchor level {level!r} is not a governed constituent of the universe this engine holds "
                f"(it carries {sorted(universe_references)}). Resolution is universe-scoped: a reference "
                f"that resolves elsewhere does not resolve here.",
                clause="at")
        constituents.append(level)
    if len(set(constituents)) != len(constituents):
        dupes = sorted({c for c in constituents if constituents.count(c) > 1})
        raise RequestInterpretationRefusal(
            "repeated-anchor-constituent",
            f"AT names {dupes} more than once. An anchor is a SET of constituents; repeating a member "
            f"states nothing further and hides a typo.", clause="at")

    return PlatformRequest(
        series=tuple(series),
        anchor_constituents=frozenset(constituents),
        explain=statement.explain,
        source_text=text.strip(),
        canonical_syntax=statement.render_canonical(),
    )


__all__ = ["EnvelopeSyntaxError", "interpret", "parse"]
