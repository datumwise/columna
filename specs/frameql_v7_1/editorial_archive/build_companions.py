from pathlib import Path
import re,json,difflib
R=Path('/mnt/data'); W=R/'frameql_alignment_work'; S=W/'sources'; O=W/'output'; D=W/'audit'
T='the_theory_of_data_v7_1_full_manuscript_working_draft_v0_4.md'; L='frameql_language_vnext_working_draft_v0_4.md'; I='frameql_v7_1_authority_and_supersession_index_v0_1.md';N='frameql_v7_1_supporting_contract_notes_v0_1.md';C='frameql_vnext_capability_profile_reconciliation_plan_v0_2.md';A='frameql_v7_1_semantic_acceptance_cases_v0_1.md';O3='columna_o3_governed_analytical_order_v0_2.md'
changes=[]
class Revision:
 def __init__(self,source,out): self.source=source; self.out=out;self.original=(S/source).read_text();self.text=self.original
 def rep(self,a,b,why):
  if self.text.count(a)!=1: raise ValueError((self.out,why,self.text.count(a),a[:100]))
  self.text=self.text.replace(a,b,1);changes.append(dict(document=self.out,reason=why,before=a,after=b))
 def sec(self,a,b,new,why):
  x=self.text.index(a); y=self.text.index(b,x);self.rep(self.text[x:y],new.rstrip()+'\n\n',why)
 def tail(self,a,new,why): self.rep(self.text[self.text.index(a):],new.rstrip()+'\n',why)
 def save(self):
  (O/self.out).write_text(self.text)
  (D/(self.out+'.diff')).write_text(''.join(difflib.unified_diff(self.original.splitlines(True),self.text.splitlines(True),fromfile=self.source,tofile=self.out)))
# Revised O3 retains the actual two-level order definition, declaration content,
# numerical example, and hierarchy account; proof/standing sections defer to T.
x=Revision('columna_o3_governed_analytical_order_v0_1.md',O3)
x.sec('# O3 — Governed Analytical Order','# 1. The anchor remains a partition',f'''# O3 — Governed Analytical Order
## Declaration, comparison, identity, and realization

**Working Draft 0.2 — 7 September 2026**  
**Status:** Order-interface proposal subordinate to [ToD v7.1 Full Manuscript Draft 0.4]({T}) (**T**) and [Language-Law Candidate 0.4]({L}).  
**No schema, syntax, runtime, publication, or implementation authorization.**

# 0. Scope and authority

This revision preserves O3's two-level order construction, sparse partition geometry, logical declaration proposal, and comparison/realization separation. It replaces the older witness-proof and evidence summaries with references to T §§7–10 so that those laws have one source.

The existing order-interface proposal supplies two kinds of logical order fact and one family binding, not necessarily three new classes or registries. The actual CDT v0.5 API has not been inspected in this revision. Requirements below do not imply that a type literally named `Witness` must be added or that no existing structure can implement them.

Historical inspector statements concern the recorded `bfb3cfe` baseline and are not a fresh repository audit. This revision does not repeat or close their runtime probes. The [active-source index]({I}) distinguishes current semantic guidance, historical implementation evidence, and superseded recommendations.
''','Rebase O3 authority to fixed complete manuscript')
x.rep('**Precision correction to amendment 0.2, §3.** Its schematic product notation and the word “independent” must not imply that every Cartesian combination exists, that the dimensions are statistically independent, or that an anchor has a uniquely discoverable factorization. The earlier ToD partition account defines a compound anchor through nonempty intersections over its governed universe. That account is preserved here. [S7, §2.7]', '**Sparse compound geometry (T §2.1.3).** Constituent coordinates must not imply that every Cartesian combination exists, that the dimensions are statistically independent, or that an anchor has a uniquely discoverable factorization. A compound anchor is the common refinement through nonempty intersections over the governed universe.','Use incorporated sparse geometry instead of amendment conflict')
x.rep('In this document, **support anchor** retains the amendment\'s meaning of *constitutive input anchor*. It must not be confused with the subset of points whose operand values currently have evidence support.', 'In this document, **support anchor** means the *constitutive input anchor* of T §§7–8. It is not another anchor kind and must not be confused with the subset of points whose operand values currently have evidence support.','Connect support term to core terminology')
x.rep('This is the standard lexicographic construction; the external reference [E1] corroborates the mathematical construction only and supplies no Columna governance authority.', 'This is the lexicographic construction admitted by T §7.1. The mathematical order argument and the institutional authority selecting its definitions remain different questions.','One source for order construction')
x.sec('## 3.3 The ordered family\'s binding','# 4. What CDT supplies, and what it does not',r'''## 3.3 The ordered family's binding

A family construction selects a fully resolved governed support order and its constitutive operand. The full target specification and family contract remain T §4: neither a complete order nor a callable FIRST/LAST spelling supplies the remaining obligations.

For the finite construction in T §8, W is constituted from operand, order, and participation with its own witness-selection and continuation law. Scalar L has an admitted construction by value projection from W. An optional rich retained family R supplies an alternative basis with an exact compatible-union compression to W. These names denote ordinary analytical families, not mandatory public declaration kinds or engine types.

A declaration must identify whether the referenced analytical object is the scalar target, witness-valued family, or another admitted family. It must not grant a scalar materialization the continuation capability of the witness solely because both concern LAST.

The order can be reused by another admitted analytical law. A human-readable name is optional where canonical construction already resolves identity. Institutional publication and ratification remain separate from denotation.
''','Bind complete target and W/L identities without defining them again')
x.rep('The inspector report identified why this interface matters: the inspected build\'s `ORDERED` set classifies accepted measure dtypes, while coordinate levels have no dtype and no declared comparison operation. That is evidence of the gap, not a template for the successor. [S3, §§F.0–F.1]', 'The earlier O2 inspector report identified a gap at its recorded baseline: the `ORDERED` accept-set concerned measure dtypes while coordinate levels lacked a declared semantic comparator. That observation is historical implementation evidence, not a claim about the uninspected CDT specification or the current build. The successor contract must be established against the actual type specification before conformance is claimed.','No unverified current API claim')
x.sec('# 8. The finite sufficient-state law, fully stated','# 9. Declaration completeness is not current evidence completeness',r'''# 8. The family proof remains in the theory

T §§8.1–8.6 is the sole mathematical account used here. Its propositions define coherent-instance witness composition and show that extracting an extremum witness from compatible finite point–value sets preserves the admitted union/combine operation. No parallel witness theorem is introduced in this interface note.

The complete finite-input fragment fixes coherent operand instance f, order, and contribution domain. Known-empty contribution supplies the identity; an unsupported contribution is not that identity. Two conflicting values for one analytical point do not satisfy the coherent-instance premise.

A representation must preserve original point identity, declared order comparison, the associated operand value where required, and the distinction between known-empty and unavailable state. It may use a typed record, coordinate tuple, governed point reference, or a faithful encoding. A nominal built-in type called `Witness` is not required.

R is an optional sufficient basis, not a prerequisite to serving W or L. A direct implementation can establish W without retaining the full pair set if its evidence establishes the winning-point claim. An adequately justified scalar may be available without an identified winner. These possibilities are not a mandatory `R → W → L` runtime pipeline.

The family law is uniform across coherent instances; the instance-relative carrier does not create a new family identity for each snapshot. Whether two materializations are compatible instances for a proposed use is an evidence/reuse question, not a fact certified by a local winner comparison.
''','Remove redundant old proof and make T the single witness-law source')
x.sec('# 9. Declaration completeness is not current evidence completeness','# 10. Authored meaning, admission, and execution',r'''# 9. Declaration completeness is not current evidence completeness

A complete declared order does not prove that a current materialization can place every required point or recover its comparison representation. Conversely, loss of an irrelevant operand value need not make a target unavailable. Evidence obligations depend on the requested law.

The following distinctions from T §9 must remain visible in a resolved order contract and its supporting evidence:

- A known domain `s1 < s2 < s3` with supported maximal value 30 can establish the coarser witness `(s3,30)` even when a finer intermediate witness at s1 cannot be obtained. Do not replace that unavailable intermediate by empty state.
- A fixed LAST law can establish scalar 7 without identifying the winner only under an adequate argument; T §9.6's example requires known nonemptiness, exhaustive possible-participant coverage, and supported equal values at every possible winner. Equal values among observed rows alone are insufficient.
- Missing selected value, unknown possible later participation, incomplete point placement, and incomplete declared order are different failures. “Last supported value” cannot replace “last participating point's value” silently.

No order-specific standing enum is introduced here. The needed claim, its dependencies, and the evidence supporting it must be distinguished however the concrete implementation represents them.

A false number is not made lawful by adding disclosure later. A late frame filter does not repair an earlier ordered walk that consumed an unplaceable contribution. Exact outcome policy and current containment remain separately authorized engineering work.
''','O3 target-relative evidence summaries and complete premises')
x.sec('# 12. State identity and reuse','# 13. Scope boundaries',r'''# 12. State identity and reuse

T §10.7 governs the materialization interface. The retained artifact must distinguish what it holds, which target claim is established and why, and what later use that information justifies.

A retained nonempty W can construct scalar L and supply admitted witness continuation. A retained L after W was discarded and an L established without a winner may share the same scalar family identity and value while carrying different establishment records. Neither implies retained W. A trace recording historical witness use is not present recoverability.

Compatibility must be established before invoking the lossy-composition theorem. With `p < q`, a source claiming `(p,10),(q,20)` can compress to `(q,20)` and conceal conflict with another source's `(p,11)`. Equal-point conflict checks on compressed winners are not a global validator. A matching context identifier must refer to adequate evidence rather than act as assurance by itself.

Reordering the governed constituent definitions or changing their precedence can change family identity. Physical serialization can change without changing that identity if its semantic representation remains faithful. Evidence refresh can change availability without creating another family, but mixing incompatible instances is not authorized by a common family name.

Coarsening sufficiency does not automatically cover deleting the winner, restricting it out, or re-forming a contextual input under different conditions. Each reuse needs the information and compatible premises required by that use. The concrete catalog and certificate schema remain outside this note.
''','CF materialization boundary and hidden-conflict obligation')
x.sec('# 15. Finite mathematical checks','# 16. Review decisions and next unit',r'''# 15. Validation status

The finite mathematical checks reported in O3 v0.1 remain historical results of that earlier proposal. They were not rerun or extended for this document reconciliation and do not verify the present Columna or CDT implementation.

This revision defers mathematical propositions to the unchanged T Draft 0.4. The current acceptance cases are semantic review obligations, not a claim that every case has an implementation or that a document check proves conformance.
''','No inherited validation count presented as new execution')
x.sec('# 16. Review decisions and next unit','# 17. Sources and evidence boundaries',f'''# 16. Remaining specification work

The order structure remains settled as a working theory input. The remaining interface review should determine whether the actual CDT specification can supply the required equality, point representation, and comparison semantics; how logical publication carries the selected constituent orders and precedence; and how the same resolved meaning reaches explanation and execution.

This task must not use legacy FIRST/LAST internals as the definition of the target. Nor should it introduce a new authoring kind, registry, or wire field merely because the requirements are listed separately. Recommend the smallest faithful representation after inspecting the relevant interfaces.

No such implementation or schema work is authorized here. The [capability/profile reconciliation plan]({C}) states the separate adoption boundaries.
''','Remaining work is targeted interface verification only')
x.tail('# 17. Sources and evidence boundaries',f'''# 17. Sources and evidence boundaries

The fixed theoretical source is [T, Full Manuscript Working Draft 0.4]({T}), especially §§2.1.3, 4–10, and 12. The language account is [Language-Law Candidate 0.4]({L}). Both are working documents, not published v7.1 or shipped-language certification.

The full original O3 v0.1 is retained in the editorial archive, including its sources, historical inspector references, and previous validation record. Its opening source hierarchy and duplicated witness/evidence summaries are replaced by this note; unchanged declaration and geometry content is retained where consistent with T.

The [source/supersession index]({I}) identifies the active note, historical inputs, and withdrawn recommendations. No source byte, publication, or runtime was changed by this revision.
''','Current source index, original references preserved as historical evidence')
# any remaining old source tags in preserved sections are explained, not invented sources
x.rep('[S3, §F.3]','[historical source S3 in archived O3 v0.1]','Retain historical source attribution without dangling active reference')
x.rep('[S5, §§2–4]','[historical source S5 in archived O3 v0.1]','Retain historical explanation-path attribution')
x.save()
# Intro is a targeted edit from the FULL v2.3 text transcription, not v2.0.
x=Revision('frameql_an_introduction_v2_3_transcribed.md','frameql_an_introduction_v2_4_working_draft_v0_1.md')
x.rep('date: "Version 2.3 - 23 August 2026"','date: "Proposed Version 2.4 - Working Draft 0.1 - 7 September 2026"','Provisional successor edition')
x.rep('**DOI:** 10.5281/zenodo.22071910  \n**Previous published version:** Version 2.2, DOI 10.5281/zenodo.22071508',f'''**Status:** Working successor for review; not published, no DOI assigned.  
**Predecessor:** Version 2.3, DOI 10.5281/zenodo.22071910.  
**Theory reference:** [ToD v7.1 Full Manuscript Working Draft 0.4]({T}).

This draft revises the explanation, not shipped syntax or behavior. The predecessor's Frame-QL code examples are retained unchanged and were not re-executed in this pass. Its full public source was read; the editorial archive records the normalized text transcription used here. This is not a byte-identical republication of the deposit.''','Status, exact predecessor and source limit')
x.rep('The language is naturally explained using the current *Theory of Data*, Version 6.1.','This working successor explains the language using *The Theory of Data*, Version 7.1, Full Manuscript Working Draft 0.4.','Fixed theory reference, not published claim')
x.rep('The *Theory of Data*, Version 6.1, is the conceptual reference for analytical identity and lawful transformation, and the Manual states normatively how retained implementation vocabulary relates to the current Theory.',f'''The theory reference for this draft is the reviewed v7.1 working manuscript, not a claim that the shipped language implements all of it. The [reconciled language-law candidate]({L}) supplies the companion semantic target. Applicable versioned grammar and shipped references remain the source for released behavior.''','Separate theory candidate and shipped reference')
x.rep('The current Theory of Data uses the following vocabulary:', 'The theory reference uses the following vocabulary:','Avoid vague current version')
x.rep('- **sufficient state** — state required for lawful exact continuation;','- **sufficient state** — a target-relative relationship among measure families whose measures supply an admitted construction; retained continuation capability remains law-specific;','Relational sufficient state')
x.rep('three foundational anchor kinds in ToD v6.', 'three foundational anchor kinds in the Theory of Data.','Retain v5 implementation vocabulary guard')
x.rep("The relationship between the two vocabularies is stated once, normatively, in the *Frame-QL Manual, Second Edition*, and this introduction inherits it: the *Theory of Data*, Version 6.1, defines the current theoretical vocabulary and governing laws of analytical data; the shipped Frame-QL/Columna implementation may retain vocabulary from earlier versions, with Manual-defined meanings, under v6.1's compatibility provision.", 'The predecessor explained the vocabulary boundary against ToD v6.1. This draft carries that separation forward to the v7.1 working theory: analytical identity and admission come from the selected governed laws; versioned grammar and reference documentation define accepted syntax and shipped behavior. Retained implementation vocabulary is not a theoretical primitive.','Accurate historical/current authority distinction')
x.rep('The Manual remains the normative boundary for what Frame-QL actually accepts and does.', 'The applicable grammar and shipped reference remain the boundary for what a released Frame-QL version accepts and does.','Syntax authority separate from Manual')
x.rep('Under ToD v6 terminology,','Under the retained family/measure distinction,','Retain intellectual structure without old-only reference')
x.rep('Version 6 simplifies that distinction:', 'Version 6 introduced, and Version 7.1 preserves, the distinction:','Explicit version continuity')
x.rep('It is not, in ToD v6, a new foundational analytical identity parallel to measure family or measure.','It is not a new foundational analytical identity parallel to measure family or measure.','No obsolete theory qualifier')
x.rep('Version 6 treats the measure as having one **current** anchor.', 'Version 7.1 retains one **current** anchor per measure.','Current anchor continuity')
x.rep('This is the v6 interpretation of what earlier Frame-QL writing called the "input-anchor/output-anchor" distinction. The distinction remains real; the ontology no longer needs to say that one measure itself carries two current anchors.', 'The input-anchor/output-anchor distinction remains real: the constitutive input can change which family is requested, while the final anchor locates its present measure. It does not give one measure two current anchors.','Constitutive versus current anchor explanation')
x.rep('Not every input anchor must be written. If the shipped planner can determine one unique, immaterial reading under the governed model, it may resolve the omission. Where multiple materially different readings remain, the request is under-specified and the correct shipped outcome is clarification.', 'Not every input anchor must be written. A governed single-valued completion can resolve an omission when it determines one analytical meaning. Several identity-distinct readings require clarification; having only one executable plan does not select the user\'s intent. Two adequate bases for the same fixed target are instead alternative ways to answer one question. The applicable release reference specifies which completions the shipped planner supports.','Target resolution not availability selection')
x.rep('The Manifold is one implementation of the broader idea that analytical knowledge can be represented as data rather than reconstructed in every query. Depending on the class of request the implementation supports, it can contain:', 'The Manifold is one implementation of the broader idea that analytical knowledge can be represented as data rather than reconstructed in every query. The authored Manifold is logical-only. Its governing definitions can identify:','Logical-only Manifold')
x.rep('- operator and reducer declarations;', '- analytical-law declarations and admitted movements;','Neutral law language')
x.rep('- evidence, provenance, and integrity findings;\n- physical bindings and materializations.', '''- the logical contracts whose evidence must be established.

The broader serving environment also needs private physical bindings, applicable evidence and certification, and available materializations. Those facts have distinct roles. The privileged realization boundary combines the logical publication with its private mapping; physical bindings do not create analytical meaning.''','Remove physical bindings from authored ontology')
x.rep('In ToD v6 terms, the conceptual question is whether the governed environment contains enough information to establish the requested family identity, source measure, anchor movement, required state, and material support.', 'The conceptual question is whether the selected model and its applicable evidence establish the requested identity and a lawful available construction. A retained result need not retain the sufficient state required for every later use.','Current evidence and retained capability')
x.rep('The current Manual exposes shipped mechanisms for these cases, including the RELATE face semantics and `WITH allocation`. Those are language-specific ways to express governed relationship behavior. The broader principle is independent of the implementation:', 'The applicable reference and profile state which relationship mechanisms are available, including their exact face or allocation surfaces. This working introduction does not enlarge that coverage. The broader principle is independent of the implementation:','Avoid importing unverified allocation availability')
x.rep('It selects the governed environment in which names, anchors, universes, operator rules, integrity information, and physical bindings are resolved.', 'It selects the governed environment for analytical resolution. Private bindings and current evidence are combined with its logical definitions only by the authorized realization components.','FROM not physical authority')
x.rep('A bare governed name can request its corresponding analytical quantity at the frame output anchor when the shipped planner has a unique supported interpretation.', 'A bare governed name resolves the intended family in the selected namespace. Whether evidence and a realization are available for that quantity is a separate question.','Meaning before availability')
x.rep('That distinction matters in Version 6. A stable new family exists only when the governed analytical model establishes the new identity and its lineage. Frame-QL can still return and name an expression under its shipped result rules without pretending that an `AS` alias alone has performed that governance act.', 'The distinction remains in v7.1. A complete admitted canonical family construction can denote analytical identity without a separate business name. A ratio can also be governed explicitly as an AOV family. But neither arithmetic syntax nor an output alias supplies a missing target specification or family law, and naming an output is not publishing or ratifying a definition.','Canonical denotation and publication')
x.rep('The condition shapes the requested result. It does not expose a user-authored scan plan.', 'The condition restricts the request\'s input under its declared formation scope; it does not expose a user-authored scan plan. `HAVING` selects already-formed output, while `ORDER BY` and `LIMIT` order or select the frame. A restriction must not silently re-form an already-constituted contextual quantity under a different context.','WHERE formation scope and output stages')
x.rep('That is useful to people and agents because interpretation becomes inspectable before physical execution.', 'That is useful to people and agents because interpretation becomes inspectable before physical execution. A data-free explanation does not, by itself, establish every data-dependent support condition or disclosure. The resolved meaning, applicable assurance, proposed plan, and remaining checks must remain distinguishable.','EXPLAIN not complete runtime evidence')
x.rep('ToD v6 sharpens a distinction that the earlier Frame-QL Introduction described as "closure."', 'The Theory of Data distinguishes family-preserving continuation, family formation, and ordinary analytical expressions. Version 7.1 makes the conditions for these judgments explicit rather than deciding them from operator names.','No new closure taxonomy')
x.rep('The source anchor must be real; the source measure must exist there; the source must refine the target; the edge must be licensed; and required state must be available.', 'The source anchor must be real; the source measure must exist there; the source must refine the target; the edge must be licensed; and required state must be available for this particular continuation. Failure of this plan to obtain an intermediate state does not exclude another adequate derivation of the same target.', 'Clarify that continuation premises belong to the particular plan')
x.rep('ToD v6 records such family-changing construction in analytical lineage.', 'Constitutive analytical lineage records such family-changing construction. Alternative proof methods or faithful execution paths to the already specified target do not create new identities.','Lineage qualifier')
x.rep('That keeps query syntax and analytical governance separate.', '''That keeps query syntax and analytical governance separate. Canonical denotation of a family under an admitted analytical law is not a new publication act, and an `AS` label is not an admission rule.

## 8.4 Governed order and retained capability

Version 7.1 withdraws Version 7.0's categorical exclusion of analytical-point-order-dependent families. A complete governed order may be constitutive of a family law whose sufficient-state combination remains invariant to evidence enumeration. For compound support, complete point orders within its constituent anchors and declared precedence induce the order over the analytical points that actually exist.

FIRST/LAST illustrates the distinction. The witness-valued family W retains the selected constitutive point and its value; the scalar family L can be constructed by taking that value. A witness may support admitted continuation even when its displayed scalar cannot. The optional retained point–value family R is another sufficient basis, not a mandatory storage stage. These are mathematical family names, not new Frame-QL syntax.

A stored scalar LAST, a retained witness, and a scalar established without identifying a winner are not interchangeable materializations. The artifact must say what it retains, which claim is established and why, and what reuse is justified. A scalar-only argument requires adequate evidence; the particular constant-value example in T requires a fixed law, known nonemptiness, exhaustive possible-participant coverage, and supported equal values at every possible winner.

None of this certifies a legacy `.last` implementation or prescribes its replacement syntax. General focal operations such as LAG and rolling still need their contextual contracts. They do not gain continuation merely by being named, and contextual formation does not categorically bar a separately admitted family.''','Concise ordered-family and materialization successor explanation')
x.rep('Names, anchor relations, support conditions, reducer rules, relationship behavior, and physical bindings can be declared once rather than reconstructed in every query.', 'Names, anchor relations, analytical laws, and relationship contracts can be governed once rather than reconstructed in each request. Their private physical mappings and current evidence remain separately maintained.','Separate stored knowledge jurisdictions')
x.rep('Some ToD v6 distinctions are not exposed directly in the shipped Frame-QL surface.', 'The reviewed v7.1 target goes beyond what this introduction can claim for a particular shipped build.','No implementation inflation')
x.rep('Where the two use different vocabulary, this introduction translates between them. It does not rewrite shipped behavior to make the implementation look more theoretically complete than it is.', f'''This working edition translates analytical concepts while retaining the released syntax boundary. The [language-law candidate]({L}) describes the reconciled semantic target; Core/Platform profiles state authored obligations, and build-status records report measured coverage. Neither is a blanket proof of v7.1 conformance. No capability promise or generated measurement is changed by this introduction.''','Four-authority version separation')
x.rep('Under ToD v6, Revenue is a governed measure family.', 'Under the Theory of Data, Revenue is a governed measure family.','Current conclusion')
x.tail('## Implementation and further reading',f'''## Implementation and further reading

For the shorter companion in this review set, see [*A Primer on Frame-QL*, proposed Version 2.3, Working Draft 0.1](a_primer_on_frameql_v2_3_working_draft_v0_1.md). Its published predecessor is Version 2.2, DOI 10.5281/zenodo.22071833.

The fixed analytical reference is [*The Theory of Data*, Version 7.1, Full Manuscript Working Draft 0.4]({T}). It is not a published edition and has no confirmed assigned DOI in this packet. Version 7.0, DOI 10.5281/zenodo.22289091, and Version 6.1, DOI 10.5281/zenodo.22013410, remain historical publications under their own versioned positions.

For the reconciled technical account, use [Language-Law Candidate 0.4]({L}) and its [authority index]({I}). For actual formal syntax and released behavior, use the applicable grammar, language reference, profiles, and build record. These working documents do not enlarge the shipped language.

Other useful published companions remain *A Primer on the Theory of Data* v2.2 (10.5281/zenodo.22018549), *Introduction to the Theory of Data* v2.2 (10.5281/zenodo.22018598), *The Theory of Data Applied* v1.0 (10.5281/zenodo.21959941), and *Analytical Governance* v1.1 (10.5281/zenodo.22046037). Their publication versions remain explicit; they are not all silently relabeled v7.1.

**Revision note.** This proposed Version 2.4 succeeds the explanation in Version 2.3, DOI 10.5281/zenodo.22071910, for review purposes only. It updates the theory reference, separates logical definition from realization, clarifies family denotation and target resolution, and adds a bounded order/reuse explanation. All predecessor `frameql` code blocks are retained unchanged. No example was rerun and no syntax, outcome, implementation, repository, or publication was changed.
''','Updated reading set and honest validation/publication status')
x.save()
# Primer keeps the short original architecture and all examples.
x=Revision('a_primer_on_frameql_v2_2_transcribed.md','a_primer_on_frameql_v2_3_working_draft_v0_1.md')
x.rep('date: "Version 2.2 - 23 August 2026"','date: "Proposed Version 2.3 - Working Draft 0.1 - 7 September 2026"','Provisional successor edition')
x.rep('**DOI:** 10.5281/zenodo.22071833  \n**Previous published version:** Version 2.1, DOI 10.5281/zenodo.22071619',f'''**Status:** Working successor for review; not published, no DOI assigned.  
**Predecessor:** Version 2.2, DOI 10.5281/zenodo.22071833.  
**Theory reference:** [ToD v7.1 Full Manuscript Working Draft 0.4]({T}).

This draft updates the conceptual explanation, not shipped syntax or behavior. The three predecessor Frame-QL examples are retained unchanged and were not re-executed. The editorial record identifies the complete public source and its normalized transcription.''','Publication scope and source provenance')
x.rep('Under the current *Theory of Data*,','Under the *Theory of Data*, whose v7.1 working manuscript is the reference for this draft,','Fixed theory target')
x.rep('The requester does not need to choose.', 'The requester does not need to choose the physical source. The system must still establish that the available representation is adequate for the requested quantity and use. A cached average, for example, need not retain the sums and counts required for another exact aggregation.','Availability versus adequate retained state')
x.rep('> **Safety should not be achieved by deleting distinctions that belong to analytical meaning.**', '''> **Safety should not be achieved by deleting distinctions that belong to analytical meaning.**

Two different adequate ways to compute one specified average are not two different questions. Conversely, when order-level and customer-level averages remain distinct possible meanings, having data for only one does not tell the system which one the user intended.''','Target resolution separated from bases and executability')
x.rep('The current *Theory of Data*, Version 6.1, defines the theoretical vocabulary and governing laws of analytical data; the shipped language may retain earlier vocabulary with Manual-defined meanings under its compatibility provision. Advances in the Theory do not enlarge the language, and retained vocabulary does not redefine the Theory; the Manual states this relationship normatively.',f'''This draft uses the v7.1 working theory for analytical identity and law. A complete admitted canonical construction can denote a family without a separate business name. An output alias does not supply a missing family law or publish a definition.

Version 7.1 also admits FIRST/LAST families under complete governed analytical-point order and the required sufficient-state law; a scalar LAST answer is not automatically reusable witness state. That theoretical admission does not certify a legacy `.last` implementation. The fuller Introduction explains this distinction without adding syntax here.

Advances in the theory do not enlarge the shipped language, and retained implementation vocabulary does not redefine the theory. The [working language-law candidate]({L}) is the reconciled semantic target; released behavior remains governed by the applicable reference and profile.''','Small theory succession and no new syntax')
x.rep("A Frame-QL request is resolved against a **Manifold**, Columna's versioned governed analytical environment.\n\nThe Manifold can contain the information needed by the implementation to resolve names, anchors, universes, operator rules, sufficient-state requirements, relationship semantics, support, evidence, and physical bindings.", '''A Frame-QL request is resolved against a **Manifold**, Columna's versioned governed logical analytical model. It supplies names, anchors, universes, analytical laws, and relationship contracts.

The broader serving environment combines that logical publication with separate private physical mappings, applicable evidence, and available materializations. The authored Manifold does not contain physical database bindings as analytical law. Mapping realizes the declared meaning; it does not create it.''','Logical-only Manifold and realization environment')
x.rep('Adjudication has four shipped outcomes: the system can serve the result, serve it with disclosures, ask for clarification, or refuse with a stated reason. A syntactically valid request is not guaranteed a number.', 'The referenced language presents four serving outcomes: serve, disclose, clarify, and refuse. Exact reason codes, errors, and availability remain version-specific. A syntactically valid request is not guaranteed a number; disclosure does not repair a computation whose analytical premises were never established.','Outcome scope without implying complete runtime conformance')
x.tail('# Where to Go Next',f'''# Where to Go Next

For the fuller account in this review set, see [*Frame-QL: An Introduction*, proposed Version 2.4, Working Draft 0.1](frameql_an_introduction_v2_4_working_draft_v0_1.md). Its published predecessor is Version 2.3, DOI 10.5281/zenodo.22071910.

The governing comparison text is [*The Theory of Data*, Version 7.1, Full Manuscript Working Draft 0.4]({T}); it remains unpublished. The [companion authority index]({I}) identifies the active technical drafts. Exact accepted syntax and shipped behavior remain in the applicable grammar and language reference; profiles and measured build records keep their separate roles.

The published ToD v7.0 (10.5281/zenodo.22289091), ToD Primer v2.2 (10.5281/zenodo.22018549), ToD Introduction v2.2 (10.5281/zenodo.22018598), and Analytical Governance v1.1 (10.5281/zenodo.22046037) retain their own edition scope.

**Revision note.** This proposed Version 2.3 updates the Version 2.2 Primer's theoretical and authority explanation while retaining its section order, central argument, three Frame-QL examples, and numerical averaging example. It is not a language release or a published replacement. No examples were rerun in this pass.
''','Successor reading references and no false DOI')
x.save()
(D/'companion_edits.json').write_text(json.dumps(changes,indent=2,ensure_ascii=False)+'\n')
for n in [O3,'frameql_an_introduction_v2_4_working_draft_v0_1.md','a_primer_on_frameql_v2_3_working_draft_v0_1.md']:
 t=(O/n).read_text();print(n,len(t.encode()),'bytes',len(t.split()),'words')
