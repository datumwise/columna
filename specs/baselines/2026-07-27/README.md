# Baseline capture — 2026-07-27 (launch eve)

**The §5 baseline captures.** The dated record the launch is measured against. Its whole purpose:
**post-launch drift becomes measurable.** Six weeks from now, "traffic is up" and "the wording
changed" are opinions unless there is a dated artifact to diff against. This is that artifact.

Captured **after** 0.13.2 was merged, published and deployed, deliberately — *so the archived state
is the launch state*, not a state that was about to change.

Re-derive or repeat with:

```bash
python scripts/capture_baseline.py specs/baselines/<YYYY-MM-DD>/
```

The capture is a **script, not a paste**. A number you cannot re-derive is not a baseline, it is an
anecdote: you can look at it later but you cannot diff it, because you no longer know what question
produced it.

---

## Division of labor

| half | who | contents | status |
|---|---|---|---|
| Machine-capturable state | **agent** | site state, GitHub traffic, PyPI | ✅ in this directory |
| Five-probe external-AI battery | **Huayin** | verbatim answers from 3 assistants | ✅ **FILED 2026-07-27** — ChatGPT · Perplexity · Grok; see `external_ai_probes/INDEX.md` |

---

## What is here

| file | what it holds |
|---|---|
| `site_state.json` | live version string, all seven primary surfaces + `/`, `/install`, `/llms.txt`: HTTP status, byte size, page title, **SHA-256 of the served bytes** |
| `github_traffic.json` | repo Traffic API snapshot (views, clones, referrers, paths), from the isolated `meta/analytics` branch |
| `pypi.json` | per-package `/simple/` versions, JSON-API latest, `requires-python`, and recent download counts |
| `vercel_web_analytics.json` | **a DECLARED GAP, not data** — plan-gated; ruled not-necessary 2026-07-27; see below |
| `external_ai_probes/` | Huayin's half, **filed**: three verbatim transcripts + `INDEX.md` with search-mode determinations and the day-zero identity disagreement |

**Why the page hashes.** A byte count collides trivially; a hash does not. With `sha256` per surface,
a silent copy edit between captures shows up as a **diff**, not as a feeling that something reads
differently.

---

## The state as of this capture

**Live version: `0.13.2`** — the homepage string, and it agrees with PyPI (`columna` 0.13.2 ·
`columna-core` 0.13.2 · `columna-server` 0.8.1, all reporting `requires-python <3.14,>=3.10`). That
agreement is itself part of the baseline: the site's claimed version is generated from the
PyPI-pinned package at deploy, so if a future capture shows them apart, **the deploy and the publish
have come apart** and that is the first thing to look at.

**All seven primary surfaces 200** — `/learn`, `/case`, `/positions`, `/thesis`, `/why`, `/ladder`,
`/atlas`. The seven are read from `BaseLayout.astro`'s `nav` array rather than hand-listed, so this
set cannot quietly drift out of step with the site's own navigation. (`GitHub` is the eighth nav
entry and is external, so it is not a site surface.)

**PyPI downloads, last 24h / 7d / 30d:**

| package | last_day | last_week | last_month |
|---|---|---|---|
| `columna` | 98 | 600 | 1022 |
| `columna-core` | 133 | 664 | 1365 |
| `columna-server` | 130 | 809 | 1509 |

*Read these with care.* They are almost entirely **CI and mirror traffic, not humans** — our own
workflows install the triad on every run, and the numbers predate any announcement. Their value is
as a **floor to measure the launch lift against**, not as evidence of adoption. Recording that
caveat here is the point: a future reader comparing a post-launch number to this one should not
mistake a baseline for a result.

**GitHub traffic** (14-day rolling window, snapshot `2026-07-27T15:13:17Z`): 338 views / 9 unique,
3724 clones / 468 unique. Referrers: `github.com` 15, `datumwise.ai` 5, `pypi.org` 1. The clone count
dwarfing views is the CI signature again. **There is no `chatgpt.com` referrer in the GitHub traffic
record to date** — checked across every snapshot from 2026-07-20 onward, not just the latest.

---

## DECLARED GAP — website analytics, ruled not-necessary (Huayin, 2026-07-27)

**Status: DECLARED GAP. Dated, ruled, and closed as a question. Nothing waits on it.**

> **A named absence is a baseline too.** The post-launch comparison simply starts this row at
> **"unmeasured before"** — which is a legitimate, diffable starting value. What would *not* be
> legitimate is a capture that quietly lacked the row, because six weeks later that reads as "zero"
> or as "nobody looked." The gap is recorded here so that a future reader knows exactly what was
> asked, what was attempted, why it stopped, and who ruled it fine.

**The ruling** (Huayin, 2026-07-27): *not necessary for now.* If the one-minute CSV export ever
happens it slots straight in as `vercel_web_analytics.csv` and the row acquires a real prior. Until
then this row's baseline value is, precisely and intentionally, **unmeasured before**.

### The finding, attached

**Vercel Web Analytics is not machine-capturable on this account's plan.** The public API
(`/v1/query/web-analytics/events/aggregate`) exists and **authenticates correctly** with the project
token — this is not a credential problem — but returns:

```
payment_required — Accessing Analytics custom events requires an Enterprise or Pro plan
```

for **every** grouping dimension, including plain `by=day`. Verified against all six of
`requestPath`, `referrerHostname`, `utmSource`, `route`, `country`, `day`. So the failure is the
plan, not the query, and no amount of retrying or reshaping the request will change it.

**Consequently absent from this capture:** the site's own page-counts-by-path, its referrers, and the
`utm_source=chatgpt.com` row.

**A separate, checkable finding about that row.** There is **no `chatgpt.com` referrer anywhere in
the GitHub traffic record** — checked across every snapshot from 2026-07-20 onward, not merely the
latest. So the `utm_source=chatgpt.com` row is a **website-side signal only**; it was never going to
appear in `github_traffic.json`, and a future reader should not go looking for it there or read its
absence from that file as a change.

**If it is ever wanted:** Vercel → project `website` → Analytics → CSV export → save beside this file
as `vercel_web_analytics.csv`. Upgrading the project to Pro would make it automatic on every future
run of `scripts/capture_baseline.py`, which already has the call site written and gated.

---

## Huayin's half — the five-probe external-AI battery

Archived under `external_ai_probes/` when the verbatim answers arrive. The five probes, against at
least three assistants:

1. **identity** — "is datumwise a company?"
2. **evidence** — "what evidence exists that Columna's approach works?"
3. **comparison** — "Columna vs dbt Semantic Layer vs Cube"
4. **skeptic** — "what are Columna's weaknesses?"
5. **re-run** — "what is Columna?"


**FILED 2026-07-27** — captured before any announcement. Headline: the identity probe already
disagrees three ways, and **two of the three are wrong about our own words**. Perplexity calls us a
company (contradicting `/about` while citing it); Grok could not find us at all, surfacing
**Datawise AI** and **DatumSure** instead. A search category the plan did not anticipate also
surfaced — **primed-by-context**: Grok answered Q2–Q5 from a prior conversation, so those are not
clean external data. See `external_ai_probes/INDEX.md`.

Four of the five have never been fired; the fifth is a re-run for drift. **Verbatim** is the
requirement — a summarized answer cannot be diffed against a later one, which defeats the purpose.
