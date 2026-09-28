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

from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Optional

from .geometry import Anchor, Universe
from .law import AnalyticalLaw, LawRegistry, STRUCTURED
from .realization import ProviderProfile
from .sorts import (
    GovernedExpression,
    MeasureFamily,
    SufficientBasis,
)
from .standing import (
    CACHED,
    CONTINUED,
    Disclosure,
    EVALUATED,
    REFUSED,
    ROOT,
    Refusal,
)
from .value import Answer, ExpressionOutput, FamilyState


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
      `instance`        the analytical instance — participation and scope where identity-bearing, plus a
                        witness of the constitution, so a state from a superseded constitution is a
                        DIFFERENT retained object rather than a silent overwrite;
      `provider`        realization standing: a value produced by an approximate provider is not
                        interchangeable with one produced by an exact one.

    Not here: a physical grain, a storage location, a partition, a file. Those are storage facts, and
    ToD v8 keeps storage out of identity."""

    sort: str
    identity: str
    anchor: Anchor
    instance: Any
    provider: str

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

    def __init__(self, universe: Universe, laws: LawRegistry, provider: ProviderProfile) -> None:
        self.universe, self.laws, self.provider = universe, laws, provider
        self._families: dict[str, MeasureFamily] = {}
        self._expressions: dict[str, GovernedExpression] = {}
        self._bound: dict[str, AnalyticalLaw] = {}
        self._store: dict[RetentionKey, Retained] = {}

    # ── constitution ─────────────────────────────────────────────────────────────────────────
    def register_family(self, family: MeasureFamily) -> MeasureFamily:
        """**Where ToD v8 §9.2 is enforced, by refusing to construct rather than by gating later.**
        `MeasureFamily.bind` raises for a law with no continuation, so a Mean family is not a reachable
        state of this engine."""
        self._bound[family.family_id] = family.bind(self.laws)
        self._families[family.family_id] = family
        return family

    def register_expression(self, expression: GovernedExpression) -> GovernedExpression:
        self._bound[expression.expression_id] = expression.bind(self.laws, self._families)
        self._expressions[expression.expression_id] = expression
        return expression

    def family(self, family_id: str) -> MeasureFamily:
        return self._families[family_id]

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
                       value_key: str = "value") -> Answer:
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
                            cells=cells, instance=family.instance(), forgotten_since_root=frozenset())
        self.retain(state)
        return Answer(route=ROOT, value=state)

    # ── retention ────────────────────────────────────────────────────────────────────────────
    def retain(self, value: Any) -> Retained:
        """Hold an object. **Holding is not authority** — every right it might confer is adjudicated at
        use, so this method asks nothing and refuses nothing."""
        sort = value.point.sort
        identity = getattr(value.point, "family_id", None) or value.point.expression_id
        key = RetentionKey(sort=sort, identity=identity, anchor=value.anchor,
                           instance=value.instance, provider=self.provider.name)
        retained = Retained(key=key, value=value)
        self._store[key] = retained
        return retained

    def retained(self, point: Any, instance: Any) -> Optional[Retained]:
        sort = point.sort
        identity = getattr(point, "family_id", None) or getattr(point, "expression_id", None)
        return self._store.get(RetentionKey(sort, identity, point.anchor, instance,
                                            self.provider.name))

    def candidates(self, family: MeasureFamily) -> tuple[Retained, ...]:
        """Every retained object that *might* seed this family, **including the ones that may not.**
        Separating candidacy from permission is the whole shape of this module: a test can hold a
        candidate in one hand and its refusal in the other."""
        return tuple(r for r in self._store.values() if r.key.identity == family.family_id)

    @property
    def held(self) -> tuple[RetentionKey, ...]:
        return tuple(self._store)

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

        # 3 · CLOSURE OVER THE WHOLE ROUTE FROM THE ROOT — the laundering guard.
        edge = value.anchor.edge_to(target)
        forgotten_total = value.forgotten_since_root | edge.forgotten
        if not law.region.admits(forgotten_total):
            through = (f" It got to {value.anchor} by forgetting "
                       f"{sorted(value.forgotten_since_root)}, and that route is part of the question: "
                       f"a two-step coarsening forgets the union, so an intermediate materialization "
                       f"cannot launder an edge the law does not admit."
                       if value.forgotten_since_root else "")
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
    def measure(self, family: MeasureFamily, anchor: Anchor, *, retain: bool = True) -> Answer:
        """**Serve `F@A`.** Exact hit, else the best admitted seed, else a refusal that names why.

        **THE ROOT IS PREFERRED AND NON-ROOT SEEDS ARE PERMITTED**, which is the required distinction. A
        non-root materialization is a legitimate continuation origin *while its value remains adequate*,
        and `adjudicate` is where "remains adequate" is decided — not here, and not by preferring the
        root so hard that the non-root case is never exercised."""
        law = self._bound[family.family_id]
        instance = family.instance()
        considered: list[str] = []

        exact = self.retained(family.at(anchor), instance)
        if exact is not None and exact.continuation_bearing:
            return Answer(route=CACHED, value=exact.value, disclosures=exact.value.disclosures,
                          considered=(str(exact.key),))

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
        pool = sorted((r for r in self.candidates(family) if r.key.instance == instance),
                      key=lambda r: len(r.key.anchor.constituents))
        blockers: list[Adequacy] = []
        for candidate in pool:
            considered.append(str(candidate.key))
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
                self.retain(state)
            route = ROOT if state.anchor == family.root else CONTINUED
            return Answer(route=route, value=state, disclosures=state.disclosures,
                          seeded_from=candidate.key, considered=tuple(considered))

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
                     f"{family.root} before it can be continued anywhere")
        return Answer(route=REFUSED, considered=tuple(considered),
                      refusal=Refusal("unanswerable", str(family.at(anchor)), detail))

    # ── serving an expression ────────────────────────────────────────────────────────────────
    def evaluate(self, expression: GovernedExpression, anchor: Anchor, *,
                 basis_id: Optional[str] = None, retain: bool = True) -> Answer:
        """**Evaluate `E@A` from a sufficient basis.** Never from a continuation, because there is none.

        Where more than one basis is admitted they are tried in declaration order and the FIRST that
        establishes wins; the refusal, if none does, reports every route it tried and why each failed.
        That is what makes "refuse an incompatible basis even when both operands individually exist" a
        legible answer rather than a bare `no`."""
        law = self._bound[expression.expression_id]
        instance = expression.instance()
        considered: list[str] = []

        exact = self.retained(expression.at(anchor), instance)
        if exact is not None and not exact.continuation_bearing:
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
            attempt = self._establish(expression, law, basis, anchor)
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
                   basis: SufficientBasis, anchor: Anchor) -> Answer:
        """One route, tried. Returns the `ExpressionOutput` or the refusal that stopped it."""
        subject = f"{expression.expression_id}@{anchor} via {basis.basis_id}"
        states: dict[str, FamilyState] = {}
        for role in basis.component_laws:
            component = self._families[basis.components[role]]
            served = self.measure(component, anchor)
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

        output = ExpressionOutput(point=expression.at(anchor), constructor=law.name, cells=cells,
                                 instance=expression.instance(), basis_id=basis.basis_id)
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
        return dropped


__all__ = ["MME", "Adequacy", "Retained", "RetentionKey"]
