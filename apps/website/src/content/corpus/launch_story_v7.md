# The story behind Columna

## What this is

**Columna is an open-source data framework — a data model, a query language, and an engine — built so that no layer of it can return a confident wrong number.**

The data model (the **Manifold**) holds what your data *means*, checked against the data itself.
The query language (**FrameQL**) can only ask for meaning the model declares.
The engine serves nothing the model can't defend.

You ask it metric questions — in Python, over MCP from an AI agent, or in plain English — and every answer comes back as one of **four moods**:

*   **Serve** — here’s the number
*   **Disclose** — here’s the number, plus the material assumptions it rides on
*   **Clarify** — your question has more than one legitimate answer — choose
*   **Refuse** — that metric is not defined over this data — here’s why

All four travel on one wire contract, so an AI agent gets the same honesty a careful human does.

Why this matters now: AI assistants answer metric questions instantly and confidently — but everyday names like *average order value*, *distinct customers*, or *sell-through rate* are often genuinely ambiguous. Today’s stacks resolve that ambiguity silently. Columna makes the resolution explicit, or makes the system ask.

**Try it in two minutes**
```bash
pip install columna
columna-server demo --play
```
You’ll watch a real clarify, refuse, disclose, and serve print as wire JSON — over the complete Cascadia Retail case. Every number on this site is a recording from the shipped package.

What follows is the story of why we built it — told through a mistake we kept making ourselves.

---

## Everyone makes this mistake. We made it twice more after writing the theory about it — and the third time, our own system caught us.

There is a mistake so natural that we made it twice *after* publishing the research that names it. We want to tell you about the third time, because our own software caught us doing it — live, on first contact, during the final test before this release.

The mistake is this: you ask for a metric **by a name**, and something, somewhere, silently decides what that name binds to.

### 1. The industry’s version

Every data team’s metric catalog carries names like `avg_order_value` and treats them as definitions. But a name is not a definition — it’s a label over a bundle of unstated choices. Average order value *per what*? Per order, per line item, or per customer? Over *which* population?

The canonical version of the mistake: an `avg_order_value` computed over a warehouse that contains **no order entity at all** — every number served under that name has silently substituted ‘transaction’ for ‘order,’ and nothing records the substitution. The name asserts an anchor the data cannot honor. We wrote a paper about exactly this — the input and output grains that common analytics leaves uncaptured — and we thought that meant we understood it.

### 2. Our own benchmark

While building our benchmark for AI analytical honesty, we wrote a ground-truth answer key that committed the same sin. On the average-order-value questions it silently bound *order → transaction*, marked the questions as requiring no disclosure, and then **penalized models for disclosing the substitution**. Models that honestly said “note: there is no order entity; I averaged over transactions” were scored as raising false alarms. 

Our own instrument, built to catch silent binding, was silently binding — and punishing honesty about it. **We caught it when we measured our own grader.** The tidy fix would have been to quietly rewrite the key; we didn't. **The frozen key ships unaltered, sin and all**, and we re-scored under the corrected reading and published both scoreboards — under which the models' honest disclosures flip from penalties to credit. The artifact (`aov_corrected_scores.json`) ships in the public benchmark kit.

### 3. The system caught us

In a live test of Columna’s query agent (July 9th), our test script asked for `sell_through_rate` — a display label from one of our own demos. Plausible. Colloquial. And **not a measure that existed** in the manifold: the demo computed a *ratio* of two measures and labeled the output column that way, but there was no `sell_through_rate` for a query to bind to.

The test *expected* the agent to figure out what we meant and query something.

The agent refused to guess. It asked:

> **you:** now the sell-through rate by store and day  
> **agent:** I don’t have a `sell_through_rate` measure in this manifold. I do have `revenue`, `orders`, `visitors`, `level` (sum/last, on store_days), and `med_amount`. Which of these would you like by store and day?

*(Verbatim, unedited — captured live from `claude-opus-4-8` on 2026-07-09, against the demo as it then stood — it has since been rebuilt as the Cascadia case. The capture ships in the repo: [`demos/agent_nonexistent_measure_transcript.md`](https://github.com/datumwise/columna/blob/main/packages/columna-server/demos/agent_nonexistent_measure_transcript.md))*

Our test marked this as a failure. It was the only correct answer in the room. **The test was wrong; the model was right.** We fixed the test.

Why did it hold? Not because the model was clever, but because the system is built so that guessing has no channel to travel through. Instructions forbid binding names that aren’t in the manifold. If a fabricated name slips through, the engine refuses it. And every number a human sees is formatted from the engine’s wire response, verbatim. The honest behavior isn’t a personality trait of one model — it’s what’s left when every path to a silent guess has been closed.

**That’s the claim this project makes:** the defense against silent binding has to be structural, because vigilance demonstrably fails. It failed the industry. It failed our benchmark. And it failed the very test we wrote for the system that finally caught it.

We’ve since added “ask for a metric that doesn’t exist” to our permanent test suite — asserting the refusal, forever.

---

## Then we published the stumbles

After that catch we rebuilt the demo as a complete case — [Cascadia Retail](/case): a realistic warehouse with realistic sins, the design decisions and their reasons, and the Manifold serving it.

We recorded our assistant answering a manager and a week-one new hire. It took **four takes — plus one honest re-roll after a defective attempt — every one preserved in the repo**. Take 1 surfaced two gaps in the agent’s instructions; take 2 confirmed one fix and surfaced a real expressiveness gap in our query language (it’s on the public ledger as the leading next increment); take 3 showed the laws working and a limit that’s architectural; take 4 ships — including a turn where the grounding guard suppressed a perfectly good clarifying question rather than risk an ungrounded reply, and a turn where the agent fetched a definition and forgot to relay it.

A law is a bias on a rented mind, not a guarantee — which is exactly why every claim in this system is checked rather than trusted, minds included. The transcripts on our site are those recordings, warts bolded.

The case now demonstrates something a compile-to-SQL semantic layer structurally can’t promise: a **lawful many-to-many crossing**. Cascadia’s products sit in up to three categories, so “revenue by category” has no innocent answer. Ask for it bare and the system returns a **menu of declared crossings**. Ask for `revenue AT {category.touch}` and it serves the deliberate over-count with the skew stated *on the answer itself*: touch total **1.44×** the grand total — which is exactly the bridge's 870 memberships over 600 products. The over-count *is* the fan-out, and the answer says so.

The industry’s most universal double-counting wound, turned into a labeled, lawful, refusable operation.

---

**Try it yourself** ([quickstart](https://github.com/datumwise/columna#quickstart-ten-minutes-no-source-checkout))  
Run `columna-server demo`, connect any agent, and ask for something plausible that isn’t there. Or read the case first and ask it Dana’s questions.

The most trustworthy thing a metrics system can say is sometimes a question.

*Columna 0.11.1 · [the case](/case) · [what is Columna?](/what-is-columna) · [the manuals](/docs/framework) · [why it looks this way](/why-columna-looks-this-way)*
