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
| `PRE_D4_REPORT_and_D5_ledger_v0_1.md` | the pre-D4 report (sequence gate) + D5 ledger rows as found | — | **awaiting desk ruling** |

**Sequence (charter):** D1 skeleton + D3 harness first → **this report** → D4 pilot *only on the ruling*.
The headline flag: the DuckDB substrait extension is unreachable here (HTTP 403); **Acero
(`pyarrow.substrait`) is the proposed offline consumer**, proven end-to-end. See the report §2.

Toolchain (study, pinned): Substrait **0.46.0** · columna-core **0.14.0** · Polars **1.43.1** ·
producer `ibis-substrait` 4.0.1 / `substrait` proto 0.16.0 · consumer `pyarrow.substrait` (Acero) 25.0.0.
