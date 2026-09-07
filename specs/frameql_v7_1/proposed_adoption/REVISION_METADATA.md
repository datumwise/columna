# Proposed adoption — J1 and J2 application record

**Applied:** 7 September 2026 during docs-only staging · **Applied by:** repository staging, from the
supplied correction records. **Not installed as new current editions. Not published.**

This directory holds exactly the two files the joint review's editorial corrections touch, and only
those. Every other reviewed document is unchanged and is read from `../reviewed_sources/`.

The corrections were **not** reconstructed. They were applied from the supplied exact replacement
strings in `../tod_frameql_joint_review_editorial_corrections_v0_1.json`, and each application was
verified four ways before it was written.

## J1 — `frameql_language_vnext_working_draft_v0_4.md` §6.3

Carries the supported-observation participation premise into the local 97-observation COUNT example.
T §11.5.1 and acceptance case E02 already state the rule; the example did not restate it. The adopted
text makes the 97 follow from the **declared participation rule**, not from the spelling
`count(x @ I)`, and states that neither count may silently shrink another target's intended
population.

| check | result |
|---|---|
| reviewed-source sha256 matches the record | **verified** `7df99739…e1a5820` |
| replaced text occurs exactly once in the source | **verified** (1 occurrence — unique) |
| adopted sha256 matches the record's `proposed_content_sha256` | **verified** `78e84a60…9e5873ab` |
| replayed diff is line-identical to the supplied `J1_editorial_correction.diff` | **verified** (8 content lines) |

Size: 62,812 → 63,218 bytes. Lines: 1,293 → 1,293. The fenced `text` example block is unchanged.

## J2 — `columna_o3_governed_analytical_order_v0_2.md` §17 (supporting §10)

Resolves the otherwise orphaned `[S6]` citation in §10 by identifying the historical architecture
handoff, **without** granting it current operational authority. The added note says so in its own
words: *"Its operational status is historical, not current."*

| check | result |
|---|---|
| reviewed-source sha256 matches the record | **verified** `37307c32…0eb54bc45` |
| replaced text occurs exactly once in the source | **verified** (1 occurrence — unique) |
| adopted sha256 matches the record's `proposed_content_sha256` | **verified** `ae55b0bd…97dcb707` |
| replayed diff is line-identical to the supplied `J2_editorial_correction.diff` | **verified** (2 content lines) |

Size: 32,132 → 32,468 bytes. Lines: 381 → 383 (the note is additive; no existing line was removed).

The `[S6]` referent it names, `START_HERE(2).md` of 14 August 2026, is staged at
`../historical_provenance/START_HERE(2).md` so the citation resolves inside the repository. That file
is **historical evidence and carries no active instruction**; `../historical_provenance/README.md`
says so, and this staging does not change that.

## What was deliberately not done

No revision metadata was written **into** either document body: the reviewed set assigns editorial
revision numbers as an adoption act, and this staging is not an adoption decision. The provenance is
recorded here, beside the files, where it can be read without altering the reviewed text or its
hashes. `../reviewed_sources/` remains byte-identical to the review package, so the baselines stay
traceable and the integrity audit still reproduces.
