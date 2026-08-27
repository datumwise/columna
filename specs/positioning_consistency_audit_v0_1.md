# datumwise / Columna positioning consistency audit (v0.1)

**Requested:** Huayin, 2026-08-27 (positioning ruling + consistency audit, §§A–J).
**Status:** AUDIT ONLY. No positioning copy changed. Nothing implemented.

**Measured against the rulings:** datumwise is the only thing that needs *positioning*
("an independent research project exploring central topics of our time around data, analytics and
technology"; bearing **Data · Certainty · Intelligence**). **Columna** needs a description —
"infrastructure for governed analytical service" — not a market position. **Core** needs a factual,
version-sensitive capability description. **Platform** needs an architecture/direction description,
never stated as shipped. The old closure claim is retired from current voice.

---

## The short answer

**The website is close to clean. The documentation and the packages are not.**

Your expectation — "very little to fix" — holds for the reader-facing site, with one page and the
layout defaults to correct. It does not hold for two surfaces nobody was looking at, both of them
live to strangers:

1. **`/docs/framework` — the normative manual — describes a commercial product that does not
   exist, in the present tense, on datumwise.ai right now.** Chapter 13 sells an open-core split:
   *"Pro includes a cloud-hosted service, in which Columna operates the entire stack — planner,
   artifact store, integrity monitoring, refresh orchestration, agent infrastructure — as a managed
   subscription."* There is no Pro tier, no cloud service, no subscription. The same chapter says
   *"Core supports two backends — Polars and the full capabilities of DuckDB"*; the shipped code has
   exactly one connector, `DuckDBConnector`. Verified live by fetching the page.
2. **PyPI ships stale and market-flavoured copy.** `columna-core` **0.16.2** renders a README headed
   *"# Columna Core (0.7.8-core)"* — nine minor versions behind, with a v0.7.8 release note as the
   lede. `columna-server` **0.11.0** ships *"the wedge product: **the first** metrics MCP server that
   can say 'it depends.'"* And both packages self-file on PyPI under `keywords = [… "semantic-layer"
   …]` — the category the manual spends three pages arguing Columna is *not*.

**Two clean negatives.** The retired closure claim — *"The ideas redefine the problem. Columna
provides the native working answer."* — **does not exist anywhere in this repository**, in any voice.
Neither does "idea-led, product-consequential". There is nothing to retire; §C's target lives only in
conversation. And **no rendered surface carries the retired bearing**: `Data · Certainty ·
Intelligence` is live on the homepage and `/foundations`, confirmed against production.

**And the best formulation of §B's requirement is already live, in the Ask constitution:**
`services/ask/ask/skill.py:31–33` — *"datumwise — an independent open-source research project …
**whose work includes** the Theory of Data, Frame-QL, Analytical Governance, and the Columna
framework."* Columna as one item in a list of works, not the culmination of the research. That is
executed on every public `/ask` request today.

---

## A note on method, because one finding was wrong before it was checked

The two sweeps were scoped to disjoint trees. The records sweep — which by instruction could not see
`apps/website/src/**` — concluded that *"`Data · Evidence · Intelligence` is the shipped wording"*,
because inside `specs/` the change exists only as an unimplemented proposal.

**That conclusion is false, and the correction matters more than the finding.** The bearing was
implemented on 2026-08-27 (`Bearing.astro:66`, `foundations.astro:146`), and production serves
`Data · Certainty · Intelligence` — verified by fetching `https://datumwise.ai/`. A spec that says
"PROPOSED, not implemented" outlives its own execution unless someone closes it. Both
`specs/foundations_mission1_recon_v0_1.md` and `specs/foundations_mission1_implementation_plan_v0_1.md`
still read as pending work that has in fact shipped — which is a small instance of the same defect
class as CV-7: a record correct as history, misleading as a current statement.

---

## 1 · The consistency tests (§I), answered

| # | test | verdict |
|---|---|---|
| I1 | any current surface still says **Data · Evidence · Intelligence** | **PASS** — no rendered surface; production confirms. Survives only in `components/home/Hero.astro:149`, a dead file with zero importers — but as *markup*, not a comment. One accidental import restores the retired bearing. |
| I2 | Columna treated as the **complete/native/final answer** | **PASS in substance** — the literal claim is absent everywhere; four paraphrases are rendered (§2c), and two live counter-formulations already refuse the reading. |
| I3 | **Core positioned as the whole future Columna** | **FAIL** — two ways. The JSON-LD `SoftwareSourceCode` node named "Columna" *is* the installable artifact on every page, with no core/server distinction. And the unbuilt tier has **three names in three live-or-frozen documents** — "Server" (enterprise plan), "Platform" (architecture records), "Pro" (the normative manual) — with no cross-reference between them. |
| I4 | **future Platform capability described as shipped** | **FAIL, live** — the manual's Chapter 13, rendered at `/docs/framework`: a Pro tier, a cloud subscription and a Polars backend, all present tense, none of them existing. The *site's own pages* pass this test (`/columna:155–157`, `/ladder:117` are exemplary); the manual it renders does not. |
| I5 | **competitor-relative market position** for Columna | **FAIL** — `columna-server`'s "the first…" on PyPI; `semantic-layer` in both packages' keywords; `/about` and `/why` differentiation sentences; `PrecisionRecallFigure` as an explicit "we beat them on both axes" graphic; and `/ladder`, which is a comparison page by design (see §3b). |
| I6 | conflicts with **"infrastructure for governed analytical service"** | **PARTIAL, and it needs a ruling** — nothing contradicts it, but the wording is **not in use anywhere**, and "governed analytical service" is currently *Analytical Governance's* subject, with Columna typed as "an executable consequence of" it. See §3c. |
| I7 | conflicts with the **new /about identity** | **FAIL, one page** — `/about:62` calls *Columna* "an independent open-source research project", five lines after `/about:57` calls *datumwise* one. |

---

## 2 · The audit

**DW** = datumwise positioning · **COL** = Columna description · **CORE** = Core capability ·
**PLAT** = Platform architecture/direction · **HIST** = historical only.

### 2a · UPDATE / RETIRE — the actual list, worst exposure first

| # | surface | exact current language | class | disposition | smallest change |
|---|---|---|---|---|---|
| **1** | `docs/columna_framework_manual_6g.md:641` — **live at `/docs/framework`** | "**Pro includes a cloud-hosted service**, in which Columna operates the entire stack … as a managed subscription." (+`:635` "Pro supports custom operators…", `:625–639` the whole open-core/Pro section, all present tense) | PLAT | **UPDATE** | Mark the tier as direction, not product. The repo already has the instrument: ADR-034's honest-hatching rule — *"unmarked constructs do not exist"* — is applied to Ch. 26 and not to Ch. 13. Apply the existing rule; no new doctrine needed. |
| **2** | `docs/columna_framework_manual_6g.md:633` — same page | "Core supports **two backends — Polars** and the full capabilities of DuckDB" | CORE | **UPDATE** | One connector ships (`connector.py:117`, `DuckDBConnector`). `datumwise_enterprise_plan_v0.2.md:19` independently records Polars as **MISSING**. Present-tense claim of capability that does not exist. |
| **3** | `packages/columna-core/README.md:1` — **PyPI front page of 0.16.2** | `# Columna Core (0.7.8-core)` + a v0.7.8 release note as the lede; `:75` mixes Core and Pro scope in one sentence | CORE | **UPDATE** | Retitle to the shipped version; replace the stale banner with one factual paragraph of shipped capability. |
| **4** | `packages/columna-server/README.md:5` — **PyPI front page of 0.11.0** | "This is the wedge product: **the first** metrics MCP server that can say *'it depends.'*" | COL | **RETIRE FROM CURRENT VOICE** | Delete. It is an unverifiable market-first claim on a shipped artifact — and `specs/f_evaluation_report_v0_1.md:83` already names this exact defect class ("'No other,' 'only system,' … exceed the evidence"). |
| **5** | `packages/columna/pyproject.toml:16`, `packages/columna-core/pyproject.toml:23` | `keywords = [… "semantic-layer" …]` | COL | **UPDATE** | The packages file themselves under the category the manual argues against. Costless to fix, and it is what package indexes and AI crawlers read as our self-classification. |
| **6** | `apps/website/src/pages/about.astro:65` | "It builds and stewards **Columna** — an honest data framework: **the grammar layer for AI analytics, beside your semantic layer, married to no database**." | COL | **UPDATE** | Everything after the em-dash is category rhetoric plus semantic-layer differentiation. |
| **7** | `apps/website/src/pages/about.astro:62` | "**Columna** is an independent open-source research project — Huayin Wang (research), Irena Wang (engineering)." | DW/COL | **UPDATE** | The predicate belongs to datumwise, now stated five lines above. |
| **8** | `apps/website/src/layouts/BaseLayout.astro:65` — **default meta description, every page setting none** | "datumwise builds and stewards Columna — an open-source data framework (Manifold, FrameQL, an honest engine) that refuses to return a confident wrong number." | DW | **UPDATE** | datumwise's identity, site-wide, defined entirely by Columna — on `/install`, `/thesis`, `/why` and every page without its own description. |
| **9** | `apps/website/src/layouts/BaseLayout.astro:104` — JSON-LD, every page | "An independent open-source research project — not a company. It builds and stewards Columna, **the grammar layer for AI analytics**." | DW | **UPDATE** | Keep "not a company" and the non-affiliation line (both load-bearing anti-confusion facts); the category phrase is the part that moved. |
| **10** | `apps/website/src/pages/about.astro:43` — page meta | "datumwise is the work of the datumwise team, building and stewarding Columna — the grammar layer for AI analytics." | DW | **UPDATE** | The page's own description still carries the identity its opening paragraph replaced. |
| **11** | `apps/website/src/content/llms_index.txt:1–13` — **`/llms.txt`, machine-facing** | Heading `# Columna`; "Columna is a framework for describing what your data MEANS, shipped as a Python library"; "not a semantic layer over someone else's engine"; datumwise appears only under "## Who" at line 12 | COL/DW | **UPDATE** | Columna-first, with no Data · Certainty · Intelligence, no Foundations, no Analytical Governance. It describes the site datumwise *had*. This is what agents read first. |
| **12** | `apps/website/src/layouts/BaseLayout.astro:116–135` — JSON-LD `SoftwareSourceCode` | one node named `Columna` = the installable artifact; no core/server distinction | COL/CORE | **UPDATE** | Emitted on `/foundations`, which never mentions Columna in prose. |
| **13** | `apps/website/src/components/home/Hero.astro:149,152` | `Data · Evidence · Intelligence` + "across data, evidence, and intelligence" | HIST | **RETIRE FROM CURRENT VOICE** | Dead file, live markup. Delete it. I1 currently depends on nobody typing one import line. |
| **14** | `research/README.md` (+ root `README.md:103` pointing at it) | "Pointers to the research artifacts behind Columna: **Atlas — (DOI: TODO)** … (DOIs to be filled in when the papers are published; this file is a placeholder index in WP-0.)" | DW/Q5 | **UPDATE** | Every one of those DOIs now exists in the registry. The root README sends readers here "for the theory behind the four moods". |
| **15** | `CLAUDE.md:59,67` | "# Current task: Launch checklist v1 — steps 3–8" · `columna-server 0.1.0` · core `0.7.8` | HIST-as-current | **UPDATE** | A months-stale "current state" in the file agents read first. Not positioning, but it is the frame every future session inherits. |

### 2b · KEEP — correct as-is, and worth protecting

| surface | language | why |
|---|---|---|
| `services/ask/ask/skill.py:31–33` — **live doctrine, executed per request** | "datumwise — an independent open-source research project … **whose work includes** the Theory of Data, Frame-QL, Analytical Governance, and the Columna framework." | The best existing statement of §B: Columna as one work among several. Also `:88` types Columna as *normative for what Columna does* and nothing more. |
| `registry/sources/ask-authority.json:228` · `current-corpus.json:95` | "The shipped language and system, within their stated jurisdiction. **Authoritative for what Columna actually does.**" | The mechanism that structurally prevents Columna from establishing a datumwise position. |
| `specs/analytical_governance_v2_page_prose_v0_2.md:389–390` | Columna "**is an executable consequence of**" the category — "**Not the definition of the category, which does not depend on it.**" | Already the anti-closure formulation §C asks for. If a replacement for the retired claim is ever wanted, it exists and is ratified. |
| `apps/website/src/pages/foundations.astro:130–137` | "Underneath the tools are questions nobody has settled… **older than our work and larger than it**." / "Governance cannot be stronger than its account of the thing being governed." | The strongest ideas→system statement on the site — and it never names Columna. |
| `foundations.astro:111` | "There is no datumwise theory of intelligence, and we are not writing one to complete a pattern." | Model of the register. |
| `columna.astro:155–157` | "The public release **consumes** governed authority. It does not provide the authoring and ratification machinery that **produces** it." | The site's one shipped/unshipped boundary, and it is correct. |
| `ladder.astro:117` | "is on our roadmap, **not in the shipped engine**. The ladder grades shipped things." | Exemplary. It is what Chapter 13 should have done. |
| `install.astro:23` | "One command installs **columna-core (the algebra)** and **columna-server (the wire + demo)**" | The only rendered place naming the shipped units separately. |
| `specs/columna_manifold_spec_current.md:3–9` | "As-built reference for `columna-core` `0.15.0-core`… Generated from the code, not from prophecy… a short **§10 Not yet implemented**" | The best-behaved anti-overclaim document in the repo. |
| `specs/doctrine_gaps.md:115` (AW-5) | the retirement of "honest metrics engine" from its last live carriers, with the ratified replacement line | **Precedent**: this exact retirement has been executed once already, cleanly. Whatever §C-style retirement is wanted, this is the pattern. |
| `about.astro:57–60` · `SiteFooter.astro:122` · `Bearing.astro:66,69` | the ruled identity sentence, the general-footer identity line, the bearing | The ruled wording, rendered. |

### 2c · HISTORICAL — leave untouched

| surface | why |
|---|---|
| `specs/context/datumwise_enterprise_plan_v0.2.md` | Four independent staleness markers (baseline v0.7.7-core, "~80% of target", names a `columna-studio` package that does not exist). Contains *"the first metrics engine an AI agent can query"*, *"category-defining engine"*, and *"**Datumwise.ai** — the company surface"* — the last flatly contradicted by current doctrine. **Historical; nothing cites it as live.** |
| `specs/two_pillars_strategy_note_v0_4.md` | Dated 2026-07-19, "nothing here builds before the launch", cites columna-server 0.5.0. Carries the semantic-layer differentiation lines. |
| `specs/wp5_1_site_widget_spec.md:10`, `wp2_3_demo_quickstart_spec.md:29` | "honest-metrics-engine positioning" — already formally retired by `doctrine_gaps.md:115`. |
| `apps/website/src/content/corpus/**` | Frozen deposited editions. `columna_thesis_v0_4.md`, `metadata_independence_essay_v0_2.md`, `launch_announcement_v2.md`, `ladder_page_v0_3.md` carry launch-era category language. **May not be edited** — but see §3a. |
| `specs/baselines/**/external_ai_probes/**` | Third-party descriptions of us; measurements, not positions. |
| `docs/columna_framework_manual_6e.md`, `6f.md` | Prior-edition records per `docs/README.md:8–11`. They carry the same Pro/Cloud text as 6g — but only 6g is normative and rendered. |
| `apps/website/src/data/latest.ts` announcement rows | Dated log entries; retitling falsifies the log (prior ruling). |
| `services/ask/FINDINGS.md`, `eval/results/*` | Dated reports and model outputs. |

---

## 3 · Four questions the audit raises that the ruling does not settle

**(a) Frozen corpus rendered in current editorial voice.** `/thesis` and `/why` render deposited
essays verbatim, and those contain the closest things on the site to the retired closure claim:
*"Columna is our proof that the discipline can be made executable"* and *"The semantic layer was only
ever half the answer. **The other half now exists.**"* The bytes are frozen and must not be edited —
but they render on live routes with no edition pin and no disclosure. Structurally identical to CV-7:
correct as a rendering, misleading as a current statement. **This is the only place "retire from
current voice" collides with "do not edit deposited bytes."**

**(b) `/ladder` exists to be competitor-relative.** A whole ratified page whose stated purpose is
*"how is this different from X?"*, with `/why` and `/the-argument` both pointing at it as the answer
to differentiation questions. §D forbids competitor-relative claims for Columna. Either `/ladder` is
the sanctioned exception — a measuring stick that grades us too, which is how it is written — or it
is now out of doctrine. It cannot be left in the middle.

**(c) "Governed analytical service" already belongs to Analytical Governance.** The ruled Columna
description — *"infrastructure for governed analytical service"* — appears nowhere in the repo, and
its key phrase is currently AG's subject: the deposited current record reads *"Analytical Governance
is the discipline governing the legitimacy of the analytical service"*, and the AG page prose types
Columna as *"an executable consequence of"* that category, explicitly **not** its definition. Adopting
the ruled sentence is coherent — infrastructure *for* a service the category defines — but it puts
Columna and AG in the same noun phrase for the first time. **Worth ruling deliberately rather than
discovering later.**

**(d) One deposited public claim is in tension with the manual.** `open_planner_deposit_v1_3.md:45`
(DOI'd, frozen) states *"There is no SQL anywhere in the system"*; `columna_framework_manual_6g.md:132`
states *"Columna's only contact with the physical layer is SQL used narrowly to extract column-wise
data and metadata"*, and `DuckDBConnector` ships. Both are defensible under different readings of
"in the system", but they are both public. Not a positioning matter — flagged because it surfaced
here and belongs in a reconciliation tranche, not this one.

---

## 4 · What I did not do

- Changed no positioning copy, on any surface.
- Edited no frozen bytes, no deposited record, and no historical document.
- Wrote no replacement wording — the smallest-change column states **scope**, not text.
- Did not reposition anything with reference to Veezoo (§G). No competitor appears in any proposed
  change; the manual and package findings are defects regardless of who else exists.
