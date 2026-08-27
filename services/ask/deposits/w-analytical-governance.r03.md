# Analytical Governance: Governing the Legitimacy of the Analytical Service

**Huayin Wang**  
**Version 2.0 · 26 August 2026**  
**DOI:** 10.5281/zenodo.22115819

## Abstract

Analytics exists to serve a user with a purpose. The service may be performed by people, software, AI agents, or combinations of them, but the governing problem is the same: the user's purpose must survive the passage from expressed intent to analytical meaning, from analytical meaning to a governed object, from that object to a produced result, and from the result to an answer or consequential use.

Analytical Governance is the discipline governing the legitimacy of the analytical service. Legitimacy means that the service preserves the user's purpose, establishes the analytical result under the relevant analytical law and support, and carries no more authority into serving or use than those grounds warrant. The service is governed through process, practice, and architecture so it remains faithful, reliable, and sufficiently grounded for the reliance placed on its result.

The Theory of Certainty supplies the upstream discipline for asking what grounds carry a conclusion, what they establish, where their warrant stops, and whether they can bear the intended reliance (Wang 2026d). Analytical Governance turns those questions into a governed analytical service.


> Service is the mission. Servability is a governing gate.

Request — the governed analytical formulation of the user's purpose.

Result — the product of the governed analytical process.

Answer — a result served as responsive to the request.

Servability — whether the result has the analytical permission required to be served as that answer.

Standing — what the result or answer may be treated as, or relied upon for, at a boundary.

Constitution — the ratified governed world of analytical meaning, law, support rules, and authority against which serving is adjudicated.


## 1. Analytics is a service relationship

An analytical system does not exist merely to compute. It serves someone who is trying to know, decide, explain, monitor, compare, or act. That purpose matters because a technically correct result can still fail the service.


> What was average revenue per open store yesterday?

Revenue rows arrive for 47 stores. A roster establishes that 50 stores exist. An operating-status source establishes that 48 were open yesterday. The arithmetic can divide total observed revenue by 47, 48, or 50. The computation does not tell us which answer serves the user's purpose.

If the system returns the mean over reporting stores while presenting it as average revenue per open store, the arithmetic may be flawless and the service unfaithful. If it identifies the correct population but uses stale or incomplete state, the interpretation may be faithful and the production unreliable. If it produces a plausible number whose grounds cannot bear the intended use, the answer may still be unservable.

Analytical Governance therefore protects more than correctness. It protects the integrity of an analytical service from purpose through use.


> The governing question is not only whether the system can produce a result. It is whether the analytical service has preserved what the user is entitled to rely on.


## 2. What must remain true


> User purpose → analytical intent → governed analytical construction → reliable production → servability → warranted reliance → consequential use

This is an operational cut through the analytical service, not a replacement taxonomy for the foundational domains whose laws the service uses. Different systems may combine functions. Governance requires that the distinctions remain visible enough to adjudicate.

The legitimacy definition states what must hold at the service boundary; faithfulness, reliability, and certainty sufficient for reliance are the operational obligations by which those conditions are maintained through the service passage.


### 2.1 Faithfulness

Faithfulness asks whether the service preserves the user's purpose as it becomes an analytical request and answer. It also requires enablement: the service should help the user articulate analytically meaningful distinctions that the user may not initially know how to express. A plausible metric, valid SQL, or familiar number is not enough. Identity-bearing distinctions that determine what question is actually being answered must survive the translation.


> Fidelity prevents the system from saying something different from what the user means. Enablement helps the user say more precisely what the user is trying to know. Neither authorizes the system to choose silently on the user's behalf.


### 2.2 Reliability

Reliability asks whether the governed analytical process can produce the established result consistently under the relevant conditions. It includes data availability, state, execution, materialization, and reproducibility. Reliability does not create analytical meaning; it preserves and produces what has already been formulated and established.


> Reliability may not silently alter the analytical object in the course of production. A reliable production path must reproduce and carry forward the object that was actually established.


### 2.3 Certainty sufficient for reliance

The Theory of Certainty asks what grounds warrant confidence in a result and whether those grounds can bear the reliance at issue (Wang 2026d). Analytical Governance ensures that the relevant grounds are established, preserved, and respected as the service crosses from request to answer and from answer to use.


## 3. The intent gap: from purpose to governed request

The first gap is the distance between what the user can initially express and the analytical request that faithfully captures the user's purpose with the distinctions needed for governance. Closing it has two obligations: preserve the purpose, and enable better articulation.

AI and semantic systems can search vocabulary, retrieve definitions, expose governed distinctions, propose interpretations, explain alternatives, and formulate a candidate governed request. This is not merely translation. A good analytical service can expand the user's expressive capacity by making relevant distinctions available for the user to articulate.

For example, a user may ask for “average revenue.” The service can surface governed alternatives such as average among reporting stores, existing stores, or stores that were open, explain the difference, and let the user choose. That is enablement. Silently selecting one of those meanings would be unauthorized formulation by the serving system, not enablement.

Enablement must not conceal materially relevant governed alternatives. If the service surfaces a selective set rather than the relevant governed set, that selectivity must itself be governed or disclosed.


> The intent gap is closed when the user's purpose has been formulated—through preservation and, where useful, enablement—as an analytical request explicit enough for independent adjudication.

If multiple already-governed interpretations remain and the user can choose among them, Clarify. Clarification is therefore not merely ambiguity handling; it is one mechanism by which the service enables better articulation without taking authority over the user's meaning. If faithful service requires meaning, evidence, or authority that does not yet exist inside the governed environment, Escalate.


## 4. The servability gap: from governed request to answer

A faithfully formulated request can still fail to produce a servable answer.


> Faithful request does not imply servable request.


> Servable = Support Sufficient AND Analytically Established

Analytical establishment asks whether the requested analytical object exists under the governed analytical model and whether the requested derivation is lawful (Wang 2026a). Support sufficiency asks whether the evidence and sufficient state required by this request are presently available; the distinction between a lawful analytical object and the retained state required for exact continuation is developed further in *Certifiable State Under Information Loss* (Wang 2026c).

Time-sensitive state must be typed carefully. A late-arriving or retroactively corrected record does not necessarily change the identity of the analytical object; it may instead change whether the required state was support-sufficient when the answer was served. If the governed definition itself is versioned over time, however, analytical identity may also change (Wang 2026a; Wang 2026c).

A missing feed may leave a lawful request unsupported. An unlawful reduction may leave abundant data unable to establish the requested result. An unresolved population may make a computable denominator analytically unestablished.

The Theory of Certainty clarifies why confidence of the wrong kind cannot repair these failures. Observed feed regularity cannot silently establish a population rule. Model accuracy cannot establish claim-specific analytical authority. Risk tolerance cannot legalize an unestablished analytical object.


> Computability does not imply servability.

Servability is not a generic property of a dataset, metric, model, or platform. It is a determination about a particular analytical request under current grounds.

A result may be servable and still not be served. Servability establishes analytical permission for the requested answer; later authorization, risk, and disclosure conditions determine the serving outcome.


## 5. Governance responses

When the service passage is incomplete, governance needs responses other than answer production. The familiar outcomes preserve different kinds of honesty.


### Serve

Serve when the request is determinate, the required analytical and support grounds are established, the result is authorized for the intended use, and no material condition requires separate disclosure.


### Disclose

Disclose when a result may be served but a material condition must travel with it. Disclosure preserves the boundary of the warrant.


### Clarify

Clarify when the missing distinction is inside the existing governed world and the requester can resolve it. Clarification protects faithfulness to purpose; it does not create new analytical authority.


### Refuse

Refuse when the requested answer cannot be served under the current analytical, support, risk, or authorization conditions. Refusal is evidence that analytical permission is real.


### Escalate

Escalate is not a fifth serving mood. It is a governance-process transition when faithful service requires something the current governed world does not possess: new meaning, new evidence, new authority, or qualified review. The request leaves the serving path and enters an authoring, declaration, review, or ratification process capable of changing the governed world.

Escalation returns either a ratified change to the governed constitution or a decision not to change it. Until that return path completes, serving remains unresolved; escalation does not produce an unofficial answer.


> Clarify stays inside the constitution. Escalate reaches the constitution's edge.


## 6. The governed world is authored, not assumed

Analytical service operates against a governed constitution of analytical meaning, law, support requirements, and authority. That constitution must be declared, reviewed, and ratified through a process separate from serving.

Serving applies the current constitution. Authoring changes or extends it through an authority event that can be reviewed and ratified.

> A serving system must not silently create the missing meaning or authority that would make its own answer servable.

When serving reaches the edge of the constitution, Escalate closes the loop: unresolved need → authoring or declaration → review and ratification → governed constitution → serving.

## 7. Standing: what the service may pass forward

Servability asks whether a candidate result may be served as the answer. Consequential use creates a further question: what may the served result now be treated as?

Standing is claim- and boundary-specific. A result may stand for exploratory display and not for compensation. A statistical estimate may stand as an estimate and not as a causal claim. A result may require disclosure before publication.

Standing prevents a result from becoming more authoritative merely because it traveled. Conclusions are portable; their grounds are less so.


## 8. Risk and authority come after analytical establishment

Cost, security, application risk, and authorization can constrain an otherwise established analytical service. They cannot supply a missing analytical ground.


> Risk may constrain the right answer. It cannot turn an unestablished answer into the right one.

An unresolved analytical identity, unsupported population, or unlawful derivation is not merely a higher-risk version of the requested answer. Once the analytical object and required support are established, exposure matters: the same result may be acceptable for exploration and unacceptable for compensation, publication, or automated action.


## 9. Govern the crossings

Analytical service becomes consequential at crossings: purpose becomes a request, a request becomes a plan, a plan produces a result, a result becomes an answer, and an answer becomes action. Each crossing creates an opportunity for authority to travel farther than its grounds.


> The component that can produce a candidate result need not be the component entitled to authorize what that result becomes.

AI agents are one application of this crossing discipline. A model may interpret language, formulate a candidate governed request, generate candidate SQL, summarize evidence, or explain an adjudication result. Those capabilities do not require the model itself to carry analytical authority.

A structural execution boundary can close one consequential path independently of predictions about the agent. This is the role of a blast wall: a structural boundary that prevents reasoning output from becoming consequential execution directly. The same principle applies to serving: the agent may propose or explain; the governed serving boundary determines what the result is entitled to become.


## 10. One request through the service


> What was average revenue per open store yesterday?


### Purpose and intent

The user wants a statement about stores that were open, not merely stores that reported revenue. Resolve the governed meanings of revenue, store, open, and yesterday. Clarify if more than one governed request remains; Escalate if the required meaning does not exist.


### Analytical construction

Establish the open-store population, the Revenue measure at the required analytical location, and the lawfulness of the requested reduction. The 50-store roster does not establish that all 50 were open. The 47 revenue rows do not establish the open-store population.


### Reliable production and support

Use the operating-status source to establish the 48 open stores and determine whether the required revenue state is supported for those points. A lawful analytical object can still be unservable if required state is unavailable.


### Governance response

Serve when the exact result is supportable and lawful. If support is incomplete but a separately governed qualified answer remains legitimate, Disclose the limitation and serve only that qualified answer. If the missing support defeats the requested answer, Refuse. Clarify when the user's governed choice is missing. Escalate when faithful service requires new governed meaning, evidence, or authority.


### Consequential use

Only after the answer is established and servable do later risk and authority conditions determine whether it may be published, used for compensation, or passed into automated action.

The arithmetic is not the hard part. The governance problem is preserving the user's purpose and the grounds that serve it across the entire passage.


## 11. What Analytical Governance uniquely governs

Theory of Data supplies laws of governed analytical identity, derivability, and consistency (Wang 2026a). The Statistical Bridge governs passages from governed evidence through formal inference to licensed claims (Wang 2026b). The Theory of Certainty distinguishes grounds of certainty, their reach, composition, and sufficiency for reliance (Wang 2026d).

Analytical Governance coordinates these kinds of interior law without replacing them.


> Analytical Governance governs the analytical service passage: what must remain true as purpose becomes request, request becomes result, result becomes answer, and answer becomes consequential use.

Its subject includes process and practice as well as architecture: how analysts, data systems, semantic systems, AI agents, reviewers, and execution controls preserve analytical meaning and authority across handoffs.

Data governance governs stewardship, access, quality, and control of data assets. Analytical Governance governs whether the analytical service is faithfully formulated, sufficiently established, honestly served, and appropriately used. The two compose; neither substitutes for the other.


## 12. Requirements and non-claims

A conforming analytical-governance practice or architecture needs, at minimum:

- a way to preserve user purpose while translating human or machine intent into an explicit analytical request;

- a governed analytical representation capable of independently establishing identity, derivation, support requirements, and relevant state;

- a reliable production path that preserves what was analytically established;

- a servability gate capable of withholding or qualifying analytical permission;

- a way to preserve standing, conditions, reasons, and alternatives as results cross boundaries;

- separation between analytical establishment and later cost, security, application, and authorization decisions;

- execution faithful to what governance actually authorized.

This framework does not guarantee perfect intent, perfect data, perfect governed declarations, or perfect decisions. It does not replace semantic knowledge, statistical inference, security engineering, physical optimization, or decision governance. It coordinates the points at which their outputs become part of an analytical service and acquire or lose permission to proceed.

Analytical Governance does not require any particular query language, semantic layer, or implementation architecture. It requires that the analytical target, the grounds relevant to serving it, and the authority for consequential use be independently adjudicable somewhere before the service crosses the relevant boundary.


## 13. Conclusion

Analytics serves a user with a purpose. Analytical Governance governs the legitimacy of that service: the purpose must be preserved, the analytical result must be established and produced reliably, and the answer must carry no more authority than its grounds warrant.

The intent gap asks whether the user's purpose has become the analytical request the system is actually answering. The servability gap asks whether the grounds required to serve that request are present. Standing governs what the resulting answer may carry forward. Risk and authority govern consequential use after analytical establishment.

The Theory of Certainty gives this architecture a cleaner foundation: different grounds establish different things, their warrant has limits, and the certainty sufficient for reliance depends on the exposure (Wang 2026d). Analytical Governance turns that foundation into service discipline.


> Preserve purpose. Establish the analytical object and its grounds. Produce it reliably. Serve only what is servable. Preserve standing across crossings. Govern consequential use.

The goal is not to formalize every analytical act. It is to ensure that when analytics serves a user, the answer remains faithful to the purpose that called for it and carries no more authority than it has earned.


## References

Wang, Huayin. 2026a. *The Theory of Data: A Foundation for Analytical Identity, Derivability, and Consistency*. Version 6.1. Zenodo. DOI: 10.5281/zenodo.22013410.

Wang, Huayin. 2026b. *The Statistical Bridge: From Governed Evidence to Inference Certificates and Licensed Claims*. Version 3.0. Zenodo. DOI: 10.5281/zenodo.21979821.

Wang, Huayin. 2026c. *Certifiable State Under Information Loss: Governed Derivability, Claim Transport, and Approximate Closure*. Version 1.0. Zenodo. DOI: 10.5281/zenodo.21972541.

Wang, Huayin. 2026d. *The Theory of Certainty: Grounds for Analytical and Operational Reliance*. Version 1.0. Zenodo. DOI: 10.5281/zenodo.22114802.

Wang, Huayin. 2026e. *Analytical Governance: From User Intent to Governed Analytical Execution*. Version 1.1. Zenodo. DOI: 10.5281/zenodo.22046037.
