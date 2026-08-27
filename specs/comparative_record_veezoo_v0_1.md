# Comparative record — Veezoo (specimen #15, promoted)

**Filed:** 2026-08-27 · **Author of the finding:** Huayin · **Status:** full comparative record,
six-lens pass OPEN (see §0)

**Subject:** Veezoo AG — Zurich, engineering since 2016. Agentic analytics on a knowledge-graph
semantic layer with an intermediate query language compiled deterministically to SQL.

**Why it is filed as a full record and not a specimen entry:** it is the closest architectural
neighbour we have found. On the authority-placement thesis it sits materially closer to us than
anything previously filed, and it is the first competitor whose architecture would survive lens 5
and lens 6 largely intact. It belongs beside Emergence and Colrows in the comparative record, and
CG2 should see it before the homepage skeleton hardens.

---

## 0 · Filing note — what this file is, and what it is not

**The master comparative record is not in this repository.** Specimens #1–14, the Emergence and
Colrows records, and the canonical wording of the six ratified lenses live outside it. The only
lens cited anywhere in this tree is **lens 5 — carrier/jurisdiction** (`specs/context/…` via
`state_of_the_platform_v0_3.md` §1.4: *"the substrate performs computation; it does not decide what
computation means"*).

So this file is the **deposit of the finding**, pending merge into that record. The six-lens pass is
deliberately left OPEN in §10 rather than authored from reconstructed lens names: five invented lens
headings would read as a completed pass and would be wrong in a way nobody could see. When the
canonical list is to hand, §10 is the only section that needs writing.

**Evidence typing.** Two classes, kept separate on purpose:

| Class | Source | Where |
|---|---|---|
| **A — vendor testimony** | the Veezoo marketing site, read by Huayin. No docs read, no product seen. | §1–§9, the finding as filed |
| **B — vendor documentation** | `docs.veezoo.com` architecture overview + the Apache Ossie page, fetched 2026-08-27 | §11 only, marked as such |

Class B was gathered *after* the finding and is reported separately. It corroborates the two
decisive negatives rather than supplying them. Nothing in §1–§9 has been rewritten to absorb it.

---

## 1 · The facts (class A)

Zurich; engineering since 2016; $6M Series A with ex-Tableau CEO **Mark Nelson** on the board;
Gartner Cool Vendor. Named production logos, none of them trivial: **AXA, Bayer, BMW, Breitling,
Coop, Dr. Reddy's, Helvetia Baloise**. Query-layer architecture, no ingestion. SOC 2 Type II,
EU-hosted.

## 2 · The architecture, stated fairly, because it is genuinely serious

A **Knowledge Graph** holds the business ontology, metrics, governance rules and KPI definitions.
The AI reasons only over those predefined concepts and never touches raw tables. It emits **VQL**,
their own query language, which is then **compiled to SQL through a deterministic, rule-based
process**. Chart titles, filters and labels are *rendered from VQL rather than written by the LLM*,
with hover-to-definition on every governed term. The graph lives in **Git** with version control,
dev branches and tests. Answers reach users through Slack, Teams, Excel, PowerPoint — and through
**MCP and an API to Claude, ChatGPT and Gemini**.

Read that list against our own stack and the resemblance is uncomfortable: declared semantic
objects, an intermediate language the requester's agent writes, deterministic compilation to the
execution engine, an authority boundary the model cannot cross, version-controlled semantics, and
governed answers served to agents over MCP. On the authority-placement thesis they place authority
in a curated graph plus a deterministic compiler — materially closer to us than anything we have
filed. And they have shipped the MCP position proposed for us four exchanges ago, at BMW scale,
today.

## 3 · The crux, and it is one word: **deterministic is not lawful**

Their guarantee is **consistency of computation** — *"Revenue is computed the same way every
time."* Ours is **establishment of the result**: that the requested analytical object exists under
governed law, that the derivation is lawful, and that the support required is actually present.

Those are different properties, and the difference is exactly the **47/48/50 case**. Veezoo would
compute average revenue over the 47 reporting stores — deterministically, every time, with a
governed definition of Revenue, an auditable trail and a clear title — and it would be unfaithful
to the question in precisely the way the Yes Machine describes.

**Reproducibility is not entitlement.** Nothing on their page suggests the graph carries

- existence law (which stores *were open*, versus which have rows);
- reducer and closure classes (whether this mean may be meaned again);
- movement law (whether that join fans out);
- the distinction between **absent**, **zero** and **ineligible**.

## 4 · Where the AI still decides — and their mitigation deserves real credit

"No hallucinations" is an overstatement of a real achievement: they have eliminated hallucinated
**syntax**, not hallucinated **interpretation**. Question → VQL is still the model's probabilistic
step; VQL → SQL is the deterministic one. Choosing the wrong governed concept therefore produces a
wrong answer with perfect provenance.

Their mitigation is genuinely clever: because the title is rendered from VQL, the interpretation
becomes **inspectable** — the user can read exactly what was asked. That converts an invisible error
into a visible one and hands the check to the user, which is **Article 5's relier duty made
operable**, and better than most of the field.

But in the **AG Rethought v0.4** vocabulary it is the wrong side of a distinction we just drew:
surfacing the governed alternatives and letting the user choose is **enablement**; silently
selecting one and then showing what was selected is **constitution by the serving system, mitigated
by disclosure**. The user must already know that the population question exists in order to notice
that "per store" resolved to "reporting stores."

## 5 · The placement — and this is the finding to lead with for CG2

Run Veezoo through the **two-gap frame** and it discriminates cleanly.

- **Intent gap — substantial work.** Governed vocabulary, inspectable resolution, hover
  definitions, deterministic labels.
- **Servability gap — nothing, so far as the page shows.** No support-sufficiency test, no
  analytical-establishment test, and — decisively — **no outcome other than an answer**. There is no
  Refuse, no Disclose, no Clarify anywhere in the material.

And constraining the model to declared concepts creates a **specific new risk in place of
hallucination**: unanswerable questions get mapped to the nearest *answerable* concept, silently.
**A vocabulary that cannot say "open store" will answer with the store it has.**

## 6 · The third gap, at the top

Feature three is *"Understand — helps you interpret the data, suggests next steps, summarizes key
insights."* Titles are protected from the LLM; **insights are not**. The architecture is rigorous up
to the number and then hands the number to a language model for interpretation and recommendation —
which is exactly where our **Evidence** and **Intelligence** pillars begin. Their trust engineering
stops at the number; the claim built on the number is ungoverned.

## 7 · Authoring

*"Agentic Modelling — model Knowledge Graphs from scratch with AI, leveraging all your existing
documentation"* is the **harvest premise** again — Databricks Genie, dltHub, Atlan, now Veezoo: that
is five.

But paired with Git branches, review and tests it is the **strongest authoring discipline in any
commercial product we have filed** — closer to ratification than anyone else. The limit stands:
review catches errors you can see; it cannot supply a fact nobody ever recorded. **No amount of PR
review over a harvested graph produces the open-store roster.**

## 8 · Strategic consequences for us, plainly

Our differentiation **cannot** be "semantic layer plus deterministic compilation" — that is shipping
at BMW with a Tableau CEO on the board. It has to be:

1. the **servability gate**;
2. **typed absence** and support;
3. **lawfulness of derivation**;
4. **outcomes other than answers**.

That is *good* news for the composition claim, which already reads that way, and it sharpens the
four-box frame: **Veezoo is an unusually strong box-two occupant reaching toward box four without
entering it.**

Note also that they are integrating **Apache Ossie** and marketing *"no lock-in of your
semantics"*: the openness and standards cards are being played, so structural honesty alone will not
differentiate at the semantic-layer level.

## 9 · Caveats on their claims, for the record

Four unsourced "#1" banners, "the most advanced semantic layer", and a governance superlative from a
board member — all **testimony**, none independent. Under our own rules that is not an attack, just
correct typing.

---

## 10 · The six ratified lenses — OPEN

Not authored here. The canonical lens list is not in this repository (see §0). One lens can be
stated from an in-tree citation:

- **Lens 5 — carrier/jurisdiction.** *"The substrate performs computation; it does not decide what
  computation means."* Veezoo **passes**: the AI reasons only over declared concepts and the
  compiler, not the model, decides what the computation means. This is the sense in which it is the
  first competitor whose architecture survives the lens intact.

Lenses 1, 2, 3, 4 and 6 to be filled from the ratified wording. §5 (two-gap) and §3 (deterministic
vs lawful) are the inputs the pass will need.

---

## 11 · Second-source addendum (class B — vendor documentation, fetched 2026-08-27)

Gathered after the finding was filed, from `docs.veezoo.com/veezoo/architecture-overview/` and
`veezoo.com/apache-ossie`. Reported separately so it cannot be mistaken for the marketing-page
testimony above.

**It corroborates both decisive negatives, from a source that is not the marketing page.**

1. **The pipeline, in their own words:** *Natural Language → Semantic Resolution → Agentic Plan →
   VQL → SQL → Execution → Verification → Visualization.* And: *"The AI does not write SQL. The AI
   only reasons over business concepts in the Knowledge Graph; compilation from VQL to SQL is
   deterministic and happens without AI involvement."* §2 and §4 stand as written.

2. **No outcome other than an answer — confirmed.** The architecture documentation describes no
   mechanism for refusing, declining, clarifying, disclosing assumptions, or reporting insufficient
   data. §5 can be upgraded from *"so far as the page shows"* to *"and the architecture
   documentation likewise shows none."*

3. **No population or eligibility semantics — confirmed.** No discussion of nulls, missing data,
   filter semantics, row eligibility, or which records are included or excluded. This is the
   47/48/50 case's home, and it is empty. §3 stands.

4. **What "Verification" actually verifies — a correction worth having.** The pipeline's Verification
   step is *"Every number the AI quotes from your data is verified character-for-character against
   the actual query results before it is displayed"*, with verified numbers clickable back to
   source. That is **numeral fidelity — our "every numeral verbatim from the wire, grounding is
   structural" move** — and it is a *third* place where they are close to us. It is emphatically
   **not** a support-sufficiency or establishment test: it checks that the number quoted matches the
   number returned, never that the number should have been returned. The documentation does not say
   what happens when verification fails.

5. **The probabilistic surface is larger than "question → one VQL".** *"Veezoo builds an execution
   plan determining which VQL queries to run and in what order… complex analyses may require
   adaptive plans that adjust based on intermediate results."* So the model chooses a *plan* — a
   sequence of governed concepts, with later steps conditioned on earlier results. §4's point
   sharpens: the inspectable title shows the user what was asked, but an adaptive multi-step plan
   has interpretation decisions that no single rendered title exposes.

6. **VKL vs VQL — a naming correction for §2/§7.** The graph is authored in **VKL** (Veezoo
   Knowledge Language); **VQL** (Veezoo Query Language) is the intermediate query language the AI
   emits. So "Agentic Modelling" generates *VKL*, and it is VKL that lives in Git under branches,
   review and tests. The authoring finding in §7 is unaffected and slightly strengthened: the
   review discipline applies to the authored semantic artifact itself.

7. **Apache Ossie, correctly named.** Apache Ossie (incubating) is an open specification for
   semantic models at the Apache Software Foundation — datasets, fields, relationships, metrics, in
   a vendor-neutral format. It was launched as **Open Semantic Interchange (OSI)** with 17 partners,
   then donated to the ASF and renamed, the acronym having collided with the Open Source Initiative.
   Veezoo state a commitment to supporting it natively, with imported definitions feeding the same
   deterministic VQL → SQL compilation. §8's standards point is correct and the name is right;
   note for our own filings that **OSI and Apache Ossie are the same effort at two dates** —
   `state_of_the_platform_v0_3.md` §3.3's "OSI vocabulary standardization" clock is this clock.

Sources: <https://docs.veezoo.com/veezoo/architecture-overview/> ·
<https://www.veezoo.com/apache-ossie>

---

## 12 · What would change the finding

Stated in advance, so the record can be falsified rather than defended:

- **Any outcome other than an answer** in the product — a refusal, a declared insufficiency, a
  clarify that offers governed alternatives rather than picking one. That would move them out of
  box two.
- **Existence or eligibility law in the graph** — anything that distinguishes *no rows* from *not
  open*, or that types absence. That is the 47/48/50 defence.
- **A closure or reducer discipline in VKL** — any declaration governing whether a derived quantity
  may be re-aggregated. That is the average-of-averages defence.
- **Governance extending past the number** to the interpretation and recommendation surface (§6).

None of the four is visible in either evidence class today.
