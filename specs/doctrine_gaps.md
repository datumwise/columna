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

## Machine-surface ledger — deferred by homepage brief v0.2 (2026-08-19)

Ruled deferrals, recorded so nothing open lives only in a PR description. The redesign's homepage
slices deliberately do **not** touch the machine-facing site; a later governed slice makes it
generated rather than hand-maintained. Each row is work the site owes its own Intelligence pillar:
if datumwise argues that machines participate in analytical work, its machine surfaces should be
governed the way its numbers are.

| # | opened | item | current state | note |
|---|---|---|---|---|
| MS-1 | 2026-08-19 | **Canonical links.** `<link rel="canonical">` on every page. | ABSENT site-wide. Implemented during Slice 1 and **removed on ruling** — machine-surface work belongs to the later governed slice, not to a homepage slice. | The implementation is one line in `BaseLayout.astro`, derived from the configured `site` so it cannot drift from the sitemap. |
| MS-2 | 2026-08-19 | **Generated, versioned `llms.txt`.** | HAND-AUTHORED and DRIFTED: `public/llms.txt` claims `contract_version "1"`; the shipped contract is `"3"`. Nothing guards it. | The drift is the argument for the whole ledger: every *generated* surface beside it stayed true while the hand-written one rotted. Do not hand-patch it — regenerate it from an authoritative source. |
| MS-3 | 2026-08-19 | **Page-level structured data.** `Article` / publication / concept nodes with DOI and version. | Only site-wide identity JSON-LD (`Organization` + `SoftwareSourceCode`) exists; no page carries its own. | This is what lets a machine reader recover research↔concept↔product relationships without inferring them from layout. |
| MS-4 | 2026-08-19 | **Social preview metadata.** `og:url`, `og:image`, Twitter card. | `og:title`/`og:description`/`og:type` only — shares render bare. | |
| MS-5 | 2026-08-19 | **RSS/Atom feed.** | Absent (`/rss.xml` 404s). | |
| MS-6 | 2026-08-19 | **A real 404 page.** | `src/pages/404.astro` does not exist. | |
| MS-7 | 2026-08-19 | **Publication / concept relationship metadata.** Supersession, version lineage, concept→implementation links, in explicit structure. | Carried in prose only. | Reads with MS-3; also the prerequisite for a structured Research index (there is no Astro content collection today — `src/content/*` is directly-imported markdown). |
| MS-8 | 2026-08-19 | **Content discovery / news mechanism.** A published work must be discoverable from the site's own inventory, not only from the author's memory. | ABSENT. The corpus is a hand-maintained set of imported markdown files; nothing enumerates the publication record, and there is no feed. | **This gap was demonstrated, not theorised.** The category-defining paper — *Analytical Governance: From User Intent to Governed Analytical Execution*, v1.0, 15 Aug 2026, DOI `10.5281/zenodo.21959749` — existed and was published, but a reviewer inspecting the live corpus and every DOI on the site concluded no defining paper existed, because the site did not expose it. The later Research/news-generation mechanism exists to make that impossible. Reads with MS-3, MS-5 and MS-7. |

### Content in development — recorded, deliberately not mixed into a slice

| # | opened | item | status |
|---|---|---|---|
| CT-1 | 2026-08-19 | ***The Theory of Data in One Afternoon*** — a first-time-reader on-ramp. Intended role: the cold-reader / Start Here entry under The Case. | In development. **Not part of Homepage Slice 1** and not to be linked from it until it lands (Huayin, 2026-08-19). |
| CT-2 | 2026-08-19 | **Analytical Governance v1.1 alignment.** A revision of the category paper is under consideration. | Being considered separately. Slice 1 links **v1.0** accurately (DOI `10.5281/zenodo.21959749`) and does not anticipate the revision. |

### Generator / source-of-record hygiene (same date, not machine-surface)

| # | opened | item | current state |
|---|---|---|---|
| GH-1 | 2026-08-19 | **Committed generated artifacts are stale.** `apps/website/src/data/case.generated.json` and `grammar.generated.json` are committed at 0.14.0 output while the branch package is 0.15.0 (the committed grammar is missing the `SOURCE_MANIFOLD` token). | Inert for CI — both jobs regenerate before building, so the build's regenerated truth is the gate. But the committed copies are not what the branch produces, and the flap detector only checks determinism, not currency. **Deliberately not "cleaned" inside a homepage slice** (Huayin, 2026-08-19). |
| GH-2 | 2026-08-19 | **`package.json` `gen:transcript` points at a file that does not exist** (`scripts/gen_transcript.mjs`; the real generator is the Python one, invoked from CI). | Broken script entry; harmless until someone runs it. |
| GH-3 | 2026-08-19 | **Orphaned assets.** `src/components/PrecisionRecallFigure.astro` has no importer; `public/media/manifold_loop.mp4` (946 KB) + its poster are unreferenced since the video was retired from `/the-argument`. | Dead weight in the tree and the bundle. |
| GH-4 | 2026-08-19 | **`/ladder` is hand-transcribed** from `src/content/corpus/ladder_page_v0_3.md` (its own source of record) and can drift from it silently. | Recorded in the page's own header comment; no guard. |

---

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
| AW-4 | 2026-07-25 | Retire / re-point `GITHUB_TOKEN` so exactly one variable, one identity, one scope does push work. | **Irena** (env sitting) | **CLOSED** 2026-07-26 | **POLICY CLOSED 2026-07-25 (Huayin):** all `datumwise/columna` work runs under the **datumwise** identity. Probe re-run 2026-07-25 confirms the working credential is correct — `DATUMWISE_PUSH_PAT` → `datumwise`, **has** `contents:write`. The stale variable **still lingers**: `GITHUB_TOKEN` → `reeeneeee`, **no** `contents:write`. Row stays open as a one-minute Irena env sitting to delete/re-point that variable; nothing is blocked on it. · **CLOSED 2026-07-26 by execution, and the PERMISSIONS-LAYER line is the record:** the 0.13.0 flip blocked at `git push` — 403, denied to `reeeneeee`, with `GITHUB_TOKEN` authenticating fine and reading everything. The trap is that `gh api repos/datumwise/columna` reported `permissions: {push: true}` **for a token that could not push**: that block describes the ACCOUNT's role on the repo, NOT the TOKEN's grant. Diagnosed by elimination — an explicit-token push ruled out credential-helper confusion, and pushing an EXISTING commit as a new ref (needing only Contents:write, touching no workflow file) still 403'd, ruling out the `workflow` scope. Contents:write was absent outright. Resolved by `DATUMWISE_PUSH_PAT` (identity `datumwise`), now the credential for ALL `datumwise/columna` work; `GITHUB_TOKEN` (`reeeneeee`) is read-only here and must not be reached for. One variable, one identity, one scope — as ruled. |
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
