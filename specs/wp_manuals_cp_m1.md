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

## Handoff — the anchor grammar is on `main` (from the anchor-grammar WP)
*(Added 2026-07-16. PR [#33](https://github.com/datumwise/columna/pull/33), merge `4c12a0b`;
independently verified post-merge and blessed by Huayin. This section is the anchor-grammar WP's
merge notification into CP-M2's channel.)*

**What discharged, and what did NOT.** The gate the anchor-grammar WP discharged is the **sequencing
gate** only — the small parser WP landed on `main` **before** the manuals merge, so Chapter 2 now
writes against ruled, shipped grammar. **The CP-M2 approval gate stands UNCHANGED:** the full rendered
diff, Chapter 2's prose for Huayin's edit, and worksheet §5 checked line by line — all before anything
merges. Sequencing cleared; approval is still Huayin's, unmoved.

**Chapter 2 documents shipped law only** (the §2c discipline). The capture's §2c universe-resolution
material — one-expression/one-universe, the expression law, the frame-juxtaposition law, `ON UNIVERSE`
dead in the query grammar, universe-qualified/suffix addressing — is **capture-only, NOT shipped**;
it is the tier-2 WP's scope. Chapter 2 must not document any of it as behavior.

**The shipped grammar Chapter 2 writes against:**
- **Anchor product `*`** is the canonical anchor separator (`revenue @ region*day`), the same operator
  as `UNIVERSE a * b * c`; the system writes `*` everywhere. **One sentence** acknowledges that the
  comma is *accepted on input* — its retirement is a ruled post-launch grammar-hygiene sweep, and the
  manual does **not** date it.
- **Resolution order (STANDING law):** a literal level-name match wins (dotted stored names like the
  demo's `cal.month` are legitimate); otherwise the token splits at the first dot and resolves as
  `family.level`, validated against **edge-derived** membership (level ∈ family iff it touches an edge
  of that lineage). Nothing here is transitional.
- **Leaf-name uniqueness is scoped per universe** (a well-formedness law): within a universe's included
  levels, two distinct levels may not share a leaf name; the same leaf MAY recur across universes.
- **Universe names never appear in anchor position** (disjoint namespaces; populations ride
  `ON UNIVERSE` in definitions).
- **The one bad state** — a single token that could reach two levels (a literal `A.B` whose
  `family.level` split also resolves) — is a well-formedness error, fail closed, both sites named.
- **Bare-unknown pass-through** (the refinement blessed post-merge, finer than the brief drew): a bare,
  non-universe, non-level token is *not* a resolution error — it flows through to the addressability
  (`out_of_universe`) mood, unchanged. Resolution errors are scoped to universe-names and bad
  qualifications only.

**Exact error strings (stable; quote verbatim in examples):**
- universe in anchor → `'transactions' is a universe, not a level: universe names do not appear in anchors; populations ride ON UNIVERSE`
- wrong family → `anchor 'cal.region': level 'region' is not in dimension family 'cal' — it belongs to ['geo']`
- qualified unknown level → `anchor 'geo.nowhere': no level named 'nowhere' — qualify an existing level as family.level, or name a level directly`
- leaf collision → `universe 'sales': levels ['cal.week', 'fiscal.week'] share the leaf name 'week' — leaf names must be unique within a universe; rename one so distinct concepts carry distinct names`
- one bad state → `level 'cal.month' collides with level 'month' in family 'cal': the anchor token 'cal.month' would reach both (a literal level and the family.level split) — rename one`
- duplicate LEVEL → `duplicate LEVEL declaration 'month' — a level name is declared exactly once`

**Behavior delta (Chapter 2 should reflect this, one line):** a universe name in the anchor that
previously produced an accidental `out_of_universe` **refusal** now produces a `frameql_syntax`
**error** on the query-error channel — no new wire reason code, four-mood wire byte-identical.

**Docs-local fixture (M1-c):** the `finance` fixture uses **clean dotless level names from birth** —
no `cal.`-style dotted legacy. Suffix/qualified addressing surfaces only if/when the fixture models
two families sharing a leaf; the bare level name is the expected form.

**Chapter 6** regenerates against this grammar (the executable subset per M1-d); the `*` anchor is the
canonical spelling in every `frameql`/`frameql-output` block.
