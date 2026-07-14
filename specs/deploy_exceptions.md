# Production deploy exceptions — ledger

**Why this file exists.** datumwise.ai deploys are supposed to go **through the pipeline**:
merge to `main` → CI regenerates the integrity transcript from the shipped package → CI deploys.
Until the three Vercel CI secrets are wired, that pipeline is inert, so production has been reached
by **direct/hand deploys**, each requiring Huayin's explicit, logged authorization. Memory doesn't
hold ledgers; this file does.

**Standing rule (from 2026-07-14).** Every exception deploy **updates this file in the same PR or
commit as the content it ships** (or, for a content-free deploy, its own commit). No exception
deploy is complete until its row is here. When the pipeline goes green, exception deploys should
stop entirely — a pipeline-native deploy is the norm; this ledger only tracks the hand deploys that
predate it or are explicitly authorized around it.

**Mechanism (identical for all rows below).** From a clean checkout of the deployed SHA:
`apps/website/scripts/gen_transcript.py > src/data/transcript.generated.json` (integrity transcript
from the shipped package) → `vercel build --prod` → `vercel deploy --prebuilt --prod`. Prebuilt
output uploaded; nothing built on Vercel — the same output the CI pipeline would produce.

## Exceptions

| # | date (UTC) | authorizer | deployed SHA | scope (what went live) |
|---|---|---|---|---|
| 1 | 2026-07-13 17:16 | Huayin | `f0543ff` | **Manifold Explorer tier 1 (+ v0.2 operator surface)** — describe cards, the "what's in this manifold?" panel, doorways, glossary, the derived-metric card. *(Post-merge deploy; not separately logged at the time — this is the omission the ledger corrects. The one that "keeps falling out of the count.")* |
| 2 | 2026-07-14 09:08 | Huayin (deploy-call **ii**, "one further logged exception") | `15b90f1` | **Positioning launch** — /ladder, /about, /notes/cacher, site-wide nav swap (Ladder in, Research to footer), the four cross-reference stitches, homepage two-hunk meta+§6 link. |
| 3 | 2026-07-14 09:23 | Huayin ("one further logged deploy exception for this change") | `2b83305` | **/about role-separated author line** — "…Huayin Wang, who researches and builds… with engineering and infrastructure by Irena Wang." |
| 4 | 2026-07-14 15:21 | Huayin ("one-time logged deploy exception") | `76be279` | **Pre-launch integrity batch** — S1b (/ladder v0.3 gate-two seam-attribution), S3 (/why 66↔67 reconciliation), S4 (algebra→grammar reframe on homepage §4, /why "historical irony", /thesis §II close). |

## Not counted here — pre-merge-first build-out

Production deploys before Exception 1 were the initial site build-out and iteration, prior to the
merge-first/logged-exception protocol (introduced with the positioning WP, 2026-07-14). Listed for
completeness, not as exceptions: `4433399` (2026-07-13, live fool-it endpoint wiring), `721b029`
(2026-07-13, Exhibit B UX), and the 2026-07-11 series (`b06040b`, `a357705`, `23eb89c`, `56a355e`,
`bf4ccd7` — the wp5.1 site build). If any of these should be reclassified as exceptions, say so and
they move up.

## Next: retire the exceptions

The blocking item is wiring the three GitHub Actions secrets so CI deploys on merge:
`VERCEL_ORG_ID = team_BmVWdfstitWderA9WOjchHQ1`, `VERCEL_PROJECT_ID = prj_wR7vlSnMEdq34K3eZQ284zdKVhsL`,
and `VERCEL_TOKEN` (generated + set directly by Max/Irena, never through chat). Then: a no-op
pipeline-native proving deploy + a prod smoke test. After that, this ledger should stop growing.
