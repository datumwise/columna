# Changelog

All notable changes to **columna-server** are recorded here
([Keep a Changelog](https://keepachangelog.com/)).

## [Unreleased] — 0.10.0 — the provisioner

**A compiled image becomes a runtime unit the server will admit — assembled, never re-emitted.**
Core-P1 K0 produces a governed publication's execution image and the receipt binding the two; nothing
yet placed them, together with deployment configuration, into the folder the store consumes. The
provisioner is that step, and it is deliberately the smallest thing that can be:

    governed-publication.json + manifold.cml + lowering-receipt.json + operator config
        -> <runtime-manifold>/

**It copies bytes; it does not re-emit them.** The lowering receipt binds a publication to an image by
content digest over the files AS SHIPPED, with no canonicalization — so a provisioner that
re-serialized the publication to an equivalent JSON, or reformatted the `.cml`, would produce a unit
whose receipt no longer describes its own files. The binding the compiler established survives
provisioning unchanged, and byte-copying is the only thing that guarantees it. A test writes the same
publication with `indent=2` and the provision refuses: semantically identical, bytewise different, and
the refusal is reporting the truth.

**It verifies by recomputing, and refuses rather than repairing.** Three sources must name the same
publication — the artifact's `ref`, the image's `SOURCE_MANIFOLD` claim, and the receipt's binding —
and both digests are recomputed over the bytes about to be copied. Identity is checked *before*
digests, so pairing unrelated artifacts reports which publication disagreed rather than an opaque hash
difference. Re-deriving a receipt to match the files would turn "these artifacts belong together" into
"these artifacts have been made to agree"; there is no receipt builder in the module, so it cannot.

**It is an assembler, not a semantic authority.** Nothing in it constructs a Manifold. The one thing
it reads from the `.cml` is a single `SOURCE_MANIFOLD` statement — an identity claim, the same one
`registry.source_ref_of` reads — obtained without parsing the image, because reading which publication
an image claims is not reading what the image means. Deployment configuration is written verbatim:
connector choice and warehouse location are operator decisions, not derivable facts.

Five refusal conditions — `MissingInput`, `MalformedInput`, `IdentityDisagreement`, `DigestMismatch`,
`DestinationNotEmpty` — and a refusal writes nothing at all: the unit is staged beside the destination
and moved into place with one rename, so a failed provision leaves neither a half-unit nor a staging
directory.

No fixture is promoted. The packaged demos carry no `SOURCE_MANIFOLD`, remain `legacy`, and a test
re-verifies their bytes are untouched after a provision runs beside them.

## [Unreleased] — 0.9.0 — the ExecutionProvider seam (S1.1) + optional execution diagnostics (S1.2) + shared Manifold identity/registry (S2.1) + governed publication serving (S2.2) + the publication→image binding

**The lowering receipt — governed standing now requires established provenance, not an origin claim
(milestones 1–3, ruling 2026-08-22).** `ENTRY_GOVERNED` previously followed from a publication
artifact plus a matching `SOURCE_MANIFOLD`. That pair is an ORIGIN CLAIM — a `.cml` asserting which
publication it came from — and anyone able to write the runtime folder could type it, so arbitrary
co-location of any artifact with any realization was sufficient. Semantic conformance belongs to
Core-P1 lowering by construction (the compiler's only inputs are the publication and the private
mapping, and it fails closed when governed law cannot be faithfully represented); a fourth file now
carries that discharged obligation across the lowering→provisioning→admission boundary:

    <runtime-manifold>/{governed-publication.json, manifold.cml, lowering-receipt.json, data.toml}

`lowering-receipt.json` binds one publication ref to two content digests — the artifact and the
execution image, **as shipped**, no canonicalization. Admission verifies all three locally and grants
governed standing only when they agree; anything else is compatibility-served with an observable
condition. Verification never loads the private mapping, never reconstructs meaning from the `.cml`,
and never re-runs lowering, so the blast wall is untouched: `GovernedPublication.logical` still comes
only from the artifact.

**The receipt establishes publication→image and nothing else.** It is not certification, not
attestation, and not `PublishedScope` admission — a governed unit's `published_scope` and `evidence`
are byte-identical to the same image served as a legacy runtime, and a test asserts it. Binding
identity is deterministic for identical inputs: `compiler` and `mapping_provenance` are retained as
opaque provenance and `established_at` as a non-authoritative timestamp, none participating in the
binding and none a runtime admission dependency.

Three additive condition codes inside `contract_version` `"3"` — the catalog's shape is unchanged and
only the value set grows: `lowering_receipt_missing`, `lowering_receipt_invalid`,
`lowering_receipt_mismatch`. A new completeness test pins that every `LoadCondition` kind the store
can emit has a stable public code, since `list_manifolds` skips unmapped kinds and an omission would
delete a deployment condition from the catalog rather than surface it.

No fixture is promoted and no legacy semantics are weakened: the packaged demos carry no
`SOURCE_MANIFOLD` and remain `legacy`. There are zero governed deployments today, so the requirement
lands with no migration burden — which is why it lands now. Compiler, `PrivateCoreMapping`,
provisioner and the first public governed fixture (milestones 4–7) remain behind the Core-P1
checkpoint; test-constructed receipts exercise the admission contract and are not an end-to-end
governed-producer proof.


**S2.2b-2 — governed publication catalog (WIRE `contract_version` `"2"` → `"3"`).** `list_manifolds`
is now a governed publication **lineage** catalog, not a runtime-folder inventory: one row per
governed `manifold_id` with `versions[]` + `latest_version` (publication facts) and per-version
`realizable` (an installation fact — publication existence and local realizability are separate),
plus explicitly classified `legacy` / `authority_incomplete` compatibility runtimes (keyed by
`runtime_id`; the latter carries `source_ref` + stable `conditions[]` from a fixed code vocabulary —
never raw details/paths/exception text). Rows are deterministically ordered (governed by
`manifold_id`, then legacy, then authority-incomplete by `runtime_id`); `versions[]` ascending semver.
Per-realization fields (`name`/`description`/`n_measures`/`universes`) were dropped — `describe` is the
detail surface. `list_versions` was deliberately not added.

**S2.2b-1 — version-aware public selection + resolved-publication disclosure (additive; contract still
`"2"` at the time).** The 9 publication/execution-scoped tools take an optional `version`; resolution
is governed-first (a governed lineage outranks a same-named compatibility folder, deterministically),
and every governed response discloses the concrete `{manifold_id, manifold_version}`. Compatibility
runtimes stay unversioned (no fabricated version). Two request-time structural errors:
`publication_not_found`, `not_realizable_here`.

**S2.2a-3 — server ingests the governed publication artifact.** `GovernedPublication.{ref,logical,
authority}` come exclusively from a co-located `governed-publication.json` (read with stdlib JSON; no
`manifold_agent` dependency), never from `logical_spec(.cml)`. A Core provider binds only when
`artifact.ref == .cml SOURCE_MANIFOLD` (else `RealizationIdentityMismatch`, no bind). Three runtime
kinds: `legacy`, `source_referenced_incomplete` (authority-incomplete, compatibility-served, never
governed), `governed`. Observable `store.conditions()`.

**S2.1 — shared Manifold identity, internal only (no wire/API change).** A Manifold is now identified
by a governed publication, not a folder layout or a `.cml` runtime artifact. New `columna_server.registry`:
`ManifoldSelector{id, version?}` (a convenience input; `version=None` ⇒ latest) resolves to a
`ManifoldRef{id, concrete version}` — **never ambiguous**; no implicit `None` survives resolution.
`GovernedPublication{ref, logical, authority}` is immutable meaning — a physical-clean logical
projection (`logical_spec`) plus publication authority/provenance — and deliberately **excludes**
runtime standing (`PublishedScope`, adjudication, attestation, provider availability). A
`ManifoldRegistry` (`list`/`resolve`/`latest`; "latest" = highest semantic version, never lexical or
filesystem recency) answers *WHICH*; the store answers *HOW* via `ResolvedManifold{publication,
provider?}` (`provider is None` ⇒ **not realizable here**, an availability state distinct from
`publication_not_found`, never routed through the four analytical moods). `ManifoldStore` becomes the
first local implementation (`FolderManifoldRegistry` over parsed `.cml` folders): a `.cml` carrying a
complete `SOURCE_MANIFOLD id VERSION semver` is a governed publication; a source-identity-less `.cml`
stays a **legacy runtime entry** — compatibility-served, id-only, never promoted and never given an
invented id/version/ratification (the P0(c) "recover access, never manufacture governance" rule). The
compatibility surface (`get`/`ids`/`all`) and every existing server behavior are unchanged.
*Deferred/recorded:* the P0(c) ratification record lives in the Studio publication bundle, not the
`.cml`; a registry over bare `.cml` carries source identity but not the ratification record
(`authority.ratification` is left `None`, not fabricated) — ingesting publication bundles is a later
step. The public MCP/API surface (optional `version`, resolved-version disclosure, `not_realizable_here`
behavior) is S2.2.



**Internal seam; no behavior change, no wire change, no API change.** The MCP serving surface no
longer knows that its execution provider is `ManifoldServer + ColumnEngine`. A new
`columna_server.provider.ExecutionProvider` protocol carries the per-Manifold execution capability
(`run` / `plan` / `explain` / `operators` / `published_scope`); the sole implementation,
`CoreExecutionProvider`, is a 1:1 adapter over today's Core runtime and is the only server-side object
that knows `ManifoldServer`. `LoadedManifold` now exposes `.provider` (execution) and `.manifold`
(logical/read model) and **no longer has a `.server` field** — so `tools.py`/`recapture.py` cannot
reach a concrete runtime through it. Result shapes stay opaque at the seam (the wire duck-types them),
so a future non-Core provider need not instantiate any `columna-core` dataclass. Every governed
result, refusal, disclosure, plan, explanation, operator exposure, and published scope is unchanged
(the full wire/recapture/trial/MCP suites pass byte-identical).

**S1.2 — execution diagnostics are optional.** The `fetches` metric that backs the wire's optional
`fetches_delta` is no longer a mandatory provider capability. A separate, optional protocol
`SupportsExecutionDiagnostics` exposes `execution_diagnostics() -> Mapping[str, int]` (cumulative,
provider-defined counters; Core reports `{"fetches": N}`). The server derives `fetches_delta` only
when the provider reports a `fetches` counter, and emits nothing otherwise — **absent ≠ zero**: it
means the provider exposes no such diagnostic, never "zero", "unknown", or "failure". Core's
`fetches_delta` (and the zero-fetch guarantee on plan/explain/check) is byte-identical. No wire
object, no contract-version bump, no generalized telemetry field; the Core-internal `explain` path is
untouched. Diagnostics observe execution; they never participate in analytical adjudication (proven by
a test that removes the capability and gets the same frame/mood/disclosures, only the diagnostic field
changing). `operators` / `published_scope` remain provisional on the provider.

## [0.8.2] — mcp 2.0 broke every fresh install; the cap is the fix, the guard is the point

**BUG FIX, user-visible and total: for roughly 17 hours, `pip install columna` produced a package
that could not start.** No code in this repository changed. The break arrived by resolver.

**THE TIMELINE, plainly** (all UTC):

| when | what |
|---|---|
| 2026-07-27 | 0.13.2 published; public launch. `columna-server` declares `mcp>=1.0` — **no ceiling**. |
| 2026-07-28 **13:41:40** | upstream publishes `mcp 1.29.0` — the last of the 1.x line. |
| 2026-07-28 **13:45:28** | upstream publishes **`mcp 2.0.0`**, four minutes later. It moves/removes `mcp.server.fastmcp`. |
| 2026-07-28 ~13:45 → 2026-07-29 | every *fresh* install resolves `mcp>=1.0` to 2.0.0. `columna-server demo --play` dies on `from mcp.server.fastmcp import FastMCP` — `ModuleNotFoundError`, exit 1, **before a single mood prints**. |
| 2026-07-29 **03:47** | our own CI goes red on `main` — on a **specs-only merge** (PR #110, no code). The red was the upstream break surfacing, not the PR. |
| 2026-07-29 | 0.8.2: `mcp>=1.0,<2.0`. Fixed. |

Anyone who installed before 13:45 on the 28th has a working environment and is unaffected; their
resolver already picked a 1.x. The victim is precisely the person the quickstart is written for —
a stranger, arriving after launch, typing the command on the install page for the first time.

**THE FIX**: `mcp>=1.0,<2.0` — which resolves to `mcp 1.29.0`, published four minutes before the
break. The floor stays at 1.0: nothing about our use of the 1.x surface changed.

**THE DOOR IS NAMED, NOT CLOSED.** The cap lifts to `<3.0` when `server.py` is ported to the 2.x
import path *and* the MCP stdio acceptance suite is green against it — a port, on its own beat, not
a hotfix at speed. A cap is not a refusal to move; it is a refusal to move by accident, on a
stranger's machine, at install time.

**THE DOCTRINE — an uncapped dependency is an UNTESTED CLAIM.** `mcp>=1.0` asserted that every
future major version of somebody else's package would keep our contract. That claim was made before
those versions existed, and it was checked by nobody. This is the *same* doctrine 0.13.2 wrote down
for `requires-python` (*fail closed with a named reason beats rare success*), applied where it
should have been applied at the same time. Twice is a class.

**SO THE REAL SHIP IS THE GUARD, NOT THE CAP** — `scripts/assert_dep_caps.py`, wired into CI on
every push and PR: **every dependency, in every package, must carry an upper bound**, including
`optional-dependencies` and `build-system.requires`. It fails, naming the offender. It runs with no
path filter and on push as well as PR, because this failure class arrives *without a diff* — the
repo that breaks is byte-identical to the repo that worked yesterday. Guarding the instance fixes a
day; guarding the class is why there will not be a third.

**AND ONE MORE THING THE OUTAGE EXPOSED, which the cap alone would have hidden.** `ci.yml` installed
the server's dependencies from a **hand-copied** spec (`pip install "mcp>=1.0" ...`) rather than from
the package metadata. So CI was never testing the shipped constraint — a cap could be right in
`pyproject.toml` and wrong in CI, indefinitely, with everything green. CI now installs
`-e "packages/columna-server[test]"` and resolves from the real metadata. The install path under
test is the install path that ships.

**The full cap sweep, this release** (nothing else changed; no surface, wire, or behaviour —
`contract_version` stays `"1"`):

- `mcp>=1.0` → **`mcp>=1.0,<2.0`** ← the fix
- `tomli>=2.0` → `tomli>=2.0,<3.0`
- `columna-core>=0.13.2` → `columna-core>=0.13.3,<1.0`
- `[http]`: `uvicorn>=0.23,<1.0`, `starlette>=0.37,<2.0`
- `[agent]`: `anthropic>=0.40,<1.0`
- `[test]`: `pytest>=8.0,<10.0`, `pytest-asyncio>=0.23,<2.0`
- `build-system`: `hatchling` → `hatchling>=1.27,<2.0`

**Internal caps sit at the MAJOR, deliberately not the minor.** `columna-core>=0.13.3,<0.14` would
deadlock our own lockstep — core moves to 0.14.0 while this server needs no change, and the
umbrella, which requires both, becomes unresolvable. For internal packages the **floor** carries the
contract (0.8.0: *"a FLOOR, not a preference"*); the cap marks the wholesale-break boundary. A cap
that can brick an install is not a safety measure.

## [0.8.1] — the declared Python ceiling, and the demo survives Windows

**BUG FIX, user-visible: `demo --play` crashed on Windows whenever stdout was not a console.**
Found by the new windows-latest CI leg **on its first run** — which is the entire argument for
adding it. `columna-server demo --play | anything` (or `> a file`) died with
`UnicodeEncodeError: 'charmap' codec can't encode` **on the opening line, before a single mood
printed**. Python writes to a Windows *console* through the wide-char API, so an interactive run
looked fine; the moment stdout became a pipe it fell back to the locale encoding — cp1252 on a
default en-US Windows — and our output is legitimately non-ASCII (U+2500 rules, em-dashes, and wire
JSON dumped `ensure_ascii=False` so non-ASCII labels serve as themselves rather than `\uXXXX`).

**The fix is at the stream, not in the text**: `columna-server` now declares UTF-8 on stdout/stderr
for every subcommand, with `errors="backslashreplace"` so an unrepresentable character prints an
escape rather than truncating the transcript mid-flight. Stripping the characters to ASCII would
have made the demo lie about what the wire carries, and would have left the next non-ASCII value to
crash somewhere quieter.

Guarded twice: the Windows CI leg is the real proof, and
`test_demo_play_survives_a_cp1252_stdio_locale` reproduces the exact failure on **any** platform via
`PYTHONIOENCODING=cp1252`, so the class fails in the unit suite in under a second. That test asserts
the rules and em-dashes are still *present* — it fails if someone "fixes" this by removing them.



**PACKAGING CHANGE, no code change.** `requires-python` moves to `">=3.10,<3.14"`, matching
`columna-core`; the floor on core rises to `>=0.13.2`. PATCH, not minor: no surface, wire, or
behaviour changed — `contract_version` stays `"1"`.

Declared here rather than inherited transitively so `pip install columna-server` on its own also
refuses cleanly on 3.14, instead of discovering the ceiling one dependency deep. Classifiers now
enumerate 3.10–3.13 (they previously named only `Python :: 3`).

See `columna-core` 0.13.2 for the finding, the doctrine, and the named door (WP-1.1).

## [0.8.0] — the describe surface follows the ASSERT retirement

Requires `columna-core>=0.13.0` — a FLOOR, not a preference: this release's contract is defined by
what core 0.13.0 removed, so `>=0.12.0` would admit a resolution whose wire still carries the fields
this version says are gone.

MINOR, not patch: no server code path changed behaviour by intent, but the DESCRIBE SURFACE CHANGED,
and a surface change is not a patch even when it arrives by cascade from the engine.

- **Fields removed from the describe wire** (with `ASSERT`, ruling 2026-07-26): the `asserts` block,
  the universes' `attributes`, and `published_scope.cut` / `cut_by`. The CUT region retired with the
  construct that defined it.
- **`contract_version` stays `"1"`.** The retirement is a REMOVAL from a block consumers were never
  required to read; the envelope and the four moods are untouched.
- **`conflicting_data` can no longer occur.** Its reason code is tombstoned, not reused.
- **Guarded, not asserted:** `test_describe_insulation.py` proves the absence in both directions —
  `asserts` not on the wire, `cut`/`cut_by` not in `published_scope`.

## [0.7.1] — the category-driver descriptions (data-only)

Patch, DATA-ONLY: no code, no wire schema, no contract change. Requires `columna-core>=0.12.0`.

- **The two category-profile driver measures gain their descriptions.** `priority` and `alloc_weight`
  shipped 0.7.0 with empty describe descriptions — their folklore was written on the line *after* the
  `MEASURE`, which the parser (DESCRIPTION lives on the header, before the `FAMILY` block) does not
  read. Moved inline before `FAMILY` and ratified (Huayin 2026-07-24):
  - `priority` — "the category's assignment rank — 1 ranks first; drives the primary face"
  - `alloc_weight` — "the category's relative allocation weight — normalized per product at the
    crossing; drives the split face"
  So `describe_manifold`, the Explorer, and the spec all carry them. No parser change (the placement was
  the defect). Verified: both flow to the wire; 135 server tests green.

## [0.7.0] — the triad on the wire, and the third Cascadia universe

Requires `columna-core>=0.12.0` (the assign/alloc faces + the anchor law).

- **Third universe.** Cascadia gains `category_attributes` (12 rows: a distinct `priority` 1..12 and a
  raw, varied `alloc_weight`, md5-deterministic / byte-reproducible) and `UNIVERSE category_profile =
  category BASIS spine` with the two driver measures. The RELATE declares two more faces beside `touch`:
  `primary = ASSIGN BY priority ORDER MIN`, `split = ALLOC BY alloc_weight` (descriptions are DRAFT,
  ratified at the merge gate).
- **Wire.** `describe_manifold`'s `relates[].faces[]` gains `driver`; query answers carry the assign
  **shadow** (`memberships_unrepresented`) and the alloc **reconciliation** badge. Additive — the VIA
  bridge stays map-layer; `contract_version` stays `"1"`.
- **Exhibits.** E11 (`revenue AT {category.primary}`) discloses the shadow (270 memberships, total ≡
  the grand total $2,212,391.86); E12 (`revenue AT {category.split}`) serves with the reconciliation
  badge (total ≡ the grand total to the cent). Recorded via the standing seed pipeline; the /case copy
  comes to the desk post-build.

## [0.6.1] — warehouse coherence (data-only)

Patch, DATA-ONLY: no code, no wire, no contract change. Requires `columna-core>=0.11.0` (unchanged).

- **The Cascadia demo warehouse now COHERES with its transaction ground truth.** A stranger-read of the
  generated exhibits (verified at the desk) found the reference/summary tables had drifted incoherent:
  FK coverage was 2,051/19,995 (customers held 2,000 of ~10,157 distinct transaction ids) and the
  summaries ran 10-15× off base truth — which *contradicted the ratified burn story*, where the stale
  summaries are *plausibly* wrong, never wild. `transactions` and `eom_inventory` are untouched (every
  recorded number delivers from them); the reference/summary tables are regenerated DERIVED-THEN-
  DEGRADED, each wearing exactly its one story-sin (`customers` grows to 10,157 = full FK coverage;
  `daily_revenue_summary` = true daily revenue minus its 15 missing days; `monthly_avg_order_value` =
  the transaction-for-order substitution; `monthly_unique_visitors` = a per-store double-count;
  `monthly_store_inventory` = the illegal sum-of-stock-over-time; support/engagement redrawn from the
  real customer distribution, engagement covering ~half).
- **A new permanent suite** (`test_warehouse_coherence.py`) makes the class structural — 100% FK
  coverage, each summary within its declared-sin tolerance of base truth, the engagement ratio.
- **Byte-stability guarded:** the E1-E10 seeds and both transcripts' numbers are byte-stable across the
  regen (the served measures deliver only from the untouched facts).
- Regeneration harness: `scripts/regen_warehouse.py` (deterministic, reproducible).

## [0.6.0] — RELATE faces go visible (the crossing served, and shown)

Requires `columna-core>=0.11.0` (the faces mechanism). `contract_version` stays `"1"` — `relates[].faces[]`
is additive, the DESCRIPTION precedent.

- **`describe_manifold`'s `relates[]` gains `faces[]`:** each declared crossing disposition rides describe
  as data — `[{name, scheme, description}]` — so a consulting agent (and the clarify-as-menu) sees the
  disposition from the source of truth before spending the query. Logical fields only; the `VIA` bridge
  stays MAP-LAYER (engine-visible, never on the wire) — the §2b insulation test asserts it.
- **Cascadia declares `FACE touch`** on product↔category (ship-dark revoked): the demo now *shows* the
  crossing. `SELECT revenue AT {category}` clarifies with the **face menu**; `SELECT revenue AT
  {category.touch}` executes — 12 categories, touch total $3.18M vs grand total $2.21M (the ~$970K
  overlap disclosed), 600/600 coverage.
- **The recapture corpus grows to ten (E1–E10):** E6 records the face menu; E10 mints the executed
  crossing (disclose · over_count · coverage). Zero drift flags.

## [0.5.0] — RELATE rides the wire (declared M:N as describe data)

Purely additive; `contract_version` stays `"1"` (the DESCRIPTION precedent — additive fields ride).
Requires `columna-core>=0.10.0` (unchanged).

- **`describe_manifold` gains `relates[]`:** declared many-to-many relationships now ride describe as
  data — `[{frm, to, note}]`, logical level names plus the NOTE string verbatim. Nothing physical (no
  VIA, no bridge-table name); the standing §2b insulation test covers the new field by construction.
  `describe_measure` is untouched.
- **Why it's load-bearing (not decoration):** a consult-first agent can now name a fan-out *before*
  spending the query — answer "why can't I get revenue by category" from the source of truth — instead
  of the M:N being invisible until tripped, its reason living only in the clarify's after-the-fact
  detail text. The RELATE was always declared "so the refusal can name exactly why"; `relates[]` finally
  puts that on the wire. Multiplicity between logical concepts is substance under §2b″.
- **Born with room for its future:** when RELATE-adjudication puts multiplicity claims on trial, their
  verdicts join these entries additively (the allocation-semantics taxonomy's wire foundation).

## [0.4.0] — the Cascadia case demo, and the agent grows hands

Full narrative: `specs/release_notes_v0_10_0.md`. Requires `columna-core>=0.10.0`.

- **The demo is Cascadia Retail** (replacing the benchmark): a realistic case — one team, one warehouse,
  six questions — modeled to a spec, adjudicated live (`demo --play` runs the E4→E8→E2→E5 four-mood
  wheel over the Cascadia Manifold; `stock`/`buyers` are the Cascadia names).
- **The case rides as an on-demand MCP resource:** `case_chapter` / `case_manifest` serve the three
  chapters verbatim — the WHY behind the Manifold, fetched on a triggering pointer, not stuffed in the
  prompt.
- **The query agent has hands:** native tool-use — within a turn it calls `describe_manifold`,
  `describe_measure`, `case_manifest`, `case_chapter`, `explain`, then the terminal `query` — bounded
  cycles, grounding preserved, the MCP boundary intact.
- **The recapture seeded corpus** (`columna_server.recapture`): E1-E9 adjudicated expectation-first
  against the ratified exemplar spec; the drift-gate the site + tripwire bind to.

## [0.3.0] — the envelope wire + EXPLAIN as a first-class tool

Full narrative: `specs/release_notes_v0_9_0.md`.

- **`query` speaks the envelope** (`SELECT … AT {…}`): the terse `cols @ anchor` form is retired from the
  wire and the `universe` argument is gone (§2c — universe is resolved structurally, never named in a
  query). The four-mood wire contract is unchanged (`contract_version "1"`).
- **`explain` is a first-class tool beside `query`:** the canonical desugared form + atom decomposition +
  the dependency cone with current verdicts + the would-be annotation, touching zero data — the agent's
  cheap inner loop.
- **Every speaking surface migrated to the envelope:** the `demo --play` tour, the MCP acceptance suite,
  and the agent's system prompt (its grammar section rewritten to teach `SELECT`/`AT`, `@`-as-input, and
  the `WHERE`/`HAVING`/`ORDER BY`/`LIMIT PER`/`WITH` clauses).

## [0.2.0] — columna init, the measured KP v0.5, the four-mood tour, and the Explorer describe

Full narrative: `specs/release_notes_v0_8_0.md`.

- **columna init** — the authoring on-ramp: the meaning-in seam between a governed aperture (catalog/
  profile/metered samples; no exfiltrating read) and a draft with a two-layer polarity wall (proposes
  closures freely, cannot express an inferred opening). It proposes; the human declares.
- **The knowledge package ships at v0.5**, reached by a pre-registered eval ratchet (v0.3 salience →
  v0.4 prune, reverted under its do-not-ship clause → v0.5 floored prune): flooding down AND ◆-recall held.
- **The four-mood tour** — `demo --play` walks serve/disclose/clarify/refuse on well-posed §2c asks;
  disclose = a stock summed across a blocked time axis (material caveat, never a silent total).
- **describe** gains the full C-1 extension (basis/absence, asserts, hierarchies, licenses, scope/cut,
  operator properties) under the §2b insulation guarantee; the **Manifold Explorer** renders any describe.
- Wire contract unchanged (`contract_version` "1").

## [0.1.0] — the MCP server, the packaged demo, and the NL agent

First release. The Columna MCP server and its two front doors, over one contract (ADR-032 D8 — the
four moods as data; `contract_version` `"1"`).

- **MCP server** (`columna-server mcp --manifolds <dir>`): five read-only tools —
  `list_manifolds`, `describe_manifold`, `describe_measure`, `query`, `explain` — over a Manifold
  store (`<id>/manifold.cml` + `data.toml`, parsed once at startup). stdio canonical;
  `--http` gated by `COLUMNA_MCP_TOKEN` (constant-time `hmac.compare_digest`). No SQL, no writes.
  The envelope grammar is parsed here; every expression is delegated to columna-core (one dialect).
- **Packaged demo** (`columna-server demo [--play]`): the benchmark Manifold over a small bundled
  warehouse (byte-identical to the core fixtures, drift-guarded), runnable with no path args.
  `--play` prints the real clarify → refuse → disclose → serve wire transcript — all four moods
  (post-§2c: the cross-universe wedge that once drove disclose is now a category error, so disclose is
  driven by a well-posed ask — `level.sum @ store*cal.month`, a stock summed across a blocked time axis).
- **Natural-language agent** (`columna-server agent`, `[agent]` extra): a true MCP client — spawns
  the server over stdio and speaks the protocol, never importing the engine. Natural language
  becomes a *proposed* Frame-QL query; the four moods drive the conversation (clarifies relayed,
  never auto-picked; every numeral verbatim from the wire — grounding is structural). Provider layer
  (`anthropic` default via `COLUMNA_AGENT_MODEL`; `scripted` for tests).

[0.1.0]: https://github.com/datumwise/columna
