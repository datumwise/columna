---
title: "Analytical Governance"
subtitle: "From User Intent to Governed Analytical Execution"
author: "Huayin Wang"
date: "Version 1.1 - 21 August 2026"
lang: en-US
papersize: letter
geometry: margin=0.9in
fontsize: 11pt
subject: "An architecture for translating user intent into a governed analytical request, establishing servability, evaluating bounded risk, and authorizing faithful execution"
keywords:
  - analytical governance
  - Theory of Data
  - analytical adjudication
  - servability
  - user intent
  - knowledge representation
  - AI agents
  - Frame-QL
  - semantic layer
  - support sufficiency
  - analytical establishment
  - risk evaluation
  - governed analytics
  - analytical execution
---

**datumwise, an independent open-source research project**  
**DOI:** 10.5281/zenodo.22046037 (supersedes Version 1.0, 10.5281/zenodo.21959749)  
**Based on:** Huayin Wang, *The Theory of Data*, Version 6.1, Zenodo DOI 10.5281/zenodo.22013410.  
**License:** Creative Commons Attribution 4.0 International (CC BY 4.0)

## Abstract

Analytical governance is often applied after a query already exists. By then, a more important decision may already have been made implicitly: what analytical object the user intended, and whether that object is entitled to be served.

This paper develops analytical governance as an architecture from user intent to governed execution. It identifies two gaps. The **intent gap** separates ordinary human language from an explicit analytical request. The **servability gap** separates a faithfully framed request from one that is both adequately supported by current data and analytically established under the laws governing that data.

Closing those gaps requires an authoritative middle representation between prose and procedure. Free-text documentation carries meaning but is weak as machine authority. SQL and code are executable but may encode a procedure while leaving analytical identity implicit. A machine-readable governed analytical model makes the requested object, its support requirements, and its lawful derivations independently adjudicable.

Only after servability is established should three remaining risks be evaluated: **cost**, **security**, and **result/application** risk. Analytical violations are not risks that can be accepted; they are unestablished requests.

> **Analytical governance translates user intent into an explicit analytical request, independently establishes that the request is supported by current evidence and analytically lawful under a machine-readable governed model, evaluates only the remaining cost, security, and result/application risks, and only then authorizes execution.**

# 1. A number the database can compute but governance cannot yet serve

Suppose a user asks:

> **What was average revenue per open store yesterday?**

The warehouse contains revenue observations for 47 stores. A separate governed store calendar says that 50 stores were open yesterday. Of the three open stores without ordinary sales observations, two are governed as zero-revenue store-days under the applicable support rule and one has a feed failure.

Several executable computations are possible.

A query over the sales table alone can divide total revenue by 47 observed stores. An outer join to the open-store population can divide by 50. A third calculation can exclude the one store whose feed is unavailable and divide by 49. All three can be written in valid SQL. All three can return a plausible number.

The database engine cannot determine from execution alone which number is entitled to answer the user's question.

Before execution, the system must establish at least four things:

1. what **open store** means in the local governed environment;
2. which 50 store-days actually belong to the requested population;
3. how the three store-days without ordinary sales observations are supported or unsupported; and
4. what analytical quantity the phrase **average revenue per open store** denotes.

This is the architectural problem. A query is too late a place to begin governance because the most important analytical decisions may already be embedded inside it.

Two gaps must be crossed before execution:

- the **intent gap**: from the user's language to an explicit analytical request;
- the **servability gap**: from that explicit request to one that is adequately supported and analytically established.

The architecture is therefore:

```text
User intent
    |
    v
Intent translation and analytical framing
    |                 [Intent gap]
    v
Explicit analytical request
    |
    v
Servability
  - support sufficiency
  - analytical establishment
    |                 [Servability gap]
    v
Bounded risk evaluation
  - cost
  - security
  - result/application
    |
    v
Authorization
    |
    v
Trusted planning and execution
```

Clarification can return the process to the user. Planning can report physical constraints back to governance. Neither interpretation nor planning may silently substitute a different analytical request.

> **Governance must settle analytical meaning and servability before physical execution receives authority.**

The rest of the paper explains why each part of the architecture is necessary.

# 2. The missing middle: knowledge must be represented for adjudication

Analytical knowledge is commonly captured in two useful but incomplete forms.

**Free text** carries meaning. Documentation, glossaries, metric descriptions, examples, caveats, and business language can explain what *open store* means or why a particular denominator matters. But prose is weak as deterministic authority. Definitions can conflict, conditions can remain implicit, and a statement such as *count every store that was open, even if it had no sales* does not by itself create a machine rule that rejects a calculation over observed sales rows only.

**SQL and code** carry executable procedure. A metric can be reified as:

```sql
SUM(net_revenue)
```

or as a much larger query. This is reproducible and operationally useful, but it may leave implicit the population, analytical location, lawful continuation rules, support requirements, sufficient state, or lineage identity of the quantity being computed.

The architecture therefore needs a third representation. The jurisdictional case for that representation — that analytical data carries its own ontology, distinct from the business ontology carried in data and from storage and logical form — is made in the companion paper *Data Has Its Own Ontology* (Wang 2026f).

| Representation | Good at | Limitation as sole governance substrate |
|---|---|---|
| Free text / documentation | meaning, explanation, local vocabulary | weak deterministic adjudication |
| SQL / executable code | physical realization | procedure can under-specify analytical identity |
| Governed analytical model | identity, analytical law, support, verification | still needs semantic grounding and physical realization |

> **Prose can describe analytical meaning. SQL can execute a procedure. Governance requires the analytical object between them.**

The Theory of Data (ToD) supplies one logical vocabulary for this middle representation. A compact vocabulary is enough for the architecture developed here:

- **Universe** — the governed domain of analytical points, including the law by which those points exist.
- **Anchor** — a governed partition of that universe.
- **Measure family** — a uniquely governed analytical quantity family.
- **Measure, $F@A$** — a measure family at an anchor.
- **Sufficient state** — the state required for lawful analytical continuation.
- **Contract, $\Gamma(e)$** — the conditions under which a proposed analytical derivation is licensed.

The full definitions and formal treatment are in *The Theory of Data*, Version 6.1, which additionally makes the identity criterion for measure families operationally explicit: family identity is fixed ex ante by declared structure, a distinction this paper's intent-translation stage depends on. Readers wanting a shorter conceptual entry point may begin with *A Primer on the Theory of Data*, Version 2.2 (DOI: 10.5281/zenodo.22018549), which is aligned with the Version 6.1 foundation.

This middle representation does not eliminate prose or SQL. AI can help translate human and organizational language into governed analytical objects. Trusted planners can translate an adjudicated analytical request into SQL or another physical execution plan. The governed analytical model is the authoritative middle against which the request can be checked independently.

The alternative is not zero complexity. It is complexity left implicit in documentation, SQL, schemas, middleware, naming conventions, and model behavior.

Two boundary statements complete the category. First, the boundary with data governance:

> **Analytical governance decides which analytical results may be served. It is distinct from data governance, which governs the stewardship, access, quality, and control of data assets. The two compose; neither substitutes for the other.**

Second, the position of analytical governance among the bodies of law it coordinates. Analytics is not governed by one body of law. Governed data, inferential models and claims, and authorized action answer to distinct correctness conditions, and a real analytical act may traverse several jurisdictions. Analytical governance is therefore a meta-framework: it tracks which law has jurisdiction, whether an operation is interior or a crossing, what warrant and authority survive each passage, and whether the serving boundary may Serve, Disclose, Clarify, or Refuse — or whether governance itself must Escalate. Across both within-world and crossing contexts, it keeps capability distinct from legitimacy: what can be computed or transported does not by itself determine what may be served or authorized. It supplies the interior law of no world it composes. It has wider scope, not higher sovereignty.

The category's membership test follows from this architecture:

> **A governed analytical system must be capable of withholding analytical permission. If it cannot refuse, it is not governed.**

# 3. The intent gap

The open-store question looks simple because the user speaks naturally:

> **What was average revenue per open store yesterday?**

The user should not be required to know a warehouse table, a semantic-layer metric identifier, a universe name, or the distinction between supported zero and unavailable observation. The system must translate between the user's conceptual world and the governed analytical world.

The first translation is:

$$
\text{human intent}
\longrightarrow
\text{candidate governed analytical request}.
$$

## 3.1 Semantic grounding is not analytical framing

Local semantic knowledge may establish that:

```text
"open store" -> stores scheduled and eligible for trade on the requested day
"revenue"    -> governed net revenue family
```

That is necessary grounding. It is not yet analytical adjudication.

The system must still determine whether the requested population is a governed population, whether the Revenue measure exists at the relevant analytical location, and what denominator and support conditions belong to the requested quantity.

Semantic knowledge answers:

> What local concept does the user's phrase refer to?

Analytical knowledge answers:

> What governed analytical object exists, and what laws and support conditions apply to it?

## 3.2 AI is well suited to translation, not authority

AI agents are useful because interpretation is uncertain. They can search definitions, connect user vocabulary to local terms, retrieve candidate governed objects, explain distinctions, and propose candidate requests.

But probabilistic plausibility must not become analytical authority.

If a user asks for **maximum revenue** and two governed identities remain possible—maximum single-order revenue and maximum daily revenue—the system should surface the distinction. It should not choose one because the language model assigns it higher probability.

**Clarify** is appropriate when the remaining distinction is something the user can settle. **Escalate** is appropriate when resolution requires a new governed definition, new evidence, or another governance authority.

The role division is therefore:

$$
\text{AI: intent} \rightarrow \text{candidate analytical request}
$$

while the governed layer determines whether that candidate is uniquely identifiable and servable.

This division has an adjacent counterpart in agent-infrastructure research. Tomašev, Franklin, and Osindero (2026) develop a governance framework for authority transfer in agent networks — delegation with contract-first decomposition, signed attestation, and privilege attenuation — and identify the "zone of indifference" in which agents comply without scrutiny, arguing for the engineered capacity to challenge or reject requests. As we read the two frameworks (the comparison is this paper's synthesis, not a claim of theirs), their verification stack certifies that delegated work was executed as specified, while analytical adjudication certifies that the specified work was analytically lawful; the two layers compose, and neither substitutes for the other.

# 4. The servability gap

A faithful interpretation can still be unservable:

$$
\text{faithful request}
\not\Rightarrow
\text{servable request}.
$$

The servability gap has two distinct halves:

$$
\boxed{
\text{Servable}
=
\text{Support Sufficient}
\land
\text{Analytically Established}
}
$$

The distinction matters because the two failures have different causes and different remedies.

## 4.1 Support sufficiency

Support sufficiency is contingent. It asks whether the evidence and state required by this request are presently available.

For the open-store request, the analytical population contains 50 open store-days. But current evidence differs across those points:

- 47 have ordinary sales observations;
- 2 are supported as zero-revenue store-days under the governed support rule;
- 1 is open but its sales feed is unavailable.

The population does not shrink merely because one observation is missing. Nor does absence automatically become zero. The system must know which points exist, which are eligible, which are supported, and which required observations or states are unavailable.

Support sufficiency also covers cases where an analytical object is lawful but the material state required to compute it has been lost. A finalized average can exist while its $(sum,count)$ state is unavailable. An exact distinct count can exist while the identity set or other exact compositional state has not been retained. The general treatment of certifiable state and its loss is given in Wang (2026e).

This is different from general **data quality**. Data-quality systems test properties of datasets and pipelines—schema conformity, freshness, null rates, uniqueness, and similar conditions. Those checks may supply evidence used in a sufficiency determination. Passing them does not by itself prove that this particular analytical request has the support and state it requires.

> **An analytical object can be logically established and still be presently unservable because its required support or material state is unavailable.**

## 4.2 Analytical establishment

Analytical establishment is structural. It asks whether the requested object exists under the governed analytical model and whether the proposed derivation is lawful.

For a proposed reduction from source anchor $B$ to target anchor $A$, the structural diagnostic order is:

$$
\boxed{
B?
\;\rightarrow\;
F@B?
\;\rightarrow\;
B \succ A?
\;\rightarrow\;
\Gamma(e)?
}
$$

That is:

1. Is $B$ a governed anchor?
2. Does the source measure $F@B$ exist?
3. Does the required refinement $B \succ A$ hold for ordinary reduction?
4. Is the transformation licensed by its governed contract $\Gamma(e)$?

The governing law may require sufficient state for exact continuation. Whether that required state is actually available now is then a **support-sufficiency** question, not a different analytical law.

Different familiar failures stop at different obligations. Fan-out can manufacture a row grouping that is not an anchor. A join can repeat a value over a legitimate finer anchor without establishing $F@B$. Inventory can begin from a valid source measure while SUM remains unlicensed across time. A lawful average can pass all four structural checks and still be presently unservable because its required $(sum,count)$ state was not retained.

The first three examples are failures of analytical establishment; the last is support insufficiency. None is repaired by risk acceptance.

> **Analytical violations are unestablished, not risks.**

A missing feed and an unlawful reduction can both make a request unservable, but they are not the same kind of failure. The first is contingent support insufficiency. The second is failure of analytical establishment.

## 4.3 Request-language expressiveness

The request crossing the adjudication boundary must carry enough information to identify the intended analytical object. That does not mean every request language must expose every ToD concept directly.

The requirement is narrower:

> **Every identity-bearing distinction required for adjudication must be explicit in the request or uniquely derivable from the governed model.**

Consider:

```text
table-spec
  dimensions: [region, quarter]
  metrics: [average_revenue]
```

This is fully adjudicable if `average_revenue` uniquely denotes a governed metric whose identity already determines its source grain, population, and lawful derivation. If the governed environment contains both `average_order_revenue` and `average_customer_revenue`, and `average_revenue` resolves to neither uniquely, the table-spec remains under-specified.

The architecture should not make identity-bearing distinctions impossible to state and then allow middleware or an AI model to choose them silently.

# 5. Risk and authorization

Risk evaluation begins only after support sufficiency and analytical establishment have been determined.

**Cost risk** asks whether an otherwise servable request is too expensive, slow, or resource-intensive under current policy. Cost policy may deny, defer, or authorize a separately governed approximation where one exists. It may not silently redefine the analytical request.

**Security risk** asks whether the requester and execution environment are authorized to access the required data, tools, sources, and operations. Separating interpretation, adjudication, and execution allows probabilistic components to propose requests without automatically acquiring execution authority.

**Result/application risk** concerns limitations on presenting or using an otherwise servable result. Partial but disclosed coverage, an approved approximation that must not be presented as exact, or data suitable for periodic reporting but not immediate operational action are examples. Result/application risk is **not** a general theory of statistical validity, causal identification, or decision quality; those questions belong to neighboring statistical or decision frameworks. For the passage from governed data to licensed statistical claims specifically, the governing framework in this corpus is *The Statistical Bridge* (Wang 2026d).

Risk can constrain execution or serving. It cannot legalize an analytically unestablished request.

# 6. Five architectural patterns, one request

The architectural differences become clearer when every pattern is asked to answer the same question:

> **What was average revenue per open store yesterday?**

The question is not which product category is best. It is where analytical intent becomes explicit, what knowledge is available to adjudicate it, and who has authority to turn a candidate meaning into execution.

MCP, where used, is a transport or tool boundary. It does not itself supply analytical governance; those properties come from the representation and service behind the boundary.

## 6.1 Pattern A: natural language to text-to-SQL

```text
User NL -> AI Agent -> SQL -> SQL Engine
```

The agent may translate the request directly into something like:

```sql
SELECT SUM(revenue) / COUNT(DISTINCT store_id)
FROM sales
WHERE day = :yesterday;
```

The query is executable. It also silently makes the observed sales table define the denominator population. The 50-store governed open-store population never becomes an explicit object against which the query can be checked.

A SQL validator can catch syntax, access, scan cost, or declared anti-patterns. It cannot prove that dividing by the 47 stores present in the sales table answers *per open store* unless the intended population has been represented independently.

Pattern A collapses intent interpretation and physical procedure too early.

## 6.2 Pattern B: structured table-spec

```text
User NL
   -> AI Agent
   -> table-spec {dimensions + metrics}
   -> service / MCP
   -> SQL Engine
```

The request might become:

```text
dimensions: [day]
metrics: [average_revenue_per_open_store]
```

This is a major improvement if the metric already carries the governed denominator population, support behavior, source grain, and lawful derivation. The agent no longer chooses joins and aggregation mechanics directly; a service or compiler owns physical planning.

If the metric definition contains only a formula or SQL fragment, however, the ambiguity has merely moved into the metric. The architectural question is not whether the request is structured, but whether the governed metric plus environment determines the full analytical identity and can be independently adjudicated.

## 6.3 Pattern C: context or semantic-layer mediation

```text
User NL -> AI Agent <-> Context / Semantic Layer -> SQL / compiler -> Engine
```

A context or semantic layer can tell the agent what **open store** means, identify the Revenue metric, expose preferred relationships, and substantially improve translation.

Two different architectures can still hide under this pattern. In one, semantic context merely informs model-authored SQL. In the stronger form, an authoritative semantic layer accepts a structured request and constrains or owns compilation.

For the open-store case, the decisive question is concrete: can the layer independently establish the 50-point open-store population and distinguish the 47 observed sales points, the 2 governed zero-revenue points, and the 1 unsupported point? If yes, it is performing substantial analytical governance for this case. If not, better context may still produce better SQL, but the support distinction remains outside independent adjudication.

The relevant question is therefore not whether a semantic layer exists, but what analytical distinctions it can represent and enforce.

## 6.4 Pattern D: ToD-native analytical request

```text
User NL
   -> AI Agent
   <-> semantic / local knowledge
   -> Frame-QL or equivalent analytical request
   -> governed analytical model / adjudicator
   -> trusted planner
   -> backend data engine
```

Here the object crossing the governance boundary is already an analytical request rather than a physical procedure. A ToD-native request can refer to governed analytical objects whose universe, anchor, family identity, support expectations, and lawful derivations are available to the adjudicator before physical planning.

Frame-QL is natural in this architecture because its request objects align with the analytical objects ToD governs. That alignment reduces the amount of analytical intent that must be reconstructed from physical procedure.

But ToD governance does not require Frame-QL or any particular implementation of the governed-model and adjudication roles.

## 6.5 Pattern E: declared analytical target plus candidate SQL

```text
declared analytical target
          +
     candidate SQL
          |
          v
 independent adjudication
          |
          v
      SQL Engine
```

Pattern E separates analytical authority from the SQL implementation without requiring a new request language or warehouse architecture.

For the open-store question, the analytical target is declared independently—for example as the governed measure corresponding to average revenue over the open-store-day population. Existing or agent-generated SQL is then treated as a **candidate realization** of that target.

The verifier can ask two different questions:

1. Is the declared analytical target itself supported and analytically established?
2. Does the candidate SQL faithfully realize that target?

A query dividing by the 47 observed sales stores can therefore be rejected as an implementation of the declared target even though the SQL is valid and executable.

This pattern is strategically important because it supplies an incremental adoption path. An organization can begin with a handful of high-value governed analytical targets, retain its existing warehouse and SQL estate, and insert independent adjudication between declared intent and execution. The governed model can expand progressively rather than requiring complete formalization before any benefit is available.

Pattern E demonstrates a broader principle:

> **ToD governance requires an independently identifiable analytical target; it does not require that the target be expressed in Frame-QL.**

## 6.6 Comparative view

| Pattern | AI translates into | Analytical target explicit? | Independent adjudication? | Adjudication point | Physical authority |
|---|---|---:|---:|---|---|
| A. Text-to-SQL | SQL procedure | Often no | Weak unless reconstructed | post-hoc validator, if any | largely model-authored |
| B. Table-spec | `{dimensions + metrics}` | Depends on governed metric model | Possible | metric/service compilation boundary | service/compiler |
| C. Context / semantic layer | grounded SQL or semantic request | Varies | Varies | semantic middleware when authoritative | model or semantic compiler |
| D. ToD-native request | governed analytical request | Yes by design | Yes | pre-planning analytical adjudicator | trusted planner/engine |
| E. Declared target + SQL | target + candidate implementation | Yes | Yes | verifier/gateway before execution | execution layer after verification |

This is not a universal ranking. A sufficiently expressive and authoritative semantic system can satisfy the same architectural requirements under different terminology. The table identifies the information and authority boundaries that must exist somewhere if the result is to be independently governed.

# 7. The Analytical Adjudication Layer

The architecture requires an independent responsibility between interpretation and execution.

Conceptually, the analytical adjudicator consumes:

```text
candidate analytical request
+ governed analytical model
+ current support/materialization evidence
```

and returns something like:

```text
analytical determination
+ canonical identity, when uniquely determined
+ support determination
+ reasons
+ alternatives, when relevant
+ conditions / disclosures required if later served
```

The important authority boundary is subtle:

> **The adjudicator may canonicalize a uniquely determined request. It does not choose among unresolved analytical meanings on the user's behalf.**

If `revenue` maps uniquely to one governed family, canonical lookup is deterministic. If `maximum revenue` could lawfully denote maximum order revenue or maximum daily revenue, the adjudicator returns **Clarify** rather than choosing one.

Analytical adjudication can therefore terminate early with **Clarify**, **Refuse**, or **Escalate**. If the request is determinate and servable, its analytical determination proceeds to bounded risk evaluation and authorization.

The **full governance process**, after those later stages, produces five externally meaningful outcomes:

- **Serve** — the request is determinate, servable, authorized, and may be returned under its governing conditions.
- **Disclose** — the request is servable and authorized, but material support or application conditions must travel with the result.
- **Clarify** — a user-resolvable analytical ambiguity remains.
- **Refuse** — the requested answer cannot be served under the current analytical, support, risk, or authorization conditions.
- **Escalate** — resolution requires new governance authority, evidence, definition, or qualified review.

One distinction inside this outcome vocabulary deserves explicit statement, because implemented systems expose it structurally. Serve, Disclose, Clarify, and Refuse are the **serving vocabulary**: what a governed system returns to a requester at the machine boundary. Escalate is the **governance-process outcome** that crosses the system boundary, because the existing governed world cannot resolve the request:

> **Clarify stays inside the constitution. Escalate reaches the constitution's edge. A clarification asks the requester to choose among already governed meanings. An escalation requires new meaning, evidence, authority, or qualified review — a governance action rather than a fifth analytical serving verdict.**

The soundness condition on the serving boundary can then be stated in one sentence:

> **Every served answer must be entitled under the declared analytical meaning and current support; unestablished answers must be withheld.**

These findings should be machine-consumable. An AI agent can use a clarification reason or a set of governed alternatives to continue the dialogue or reformulate a request.

> **The agent may respond to adjudication. It does not overrule adjudication.**

Trusted planning can also report physical constraints: a binding may be absent, exact state may not be materialized, a plan may be unexpectedly expensive, or an access boundary may be encountered. Those findings can flow back into support determination, risk evaluation, or authorization.

> **Planning may report constraints; it may not silently substitute a different analytical request.**

# 8. Returning to the open-store result

The original request was:

> **What was average revenue per open store yesterday?**

The architectural trace is now short and explicit.

**Intent translation**  
`open store` resolves to the governed open-store-day population; `revenue` resolves to the governed Revenue family.

**Support sufficiency**  
50 store-days exist and are eligible. 47 have ordinary revenue observations. 2 are supported as zero-revenue store-days under the governed support rule. 1 is open but currently unsupported because its feed is unavailable.

**Analytical establishment**  
The requested denominator population is a governed analytical population, Revenue exists at the required analytical location, and the requested derivation is lawful. There is no analytical violation.

**Adjudication**  
The requested all-store measure is analytically established but not presently support-sufficient because one of the 50 eligible store-days lacks required revenue evidence. The adjudicator can report that reason and, if one is separately governed, identify a supported-population alternative. It must not silently divide by the 47 observed sales rows and call the result *average revenue per open store*.

**Risk and authorization**  
If the missing support becomes available, or the user selects a separately governed servable alternative, cost and security determine whether execution is authorized. Result/application conditions determine whether the final governance outcome is **Serve** or **Disclose** and what disclosure must accompany the result.

The arithmetic was never the hard part. The hard part was making the population, support state, analytical identity, and serving authority explicit before a computation was allowed to stand as the answer. How warrant and authority compose across longer chains of governed worlds and crossings — beyond the single passage examined here — is the open research program this architecture points toward.

# 9. Requirements, adoption, and scope

A conforming architecture needs:

- machine-usable semantic knowledge for grounding user language;
- a governed analytical representation rich enough for distinctions that affect identity, support, and derivability;
- a request boundary at which all identity-bearing distinctions are explicit or uniquely derivable;
- independent support-sufficiency and analytical-establishment checks;
- bounded evaluation of cost, security, and result/application risk;
- the capacity to withhold analytical permission — a system that cannot refuse is not governed;
- and trusted physical execution faithful to the adjudicated request.

ToD provides a logical foundation for the analytical portion of this requirement. Frame-QL is ToD-native because it speaks naturally in governed analytical objects, but neither Frame-QL nor any one product or protocol is required.

Adoption can be incremental. Organizations can begin with a small set of high-value measures, existing semantic definitions, and existing SQL. Pattern E allows those analytical targets to be declared independently and existing SQL to be verified against them. Over time, the governed analytical model can absorb stronger identity, support, lineage, and contract information.

The architecture does not guarantee perfect intent, perfect data, or perfect governed declarations. It does not replace semantic knowledge, statistical inference, security engineering, physical optimization, or decision governance. Explicit analytical governance also has real cost: governed identities, contracts, support conditions, and sufficient state must be maintained.

Again, the alternative is not zero complexity. It is complexity resolved implicitly by whichever component happens to act first.

# 10. Conclusion

A valid query is not yet an authorized analytical answer.

The open-store example required no exotic mathematics. The difficulty was that several executable computations existed while only a governed representation of the intended population, support conditions, and analytical identity could establish which result—if any—was entitled to answer the user.

That is why analytical governance must begin before the query.

Human intent must be translated into an explicit analytical request. The request must be checked separately for support sufficiency and analytical establishment. Analytical violations remain unestablished rather than becoming risks that an organization can accept. Only then should cost, security, and result/application risk determine what execution and serving authority the request receives.

The architecture therefore separates three powers:

$$
\boxed{
\text{interpretation}
\neq
\text{analytical adjudication}
\neq
\text{physical execution}
}
$$

AI has a natural role in the first because interpretation requires flexible search over language and local knowledge. Governed analytical structure is required for the second because analytical authority must be independently testable. Trusted planners and engines own the third because execution must faithfully realize what has already been established.

> **Translate intent. Establish servability. Evaluate bounded risk. Authorize deliberately. Execute faithfully.**

That is the path from a human question to a result that is not merely computable, but entitled to answer it.

# References

Tomašev, Nenad, Matija Franklin, and Simon Osindero. 2026. *Intelligent AI Delegation*. arXiv:2602.11865.

Wang, Huayin. 2026a. *The Theory of Data: A Foundation for Analytical Identity, Derivability, and Consistency*. Version 6.1. Zenodo. DOI: 10.5281/zenodo.22013410.

Wang, Huayin. 2026b. *A Primer on the Theory of Data*. Version 2.2. Zenodo. DOI: 10.5281/zenodo.22018549.

Wang, Huayin. 2026c. *Frame-QL: An Introduction — Query by Declaring the Result*. Version 1.2. Zenodo. DOI: 10.5281/zenodo.21890891.

Wang, Huayin. 2026d. *The Statistical Bridge: From Governed Evidence to Inference Certificates and Licensed Claims*. Version 3.0. Zenodo. DOI: 10.5281/zenodo.21979821.

Wang, Huayin. 2026e. *Certifiable State Under Information Loss: Governed Derivability, Claim Transport, and Approximate Closure*. Version 1.0. Zenodo. DOI: 10.5281/zenodo.21972541.

Wang, Huayin. 2026f. *Data Has Its Own Ontology: Not Borrowed from the World It Describes*. Version 1.1. Zenodo. DOI: 10.5281/zenodo.22026962.

# Revision Note (Version 1.1)

Version 1.1 is an alignment-and-wiring revision executed from a ratified revision record (21 August 2026). Changes: (1) the serving/governance distinction stated in §7 — Serve, Disclose, Clarify, Refuse as the serving vocabulary; Escalate as the governance-process outcome at the constitution's edge; (2) the category's membership test added to §2 and §9: a system that cannot refuse is not governed (adopted into canon from the 2026 site formulation); (3) the serving-boundary soundness condition stated in §7; (4) the boundary with data governance stated in §2; (5) the multi-world positioning paragraph added to §2, with the composition research program noted in §8; (6) citation wiring: The Statistical Bridge (§5), certifiable state (§4.1), the ontology companion (§2), the foundation reference updated to ToD v6.1, and adjacent agent-delegation work (§3.2, with the comparative reading marked as this paper's synthesis). Non-changes: the five-outcome structure, the two-gap architecture, the Servable factorization, the worked example, and Patterns A–E stand unmodified. The full record, including provenance and explicit non-changes, is retained in the project archive.
