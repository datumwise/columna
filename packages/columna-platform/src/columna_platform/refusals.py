"""Proof A's refusal vocabulary — want-of-law vs want-of-state, kept un-collapsed.

THE DISTINCTION IS THE PRODUCT. A refusal that cannot say whether the LAW does not license the ask
or whether the STATE is not here destroys the evidentiary value of refusing, because the two carry
different remedies and land on different people:

    want-of-law    the governed law does not license this.   Remedy: a governed ruling / a licence.
                   Re-realization changes NOTHING.
    want-of-state  the law licenses it; the material state is
                   not admissible or not present.            Remedy: RE-REALIZATION.

This mirrors `columna_core.compiler.refusals`, which keeps five lowering conditions un-collapsed for
the same reason ("lowering failed" tells an operator nothing about whose gap it is). It does not
REPLACE that taxonomy: these are execution-path conditions, raised after lowering is out of scope.

WHY THESE ARE NOT WIRE REASONS. `columna_core.disclosure.REASON_OUTCOME` is a CLOSED, fail-closed
registry, and minting an entry in it is a ruling, not an implementation decision — the module says so
itself ("Register it (with a dated note on its intent) rather than letting it default"). Proof A
found no registered reason that carries either condition to its existing intent, and declined to
borrow one. See `serving.py` for the finding; nothing here reaches the wire.
"""
from __future__ import annotations
from typing import Optional


class ProofRefusal(Exception):
    """A fail-closed refusal on the successor execution path. Always names a jurisdiction."""

    #: stable token — the public name of this condition
    condition = "ProofRefusal"
    #: who owns the gap
    jurisdiction = "unassigned"
    #: what, if anything, would resolve it
    remedy: Optional[str] = None

    def __init__(self, detail: str, *, subject: str = ""):
        self.detail = detail
        self.subject = subject
        where = f" [{subject}]" if subject else ""
        super().__init__(f"{self.condition}{where}: {detail}")


class WantOfLaw(ProofRefusal):
    """The governed law does not license what was asked.

    Re-realization cannot resolve a want-of-law, and saying so is half the point: an operator told
    only "refused" will go and re-materialize, which is work that cannot possibly help."""

    condition = "WantOfLaw"
    jurisdiction = "governed"
    remedy = None


class WantOfState(ProofRefusal):
    """The law licenses the ask; the material state is not admissible, or not retained.

    MUST carry that re-realization would resolve it. The SSE contract's `refuse` row requires this
    explicitly, and it is the difference between an honest gap and an apparent incapacity."""

    condition = "WantOfState"
    jurisdiction = "realization"
    remedy = "re-realization would resolve this"


class WantOfCompatibility(ProofRefusal):
    """Two states share an analytical identity but their STANDINGS may not be combined.

    Neither a want-of-law nor a want-of-state: both states are valid and individually reusable, and
    NOTHING is missing. This is the participation/support row of the SSE contract's invalidation
    table — the axis whose mechanism is *blocks combination* and whose remedy is neither a licence
    nor re-realization. Collapsing it into either of the other two would misdirect every operator who
    read it."""

    condition = "WantOfCompatibility"
    jurisdiction = "governed"
    remedy = None


class UnsupportedByThisProfile(Exception):
    """NOT a governed verdict — a limit of what this profile implements (ruled 2026-09-12 §7).

    DELIBERATELY NOT A `ProofRefusal`. The three refusals above are findings of law or of state: they
    say the request was answered and the answer was no. This says the request was not answered at
    all. It carries no `jurisdiction`, because attaching one would place a capability gap inside a
    governed jurisdiction and tell an operator their question was unlawful when it was merely
    unimplemented here — and `want_of_state`'s remedy would then send them to re-materialize against
    a path that does not exist.

    It must therefore never be mapped to a wire reason. Where it escapes, it escapes as what it is:
    a profile that was asked for something it does not do, and said so, WITHOUT falling back to Core.
    """
