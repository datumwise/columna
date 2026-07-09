# The Columna query agent — the wedge in natural language

`columna-server agent` is Columna's own natural-language front door, and it is **a true MCP client**:
it spawns `columna-server` over stdio and speaks the protocol — it never touches the engine
in-process. Natural language becomes a *proposed* Frame-QL query; the planner disposes; the four
moods drive the conversation. The model proposes, the layer checks, the human decides.

Run it against the packaged demo (needs `ANTHROPIC_API_KEY` and the agent extra —
`pip install -e "packages/columna-server[agent]"`):

```bash
columna-server agent            # packaged demo Manifold, no path args
```

Below is a real conversation (the transcript the hermetic tests assert against, value rows elided).
It walks through **all four moods** — serve → clarify → refuse → disclose — in one human exchange.
Every number shown comes verbatim from the server's wire JSON; the agent never computes or restates
a figure, so it can never state a wrong one.

---

**you:** what's revenue by region?

**agent** *(serve)*:
> Here is the answer:
> revenue: region="south"=771240.4099999999; region="north"=601075.3299999996; region="east"=615704.5300000003; region="west"=224371.58999999994

The agent proposed `QUERY: revenue @ region`; the server served it; the agent presents the values
exactly as the wire returned them.

---

**you:** what's the sell-through rate by store and day?

**agent** *(clarify — relayed to you, never auto-picked)*:
> That question is ambiguous: ratio combines measures over different populations ['store_days',
> 'transactions'] … which population should the rate be taken over?
> Please choose:
>   [1] express both numerator and denominator within universe 'store_days'
>   [2] express both numerator and denominator within universe 'transactions'
> Reply with the number of your choice.

`revenue / level.last` spans two populations, so the rate has no single value. The server clarifies;
the agent relays the alternatives and **waits for your choice**. It does not guess a population.

---

**you:** 1

**agent** *(refuse — explained honestly)*:
> That can't be answered: revenue is bound to universe 'transactions', not the pinned population
> 'store_days' — it is not defined over that population

Your choice is applied mechanically (the alternative's `apply` universe). Pinning `store_days` makes
the numerator out-of-domain, so there is no faithful rate over that population — the server refuses,
with the reason, and the agent invents nothing.

---

**you:** then just show revenue and inventory side by side by store and day

**agent** *(disclose — served, with a material caveat)*:
> Answer (with caveats):
> rev: store="S001" day="2024-01-05"=218.18; … (rows elided)
> inv: store="S001" day="2024-01-03"=5622.0; … (rows elided)
> · disclosure [denominator_population, material]: frame spans multiple universes ['store_days',
>   'transactions'] — population is ambiguous; pin it with ON UNIVERSE

Reformulated as two separate columns over the union population, the numbers are served **with** a
material coverage caveat riding on the frame — surfaced in the reply, not dropped.

---

**Four moods, one conversation.** The agent proposed queries and relayed a clarify; it never wrote a
result number or picked a population. The engine decided answerability; you decided between genuine
alternatives. One contract, one truth — now reachable in plain English.
