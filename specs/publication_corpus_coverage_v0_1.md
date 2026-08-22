# Publication corpus coverage — v0.1

**Ledger. Not publication authority.** Every current bibliographic fact lives in
`registry/publications/`. This document records how coverage is measured, what it found, and what
remains open. Class `ledger` in `registry/publications/consumers.json`.

Opened 2026-08-21 (Phase 3B, the Evidence publication foundation).
Closed to zero uncovered concepts 2026-08-21 (Phase 3B.1, publication identity closure).

---

## 1. Why this file exists

The registry grew from what the property **cites**: the harvester seeds itself from every Zenodo id in
a tracked file, plus `extra_seeds.txt`, then expands each seed's concept to all of its versions. That
is closed under versioning and closed under citation. It is **not** closed under *deposit* — a work
nobody has cited yet is a work the registry has never heard of.

Phase 3B proved the gap is not hypothetical: nine works and seventeen deposited versions of the
Statistical Bridge corpus existed entirely on Zenodo and entirely outside the registry, cited by not
one tracked file. Nothing was stale; nothing was wrong. The defect was **absence**, which is precisely
the defect a scan of what the repo already says can never find.

So coverage gets measured, and what it finds gets written down here.

---

## 2. How coverage is measured

```sh
python scripts/harvest_zenodo_snapshot.py --coverage
```

A **creator sweep**: every latest-version record Zenodo attributes to the corpus creator, resolved to
its concept, minus the concepts `works.json` attaches. What remains is the uncovered set.

**A correction to a claim this repo used to make.** `harvest_zenodo_snapshot.py` said, in its own
docstring, that a creator sweep was not available — *"a query for 'Huayin Wang' returns zero hits,
verified 2026-08-21"*. That observation was accurate and the conclusion drawn from it was wrong:

```
q=metadata.creators.person_or_org.name:"Wang, Huayin"     → 34 latest-version records
q="Huayin Wang"                                            → 0
```

One spelling of the question had been tested and its answer recorded as a property of the world.
(Compare the G7 widening of the same day: *a scanner that reads one spelling of an identifier does not
audit identifiers, it audits a spelling.* Same mistake, one layer out.)

**What the sweep is not.** Report-only, by ruling. It never seeds, never writes registry state, never
decides intellectual identity, and is not a CI dependency — it reaches the network, and a gate that
reaches the network fails on someone else's outage. A record's mere existence at Zenodo does not make
it authority for anything; attaching or naming it is editorial.

### 2.2 Where the brief and the deposit disagreed — the deposit won

The Phase 3B.1 brief gave the current publication of record for case 2 as:

> Three Structural Sources of Silent Analytical Failure: **Anchor, Universe, and Regime**

The deposit carries **no subtitle**. Zenodo record `21893929`, resolved live on 2026-08-21, has
`metadata.title == "Three Structural Sources of Silent Analytical Failure"`. The subtitle is a true
description of the paper's content — anchor, universe and regime are exactly its three sources — and
it is not part of the deposited title, so it is not the Record's title. The brief said *"do not use
this message as bibliographic authority"*, and this is the case where that instruction did work.
`G9` now asserts the exact deposited string, so the discrepancy cannot be re-introduced by hand.

(The resource type moved too: the superseded record was deposited as a *Preprint*, the successor as a
*Working paper*. Record-level, like the title, and for the same reason.)

---

## 3. Coverage as of 2026-08-21, after Phase 3B.1

```
creator sweep      34 latest-version records → 34 concepts
works.json         34 concepts across 32 works
uncovered          0
```

**Closed is a state, not a property.** The next deposit re-opens it, and `34/34` is not a guarantee —
it is a reading taken on a date. The sweep is re-run after deposits, and the number it reports is
whatever Zenodo says at the time; it is never asserted as a constant.

Every one of the 32 works' current records equals Zenodo's latest version for its attached concepts,
verified record by record. **No stale current authority anywhere in the registry.**

---

## 4. The model change that closed it

> **One Work may attach one or more Zenodo concept identities over its publication history.**
> (Huayin, ruling of 2026-08-21.)

A datumwise `Work` is the governed intellectual identity. A Zenodo concept is an **attached external
publication identity** — one of possibly several the work acquires. `works.json` carries
`attachedConcepts: [{recid, doi}]`, in first-deposit order; empty for a work never deposited.

```
one datumwise Work identity
one Work attaches 1..n Zenodo concept identities

one Record  → exactly one datumwise Work
            → exactly one concrete Zenodo concept

record.conceptRecid ∈ work.attachedConceptRecids          (G4)
one concept is attached by at most ONE work               (G1)
an attachment must be witnessed by ≥1 record of the work  (G4)
```

**Currentness did not move.** It is governed `status` on the Record and nothing else — not concept,
not attachment order, not version string, not date, not DOI magnitude. Supersession **may** now cross
attached concepts inside one work, and G3 is unchanged: edges still stay inside a *work*.

### 4.1 Case 1 — *The Silent Failure Atlas*, one work under two concepts

```
concept 20710592  →  20710593  v1.2  2026-06-16   "…: A Taxonomy of Silent Analytical Failures in Data Analysis"
concept 20762838  →  20762839  v1.3  2026-06-19   "…: A Taxonomy of Silent Analytical Failures in Data Analysis (v1.3)"
```

v1.3's own Zenodo description reads *"New addition of MIN/MAX pattern, updated from v1.2"*. Both
concepts attach to the existing `w-silent-failure-atlas`; **no second Atlas work was created**. The
chain is `r02 (v1.2) → r01 (v1.3, current)` — and note the ids: the *earlier* deposit carries the
*later* recordId, because ids are minted, never renumbered. The current record is v1.3, the same
answer as before the ruling, now for a reason the registry can state rather than a gap it could not.

The rendered consequence: the Atlas now has two records, so `versionTag` resolves for the first time
and `/about` and `llms.txt` read *"The Silent Failure Atlas — v1.3"*. Its DOI did not change.

### 4.2 Case 2 — *Two Great Sources* → *Three Structural Sources*, across concepts

```
concept 21553378  →  21553379  (unversioned)  2026-07-25  "The Two Great Sources of Silent Analytical Failure"
concept 21893928  →  21893929  v2.0           2026-08-11  "Three Structural Sources of Silent Analytical Failure"
```

`21893929` declares `isNewVersionOf 10.5281/zenodo.21553379` in its own Zenodo metadata. Ruled: one
work, two concepts, one chain. `r02 (v2.0)` is current and supersedes `r01`, which stays first-class
and historical.

**The workId did not change.** `w-two-great-sources` still names a work whose current deposit is
titled *Three Structural Sources*. That reads strangely on purpose: the slug is a mnemonic, no code
parses it, and renaming internal identity to track an external title is the exact coupling this
registry exists to break. The `canonicalLabel` — which *is* editorial naming — did change, to
*Three Structural Sources of Silent Analytical Failure*.

**Not one citation was mechanically currentized.** Nine tracked files name `21553379` and all nine are
right to:

| file | class | why it keeps the superseded DOI |
|---|---|---|
| 4 × `content/corpus/*.md` | `frozen-corpus` | ratified byte-frozen editions |
| `data/latest.ts` | `manual-deferred` | a dated announcement log — *"2026-07-25"* is true as a log entry and would be **falsified** by pointing it at v2.0 |
| `positions/the-two-great-sources-…astro` | `edition-pinned` | renders the v1.1 bytes; citing v2.0 above them would be the misattribution |
| `docs/tools/link_checking.md` | `manual-deferred` | a `curl` example; makes no publication claim |
| `prototype/index.html` | `frozen` | historical artifact |
| `scripts/check_publications.py` | `acceptance` | the gate's own assertions, literal on purpose |

What changed is the two `derived` surfaces, and they changed **with no edit to any page**: `/about`
and `llms.txt` re-derived to *Three Structural Sources … v2.0 … doi:10.5281/zenodo.21893929* because
they read status, not text. That is the whole thesis of this registry, executed once, in public.

### 4.3 Case 3 — two clean identities claimed

| work | current | versions | concept |
|---|---|---|---|
| `w-frameql-primer` — *A Primer on Frame-QL* | v2.0 `10.5281/zenodo.21960873` | 3 | 21888997 |
| `w-data-has-its-own-ontology` — *Data Has Its Own Ontology* | v1.1 `10.5281/zenodo.22026962` | 2 | 22003682 |

Both chains single-concept and monotonic. **No pillar assignment is implied**: `kind` is
`unclassified` for all 32 works, so registration expresses no opinion about where either belongs.

### 4.4 Case 4 — a malformed external identifier, unchanged

Record `21960873` carries `related_identifiers[0].identifier =
"10.5281/zenodo.2188899810.5281/zenodo.21888998"` — two DOIs concatenated, resolving 404. The second
instance of this defect class (`rc-primer-v22-related-identifier` is the first), and what a
**prepend-instead-of-replace** edit produces in Zenodo's related-identifiers editor. Repairable only
at the deposit. It costs one unresolved seed per harvest and is recorded, not compensated for.

---

## 5. What was deliberately NOT added

**No citation edges.** The Evidence corpus is densely cross-cited — *The Two Jobs of the Conditioning
Bar* names five sibling records in its own front matter — and modelling that graph stays refused. The
registry governs publication **identity and currentness**, and answers the four questions a derived
surface asks:

```
what is current?                                → status, exactly one per work
what supersedes what?                           → supersedes, by recordId, within a work
what work does this record belong to?           → workId
what may a derived surface render as current?   → currentRecord(workId)
```

Recorded as future capability. Nothing on the site needs it.

**No scalar concept field kept for cosmetic continuity.** `conceptRecid` / `conceptDoi` are gone, not
deprecated. Every reader — the gate, the minter, the harvester, the typed site adapter — moved in the
same commit. A compatibility shim would have been a second way to ask the same question, which is how
the stale-DOI problem started.

---

## 6. Open items

| id | item | state |
|---|---|---|
| CV-1 | Atlas v1.2 unmodeled | **CLOSED** 3B.1 case 1 — both concepts attached |
| CV-2 | *Three Structural Sources* successor across concepts | **CLOSED** 3B.1 case 2 — ratified, current, derived surfaces re-derived |
| CV-3 | *A Primer on Frame-QL*, *Data Has Its Own Ontology* uncovered | **CLOSED** 3B.1 case 3 — both claimed |
| CV-4 | Frame-QL Primer v2.0 related identifier malformed at the deposit | **OPEN** — an edit on Zenodo; nothing in this repo can fix external metadata |
| CV-5 | Evidence-pillar membership of *Regression Has an Anchor* and *Regime Has a Contract* | **OPEN** — editorial review; registration implies nothing |
| CV-6 | `/analytical-governance` names *The Statistical Bridge* as a neighbour with no link | **CLOSED** Phase 3C — the neighbour resolves to `/evidence`, the argument, not to the deposit |
| CV-7 | the live route `/positions/the-two-great-sources-of-silent-analytical-failure` and its page title name the superseded account | **OPEN** — correct as an edition-pinned rendering of the v1.1 bytes; whether the ROUTE should follow the retitled successor is editorial, and publication foundation does not get to answer it |
| CV-8 | corpus `kind` ungoverned for all 32 works, so no surface may state a count | **OPEN by design** — G10 enforces it |
| CV-9 | **“jurisdiction” is carrying two meanings.** `/evidence` states that Evidence is *a standing acquired through a governed crossing, not a sovereign jurisdiction*; the homepage's `ThreeQuestions` source comment calls Data · Evidence · Intelligence *“different JURISDICTIONS, not three planes of one lattice.”* Both are defensible and they are not the same word-sense: the homepage means **jurisdiction-of-law/question** — which body of law answers this question — while `/evidence` denies **Evidence-as-sovereign-province**, a region of the world with its own territory. | **OPEN, editorial, not a blocker.** Logged 2026-08-22 (Huayin, PR #194 review §4): the homepage is NOT changed. A future ruling should separate the two senses explicitly rather than let the shared word imply that Evidence is a sovereign world. Recorded here so the tension is inherited deliberately instead of rediscovered as a contradiction between two live surfaces. |
