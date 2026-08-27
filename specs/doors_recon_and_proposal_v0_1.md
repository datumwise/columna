# Doors — recon + bounded proposal (v0.1)

**Requested:** Huayin, 2026-08-27 (Doors doctrine + artifact recon brief, §K).
**Status:** RECON AND PROPOSAL ONLY. Nothing implemented. `/doors` does not exist and is not
scaffolded. The Yes Machine Problem has not been imported. No silent-failure rewriting, no
Regression/Missingness work, no Trust, Authoring, Ask seeding, Anthropic comparison, or AI-agent
article started.

**Governing idea being served:** a Door is for passage; once crossed, the reader should have
somewhere deeper to go.

---

## The headline, before the detail

Three findings change the shape of the answer, and all three are good news for a light surface:

1. **The destinations are already modelled.** `registry/sources/sources.json` carries `route` (a page
   this site authored) and `readingRoute` (`/read/<slug>`, the work itself) for every candidate. A
   Door's destination is `route ?? readingRoute` — resolvable, not typed. Only the off-domain Yes
   Machine has neither.
2. **Ask's corpus membership is keyed on `sources.json.route`.** So `/doors` must *not* be given a
   `route` entry. As a plain page it is invisible to Ask; as a catalogued source it would silently
   join the agent's authority-bearing corpus. This is the single sharpest collision, and avoiding it
   costs nothing.
3. **The onward movement doctrine (§I) has nowhere to live today.** `/read/*` pages end in
   provenance ("the record is the authority… open the deposited record → · the rest of the corpus");
   `/positions/*` pages end in an evidence note. Neither ends in "and here is the question this
   opens." If the Door is to stay light, the onward question must be at the destination — and the
   destination does not currently have one. **This is the only place the doctrine demands new
   editorial work, and it is one line per Door.**

---

## K1 · What existing route/components could support a very light `/doors`

**Nothing new is needed.** The site already has the exact shape twice:

| Precedent | File | Shape | Fit |
|---|---|---|---|
| **`/positions` index** | `apps/website/src/pages/positions/index.astro` | literal array → `<ul>` of {title, stamp, pull}, hairline-separated | **Closest.** Drop `stamp`, rename `pull` → invitation, and it *is* the Door list. ~45 lines including styles. |
| homepage directory | `src/pages/index.astro` (`DIRECTORY`) | ordered `<ol>` of {title, blurb, href} + rung numbers | Right primitives, wrong affordance — it is a *ladder* (sequenced). Doors are explicitly not ordered. |
| `/learn` groups | `src/pages/learn.astro` | grouped list with an `external: true` flag | The **external-destination precedent** — see K3. |

**Recommendation:** one new page, `src/pages/doors.astro`, built from a literal array, using the
`/positions` index markup. No content collection, no component extraction, no data file, no registry
entry. If a second surface ever needs the same list, extract then — not now.

`BaseLayout` already supports it with zero changes: `footer="general"` (the default — Doors is a
datumwise-level surface, not the Columna estate) and the install chip stays off by the same default.

## K2 · Can the three strong Doors be represented without a new artifact type?

**Yes, and without touching any artifact.** A Door is three fields and a role; none of them is a
property of the work.

- *Data Has Its Own Ontology* → `readingRoute: /read/data-has-its-own-ontology` (registry, today)
- *Never Let Your Agent Touch the Database* → `route: /positions/never-let-your-agent-touch-the-database` (registry, today)
- *The Two Jobs of the Conditioning Bar* → `readingRoute: /read/conditioning-bar` (registry, today)

No new publication type, authority class, provenance class, standing, or corpus layer is created —
which is §B satisfied structurally rather than by promise. The destination page is unchanged and
keeps its own identity and standing; `/doors` never restates them (§J).

**One caution, stated because it is cheap now and expensive later:** do not add a `door: true` flag
to `sources.json`. That file is read by Ask as well as the site, its two route fields already carry a
load-bearing distinction (`sources.ts:41-55`), and Door status is editorial, not catalogue truth. The
Door list belongs in the page that renders it.

## K3 · Heterogeneous destinations

Three kinds, and the site already handles two of them.

| Kind | Example | Handling | New work |
|---|---|---|---|
| `/read/<slug>` publication | Data Has Its Own Ontology | ordinary internal link | none |
| `/positions/<slug>` site-authored | Never Let Your Agent | ordinary internal link | none |
| **external (LinkedIn-first)** | The Yes Machine Problem | **the `/learn` pattern**: `external: true` → `rel="noopener" target="_blank"` and a trailing ` ↗` on the title | reuse, don't invent |

`learn.astro:106` is the precedent, glyph and all:
`<a href={it.href} {...(it.external ? { rel:'noopener', target:'_blank' } : {})}>{it.title}{it.external ? ' ↗' : ''}</a>`

**The tension to rule on, not for me to settle.** Ten days ago the ruling was *"the publication text
stops living off-domain"* — fourteen Core works were brought onsite precisely so a reader following a
foundational question need not leave. A Door whose destination is a LinkedIn article sends a cold
reader **off the property at the first crossing**, into a surface where none of the site's guarantees
(provenance block, fidelity pin, onward path, no login wall) apply. §B already permits this, so this
is not an objection — it is a consequence worth having said out loud. Three options, cheapest first:

- **(a) External, marked.** Ship it as `↗`. Accepts the tension; zero build.
- **(b) Wrapper onsite.** The Door points at a short onsite page that carries the invitation and the
  onward question and links out. Keeps the crossing on the property; costs one page and a decision
  about what that page *is*.
- **(c) Onsite home later.** Ship external now; give it an onsite home when/if it is deposited.
  Requires nothing today and preserves both options.

I would not decide this until the piece is written; (a) and (c) are the same first move.

## K4 · The smallest editorial metadata `/doors` actually needs

**One new fact per Door.** Title and destination are already in the registry; only the *invitation*
is genuinely new — `purpose` in `sources.json` exists but is descriptive, written to help a scanning
researcher, not to attract a stranger.

```
{ title, invitation, href, external?, specialist? }
```

- `title` — the artifact's **actual current title** (§H). Not a Door label wearing a publication's
  clothes.
- `invitation` — one sentence, ≤ ~20 words. The thing that makes someone cross.
- `href` — `route ?? readingRoute` for onsite works; a URL for external ones.
- `external?` — reader-visible marker + `rel`/`target` (K3).
- `specialist?` — the §E.4 subordination for the Conditioning Bar: same list, visually quieter
  (smaller title, no separate section, no heading that creates a category). One boolean beats a
  second section, because a section implies a taxonomy and §C forbids one.

**Nothing else.** No DOI, version, date, provenance summary, standing, role, category, filter, tag,
count, "related", or reading time. Two of those are not merely unnecessary but *gated*:
`scripts/check_publications.py`'s G7 echo audit fails the build if a file types a Zenodo token
without a `consumers.json` row, and G10 forbids a publication-count claim on a non-derived surface
while works remain `kind: unclassified` (all 33 are). **A `/doors` page that types no DOI and no
count is inert to both gates.** That is an argument for the light surface with teeth in it.

## K5 · Onward exploration without turning the Door into a hub

**Put the next question at the destination, after the piece — never on `/doors`.** That keeps §C
(pass-through, not a hub) and §I (create a natural next question) from fighting each other, because
the question arrives *when the reader has just finished reading*, which is the only moment it lands.

Current state, which is why this needs a ruling:

- **`/read/<slug>`** ends with `.foot`: *"The record is the authority. This page reproduces it; it
  does not replace it. Open the deposited record → · the rest of the corpus."* A provenance exit, and
  the only exits are the DOI and `/research`. A reader who just read *Data Has Its Own Ontology* is
  offered the deposit and the corpus index — not `/foundations`.
- **`/positions/<slug>`** ends with an editorial evidence-note; no onward path at all.

**Proposal:** one sentence appended to the destination foot, per Door, in the site's existing voice —
the §I examples are already the right sentences. Two constraints the route imposes:

1. On `/read/*` it must sit in `.foot`, **after** the deposited text. The crossing block promises
   *"datumwise has not summarised, sequenced or introduced it on this page"* — that promise governs
   everything above the deposit. The foot already carries editorial voice, so this is consistent.
2. It must be per-work, not a generic template, or it becomes furniture. Four sentences total for
   four Doors; if that ever needs a data structure, the collection has grown past what §D allows.

**This is the only new editorial writing the initial collection requires.**

## K6 · Header placement

**Not immediately. After the collection is complete.** This is already ruled in-tree and the ruling
covers this exact case — `SiteHeader.astro`, ruling R8, 2026-08-27:

> *"Doors does not exist yet and Ask has no reviewed answers yet, so a literal five-item header would
> advertise two rooms that are not furnished."*

With two of three general Doors live and the Yes Machine unpublished, `/doors` on day one is a
half-furnished room advertised at full volume. **Reach it from the homepage instead, and add the
header door when the third Door lands.**

Where on the homepage is a real question with a real collision: the wayfinding band is an **ordered
ladder** of eight entries, and its first item is the protected `dir-entrance` — `check_discoverability.mjs`
asserts *exactly one* `dir-entrance` linking `/start-here`. A ninth rung competes with the
`/start-here` entrance for the same job (where a stranger begins). Options, in the order I would try
them: a single line under the Bearing, above the encounter; a rung on the ladder; or nothing until
the header door is earned. **Not proposing; flagging that "put it on the homepage" is a composition
decision, not a link.**

One naming hazard while it is still free: **`SiteHeader.astro`'s nav constant is already named
`DOORS`** (Foundations · Analytical Governance · Columna), and "doors" appears in that sense across
`index.astro`, `columna.astro`, `research.astro` and `the-argument.astro`. Two meanings of *door* in
one shell, one of them in code, and the doctrine says Doors are explicitly *not* peers of those three.
Rename the nav constant to `NAV` (or `PRIMARY`) in the same change that introduces `/doors`.

## K7 · The stale-title defect — see the separate section below

Diagnosed independently and **not mixed into Door classification**. See §"Currency defect" at the
end of this document; it proposes the repair's scope only.

## K8 · Collisions with registry, Ask, publication standing, readingRoute, sitemap, navigation

| Surface | Collision | Verdict |
|---|---|---|
| **Ask corpus** | Membership is `dist/` ∩ `sources.json.route` ∩ `ask-authority.json` layer (`services/ask/ask/index_build.py`). A page with no `route` entry is crawled and then **skipped as uncatalogued**. | **`/doors` must not get a `sources.json` route entry.** As a plain page: zero effect on chunks, route count, or corpus semantics. Give it a `route` and it silently becomes an authority-bearing surface for the agent. |
| `readingRoute` | Deliberately distinct from `route` (`sources.ts:41-55`); overloading it would move Ask's corpus. | `/doors` **reads** these fields; it must not write to either. No `/read/*` route is in the Ask index today, and that stays true. |
| Publication registry | `works.json` / `records.json` are identity + bibliography + currency only; **no route field exists**. | A Door needs no registry object. Door status is editorial, adds discoverability, changes no standing — §B satisfied structurally. |
| Publication standing | `check_publications.py` G7 echo audit + G10 count rule. | Inert **iff** `/doors` types no DOI and no publication count. Design constraint, already met by K4. |
| Sitemap | `astro.config.mjs` filter excludes only two redirect stubs; everything built is listed. | `/doors` auto-listed. Nothing to do. |
| `llms.txt` | `src/content/llms_index.txt` is hand-authored prose; only `{{PUBLICATIONS}}` is derived. | A human adds one line, once, when `/doors` is worth naming to machines. `check_prose_coherence.py` only parses FrameQL blocks, so prose is inert to it. |
| `check_discoverability.mjs` | Enumerates 3 protected routes; does not enumerate all routes; no external-link handling. | Nothing breaks. Whether `/doors` *joins* the protected table is a decision for when it has inbound links worth defending — "adding a route here is a decision, not a default." |
| `check_fragments.mjs` | Internal only; absolute `http(s)` hrefs never match. | An external LinkedIn URL is invisible to the gate — **so nothing checks it.** A dead Door is a silent dead Door. Worth one line in the page comment. |
| Navigation semantics | The `DOORS` constant collision (K6). | Rename in the same change. |

## K9 · Minimal implementation sequence

Assuming the initial collection is *Data Has Its Own Ontology*, *Never Let Your Agent Touch the
Database*, and *The Yes Machine Problem* once published, with the Conditioning Bar optionally present
as a specialist Door.

**Step 0 — decide (no code).** (i) the three invitations; (ii) the onward question per destination;
(iii) whether the Conditioning Bar ships in the initial collection; (iv) K3(a) vs (b) for the Yes
Machine. These are editorial and none of them is mine to make.

**Step 1 — the page.** `src/pages/doors.astro`: literal array of 2–3 entries, `/positions`-index
markup, `footer="general"`. Rename `SiteHeader`'s `DOORS` → `NAV` in the same commit. **No header
link.** Gates: build + the four site gates, unchanged.

**Step 2 — the onward lines.** One sentence in the `.foot` of `/read/data-has-its-own-ontology` and
at the end of `/positions/never-let-your-agent-touch-the-database`. This is the step that makes them
Doors rather than links; it is also the step most easily skipped, so it should not be split into a
later slice.

**Step 3 — reachability.** One homepage route into `/doors`, chosen per K6. Re-run
`check_discoverability.mjs` (the `dir-entrance` singularity assertion is the one to watch).

**Step 4 — the Yes Machine, when published.** Add the third entry with `external: true`; revisit
K3(b) only if it earns an onsite home.

**Step 5 — the header door, when the collection is complete.** `SiteHeader` goes to four items, and
the R8 comment gets its update: the room is now furnished. Consider adding `/doors` to
`llms_index.txt` in the same change.

Steps 1–3 are a single small PR. Steps 4–5 are separate and later, by construction.

---

## Currency defect (K7) — Three Structural Sources / Two Great Sources

*Diagnosed independently. Not Door work; the piece is not a Door and this repair does not make it
one.*

**It is already banked — and it is more precisely typed than "stale title".**

The ledger has it twice, open, since 2026-08-21:

- `specs/publication_corpus_coverage_v0_1.md:224` — **CV-7**: *"the live route … and its page title
  name the superseded account — OPEN. Correct as an edition-pinned rendering of the v1.1 bytes;
  whether the ROUTE should follow the retitled successor is editorial, and publication foundation
  does not get to answer it."*
- `registry/publications/reconciliation.json:161` (`rc-two-great-sources-successor`) — *"RECONCILIATION
  DEBT, NOT CLOSED HERE."*

So this is not a defect nobody noticed; it is a question deliberately handed to editorial and never
answered. **The correction closes an open ledger item rather than opening a new one.**

**The registry facts.** `w-two-great-sources` has two records across a concept boundary:

| record | title | version | date | DOI | status |
|---|---|---|---|---|---|
| `.r01` | The Two Great Sources of Silent Analytical Failure | (unversioned) | 2026-07-25 | `10.5281/zenodo.21553379` | superseded |
| `.r02` | **Three Structural Sources of Silent Analytical Failure** | 2.0 | 2026-08-11 | `10.5281/zenodo.21893929` | **current** |

`works.json:63` already carries the current `canonicalLabel`.

**What is NOT wrong, and must not be "fixed".** The page renders the **deposited r01 bytes verbatim**
(`src/content/corpus/position_two_great_sources_site_v1_1.md`, class `frozen-corpus`,
`consumers.json:217`), and `sources.json:75` marks the source `editionPinned: true`. Its rendered
H1, its `v1.0` byline and its DOI `…21553379` are **correct**: that is what the first edition says.
Editing frozen deposited bytes to chase currency is the one thing the repo forbids outright. There
is also **no r02 artifact onsite** — no deposit, no corpus file, no `/read` page — so the repair
cannot be "point at the current one." There is nothing current to point at.

**What IS wrong** is narrower and entirely fixable: the site speaks **in its own voice**, in four
hand-typed strings, as if the superseded title were the work's name — with no disclosure at all.

| # | file:line | current string | class |
|---|---|---|---|
| 1 | `positions/the-two-great-sources-…astro:9` | `<BaseLayout title="The Two Great Sources of Silent Analytical Failure — datumwise"` | site chrome |
| 2 | `positions/index.astro:23` | `title: 'The Two Great Sources of Silent Analytical Failure'` | site chrome |
| 3 | `positions/index.astro:24` | `stamp: 'July 2026 · v1.0'` | site chrome (stamp is honest for the edition; it is the *title* beside it that misleads) |
| 4 | `learn.astro:75` | index entry under the old title | site chrome |

**And the site already knows how to say the true thing.** `/research` derives exactly this
disclosure today (`research.astro:139`, driven by `editionPinned`):

> *edition-pinned* — This site renders the deposited **first edition** (25 July 2026) — the edition
> this page was built from. The current record is **v2.0**. The onsite edition was deposited under
> its earlier title, *The Two Great Sources of Silent Analytical Failure*.

So `/research` names the work correctly and discloses the pin, while the position route names the
superseded account with no pin at all. **The two live surfaces disagree**, and one of them is
derived.

**Smallest correct repair — scope only, not designed here.** Bring the four hand-typed strings into
the shape `/research` already derives: name the **current** work, disclose the **pinned edition**,
leave every frozen byte untouched. That is a chrome-only change with no route change, no redirect, no
registry edit, and no frozen-bytes edit. Two consequences to carry with it:

- **Ask must be regenerated.** `services/ask/index/chunks.json:9142-9301` holds 9 chunks for this
  route whose `title` is a scrape of the stale page `<title>` (their `sourceLabel` is already
  correct). A `<title>` change without `python3 -m ask.index_build` leaves the agent quoting the old
  name.
- **The ledger must be closed or re-stated.** CV-7 and `rc-two-great-sources-successor` should record
  the answer, not keep asserting an open question that has been silently settled.

**Explicitly out of this repair: the ROUTE.** Renaming the slug is the expensive half CV-7 left open
— it pulls in a redirect in `astro.config.mjs` (precedent at `:86-87`), `sources.json:71`,
`consumers.json:367`, `reconciliation.json:153`, a chunks regeneration whose `url` values are
snapshots, and a frozen inbound link at `research_corpus_map_v0_2.md:25` that can only be kept alive
by the redirect and never by editing. **My recommendation is to fix the voice and leave the route**,
but that is the editorial call CV-7 reserved, and it is not mine.

**Also excluded by prior ruling:** `src/data/latest.ts:207-212`. It is a dated announcement log;
retitling a log entry falsifies it.

---

## What I did not do

- Did not create `/doors`, a component, a data file, or a registry entry.
- Did not import, ingest or draft The Yes Machine Problem.
- Did not touch the silent-failure piece, Regression Has an Anchor, or Missingness Has a Universe.
- Did not retitle anything, and did not propose a Door label that could pass as a publication title.
- Did not decide the four Step-0 editorial questions.
