# What is FrameQL — and why?

*A plain-language companion to the FrameQL manual. Loose analogies ahead — the manual draws
the exact lines.*

---

FrameQL is the query language of the Manifold. The name tells you almost everything, so
let's start there.

## The name is the idea

Start with **DataFrame** — the thing every analyst already knows. Now take the **Data** out.

What's left is the **Frame**: and here's the surprise — it still has everything. A frame is
a collection of column expressions standing at one anchor. Each column says *what it is*
(revenue; average order value; last inventory level), and the anchor says *where it stands*
(by month; by store and month). No rows needed. The rows are the data's job.

FrameQL is the conclusion of that thought: **the Frame is the query.** You don't write
instructions for computing a table — you *describe the frame you want*, and the Manifold,
which already knows the data's laws, produces it. A query is a declaration, not a recipe.

## What that looks like

```
SELECT revenue, order_count
AT {region}
```

Read it as: *the frame whose columns are revenue and order count, standing at region.*
That's the whole query. Notice what's missing:

- **No `FROM` full of tables.** At most a Manifold's name — one word, and only when you
  work across several. The Manifold is the from.
- **No `JOIN`.** The Manifold already declares how store reaches region and day reaches
  month — the paths are part of the model, checked and badged. You never re-teach the
  data's geography in a query; you just stand somewhere.
- **No `GROUP BY`.** The anchor *is* the grain. `AT {region}` doesn't group rows — it
  declares where the frame stands, and everything arrives there lawfully or tells you why
  it can't.

It reads SQL-adjacent on purpose. But don't let the familiarity fool you — the *column* is
where the two languages part ways.

## The #1 difference: a column is three things

In SQL, a column is a name. In Columna, what a column of the frame really is decomposes
into **three pieces**:

1. **the metric family** — *which quantity*: revenue, order value, inventory level;
2. **the operator** — *how it arrives*: summed, averaged, last-observed, counted;
3. **the anchor** — *at what grain*: read from orders, standing at month.

SQL has all three too — it just scatters them. The quantity is in the SELECT, the operator
is an aggregate function somewhere, the grain is implied by a GROUP BY several lines away,
and nothing checks that the combination *means* anything. FrameQL puts the three pieces in
one expression and the Manifold checks the combination against declared law: `sum` over
revenue at month is lawful; `sum` over an inventory *level* across months is not a real
total, and the answer will say so.

The `@` is the third piece's character. Some quantities change meaning depending on the
grain you compute them *from* — "average order value by month": averaged over *orders*, or
over *days*? Different numbers. SQL can't even ask the question cleanly. FrameQL gives it
one character:

```
SELECT avg(aov @ order)
AT {cal.month}
```

*Average the order-level `aov`, standing at month.* The `@` marks the **input anchor**;
`AT` marks the output. Two anchors, two jobs, one character apart. Leave the `@` off where
it matters and the Manifold doesn't guess — it answers in the `clarify` mood: *here are the
readings, pick one.* The language refuses to let an ambiguous question produce a confident
number.

## Columns are expressions, not names

The second thing SQL habit won't expect: there are **no column names** in FrameQL — not
even in the simplest query. `SELECT revenue` doesn't name a column; `revenue` is a **metric
family**, and the frame column it produces is already an expression — the family's default
operator, at a lawfully inferred anchor, filled in by rule (and refused with a `clarify`
when the rule can't decide). From there, a column can be a full **mathematical
expression** — operators over multiple metrics, composed freely (within one population):

```
SELECT (revenue - cost) / revenue AS margin,
       revenue / order_count     AS aov_per_order
AT {region*cal.month}
```

A margin and a per-order average, each written as *what it is* and named with `AS`
(composite expressions have no mechanical default name — the language asks you to name
what you compose) — no CTEs, no intermediate
views, no re-stating the grain for each piece. The expression's components share the frame's
anchors and the Manifold's laws travel through the arithmetic: if any piece can't stand
lawfully at the anchor, the whole column says so instead of quietly computing nonsense.

(One population per expression, note — a ratio across two different populations isn't a
formula, it's a category error, and the language treats it as one.)

## The query SQL makes you fight for

Here's a small thing FrameQL does in two clauses that SQL makes you earn with a window
function and a subquery: *top 3 stores by revenue, within each region.*

```
SELECT revenue
AT {region*store}
ORDER BY region, revenue DESC
LIMIT 3 PER {region}
```

The frame stands at *region and store*; the ranking happens along `ORDER BY`; and
`LIMIT 3 PER {region}` keeps the top three *within each region*. In SQL that's
`ROW_NUMBER() OVER (PARTITION BY …)` wrapped in a subquery because you can't filter on a
window function directly — the operational machinery leaking into your question. Here the
question is just… stated.

Two quiet laws are at work, and both are the frame model being honest. First: region is
**in the anchor** — `ORDER BY` and `PER` may only reference the frame's own columns, so if
region participates, region is in the frame. There is no sorting by invisible columns; the
Frame *is* the query. Second: nothing in the query asserts that a store belongs to one
region — that's not the query's job. The `store → region` path is **declared in the
Manifold and checked against the data**, verdict attached; each store row carries its one
region because the model *knows* it, and if the data ever contradicts it, the answer says
so instead of quietly doubling rows.

## The rest of the envelope

- **`WHERE`** filters the *input* (before any reduction) — and if a filter dimension can't
  lawfully reach some series' input, you get a clarify, never a silently partial answer.
- **`HAVING`** filters the *output frame*, by column name, after reduction — name a
  column with `AS` (`SELECT sum(revenue) AS total AT {customer} HAVING total > 10000`), or
  use the mechanical default (`sum(revenue)` answers to `sum_revenue`). The old distinction,
  made precise: `WHERE` restricts what is reduced; `HAVING` restricts what is shown.
- **`ORDER BY` / `LIMIT`** as above — with the `PER` rules pinned down so results are
  deterministic.

And one thing you might expect that isn't there: there's no way to name a *universe* in a
query. Which population a measure describes is a fact of its *definition*, settled when the
Manifold was declared — not a choice you make (or get wrong) at query time.

## Why this is the natural way to ask a Manifold

Every query language carries the knowledge its data model lacks. Tables know nothing, so SQL
must carry everything: the joins, the grouping, the grain, the caveats — all yours to get
right, every single time, in every query.

A Manifold already holds that knowledge — the populations, the paths, which totals survive
which trips — *checked against the data and wearing verdicts.* So the query has almost
nothing left to say except the one thing only you know: **what frame you want.** That's why
FrameQL is small, why it's declarative, and why its answers come back in the four moods
(serve · disclose · clarify · refuse) — the model knows enough to be honest about what you
asked.

## Try it

```
SELECT level.sum
AT {store*cal.month}
```

Ask the demo Manifold to sum an inventory level into months and it will serve the per-month
figures — with a note explaining why snapshots summed over time don't add to a meaningful
total. The language doesn't stop you; it makes sure you know. (Run it: the [Explorer](/explorer)
has a copy-as-query button on every measure.)

## Go deeper

- **[The FrameQL manual](/docs/frameql)** — the grammar, the semantics, the type rules,
  completely.
- **[What is a Manifold?](/what-is-manifold)** — the model this language is paired to.
- **[What is Columna?](/what-is-columna)** — the framework this language speaks to.
- **[The Explorer](/explorer)** — the demo Manifold, live, with queries to copy.
