# Baselines — **DORMANT (closed 2026-07-29, ratifier ruling)**

**The probe program is CLOSED. Day 0 and day 2 are archived; no further runs are scheduled.**

This is a closure, not an abandonment. The battery was built to answer one question — *does the
public record recognise us, and does it drift?* — and two captures forty hours apart answered it
sharply enough that a third on a schedule would have measured mostly sampling noise. What it found is
recorded below and does not expire.

| directory | what it is | status |
|---|---|---|
| `2026-07-27/` | the launch-eve **baseline** — site state, GitHub traffic, PyPI, and the five-probe battery across three assistants | archived, **never edited** |
| `2026-07-29/` | the day-2 **re-run**, filed beside the baseline | archived |
| `PROBE_MODE_SCHEMA.md` | the four-mode taxonomy for classifying captures | **dormant, preserved** — it is how a revival would file, not a live process |
| `2026-07-27/external_ai_probes/ATTRIBUTION_CONFLICT.md` | day-zero Grok/ChatGPT attribution | **permanently DISPUTED — open by design** |

## What the program established

1. **A search-first engine lost us after launch.** Perplexity went `found-and-wrong` (day 0:
   *"Yes, Datumwise is described as a company"*, citing the page that says otherwise) →
   **`not-found-confabulated`** (day 2: ten pages, sixty-six citations, a *"self-documenting semantic
   layer product from Datumwise/Datawise"*, none of them our pages). The one engine whose answers are
   built from retrieval at query time moved **away** from us while the site was live, indexed, and
   growing.
2. **Nobody corrected Q2.** The identity error belonged to exactly one assistant, and that assistant
   stopped answering about us. The set's improvement came from **Grok** (`not-found-honest` →
   `found-and-right`); **ChatGPT** was stable and deepened. Averaged, these cancel into a sentence
   true of nobody — which is why the movement table exists and the average does not.
3. **The confusable cluster is a live discoverability risk**, not a theoretical one: `datawise.ai`,
   `datawise-inc.com`, `datawisecs.com`, `datawiseai.io`, `columns.ai` were served *as us*.
4. **`fresh` does not mean unprimed** — freshness is a property of the window, not of the model's
   knowledge. Believe the `Basis` quotation, not the session field.
5. **Attribution decays.** The re-run arrived unattributed, was filed A/B/C, and was amended within
   the hour. The day-zero set arrived *attributed from recollection* and two of its three are now
   permanently in dispute. **Captured with the paste, or it is a memory test taken later.**

## What survived the closure, and now lives elsewhere

**The disambiguation + schema.org row** — the prose line in `llms.txt`, the site footer and `/about`,
plus schema.org JSON-LD (`Organization` + `SoftwareSourceCode`, with the non-affiliation carried in
`disambiguatingDescription`) on every indexable page. Minted from finding 3, but **not
probe-dependent**: it is site hygiene, it stands on its own, and it does not need another capture to
justify it.

## If this is ever revived

Re-derive the machine half with the same script that produced both captures — it is a script, not a
paste, so the question that produced each number is still knowable:

```bash
python scripts/capture_baseline.py specs/baselines/<YYYY-MM-DD>/
```

File probe captures per `PROBE_MODE_SCHEMA.md`: assistant, session, **mode**, and the `Basis`
quotation that determines it. Re-test **Perplexity first** — it is the cell that moved, and the one
the disambiguation row is aimed at.
