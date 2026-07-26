# Doctrine ↔ code gaps — the ledger

Ratified doctrine the shipped code does not yet match. Every open row is a divergence `main` carries
**on the record** until the closing change merges. A gap lands here the moment it is known (a ruled
item leaving scope is a checkpoint event, surfaced before merge — never a silent drop); it is struck
when its fix merges, with the closing commit named.

Sibling ledger: [`open_forks.md`](open_forks.md) — the opposite direction (code *ahead* of doctrine:
a provisional choice awaiting Huayin's ruling), where PR-surfaced forks are durably queued.

| # | opened | doctrine | what `main` does | root cause | status |
|---|---|---|---|---|---|
| ~~DG-1~~ | 2026-07-14 (post WP-B merge `18189db`) | Capture v0.8 (§"Reduction OF a derivation"): unpinned `avg(aov) @ month` ⇒ **engine clarify** enumerating candidate input anchors; pinned `avg(aov@day) @ month` ⇒ **legal, definite quantity** served with a communicative disclosure naming the reading (ruling (A), CP-B1). | Both forms return **`error`/`unknown`**: pinned → "illegal expression construct: MatMult"; unpinned → "'avg' is not a scan operator". Inline reduction is unimplemented, so the ruled clarify and the ruled serve are both absent. | Ruling (A) was ruled at CP-B1 and scoped into B-4 by the B-1 report, then **descoped mid-build without a checkpoint** — surfaced at merge as if an agreed deferral. The descope fails closed (an error, not a wrong number), but the doctrine gap must not linger unrecorded. | ~~**CLOSED** 2026-07-14 by WP-B.1, merge `a074319` (PR #18). Both forms now match doctrine; verified green on merged main.~~ |

| DG-2 | 2026-07-16 (CP-1 §2c, [PR #35](https://github.com/datumwise/columna/pull/35)) | The everything-classifies guarantee: every query resolves to a classified outcome (serve/disclose/clarify/refuse/error), never a raw exception. `level.sum @ cal.month` (a stock whose `sum` is BLOCKED over calendar) collapsed to `cal.month` — collapse a base coordinate (`store`) while transporting another (`day`) across the blocked lineage — SHOULD serve with a critical `blocked_reduction` caveat (as `level.sum @ store*cal.month` does, §2a). | On main it leaked a raw `ColumnNotFoundError` ("unable to find column 'store'") — collapse-while-blocked-transport escapes classification entirely (verified pre-existing, not a §2c regression; found by Huayin's probe). This WP adds an everything-classifies BACKSTOP in `planner.run` (raw exception → classified ERROR/`unsupported`), so it no longer ships unclassified — but it now ERRORS where it should SERVE-with-caveat. | The engine's collapse path drops the collapsed base coordinate's column before the blocked-lineage transport annotates it; the structural fix is engine-side (`engine.py`), out of §2c's planner scope. | **OPEN** — backstop landed (classified, not raw); the structural serve-with-caveat fix is pinned by `test_collapse_with_blocked_transport_classifies` (asserts CLASSIFIED, not raw) and this row. |

## Authorized work — rulings tracked to verified completion

**The rule** (Huayin, 2026-07-25, minted from the fossil audit): *a work-authorizing ruling enters a
ledger at issuance and closes only on verified completion. Rulings that aren't tracked didn't happen.*

This class lives HERE, not in `open_forks.md` (Huayin's consolidation ruling, 2026-07-25: **no third
ledger**). Its remit — *"a ruled item leaving scope is a checkpoint event … never a silent drop"* — is
this class verbatim. `open_forks.md` keeps genuine *undecided* forks only.

It was minted because a ruled micro-PR — migrate the surviving `EDGE … ALONG … VIA` fossils to
`HIERARCHY` — evaporated. Nothing caught it: the only check that would have (`docs.yml`'s regen-check)
fires on a `docs/**` path filter, so `main` sat red 2026-07-19 → 2026-07-25 unseen. The structural fix
for the *non-use* failure is the weekly `docs.yml` run, which now prints every open row of both
ledgers into its job summary — a ledger that **arrives** rather than waiting to be consulted.

| # | ruled | authorized work | owner | status | evidence |
|---|---|---|---|---|---|
| AW-6 | 2026-07-26 | The byte-identical charter guard should fail with a NAMED reason when `specs/` is absent — "charter guard requires a source checkout" — instead of a raw `FileNotFoundError`. | agent | **OPEN** — rowed, not this release | `test_case_resource.py` computes `_SPECS` by walking five directories up from `columna_server.__file__`: the repo root from a source tree, the VENV ROOT from site-packages. Run against an installed wheel it goes red 3/3 with `FileNotFoundError`, which reads exactly like the byte mismatch it is not. Fails closed either way (proverb 5 satisfied — non-zero exit, no sentinel), so this is a legibility fix, not a correctness one. Found 2026-07-26 during the 0.13.0 pre-tag battery. **The corollary is the point:** a red suite is not a red job either — read the REASON, not the colour. Proverb 7 runs in both directions. |
| ~~AW-1~~ | ~2026-07 | Migrate surviving `EDGE … ALONG … VIA` fossils to `HIERARCHY`. | agent | ~~**CLOSED** 2026-07-25~~ | ~~Never landed at issuance — `regen_examples.py` had exactly ONE commit (`93da449`). Closed by [PR #90](https://github.com/datumwise/columna/pull/90) (merge `483fac1`): fixture, core README, `benchmarks.py` GOLD B5, `test_init_loop.py` + its assertion. regen-check green on main for the first time since 07-18.~~ |
| ~~AW-2~~ | 2026-07-25 | Launch checklist v1 step 5 — the verbatim REPL transcript committed to `demos/`. | — | ~~**STRUCK 2026-07-25 — FALSE ALARM, agent error**~~ | ~~The work HAD landed. The agent probed repo-root `demos/`, found nothing, and rowed it open; the real path is **`packages/columna-server/demos/agent_nonexistent_measure_transcript.md`** — present, and **200 on GitHub** (blob and raw). `/story` cites it correctly; the link TEXT renders as `demos/…` while the URL carries the full path, which is what misled the probe. The page's other repo claim ("four takes — plus one honest re-roll — every one preserved") also verifies: `ch3_take1..take4` + `take4a_badroll`. **No claim-integrity item; no citation amendment.** Recorded rather than deleted, per the never-silent rule: a correction is ledger content.~~ |
| ~~AW-3~~ | 2026-07-25 | Swap the site contact string to `contact@datumwise.ai` once the alias exists. | Irena (alias) → agent (swap) | ~~**CLOSED** 2026-07-25~~ | ~~Alias live (Huayin). Swapped in `about.astro`; the swappable-const design held — a repo-wide sweep found the old address authored in exactly ONE place, and the built `dist/` now contains it nowhere. All three contact-bearing surfaces agree (`/about`, `llms-full`, the Two Great Sources position piece). **This also closed a live divergence**: llms-full already served `contact@datumwise.ai` via that ratified paper while `/about` still served the gmail address, so the site had been giving humans and agents different addresses. Screenshot verified. **Delivery NOT verified** — no mailbox or SMTP available to me; a human must send to the alias and confirm receipt.~~ |
| AW-4 | 2026-07-25 | Retire / re-point `GITHUB_TOKEN` so exactly one variable, one identity, one scope does push work. | **Irena** (env sitting) | **OPEN** — variable only; policy closed | **POLICY CLOSED 2026-07-25 (Huayin):** all `datumwise/columna` work runs under the **datumwise** identity. Probe re-run 2026-07-25 confirms the working credential is correct — `DATUMWISE_PUSH_PAT` → `datumwise`, **has** `contents:write`. The stale variable **still lingers**: `GITHUB_TOKEN` → `reeeneeee`, **no** `contents:write`. Row stays open as a one-minute Irena env sitting to delete/re-point that variable; nothing is blocked on it. |
| AW-5 | 2026-07-25 | The core README grammar correction reaches PyPI. | rides next release | **CLOSED** 2026-07-26 | Corrected in-repo by [PR #90](https://github.com/datumwise/columna/pull/90). A README ships to PyPI only with a release, so it rides 0.12.2-whenever. **No release minted for prose** (ruled). · **A5 (2026-07-26) rides this row:** columna-core's PyPI *summary* is also off-voice — "the column-foundation analytic framework (multi-table, transport-based, correctness-governed)" — matching no other surface and reading as jargon to an external reader. External-AI probe finding; fix it alongside the README at the next release, since both only reach PyPI with a release. · **CLOSED by 0.13.0** (2026-07-26, tag `v0.13.0`): "the next release" arrived. The #90 `HIERARCHY` correction is confirmed present in the wheel's tree (the `EDGE` fossil is gone), and the off-voice summary is replaced by the ratified line — "Columna Core — the definition language, adjudication, and engine of Columna, by datumwise." Both verified in the BUILT WHEEL METADATA before publish, not in the source tree: a README reaches PyPI only as packaged bytes. The same pass retired "honest metrics engine" from its last live carriers (root README, `packages/columna/README.md`, and the umbrella's module docstring — a fourth carrier the ruling had not enumerated), all three wheels verified free of the phrase. |


## Log
- **DG-2 opened 2026-07-16** (CP-1 §2c). Huayin's probe found `level.sum @ cal.month` leaking a raw
  `ColumnNotFoundError` on main — a hole in the everything-classifies guarantee (pre-existing, not a
  §2c regression). Per his ruling ("does not ship past the #35 gate unclassified"): the WP adds an
  everything-classifies backstop in `planner.run` so the query is at least CLASSIFIED (error), and this
  row records that it SHOULD serve with a critical `blocked_reduction` caveat — the structural
  engine-side fix deferred, pinned by a test.
- **DG-1 opened 2026-07-14.** Recorded per Huayin's ruling (2026-07-14): "a ruled item leaving scope
  is a checkpoint event, raised before merge, every time"; "the unpinned case is capture-ruled — main
  currently contradicts ratified doctrine — that gap doesn't get to linger unrecorded." WP-B.1 (pinned
  inline reduction per (A), unpinned engine clarify per capture v0.8, the input_anchor-fit finding
  owed to CP-B2, and their tests) closes it.
- **DG-1 CLOSED 2026-07-14** by WP-B.1, merge commit `a074319` (PR #18). Pinned inline reduction serves
  with the immaterial communicative note; unpinned clarifies enumerating candidate input anchors —
  both match capture v0.8. No open gaps remain.
