# The Grain Gap: Why Your AI Analyst Is Confidently Wrong

*Three people, three "correct" answers to one simple question — and the missing coordinate that's about
to become the AI-trust problem nobody is pricing in.*

---

You finally did the thing.

After two years of AI-strategy decks, you wired a genuinely capable LLM up to your warehouse and let
it answer questions in plain English. First real test. You type:

> *What was our average order value last quarter?*

1.2 seconds later: **$41.67.** Clean. Formatted. A little chart, even. A cited source table.

Ship it, right?

Here's the thing. $41.67 is a right answer. So is **$83.33**. So is **$125.00**. Your AI picked one of
the three, served it with the serene confidence of a machine that has never once doubted itself, and
mentioned none of the others. Nobody in the loop knows a choice was made.

That's not a hallucination. The SQL is valid. The number is real. The lineage checks out. It's
something quieter and, for anyone trying to trust AI on their data, *worse*: **a defensible wrong
answer.** The kind no guardrail catches, because by every check you've built, it's correct.

Let me show you where the other two answers come from. Ninety seconds, and you'll never un-see it.

## The ninety-second version

Here's a quarter of sales. The whole thing:

| order | customer | line items (each a sale) |
|---|---|---|
| O1 | Ada | $100, $20 |
| O2 | Ada | $10 |
| O3 | Ben | $40, $40, $40 |

Revenue is $250. Now, *average order value.* Watch:

- Divide by the **6 line items** → $250 / 6 = **$41.67**
- Divide by the **3 orders** → $250 / 3 = **$83.33**
- Divide by the **2 customers** → $250 / 2 = **$125.00**

Same data. Same three words. Three answers, none of them wrong. They differ only in *what you divided
by* — and "what you divided by" is a decision that the question never stated, the column name never
records, and your AI made silently on your behalf.

That decision has a name. It's the **input anchor** — the grain a measure is computed *over*. And it's
the single most under-recorded fact in your entire data stack.

And here's why it suddenly matters more than it ever has. When the person dividing by the wrong thing
was a *human*, you usually found out — eventually. Three analysts with three numbers is an argument,
and an argument is *visible*; somebody finally says "wait, are you doing this per customer?" and the
bug dies in the meeting. An AI doesn't argue. It picks one, moves on, and sounds terrific doing it. The
disagreement that used to save you never happens. (Hold that thought — it's the whole game, and we'll
come back to it.) First, the mechanics, because once you see them you can't trust a bare number again.

## A measure has two grains. You only ever name one.

You already think about grain — just half of it. You ask for revenue **by region**, sales **by
month**. That's the *output anchor*: the grain of the answer. It's the one everybody states.

The other grain is the one nobody states: the grain you compute *over*. Average order value reported
for the quarter still has to be averaged over *something* — lines, orders, customers. The output
anchor is the grain you asked for. The input anchor is the grain you forgot existed.

And for a long time, you got away with forgetting it. Here's why.

## SUM lulled you into a false sense of security

Try the same trick on **total revenue.** Sum the lines, sum the orders, sum the customers — you get
$250 every single time. The input anchor doesn't matter, because addition doesn't care what order you
add things in.

That's it. That's the whole reason a generation of dashboards treated every metric as if it lived at
one grain: we built our intuitions on `SUM`, and `SUM` is the one operator where the input anchor
genuinely doesn't matter. It was never a law of data. It was a **happy accident of addition** — and
the moment you reach for an average, a rate, a ratio, a percentage, an index, the accident runs out
and the input anchor wakes up and starts changing your numbers.

## The trap that gets the veterans: MIN and MAX

Here's the one that should make you sit up, because it catches people who *know* all of the above.

The seasoned instinct is: *averages and ratios are spicy, but additive stuff is safe.* So you trust
`MIN` and `MAX`. They re-aggregate perfectly — the minimum of the minimums is the overall minimum —
and they pass every "is this safe to roll up?" test in the book.

And they're still ambiguous. "Lowest inventory last month" — lowest *what?* The lowest single
store-day reading? The lowest day across the whole chain? Wildly different numbers, identical column
name, zero warning. `MIN` and `MAX` sail through the additivity check **and** are meaningless without
their input grain. Re-aggregable is not the same as interpretable — and that gap is exactly where a
confident AI will plant a flag and march off in the wrong direction.

## Here's the tell: you've been duct-taping this for years

The most quietly damning part? Your industry already *discovered* the input anchor. It just keeps
fixing it in the worst possible place — the metric's name.

**ARPU** vs **ARPPU.** Average revenue per *user* vs per *paying user*. Two acronyms that exist for
one reason: the denominator — the input anchor — was different, two teams computed two numbers, and
somebody got tired of the argument. **Gross** vs **net.** **DAU** vs **MAU.** **Blended** vs **paid**
CAC. Every one of these is a little scar tissue from a grain fight, healed over by forking the name.

It's the field shouting that the input anchor is real and load-bearing — and then writing it down in a
*string*. A name like `avg_order_value` will happily claim its input anchor is "order" over a table
that contains no orders at all. The name carries what someone *meant*; the data carries what actually
*happened*; and nothing on Earth checks that they match.

## So: is *your* metric a landmine? The cheat-sheet.

Most metrics are fine. You can tell at a glance which ones aren't:

| If your metric is… | Examples | Safe as one bare number? |
|---|---|---|
| **Additive** (sums, and things that sum) | total revenue, units sold, headcount | ✓ **Yes** — same answer however you slice it |
| **An average, rate, ratio, %, or index** | AOV, conversion rate, ARPU, gross margin | ✗ **No** — record what it's computed *over* |
| **A distinct count** | unique visitors, active accounts | ✗ **No** — "distinct per *what* window?" |
| **A min, max, or plain count** | lowest balance, peak load, # of transactions | ✗ **No** — looks safe, isn't |

Three of the four rows are minefields. The bottom row is the one that gets the experts. Pin those
first.

## Why this just became urgent (and not academic)

For twenty years, the grain gap was survivable, because the people hitting it were *people.* Three
analysts in a room arguing about which AOV is "right" looks like dysfunction — but it's actually a
safety mechanism. The disagreement is *visible.* Somebody eventually says "wait, are you doing this
per customer?" and the bug gets caught in the meeting.

Now point an LLM at the same warehouse. The argument vanishes. You get **one** number, instantly,
fluently, with a chart and a citation and not a flicker of doubt. The safety mechanism — the visible
disagreement — is exactly what the AI removes. It collapses three answers into one and hands it to you
with a confidence the question never earned.

This is the real shape of the "can we trust AI on our data?" crisis, and it's almost never named
correctly. Everyone's braced for *hallucinations* — the AI inventing a number. The grain gap is
sneakier: the AI computes a **real** number, **correctly**, from a **valid** query, and it's still
the wrong answer to the question you asked, because it silently bound a grain you never specified. No
hallucination detector will ever flag it. It's not lying. It's guessing — and not telling you.

You can't fix a guessing problem by making the model bigger or the prompt cleverer. A perfectly
accurate reader of an under-specified question still has to pick. The fix has to live one layer down —
in the **semantic layer**, where the metric is defined — and it has exactly three jobs:

1. **Capture the anchors as structure, not prose.** Make the input anchor a *field* the metric carries,
   not a hint smuggled into its name. Then "customer" means one thing to Finance, to the dashboard,
   and to the AI — the same thing, checkably.

   ```yaml
   metric: avg_order_value
   output_anchor: [region, quarter]   # the grain it's reported at
   input_anchor:  order               # the grain it's averaged OVER  ← the one nobody records
   reducer:       avg
   ```

2. **Make ambiguity loud again.** When a question genuinely doesn't pin the grain, the right move
   isn't to silently pick one — it's to *surface the choice*, the way the analyst in the meeting did.
   That's your human-in-the-loop moment, and it's only possible if the layer knows the anchor was
   undetermined in the first place.

3. **Carry the anchor through every hop.** The input anchor is provenance. If it's preserved from
   source to metric to model, your lineage actually means something; if it's dropped at the first
   transformation, you're tracing the plumbing while the water's already mixed.

Do that, and the AI stops guessing — not because it got smarter, but because the question finally
arrives fully specified. *That's* an audit-ready semantic layer: not one that logs what the AI did,
but one where the AI couldn't have quietly done the wrong thing in the first place.

## The bottom line

A metric you can actually trust isn't a name and a number. It's a **family** (revenue, balance,
satisfaction), an **output anchor** (the grain you report at), an **input anchor** (the grain you
compute over), and a **reducer** (how you collapse it). The industry records the first two by habit,
the last in a function call, and the input anchor — the one that's about to embarrass your AI in front
of the whole company — almost nowhere, except hidden inside acronyms like ARPPU.

The disagreements were never about who did the math wrong. Everybody did the math right. They were
about a grain nobody wrote down. In the dashboard era, that cost you a tense meeting. In the AI era,
it costs you trust — and trust is the only currency that makes "AI on your data" worth anything at
all.

---

*The formal version of this idea — the exact criterion for when the input anchor "wakes up," why the
average and the weighted average hide it for different reasons, and why MIN/MAX are the sleeper trap —
is published as* **The Two Anchors of a Measure** *(Wang, 2026; DOI: 10.5281/zenodo.20789318),
companion to* The Silent Failure Atlas. *The structured, checkable capture of these grains — so your
people and your models finally mean the same thing — is the problem* **datumwise** *is built to solve.*
