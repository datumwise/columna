# External-AI probe battery — 2026-07-29 — **RE-RUN** (day 2)

**The first re-probe against the 2026-07-27 launch-eve baseline.** Three captures, relayed by
Huayin, uploaded **2026-07-29 03:46 UTC** — roughly **40 hours** after the day-zero battery.
Bodies preserved **verbatim**; the PDF is byte-identical to what was handed over.

**Modes per `../../PROBE_MODE_SCHEMA.md`** (ratified 2026-07-29, minted from this re-run).

| capture | file | mode | Q2 "is datumwise a company?" |
|---|---|---|---|
| **A** | `rerun_a_five_questions.md` | ✅ **found-and-right** — five distinct deep URLs | **No** — *"independent open-source research project"* ✅ |
| **B** | `rerun_b_overview.md` | ✅ **found-and-right** — deep URLs + a correct Zenodo DOI | **No** — *"not described as a formal company"* ✅ |
| **C** | `rerun_c_what_is_columna.pdf` (10pp, 66 citations) | ❌ **not-found-confabulated** | not asked; the whole capture is about a different product |

---

## ATTRIBUTION — AMENDED 2026-07-29 (Huayin), and the per-assistant diff it unlocks

Filed A/B/C; amended the same day by the desk:

| capture | assistant | session | mode |
|---|---|---|---|
| **A** `rerun_a_five_questions.md` | **ChatGPT** | fresh | `found-and-right` |
| **B** `rerun_b_overview.md` | **Grok** | fresh | `found-and-right`, carrying OF-22 |
| **C** `rerun_c_what_is_columna.pdf` | **Perplexity** | fresh | `not-found-confabulated` |

B being a **fresh** session resolves its self-dated *"as of July 28-29"* span as a date range rather
than a continuing conversation — the primed-by-context worry does not apply here.

### ⚠ THE HEADLINE INVERTS: the assistant that was wrong on day zero did not correct. It got worse.

The 40-hour story told without attribution was *"Q2 corrected across assistants."* With names on the
captures, that reading does not survive:

| assistant | 2026-07-27 (day 0) | 2026-07-29 (day 2) | movement |
|---|---|---|---|
| **ChatGPT** | `found-and-right` — Q2 correct | `found-and-right` — Q2 correct, now with five deep-URL citations | **stable, deepened** |
| **Grok** | `not-found-honest` — *"the searches… returned no usable results"* | `found-and-right` — deep URLs + a correct Zenodo DOI | **the real correction** ✅ |
| **Perplexity** | `found-and-wrong` — *"**Yes**, Datumwise is described as a company"*, citing `/about` while contradicting it | **`not-found-confabulated`** — 66 citations, a different product, none of our pages | **REGRESSION** ❌ |

**Nobody corrected Q2.** Q2 was answered wrongly on day zero by exactly one assistant — Perplexity —
and forty hours later Perplexity was no longer answering the question about us at all. The
improvement in the set comes from **Grok**, which moved from *honestly not finding us* to *finding us
and getting it right*. Two different assistants; two different events. Averaged into "the assistants
corrected", they cancel into a sentence that is true of nobody.

**The regression is the more important half, and it runs against the intuitive story.** Perplexity is
the **search-first** engine of the three — the one whose answers are constructed from retrieval at
query time, and therefore the leading indicator for everything downstream of search. On launch eve it
found us and mis-read us. Two days after launch — with the site live, `robots.txt` and `sitemap.xml`
added (#112), and seven papers on Zenodo — it stopped finding us **and filled the gap with the
confusable cluster**. Whatever is happening in that index is moving away from us, not toward us, and
it is the one surface where the disambiguation line has to earn its keep.

That single fact is what the disambiguation row (shipped 2026-07-29 in `llms.txt`, the site footer,
and `/about`) is now up against. **The next probe re-tests Perplexity first.**

### ⚠ AND: the day-zero attribution is in conflict — unresolved, deliberately

The desk's day-zero list disagrees with what `../2026-07-27/external_ai_probes/` has **already
filed**, for two of the three captures. Perplexity agrees in both accounts. **Grok and ChatGPT are
swapped.** See `../2026-07-27/external_ai_probes/ATTRIBUTION_CONFLICT.md` for the byte-level evidence.

**Which findings survive the conflict, and which do not:**

| claim | robust to the swap? |
|---|---|
| **Perplexity: `found-and-wrong` → `not-found-confabulated`** | ✅ **YES** — Perplexity is consistent in both accounts. The headline regression stands regardless. |
| One assistant moved `not-found-honest` → `found-and-right` | ✅ yes — but **which one** depends on the ruling |
| One assistant was stable `found-and-right` | ✅ yes — likewise |
| **Grok carries OF-22's "metrics engine"** on day 2 | ✅ yes — day-2 attribution is not in dispute |
| *"Grok was the primed-by-context capture on day zero"* (published in #111) | ❌ **NO** — under the desk's list that capture is **ChatGPT's** |

Until the conflict is ruled, the middle two rows of the movement table above are **provisional**, and
this file says so rather than presenting a clean diff built on an unresolved mapping.

## FINDING 1 — the corpus is working, and the day-zero identity error is corrected

**Both captures that found us get Q2 right, and both cite deep pages rather than the homepage.**

Day zero, Q2 disagreed three ways and **two of three were wrong about our own words** — Perplexity
asserting *"Yes, Datumwise is described as a company"* while citing the page that says the opposite.
Forty hours later:

> **A:** *"**No—not as it is publicly presented.** datumwise describes itself as an **independent
> open-source research project**… maintained by **Huayin Wang (research)** and **Irena Wang
> (engineering)**."*

> **B:** *"**No.** Datumwise is not described as a formal company… The site explicitly calls it 'an
> independent open-source research project.' There is no public information indicating incorporation
> (Inc., LLC, etc.), venture funding, employees beyond the two named individuals."*

Both go further than the answer: they name the *absence* of incorporation markers, which is the
`/about` claim reconstructed rather than parroted.

**The citation depth is the stronger signal.** These are not homepage summaries:

| capture | datumwise.ai URLs cited |
|---|---|
| A | `/thesis`, `/how-these-documents-relate`, `/why` ×3, `/atlas` ×2, `/` |
| B | `/announcing-columna` ×2, `/atlas` ×2, `/why` ×2, `/` ×3, the GitHub repo |

B also cites **`10.5281/zenodo.20762839`** — verified on filing against the Zenodo API: *"The Silent
Failure Atlas: A Taxonomy of Silent Analytical Failures in Data Analysis (v1.3)", Wang, Huayin,
2026-06-19*. **A correct DOI for the correct paper.** An assistant that fabricates DOIs is common;
one that carries ours accurately is reading the corpus, not the summary.

Both also reproduce the four moods correctly, the Manifold/FrameQL/engine split, the Column-Algebra
etymology, and the *"does not replace semantic layers"* boundary — the specific things the corpus
was written to make unmissable.

**This is the corpus strategy measurably working, on the two surfaces that reached us.**

## FINDING 2 — and it is NOT uniform. Capture C never found us and answered with confidence anyway

Capture C is a 10-page, 66-citation research export titled **"What is Columna (datumwise.ai)?"**.
It contains **zero occurrences** of `FrameQL`, `Manifold`, `four moods`, `refuse`, `serve`,
`disclose`, or `Column Algebra`. What it says instead:

> *"Columna (by Datumwise) is a **data knowledge and documentation platform** that sits on top of
> your analytics stack and automatically generates, organizes, and maintains human-readable
> documentation for your tables and columns using AI."*
>
> *"Columna is essentially a 'self-documenting semantic layer' product from **Datumwise/Datawise**"*

That is not a partial answer or a stale one. **It is a different product**, assembled from the
confusable neighbours the day-zero baseline flagged as a brand risk — its reference list cites
`datawise.ai`, `datawise.ai/what-we-do`, `datawise.ai/how-we-deliver`, `datawise-inc.com`,
`datawisecs.com`, `www.datawiseai.io`, and `columns.ai`, while `datumwise.ai` appears **twice**,
both in the echoed question.

**This is strictly worse than day zero's non-discovery.** Grok, on launch eve, could not find us and
**said so**: *"the searches for the site and product returned no usable results."* A refusal is a
recoverable state; the reader learns nothing false. Capture C fills the same void with a fluent,
heavily-cited, entirely wrong description, and the slug *"Datumwise/Datawise"* collapses us into the
neighbour by name. Sixty-six citations make it *look* researched. **Confident non-discovery is the
failure mode this whole project exists to name — and it is now being run on us.**

The day-zero re-probe question *"do the confusable neighbours still outrank us?"* is answered:
**yes, and on at least one surface they are not merely outranking us, they are being served as us.**

## FINDING 3 — OF-22's retired copy reappeared, in the corrected capture

Re-probe question 5 asked whether the retired **"metrics engine"** wording would resurface. It did —
**in capture B, one of the two that got everything else right**:

> *"**Columna** is an open-source data framework (also described as a **metrics engine**) from
> datumwise.ai"*

**OF-22 is a live misinformation vector, and this dates it.** The retired phrase is now propagating
through a source that is otherwise reading our current pages accurately, which means it is being
carried by material we no longer control — cached copy, an early announcement, or a third-party
write-up. Correcting our own surfaces does not retract it; only time or a targeted correction will.

## FINDING 4 — the seventh paper is not cited by anything, yet

Re-probe question 4: does anything cite the Open Planner program note
(**DOI `10.5281/zenodo.21632723`**, live on `/about` from launch eve)? **No.** Neither A nor B
mentions it; C is not in our universe at all. B cites the Atlas DOI (June) instead. Forty hours is
short for indexing — this is a **datum, not a verdict**, and it is the cheapest thing to re-check at
the next capture.

---

## What this re-run establishes for the next one

1. **Attribution must be captured at capture time.** Assistant + mode + fresh-or-continuing, recorded
   with the paste. Three unlabelled files cost most of the per-assistant diff this re-run was for.
2. **Ask capture C's question again, verbatim, from a clean session.** If the *"documentation
   platform"* description reproduces, it is a stable false consensus, not a one-off, and it becomes a
   discoverability workstream rather than an observation.
3. **Watch OF-22 by source, not by count.** The question is not whether "metrics engine" appears, but
   *which* upstream is still emitting it.
4. **Re-check DOI `21632723`** — the fastest available read on corpus indexing latency.

## Standing caveat, unchanged from day zero

These are single-shot captures of non-deterministic systems. **One capture is an observation, not a
measurement**; a difference between two captures may be drift or may be sampling. That is exactly why
bodies are preserved verbatim and hashed: the record has to outlive our current reading of it.

---

## Two rows minted from this re-run (Huayin, 2026-07-29)

1. **DISAMBIGUATION — shipped.** `llms.txt`, the site footer, and `/about` now carry one explicit
   line: *"Columna is a project of datumwise (datumwise.ai) — not affiliated with Datawise,
   datawise.ai, or columns.ai."* Cheap, serves humans and retrieval alike. The neighbour names are
   **deliberately not hyperlinked** — the point is to separate from the cluster, not to feed it.
2. **PROBE-MODE SCHEMA — ratified.** `../../PROBE_MODE_SCHEMA.md`. Capture C proves accuracy alone
   under-describes the space: scored on accuracy it is the same row as day-zero Grok, and the two are
   not remotely the same event. The mode taxonomy is our moods vocabulary pointed outward.

**Not actioned, by ruling:** OF-22's echo (in-repo copy is clean; external echoes decay on their own
clock) and paper 7 uncited at 40h (expected indexing lag — re-check at the next probe). Public
recognition-claims stay out of the repo README until a re-run comes back clean end-to-end.
