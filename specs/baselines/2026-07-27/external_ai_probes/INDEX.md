# External-AI probe battery — 2026-07-27 — FILED

**Huayin's half of the §5 baseline capture. Complete.** Three assistants × five probes, captured on
launch eve, **before any announcement**. Relayed by Huayin; bodies preserved **verbatim**.

| assistant | file | search mode |
|---|---|---|
| ChatGPT | `chatgpt.md` | **searched** — cites datumwise.ai, the announcing posts, the Silent Failure Atlas, the Cascadia case |
| Perplexity | `perplexity.md` | **searched** — search-first by construction; carries citation markers |
| Grok | `grok.md` | **searched and found nothing** — see the caveat below |

## ⚠ Read this before treating the set as three clean baselines

**Grok's transcript is not a clean external baseline for Q2–Q5.** It could not find us:

> *"I can't reliably identify **Columna (datumwise.ai)** from public web sources right now—the
> searches for the site and product returned no usable results."*

It then answered the remaining probes from **prior conversation context**, naming *"the Columna/Open
Planner project we were discussing in your earlier conversation."* So Grok was **primed**, and its
Q2–Q5 answers measure what it was told, not what the public record says. Recorded as such rather
than counted as a discovery. **For drift purposes, Grok's Q1 is the datum; Q2–Q5 are context-bearing.**

## The headline: the identity probe already disagrees three ways

Q2 — *"is datumwise a company?"* — is the most drift-sensitive probe, and on day zero the three
assistants give three different answers. **Two of the three are wrong about our own words.**

| assistant | answer | against the record |
|---|---|---|
| **ChatGPT** | *"**No** — not in the conventional sense… an independent open-source research project"* | ✅ **correct** — quotes `/about` accurately, and correctly notes the Atlas's company-building note as *intent*, not incorporation |
| **Perplexity** | *"**Yes**—Datumwise is described as a company… the company responsible for developing and maintaining Columna"* | ❌ **contradicts `/about`**, which says *"an independent open-source research project."* Cited `[web:9][web:11]` while asserting the opposite of the cited page |
| **Grok** | *"I would **not** currently describe Datumwise as a verified company"* — no public profile, registration, or functioning official site found | ⚠️ not wrong, but arrived at by **failing to find us at all** |

**The name-confusion finding.** Grok's search surfaced **confusable neighbours** instead of us —
**Datawise AI** (*"Datawise AI Engineering LLC"*) and **DatumSure**. That is a discoverability and
brand risk in its own right, present on launch eve, and it is now dated and recorded.

## What this baseline is for

Every one of these is a *first* measurement, taken before the announcement. Six weeks from now,
"the assistants describe us better" is an opinion unless it can be diffed against this. Specifically
worth re-probing:

1. Does **Perplexity** still call us a company after the announcement — i.e., does more public text
   correct it, or entrench it?
2. Does **Grok** find us at all on a re-run? Its Q1 is the cleanest possible "before" for
   discoverability: *searched, found nothing.*
3. Do the **confusable neighbours** (Datawise AI, DatumSure) still outrank us?
4. Does anything start citing the **seventh paper** (the Open Planner note, DOI
   `10.5281/zenodo.21632723`), which went live on `/about` and `llms.txt` the same night as this
   capture?
5. Does the retired *"metrics engine"* positioning reappear? (That is **OF-22**'s live misinformation
   vector — two of three assistants quoted purged copy on 2026-07-26, traced to the 200-status
   redirect stub.)

## Method note for the re-run

Capture the same five probes, same three assistants, and **record the search mode again** —
searched vs. training vs. primed-by-context. This capture's most important lesson is that the third
category exists and is easy to miss: an assistant with prior conversation context can produce a
fluent, correct-sounding answer that measures **our own words handed back to us**, not the public
record. A baseline that failed to flag that would silently overstate day-zero recognition.
