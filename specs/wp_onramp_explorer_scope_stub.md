# On-ramp + Explorer WP — scope stub

**Status: stub (not cut).** A placeholder so ruled scope is *inherited, not rediscovered* when this WP
is cut. Items here arrived by ruling elsewhere (ADR-034, ADR-035) and are parked against the WP that
will build them. Cutting the WP starts from this list; nothing below is re-litigated, only scheduled.

The on-ramp motion: `columna init` drafts an **evidence-graded** Manifold; Explorer tier 2 renders the
named surfaces (derived describe objects already ship — WP-B B-5). Both build against the query
surface and the Certificate kernel, which is why the items below ride here.

## Inherited scope — ADR-034 (definition-language, Certificate customers)

**D1 — Core, the Certificate kernel's next customers (built inside this WP).** The kernel shipped in
WP-B (`License`; the four verdicts VERIFIED/CORROBORATED/UNTESTABLE/CONTRADICTED; publish-time
adjudication; fail-closed CONTRADICTED). These three reuse it **unchanged** — same pipeline fertility
runs (declared → math-verify where provable, else data-refute → verdict; CONTRADICTED fails closed at
publish). If any needs a `License`/adjudication schema change, that change is a **checkpoint fork of
this WP**, not a silent extension (ADR-034 Consequences — the kernel's generality claim under test):

- **`ASSERT`** — a declared precondition, adjudicated at publish.
- **`HIERARCHY store -> region` (multi-level chains, verified)** — chains desugar to `EDGE`s; the new
  content is the *verification* (is the edge functional in the data? → verdict). An on-ramp-drafted
  `HIERARCHY` carrying `INFERRED_SAMPLE` means something only because publish-time machinery can
  refutation-test it and stamp CORROBORATED / CONTRADICTED.
- **`UNIVERSE ... BASIS` (registry / spine / product / events)** — typed point-provenance, adjudicated.

**Evidence-grade → verdict mapping (record explicitly when cut, ADR-034 Consequences).** The grades
already in `model.py` (`DECLARED` / `PROVEN` / `INFERRED_SAMPLE` / `INFERRED_DOCS`) are the
declaration's *provenance*; the verdict is its *adjudicated status*. These customers connect the two;
the WP writes the mapping down.

**D2 — Core, small, same motion: `ALIAS`.** "One anchored measure can wear a hundred names"
(metadata-independence essay) has no syntax today. `ALIAS` is communicative metadata by definition
(no legality impact), cheap to parse, visible only where names render — the Explorer. Ships here or the
promise stays prose.

## Inherited scope — ADR-035 (query surface)

- **Depends on the parser promotion** (ADR-035 D3, cut separately as `wp-frameql-promotion`): the
  query surface (`parse_frameql`) lands under core's test regime **before** Explorer tier 2 / on-ramp
  build against it.
- **Wire-strings coverage check (ADR-035 Consequences).** Every reason and code in the *shipped*
  vocabulary must have a friendly string in the demo site's governed `wire_strings.json` **before any
  surface can emit it**. Build this as a test/gate in this WP.
  - *Known gap to close:* `input_anchor_ambiguous` (the unpinned inline-reduction clarify, WP-OF1) has
    no friendly string yet. Nothing surfaces it today; this WP adds the string and the coverage gate
    together so the gap cannot silently reopen. (`wire_strings.json` lives under `apps/website/` —
    out of scope for the specs/core changes that opened this item; it lands with this WP's surface work.)

## Provenance
- ADR-034 D1/D2 → this stub, per Huayin (2026-07-14): "enter the ADR-034 D1/D2 items into the
  on-ramp + Explorer WP's scope stub so they're inherited, not rediscovered."
- ADR-035 Consequences (wire-strings coverage) → this stub, same instruction.
- Not scheduled here: `WITHHOLD`/`ACCESS` (ROADMAP — Pro/enterprise, ADR-034 D3) and
  `INHERITS ... VERSION` (ROADMAP — layered-cache era, ADR-034 D4). Scoping notes only; see the
  manuals status pass (`manuals_alignment_pass_v0_1.md`).
