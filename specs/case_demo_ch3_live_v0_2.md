# Cascadia Retail — live

*Chapter 3 of the case demo: the Manifold goes live. Every claim from chapter 2 gets
checked, the questions get asked, and Dana's "what done looks like" gets tested.
Everything shown here is real output from the running system — recorded, never
hand-edited.*

---

## First, the trials

A Manifold isn't accepted on the author's word. Every claim in the chapter-2 spec is
checked against the actual warehouse before anything serves:

| Claim | Verdict |
|---|---|
| `location`: store → region is functional (one region per store) | **corroborated** — 24/24 stores, one region each |
| `calendar`: day → month → quarter → year chains cleanly | **corroborated** — 731/731 days, every hop |
| `calendar`: day → week (the branch that can't chain) | **corroborated** |
| product ↔ category is many-to-many | **corroborated** — products found in 1–3 categories |
| ASSERT `returns_bounded`: units returned ≤ units sold | **corroborated** — holds on every tracked row |
| `transaction` BASIS events (absence = nothing happened) | **untestable** — the author's call, on the record |
| `inventory` BASIS spine (absence = a gap) | **untestable** — same |
| `inventory` carve: day ≥ store.opened | **corroborated** — no snapshot predates its store |

Two things to notice. The vocabulary is honest about what data can do: checked claims
are *corroborated* — the data supports them today; only mathematical facts earn
*verified*. And the basis claims are *untestable* — no data can prove what a missing
row means; that's a human's call, and the system records it as one instead of
pretending otherwise. And the verdicts aren't documentation — they're
load-bearing: if the data ever contradicts a claim, that claim stops serving until
someone fixes the data or the declaration.

## The questions, asked

**The veteran's way.** Priya types tersely, in the query language:

```
SELECT revenue, orders AT {region, cal.quarter}
```
→ **serve**: sixteen rows, four regions × four quarters. Every answer arrives as a
pair — the numbers, and the basis they stand on (population: transaction; paths:
location, calendar — both verified).

**The first burn, retried.** A new analyst — this is week two for him — asks for
"total inventory by month, per store":

```
SELECT stock.sum AT {store, cal.month}
```
→ **serve, with a caveat that can't be missed**: the per-month figures come back, and
with them: *stock summed across the blocked `calendar` lineage — per-bucket totals do
not reconcile along this axis; for month-end position, use `stock.last`.* The
meaningless exec-deck number now cannot be produced silently. He reads the caveat,
switches to `stock.last`, and gets the position Dana's question 5 actually wanted.
The burn didn't need a policy or a training. It needed a declaration.

**The ambiguous ask.** "What was the average monthly order value for the year?"

```
SELECT avg(aov) AT {cal.year}
```
→ **clarify**: averaged *from which grain*? The average of twelve monthly AOVs and
the pooled AOV over all transactions are different numbers. The system lists the
readings; the asker picks; the number is exact. A vague question came back as a
question — Dana's constraint, working.

**The question that comes back with its reason attached.** "Revenue by category,
please." → **clarify**: *product ↔ category is many-to-many (a product belongs to up
to 3 categories); this aggregate is underdetermined — the measure would be replicated
across matches and the total inflated.* And it offers the only honest readings: accept
the overlap deliberately ("revenue touching each category," multi-counted and saying
so) — or stay at product. Nobody gets a silently inflated number; anyone can get the
deliberate one. The someday question arrived, and the answer was ready years early.

**And the second burn?** Nothing to show — which is the point. The stale summary
tables aren't in the answering path at all; there is one `revenue`, it comes from the
authoritative binding on the map, and the two-decks meeting can't happen again.

## The Explorer

Everything above is browsable. The Explorer renders the Manifold spec — the logical
document, nothing physical — with every declaration wearing its verdict: the
universes with their basis and what absence means, the atlas with its two hierarchies,
each measure with its laws, each claim with its trial. Every fact carries the triad:
*defined as* (the declaration), *tested* (the verdict), *show me* (a query to copy).
A new hire's first hour lives here: it's the folklore, out of Priya's head, on a page.

## The MCP server

The assistant doesn't get table access — Dana's constraint. It gets an MCP server
over the Manifold, which exposes exactly three things:

- **`describe`** — the whole Manifold, machine-readable: every name, description,
  law, and verdict. The assistant reads this first; it's how it knows what `buyers`
  means and that `stock.sum` is blocked over time.
- **`query`** — FrameQL in, the four-mood answer out: result plus disclosure, always.
- **`explain`** — a dry run: what a query *would* do — its canonical form, the paths
  it takes, the verdicts it relies on, the mood it would return — touching no data.
  The assistant checks before it runs.

And the server carries **knowledge** — the operating instructions the assistant is
given: the grammar; the standing laws (*a clarify is the human's question, never the
assistant's guess — relay it; use the declared names — an answer that renames things
teaches folklore all over again*); and the pointer to `describe` as the source of
truth. The veteran's context, packaged and transferable.

## The assistant, in conversation

A regional manager (never wrote SQL in her life):

> **Manager:** How did the west do last quarter?
> **Assistant:** West region, Q2 2025: revenue $412,380 across 3,921 orders — average
> order value $105.17. *(Basis: transaction population; store→region and calendar
> paths, both verified. Computed from base data, not summaries.)*

The new hire, week one:

> **New hire:** How are we doing on returns?
> **Assistant:** Return rate is `units_returned / units_sold` — one definition,
> declared. Do you want it by month, by product, or both? (One note from the
> definition: rows before returns tracking began count as no return.)
> **New hire:** By month, this year.
> **Assistant:** *(serves the twelve rows, with the note attached.)*

The vague question came back as a question. The folklore came out of the system, not
out of anyone's head. The veteran and the week-one hire got the same right answers —
one typed FrameQL, one typed English, and neither needed to know which table is stale.

## What done looked like

Chapter 1 set the bar: right answers with their assumptions attached; ambiguity comes
back as a question; the impossible gets refused with reasons; the two burns become
impossible, not discouraged; a new hire gets what the veteran gets. Every clause of
that is above, in output — not promised, shown.

*The whole case — the warehouse, the map, the spec, and every transcript on this
page — ships in the demo. `pip install columna`, and rerun it yourself.*
