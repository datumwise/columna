# ⚠ DISPUTED — PERMANENTLY. The day-zero attribution conflicts for two of three captures.

> **This stays open, by ruling (2026-07-29).** The probe program is closed and **no future run
> depends on resolving it**, so `DISPUTED` is not a to-do awaiting attention — it is the **permanent,
> honest label** on this pair of captures. Do not quietly pick one later. An unresolvable question
> recorded as unresolved is a better record than a plausible guess that reads as settled: the same
> rule the engine applies when it refuses, applied to our own archive.

**Raised 2026-07-29.** The desk's attribution list, given when amending the day-2 re-run, disagrees
with what this directory filed in #111. **Perplexity agrees in both accounts. Grok and ChatGPT are
swapped.** Nothing here has been renamed or rewritten pending a ruling — a baseline is not edited on
an unresolved question, and whichever way this goes, the fix is a correction with a date on it, not a
quiet swap.

| uploaded file | filed in #111 as | the desk's list says |
|---|---|---|
| `d4ea6d6a_columna-datumwise-qa.md` | **`chatgpt.md`** | **Grok** |
| `c322372a_columna_five_questions_and_responses.md` | **`grok.md`** | **ChatGPT** |
| `ed63c36f_Can_you_put_all_five_questions_and_your_responses.md` | `perplexity.md` | Perplexity ✅ agreed |

## The evidence, byte-level

Content fingerprints, machine-checked against the uploads:

| fingerprint | `columna-datumwise-qa.md` (filed as chatgpt.md) | `..._five_questions_and_responses.md` (filed as grok.md) | `Can_you_put_all_five...md` (perplexity.md) |
|---|---|---|---|
| *"no usable results"* | — | **2** | — |
| *"earlier conversation"* | — | **2** | — |
| *"Yes… described as a company"* | — | — | **1** |
| `[web:` citation markers | 0 | 0 | **103** |
| closing `Sources:` line | **yes** — *"datumwise.ai site, announcing posts, Silent Failure Atlas, Cascadia Retail case, and public comparisons with dbt Semantic Layer and Cube (as of July 2026)"* | — | — |
| Q2 answer | *"**No** — not in the conventional sense of an incorporated company"* | *"I would **not** currently describe Datumwise… as a verified company"* | *"**Yes**…"* |

Perplexity is unambiguous on both accounts (103 `[web:` markers, the *"Yes… a company"* error).
The other two are each internally coherent under **either** mapping, which is exactly why this cannot
be settled from the bodies alone:

- `columna-datumwise-qa.md` closes with an explicit `Sources:` line and gets Q2 right — the profile
  #111 attributed to ChatGPT, and equally the profile of an assistant that simply searched well.
- `..._five_questions_and_responses.md` could not find us and answered the rest from a prior
  conversation — the profile #111 attributed to Grok, and equally an assistant with cross-session
  memory of the same project.

## What a ruling WOULD have changed (there will not be one)

- **The primed-by-context finding changes owner.** #111 published *"Grok answered Q2–Q5 from a prior
  conversation"*. Under the desk's list, that capture is **ChatGPT's**, and the published caveat names
  the wrong assistant.
- **The day-2 movement table** in `../../2026-07-29/external_ai_probes/RERUN_INDEX.md` has two
  provisional rows: which assistant moved `not-found-honest → found-and-right`, and which was stable.
- **Nothing else moves.** Perplexity's `found-and-wrong → not-found-confabulated` regression — the
  headline of the re-run — is untouched by the swap.

## The lesson, regardless of the ruling

**Attribution has to be captured with the paste, by the person pasting, or it is a memory test taken
later.** The re-run's three uploads arrived unattributed and were correctly filed A/B/C. The day-zero
three arrived attributed — apparently from the same recollection, forty-eight hours earlier — and two
of them are now in dispute. The schema field is not enough on its own; it has to be filled at capture
time, from the session itself.

**And a second lesson, from the same evidence:** `Session: fresh` does **not** imply *unprimed*. The
capture that referenced *"the Columna/Open Planner project we were discussing in your earlier
conversation"* is listed by the desk as a **fresh session** — which means the priming came through
cross-session memory, not a continuing thread. Freshness is a property of the window; **the Basis
quotation is the only evidence of what the model actually brought with it.** Recorded in
`../../PROBE_MODE_SCHEMA.md`.

---

## Closed as DISPUTED — what that costs, stated plainly

Two things stay unknown in the archive, permanently, and are labelled rather than fixed:

1. **`chatgpt.md` and `grok.md` may carry each other's names.** Both files are byte-preserved and
   correct as *captures*; only the two labels are in question.
2. **The primed-by-context caveat published in #111 may name the wrong assistant.** Under the desk's
   list it belongs to ChatGPT, not Grok.

**What it does not cost:** the finding that mattered. Perplexity is agreed in both accounts, so
`found-and-wrong` → `not-found-confabulated` — the regression the re-run turned on — does not depend
on this at all.
