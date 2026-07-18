# What is Columna?

*A plain-language orientation. Rough analogies ahead — the manuals draw the exact lines.*

---

Columna is a framework for describing what your data **means**, shipped as a Python library.
You describe the meaning once — what the populations are, what the measures are, which
totals are safe to take — and Columna checks that description against the actual data and
serves it to whoever asks: an AI agent over MCP, or you directly.

It's a library in the way SQL is "a language": technically true, but the interesting part is
the model underneath. pandas and polars operate on values. Columna works one level up, on
what the values mean.

## Where it sits

A quick way to place it — five ways of getting an answer out of data:

```
a)  you → SQL → tables
b)  you → SQL → semantic layer → tables
c)  you → question → agent → SQL → semantic layer → tables
d)  you → question → agent → FrameQL → Manifold → tables
e)  you → FrameQL → Manifold → tables
```

Columna is (d) and (e). The step from (c) to (d) is the interesting one: the agent stops
writing SQL. In (c), even with a semantic layer underneath, the agent still speaks the
physical language — it can name tables, columns, joins. In (d), the agent speaks **FrameQL**,
a small language that only has words for meaning. There are no words for tables in it.

A rough picture: the Manifold is a **map of the city**, and FrameQL asks about *places*.
SQL asks about the *pipes*. The Manifold is the one component that knows both — it reads
your tables underneath and answers in meaning above. Your agent orders from the menu; it
never needs to walk into the kitchen.

## The pieces, by analogy

If you know the BI world, each piece has a familiar counterpart, one level up:

| the BI stack | the Columna stack |
|---|---|
| ODBC/JDBC — how anything connects | **the Columna API** — how anything connects |
| the relational model and its tables | **the Manifold** — the data model underneath the API (not a database, not your schema) |
| SQL, against tables | **FrameQL**, against the Manifold |

Agents usually arrive through **MCP**, which is a thin shell over that same API — a plug
shaped for one kind of caller. Path (e) skips it entirely: you can speak to the API
directly.

The Manifold holds the description: which **populations** exist (transactions; store-days),
which **coordinates** you can stand at (day, month, store, region) and how they connect,
which **measures** live where, and the rules that govern them — for instance, that an
inventory level is a snapshot, so summing it across months produces a number that doesn't
mean anything.

One more thing the Manifold does, and it's the part that tends to surprise people: it
**checks the description against the data.** Each claim gets tested and carries a small
verdict — verified, corroborated, untestable, or contradicted. You can see these in the
[Explorer](/explorer): every measure, with its definition, its verdict, and a query to try.

## What an answer looks like

Ask the Manifold a question and the answer comes back in one of four moods:

- **serve** — here's the number.
- **disclose** — here's the number, plus something you should know about it (say, you summed
  a snapshot across months — you get the per-month figures, with a note explaining why
  they don't add up to a meaningful total).
- **clarify** — the question can be read two ways; here are the readings, pick one.
- **refuse** — the data can't honestly answer this, and here's why (the classic: asking for
  inventory by customer, when inventory simply doesn't have customers).

Every answer is a pair — the result and its context — so whoever's asking (an agent or you)
always knows what they're standing on.

## How a Manifold gets made

You don't write one from scratch. `columna init` reads your database — schema, profiles,
samples — and proposes a Manifold: the populations it sees, the measures, the rules. You
review and adjust; it can't finalize anything on its own. (By design, it's free to propose
*restrictions* but can't invent *permissions* — those are yours to grant.) Then the checks
run, the verdicts attach, and it's ready to serve.

## Try it in two minutes

```
pip install columna
columna-server demo --play      # four asks, four moods, on seeded demo data
```

Then open the [Explorer](/explorer) to browse the same demo Manifold the tour just queried.

## Small glossary

- **Manifold** — the described, checked data model that agents (or you) query. Not a
  database; not your relational schema.
- **Universe** — one population of facts (transactions; store-days). Every expression
  evaluates inside exactly one.
- **Level / edge** — the coordinates: grains you can stand at, and the declared paths
  between them (`day → month`, `store → region`).
- **Measure / derived** — a quantity read from the data; a quantity defined from other
  measures.
- **Basis** — what a missing row means in a universe: a real zero (event streams), a gap
  (a grid with a hole in it), or a membership fact (a registry).
- **Verdict** — the result of checking a described claim against the data: verified,
  corroborated, untestable, or contradicted.
- **describe** — the machine-readable rendering of a Manifold; what an agent reads first.
- **FrameQL** — the query language against the Manifold, as SQL is to tables. You declare
  the frame you want: `SELECT aov AT {cal.month}`.
- **The wire** — the answer format: result + context, in one of the four moods. The same\n  contract whether it arrives over MCP or straight from the API.
- **`columna init`** — reads a database and proposes a Manifold; you review and decide.

## Go deeper

- **[The Columna framework manual](/docs/framework)** — the full discipline, precisely.
- **[The FrameQL manual](/docs/frameql)** — the query language, completely.
- **[What is a Manifold?](/what-is-manifold)** — the artifact at the center: the new data
  model, up close.
- **[The Explorer](/explorer)** — the demo Manifold, live.
- **[Install](/install)** — set up against your own data.

*And for why any of this matters — the argument, not the orientation — see [Why](/why) and
[The Ladder](/ladder).*
