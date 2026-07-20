# Columna is now available: the open-source data framework that refuses to return a confident wrong number

*For the AI era, where machines answer metric questions instantly and without hesitation, we built the grammar layer analytics never had.*

Today we are releasing **Columna** — an open-source data framework designed for the age of AI analysts, and wired for them: every capability below is served over MCP as naturally as in Python.

The problem is no longer hidden. Ask "what was our average order value?" on a single dataset and you can legitimately get three different answers depending on the unstated grain (per order, per line item, or per customer). Human analysts used to argue about this. AI systems usually don't — they return one confident number, often defensible but wrong in context. Semantic layers and text-to-SQL tools haven't fixed this, because the fix is architectural: nothing in the stack *adjudicates* whether a metric question is even well-posed over the data at hand.

Columna changes that.

## What Columna is

Columna is a framework in the same sense the relational model was: a data model, a query language, and an engine, under one law. The data model — the **Manifold** — holds what your data *means*: measures over anchors (columns as the true atomic unit of analysis, not tables as containers), populations with declared absence semantics, hierarchies that are checked against the data, and operations barred where the arithmetic doesn't survive the trip. The query language — **FrameQL** — can only ask for meaning the model declares. The engine serves nothing the model can't defend. Three parts, one law: nothing answers unless the model has already justified it against the data.

The result is structural honesty. Every answer comes back in one of **four moods**, on one wire contract:

* **Serve** — here's the number.
* **Disclose** — here's the number, plus the material assumptions it rides on.
* **Clarify** — your question has more than one legitimate answer; choose.
* **Refuse** — that metric is not defined over this data — and here's why.

These moods are not prompts or best practices. They are enforced by the framework itself: the model is adjudicated against the data at publish, and the planner rules every query against the model before the engine computes a thing. AI agents — over MCP or in natural language — get the same transparency a careful human analyst would demand.

One example from the live demo, because it makes the temperament concrete: products sit in multiple categories, so "revenue by category" double-counts; Columna bars the naive rollup, offers the declared lawful crossing, and serves it *with the over-count stated on the answer* — 1.44× the grand total, which is exactly the category bridge's own fan-out. The wrongness is deliberate, labeled, and refusable.

## Why this matters now

As agentic AI moves from experiment to production, the cost of silent metric failures is rising fast: an agent answering a thousand metric questions a day doesn't get tired or suspicious — it gets confidently wrong at scale, in writing, with no analyst in the loop to squint. Columna provides the blast wall: the grammar layer adjudicates, while your semantics — names, intent, conversation — stay expressive. It sits beside your semantic layer, married to no database, and directly addresses the grain gap and the silent failure modes catalogued in our public Atlas.

## Try it right now — two minutes, no signup

```bash
pip install columna
columna-server demo --play
```

You'll watch a real clarify, refuse, disclose, and serve print as wire JSON, running locally over a complete worked case.

## Go deeper

* **[The Case](https://datumwise.ai/case)** — Cascadia Retail, end to end: the company, the warehouse, the design and its reasons, and the system live. Every number on our site is a recording from the shipped package — including the transcripts where our own agent stumbled, all takes preserved.
* **[The Thesis](https://datumwise.ai/thesis)** — the full argument.
* **[The Grain Gap](https://datumwise.ai/why)** — why the problem is urgent for AI.
* **[The Atlas](https://datumwise.ai/atlas)** — a living catalog of silent analytical failures.

Everything is open source under Apache-2.0: [github.com/datumwise/columna](https://github.com/datumwise/columna)

We are not claiming Columna replaces your semantic layer. We are claiming that correctness should be machine-checkable, and that refusal is sometimes the most responsible answer. A number owes you its assumptions — Columna makes that enforceable.

If you have ever been surprised by inconsistent or silently wrong metrics from AI systems, this project is for you. We welcome contributions to the Atlas, feedback on the Manifold concept, design partners for real-world testing, and open discussion on the thesis.

The debt in analytics came due the day the analyst stopped being human. Columna is our attempt to pay it.

— The datumwise team
