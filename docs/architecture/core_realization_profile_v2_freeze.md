# Core Realization Profile v2 — claim-field freeze — **CANDIDATE**

**Status:** **CANDIDATE, not ratified — but the implementation now conforms.** The conformance unit
of 2026-09-12 landed R0/R1/R2, the §6 version-shape refusal, the §8 strictness items and the
constant-coherence test, so nothing in this document is now awaiting work. This freeze describes
**mapping-format major 2**, which is the major `columna-core` reads and writes. Prepared 2026-09-12 on instruction (Huayin) for
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

**What "faithfully" means, stated as a test rather than a sentiment.** An earlier draft wrote the
test as *"must not produce the same emitted reference"*. That is too narrow, and narrowly wrong in a
way that would license the next drop: a fact can be load-bearing without ever appearing in a
rendered string. `connection` may select which material source is consulted; `schema` may qualify an
endpoint's identity without changing the rendered table name a given profile emits; a fact may bear
only on standing or admission; a fact may be relevant precisely because it should have caused a
**refusal**. A test keyed on rendered output would call all four of those "consumed".

> **The faithful-consumption test.** A realization fact is consumed faithfully only if changing that
> fact **alone** can change the **effective material realization**, the **standing or check
> behaviour**, or **cause a refusal** — wherever that fact is semantically relevant.
>
> **Corollary, which is the operative half:** two claims differing in a relevant realization fact
> MUST NOT be **observationally indistinguishable** merely because the implementation dropped the
> fact.

Four channels, then, not one — a profile discharges a fact through whichever are relevant to it:

| channel | the fact changes… |
|---|---|
| material-source selection | *which* source is consulted |
| qualified endpoint identity | *what* the endpoint denotes, whether or not the rendered string differs |
| standing / admission | what the claim is admitted *as*, or whether it is admitted |
| refusal / check behaviour | whether the profile refuses, and what it names when it does |

**Indistinguishability is the defect, not silence.** The question is never whether the profile
mentioned the fact; it is whether a producer could change the fact and observe nothing. Where that is
true, the fact was not consumed — it was absorbed. R1 and R2 below are this test applied to the two
facts at issue, and they are consequences of it, not additional rules.

### 5.2 R1 — `connection`

> A **single-connection profile** MAY discharge `connection` by **CHECK**: it declares the one
> connection it serves and refuses a realization whose `connection` differs, naming both the claimed
> and the served connection. It MUST NOT accept a mismatching claim.
>
> A **multi-connection profile** MUST discharge it by **CONSUME** — `connection` must reach
> **material-source selection**. This is the channel that matters for this fact, and it need not
> surface in any rendered reference: what must change is *which source is consulted*. Under multiple
> connections two realizations differing only in `connection` denote different material locations, so
> a profile that checks against a single declared context cannot tell them apart, and two
> distinguishable claims become observationally identical.
>
> A profile that can do neither MUST REFUSE.

### 5.3 R2 — `schema`

> A profile that can emit a schema-qualified reference MUST **CONSUME** `schema` and qualify the
> reference.
>
> A profile that cannot MUST **REFUSE** any endpoint carrying a non-null `schema`. It MUST NOT drop
> the field and emit an unqualified reference: `{schema: "sales", table: "revenue"}` and
> `{schema: "staging", table: "revenue"}` are different material locations, and an unqualified
> `FROM revenue` collapses them — two claims made observationally indistinguishable by the drop,
> which is exactly what the test forbids, and the more dangerous for being silent, since both
> endpoints will usually resolve to *something*. The channel here is **qualified endpoint identity**:
> what the endpoint denotes changes even where a profile's rendered string would not.
>
> **A null `schema` is not a dropped one.** Null asserts *"no schema qualification applies"*, which a
> profile may consume by emitting the unqualified reference. The distinction is between a fact that
> says nothing and a fact that was not listened to.

### 5.4 Standing of these rules

R0/R1/R2 are conformance requirements on a **profile**, not on this format: the format's obligation
is to carry the facts, and it does.

**K0v2 NOW SATISFIES ALL THREE** (landed 2026-09-12, on instruction, after this document was
reviewed — so the order was ruling first, implementation second, which is the order that keeps a
candidate from acquiring force by being written):

- **R2 · `schema`** — the profile **REFUSES** a non-null schema. It emits `FROM <table>` and the Core
  execution grammar's table is a bare `^\w+$`; it has no schema notion at all, so it cannot consume
  the fact and says so (`ExecutionRepresentationGap`). A **null** schema is consumed by emitting the
  unqualified reference, which is the distinction between a fact that says nothing and a fact that
  was not listened to.
- **R1 · `connection`** — the single-connection profile **CHECKS** it: all realizations must agree on
  one connection (`UnsupportedCoreCapability` otherwise, since one image cannot be bound to two), and
  where the caller supplies a bound context, a differing claim refuses (`InputIdentityMismatch`).
- **R0** — the criterion is asserted directly: two mutations that previously produced a
  byte-identical image now each change the outcome.

**Two fixtures stopped claiming what the image could not carry.** Both declared `schema: "main"`,
which the compiler silently dropped, so `main.sales_lines` and any other schema's `sales_lines`
compiled to the same reference. They now declare `schema: null`.

**A future multi-connection profile must CONSUME `connection`, not merely check it** — under multiple
connections two realizations differing only there denote different material locations, so a check
against one declared context cannot tell them apart. Recorded in the profile; not implemented.

## 6. Version rules

- `mapping_format_version` is a **bare major a loader keys on**, following
  `PUBLICATION_FORMAT_VERSION`'s style — **not** the `"0.1"` style.
- The major is the **only** compatibility axis. A reader accepts exactly the major it implements and
  refuses every other, with a message naming what changed.
- A new major **adds** a golden witness set; it never edits one.
- **Both reader defects are CLOSED (2026-09-12):**
  - `int(fmt.split(".", 1)[0])` accepted `"2.5"` as major 2. The version is now matched against
    `^\d+$` first: this format is a bare MAJOR, and a spelling it does not define is **unreadable**
    rather than truncated to its head. `"2.0"` refuses too — a reader that normalizes an
    unrecognised spelling has decided what it means.
  - `MAPPING_FORMAT_VERSION` and `SUPPORTED_MAPPING_FORMAT_MAJOR` are now compared by a **test**
    (`tests/test_mapping_format_constants.py`), over both the v1 and v2 readers.

**A CORRECTION TO THIS DOCUMENT'S OWN CLAIM.** An earlier revision said the constants defect was
*"the same defect already live at `columna_server/registry.py:46`"*. **That was wrong**, and checking
it was the only way to find out. `registry.py`'s constant is `SUPPORTED_PUBLICATION_FORMAT_MAJOR` —
a **publication**-format major, a different dimension from the mapping format — and it is genuinely
behind (1, against `manifold_agent.publication.PUBLICATION_FORMAT_VERSION` of `"2"`). But it is not
the same *kind* of defect: the mapping constants are a producer and a consumer **in one module**, so
a test can compare them; the server's consumer must agree with a producer in a **deliberately
import-disjoint tree**, and `columna-server` may not import `manifold_agent` — the disjointness is
test-enforced and this freeze rests on it. No in-process comparison can exist without breaking that
invariant. Whether the server should accept publication major 2 is a **compatibility ruling**, not a
coherence test, and it is out of this unit's scope. Pinned at
`columna-server/tests/test_publication_format_major.py` so the gap keeps a name.

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

**All reader defects named here are CLOSED (2026-09-12), and one more was found while closing them:**

- a **missing** `grain` produced the same message as an **invalid** one (absent → `None not in
  GRAINS`), telling a producer it had written something wrong when it had written nothing. They are
  now different refusals;
- `load_mapping` now wraps `json.JSONDecodeError` like its sibling `load_lowering_receipt`, so two
  loaders over the same kind of artifact no longer answer in different languages;
- duplicate **anchor-component** realizations now refuse in the reader, beside the duplicate-family
  rule, rather than only later in the profile — one artifact defect was refusing in two different
  places depending on which key it was on, and a reader used outside the profile saw neither;
- **FOUND WHILE CHECKING: the TOP-LEVEL key set was not closed.** This section claimed closed key
  sets at all three levels and only two were — an unrecognised top-level key was silently ignored,
  which is the one outcome a closed format may not have, because the producer is told nothing and
  believes the claim was carried. Now closed.

---

## 9. Naming hazard, recorded

`manifold_agent.mapping` defines `MAPPING_VERSION = "0.1"` and a `mapping_version` field on a
**different object** — the legacy `mapping.yaml` binding list, which is member-keyed and carries
`root_evaluator`. `mapping_format_version` is deliberately a distinct name over a distinct object.
The two must never be conflated, and a producer for *this* contract is not an extension of that one.

---

## 10. Two currency checks, deliberately separate

On ratification — **not before** — this document's currency must be guarded. There are **two**
checks, they guard **different things**, and neither substitutes for the other. Keeping them
separate is the point of this section (instruction, Huayin, 2026-09-12): a stamp that looks like it
covers the constants would be worse than no stamp, because it would retire the question.

### 10.1 CHECK ONE — prose-currency enrolment (the ratified freeze)

**Guards:** *does the shipped state still match what this document says about itself?*
**Mechanism:** `scripts/currency_stamps.toml` + `scripts/check_currency_stamps.py`.

Stated concretely, because *"this should be enrolled"* is precisely how a document ends up not
being. The mechanism as it stands renders four placeholders — `{umbrella}` `{core}` `{server}`
`{contract}` — and the mapping-format major is **not** among them. Enrolment is therefore **a guard
change plus entries**, not a TOML line:

1. **A fifth placeholder, imported, never literal — LANDED 2026-09-12.** `{mapping_major}` is
   rendered from `columna_core.compiler.realization.SUPPORTED_MAPPING_FORMAT_MAJOR`, by the rule the
   guard already applies to `{contract}`: *"the contract is the package's to declare; a literal here
   would be the very defect being guarded."* The known-placeholder list in the error path was updated
   in the same change, and the guard's report line now names the major it read.

2. **A stamp on this document's own status line — LANDED 2026-09-12.** The status line now carries
   a non-wrapping sentence naming the major (*"This freeze describes **mapping-format major 2**…"*),
   enrolled in the manifest, so a mapping-major bump that leaves this freeze describing the
   superseded major fails closed.

3. **A stamp wherever shipped prose names the mapping-format major** — coverage grows by a named
   entry and a reason beside it, never by the guard deciding for itself what looks current.

**Why enrol at all:** the v1 freeze is cited by no code, by no test, and is enrolled in nothing.
That is how a ratified format document becomes folklore — true when written, unfalsifiable
thereafter. The guard's polarity suits this use: *history is the default, currency is declared*.

### 10.2 CHECK TWO — a code/test invariant on the constants (NOT a stamp)

**Guards:** *do the producer and consumer constants still agree with each other?*
**Mechanism:** a **test**. It does not exist, and ratification should require it.

§6 records the defect: `MAPPING_FORMAT_VERSION = "2"` and `SUPPORTED_MAPPING_FORMAT_MAJOR = 2` live
side by side in `realization.py`, must agree, and **nothing compares them**. The same defect is
already live at `columna_server/registry.py:46`, still major 1 while
`columna_core.governed.publication` is at major 2 — which is the proof that it is a real failure mode
and not a hypothetical one.

> **The prose stamp cannot close this, and must not be described as if it could.** The currency guard
> renders a template from the shipped state and asserts the literal appears in a file. It compares
> **prose to shipped state**. It has no mechanism for comparing **two constants to each other**, and
> adding one would make it something other than what it is — a guard that reads no prose it was not
> pointed at.

An enrolment that quietly left this uncovered would be the more dangerous outcome of the two,
because the stamp's presence would read as assurance. Both checks, or the gap stays named.
