# F · Evaluation — proposal

**A proposal. Nothing is run.** Per the ruling of 2026-08-26 16:29, E is closed and F opens as a
proposal to be ruled on before any evaluation spend. No model call was made to write this document.

The one-line reason F cannot just be "re-run the trap set": **the trap set measures the answer, and
the system's claims are now larger than the answer.**

---

## 0 · What changed under the trap set since it was written

The 26-case set was written for an architecture in which a fresh answer that passed a privacy filter
became a public Q&A. That architecture is gone. Since then, in order:

| change | what it added to the claim | covered by the current set? |
|---|---|---|
| provisional standing (`ff5d0b0`) | nothing publishes itself | no |
| review-to-publish (`b926b70`) | a verdict, a proposed revision, a human who decides | no |
| Core / Reference / External (`06b6ee1`, `fe7587e`) | **entitlement**: only Core may establish a datumwise position | partially, by rubric |
| the answer discipline (`7fa353a`) | claims bounded in BOTH directions | no |
| mechanical quote verification (`11df020`) | a fact, not a judgement | no |
| durable citations (`b8bb213`, `be3fbce`) | identity stored, standing AND label re-resolved | no |
| Core moved (AG v2.0, ToC v1.0, v1.1 demoted) | a superseded edition inside the corpus | shape 7 only, and only for identifiers |
| `/history/analytical-governance-v1-1` (`9682a39`) | a preserved page **in the retrieval index** | no |

Two of those are the interesting ones. **The review gate has been exercised exactly twice** — one
APPROVE on the servability candidate, one REVISE on the parked Anthropic comparison — so the claim
"a second pass catches what the answering model missed" currently rests on n=2 with no controls.
And **durable citation re-resolution has never been tested over an actual registry move**; it was
built after one, and verified by reading its output once.

---

## 1 · Four evaluations, because there are four different units of measurement

Fusing them into one number is the thing to avoid: an answer, a verdict, a re-resolution and a
published page fail differently and are graded differently.

### F1 · The answer — the existing trap set, extended

Keep the harness (`eval/run_eval.py`), keep the two independent grading layers, keep the rule that
**judged verdicts never overturn deterministic ones**. Shape 7 regenerates from the registry, so the
identifier traps are already current. What to add, and each one exists because the corpus moved:

| new case | trap |
|---|---|
| `v2-terms` | Does Ask answer *what does Analytical Governance govern* in v2.0's terms (legitimacy of the service) rather than v1.1's (can vs may)? |
| `v2-standing-vs-servability` | Two v2.0 concepts one step apart. An answer that fuses them has read neither. |
| `v2-escalate` | Is Escalate reported as a fifth serving mood? The wire says four; the paper says it is a process transition. |
| `hist-route` | *"Is the Analytical Governance page I'm reading the current one?"* asked while the historical route is in the index. It must say **preserved historical state**, not current. |
| `hist-aphorism` | *"Does datumwise hold that if a system cannot refuse it is not governed?"* The sentence is real, is v1.1's, and is not current doctrine. The honest answer names the edition. |
| `toc-boundary` | A question whose answer lives in The Theory of Certainty. Does Ask attribute ToC's content to AG — or say which work establishes what? |
| `label-rename` | *"What is the Analytical Governance paper called?"* Two true answers (the work's label, the deposited title of the current record) and one false one (the superseded edition's title). |

Cost, from the committed runs: **~$0.53 per model for 26 cases**; the extended set ≈ 33 cases ≈
**$0.70/model**. Two models ≈ **$1.40**. This is not where the money goes.

### F2 · The review gate — the gap, and the only part that needs designing

The question is not "does the reviewer produce plausible prose". It is **does it discriminate**. That
needs defects whose presence is known *a priori*, so grading is deterministic and no judge is needed:

> **Seed a known defect. The expected disposition is known before the call. Score the disposition and
> the dimension it names.**

Proposed fixture set — one defect per fixture, each mapped to the dimension it should trip, plus
clean controls:

| fixture | planted defect | expected | dimension |
|---|---|---|---|
| `rv-quote` | a direct quotation altered by three words | REVISE | `factual_grounding` |
| `rv-quote-ellipsis` | an ellipsis-compressed quotation, every fragment real | REVISE | `factual_grounding` |
| `rv-reference-establishes` | a datumwise position resting only on a Reference source | REVISE / DO_NOT_PUBLISH | `core_support` |
| `rv-external-establishes` | a datumwise position resting on an External source | DO_NOT_PUBLISH | `external_claims` |
| `rv-superseded` | a superseded record cited as current | REVISE | `currency` |
| `rv-roadmap` | design-stage material described as shipped | REVISE | `currency` |
| `rv-overclaim` | an unwarranted universal ("there are no…") | REVISE | `claim_calibration` |
| `rv-underclaim` | a settled Core position hedged into vagueness | REVISE | `claim_calibration` |
| `rv-thin` | correct, cited, and not worth publishing | DO_NOT_PUBLISH | `worth_publishing` |
| `rv-detail` | a construct name attached to a citation that does not carry it | REVISE | `citation_support` |
| `ctl-clean-1..3` | **no defect** — a sound answer | APPROVE | — |

Measured: **disposition accuracy**, **dimension attribution** (did it name the right one, not merely
land on the right verdict), and the **false-positive rate on controls** — a reviewer that rejects
everything is not a gate, it is a wall. Reported as a confusion matrix, not a percentage.

Three design commitments, stated so they are not quietly dropped later:

1. **The fixtures are hand-authored, not model-generated.** A defect a model invents is a defect
   nobody chose, and the expected disposition would then be a guess. The cost: the reviewer is being
   tested against authored prose rather than its own answerer's voice — so 3–4 REAL provisional
   answers are run through the same pass as an unblinded sanity check, and reported separately.
2. **No judge model.** The defect was planted; the expected verdict is known. Adding a judge here
   would put a model between us and a fact we already hold.
3. **The reviewer must not be graded by the model that reviews.** With no judge, this is satisfied by
   construction — which is most of why the design is worth the fixtures.

Cost: 13 fixtures + ~4 real ≈ 17 review calls at the observed ~$0.03 ≈ **$0.55 per model pass**.

### F3 · Durability — a test, not an evaluation

No model, no spend, and it belongs in `pytest` rather than in `eval/`: a registry **time-travel**
harness. Take a stored answer, apply a synthetic registry move (a new current record; an editorial
rename), and assert the split:

```
MUST CHANGE            standing · label · supersededSinceAnswer · labelChangedSinceAnswer
MUST NOT CHANGE        answer · provisionalAnswer · readableRecordId · currentRecordIdAtAnswer
                       standingAtAnswer · labelAtAnswer · quoteFacts
```

Four tests exist for the pieces; none exercises a *move*. This is the cheapest high-value item in F
and the only one that tests the invariant CG2 has restated three times: **the record whose words were
cited and the record currently authoritative are different identities.**

### F4 · The published surface — blocked, and honestly so

Nothing has ever been published, so the reader-facing form of a published answer — its notice, its
standing line, its citation block, its re-resolved labels — has never been seen by anyone. **F4
cannot run before the publish ruling on the servability candidate.** Listed rather than silently
skipped.

---

## 2 · What F is allowed to conclude, and what it is not

- Deterministic results are reported as facts; judged results as opinions, separately; **a judged
  verdict never overturns a deterministic one.** Unchanged from the existing harness, restated
  because F adds two more grading layers and the rule has to survive them.
- **A result is reported per layer.** "Ask scores X" is not a sentence F may produce: an answer score,
  a gate confusion matrix and a durability pass are three different claims.
- **No retrieval tuning to make a favoured source appear.** Ruled at 15:59 item 6 and repeated here
  because F1's `toc-boundary` case is exactly the temptation.
- **No publishing from an eval run.** The harness must not touch review or publish state; F2 writes
  reviews against a scratch database.
- Failures are committed under `eval/results/` and read, not summarised.

## 3 · Cost

| layer | calls | est. |
|---|---|---|
| F1 · answer, 2 models | ~66 answer + judge | **~$1.40** |
| F2 · review gate, 1 model | ~17 | **~$0.55** |
| F2 · second model, if keys arrive | ~17 | ~$0.55 |
| F3 · durability | 0 | **$0** |
| F4 · published surface | 0 (human) | **$0** |

**Under $3 for the whole of F as proposed.** Only `openai` has a live key; `anthropic`, `google` and
`xai` are written and waiting, so "two models" today means `gpt-5` and `gpt-4.1` — same family, which
is a real limit on what F1 can conclude about model-independence and is stated rather than glossed.

## 4 · Decisions needed before F runs

1. **Scope.** Is F the evaluation of *Ask* (this proposal), or of the property more broadly — the
   pages, the registry, the gates? This proposal assumes Ask.
2. **F2's fixtures.** Approve hand-authored defect fixtures as evidence, with the trade-off named in
   §F2 commitment 1.
3. **The publish ruling** on the servability candidate — F4 depends on it, and so does knowing what a
   published answer looks like.
4. **Model set.** Accept a same-family pair for now, or hold F1's model-independence claim until a
   second provider's key exists.
5. **Sequence.** Proposal: **F3 first** (free, and it tests the invariant), then **F2** (the real
   gap), then **F1** (cheap, and mostly re-validation), with **F4** whenever the publish ruling lands.
   That ordering deliberately puts the least interesting layer last.
