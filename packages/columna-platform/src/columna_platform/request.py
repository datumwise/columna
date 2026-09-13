"""columna_platform.request — ANALYTICAL REQUEST RESOLUTION, from governed law alone.

THE QUESTION THIS MODULE ANSWERS (ruled Huayin, 2026-09-12 §5, "the real proof"): a public Frame-QL
request arrives as syntax; the successor path needs `AnalyticalIdentity(family_id, anchor)`. Getting
from one to the other is where a successor path either earns its independence or quietly borrows the
legacy ontology it was built to replace.

WHAT THIS MODULE MAY USE. The parsed statement — series text and the `AT {…}` levels — and the
GOVERNED PUBLICATION. Nothing else. In particular it may not use `model.py`'s measure/member
resolution, the planner's identity logic, a `.cml` meaning lookup, fuzzy matching, a server-local
convenience map, or a fixture special case. The rule behind the list: **the successor may take the
SHAPE of the request from the language, and its MEANING only from governed law.**

THE RESOLUTION IS ONE GOVERNED FUNCTION, NOT A MAP BUILT HERE. `GovernedPublicationV2.
resolve_reference` already exists and already carries the rule — name → at most one family, one
direction only, canonical reference or declared alias. This module calls it. Writing a second
name→family map here would be exactly the "convenience map" the ruling forbids, and it would be a
second enumeration of a rule the publication format already owns.

AMBIGUITY IS NOT DECIDED HERE — IT IS IMPOSSIBLE HERE. `parse_publication` refuses at parse time if
two families answer to one reference (§2.2: "two distinct active identities cannot be hidden under
one ambiguous canonical reference"). So the "more than one governed match" case cannot reach this
module: an ambiguous artifact does not parse, and a publication that parsed has already proved the
uniqueness this resolver depends on. Re-checking it here would duplicate a rule the format owns and
would suggest the guarantee were weaker than it is. The upstream refusal is pinned by test instead.

TWO KINDS OF NO, KEPT APART. A governed defect — no family answers to this reference, no anchor is
declared over these components, the ask moves off the constitutive anchor — is a `WantOfLaw`: a
verdict of governed law, which the wire may report as a governed refusal. A request this profile
simply does not implement — several series, an expression to evaluate — is `UnsupportedByThisProfile`,
which is NOT a governed verdict and must never be dressed as one. A capability limit reported as a
law refusal would tell an operator their question was unlawful when it was merely unimplemented.
"""
from __future__ import annotations

from dataclasses import dataclass

from columna_core.governed.publication import Family, GovernedPublicationV2

from .refusals import UnsupportedByThisProfile, WantOfLaw
from .state import AnalyticalIdentity

#: The declaration kind that carries an anchor's components in the governed logical projection.
ANCHOR = "anchor"


@dataclass(frozen=True)
class ResolvedRequest:
    """What the request turned out to be ASKING FOR, in governed terms.

    `identity` is the whole point; `family` and `column_name` ride along because the caller needs
    them to build the answer and re-deriving them would mean resolving twice."""

    identity: AnalyticalIdentity
    family: Family
    column_name: str


def _declared_anchors(pub: GovernedPublicationV2) -> dict[str, frozenset]:
    """anchor name → its declared component names, read from the governed logical projection.

    The anchor's components are governed facts sitting in the publication's own `anchor`
    declarations. Nothing about dimension levels, hierarchies or `.cml` geometry enters here."""
    out = {}
    for decl in pub.of_kind(ANCHOR):
        components = decl.body.get("components") or []
        names = frozenset(c.get("name") for c in components if isinstance(c, dict) and c.get("name"))
        out[decl.name] = names
    return out


def resolve(pub: GovernedPublicationV2, statement) -> ResolvedRequest:
    """Frame-QL request → `AnalyticalIdentity`, or a refusal that says which kind of no it is.

    `statement` is whatever `columna_core.envelope.parse_statement` returned. This function reads
    exactly two things off it — `series` and `anchor` — and treats both as SYNTAX, never as meaning.
    """
    # ── the series token ────────────────────────────────────────────────────────────────────────
    if len(statement.series) != 1:
        raise UnsupportedByThisProfile(
            f"this path plans ONE governed reference and this request names {len(statement.series)}; "
            f"a multi-column frame is not a governed defect, it is unimplemented here")

    token = statement.series[0].expr.strip()
    family = pub.resolve_reference(token)
    if family is None:
        # NO GUESS. Not the nearest name, not a case-folded one, not a prefix. A reference the
        # publication does not carry names no governed analytical object, and inventing one here
        # would be this profile deciding what the author meant.
        raise WantOfLaw(
            f"no governed family answers to the reference {token!r} in publication "
            f"{pub.ref.manifold_id}@{pub.ref.version}; this path resolves a series to a governed "
            f"family by canonical reference or declared alias, and does not evaluate expressions "
            f"or guess at near matches", subject=token)

    # ── the anchor ──────────────────────────────────────────────────────────────────────────────
    requested = frozenset(statement.anchor)
    if not requested:
        raise WantOfLaw(
            f"the grand-total frame `AT {{}}` asks for {family.canonical_reference!r} projected off "
            f"its constitutive anchor {family.constitutive_anchor!r}, which is MOVEMENT and requires "
            f"a positive governed licence; this pre-flight carries none", subject=family.family_id)

    declared = _declared_anchors(pub)
    matches = sorted(name for name, components in declared.items() if components == requested)
    if not matches:
        raise WantOfLaw(
            f"no governed anchor is declared over the components {sorted(requested)}; the "
            f"publication declares {_spell_anchors(declared)}", subject=family.family_id)
    if len(matches) > 1:                                              # pragma: no cover - see below
        # Two anchors over one component set. The format does not forbid it today, so this profile
        # refuses rather than picking: an arbitrary choice here would bind material state to an
        # anchor the author never named. Uncovered because the case cannot be built from a
        # publication this proof is authorized to write; recorded as a finding rather than faked.
        raise WantOfLaw(
            f"components {sorted(requested)} are declared by {matches}; this profile will not "
            f"choose between two governed anchors", subject=family.family_id)

    anchor = matches[0]
    if anchor != family.constitutive_anchor:
        raise WantOfLaw(
            f"{family.canonical_reference!r} is constituted at {family.constitutive_anchor!r} and "
            f"this asks it at {anchor!r}; moving a family between anchors requires a positive "
            f"governed movement licence, which this pre-flight carries none of", subject=family.family_id)

    return ResolvedRequest(
        identity=AnalyticalIdentity(family_id=family.family_id, anchor=anchor),
        family=family,
        column_name=statement.series[0].alias or token,
    )


def _spell_anchors(declared: dict) -> str:
    """Spell the declared anchors for a refusal message: `sale_at{day*store}`, sorted."""
    return ", ".join(f"{name}{{{'*'.join(sorted(c))}}}" for name, c in sorted(declared.items())) or "none"
