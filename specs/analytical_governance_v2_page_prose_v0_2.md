# /analytical-governance — proposed current-page prose (v2.0 doorway)

**For review before any reader-facing change. Status: NOT IMPLEMENTED.** No file under
`apps/website/src/` has been touched. This supersedes the structural draft
`analytical_governance_v2_page_draft_v0_1.md`, which stays as the record of the findings that
produced it.

Authored **fresh from Analytical Governance v2.0** (`w-analytical-governance.r03`, as retrieved and
byte-verified), not by editing the v1.1 compression into place — per ruling E.5. Every proposition,
definition and quoted line below traces to a section of that record; the section is named beside it.
Where the page speaks in its own voice, it is marked *page voice* and claims nothing the record does
not carry.

Rulings applied: **E.1** label · **E.2** ToC referenced, never absorbed; no domain triad asserted ·
**E.3** v1.1 body preserved, not rewritten · **E.4** order as ruled, Standing after the responses ·
**E.5** fresh authorship.

---

## The page at a glance

| § | section | ruled item |
|---|---|---|
| 1 | Analytics is a service relationship — hero, the wound, the six words | 1 |
| 2 | Legitimacy — what must remain true | 2 |
| 3 | The intent gap — fidelity and enablement | 3 |
| 4 | The servability gap | 4 |
| 5 | Governance responses — Serve · Disclose · Clarify · Refuse, and Escalate | 5 |
| 6 | Standing — what the answer may carry forward | 6 |
| 7 | Serving and authoring — where the constitution comes from | 7 |
| 8 | Governed crossings — and where this sits | 8 |
| 9 | Conformance — requirements, non-claims, and one quotation from the wire | 9 |

Nine movements, one WIRE quotation near the end, PAPER everywhere else. Shorter than the current
page: the matrix, the three powers and the ticket/visa compression are gone (E.4), and the sections
that remain are re-cut rather than re-worded.

---

## §1 · Analytics is a service relationship

### 1a · Hero

> **Analytical Governance**
>
> # A correct number can still fail the service.
>
> Analytical Governance is the discipline governing the **legitimacy of the analytical service**: the
> user's purpose must survive the passage from expressed intent to an answer, the result must be
> established under the analytical law and support that apply, and the answer must carry no more
> authority than its grounds warrant.

Then, in the band the conformance test occupies today — quiet, full width, labelled as the criterion
it is, above the publication signpost:

> **Conformance test**
> A conforming analytical service must be able to **withhold or qualify analytical permission**.
> Refusal is not an error state. It is the evidence that the permission is real.

Then the signpost, every field registry-derived:

> *[deposited title of the current record]* — Huayin Wang · Version *[n]* · *[date]* · DOI *[doi]*
> The category paper. This page is a doorway; the deposit governs.

*Traces:* §Abstract (the legitimacy definition, near-verbatim); §1 ("the arithmetic may be flawless
and the service unfaithful" — the H1 is the page's compression of that sentence, and is *page
voice*); §12 first requirement and §5 Refuse (the criterion band).

*Retired here, both v1.1-only and both preserved on the historical route:* "What can be computed is
not yet what may be served" as the page thesis — it returns in §4 as the record's own
"Computability does not imply servability" — and "If it cannot refuse, it is not governed" (E.3).

### 1b · The wound

> ## A number the database can compute but the service cannot yet serve
>
> ### What was average revenue per open store yesterday?
>
> | the system has | which establishes | from |
> |---|---|---|
> | 47 revenue rows | what **reported** — not what was open | the sales table |
> | 50 stores | the **roster** — not that 50 were open | the store roster |
> | 48 open yesterday | the **requested population** | the operating-status source |
>
> The arithmetic can divide total observed revenue by 47, by 48, or by 50. All three are executable.
> All three return a plausible number. **The computation does not tell us which answer serves the
> user's purpose.**
>
> The 50-store roster does not establish that all 50 were open. The 47 revenue rows do not establish
> the open-store population. A system that returns the mean over reporting stores while presenting it
> as *average revenue per open store* can be arithmetically flawless and unfaithful as a service —
> and a system that identifies the right population but uses stale or incomplete state can be
> faithful in interpretation and unreliable in production.

Then the disposition, stated rather than implied — and deliberately *without* the serving vocabulary,
which is typed in §5:

> No number is entitled to answer this question yet, and the reason is not arithmetic. The population
> has to be established, the required state has to be shown to be present for those points, and only
> then is there a question about what may be served. **Establishing the population and establishing a
> servable answer are two different things.**

*Traces:* §1 in full; the "faithful interpretation, unreliable production" pair is §1's own third
sentence; the closing distinction is §10's "Reliable production and support" step compressed.

*Note for implementation:* this replaces `OpenStoreWound.astro` rather than editing it. The v1.1
component's numbers (50 open store-days, 2 governed zero-revenue days, 1 feed failure, denominators
47/49/50) belong to the v1.1 record and stay on the historical route unchanged.

### 1c · The six words this page uses precisely

A definition strip, six lines, no commentary — the paper's own glossary, which the current page has
no equivalent of and which does more for a serious reader than any diagram:

> **Request** — the governed analytical formulation of the user's purpose.
> **Result** — the product of the governed analytical process.
> **Answer** — a result served as responsive to the request.
> **Servability** — whether the result has the analytical permission required to be served as that answer.
> **Standing** — what the result or answer may be treated as, or relied upon for, at a boundary.
> **Constitution** — the ratified governed world of analytical meaning, law, support rules, and authority against which serving is adjudicated.

*Traces:* the definition block between §Abstract and §1, verbatim.

---

## §2 · Legitimacy — what must remain true

> ## What must remain true
>
> User purpose → analytical intent → governed analytical construction → reliable production →
> servability → warranted reliance → consequential use

> This is an operational cut through the analytical service, not a replacement taxonomy for the
> foundational domains whose laws the service uses. Different systems may combine functions.
> Governance requires that the distinctions remain visible enough to adjudicate.

Three obligations, one short paragraph each — set as three units, not as three cards:

> **Faithfulness** — does the service preserve the user's purpose as it becomes a request and an
> answer? Two duties, and only one of them is translation. *Fidelity* prevents the system from saying
> something different from what the user means. *Enablement* helps the user say more precisely what
> they are trying to know. **Neither authorises the system to choose silently on the user's behalf.**
>
> **Reliability** — can the governed process produce the established result consistently under the
> relevant conditions? Data availability, state, execution, materialisation, reproducibility.
> Reliability does not create analytical meaning: *a reliable production path must reproduce and carry
> forward the object that was actually established.*
>
> **Certainty sufficient for reliance** — are the grounds relevant to this result established,
> preserved and respected as the service crosses from request to answer, and from answer to use?

Then ToC, once, as the external foundation — one paragraph, one link, no absorption (E.2):

> Analytical Governance does not develop its own account of what makes grounds sufficient. That
> upstream discipline — what grounds carry a conclusion, what they establish, where their warrant
> stops, and whether they can bear the reliance being placed on them — is developed separately in
> **The Theory of Certainty**, and Analytical Governance turns those questions into a governed
> analytical service.
> → *[current publication record of The Theory of Certainty, registry-derived]*

*Traces:* §2, §2.1, §2.2, §2.3, §Abstract's ToC paragraph, §13's ToC sentence.

*Deliberately absent:* the three grounds, the substitution error, reach, composition, exposure.
Those are ToC's, and a doorway that summarised them would absorb the theory it is pointing at. No
triad of domains is named, drawn, or implied anywhere on the page (E.2).

---

## §3 · The intent gap — fidelity and enablement

> ## The intent gap
>
> ### From purpose to governed request

> The first gap is the distance between what a user can initially express and the analytical request
> that faithfully captures their purpose with the distinctions governance needs. Closing it has two
> obligations: preserve the purpose, and enable better articulation.

> AI and semantic systems can search vocabulary, retrieve definitions, expose governed distinctions,
> propose interpretations, explain alternatives, and formulate a candidate governed request. **This is
> not merely translation.** A good analytical service can expand what the user is able to say, by
> making the relevant distinctions available to be said.

The worked case, which is the shortest proof of the distinction on the page:

> A user asks for "average revenue." The service can surface the governed alternatives — among
> reporting stores, among existing stores, among stores that were open — explain the difference, and
> let the user choose. **That is enablement. Silently selecting one of them is unauthorized
> formulation by the serving system.**

And the guard the v1.1 page has no equivalent of:

> Enablement must not conceal materially relevant governed alternatives. If the service surfaces a
> selective set rather than the relevant governed set, **that selectivity must itself be governed or
> disclosed.**

Closing line:

> The intent gap is closed when the user's purpose has been formulated — through preservation and,
> where useful, enablement — as an analytical request **explicit enough for independent
> adjudication**.

*Traces:* §3 throughout, near-verbatim.

---

## §4 · The servability gap

> ## The servability gap
>
> ### From governed request to answer

Two propositions carry the section:

> **Faithful request does not imply servable request.**
>
> **Servable = Support Sufficient AND Analytically Established**

> **Analytical establishment** asks whether the requested analytical object exists under the governed
> analytical model and whether the requested derivation is lawful. **Support sufficiency** asks
> whether the evidence and sufficient state this particular request requires are presently available.

Three failures, one line each — the page's densest useful paragraph:

> A missing feed can leave a lawful request unsupported. An unlawful reduction can leave abundant
> data unable to establish the requested result. An unresolved population can make a computable
> denominator analytically unestablished.

Then the sentence that used to be the hero, in its own edition's words, followed by the two that stop
the gate being read as a property of a platform:

> **Computability does not imply servability.**
>
> Servability is not a generic property of a dataset, metric, model, or platform. It is a
> determination about a particular analytical request under current grounds.
>
> A result may be servable and still not be served. Servability establishes the analytical permission
> for the requested answer; authorisation, risk and disclosure conditions determine the serving
> outcome.

One short paragraph on time, because it is the case every practitioner will bring and v2.0 answers it
directly:

> A late-arriving or retroactively corrected record does not necessarily change the identity of the
> analytical object; it may instead change whether the required state was support-sufficient when the
> answer was served. If the governed definition itself is versioned over time, analytical identity
> may change too.

*Traces:* §4 throughout.

---

## §5 · Governance responses

Layout as today — four moods in one row as the serving vocabulary, a hard rule, Escalate beneath it
and outside the row. Text re-cut to v2.0 §5:

> ## Governance responses
>
> ### The serving vocabulary — what a governed system returns at the machine boundary
>
> **Serve** — the request is determinate, the required analytical and support grounds are established,
> the result is authorised for the intended use, and no material condition requires separate
> disclosure.
> **Disclose** — the result may be served, but a material condition must travel with it. Disclosure
> preserves the boundary of the warrant.
> **Clarify** — the missing distinction is inside the existing governed world and the requester can
> resolve it. Clarification protects faithfulness to purpose; it does not create new analytical
> authority.
> **Refuse** — the requested answer cannot be served under current analytical, support, risk or
> authorisation conditions. **Refusal is evidence that analytical permission is real.**
>
> ### The governance-process outcome — across the system boundary
>
> **Escalate** — faithful service requires something the current governed world does not possess: new
> meaning, new evidence, new authority, or qualified review. **It is not a fifth serving mood.** The
> request leaves the serving path and enters an authoring, declaration, review or ratification
> process capable of changing the governed world.
>
> Escalation returns either a ratified change or a decision not to change. Until that return path
> completes, serving remains unresolved: **escalation does not produce an unofficial answer.**

Kept, because it is the one place the page can be misread into a response enum:

> The full governance process therefore produces **five externally meaningful outcomes**. The machine
> serving vocabulary has **four**. Those are two counts of two different things, and collapsing them
> is how a governance boundary quietly becomes a response enum.

*Traces:* §5 for all five; the count note is *page voice* and survives from the v1.1 page unchanged,
because v2.0 states both halves of it (§5 Escalate; §11's account of what is governed).

---

## §6 · Standing — what the answer may carry forward

Placed after the responses, as ruled: standing is downstream of the serving verdict.

> ## Standing
>
> Servability asks whether a candidate result may be served as the answer. Consequential use creates a
> further question: **what may the served result now be treated as?**

> Standing is claim- and boundary-specific. A result may stand for exploratory display and not for
> compensation. A statistical estimate may stand as an estimate and not as a causal claim. A result
> may require disclosure before publication.
>
> **Standing prevents a result from becoming more authoritative merely because it travelled.
> Conclusions are portable; their grounds are less so.**

Then risk and authority, as the same boundary seen from the other side — one movement, not a section:

> Cost, security, application risk and authorisation can constrain an otherwise established analytical
> service. They cannot supply a missing analytical ground. **Risk may constrain the right answer. It
> cannot turn an unestablished answer into the right one.**
>
> An unresolved analytical identity, an unsupported population, or an unlawful derivation is not a
> higher-risk version of the requested answer. Once the object and its required support are
> established, exposure matters: the same result may be acceptable for exploration and unacceptable
> for compensation, publication, or automated action.

*Traces:* §7 and §8.

---

## §7 · Serving and authoring — where the constitution comes from

> ## The governed world is authored, not assumed
>
> Analytical service operates against a governed **constitution**: analytical meaning, law, support
> requirements, authority. That constitution must be declared, reviewed and ratified through a process
> **separate from serving**.
>
> **Serving applies the current constitution. Authoring changes or extends it**, through an authority
> event that can be reviewed and ratified.
>
> **A serving system must not silently create the missing meaning or authority that would make its own
> answer servable.**
>
> unresolved need → authoring or declaration → review and ratification → governed constitution →
> serving
>
> **Clarify stays inside the constitution. Escalate reaches the constitution's edge.**

*Traces:* §6 throughout, plus §5's Escalate for the closing pair.

*Page voice, and worth saying out loud in the draft:* this section is where the site's own Authoring
work will eventually attach. The page must not imply that datumwise ships an authoring process — it
states the requirement that one exist and be separate. No forward reference, no roadmap language.

---

## §8 · Governed crossings

> ## Govern the crossings
>
> Analytical service becomes consequential at crossings: purpose becomes a request, a request becomes
> a plan, a plan produces a result, a result becomes an answer, and an answer becomes action. Each
> crossing is an opportunity for authority to travel farther than its grounds.
>
> **The component that can produce a candidate result need not be the component entitled to authorize
> what that result becomes.**

> AI agents are **one application** of this crossing discipline. A model may interpret language,
> formulate a candidate governed request, generate candidate SQL, summarise evidence, or explain an
> adjudication result. None of those capabilities requires the model itself to carry analytical
> authority.
>
> A structural execution boundary can close one consequential path independently of predictions about
> the agent. This is the role of a **blast wall**: a structural boundary that prevents reasoning output
> from becoming consequential execution directly. The same principle applies to serving — the agent
> may propose or explain; the governed serving boundary determines what the result is entitled to
> become.

Then *where this sits*, shortened, still a relation list rather than a symmetric diagram (these
bodies of law have different shapes, and a four-box figure would claim a symmetry the corpus does not
have):

> **Data governance** — *composes with.* Data governance governs stewardship, access, quality and
> control of data assets. Analytical Governance governs whether the analytical service is faithfully
> formulated, sufficiently established, honestly served and appropriately used. The two compose;
> neither substitutes for the other.
> **The Theory of Data** — *supplies interior law to.* Laws of governed analytical identity,
> derivability and consistency.
> **The Statistical Bridge** — *governs a crossing inside.* Passages from governed evidence through
> formal inference to licensed claims. Analytical Governance may compose that crossing into a larger
> path; it does not replace the Bridge's law and does not adjudicate inference itself.
> **The Theory of Certainty** — *supplies the upstream discipline to.* Grounds of certainty, their
> reach, their composition, and sufficiency for reliance.
> **Columna** — *is an executable consequence of.* Evidence that these distinctions can be embodied
> in a working system. Not the definition of the category, which does not depend on it.
> **Frame-QL** — *is one request language for.* Convenient because it speaks natively in governed
> analytical objects. No language or protocol is required by the category.

> Analytical Governance **coordinates these kinds of interior law without replacing them.** It governs
> the analytical service passage: what must remain true as purpose becomes request, request becomes
> result, result becomes answer, and answer becomes consequential use. Its subject includes process
> and practice as well as architecture — how analysts, data systems, semantic systems, AI agents,
> reviewers and execution controls preserve analytical meaning and authority across handoffs.

*Traces:* §9 for the crossings and the blast wall; §11 for the relations, the data-governance pairing
and the coordination sentence. The ToC row is the second and last appearance of ToC on the page.

---

## §9 · Conformance

> ## Conformance
>
> A conforming analytical-governance practice or architecture needs, at minimum:
>
> - a way to preserve user purpose while translating human or machine intent into an explicit
>   analytical request;
> - a governed analytical representation capable of independently establishing identity, derivation,
>   support requirements and relevant state;
> - a reliable production path that preserves what was analytically established;
> - **a servability gate capable of withholding or qualifying analytical permission;**
> - a way to preserve standing, conditions, reasons and alternatives as results cross boundaries;
> - separation between analytical establishment and later cost, security, application and
>   authorisation decisions;
> - execution faithful to what governance actually authorised.

> **The non-claims, which are what keep this a category and not a product pitch.** This framework does
> not guarantee perfect intent, perfect data, perfect governed declarations, or perfect decisions. It
> does not replace semantic knowledge, statistical inference, security engineering, physical
> optimisation, or decision governance. It requires no particular query language, semantic layer, or
> implementation architecture. It requires that the analytical target, the grounds relevant to serving
> it, and the authority for consequential use be **independently adjudicable somewhere** before the
> service crosses the relevant boundary.

Then the WIRE quotation, mechanism unchanged — generated from the shipped package on the deploy path,
with the build-time assertions kept (the four serving moods present; `escalate` absent because it is
not a serving verdict; the build fails rather than the page continuing to claim it). Its prose is
re-cut to the v2.0 frame:

> **Product consequence.** A category no system has embodied is a proposal. The distinction this page
> turns on is testable in one place: what a governed engine is actually willing to return.

And the closing path, from §13:

> Preserve purpose. Establish the analytical object and its grounds. Produce it reliably. Serve only
> what is servable. Preserve standing across crossings. Govern consequential use.
>
> The goal is not to formalise every analytical act. It is to ensure that when analytics serves a
> user, the answer remains faithful to the purpose that called for it and carries no more authority
> than it has earned.

Then the two paths out, as now: *read the paper* (registry-derived) and *see the executable
consequence* (`/columna`).

*Traces:* §12 and §13.

---

## Implementation plan, for approval with the prose

**New components** (`src/components/ag2/`, so the v1.1 set stays untouched for the historical route):
`Ag2Hero`, `ServiceWound`, `TermStrip`, `MustRemainTrue`, `IntentGap`, `ServabilityGap`,
`GovernanceResponses` (the four + Escalate; adapted from `ServingBoundary`, which is already the right
shape), `StandingSection`, `ServingAndAuthoring`, `Crossings` (absorbing the relation list),
`Conformance2`. `WireQuotation` is **reused as-is** — its assertions are about the shipped package,
not about the edition.

**Retired from the current route, preserved on the historical one:** `AgHero`, `OpenStoreWound`,
`TwoGaps`, `CanMayMatrix`, the three-powers section, both v1.1 conformance blockquotes, the
ticket/visa compression.

**Anchors.** New: `#service`, `#the-wound`, `#terms`, `#must-remain-true`, `#intent-gap`,
`#servability`, `#responses`, `#standing`, `#authoring`, `#crossings`, `#conformance`, `#wire`,
`#path`. Live anchors today are `#the-wound`, `#two-gaps`, `#can-may`, `#powers`, `#serving`,
`#conformance`, `#boundaries`, `#wire`, `#authorize`. `#the-wound`, `#conformance` and `#wire` keep
their addresses; `#serving` → `#responses`, `#boundaries` → `#crossings`, `#authorize` → `#path` as
in-page shims; **`#two-gaps`, `#can-may` and `#powers` have no successor** and forward to the same
anchor on the historical route, exactly as the eight legacy `/research` fragments do.

**Derivation rules, unchanged and gated.** No title, version, date or DOI typed anywhere — AG and ToC
both through `citation(workId)`; `check_publications.py` keeps this route `derived` (G7) and fails the
build on a literal. No count of works, papers or domains (G10). The wire quotation keeps its build-time
assertions. The example's numbers are the paper's prose and are re-read from the record by hand at
every edition change — which is exactly the failure this whole reconciliation found, so it is written
down here rather than trusted to memory.

**The historical route** is specified in `analytical_governance_v2_page_draft_v0_1.md` §3 and is
unchanged by this draft: `/history/analytical-governance-v1-1`, byte-faithful body, an explicit
non-current header with both records named, `s-analytical-governance-v1-1` gaining the route,
components copied rather than shared.

---

## What I need before writing site files

1. **The prose itself** — approve, or mark the lines to change.
2. **The H1.** *"A correct number can still fail the service."* is the page's compression of §1 and is
   the one sentence on the page in the page's own voice at display size. If it should instead be a
   record sentence, the candidates are *"Analytics exists to serve someone with a purpose"* (§1) or
   *"Service is the mission. Servability is a governing gate"* (the pre-§1 aphorism).
3. **The definition strip (§1c).** New to the page, verbatim from the record. In or out?
4. **The §7 forward-reference guard.** Confirm the page states the authoring requirement without
   implying datumwise ships an authoring process.
5. **Route order.** Whether the historical route lands in the same commit as the new current page, or
   first, on its own, so that no moment exists in which the v1.1 body is unreachable.

---

# IMPLEMENTATION RECORD — 2026-08-26, after the final E rulings (15:59)

Implemented and rendered. This section records what shipped and where it departed from the plan above;
the prose sections are unchanged except where a ruling changed them.

## Rulings applied

| item | ruling | how it landed |
|---|---|---|
| 1 | durable citation labels | `labelAtAnswer` / `label` / `labelChangedSinceAnswer` in `citations.py`; four tests; six facts kept six |
| 2 | candidate stays unpublished | still `provisional`, `published: false`; packet re-read from storage |
| 3 | H1 changed | **"Producing a result is not the same as serving an answer."** — the earlier "correct number" H1 is gone, and the `correct` audit is below |
| 4 | keep the definition strip | shipped as `components/ag/TermStrip.astro`, six terms verbatim |
| 5 | historical route first | `/history/analytical-governance-v1-1` built and verified **before** the current page was replaced, in that order |
| 6 | preserve #can-may / #powers | shim forwards them, plus three heading ids the plan had missed — see the anchor finding |
| 7 | current page order | service → legitimacy → intent gap → servability gap → responses → **standing** → serving ↔ authoring → crossings → conformance |
| 8 | ToC is a pointer | exactly two appearances: the deferral paragraph in §Legitimacy and one relation row. No grounds, no triad |
| 9 | retired v1.1 material | matrix, three powers and the refusal aphorism are on the historical route only |

## Deviations from the plan, and why

1. **Component directories are `ag/` (current) and `ag-v1-1/` (preserved), not `ag2/`.** The plan
   proposed a new `ag2/` set beside an untouched `ag/`, which would have left `ag/` holding retired
   components that nothing renders. Instead the retired four were **git-moved** into `ag-v1-1/`
   (so `git log --follow` still reaches their whole history) and the current set stays in `ag/`.
   One directory means current, one means preserved.
2. **`WireQuotation` is copied, not shared.** The plan said reuse it, because its assertions are
   about the shipped package rather than the edition. That was right about the assertions and wrong
   about the rule: a component imported by both routes drifts into the preserved page at the next
   edit, which is the failure the copy-not-share rule exists to prevent. Both copies are identical
   today and the historical one is now frozen.
3. **One derivation inside the preserved body changed, and only the derivation.** The v1.1 hero's
   publication signpost read `citation('w-analytical-governance')` — the work's *current* record. That
   was correct while this page WAS the current doorway and became wrong the moment it stopped being
   one: the preserved page would have rendered the v1.1 compression above a v2.0 signpost and
   misattributed its own body. It is now pinned to `w-analytical-governance.r02`, passed in by the
   route. **No claim in the preserved body was edited.**

## Anchor / redirect compatibility — one finding beyond the ruling

The ruling named two anchors. There were six, because **Ask builds its citation URLs from HEADING ids,
not section ids**: published answers already point at `/analytical-governance#bound-h` and `#close-h`
(see `services/ask/eval/results/*`). A heading id is as load-bearing as a hand-authored link.

| fragment | kind | disposition |
|---|---|---|
| `#two-gaps`, `#can-may`, `#powers` | section ids, live since 21 Aug | → historical route, same anchor |
| `#gaps-h`, `#matrix-h`, `#powers-h` | heading ids of the same sections | → historical route, same anchor |
| `#bound-h` | heading id, "where this sits" | → `#where-this-sits`, a real successor section |
| `#serving`, `#boundaries`, `#authorize` | section ids | → `#responses`, `#crossings`, `#path` in-page |
| `#the-wound`, `#conformance`, `#wire`, `#conf-h`, `#close-h`, `#serving-h`, `#wound-h`, `#ag-thesis` | unchanged | resolve locally |

No successor section was fabricated to preserve a name. Verified by loading
`/analytical-governance#can-may` in a real browser: it lands on the preserved matrix.

## The "correct" audit

Two occurrences survive on the current page and its components, both with the predicate named:

- `ServiceWound.astro` — "each can be written in valid SQL, **each executes correctly**, and each
  returns a plausible number." The predicate is execution, which is exactly what is being conceded.
- `analytical-governance.astro` §servability — "a late-arriving or **retroactively corrected**
  record". This is the paper's term for a data correction, not a claim about an answer.

Removed by the rewrite: "correct number" (the old H1 draft) and the v1.1 page's "Refuse is governance
functioning correctly" (re-cut to "functioning as designed" in the component comment). Elsewhere the
page names the predicate directly: *arithmetically flawless*, *lawfully derived*, *support-sufficient*,
*reproducible*, *servable*, *authorized*, *unfaithful as a service*, *not entitled to answer*. No
taxonomy of correctness was created.

## One naming rule, now in all three places

Adding a route to the preserved source exposed the last copy of the label defect: `index_build`'s
ROUTE path fell back to the work's `canonicalLabel`, which would have labelled the preserved page
"Analytical Governance" and made it read as the current work. It now uses the same rule the deposit
path and `citations.py` use — *an explicitly titled source pinned to a non-current record keeps its own
dated title*. The historical route's 18 chunks are labelled "Analytical Governance v1.1, 21 August
2026", `layer: reference`, standing = edition-pinned + preserved historical state.

## Gates

Website build clean, 45 pages (44 before + the historical route). Publication registry OK — 33 works,
80 records, 85 classified consumers. Corpus membership OK — 45 sources, 17 IN, 28 REFERENCE ONLY, 0
unadjudicated. Ask index rebuilt: 1336 chunks / 20 routes, historical 55, edition-pinned 46. 66 ask
tests green. `check_currency_stamps` still cannot run in this container (columna-core not installed).
