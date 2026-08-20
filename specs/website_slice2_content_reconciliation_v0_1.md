# Website Slice 2 — the Content Reconciliation Ledger (v0.1, PROPOSED)

**Status:** PROPOSED for ruling. No implementation authorized by this document.
**Opened:** 2026-08-20, after Slice 1 merged (`cc7961a`, PR #178).
**Sibling ledgers:** [`doctrine_gaps.md`](doctrine_gaps.md) (doctrine ↔ code), [`open_forks.md`](open_forks.md) (undecided forks).
This ledger is the third axis: **doctrine ↔ published site surface.**

---

## 0 · The governing principle

> **The old site is evidence and source material, not the design constraint.**

The new positioning, the four-door architecture, current doctrine, and the approved visual grammar
determine the target site. Existing pages are evaluated *against* that target. **They do not veto it
merely because they already exist.**

Legitimate preservation is bounded to exactly three classes. A surface that is not in one of them
has no standing to constrain the redesign:

| # | class | what it protects | test |
|---|---|---|---|
| P1 | **Frozen deposits** | byte-identity with a published record (Zenodo) | is there a deposit whose bytes this file must match? |
| P2 | **Engineering addresses / external-link contracts** | URLs and fragments cited off-site, by CI, or by shipped code | would changing this break something we do not control? |
| P3 | **Attribution honesty** | authorship, version, date, DOI, supersession | does changing this misstate who said what, when? |

Anything else — tone, length, page count, historical ordering, "we already wrote it" — is **evidence**,
not a constraint.

### The two transition rules

> **Revision debt may remain temporarily unpaid.**

A surface may sit in REVISE or ARCHIVE for as long as needed. Slice 2 does not have to repay the whole
debt to proceed. What matters is that the debt is *recorded*, not that it is *settled*.

> **No new surface may import a REVISE or ARCHIVE formulation as current doctrine.**

This is the load-bearing rule and the one that needs enforcement, not goodwill. A frozen or superseded
artifact may still be **cited** with clear version/historical context; it simply **cannot legislate
current doctrine forward**. Citation is allowed; inheritance is not.

*Recommended enforcement (proposed, not built):* every ledger row carries a `doctrine_status` of
`CURRENT | REVISE | ARCHIVE | FROZEN`. A new surface that imports a corpus file whose row is not
`CURRENT` must carry an explicit historical frame, or the build fails. This is the same shape as the
publication-record check proposed in the Slice 2 preflight — cheap, local, and it makes the rule
mechanical instead of remembered.

---

## 1 · Forward doctrine fixed by this ledger

These supersede any earlier formulation on any existing surface. Where an existing page contradicts
them, the page is REVISE — the doctrine does not bend to the page.

### 1.1 · The Manifold

> **A Manifold is a declaration, not merely a description — the world's constitution, not its inventory.**
>
> **Its declarations stand trial.**

**Superseded:** the "law + trial record fused" formulation. It is retained as *history* and may be
cited as such; it may **not** be carried forward as current architecture.

**Known collision (must be resolved before any new surface quotes the Manifold):**
`apps/website/src/content/corpus/what_is_manifold_draft_v0_2.md` — a ratified, byte-frozen corpus
piece rendered live at `/what-is-manifold` — currently teaches the opposite:

- `:27` — *"A Manifold is a **description of what a dataset means**…"*
- `:50` — *"A Manifold is a description that **stands trial**."*
- `:57` — *"the artifact is really two things fused: the **law** (what was declared) and the **trial record**…"*

The *substance* survives the change (declaration + standing trial); the *words* do not. This file is
**REVISE**, and until it is revised no new surface may import its Manifold definition.

### 1.2 · The orientation device — newly ratified site language

| element | role |
|---|---|
| **Theory of Data** | law |
| **Manifold** | declared world |
| **Frame-QL** | language |
| **Columna** | machine / system |

Mnemonic: **Law · World · Language · Machine**

**Provenance, stated plainly:** this is a **teaching shorthand introduced by the redesign**. It is
*not* a quotation from an older publication, and an exhaustive search of the repo confirms it has no
prior antecedent — the phrase "orientation spine" appears nowhere, and the four-part mapping exists
in no corpus file. It must therefore be introduced in the redesign's own voice and **never attributed
to a paper**.

**Related collision:** `what_is_manifold_draft_v0_2.md:12` asserts *"The Manifold is the new data
model — the data model of substance, where the relational model was the data model of form"* — a claim
of **succession**, not analogy. If the orientation device is to be framed as analogy-not-equivalence,
that tension is a ruling, not an edit. Recorded, not resolved.

---

## 2 · Ledger schema

Each surface carries **eight** fields. Content disposition and route disposition are recorded
**separately and may disagree** — that separation is the point of the ledger. A page whose prose is
retired may still owe its URL to the outside world.

| field | values / content |
|---|---|
| **current role** | what the surface does today |
| **intended new owner** | The Case · Analytical Governance · Research · Columna · — (supporting) |
| **content disposition** | `KEEP` · `REVISE` · `REFRAME` · `ARCHIVE` · `FREEZE` |
| **route disposition** | `KEEP` · `REPOINT` · `REDIRECT` · `ALIAS` · `RETIRE` |
| **doctrine/content collision** | the specific sentence that fights current doctrine |
| **source of record** | generated / imported md / hand-transcribed / hand-written |
| **replacement / successor** | what carries this forward |
| **external / citation / engineering constraint** | which of P1/P2/P3 applies, and the evidence |

**Content dispositions.** `KEEP` — carries forward as-is. `REVISE` — the idea survives, the words do
not. `REFRAME` — the words survive, the framing/owner changes. `ARCHIVE` — leaves the live argument;
retained and citable as history. `FREEZE` — byte-frozen (P1); may not be edited at all.

**Route dispositions.** `KEEP` — URL unchanged. `REPOINT` — URL unchanged, destination content
changes. `REDIRECT` — URL 301s elsewhere. `ALIAS` — URL kept as a second address for a new canonical.
`RETIRE` — URL withdrawn (permitted only when no P2 constraint exists).

---

## 3 · The ledger — seeded

Legend for constraint: **P1** frozen deposit · **P2** address/link contract · **P3** attribution.

### 3.1 · The argument cluster — the slice's core decision

| surface | current role | new owner | content | route | collision | source of record | successor | constraint |
|---|---|---|---|---|---|---|---|---|
| `/the-argument` | the former homepage essay, moved intact | **The Case** | **REVISE** | **REPOINT** | — | hand-written `.astro`, no corpus backing | becomes the body of The Case | **P2 HIGH** — named in `llms.txt:48`; carries the migrated `#exhibit-a` / `#exhibit-b` fragments that a homepage shim still rewrites into it |
| `/thesis` | the same argument, formal register (1,440 w) | **Research** | **REFRAME** | **KEEP** | — | `columna_thesis_v0_4.md` (body stamps v0.7) | the formal statement under Research | P2 LOW-MED — was in the retired 8-item nav; **P3** version/filename divergence is documented, not a defect |
| `/why` | **a bundle, not an argument** — two corpus docs stacked | **split** | **REFRAME** (essay) + **KEEP** (Seam) | **REDIRECT** | — | two corpus md files | essay → AG page; Silent Seam → Research | P2 MED — linked from *frozen* `what_is_columna_draft_v0_7.md:124`, which itself ships inside `llms-full.txt` |

**The decision this cluster forces:** these three make one argument at three lengths, section-for-section,
one pair sharing an identical heading. `/positions`' doctrine row presents all three as co-equal.
Under §0 the question is not *"which existing page wins"* but *"what does The Case need to be"* — and
the other two become a formal statement and a redirect.

### 3.2 · The Case cluster

| surface | current role | new owner | content | route | collision | source of record | successor | constraint |
|---|---|---|---|---|---|---|---|---|
| `/case` | Cascadia Retail, 3 chapters, build-generated exhibits | **The Case** | **KEEP** | **KEEP** | — | `content/case/*.md` + `case.generated.json` — **best-governed page on the site** | — | **P2 CRITICAL** — referenced by CI (`website.yml`) *and* by shipped Python (`recapture.py:49`). Moving it breaks a released artifact |
| `/ladder` | the comparison gauntlet, 5 fates / fate matrix | **The Case** | **KEEP** | **KEEP** | — | **hand-transcribed** from `ladder_page_v0_3.md` — the site's single worst drift risk | — | **P2 HIGH** — footer deep-link `#the-fast-pipe` on every page |
| `/grain-gap` | popular-register version of Exhibit A | **The Case** | **KEEP** | **KEEP** | — | `datumwise_grain_gap_article_v2.md` | — | P2 LOW-MED. **Currently orphaned** — its only inbound is a component that no longer renders |
| `/story` | launch companion; the three-incident confession | **The Case** | **REFRAME** | **KEEP** | — | `launch_story_v7.md` | confession lifted into The Case | P2 MED — verbatim in `llms-full.txt` |
| `/announcing-columna` | dated launch post | — | **ARCHIVE** | **REDIRECT** (must **chain** `/launch`) | — | `launch_announcement_v2.md` | `/the-argument` | **P2 HIGH despite zero inbound** — the canonical launch URL by ruling; launch posts are the most-shared URL class |
| `/how-to-read-the-wire` | six ideas + an SVG schematic | The Case | **ARCHIVE** | **RETIRE** or REDIRECT | duplicates the four-moods block | hand-written | `/case` | **P2 LOW** — genuinely zero inbound, the only clean retirement in the seed |

### 3.3 · Analytical Governance

| surface | current role | new owner | content | route | collision | source of record | successor | constraint |
|---|---|---|---|---|---|---|---|---|
| `/analytical-governance` | **navigation signpost, by ruling** | **AG** | **KEEP → expand** | **KEEP** | — | hand-written, clean | the full AG page | P2 LOW as URL; **HIGH as citation surface** — the only place the category paper appears |
| `/positions` (index) | the doctrine row + 4 stamped entries | **AG** | **REVISE** | **KEEP** | its doctrine row asserts `/thesis` `/why` `/ladder` `/the-argument` are co-equal — **contradicts §3.1** | hand-written | — | P2 HIGH — `llms.txt:72` |
| `/positions/never-let-your-agent-…` | the authority boundary, argued | **AG** | **FREEZE** | **KEEP** | — | `position_*_v1_1.md` | — | **P1 + P2 + P3** — own DOI byline; verbatim in `llms-full.txt`; is itself a redirect target |
| `/positions/the-two-great-sources-…` | the failure partition, claim form | **AG** | **FREEZE** | **KEEP** | — | corpus md | — | **P1 + P3** |
| `/positions/practice-needs-a-theory` | foundations piece | **Research** | **FREEZE** | **KEEP** | — | corpus md | — | **P1 + P3** |
| `/positions/row-table-join-…` | foundations piece — **distinct site edition** | **Research** | **FREEZE** | **KEEP** | — | corpus md; deliberately diverges from its paper | — | **P1 + P3** — the divergence is ruled, not drift |

### 3.4 · Research

| surface | current role | new owner | content | route | collision | source of record | successor | constraint |
|---|---|---|---|---|---|---|---|---|
| `/research` | corpus map rendered as prose — **not a list** | **Research** | **REVISE** | **KEEP** | the map omits the AG paper entirely (ledger MS-8) | `research_corpus_map_v0_2.md` (body says v0.3 — **three surfaces disagree**) | narrative kept + a generated index below it | **P2 HIGH** — nav door, footer, redirect target |
| `/atlas` | the failure atlas, 5,430 w — largest doc on the site | **Research** | **FREEZE** | **KEEP** | count drift: 67 modes here, 66 in the Seam at `/why`, patched by a hand-written note | corpus md | — | **P1 + P2 HIGH** — its DOI is the **first footer link on every page** |
| `/benchmark` | the Ground Truth landing — *citing*, not carrying | **Research** | **KEEP** | **KEEP** | — | hand-written; blockquote duplicated verbatim in `/ladder` with no shared constant | — | P2 MED-HIGH — fronts a DOI + public repo |
| `/learn/what-is-the-theory-of-data` | hosts the ToD introduction | **Research** | **FREEZE** | **KEEP** | — | corpus md, **byte-identical to the Zenodo deposit** | — | **P1 STRICT** — URL is movable; **the bytes are not** |
| `/learn/frameql-an-introduction` | hosts the Frame-QL introduction | **Research** | **FREEZE** | **KEEP** | — | as above | — | **P1 STRICT** |
| `/notes/cacher` | design-stage roadmap note | Research | **KEEP** | **KEEP** | — | hand-written | — | P2 LOW-MED — the honesty device that makes `/ladder`'s matrix credible |

### 3.5 · Columna

| surface | current role | new owner | content | route | collision | source of record | successor | constraint |
|---|---|---|---|---|---|---|---|---|
| `/columna` | **navigation signpost, by ruling** | **Columna** | **KEEP → expand** | **KEEP** | — | hand-written, clean | the full Columna page | P2 LOW (new URL) |
| `/learn` | a link hub | **Columna** | **ARCHIVE** | **REDIRECT** → `/columna` | two hubs, one pointing at the other; **stale labels** (`6e` vs shipped `6g`; `v1` vs `v2`); lists 2 of 4 positions | hand-written arrays | `/columna` | P2 MED — the `kicker` breadcrumb on 6 pages |
| `/what-is-columna` | framework orientation + **the site's only glossary** | **Columna** | **KEEP** | **KEEP** | — | corpus md | — | **P2 HIGH** — `llms.txt:47`, verbatim in `llms-full.txt`, glossary-anchor target from 5 pages |
| `/what-is-manifold` | the Manifold, up close | **Columna** | **REVISE** ⚠️ | **KEEP** | **§1.1 — teaches "description", contradicts forward doctrine** | corpus md | revised piece | **P1 tension** — ratified corpus vs. new doctrine. **Highest-priority collision in the ledger** |
| `/what-is-frameql` | the language | **Columna** | **KEEP** | **KEEP** | — | corpus md | — | P2 MED |
| `/what-is-a-universe` | the territory a question is asked in | **Columna** | **KEEP** | **KEEP** | — | corpus md | — | **P2 HIGH** — verbatim in `llms-full.txt` |
| `/why-columna-looks-this-way` | where the structure came from | **Columna** | **KEEP** | **KEEP** | overlaps `columna_thesis_v0_4.md` §VI | corpus md | — | **P2 HIGH** — a redirect target *and* verbatim in `llms-full.txt` |
| `/explorer` | live demo-manifold instance | **Columna** | **KEEP** | **KEEP** | — | SSR'd from the shipped package — **no drift possible** | — | **P2 HIGH** — 9 links across 4 frozen corpus files |
| `/install` | install + the only Python-version troubleshooting copy | **Columna** | **KEEP** | **KEEP** | — | hand-written | — | P2 MED — floated site-wide by `AmbientChip` |
| `/docs/framework` · `/docs/frameql` · `/docs/reference` | the manuals | **Columna** | **KEEP** | **KEEP** | **labels stale** (see `/learn`) | repo-root `docs/` | — | **P2 HIGH** — `llms.txt:76-78` |
| `/docs/grammar` | the shipped grammar reference | **Columna** | **KEEP** | **KEEP** | — | **generated from the package — cannot drift** | — | **P2 HIGH** — `llms.txt` gives it an imperative |

### 3.6 · Supporting

| surface | current role | new owner | content | route | collision | source of record | successor | constraint |
|---|---|---|---|---|---|---|---|---|
| `/about` | team, 9 DOIs, contact, disambiguation | — | **REVISE** | **KEEP** | **misses the AG paper and ToD v4.0+; lists ToD v3.1 as current** | hand-written `pubs` array | driven by the publication record | **P3** — attribution honesty is directly at stake |

---

## 4 · What this ledger says Slice 2 should contain

Ordered by dependency. **Not authorized by this document — proposed for ruling.**

1. **The publication record** (`publications.ts` + the no-unregistered-DOI check). It is the only item
   that makes a *class* of failure impossible rather than fixing an instance, it repairs `/about`'s
   attribution (**P3**), it strikes ledger **MS-8**, and §1's `doctrine_status` enforcement rides the
   same mechanism.
2. **The Analytical Governance page**, gated on the two §1 rulings.
3. **`/what-is-manifold` revision** — the highest-priority collision. Until it lands, no new surface
   may import the Manifold definition (transition rule 2).
4. **Record the three paper↔product divergences** in `doctrine_gaps.md` (missing `Escalate`; the two
   `Clarify`-vs-`ERROR` cases from the ToD v6 reconciliation checkpoint).

**Explicitly deferred:** route consolidation and redirect execution. Every REDIRECT above touches a
**P2** surface, and *The Theory of Data in One Afternoon* changes what the redirected pages are *for*.
Migrating externally-cited URLs twice is worse than migrating them late.

---

## 5 · Open questions for ruling

1. **Manifold wording** — §1.1. Revise `what_is_manifold_draft_v0_2.md`, or scope the forward doctrine
   to new surfaces only and let the old piece stand as history?
2. **Analogy vs succession** — §1.2. The corpus asserts the Manifold *succeeds* the relational model;
   the orientation device is framed as teaching analogy. Which governs?
3. **"The Case" naming** — the door named *The Case* points at `/case`, the Cascadia worked example,
   while the argument lives at `/the-argument`. Under §3.1 these swap. Does `/case` get a new name, or
   does the door take a new URL? (`/case` itself is **P2 CRITICAL** and cannot move.)
4. **`/manifold` 404** — the Universe Visual caption links a route that does not exist, from `/case`
   and `/explorer`. Where should "Manifold spec" point?
5. **`doctrine_status` enforcement** — build a real check, or keep transition rule 2 as discipline?
