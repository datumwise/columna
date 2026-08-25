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

Results are committed under `eval/results/` so failures can be read rather than summarised.
