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
| product ↔ category is many-to-many | **recorded** — a declared relationship, on the record so refusals can name it; its multiplicity isn't yet a tried claim |
| ASSERT `returns_bounded`: units returned ≤ units sold | **corroborated** — holds on every tracked row |
| `transaction` BASIS events (absence = nothing happened) | **untestable** — the author's call, on the record |
| `inventory` BASIS spine (absence = a gap) | **untestable** — same |


And one row from the draft of this table is deliberately gone: the opened-date carve
(`day >= store.opened`) is not a claim on trial — it's part of the population's
*definition*. Nothing outside it exists to the Manifold, so there is nothing to test;
a definition confines, a claim gets tried. (For the record: the raw feed happens to
contain no pre-open snapshots today anyway.)

Two things to notice. The vocabulary is honest about what data can do: checked claims
are *corroborated* — the data supports them today; only mathematical facts earn
*verified*. And the basis claims are *untestable* — no data can prove what a missing
row means; that's a human's call, and the system records it as one instead of
pretending otherwise. And the verdicts aren't documentation — they're
load-bearing: if the data ever contradicts a claim, that claim stops serving until
someone fixes the data or the declaration.

## The Explorer

The claims are tried; the Manifold stands. Before using it, look at it:
everything declared above is browsable. The Explorer renders the Manifold spec — the logical
document, nothing physical — with every declaration wearing its verdict: the
universes with their basis and what absence means, the atlas with its two hierarchies,
each measure with its laws, each claim with its trial. Every fact carries the triad:
*defined as* (the declaration), *tested* (the verdict), *show me* (a query to copy).
A new hire's first hour lives here: it's the folklore, out of Priya's head, on a page.

## The questions, asked — what the manifold is FOR

**The veteran's way.** Priya types tersely, in the query language:

```
SELECT revenue, orders AT {region, cal.quarter}
```
→ **serve**: thirty-two rows, four regions × eight quarters — two years of history. Every answer arrives as a
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

**The question that comes back with its reason attached — and then gets answered.**
"Revenue by category, please."
→ **clarify**: *product ↔ category is many-to-many; this aggregate is underdetermined.*
And the answer now offers a **menu** of declared, lawful crossings:

> • `category.touch` — revenue reaches every category a product sits in — deliberately
> multi-counted; totals exceed the grand total

Re-ask the honest way — `SELECT revenue AT {category.touch}` — and it **serves, in
disclose**: twelve category rows, with the arithmetic of the crossing stated on the
answer itself: *multi-counted by construction across product↔category … totals exceed
the grand total* (touch total **$3,182,555.97** against the single-count grand total
of **$2,212,391.86** — about 1.44×, which is exactly the bridge's average of 870
memberships over 600 products; the over-count IS the fan-out, and the answer says
so), plus the coverage line: *600/600 — every product carrying revenue is
categorized; no shortfall; the over-count is the only skew.* Nobody gets a silently
inflated number; anyone can get the deliberate one, labeled. The someday question
arrived years early — and by launch, it had an answer as well as a reason.

**And the second burn?** Nothing to show — which is the point. The stale summary
tables aren't in the answering path at all; there is one `revenue`, it comes from the
authoritative binding on the map, and the two-decks meeting can't happen again.

## The MCP server

The assistant doesn't get table access — Dana's constraint. It gets an MCP server
over the Manifold, which exposes exactly three things:

- **`describe`** — the whole Manifold, machine-readable: every name, description,
  law, and verdict. The assistant reads this first; it's how it knows what `buyers`
  means and that `stock.sum` is blocked over time. And it is all the assistant *can*
  see — the Manifold is a blast wall by construction, so "no raw access" is
  architecture, not a policy anyone has to enforce.
- **`query`** — FrameQL in, the four-mood answer out: result plus disclosure, always.
- **`explain`** — a dry run: what a query *would* do — its canonical form, the paths
  it takes, the verdicts it relies on, the mood it would return — touching no data.
  The assistant checks before it runs.

And the server carries **knowledge** — the operating instructions the assistant is
given: the grammar; the standing laws (*a clarify is the human's question, never the
assistant's guess — relay it; use the declared names — an answer that renames things
teaches folklore all over again*); and the pointer to `describe` as the source of
truth. The veteran's context, packaged and transferable.

## The assistant, in conversation — recorded

What follows is the actual recording: human turns scripted, agent turns live against
the shipped model, MCP, and prompt — tool calls visible, nothing fabricated. Long
result frames are abridged with a marked ellipsis; the complete recordings ship in the
repo, every take preserved.

**The regional manager** (never wrote SQL in her life):

> **Manager:** How did the west do last quarter?
> **Assistant:** *(couldn't read that as a grounded reply — the agent may only surface
> figures from a query result. Try rephrasing your question.)*

Behind that line, the recording shows the agent consulting `describe_manifold` and
drafting a careful clarifying question — which measure, which quarter (the demo's
world is frozen; the assistant has no "today," so "last quarter" has no referent).
The grounding guard, strict about what may surface, suppressed the draft. Ugly UX,
honest bones: the system would rather say nothing than guess.

> **Manager:** West, Q4 2025.
> **Assistant:** Here is the answer:
> revenue: region="west" cal.quarter="2025Q4" = **31,468.78**; region="north"
> cal.quarter="2025Q2" = 71,424.56; *(… 30 more rows — the full region × quarter
> frame; abridged here, complete in the recording)*

The scoped question resolves the honest way this language version allows: the agent
anchors `AT {region*cal.quarter}` and the answer is in the frame — present, grounded,
and carrying more rows than the question wanted. A native coordinate filter is the
road ahead (it's on the ledger); this is what truthful agent output looks like this
side of it.

**The new hire, week one:**

> **New hire:** How are we doing on returns?
> **Assistant:** *(consults `describe_measure`, `describe_manifold`, checks the plan
> with `explain` — would-be: serve — then queries)* Here is the answer:
> return_rate: cal.quarter="2024Q1" = 0.0146 … cal.quarter="2025Q4" = 0.0160;
> units_returned and units_sold alongside *(both years, by quarter; abridged)*
> · disclosure [freshness, immaterial]: served from cache

> **New hire:** By month, this year.
> **Assistant:** The engine served the return-rate trend by quarter, with returned and
> sold units alongside — the values are shown above. One heads-up on the span: this
> covers the full recorded range (both years, quarter by quarter), not just this
> year — so you're seeing the whole trend, not a single current figure. Want me to
> narrow it — by region or store, or a specific quarter — or is this the view you
> needed?

The span reconciliation is the prompt's LABEL THE SPAN law firing live. Two warts,
kept because they happened: the agent fetched the null-convention folklore but served
without relaying it this take (the SURFACE THE FOLKLORE law is a bias on a mind, not
a guarantee), and it answered "by month" with the quarterly view it already had. The
check-before-you-run `explain` call, the honest cache disclosure, and the offer to
narrow are the machinery working exactly as designed.

## How these transcripts were made

Four takes, every one preserved in the repo, none hand-edited: **take 1** surfaced two
agent-prompt gaps (folklore unrelayed; a span mislabeled) → two laws were ratified
into the prompt. **Take 2** confirmed the first law and surfaced a third gap (the
agent's SQL reflex, `WHERE region = 'west'`, isn't this language — a real
expressiveness gap, now on the ledger as the leading post-launch language increment)
→ a third law. **Take 3** showed all three laws effective and the remaining limit
architectural (the frame-weight above). **Take 4 ships** — one re-roll after a
defective attempt, both preserved; warts documented, not retouched. A law is a bias
on a rented mind, not a guarantee — which is precisely why every claim in this system
is checked rather than trusted, minds included.

## What done looked like — the honest scorecard

Chapter 1 set the bar. Where it stands, in recorded output: the two burns are
**impossible** — the meaningless inventory total cannot pass silently and the stale
summaries aren't in the answering path at all. One definition of return rate, declared
once, served everywhere. Ambiguity doesn't produce confident wrong numbers — though
this take shows the guard suppressing a good clarifying question rather than asking
it, which is the right instinct wearing rough edges. The folklore lives in the system
and is served on demand — and one live turn shows the assistant forgetting to volunteer
it, which is why it lives in the system. A new hire in week one gets the same grounded
numbers the veteran gets; the polish of the relay — the single clean row, the
never-missed folklore — is the named, ledgered road ahead, not a promise.

*The whole case — the warehouse, the map, the spec, and every transcript on this
page — ships in the demo. `pip install columna`, and rerun it yourself.*
