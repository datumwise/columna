# View-count correction — ledger, 2026-08-26

**Status: RULED AND EXECUTED, 2026-08-26 (§5c).** This ledger was written REPORT ONLY, with the
statement in §5a unrun and awaiting a ruling. Huayin ruled it the same evening — *"public views
begin at publication… there was no public readership represented by those two reads"* — and it was
run once, under its own guards. §5c records what it did. Everything above §5c is left exactly as it
was written before the ruling, because a ledger that edits its own pre-ruling reasoning after the
ruling arrives stops being evidence of what was proposed.

## 1. The ruling

> Public `views` should count public reads after publication. Pre-publication/provisional/reviewer
> reads should not appear as public readership on the reviewed object. If internal/review read
> counts are useful, preserve them separately. Please use the smallest clean implementation and
> report how existing counts are treated. Do not silently rewrite historical metrics.
> — Huayin, 2026-08-26

## 2. The rule now in force

A read arrives at exactly one place: `store.get(qa_id, bump_view=True)`, reached only from the
public `GET /qa/<id>` route.

| the row at the moment of the read | counter incremented | visible to |
|---|---|---|
| `published = 1` | `views` | the reader — `views` on the public payload |
| `published <> 1` | `provisional_views` | the reviewer only — `provisionalViews` on `/review/item/<id>` and the review queue |

**The publication predicate is `published`, not `standing`.** Reasons, in the order they decided it:

1. `publish()` is the only writer of `published = 1`, and it is a human act. The schema says so on
   the column itself: *"only a human approval sets this"*.
2. `listing()` — the public collection — already gates on `standing='reviewed' AND published=1`.
   Reads of a row a reader cannot reach are not public readership, and `published` is the narrower
   of the two conditions.
3. `tests/test_public_surface.py` asserts that a *reviewed-but-unpublished* row must not reach a
   reader. So `standing='reviewed'` alone is demonstrably not the publication fact in this codebase.
4. In the present code the two are equivalent anyway — `publish()` and `reject()` are the only
   writers of either, and they always move both together — so the choice costs nothing today and is
   the correct one if they ever diverge.

Two further properties, both deliberate:

- **Exactly one counter moves per read.** `(published = 1)` and `(published <> 1)` partition every
  possible value of the column, so `views + provisional_views` remains every read the service
  served. Nothing is dropped and nothing is double-counted.
- **The typing lives at the single write site**, not at the callers. The HTTP layer goes on asking
  one question — "count this read" — and cannot get the kind wrong.

`provisional_views` is added by the same additive `ALTER TABLE` path already used for `evidence` and
`published_answer` (`store._ADDED_COLUMNS` / `store._migrate`). It defaults to `0` on existing rows.
**That zero is not a claim that those rows had no pre-publication reads** — it is the honest reading
that nothing distinguished them until the column existed. `test_migrating_an_existing_database_does_
not_rewrite_its_view_counts` pins that the migration leaves `views` untouched.

## 3. Where the data actually is

Three databases carry `qa` rows. None was modified.

| # | database | role | reachable now | published rows | Σ `views` on them |
|---|---|---|---|---|---|
| A | fly volume `ask_data` → `/data/ask.db` on app `ask-datumwise` | the deployed service | **no** | unknown | unknown |
| B | `/data/ask.db` in this container (the default `ASK_DB`) | test-suite spill | yes | 29 | 4 |
| C | `/tmp/ask-servability.db` | the F4 publication | yes (ephemeral) | 1 | 2 |

**A — the fly volume.** Not inspected: it is not reachable from this container, and the F report
records it as *"a different, older database — the publication in F4 is local, and deploying is a
separate act with a separate token"* (`specs/f_evaluation_report_v0_1.md`). It runs older code, so
its rows do not yet have the column. On its next start under this code the additive migration adds
`provisional_views = 0` and changes no `views`. **Whatever counts it holds are unexamined and are
not proposed for correction here.** If they matter, they must be read before anything is decided.

**B — `/data/ask.db`.** 79 `qa` rows, all of them fixture questions written by the hermetic test
suite run without `ASK_DB` set (`"What does the fixture paper establish?"`, `"Can an unreviewed
answer have stars?"`, …). **There is no real publication in this file.** 29 rows are `published=1`;
25 of them have `views = 0`. The four that do not:

| id | `views` | question | what the record establishes |
|---|---|---|---|
| `8504ef8ec3bf` | 1 | Can an unreviewed answer have stars? | the single read is `store.get(qid, bump_view=True)` at `tests/test_public_surface.py:115`, executed **before** `store.publish` on the next lines — pre-publication, unambiguously, from the test source |
| `aafef0dade6e` | 1 | Can an unreviewed answer have stars? | same test, a later run |
| `de125c8a564e` | 1 | Can an unreviewed answer have stars? | same test, a later run |
| `8f5ff2f96af4` | 1 | Can an unreviewed answer have stars? | same test, a later run |

One unpublished row also carries a count: `d66472edc05f`, `views = 1`, `standing = provisional` —
the same test, from a run that did not reach the publish step.

**C — `/tmp/ask-servability.db`.** One row: the servability Q&A published through the real review
endpoint during F4. This is the specimen the F report names.

| id | `views` | `published` | `reviewed_by` | `reviewed_at` |
|---|---|---|---|---|
| `772b736f2852` | 2 | 1 | huayin | 2026-08-26 21:24:33Z |

## 4. What can actually be established about those reads

`views` was a single integer with no per-read record, so **for any row the only evidence available
is external to the database.** There are exactly two rows-classes where such evidence exists.

**Unambiguous — `772b736f2852` (database C).** Two independent facts agree:

- `specs/f_evaluation_report_v0_1.md` states it directly: *"The public read (`GET /qa/<id>`) bumps
  the view counter, and two of those reads happened while the object was still **provisional** —
  mine, during F4's before/after inspection."* Two reads, both pre-publication, both a reviewer's.
- The counter has never exceeded that. `docs/published_servability_qa_2026-08-26.json`, dumped after
  publication at 21:24:33Z, records `views: 2`, and the row still reads `views = 2` now. So the
  total number of reads ever served is 2, and the report accounts for both.

Two documented pre-publication reads and a total of two reads leaves no room for a public read.
**`views` should be 0 and `provisional_views` should be 2.**

**Unambiguous but not worth correcting — the four `views = 1` rows in database B.** The read is
visible in the test source and is pre-publication in every case. But these are not publications:
they are fixture rows in a file that only exists because the suite was run without `ASK_DB` set.
Correcting a test artefact would dress up a spill as a metric. The proposed treatment is to leave
them, and separately to stop the suite writing to the default path at all — noted below as a
follow-up, not done here.

**Everything else — not establishable.** Database A has not been read. All other rows are at 0.

## 5. PROPOSED CORRECTION — NOT APPLIED

Everything in this section is a proposal. **It has not been executed.** Applying it is a separate,
explicitly-labelled step that a human must authorise, and this change does not perform it.

### 5a. The one row where the evidence is unambiguous

Database: `/tmp/ask-servability.db` (or wherever the servability row is when the ruling is made).

| id | field | before | after |
|---|---|---|---|
| `772b736f2852` | `views` | **2** | **0** |
| `772b736f2852` | `provisional_views` | **0** | **2** |
| `772b736f2852` | `rank` (derived, `log10(views+1)`) | 0.4771 | 0.0 |

```sql
-- NOT RUN. Requires a human ruling. Reclassifies, does not delete: views + provisional_views is
-- unchanged at 2, so no read is erased — only its kind is corrected.
UPDATE qa
   SET provisional_views = provisional_views + 2,
       views             = views - 2
 WHERE id = '772b736f2852'
   AND views = 2                      -- refuses to run if any further read has landed since
   AND provisional_views = 0;         -- refuses to run twice
```

The two guard clauses are the point: if a genuine public read arrives before the statement is run,
the premise ("all reads so far were pre-publication") is no longer true and the statement must not
fire. It should be re-derived, not re-run.

### 5b. Everything else

**No change proposed.** Database A is unread; database B is a test artefact; every other row is at
zero. Any correction there would be an invention, and inventing a number is the failure the ruling
names.

### 5c. The alternative that was NOT chosen

The F report offered two defensible readings — *reset the counter at publication (views measure
public life)* or *keep it (views measure reads of that text)*. The ruling picks the first for the
public number, and the implementation keeps the second available in `provisional_views` rather than
discarding it, so the reading that was not chosen is still recoverable from the record.

## 6. Follow-ups, not done here

- **Read database A before anything is decided about it.** It is the only one whose counts might be
  real, and it has not been looked at.
- **The test suite writes to the default `ASK_DB` (`/data/ask.db`).** That is how 79 fixture rows and
  four published-with-a-view rows got there. The suite should be pointed at a temporary file; until
  it is, `/data/ask.db` is not a source of metrics about anything.


---

## 5c. Executed — 2026-08-26

**Ruling (Huayin):** reset the servability Q&A's public `views` from 2 to 0 using the guarded SQL.
*"Those two reads occurred while the object was provisional/reviewed, before it became a public
reviewed answer. Our rule is: public views begin at publication. This is not a rewrite of historical
public readership; there was no public readership represented by those two reads."*

Run once, unmodified, on `772b736f2852` in `/tmp/ask-servability.db`:

| | before | after |
|---|---|---|
| `views` | 2 | **0** |
| `provisional_views` | 0 | **2** |
| `views + provisional_views` | 2 | **2** — no read erased, only its kind corrected |
| public payload `views` | 2 | **0** |
| public payload `rank` | 0.4771 | **0.0** |
| `standing` · `published` · `reviewed_at` · notice | reviewed · true · unchanged | unchanged |
| public payload carries `provisionalViews` | no | **no** |
| review payload | — | `views: 0`, `provisionalViews: 2` |

Both guards held. Re-running the identical statement affects **0 rows**, because
`AND provisional_views = 0` is now false — it cannot be applied twice.

### The object this was run against is container-local, and that is a finding

`772b736f2852` lives in `/tmp/ask-servability.db` inside the working container. **It is not on the
Fly volume**, and the deployed service has never held it: the volume carries four rows, all of them
older, none of them this one. F4 published *through the real endpoint*, which is what the ruling of
16:35 asked for and what it proves — but into a scratch database, so the published OBJECT is
ephemeral while the published RECORD is not.

What survives durably is `docs/published_servability_qa_2026-08-26.json`, the specimen captured from
`GET /qa/<id>` on the day, and `tests/test_public_surface.py`, which asserts the rules from the
reader's side. The correction above is therefore a correction to the live object *where that object
actually exists*, and it does not reach production because production never had it.

Publishing it on the deployed service would be a new publication act, through the review gate, on a
ruling. It has not been done.
