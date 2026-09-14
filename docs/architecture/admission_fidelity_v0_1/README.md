# Raw evidence — admission fidelity study v0.1

Primary records for `../admission_fidelity_study_v0_1.md`. Kept so the study's claims are
reproducible rather than merely reported.

| file | what it is |
|---|---|
| `probe_1_matrix.py` | the probe: 3 crossings × 15 cases |
| `probe_2_followups.py` | 6 follow-up measurements resolving ambiguous rows from run 1 |
| `run_1_matrix.txt` | verbatim stdout of `probe_1_matrix.py` |
| `run_2_followups.txt` | verbatim stdout of `probe_2_followups.py` |
| `probe_3_errata_checks.py` | **added 2026-09-14 with the errata revision** — one re-measurement, separating the fourth-hop decimal collapse's two candidate causes (the `(38,0)` TYPE vs the VALUE's digit count), plus the version stamps runs 1 and 2 never printed |
| `run_3_errata_checks.txt` | verbatim stdout of `probe_3_errata_checks.py` |

**RUNS 1 AND 2 ARE UNTOUCHED BY THE 2026-09-14 ERRATA REVISION.** What that revision corrects is the
*claims the study made about* these runs, recorded in §0 of the study. The raw records are primary
evidence and are not edited after the fact — including where they show a probe defect (all fifteen
`duckdb-native` rows in run 1 are `ERROR`, which is [E1]). Run 3 **adds** a measurement; it replaces
no row in runs 1 or 2.

**`probe_3_errata_checks.py` loads the DuckDB ADBC driver differently, on purpose.** Probes 1 and 2
pass an absolute path to `_duckdb*.so`; probe 3 uses `adbc_driver_duckdb`, which the `duckdb` wheel
vendors and which resolves the same shared object through `importlib.util.find_spec`. Same binary,
same `duckdb_adbc_init` entrypoint — only the way it is located changes, and probe 3's way is
pinnable while `DUCK_LIB` is not.

**Not run in CI, by design.** These require `adbc-driver-manager` and `adbc-driver-sqlite`, which
are not dependencies of any package in this repo and must not become ones for a measurement
exercise. `DUCK_LIB` in both scripts is an absolute path to the duckdb extension module in the
environment where the run happened and will need repointing elsewhere.

To reproduce: create a throwaway venv, `pip install pyarrow duckdb polars adbc-driver-manager
adbc-driver-sqlite`, repoint `DUCK_LIB`, run both scripts. Versions observed are recorded in §2 of
the study; a different set of versions is a different measurement, not a contradiction of this one.
