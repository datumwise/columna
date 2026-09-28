"""
columna_platform.kernel.standing — analytical instance, compatibility, and refusal.

**THE ONE RULE THIS MODULE EXISTS TO ENFORCE: PHYSICAL AVAILABILITY IS NOT ANALYTICAL AUTHORITY.**

An MME holds objects. Holding one is a fact about a cache; whether it may be SERVED at a location, or
may SEED a continuation to another, or may FILL A ROLE in an expression's basis, are three separate
governed questions — and every one of them can be `no` about an object that is sitting right there.
This module carries the vocabulary those `no`s are said in.

WHY AN `AnalyticalInstance` IS NOT A CACHE KEY
----------------------------------------------
Two retained states over the same family at the same anchor can still be **jointly meaningless**: ToD
v8 §11.5.2's basis is *"a matching SUM and COUNT with the same participating contributions in both
components"*, and the word doing the work is MATCHING. So a retained value carries the instance it was
constituted under — the world, the participation, the scope, and a witness of the constitution — and
combination asks whether two instances agree BEFORE any arithmetic happens. A key that merely
distinguished objects would let the engine combine two that should never have met.

The three questions are asked in three places and answered with the same `Compatibility`, so a
consumer never has to interpret a bare Boolean.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

# ── how an answer was reached. Reported, because the route is a governed fact. ────────────────────
ROOT = "root"                     # served from F@R_F, the canonical continuation origin
CONTINUED = "continued"           # merged down from a finer retained state
CACHED = "cached"                 # an exact retained hit at the asked location
EVALUATED = "evaluated"           # an expression computed from a sufficient basis
REFUSED = "refused"
ROUTES = frozenset({ROOT, CONTINUED, CACHED, EVALUATED, REFUSED})


@dataclass(frozen=True)
class AnalyticalInstance:
    """**What makes two retained states combinable.** Not an identity and not a key.

    `constitution` is an opaque witness of the governed constitution the state was formed under — a
    digest, a publication version, anything the authoring side can make stable. It is compared and never
    interpreted, which is what keeps this kernel free of a serialization format it does not yet have."""

    universe: str
    participation: str
    constitution: str
    scope: Optional[str] = None

    def compatible_with(self, other: "AnalyticalInstance") -> "Compatibility":
        if self.universe != other.universe:
            return Compatibility(False, "different-universe",
                                 f"{self.universe!r} vs {other.universe!r}: two worlds' values are "
                                 f"not contributions to one quantity")
        if self.participation != other.participation:
            return Compatibility(
                False, "different-participation",
                f"{self.participation!r} vs {other.participation!r}. These states ranged over "
                f"different contributions, so they are individually valid and jointly meaningless — "
                f"combining them would produce a number that is about no population")
        if self.scope != other.scope:
            return Compatibility(False, "different-scope",
                                 f"{self.scope!r} vs {other.scope!r}")
        if self.constitution != other.constitution:
            return Compatibility(
                False, "different-constitution",
                f"{self.constitution!r} vs {other.constitution!r}: the governed constitution moved "
                f"between these two states, so one of them is stale rather than alternative")
        return Compatibility(True, "matching", "same world, participation, scope and constitution")


@dataclass(frozen=True)
class Compatibility:
    holds: bool
    code: str
    detail: str

    def __bool__(self) -> bool:
        return self.holds


@dataclass(frozen=True)
class Refusal:
    """A governed `no`, said in a way a caller can act on: a code to branch on, a subject, and the
    reason in the theory's own terms. **Never an exception on the serving path** — an unanswerable ask
    is a capability limit, and raising would make it look like a defect in the artifact."""

    code: str
    subject: str
    detail: str

    def __str__(self) -> str:
        return f"[{self.code}] {self.subject}: {self.detail}"


@dataclass(frozen=True)
class Disclosure:
    """Something true about an answer that the answer itself does not carry — an approximation's error
    bound, a route that went through a non-root materialization. **Rides with the value, always**: a
    disclosure a caller can drop is a disclosure that will be dropped."""

    code: str
    detail: str


__all__ = ["CACHED", "CONTINUED", "EVALUATED", "REFUSED", "ROOT", "ROUTES", "AnalyticalInstance",
           "Compatibility", "Disclosure", "Refusal"]
