# WP-5.1 checkpoint (c) — build plan (APPROVED 2026-07-11)

Approved by Huayin 2026-07-11. Records the verified query pins, the deployment architecture, and
the rulings that unblock the build. Authority: `CLAUDE_WP5_1.md` → `wp5_1_addendum_v2.md` →
`wp5_1_site_widget_spec.md` (engineering) → `wp5_1_checkpoint_b_exhibit_script_v0_2.md`.

## Rulings (Huayin, 2026-07-11)

1. **Clarify fork → Option A (honest relabel).** The shipped demo Manifold serves `aov`; it does
   not clarify. Exhibit B's live clarify uses the real `sell_through_rate` wedge, labeled
   truthfully ("sell-through rate — revenue over end-of-period inventory"); alternatives render as
   the two populations. The §7 copy hook is softened so it does not claim to be §2's AOV question.
   Adding an AOV-clarifying case is logged **product-side, never site-driven** (invariant #2 holds).
2. **Vercel** for the static site; **Cloudflare** for DNS (assistant token provided out-of-band,
   used inline only, never committed, rotated after wiring).
3. **Superset transcript, generated-only, build-fails-closed.** CI captures the four pinned
   queries + the Q1 round-trip + the unknown-measure ASK by running the shipped PyPI package
   (a superset of `demo --play`'s three moods). Never hand-edited, never committed. Build FAILS if
   generation fails.
4. **Branch** `wp5.1-website` off `main`; PR to follow. Durable `datumwise` write already in place.

Both minor mismatches ratified: render the wire's truth — `disclose` caveat is
`denominator_population / material / info` (not `blocked_reduction/critical`); the fool-it trap
returns `error` ("unknown column"), rendered neutral ("not a mood — plumbing") + the ASK.

## Verified query pins (PyPI columna-core 0.7.8 / columna-server 0.1.0, manifold `benchmark`)

Frozen into `apps/website/src/data/seeded_queries.json`. Every outcome below was produced by
running the query against the installed package on 2026-07-11.

| id | mood | frameql | universe | outcome (verified) |
|----|------|---------|----------|--------------------|
| clarify | clarify | `sell_through_rate: revenue / level.last @ store, day` | — | `clarify`; 2 alternatives `on_universe('store_days')`, `on_universe('transactions')` |
| refuse | refuse | `sell_through_rate: revenue / level.last @ store, day` | `transactions` | `refuse`, `out_of_universe` |
| disclose | disclose | `revenue: revenue, inv: level.last @ store, day` | — | `disclose`; caveat `denominator_population` material/info/coverage |
| serve | serve | `revenue @ region` | — | `serve`, clean |
| fool-it | error→ASK | `<unknown> @ store, day` (placeholder `sell_through_rate`) | — | `error` "unknown column" → widget composes ASK from cached measure index |

Q1 (clarify) and Q3 (refuse) are the same query with/without the universe pin — the pin is exactly
what the clarify offers.

## Deployment architecture

**Endpoint (Fly.io, `demo.datumwise.ai`).** Discovery: `demo --http` binds **loopback-only** when
`COLUMNA_MCP_TOKEN` is unset, and **externally + bearer-required** when set. The engine is not
changed. Therefore: one Fly machine, two processes — `columna-server demo --http 127.0.0.1:8765`
(ungated loopback) behind **nginx** on `0.0.0.0:8080`. nginx is the public face: `limit_req` per-IP
(60 req/min, burst 20 → 429), CORS `Access-Control-Allow-Origin: https://datumwise.ai`, SSE-safe
(`proxy_buffering off`). No bearer token reaches the browser; read-only demo Manifold only;
worst-case abuse = restart. Dockerfile (`python:3.12-slim` + nginx, pinned pip installs) doubles as
the `docker run` quickstart image.

**Site (Vercel, `datumwise.ai`).** Astro static. Browser island speaks MCP streamable-http via
`@modelcontextprotocol/sdk`, asserts `contract_version == "1"` at init → else degrade to the
CI-generated transcript. DNS via Cloudflare: `datumwise.ai` → Vercel, `demo.` → Fly, repo About
homepage → site.

**Integrity (GitHub Actions).** Install columna from PyPI → run the shipped package to generate
`transcript.generated.json` (four pins + round-trip + ASK, plus a literal `demo --play`
cross-check) → `astro build`. Build fails if generation fails. The file is gitignored.

## Sitemap & structure

Pages: Home (§1–§8 argument scroll) · The Thesis · Why · The Atlas · How these documents relate ·
The launch post · Install · (Grain Gap, the §2 "full version"). `/run-the-audit` route reserved,
no page (addendum). Project tree per the checkpoint message; corpus renders verbatim via content
collections; only NEW chrome/nav/titles follow the Thesis naming sweep.

## Ride-along (with the build)

Repo About description fix; Thesis-rename sweep (Discussion title, README refs); repo About
homepage → datumwise.ai once DNS resolves.
