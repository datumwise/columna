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
    ExpressionEvaluator,
    KernelRefusal,
    MME,
    Refusal,
)
from columna_platform.kernel.fulfillment import (
    INCOMPLETE,
    NOT_SUPPORTED,
    ROUTE_POLICY_NEEDED,
    SERVED,
    UNAVAILABLE,
    UNRESOLVED_STATE,
    FulfillmentCoordinator,
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
    """**The serving path.** One constituted MME, one expression evaluator above it, and Frame-QL text in.

    **THE TWO COLLABORATORS ARE TWO, AND THAT IS M-2** (ruled 2026-09-29 §1, §6). Platform serving supports
    expressions exactly as fully as it did before; what changed is that it no longer gets them from the
    MME. A family column is answered by `MME.measure` and an expression column by
    `ExpressionEvaluator.evaluate`, and the evaluator reaches the MME for its operands — never the other
    way round. The service is the smallest thing that stands where §6's **Fulfillment Coordinator** will
    eventually stand: the one place that knows about both."""

    def __init__(self, mme: MME, evaluator: Optional[ExpressionEvaluator] = None,
                 coordinator: Optional[FulfillmentCoordinator] = None) -> None:
        self.mme = mme
        #: Constructed over the engine, not obtained from it. An injected one is accepted so that a caller
        #: with a different evaluation strategy can supply it without subclassing the service.
        self.expressions = evaluator or ExpressionEvaluator(mme)
        #: **THE FAMILY PATH, AND THERE IS NO OTHER ONE** (B-2, ruled 2026-09-30: *"Do not preserve the
        #: direct `FrameQLService → mme.measure` family path as a fallback"*). A default coordinator over
        #: an EMPTY estate is the honest state of a deployment with no providers: it consults nobody and a
        #: cold family comes back `lawful-but-unavailable` rather than silently unserved. A deployment with
        #: a real provider injects a coordinator holding it, and this class never learns what a provider is.
        self.coordinator = coordinator if coordinator is not None else FulfillmentCoordinator(
            mme, evaluator=self.expressions)

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
                answer, fulfilled = self._serve_one(s.token, sorts[s.token], anchor)
            except KernelRefusal as exc:
                # A REALIZATION limit reaches here as an exception because it is not a governed verdict
                # about the ask — the law is intact and this build cannot execute it.
                return Outcome(UNSUPPORTED, query, request=request, sorts=sorts,
                               refusal=Refusal(exc.code, exc.subject, exc.detail))
            if answer is None or not answer.served:
                return self._not_served(query, request, sorts, s.alias, answer, fulfilled)
            answers[s.alias] = answer

        try:
            frame = self._frame(request, anchor, sorts, answers)
        except KernelRefusal as exc:
            # **A PER-CELL GOVERNED VERDICT, AND THE FRAME DECLINES TO PRINT ANYTHING IN ITS PLACE** (B-2).
            # `ColumnarFamilyState.cell` refuses at a point that participates and whose required value is
            # not established. Reaching here means a state was served whose payload still has want of state
            # somewhere — the engines refuse that before serving a fold, so this is the floor rather than
            # the usual path — and the honest answer is the refusal, never a dash. It is classified REFUSE
            # and not UNSUPPORTED because it IS a governed verdict: the build implements the ask perfectly.
            return Outcome(REFUSE, query, request=request, sorts=sorts,
                           refusal=Refusal(exc.code, exc.subject, exc.detail))
        classification = DISCLOSE if any(c.disclosures for c in frame.columns) else SERVE
        return Outcome(classification, query, request=request, frame=frame, sorts=sorts)

    # ── the not-served mapping · SIX MOODS, FIVE CLASSIFICATIONS, AND THE RESIDUE IS NAMED ────
    def _not_served(self, query: str, request: PlatformRequest, sorts: dict, alias: str,
                    answer: Optional[Answer], fulfilled: Any) -> Outcome:
        """**Which Frame-QL classification truthfully carries this fulfilment mood?**

        Ruled (Huayin, 2026-09-30): *"Do not collapse distinctions merely to get B-2 green… do not turn
        `lawful but unavailable` into an analytical refusal… If the existing Frame-QL classification
        vocabulary cannot truthfully represent one of the coordinator moods without changing its meaning,
        stop on that specific vocabulary gap rather than inventing a classification."*

        **THE SPLIT IS THE ONE THIS SERVICE ALREADY MADE, NOT A NEW ONE.** Before F-1 was wired in, a
        governed verdict arrived as an unserved `Answer` and became `REFUSE`, while a build limit arrived as
        a `KernelRefusal` and became `UNSUPPORTED`. That rule is kept — but **the mood is read FIRST**, and
        the order is load-bearing rather than stylistic:

            the three estate moods       → **NO TRUTHFUL CLASSIFICATION EXISTS** (see below). Checked
                                           first, because the in-memory engine states its cache miss AS a
                                           governed refusal (`unanswerable`: *"no state is held under this
                                           analytical instance"*), so classifying by the carried refusal
                                           would make every cold family an ANALYTICAL REFUSAL — the one
                                           mapping that was ruled out by name. The columnar engine returns
                                           the same miss with no refusal object at all, and that the two
                                           substrates differ here is exactly why the MOOD is the thing to
                                           read and the refusal is the thing to quote.
            `answer.refusal` present     → REFUSE, that refusal verbatim, with the mood appended and never
                                           substituted. Covers `UNRESOLVED_STATE` (`want-of-state` IS a
                                           governed standing about evidence) and every `NOT_SUPPORTED` the
                                           engine already stated as a verdict — outside the continuation
                                           region, outside `R_F`, an incompatible basis.
            `NOT_SUPPORTED`, no verdict  → UNSUPPORTED. *"lawful Frame-QL this build does not implement"*
                                           is exactly what the mood says when no governed refusal
                                           accompanies it.

        THE VOCABULARY GAP, STATED RATHER THAN PAPERED OVER. `UNAVAILABLE`, `ROUTE_POLICY_NEEDED` and
        `INCOMPLETE` are conditions of the ESTATE, and Frame-QL's five classifications are about the QUERY:

            `lawful-but-unavailable`   the ask is lawful, this build implements it, and nobody can supply
                                       it right now. Not `REFUSE` (the answer is not NO — it was ruled
                                       explicitly that this must not become an analytical refusal), not
                                       `UNRESOLVED` (the name resolved), and not honestly `UNSUPPORTED`
                                       (the build implements it fine).
            `route-policy-needed`      two admissible routes and nothing executed. A request for a
                                       DECISION, which is not a statement about the query at all.
            `incomplete-fulfillment`   realization ran and was not enough. Work happened, so it is not an
                                       implementation limit either.

        They are returned as `UNSUPPORTED` **carrying the mood as the refusal code** so that no caller can
        mistake which condition it met, and so that the day a sixth classification is ruled on, every one
        of these is findable by its code. That is a recorded gap, not a resolution, and B-2 stops on it."""
        mood = getattr(fulfilled, "mood", "")
        subject = getattr(fulfilled, "target", alias)
        carried = f"series {alias!r}: {answer.refusal.detail}" if (
            answer is not None and answer.refusal is not None) else ""

        # 1 · THE THREE ESTATE MOODS COME FIRST, AND THE ORDER IS THE RULING. **No truthful
        #     classification exists** for them — see the docstring. They are checked BEFORE any refusal
        #     the answer carried, because the in-memory engine states its cache miss AS a refusal
        #     (`unanswerable`: *"no state is held under this analytical instance"*) and classifying by that
        #     would turn `lawful-but-unavailable` into an analytical refusal — ruled explicitly against.
        #     **THE ENGINE'S "I DO NOT HOLD IT" IS NOT A VERDICT ABOUT THE QUESTION.** That the two
        #     substrates differ here at all — the columnar engine returns a miss without a refusal object —
        #     is exactly why the mood is the thing to read and the refusal is the thing to quote.
        if mood in (UNAVAILABLE, ROUTE_POLICY_NEEDED, INCOMPLETE):
            detail = getattr(fulfilled, "detail", "")
            if carried:
                detail += f" The engine said: {carried}"
            detail += (
                f" **THIS IS NOT A CLAIM THAT THE BUILD CANNOT DO IT, AND NOT A REFUSAL OF THE ASK.** "
                f"Frame-QL classifies the QUERY and {mood!r} is a condition of the ESTATE; the vocabulary "
                f"has no classification that carries it truthfully, so it is reported here under the "
                f"nearest existing one with its own code intact. Recorded as an open vocabulary gap "
                f"(B-2), not as a verdict about the ask.")
            return Outcome(UNSUPPORTED, query, request=request, sorts=sorts,
                           refusal=Refusal(mood, subject, detail))

        # 2 · A GOVERNED VERDICT CLASSIFIES ITSELF. `UNRESOLVED_STATE` always arrives this way — its
        #     `want-of-state` IS a standing about evidence — and so does every `NOT_SUPPORTED` the engine
        #     already stated as one: outside the continuation region, outside `R_F`, incompatible basis.
        #     The mood is appended, never substituted: two facts, and the specific one is kept.
        if carried:
            detail = carried + (f" [fulfilment mood: {mood}]" if mood and mood != SERVED else "")
            return Outcome(REFUSE, query, request=request, sorts=sorts,
                           refusal=Refusal(answer.refusal.code, answer.refusal.subject, detail))

        # 3 · NO LAWFUL ROUTE IN THIS BUILD, and no governed verdict accompanying it. `UNSUPPORTED` means
        #     exactly *"lawful Frame-QL this build does not implement"*, so this one is a true mapping.
        if mood == NOT_SUPPORTED:
            return Outcome(UNSUPPORTED, query, request=request, sorts=sorts,
                           refusal=Refusal(mood, subject, getattr(fulfilled, "detail", "")))
        if mood == UNRESOLVED_STATE:                         # pragma: no cover - always carries a verdict
            return Outcome(REFUSE, query, request=request, sorts=sorts,
                           refusal=Refusal(mood, subject, getattr(fulfilled, "detail", "")))
        return Outcome(UNSUPPORTED, query, request=request, sorts=sorts,
                       refusal=Refusal(mood or "not-fulfilled", subject,
                                       getattr(fulfilled, "detail", "")))

    # ── the two paths, chosen by SORT and never by inspection of what came back ───────────────
    def _serve_one(self, token: str, sort: str, anchor: Anchor):
        """`(answer, fulfilment)` — the fulfilment is the coordinator's outcome, or `None` for an
        expression.

        **THE FAMILY BRANCH NO LONGER CALLS `mme.measure`** (B-2). It was one line and it was the whole
        reason a cold Frame-QL request could never reach a provider: `measure` asks the cache and stops,
        so `NEED` came back as an unserved answer and was classified as a refusal. The coordinator owns
        the loop that turns `NEED` into propose → realize → adjudicate → admit → retry, and this service
        now has no path that skips it.

        The expression branch is unchanged and deliberately does NOT go through `fulfill_expression`: that
        method passes a `GovernedExpression` object to the evaluator, which the columnar evaluator cannot
        take (it wants an `expression_id`), and B-2 is one family request. Recorded as the next
        substrate-neutrality seam; untouched here on purpose."""
        if sort == "family":
            outcome = self.coordinator.fulfill(self.mme.family(token), anchor)
            return outcome.answer, outcome
        # **ABOVE the MME, and asked of a different object.** The dispatch was already by SORT and never
        # by inspecting what came back; M-2 only changes who the second branch talks to.
        return self.expressions.evaluate(self.mme.expression(token), anchor), None

    def _frame(self, request: PlatformRequest, anchor: Anchor, sorts: dict,
               answers: dict) -> Frame:
        # **THE NEUTRAL SURFACE, AND NOTHING ELSE** (B-2). This read `answer.value.cells` — a `Mapping`
        # that only the in-memory substrate has — which is why this service could not serve a single query
        # over the columnar engine. `coordinates` + `cell()` is the surface both substrates honestly
        # implement, and the columnar one keeps its refusal.
        covered: dict[str, set[tuple]] = {
            alias: set(answer.value.coordinates) for alias, answer in answers.items()}
        keys: set[tuple] = set()
        for points in covered.values():
            keys |= points
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
                #
                # **ABSENCE IS TESTED BY MEMBERSHIP, NOT BY A DEFAULT** (B-2). `cells.get(key, "—")` made
                # "no value here" and "a value the state declines to return" one answer. They are two:
                # a point outside `coordinates` is absent and gets the dash, and a point INSIDE it whose
                # value the state will not yield raises — which `serve` turns into a governed REFUSE
                # rather than printing anything at all.
                row.append(answers[s.alias].value.cell(key) if key in covered[s.alias] else "—")
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
                            f"→ authorize() → MME.fulfill()")
                # **EXPLAIN NOW SHOWS THE TWO ACTS SEPARATELY** (B-0b), because they are two acts and a
                # plan that merged them could not show which one stopped a request. Authorization is
                # constitutional and is asked first; the cache's adjudication of each candidate is only
                # reached when a request exists at all.
                authorized = self.mme.authorizer.authorize(family, anchor)
                if not authorized:
                    plan.append(f"    AUTHORIZATION REFUSED [{authorized.refusal.code}] — the "
                                f"constitution permits no value here, so no request reaches the cache "
                                f"and no candidate is considered")
                    continue
                plan.append(f"    authorized: fold {authorized.request.fold}")
                for candidate in self.mme.candidates(family):
                    verdict = self.mme.adjudicate(candidate, authorized.request)
                    plan.append(f"    candidate {candidate.key} → "
                                + ("ADMITTED" if verdict else f"REFUSED [{verdict.code}]"))
            else:
                expression = self.mme.expression(s.token)
                plan.append(f"{s.token}: GOVERNED EXPRESSION, constructor={expression.constructor} "
                            f"→ ExpressionEvaluator.evaluate() (ABOVE the MME; its operands come "
                            f"from MME.measure)")
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
