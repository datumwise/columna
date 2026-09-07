# Predecessor source provenance — durable evidence record

**Verification performed:** 7 September 2026 · **Repository base:** `bfb3cfe`
**Scope: the deposited Markdown artifact only.** No claim is made about the deposited PDF rendering.

This record exists so the provenance claims in the adopted Introduction and Primer, and in the
adoption-facing authority index, rest on something durable rather than on prose. It keeps three facts
apart on purpose, because conflating them would misrepresent the historical record.

## 1. What was available during the ORIGINAL editorial pass

The editorial pass read the predecessors as **public repository text** and recorded them in the
editorial archive as normalized transcriptions. Direct deposit download was not available to that
pass. Its own notes say so, and they are preserved unedited:

> "Full source body transcribed from the raw public repository text on 7 September 2026. Blank-line
> and paragraph whitespace normalized. Front matter restored against the complete web view. **Not an
> original-byte or Zenodo checksum verification.**"
> — `../editorial_archive/audit/frameql_an_introduction_v2_3_transcribed.md.note.txt` (and the Primer's
> identical note)

**The checksums that pass recorded therefore identify its transcriptions, not the deposited
originals.** Nothing in this follow-up rewrites that; the archived notes, manifests and register keep
their original wording.

## 2. What was verified SUBSEQUENTLY, and how

A later, separate act on 7 September 2026: both Zenodo records were fetched over the public REST API
and their Markdown artifacts downloaded and compared byte-for-byte against the repository sources.

| | *Frame-QL: An Introduction* v2.3 | *A Primer on Frame-QL* v2.2 |
|---|---|---|
| registry record | `w-frameql-introduction.r07` | `w-frameql-primer.r05` |
| Zenodo record id | `22071910` | `22071833` |
| DOI | `10.5281/zenodo.22071910` | `10.5281/zenodo.22071833` |
| deposit artifact | `frameql_an_introduction_v2_3_publication.md` | `a_primer_on_frameql_v2_2_publication.md` |
| pinned repository path | `apps/website/src/content/corpus/frameql_an_introduction_v2_3.md` | `apps/website/src/content/corpus/a_primer_on_frameql_v2_2.md` |
| md5 (publisher-declared, and observed) | `8aa327a4ad6ea7b948d20274db45f1df` | `6c1292a26514c4d8c715a104408f43bc` |
| sha256 | `ea52d43a31da989c651b32f328d74e667bc001833b5a689ba3eaaf71c66d6327` | `5555940bd9c571602d4d43c37955930c5dc09aa4079f2a686f368cb3f9ab8fa4` |
| size / lines | 28,310 bytes · 607 lines | 9,295 bytes · 250 lines |
| verdict | **byte-identical** (`cmp` clean, 0 diff lines) | **byte-identical** (`cmp` clean, 0 diff lines) |

Both deposits publish Markdown **alongside** the PDF, so this is a genuine byte comparison and not a
PDF-derived paraphrase. The observed md5 of each repository file equals the checksum Zenodo publishes
for the corresponding deposit artifact.

**Limits of this verification, stated rather than implied.** It covers the Markdown artifact only. It
is a point-in-time fetch pinned to **record ids** `22071910` / `22071833`, not to concept DOIs, so it
says nothing about future versions. And neither work is registered in
`services/ask/deposits/manifest.json`, the repository's durable checksummed deposit record — that
manifest is machine-generated and marked do-not-hand-edit, and **the ingest pipeline was not run and
that file was not edited**, by instruction.

## 3. The exact transcription differences, and the successor edits

### 3.1 Primer v2.2 — no difference

The editorial transcription is **byte-identical** to the deposit-verified repository source
(sha256 `5555940b…`, 9,295 bytes, 250 lines on both sides). The declared normalization was a **no-op**
for this document.

### 3.2 Introduction v2.3 — three paragraph splits, no word changed

Content is identical: **3,988 whitespace-separated tokens on both sides with not one token
different**, and all **16** fenced blocks byte-identical. The only divergence is structural — three
long paragraphs each split in two, giving **+3 paragraph blocks, +6 lines, +3 bytes** (28,310 →
28,313).

| # | paragraph split after… | inherited by the v2.4 successor? |
|---|---|---|
| A | *"…it pins the anchor at which a subexpression must be available when it is consumed by an enclosing operation."* | **yes** — retained |
| B | *"…This introduction does not import unshipped Theory of Data features into the language."* | **yes** — retained |
| C | *"…under v6.1's compatibility provision."* | no — that paragraph is revised in v2.4, so the split does not arise |

**Splits A and B are retained and are recorded here as editorial changes.** No rebuild was performed
solely to undo them, by instruction. They change paragraph segmentation only; they move no word and
touch no example.

A fair characterisation of the archive's own phrase: "blank-line and paragraph whitespace normalized"
is exactly accurate for the Primer, and slightly generous for the Introduction, because introducing a
paragraph break is a structural edit rather than a normalisation — even when no word moves.

## 4. Examples: preserved, not newly executed

Every Frame-QL example carried from a predecessor into its successor is **carried across, not
re-executed**. Both successors say so in their own mastheads, and that statement is true.

These corpus documents are **outside** the repository's machine-verified example regime:
`docs/tools/regen_examples.py` globs `docs/**/*.md` and the docs gate invokes it with no path
arguments, so `apps/website/src/content/corpus/` is never covered; and none of these documents carries
a ```` ```frameql-output ```` block, which that regime requires. A preserved example is therefore an
unexecuted prose illustration, and no coverage or conformance claim attaches to it.

## 5. What this record does not do

It does not amend the archived editorial notes, source manifest, reconciliation register, or the
reviewed baselines; all remain unedited at `../editorial_archive/` and `../reviewed_sources/`. It does
not attribute the later verification to the original pass. It does not turn a revised successor into a
republication of a deposit. And it authorizes no publication, deposit production, or ingestion.
