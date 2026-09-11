"""
columna_core.governed.resolve — the total canonical `Law(F)` view.

TOTALITY IS SEMANTIC, NOT LITERAL (ruled 2026-09-11). The publication does not serialize a
consequence that a cited law already determines — doing so would make the bytes look total while
teaching a reader to trust a restated theorem. Instead THIS module produces, for every family, a
view in which **silence is impossible**: each of ToD v7.1 §4's nine responsibilities carries exactly
one standing, with the provenance that established it.

    established      · by an authoritative constitutive declaration      (DECLARED)
                     · by an admitted foundation-law citation            (CITED_LAW)
                     · by lawful entailment from other established parts (ENTAILED)
    explicit-none    a POSITIVE negative — the responsibility is established, and what it
                     establishes is that nothing applies
    unestablished    not yet established. Never a default, never a permission

This is RESPONSIBILITY-LOCAL RESOLUTION STANDING, not a universal analytical-standing enum: it says
how *this* responsibility of *this* family came to be settled, and nothing about the family's
standing in the world.

THE RULE IT PRESERVES: **declaration is for analytical choices; derivation is for consequences.**
Nothing a cited law determines is ever asked of a human — MIN/MAX's empty fiber, a constructed
family's continuation, a result's value domain, the lineage graph. Nothing a law does NOT determine
is ever invented — a primitive family's continuation is an analytical choice (is this quantity
additive?), and where it is not declared it is UNESTABLISHED and stays so.

VALIDITY IS ABOUT IDENTITY. A record cannot claim to establish a MeasureFamily while its
identity-bearing constitution is itself unresolved, so the `Σ(F)` responsibilities — the ones §3.9
makes a succession when they change — must be settled. The rest may remain unestablished: a family
can exist while a particular movement has not been established. **No defaults are invented to satisfy
validation.**
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from . import foundation as fdn
from .publication import (
    CONSTRUCTION,
    COINCIDENT,
    ExplicitNone,
    Family,
    GovernedPublicationV2,
    PRIMITIVE,
)

# ── the nine responsibilities of ToD v7.1 §4, in the paper's order ───────────────────────────────
C1_TARGET = "target_specification"
C2_IDENTITY = "identity_and_ancestry"
C3_DOMAIN_MOVEMENT = "domain_and_movement"
C4_FORMATION = "formation"
C5_PARTICIPATION = "eligibility_and_participation"
C6_SEMANTIC_VALUES = "semantic_values"
C7_SUFFICIENT_STATE = "sufficient_state_bases"
C8_CONTINUATION = "continuation_and_agreement"
C9_EXCEPTIONAL = "exceptional_cases"

RESPONSIBILITIES = (C1_TARGET, C2_IDENTITY, C3_DOMAIN_MOVEMENT, C4_FORMATION, C5_PARTICIPATION,
                    C6_SEMANTIC_VALUES, C7_SUFFICIENT_STATE, C8_CONTINUATION, C9_EXCEPTIONAL)

#: `Σ(F)` — the identity-bearing responsibilities. Derived from §2.2's signature content and §3.9's
#: succession test, which must agree and do: anything whose change is a succession is in the
#: signature; anything whose change is not, is out. A family is not VALID until these are settled.
#:
#: C3 is deliberately absent. §4.1 keeps the family's defined domain separate from its identity, and
#: the ruling is explicit that "a family can exist while a particular continuation/movement has not
#: been established". C7 and C9 are consequences, not constitution.
IDENTITY_BEARING = (C1_TARGET, C2_IDENTITY, C4_FORMATION, C5_PARTICIPATION,
                    C6_SEMANTIC_VALUES, C8_CONTINUATION)

# ── standings and provenances ────────────────────────────────────────────────────────────────────
ESTABLISHED, EXPLICIT_NONE, UNESTABLISHED = "established", "explicit-none", "unestablished"
DECLARED, CITED_LAW, ENTAILED = "declared", "cited-law", "entailed"


class LawResolutionRefusal(ValueError):
    """The family's contract cannot be resolved into a coherent view.

    Distinct from "unestablished": unestablished is a legitimate resolved state, this is an artifact
    that contradicts itself or cites what does not exist. Consumers map it onto their own refusal
    taxonomy rather than this module minting one."""


@dataclass(frozen=True)
class Standing:
    """One responsibility's resolved standing."""

    responsibility: str
    standing: str
    provenance: Optional[str] = None
    value: Any = None
    note: str = ""

    @property
    def settled(self) -> bool:
        """Established or explicitly none — either way, not silent."""
        return self.standing in (ESTABLISHED, EXPLICIT_NONE)


@dataclass(frozen=True)
class LawView:
    """A TOTAL canonical view of one family's `Law(F)`. Silence is not representable."""

    family_id: str
    canonical_reference: str
    entries: dict = field(default_factory=dict)

    def __getitem__(self, responsibility: str) -> Standing:
        return self.entries[responsibility]

    def standing(self, responsibility: str) -> str:
        return self.entries[responsibility].standing

    @property
    def valid(self) -> bool:
        return not self.validity_problems

    @property
    def validity_problems(self) -> tuple:
        out = []
        for r in IDENTITY_BEARING:
            e = self.entries[r]
            if not e.settled:
                out.append(f"{r} is {e.standing}"
                           + (f" — {e.note}" if e.note else ""))
        return tuple(out)

    @property
    def unestablished(self) -> tuple:
        return tuple(r for r in RESPONSIBILITIES if self.entries[r].standing == UNESTABLISHED)


def _continuation_law(view_slot: Standing):
    """The FoundationLaw a resolved continuation names, or None where it does not name one."""
    if view_slot.standing != ESTABLISHED:
        return None
    return view_slot.value


def resolve_family(fam: Family, pub: GovernedPublicationV2, _stack: tuple = ()) -> LawView:
    """Resolve one family's nine responsibilities. Total by construction."""
    if fam.family_id in _stack:
        raise LawResolutionRefusal(
            f"constitutive lineage is not well-founded: {' -> '.join(_stack + (fam.family_id,))}. "
            f"§3.7 requires a well-founded relation rooted in the universe's governed primitive "
            f"inputs.")
    e: dict = {}
    subject = f"family {fam.family_id!r} ({fam.canonical_reference})"

    # ── C2 · identity and ancestry ───────────────────────────────────────────────────────────────
    parents = []
    for pid in fam.parents:
        parent = pub.family(pid)
        if parent is None:
            raise LawResolutionRefusal(
                f"{subject}: formation names parent family_id {pid!r}, which this publication does "
                f"not declare. A construction cannot cite what is not governed here.")
        parents.append(parent)
    e[C2_IDENTITY] = Standing(
        C2_IDENTITY, ESTABLISHED, DECLARED,
        value={"family_id": fam.family_id, "universe": fam.universe,
               "constitutive_anchor": fam.constitutive_anchor,
               "canonical_reference": fam.canonical_reference,
               "parents": tuple(fam.parents)},
        note=("lineage is DERIVED from formation (§3.7), not separately asserted"
              if fam.parents else "primitive: a root of the lineage relation (§3.7)"))

    # ── C1 · target specification ────────────────────────────────────────────────────────────────
    # A cited law does NOT establish the target. §11.5.1 makes COUNT the standing proof: `count(I)`
    # and `count(x@I)` are "distinct targets", and citing COUNT chooses neither.
    e[C1_TARGET] = Standing(C1_TARGET, ESTABLISHED, DECLARED, value=fam.target)

    # ── C4 · formation ───────────────────────────────────────────────────────────────────────────
    if fam.formation.kind == PRIMITIVE:
        cs = fam.formation.contribution_structure
        if cs is None:
            e[C4_FORMATION] = Standing(
                C4_FORMATION, UNESTABLISHED, note=(
                    "primitive intake, but the contribution structure is not established: where the "
                    "physical source grain is finer than the constitutive anchor, resolving several "
                    "contributions into one constituted value IS analytical law, and nothing here "
                    "establishes it"))
        else:
            if cs != COINCIDENT:
                law = fdn.resolve(cs)                      # refuses an unknown citation
                if not law.usable_as_continuation and law.name != "COUNT":
                    pass                                    # resolution law need not continue
                note = f"several contributions per point, resolved by {cs}"
            else:
                note = "one contribution per analytical point (claim, checked against realization)"
            e[C4_FORMATION] = Standing(C4_FORMATION, ESTABLISHED, DECLARED,
                                       value={"kind": PRIMITIVE, "contribution_structure": cs},
                                       note=note)
    else:
        law = fdn.resolve(fam.formation.law)
        missing = [p for p in law.required_parameters if p not in fam.formation.parameters]
        if missing:
            raise LawResolutionRefusal(
                f"{subject}: formation law {fam.formation.law} requires identity-bearing "
                f"parameter(s) {missing}, which the constitution does not carry")
        e[C4_FORMATION] = Standing(
            C4_FORMATION, ESTABLISHED, CITED_LAW,
            value={"kind": CONSTRUCTION, "law": fam.formation.law, "law_name": law.name,
                   "operands": fam.formation.operands, "parameters": fam.formation.parameters},
            note=f"formation cites {fam.formation.law}")

    # ── C5 · eligibility and participation ───────────────────────────────────────────────────────
    if fam.participation:
        e[C5_PARTICIPATION] = Standing(C5_PARTICIPATION, ESTABLISHED, DECLARED,
                                       value=fam.participation)
    else:
        e[C5_PARTICIPATION] = Standing(
            C5_PARTICIPATION, UNESTABLISHED,
            note=("§4.2: participation 'is not automatically the set of surviving physical records'. "
                  "It is a choice, and no law supplies it"))

    # ── C6 · semantic values ─────────────────────────────────────────────────────────────────────
    if fam.formation.kind == PRIMITIVE:
        if fam.value_domain is None:
            e[C6_SEMANTIC_VALUES] = Standing(
                C6_SEMANTIC_VALUES, UNESTABLISHED,
                note="a primitive family's operand domain is declared; nothing entails it")
        elif fam.value_domain not in fdn.DOMAINS:
            raise LawResolutionRefusal(
                f"{subject}: value_domain {fam.value_domain!r} is not a governed value domain "
                f"({sorted(fdn.DOMAINS)})")
        else:
            e[C6_SEMANTIC_VALUES] = Standing(C6_SEMANTIC_VALUES, ESTABLISHED, DECLARED,
                                             value=fam.value_domain)
    else:
        law = fdn.resolve(fam.formation.law)
        parent_views = [resolve_family(p, pub, _stack + (fam.family_id,)) for p in parents]
        operand_standing = parent_views[0][C6_SEMANTIC_VALUES]
        if operand_standing.standing != ESTABLISHED:
            e[C6_SEMANTIC_VALUES] = Standing(
                C6_SEMANTIC_VALUES, UNESTABLISHED,
                note=f"operand family {parents[0].family_id!r} has no established value domain")
        else:
            operand_domain = operand_standing.value
            if not law.admits_operand(operand_domain):
                raise LawResolutionRefusal(
                    f"{subject}: formation law {law.name} does not admit an operand of domain "
                    f"{operand_domain!r} (admits {sorted(law.operand_domains)})")
            if fam.value_domain is not None and fam.value_domain != law.result_for(operand_domain):
                raise LawResolutionRefusal(
                    f"{subject}: declares value_domain {fam.value_domain!r} but "
                    f"{law.name} over {operand_domain!r} yields "
                    f"{law.result_for(operand_domain)!r}. A constructed family's result domain is a "
                    f"consequence, not a choice.")
            e[C6_SEMANTIC_VALUES] = Standing(
                C6_SEMANTIC_VALUES, ESTABLISHED, ENTAILED,
                value=law.result_for(operand_domain),
                note=f"{law.name} over an operand of domain {operand_domain!r}")

    # ── C8 · continuation and agreement ──────────────────────────────────────────────────────────
    entailed_name = None
    if fam.formation.kind == CONSTRUCTION:
        entailed_name = fdn.resolve(fam.formation.law).entails_continuation

    if isinstance(fam.continuation, ExplicitNone):
        e[C8_CONTINUATION] = Standing(C8_CONTINUATION, EXPLICIT_NONE, DECLARED,
                                      note=fam.continuation.reason or
                                      "declared not to compose across refinement")
    elif fam.continuation is not None:
        law = fdn.resolve(fam.continuation)
        if not law.usable_as_continuation:
            raise LawResolutionRefusal(
                f"{subject}: cites {fam.continuation} as a CONTINUATION, which this vocabulary "
                f"refuses — {law.identity_note}")
        if entailed_name is not None and entailed_name != law.name:
            raise LawResolutionRefusal(
                f"{subject}: declares continuation {law.name} while its formation law entails "
                f"{entailed_name}. A continuation that diverges from the formation law is a "
                f"different family (§3.9), not an override — cite a different formation law.")
        e[C8_CONTINUATION] = Standing(C8_CONTINUATION, ESTABLISHED, DECLARED, value=law,
                                      note=f"declared: {fam.continuation}")
    elif entailed_name is not None:
        if entailed_name == fdn.NO_CONTINUATION:
            e[C8_CONTINUATION] = Standing(
                C8_CONTINUATION, EXPLICIT_NONE, ENTAILED,
                note=f"{fdn.resolve(fam.formation.law).name} does not compose across refinement")
        else:
            law = fdn.LAWS[entailed_name]
            e[C8_CONTINUATION] = Standing(
                C8_CONTINUATION, ESTABLISHED, ENTAILED, value=law,
                note=(f"entailed by formation law "
                      f"{fdn.resolve(fam.formation.law).name}: values formed by it compose under "
                      f"{law.name}"))
    else:
        e[C8_CONTINUATION] = Standing(
            C8_CONTINUATION, UNESTABLISHED,
            note=("a primitive family's continuation is an analytical CHOICE — whether this quantity "
                  "composes across refinement at all — and there is no formation law to entail one "
                  "from. Nothing here establishes it, and no default is invented"))

    # A continuation composes values OF THIS FAMILY'S OWN domain, so the law must admit that domain.
    # Checked here rather than only on constructions: a primitive family declaring an additive
    # continuation over a `text` quantity is exactly the error this catches, and it has no formation
    # law whose operand check would have caught it first.
    cont_check = _continuation_law(e[C8_CONTINUATION])
    if cont_check is not None and e[C6_SEMANTIC_VALUES].standing == ESTABLISHED:
        own_domain = e[C6_SEMANTIC_VALUES].value
        if not cont_check.admits_operand(own_domain):
            raise LawResolutionRefusal(
                f"{subject}: continuation law {cont_check.name} does not admit values of domain "
                f"{own_domain!r} (admits {sorted(cont_check.operand_domains)}). A family cannot "
                f"compose under a law that does not accept the values it carries.")

    # ── C7 · sufficient-state bases ──────────────────────────────────────────────────────────────
    cont = _continuation_law(e[C8_CONTINUATION])
    if cont is not None:
        e[C7_SUFFICIENT_STATE] = Standing(
            C7_SUFFICIENT_STATE, ESTABLISHED, ENTAILED, value=cont.sufficient_state,
            note=f"entailed by the continuation law {cont.name}")
    elif e[C8_CONTINUATION].standing == EXPLICIT_NONE:
        e[C7_SUFFICIENT_STATE] = Standing(
            C7_SUFFICIENT_STATE, EXPLICIT_NONE, ENTAILED,
            note="no continuation, therefore no state that continues it")
    else:
        e[C7_SUFFICIENT_STATE] = Standing(
            C7_SUFFICIENT_STATE, UNESTABLISHED,
            note="follows the continuation, which is unestablished")

    # ── C3 · domain and movement ─────────────────────────────────────────────────────────────────
    # Two POSITIVE declarations are required for admission (§4.1): the anchor must be in the declared
    # domain AND the movement licensed. Absence is UNESTABLISHED and can never read as permission.
    if isinstance(fam.movement, ExplicitNone) or isinstance(fam.domain, ExplicitNone):
        e[C3_DOMAIN_MOVEMENT] = Standing(
            C3_DOMAIN_MOVEMENT, EXPLICIT_NONE, DECLARED,
            value={"domain": fam.domain, "movement": fam.movement},
            note="declared: no movement is licensed for this family")
    elif fam.domain is not None or fam.movement is not None:
        e[C3_DOMAIN_MOVEMENT] = Standing(
            C3_DOMAIN_MOVEMENT, ESTABLISHED, DECLARED,
            value={"domain": fam.domain, "movement": fam.movement})
    else:
        e[C3_DOMAIN_MOVEMENT] = Standing(
            C3_DOMAIN_MOVEMENT, UNESTABLISHED,
            note=("§4.1: 'A geometrically available projection and a computable state operation do "
                  "not by themselves put A in the admitted anchors.' Absence of a prohibition is "
                  "not permission"))

    # ── C9 · exceptional cases ───────────────────────────────────────────────────────────────────
    declared_ex = dict(fam.exceptional)
    if cont is not None or e[C8_CONTINUATION].standing == EXPLICIT_NONE:
        entailed_empty = cont.empty_fiber if cont is not None else "not_applicable"
        if "empty_fiber" in declared_ex and declared_ex["empty_fiber"] != entailed_empty:
            raise LawResolutionRefusal(
                f"{subject}: declares empty_fiber {declared_ex['empty_fiber']!r} while the "
                f"continuation law entails {entailed_empty!r}. A theorem of the cited law is not "
                f"re-declarable; a family that means something else means it by a different law.")
        value = {"empty_fiber": entailed_empty}
        value.update(declared_ex)
        note = ("empty fiber ENTAILED by the continuation law, never re-asked"
                + (f"; {cont.identity_note}" if cont is not None else ""))
        e[C9_EXCEPTIONAL] = Standing(C9_EXCEPTIONAL, ESTABLISHED,
                                     DECLARED if declared_ex else ENTAILED, value=value, note=note)
    else:
        e[C9_EXCEPTIONAL] = Standing(
            C9_EXCEPTIONAL, ESTABLISHED if declared_ex else UNESTABLISHED,
            DECLARED if declared_ex else None, value=declared_ex or None,
            note="the empty-fiber case follows the continuation, which is unestablished")

    missing = [r for r in RESPONSIBILITIES if r not in e]
    if missing:                                             # pragma: no cover - structural guard
        raise LawResolutionRefusal(f"{subject}: resolution is not total; missing {missing}")
    return LawView(fam.family_id, fam.canonical_reference, e)


def resolve_all(pub: GovernedPublicationV2) -> dict:
    """Every family's total view, keyed by `family_id`."""
    return {f.family_id: resolve_family(f, pub) for f in pub.families}


def render(view: LawView) -> str:
    """A human-readable total view. The point of the format is that nothing can be absent."""
    lines = [f"Law(F) — {view.canonical_reference}  [{view.family_id}]"]
    width = max(len(r) for r in RESPONSIBILITIES)
    for r in RESPONSIBILITIES:
        s = view.entries[r]
        prov = f" ({s.provenance})" if s.provenance else ""
        lines.append(f"  {r:<{width}}  {s.standing}{prov}")
        if s.note:
            lines.append(f"  {'':<{width}}    · {s.note}")
    problems = view.validity_problems
    lines.append(f"  VALID: {'yes' if not problems else 'NO — ' + '; '.join(problems)}")
    return "\n".join(lines)
