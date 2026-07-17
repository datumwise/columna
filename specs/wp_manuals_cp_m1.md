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

---

## CP-M2 Part-2 shipped-law reconciliation — flags for the prose pass (2026-07-17)
Per Huayin's amendment (reconcile the shipped-law delta wherever it touches; flag what resists). Done:
(i) Chapter 1.5 (anchor,universe) — `ON` reconciled to structural resolution / definition-language;
(ii) the empty-bucket/absence rule rewritten to the shipped B3 basis law (events→zero, spine/product→gap
+`incomplete_data`, registry→membership); (iii) Chapter 7 — the missing `cross_universe` outcome added +
key cases annotated with shipped reason codes (`input_anchor_ambiguous`/`co_anchor_ambiguous`,
`non_functional_transport`, `incomplete_data`/`data_gap`, `b_anchor_crossing`); (iv) Appendix B — `ON`
reclassified as definition-language, the envelope markers `@`/`*`/`:` named. **FLAGGED as resisting a
clean §2c-only reconciliation (need the prose pass / ride the broader Coframe→envelope rewrite):**
- **Chapter 1's `SELECT`/`FROM`/`AT` grammar** (incl. line 46's `[ON <universe>]`) is Coframe throughout;
  reconciling `ON` alone leaves Chapter 1 half-envelope, half-Coframe. Should ride the Appendix-A move.
- **Chapter 7's "inform-and-serve" doctrine** names the fourth outcome **`inform`** (ADR-020); the shipped
  wire's fourth mood is **`refuse`**. Renaming throughout is a doctrinal prose call, not mechanical.
- **Appendix B Coframe keywords** (`FROM`/`SELECT`/`AT`/`{...}`) — entangled with the Coframe→envelope
  rewrite; not reconciled here.

## CP-M2 Part-2 session RETIRED (2026-07-17)
**The fresh session handed Part 2 on 2026-07-14 stalled — it produced no commits; `wp-manuals-alignment`
did not advance past `9b061ae`. It is formally CLOSED. Part 1 (`99deb0e`) stands landed, untouched.**
Under CP-3b (Huayin, 2026-07-17) Part 2 is **reassigned to the CP-3b builder** as a parallel track, scoped
**exactly** as specced below (not an invitation to broader manual edits), riding **its own PR on
`wp-manuals-alignment`** (separate gate from the site beat). The **CP-M2 approval gate is UNCHANGED**: the
full rendered Chapter 2 diff comes to Huayin's prose pass before anything merges. No zombie tracks.

## CP-M2 status & fresh-session handoff (2026-07-14)

M1-a…d ruled (Huayin, 2026-07-14): flat · fenced · docs-local (tiny, harness-only, never in a wheel) ·
(i) with the **two-tier mark**. CP-M2 is split; **part 1 is done, part 2 goes to a fresh session**
(Huayin's routing — the prose conditions warrant a clean context; the repo + PR #24 carry the state).

**Part 1 — DONE & pushed** (branch `wp-manuals-alignment`, PR #24; ADR edit on PR #22):
- Watermarks → "reconciled through ADR-035" (all three); reference Appendix B concordance (ADR-033
  App A verbatim); Part VI head-note; Chapter 26 head-note + 26.2–26.9 two-tier marks.
- ADR-035 growth-precedent: tier-one "engine-shipped, surface pending" candidates (WHERE + scan
  clauses) queued (on PR #22).

**Part 2 — REMAINING (the fresh session):**
1. **Fold in Huayin's part-1 wording notes** on the marks (he is skimming the part-1 diff and will
   send them; apply in one pass).
2. **Frame-QL Chapter 2 rewrite** to the shipped envelope grammar — net-new prose, comes to CP-M2 as
   a rendered diff *for Huayin's edit* (copy law). Shape: `columns @ anchor`; label form `name: expr`;
   dotted members; inline `@` input pins (`avg(aov@day) @ month`); the clarifies
   `co_anchor_ambiguous` / `input_anchor_ambiguous`; D1's grow-by-ruling rule stated in-voice.
3. **Chapter 6** — tag the executable subset (≈ 6.1–6.6) as ```frameql / ```frameql-output and
   regenerate via the harness; **two-tier-mark the rest**: WHERE (6.8) + scans (6.11, 6.13) =
   *engine-shipped, surface pending — enters the grammar by ruling, ADR-035 D1 (not a scheduling
   promise)*; HAVING (6.9), LIMIT…PER (6.10), WITH/allocation (6.12, 6.14), bracket-filter (6.7) =
   **[ROADMAP]**.
4. **Fixture growth — APPROVED, scoped** (Huayin, per the M1-c rider): add a `month` level and a small
   `product` fixture to `docs/tools/regen_examples.py`. **Tiny, harness-only, never in a wheel.**
5. **Appendix A** — the Coframe canonical form (Chapter-1.3/1.4 `FROM`/`SELECT`/`AT` ceremony + the
   old Chapter 2) moved to a historical-lineage appendix, with the one paragraph noting which ideas
   the shipped grammar absorbed (per-subexpression anchors) and which were declined (`FROM`/`SELECT`,
   container ceremony; ADR-035 D2). **Lineage appendix reserved for Coframe-form material only.**
6. **First-mention copy law (ratified 2026-07-14):** public surfaces introduce the project as
   **"Columna, by datumwise."** Check the three manuals' title pages + any first-mention sites
   conform — likely a no-op or one line each. **Report, do not improvise wording.**
7. **Acceptance (worksheet §5, checked line by line at CP-M2):** every Chapter-26 construct one mark;
   zero Chapter-6 executable examples that don't run; watermarks cite ADR-035; Appendix B concordance;
   Part VI head-note. Then audit Section E declared CLOSED in the PR; fork registry at zero.

**Gates (UPDATED — naming ruled 2026-07-14: *Columna stays, as-is*).** Merge of PR #24 is now gated on
**CP-M2 approval ONLY**. The naming gate is discharged; **no rename sweep runs** on this branch or
anywhere, and the sweep-ready protocol **stands down** as a standing capability. Flow: full CP-M2
rendered diff for Huayin's edit → CP-M2 approval → merge (= publication). No deploys; `docs/**` does
not trigger the website workflow (verified).
