"""
columna_platform.kernel.mme — **the in-memory Materialized Measure Engine. Family materializations only.**

    **MME manages only family materializations `F@A`.**  — Huayin, 2026-09-29 (M-2 §1)

That box is this module's boundary, and after M-2 it is a property of the code rather than a convention.
There is no expression store here, no expression retention key, no expression lifecycle and no method that
returns an `ExpressionOutput`. Expressions are **constituted** by this engine — registered, law-bound,
witnessed — and **evaluated above it**, by `kernel.expression.ExpressionEvaluator`, which consumes family
state through `measure` like any other consumer.

THE THREE DISTINCTIONS THIS ENGINE MAKES OPERATIONAL
----------------------------------------------------
Ruled (Huayin, 2026-09-28):

  **Family root authority.**              `F@R_F` is the canonical continuation origin.
  **Non-root family materialization.**    A lawful `F@A` may be cached and may seed later continuation
                                          ONLY WHILE its family value remains adequate for that admitted
                                          continuation.
  **Physical availability is not analytical authority.**

A fourth was ruled with them — *"`E@A` may be cached and served but never becomes family continuation
state"* — and M-2 settles it by removing its first clause: in v1 `E@A` is not cached at all, so the only
thing left to keep true is the second clause, which is now true because there is nowhere for an expression
output to be that the continuation machinery can see. `adjudicate`'s sort question survives as a
**boundary** verdict for objects handed in from above, not as a screen over the store's own contents.

The last distinction is the load-bearing one, and it is why this module is shaped as `retain` /
`candidates` / `adjudicate` / `serve` rather than as a cache with a lookup. **Holding an object and being
permitted to use it are two facts**, and `adjudicate` is the only place the second is decided. Every
refusal below is a refusal about an object that is sitting in the store.

THE REQUEST BOUNDARY IS OBSERVED
--------------------------------
Ruled §4/§7: every request for family state is observable — READY, NEED, WANT_OF_STATE or UNSUPPORTED —
and *"observation should happen at the request boundary, not only when a cached materialization is
selected."* `measure` is that boundary, and it emits exactly one `RequestObservation` on every path
including every refusal. The emission is append-style, write-only and wrapped so that an observer which
raises costs the request nothing: **serving correctness never depends on logging** (§4). Nothing in this
module ever reads an observation back, which is how *"observations never create analytical rights"* (§6)
is held as a property rather than remembered as a rule.

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

import time
from dataclasses import dataclass, replace
from typing import Any, Iterable, Mapping, Optional

from .geometry import Anchor, KernelRefusal, Universe
from .law import AnalyticalLaw, LawRegistry, STRUCTURED
from .realization import ProviderProfile, RealizationStanding
from .sorts import GovernedExpression, MeasureFamily
from .standing import (
    CACHED,
    CONTINUED,
    UNSTATED_DATA_STATE,
    REFUSED,
    ROOT,
    Refusal,
)
from .observation import (
    FamilyRequest,
    Fulfillment,
    NEED,
    ObservationSink,
    READY,
    WorkloadObserver,
    disposition_for,
    observe_request,
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
)
from .authorization import (
    AuthorizedFamilyContinuation,
    AuthorizedStanding,
    ContinuationAuthority,
)
from .realization_fidelity import RealizationAuthority
from .requirement import RequirementOutcome
from .value import Answer, FamilyState
from .witness import ConstitutionWitness


# ── retention ────────────────────────────────────────────────────────────────────────────────────
@dataclass(frozen=True)
class RetentionKey:
    """**The analytical description of one retained family materialization.**

    Ruled: *"Do not reproduce existing cache keys merely because they exist… Do not over-design the
    final persistent key yet."* So this carries exactly the axes a retained object must be told apart by:

      `identity`        the governed `family_id`;
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

    **`sort` IS RETIRED IN M-2, AND ITS RETIREMENT IS A RESULT** (ruled 2026-09-29 M-2 §2: *"assess
    whether M-2 now allows retirement of `RetentionKey.sort`"* — it does). The field existed because family
    state and expression output shared this key and had to be told apart in it. They no longer share it:
    the MME retains family materializations and nothing else, so `sort` could only ever hold `"family"`, and
    a key axis with one inhabitant is not an axis. **The SORT DISTINCTION is untouched** — `FamilyState` and
    `ExpressionOutput` are still two types with two sets of rights, `FamilyPoint.sort` still answers which,
    and `adjudicate`'s first question still refuses a non-continuation-bearing object by a governed verdict.
    What is gone is the need to re-state that distinction *inside the cache key*, because the cache now has
    only one sort in it.

    Not here: a physical grain, a storage location, a partition, a file. Those are storage facts, and
    ToD v8 keeps storage out of identity."""

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

    #: **A CONSTANT, NOT A FIELD.** Readers, exhibits and log lines that printed `family:revenue@…` still
    #: print it, and nothing can construct a key claiming to be anything else.
    sort = "family"

    def __str__(self) -> str:
        return f"{self.sort}:{self.identity}@{self.anchor}"


@dataclass(frozen=True)
class Retained:
    """One held family materialization, as a value plus its analytical description."""

    key: RetentionKey
    value: Any                       # FamilyState (columnar or in-memory)

    @property
    def continuation_bearing(self) -> bool:
        """**Still asked, and now asked of things arriving from ABOVE the engine.**

        Inside the MME this is now invariably true — nothing else can be retained. It survives because
        `adjudicate` is a *public* verdict that anything may be handed to, including an `ExpressionOutput`
        held by the evaluator above, and a boundary that refuses by returning a governed reason is worth
        more than one that refuses by being impossible to reach."""
        return bool(getattr(self.value, "CONTINUATION_BEARING", False))


# ── THE PRIOR QUESTIONS, AND WHY THIS MODULE NO LONGER ASKS THEM ────────────────────────────────
# M-1 shipped `PoolResolution` / `resolve_pool`: a screen that asked, before any adjudication, whether a
# held object was (a) under the CURRENT constitution and (b) drawn from ONE evidence state. **M-2 retires
# both**, and the reason is that each question is now answered STRUCTURALLY on the family path rather than
# procedurally at read time:
#
#   (a) CONSTITUTION.   M-1 made the Manifold BUILD the semantic partition — a materialization carries its
#                       `build`, and `AnalyticalInstance.constitution_context` carries the build reference,
#                       so `same_but_for_data_state` already excludes material from a superseded
#                       constitution. `stale_states()` keeps reporting WHICH determinant moved.
#   (b) EVIDENCE STATE. `MaterializationStore._coexistence_standing` refuses to make a second evidence
#                       state CURRENT in one slot, so "two current data states, neither of them the
#                       answer" is not a situation this engine can be in. It was a REFUSAL in M-1 and it is
#                       an UNREACHABLE STATE in M-2, which is strictly stronger: the ambiguity is prevented
#                       at admission instead of detected at serving.
#
# The screen's only remaining caller was the **expression cache**, and M-2 does not have one. Deleting it
# is therefore not a loss of a governed refusal; a test pins both replacements so that a future widening
# which reintroduces the ambiguity fails loudly rather than silently picking an evidence state.


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
                 manifold: str, build: str,
                 observer: Optional[WorkloadObserver] = None) -> None:
        """**`manifold` and `build` are REQUIRED** (J-0). They used to default to `"default"` and
        `"build-1"`, so two engines constructed without arguments shared one `build.reference` and every
        guard keyed on it compared a world to itself. An engine that cannot say which build it is cannot
        refuse another build's material, and the ceremony is one keyword at twenty-five call sites."""
        # **ONE MME PER MANIFOLD JURISDICTION.** A logical rule, not a deployment one: this engine may
        # share its process, its provider and its store with any number of others. What it may not share
        # is authority, so it refuses to register an object belonging to another Manifold — the accident
        # the ruling is against is one runtime holding two worlds that use the same family name.
        self.manifold = manifold
        #: **The Manifold BUILD is the cache's semantic world** (ruled 2026-09-29 §6:
        #: `constitution_context = ManifoldBuildId`). A new build is a new world and old cache state is not
        #: reused into it by default — which is why the store is per-build and the per-object witness is no
        #: longer the runtime partition mechanism.
        self.build = ManifoldBuild(manifold=manifold, build=build)
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
        #: **The workload observation seam** (ruled M-2 §4). Write-only, append-style, and wrapped so that
        #: it cannot fail a request. Defaults to a `NullObserver`, so an engine nobody is watching pays
        #: nothing and — importantly — takes exactly the same code path as one that is: there is no
        #: `if observing:` branch anywhere in `measure`, because a serving path that differs by whether it
        #: is being logged is a serving path whose logs describe a different program.
        self.observations = ObservationSink(observer)
        #: **Every constitution this engine has seen, by digest.** Its own constitutional history, kept so
        #: that staleness can name WHICH determinant moved rather than only that something did. It grows on
        #: re-registration and nothing is ever removed: a superseded constitution is a fact about the past,
        #: and forgetting it would make the state held under it unexplainable.
        self._constitutions: dict[str, ConstitutionWitness] = {}
        #: Stores holding material under this authority's build — this engine's own, plus any columnar
        #: engine attached to it. Every one of them must be ON this build; `attach_store` enforces it.
        self._attached: list[MaterializationStore] = [self.materializations]
        #: **THE COMPONENT THAT OWNS ANALYTICAL CONTINUATION AUTHORIZATION** (B-0b). Constructed over this
        #: engine because this class is still the Manifold build authority as well as the cache — the
        #: residual the B-0 reconciliation named. What the ruling requires is that the constitutional
        #: READING happen in one place, and it does: `region` is read in `authorization.py` and nowhere
        #: else. `measure`, `admit` and `requirement_for` are this half's methods and go with it when the
        #: class is split; `fulfill` and `put` are the cache's and stay.
        self.authorizer = ContinuationAuthority(self)
        #: **THE COMPONENT THAT OWNS PHYSICAL-REALIZATION FIDELITY** (B-1′). A different question from the
        #: one above: `authorizer` decides whether an operation may be attempted, this decides whether a
        #: particular physical result IS the object it claims to be. It obtains standings through the
        #: authorizer rather than re-reading the constitution, so there is still exactly one reader of the
        #: continuation region.
        self.realizations = RealizationAuthority(self)

    # ── constitution ─────────────────────────────────────────────────────────────────────────
    def register_family(self, family: MeasureFamily) -> MeasureFamily:
        """**Where ToD v8 §9.2 is enforced, by refusing to construct rather than by gating later.**
        `MeasureFamily.bind` raises for a law with no continuation, so a Mean family is not a reachable
        state of this engine."""
        self._require_own(family.manifold, family.family_id)
        bound = family.bind(self.laws)
        witness = family.witness(bound)
        if family.family_id in self._families:
            self._refuse_in_place_movement(family.family_id, witness)
        self._bound[family.family_id] = bound
        self._families[family.family_id] = family
        self._remember(witness)
        return family

    def register_expression(self, expression: GovernedExpression) -> GovernedExpression:
        self._require_own(expression.manifold, expression.expression_id)
        bound = expression.bind(self.laws, self._families)
        witness = expression.witness(bound)
        if expression.expression_id in self._expressions:
            self._refuse_in_place_movement(expression.expression_id, witness)
        self._bound[expression.expression_id] = bound
        self._expressions[expression.expression_id] = expression
        self._remember(witness)
        return expression

    def _require_own(self, manifold: str, identity: str) -> None:
        if manifold != self.manifold:
            raise KernelRefusal(
                "foreign-manifold", identity,
                f"belongs to Manifold {manifold!r} and this MME is the jurisdiction of "
                f"{self.manifold!r}. A governed analytical object belongs to exactly one Manifold; "
                f"registering it here would put one identity under two authorities.")

    def attach_store(self, store: MaterializationStore) -> MaterializationStore:
        """Register another engine's materialization store under this authority. **It must be on this
        build** (J-0): a store is partitioned by the world it belongs to, and attaching one from another
        world would put this authority's name over material it never constituted."""
        if store.build != self.build:
            raise KernelRefusal(
                "foreign-store", str(store.build),
                f"a materialization store for {store.build.reference} cannot be attached to the "
                f"authority of {self.build.reference}. A store is partitioned by build because a build "
                f"is a semantic world; attaching across one would make this authority answerable for "
                f"material constituted under a declaration it does not hold.")
        if store not in self._attached:
            self._attached.append(store)
        return store

    def _refuse_in_place_movement(self, identity: str, now: ConstitutionWitness) -> None:
        """**A build does not reinterpret its own constitution** (J-0, ruling 5).

        The former behaviour was `_declaration_moved`: re-registering a changed declaration superseded
        every materialization of that name, in this store and in every attached one, and filed a
        `Staleness` record describing what moved. Two things were wrong with it. It swept by bare
        `family_id` with no manifold or build filter, so one world's edit could supersede another
        world's material of the same name. And it treated constitutional movement as an event a
        *running* engine absorbs, when a meaning change is a successor build — the store is per-build
        precisely so that the old world's material is unreachable from the new one rather than needing
        to be chased. The observability `stale_states()` carried now rides on this refusal, which names
        the determinants that moved.

        **THE TEST IS THE WITNESS, NOT DATACLASS EQUALITY**, and the distinction is load-bearing. A
        declaration may be re-registered with a non-identity-bearing field changed — a target
        description, an alias, or an ADDITIONAL ADMITTED BASIS, which the 2026-09-28 ruling is explicit
        about: *"admitting a new route must not stale values already established over an existing
        one."* Those are not movement. Only a determinant change is."""
        before = self.witness_of(identity)
        if before.digest == now.digest:
            return
        comparison = before.compare(now)
        raise KernelRefusal(
            "constitution-moved-in-place", f"{identity}@{self.build.reference}",
            f"{identity!r} is already constituted in build {self.build.reference} and the declaration "
            f"offered differs in {', '.join(comparison.changed) or 'an identity-bearing fact'}. A "
            f"governed meaning change is a SUCCESSOR BUILD, not an edit to a running one: material held "
            f"here was established under the constitution this engine still holds, and reinterpreting "
            f"it in place would leave values whose meaning nobody can state. Build again. "
            f"{comparison.detail}")

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

    def instance_of(self, identity: str) -> Any:
        """The analytical instance of a registered object — **stamped with this engine's Manifold.**

        The single place an instance is obtained, so no caller can construct one that forgets which
        jurisdiction it belongs to."""
        obj = self._families.get(identity) or self._expressions[identity]
        return replace(obj.instance(), constitution_context=self.build.reference)

    def family(self, family_id: str) -> MeasureFamily:
        return self._families[family_id]

    def subject(self, family_or_id: Any) -> MeasureFamily:
        """**One family, however the caller named it** — a `MeasureFamily` or its `family_id`.

        Added in F-1, and it is a seam correction rather than a convenience. The two engines had
        divergent signatures: `kernel.MME.measure` took a `MeasureFamily` and `ColumnarMME.measure` took a
        `family_id` string, so **no component above them could call both** — a Fulfillment Coordinator
        written against either one was written against that substrate. Normalising here, in the analytical
        authority that owns the registry, is the smallest fix that does not move a single existing call
        site: every caller keeps the spelling it had.

        It is deliberately NOT a lookup that returns either sort — `sort_of` is still asked first, and
        `expression()` is still a peer of `family()` (M-2). This normalises the SPELLING of one family, not
        the question of which sort a token is.

        **AND IT IS WHERE REGISTERED-DECLARATION AUTHORITY IS ESTABLISHED** (J-0). It used to return the
        caller's object verbatim, which made it the widest door in the kernel: `authorize`,
        `authorize_standing`, `requirement_for`, `measure`, `requirement_for` and the Fulfillment
        Coordinator all funnel through here, and each then read `root`, `parameters` and `instance()` off
        an object nobody had checked while taking the LAW from this engine's registry. A declaration from
        another build — or a same-named declaration from this one that nobody constituted — was
        authorized against a constitution it does not belong to.

        The test is equality against what this build registered, **not** `obj.manifold == self.manifold`.
        That is deliberate and it is stronger three ways: it catches an object that merely *claims* the
        right Manifold; it catches a same-Manifold object whose root or parameters differ from the
        constituted one, which a name check waves through and which is exactly what the callers above go
        on to read; and it needs no new field, because `MeasureFamily` is frozen and compares by value.
        **Constitution is authority; self-description is not.**

        It returns the REGISTERED declaration rather than the caller's equal copy, so that everything
        downstream reads the constituted object."""
        if isinstance(family_or_id, str):
            return self._families[family_or_id]
        return self._constituted(family_or_id, self._families, "family")

    def subject_expression(self, expression_or_id: Any) -> GovernedExpression:
        """`subject`'s peer for the expression sort (M-2 keeps them peers rather than widening either)."""
        if isinstance(expression_or_id, str):
            return self._expressions[expression_or_id]
        return self._constituted(expression_or_id, self._expressions, "expression")

    def _constituted(self, declared: Any, registry: Mapping[str, Any], sort: str) -> Any:
        """**The one jurisdiction test for declarations.** See `subject`."""
        identity = getattr(declared, "family_id", None) or getattr(declared, "expression_id", "?")
        registered = registry.get(identity)
        if registered is None:
            raise KernelRefusal(
                "not-constituted", str(identity),
                f"no {sort} named {identity!r} is constituted in build {self.build.reference}. A "
                f"declaration does not acquire authority by being handed to an engine; it acquires it by "
                f"being registered, and this one was not.")
        if registered != declared:
            raise KernelRefusal(
                "foreign-declaration", str(identity),
                f"the {sort} offered as {identity!r} is not the declaration build "
                f"{self.build.reference} constituted. It may belong to another Manifold, to another "
                f"build of this one, or to nothing at all — this engine cannot tell and must not guess. "
                f"Analytical authority comes from constitution, not from what an object says about "
                f"itself, and reading a root or a parameter off an unconstituted declaration while "
                f"taking the law from this registry would adjudicate a question nobody asked here.")
        return registered

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
        cheaper than a second entry point that exists for one law's benefit.

        **The family is resolved through `subject` first** (J-0): this is the one establishment path that
        does not already go through the authority, and it reads `root`, `parameters`, `order_by` and
        `instance()` off whatever it is handed."""
        family = self.subject(family)
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
        """Hold one **governed family value**. Holding is not authority — every right it might confer is
        adjudicated at use, so this method makes no analytical claim about what it takes.

        **IT TAKES FAMILY STATE AND NOTHING ELSE** (ruled M-2 §1). In M-1 this method branched: family
        state went to the materialization store, and an `ExpressionOutput` was filed in a keyed side store
        living on this object. That side store is gone. An expression output offered here is refused with
        a governed reason rather than quietly accepted into a cache that no longer exists — and the reason
        names where it belongs, because a caller holding a finalized result and looking for somewhere to
        put it has asked a reasonable question with a wrong answer."""
        if value.point.sort != "family":
            identity = getattr(value.point, "expression_id", None) or value.point.identity
            raise KernelRefusal(
                "not-a-family-materialization", str(identity),
                f"{value.point} is an EXPRESSION output, and this engine manages family materializations "
                f"only (M-2 §1). It is not refused because it is unwelcome or because its value is "
                f"suspect — it is refused because there is no expression store here to put it in, and "
                f"adding one back would restore exactly the shared retention key, lifecycle and "
                f"dependency machinery this unit removed. MME v1 does not cache `E@A` at all: an "
                f"expression is re-evaluated from a sufficient basis by "
                f"`kernel.expression.ExpressionEvaluator`, which sits ABOVE this engine and consumes "
                f"the family state it supplies.")
        # **FAMILY STATE IS A CACHE OBJECT, NOT A KEYED SLOT.** It goes to the materialization store,
        # which mints an opaque identity so two instances of one `F@A` can coexist.
        admission = self.admit(value)
        if not admission:
            raise KernelRefusal(admission.code, value.point.family_id, admission.detail)
        return Retained(key=self._descriptor(self.materializations.get(admission.id)), value=value)

    # ── admission ────────────────────────────────────────────────────────────────────────────
    def admit(self, value: Any, *, establishment: Optional[Establishment] = None,
              intent: Optional[TransitionIntent] = None, residency: str = "resident",
              witness: Optional[str] = None, note: str = ""):
        """**Offer one governed family value to the cache.** Mints a standing, then `put`s.

        **THIS METHOD IS THE AUTHORITY HALF'S, NOT THE CACHE'S** (B-0b). It is on this class because this
        class is still both the Manifold build authority and the materialization cache — the residual the
        B-0 reconciliation recorded — and when that class is split it goes with the authority. What matters
        for the ruling is that the *constitutional reading* happens in `ContinuationAuthority` and that
        `put`, the cache door, performs none of it. There is no path to `put` that skips minting.

        `establishment` is the material's ACTUAL standing and is never manufactured (ruled §8): a value
        formed at `R_F` is `AT_ROOT`, one folded from held material is `CONTINUED` and names its parent, and
        one supplied at a non-root anchor by a governed realization is `INDEPENDENT` — which is a different
        claim from "it was derived and we lost the receipt".

        **THE VALUE'S OWN JURISDICTION IS CHECKED HERE** (J-0), with the test the realization path has
        always used — `same_but_for_data_state`, which compares manifold, universe, participation, scope
        and `constitution_context`, and is therefore a jurisdiction test and a build test at once. The
        local path reached the cache without it: `retain` checked only the sort and `establish_root`
        stamped a context onto an instance it had not verified. `retain` inherits this check by calling
        here, and the realization path keeps its own at fidelity check 4."""
        carried = getattr(value, "instance", None)
        if carried is not None:
            declared = self.instance_of(value.point.family_id)
            if not carried.same_but_for_data_state(declared):
                return Admission(
                    False, code="foreign-material",
                    detail=f"the value offered for {value.point.family_id!r} is an instance of "
                           f"{carried.manifold}/{carried.constitution_context} and this engine "
                           f"constitutes it as {declared.manifold}/{declared.constitution_context}. A "
                           f"governed value belongs to the world that established it; holding it here "
                           f"would put one engine's name over another's material.")
        authorized = self.authorizer.authorize_standing(value.point.family_id, value.anchor)
        if not authorized:
            return Admission(False, code=authorized.refusal.code, detail=authorized.refusal.detail)
        return self.put(value, authorized.request, establishment=establishment, intent=intent,
                        residency=residency, witness=witness, note=note)

    def put(self, value: Any, standing: AuthorizedStanding, *,
            establishment: Optional[Establishment] = None,
            intent: Optional[TransitionIntent] = None, residency: str = "resident",
            witness: Optional[str] = None, build: Optional[str] = None,
            realization: Optional[Any] = None, note: str = ""):
        """**THE CACHE DOOR. No constitution is read here, and none can be.**

        Everything below is a cache/materialization question. The two checks it performs are COMPARISONS of
        carried values, never interpretations of governed meaning:

        * **the standing covers this material** — a mint for `revenue@{day}` does not admit `on_hand@{store}`,
          so an authorization cannot be obtained cheaply and reused for something else;
        * **off-build material** — if the offerer supplies a constitution witness it must equal the one the
          standing was minted under. A new Manifold build is a new semantic world and material does not
          cross into one by being present. This is cache coherence: a cache mixing builds serves material
          from a declaration that no longer holds.

        What is NOT here, and is the point of B-0b: no `region`, no `admits`, no law lookup, no
        `cumulative_forgotten`. *"A materialization may only exist where the family law admits a value"* is
        still true and is now true because **no standing is minted where it is false** — asked once, above,
        by the component whose question it is."""
        identity = value.point.family_id
        # **THE STANDING MUST BE THIS ENGINE'S** (J-0). Both checks below this one compare two values the
        # OFFERER supplied against each other, so they agree whenever an offer is internally consistent —
        # including an offer assembled by another build. These two ask the question those could not: was
        # this permission issued by this authority, and is it for this world.
        if not self.authorizer.issued(standing):
            return Admission(
                False, code="foreign-credential",
                detail=f"the standing offered for {identity!r} was not minted by {self.authorizer.name}. "
                       f"A credential is permission from one authority; another authority's permission is "
                       f"a real credential and is not permission here. Obtain one from this engine.")
        if standing.build != self.build.reference:
            return Admission(
                False, code="off-build-material",
                detail=f"the standing was minted against {standing.build} and this engine is "
                       f"{self.build.reference}. A new Manifold build is a new semantic world.")
        if standing.family_id != identity or standing.anchor != value.anchor:
            return Admission(
                False, code="standing-does-not-cover-this-material",
                detail=f"the authorization covers {standing.subject} and the material offered is "
                       f"{identity}@{value.anchor}. An authorization is for one analytical location; "
                       f"reusing one obtained for another is how a caller would manufacture permission "
                       f"without asking for it.")
        if build is not None and build != standing.build:
            return Admission(
                False, code="off-build-material",
                detail=f"the offered material was realized against Manifold build {build} and this engine "
                       f"is {standing.build}. A new Manifold build is a new semantic world; material does "
                       f"not cross into one by being present. **THIS IS CACHE COHERENCE AND IT IS ASKED "
                       f"HERE** — a cache mixing builds serves material from a declaration that no longer "
                       f"holds — which is why the realization authority requires the claim to STATE its "
                       f"build and deliberately does not compare it a second time.")
        if witness is not None and witness != standing.witness:
            return Admission(False, code="off-build-material",
                             detail=f"the offered material carries constitution witness {witness} and this "
                                    f"build constitutes {identity!r} as {standing.witness}. A new Manifold "
                                    f"build is a new semantic world; material does not cross into one by "
                                    f"being present.")
        if establishment is None:
            establishment = Establishment(AT_ROOT if standing.at_root else INDEPENDENT)
        return self.materializations.admit(
            point=value.point, instance=value.instance, value=value,
            establishment=establishment, realization=realization or self.realization, intent=intent,
            residency=residency, note=note)

    @staticmethod
    def _descriptor(m: FamilyMaterialization) -> RetentionKey:
        """A `RetentionKey`-shaped **descriptor** of a materialization, for readers that ask what is held.

        It is no longer an identity — `m.id` is — and nothing looks anything up by it. It exists because the
        analytical attributes remain the useful thing to report and select on."""
        return RetentionKey(identity=m.family_id, anchor=m.anchor,
                            instance=m.instance, realization=m.realization,
                            constitution=m.build.reference)

    def retained(self, point: Any, instance: Any) -> Optional[Retained]:
        """The CURRENT materialization at this point under this instance, if one is held.

        A convenience over `select`, kept because *"what is held for `F@A`"* is the question callers ask.
        It answers with the cheapest current candidate; which retained instance that is remains the MME's
        choice and never the caller's (ruled §2)."""
        if point.sort != "family":
            # **NOT `None`, WHICH WOULD BE A LIE ABOUT AN EMPTY CACHE.** Nothing is held for an expression
            # because nothing CAN be; returning "not held" would invite a caller to establish it and try
            # again forever. (M-2 §1: no expression cache in v1.)
            raise KernelRefusal(
                "not-a-family-materialization", str(point),
                f"{point} is an expression point. This engine holds family materializations only; ask "
                f"`ExpressionEvaluator.evaluate` for `E@A`, which re-establishes it from a sufficient "
                f"basis rather than looking it up.")
        held = self.materializations.select(point.family_id, anchor=point.anchor, instance=instance,
                                            serviceable=True)
        if not held:
            return None
        best = min(held, key=lambda m: (len(getattr(m.value, "cells", ()) or ()), -m.admitted_seq))
        return Retained(key=self._descriptor(best), value=best.value)

    def holdings(self) -> tuple[Retained, ...]:
        """**Everything held, as objects rather than keys.** All of it is family materializations; after
        M-2 there is nothing else it could be. Reach for this rather than the store: a materialization is
        located by its opaque id, and the descriptor on a `Retained` is a report, not a lookup handle."""
        return tuple(Retained(key=self._descriptor(m), value=m.value)
                     for m in self.materializations.all() if m.has_payload)

    def materialization(self, mid: MaterializationId) -> Optional[FamilyMaterialization]:
        """One retained instance, by its opaque cache identity."""
        return self.materializations.get(mid)

    def candidates(self, family: MeasureFamily) -> tuple[Retained, ...]:
        """Every retained object that *might* seed this family, **including the ones that may not.**
        Separating candidacy from permission is the whole shape of this module: a test can hold a
        candidate in one hand and its refusal in the other.

        The family is resolved through `subject` (J-0): this reads a name off whatever it is handed and
        then lists THIS build's material under it, so an unconstituted declaration would have had local
        holdings reported as its own."""
        family = self.subject(family)
        return tuple(Retained(key=self._descriptor(m), value=m.value)
                     for m in self.materializations.select(family.family_id, eligibility=None)
                     if m.has_payload)

    @property
    def held(self) -> tuple[RetentionKey, ...]:
        """Descriptors of every held family materialization."""
        return tuple(self._descriptor(m) for m in self.materializations.all())

    # ── the adjudication ─────────────────────────────────────────────────────────────────────
    def adjudicate(self, candidate: Retained, request: AuthorizedFamilyContinuation) -> Adequacy:
        """**Can THIS held object fulfill an ALREADY-AUTHORIZED continuation?** Four questions, in order.

        Five, since J-0: the first is whether the authorization is this authority's. A credential is a
        permission one build issued; another build's is a real credential and is not permission here.

        **THE SIGNATURE IS THE RESULT OF B-0b.** It was `(candidate, family, target)` and it consulted the
        family law, because the third of its five questions was constitutional. That question is gone — the
        authority answered it before this request existed — and with it went every reason to know the family
        or the law. What remains is a function of the CANDIDATE and the EXECUTION REQUIREMENTS, which is the
        clearest available statement that the adjudication is a cache/execution matter:

            *"MME determines whether held family materialization can fulfill an already-authorized
            continuation request correctly and consistently."*  — Huayin, 2026-09-29

        WHY EACH SURVIVING CHECK IS NOT ANALYTICAL AUTHORIZATION — and §2 asks for this explicitly, because
        geometry is the one most easily mistaken for governance:

          1. **sort** — an expression output is not family state. A TYPE fact; the verdict is a courtesy so
             the caller is told which rule stopped them rather than what Python noticed.
          2. **reachability** — `{store}` cannot reach `{day}`. **THIS IS GEOMETRY, NOT GOVERNANCE**, and the
             distinction matters: `F@{day}` may be perfectly lawful and servable from another seed, and this
             verdict says nothing about whether it is. It says the payload in hand has already forgotten the
             constituent the request needs. Constituent containment is a fact about what a cached value
             retains, not about what a Manifold permits — a cache reporting `not-reachable` is not overruling
             the constitution, it is declining to invent information it threw away.
          3. **payload adequacy** — the fold needs `required_input_value_form` and this payload is not in it.
             A finalized scalar where the composition reads sketches cannot be merged; merging it would
             produce a confident wrong number. Execution, not permission.
          4. **build capability** — can THIS build execute the composition? A provider's inability never
             removes a law and equally never removes the authorization: the request is lawful and
             unservable, which is a different sentence from unlawful. Deliberately kept here rather than in
             the authority, because it is a question about the engine, not the constitution."""
        value = candidate.value

        # 0 · WHOSE PERMISSION IS THIS? (J-0)
        if not self.authorizer.issued(request):
            return Adequacy(
                False, "foreign-credential",
                f"the continuation offered for {request.family_id!r} was not authorized by "
                f"{self.authorizer.name}. An authorization is one build's permission over its own "
                f"governed object; adjudicating held material against another build's permission "
                f"would answer a question this jurisdiction was never asked.")

        # 1 · SORT.
        if not candidate.continuation_bearing:
            return Adequacy(
                False, "not-continuation-bearing",
                f"{candidate.key} is a FINALIZED EXPRESSION RESULT. It may be cached and served — it is "
                f"both, right now — and it never becomes family continuation state. An expression's "
                f"value is re-evaluated from a sufficient basis at each location; it does not compose, "
                f"and being named, cached, repeated or durably governed does not make it "
                f"continuation-bearing (ToD v8 §3.7)")

        # 2 · REACHABILITY. **GEOMETRY, NOT GOVERNANCE.** See the docstring.
        if value.anchor == request.target:
            return Adequacy(True, "exact", "already at the asked location")
        if not value.anchor.refines(request.target):
            return Adequacy(
                False, "not-reachable",
                f"{value.anchor} is not finer than {request.target}, so {request.target} is not reachable "
                f"from it by forgetting constituents. A coarsening forgets; it does not acquire. This is a "
                f"fact about the payload held, not about the target: the continuation is AUTHORIZED and "
                f"another seed may well serve it")

        # 3 · PAYLOAD ADEQUACY. Does it still carry the state the fold's input form requires?
        if (request.fold.required_input_value_form == STRUCTURED
                and value.value_form != STRUCTURED):
            return Adequacy(
                False, "state-no-longer-sufficient",
                f"{candidate.key} holds a {value.value_form!r} value where "
                f"{request.fold.merge_realization} composes over a {STRUCTURED!r} one. "
                f"{request.fold.sufficient_state}")

        # 4 · BUILD CAPABILITY. A provider limit, said as one.
        if not self.provider.realizes(request.fold.merge_realization):
            return Adequacy(
                False, "unrealized-law",
                f"law {request.fold.merge_realization!r} has no realization in provider profile "
                f"{self.provider.name!r}. The "
                f"law is unchanged; this build cannot execute its composition (ToD v8 §4.1)")

        return Adequacy(True, "admitted",
                        f"seeded from {'R_F' if value.at_root else f'a non-root materialization at {value.anchor}'};"
                        f" the continuation to {request.target} was authorized before this request arrived")

    # ── serving a family ─────────────────────────────────────────────────────────────────────
    def measure(self, family: Any, anchor: Anchor, *, retain: bool = True,
                data_state: Optional[str] = None, on_behalf_of: str = "") -> Answer:
        """**Serve `F@A`: authorize, then fulfill.** The authority half's entry point.

        Two acts, in order, and the order is the architecture (B-0b):

            authorize   may this continuation be done?          ← `ContinuationAuthority`, reads the region
            fulfill     can it be done from what I hold?        ← the cache, reads no constitution

        An unauthorized target returns the AUTHORITY'S refusal verbatim rather than a cache miss, because the
        two mean different things and §7 forbids conflating them: *"MME MISS has no analytical meaning."* A
        target outside the continuation region is not a cold cache, and no amount of retention would change
        it — so it never becomes a miss at all; it never reaches the cache."""
        started_ns = time.perf_counter_ns()
        authorized = self.authorizer.authorize(
            family, anchor, data_state=data_state, retain=retain, on_behalf_of=on_behalf_of)
        if not authorized:
            # **THE REQUEST BOUNDARY STILL OBSERVES, EVEN THOUGH THE CACHE WAS NEVER ASKED** (M-2 §7 kept
            # true under B-0b). One `RequestObservation` per call on EVERY path, and this path is the new
            # one: an unauthorized continuation. Its disposition is `UNSUPPORTED`, which is exactly the row
            # a cache economist needs — *no amount of retention would ever serve this* — and it is emitted
            # here rather than in `fulfill` because `fulfill` never ran. Recording it as a cache MISS would
            # have been the error §7 forbids: a miss means the cache could not satisfy a LAWFUL request.
            subject = self.subject(family)
            observe_request(
                self.observations,
                FamilyRequest(manifold=self.manifold, build=self.build.reference,
                              family_id=subject.family_id, target=anchor, data_state=data_state,
                              on_behalf_of=on_behalf_of),
                started_ns=started_ns, route=REFUSED,
                refusal_code=authorized.refusal.code,
                disposition=disposition_for(authorized.refusal.code),
                fulfillment=Fulfillment(considered=0))
            return Answer(route=REFUSED, refusal=authorized.refusal)
        return self.fulfill(authorized.request)

    def fulfill(self, request: AuthorizedFamilyContinuation) -> Answer:
        """**Can this ALREADY-AUTHORIZED continuation be performed from held state?**

        Exact hit, else the cheapest admitted seed, else a MISS that carries no analytical meaning. Nothing
        in this method reads the constitution: no `region`, no `admits`, no law, no `cumulative_forgotten`.
        Every branch is a cache/materialization/execution question, and a `grep` over this method for the
        constitutional vocabulary is one of B-0b's proofs.

        **THE ROOT IS PREFERRED AND NON-ROOT SEEDS ARE PERMITTED.** A non-root materialization is a
        legitimate continuation origin *while its payload remains adequate*, and `adjudicate` is where
        "remains adequate" is decided.

        **THIS IS THE REQUEST BOUNDARY, AND IT IS WHERE OBSERVATION HAPPENS** (ruled M-2 §7). Exactly one
        `RequestObservation` per call, on every path — hit, derivation and miss — because *"a cache policy
        cannot learn from hits alone."* Observation is emitted AFTER the answer is determined and never gates
        it."""
        if not self.authorizer.issued(request):                      # J-0, as in `adjudicate`
            raise KernelRefusal(
                "foreign-credential", f"{request.family_id}@{request.target}",
                f"this continuation was authorized by another build, not by {self.authorizer.name}. "
                f"Serving it here would fulfil one jurisdiction's permission out of another's cache.")
        started_ns = time.perf_counter_ns()
        anchor = request.target
        observed = FamilyRequest(manifold=self.manifold, build=request.build,
                                 family_id=request.family_id, target=anchor,
                                 data_state=request.data_state, on_behalf_of=request.on_behalf_of)
        considered: list[str] = []

        # ── CANDIDATE SELECTION IS THE MME'S, NEVER THE CALLER'S (ruled 2026-09-29 §2) ──────────────
        # The request asked for an analytical identity; which retained instance answers it is a cache
        # decision, made here by cost. Only CURRENT, payload-bearing materializations are candidates: a
        # superseded one may stay resident for as long as policy likes and will never answer.
        pool = self.materializations.candidates_for(request.family_id, anchor, request.instance,
                                                   data_state=request.data_state)
        exact = next((m for m in pool if m.anchor == anchor), None)
        if exact is not None:
            observe_request(self.observations, observed, started_ns=started_ns, route=CACHED,
                            disposition=READY,
                            fulfillment=Fulfillment(directly_held=True, selected=(exact.id,),
                                                    considered=1))
            return Answer(route=CACHED, value=exact.value, disclosures=exact.value.disclosures,
                          considered=(str(self._descriptor(exact)),))

        # **LEAST WORK FIRST, FALLING BACK TOWARD THE ROOT** — a governed choice, not an optimization.
        # Candidates are ordered COARSEST FIRST among those still finer than the target, which is the fewest
        # cells to fold. The fallback direction is safe because a FINER seed has forgotten LESS, so it is
        # never less permissive: trying the cheapest first cannot turn a servable ask into a refusal.
        blockers: list[Adequacy] = []
        for materialization in pool:
            descriptor = self._descriptor(materialization)
            considered.append(str(descriptor))
            candidate = Retained(key=descriptor, value=materialization.value)
            verdict = self.adjudicate(candidate, request)
            if not verdict:
                blockers.append(verdict)
                continue
            state = candidate.value
            if state.anchor != anchor:
                # **THE FOLD IS KEYED BY THE REQUEST'S EXECUTION REQUIREMENT**, not by a law this method
                # looked up. `merge_realization` is the in-memory profile's key; a columnar engine keys the
                # same authorized fold by `composition` instead, which is why the request carries both.
                merge = self.provider.capability(request.fold.merge_realization, "merge")
                state = state.fold_onto(anchor, merge)
            # **CONDITIONS ARE PROPAGATED, NEVER DERIVED** (B-0b). The `approximate` standing used to be
            # authored here by reading `law.approximation` — a cache asserting an analytical fact about a
            # law. It now arrives on the request, decided by the authority, and this loop only carries it.
            for condition in request.conditions:
                state = state.with_disclosure(condition)
            admitted: tuple[MaterializationId, ...] = ()
            if request.retain:
                # **THE DEPENDENCY EDGE IS RECORDED HERE AND NOWHERE ELSE.** A continuation names what it
                # was continued FROM, which is the relation supersession propagates along — a different fact
                # from the entitlement, which the authority settled before this request existed. The
                # retention uses the standing the authorization already paired with this target, so the
                # cache does not go back to the constitution to keep what it just computed.
                admission = self.put(state, request.standing, establishment=(
                    Establishment(CONTINUED_FROM, (materialization.id,))
                    if state.anchor != materialization.anchor else Establishment(AT_ROOT)))
                if admission:
                    admitted = (admission.id,)
            route = ROOT if state.anchor == self._families[request.family_id].root else CONTINUED
            observe_request(self.observations, observed, started_ns=started_ns, route=route,
                            disposition=READY,
                            fulfillment=Fulfillment(
                                directly_held=False, selected=(materialization.id,),
                                seeded_from=materialization.anchor,
                                folded=len(getattr(candidate.value, "cells", ()) or ()) or None,
                                considered=len(considered), admitted=admitted))
            return Answer(route=route, value=state, disclosures=state.disclosures,
                          seeded_from=descriptor, considered=tuple(considered))

        # **THE MISS, AND IT CARRIES NO ANALYTICAL MEANING** (ruled §7). It means exactly one thing: the
        # cache cannot currently satisfy this already-lawful request from the state it holds. It does not
        # mean the target is unlawful — an unlawful target has no request and never arrives here — nor that
        # the family does not exist, nor that a backend cannot supply it. The governed fulfillment layer
        # interprets the miss and decides what happens next.
        #
        # The blockers are deduped and the uninformative ones demoted, because a refusal that recites the
        # same reason once per candidate is a refusal nobody finishes reading. `not-reachable` is geometry
        # and says nothing about the ask unless it is the only thing to say, so it sorts last.
        best: dict[str, Adequacy] = {}
        for b in blockers:
            kept = best.get(b.code)
            if kept is None or len(b.detail) > len(kept.detail):
                best[b.code] = b
        ordered = sorted(best.values(), key=lambda b: b.code == "not-reachable")
        family = self._families[request.family_id]
        detail = (" · ".join(f"{b.code} — {b.detail}" for b in ordered)
                  or f"no retained state of {request.family_id} exists under this analytical instance, "
                     f"and this engine does not invent one: a value must be established at "
                     f"{family.root} before it can be continued anywhere") + self._also_held(family)
        # The disposition is derived from the BLOCKING code: a request blocked by `unrealized-law` is
        # UNSUPPORTED — no amount of retention would ever serve it — while one blocked by an empty pool is
        # NEED, the row that says "retaining this would have helped". Collapsing them is how a cache policy
        # learns to cache its way out of a limit.
        blocking = ordered[0].code if ordered else ""
        observe_request(self.observations, observed, started_ns=started_ns, route=REFUSED,
                        refusal_code=blocking or "unanswerable",
                        disposition=(disposition_for(blocking) if blocking else NEED),
                        fulfillment=Fulfillment(considered=len(considered)))
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

    # ── stating what is needed — the MME's half of the realization seam (R-1 §2) ──────────────
    def requirement_for(self, family: Any, target: Anchor, *,
                        data_state: Optional[str] = None, note: str = "") -> RequirementOutcome:
        """**What governed family state would satisfy a request for `F@target`?** Delegated to the authority.

        Its body moved to `ContinuationAuthority.requirement_for` in B-0b, because every one of its three
        refusals is constitutional or build-capability reasoning and none of them is a cache question — and
        because leaving it here would have left the cache engine reading `region` after everything else
        stopped. The name stays on this class for the same reason `measure` does: this class is still the
        authority as well as the cache, and both go with the authority half when it is split.

        **IT IS NOT AN AUTHORIZED REQUEST AND IS NOT BECOMING ONE** (ruled §7). An authorization says *"this
        is lawful, attempt it from held state"*; a requirement says *"held state was not enough, and here is
        what governed state would be"*. The second follows from attempting the first."""
        return self.authorizer.requirement_for(family, target, data_state=data_state, note=note)

    # ── serving an expression — NOT HERE ANY MORE ────────────────────────────────────────────
    #
    # `evaluate` and `_establish` lived here through M-1 and moved OUT in M-2, to
    # `kernel.expression.ExpressionEvaluator`. Ruled §1: *"Expressions remain fully supported by Platform
    # serving, but they consume family state supplied by MME and are evaluated above it."*
    #
    # **No delegating shim is left behind**, deliberately. An `MME.evaluate` that forwarded to the
    # evaluator would keep every call site compiling and would keep the boundary imaginary — consumers
    # would go on treating the MME as the thing that serves expressions, and the next unit would find the
    # same coupling wearing a different name. Callers construct the evaluator over the engine:
    #
    #     evaluator = ExpressionEvaluator(mme)
    #     answer    = evaluator.evaluate(mme.expression("average_order_value"), month)
    #
    # What the MME keeps for expressions is CONSTITUTION and nothing else: `register_expression`,
    # `expression()`, `expressions`, `sort_of`, `witness_of`, `law_of`, `instance_of`. Those are the
    # Manifold build's authority over what an expression MEANS, which M-2 explicitly does not move
    # (§2: *"Do not remove expression semantics from the kernel"*). What moved is where it RUNS.

    # ── invalidation — CONSERVATIVE, and that is the ruling ──────────────────────────────────
    def invalidate(self, identity: str) -> tuple[RetentionKey, ...]:
        """Drop every retained object of `identity`. **Rebuild is from the root.**

        No delta retraction and no deletion maintenance, deliberately: a mergeable family is not thereby
        a *retractable* one, and ToD v8 §3.1 says so in its own words — value closure *"does not imply
        recoverability of prior contributions or sufficiency for restriction, deletion, correction, or a
        changed analytical law."* Implementing retraction because the algebra looks like a group would be
        granting a capability the theory withholds."""
        materialized = self.materializations.select(identity, eligibility=None)
        for m in materialized:
            self.materializations.unpin(m.id)                 # invalidation is deliberate; pinning is not a veto
            self.materializations.drop(m.id)
        return tuple(self._descriptor(m) for m in materialized)


__all__ = ["MME", "Adequacy", "Retained", "RetentionKey"]
