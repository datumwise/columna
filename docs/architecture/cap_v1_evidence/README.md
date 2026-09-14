# Evidence — Carrier Admission Profile v1 candidate

Supporting material for [`../carrier_admission_profile_v1_candidate.md`](../carrier_admission_profile_v1_candidate.md)
and [`../source_adapter_contract_v1_candidate.md`](../source_adapter_contract_v1_candidate.md) §8.

| file | what it is |
|---|---|
| `probe_cap_v1_ingress.py` | the probe: the DuckDB-ADBC driver *package* identity, and CAP v1's three admitted shapes through the complete four-hop path, plus confirmation that every refused shape is actually emitted by this driver |
| `run_cap_v1_ingress.txt` | verbatim stdout |

**SUPPORTING EVIDENCE, NOT NORMATIVE AUTHORITY.** CAP v1 §0 rule 5: no rule in that profile is
justified by *"the probe measured it"*. This run is cited only in blocks marked
`[evidence · non-normative]`, **every one of which could be deleted without weakening any rule.**
It is here so a reader can check that the hazards CAP refuses are real and that the one shape it
admits does cross — not so that the crossing becomes the reason.

**Not run in CI, by design** — same reasoning as the v0.1 study's raw evidence: it needs a driver that
is not a dependency of any package in this repository, and confirming a driver choice must not add one
before the choice is ratified.

To reproduce:

```
pip install duckdb==1.5.5 adbc-driver-manager==1.12.0 pyarrow==25.0.1 polars==1.44.2
python probe_cap_v1_ingress.py
```

No `DUCK_LIB` path to repoint — that is the point of the run's first section.
