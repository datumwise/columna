"""
columna_core.compiler.refusals — the K0 refusal taxonomy, kept deliberately un-collapsed.

Five conditions, never merged into a generic ``LoweringError``. Collapsing them is precisely what
would breach the blast wall: "lowering failed" tells an operator nothing about WHOSE gap it is, and
the whole point of the taxonomy is that the four gap classes answer four different questions and are
owned by four different people.

    InputIdentityMismatch      is this mapping even FOR this publication?   (input authority)
    LogicalMeaningMissing (L)  do we know what this MEANS?                  (authoring/model gap)
    MappingIncomplete     (M)  do we know how that meaning is REALIZED?     (mapping gap)
    UnsupportedCoreCapability (C)  can Core PERFORM it faithfully?          (compiler coverage gap)
    ExecutionRepresentationGap (G)  can the image REPRESENT the law at all? (execution grammar gap)

``InputIdentityMismatch`` sits BEFORE the four gap categories: it is an input-authority condition,
not a lowering outcome, and it is checked before any lowering work begins.

Certification is NOT here, by ruling. ``compile()`` answers "can governed law be faithfully
translated?"; whether a path is licensed on a realization is adjudication's question, asked later.
A K0 compile therefore never emits ``GovernedCertificationMissing`` — the image it produces is
CLOSED, and nothing about it implies admission.
"""
from __future__ import annotations


class CompileRefusal(Exception):
    """A fail-closed compiler refusal. Always carries a category; never a bare message.

    The refusal is the product. A compiler that cannot faithfully translate governed law must say
    which KIND of thing is missing, because that decides who can fix it."""

    #: stable category token — the public name of this condition
    category = "CompileRefusal"

    def __init__(self, detail: str, *, subject: str = ""):
        self.detail = detail
        self.subject = subject
        where = f" [{subject}]" if subject else ""
        super().__init__(f"{self.category}{where}: {detail}")


class InputIdentityMismatch(CompileRefusal):
    """The private mapping is not the realization of this publication.

    Checked FIRST, before any lowering. Without it a valid mapping for ``retail@1.2.0`` could be
    combined with ``retail@1.3.0`` and the compiler would manufacture a valid-looking image for the
    wrong governed meaning — the failure the whole binding exists to prevent."""

    category = "InputIdentityMismatch"


class LogicalMeaningMissing(CompileRefusal):
    """**L** — the governed publication does not carry meaning the compiler needs.

    Fix belongs in authoring. The compiler may not invent the missing fact, and may not reach into
    evidence, profile or Studio state to recover it."""

    category = "LogicalMeaningMissing"


class MappingIncomplete(CompileRefusal):
    """**M** — the meaning is governed, but its physical realization is absent or ambiguous.

    Fix belongs in the private mapping. Note this is NOT a licence to derive the fact: "derivable"
    means derivable while CONSTRUCTING the mapping, never by the compiler at compile time."""

    category = "MappingIncomplete"


class UnsupportedCoreCapability(CompileRefusal):
    """**C** — meaning and realization are both present, but Core cannot perform the operation
    faithfully (or K0 does not yet cover it).

    Distinct from **G**: the representation could hold it; this build cannot compute it correctly.
    Approximating instead of refusing is forbidden unless approximation is itself an explicit
    governed contract, and K0 does not invent one."""

    category = "UnsupportedCoreCapability"


class ExecutionRepresentationGap(CompileRefusal):
    """**G** — the Core execution image cannot represent the required law at all.

    No lowering can target a slot that does not exist. The authored law stays authoritative; Core
    must eventually gain a representation that carries it, or keep refusing to compile it."""

    category = "ExecutionRepresentationGap"


#: Every category this module can raise. A completeness test pins this against the class set, for
#: the same reason the server pins its LoadCondition codes: a category that exists but is not
#: enumerated is a condition that vanishes from the report rather than surfacing in it.
CATEGORIES = (
    InputIdentityMismatch.category,
    LogicalMeaningMissing.category,
    MappingIncomplete.category,
    UnsupportedCoreCapability.category,
    ExecutionRepresentationGap.category,
)
