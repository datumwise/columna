# apps/demo-endpoint-vercel — RETIRED (P1-32, 2026-09-02)

This surface is **retired**. `index.py` answers every request with `410 Gone` and a retirement
notice. It serves no analytical result, reads no data file, and records no version, contract or
manifold of its own.

## What was here

A read-only Vercel function that replayed **precomputed wire** — real output captured on 2026-07-13
by running columna-core 0.7.8 / columna-server 0.1.0 over the packaged `benchmark` manifold and
committing the result as `_wire/precomputed.json` (6.9 MB, 11 captured queries plus an
unknown-column template). It powered Exhibit B's "live fool-it" box on datumwise.ai. The full engine
could not run on Vercel (polars + pyarrow + duckdb exceed the 250 MB limit), so a capture was served
instead — genuine wire, never a facsimile.

## Why it was retired rather than regenerated

It was built as a **live** surface ("regenerate on any package bump") and then nothing regenerated
it — no CI path, no gate, no freshness check; the only guard it claimed, "drift-guarded by the
recorded versions in meta", was version metadata that nothing read. Fifty-one days later the
committed capture disagreed with the system in every dimension that mattered:

| the capture | the system, 2026-09-02 |
|---|---|
| wire contract `1` | contract `4` |
| `benchmark` manifold | the packaged demo is `cascadia` |
| queries in the terse `<measure> @ <anchor>` form | that form was retired in 0.9.0 — every captured query is now a syntax error |
| six advertised measures | four of them no longer exist |
| `region_label` served as NULL | repaired at the declaration level by P1-18 |
| generator calls `query(..., universe=...)` | no such argument — the generator cannot run at all |

Moving it to the current contract would have been a **re-authoring**, not a regeneration, and it
would have had to answer a canonical language question (what replaces the query-side `universe=`
pin — OF-4) to resurrect a surface with **no remaining consumer**: the site's client was disabled in
place on 2026-08-25, and the seed file that held this URL was orphaned.

Ruled by Huayin, 2026-09-02: **retire it; do not migrate it.** *"Do not invent current semantics to
preserve a dead demo contract."* So `scripts/generate.py`, `vendor/frameql.py` and
`_wire/precomputed.json` were **deleted**, not updated — a generated artifact must not keep authority
merely by being committed and served. No freshness or determinism gate was added, deliberately:
there is no longer an artifact for one to guard.

## Current Columna behaviour

`pip install columna`, or https://datumwise.ai. Nothing in this directory speaks for the current
system.

## Deploy

```bash
vercel deploy --prod    # its own Vercel project, decoupled from the site
```
