# Analytical Practice Needs a Firmer Foundation

*A position from datumwise (independent open-source research project)*

**Huayin Wang** · Version 1.1 · 3 August 2026

Data teams have become much better at building reliable systems. We have stronger warehouses, versioned transformations, tests, contracts, observability, catalogs, lineage, and semantic layers.

Yet a familiar class of analytical failures remains.

- Two dashboards use the same metric name and disagree.
- A mean is re-aggregated as a mean of means.
- Inventory snapshots are summed across time.
- A join multiplies a measure.
- A filter changes the population while the label stays the same.
- Missing events are treated as missing values, or missing values as zero.
- A valid measure is computed at an unintended grain.

These are not all the same bug, and no single tool will eliminate them. But they recur in recognizable forms because analytical systems often lack a shared formal language for the things the failures have in common: typed coordinates, populations, absence, aggregation law, and movement between grains and universes.

The problem is not that practice has no foundation. Relational databases, SQL, dimensional modeling, and statistical methods are substantial foundations for important parts of the work.

The narrower claim is:

> Our current foundations do not provide a complete, executable account of analytical meaning and lawful transformation.

That missing account forces essential knowledge to live in prose, convention, and human memory. A firmer theory would not replace practice. It would give practice a place to put the knowledge it already has.

## Why the same failures return

A recurring failure is often a sign that the system can express an operation more easily than it can express the operation’s preconditions.

SQL can sum a column without asking whether sum is lawful along the selected axis.

A join can copy one value onto many rows without asking whether that movement is attribution, allocation, deliberate repetition, or an error.

A filter can remove members of a population without asking whether the resulting number still denotes the same measure.

A semantic layer can define a metric consistently without proving that every plan using the metric preserves its grain, population, and aggregation state.

The execution system is doing what it was designed to do. It checks syntax, data types, access rules, and physical feasibility. Analytical law is usually outside its jurisdiction.

Teams compensate with best practices:

- document the grain;
- beware of fan-out;
- do not average averages;
- treat stock and flow differently;
- inspect nulls;
- test important joins;
- ask the domain expert.

This knowledge is valuable. The problem is not that it is informal or practical. The problem is that it is rarely attached to the data in a form a machine can use to accept, qualify, or refuse a computation.

## Existing tools solve real parts of the problem

A firmer foundation should begin by recognizing what current tools already do well.

**Schema contracts** protect names, physical types, and structural compatibility.

**Transformation tests** check expected invariants and known failure cases.

**Observability** detects freshness, volume, distribution, and lineage changes.

**Catalogs and documentation** preserve human context.

**Dimensional modeling** gives strong practical guidance about grain, facts, dimensions, and common join traps.

**Semantic layers** centralize measure definitions and improve consistency.

**Query engines and optimizers** execute complex plans efficiently.

These are not failed ideas. They solve different parts of the system.

Their limitation is compositional. A collection of useful checks does not automatically become a theory of what every lawful transformation must preserve.

A test catches what someone anticipated. A definition says how to calculate a metric. Documentation explains intent. Lineage records what depended on what. None of these, by itself, supplies a general judgment of the form:

$$
\operatorname{Lawful}(T,C)
$$

where a transformation $T$ is checked against every applicable clause of a governed data object $C$.

That judgment is the missing layer.

## What the foundation must describe

A useful foundation for analytical data should be able to answer several basic questions.

1. What kind of value is this?
2. At which typed coordinates does it live?
3. Which population do those coordinates belong to?
4. What does absence mean in that population?
5. Which operations are admitted?
6. Along which anchor movements are they admitted?
7. What state must be retained for exact re-aggregation?
8. How may values cross between populations?
9. Which premises have been verified, assumed, or contradicted?
10. When should the system serve, disclose, clarify, or refuse?

The Theory of Data proposes one formal vocabulary for answering them.

It is a working theory, not a settled standard. Its importance depends on whether the vocabulary proves useful, executable, and complete enough for the failure classes it claims to govern.

## The objects of the theory

The theory begins with typed location.

A **datum** is one typed value at one typed anchor point:

$$
p=(a,x)
$$

Its key is the anchor point $a$.

A **member** — a governed series; the object a trustworthy column realizes at one grain — is a homogeneous, functionally consistent binding of datums:

$$
v:S_v\rightarrow X
$$

A **measure** is the stable governed family whose laws determine which anchored members share one analytical identity. `revenue` is a measure; transaction revenue and customer-month revenue may be different members of it. The first failure on the opening list becomes precise here: two dashboards that disagree under one metric name are two fields claiming membership in one measure without a licensing derivation.

A **universe** identifies the population in which those anchor points exist. Event universes are generated by occurrences. Spine universes establish expected points independently of value presence.

This difference matters immediately.

If no transaction occurred, the corresponding event point may not exist. If a daily reporting spine expects a store-day point and no value is present, the absence may be a missing-value condition.

The concise distinction is:

> Events generate coordinates. Spines await values.

A governed member carries an explicit contract:

- **V-anchor:** where values live;
- **M-anchor:** where absence has operational significance;
- **B-law:** where a given operator and anchor movement must stop — the Theory’s contract-inheritance boundary;
- **family:** which aggregators, state representations, and compositions are admitted;
- **evidence status:** which declarations are verified, corroborated, assumed, unidentifiable, or contradicted.

These declarations do not describe every aspect of the business world. They describe the parts of meaning required to govern analytical movement.

## From “best practice” to typed obligation

Consider the question:

> May inventory be summed across months?

In ordinary practice, the answer may live in documentation or in the memory of an experienced analyst.

In the proposed foundation, the question becomes explicit.

The inventory-level member at store-day carries:

- a value type;
- a universe;
- a V-anchor containing a time level;
- the measure’s family of admitted operators;
- a B-law that blocks `sum` over the relevant time contraction.

A proposed reducer contains both its input and output anchors. The kernel checks whether `sum` is licensed for that exact movement.

The result is not “we recommend against it.” It is:

> This transformation is not defined under the declared contract.

The same mechanism is not limited to time. A measure may be blocked across product, scenario, geography, legal entity, or any other typed axis.

Stock and flow remain useful domain words. The executable rule is the operator-and-anchor restriction underneath them.

## Aggregation requires more than a formula

Many analytical failures arise because an aggregator’s displayed output is mistaken for sufficient state.

A mean is a simple example. The scalar mean cannot generally be re-aggregated exactly. The pair:

$$
(\mathrm{sum},\mathrm{count})
$$

can.

Count-distinct can be composed exactly through set union, but the exact state may be unbounded. A sketch gives bounded approximate state and therefore carries an approximation obligation.

The foundation should distinguish:

- exact scalar state;
- exact fixed-size structured state;
- exact unbounded state;
- approximate bounded state.

This turns “do not average averages” from a warning into an algebraic property of the declared operator family.

Algebra is still not sufficient. A sum may compose perfectly as a monoid and remain unlawful for a particular measure, population, or anchor movement.

## Joins require a passage law

A fan-out is not only a join problem. It is an undeclared value-movement problem.

Suppose one order value relates to several line-item points. The relation alone does not say whether the value should be:

- copied to every line;
- assigned to one line;
- split by weights;
- retained at order grain;
- prohibited from crossing.

The foundation separates the coordinate relation from the value law.

This makes conservation testable. For a split allocation:

$$
\sum_b v'(b)=\sum_a v(a)
$$

should hold under the declared weights.

A conventional join may implement the plan. It should not be allowed to invent the plan’s meaning.

## Lawfulness is a conjunction

A transformation is lawful only when every applicable obligation is licensed.

For a reducer, those obligations may include:

- **type:** the operator accepts the input type and produces the declared output type;
- **anchor:** the source-to-target map is a valid hierarchy movement or contraction;
- **algebra:** the aggregation state supports the requested composition;
- **family:** the measure’s law admits the operator for this member;
- **B-law:** the exact movement is not blocked;
- **M-law:** absence and coverage obligations are respected;
- **universe:** the movement remains within a population or uses a declared passage;
- **population:** the result denotes the intended members.

This is stricter than checking whether the plan runs. It is also more modest than claiming that the system has discovered absolute truth.

The judgment is relative to a declared model and the evidential status of its premises.

## Declaration should complement documentation

A formal foundation does not make prose unnecessary.

Documentation remains the best place to explain:

- why a measure matters;
- who owns it;
- how the business uses it;
- historical context;
- unusual exceptions;
- domain language.

Declarations serve a different purpose. They encode the clauses computation must obey:

- value type;
- anchor;
- universe;
- admitted family;
- sufficient state;
- blocked movements;
- crossing laws;
- coverage obligations.

The practical change is therefore not “declaration replaces documentation.”

It is:

> Documentation explains meaning to people. Declarations make selected parts of meaning binding on machines.

## Adjudication should complement trust

A declaration can be wrong.

A model may claim that every store maps to one region when the actual data contains conflicting assignments. It may claim complete coverage when expected points are absent. It may declare allocation weights that do not sum to one.

Where a clause is testable, the system should adjudicate it against the data before publication or execution.

Where a clause is not identifiable from the data, the system should record that honestly.

Useful premise statuses include:

- verified;
- corroborated;
- assumed;
- unidentifiable from available data;
- contradicted.

This prevents two opposite errors:

- trusting every declaration because it was centrally defined;
- pretending the data can prove every semantic premise.

The kernel’s guarantee is relative:

> Given the declared contract and the recorded status of its premises, determine whether the proposed transformation preserves that contract.

## Refusal is one result, not the only result

A lawful system should not reduce every uncertainty to either “answer” or “error.”

The Theory of Data proposes four response modes.

### Serve

One lawful interpretation exists and all material obligations are discharged.

### Disclose

The result is lawful, but coverage, approximation, skew, stale support, or another material condition must accompany it.

### Clarify

Several lawful interpretations exist and a human choice is part of the meaning.

### Refuse

No lawful plan exists under the declared model and available premises.

This is more useful than a system that always answers, but it is also more useful than one that refuses whenever certainty is incomplete.

Honesty is not maximal caution. It is making the response match the proof state.

## Lawfulness is not faithfulness

Even a lawful plan can answer the wrong question.

A planner may select:

- a related but unintended measure;
- the wrong lawful population;
- an unintended output anchor;
- a lawful but unintended crossing path.

A trusted analytical system therefore needs two judgments:

$$
\operatorname{Lawful}(P,M)
$$

and:

$$
\operatorname{Faithful}(P,Q,M)
$$

The first asks whether plan $P$ preserves model $M$.

The second asks whether plan $P$ actually answers question $Q$ under that model.

This distinction becomes especially important when language models or search procedures propose plans. Semantic checking must verify both the legality of the movement and its fidelity to the ask.

## What changes in practice

A firmer foundation would not arrive as one replacement product. It would change several interfaces.

### Models become executable contracts

The model records anchors, universes, families, blocked movements, sufficient states, and crossing laws in a neutral form.

### Publication includes adjudication

Testable declarations are checked against the actual data. Contradicted clauses prevent publication or narrow what may be served.

### Planning becomes certifiable

An untrusted planner may search for candidate plans. A trusted kernel checks lawfulness and faithfulness before any executable query reaches the database.

### Answers carry proof-derived conditions

Coverage limits, approximation guarantees, assumptions, and crossing choices travel with the result because they arise from the certification process.

### Refusal becomes precise

The system names the violated obligation and identifies what declaration, data correction, or human choice would be required to proceed.

These changes complement existing tests, contracts, observability, semantic layers, and engines. They give those tools a common object model for analytical law.

## What the theory does not yet prove

A foundational proposal should state its limits.

The current theory does not yet prove that:

- its primitive calculus is complete for every analytical operation;
- its declaration categories are minimal;
- independent modelers will produce compatible contracts reliably;
- every important failure maps cleanly to one named obligation;
- the approach will outperform conventional methods across domains;
- refusal decisions are always correct;
- faithfulness can be decided for unrestricted natural-language questions.

Those are research questions.

The appropriate evidence hierarchy is:

1. internal coherence;
2. compression of known failure classes;
3. implementation feasibility;
4. convergence with related traditions;
5. executed attacks and benchmarks;
6. comparative and predictive evaluation.

The maxim is:

> Agreement is search evidence; execution is evidence.

## Why build it now

The analytical stack is becoming more modular. Engines, plans, and transport can increasingly be separated and exchanged. Language models can propose queries and plans at a scale that makes manual review less dependable.

That makes the semantic gap more urgent.

A faster engine can execute a wrong plan faster. A better planner can produce more plausible wrong plans. A richer semantic catalog can centralize an incorrect assumption more efficiently.

The missing capability is not more generation. It is adjudication.

[Columna](https://github.com/datumwise/columna) is an open-source attempt to implement this layer: declared models, premise checks, certified planning, and answer modes that can serve, disclose, clarify, or refuse.

The project does not validate the theory merely by existing. Its value will depend on whether it prevents failures, exposes assumptions, transfers across domains, and earns trust under adversarial testing.

## The practical position

Analytical practice does not need to abandon its tools. It needs a firmer account of what those tools are allowed to do.

Rows and tables can continue to store data.

SQL can continue to execute plans.

Tests can continue to verify expected behavior.

Semantic layers can continue to define shared measures.

Documentation can continue to explain the business.

But the laws of analytical movement should be stated directly, attached to the governed data, checked against evidence, and enforced before execution.

The next improvement in analytics is not only faster computation or better generation.

It is the ability to say, with reasons:

- this answer is lawful;
- this answer is lawful under stated conditions;
- this question has several lawful readings;
- this computation is undefined and must not be served.

That is what a firmer foundation should make possible.

## Reading path

This piece is part of the datumwise series. The suggested order is: *Analytical Practice Needs a Firmer Foundation* — *Row, Table, and Join Are Not the Foundations of Analytical Meaning* — *The Theory of Data: An Introduction* — *Frame-QL: An Introduction* — *Never Let Your Agent Touch the Database*.

## Further reading

- [The Theory of Data: Governed Analytical Objects, Lawful Transformation, and Certification](https://doi.org/10.5281/zenodo.21774032). Version 4.0. datumwise.
- [*A Contract Calculus for Governed Analytical Transformation*](https://doi.org/10.5281/zenodo.21752373). Version 1.0.
- [Columna](https://github.com/datumwise/columna) — the open-source governed engine; the Frame-QL Manual is distributed with the repository, and every example in it is verified against the running parser.
