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

## The durability and public-surface tests

`tests/test_durability.py` applies a synthetic registry move — a supersession and an editorial rename
together — and asserts which fields must change and which must not. `tests/test_public_surface.py`
asserts what a reader can and cannot see: no provisional, rejected or reviewed-but-unpublished object
reaches the public collection, and no reputation appears on anything a human has not published. Both
are hermetic and in the ordinary test run.
