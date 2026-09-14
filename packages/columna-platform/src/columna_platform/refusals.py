"""Proof A's refusal vocabulary — want-of-law vs want-of-state vs want-of-compatibility, un-collapsed.

THE DISTINCTION IS THE PRODUCT. A refusal that cannot say whether the LAW does not license the ask
or whether the STATE is not here destroys the evidentiary value of refusing, because the two carry
different remedies and land on different people:

    want-of-law            no positive law licenses the requested transformation.
                           Remedy: a governed ruling / a licence. Re-realization changes NOTHING.
    want-of-compatibility  the relevant objects are each VALID and may not lawfully be combined,
                           because their compatibility conditions differ. Nothing is missing.
                           Remedy: neither a licence nor re-realization.
    want-of-state          the law licenses it; required admissible state is unavailable.
                           Remedy: RE-REALIZATION.

This mirrors `columna_core.compiler.refusals`, which keeps five lowering conditions un-collapsed for
the same reason ("lowering failed" tells an operator nothing about whose gap it is). It does not
REPLACE that taxonomy: these are execution-path conditions, raised after lowering is out of scope.

WHY THESE ARE NOT WIRE REASONS. `columna_core.disclosure.REASON_OUTCOME` is a CLOSED, fail-closed
registry, and minting an entry in it is a ruling, not an implementation decision — the module says so
itself ("Register it (with a dated note on its intent) rather than letting it default"). Proof A
found no registered reason that carries either condition to its existing intent, and declined to
borrow one. The reasons were subsequently RULED AND MINTED (`want_of_law`/`want_of_state` 2026-09-12;
`realization_contradicts_law` and `want_of_compatibility` 2026-09-14), and `serving.py` now carries a
CLOSED CLASS-KEYED MAPPING from these classes to them. Nothing in this module reaches the wire; the
translation happens at that one boundary and the mapping has no fallback, so a class added here
without an entry there fails the build.

TWO CLASSES SIT OUTSIDE `ProofRefusal` ON PURPOSE — `UnsupportedByThisProfile` and
`RealizationContradictsLaw`. The hierarchy is for FINDINGS: the request was answered and the answer
was no (mood REFUSE). Those two say the request was never answered at all (mood ERROR), and keeping
them out of the hierarchy is what makes it impossible for the governed handler to hand them a
jurisdiction by accident.
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


class RealizationContradictsLaw(Exception):
    """The realization artifact asserts an execution fact INCOMPATIBLE WITH A POSITIVE GOVERNED FACT.

    DELIBERATELY NOT A `ProofRefusal`, for the same structural reason `UnsupportedByThisProfile` is
    not one, and the line is the same line: the three refusals above are FINDINGS OF LAW OR OF STATE
    — the request was answered and the answer was no, which is why they carry REFUSE. This says the
    request was NEVER ANSWERED: the two artifacts disagree, so nothing was executed and there is no
    verdict about the data to report. That is an ERROR, and a class that cannot be caught by the
    governed handler cannot be accidentally given a governed jurisdiction by it.

    NOT `WantOfState`, WHICH IS THE CONFUSION THIS CLASS EXISTS TO PREVENT. `want_of_state` promises
    that RE-MATERIALIZATION may resolve it. Re-materializing the same data cannot repair a claim
    that contradicts the governing law — the material is not what is wrong — so that remedy would
    send an operator to do work that cannot possibly help.

    NOT `WantOfLaw` either: the law is established and says the OPPOSITE of the claim, which is not
    an absence of licence. And not `unsupported`: the profile implemented the thing; the artifact is
    wrong.

    Reaches the wire as `realization_contradicts_law` — `(ERROR, None, REALIZATION)`, minted
    2026-09-14 — carrying NO alternatives, because the vocabulary has no lawful spelling for
    "correct or replace the realization mapping" and the nearest one bundles it with a data re-pull.

    THE DETAIL NAMES THE FACT, NOT THE IMPLEMENTATION: the family's canonical reference, the
    governed law, the realization's claim, and the contradiction. Opaque family ids and module paths
    are implementation and do not belong in a message an operator reads."""

    def __init__(self, detail: str, *, subject: str = ""):
        self.detail = detail
        self.subject = subject
        where = f" [{subject}]" if subject else ""
        super().__init__(f"RealizationContradictsLaw{where}: {detail}")


class UnsupportedByThisProfile(Exception):
    """NOT a governed verdict — a limit of what this profile implements (ruled 2026-09-12 §7).

    DELIBERATELY NOT A `ProofRefusal`. The three refusals above are findings of law or of state: they
    say the request was answered and the answer was no. This says the request was not answered at
    all. It carries no `jurisdiction`, because attaching one would place a capability gap inside a
    governed jurisdiction and tell an operator their question was unlawful when it was merely
    unimplemented here — and `want_of_state`'s remedy would then send them to re-materialize against
    a path that does not exist.

    THE PROHIBITION, NARROWED (ruled Huayin, 2026-09-14). It read "it must never be mapped to a wire
    reason", which was right about the danger and too wide about the remedy: an exception escaping
    past the server is not an answer either, and a caller who asked a meaningful question learns
    nothing from a transport-level error. The rule that survives is the one that was always doing the
    work — A GOVERNED REFUSAL MAY NEVER BORROW THE CAPABILITY REASON, and a capability limit may
    never borrow a governed one. So:

        · the three `ProofRefusal`s above must never carry `unsupported`;
        · this exception must never carry `want_of_law` or `want_of_state`;
        · the provider/serving boundary MAY translate this into the already-registered wire reason
          `unsupported` — `(ERROR, None, REALIZATION)`, "not implemented in this build (capability)"
          — which mints nothing, changes no mood, and moves no contract version.

    The translation happens at that boundary and nowhere earlier, which is why this stays outside the
    `ProofRefusal` hierarchy: a class that cannot be caught by the governed handler cannot be
    accidentally given a jurisdiction by it.
    """
