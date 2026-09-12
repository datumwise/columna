# Raw evidence — admission fidelity study v0.1

Primary records for `../admission_fidelity_study_v0_1.md`. Kept so the study's claims are
reproducible rather than merely reported.

| file | what it is |
|---|---|
| `probe_1_matrix.py` | the probe: 3 crossings × 15 cases |
| `probe_2_followups.py` | 6 follow-up measurements resolving ambiguous rows from run 1 |
| `run_1_matrix.txt` | verbatim stdout of `probe_1_matrix.py` |
| `run_2_followups.txt` | verbatim stdout of `probe_2_followups.py` |

**Not run in CI, by design.** These require `adbc-driver-manager` and `adbc-driver-sqlite`, which
are not dependencies of any package in this repo and must not become ones for a measurement
exercise. `DUCK_LIB` in both scripts is an absolute path to the duckdb extension module in the
environment where the run happened and will need repointing elsewhere.

To reproduce: create a throwaway venv, `pip install pyarrow duckdb polars adbc-driver-manager
adbc-driver-sqlite`, repoint `DUCK_LIB`, run both scripts. Versions observed are recorded in §2 of
the study; a different set of versions is a different measurement, not a contradiction of this one.
