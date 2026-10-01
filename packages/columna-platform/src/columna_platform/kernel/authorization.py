"""
columna_platform.kernel.authorization — **who decides that a family continuation MAY be done.**

    *"MME does not determine whether a family continuation is analytically authorized. MME determines
    whether held family materialization can fulfill an already-authorized continuation request correctly
    and consistently."*  — Huayin, 2026-09-29 (B-0b, the decisive ruling)

        Manifold / analytical authorization
                ↓
        Authorized family-continuation request
                ↓
        MME
                ↓
        materialization suitability + execution

THE DESIGN TEST THIS MODULE EXISTS TO PASS
------------------------------------------
    *"Changing a family's continuation region may change which authorized requests are issued. It must not
    require changing MME logic."*

Before B-0b, `law.region.admits(cumulative_forgotten(...))` was asked in four places and every one of them
was inside a cache engine. B-0a collapsed the four onto one name so the duplication was visible; B-0b moves
that one question here. **`region` is now read in exactly one module — this one.** A region edit changes
which requests get minted and nothing else, which is the ruling made mechanical rather than stated.

WHY NOT A `ContinuationEntitlement`
-----------------------------------
The reconciliation first proposed handing MME a carried entitlement object. That was refused, correctly:

    *"An entitlement object that contains constitutional permission and is then interpreted by MME would
    leave analytical authorization inside the cache decision path, merely behind a wrapper."*

The argument that settles it is the design test itself. Under an entitlement, changing a region changes the
entitlement's CONTENT and MME still evaluates it — the constitution still reaches the cache's decision path,
wearing a wrapper. Under an authorized request, changing a region changes WHICH REQUESTS EXIST. So permission
is not data MME consumes; **it is a precondition the request's existence has already discharged.** There is
no field on `AuthorizedFamilyContinuation` from which MME could re-derive permission, because there is no
such field to add.

AUTHORIZATION IS NOT THE SAME ACT AS FULFILLMENT, AND NEITHER IS REALIZATION REQUIREMENT
----------------------------------------------------------------------------------------
Three different things, kept apart deliberately (ruled §7):

    `AuthorizedFamilyContinuation`   this operation is analytically lawful — attempt it from held state
    an `Answer` from `MME.fulfill`   whether held state could actually do it
    a `FamilyRequirement`            held state could not, so: what governed state WOULD satisfy it

The third follows from attempting the first and is a different object with a different question. It is not
collapsed into this one.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from .geometry import Anchor
from .law import FOLD_SHAPES, VALUE_FORMS
from .materialization import cumulative_forgotten, entitlement_holds
from .requirement import FamilyRequirement, RequirementOutcome, acceptable_anchors
from .standing import Disclosure, Refusal

# ══ the minting guard ═════════════════════════════════════════════════════════════════════════════
#
# **STRUCTURAL OWNERSHIP, NOT SECURITY THEATRE** (ruled §6). The requirement is:
#
#     *"ordinary MME callers cannot manufacture analytical authority merely by assembling
#     `family + target + addition`."*
#
# So the authorized request carries a mark that only this module can supply, and refuses to exist without
# it. That is a jurisdiction boundary in the type system: a caller who assembles the fields by hand gets a
# `KernelRefusal` naming the component that should have minted it, not a usable request. No cryptography is
# involved and none is wanted — the point is that the ONE place able to mint is the one place that reads the
# constitution, so "authorized" and "constitutionally checked" are the same event by construction.
class _Mint:
    """The issuing capability. **One instance PER AUTHORITY**, module-private, unexported.

    **J-0 CHANGED THIS FROM A MODULE SINGLETON TO A PER-AUTHORITY OBJECT**, and the change is the whole
    difference between *some* authority issued this and *this* authority issued it. A process may hold
    two Manifold builds; before J-0 both minted with the same mark, so a credential granted by one
    satisfied the other's guard and a foreign build's permission was indistinguishable from a local one.
    The class stays module-private so a credential remains unconstructible outside this module; which
    authority minted it is asked at the consuming boundary, by `issued`."""

    __slots__ = ("authority",)

    def __init__(self, authority: str) -> None:
        self.authority = authority

    def __repr__(self) -> str:                                   # pragma: no cover - diagnostics only
        return f"<continuation-authority mint: {self.authority}>"


# ══ execution requirements — HOW, never WHETHER ═══════════════════════════════════════════════════
@dataclass(frozen=True)
class FoldRequirement:
    """**What an authorized continuation needs in order to EXECUTE.** Resolved above, consumed below.

    Every field here is an execution fact. None of them is permission, and none of them can be turned back
    into permission: knowing that a fold is `addition` over `value-bearing` state says nothing about whether
    the edge it crosses is admitted.

    **THE TWO CAPABILITY KEYS ARE DELIBERATELY NOT ONE KEY** (ruled §4). E-1 established that analytical law
    and physical execution capability are not keyed uniformly, and this record preserves that rather than
    flattening it:

        governed operation semantics   the LAW — and it stays above this line
                ↓
        provider execution mode        `grouped` for any family continuation; `scan` reserved
                ↓
        physical capability            keyed differently per provider contract

    `composition` is the GROUPED key: a composition token. `SUM`, `COUNT` and `STOCK_LEVEL` are three laws
    that all reduce by `addition`, and a columnar provider needs ONE capability for them, not three — so
    keying the fold by law name there would have invented two capabilities that do not exist.
    `merge_realization` is the in-memory `ProviderProfile` key, which IS the law name, because a
    `Realization` is declared per law. Same operation, two contracts, two keys; collapsing them for
    tidiness would have re-created the defect E-1 removed."""

    #: E-1's execution mode. A family continuation is a REDUCER, so today this is always `grouped`; the
    #: field exists because `scan` is the reserved extension point and a future SCAN-shaped continuation
    #: would be a different physical contract with the same authorization.
    execution_mode: str
    #: The GROUPED capability key — a COMPOSITION TOKEN (`addition`, `sketch_union`), never a law name.
    composition: str
    #: The in-memory `ProviderProfile` key for `capability(…, "merge")`. That profile is keyed by law
    #: because a `Realization` is declared per law; this is that contract's key, not a second spelling of
    #: the composition.
    merge_realization: str
    #: The value form the fold's INPUT must already be in, or the held payload cannot execute it.
    required_input_value_form: str
    #: `value-bearing` or `population` — what the reduction contributes over. Read off the LAW, which
    #: declares it (B-0b); never inferred from a law-name enumeration inside an engine.
    fold_shape: str
    #: The law's OWN WORDS for what its composition needs, carried so that a cache refusing an inadequate
    #: payload can explain itself without reading the law. The last law read inside `adjudicate` was this
    #: string; carrying it is what makes that method a function of the candidate and the requirements only.
    sufficient_state: str = ""

    def __post_init__(self) -> None:
        from .geometry import KernelRefusal

        if self.execution_mode not in EXECUTION_MODES:
            raise KernelRefusal("unknown-execution-mode", self.execution_mode,
                                f"{self.execution_mode!r} is not one of {list(EXECUTION_MODES)}")
        if self.fold_shape not in FOLD_SHAPES:
            raise KernelRefusal("unknown-fold-shape", self.fold_shape,
                                f"{self.fold_shape!r} is not one of {sorted(FOLD_SHAPES)}")
        if self.required_input_value_form not in VALUE_FORMS:
            raise KernelRefusal("unknown-value-form", self.required_input_value_form,
                                f"{self.required_input_value_form!r} is not one of {sorted(VALUE_FORMS)}")

    def __str__(self) -> str:
        return (f"{self.execution_mode}:{self.composition}"
                f"[{self.required_input_value_form}, {self.fold_shape}]")


#: The execution modes a fold may name. Mirrors `columnar.capability.EXECUTION_MODES`, which cannot be
#: imported here because the columnar layer depends on the kernel and not the reverse. A test asserts the
#: two vocabularies agree so they cannot drift into two meanings of one word.
GROUPED_MODE = "grouped"
SCAN_MODE = "scan"
EXECUTION_MODES = (GROUPED_MODE, SCAN_MODE)


# ══ the authorized objects ════════════════════════════════════════════════════════════════════════
@dataclass(frozen=True)
class AuthorizedFamilyContinuation:
    """**A continuation that the constitution has already permitted. Its existence IS the permission.**

    Nothing here is the continuation region, the family law, or a right MME must re-adjudicate. Every field
    is something the cache needs in order to *find suitable state, test reachability, check the payload can
    execute the fold, run it, keep standing straight, and record the dependency* — and the list was derived
    from what the cache code actually reads, not from what would look formal."""

    #: WHICH analytical identity, and WHERE. The two facts the cache keys and folds onto.
    family_id: str
    target: Anchor
    #: The analytical instance held state must match. Compared with `same_but_for_data_state`, never
    #: interpreted — the same pattern `Slot` already uses for `participation` and `scope`.
    instance: Any
    #: The evidence state required, where the request named one. `None` means indifferent — NOT that any
    #: mixture will do.
    data_state: Optional[str]
    #: HOW an admitted fold executes. See `FoldRequirement`.
    fold: FoldRequirement
    #: **The paired right to HOLD a value at `target`.** If a continuation to `A` is authorized then a
    #: value may stand at `A` — same constitutional fact, minted at the same moment — so a fold that
    #: produces one need not send the cache back to the authority to retain it. This is not permission MME
    #: re-adjudicates; it is the second authorization for the second act.
    standing: "AuthorizedStanding"
    #: The build this authorization was issued under. Carried so the cache can COMPARE — a new Manifold
    #: build is a new semantic world and material does not cross into one by being present.
    build: str
    #: The per-object constitution digest, for the same comparison at object granularity.
    witness: str
    #: Conditions the ANSWER must carry, decided above. Today this is where an `approximate` standing
    #: rides, because `law.approximation` is a constitutional fact and a cache may not author a
    #: disclosure from one. MME PROPAGATES these; it never derives them.
    conditions: tuple[Disclosure, ...] = ()
    #: Whether a derived materialization should be retained. A cache-policy input, and the caller's to
    #: state — not something MME infers.
    retain: bool = True
    #: §8's route/use evidence: which consumer above the MME caused this demand.
    on_behalf_of: str = ""
    #: The minting mark. See `_Mint`.
    issued_by: Any = None

    def __post_init__(self) -> None:
        from .geometry import KernelRefusal

        if not isinstance(self.issued_by, _Mint):
            raise KernelRefusal(
                "unauthorized-continuation", f"{self.family_id}@{self.target}",
                "an AuthorizedFamilyContinuation was constructed outside the continuation authority. Its "
                "existence is the analytical permission for this fold, so it may only be minted by the "
                "component that reads the constitution — `ContinuationAuthority.authorize`. Assembling "
                "family + target + a composition is not authorization: it is the shape of authorization "
                "without the act. Obtain one from the authority, or discover there that the request is "
                "not lawful.")

    @property
    def subject(self) -> str:
        return f"{self.family_id}@{self.target}"

    def __str__(self) -> str:
        return f"authorized({self.subject} via {self.fold})"


@dataclass(frozen=True)
class AuthorizedStanding:
    """**That `F@A` is a lawful location for material to STAND.** The admission-side twin.

    A continuation is the right to *fold toward* a location. This is the narrower right to *hold a value
    at* one, and it is what independently established material needs — a provider's offer is not a fold.
    The two are separate because they are asked at different moments by different callers, but they read
    the same constitutional fact, in the same module, once.

    **THIS IS THE GOVERNED REALIZATION BOUNDARY IN EMBRYO.** B-2 will thicken it with a realization
    contract asserting that a physical result faithfully realizes this `F@A`; what exists here is the half
    that answers *"may a value of this family stand at this anchor at all?"* — and that half must exist now,
    because removing `admit`'s region check without it would leave the question asked nowhere."""

    family_id: str
    anchor: Anchor
    build: str
    witness: str
    at_root: bool
    issued_by: Any = None

    def __post_init__(self) -> None:
        from .geometry import KernelRefusal

        if not isinstance(self.issued_by, _Mint):
            raise KernelRefusal(
                "unauthorized-standing", f"{self.family_id}@{self.anchor}",
                "an AuthorizedStanding was constructed outside the continuation authority. Whether a "
                "family may hold a lawful value at an anchor is a constitutional question, and a cache "
                "that accepted a self-asserted answer would be a cache that could be told anything.")

    @property
    def subject(self) -> str:
        return f"{self.family_id}@{self.anchor}"


@dataclass(frozen=True)
class Authorization:
    """**The outcome of asking.** Granted with a request, or refused with the governed reason.

    Total, and falsy when refused, so `if not auth:` is the whole check. The refusal is the one that used to
    come out of `MME.admit`/`adjudicate`, moved with its jurisdiction rather than reworded."""

    request: Optional[Any] = None
    refusal: Optional[Refusal] = None

    def __bool__(self) -> bool:
        return self.request is not None

    @property
    def granted(self) -> bool:
        return self.request is not None


# ══ the authority ═════════════════════════════════════════════════════════════════════════════════
class ContinuationAuthority:
    """**The component that interprets the constitution and mints authorizations. THE ONLY ONE.**

    It is constructed over a *constitution* — anything exposing `subject`, `law_of`, `instance_of`,
    `manifold`, `build`, `witness_of` and `provider`. Today that is the `MME` class, because the class is
    still both the Manifold build authority and the cache; the B-0 reconciliation recorded that as the
    residual, and it is why this object is constructed over the engine rather than beside it. **What
    matters for the ruling is that the constitutional READING happens here and nowhere else**, so MME's own
    fulfillment path contains no `region`, no `admits`, and no law-name enumeration. When the class is
    eventually split, this object moves with the authority half and MME keeps `fulfill`/`put`.

    WHAT IT REFUSES, AND WHY THOSE REFUSALS ARE HERE
    -----------------------------------------------
      * **`outside-continuation-region`** — the target is not a lawful location for this family. This
        refusal used to come from `MME.adjudicate` (as `outside-continuation-region`) and from `MME.admit`
        (as `anchor-outside-the-continuation-region`) — **two codes for one question, because two
        components were asking it.** One component asks it now, so there is one code, and the retired
        spelling is gone. If it never fires, no request exists, and MME is never asked something unlawful.
      * **`target-outside-the-family-root`** — geometry prior to law: a family lives at or below `R_F`.
      * **`unrealized-law`** — *not* an authorization refusal in substance, and it stays out of here. Whether
        THIS BUILD can execute a composition is a capability question about the engine, and the engine keeps
        it (see `MME.adjudicate` step 5). A provider's inability never removes a law, and it equally never
        removes the authorization: the request is lawful and unservable, which is a different sentence.
    """

    def __init__(self, constitution: Any) -> None:
        #: The Manifold build authority. Duck-typed on purpose: the kernel engine and the columnar engine
        #: both satisfy it, and neither is named here.
        self.constitution = constitution
        #: **THIS AUTHORITY'S OWN MINT** (J-0). Not shared with any other authority in the process, so a
        #: credential can say which build permitted it and not merely that something did.
        self._mint = _Mint(self.name)

    @property
    def name(self) -> str:
        return f"continuation-authority({self.constitution.manifold})"

    def issued(self, credential: Any) -> bool:
        """**Did THIS authority mint this credential?** Asked at every boundary that acts on one.

        Object identity against a mint no other authority holds. A credential from another build is a
        real credential — it is simply not permission *here*, and the difference is exactly what J-0
        exists to make visible."""
        return getattr(credential, "issued_by", None) is self._mint

    # ── the constitutional reading, in one place ─────────────────────────────────────────────────
    def _fold_for(self, law: Any) -> FoldRequirement:
        """Resolve the law's semantics into execution requirements. **The only place a law becomes a fold.**"""
        return FoldRequirement(
            execution_mode=GROUPED_MODE,
            composition=law.continuation.token if law.continuation is not None else "",
            merge_realization=law.name,
            required_input_value_form=law.value_form,
            fold_shape=law.fold_shape,
            sufficient_state=law.sufficient_state)

    def _conditions_for(self, law: Any) -> tuple[Disclosure, ...]:
        """Conditions the answer must carry, derived from the constitution HERE so the cache need not.

        `approximation` is a constitutional property of the law, so the *"every value served from it carries
        that standing"* disclosure is an analytical statement. Both engines used to author it inside
        `measure` by reading `law.approximation`; that is a cache authoring analytical meaning, and B-0b
        moves it. MME now propagates what the request carries."""
        if law.approximation == "exact":
            return ()
        return (Disclosure(
            "approximate", f"{law.name} is {law.approximation}; every value served from it "
                           f"carries that standing"),)

    # ── minting a continuation ───────────────────────────────────────────────────────────────────
    def authorize(self, family: Any, target: Anchor, *, data_state: Optional[str] = None,
                  retain: bool = True, on_behalf_of: str = "") -> Authorization:
        """**May `F@target` be continued at all?** If yes, hand back the request that says so."""
        from .geometry import KernelRefusal

        family = self.constitution.subject(family)
        law = self.constitution.law_of(family.family_id)

        # 1 · GEOMETRY BEFORE LAW. A family lives at or below `R_F`; a target naming a constituent the root
        #     does not carry is not a coarsening of it, and `cumulative_forgotten` refuses rather than
        #     returning a set. Caught here so the authority's answer is total.
        try:
            cumulative_forgotten(family, target)
        except KernelRefusal as refused:
            return Authorization(refusal=Refusal(
                refused.code, f"{family.family_id}@{target}", refused.detail))

        # 2 · THE CONSTITUTIONAL QUESTION, AND THE ONLY PLACE IT IS ASKED.
        if not entitlement_holds(family, law, target):
            forgotten = cumulative_forgotten(family, target)
            return Authorization(refusal=Refusal(
                "outside-continuation-region", f"{family.family_id}@{target}",
                f"{family.family_id} may hold no lawful value at {target}: reaching it from "
                f"{family.root} forgets {sorted(forgotten)}, which {law.region.why_not(forgotten)}. "
                f"**NO CONTINUATION IS AUTHORIZED**, so no request reaches the materialization cache: a "
                f"governed realization can supply a value, and a cache can hold one, and neither makes "
                f"the family's law admit one where it does not. The question is the WHOLE ROUTE FROM "
                f"{family.root} and is computed by set subtraction, so **an intermediate materialization "
                f"cannot launder an edge the law does not admit** — and under B-0b that is no longer a "
                f"guard the cache applies but a request that never exists. What is held, what was "
                f"evicted, and what a provider could compute are all irrelevant to this answer."))

        return Authorization(request=AuthorizedFamilyContinuation(
            family_id=family.family_id, target=target,
            instance=self.constitution.instance_of(family.family_id), data_state=data_state,
            fold=self._fold_for(law),
            standing=self.authorize_standing(family, target).request,
            build=self.constitution.build.reference,
            witness=self.constitution.witness_of(family.family_id).digest,
            conditions=self._conditions_for(law), retain=retain, on_behalf_of=on_behalf_of,
            issued_by=self._mint))

    # ── minting a standing ───────────────────────────────────────────────────────────────────────
    def authorize_standing(self, family: Any, anchor: Anchor) -> Authorization:
        """**May a value of this family STAND at this anchor?** The admission-side question."""
        from .geometry import KernelRefusal

        family = self.constitution.subject(family)
        law = self.constitution.law_of(family.family_id)
        try:
            cumulative_forgotten(family, anchor)
        except KernelRefusal as refused:
            return Authorization(refusal=Refusal(
                refused.code, f"{family.family_id}@{anchor}", refused.detail))

        if not entitlement_holds(family, law, anchor):
            forgotten = cumulative_forgotten(family, anchor)
            return Authorization(refusal=Refusal(
                "outside-continuation-region", f"{family.family_id}@{anchor}",
                f"{family.family_id} may hold no lawful value at {anchor}: reaching it from "
                f"{family.root} forgets {sorted(forgotten)}, which {law.region.why_not(forgotten)}. "
                f"**THIS IS ASKED OF INDEPENDENTLY ESTABLISHED MATERIAL TOO**: a governed realization can "
                f"supply a value, and cannot make the family's law admit one where it does not."))

        return Authorization(request=AuthorizedStanding(
            family_id=family.family_id, anchor=anchor, build=self.constitution.build.reference,
            witness=self.constitution.witness_of(family.family_id).digest,
            at_root=anchor == family.root, issued_by=self._mint))

    # ── the realization requirement — A DIFFERENT QUESTION, kept distinct (§7) ────────────────────
    def requirement_for(self, family: Any, target: Anchor, *, data_state: Optional[str] = None,
                        note: str = "") -> RequirementOutcome:
        """**What governed family state would satisfy a request for `F@target`?**

        Moved here from `MME` by B-0b, unchanged in substance. It belongs to the authority for the same
        reason the authorization does — every one of its three refusals is constitutional or build-capability
        reasoning — and moving it is what leaves the cache with no reader of `region` at all.

        **IT IS NOT THE AUTHORIZED REQUEST AND IS NOT COLLAPSED INTO ONE** (ruled §7). An authorization says
        *"this is lawful, try it from held state"*; a requirement says *"held state was not enough, here is
        what governed state would be"*. The second follows from attempting the first, and an object that was
        both would make "lawful" and "needed" one word."""
        family = self.constitution.subject(family)
        law = self.constitution.law_of(family.family_id)
        if not target.constituents <= family.root.constituents:
            return RequirementOutcome(
                None,
                f"{target} is not a coarsening of {family.family_id}'s root {family.root}: it names "
                f"{sorted(target.constituents - family.root.constituents)}, which this family's "
                f"materializations never carry. A family lives at or below `R_F`, so there is no state "
                f"at this location for the estate to supply — this is not a gap in the estate.")
        if not entitlement_holds(family, law, target):
            forgotten = cumulative_forgotten(family, target)
            return RequirementOutcome(
                None,
                f"{family.family_id}@{target} is not a lawful location for this family: reaching it from "
                f"{family.root} forgets {sorted(forgotten)}, which {law.region.why_not(forgotten)}. **NO "
                f"REALIZATION REQUIREMENT IS EMITTED.** There is no governed family state here for a "
                f"provider to supply, and a provider that could compute the number would not thereby make "
                f"it a lawful Columna materialization (R-1 §6).")
        if not self.constitution.provider.realizes(law.name):
            return RequirementOutcome(
                None,
                f"law {law.name!r} has no realization in provider profile "
                f"{self.constitution.provider.name!r}. The law "
                f"is unchanged and the target is lawful; this build cannot execute the composition, so "
                f"obtaining the material would not make the request servable. That is a capability "
                f"question about THIS build, not a requirement for the estate.")
        acceptable, truncated = acceptable_anchors(family, law, target)
        return RequirementOutcome(FamilyRequirement(
            manifold=self.constitution.manifold, build=self.constitution.build.reference,
            family_id=family.family_id, target=target, root=family.root,
            acceptable=acceptable, acceptable_truncated=truncated,
            instance=self.constitution.instance_of(family.family_id), data_state=data_state,
            law=law.name, value_form=law.value_form, sufficient_state=law.sufficient_state,
            # **READ OFF THE LAW, WHICH DECLARES IT** (B-3). Not derived here, not enumerated here, and
            # sitting beside the four other governed facts already carried from the same object — which is
            # the whole argument for it being one line: this method already had the law in hand, and the
            # only reason a provider was guessing was that nobody passed the fact along.
            fold_shape=law.fold_shape,
            approximation=law.approximation,
            witness=self.constitution.witness_of(family.family_id).digest, note=note))


__all__ = ["EXECUTION_MODES", "GROUPED_MODE", "SCAN_MODE", "Authorization",
           "AuthorizedFamilyContinuation", "AuthorizedStanding", "ContinuationAuthority",
           "FoldRequirement"]
