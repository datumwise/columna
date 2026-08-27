# Foundations mission 1 — bounded implementation plan (PROPOSED)

Against the rulings of 2026-08-27. Companion to `foundations_mission1_recon_v0_1.md`.
**Nothing implemented. No reader-facing file changed.**

Six steps. Each is independently shippable, independently revertible, and ends at a stop point with a
named verification. Rulings 7 and 8 (onsite readability, the orphaned Ground for Certainty) are
**step 3** — moved earlier than the recon proposed, for a reason given there.

---

## The sequence at a glance

| # | step | reader sees | depends on | new ruling needed? |
|---|---|---|---|---|
| 1 | **The word** — Evidence → Certainty | the bearing reads *Data · Certainty · Intelligence* | — | no |
| 2 | **Free the word** — rename `/research`'s "Foundations" group | one section heading changes on `/research` | — | **yes, small** — the replacement name |
| 3 | **The reading surface** — 14 deposited works become readable on-domain | *"deposit only — not readable here"* becomes a readable page, incl. **The Ground for Certainty** | — | **yes, two** — route name; unverified-provenance rendering |
| 4 | **`/foundations` I** — opening + three territories, questions-first | the page exists, honest, no relation rows | 2, 3 | **yes, two** — the "unsettled" list; citing outside traditions |
| 5 | **`/foundations` II** — relation rows, "How these relate", the `/research` line | the discussion connects to the works | 4 | no |
| 6 | **The payoff** — homepage link + navigation | the bearing becomes a destination; nav changes | 5 | **yes, one** — nav shape |

---

## Step 1 · The word

**Files.** `apps/website/src/components/home/Bearing.astro` (the `territories` line + the lede);
`apps/website/src/pages/index.astro` (`<title>` and meta description). ~4 lines.

**Reader-visible outcome.** Above the fold, `Data · Evidence · Intelligence` becomes
**`Data · Certainty · Intelligence`**, and the lede's *"across data, evidence, and intelligence"*
follows it. Nothing else on the site changes. No new link, no new page.

**Dependencies.** None. Shippable alone, today.

**Stop / verification.**
- `npm run build` clean, 45 pages.
- Screenshot the homepage above the fold and read it.
- `grep -r "Data · Evidence · Intelligence" apps/website/src` returns **only** the retired
  `Hero.astro` and `ThreeQuestions.astro` (both unimported) — confirming no live surface still
  carries the old triad.
- **`/evidence` is unchanged and its two guards are intact.** This is the check that matters: the
  page whose thesis is *"Evidence is a standing acquired through a governed crossing, not a
  sovereign jurisdiction"* must not acquire a triad by accident.

**New ruling needed.** No — ruling 2 approves it.

---

## Step 2 · Free the word

**Files.** `apps/website/src/data/sources.ts`, the `GROUPS` array, line ~135. One title string,
possibly one blurb.

### Recommendation, and why the two suggested registers do not fit

The group's siblings are **kind-nouns**: *Introductions and primers* · *Positions* · *Applied work
and readings* · *Studies, catalogues and program notes* · *Normative and generated references* ·
*Machine evidence* · *Teaching surfaces* · *The negative record* · *Historical records*. The heading
has to name **this kind**, in that register.

- **"Publications"** does not work: **every** group on the page is publications. *Positions* are
  deposited. *Introductions and primers* are deposited. The word would name the page, not the group.
- **"Research record"** does not work either: the page's own H1 is *"The current research corpus"*
  and its lede calls itself the record. The group would be claiming the whole page's name — the same
  shape of collision we are repairing, one level down.

**Recommended: `Theory and results`.** It fits the sibling register exactly, it is what the group's
own blurb already says (*"The theory itself, and the results that establish it"*), and it claims no
word another surface owns. If a plainer register is wanted: **`The theory, with its proofs`**.

**Reader-visible outcome.** One heading on `/research`. Nothing moves; no row changes group.

**Dependencies.** None — but it **must land before step 4**, or `/foundations` ships into a domain
where `/research` already owns the word.

**Stop / verification.** Build clean; `/research` renders the new heading; **`grep -ri "foundations"
apps/website/src/pages apps/website/src/data` returns no group/section heading** — only the
homepage lede's ordinary use of the word, which is prose and correct.

**New ruling needed.** **Yes, small:** confirm the replacement name.

---

## Step 3 · The reading surface  ← *this is the step ruling 7 asks for*

**The problem, restated with its number.** 14 Core works have no onsite reading route. `/research`
says *"deposit only — not readable here"* fourteen times. Those same 14 works are **already in this
repository**, byte-verified against Zenodo's own checksums, in `services/ask/deposits/` — **110,149
words**, ingested for the Ask agent and readable by a machine but not by a person.

> The publication text a reader is sent away to Zenodo for is already sitting in the repo that builds
> the site.

**The design: one route, N works, zero bespoke pages.**

```
/read/<slug>          one dynamic route, getStaticPaths() over the deposit manifest
```

| element | source | why |
|---|---|---|
| the body | `services/ask/deposits/<recordId>.md`, rendered byte-faithfully | it *is* the publication of record — md5-matched to Zenodo at ingest |
| title, version, date, DOI, standing | **the registry, at build** — `publications.ts` `currentRecord()` | not typed. The existing `/learn/` routes hardcode `const DOI = '10.5281/…'`; the new surface must not repeat that |
| the crossing | the site's existing **paper → wire crossing** grammar (`ds-crossing`) | see below |
| provenance | `manifest.json` — `provenance: zenodo` vs `supplied`, with checksums | two of the sixteen are author-supplied and must say so |

**The crossing marker reuses a distinction the site already draws.** The homepage already changes
register — paper to wire — at the moment it stops asserting and starts showing machine output.
Ruling 7 asks for exactly that move one level up: *a reader should know clearly when they have
crossed from editorial discussion into the publication of record.* So the reading surface opens with
one typed block, in the register the site already uses for crossings, carrying version · date · DOI ·
byte-fidelity · provenance — and then the deposited text, unadorned and unedited. **Editorial voice
stops at that block.** That is the boundary, and it is visible rather than stated.

This also satisfies ruling 8 with no special case: **The Ground for Certainty v1.1 gets a route
because it is a deposited current record**, not because Certainty needed a page to match Data.

**Scope: the 14 works the registry rules current and that have no route today.** Not the 2 preserved
editions (AG v1.1's paper, The Theory of Certainty v1.0) — those are a follow-on, because a preserved
edition needs the PRESERVED HISTORICAL STATE chrome and AG v1.1 already has a preserved *doorway*
page that is a different object from its *paper*.

### Two integration facts that nobody would guess, and one is a hazard

**(a) `sources.json` is shared with the Ask agent, and `route` is load-bearing there.**
`ingest_deposits.targets()` skips any source that has a `route` — *"already readable from the shipped
site build"*. So writing the new reading routes into `sources.json` **changes where the Ask agent
reads those 14 works from**: deposit-derived chunks become route-derived chunks. If the manifest and
index are not regenerated in the same change, the index gets **both** and every one of those works is
double-indexed.

> Giving a paper a reading page silently rewires the agent's corpus. This is the single riskiest
> thing in the six steps, and it is invisible from the website side.

Two options, and this wants a decision rather than a default:
- **(i)** accept the switch — regenerate manifest + index in the same commit, verify Core coverage is
  unchanged. Simplest, one source of truth for "is it readable here".
- **(ii)** add a distinct field (`readingRoute`) so `route` keeps meaning *"a site page about this
  source"* and the agent's behaviour is untouched. Safer, at the cost of two adjacent fields.

**Recommendation: (ii).** `route` currently means *a page the site authored about this work*
(`/learn/what-is-the-theory-of-data` is a hosted edition **with page chrome**). A reading surface is
not that; it is the work itself. Two meanings in one field is the kind of collapse ruling J names,
and the Ask agent is exactly the reader that would suffer from it.

**(b) The deposits live outside `src/`.** Precedent exists — `/docs/framework` imports from repo-root
`docs/` — but a *dynamic* route needs `import.meta.glob` across that boundary. **This is the one
implementation unknown in the plan**, and it is the first thing step 3 verifies. Fallback if it does
not resolve: a `scripts/` copy step gated on the manifest checksums, matching the `*.generated.json`
pattern the site already uses.

**Reader-visible outcome.** `/research`'s fourteen *"deposit only — not readable here"* rows become
**Read**. A reader following a foundational question reaches the actual publication **without leaving
the domain**, and knows, from a visible change of register, that they have crossed into it. The
"Record" link to Zenodo stays on every one — the source of record is never replaced, only reached.

**Dependencies.** None on 1 or 2. **Must precede step 4**, so `/foundations` has somewhere to send a
reader that is not Zenodo.

**Stop / verification.**
- build clean; page count rises by exactly 14.
- **read three rendered pages myself** — one long (Contract Calculus, 14,651 w), one short (The
  Ground for Certainty, 3,772 w), one author-supplied (Missingness, `provenance: supplied`) — and
  confirm the body is byte-faithful and the typed block is registry-derived.
- `python3 scripts/check_publications.py` — **G7 must stay green.** The new route file may carry no
  DOI literal; the deposits are already declared `frozen-deposit`.
- **the Ask integration check, and it is the one that matters:** rebuild the index, then confirm
  `core 834` chunks and 17 Core sources still reachable, `check_core_reachable` passes, and **no work
  is double-indexed**.
- `python3 scripts/check_corpus_membership.py` green.

**New rulings needed. Two:**
1. **The route name.** `/read/<slug>` (recommended — plain, reader-facing, the crossing carried by
   chrome not URL) or `/publications/<slug>` (the crossing carried by the URL too). Note `/record/`
   collides with `/research`'s existing "Record" link label.
2. **The two author-supplied works.** `Missingness Has a Universe` and `A Primer on the Theory of
   Data` are deposited on Zenodo as **PDF only**; their markdown was supplied by the author and
   **cannot be checksum-verified against the record**. May they be rendered as publication text? My
   recommendation: **yes, with their weaker provenance stated in the typed block** — the manifest
   already records the distinction and hiding it would be worse than the gap. But rendering
   unverifiable bytes as *the publication of record* is a publication decision, not mine.

---

## Step 4 · `/foundations`, part I — opening and the three territories

**Files.** `apps/website/src/pages/foundations.astro` (new). Possibly
`apps/website/src/components/foundations/` for the territory composition.

**Content.** As outlined in the recon §4: an opening that names no proper nouns, then three
territory sections each carrying **the questions · where we are · ways in · what is unsettled**.
Questions-first (ruling 5). No relation rows yet.

### `ThreeQuestions.astro` assessed against the current rulings (ruling 9)

Not restored mechanically. Item by item:

| element | verdict |
|---|---|
| **the composition** — one continuous field, hairline dividers, `repeat(3, 1fr)` collapsing to `1fr` at 56rem, and a comment forbidding cards | **reuse.** It is already *name the triad, do not diagram it*: no boxes, no fills, no arrows. |
| **"different JURISDICTIONS, not three planes of one lattice … no untyped edge crosses between them"** | **reuse the rule, retire the word.** This is exactly ruling 2's invariant, written a month early. But *jurisdiction* is the open CV-9 collision — `/evidence` denies Evidence is a "sovereign jurisdiction" while this file calls all three "jurisdictions". `/foundations` forces CV-9; see the ruling request below. |
| **Data** — *"What is the analytical object?"* | **replace with ruling C's wording**, *"What is the analytical thing we are working with?"* — it is the cold-readable one, and the reader arriving from The Yes Machine does not yet have the word *object*. |
| **Evidence** — *"What does the evidence support?"* / *"Evidence licenses claims only through an explicit governed passage."* | **re-author entirely.** This is **Statistical Bridge doctrine — one part of Certainty, not the whole of it.** Keeping it would make the territory the size of one paper, which is the mistake the rename exists to fix. |
| **Intelligence** — *"What may reason and act on it?"* / **"Interpretation is useful. Interpretation is not authority."** + its support line | **survives intact.** Already locked in its own file against being rewritten in Data's vocabulary; already ruling-compatible; and it is the one thing datumwise holds firmly here. |
| **the marks** — `F @ A` · `evidence → inference → claim` · `intent → candidate → authority` | **drop, or demote below the fold of the section.** They are formal notation for a reader who has just arrived from a LinkedIn article. `evidence → inference → claim` is also Bridge-specific and would survive the rename it should not survive. |
| **the ordinals 1 · 2 · 3** | **drop.** Numbering three territories implies a sequence, and ruling 2 forbids implying they are equivalent or ordered. The recon's *"do not draw a pipeline"* is the same point; the ordinals draw one in miniature. |

So: **reuse the shell and one of the three units; re-author the rest.** The retirement reason
(*"three short explanations cannot carry three foundations before a reader has experienced any of
them"*) is **satisfied, not overridden** — on `/foundations` the reader chose the abstraction, and
the sections are no longer three short explanations but four moves each.

**Reader-visible outcome.** `/foundations` exists and is honest before it is complete: the three
territories, their questions, where the work is thick and thin, and what is open. Reachable by URL;
**nothing links to it yet.**

**Dependencies.** Step 2 (the word must be free) and step 3 (somewhere to send a reader).

**Stop / verification.**
- build clean; **the Yes Machine cold-reader test run for real** — read the article to its last line
  (*"we have to go back to the foundations"*), land on `/foundations`, and check the one thing that
  matters: do the three words arrive as *questions the article already raised*, or as *three things
  this company sells*?
- no diagram, no boxes, no arrows, no ordinals — verified by screenshot, not by intent.
- `/evidence` and `/analytical-governance` guards still intact and unedited.
- G7 green: `/foundations` is a `derived` surface and may carry no publication literal.

**New rulings needed. Two:**
1. **What "unsettled" says.** `specs/doctrine_gaps.md` and `specs/open_forks.md` hold real, dated open
   questions — but they are **internal ledgers** and no site surface has ever shown open questions to
   readers. Which are reader-facing is editorial, and it is the element that decides whether the page
   is a discussion or a brochure.
2. **Citing outside traditions.** Ruling A says Foundations may draw on *"established ideas and
   traditions from elsewhere"* and *"current research"*. **No datumwise surface currently cites
   anyone outside datumwise** — and Ask types external sources as a class that may never establish a
   datumwise position. Without a stated convention, the first external citation will read as
   endorsement. This wants a ruling **before** composition, not after.

Also folded in here: **CV-9** — the two senses of *jurisdiction* — because `/foundations` is the page
that forces it.

---

## Step 5 · `/foundations`, part II — the connections

**Files.** `apps/website/src/pages/foundations.astro`; `apps/website/src/data/publications.ts`
(read-only use).

**Content.** The relation rows (recon §5), reusing `/analytical-governance`'s `NEIGHBOURS` pattern:
**name · relation-verb · prose**, hairline rules, no cards, href optional. Two or three per
territory, chosen for a reader. Then *"How these relate"* — **prose, not a diagram** — including where
Analytical Governance stands: **its own seat** (ruling 1), drawing on all three, filed under none.
Then one line to `/research`.

**Why a relation row is not a catalog row:** a catalog row says *here is a work*; a relation row says
*here is how this work stands to this question* — and a relation verb cannot be written without
taking a position. Publications become contributions to a discussion (ruling 5), and the
territory/theory/publication distinction becomes structural: the territory is the section, the
account is named in the prose, the publication is the row with the href.

**Reader-visible outcome.** The discussion connects to the works, and every "way in" now lands on a
readable page from step 3 rather than on Zenodo.

**Dependencies.** Step 4. Split from it deliberately, so the catalog pressure is visible as its own
decision rather than smuggled in with the prose.

**Stop / verification.**
- every publication fact registry-derived — **zero DOI or version literals** in the page; G7 green.
- **row count discipline**: if a row is present because the work exists rather than because a reader
  needs it, it belongs on `/research`. Checked by reading, not by lint.
- The Ground for Certainty resolves to **v1.1** and links to its step-3 reading page.
- "How these relate" contains no diagram, and AG appears outside the three.

**New ruling needed.** No — bounded by 4's rulings.

---

## Step 6 · The payoff — homepage and navigation

**Files.** `apps/website/src/pages/index.astro` (the territory line after the encounter);
`apps/website/src/components/site/SiteHeader.astro` (the `DOORS` array).

**Content.** The homepage already contains the unpaid seam — *"This is one problem out of several,
and not the hardest."* It gains **one sentence and one link** to `/foundations`. Still prose, still
no cards. The Bearing's terrain words stay **unlinked**: three big clickable words at the top of the
homepage is the old architecture in a smaller costume, and the file's own ruling still holds.

**Navigation.** Ruling 1 gives the architecture — *Foundations · Analytical Governance · Doors · Ask
· Columna* — and says explicitly it is **not** a ruling that all five become equal nav items. Today
the header is three flat doors. Doors does not exist yet and Ask has no reviewed answers yet, so a
literal five-item header would advertise two rooms that are not furnished.

**Recommended for this step: `Foundations · Analytical Governance · Columna`** — a substitution, not
an expansion. `Research` leaves the header (it stays in the footer, where it already is, and is
linked from `/foundations`). Foundations takes the position a reader meets first. Doors and Ask join
the header when they are worth arriving at, which is your steps 3 and 4 of the mission, not this one.

**Reader-visible outcome.** The bearing becomes a destination; the site's front door matches its
intellectual architecture.

**Dependencies.** Step 5 — deliberately last. **A page should be worth arriving at before anything
points to it.**

**Stop / verification.** Build clean; `check_discoverability.mjs` still passes (it enforces exactly
one homepage entrance linking `/start-here`, plus `/case` and `/known-issues` links); every route
that left the header still reachable; the full cold-reader walkthrough from the homepage down.

**New ruling needed. One:** the header composition above — whether `Research` may leave the header,
and whether Foundations replaces or joins.

---

## What this plan deliberately does not do

- **Doors.** Not built, not designed. `/park/when-is-it-data` is a Door in embryo and
  `/positions/*` are adjacent; what a Door *is* versus a position is an editorial ruling, not a
  build task.
- **Ask seeding**, `/learn` re-scoping, the homepage legacy boundary, the three-navigational-surfaces
  disagreement, `/learn`'s stale `6e` label, the sitemap's two mis-advertised redirect stubs.
- **A Certainty page.** Ruling 8 is satisfied by step 3 giving The Ground for Certainty a route and
  step 5 leading into it — **not** by building a symmetric page because Data has one.
- **Any model evaluation.** Nothing agent-facing changes in steps 1, 2, 4, 5, 6. **Step 3 does** —
  it can rewire where the agent reads 14 Core works — so under the rule of 2026-08-26 that step
  carries deterministic index/coverage verification, and an evaluation only if the retrieval
  behaviour is shown to have moved.

## Rulings needed before implementation begins

| # | step | ruling |
|---|---|---|
| R1 | 2 | the `/research` group's new name — recommended **"Theory and results"** |
| R2 | 3 | the route name — recommended **`/read/<slug>`** |
| R3 | 3 | may the two **author-supplied** works be rendered as publication text, with weaker provenance stated? |
| R4 | 3 | `route` vs a new `readingRoute` field in `sources.json` — recommended **the new field**, to keep the Ask agent's corpus unchanged |
| R5 | 4 | which open questions are **reader-facing** |
| R6 | 4 | the convention for citing **outside traditions** |
| R7 | 4 | **CV-9** — the two senses of *jurisdiction* |
| R8 | 6 | header composition — may `Research` leave the header? |

R1–R4 gate the first shippable half. R5–R7 gate composition. R8 gates only the last step.
