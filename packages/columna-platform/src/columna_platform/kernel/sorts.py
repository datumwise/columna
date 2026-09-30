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
from .standing import UNSTATED_DATA_STATE, AnalyticalInstance
from .witness import (
    ConstitutionWitness,
    expression_witness,
    family_witness,
    refuse_a_declared_constitution,
)


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


# ══ root formation · WHAT THE ROOT FAMILY VALUE IS CONSTITUTED FROM ═══════════════════════════════
#
#     **Root formation says what the root family value is constituted from. Evidence provenance says how
#     that root establishment is supported. Physical realization says how the governed formation is
#     executed. Continuation says how an already-established family value moves. Keep all four
#     separate.**  — Huayin, 2026-09-30 (B-4a, the governing distinction)
#
# **THIS VOCABULARY IS FAMILY CONSTITUTION AND IT IS NOT IN `law.py`, WHICH IS THE POINT.** Every other
# governed vocabulary in this kernel — `VALUE_FORMS`, `DOMAINS`, `FOLD_SHAPES` — lives beside
# `AnalyticalLaw` because the law asserts it. Formation is asserted by the FAMILY. Putting these two
# tokens next to `FOLD_SHAPES` would have quietly suggested that a law implies a formation, and the three
# inference rules this unit exists to forbid are exactly:
#
#     COUNT      → POPULATION                    (B-0b removed this one from the cache engine)
#     COUNT      → PARTICIPATION_CARDINALITY     (would be the same defect at a third address)
#     POPULATION → PARTICIPATION_CARDINALITY     (the subtlest: a continuation fact implying a
#                                                 formation fact, which is two questions collapsed)
#
# So the constant lives with the record that states it, and a reader looking for "what does COUNT imply"
# finds nothing to read.
#
# **WHY NOT `root_evaluator`.** The slot was reserved under that name in `law`'s docstring below and in
# `witness.py`. Ruled against (B-4a): *"`root_evaluator` carries historical implementation baggage and
# risks conflating governed formation with physical evaluation again."* An evaluator is a thing that RUNS;
# what is declared here is what the value IS. `formation` names the act, not the machinery.

#: **The root family value is independently established as a value of this family**; this formation law
#: does not derive that value from participation.
#:
#: **`DIRECT` DOES NOT MEAN OBSERVED** (ruled explicitly). A `DIRECT` root may be observed, reported,
#: assigned, supplied by an authoritative source, or physically computed under a realization contract —
#: none of which changes the formation law, because all of them are answers to a DIFFERENT question.
#: Evidence provenance is not root formation, and the reason this matters here is that the first draft of
#: this unit proposed `OBSERVED` as the token and had to be corrected: it named the provenance and left
#: the formation unstated.
DIRECT = "direct"

#: **At a root location, the family value is the cardinality of the governed participating domain
#: constituted there:** `F@R_F(r) = |D_R_F(r)|`.
#:
#: **THE LAW IS CARDINALITY AND THE LITERAL `1` IS NOT PART OF IT** (ruled explicitly: do not name this
#: `UNIT_PER_PARTICIPANT`, do not encode `1` as the formation law). At an individuating root such as
#: `{store, day, order}` each participating point contains exactly one Order, so the value there IS 1 —
#: but that is a consequence of the root meeting this law, not the law itself. A family rooted at
#: `{store, day}` may legitimately have `|D(r)| = 7`: seven distinct governed Order points at one root
#: location, under this same unchanged declaration.
#:
#: **THAT IS NOT "GEOMETRY REPRESENTING MULTIPLICITY", WHICH IT DOES NOT DO** (ruled, 2026-09-30). Keep
#: these two apart:
#:
#:     duplicate physical representations of ONE governed point   ≠   multiple governed participating points
#:
#: The first is a realization/fidelity problem — two rows claiming one Order are not two Orders. The
#: second is seven Orders, which is a fact about the domain and not about the carrier. Nothing currently
#: declares whether a root individuates its domain, which is why `RealizationAuthority` can verify this
#: formation only at a root that does.
PARTICIPATION_CARDINALITY = "participation-cardinality"

#: **NOT A CLOSED ONTOLOGY** (ruled §8). These are the only two formation laws the families now in hand
#: require. Structured sufficient-state roots — HLL sketches formed over a governed domain, moment state,
#: ordered witnesses — will need their own formation laws, and adding one must not change what this field
#: MEANS. That is why the field carries a token from an open set rather than a boolean or an enum of
#: "value vs count": a third token is an addition, not a redefinition.
FORMATION_LAWS: frozenset[str] = frozenset({DIRECT, PARTICIPATION_CARDINALITY})


# ══ sort 1 · the measure family ═══════════════════════════════════════════════════════════════════
@dataclass(frozen=True)
class MeasureFamily:
    """**A continuation-bearing durable analytical object.**

    `root` is `R_F`, §3.2's **family-relative** origin of continuation — relative because two families
    in one world may be constituted at different locations, and neither one's root is the world's."""

    family_id: str
    #: **The Manifold that owns this family.** Logical ownership, not a deployment fact: many Manifolds
    #: may share one process, runtime, store and provider, and none of that shares authority.
    manifold: str
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
    #: formation identity of the value, and no basis role is checked against it.
    #:
    #: **THE RESERVED SLOT IS NOW FILLED, AND NOT UNDER THE RESERVED NAME.** This note used to end *"a
    #: `root_evaluator` attaches BESIDE this field rather than replacing its meaning"*. It does attach
    #: beside — it is `formation`, below — and the name changed by ruling (B-4a): an evaluator is a thing
    #: that runs, and what is declared is what the value IS.
    law: str
    value_domain: str
    participation: str
    target: str
    #: **WHAT THIS FAMILY'S ROOT VALUE IS CONSTITUTED FROM.** One of `FORMATION_LAWS`; see the vocabulary
    #: above for the governing distinction and for why it does not live in `law.py`.
    #:
    #: **NO SILENT DEFAULT** (ruled §9). The `""` is not a default value, it is the absence that
    #: `__post_init__` refuses: formation is identity-bearing family constitution, and a family whose root
    #: formation went unstated would be a family whose witness agreed with itself across a change of
    #: meaning. It is spelled as an empty default rather than as a required positional field so that the
    #: failure is a GOVERNED REFUSAL naming the ruling, rather than a `TypeError` naming a keyword.
    #:
    #: It is a determinant of the `ConstitutionWitness` **by derivation and with no edit to
    #: `witness.py`**: `FAMILY_NON_DETERMINANTS` is an exclusion list and this field is not in it. So a
    #: family that changed formation changes identity, which is correct — a count formed from cardinality
    #: and a count supplied directly are not the same constitution even at the same root.
    formation: str = ""
    #: A governed order, where the law requires one to select at all (LAST/FIRST).
    order_by: Optional[str] = None
    parameters: Mapping[str, object] = field(default_factory=dict)
    #: **RETIRED, AND KEPT ONLY SO THAT SUPPLYING ONE IS REFUSED** (P-1, 2026-09-29). The constitution
    #: witness is COMPUTED from this record's identity-bearing fields by `witness()`; it was previously a
    #: caller-supplied token defaulting to `"c0"`, which agreed with itself no matter how far the
    #: declaration moved — the exact failure a staleness check exists to catch.
    constitution: Optional[str] = None

    def __post_init__(self) -> None:
        refuse_a_declared_constitution(self, self.family_id)
        if not self.formation:
            raise KernelRefusal(
                "no-root-formation-declared", self.family_id,
                f"{self.family_id!r} declares a continuation law ({self.law!r}) and a root ({self.root}) "
                f"and does not say what its root value is CONSTITUTED FROM. Those are different questions "
                f"and neither answers the other: `law` is how an established value moves, `formation` is "
                f"what the value at `R_F` is. **THERE IS NO DEFAULT** — formation is identity-bearing "
                f"constitution, so assuming {DIRECT!r} would make this family's witness agree with itself "
                f"across a change of meaning. Declare one of {sorted(FORMATION_LAWS)}; if none of them "
                f"states this family's root honestly, that is a gap in the constitution and not a gap "
                f"here.")
        if self.formation not in FORMATION_LAWS:
            raise KernelRefusal(
                "unknown-root-formation", self.family_id,
                f"{self.formation!r} is not a declared root-formation law. The vocabulary is "
                f"{sorted(FORMATION_LAWS)} and it is deliberately OPEN — a structured sufficient-state "
                f"root will need its own — but it is not open to a caller: a formation law nobody declared "
                f"is a value nobody can realize or adjudicate.")

    def witness(self, law: AnalyticalLaw) -> ConstitutionWitness:
        """**This family's computed `ConstitutionWitness`, against its BOUND law.**

        The law is required, not optional, and that is boundary check 1 of 2026-09-29: *"v8 makes admitted
        continuation edges identity-bearing… Changing the region must change the family witness."* The
        region lives on the law, so a witness computed from this record's text alone would be blind to it —
        and to the composition, the value form and everything else the law asserts. The `law` determinant
        therefore carries the law's NAME and the law's own witness digest.

        It follows that a witness is computed against the law vocabulary of a Manifold rather than from a
        declaration in isolation, which is the honest position: the same declaration under a different law
        vocabulary is not the same constitution. `MME.witness_of` is the ordinary way to obtain one, because
        the engine is what binds a law name to a law."""
        return family_witness(self, law)

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
        _refuse_undeclared_parameters(law, self.parameters, self.family_id)
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

    def instance(self, scope: Optional[str] = None, *,
                 data_state: str = UNSTATED_DATA_STATE) -> AnalyticalInstance:
        """The analytical instance of this family — **which does NOT carry this family's own constitution
        witness.** That witness is per-object and answers a staleness question about one identity; it is
        computed by `witness()` and keyed on the `RetentionKey`. What the instance carries is the shared
        constitution CONTEXT (publication-level) and the `data_state` of the material it was established
        from. Keeping them apart is P-1's whole instruction."""
        return AnalyticalInstance(manifold=self.manifold, universe=self.universe,
                                  participation=self.participation, scope=scope,
                                  data_state=data_state)

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
    manifold: str
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
    #: **RETIRED** — see `MeasureFamily.constitution`. Computed by `witness()`.
    constitution: Optional[str] = None

    def __post_init__(self) -> None:
        refuse_a_declared_constitution(self, self.expression_id)

    def witness(self, law: AnalyticalLaw) -> ConstitutionWitness:
        """**This expression's computed `ConstitutionWitness`, against its BOUND constructor law.**

        `admitted_bases` is NOT a determinant of it — ruled 2026-09-28, *"expression identity ≠ one
        particular sufficient basis used to establish it"* — so admitting a new route leaves every value
        already established over an existing route current rather than stale. Which route a value actually
        took rides on the value, as `ExpressionOutput.basis_id`.

        The constructor's own REQUIRED BASIS is a different matter and does enter, through the law's witness:
        what routes an expression admits is the declaration's business, but what the law REQUIRES of any
        route is the law's, and a law that changed its requirement is a different constitution."""
        return expression_witness(self, law)

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
        _refuse_undeclared_parameters(law, self.parameters, self.expression_id)
        return law

    def instance(self, *, data_state: str = UNSTATED_DATA_STATE) -> AnalyticalInstance:
        return AnalyticalInstance(manifold=self.manifold, universe=self.universe,
                                  participation=self.participation, scope=self.scope,
                                  data_state=data_state)

    def at(self, anchor: Anchor) -> ExpressionPoint:
        return ExpressionPoint(self.expression_id, anchor)

    def basis(self, basis_id: str) -> Optional[SufficientBasis]:
        for b in self.admitted_bases:
            if b.basis_id == basis_id:
                return b
        return None


def _refuse_undeclared_parameters(law: AnalyticalLaw, parameters: Mapping[str, object],
                                  identity: str) -> None:
    """**`parameters` IS A SEMANTIC CONSTITUTION FIELD, AND THE LAW SAYS WHAT MAY BE IN IT.**

    Ruled (Huayin, 2026-09-29): *"`parameters` may be taken whole only because it is a semantic constitution
    field. Do not allow provider/codec/performance parameters into that field. Those belong to realization
    standing. A ConstitutionWitness is analytical identity, not merely a conservative cache-invalidation
    hash."*

    The witness takes this field WHOLE, so the field has to be clean at the source — and the authority for
    what individuates a law's use is the law, which already declares it. A denylist of suspicious names
    (`codec`, `batch_size`, `compression`…) would have to guess; `required_parameters` states it."""
    undeclared = sorted(set(parameters) - set(law.required_parameters))
    if undeclared:
        raise KernelRefusal(
            "undeclared-parameter", identity,
            f"declares parameter(s) {undeclared}, which law {law.name!r} does not name as "
            f"identity-bearing (it declares {list(law.required_parameters)}). **THIS FIELD IS ANALYTICAL "
            f"IDENTITY AND IT ENTERS THE CONSTITUTION WITNESS WHOLE**, so a provider, codec, compression, "
            f"batch-size or any other performance knob put here would make a physical tuning choice a "
            f"different analytical constitution — and would make the witness a cache-invalidation hash "
            f"instead of an identity. Those belong to REALIZATION STANDING "
            f"(`RealizationStanding`/`ProviderProfile`). If the parameter genuinely individuates this "
            f"law's use, the law must declare it.")


def universe_of(u: Universe) -> str:                            # readability in exhibits
    return u.name


__all__ = ["DIRECT", "FORMATION_LAWS", "PARTICIPATION_CARDINALITY", "ExpressionPoint", "FamilyPoint",
           "GovernedExpression", "MeasureFamily", "Operand", "SufficientBasis", "universe_of"]
