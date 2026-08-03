# Never Let Your Agent Touch the Database

*A position from datumwise (independent open-source research project)*

**Huayin Wang** · Version 1.1 · 3 August 2026

AI agents can be useful in analytical systems. They can interpret a question, search a governed model, propose a structured request, compare candidate interpretations, and explain a result.

They should not hold database credentials or control an executable database language.

That is the position.

> **Treat the model as an untrusted searcher. Put a small, deterministic, governed boundary between the model and the database.**

This is not an argument that language models are uniquely malicious, or that databases can never be used safely by automated software. It is an architectural claim about authority.

A probabilistic model is good at proposing possibilities. It is not the right component to decide, by itself:

- which data it may access;
- which analytical interpretation is lawful;
- which query plan may execute;
- how much warehouse work may be spent;
- whether an ambiguous question should produce a number;
- whether a result should be served, qualified, clarified, or refused.

Those decisions should belong to a smaller system whose behavior can be inspected, tested, constrained, and audited.

## What “touch the database” means

The phrase is stronger than “use read-only credentials.”

An agent touches the database when model output directly controls executable database behavior. That includes architectures in which the model:

- holds credentials;
- writes SQL that is sent to the warehouse;
- selects arbitrary tables and columns through a database tool;
- controls an unrestricted query builder;
- chooses joins, filters, groupings, or limits that are translated directly into execution;
- emits SQL that a validator approves after the fact.

A model does **not** need that authority in order to answer analytical questions.

It can instead speak a constrained language over declared meaning. It can say, in effect:

> “I believe the user is asking for this measure, over this population, at this output anchor, under this interpretation.”

A trusted layer can then determine whether that request is defined, whether the interpretation is faithful, and which engine-owned plan may execute.

The model may propose. It should not adjudicate.

## One authority creates three kinds of risk

Security, cost, and analytical correctness are often treated as separate concerns. In practice they have different owners, incident processes, and products.

But all three become harder when a model can author arbitrary executable database commands.

### Security risk

A model with database authority is an untrusted client with a natural-language control surface.

Its behavior can be influenced by:

- prompt injection;
- malicious retrieved content;
- compromised tools;
- misleading metadata;
- accidental instruction conflicts;
- user requests that exceed the user’s own authority;
- model-generated plans that expose sensitive fields indirectly.

Least-privilege accounts, row-level policies, masking, read replicas, and audit logs are necessary controls. They reduce damage. They do not change the underlying fact that model output remains on a privileged path to the data.

The strongest reduction in model blast radius is to avoid giving the model database authority at all.

This does not make the whole system secure. The trusted engine, model registry, compiler, credentials, execution service, and result channel still require ordinary security engineering. The gain is narrower and concrete: compromise of the model does not automatically become arbitrary database execution.

### Cost risk

A model does not experience warehouse cost.

It can:

- omit a partition predicate;
- select a much larger population than intended;
- repeat an expensive request in a loop;
- explore many candidate queries;
- generate structurally different plans for the same meaning;
- retry successful work because it is uncertain about the answer;
- trigger computation when a cached governed result already exists.

Post-generation limits can stop some extreme cases. Cost estimation can reject obviously expensive SQL. Query quotas can cap damage.

Those controls are useful, but they are reactive. They inspect commands after the model has been allowed to create them.

A governed request boundary changes the order of control. The engine owns the set of possible execution shapes. The model can ask for a declared meaning; it cannot invent an arbitrary scan.

This does not guarantee low cost. A lawful analytical request may still be expensive. The difference is that the cost belongs to a known plan class that the engine can estimate, budget, cache, schedule, or decline before execution.

### Analytical risk

A secure and inexpensive query can still be wrong.

The most dangerous errors in analytics are often not syntax errors. They are successful computations over an unstated interpretation.

A model may:

- average values that were already averaged;
- sum a snapshot across a blocked time movement;
- re-aggregate an exact distinct count without its sufficient state;
- choose a plausible but unintended population;
- treat missing events as missing values;
- cross a many-to-many relation and duplicate a measure;
- choose one legitimate interpretation without telling the user;
- fabricate a measure whose name resembles a declared one;
- answer at a lawful anchor that is not the anchor requested.

SQL validation cannot prove these choices correct when the necessary meaning has never been declared.

The problem is not merely that models sometimes generate bad SQL. It is that SQL is not a complete language for stating the obligations that make an analytical result defensible.

## Why guardrails are not the same as a boundary

Guardrailed text-to-SQL is real progress.

A responsible system may use:

- read-only credentials;
- statement allowlists;
- schema restrictions;
- row limits;
- cost estimates;
- scan caps;
- query timeouts;
- static analysis;
- replicas;
- human approval;
- audit logs.

These controls should exist whenever generated SQL is used.

But they answer a different question:

> “May this command run safely enough?”

They do not necessarily answer:

> “Does this command compute the meaning the user asked for?”

A query can pass every operational guardrail and still use the wrong input anchor, population, crossing law, or aggregation state.

The deeper architectural distinction is:

- **inspection after authorship:** the model writes an executable command and another component tries to reject bad ones;
- **construction under law:** the model can express only a governed request, and the trusted engine constructs the executable plan.

The second approach does not remove the need for inspection. It removes the model’s authority to author the final command.

## A semantic layer helps, but a vocabulary is not yet a proof

Semantic layers are closer to the needed boundary because they declare shared measures and dimensions.

They can substantially improve:

- consistency;
- discoverability;
- access control;
- reuse;
- performance;
- governance.

The remaining question is whether the semantic model carries enough law to adjudicate difficult requests.

A conventional metric definition may state how revenue is calculated. It may not state:

- the member’s input anchor;
- the universe whose members contribute;
- where absence is meaningful;
- which reductions are blocked;
- which aggregation state must be retained;
- how values may cross a many-to-many relation;
- whether multiple lawful interpretations exist;
- what evidence supports the declaration.

A menu of predefined metrics reduces freedom by limiting what can be requested. A governed grammar can do something different: allow a broad class of requests while restricting what may be **silently meant**.

That distinction matters.

## The Theory of Data boundary

The Theory of Data provides one vocabulary for building this boundary.

A **datum** is one typed value at one typed anchor point:

$$
p=(a,x)
$$

A **member** — a governed series; the object a trustworthy column realizes at one grain — is a homogeneous, functionally consistent binding of datums:

$$
v:S_v\rightarrow X
$$

A **measure** is the stable governed family whose laws determine which anchored members share one analytical identity; `revenue` is a measure, while transaction revenue and customer-month revenue may be different members of it.

A **universe** identifies the population in which those anchor points exist.

A governed member carries declarations such as:

- **V-anchor:** where values live;
- **M-anchor:** where absence has operational significance;
- **B-law:** where a particular operator and anchor movement must stop — the Theory’s contract-inheritance boundary;
- **family:** which operations and aggregation states are admitted;
- **evidence status:** which premises are verified, corroborated, assumed, unidentifiable, or contradicted.

A request can then be judged against explicit obligations rather than inferred from container structure.

For example, a reducer needs an input anchor, an output anchor, an aggregator, and a lawful anchor map:

$$
(q_*^g v)(b)
=
g\{v(a)\mid q(a)=b\}
$$

The trusted system can ask:

- Is the anchor movement valid?
- Does the aggregator accept the value type?
- Does the measure’s family admit the operation?
- Does the required sufficient state exist?
- Does B-law block this movement?
- Are M-anchor and coverage obligations satisfied?
- Does the plan remain within one universe or use a declared passage?
- Does the result answer the user’s actual ask?

These questions cannot be settled by fluency.

## Split the planner into an untrusted searcher and a trusted kernel

A practical agent architecture does not require deterministic search everywhere.

Planning can be difficult. Natural-language interpretation can be ambiguous. There may be many lawful candidate plans.

A model can help search that space.

The important split is:

### Untrusted searcher

The model may:

- interpret user language;
- inspect a public logical projection of the governed model;
- identify candidate measures, anchors, universes, and operations;
- propose one or more structured asks;
- propose candidate plans;
- explain ambiguity;
- ask for clarification.

The searcher may be probabilistic, replaceable, and even adversarial.

### Trusted kernel

A deterministic kernel must check at least two independent obligations.

#### Lawfulness

Does the candidate plan preserve every applicable clause of the declared data contract?

$$
\operatorname{Lawful}(P,M)
$$

#### Faithfulness

Does the candidate plan compute the denotation of the user’s ask rather than a nearby lawful computation?

$$
\operatorname{Faithful}(P,Q,M)
$$

A lawful plan can still answer the wrong question. Both judgments matter.

Only a certified plan reaches the execution service.

The governing principle is:

> **Probability may search. It may not adjudicate.**

## Engine-owned execution

After certification, the engine—not the model—constructs or selects the executable plan.

The model should never need to know:

- database credentials;
- physical table names;
- hidden join keys;
- storage locations;
- partition details;
- execution-specific SQL;
- sensitive schema not exposed by the public model projection.

The trusted execution layer may compile the certified plan to SQL, use a dataframe engine, call a semantic service, read a columnar file, or execute another backend.

The important point is ownership. The executable artifact belongs to the trusted system.

This keeps the logical request separate from the physical binding.

## Four honest outcomes

An analytical system should not turn every request into either a number or an error.

A governed boundary can return four kinds of result.

### Serve

One lawful and faithful interpretation exists, and all material obligations are discharged.

### Disclose

The result is lawful, but a material condition must accompany it—for example incomplete coverage, approximation, stale-but-permitted data, or deliberate overlap.

### Clarify

More than one lawful interpretation exists and human choice is part of the meaning.

### Refuse

No lawful and faithful plan exists under the declared model and available premises.

Refusal is not a failure of the agent. Serving an undefined result would be the failure.

At the same time, refusal should not become a substitute for careful modeling. A system that refuses too broadly has poor recall. The goal is not maximal restriction. It is high precision over lawful asks and broad coverage of the lawful inquiry space.

## A many-to-many example

Suppose the user asks for revenue by product category, and products may belong to several categories.

A relation between products and categories does not determine how revenue should move.

Several interpretations may be lawful:

1. **Touch**  
   Count the full product revenue in every category. Totals intentionally exceed the grand total.

2. **Primary assignment**  
   Assign each product to one primary category. Some memberships are ignored.

3. **Weighted split**  
   Divide each product’s revenue across categories using declared weights that conserve the total.

These are not three SQL tricks. They are three meanings.

The model may notice the ambiguity. It should not choose silently.

The governed system should clarify, or execute a named passage whose consequences travel with the answer.

This is how a grammar can be safer without being only a narrow menu.

## What this architecture does not guarantee

The boundary is not magic.

It does not guarantee that:

- the declared model is true;
- every relevant semantic fact has been declared;
- the kernel is bug-free;
- every lawful question is expressible;
- the model will interpret language correctly;
- the database or execution engine is secure;
- costs are always small;
- all analytical errors fit the current theory;
- refusals are always correct;
- production effectiveness has already been established across industries.

A wrong contract can be enforced consistently.

That is why declarations should be adjudicated where possible, carry evidential status, and remain open to human review and revision.

The architecture changes what can fail silently. It does not abolish fallibility.

## The practical rule

Let the model:

- interpret language;
- search declared meaning;
- propose structured asks;
- propose candidate plans;
- identify ambiguity;
- explain certified results and disclosures.

Do not let the model:

- hold database credentials;
- author arbitrary executable database commands;
- redefine the governed model at request time;
- bypass lawfulness or faithfulness checks;
- turn ambiguity into a confident number;
- decide its own execution authority.

The strongest version of the position is not “never use AI with a database.”

It is:

> **Never make probabilistic model output the final authority over database execution or analytical meaning.**

Put a governed wall in between.

Make that wall small enough to inspect, expressive enough to serve legitimate questions, and honest enough to clarify or refuse when the data does not support a defensible answer.

## Reading path

This piece is part of the datumwise series. The suggested order is: *Analytical Practice Needs a Firmer Foundation* — *Row, Table, and Join Are Not the Foundations of Analytical Meaning* — *The Theory of Data: An Introduction* — *Frame-QL: An Introduction* — *Never Let Your Agent Touch the Database*.

## Further reading

- [The Theory of Data: Governed Analytical Objects, Lawful Transformation, and Certification](https://doi.org/10.5281/zenodo.21774032). Version 4.0. datumwise.
- [*A Contract Calculus for Governed Analytical Transformation*](https://doi.org/10.5281/zenodo.21752373). Version 1.0.
- [Columna](https://github.com/datumwise/columna) — the open-source governed engine; the Frame-QL Manual is distributed with the repository, and every example in it is verified against the running parser.

Earlier datumwise notes on the same architecture:

- [The Open Planner: Certified Analytical Plans from Untrusted Searchers](https://doi.org/10.5281/zenodo.21632723)
- [The Two Anchors of a Measure](https://doi.org/10.5281/zenodo.20789318)
- [Multi-Universe Processing](https://doi.org/10.5281/zenodo.21543584)
- [The Two Great Sources of Silent Analytical Failure](https://doi.org/10.5281/zenodo.21553379)
- [Ground Truth benchmark kit](https://github.com/datumwise/ground-truth-benchmark)
- [Columna](https://github.com/datumwise/columna)
