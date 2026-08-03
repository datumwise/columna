---
title: "The Theory of Data: An Introduction"
subtitle: "Analytical Meaning, Lawful Transformation, and Governed Results"
author: "Huayin Wang"
date: "2026-08-02"
lang: en-US
geometry: margin=0.82in
fontsize: 11pt
papersize: letter
---

**datumwise, an independent open-source research project**

**Version 1.1**

**Keywords:** Theory of Data; analytical identity; measure; member; frame; Manifold; lawful transformation; certification; Frame-QL; SQL; AI-assisted analytics

---

## Abstract

The Theory of Data begins from a distinction that analytical systems often leave implicit: producing values is not the same as establishing what governed analytical object those values represent.

The Theory describes analytical data independently of its current physical storage. A **datum** is one typed value at one analytical location. A **member** is one governed realization of a measure at a particular anchor in a particular universe. A **measure** is the stable governed family whose laws determine which members share one analytical identity. A **frame** is an assembly of co-anchored fields, each carrying its own status; a fully governed frame is one whose fields are all members.

This ontology makes three transformation outcomes explicit. A calculation may derive another member of the same measure, synthesize a member of a different measure, or produce a useful field without establishing a complete governed identity. Transaction revenue reduced to customer-month revenue may remain within the revenue measure. Revenue divided by order count may synthesize average order value. Inventory levels summed through time may produce numbers without producing another inventory-level member.

A **Manifold** records measures, root members, universes, anchors, family laws, observation rules, evidence, lineage, and physical bindings. It also records the conditions under which supported transformations are admitted. A requester can therefore declare a desired frame while a planner derives candidate members, a trusted kernel certifies the obligations it supports, and an execution engine realizes the admitted plan through SQL or another backend.

The central claim is not that every business fact can be formalized or that every analytical question can be answered automatically. It is narrower and more operational: the governance information required to identify analytical objects and adjudicate a supported class of transformations can be represented systematically, checked where the calculus is defined, and carried with the result.

This paper is the accessible introduction. The canonical Version 3.1 manuscript contains the full definitions, claim-status distinctions, formal scope, and open research program.

---

## About this introduction

The Theory of Data is a proposal about the foundation of analytical systems.

It is not primarily a catalogue of analytical mistakes, a style guide for SQL, or a list of governance practices. It asks what analytical data must be so that meaning, transformation, and reuse can be governed systematically.

The paper uses several familiar expressions as teaching bridges:

| Familiar expression | Formal expression | Important qualification |
|---|---|---|
| value at a key | datum | the key is a complete typed analytical point |
| column at one grain | member | the column realizes the member — one realization, not the whole measure identity |
| measure | measure | stable governed family of lawful members |
| grain or analytical location | anchor | typed coordinate structure, possibly with logical order |
| population | universe | governed population together with an existence law |
| requested result table | frame | coherent assembly of co-anchored fields |

The familiar terms remain useful. The distinctions matter because physical words such as *column*, *table*, *key*, and *join* often combine several analytical objects that need to be governed separately.

# 1. An analytical request asks for data, not a production procedure

Suppose a person asks for revenue by customer and month.

The request appears simple. Yet in an ordinary workflow, answering it may require someone to know which physical revenue field is authoritative, which records belong to the relevant population, which date determines the month, how customers are identified, whether returns are included, which relationship path is valid, whether a join duplicates revenue, and whether a monthly materialization can be reused.

The person asked for a result. The analyst is often required to supply both the result and the procedure that produces it.

This coupling feels natural because analytical systems expose storage and processing structures directly. The analyst sees rows, tables, schemas, joins, filters, and aggregations, so the question is translated into operations over those objects.

But the requested object is not a join plan. It is revenue, realized for each customer-month point in a particular population under a particular interpretation.

That observation leads to the Theory's first separation:

> **What the data is should be represented independently of how the data is currently stored and processed.**

The physical system may still use tables, joins, indexes, files, dataframes, caches, APIs, and generated SQL. The Theory does not deny those objects. It places them on the implementation side of the boundary.

The analytical side needs a stable account of the requested measure, its location, its population, its observation conditions, the transformations that preserve its identity, the transformations that create another identity, and the evidence supporting those declarations.

Once that account exists, the request can remain about the answer.

# 2. Analytical identity is not physical form

A physical table can carry many different kinds of analytical objects. A decimal column may represent revenue, inventory level, exchange rate, temperature, probability, or an identifier encoded as a number. Two columns with the same physical type may obey different analytical laws. Two columns with different physical representations may realize the same analytical object.

Customer-month revenue might be obtained from transaction rows, a monthly aggregate table, a dataframe, a cache, or an accounting service. A change in physical source should not silently change what customer-month revenue means.

The Theory therefore does not begin with `ROW`, `TABLE`, `SCHEMA`, or `JOIN` as analytical primitives. Rows and tables organize carriers. Schemas describe physical structure. Joins match representations. These are indispensable implementation concepts, but they do not by themselves establish the analytical identity of the values they carry.

The Theory begins with values at analytical locations and builds upward.

## 2.1 Datum

A **datum** is one typed value at one typed analytical point.

```text
(customer = C17, month = 2026-07) -> USD 420
```

The datum is not merely the number `420`. Its analytical content includes the nominal value type and the point at which the value is defined. A database key may implement that point, but a particular primary-key layout does not define the analytical location.

## 2.2 Member

A **member** is one governed anchored realization of a measure family.

Customer-month revenue is one member. Transaction revenue is another. A member has more than values. Its contract includes a measure identity, an output anchor, a universe, participation and coverage conditions, observation behavior, sufficient state, boundaries, evidence, and lineage. Ordered or approximate members carry the corresponding additional contracts.

A physical column may realize one member. It is not the measure itself, and it is not automatically a governed member merely because it has a stable name. A column can mix populations, locations, or observation states; its physical type may be too weak; or the system may not know which transformations preserve its identity.

## 2.3 Measure

A **measure** is a stable governed family.

`revenue` is a measure. Its members may include transaction revenue, customer-month revenue, store-day revenue, and region-quarter revenue.

Those members share one analytical identity only when the family law admits the relevant derivations and the required value, population, support, multiplicity, boundary, and evidence conditions are satisfied.

The measure therefore owns more than a metric label. It owns the laws that determine which anchored realizations remain members of the same measure family.

> **The measure is not one column at one grain. A column may realize one member of the measure.**

## 2.4 Frame

A **frame** is a coherent assembly of fields at one declared output anchor.

A frame at `{customer, month}` might contain customer-month revenue, customer-month order count, and customer-month average order value. The fields are co-anchored, but they need not belong to the same measure or share the same transformation family.

A physical table can represent such a frame. It can also represent an incoherent mixture of values that merely happen to occupy adjacent columns. Co-location is a presentation and execution fact. It does not establish composability.

# 3. One measure can have many members

The measure-member distinction explains how a measure can remain stable while its analytical location changes.

Consider transaction revenue:

```text
revenue at {transaction}
```

Suppose each transaction belongs to one customer and one calendar month, the relevant mappings are functional, and the revenue family admits additive reduction over those movements. The system may derive:

```text
revenue at {customer, month}
```

The output is not a new measure merely because its values now live at a different anchor. It is another member of the revenue measure.

The transformation changed the member while preserving the measure. This is **member closure**.

The same idea applies to non-additive families. A daily inventory-level member may yield a month-end inventory-level member through a `last` subfamily when the logical order, participation rule, support, and boundary conditions are satisfied. The member changes; the measure family remains inventory level.

## 3.1 A requested anchor does not always determine a member

For revenue, a declared default additive subfamily may make the following conceptual request determinate:

```text
revenue at {customer, month}
```

For inventory level, the same form is generally incomplete:

```text
inventory_level at {store, month}
```

The intended monthly member could be first, last, maximum, average observed level, or another governed interpretation. The output anchor identifies where the values should exist. It does not by itself identify which family law produces them.

A fully resolved member may require the measure, operator subfamily, output anchor, universe, participation or coverage policy, logical order, and approximation contract. A system may omit a field from the surface request only when the Manifold resolves it uniquely and records whether the field was supplied by the requester or selected by a declared default.

This is not verbosity for its own sake. A short request is precise when the omitted information is recoverable without an unrecorded choice.

## 3.2 A member is not its derivation path

A measure family may admit more than one route to the same analytical member.

Revenue might move from day to quarter directly, or from day to month and then from month to quarter. When both routes preserve the required sufficient state and resolve to the same canonical identity, they should not create two competing quarter-revenue members.

The Theory therefore separates **member identity** from **certificate history**.

The member's identity is determined by the stable analytical facts that define the requested realization: the measure, admitted family, output anchor, universe, participation and coverage policy with its referent, and any required order or approximation contract. The input anchor, physical route, evidence chain, and lineage describe how a particular certificate reached that member. They do not multiply the member merely because the path differs.

This distinction matters operationally. A direct derivation and a staged derivation may identify one member while carrying different lineage or different evidence strength. The serving system may prefer the stronger certificate without pretending that it discovered a different measure.

The equivalence is not automatic. A staged calculation must preserve the state required for continued composition. If a monthly mean is materialized only as a displayed scalar and its `(sum, count)` state is discarded, averaging those monthly values is not a lawful staging of the original mean. It is another derivation with another interpretation.

Likewise, a coverage label is incomplete without its referent. "Complete over eligible days" and "complete over eligible months" are different claims even when both are spelled `Complete`. Structural transformation either preserves the referent through state-disciplined staging or establishes a new indexed permission.

The principle is compact:

> **One analytical member may have several certificates, but two derivations count as the same member only when their canonical contracts agree.**

# 4. Transformation has three possible identity outcomes

Analytical systems often treat every successful expression as another reusable column. The Theory separates evaluation from analytical identity.

## 4.1 Same-measure member closure

A lawful transformation may produce another member of the same measure:

```text
transaction revenue
    -> customer-month revenue
```

The system must establish that the revenue identity survives the movement. Numeric addition is not enough. Population, eligibility, support, multiplicity, sufficient state, capability boundaries, and family law must agree.

When they do, the result may re-enter later governed transformations as revenue.

## 4.2 New-measure synthesis

A transformation may establish a different analytical identity:

```text
revenue / order_count
    -> average_order_value
```

Average order value is not a member of the revenue measure or the order-count measure. It belongs to another measure.

Creating it requires more than naming an expression. The system needs a complete output contract: value type, anchor, universe, denominator-zero policy, participation and support behavior, sufficient state for later composition, boundaries, evidence, and lineage. An output alias may name the field; it does not create or prove the measure.

The same pattern applies to transformations such as:

```text
revenue - cost -> profit
inventory_level * duration -> inventory_exposure
```

They may synthesize new measures when complete contracts and admitted synthesis laws exist.

## 4.3 Non-closure

A calculation may be executable without producing a governed member of either an existing measure or a new one.

The familiar example is inventory summed through time:

```text
sum of daily inventory levels
```

The arithmetic returns a number. The number is not another inventory level. It may become inventory exposure or a recorded-observation summary under a separate synthesis contract. Until then, it is a provisional or terminal field rather than a governed member.

The field may still be displayed, exported, inspected, or used under an explicit provisional status. What it does not receive automatically is governed composability.

> **Successful evaluation answers whether values can be produced. Closure answers what governed analytical object, if any, has been produced.**

## 4.4 Sufficient state belongs to the family law

A displayed value may contain less information than its family requires for exact continuation.

A mean is one scalar. Exact recombination generally requires at least `(sum, count)`. Averaging subgroup means does not reconstruct the overall mean unless the required weighting state is preserved.

This is not merely advice about avoiding "mean of means." It is part of the measure's law. The law states which state is sufficient, how it combines, when finalization is valid, and whether a finalized display value remains fertile — retains the state its family requires — for later transformation.

The same distinction appears in distinct counts, rates, quantiles, sketches, coverage-aware reductions, and ordered selections. The result's right to continue through the system depends on the state and contract it carries, not only on the scalar displayed to a user.

# 5. The Manifold gives analytical governance a home

Analytical knowledge is often distributed across SQL, semantic models, tests, dashboards, wiki pages, lineage systems, conventions, and the memory of experienced analysts.

The knowledge is real. The difficulty is that it is rarely represented as one coherent object from which a system can derive analytical consequences.

A **Manifold** provides that governed environment.

For the supported analytical domain, it can record:

- stable measure identities and vocabulary;
- root member contracts and originated physical bindings;
- value types, units, and typed operations;
- universes, eligibility, and observed support;
- anchors, hierarchy maps, and logical order;
- operator subfamilies and sufficient state;
- participation, coverage, and approximation policies;
- relationship functionality, assignment, allocation, and fan-out rules;
- capability-resolved inheritance boundaries;
- evidence, lineage, and versioned physical realizations.

The Manifold is not merely a metric name attached to a SQL expression. A SQL expression states how values can be constructed under one physical arrangement. A measure declaration states what analytical identity the values belong to, which members may be derived, what conditions preserve that identity, and which transformations establish another identity.

The SQL may change while the member remains stable. Conversely, identical SQL text may support different analytical claims under different populations, observation rules, or family contracts.

## 5.1 Physical binding does not create a second identity

A member may be derived from a root contract, or it may already exist as a governed materialization, cache, service response, or independently computed pipeline. When the current supported calculus cannot derive a member at that identity, an adjudicated binding may supply it under an explicit adequacy premise.

A physical binding should not create a second analytical member merely because it arrived through another implementation route. If an equivalent member is derivable, the binding attaches evidence, lineage, and a physical access path to that member class.

If a bound realization conflicts with a derivable member at the same identity, the conflict must be surfaced and the governed binding rejected. The values may be retained separately under an explicitly provisional status, but the system may not preserve a single member identity while allowing incompatible contracts to occupy it.

This is the same identity principle applied at the physical boundary: one member may have several realizations and certificates, but an implementation does not redefine the measure by being convenient.

## 5.2 Evidence is part of the result

The Theory does not claim that all governance declarations are proved from data.

Some conditions can be checked directly: key uniqueness, hierarchy functionality, exact weight normalization, observed coverage, or conservation in a supported fragment. Some can be corroborated but not fully established from finite observations, such as long-run mapping stability. Some remain explicit assumptions, including many intended-population and policy judgments.

These statuses should not be collapsed into one boolean called "valid." Evidence travels with the declaration and with the certificate that depends on it.

A contradicted premise cannot support a governed lawful result. The system may still produce a provisional or disputed field where policy permits, but it must not silently upgrade contradiction into governed closure.

This makes governance executable without pretending that judgment or uncertainty has disappeared.

# 6. Certification connects the broad theory to the proved kernel

The Theory is broader than the current formal calculus. That breadth creates a responsibility: the family layer may add interpretation, but it may not override the rules proved for a supported fragment.

Where a transformation is representable in the contract calculus, the broad same-measure transformer must factor through fragment certification. If the fragment refuses the local transformation because a boundary is spent, coverage is unsupported, eligible totality fails, weights are inexact, or another stated side condition is not met, the family law cannot license the same movement by assertion.

This is **projection coherence**.

The broad member contract contains more than the local fragment contract. It may carry measure identity, observation-process declarations, evidence, and lineage that the fragment suppresses. But the extension is non-interfering: it may enrich the certified result; it may not alter the local components the fragment has already adjudicated.

The asymmetry is deliberate:

- the kernel may certify a local value-and-contract transformation that the family declines to classify as a member;
- the family may not certify a governed member whose local projection the kernel refuses.

The first case is a locally certified but family-unclassified output. It may be useful, but it has not closed as a member of the measure. The second case would allow the broad ontology to bypass its own proved safety layer and is therefore disallowed.

Capability-resolved boundaries support the same rule. A boundary attaches to the underlying analytical capability, not merely to one operator spelling. Renaming `sum`, wrapping it in a subfamily, or registering an alias cannot make a blocked movement lawful. Member-level boundaries may strengthen the family floor; they may not weaken it except through a separately registered transformer that produces a new member under a new contract.

The claim-status architecture keeps this account honest. Some statements in the program are definitions. Some are proved in the finite fragments. Some are design constraints or framework propositions. Others remain adequacy premises, implementation policies, or open problems. The Theory's ambition depends on preserving those differences rather than presenting every intended property as an accomplished theorem.

# 7. Querying becomes declaration of a frame

Once measures and their family laws are represented independently of storage, the query interface can change.

Instead of telling the system how to manipulate rows, the requester can declare which members should appear in the output frame.

Frame-QL is one language built on this consequence:

```frameql
FROM retail_manifold
SELECT revenue, order_count
AT {customer, cal.month}
```

The statement requests the customer-month members named `revenue` and `order_count` from `retail_manifold`.

It does not name tables, join keys, `GROUP BY`, or an execution sequence. The Manifold resolves the requested analytical identities. The planner searches for candidate derivations or governed bindings. The certification layer adjudicates the supported obligations. The execution system produces SQL or another physical plan only after the analytical request has been resolved.

This is not merely shorter SQL.

SQL is declarative about relational processing. Frame-QL is declarative about governed analytical identity.

The languages occupy different layers. SQL may remain the execution language behind the boundary. Frame-QL states the frame to be produced. The language's normative reference is its Manual, distributed with the public Columna repository, where every example is verified against the running parser rather than written from memory.

## 7.1 Output declaration is sufficient

The requester does not need to restate information already governed by the Manifold: where revenue is stored, which hierarchy edge realizes month, which additive state is required, which materialization may satisfy the member, or which physical keys implement the path.

Omission is safe only when the omitted information can be resolved uniquely or through a declared default whose use is recorded in the certificate.

## 7.2 Output declaration is also a limit of authority

The same boundary prevents a requester or planner from overriding analytical law with a plausible procedure.

A surface request cannot silently choose an undeclared many-to-many interpretation, replace one universe with another, select a physical first when a logical first is required, weaken a capability boundary through an alias, or turn a provisional field into a governed member by assigning an output name.

The user declares the desired analytical object. The governed system owns the derivation, certification, physical binding, and execution authority.

# 8. AI belongs at the intent boundary

This architecture creates a natural role for AI agents.

A language model can interact with a person, resolve vocabulary, identify several plausible readings, search a declared analytical environment, and propose a formal request. It can ask whether "monthly inventory" means last observed level, end-of-period level, maximum, average, or exposure. It can explain why product-category revenue requires a declared assignment or allocation rule.

The model is not the final authority over analytical law, physical access, or execution.

The division of responsibility is:

```text
person states an analytical need
    -> AI proposes a resolved frame request
    -> the Manifold identifies measures and candidate members
    -> the trusted kernel certifies supported obligations
    -> the engine binds sources and executes the admitted plan
    -> the result returns with identity, conditions, evidence, and lineage
```

Probability may search the space of interpretations. It must not decide that ambiguity is a number.

The agent does not need database credentials, permission to invent joins, or authority to certify its own SQL. Its role is interpretation and proposal. The governed environment adjudicates the result.

# 9. What the current program establishes - and what it does not

The Theory of Data is both a framework and a research program.

The accompanying Contract Calculus proves results for finite fragments. The current chain covers total member contracts and inherited movement boundaries; finite population, eligibility, observed support, and coverage-aware state; and declared relation expansion with replication, assignment, exact allocation, and fan-out refusal. Within those fragments, the work includes syntax-directed certification, determinacy, staging agreement under sufficient state, boundary soundness, decidability bounds, and explicit separation between evaluable results and governed closure.

The practical meaning of that chain is worth stating plainly: within the supported fragments, "this number is deterministic, plausible, and not the thing it claims to be" is a machine-checkable verdict, not a reviewer's opinion.

The broad Theory is larger than those proofs. Projection coherence states how the family layer must respect the fragments where they apply. It does not turn the unproved remainder into a theorem.

Several limits remain important.

The current measure model begins from a single root member. That is a genuine scope restriction. An enterprise measure such as revenue may originate from billing, point-of-sale, and partner systems. Reconciling several roots into one governed family requires additional identity, equivalence, and evidence rules.

The proved population fragment is strongest for image-generated universes. Independent spine universes - expected store-days, registered customers, contractual reporting periods - require the next population extension. Richer observation-process transport, non-thin hierarchy structures, partial ordered reducers, approximation composition, and a complete evidence calculus also remain open.

General natural-language faithfulness is not solved. A system can make more of the interpretation explicit, represent unresolved identity fields, record defaults, and ask targeted clarifying questions. It cannot prove that every human utterance has one recoverable formal meaning.

These limits are not peripheral disclaimers. They are part of the Theory's method: a governed system must distinguish what is defined, what is proved, what is declared, what is assumed, and what remains open.

# 10. The change in perspective

The Theory of Data changes the starting point of analytical system design.

The ordinary starting point is the container. Data is presented as rows and columns, and analytical meaning is reconstructed through conventions surrounding those structures.

The Theory begins with analytical identity.

A typed value at an analytical point is a datum. A governed anchored realization is a member. A stable family of lawful members is a measure. A coherent requested assembly is a frame.

Transformations are judged not only by whether an engine can execute them, but by their identity outcome. A transformation may preserve a measure by deriving another member, establish a different measure through synthesis, or produce a field that remains provisional or terminal.

Different derivation paths do not automatically create different members. When their canonical contracts agree and the required continuation state is preserved, they are certificates for one analytical object. Physical materializations attach to that object when their contracts agree; they do not redefine it.

A Manifold gives those objects and laws a governed home. The proved kernel checks the fragment it claims to support. The family layer may add interpretation but cannot bypass local refusal. The requester declares the desired frame. SQL and other physical languages remain behind the boundary.

AI can participate without becoming the authority over data meaning or database execution. It can translate intention into a proposal and return to the user when the proposal is ambiguous. Certification remains deterministic relative to the declared environment.

This is not a proposal to discard databases, SQL, statistics, dimensional models, semantic layers, tests, lineage systems, or human judgment. Those systems continue to perform essential work. The Theory supplies a distinct foundation beneath and across them: an account of the analytical objects they store, calculate, test, name, bind, and move.

The core vision is compact:

> **Separate analytical identity from physical storage. Represent measures as governed measure families. Treat their anchored realizations as members. Request coherent frames. Derive and certify the process behind the boundary.**

---

## Introductory glossary

| Term | Meaning in the Theory |
|---|---|
| **Datum** | One typed value at one typed analytical point |
| **Series** | A homogeneous typed binding of datums over one anchor; the shape, prior to governance |
| **Member** | One governed anchored realization of a measure family |
| **Root member** | The originated member from which same-measure derivations begin in the current model |
| **Measure** | Stable governed family and the laws of its members |
| **Anchor** | Typed analytical coordinate structure at which a member exists |
| **Universe** | Governed population together with its existence law |
| **Operator subfamily** | A named family of admitted operations, state, movement, boundaries, and output rules |
| **Canonical member identity** | Path-independent analytical identity used to determine whether derivations denote the same member |
| **Certificate** | Evidence, lineage, resolved defaults, and adjudicated obligations supporting one realization or derivation |
| **Member closure** | Lawful derivation of another member of the same measure |
| **Measure synthesis** | Establishment of a member of a different measure under a complete new contract |
| **Non-closure** | Production of values without complete same-measure closure or new-measure synthesis |
| **Frame** | Coherent assembly of fields at one declared output anchor |
| **Manifold** | Versioned governed environment containing measures, laws, evidence, and physical bindings |
| **Projection coherence** | Requirement that the broad family layer cannot admit a transformation rejected by an applicable proved fragment |

---

## References

Wang, Huayin. 2026. *The Theory of Data: Governed Analytical Objects, Lawful Transformation, and Certification*. Version 4.0. datumwise. DOI: [https://doi.org/10.5281/zenodo.21774032](https://doi.org/10.5281/zenodo.21774032)

Wang, Huayin. 2026. *A Contract Calculus for Governed Analytical Transformation: Totality, Partiality, Population, Expansion, and Fan-Out*. Version 1.0. Zenodo. DOI: 10.5281/zenodo.21752373.

Wang, Huayin. 2026. *Technical Supplement Collection for A Contract Calculus for Governed Analytical Transformation*. Version 1.0. Zenodo. DOI: 10.5281/zenodo.21752681.

Wang, Huayin. 2026. *The Frame-QL Manual*. Second Edition. datumwise. Documentation of columna-core 0.14.0, distributed with the public Columna repository. https://github.com/datumwise/columna
