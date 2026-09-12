# Core Realization Profile v2 — claim-field freeze — **CANDIDATE**

**Status:** **CANDIDATE, not ratified.** Prepared 2026-09-12 on instruction (Huayin) for
ratification review. Supersedes nothing until ratified; `core_p1_k0_design_freeze.md` §3 remains the
ratified freeze for mapping format v1.
**Merging this file does not ratify it.** It is committed so it can be reviewed in place; its status
line is the authority on its standing, and only an explicit ruling changes that line.
**Shape follows:** `core_p1_k0_design_freeze.md` §3 (*"`PrivateCoreMapping` — field freeze —
RATIFIED"*, CG2, 2026-08-22), deliberately, so the two are read the same way.
**Evidence base:** `columna_core/compiler/realization.py` (the v2 consumer as built),
`columna_core/compiler/compile_v2.py` (the K0v2 profile that consumes it), and the Phase 0
reconnaissance of 2026-09-12.

---

## 0. What this document is, and what it is not

**Freeze the on-disk format, not a Python class.** Inherited verbatim in intent from the v1 freeze,
and for the same reason: the `columna` and `manifold-agent` trees are import-disjoint and the
disjointness is test-enforced (`test_server_ingests_the_artifact_without_importing_manifold_agent`
and `test_producer_artifact_v2.py` both assert `"manifold_agent" not in sys.modules`). A shared
executable contract package would break a tested invariant to save duplicated parsing.

**`realization.py` is Core's implementation of this contract, not the contract.** It is one
conforming reader. Where this document and that module disagree, this document is the defect or the
module is — and which one is a ruling, not a code review.

**A golden artifact witnesses conformance. It never defines the universe of valid artifacts.** A
single artifact cannot express optionality, cardinality, or a prohibition — and a prohibition is the
load-bearing half of this contract. Goldens are therefore required *per branch of the claim space*
(`coincident`/`finer` × `exact`/`approximate` × primitive/constructed), and each is labelled a
witness.

**File:** `private-core-mapping.json`. **JSON, not YAML** — the `columna` tree has zero `yaml`
imports and no PyYAML dependency; persisting this as YAML would force one on the consumer for
nothing. Serialization is deterministic: sorted keys, stable separators, mirroring the publication
artifact.

---

## 1. The frozen shape

```
PrivateCoreMappingV2
    mapping_format_version   "2"
    publication_ref          { manifold_id: str, version: str }
    realizations             [ ... ]
```

Exactly two realization kinds:

```jsonc
{ "kind": "anchor_component",
  "anchor_ref":     "<anchor declaration name>",
  "component_name": "<authored component name>",
  "endpoint": { "connection": str, "schema": str|null, "table": str, "column": str } }

{ "kind": "family",
  "family_id":              "<opaque governed family identity>",
  "endpoint":               { "connection": str, "schema": str|null, "table": str, "column": str|null },
  "grain":                  "coincident" | "finer",
  "formation_operator":     str|null,
  "continuation_operator":  str|null,
  "exactness":              "exact" | "approximate" }
```

---

## 2. What a realization MAY say

Five things, and no sixth:

1. **the family it realizes, by `family_id` ONLY** — never by name, never by reducer, never by
   position;
2. **the endpoint(s)** — a fully resolved material location;
3. **a GRAIN-CORRESPONDENCE CLAIM** — how the physical source grain relates to the family's
   constitutive anchor: `coincident`, or `finer`;
4. **a DELIVERY CLAIM** — the backend operator this realization claims discharges the family's
   declared law, and whether it does so exactly or approximately;
5. **realization evidence** — freshness, data-state version, producer attestation. **Deliberately
   absent from this freeze** (§7).

---

## 3. What a realization may NEVER say

Verbatim from the ruled list: *which reducer makes the family what it is · how contributions resolve
into a constituted value · which anchor is constitutive · who the parents are · what the
participation is.*

> **Nothing whose change would change `Σ(F)`.**

In v1 exactly one field — `root_evaluator` — said the first two of those, which is why a private
file could mint a family succession under ToD v7.1 §3.9. That field does not exist here and may not
be reintroduced under another name.

**The claim/check inversion, which is the whole contract in one line:**

> Every field above is a CLAIM the compiler checks against governed law, never a fact from which the
> compiler derives governed meaning.

---

## 4. Publication and family binding

- `mapping.publication_ref == publication.ref`, **checked first, before any lowering**. Mismatch is
  `InputIdentityMismatch`; a wholly absent input is an invalid invocation. A mapping is bound to
  exactly one immutable publication.
- **`family_id` is not derivable from anything in this file.** The reader never computes one, never
  falls back to a name, and refuses a realization whose `family_id` the publication does not
  declare. A mapping edit therefore cannot be a family succession — it can only fail to match one.
- Every governed family the profile lowers requires exactly one realization. Missing, duplicate and
  unknown all refuse.
- Every authored anchor component maps to **exactly one** realization. **No tuple-position
  inference** — carried forward from v1, where `grain=tuple(keys)` had no named coordinate→column
  association.

---

## 5. Endpoint fields — and the two rules that make them meaningful

Endpoints are **fully resolved in the mapping as stored**. "Derivable" means derivable while
*constructing* the mapping, never by the compiler at compile time.

`connection` and `schema` are retained in the contract (ruling, Huayin, 2026-09-12): they are
legitimate material-realization facts. Retention alone is not enough, because the Phase 0
reconnaissance found both currently validated by the reader and then unconsumed — `connection` is
read nowhere in `compile_v2.py`, and `schema` is validated and then dropped at emission, leaving the
image's `FROM <table>` unqualified. By this project's own doctrine (*"a key nobody consumes is
meaning nobody carried"*) that is not a a tidiness question but a silent drop. Therefore:

> **R1 — connection.** A single-connection profile MAY treat `connection` as an expected context and
> check that the claim matches it. It MUST NOT silently ignore a mismatching claim.

> **R2 — schema.** A profile that cannot carry a schema-qualified endpoint faithfully MUST REFUSE
> that endpoint. It MUST NOT drop `schema` and emit an unqualified reference.

Both are conformance requirements on a *profile*, not on this format. K0v2 satisfies neither today;
that is recorded in the law-loss register and is not repaired by this document.

**R1/R2 enforcement is deliberately NOT landed** (ruling, Huayin, 2026-09-12): it waits on review
and ratification of this candidate. Landing a refusal that this document merely proposes would let a
candidate acquire force by being written, which is the same error as a golden acquiring normative
status by being committed.

---

## 6. Version rules

- `mapping_format_version` is a **bare major a loader keys on**, following
  `PUBLICATION_FORMAT_VERSION`'s style — **not** the `"0.1"` style.
- The major is the **only** compatibility axis. A reader accepts exactly the major it implements and
  refuses every other, with a message naming what changed.
- A new major **adds** a golden witness set; it never edits one.
- **Two defects in the current reader that ratification should close:**
  - `int(fmt.split(".", 1)[0])` accepts `"2.5"` as major 2. A version string that is not
    `MAJOR` or `MAJOR.MINOR` should be `unreadable`, not silently truncated.
  - The producer constant `MAPPING_FORMAT_VERSION` is **never consulted** by the check — only
    `SUPPORTED_MAPPING_FORMAT_MAJOR` is. Two constants that must agree, with nothing comparing them.
    This is the same defect already live at `columna_server/registry.py:46`, still major 1 while
    `columna_core.governed.publication` is at major 2. The freeze should require a single guard that
    the two agree.

---

## 7. Deliberately absent

Named here so the absence is deliberate rather than forgotten:

- **realization attestation** — who asserted this claim, and on what authority;
- **realization currency** — whether the assertion is still true of the source;
- **assertion identity** — the producing responsibility's own identity.

These are the three open jurisdictions. The shape above is frozen **independently of** deciding
them, which is the point of freezing now: the claim fields are determined by `Σ(F)`-invariance, not
by who writes the file. `lowering-receipt.json` already reserves the hook — `mapping_provenance`,
typed `Optional[Any]`, explicitly opaque, excluded from `binding`, *"never consulted by
admission"* — and its threat model already records that a receipt *"does NOT resist a forger…
Signing is a separate ruling; the schema leaves room for it."*

Also deliberately absent, carried from v1: relationship · hierarchy · attribute · bridge/`via` · any
restriction-reference record.

---

## 8. Strict refusal behaviour

Closed key sets at **all three** levels — top level, per realization kind, and endpoint. An
unrecognised key refuses; it is never ignored. Closed enums for `grain` and `exactness`; an
undisclosed approximation is exactly what ToD §10.9 forbids, so `exactness` must be checked on
**every** path a profile lowers, not only the constructed one.

Three reader defects ratification should close:

- a **missing** `grain` currently produces the same message as an **invalid** one (absent → `None
  not in GRAINS`); absence and error are different refusals;
- `load_mapping` does not wrap `json.JSONDecodeError`, while its sibling `load_lowering_receipt`
  does — a malformed file should refuse in this vocabulary, not raise a stdlib error;
- duplicate **anchor-component** realizations are not detected by the reader (they are caught later,
  in the profile); detection belongs with the other totality rules.

---

## 9. Naming hazard, recorded

`manifold_agent.mapping` defines `MAPPING_VERSION = "0.1"` and a `mapping_version` field on a
**different object** — the legacy `mapping.yaml` binding list, which is member-keyed and carries
`root_evaluator`. `mapping_format_version` is deliberately a distinct name over a distinct object.
The two must never be conflated, and a producer for *this* contract is not an extension of that one.

---

## 10. Enrolment

On ratification, enrol this document's currency claim in `scripts/currency_stamps.toml` so the
mapping-format major and the shipped state cannot drift apart in prose. The v1 freeze is cited by no
code and no test and is enrolled in nothing, which is how a ratified format document becomes
folklore. The guard's polarity — *history is the default, currency is declared* — is correct for this
use.
