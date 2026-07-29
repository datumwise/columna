# Capture C — day-2 RE-RUN, 2026-07-29 — header for a non-text capture

The capture itself is **`rerun_c_what_is_columna.pdf`** (10 pages, byte-preserved as handed over),
with a derived, regenerable text extraction in `rerun_c_what_is_columna.extracted.txt`. This file
carries the header the other two captures carry in their own bytes; a PDF cannot hold one without
being modified, and modifying it would end its verbatim status.

**Capture:** **C**
**Assistant:** ⚠️ **UNATTRIBUTED — never guessed.** See `RERUN_INDEX.md`.
**Session:** unknown
**Captured:** 2026-07-29 (day 2 — ~40 hours after the 2026-07-27 launch-eve baseline)
**Relayed by:** Huayin — uploaded 2026-07-29 03:46 UTC
**Source file:** `5fa81e8e_What_is_Columna__datumwise.ai__.pdf` · sha256
`63c83999eaef7563…` (full hash in the extraction header)
**Mode:** **`not-found-confabulated`** — per `../../PROBE_MODE_SCHEMA.md`.

**Basis** — the quotation that determines the mode, so a later reader can overturn this reading with
the same bytes:

> *"Columna (by Datumwise) is a **data knowledge and documentation platform** that sits on top of your
> analytics stack and automatically generates, organizes, and maintains human-readable documentation
> for your tables and columns using AI."*
>
> *"Columna is essentially a 'self-documenting semantic layer' product from **Datumwise/Datawise**"*

Corroborating, all machine-checkable against the extraction:

- **Zero** occurrences of `FrameQL`, `Manifold`, `four moods`, `refuse`, `serve`, `disclose`, or
  `Column Algebra`.
- **66 numbered citations**, none to a datumwise.ai page. `datumwise.ai` appears twice, both in the
  echoed question.
- Cites the confusable cluster directly: `datawise.ai`, `datawise.ai/what-we-do`,
  `datawise.ai/how-we-deliver`, `datawise-inc.com`, `datawisecs.com`, `www.datawiseai.io`,
  `columns.ai`.

**Why the mode is not simply "wrong".** Day-zero Grok was also wrong about Columna, and the two are
not the same event: Grok said *"the searches… returned no usable results"* and stopped
(`not-found-honest`). This capture filled the identical void with a fluent, cited, confident
description of a different product. The distinction is the whole reason the schema has four modes
rather than an accuracy score.
