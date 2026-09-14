"""Retained state — analytical identity plus standing, kept apart on purpose.

TWO QUESTIONS, TWO ANSWERS (SSE contract §1):

    what is this state OF?              ->  AnalyticalIdentity, `F @ A`
    may these two states be REUSED?     ->  Standing

    Matching `F @ A` is NECESSARY for reuse. It is NOT SUFFICIENT.

STANDING TRAVELS WITH STATE. It is never reconstructed from a bare value buffer — the precedent is
Core's own `CacheEntry`, which stores the disclosure beside the frame because "STORING THE DISCLOSURE
IS THE POINT, not an optimisation". A retained value whose standing has to be re-derived at
retrieval is a value whose standing can be re-derived DIFFERENTLY.

The axes carried below are the SSE contract's §4.1 list. They are carried as REACHABLE FACTS, not as
a frozen record: the contract deliberately does not name this object or fix its arity, and neither
does this module. `Standing` here is Proof A's working representation, and nothing downstream may
treat its shape as the contract.
"""
from __future__ import annotations
from dataclasses import dataclass, replace
from typing import Optional

import pyarrow as pa

from .refusals import WantOfCompatibility, WantOfLaw, WantOfState


@dataclass(frozen=True)
class AnalyticalIdentity:
    """`F @ A` — what the state is OF, and nothing about how it is stored.

    Deliberately two fields. Widening this to encode storage details is the specific error the SSE
    contract forbids: it would make two states of one analytical thing look like two things."""

    family_id: str
    anchor: str


@dataclass(frozen=True)
class Standing:
    """Whether a state may be reused or combined — the axes, each reachable, none merged."""

    #: THE ACTUAL GOVERNED CONSTITUTION under which this state was established. Part of
    #: compatibility (RULED Huayin, 2026-09-14 — OF-39). The SSE contract's invariant is
    #: COMPARABILITY plus conservative invalidation; a fingerprint is a permitted representation of
    #: it, not the invariant itself.
    constitution: Optional[str]
    #: HOW constitution fingerprints are formed, and therefore WHETHER two are comparable at all.
    #: An incomparable scheme must read as STALE, never as equal. Distinct in role from the field
    #: above: the scheme says whether the comparison is meaningful, the fingerprint says which
    #: constitution was in force.
    constitution_scheme: Optional[str]
    #: C5 — the regime under which contributions participate.
    participation: Optional[str]
    #: the sufficient-state basis, DERIVED BY THE GOVERNED LAYER and carried in as execution input.
    basis: Optional[str]
    #: the realization claim this state stands on.
    realization: Optional[str]
    #: opaque comparable currency token. `None` closes reuse; it never means "fresh".
    currency: Optional[str] = None
    #: the movement licence this state was continued under, if it was. ADDITIVE (Proof B): a state
    #: that arrived by a licensed movement must be able to say so, or the standing it carries forward
    #: is a claim about a path nobody recorded.
    movement: Optional[str] = None

    @property
    def comparable_to(self):
        """The sub-tuple on which two standings may be COMPARED AT ALL.

        Explicit comparability is the point: two standings either agree, disagree, or are
        INCOMPARABLE, and incomparable must not read as agree.

        THE CONSTITUTION FINGERPRINT IS IN THIS TUPLE (RULED Huayin, 2026-09-14, closing OF-39).
        It was not, and the two fields' roles are why that was wrong:

          · `constitution_scheme` establishes HOW fingerprints are formed, and therefore whether
            two of them are comparable at all;
          · `constitution` identifies WHICH actual governed constitution this state stands under.

        Carrying only the scheme meant two states established under DIFFERENT governed
        constitutions, agreeing on every other axis, compared as compatible and could be folded
        together. The defect was inert only because nothing on the serving path calls `combine` —
        which is precisely why it survived, and why it is repaired while it still changes no
        behaviour rather than later, when it would.

        THIS DOES NOT MAKE THE CONSTITUTION PART OF ANALYTICAL IDENTITY, and the distinction is
        load-bearing:

          · ANALYTICAL IDENTITY (`AnalyticalIdentity`, `F @ A`) is what the state is OF. Two states
            under different constitutions are still states of the same thing, and a request for
            that thing still names them both.
          · COMPATIBILITY STANDING is whether two otherwise-identical states may lawfully
            participate in one continuation. That is the question this tuple answers, and it is a
            different question with a different answer.

        Widening `AnalyticalIdentity` to carry the constitution would be the specific error the SSE
        contract forbids — encoding storage/standing detail into identity — and it would make a
        re-constituted state a state of something ELSE, which it is not.
        """
        return (self.constitution_scheme, self.constitution,
                self.participation, self.basis, self.realization)


@dataclass(frozen=True)
class RetainedState:
    """A value buffer that knows what it is of, and under what standing."""

    identity: AnalyticalIdentity
    standing: Standing
    array: pa.Array
    governed_domain: str
    #: physical description, kept for disclosure only. NEVER consulted in a governed decision.
    carrier_type: str = ""
    finalized: bool = False
    #: COMPOSITE STATE (Proof C), optional so Proof A's and B's states are unaffected. Where present,
    #: the sufficient state is the matching (SUM, COUNT) basis and `array` is not the witness.
    composite: object = None
    #: ANCHORED STATE (Proof B), optional so Proof A's bare-value states are unaffected. Where
    #: present, `table` carries the anchor coordinates alongside the values and `anchor_columns`
    #: names them — which is what makes a fold across a coordinate possible at all.
    table: Optional["pa.Table"] = None
    anchor_columns: tuple = ()


class RetainedStateStore:
    """Proof A's in-memory store. NO PERSISTENCE — durability belongs to a later proof.

    A RETRIEVAL MISS IS NOT A REFUSAL (ruled Huayin, 2026-09-12). The store may be handed a
    `rematerializer` — a callable that can re-establish a state for an identity. Where one exists and
    succeeds, an evicted state is re-established TRANSPARENTLY and the request serves; the caller
    never learns that the cache missed, because the cache's internal state is not a governed fact.

    Refusal is therefore reserved for the real condition: NO CURRENTLY ADMISSIBLE PATH OR STATE can
    establish the target. That is why the wire reason is `want_of_state` and not `evicted` — naming
    the cache outcome would freeze an implementation detail into the public vocabulary and go stale
    the moment transparent re-materialization lands."""

    def __init__(self, rematerializer=None):
        self._states: list = []
        #: () -> RetainedState | None. None = no re-materialization path is available at all.
        self._rematerializer = rematerializer
        #: counts, for evidence: did a serve go through a transparent re-establishment?
        self.rematerializations = 0

    def establish(self, identity: "AnalyticalIdentity"):
        """Try to re-establish state for an identity. Returns the state, or None if no path exists.

        Two distinct Nones collapse here ON PURPOSE — no path configured, and a path that could not
        produce admissible state — because the caller's question is the same either way: is there a
        currently admissible state? The DETAIL of which it was belongs in the refusal, not in the
        control flow."""
        if self._rematerializer is None:
            return None
        st = self._rematerializer(identity)
        if st is None:
            return None
        self.rematerializations += 1
        return self.insert(st)

    # ── insert ──────────────────────────────────────────────────────────────────────────────────
    def insert(self, st: RetainedState) -> RetainedState:
        """Realization standing must be present. A `None` currency token is ALLOWED and closes reuse.

        Never manufacture freshness: a token we could not honestly warrant is recorded as absent, and
        absence closes reuse rather than being optimistically read as current."""
        if getattr(st, "finalized", False):
            # CONTROL 1 (Proof C). A displayed value is not sufficient state, and the store is where
            # that has to bite — a finalized scalar that gets retained is indistinguishable from a
            # basis at every later point.
            raise WantOfState(
                "a finalized value is a displayed value, not sufficient state; re-materializing the "
                "basis it was computed from would resolve this", subject=st.identity.family_id)
        if st.standing.realization is None:
            raise WantOfState(
                "insert requires realization standing; a state that cannot say which realization it "
                "stands on cannot later be invalidated when that realization changes",
                subject=st.identity.family_id)
        self._states.append(st)
        return st

    # ── retrieve ────────────────────────────────────────────────────────────────────────────────
    def retrieve(self, identity: AnalyticalIdentity) -> tuple:
        """All states of this identity, IN WHATEVER STANDINGS THEY HOLD. Never merged.

        Returning several is correct and is not a defect to tidy away: merging them here would make
        a compatibility decision at a layer that does not own it."""
        return tuple(s for s in self._states if s.identity == identity)

    # ── combine ─────────────────────────────────────────────────────────────────────────────────
    def combine(self, a: RetainedState, b: RetainedState) -> RetainedState:
        """Equal identity AND compatible standing, and the law must license the fold."""
        if a.identity != b.identity:
            raise WantOfLaw("combine requires one analytical identity; these are two",
                            subject=f"{a.identity.family_id} vs {b.identity.family_id}")
        if a.standing.comparable_to != b.standing.comparable_to:
            # NOT a want-of-state: nothing is missing. Both states are valid and individually
            # reusable; the law simply does not license adding THESE two together.
            raise WantOfCompatibility(
                f"identical analytical identity, incompatible standing: "
                f"{a.standing.comparable_to} vs {b.standing.comparable_to}",
                subject=a.identity.family_id)
        if a.standing.currency is None or b.standing.currency is None:
            raise WantOfState("a state with no warranted currency token may not be reused",
                              subject=a.identity.family_id)
        if a.finalized or b.finalized:
            raise WantOfLaw("a finalized value is not sufficient state and may not be combined",
                            subject=a.identity.family_id)
        return replace(a, array=pa.concat_arrays([a.array, b.array]))

    # ── finalize ────────────────────────────────────────────────────────────────────────────────
    def finalize(self, st: RetainedState) -> RetainedState:
        """Mark a result NOT sufficient state. Offering it back as state is refused (see `insert`)."""
        return replace(st, finalized=True)

    def evict(self, identity: AnalyticalIdentity) -> int:
        """Policy only. MUST NOT convert a want-of-state into a want-of-law: after eviction the law
        still licenses the ask, so what is missing is state, and re-realization resolves it."""
        before = len(self._states)
        self._states = [s for s in self._states if s.identity != identity]
        return before - len(self._states)
