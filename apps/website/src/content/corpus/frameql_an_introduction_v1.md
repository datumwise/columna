# Frame-QL: An Introduction

*Query by Declaring the Result*

**datumwise, an independent open-source research project**

**Version 1.0**

**DOI:** [doi.org/10.5281/zenodo.21763321](https://doi.org/10.5281/zenodo.21763321)

**Keywords:** Frame-QL; analytical query language; Theory of Data; atom; atom member; frame; Manifold; governed analytics; analytical intent; AI agents; SQL; certification

---

## Abstract

Frame-QL is a language for declaring a governed analytical result. The requester names the analytical objects to be returned, declares the anchor at which their requested members should exist, and states the conditions that shape the result. The requester does not prescribe the relational operations or physical commands used to produce it.

This design follows from the ontology of the Theory of Data. An **atom** is a stable governed measure family, such as revenue, inventory level, or order count. An **atom member** is one governed realization of that atom at a particular analytical location under a member contract. A **frame** is an assembly of co-anchored fields at one output anchor; in the fully governed case, every field is an atom member. A **Manifold** records the atoms, root members, family laws, populations, boundaries, evidence, lineage, and physical bindings required to adjudicate the class of member derivations it supports.

Because that knowledge is governed outside the query, a requester can ask for the customer-month member of the revenue atom without writing the path that constructs it. The planner resolves and certifies the request; a trusted engine may then realize it through SQL, dataframe operations, a cache, an API, or another backend.

This paper develops the governing idea of Frame-QL: the output frame is the query. It explains why rows, tables, joins, and GROUP BY are not primitives of the request interface; how atom identity differs from a physical column; how ambiguity becomes clarification rather than silent choice; and why Frame-QL gives AI agents a useful interpretive role without granting them authority over analytical law or database execution. The Frame-QL Manual remains authoritative for syntax and shipped behavior.

## About this introduction

This is an introduction to the idea behind Frame-QL, not a grammar reference or a catalogue of language features. It develops one proposition:

> **A Frame-QL query declares the output data. It does not prescribe the process used to produce it.**

The proposition has two consequences.

Specifying the output can be sufficient because the Manifold already contains the governed knowledge required to identify supported analytical objects and derive their lawful members.

Specifying the output is also the limit of the requester's authority. Planning, analytical law, physical binding, credentials, and executable backend commands belong to trusted system components.

The language is concise because responsibility has been divided, not because the omitted work has disappeared.

# 1. The result is the query

Consider a request for revenue by customer and month:

```frameql
FROM retail_manifold
SELECT revenue
AT {customer, cal.month}
```

The surface is deliberately familiar. A SQL-literate reader can see a source, a selected measure, and an output location. But the statement is not a compressed relational program.

`revenue` names a governed analytical identity. `AT {customer, cal.month}` declares where the requested result should live. The query asks for the customer-month member of the revenue atom and for the frame that contains it.

It does not name a transaction table. It does not identify a customer key, choose a date column, write a join, specify a grouping procedure, or decide whether the result should be read from detail, a materialization, a cache, or an external service. It does not assume that the backend is relational.

Yet the request is precise at the level that matters to the requester. It states what analytical object is wanted and where that object must exist.

This is the governing reversal of Frame-QL:

> **The requester declares the result. The governed system owns the derivation.**

The distinction is easiest to see by separating an atom from its members.

# 2. The atom is named; the member is requested

An atom is a stable governed measure identity together with the family laws that determine its lawful members.

Revenue is an atom. It is not identical to a particular column in an orders table, a particular SQL expression, or a particular stored grain. Its identity is intended to survive changes in physical representation.

An atom member is one governed realization of that atom at a particular anchor in a particular universe under a complete member contract. Conceptually, the revenue atom may have lawful members such as:

```text
revenue at transaction
revenue at customer-month
revenue at region-quarter
```

When the revenue family admits the required movement, these are not unrelated columns that happen to share a label. They are members of one governed measure family.

A frame assembles fields at one output anchor; in the fully governed case, every field is a member. The query above returns customer and month as the frame's coordinates, together with the requested revenue member at that same anchor. A served frame may also carry explicitly labeled provisional fields; their status rides the result annotation (see Section 5.2).

A physical column may realize one member. It is not the atom itself. The same member may be obtained from a normalized table, a wide analytical table, a materialized aggregate, a cached sufficient state, an event stream, or an API. Conversely, a physical column does not become a governed member merely because it contains plausible values. Atom membership depends on the member contract and the atom's family law, not on storage shape.

## 2.1 An anchor is necessary, but not always sufficient

The output anchor tells the system where the requested member must live. It does not always determine which member is intended.

Inventory level at store-month might mean the opening level, closing level, maximum observed level, or an average of observations. Those results share an output anchor but differ in operator, input grain, order, participation, and analytical identity.

The same issue appears in a mean. Consider:

```frameql
SELECT avg(aov)
AT {customer}
```

The statement parses, but it does not determine what instances of average order value are being averaged. Daily values, monthly values, and transaction-level values define different statistics.

Frame-QL can make the input explicit:

```frameql
SELECT avg(aov @ {customer, cal.day}) AS typical_day_aov
AT {customer}
```

Here `AT {customer}` declares the final output anchor. The inner `@ {customer, cal.day}` is an anchor ascription in input position; in this example, it pins the customer-day values that feed the outer average.

The distinction is structural. `AT` appears once and declares the output anchor of the frame. `@` ascribes an expression in input position. Depending on context, the governed planner may realize an ascription through aggregation, broadcast, or identity. Its most important role in this introduction is to make a grain-sensitive intermediate expression determinate.

A concise query is therefore not permission to guess. Omission is lawful only when the Manifold makes the missing choice unique.

# 3. Why output declaration is possible

A language can ask only for the result when some other part of the system already knows enough to derive the process.

That role belongs to the Manifold.

A Manifold is a versioned governed environment for analytical objects. It contains the declarations needed to identify those objects and adjudicate the class of transformations the system supports. For an atom such as revenue, the Manifold may record:

- the stable atom identity and its root member;
- value type, units, anchor, universe, eligibility, and observed support;
- default and alternative operator subfamilies;
- sufficient state required for exact composition;
- movements that preserve the atom's identity;
- movements that require a different atom or do not close;
- relationship functionality, assignment, allocation, and conservation rules;
- observation conditions, evidence, and lineage;
- physical bindings through which members may be realized.

This is more than a dictionary from business names to SQL snippets. A SQL expression describes one procedure for constructing values. A Manifold describes the governed analytical object those values are intended to realize and the laws under which other members may be derived.

Suppose revenue is first served from normalized transaction tables. Later, the organization introduces a lakehouse, a customer-month materialization, a cache, or an accounting service. The execution plan may change substantially. The analytical request can remain unchanged:

```frameql
SELECT revenue
AT {customer, cal.month}
```

The name and requested anchor remain stable because they belong to the analytical model rather than to one storage layout.

The claim should remain ambitious and bounded:

> **A Manifold captures the declared governance information required to identify its analytical objects and adjudicate the class of transformations the system supports.**

It does not contain every fact a human could know about a business. It does not solve unrestricted natural-language interpretation, causal inference, or every future analytical method. When a required law has not been declared, the system must expose the gap rather than replace it with a familiar processing convention.

# 4. Analytical identity is independent of storage

Rows, tables, schemas, and joins remain useful. They are powerful forms of representation and execution. Frame-QL does not deny their existence; it places them on the other side of the request boundary.

A physical carrier answers:

> Where can the system obtain these values?

A member contract answers:

> What analytical object do these values realize?

Frame-QL addresses the second question. The trusted planner and engine own the first.

This separation matters most where a physical operation leaves analytical meaning underdetermined.

Suppose a product can belong to several categories. The product-category relationship identifies possible matches. It does not decide what should happen to product revenue. Revenue might deliberately appear in every category, be assigned to one primary category, be allocated across categories by weights, remain at product grain for filtering, or be unavailable for category aggregation until a passage rule is supplied.

Those are different analytical meanings. They are not alternative implementations of one self-explanatory join.

A trusted engine may eventually use a join to realize a declared passage. But the query author does not create analytical law by selecting a join type. The Manifold must already contain the applicable movement rule, or the request remains incomplete.

The same distinction applies to grouping. `AT {customer, cal.month}` declares the output location. The engine may use grouping to realize that location, but `GROUP BY` is not how the requester defines the member. It is one possible operation in a physical plan derived after the analytical request has been resolved.

SQL therefore remains important without becoming the request language of governed identity:

> **SQL is declarative about relational processing. Frame-QL is declarative about governed analytical identity.**

Frame-QL is not shorter SQL, a SQL dialect, a query builder, or a logical-plan language. SQL may be generated after the requested members have been resolved and the plan has been certified.

# 5. What the statement declares

The full Frame-QL envelope contains more syntax than this introduction needs to teach. Four elements carry the governing idea.

## 5.1 FROM selects the governed environment

```frameql
FROM retail_manifold
SELECT revenue
AT {region}
```

`FROM` names a Manifold, not a physical table. It selects the governed environment against which names, anchors, universes, family laws, evidence, and physical bindings are resolved. On a surface already bound to one Manifold, the clause may be supplied by the surface; the resolved Manifold identity still travels with the result annotation.

## 5.2 SELECT names or constructs output series

```frameql
SELECT revenue, order_count
AT {region, cal.month}
```

A bare name resolves to an atom and requests a member at the query's output anchor when the applicable family and path are uniquely determined.

A map expression can construct a different analytical quantity:

```frameql
SELECT (revenue / order_count) AS average_order_value
AT {region, cal.month}
```

The expression is syntactically valid, and `AS average_order_value` gives the output field a stable name. The alias does not, by itself, mint or prove an atom. The result is a governed member of an `average_order_value` atom only if the Manifold and certification layer can establish a complete output contract and bind the expression to that identity. Otherwise the values may remain a provisional field whose status is explicit.

This distinction prevents a familiar name from doing more work than the declarations support.

## 5.3 AT declares the output anchor

```frameql
SELECT revenue
AT {customer, cal.month}
```

`AT` applies to the whole query. Every selected series must be realized at that one output anchor so that the result forms a coherent frame. The anchor coordinates appear as leading columns of the frame; they are not repeated in `SELECT`.

This is why the language does not need `GROUP BY` at the request surface. The requester has already stated the analytical location of the result.

## 5.4 Conditions shape the requested frame

```frameql
FROM retail_manifold
SELECT revenue
AT {customer, cal.month}
WHERE order_status = "completed"
```

The condition restricts the inputs from which the requested member is derived. It does not expose a scan plan. The planner determines how the predicate reaches each series, whether the required dimensions are available from its root member, and how the restriction affects population and support.

Other clauses similarly describe the requested result: post-result conditions, ordering, and limits apply to the frame. They are not steps in a user-authored execution pipeline.

# 6. From declaration to governed realization

The brevity of the query does not mean the system performs little reasoning. It means the reasoning has been centralized.

For the revenue request, the planner first resolves the name to a versioned atom in the selected Manifold. It identifies the root member, the relevant operator subfamily, the population, and the candidate path to the requested anchor.

It then determines the member being requested. The output anchor, any input ascriptions, conditions, order, and participation rules must jointly identify one analytical result. When several lawful members remain possible, the declaration is incomplete.

Next comes the identity judgment. A lawful reduction from transaction revenue to customer-month revenue may produce another member of the same revenue atom. A ratio of revenue to order count may produce a member of a different average-order-value atom if a complete new contract is established. A calculation may also produce values without closing as a governed member of any atom.

The certification layer checks the obligations represented by the supported calculus and the Manifold declarations. Depending on the request, those obligations may concern value types, anchors, universes, support, sufficient state, order, multiplicity, allocation, observation conditions, contract-inheritance boundaries, evidence, authorization, and faithfulness to the ask.

These obligations are not an aspirational checklist. A growing fragment of them is backed by machine-checkable theorems in the Theory's formal companion: within that fragment, a result can be proved evaluable, deterministic under every execution schedule, and still not the analytical object it claims to be. That separation — computable versus entitled — is the specific guarantee this architecture adds over a conventional semantic layer, and the kernel that decides it is small enough to inspect and trust.

Only after that analytical work does the engine construct or select a physical plan. The plan may contain joins, grouping, windows, scans, cache reads, materialized aggregates, or backend-specific SQL. Those operations are real, but they are engine-owned consequences of the declaration rather than instructions authored by the requester.

The result can therefore carry more than values. Its annotation can record the resolved Manifold, atom and member identities, anchors and universes, canonical query, evidence state, disclosures, and lineage relevant to the served frame.

`EXPLAIN` makes the interpretation visible without executing the data request:

```frameql
EXPLAIN
FROM retail_manifold
SELECT revenue
AT {customer, cal.month}
```

For a person, this exposes how the statement was resolved. For an agent, it creates a propose-validate-refine loop before warehouse work begins.

# 7. The language does not silently choose another meaning

The distinction among atom, member, and field gives Frame-QL a precise way to handle transformations.

## 7.1 Member closure

A lawful transformation may produce another member of the same atom:

```text
transaction revenue -> customer-month revenue
```

This is member closure. The output changes analytical location while preserving the revenue identity under the revenue atom's family law.

## 7.2 Atom synthesis

A transformation may create a different analytical identity:

```text
revenue / order count -> average order value
```

This is atom synthesis only when a complete output contract is established for the new atom and its member. The formula and output alias alone are not sufficient.

## 7.3 Non-closure

A transformation may produce computable values without producing a complete governed identity. Summing inventory levels through time, for example, does not remain within the inventory-level atom. It could become a different exposure or observation-summary atom under an explicit contract. Without that contract, the output is non-closing even if the arithmetic is executable.

These three outcomes separate computation from governed identity. All may appear physically as numeric columns. Their analytical status is different.

The same discipline applies when the request itself is underdetermined. An unpinned mean may admit several members. A many-to-many relationship may admit several passage laws. Two series may share coordinate labels while belonging to different universes. Frame-QL does not convert those gaps into hidden choices.

The result contract can therefore serve a fully governed frame (one whose fields are all members), serve it with disclosures, request clarification, or refuse execution where no result can or may be produced. The important point is not the vocabulary of the four outcomes. It is that ambiguity, evidence, and governance are part of interpretation rather than after-the-fact commentary on generated SQL.

One clarification prevents a misreading across the paper family: non-closure is an identity judgment, not a serving decision. Whether a non-closing number is served with disclosure, returned for clarification, or withheld is the system's declared policy. The Theory determines status; policy determines presentation.

# 8. Frame-QL as the AI intent boundary

AI agents make this division of responsibility especially useful.

A language model is well suited to interaction. It can converse in the user's vocabulary, search a governed model, identify candidate atoms, compare plausible readings, ask for missing domain judgment, propose a Frame-QL statement, and explain the resolved result.

It does not need database credentials or authority to write executable SQL.

The intended path is:

```text
user question
    -> AI interpretation
    -> Frame-QL declaration
    -> Manifold resolution and certification
    -> engine-owned physical plan
    -> governed frame
```

Each component keeps a distinct responsibility.

The user supplies the analytical need and domain judgments that cannot be derived.

The model searches language and possible interpretations.

Frame-QL records the proposed output in a constrained formal language.

The Manifold supplies governed identities and laws.

The certification layer adjudicates the supported obligations.

The engine owns credentials, cost controls, physical bindings, executable commands, and execution.

This is not merely post-generation SQL validation. In a guardrailed text-to-SQL system, the model authors an executable command and another component attempts to reject unsafe or unacceptable commands. In the Frame-QL architecture, the model does not author the final command. It proposes a governed result declaration from which trusted components derive the plan.

Operational controls remain necessary: access control, budgets, timeouts, auditing, and ordinary database security do not disappear. The narrower architectural gain is that model output is not the final authority over either analytical meaning or database behavior.

Clarification also becomes productive rather than exceptional. When the planner reports that a mean lacks an input anchor, the agent can ask what units should be averaged. When a category passage requires assignment or allocation, it can explain the alternatives in domain language. When no requested atom exists, it can distinguish a vocabulary mismatch from a request to define a genuinely new analytical identity.

The model remains an interpreter and searcher. The governed system remains the authority.

# 9. What changes when the output is the query

Once the requested output becomes the unit of declaration, several responsibilities move to more appropriate places.

Analytical knowledge moves out of individual queries and into governed atom and member contracts. The relationship among measure, population, anchor, operator family, sufficient state, passage law, and evidence is declared once rather than reconstructed by every query author.

Plan ownership becomes explicit. The requester owns the analytical intention. The governed planner owns member derivation. The trusted engine owns physical realization.

Requests become more stable. A statement that names analytical identity can survive changes in schemas, tables, materializations, and backends so long as the Manifold preserves the governed object and supplies a valid binding.

Results become more self-describing. A frame can carry its resolved member identities, anchors, universes, Manifold version, canonical declaration, evidence conditions, disclosures, and lineage together with its values.

Failures become more precise. The system can distinguish an unknown name from an ambiguous member, a blocked same-atom derivation from a possible new atom, a cross-population expression from a lawful juxtaposition, and a computable field from a governed result.

These are not incidental benefits of shorter syntax. They follow from changing what the query is allowed to mean.

## Scope

Frame-QL is one executable language built against the Theory of Data. The Theory is broader than the current language, and the language is broader than any one backend.

The current implementation supports a defined grammar, operator set, and outcome contract. Some theoretical distinctions remain outside the shipped surface or require further formal work. This introduction does not promote planned syntax to implemented behavior, and it does not claim that every analytical question can already be resolved.

The Frame-QL Manual, Second Edition is authoritative on syntax, canonical form, operators, outcomes, and version-specific behavior. It is distributed with the public Columna repository, and every Frame-QL example in it is verified against the running parser rather than written from memory. The canonical Theory of Data is authoritative on atoms, members, frames, lawful transformation, and certification.

# 10. Closing perspective

Frame-QL begins from a simple consequence of governing data independently of storage.

Revenue is not exhausted by one physical column at one grain. It is a governed atom whose lawful members may exist at transaction, customer-month, region-quarter, or other declared analytical locations. A frame assembles the fields requested at one output anchor.

Once a Manifold records those atoms, root members, family laws, populations, boundaries, evidence, and bindings, the requester no longer needs to reproduce the production procedure. The requester names the atoms, declares the output anchor, and states the conditions. The governed system determines whether the members are identified, whether their derivations close within an atom, whether a different atom can be synthesized, and which physical plan may execute.

That is why Frame-QL contains no query-time joins and no `GROUP BY`. Their absence is not a denial of relational execution. It marks the abstraction boundary between analytical declaration and physical realization.

For an AI agent, the consequence is equally direct. The model can interpret, search, clarify, and propose. It need not own analytical law, database credentials, or executable commands.

The frame is the query because the frame is the thing the requester wants.

---

## References

Wang, Huayin. 2026. *The Theory of Data: Governed Analytical Objects, Lawful Transformation, and Certification*. Version 3.1. datumwise. DOI: [https://doi.org/10.5281/zenodo.21760008](https://doi.org/10.5281/zenodo.21760008)

Wang, Huayin. 2026. *The Frame-QL Manual*. Second Edition. datumwise. Documentation of columna-core 0.14.0, distributed with the public Columna repository. https://github.com/datumwise/columna
