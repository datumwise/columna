# The source catalog

`sources.json` is the language-neutral catalog of **things a serious reader can be sent to**. It is
the model behind `/research`, and it is built to be read later by *Ask datumwise* without a second,
private map existing anywhere.

## The one rule

**Publication facts are never stored here.**

Title, version, date, DOI and currency belong to `registry/publications/` and are read through
`currentRecord(workId)` / `recordFor(recordId)` at render time. A source entry holds a *reference*
(`workId`, `recordId`) and never a copy. If you find yourself typing a version number into this
file, the model is wrong, not the number.

The same rule that produced the registry applies here: *a fact that must be re-typed to stay true
will eventually be false.*

## There is no `standing` enum

An earlier draft had one — `deposited | onsite | generated | preserved | internal-ratified` — and it
was a false taxonomy (Huayin, 2026-08-25): a source can be deposited *and* onsite, generated *and*
onsite, preserved *and* onsite. Those are orthogonal facts, so they are stored as orthogonal fields
and the page composes them into a sentence:

| the field | what it means when present |
|---|---|
| `workId` | this source is a deposited work; its record is in the publication registry |
| `route` | it can be read on this site, here |
| `recordId` + `editionPinned` | the route renders **this specific deposited edition**, which may not be the current one |
| `generatedBy` | produced by running the shipped package; the named script is the generator |
| `gates` | what fails the build if this source's claim drifts |
| `preservedState` | an intentionally preserved historical state, as of this date |

Nothing is asserted by absence. A work with no `route` is simply not readable here yet.

## Edition-pinned routes

`editionPinned` is the feature, not an apology. Several site routes render a byte-faithful deposited
edition by ruling; when the registry's current record has moved on, `/research` says both plainly —
*current record v1.2 · readable here v1.1* — with every number derived. An edition-pinned route is
not stale, and it is not current. It is pinned, and the reader is told which.

## Fields

```
sourceId        required, stable, `s-…`
role            required — see below
purpose         required, one editorial line
route           optional
workId          optional, foreign key into registry/publications/works.json
recordId        optional, foreign key into records.json; only meaningful with editionPinned
editionPinned   optional boolean
generatedBy     optional string — the generator script
gates           optional string[] — e.g. build-adjudicated, currency-stamp
preservedState  optional ISO date
```

### Roles

`foundation` · `supplement` · `introduction` · `primer` · `applied` · `reading` · `position` ·
`catalog` · `study` · `program-note` · `normative-reference` · `generated-reference` ·
`machine-evidence` · `teaching` · `negative-record` · `historical-record`

Role is editorial and lives **here**, not on the work. `works.json.kind` is deliberately untouched
and stays `unclassified`, which keeps `COUNTS_ARE_DERIVABLE` false and G10 intact: no surface may
render a count of publications, and this catalog does not create a way around that.

Roles exist so a reader can decide *is this the thing I need, and what authority does it carry*.
They are not navigation categories and the page must not turn them into equal doors.
