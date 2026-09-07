# ToD v7.1 / Frame-QL — Joint Consistency Case Ledger

**Review 0.1 — 7 September 2026**

Forty reviewer-authored source comparisons. These are not executed Frame-QL cases, new mathematical proofs, or runtime conformance tests. “Consistent” means the stated expectation is supported by the referenced texts under the supplied premises. It is not a guarantee that all possible defects have been excluded.

**T:** [the_theory_of_data_v7_1_full_manuscript_working_draft_v0_4.md](reviewed_sources/the_theory_of_data_v7_1_full_manuscript_working_draft_v0_4.md).  
**LQ:** [frameql_language_vnext_working_draft_v0_4.md](reviewed_sources/frameql_language_vnext_working_draft_v0_4.md).

**Result:** 39 cases need no local correction. E02 agrees at the contract level; J1 makes a separate LQ §6.3 count example carry its required participation premise explicitly. No change to the forty expected judgments is proposed.

## F01 — Specified target before bases

**Premises.** A proposed family has two mutually agreeing constructors but no nominated defining construction or independent target specification.

**Expected judgment.** The family contract is incomplete; agreement has no independently specified target against which adequacy can be judged.

**Do not.** Admit the family solely because the two implementations agree.

**Review.** T requires a nominated defining construction or independent target specification before adequacy can be checked. LQ explicitly delegates admission to that contract. Two agreeing implementations cannot fill the missing target.

**Source comparison:** T §§4, 5.3; LQ §6.5. Supporting notes §5; capability plan §2; Introduction §6.2.

## F02 — Canonical family without a business name

**Premises.** An admitted law and fully specified constitutive input establish mean(revenue@order); no business alias has been assigned.

**Expected judgment.** Its canonical family expression can denote the family. Institutional publication remains a separate authority.

**Do not.** Require an AS name or a new authoring ceremony before the analytical identity can be denoted.

**Review.** The family can be denoted by its admitted canonical expression without a business name. Both texts preserve the distinct institutional act of publication; neither syntax nor successful computation supplies a missing law.

**Source comparison:** T §§3.9, 4; LQ §§3.5, 11.1. Supporting notes §1.2; Introduction §§6.2, 8.3; Primer, “Why Frame-QL Has @ and AT”.

## F03 — Aliases do not admit law

**Premises.** A query computes revenue/orders AS aov without a supplied AOV family contract.

**Expected judgment.** The alias names an output; it does not establish the missing law. An explicitly governed AOV family remains possible.

**Do not.** Treat output naming as either automatic family admission or a permanent ban on an AOV family.

**Review.** The query alias remains a column key. The positive, governed AOV example is retained in T; the language does not turn the warning against automatic admission into a ban on a ratio family.

**Source comparison:** T §§3.5, 3.7, 3.9; LQ §§2.3, 11.2. Introduction §6.2; integration sheet §3.

## F04 — Constitutive ancestry versus plan

**Premises.** Two licensed derivations claim the same family and anchor using different staging paths under matching premises.

**Expected judgment.** Consistency applies to the same target; physical path/proof method is not new identity.

**Do not.** Include plan identity in the family signature to evade required agreement.

**Review.** Constitutive ancestry identifies the target; an alternative lawful realization or proof of that target does not create another family. Both texts retain identity-relative agreement rather than defeating it through path-specific IDs.

**Source comparison:** T §§2.2, 6.4–6.5; LQ §§3.1, 10.1. Supporting notes §1.2; Introduction §8.2; integration sheet §5.

## F05 — Meaning before executable availability

**Premises.** Mean over orders and mean over customers are identity-distinct possible readings; only one has a presently executable plan.

**Expected judgment.** The unresolved intent distinction remains. Availability can be reported, not silently used to choose meaning.

**Do not.** Serve the available target as though availability resolved the request.

**Review.** The two analytical readings remain distinct when only one can execute. Availability is a constraint reported after meaning is resolved, not evidence of the user's intended quantity.

**Source comparison:** T §§2.2, 3.9, 9.1; LQ §10.1. Supporting notes §1.2; Introduction §3; Primer, “Why Output Dimensions Are Not Always Enough”; integration sheet §6.

## F06 — Several bases, one target

**Premises.** SUM/COUNT and an exact multiset are both adequate and available for the same fixed MEAN with matching participation.

**Expected judgment.** They are alternative constructions of one target, not an intent ambiguity.

**Do not.** Return Clarify merely because there are two bases.

**Review.** Adequate SUM/COUNT and multiset constructions are two ways to establish one target. Their common participation and domains must hold; selecting a realization does not require a new intent clarification.

**Source comparison:** T §§5.3, 5.5; LQ §§6.6, 10.1. Supporting notes §1.2; Introduction §3; integration sheet §6.

## F07 — Multiplicity remains part of the law

**Premises.** Ordinary MEAN is defined over participating values 0,0,6.

**Expected judgment.** The mean is 2; replacing the multiset by set {0,6} yields another construction and gives 3.

**Do not.** Declare a deduplicating set an exact basis for this MEAN.

**Review.** The target specifies multiplicity. Set deduplication changes the inputs of ordinary MEAN, so the equality of a candidate constructor on other cases cannot make the set a sufficient basis here.

**Source comparison:** T §5.3; LQ §6.6. Supporting notes §5; statistical supplement S.2 and S.7.

## F08 — Intake versus continuation

**Premises.** Two retained count values 37 and 12 represent compatible disjoint contributions.

**Expected judgment.** Count continuation adds them to 49. Counting the two summary rows instead would answer a different question.

**Do not.** Use count-of-summary-rows as count-state merge.

**Review.** Continuation consumes retained counts as additive state and yields 49, not two. The distinction is an analytical input role, not something inferred from an integer type or operator token.

**Source comparison:** T §5.2; LQ §6.6. Capability plan §§2–3; T §11.5.1.

## O01 — One-dimensional analytical order

**Premises.** Day is a governed anchor with complete chronology and the family has its remaining complete contract.

**Expected judgment.** Precedence is trivial; the declared order supports the admitted finite FIRST/LAST construction.

**Do not.** Require a new generic tie policy or infer chronology from a lineage label alone.

**Review.** T's finite FIRST/LAST construction permits one-dimensional governed chronology, with trivial constituent precedence. The language requires the remaining family contract and does not add generic tie selection.

**Source comparison:** T §§7.1, 8; LQ §9.2. O3 §§2–4; supporting notes §1.1; Introduction §8.4.

## O02 — Compound precedence required

**Premises.** Customer and Day have complete point orders, but no precedence is supplied for the claimed global Customer-Day support.

**Expected judgment.** The compound order is not fully selected.

**Do not.** Infer precedence from output column order.

**Review.** Complete constituent orders without selected precedence do not specify the admitted global compound order. Output-coordinate listing order cannot complete it.

**Source comparison:** T §7.1; LQ §9.2. O3 §§2, 3.2; supporting notes §1.1.

## O03 — Missing constituent order

**Premises.** Precedence is supplied but Customer has no complete governed point order.

**Expected judgment.** The claimed complete compound order is unestablished.

**Do not.** Sort Customer IDs lexically as an implicit analytical order.

**Review.** Precedence alone cannot replace a missing constituent point order. A sortable identifier or physical collation does not establish the selected analytical order.

**Source comparison:** T §§7.1–7.3; LQ §9.2. O3 §§2, 4, 13; integration sheet §7.

## O04 — Sparse analytical point space

**Premises.** The governed support contains only (C1,d3),(C2,d1),(C2,d2).

**Expected judgment.** Only these points participate; order does not create (C2,d3) or another absent combination.

**Do not.** Fill the Cartesian product before LAST without an existence law.

**Review.** The injection from the actual anchor into its coordinate product is not a Cartesian-completeness assertion. Order compares the existing points and does not create the absent tuple.

**Source comparison:** T §§2.1.3, 7.1; LQ §9.2. O3 §§1, 5; Introduction §8.4.

## O05 — Form the support measure first

**Premises.** Several Product carrier records lie beneath one Account-Day point.

**Expected judgment.** Apply the operand formation law to establish its value at Account-Day before FIRST/LAST consumes that analytical point.

**Do not.** Select a raw row by day or invent SUM as the formation rule merely to collapse duplicates.

**Review.** The operand law establishes the value at the analytical input point before that point is consumed. Repeated carrier rows are neither tied analytical points nor permission to choose SUM. This formation rule does not demand every nonwinning value for the distinct partial-evidence arguments.

**Source comparison:** T §§3.1, 7.3; LQ §9.3. O3 §§4, 8–9; supporting notes §2.1; T §§9.2–9.6.

## O06 — Ordered family not automatic legacy conformance

**Premises.** FIRST/LAST has an admitted construction in T; a legacy .last spelling is accepted by a particular build.

**Expected judgment.** Analytical admission and that execution path’s conformance are separate claims.

**Do not.** Certify every existing .last because the theory now admits an ordered family.

**Review.** Theoretical FIRST/LAST admission is conditional on the complete construction. Existing syntax, a runtime category, and accepted legacy declarations are separate conformance facts, not proof of that construction.

**Source comparison:** T §§3.6, 4, 8; LQ §§9.1, 9.7, 13. Capability plan §§3, 7; Introduction §§8.4, 11; integration sheet §7.

## O07 — Original point witness through coarsening

**Premises.** For s1<s2<s3<s4, admitted intermediate groups are {s1,s4} and {s2,s3}, with coherent supported values.

**Expected judgment.** Retained winners s4 and s3 combine to s4 using the original support order.

**Do not.** Compare intermediate group labels or demand an unrelated new order on B.

**Review.** Both texts preserve the original S-point in intermediate witnesses. Arbitrary admitted intermediate grouping does not require an order on group labels; compatible contributions and admitted projections remain premises.

**Source comparison:** T §§8.3–8.4; LQ §9.5. O3 §7; T §8.4.

## O08 — Scalar is not witness continuation

**Premises.** An exact scalar LAST was materialized but its selected point is not retained or recoverable.

**Expected judgment.** The scalar target is available; further witness comparison is not licensed from it alone.

**Do not.** Set scalar re-entry true merely because LAST has family standing.

**Review.** A stored scalar answers its scalar claim but does not automatically retain the selected point. Family admission does not turn a scalar re-entry flag on, and re-entry insufficiency does not veto family standing.

**Source comparison:** T §§8.1, 10.7; LQ §§9.4, 10.6. Capability plan §3; O3 §12; Introduction §8.4.

## O09 — R is optional

**Premises.** An adequate argument establishes W; a full retained point–value set is unavailable.

**Expected judgment.** W can be used under its actual admitted contract; full R storage is not mandatory.

**Do not.** Impose R→W→L as a required runtime/storage pipeline.

**Review.** R is an optional sufficient basis. Adequate direct witness evidence may exist when R cannot be retained or fully established; the homomorphism is not a mandatory storage pipeline.

**Source comparison:** T §§8.6, 9.2; LQ §9.4. O3 §§8–9; Introduction §8.4.

## O10 — Same results, different laws

**Premises.** Two different declared precedence orders currently yield the same winner.

**Expected judgment.** Numerical agreement does not merge their analytical identities.

**Do not.** Infer equivalent family identity from observed equality.

**Review.** Observed winner equality does not constitute equivalence of different order laws. Equivalence must be established over the relevant declared scope; identity-neutral physical serialization changes remain possible.

**Source comparison:** T §§2.2, 7.2; LQ §§9.2, 10.1. O3 §§5–6; supporting notes §1.2.

## O11 — Frame selection can coincide with LAST

**Premises.** A versioned output ORDER BY/LIMIT PER query selects a row whose value equals a LAST answer.

**Expected judgment.** Frame selection remains legitimate in its own scope; no inner family identity or reusable witness follows.

**Do not.** Either ban the frame operation or use it as ambient order/family proof.

**Review.** Frame ORDER BY/LIMIT PER remains legitimate output selection. It neither becomes a forbidden operation because it resembles LAST nor supplies an inner ordered family, witness, or implicit order contract.

**Source comparison:** T §12.4; LQ §9.7. Supporting notes §2.4; O3 §§11, 14; integration sheet §8.

## C01 — Contextual formation can precede a family

**Premises.** The law fixes daily predecessor formation over 100,110,95,105 and a separately admitted additive family over the changes.

**Expected judgment.** Established changes 10,-15,10 sum to 5 coherently.

**Do not.** Exclude the family solely because formation used neighboring points.

**Review.** The original predecessor context forms the three changes. The separately admitted additive family can continue over them. Contextual formation is not rejected merely because it used another point.

**Source comparison:** T §§3.3–3.4; LQ §6.10. Supporting notes §2.3; Introduction §8.4.

## C02 — Restriction must preserve formation

**Premises.** The same change family is requested after grouping the source into pairs.

**Expected judgment.** Reusing original changes differs from restarting predecessor formation inside the pairs, which gives 20.

**Do not.** Push a restriction/grouping through formation without an equivalence justification.

**Review.** Restarting predecessor formation in subgroups loses a boundary contribution and changes the construction. LQ locates WHERE in its declared formation scope instead of licensing arbitrary predicate pushdown.

**Source comparison:** T §§3.3, 10.2; LQ §§2.4, 6.10. Supporting notes §§2.3–2.4; Introduction §6.4; integration sheet §8.

## C03 — Faithful recomputation is not forbidden

**Premises.** The original contextual formation and its full governing context can be reproduced from adequate evidence.

**Expected judgment.** Recomputation can establish the same constitutive values; caching is not required by the theory.

**Do not.** Interpret “do not change formation” as “never recompute.”

**Review.** A faithful reconstruction of the same constitutive values and context remains allowed. Neither theory nor companion text converts formation preservation into a requirement to cache rather than recompute.

**Source comparison:** T §§3.3–3.4; LQ §6.10. Supporting notes §2.3; integration sheet §8.

## C04 — Focal window law needs its own contract

**Premises.** A rolling expression is written without specifying positional versus time-range neighborhood and material endpoint conventions.

**Expected judgment.** The expression’s meaning remains incomplete where these choices change the result.

**Do not.** Treat complete order alone as a full window specification or automatically admit family continuation.

**Review.** The order relation alone does not fix a contextual window. Positional/range choice, participation, and meaningful boundary conventions require the particular expression contract; family continuation remains separately admitted.

**Source comparison:** T §§3.4, 11.4; LQ §9.6. Supporting notes §2.2; O3 §13; capability plan §4.

## E01 — Established output, unplaced source

**Premises.** A Day output point exists and Revenue is eligible, but required known source contributions cannot be placed by Day.

**Expected judgment.** The target value may be unsupported; the upstream placement cause remains distinct.

**Do not.** Declare the output point nonexistent or forbid target missingness solely because a source placement is unresolved.

**Review.** The subject of the failed placement claim is the source point. The target point may already exist and be eligible but have an unsupported value. R4 no longer makes all source placements a precondition for describing target missingness.

**Source comparison:** T §§2.3, 9.1–9.4; LQ §§8.1–8.4. Supporting notes §3.1; O3 §9; integration sheet §9.

## E02 — Known domain with incomplete operand support

**Premises.** Governance establishes exactly 100 participating transactions, with 99 supported Revenue observations.

**Expected judgment.** Point count is 100; a count under a declared supported-operand participation law may be 99. A mean over all 100 cannot silently shrink.

**Do not.** Infer intended population from surviving ordinary rows.

**Review.** T §11.5.1, LQ §8.5, and this case correctly make 99 depend on a declared supported-observation participation rule. LQ §6.3's separate 97-observation example should state that same premise locally; correction J1 supplies it without changing the count forms or law.

**Source comparison:** T §§2.3, 4.2, 11.5.1; LQ §8.5. Supporting notes §3.2; correction J1.

## E03 — Coarser witness, unavailable staged input

**Premises.** Participation s1<s2<s3 and intermediate blocks {s1},{s2,s3} are known; f(s1) unavailable, f(s2)=20 and f(s3)=30 supported.

**Expected judgment.** Coarser W=(s3,30) is established by maximality evidence even though a plan consuming both exact intermediate witnesses lacks an input.

**Do not.** Replace unavailable intermediate W with known-empty identity, or infer target impossibility from this plan’s failure.

**Review.** Participation and intermediate-block membership are known; the unavailable item is the first witness value. The coarser witness follows from maximality evidence, not from substituting empty state or pretending the blocked staged plan ran.

**Source comparison:** T §§6.1, 9.5; LQ §8.7. Supporting notes §3.3; O3 §9.

## E04 — Scalar without winner identity

**Premises.** Fixed LAST law; p<q; p definitely participates; q participation unresolved; p,q exhaust possible participants; both operand values supported as 7.

**Expected judgment.** Nonempty scalar L=7 is established; selected-point W is not.

**Do not.** Claim W, choose an arbitrary observed 7 without the exhaustive evidence, or treat W as necessary for every L proof.

**Review.** The scalar-only argument retains its fixed law, known nonemptiness, exhaustive possible-participant account, and supported equality at every possible winner. It establishes L, not a selected W, and is not a general constant-fill procedure.

**Source comparison:** T §9.6; LQ §8.8. Supporting notes §3.3; O3 §9; Introduction §8.4; T §10.7.

## E05 — Missing selected operand

**Premises.** Participation and order identify the latest eligible point, whose operand value is unsupported.

**Expected judgment.** Ordinary LAST value is unsupported unless another adequate argument establishes the same target.

**Do not.** Return an earlier supported value by silent support-skipping.

**Review.** Ordinary LAST of the participating points does not silently become LAST of supported values. Any alternative adequate argument must establish the same target rather than change participation.

**Source comparison:** T §§9.2–9.3; LQ §8.6. Supporting notes §2.2; O3 §§9, 14.

## E06 — Known empty is not unknown

**Premises.** An intermediate contribution set is unknown, or the selected value is unsupported.

**Expected judgment.** No algebraic unit can stand for that unknown evidence without a separate admitted argument.

**Do not.** Coerce carrier NULL or unknown support to bottom/zero/empty set.

**Review.** The empty unit describes known-empty contribution where admitted. Unavailable value, unestablished placement, and unknown participation are not identities. The inherited MIN/MAX semigroup case introduces no synthetic null.

**Source comparison:** T §§5.2, 6.1.1, 8.2, 9; LQ §8.9. Supporting notes §3.3; O3 §§8–9; integration sheet §9.

## E07 — Late filtering cannot undo ordered influence

**Premises.** An unplaceable contribution affects cumulative/lag output, then its own row is withheld.

**Expected judgment.** The resulting computation has not been repaired by the late withholding.

**Do not.** Report ordinary established results merely because no NULL-coordinate row remains.

**Review.** Removing the unplaced row after an ordered walk does not undo its effect on surviving outputs. Disclosure alone cannot establish the original target; a restricted result needs its own explicit claim and conditions.

**Source comparison:** T §9.4; LQ §8.10. Supporting notes §3.4; O3 §9; integration sheet §9; capability plan §7.

## R01 — Lossy compression can hide contradiction

**Premises.** With p<q, one alleged coherent input has (p,10),(q,20); another has (p,11).

**Expected judgment.** Their coherent-instance premise is violated; compressed winner comparison cannot validate it.

**Do not.** Treat equal-point conflict checks or a common context label as a global consistency certificate.

**Review.** The contradictory nonwinning claim can disappear before local winner comparison. T and all technical companions require adequate compatibility evidence outside the lossy combine; a matching context label alone is not that evidence.

**Source comparison:** T §10.6; LQ §10.7. Supporting notes §5; O3 §§8, 12.

## R02 — Three materialization claims

**Premises.** A catalog holds W, scalar L projected from discarded W, or scalar L established without identifying its winner.

**Expected judgment.** Record retained content, established claim and justification, and permitted reuse; the scalar rows need not have different family identities.

**Do not.** Collapse all entries into “LAST available” or create family identity by proof method.

**Review.** All three materialization situations remain distinguished. W can supply L on the nonempty constructor domain. Scalar proof histories do not create new family identities and do not imply W is retained or recoverable.

**Source comparison:** T §10.7; LQ §10.6. O3 §12; Introduction §8.4; capability plan §2.

## R03 — Equal mean display, unequal continuation

**Premises.** Exact states (10,1) and (1000,100) both display 10; both are extended by (20,1).

**Expected judgment.** The results become 15 and 1020/101; scalar equality did not preserve continuation information.

**Do not.** Merge or substitute displayed means as adequate state.

**Review.** Equal present scalar means do not determine weights for later extension. Continuation-state substitution requires the next operation's adequate information and compatible premises, not merely equal displays.

**Source comparison:** T §10.5; LQ §6.6. Supporting notes §5; Primer, “The Result Can Be the Query”.

## R04 — Restriction or deletion of winner

**Premises.** Only the compressed maximal witness is retained, and the next request excludes or deletes that point.

**Expected judgment.** A new adequate derivation or richer retained information is required to identify its replacement.

**Do not.** Infer arbitrary filtering/deletion capability from witness coarsening capability.

**Review.** Extremum state sufficient for admitted coarsening can lose the replacement winner needed after deletion or restriction. A richer input or adequate new argument may be necessary; stored availability alone does not grant it.

**Source comparison:** T §§10.2–10.3; LQ §10.8. O3 §12; supporting notes §5.

## R05 — Approximate realization of unchanged target

**Premises.** An explicit approximation contract supports an HLL estimate of exact count distinct.

**Expected judgment.** It may target the same family while remaining an approximate realization, not an exact sufficient-state basis.

**Do not.** Invent a new target solely from error grade, or silently reuse the estimate as exact state.

**Review.** An approximate realization can target the same analytical family, but does not become exact sufficient state. Both source and companion texts preserve the error/realization boundary and forbid approximation as an excuse for unestablished meaning.

**Source comparison:** T §10.9; LQ §§6.9, 10.8. Capability plan §4; supporting notes §5.

## G01 — EXPLAIN does not observe unperformed checks

**Premises.** EXPLAIN resolves meaning and a proposed plan without data execution or applicable evidence for all runtime conditions.

**Expected judgment.** It distinguishes what is established from checks outstanding.

**Do not.** Guarantee all future disclosures or complete data support from a data-free explanation.

**Review.** EXPLAIN can expose resolved meaning, plans, and applicable assurance, not evidence of every unperformed data check. The same semantic request must reach execution; disclosure completeness is not promised without applicable evidence.

**Source comparison:** T §§9.1, 12.3–12.4; LQ §10.3. O3 §11; Introduction §7; integration sheet §4.

## G02 — Family law versus engine kind

**Premises.** An operator belongs to a runtime category or a canonical capability list.

**Expected judgment.** Family admission still needs the complete target/law contract; category does not confer authority.

**Do not.** Grant family founding solely from an anchor-changing kind.

**Review.** The complete analytical family law, language meaning, profile obligation, runtime category, and materialized capability remain different questions. No fourth-cell or reducer-kind shortcut confers family founding.

**Source comparison:** T §3.6; LQ §13. Capability plan §§2–3; supporting notes §1.3.

## G03 — No syntax from theory alone

**Premises.** The theory admits tuples, witnesses, order definitions or a family construction not exposed by a shipped grammar/profile.

**Expected judgment.** Semantic admission and language/implementation availability remain separate.

**Do not.** Advertise theoretical notation as accepted syntax or edit measured build status to imply support.

**Review.** Theory notation and working semantic admission are not accepted syntax or build conformance. The intros preserve their examples and versioned release boundary without reporting new execution.

**Source comparison:** T §§12–13; LQ §§1, 13. Introduction §§11–12; Primer scope paragraphs; capability plan §5; authority index §§2, 5.

## G04 — CDT interface remains unverified

**Premises.** This pass specifies required comparison and representation behavior but does not inspect CDT v0.5.

**Expected judgment.** Readiness is unverified; a new nominal Witness type is neither asserted absent nor mandated.

**Do not.** Claim present API support/absence from the theory manuscript.

**Review.** The actual CDT API has not been verified in this set. Requirements are explicit, but neither absence of a nominal Witness type nor presence of a usable implementation is inferred. Interface verification is a separate gate.

**Source comparison:** T §§8.5, 12.2, 13.3; LQ §9.5. O3 §§0, 4, 16; capability plan §§4–5.

## G05 — Historical instructions are not active authority

**Premises.** An earlier O1/O2/M2/CP document says FIRST/LAST cannot found families or universal formation locality is required.

**Expected judgment.** Use the explicit current supersession index and reconciled language target; preserve historical observations at their own snapshots.

**Do not.** Execute an old “settled” instruction because its filename or prior PASS sounds authoritative.

**Review.** The active index explicitly supersedes the categorical ordered-family and universal formation-locality rules in old notes and handoffs. Historical reports remain evidence at their snapshots, not new implementation instructions.

**Source comparison:** T Appendix C.4; LQ §§15–16. Authority index §§3–6; integration sheet §12; reconciliation register §6.
