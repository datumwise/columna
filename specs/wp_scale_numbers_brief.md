# WP — Indicative scale numbers (fresh-session brief)

**Routed to a fresh session** (Huayin, 2026-07-14), same reasoning as the manuals part-2: a real
scaling run + write-up deserves a clean context. This file + the transcript are the complete handoff.

## Governing rule (verbatim, survives everything)
**NOTHING PUBLISHES under this WP.** The harness lives in `scripts/`; the **numbers document comes to
Huayin as a report, NOT a commit to any public-rendering path** (`docs/**`, `apps/website/**`). Huayin
decides if and where a sentence ever appears. The methodology *is* the deliverable — an overhead
number measured against the wrong baseline is exactly the misleading figure Columna exists to prevent.

## Original Phase-3 spec (verbatim, from the pre-launch integrity WP brief §Phase 3)
> **Phase 3 — Indicative scale numbers (OPTIONAL, read-only, no publication).** Generate a synthetic
> warehouse at ~10M and ~100M fact rows in the demo's shape; time `resolve` for a representative query
> set (additive rollup, ordered-monoid transport, holistic recompute, sketch path) hot and cold;
> report the numbers and the observed memory high-water mark to Huayin as a note. Purpose: the site
> currently makes no scale statement, and the first serious evaluator will ask; Huayin decides if and
> where a sentence appears. Nothing publishes under this WP.

**Reconciliation (Huayin):** the ratified methodology below *supersedes the spec where they differ in
analytical shape* (the backend-vs-in-engine decomposition and the named hypothesis are additions the
original lacked; the five-shape query set subsumes its four — **keep the "holistic recompute" shape
explicitly**). The spec's strictures survive intact where stricter: **hot and cold, the 10⁸ point,
report-as-note, nothing publishes.**

## Ratified methodology
**The question a serious evaluator asks:** "Your engine adds a correctness layer above the backend —
what does that cost?" So decompose each `resolve`'s wall-clock into:
- **backend-delivery time** — the single-table group-bys / distinct-maps the connector issues (any
  tool pays this), and
- **in-engine time** — transport + planning + hazard/disclosure (this is *the overhead*).
Report the overhead as both absolute ms and a fraction of total.

**Named hypothesis (to TEST, never assert):** overhead scales with *distinct keys at the target
grain*, not fact rows — so as data grows, the overhead *fraction* shrinks. If the numbers say
otherwise, the document says otherwise.

## Query set — the five shapes (over the demo/benchmark Manifold)
Covers the spec's four + the co-anchored ratio. Concrete targets on `benchmark.cml`:
1. **Additive rollup** — `revenue @ region` (sum, VALUE witness, transported store→region along a
   functional edge).
2. **Ordered-monoid transport** — `level.last @ region` (the semi-additive stock's `last`: ORDERED_W
   witness, carries a day witness; the B-anchor case).
3. **Holistic recompute** — `med_amount @ region` (median: non-monoid, recompute-from-base at the
   target grain). *Keep this one explicitly — the spec named it and the ratio-focused list didn't.*
4. **Sketch path** — `visitors @ cal.quarter` (distinct via HLL: SKETCH witness + merge).
5. **Co-anchored ratio** — `revenue / orders @ region` (the map/co-anchor path; the methodology's
   addition).

## Scales & runs
- **Row scale:** 10⁴ · 10⁵ · 10⁶ · 10⁷ · 10⁸ fact rows (the spec's 10M=10⁷ and 100M=10⁸ are the
  anchor points; the smaller scales draw the curve). **Extend to 10⁸ if the machine allows; report the
  actual ceiling reached either way.**
- **Hot AND cold** per (query, scale): **cold** = fresh engine, cache miss, backend hit — **the honest
  headline**; **hot** = second `resolve`, cache hit. **Caveat, stated plainly:** the current "cache"
  is a trivial identical-hit dict, not the real aggregate-navigating Cacher, so hot numbers flatter a
  capability that isn't built yet — cold is what a fresh query actually costs today.
- **Hypothesis-isolating sweep:** at **fixed fact rows** (pick a mid scale that runs fast, e.g. 10⁷),
  **vary distinct-key cardinality at the target grain across 10²–10⁶** and measure in-engine vs
  backend time. This *tests* "overhead scales with keys, not rows" directly instead of inferring it
  from the row-scale curve.
- **Memory:** report the peak high-water mark per point (`resource.getrusage(RUSAGE_SELF).ru_maxrss`
  and/or `tracemalloc`).

## Hygiene (reproducibility)
- **N ≥ 5 repeats** per point; report **median and spread** (IQR or min–max), not a single number.
- **Seeded** synthetic generation (fixed seed; deterministic warehouse per scale).
- The document **opens with the exact environment** — machine (CPU, RAM), OS, Python / DuckDB / Polars
  / columna-core versions, the seed — so the run reproduces.

## Deliverables
- **Harness → `scripts/`** (committable): a seeded synthetic-warehouse generator (in the demo's shape)
  + the timing driver (per-shape, per-scale, hot/cold, N repeats, the key-cardinality sweep, memory
  high-water, backend-vs-in-engine decomposition). Instrument the connector to attribute backend time
  (the engine already exposes `fetch_count`/`stats`; add timing around the `deliver_*` calls).
- **Numbers document → a REPORT to Huayin** (markdown): environment header, the row-scale table
  (hot/cold, decomposed, memory, median+spread), the key-cardinality sweep table, and a plain reading
  of whether the hypothesis held — with honest caveats (single machine, DuckDB backend, synthetic
  data, these queries, the trivial-dict-cache note). **NOT committed to any public-rendering path.**

## Method notes for the runner
- Use `ManifoldServer` / the engine's `resolve` directly (not the MCP wire) to time the analytical
  path cleanly; the demo/benchmark Manifold is the shape.
- "Cold" must be a genuinely fresh engine (new `ColumnEngine`, empty cache, and — for a fair backend
  measurement — a warehouse the OS page cache isn't holding hot from generation; note this limitation
  if it can't be fully controlled on a single box).
- Backend-vs-in-engine: wrap the connector's `deliver_*` methods with a timer; in-engine = total −
  Σ(deliver). Sketch-path publish (`publish_witnesses`) is backend+engine build cost — measure it
  separately and say which column of the table it lands in.
