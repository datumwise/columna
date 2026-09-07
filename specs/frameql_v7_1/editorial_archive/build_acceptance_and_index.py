from pathlib import Path
import json,hashlib
W=Path('/mnt/data/frameql_alignment_work');O=W/'output';D=W/'audit'
T='the_theory_of_data_v7_1_full_manuscript_working_draft_v0_4.md';L='frameql_language_vnext_working_draft_v0_4.md';N='frameql_v7_1_supporting_contract_notes_v0_1.md';O3='columna_o3_governed_analytical_order_v0_2.md';C='frameql_vnext_capability_profile_reconciliation_plan_v0_2.md'; A='frameql_v7_1_semantic_acceptance_cases_v0_1.md'; INDEX='frameql_v7_1_authority_and_supersession_index_v0_1.md'
cases=[]
def case(id,topic,premises,expected,forbidden,theory,language):cases.append(dict(id=id,topic=topic,premises=premises,expected=expected,prohibited_shortcut=forbidden,theory_sections=theory,language_sections=language))
case('F01','Specified target before bases','A proposed family has two mutually agreeing constructors but no nominated defining construction or independent target specification.','The family contract is incomplete; agreement has no independently specified target against which adequacy can be judged.','Admit the family solely because the two implementations agree.','§§4, 5.3','§6.5')
case('F02','Canonical family without a business name','An admitted law and fully specified constitutive input establish mean(revenue@order); no business alias has been assigned.','Its canonical family expression can denote the family. Institutional publication remains a separate authority.','Require an AS name or a new authoring ceremony before the analytical identity can be denoted.','§§3.9, 4','§§3.5, 11.1')
case('F03','Aliases do not admit law','A query computes revenue/orders AS aov without a supplied AOV family contract.','The alias names an output; it does not establish the missing law. An explicitly governed AOV family remains possible.','Treat output naming as either automatic family admission or a permanent ban on an AOV family.','§§3.5, 3.7, 3.9','§§2.3, 11.2')
case('F04','Constitutive ancestry versus plan','Two licensed derivations claim the same family and anchor using different staging paths under matching premises.','Consistency applies to the same target; physical path/proof method is not new identity.','Include plan identity in the family signature to evade required agreement.','§§2.2, 6.4–6.5','§§3.1, 10.1')
case('F05','Meaning before executable availability','Mean over orders and mean over customers are identity-distinct possible readings; only one has a presently executable plan.','The unresolved intent distinction remains. Availability can be reported, not silently used to choose meaning.','Serve the available target as though availability resolved the request.','§§2.2, 3.9, 9.1','§10.1')
case('F06','Several bases, one target','SUM/COUNT and an exact multiset are both adequate and available for the same fixed MEAN with matching participation.','They are alternative constructions of one target, not an intent ambiguity.','Return Clarify merely because there are two bases.','§§5.3, 5.5','§§6.6, 10.1')
case('F07','Multiplicity remains part of the law','Ordinary MEAN is defined over participating values 0,0,6.','The mean is 2; replacing the multiset by set {0,6} yields another construction and gives 3.','Declare a deduplicating set an exact basis for this MEAN.','§5.3','§6.6')
case('F08','Intake versus continuation','Two retained count values 37 and 12 represent compatible disjoint contributions.','Count continuation adds them to 49. Counting the two summary rows instead would answer a different question.','Use count-of-summary-rows as count-state merge.','§5.2','§6.6')
case('O01','One-dimensional analytical order','Day is a governed anchor with complete chronology and the family has its remaining complete contract.','Precedence is trivial; the declared order supports the admitted finite FIRST/LAST construction.','Require a new generic tie policy or infer chronology from a lineage label alone.','§§7.1, 8','§9.2')
case('O02','Compound precedence required','Customer and Day have complete point orders, but no precedence is supplied for the claimed global Customer-Day support.','The compound order is not fully selected.','Infer precedence from output column order.','§7.1','§9.2')
case('O03','Missing constituent order','Precedence is supplied but Customer has no complete governed point order.','The claimed complete compound order is unestablished.','Sort Customer IDs lexically as an implicit analytical order.','§§7.1–7.3','§9.2')
case('O04','Sparse analytical point space','The governed support contains only (C1,d3),(C2,d1),(C2,d2).','Only these points participate; order does not create (C2,d3) or another absent combination.','Fill the Cartesian product before LAST without an existence law.','§§2.1.3, 7.1','§9.2')
case('O05','Form the support measure first','Several Product carrier records lie beneath one Account-Day point.','Apply the operand formation law to establish its value at Account-Day before FIRST/LAST consumes that analytical point.','Select a raw row by day or invent SUM as the formation rule merely to collapse duplicates.','§§3.1, 7.3','§9.3')
case('O06','Ordered family not automatic legacy conformance','FIRST/LAST has an admitted construction in T; a legacy .last spelling is accepted by a particular build.','Analytical admission and that execution path’s conformance are separate claims.','Certify every existing .last because the theory now admits an ordered family.','§§3.6, 4, 8','§§9.1, 9.7, 13')
case('O07','Original point witness through coarsening','For s1<s2<s3<s4, admitted intermediate groups are {s1,s4} and {s2,s3}, with coherent supported values.','Retained winners s4 and s3 combine to s4 using the original support order.','Compare intermediate group labels or demand an unrelated new order on B.','§§8.3–8.4','§9.5')
case('O08','Scalar is not witness continuation','An exact scalar LAST was materialized but its selected point is not retained or recoverable.','The scalar target is available; further witness comparison is not licensed from it alone.','Set scalar re-entry true merely because LAST has family standing.','§§8.1, 10.7','§§9.4, 10.6')
case('O09','R is optional','An adequate argument establishes W; a full retained point–value set is unavailable.','W can be used under its actual admitted contract; full R storage is not mandatory.','Impose R→W→L as a required runtime/storage pipeline.','§§8.6, 9.2','§9.4')
case('O10','Same results, different laws','Two different declared precedence orders currently yield the same winner.','Numerical agreement does not merge their analytical identities.','Infer equivalent family identity from observed equality.','§§2.2, 7.2','§§9.2, 10.1')
case('O11','Frame selection can coincide with LAST','A versioned output ORDER BY/LIMIT PER query selects a row whose value equals a LAST answer.','Frame selection remains legitimate in its own scope; no inner family identity or reusable witness follows.','Either ban the frame operation or use it as ambient order/family proof.','§12.4','§9.7')
case('C01','Contextual formation can precede a family','The law fixes daily predecessor formation over 100,110,95,105 and a separately admitted additive family over the changes.','Established changes 10,-15,10 sum to 5 coherently.','Exclude the family solely because formation used neighboring points.','§§3.3–3.4','§6.10')
case('C02','Restriction must preserve formation','The same change family is requested after grouping the source into pairs.','Reusing original changes differs from restarting predecessor formation inside the pairs, which gives 20.','Push a restriction/grouping through formation without an equivalence justification.','§§3.3, 10.2','§§2.4, 6.10')
case('C03','Faithful recomputation is not forbidden','The original contextual formation and its full governing context can be reproduced from adequate evidence.','Recomputation can establish the same constitutive values; caching is not required by the theory.','Interpret “do not change formation” as “never recompute.”','§§3.3–3.4','§6.10')
case('C04','Focal window law needs its own contract','A rolling expression is written without specifying positional versus time-range neighborhood and material endpoint conventions.','The expression’s meaning remains incomplete where these choices change the result.','Treat complete order alone as a full window specification or automatically admit family continuation.','§§3.4, 11.4','§9.6')
case('E01','Established output, unplaced source','A Day output point exists and Revenue is eligible, but required known source contributions cannot be placed by Day.','The target value may be unsupported; the upstream placement cause remains distinct.','Declare the output point nonexistent or forbid target missingness solely because a source placement is unresolved.','§§2.3, 9.1–9.4','§§8.1–8.4')
case('E02','Known domain with incomplete operand support','Governance establishes exactly 100 participating transactions, with 99 supported Revenue observations.','Point count is 100; a count under a declared supported-operand participation law may be 99. A mean over all 100 cannot silently shrink.','Infer intended population from surviving ordinary rows.','§§2.3, 4.2, 11.5.1','§8.5')
case('E03','Coarser witness, unavailable staged input','Participation s1<s2<s3 and intermediate blocks {s1},{s2,s3} are known; f(s1) unavailable, f(s2)=20 and f(s3)=30 supported.','Coarser W=(s3,30) is established by maximality evidence even though a plan consuming both exact intermediate witnesses lacks an input.','Replace unavailable intermediate W with known-empty identity, or infer target impossibility from this plan’s failure.','§§6.1, 9.5','§8.7')
case('E04','Scalar without winner identity','Fixed LAST law; p<q; p definitely participates; q participation unresolved; p,q exhaust possible participants; both operand values supported as 7.','Nonempty scalar L=7 is established; selected-point W is not.','Claim W, choose an arbitrary observed 7 without the exhaustive evidence, or treat W as necessary for every L proof.','§9.6','§8.8')
case('E05','Missing selected operand','Participation and order identify the latest eligible point, whose operand value is unsupported.','Ordinary LAST value is unsupported unless another adequate argument establishes the same target.','Return an earlier supported value by silent support-skipping.','§§9.2–9.3','§8.6')
case('E06','Known empty is not unknown','An intermediate contribution set is unknown, or the selected value is unsupported.','No algebraic unit can stand for that unknown evidence without a separate admitted argument.','Coerce carrier NULL or unknown support to bottom/zero/empty set.','§§5.2, 6.1.1, 8.2, 9','§8.9')
case('E07','Late filtering cannot undo ordered influence','An unplaceable contribution affects cumulative/lag output, then its own row is withheld.','The resulting computation has not been repaired by the late withholding.','Report ordinary established results merely because no NULL-coordinate row remains.','§9.4','§8.10')
case('R01','Lossy compression can hide contradiction','With p<q, one alleged coherent input has (p,10),(q,20); another has (p,11).','Their coherent-instance premise is violated; compressed winner comparison cannot validate it.','Treat equal-point conflict checks or a common context label as a global consistency certificate.','§10.6','§10.7')
case('R02','Three materialization claims','A catalog holds W, scalar L projected from discarded W, or scalar L established without identifying its winner.','Record retained content, established claim and justification, and permitted reuse; the scalar rows need not have different family identities.','Collapse all entries into “LAST available” or create family identity by proof method.','§10.7','§10.6')
case('R03','Equal mean display, unequal continuation','Exact states (10,1) and (1000,100) both display 10; both are extended by (20,1).','The results become 15 and 1020/101; scalar equality did not preserve continuation information.','Merge or substitute displayed means as adequate state.','§10.5','§6.6')
case('R04','Restriction or deletion of winner','Only the compressed maximal witness is retained, and the next request excludes or deletes that point.','A new adequate derivation or richer retained information is required to identify its replacement.','Infer arbitrary filtering/deletion capability from witness coarsening capability.','§§10.2–10.3','§10.8')
case('R05','Approximate realization of unchanged target','An explicit approximation contract supports an HLL estimate of exact count distinct.','It may target the same family while remaining an approximate realization, not an exact sufficient-state basis.','Invent a new target solely from error grade, or silently reuse the estimate as exact state.','§10.9','§§6.9, 10.8')
case('G01','EXPLAIN does not observe unperformed checks','EXPLAIN resolves meaning and a proposed plan without data execution or applicable evidence for all runtime conditions.','It distinguishes what is established from checks outstanding.','Guarantee all future disclosures or complete data support from a data-free explanation.','§§9.1, 12.3–12.4','§10.3')
case('G02','Family law versus engine kind','An operator belongs to a runtime category or a canonical capability list.','Family admission still needs the complete target/law contract; category does not confer authority.','Grant family founding solely from an anchor-changing kind.','§3.6','§13')
case('G03','No syntax from theory alone','The theory admits tuples, witnesses, order definitions or a family construction not exposed by a shipped grammar/profile.','Semantic admission and language/implementation availability remain separate.','Advertise theoretical notation as accepted syntax or edit measured build status to imply support.','§§12–13','§§1, 13')
case('G04','CDT interface remains unverified','This pass specifies required comparison and representation behavior but does not inspect CDT v0.5.','Readiness is unverified; a new nominal Witness type is neither asserted absent nor mandated.','Claim present API support/absence from the theory manuscript.','§§8.5, 12.2, 13.3','§9.5')
case('G05','Historical instructions are not active authority','An earlier O1/O2/M2/CP document says FIRST/LAST cannot found families or universal formation locality is required.','Use the explicit current supersession index and reconciled language target; preserve historical observations at their own snapshots.','Execute an old “settled” instruction because its filename or prior PASS sounds authoritative.','Appendix C.4','§§15–16')
(O/'frameql_v7_1_semantic_acceptance_cases_v0_1.json').write_text(json.dumps(dict(status='semantic review cases; not executable Columna tests',theory=T,language=L,cases=cases),indent=2,ensure_ascii=False)+'\n')
md=f'''# Frame-QL / ToD v7.1 — Semantic Acceptance Cases

**Working set 0.1 — 7 September 2026**  
**Status:** {len(cases)} source-derived semantic review cases, not executed Columna tests, mathematical proofs, or release-conformance claims.  
**Theory:** [T Draft 0.4]({T}). **Language:** [Candidate 0.4]({L}).

Each case states its premises so a future test cannot replace the governed claim with an easier one. Exact runtime outcomes or reason codes are not invented where only the semantic disposition is fixed. Contextual-language implications are identified by their LQ sections; the underlying family and evidence rules remain T's.

The [JSON companion](frameql_v7_1_semantic_acceptance_cases_v0_1.json) contains the same cases for future review tooling. This pass checks document consistency and premise coverage; it does not run these cases against an engine.

'''
for c in cases:
 md+=f"## {c['id']} — {c['topic']}\n\n**Premises.** {c['premises']}\n\n**Expected judgment.** {c['expected']}\n\n**Do not.** {c['prohibited_shortcut']}\n\n**Sources:** T {c['theory_sections']}; LQ {c['language_sections']}.\n\n"
(O/A).write_text(md)
# Supersession index: use exact snapshot names, with hash manifest kept separate.
source_rows=[
('frameql_language_vnext_working_draft_v0_3.md','Superseded as the local language-law target',L+'; chapters 3, 6, 8–13 and acceptance set replace the outdated rules. Preserve @/AT, broadcast, co-participation and frame boundaries.'),
('frameql_vnext_o1_ordered_expression_compatibility_ruling_v0_1.md','Superseded for current design',N+' §1 and LQ §10 retain complete governed resolution; categorical non-family FIRST/LAST and compulsory legacy migration are withdrawn.'),
('frameql_vnext_o2_ordered_expression_semantic_architecture_v0_2.md','Superseded as a unified admission architecture',N+' §2 and LQ §9 retain analytical domain/context insights; do not apply its non-family verdict to admitted ordered families.'),
('frameql_vnext_o2_reconciliation_to_tod_v7_1_v0_1.md','Superseded despite its title',N+' §§2.3–2.4; withdraw universal formation-locality exclusion and incomplete TOP-k promotion. Use T §3.4.'),
('frameql_vnext_r4_standing_amendment_v0_2.md','Subsumed and qualified',N+' §3 and LQ §8 preserve standing distinctions; remove all-input/placement prerequisites that would block target-relative evidence arguments.'),
('columna_o3_governed_analytical_order_v0_1.md','Superseded by interface revision',O3+' preserves order structure, updates W/L/R and evidence/reuse, and no longer carries an independent proof account.'),
('frameql_vnext_capability_profile_reconciliation_plan_v0_1.md','Superseded as a migration proposal',C+' withdraws categorical FIRST/LAST non-family/re-entry-inapplicable instructions and freezes no replacement schema.'),
('frameql_vnext_authority_reconciliation_v0_1.md','Historical reconciliation plan',INDEX+' and LQ §1 preserve authority separation; old admission/registry recommendations are not current.'),
('frameql_vnext_current_manual_migration_matrix_v0_1.md','Historical source map, not an edit instruction','Reference integration patch sheet replaces its semantic dispositions. Old repository line numbers are not assumed current.'),
('frameql_vnext_m1_semantic_review_v0_1.md','Historical review under earlier premises','Broadcast/WHERE discoveries survive. Its PASS does not endorse the superseded order or locality boundary.'),
('FRAMEQL_VNEXT_M2_CC_RECONNAISSANCE.md','Historical mission text; not reusable authorization','Observed implementation evidence belongs to its report/snapshot. Do not reuse its old settled exclusions or initiate code work from it.'),
('FRAMEQL_VNEXT_O2_CC_DESIGN_RECONNAISSANCE.md','Historical mission text; not reusable authorization','Questions can inform a future bounded mission; instructions excluding FIRST/LAST families are withdrawn.'),
('frameql_companion_corpus_assessment_against_tod_v7_1_v0_1.md','Historical assessment, now dispositioned','Its findings are mapped to the outputs in the reconciliation register. It remains evidence of what needed changing, not an active competing specification.'),
]
intro='frameql_an_introduction_v2_4_working_draft_v0_1.md'; primer='a_primer_on_frameql_v2_3_working_draft_v0_1.md'; patch='frameql_v7_1_reference_integration_patch_sheet_v0_1.md'
md=f'''# Frame-QL / ToD v7.1 — Active Authority and Supersession Index

**Working index 0.1 — 7 September 2026**  
**Scope:** The local reconciled companion review set created in this task. It does not claim that repository, website, retrieval corpus, or Zenodo records have been updated.  
**No publication or implementation authorization.**

## 1. Read the current set in this order

| Document | Responsibility |
|---|---|
| [ToD v7.1 Full Manuscript Draft 0.4]({T}) | Fixed working analytical foundation; unchanged in this pass, unpublished |
| [Frame-QL Language-Law Candidate 0.4]({L}) | Single reconciled expression/request semantic target; not the shipped Manual |
| [Supporting Contract Notes 0.1]({N}) | Governed completion, contextual domains, and standing; subordinate to T and LQ |
| [O3 Order Interface 0.2]({O3}) | Logical order declarations, comparison requirements, realization and reuse interface; no schema/API claim |
| [Semantic Acceptance Cases 0.1]({A}) | Explicit premises and expectations for review; not executed engine tests |
| [Capability/Profile Plan 0.2]({C}) | Rebased future adoption constraints; no registry, promise, or measurement changed |
| [Release-reference integration patch sheet]({patch}) | Proposed local replacements for remaining public-reference wording; requires separate repository adoption |
| [Introduction proposed v2.4, draft 0.1]({intro}) | Fuller conceptual entry point, preserving the predecessor structure and 14 Frame-QL examples |
| [Primer proposed v2.3, draft 0.1]({primer}) | Short entry point, preserving its section order and three Frame-QL examples |

This order is for technical reconciliation review. A new conceptual reader can begin with the Primer and Introduction. Neither replaces the technical authority.

The exact input/output hashes, source acquisition limits, and changes are in the reconciliation register and manifest. Intro/Primer successor edition numbers are proposed, not publication metadata. No v7.1 DOI is invented.

## 2. Different jurisdictions are not competing theories

T supplies analytical target identity, family admission, sufficient state, evidence and reuse boundaries. LQ supplies the successor request semantics. The applicable versioned grammar determines accepted syntax. Released reference semantics, authored profile obligations and measured build coverage retain their own scopes. A discrepancy in current implementation must be stated, not erased by changing analytical meaning.

A title containing “Manual” or “canonical” on a working file does not make it the shipped authority. A code path or green coverage table does not prove a v7.1 family contract. A newly admitted theoretical construction is not a new shipped function.

The logical Manifold, private realization mapping, current evidence/certification, and institutional publication authority remain distinct. No new schema or services are implied merely by distinguishing their claims.

## 3. Explicit disposition of earlier working guidance

The following files remain intact in the editorial archive. “Superseded” means their recommendations are not current design authority; it does not rewrite observed historical implementation facts.

| Exact older file | Current disposition | Replacement / retained work |
|---|---|---|
'''
for a,b,c in source_rows:md+=f'| `{a}` | {b} | {c} |\n'
md+=f'''
Older opening drafts, core-semantic chapter drafts, consolidated language candidates v0.1/v0.2, and the monolithic rewrite architecture are ancestors of LQ0.3 and not additional active authorities. The earlier ToD amendments and stress test are already dispositioned by T Appendix C; their universal formation-locality exclusion must not be restored through a companion citation.

## 4. Published predecessors remain versioned history

*Frame-QL: An Introduction* v2.3 (10.5281/zenodo.22071910) and *A Primer on Frame-QL* v2.2 (10.5281/zenodo.22071833) are preserved as published predecessors. The new files are working successors. Full public repository source text was read; the local editorial inputs are whitespace-normalized transcriptions, not independently checksum-verified Zenodo deposit bytes. Historical publications are not silently overwritten.

Published ToD v7.0 (10.5281/zenodo.22289091) retains its historical exclusion of ordered families. T states that v7.1 changes that position. A current reading index must distinguish that succession from simultaneous conflicting authority. No historical DOI becomes a v7.1 DOI by citation.

## 5. Repository references and adoption remain separate

The public `docs/frame_ql_language.md`, grammar, profile documents, capability TOMLs, generated build status, and revision history were not edited. The new [patch sheet]({patch}) identifies proposed successor-reference wording and scope notices. It is not a claim of a commit-pinned patch or an applied repository change.

Before claiming the live corpus is aligned, the authorized repository maintainer must install the chosen working or publication successors, update the reading index and any route/retrieval references deliberately, and preserve released grammar/profile/build facts. Generated tables stay generated. Current code and publication status require separate evidence.

## 6. No old mission becomes a new authorization

Earlier CC handoffs and merge instructions apply only to their stated scope and reported revision. This index authorizes no implementation. It does not schedule another reconnaissance or declare existing ordered-path defects fixed.

Reported physical-row FIRST/LAST selection and ordered contribution before late placement withholding remain distinct correctness issues. A separately authorized closed-by-default correction need not wait for complete successor functionality, but this document reconciliation is not that correction.

## 7. Ready for a joint document review, not a release declaration

The active local set now has one family contract source and one language-law target. Reviewers should check consistent admission, identity, evidence, restriction, explanation, and reuse claims across it. The acceptance cases identify the shortcuts that should not return through editorial compression.

Pending boundaries are actual CDT/interface verification, release-specific implementation conformance, exact publication-source byte checks where required for deposit production, repository/site installation, and final publication metadata. Those are explicit pending tasks rather than covert gaps in the semantic reading set.
'''
(O/INDEX).write_text(md)
(D/'supersession_dispositions.json').write_text(json.dumps([dict(source=a,disposition=b,replacement=c)for a,b,c in source_rows],ensure_ascii=False,indent=2)+'\n')
print(len(cases),'semantic review cases;',len(source_rows),'specific historical guidance dispositions')
