# Governing Across Ontological Worlds

## Why Enterprise AI Should Separate Meaning, Data, and Execution

**Huayin Wang**  
**Version 1.0 · 30 August 2026**  
**DOI:** 10.5281/zenodo.22181382  
**License:** Creative Commons Attribution 4.0 International (CC BY 4.0)  
**datumwise, an independent open-source research project**

## Abstract

Enterprise AI increasingly depends on business ontologies, semantic layers, shared identifiers, governed metrics, and common data services. These technologies address real problems. They reduce semantic disorder and give intelligent systems a more coherent environment in which to reason.

The architectural risk appears when integration is achieved by tightly coupling objects that belong to different ontological worlds: business meaning, governed analytical data, and material representation. A business term may be bound directly to a warehouse field and SQL expression. A shared identifier may be treated as one identity across business ontology, analytical data, and physical records. A graph relation may be allowed to carry predicates or measures merely because two endpoints share reference. In each case, a relation established under one kind of authority acquires force in another.

This paper argues that such coupling is a governance error when the objects on the two sides remain governed by different laws or authorities. The reason is structural: **a crossing can be governed as a crossing only while its two sides remain distinct**. Once Business World and Data World are merged, constitution appears to be an internal modeling step. Once Data World and Material Data World are merged, realization appears to be an internal implementation step. The transfer of authority still occurs, but it is no longer represented as an independently governable act.

The alternative is neither semantic fragmentation nor a rejection of common infrastructure. It is to keep independently governed worlds distinct, establish explicit and purpose-bounded relations between them, and let applications compose those governed crossings. A shared identifier can be evidence for such a relation; it is not permission for unrestricted semantic or analytical propagation. A crossing may also establish new shared meaning that belongs to the relation itself. The endpoints remain themselves; the new relation lives in the passage.

AI agents make this design issue urgent because they can traverse business meaning, analytical construction, material execution, interpretation, and action in one continuous process. What was previously a coordination problem can become an authority-propagation problem at machine speed.

The resulting principle is simple:

> **Separate the worlds. Govern the crossings. Compose through the crossings.**

Ontological separation does not prevent integration. It is what makes governed integration possible.

---

# 1. Integration by coupling

Enterprise data architecture has spent decades trying to make fragmented systems work together.

The problems are familiar. Different departments use different meanings for the same word. Different systems use different identifiers for the same entity. Metrics are implemented repeatedly. Relationships are embedded in application code and SQL. Business logic accumulates in warehouses, dashboards, semantic models, and people's memory.

The arrival of AI agents makes this fragmentation more visible. An agent that is expected to operate across an enterprise cannot safely reconstruct the meaning of `customer_id`, `revenue`, `active`, or `region` from physical schemas every time it receives a question. It needs organized knowledge.

Business ontologies, semantic layers, knowledge graphs, metric systems, master data, common identifiers, and governed data products are therefore natural parts of an enterprise-AI architecture. They can substantially improve discoverability and consistency.

A common stack can be drawn simply:

```text
business ontology
        ↓
semantic layer
        ↓
enterprise data and tools
        ↓
AI agent
```

The stack centralizes whether or not centralization was named as the goal. More precisely, it tends to settle some questions before the application acts. It may settle which business concept a term denotes, which record identities refer to the same thing, which metric definition is authoritative, which relationships connect entities, and how those objects bind to material data.

There is nothing inherently wrong with such settlement. Where the underlying meaning and authority are genuinely shared, centralization is efficient. If an enterprise has one authoritative currency code system, one legal entity identifier, or one ratified Revenue definition for a particular reporting purpose, repeating the same agreement inside every application would add little value.

The problem begins when integration requires several different kinds of authority and the architecture treats them as one.

Three common practices illustrate the issue.

**Implementation capture** occurs when a business term is bonded directly to its current warehouse field, metric object, or SQL implementation:

```text
business term
    ↓
warehouse field / metric
    ↓
SQL implementation
```

Over time, the business concept, analytical object, and physical procedure can become difficult to distinguish. Changing the business meaning appears to require changing the warehouse object. Conversely, the existing SQL can begin to define what the business term means because that is what the system happens to compute.

**Identity collapse** occurs when one identifier is treated as one identity across the Material Data World, Data World, and Business World:

```text
material record identity
        =
analytical data identity
        =
business identity
```

A single identifier may be treated as the identity of the physical row, the governed analytical object, and the business entity or role. This can simplify reference. It can also erase the fact that these identities answer different questions.

**Reference inflation** occurs when shared reference is treated as permission to carry predicates, relationships, measures, or claims across the boundary:

```text
same referent
    ↓
portable predicates and relationships
    ↓
analytical permission
```

Two systems establish that they refer to the same company, customer, supplier, or asset. The shared reference then becomes a basis for carrying properties, relationships, metrics, or claims across the boundary.

Again, the first step can be highly valuable. The difficulty lies in the authority silently attached to the later steps.

These labels are descriptive, not new architectural categories. They simply let the paper refer consistently to three recurring forms of the same error: cross-world authority propagating without an independently governed relation.

These are forms of **tight coupling across ontological worlds**. A decision, identity, or relationship established in one world is allowed to determine identity or behavior in another without a separately governed passage.

The criticism in this paper is directed at that practice, not at a technology category. A semantic layer can preserve strong boundaries or erase them. A federated architecture can still propagate authority through a shared identifier graph without an explicit crossing. A warehouse can be used as a material realization of governed data or can become the de facto source of analytical identity. The architectural question is not whether the platform is called centralized, federated, semantic, graph-based, or domain-oriented.

The question is:

> **When two parts of the system are governed by different laws or authorities, is their relationship itself governed, or has the architecture already fused them?**

That distinction is the paper's center. Tight coupling is objectionable here not because coupling is aesthetically impure, but because it can make a transfer of authority disappear inside what looks like one internal object or operation.

---

# 2. Three worlds and two kinds of governance

The full distinction among the Business World, Data World, and Material Data World is developed in *The Three Worlds of Analytics* (Wang 2026b). Only the part necessary for the present argument is required here.

The **Business World** is the world of domain meaning. It contains customers, products, contracts, stores, policies, classifications, organizational relationships, and concepts such as *active customer* or *recognized revenue*. Its governing question is:

> **What does this mean in this organization or domain?**

The **Data World** is the world of governed analytical data, developed formally in *The Theory of Data* (Wang 2026a). It contains measures, populations, universes, anchors, analytical identity, derivation, support, absence, sufficient state, and analytical lineage. Its governing question is:

> **What analytical object exists, and what follows lawfully from it?**

The **Material Data World** is the world of representation and computation. It contains records, rows, columns, tables, dataframes, files, databases, schemas, indexes, queries, execution plans, and physical operations. Its governing question is:

> **How is data represented, stored, retrieved, transformed, and computed?**

The distinction can be compressed into one criterion:

> **Different objects, different laws, different authority.**

The worlds necessarily interact. A business concept may need to be constituted as governed analytical data. A governed analytical object may need to be realized in a warehouse. A computed result may return to the business as an answer.

The important distinction is not between interaction and separation. The important distinction is between **governance within a world** and **governance across worlds**.

Within the Business World, governance determines which definitions, classifications, and domain relationships are authoritative.

Within the Data World, governance determines analytical identity, lawful derivation, population, support, movement, and consistency.

Within the Material Data World, governance determines representation, access, physical integrity, execution correctness, and operational behavior.

A crossing asks a different class of questions.

Suppose a business concept is related to a governed analytical object. The relevant questions include:

- Which business concept is being related?
- Which analytical object does it constitute?
- For what purpose does the relation hold?
- Which aspects of business meaning become part of analytical identity?
- What evidence supports the relation?
- Who has authority to ratify it?
- Which business authority remains local and does not enter the Data World?
- What happens when the business definition changes?

Suppose a Data World object is bound to a material representation. The questions change:

- Which physical source realizes the governed object?
- Which keys realize its analytical points?
- Which material relationships preserve the required analytical relation?
- What support does the current material state establish?
- What analytical authority does the physical system *not* acquire?
- When must the realization be re-established?

These are governance questions about **passage**, not simply additional rules inside either endpoint.

This distinction leads to the central deduction.

---

# 3. Separation is a condition of crossing-governance

A crossing can be governed as a crossing only while the worlds on its two sides remain distinct.

This is the load-bearing argument of the paper.

Consider first the boundary between the Business World and the Data World.

Suppose an organization uses one integrated semantic object to represent a business concept and the analytical data associated with it. The definition of *Revenue*, its analytical identity, its population, and the code that computes it may all appear under one metric object. The system can be disciplined and well documented. Yet the architectural act by which business meaning became governed analytical identity is no longer clearly represented as a passage between authorities.

It looks like an internal modeling step.

Once that happens, several questions become harder to ask independently.

Was the business definition itself authoritative?

Which parts of that definition became identity-bearing analytical law?

Did a local semantic distinction become a new Data World identity, or merely a label?

Which analytical rules follow from the business declaration, and which require separate Data World law?

If the business meaning changes, which analytical identities should change and which should remain stable?

The crossing still exists in substance. Business meaning is still being made to govern analytical data. But the architecture has declared the two sides to be one object, so the transfer of authority is no longer visible as a separate event.

Now consider the boundary between the Data World and the Material Data World.

Suppose Revenue is identified by a warehouse column and SQL expression. Its source grain is inferred from table structure. Relationships are inferred from foreign keys. Missing rows are interpreted through the physical representation. The system may calculate correctly and reproducibly.

Again, the crossing has become internal.

The system can ask whether the query ran, whether the schema is valid, whether the join is permitted by the database, and whether the result reconciles materially. It has a weaker place to ask whether the material construction faithfully realizes the independently governed analytical object because the object and its implementation have already been bonded together.

A physical change can then acquire analytical force by accident. A new join path can change contribution multiplicity. A schema migration can change which points are present. A rewritten SQL expression can alter population semantics. A warehouse key can become the practical definition of identity.

The problem is not that material systems are incapable of carrying semantic information. They can carry a great deal of it.

The problem is that **one world has become the source of authority for another because the boundary through which authority moved has been erased**.

The same issue appears horizontally across independently governed business domains.

Finance may govern *Billing Customer*. Support may govern *Service Customer*. A unified enterprise `Customer` can be useful if the organization has genuinely established one object that subsumes both for the relevant purposes. But if the two concepts remain legitimately different, collapsing them into one identity makes the relationship between them an internal fact of the central ontology.

The system can no longer distinguish easily between:

- what Finance means by Billing Customer;
- what Support means by Service Customer;
- the fact that a particular billing party corresponds to particular service relationships;
- the purpose for which that correspondence is valid;
- and the authority that ratified the correspondence.

Merger has turned a relation among governed objects into the internal structure of one object.

This produces the paper's principal claim:

> **If the difference between worlds is erased, the transfer of authority cannot be represented as a distinct governed act.**

The converse matters just as much. When the endpoints remain distinct, the relation between them can itself become a governed object. New shared meaning can be created in that relation without forcing either endpoint to absorb the other.

The conclusion is stronger than a preference for loose coupling.

Ontological separation is not valuable merely because modular systems are easier to maintain.

It is valuable because it preserves the crossing as an object that can be governed.

---

## 3.1 Three recurring forms of the same error

The examples in §1 can now be located more precisely.

In **implementation capture**, a material implementation becomes the practical source of business or analytical meaning.

In **identity collapse**, one identifier is treated as one identity across worlds whose identities answer different questions.

In **reference inflation**, a shared referent is allowed to carry predicates, measures, or standing beyond what shared reference establishes.

The shared-identifier case makes the distinction especially clear. Suppose two organizations use the same globally resolvable identifier for a supplier. They have solved an important problem: they can establish that their records refer to the same supplier without first negotiating a local key mapping.

But a sequence of further claims may still be required:

```text
same identifier
    ↓
same referent
    ↓
same object for this purpose
    ↓
same business meaning
    ↓
same analytical identity
    ↓
same lawful derivations
    ↓
same standing for use
```

Each arrow is a separate claim.

The identifier does not establish the whole chain.

A passport is a useful analogy because it stops at the right place. It helps another jurisdiction establish who has arrived. It does not by itself determine every right, obligation, role, or standing that applies there.

Likewise, a shared identifier can be strong evidence for a crossing. It does not replace the crossing.

> **Permissionless reference is not permissionless authority.**

The general rule is therefore:

> **Integration does not justify collapsing identities across worlds. Where objects remain governed by different laws or authority, relate them through a governed crossing rather than treating them as one identity.**

---

# 4. A crossing is a governed relation

If integration is not performed by merger, the architecture needs another object.

A useful working definition is:

> **A crossing is a versioned governed relation that states what may pass between identified endpoints, for a stated purpose, under stated evidence and authority.**

The definition is intentionally implementation-neutral.

A crossing is first a declaration about meaning and authority.

An implementation may compile that declaration into mappings, capabilities, policies, plans, certificates, validation rules, or runtime checks. Those artifacts realize the crossing. They are not its conceptual definition.

At minimum, a crossing should be able to establish several things.

**Endpoints.** What governed objects are being related?

**Relation.** What exactly is asserted between them?

**Purpose.** For what use does the relation hold?

**Evidence.** What supports the assertion?

**Authority.** Who or what process ratified it?

**Validity.** Which version or period does it govern?

**Permitted consequences.** What predicates, movements, transformations, or uses does it license?

**Non-transferred authority.** What remains local to each endpoint?

**Revision and revocation.** What happens when the relation or an endpoint changes?

This is not intended as a universal contract schema. Different crossings require different details. A Business-to-Data constitution and a Data-to-Material realization do not carry identical evidence or authority. A cross-domain business relation may need cardinality and purpose limits. A material realization may need freshness or support evidence.

The important architectural fact is that the relation is governed independently of the endpoints.

For a cross-domain relation, ratification normally requires the owners or accountable authorities of the two endpoints, together with an authority competent for the stated purpose of the relation. The exact institutional form can vary; what matters is that neither endpoint owner nor the consuming application can unilaterally mint cross-boundary authority.

Not every crossing is the same kind of artifact. The governing questions are shared, but the evidence and non-transfer rules differ by boundary:

| Crossing | Typical endpoints | Typical evidence | What does not transfer automatically |
|---|---|---|---|
| **Business ↔ Business** | Billing Customer ↔ Service Customer | domain definitions, contracts, account records, approved correspondence | one domain's predicates, policies, or ownership over the other |
| **Business ↔ Data** | recognized revenue ↔ governed Revenue family/population | ratified business definition, analytical constitution, identity-bearing rules | business authority over Data World law; Data World identity back into all business meanings |
| **Data ↔ Material** | governed measure ↔ table/column/API realization | bindings, keys, structural tests, support/freshness evidence | material schema or execution authority over analytical identity and law |

The table is intentionally small. Its purpose is to prevent three different crossings from being treated as one generic mapping problem.

That independence has two consequences.

First, the relation can change without redefining either endpoint.

Second, a relation can be created even when neither endpoint previously contained it.

This constructive point is central enough to state plainly:

> **The relation may be new while the endpoints remain themselves.**

Suppose Finance governs **Billing Customer** and Support governs **Service Customer**.

Both concepts may be complete and authoritative in their own domains. Neither domain may have any reason to define the other.

A new application asks:

> Which service relationships correspond to which billing parties for customer-health analysis?

The organization now needs a relation that did not previously exist as an authoritative object.

That new relation can live in the passage.

It can say, for example:

```text
Billing Customer
        ↕
customer-health correspondence
        ↕
Service Customer
```

The crossing can be ratified for customer-health analysis, supported by account administration and contract evidence, versioned over time, and limited in the consequences it licenses.

Billing Customer remains Billing Customer.

Service Customer remains Service Customer.

The new meaning is not forced into either endpoint.

This is the constructive half of the architecture.

Explicit crossings do not merely prevent accidental authority transfer. They provide a place where new, limited, accountable shared meaning can be created.

---

# 5. Application composition without semantic merger

The phrase *compose in the application* can sound like ordinary integration glue unless the authority boundary is made explicit.

The application does not receive permission to invent a relationship merely because it needs one.

It composes governed objects through already established crossings.

A worked case makes the difference concrete.

## 5.1 Local business meanings

Finance governs:

```text
Billing Customer
Billing Account
Recognized Revenue
Payment Responsibility
```

Support governs:

```text
Service Customer
Service Account
Support Case
Service Entitlement
```

A **Billing Customer** is the party responsible for payment under a billing relationship.

A **Service Customer** is the customer relationship under which service and support are delivered.

The two often correspond. They are not necessarily identical.

One parent company may pay for several operating subsidiaries.

One billing account may cover several service accounts.

A reseller may pay while another organization receives the service.

Several billing parties may also relate to one service organization over time.

The two domains therefore have legitimate reasons to keep their customer concepts distinct.

## 5.2 Constitution into the Data World

Finance's business meaning can be related to governed analytical objects.

Conceptually:

```text
Finance: Billing Customer
        ↓ governed constitution
Data World: BillingCustomer population
Data World: RecognizedRevenue @ BillingCustomer
```

Support can do the same independently:

```text
Support: Service Customer
        ↓ governed constitution
Data World: ServiceCustomer population
Data World: SupportCases @ ServiceCustomer
```

Neither constitution creates a universal enterprise `Customer`.

The Data World can govern both analytical populations and the measures that live on them.

## 5.3 The cross-domain relation

For a customer-health application, the relevant authorities establish a governed relation between the two populations.

Assume the current relation includes:

```text
Billing Customer B17
    ↔ Service Customer S21
    ↔ Service Customer S22
    ↔ Service Customer S23

Billing Customer B18
    ↔ Service Customer S23
```

The relation is not one-to-one.

That fact matters.

Suppose Finance reports:

```text
RecognizedRevenue @ B17 = $1,000,000
RecognizedRevenue @ B18 = $400,000
```

Support reports:

```text
SupportCases @ S21 = 20
SupportCases @ S22 = 18
SupportCases @ S23 = 12
```

The crossing establishes correspondence for customer-health analysis.

It does not establish that Revenue can be copied to every related Service Customer.

If the system replicated B17's $1,000,000 onto S21, S22, and S23, then joined B18's $400,000 to S23, it could produce physically valid rows and completely invalid analytical attribution.

The relationship is not analytical permission. Treating it as such would be **reference inflation**: correspondence would be allowed to carry a measure it never licensed.

## 5.4 A question the application may answer

The executive asks:

> Which billing customers with declining Revenue are associated with service customers whose support-case volume is rising?

This question can be answered without creating a universal Customer.

The application can:

1. keep `RecognizedRevenue` at the `BillingCustomer` analytical location;
2. use the governed billing-to-service relation;
3. reduce or otherwise summarize the related Support Case measure back to the Billing Customer location under the applicable Data World law;
4. compare the Revenue trend and support trend at `BillingCustomer`;
5. return the result with the purpose and relevant crossing preserved where required.

The resulting statement might be:

> Billing Customer B17 has declining Recognized Revenue and is associated, under the approved customer-health relation, with Service Customers whose combined support-case volume increased during the period.

That statement is more precise than simply saying "Customer B17 has declining revenue and rising support cases." It preserves the fact that the result was composed across two governed concepts.

## 5.5 A plausible question the application must not answer yet

Now ask:

> Which Service Customer has the largest Revenue decline?

The system has Revenue at Billing Customer.

It has a many-to-many correspondence between Billing Customer and Service Customer.

It does **not** have an allocation or assignment rule that establishes `RecognizedRevenue @ ServiceCustomer`.

The request is computationally tempting.

A join can be written immediately.

A model can choose a plausible rule.

The result could even look reasonable.

But the analytical passage has not been established.

The system should therefore refuse that interpretation, clarify the intended attribution rule, or escalate the need for a new governed relation or measure, using the service distinctions developed in *Analytical Governance* (Wang 2026c).

The reason chain is explicit:

```text
governed correspondence exists
        ↓
Revenue attribution is not part of that correspondence
        ↓
no Data World law establishes RecognizedRevenue @ ServiceCustomer
        ↓
requested measure is not established
        ↓
do not serve the answer
```

The system knows why it must stop:

- the business crossing establishes correspondence, not Revenue attribution;
- the Data World does not contain a lawful movement that establishes Recognized Revenue at Service Customer;
- no ratified allocation or assignment rule supplies the missing authority.

This is where the design principles become a design discipline.

The absence of a crossing is not an invitation to improvise.

It is evidence that the requested passage has not been governed.

## 5.6 When one side changes

Suppose Support changes its Service Customer definition.

Beginning 1 October, service relationships are separated by product line. Existing Service Customer S21 is succeeded by two governed service relationships:

```text
S21-A
S21-B
```

What should change?

Support's own business ontology changes under Support authority.

Its Business-to-Data constitution changes accordingly.

Crossings whose endpoint was the earlier Service Customer identity must be reviewed.

The customer-health correspondence involving B17 and S21 may be replaced with relations to S21-A and S21-B.

Any analytical construction depending on the old crossing may need re-establishment for dates after the change.

What does **not** change automatically?

Finance's Billing Customer definition.

Recognized Revenue identity.

The rest of Support's unrelated concepts.

The Data World foundation.

Historical results governed under the earlier valid relation.

A further question now becomes visible rather than being silently assumed: **are trends across the succession boundary still comparable?** The answer may be yes, but it requires its own grounds. If the change from S21 to S21-A/S21-B alters the service population or the meaning of the support measure materially, a time series that spans 1 October may need a governed succession or comparability relation before values on the two sides are treated as one continuous analytical series.

This is a direct architectural benefit of keeping the relation explicit.

The system can identify what changed, which crossings depend on it, which downstream applications depend on those crossings, and what remained stable.

A central universal Customer identity can also be versioned carefully, but the architecture has to reconstruct the same dependency boundaries inside the central object.

An explicit crossing makes them first-class from the start.

## 5.7 What application composition means

The application therefore does not merge the endpoints.

It does not invent authority.

It combines governed objects through governed relations.

> **Application composition means that an application may obtain foreign-world force only through an already ratified crossing; technical connectivity alone does not create permission.**

That is the alternative topology in operational form.

---

# 6. Why AI changes the operating conditions

AI did not create these crossings.

It changed the conditions under which they are traversed.

For much of the history of analytics, people stood at many of the important boundaries.

A business user asked a question.

An analyst interpreted it.

A data engineer understood the material relationships.

An analytics engineer understood metric construction.

A statistician understood what the evidence supported.

A reviewer or domain expert could challenge the result.

These people were often described as translators. They did more than translate.

They carried local distinctions and authority boundaries that the systems themselves did not represent.

An analyst could know that Finance's *customer* and Support's *customer* were not one thing.

An engineer could know that a matching identifier did not authorize a many-to-many Revenue transfer.

A statistician could know that a material result supported one descriptive claim but not a broader inference.

AI agents increasingly compress this work into one continuous process, from interpretation and relationship selection through execution, interpretation, and action.

This capability is valuable precisely because it reduces the friction that previously required several people and systems. It also removes many of the informal stops at which an authority boundary could be noticed.

If the architecture has already tightly coupled business meaning, analytical identity, and material execution, an agent can propagate an upstream settlement through the entire chain without encountering a visible boundary. Implementation capture, identity collapse, and reference inflation can then compound rather than remain separately challengeable.

A business term resolves to a semantic object.

The semantic object resolves to a metric.

The metric resolves to SQL.

The SQL resolves to a result.

The result becomes natural-language explanation.

The explanation becomes action.

Every local operation may appear valid.

The problem is that the authority acquired at the start can travel farther than the grounds that established it.

This is why:

> **What was previously a coordination problem can become an authority-propagation problem.**

The appropriate response is not to make the agent less capable.

The agent should be able to search broadly, compare alternatives, propose crossings, identify missing relations, and formulate new requests.

The distinction is between intelligence and authority, developed directly for AI agents in *Do Not Let Your AI Agent Govern Itself* (Wang 2026d).

> **Let intelligence traverse broadly. Let authority traverse only through governed passages.**

That rule permits more useful agents, not weaker ones.

A well-governed system can safely expose more of the legitimate enterprise request space because the agent's ability to reach an object is no longer confused with authority to make every use of it.

---

# 7. The modularity lineage and adjacent architecture

The argument belongs in the history of modular design, but the history should make one move and stop. The purpose of the comparison is not to claim novelty by analogy. It is to show that architecture already learned to control the propagation of local decisions; this paper extends that concern to the propagation of authority.

Software engineering learned that tightly coupled systems are difficult to maintain because local implementation decisions propagate too far; Parnas's modularization argument remains a foundational statement of this design concern (Parnas 1972).

A compact lineage is sufficient:

> **Decomposition localized complexity.**  
> **Information hiding localized change.**  
> **Component interfaces localized implementation dependency.**

The present argument extends the concern from change to authority.

> **Ontological separation localizes authority.**

Classical modularity asks how to prevent one component's implementation choices from becoming unnecessary dependencies elsewhere.

Multi-world governance asks how to prevent one world's legitimate authority from silently acquiring force in another.

A business definition should not automatically become analytical identity.

A physical key should not automatically become Data World identity.

A shared entity reference should not automatically carry every predicate.

A graph merge should not automatically license analytical derivation.

A successful query should not automatically acquire the standing of a business answer.

The analogy has a limit. The Business, Data, and Material Data worlds are not merely software modules. Their distinction rests on kinds of objects, governing laws, and authority. The modularity lesson matters because architecture already learned not to fuse technical components merely because they must work together.

The same restraint is more important when the boundary separates different jurisdictions of meaning and law.

## 7.1 Bounded contexts

Domain-driven design provides the nearest familiar precedent (Evans 2003).

Bounded contexts allow the same term to have different meanings in different models and make relationships among contexts explicit. That is highly compatible with the present argument.

The distinction is one of scope.

A bounded context is ordinarily a boundary around a domain model or software model. The Three Worlds distinction can cut across domains because the boundary may separate different *kinds* of governed objects: business meaning, analytical data, and material representation.

A Finance bounded context and a Support bounded context can therefore remain distinct within the Business World, while each also crosses into a shared Data World and from there into material realization.

The present argument does not replace bounded contexts. It explains why some context relationships are not merely model translation. When the boundary also crosses from business meaning into analytical law, or from analytical law into material realization, it carries a transfer of authority that must remain explicit.

## 7.2 Data mesh

Data mesh likewise contributes an important principle: domains should retain meaningful ownership rather than treating all data as the output of one central team (Dehghani 2022).

That decentralization addresses organizational and product boundaries.

The present argument adds a condition on composition.

Domain ownership alone does not determine whether two domain data products can be analytically combined, whether their identities are equivalent, or what authority a shared identifier carries across them.

A mesh can therefore remain federated organizationally while still tightly coupling worlds if shared reference, shared schema, or material compatibility is treated as sufficient analytical license.

Federation of ownership does not by itself guarantee separation of authority.

The crossing remains necessary.

## 7.3 Data contracts

Data contracts make producer-consumer obligations explicit and can carry schema, quality, operational, and governance expectations; the Open Data Contract Standard is one current example (Bitol 2025).

They are natural implementation surfaces for some crossing obligations.

The distinction again is jurisdiction.

A contract can govern material delivery without establishing analytical identity. It can record a semantic relation without proving every lawful derivation that follows from it.

The important requirement is not the label *contract*. It is that the relation crossing a boundary be explicit enough that each kind of authority remains accountable.

These adjacent practices therefore support rather than dissolve the argument.

They show that modern architecture is already moving toward explicit boundaries.

The additional claim here is that **authority propagation across ontological worlds must itself be treated as a first-class design concern**.

---

# 8. The honest trade

A central semantic settlement has real economic value.

Where participants genuinely share one authoritative meaning, identifier, and set of consequences, centralization reduces repeated negotiation. Later applications can reuse the agreement cheaply.

That is a major advantage.

If every application had to re-ratify the meaning of ISO currency codes, legal entity identifiers, or a genuinely enterprise-wide reporting metric, governance would become wasteful.

The paper therefore does not argue that every relation should be local or every semantic object should be duplicated.

The principle is:

> **Centralize where authority is genuinely common. Use explicit crossings where authority remains distinct.**

Governed crossings cost more than silent propagation.

Someone has to author the relation.

Evidence has to be gathered.

An accountable authority has to ratify it.

The relation must be maintained.

Some passages will not exist when a user first asks for them.

The correct response may be clarification, refusal, or escalation rather than immediate execution.

That additional friction is real.

Its deepest organizational cost is not the extra artifact or review step. **Ratification assigns ownership.** Someone or some accountable process must stand behind the claim that these two governed objects are related in this way for this purpose. A central settlement can obscure that ownership because the relation appears simply as part of the enterprise model, registry, or platform. Explicit crossings make the authority event visible.

It buys several things.

**Scoped equivalence.** A relation can hold for customer-health analysis without becoming a universal identity claim.

**Preserved local disagreement.** Finance and Support can maintain different customer concepts without blocking every combined application.

**Purpose limitation.** A relation established for analysis need not acquire standing for compensation, contractual entitlement, or regulatory reporting.

**Revision and revocation.** The passage can change without redefining its endpoints.

**Auditability.** A system can state why a relation existed and which authority established it.

**Failure diagnosis.** The system can distinguish "same referent" from "lawful analytical movement" from "servable result."

**Local change.** A domain can evolve without silently rewriting unrelated domains.

This ownership requirement is both a feature and an adoption barrier. Accountable authority is harder than inherited convention, which helps explain why tightly coupled settlements remain attractive even when their governance weaknesses are understood.

## 8.1 Does this recreate pairwise integration cost?

Explicit crossings do not require every participant to negotiate an entirely custom relationship with every other participant.

Common infrastructure can lower the cost substantially.

Organizations can share:

- global or enterprise identifiers;
- common Data World laws;
- standard relation types;
- reusable evidence patterns;
- common ratification procedures;
- shared contract formats;
- common validation services;
- common material execution infrastructure.

The architecture can standardize the machinery without forcing one universal business ontology.

This produces a different balance:

> **shared foundation, plural business semantics, governed crossings, application composition.**

The purpose of the crossing is not to maximize local uniqueness.

It is to preserve the distinctions that carry independent law or authority.

---

# 9. Design principles

The argument can be reduced to six design principles.

## 9.1 Separate where authority differs; centralize where it is genuinely shared

Integration is a requirement. Ontological merger is not.

Do not bond business meaning, analytical identity, and material representation into one object merely to make integration easier when those objects remain governed by different laws or authorities.

Conversely, where meaning, identity, law, and authority are genuinely common, shared settlement is appropriate. The principle is not decentralization for its own sake. It is to preserve distinctions that still carry independent authority.

## 9.2 Govern within each world by that world's law

Business meaning, analytical data, and material representation answer different governance questions.

One world should not silently settle another's jurisdiction merely because the same system can represent both.

## 9.3 Govern transfers through explicit, revisable crossings

When meaning, identity, standing, or authority moves between worlds or independently governed domains, represent the passage explicitly enough to govern it.

A crossing should make its endpoints, purpose, evidence, authority, permitted consequences, and limits visible. When an endpoint changes, review the crossings that depend on it rather than silently redefining unrelated domains.

## 9.4 Treat shared reference as evidence, not license

A common identifier can establish a referential fact.

It does not automatically authorize predicate propagation, analytical substitution, or unrestricted composition.

> **Permissionless reference is not permissionless authority.**

## 9.5 Allow new shared meaning to live in the relation

Integration may require a relation that neither endpoint previously contained.

Create the relation without forcing either endpoint to absorb the other.

> **The relation may be new while the endpoints remain themselves.**

## 9.6 Compose through governed crossings; let intelligence traverse broadly

Applications should consume already-governed relations and objects. Technical connectivity alone does not create authority.

AI agents may interpret, propose, compare, search, and explore across the enterprise. Their reach should be broad.

What acquires authoritative consequence should still be determined independently at the crossings.

> **Let intelligence traverse broadly. Let authority traverse only through governed passages.**

---

# 10. Conclusion

Enterprise AI architecture has good reasons to seek coherent meaning, shared identity, reusable metrics, and common data services.

The problem is not integration.

The problem is where integration is made authoritative.

Tight coupling lowers integration friction when it makes relationships implicit.

It also allows authority to propagate across worlds without a separately governed passage.

The Three Worlds perspective offers a different architecture.

Keep business meaning, governed analytical data, and material realization distinct where their laws and authorities remain distinct.

Govern the relations that connect them.

Allow a new shared relation to live in the passage when an application needs meaning that neither endpoint previously contained.

The relation can be new while the endpoints remain themselves.

Then let applications compose those governed relations without requiring a universal semantic merger first.

This is not a call for semantic fragmentation.

Common foundations remain valuable.

Shared identifiers remain valuable.

Semantic layers remain valuable.

Data contracts, bounded contexts, and federated domain ownership remain valuable.

The governing question is whether these mechanisms preserve the boundary at which one kind of authority becomes another.

That boundary becomes especially important for AI agents.

Agents can now move from language to semantic resolution, from semantic resolution to analytical construction, from analytical construction to material execution, and from results to action in one continuous process.

If the architecture has already erased the crossings, an upstream settlement can propagate through that chain at machine speed.

What was previously a coordination problem can become an authority-propagation problem.

The response should not be to reduce intelligence.

It should be to govern passage.

> **Let intelligence traverse broadly. Let authority traverse only through governed passages.**

The decisive architectural claim is therefore:

> **You cannot govern a crossing as a crossing after the architecture has erased the distinction between its two sides.**

And the resulting design principle is:

> **Separate the worlds. Govern the crossings. Compose through the crossings.**

Ontological separation does not prevent integration.

It is what makes governed integration possible.

---

# References

Bitol. 2025. *Open Data Contract Standard*. Version 3.1.0. Released 7 December 2025.

Dehghani, Zhamak. 2022. *Data Mesh: Delivering Data-Driven Value at Scale*. Sebastopol, CA: O'Reilly Media.

Evans, Eric. 2003. *Domain-Driven Design: Tackling Complexity in the Heart of Software*. Boston, MA: Addison-Wesley Professional.

Parnas, David L. 1972. “On the Criteria to Be Used in Decomposing Systems into Modules.” *Communications of the ACM* 15(12): 1053–1058. DOI: 10.1145/361598.361623.

Wang, Huayin. 2026a. *The Theory of Data: A Foundation for Analytical Identity, Derivability, and Consistency*. Version 6.1. Zenodo. DOI: 10.5281/zenodo.22013410.

Wang, Huayin. 2026b. *The Three Worlds of Analytics: Why Business Meaning, Data, and Material Data Need Different Governance*. Version 1.1. Zenodo. DOI: 10.5281/zenodo.22146487.

Wang, Huayin. 2026c. *Analytical Governance: Governing the Legitimacy of the Analytical Service*. Version 2.0. Zenodo. DOI: 10.5281/zenodo.22115819.

Wang, Huayin. 2026d. *Do Not Let Your AI Agent Govern Itself: Govern the Crossings, Then Give It Full Access*. Version 1.0. Zenodo. DOI: 10.5281/zenodo.22148861.
