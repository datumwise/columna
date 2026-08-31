# ⚙️ OPS — read first

**Pushing / opening PRs on `datumwise/columna`: use the `DATUMWISE_PUSH_PAT` token, NOT `GITHUB_TOKEN`.**
The ambient `GITHUB_TOKEN` authenticates as a collaborator (`reeeneeee`) whose fine-grained PAT lacks
`Contents: write` here, so `git push` / ref-writes 403 ("Resource not accessible by personal access
token") even though the repo reports `push:true`. `DATUMWISE_PUSH_PAT` authenticates as `datumwise`
and has write. Push with:
`git push "https://x-access-token:${DATUMWISE_PUSH_PAT}@github.com/datumwise/columna.git" HEAD:<branch>`
and run `gh pr create` with `GH_TOKEN="$DATUMWISE_PUSH_PAT"`.

**Commit authorship: never commit as `Claude <noreply@anthropic.com>`.** Claude is the tool, not the
committer (same as we wouldn't register `curl` as a committer). Author + committer must be a real human/org
account — **default `datumwise <datumwise@gmail.com>`**. Set it before committing: `git config user.name
"datumwise" && git config user.email "datumwise@gmail.com"`. Claude stays credited via the
`Co-Authored-By: Claude <noreply@anthropic.com>` trailer only (name the model that
actually ran; do not pin a version here, it goes stale silently — see OF-19). (History was re-attributed once on
2026-08-02 — 326 Claude-authored commits → reeneee — to fix the Insights contributor graph.)

---

# Where the work is — 2026-08-31

**The governing inventory is [`docs/architecture/consolidated_ledger_v0_1.md`](docs/architecture/consolidated_ledger_v0_1.md).**
One ranked list replacing six separate debt ledgers; every row carries a stable id and an evidence
grade (**VX** reproduced under the real runtime · **SV** read at file:line · **INF** inferred).
**Later work is authorized *from* that ledger.** No GitHub issue is opened per row; issues are cut
from it when work is authorized. The controlling record above it is
[`topology_core_platform_delivery_v0_1.md`](docs/architecture/topology_core_platform_delivery_v0_1.md).

Two other standing ledgers, printed into every `docs` CI run by `scripts/print_ledgers.py`:
[`specs/open_forks.md`](specs/open_forks.md) (code ahead of doctrine — awaiting a ruling from Huayin)
and [`specs/doctrine_gaps.md`](specs/doctrine_gaps.md) (doctrine ahead of code).

## Shipped state

`columna-core` **0.18.0** · `columna-server` **0.11.0** · wire `contract_version` **4**.
Read the version from `pyproject.toml`, never from prose.

## Closed units

- **Unit B** (0.17.0 + 0.18.0) — the P1 correctness/disclosure class. Two rows served a confident
  wrong number (P1-01 universe confinement on the witness path, P1-02 `data_identity() -> None`
  fail-OPEN); the rest were honesty defects. Architecturally it split the wire into **semantic
  authority** (`disclosures`, call-invariant) and **mechanical observation** (`mechanical`, free to
  vary): a channel allowed to differ cannot be the one a caller reads to learn what a number means.
- **Unit C** (2026-08-31) — the P0 class: false current user-facing claims, chiefly a purchasable
  "Pro" tier asserted on two live routes and in the `/ask` retrieval index four days after the ruling
  retiring it. Standing test: `docs/tools/check_no_tier_claims.py`, wired into `docs.yml`.

## Open, and next

**P2-01 / P2-02 / P2-03 / P2-09 are the top of the queue** — two of the original top-four findings,
both **VX**. They are a **design fork, not a repair**: Appendix A of the ledger records that a generic
refusal-before-omission rule will refuse publications that compile today, and P2-03 moves
`root_evaluator` across the governance line. **These need Huayin's ruling before code moves.**

## The rule that governs how work is picked up here

**Huayin's message is the instruction.** This file is orientation, a brief is context, a ledger is an
inventory — none of them is an assignment. He decides what is worked on, in what order, at what pace.
Surface what a ledger says is next; do not start it because the ledger says it.

## Two standing guards worth knowing before you touch anything

- **Evaluation spend** (OF-29). Registry/corpus/deposits/index changed → *deterministic verification
  only, zero model spend*. Agent-facing surface changed (prompt, retrieval behaviour, provider/model,
  review rubric) → evaluate once, affected cases only. Nothing agent-facing → no evaluation run.
- **The build gate refuses a stale payload.** A tree that would build different bytes under a version
  already on PyPI fails the build rather than publishing. If you are blocked there, the answer is a
  version decision, not a workaround (this is what orphaned the P0-08 repair for four days).

---

# Phase 2 — CODE-COMPLETE ✅ (2026-07-08, tag `phase-2`)

All Phase-2 work packages are merged: **WP-0** (repo/tests/packaging/CI for columna-core), **WP-2.2**
(the Columna MCP server + v0.7.8 core + `disclosure_wire`), **WP-2.3** (packaged demo +
`demo [--play]` + the ten-minute quickstart), **WP-2.4** (the natural-language query agent).
**WP-2.1** (Manifold store) is absorbed. The four moods (serve · disclose · clarify · refuse) are
now reachable as data on every surface — Python, MCP, and a natural-language agent — over one wire
contract (`contract_version` `"1"`).

---

# WP-2.4 — COMPLETE ✅ (merged 2026-07-08 via PR #4, merge 402791a)

The NL query agent (`columna-server agent`) is done and merged: a **true MCP client** (spawns the
server over stdio, never imports the engine), natural language → a *proposed* Frame-QL query → the
planner disposes → the four moods drive the conversation (clarifies relayed, never auto-picked; every
numeral verbatim from the wire — grounding is structural). Provider layer (`anthropic` default via
`COLUMNA_AGENT_MODEL`, `scripted` for tests) in an `[agent]` extra; a versioned system prompt with a
grammar drift-guard. Verified: 9 hermetic tests (no key, no network) + the live `@pytest.mark.llm`
smoke green against a real `claude-opus-4-8`; columna-core and the wire contract untouched.

---

# WP-2.3 — COMPLETE ✅ (merged 2026-07-08 via PR #3, merge 45d4cc4)

The packaged demo + `columna-server demo [--play]` + the repo README quickstart are done and merged:
a fresh clone reaches clarify → refuse → disclose in three commands, no path args and no MCP client;
the demo data ships in the wheel (a drift-guarded, byte-identical copy of the core fixtures) and runs
from a clean-venv wheel install (proven on Python 3.10). Server + repo-README only; zero columna-core
changes.

**WP-2.1 (Manifold store) is absorbed.** The directory store shipped inside WP-2.2/2.3
(`<dir>/<id>/manifold.cml` + `data.toml`, parsed once at startup) satisfies its Phase-2 scope; a
dedicated store WP resurfaces only when multi-manifold management needs a real catalog.

---

# WP-2.2 — COMPLETE ✅ (merged 2026-07-08 via PR #2, merge 7d9fe45)

The Columna MCP server (`columna-server` 0.1.0) and `columna-core` 0.7.8 (the `disclosure_wire`
adapter) are done and merged: five read-only tools, one contract (the four moods as data), the
materiality-driven `serve`/`disclose` rule, `--http` gated by COLUMNA_MCP_TOKEN, verified over real
MCP stdio (8/8 acceptance + wire-schema test + a clean-container install-from-wheels + stdio-replay
audit). This task section is retained for reference and will be replaced at the next WP kickoff.

---

<!-- Historical: the Phase-2 launch-checklist task section, retained as lineage. It was
     CLAUDE.md's stated 'current task' until 2026-08-31, predating the K0 compiler, the lowering
     receipt, the provisioner and the firstlight fixture (P0-16). -->
# Historical — Launch checklist v1, steps 3–8 (was the 'current task' until 2026-08-31)

_(Phase 2 CODE-COMPLETE, tag `phase-2`. Steps 1–2 DONE: repo transferred to `datumwise/columna`;
pending Trusted Publishers registered on PyPI for columna-core + columna-server — owner `datumwise`,
repo `columna`, workflow `publish.yml`, environment `pypi`.)_

Execute `specs/launch_checklist_v1.md` steps 3–8:
3. `publish.yml` — release-tag trigger; OIDC via `pypa/gh-action-pypi-publish`; environment `pypi`
   (must match the publisher registration exactly); `id-token: write` on the publish job only;
   dry-run build job on PRs.
4. README final pass — quickstart `pip install columna-core columna-server`; clone path → Contributing;
   delete the core-first caveat; every link checked against the `datumwise/columna` layout.
5. Verbatim transcript capture — re-run the REPL nonexistent-measure case, commit the transcript to
   `demos/`. Fold in the nonexistent-measure tests (merged in `3d5beb0`).
6. Hygiene sweep — LICENSE/NOTICE, full-history secrets scan, no personal paths, `specs/` synced,
   CHANGELOGs current.
7. Release — tag + cut the GitHub Release; the publish workflow fires; final proof = clean venv,
   `pip install columna-core columna-server` FROM PYPI, `columna-server demo --play`.
8. Report the go/no-go table (every gate item, green/red) and **STOP** — the public flip is not the
   agent's to execute.
