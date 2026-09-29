"""
columna_platform.kernel.realization — **the physical provider profile. THE OTHER HALF OF THE SPLIT.**

`law.py` is the semantic authority: what a law ASSERTS, what it composes under, whether its closure is
edge-relative, what basis it needs. This module is what a particular provider can actually DO about it,
and the two are separate objects because ToD v8 §8.7 puts them in different jurisdictions and because
§4.1's rule needs somewhere to bite: **a backend's inability does not remove a law.**

That rule is executable here rather than stated. A law with no realization in the active profile is
LAWFUL AND UNSERVABLE, and the MME refuses it as a *realization* limit naming the provider — never as a
governed absence, which would send a steward to fix a declaration that is correct. (That confusion is
exactly what V8-0 found at Core's C7 seam and V8-1 found at its family lookup; it is not rebuilt here.)

WHAT IS AND IS NOT HERE
-----------------------
Here: `contribute` (raw occurrences → a value at `R_F`), `merge` (the composition, executably),
`identity` (the empty-fibre fold, where the algebra has one), and `apply` (an expression constructor over a
role-keyed basis). All of it per-provider by construction.

**THERE IS NO `finalize`, AND THAT IS A RULING, NOT AN OMISSION (E-3, 2026-09-29).** The field existed
from the start, was never populated and never read, and the question E-3 was asked is whether it named any
legitimate *family-level* responsibility under v8. It does not, for a reason the v8 model makes structural:
a structured family law names its finalizer by governed law name (`HLL_SKETCH.finalized_by ==
"HLL_ESTIMATE"`), and that named law is itself a law with its own realization, whose `apply` IS the
finalization. So finalization is already realized — one level up, on the CONSTRUCTOR, where the law that
licenses it lives. A `finalize` on the FAMILY's realization would be a **second route from family state to
a displayed number, owned by a provider and authorised by no law** — which is the exact defect class §4.1
and §8.7 exist to prevent, and it would be reachable without ever consulting `finalized_by`. Two paths to
one number is how they come to disagree.

It was also strictly weaker than the `apply` it duplicated: `Callable[[Any], Any]` takes one payload and no
parameters, so a provider using it could not express a parameterised finalizer at all — and sketch
parameters are compatibility-bearing.

The concept's correct residue is already in the code, on the columnar half: `ExecutionCapability.finalizes`
is **derived** from a capability's value-form transition (`STRUCTURED → SCALAR`) and asserted nowhere. That
is what "is a finalizer" should be — a property read off a declaration, not a slot a provider can fill.
Retiring the field brings this half of the split into agreement with that one.

Not here, and deliberately: `operand_domains`, `result_domain`, the composition's ALGEBRA, the
continuation region, the required basis. A provider that could state those would be a second semantic
authority wearing the clothes of the first — which is the defect the V8-1 reconnaissance measured in
Core's `operators.py` and is the reason this file is thin.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Iterable, Mapping, Optional

from .geometry import KernelRefusal


@dataclass(frozen=True)
class RealizationStanding:
    """**WHICH PHYSICAL REALIZATION produced or carries a value — the third of P-1's three facts.**

    Ruled (Huayin, 2026-09-29): constitution, data state and realization *"remain separately reasoned even
    if a later retention key combines references to all three."* This is the third, as an object rather than
    a bare provider string, so that it has somewhere to grow (a codec, a format, a compression) without any
    of that leaking into the analytical instance.

    It is **not** identity and **not** analytical standing: two values over one constitution and one
    evidence state, produced by two providers, are the same analytical quantity differently realized. What
    it distinguishes is interchangeability of the MATERIAL — *"a value produced by an approximate provider is
    not interchangeable with one produced by an exact one"* — which is why it is an axis of `RetentionKey`
    and of nothing else.

    `carrier` names the carriage, not a persistence format: P-1 stops short of Parquet/Iceberg/Postgres, so
    the only carriers that exist today are in-memory ones."""

    provider: str
    carrier: str = "in-memory"

    @property
    def token(self) -> str:
        return f"{self.provider}/{self.carrier}"

    def __str__(self) -> str:
        return self.token


@dataclass(frozen=True)
class Realization:
    """One law, as one provider can execute it. Every field is optional except the law it realizes,
    because which of them a law NEEDS is the law's business and not this record's."""

    law: str
    #: raw operand values for ONE root cell → the family value payload. `None` for a law that is only
    #: ever reached by composition or finalization.
    contribute: Optional[Callable[[Iterable[Any], Mapping[str, Any]], Any]] = None
    #: the composition, executably. Required for anything that continues.
    merge: Optional[Callable[[Any, Any], Any]] = None
    #: the empty-fibre fold value, where the algebra has an identity.
    identity: Optional[Callable[[], Any]] = None
    #: an expression constructor over a role-keyed basis of family payloads → the expression's value.
    apply: Optional[Callable[[Mapping[str, Any], Mapping[str, Any]], Any]] = None
    note: str = ""


class ProviderProfile:
    """The realizations one provider offers. **A profile, not an authority.**"""

    def __init__(self, name: str, realizations: Iterable[Realization]) -> None:
        self.name = name
        self._by_law: dict[str, Realization] = {}
        for r in realizations:
            if r.law in self._by_law:
                raise KernelRefusal("duplicate-realization", name,
                                    f"law {r.law!r} is realized twice in one profile")
            self._by_law[r.law] = r

    def __contains__(self, law: str) -> bool:
        return law in self._by_law

    def realizes(self, law: str) -> bool:
        return law in self._by_law

    def of(self, law: str) -> Realization:
        r = self._by_law.get(law)
        if r is None:
            raise KernelRefusal(
                "unrealized-law", self.name,
                f"law {law!r} has no realization in provider profile {self.name!r}. The law is LAWFUL "
                f"and this build cannot serve it — a backend's inability does not remove a law (ToD v8 "
                f"§4.1). This is a REALIZATION limit, not a governed absence, and its remedy is a "
                f"provider rather than a correction to the declaration.")
        return r

    def capability(self, law: str, what: str) -> Callable:
        r = self.of(law)
        fn = getattr(r, what, None)
        if fn is None:
            raise KernelRefusal(
                "unrealized-capability", self.name,
                f"provider {self.name!r} realizes law {law!r} but supplies no {what!r}. The capability "
                f"the ask needs is absent from this profile; the law is unchanged.")
        return fn

    @property
    def laws(self) -> tuple[str, ...]:
        return tuple(sorted(self._by_law))


__all__ = ["ProviderProfile", "Realization", "RealizationStanding"]
