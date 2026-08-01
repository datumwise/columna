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
| `certificate_cargo_schema_v0_1.md` / `_v0_2.md` | D2 — the certificate cargo schema (desk; v0.2 adjudicated: §4b rule cert, S6 list, channel correction) | — | v0.2 in force |
| `D2_reconciliation_notes_v0_1.md` | D2 reconciliation — full field-by-field (V1 ✔, V3 ✔; S/M/V map + §6 answers, all adopted) | — | adjudicated |
| `cert_v0_2.py` | the v0.2 certificate library — digests, plan-cert + rule-cert builders, S9 plan walker | (imported) | — |
| `emit_c1_v0_2.py` | steps 1–2 — mint C1 rule cert + re-emit C1 plan cert v0.2-conformant + channel test | `python emit_c1_v0_2.py .` | green |
| `pilot_c2.py` | step 3 — C2 pilot (full spine + WHERE-CARVE + mean-via-(sum,count)); emits v0.2 NATIVELY | `python pilot_c2.py .` | **ACCEPTED** (schema acceptance test passed) |
| `adjudication_record/rule_*.json` | the rule certificates (C1 TRANSPORT-shaped-sum; C2 REDUCE-mean) — M1 points here | — | 2 minted |
| `fixtures/c1_*_v0_2.json`, `c2_*_v0_2.json` | v0.2 plan certs + semantic channels (V3 byte-stable) | — | conformant |
| `C2_and_v0_2_conformance_v0_1.md` | steps 1–3 report — rule certs, C1 re-emit, C2 pilot, amortization | — | complete |

**Sequence (charter):** D1 skeleton + D3 harness → pre-D4 report → **ruling** → D4 pilot. All done.
Ruling (2026-07-31): **Acero (`pyarrow.substrait`) is C1's first consumer** (DuckDB is the second
consumer — the cross-consumer inheritance test, **un-gated**; the earlier "HTTP 403 / egress" was
corrected 2026-08-01: the substrait extension is merely unpublished for DuckDB 1.5.5, resolved by a
consumer pin `duckdb==1.1.3`, no environment change — see BLOCK-1). CARVE's WHERE gap was closed by
amendment; D1's left column is 100%-attested-no-asterisks.

Toolchain (study, pinned): Substrait **0.46.0** · columna-core **0.14.0** · Polars **1.43.1** ·
producer `ibis-substrait` 4.0.1 / `substrait` proto 0.16.0 · consumer `pyarrow.substrait` (Acero) 25.0.0.
