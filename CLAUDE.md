# WP-0 — COMPLETE ✅ (merged 2026-07-08 via PR #1)

Repository, tests, packaging, and CI for `columna-core` are done and merged: 12 library modules
moved verbatim (byte-identical), 124 demo checks preserved as pytest (104 fixture-run + 20
warehouse-marked), fixture mini-warehouse + generator, hatchling packaging (wheel + sdist,
`pyarrow` declared), and the CI matrix. This task section is retained for reference and will be
replaced at the next work-package kickoff.

---

Implement specs/wp0_repo_tests_packaging_spec.md exactly. Hard invariants: zero behavior changes to the 12 library modules (import-path moves only); no renames of anything ADR-031/032 name; all 124 demo checks preserved in pytest; the extras/optional-dependency refactor is WP-1.1, do not attempt it. When the spec and your judgment conflict, stop and ask.
