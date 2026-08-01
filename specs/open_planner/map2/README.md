# MAP-2 — the outbound mapping study (beat 2)

Certified lowerings of Columna plans onto container plans. Governing artifact: the beat-2 charter,
`../map2_mapping_study_charter_v0_1.md` (desk-drafted, ratified). This directory holds CC's
deliverables. **D2 (certificate cargo schema) is the desk's, drafted in parallel — not here.**

| file | deliverable | run | state |
|---|---|---|---|
| `trace_nodes.py` | D1 left column — the **attested** Polars trace of the eight nodes (observer only; edits nothing) | `python trace_nodes.py fixtures/` | green; 0 ninth-node candidates |
| `fixtures/d1_polars_trace.json` | the frozen trace (evidence for D1's left column) | — | committed on creation |
| `D1_lowering_table_v0_1.md` | D1 — the lowering table (8 nodes + 2 compositions); verdicts **proposed** for desk adjudication | — | complete |
| `oracle_harness.py` | D3 — the oracle protocol; Polars reference oracle; instruments + **mandatory negative control** | `python oracle_harness.py --selftest` | green; negative control valid |
| `PRE_D4_REPORT_and_D5_ledger_v0_1.md` | the pre-D4 report (sequence gate) + D5 ledger rows as found | — | ruled 2026-07-31 (Acero granted; CARVE gap closed) |
| `pilot_c1.py` | D4 — the C1 pilot: lower → Substrait 0.46.0 → Acero → oracle-compare | `python pilot_c1.py fixtures/` | **ACCEPTED** |
| `fixtures/d4_c1_pilot_certificate.json` | the pilot's conservation certificate (evidence) | — | `ACCEPTED: true` |
| `D4_C1_pilot_v0_1.md` | D4 report — acceptance table, Attack B / Class C, perimeter, V1/V3 | — | complete |
| `fixtures/d4_c1_semantic_channel.json` | the certificate's SEMANTIC channel (byte-stable; V3 diffs this) | — | invariant across runs |
| `certificate_cargo_schema_v0_1.md` | D2 — the certificate cargo schema (desk-drafted; S1–S10 / M1–M4 / V1–V6) | — | filed; v0.2-pending |
| `D2_reconciliation_notes_v0_1.md` | D2 reconciliation — full field-by-field (V1 ✔, V3 ✔; S/M/V map + §6 answers) | — | returned for adjudication |

**Sequence (charter):** D1 skeleton + D3 harness → pre-D4 report → **ruling** → D4 pilot. All done.
Ruling (2026-07-31): **Acero (`pyarrow.substrait`) is C1's first consumer** (the DuckDB extension is
unreachable here — HTTP 403; deferred-not-dropped, enters later as the second consumer under the same
harness = the cross-consumer inheritance test). CARVE's WHERE gap was closed by amendment; D1's left
column is 100%-attested-no-asterisks.

Toolchain (study, pinned): Substrait **0.46.0** · columna-core **0.14.0** · Polars **1.43.1** ·
producer `ibis-substrait` 4.0.1 / `substrait` proto 0.16.0 · consumer `pyarrow.substrait` (Acero) 25.0.0.
