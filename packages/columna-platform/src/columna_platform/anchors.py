"""The ONE reader of a governed anchor declaration — and the one place a malformation is judged.

WHY THIS MODULE EXISTS. Three functions parsed the same `anchor` declaration out of the governed
logical projection, each keeping the part it needed and each judging malformation differently:

    movement._declared_components   ordered names   REFUSED a non-list `components` (WantOfLaw)
    serving.declared_components     name -> type    returned {} silently (`... or []`)
    request._declared_anchors       name sets       returned an empty set silently

They answer three genuinely different questions and their APIs are RIGHT to differ — a movement
licence needs identity and DECLARATION ORDER, admission needs the governed TYPE, request resolution
needs a set to match an ask against. What was wrong was not the three views; it was **three
parsers**, so "what counts as a malformed anchor declaration" had three answers and the strictest
one was reachable from only one of three doors.

SO THE VIEWS STAY DISTINCT AND THE PARSING DOES NOT. `declared_coordinates` is the canonical read;
everything else in this module is a projection of it, and no other module reaches into the raw
component list again — a control asserts that this is the only file in the package that names the
key at all. That is not a DRYness argument — it is so that ONE governed
declaration has ONE malformation policy, and so a future fourth consumer inherits it instead of
writing a fourth interpretation of the same JSON.

WHERE A MALFORMATION LANDS, AND WHY IT IS `WantOfLaw`. A publication whose anchor declaration is
absent, unparseable or nameless has not established the analytical point its families are
constituted at. That is a defect in the GOVERNED artifact: re-materializing cannot supply it, so it
must never reach a caller as a want-of-state blaming the carrier. It is caught HERE, at the reading
boundary, rather than relied upon to surface downstream — before the repair a malformed declaration
happened to be caught by request resolution, which was luck about ordering, not a guarantee.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Tuple

from .refusals import WantOfLaw

#: The declaration kind that carries an anchor's components in the governed logical projection.
ANCHOR = "anchor"


@dataclass(frozen=True)
class CoordinateDeclaration:
    """One governed coordinate of an anchor, as the publication declares it.

    TWO FIELDS, AND THEY ARE NOT THE SAME KIND OF FACT. `name` is what the coordinate IS — the
    publication must supply it, and a declaration without one is malformed. `governed_type` is what
    the coordinate is declared to BE, and it is `Optional` because a publication may lawfully omit
    it today; a profile that cannot admit an untyped coordinate refuses it as a CAPABILITY limit
    (see `admission`), which is a different thing from the declaration being malformed."""

    name: str
    governed_type: Optional[str]


def declared_coordinates(pub, anchor: str) -> Tuple[CoordinateDeclaration, ...]:
    """THE CANONICAL READ. The anchor's coordinates, in DECLARATION ORDER, validated once.

    Order is preserved and is load-bearing: it reaches `MovementLicence.source_components` and is
    rendered in a licence's description (`sale_at(store*day)`), so a reader that sorted or
    set-ified here would quietly change evidence a human is shown.

    Every refusal below is a `WantOfLaw` against the ANCHOR: the governed artifact has not
    established the analytical point, and no re-realization supplies it."""
    for decl in pub.of_kind(ANCHOR):
        if decl.name != anchor:
            continue
        body = decl.body or {}
        if "components" not in body:
            raise WantOfLaw(
                f"anchor {anchor!r} declares no component list; an anchor without components "
                f"establishes no analytical point for a family to be constituted at",
                subject=anchor)
        comps = body["components"]
        if not isinstance(comps, list):
            raise WantOfLaw(
                f"anchor {anchor!r} declares `components` as {type(comps).__name__}, not a list; "
                f"the governed declaration cannot be read", subject=anchor)
        out, seen = [], set()
        for i, c in enumerate(comps):
            if not isinstance(c, dict):
                raise WantOfLaw(
                    f"anchor {anchor!r} component #{i} is {type(c).__name__}, not a declaration",
                    subject=anchor)
            name = c.get("name")
            if not isinstance(name, str) or not name.strip():
                raise WantOfLaw(
                    f"anchor {anchor!r} component #{i} declares no non-empty name ({name!r}); a "
                    f"coordinate nobody named cannot be matched against material or against an ask",
                    subject=anchor)
            if name in seen:
                # NOT IN THE REQUIRED POLICY, AND INCLUDED DELIBERATELY. Two declarations of one
                # coordinate is a malformation of the same declaration, and a reader that accepted
                # it would silently let the LAST one win — deciding, in a parser, which governed
                # type a coordinate has. Reported rather than assumed.
                raise WantOfLaw(
                    f"anchor {anchor!r} declares component {name!r} more than once; the governed "
                    f"declaration does not say which is the coordinate", subject=anchor)
            seen.add(name)
            out.append(CoordinateDeclaration(name=name, governed_type=c.get("type")))
        return tuple(out)
    raise WantOfLaw(f"the publication declares no anchor {anchor!r}", subject=anchor)


def declared_coordinate_names(pub, anchor: str) -> Tuple[str, ...]:
    """The ORDERED names — the movement view. Derived, never re-parsed."""
    return tuple(c.name for c in declared_coordinates(pub, anchor))


def declared_coordinate_types(pub, anchor: str) -> Dict[str, Optional[str]]:
    """`name -> governed type` — the admission view. Derived, never re-parsed.

    A plain `dict` and not the tuple above because admission asks a LOOKUP question — "what is this
    coordinate governed as?" — about a coordinate it already has in hand from the carrier. Insertion
    order still follows the declaration, so nothing is lost by taking this view."""
    return {c.name: c.governed_type for c in declared_coordinates(pub, anchor)}


def declared_anchor_names(pub) -> Dict[str, frozenset]:
    """`anchor name -> its declared coordinate names` for EVERY anchor — the request view.

    VALIDATES EVERY ANCHOR, INCLUDING ONES THE ASK DOES NOT NAME, and that is a deliberate widening
    recorded rather than slipped in: request resolution matches an ask against ALL declared anchors,
    so it reads all of them, and a publication carrying one malformed anchor declaration is a
    malformed publication whichever anchor was asked for. The alternative — validate only the anchor
    that happens to match — would make the malformation policy depend on the question, which is the
    condition this module exists to end."""
    return {decl.name: frozenset(declared_coordinate_names(pub, decl.name))
            for decl in pub.of_kind(ANCHOR)}
