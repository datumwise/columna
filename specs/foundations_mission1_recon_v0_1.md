# Readable-site mission 1 — recon and redesign proposal (PROPOSED, not implemented)

Recon of the actual repo and built site against the rulings of 2026-08-26. **No reader-facing file
has been changed.** Every quotation below is from the current tree or the current build.

The eleven requested items are answered in order at §1–§11. Read §0 first: three of the eleven
answers change shape once you know what is already there.

---

## 0 · Four facts that reframe the mission

### 0.1 The bearing is already on the homepage, and it is one word away

`components/home/Bearing.astro`, above the fold, today:

> # First Principles — *Analytics*
> ### Data · Evidence · Intelligence
> datumwise develops first-principles **foundations**, languages, and systems for analytics across
> data, evidence, and intelligence.

So `DATA · CERTAINTY · INTELLIGENCE` is not an element to design. It is **Evidence → Certainty** in
an element that already exists, already sits above the fold, and already says *foundations* in its
supporting line. It is also already the treatment ruling G warns against assuming — a quiet
dot-separated line, **not three cards** — and its own file says why:

> *THE TERRAIN NAMES ARE NOT LINKS. Three big clickable doors would be the old architecture wearing
> a smaller costume… so the words do not promise a destination they cannot yet deliver.*

**The word change is not cosmetic.** *Evidence* is a thing you have. *Certainty* is a question about
what your grounds can bear. Evidence sits **inside** Certainty as one kind of ground — which is the
distinction The Ground for Certainty exists to make. The current word names an input; the ruled word
names the territory.

### 0.2 `/Framework` does not exist

There is no `/framework` route. It is a 404 today. What exists:

| surface | what it actually is |
|---|---|
| `/docs/framework` | **the Columna framework manual, 6th edition (6g)** — an engineering document about the Column-Operator-Frame substrate. Indexed; linked from `/learn` and three corpus documents. It belongs to **Columna**, not to Foundations. |
| `/research` | the source estate — every deposited work with its current record. The closest thing to a "framework listing". |
| `/learn` rung 4 | the label *"Learn the framework"* → `/learn`. The only reader-facing use of the word. |

So item 9 (redirects/SEO for `/Framework → /Foundations`) is nearly empty, and item 2 ("what remains
useful in /Framework") is really a question about **`/research` and `/learn`**. See §2 and §9.

### 0.3 `/research` already has a section headed **"Foundations"** — and it is the catalog

Live on `/research` today:

> ## Foundations
> *The theory itself, and the results that establish it.*
> **The Ground for Certainty** · current record v1.1 · 26 August 2026 · deposit only — not readable here
> **The Two Anchors of a Measure** · v2.0 · … **The Theory of Data** · v6.1 · …

The word is already in use on the site, as a **role label inside a publication catalog** — which is
precisely the thing ruling C forbids `/Foundations` from becoming. If `/Foundations` ships without
addressing this, the site will carry two "Foundations" meaning different things, one of them the
catalog the other is defined against. **This is the sharpest instance of the ruling-J failure mode
already present in the tree.** Repair proposed in §10.

### 0.4 The real legibility problem is not navigation — it is that the corpus is off-site

Of the **17 Core sources** — the works through which datumwise currently states its position — **14
have no onsite route.** `/research` says so, in its own words, fourteen times: *"deposit only — not
readable here."*

| readable on datumwise.ai | The Theory of Data: An Introduction · Frame-QL: An Introduction · A Primer on Frame-QL |
|---|---|
| **deposit-only (PDF/markdown on Zenodo)** | **the other fourteen, including The Theory of Data, The Ground for Certainty, The Statistical Bridge, Analytical Governance** |

A reader who follows a foundational question to its source currently leaves the site. `/Foundations`
cannot fix this by linking harder; linking harder *is* the catalog. **Every design below is shaped by
this constraint**, and §11 puts one bounded repair for it in the sequence.

---

## 1 · Homepage: current structure, and what to change

### Current structure, in order

| # | section | file | ~height | cold-readable? |
|---|---|---|---|---|
| 0 | header — *Analytical Governance · Research · Columna · GitHub* | `site/SiteHeader.astro` | 60px | — |
| 1 | **Bearing** — the identity claim + the terrain line | `home/Bearing.astro` | ≈340px *(capped by ruling)* | **yes** |
| 2 | **Umbrella** — the standing encounter: 52 shops, six umbrellas, "six out of what?" | `encounters/umbrella.astro` | **~70% of the page** | **yes, entirely — the strongest cold surface on the site** |
| — | *the joint:* "Arithmetic will happily continue. / This won't." | | | yes |
| — | the dark wire block: a live `REFUSE` from the shipped package | | | **no** — blocked lineage, reducer, anchor, manifold |
| — | the way on → `/park/when-is-it-data`, then The Theory of Data v6.1 | | | yes |
| — | **"This is one problem out of several, and not the hardest."** | | ~250px, near-empty | yes |
| 3 | *legacy boundary* — a dashed rule marking unfinished work | | | — |
| 4 | "What Columna is" — Manifold, FrameQL, engine, four moods, MCP | | ~460px | **no** — densest prior-knowledge block on the page |
| 5 | "Where to go" — an ordered 8-rung directory | | ~840px | mostly |
| 6 | about + design partners | | ~260px | yes |

### The recommendation: one word, and one existing sentence made to pay off

**Do not add a three-item composition to the homepage.** Two independent reasons, both already in
the tree:

1. **It was tried and ruled out, and the reason still holds.** `components/home/ThreeQuestions.astro`
   exists, complete, and is **imported by nothing**. It was retired on 2026-08-25 with the reason
   recorded in `index.astro`:

   > *the Three Questions composition — **three short explanations cannot carry three foundations
   > before a reader has experienced any of them**.*

   That ruling is not in tension with the new one. It is the argument **for** putting the deep
   treatment at `/Foundations`: the homepage names the terrain, and the page a reader chooses to
   visit explains it. Ruling G says exactly this.

2. **The homepage already has the seam, and it is currently unpaid.** After the encounter ends, the
   page says *"This is one problem out of several, and not the hardest"* — and then goes to the
   product. It names a plurality of foundational problems and never says what they are. That
   sentence is the natural, already-composed place for the bearing to become a destination.

**So, three changes, in decreasing confidence:**

| # | change | why |
|---|---|---|
| **1a** | `Bearing.astro`: `Data · Evidence · Intelligence` → **`Data · Certainty · Intelligence`**, and the lede's "across data, evidence, and intelligence" with it. Also `<title>`/meta description on `index.astro`. | The ruled bearing, in the element built for it. One line of copy. |
| **1b** | The territory line after the encounter gains **one sentence and one link** — e.g. *"This is one problem out of several, and not the hardest. The others are where we think analytics actually begins:"* → **Foundations**. Still prose, still no cards. | Pays off the promise the hero makes, at the only point in the page where a reader has *earned* the abstraction by having just experienced one instance of it. |
| **1c** | `/learn` rung 4, *"Learn the framework"*, is retitled and re-pointed — it is the only reader-facing use of the word "framework" and it points at a Columna manual index. | Removes the word from the reader-facing vocabulary without touching the manual itself. |

**Do not** make the terrain words links in the Bearing. The file's ruling holds even once
`/Foundations` exists: three big clickable words at the top of the homepage *is* the old architecture
in a smaller costume, and it invites a reader to pick a territory before they have any reason to care
which. The single link at 1b is earned; three links at 1a are not.

**Deliberately not proposed:** deleting the legacy boundary, rewriting "What Columna is", or
re-sequencing the directory. All are real, all are out of this mission.

---

## 2 · The "/Framework" surfaces: keep, move, retire, re-author

Since `/framework` does not exist, this reads against the three surfaces that carry the role.

### `/docs/framework` — the Columna framework manual (6g)
**KEEP, UNCHANGED, AND DO NOT RENAME.** It is an engineering manual about the shipped substrate. It
is Columna's, not Foundations'. Renaming or redirecting it would be the exact confusion the new
concept exists to end — *"Framework" implied a fairly complete system*, and this document genuinely
is a manual for one. Its only defect is that `/learn` labels it **6e** while it renders **6g**
(stale by two editions) — a one-line correction, worth doing whenever `/learn` is next touched.

### `/research` — the source estate
**KEEP as the catalog; it is doing a job `/Foundations` must not do.** This is the cleanest division
available: `/research` answers *what has datumwise deposited, at what version, with what standing*;
`/Foundations` answers *what are the foundational problems and where is the discussion*. One is a
register, one is a discussion.

- **Conflicts:** its section heading **"Foundations"** (§0.3, §10).
- **Preserve:** the registry-derived rendering. Nothing on `/research` is hand-typed; it re-resolved
  to *The Ground for Certainty v1.1* automatically yesterday. `/Foundations` should inherit that
  discipline for every publication fact it shows.
- **Re-author eventually, not now:** its role vocabulary (`FOUNDATION`, `NORMATIVE`, …) predates the
  three territories and will need reconciling once they are ruled reader-facing.

### `/learn` — the practitioner index
**KEEP, RE-SCOPE LATER.** It is a Columna orientation index (manuals, Explorer, install) that has
accumulated non-Columna entries. Under `Foundations · Doors · Ask · Columna` it is a **Columna**
surface. Not this mission.

### What genuinely needs re-authoring
Nothing existing. `/Foundations` is a **new composition**, not a rewrite of a page — which is why
this proposal recommends building it beside the current site rather than converting anything.

---

## 3 · `/Foundations` — information architecture and reader journey

### The journey to design for

The Yes Machine ends:

> *"Governance cannot be stronger than its account of the thing being governed. That is why better
> governance eventually requires **better foundations**."* … *"Into the identity and laws of
> analytical data. … Into the passage from governed data to statistical claims. Into what happens
> when those claims enter interpretation, delegation and action."* … *"And to do that, we have to go
> back to **the foundations**."*

Two consequences, and they decide the design:

1. **The article's last word is the route name.** `/foundations` is the landing surface — a top-level
   route, not a section of `/research`.
2. **The reader arrives holding the questions and none of the proper nouns.** The article names the
   three territories *in prose, in order,* and names no theory. So a page that opens with theories is
   discontinuous with the sentence that sent them. **Ruling C is not a stylistic preference; it is the
   only thing continuous with the referrer.**

### The shape

```
/foundations
├─ Opening              why foundations, in four or five sentences. No proper nouns.
├─ Data                 the questions · where we are · ways in · what is unsettled
├─ Certainty            the questions · where we are · ways in · what is unsettled
├─ Intelligence         the questions · where we are · ways in · what is unsettled
├─ How these relate     including where Analytical Governance stands (not inside any of them)
└─ Where the record is  one line → /research. Not a list.
```

**Each territory is one continuous section, and each has the same four moves — but not the same
amount to say.** The four moves are what let maturity differ without symmetry breaking the design:

- **the questions** — reader-facing, no priors. This is the heading matter.
- **where we are** — honest prose: what we think we have established, in what depth.
- **ways in** — two or three, at most, chosen for a reader, not enumerated for completeness.
- **what is unsettled** — named openly. This is the section that carries Intelligence and stops the
  page from being a brochure.

**"What is unsettled" is load-bearing, not decoration.** It is what makes the page a place where
*foundational discussions happen* (ruling A) rather than a summary of holdings, and it is what makes
DATA's thickness and INTELLIGENCE's thinness read as the same kind of honesty rather than as an
embarrassment on one side.

---

## 4 · Content outline (headings and purpose; not copy)

### Opening
> **Purpose:** say why foundations, without naming a single datumwise work. Should be readable by
> someone who has just finished a LinkedIn article and knows nothing else. Should end by naming the
> three territories as *where we currently think the foundational problems are*, with the
> can-evolve caveat of ruling B stated once, plainly, and never repeated.

### Data — *what is the analytical thing we are working with?*
> **Questions.** What gives analytical data identity? What transformations preserve or change it?
> How do analytical objects stay derivable and consistent as they move through systems?
> **Where we are.** The most developed territory. Identity, derivability, consistency have an
> account with proofs; a query language exists that can only ask for meaning a model declares.
> **Ways in.** *When is it data?* (a four-minute walk, already built at `/park/when-is-it-data`) ·
> The Theory of Data in One Afternoon (`/start-here`) · the deposited account.
> **What is unsettled.** (Candidates exist in `specs/doctrine_gaps.md` and `specs/open_forks.md` —
> these are real, dated, and already written down. Selecting which are reader-facing is editorial and
> is a decision for you, not for me.)

### Certainty — *what gives us sufficient grounds to rely on what we know?*

> **Know before writing this section:** `/evidence` is already the de facto Certainty surface. Its
> own header names the five deposited works that govern it — *The Statistical Bridge* v3.0, its
> Primer, *Where Does Probability Live?*, *Certifiable State*, *The Two Jobs of the Conditioning
> Bar* — and rules that the page *"may compress, sequence, visualize and connect them. It does not
> extend them, and it invents no example the corpus does not already carry."* **The Ground for
> Certainty is not among them, and has no onsite route** (C10). So this section is not writing on
> blank ground: it is the first surface that would put the territory's keystone and its existing
> page in the same frame.
> **Questions.** What is carrying the confidence? How far do those grounds reach? What happens as
> evidence becomes inference, claim, decision, action?
> **Where we are.** Substantial and recent. Grounds of certainty distinguished, their reach bounded,
> their composition described; the passage from governed evidence to licensed claims has its own
> account.
> **Ways in.** The Ground for Certainty (current foundational publication) · the Statistical Bridge.
> **What is unsettled.** The reach of behavioural evidence; how grounds compose without laundering.
> **Distinction to hold visibly here** (ruling E): *Certainty* is the territory · *Theory of
> Certainty* is the account · *The Ground for Certainty* is the current publication. This is the one
> place on the site where all three appear together, so it is the page that must model the
> distinction rather than state it. See §5 for the mechanism.

### Intelligence — *how do intelligent actors understand, choose, and act?*
> **Questions.** What changes when intelligence itself becomes part of the analytical machinery?
> How should humans work with intelligent agents, and machines with other machines?
> **Where we are.** *Least settled, and said so.* See §6 — there is one real position here and it
> should carry the section.
> **Ways in.** The position piece, and the governed-authority boundary as it exists in the shipped
> system.
> **What is unsettled.** Most of it. Named specifically, not vaguely.

### How these relate
> **Purpose:** the relations, and the boundary. Analytical Governance is **not** filed under any of
> the three (ruling F): it is the discipline governing the legitimacy of the analytical service,
> which *encounters* foundational problems in all three. Say that once, in a form a reader can hold.
> **Do not** draw a pipeline, a stack, or a Venn diagram. Data → Certainty → Intelligence is not a
> sequence, and any left-to-right arrangement will be read as one.

### Where the record is
> One sentence → `/research`. The catalog is one link away and never reproduced.

---

## 5 · Linking works without becoming a catalog

**The site already has the right pattern, built and shipped**: the `NEIGHBOURS` block on
`/analytical-governance` §*Where this sits*. Each row is **name · relation-verb · prose**, hairline
rules, no cards, href optional:

```js
{ id: 'tod', name: 'The Theory of Data', href: '/learn/what-is-the-theory-of-data',
  relation: 'supplies interior law to',
  text: 'Laws of governed analytical identity, derivability and consistency. It is narrowly
         that: not a general ontology of analytical objects, and not the law of every world the
         service crosses.' }
```

**Why this solves the catalog problem.** A catalog row says *here is a work*. A relation row says
*here is how this work stands to this question* — and a relation verb cannot be written without
taking a position, which is what makes it a discussion rather than a list. It also makes the ruling-E
distinction structural instead of stated: the territory is the section, the account is named in the
prose, and the publication is the row with the href. Three different things in three different
positions, so a reader cannot flatten them without noticing.

**Three rules for `/Foundations` rows:**

1. **Two or three per territory, chosen for a reader.** Completeness is `/research`'s job. If a row
   is there because the work exists rather than because a reader needs it, it belongs on `/research`.
2. **Every publication fact registry-derived**, via `data/publications.ts` — the mechanism that
   moved `/research` and `/analytical-governance` to *The Ground for Certainty v1.1* with no edit.
   No version string or DOI typed into the page; `check_publications.py` will fail the build if one
   is (`derived` class, G7).
3. **A row may name a work with no onsite route, and must say so** — `/research` already has the
   honest phrasing (*"deposit only — not readable here"*). Given §0.4 this will be most of them.

---

## 6 · The Intelligence territory — recommendation

**Recommendation: use the treatment the site has already ruled and already shipped.** `/evidence`
solved this problem in August, in one paragraph, and it is better than anything I would propose:

> **Intelligence — begins after this page ends.** A licensed claim does not yet determine what a
> person or an agent may conclude from it, communicate, delegate, or act upon. That is a different
> jurisdiction with a different governed object, **and it is not built here — named so that its
> absence is a boundary rather than a gap.**

With the ruling that produced it, in the same file:

> *Intelligence appears as an ACKNOWLEDGED ABSENCE rather than a fourth box, because a licensed
> claim genuinely does not yet settle what anyone may conclude or do — and that jurisdiction is not
> built here.*

**An absence that is named is a boundary. An absence that is unnamed is a gap.** That sentence is
the whole treatment, it is already datumwise's, and `/Foundations` should inherit it rather than
invent a second way of saying it.

### What actually exists — measured, not asserted

Across **110,149 words** of deposited text, material substantively *about* intelligence, agency or
human–machine collaboration is roughly **1,100 words — about 1%**. There is **no deposited work whose
subject is intelligence**, no route about it, no `role` for it in the source catalog, and no
jurisdiction for it in the corpus ruling. Core-corpus counts: **DATA ~10 · CERTAINTY ~5 ·
INTELLIGENCE 0.**

What is real, in descending strength:

| asset | what it is | honest reading |
|---|---|---|
| **The Ground for Certainty §7, "The intelligent-agent problem"** (~416 w) | *"Capability expands what the actor can do. It does not automatically strengthen the ground on which we are certain what the actor will choose or what authority its output should carry."* | **The strongest intelligence material in the corpus** — and it is a section of a *certainty* paper. Genuinely developed as a corollary, not as a territory. |
| **The Ground for Certainty §2, "Theory of other"** (~253 w) | goals · intellect · principles · environment; *"A door may in fact be unlocked while the other believes it is locked."* | A sketch, explicitly deferred to work that **is not published**. |
| **Never Let Your Agent Touch the Database** (2,487 w) | *"Treat the model as an untrusted searcher. Put a small, deterministic, governed boundary between the model and the database."* | Fully developed **as architecture**. A containment argument about *authority placement* — it says almost nothing about how machines reason. |
| **Analytical Governance §9** (~169 w) | the blast wall; *"the agent may propose or explain; the governed serving boundary determines what the result is entitled to become"* | Intelligence **as a use case**, deliberately subordinated: the paper's own words are *"one application"*. |
| **"Interpretation is useful. Interpretation is not authority."** | the locked line in the retired `ThreeQuestions.astro` | A genuine position, already written, already ruled, protected in its own file against being rewritten in Data's vocabulary. |
| **The Open Planner** · **the nine-model study** · **Ask itself** | a research programme, an empirical study, and a running governed agent | All real. None is a theory of the actor — the Open Planner *deliberately* treats the searcher as a black box, which is its point. |

### The forward reference that points at nothing

The Ground for Certainty §2 defers part of this territory to **Trust**, and Trust is not in the
corpus. `ask-authority.json` records why, and it is a decision rather than an oversight:

> *Trust v0.6 deliberately NOT admitted, in any layer: **it is developing work**, and registering it
> at all would make the a1 and s1 hallucination traps assert something false.*

So the shape of the section is already determined by facts on the ground: **one position held firmly,
one published corollary, one architectural containment argument, and a named body of developing work
that is deliberately not yet claimed.** That is not a thin section pretending to be thick. It is an
accurate one.

### So the section should

1. **Open with the boundary sentence**, in `/evidence`'s register.
2. **Carry the one thing held firmly** — *interpretation is not authority* — and its support line.
3. **Name what is open specifically**: what an agent's proposal *is*, what makes delegation
   legitimate, what a machine owes another machine, and what grounds could warrant relying on an
   actor whose motives are not established. **A specific gap reads as a research programme; a vague
   one reads as an absence.** That difference is the entire treatment.
4. **Be visibly shorter — perhaps a third of Data's — and not apologise for it.** Ruling D asks for
   the unevenness to remain visible; proportion shows it more honestly than a disclaimer does.
5. **Not pre-empt the banked AI-agent article, and not name a "Theory of Intelligence."** Neither is
   a temptation to resist so much as a line already drawn by you.

---

## 7 · Navigation implications

Today: **Analytical Governance · Research · Columna** + GitHub (hardcoded in `SiteHeader.astro`, no
data file; mobile is a no-JS `<details>` sheet with the same items).

Target: **Foundations · Doors · Ask · Columna**.

| door | status | what has to happen |
|---|---|---|
| **Foundations** | new | the page (§3–§4) |
| **Doors** | **not empty — partially built under another name.** `/park/when-is-it-data` is already *"a four-minute walk"*, already a small exploratory piece, already linked from the encounter. `/positions/*` are adjacent but heavier. | a container route and an editorial ruling on what a Door is vs a position. **Out of this mission.** |
| **Ask** | live at `/ask`, **not in the nav today** | promotion, once it has reviewed answers (your step 4) |
| **Columna** | live and in the nav | absorbs `/learn`, `/docs/*`, `/install`, `/case`, `/explorer` |
| **Analytical Governance** | in the nav today, **not in the target four** | **This is the real navigation question, and it is doctrinal, not structural.** |

### The one navigation problem worth your ruling now

`Foundations · Doors · Ask · Columna` has **no place for Analytical Governance**, which is currently
the site's *first* nav door and, by ruling F, is not filed under any territory. Three options:

- **(a) a fifth door.** Honest; weakens the four-part story.
- **(b) inside Foundations.** *Contradicts ruling F* as literally as possible.
- **(c) between Foundations and Columna, as its own thing** — the discipline that connects the
  foundational terrain to the engineered system. Matches the AG page's own self-description and
  matches ruling F's "necessarily encounters foundational problems in all three".

**Recommendation: (c)**, which in practice is (a) with a reason — five doors where the fifth is
positioned, not appended. But this is a doctrinal call about what datumwise *is*, so it is yours.

Also worth knowing: **three navigational surfaces currently disagree about what the site is.** The
header offers 3 destinations, the homepage directory 8, the footer 4 — and they share exactly one
(`/research`). Any nav change should reconcile at least the header and the homepage directory, or
the new architecture will be contradicted by the page that introduces it.

---

## 8 · Reuse vs new composition

**Reusable as-is — no new design work:**

| pattern | where | use for |
|---|---|---|
| the **relation map** (`NEIGHBOURS`) | `/analytical-governance` | §5, the whole linking model |
| `ThreeQuestions.astro` | built, unimported | **the territory sections' bones.** One continuous field, hairline dividers, `grid-template-columns: repeat(3, 1fr)` collapsing to 1fr at 56rem, and a comment that already forbids cards. It also already carries the **jurisdictions-not-planes** rule (ruling B) and the locked Intelligence line (§6). |
| the design-system registers | `tokens.css` / `redesign.css` — `ds-paper`, `ds-wire`, `ds-section`, `ds-measure-wide`, `ds-proposition`, `ds-label`, `ds-mark`, `ds-pillar` | all of it |
| `publications.ts` — `citation()`, `currentRecord()`, `work()` | `data/` | every publication fact (§5 rule 2) |
| the hairline **ordered list** | homepage directory | "ways in" |
| the **preserved-route** pattern | `/history/analytical-governance-v1-1` | if anything is superseded later |

**Genuinely new:**

1. **The opening.** Nothing on the site addresses a reader who has read a LinkedIn article and
   nothing else. `/start-here` is the nearest and is aimed at practitioners *"opening from failures
   they have personally debugged"* — a different reader.
2. **"What is unsettled."** No existing pattern shows open questions to readers. `doctrine_gaps.md`
   and `open_forks.md` are internal ledgers, not reader surfaces. This is the page's most novel and
   most valuable element and it is where the composition work actually is.
3. **The three-way relation statement** (§4, "How these relate") — must be prose, because every
   diagram of three things implies a symmetry or a sequence that ruling B denies.

**A caution about reusing `ThreeQuestions.astro`:** its content is *retired doctrine*. `Evidence`
must become `Certainty` and its answer (*"Evidence licenses claims only through an explicit governed
passage"*) is **Statistical Bridge doctrine — a part of Certainty, not the whole of it**. Reuse the
composition; re-author the content.

---

## 9 · Redirects, history, SEO

**Almost nothing is owed, because `/framework` never existed.**

- `/framework` → 404 today. No inbound links, no sitemap entry, no external exposure. **No redirect
  is required.** Adding `/framework → /foundations` is cheap insurance against a guessable URL and is
  the site's own standing rule (*"a 404 is never acceptable for a live/guessable URL"*) — recommended,
  not required.
- **`/docs/framework` must NOT redirect.** It is indexed, linked from `/learn` and three corpus
  documents, and it is a *Columna manual*. Redirecting it to `/foundations` would send a reader
  looking for operator semantics to a page of foundational questions.
- `/foundations` is a **new route** — additive, no history to preserve, sitemap picks it up
  automatically.
- The mechanism, if wanted: `astro.config.mjs` `redirects` (4 entries today; Astro emits meta-refresh
  stubs). **Note a live defect:** the sitemap filter excludes only 2 of the 4 stubs, so two
  redirect stubs are currently advertised as canonical URLs. Small, real, unrelated — worth fixing
  whenever that file is next opened.
- **The one genuine SEO risk is not a redirect.** It is that `/research` currently owns the word
  *Foundations* on this domain (§0.3). Two pages competing for it is worse than either.

---

## 10 · Conflicts between the rulings and the current site

| # | conflict | severity | proposal |
|---|---|---|---|
| **C1** | **`/research` has a section headed "Foundations"** — a role label on a publication catalog, the exact thing `/Foundations` must not be. | **high** — a ruling-J distinction-collapse already in the tree | rename that section on `/research`. It is describing *deposited works that establish the theory*, so something like **"The theory and its proofs"** says what it means. One heading, one page. |
| **C2** | The header's first door is **Analytical Governance**, absent from `Foundations · Doors · Ask · Columna`, and ruling F forbids filing it under a territory. | **high**, doctrinal | §7 — needs your ruling, recommend (c) |
| **C3** | **14 of 17 Core works are not readable on the site.** A page organised around foundational *discussions* mostly links off-domain. | **high**, structural | §11 step 5 — one bounded repair |
| **C4** | `ThreeQuestions.astro` was retired 2026-08-25 with a recorded reason. Reusing it needs that ruling addressed, not ignored. | medium | it is *completed*, not contradicted: the reason was that three explanations cannot precede experience — on `/Foundations` the reader has chosen the abstraction. Say so in the file. |
| **C5** | `/Foundations` should discuss *"established ideas and traditions from elsewhere"* and *"current research"* (ruling A). **No site surface currently cites anyone outside datumwise** except the disambiguation footer, and Ask types external sources as a separate class that may never establish a datumwise position. | medium | the page needs a stated convention for citing outside work — otherwise the first external citation will read as endorsement. Worth ruling before composition. |
| **C8** | **`/analytical-governance` carries a standing prohibition, authored 2026-08-26 — one day old:** *"THE THEORY OF CERTAINTY IS A POINTER, TWICE … and **no domain triad, named or implied**."* And `/evidence` carries **two hard guards** against drawing Data · Evidence · Intelligence as three equal boxes, plus a ruled sentence: *"Evidence is a standing acquired through a governed crossing, **not a sovereign jurisdiction**."* | **high** — the newest reader-facing rulings on the site are aimed at exactly this move | see below. Not a blocker, but it must be ruled explicitly rather than quietly overridden. |
| **C9** | **CV-9, already open in `publication_corpus_coverage_v0_1.md`:** the word *jurisdiction* carries two meanings — `/evidence` denies Evidence is a "sovereign jurisdiction" while `ThreeQuestions` calls the three "different JURISDICTIONS". Logged 2026-08-22, *"OPEN, editorial, not a blocker"*. `/Foundations` is the page that forces it. | medium | rule the two senses apart, or pick a different word for one of them, before composition |
| **C10** | **The Ground for Certainty — the work that most literally names the Certainty territory — has no onsite route at all,** and `/evidence`, the de facto Certainty surface, was built from the five-work Statistical Bridge cluster and does not mention it. | **high**, and it is the sharpest instance of C3 | §11 — the Certainty section cannot be written honestly around a keystone the reader cannot reach |
| **C6** | `/learn` labels the framework manual **6e**; it renders **6g**. | low | one line |
| **C7** | Sitemap advertises 2 redirect stubs as canonical. | low | one line |

### C8 in full, because it deserves more than a table row

These are not stale guards. They are the most recent reader-facing rulings on the site, and they were
made for a reason that is still good: **promoting Evidence to a sovereign province by drawing it as
one.** `/evidence`'s own comment says the layout must never draw the three as equal boxes *"before
the sentence beneath it could deny it"*.

**The rename relieves this rather than aggravating it, and that is the argument for proceeding.**
*Evidence* is a standing a claim acquires by crossing — so a page that drew it as a third world would
contradict the page's own thesis. **Certainty is not a standing; it is a body of law about grounds**,
which is what The Ground for Certainty is. The word the guards were written against is the word being
retired.

What still has to be honoured, and what `/Foundations` should therefore inherit:

- **no three equal boxes, no diagram, no left-to-right sequence.** Ruling B says the same thing from
  the other direction. The composition in §8 is a continuous field with hairline dividers, and
  §4's "How these relate" is prose for exactly this reason.
- **`/analytical-governance` stays as it is.** Its prohibition is page-scoped and ruling F keeps AG
  outside the triad anyway. It should not gain a triad, and nothing here asks it to.
- **`/evidence`'s boundary paragraph is an asset, not an obstacle** — it is the treatment §6 adopts.

**Recommendation: rule C8 explicitly** — that the triad may be *named* on `/foundations` and the
homepage bearing, may not be *drawn* anywhere, and that `/analytical-governance` and `/evidence` keep
their guards unchanged. That is one sentence, and without it the next person reads a 2026-08-26
prohibition and a 2026-08-27 page that appears to ignore it.

**No conflict found** between the rulings and the registry/publication architecture. The
territory/theory/publication distinction (ruling E) is already *enforced* there — `workId` is
durable, `canonicalLabel` follows the deposited title *because that is how the corpus cites the
work*, and a superseded record keeps its own title forever. `/Foundations` inherits a machine that
already refuses to collapse the distinction it is being asked to display.

---

## 11 · Smallest bounded implementation sequence

Each step is independently shippable and independently revertible.

| # | step | touches | why here |
|---|---|---|---|
| **1** | **The word.** `Evidence → Certainty` in `Bearing.astro`, the homepage lede, `<title>`/meta. | 2 files, ~4 lines | The ruled bearing goes live immediately, correctly, with no new page. Zero risk. |
| **2** | **C1 — rename `/research`'s "Foundations" section.** | 1 heading | Clears the word *before* anything claims it. Doing this after step 3 means shipping the collision. |
| **3** | **`/foundations`, opening + the three territories**, questions-first, no relation rows yet. | 1 new page | The page exists and is honest before it is complete. |
| **4** | **Relation rows** (§5) + "How these relate" + the `/research` line. | same page + `publications.ts` | Needs step 3's prose to sit against; splitting it keeps the catalog pressure visible as its own decision. |
| **5** | **The homepage payoff** — one sentence and one link at the territory line (1b). | `index.astro` | Deliberately **last**: the homepage should not point at a page until that page is worth arriving at. |
| **6** | **Nav**, once C2 is ruled. | `SiteHeader.astro` | Blocked on your ruling, not on code. |

**One candidate for step 3.5, offered because it is small and because C10 is real:** give **The
Ground for Certainty** an onsite route, as `/learn/what-is-the-theory-of-data` does for The Theory of
Data — the deposited text rendered byte-faithfully at its own address. It is 3,772 words, already in
the repo at `services/ask/deposits/w-theory-of-certainty.r02.md`, already Zenodo-verified, and the
edition-pinned-route pattern is built and ruled. It would give the Certainty section something to
send a reader *to* rather than *away to Zenodo*, and it is the cheapest possible dent in C3. **It is
a publication-surface decision, so it is yours, and it is not in the sequence above.**

**Out of this sequence, on purpose:** Doors, Ask seeding, `/learn` re-scoping, the legacy boundary,
the three-surfaces-disagree problem (§7), and the deposit-readability repair (C3) — which is the
largest genuine obstacle to a readable site and deserves its own mission rather than a corner of this
one.

**Recommended cold-reader test, when the sequence completes:** read The Yes Machine to its last line,
then land on `/foundations` — and check the one thing that matters, which is whether the three words
arrive as *questions the article already raised* or as *three things this company sells*.

---

## What I did not do

- Changed no reader-facing file.
- Wrote no copy. §4 is headings and purpose, as asked.
- Did not read The Yes Machine as a site asset: it is not in this repo (it is an attachment), so §3
  quotes the draft rather than a published article.
- Ran no model evaluation. Under the rule of 2026-08-26 this tranche changed nothing agent-facing.
