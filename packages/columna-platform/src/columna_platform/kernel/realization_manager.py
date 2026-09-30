"""
columna_platform.kernel.realization_manager — **what the physical estate can supply. R-1, interface only.**

    **Realization Manager answers: what governed family materialization can the physical estate supply
    for this analytical requirement?**  — Huayin, 2026-09-29 (R-1 §1)

    It does not decide analytical lawfulness. It does not grant continuation rights. It does not bypass
    MME.

This module is the estate's half of the seam whose other half is `requirement.py`. It is an INTERFACE
unit: there is no backend here, no ADBC, no SQL, no connection, no credential and no I/O of any kind. What
it establishes is the SHAPE of the second actor, so that M-2's `NEED` becomes something a party can be
responsible for.

THE ONE DOOR, AND WHY THERE IS NO SECOND
-----------------------------------------
Ruled §1: *"Any realized family materialization must enter through the ordinary MME admission path and
receive exactly the same adjudication as any other independently established `F@A`."*

So `RealizationManager.establish` is four lines long and every one of them is a call to `MME.admit`. The
manager **holds no reference to a `MaterializationStore`**, has no privileged constructor for a
`FamilyMaterialization`, and cannot mint a `MaterializationId`. That is not a convention kept by care; it
is the absence of the machinery, and a test asserts the absence.

The blast wall (§6) falls out of it rather than being rebuilt here:

    **A backend being able to compute something does not make it a lawful Columna materialization.**

A provider may propose anything it likes — including an anchor outside the family's continuation region —
and `MME.admit` will refuse it by `outside-continuation-region`, in the same words, by the same
rule, as it refuses a locally-derived value at the same place. **The manager does not pre-filter**, and
that is deliberate: filtering would be the manager adjudicating analytical lawfulness, which §1 says it
does not do. It REPORTS the discrepancy (`ProposalSet.outside_requirement`) and adjudicates nothing.

CAPABILITY AND EXECUTION ARE TWO VERBS (§4)
--------------------------------------------
    `propose`   **what could you supply?**   Nothing is fetched. No connection is opened. This is the verb
                the Fulfillment Coordinator will eventually use to compare lawful alternatives —
                `Revenue@Month` directly, `Revenue@Day` then continue, `Revenue@Order` then continue,
                across however many providers — *without paying for any of them.*
    `realize`   **supply it.**               One named proposal, executed.

Designing the interface as `realize(request)` alone would have made capability discovery impossible
without execution, and every future route comparison would have had to fetch all the routes in order to
choose between them. Which is why the split is here in R-1, years before anything needs it.

**AND THERE IS NO THIRD VERB.** Ruled §7: no route-choice policy yet. `ProposalSet` has no `best()`, no
`cheapest()`, no `preferred()`, no score and no sort key — the alternatives are handed over whole and in
the order they were offered, and choosing among them belongs to the Fulfillment Coordinator and eventually
to a cost model that has not been ruled. A test guards the absence of every one of those names, for the
same reason M-2 guards the absence of a cache optimizer: the temptation in the unit that builds the
comparison surface is to add the one obvious comparison.

THE PHYSICAL DIRECTION THIS STAYS COMPATIBLE WITH (§5)
-------------------------------------------------------
    Realization Manager → provider → ADBC where appropriate → backend → **Arrow family materialization**

None of that is implemented. What is preserved is that `RealizationOffer.value` is the substrate's own
family-state object, so a columnar provider hands over Arrow-backed state and it enters `admit` unchanged
— no row materialization, no conversion, no intermediate representation invented at this boundary. **ADBC
is access/transport, not analytical authority**, and nothing in this module knows it exists.

DataFusion remains the columnar execution substrate for continuation and expression work and is a
different question entirely; this module has no opinion about it and never touches it.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Optional, Protocol, runtime_checkable

from .geometry import Anchor, KernelRefusal
from .realization_fidelity import AdjudicatedRealization
from .materialization import INDEPENDENT, Establishment
from .observation import NEED, PROCESS_CONTROL, READY, UNSUPPORTED, WANT_OF_STATE
from .realization import RealizationStanding
from .requirement import FamilyRequirement


# ── what a provider says it COULD do ─────────────────────────────────────────────────────────────
@dataclass(frozen=True)
class RealizationProposal:
    """**One way the estate says it could supply the required family state.** Nothing has been fetched.

    A proposal is a CLAIM about capability and carries no analytical authority whatsoever: it does not
    establish, does not reserve, does not entitle, and is not consulted by any admission path. Two
    providers may propose the same `F@A` and both may be wrong."""

    provider: str
    family_id: str
    anchor: Anchor
    #: What the supplied state would carry — `scalar` / `structured`. Declared at proposal time because it
    #: is the thing most likely to be wrong: a provider that would hand back a finalized HLL estimate where
    #: the family law merges sketches should be discoverable BEFORE it is executed.
    value_form: str = ""
    realization: RealizationStanding = field(
        default_factory=lambda: RealizationStanding(provider="unnamed"))
    #: **Always INDEPENDENT.** A provider SUPPLIES a value at an anchor; it does not continue one from
    #: retained material, because it holds none and knows of none. Ruled M-1 §8: establishment is the
    #: material's actual standing and is never manufactured.
    establishment_kind: str = INDEPENDENT
    #: The provider's own handle for executing THIS proposal — a query id, a file reference, a closure,
    #: whatever it likes. **The manager never interprets it**, which is how physical route planning stays
    #: below this boundary (§2).
    handle: Any = None
    #: Free text for a human reading a comparison. Not a cost, not a rank, not machine-consumed.
    diagnostics: str = ""

    def __post_init__(self) -> None:
        if self.establishment_kind != INDEPENDENT:
            raise KernelRefusal(
                "realization-is-not-continuation", self.provider,
                f"a proposal claims establishment {self.establishment_kind!r}. A realization provider "
                f"SUPPLIES a value at an anchor; it cannot have CONTINUED one, because continuation is a "
                f"relation between retained materializations and a provider holds none and names none. "
                f"Only {INDEPENDENT!r} is available here.")

    def __str__(self) -> str:
        return f"{self.provider}: {self.family_id}@{self.anchor} [{self.value_form or 'unstated'}]"


@dataclass(frozen=True)
class ProposalSet:
    """**Every way the estate says it could meet one requirement — IN NO ORDER OF PREFERENCE.**

    Ruled §G: multiple possible realization anchors and providers must be representable *without choosing
    among them*. So this type is shaped entirely around showing alternatives and entirely against reducing
    them: the groupings below are VIEWS, the order is the order providers were consulted, and there is no
    method that returns one proposal.

    `declined` and `consulted` are here because a comparison that cannot see who was asked and came back
    empty is a comparison over an unknown population — a future coordinator reasoning about whether to fall
    back to a root fetch needs to know the difference between *"no provider offers `Revenue@Month`"* and
    *"the one provider that would have was unreachable."*"""

    requirement: FamilyRequirement
    proposals: tuple[RealizationProposal, ...] = ()
    #: Every provider asked, in order, including the ones that offered nothing.
    consulted: tuple[str, ...] = ()
    #: `(provider, why)` for each provider that offered nothing or could not be asked. **Diagnostic,
    #: never silent**: a provider that cannot is a fact about the estate, not an absence of one.
    declined: tuple[tuple[str, str], ...] = ()

    def __len__(self) -> int:
        return len(self.proposals)

    def __iter__(self):
        return iter(self.proposals)

    @property
    def anchors(self) -> tuple[Anchor, ...]:
        """The distinct anchors the estate offered, coarsest first. **An ordering for a reader, not a
        ranking**: fewer constituents is less material, which is a fact about size and not about cost —
        network, latency, pushdown and locality are all invisible from here and all belong to §5's
        end-to-end quantity."""
        return tuple(sorted({p.anchor for p in self.proposals},
                            key=lambda a: (len(a.constituents), a.order)))

    def by_anchor(self) -> dict[str, tuple[RealizationProposal, ...]]:
        """**§G's first axis**: `Revenue@Month` directly versus `Revenue@Day` then continue."""
        out: dict[str, list[RealizationProposal]] = {}
        for p in self.proposals:
            out.setdefault(str(p.anchor), []).append(p)
        return {k: tuple(v) for k, v in sorted(out.items())}

    def by_provider(self) -> dict[str, tuple[RealizationProposal, ...]]:
        """**§G's second axis**: two providers offering the same thing differently."""
        out: dict[str, list[RealizationProposal]] = {}
        for p in self.proposals:
            out.setdefault(p.provider, []).append(p)
        return {k: tuple(v) for k, v in sorted(out.items())}

    @property
    def outside_requirement(self) -> tuple[RealizationProposal, ...]:
        """Proposals at an anchor the requirement did not list. **REPORTED, NOT REMOVED** (§1, §6).

        Filtering here would be the manager deciding analytical lawfulness; refusing here would make the
        requirement's capped `acceptable` list into an authority. So these travel with the rest, and
        `MME.admit` decides — by the same rule, in the same words, as for any other material."""
        return tuple(p for p in self.proposals if not self.requirement.names_anchor(p.anchor))

    def summary(self) -> str:
        return (f"{len(self.proposals)} proposal(s) for {self.requirement.family_id}@"
                f"{self.requirement.target} at {len(self.anchors)} anchor(s) from "
                f"{len(self.by_provider())} provider(s); {len(self.consulted)} consulted, "
                f"{len(self.declined)} declined")


# ── what a provider actually supplied ────────────────────────────────────────────────────────────
@dataclass(frozen=True)
class RealizationOffer:
    """**Governed family state the estate has actually supplied**, on its way to `MME.admit`.

    It is an OFFER and not a materialization: it has no `MaterializationId`, no residency, no eligibility
    and no place in any store. Those are minted by admission, if admission happens."""

    provider: str
    family_id: str
    anchor: Anchor
    #: The substrate's own family-state object — `FamilyState`, or an Arrow-backed `ColumnarFamilyState`.
    #: **No conversion happens at this boundary** (§5): Arrow stays Arrow all the way into `admit`.
    value: Any
    instance: Any = None
    realization: RealizationStanding = field(
        default_factory=lambda: RealizationStanding(provider="unnamed"))
    #: **WHICH GOVERNED ENVIRONMENT THIS CLAIM WAS MADE AGAINST** (B-1′). A provider states these; it does
    #: not judge them. `RealizationAuthority` requires both to be present — a claim that will not say which
    #: build and which per-object declaration it realized cannot be bound to one — and `MME.put` owns the
    #: comparison, because build and witness coherence is cache coherence and one asker is enough.
    build: str = ""
    witness: str = ""
    #: **Always `Establishment(INDEPENDENT)`.** Enforced in `__post_init__` rather than documented.
    establishment: Establishment = field(default_factory=lambda: Establishment(INDEPENDENT))
    #: The proposal this executes, where there was one. Kept so a future coordinator can tell whether what
    #: arrived is what was advertised — a claim and its settlement are two facts.
    from_proposal: Optional[RealizationProposal] = None
    diagnostics: str = ""

    def __post_init__(self) -> None:
        if self.establishment.kind != INDEPENDENT:
            raise KernelRefusal(
                "realization-is-not-continuation", self.provider,
                f"an offer claims establishment {self.establishment.kind!r}. Realized material is "
                f"{INDEPENDENT!r} by construction: the estate supplied a value at an anchor, which is a "
                f"different claim from 'it was derived and we lost the receipt' (ruled M-1 §8).")

    def __str__(self) -> str:
        return f"{self.provider} offers {self.family_id}@{self.anchor}"


# ── the provider ─────────────────────────────────────────────────────────────────────────────────
@runtime_checkable
class RealizationProvider(Protocol):
    """**Two verbs, and the split between them is the whole of §4.**

    A provider is free to be a database, a file, a service or a constant; nothing above it may assume
    which. What it may NOT be is an analytical authority — there is no method here that returns a law, a
    region, an entitlement or a verdict, and that absence is the same one `realization.py` keeps for the
    provider profile."""

    name: str

    def propose(self, requirement: FamilyRequirement) -> Iterable[RealizationProposal]:
        """**Capability discovery. Executes nothing, fetches nothing, opens nothing.**"""
        ...

    def realize(self, proposal: RealizationProposal) -> RealizationOffer:
        """**Execution.** One named proposal, supplied."""
        ...


class RealizationManager:
    """**The second actor.** *"I can obtain the missing governed family materialization."*

    It holds providers and nothing else — no store, no law registry, no universe, no ability to construct
    a materialization. Everything it can do is: ask providers what they could supply, ask one to supply it,
    and hand the result to `MME.admit`."""

    def __init__(self, *providers: RealizationProvider) -> None:
        self._providers: list[RealizationProvider] = []
        for provider in providers:
            self.register(provider)

    def register(self, provider: RealizationProvider) -> RealizationProvider:
        if not (hasattr(provider, "propose") and hasattr(provider, "realize")
                and hasattr(provider, "name")):
            raise KernelRefusal(
                "not-a-realization-provider", type(provider).__name__,
                "a realization provider must offer `name`, `propose` and `realize`. The two verbs are "
                "separate on purpose (R-1 §4): capability discovery must be possible without executing "
                "the realization, or every future route comparison has to fetch every route in order to "
                "choose between them.")
        self._providers.append(provider)
        return provider

    @property
    def providers(self) -> tuple[str, ...]:
        """In REGISTRATION order, which is not a preference order. Nothing here ranks (§7)."""
        return tuple(p.name for p in self._providers)

    # ── capability ───────────────────────────────────────────────────────────────────────────
    def propose(self, requirement: FamilyRequirement) -> ProposalSet:
        """**What could the estate supply for this requirement?** Nothing is executed.

        Every provider is asked and every answer is kept — including the empty ones, as `declined`. A
        provider that raises while being asked is recorded and does not stop discovery: capability
        discovery is advisory, and one unreachable provider must not make the others invisible. A provider
        that raises while *realizing* is a different matter and propagates, because there the caller asked
        for the thing that failed."""
        proposals: list[RealizationProposal] = []
        declined: list[tuple[str, str]] = []
        for provider in self._providers:
            try:
                offered = tuple(provider.propose(requirement) or ())
            except PROCESS_CONTROL:
                raise
            except Exception as exc:                       # noqa: BLE001 - one provider is not the estate
                declined.append((provider.name, f"could not be asked: {exc!r}"))
                continue
            if not offered:
                declined.append((provider.name, "offers nothing for this requirement"))
                continue
            proposals.extend(offered)
        return ProposalSet(requirement=requirement, proposals=tuple(proposals),
                           consulted=self.providers, declined=tuple(declined))

    # ── execution ────────────────────────────────────────────────────────────────────────────
    def realize(self, proposal: RealizationProposal) -> RealizationOffer:
        """**Supply one named proposal.** The provider that made it is the provider that executes it."""
        provider = next((p for p in self._providers if p.name == proposal.provider), None)
        if provider is None:
            raise KernelRefusal(
                "unknown-realization-provider", proposal.provider,
                f"{proposal.provider!r} is not registered with this manager (it holds "
                f"{list(self.providers)}). A proposal is executed by the provider that made it; there is "
                f"no substitution, because two providers offering the same `F@A` are offering two "
                f"differently realized values and the realization standing is an axis of the key.")
        offer = provider.realize(proposal)
        if offer.family_id != proposal.family_id or offer.anchor != proposal.anchor:
            raise KernelRefusal(
                "offer-does-not-match-proposal", proposal.provider,
                f"{proposal.provider!r} proposed {proposal.family_id}@{proposal.anchor} and supplied "
                f"{offer.family_id}@{offer.anchor}. A claim and its settlement must be the same claim: a "
                f"coordinator that compared alternatives on the proposal and received something else "
                f"compared nothing.")
        return offer

    # ── THE ONE DOOR ─────────────────────────────────────────────────────────────────────────
    @staticmethod
    def establish(mme: Any, adjudicated: AdjudicatedRealization, *, residency: str = "resident",
                  intent: Any = None) -> Any:
        """**Offer ADJUDICATED realized material to the MME, through the ordinary admission path** (§1, §D).

        **THE SIGNATURE IS THE B-1′ BOUNDARY.** This took a `RealizationOffer` — a provider's own claim — and
        now takes an `AdjudicatedRealization`, which only `RealizationAuthority` can mint. So there is no path
        from a physical result to the cache that skips the fidelity question, and the guarantee is structural
        rather than remembered: *"a provider result does not become F@A merely because somebody labels it with
        that identity."*

        What is NOT here is as important. There is no `trusted_backend_put`, no privileged shortcut and no
        parameter that suppresses a check (§4). Backend origin overrides nothing: duplicate-current
        disagreement, build and witness coherence, the materialization lifecycle and every ordinary
        consistency check apply to realized material exactly as to locally derived material, and `admit`
        asks the entitlement question of independent material exactly as of a continuation — which is why the
        blast wall (§6) is enforced by code that already existed rather than by a check added here.

        **AND THE REALIZATION AXIS FINALLY CARRIES THE TRUTH.** Before B-1′ every admission stamped the
        ENGINE's `RealizationStanding`, so two providers' material landed under one identical token and
        `RetentionKey`'s realization axis — which exists precisely so that *"a value produced by an
        approximate provider is not interchangeable with one produced by an exact one"* — recorded the wrong
        thing about every realized value. The adjudicated offer's own standing is passed down.

        A `Refusal` is a normal outcome and is returned rather than raised: the estate being able to compute
        something, the claim being faithful, and the family law admitting it are three questions, and this is
        where the third one is asked."""
        if not isinstance(adjudicated, AdjudicatedRealization):
            raise KernelRefusal(
                "unadjudicated-offer-at-the-door", getattr(adjudicated, "provider", type(adjudicated).__name__),
                "this door takes an `AdjudicatedRealization` and was handed a "
                f"{type(adjudicated).__name__}. A provider's own offer is a CLAIM; whether that physical "
                "result faithfully realizes the governed object it names is adjudicated by "
                "`RealizationAuthority.adjudicate` first. Passing the claim straight through would be the "
                "privileged shortcut B-1′ exists to make unavailable.")
        offer = adjudicated.offer
        value = offer.value
        for condition in adjudicated.conditions:
            value = value.with_disclosure(condition)
        return mme.put(value, adjudicated.standing, establishment=offer.establishment,
                       residency=residency, intent=intent,
                       witness=offer.witness, build=offer.build,
                       realization=adjudicated.realization,
                       note=f"realized by {offer.provider}"
                            + (f" — {offer.diagnostics}" if offer.diagnostics else ""))


# ── NEED → requirement ───────────────────────────────────────────────────────────────────────────
#: Which dispositions M-2 emits that R-1 knows how to turn into a requirement. Exactly one, and the
#: narrowness is the point: R-1 is the interface for *"lawful, and we do not hold it."*
REALIZABLE_DISPOSITIONS = (NEED,)


def requirement_from(mme: Any, observation: Any) -> Any:
    """**Map one `RequestObservation` to the requirement it implies, or to the reason it implies none**
    (§F).

    Three of the four dispositions produce no requirement, and they produce it for three different
    reasons — which is exactly why `RequirementOutcome` carries one:

      `READY`         nothing is needed. The request was served.
      `UNSUPPORTED`   **nothing may be asked of the estate.** This is the load-bearing case. The family law
                      admits no value at the target, so there is no governed family state for a provider to
                      supply — and turning it into a realization request would be inviting a backend to
                      compute an answer the law forbids, which is precisely the laundering the blast wall
                      exists to stop. A backend can almost certainly produce the number.
      `WANT_OF_STATE` the material is present and the VALUE is owed at participating points. That is a real
                      thing the estate might supply and it is **a different requirement shape** — it names
                      points, not an anchor — so R-1 does not invent it. Deferred explicitly rather than
                      silently mapped onto the anchor-shaped one.
      `NEED`          a requirement."""
    from .requirement import RequirementOutcome

    disposition = observation.disposition
    if disposition == READY:
        return RequirementOutcome(None, "the request was served; nothing is needed")
    if disposition == UNSUPPORTED:
        return RequirementOutcome(
            None,
            f"{observation.request.family_id}@{observation.request.target} is UNSUPPORTED "
            f"[{observation.refusal_code}]: no lawful route to this target exists, so there is no "
            f"governed family state for the estate to supply. **THIS IS NOT A GAP IN THE ESTATE.** A "
            f"backend could very likely compute the number; it would not be a lawful Columna "
            f"materialization, and asking for it would be asking a provider to launder an answer the "
            f"family law does not admit.")
    if disposition == WANT_OF_STATE:
        return RequirementOutcome(
            None,
            f"{observation.request.family_id}@{observation.request.target} has WANT OF STATE: the "
            f"material is held and the value it requires is not established at some participating "
            f"points. That is a realizable need and it is a DIFFERENT requirement shape — it names "
            f"points rather than an anchor — and R-1 does not invent it. The remedy today is "
            f"establishment of the missing value, not residency and not a coarser fetch.")
    if disposition != NEED:                                          # pragma: no cover - defensive
        return RequirementOutcome(None, f"unknown disposition {disposition!r}")

    # **THE MME STATES ITS OWN REQUIREMENT.** This function maps a disposition; it does not construct a
    # requirement, because what is lawfully needed is an analytical question and the analytical authority
    # answers it (§2). `requirement_for` returns a `RequirementOutcome` of its own.
    assert RequirementOutcome                                        # imported for the readers above
    return mme.requirement_for(mme.family(observation.request.family_id), observation.request.target,
                               data_state=observation.request.data_state,
                               note=f"NEED observed at request #{observation.seq}"
                                    + (f", on behalf of {observation.request.on_behalf_of}"
                                       if observation.request.on_behalf_of else ""))


__all__ = ["REALIZABLE_DISPOSITIONS", "ProposalSet", "RealizationManager", "RealizationOffer",
           "RealizationProposal", "RealizationProvider", "requirement_from"]
