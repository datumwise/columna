"""
columna_core.governed.migrate — v1 publication + v1 mapping -> a MIGRATION PROPOSAL.

**MIGRATION EVIDENCE IS NOT GOVERNING AUTHORITY** (ruled 2026-09-11). This module reads a v1
artifact and the private mapping that gave it meaning, and produces a PROPOSAL: candidate families,
the facts it can entail, and — the part that matters — an explicit list of the analytical facts that
must be authoritatively established before a v2 publication can exist.

**It never emits a publication.** There is no `--write`, no `--auto`, and no code path here that
produces a `family` declaration ready to publish. That is not a missing feature. A v1 member name and
a `root_evaluator` token are evidence about what someone once realized; treating them as a governed
target specification would re-commit, in a migration tool, the exact defect the migration exists to
remove.

WHAT IT MAY CONCLUDE:
  · that a legacy member is EVIDENCE FOR a family, or evidence for the operand family's own
    continuation under another name — using ToD v7.1's target and succession tests;
  · that a fact is ENTAILED once a law is established (empty fibers, result domains, lineage);
  · that a fact is UNRESOLVED, with the reason and the section that governs it.

WHAT IT MAY NOT CONCLUDE: that a target is governed because a name implies it. `revenue_min` is
evidence that someone realized `min(amount)`; it is not evidence that a governed MIN family was ever
established, nor which of §11.5.1's two COUNT targets `revenue_count` asserts.

The proposal is deliberately longer than a checklist. The number and identity of v2 families are
outcomes of establishment, not migration constants, and a tool that reported "3 questions" would be
optimizing for the shape of an interview rather than for the state of the evidence.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

#: How a legacy member's reducer token relates to the operand family, once classified.
CONTINUATION_OF_OPERAND = "continuation-of-operand"
CANDIDATE_CONSTRUCTED = "candidate-constructed-family"
UNDECIDED = "undecided"


@dataclass(frozen=True)
class Unresolved:
    """One analytical fact that must be authoritatively established. Never a default."""

    subject: str
    question: str
    why_not_derivable: str
    authority: str = ""

    def to_dict(self) -> dict:
        return {"subject": self.subject, "question": self.question,
                "why_not_derivable": self.why_not_derivable, "authority": self.authority}


@dataclass(frozen=True)
class Candidate:
    """A PROPOSED family. Not a declaration: every slot it cannot fill is named, not defaulted."""

    proposed_reference: str
    classification: str
    evidence: dict
    unresolved: tuple = ()

    def to_dict(self) -> dict:
        return {"proposed_reference": self.proposed_reference,
                "classification": self.classification,
                "evidence": self.evidence,
                "unresolved": [u.to_dict() for u in self.unresolved]}


@dataclass(frozen=True)
class MigrationProposal:
    source_ref: str
    evidence: dict = field(default_factory=dict)
    entailed: tuple = ()
    candidates: tuple = ()
    unresolved: tuple = ()

    def to_dict(self) -> dict:
        return {"source_ref": self.source_ref,
                "status": "PROPOSAL — not a publication. Every unresolved fact below requires "
                          "authoritative establishment before a v2 publication can exist.",
                "evidence": self.evidence,
                "entailed_once_law_is_established": list(self.entailed),
                "candidates": [c.to_dict() for c in self.candidates],
                "unresolved": [u.to_dict() for u in self.unresolved]}


#: Legacy reducer token -> the foundation law it is EVIDENCE for. Evidence, not establishment.
_SUGGESTS = {"sum": "SUM", "count": "COUNT", "min": "MIN", "max": "MAX", "mean": "MEAN",
             "avg": "MEAN"}


def propose(v1_publication: Any, v1_mapping: Any) -> MigrationProposal:
    """Read v1 plain-data artifacts and produce a proposal.

    Both arguments are the raw dicts (`json.load` output), deliberately: this module does not import
    the v1 compiler, because a migration tool that could compile v1 would be tempted to trust it."""
    ref = (v1_publication.get("ref") or {})
    source = f"{ref.get('manifold_id')}@{ref.get('version')}"
    decls = ((v1_publication.get("logical") or {}).get("declarations") or [])
    by_kind: dict = {}
    for d in decls:
        by_kind.setdefault(d.get("kind"), []).append(d)

    realizations = v1_mapping.get("realizations") or []
    member_real = {r.get("member_ref"): r for r in realizations if r.get("kind") == "member"}

    measures = by_kind.get("measure", [])
    members = by_kind.get("member", [])
    anchors = by_kind.get("anchor", [])

    evidence = {
        "declared_kinds": {k: len(v) for k, v in sorted(by_kind.items())},
        "member_bodies_byte_identical": len({json.dumps(m.get("body"), sort_keys=True)
                                             for m in members}) == 1 if members else None,
        "root_evaluators": {m.get("member_ref"): m.get("root_evaluator")
                            for m in realizations if m.get("kind") == "member"},
        "realized_endpoints": sorted({
            f"{(r.get('endpoint') or {}).get('table')}.{(r.get('endpoint') or {}).get('column')}"
            for r in realizations if r.get("kind") == "member"}),
        "declared_anchors": {a.get("name"): [c.get("name") for c in
                                             (a.get("body") or {}).get("components") or []]
                             for a in anchors},
    }

    entailed = (
        "empty-fiber behaviour for every family, from its continuation law (§5.2, §6.1.1, §11.5.1)",
        "result value domains, from the cited law and the operand's domain",
        "constructed-family lineage, from formation's parent family_ids (§3.7)",
        "self-sufficiency and re-entry properties, from the cited continuation law",
    )

    unresolved: list = []
    candidates: list = []

    for meas in measures:
        mname = meas.get("name")
        body = meas.get("body") or {}
        mine = [m for m in members if (m.get("body") or {}).get("measure") == mname]
        legacy_anchor = {(m.get("body") or {}).get("anchor") for m in mine}
        tables = {(member_real.get(m.get("name"), {}).get("endpoint") or {}).get("table")
                  for m in mine}

        # ── the operand family ───────────────────────────────────────────────────────────────────
        operand_unresolved = [
            Unresolved(
                subject=f"operand family proposed from measure {mname!r}",
                question=("At what constitutive anchor is this quantity formed, and what is its "
                          "contribution structure — one contribution per analytical point, or "
                          "several resolved by a law?"),
                why_not_derivable=(
                    f"the legacy member anchor {sorted(legacy_anchor)} is NOT definitionally the "
                    f"constitutive intake anchor, and nothing in the publication asserts that it is "
                    f"unique in the realized table {sorted(t for t in tables if t)}. Anchor "
                    f"uniqueness is gate EVIDENCE, which publication deliberately drops. Where the "
                    f"source grain is finer, resolving contributions is analytical law — and in v1 "
                    f"it was supplied silently by `root_evaluator`"),
                authority="ToD v7.1 §2.2 (a physical key does not define analytical standing), §3.7"),
            Unresolved(
                subject=f"operand family proposed from measure {mname!r}",
                question="Does this quantity compose across admitted refinement, and under what law?",
                why_not_derivable=(
                    "a primitive family's continuation is an analytical CHOICE — there is no "
                    "formation law to entail one from. That the v1 mapping realized `sum` is "
                    "evidence about a realization, not an establishment of additivity"),
                authority="ToD v7.1 §5.2, §3.9"),
            Unresolved(
                subject=f"operand family proposed from measure {mname!r}",
                question="What is the participation law — which points and which contributions?",
                why_not_derivable=("§4.2: participation 'is not automatically the set of surviving "
                                   "physical records'. v1 declared none"),
                authority="ToD v7.1 §4.2"),
            Unresolved(
                subject=f"operand family proposed from measure {mname!r}",
                question="What does an eligible point with no observed value denote (Φ)?",
                why_not_derivable="a choice about the kind of quantity (flow vs stock), never a "
                                  "consequence; v1 declared none for this measure",
                authority="fill_rule ruling; ToD v7.1 §4 (exceptional cases)"),
        ]
        candidates.append(Candidate(
            proposed_reference=mname,
            classification="candidate-primitive-family",
            evidence={"legacy_measure_body": body,
                      "legacy_members": [m.get("name") for m in mine]},
            unresolved=tuple(operand_unresolved)))
        unresolved.extend(operand_unresolved)

        # ── each legacy member, CLASSIFIED rather than mapped ─────────────────────────────────────
        for m in mine:
            name = m.get("name")
            real = member_real.get(name) or {}
            token = real.get("root_evaluator")
            suggests = _SUGGESTS.get(token)
            member_unresolved = [
                Unresolved(
                    subject=f"legacy member {name!r}",
                    question=("Is a governed family with this target established at all? The legacy "
                              "name and the private `root_evaluator` are evidence that someone "
                              "realized this reduction; neither establishes a governed target."),
                    why_not_derivable=("ruled 2026-09-11: do not assume MIN/MAX/COUNT targets are "
                                       "governed merely because their legacy names imply them"),
                    authority="ToD v7.1 §4 (target specification)"),
            ]
            classification = UNDECIDED
            if suggests == "SUM":
                classification = UNDECIDED
                member_unresolved.append(Unresolved(
                    subject=f"legacy member {name!r}",
                    question=(f"Is this the operand family {mname!r} CONTINUED under another name, "
                              f"or a distinct constructed SUM family over it?"),
                    why_not_derivable=(
                        "§11.5.1 — 'A named family such as Revenue may already denote the same "
                        "construction; canonicalization can identify them ONLY WHERE IDENTITY AND "
                        "PARTICIPATION AGREE.' v1 declares participation for neither, so the "
                        "condition cannot be evaluated from the artifact. If they agree this member "
                        "is a NAME, not a family, and the number of v2 families drops by one."),
                    authority="ToD v7.1 §11.5.1, §3.9"))
            elif suggests == "COUNT":
                classification = CANDIDATE_CONSTRUCTED
                member_unresolved.append(Unresolved(
                    subject=f"legacy member {name!r}",
                    question=("WHICH count? `count(I)` counts participating analytical points; "
                              "`count(x@I)` counts participation under the operand construction's "
                              "governed rule."),
                    why_not_derivable=(
                        "§11.5.1 calls these 'distinct targets', and the artifact says neither. This "
                        "is the seam P1-10 came through, and the number is the denominator of every "
                        "mean taken over this measure."),
                    authority="ToD v7.1 §11.5.1, §11.5.2"))
            elif suggests in ("MIN", "MAX"):
                classification = CANDIDATE_CONSTRUCTED
                member_unresolved.append(Unresolved(
                    subject=f"legacy member {name!r}",
                    question=("Extrema of WHAT — the source contributions at a point, or the "
                              "established operand values at the constitutive anchor?"),
                    why_not_derivable=(
                        "§3.7: 'A MAX formed from Order Revenue and a MAX formed after Revenue is "
                        "established at Day are different constructions unless a governing "
                        "equivalence proves otherwise.' They coincide only where one contribution "
                        "per point holds, which is a data fact and not a law."),
                    authority="ToD v7.1 §3.7, §11.5.1"))
            elif suggests is None:
                member_unresolved.append(Unresolved(
                    subject=f"legacy member {name!r}",
                    question=f"The mapping's root_evaluator {token!r} matches no known foundation "
                             f"law; what law does this family cite?",
                    why_not_derivable="no vocabulary entry corresponds to the legacy token",
                    authority="foundation vocabulary"))
            candidates.append(Candidate(
                proposed_reference=name,
                classification=classification,
                evidence={"legacy_body": m.get("body"), "root_evaluator": token,
                          "suggests_foundation_law": suggests,
                          "endpoint": real.get("endpoint")},
                unresolved=tuple(member_unresolved)))
            unresolved.extend(member_unresolved)

    unresolved.append(Unresolved(
        subject="every proposed family",
        question="What is the family's admitted domain, and which movements are licensed?",
        why_not_derivable=("v1 declares no movement condition anywhere, and under the settled rule "
                           "absence of a prohibition is UNESTABLISHED, never permission. Nothing "
                           "may be manufactured here for a future hierarchy to execute."),
        authority="ToD v7.1 §4.1"))
    unresolved.append(Unresolved(
        subject="every proposed family",
        question="Who establishes this family's identity-bearing constitution, and when?",
        why_not_derivable=("§4: 'A declaration states a proposed definition. Human ratification "
                           "establishes the declaration's authority in its domain.' A migration tool "
                           "is not a human and does not carry authority across a format break."),
        authority="ToD v7.1 §4"))

    return MigrationProposal(source, evidence, entailed, tuple(candidates), tuple(unresolved))


def render(proposal: MigrationProposal) -> str:
    out = [f"MIGRATION PROPOSAL — {proposal.source_ref}",
           "=" * 78,
           "",
           "THIS IS NOT A PUBLICATION. Every unresolved fact below requires authoritative",
           "establishment. The number and identity of v2 families are outcomes of that process,",
           "not migration constants — and may be fewer than the legacy member count.",
           "",
           "-- EVIDENCE (non-authoritative; seeds proposals only) " + "-" * 24]
    for k, v in proposal.evidence.items():
        out.append(f"  {k}: {json.dumps(v, sort_keys=True)}")
    out += ["", "-- ENTAILED once a law is established (never asked of a human) " + "-" * 15]
    out += [f"  · {e}" for e in proposal.entailed]
    out += ["", f"-- CANDIDATES ({len(proposal.candidates)}) " + "-" * 56]
    for c in proposal.candidates:
        out.append(f"  {c.proposed_reference}   [{c.classification}]")
        for u in c.unresolved:
            out.append(f"      ? {u.question}")
    out += ["", f"-- UNRESOLVED ANALYTICAL FACTS ({len(proposal.unresolved)}) " + "-" * 40]
    for i, u in enumerate(proposal.unresolved, 1):
        out.append(f"  {i:>2}. [{u.subject}]")
        out.append(f"      Q: {u.question}")
        out.append(f"      why not derivable: {u.why_not_derivable}")
        if u.authority:
            out.append(f"      authority: {u.authority}")
    return "\n".join(out)
