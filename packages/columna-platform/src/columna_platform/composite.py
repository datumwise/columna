"""Composite sufficient state for MEAN — matching (SUM, COUNT) over ONE participation decision.

THE PROPOSITION:

    A governed family may require composite sufficient state whose components must share one
    participation history, and the finalized displayed value is not interchangeable with that state.

THE BASIS IS READ, NOT INVENTED. Since the C7 correction (ruled 2026-09-12) a MEAN family resolves

    C8 continuation_and_agreement  EXPLICIT_NONE   the displayed mean does not compose
    C7 sufficient_state_bases      ESTABLISHED     StateBasis(("SUM","COUNT"),
                                                              requires_common_participation=True)

so this module asks the law view what its basis is and refuses anything it does not recognise. It
does not decide that a mean needs a sum and a count; the foundation has said so since §11.5.2 was
written, and now says it where a resolver can read it.

WHY ONE PASS IS A STRUCTURAL REQUIREMENT AND NOT A CONVENTION. §11.5.2's basis is a *matching* SUM
and COUNT — same participating contributions in both components. Nothing about a sum of 36 and a
count of 4 says they ranged over the same things. Retain them separately and the pair is a claim
nobody made: their quotient is a mean of nothing, and it will usually look plausible, which is what
makes it dangerous. So `constitute` is the ONLY way to mint components, it mints them together in one
pass over one admitted carrier, and it stamps both with the SAME `ParticipationWitness`. An
after-the-fact pair cannot produce a matching witness because it never had one pass to witness.

This is the P1-10 defect one layer up: `count(*)` discarding its operand gave `revenue.sum` and
`revenue.count` different supports, and `revenue.sum / revenue.count` served a mean over mismatched
denominators, silently.

THE PUBLIC NAME AND SHAPE OF THESE OBJECTS ARE NOT FROZEN. Proof-C-local, like Proof B's licence.
"""
from __future__ import annotations
import uuid
from dataclasses import dataclass, replace
from decimal import Decimal


import pyarrow as pa

from columna_core.governed.foundation import LAWS, StateBasis
from columna_core.governed.resolve import (
    C5_PARTICIPATION, C7_SUFFICIENT_STATE, ESTABLISHED,
)

from .refusals import WantOfCompatibility, WantOfLaw, WantOfState


#: THE BOUNDARY ON THE MECHANISM, recorded verbatim (ruled Huayin, 2026-09-12). A constant, like
#: `EMPTY_FIBER_RULING` and `RESPONSIBILITY_STANDING_RULE`, because the thing most likely to be
#: mistaken for a governed fact here is the token — it is concrete, it is checked, and it works.
PASS_ID_BOUNDARY = (
    "pass_id is a Proof-C runtime witness of common constitution, not a frozen "
    "constitutional/public representation of participation standing. The governing requirement is "
    "shared participation provenance; the current token mechanism is one implementation of that "
    "requirement."
)

@dataclass(frozen=True)
class ParticipationWitness:
    """Evidence that a set of components was constituted over ONE participation decision.

    `pass_id` is minted per constitution pass and is the part that cannot be forged by assembling
    components later. IT IS A MECHANISM, NOT THE REQUIREMENT — see `PASS_ID_BOUNDARY`: what is
    governed is shared participation PROVENANCE, and a token is one way to witness it. A successor
    may witness the same fact differently without this proof having said otherwise. Two states constituted separately hold different `pass_id`s even when every
    other field agrees — which is exactly the case the pairing rule must catch, because it is the
    case where the numbers look fine."""

    participation: str
    anchor: str
    carrier_fingerprint: str
    pass_id: str

    def matches(self, other: "ParticipationWitness") -> bool:
        """Same PASS — the test for whether two components may form one basis."""
        return self == other

    def same_participation(self, other: "ParticipationWitness") -> bool:
        """Same participation RULE and anchor — the weaker test for whether two BASES may combine.

        Deliberately weaker than `matches`: continuation adds states from different fibers, so two
        composites being combined necessarily come from different passes. What they may not differ in
        is the participation rule under which their contributions were admitted."""
        return (self.participation, self.anchor) == (other.participation, other.anchor)


@dataclass(frozen=True)
class Component:
    """One component of a composite basis, carrying the law that governs its own continuation."""

    law: str
    value: object
    governed_domain: str
    #: read from the foundation — never inferred from the component's NAME
    continues_under: str
    witness: ParticipationWitness


@dataclass(frozen=True)
class CompositeState:
    """A matching (SUM, COUNT) basis. `finalized` marks a value that is NOT sufficient state."""

    family_id: str
    anchor: str
    components: tuple
    witness: ParticipationWitness
    basis_note: str
    finalized: bool = False

    def component(self, law: str) -> Component:
        for c in self.components:
            if c.law == law:
                return c
        raise WantOfState(f"the basis carries no {law} component", subject=self.family_id)


def _fingerprint(array: pa.Array) -> str:
    """Identity of the admitted carrier this pass read. Not a hash of the VALUES — two different
    carriers may hold equal values and still be different admissions."""
    return f"{array.type}:{len(array)}:{uuid.uuid4().hex[:8]}"


def declared_basis(law_view) -> StateBasis:
    """The family's C7 basis, or refuse. Read from the law view; never assumed."""
    c7 = law_view[C7_SUFFICIENT_STATE]
    if c7.standing != ESTABLISHED:
        raise WantOfLaw(
            f"the family's sufficient-state basis is {c7.standing}; there is no basis to constitute",
            subject=law_view.canonical_reference)
    if not isinstance(c7.value, StateBasis):
        raise WantOfLaw(
            f"the family's sufficient state is scalar ({c7.value!r}); this path constitutes a "
            f"COMPOSITE basis and will not repackage a scalar as one",
            subject=law_view.canonical_reference)
    return c7.value


def constitute(law_view, admitted, *, anchor: str) -> CompositeState:
    """THE ONLY WAY TO MINT COMPONENTS. One admitted carrier, one participation decision, one pass."""
    subject = law_view.canonical_reference
    basis = declared_basis(law_view)

    if basis.components != ("SUM", "COUNT"):
        raise WantOfLaw(f"this proof constitutes ('SUM','COUNT') only; the basis is "
                        f"{basis.components}", subject=subject)

    c5 = law_view[C5_PARTICIPATION]
    if c5.standing != ESTABLISHED:
        raise WantOfLaw(
            f"participation is {c5.standing}. A basis that requires COMMON participation cannot be "
            f"constituted where the participation itself is not established", subject=subject)

    witness = ParticipationWitness(
        participation=c5.value, anchor=anchor,
        carrier_fingerprint=_fingerprint(admitted.array), pass_id=uuid.uuid4().hex)

    # ── THE ONE PASS ────────────────────────────────────────────────────────────────────────────
    # Both components come off the same iteration of the same admitted values. There is deliberately
    # no code path that produces one without the other.
    total, n = Decimal(0), 0
    for v in admitted.array.to_pylist():
        if v is None:
            raise WantOfState(
                "a null reached constitution; admission refuses carriers whose absence semantics are "
                "not governed, so this state should not exist", subject=subject)
        total += v
        n += 1

    return CompositeState(
        family_id=law_view.family_id, anchor=anchor, witness=witness, basis_note=basis.note,
        components=(
            Component("SUM", total, admitted.governed_domain,
                      LAWS["SUM"].entails_continuation, witness),
            Component("COUNT", n, LAWS["COUNT"].result_domain,
                      LAWS["COUNT"].entails_continuation, witness),
        ))


def pair(sum_component: Component, count_component: Component, *, family_id: str,
         anchor: str, basis_note: str = "") -> CompositeState:
    """Assemble a basis from components retained SEPARATELY. Refuses unless they share one pass.

    This function exists ONLY so the refusal is reachable and testable. It is the operation the
    proposition denies, and having it named is better than having it absent — an absent operation
    gets reinvented by whoever needs it next, without the check."""
    a, b = sum_component.witness, count_component.witness
    if not a.matches(b):
        detail = ("components were not constituted in one pass over one admitted carrier"
                  if a.same_participation(b) else
                  "components do not even share a participation rule")
        raise WantOfCompatibility(
            f"a matching (SUM, COUNT) basis requires COMMON PARTICIPATION STANDING and these "
            f"components do not carry it: {detail}. Equal-looking values do not establish that two "
            f"components ranged over the same contributions", subject=family_id)
    return CompositeState(family_id=family_id, anchor=anchor,
                          components=(sum_component, count_component),
                          witness=a, basis_note=basis_note)


def continue_composite(a: CompositeState, b: CompositeState) -> CompositeState:
    """Componentwise continuation, each component under ITS OWN foundation-declared law.

    NOT under "COUNT" for the count component: `LAWS['COUNT'].usable_as_continuation` is False and
    its `composition` is None. What the foundation says is `entails_continuation == 'SUM'` — counts
    compose by addition. Reading the law rather than the component's NAME is the whole point."""
    if a.finalized or b.finalized:
        raise WantOfLaw("a finalized value is not sufficient state and may not be continued",
                        subject=a.family_id)
    if a.family_id != b.family_id or a.anchor != b.anchor:
        raise WantOfLaw("continuation requires one analytical identity", subject=a.family_id)
    if not a.witness.same_participation(b.witness):
        raise WantOfCompatibility(
            f"these bases were constituted under different participation standing "
            f"({a.witness.participation!r} vs {b.witness.participation!r}); numerically combining "
            f"them would produce a mean over contributions nobody admitted together",
            subject=a.family_id)

    merged = ParticipationWitness(
        participation=a.witness.participation, anchor=a.anchor,
        carrier_fingerprint=f"derived({a.witness.carrier_fingerprint},"
                            f"{b.witness.carrier_fingerprint})",
        pass_id=f"derived({a.witness.pass_id},{b.witness.pass_id})")

    out = []
    for law in ("SUM", "COUNT"):
        ca, cb = a.component(law), b.component(law)
        if ca.continues_under != cb.continues_under:            # pragma: no cover - defensive
            raise WantOfLaw(f"the {law} components disagree on their continuation law", subject=a.family_id)
        if ca.continues_under != "SUM":
            raise WantOfLaw(f"this proof continues components under SUM only; the {law} component "
                            f"continues under {ca.continues_under!r}", subject=a.family_id)
        out.append(replace(ca, value=ca.value + cb.value, witness=merged))

    return CompositeState(family_id=a.family_id, anchor=a.anchor, components=tuple(out),
                          witness=merged, basis_note=a.basis_note)


@dataclass(frozen=True)
class Finalized:
    """A displayed value. NOT sufficient state — that is the point, and it is stated in the type."""

    family_id: str
    anchor: str
    value: Decimal
    governed_domain: str
    #: the witness the value was computed from, for disclosure. Never a substitute for the basis.
    witness: ParticipationWitness
    is_sufficient_state: bool = False


def finalize(state: CompositeState) -> Finalized:
    """Compute the mean. Refuses BEFORE arithmetic if the basis is not matched.

    The order is the proof: every check below happens before a division, so a corrupted component
    cannot be caught by its result looking wrong — it is caught by its standing being wrong."""
    subject = state.family_id
    s, c = state.component("SUM"), state.component("COUNT")

    # ── standing, before arithmetic ─────────────────────────────────────────────────────────────
    if not s.witness.matches(state.witness) or not c.witness.matches(state.witness):
        raise WantOfCompatibility(
            "a component's participation witness does not match the basis it is part of; the value "
            "may look plausible and the standing does not hold", subject=subject)
    if not s.witness.matches(c.witness):
        raise WantOfCompatibility("the SUM and COUNT components were not constituted together",
                                  subject=subject)
    if c.value == 0:
        raise WantOfState("the basis carries no contributions; a mean over an empty basis is not a "
                          "value this proof establishes", subject=subject)

    quotient = Decimal(s.value) / Decimal(c.value)
    if quotient * c.value != s.value:
        # OUT OF SCOPE BY RULING (2026-09-12). Whether an analytically exact result with no finite
        # representation must refuse, disclose, or use another representation is UNRULED. Proof C's
        # fixture is chosen so this cannot fire; the branch refuses rather than rounding, so the
        # proof cannot silently answer a question it was told to leave open.
        raise WantOfState(
            "the exact mean has no finite representation in this execution type. The standing and "
            "serving behaviour for that case are UNRULED, and this proof does not decide them",
            subject=subject)

    return Finalized(family_id=state.family_id, anchor=state.anchor, value=quotient,
                     governed_domain=s.governed_domain, witness=state.witness)


def offer_as_state(final: Finalized) -> CompositeState:
    """Offering a finalized scalar back as sufficient state. Always refuses."""
    raise WantOfState(
        f"a finalized value ({final.value}) is a displayed value, not sufficient state: §5.2 — 'a "
        f"displayed scalar generally loses the weight required for exact continuation. Its SUM and "
        f"COUNT basis retains that information.' Re-materializing the basis would resolve this",
        subject=final.family_id)
