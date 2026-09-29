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

THREE FACTS ABOUT A RETAINED OBJECT, AND THIS MODULE OWNS THE SECOND
--------------------------------------------------------------------
Ruled (Huayin, 2026-09-29, P-1): *"Keep these three things distinct: **ConstitutionWitness** — which governed
analytical constitution this object belongs to; **AnalyticalInstance / data-state identity** — which actual
root/evidence state this retained material belongs to; **Realization standing** — which physical/provider/codec
realization produced or carries it. Do not collapse them into one version/freshness token."*

    constitution   `witness.py`       COMPUTED per object, and carried on the `RetentionKey` — **not here.**
    data state     **here**           `data_state` — which root/evidence state this material came from.
    realization    `realization.py`   `RealizationStanding`, also on the key. Absent from this record: a
                                      value produced by two providers under one constitution and one data
                                      state is the same analytical instance, differently realized.

**WHY THE PER-OBJECT WITNESS IS NOT A FIELD OF THIS RECORD, WHICH IS A CORRECTION MADE WHILE BUILDING P-1.**
The first attempt put the computed `ConstitutionWitness` digest here, in the old `constitution` slot. It
broke every expression immediately, and the breakage was the lesson: `Revenue`'s witness and `OrderCount`'s
witness necessarily DIFFER — different laws, different value domains — so `compatible_with` declared the
canonical SUM/COUNT basis jointly unusable on `different-constitution`. Comparing two different objects'
own constitution witnesses is a category error. The per-object witness answers *"has THIS object's
constitution moved"*, which is a staleness question about one identity, and it is enforced where that
question belongs: at candidate resolution, keyed on the witness. What this record carries is
`constitution_context` — the SHARED governed constitution two different objects were constituted under,
which is a publication-level fact and the only sense in which "same constitution" spans two identities.

`data_state` exists because *"same constitution + new source/root data → same ConstitutionWitness, different
AnalyticalInstance"* is otherwise unstatable: before it, a reload produced an instance identical in every
field, so two evidence states silently overwrote one another in the store. It is an OPAQUE token supplied by
whoever establishes the material — a load id, an evidence digest, a snapshot reference. **No format is
invented for it here** (P-1: *"do not invent persistence format or serialization yet"*), and nothing in this
kernel parses it; it is compared and reported, never interpreted.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Optional

# ── how an answer was reached. Reported, because the route is a governed fact. ────────────────────
ROOT = "root"                     # served from F@R_F, the canonical continuation origin
CONTINUED = "continued"           # merged down from a finer retained state
CACHED = "cached"                 # an exact retained hit at the asked location
EVALUATED = "evaluated"           # an expression computed from a sufficient basis
REFUSED = "refused"
ROUTES = frozenset({ROOT, CONTINUED, CACHED, EVALUATED, REFUSED})

#: **No root/evidence state is CLAIMED.** Not a wildcard and not unknown-ness: an instance carrying it is
#: attributable to no particular established material, and two such instances are the same unstated state.
UNSTATED_DATA_STATE = "data:unstated"

#: The shared governed-constitution context, when nothing has stated one. See `AnalyticalInstance`.
CONSTITUTION_CONTEXT_UNSTATED = "context:unstated"


@dataclass(frozen=True)
class AnalyticalInstance:
    """**What makes two retained states combinable.** Not an identity and not a key.

    `constitution` is an opaque witness of the governed constitution the state was formed under — a
    digest, a publication version, anything the authoring side can make stable. It is compared and never
    interpreted, which is what keeps this kernel free of a serialization format it does not yet have.

    **`manifold` IS FIRST AND IS CHECKED FIRST** (ruled Huayin, 2026-09-28): *"One Columna installation
    supports many Manifolds… Each Manifold has its own MME jurisdiction… Shared infrastructure does not
    imply shared analytical authority. A family, expression, analytical instance, retained state, cache,
    or compatibility judgment belongs to exactly one Manifold unless an explicit cross-Manifold governed
    bridge says otherwise."*

    It lives HERE, on the combinability witness, rather than only on the engine — because the danger is
    not two engines, it is one shared Arrow/DataFusion runtime under two Manifolds that happen to use the
    same family name. Putting the Manifold on the instance makes such states **different retained
    objects** and makes their combination a refusal, by the same mechanism that already separates two
    participations. Cross-Manifold composition is then an explicit governed crossing and cannot happen
    incidentally."""

    manifold: str
    universe: str
    participation: str
    #: **THE SHARED GOVERNED CONSTITUTION CONTEXT — publication-level, and NOT the per-object
    #: `ConstitutionWitness`** (which is computed in `witness.py` and carried on the `RetentionKey`). This is
    #: the only sense of "same constitution" that spans two DIFFERENT identities, which is what this record
    #: is for: it is compared when asking whether a `Revenue` state and an `OrderCount` state may combine.
    #:
    #: **NOTHING COMPUTES IT YET**, and it is named rather than silently defaulted for that reason: the
    #: kernel has no publication object, so every object is constituted under one unstated context. When a
    #: governed publication witness exists it lands here — and it lands here WITHOUT becoming a freshness
    #: token, because freshness of the material is `data_state` and supersession of a declaration is the
    #: witness on the key.
    constitution_context: str = CONSTITUTION_CONTEXT_UNSTATED
    scope: Optional[str] = None
    #: **WHICH ROOT/EVIDENCE STATE this material belongs to.** Opaque, supplied at establishment, never
    #: parsed. `UNSTATED_DATA_STATE` means no evidence state is CLAIMED — which is a legible standing and
    #: not a wildcard: two objects that both claim nothing are the same unstated state.
    data_state: str = UNSTATED_DATA_STATE

    def with_data_state(self, data_state: str) -> "AnalyticalInstance":
        """This instance, attributed to one root/evidence state. The single place that stamp is applied."""
        return replace(self, data_state=data_state)

    def same_but_for_data_state(self, other: "AnalyticalInstance") -> bool:
        """**Every governed axis agrees; only the evidence state may differ.** Two loads of one constitution
        answer `True` here and are still different instances — which is exactly the distinction P-1 asks to
        keep, and it is what lets candidate resolution find both and then refuse to guess between them."""
        return (self.manifold, self.universe, self.participation, self.scope,
                self.constitution_context) == (other.manifold, other.universe, other.participation,
                                               other.scope, other.constitution_context)

    def compatible_with(self, other: "AnalyticalInstance") -> "Compatibility":
        if self.manifold != other.manifold:
            return Compatibility(
                False, "different-manifold",
                f"{self.manifold!r} vs {other.manifold!r}. Each Manifold owns its own MME jurisdiction, "
                f"and shared infrastructure does not imply shared analytical authority. Composing across "
                f"Manifolds is an EXPLICIT governed crossing — it is not an incidental consequence of one "
                f"runtime, one store, or two worlds choosing the same name")
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
        if self.constitution_context != other.constitution_context:
            return Compatibility(
                False, "different-constitution-context",
                f"{self.constitution_context!r} vs {other.constitution_context!r}: these two states were "
                f"constituted under different governed constitutions, so one of them is stale rather than "
                f"alternative. **THIS IS THE PUBLICATION-LEVEL FACT AND NOT A PER-OBJECT WITNESS**: two "
                f"different families never share a per-object constitution witness, and comparing theirs "
                f"would declare the canonical SUM/COUNT basis unusable")
        if self.data_state != other.data_state:
            # **A SEPARATE CODE, BECAUSE IT IS A SEPARATE FACT.** The constitution is the same one; what
            # differs is which root/evidence state each side ranged over. Conservative, and the asymmetry
            # is the usual one: withholding a combination that may have been lawful costs an answer, while
            # allowing one across two evidence states reports a number about neither.
            return Compatibility(
                False, "different-data-state",
                f"{self.data_state!r} vs {other.data_state!r}: ONE governed constitution, TWO root/evidence "
                f"states. These are not stale-versus-current and neither is wrong — they range over "
                f"different established material, so combining them would produce a number about neither. "
                f"Re-establish both sides from one evidence state, or ask for one explicitly")
        return Compatibility(True, "matching",
                             "same world, participation, scope, constitution and data state")


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


__all__ = ["CACHED", "CONSTITUTION_CONTEXT_UNSTATED", "CONTINUED", "EVALUATED", "REFUSED", "ROOT",
           "ROUTES", "UNSTATED_DATA_STATE", "AnalyticalInstance", "Compatibility", "Disclosure",
           "Refusal"]
