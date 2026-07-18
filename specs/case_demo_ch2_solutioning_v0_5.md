# Cascadia Retail — the solutioning

*Chapter 2 of the case demo: how the data team went from Dana's request to a Manifold
design. The decisions, the reasons, and what was deliberately left out.*

---

## Working backward from the questions

The team started from Dana's six questions and asked, for each: what data answers it,
at what grain, along what paths? That trace decided almost everything:

| Dana's question | What it needs |
|---|---|
| 1. Revenue & orders by store/region/month/quarter | transaction facts; store, region, and calendar grains; a path from store to region and from day to the calendar |
| 2. Average order value | revenue ÷ orders — a defined ratio, one definition for everyone |
| 3. Best/worst products; top stores per region | the product grain; ordered, top-n answers |
| 4. Return rate by product and month | units sold and units returned, summed; their ratio |
| 5. End-of-month inventory position per store | the stock snapshots — *position*, not totals |
| 6. Unique customers who bought | a distinct count of customers, by month and region |

Two tables answer all six: `transactions` and `eom_inventory`. Everything else is
either a reference table serving the grains and paths, or out of scope.

## What we verified before designing

A design is only as good as what you actually know about the data. The team checked;
each finding became a decision:

- **`eom_inventory` is misnamed — the data says daily.** The name says end-of-month;
  the rows are one snapshot per store per *day* (~17,000 rows over two years). Almost
  certainly a fossil from when the feed was monthly. Decision: **grain comes from the
  data, never from the name** — the model treats it as the daily snapshot table it is.
- **`transactions` is a daily fact, and that's fine.** Day grain, no timestamps — a
  daily rollup of an upstream transaction log the warehouse doesn't keep. A fact table
  summarizing a log is normal; the model just has to be honest that *day* is the finest
  time grain anyone can ask at.
- **The two facts have different grains.** A transaction row is one sale line
  (customer × store × product × day); an inventory row is one snapshot (store × day).
  Different populations → they will be modeled as **two separate populations**, never
  silently mixed.
- **The snapshots are a running level, not a flow.** Summing them across days produces
  Dana's meaningless number. Decision: summing stock **across time will be blocked by
  declaration** — the first burn becomes impossible, not discouraged.
- **The summary tables are stale.** `daily_revenue_summary` has 716 rows against 731
  calendar days — fifteen days missing. That's the second burn, explained. Decision:
  **summary tables are not sources.** The base tables are authoritative (the
  warehouse's own notes agree). They stay in the warehouse; they don't enter the model.
- **Weeks don't nest in months.** The team checked the calendar: ISO weeks straddle
  month boundaries. So the calendar rollup chain is day → month → quarter → year, and
  **week hangs as its own path off day** — it can't sit in the chain.
- **A product can be in up to three categories.** Any revenue-by-category rollup would
  triple-count. No question asks for it — but someone will. Decision: declare the
  relationship as **explicitly many-to-many**, so when the question comes, the refusal
  can name exactly why.
- **`transactions.customer_region` is a denormalized copy.** "By region" in Dana's
  questions means *store* geography (managers own stores). Decision: **one region
  concept**, reached from store via the store table; the copied column is ignored.
- **`units_returned` is null on early rows** — returns tracking started partway
  through the history. Decision: nulls count as no-return, and the return-rate
  definition **says so in its description** (folklore into the system).
- **Stores opened on different dates** — S014 mid-year. Snapshot rows before a store
  existed would poison averages. Decision: the inventory population is **carved by
  `day >= opened_date`** — Priya's knowledge, now a declared predicate.

## The design

**Two populations (universes):**

```
UNIVERSE transaction = customer * store * product * day   BASIS events
UNIVERSE inventory   = store * day
    WHERE day >= store.opened                       BASIS spine
```

Universe names are **singular concepts** — a universe names what its population is
*about*, never describes the records or the grid. (Notice the quiet split: the physical
table is `transactions`, plural; the universe is `transaction`, singular. And the
inventory universe isn't named for its store×day grid — the grid is its *shape*, not
its meaning.) The universe definition — products × predicate × basis — is the **scope
contract**: the Manifold binds to this declared population, and stays stable no matter
what else the warehouse grows.

`events` says: a missing combination means *nothing happened* — an honest zero.
`spine` says: this is a grid that should be complete — a missing row is a *gap*, and
answers over gaps must say so.

**The atlas** — the grains and the paths between them:

```
LEVEL customer, store, product, day        (base grains)
LEVEL region, category
LEVEL cal.week, cal.month, cal.quarter, cal.year

HIERARCHY location {
    store -> region
}
HIERARCHY calendar {
    day -> cal.month -> cal.quarter -> cal.year
    day -> cal.week
}
RELATE product <-> category                ("up to 3 categories per product")
```

One declaration form for all functional paths: a **hierarchy** is a named family of
them — a single hop (location), a chain, or a small branching structure (calendar
needs the branch, because weeks don't nest in months). Every declared path is a claim,
tested against the actual tables. Lineage names name *meanings* — `location`,
`calendar` — and a bar like `BLOCKED { calendar }` bars the whole lineage, week branch
included.

**The measures** — named in the team's own vocabulary, each with a one-line
description (Dana's folklore rule: if a new hire can't understand the name from its
description, the name isn't done). Note what you *don't* see below: table names,
column names. **The Manifold spec is purely logical** — it's the document everyone
reads, so nothing physical crosses into it. How each name attaches to the warehouse
lives in a separate document: the physical→logical map.

*The Manifold spec (what everyone sees):*

```
MEASURE revenue         ON transaction    -- "sale amount, summed"
MEASURE orders          ON transaction    -- "count of sale lines"
MEASURE buyers          ON transaction    -- "distinct customers who bought"
MEASURE units_sold      ON transaction    -- "units sold"
MEASURE units_returned  ON transaction
    -- "units returned; nulls predate returns tracking and count as no return"

MEASURE stock ON inventory               -- "the stock level snapshot"
    FAMILY {
        sum   BLOCKED { calendar }   -- "stock summed across time doesn't reconcile"
        last  ORDER day              -- "position = the latest snapshot"
    }

DERIVED aov         = revenue / orders
DERIVED return_rate = units_returned / units_sold

ASSERT returns_bounded ON transaction: units_returned <= units_sold
    -- the team's data contract, checked against the data, not hoped
```

*The physical→logical map (the data team's document) — and notice its shape:
**many to one.** A warehouse accumulates multiple physical incarnations of each
concept — copies, denormalizations, summaries — and the map's job is to resolve each
many down to one authoritative binding, with the rejects kept **on the map, with
reasons**. (Dana's second burn was exactly an unresolved many-to-one: two incarnations
of revenue, no declared winner.)*

```
logical            binds to                     other incarnations (rejected, why)
─────────────────  ───────────────────────────  ────────────────────────────────────
transaction        transactions
inventory          eom_inventory                 (name is a fossil — grain is daily)
revenue            sum(amount)                   daily_revenue_summary.revenue (stale)
orders             count(*)                      monthly_avg_order_value.n_txns (stale)
buyers             distinct(customer_id)         monthly_unique_visitors (stale)
units_sold         sum(units)
units_returned     sum(units_returned)
stock              level                         monthly_store_inventory (stale rollup)
region             stores.region                 transactions.customer_region (copy);
                                                 customers.region (customer's, not store's)
store.opened       stores.opened_date
calendar paths     calendar(day, ...)            location path: stores(store_id, region)
```

So the solutioning produces **two artifacts**: the physical→logical map (many to one —
the survey of the territory, rejects and all) and the Manifold spec (purely logical —
the output everyone reads). The wall between them is the same wall the running system
keeps: agents and readers see meaning; only the map — and the engine — know the
plumbing.

Three renames from the physical layer, each with a reason: `buyers` (not "visitors" —
these are customers who bought, and that's what Dana's question 6 says); `units_sold`
(the column is just `units`; the measure says what it means); and **`stock`** for the
inventory measure (the source column is called `level`, which collides with the word
for grains — a new hire reading "level by month" learns nothing; "stock by month" is
self-explaining).

## What we left out, and why

Scoping is mostly saying no, with reasons a reader can check:

- **The four summary tables** — never sources. They're stale, the base tables answer
  everything, and their only honest purpose — query speed — is the engine's cache's
  job, not a table's.
- **`satisfaction`** — real data, no question asks for it. Available when one does.
- **Customer segment, customer-region analysis** — same: in the warehouse, not in the
  questions.
- **`engagement_scores`** — covers only ~half the customers; any customer-level answer
  from it would be quietly wrong for the other half. Until coverage is understood,
  it's out — and that reason is recorded, not just the decision.
- **`support_tickets`** — another team's domain; Sales Ops didn't ask.
- **Revenue by category** — deliberately *not* offered: the many-to-many makes an
  honest single-count impossible, and the declared relationship exists so the refusal
  can say exactly that.

*Next chapter: the Manifold goes live — every claim above gets checked against the
actual data and comes back with a verdict, and then the questions get asked.*
