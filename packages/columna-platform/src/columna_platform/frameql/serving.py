"""
columna_platform.frameql.serving — **the authority path, end to end.**

    Frame-QL syntax  →  Platform request interpretation  →  family or expression target
                     →  MME adjudication  →  Answer / classified refusal

THE RESOLUTION RULE, AND THE ONE THING IT MUST NOT DO
------------------------------------------------------
Ruled (Huayin, 2026-09-28): *"A name must resolve by analytical sort: family → family path; governed
expression → expression path; unknown → unresolved/refusal. Do not widen `AnalyticalIdentity` from the old
estate. Use the kernel's native family/expression types."*

So resolution asks `MME.sort_of(token)` — **one question, before the call** — and dispatches to
`measure` or `evaluate`. It never holds a family in a variable typed for an expression, and there is no
widened identity type anywhere in this package: the kernel's `FamilyPoint` and `ExpressionPoint` are
peers, and the dispatch happens before either exists.

**AND AN UNKNOWN NAME IS UNRESOLVED, NEVER "NO FAMILY ANSWERS TO IT".** That distinction is the defect
V8-0 found at Core's C7 seam and V8-1 found at its family lookup: a capability limit reported as a
governed absence sends a steward to correct a publication that is correct. Three separate classifications
keep them apart — `UNRESOLVED` (the engine holds no such governed object), `REFUSE` (the object exists and
the answer is no), `UNSUPPORTED` (the query is lawful and this build does not implement it).

WHY A FRAME AND NOT A VALUE
---------------------------
Frame-QL selects several series at ONE output anchor, so the answer is a frame: the anchor's cells down,
the requested series across. Each series is served INDEPENDENTLY through the kernel — a family through
continuation, an expression through its basis — and the frame is assembled afterwards. **If any series
refuses, the whole request refuses**, naming which one: a frame with a missing column is not a frame, and
serving the rest would hand back something that looks like an answer to the question that was asked.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from columna_platform.kernel import (
    STRUCTURED,
    Anchor,
    Disclosure,
    KernelRefusal,
    MME,
    Refusal,
)
from columna_platform.kernel.value import Answer

from .request import PlatformRequest, RequestInterpretationRefusal
from .syntax import EnvelopeSyntaxError, interpret

# ── the four classified outcomes, plus the syntax one ────────────────────────────────────────────
SERVE = "serve"              # an answer, with nothing further to say about it
DISCLOSE = "disclose"        # an answer that carries a standing the caller must not drop
REFUSE = "refuse"            # the object exists, the ask is lawful, and the answer is NO
UNRESOLVED = "unresolved"    # this engine holds no governed object under that name
UNSUPPORTED = "unsupported"  # lawful Frame-QL this build does not implement
SYNTAX = "syntax"            # the text is not Frame-QL
CLASSIFICATIONS = (SERVE, DISCLOSE, REFUSE, UNRESOLVED, UNSUPPORTED, SYNTAX)


@dataclass(frozen=True)
class Column:
    """One served series, and the authority by which it was served."""

    alias: str
    token: str
    #: `"family"` or `"expression"`. The resolved analytical SORT, reported because it is the fact that
    #: decided which path ran.
    sort: str
    #: The kernel route: `root` / `cached` / `continued` / `evaluated`.
    route: str
    #: For a continued family: the retained state it was seeded from. For an expression: the basis id.
    via: Optional[str] = None
    disclosures: tuple[Disclosure, ...] = ()


@dataclass(frozen=True)
class Frame:
    """The served answer: the output anchor's cells down, the requested series across."""

    anchor: Anchor
    coordinates: tuple[str, ...]
    columns: tuple[Column, ...]
    rows: tuple[tuple, ...]

    def render(self) -> str:
        head = list(self.coordinates) + [c.alias for c in self.columns]
        widths = [max(len(str(h)), *(len(_fmt(r[i])) for r in self.rows)) if self.rows else len(str(h))
                  for i, h in enumerate(head)]
        lines = ["  ".join(str(h).ljust(w) for h, w in zip(head, widths))]
        lines.append("  ".join("─" * w for w in widths))
        for row in self.rows:
            lines.append("  ".join(_fmt(v).ljust(w) for v, w in zip(row, widths)))
        return "\n".join(lines)


#: Value forms a frame can DISPLAY. Anything else is rendered opaquely — see `_fmt`.
_DISPLAYABLE = (int, float, str, bool, type(None))


def _fmt(value: Any) -> str:
    """**A STRUCTURED FAMILY VALUE HAS NO DISPLAY FORM, AND THE FRAME SAYS SO RATHER THAN IMPROVISING
    ONE.**

    This is not cosmetic. A continuation-bearing structured value — an HLL sketch — is the family's
    state; the number a human wants from it is produced by a FINALIZATION, which is a governed
    EXPRESSION with its own standing. `str()` on the sketch happens to emit a debug summary containing an
    `Estimate:` line, so rendering it naively would print a cardinality **through the family path**,
    bypassing the expression that is the only lawful way to obtain one. The frame would then show, in a
    column labelled with the family's name, a number that is the expression's answer.

    So a non-displayable payload renders as an opaque marker. The value is intact and served; what the
    frame declines to do is pretend it is a scalar."""
    if isinstance(value, float):
        return f"{value:.4f}"
    if isinstance(value, _DISPLAYABLE):
        return str(value)
    return f"⟨{type(value).__name__}⟩"


@dataclass(frozen=True)
class Outcome:
    """**A TOTAL serving verdict over a Frame-QL query.** Never silence, and never an exception
    escaping to the caller as the answer."""

    classification: str
    query: str
    request: Optional[PlatformRequest] = None
    frame: Optional[Frame] = None
    refusal: Optional[Refusal] = None
    #: The resolved sorts, per series token. Reported even on a refusal, because *which sort a name
    #: resolved to* is usually the fact that explains the refusal.
    sorts: dict = field(default_factory=dict)
    plan: tuple[str, ...] = ()

    @property
    def served(self) -> bool:
        return self.classification in (SERVE, DISCLOSE)

    @property
    def disclosures(self) -> tuple[Disclosure, ...]:
        return tuple(d for c in (self.frame.columns if self.frame else ()) for d in c.disclosures)

    def render(self) -> str:
        out = [f"$ {self.query}"]
        if self.request is not None:
            out.append(f"  request   {self.request.render()}")
        if self.sorts:
            out.append("  resolved  " + ", ".join(f"{k} → {v}" for k, v in self.sorts.items()))
        out.append(f"  outcome   {self.classification.upper()}")
        if self.frame is not None:
            for c in self.frame.columns:
                out.append(f"  authority {c.alias}: {c.sort} · route={c.route}"
                           + (f" · via {c.via}" if c.via else ""))
            out.append("")
            out.append("\n".join("    " + line for line in self.frame.render().splitlines()))
        for d in self.disclosures:
            out.append(f"  ⚠ {d.code}: {d.detail}")
        if self.refusal is not None:
            out.append(f"  refusal   [{self.refusal.code}] {self.refusal.detail}")
        for step in self.plan:
            out.append(f"  plan      {step}")
        return "\n".join(out)


class FrameQLService:
    """**The serving path.** One constituted MME, and Frame-QL text in."""

    def __init__(self, mme: MME) -> None:
        self.mme = mme

    # ── the whole path ───────────────────────────────────────────────────────────────────────
    def serve(self, query: str) -> Outcome:
        try:
            request = interpret(query, universe_references=self.mme.universe.references)
        except EnvelopeSyntaxError as exc:
            return Outcome(SYNTAX, query,
                           refusal=Refusal("frameql_syntax", query, str(exc)))
        except RequestInterpretationRefusal as exc:
            return Outcome(UNSUPPORTED, query,
                           refusal=Refusal(exc.code, exc.clause or query, exc.detail))

        # ── RESOLUTION BY SORT. One question per token, asked before anything is served. ──────
        sorts: dict[str, Optional[str]] = {s.token: self.mme.sort_of(s.token) for s in request.series}
        unknown = [t for t, sort in sorts.items() if sort is None]
        if unknown:
            return Outcome(
                UNRESOLVED, query, request=request, sorts=sorts,
                refusal=Refusal(
                    "unresolved-reference", ", ".join(unknown),
                    f"this engine holds no governed analytical object under {unknown}. It holds "
                    f"families {sorted(self.mme.families)} and governed expressions "
                    f"{sorted(self.mme.expressions)}. **NOTE WHAT THIS IS NOT**: it is not a claim that "
                    f"no FAMILY answers to the name — that would send a steward to correct a "
                    f"constitution which may be perfectly correct. The name resolves to no sort at all, "
                    f"and no near match is guessed."))

        anchor = self.mme.universe.anchor(request.anchor_constituents)

        if request.explain:
            return self._explain(query, request, sorts, anchor)

        answers: dict[str, Answer] = {}
        for s in request.series:
            try:
                answer = self._serve_one(s.token, sorts[s.token], anchor)
            except KernelRefusal as exc:
                # A REALIZATION limit reaches here as an exception because it is not a governed verdict
                # about the ask — the law is intact and this build cannot execute it.
                return Outcome(UNSUPPORTED, query, request=request, sorts=sorts,
                               refusal=Refusal(exc.code, exc.subject, exc.detail))
            if not answer.served:
                return Outcome(REFUSE, query, request=request, sorts=sorts,
                               refusal=Refusal(answer.refusal.code, answer.refusal.subject,
                                               f"series {s.alias!r}: {answer.refusal.detail}"))
            answers[s.alias] = answer

        frame = self._frame(request, anchor, sorts, answers)
        classification = DISCLOSE if any(c.disclosures for c in frame.columns) else SERVE
        return Outcome(classification, query, request=request, frame=frame, sorts=sorts)

    # ── the two paths, chosen by SORT and never by inspection of what came back ───────────────
    def _serve_one(self, token: str, sort: str, anchor: Anchor) -> Answer:
        if sort == "family":
            return self.mme.measure(self.mme.family(token), anchor)
        return self.mme.evaluate(self.mme.expression(token), anchor)

    def _frame(self, request: PlatformRequest, anchor: Anchor, sorts: dict,
               answers: dict) -> Frame:
        keys: set[tuple] = set()
        for answer in answers.values():
            keys |= set(answer.value.cells)
        columns = []
        for s in request.series:
            answer = answers[s.alias]
            via = (str(answer.seeded_from) if answer.seeded_from is not None else None)
            disclosures = tuple(answer.disclosures)
            # **A STRUCTURED FAMILY VALUE IS SERVED WITH THE FACT THAT IT IS NOT A DISPLAY VALUE.** The
            # caller asked for the family and gets the family's state, which is the right answer; what it
            # must not do is read a number out of it. The law names its finalization, so the disclosure
            # can name the governed expression that IS the lawful way to obtain one.
            if sorts[s.token] == "family":
                law = self.mme.law_of(s.token)
                if law.value_form == STRUCTURED:
                    disclosures += (Disclosure(
                        "structured-family-value",
                        f"{s.alias!r} is a CONTINUATION-BEARING STRUCTURED value ({law.name}) and has no "
                        f"display form. It is the family's state, it merges, and it is not a number. The "
                        f"lawful way to obtain a displayable result is the finalization "
                        f"{law.finalized_by!r} — a governed EXPRESSION, whose result in turn cannot seed "
                        f"family continuation."),)
            columns.append(Column(alias=s.alias, token=s.token, sort=sorts[s.token],
                                  route=answer.route, via=via, disclosures=disclosures))
        rows = []
        for key in sorted(keys, key=lambda k: tuple(map(str, k))):
            row = list(key)
            for s in request.series:
                # A cell absent from ONE series is reported as absent rather than as zero: §4.3's
                # undefined-on-basis case is a governed standing and a 0 would be a value the theory
                # does not license here.
                row.append(answers[s.alias].value.cells.get(key, "—"))
            rows.append(tuple(row))
        return Frame(anchor=anchor, coordinates=anchor.order, columns=tuple(columns), rows=tuple(rows))

    # ── EXPLAIN · the authority path, WITHOUT serving ─────────────────────────────────────────
    def _explain(self, query: str, request: PlatformRequest, sorts: dict, anchor: Anchor) -> Outcome:
        """**Reports the path and does not execute it.** Cheap, and it is the thing that makes the
        authority path inspectable rather than merely claimed: a reader can see which sort a name
        resolved to, which kernel entry point that selects, and — for a family — which retained states
        are candidates and what the adjudication says about each."""
        plan = [f"syntax    → {request.canonical_syntax.replace(chr(10), ' ; ')}",
                f"request   → {request.render()}",
                f"anchor    → {anchor}"]
        for s in request.series:
            sort = sorts[s.token]
            if sort == "family":
                family = self.mme.family(s.token)
                plan.append(f"{s.token}: FAMILY, R_F={family.root}, law={family.law} "
                            f"→ MME.measure()")
                for candidate in self.mme.candidates(family):
                    verdict = self.mme.adjudicate(candidate, family, anchor)
                    plan.append(f"    candidate {candidate.key} → "
                                + ("ADMITTED" if verdict else f"REFUSED [{verdict.code}]"))
            else:
                expression = self.mme.expression(s.token)
                plan.append(f"{s.token}: GOVERNED EXPRESSION, constructor={expression.constructor} "
                            f"→ MME.evaluate()")
                for basis in expression.admitted_bases:
                    roles = ", ".join(f"{r}→{f}" for r, f in sorted(basis.components.items()))
                    plan.append(f"    basis {basis.basis_id}: {roles}"
                                + (" (requires common participation)"
                                   if basis.requires_common_participation else ""))
                if not expression.admitted_bases:
                    plan.append("    no admitted basis: well-formed and not evaluable")
        plan.append("NOT EXECUTED — EXPLAIN reports the authority path and serves nothing.")
        return Outcome(SERVE, query, request=request, sorts=sorts, plan=tuple(plan))


__all__ = ["CLASSIFICATIONS", "Column", "DISCLOSE", "Frame", "FrameQLService", "Outcome", "REFUSE",
           "SERVE", "SYNTAX", "UNRESOLVED", "UNSUPPORTED"]
