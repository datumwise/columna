# Servability candidate — regenerated against current Core (2026-08-26)

Ruling E.6 (CG2, 2026-08-26): retire the old provisional servability Q&A, generate a fresh
candidate against current Core, run it through the review workflow, **do not publish**, bring the
candidate and the review packet back. This is that packet. The machine-readable form is
`servability_candidate_2026-08-26.json` beside this file — question, answer, every source with
both standing sentences, the reviewer's nine findings, and the quote-verification facts.

**Nothing is published.** The candidate sits provisional and unpublished, which is where the
ruling says to stop.

---

## 0 · Retiring the old candidate — what was actually there to retire

The step-5 candidate (commit `53cca2d`) lived in a **local, ephemeral SQLite file**. It is gone:
the container that held it has been replaced, and no durable surface ever carried it.

Checked rather than assumed, on the live deployment (`ask-datumwise.fly.dev`, 2026-08-26):

- `/qa` returns **three** rows — the four moods, and two Never-Let-Your-Agent questions. No
  servability answer, published or cached.
- `/review/queue` is **not reachable**: `ASK_REVIEW_TOKEN` is unset there, so the review surface
  is closed and no candidate could have been queued through it.
- the live index reports **1280 chunks**; the committed index is **1318**. The deployment predates
  the ToC/AG v2.0 reconciliation entirely.

So the retirement is a **recorded fact, not a performed reject**: there was no durable row to
reject, and no reader ever saw the v1.1-era answer. What is retired is its *standing as a
candidate* — it is not revived, not re-reviewed, and not carried forward. The screenshot in
`review-candidate.png` stays as evidence of the workflow, dated, and is not current authority.

The v1.1-era candidate is also the finding that produced `citations.py`: its four stored citations
read, as literal text, that Analytical Governance v1.1 was the current record. That defect is
fixed at the architecture (step D, accepted), and the fresh candidate below is the first one
generated after the fix.

---

## 1 · The question

> Why does datumwise use "servability" rather than "serviceability" or "answerability"?

Deliberately the **same question, verbatim**, as the retired candidate. A different question would
have made this a new test instead of the same test against a moved Core.

## 2 · What retrieval put in front of the model

Top-8, BM25, standing attached to every passage:

| token | layer | source | section |
|---|---|---|---|
| S1 | core | Analytical Governance v2.0 | Abstract |
| S2 | core | Analytical Governance v2.0 | 13. Conclusion |
| S3 | core | Analytical Governance v2.0 | 7. Standing: what the service may pass forward |
| S4 | core | Analytical Governance v2.0 | 2. What must remain true |
| S5 | core | Analytical Governance v2.0 | 4. The servability gap |
| S6 | core | The Statistical Bridge v3.0 | 2. The bridge practitioners already use |
| S7 | core | Frame-QL: An Introduction | 10. Consequences of declaring the output |
| S8 | core | Analytical Governance v2.0 | 12. Requirements and non-claims |

**Two facts worth reporting rather than smoothing over.**

1. **Analytical Governance v1.1 did not appear at all.** It is indexed as `layer: reference`,
   `isHistorical: true`, demoted and labelled — and on the question whose old answer was built
   entirely from it, it no longer ranks into the top 8. The demotion is doing its job.
2. **The Theory of Certainty did not appear either.** The ruling asked for a candidate against
   current Core *as retrieved*, and honestly reported: BM25 did not surface ToC for a
   terminology question about servability, so ToC contributed nothing to this answer. That is a
   retrieval outcome, not a jurisdiction ruling — ToC is in the index as Core (16 passages). It is
   the same class of gap as FINDINGS.md §1 (`s3`, `/docs/grammar`): reader's words vs corpus's
   words. No repair was attempted for this run, because tuning retrieval to make a named source
   appear would be steering the evidence.

## 3 · The provisional answer

Model `openai:gpt-5` · 27.5s · $None. Identifier gate: **pass** (0 fatal, 0 warnings).

```
Short answer: datumwise uses servability to name a specific governance gate: whether a produced result has the analytical permission to be served as the answer to the governed request. It is about permission under grounds, not about mere capability or convenience.

What the corpus establishes
- Definition and scope. Servability is “whether the result has the analytical permission required to be served as that answer,” with request, result, and answer distinctly defined in the service flow [S1]. It is a gate in the passage from intent to use [S4].
- What makes something servable. A request is servable if and only if it is both analytically established (lawful object and derivation) and support-sufficient (the required evidence/state are actually present). Computability does not imply servability. Servability grants analytical permission; later authorization and disclosures still govern whether it is actually served [S5].
- Separation from what comes after. Standing is a further, boundary-specific question about what a served result may now be treated as or relied on for. That is distinct from servability [S3]. The discipline’s maxim is “Serve only what is servable,” then preserve standing and govern consequential use [S2].

Why not “serviceability” or “answerability”?
- The corpus does not define those alternative terms. What it does do is carve the service into distinct adjudications—faithful request, reliable production, servability, standing, and consequential use—so each can be judged on its own grounds [S4], [S8].
- Analysis: Using “serviceability” would risk conflating servability’s governance question (permission under law and support) with operational ability to compute or deliver; the corpus is explicit that computability and platform mechanics are not sufficient for servability [S5].
- Analysis: Using “answerability” would blur servability with either “can we produce some answer” (again, computability) or with post-serving authority. The corpus separates those: first, whether it may be served at all (servability) [S1], [S5]; then, if served, what it may stand for at a boundary (standing) [S3]; and, separately, risk/authorization for consequential use [S2], [S4].

In short, datumwise chooses servability because it centers the governed permission to serve a specific answer under present grounds. That precision is necessary to keep capability, permission, and post-serving authority from collapsing into each other [S1], [S2], [S3], [S4], [S5], [S8].
```

## 4 · Citations, with both standing sentences

**[S1]** `layer=core` — Abstract  
  · standing now: current record v2.0 (2026-08-26, doi:10.5281/zenodo.22115819); deposited text — read from the deposited record, not from a page on this site  
  · readable record: `w-analytical-governance.r03` · superseded since answer: **False**  
**[S2]** `layer=core` — 13. Conclusion  
  · standing now: current record v2.0 (2026-08-26, doi:10.5281/zenodo.22115819); deposited text — read from the deposited record, not from a page on this site  
  · readable record: `w-analytical-governance.r03` · superseded since answer: **False**  
**[S3]** `layer=core` — 7. Standing: what the service may pass forward  
  · standing now: current record v2.0 (2026-08-26, doi:10.5281/zenodo.22115819); deposited text — read from the deposited record, not from a page on this site  
  · readable record: `w-analytical-governance.r03` · superseded since answer: **False**  
**[S4]** `layer=core` — 2. What must remain true  
  · standing now: current record v2.0 (2026-08-26, doi:10.5281/zenodo.22115819); deposited text — read from the deposited record, not from a page on this site  
  · readable record: `w-analytical-governance.r03` · superseded since answer: **False**  
**[S5]** `layer=core` — 4. The servability gap: from governed request to answer  
  · standing now: current record v2.0 (2026-08-26, doi:10.5281/zenodo.22115819); deposited text — read from the deposited record, not from a page on this site  
  · readable record: `w-analytical-governance.r03` · superseded since answer: **False**  
**[S8]** `layer=core` — 12. Requirements and non-claims  
  · standing now: current record v2.0 (2026-08-26, doi:10.5281/zenodo.22115819); deposited text — read from the deposited record, not from a page on this site  
  · readable record: `w-analytical-governance.r03` · superseded since answer: **False**  

Every citation is Core and every one resolves to `w-analytical-governance.r03`. `standing` and
`standingAtAnswer` are identical because the answer was written after the supersession, and
`supersededSinceAnswer` is false on all six. That is the durable-citation machinery reporting *no
drift yet* — which is the only honest reading on day one, and the field that will change by itself
when v2.1 lands.

## 5 · Quote verification — now read back from durable storage

**Repaired under ruling E.7 before this packet was re-issued.** The facts below are no longer
recomputed for the packet: they are read out of the `reviews` row, which is what the review screen
renders and what a later reader will find.

```
  VERBATIM MATCH — attributed to S1, S4
    quoted: "whether the result has the analytical permission required to be served as that answer,"
    fact:   exact match, except the quotation's terminal punctuation, which belongs to the sentence
            hosting it
```

`quoteFactsRecorded: true` · `quoteFactsReconstructed: true` · one quotation, `verbatimMatch: true`,
`foundIn: [S1]`.

**Reconstructed, and it says so.** This review ran before the column existed, so its facts were
recomputed from the stored answer and the stored evidence and written with `reconstructed: true`.
`quotes.verify()` is deterministic over two immutable records, so they are the same facts — and the
review screen carries a banner saying they were re-derived rather than captured, because a
re-derived fact and a recorded one are different things. **No second model review call was spent:**
the reconstruction reproduced the facts the reviewer had, character for character, including the
terminal-punctuation clause.

What the repair added, and nothing more:

- `reviews.quote_facts`, a JSON envelope: `facts` (structured verdicts), `asSent` (the rendered
  block exactly as the reviewer received it — a newer formatter may not re-render old facts and
  still call it the same evidence), `reconstructed` (a flag, never a default).
- `NULL` means **not recorded**, which is not `[]`. An empty list is the check having run and found
  no quotation of five or more words. Silence and an empty result are different facts, and the review
  screen renders them differently.
- `store.attach_quote_facts()`, which **refuses** to overwrite facts that were genuinely captured.
- `ask/backfill_quote_facts.py`, a script rather than a migration, because recomputing what a
  reviewer was told is a re-derivation and deserves to be an explicit act.
- The review screen renders all four states — VERBATIM MATCH, NOT VERBATIM, UNKNOWN, UNATTRIBUTED —
  plus the not-recorded and reconstructed banners, with the as-sent block behind a disclosure.

Quote verification was **not** broadened. It still answers only *is this string in that text*.

## 6 · The review verdict

**APPROVE** · `openai:gpt-5` · 30.3s · $0.03144 · no proposed revision, no changes.

> Well-supported use of CORE sources explains why datumwise uses “servability” and distinguishes it from computability, service mechanics, standing, and consequential use. Quotations check out, analysis is clearly labeled, and claims are calibrated. One minor note: the line about the corpus not defining alternative terms implicitly refers to the cited corpus, which is acceptable here. Overall, suitable for publication without changes.

| dimension | ok | note |
|---|---|---|
| `core_support` | ✓ | Claims about servability’s definition and role trace directly to CORE sources. For example, “Servability is ‘whether the result has the analytical permission required to be served as that answer,’” is verbatim from S1; “Servable = Support Sufficient AND Analytically Established” and “Computability does not imply servability” are from S5; the separation from standing (“Standing is a further, boundary-specific question…”) is supported by S3; and the sequence placing servability as a gate is supported by S4 and S1. |
| `reference_use` | ✓ | No REFERENCE or EXTERNAL sources are used. All establishing claims rely on CORE sources explicitly labeled [S1]–[S5], [S8]. |
| `currency` | ✓ | All citations are to the current record v2.0 (2026-08-26). No roadmap or superseded material is invoked. |
| `citation_support` | ✓ | The direct quotation “whether the result has the analytical permission required to be served as that answer,” is verified verbatim to S1/S4. Other cited specifics are supported: “Serve only what is servable” (S2), the iff condition for servability (S5), and the post-serving authorization/disclosure separation (S5). |
| `factual_grounding` | ✓ | Prose stays within what the sources establish. The use of “if and only if” matches S5’s explicit equivalence. “It is a gate in the passage from intent to use” is warranted by S1 (calling servability a governing gate) and S4’s service flow. No invented attributions or overstated quotes detected. |
| `external_claims` | ✓ | No external claims are made. |
| `separation` | ✓ | The answer clearly separates corpus-grounded statements (“What the corpus establishes”) from Ask’s own reasoning (“Analysis”). |
| `claim_calibration` | ✓ | Strength matches evidence. Where the answer extends beyond the text (“Why not ‘serviceability’ or ‘answerability’?”), it is explicitly marked as Analysis and bounded by the cited architecture. Minor note: “The corpus does not define those alternative terms.” reasonably refers to the provided corpus; it does not over-claim beyond the cited materials. |
| `worth_publishing` | ✓ | Concise, well-supported, and addresses a specific terminological choice with clear governance implications; worth publishing. |

## 7 · Findings

**A · The review-record defect is FIXED (E.7).** See §5. `review.review()` now returns the rendered
block as well as the structured facts; `save_review()` persists both; `_review_row()` returns them
with `quoteFactsRecorded` first, so an unrecorded review can never be read as a review whose answer
quoted nothing; the screen renders them. Four new tests, 62 green.

**B · The candidate is an APPROVE, so this run still does not exercise REVISE.** Restated rather
than quietly dropped: the proposal path is implemented, unit-tested and fails closed, and the only
model that has ever chosen it on real material did so on the parked Anthropic comparison. One
APPROVE on datumwise-only Core is not evidence that the reviewer discriminates.

**C · NEW — the same class of defect the durable-citation work fixed, one field over: `label`.**
The citations in §4 read *"Analytical Governance: From User Intent to Governed Analytical
Execution"*, which is the editorial label as it stood when the answer was written. Under ruling E.1
that label is now *"Analytical Governance"*. `citations.resolve()` re-resolves **standing** from
record identity and leaves **label** as stored text — so a stored citation goes on displaying an
editorial name the registry has since changed, exactly as it used to go on displaying a superseded
standing sentence.

It is a narrower defect than the standing one and worth stating precisely rather than escalating:
`label` derives from `works.canonicalLabel`, which is *editorial naming* and Work-level, so it does
not bear on which record was cited. The architectural invariant is untouched — the record whose words
were cited is `w-analytical-governance.r03` in both the stored citation and the re-resolved one, and
nothing collapses it into the work's current record. But the label is a **resolved presentation**
carried as text, which is the shape this repo keeps correcting.

**Not fixed, and not begun.** It needs a ruling: either label joins standing as a re-resolved
presentation (identity is already stored — `sourceId` → `workId` → `canonicalLabel`), or stored
labels are deliberately frozen as what the answer was shown, in which case the review screen should
say so. Both are defensible; picking one silently is not.

## 8 · What a human still owes

Publish, edit, or discard. Nothing here decides that.
