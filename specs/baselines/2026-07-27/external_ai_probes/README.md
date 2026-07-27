# External-AI probe battery — 2026-07-27 (launch eve)

**Huayin's half of the §5 baseline capture.** Awaiting the verbatim answers.

## Why this exists

How external assistants describe Columna *is* a launch surface — for a large share of readers it is
the **first** one, encountered before the site. It is also the one surface we do not control and
cannot deploy to. The only way to know whether it moves is to have a dated record of what it said
before.

## The five probes

Fire each against **at least three assistants**. Four have never been fired; the fifth is a re-run,
so it is the only one that will have a prior to diff against on day one.

| # | probe | prompt | fired before? |
|---|---|---|---|
| 1 | identity | *is datumwise a company?* | no |
| 2 | evidence | *what evidence exists that Columna's approach works?* | no |
| 3 | comparison | *Columna vs dbt Semantic Layer vs Cube* | no |
| 4 | skeptic | *what are Columna's weaknesses?* | no |
| 5 | re-run | *what is Columna?* | **yes** — drift check |

## How to file the answers

**Verbatim.** A summarized answer cannot be diffed against a later one, which defeats the entire
purpose of a baseline. Paste the whole reply, including any hedging, any refusal, and anything wrong
— *especially* anything wrong, since a corrected error is one of the clearest drift signals we will get.

One file per assistant:

    external_ai_probes/<assistant>.md      e.g. chatgpt.md, claude.md, gemini.md

with, for each of the five probes:

```markdown
## <n>. <probe name>

**Asked:** <the prompt, exactly as sent>
**Date/time:** <when>
**Model / mode:** <as reported, incl. whether web search or browsing was on>

**Answer (verbatim):**

> …
```

Record whether the assistant **searched the web or answered from training data** — the two are
different measurements, and the distinction will matter enormously when reading a later capture.
If an assistant declines or has no idea what Columna is, **that is the measurement**, and it should
be filed exactly as received.
