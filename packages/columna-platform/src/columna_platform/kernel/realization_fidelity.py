"""
columna_platform.kernel.realization_fidelity — **does this physical result faithfully realize the governed
analytical object it claims to establish?**

    *"A physical result may be evidence for a governed analytical object. It does not become that object by
    being produced, labelled, or offered. Fidelity between physical result and analytical identity must be
    independently established before cache admission."*  — Huayin, 2026-09-30 (B-1′)

        physical provider result
                ↓
        claim: this realizes F@A                      ← `RealizationOffer`, which already WAS the claim
                ↓
        faithful-realization adjudication             ← here
                ↓
        adjudicated physical offer                    ← `AdjudicatedRealization`, mint-guarded
                ↓
        ordinary MME admission                        ← `RealizationManager.establish` → `mme.put`
                ↓
        FamilyMaterialization

WHY THE NAME
------------
Ruled: *"derive the exact naming from the existing code and vocabulary."* The vocabulary already contains
`Realization`, `RealizationStanding`, `RealizationManager`, `RealizationOffer`, `RealizationProposal`,
`RealizationProvider` — and, decisively, `ProviderProfile`'s own docstring: *"A profile, not an authority."*
So **authority** is this codebase's established word for the judging role, and B-0b already used it for the
other constitutional question. `RealizationManager` brokers what providers propose and execute;
`RealizationAuthority` judges whether what came back is what it claims to be. Manager versus authority, in
the sense the code already uses both words.

The phrase "RealizationContract" is deliberately NOT frozen into a class. A contract is what a provider and
the governed world agree in advance; what this module adjudicates is one settlement against that agreement,
and the two should not share a name before the first real provider tells us what an agreement needs.

THREE CLAIMS, AND THEY ARE NOT ONE (ruled §1)
---------------------------------------------
    `AuthorizedFamilyContinuation`   this analytical continuation may lawfully be attempted
    `AuthorizedStanding`             a value of this family may stand at this analytical point
    `AdjudicatedRealization`         THIS PARTICULAR PHYSICAL RESULT faithfully realizes that object

    operation authorization  ≠  target standing  ≠  realization fidelity

The middle one is a precondition of the third and the third is not a precondition of the first: a faithful
realization at `F@A` licenses admission of that value and **nothing about what may be continued from it**,
which B-0b owns. §I below is the test that keeps those apart.

WHAT THIS MODULE DOES NOT DO — AND WHY THAT IS THE POINT (ruled §6)
------------------------------------------------------------------
It does not re-ask questions another layer already owns. §6: *"Do not force every mismatch into one generic
realization refusal if some are already properly owned by standing or MME admission."* So:

    a target outside the continuation region   → the STANDING refuses, verbatim, and its refusal is
                                                 returned unchanged. Fidelity never overrides it and never
                                                 restates it.
    off-build / stale-declaration material     → `MME.put` owns build and witness coherence. This authority
                                                 REQUIRES the offer to state both — a claim that will not
                                                 say which governed environment it was made against is not
                                                 a claim — and then passes them down. Comparing them here
                                                 as well would be a second asker of one question, which is
                                                 exactly the defect B-0a and B-0b removed.
    a standing that claims more support than
    the carrier can back                       → the substrate's own `establish` owns it
                                                 (`support-without-a-value`).

What is left is the fidelity question itself, and it is small: **does the physical result actually BE the
object the offer says it is?**
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from .geometry import KernelRefusal
from .sorts import PARTICIPATION_CARDINALITY
from .standing import Disclosure, Refusal

# ══ the minting guard ═════════════════════════════════════════════════════════════════════════════
#
# **SAME SPIRIT AS B-0b'S, AND FOR THE SAME REASON** (ruled §3). A provider may return values, its own
# identity, carrier information, evidence, and the analytical identity it CLAIMS to realize. It must not be
# able to mint the credential that says its own output faithfully realizes `F@A` — that judgment belongs
# above the provider and before admission. So the credential carries a module-private mark and refuses to
# exist without it, and the only holder of the mark is the authority that reads the constitution.
#
# No cryptography, and none is wanted: the boundary is that a self-certifying provider is not expressible.
class _Mint:
    """The issuing capability. One instance, module-private, unexported."""

    __slots__ = ()

    def __repr__(self) -> str:                                   # pragma: no cover - diagnostics only
        return "<realization-authority mint>"


_MINT = _Mint()


# ══ the credential ════════════════════════════════════════════════════════════════════════════════
@dataclass(frozen=True)
class AdjudicatedRealization:
    """**A physical offer whose fidelity to its claimed analytical object has been independently
    established.** The only thing `RealizationManager.establish` accepts.

    It is not a materialization and it is not permission to skip anything: it is the one precondition of
    ORDINARY admission that a provider-originated value has and a locally derived one does not need, because
    a locally derived value was produced by the governed engine's own composition and has nothing to claim."""

    #: The offer as adjudicated. Carried whole rather than unpacked, so a later reader can see exactly what
    #: was judged — a credential that summarised its subject could drift from it.
    offer: Any
    #: The `AuthorizedStanding` this was checked against. Fidelity presupposes standing: there is no sense in
    #: which a value faithfully realizes `F@A` if no value of `F` may stand at `A`. Carried so `establish`
    #: hands `put` the same standing that was adjudicated, rather than minting a second one.
    standing: Any
    #: Which physical realization produced or carries this value. **The offer's, not the engine's** — B-1′
    #: is where this axis starts carrying the truth (see `RealizationManager.establish`).
    realization: Any
    #: What the authority actually observed, in words, for the record. Evidence, never authority.
    evidence: tuple[str, ...] = ()
    #: Conditions the admitted value must carry because of how it was realized — e.g. that it arrives with
    #: want of state. Propagated, never derived by the cache.
    conditions: tuple[Disclosure, ...] = ()
    issued_by: Any = None

    def __post_init__(self) -> None:
        if self.issued_by is not _MINT:
            raise KernelRefusal(
                "unadjudicated-realization", str(getattr(self.offer, "provider", "?")),
                "an AdjudicatedRealization was constructed outside the realization authority. The claim "
                "that a physical result faithfully realizes a governed analytical object is not the "
                "provider's to make about its own output: a provider that could mint this credential would "
                "be a provider that could settle analytical identity by assertion. Obtain one from "
                "`RealizationAuthority.adjudicate`, or discover there that the claim does not hold.")

    @property
    def subject(self) -> str:
        return f"{self.offer.family_id}@{self.offer.anchor}"

    def __str__(self) -> str:
        return f"adjudicated({self.subject} realized by {self.offer.provider})"


@dataclass(frozen=True)
class Adjudication:
    """**The outcome of asking.** Granted with a credential, or refused with the governed reason.

    Total, and falsy when refused, so `if not adjudicated:` is the whole check. A refusal OWNED BY ANOTHER
    LAYER is passed through unchanged — its code is that layer's, not this one's."""

    credential: Optional[AdjudicatedRealization] = None
    refusal: Optional[Refusal] = None

    def __bool__(self) -> bool:
        return self.credential is not None

    @property
    def adjudicated(self) -> bool:
        return self.credential is not None


# ══ the authority ═════════════════════════════════════════════════════════════════════════════════
class RealizationAuthority:
    """**Judges whether a physical result faithfully realizes the governed object it claims.** The only
    minter of `AdjudicatedRealization`.

    Constructed over a *constitution* — anything exposing `subject`, `law_of`, `instance_of`, `manifold` and
    `authorizer` — which today is the `MME` class for the same reason `ContinuationAuthority` is. It obtains
    the target standing THROUGH that authorizer rather than re-deriving it, so the constitutional reading
    still happens in exactly one module and this one adds no second opinion about what is lawful.

    THE FIVE FIDELITY QUESTIONS, AND WHY EACH IS ABOUT THE RESULT AND NOT ABOUT THE LAW
    ----------------------------------------------------------------------------------
    Each asks whether the physical thing IS the claimed thing. None asks whether the claimed thing is
    permitted — that was settled before this ran, and its refusal is passed through when it was not:

      0. **standing** — may a value of this family stand at this anchor? Delegated, and its refusal returned
         verbatim. Not a fidelity question; a precondition of one.
      1. **the payload is of the claimed family** — a value whose own point names another identity is not
         evidence for this one, however it was labelled.
      2. **the payload is at the claimed anchor** — the same, for location. A total offered as a daily
         breakdown is not a daily breakdown.
      3. **the payload is in the form the law's composition retains** — a finalized estimate is not a sketch.
         This is the check that stops *"the provider computed the right number"* from being mistaken for
         *"the provider supplied the governed family value"*, which is the whole HLL lesson.
      4. **the analytical instance agrees with the declaration** — but for the data state, which is the one
         axis a realization MAY declare (it says which established material it carries).
      5. **the offer's own realization standing agrees with the offerer** — a claim that is not
         self-consistent about who made it cannot be evidence about anything.

    And two things it REQUIRES the offer to state without judging them, because `MME.put` owns them: the
    build and the per-object constitution witness the claim was made against."""

    def __init__(self, constitution: Any) -> None:
        self.constitution = constitution

    @property
    def name(self) -> str:
        return f"realization-authority({self.constitution.manifold})"

    def adjudicate(self, offer: Any) -> Adjudication:
        """**Adjudicate one physical offer's fidelity to its claimed analytical object.**"""
        subject = f"{offer.family_id}@{offer.anchor}"
        family = self.constitution.subject(offer.family_id)
        law = self.constitution.law_of(offer.family_id)
        evidence: list[str] = []
        conditions: list[Disclosure] = []

        # ── 0 · STANDING. Delegated, and its refusal is NOT restated as a fidelity failure. ───────
        standing = self.constitution.authorizer.authorize_standing(family, offer.anchor)
        if not standing:
            return Adjudication(refusal=standing.refusal)
        evidence.append(f"standing: a value of {offer.family_id!r} may stand at {offer.anchor}")

        # ── the claim must say which governed environment it was made against (§5) ────────────────
        if not getattr(offer, "build", ""):
            return Adjudication(refusal=Refusal(
                "realization-states-no-build", subject,
                "the offer names no Manifold build. A claim that will not say which governed environment it "
                "was made against cannot be bound to one, and a value admitted without that binding could "
                "have been realized against a declaration that no longer holds. **THIS AUTHORITY DOES NOT "
                "COMPARE IT** — `MME.put` owns build and witness coherence and comparing it here would be a "
                "second asker of one question — but it requires the claim to be complete enough to check."))
        if not getattr(offer, "witness", ""):
            return Adjudication(refusal=Refusal(
                "realization-states-no-witness", subject,
                "the offer names no constitution witness for the object it claims to realize. The "
                "per-object declaration is what makes `F@A` mean something; a claim silent about which "
                "declaration it realized is a claim about nothing in particular."))
        evidence.append(f"claim bound to build {offer.build} and witness {offer.witness}")

        # ── 1 · THE PAYLOAD IS OF THE CLAIMED FAMILY ──────────────────────────────────────────────
        carried_identity = getattr(offer.value.point, "family_id", None) or offer.value.point.identity
        if carried_identity != offer.family_id:
            return Adjudication(refusal=Refusal(
                "realization-is-not-of-the-claimed-family", subject,
                f"the offer claims to realize {offer.family_id!r} and the payload's own point names "
                f"{carried_identity!r}. A physical result does not become a governed object by being "
                f"labelled with its identity — the label and the payload disagree, and this authority will "
                f"not decide which of the two the provider meant."))

        # ── 2 · THE PAYLOAD IS AT THE CLAIMED ANCHOR ──────────────────────────────────────────────
        if offer.value.anchor != offer.anchor:
            return Adjudication(refusal=Refusal(
                "realization-is-not-at-the-claimed-anchor", subject,
                f"the offer claims {offer.anchor} and the payload stands at {offer.value.anchor}. These are "
                f"different analytical locations and a value at one is not evidence for the other: "
                f"accepting it would admit a grand total as a daily breakdown, or the reverse."))

        # ── 3 · THE PAYLOAD IS IN THE FORM THE COMPOSITION RETAINS ────────────────────────────────
        if offer.value.value_form != law.value_form:
            return Adjudication(refusal=Refusal(
                "realization-value-form-mismatch", subject,
                f"the offer supplies a {offer.value.value_form!r} value where {law.name} retains a "
                f"{law.value_form!r} one. {law.sufficient_state}. **THE PROVIDER MAY WELL HAVE COMPUTED THE "
                f"RIGHT NUMBER**; a finalized estimate is not a sketch, and what the family retains is the "
                f"thing later continuation composes over. Supplying the display value instead is the one "
                f"substitution that cannot be detected after admission."))
        evidence.append(f"value form {offer.value.value_form!r} is what {law.name} retains")

        # ── 4 · THE ANALYTICAL INSTANCE AGREES WITH THE DECLARATION ───────────────────────────────
        declared = self.constitution.instance_of(offer.family_id)
        carried = offer.value.instance
        if not carried.same_but_for_data_state(declared):
            return Adjudication(refusal=Refusal(
                "realization-instance-mismatch", subject,
                f"the offer carries analytical instance {carried} and this build declares {declared}. A "
                f"realization does not get to declare a family's analytical instance. **WHAT IT MAY DECLARE "
                f"IS THE DATA STATE** — which established material it carries — and every other governed "
                f"axis must agree with the registered declaration."))
        evidence.append(f"instance agrees with the declaration but for data state ({carried.data_state})")

        # ── 5 · THE CLAIM IS SELF-CONSISTENT ABOUT WHO MADE IT ────────────────────────────────────
        if offer.realization.provider != offer.provider:
            return Adjudication(refusal=Refusal(
                "realization-standing-disagrees-with-the-offerer", subject,
                f"the offer is made by {offer.provider!r} and carries realization standing naming "
                f"{offer.realization.provider!r}. Which provider's material this is decides whether it is "
                f"interchangeable with another's, so a claim inconsistent about its own origin is not "
                f"evidence about anything."))
        evidence.append(f"realized by {offer.realization.token}")

        # ── 6 · THE ROOT PAYLOAD IS WHAT ITS DECLARED FORMATION SAYS IT IS (B-4a) ─────────────────
        #
        # **THE HOLE THIS CLOSES WAS MEASURED, NOT IMAGINED.** In a cold world a population family whose
        # payload disagreed with its own membership was admitted and served — 7 participating points, 11
        # orders reported — and the only thing that would have caught it is `duplicate-current-disagreement`,
        # which needs an honest copy already retained. Ruled: *"must fail fidelity BEFORE admission, even
        # when no honest materialization is already cached. Do not rely on `duplicate-current-disagreement`;
        # that is too late and only works in a warm world."*
        #
        # This is the first check here that compares the payload against a governed EXPECTATION rather than
        # against the claim's own self-description, and it is a fidelity question in the strict sense: is
        # this result really the claimed `F@A`? A count that disagrees with the domain it is a count of is
        # not that object, however well-formed it is.
        if offer.anchor == family.root:
            verdict = self._formation_holds(family, offer, subject)
            if verdict is not None:
                return Adjudication(refusal=verdict)
            evidence.append(f"root payload agrees with declared formation {family.formation!r}")

        # ── WANT OF STATE IS EVIDENCE, NOT A FIDELITY FAILURE ─────────────────────────────────────
        # A provider may faithfully realize a family value that participates somewhere its required value is
        # not established. That is a true fact about the world and holding it is correct; what may not happen
        # is a reduction or a basis role using it as though the missing values were not required, and both of
        # those are refused where they occur. So it is recorded as a condition and travels with the value.
        if getattr(offer.value, "wants_state", False):
            points = getattr(offer.value, "points_wanting_state", lambda: ())()
            conditions.append(Disclosure(
                "realized-with-want-of-state",
                f"{offer.provider!r} realized {subject} with {len(points)} participating point(s) whose "
                f"required value is not established. The realization is FAITHFUL — this is what the world "
                f"says — and the value is held with that standing recorded. It is not `NA`, not zero and not "
                f"nonparticipation, and any reduction over the affected domain is refused until the value "
                f"is established."))
            evidence.append(f"carries want of state at {len(points)} point(s)")

        return Adjudication(credential=AdjudicatedRealization(
            offer=offer, standing=standing.request, realization=offer.realization,
            evidence=tuple(evidence), conditions=tuple(conditions), issued_by=_MINT))

    @staticmethod
    def _formation_holds(family: Any, offer: Any, subject: str) -> Optional[Refusal]:
        """**Does the offered root payload agree with the family's declared root formation?**
        `None` means it does, or that this formation states nothing checkable here.

        ONE FORMATION IS CHECKABLE TODAY AND THE OTHER IS DELIBERATELY NOT.

        `DIRECT` says the value is independently established as a value of this family and is NOT derived
        from participation — so there is nothing to recompute and no expectation to compare against. A
        `DIRECT` root that arrives with the wrong number is wrong, and no authority here can know it;
        that is what it means for a value to be established rather than derived. Silence is the correct
        answer, not a gap.

        `PARTICIPATION_CARDINALITY` says the value IS the cardinality of the governed participating domain
        constituted at the point. That is recomputable from the offer itself, and so it is recomputed.

        **WHERE THE EXPECTED CARDINALITY COMES FROM, AND WHY IT IS NOT THE LITERAL `1`.** The ruling is
        explicit that `1` is not part of the law. So the expectation is derived from the model's own
        representation of the domain: the participating domain at a coordinate is the set of index
        positions carrying that coordinate, and `CoordinateIndex` REFUSES duplicate coordinates — one
        analytical point may not hold two positions. Hence `|D(r)| = 1` at a root, as a consequence of the
        geometry rather than as a constant written down here, and the arithmetic below would yield 7 or 20
        unchanged the day a geometry represents multiplicity. That is the same distinction the declaration
        makes: cardinality is the law, and the value is what the law meets.

        **SUBSTRATE-NEUTRAL, BECAUSE THIS FILE IS IN THE KERNEL.** It reads `coordinates` + `cell()` — the
        surface B-2 established on both family-state types — and touches no Arrow, no mask and no
        `ColumnStanding`. A check that had reached for `standing.participation` would have made the kernel's
        fidelity boundary columnar-only."""
        if family.formation != PARTICIPATION_CARDINALITY:
            return None
        counts: dict[tuple, int] = {}
        for coordinate in offer.value.coordinates:
            counts[coordinate] = counts.get(coordinate, 0) + 1
        for coordinate, expected in counts.items():
            try:
                supplied = offer.value.cell(coordinate)
            except KernelRefusal:
                # The payload declines to yield a value where the formation says one is constituted. A
                # population reduction has no want of state, so this is not that; it is a payload that
                # cannot answer for a point it claims to cover.
                return Refusal(
                    "realization-withholds-a-constituted-value", subject,
                    f"{offer.provider!r} offers {subject} whose formation is "
                    f"{PARTICIPATION_CARDINALITY!r} and whose payload will not yield a value at "
                    f"{coordinate!r}. The cardinality of a participating domain is constituted wherever "
                    f"the domain is; a point covered by this claim and unanswerable within it is not a "
                    f"faithful realization of it.")
            if supplied != expected:
                return Refusal(
                    "realization-contradicts-its-formation", subject,
                    f"{offer.provider!r} offers {subject} with {supplied!r} at {coordinate!r} where its "
                    f"declared root formation {PARTICIPATION_CARDINALITY!r} constitutes {expected!r}. "
                    f"**THE PAYLOAD DISAGREES WITH THE DOMAIN IT IS A COUNT OF.** This family's root "
                    f"value is not evidence a provider may report; it IS the cardinality of the governed "
                    f"participating domain constituted at the point, so a different number is not a "
                    f"different measurement — it is a claim to be an object it is not. Admitting it would "
                    f"serve a count of {supplied!r} over a domain of {expected!r}, and no later check "
                    f"recovers the difference: continuation would add it, an expression basis would "
                    f"divide by it, and both answers would be confidently wrong.")
        return None


__all__ = ["AdjudicatedRealization", "Adjudication", "RealizationAuthority"]
