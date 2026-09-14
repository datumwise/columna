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

from .anchors import ANCHOR, declared_anchor_names   # noqa: F401 - ANCHOR re-exported
from .refusals import UnsupportedByThisProfile, WantOfLaw
from .state import AnalyticalIdentity

# `ANCHOR` moved to `anchors`, which owns the governed reading; it is re-exported here because it
# WAS a public name of this module and removing a name is a separate decision from moving its
# definition. Checked at the time of the move: nothing outside `anchors` references it today
# (`serving` did, and no longer needs to), so this re-export is a courtesy, not a load-bearing seam.
# There is deliberately only ONE definition of it.


@dataclass(frozen=True)
class ResolvedRequest:
    """What the request turned out to be ASKING FOR, in governed terms.

    `identity` is the whole point; `family` and `column_name` ride along because the caller needs
    them to build the answer and re-deriving them would mean resolving twice."""

    identity: AnalyticalIdentity
    family: Family
    column_name: str


#: THE REQUEST VIEW: `anchor name -> its declared coordinate names`, as SETS, for every anchor.
#: Resolution matches an ask against the declarations, and a set is what an ask is — `AT {store*day}`
#: names no order. Nothing about dimension levels, hierarchies or `.cml` geometry enters here.
#:
#: DERIVED, NOT RE-PARSED (2026-09-14). This was the third parser of the same `anchor` declaration
#: and the one whose leniency was load-bearing by accident: a malformed declaration silently became
#: an empty set here, and the refusal a caller actually saw — "no governed anchor is declared over
#: the components [...]" — was correct in jurisdiction but only because this happened to run first.
#: That was luck about ordering. The canonical reader refuses at the reading boundary instead.
_declared_anchors = declared_anchor_names


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


# ══ REQUEST COMPLETENESS — no accepted clause may simply be unread ════════════════════════════
#
# THE INVARIANT (ruled Huayin, 2026-09-14): every syntactic part of a request accepted into
# successor execution is either CONSUMED by governed resolution or EXPLICITLY REJECTED as
# unsupported. A clause may not be parsed, carried, and then ignored.
#
# WHY THIS IS A CHECK AND NOT A CONVENTION. `Statement` has nine fields and this profile reads two.
# The other seven were accepted and discarded, so a request carrying `WHERE store = 'nowhere'` was
# answered with every row — an affirmative serve for a question nobody asked (OF-53). Nothing
# failed: not a test, not a gate, not a type. A profile is entitled to implement a subset of the
# language; it is not entitled to accept the rest and answer anyway.
#
# AND WHY THE PARTITION IS COMPUTED RATHER THAN LISTED. The same defect was already found once, for
# `from_manifold`, and repaired for that field alone (`tools._resolve_for_request`, P1-19) — the
# class stayed open because the fix was per-field. So the rule here is stated over the WHOLE field
# set: anything not classified below is unknown, and an unknown field fails closed on every
# request until someone decides what the successor does with it. That is deliberately loud. A new
# `Statement` field turns every successor test red in CI on the first run, which is the cheapest
# possible moment to be asked the question.

#: Fields this profile CONSUMES. `series` names the governed reference; `anchor` names where the
#: value stands. Together they are the whole of `AnalyticalIdentity`.
CONSUMED_CLAUSES = frozenset({"series", "anchor"})

#: Fields consumed BEFORE the provider is reached, by the server's statement-routing boundary.
#: `from_manifold` is read by `tools._resolve_for_request`, which redirects to the runtime the
#: statement names and returns an invalid wire for an unknown one. Not this profile's to re-check:
#: a second consumer would be a second definition of which manifold a request addresses.
CONSUMED_UPSTREAM = frozenset({"from_manifold"})

#: field -> (public spelling, why this profile has no governed reading of it). The reason is part
#: of the data because it reaches the caller: "unsupported" without a reason is not an answer.
UNSUPPORTED_CLAUSES = {
    "where": (
        "WHERE",
        "a restriction narrows which analytical points exist, and this profile has no governed "
        "restriction object for it to mean — lowering it to a physical predicate would decide "
        "population, support and absence by implementation rather than by law"),
    "having": (
        "HAVING",
        "an output-frame predicate restricts the served frame after the fold, and this profile has "
        "no governed account of a partial frame or of what its omissions disclose"),
    "order_by": (
        "ORDER BY",
        "CAP v1 carries no ordering guarantee, so an order served here would be the driver's "
        "incidental one presented as the request's — a claim the profile cannot make"),
    "limit": (
        "LIMIT",
        "a row cap changes which analytical points the answer covers, which is a disclosure "
        "question this profile has no governed answer to; silently serving all of them is worse"),
    "bindings": (
        "WITH",
        "a binding introduces a name whose meaning is evaluated, and this profile evaluates no "
        "expressions — it resolves one governed reference from governed law"),
    "explain": (
        "EXPLAIN",
        "EXPLAIN asks for a plan and NOT an execution; this path has no plan representation, and "
        "executing in answer to it would do the one thing the keyword exists to prevent"),
}


def require_supported_clauses(statement) -> None:
    """Refuse any accepted-but-unimplemented clause as a CAPABILITY LIMIT, before anything resolves.

    `UnsupportedByThisProfile`, never `WantOfLaw` (ruled Huayin, 2026-09-14). The public request
    form may be perfectly lawful and executable in another profile; what is missing is a governed
    interpretation HERE. A `want_of_law` would tell the caller their question was unlawful when the
    truth is that this build does not implement it, and it would send them to fix a publication
    that is not wrong. There is likewise NO Core fallback: handing the statement to another runtime
    would misreport whose semantics produced the number.

    This runs FIRST — before `resolve`, before law, before any material access — so a rejected
    clause costs zero fetches and cannot be discarded by a partial resolution that ran ahead of it.
    """
    import dataclasses

    fields = {f.name for f in dataclasses.fields(statement)}
    classified = CONSUMED_CLAUSES | CONSUMED_UPSTREAM | set(UNSUPPORTED_CLAUSES)

    unknown = fields - classified
    if unknown:
        # THE COMPLETENESS RULE, ENFORCED RATHER THAN DOCUMENTED. Not a developer error and not an
        # assertion: a request surface this profile has not classified is one it cannot honestly
        # execute against, because the unclassified part might change the answer.
        raise UnsupportedByThisProfile(
            f"the request carries {sorted(unknown)}, which this profile has not classified as "
            f"either consumed or unsupported; it will not execute against a request surface it "
            f"has not decided about")

    present = [name for name in UNSUPPORTED_CLAUSES
               if getattr(statement, name, None) not in (None, False, [], (), "")]
    if present:
        spellings = ", ".join(UNSUPPORTED_CLAUSES[n][0] for n in present)
        why = "; ".join(f"{UNSUPPORTED_CLAUSES[n][0]}: {UNSUPPORTED_CLAUSES[n][1]}" for n in present)
        raise UnsupportedByThisProfile(
            f"this profile does not implement {spellings} — {why}. The statement is valid Frame-QL "
            f"and may execute on another profile; it is not executed here, and it is not silently "
            f"served without the clause")
