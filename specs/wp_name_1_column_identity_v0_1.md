# WP-NAME-1 — column identity is the canonical expression, not a pin-eliding default (v0.1)

*Status: **RATIFIED & LANDED** in columna-core 0.14.0 (Huayin, 2026-07-30). Filed 2026-07-30 as a
proposal; all three open questions ruled and the code shipped in the same window. See OF-27 (struck)
and the CHANGELOG. Rulings folded in below.*

> **Rulings (Huayin, 2026-07-30).**
> 1. **Leaf case — uniform, no exceptions.** The canonical expression is the identity for *every*
>    unaliased series, including leaves: a bare measure keys as `revenue`, and member access ships
>    verbatim as `revenue.sub`-style dotted — the dot-to-underscore mangle (`revenue_sub`) was itself
>    an invention and retires with its sibling. §4's law (*derived by rule or refused, never invented*)
>    completes rather than gains an exception. Dotted keys are legal JSON and legal dataframe columns;
>    ORDER BY/HAVING accept the dotted reference through the existing attribute parsing; the collision
>    guard already covers key-vs-dimension conflicts.
> 2. **Vehicle — its own release, 0.14.0.** A `contract_version` bump is what a pre-1.0 minor exists to
>    signal; batching with a future wire-WP means waiting on a partner with no date while the
>    name-keyed consumer base grows daily — the cheapest day for this change is always today. Server
>    stays 0.8.2 (the wire-schema text `CONTRACT_VERSION` lives in columna-core and the server
>    re-exports it — reported and confirmed).
> 3. **Migration note — teach the principle, not just the diff.** Release notes + wire docs carry:
>    `contract_version` is now `"2"`; unaliased column keys changed from mechanical defaults to
>    canonical expressions (`avg_revenue` → `avg(revenue)`, `revenue_sub` → `revenue.sub`); consumers
>    who key on names should key on **AS aliases, which are author-owned and will never change under
>    any future rule** — the durable advice and the whole naming philosophy in one line.

## The finding

The §4 mechanical default names an unaliased single reducer `<reducer>_<measure>`:
`avg(aov @ {day})` → `avg_aov`, and — the manual says so in as many words (`docs/frame_ql_manual_v1.md:149`)
— *"the input anchor does not affect the default name."* That sentence is the bug. It is stated as a
convenience; it is a **denotational elision**.

Per the Two Anchors law (`specs/reference/two_anchors_paper_v1_1.md`), a pinned reduction's identity
is the triple **(reducer, input anchor, output anchor)**. `avg(aov @ {day})` reduced to `{cal.month}`
and `avg(aov @ {cal.week})` reduced to `{cal.month}` are *different quantities* — different input
anchors, same reducer, same output. The mechanical default names **both** `avg_aov`. It keeps the
reducer and the measure and throws the input anchor away: it names half the denotation and asserts,
in the manual, that the discarded half doesn't matter to identity. The whole point of the two-anchors
work is that it does.

## WP-GRAIN-1 sharpens the finding from lossy to colliding

Before the composite input anchor (0.13.4), the elision was quietly lossy — two single-level pins
that happen to share a measure collided, but such a frame was rare. WP-GRAIN-1 makes the collision
ordinary: `avg(revenue @ {store*product*cal.month})` and `avg(revenue @ {customer*store*product*day})`
— the two F1 asks, both now first-class — **both default-name to `avg_revenue`.** Put them in one
frame and the §4 collision guard (`planner.py:_check_name_collisions`) refuses: *"two columns resolve
to the name 'avg_revenue' — names must be distinct, never suffixed; give one an AS alias."* That
refusal is correct and it is load-bearing (it never suffixes, so it never invents `avg_revenue_2`);
but it is firing because the default threw away exactly the coordinate that distinguishes the two
columns. The guard is catching the default's lie. The right fix is upstream: stop telling the lie.

## The proposal

**A column's identity is one of exactly two things:**

1. an explicit **`AS` alias** — the writer names it; or
2. the **canonical expression** itself, verbatim — the framework names it by what it *is*.

Retire the `<reducer>_<measure>` mechanical default entirely. An unaliased reduction is named by its
canonical form: `avg(aov @ {day})` is the column `avg(aov @ {day})`; the two F1 asks are the columns
`avg(revenue @ {store*product*cal.month})` and `avg(revenue @ {customer*store*product*day})` — which
do not collide, because their canonical forms are the coordinates that distinguish them. The
bare-column and `measure.member` cases keep producing a name (`revenue`, `revenue_sum`) because there
the canonical expression *is* that identifier — this is not a special default, it is the same rule
(identity = canonical expression) landing on a leaf. Only the composite-expression cases that already
demand `AS` (map expressions, nested reductions, bracket filters — `Chapter 1.6`) keep demanding it,
unchanged.

## Canonical, not uttered

The identity is the **canonical** expression — the desugared, brace-normalized, WITH-inlined artifact
that `EXPLAIN` emits and that round-trips (`desugar` / `render_canonical`) — **not** the string the
writer uttered. Argue:

- **Uttered is unstable.** `avg(aov @ day)`, `avg(aov@day)`, `avg(aov @ {day})`, and a WITH-macro
  that expands to the same all utter differently and denote identically. Keying identity on the
  utterance makes the column name depend on whitespace and sugar choice — the same defect the manual
  already rejected for clause-reference (`docs/frame_ql_manual_v1.md:395`: *"deciding when two
  expressions are 'the same' … raised more questions than the convenience answered"*).
- **Canonical is a fixed point.** The desugaring transform is idempotent and denotation-preserving
  (WP-FrameQL rider 1); two asks with the same denotation have the same canonical form and therefore
  the same identity, and two asks with different denotations differ. Identity tracks denotation
  exactly — which is the property the whole grammar is built to guarantee.
- **Canonical is already the artifact we show.** `EXPLAIN` emits canonical; the wire's disclosure
  reading names the canonical pin (`{store*product*cal.month}`); the recall ledger and case corpus
  quote canonical. Naming the column by anything else would make the column label disagree with the
  reading beside it.

## What is untouched (and provably so)

- **Declared names are untouched.** A `DERIVED`/`MEASURE`'s declared identifier is its name by
  declaration; it is not an unaliased inline expression and this WP does not touch it. `aov`,
  `daily_aov`, `revenue` keep their declared names everywhere.
- **Computation is provably unaffected.** A column's name is metadata — a label carried on
  `ColumnResult.name` and surfaced as the wire's `columns[].name`. The engine resolves and reduces on
  **levels and expressions**, never on the column's display name; no resolution path reads it. Changing
  the label cannot change a number. The acceptance suite proves this: every served value is
  byte-identical before and after (the naming change is a pure relabel).
- **The collision guard stands, unchanged (`planner.py:_check_name_collisions`).** It still refuses
  two columns that resolve to one identity, and it still **never suffixes**. Under canonical identity
  a genuine collision means two columns with the *same canonical expression and no alias* — i.e. the
  same column asked twice — which is a writer error the guard names honestly (`give one an AS alias`),
  exactly as today. The guard's contract does not change; only what feeds it does.

## Position on `contract_version`

**Bump `contract_version` `"1"` → `"2"`.** This is the one place WP-NAME-1 touches the wire, and it
touches it deliberately. The default column **key** changes for the *same utterance*:
`SELECT avg(aov @ {day}) AT {cal.month}` returned `columns[0].name == "avg_aov"` under `"1"` and
returns `columns[0].name == "avg(aov @ {day})"` under `"2"`. A consumer that keys results by column
name — a dashboard column map, a saved view, an agent that addresses `avg_aov` — reads a different
key for a query it did not change. That is precisely a breaking wire change, and **a changed default
key for the same utterance is what version fields are for.** WP-GRAIN-1 added reason codes without a
bump (the envelope shape was unchanged and readers route by outcome); WP-NAME-1 changes the value of
an existing field for an unchanged input, which is the opposite case. The contract's own rule — grow
by rule, break by version — obliges the bump. (Open question O-1 below asks whether the tombstone
discipline should extend to a documented `"1"→"2"` migration note for the name field.)

## The wire-visible blast radius, and the regeneration checklist AS acceptance

Because the column name is wire-visible, retiring the default changes every committed artifact that
displays an unaliased reduction's name. The acceptance criterion for WP-NAME-1 is **not** a handful of
unit assertions; it is that **every committed output regenerates coherently and the diff is exactly
the name change, nothing else.** The checklist:

| Surface | File(s) | What changes | Regenerate / verify |
|---|---|---|---|
| Integrity transcript | `apps/website/src/data/transcript.generated.json` (gitignored; built) | any unaliased reduction's `columns[].name` | `gen_transcript.py`; the flap detector must stay green |
| /case corpus | `apps/website/src/data/case.generated.json`; `columna_server.recapture.EXEMPLARS` | exemplar column names + any prose quoting `avg_aov`-style names | `gen_case.py`; `test_case_demo_recapture.py` |
| Grammar reference | `apps/website/src/data/grammar.generated.json` | if it quotes a default name | `gen_grammar.py` |
| Demo transcripts | `packages/columna-*/demos/`, `demos/*.txt`, `_run_demos.py` fixtures | printed column headers | re-run demos; `test_fixture_drift.py` counts unchanged |
| FrameQL manual | `docs/frame_ql_manual_v1.md:145,149,173,175,297,453,599,724,784` | the naming-law section: retire the `<reducer>_<measure>` clause, rewrite §1.6 around canonical identity, fix every worked example that shows a default name | hand edit; prose-coherence tripwire re-parses every code block |
| Wire-strings / explorer | `apps/website/src/data/wire_strings.json`, `explorer.ts` | any place that renders or maps a default name | verify no hardcoded `avg_aov` |
| Core tests | `test_envelope_planner.py:45-47`, `test_envelope_sugars.py:29,95`, `test_envelope_explain.py:21`, `test_inline_reduction.py` | assertions expecting `avg_aov` / `AS avg_aov` become the canonical-identity form | update expectations |
| Contract version | `disclosure_wire.py` `CONTRACT_VERSION`; `test_disclosure_wire.py`; every golden asserting `"1"` | `"1"` → `"2"` | bump + update goldens; document the migration |

A spec is a promise; this table is the promise. WP-NAME-1 is done when the checklist is green end to
end and the only semantic delta anywhere is the column name (values, moods, disclosures, reasons all
byte-identical), plus the single deliberate `contract_version` bump.

## Scope, precisely

| in scope | out of scope |
|---|---|
| retire the `<reducer>_<measure>` mechanical default | changing declared measure/derived names |
| column identity = canonical expression \| AS alias | changing the `AS`-required set (composite/map/bracket stay required) |
| bump `contract_version` to `"2"` for the changed name key | any change to values, moods, disclosures, or reason codes |
| regenerate every wire-visible surface (the checklist) | the collision guard's behavior (it stands verbatim) |

## Open questions

- **O-1.** Does the `"1"→"2"` bump carry a documented migration note (old-key → new-key) for consumers
  keying on `avg_aov`-style names, or is the bump itself the whole contract (consumers re-read the
  wire's `name` field, which they should already treat as authoritative)?
- **O-2.** Bare-column identity: is `revenue` (a served bare measure) named `revenue` or its canonical
  `revenue` with an implied member — i.e. does `measure.member` render `revenue_sum` or `revenue.sum`?
  The manual currently shows `<measure>_<member>` with an underscore (`sum_revenue`); canonical
  identity would argue for the dialect the reader sees elsewhere (`revenue.sum`). One-line ruling
  needed so the leaf case is consistent with the composite case.
- **O-3.** Sequencing: WP-NAME-1 is a `contract_version` bump; does it ride its own release, or batch
  with the next wire-touching WP so consumers absorb one version step, not two?
