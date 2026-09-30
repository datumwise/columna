"""
columna_platform.kernel.observation — **the family-request observation seam.**

Ruled (Huayin, 2026-09-29, M-2 §4): *"Every request made to MME for family state should be observable,
whether it is ultimately READY, NEED, WANT_OF_STATE or UNSUPPORTED… The observation is operational/workload
evidence, not analytical data and not part of family identity or standing."*

So this module is **the smallest record that a later cache-economics optimizer could be built on, and
nothing more.** No scoring, no policy, no eviction advice, no cost model. It answers one question — *what
was asked of the MME, and what actually happened* — and it answers it for misses as loudly as for hits.

THE FOUR PROPERTIES THIS SEAM HAS TO HAVE
-----------------------------------------
  **1 · AT THE REQUEST BOUNDARY, NOT AT THE HIT.**  Ruled §7: *"A cache policy cannot learn from hits
  alone… If `Revenue@Month` is repeatedly absent and repeatedly derived/fetched, those requests must still
  be visible."* An observation is emitted for every `measure`, including the ones that refuse. A log that
  only records successes describes a cache that is already correct and can never tell you which one to
  build.

  **2 · NON-AUTHORITATIVE.**  An observation never creates, extends or withholds an analytical right.
  Ruled §6: *"Request/workload observations may influence future residency decisions only. They never
  create analytical rights."* Nothing in the serving path reads an observation back; the sink is
  write-only by construction, and the MME holds no accessor that consults one.

  **3 · NON-BLOCKING.**  Ruled: *"observation failure must never affect analytical serving"* (Huayin,
  2026-09-29, refining M-2 §4). Every emission goes through `ObservationSink.emit`, which contains observer
  FAILURES and counts them. An observer that raises, hangs on a bad attribute or returns garbage costs the
  request nothing but a tick on `sink.failures`. This is why the interface is append/event-style rather
  than a callback that can veto. See `ObservationSink.emit` for what is contained and what deliberately
  is not.

  **4 · ENOUGH SHAPE TO SUPPORT ECONOMICS LATER, WITHOUT ASSERTING ANY.**  See below.

WHAT `V(m)` NEEDS, AND WHY THIS RECORD IS SHAPED THE WAY IT IS
--------------------------------------------------------------
Ruled §5, and the ruling is explicitly a warning about the OBVIOUS formula. Do **not** model cache value as

    request_frequency × recompute_from_root_cost

The relevant quantity is the marginal reduction in end-to-end **lawful fulfillment** cost:

    V(m) = Σ_q λ(q) · ( C[best lawful fulfillment of q WITHOUT m] − C[best lawful fulfillment of q WITH m] )

where the lawful alternatives include serving from another cached materialization, continuing from a
cached edge/ancestor, continuing from the cached root, fetching a non-root materialization from a backend,
fetching the root and continuing, backend pushdown, and local columnar compute — each with its own latency
and cost. **This optimizer is not implemented in M-2** and this module does not gesture at it. What the
ruling requires of M-2 is only that the record not make it impossible, and there are three things the
obvious record would have thrown away:

  · **λ(q) is demand for a TARGET, not for a materialization.** Ruled §8: *"A retained family
    materialization can be valuable even if rarely requested directly… Its cache value may come from
    reducing fulfillment cost for many downstream targets."* So `FamilyRequest` records what was ASKED
    (family + target anchor), and `Fulfillment` separately records what ANSWERED (`selected`). A record
    that only logged the materialization id would make `Revenue@Day`'s value as an ancestor invisible.

  · **The counterfactual needs the ROUTE, not just the outcome.** `seeded_from` and `work` say *which*
    materialization was continued from and *how far*, which is what a later estimator differences against.
    Without it, "with m" and "without m" are the same row.

  · **A miss has to say WHICH KIND of miss.** `NEED` and `UNSUPPORTED` are both refusals and they are
    opposite evidence: retaining something would have changed the first and could never change the second.
    Collapsing them into "miss" is how a cache optimizer learns to cache things that no cache can help.

Counters here are **observed**, never modelled: elapsed nanoseconds, cells folded, candidates considered.
Ruled §4: *"latency/cost counters where available without inventing a cost model."* There is no unit
conversion, no weighting and no currency in this module, because every one of those would be the cost
model arriving early and unrulled.

THE FOUR DISPOSITIONS
---------------------
Named by what the CONSUMER should do about them, which is the distinction a policy needs:

    READY           the family state was supplied. `directly_held` says whether the target itself was
                    held or whether it was derived, which is the difference between a hit and work.
    NEED            lawful, and we do not have it. The state could be established or realized and then
                    this request would succeed. **The only disposition where a cache decision would have
                    changed the outcome** — which is exactly what makes it the interesting row.
    WANT_OF_STATE   the material is present and the value is OWED AND ABSENT at participating points.
                    Not a cache miss: more cache would not help, and the remedy is establishment of the
                    missing value, not residency. Kept distinct from `NEED` for that reason alone.
    UNSUPPORTED     no lawful route exists at all — outside the continuation region, no realization for
                    the law, no admitted basis. Retaining anything, anywhere, forever, would not change
                    this answer. A policy that cannot see this disposition will try to cache its way out
                    of a law.
"""
from __future__ import annotations

import itertools
import time
from dataclasses import dataclass, field
from typing import Optional, Protocol, runtime_checkable

from .geometry import Anchor
from .materialization import MaterializationId

# ── the four dispositions ────────────────────────────────────────────────────────────────────────
READY = "ready"
NEED = "need"
WANT_OF_STATE = "want-of-state"
UNSUPPORTED = "unsupported"
DISPOSITIONS = (READY, NEED, WANT_OF_STATE, UNSUPPORTED)

#: Refusal codes that mean **no lawful route exists**, as opposed to *we do not hold it*. The mapping is
#: kept here rather than inside the engines so that both MMEs classify identically and a reader can see the
#: whole judgement in one place. Anything not listed is `NEED`: the conservative direction, because
#: mistaking "unsupported" for "need" costs a policy a wasted consideration, and the reverse teaches it that
#: a law it can never satisfy is merely a cold cache.
UNSUPPORTED_CODES = frozenset({
    # ONE code for one question (B-0b). `anchor-outside-the-continuation-region` was the same refusal
    # emitted by `MME.admit`, and it existed only because `admit` was a SECOND asker of a constitutional
    # question. The authority is the single asker now, so the second spelling is retired rather than kept
    # as a synonym nothing can produce.
    "outside-continuation-region",
    "unrealized-law",
    "no-admitted-basis",
    "incompatible-basis",
    "layouts-differ",
    "unknown-object",
})

WANT_OF_STATE_CODES = frozenset({"want-of-state", "basis-operand-wants-state"})

# **`state-no-longer-sufficient` IS `NEED`, NOT `UNSUPPORTED`, AND F-1 IS WHERE THAT SHOWED.** M-2 listed
# it as unsupported; R-1's `MME.requirement_for` emits a requirement for it, because a held FINALIZED
# scalar where the law composes structured state is precisely something the estate could supply properly.
# The two classifications disagreeing would have meant the workload log and the Fulfillment Coordinator
# telling a future cache economist different stories about the same request, so they are now one
# judgement: supplying adequate state would fix it, therefore NEED.


def disposition_for(refusal_code: str) -> str:
    """**Classify one refusal into the disposition a policy can act on.** Total: every code lands."""
    if refusal_code in WANT_OF_STATE_CODES:
        return WANT_OF_STATE
    if refusal_code in UNSUPPORTED_CODES:
        return UNSUPPORTED
    return NEED


_SEQUENCE = itertools.count(1)


# ── the record ───────────────────────────────────────────────────────────────────────────────────
@dataclass(frozen=True)
class FamilyRequest:
    """**What was asked of the MME** — recorded before anything is known about the answer.

    This is the `q` in `Σ_q λ(q)`: a demand for an analytical identity at a target anchor, which is the
    thing a frequency is counted over. It deliberately carries no materialization id, because a request
    does not name one (ruled M-1 §2: *"the request asks for an analytical identity, not a physical
    materialization"*), and a record that conflated them would make §8's descendant-reuse value unaskable.

    `on_behalf_of` is the **use** the ruling asks be preserved (§8: *"enough route/use information"*): when
    `Revenue@Month` is requested because `AOV@Month` needed it, that is not the same demand signal as a
    user asking for `Revenue@Month` directly, and a later estimator that could not tell them apart would
    attribute an expression's traffic to a family's popularity."""

    manifold: str
    build: str
    family_id: str
    target: Anchor
    data_state: Optional[str] = None
    #: The consumer above the MME that caused this request, where there is one — e.g.
    #: `"average_order_value@{month} via revenue-and-count"`. Empty for a direct ask.
    on_behalf_of: str = ""

    def __str__(self) -> str:
        via = f" ← {self.on_behalf_of}" if self.on_behalf_of else ""
        return f"{self.family_id}@{self.target}{via}"


@dataclass(frozen=True)
class Fulfillment:
    """**The work actually performed**, where the engine knows it. Every field is observed, not estimated.

    `directly_held` is the ruling's *"whether target was directly held or derived"* and is the single most
    load-bearing bit for a future optimizer: it is the difference between a request that cost nothing and
    one that cost a fold, over the same family and the same anchor."""

    #: Was `F@target` itself held, or was the answer derived by continuing from a finer materialization?
    directly_held: bool = False
    #: Which materialization(s) answered. Empty on every refusal, and on a refusal that is the point.
    selected: tuple[MaterializationId, ...] = ()
    #: Where the continuation started, when it was one. `None` for a direct hit or a refusal.
    seeded_from: Optional[Anchor] = None
    #: Continuation work, in the substrate's own unit: source cells/rows folded. `None` where unknown —
    #: and `None` is honest, where a zero would be a claim.
    folded: Optional[int] = None
    #: How many retained materializations were adjudicated before an answer was reached. The cost of the
    #: SEARCH, which is distinct from the cost of the WORK.
    considered: int = 0
    #: What this request ADDED to the cache, if it retained its own result. A future policy needs to know
    #: that a request was also a producer — otherwise a derived materialization looks like it appeared for
    #: free and the fold that made it is charged to nobody.
    admitted: tuple[MaterializationId, ...] = ()


@dataclass(frozen=True)
class RequestObservation:
    """**One family request and its outcome.** Append-only; nothing mutates one and nothing reads one back
    into the serving path."""

    seq: int
    at: float                              # wall clock, seconds. The engine holds no clock of its own.
    elapsed_ns: int
    request: FamilyRequest
    disposition: str
    #: The kernel route the answer took (`cached` / `root` / `continued` / `refused`), carried verbatim.
    #: Distinct from the disposition: the route is what happened, the disposition is what it means.
    route: str
    fulfillment: Fulfillment = field(default_factory=Fulfillment)
    refusal_code: str = ""

    @property
    def served(self) -> bool:
        return self.disposition == READY

    def __str__(self) -> str:
        how = ("held" if self.fulfillment.directly_held else
               f"derived from {self.fulfillment.seeded_from}" if self.fulfillment.seeded_from
               else self.refusal_code or "—")
        return f"#{self.seq} {self.request} → {self.disposition} [{how}] {self.elapsed_ns / 1e6:.2f}ms"


# ── the sink ─────────────────────────────────────────────────────────────────────────────────────
@runtime_checkable
class WorkloadObserver(Protocol):
    """**Append/event-style, deliberately** (ruled §4: *"Prefer an append/event-style observation interface
    rather than coupling correctness to logging"*).

    One method, no return value, no ability to refuse. There is nothing an observer can say back to the
    engine, which is what makes "observations never create analytical rights" a property of the TYPE rather
    than a rule someone has to keep."""

    def observe(self, observation: RequestObservation) -> None: ...


#: **Exceptions that are the PROCESS being stopped, not an observer failing.** Named as a constant so the
#: distinction is one decision recorded in one place, rather than a tuple inlined at an `except` clause and
#: silently re-derived the next time someone touches it.
PROCESS_CONTROL = (KeyboardInterrupt, SystemExit, GeneratorExit)


class NullObserver:
    """The default. An MME with no observer configured does not pay for one and does not branch on one."""

    def observe(self, observation: RequestObservation) -> None:
        return None


class RecordingObserver:
    """**An in-memory append log**, which is the whole of M-2's observer.

    It is a reference implementation and a test instrument, not a policy: it counts, it groups, and it
    refuses to score. The accessors below are the shapes §7 and §8 name — demand per target, and misses
    separated from hits — because those are the questions the next unit will ask, and writing them here is
    how we find out whether the record can answer them before committing to a persistent one."""

    def __init__(self) -> None:
        self.records: list[RequestObservation] = []

    def observe(self, observation: RequestObservation) -> None:
        self.records.append(observation)

    def __len__(self) -> int:
        return len(self.records)

    def __iter__(self):
        return iter(self.records)

    def by_disposition(self) -> dict[str, int]:
        out: dict[str, int] = {}
        for r in self.records:
            out[r.disposition] = out.get(r.disposition, 0) + 1
        return dict(sorted(out.items()))

    def demand(self) -> dict[tuple[str, str], int]:
        """**λ(q): how often each `F@A` was ASKED FOR**, hits and misses alike (§7).

        Keyed by what was requested and never by what answered, which is what keeps an ancestor's value
        from being attributed to the descendants it served."""
        out: dict[tuple[str, str], int] = {}
        for r in self.records:
            key = (r.request.family_id, str(r.request.target))
            out[key] = out.get(key, 0) + 1
        return dict(sorted(out.items()))

    def uses_of(self, mid: MaterializationId) -> tuple[RequestObservation, ...]:
        """Every request this materialization answered — **including requests for a DIFFERENT anchor**,
        which is §8's case: a `Revenue@Day` that is never asked for directly and answers everything."""
        return tuple(r for r in self.records if mid in r.fulfillment.selected)

    def misses(self) -> tuple[RequestObservation, ...]:
        """The rows a hit-only log would not have (§7)."""
        return tuple(r for r in self.records if r.disposition != READY)

    def summary(self) -> str:
        return (f"{len(self.records)} family request(s); dispositions {self.by_disposition()}; "
                f"{len(self.misses())} not served")


class ObservationSink:
    """**Where observation is made unable to break serving.**

    The MME holds one of these, never a bare observer, and the only method the serving path calls is
    `emit`. What is caught is counted and the last one is kept for diagnosis, so a broken observer is loud
    in `sink.summary()` and silent everywhere that matters."""

    def __init__(self, observer: Optional[WorkloadObserver] = None) -> None:
        # **`is not None`, NOT `or`.** A `RecordingObserver` defines `__len__`, so an empty one is FALSY —
        # `observer or NullObserver()` silently discarded every freshly-constructed recorder and observation
        # looked like it was working while recording nothing. An identity test is the only correct one here:
        # an observer's truthiness is its own business and says nothing about whether it was supplied.
        self.observer: WorkloadObserver = observer if observer is not None else NullObserver()
        self.emitted = 0
        self.failures = 0
        self.last_failure: Optional[BaseException] = None

    @property
    def active(self) -> bool:
        return not isinstance(self.observer, NullObserver)

    def emit(self, observation: RequestObservation) -> None:
        """**An observation FAILURE never reaches the serving path.** The obligation is discharged in one
        place rather than at every call site — a `try` around each `measure` would have been a rule to
        remember instead of a property to hold.

        **AND PROCESS-CONTROL EXCEPTIONS ARE NOT OBSERVATION FAILURES** (ruled 2026-09-29: *"swallowing
        process-control exceptions such as `KeyboardInterrupt`/`SystemExit` is unusual… do not treat
        'catch every BaseException forever' as an architectural requirement"*). M-2 shipped a bare
        `except BaseException`, and the distinction it missed is the one that matters:

          · a `TypeError`, a broken socket, a `RecursionError` inside an observer — these are the LOGGING
            BACKEND failing. They say nothing about the request, and containing them is exactly the ruled
            invariant;
          · a `KeyboardInterrupt` or `SystemExit` arriving during an observer call is **the process being
            asked to stop**. It did not originate in the observer and is not about it; the interrupt landed
            in this frame only because this frame happened to be executing. Eating it means Ctrl-C is
            silently ignored for as long as a serving loop runs, and a `SystemExit` raised by a shutdown
            path is discarded — a worse failure than the one the containment was protecting against, and
            not what the invariant asks for.

        **Re-raising does not violate the invariant**, and it is worth saying why rather than asserting it:
        the observation is emitted only AFTER the answer is fully determined, so there is no analytical
        work left to interrupt. What an interrupt aborts is the RETURN of an already-computed answer — and
        it would have aborted the very next instruction anyway, observer or no observer. **The serving is
        not affected; the process is stopping, because it was told to.**

        `GeneratorExit` joins them: it is the interpreter unwinding a generator, not an observer fault, and
        swallowing it corrupts the unwind rather than protecting a request."""
        try:
            self.observer.observe(observation)
            self.emitted += 1
        except PROCESS_CONTROL:
            # NOT counted as an observer failure, because it is not one. Straight back out.
            raise
        except Exception as exc:                          # noqa: BLE001 - deliberate, and the point
            self.failures += 1
            self.last_failure = exc

    def summary(self) -> str:
        broken = f"; {self.failures} FAILED (last: {self.last_failure!r})" if self.failures else ""
        return f"{type(self.observer).__name__}: {self.emitted} observed{broken}"


def observe_request(sink: ObservationSink, request: FamilyRequest, *, started_ns: int,
                    route: str, refusal_code: str = "", disposition: Optional[str] = None,
                    fulfillment: Optional[Fulfillment] = None) -> RequestObservation:
    """**Mint and emit one observation.** Returns the record so a caller can assert on it; the return value
    is never consulted by the serving path.

    The disposition is DERIVED from the refusal code unless the caller names one, so that the two engines
    cannot drift into classifying the same refusal differently."""
    if disposition is None:
        disposition = READY if not refusal_code else disposition_for(refusal_code)
    observation = RequestObservation(
        seq=next(_SEQUENCE), at=time.time(), elapsed_ns=max(0, time.perf_counter_ns() - started_ns),
        request=request, disposition=disposition, route=route,
        fulfillment=fulfillment or Fulfillment(), refusal_code=refusal_code)
    sink.emit(observation)
    return observation


__all__ = ["DISPOSITIONS", "NEED", "PROCESS_CONTROL", "READY", "UNSUPPORTED", "UNSUPPORTED_CODES",
           "WANT_OF_STATE",
           "WANT_OF_STATE_CODES", "FamilyRequest", "Fulfillment", "NullObserver", "ObservationSink",
           "RecordingObserver", "RequestObservation", "WorkloadObserver", "disposition_for",
           "observe_request"]
