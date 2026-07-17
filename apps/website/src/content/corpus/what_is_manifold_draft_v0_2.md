# What is a Manifold?

*A plain-language companion to the framework manual. Loose analogies ahead — the manual
draws the exact lines.*

---

If you read [What is Columna?](/what-is-columna), you met the Manifold in one sentence:
the described, checked data model that agents (or you) query. If you read
[What is FrameQL?](/what-is-frameql), you met it as "a model that already knows." Both
sentences point at one claim, and if you take a single thing from this page, take this:

**The Manifold is the new data model — the data model of substance, where the relational
model was the data model of form.**

The relational model earned its fifty years by modeling *form* completely: rows, tables,
keys — the shape of records. What it never modeled is what the records *mean*. That's why
every serious analytical conversation happens in a vocabulary SQL doesn't have, and why
the meaning has lived in heads, wikis, and tribal memory ever since. The Manifold is a
data model of the other thing: the **substance**. Its primitives aren't tables and keys —
they are populations, coordinates, metric families, and laws. And just as SQL is the
grammar paired to the relational model, FrameQL is the grammar paired to this one: the
model beneath the grammar.

## The artifact

A Manifold is a **description of what a dataset means**, kept as a first-class object next
to the data it describes. It holds:

- the **populations** — which worlds of facts exist (transactions; store-days), and what a
  missing row means in each (a real zero, a gap, or a membership fact);
- the **coordinates** — the grains you can stand at, and the declared functional paths
  between them (`day → month`, `store → region`);
- the **metric families** — which quantities live where, and the operators that are lawful
  for each along each path (revenue sums anywhere; an inventory *level* does not sum
  across time);
- and the **laws** — the declared invariants and restrictions that make all of the above
  checkable rather than aspirational.

Notice what it doesn't hold: **rows**. A Manifold contains no data. It is the Frame idea
from FrameQL, applied to a whole dataset — everything about the meaning, nothing about the
values. The values stay in your database; the meaning finally gets a home of its own.

## The part that makes it different: the trials

Plenty of tools let you *write down* what data means — a metrics file, a semantic model, a
wiki page. All of them share a fate: they drift. The description says one thing, the data
grows into another, and nobody finds out until a number is wrong in a meeting.

A Manifold is a description that **stands trial**. Every claim in it is checked against
the actual data and wears the outcome — *verified*, *corroborated*, *untestable*, or
*contradicted* — and the verdicts have teeth: a contradicted claim doesn't linger as a
stale comment; it cuts its own serving scope until the data or the declaration changes.
The system never serves past its verdicts.

So the artifact is really two things fused: the **law** (what was declared) and the
**trial record** (how the declarations fared against reality). That fusion is what makes
a Manifold trustworthy enough to hand to an agent — and it's what a schema, a metrics
YAML, or a documentation page never had.

## A living artifact

A Manifold has a lifecycle, and the lifecycle is the point:

**proposed → declared → adjudicated → published → re-attested → amended → republished.**

Authoring tools (like `columna init`) *propose* one from a messy database; a human
*declares* what's true; the trials run; the artifact *publishes* and starts serving. Then
the world moves — data drifts, a claim gets contradicted, scope gets cut, the author
amends, the trials run again. A Manifold at rest is a snapshot; a Manifold in use is a
history. Formats will vary and implementations will multiply; the artifact's identity
stays the same — *the declared meaning, plus its trials.*

## The center of an ecosystem

Data models are what ecosystems form around — fifty years of tooling grew on the
relational model, and the same will happen here, because the Manifold is an artifact: a
thing you can hold, version, and speak to. Tools grow around it in rings. Four categories matter, and only one of them is "ours":

**Authoring tools.** Everything that helps meaning get *into* a Manifold. Expect these to
grow like mushrooms — every backend, every model, every interface wants its own front
door. They can differ in everything except one law they all inherit: tools *propose*;
only humans *declare*. Data may suggest walls, never doors.

**Explorer tools.** Everything that helps people *see* a Manifold. If the Manifold is the
phone, explorers are the phone covers — many, varied, replaceable, and none of them the
point. Our [Explorer](/explorer) is deliberately one of many: it binds to the standard
`describe` rendering and nothing else, which is exactly the seam any other explorer would
use.

**MCP servers.** Everything that lets *agents* speak to a Manifold. There is one wire
contract; there will be many shells around it — custom MCPs tuned to a team, a domain, a
deployment — all thin, because the contract underneath does the work. (And beneath every
shell, the same API, which you can also call directly.)

**Agents.** Here is where it gets interesting. The Manifold separates the **grammar
layer** (what can be asked, and what the answers mean — declared, adjudicated, stable)
from the **semantic layer** (what's *worth* asking, what the domain knows, what good
judgment looks like). The old "semantic layer" collapsed both into one proprietary
artifact. Un-collapsing them opens a new creative space: agents that bundle skills,
domain knowledge, and judgment — specializing freely, at every level of sophistication —
precisely because the meaning they reason over is already settled beneath them. A
finance-close agent and an inventory-ops agent can be utterly different minds speaking
the same lawful ground. That's a new kind of semantic layer, and it doesn't belong to us;
it belongs to whoever builds it.

## Try one

The demo Manifold is live in the [Explorer](/explorer) — every population with its basis,
every measure with its laws, every claim with its verdict, and a query to copy on each
card. Or read it the way an agent does:

```
pip install columna
columna-server demo --play
```

## Go deeper

- **[The framework manual](/docs/framework)** — populations, coordinates, families, laws,
  adjudication: every exact line.
- **[What is FrameQL?](/what-is-frameql)** — the language you speak to it.
- **[What is Columna?](/what-is-columna)** — the framework around it.
