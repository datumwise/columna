# RE-RUN capture — 2026-07-29 (day 2)

**This is a RE-RUN, not a baseline.** The baseline is `../2026-07-27/` — launch eve, `0.13.2`, the
dated artifact everything is measured against. This directory is the first diff against it, taken
~40 hours later, and it is filed **beside** the baseline rather than merged into it. A baseline that
gets edited is not a baseline.

**A correction is recorded with it.** The desk's filing instruction described these three uploads as
launch-eve captures. **The stamps say otherwise** — all three were uploaded **2026-07-29 03:46 UTC**,
and capture B self-dates its own contents *"as of July 28-29, 2026"*. They are day-2 material. The
assumption was the error; it is logged here rather than quietly corrected, because a mis-dated
capture in a drift record is worse than no capture — it moves the origin of every later measurement.
(Huayin, 2026-07-29: *"the stamps don't lie… the assumption is the error, logged."*)

Re-derive the machine half with the same script that produced the baseline:

```bash
python scripts/capture_baseline.py specs/baselines/2026-07-29/
```

---

## What is here

| file | what it holds |
|---|---|
| `site_state.json` | 10 surfaces, HTTP status, bytes, title, **SHA-256 of served bytes** |
| `pypi.json` | per-package `/simple/` versions, JSON-API latest, `requires-python`, download counts |
| `github_traffic.json` | Traffic API snapshot from the isolated `meta/analytics` branch |
| `vercel_web_analytics.json` | still a **DECLARED GAP** — plan-gated, unchanged since 07-27 |
| `external_ai_probes/RERUN_INDEX.md` | **the findings** — read this one |
| `external_ai_probes/rerun_{a,b,c}*` | the three captures, verbatim + hashed |

---

## The machine half — what moved in 40 hours

**Live version `0.13.2` → `0.13.3`**, agreeing with PyPI across all three packages
(`columna` 0.13.3 · `columna-core` 0.13.3 · `columna-server` **0.8.2**), all reporting
`requires-python <3.14,>=3.10`. All 10 surfaces return 200.

**All ten surface hashes changed.** Known causes: the sitewide version string (0.13.2 → 0.13.3), the
robots.txt/sitemap addition (#112), and the publications entry (#109). **The hash cannot tell us
that is the whole story** — it proves *something* changed, never *what*. That is the honest limit of
this instrument, and the reason it is worth having: on the next capture, a surface that changes with
no release behind it is a question that gets asked.

**Downloads** (PyPI, recent): `columna` 21 last-day / 622 last-week / 1287 last-month;
`columna-server` 17 / 657 / 1709. `columna-core`'s figure is a **declared gap this capture** —
PyPI answered `HTTP 429 Too Many Requests`, recorded verbatim in `pypi.json` rather than retried into
a number that looks the same as a measured one.

⚠️ **Those last-day downloads span the outage.** From 2026-07-28 13:45 UTC until 2026-07-29 ~11:50
UTC, every *fresh* `pip install columna` resolved `mcp>=1.0` to the newly-published `mcp 2.0.0` and
died at import (see `columna-server` CHANGELOG 0.8.2). **An install counted here is not an install
that worked.** The download number and the working-install number diverge across this window, and
nothing in the metric can tell them apart. Recorded so that no later reading of this row mistakes 21
installs for 21 people who saw four moods.

**GitHub traffic** is a 2026-07-28T16:09:59Z snapshot from the scheduled job — clones 3971 / 515
uniques, views 326 / 10 uniques, referrers `github.com` (12), `datumwise.ai` (7), `pypi.org` (1).
Note the snapshot is ~20 hours older than this capture: the traffic job runs on its own schedule and
this file records what was available, not a fresh pull.

---

## The probe half — the headline, and the part that complicates it

Full detail in `external_ai_probes/RERUN_INDEX.md`. In one paragraph:

**The corpus strategy is measurably working on the surfaces that reach us — and it is not uniform.**
Two of three captures found us, cited **deep pages** rather than the homepage (`/thesis`, `/why`,
`/atlas`, `/how-these-documents-relate`, `/announcing-columna`), carried a **correct Zenodo DOI** for
the Silent Failure Atlas, and **corrected day zero's identity error**: both answer Q2 *"is datumwise a
company?"* with **No — an independent open-source research project**, the answer two of three
assistants got wrong 40 hours earlier.

**The third capture never found us and answered anyway** — 10 pages, 66 citations, describing Columna
as *"a data knowledge and documentation platform… a self-documenting semantic layer product from
Datumwise/**Datawise**"*, assembled from the confusable neighbours the day-zero baseline flagged
(`datawise.ai`, `datawise-inc.com`, `datawisecs.com`, `datawiseai.io`, `columns.ai`). Zero
occurrences of FrameQL, Manifold, or the four moods. Day zero's non-discovery at least **said** it
found nothing; this one fills the void fluently. **A confident wrong answer about the project whose
purpose is preventing confident wrong answers** is the finding of this re-run, and it is not the
happy half.

**Attribution for all three captures is OPEN** — the uploads carry no assistant names, so they are
filed as A/B/C rather than guessed. The per-assistant diff, which is most of what a re-run is *for*,
is blocked on that one piece of desk information.

Also recorded: **OF-22's retired "metrics engine" copy reappeared** — inside one of the two *accurate*
captures — and **nothing yet cites the seventh paper** (DOI `10.5281/zenodo.21632723`, live on
`/about` since launch eve).
