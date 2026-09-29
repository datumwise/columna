"""
columna_platform.frameql.request — **the Platform-native canonical request form.**

THE AUTHORITY PATH THIS PACKAGE IMPLEMENTS
------------------------------------------
    Frame-QL syntax → Platform request interpretation → family or expression target
                    → MME adjudication → Answer / classified refusal

This module is the SECOND arrow's destination and the boundary of the first. `syntax.py` produces a
`PlatformRequest` and the Frame-QL AST goes no further: **nothing downstream of here has ever seen a
`Statement`**, so no grammar fact can become a semantic one by being carried along.

WHY A SEPARATE REQUEST TYPE AND NOT THE PARSER'S AST
-----------------------------------------------------
The AST is SYNTAX — `series` is verbatim expression text and `anchor` is a tuple of level spellings. A
`PlatformRequest` is the ASK — governed tokens, and a constituent SET resolved inside a universe. The
conversion is where a spelling becomes a governed reference, and having it in one place means there is
exactly one such conversion rather than one per consumer.

**AND IT IS WHERE A CAPABILITY LIMIT IS SAID AS ONE.** Frame-QL's envelope carries `WHERE`, `HAVING`,
`ORDER BY`, `LIMIT`, `WITH` and `FROM`. This serving unit implements none of them, and the difference
between *"this build does not do that yet"* and *"the theory does not permit that"* is the whole of what
a refusal is for. Every unsupported clause therefore refuses with `unsupported-by-this-profile` and names
the clause; nothing is silently ignored, which is the failure mode that makes a query mean something
other than what it says.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


class RequestInterpretationRefusal(Exception):
    """The query is well-formed Frame-QL and this profile cannot interpret it into a governed ask.

    Distinct from a SYNTAX error (the text is not Frame-QL) and from a governed REFUSAL (the ask is
    lawful and the answer is no). Three different things, three different reports — and this one always
    names the clause or spelling that could not be carried, because its remedy is a build rather than a
    correction to the query."""

    def __init__(self, code: str, detail: str, *, clause: Optional[str] = None) -> None:
        super().__init__(f"[{code}] {detail}")
        self.code, self.detail, self.clause = code, detail, clause


@dataclass(frozen=True)
class RequestedSeries:
    """One requested output column: the governed token as written, and the name it answers under.

    `token` is a governed NAME and not an expression. This unit is expression-FIRST in the sense the
    ruling means — a composed expression must be a declared `GovernedExpression` that the request names,
    never an arithmetic tree the serving path assembles — so a series carrying operators is refused
    rather than interpreted. That is a capability boundary and it is stated as one."""

    token: str
    alias: str


@dataclass(frozen=True)
class PlatformRequest:
    """**The canonical request form.** Governed tokens, a constituent set, and nothing syntactic."""

    series: tuple[RequestedSeries, ...]
    #: The OUTPUT anchor's constituents, as a set. `frozenset()` is the grand total — a DECLARED
    #: location, not a missing one, which is what `AT {}` means.
    anchor_constituents: frozenset[str]
    explain: bool
    #: The text this came from, kept for reporting. Never re-parsed and never consulted for meaning.
    source_text: str
    #: The parser's own normalized re-emission. A round-trip witness that the parse caught the
    #: structure — carried so an exhibit can show the syntax→request step rather than assert it.
    canonical_syntax: str

    @property
    def tokens(self) -> tuple[str, ...]:
        return tuple(s.token for s in self.series)

    def render(self) -> str:
        at = "{" + " * ".join(sorted(self.anchor_constituents)) + "}"
        return (f"PlatformRequest(series={[s.token for s in self.series]}, at={at}"
                + (", EXPLAIN" if self.explain else "") + ")")


__all__ = ["PlatformRequest", "RequestInterpretationRefusal", "RequestedSeries"]
