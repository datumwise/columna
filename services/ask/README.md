# Ask datumwise — v0

A public agent that answers questions about datumwise from datumwise's own governed sources, and
shows the sections it used so a reader can check it.

    /ask  (static page on datumwise.ai)  ->  ask-datumwise.fly.dev  (this service)

## The shape

| piece | file | what it does |
|---|---|---|
| index | `ask/index_build.py` | builds the retrieval index **from the shipped site build**, joining every passage to its standing in the publication registry |
| retrieval | `ask/retrieve.py` | BM25 over 663 sections; historical and edition-pinned passages are demoted, never excluded, and always labelled |
| constitution | `ask/skill.py` | the datumwise-representative instruction — ~70 lines of prose, no machinery |
| providers | `ask/providers.py` | `provider:model` boundary; OpenAI live, Anthropic/Google/xAI written and awaiting keys |
| identifier gate | `ask/verify.py` | **the one hard check**: every DOI in an answer must exist in the registry |
| storage | `ask/store.py` | cached Q&A, votes, views, conversation log, and the ranking rule |
| pipeline | `ask/answer.py` | retrieve → constitute → call → verify → record |
| service | `ask/app.py` | seven JSON endpoints, stdlib only, per-IP rate limit |

## The three levels

Not a sequence — an assignment by failure class:

1. **Instruction** — the source boundary ("represent datumwise from datumwise"). Cheap; it works.
2. **Tool design** — standing. The model is never asked to *recall* which edition is current; every
   retrieved passage arrives with a derived `standing` line attached, so getting currency wrong
   requires contradicting the tool rather than merely forgetting.
3. **Hard gate** — identifiers, from day one rather than earned from failure. A fabricated DOI is
   silent, public, and falsifiable by a stranger with a browser.

## Running it

```bash
# rebuild the index after a site change (requires a site build first)
(cd apps/website && npm run build) && (cd services/ask && python3 -m ask.index_build)

# tests — hermetic, no key, no network
(cd services/ask && python3 -m pytest tests/ -q)

# the trap set, against one or more models
(cd services/ask && python3 eval/run_eval.py --models openai:gpt-5,openai:gpt-4.1)

# locally
(cd services/ask && ASK_DB=/tmp/ask.db ASK_ALLOW_LOCAL=1 python3 -m ask.app)
```

## The trap set

`eval/questions.json`. Shapes 1–6 are Huayin's brief. Shape 7 is **derived from the registry** —
every superseded record, every edition-pinned route, and every non-deposited teaching surface is a
trap, so the set stays current as the registry moves instead of rotting the way hand-written evals do.
Eight cases were added on 2026-08-26 when the corpus moved beneath the set: AG v2.0 superseded v1.1,
The Theory of Certainty entered Core, the v1.1 doorway became a preserved route *inside the index*,
and the work's editorial label was renamed.

Results are committed under `eval/results/` so failures can be read rather than summarised.

### When an evaluation may run at all — the governing rule (Huayin, 2026-08-26)

| what changed | what runs |
|---|---|
| registry · corpus · deposits · index **only** | **deterministic verification only. Zero model spend.** |
| an **agent-facing surface** — prompt, retrieval behaviour, provider/model, review rubric, or anything else that can materially change generated or reviewed behaviour | **evaluate once**, affected cases **only** |
| nothing agent-facing | **no evaluation run** |

> Do not spend model calls merely to reconfirm evidence-layer facts that can be established
> deterministically.

**Why this had to be ruled.** This harness was built to test the AGENT BUILD. It drifted into testing
the whole pipeline's output while the agent sat constant — which puts the spend on the one component
that had not changed. A corpus move cannot change what the agent *is*; it can only change what the
agent is HANDED, and what it is handed is exactly what a deterministic check reads directly.

The evidence for the rule is in this repo. Every retrieval failure found in F — `h2`, `r6`, and
`h4`'s false pass — was visible in the evidence layer before any model was called, and the repair was
verified in production across the whole class (registry currency, the typed-authority gate, historical
reachability) with **zero** model calls. See §6–7 of `specs/certainty_v1_1_reconciliation_report_v0_1.md`.

The rule is enforced by hand today. `OF-29` banks the harness guard that will enforce it in the
machinery, with an explicit human override that is recorded in the evaluation record rather than
silent — because a rerun that does not declare itself a deliberate rerun is the reflex the guard
exists to stop.

## The review gate, evaluated as a gate

`eval/review_fixtures.json` + `eval/run_review_eval.py`. A different shape of evaluation, because the
question is not whether the reviewer writes plausible prose but **whether it discriminates**:

> Seed a known defect. The expected disposition is known before the call. Score the disposition, the
> dimension it names, and the false-positive rate on clean controls.

Ground truth is hand-authored — a defect a model invents is a defect nobody chose — so **no judge
model appears anywhere in this harness**. Passages are not pasted into the fixtures: each source names
a chunk in the shipped index by `(sourceId, heading)` and the real text is resolved at run time, so a
planted defect is a defect against what the corpus actually says.

```bash
(cd services/ask && python3 eval/run_review_eval.py)                      # the whole fixture set
(cd services/ask && python3 eval/run_review_eval.py --only rv-quote-altered --tag targeted)
```

`--only` requires `--tag`: a subset run may not overwrite the file a full run wrote.

## Three source classes reach the model, not two

`[S#]` is the corpus. `[X#]` is the outside world. `[R#]` is **datumwise's own publication registry**,
added 2026-08-26 after evaluation F1 found the same defect on two independent models: passages inside
*other* papers that name the work being asked about — reference lists, reading paths, further-reading
pointers — out-ranked the work's own current deposit on questions about identity and currency. On one
case the system told a reader that a superseded edition was the current position, citing two other
papers' pointer sections as its evidence.

The passage was not wrong. The Frame-QL Primer's reading path says "Analytical Governance, Version
1.1" because that is what it was called when the Primer was deposited. It is authoritative *as part of
the Primer*, and it is not authority for what Analytical Governance is called today. That is a
question of ENTITLEMENT, not of score, so the repair is a source and not a filter — see
`ask/identity.py`, which also explains why the deeper cause was ours: the index deliberately holds no
publication facts, and we then asked questions only those facts can answer.

`[R#]` is the entitled authority for what a work is currently called, which version is current, which
DOI resolves to it, and what it superseded. It carries no argument and may not settle doctrine. It
appears only when the question asks about identity or currency AND names a work the registry knows;
it is never invented for a work that does not exist. `tests/test_typed_authority.py` holds it from
both sides.

## The durability and public-surface tests

`tests/test_durability.py` applies a synthetic registry move — a supersession and an editorial rename
together — and asserts which fields must change and which must not. On 2026-08-26 the corpus supplied
the real thing four hours later (The Theory of Certainty v1.0 → The Ground for Certainty v1.1), and
`tests/test_ask.py` now tests the same invariant against it, reading the live registry on purpose.
`tests/test_public_surface.py`
asserts what a reader can and cannot see: no provisional, rejected or reviewed-but-unpublished object
reaches the public collection, and no reputation appears on anything a human has not published. Both
are hermetic and in the ordinary test run.
