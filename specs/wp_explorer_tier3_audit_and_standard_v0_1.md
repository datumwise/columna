# WP Explorer Tier 3 — the audit and the standard (v0.1)

> **WITHDRAWN — 2026-07-18 (Huayin's call). Retired, not deleted.** The interactive Explorer tier-3 WP
> is cancelled: the Manifold spec is the sufficient expression of a manifold's content; visualization
> adds image, not understanding; and this charter's marketing job was absorbed by the `/case` section.
> A SUCCESSOR is chartered — **the Universe Visual** (a static, generated Figure 1 from `describe`;
> "visualization rejected as machinery, accepted as Figure 1"): see
> `specs/universe_visual_design_brief_v0_1.md`. This document remains a **historical record**; its
> demo-content findings (a demo declaring 0 asserts / 0 hierarchies / no descriptions, badging almost
> nothing) were **closed by the Cascadia case-demo WP** — real hierarchies, descriptions, an assert,
> and verdicts now exist. The audit below is preserved unchanged for the record.

Scoping input for the Explorer rebuild. Ruled by Huayin; audited at the design desk
against main's describe surfaces and the shipped component.

## Huayin's standard (the acceptance bar for every increment)

1. **Complete model of the data** — complete coverage of ALL information about the
   substance of the data (not forms). Every piece a Manifold carries, visible.
2. **Aiming for the best UI** — navigation, presentation, and visualization.
   It is worth the effort: the Explorer is THE eye-catching piece, with the biggest
   marketing impact of any single surface.

## The audit — Manifold information, piece by piece, vs the shipped Explorer

| Manifold information (the substance, layer by layer) | In Explorer? | How visualized |
|---|---|---|
| The atlas — levels (10, base flags) | ABSENT | — |
| The atlas — functional edges (5, frm→to, named lineages: the FD-DAG) | ABSENT | — |
| Hierarchies (declared rollups + edge verdicts) | ABSENT | — (demo also declares none) |
| Universe: name, base dims, predicate | yes | text lines on card |
| Universe: basis + absence semantics | yes | text |
| Universe: basis License + verdict | yes | verdict badge + license text |
| Measure: name, family members, universe | yes | card header + member list |
| Measure: B-anchor bars (e.g. level.sum BLOCKED{calendar}) | ABSENT | — (lives in describe_measure, never fetched) |
| Measure: operator properties (monoid, linear, needs-order) | ABSENT | — |
| Measure: V-anchor grain, M-anchor mechanism, dtype, provenance | ABSENT | — |
| Measure: licenses (fertility per-lineage, with verdicts) | partial | one license badge; per-lineage detail absent |
| Derived: formula, resolution anchor, denotation flag, members | yes | card with formula text |
| Asserts (predicates, License, verdict) | ABSENT | — (component has no section; demo declares zero) |
| Published scope / cuts / attributions | partial | static line; no structured cut rendering |
| The triad (defined as / tested / show me) + copy-as-query | yes | labelled triad per card |

## The three diagnoses

1. **Depth gap** — the component binds `describe_manifold` only and never fetches
   `describe_measure`; the entire measure-detail layer (bars, operator signatures,
   anchors, provenance, per-lineage licenses) is invisible.
2. **Demo-content gap** — the demo manifold declares no asserts, no hierarchies, no
   fertility; the verdict machinery has almost nothing real to wear.
3. **Geometry gap** — the Manifold is a geometric object (an atlas of levels under a
   DAG of functional edges; universes as regions; measures pinned to home grains; bars
   as marked crossings) and the Explorer renders none of the geometry. Cards-with-text
   is the right idiom for licenses and formulas; it is the wrong idiom for an atlas.

## Design-gate requirements (deliverable 1, before any build)

The proposal brings, for Huayin's ratification:

- **(a) Information architecture** — how ALL of the table above is organized. Evaluate
  the atlas-as-navigation-spine concept (the FD-DAG as the Explorer's home: levels as
  nodes, edges with lineage labels, universes as regions, bars as marked crossings,
  hierarchies visible, every element click-through to detail) but propose what you
  conclude is best.
- **(b) Navigation model** — atlas ↔ cards ↔ per-measure drill-down (fed by
  `describe_measure`, embedded at build time; the site stays static), search, and
  deep-linkable routes per object (shareable URLs are marketing surface).
- **(c) Visual direction** — rendered mockups/screenshots Huayin can SEE, not
  descriptions. Consult the frontend-design skill. State the rendering approach and how
  interactivity degrades gracefully.
- **(d) Demo-enrichment plan** — declare real ASSERTs, a hierarchy, and a provable
  fertility in the demo manifold so verdicts populate genuinely; include the seeded-gap
  option (a store dark for a day → `incomplete_data` live, the ratified [D3] string
  finally ships). One recapture; Huayin's checkpoint with the seeded-number diff.
- **(e) Increment plan** — with render-verification screenshots at every checkpoint.

## Standing laws, extended for this WP

- Portability extends to the describe FAMILY: the component binds `describe_manifold`
  + `describe_measure` artifacts — still zero site imports, zero site coupling. Any
  competitor explorer uses the same seam; that stays a feature.
- Copy law on every new string.
- Generated query strings emit ENVELOPE syntax; verify the copy-as-query generator is
  fully migrated. Propose copy-as-EXPLAIN beside copy-as-query (EXPLAIN is first-class
  on the wire now).
- This WP lands as its OWN single deploy; the one-motion discipline applies.
- Sequence: design proposal → Huayin's design ratification → build increments →
  the Explorer deploy → the acceptance walk on the finished surface → freeze → launch.
