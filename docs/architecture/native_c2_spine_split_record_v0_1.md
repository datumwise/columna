# C2 · The spine split — implementation record

**2026-09-22.** Unit C2 of the native-consumer sequence. **Construction, not demolition:** nothing
obsolete was retired, no producer change, no Platform change, no compilation, no Law(F) work.
Suites green — `columna-core` 1864 passed / 50 skipped, `columna-server` 416 passed / 2 skipped,
`columna-platform` 286 passed.

**Stop-gate, as stated:** *"a v3 unit loads and is visible in the catalog — the present failure is
invisibility, not refusal — and v1/v2 units are byte-unchanged."* Both halves witnessed by
`packages/columna-server/tests/test_native_v3_spine.py` (17 tests).

Three majors in one installation, measured:

```
catalog
  firstlight  governed  1.0.0  realizable: true
  harbour     governed  1.0.0  realizable: false     <- the native unit, visible and unserved
  lighthouse  governed  1.0.0  realizable: false

firstlight  major=1  has_cml=True   native=False  logical=present  provider=bound
lighthouse  major=2  has_cml=False  native=False  logical=present  provider=none
harbour     major=3  has_cml=False  native=True   logical=None     provider=none
```

and the native unit's governed currency, re-verified through the server's own read path:

```
elf-2 attestation    harbour     CURRENT    recomputes to f077c0e15f4af4ff…
F4 coverage          harbour     COVERED    6 asserted, 6 raised by this constitution
U-authority binding  berthings   BOUND      cites the attestation carried on 'harbour'
fcf-2 constitution   berthings   CURRENT    recomputes to 38546850c5f83933…
U-authority binding  moorings    UNBOUND    not BOUND and not equivalent standing
fcf-1 constitution   moorings    CURRENT    recomputes to cecffbe222b7bda6…
```

**The failure corrected was silence, not refusal.** Before C2, `_is_governed_only_unit` called
`load_publication_artifact`, caught `UnsupportedPublicationFormat`, returned `False`, and the unit
*did not exist*: an installation holding a lawful native publication was told it had nothing. The
refusal underneath was load-bearing and stays — relabel that artifact `"2.0"` and the v2 reader
**accepts** it while discarding every constitution it carries — so v3 was admitted by being read as
v3, never by relabelling, wrapping, or widening v2.

---

## 1 · What the native spine now owns

Everything below `(supported major, concrete ref)`:

| owned | where |
|---|---|
| the version gate's two mechanisms — major selection, minor recognition | `governed.native.read_version` |
| positively admitted declaration kinds; consume-or-refuse at the declaration **envelope** | `governed.native` |
| the constitution as governed facts; machine conformance; unadmitted premise forms | `governed.native` |
| the four currency claims — `elf-2`, F4 coverage, the U-authority binding, `fcf-1`/`fcf-2` | `governed.native` |
| the denotation table and the derived geometry | `governed.native` |
| **ingest dispatch** for major 3 | `registry._read_v3` — 12 lines, delegating |
| **visibility** of a `.cml`-less native unit | `store._VISIBLE_GOVERNED_ONLY_MAJORS` |

`registry._read_v3` calls no v1/v2 helper. There is no expression on that path that could produce a
`logical` wrapper, an `authority` section, a ratification map, or a declaration in the authoring
vocabulary.

## 2 · What remains shared with, or convergent upon, the legacy spine

**Two facts, and they are the whole of the shared spine now:** a *supported format major*, and a
*concrete `ref`* (`manifold_id` + a concrete version). Everything the old spine additionally called
shared — the `logical` wrapper, the `authority` object, ratification keys corresponding to universe
names — **was never a spine; it was v1 and v2's contract, hoisted.** It now lives in
`registry._v1v2_envelope`, unchanged, running the same checks in the same order over the same bytes.

Beyond ingest, these installation-level objects are shared and did not need to change:

* `ManifoldSelector` / `ManifoldRef`, and "latest" as highest semver;
* `FolderManifoldRegistry` — keyed by ref, indifferent to what a publication *means*;
* `GovernedPublication` as a container, `LoadedManifold`, the catalog row shape, `realizable_refs`,
  the four public `kind`s and the condition-code channel.

> **The generalization worth recording: IDENTITY and AVAILABILITY converge; MEANING does not.**
> *Which* publication this is, and *whether this installation can serve it*, are the same questions
> for every major and are answered by one mechanism. *What it says* is per-major all the way down.
> That is a sharper boundary than "the spine", and C2 found it by being forced to cut somewhere.

## 3 · Places C2 translates native meaning into a legacy-shaped object

**None.** Four sites would have, and each was cut the other way instead:

| site | what a translation would have looked like | what was done |
|---|---|---|
| `PublicationArtifactData.logical` | deserialize the native declaration list into the v2 slot — it *fits* | left `None`; `native` added beside it |
| `PublicationAuthority.ratification` | synthesize a `{universe → record}` map from the per-declaration attestations | left `None`, **with the reason stated**: the v2 OBJECT does not exist, and the native standing (recomputed and verified) is strictly stronger than the slot it is absent from |
| `tools._governed_discovery` | `(publication.logical or {})` → `measures: [], anchors: [], levels: []` | **refuses** — a well-formed answer meaning *nothing to ask*, about a publication carrying two families, is the measured v2 failure in a different costume |
| `store._load_one` promotion to `ENTRY_GOVERNED` | verify the lowering receipt and bind the native publication to the `.cml` beside it | **classified, never promoted** — `NativePublicationNotLowerable` |

The last is the one with a reason beyond hygiene. The `.cml` universe construct is
`UNIVERSE <n> = <dim> * <dim> [BASIS <b>]`: there is no slot for a constitution and no way to spell
an existence law. Whatever a receipt attests about those two files, it cannot be that *this image
realizes this publication's law*. **A native unit IS the publication; an image beside it is a
different unit, not a realization of this one.**

The only shared-shape slots a native unit fills are `ref` and the catalog row — identity and
availability, per §2, not meaning.

## 4 · Is Law(F) encountered?

**No.** Nothing in C2 resolves a family's law, calls `governed.resolve`, constructs a `LawView`, or
reads a responsibility. The nearest approach is `registry._read_v2`, which delegates to
`parse_publication` — v2's reader, on v2 bytes, unchanged.

**No fact forced an encounter, and it is worth saying why not:** C2's questions are *can this
installation see this publication* and *is it well-formed under its own contract*. Neither is a
question about what a family means. A native unit reaches the catalog carrying its resolved model
and stops there, because the next thing anyone could ask of it needs a provider — which is serving,
and out of scope.

So the evidence bearing on convergence is still only negative and still only about the layers above:
nothing below the reader was consulted, and nothing asked to be. **Law(F) remains open, and C2
neither assumes nor tests it.**

## 5 · Legacy assumptions that became unreachable rather than needing emulation

Each of these was a *load-bearing assumption of the shared spine* before C2 and is now simply not
expressible on the native path:

* *"a governed publication has a `logical` wrapper"* — no longer a spine fact; the native artifact
  has no such key and one is a refusal.
* *"a governed publication has a top-level `authority` section"* — ditto. Standing lives on the
  declarations that carry it.
* *"publication-global ratifications, keyed by universe name"* — natively unstatable: the
  attestation hangs off the universe, so no publication-global map can be built.
* *"every declaration is `{kind, name, body}`"* — a native universe is 100% envelope and 0% body,
  and a `body` on one refuses **by name**, with the legacy keys it carried listed.
* *"the major that can be READ is the major that can be SERVED"* — one constant was doing both
  jobs, which is precisely what left a v3 unit with no state to be in. Now
  `_VISIBLE_GOVERNED_ONLY_MAJORS` and `_PLATFORM_PUBLICATION_MAJOR` are asked separately.
* *"a governed unit with a `.cml` beside it is a lowered realization of its publication"* — for a
  native publication, structurally impossible (§3).

**Nothing was removed to achieve any of this.** `compile_v2`, the v2 reader's silent acceptance
(P2-01), the `logical` envelope, publication-global anchors and the whole lowered path are
untouched and still ship for the majors that have one.

## 6 · New governed facts C2 required that the v3 artifact does not contain

**None.** C2 asked the artifact for nothing it does not carry, and no producer change was
considered. Two near-misses, recorded because neither is a missing governed fact and both could be
mistaken for one:

* **The public `discovery` payload has no native answer.** `measures[].grain`, `anchors[].basis`
  and the `levels` list are read out of anchor declarations and `universe.body` — objects the
  native model does not have. That is an **unresolved design question about a wire surface** (the
  recon leaves `discovery.levels` explicitly open), not a fact missing from the artifact. C2
  refuses rather than settling it by accident; the refusal is presently unreachable through
  `discovery` (the provider gate answers `not_realizable_here` first) and is placed now because the
  day a native unit becomes servable, the failure mode is a well-formed empty answer rather than an
  error.
* **A governed-only unit has no `data.toml`, so no name or description.** It uses the folder id and
  an empty description — exactly as a v2 governed-only unit already did. Unchanged, and not a
  native question.

---

## 7 · Carried forward

* **OF-59** (`specs/open_forks.md`) — the canonicalization conformance obligation from C1's F-1,
  rowed as adjudicated: independent implementations stay independent, one fixture is presently the
  only agreement witness, and the mechanism for stronger evidence is deliberately unchosen.
* **F-3 fixture debt** stands, unaddressed by design: the server suite reads the v3 fixture from
  `columna-core/tests/fixtures_v3/` rather than taking a third copy, so C2 added no new drift
  surface, and no cross-repo synchronization mechanism was built.
* **Ruling 3 boundary held:** nothing in C2 touches movement, and geometry still establishes only
  that a target location exists.
