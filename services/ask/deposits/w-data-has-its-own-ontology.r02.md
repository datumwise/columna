---
title: "Data Has Its Own Ontology"
subtitle: "Not Borrowed from the World It Describes"
author: "Huayin Wang"
date: "Version 1.1 - 20 August 2026"
version: "1.1"
doi: "10.5281/zenodo.22026962"
license: "CC BY 4.0"
lang: en-US
papersize: letter
geometry: margin=0.9in
fontsize: 11pt
subject: "A jurisdictional argument for the ontology of governed analytical data and its relationship to business ontology, relational form, semantic-layer technology, and AI agents"
keywords:
  - Theory of Data
  - data ontology
  - ontology
  - governed analytical data
  - business ontology
  - semantic layer
  - relational model
  - analytical identity
  - analytical law
  - AI agents
  - analytical governance
  - semantic contracts
  - jurisdiction
  - constitution
---

**datumwise, an independent open-source research project**

**Version 1.1 - 20 August 2026**  
**DOI:** 10.5281/zenodo.22026962  
**License:** Creative Commons Attribution 4.0 International (CC BY 4.0)  
**Supersedes:** *Data Has Its Own Ontology: Not Borrowed from the World It Describes*, Version 1.0, DOI **10.5281/zenodo.22003683**

**Foundation:** Huayin Wang, *The Theory of Data: A Foundation for Analytical Identity, Derivability, and Consistency*, Version 6.1, DOI **10.5281/zenodo.22013410**.

**Companion entry point:** Huayin Wang, *A Primer on the Theory of Data*, Version 2.2, DOI **10.5281/zenodo.22018549**.

# Abstract

“Data ontology” has become a familiar term in AI engineering and enterprise architecture. It usually means a machine-readable semantic model of the domain represented by data: Customers, Accounts, Products, Contracts, Transactions, their properties, their relationships, and the rules that govern them. Such systems are valuable. They describe the world that data is about.

This paper asks a prior question: **does the data itself have an ontology?**

The Theory of Data (ToD) is an ontology, with governing laws, for governed analytical data. This paper is the jurisdictional argument for that claim. It is a positioning companion to the formal foundation rather than a replacement for it.

The distinction begins with a simple observation: **data is something about something else**. A datum is a typed value at a governed analytical point. From that binding follow questions that are not settled by domain meaning, relational form, or execution alone: what makes an analytical point exist, what partition gives it location, what family gives a measure identity, what state must survive for lawful continuation, and which transformations preserve or establish that identity.

The paper develops a jurisdiction test. A distinct analytical-data jurisdiction is warranted when there are recurring objects with their own conditions of existence and identity, laws of composition and lawful change, and characteristic questions whose correctness remains unresolved even when neighboring systems are internally correct. Four demonstrations make the claim concrete: average-of-averages, many-to-many Product–Category grouping, Inventory through time, and missing value versus missing point. Each can be patched locally inside a neighboring framework. The deeper fact is that the patches must compose under one analytical identity discipline. When population constitution, partition geometry, sufficient state, multiplicity, and family law interact in a single request, one body of law must govern their interaction.

The paper also distinguishes five layers that are often collapsed: ontology, analytical law, semantic contracts, governance process, and implementation carrier. It retains the relational model as a genuine ontology of logical data form while clarifying the role in which relational objects often serve as proxies for analytical identity. It models the crossing from an external domain into analytical data as a governed constitution relation and distinguishes constitution failure from internal analytical-law failure.

For AI agents, the consequence is practical. Business ontology resolves domain meaning. Relational and schema structure describe logical form. Semantic-layer technology exposes governed concepts. ToD adjudicates analytical identity and lawful transformation. The Statistical Bridge governs the later passage from analytical data to statistical evidence and claims.

The paper’s central claim is therefore deliberately narrow:

> **You may already have an ontology of your business. The Theory of Data is the ontology, with governing laws, of analytical data itself — the foundation under which your own data ontology is declared.**

# 1. The occupied phrase: what “data ontology” usually means

The phrase **data ontology** is already occupied.

In current AI, knowledge-graph, and enterprise architecture practice, it commonly refers to a formal semantic model of the domain represented by data. Such an ontology defines classes such as:

```text
Customer
Account
Transaction
Product
Contract
```

together with their properties, relationships, constraints, and axioms.

This usage has a strong intellectual foundation. Gruber described ontology as a specification of a representational vocabulary for a shared domain of discourse (Gruber 1993). Formal ontology developed more explicit methods for categories, dependence, identity, and ontological commitment in information systems (Guarino 1998). Industry ontologies such as FIBO define the things of interest in financial business applications and the ways those things relate (EDM Council 2026). RDF and OWL provide machine-readable formalisms for representing resources, classes, properties, individuals, and formally defined semantics (W3C 2012; W3C 2014).

This is valuable work.

It is also usually an ontology of the **world described by the data**.

A Customer is a business object.

An Account is a business object.

A Product, Claim, Visit, Contract, and Transaction are domain objects.

The ontology tells machines what those things mean and how they relate.

That leads to the threshold distinction of this paper:

> **An ontology of the things described by data is not yet an ontology of the data itself.**

The distinction can be stated in three layers:

| Layer | Primary question |
|---|---|
| **Schema / logical form** | How is represented data structured? |
| **Domain or business ontology** | What do the represented things mean in the world? |
| **Theory of Data** | What analytical data object has been established, and what may lawfully happen to it? |

The short positioning form is:

> **You already have an ontology of your business. ToD is the ontology of data; your own data ontology is declared under it.**

The formal scope is narrower than that slogan. ToD concerns **governed analytical data**: analytical point existence, location, identity, derivability, consistency, sufficient state, lineage, and lawful transformation.

Two levels must remain distinct. **The Theory of Data is the ontology of data**: the domain-general categories and laws that hold across conforming analytical systems. **A Manifold is a data ontology**: a governed declaration of one analytical world under those categories and laws. In that sense, the definite article marks the categorical level, while the possessive marks the instantiated one: *the ontology of data* versus *your data ontology*. The analogy to upper and domain ontologies is useful but limited. ToD does more than supply categories; it also supplies laws and theorems governing analytical identity, staging, derivability, consistency, and typed absence. A conforming data ontology declares its own universes, anchors, families, and contracts, but those declarations do not get to redefine the governing analytical laws.

This paper exists to move a reader from the familiar phrase **data ontology** to the less familiar question **what is data’s ontology?**

# 2. What kind of thing is the Theory of Data?

The phrase *ontology* can be stretched too far if categories, laws, contracts, governance, and implementation are treated as one thing.

The Theory of Data separates them.

## 2.1 Ontology

The ontology identifies the kinds of analytical objects that exist and the conditions under which they are the objects they claim to be.

Its core objects include:

$$
Universe,\quad
ExistenceLaw,\quad
Anchor,\quad
Datum,\quad
MeasureFamily,\quad
Measure,\quad
SufficientState,\quad
Lineage.
$$

A measure is a measure family at an anchor:

$$
\boxed{F@A}.
$$

These are categories of governed analytical data.

## 2.2 Analytical law

The ontology comes with a formal body of law governing those objects.

The law asks, among other things:

- what makes a root point exist;
- when one anchor refines another;
- which transformations preserve anchor;
- which reductions are lawful;
- what state is sufficient for continuation;
- when a new measure family is established;
- when two derivations claiming one identity are required to agree.

This law is part of the jurisdictional claim. An ontology of analytical data that listed nouns but said nothing about lawful transformation would omit the feature that makes analytics analytically dangerous: quantities can cease to be what they were while the arithmetic and execution remain valid.

## 2.3 Semantic contracts

A particular governed system instantiates the ontology and law through declarations and contracts.

Examples include:

- the existence law of a universe;
- the partition semantics of an anchor;
- the identity-bearing declaration of a measure family;
- the sufficient-state law of a reducer;
- multiplicity or allocation contracts;
- support and order conditions.

These are semantic contracts because they make analytical commitments explicit enough to be checked, explained, and enforced.

## 2.4 Governance process

The process by which declarations become authoritative is distinct from the ontology.

Organizations may review, ratify, version, challenge, supersede, or retire governed declarations.

ToD can specify structural conformance. It does not decide which committee, owner, institution, or process has authority to publish the accepted declaration.

Thus:

$$
\boxed{
\text{structural conformance}
\neq
\text{institutional authority}.
}
$$

## 2.5 Implementation carrier

The ontology and its contracts may be carried by many technologies:

- RDF or OWL;
- SHACL;
- YAML or JSON declarations;
- a semantic layer;
- a query compiler;
- a type system;
- a catalog;
- a database;
- a policy engine.

The carrier is not the jurisdiction.

A rule does not become relational law merely because it is enforced in SQL. An analytical identity contract does not become business ontology merely because it is stored in a knowledge graph.

This separation is important because the argument of this paper is semantic, not technological:

> **A jurisdiction is identified by the objects and correctness criteria that govern the question, not by the syntax or system that happens to carry the rules.**

# 3. The jurisdiction test

A vocabulary alone does not establish a distinct ontology.

The stronger test is whether a coherent class of objects and questions has its own conditions of correctness.

A region warrants a distinct analytical ontology when five conditions hold:

1. **distinctive existence conditions** — some analytical objects exist under laws not reducible to row presence or domain-object existence;
2. **distinctive identity conditions** — two values or representations can be equal while denoting different analytical objects;
3. **laws of lawful change and composition** — transformations can preserve, establish, or destroy analytical identity;
4. **cross-domain recurrence** — the same forms recur across unrelated analytical domains;
5. **residual adjudication** — neighboring systems can remain internally correct while a recurring analytical question still requires another body of law.

The fifth condition is the operational test:

> **Which body of semantic law has final authority over the question currently before the system?**

Arithmetic settles arithmetic.

Business ontology settles business meaning.

Relational algebra settles relational form and relational operations.

A semantic layer can expose governed definitions and execution surfaces.

Statistical theory settles inferential questions under its assumptions.

Analytical-data law settles whether the analytical object exists, what identity it has, which state is sufficient, and which transformation preserves or establishes that identity.

The characteristic error pattern matters as evidence. Violating these laws produces recurring analytical failures across domains: wrong denominators, silent duplication, invalid rollups, lost state, unstable results, and false equivalence between quantities that merely share names or values.

The claim is not that other technologies are incapable of encoding these rules.

The claim is:

> **When another formalism fully represents these analytical identity conditions and composes them coherently, it is carrying the analytical-data ontology rather than eliminating the need for it.**

# 4. The relational proxy ontology we already use

The relational model is the obvious objection to any claim that data needs an ontology.

It is also part of the explanation.

Codd’s relational model gave data a domain-independent logical form built from relations, tuples, domains, attributes, keys, and relational operations, while separating the user’s logical view from physical storage details (Codd 1970). That achievement was foundational.

The relational model is a genuine formal model of logical data structure.

This paper uses the phrase **proxy ontology** for a narrower role:

> **Relational objects often serve as practical stand-ins for analytical identity. “Proxy” names that role; it does not imply that the relational model is unreal, incomplete, or merely representational in its own jurisdiction.**

In practice, analytical systems routinely rely on correspondences such as:

$$
\text{row}
\approx
\text{analytical point}
$$

$$
\text{column}
\approx
\text{measure}
$$

$$
\text{GROUP BY columns}
\approx
\text{anchor}
$$

$$
\text{JOIN}
\approx
\text{analytical relation}
$$

$$
\text{displayed value}
\approx
\text{sufficient analytical state}.
$$

These proxies often work.

Their limits appear when logical form and analytical identity diverge.

One analytical point may be supported by several rows.

One row may contribute to several analytical quantities.

A point may exist with no row at all.

The same schema can represent different universes.

The same `JOIN` can implement assignment, attribution, expansion, restriction, or fan-out.

The same `SUM` can preserve a family along one anchor edge and establish a different quantity along another.

The same scalar can display the current value while failing to preserve the state required for future exact continuation.

The historical progression is therefore:

$$
\text{physical storage}
\longrightarrow
\text{logical data representation}
\longrightarrow
\text{analytical data identity}.
$$

Codd separated logical representation from physical storage.

The Theory of Data separates analytical identity from logical representation.

The claim is not that one layer replaces the other. Each answers a different class of questions.

# 5. Four demonstrations, one analytical law

The four examples below are familiar because each can be repaired locally.

That fact is not evidence against a distinct analytical jurisdiction.

It is evidence for one when the repairs must compose.

| Case | Domain / neighboring layer can settle | Local technical remedy | Analytical question that remains | Why a unified jurisdiction matters |
|---|---|---|---|---|
| **Average of averages** | what “average response time” means; where values are stored | aggregate-state typing such as `(sum,count)` | does this representation retain sufficient state for exact continuation? | state capability must compose with the identity of the measure being continued |
| **Product–Category** | Products may belong to several Categories; the join is valid | cardinality checks, assignment, allocation | what contribution semantics create a lawful analytical geometry? | multiplicity and allocation must be governed relative to the measure identity and universe |
| **Inventory through time** | what Inventory means; SQL can aggregate it | temporal-measure semantics | does this anchor movement preserve Inventory or establish another family? | temporal behavior is one instance of the general identity-preserving transformation problem |
| **Missing row / missing point** | Visit and Assay concepts; row/null representation | population or spine modeling | does the point exist, is the measure eligible, is support missing, or is the value zero? | existence and support must compose with later aggregation and claim semantics |

Each local remedy is useful.

The deeper issue appears when one request needs several remedies simultaneously.

Consider:

> **Average revenue per active customer last quarter.**

The system may need to decide:

- what makes an Active Customer point exist;
- whether the customer population comes from a declared status spine or observed activity;
- whether Revenue joins through a relationship that changes multiplicity;
- whether the requested average is formed from exact sufficient state;
- whether the resulting quantity preserves an existing family or establishes a new one.

An aggregate-state type system can answer one part.

A population model can answer another.

A relationship-cardinality framework can answer another.

A temporal semantic rule can answer another.

But the request is one analytical object.

The parts must therefore compose under one identity discipline.

This is where jurisdiction becomes visible:

> **A set of local remedies becomes an analytical ontology when the remedies are governed as one coherent body of law over analytical existence, identity, state, geometry, and transformation.**

Extend neighboring systems far enough to supply those shared conditions and they can carry ToD semantics perfectly well. What has been reconstructed is the same analytical jurisdiction in another implementation form.

Several adjacent formal traditions already expose pieces of this structure. OLAP work on data cubes and summarizability showed that lawful aggregation depends on dimensional structure and aggregation properties rather than on `GROUP BY` syntax alone (Gray et al. 1997; Lenz and Shoshani 1997). Database provenance distinguishes forms of dependency and derivation that remain neighboring to, but distinct from, analytical lineage (Buneman, Khanna, and Tan 2001; Green, Karvounarakis, and Tannen 2007; W3C 2013). Formal-ontology engineering supplies disciplined accounts of categories, identity, and cross-system interoperability (ISO 2021; Keet 2018), while SHACL illustrates how explicit semantic constraints can be carried and validated in a machine-readable form (W3C 2017). These traditions are not rivals to the present claim. They are partial anticipations and implementation neighbors. *The Theory of Data Applied* shows how familiar practitioner rules repeatedly converge on identity, geometry, state, and law (Wang 2026b), while the project’s contract calculus develops the transformation-side obligations around population, expansion, allocation, and fan-out (Wang 2026e). The jurisdictional claim concerns the coherent composition of these analytical concerns under one identity discipline.

# 6. The data region has its own existence and identity conditions

The jurisdiction claim becomes strongest when we examine analytical objects directly.

## 6.1 Analytical existence follows an existence law

In ToD, a **universe** establishes a governed root-point domain under an explicit existence law.

Under an occurrence-based law, a point can exist because a governed occurrence was admitted.

Under a declared or generated law, a point can exist independently of observation: a scheduled visit, a store-day, a registered account, a forecast date, a reporting obligation.

This immediately separates analytical point existence from row existence.

A row may record evidence for a point.

A row may instantiate an occurrence that establishes a point.

A point may also exist with no row at all.

The sequence is:

$$
\boxed{
\text{existence law}
\rightarrow
\text{point existence}
\rightarrow
\text{anchor}
\rightarrow
\text{eligibility}
\rightarrow
\text{support}
\rightarrow
\text{value}.
}
$$

An absent row can therefore correspond to several analytically different states.

## 6.2 Analytical identity is established before comparison

Version 6.1 makes the identity criterion operationally explicit (Wang 2026a).

A governed measure family has an analytical identity before outputs are compared.

An implementation may assign an immutable family ID to that identity. A canonical name is a governed human-readable handle.

Thus:

$$
\boxed{
family\_id
\neq
canonical\_name.
}
$$

More importantly:

$$
\boxed{
\text{identity}
\rightarrow
\text{consistency test}
}
$$

rather than:

$$
\text{value agreement}
\rightarrow
\text{identity}.
$$

Suppose two computations both return `100`.

One may be maximum daily Revenue.

Another may be maximum order Revenue.

The values agree.

The analytical identities differ because the family-establishing operation begins at different analytical locations.

Conversely, if two derivations independently claim the same governed family at the same anchor, they have already committed themselves to one analytical identity. Under satisfied contracts, disagreement is evidence of a failed derivation, premise, implementation, or realization claim.

This direction matters ontologically because identity is not inferred from accidental equality.

## 6.3 Displayed value, state, and identity are different

A displayed average of `42` may or may not retain the state required for exact continuation.

For an ordinary arithmetic mean, useful sufficient state is:

$$
(sum,count).
$$

For exact distinct count, the displayed cardinality is not the identity set needed for arbitrary exact continuation.

Thus:

$$
\boxed{
\text{displayed value}
\neq
\text{sufficient state}
\neq
\text{analytical identity}.
}
$$

The current value, the lawful future of the representation, and the analytical object represented are different questions.

## 6.4 Anchors are governed partitions

A business ontology may correctly state that one Product belongs to several Categories.

That relationship does not automatically define a Category anchor over the original universe because the resulting groups overlap.

A governed system can construct analytical geometry in several ways:

- assign each source point to one Category;
- establish a membership universe whose root points are `(source, category)` pairs;
- allocate contribution across memberships;
- deliberately use full-touch expansion when that is the intended analytical semantics.

The principle remains:

> **An anchor is a partition. Overlap becomes analytical geometry through governed construction.**

This is not a restriction on business knowledge.

It is a condition on analytical location and contribution.

## 6.5 Family law governs lawful continuation

A business ontology can define Inventory correctly.

Arithmetic permits addition.

SQL can execute:

```sql
SUM(inventory)
```

A semantic layer can expose a governed metric named Inventory.

The remaining analytical question is:

> **Does this movement still establish Inventory?**

Inventory may sum lawfully across one partition direction and establish another quantity across another.

The operator name does not settle the identity of the result.

The family law does.

# 7. From the world to the data world: governed constitution

Data is about something else.

That aboutness creates a crossing.

Let:

$$
W
$$

denote an external domain world: business, physical, social, economic, institutional, or scientific.

Let:

$$
D
$$

denote a governed analytical-data world.

Write schematically:

$$
\boxed{
W
\overset{\mu}{\Longrightarrow}
D
}
$$

where $\mu$ is a **governed constitution relation**.

It is called a relation rather than a simple function because constitution can be partial, many-to-many, and versioned over time. Most things in the external world are never constituted as analytical objects; one domain distinction can support several analytical universes; later governed declarations can establish successor constitutions.

The present paper requires constitution to be explicit and governed. It does not attempt a general theory of reference, measurement, or representation between worlds.

## 7.1 Occurrence constitution

Suppose a governed transaction rule admits a completed sale event.

The constitution relation can establish:

$$
\text{qualified sale occurrence}
\rightsquigarrow
\text{root point in a transaction universe}.
$$

The external occurrence supplies the referent and admission premise.

The analytical universe supplies the point identity and later partition geometry.

## 7.2 Declared constitution

Suppose an operating calendar declares that Store 17 is open on 20 August.

The constitution relation can establish:

$$
\text{governed calendar declaration}
\rightsquigarrow
\text{store-day root point}.
$$

No transaction need occur.

The analytical point exists because the declared existence law established it.

## 7.3 Constitution failure and analytical-law failure

This separation gives two failure classes.

A **constitution failure** occurs when the wrong analytical object is established from the external domain:

- the wrong population is admitted;
- two domain entities are collapsed;
- one event is admitted twice;
- an observed-event population substitutes for a declared population;
- the wrong business concept is bound to a family.

An **internal analytical-law failure** occurs after the intended analytical objects have been constituted:

- a finalized average is reused as sufficient state;
- incomparable anchors are treated as refinements;
- a many-to-many relation silently multiplies contribution;
- a reduction crosses an unlicensed family edge.

The crossing can fail while the internal derivation is lawful.

The crossing can be correct while the derivation fails.

These are different diagnoses.

## 7.4 Domain-general forms, domain-specific declarations

This distinction also resolves a common misunderstanding about “domain independence.”

ToD does not inspect the English word `Inventory` and discover how Inventory must aggregate.

It supplies domain-general forms of adjudication:

- existence law;
- partition and refinement;
- family identity;
- sufficient state;
- multiplicity;
- lawful continuation;
- lineage;
- consistency.

Domain-specific governance supplies the declarations that instantiate those forms:

- what Revenue includes;
- which currency applies;
- what Active Customer means;
- whether Inventory preserves identity across a given direction;
- what participation and allocation rules apply;
- which regime is meaning-bearing.

The mature statement is:

> **Domain knowledge constrains which analytical objects are constituted. ToD supplies domain-general forms for what those objects are and how their declared laws may compose.**

# 8. Several ontologies can describe the same represented material

A distinct analytical ontology does not imply exclusivity.

The same material can participate in several ontologies because each answers a different question.

Consider:

```text
(customer=C17, month=2026-07, revenue=420)
```

The represented item can simultaneously be:

1. an **information content entity or data item** under an information-artifact ontology;
2. a **tuple** under the relational model;
3. a statement referring to **Customer C17** and organizational Revenue under a business ontology;
4. a realization or piece of evidence for the analytical measure:

$$
Revenue@CustomerMonth.
$$

The Information Artifact Ontology is especially relevant because it includes information content entities, data items, and an **is about** relation (Information Artifact Ontology 2026).

Aboutness is fundamental.

ToD begins from the same fact in another direction:

> **Data is something about something else.**

IAO asks what kind of information entity the artifact is and what it is about.

The relational model asks what logical form the represented data has.

Business ontology asks what Customer and Revenue mean in the domain.

ToD asks what analytical point has been constituted, which family identity is being realized, which state is sufficient, and which transformations preserve that identity.

These accounts are compatible because they are not competing for one undifferentiated notion of meaning.

They occupy neighboring jurisdictions.

# 9. Semantic-layer technology carries semantics; it does not erase jurisdiction

Semantic-layer architecture places shared governed logic between data stores and consumers such as BI tools, APIs, and AI agents. Current treatments emphasize reusable metric definitions, joins, business terminology, and access rules (Thoughtworks 2026).

That is an architectural role.

A semantic layer can carry:

- business ontology;
- schema and relationship declarations;
- metric definitions;
- ToD analytical contracts;
- permissions;
- materialization metadata;
- query interfaces.

The implementation may place these concerns behind one service.

Their semantic authority remains distinguishable.

A semantic layer can expose a metric called Revenue.

A business ontology can define Revenue as an organizational concept.

A relational system can carry the values and join paths.

ToD can govern:

- which Revenue family identity is intended;
- the anchors at which its measures exist;
- which reducer law preserves the family;
- what sufficient state is required;
- what lineage establishes derived families;
- what multiplicity or support contracts apply.

Thus:

> **Implementation location and ontological jurisdiction are separate properties.**

This matters especially for AI because a single semantic API can conceal several different authorities behind one interface.

# 10. One analytical-agent request, end to end

Consider the request:

> **What was average revenue per active customer last quarter?**

The sentence looks simple.

A governed agent should not execute it immediately.

## 10.1 Domain resolution

Business ontology resolves the relevant concepts:

- Customer;
- Active Customer;
- Revenue;
- quarter.

At this stage the agent may understand the organization perfectly and still lack a unique analytical request.

## 10.2 Competing constitutions

Suppose two governed interpretations of Active Customer exist.

A status-based constitution:

$$
U_{\mathrm{status}}
=
\{\text{customers active under governed status at quarter start}\}.
$$

An occurrence-derived constitution:

$$
U_{\mathrm{activity}}
=
\{\text{customers with qualifying activity during the quarter}\}.
$$

Both use valid business concepts.

They have different existence laws and different denominators.

The agent therefore reaches:

> **Clarify:** “Should ‘active customer’ mean governed active status at the start of the quarter, or customers with qualifying activity during the quarter?”

This is not a language-model preference.

It is unresolved analytical constitution.

## 10.3 Multiplicity

After the population is resolved, Revenue may need attribution to Customer.

If the relationship path is many-to-many, the agent must know whether contribution semantics use:

- assignment;
- allocation;
- a membership universe;
- full-touch expansion.

A valid join alone is not enough.

## 10.4 Sufficient state

The requested result is an average.

If the system has only finalized subgroup averages, exact continuation may be impossible.

If it retains the appropriate sufficient state, such as Revenue state and Customer-count state, the result may be exactly derivable.

## 10.5 Identity and execution

Only after the population, contribution semantics, state capability, and target family are established can the request be recognized as one governed analytical object.

The decision sequence is:

$$
\boxed{
\text{User request}
\rightarrow
\text{domain resolution}
\rightarrow
\text{candidate constitution}
\rightarrow
\text{ToD adjudication}
\rightarrow
\begin{cases}
\text{Serve}\\
\text{Disclose}\\
\text{Clarify}\\
\text{Refuse}
\end{cases}
}
$$

**Serve** when the object and path are established and the governed result is entitled to be returned.

**Disclose** when the target is meaningful and serviceable but a material limitation, qualification, or retained-capability boundary must accompany the result.

**Clarify** when several governed analytical meanings remain possible.

**Refuse** when a required analytical premise or transformation contract is absent.

At a surrounding governance boundary, a system may also **Escalate** a case for institutional resolution; that is a governance action rather than a fifth analytical serving verdict (Wang 2026c).

This example demonstrates why the four local remedies in Section 5 need one composition discipline. Population constitution, multiplicity, state, and identity are separate questions, but the requested result is one analytical object.

# 11. From analytical data to statistical claims

The analytical jurisdiction ends before statistical inference begins.

Suppose the request becomes:

> **Is average revenue per active customer increasing, and will it continue next quarter?**

ToD can govern the analytical objects used as evidence.

It does not by itself license the future claim.

The Statistical Bridge asks what makes governed analytical data evidence for a formal target and licensed claim: where probability enters, which model or inferential object has authority, what premises support the passage, and how far the result may travel (Wang 2026d).

The architecture is therefore plural:

$$
\boxed{
\begin{array}{ll}
\textbf{Business ontology:} & \text{What does the domain mean?}\\[2pt]
\textbf{Relational / schema form:} & \text{How is represented data logically structured?}\\[2pt]
\textbf{Semantic Layer:} & \text{How are governed concepts exposed and executed?}\\[2pt]
\textbf{Theory of Data:} & \text{What analytical objects exist and what transformations are lawful?}\\[2pt]
\textbf{Statistical Bridge:} & \text{What claims can the resulting evidence support?}
\end{array}
}
$$

The systems can share software.

Their governing questions remain distinct.

# 12. Scope

The title of this paper is intentionally strong.

Its scope is intentionally narrow.

The Theory of Data is not an ontology of all possible information, all business objects, or all analytical reasoning.

It governs **governed analytical data**.

Business ontology retains authority over concepts such as Customer, Product, Contract, Risk, Organization, and Supply Chain.

The relational model retains authority over logical relational form.

Semantic-layer technology retains its architectural role in serving governed concepts and execution surfaces.

Mathematics retains authority over mathematical law.

Statistical and causal theory retain authority over inferential and causal claims.

ToD’s jurisdiction is concentrated in a small set of recurring concerns:

- analytical standing;
- analytical identity;
- derivability;
- consistency;
- materialized capability.

Its core objects remain correspondingly small:

- universe and existence law;
- anchor and partition geometry;
- datum;
- measure family and measure;
- mapper and reducer;
- sufficient state;
- lineage and contracts.

A **Manifold** is an enterprise or domain declaration under this foundation: one governed data ontology instantiated from ToD's categories and laws. ToD is therefore not an enterprise's constitution; it is the theory of what such a constitution is and what analytical laws every conforming constitution must obey.

The claim is foundational rather than universal.

The consequences can spread widely because analytical data sit beneath many systems.

That does not make analytical data identical to every layer built on top of them.

# 13. Conclusion

The phrase **data ontology** usually points outward.

It names a semantic model of the world represented by data: Customers, Accounts, Products, Transactions, Contracts, and the relationships and rules that make those domain objects intelligible to humans and machines.

That work is important.

This paper asks the phrase to turn inward.

What is the ontology of the analytical data itself?

The answer begins with a simple observation:

> **Data is something about something else.**

A datum is a typed value at a governed analytical point.

A universe establishes which root points exist.

An anchor partitions those points into analytical locations.

A measure family supplies governed analytical identity.

A measure is that family at one anchor:

$$
F@A.
$$

Sufficient state governs lawful continuation.

Family law governs which transformations preserve identity.

Lineage records where new analytical identities come from.

Version 6.1 adds an especially important identity rule:

> **Identity is established before comparison. Agreement tests an identity already claimed; it does not create that identity.**

The four demonstrations show why these ideas form one jurisdiction.

An average can be arithmetically valid while sufficient state is lost.

A Product–Category relation can be correct while analytical contribution remains unresolved.

Inventory can be perfectly meaningful while a requested reduction establishes another quantity.

A row can be absent while an analytical point still exists.

Each case has a local technical remedy.

The jurisdiction appears when those remedies must compose into one governed analytical object.

The relational model can carry some of that law.

A semantic layer can carry some or all of it.

A knowledge graph can carry it.

A type system can enforce it.

None of those carriers removes the semantic question:

> **What body of law determines whether this analytical object exists, what identity it has, and what transformations preserve that identity?**

That body of law is the analytical-data jurisdiction formalized by the Theory of Data.

The strong positioning form is:

$$
\boxed{
\textbf{You may already have an ontology of your business.}
}
$$

$$
\boxed{
\textbf{The Theory of Data is the ontology, with governing laws, of analytical data itself.}
}
$$

$$
\boxed{
\textbf{Your own data ontology is declared under it.}
}
$$

The difference is only a few words.

It is the difference this paper exists to make visible.

# References

Buneman, Peter, Sanjeev Khanna, and Wang-Chiew Tan. 2001. “Why and Where: A Characterization of Data Provenance.” In *Database Theory — ICDT 2001*, 316–330. DOI: 10.1007/3-540-44503-X_20.

Codd, Edgar F. 1970. “A Relational Model of Data for Large Shared Data Banks.” *Communications of the ACM* 13(6): 377–387. DOI: 10.1145/362384.362685.

EDM Council. 2026. “Financial Industry Business Ontology (FIBO).” *Open Knowledge Graph*. Accessed 18 August 2026. https://spec.edmcouncil.org/

Gray, Jim, Surajit Chaudhuri, Adam Bosworth, Andrew Layman, Don Reichart, Murali Venkatrao, Frank Pellow, and Hamid Pirahesh. 1997. “Data Cube: A Relational Aggregation Operator Generalizing Group-By, Cross-Tab, and Sub-Totals.” *Data Mining and Knowledge Discovery* 1: 29–53. DOI: 10.1023/A:1009726021843.

Green, Todd J., Grigoris Karvounarakis, and Val Tannen. 2007. “Provenance Semirings.” In *Proceedings of the Twenty-Sixth ACM SIGACT-SIGMOD-SIGART Symposium on Principles of Database Systems*, 31–40. DOI: 10.1145/1265530.1265535.

Gruber, Thomas R. 1993. “A Translation Approach to Portable Ontology Specifications.” *Knowledge Acquisition* 5(2): 199–220. DOI: 10.1006/knac.1993.1008.

Guarino, Nicola. 1998. “Formal Ontology and Information Systems.” In *Formal Ontology in Information Systems: Proceedings of FOIS'98*, 3–15. Amsterdam: IOS Press.

Information Artifact Ontology. 2026. “Information Artifact Ontology (IAO).” IAO Project repository. Accessed 18 August 2026. https://github.com/information-artifact-ontology/IAO

ISO. 2021. *ISO/IEC 21838-2:2021 — Information Technology — Top-Level Ontologies (TLO) — Part 2: Basic Formal Ontology (BFO).* Geneva: International Organization for Standardization. https://www.iso.org/standard/74572.html

Keet, C. Maria. 2018. *An Introduction to Ontology Engineering*. Cape Town: Maria Keet. Open Textbook Library. https://open.umn.edu/opentextbooks/textbooks/an-introduction-to-ontology-engineering

Lenz, Hans-Joachim, and Arie Shoshani. 1997. “Summarizability in OLAP and Statistical Data Bases.” In *Proceedings of the Ninth International Conference on Scientific and Statistical Database Management*, 132–143. DOI: 10.1109/SSDM.1997.621175.

Thoughtworks. 2026. “Semantic Layer.” *Technology Radar*, Volume 34, April 2026. https://www.thoughtworks.com/radar/techniques/semantic-layer

W3C. 2012. *OWL 2 Web Ontology Language Document Overview (Second Edition).* W3C Recommendation, 11 December 2012. https://www.w3.org/TR/owl2-overview/

W3C. 2013. *PROV-DM: The PROV Data Model.* W3C Recommendation, 30 April 2013. https://www.w3.org/TR/prov-dm/

W3C. 2014. *RDF 1.1 Concepts and Abstract Syntax.* W3C Recommendation, 25 February 2014. https://www.w3.org/TR/rdf11-concepts/

W3C. 2017. *Shapes Constraint Language (SHACL).* W3C Recommendation, 20 July 2017. https://www.w3.org/TR/shacl/

Wang, Huayin. 2026a. *The Theory of Data: A Foundation for Analytical Identity, Derivability, and Consistency*. Version 6.1. Zenodo. DOI: 10.5281/zenodo.22013410.

Wang, Huayin. 2026b. *The Theory of Data Applied: Classical Analytical Failures as Problems of Identity, Geometry, State, and Law*. Version 1.0. Zenodo. DOI: 10.5281/zenodo.21959941.

Wang, Huayin. 2026c. *Analytical Governance: From User Intent to Governed Analytical Execution*. Version 1.0. Zenodo. DOI: 10.5281/zenodo.21959749.

Wang, Huayin. 2026d. *The Statistical Bridge: From Governed Evidence to Inference Certificates and Licensed Claims*. Version 3.0. Zenodo. DOI: 10.5281/zenodo.21979821.

Wang, Huayin. 2026e. *A Contract Calculus for Governed Analytical Transformation: Totality, Partiality, Population, Expansion, and Fan-Out*. Version 1.0. Zenodo. DOI: 10.5281/zenodo.21752373.

Wang, Huayin. 2026f. *A Primer on the Theory of Data*. Version 2.2. Zenodo. DOI: 10.5281/zenodo.22018549.

---

## Revision note

**Version 1.1.** This revision aligns the paper with *The Theory of Data*, Version 6.1 and recasts the paper explicitly as a jurisdictional argument for the ontology of governed analytical data. It distinguishes ontology, analytical law, semantic contracts, governance process, and implementation carrier; clarifies the “proxy ontology” role of relational form; promotes the four demonstrations into a comparative and compositional argument; defines the world-to-data crossing as a governed constitution relation; adopts domain-general analytical forms with domain-specific governed declarations; makes explicit the two-level distinction between **the ontology of data** (ToD) and **a data ontology** (a governed Manifold declared under ToD); adds ex-ante identity, a mapped coexistence example with information-artifact and relational ontologies, an adjacent-formal-traditions reconciliation, and an end-to-end analytical-agent walkthrough using the corpus-wide **Serve · Disclose · Clarify · Refuse** outcome vocabulary.

**DOI:** **10.5281/zenodo.22026962**

**Supersedes:** Version 1.0, DOI **10.5281/zenodo.22003683**
