# Never Let Your Agent Touch the Database

*A position held by datumwise · July 2026 · v1.0.
Evidence-linked throughout; the position moves if the evidence does. This is the site edition; the paper edition lives on Zenodo ([doi.org/10.5281/zenodo.21765252](https://doi.org/10.5281/zenodo.21765252)).*

---

Three different people in your company are currently afraid of the same
architecture, for three different reasons — the one where an AI agent holds your
database credentials and writes its own queries.

Your security lead read the incident write-ups: an LLM with database
credentials is an attack surface with a natural-language interface — prompt
injection becomes data exfiltration, the model's elevated privileges bypass
user-level permissions (the old "confused deputy," reborn with a chat window),
and a compromised agent is a gateway to everything it can see. The emerging
consensus in the security literature is blunt: treat the model as an untrusted
client, always.

Your finance lead read the bills. Warehouses charge per byte scanned and per
second of compute — pricing built for analysts who run hundreds of queries a
day and feel a slow query in their fingertips. Agents run thousands of queries
an hour at 2 a.m. with no cost intuition at all. The measured reality:
LLM-generated SQL shows up to 3.4× cost variance across models, with outlier
queries scanning more than 36 gigabytes because nobody added a partition
filter. A runaway agent loop is a four-figure bill in minutes, and your
monitoring flags errors — not expensive successes.

And your data lead read the accuracy reports. State-of-the-art text-to-SQL
scores roughly 75–85% on the public benchmarks; the best warehouse-native
systems report 85–90% against a well-built semantic model. Read those numbers
the other way: one answer in ten is wrong, and it is served at exactly the
same confidence as the nine that are right. Worse — as our own nine-model
benchmark showed — the failures that matter are silent: entire failure
families fail identically across vendors and scales, unmoved by better
documentation.

Breach. Bill. Fabrication. Three fears, three budgets, three vendor
categories selling three mitigations. Our position is that all three fears
are one architectural mistake, and they retire together the moment you make
one decision:

**Your agent never touches the database. Not directly, not through generated
SQL, not through a guardrail that inspects the SQL it generated anyway.**

## What the market does instead

**Guardrailed text-to-SQL** — validators, read replicas, least-privilege
accounts — inspects queries *after a model authors them*. The guardrail
catches syntax and unbounded scans; it cannot catch wrong meaning, because
meaning was never declared anywhere it could check. Safety by inspection,
not construction.

**Warehouse-native governed NL** — semantic views plus a managed gateway —
is real progress on the breach fear, inside one vendor's walls. But the core
step is still *SQL generation from a model of the schema*: 85–90% accurate,
served uniformly confident, with no contract for the other 10–15%. And the
cost fear inverts into the vendor's feature: every agent query drives
warehouse consumption you're already paying for.

**Semantic layers with AI endpoints** are the closest kin — a declared
vocabulary is genuine insulation. But the definitions are asserted, never
tested against the data; the hard questions (anything crossing a
many-to-many) are silently mangled or simply absent; and there is no way for
the system to say *"that question has three legitimate answers"* or *"that
metric is not defined here."* It serves what it has, confidently, and what it
has is a menu.

## The wall

There is a fourth architecture. Put a declared, adjudicated meaning layer
between the model and the data — and make the model speak *its* language
instead of the database's.

In Columna, the model's only channel is a grammar that can reference declared
meaning and nothing else. No one — not the model, not the middleware — writes
SQL at any step; the engine executes its own plans over meaning that was
declared by a human and *tried against the data itself* before it ever
served. Every answer comes back in one of four moods: served; served with its
assumptions stated; clarified ("your question has three legitimate answers —
choose"); or refused, with the reason. Ask it for a metric that doesn't
exist, and it will tell you so — verbatim transcripts of exactly that refusal
ship in the repo, because we don't ask you to take honesty on faith.

Now walk the three fears through the wall. **Breach**: the model holds no
database credentials and speaks no executable query language; there is no
injection payload in a grammar that cannot express one, and the blast radius
of a compromised agent is "asks the wall questions." **Bill**: every ask has
a declared shape the engine owns; there is no arbitrary scan to run away
with, and the engine's cache serves repeated meaning without repeated
compute. **Fabrication**: the numbers are grounded in engine execution,
formatted from the wire verbatim — and the ill-defined ask *cannot* be served
as a confident number, because refusal is a first-class answer.

One wall. Three insurance policies. Apache-2.0.

## "But a wall is narrow" — no. Measure it.

The objection writes itself: governed means restricted; you've bought safety
by shrinking what can be asked. So measure it, with the instrument every data
scientist already trusts. **Precision**: of the inquiries served, how many
were defensible? **Recall**: of the *legal* inquiries — the ones with a
defined meaning over your actual data — how many can be served?

Text-to-SQL fails precision by construction: it cannot abstain, so every
ill-defined ask becomes a confident false positive (its apparent 100% recall
is inflated by served illegalities — "average order value" over a warehouse
with no order entity is not an answer, it's an accident). Semantic layers
fail recall: a menu of pre-compiled metrics with no lawful many-to-many, no
clarification, no crossing — the industry's most common hard question,
unaskable. And the standard remediation — bolting guardrails onto generation
— *spends recall to buy safety while gaining almost no precision*, migrating
toward the worst corner of the chart.

Columna's refusals are precision events, not recall failures. And its recall
runs *wider* than either incumbent where it matters most: "revenue by
category" over products in multiple categories has three legitimate meanings,
and Columna serves all three — the deliberate over-count with its 1.44× skew
stated on the answer, the single-count with its 270 discarded memberships
disclosed, the weighted split reconciling to the grand total to the cent,
certified. The wall is made of grammar, not menu items: the grammar does not
regulate what you can ask; it regulates what can be silently meant. And where
our recall has gaps, they're published — a dated ledger of exactly which
inquiry classes come next, which no closed vendor can show you.

The market has spent three years A/B testing precision against recall.
This is the F1 play.

## See it, don't trust it

`pip install columna && columna-server demo --play` — two minutes, no signup.
Connect any agent and ask for something plausible that isn't there. The most
trustworthy thing the wall will do is refuse you, and tell you why.

---

*Evidence, one click each: [the nine-model study](https://doi.org/10.5281/zenodo.21349581) ·
[the public benchmark kit](https://github.com/datumwise/ground-truth-benchmark) ·
[Two Anchors](https://doi.org/10.5281/zenodo.20789318) ·
[Multi-Universe Processing](https://doi.org/10.5281/zenodo.21543584) ·
[The Two Great Sources](https://doi.org/10.5281/zenodo.21553379) ·
[the case study](/case) · [the story](/story) · and the demo:
`pip install columna`.*
