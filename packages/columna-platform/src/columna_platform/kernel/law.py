"""
columna_platform.kernel.law — **the reusable semantic operator/law authority. SEMANTIC CONTENT ONLY.**

ONE OF TWO RESPONSIBILITIES, AND THE SPLIT IS THE RULING
--------------------------------------------------------
Ruled (Huayin, 2026-09-28): *"Keep two responsibilities separate: reusable semantic law/operator
schema; physical provider implementation… Do not port Core's duplicated `operators.py` /
`foundation.py` authority split merely for compatibility. Use those files as evidence about required
capabilities."*

So this module is the SEMANTIC AUTHORITY and `realization.py` is the PROVIDER PROFILE, and the split is
made once here rather than inherited as two registries that each hold half of the other's job. The V8-1
reconnaissance measured that split in Core and itemized what was stranded on the wrong side —
`re_entrant`, `is_monoid`, `linear`, `combine`, and a duplicated `accepts`/`out_rule` versus
`operand_domains`/`result_domain` signature axis. **None of it is ported.** `is_monoid` and `combine`
appear here as what they are (`Composition.has_identity` and `Composition.token`); `re_entrant` appears
as `ContinuationRegion`, because a Boolean could not carry it; `linear` and the SQL/scan machinery are
realization and are not here at all.

THE THREE DISTINCTIONS THIS SCHEMA EXISTS TO MAKE
--------------------------------------------------
**1 · STRUCTURAL KIND IS ORTHOGONAL TO ANALYTICAL SORT.** `MAP` / `REDUCER` / `ORDERED` describes the
shape of a computation. It says NOTHING about whether the thing computed is a measure family or a
governed expression, and a test pins that: `HLL_SKETCH` is a REDUCER and founds a family; `HLL_ESTIMATE`
is a MAP and cannot; `MEAN` is a REDUCER and cannot. Core's ToD v7.1 §3.6 already said routing confers
nothing — *"Neither operation receives or loses family authority solely from an implementation
classification"* — and this schema makes it structurally impossible to confuse them.

**2 · A LAW EITHER CARRIES A CONTINUATION OR IT DOES NOT, AND ONLY THE FIRST MAY FOUND A FAMILY.** This
is ToD v8 §9.2 — v7.1 allowed a durable derived measure family to be justified *either* by
self-sufficient continuation *or* by a sufficient-state basis, and v8 keeps only the first. In Core that
had to be retro-fitted as a gate that fired after resolution (V8-0's C4 clause 2, over an object that
had already been constituted as a family). **Here it is a constitution-time impossibility:**
`MeasureFamily` will not construct over a law whose `continuation is None`, so "do not create a Mean
family" is not a rule anyone has to remember.

**3 · VALUE FORM IS NOT RESULT DOMAIN.** A family's continuation-bearing VALUE and its displayed RESULT
are different objects, and the HLL case is the flagship: the value form is a SKETCH, which merges; the
displayed result is an integer estimate, which does not. `value_form` is what the family retains;
`finalization` is the separate law that turns it into something displayable — and that law is an
EXPRESSION constructor, never a continuation.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .geometry import Anchor, Edge, KernelRefusal

# ── structural kind. ORTHOGONAL to analytical sort; see the module note. ─────────────────────────
MAP, REDUCER, ORDERED = "MAP", "REDUCER", "ORDERED"
KINDS = frozenset({MAP, REDUCER, ORDERED})

# ── value form: WHAT A FAMILY RETAINS, which is not what it displays ────────────────────────────
#: the displayed value IS the retained value (a running total witnesses a SUM)
SCALAR = "scalar"
#: the retained value is a structured witness the displayed value cannot be recovered from
STRUCTURED = "structured"
#: the retained value is a witness plus the order key that selected it
ORDERED_WITNESS = "ordered_witness"
VALUE_FORMS = frozenset({SCALAR, STRUCTURED, ORDERED_WITNESS})

# ── governed value domains. The authoring vocabulary, not an engine's dtypes. ────────────────────
DOMAINS = frozenset({"integer", "decimal", "text", "boolean", "date", "timestamp", "sketch"})
SAME_AS_OPERAND = "same_as_operand"

# ── composition tokens ──────────────────────────────────────────────────────────────────────────
ADDITION, SKETCH_UNION, LATEST_BY_ORDER, MINIMUM, MAXIMUM = (
    "addition", "sketch_union", "latest_by_order", "minimum", "maximum")


@dataclass(frozen=True)
class Composition:
    """**The analytical composition a law induces on its own values** — the algebra, not a dispatch tag.

    `has_identity` is a THEOREM about the law and never a preference: it is the whole of the
    empty-fibre question. A commutative semigroup with no identity supplies no fold value over an empty
    contributing fibre, and saying so is a governed answer rather than a gap."""

    token: str
    associative: bool
    commutative: bool
    has_identity: bool
    note: str

    @property
    def is_monoid(self) -> bool:
        return self.associative and self.has_identity


@dataclass(frozen=True)
class ContinuationRegion:
    """**Over WHICH edges does this family's value closure hold?**

    The object the V8-1 reconnaissance said had to exist. Core carries `re_entrant` as a global Boolean
    and its own comment forbids flattening a conditional certification into `True` — *"If type, order,
    support or anchor conditions would qualify the certification, the case must NOT be flattened into
    True; it stays uncertified"* — which is sound against a Boolean and refuses exactly the case ToD v8
    §3.1 and §3.5 require. So the Boolean is replaced rather than moved.

    **THIS IS A PLATFORM IMPLEMENTATION REPRESENTATION AND NOT A NEW ToD PRIMITIVE** (ruled Huayin,
    2026-09-28, approving it on exactly that footing). It represents the family's **admitted continuation
    region / edge-relative value-closure conditions** — facts v8 already has in §3.1 and §3.5 — in a form
    an engine can adjudicate against. It does not add a concept to the theory and must not be cited as
    though it did.

    The invariant it exists to hold, in the ruling's own words:

        *A non-root family materialization does not erase the authority path from `F@R_F`. It may seed
        later continuation only when the complete resulting route remains admitted under the same family
        constitution and premises.*

    Escalate to a theory gap only on finding a lawful family whose continuation rights **cannot** be
    expressed by v8's admitted-edge / partial-continuation-graph semantics. The `forgettable` set below is
    the narrow shape those semantics need for the laws in this build; a family needing a genuine
    per-edge graph would be represented by widening THIS object, not by amending the theory.

    Represented POSITIVELY, as the constituents a continuation may forget. `EVERYWHERE` is the ordinary
    additive case; a restricted region is the stock case — a level of on-hand stock composes across
    stores and **does not** compose across time, and no amount of caching changes that.

    **THE LAUNDERING GUARD IS THE REASON THIS TAKES A CUMULATIVE SET AND NOT ONE EDGE.** Forgetting
    `{store}` and then `{day}` forgets `{store, day}`. If `day` is not forgettable, a two-step route
    must refuse as surely as the one-step route does — otherwise an intermediate materialization becomes
    a way to obtain an answer the law forbids, and *physical availability would have become analytical
    authority.* So `admits` is asked about everything forgotten SINCE THE ROOT, never about the last hop
    alone."""

    forgettable: Optional[frozenset[str]]       # None == every constituent may be forgotten
    note: str = ""

    @staticmethod
    def everywhere(note: str = "value closure holds over every coarsening") -> "ContinuationRegion":
        return ContinuationRegion(forgettable=None, note=note)

    @staticmethod
    def forgetting_only(refs, note: str) -> "ContinuationRegion":
        return ContinuationRegion(forgettable=frozenset(refs), note=note)

    def admits(self, forgotten_since_root: frozenset[str]) -> bool:
        if self.forgettable is None:
            return True
        return forgotten_since_root <= self.forgettable

    def why_not(self, forgotten_since_root: frozenset[str]) -> str:
        excluded = sorted(forgotten_since_root - (self.forgettable or frozenset()))
        return (f"its value closure does not extend to forgetting {excluded} "
                f"({self.note}). Closure is edge-relative: this family composes over "
                f"{sorted(self.forgettable or ())} and over nothing else")


@dataclass(frozen=True)
class RequiredBasis:
    """**What an EXPRESSION constructor needs in order to be established.**

    Role-indexed, because ToD v8 §5.3's basis is `(G₁…G_m)` and a position is not a role — the one piece
    of the V8-1 record design carried across verbatim, since it is the thing that lets `(Count, SumX,
    SumX², SumXY)` be stated at all.

    `requires_common_participation` is §11.5.2's word MATCHING made a field: a SUM and a COUNT that
    ranged over different contributions are individually valid and jointly meaningless. A basis that did
    not carry the requirement would license exactly the pairing it exists to forbid.

    **`components` NAMES BASIS SLOTS, AND A SLOT BINDS A GOVERNED ANALYTICAL IDENTITY — NOT A
    ROOT-FORMATION OPERATOR** (ruled Huayin, 2026-09-28). The slot labels here are v8 §11.5.2's own words
    (`SUM`, `COUNT`), and that spelling is a description of the slot's job, **not a requirement that the
    family bound into it was formed by a law of that name.** Revenue and OrderCount are bound as governed
    identities; how each one's root value was formed is a separate question and stays separate.

    So there is deliberately **NO CHECK** anywhere in this kernel that a basis component's family was
    "formed by" the component law. The V8-1 report recommended adding one and the ruling declined it:
    *"Root formation and family continuation stay separate. Expression basis roles bind governed
    analytical identities… not root-formation operators."* `test_frameql_serving.py` pins the absence, so
    the rule cannot reappear by accident."""

    components: tuple[str, ...]
    requires_common_participation: bool
    note: str


@dataclass(frozen=True)
class AnalyticalLaw:
    """One reusable semantic law. **Semantic content only** — nothing here names a backend."""

    name: str
    kind: str
    target_form: str
    operand_domains: frozenset[str]
    result_domain: str
    value_form: str
    sufficient_state: str
    #: The composition this law's OWN values compose under, or `None`. **`None` is what makes a law
    #: unable to found a family** (ToD v8 §9.2) — not a missing field to be filled in later.
    continuation: Optional[Composition] = None
    #: Over which edges the closure holds. Meaningless without a continuation, and validated as such.
    region: ContinuationRegion = field(default_factory=ContinuationRegion.everywhere)
    approximation: str = "exact"
    #: A governed order this law needs in order to select at all (LAST/FIRST).
    requires_order: bool = False
    #: Identity-bearing parameters, which individuate the law's use rather than tune it.
    required_parameters: tuple[str, ...] = ()
    #: Present only on an EXPRESSION CONSTRUCTOR: the basis over other families it needs.
    required_basis: Optional[RequiredBasis] = None
    #: For a law whose `value_form` is STRUCTURED: the law that FINALIZES its value for display. Named
    #: rather than implied, because the finalization is a different law with a different standing —
    #: it is an expression constructor, and it is the pair the HLL proof turns on.
    finalized_by: Optional[str] = None
    identity_note: str = ""

    def __post_init__(self) -> None:
        if self.kind not in KINDS:
            raise KernelRefusal("unknown-kind", self.name, f"{self.kind!r} is not one of {sorted(KINDS)}")
        if self.value_form not in VALUE_FORMS:
            raise KernelRefusal("unknown-value-form", self.name,
                                f"{self.value_form!r} is not one of {sorted(VALUE_FORMS)}")
        if self.result_domain != SAME_AS_OPERAND and self.result_domain not in DOMAINS:
            raise KernelRefusal("unknown-domain", self.name,
                                f"result domain {self.result_domain!r} is not governed")
        if self.continuation is None and self.region.forgettable is not None:
            raise KernelRefusal(
                "region-without-continuation", self.name,
                "states a restricted continuation region while carrying no continuation. A region is "
                "the answer to 'over which edges does the closure hold'; a law with no closure has no "
                "edges to be relative to.")
        if self.continuation is not None and self.required_basis is not None:
            raise KernelRefusal(
                "both-sorts", self.name,
                "carries BOTH a continuation and a required basis over other families. Those are the "
                "two sorts' establishment routes and ToD v8 §9.2 keeps them apart: a law that both "
                "composes and must be reconstructed from other objects would let one citation found "
                "either sort depending on who read it.")
        if self.value_form == STRUCTURED and self.finalized_by is None and self.continuation is not None:
            raise KernelRefusal(
                "structured-without-finalization", self.name,
                "retains a STRUCTURED value and names no finalization. A structured value that cannot "
                "be finalized can be merged forever and never displayed, and the law owes the name of "
                "the expression constructor that displays it.")

    # ── the two standings, entailed and never declared ──────────────────────────────────────────
    @property
    def continuation_bearing(self) -> bool:
        return self.continuation is not None

    @property
    def may_found_a_family(self) -> bool:
        """**ToD v8 §9.2, as a property rather than a gate.** A family's values continue under
        refinement from its own law. A law with no continuation cannot supply that, and no amount of
        naming, caching, repetition or durable governance substitutes (§3.7)."""
        return self.continuation_bearing

    @property
    def may_be_a_constructor(self) -> bool:
        """An expression constructor is a law that determines a value from a basis over OTHER governed
        objects. A law that composes its own values is a family law, and is not one of these."""
        return self.required_basis is not None or not self.continuation_bearing

    def admits_operand(self, domain: str) -> bool:
        return domain in self.operand_domains

    def result_for(self, operand_domain: str) -> str:
        return operand_domain if self.result_domain == SAME_AS_OPERAND else self.result_domain

    def admits_edge(self, edge: Edge, forgotten_since_root: frozenset[str]) -> bool:
        return self.continuation_bearing and self.region.admits(forgotten_since_root | edge.forgotten)


class LawRegistry:
    """The semantic authority, as a lookup. **Immutable once built**, and a citation that names an
    unknown law refuses rather than falling back to a same-named law elsewhere."""

    def __init__(self, laws: tuple[AnalyticalLaw, ...], *, vocabulary: str, version: str) -> None:
        self.vocabulary, self.version = vocabulary, version
        self._laws = {law.name: law for law in laws}
        if len(self._laws) != len(laws):
            raise KernelRefusal("duplicate-law", vocabulary, "a law is registered twice")

    def __contains__(self, name: str) -> bool:
        return name in self._laws

    def __iter__(self):
        return iter(self._laws.values())

    def get(self, name: str) -> AnalyticalLaw:
        law = self._laws.get(name)
        if law is None:
            raise KernelRefusal(
                "unknown-law", self.vocabulary,
                f"{name!r} names no law in {self.vocabulary}/{self.version} "
                f"(known: {sorted(self._laws)}). A law whose content moved is a different law; this "
                f"authority will not substitute one of its own.")
        return law

    def family_laws(self) -> tuple[AnalyticalLaw, ...]:
        return tuple(law for law in self if law.may_found_a_family)

    def constructors(self) -> tuple[AnalyticalLaw, ...]:
        return tuple(law for law in self if not law.may_found_a_family)


__all__ = [
    "ADDITION", "AnalyticalLaw", "Anchor", "Composition", "ContinuationRegion", "DOMAINS", "KINDS",
    "LATEST_BY_ORDER", "LawRegistry", "MAP", "MAXIMUM", "MINIMUM", "ORDERED", "ORDERED_WITNESS",
    "REDUCER", "RequiredBasis", "SAME_AS_OPERAND", "SCALAR", "SKETCH_UNION", "STRUCTURED",
    "VALUE_FORMS",
]
