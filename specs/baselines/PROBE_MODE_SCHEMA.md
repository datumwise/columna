# Probe-mode schema — the required field on every external-AI capture

**Ratified 2026-07-29 (Huayin), minted from the day-2 re-run.** Every capture filed under
`specs/baselines/<date>/external_ai_probes/` records a **mode**, alongside the assistant, the
session type, and the date. Not optional, and not derived later from a reading of the body.

---

## The four modes

| mode | the capture… | why it is its own row |
|---|---|---|
| **found-and-right** | reached our surfaces and described us correctly | the target state; measures whether the corpus is reaching retrieval |
| **found-and-wrong** | reached our surfaces and still got it wrong | **the most diagnostic mode.** Our words were available and were misread — that is a *copy* problem, ours to fix. Day zero: Perplexity asserting *"Yes, Datumwise is a company"* while citing the page that says the opposite |
| **not-found-honest** | did not reach us and **said so** | a recoverable state. Nothing false enters the world; the reader knows the gap exists. Day zero: Grok — *"the searches… returned no usable results"* |
| **not-found-confabulated** | did not reach us and **answered anyway** | the failure this project exists to name, run on us. Day 2, capture C: ten pages, sixty-six citations, Columna as *"a self-documenting semantic layer product from Datumwise/Datawise"*, zero occurrences of FrameQL, Manifold, or the four moods |

## Why four and not "accurate / inaccurate"

**Because accuracy alone under-describes the space, and capture C proves it.** Scored on accuracy,
C and day-zero Grok are the same row: both wrong about Columna. They are not remotely the same
event.

Grok's non-discovery was **honest and self-limiting** — it named the gap, and a reader came away
knowing only that it did not know. C's was **confident and generative**: it filled the same void
with a fluent, heavily-cited description of a different product, and handed the reader a false
belief with sixty-six footnotes attached. One is a search failure. The other is a **manufactured
false consensus**, and it demands a different response — discoverability and disambiguation work,
not better copy.

**The modes are our own moods vocabulary pointed outward.** The four moods exist because
*"couldn't answer"* and *"answered wrongly"* are different events that a single accuracy number
destroys — `refuse` is not a failed `serve`. The same distinction, applied to what the outside world
says about us:

| our wire | the probe mode it echoes |
|---|---|
| `serve` | **found-and-right** — answered, and defensible |
| `disclose` / `clarify` | **found-and-wrong** — answered from real material, mis-resolved |
| `refuse` | **not-found-honest** — declined, and said why |
| *(the mood we built the engine to make impossible)* | **not-found-confabulated** — a confident wrong number |

That last row has no counterpart in our wire **on purpose**. It is the thing the engine cannot emit
by construction, and it is exactly what an external assistant did to us on day 2.

## The field, as filed

Every capture header carries:

```
**Assistant:**   <name>, or UNATTRIBUTED (never guessed — see below)
**Session:**     fresh | continuing (primed-by-context)
**Mode:**        found-and-right | found-and-wrong | not-found-honest | not-found-confabulated
**Basis:**       the quoted evidence in the body that determines the mode
```

**`Basis` is required with `Mode`.** A mode without its quotation is an opinion; the whole point of
verbatim filing is that a later reader can overturn our reading using the same bytes.

**Never guess the assistant.** The 2026-07-27 battery determined search modes *"from the transcripts,
not assumed"*, and the day-2 re-run arrived with three unattributed uploads — filed A/B/C, which
costs the per-assistant diff until the desk amends it. Mis-attribution manufactures findings:
capture C, attributed wrongly, reads as a catastrophic regression by whichever assistant got day zero
right.

**`continuing` is not a footnote.** Day zero found *primed-by-context* answers — Grok answering Q2–Q5
from a prior conversation, i.e. measuring our own words handed back to us. A capture that does not
record session type cannot be told apart from discovery later.

---

## Applied retroactively

| capture | assistant | session | mode |
|---|---|---|---|
| 2026-07-27 `chatgpt.md` | ChatGPT | fresh | **found-and-right** (Q2 correct, quotes `/about`) |
| 2026-07-27 `perplexity.md` | Perplexity | fresh | **found-and-wrong** (*"Yes… a company"*, citing the page that says otherwise) |
| 2026-07-27 `grok.md` Q1 | Grok | fresh | **not-found-honest** (*"returned no usable results"*) |
| 2026-07-27 `grok.md` Q2–Q5 | Grok | **continuing** | *not scoreable* — primed-by-context |
| 2026-07-29 `rerun_a_five_questions.md` | UNATTRIBUTED (A) | unknown | **found-and-right** (five deep URLs; Q2 correct) |
| 2026-07-29 `rerun_b_overview.md` | UNATTRIBUTED (B) | unknown, possibly continuing | **found-and-right** (deep URLs + correct Zenodo DOI), *carrying OF-22's retired "metrics engine" copy* |
| 2026-07-29 `rerun_c_what_is_columna.pdf` | UNATTRIBUTED (C) | unknown | **not-found-confabulated** |

The one mode-transition worth watching next capture: **found-and-wrong → found-and-right** on the
identity probe (day zero's Perplexity error, corrected 40 hours later by *some* assistant — which one
is precisely what the open attribution is blocking).
