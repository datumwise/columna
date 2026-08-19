# Core-P0.5 — Governed-certification lifecycle (design record)

**Status:** design / pre-implementation. No compiler code, no certification persistence, no shared
`License` type, no face-law implementation.
**Date:** 2026-08-13
**Sources:** `columna` @ main (`0.15.0-core`), `manifold-agent` @ `d9ea705` (`0.12.0`).
Reads with `f0_reconnaissance.md`, `s2_closure.md`, `core_p1_compiler_input.md`,
`core_p1_compiler_contract.md`.

Two statements govern this record:

> **The defect is not that adjudication is absent. The defect is that serving does not structurally
> require its positive result.**

> **A contradiction block-list is not equivalent to a certification allow-list.**

Governing invariant:

> **Declaration makes a capability a candidate. Certification makes it usable.**

Today both faced crossings and hierarchy transport violate that invariant: declared capability is
served as though it were licensed capability.

---

## 1. The fail-open defect (the stop condition)

### 1a. Hierarchy transport is fail-open

`blocked_edges` is a **subtractive block-list of only CONTRADICTED-on-reattest edges**:
- built only under `degrade=True`, adding an edge solely when `_prove_hierarchy` raises
  `HierarchyContradiction` (`adjudication.py:614-631`; `scope_from_report` reads only `report["_blocked"]`,
  `:388-392`).
- the planner refuses transport **iff** the edge is in that set (`planner.py:113-128`); an empty set
  short-circuits to "nothing blocked" (`:116`).
- addressability (`_check_addressable` `planner.py:162-203`) and `find_path` traverse a shape DAG built
  from **all** `m.edges` with **no verdict filter** (`projection.py:130,149-164`); edges enter `m.edges` at
  parse (`parser.py:515`), before any adjudication.
- strict first publish/load never sets `report["_blocked"]` (`adjudication.py:630` guards on `degrade`);
  `store.py:154-159` adjudicates strict at load, then `blocked_edges` is empty.

Per-verdict: CORROBORATED → usable (correct); CONTRADICTED @ first publish → fail-closed load (safe);
CONTRADICTED @ reattest → refused; **UNTESTABLE → usable (fail-open)**; **no-adjudication / load-only store
→ usable (fail-open)**. A parsed-but-uncorroborated `FunctionalEdge` **can** become an addressable
transport path — the forbidden silent fan-out.

### 1b. Faced crossings are fail-open

The face License is minted at publish (`_prove_face`, sole constructor, `adjudication.py:457-528,650`) but
**never consulted at serve**. The planner deems a faced coordinate addressable from the **declaration**
(`parse_faced`, `planner.py:168-175`; `model.py:373-384`); engine resolvers read `face.license` **zero**
times (`engine.py:281-451`). A `ManifoldServer` that parses faces and answers a faced query **without
`publish()`** serves the crossing with `license=None`. Faces never contribute to `blocked_edges`
(hierarchy-only). Enforcement is only the all-or-nothing publish abort ("a CONTRADICTED face ⇒ the whole
manifold fails to publish"), **not** "no license ⇒ this crossing refuses." A CONTRADICTED face at reattest
throws **uncaught** — the faces block in `adjudicate` has no degrade/scope-edit path (`:645-656`).

The constitutional claim "the default is closed" (`model.py:106,114`) holds for **derived-column
fertility** but is **violated for hierarchy edge transport and for faces**.

---

## 2. Immutable law vs realization-bound certification

| | immutable publication law | realization-bound certification |
|---|---|---|
| carrier | universe `Ratification` (manifold-agent, `ratification.py`) | Core `License` (in-memory, `columna_core`) |
| fingerprints | logical: anchor · basis · restriction AST · logical deps (`ratification.py:157-163`); physical/data **deliberately excluded** (`:96-99`) | attested **data**: FD holds / unique-top / non-neg-positive-sum |
| stale on | logical change | data re-attestation (connector data identity — P0.5b-0) |
| lifetime | durable human publication authority | ephemeral runtime state, recomputed each publish/attest |

Certifications are **not** publication identity. The same immutable `retail@1.3.0` realized against env A
(FD holds) vs B (FD contradicted) has one meaning, two certification results. Do **not** put data-derived
verdicts into immutable `GovernedPublicationArtifact`.

---

## 3. Three distinct concepts — never merged into one representation

```
declaration            what was authored             (candidate capability)
certification          what adjudication proved       (against a realization + data state)
serving admission      what may be exercised NOW      (the runtime scope the planner consumes)
```

Today the planner/engine authorize from the **declaration** (or absence from a block-list). They must
instead authorize from **serving admission**, derived from **certification**, which is about the
**declaration** proven on a realization.

---

## 4. Current per-verdict behavior (today)

| verdict / state | faces | hierarchy |
|---|---|---|
| VERIFIED (touch) | served; license inert | n/a |
| CORROBORATED | served; license inert | usable (correct) |
| UNTESTABLE | n/a (faces raise instead) | **usable — fail-open** |
| CONTRADICTED @ first publish | whole publish aborts (fail-closed) | fail-closed load (safe) |
| CONTRADICTED @ reattest | throws **uncaught** | refused via `blocked_edges` |
| no adjudication / license None | **served — fail-open** | **usable — fail-open** |

---

## 5. Ruling: positive admission, not negative blocking

Current polarity is "usable unless contradicted." Governed polarity must be **"usable only if positively
licensed."**

```
hierarchy edge:  CORROBORATED → usable;  CONTRADICTED / UNTESTABLE / no-adjudication → not usable
face:            touch+VERIFIED → usable;  assign/alloc+CORROBORATED → usable;  CONTRADICTED / license-missing → not usable
```

- A declaration alone must never open the crossing.
- Do **not** implement this as "add UNTESTABLE to `blocked_edges`" — that keeps the wrong polarity. The
  serving state must represent **positively admitted** capabilities (conceptually `certified_edges` /
  `certified_faces`), so that **absence means closed**.
- **Path discovery must respect certification.** An uncorroborated functional edge must **not** establish
  addressability: `declared shape graph + current governed certification scope → usable shape graph`
  (filtered traversal), so no later code path can bypass a post-hoc refusal. Likewise, parsing
  `<coord>.<face>` resolves the *named declaration*; it does not establish the crossing is executable.

---

## 6. Carrier: runtime `PublishedScope`, not a durable artifact (for now)

Keep the existing split: `GovernedPublication` = immutable meaning/authority; `PublishedScope` = runtime
adjudication/serving state (recomputed fresh each publish/attest; "no history … history lives in
watermarks", `adjudication.py:355-362`).

Desired lifecycle:
```
publication (immutable law) + private realization (physical)
    → compile        → closed execution image
    → adjudicate     → establish certification for THIS runtime state
    → PublishedScope → hold current serving admission
    → serve          → require current admission
```
Extend `PublishedScope` to **positively record** admitted hierarchy edges and relationship crossings; the
planner consumes that scope. Planner/engine must **not** infer authorization from `Face.license`,
declaration presence, or absence from a block-list. On restart, certification may be recomputed — acceptable
for Core. A durable certification artifact is deferred until a concrete requirement forces it (cross-process
transfer, offline certification, custody/history, avoiding re-adjudication after restart, Platform
cross-domain transport). But the **meaning** of certification is defined independently of Core's `License`
class now.

---

## 7. Certification-binding requirements (P0.5b)

**Partly closed by P0.5b-0 (2026-08-19) — data identity only.** When this record was written,
`attestation` was a `table:rowcount` watermark, so a proof on realization A was indistinguishable from one
for realization B with matching table names + counts, and it could silently transfer. That primitive is
gone. `Connector.data_identity(table) -> Optional[str]` is now part of the **Protocol**, and both consumers
that gated on row count — the certification attestation and the engine result cache — gate on it. The
contract asks for a **change/version token trustworthy for reuse under the guarantee the connector
documents**, not for a collision-free identity: a backend-native version/snapshot token (table-format
snapshot id, catalog version, MVCC watermark) is a source-provided data identity under that backend's
contract; the DuckDB fallback is a content+schema fingerprint of the current realized table state — a
change detector, finite, not collision-free. No trustworthy token ⇒ `None` ⇒ **fail closed for reuse**
(nothing cached, nothing data-established treated as current); serving itself is never affected. Currency
is judged per capability, from the read set each proof reports (`_hierarchy_deps` / `_face_deps` →
`PublishedScope.edge_evidence` / `face_evidence`), so a table no proof read closes nothing.

`License` still carries only `{verdict, lineages(subject), basis(claim), attestation}` — **no
`publication_ref`, and no realization identity beyond the per-table data state**. Mapping identity, binding
identity, source selection, and the rest of realization semantics remain OPEN for full P0.5b. A sound
certification must distinguish at least:
```
publication identity · realization identity · certification subject · certification claim · verdict · data-attestation identity   (+ time/provenance)
```
Central invariant:
> **Certification for publication P on realization R under attestation A licenses only P/R/A — unless the
> certification is explicitly timeless.**
`touch` = VERIFIED, symbolic/timeless, no data-attestation dependency. `hierarchy FD` / `assign` / `alloc`
= data-dependent, require realization + attestation binding. Do not freeze the fingerprint format; first
trace what stable realization identity + source-attestation capabilities actually exist.

**Adjudication status ≠ serving license.** Adjudication yields VERIFIED / CORROBORATED / CONTRADICTED /
UNTESTABLE; a serving license exists only for VERIFIED / CORROBORATED **and** only if the identity/currentness
bindings hold: `adjudication verdict → license derivation → PublishedScope admission`. Do not treat
`UNTESTABLE` as a weak license; do not treat "not contradicted" as a license.

**Re-attestation / staleness (P0.5a must close this):** if old certification existed, data changes, and
reattest fails to re-establish it — the affected capability must **not** retain an apparently current
license. Whether the whole Manifold becomes unavailable or only the capability closes is a later policy
decision (do not broaden P0.5a into it), but structurally the stale capability must lose its live license.
The exact atomic state transition is to be designed before code. (Note today's reattest face-contradiction
throws rather than degrading — a corner P0.5a must handle.)

---

## 8. Face-law carriage gap (P0.5c)

The shared authored `relationship` carries only `{from, to, functionality, disposition}` (`validate.py:86`),
and `disposition` is descriptive prose (`logical.py:89,99`) — no touch/assign/alloc law is authored or
published anywhere in manifold-agent / columna-studio (exhaustive grep: zero face-authoring hits). Face law
lives **only** in hand-authored Core `.cml` (`parser.py:270-353`). A genuine **logical carriage gap**: the
compiler cannot even know which face was declared, independent of certification.

Do **not** copy `.cml FACES` syntax into the shared model verbatim. Express relationship-crossing law in
**runtime-independent semantic terms**; Core lowers it into `FACES` later. Classify each current Core field
as one of: *semantic law · required governed disclosure · human description/prose · Core serialization
requirement.* In particular, determine whether the mandatory `.cml` folklore/description is analytical law
or merely a Core disclosure/serialization requirement — do not fingerprint prose into shared logical
identity without a reason. The shared crossing law must express the timeless-vs-data-dependent distinction
(`touch` symbolic/timeless; `assign`/`alloc` data-dependent) **without** depending on
`columna_core.model.Face`.

---

## 9. Authority-independent compiler kernel

```
KERNEL (serve-safe today; does NOT depend on the fail-open certification paths):
  measure · member · anchor · universe · bare non-functional relationship · co-located attribute
```
Strict boundaries:
- **measure/member** — only exact currently-supported reducers; holistic/sketch still **C**-refuse.
- **anchor** — A-coord realization required; no unnamed tuple-position inference.
- **universe** — restrictions compose only through governed coordinate / co-located-attribute realizations.
- **bare relationship** — stays explicitly non-functional; must **not** become an additive transport path
  merely because the physical join is emittable; no face/crossing synthesized.
- **co-located attribute** — no hierarchy/relationship transport required to retrieve its value.
- **excluded until prerequisites met:** HIERARCHY / functional transport · FACES · cross-table attribute
  attachment · boundary · crosswalk.

---

## 10. The three P0.5 threads and sequencing

```
P0.5a  closed-by-default governed serving   — live runtime correctness fix (positive admission)
P0.5b  certification identity + freshness    — publication / realization / attestation binding
       (P0.5b-0 landed the data-identity + cache-safety slice; the rest is open)
P0.5c  shared relationship-crossing law      — authoring/publication carriage for face semantics
```
- **P0.5a** answers *"may an uncertified declared capability execute?"* — must become **no**. Highest
  priority (a live governed-serving defect, tracked as its own issue so it cannot vanish inside the compiler
  project).
- **P0.5b** answers *"what exact thing did this certification prove, against which realization and data
  state?"* The **data-state** half is answered by P0.5b-0 (`Connector.data_identity`, per-capability
  evidence currency). The **realization/publication** half — mapping identity, binding identity, source
  selection — is still open.
- **P0.5c** answers *"what crossing law did the governed author actually declare?"*

Sequence:
```
persist this record → P0.5a minimal closed-by-default serving fix → Core-P1 authority-independent kernel may begin
```
P0.5b and P0.5c do **not** block the kernel compiler; they gate expansion into hierarchy, faced
relationships, and cross-table attributes.

---

### Governing stop rule (verbatim, unchanged)

> If the governed publication does not contain enough meaning to compile, stop. If the private mapping does
> not contain enough realization information to compile, report a mapping gap. In neither case may the
> compiler invent the missing fact.
