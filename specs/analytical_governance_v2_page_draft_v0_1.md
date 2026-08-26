# /analytical-governance — the v2.0 doorway

**Draft for ruling. Status: NOT IMPLEMENTED.** Per CG2 ruling E.5 (2026-08-26), the proposed prose
and structure come back before any reader-facing site file changes. Nothing under
`apps/website/src/` has been touched for this draft. The registry title correction (E.1) *has* been
applied, because that is registry truth being re-derived from a corrected deposit, not page copy.

Source of record: **Analytical Governance v2.0**, `w-analytical-governance.r03`, as retrieved and
byte-verified in `services/ask/deposits/`. Every sentence proposed below is traced to a section of
that record. Where the current page says something only v1.1 said, that is called out rather than
carried across.

---

## 0 · The three findings that shape the draft

### F1 · The subject of the page changes, and the current hero states the old one

v1.1 organised the category around **can vs may**. v2.0 organises it around the **legitimacy of a
service**, and demotes servability from the mission to a gate inside it — in the paper's own words,
before §1:

> Service is the mission. Servability is a governing gate.

The current hero's proposition — *"What can be computed is not yet what may be served"* — is a true
sentence that is no longer the paper's organising claim. It survives inside the new §4 as the
servability gap's compression (v2.0 §4: *"Computability does not imply servability."*), and it stops
being the page's thesis.

### F2 · The open-store numbers changed between editions, and the page renders v1.1's

| | v1.1 (`r02` §1, §8) | v2.0 (`r03` §1, §10) |
|---|---|---|
| roster | 50 stores **open** yesterday | 50 stores **exist** |
| open yesterday | — | **48**, per an operating-status source |
| revenue rows | 47 | 47 |
| decomposition | 2 governed zero-revenue store-days, 1 feed failure | none |
| candidate denominators | 47 / 49 / 50 | 47 / 48 / 50 |
| disposition | population established (50); requested result withheld for one unsupported point | the roster does not establish openness; the revenue rows do not establish the population |

`components/ag/OpenStoreWound.astro` renders the v1.1 column — including the ruled disposition line
("The 50-store population *is* the governed population… still withheld, because one store-day…
lacks the revenue evidence"). **Under current Core that sentence has no support**: v2.0 neither
carries the 2/1 decomposition nor makes 50 the open population. The component must be re-derived
from v2.0 §1 + §10, not adjusted.

This is the sharpest argument for ruling E.3: the v1.1 body is a *faithful historical state* and is
not merely an older wording of the current page.

### F3 · Two of the page's strongest sections are v1.1-only material

- **`CanMayMatrix`** — CAN/MAY × within-world/crossing. v2.0 has no within-world/crossing axis at
  all; its §9 "Govern the crossings" means the crossings of the *service passage* (purpose → request
  → plan → result → answer → action), which is a different object. The matrix does not migrate.
- **The conformance blockquotes** — *"A governed analytical system must be capable of withholding
  analytical permission. If it cannot refuse, it is not governed."* and *"Every served answer must be
  entitled under the declared analytical meaning and current support…"* are both **verbatim v1.1**
  (`r02` L155, L494) and neither appears in v2.0. v2.0's equivalents are the §12 requirement (*"a
  servability gate capable of withholding or qualifying analytical permission"*), the §5 line
  (*"Refusal is evidence that analytical permission is real"*), and the §13 maxim (*"Serve only what
  is servable"*).

- **`Three powers, separated`** (interpretation ≠ adjudication ≠ execution) is v1.1's taxonomy.
  v2.0's operational cut is different and is stated in §2: *"User purpose → analytical intent →
  governed analytical construction → reliable production → servability → warranted reliance →
  consequential use"*, with §9 carrying the authority separation as a sentence rather than a
  three-power structure: *"The component that can produce a candidate result need not be the
  component entitled to authorize what that result becomes."*

**Nothing above is a defect in the v1.1 page.** It was faithful to its record. It is now the record
of a superseded edition, which is exactly what the historical route is for.

---

## 1 · The page, as nine approved movements in eight sections

Ruling E.4's order is kept. §6 and §7 of the ruling are set as one section because Escalate is the
joint between them and the existing `ServingBoundary` already renders that joint correctly.
Register: PAPER throughout, one WIRE quotation near the end, as now.

### §1 — Hero · analytics is a service relationship

> **Label** Analytical Governance
>
> **Proposition** Analytics exists to serve someone with a purpose.
>
> **Organizing sentence** Analytical Governance is the discipline governing the **legitimacy of the
> analytical service**: the user's purpose must survive the passage from intent to answer, the result
> must be established under the relevant analytical law and support, and the answer must carry no
> more authority than its grounds warrant.
>
> **Criterion band** (quiet, full width, above the rule — the position the conformance test holds
> today)
> A conforming analytical service must be able to **withhold or qualify analytical permission**.
> Refusal is not an error state; it is the evidence that the permission is real.
>
> **Signpost** registry-derived: deposited title, author, version, date, DOI of the current record,
> plus the standing line *"The category paper. This page is a doorway; the deposit governs."*

Traces: §Abstract (legitimacy definition), the pre-§1 aphorism, §5 Refuse, §12 first requirement.

Retired here: *"What can be computed is not yet what may be served"* as the page thesis, and *"If it
cannot refuse, it is not governed"* as the criterion band. Both are preserved on the historical
route in their own edition's voice.

### §2 — The wound, re-derived · one question, three arithmetics

Same shape as today (question, what the system knows, the candidate procedures, the landing), with
v2.0's facts:

> **What was average revenue per open store yesterday?**
>
> | fact | establishes | source |
> |---|---|---|
> | 47 revenue rows arrived | what reported, not what was open | the sales table |
> | 50 stores exist | the roster — **not** that 50 were open | the store roster |
> | 48 were open yesterday | the requested population | the operating-status source |
>
> Divide by 47, by 48, or by 50. All three are executable. All three return a plausible number.
>
> **The computation does not tell us which answer serves the user's purpose.** The 50-store roster
> does not establish that all 50 were open; the 47 revenue rows do not establish the open-store
> population. Presenting the mean over reporting stores as *average revenue per open store* can be
> arithmetically flawless and unfaithful as a service.

Deliberately still *no crowned number*, for the v2.0 reason rather than the v1.1 one: the
disposition depends on whether the required revenue state is supported for the 48 established points
(§10, "Reliable production and support"), and that is the next two sections' work.

### §3 — Legitimacy · what must remain true

The operational cut, set as the page's spine (v2.0 §2):

> User purpose → analytical intent → governed analytical construction → reliable production →
> servability → warranted reliance → consequential use

> This is an operational cut through the analytical service, not a replacement taxonomy for the
> foundational domains whose laws the service uses. Different systems may combine functions.
> Governance requires only that the distinctions stay visible enough to adjudicate.

Then the three obligations, tight, one paragraph each (§2.1–2.3):

- **Faithfulness** — does the service preserve the user's purpose as it becomes a request and an
  answer? Two duties, not one: *fidelity* keeps the system from saying something different from what
  the user means; *enablement* helps the user say more precisely what they are trying to know.
  Neither authorises the system to choose silently on the user's behalf.
- **Reliability** — can the governed process produce the established result consistently? It
  preserves and produces; it does not create analytical meaning, and *"a reliable production path
  must reproduce and carry forward the object that was actually established."*
- **Certainty sufficient for reliance** — whether the grounds can bear the reliance being placed on
  them.

**The Theory of Certainty appears here, and only as an external foundation** (ruling E.2). One
placement, one paragraph, no absorption:

> Analytical Governance does not develop its own account of what makes grounds sufficient. That
> upstream discipline — what carries a conclusion, what it establishes, where its warrant stops, and
> whether it can bear the intended reliance — is developed separately in **The Theory of Certainty**,
> and Analytical Governance turns those questions into a governed analytical service.
> [→ the current publication record, registry-derived]

Not on the page, deliberately: the three grounds (theory of object / theory of other / behavioural
evidence), the substitution error, reach, composition, exposure. Those are ToC's, and a doorway that
summarised them would be absorbing the theory it is pointing at. No triad of domains is asserted,
named, or implied (ruling E.2, third clause).

### §4 — The intent gap · fidelity and enablement

> The first gap is the distance between what a user can initially express and the analytical request
> that faithfully captures their purpose with the distinctions governance needs.

The worked case, from §3, is the page's best short proof that enablement is not translation:

> A user asks for "average revenue." The service can surface the governed alternatives — among
> reporting stores, existing stores, stores that were open — explain the difference, and let the user
> choose. **That is enablement. Silently selecting one of them is unauthorized formulation.**

And the guard v2.0 adds, which the v1.1 page has no equivalent of:

> Enablement must not conceal materially relevant governed alternatives. Selectivity must itself be
> governed or disclosed.

Closing line of the section (§3): the gap is closed when the purpose has become *"an analytical
request explicit enough for independent adjudication."*

### §5 — The servability gap · from governed request to answer

Two propositions, set as the section's structure (§4):

> **Faithful request does not imply servable request.**
>
> **Servable = Support Sufficient AND Analytically Established**

Then, in prose: analytical establishment asks whether the requested object exists under the governed
model and whether the derivation is lawful; support sufficiency asks whether the evidence and
sufficient state this request requires are presently available. Three failures, one line each — a
missing feed leaves a lawful request unsupported; an unlawful reduction leaves abundant data unable
to establish the result; an unresolved population makes a computable denominator unestablished.

The compression that used to be the hero lands here, in its own edition's words:

> **Computability does not imply servability.**

And the two sentences that keep the gate from being read as a platform property:

> Servability is not a generic property of a dataset, metric, model, or platform. It is a
> determination about a particular analytical request under current grounds.
>
> A result may be servable and still not be served.

### §6 — Governance responses, and the edge of the constitution

Keeps the existing shape, which is already the v2.0 shape: **Serve · Disclose · Clarify · Refuse**
in one row as the serving vocabulary, a hard rule, then **Escalate** beneath it, outside the row.
Text updated to v2.0 §5 wording — notably Refuse (*"Refusal is evidence that analytical permission is
real"*) and Escalate (*"not a fifth serving mood… a governance-process transition"*, with the return
path: *"escalation does not produce an unofficial answer."*)

Immediately below, ruling E.4's item 7 — serving ↔ authoring (§6) — as the same section's second
movement rather than its own:

> The service runs against a governed **constitution**: analytical meaning, law, support
> requirements, authority. **Serving applies the current constitution. Authoring changes or extends
> it**, through an authority event that can be reviewed and ratified.
>
> **A serving system must not silently create the missing meaning or authority that would make its
> own answer servable.**
>
> unresolved need → authoring or declaration → review and ratification → governed constitution →
> serving
>
> **Clarify stays inside the constitution. Escalate reaches the constitution's edge.**

The existing count-note survives verbatim in substance: five externally meaningful outcomes for the
governance process, four at the machine serving boundary, and collapsing the two counts is how a
governance boundary quietly becomes a response enum.

### §7 — Standing · what the service may pass forward

Ruling order puts standing before responses; the draft keeps standing *here*, after them, and this
is the one departure from E.4's sequence that the draft asks for. The reason: standing is about what
happens to an answer *after* it has been served, and every v2.0 sentence about it presupposes the
serving verdict (§7 opens *"Servability asks whether a candidate result may be served as the
answer"*). Placed before §6, the page has to explain a served answer before it has said what serving
is. **If CG2 prefers the ruled order, the section is written the same way and simply moves up.**

> Standing is claim- and boundary-specific. A result may stand for exploratory display and not for
> compensation. An estimate may stand as an estimate and not as a causal claim.
>
> **Standing prevents a result from becoming more authoritative merely because it travelled.
> Conclusions are portable; their grounds are less so.**

Folded in, one short movement, from §8 — because it is the same boundary seen from the other side:

> Cost, security, application risk and authorisation can constrain an established analytical
> service. They cannot supply a missing analytical ground. **Risk may constrain the right answer. It
> cannot turn an unestablished answer into the right one.**

### §8 — Governed crossings

> Analytical service becomes consequential at crossings: purpose becomes a request, a request
> becomes a plan, a plan produces a result, a result becomes an answer, an answer becomes action.
> Each crossing is an opportunity for authority to travel farther than its grounds.
>
> **The component that can produce a candidate result need not be the component entitled to
> authorize what that result becomes.**

AI agents as *one application* of the crossing discipline, not the subject of the section (§9): a
model may interpret language, formulate a candidate request, generate candidate SQL, summarise
evidence, explain an adjudication — none of which requires it to carry analytical authority. Then
the blast wall, in v2.0's own framing: *"a structural boundary that prevents reasoning output from
becoming consequential execution directly"*, and *"a structural execution boundary can close one
consequential path independently of predictions about the agent."*

This is also where the page's existing "where this sits" relation list belongs, shortened. Data
governance stays canonical (*"The two compose; neither substitutes for the other"* — §11), Theory of
Data and the Statistical Bridge keep their relations, **and The Theory of Certainty joins the list**
with the relation *supplies the upstream discipline to* — the second and last appearance of ToC on
the page, as a neighbour, not as content.

### §9 — Conformance, consequence, and the path

The membership test, argued rather than displayed, now from §12 rather than v1.1's aphorism. The
requirements list is short enough to render whole and is the strongest thing on the page for a
reader deciding whether their own architecture conforms:

> A conforming practice or architecture needs, at minimum: a way to preserve user purpose while
> translating intent into an explicit analytical request; a governed analytical representation that
> can independently establish identity, derivation, support requirements and relevant state; a
> reliable production path that preserves what was established; **a servability gate capable of
> withholding or qualifying analytical permission**; a way to preserve standing, conditions, reasons
> and alternatives across boundaries; separation between analytical establishment and later cost,
> security, application and authorisation decisions; and execution faithful to what governance
> actually authorised.

With the non-claims kept, because they are what stop the category reading as a product claim: it
does not guarantee perfect intent, data, declarations or decisions; it does not replace semantic
knowledge, statistical inference, security engineering, physical optimisation or decision governance;
and it requires no particular query language, semantic layer, or architecture.

Then, unchanged in mechanism: **the WIRE quotation** (build-adjudicated against the shipped package;
the four serving moods present, `escalate` absent by construction) and the closing path, re-cut to
v2.0's §13 maxim:

> Preserve purpose. Establish the analytical object and its grounds. Produce it reliably. Serve only
> what is servable. Preserve standing across crossings. Govern consequential use.

---

## 2 · Derivation rules the implementation must keep

1. **No publication fact is typed.** Title, version, date, DOI for both AG and ToC come from
   `citation(workId)`. `check_publications.py` classifies this route `derived` (G7) and the build
   fails if a literal DOI appears. The ToC link resolves through the registry to the current ToC
   record; nothing on the page states which version that is.
2. **No count of works, papers or domains.** G10 stays satisfied; `kind` is still `unclassified` for
   every work.
3. **The wire quotation keeps its build-time assertions** (four moods present, `escalate` absent).
4. **The example's numbers are prose, not derived** — they are the paper's, and the page cites the
   section they come from. The gate cannot check them; the historical-state finding above is why
   they are re-read from the record by hand at every edition change.

---

## 3 · Preserving the v1.1 body (ruling E.3)

The current page body becomes a preserved historical state at a permanent address, following the
`/history/research-map-2026-08-03` pattern exactly.

| | proposal |
|---|---|
| route | `/history/analytical-governance-v1-1` |
| content | the current page **byte-faithful**, including `AgHero`, `OpenStoreWound`, `TwoGaps`, `CanMayMatrix`, the three powers, the v1.1 conformance blockquotes, `ServingBoundary`, the relation list, `WireQuotation`, the closing path |
| header | an explicit non-current banner: preserved state of 21 August 2026; the current record is v2.0 and the current doorway is `/analytical-governance` — both registry-derived |
| registry | `s-analytical-governance-v1-1` already exists in `registry/sources/sources.json` as `role: historical-record`, `recordId: w-analytical-governance.r02`, `preservedState: 2026-08-21`, with **no route**. This adds the route. |
| Ask | the v1.1 deposit is already indexed as `layer: reference`, demoted and labelled; the new route inherits the same standing sentence |
| components | the v1.1 components are **copied, not shared**. A component imported by both routes would drift into the current page at the next edit, which is the whole failure mode being closed. The v2.0 doorway gets its own set. |
| anchors | `#the-wound`, `#two-gaps`, `#can-may`, `#powers`, `#serving`, `#conformance`, `#boundaries`, `#wire`, `#authorize` are live and sitemap-indexed today. `#can-may` and `#powers` have **no successor** on the v2.0 page. Proposal: the same fragment shim `/research` uses — those two forward to the historical route at the same anchor; the other seven resolve on the current page, where the section still exists in a v2.0 voice. |

Note on **currency vs preservation**, from the ruling: a citation of the v1.1 *page* must resolve to
the v1.1 *record* — the record whose words were actually cited — and the fact that v2.0 is now
current is a separate fact, stated separately. That is what `citations.py` does for Ask answers, and
the historical route's header states both for the same reason.

---

## 4 · Decisions this draft needs from CG2

1. **`canonicalLabel` for `w-analytical-governance`.** It is `"Analytical Governance: From User
   Intent to Governed Analytical Execution"` — the *superseded* edition's title, and it is editorial
   naming, which the registry README reserves to a person. With the title corrected it now renders,
   live, on `/about`, `/research`, `llms.txt`, the AG closing path (as *"…From User Intent to
   Governed Analytical Execution — Version 2.0"*) and every Ask citation label for this work.
   **Recommendation: `"Analytical Governance"`.** The label is meant to be stable across the whole
   deposit history; a v1.x subtitle never was. Not changed unilaterally.
2. **The §7 placement** (standing after the responses rather than before). Either order is written;
   the draft argues for the later one.
3. **The retired v1.1 aphorism.** *"If it cannot refuse, it is not governed"* is a compression v2.0
   does not contradict but does not state. The draft removes it from current authority and preserves
   it on the historical route. Keeping it on the current page would mean the page's criterion band
   cites a superseded edition.
4. **The matrix and the three powers.** The draft retires both from the current doorway (F3). If
   either is to survive as current, it needs a v2.0 grounding the draft could not find.
