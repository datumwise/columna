# v0.7.8 worklist (items surfaced during WP-0, deferred to preserve the zero-change freeze)

Source: WP-0 acceptance review. None of these may be fixed inside WP-0's branch; all are
behavior-touching and belong to the next library version bump.

1. **parser.py:226 — F821, `Optional` undefined.** Annotation-only, masked by
   `from __future__ import annotations`; no runtime NameError today, but breaks
   `typing.get_type_hints(parse_predicate)`. Fix: import `Optional` (or drop the annotation).
   Relevant before WP-3 (authoring introspection may walk annotations).
2. **Unused-import / dead-local cruft sweep** (config-ignored in WP-0, reported by ruff):
   - `disclosure.py:27` unused `dataclasses.field`
   - `engine.py:19,21,24` unused `dataclasses.field`, `math`, `.model.{SKETCH,ADDITIVE,HOLISTIC}`;
     `:93` F541 f-string without placeholder
   - `model.py:170` unused local `known_cols`
   - `parser.py:26` unused `.model.{ADDITIVE,SKETCH,HOLISTIC}`
   After the sweep, tighten the corresponding per-file-ignores back out of pyproject.
3. **`region_label` parity** — RESOLVED in WP-0 micro follow-up (added to `benchmark.cml`,
   structural parity test added). Listed here only so the v0.7.8 changelog credits the find.
4. Consider promoting the WP-0 infra guards (byte-identical `.cml`, structural parity) into the
   documented test taxonomy in `tests/README` when one is written.

## Surfaced during WP-2.2 (deferred; do not implement in this line)

5. **[Option B] Realizability-checked clarify alternatives + union/side-by-side as a first-class
   resolution.** Today a co-anchoring clarify (`revenue / level.last`) names universe pins whose
   substitution honestly *refuses* (the other operand is out-of-domain), so the clarify→serve
   round-trip only completes by reformulating into separate columns (WP-2.2 acceptance #4, hop 2).
   The engine-level fix is to (a) mark each alternative with whether it actually *realizes* into a
   served/disclosed answer, and (b) make the union / side-by-side over the shared sub-population a
   named resolution the planner can offer directly — i.e. Option A's cross-universe confinement
   (ADR-032 open-question 2, Option B), with the resolution-time coverage disclosure of ADR-031 D13.
   Ruled during WP-2.2 (A2+): the wire adapter stays faithful and never synthesizes alternatives, so
   this belongs in the engine, not the surface.

6. **[contract-v2] `coverage` → `denominator_population` code coarseness.** The normative wire table
   (WP-2.2) maps the engine `coverage` category to the single code `denominator_population`. That
   conflates distinct coverage facts (population divergence vs. a rate's denominator population vs.
   an as-of coverage gap). The table is normative and intentionally coarse for v1 (our authorship);
   a finer split is a wire-contract v2 concern, tracked here so the coarseness is a decision on
   record, not an oversight.
