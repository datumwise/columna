# The Ground for Certainty v1.1 — reconciliation, typed authority, and historical reachability

Run 2026-08-26 under the post-F ruling. Scope as ruled: reconcile the new current record, correct the
bounded identity/currency retrieval defect, demonstrate historical reachability, correct the public
view count, run only the targeted checks the new event materially affects. **F was not re-run.**
Nothing outside that was touched.

Total model spend in this tranche: **$0.343** (two targeted evaluation runs; everything else is
deterministic and costs nothing).

---

## 1 · Verified Zenodo facts for v1.1, as actually found

Read from `zenodo.org/api/records/22118479` and frozen into
`registry/publications/zenodo_snapshot_2026-08-26.json`. Nothing here was typed from the message.

| field | as found |
|---|---|
| recid | `22118479` |
| DOI | `10.5281/zenodo.22118479` |
| **concept** | conceptRecid `22114801` (its concept DOI is the 10.5281/zenodo form of that recid) |
| title | `The Ground for Certainty` |
| version | `1.1` |
| publication date | `2026-08-26` |
| **resource type** | `Working paper` (`publication` / `workingpaper`) |
| licence | `cc-by-4.0` |
| creator | `Wang, Huayin` — datumwise, an independent open-source research project |
| relation | `isNewVersionOf` → `10.5281/zenodo.22114802` |
| files | `the_ground_for_certainty_v1_1_zenodo_22118479.md` — 26 239 bytes, **md5 `b265135ebaa4c006a2deb18518b78cf1`** · `…​.pdf` — 84 692 bytes, md5 `bd008cf08c67965de40c188a40d952e6` |

**The concept is the same one v1.0 carries.** So this reconciles as a normal new version inside
`w-theory-of-certainty` — the shape F3 tested — and NOT as a retitled successor deposited under a new
concept, which is the shape Two Great Sources → Three Structural Sources took. The distinction was
checked rather than assumed, because the two look identical from the message and are modelled
differently.

The deposit was fetched and its md5 verified against Zenodo's own before it entered the tree. The
snapshot delta is **one record and one version count** (concept `22114801` versionCount 1 → 2). No other
bibliographic fact moved anywhere in the corpus.

**The harvester found the new record without being told about it.** Seeds are scraped from what the
repo cites, and nothing in the repo cited `22118479` yet; it arrived by expanding the concept to all
of its versions. That is the "closed under versioning" property doing the job it was built for.

---

## 2 · Registry / deposit / Core / historical delta

| layer | change |
|---|---|
| `records.json` | `w-theory-of-certainty.r02` **minted current** — The Ground for Certainty, v1.1, `22118479`, `supersedes: w-theory-of-certainty.r01`. `.r01` → **`superseded`**, keeping its own deposited title, `The Theory of Certainty` |
| `works.json` | `canonicalLabel` → **The Ground for Certainty**. `workId` untouched |
| `sources.json` | new `s-theory-of-certainty-v1-0`, `role: historical-record`, pinned to `.r01`, `preservedState: 2026-08-26` |
| `ask-authority.json` | `s-theory-of-certainty` stays **Core** and re-resolves to r02; `s-theory-of-certainty-v1-0` is **Reference / jurisdiction `historical`**. History entry appended |
| `current-corpus.json` | the work stays IN; the preserved edition is REFERENCE ONLY / historical |
| `deposits/` | `w-theory-of-certainty.r02.md` added (Zenodo-verified). **`.r01.md` does not move** — same bytes, same checksums, re-keyed to the preserved identity |
| index | 16 Core chunks now read r02 and are labelled *The Ground for Certainty*; **16 new preserved chunks** read r01, are labelled *The Theory of Certainty v1.0, 26 August 2026*, and carry *"PRESERVED HISTORICAL STATE … may not establish datumwise's current position"* |
| `consumers.json` | new `frozen-deposit` row for r02.md; the r01.md row annotated as superseded and **not closed**; the gate's own acceptance row extended |
| `check_publications.py` | the G9 ToC assertion rewritten as a two-record chain — see §9 |

`workId`, `sourceId` and `recordId` are all unchanged for the work itself. **`s-theory-of-certainty`
still names the Core source and `w-theory-of-certainty` still names the work**, which is the F3
invariant holding under a real move: identity is durable, presentation is resolved.

**The v1.0 edition gets its own identity, not a flag.** That is Huayin's own ruling of earlier the
same day, applied unchanged: *one sourceId cannot be both current authority and preserved history*.
It is the smaller half of the AG v1.1 apparatus — a source identity and a jurisdiction, and no
`/history/` route, because there was never an onsite Certainty doorway page to preserve.

### The deposit diff is seven lines, and it settles item 4 by evidence

`w-theory-of-certainty.r01.md` → `.r02.md` changes exactly: title, subtitle, version/date, `subject`,
the LaTeX running head, the DOI line — and **one sentence of the abstract**, which now reads:

> This paper develops a concise framework for analytical and operational reliance **within the Theory
> of Certainty**.

The keyword list still leads with `Theory of Certainty`. The substantive framework is byte-identical
otherwise. So the claim "the framework term survives; the publication title changed" is not something
we took on trust — it is in the deposited bytes.

---

## 3 · Every current-presentation change caused by re-resolution

Verified in the built site, not in source.

| surface | before | after |
|---|---|---|
| `/analytical-governance` §Legitimacy pointer — **a citation** | The Theory of Certainty → doi:…22114802 | **The Ground for Certainty** → `doi.org/10.5281/zenodo.22118479` |
| `/analytical-governance` §Where this sits relation row — **names the discipline** | The Theory of Certainty | **unchanged** — href still re-resolves to …22118479 |
| `/research` | The Theory of Certainty | **The Ground for Certainty**, current record link → …22118479 |
| Ask citation labels | The Theory of Certainty | **The Ground for Certainty** (resolved at read time, not stored) |
| Ask standing sentences | current record v1.0 (…22114802) | current record v1.1 (…22118479) |

Everything except the relation row re-resolved for free, because
`apps/website/src/data/publications.ts` imports the registry JSON directly and `currentRecord()`
reads the ruled `status` rather than picking a winner by date.

### The relation row: changed, then changed back, and the correction is the finding

`analytical-governance.astro:126` carried the hand-typed string `'The Theory of Certainty'` as a
relation-row name, directly above a registry-derived `href`. I derived it — reasoning that a title is
as much a publication fact as a version or a DOI, and that this file types none of those. **That
reasoning was right about publication facts and wrong about that string.**

> Theory of Certainty is still valid, except when citing the article, the title needs to match the
> new paper. **Not all Theory of Relativity are in books titled Theory of Relativity.**
> — Huayin, 2026-08-26

The row's relation is *supplies the upstream discipline to*. It names the **discipline**, the way a
sentence about relativity names relativity and not whichever paper currently states it best. A
theory's name is editorial and stable; a publication's title moves when the author retitles it. Those
are two facts that merely happened to be the same string until 2026-08-26, and a rename is exactly
the event that separates them.

Reverted to the literal, with the `href` left registry-derived so the link still lands on the current
record. **Anchor text that names a theory over a target that resolves to its current foundational
publication is what a citation to a theory has always looked like — it is not a mismatch.**

The page names the *publication* once, one screen up, in §Legitimacy — *"developed separately in
{certainty.label}"* — which **is** a citation of the article and therefore does re-resolve. Two
appearances, two different jobs, and item 8 of the page rulings caps it at two.

Screenshot- and markup-verified. The built page now contains exactly:

```
'The Ground for Certainty'  ->  https://doi.org/10.5281/zenodo.22118479      (the citation)
'The Theory of Certainty'   ->  https://doi.org/10.5281/zenodo.22118479      (the discipline)
```

The rule is written down where the next person will look for it —
`registry/publications/README.md`, under the `canonicalLabel` section, because `canonicalLabel` is
the one string this decision actually governs: it follows the deposited title **because that is how
the corpus cites the work**, and for no other reason.

---

## 4 · Conceptual "Theory of Certainty" was not mechanically renamed

A full-repo sweep classified every occurrence into current-presentation / deposited-history /
conceptual-prose / test-and-ledger before anything was edited. **Not one conceptual use was touched.**

Untouched, on purpose:

- **AG v2.0's deposited bibliography** — `Wang, Huayin. 2026d. *The Theory of Certainty: Grounds for
  Analytical and Operational Reliance*. Version 1.0. Zenodo. DOI: 10.5281/zenodo.22114802.` and its
  five in-body `(Wang 2026d)` references. `frozen-deposit`. AG v2.0 was published citing v1.0 and
  that is a true historical fact.
- **The v1.0 deposit itself** — byte-frozen, sha256 and md5 unchanged.
- **Every conceptual sentence** — the AG page's design-intent comments, the `/analytical-governance`
  prose about the upstream discipline, `sources.json`'s `purpose` field, the two AG-page specs, the
  dated ledger entry in `ask-authority.json`.
- **The committed F1 eval results**, which record what Ask actually said on the day.
- **The published servability Q&A** (ruling F) — not regenerated, not re-reviewed, not edited.

The only prose that changed is prose that **cites the current publication**. That is the whole rule,
and the boundary is not "conceptual vs literal" — it is *citing the article vs naming the theory*.
The relation row above is the case where I got the boundary wrong on the first pass; §3 records it.

---

## 5 · Targeted durability and current-vs-historical checks, against the real transition

F3 tested a **synthetic** move that supersedes and renames at once, because a synthetic move can be
made to do that on demand. Four hours later the corpus supplied the real one. Four new tests use it:

| test | asserts |
|---|---|
| `test_the_real_v1_0_to_v1_1_transition_flags_a_stored_citation` | a citation stored while v1.0 was current keeps `standingAtAnswer` and `labelAtAnswer` exactly, re-resolves to v1.1/22118479, sets **both** `supersededSinceAnswer` and `labelChangedSinceAnswer`, and keeps `readableRecordId` = r01 while `currentRecordId` = r02 |
| `test_the_superseded_certainty_record_keeps_its_own_deposited_title` | r01 stays titled *The Theory of Certainty* and `superseded`; r02 is *The Ground for Certainty* and `current`; the edge is by recordId |
| `test_the_preserved_certainty_edition_is_labelled_by_its_own_edition_name` | Core chunks read r02 and are labelled *The Ground for Certainty*; preserved chunks read r01, are labelled *The Theory of Certainty v1.0, 26 August 2026*, are `reference`+historical, and the two record identifiers do not fuse |
| `test_the_preserved_certainty_edition_is_reachable_the_same_way` | an explicit question about v1.0 retrieves the preserved edition, with r01 readable and r02 current |

**One existing control had to move, and the reason is the control doing its job.**
`test_a_citation_still_current_is_not_flagged` used ToC r01 as its example of a *still-current*
record. It started failing at 22:20 — correctly. It was asserting `supersededSinceAnswer is False`
about a record that had just become superseded. The control moves to a single-record work
(`w-certifiable-state`) and the ToC case is kept as the **positive** arm above. A control fixture has
to be chosen so the world cannot make it true or false by accident.

`test_a_label_resolves_even_when_the_standing_cannot` was re-expected to *The Ground for Certainty* —
that assertion exists precisely to prove the label is resolved now rather than carried.

---

## 6 · The typed-authority correction, and its results on h2 / h3 / r6

### The diagnosis, sharpened past the F report

The F report named the class. The stored evidence names the passages. On `h2` and `r6` the offending
citations were `/learn/frameql-primer#where-to-go-next` and
`/learn/frameql-an-introduction#implementation-and-further-reading` — **not** reference lists. The
bibliography gate already existed and already hard-gates `References`/`Bibliography` sections. These
two are *reading-path and further-reading pointer sections*, deliberately excluded from that set,
because "Implementation and further reading" makes a real claim about which source is authoritative
for shipped meaning and case `s3` is about exactly that claim.

And the deeper cause is ours. `index_build.py` deliberately keeps publication facts **out** of the
index — foreign keys only, never a title, version or DOI — because a fact copied into a build
artifact becomes a second source of truth for it, and G7 was right to reject that. The consequence
went unnoticed until F1:

> Having removed the fact from every passage, we then asked the agent questions that only that fact
> can answer, and handed it nothing entitled to carry it. It read the title off the nearest piece of
> prose that had one.

### The repair is a source, not a filter

A third token namespace, matching the [S#] / [X#] split the codebase already uses for the same
reason — *the cheapest way to make a model keep two classes apart is to never let them share a
namespace*:

```
[S#]  datumwise passages       — what the corpus says.
[X#]  external sources         — the outside world.
[R#]  the publication registry — what a work is CALLED, which version is CURRENT, which DOI
                                 resolves to it, and what it superseded. Nothing else.
```

`ask/identity.py` types the QUESTION (identity/currency cues) and resolves WHICH work it names —
against **every title the work has ever carried**, not only the current one, because "is the Theory
of Certainty still current?" names a work whose current title no longer contains those words. Both
conditions must hold, so the registry never appears on a question that merely mentions a work.

Three narrow consequences, and nothing else changed:

1. **The card is presented** as `[R#]`, with a standing sentence that says what it may establish and,
   explicitly, that it *"carries no argument"* and *"may not be used to settle a question of
   doctrine."*
2. **Pointer sections belonging to other works are excluded** — on identity questions **only**. A
   hard gate rather than a demotion, for the same reason `layer == "out"` is: a demotion still admits
   the passage when nothing else scores, which is exactly when citing it does the most damage. A
   pointer section inside the work being *asked about* is not excluded; that is the work speaking
   about itself.
3. **The constitution and the reviewer rubric both gained the rule**, in the same words: another
   paper's mention of a work is authoritative *as part of that paper* and is not authority for the
   cited work's current title, version, DOI or currency.

A registry citation is **evidence, not a durable citation**. It is deliberately kept out of `sources`:
a durable citation's whole job is to re-resolve its stored presentation against the registry later,
and a citation *of* the registry has nothing to re-resolve.

### Results — gpt-5, the same cases, the same harness

| case | F1 (2026-08-26, before) | now | judged |
|---|---|---|---|
| `h2` *"…is that datumwise's current position?"* | **FAIL**, judged 1 | **PASS** | overall **4**, currency ✓, source_selection ✓ |
| `r6` *"What is the AG paper called, and what version is current?"* | **FAIL**, judged 2 | **PASS** | overall **5**, currency ✓, citation_accuracy ✓ |
| `h4` *"What did v1.1 argue, and what changed in v2.0?"* | pass, **false** — judged 2 | **PASS**, on the strengthened assertion | overall **3**, currency ✓ |
| `h3` *"…if a system cannot refuse, it is not governed?"* | **FAIL**, judged 3 | **still FAIL**, judged 2 | see below |

`r6`'s answer now reads: *"Analytical Governance — current record v2.0 — is deposited under the title
'Analytical Governance: Governing the Legitimacy of the Analytical Service.' [R1]"* The defect was
giving the **superseded** title as the current one. It is gone, and the answer distinguishes the
editorial label from the deposited title without being asked to.

On `h2` the top-8 no longer contains a single pointer passage. It contains the preserved v1.1 route,
whose own first line is *"This page is not current… the current record is Version 2.0… and the
current doorway is Analytical Governance."*

**`h3` is NOT fixed, and it is not a typed-authority failure.** Its retrieved passages were four Core
sources and no Analytical Governance at all — BM25 simply did not rank AG for that sentence. The
sentence being quoted is v1.1's conformance test, which lives in the preserved edition; the honest
answer names the edition. See §10 for the ruling this needs.

**A harness defect I introduced, found and fixed in the same hour.** The registry block reached the
agent as `[R#]` and reached the **judge** as nothing at all, because the judge prompt is built from
`sources`. On the first targeted run the judge marked h2 and r6 down for *"citing a registry without
providing it"* — the agent had used the new mechanism exactly as designed and was penalised for it.
The same hole existed on the **reviewer** side: `_fmt_sources` read `sources or evidence`, so an
answer citing one `[S#]` and one `[R#]` would have had its registry block hidden from the reviewer
while the reviewer was asked to check its currency. Both are fixed; the pre-fix numbers are committed
in `eval/results/openai_gpt-5_typed-authority.json` beside the corrected run, so the difference stays
readable rather than being quietly replaced.

---

## 7 · Historical reachability — h4 strengthened, and demonstrated

**The old assertion was `must_any: [["1.1"], ["2.0"]]`.** In F1 it passed on both models while both
answered *"the corpus does not establish what v1.1 argued."* The preserved edition was never
retrieved; the digits appeared; the assertion could not tell the difference.

**The cause was a cue list.** `historical` opened on phrases like *"used to say"* and *"back then."*
Naming a superseded edition by its number — the plainest way anyone asks a historical question about
a publication — was the one way that did not work.

**The repair is registry-derived, not another cue string.** `names_superseded_edition()` is true
exactly when the version the question names is a version the registry rules superseded. It becomes
true for a new work on the day that work is superseded, and needs no edit.

**The assertion is now about reaching evidence, not about vocabulary.** A new harness assertion kind,
`must_cite`, reads the *source list* rather than the prose — the only assertion in the harness that
does. `h4` carries `must_cite: ["s-analytical-governance-v1-1"]`, three `must_any` groups, and a
`must_not` on the exact refusal sentence both models produced.

**Demonstrated:** h4 now retrieves 6 preserved v1.1 passages including v1.1's own *Revision Note*, and
the answer cites **five of them**, all `s-analytical-governance-v1-1`. Judge: currency ✓.

The invariant's other arm is held and tested:
`test_a_current_position_question_still_cannot_be_settled_by_a_preserved_edition` — a current-position
question returns Core only, with nothing historical in it.

**I tried a larger version of this and backed it out.** Preserved editions of Core works were briefly
made always-reachable-but-demoted, which would have helped `h3`. It broke
`test_historical_passages_are_reachable_only_through_the_historical_jurisdiction` — a ruled invariant
with a test on it. Changing it is a doctrinal move, not a patch, so it is brought as a proposal in
§10 and **the code is reverted**.

---

## 8 · Public view count, and what happened to the existing counts

`views` and `provisional_views` are now separate columns, added through the same additive
`ALTER TABLE` path `evidence` and `published_answer` use. The typing lives at the **single write
site** — `store.get(qa_id, bump_view=True)` — so the HTTP layer goes on asking one question and
cannot get the kind wrong:

```sql
UPDATE qa SET views            = views            + (published = 1),
              provisional_views = provisional_views + (published <> 1) WHERE id=?
```

`(published = 1)` and `(published <> 1)` partition every value, so exactly one counter moves per read
and `views + provisional_views` remains every read the service served. **The predicate is `published`,
not `standing`** — `publish()` is the only writer of it and it is a human act; the public collection
already gates on it; and `test_public_surface.py` proves a reviewed-but-unpublished row is not
reachable by a reader, so `standing == reviewed` is demonstrably not the publication fact here.

`provisional_views` never reaches `_row_to_public`. It appears on the **review** surface only —
internal read counts preserved separately, as the ruling permits.

### Existing counts: reported, not rewritten

Full ledger: `services/ask/docs/view_count_correction_2026-08-26.md`.

| db | role | published rows | Σ views | treatment |
|---|---|---|---|---|
| fly volume, `ask-datumwise` | the deployed service | **not reachable from this container** | unknown | rows gain `provisional_views = 0` additively on next start; **no `views` changed** |
| `/tmp/ask-servability.db` | the F4 publication | 1 | 2 | correction **proposed, not applied** |
| local `/data/ask.db` | test-suite spill, no real publication | 29 | 4 | leave alone; test artefacts |

For the servability Q&A (`772b736f2852`), two independent facts agree that both reads were
pre-publication reviewer reads: the F report says so, and the specimen dumped *after* publication
already recorded `views: 2`, which the row still reads. The proposed correction — `views` 2 → 0,
`provisional_views` 0 → 2 — is written out with guard clauses that refuse to fire if a genuine public
read has landed since, and refuses to run twice. **It has not been executed.** Rewriting a published
metric is a separate act and wants your word on it.

Existing rows start at `provisional_views = 0`. That is not a claim that they had no pre-publication
reads; it is the honest reading that nothing distinguished them until the column existed.

Seven new deterministic tests, negative-tested against six deliberate breaks; every one fails under at
least one break.

---

## 9 · Gates

| gate | result |
|---|---|
| publication registry (`check_publications.py`, G1–G10) | **OK** — 33 works, **81** records, **88** classified consumers, 13 reconciliation items |
| corpus membership | **OK** — **46** catalogued sources, 17 IN, 29 REFERENCE ONLY, 0 unadjudicated |
| deposit manifest (`ingest_deposits --check`) | **OK** — 16 ingested, 14 Zenodo-verified, 2 author-supplied, all sha256 match |
| website build | **clean**, 45 pages |
| ask tests | **107 passed** (+27 on F's 80) |
| `check_currency_stamps` | still cannot run in this container — columna-core not installed. Unchanged by this tranche |

### Two findings inside the gates

**1. The deposit ingest gate has been dead since commit `06b6ee1`.** `ingest_deposits.targets()` read
`corpus["in"]` — a key that left the file when Ask's authority manifest was split out of
`current-corpus.json`. It raised `KeyError` on **every** invocation, so `--check`, the offline gate
whose job is to report a deposit gone STALE against the registry, has been crashing rather than
checking, and AG v1.1's manifest row was written by hand under a header that says *"do not hand-edit."*
A gate that cannot run is not a gate, and a generator that cannot generate beside that header is the
more expensive half of the defect.

Repaired: Core floats to the current record; historical-record sources pin to their own `recordId`
forever and are labelled by their own edition name rather than the work's current label. The
regeneration reproduced **every existing row byte-identically** — same md5s, same sha256s — which is
the evidence that the repaired generator agrees with the hand-written file. Then, before anything was
changed, it said:

```
STALE       s-theory-of-certainty is ingested at w-theory-of-certainty.r01
            but the registry now rules w-theory-of-certainty.r02 current
UNINGESTED  s-theory-of-certainty-v1-0 ... absent from the manifest
```

— exactly the two things this reconciliation had to do.

**2. G7 failed closed three times during this work, correctly each time**: on the new deposit file
before it was tracked, on the new DOI literal in the gate's own G9 block, and on the two DOI literals
in the new typed-authority tests. All three are now declared, `acceptance` class, with the reason
written down.

**The G9 assertion was rewritten, not deleted.** It pinned `22114802` as current earlier the same day;
it now asserts the two-record chain — and because this is the corpus's **first edge that supersedes
and renames in one move**, it additionally pins **both deposited titles by name**. The failure that
catches is not a missing record; it is a helpful hand tidying the superseded record's title to match
its successor, which would erase the fact that AG v2.0's bibliography cited a title that really
existed. The consumers note is **extended, not edited**: a ledger that revises its own earlier entries
stops being evidence of what was asserted when.

**One pre-existing defect found and NOT fixed (out of tranche):** the ask test suite is not hermetic
with respect to its database. `ASK_DB=X pytest tests` twice against the same file fails
`test_cache_and_vote_round_trip` the second time. A green run that can go red from a leftover file is
a gate that lies. One-line fix (a per-run temp DB fixture); it wants a ruling because it touches
every test.

---

## 10 · Merge / deploy readiness

**Recommendation: ready to merge. NOT ready to deploy, and the reason is one open ruling plus one
number.**

Ready:

- **The new current record**, reconciled through the machinery rather than beside it — minted, gated,
  rebuilt, and re-resolved on every current surface, with the preserved edition given its own
  identity and its own reachable jurisdiction.
- **The identity/currency defect**, closed for the class it was diagnosed as. h2 and r6 both pass on
  gpt-5, judged 4 and 5, with currency ✓ on both — and the mechanism is a typed source with a stated
  entitlement, not a ranking change. Embeddings were not turned on.
- **Historical reachability**, demonstrated: h4 reaches and cites five preserved v1.1 passages, and
  the assertion now checks the source list rather than the digits.
- **The view-count rule**, in force for future reads, with the existing counts reported and untouched.

Wanting a ruling before deploy:

1. **`h3`, and the invariant behind it.** A question that quotes a superseded edition's sentence and
   asks whether datumwise holds it cannot currently be answered honestly, because the preserved
   edition is invisible unless the question names a version. The proposal, backed out of this
   tranche: **a preserved edition of a *Core* work is always reachable, and always demoted and
   labelled** — narrow (two sources today: AG v1.1 and Certainty v1.0), and it changes a ruled
   invariant with a test on it, which is why it is here and not in the diff. Invisibility is
   currently doing the labelling's job and doing it worse: a labelled demoted passage can be reasoned
   about, a missing one cannot.
2. **The `h4` residual.** Opening `historical` boosts the reference layer ×1.6, and on h4 it took all
   eight slots — so the answer describes v1.1 well and states v2.0's organising claim weakly, because
   v2.0's own text never arrived. A question about **both** editions currently gets one. Ranking
   change, therefore out of scope; reported.
3. **The servability Q&A's `views: 2`.** SQL written, guarded, not run.
4. **The deploy itself.** The live fly deployment is a different, older database. Nothing here has
   been deployed, no cache has been purged, and `cache_purge` must be run against the live database
   after the index move — a cached answer is a promise that asking again gives the same thing, and
   this rebuild voided it. Deploy from the intended merge state, on your ruling, not from here.

---

## Cost

| item | spend |
|---|---|
| targeted evaluation, gpt-5, h2/h3/h4/r6 (answers $0.104 + judge $0.088) | $0.192 |
| re-run of h2/h4/r6 after the judge defect was fixed (answers $0.062 + judge $0.089) | $0.151 |
| reconciliation, index rebuild, site build, 107 tests, all gates | $0.000 |
| **total** | **$0.343** |
