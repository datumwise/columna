# apps/demo-endpoint-vercel — the read-only Columna demo endpoint (Vercel)

Powers **Exhibit B's live fool-it surface** on datumwise.ai. A lightweight Vercel serverless
function that serves **real, shipped-package wire** for the packaged `benchmark` demo Manifold.

## Why not run the engine here?

The full engine needs `polars` + `pyarrow` (153 MB) + `duckdb`, which exceeds Vercel's **250 MB**
serverless unzipped limit. So instead of faking anything, we **capture genuine wire at build time**
by running the actual package (`scripts/generate.py` → `_wire/precomputed.json`) and serve it. Every
byte returned is exactly what `columna-server`'s Python API produces.

The fool-it surface is a measure name templated into `"<name> @ store, day"` — a **finite, fully
covered** space:

| input                              | response                                                        |
|------------------------------------|-----------------------------------------------------------------|
| a captured query (seed / measure)  | that exact real wire                                            |
| a single unknown measure name      | the engine's real `unknown column '<token>'` refusal (echoed)   |
| SQL / an envelope violation        | the real Frame-QL syntax-error wire (vendored parser)           |
| anything else uncovered            | an honest `not_precomputed` error — **never a fabricated number**|

Arbitrary-query *compute* (any Frame-QL, live) is the **Fly upgrade** — this endpoint is the
"Vercel first" step. Swapping backends later = changing one URL in the site.

## API

```
POST /api/query   {"frameql": "revenue @ store, day", "universe": null}  -> disclosure wire (JSON)
GET  /api/query                                                          -> {ok, contract, measures}
GET  /healthz                                                            -> ok
```

CORS is scoped to `datumwise.ai`, `*.vercel.app`, and `localhost`. Read-only; no token; no write path.

## Regenerate the captured wire (on any package bump)

```bash
../../.venv/bin/python scripts/generate.py   # runs the real engine; drift-guarded by pinned versions in meta
```

## Deploy

```bash
vercel deploy --prod          # linked to the datumwise team; its own project, decoupled from the site
```
