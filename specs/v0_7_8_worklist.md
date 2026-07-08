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
