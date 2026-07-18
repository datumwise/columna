# Cascadia Retail — the setup

*Chapter 1 of the case demo: the company, the data they have, and what they asked for.
Nothing here is about Columna yet — this is the situation any solution would face.*

---

## The company

Cascadia Retail runs 24 stores across four regions (north, south, east, west), selling
about 600 products to a customer base of roughly 2,000 registered accounts. A small data
team maintains a warehouse; a Sales Operations team lives in it.

## The data they have

The warehouse is ordinary — which is to say, it has history. Fourteen tables:

**The facts:**
- `transactions` — one row per sale line: customer, store, product, day, amount, units,
  units returned, a satisfaction score (often null), and the customer's region copied
  onto the row. ~20,000 rows over two years.
- `eom_inventory` — daily stock snapshots per store: store, day, level. ~17,000 rows.

**The reference tables:**
- `stores` (24 — with region and opened_date), `customers` (~2,000 — with segment,
  region, signup date), `products` (600 — with base price), `categories` (12), and
  `product_categories` — a bridge, because a product can sit in up to three categories.
- `calendar` — two years of days mapped to week, month, quarter, year.

**The rest — every warehouse has these:**
- Four pre-built summary tables (`daily_revenue_summary`, `monthly_avg_order_value`,
  `monthly_unique_visitors`, `monthly_store_inventory`) that someone made for a
  dashboard years ago. Convenient, and nobody is sure they're still right.
- Two side tables from other teams (`support_tickets`, `engagement_scores` — the
  latter covering only about half the customers).
- `warehouse_notes` — three rows of tribal knowledge, including: *"summary tables are
  convenience copies; the base tables are authoritative."*

The demo shows each table's schema and a few real rows before anything else happens —
if you don't know the data, nothing downstream can make sense.

## What Sales Ops asked for

Dana runs Sales Operations. Her team answers questions for regional managers all week,
by hand, in SQL and spreadsheets. Her request, lightly edited:

> "We want the team — and honestly, the managers themselves — to get answers from the
> AI assistant we already use, without waiting on us. But it has to be *right*, and it
> has to say what it's assuming. We've been burned."

**The questions her team answers every week** (this list is the requirement):

1. Revenue and order count — by store, by region, by month, by quarter.
2. Average order value, by month — and by store when a manager asks.
3. Best- and worst-performing products this month; top stores per region.
4. Return rate (units returned over units sold), by product and by month.
5. End-of-month inventory position, per store.
6. Unique customers who bought, by month and by region.

**The two times they got burned** (this is the trust bar):

- *The inventory total.* A deck went to the exec team with "total inventory by month" —
  daily snapshots summed across the month. The number was meaningless (thirty days of
  the same stock, added together), and nobody caught it until a warehouse manager
  laughed at it.
- *The two revenues.* Two decks in the same meeting showed different monthly revenue.
  One had used `daily_revenue_summary`; the other computed from `transactions`. They
  disagree — the summary is missing days — and it took an afternoon to find out which
  was right.

**Who has to be served** — and this matters as much as the questions:

Dana's team spans an analyst with eight years of context — she knows the summary
tables are stale, knows what `level` means, knows store S014 opened mid-year — and new
hires who know retail generally but none of this warehouse's folklore. Both must get
right answers: the veteran asking terse questions in her own shorthand, the new hire
asking vague ones without knowing what to ask. "If the right answer depends on knowing
our folklore," Dana says, "then the folklore has to live in the system, not in
Priya's head."

**Her constraints:**

- The assistant never gets raw table access. ("It will do what our interns did, faster.")
- Every answer states its basis — what was counted, over what population, with what
  caveats.
- If a question is ambiguous, it should come back as a question — not as a guess.
- If something can't be answered honestly, say so and say why.

## What "done" looks like

A regional manager types "how did the west do last quarter?" into the assistant and
gets a right answer with its assumptions attached. A new hire in week one gets the same
right answer the eight-year veteran gets — and when their question is too vague, the
assistant asks back instead of guessing. Dana's team stops being a query service. And the two failure modes above become *impossible* — not discouraged,
impossible: the meaningless inventory total can't be produced without a warning, and
the stale summary table isn't in the answering path at all.

*Next chapter: how the data team scoped and designed the Manifold to meet this — the
decisions, the naming, and what they deliberately left out.*
