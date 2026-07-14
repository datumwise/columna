# CP-M1 — Manuals alignment WP, design checkpoint (before content edits)

Branch `wp-manuals-alignment`. Per the brief, CP-M1 delivers: docs/ structure, the example-marking
scheme, the harness design, and one rendered sample of a regenerated Chapter-6 example — with forks
named. **No manual content is edited yet**; the alignment edits + the Chapter-2 rewrite land after
this is ruled and come to CP-M2 as a rendered diff.

## What's built (design, proven)
- **Residency:** the three manuals are committed under `docs/` as uploaded; `docs/README.md` is the
  map. The merge is the publication.
- **The harness** (`docs/tools/regen_examples.py`): extracts every ```frameql query block, runs it
  against the shipped package over a docs fixture Manifold, and rewrites the following
  ```frameql-output block. `--check` (CI) fails on any run error OR output drift. Proven: 3 real
  examples regenerate; `--check` passes clean, and catches both injected drift and a broken query
  (exit 1). "An example that stops parsing fails the manual's build" is literally true.
- **CI:** `.github/workflows/docs.yml` runs `regen_examples.py --check` on `docs/**`. **Deploy-path
  finding (verified, clean):** `website.yml` triggers only on `apps/website/**` (+ its own file), so
  publishing `docs/**` does **not** trigger a site deploy. No finding to escalate.
- **Sample:** `docs/tools/SAMPLE_regeneration.md` — three executable examples in the shipped grammar,
  machine-regenerated (per-region revenue → serve; profit map → serve; and `mean(revenue) @ region`
  unpinned → **clarify `input_anchor_ambiguous`**, exercising the WP-OF1 vocabulary end to end).

## Forks — for ruling
- **M1-a · docs/ structure.** Proposed: **flat manual files** (`docs/*.md`) + `docs/tools/` for the
  harness. Alternative: per-manual directories. Flat keeps the eventual site "Read it" links simple
  (one URL per manual) and there are only three files. *Rec: flat.*
- **M1-b · example-marking scheme.** Implemented: **fenced info-strings** — a ```frameql query block
  immediately followed by a ```frameql-output block. Alternative: sentinel HTML comments
  (`<!-- frameql:run -->`). Fenced blocks render as code everywhere, need no HTML, and are trivially
  machine-parseable. *Rec: fenced info-strings.*
- **M1-c · docs fixture Manifold.** Implemented: a **docs-local `finance` fixture** (small Manifold +
  in-memory data in the harness). Alternative: reuse the shipped demo Manifold. The docs-local fixture
  lets the manual keep its readable `finance`/`revenue`/`cost` vocabulary and stays independent of
  demo-data changes. *Rec: docs-local (may grow a `product` fixture for the product-manifold examples).*
- **M1-d · the executable subset (the load-bearing finding).** Chapter 6 has 14 examples; **most use
  clauses the shipped envelope grammar does not have** — `WHERE` (6.8), `HAVING` (6.9), `ORDER BY` +
  `LIMIT ... PER` (6.10), `WITH` macros/allocation (6.12, 6.14), bracket filters (6.7), scans with
  `reset`/`step` (6.11, 6.13). The shipped grammar is `columns @ anchor` only. So the **executable
  set is the subset expressible in the shipped grammar** (≈ 6.1–6.6: aggregation, multi-metric,
  composite reduction via inner `@`, `mean` with input anchor, maps, ratios). Options for the rest:
  - **(i)** mark them **[ROADMAP]/[SCHEDULED]** in the honest-hatching idiom and do **not** execute
    them (they document a language that grows by ruling — ADR-035 D1) — *recommended*;
  - **(ii)** move the unshipped-clause examples into the historical/lineage appendix beside the
    Coframe canonical form;
  - **(iii)** cut them.
  This ruling sets how much of Chapter 6 is executable-regenerated vs marked. *Rec: (i).* Either way,
  only the executable subset carries ```frameql-output blocks; the marked ones carry a status tag.

## Adjacent finding (not a fork)
- **Wire-strings coverage gap, visible in the sample:** `input_anchor_ambiguous` has no friendly
  string in the site's `wire_strings.json` (already logged in `wp_onramp_explorer_scope_stub.md`).
  The harness surfaces the raw reason; the on-ramp+Explorer WP owns the coverage gate. No action here.

## Not done (post-CP-M1, gated)
Watermarks → ADR-035; Appendix B concordance; the Chapter-26 status-mark table + head-notes; the
Frame-QL Chapter 2 rewrite (new prose → CP-M2 for Huayin's edit) + Chapter 6 tagging/regeneration; the
Coframe canonical form → lineage appendix. All land after M1-a…d are ruled, and arrive at CP-M2 as a
rendered diff with the harness green in CI and the worksheet §5 acceptance checked item by item.
