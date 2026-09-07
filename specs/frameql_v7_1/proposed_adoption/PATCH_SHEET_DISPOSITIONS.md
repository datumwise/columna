# Reference integration patch sheet — recorded dispositions

**Ruled 7 September 2026.** Recorded here so the sheet cannot later be applied wholesale, and so a
withheld item cannot be mistaken for a rejected one.

**Two proposals are authorized and applied in this pass. Nine are not applied.** The sheet itself
remains archived, unedited, at `../reviewed_sources/frameql_v7_1_reference_integration_patch_sheet_v0_1.md`.

**Withholding an edit does not certify the existing wording as correct.** EXPLAIN (§4) and the other
contract questions below remain **open**. What is settled is only that they are not editorial acts and
are not resolved by this pass.

| § | subject | disposition | why |
|---|---|---|---|
| 2 | opening authority notice | **not applied** | would install, in the shipped reference, an authority relation to a v7.1 candidate that is not a published edition; also reintroduces release-scoped wording into a document deliberately kept build-independent. Collides with the language law's own §2.9 |
| **3** | **alias / output key** | **APPLIED, reduced** | adopted as an output-key clarification only. The sentence importing admitted-law / publication-or-ratification vocabulary was **dropped**; no family-admission language enters the reference. All existing alias syntax, scope, visibility, collision and error behaviour is unchanged |
| 4 | EXPLAIN | **not applied — question remains OPEN** | widens a stated release guarantee ("modulo certificate changes") to any premise failure. That is a contract change requiring a ruling, not an editorial edit. Its adoption condition also names a parser/render round-trip guarantee that the reference does not contain |
| 5 | canonical target vs execution decomposition | **not applied — question remains OPEN** | would withdraw a standing argument the reference currently asserts (§2.1). Withdrawing standing from canonical language law is a ruling |
| 6 | default completion / input anchor | **not applied** | the reference already states the equivalence-law rule and already retires the older formulation the proposal targets. No-op as written |
| 7 | family / FIRST-LAST / ordered operations | **not applied — no suitable exact replacement destination as written** | **Correction to the earlier staging report, which overstated this.** The subject is *not* absent from non-generated prose: §2.2 carries family-variant prose explicitly, including `level.last` and `SELECT level.last AT {store}`, and distinguishes a family variant from a `member`. What is true is narrower — the proposal supplies no exact destination that matches the current headings, and the only *enumeration* of `first`/`last` sits inside a machine-generated capability block, which is not hand-editable. A future version of this proposal needs a destination and replacement text pinned to §2.2 |
| 8 | WHERE / HAVING / frame selection | **not applied — question remains OPEN** | the WHERE/HAVING distinction is already stated (§4.2). The genuinely new content — a prohibition on silently re-forming a constituted contextual quantity, and a pushdown-licensing rule — are semantic rulings, and the pushdown sentence would sit awkwardly against what build status records |
| 9 | Φ / NULL / support | **not applied** | the reference already refuses the conflation (§1.5, §7.5). The proposal's enumeration of six distinct judgments is the existence / placement / eligibility / support architecture that the consolidated ledger records as **not built and not authorized**; stating them as judgments the release makes would present an unbuilt obligation as shipped ontology |
| 10 | bracket roadmap withdrawal | **not applied — question remains OPEN** | retiring a roadmap construct is a ruling with a required tombstone idiom, not an editorial withdrawal; it also moves a documentation-gate census, and `E[key]` has no capability id to hang a working semantic role on |
| **11** | **profile / generated-table authority notice** | **APPLIED, outside the generated block** | adopted into the **authored** prose above `BEGIN GENERATED`, never inside it. The family-continuation sentence was **dropped** — it is successor family-contract language. No generated row was touched |
| 12 | adoption checklist | n/a | not a wording proposal. Two items verified holding: generated tables remain generated (0 drift), and no DOI is invented |

## Applied text, exactly

**§3 — `docs/frame_ql_language.md` §1.6.** One word changed in the existing sentence (*identity* →
*output key*), and one clarifying paragraph added:

> An alias supplies an output column key and follows the visibility and collision rules below. It does
> not establish analytical family identity, and changing the output key does not change the
> already-resolved analytical quantity.

**§11 — `docs/frame_ql_language.md`, authored prose immediately above `<!-- BEGIN GENERATED -->`.**

> These entries record distinct authorities, identified by their columns and source files: canonical
> standing is language law, a profile states an authored obligation, and build status reports measured
> coverage. Callable availability is not full analytical-law conformance. No theoretical revision
> silently changes operator standing, profile promises, or measured release coverage.

The profile documents already carry the equivalent statement in their own authored prose, so §11 was
not duplicated into them.
