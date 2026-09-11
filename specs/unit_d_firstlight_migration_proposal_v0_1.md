# Unit D — the `firstlight` migration proposal
## Machine-generated. **This is not a publication.**

**Status:** evidence for authoritative establishment, 2026-09-11.
**Regenerate:**

```
python -c "import json;from columna_core.governed.migrate import propose,render;\
print(render(propose(json.load(open('packages/columna-server/fixtures/firstlight/governed-publication.json')),\
json.load(open('packages/columna-server/fixtures/firstlight/private-core-mapping.json')))))"
```

The v1 artifact is **immutable by its own design** — its producer stage is not byte-reproducible, so
it was produced once and committed, and every downstream guard reads the committed bytes. It is not
edited. What follows is the proposal for a **v2 successor**, which must be authored.

`columna_core.governed.migrate` has no code path that emits a publication, and a test pins that:
`test_the_migration_tool_produces_a_proposal_and_cannot_produce_a_publication`. A legacy member name
and a private `root_evaluator` token are evidence about what someone once realized. Treating them as
a governed target specification would re-commit, inside the migration tool, the exact defect the
migration exists to remove.

**The number and identity of v2 families are outcomes of establishment, not migration constants** —
and may be fewer than the four legacy members, because item 6 below can dissolve one.

---

```
MIGRATION PROPOSAL — firstlight@1.0.0
==============================================================================

THIS IS NOT A PUBLICATION. Every unresolved fact below requires authoritative
establishment. The number and identity of v2 families are outcomes of that process,
not migration constants — and may be fewer than the legacy member count.

-- EVIDENCE (non-authoritative; seeds proposals only) ------------------------
  declared_kinds: {"anchor": 1, "measure": 1, "member": 4, "universe": 1}
  member_bodies_byte_identical: true
  root_evaluators: {"revenue_count": "count", "revenue_max": "max", "revenue_min": "min", "revenue_sum": "sum"}
  realized_endpoints: ["sales_lines.amount"]
  declared_anchors: {"sale_at": ["store", "day"]}

-- ENTAILED once a law is established (never asked of a human) ---------------
  · empty-fiber behaviour for every family, from its continuation law (§5.2, §6.1.1, §11.5.1)
  · result value domains, from the cited law and the operand's domain
  · constructed-family lineage, from formation's parent family_ids (§3.7)
  · self-sufficiency and re-entry properties, from the cited continuation law

-- CANDIDATES (5) --------------------------------------------------------
  revenue   [candidate-primitive-family]
      ? At what constitutive anchor is this quantity formed, and what is its contribution structure — one contribution per analytical point, or several resolved by a law?
      ? Does this quantity compose across admitted refinement, and under what law?
      ? What is the participation law — which points and which contributions?
      ? What does an eligible point with no observed value denote (Φ)?
  revenue_sum   [undecided]
      ? Is a governed family with this target established at all? The legacy name and the private `root_evaluator` are evidence that someone realized this reduction; neither establishes a governed target.
      ? Is this the operand family 'revenue' CONTINUED under another name, or a distinct constructed SUM family over it?
  revenue_count   [candidate-constructed-family]
      ? Is a governed family with this target established at all? The legacy name and the private `root_evaluator` are evidence that someone realized this reduction; neither establishes a governed target.
      ? WHICH count? `count(I)` counts participating analytical points; `count(x@I)` counts participation under the operand construction's governed rule.
  revenue_min   [candidate-constructed-family]
      ? Is a governed family with this target established at all? The legacy name and the private `root_evaluator` are evidence that someone realized this reduction; neither establishes a governed target.
      ? Extrema of WHAT — the source contributions at a point, or the established operand values at the constitutive anchor?
  revenue_max   [candidate-constructed-family]
      ? Is a governed family with this target established at all? The legacy name and the private `root_evaluator` are evidence that someone realized this reduction; neither establishes a governed target.
      ? Extrema of WHAT — the source contributions at a point, or the established operand values at the constitutive anchor?

-- UNRESOLVED ANALYTICAL FACTS (14) ----------------------------------------
   1. [operand family proposed from measure 'revenue']
      Q: At what constitutive anchor is this quantity formed, and what is its contribution structure — one contribution per analytical point, or several resolved by a law?
      why not derivable: the legacy member anchor ['sale_at'] is NOT definitionally the constitutive intake anchor, and nothing in the publication asserts that it is unique in the realized table ['sales_lines']. Anchor uniqueness is gate EVIDENCE, which publication deliberately drops. Where the source grain is finer, resolving contributions is analytical law — and in v1 it was supplied silently by `root_evaluator`
      authority: ToD v7.1 §2.2 (a physical key does not define analytical standing), §3.7
   2. [operand family proposed from measure 'revenue']
      Q: Does this quantity compose across admitted refinement, and under what law?
      why not derivable: a primitive family's continuation is an analytical CHOICE — there is no formation law to entail one from. That the v1 mapping realized `sum` is evidence about a realization, not an establishment of additivity
      authority: ToD v7.1 §5.2, §3.9
   3. [operand family proposed from measure 'revenue']
      Q: What is the participation law — which points and which contributions?
      why not derivable: §4.2: participation 'is not automatically the set of surviving physical records'. v1 declared none
      authority: ToD v7.1 §4.2
   4. [operand family proposed from measure 'revenue']
      Q: What does an eligible point with no observed value denote (Φ)?
      why not derivable: a choice about the kind of quantity (flow vs stock), never a consequence; v1 declared none for this measure
      authority: fill_rule ruling; ToD v7.1 §4 (exceptional cases)
   5. [legacy member 'revenue_sum']
      Q: Is a governed family with this target established at all? The legacy name and the private `root_evaluator` are evidence that someone realized this reduction; neither establishes a governed target.
      why not derivable: ruled 2026-09-11: do not assume MIN/MAX/COUNT targets are governed merely because their legacy names imply them
      authority: ToD v7.1 §4 (target specification)
   6. [legacy member 'revenue_sum']
      Q: Is this the operand family 'revenue' CONTINUED under another name, or a distinct constructed SUM family over it?
      why not derivable: §11.5.1 — 'A named family such as Revenue may already denote the same construction; canonicalization can identify them ONLY WHERE IDENTITY AND PARTICIPATION AGREE.' v1 declares participation for neither, so the condition cannot be evaluated from the artifact. If they agree this member is a NAME, not a family, and the number of v2 families drops by one.
      authority: ToD v7.1 §11.5.1, §3.9
   7. [legacy member 'revenue_count']
      Q: Is a governed family with this target established at all? The legacy name and the private `root_evaluator` are evidence that someone realized this reduction; neither establishes a governed target.
      why not derivable: ruled 2026-09-11: do not assume MIN/MAX/COUNT targets are governed merely because their legacy names imply them
      authority: ToD v7.1 §4 (target specification)
   8. [legacy member 'revenue_count']
      Q: WHICH count? `count(I)` counts participating analytical points; `count(x@I)` counts participation under the operand construction's governed rule.
      why not derivable: §11.5.1 calls these 'distinct targets', and the artifact says neither. This is the seam P1-10 came through, and the number is the denominator of every mean taken over this measure.
      authority: ToD v7.1 §11.5.1, §11.5.2
   9. [legacy member 'revenue_min']
      Q: Is a governed family with this target established at all? The legacy name and the private `root_evaluator` are evidence that someone realized this reduction; neither establishes a governed target.
      why not derivable: ruled 2026-09-11: do not assume MIN/MAX/COUNT targets are governed merely because their legacy names imply them
      authority: ToD v7.1 §4 (target specification)
  10. [legacy member 'revenue_min']
      Q: Extrema of WHAT — the source contributions at a point, or the established operand values at the constitutive anchor?
      why not derivable: §3.7: 'A MAX formed from Order Revenue and a MAX formed after Revenue is established at Day are different constructions unless a governing equivalence proves otherwise.' They coincide only where one contribution per point holds, which is a data fact and not a law.
      authority: ToD v7.1 §3.7, §11.5.1
  11. [legacy member 'revenue_max']
      Q: Is a governed family with this target established at all? The legacy name and the private `root_evaluator` are evidence that someone realized this reduction; neither establishes a governed target.
      why not derivable: ruled 2026-09-11: do not assume MIN/MAX/COUNT targets are governed merely because their legacy names imply them
      authority: ToD v7.1 §4 (target specification)
  12. [legacy member 'revenue_max']
      Q: Extrema of WHAT — the source contributions at a point, or the established operand values at the constitutive anchor?
      why not derivable: §3.7: 'A MAX formed from Order Revenue and a MAX formed after Revenue is established at Day are different constructions unless a governing equivalence proves otherwise.' They coincide only where one contribution per point holds, which is a data fact and not a law.
      authority: ToD v7.1 §3.7, §11.5.1
  13. [every proposed family]
      Q: What is the family's admitted domain, and which movements are licensed?
      why not derivable: v1 declares no movement condition anywhere, and under the settled rule absence of a prohibition is UNESTABLISHED, never permission. Nothing may be manufactured here for a future hierarchy to execute.
      authority: ToD v7.1 §4.1
  14. [every proposed family]
      Q: Who establishes this family's identity-bearing constitution, and when?
      why not derivable: §4: 'A declaration states a proposed definition. Human ratification establishes the declaration's authority in its domain.' A migration tool is not a human and does not carry authority across a format break.
      authority: ToD v7.1 §4
```
