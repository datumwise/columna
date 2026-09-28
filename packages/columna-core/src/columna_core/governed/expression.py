"""
columna_core.governed.expression — the total canonical `Law(E)` view for a **governed expression**.

THE SIBLING OF `resolve`, AND DELIBERATELY NOT AN EXTENSION OF IT.

Ruled (Huayin, 2026-09-28): *"Build `Expression` as a true sibling of `Family`. Do not implement it
as `Family(continuation=None)` or route it through `resolve_family`. The expression resolver should
answer expression questions only. It should have its own total governed view / validation contract
rather than inherit family responsibilities such as root, family domain, continuation, movement, or
empty-fiber family law."*

**THE REPO SUPPLIES THE REASON, NOT ONLY THE RULING.** `resolve_family` produces a TOTAL view over
nine responsibilities, so for an expression-shaped record it would not decline to answer — it would
ANSWER, and four of its answers would be family facts nobody asked for: C8 `EXPLICIT_NONE`, C7
`ESTABLISHED` by the formation route, C9 `{"empty_fiber": "no_composition"}`, and a C3 domain/movement
standing. And after V8-0 the first two combine, correctly, into a guaranteed C4 refusal. So routing an
expression through the family resolver does not merely misname the object: it routes it into a resolver
whose every answer is about a family, which then refuses it for not being one.

SEVEN RESPONSIBILITIES, NOT NINE, AND NONE OF THEM C3/C8/C9
-----------------------------------------------------------
Each carries exactly one standing, with the provenance that settled it, exactly as `Law(F)` does.
Silence is not representable here either — that discipline is sort-agnostic and is the best thing in
the governed layer.

  E1  constructor                      the operator law this expression is built by
  E2  operands_and_roles               the role-indexed governed operands, and their domains
  E3  constitutive_inner_anchors       §3.6 — where the expression is CONSTITUTED, not a root
  E4  participation_and_scope          who participates, and over what scope
  E5  admitted_bases                   zero, one, or several establishment routes
  E6  basis_agreement                  v8: *alternative lawful bases must agree*
  E7  identity_bearing_parameters      what the constructor requires to be individuated

WHAT IS REUSED FROM `resolve`, AND WHAT IS NOT
----------------------------------------------
**Reused: the STANDING VOCABULARY only** — `Standing`, and the `established` / `explicit-none` /
`unestablished` triad with its provenances. Those say how a responsibility came to be settled and carry
no sort: a fact established by a cited law is established by a cited law whatever holds it.

**Not reused, each because it would assert a family fact:** `LawView` (it is keyed by `family_id` and
its validity runs over `Σ(F)`); `IDENTITY_BEARING`, which IS `Σ(F)` and contains C4 formation, C5
participation, C6 semantic values and C8 continuation; `resolve_family`; and family lineage —
`Family.parents` derives a family→family constitutive edge, and an expression's ancestry runs through
its OPERANDS, so the edge is expression→family and must never be recorded as the other thing (§7.1
keeps family / expression / carrier lineage apart).

WHAT THIS MODULE DOES NOT DO, IN THIS UNIT
-------------------------------------------
* **No request serving and no peer Frame-QL target.** `native.NativePublication.sort_of` exists so a
  target has a lawful object to point at; nothing routes on it yet (ruling 8).
* **No applicability / participation / support split.** C5 stays deferred (ruling 9), so E4 is ONE
  responsibility and says so rather than pre-empting the split with three.
* **No local definition of `governed equivalence`** (ruling 6). See `GOVERNED_EQUIVALENCE_ERRATA`.
* **No generalization of `composite.py`** and no Operator Registry reconciliation.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Optional

from . import foundation as fdn
from .native import (
    ECF1,
    AdmittedBasis,
    Expression,
    Family as NativeFamily,
    Universe,
    canonical_expression_payload,
)
from .resolve import (
    CITED_LAW,
    DECLARED,
    ENTAILED,
    ESTABLISHED,
    EXPLICIT_NONE,
    UNESTABLISHED,
    Standing,
)

# ── the seven responsibilities of `Law(E)` ───────────────────────────────────────────────────────
E1_CONSTRUCTOR = "constructor"
E2_OPERANDS = "operands_and_roles"
E3_INNER_ANCHORS = "constitutive_inner_anchors"
E4_PARTICIPATION = "participation_and_scope"
E5_ADMITTED_BASES = "admitted_bases"
E6_BASIS_AGREEMENT = "basis_agreement"
E7_PARAMETERS = "identity_bearing_parameters"

EXPRESSION_RESPONSIBILITIES: tuple[str, ...] = (
    E1_CONSTRUCTOR, E2_OPERANDS, E3_INNER_ANCHORS, E4_PARTICIPATION, E5_ADMITTED_BASES,
    E6_BASIS_AGREEMENT, E7_PARAMETERS)

#: `Σ(E)` — the identity-bearing responsibilities, from ToD v8 §7.3's own list: constructor · governed
#: operand identities · operand roles · constitutive inner anchors · participation and scope ·
#: identity-bearing parameters.
#:
#: **E5 AND E6 ARE OUT, AND THAT IS THE RULING OF 2026-09-28**: *"expression identity ≠ one particular
#: sufficient basis used to establish it."* A sufficient basis is an ESTABLISHMENT ROUTE; v8 allows
#: several for one expression; so an expression with no admitted basis yet, one with a basis, and one
#: with two are the SAME expression at three moments of its governance — not three expressions. The
#: agreement obligation is a consequence of how many routes are admitted, so it cannot be constitutive
#: either.
#:
#: This mirrors `resolve.IDENTITY_BEARING`'s own discipline, where C7 and C9 are consequences rather
#: than constitution — and it is the same exclusion made for the same reason, one sort over.
SIGMA_E: tuple[str, ...] = (E1_CONSTRUCTOR, E2_OPERANDS, E3_INNER_ANCHORS, E4_PARTICIPATION,
                            E7_PARAMETERS)

#: Succession verdicts. Two, and deliberately not three: there is no "possibly the same" state, because
#: a verdict a consumer has to interpret is a verdict that will be interpreted differently twice.
SAME_EXPRESSION, SUCCESSOR_REQUIRED = "same-expression", "successor-required"

#: **THE ERRATA CANDIDATE, RECORDED HERE BECAUSE THIS IS WHERE THE REPO HITS IT** (ruling 6, Huayin
#: 2026-09-28): *"Do not invent a local definition of 'governed equivalence' to preserve identity
#: across a change… Please record the `governed equivalence` issue as a theory errata candidate, not an
#: implementation blocker."*
#:
#: `governed equivalence` is the escape clause on BOTH of v8's succession rules (§7.3, twice, and
#: §7.6), and v8 never defines it. ToD v7.1 §6.6 did: the equivalence must be a CONGRUENCE with respect
#: to `⊕` and must preserve constructor outputs. Until v8 carries that or its replacement, this module
#: is CONSERVATIVE in exactly one direction — where an identity-bearing constituent changes it says
#: `SUCCESSOR_REQUIRED`, and it never says `SAME_EXPRESSION` on the strength of an equivalence it would
#: have had to define itself.
#:
#: The same undefined phrase is the reason E6 stops where it does. Two alternative bases filling one
#: role with two DIFFERENT families is the case where agreement genuinely needs governed equivalence,
#: and this module reports that it cannot adjudicate it rather than guessing in either direction.
GOVERNED_EQUIVALENCE_ERRATA = (
    "`governed equivalence` is load-bearing in ToD v8 §7.3 (twice) and §7.6 and is never defined "
    "there. ToD v7.1 §6.6 required a congruence with respect to `⊕` that preserves constructor "
    "outputs; that requirement, or its deliberate replacement, is the missing definition. Until it "
    "exists, an identity-bearing change mints a successor and no local equivalence is invented."
)


class ExpressionResolutionRefusal(ValueError):
    """The expression's contract cannot be resolved into a coherent view.

    Distinct from `unestablished`, which is a legitimate resolved state: this is an artifact that
    contradicts itself or cites what does not exist. A separate type from `LawResolutionRefusal` for
    the reason `ExpressionAuthority` is a separate type from `FamilyAuthority` — the content is
    similar, the SUBJECT is not, and a consumer's refusal taxonomy should not have to ask which sort a
    refusal came from after the fact."""


@dataclass(frozen=True)
class ExpressionView:
    """A TOTAL canonical view of one expression's `Law(E)`. Silence is not representable.

    **There is no `family_id` on this record and nowhere to put one.** Its validity runs over `Σ(E)`,
    not `Σ(F)`, and it carries no root, no family domain, no continuation, no movement and no
    empty-fiber family law."""

    expression_id: str
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
        """**VALIDITY IS ABOUT IDENTITY**, the same rule `LawView` states. An expression cannot claim
        to establish a governed expression while its identity-bearing constitution is unresolved. The
        rest MAY remain unestablished: an expression can exist while no sufficient basis has yet been
        admitted, and E5/E6 are therefore not validity conditions."""
        out = []
        for r in SIGMA_E:
            e = self.entries[r]
            if not e.settled:
                out.append(f"{r} is {e.standing}" + (f" — {e.note}" if e.note else ""))
        return tuple(out)

    @property
    def unestablished(self) -> tuple:
        return tuple(r for r in EXPRESSION_RESPONSIBILITIES
                     if self.entries[r].standing == UNESTABLISHED)

    @property
    def establishable(self) -> bool:
        """Is there an admitted route by which a value of this expression could be determined?

        **A SEPARATE QUESTION FROM `valid`, AND KEEPING THEM SEPARATE IS THE POINT.** A valid
        expression with no admitted basis is a fully constituted governed object that nothing can yet
        evaluate — which is a capability limit, not a defect of its constitution. Fusing the two is
        precisely the fusion V8-0 had to unpick at the C7 seam."""
        return self.entries[E5_ADMITTED_BASES].standing == ESTABLISHED


def _constructor_law(expr: Expression) -> fdn.FoundationLaw:
    citation = fdn.LawCitation.from_dict(dict(expr.body["constructor"]))
    try:
        return fdn.resolve(citation)
    except fdn.UnknownFoundationLaw as exc:
        raise ExpressionResolutionRefusal(
            f"expression {expr.canonical_reference!r} cites constructor {citation}: {exc}. A "
            f"constructor is not approximated by a same-named law at another version."
        ) from exc


def _declared_continuation_law(fam: NativeFamily) -> Optional[str]:
    """The continuation LAW NAME a native family declares, or `None`.

    Read off the body rather than through `resolve_family`, and the narrowness is deliberate: this
    module needs one field from an operand's declaration and has no business resolving an operand's
    nine family responsibilities to get it. (`native_law._ParentLookup` made the same finding one layer
    up: law resolution needs a lookup, not a publication-shaped object.)"""
    cont = fam.body.get("continuation")
    if not isinstance(cont, dict):
        return None
    law = cont.get("law")
    return law if isinstance(law, str) and law else None


def resolve_expression(expr: Expression, universe: Universe,
                       families: Mapping[str, NativeFamily]) -> ExpressionView:
    """`Law(E)` — **the total seven-responsibility view, from the expression's own clauses.**

    `families` supplies the expression's operand and basis-component families by `family_id`. They are
    read for two facts only — a declared `value_domain` and a declared `continuation` law — and for
    nothing else. An expression does not inherit its operands' law; it CITES their identities.
    """
    e: dict[str, Standing] = {}
    subject = expr.canonical_reference
    law = _constructor_law(expr)

    # ── E1 · constructor ──────────────────────────────────────────────────────────────────────
    #
    # ESTABLISHED BY CITATION, and the note reports one fact a steward should see rather than
    # adjudicating on it: whether the constructor's own algebra yields a continuation. v8 does not
    # forbid an expression whose constructor composes — §5.4's moment families are continuation-bearing
    # AND carry structured composite state — so a law with a continuation is NOT refused here. What it
    # may be is a sign that the object was authored as the wrong sort, and that is a judgment for
    # whoever constituted it, made possible by reporting the fact.
    composes = law.entails_continuation != fdn.NO_CONTINUATION
    e[E1_CONSTRUCTOR] = Standing(
        E1_CONSTRUCTOR, ESTABLISHED, CITED_LAW, value=law,
        note=(f"{law.name}; "
              + (f"its values compose under {law.entails_continuation} — an expression whose "
                 f"constructor carries a continuation is lawful (§5.4) but is worth a second look at "
                 f"the sort it was authored as"
                 if composes else
                 f"no continuation: {law.identity_note}. This is the case §3.5 names an expression "
                 f"for — the value is RE-EVALUATED from a basis, never continued")))

    # ── E2 · operands and roles ───────────────────────────────────────────────────────────────
    #
    # The reader already refused duplicate roles and dangling family references. What is left is the
    # one check that needs the VOCABULARY: does the constructor admit each operand's governed value
    # domain? `admits_operand` is the law's own statement and is reused rather than reworded.
    #
    # **ARITY IS NOT CHECKED, AND THE REASON IS A MISSING FACT, NOT AN OVERSIGHT.** No law in
    # `foundation` states how many operands it takes — `operand_domains` is a domain set, not a
    # signature — so the operand COUNT has nothing to be checked against. That is reported in the note
    # rather than replaced by a guess: a resolver that assumed arity 1 because today's laws are unary
    # would be authoring the vocabulary.
    domain_problems: list[str] = []
    for o in expr.operands:
        fam = families.get(o.family_id)
        if fam is None:                                     # pragma: no cover - refused at read
            raise ExpressionResolutionRefusal(
                f"{subject}: operand role {o.role!r} names family {o.family_id!r}, which was not "
                f"supplied to this resolver.")
        domain = fam.body.get("value_domain")
        if not isinstance(domain, str) or not domain:
            domain_problems.append(
                f"role {o.role!r}: family {fam.canonical_reference!r} declares no value_domain, so "
                f"the constructor's operand admission cannot be settled")
        elif not law.admits_operand(domain):
            raise ExpressionResolutionRefusal(
                f"{subject}: constructor {law.name} admits operand domains "
                f"{sorted(law.operand_domains)}, and role {o.role!r} is filled by "
                f"{fam.canonical_reference!r}, whose governed value domain is {domain!r}. An operand "
                f"outside the law's admitted domains is not an under-specified expression; it is one "
                f"the cited law does not define.")
    arity_note = ("operand arity is UNCHECKED: no law in this vocabulary states a signature, so there "
                  "is nothing for a count to be checked against")
    if domain_problems:
        e[E2_OPERANDS] = Standing(
            E2_OPERANDS, UNESTABLISHED, None,
            value=expr.operands, note="; ".join(domain_problems) + f". {arity_note}")
    else:
        e[E2_OPERANDS] = Standing(
            E2_OPERANDS, ESTABLISHED, DECLARED, value=expr.operands,
            note=(f"roles {list(expr.roles)}, every operand domain admitted by {law.name}. "
                  f"{arity_note}"))

    # ── E3 · constitutive inner anchors (§3.6) ────────────────────────────────────────────────
    #
    # DECLARED where declared; otherwise ENTAILED from the operands' own constitutive anchors, which is
    # this module's half of the rule the governed layer runs on: declaration is for analytical choices,
    # derivation is for consequences. An expression constituted exactly where its operands are has made
    # no choice to record.
    #
    # **AND WHERE THE OPERANDS DISAGREE THE ENTAILMENT FAILS, rather than picking one.** Two operands at
    # two constitutive anchors leave a real analytical choice — which of them the expression is
    # constituted over, or a third — and UNESTABLISHED is the correct report. Choosing the first would
    # make the identity of the expression depend on declaration order.
    if expr.inner_anchor_tokens:
        resolved = tuple(universe.denote(tok) for tok in expr.inner_anchor_tokens)
        e[E3_INNER_ANCHORS] = Standing(
            E3_INNER_ANCHORS, ESTABLISHED, DECLARED, value=resolved,
            note=(f"declared: {', '.join(str(a) for a in resolved)}. These are where the expression is "
                  f"CONSTITUTED (§3.6) and are identity-bearing; they are NOT a root, and the anchor "
                  f"an expression is EVALUATED at is a property of a request"))
    else:
        operand_tokens = {families[o.family_id].anchor_token for o in expr.operands}
        denoted = {universe.denote(tok) for tok in operand_tokens}
        denoted.discard(None)
        if len(denoted) == 1:
            only = next(iter(denoted))
            e[E3_INNER_ANCHORS] = Standing(
                E3_INNER_ANCHORS, ESTABLISHED, ENTAILED, value=(only,),
                note=(f"none declared; entailed from the operands, which are all constituted at "
                      f"{only}. Synonymous tokens collapse here, because an anchor is a constituent "
                      f"set and not a name"))
        else:
            e[E3_INNER_ANCHORS] = Standing(
                E3_INNER_ANCHORS, UNESTABLISHED, None, value=None,
                note=(f"none declared, and the operands are constituted at {len(denoted)} distinct "
                      f"anchors ({', '.join(sorted(str(a) for a in denoted))}), so nothing is "
                      f"entailed. Which location this expression is constituted over is an analytical "
                      f"choice and is not supplied here"))

    # ── E4 · participation and scope ──────────────────────────────────────────────────────────
    #
    # **ONE RESPONSIBILITY, AND THAT IS THE DEFERRAL AND NOT A SIMPLIFICATION** (ruling 9, 2026-09-28):
    # no applicability / participation / support split in V8-1. Splitting it here would be pre-empting
    # C5's unit with an encoding chosen by whoever got there first — which is exactly the mistake C3's
    # own split had to undo one layer up.
    scope = expr.body.get("scope")
    e[E4_PARTICIPATION] = Standing(
        E4_PARTICIPATION, ESTABLISHED, DECLARED,
        value={"participation": expr.body["participation"], "scope": scope},
        note=("participation declared" + ("; scope declared" if scope else "; no scope declared — "
              "absent and declared-empty are the same fact, and `ecf-1` digests them identically")
              + ". Participation and scope are ONE responsibility here: the C5 applicability / "
                "participation / support split is deferred"))

    # ── E5 · admitted bases — zero, one, or several ───────────────────────────────────────────
    basis = law.state_basis
    if not expr.admitted_bases:
        if basis is None:
            e[E5_ADMITTED_BASES] = Standing(
                E5_ADMITTED_BASES, EXPLICIT_NONE, ENTAILED, value=(),
                note=(f"{law.name} carries no composite basis, so its own sufficient state IS the "
                      f"basis and no external route is needed. A POSITIVE negative: the "
                      f"responsibility is settled, and what it settles is that nothing external "
                      f"applies"))
        else:
            e[E5_ADMITTED_BASES] = Standing(
                E5_ADMITTED_BASES, UNESTABLISHED, None, value=(),
                note=(f"{law.name} requires a composite basis over {list(basis.components)} and this "
                      f"expression admits none. LEGIBLE, NOT A DEFECT: a fully constituted expression "
                      f"may have no admitted establishment route yet, which is why this is not a "
                      f"validity condition. It is not evaluable until one is admitted"))
    else:
        if basis is None:
            raise ExpressionResolutionRefusal(
                f"{subject}: admits {len(expr.admitted_bases)} sufficient basis/bases while its "
                f"constructor {law.name} states no composite basis. There is nothing in the "
                f"vocabulary to check the declared components against, and accepting them would "
                f"license any role set whatsoever — so this fails closed. Either the constructor is "
                f"wrong or the law owes a `state_basis`.")
        required = tuple(sorted(basis.components))
        for b in expr.admitted_bases:
            _check_basis(subject, expr, b, law, basis, required, families)
        e[E5_ADMITTED_BASES] = Standing(
            E5_ADMITTED_BASES, ESTABLISHED, DECLARED, value=expr.admitted_bases,
            note=(f"{len(expr.admitted_bases)} admitted route(s) "
                  f"{[b.basis_id for b in expr.admitted_bases]}, each filling {list(required)} as "
                  f"{law.name} requires. NOT identity-bearing: admitting or withdrawing a route does "
                  f"not touch Σ(E)"))

    # ── E6 · basis agreement ──────────────────────────────────────────────────────────────────
    #
    # v8: *alternative lawful bases must agree*. With fewer than two there is no agreement obligation,
    # and that is an EXPLICIT_NONE — a positive negative — rather than a vacuous ESTABLISHED, because
    # "established" would read as "the alternatives were compared".
    if len(expr.admitted_bases) < 2:
        e[E6_BASIS_AGREEMENT] = Standing(
            E6_BASIS_AGREEMENT, EXPLICIT_NONE, ENTAILED, value=None,
            note=(f"{len(expr.admitted_bases)} admitted basis/bases: there are no alternatives for an "
                  f"agreement to hold between. The obligation exists and has nothing to range over"))
    else:
        shapes = {b.basis_id: (b.component_laws, b.requires_common_participation)
                  for b in expr.admitted_bases}
        distinct = set(shapes.values())
        if len(distinct) != 1:
            raise ExpressionResolutionRefusal(
                f"{subject}: its admitted bases do not agree — {shapes}. v8 allows more than one "
                f"sufficient basis for one expression and requires that alternative lawful bases "
                f"AGREE; two routes stating different component laws or different participation "
                f"requirements are not alternatives, they are a contradiction in the declaration.")
        differing_roles = sorted({
            role for role in expr.admitted_bases[0].component_laws
            if len({_role_family(b, role) for b in expr.admitted_bases}) > 1})
        e[E6_BASIS_AGREEMENT] = Standing(
            E6_BASIS_AGREEMENT, ESTABLISHED, ENTAILED, value=tuple(sorted(distinct))[0],
            note=(f"{len(expr.admitted_bases)} alternatives agree on component laws and on the "
                  f"participation requirement"
                  + (f". THE RESIDUE IS NOT ADJUDICATED: roles {differing_roles} are filled by "
                     f"DIFFERENT families across the alternatives, and whether two families are "
                     f"interchangeable in one role is exactly the `governed equivalence` question v8 "
                     f"leaves undefined. {GOVERNED_EQUIVALENCE_ERRATA}"
                     if differing_roles else
                     ". Every role is filled by the same family in every alternative, so no "
                     "equivalence judgment is needed")))

    # ── E7 · identity-bearing parameters ──────────────────────────────────────────────────────
    params = expr.body.get("parameters") or {}
    missing = [p for p in law.required_parameters if p not in params]
    if missing:
        e[E7_PARAMETERS] = Standing(
            E7_PARAMETERS, UNESTABLISHED, None, value=params,
            note=(f"{law.name} requires {list(law.required_parameters)} and "
                  f"{sorted(missing)} is/are not supplied. Identity-bearing and therefore a VALIDITY "
                  f"problem: an expression whose individuating parameters are unsettled cannot claim "
                  f"to be an established expression, and no default is invented to satisfy the check"))
    elif law.required_parameters:
        e[E7_PARAMETERS] = Standing(
            E7_PARAMETERS, ESTABLISHED, DECLARED, value=params,
            note=f"{law.name} requires {list(law.required_parameters)}; all supplied")
    else:
        e[E7_PARAMETERS] = Standing(
            E7_PARAMETERS, EXPLICIT_NONE, ENTAILED, value=params,
            note=(f"{law.name} requires no identity-bearing parameters"
                  + (f"; the declaration carries {sorted(params)} anyway, which is inside Σ(E) by "
                     f"derivation and so IS identity-bearing whether the law asked for it or not"
                     if params else "")))

    absent = [r for r in EXPRESSION_RESPONSIBILITIES if r not in e]
    if absent:                                              # pragma: no cover - structural guard
        raise ExpressionResolutionRefusal(
            f"{subject}: resolution is not total; missing {absent}")
    return ExpressionView(expr.expression_id, expr.canonical_reference, e)


def _role_family(b: AdmittedBasis, role: str) -> Optional[str]:
    for c in b.components:
        if c.role == role:
            return c.family_id
    return None


def _check_basis(subject: str, expr: Expression, b: AdmittedBasis, law: fdn.FoundationLaw,
                 basis: fdn.StateBasis, required: tuple, families: Mapping[str, NativeFamily]) -> None:
    """One admitted basis, against the constructor law's own `state_basis`.

    **THREE CHECKS, AND ONE NAMED LIMIT.**

    1. **Coverage.** The basis must fill exactly the component laws the constructor requires — no
       fewer (a partial basis determines nothing) and no more (a component the law does not require is
       not part of the route it named).
    2. **The participation requirement must agree with the law's.** `StateBasis
       .requires_common_participation` is what the LAW demands of any basis; the declaration states what
       THIS route was established under. §11.5.2's word is MATCHING — a SUM and a COUNT over different
       contributions are individually valid and jointly meaningless — so a route claiming the weaker
       requirement is licensing exactly the pairing the law forbids.
    3. **Continuation congruence.** Each component family must declare a continuation law equal to the
       component law's own `entails_continuation`.
    4. **And where the route requires common participation, the component families must DECLARE THE
       SAME PARTICIPATION.** This is §11.5.2's word MATCHING made executable, and it is checkable from
       the bytes: two families whose declared participation differs did not range over the same
       contributions, so their quotient is a mean of nothing. A route that asserted
       `requires_common_participation` while its components disagreed would be carrying the flag that
       forbids the pairing and the pairing.

    **AND THE LIMIT, STATED RATHER THAN PAPERED OVER: check 3 CANNOT DISTINGUISH TWO COMPONENT LAWS
    THAT ENTAIL THE SAME CONTINUATION.** `SUM` and `COUNT` both entail `SUM`, so a family whose target
    is a count and one whose target is a total are indistinguishable here. The missing fact is in the
    FAMILY declaration, not in this module: a family declares its `target` as prose and its
    `continuation` as a citation, and never names the law its own values are FORMED by. Checking the
    role properly needs that fact; inventing it here would make an expression resolver the author of
    the family contract. **Reported as a repo obligation, not filled.**"""
    if b.component_laws != required:
        raise ExpressionResolutionRefusal(
            f"{subject}: basis {b.basis_id!r} fills component laws {list(b.component_laws)}, and "
            f"constructor {law.name} requires exactly {list(required)} ({basis.note}). A basis that "
            f"does not cover the required components determines nothing, and one that covers more is "
            f"not the route the law named.")
    if b.requires_common_participation != basis.requires_common_participation:
        raise ExpressionResolutionRefusal(
            f"{subject}: basis {b.basis_id!r} declares requires_common_participation="
            f"{b.requires_common_participation} while {law.name}'s own basis requires "
            f"{basis.requires_common_participation} ({basis.note}). The law's requirement is not a "
            f"default a declaration may relax.")
    constructor = dict(expr.body["constructor"])
    for c in b.components:
        try:
            component_law = fdn.resolve(fdn.LawCitation(
                constructor["vocabulary"], constructor["version"], c.role))
        except fdn.UnknownFoundationLaw as exc:
            raise ExpressionResolutionRefusal(
                f"{subject}: basis {b.basis_id!r} names component role {c.role!r}, which is not a law "
                f"in the constructor's own vocabulary: {exc}") from exc
        fam = families[c.family_id]
        declared = _declared_continuation_law(fam)
        expected = component_law.entails_continuation
        if declared != expected:
            raise ExpressionResolutionRefusal(
                f"{subject}: basis {b.basis_id!r} fills role {c.role!r} with family "
                f"{fam.canonical_reference!r}, which declares continuation {declared!r}. Values formed "
                f"by {component_law.name} continue under {expected!r}, so this family's own law cannot "
                f"be supplying that component. (This check is CONTINUATION CONGRUENCE and cannot "
                f"distinguish two component laws that entail the same continuation — see the module "
                f"note. It is a necessary condition, not a sufficient one.)")

    if b.requires_common_participation:
        declared_participation = {
            families[c.family_id].body.get("participation") for c in b.components}
        if len(declared_participation) != 1:
            detail = ", ".join(
                f"{families[c.family_id].canonical_reference!r}: "
                f"{families[c.family_id].body.get('participation')!r}" for c in b.components)
            raise ExpressionResolutionRefusal(
                f"{subject}: basis {b.basis_id!r} declares requires_common_participation=True and its "
                f"components declare DIFFERENT participation ({detail}). {basis.note}. The word doing "
                f"the work is MATCHING: components that ranged over different contributions are "
                f"individually valid and jointly meaningless, and a route asserting the requirement "
                f"while failing it carries both the prohibition and the thing prohibited.")


# ── succession ───────────────────────────────────────────────────────────────────────────────────
@dataclass(frozen=True)
class Succession:
    """Whether a change to an expression's declaration minted a successor."""

    verdict: str
    #: The `ecf-1` payload keys that differ. Empty exactly when the verdict is `SAME_EXPRESSION`.
    changed: tuple[str, ...]
    note: str


def succession(before: Expression, before_universe: Universe,
               after: Expression, after_universe: Universe) -> Succession:
    """**§7.3's succession rule, implemented cleanly and CONSERVATIVELY** (ruling 6, 2026-09-28).

    The rule: *where an identity-bearing expression constituent changes, mint a successor unless an
    already-governed explicit equivalence mechanism genuinely supplies the answer.* There is no such
    mechanism in this build and `governed equivalence` is undefined in v8, so the second clause never
    fires and this function never says `SAME_EXPRESSION` on the strength of an equivalence it would
    have had to invent. See `GOVERNED_EQUIVALENCE_ERRATA`.

    **IT COMPARES `Σ(E)` PAYLOADS, NOT DECLARATIONS**, which is what makes the negative cases true by
    construction rather than by enumeration: admitting a second sufficient basis, withdrawing one,
    adding an alias or re-spelling the canonical reference cannot reach the payload, so they cannot
    mint a successor. That is ruling 4 made executable — `expression identity ≠ one particular
    sufficient basis used to establish it`.

    Both universes are taken because the payload RESOLVES inner anchors, so a change to the world can
    change `Σ(E)` without any expression byte moving — and that is correct: an expression constituted
    over a constituent set is constituted over a different one when the set changes."""
    a = canonical_expression_payload(before, before_universe)
    b = canonical_expression_payload(after, after_universe)
    changed = tuple(sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k)))
    if not changed:
        return Succession(
            SAME_EXPRESSION, (),
            note=("Σ(E) is unchanged, so this is the same expression. Anything that differs between "
                  "these two declarations is outside identity by decision — the admitted bases, the "
                  "references and the aliases are all governed and auditable through publication "
                  "history, and none of them is constitutive"))
    return Succession(
        SUCCESSOR_REQUIRED, changed,
        note=(f"Σ(E) differs at {list(changed)}, so §7.3 mints a SUCCESSOR expression with a new "
              f"expression_id. NO EQUIVALENCE ESCAPE IS TAKEN: {GOVERNED_EQUIVALENCE_ERRATA}"))


def render(view: ExpressionView) -> str:
    """A human-readable total view. The point of the format is that nothing can be absent."""
    lines = [f"Law(E) — {view.canonical_reference}  [{view.expression_id}]  scheme {ECF1}"]
    width = max(len(r) for r in EXPRESSION_RESPONSIBILITIES)
    for r in EXPRESSION_RESPONSIBILITIES:
        s = view.entries[r]
        prov = f" ({s.provenance})" if s.provenance else ""
        lines.append(f"  {r:<{width}}  {s.standing}{prov}")
        if s.note:
            lines.append(f"  {'':<{width}}    · {s.note}")
    problems = view.validity_problems
    lines.append(f"  VALID: {'yes' if not problems else 'NO — ' + '; '.join(problems)}")
    lines.append(f"  EVALUABLE: {'yes' if view.establishable else 'no — no admitted basis'}")
    return "\n".join(lines)


def resolve_all_expressions(pub: Any) -> dict:
    """Every expression's total view in a native publication, keyed by `expression_id`."""
    families = {f.family_id: f for f in pub.families}
    return {x.expression_id: resolve_expression(x, pub.universe(x.universe_reference), families)
            for x in pub.expressions}
