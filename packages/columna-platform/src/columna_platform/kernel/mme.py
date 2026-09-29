"""
columna_platform.kernel.mme — **the in-memory Materialized Measure Engine.**

THE FOUR DISTINCTIONS THIS ENGINE MAKES OPERATIONAL
---------------------------------------------------
Ruled (Huayin, 2026-09-28):

  **Family root authority.**              `F@R_F` is the canonical continuation origin.
  **Non-root family materialization.**    A lawful `F@A` may be cached and may seed later continuation
                                          ONLY WHILE its family value remains adequate for that admitted
                                          continuation.
  **Expression cache.**                   `E@A` may be cached and served but never becomes family
                                          continuation state.
  **Physical availability is not analytical authority.**

The last one is the load-bearing one, and it is why this module is shaped as `retain` / `candidates` /
`adjudicate` / `serve` rather than as a cache with a lookup. **Holding an object and being permitted to
use it are two facts**, and `adjudicate` is the only place the second is decided. Every refusal below is
a refusal about an object that is sitting in the store.

THE ADJUDICATION, IN THE ORDER IT ASKS
--------------------------------------
  1. **Sort.** Is the retained thing family state at all? An `ExpressionOutput` is refused HERE, by a
     governed verdict — the type already makes it impossible (it has no `fold_onto`), and the verdict
     exists so a caller is told WHY rather than shown an `AttributeError`.
  2. **Reachability.** Is the target a coarsening of the candidate's anchor? Geometry, not law.
  3. **Closure, over the WHOLE ROUTE FROM THE ROOT.** The laundering guard. Forgetting `{store}` then
     `{day}` forgets `{store, day}`; if `day` is outside the region the two-step refuses exactly as the
     one-step does. Without this, an intermediate materialization is a way to obtain an answer the law
     forbids — and physical availability would have become analytical authority in the one place it is
     hardest to see.
  4. **Adequacy of the value.** Does the retained value still carry the sufficient state the composition
     needs? A structured witness does; a finalized scalar does not.
  5. **Realization.** Can the active provider execute the composition? A `no` here is a provider limit
     and says so.

WHAT IS DELIBERATELY NOT HERE
-----------------------------
No delta retraction and no deletion maintenance (ruled: *"v8 explicitly does not grant that
capability"*). Invalidation is conservative — a state whose constitution has moved is not patched, it is
**stale**, and re-establishment is from the root. No persistence backend, no serialization, no request
routing, no authoring syntax. And nothing imports `columna_core`.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any, Iterable, Mapping, Optional

from .geometry import Anchor, KernelRefusal, Universe
from .law import AnalyticalLaw, LawRegistry, STRUCTURED
from .realization import ProviderProfile, RealizationStanding
from .sorts import (
    GovernedExpression,
    MeasureFamily,
    SufficientBasis,
)
from .standing import (
    CACHED,
    UNSTATED_DATA_STATE,
    CONTINUED,
    Disclosure,
    EVALUATED,
    REFUSED,
    ROOT,
    Refusal,
)
from .materialization import (
    AT_ROOT,
    CONTINUED as CONTINUED_FROM,
    CURRENT,
    INDEPENDENT,
    SUPERSEDED,
    Establishment,
    FamilyMaterialization,
    ManifoldBuild,
    MaterializationId,
    MaterializationStore,
    TransitionIntent,
    Admission,
    cumulative_forgotten,
)
from .value import Answer, ExpressionOutput, FamilyState
from .witness import ConstitutionWitness


# ── retention ────────────────────────────────────────────────────────────────────────────────────
@dataclass(frozen=True)
class RetentionKey:
    """**What is sufficient to distinguish a retained object — and no more than that.**

    Ruled: *"Do not reproduce existing cache keys merely because they exist… Do not over-design the
    final persistent key yet."* So this is the in-memory key, carrying exactly the axes a retained object
    must be told apart by:

      `sort`            family state and expression output are different objects with different rights,
                        and a key that could not tell them apart would make proof 5 unstatable;
      `identity`        the governed `family_id` / `expression_id`;
      `anchor`          where it is;
      `instance`        the analytical instance — participation and scope where identity-bearing, the
                        shared constitution CONTEXT, and the `data_state` of the material: which actual
                        root/evidence state this object belongs to;
      `constitution`    the per-object **`ConstitutionWitness` digest**, computed from identity-bearing
                        governed facts, so a state from a superseded constitution is a DIFFERENT retained
                        object rather than a silent overwrite;
      `realization`     realization standing: a value produced by an approximate provider is not
                        interchangeable with one produced by an exact one.

    **THREE AXES FOR P-1'S THREE FACTS, AND THE POINT IS THAT THEY ARE THREE** (Huayin, 2026-09-29):
    constitution change, root/evidence freshness and physical realization *"remain separately reasoned even
    if a later retention key combines references to all three."* This key is that combination, and it
    combines REFERENCES: each axis is computed by its own authority (`witness.py`, whoever established the
    material, the provider profile), and each is separately reportable — so "the declaration moved", "the
    data was reloaded" and "the provider changed" never arrive as one undifferentiated "stale".

    Not here: a physical grain, a storage location, a partition, a file. Those are storage facts, and
    ToD v8 keeps storage out of identity."""

    sort: str
    identity: str
    anchor: Anchor
    instance: Any
    realization: RealizationStanding
    #: The computed `ConstitutionWitness` digest of the object this value belongs to.
    constitution: str = ""

    @property
    def provider(self) -> str:
        """Legibility: the provider NAME out of the realization standing."""
        return self.realization.provider

    @property
    def data_state(self) -> str:
        return self.instance.data_state

    def __str__(self) -> str:
        return f"{self.sort}:{self.identity}@{self.anchor}"


@dataclass(frozen=True)
class Retained:
    key: RetentionKey
    value: Any                       # FamilyState | ExpressionOutput

    @property
    def continuation_bearing(self) -> bool:
        return bool(getattr(self.value, "CONTINUATION_BEARING", False))


@dataclass(frozen=True)
class Staleness:
    """**One retained object whose constitution has moved, and WHICH determinant moved.**

    *"Staleness due to constitution change is mechanically detectable"* (P-1). Detectable is the floor; this
    record is the ceiling — it names the determinants, because a steward asked to re-establish from the root
    is owed the governed fact that made it necessary."""

    key: RetentionKey
    held_under: str
    current: ConstitutionWitness
    changed: tuple[str, ...]
    detail: str

    def __str__(self) -> str:
        return f"{self.key} STALE [{', '.join(self.changed)}]"


@dataclass(frozen=True)
class PoolResolution:
    """**Which retained objects are even candidates, before any adjudication.**

    Separated from `adjudicate` deliberately: adjudication answers *"may this seed that"*, and this answers
    the three prior questions that are not about the edge at all — is it the same object, under the CURRENT
    constitution, and from ONE evidence state. A state failing any of those is not a blocked candidate; it
    is not a candidate."""

    pool: tuple[Retained, ...]
    #: Held under a SUPERSEDED constitution witness. Not candidates, and not silently missing either.
    superseded: tuple[Retained, ...]
    #: The distinct `data_state`s among the constitution-current held objects.
    data_states: tuple[str, ...]
    refusal: Optional[Refusal] = None

    @property
    def note(self) -> str:
        """What a refusal on the serving path should append about what WAS held. Empty when nothing was."""
        if not self.superseded:
            return ""
        return (f" {len(self.superseded)} retained state(s) of this object ARE held and are STALE: they "
                f"were established under a superseded constitution witness "
                f"({sorted({r.key.constitution for r in self.superseded})}), and this engine does not "
                f"patch a state whose constitution has moved — re-establishment is from the root. Ask "
                f"`stale_states()` for which governed determinant moved.")


def resolve_pool(held: Iterable[Retained], identity: str, instance: Any, witness_digest: str,
                 subject: str, data_state: Optional[str] = None) -> PoolResolution:
    """**The three prior questions, asked once for both MMEs.**

    The kernel owns this because every one of them is an analytical question, not a columnar one: the
    columnar engine calls exactly this function, as it calls exactly this `adjudicate`."""
    # **CONSTITUTION SUPERSESSION IS CHECKED BEFORE THE INSTANCE AXES, AND THE ORDER IS LOAD-BEARING.**
    # A determinant like `participation` is BOTH a witness determinant and an axis of the analytical
    # instance, so a moved declaration moves both at once. Screening on the instance first would have
    # dropped the superseded state as "a different instance" and the refusal would have reported nothing
    # held — when what is held is precisely a state of this object under a constitution that has moved.
    mine = [r for r in held if r.key.identity == identity]
    superseded = tuple(r for r in mine if r.key.constitution != witness_digest)
    current = [r for r in mine if r.key.constitution == witness_digest
               and r.key.instance.same_but_for_data_state(instance)]
    states = tuple(sorted({r.key.instance.data_state for r in current}))
    if data_state is not None:
        current = [r for r in current if r.key.instance.data_state == data_state]
    elif len(states) > 1:
        # **THE ENGINE DOES NOT PICK AN EVIDENCE STATE.** Two loads of one constitution are both current
        # and neither is the answer; choosing the larger, the newer or the first would be the engine
        # deciding a governed fact, and there is no "newer" here anyway — this kernel holds no clock.
        return PoolResolution(
            pool=(), superseded=superseded, data_states=states,
            refusal=Refusal(
                "ambiguous-data-state", subject,
                f"{len(states)} root/evidence states of this object are held under ONE constitution: "
                f"{list(states)}. They are not stale-versus-current and neither is wrong — they range over "
                f"different established material, so serving either would answer a question nobody asked. "
                f"Name the data state, or establish one. **NOTHING IS MERGED ACROSS THEM**: two evidence "
                f"states are not two contributions to one quantity."))
    return PoolResolution(pool=tuple(current), superseded=superseded, data_states=states)


@dataclass(frozen=True)
class Adequacy:
    """Whether one retained candidate may seed a continuation to one target. Total: a `no` always says
    which of the five questions it failed."""

    holds: bool
    code: str
    detail: str

    def __bool__(self) -> bool:
        return self.holds


class MME:
    """The engine. In-memory, single provider profile, conservative invalidation."""

    def __init__(self, universe: Universe, laws: LawRegistry, provider: ProviderProfile, *,
                 manifold: str = "default", build: Optional[str] = None) -> None:
        # **ONE MME PER MANIFOLD JURISDICTION.** A logical rule, not a deployment one: this engine may
        # share its process, its provider and its store with any number of others. What it may not share
        # is authority, so it refuses to register an object belonging to another Manifold — the accident
        # the ruling is against is one runtime holding two worlds that use the same family name.
        self.manifold = manifold
        #: **The Manifold BUILD is the cache's semantic world** (ruled 2026-09-29 §6:
        #: `constitution_context = ManifoldBuildId`). A new build is a new world and old cache state is not
        #: reused into it by default — which is why the store is per-build and the per-object witness is no
        #: longer the runtime partition mechanism.
        self.build = ManifoldBuild(manifold=manifold, build=build or "build-1")
        #: **Family materializations.** Cache-object identity is opaque and two instances of one `F@A` may
        #: coexist here; the analytical facts are selectable attributes of the records.
        self.materializations = MaterializationStore(self.build)
        self.universe, self.laws, self.provider = universe, laws, provider
        #: **Realization standing, as an object.** The third of P-1's three facts; an axis of the key and
        #: of nothing else.
        self.realization = RealizationStanding(provider=provider.name, carrier="in-memory")
        self._families: dict[str, MeasureFamily] = {}
        self._expressions: dict[str, GovernedExpression] = {}
        self._bound: dict[str, AnalyticalLaw] = {}
        self._store: dict[RetentionKey, Retained] = {}
        #: **Every constitution this engine has seen, by digest.** Its own constitutional history, kept so
        #: that staleness can name WHICH determinant moved rather than only that something did. It grows on
        #: re-registration and nothing is ever removed: a superseded constitution is a fact about the past,
        #: and forgetting it would make the state held under it unexplainable.
        self._constitutions: dict[str, ConstitutionWitness] = {}
        #: Diagnostics only (ruled §6): which materializations stopped being current because a declaration
        #: moved, and which determinant moved. Not a version store and not consulted when serving.
        self._declaration_moves: list[Staleness] = []
        #: Stores holding material under this authority's build — this engine's own, plus any columnar
        #: engine attached to it. A declaration move must reach all of them, because the consequence is a
        #: fact about the constitution and not about which substrate happens to hold the bytes.
        self._attached: list[MaterializationStore] = [self.materializations]

    # ── constitution ─────────────────────────────────────────────────────────────────────────
    def register_family(self, family: MeasureFamily) -> MeasureFamily:
        """**Where ToD v8 §9.2 is enforced, by refusing to construct rather than by gating later.**
        `MeasureFamily.bind` raises for a law with no continuation, so a Mean family is not a reachable
        state of this engine."""
        self._require_own(family.manifold, family.family_id)
        was = self._families.get(family.family_id)
        was_witness = self.witness_of(family.family_id) if was is not None else None
        self._bound[family.family_id] = family.bind(self.laws)
        self._families[family.family_id] = family
        witness = self._remember(family.witness(self._bound[family.family_id]))
        if was_witness is not None and was_witness.digest != witness.digest:
            self._declaration_moved(family.family_id, was_witness, witness)
        return family

    def register_expression(self, expression: GovernedExpression) -> GovernedExpression:
        self._require_own(expression.manifold, expression.expression_id)
        self._bound[expression.expression_id] = expression.bind(self.laws, self._families)
        self._expressions[expression.expression_id] = expression
        self._remember(expression.witness(self._bound[expression.expression_id]))
        return expression

    def _require_own(self, manifold: str, identity: str) -> None:
        if manifold != self.manifold:
            raise KernelRefusal(
                "foreign-manifold", identity,
                f"belongs to Manifold {manifold!r} and this MME is the jurisdiction of "
                f"{self.manifold!r}. A governed analytical object belongs to exactly one Manifold; "
                f"registering it here would put one identity under two authorities.")

    def attach_store(self, store: MaterializationStore) -> MaterializationStore:
        """Register another engine's materialization store under this authority."""
        if store not in self._attached:
            self._attached.append(store)
        return store

    def _declaration_moved(self, identity: str, was: ConstitutionWitness,
                           now: ConstitutionWitness) -> None:
        """**A declaration moved inside one build, so every materialization of it stops being current.**

        Under MME v1 the Manifold BUILD is the semantic world (ruled §6), so the ordinary way to change
        semantics is to build again — and old cache state is not carried into a new world. Changing a
        declaration *in place* is the irregular case, and the honest consequence is the governed one the
        lifecycle already has: the material is not wrong, it is **not current**, and it may stay resident
        for as long as policy likes. Nothing is patched and nothing is silently dropped; re-establishment
        is from the root."""
        comparison = was.compare(now)
        for store in self._attached:
            affected = store.select(identity, eligibility=CURRENT)
            store.supersede(
                [m.id for m in affected],
                reason=f"the declaration of {identity!r} moved within build {self.build}: "
                       f"{', '.join(comparison.changed)}")
            for m in affected:
                self._declaration_moves.append(Staleness(
                    key=self._descriptor(m), held_under=was.digest, current=now,
                    changed=comparison.changed, detail=comparison.detail))

    def _remember(self, witness: ConstitutionWitness) -> ConstitutionWitness:
        self._constitutions[witness.digest] = witness
        return witness

    # ── the three facts, each obtainable on its own ──────────────────────────────────────────
    def witness_of(self, identity: str) -> ConstitutionWitness:
        """**The computed `ConstitutionWitness` of a registered object.** Fact one of three.

        Read from the registered DECLARATION every time rather than cached, so it cannot drift from the
        object it is about: if the declaration in this engine has moved, this moves with it, and that is
        precisely what makes the states held under the old one detectably stale."""
        obj = self._families.get(identity) or self._expressions.get(identity)
        if obj is None:
            raise KernelRefusal(
                "not-constituted", identity,
                f"no family or expression named {identity!r} is registered in Manifold "
                f"{self.manifold!r}, so there is no governed constitution to witness. A witness is "
                f"computed from a declaration; it is not something a retained object can supply about "
                f"itself.")
        # **THE BOUND LAW IS PART OF THE WITNESS** (boundary check 1, 2026-09-29): the admitted continuation
        # region is identity-bearing and lives on the law, so the engine — which is what binds a law name to
        # a law — is the right place for a witness to be obtained.
        return obj.witness(self._bound[identity])

    def constitution_seen(self, digest: str) -> Optional[ConstitutionWitness]:
        """A constitution this engine has registered at some point, by digest — its own history."""
        return self._constitutions.get(digest)

    def stale_states(self) -> tuple[Staleness, ...]:
        """**Which materializations stopped being current because a declaration moved, and what moved.**

        Diagnostics (ruled §6): the per-object witness is no longer the runtime partition — the build is —
        so this reports rather than decides. The governed consequence already happened at re-registration:
        the affected materializations are `SUPERSEDED`, which is why they cannot be served."""
        return tuple(self._declaration_moves)

    def instance_of(self, identity: str) -> Any:
        """The analytical instance of a registered object — **stamped with this engine's Manifold.**

        The single place an instance is obtained, so no caller can construct one that forgets which
        jurisdiction it belongs to."""
        obj = self._families.get(identity) or self._expressions[identity]
        return replace(obj.instance(), constitution_context=self.build.reference)

    def family(self, family_id: str) -> MeasureFamily:
        return self._families[family_id]

    def expression(self, expression_id: str) -> GovernedExpression:
        """**A PEER of `family()`, not a widening of it.** A caller asks `sort_of` first and then the
        accessor for that sort; there is no lookup that returns either, so no consumer has to ask what
        came back after the call."""
        return self._expressions[expression_id]

    @property
    def families(self) -> tuple[str, ...]:
        return tuple(sorted(self._families))

    @property
    def expressions(self) -> tuple[str, ...]:
        return tuple(sorted(self._expressions))

    def law_of(self, identity: str) -> AnalyticalLaw:
        return self._bound[identity]

    def sort_of(self, identity: str) -> Optional[str]:
        """`"family"` / `"expression"` / `None`. **The dispatch question, asked once and before the
        call** — which is what keeps a consumer from having to ask what came back after one."""
        if identity in self._families:
            return "family"
        if identity in self._expressions:
            return "expression"
        return None

    # ── establishment at the root ────────────────────────────────────────────────────────────
    def establish_root(self, family: MeasureFamily, rows: Iterable[Mapping[str, Any]], *,
                       value_key: str = "value",
                       data_state: str = UNSTATED_DATA_STATE,
                       intent: Optional[TransitionIntent] = None) -> Answer:
        """**Constitute `F@R_F` from occurrences.** The canonical continuation origin, and the only place
        raw contributions land: a contribution is an occurrence at the family's root, and "a contribution
        at a coarser anchor" is not a thing the theory has.

        Each root cell's occurrences are handed to the provider's `contribute` as BOTH the bare operand
        values and the whole rows. The rows are there for an ORDERED law, which cannot select a witness
        from values alone — it needs the governed order key beside each one — and passing them always is
        cheaper than a second entry point that exists for one law's benefit."""
        law = self._bound[family.family_id]
        contribute = self.provider.capability(law.name, "contribute")
        buckets: dict[tuple, list[Mapping[str, Any]]] = {}
        for row in rows:
            buckets.setdefault(self.universe.cell_of(family.root, row), []).append(row)
        params = dict(family.parameters)
        if family.order_by:
            params["order_by"] = family.order_by
        cells = {cell: contribute([r.get(value_key) for r in rws], {**params, "rows": rws,
                                                                    "value_key": value_key})
                 for cell, rws in buckets.items()}
        state = FamilyState(point=family.root_point, law=law.name, value_form=law.value_form,
                            cells=cells,
                            instance=replace(family.instance(data_state=data_state),
                                             constitution_context=self.build.reference),
                            forgotten_since_root=frozenset())
        admission = self.admit(state, establishment=Establishment(AT_ROOT), intent=intent)
        if not admission:
            raise KernelRefusal(admission.code, family.family_id, admission.detail)
        return Answer(route=ROOT, value=state)

    # ── retention ────────────────────────────────────────────────────────────────────────────
    def retain(self, value: Any) -> Retained:
        """Hold an object. **Holding is not authority** — every right it might confer is adjudicated at
        use, so this method asks nothing and refuses nothing."""
        sort = value.point.sort
        identity = getattr(value.point, "family_id", None) or value.point.expression_id
        if sort == "family":
            # **FAMILY STATE IS A CACHE OBJECT, NOT A KEYED SLOT.** It goes to the materialization store,
            # which mints an opaque identity so two instances of one `F@A` can coexist. Expressions stay
            # here: MME v1 does not manage `E@A`, and until they move above the engine entirely they are
            # held in the old keyed store where they cannot be mistaken for family materializations.
            admission = self.admit(value)
            if not admission:
                raise KernelRefusal(admission.code, identity, admission.detail)
            return Retained(key=self._descriptor(self.materializations.get(admission.id)),
                            value=value)
        key = RetentionKey(sort=sort, identity=identity, anchor=value.anchor,
                           instance=value.instance, realization=self.realization,
                           constitution=self.witness_of(identity).digest)
        retained = Retained(key=key, value=value)
        self._store[key] = retained
        return retained

    # ── admission: the one door for family material ──────────────────────────────────────────
    def admit(self, value: Any, *, establishment: Optional[Establishment] = None,
              intent: Optional[TransitionIntent] = None, residency: str = "resident",
              witness: Optional[str] = None, note: str = ""):
        """**Offer one governed family value to the cache.**

        `establishment` is the material's ACTUAL standing and is never manufactured (ruled §8): a value
        formed at `R_F` is `AT_ROOT`, one folded from held material is `CONTINUED` and names its parent, and
        one supplied at a non-root anchor by a governed realization is `INDEPENDENT` — which is a different
        claim from "it was derived and we lost the receipt".

        Two analytical checks run before any cache consequence:

        * **off-build material** — if the offerer supplies a constitution witness, it must be this build's;
        * **entitlement** — a materialization may only exist where the family law admits a value, and that
          is `region.admits(R_F − anchor)`, asked identically of derived and independent material."""
        identity = value.point.family_id
        family, law = self._families[identity], self._bound[identity]
        if witness is not None and witness != self.witness_of(identity).digest:
            return Admission(False, code="off-build-material",
                             detail=f"the offered material carries constitution witness {witness} and this "
                                    f"build constitutes {identity!r} as "
                                    f"{self.witness_of(identity).digest}. A new Manifold build is a new "
                                    f"semantic world; material does not cross into one by being present.")
        if not law.region.admits(cumulative_forgotten(family, value.anchor)):
            return Admission(
                False, code="anchor-outside-the-continuation-region",
                detail=f"{identity} may hold no lawful value at {value.anchor}: reaching it from "
                       f"{family.root} forgets {sorted(cumulative_forgotten(family, value.anchor))}, which "
                       f"{law.region.why_not(cumulative_forgotten(family, value.anchor))}. **THIS IS ASKED "
                       f"OF INDEPENDENTLY ESTABLISHED MATERIAL TOO**: a governed realization can supply a "
                       f"value, and cannot make the family's law admit one where it does not.")
        if establishment is None:
            establishment = Establishment(
                AT_ROOT if value.anchor == family.root else INDEPENDENT)
        return self.materializations.admit(
            point=value.point, instance=value.instance, value=value,
            establishment=establishment, realization=self.realization, intent=intent,
            residency=residency, note=note)

    @staticmethod
    def _descriptor(m: FamilyMaterialization) -> RetentionKey:
        """A `RetentionKey`-shaped **descriptor** of a materialization, for readers that ask what is held.

        It is no longer an identity — `m.id` is — and nothing looks anything up by it. It exists because the
        analytical attributes remain the useful thing to report and select on."""
        return RetentionKey(sort="family", identity=m.family_id, anchor=m.anchor,
                            instance=m.instance, realization=m.realization,
                            constitution=m.build.reference)

    def retained(self, point: Any, instance: Any) -> Optional[Retained]:
        """The CURRENT materialization at this point under this instance, if one is held.

        A convenience over `select`, kept because *"what is held for `F@A`"* is the question callers ask.
        It answers with the cheapest current candidate; which retained instance that is remains the MME's
        choice and never the caller's (ruled §2)."""
        identity = getattr(point, "family_id", None) or getattr(point, "expression_id", None)
        if point.sort == "family":
            held = self.materializations.select(identity, anchor=point.anchor, instance=instance,
                                                serviceable=True)
            if not held:
                return None
            best = min(held, key=lambda m: (len(getattr(m.value, "cells", ()) or ()), -m.admitted_seq))
            return Retained(key=self._descriptor(best), value=best.value)
        return self._store.get(RetentionKey(point.sort, identity, point.anchor, instance,
                                            self.realization, self.witness_of(identity).digest))

    def holdings(self) -> tuple[Retained, ...]:
        """**Everything held, as objects rather than keys** — family materializations and expression
        outputs. Reach for this rather than the internal store: a materialization is located by its opaque
        id, and the descriptor on a `Retained` is a report, not a lookup handle."""
        return tuple([Retained(key=self._descriptor(m), value=m.value)
                      for m in self.materializations.all() if m.has_payload]
                     + list(self._store.values()))

    def materialization(self, mid: MaterializationId) -> Optional[FamilyMaterialization]:
        """One retained instance, by its opaque cache identity."""
        return self.materializations.get(mid)

    def candidates(self, family: MeasureFamily) -> tuple[Retained, ...]:
        """Every retained object that *might* seed this family, **including the ones that may not.**
        Separating candidacy from permission is the whole shape of this module: a test can hold a
        candidate in one hand and its refusal in the other."""
        return tuple(Retained(key=self._descriptor(m), value=m.value)
                     for m in self.materializations.select(family.family_id, eligibility=None)
                     if m.has_payload)

    @property
    def held(self) -> tuple[RetentionKey, ...]:
        """Descriptors of everything held — family materializations and expression outputs alike."""
        return tuple([self._descriptor(m) for m in self.materializations.all()] + list(self._store))

    # ── the adjudication ─────────────────────────────────────────────────────────────────────
    def adjudicate(self, candidate: Retained, family: MeasureFamily, target: Anchor) -> Adequacy:
        """**May this held object seed a continuation to `target`?** Five questions, in this order."""
        law = self._bound[family.family_id]
        value = candidate.value

        # 1 · SORT. An expression output is refused here by a governed verdict. The type already makes
        #     it impossible — `ExpressionOutput` has no `fold_onto` — and this exists so the caller is
        #     told which rule stopped them instead of what Python noticed.
        if not candidate.continuation_bearing:
            return Adequacy(
                False, "not-continuation-bearing",
                f"{candidate.key} is a FINALIZED EXPRESSION RESULT. It may be cached and served — it is "
                f"both, right now — and it never becomes family continuation state. An expression's "
                f"value is re-evaluated from a sufficient basis at each location; it does not compose, "
                f"and being named, cached, repeated or durably governed does not make it "
                f"continuation-bearing (ToD v8 §3.7)")

        # 2 · REACHABILITY. Geometry, not law.
        if value.anchor == target:
            return Adequacy(True, "exact", "already at the asked location")
        if not value.anchor.refines(target):
            return Adequacy(
                False, "not-reachable",
                f"{value.anchor} is not finer than {target}, so {target} is not reachable from it by "
                f"forgetting constituents. A coarsening forgets; it does not acquire")

        # 3 · CLOSURE OVER THE WHOLE ROUTE FROM THE ROOT — the laundering guard, ROOT-RELATIVE.
        #
        # **DERIVED, NOT READ OFF THE STATE** (ruled 2026-09-29 §7). The cumulative forgotten set is set
        # subtraction, so for `T ⊆ M ⊆ R` every route forgets `(R − M) ∪ (M − T) = R − T`. The route cannot
        # change it, so the guard is a function of the family law, `R_F` and the TARGET — and the
        # intermediate materialization, its provenance and its resident ancestors never enter. That is what
        # makes "evicting an ancestor must not create new analytical rights" true by construction rather
        # than by remembering. `forgotten_since_root` survives as PROVENANCE and is no longer authority; a
        # test pins the equivalence so that widening `ContinuationRegion` into a genuine per-edge graph —
        # the one change that would make routes matter — fails loudly here.
        forgotten_total = cumulative_forgotten(family, target)
        if not law.region.admits(forgotten_total):
            through = (f" This candidate sits at {value.anchor}, a NON-ROOT materialization, and that "
                       f"changes nothing: the question is the whole route from {family.root}, so an "
                       f"intermediate materialization cannot launder an edge the law does not admit."
                       if value.anchor != family.root else "")
            return Adequacy(
                False, "outside-continuation-region",
                f"{family.family_id}: {law.region.why_not(forgotten_total)}.{through}")

        # 4 · ADEQUACY OF THE VALUE. Does it still carry the sufficient state the composition needs?
        if law.value_form == STRUCTURED and value.value_form != STRUCTURED:
            return Adequacy(
                False, "state-no-longer-sufficient",
                f"{candidate.key} holds a {value.value_form!r} value where {law.name} composes over a "
                f"{STRUCTURED!r} one. {law.sufficient_state}")

        # 5 · REALIZATION. A provider limit, said as one.
        if not self.provider.realizes(law.name):
            return Adequacy(
                False, "unrealized-law",
                f"law {law.name!r} has no realization in provider profile {self.provider.name!r}. The "
                f"law is unchanged; this build cannot execute its composition (ToD v8 §4.1)")

        origin = "R_F" if value.at_root else f"a non-root materialization at {value.anchor}"
        return Adequacy(True, "admitted",
                        f"seeded from {origin}; forgetting {sorted(forgotten_total)} is inside "
                        f"{family.family_id}'s continuation region")

    # ── serving a family ─────────────────────────────────────────────────────────────────────
    def measure(self, family: MeasureFamily, anchor: Anchor, *, retain: bool = True,
                data_state: Optional[str] = None) -> Answer:
        """**Serve `F@A`.** Exact hit, else the best admitted seed, else a refusal that names why.

        **THE ROOT IS PREFERRED AND NON-ROOT SEEDS ARE PERMITTED**, which is the required distinction. A
        non-root materialization is a legitimate continuation origin *while its value remains adequate*,
        and `adjudicate` is where "remains adequate" is decided — not here, and not by preferring the
        root so hard that the non-root case is never exercised."""
        law = self._bound[family.family_id]
        instance = self.instance_of(family.family_id)
        considered: list[str] = []

        # ── CANDIDATE SELECTION IS THE MME'S, NEVER THE CALLER'S (ruled 2026-09-29 §2) ──────────────
        # The request asked for an analytical identity; which retained instance answers it is a cache
        # decision, made here by cost. Only CURRENT, payload-bearing materializations are candidates:
        # a superseded one may stay resident for as long as policy likes and will never answer.
        pool = self.materializations.candidates_for(family.family_id, anchor, instance,
                                                    data_state=data_state)
        exact = next((m for m in pool if m.anchor == anchor), None)
        if exact is not None:
            return Answer(route=CACHED, value=exact.value, disclosures=exact.value.disclosures,
                          considered=(str(self._descriptor(exact)),))

        # **LEAST WORK FIRST, FALLING BACK TOWARD THE ROOT** — and the order is a governed choice, not
        # an optimization detail.
        #
        # The first draft tried the ROOT FIRST, which is wrong twice over. It does the most possible work
        # on every ask, and — the real defect — it makes non-root materialization POINTLESS, so the
        # engine could never exercise the right the ruling specifically asks it to make operational: *"a
        # lawful F@A may be cached and may seed later continuation."* A rule that is never reached is not
        # a rule that holds.
        #
        # So candidates are ordered COARSEST FIRST among those still finer than the target, which is the
        # fewest cells to fold. The fallback direction is safe because a FINER seed has forgotten LESS,
        # so it is never less permissive: if any candidate is admitted, the root is admitted. Trying the
        # cheapest first therefore cannot turn a servable ask into a refusal — it can only turn a more
        # expensive answer into a cheaper one.
        blockers: list[Adequacy] = []
        for materialization in pool:
            descriptor = self._descriptor(materialization)
            considered.append(str(descriptor))
            candidate = Retained(key=descriptor, value=materialization.value)
            verdict = self.adjudicate(candidate, family, anchor)
            if not verdict:
                blockers.append(verdict)
                continue
            state = candidate.value
            if state.anchor != anchor:
                merge = self.provider.capability(law.name, "merge")
                state = state.fold_onto(anchor, merge)
            if law.approximation != "exact":
                state = state.with_disclosure(Disclosure(
                    "approximate", f"{law.name} is {law.approximation}; every value served from it "
                                   f"carries that standing"))
            if retain:
                # **THE DEPENDENCY EDGE IS RECORDED HERE AND NOWHERE ELSE.** A continuation names what it
                # was continued FROM, which is the relation supersession propagates along — and is a
                # different fact from the entitlement, which is derived from the family root.
                self.admit(state, establishment=(
                    Establishment(CONTINUED_FROM, (materialization.id,))
                    if state.anchor != materialization.anchor else Establishment(AT_ROOT)))
            route = ROOT if state.anchor == family.root else CONTINUED
            return Answer(route=route, value=state, disclosures=state.disclosures,
                          seeded_from=descriptor, considered=tuple(considered))

        # **THE BLOCKERS ARE DEDUPED AND THE UNINFORMATIVE ONES DEMOTED**, because a refusal that recites
        # the same reason once per candidate is a refusal nobody finishes reading. `not-reachable` is
        # geometry — a candidate at a sibling location — and says nothing about the ask unless it is the
        # only thing to say, so it sorts last.
        best: dict[str, Adequacy] = {}
        for b in blockers:
            kept = best.get(b.code)
            # ONE ENTRY PER CODE, keeping the LONGEST detail. Two candidates blocked for the same reason
            # produce the same code with different amounts of explanation — the laundering guard's
            # message names the route it came through and the direct one does not — and the longer text
            # strictly contains the shorter, so keeping it loses nothing and repeats nothing.
            if kept is None or len(b.detail) > len(kept.detail):
                best[b.code] = b
        ordered = sorted(best.values(), key=lambda b: b.code == "not-reachable")
        detail = (" · ".join(f"{b.code} — {b.detail}" for b in ordered)
                  or f"no retained state of {family.family_id} exists under this analytical instance, "
                     f"and this engine does not invent one: a value must be established at "
                     f"{family.root} before it can be continued anywhere") + self._also_held(family)
        return Answer(route=REFUSED, considered=tuple(considered),
                      refusal=Refusal("unanswerable", str(family.at(anchor)), detail))

    def _also_held(self, family: MeasureFamily) -> str:
        """What IS held that could not answer — so a refusal never pretends the cache is empty when it is
        merely not current, or resident but evicted."""
        parts = []
        not_current = self.materializations.select(family.family_id, eligibility=SUPERSEDED)
        if not_current:
            parts.append(f"{len(not_current)} retained materialization(s) of {family.family_id!r} are held "
                         f"and are NOT CURRENT (superseded): "
                         f"{[f'{m.id}@{m.anchor}' for m in not_current]}. Residency never creates "
                         f"analytical authority, so their bytes being present is not an answer.")
        without_payload = [m for m in self.materializations.select(family.family_id, eligibility=CURRENT)
                           if not m.serviceable]
        if without_payload:
            parts.append(f"{len(without_payload)} current materialization(s) are unusable by POLICY "
                         f"(evicted or expired): {[f'{m.id}:{m.residency}' for m in without_payload]}. "
                         f"That is OUR absence, not the world's — the remedy is to establish the state "
                         f"again, not to conclude anything about the evidence.")
        return (" " + " ".join(parts)) if parts else ""

    # ── serving an expression ────────────────────────────────────────────────────────────────
    def evaluate(self, expression: GovernedExpression, anchor: Anchor, *,
                 basis_id: Optional[str] = None, retain: bool = True,
                 data_state: Optional[str] = None) -> Answer:
        """**Evaluate `E@A` from a sufficient basis.** Never from a continuation, because there is none.

        Where more than one basis is admitted they are tried in declaration order and the FIRST that
        establishes wins; the refusal, if none does, reports every route it tried and why each failed.
        That is what makes "refuse an incompatible basis even when both operands individually exist" a
        legible answer rather than a bare `no`."""
        law = self._bound[expression.expression_id]
        instance = expression.instance()
        considered: list[str] = []

        resolution = resolve_pool(self._store.values(), expression.expression_id, instance,
                                  self.witness_of(expression.expression_id).digest,
                                  str(expression.at(anchor)), data_state)   # expressions only, in v1
        if resolution.refusal is not None:
            return Answer(route=REFUSED, refusal=resolution.refusal)
        exact = next((r for r in resolution.pool
                      if r.key.anchor == anchor and not r.continuation_bearing), None)
        if exact is not None:
            return Answer(route=CACHED, value=exact.value, disclosures=exact.value.disclosures,
                          considered=(str(exact.key),))

        routes = ([b for b in expression.admitted_bases if b.basis_id == basis_id]
                  if basis_id else list(expression.admitted_bases))
        if not routes:
            missing = (f"basis {basis_id!r} is not admitted by this expression"
                       if basis_id else
                       "this expression admits NO sufficient basis. It is well-formed and not "
                       "evaluable — a constituted expression may exist before any establishment route "
                       "is admitted, and that is a capability limit rather than a defect")
            return Answer(route=REFUSED,
                          refusal=Refusal("no-admitted-basis", str(expression.at(anchor)), missing))

        failures: list[str] = []
        for basis in routes:
            considered.append(basis.basis_id)
            attempt = self._establish(expression, law, basis, anchor, data_state)
            if attempt.served:
                output = attempt.value
                if retain:
                    self.retain(output)
                return Answer(route=EVALUATED, value=output, disclosures=output.disclosures,
                              seeded_from=basis.basis_id, considered=tuple(considered))
            failures.append(f"basis {basis.basis_id!r}: {attempt.refusal.detail}")

        return Answer(route=REFUSED, considered=tuple(considered),
                      refusal=Refusal(
                          "no-sufficient-basis-establishes", str(expression.at(anchor)),
                          " | ".join(failures) + ". Every admitted route was tried. NOTE WHAT THIS IS "
                          "NOT: it is not a claim that the operands are absent — where they are present "
                          "and incompatible, the refusal above says so, because physical availability "
                          "is not analytical authority"))

    def _establish(self, expression: GovernedExpression, law: AnalyticalLaw,
                   basis: SufficientBasis, anchor: Anchor,
                   data_state: Optional[str] = None) -> Answer:
        """One route, tried. Returns the `ExpressionOutput` or the refusal that stopped it."""
        subject = f"{expression.expression_id}@{anchor} via {basis.basis_id}"
        states: dict[str, FamilyState] = {}
        for role in basis.component_laws:
            component = self._families[basis.components[role]]
            served = self.measure(component, anchor, data_state=data_state)
            if not served.served:
                return Answer(route=REFUSED, refusal=Refusal(
                    "role-unfilled", subject,
                    f"role {role!r} is filled by {component.family_id!r}, which cannot be served at "
                    f"{anchor}: {served.refusal.detail}"))
            states[role] = served.value

        # COMPATIBILITY. Asked BEFORE any arithmetic, over states that all exist — which is the whole
        # point: two individually valid components can be jointly meaningless.
        if basis.requires_common_participation:
            roles = list(states)
            reference = states[roles[0]]
            for role in roles[1:]:
                agreement = reference.instance.compatible_with(states[role].instance)
                if not agreement:
                    return Answer(route=REFUSED, refusal=Refusal(
                        "incompatible-basis", subject,
                        f"roles {roles[0]!r} and {role!r} are both ESTABLISHED AND AVAILABLE at "
                        f"{anchor} and are not jointly usable [{agreement.code}]: {agreement.detail}. "
                        f"{law.required_basis.note if law.required_basis else ''} The word doing the "
                        f"work is MATCHING — components that ranged over different contributions are "
                        f"individually valid and jointly meaningless, so their combination is a number "
                        f"about no population".strip()))

        apply = self.provider.capability(law.name, "apply")
        keys: set[tuple] = set()
        for state in states.values():
            keys |= set(state.cells)
        cells: dict[tuple, Any] = {}
        undefined: list[tuple] = []
        for key in sorted(keys):
            payloads = {role: state.cells.get(key) for role, state in states.items()}
            if any(p is None for p in payloads.values()):
                undefined.append(key)
                continue
            result = apply(payloads, dict(expression.parameters))
            if result is None:
                # §4.3's case: the basis is established and the expression is UNDEFINED on it. A
                # governed answer about that cell, not an error and not a zero.
                undefined.append(key)
                continue
            cells[key] = result

        # **THE OUTPUT IS ATTRIBUTED TO THE EVIDENCE STATE ITS OPERANDS CAME FROM**, where they agree on
        # one. Where they do not — possible only for a basis the law does not require common participation
        # for — it is attributed to none, which is what `UNSTATED_DATA_STATE` says: not a lie about a
        # single evidence state, and not a new token invented to describe a mixture.
        operand_states = {st.instance.data_state for st in states.values()}
        attributed = operand_states.pop() if len(operand_states) == 1 else UNSTATED_DATA_STATE
        output = ExpressionOutput(point=expression.at(anchor), constructor=law.name, cells=cells,
                                 instance=expression.instance(data_state=attributed),
                                 basis_id=basis.basis_id)
        for state in states.values():
            for d in state.disclosures:
                output = output.with_disclosure(d)
        if undefined:
            output = output.with_disclosure(Disclosure(
                "undefined-on-basis",
                f"{len(undefined)} cell(s) carry no value: the basis is established there and the "
                f"expression is UNDEFINED on it (ToD v8 §4.3). Distinct from absent and from zero"))
        return Answer(route=EVALUATED, value=output)

    # ── invalidation — CONSERVATIVE, and that is the ruling ──────────────────────────────────
    def invalidate(self, identity: str) -> tuple[RetentionKey, ...]:
        """Drop every retained object of `identity`. **Rebuild is from the root.**

        No delta retraction and no deletion maintenance, deliberately: a mergeable family is not thereby
        a *retractable* one, and ToD v8 §3.1 says so in its own words — value closure *"does not imply
        recoverability of prior contributions or sufficiency for restriction, deletion, correction, or a
        changed analytical law."* Implementing retraction because the algebra looks like a group would be
        granting a capability the theory withholds."""
        dropped = tuple(k for k in self._store if k.identity == identity)
        for k in dropped:
            del self._store[k]
        materialized = self.materializations.select(identity, eligibility=None)
        for m in materialized:
            self.materializations.unpin(m.id)                 # invalidation is deliberate; pinning is not a veto
            self.materializations.drop(m.id)
        return dropped + tuple(self._descriptor(m) for m in materialized)


__all__ = ["MME", "Adequacy", "PoolResolution", "Retained", "RetentionKey", "Staleness",
           "resolve_pool"]
