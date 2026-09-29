"""
columna_platform.kernel.sorts — **the two durable analytical sorts, and their identities.**

ToD v8 §3.5 recognizes two, and §8.5 gives Manifold *"two distinct reusable analytical classes"*:

    MeasureFamily        F@A   its values CONTINUE under refinement, from its own law
    GovernedExpression   E@A   its values are RE-EVALUATED from a sufficient basis, at each location

**NEITHER IS A VARIANT OF THE OTHER AND NEITHER IS REACHABLE THROUGH THE OTHER.** They are two types
with two identity types, and the kernel never holds one in a variable typed for the other. §3.7 forbids
closing the gap by promotion: *naming, caching, repetition or durable governance does not make a result
continuation-bearing.*

WHERE THE §9.2 CONTAINMENT LIVES NOW
------------------------------------
In Core it had to be a gate that fired after resolution, over an object already constituted as a family
(V8-0's C4 clause 2). **Here it is a constitution-time impossibility.** `MeasureFamily.__post_init__`
refuses a law whose `continuation is None`, so *"do not create a Mean family"* is not a rule anyone has
to remember — `MeasureFamily(law="MEAN")` does not exist as a reachable state. That is the difference
between migrating a semantic and building on one.

WHAT A FAMILY HAS THAT AN EXPRESSION DOES NOT, AND VICE VERSA
--------------------------------------------------------------
A family has a **root** `R_F` — §3.2's origin of continuation — a continuation law, and a continuation
region. An expression has **constitutive inner anchors** (§3.6), role-indexed governed operands, and
**admitted bases**. There is no field on either that could hold the other's fact, which is the point:
the absence is structural, not a convention.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Optional

from .geometry import Anchor, Edge, KernelRefusal, Universe
from .law import SAME_AS_OPERAND, AnalyticalLaw, LawRegistry
from .standing import AnalyticalInstance


# ══ identities ════════════════════════════════════════════════════════════════════════════════════
@dataclass(frozen=True)
class FamilyPoint:
    """**`F@A` — a family analytical identity.** The family, and where it is being asked for.

    Two fields and no more. Not a cache key: storage and realization standing are not identity, and a
    retained object is located by a `RetentionKey` which carries this plus what makes a retained thing
    distinguishable (see `mme.py`). Keeping them apart is why an expression result and a family value at
    the same anchor cannot collide in one store."""

    family_id: str
    anchor: Anchor

    def __str__(self) -> str:
        return f"{self.family_id}@{self.anchor}"

    @property
    def sort(self) -> str:
        return "family"


@dataclass(frozen=True)
class ExpressionPoint:
    """**`E@A` — an expression analytical identity.** A PEER of `FamilyPoint`, not a widening of it.

    A single widened identity type carrying a `sort` discriminator would mean every consumer asks what
    came back after the call, forever — and the one that forgets is the one that serves an expression as
    a family. Two types ask the question before the call instead of after."""

    expression_id: str
    anchor: Anchor

    def __str__(self) -> str:
        return f"{self.expression_id}@{self.anchor}"

    @property
    def sort(self) -> str:
        return "expression"


# ══ sort 1 · the measure family ═══════════════════════════════════════════════════════════════════
@dataclass(frozen=True)
class MeasureFamily:
    """**A continuation-bearing durable analytical object.**

    `root` is `R_F`, §3.2's **family-relative** origin of continuation — relative because two families
    in one world may be constituted at different locations, and neither one's root is the world's."""

    family_id: str
    universe: str
    #: `R_F`. The canonical continuation origin, and the only location contributions land at.
    root: Anchor
    #: **THE FAMILY'S CONTINUATION LAW, AND THAT IS WHAT IT STAYS** (ruled Huayin, 2026-09-28): *"If
    #: `MeasureFamily.law` in the new kernel means continuation law, keep it that way. Do not let it
    #: become a substitute for `root_evaluator` or a generic formation-law identity."*
    #:
    #: It is validated as continuation-bearing (`bind`), so what this field names is the law by which this
    #: family's values COMPOSE. **ROOT FORMATION IS A SEPARATE RESPONSIBILITY** — §3.2's origin is a
    #: location, and what happens AT it is a different act from what composes away from it.
    #:
    #: Today `establish_root` reaches the same law's `Realization.contribute` to fold occurrences into a
    #: root value. **That is a REALIZATION convenience and not a semantic identity**, and it is written
    #: down here so it cannot quietly become one: nothing in this kernel treats this field as the
    #: formation identity of the value, no basis role is checked against it, and when the Operator
    #: Registry work gives root evaluation its own reusable signature, a `root_evaluator` attaches
    #: BESIDE this field rather than replacing its meaning.
    law: str
    value_domain: str
    participation: str
    target: str
    #: A governed order, where the law requires one to select at all (LAST/FIRST).
    order_by: Optional[str] = None
    parameters: Mapping[str, object] = field(default_factory=dict)
    #: An opaque witness of the constitution this family was established under.
    constitution: str = "c0"

    def bind(self, registry: LawRegistry) -> AnalyticalLaw:
        """Resolve and VALIDATE this family's law. Called at registration, so an unlawful family cannot
        be reached by a serving path that has already assumed it is lawful."""
        law = registry.get(self.law)
        if not law.may_found_a_family:
            raise KernelRefusal(
                "not-a-family-law", self.family_id,
                f"law {law.name!r} carries no continuation, so it cannot found a MEASURE FAMILY (ToD "
                f"v8 §9.2 keeps measure family to the continuation-bearing case). {law.identity_note or ''} "
                f"An object whose value must be reconstructed from a basis over other families is a "
                f"GOVERNED EXPRESSION — build one of those. Naming, caching, repetition or durable "
                f"governance does not make this value continuation-bearing (§3.7).".strip())
        if law.requires_order and not self.order_by:
            raise KernelRefusal(
                "order-not-governed", self.family_id,
                f"law {law.name!r} selects by a governed order and this family declares none. Without "
                f"an order the law does not select a witness — it picks one, which is a different and "
                f"ungoverned act.")
        if not law.requires_order and self.order_by:
            raise KernelRefusal(
                "gratuitous-order", self.family_id,
                f"declares order_by={self.order_by!r} while law {law.name!r} does not select by order.")
        missing = sorted(p for p in law.required_parameters if p not in self.parameters)
        if missing:
            raise KernelRefusal(
                "unsupplied-parameter", self.family_id,
                f"law {law.name!r} requires identity-bearing parameters {missing}, which this family "
                f"does not supply. No default is invented: a parameter that individuates a law's use "
                f"cannot be guessed.")
        if self.root.universe != self.universe:
            raise KernelRefusal("root-in-another-world", self.family_id,
                                f"root {self.root} is not relative to {self.universe!r}")
        # **`value_domain` IS THE DOMAIN OF THE FAMILY'S OWN VALUE**, which is not the domain of the
        # occurrences its law consumes at the root. HLL_SKETCH admits `text` operands and yields a
        # `sketch`: the family IS the sketch. A `same_as_operand` law's family may declare any domain the
        # law admits as an operand, because for those the two coincide by definition.
        #
        # This check exists because the first exhibit written against this kernel declared the sketch
        # family's domain as `text` — the operand's domain — and an expression constructor over it then
        # looked ill-typed for the wrong reason. Catching it at constitution says which fact was confused.
        if law.result_domain == SAME_AS_OPERAND:
            if not law.admits_operand(self.value_domain):
                raise KernelRefusal(
                    "value-domain-not-admitted", self.family_id,
                    f"declares value_domain {self.value_domain!r} while law {law.name!r} admits "
                    f"{sorted(law.operand_domains)} and yields its operand's own domain.")
        elif self.value_domain != law.result_domain:
            raise KernelRefusal(
                "value-domain-mismatch", self.family_id,
                f"declares value_domain {self.value_domain!r} while law {law.name!r} yields "
                f"{law.result_domain!r}. A family's value domain is the domain of ITS OWN VALUE — what "
                f"it retains and what an expression's constructor sees — not the domain of the "
                f"occurrences the law consumes at the root.")
        return law

    def instance(self, scope: Optional[str] = None) -> AnalyticalInstance:
        return AnalyticalInstance(universe=self.universe, participation=self.participation,
                                  constitution=self.constitution, scope=scope)

    def at(self, anchor: Anchor) -> FamilyPoint:
        return FamilyPoint(self.family_id, anchor)

    @property
    def root_point(self) -> FamilyPoint:
        """**`F@R_F`** — the canonical continuation origin, named rather than reconstructed."""
        return FamilyPoint(self.family_id, self.root)

    def edge_from_root(self, anchor: Anchor) -> Edge:
        return self.root.edge_to(anchor)


# ══ sort 2 · the governed expression ══════════════════════════════════════════════════════════════
@dataclass(frozen=True)
class Operand:
    """One **role-indexed** governed operand. The role is the point: a position survives a reordering
    of a serialization and a role does not, which is why a role can be identity-bearing."""

    role: str
    family_id: str


@dataclass(frozen=True)
class SufficientBasis:
    """**One admitted establishment route — and an expression may admit zero, one, or several.**

    Ruled (Huayin, 2026-09-28): *"expression identity ≠ one particular sufficient basis used to
    establish it."* So this is a member of a TUPLE on the expression, never a singular `declared_basis`
    field. Zero is a legible state: an expression may be constituted before any route is admitted, in
    which case it is well-formed and not evaluable — two questions, deliberately separate."""

    basis_id: str
    #: role (a component LAW name) → the governed family whose state supplies it
    components: Mapping[str, str]
    requires_common_participation: bool

    @property
    def component_laws(self) -> tuple[str, ...]:
        return tuple(sorted(self.components))


@dataclass(frozen=True)
class GovernedExpression:
    """**An object whose value is determined by a sufficient basis over other governed families.**

    No root, no continuation, no continuation region, no movement, and no empty-fibre family law — there
    is nowhere on this record to put one. Its empty behaviour comes from its CONSTRUCTOR OVER ITS BASIS:
    ToD v8 §4.3 states it for the case at hand, where the SUM/COUNT basis is established as `(0, 0)` and
    *"the expression is undefined on that basis"* at `n = 0`."""

    expression_id: str
    universe: str
    constructor: str
    operands: tuple[Operand, ...]
    participation: str
    #: The CONSTITUTIVE INNER anchors (§3.6). **Not a root.** Plural, because reducing several to one
    #: would be inventing the root this sort does not have.
    inner_anchors: tuple[Anchor, ...] = ()
    scope: Optional[str] = None
    admitted_bases: tuple[SufficientBasis, ...] = ()
    parameters: Mapping[str, object] = field(default_factory=dict)
    constitution: str = "c0"

    def bind(self, registry: LawRegistry, families: Mapping[str, MeasureFamily]) -> AnalyticalLaw:
        law = registry.get(self.constructor)
        if law.may_found_a_family:
            raise KernelRefusal(
                "not-a-constructor", self.expression_id,
                f"law {law.name!r} carries a continuation, so it founds a MEASURE FAMILY rather than "
                f"constructing an expression. Building an expression over it would take an object whose "
                f"values compose and declare that they do not.")
        roles = [o.role for o in self.operands]
        if len(set(roles)) != len(roles):
            raise KernelRefusal("duplicate-role", self.expression_id,
                                "an operand role is filled twice; a role is an INDEX, not a label.")
        for o in self.operands:
            fam = families.get(o.family_id)
            if fam is None:
                raise KernelRefusal(
                    "dangling-operand", self.expression_id,
                    f"operand role {o.role!r} names family {o.family_id!r}, which is not registered.")
            if not law.admits_operand(fam.value_domain):
                raise KernelRefusal(
                    "operand-domain", self.expression_id,
                    f"constructor {law.name} admits {sorted(law.operand_domains)} and role {o.role!r} "
                    f"is filled by a family whose governed value domain is {fam.value_domain!r}. An "
                    f"operand outside the law's domains is not under-specified; it is one the law does "
                    f"not define.")
        required = law.required_basis
        seen: set[str] = set()
        shapes: dict[tuple, str] = {}
        for basis in self.admitted_bases:
            if basis.basis_id in seen:
                raise KernelRefusal("duplicate-basis", self.expression_id,
                                    f"basis {basis.basis_id!r} is declared twice.")
            seen.add(basis.basis_id)
            if required is None:
                raise KernelRefusal(
                    "basis-without-requirement", self.expression_id,
                    f"admits basis {basis.basis_id!r} while constructor {law.name} states no required "
                    f"basis. There is nothing in the law to check the components against, and accepting "
                    f"them would license any role set whatsoever.")
            if basis.component_laws != tuple(sorted(required.components)):
                raise KernelRefusal(
                    "basis-coverage", self.expression_id,
                    f"basis {basis.basis_id!r} fills {list(basis.component_laws)} and {law.name} "
                    f"requires exactly {sorted(required.components)} ({required.note}). A basis that "
                    f"does not cover the required components determines nothing; one that covers more "
                    f"is not the route the law named.")
            if basis.requires_common_participation != required.requires_common_participation:
                raise KernelRefusal(
                    "basis-participation-requirement", self.expression_id,
                    f"basis {basis.basis_id!r} declares requires_common_participation="
                    f"{basis.requires_common_participation} while {law.name} requires "
                    f"{required.requires_common_participation}. The law's requirement is not a default "
                    f"a declaration may relax.")
            for role, fid in basis.components.items():
                if fid not in families:
                    raise KernelRefusal("dangling-basis-component", self.expression_id,
                                        f"basis {basis.basis_id!r} role {role!r} names unregistered "
                                        f"family {fid!r}.")
            shape = tuple(sorted(basis.components.items()))
            if shape in shapes:
                raise KernelRefusal(
                    "duplicate-route", self.expression_id,
                    f"basis {basis.basis_id!r} admits the same role-to-family assignment as "
                    f"{shapes[shape]!r}. Two ids over one route are not two alternatives; they are one "
                    f"route counted twice, and the agreement obligation between alternatives would be "
                    f"trivially satisfied by the duplicate.")
            shapes[shape] = basis.basis_id
        return law

    def instance(self) -> AnalyticalInstance:
        return AnalyticalInstance(universe=self.universe, participation=self.participation,
                                  constitution=self.constitution, scope=self.scope)

    def at(self, anchor: Anchor) -> ExpressionPoint:
        return ExpressionPoint(self.expression_id, anchor)

    def basis(self, basis_id: str) -> Optional[SufficientBasis]:
        for b in self.admitted_bases:
            if b.basis_id == basis_id:
                return b
        return None


def universe_of(u: Universe) -> str:                            # readability in exhibits
    return u.name


__all__ = ["ExpressionPoint", "FamilyPoint", "GovernedExpression", "MeasureFamily", "Operand",
           "SufficientBasis", "universe_of"]
