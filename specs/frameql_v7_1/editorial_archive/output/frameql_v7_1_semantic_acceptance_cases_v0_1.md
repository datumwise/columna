# Frame-QL / ToD v7.1 — Semantic Acceptance Cases

**Working set 0.1 — 7 September 2026**  
**Status:** 40 source-derived semantic review cases, not executed Columna tests, mathematical proofs, or release-conformance claims.  
**Theory:** [T Draft 0.4](the_theory_of_data_v7_1_full_manuscript_working_draft_v0_4.md). **Language:** [Candidate 0.4](frameql_language_vnext_working_draft_v0_4.md).

Each case states its premises so a future test cannot replace the governed claim with an easier one. Exact runtime outcomes or reason codes are not invented where only the semantic disposition is fixed. Contextual-language implications are identified by their LQ sections; the underlying family and evidence rules remain T's.

The [JSON companion](frameql_v7_1_semantic_acceptance_cases_v0_1.json) contains the same cases for future review tooling. This pass checks document consistency and premise coverage; it does not run these cases against an engine.

## F01 — Specified target before bases

**Premises.** A proposed family has two mutually agreeing constructors but no nominated defining construction or independent target specification.

**Expected judgment.** The family contract is incomplete; agreement has no independently specified target against which adequacy can be judged.

**Do not.** Admit the family solely because the two implementations agree.

**Sources:** T §§4, 5.3; LQ §6.5.

## F02 — Canonical family without a business name

**Premises.** An admitted law and fully specified constitutive input establish mean(revenue@order); no business alias has been assigned.

**Expected judgment.** Its canonical family expression can denote the family. Institutional publication remains a separate authority.

**Do not.** Require an AS name or a new authoring ceremony before the analytical identity can be denoted.

**Sources:** T §§3.9, 4; LQ §§3.5, 11.1.

## F03 — Aliases do not admit law

**Premises.** A query computes revenue/orders AS aov without a supplied AOV family contract.

**Expected judgment.** The alias names an output; it does not establish the missing law. An explicitly governed AOV family remains possible.

**Do not.** Treat output naming as either automatic family admission or a permanent ban on an AOV family.

**Sources:** T §§3.5, 3.7, 3.9; LQ §§2.3, 11.2.

## F04 — Constitutive ancestry versus plan

**Premises.** Two licensed derivations claim the same family and anchor using different staging paths under matching premises.

**Expected judgment.** Consistency applies to the same target; physical path/proof method is not new identity.

**Do not.** Include plan identity in the family signature to evade required agreement.

**Sources:** T §§2.2, 6.4–6.5; LQ §§3.1, 10.1.

## F05 — Meaning before executable availability

**Premises.** Mean over orders and mean over customers are identity-distinct possible readings; only one has a presently executable plan.

**Expected judgment.** The unresolved intent distinction remains. Availability can be reported, not silently used to choose meaning.

**Do not.** Serve the available target as though availability resolved the request.

**Sources:** T §§2.2, 3.9, 9.1; LQ §10.1.

## F06 — Several bases, one target

**Premises.** SUM/COUNT and an exact multiset are both adequate and available for the same fixed MEAN with matching participation.

**Expected judgment.** They are alternative constructions of one target, not an intent ambiguity.

**Do not.** Return Clarify merely because there are two bases.

**Sources:** T §§5.3, 5.5; LQ §§6.6, 10.1.

## F07 — Multiplicity remains part of the law

**Premises.** Ordinary MEAN is defined over participating values 0,0,6.

**Expected judgment.** The mean is 2; replacing the multiset by set {0,6} yields another construction and gives 3.

**Do not.** Declare a deduplicating set an exact basis for this MEAN.

**Sources:** T §5.3; LQ §6.6.

## F08 — Intake versus continuation

**Premises.** Two retained count values 37 and 12 represent compatible disjoint contributions.

**Expected judgment.** Count continuation adds them to 49. Counting the two summary rows instead would answer a different question.

**Do not.** Use count-of-summary-rows as count-state merge.

**Sources:** T §5.2; LQ §6.6.

## O01 — One-dimensional analytical order

**Premises.** Day is a governed anchor with complete chronology and the family has its remaining complete contract.

**Expected judgment.** Precedence is trivial; the declared order supports the admitted finite FIRST/LAST construction.

**Do not.** Require a new generic tie policy or infer chronology from a lineage label alone.

**Sources:** T §§7.1, 8; LQ §9.2.

## O02 — Compound precedence required

**Premises.** Customer and Day have complete point orders, but no precedence is supplied for the claimed global Customer-Day support.

**Expected judgment.** The compound order is not fully selected.

**Do not.** Infer precedence from output column order.

**Sources:** T §7.1; LQ §9.2.

## O03 — Missing constituent order

**Premises.** Precedence is supplied but Customer has no complete governed point order.

**Expected judgment.** The claimed complete compound order is unestablished.

**Do not.** Sort Customer IDs lexically as an implicit analytical order.

**Sources:** T §§7.1–7.3; LQ §9.2.

## O04 — Sparse analytical point space

**Premises.** The governed support contains only (C1,d3),(C2,d1),(C2,d2).

**Expected judgment.** Only these points participate; order does not create (C2,d3) or another absent combination.

**Do not.** Fill the Cartesian product before LAST without an existence law.

**Sources:** T §§2.1.3, 7.1; LQ §9.2.

## O05 — Form the support measure first

**Premises.** Several Product carrier records lie beneath one Account-Day point.

**Expected judgment.** Apply the operand formation law to establish its value at Account-Day before FIRST/LAST consumes that analytical point.

**Do not.** Select a raw row by day or invent SUM as the formation rule merely to collapse duplicates.

**Sources:** T §§3.1, 7.3; LQ §9.3.

## O06 — Ordered family not automatic legacy conformance

**Premises.** FIRST/LAST has an admitted construction in T; a legacy .last spelling is accepted by a particular build.

**Expected judgment.** Analytical admission and that execution path’s conformance are separate claims.

**Do not.** Certify every existing .last because the theory now admits an ordered family.

**Sources:** T §§3.6, 4, 8; LQ §§9.1, 9.7, 13.

## O07 — Original point witness through coarsening

**Premises.** For s1<s2<s3<s4, admitted intermediate groups are {s1,s4} and {s2,s3}, with coherent supported values.

**Expected judgment.** Retained winners s4 and s3 combine to s4 using the original support order.

**Do not.** Compare intermediate group labels or demand an unrelated new order on B.

**Sources:** T §§8.3–8.4; LQ §9.5.

## O08 — Scalar is not witness continuation

**Premises.** An exact scalar LAST was materialized but its selected point is not retained or recoverable.

**Expected judgment.** The scalar target is available; further witness comparison is not licensed from it alone.

**Do not.** Set scalar re-entry true merely because LAST has family standing.

**Sources:** T §§8.1, 10.7; LQ §§9.4, 10.6.

## O09 — R is optional

**Premises.** An adequate argument establishes W; a full retained point–value set is unavailable.

**Expected judgment.** W can be used under its actual admitted contract; full R storage is not mandatory.

**Do not.** Impose R→W→L as a required runtime/storage pipeline.

**Sources:** T §§8.6, 9.2; LQ §9.4.

## O10 — Same results, different laws

**Premises.** Two different declared precedence orders currently yield the same winner.

**Expected judgment.** Numerical agreement does not merge their analytical identities.

**Do not.** Infer equivalent family identity from observed equality.

**Sources:** T §§2.2, 7.2; LQ §§9.2, 10.1.

## O11 — Frame selection can coincide with LAST

**Premises.** A versioned output ORDER BY/LIMIT PER query selects a row whose value equals a LAST answer.

**Expected judgment.** Frame selection remains legitimate in its own scope; no inner family identity or reusable witness follows.

**Do not.** Either ban the frame operation or use it as ambient order/family proof.

**Sources:** T §12.4; LQ §9.7.

## C01 — Contextual formation can precede a family

**Premises.** The law fixes daily predecessor formation over 100,110,95,105 and a separately admitted additive family over the changes.

**Expected judgment.** Established changes 10,-15,10 sum to 5 coherently.

**Do not.** Exclude the family solely because formation used neighboring points.

**Sources:** T §§3.3–3.4; LQ §6.10.

## C02 — Restriction must preserve formation

**Premises.** The same change family is requested after grouping the source into pairs.

**Expected judgment.** Reusing original changes differs from restarting predecessor formation inside the pairs, which gives 20.

**Do not.** Push a restriction/grouping through formation without an equivalence justification.

**Sources:** T §§3.3, 10.2; LQ §§2.4, 6.10.

## C03 — Faithful recomputation is not forbidden

**Premises.** The original contextual formation and its full governing context can be reproduced from adequate evidence.

**Expected judgment.** Recomputation can establish the same constitutive values; caching is not required by the theory.

**Do not.** Interpret “do not change formation” as “never recompute.”

**Sources:** T §§3.3–3.4; LQ §6.10.

## C04 — Focal window law needs its own contract

**Premises.** A rolling expression is written without specifying positional versus time-range neighborhood and material endpoint conventions.

**Expected judgment.** The expression’s meaning remains incomplete where these choices change the result.

**Do not.** Treat complete order alone as a full window specification or automatically admit family continuation.

**Sources:** T §§3.4, 11.4; LQ §9.6.

## E01 — Established output, unplaced source

**Premises.** A Day output point exists and Revenue is eligible, but required known source contributions cannot be placed by Day.

**Expected judgment.** The target value may be unsupported; the upstream placement cause remains distinct.

**Do not.** Declare the output point nonexistent or forbid target missingness solely because a source placement is unresolved.

**Sources:** T §§2.3, 9.1–9.4; LQ §§8.1–8.4.

## E02 — Known domain with incomplete operand support

**Premises.** Governance establishes exactly 100 participating transactions, with 99 supported Revenue observations.

**Expected judgment.** Point count is 100; a count under a declared supported-operand participation law may be 99. A mean over all 100 cannot silently shrink.

**Do not.** Infer intended population from surviving ordinary rows.

**Sources:** T §§2.3, 4.2, 11.5.1; LQ §8.5.

## E03 — Coarser witness, unavailable staged input

**Premises.** Participation s1<s2<s3 and intermediate blocks {s1},{s2,s3} are known; f(s1) unavailable, f(s2)=20 and f(s3)=30 supported.

**Expected judgment.** Coarser W=(s3,30) is established by maximality evidence even though a plan consuming both exact intermediate witnesses lacks an input.

**Do not.** Replace unavailable intermediate W with known-empty identity, or infer target impossibility from this plan’s failure.

**Sources:** T §§6.1, 9.5; LQ §8.7.

## E04 — Scalar without winner identity

**Premises.** Fixed LAST law; p<q; p definitely participates; q participation unresolved; p,q exhaust possible participants; both operand values supported as 7.

**Expected judgment.** Nonempty scalar L=7 is established; selected-point W is not.

**Do not.** Claim W, choose an arbitrary observed 7 without the exhaustive evidence, or treat W as necessary for every L proof.

**Sources:** T §9.6; LQ §8.8.

## E05 — Missing selected operand

**Premises.** Participation and order identify the latest eligible point, whose operand value is unsupported.

**Expected judgment.** Ordinary LAST value is unsupported unless another adequate argument establishes the same target.

**Do not.** Return an earlier supported value by silent support-skipping.

**Sources:** T §§9.2–9.3; LQ §8.6.

## E06 — Known empty is not unknown

**Premises.** An intermediate contribution set is unknown, or the selected value is unsupported.

**Expected judgment.** No algebraic unit can stand for that unknown evidence without a separate admitted argument.

**Do not.** Coerce carrier NULL or unknown support to bottom/zero/empty set.

**Sources:** T §§5.2, 6.1.1, 8.2, 9; LQ §8.9.

## E07 — Late filtering cannot undo ordered influence

**Premises.** An unplaceable contribution affects cumulative/lag output, then its own row is withheld.

**Expected judgment.** The resulting computation has not been repaired by the late withholding.

**Do not.** Report ordinary established results merely because no NULL-coordinate row remains.

**Sources:** T §9.4; LQ §8.10.

## R01 — Lossy compression can hide contradiction

**Premises.** With p<q, one alleged coherent input has (p,10),(q,20); another has (p,11).

**Expected judgment.** Their coherent-instance premise is violated; compressed winner comparison cannot validate it.

**Do not.** Treat equal-point conflict checks or a common context label as a global consistency certificate.

**Sources:** T §10.6; LQ §10.7.

## R02 — Three materialization claims

**Premises.** A catalog holds W, scalar L projected from discarded W, or scalar L established without identifying its winner.

**Expected judgment.** Record retained content, established claim and justification, and permitted reuse; the scalar rows need not have different family identities.

**Do not.** Collapse all entries into “LAST available” or create family identity by proof method.

**Sources:** T §10.7; LQ §10.6.

## R03 — Equal mean display, unequal continuation

**Premises.** Exact states (10,1) and (1000,100) both display 10; both are extended by (20,1).

**Expected judgment.** The results become 15 and 1020/101; scalar equality did not preserve continuation information.

**Do not.** Merge or substitute displayed means as adequate state.

**Sources:** T §10.5; LQ §6.6.

## R04 — Restriction or deletion of winner

**Premises.** Only the compressed maximal witness is retained, and the next request excludes or deletes that point.

**Expected judgment.** A new adequate derivation or richer retained information is required to identify its replacement.

**Do not.** Infer arbitrary filtering/deletion capability from witness coarsening capability.

**Sources:** T §§10.2–10.3; LQ §10.8.

## R05 — Approximate realization of unchanged target

**Premises.** An explicit approximation contract supports an HLL estimate of exact count distinct.

**Expected judgment.** It may target the same family while remaining an approximate realization, not an exact sufficient-state basis.

**Do not.** Invent a new target solely from error grade, or silently reuse the estimate as exact state.

**Sources:** T §10.9; LQ §§6.9, 10.8.

## G01 — EXPLAIN does not observe unperformed checks

**Premises.** EXPLAIN resolves meaning and a proposed plan without data execution or applicable evidence for all runtime conditions.

**Expected judgment.** It distinguishes what is established from checks outstanding.

**Do not.** Guarantee all future disclosures or complete data support from a data-free explanation.

**Sources:** T §§9.1, 12.3–12.4; LQ §10.3.

## G02 — Family law versus engine kind

**Premises.** An operator belongs to a runtime category or a canonical capability list.

**Expected judgment.** Family admission still needs the complete target/law contract; category does not confer authority.

**Do not.** Grant family founding solely from an anchor-changing kind.

**Sources:** T §3.6; LQ §13.

## G03 — No syntax from theory alone

**Premises.** The theory admits tuples, witnesses, order definitions or a family construction not exposed by a shipped grammar/profile.

**Expected judgment.** Semantic admission and language/implementation availability remain separate.

**Do not.** Advertise theoretical notation as accepted syntax or edit measured build status to imply support.

**Sources:** T §§12–13; LQ §§1, 13.

## G04 — CDT interface remains unverified

**Premises.** This pass specifies required comparison and representation behavior but does not inspect CDT v0.5.

**Expected judgment.** Readiness is unverified; a new nominal Witness type is neither asserted absent nor mandated.

**Do not.** Claim present API support/absence from the theory manuscript.

**Sources:** T §§8.5, 12.2, 13.3; LQ §9.5.

## G05 — Historical instructions are not active authority

**Premises.** An earlier O1/O2/M2/CP document says FIRST/LAST cannot found families or universal formation locality is required.

**Expected judgment.** Use the explicit current supersession index and reconciled language target; preserve historical observations at their own snapshots.

**Do not.** Execute an old “settled” instruction because its filename or prior PASS sounds authoritative.

**Sources:** T Appendix C.4; LQ §§15–16.

