# WP-5.1 spec — datumwise.ai: site + live widget (v1)

**Prereq (Huayin, before kickoff):** grant Claude Code's identity durable write access to
`datumwise/columna` (org-side). No tokens through chat.

**Goal.** Public site at datumwise.ai: the positioning, the launch post, the research, and a
**live widget** that runs the three-mood demo against a hosted Columna endpoint.

## Deliverables
1. **Site** (`apps/website/`, Astro, static): Home (honest-metrics-engine positioning + widget),
   Launch post (moved verbatim from the Discussion; Discussion gets a link back), Research
   (both DOIs + benchmark pointers), Docs links, Install (`pip install` + quickstart), GitHub link.
   Anti-hype design language; disclosure as a design element.
2. **Hosted demo endpoint:** Dockerfile (deliverable — also the `docker run columna/server`
   quickstart image) running `columna-server demo --http`, deployed to Fly.io at
   `demo.datumwise.ai`. Read-only by construction; add rate limiting; serves ONLY the packaged
   demo Manifold (isolated; worst-case abuse = restart).
3. **Widget:** scripted three-mood flow (clarify → refuse → disclose) driven live against the
   endpoint, rendering real wire JSON; a "try to fool it" input (nonexistent-measure → the ASK).
   **Graceful degrade:** endpoint down → play the recorded `demo --play` transcript with a
   "live demo temporarily offline" note. The site must never look broken.
4. **DNS/About:** datumwise.ai → site; `demo.` subdomain → Fly; repo About homepage → site.

## Invariants
No engine/contract changes; widget consumes the wire as-is (`contract_version "1"`); every
number shown comes from the wire or the recorded transcript — never hand-written; token-gated
HTTP stays for non-demo deployments (the public demo endpoint may run ungated but rate-limited).

## Acceptance
Site builds + deploys; widget completes the three moods live; degrade path verified (endpoint
stopped → recorded transcript plays); Dockerfile runs locally (`docker run` → `--play` works);
Lighthouse ≥ 90; all links resolve.

## Checkpoint (light)
Before building: (a) sitemap + homepage copy verbatim, (b) widget interaction script,
(c) Fly deployment plan + rate-limit approach. Then build on approval.
