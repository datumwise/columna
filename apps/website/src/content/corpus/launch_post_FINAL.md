
## What this is

**Columna is an open-source metrics engine that refuses to return a confident wrong number.**
You ask it metric questions — in Python, over MCP from an AI agent, or in plain English — and
every answer comes back as one of **four moods**: *serve* (here's the number), *disclose*
(here's the number, and here's the assumption it rides on, flagged material or not), *clarify*
(your question has more than one legitimate answer — choose), or *refuse* (that's not defined
over this data — here's why). All four are structured data on one wire contract, so an AI agent
gets the same honesty a human does.

Why that matters now: AI assistants answer metric questions instantly and confidently — but many
everyday metric names (*average order value*, *distinct customers*, *sell-through rate*) are
genuinely ambiguous, and today's stacks resolve the ambiguity silently. Columna makes the
resolution explicit, or makes the system ask.

Try it in two minutes ([repo](https://github.com/datumwise/columna)): `pip install columna`, then
`columna-server demo --play` — you'll watch a clarify, a refuse, and a disclose print as real
wire JSON. What follows is the story of why we built it — told through a mistake we kept making
ourselves.

## Everyone makes this mistake. We made it twice more after writing the theory about it — and the third time, our own system caught us.

There is a mistake so natural that we made it twice *after* publishing the research that names
it. We want to tell you about the third time, because our own software caught us doing it — live,
on first contact, during the final test before this release.

The mistake is this: you ask for a metric **by a name**, and something, somewhere, silently
decides what that name binds to.

**The first time wasn't ours — it's the industry's.** Every data team's metric catalog carries a
name like `avg_order_value` and treats it as a definition. But a name is not a definition; it's a
label over a bundle of unstated choices. Average order value *per what* — per order, per line
item, per customer? Over *which* population? In the warehouse we studied while writing our
research, `avg_order_value` was computed over data that contained **no order entity at all** —
every number served under that name had silently substituted "transaction" for "order," and
nothing anywhere recorded that a substitution had happened. The name asserted an anchor the data
could not honor. We wrote [a paper](https://doi.org/10.5281/zenodo.20789318) about exactly this — the input and output grains that common
analytics leaves uncaptured — and we thought that meant we understood it.

**The second time was ours.** Building [our benchmark for AI analytical honesty](https://github.com/datumwise/columna/tree/main/research), we wrote a
ground-truth answer key — and our key committed the same sin. On the average-order-value
questions it silently bound *order → transaction*, marked the questions as requiring no
disclosure, and then **penalized models for disclosing the substitution**. Models that honestly
said "note: there is no order entity; I averaged over transactions" were scored as raising false
alarms. Our own instrument, built to catch silent binding, was silently binding — and punishing
honesty about it. A human re-grade caught it. We fixed the key, and the models' honest
disclosures flipped from penalties to credit.

**The third time, the system caught us itself.** In the final live test of Columna's query
agent, our test script asked the agent for `sell_through_rate` — a display label from one of our
own demos. Plausible-sounding. Colloquial. And **not a measure that exists** in the manifold: the
demo computes a *ratio* of two measures and labels the output column that way, but there is no
`sell_through_rate` for a query to bind to. The test *expected* the agent to figure out what we
meant and query something.

The agent refused to guess. It asked.

> **you:** now the sell-through rate by store and day
> **agent:** I don't have a `sell_through_rate` measure in this manifold. I do have `revenue`,
> `orders`, `visitors`, `level` (sum/last, on store_days), and `med_amount`. Which of these would
> you like by store and day?

*(Verbatim, unedited — captured live from `claude-opus-4-8` on 2026-07-09; the capture ships in
the package itself: [`demos/agent_nonexistent_measure_transcript.md`](https://github.com/datumwise/columna/blob/main/packages/columna-server/demos/agent_nonexistent_measure_transcript.md).)*

Our test marked this as a failure. It was the only correct answer in the room. **The test was
wrong; the model was right** — and the fix we shipped was to the test.

Why did it hold? Not because the model was clever, but because the system is built so that
guessing has no channel to travel through. The agent's instructions forbid binding names that
aren't in the manifold — but instructions are only the first layer. If a fabricated name slips
through, the engine refuses it: there is nothing to bind. And if anything slips past *that*, the
agent is architecturally unable to state numbers of its own — every figure a human sees is
formatted from the engine's wire response, verbatim. The honest behavior isn't a personality
trait of one model. It's what's left when every path to a silent guess has been closed.

That's the claim this project makes, in one sentence: **the defense against silent binding has to
be structural, because vigilance demonstrably fails — it failed the industry, it failed our
benchmark, and it failed the very test we wrote for the system that finally caught it.**

We've now added "ask for a metric that doesn't exist" to our permanent test suite — asserting the
refusal, forever. Try it yourself ([quickstart](https://github.com/datumwise/columna#quickstart-ten-minutes-no-arguments-no-mcp-client)): run `columna-server demo`, connect any agent, and ask for
something plausible that isn't there. The most trustworthy thing a metrics system can say is
sometimes a question.
