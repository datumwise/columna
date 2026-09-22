"""columna_platform.native_request — ANALYTICAL REQUEST RESOLUTION over a NATIVE v3 publication.

C3 of the native-consumer sequence, and the first operation beyond visibility and availability:
**a public Frame-QL request arrives as syntax, and the native path needs `AnalyticalIdentity`.**

THIS IS A SECOND RESOLVER, NOT A DEEPER `request.py`. `request.resolve` matches an ask against every
DECLARED anchor of a v2 publication and returns the matching declaration's NAME. Natively there are
no anchor declarations to match against and no name to return: a Case-S anchor is derived from a
constitution, `R-C` makes a derived anchor structurally unwritable, and many governed tokens may
denote one anchor. A shared code path would have to keep the declaration namespace alive to have
somewhere to look.

> **THE SHIFT, IN ONE LINE: the request's coordinate set IS the anchor.** `AT {berth * day}` *is*
> `A = {berth, day}`, resolved inside `U`. Nothing is looked up, so nothing can be ambiguous.

That dissolves a live v2 refusal rather than porting it. `request.resolve` refuses when two declared
anchors carry one component set — *"this profile will not choose between two governed anchors"*,
marked `# pragma: no cover` because *"the case cannot be built from a publication this proof is
authorized to write."* **In the native fixture it is the ordinary case**: `berthing_at` and
`berth_day` both denote `{berth, day}`. A consumer that kept name-matching would refuse a lawful
publication on its first request. Here there is no name to match, so the refusal has no subject.

WHAT THIS MODULE MAY USE. The parsed statement — series text and the `AT {…}` coordinate set — and
the NATIVE RESOLVED MODEL. Nothing else. In particular: no anchor declaration, no publication-global
anchor map, no `universe.body.anchor`, no basis, no global coordinate namespace, no `.cml` meaning
lookup, no physical grain, no mapping, no uniqueness evidence, and no cross-universe search. **Most
of that list is not refused here — it is unreachable**: the parameter is a `NativePublication`, and
none of those objects exists on it.

THE MOVEMENT BOUNDARY IS OBSERVED, NOT CROSSED (ruling 3, 2026-09-22). §4's division is the whole
of what this module uses:

    geometry decides whether a target analytical location EXISTS;
    governed movement standing decides whether `F` may STAND there.

**THIS MODULE ANSWERS ONLY THE FIRST, AND C4 MOVED THE SECOND OUT OF IT.** As first written, a
coarser ask was refused *here*, for want of governed movement standing. The refusal said the right
thing and said it in the wrong place: resolution answers *what is being asked for*, and whether `F`
may stand there is governed AUTHORITY — a different question, decided against `Law(F)`, which this
module may not see. Refusing here also made the standing question unreachable, so nothing could ever
be asked to license it. The v2 resolver had already drawn this line for its own reasons and states
it in the same words; that agreement is recorded in C4's report rather than treated as a template.

So a coarser ask now RESOLVES — geometry says the location exists, and `target` carries it — and a
NON-PROJECTABLE ask still refuses here, because that is a fact about geometry and not about
standing: if the target cannot be obtained by lawful universe geometry, the problem is not a missing
licence. **No licence object is constructed, nothing is carried forward that names an anchor, and
nothing of the v2 movement implementation is ported.** The native movement contract is derived
later, from the native model.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from columna_core.governed.native import Anchor, Family, NativePublication, Universe

from .refusals import UnsupportedByThisProfile, WantOfLaw
from .request import require_supported_clauses  # noqa: F401 - the request SURFACE is shared
from .state import AnalyticalIdentity


@dataclass(frozen=True)
class NativeResolvedRequest:
    """What the request turned out to be ASKING FOR, in native governed terms.

    **THERE IS NO SECOND LOCATION FIELD, AND THAT IS THE POINT OF C3.** The v2 pair carries the
    resolved identity AND the structural request, and the two are reported independently:
    `plan_result` returns `tuple(statement.anchor)` and `decide_result` returns
    `(identity.anchor,)`. Measured on the shipped v2 fixture, one lawful request yields
    `('store', 'day')` from the pre-flight and `('sale_at',)` from execution — **two answers to
    "where does this value stand"**, which the ruling forbids.

    Natively the divergence is not repaired; **it becomes unstatable.** The two candidate
    representations — the request's coordinate set, and the anchor's name — are not two
    representations of one location. The first IS the location; the second does not exist. So
    `location` below is *defined as* `identity.anchor`, there is no other expression of it anywhere
    on this path, and a future caller cannot reintroduce the divergence by reaching for the other
    one, because there is no other one to reach for."""

    identity: AnalyticalIdentity
    family: Family
    universe: Universe
    column_name: str
    #: The location the ask NAMES, when it is not the family's constitutive one — i.e. this request
    #: is a MOVEMENT. `None` on every non-moving request.
    #:
    #: **IDENTITY STAYS AT THE CONSTITUTIVE ANCHOR HERE, deliberately.** Resolution establishes what
    #: the state is OF and where the family is constituted; whether `F` may stand at the target is a
    #: question of governed authority that resolution cannot answer. So the target rides alongside as
    #: a REQUEST FACT — a geometric one: it is present exactly when the projection exists.
    #:
    #: It is an `Anchor`, not a name, for the same reason `identity.anchor` is: there is no name.
    target: Optional[Anchor] = None

    @property
    def is_moving(self) -> bool:
        return self.target is not None

    @property
    def location(self) -> Anchor:
        """**Where the value stands** if this request is answered — the constitutive anchor, or the
        target once a movement has been adjudicated and performed. Before adjudication it is the
        constitutive anchor, because that is where the state is established.

        One expression, one source: C3's finding is unaffected by the target, because the target is
        not a second rendering of the same location — it is a different location, named by the ask
        and not yet occupied."""
        return self.identity.anchor


def frame_location(anchor: Anchor) -> tuple[str, ...]:
    """The public frame location for a native anchor — **the ONE site that answers this**.

    Sorted constituent references, because an anchor is a SET and a public surface must not present
    an incidental order as meaningful. Deliberately NOT a name: there may be several governed tokens
    denoting this anchor and nothing selects between them, so reporting one would present a
    convention as the location. Reporting `{}` for the scalar anchor is an empty tuple, which is the
    truthful answer and not an absent one."""
    return tuple(sorted(anchor.constituents))


def resolve(pub: NativePublication, statement) -> NativeResolvedRequest:
    """Frame-QL request → `AnalyticalIdentity(family_id, Anchor)`, or a refusal that says which
    kind of no it is.

    `statement` is whatever `columna_core.envelope.parse_statement` returned. Exactly two of its
    fields are read — `series` and `anchor` — and both are treated as SYNTAX, never as meaning.
    """
    # ── the series token ────────────────────────────────────────────────────────────────────────
    if len(statement.series) != 1:
        raise UnsupportedByThisProfile(
            f"this path resolves ONE governed reference and this request names "
            f"{len(statement.series)}; a multi-column frame is not a governed defect, it is "
            f"unimplemented here")

    token = statement.series[0].expr.strip()
    family = pub.resolve_reference(token)
    if family is None:
        # NO GUESS. Not the nearest name, not a case-folded one, not a prefix, and not a
        # `family_id` — identity is not a way of asking.
        raise WantOfLaw(
            f"no governed family answers to the reference {token!r} in publication "
            f"{pub.manifold_id}@{pub.version}; this path resolves a series to a governed family by "
            f"canonical reference or declared alias, and does not evaluate expressions or guess at "
            f"near matches", subject=token)

    # ── F → U ───────────────────────────────────────────────────────────────────────────────────
    # The family fixes the universe, and the universe is the ONLY context in which anything that
    # follows resolves. It is a precondition of resolution, not a component of the identity
    # resolution produces.
    universe = pub.universe(family.universe_reference)
    constitutive = universe.denote(family.anchor_token)
    if constitutive is None:  # pragma: no cover - the reader refuses a dangling token at ingest
        raise WantOfLaw(
            f"family {family.canonical_reference!r} is constituted at {family.anchor_token!r}, "
            f"which denotes nothing in universe {universe.name!r}", subject=family.family_id)

    column_name = statement.series[0].alias or token

    # ── U → A ───────────────────────────────────────────────────────────────────────────────────
    # THE REQUEST'S COORDINATE TOKENS ARE THE CONSTITUENT SET. They are resolved INSIDE `U` — a
    # reference that resolves in another world does not resolve here — and nothing is matched
    # against a declaration, because there is none to match.
    requested = frozenset(statement.anchor)
    unknown = sorted({r for r in requested
                      if universe.constitution.resolve_coordinate(r) is None})
    if unknown:
        raise WantOfLaw(
            f"{unknown} do not resolve as constituents of universe {universe.name!r}, whose closed "
            f"individuation is {list(universe.coordinates)}. Resolution is universe-scoped: a "
            f"coordinate that resolves in another world does not resolve here, and nothing stands "
            f"in for a constituent — not an anchor declaration, not a level, not a physical column, "
            f"not a mapping", subject=family.family_id)

    asked = universe.anchor(requested)
    if asked == constitutive:
        return NativeResolvedRequest(
            identity=AnalyticalIdentity(family_id=family.family_id, anchor=constitutive),
            family=family, universe=universe, column_name=column_name)

    # ── the ask is NOT the constitutive anchor · §4's division, applied ────────────────────────
    if constitutive.refines(asked):
        # GEOMETRY SAYS YES: the projection exists, and exactly what it forgets is computable. That
        # is the whole of what resolution may conclude. Whether `F` may STAND there is decided
        # against `Law(F)` — see `native_law.assert_answerable` — and a location existing is never a
        # licence to occupy it.
        return NativeResolvedRequest(
            identity=AnalyticalIdentity(family_id=family.family_id, anchor=constitutive),
            family=family, universe=universe, column_name=column_name, target=asked)

    # The ask names constituents the family is not constituted over — a FINER or disjoint location.
    # Not movement, and not a standing question at all: a coarser location is reached by forgetting,
    # never by acquiring, so there is nothing here for a licence to license.
    acquired = sorted(asked.constituents - constitutive.constituents)
    raise WantOfLaw(
        f"{family.canonical_reference!r} is constituted at {constitutive}, and this ask stands at "
        f"{asked}, which would require {acquired} this family does not hold. A coarser analytical "
        f"location is reached by FORGETTING constituents, never by acquiring them, so this is not a "
        f"movement awaiting a licence — there is no such location for this family to stand at",
        subject=family.family_id)
