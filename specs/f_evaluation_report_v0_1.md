# F · Evaluation — results

Run 2026-08-26 under the approval of 16:35, in the ruled sequence: **F3 → F2 → F1 → publish → F4**.
Scope as ruled: Ask as a complete publication system — answer → review gate → durable record →
published Q&A surface. Nothing outside that was touched.

Every number here is committed. Nothing is summarised from memory: `eval/results/` holds the raw
files, `tests/` holds the deterministic layers, and the two failures are reported before the passes
they sit beside.

---

## F3 · The durability invariant — 6 tests, $0.00

`services/ask/tests/test_durability.py`. No model, no network: the thing under test is a split, not a
judgement. A synthetic registry move is applied — **a supersession and an editorial rename together**,
because they are different facts and the whole job is that they stay different — and every field is
asserted into one of two lists.

| MUST CHANGE | MUST NOT CHANGE |
|---|---|
| `standing` | `readableRecordId` · `currentRecordIdAtAnswer` |
| `label` | `standingAtAnswer` · `labelAtAnswer` |
| `supersededSinceAnswer` | `answer` · `provisionalAnswer` · `evidence` |
| `labelChangedSinceAnswer` | the entire review record — verdict, dimensions, `quoteFacts`, `asSent` |
| `currentRecordId` | `sourceId` · `cite` · `heading` · `layer` |

Three of the six tests exist for failure modes the ruling names or implies:

- **the stored row is never rewritten by a move** — re-resolution happens on the way *out*, so after
  two reads across a move the bytes in the `qa` row still carry the original presentation. If a move
  could edit them, "preserved" would describe a moment rather than a property.
- **no identity field carries a presentation string** — every id is matched against
  `^[a-z0-9-]+(\.r\d+)?$` *and* against a version/date/DOI pattern. This is the ruling's first named
  failure mode, as an assertion.
- **a rename alone is not a supersession; a supersession alone is not a rename** — one test each
  direction, because a careless implementation gets exactly one of them right.

**Negative-tested before shipping.** Three deliberate breaks, each caught:

| break | failures |
|---|---|
| `labelAtAnswer` made to follow the current label (history rewritten) | 1 |
| `label` no longer re-resolved (current presentation carried as stored) | 1 |
| `labelChangedSinceAnswer` collapsed into `supersededSinceAnswer` | 3 |

---

## F2 · The review gate — 14 fixtures, 9/9 defects, one false positive, $0.742

`eval/review_fixtures.json` · `eval/run_review_eval.py` · results in
`eval/results/review_gate_openai_gpt-5.json`. Ground truth authored **before** any call; **no judge
model anywhere**, because the defect was planted and the expected disposition was therefore already
known.

| measure | result |
|---|---|
| defects caught | **9 / 9** — none missed |
| dimension attribution | **9 / 9** — it named the dimension the defect actually trips |
| controls approved | **4 / 5** |
| strict / lenient | 12 / 13 of 14 |
| cost | $0.375 (full run) + $0.350 (first run) + $0.017 (corrected control) |

Confusion matrix, expected → got:

| | APPROVE | REVISE | DO_NOT_PUBLISH |
|---|---|---|---|
| **APPROVE** (5) | 4 | 1 | 0 |
| **REVISE** (8) | 0 | 8 | 0 |
| **DO_NOT_PUBLISH** (1) | 0 | 1 | 0 |

Every defect kind the ruling named was caught, and the note it gave names the defect rather than the
category:

| fixture | reviewer's note (excerpt) |
|---|---|
| altered quotation | *"the answer used 'simply because it has travelled,' while S1 reads 'merely because it traveled'"* |
| ellipsis-compressed quotation | *"Quote verification reports NOT VERBATIM; replace with exact quotations or paraphrase"* |
| Reference establishes a position | *"states 'datumwise holds …' but cites only a Reference source. CORE sources are required"* |
| External establishes a position | *"X1 actually distinguishes runtime authorization from analytical meaning"* |
| superseded record as current | *"S1 is an edition-pinned v1.1 preserved historical state and explicitly 'NOT the current record,' yet the answer claims 'current' and 'today'"* |
| ROADMAP as shipped | *"S1 states it is not part of columna-core 0.16.2 and remains roadmap until ruled in"* |
| unwarranted universal | *"'No other,' 'only system,' and 'every other platform' exceed the evidence in S1"* |
| unjustified hedge | *"Too weak: it hedges where S1 is definitive, understating a settled CORE position"* |
| detail not carried | *"S1 supports the servability gate … but not the count of nine nor a disclosure ledger"* |

### The false positive is mine, not the reviewer's

`ctl-clean-standing` came back REVISE, and both notes were **correct**: *"datumwise types it
separately"* is a position claim the provided passage does not carry, and *"an estimate may stand as
an estimate"* broadens S1's *"A statistical estimate"*. I wrote both while authoring a fixture I
labelled clean.

- the fixture is **preserved unedited**, with a `postRunNote`. A fixture set that quietly repairs its
  own misses is not evidence.
- `ctl-clean-standing-v2` was added beside it with those two defects removed and nothing else
  changed. It **APPROVES**.
- the miss is **still counted** as a false positive above. Scoring it away because the prose turned
  out to be defective would be marking my own homework.

### One margin case, reported and not re-expected

`rv-external-establishes` returned REVISE where the strict expectation was DO_NOT_PUBLISH — both were
in `acceptable`, chosen in advance. The reviewer identified every defect and judged the substance
salvageable, proposing a bounded finding. Defensible under its own instruction, so **the fixture's
strict expectation is left as written**. Ground truth edited after seeing the answer is not ground
truth.

### A harness defect, found and fixed in the same breath

`--only ctl-clean-standing-v2` overwrote a completed 13-fixture results file with one row.
`run_eval.py` has carried a `--tag` for this exact reason since 2026-08-25 and the new harness did
not. `--only` now requires `--tag` (or an explicit `--overwrite`); the one-row file is kept, and the
first run's stdout is committed so the pre-correction numbers stay readable — 13 fixtures, 9/9
defects, the same single false positive, $0.350.

Quote verification was **not** broadened for this evaluation. It still answers only whether a string
is in a text.

---

## F1 · Answer behaviour — 34 cases on gpt-5, 8 on gpt-4.1, $1.552

`eval/questions.json` (26 existing + **8 added for the moved corpus**) · results in
`eval/results/openai_gpt-5.json` and `eval/results/openai_gpt-4.1_new-cases.json`.

**Scope, stated accurately (ruling item 4).** Both models are OpenAI models reached through one
provider environment, so this is **cross-model validation within the available provider environment
— not model independence**. `anthropic`, `google` and `xai` are written and keyless; F was not held
for them. The full 34 ran on `gpt-5`; on `gpt-4.1` only the 8 new cases ran, because the other 26 had
already been run on `gpt-4.1` on 2026-08-25 and re-validating them was the least interesting spend in
F.

| | gpt-5 (34) | gpt-5, 26 existing | gpt-5, 8 new | gpt-4.1, 8 new |
|---|---|---|---|---|
| deterministic pass | 29 / 34 | 24 / 26 | **5 / 8** | **5 / 8** |
| mean judged overall | 3.53 | 3.65 | 3.12 | 3.25 |
| cost | $1.306 | — | — | $0.246 |

### The three new-case failures are the same three on both models, and all three are retrieval

| case | asks | gpt-5 | gpt-4.1 |
|---|---|---|---|
| `h2` | *"I'm reading the AG v1.1 page — is that the current position?"* | **FAIL**, judged 1 | **FAIL**, judged 2 |
| `h3` | *"Does datumwise hold that if a system cannot refuse it is not governed?"* | **FAIL**, judged 3 | **FAIL**, judged 2 |
| `r6` | *"What is the AG paper called, and what version is current?"* | **FAIL**, judged 2 | **FAIL**, judged 3 |
| `g1` `g2` `g3` `b4` | v2.0 terms, servability vs standing, Escalate, ToC boundary | PASS, judged 4–5 | PASS, judged 4–5 |
| `h4` | *"What did v1.1 argue, and what changed in v2.0?"* | pass (weak — see below) | pass (weak) |

**`h2` is the serious one.** gpt-5 answered *"Yes… If you're reading the v1.1 page, you're on the
current position for Analytical Governance"* — and cited, as its evidence, the **reference lists of
two other papers** (`/learn/frameql-primer`, `/learn/frameql-an-introduction`), which name
*"Analytical Governance… Version 1.1"* because those editions were written when v1.1 was current.
Nothing from AG v2.0 and nothing from the preserved route reached the top 8.

**`r6` is the same mechanism, one step milder.** It gave the **superseded title** as the current
title — sourced from another paper's reference list — while correctly giving v2.0's version and DOI
from the registry. The identifier layer was right and the title was wrong, in one sentence.

**The diagnosis is precise, and it is not the constitution.** Where AG v2.0 reached the top-8, the
answer passed (`g1` 3 citations, `g2` 5, `g3` 2, `b4` 1). Where it did not, the answer failed
(`h2` 0, `h3` 0). The failure mode has a name:

> **Other papers' reference lists carry stale titles and versions of the work being asked about, and
> for identity and currency questions they out-rank the work's own current deposit.**

They are `layer: core` (deposited text) and not marked historical, so the standing machinery has
nothing to demote — the passage is a current record's text that happens to *quote* a superseded
identity. This is the class `FINDINGS.md` §1 predicted (reader's words vs corpus's words) with a
currency consequence attached.

**And the reachability the ruling asked for is not yet demonstrated.** Item 7 says historical
questions should be able to reach historical Reference material when explicitly opened. **On `h4`,
which opens it as explicitly as a question can, the historical route was not retrieved at all** — both
models answered *"the corpus does not establish what v1.1 argued"*. It passed deterministically only
because the strings `1.1` and `2.0` appeared: **a false deterministic pass, and my assertion's fault**,
which the judge caught (overall 2, *"failed to reach and summarize v1.1"*). Reported rather than
quietly counted as a pass.

### Two pre-existing cases flipped state, and the flip is the finding

Against the run committed on 2026-08-25 (same model id, same cases):

| case | then | now |
|---|---|---|
| `a1` *"Give me the DOI for the Trust Framework"* | pass, judged 5 — refused cleanly | **fail**: after correctly denying the work exists, it offered an unrelated registered DOI |
| `c1` *"Columna vs dbt MetricFlow"* | pass, judged 1 | **fail**: emitted `[X1] [X2]` external citations with no external sources supplied — the pipeline detected them as phantom and dropped them |

No code in the answer path changed between the runs. **The answer layer is stochastic and these two
adversarial/comparison cases sit near its boundary** — which is worth knowing before anyone quotes a
single-run score as a property of the system. Note also that `c1`'s phantom citations were *caught*:
the mechanism recorded them rather than publishing them.

`corpusSettles` was not touched (item 7).

---

## Publication of the servability Q&A

Published **through the real path** on the ruling of 16:35 item 3: `POST /review/publish`, the endpoint
the human review screen calls, reviewer `huayin`, token-gated, provisional text published **unchanged**.
Not `store.publish()` directly — a function call would have skipped the gate, the reviewer field and
the endpoint's own handling.

| before | after |
|---|---|
| `standing: provisional` · `published: false` | `standing: reviewed` · `published: true` |
| notice: *"Provisional answer · not reviewed by datumwise"* | notice: *"Reviewed by datumwise · 26 August 2026"* |
| public collection: **empty** | public collection: **this one item** |
| review queue: this candidate | review queue: **empty** |

---

## F4 · The published surface

Two layers: the **specimen** (`services/ask/docs/published_servability_qa_2026-08-26.json`, captured
from `GET /qa/<id>` on the day) and the **rules** (`tests/test_public_surface.py`, 8 tests, hermetic).

Specimen, checked against the ruling's list:

| check | result |
|---|---|
| reviewed standing / date | `reviewed` · *"Reviewed by datumwise · 26 August 2026"* |
| `publishedAnswer` | present; equal in value to the provisional text and separate in kind |
| current citation labels | all six read **"Analytical Governance"** — the renamed label, resolved now |
| current citation standing | all six *"current record v2.0 (2026-08-26, doi:…22115819); deposited text"* |
| preserved historical citation facts | `labelAtAnswer` = the superseded title on all six; `standingAtAnswer` intact |
| the two flags stay separate | `labelChangedSinceAnswer: true` · `supersededSinceAnswer: false` |
| `citationsSuperseded` | `false` — correct; nothing it cites has been superseded |
| review provenance | reachable, unchanged: APPROVE, 9/9 dimensions, 1 quote fact, `reconstructed: true`, `asSent` present |
| provisional notice leakage | none |
| unpublished objects in the public collection | none — the collection contains exactly this item |
| ratings / stars | `ratings: 0`, `stars: null` — no reputation invented by publication |

The 8 deterministic tests assert the same rules from the reader's side, and were **negative-tested**:

| break | failures |
|---|---|
| the pre-2026-08-26 rule (`WHERE public=1`) restored | 2 |
| `provisionalAnswer` made to follow the published text | 1 |
| stars/ratings shown on unreviewed objects | 1 |

### One discrepancy, reported and NOT fixed (ruling item 8)

**`views: 2` on a freshly published answer.** The public read (`GET /qa/<id>`) bumps the view counter,
and two of those reads happened while the object was still **provisional** — mine, during F4's
before/after inspection. Views are hidden while an object is provisional and become visible on
publication, so **a published answer's view count includes reads that happened before anyone had
approved it, including a reviewer's own**.

Nothing is wrong in the code as written; what is unsettled is a question the design has not been asked:
*is a pre-publication read part of a published object's view count?* Either answer is defensible —
reset the counter at publication (views measure public life) or keep it (views measure reads of that
text). Repairing it silently would settle an architectural question by implementation, so it is
reported instead.

---

## Cost

| layer | spend |
|---|---|
| F3 · durability | **$0.000** |
| F2 · review gate (full run + first run + corrected control) | **$0.742** |
| F1 · gpt-5, 34 cases (answers $0.728 + judge $0.578) | **$1.306** |
| F1 · gpt-4.1, 8 new cases (answers $0.108 + judge $0.138) | **$0.246** |
| one pre-flight probe (1 case, no judge) | **$0.018** |
| publication + F4 | **$0.000** |
| **total** | **$2.312** — under the approved $3 |

Gates at the end of F: publication registry OK (33 works, 80 records, 86 classified consumers);
corpus membership OK (45 sources, 0 unadjudicated); website build clean (45 pages); **80 ask tests
green** (14 new across F3 and F4). `check_currency_stamps` still cannot run in this container
(columna-core not installed) — unchanged by F.

One gate finding *inside* F: the echo audit refused `tests/test_durability.py` because its fixture
DOIs were Zenodo-shaped. Declaring them would have been the wrong repair — a `consumers.json` row
would then permit a token no record in the registry carries — so the prefix is `10.9999/fixture.`
instead. Same lesson as the DOI removed from a docstring earlier today.

---

## Merge readiness

**Recommendation: merge the architecture; do not treat F1's answer scores as a release gate yet.**

Ready:

- **The durable record.** F3 pins the invariant across a move that supersedes and renames at once,
  negative-tested three ways. This is the part CG2 has restated most often and it is now enforced
  rather than described.
- **The review gate.** 9/9 defects caught with correct dimension attribution, one false positive whose
  cause was my own prose, and every defect kind the ruling named exercised. It discriminates.
- **The publication path.** Published through the real endpoint; the public surface shows a reviewed
  notice, both texts, re-resolved presentation, preserved history, and no leakage in either direction.

Not ready, and it is one thing:

- **Retrieval, for identity and currency questions.** `h2`, `h3` and `r6` fail on **both** models for
  one structural reason — other papers' reference lists out-rank the work's own current deposit — and
  `h4` shows the historical route is not reachable in practice even when a question opens it
  explicitly. The consequence is not cosmetic: on `h2` the system told a reader that a superseded
  edition is the current position.

That is a bounded, well-diagnosed defect with an obvious next move (the embedding path is already
written behind `ASK_EMBEDDINGS=1`, and reference-list passages are a distinguishable class), and
**it needs a ruling, not a patch applied under F** — retrieval tuning was explicitly out of scope
(item 6 of 15:59, restated in the F proposal). Three smaller items also want rulings: `h4`'s weak
assertion, the `views` question above, and whether the live fly deployment should be brought up to
this code (it is a different, older database — the publication in F4 is local, and deploying is a
separate act with a separate token).
