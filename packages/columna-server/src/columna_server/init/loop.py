"""
columna_server.init.loop — the `columna init` authoring loop (WP on-ramp/Explorer, CP-2 artifact 3).

The A4 loop made mechanical: **generate → review → revise**, until the human publishes. The MIND is
rented (a provider); the WORLD is this harness — the draft artifact + its polarity wall (columna_core.
draft), the connector aperture (columna_core.connector), and the laws below. Publish is the author's
act; a settled review mark stays settled unless the human reopens it (the revise-turn law).

Hermetic by construction: with a ScriptedProvider it runs with no real model — so the loop, the wall,
the mark bookkeeping, and the aperture call shapes are all exercised for real, only the judgment swapped
for a fixed script. (Judgment QUALITY is the eval suite's jurisdiction, not this harness's.)
"""
from __future__ import annotations

from columna_core.draft import (Draft, Proposal, INFERRED_CATALOG, STRUCK,
                                SCOPED, PROPOSED_STATE, DECLARED_STATE, ATTESTED, PUBLISHED)


class LoopViolation(Exception):
    """A harness-law breach — e.g. a revise turn re-proposing a struck declaration."""


def _spec_to_proposal(s: dict) -> Proposal:
    """A provider's proposal spec (a plain dict — the mind speaks data) → a Proposal. An opening spec
    from the agent has no author mark, so this raises PolarityViolation at construction (wall layer 1):
    init literally cannot build a door."""
    return Proposal(kind=s["kind"], body=s["body"], grade=s.get("grade", INFERRED_CATALOG),
                    opens_fertility=s.get("opens_fertility", False),
                    author_declared=s.get("author_declared", False))


class ScriptedProvider:
    """A fixed script of proposal-generations (no real model). Each propose()/revise() yields the next
    generation; a generation is a list of proposal-spec dicts."""

    def __init__(self, generations):
        self._gen = [list(g) for g in generations]
        self._i = 0

    def propose(self, aperture, draft):
        return self._next()

    def revise(self, aperture, draft):
        return self._next()

    def _next(self):
        g = self._gen[self._i] if self._i < len(self._gen) else []
        self._i += 1
        return g


class InitLoop:
    """Drives a Draft through the state machine via a provider (the mind) reading the aperture (the
    data wall). All acts marked (human) belong to the author; the agent only ever proposes."""

    def __init__(self, aperture, provider, manifold_name: str):
        self.aperture = aperture
        self.provider = provider
        self.draft = Draft(manifold_name)

    def generate(self) -> Draft:
        # scoped → proposed: the provider proposes declarations, reading through the aperture only.
        for s in self.provider.propose(self.aperture, self.draft):
            self.draft.add(_spec_to_proposal(s))            # PolarityViolation here if it tries a door
        if self.draft.state == SCOPED:
            self.draft.advance(PROPOSED_STATE)
        return self.draft

    def review(self, marks: dict) -> Draft:
        """(human) apply review marks {proposal_index: mark}."""
        for i, mark in marks.items():
            self.draft.proposals[i].review = mark
        return self.draft

    def revise(self) -> Draft:
        # the provider addresses the marks — but a STRUCK declaration stays struck unless the human
        # reopened it (the revise-turn law); re-proposing one is a harness violation.
        struck = {p.body for p in self.draft.proposals if p.review == STRUCK}
        for s in self.provider.revise(self.aperture, self.draft):
            if s["body"] in struck:
                raise LoopViolation(
                    f"revise re-proposed a struck declaration {s['body']!r} — a settled mark stays "
                    f"settled unless the human reopens it")
            self.draft.add(_spec_to_proposal(s))
        return self.draft

    # ---- the author's acts (never the agent's) ----
    def declare(self) -> Draft:
        return self.draft.advance(DECLARED_STATE)

    def attest(self) -> Draft:
        return self.draft.advance(ATTESTED)

    def publish(self) -> str:
        """(human) the author's act — advances to published (requires every proposal reviewed) and
        lowers the draft to a `.cml` string (the wall's second layer enforced in the lowering)."""
        self.draft.advance(PUBLISHED)
        return self.draft.lower_to_cml()
