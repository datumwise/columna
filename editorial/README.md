# editorial/

**Working drafts of public-facing writing. Nothing in this directory is a publication, and nothing
in it carries authority.**

This directory exists because the repo had no non-authority home for editorial writing. Every other
place a draft could plausibly go means something the draft is not:

| Location | What putting a draft there would assert |
|---|---|
| `registry/publications/` | it is a registered work with records, a DOI and currency |
| `services/ask/deposits/` | it is corpus the agent may quote as datumwise's position |
| `apps/website/src/content/corpus/` | it is deposited bytes rendered by a live route |
| `docs/` | it is a manual, rendered at `/docs/*` |
| `specs/` | it is a ruling, plan, recon or report |

So: `editorial/drafts/` — text on its way somewhere else, kept where the rest of the work can see it,
asserting nothing.

## What a file here is NOT

- **not** registered in `registry/publications/` — no workId, no record, no DOI, no version standing
- **not** in Core, and **not** in any authority layer
- **not** ingested into Ask — see below for why this is structural, not a promise
- **not** deposited anywhere
- **not** rendered by any site route: no page imports from this directory, no `/read` page, no
  onsite duplicate of the eventual publication
- **not** published, and not a claim about what will be published

## Why it is inert, structurally

Not by convention — by how the two consumers actually work:

- **Ask.** Corpus membership is `apps/website/dist/**` ∩ a `route` in `registry/sources/sources.json`
  ∩ a non-`out` layer in `registry/sources/ask-authority.json` (`services/ask/ask/index_build.py`),
  plus the separate deposits path via `services/ask/deposits/manifest.json`. A markdown file here is
  in none of those, so it produces no chunks and changes no route count.
- **The website.** Astro builds `apps/website/src/pages/**`; corpus markdown is rendered only where a
  page imports it. Nothing here is imported, so nothing here ships.
- **The publication gates.** `scripts/check_publications.py` G7 fails closed on a tracked file
  carrying a Zenodo token with no `consumers.json` classification. Drafts here must therefore **not
  type DOIs**. If a draft ever needs to cite a deposited work, cite it by title and let the registry
  own the identifier.

If a draft in here ever *should* become any of the things listed above, that is a ruling and a
separate change — it does not happen by a file moving.

## Naming

`<slug>_v<N>.md`, matching the draft's own version. A new version is a new file, not an edit in
place: these are the bytes as received, and the point of keeping them is to be able to say later what
was actually said at each stage.
