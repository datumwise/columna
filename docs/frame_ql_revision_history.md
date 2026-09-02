# Frame-QL revision history

**Non-normative.** Nothing here is current law. This document records how the Frame-QL manual's
claims changed and when — superseded behaviour, corrections, migration notes, and the dates each
change entered. Every rule that is still in force was moved into
[`frame_ql_language.md`](frame_ql_language.md) before these notes were filed here; if a statement
below contradicts the language manual, the language manual is right and this is the record of what
was believed earlier.

It exists because the manual used to carry this material inline. That made a reader assemble current
law out of a paragraph and the dated correction beneath it, and it is where several stale claims sat
unnoticed — a note is easy to write and easy to stop re-reading.

Entries are grouped by the section they were attached to, in document order.

## Editions and availability

**▸ Currency repair, 2026-08-31.** This section previously read *"Columna ships in two tiers, and
this one manual covers both,"* and thirteen constructs below carried an inline **[Pro]** marker
denoting purchasable availability. **There is one tier.** The marker is retired by topology record
§17.5 and the claim by §17.4: no product claim may be created for a delivery form with no factual
referent. Each tagged construct has been re-typed below against what the shipped package
*executes*, and two of them — MNAR exclusion (Chapter 7.4) and coverage (Chapters 5.7, 7.4) —
turned out to **ship today**, so the marker had been withholding, in prose, capability the open
package already serves.

## 2.1 The shape of the canonical form

**▸ Second-Edition sync (the multi-input shape is [ROADMAP], 2026-08-31).** This paragraph used to
end *"The framework parses this form directly, type-checks it, and plans it."* That is true of the
**single-input** shape — `op(col @ {a})` — and false of the multi-input one written above with
`col_1, col_2, …`: **shipped reducers are arity-1**, so a reduction over several inputs is refused
on arity before any grain question is reached. The block above is therefore a **schematic** of the
canonical form, not a query that runs.

The consequence is recorded rather than left for a reader to discover: the multi-input
`input_anchor_ambiguous` clarification described in §2.3 is **unreachable**, because the arity
refusal fires first. The shape remains the leading candidate for the future Column Algebra
surface — it is already canonical, and building it would repair the language rather than enlarge
it — but it requires the participation / joint-support law first, and no `(a,b) @ A` alternative
is to be introduced in its place (ruled Huayin, 2026-08-31).

## 2.3 Single-series reducers and the input pin

**▸ Second-Edition sync (2026-08-31).** This paragraph previously stated the clarify
unconditionally — *"the framework does not guess. It clarifies…"* — describing the `|L| > 1` branch
as if it were the whole rule. The `|L| = 1` branch has shipped since 2026-08-20 and is the common
case on a shallow Manifold, so a reader following the old text would have expected a clarification
and received a served number with a material caveat. Corrected against the shipped disposition.

**▸ Second-Edition sync (tombstone).** The First Edition named the multi-input case with a *distinct* reason, **`co_anchor_ambiguous`**. That reason is **retired** — tombstoned 2026-07-16 under the §2c expression law, with a retirement-pin test asserting it is never emitted. The cross-universe rate it originally named is now the **`cross_universe`** category error (§2.5), and within one universe the denotation rule leaves nothing to disambiguate, so the shipped planner emits **`input_anchor_ambiguous`** here. The spelling is kept only as a dated tombstone, so old transcripts stay interpretable.

## 2.8 Subsetting and scans **[ROADMAP]** / **[SCHEDULED]**

**▸ Second-Edition sync (recognition is not capability, 2026-08-31).** The two forms are *not*
unshipped in the same way, and the difference is worth naming because the shipped behaviour can
mislead a reader who checks only whether a query is accepted.

- **The bracket filter is not shipped.** `revenue[region = "east"]` is accepted by the statement
  grammar and refused at planning — it does *not* fail to parse (§6.7 says the same; a Second-Edition
  sentence claiming "does not parse" was wrong, and the two sections contradicted each other until
  2026-09-01). Frame-QL owns that refusal: the raw CPython `SyntaxError` it used to leak is repaired.
- **Scan operators are registered, and SIX OF EIGHT EXECUTE.** `cumsum`, `cummax`, `cummin` serve;
  `lag`, `lead`, `pct_change` serve with disclosures. `rolling_mean` and `rolling_sum` are
  registered as CONTRACT and are not implemented in this build — a governed `unsupported` answer,
  not a crash. The per-operator status is Appendix A's scan table, which
  `check_manual_frameql.py` diffs against the shipped registry, so this paragraph can no longer
  drift from the vocabulary it describes.

  *(Until 2026-09-01 this bullet read "Scan execution is not available in the current Core build",
  which was false for six of the eight operators it named. It was invisible because no fenced
  example exercised them — the reason the gate now reads the operator registry directly rather
  than only the examples.)*
- **`reset =` and `step =` are a narrower roadmap item still.** The shipped scan signatures accept
  `n =` and `by =`; the family-aware calendar parameters described below are not implemented, so
  the year-to-date and year-over-year spellings are unshipped on two counts rather than one.

Every worked example in Chapter 6 that is presented as *producing* a scan result is marked
`[ROADMAP]` for this reason, even though its syntax and planning path already ship.

## 2.9 The grammar grows by ruling

**▸ Second-Edition sync (the claim is now enforced, 2026-08-31).** The sentence above used to end
*"the manual is structurally incapable of documenting a query it did not run"*, and that was
**false when written**: the standing gate checked GRAMMAR ONLY, so four Chapter 6 examples using
forms §2.8 itself calls unshipped sat unmarked and parse-clean, and seventeen of the Manual's
thirty-seven examples parsed cleanly and then failed at planning or execution. A guard that proves
a query is well-formed proves nothing about whether it runs, and the gap between those two is
exactly where a manual goes quietly wrong.

The claim is now carried by a gate rather than by a promise. `docs/tools/check_manual_frameql.py`
plans **every** example marked shipped through the real planning surface, against adjudicated
fixtures declaring this Manual's own vocabulary, and **executes** the ones that plan to serve or
disclose — because an example presented as executable is not validated until the stage at which
its claimed behaviour is observable. An example documented to Clarify or Refuse must reach that
outcome *with the reason the prose names*; a generic failure is not a pass. The expectations live
in this document — its section marks and its fences — so there is no second copy of them to drift. What ships through columna-core 0.18.1 is the envelope of Chapter 1 with the series forms of §§2.1–2.7: reductions with explicit input pins — single-level or a **product grain** (§2.3, the composite input anchor of WP-GRAIN-1) — maps, composite reductions, the anchor product, one universe per expression, every grain either determined or pinned — and every answer one of the four moods (serve · disclose · clarify · refuse). The same rule governs the theory: **theory evolution does not automatically enlarge Frame-QL.** A Theory-of-Data distinction enters this language when it is implemented, tested, versioned, and ruled in — not when it is published.

## 4.1 The `WHERE` clause: pre-query input filtering

**▸ Second-Edition sync (this section's previous note was WRONG, and is corrected rather than
quietly replaced, 2026-08-31).** An earlier revision of this note said *"`WHERE` is parsed … the
filtered frame does not execute in the current Core build … This holds for a dimension that is a
coordinate of the fact itself."* **That is false, and the claim was made from evidence that tested
only one spelling.** `WHERE` on a **base dimension executes and serves**, in either quote spelling:

```
FROM finance_manifold SELECT revenue AT {customer} WHERE day >= "2024-01-01"
```

What is genuinely unsupported is narrower and is stated in §4.1.1: a predicate on a dimension
reached only **across a relationship** — the filter is pushed to the measure's own source, which
carries the universe's base coordinates and not the joined ones. That form is refused before
execution with `filter_unsupported`, which is a statement about the BUILD; the separate
`filter_unreachable` clarify remains a statement about the MANIFOLD, and the two are deliberately
not the same reason.

**▸ Second-Edition sync (literal quoting at `WHERE` — the follow-up this note rowed is now SHIPPED, 2026-08-31).** The prior revision of this note told readers that a `WHERE` string literal had to be **single-quoted**, because the predicate reached the backend verbatim and SQL read `"2024-06-01"` as an *identifier*. **That divergence is repaired.** Frame-QL accepts `'x'` and `"x"` as the same language-level kind — one string literal — and the predicate is now normalized into the substrate's spelling before it becomes backend SQL, so **both spellings execute and return the same rows**. Frame-QL's literal law is Frame-QL's; the substrate no longer reinterprets it. (This is quote-path convergence, not a new filtering capability: it admits no dimension that was not already filterable — see §4.1.1.)

## 5.3 B-anchor checking

**▸ Frame-QL revision (generated-family law, 2026-08-20).** Ratified as **ADR-036**, superseding ADR-020's inform-and-serve rule *for this case only*: **structurally prohibited analytical operations refuse. Disclose exists inside the lawful region; it cannot legalize an operation the governed law does not possess.** Until this ruling the paragraph above read *served, bound to a critical disclosure* — the number was produced and the prohibition rode out with it. The mechanism of that error is now on the record: a caveat attached to a number that should never have been produced is what let the same meaningless total keep being served, one wrapper at a time. The check is on the **operation**, not on the leaf — every point in an expression where a reduction actually travels, whether the reader *wrote* the reducer or *generated* it, is adjudicated against the governed ancestry's B-anchor over the lineages it crosses — so `level.sum`, `sum(level.last @ {day})`, `-level.sum`, `2 * level.sum`, a scan over any of them, and a `DERIVED` column carrying one all refuse alike. *Family generation creates a new analytical family. It does not create a new operator permission.* The **scope** of applicability is untouched: per operator × lineage, no stock/flow/rating type (ADR-031 D5 clarified, not reversed) — `sum` of a stock across *stores*, and `avg`/`min`/`max`/`count` of a stock across *time*, all remain lawful, because the author barred `sum` along `calendar` and barred nothing else. The disclosure code `b_anchor_crossing` is tombstoned as a producer, retained and still wired (7.4).

**▸ Frame-QL revision (locus).** The B-anchor crossing is *detected statically by the planner* — the B-anchor and the path's eliminated families are knowable from the spec, before any data is touched — and it is the planner that attaches the critical disclosure. What is *not* static is whether a route-around dissolves the crossing; that is a resolution fact, so the **column engine** may, during execution, recompute from a fertile root and *downgrade* the finding to an informational route-around (`RECOMPUTED_FROM_DETAIL`), or leave it `critical` when no sound route exists. The disclosure thus originates at the planner and has its final severity settled at the engine; in every case the number is served. This is the inform-and-serve boundary in miniature: the planner names the risk, the engine never withholds on it. *(▸ 2026-08-20, ADR-036: the **locus** finding stands verbatim — detection is static, from the spec, at the planner. Its **verdict** does not, and neither does the downgrade path it describes: a crossing is refused at the planner outright, and no engine route-around dissolves it, because recomputing from detail performs the same prohibited travel. Read this note for where the check lives; read the note above it for what the check now decides.)*

## 6.2 Multiple metrics at a shared anchor **[ROADMAP — the `count(*)` series only]**

**▸ Second-Edition sync (query-level `count(*)` is unresolved architecture, 2026-08-31).** The
example above uses `count(*)` **as a series in `SELECT`**, and that form does not ship: it has no
determinate analytical object to count. A `UNIVERSE` declares coordinates, not a fact table — only
a `MEASURE` carries `FROM <table>` — so a bare `count(*)` in a query does not name what is being
counted, and at least three readings are open: the physical source-row count, the count of
existing analytical points, and the count of observations of some measure. **The Manual does not
choose among them**; picking one silently is how a number acquires a meaning nobody declared.
Resolving it is a language ruling, not a parser fix.

**`AS count(*)` in a `.cml` MEASURE is a different and established case** and is unaffected: there
the source table is declared on the measure, so what is counted is not in question.

## 6.11 Scan for running total

**▸ Currency (2026-09-01).** This section read *"Parses and plans; does not execute"* and was
marked `[ROADMAP]`. That was true when written and had stopped being true: order-only scan
execution ships. The correction is here rather than in the code because a capability that arrives
must make the stale sentence fail — never make the working build look like the regression.

## 6.13 Time intelligence: year-to-date and year-over-year **[ROADMAP]**

**▸ Currency (2026-09-01).** This read *"unshipped on two counts"*, the first being that "scan
execution is not available in the current Core build". That count is gone: `cumsum` executes
(§6.11). Only the parameter count remains.

## Appendix B: Reserved Keywords

**▸ shipped-law reconciliation (2026-07-17), RESOLVED.** The prior edition of this appendix flagged `FROM`/`SELECT`/`AT`/`{…}` as "Coframe canonical form, not the shipped grammar," pending the Coframe→envelope rewrite. That rewrite has landed: the **envelope** `SELECT … AT {…}` *is* the shipped grammar (Chapter 1), so these are the shipped query keywords, reconciled above. The retired terse `@`-fragment (its `:` label and trailing-`@` output) moves to Appendix D.


## Preface — the edition ledger

### Revision note (Frame-QL Second Edition) — the mechanical sync

The Second Edition changes no doctrine. It is a **mechanical sync** of the First Edition's text to the shipped package through **columna-core 0.14.0 / 0.13.4** — names, pins, reason codes, and version stamps brought level with what the parser and planner actually do. The rule the desk keeps for its own transcripts is now the manual's: **every FrameQL example is verified against the running parser, not written from memory** (the standing self-check of `docs/tools/check_manual_frameql.py`, run against the shipped columna-core — 0.18.1 at this revision). Each change is flagged in place with a **▸ Second-Edition sync** note. The ledger:

1. **Column identity is the canonical expression, not a mechanical default** (WP-NAME-1, 0.14.0; **wire contract `"1"` → `"2"`**). The `<reducer>_<measure>` default (`sum_revenue`) and the dot-to-underscore mangle (`revenue_sum`) are **retired** — both were invented names, and the input anchor they dropped is half a pinned reduction's denotation (the Two Anchors law). An unaliased series is now keyed by its **canonical expression, verbatim**: `avg(revenue @ {day})` keys as `avg(revenue @ {day})` (the pin visible in the key), a bare measure as `revenue`, member access as `revenue.sum` (dotted, unmangled). `EXPLAIN` emits no redundant `X AS X`. Consumers needing a stable handle key on an `AS` alias, which is author-owned and changes under no future rule. The bump carries exactly one thing — the default key of an unchanged utterance; no value, mood, disclosure, or reason code moves. (Chapters 1.6, 2.7; Appendix D.)
2. **The composite input anchor: a product grain is a first-class pin** (WP-GRAIN-1, 0.13.4; no wire change, contract stays `"1"` at that release — a minted reason routes by outcome). An inline reduction's input anchor may pin a **product** of levels — `avg(revenue @ {store*product*cal.month})` — not just one. Two reason codes are minted inside the existing vocabulary: **`pin_coarser_than_output`** (REFUSE, Law 1 — a pin level coarser than the output grain cannot resolve at a finer output) and **`redundant_pin`** (CLARIFY, Law 2 — two cross-comparable pin levels fix one axis, not two). Law 4 generalizes the immaterial two-stage-statistic provenance note (still a **serve**). One corner is rowed out: a composite pin whose product includes a *faced* output coordinate meets the G4 chain guard and refuses **`chained_crossing`** — a named refusal, never a silent number. (Chapters 2.3, 2.7; Example 6.16; Chapters 5.6, 7.3.)
3. **`co_anchor_ambiguous` is tombstoned** (retired 2026-07-16 under the §2c expression law; a retirement-pin test asserts it is never emitted). The First Edition named it the "multi-input case" of the unpinned-reduction clarify; the shipped planner emits **`input_anchor_ambiguous`** there (one reason per contested dimension — OF-1), and the cross-universe rate the reason originally named is now the **`cross_universe`** category error (Chapter 2.5), not a clarify. The spelling is kept as a dated tombstone so old transcripts stay interpretable — vocabularies grow by rule and shrink by tombstone, never silently. (Chapters 2.3, 7.3.)
4. **Version stamps.** The Second Edition sync documented columna-core **0.14.0** as implemented (preface, harness note, Chapters 2.8–2.9, Appendix B) and cited wire contract **`"2"`**. The retired terse `@`-fragment (Appendix D) and the grow-by-ruling surfaces are unchanged.
5. **The RELATE face triad completed** (0.12.0; scope amendment to phase (a), ratified 2026-07-31 — shipped-reality drift, the same class as the version stamps). The First Edition documented **`touch` only**, with `assign`/`alloc` declared-but-deferred; 0.12.0 shipped the full triad and all three now execute. Chapter 5.6 now documents each face as the engine emits it: `touch` (over-count, **disclose**), `assign` (`ASSIGN BY … ORDER MIN|MAX`, single-count reconciling to the grand total, shadow `memberships_unrepresented`, **disclose**), and `alloc` (`ALLOC BY …`, weighted split reconciling to the cent, the reconciliation badge `{crossed_total, base_total, delta, tolerance, status}`), plus the fail-closed per-scheme adjudication, the **G5** anchor law (a distinct-class measure refuses at every face), and the **G4** chain guard. (Wire additive; `contract_version` stayed `"1"` at that release.)
6. **Wire counters `executed` / `fetches_delta`** (additive to contract `"2"`, no doctrine). The annotation carries two server-surface execution counters — `executed` and `fetches_delta` — emitted on both the plan (`EXPLAIN`) and run paths. They are a server-surface detail, not a language feature; they move no value, mood, disclosure, or reason code, and grow no wire chapter here.

### Revision note (Frame-QL First Edition)

This edition is the vetted Third-Edition text, renamed and reconciled. The reconciliations are small and are flagged in place with a **▸ Frame-QL revision** note. The ledger:

1. **Many-to-many aggregate-across (fan-out) is a clarification, not a served disclosure** (Chapters 5.6, 7.3, 7.4). Under the column-foundation (ADR-031) the engine *transports* along functional edges and never *joins*; a non-functional (M:N) edge is therefore not a traversable path, and the membership aggregation the Third Edition served is not expressible without a declared resolution. The unmet precondition is reported, *statically and before execution*, as a clarification naming the same three remedies. This replaces "serve membership with overlap disclosure" for the undeclared case.
2. **The inform-and-serve boundary is the planner/engine boundary** (Chapters 5, 7.2). Everything statically catchable — ambiguity, unknown operator, unknown column, type mismatch, non-traversable edge, governance/access — is decided by the *planner*, before resolution, and may yield a clarify/refuse with no result. Analytical risk that survives to the *column engine* is served-and-disclosed, never withheld. A B-anchor crossing is *detected* at the planner (it attaches the critical disclosure) and may be *downgraded* to a route-around at the engine (Chapter 5.3); the number is always served.
3. **Mule recompute is recompute-from-base at the output grain** where no fertile decomposition exists (Chapter 7.4, Appendix A) — stated explicitly, consistent with the Third Edition.
4. **Universe depth.** The `(anchor, universe)` grain is unchanged at the language surface; the basis-driven empty-bucket rule is **corrected** (Chapter 1.5, columna#148) — the basis still fixes which points the frame expects, but what an absent value *means* is now the measure's fill rule Φ, not the universe basis. Beneath the surface, Columna enriches *universe* with a population-consistency layer (support reconciliation across a universe's columns; path-independence of a reduced total across anchorings). This is semantics under the syntax, not new syntax.
5. **The envelope is the language; the terse `@`-fragment is retired** (Preface; Chapters 1–4; Appendix D). The pre-launch surface spelled the output anchor with a trailing `@` (`aov @ cal.month`); the ratified envelope (ADR-035) makes `@ {…}` the input-anchor marker *universally* and `AT {…}` the sole output-grain declaration, and adds the `FROM`/`WHERE`/`HAVING`/`ORDER BY`/`LIMIT … PER`/`WITH` clauses. This edition documents the envelope as implemented; the terse form moves to Appendix D (lineage). **`FROM` is optional** — it defaults to the bound Manifold and is required only where a surface holds more than one (Chapter 1.3).
6. **The fourth mood is `refuse`, not `inform`** (Chapter 7). The shipped wire's four moods are **serve · disclose · clarify · refuse**. The withholding outcome this manual's Third-Edition lineage called *inform* (ADR-020's "inform-and-serve" doctrine) is the wire's `refuse`; the doctrine's spirit — withhold only structurally, disclose analytical risk — is unchanged, and this edition uses `refuse` throughout. (The separate `cross_universe` category error rides the query-**error** channel, not a mood — Chapters 2, 7.)
7. **Structurally prohibited reductions refuse; Disclose cannot legalize them** (Chapters 5.3, 7.2, 7.3, 7.4). *(Ratified 2026-08-20 — ADR-036, superseding ADR-020's inform-and-serve rule for this case only.)* A reduction that travels a lineage its operator is declared `BLOCKED` along has no lawful reading, so it is **refused** (`blocked_reduction`; no values on the wire), in *every* spelling: written as a declared family member (`level.sum`), **generated** by an inline reducer above a lawful sibling (`sum(level.last @ {day})`), or wrapped in a unary, binary, scalar, scan or `DERIVED` carrier. *Family generation creates a new analytical family. It does not create a new operator permission.* Applicability stays **per operator × lineage** — there is no stock/flow/rating type (ADR-031 D5 clarified, not reversed): summing a stock across *stores* stays lawful, and `avg`/`min`/`max`/`count` over a stock across time stay lawful, because the author barred `sum` and barred nothing else. The disclosure code `b_anchor_crossing` is **tombstoned as a producer** and retained, still wired, so archived wires and deposited transcripts still resolve (7.4). `CONTRACT_VERSION` stays `"3"`; the reason string is additive on the existing Refuse channel.


## Inline provenance notes lifted from the manual

These were parentheticals attached to catalog entries and paragraphs. They recorded when a
claim entered or changed; none of them is current law.

- ▸ currency update, 2026-09-01: those current-state stamps now read **columna-core 0.18.1** and contract **`"4"`** — see Currency above. This ledger row is left as the record of what the Second-Edition sync did; the sync itself is not restamped.
- ▸ shipped-law reconciliation, 2026-08-20, ADR-036: the last clause no longer holds for the **structurally prohibited** reduction. A reducer travelling a lineage it is declared `BLOCKED` along is refused at the planner, before any number exists — see item 7 below and Chapter 5.3. The boundary itself is unchanged: everything statically catchable is still decided by the planner, and analytical *risk* surviving to the engine is still served-and-disclosed.
- ▸ Frame-QL revision, shipped-law — `[SCHEDULED]`: explicit version pinning — a `VERSION n` on `FROM` — is **designed but not yet in the shipped envelope grammar**; it enters by ruling (ADR-035 D1), not by default. `[SCHEDULED]` (not `[ROADMAP]`) because the surface is designed and committed, only unshipped — the resolved version is always disclosed today, so nothing is lost by pinning arriving later.
- ▸ shipped-law reconciliation, 2026-08-20, ADR-036: this read "served, if at all, only with the corresponding critical disclosure" until the crossing became a structural refusal.
- ▸ shipped-law reconciliation, 2026-08-20, ADR-036: **B-anchor crossings left this list.** A crossing is not a risk attached to a lawful answer; it is an operation the governed law does not grant, and it is refused — §5.3.
- ▸ shipped-law reconciliation, 2026-08-20, ADR-036: the third limb is new, and it is not an analytical-risk withholding. The four moods sort by **lawfulness**, not by confidence — *serve*: lawful, no material condition; *disclose*: lawful, a material condition travels with the answer; *clarify*: several lawful meanings remain; *refuse*: no lawful path exists.
- ▸ shipped-law: this is the wire's fourth mood, `refuse`. The Third-Edition lineage called it *inform*, under ADR-020's "inform-and-serve" doctrine — same outcome, same spirit; the shipped name is `refuse`.
- ▸ 2026-08-20, ADR-036: "determinate and producible" is to be read as **lawful** and producible. A structurally prohibited reduction is arithmetically determinate and is still refused — the prohibition is on the operation, not on the confidence of its answer — and no fifth outcome is minted for it: it is an ordinary `refuse`.
- ▸ shipped-law reconciliation, 2026-08-20, ADR-036: the menu enumerates the **lawful** candidate pins only. Where exactly one candidate is lawful nothing is contested, so the framework proceeds on the defaulted anchor and owes the material `input_anchor` note; where **none** is lawful the ask refuses `blocked_reduction` rather than clarifying, because an unlawful reading is not a choice the asker can be offered — offering it is how a reader gets talked into a laundered answer one keystroke later.
- ▸ shipped-law reconciliation, 2026-07-17: the input anchor is written inline — `avg(revenue @ {day})` — and a composite pin `@ {a*b*c}` is admissible, §2.3.
- ▸ Second-Edition sync: the First Edition named the multi-input case `co_anchor_ambiguous`; that reason is **tombstoned** (retired 2026-07-16, §2c expression law; never emitted) — the planner emits `input_anchor_ambiguous` per contested dimension, and the cross-universe rate the reason once named is now the `cross_universe` category error below.
- ▸ Second-Edition sync: minted 2026-07-30, WP-GRAIN-1.
- ▸ currency addition, 2026-08-22: shipped code named here for the first time; the condition is long-standing.
- ▸ currency addition, 2026-08-22: shipped code and channel recorded as emitted. The taxonomic question — whether the manual's clarify framing or the shipped error channel is the intended reading — is left open here rather than settled in a documentation pass.
- ▸ shipped-law reconciliation, 2026-07-17: net-new — the retired cross-universe "wedge" lands here.
- ▸ Frame-QL revision: made explicit; the planner typechecks operator names against the registry before resolution.
- ▸ Frame-QL revision: made explicit; signatures are checked at the planner.
- ▸ Frame-QL revision: under the column-foundation this is a clarification, not a served membership aggregation.
- ▸ shipped-law reconciliation, 2026-07-17: the shipped envelope planner raises `filter_unreachable` for a `WHERE` predicate whose dimension no series' input grain can reach.
- ▸ shipped-law reconciliation, 2026-08-20, ADR-036: minted here, and moved here **from 7.4**, where ADR-020 had placed it as a served critical disclosure. **Family generation creates a new analytical family. It does not create a new operator permission.** Scope is unchanged — per operator × lineage, no stock/flow type: `sum` of the same stock across *stores*, and `avg`/`min`/`max`/`count` of it across time, all stay lawful.
- ▸ Second-Edition sync: minted 2026-07-30, WP-GRAIN-1.
- ▸ currency addition, 2026-08-22: minted 2026-08-19, after the Second-Edition sync point.
- ▸ currency addition, 2026-08-22: minted 2026-08-20, after the sync point.
- ▸ currency addition, 2026-08-22: minted 2026-08-20; the law was already documented at 5.6, the code was not named here.
- ▸ currency addition, 2026-08-22: shipped code named here for the first time; the condition is long-standing.
- ▸ shipped-law reconciliation, 2026-08-20, ADR-036: **B-anchor violations are no longer in that list.** The Third-Edition taxonomy refused them; ADR-020 moved them here to 7.4; ADR-036 returns them to the refusals above — this time as a structural prohibition rather than an analytical judgment, which is precisely the distinction the intervening reading lacked.
- ▸ Frame-QL revision: this served-disclosure applies to a join-capable engine; under the column-foundation the undeclared case is a planner clarification, not a served result — see the revision note in Chapter 5.6.
- ▸ 2026-08-20, ADR-036: unchanged, and now unambiguous — a severity never withholds, because everything that reaches a disclosure is already lawful. What withholds is the prior question of §5.3: whether the governed law grants the operation at all.
- ▸ shipped-law reconciliation, 2026-08-20, ADR-036: the third clause is new, and it is *structural* in exactly the sense the sentence already claims — it reads a declaration the author wrote, not an opinion the engine formed. The author declares `BLOCKED { calendar }` once; the engine enforces it everywhere, including in the spellings the author never anticipated.
- ▸ 2026-08-20, ADR-036: the engine's clause gained its third limb. Note what did not change — the engine still forms no analytical opinion of its own; declining a blocked reduction is the author's `BLOCKED` declaration being carried out, in every spelling of it.


## Preface — the Second Edition subtitle

*Frame-QL Second Edition — a mechanically-reconciled continuation of the Frame-QL Manual, First Edition (which it supersedes). This edition preserves the First Edition's text and syncs it to shipped reality through **columna-core 0.14.0** (wire contract `"2"`): the canonical column identity of WP-NAME-1 (0.14.0), the composite input anchor of WP-GRAIN-1 (0.13.4), the minted and tombstoned reason codes, and the version stamps — each change flagged in place with a **▸ Second-Edition sync** note and ledgered below. The First Edition was itself a renamed, lightly-revised continuation of the Coframe-QL Manual, Third Edition (which it superseded): it renamed that text to Columna/Frame-QL/Manifold and reconciled it to the column-foundation redesign (ADR-031), the edition split it then carried (since retired — topology record §17.5), and the shipped **envelope grammar** (ADR-035). It inherits the v4 operator model (ADR-009…015), the V/M/B anchor vocabulary (ADR-024), the anchor-ascription rule, family-aware scans, macro bindings, EXPLAIN, and the (anchor, universe) grain (ADR-025…028). The **envelope** — `SELECT <series> [AS <alias>], … AT {anchor}` with its optional `FROM`, `WHERE`, `HAVING`, `ORDER BY`, `LIMIT … PER`, and `WITH` clauses, where `@ {…}` is the input-anchor marker universally and `AT {…}` is the sole output-grain declaration — is the language, and this edition documents it **as implemented** (columna-core 0.18.1). The pre-launch shipped surface was a *fragment* of it — the terse `cols @ anchor` form, where a trailing `@` spelled the output anchor; that fragment is **retired** (its two `@`s meant opposite things) and preserved for lineage in Appendix D. The fourth outcome, named `inform` under ADR-020's inform-and-serve doctrine, ships on the wire as the `refuse` mood; this edition uses **`refuse`** throughout (Chapter 7). The §2c universe law (structural universe resolution; one expression, one universe; `cross_universe`), the corrected B3 basis rule (the basis fixes which points the frame *expects*; a measure's fill rule Φ fixes what an absence *denotes* — columna#148), and the shipped reason codes are reconciled into the semantics they govern.*
