"""
columna_platform.kernel.materialization — **MME v1: the governed family-materialization cache.**

    *"MME v1 is a governed family-materialization cache. Ordinary cache mechanics manage residency and
    dependency; analytical law governs reuse."*  — Huayin, 2026-09-29

    *"Residency never creates analytical authority."*

THE ONE DISTINCTION THIS MODULE EXISTS TO MAKE
-----------------------------------------------
    analytical identity  `F@A`        which governed quantity, at which location
    cache-object identity `MaterializationId`   which retained instance of it

They are different, and **two retained instances of one `F@A` must be able to coexist** (ruled
2026-09-29 §1). The engine could not represent that before: its `RetentionKey` was a structural tuple, so a
second materialization of the same `F@A` under the same instance silently OVERWROTE the first — measured, not
inferred. An opaque id minted at admission is the fix, and the analytical facts stay on the record as
**selectable attributes** rather than as the identity.

WHAT IS IN AND WHAT IS OUT
--------------------------
In: family materializations `F@A`, their dependency edges, current/superseded standing, residency, admission,
supersession, candidate selection. Out: expression outputs (v1 serves them above the MME), persistence,
scheduling, CDC, source cursors, refresh orchestration, backend planning. Nothing here knows what a file is.

TWO INDEPENDENT AXES, AND THE RULES THAT MAKE THE SPLIT SAFE
------------------------------------------------------------
    eligibility   CURRENT | SUPERSEDED     governed: may this answer a current ask, may it seed
    residency     PINNED | RESIDENT | EVICTABLE | EVICTED | EXPIRED     policy: is the payload here, may it go

`HISTORICAL` is deliberately absent (ruled: *"do not create a separate HISTORICAL state yet"*). Non-current
material retained on purpose is `SUPERSEDED` + a residency that keeps it. Three rules hold the split:

* **residency never creates authority** — no residency value makes a `SUPERSEDED` entry answerable;
* **`EXPIRED` is not `SUPERSEDED`** — a policy withdrawal of a still-current value is a `NEED`, not a claim
  that the value was wrong;
* **eviction is our absence, not the world's** — a missing payload is a `NEED`, never a `WANT_OF_STATE`.

CONTINUATION ENTITLEMENT IS **DERIVED**, NOT STORED — AND THE REASON IS A THEOREM
--------------------------------------------------------------------------------
Ruled 2026-09-29 §7: do not freeze `forgotten_since_root`; test three possible sources, and produce a
counterexample if route-sensitive entitlement is real. **There is no counterexample, and the reason is
algebraic.** For constituent sets with `T ⊆ M ⊆ R`:

        (R − M) ∪ (M − T)  =  R − T

The cumulative forgotten set is set subtraction, so *every* route from the family root `R_F` to a target `T`
forgets exactly `R_F − T`. A `ContinuationRegion` is a predicate over that cumulative set, therefore:

    **admitted(M → T)  ≡  region.admits(R_F.constituents − T.constituents)**

— a function of the family law, the family's root and the TARGET. The intermediate anchor does not appear;
the route does not appear; provenance does not appear. Verified over every family and every anchor pair in
the built vocabulary: 0 mismatches, 0 route-sensitive targets.

Three consequences, all of them things the ruling asked to be sure of:

1. `forgotten_since_root` is **not** the irreducible source of entitlement. It is retained as PROVENANCE and
   is no longer read as authority. (`entitlement_holds` below is the authority.)
2. **Evicting an ancestor cannot change a descendant's rights**, trivially — the rights never mentioned an
   ancestor. The invariant is protected by construction rather than by remembering to protect it.
3. Independent establishment needs no fabricated route. A materialization at `M` is lawful iff
   `region.admits(R_F − M)`, whoever produced it — so the engine stops manufacturing
   `root.forgets(anchor)` for material that was never derived (ruled §8).

**WHEN THIS WOULD STOP BEING TRUE**, stated so the next person can check rather than trust: if
`ContinuationRegion` ever stops being a predicate over the cumulative forgotten set and becomes a genuine
per-edge graph whose admission is not determined by the union — the widening its own docstring anticipates —
then route-sensitivity becomes possible and the frozen entitlement comes back. A test pins the equivalence so
that widening the region without revisiting this will fail loudly.
"""
from __future__ import annotations

import itertools
from dataclasses import dataclass, replace
from typing import Any, Iterable, Optional

from .geometry import Anchor, KernelRefusal
from .realization import RealizationStanding
from .sorts import FamilyPoint, MeasureFamily
from .standing import AnalyticalInstance

# ══ identities ════════════════════════════════════════════════════════════════════════════════════
_SEQUENCE = itertools.count(1)


@dataclass(frozen=True)
class ManifoldBuild:
    """**The semantic world a cache belongs to** (ruled §6: `constitution_context = ManifoldBuildId`).

    *"A new Manifold build is a new semantic world for the MME. Old cache state is not reused into it by
    default."* So this is the cache's partition, and it is one token rather than a derived digest: the build
    is declared by whoever built the Manifold, not computed from its contents. Per-object
    `ConstitutionWitness` stays useful for admission validation, diagnostics and detecting off-build material
    crossing — it is no longer the runtime partition mechanism."""

    manifold: str
    build: str

    @property
    def reference(self) -> str:
        return f"{self.manifold}@{self.build}"

    def __str__(self) -> str:
        return self.reference


@dataclass(frozen=True)
class MaterializationId:
    """**Opaque cache-object identity.** Not derived from family, anchor, data state or any other analytical
    attribute — those remain selectable properties of the record, and a cache identity computed from them
    could not tell two coexisting instances apart, which is the defect this replaces."""

    token: str

    def __str__(self) -> str:
        return self.token


def _mint() -> MaterializationId:
    return MaterializationId(f"mat-{next(_SEQUENCE):06d}")


# ══ standings ═════════════════════════════════════════════════════════════════════════════════════
#: Eligibility — GOVERNED. Two values only, per the ruling; `SUPERSEDED` means exactly "not eligible for
#: current serving", whether or not a named successor exists.
CURRENT = "current"
SUPERSEDED = "superseded"
ELIGIBILITIES = (CURRENT, SUPERSEDED)

#: Residency — POLICY. `EVICTED` means the payload is gone and the record remains, which is what lets a
#: dependency edge keep meaning something after its parent's bytes are released.
PINNED = "pinned"
RESIDENT = "resident"
EVICTABLE = "evictable"
EVICTED = "evicted"
EXPIRED = "expired"
RESIDENCIES = (PINNED, RESIDENT, EVICTABLE, EVICTED, EXPIRED)
#: Residencies whose payload is present AND usable. `EXPIRED` holds bytes it may not serve from.
USABLE_RESIDENCIES = frozenset({PINNED, RESIDENT, EVICTABLE})

#: How a materialization came to be. Establishment standing is ASSERTED at admission and adjudicated; it is
#: never manufactured (ruled §8).
AT_ROOT = "at-root"              # formed at R_F
CONTINUED = "continued"          # derived from other retained materialization(s)
INDEPENDENT = "independent"      # supplied at a non-root anchor by a governed realization
ESTABLISHMENTS = (AT_ROOT, CONTINUED, INDEPENDENT)


@dataclass(frozen=True)
class Establishment:
    """**Actual establishment standing.** `derived_from` is the dependency relation and nothing else — it is
    what supersession propagates along, and it is recorded separately from analytical identity."""

    kind: str
    derived_from: tuple[MaterializationId, ...] = ()

    def __post_init__(self) -> None:
        if self.kind not in ESTABLISHMENTS:
            raise KernelRefusal("unknown-establishment", self.kind,
                                f"{self.kind!r} is not one of {list(ESTABLISHMENTS)}")
        if self.kind == CONTINUED and not self.derived_from:
            raise KernelRefusal(
                "continuation-without-a-parent", self.kind,
                "a CONTINUED materialization must name what it was continued from. An unattributed "
                "continuation is indistinguishable from an independent establishment, and the two have "
                "different admission questions.")
        if self.kind != CONTINUED and self.derived_from:
            raise KernelRefusal(
                "unattributed-derivation", self.kind,
                f"a {self.kind} materialization names {len(self.derived_from)} parent(s). Root and "
                "independent establishment are not derivations; recording a parent here would fabricate a "
                "route the material did not take.")

    def __str__(self) -> str:
        parents = ", ".join(str(p) for p in self.derived_from)
        return f"{self.kind}({parents})" if parents else self.kind


# ══ the managed unit ══════════════════════════════════════════════════════════════════════════════
@dataclass(frozen=True)
class FamilyMaterialization:
    """**One governed instance of `F@A` held for possible reuse.**

    Ten slots, grouped so that no consumer can read one job's field as another's: cache identity, analytical
    identity, the value, establishment, realization, and the two lifecycle axes.

    **No expression fields.** No `constructor`, no `basis_id`, no basis compatibility — expressions are
    served above the MME in v1. **No scheduler data.** No cursor, watermark, schedule or source reference."""

    # ── cache-object identity ────────────────────────────────────────────────────────────────
    id: MaterializationId
    build: ManifoldBuild
    # ── analytical identity (selectable attributes, NOT the identity of this object) ─────────
    point: FamilyPoint
    instance: AnalyticalInstance
    # ── the value ────────────────────────────────────────────────────────────────────────────
    value: Optional[Any]                       # None once the payload is evicted
    value_fingerprint: str
    # ── how it came to be ────────────────────────────────────────────────────────────────────
    establishment: Establishment
    realization: RealizationStanding
    # ── lifecycle, two independent axes ──────────────────────────────────────────────────────
    eligibility: str = CURRENT
    residency: str = RESIDENT
    superseded_by: Optional[MaterializationId] = None
    superseded_reason: str = ""
    admitted_seq: int = 0
    note: str = ""

    @property
    def family_id(self) -> str:
        return self.point.family_id

    @property
    def anchor(self) -> Anchor:
        return self.point.anchor

    @property
    def data_state(self) -> str:
        """A selectable attribute, never this object's identity. (The typed `{scheme, token}` reference
        ruled during P-2 rides with the parked persistence mechanics; M-1 needs only to select on it.)"""
        return self.instance.data_state

    @property
    def slot(self) -> "Slot":
        return Slot(build=self.build, family_id=self.family_id, anchor=self.anchor,
                    participation=self.instance.participation, scope=self.instance.scope)

    @property
    def has_payload(self) -> bool:
        return self.value is not None and self.residency != EVICTED

    @property
    def serviceable(self) -> bool:
        """**May this answer a current ask or seed a continuation?** Both axes must agree, and the governed
        one is checked first so that a policy value can only ever subtract."""
        return (self.eligibility == CURRENT
                and self.residency in USABLE_RESIDENCIES
                and self.has_payload)

    def __str__(self) -> str:
        return (f"{self.id} {self.family_id}@{self.anchor} [{self.eligibility}/{self.residency}] "
                f"{self.establishment} {self.data_state}")


@dataclass(frozen=True)
class Slot:
    """**The analytical slot a materialization occupies.** What "the current answer" is an answer *for*.

    `data_state` is deliberately NOT part of it (ruled §2: *"if they belong to distinct historical/data
    states, the ordinary current request must not see them as two interchangeable current answers"*). A
    request names an analytical identity, so at most one evidence state may be CURRENT in a slot; others are
    retained and not current. Realization is not part of it either: two providers' material for one slot are
    candidates for the same answer, not two answers."""

    build: ManifoldBuild
    family_id: str
    anchor: Anchor
    participation: str
    scope: Optional[str]

    def __str__(self) -> str:
        return f"{self.family_id}@{self.anchor}:{self.build}"


# ══ admission ═════════════════════════════════════════════════════════════════════════════════════
COEXIST = "coexist"
SUPERSEDE = "supersede"
REJECT = "reject"


@dataclass(frozen=True)
class TransitionIntent:
    """**What the offerer claims this material should do to what is already held.**

    *"Caller may supply transition intent. MME owns dependency consequences after admission."* The caller's
    authority ends at this record; everything after admission — currentness, inheritance, eligibility,
    residency — is the MME's."""

    kind: str = COEXIST
    supersedes: tuple[MaterializationId, ...] = ()

    def __post_init__(self) -> None:
        if self.kind not in (COEXIST, SUPERSEDE, REJECT):
            raise KernelRefusal("unknown-intent", self.kind,
                                f"{self.kind!r} is not one of {[COEXIST, SUPERSEDE, REJECT]}")
        if self.kind == SUPERSEDE and not self.supersedes:
            raise KernelRefusal(
                "supersede-names-nothing", self.kind,
                "SUPERSEDE must name the materialization(s) it supersedes. An unnamed supersession would "
                "make the MME guess which retained instance the offerer meant, which is the guess this "
                "protocol exists to remove.")
        if self.kind != SUPERSEDE and self.supersedes:
            raise KernelRefusal("intent-names-targets", self.kind,
                                f"a {self.kind} intent names supersession targets.")


@dataclass(frozen=True)
class Admission:
    """The verdict, and everything the MME did as a consequence. Truthy when the material was admitted."""

    admitted: bool
    id: Optional[MaterializationId] = None
    eligibility: str = ""
    superseded: tuple[MaterializationId, ...] = ()
    inherited: tuple[MaterializationId, ...] = ()
    code: str = ""
    detail: str = ""

    def __bool__(self) -> bool:
        return self.admitted

    def __str__(self) -> str:
        if not self.admitted:
            return f"REFUSED [{self.code}] {self.detail}"
        return (f"ADMITTED {self.id} as {self.eligibility}"
                + (f", superseding {[str(s) for s in self.superseded]}" if self.superseded else "")
                + (f", inherited {[str(i) for i in self.inherited]}" if self.inherited else ""))


# ══ entitlement — derived, never stored ═══════════════════════════════════════════════════════════
def cumulative_forgotten(family: MeasureFamily, target: Anchor) -> frozenset:
    """**Everything forgotten on ANY route from `R_F` to `target`** — `R_F − target`, and the route cannot
    change it (see the module docstring's theorem)."""
    if not target.constituents <= family.root.constituents:
        raise KernelRefusal(
            "target-outside-the-family-root", family.family_id,
            f"{target} carries constituents the family's root {family.root} does not. A family's "
            f"materializations live at or below `R_F`; this is not a coarsening of it.")
    return frozenset(family.root.constituents - target.constituents)


def entitlement_holds(family: MeasureFamily, law: Any, target: Anchor) -> bool:
    """**May this family hold a lawful value at `target` at all?** The whole of the laundering guard, computed
    root-relatively and therefore identically for every materialization of the family."""
    return bool(law.region.admits(cumulative_forgotten(family, target)))


def admitted_targets(family: MeasureFamily, law: Any, anchors: Iterable[Anchor]) -> tuple[Anchor, ...]:
    """Which of `anchors` this family may lawfully be continued to. Used by the eviction invariant's test:
    the answer must not move when an ancestor's payload is released."""
    return tuple(a for a in anchors
                 if a.constituents <= family.root.constituents and entitlement_holds(family, law, a))


# ══ the store ═════════════════════════════════════════════════════════════════════════════════════
def fingerprint(value: Any) -> str:
    """**A realization-level agreement test**, for duplicate-current consistency ONLY.

    Not analytical identity and not a witness: it answers *"do these two retained instances of one slot say
    the same thing"*, which is a question about material. Two analytically equal values computed in different
    orders may differ in the last float bit and would be reported as a disagreement — a known limit, and the
    conservative direction: a false consistency failure is loud, a false agreement is silent."""
    import hashlib

    parts: list[str] = []
    cells = getattr(value, "cells", None)
    if isinstance(cells, dict):
        parts.append(repr(sorted((tuple(map(str, k)), repr(v)) for k, v in cells.items())))
    array = getattr(value, "values", None)
    if array is not None and hasattr(array, "to_pylist"):
        parts.append(repr(array.to_pylist()))
        standing = getattr(value, "standing", None)
        if standing is not None:
            parts.append(repr(standing.participation.to_pylist()))
            parts.append(repr(standing.support.to_pylist()))
    if not parts:
        parts.append(repr(value))
    return "fp-" + hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()[:16]


class MaterializationStore:
    """**What is held, what depends on what, and what is current.** Ordinary cache mechanics, governed.

    It decides nothing analytical: every question about whether a held value may seed a continuation is put
    to `kernel.MME.adjudicate`, exactly as before. What this owns is identity, coexistence, currentness,
    dependency consequences and residency."""

    def __init__(self, build: ManifoldBuild) -> None:
        self.build = build
        self._by_id: dict[MaterializationId, FamilyMaterialization] = {}

    # ── reading ──────────────────────────────────────────────────────────────────────────────
    def __len__(self) -> int:
        return len(self._by_id)

    def __iter__(self):
        return iter(self._by_id.values())

    def get(self, mid: MaterializationId) -> Optional[FamilyMaterialization]:
        return self._by_id.get(mid)

    def all(self) -> tuple[FamilyMaterialization, ...]:
        return tuple(self._by_id.values())

    def select(self, family_id: Optional[str] = None, *, anchor: Optional[Anchor] = None,
               eligibility: Optional[str] = CURRENT, instance: Optional[AnalyticalInstance] = None,
               data_state: Optional[str] = None,
               serviceable: Optional[bool] = None) -> tuple[FamilyMaterialization, ...]:
        """**Selection over ATTRIBUTES.** The analytical facts are searchable properties, not the identity."""
        out = []
        for m in self._by_id.values():
            if family_id is not None and m.family_id != family_id:
                continue
            if anchor is not None and m.anchor != anchor:
                continue
            if eligibility is not None and m.eligibility != eligibility:
                continue
            if instance is not None and not m.instance.same_but_for_data_state(instance):
                continue
            if data_state is not None and m.data_state != data_state:
                continue
            if serviceable is not None and m.serviceable != serviceable:
                continue
            out.append(m)
        return tuple(out)

    def current_in_slot(self, slot: Slot) -> tuple[FamilyMaterialization, ...]:
        return tuple(m for m in self._by_id.values()
                     if m.slot == slot and m.eligibility == CURRENT)

    def descendants(self, mid: MaterializationId) -> tuple[MaterializationId, ...]:
        """Everything transitively established FROM `mid`. The relation supersession propagates along."""
        found: list[MaterializationId] = []
        frontier = [mid]
        while frontier:
            parent = frontier.pop()
            for m in self._by_id.values():
                if parent in m.establishment.derived_from and m.id not in found:
                    found.append(m.id)
                    frontier.append(m.id)
        return tuple(found)

    # ── admission ────────────────────────────────────────────────────────────────────────────
    def admit(self, *, point: FamilyPoint, instance: AnalyticalInstance, value: Any,
              establishment: Establishment, realization: RealizationStanding,
              intent: Optional[TransitionIntent] = None, residency: str = RESIDENT,
              note: str = "") -> Admission:
        """**The one door.** Warm start, a continuation's result and an external offer all arrive here.

        The analytical checks that precede this (is `F` constituted, does the constitution match the build,
        do the governed axes agree, is the standing well-formed, is the entitlement claim admissible) belong
        to the engine and run before it calls in. What this owns is the cache consequence."""
        intent = intent or TransitionIntent()
        if intent.kind == REJECT:
            return Admission(False, code="rejected-by-offerer",
                             detail="the offerer asked for this material to be rejected.")
        if residency not in RESIDENCIES:
            raise KernelRefusal("unknown-residency", residency,
                                f"{residency!r} is not one of {list(RESIDENCIES)}")
        for parent in establishment.derived_from:
            if parent not in self._by_id:
                raise KernelRefusal(
                    "parent-not-held", str(parent),
                    f"this materialization claims to continue from {parent}, which this store does not "
                    f"hold. A dependency edge must point at a record — an edge to nothing would make "
                    f"supersession unable to find its descendants.")

        slot = Slot(build=self.build, family_id=point.family_id, anchor=point.anchor,
                    participation=instance.participation, scope=instance.scope)
        fp = fingerprint(value)
        superseded: tuple[MaterializationId, ...] = ()
        inherited: tuple[MaterializationId, ...] = ()

        if intent.kind == SUPERSEDE:
            problem = self._validate_supersession(intent.supersedes, point)
            if problem is not None:
                return problem
            eligibility, reason = CURRENT, ""
        else:
            standing = self._coexistence_standing(slot, instance, fp)
            if isinstance(standing, Admission):
                return standing                                     # a consistency failure
            eligibility, reason = standing

        mid = _mint()
        materialization = FamilyMaterialization(
            id=mid, build=self.build, point=point, instance=instance, value=value,
            value_fingerprint=fp, establishment=establishment, realization=realization,
            eligibility=eligibility, residency=residency, superseded_reason=reason,
            admitted_seq=next(_SEQUENCE), note=note)
        self._by_id[mid] = materialization

        if intent.kind == SUPERSEDE:
            superseded, inherited = self.supersede(intent.supersedes, by=mid)
        return Admission(True, id=mid, eligibility=eligibility, superseded=superseded,
                         inherited=inherited, code="admitted",
                         detail=f"admitted as {eligibility}" + (f" ({reason})" if reason else ""))

    def _validate_supersession(self, targets: Iterable[MaterializationId],
                               point: FamilyPoint) -> Optional[Admission]:
        """*"MME must validate the claimed analytical slot/state relationship, then apply cache
        consequences."* A supersession may cross anchors — `Revenue@Day` may supersede `Revenue@Month` with
        no edge between them (ruled §4) — but it may not cross a family or a build, because those are
        relationships the MME cannot check and would be taking on faith."""
        for target in targets:
            held = self._by_id.get(target)
            if held is None:
                return Admission(False, code="supersession-target-not-held",
                                 detail=f"{target} is not held by this store.")
            if held.family_id != point.family_id:
                return Admission(
                    False, code="unrelated-supersession-target",
                    detail=f"{target} is a materialization of {held.family_id!r} and the offered material "
                           f"is {point.family_id!r}. Supersession is a claim about ONE family's analytical "
                           f"slot; across families it would be an evidence-level claim this engine cannot "
                           f"validate and will not take on faith.")
            if held.build != self.build:
                return Admission(False, code="supersession-across-builds",
                                 detail=f"{target} belongs to build {held.build}; this store is "
                                        f"{self.build}. A new build is a new semantic world.")
        return None

    def _coexistence_standing(self, slot: Slot, instance: AnalyticalInstance,
                              fp: str) -> Any:
        """Where a COEXIST offer lands, and the duplicate-current consistency rule (ruled §H)."""
        current = self.current_in_slot(slot)
        if not current:
            return (CURRENT, "")
        same_state = [m for m in current if m.instance == instance]
        if not same_state:
            # A different evidence state, offered to coexist. It is RETAINED and NOT CURRENT: an ordinary
            # request names an analytical identity, and must never be handed two interchangeable current
            # answers drawn from different evidence states. Making it current is what SUPERSEDE is for.
            return (SUPERSEDED, "coexisting under a different data state; not current")
        disagreeing = [m for m in same_state if m.value_fingerprint != fp]
        if disagreeing:
            return Admission(
                False, code="duplicate-current-disagreement",
                detail=f"{len(disagreeing)} retained CURRENT materialization(s) of {slot} claim the same "
                       f"analytical state and hold a DIFFERENT value "
                       f"({[str(m.id) for m in disagreeing]}). This is a consistency failure, not a cache "
                       f"choice: the MME may pick between agreeing candidates, and it will not pick between "
                       f"two answers to one question. Neither is discarded and nothing is admitted.")
        # agreeing duplicates may coexist as current; the selector picks by cost
        return (CURRENT, "agreeing duplicate of a current materialization")

    # ── lifecycle ────────────────────────────────────────────────────────────────────────────
    def supersede(self, targets: Iterable[MaterializationId], *, by: Optional[MaterializationId] = None,
                  reason: str = "") -> tuple[tuple[MaterializationId, ...], tuple[MaterializationId, ...]]:
        """**Mark targets superseded and propagate to their descendants — eagerly.**

        Eagerly, because a lazy walk would have to consult ancestors at read time and an evicted ancestor
        would then make a descendant look independently established. Consequences live in the entries.

        Residency is untouched: *"supersession changes current serving eligibility, not necessarily
        residency."*"""
        marked: list[MaterializationId] = []
        inherited: list[MaterializationId] = []
        for target in targets:
            held = self._by_id.get(target)
            if held is None:
                continue
            if held.eligibility != SUPERSEDED:
                self._by_id[target] = replace(
                    held, eligibility=SUPERSEDED, superseded_by=by,
                    superseded_reason=reason or "replaced by a newly admitted materialization")
                marked.append(target)
            for child in self.descendants(target):
                kid = self._by_id[child]
                if kid.eligibility != SUPERSEDED:
                    self._by_id[child] = replace(
                        kid, eligibility=SUPERSEDED, superseded_by=None,
                        superseded_reason=f"established from {target}, which was superseded")
                    inherited.append(child)
        return tuple(marked), tuple(inherited)

    def evict(self, mid: MaterializationId) -> FamilyMaterialization:
        """**Release the payload, keep the record.** The record keeps the dependency edge meaningful; the
        entitlement of every descendant is unaffected because it never depended on this payload."""
        held = self._require(mid)
        if held.residency == PINNED:
            raise KernelRefusal("pinned", str(mid),
                                f"{mid} is PINNED and may not be evicted. Unpin it deliberately.")
        evicted = replace(held, value=None, residency=EVICTED)
        self._by_id[mid] = evicted
        return evicted

    def drop(self, mid: MaterializationId) -> None:
        """**Forget the record entirely.** Stronger than eviction, and the invariant must survive it too."""
        held = self._require(mid)
        if held.residency == PINNED:
            raise KernelRefusal("pinned", str(mid), f"{mid} is PINNED and may not be dropped.")
        del self._by_id[mid]

    def pin(self, mid: MaterializationId) -> FamilyMaterialization:
        held = self._require(mid)
        self._by_id[mid] = replace(held, residency=PINNED)
        return self._by_id[mid]

    def unpin(self, mid: MaterializationId, *, residency: str = RESIDENT) -> FamilyMaterialization:
        held = self._require(mid)
        self._by_id[mid] = replace(held, residency=residency)
        return self._by_id[mid]

    def expire(self, mid: MaterializationId) -> FamilyMaterialization:
        """**Policy withdraws the value; the bytes may remain.** Not supersession: nothing says this value
        was wrong, so the disposition it produces is `NEED`, not a claim about the world."""
        held = self._require(mid)
        self._by_id[mid] = replace(held, residency=EXPIRED)
        return self._by_id[mid]

    def _require(self, mid: MaterializationId) -> FamilyMaterialization:
        held = self._by_id.get(mid)
        if held is None:
            raise KernelRefusal("not-held", str(mid), f"{mid} is not held by this store.")
        return held

    # ── candidate selection — the MME's choice, never the caller's ───────────────────────────
    def candidates_for(self, family_id: str, target: Anchor, instance: AnalyticalInstance,
                       *, data_state: Optional[str] = None
                       ) -> tuple[FamilyMaterialization, ...]:
        """**Every serviceable materialization that could reach `target`, cheapest first.**

        *"Cache choice stays inside MME."* The request asked for an analytical identity; which retained
        instance answers it is this engine's business, ordered by cost — fewest cells to fold first, which is
        the kernel's own least-work-first rule — and made deterministic by admission order so that two runs
        of one engine agree."""
        usable = [m for m in self._by_id.values()
                  if m.family_id == family_id and m.serviceable
                  and m.instance.same_but_for_data_state(instance)
                  and (data_state is None or m.data_state == data_state)
                  and target.constituents <= m.anchor.constituents]
        return tuple(sorted(usable, key=lambda m: (_cost(m), -m.admitted_seq, m.id.token)))

    # ── reporting ────────────────────────────────────────────────────────────────────────────
    def summary(self) -> str:
        by_eligibility: dict[str, int] = {}
        by_residency: dict[str, int] = {}
        for m in self._by_id.values():
            by_eligibility[m.eligibility] = by_eligibility.get(m.eligibility, 0) + 1
            by_residency[m.residency] = by_residency.get(m.residency, 0) + 1
        return (f"{len(self._by_id)} materialization(s); "
                f"eligibility {dict(sorted(by_eligibility.items()))}; "
                f"residency {dict(sorted(by_residency.items()))}")


def _cost(m: FamilyMaterialization) -> int:
    """How much work folding this one would be. Cells, where the value knows; else its anchor's width."""
    value = m.value
    cells = getattr(value, "cells", None)
    if isinstance(cells, dict):
        return len(cells)
    index = getattr(value, "index", None)
    if index is not None:
        try:
            return len(index)
        except TypeError:                                          # pragma: no cover - defensive
            pass
    return len(m.anchor.constituents)


__all__ = ["AT_ROOT", "Admission", "COEXIST", "CONTINUED", "CURRENT", "ELIGIBILITIES", "EVICTABLE",
           "EVICTED", "EXPIRED", "Establishment", "ESTABLISHMENTS", "FamilyMaterialization",
           "INDEPENDENT", "ManifoldBuild", "MaterializationId", "MaterializationStore", "PINNED",
           "REJECT", "RESIDENCIES", "RESIDENT", "SUPERSEDE", "SUPERSEDED", "Slot", "TransitionIntent",
           "USABLE_RESIDENCIES", "admitted_targets", "cumulative_forgotten", "entitlement_holds",
           "fingerprint"]
