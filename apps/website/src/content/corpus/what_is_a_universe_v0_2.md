# What is a universe?

A **universe** is a population of records plus everything you can lawfully say
about it. It's the answer to a question every warehouse quietly dodges: *when
you ask for "revenue by category," what world is that question even asked in?*

## Start with a population

Every fact table is *about* something. Cascadia's `transactions` table is about
**sale lines** — one row, one line sold: a customer, a store, a product, a day,
an amount. Its `eom_inventory` table is about **stock snapshots** — one row per
store per day, a level read off the shelves.

That "about" is the universe's **base**. And bases differ in what absence
means: a missing sale-line combination means *nothing happened* — an honest
zero (an **events** base); a missing snapshot means *a gap in a grid that
should be complete* — and answers over gaps must say so (a **spine** base).
Same warehouse, two different kinds of nothing.

## Grow it by the arrows that don't lie

From the base, the universe grows along **many-to-one arrows** — the
relationships where each thing has exactly one home. Every store has exactly
one region. Every day sits in exactly one month; every month in one quarter.
So from a sale line you can climb: store → region, day → month → quarter →
year. Numbers climb these arrows safely — revenue by store rolls up to revenue
by region and nothing is counted twice, *because each store has one region to
give its revenue to.*

Everything reachable this way — the grains, and every attribute they carry —
belongs to the universe. That's the whole rule: **a universe is a base plus
its many-to-one closure.** You don't choose its size; the data's own structure
decides, and the model just writes it down.

## And then the arrow that breaks

Cascadia's products sit in **up to three categories**. Product → category is
many-to-many: a product has no single category to give its revenue to. The
climb fails — and with it, category falls *outside* the transaction universe.
Not "hard to reach." Outside.

This is the moment most stacks fumble silently: the join fans out, revenue
multiplies, and "revenue by category" comes back 44% bigger than total revenue
with nobody the wiser. Columna does something different: it declares the
boundary. Category lives in its own small universe (twelve rows — each
category's priority rank and allocation weight), and the product↔category
relationship is declared for what it is — a **frontier**, not a path.

## Crossing, when you mean to

Between universes there are exactly two kinds of passage, and both are
declared:

- **Shared grains.** Transactions and inventory both live on store and day —
  the same declared levels, presented twice. So revenue (from sales) and
  stock position (from snapshots) compose at store × month lawfully, with no
  ceremony: the identity of the grains is the license.
- **Faces.** Crossing the many-to-many frontier requires a declared face —
  each one named for what it does. Cascadia declares three: **touch** (revenue
  reaches every category a product sits in — deliberately multi-counted,
  1.44× the total, and the answer says so), **primary** (each product's
  top-priority category gets it — single-counted, 270 secondary memberships
  disclosed as unrepresented), **split** (a weighted spread that reconciles to
  the grand total to the cent — certified on the answer).

And if neither passage exists? The ask **refuses, and says why**. Ask this
demo for stock by customer and you'll get the honest answer: those live in
different universes, and no declared passage connects them.

## Why carve at all?

Because every silent double-count, every mystery join explosion, every
"primary category" chosen by a forgotten ETL rule is the same event: a
question crossing a boundary nobody declared. Universes make the boundaries
visible; declared passages make the crossings lawful; and everything else
refuses by name instead of guessing.

One warehouse. Three universes. Two kinds of passage. No third way through —
and that's the feature.

*See it drawn — live, from the running system — in [Figure 1 on the case
page](/case). Or run it: `pip install columna`, and ask for revenue by
category three lawful ways.*

*The theory, in full: [Multi-Universe Processing](https://doi.org/10.5281/zenodo.21543584) ·
[The Two Great Sources](https://doi.org/10.5281/zenodo.21553379).*
