# Publication corpus coverage — v0.1

**Ledger. Not publication authority.** Every current bibliographic fact lives in
`registry/publications/`. This document records what the registry does **not** yet cover, and why —
including two cases the registry's data model cannot currently represent at all.

Opened 2026-08-21, Phase 3B (the Evidence publication foundation). Class `ledger` in
`registry/publications/consumers.json`.

---

## 1. Why this file exists

The registry has never claimed to model the whole deposited corpus. It grew from what the property
**cites**: the harvester seeds itself from every Zenodo id in a tracked file, plus `extra_seeds.txt`
for ids that were ruled on but never written down. That is closed under versioning and closed under
citation. It is **not** closed under *deposit* — a work nobody has cited yet is a work the registry
has never heard of.

Phase 3B proved that gap is not hypothetical. Nine works and seventeen deposited versions of the
Statistical Bridge corpus existed entirely on Zenodo and entirely outside the registry, cited by not
one tracked file. Nothing was stale; nothing was wrong. The defect was **absence**, and absence is
precisely the defect a scan of what the repo already says can never find.

So coverage now gets measured, and what is measured gets written down here.

---

## 2. How coverage is measured

`python scripts/harvest_zenodo_snapshot.py --coverage`

A **creator sweep**: ask Zenodo for every latest-version record it attributes to the corpus creator,
resolve each to its concept, and subtract the concepts `works.json` already claims. What remains is
the uncovered set.

**A correction to a claim this repo used to make.** `harvest_zenodo_snapshot.py` said, in its own
docstring, that a creator sweep was not available — *"a query for 'Huayin Wang' returns zero hits,
verified 2026-08-21"*. That observation was accurate and the conclusion drawn from it was wrong. The
free-text query does return zero. The **fielded** query does not:

```
q=metadata.creators.person_or_org.name:"Wang, Huayin"     → 34 latest-version records
q="Huayin Wang"                                            → 0
```

The sweep was available the whole time; the repo had tested one spelling of the question and recorded
the answer as a property of the world. (Compare the G7 widening of 2026-08-21: *a scanner that reads
one spelling of an identifier does not audit identifiers, it audits a spelling.* Same mistake, one
layer out.) The docstring is corrected and the sweep is now a flag.

**What the sweep is not.** It is a *reporting* mode. It never seeds, never writes the snapshot, and
never adds a work — naming a work is editorial and stays editorial. It is also not part of CI: it
reaches the network, and a gate that reaches the network fails on someone else's outage.

---

## 3. Coverage as of 2026-08-21

Creator sweep: **34** latest-version records → 34 Zenodo concepts.
Registry after Phase 3B: **30 works**, 67 records.
Every one of the 30 works' current records equals Zenodo's latest version for its concept — verified
record by record. **No stale current authority anywhere in the registry.**

### 3.1 Onboarded by this unit (9 works, 17 records)

| work | current | concept |
|---|---|---|
| `w-statistical-bridge` | v3.0 | 21795311 |
| `w-statistical-bridge-primer` | v2.0 | 21864433 |
| `w-where-does-probability-live` | v1.0 | 21977941 |
| `w-certifiable-state` | v1.0 | 21972540 |
| `w-reading-rethinking` | v2.0 | 21863558 |
| `w-reading-bayesian-workflow` | v1.0 | 21983507 |
| `w-conditioning-bar` | v1.0 | 22010142 |
| `w-regression-has-an-anchor` | v2.0 | 21783728 |
| `w-regime-has-a-contract` | v1.0 | 21840853 |

The first seven are the Evidence pillar as its own texts constitute it. The last two are
**Bridge-crossing and held for membership review**: both rebuild a statistical object across the
boundary between the Theory of Data and the Statistical Bridge, and either could reasonably be called
an Evidence work or a Theory-of-Data work. Onboarding them settles their **publication identity** and
settles nothing else — `kind` is `unclassified` for all thirty works, so the registry expresses no
opinion about pillar membership and cannot be read as having expressed one.

### 3.2 Uncovered, clean, awaiting a naming ruling (2 works)

Neither is an Evidence work; both are one line of `works.json` away whenever they are wanted.

- **A Primer on Frame-QL** — concept `21888997`; three versions, current v2.0
  (`10.5281/zenodo.21960873`). See §4.3: its Zenodo metadata carries a malformed related identifier.
- **Data Has Its Own Ontology** — concept `22003682`; two versions, current v1.1
  (`10.5281/zenodo.22026962`). A positioning companion to *The Theory of Data* v6.1.

### 3.3 Uncovered and NOT representable in the current model (2 cases)

Both are recorded as reconciliation items. Both are **blocked on an architectural ruling, not on
data**, and neither is touched by this unit. See §4.

---

## 4. What the Evidence sweep exposed about the model

The Evidence corpus itself is clean: nine works, nine concepts, every version chain single-concept
and monotonic, no ambiguous DOI chain, no supersession puzzle. **The model gaps below were found by
the corpus sweep, not by the Evidence corpus.** They are reported here rather than repaired, per the
standing rule that a model weakness stops the unit instead of widening the schema inside it.

### 4.1 One work, two Zenodo concepts — *The Silent Failure Atlas*

```
concept 20710592  →  20710593  v1.2  2026-06-16  "The Silent Failure Atlas: A Taxonomy…"
concept 20762838  →  20762839  v1.3  2026-06-19  "The Silent Failure Atlas: A Taxonomy… (v1.3)"
```

v1.3's own Zenodo description reads *"New addition of MIN/MAX pattern, updated from v1.2"*. These are
two deposits of one intellectual object under **two separate concept records** — v1.3 was deposited
fresh rather than as a new version of the existing concept.

The registry models only `20762838`, so v1.2 is an unmodeled version of a modeled work.

**Why it cannot simply be added.** `Work.conceptRecid` is single-valued, and G4 fails any record whose
snapshot concept differs from its work's declared concept. So:

- filing v1.2 under `w-silent-failure-atlas` → **G4 fails** (concept mismatch);
- filing it as its own work → asserts something false: that there are two Atlases;
- leaving it out → the current state, which is at least not a lie, but the registry silently does not
  know about a deposited version of a work it does model.

The ruling this needs is whether a Work may **attach more than one concept identity**. The existing
doctrine already points that way — *"a later deposit ATTACHES an external concept identity to an
existing datumwise work"* — and a set-valued attachment is a small change to `works.json`, G1 and G4.
It is a schema change, so it is not made here.

Cross-reference: *The Silent Seam* (`10.5281/zenodo.20710717`) declares `isSupplementTo`
`10.5281/zenodo.20710593` — the v1.2 record, in the uncovered concept. The site's footer pairs the two
works and is unaffected: it derives from the registry and cites v1.3.

### 4.2 A retitled successor in a new concept — *Two Great Sources* → *Three Structural Sources*

```
concept 21553378  →  21553379  (unversioned)  2026-07-25  "The Two Great Sources of Silent Analytical Failure"
concept 21893928  →  21893929  v2.0           2026-08-11  "Three Structural Sources of Silent Analytical Failure"
```

`21893929` (`10.5281/zenodo.21893929`) declares, in its own Zenodo metadata, `isNewVersionOf` `10.5281/zenodo.21553379`, and calls
itself **version 2.0**. That is an explicit, machine-readable supersession claim that **crosses a
concept boundary** — the successor was deposited as a new concept, and its title changed with the
argument (two sources became three: anchor, universe, regime).

**This is a live consequence, not a curiosity.** `w-two-great-sources` is a member of
`CHRONOLOGICAL_SELECTION`, so `/about` and the `llms.txt` inventory render `21553379` as the current
record of that work today. If the successor claim is ratified, that is stale current authority on two
derived surfaces — the exact class of defect the registry was built to end — and the registry
currently **cannot express the repair**: G3 requires supersession edges to stay inside one work, and a
work may hold only one concept.

Three candidate readings, none of them ours to pick:

1. **One work, two concepts, one chain** — v2.0 supersedes the 2026-07-25 deposit. Needs §4.1's
   multi-concept attachment, and then falls out for free.
2. **Two works, related** — a distinct paper that supersedes an argument rather than a version. Needs
   a *relationship* edge between works, which the model deliberately does not have (§5).
3. **Deposit defect** — `isNewVersionOf` was asserted where a `references`/`isSupersededBy` relation
   was meant, in which case nothing changes in the registry and the item retires.

Until one of the three is ruled, `/about` continues to render `21553379`. That is recorded, not
hidden — which is the whole point of this file.

### 4.3 Malformed external identifier — *A Primer on Frame-QL* v2.0

Record `21960873` carries `related_identifiers[0].identifier =
"10.5281/zenodo.2188899810.5281/zenodo.21888998"` — two DOIs concatenated with no separator, the
identical defect class as `rc-primer-v22-related-identifier` (*A Primer on the Theory of Data* v2.2).
A second instance makes it a pattern rather than a slip: it is what a **prepend-instead-of-replace**
edit produces in the Zenodo related-identifiers editor. Repairable only at the deposit.

---

## 5. What this unit deliberately did NOT add

**No citation edges.** The Evidence corpus is densely cross-cited — *The Two Jobs of the Conditioning
Bar* names five sibling records in its own front matter — and modelling that graph was refused. The
registry's job is publication **identity and currentness**, and it already answers the four questions
a derived surface actually asks:

```
what is current?                                  → status, exactly one per work
what supersedes what?                             → supersedes, by recordId, within a work
what work does this record belong to?             → workId
what may a derived surface render as current?     → currentRecord(workId)
```

A general bibliographic relation model would be a second, much larger system, and nothing on the site
needs it yet. Recorded as **future capability**, and as the thing §4.2's reading 2 would require.

**No surface changes.** No page, selection or copy was touched. `/about` and `llms.txt` still render
the same ten curated works; the nine new works are governed and uncited, which is the correct state
for a foundation laid before the surface that will stand on it.

---

## 6. Open items

| id | item | blocked on |
|---|---|---|
| CV-1 | Atlas v1.2 in concept `20710592` is an unmodeled version of a modeled work | multi-concept attachment ruling (§4.1) |
| CV-2 | *Three Structural Sources* claims `isNewVersionOf` the *Two Great Sources* deposit, across concepts | ruling among §4.2's three readings |
| CV-3 | *A Primer on Frame-QL* and *Data Has Its Own Ontology* uncovered | a naming ruling; one line each |
| CV-4 | Frame-QL Primer v2.0 related identifier is malformed at the deposit | an edit on Zenodo; nothing in this repo can fix it |
| CV-5 | Evidence-pillar membership of *Regression Has an Anchor* and *Regime Has a Contract* | editorial review (§3.1) |
| CV-6 | `/analytical-governance` names *The Statistical Bridge* as a neighbour with no link | Phase 3C decides whether the target is `/evidence` or the DOI |
