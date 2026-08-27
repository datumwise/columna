# Ask datumwise v0 — what the prototype demonstrated

Written after building and attacking it. Only things the prototype actually showed; nothing
imagined. Each item says what would change and why the evidence supports it.

## The instruction-first bet paid off, and the numbers say where

26/26 deterministic cases pass. On the judged criteria the citation bug could not have touched:

| criterion | score |
|---|---|
| separation (external vs datumwise) | **26/26** |
| premise_resistance (false premises) | **26/26** |
| currency (current vs superseded/pinned) | **24/26** |
| corpus_faithfulness | 23/26 |
| abstention | 23/26 |
| answer_quality | 23/26 |

Huayin's philosopher intuition holds for the source boundary: a ~70-line instruction plus disciplined
retrieval got perfect scores on premise resistance and external/datumwise separation. **No hard
mechanism was needed for either, and none was built.**

Currency at 24/26 is the interesting one, because it is the criterion we did NOT leave to
instruction — every passage arrives carrying derived standing. That is the Level-2 bet, and it is
the second-best score on the board.

## 1 · Retrieval is the weakest link, not the constitution

The clearest failure in the set is **s3** — "What is the authoritative reference for shipped Frame-QL
behavior?" The right answer is `/docs/grammar`, the generated, build-adjudicated reference verified
against the released parser. The agent named the Frame-QL Manual instead.

**This is a retrieval failure, not a reasoning failure.** `/docs/grammar` is in the index, and BM25
does not rank it in the top 10 for that question. The reason is visible: the reader asks for the
"authoritative reference for shipped behavior"; the page opens "Read this before writing a Manifold…
generated from columna-core 0.15.0 at build time." Almost no lexical overlap. The agent answered
well from what it was given; it was given the wrong sections.

**Change:** turn on the embedding path (already written, behind `ASK_EMBEDDINGS=1`) and re-run the
trap set. This is the one case in 26 where BM25's characteristic weakness — reader's words vs
corpus's words — is demonstrated rather than assumed. It is also the reason not to have turned
embeddings on by default before measuring: 25 of 26 did not need them.

## 2 · The output contract is the brittle joint

The only mechanism that failed in live use was the format agreement, not the reasoning: gpt-5 emitted
the required JSON without its fence, and every citation was lost. Fixed by parsing both shapes and
unioning with the inline markers.

**The general lesson, worth carrying into Authoring:** where the agent's output must be *machine
read*, do not let an instruction be the only thing holding the contract. Parse permissively, and
prefer evidence that lives in the prose the reader sees over metadata the model emits alongside it.

## 3 · Two of my own assertions were wrong, and the agent was right

On the first run, `s4` and `r2` "failed". Both were my test being wrong:

* `s4` demanded the literal `/research`; the agent had written "the Research page".
* `r2` forbade every DOI; the agent had correctly denied the asked-for DOI, then offered the
  registered current DOI of a correctly-named different work as an alternative.

**A trap set that fails good answers teaches nothing.** `must_any` was added and both were corrected.
Worth stating because it is the strongest evidence in the run: the deterministic layer produced
**two false positives and zero false negatives.**

## 4 · Abstention is strong on named things, weaker on abstract ones

The agent scored 5/5 on every "this thing does not exist" trap — the Trust Framework, Known Issues'
DOI, One Afternoon's DOI. It refused cleanly and explained why.

It was weakest on **b1**, "What does datumwise mean by trust?" — where the judge found it assembling
a confident definition rather than tightly scoping what the corpus actually says. The pattern:
**abstention is easy when the missing thing has a name, and hard when the question asks for a
doctrine the corpus only gestures at.**

**Change (only if it recurs):** nothing yet. This is one case, it is the hardest shape in the set,
and the honest move is to watch whether real readers ask this kind of question before building for it.

## 5 · Caching earned its place immediately, and degrades well

18.3s cold, **35ms** cached — and when the OpenAI account ran out of credits mid-session, the cached
Q&A kept serving for free while new questions failed. A read-mostly public surface built on an
exhaustible resource should degrade to its cache, and this one does. No change.

## 6 · Two security defects found by using it, both fixed

* **Provider errors leaked to the client** — the credit-exhaustion error handed the browser our
  provider, status, error code and organisation billing URL. Now one sentence to the reader, full
  detail to the server log.
* **/ask had no spend control.** The CORS allow-list is not one: browsers enforce it, `curl` ignores
  it. A per-IP limit (30/hour, 120/day) now stands between a script and the bill. It is crude and
  in-memory; if the surface sees real traffic that is the first thing to replace.

## 7 · The gate taught the agent something

G7 rejected the retrieval index for carrying literal DOIs, and it was right: a committed index of
page text is a second source of truth for identifiers that goes stale when the registry moves. The
repair — foreign keys in the index, identifiers resolved from the registry at request time — is
strictly better than what it replaced, and the agent now receives *more* than before, all of it live.

**The generalisable claim:** the discipline that keeps the website honest transferred to the agent
without modification. That is evidence for the Gateway-2 thesis that the source/standing layer, not
the agent framework, is where datumwise's real work lives.

## What I would NOT change

* No embeddings by default (25/26 did not need them; case s3 is the argument for measuring, not for
  switching them on blind).
* No semantic canonicalisation of duplicate questions — not one duplicate has been observed yet.
* No additional hard gates. The identifier gate fired correctly and nothing else demanded one.
* No framework adoption. The service is stdlib-only and the whole API is one file.
