# CP-3b — the stranger's on-ramp: the ONE package artifact (v0.1, for ratification)
**From: Claude Code, 2026-07-17. Pre-launch beat, proposals-first. Division of labor (standing this beat):
the design desk writes, I wire. Bring one package — the plan, every Tier-1 string drafted, the Tier-2
routing proposal, the 5e disposition, the manuals status. Huayin ratifies once and whole; then I build;
the PR holds to checkpoint. Site-only — rides the existing 0.8.0 pin, no release cut; nothing merges to
`apps/website/**` without Huayin's explicit go.**

---

## 0 · The plan (two tiers, both pre-launch, one ratification)
- **Tier 1 — make the site legible to the stranger's own agent** (light, MY draft). `llms.txt` +
  `llms-full.txt` at the site root; "Ask your AI" self-contained copy-blocks where a stranger's "?" is
  born (the transcript box, the `/explorer` page shell, term chips on the positional pages).
- **Tier 2 — the deep-dive layer** (routing MINE; the front-door piece is pre-supplied + ratified). Wire
  `what_is_columna_draft_v0_4.md` VERBATIM at a route of its own; the Learn surface gathering the manuals
  + Explorer + install + release notes; the 5e disposition.
- **Manuals status** reported below — the framework/FrameQL CP-M2 pass is launch-blocking.
- **Sequencing:** freeze waits on this beat **plus** the manuals pass; then the acceptance walk resumes.

---

## 1 · TIER 1 — every string drafted (MY draft, for ratification)

### 1a · `apps/website/public/llms.txt` (site root, the concise agent index) — DRAFT
```
# Columna

> Columna is a framework for describing what your data MEANS, shipped as a Python library. You
> describe the meaning once — the populations, the measures, which totals are safe to take — and
> Columna checks that description against the data and serves it to whoever asks: an AI agent over
> MCP, or you directly. It works one level up from pandas/polars — on what values mean, not the values.

## The four moods
Every answer is one of four, returned as structured data on one contract (contract_version "1"):
- serve — here's the number.
- disclose — here's the number, plus something you should know about it (e.g. you summed a snapshot
  across months, so you get the per-month figures with a note on why they don't add to a real total).
- clarify — the question can be read two ways; here are the readings, pick one.
- refuse — the data can't honestly answer this, and here's why (the classic: inventory by customer —
  inventory has no customers).

## Core vocabulary
- Manifold — the described, checked data model that agents (or you) query. Not a database, not a schema.
- Universe — one population of facts (transactions; store-days). Every expression evaluates in exactly one.
- Level / edge — the coordinates (grains you can stand at) and the declared paths between them (day→month).
- Measure / derived — a quantity read from the data; a quantity defined from other measures.
- Basis — what a missing row MEANS in a universe: a real zero (events), a gap (spine/product), or a
  membership fact (registry).
- Verdict — the result of checking a described claim against the data: verified, corroborated,
  untestable, or contradicted.
- FrameQL — the query language against the Manifold, as SQL is to tables: an anchor plus what you ask,
  `aov @ cal.month`.
- describe — the machine-readable rendering of a Manifold; what an agent reads first.
- The wire — the answer format: result + context, in one of the four moods; the same contract over MCP
  or straight from the API.

## Start here
- What is Columna? (plain-language orientation): /what-is-columna
- Try it: `pip install columna` then `columna-server demo --play`  (four asks, four moods, seeded data)
- The Explorer (the demo Manifold, live — every measure with its verdict and a query): /explorer
- Full agent orientation: /llms-full.txt

## Go deeper
- The framework manual: /docs/framework
- The FrameQL manual: /docs/frameql
- The reference manual: /docs/reference
- How these documents relate: /how-these-documents-relate
```

### 1b · `apps/website/public/llms-full.txt` (site root, the fuller orientation) — DRAFT
> **Proposal:** `llms-full.txt` = the `llms.txt` header + the FULL ratified "What is Columna?" body
> inlined verbatim (it is already the plain-language orientation, glossary included), then the four-mood
> examples and the demo `describe` pointer. Rather than re-draft prose the desk already ratified, I
> propose `llms-full.txt` is **generated at build** as: `llms.txt` intro → the `what_is_columna` body →
> a "Live demo describe" section pointing at the Explorer's `describe` JSON. **Confirm** this
> compose-from-ratified-parts approach, or tell me to draft net-new full prose.

### 1c · "Ask your AI" copy-blocks (self-contained; paste-into-any-chat) — DRAFT
Each block is one collapsible `<details>` with a copy button; the copied text is definition + surrounding
law + one example + the invitation. Three placements:

**[AI-1] At the transcript box (ExhibitB) — "the wire":**
```
Columna's "wire" is the answer format an AI agent receives from a data query: a RESULT paired with its
CONTEXT, in one of four moods — serve, disclose, clarify, refuse — on one contract (contract_version
"1"), identical over MCP or a direct API call. Example: asking a rate whose two measures live in
different populations returns `clarify` (the readings, to pick from), never a guessed number. Explain
this wire format to me, and answer my follow-up questions about it.
```

**[AI-2] At the `/explorer` page shell (the SITE INSTANCE, not the portable component) — "describe & verdicts":**
```
Columna's `describe` is the machine-readable rendering of a Manifold — every measure, universe, edge,
and derived column, each carrying a VERDICT from checking the description against the data (verified,
corroborated, untestable, contradicted). No physical identifier ever crosses describe — an agent reads
meaning, never table or column names. Example: a universe declares its BASIS (events → a missing row is
a real zero; spine → a missing row is a gap), and describe carries that with its tested verdict. Explain
what describe is and how an agent uses it, and answer my follow-ups.
```

**[AI-3] Term chip on the positional pages (Universe / Basis / the four moods / FrameQL) — templated:**
```
In Columna, {TERM} means: {ONE-LINE DEFINITION}. The surrounding law: {THE RULE IT RIDES}. Example:
{ONE CONCRETE EXAMPLE}. Explain {TERM} to me in plain language and answer my follow-up questions.
```
Filled per chip from the glossary (Universe · Basis · four moods · Manifold · FrameQL · Verdict). The
chip's fill comes from the ratified `what_is_columna` glossary — one source, no drift.

---

## 2 · TIER 2 — the deep-dive layer (routing proposal)

### 2a · The front door — "What is Columna?" (pre-supplied, wire VERBATIM)
- **Source:** `specs/context/what_is_columna_draft_v0_4.md` (attached, preserved byte-identical). I wire
  it verbatim, byte-preserved — **no drafting, no edits to its text.**
- **Proposed route: `/what-is-columna`** (a page of its own). Linked from the **homepage** and from the
  **positional pages' term chips**.
- **Register note honored:** it is deliberately informational/tutorial — a different voice from the
  positional pages. Its ONE upward link to Why/The Ladder sits at its end **by design** — I add **no**
  cross-promotion into it. The paradigm ladder (a–e) renders as the **code block it is** — no diagram.

### 2b · The Learn routing (a gathered surface; routing, not a glossary)
The front-door piece already links to `/docs/framework`, `/docs/frameql`, `/explorer`, `/install`. Today
**none of `/docs/*` exists as a web route** — the manuals live in `docs/` (repo) but are not served on
the site. Proposal: a **`/learn`** hub (or fold into the existing `/how-these-documents-relate`) that
gathers, with term-links down from the positional pages:

| surface | route (proposed) | exists? |
|---|---|---|
| What is Columna? (front door) | `/what-is-columna` | build this beat |
| The framework manual (6e) | `/docs/framework` | **missing** — needs a route rendering `docs/columna_framework_manual_6e.md` |
| The FrameQL manual (v1) | `/docs/frameql` | **missing** — needs a route rendering `docs/frame_ql_manual_v1.md` |
| The reference manual (5e) | `/docs/reference` | **missing** — see the 5e disposition (§3) |
| The Explorer (live demo Manifold) | `/explorer` | ✅ shipped (CP-3) |
| Install | `/install` | ✅ shipped |
| Release notes (0.8.0) | `/releases` or GitHub Release | **decide** — link the GitHub Release, or a site page |
| How these documents relate | `/how-these-documents-relate` | ✅ shipped (the corpus map) |

**Dependency (load-bearing):** the `/docs/*` manual routes **route INTO the manuals**, so they must serve
the **CP-M2-aligned** manuals, not the CP-M1 residency copies. **The manuals routes therefore depend on
the CP-M2 pass landing** (see §4). Proposal: build the `/learn` hub + the front door + `llms.txt` now;
**gate the `/docs/*` manual routes on the CP-M2 merge** (they light up when the aligned manuals land).

### 2c · Homepage + positional wiring
- Homepage: a compact link to `/what-is-columna` (the stranger's first "what is this?") near the exhibit,
  alongside the existing `/explorer` entry point.
- Positional pages (thesis · why · ladder · atlas · grain-gap): term chips (Universe · Basis · four moods
  · FrameQL · Verdict) that (a) carry an "Ask your AI" [AI-3] block and (b) link to `/what-is-columna`'s
  glossary anchor.

---

## 3 · The 5e disposition — ROUTE (labeled), do not supersede
`docs/columna_reference_manual_5e.md` is **not** an old edition of the framework manual — per
`docs/README.md` it is the **reference manual (5th ed.)**: the object model, the definition language
(Chapter 26), the Certificate layer (Part VI) — a **distinct manual** from the framework manual (6e) and
the FrameQL manual (v1). The ambiguity is the *bare "5e"* next to "6e", not a superseded edition.
**Proposal: ROUTE it as `/docs/reference`, labeled unambiguously** on the Learn surface — *"The reference
manual — the object model, the definition language, the Certificate layer"* — so a stranger sees three
DISTINCT manuals (framework / reference / FrameQL), not a stale edition. It rides the same CP-M2
gate as the others (its Chapter-26 status marks are CP-M2 Part 1, already done). **Confirm ROUTE, or rule
supersede.**

---

## 4 · Manuals status — DEMANDED, reported plainly
The framework/FrameQL CP-M2 pass is the deep layer this beat routes into; here is exactly where it stands
(from `origin/wp-manuals-alignment`, latest commit `9b061ae`):

- **CP-M2 Part 1 — DONE** (commit `99deb0e`): watermarks (ADR-035), Appendix B concordance (ADR-033 App A
  verbatim), Part VI head-note, Chapter 26 head-note + 26.2–26.9 two-tier SHIPPED/SCHEDULED/ROADMAP marks.
  The naming gate is discharged (Columna stays; no rename sweep).
- **CP-M2 Part 2 — STALLED / NOT PRODUCED.** Part 2 (the **FrameQL Chapter 2 rewrite** to the shipped
  envelope grammar → the **rendered diff for Huayin's prose pass**, plus Chapter 6 tagging/regeneration
  and the Coframe canonical form → lineage appendix) was **handed to a fresh session on 2026-07-14** — and
  `wp-manuals-alignment` **has not advanced since** (no commits in 3 days). **The Chapter 2 rendered diff
  is NOT ready.** The fresh session appears stalled.
- **Consequence:** this is **launch-blocking** (freeze waits on it), AND the `/docs/*` Learn routes depend
  on the aligned manuals. **Recommend unsticking now** — I can pick up CP-M2 Part 2 (the FrameQL Chapter 2
  rewrite → rendered diff, against the shipped §2c grammar the CP-2 handoff already ruled) as a parallel
  track this beat, bringing you the rendered diff for your prose pass. **Your call: assign it to me, or
  re-task the manuals session.**

---

## 5 · New OF row — the hosted access point (post-launch, ROWED not built)
**OF-11 (proposed):** a single future WP exposing the demo Manifold as a **live socket, two plugs on one
API** — an **HTTP endpoint** for direct FrameQL callers (path (e), today undemonstrable without
installing) and an **MCP endpoint** ("point your agent here"). The wire contract IS the API contract
(`contract_version` "1"), so the lift is **transport + operations only** — no engine or contract change.
Absorbs the earlier tier-3 note. Rowed, not built; not this beat.

---

## What I'm asking you to ratify (once, whole)
1. **Tier-1 strings** (§1a `llms.txt`, §1b the `llms-full.txt` compose-approach, §1c the three copy-blocks).
2. **Tier-2 routing** (§2a `/what-is-columna` route + verbatim wiring; §2b the `/learn` hub + the
   `/docs/*` routes gated on CP-M2; the release-notes link decision).
3. **The 5e disposition** (§3 ROUTE as `/docs/reference`, labeled).
4. **The manuals unstick call** (§4 — assign CP-M2 Part 2 to me, or re-task the manuals session).
5. **OF-11** (§5).

On ratification I build (site-only, no release cut, nothing to `apps/website/**` without your go); the PR
holds to checkpoint.
