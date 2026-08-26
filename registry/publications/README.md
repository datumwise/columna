# The publication registry

**One place a publication fact can come from.** Every DOI, version, date and deposited title the
property asserts as *current* is read from here. Nothing downstream re-types one.

Opened 2026-08-21 (Slice 2 item 1, Phase 1A). Governing rulings: Huayin, 2026-08-21.

---

## Why it exists

On the morning this was built, the property said all of the following at once:

| surface | said The Theory of Data was at | actually |
|---|---|---|
| `/about` | v3.1 — `21760008`, deposited 2026-08-02 | **v6.1 — `22013410`, since 2026-08-19** |
| `llms.txt` (read first by every retrieval system) | v1.0 — `21707018` | ″ |
| `docs/columna_framework_manual_6g.md` (current manual) | v3.1 and v4.0 | ″ |

and the footer of **every page** cited *The Two Anchors of a Measure* v1.0, ten days after v2.0 was
deposited; and `/about` cited *The Open Planner* v1.0 and the *Foundations Note* v1.0, each one
version behind. Four stale current DOIs on one page, and no two surfaces agreeing.

None of that was carelessness. Every one of those entries carried a careful source comment explaining
its ordering and its wording, and none of the comments were wrong — **the DOIs were.** That is the
finding: a fact which must be re-typed to stay true will eventually be false, and a list that
documents its own editorial reasoning in the margin reads as maintained long after it stopped being.
The defect was architecture, and it is fixed architecturally or not at all.

---

## The model

```
Work                                    Record
────                                    ──────
workId            locally minted        recordId      locally minted
canonicalLabel    editorial name        workId        the work it deposits
kind              corpus classification title         the EXACT deposited title of THIS version
attachedConcepts  external, 1..n        version, date, doi, recid
  [{recid, doi}]  (empty if never       status        current | superseded
                   deposited)           authors, license, resourceType
                                        supersedes?   a recordId, in the same work
```

### `workId` ≠ Zenodo concept

> A later deposit **attaches** an external concept identity to an existing datumwise work.
> It does not change the work's internal identity.

Every work gets a locally minted, permanent `workId` — including works that have never been
deposited. The Zenodo concept record is *authoritative evidence* for grouping version records into
one work; it is not the thing that creates the work. Two consequences, both deliberate: a work can
exist before it is deposited and acquire its DOIs later without an identity migration, and the corpus
does not depend structurally on Zenodo remaining the deposit provider forever.

### One work, many attached concepts

> **One Work may attach one or more Zenodo concept identities over its publication history.**
> (Huayin, ruling of 2026-08-21, Phase 3B.1.)

The first cut of this model gave a work exactly one concept, and this corpus falsified that twice
within a day of the sweep that looked:

- **The Silent Failure Atlas** was deposited as v1.2 under concept `20710592` and, three days later,
  as v1.3 under a **new** concept `20762838` — not as a new version of the first. One work, two
  concepts. Under a single-valued field it was unrepresentable: filing v1.2 under the Atlas broke G4,
  and filing it as its own work asserted there are two Atlases.
- **The Two Great Sources of Silent Analytical Failure** acquired a retitled successor — *Three
  Structural Sources*, v2.0 — deposited under its own concept while declaring `isNewVersionOf` the
  earlier record in its own Zenodo metadata. Under the old model, `/about` and `llms.txt` would have
  gone on rendering the superseded record as current, and **the registry could not have expressed the
  repair.**

Neither is a mistake anyone made in this repo. Both are ordinary things to do at a deposit provider,
and a model that cannot hold them is the thing that is wrong.

So the field is a list, `attachedConcepts`, in first-deposit order — and the invariants are narrow:

```
record.conceptRecid ∈ work.attachedConceptRecids           G4
one concept is attached by at most ONE work                G1
an attachment must be witnessed by ≥1 record of the work   G4
```

**Currentness did not move.** It is governed `status` on the Record and nothing else — not concept,
not attachment order, not version string, date, or DOI magnitude. Supersession **may** cross attached
concepts inside one work; G3 is unchanged, because it always said *inside a work*, and a concept was
never what a work is.

**The local id does not follow the title.** `w-two-great-sources` keeps its workId although its
current deposit is titled *Three Structural Sources*. That reads strangely on purpose. The slug is a
mnemonic, no code parses it, and renaming internal identity to track an external title is the exact
coupling this registry exists to break. `canonicalLabel` — which *is* editorial naming — did change.

The old scalar `conceptRecid` / `conceptDoi` are **gone, not deprecated**. Every reader moved in the
same commit. A compatibility shim would have been a second way to ask the same question, which is how
the stale-DOI problem started.

The same principle governs `recordId`. Internal reference integrity — `supersedes`, every lookup, every
selection — runs on locally minted ids. **Nothing parses a DOI string**, and `check_publications.py`
G6 fails the build if an id ever embeds one. The slug inside an id is a mnemonic for humans; no code
reads it.

### The exact title is record-level

Not stable across versions, and in this corpus provably not. One work, `w-theory-of-data`, has been
deposited as:

- *The Theory of Data — Particles, Atoms, Anchors, Universes, and Lawful Transformation* (v1.0, v3.1)
- *The Theory of Data: Governed Analytical Objects, Lawful Transformation, and Certification* (v4.0)
- *The Theory of Data: A Foundational Framework for Governed Analytical Data…* (v5.0)
- *The Theory of Data* (v6.0, v6.1)

and its resource type changed too (v5.0 was deposited as a *Working paper*, everything else as a
*Preprint*). Authors and licence sit on the Record for the same reason: they *may* vary between
versions, so the version is where they belong.

The Work carries only `canonicalLabel` — the site's short name for the thing. That is **editorial
naming, not a publication fact**, and it is the only publication-adjacent string on this property
still chosen by a person.

### A theory's name and a paper's title are different facts (Huayin, 2026-08-26)

`canonicalLabel` is how the corpus **cites the work**, so it follows the current record's deposited
title. It is not the name of the idea, and the two must be allowed to come apart:

> Theory of Certainty is still valid, except when citing the article, the title needs to match the
> new paper. **Not all Theory of Relativity are in books titled Theory of Relativity.**

The ruling came from a live case. *The Theory of Certainty* v1.0 was superseded the same day it was
deposited by *The Ground for Certainty* v1.1 — the title changed because that one concise paper
examines the grounds on which reliance rests, and calling it "The Theory of Certainty" made it sound
more comprehensive than intended. The theory kept its name. The paper did not.

So a supersession that renames moves exactly two things: the `canonicalLabel`, and every surface that
**cites the article**. It does not move prose that names the theory, the discipline or the account.
On `/analytical-governance` both appear, one screen apart, and the difference is visible in the
markup: §Legitimacy says *"developed separately in {certainty.label}"* — a citation, registry-derived,
now reading **The Ground for Certainty** — while the §Where this sits relation row is headed **The
Theory of Certainty** under the relation *supplies the upstream discipline to*, because that row names
the discipline. Its `href` is still registry-derived, so it lands on the current record. Anchor text
that names a theory over a target that resolves to its current foundational publication is what a
citation to a theory has always looked like; it is not drift.

The failure this prevents is a mechanical rename: a find-and-replace across the corpus would have
retitled the idea in every sentence that discusses it, including sentences inside deposited papers
that are frozen by definition. The gate cannot catch that one, because a theory's name is not a
Zenodo token. It is caught by classifying each occurrence before editing any of them.

### `kind` is deliberately ungoverned

Every work reads `kind: "unclassified"`, and that is load-bearing. `llms.txt` used to open its
evidence section with *"The nine papers, chronological"* — a hand-typed number beside a hand-typed
list. The tempting repair is `count(distinct doi)`, which is refused: records, works, papers,
program notes, primers, introductions, positions and a technical supplement are **not the same
counting unit**, and no governed definition says which of them the word "papers" ranges over. 74
records across 32 works is not "32 papers". Replacing a stale magic number with a freshly computed
wrong one is laundering, not migration.

So the claim was dropped rather than recomputed, and the drop is enforced: G10 fails the build if a
count-of-publications claim appears on a derived surface while any work is unclassified. When the
corpus classification is ruled, `COUNTS_ARE_DERIVABLE` flips and the sentence becomes one the registry
can defend — and not one minute before.

---

## The files

| file | what it is | authored by |
|---|---|---|
| `works.json` | 32 works: id, label, kind, attached concept identities (1..n) | **hand** (the only editorial file) |
| `records.json` | 74 deposited versions, every bibliographic field | `mint_publication_records.py` |
| `zenodo_snapshot_2026-08-21.json` | frozen evidence: what Zenodo said, on a date | `harvest_zenodo_snapshot.py` |
| `consumers.json` | every file in the repo that names a DOI, and on what terms | hand, checked mechanically |
| `reconciliation.json` | known discrepancies and retired identifiers | hand |
| `extra_seeds.txt` | ids the registry must cover that no file cited yet | hand |

**A frozen snapshot, not a live call.** A gate that reaches the network fails on someone else's
outage and passes on someone else's cache. This one is hermetic, and the evidence is reviewable *in
the diff*: when a publication fact changes, it changes as bytes, with a date on it, not as a silent
difference between two CI runs. `check_publications.py --live` re-verifies against Zenodo on demand.

---

## Coverage: what this registry does NOT model

**Closed under versioning is not closed under deposit.** The harvester seeds from what the repo
*cites*, then expands each seed's concept to all of its versions, so no version of a modeled work can
go missing. Nothing in that loop can find a work **nobody has cited yet** — and on 2026-08-21 that was
the entire Statistical Bridge corpus: nine works, seventeen deposited versions, no stale DOI and no
wrong DOI, simply absent. Absence is the one defect a scan of what the repo already says cannot find.

So coverage is measured rather than assumed:

```sh
python scripts/harvest_zenodo_snapshot.py --coverage
```

A creator sweep against Zenodo, minus the concepts `works.json` claims. It **reports**; it never
seeds, never writes, and is never in CI — it reaches the network, and naming a work is editorial.

As of 2026-08-21 the sweep reports **34 concepts across 32 works, 0 uncovered** — but *closed* is a
state, not a property: the next deposit re-opens it, and `34/34` is a reading taken on a date, never a
constant to be asserted. An uncovered concept is not automatically an error either. Onboarding one
means **naming** a work, or **attaching** a concept to a work that already exists — the same editorial
act in two shapes, and neither is done by a script. Known-and-declined entries live in
`reconciliation.json` and are argued in `specs/publication_corpus_coverage_v0_1.md`. **Read those
before treating a coverage line as news.**

---

## Reconciliation is not bibliography

Kept adjacent to the records, and conceptually apart from them.

> **The record says what the publication is. The reconciliation data says where stale or erroneous
> assertions are historically permitted, or currently forbidden.**

A `Record` is never contaminated with the claim that its DOI is somehow "wrong" because a frozen file
misquoted it. The worked example is `rc-open-planner-v13-doi`: the deposited program note's own byline
says *"Version 1.3 … DOI: 10.5281/zenodo.21632723"*, and `21632723` is v1.0 — v1.3 is `21695710`.

- The **deposit is not touched.** Its bytes are the record of what was published, defects included. A
  defect in a deposit is fixed at the deposit or not at all.
- The **README beside it was corrected**, because it is a current document making a current claim.
- The registry models `21632723` as **v1.0**, which is what it is.
- The reconciliation item grants the exception **to the file, never to the claim** — so a checker that
  tolerates the token there cannot conclude that `21632723` *is* the v1.3 record. G9 asserts the
  opposite explicitly, and fails if the registry ever adopts the deposit's belief.

Historical-artifact truth and current bibliographic truth are different registers. This directory
keeps them in different files.

---

## Consumer classes

Every file in the repo that names a Zenodo DOI is classified. An unclassified one **fails the build** —
a new hand-authored publication fact must be declared, not merely appear.

| class | rule | examples |
|---|---|---|
| `derived` | carries **zero** literal DOIs; reads the registry | `/about`, the page footer, `/ladder`, the `llms.txt` index |
| `frozen-deposit` | the published artifact itself; bytes are the record | `open_planner_deposit_v1_3.md` |
| `frozen-corpus` | ratified byte-frozen corpus piece (ledger P1) | the position papers, the corpus map |
| `frozen` | dated capture, superseded edition, historical artifact | the AI probe baselines, manual 6f, the prototype |
| `edition-pinned` | cites the DOI of the edition it renders verbatim — *not* the current one | `/learn/*`, `/positions/*` |
| `ledger` | internal tracking document | `doctrine_gaps.md`, the Slice 2 ledger |
| `acceptance` | the gate's own ruling assertions; literal on purpose | `check_publications.py` |
| `manual-deferred` | hand-authored, currency-bearing, **owed** | manual 6g, `/benchmark`, `/analytical-governance` |

`edition-pinned` is the class that stops this system from being stupid. `/learn/what-is-the-theory-of-data`
renders the v1.1 bytes of *The Theory of Data: An Introduction* and cites v1.1's DOI while v2.2 is
current. That is **correct**: citing v2.2 above v1.1's bytes would be the misattribution. Currency is
not a virtue everywhere — it is a property that current-facing surfaces owe and frozen ones do not.

---

## What the gate cannot do

It does not decide whether a citation is *semantically* appropriate. An edition-pinned page citing its
own deposited edition and a stale page citing a superseded record are byte-identical to a scanner.
The decidable layer is enforced here; the rest is a human review gate, and pretending otherwise would
manufacture false confidence (Slice 2 ledger §0). Ten gates, `G1`–`G10`, documented at the top of
`scripts/check_publications.py`; each one has a negative test that was run before it shipped.

---

## Adding a deposit

```sh
python scripts/harvest_zenodo_snapshot.py --out registry/publications/zenodo_snapshot_<date>.json
python scripts/mint_publication_records.py          # mints ids; never renumbers; prints currency changes
python scripts/check_publications.py --report
```

A brand-new **work** is refused by the minter and must be added to `works.json` by hand. Deciding that
a set of deposits is one intellectual object, and what the corpus calls it, is the one genuinely
editorial act in this system, and it does not get automated.
