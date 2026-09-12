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

**Goldens are NON-NORMATIVE** (ruling, Huayin, 2026-09-12). **A golden artifact witnesses
conformance. It never defines the universe of valid artifacts.** A single artifact cannot express
optionality, cardinality, or a prohibition — and a prohibition is the load-bearing half of this
contract. Goldens are therefore required *per branch of the claim space* (`coincident`/`finer` ×
`exact`/`approximate` × primitive/constructed), and each is labelled a witness.

Three consequences of non-normativity, stated so the label cannot erode into practice:

- conformance is judged against **this document**, never against the goldens — where a golden and
  this document disagree, the golden is wrong until a ruling says otherwise;
- a golden's presence ratifies nothing, and adding one is never an amendment to the format;
- a golden may not be cited as authority for a permission. That an artifact exists and is accepted
  shows only that *this* artifact is accepted.

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

## 5. Endpoint fields — legitimate facts, and the rule that makes them meaningful

Endpoints are **fully resolved in the mapping as stored**. "Derivable" means derivable while
*constructing* the mapping, never by the compiler at compile time.

`connection` and `schema` are **legitimate realization facts** (ruling, Huayin, 2026-09-12). They
are material facts about where the governed family is realized, on the same footing as `table` and
`column` — not incidental context supplied for the producer's convenience, and not metadata a
profile may treat as advisory.

Retention alone is not enough. The Phase 0 reconnaissance found both validated by the reader and
then unconsumed: `connection` is read nowhere in `compile_v2.py`, and `schema` is validated and then
dropped at emission, leaving the image's `FROM <table>` unqualified. *Re-verified against `main` at
`c98cf53`: the lowering path reads `real.endpoint.table` and `real.endpoint.column`, and nothing
else.* By this project's own doctrine — *"a key nobody consumes is meaning nobody carried"* — that is
not a tidiness question but a silent drop.

### 5.1 R0 — the general rule

> **R0 — NO REALIZATION FACT MAY BE DROPPED.** For every fact this format carries, a conforming
> profile must do exactly one of three things: **CONSUME** it (carry it into the emitted reference),
> **CHECK** it (compare it against a context the profile can justify, and refuse a mismatch), or
> **REFUSE** the endpoint (state that it cannot consume the fact faithfully). **Silently ignoring a
> fact is not one of the three.**

The reason is the claim/check inversion of §3 read in the other direction. Every field here is a
claim the artifact *makes*. A claim the compiler neither honours nor tests is a claim the artifact
made and the system did not answer — the producer believes it was heard, and nothing recorded that
it was not.

**What "faithfully" means, stated as a test rather than a sentiment:**

> A fact is consumed faithfully only if it retains its **discriminating power** — two realizations
> differing in that fact *alone* must not produce the same emitted reference.

That is the whole criterion. R1 and R2 are its application to the two facts at issue.

### 5.2 R1 — `connection`

> A **single-connection profile** MAY discharge `connection` by **CHECK**: it declares the one
> connection it serves and refuses a realization whose `connection` differs, naming both the claimed
> and the served connection. It MUST NOT accept a mismatching claim.
>
> A **multi-connection profile** MUST discharge it by **CONSUME** — `connection` must reach the
> emitted reference, or the resolution that selects the source. Under multiple connections two
> realizations differing only in `connection` denote different material locations, so a profile that
> merely checks cannot tell them apart, and CHECK loses the discriminating power R0 requires.
>
> A profile that can do neither MUST REFUSE.

### 5.3 R2 — `schema`

> A profile that can emit a schema-qualified reference MUST **CONSUME** `schema` and qualify the
> reference.
>
> A profile that cannot MUST **REFUSE** any endpoint carrying a non-null `schema`. It MUST NOT drop
> the field and emit an unqualified reference: `{schema: "sales", table: "revenue"}` and
> `{schema: "staging", table: "revenue"}` are different material locations, and an unqualified
> `FROM revenue` collapses them — the exact loss of discriminating power R0 forbids, and the more
> dangerous for being silent, since both endpoints will usually resolve to *something*.
>
> **A null `schema` is not a dropped one.** Null asserts *"no schema qualification applies"*, which a
> profile may consume by emitting the unqualified reference. The distinction is between a fact that
> says nothing and a fact that was not listened to.

### 5.4 Standing of these rules

R0/R1/R2 are conformance requirements on a **profile**, not on this format: the format's obligation
is to carry the facts, and it does. K0v2 satisfies none of the three today — that is recorded in the
law-loss register and is **not** repaired by this document.

**Enforcement is deliberately NOT landed** (ruling, Huayin, 2026-09-12): it waits on review and
ratification of this candidate. Landing a refusal that this document merely proposes would let a
candidate acquire force by being written — the same error as a golden acquiring normative status by
being committed.

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

## 10. Enrolment in the prose-currency mechanism

On ratification — **not before** — enrol this document in `scripts/currency_stamps.toml`. Stated
concretely, because *"this should be enrolled"* is precisely how a document ends up not being.

**The mechanism as it stands renders four placeholders** — `{umbrella}` `{core}` `{server}`
`{contract}` — and the mapping-format major is not among them. Enrolment is therefore **one guard
change plus two entries**, not a TOML line:

1. **A fifth placeholder, imported, never literal.** `{mapping_major}`, rendered from
   `columna_core.compiler.realization.SUPPORTED_MAPPING_FORMAT_MAJOR`, by the rule the guard already
   applies to `{contract}`: *"the contract is the package's to declare; a literal here would be the
   very defect being guarded."* The known-placeholder list in the guard's error path must be updated
   in the same change, or a mistyped name reports four names when there are five.

2. **A stamp on this document's own status line**, so that a mapping-major bump which leaves this
   freeze describing the superseded major fails closed. Per the manifest's own guidance, enrol the
   half of the claim that carries the version and does not wrap.

3. **A stamp wherever shipped prose names the mapping-format major** — the same coverage-by-named-
   entry discipline the manifest applies everywhere else. Coverage grows by enrolment and a reason
   beside it, never by the guard deciding for itself what looks current.

**One thing the stamp cannot do, recorded so ratification does not mistake it for done.** §6's
producer/consumer defect — `MAPPING_FORMAT_VERSION` and `SUPPORTED_MAPPING_FORMAT_MAJOR` must agree
and nothing compares them — is **not** closeable by this mechanism. The guard checks *prose against
the shipped state*; it has no way to compare two constants to each other. That agreement is a
**test**, and ratification should require one.

**Why enrol at all:** the v1 freeze is cited by no code, by no test, and is enrolled in nothing.
That is exactly how a ratified format document becomes folklore — true when written, unfalsifiable
thereafter. The guard's polarity is right for this use: *history is the default, currency is
declared*; nothing scans this file, and a claim is checked only because a human enrolled it by name.
