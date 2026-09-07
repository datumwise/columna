from pathlib import Path
import re, json, hashlib, shutil, difflib
ROOT=Path('/mnt/data'); WORK=ROOT/'frameql_alignment_work'; SRC=WORK/'sources'; OUT=WORK/'output'; AUD=WORK/'audit'
for p in (SRC,OUT,AUD): p.mkdir(exist_ok=True,parents=True)
local_names=[
 'the_theory_of_data_v7_1_full_manuscript_working_draft_v0_4.md',
 'frameql_language_vnext_working_draft_v0_3.md',
 'frameql_vnext_o1_ordered_expression_compatibility_ruling_v0_1.md',
 'frameql_vnext_o2_ordered_expression_semantic_architecture_v0_2.md',
 'frameql_vnext_o2_reconciliation_to_tod_v7_1_v0_1.md',
 'frameql_vnext_r4_standing_amendment_v0_2.md',
 'columna_o3_governed_analytical_order_v0_1.md',
 'frameql_vnext_capability_profile_reconciliation_plan_v0_1.md',
 'frameql_vnext_authority_reconciliation_v0_1.md',
 'frameql_vnext_current_manual_migration_matrix_v0_1.md',
 'frameql_vnext_m1_semantic_review_v0_1.md',
 'FRAMEQL_VNEXT_M2_CC_RECONNAISSANCE.md',
 'FRAMEQL_VNEXT_O2_CC_DESIGN_RECONNAISSANCE.md',
 'frameql_companion_corpus_assessment_against_tod_v7_1_v0_1.md',
 'frameql_companion_corpus_assessment_source_manifest_v0_1.json',
]
manifest=[]
for name in local_names:
 p=ROOT/name
 if not p.is_file(): raise FileNotFoundError(p)
 data=p.read_bytes(); shutil.copy2(p,SRC/name)
 manifest.append(dict(name=name,source='confirmed local supplied artifact',bytes=len(data),sha256=hashlib.sha256(data).hexdigest()))
# Recover the complete publication front matter seen in the web source. Body
# transcriptions normalize whitespace; they are NOT claimed as original deposit bytes.
for stem,old,date in [
 ('a_primer_on_frameql_v2_2_transcribed.md','a_primer_on_frameql_v2_0_publication_ready.md','Version 2.2 - 23 August 2026'),
 ('frameql_an_introduction_v2_3_transcribed.md','frameql_an_introduction_v2_0_zenodo_21960798.md','Version 2.3 - 23 August 2026')]:
 p=SRC/stem; t=p.read_text(); front=(ROOT/old).read_text().split('---',2)[1]
 front=re.sub(r'date: "[^"]+"',f'date: "{date}"',front)
 t='---'+front+'---'+t.split('---',2)[2]
 p.write_text(t)
 (AUD/(stem+'.note.txt')).write_text('Full source body transcribed from the raw public repository text on 7 September 2026. Blank-line and paragraph whitespace normalized. Front matter restored against the complete web view. Not an original-byte or Zenodo checksum verification. See source manifest for URL.\n')
for name,url in [
 ('a_primer_on_frameql_v2_2_transcribed.md','https://raw.githubusercontent.com/datumwise/columna/main/apps/website/src/content/corpus/a_primer_on_frameql_v2_2.md'),
 ('frameql_an_introduction_v2_3_transcribed.md','https://raw.githubusercontent.com/datumwise/columna/main/apps/website/src/content/corpus/frameql_an_introduction_v2_3.md')]:
 b=(SRC/name).read_bytes();manifest.append(dict(name=name,source='full web-text transcription; normalized whitespace; not deposit bytes',url=url,viewed='2026-09-07',bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
(AUD/'source_manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
T='the_theory_of_data_v7_1_full_manuscript_working_draft_v0_4.md'
L='frameql_language_vnext_working_draft_v0_4.md'
N='frameql_v7_1_supporting_contract_notes_v0_1.md'
I='frameql_v7_1_authority_and_supersession_index_v0_1.md'
C='frameql_vnext_capability_profile_reconciliation_plan_v0_2.md'
A='frameql_v7_1_semantic_acceptance_cases_v0_1.md'
changes=[]
text=(SRC/'frameql_language_vnext_working_draft_v0_3.md').read_text()
def edit(old,new,why):
 global text
 n=text.count(old)
 if n!=1: raise ValueError((why,n,old[:100]))
 text=text.replace(old,new,1);changes.append(dict(document=L,reason=why,before=old,after=new))
def section(start,end,new,why):
 global text
 a=text.index(start); b=text.index(end,a)
 edit(text[a:b],new.rstrip()+'\n\n',why)
section('# The Frame-QL Manual — vNext Language-Law Candidate','# Preface',f'''# The Frame-QL Manual — vNext Language-Law Candidate

**Working Draft 0.4 — 7 September 2026**  
**Status:** Reconciled working semantic target; not the shipped Manual.  
**Theory reference:** [ToD v7.1 Full Manuscript Working Draft 0.4]({T}), abbreviated **T** below.  
**Scope:** Expression and request meaning, evidence and reuse obligations, and compatibility boundaries. This is not a complete grammar reference or a release-conformance claim.  
**No DOI assigned. Not a syntax release. Not an implementation authorization.**

This candidate succeeds Language-Law Candidate 0.3 for the local working program. The [authority and supersession index]({I}) identifies its supporting notes and the older rules withdrawn for current design. It does not replace a published edition, change repository files, or establish that current code conforms to the successor theory.

**Reading notation.** Fenced `frameql` examples retain familiar envelope forms; they were not executed in this documentation pass. Fenced `text` expressions and mathematical formulas describe semantics and do not claim parser acceptance. The applicable versioned grammar determines formal syntax, the language reference its versioned meaning, the profiles their obligations, and measured build records implementation coverage. T determines analytical family law. These responsibilities are distinct.

---
''','Identify frozen theory target and separate local semantics from release authority')
edit('This Manual states what Frame-QL means.','This candidate states the proposed reconciled language meaning. It is not a replacement for the applicable shipped reference until separately adopted.','Avoid claiming working candidate is already the shipped authority')
edit('Build Status reports what a particular shipped build actually runs.','Build Status records implementation coverage measured for a particular build. A coverage result is not, by itself, a proof of the complete analytical contract.','Distinguish measured coverage from semantic conformance')
edit("A profile may implement less or more than another profile.","Profiles may undertake different subsets of canonical language capabilities. Their declarations do not execute those capabilities or change their meaning.",'Profiles promise, builds implement')
edit('Its family identity and analytical lineage exist independently of the query.','Its family identity and constitutive analytical lineage are resolved from governed declarations. The chosen realization path and proof method for an already specified target do not create another family identity.','Constitutive lineage qualifier')
edit("Durable analytical identity is established by governed analytical law and Manifold declaration, not by an output label.","An admitted canonical analytical construction can denote a family without a separate business name. An output label does not establish that law, publish a declaration, or ratify a new analytical identity (§11).",'Family denotation versus naming/publication')
edit('A separate governed carve or population declaration is required where the population claim itself changes.', '''A separate governed carve or population declaration is required where the population claim itself changes.

Restriction must preserve the declared formation scope. A request-local law may deliberately form its inputs within the stated restriction. A previously constituted contextual quantity must not silently be re-formed under a new context while retaining the same claim. Selecting already-established daily changes differs from restarting the predecessor relation inside each selected group. Physical predicate pushdown is permitted only where that equivalence is established; this is a semantic obligation, not a new clause or prescribed plan. See T §§3.1–3.4 and §10.2.''','WHERE cannot silently change constitutive contextual formation')
section('## 3.5 Family-forming analytical expression','## 3.6 Ordered analytical expression',r'''## 3.5 Family-forming analytical expression

Conceptual examples include:

```text
sum(revenue @ {order})
mean(revenue @ {order})
variance(price @ {transaction})
count(order)
```

Where the complete admitted analytical law applies, a canonical family expression can denote the resulting family. It need not first receive a noun-like business name. Operator spelling alone does not supply the law: the target, formation, constitutive anchors, participation, basis adequacy, and admitted continuation must be established under T §4.

The inner anchor remains identity-bearing when changing it changes the quantity. `mean(revenue @ {order})` and `mean(revenue @ {customer})` need not denote the same family even when reported at the same outer anchor. Syntax, catalog membership, a query alias, or code execution does not replace this admission judgment.

Family-forming and ordered are not mutually exclusive classifications. An admitted ordered law is one case of this same family contract.
''','Reference complete target contract; ordered family construction admitted')
section('## 3.6 Ordered analytical expression','## 3.7 Predicate and standing expression',r'''## 3.6 Ordered analytical expression

An ordered expression uses a governed order of analytical points. Whether it denotes a family is a separate question about its complete analytical law.

T §§7–8 admits finite FIRST/LAST constructions through an independently constituted witness-valued family and a value-returning target family. General contextual expressions such as LAG, ranking, cumulative, and rolling operations need their own domain and operator contracts. Their focal syntax does not itself establish continuation, but a contextual formation history does not categorically prohibit a subsequently governed family (§6.10).

The earlier distinction between value order and analytical-point order remains useful: MAX compares operand values; LAST selects a point under the constitutive analytical order and returns its associated value. Both can belong to admitted family constructions. Neither is admitted merely by its name.

All such constructions must be invariant to incidental evidence enumeration to the extent claimed by their analytical laws. Backend row order, storage layout, and output `ORDER BY` supply no hidden inner-order authority. Chapter 9 describes the ordered-family and contextual-expression cases without merging their distinct requirements.
''','Withdraw categorical order-dependent family exclusion')
edit('These are language distinctions.\n\nThey are not additional ontological kinds in Theory of Data.','These are language distinctions, not a proposal for mutually exclusive runtime enum values. Some descriptions overlap: an ordered family-forming expression is both ordered and family-forming. They are not additional ontological kinds in Theory of Data.','Do not turn expression taxonomy into ontology or disjoint implementation enum')
edit('## 4.7 Anchoring does not create durable identity','## 4.7 Anchoring and family identity','Clarify identity follows law rather than anchor spelling')
# (reason default handled below)
edit('A governed Manifold declaration may separately promote a suitable expression into a family.\n\nThe query does not perform that promotion.', '''A complete governed analytical law can establish a family from a suitable expression. Its canonical family expression can then denote that identity without a separate business name. The act of anchoring an arbitrary arithmetic expression does not perform that admission, and `AS` or `WITH` does not publish or ratify it (§11).''','Avoid conflating analytical formation with institutional publication')
section('## 6.5 The family-law contract','## 6.6 Sufficient state belongs to analytical law',r'''## 6.5 The family-law contract

**T §4 is the governing family-law contract.** This language candidate references that contract rather than maintaining a competing shortened admission rule.

In particular, a family must specify its asserted target, either through a nominated non-circular defining construction or an independent semantic specification over the governed inputs and contributions. Candidate bases are checked against that target; agreement among bases cannot supply a missing target specification. The same law fixes formation, constitutive ancestry and parameters, admitted anchors and movements, participation and coverage, semantic value requirements, sufficient-state constructors and adequacy, and empty or undefined cases.

Frame-QL must resolve which admitted target and which meaning-bearing parameters the request selects. It must distinguish an absent or ambiguous definition from inadequate present evidence or unsupported implementation. A catalog entry stated at incomplete contract depth does not become realizable merely by appearing in an example here.

Canonical names resolve the identity; they do not mint it. Constitutive formation is identity-bearing where the law makes it so. A choice between compatible realizations or proof methods for the same specified target is not.
''','Mandatory target specification and one authoritative family contract')
section('## 6.6 Sufficient state belongs to analytical law','## 6.7 Rich-value state remains ordinary analytical data',r'''## 6.6 Sufficient state belongs to analytical law

For a target family F, an admitted basis is a collection of ordinary families whose established measures at A construct F@A under its law. T §§5–6 defines adequacy, well-foundedness, and coherence. Frame-QL consumes those obligations; it does not infer sufficiency from a type name or matching display.

For exact MEAN, SUM and COUNT supply one admitted basis. A finalized mean alone does not generally supply continuation state. An exact multiset can supply an alternative basis under the same participation law, while a set that discards multiplicity cannot replace it: the mean of `0, 0, 6` is 2; the mean after deduplication is 3.

Three questions remain distinct: whether a basis is valid for the target, whether its required measures are available in the present evidence, and whether a proposed substitution retains what a later operation requires. The two exact states `(sum=10,count=1)` and `(sum=1000,count=100)` both display 10, but adding `(20,1)` produces 15 and `1020/101`. Current display agreement is not continuation equivalence.

This also separates intake from continuation. Adding two retained counts 37 and 12 yields 49; treating them as two raw observations and counting them yields 2. The requested law determines which operation is intended.

An unavailable basis does not prove that the target is unavailable through every admitted argument. Conversely, an available scalar target does not prove that a particular basis is retained. Chapters 8–10 carry these distinctions into evidence, explanation, and reuse.
''','Basis correctness, present availability, and future substitution')
section('## 6.9 Availability is profile-specific','# 7. Semantic values, attributes, methods, and subscription',r'''## 6.9 Availability is profile-specific

A theoretically admitted law is not automatically a ratified language construct, a profile obligation, or an implemented operation. Those claims require their own versioned authorities. This chapter makes no new availability or implementation-conformance claim.

Exact semantic requirements also remain distinct from an approximate realization of the same target. Under T §10.9, an HLL estimate may target exact count distinct under an explicit approximation contract; it is not an exact sufficient-state basis for that target. Approximation does not automatically create another family identity, and it cannot excuse an undefined computation.

## 6.10 Contextual formation and later continuation

A contextual expression can be the input to an admitted family construction only when the target, constitutive formation and participation, empty or undefined cases, an independently establishable adequate basis, and coherent admitted continuation are specified. The continuation must not change the formation. These are the same T §4 obligations, not a new admission test.

For example, governed predecessor formation over `100, 110, 95, 105` yields changes `10, -15, 10`. Summing those established changes yields 5 under regrouping. Recomputing changes separately inside `(100,110)` and `(95,105)` yields 20 because it omits the boundary change. That is changed formation, not an alternative continuation of the original construction.

Faithful recomputation using the same governing formation and adequate evidence remains possible; caching is not a theoretical requirement. Ordinary LAG, rank, cumulative, or rolling syntax neither supplies a family contract by itself nor makes such a contract impossible merely because formation uses context.

---
''','Contextual formation admission and exact/approximate boundary')
edit("`level.last` belongs conceptually to ordered analytics.","`level.last` requires resolution to its complete governed analytical meaning; an admitted FIRST/LAST family law is possible, while the legacy spelling alone supplies no proof of that contract.",'Dotted LAST can denote admitted family without validating legacy encoding')
# Replace the standing chapter, retaining all substantive distinctions but not the old universal pipeline.
section('# 8. Analytical standing: existence, placement, eligibility, and support','# 9. Ordered analytical expressions',r'''# 8. Analytical standing: existence, placement, eligibility, and support

## 8.1 Standing questions precede carrier interpretation

A missing row, SQL NULL, NaN, absent JSON field, or failed conversion is a realization observation. It does not determine an analytical judgment by itself. T §§2.3 and 9 distinguish point existence, eligibility, evidence support, and supported values; the earlier R4 work additionally identifies support for placing an existing point under a governed anchor.

These are dependencies of particular claims, not a mandatory all-input pipeline. A request needs evidence sufficient for its actual law. The point whose existence or placement is unresolved must be identified: it may be a contributing point, not the already-established output point.

## 8.2 Point existence and placement

An existence law specifies what makes a root point belong to the universe. Evidence may establish existence, establish nonexistence, or leave a candidate's existence unresolved. Absence from a surviving physical table alone does not prove nonexistence.

When a point is known to exist and A is a governed anchor, partition law determines its unique A-block. Evidence may still be insufficient to identify that block. This is an unavailable placement judgment, not an invalid partition and not necessarily an unavailable operand value.

A known transaction can retain its value and Store placement while losing Day placement. A Store total may remain establishable; a complete Day breakdown may not. Conversely, an independently established Day output point can exist while source contributions cannot be placed into it. Do not relabel that output point nonexistent merely because its measure cannot be established.

## 8.3 Four different anchor-related failures

| Case | Meaning |
|---|---|
| A necessary input anchor is omitted | The request may have several identity-distinct readings. This is request determinacy, not missing data. |
| The referenced anchor is not governed | The requested analytical location is not established by the selected model. |
| A candidate point's existence is unresolved | The system lacks adequate evidence whether the point belongs to the governed domain. |
| An existing point's required projection is unresolved | The point is known; its membership under this particular anchor cannot be established. |

The exact refusal/clarification codes remain a versioned language and serving contract. No new code or standing enum is defined here.

## 8.4 Eligibility, support, and missing

At an established output point, a measure may be eligible, ineligible, or of unresolved eligibility. Its value is supported only where adequate evidence establishes it under the governing law.

The conceptual predicate `missing(E)` retains its narrow reading:

```text
established point + established eligibility + unsupported target value
```

It does not mean a nonexistent point, established ineligibility, unresolved eligibility, or carrier NULL. If the target point exists and eligibility is established, an upstream placement gap can be the reason the value is unsupported there. Calling that measure missing does not erase the distinct upstream cause.

This corrects the earlier overbroad precondition that every relevant contributing placement must already be established before target missingness can be described. Required evidence depends on the law; failure causes and target standing should both remain legible.

## 8.5 Lost records and point counts

Accepting a governed account that a particular transaction occurred but its record was lost can establish the point's existence independently of its values. A count of known transaction points can remain 100 while only 99 Revenue values are supported. That does not authorize a mean over the 100-point eligible population to shrink its denominator to 99.

`count(I)` and `count(x@I)` refer to different targets: point count and law-defined measure participation. A complete-case participation rule, where actually declared, defines its own contribution semantics; missing observations cannot silently establish that rule.

Loss of the whole record can affect existence evidence, coordinates, eligibility evidence, or values differently. Do not classify every known loss as universal value missingness, or every absent record as unsupported existence.

## 8.6 Target-relative evidence requirements

FIRST/LAST illustrates why a universal all-values-present rule would be wrong. With a fixed complete participating domain `s1 < s2 < s3`, known placement and order, and supported value 30 at the maximal point s3, the LAST witness can be established even when an earlier operand value is unavailable. SUM generally requires different evidence.

The converse limitation matters: a supported value at s3 is insufficient when a later eligible point may exist and affect the target. The law requires evidence about the possible winner, not simply a convenient supported value.

Under the ordinary last-participating-point law, an unsupported selected operand is not replaced by an earlier supported value. “Last participating point's value” and “last supported value” are different targets unless an admitted equivalence establishes otherwise.

## 8.7 An unavailable staged plan need not make the target unavailable

In T §9.5, participation and order of `s1 < s2 < s3` are known. The value at s1 is unavailable; s2 and s3 have supported values 20 and 30. An intermediate anchor separates `{s1}` from `{s2,s3}`. The first exact intermediate witness is unavailable, yet the coarser witness `(s3,30)` is established by the maximality evidence.

A plan consuming every intermediate witness cannot simply run with those missing inputs. Another adequate derivation can establish the target. In particular, **the unavailable intermediate witness must not be replaced by the known-empty identity**. Admitted movements do not by themselves establish a staged plan's evidence premises.

## 8.8 A scalar can be established without an identified winner

T §9.6 supplies a bounded value-only argument. Under a fixed LAST law, suppose `p < q`, p definitely participates, participation of q is unresolved, p and q exhaust all possible participants, and their operand values are supported as 7. The target is known nonempty; every possible winner has supported value 7. Thus scalar LAST is established as 7 while the winning point identity is not.

This argument requires **the fixed law, known nonemptiness, exhaustive possible-participant coverage, and supported equal values at every possible winner**. Equal observed values among surviving records are not enough. It establishes the scalar only, never a fabricated witness. These are premises of this particular argument, not a universal necessity test for all value-only establishment.

## 8.9 Empty contribution, unsupported value, and zero

The identity of a state-combination law represents known-empty contribution under that law. It is not semantic NULL and is not a replacement for unknown evidence. MIN/MAX may instead use a semigroup over nonempty supported fibers; no artificial empty value is required.

A supported zero is an ordinary established value. An absent observation can establish zero only under the applicable existence, participation, coverage, and completion law. `coalesce(E,0)` cannot manufacture that authority merely through a familiar spelling.

## 8.10 Frame-level consequence

A returned frame must not claim completeness after silently losing eligible evidence. Nor can a later disclosure validate a computation whose required participation was never established. In particular, removing an unplaced output row after an ordered walk does not undo that row's contribution to cumulative or predecessor results.

A partial-result contract must say which result is actually established and what is withheld. This document neither overturns the recorded R4-C0 empty-frame-with-disclosure decision nor certifies the current implementation as complete R4 support. Reported remaining ordered-path defects are not closed by this text.

## 8.11 Introspection remains a separate language decision

`exists`, `eligible`, `supported`, and `missing` above are conceptual names. Their public grammar, availability, unknown-case behavior, and wire representation are not finalized here. They inspect different analytical judgments; they are not generic functions over a nullable scalar domain.

---
''','Reconcile R4 with target-relative evidence and preserve upstream cause distinctions')
section('# 9. Ordered analytical expressions','# 10. Canonicalization and compatibility syntax',r'''# 9. Ordered families and contextual ordered expressions

## 9.1 Order is a semantic dependency, not a family veto

Analytical-point order and evidence enumeration are different. An admitted family can depend on a governed order of analytical points while its continuation is invariant to the order in which compatible contributions are processed. T §§7–8 provides the finite FIRST/LAST construction. Nothing in this chapter certifies every operation called `first` or `last`.

The MAX/LAST contrast concerns what is compared: operand values versus constitutive analytical points. It does not decide family standing. The complete target and family-law contract decides that question.

## 9.2 Constitutive ordered support

For the admitted construction, S is an ordinary constitutive input anchor. Its governed constituent anchors A1 through An jointly identify its existing points:

```text
q: S ↪ product(A1, ..., An)
```

The image need not fill the Cartesian product. Governance supplies a complete analytical-point order within each constituent anchor and a complete precedence among those constituents. Their lexicographic composition determines the order on existing S-points. This is the initial construction admitted by T, not a claim that every possible product order must be lexicographic.

A complete Day chronology does not automatically supply global Customer-Day order. When the claimed support is the whole compound space, its constituent orders and precedence must be established. A narrower fixed-customer context does not acquire cross-customer continuation because several customers happen to appear in the carrier.

Order structure is part of the identity where it constitutes the family law. Output-coordinate listing order, lexical identifier order, a lineage named `calendar`, and physical insertion order cannot silently supply it.

## 9.3 Form analytical points before selecting them

FIRST/LAST consumes established analytical support points under the declared law, not arbitrary finer carrier rows. Several Product records beneath one Account-Day point must first establish the operand at that Account-Day anchor. This does not authorize choosing SUM by convenience: the operand's governing formation determines the value.

If distinct support points are still indistinguishable under the supplied order representation, the claimed complete order is unestablished. The foundational FIRST/LAST construction has no generic physical tie-breaker. The valid response is to identify the missing law or failed realization premise, not append a row ID.

## 9.4 Witness family and value-returning family

T §8 defines a witness-valued family W independently from the operand, support order, and participation. It then defines a value-returning target L. Under an admitted nonempty construction:

```text
W@A = selected original support point with its value
L@A = value(W@A)
```

The witness family supplies sufficient state for the scalar target and may itself continue by the admitted extremum-witness law. The scalar does not generally retain the point needed for later witness comparison. Family standing and scalar re-entry sufficiency are separate facts.

A rich retained point–value family R supplies an alternative basis and an exact compatible-union-to-witness compression. R, W, and L are mathematical family names, not mandatory API names, types, storage stages, or separate public declarations. The language refers to T's proofs; it does not define another witness algebra here.

## 9.5 Continuation preserves original-point witnesses

For admitted `S ⪰ B ⪰ A`, intermediate states retain their original S-point witnesses and compare them under the same constitutive order. No new order on intermediate B labels is needed for that continuation.

This is not permission to cross every geometrically possible projection. The family must admit the movement and its evidence premises must hold. Selecting global LAST and summing separate customer LAST values are different constructions. A claim that LAST and another family operation commute needs its own law.

A typed tuple, governed point reference, or other faithful representation may carry the witness. The concrete CDT comparison and representation contract is a separate verification task; no nominal type named `Witness` is required by this text.

## 9.6 Contextual order and neighborhoods

LAG, LEAD, ranking, cumulative operations, and rolling operations require governed focal context. Their request semantics must determine, as relevant, the complete analytical points being considered, the comparison or positional relation, the contextual grouping, selection or neighborhood, boundary behavior, and operand participation.

For an account's daily balances the complete points may be Account-Day, not just Day labels. A contextual grouping cannot be inferred merely as “the output anchor minus the order key.” Changing presentation must not silently change that context.

A positional seven-point window differs from a preceding-seven-day range. A complete order does not alone supply a distance convention, endpoint inclusion, reset rule, or support-skipping policy. Rank may intentionally assign equal ordinal standing to equal compared values; that equality-class law is not a substitute for the complete support-point order of the foundational FIRST/LAST family.

These requirements describe contextual expression meaning. They neither automatically give the expression family continuation nor rule out a separately admitted family constructed from that expression. Section 6.10 and T §3.4 govern that admission.

## 9.7 Shorthand, output selection, and compatibility

A short ordered spelling is usable only when its governing environment determines the intended meaning under the selected language version. Completed meaning must be inspectable even when not every field is written in the query. T §7's family order is not a free query-time sort convention.

Query-level `ORDER BY` and `LIMIT ... PER` order or select the returned frame. They may happen to return the same number as an inner LAST expression, but that does not establish the same target, sufficient state, or continuation. Their legitimate use as frame selection is not prohibited merely because the results can coincide.

The published `.last` spelling and the old `FAMILY { last ORDER ... }` execution encoding are different compatibility questions. Preserve useful public reference where complete meaning can be resolved, but do not mechanically upgrade an incomplete declaration into v7.1 conformance. This document neither removes the spelling nor mandates retirement or preservation of a particular internal mechanism.

---
''','Ordered family W/L/R account separate from contextual expression contracts')
section('# 10. Canonicalization and compatibility syntax','# 11. Manifold promotion boundary',r'''# 10. Resolution, canonicalization, and materialized reuse

## 10.1 Resolve the target before selecting a realization

Canonical resolution counts distinct analytical meanings, not spellings, execution paths, or available bases. Under the selected governed environment:

```text
no lawful analytical reading      → cannot serve this request as stated
one distinct analytical reading   → target resolved; evidence and realization remain to check
several user-distinguishable readings → clarify the intended target
```

The zero/one/many discipline does not turn every unavailable plan into an absent meaning. A fully specified target can remain well defined when its required evidence is unavailable. Exact disposition codes belong to the applicable serving contract.

MEAN over orders and MEAN over customers may be two meanings. SUM/COUNT and an adequate multiset construction for one fixed MEAN are two bases for one meaning. Current numerical equality does not collapse different family identities, and different valid proof methods do not split one identity.

If two meanings remain but only one is presently executable, executable availability does not choose the user's intent. Once the meaning is fixed, choosing among compatible admitted realizations need not become another intent question.

## 10.2 Four different records

Distinguish the normalized surface statement, the resolved analytical meaning, a proposed physical plan, and the evidence establishing the particular result or its premises. These are responsibilities, not a prescribed new wire schema.

A canonical surface renderer may retain a parse/render round-trip contract. The complete resolved meaning can be exposed separately; it need not be forced into unsupported surface syntax. The selected family, constitutive anchors and order, participation, and target anchor must not diverge between explanation and execution.

## 10.3 EXPLAIN states what is known and what remains to be established

EXPLAIN can show resolved meaning, proposed realization, and applicable existing assurance without executing the result computation. It must distinguish those facts from checks not yet performed and from evidence that is not applicable or current.

A data-free explanation cannot promise every disclosure a later execution will produce unless adequate applicable evidence already establishes all those conditions. A clean static explanation does not certify unobserved placement completeness, coherent inputs, or a numerical result. This is corrected successor-reference wording; it does not claim that the present EXPLAIN payload already exposes all these distinctions.

## 10.4 Input anchors and governed completion

An omitted identity-bearing anchor or law parameter may be completed only when the governed definitions determine one meaning, including any established equivalences. Default completion selects an already defined construction; it does not invent identity.

An unavailable preferred basis, cache, or engine path may be disclosed as a constraint, not used to silently select another target. Governance-controlled alternatives must remain visibly alternatives when they change the requested quantity.

## 10.5 Dots, brackets, and retained surfaces

Historical `revenue.sum` may resolve to a governed sum-family reference or construction. Historical `level.last` may resolve to an admitted ordered family where the full contract exists. Neither dotted spelling decides family standing or proves the current execution encoding faithful. Normalization must respect constitutive anchors, input formation, and retained information; it is not a string substitution.

In this working target, `[]` remains reserved for semantic-value subscription, not the earlier analytical bracket-filter roadmap. That supersedes the roadmap recommendation, not an actual parser release. Exact accepted syntax remains versioned separately.

`AS` names an output key; supported `WITH` forms provide query-local reuse. Neither ratifies an analytical law or grants institutional publication authority. Section 11 distinguishes these acts from canonical family denotation.

## 10.6 Retained content, established claim, and permitted reuse

A catalog entry saying only “LAST at A is available” is insufficient for deciding reuse. T §10.7 distinguishes:

| Retained content | Established claim | Reuse boundary |
|---|---|---|
| Nonempty witness W@A | Selected point and associated value under the applicable evidence | Scalar projection and admitted witness continuation under compatible premises |
| Scalar L@A after valid witness finalization, witness no longer retained or recoverable | The scalar target | No inferred witness reconstruction or continuation |
| Scalar L@A established without identifying the winner | The scalar target under its adequate argument | No selected-point claim or inferred witness capability |

The last two rows can have the same family identity and value. Their establishment records and retained capabilities differ. The third row includes the specific argument of §8.8 only under its fixed law, known nonemptiness, exhaustive possible-participant coverage, and supported equal values at every possible winner.

An established witness can supply the scalar through its admitted constructor. The scalar does not generally supply the witness. A history recording that a witness was once used is not proof that the witness remains recoverable now.

## 10.7 Compatibility before lossy combination

A compressed winner is not a global consistency validator. If `p < q`, one source's `(p,10),(q,20)` compresses to `(q,20)` and can hide a conflicting `(p,11)` supplied later. A local equal-point conflict exception does not establish coherent inputs after the conflicting point has been discarded.

The evidence and context required for combination must be established outside that lossy shortcut. Matching context labels alone do not prove the premise. Nor does this require a full source-record set in every witness: a sufficient assurance or recoverability account can establish the needed compatibility. The concrete mechanism is outside this language revision.

## 10.8 Reuse is specific to the next operation

Witness coarsening does not automatically answer a later restriction that excludes the winner, a deletion of that winner, or changed formation. Additive summaries with overlapping contributions cannot simply be combined without compatible contribution accounting. Approximate and exact realizations of the same target are not interchangeable merely because their family IDs match.

The governing rule is the same throughout: retained information and established premises must justify the particular target and reuse being claimed. Material availability creates no additional analytical permission.

---
''','Resolve meaning separately from plans; same meaning shared by EXPLAIN and execution; retained content and evidence')
section('# 11. Manifold promotion boundary','# 12. Validity, adjudication, and realization',r'''# 11. Family denotation, naming, and publication

## 11.1 Canonical denotation does not require a business-name ceremony

A complete admitted canonical construction can denote a family directly. Under an established MEAN law and constitutive operand, `mean(revenue@order)` can be an identity-bearing reference even before a separate human-readable name is assigned.

This does not turn arbitrary query syntax into governance authority. The target specification and family contract must already be supplied by the selected governed definitions and applicable law. Neither successful computation nor an alias proves that contract.

## 11.2 Output naming and institutional authoring are separate

An `AS` alias changes a frame column key. A supported `WITH` macro binds query-local text or expression reuse according to its language contract. Saving a query persists the request. None of these acts publishes or ratifies a new Manifold declaration.

A governed authoring process may establish a durable named definition or binding when authorized to do so. Names resolve existing identity; changes to an identity-bearing formation or law establish succession rather than redefining the old family retroactively. Proof method and physical plan remain outside constitutive identity.

## 11.3 Contextual and structural declarations

A named contextual expression does not automatically gain family continuation. A separately admitted family constructed from it must satisfy T §4 and preserve its stated formation. This applies to ordered and unordered contextual formation alike.

A categorical-looking value also does not automatically create an anchor. A structural declaration must establish the partition or explicit universe construction it claims, including contribution semantics when relationships overlap.

## 11.4 No new authoring format is specified here

This language revision does not add a Manifold kind, a `DERIVED` syntax, a publication field, or a witness type. Those are separate specification tasks. The distinction established here is semantic: denoting a family, naming an output, retaining a result, and publishing an authoritative definition are different acts.

---
''','Replace overbroad query-only identity and promotion rule')
section('# 12. Validity, adjudication, and realization','# 13. Capability and profile boundary',r'''# 12. Validity, adjudication, and realization

A parseable request is not necessarily determinate, supported, realizable, or authorized. The language must preserve those distinctions instead of mapping every problem to a nullable cell or an engine exception.

The selected governed model supplies the analytical laws. Resolution identifies the target and required context. Evidence establishes the applicable premises. A profile and implementation determine whether an admitted realization is supported here. Trusted execution must remain faithful to the resolved meaning. Institutional authorization and result policy remain surrounding responsibilities.

These dependencies do not require all evidence checks to run before every planning step: planning can identify missing premises, and an execution can obtain evidence. What it cannot do is silently rewrite the target, reinterpret assured declarations from physical conventions, or replace an unknown premise with a convenient default.

The planner selects the admitted route and semantic operation; execution performs that operation. Declaration is not certification, and absence of contradiction is not permission. Existing positive-admission boundaries are retained. A later disclosure cannot make an unestablished computation a lawful answer.

Refusal, clarification, partial-result contracts, and errors retain their versioned meanings. No new reason code, outcome, standing enum, wire field, or approval workflow is created by this document. Known engineering defects reported in earlier reconnaissance remain a separate correctness mission; this revision neither reproduces nor closes them.

---
''','Preserve analytical/realization/authority distinctions without imposing false pipeline')
section('# 13. Capability and profile boundary','# 14. Semantic acceptance suite',f'''# 13. Capability and profile boundary

The canonical language defines expression meaning and language standing. Profiles undertake subsets of those capabilities; build records report measured realization. T independently decides whether a construction satisfies analytical family law. A callable spelling or runtime kind does not answer all these questions.

In particular, distinguish analytical-point-order dependence, family-law admission, retained value/state capability, and the operation a representation is licensed to perform next. These distinctions do not require four new registry columns. The [rebased reconciliation plan]({C}) gives the constraints for a later schema review.

An implementation may route FIRST/LAST through legacy machinery while the successor theory has a different account of their admitted laws. That is a declared implementation gap or compatibility boundary, not evidence that the machinery already conforms. A displayed-value re-entry flag cannot be changed merely because ordered family admission is now possible.

No Core promise is reduced or enlarged in this document. No Platform-only dialect is introduced. Existing versioned grammar, profile files, generated capability tables, and measured build status remain unchanged. A future adoption must explicitly map language coverage, known limitations, and implementation evidence; it cannot manufacture agreement by editing generated status by hand.

---
''','Capability categories do not conflate law, runtime and re-entry')
section('# 14. Semantic acceptance suite','# 15. Remaining work before implementation reconciliation',f'''# 14. Semantic acceptance suite

The [companion acceptance set]({A}) records the reconciled expectations with premises, expected judgments, prohibited shortcuts, and source sections. These are semantic review cases, **not executed Columna tests or a new formal proof suite**.

The principal questions are whether FIRST/LAST can be admitted without certifying legacy paths, whether a target is distinguished from its bases, whether partial evidence is handled under the actual law, whether retained content limits reuse, and whether versioned syntax/coverage stays separate from theory.

The older §14 rows that categorically placed LAST outside families are superseded. So are intermediate acceptance claims using universal formation locality or admitting TOP-k without a complete contract. The active index identifies the historical files rather than silently deleting the research record.

---
''','Migrate semantic acceptance tests with rules')
section('# 15. Remaining work before implementation reconciliation','# 16. Status',f'''# 15. Remaining work before implementation reconciliation

The local companion set now uses one theory reference and one language-law target. Its supporting notes and supersession index must travel together when used for review. Older handoffs are not current instructions merely because a filename says “settled” or “PASS.”

This documentation pass does not decide public grammar for order declarations, typed subscriptions, standing predicates, or new authoring kinds. It does not establish actual CDT capability, choose a runtime representation, or fix reported ordered-path defects. Those require bounded interface and engineering work after their own authorization.

The draft successors of the Introduction and Primer preserve their entry-point purpose. Repository/site/deposit adoption, release-specific reference patches, and final publication metadata remain separate tasks. This local candidate must not be advertised as already shipped.

---
''','Explicit remaining installation and interface gates')
section('# 16. Status','\n', '# 16. Status','noop') if False else None
# replace remaining final status via exact tail
pos=text.index('# 16. Status')
edit(text[pos:],f'''# 16. Status and sources

This is a local working language-law candidate aligned to T Draft 0.4, not a published language edition or implementation authorization. T remains unchanged. Its proofs and their recorded validation status are referenced, not reproduced or rerun here.

The [active-source index]({I}) is the reading entry point. The [supporting notes]({N}) own the order-completion, contextual-domain, standing, and order-realization explanations subordinate to this candidate. The [acceptance set]({A}) records semantic checks. The [capability/profile plan]({C}) records future reconciliation constraints without changing those authorities.

The source and change register supplies exact local input hashes, full-text Intro/Primer retrieval provenance, and the diff against candidate 0.3. Historical publications retain their own versioned statements. Only the active working guidance identified in this package is superseded for current design.
''','Status and source references')
# Clarify authority one time in initial chapter without more duplicate machinery.
needle='It does not redefine them.'
edit(needle,needle+' The authored Manifold supplies the selected logical definitions; separate private mappings and runtime evidence realize them. Physical bindings do not become authored analytical law.','Logical-only Manifold boundary')
edit('## 6.8 Family aliases and governed named families', 'An exact finite set or multiset can retain a growing amount of evidence. Failure to provide a bounded-size sketch is not proof that no finite exact sufficient basis exists. Analytical adequacy and the cost of a particular representation remain different questions.\n\n## 6.8 Family aliases and governed named families','Bounded memory versus finite exact state')
(OUT/L).write_text(text)
(AUD/'language_edits.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2)+'\n')
(AUD/'language_v0_3_to_v0_4.diff').write_text(''.join(difflib.unified_diff((SRC/local_names[1]).read_text().splitlines(True),text.splitlines(True),fromfile=local_names[1],tofile=L)))
print('Language candidate:',len(text.encode()),'bytes;',len(text.split()),'words;',len(changes),'edits')
