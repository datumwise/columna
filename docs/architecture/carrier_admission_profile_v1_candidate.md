# Carrier Admission Profile — v1 — **CANDIDATE**

**Status:** candidate contract, 2026-09-14. **Not ratified.** Prepared on instruction (Huayin,
2026-09-14) as deliverable 3 of eight, ahead of any ADBC implementation.

**What this is.** The rules by which material that has arrived — with a concrete physical type, which
is the thing that does not exist at lowering — is admitted as, or refused as, the governed analytical
fact it claims to be.

**What this is not.** It is **not** a ratification of
[`admission_fidelity_study_v0_1.md`](admission_fidelity_study_v0_1.md), which was corrected on the
same day and whose own header now says it must not be ratified as an envelope. It is **not** a
statement about what Arrow can represent, and every refusal below is **profile non-support** rather
than a claim that a representation is inherently unlawful.

---

## 0. Where CAP's authority comes from

Five sources, in this order of precedence:

1. **Governed anchor and value facts** — what the publication declares. Highest authority; CAP may
   never override or supply one.
2. **Arrow structural facts, where genuinely structural.** That Arrow's type system *has* a
   `decimal128(p, s)` and a validity bitmap distinct from values is a property of the format. That a
   given driver *uses* them is not, and is never treated as one.
3. **Explicit conservative profile choices.** Where neither of the above decides, CAP chooses, and
   says that it is choosing.
4. **Runtime inspection of the schema actually delivered.** Every rule below is enforced against the
   Arrow schema in hand, never against a remembered driver mapping.
5. **Measurement — supporting evidence only.**

> **THE RULE ABOUT RULE 5, STATED SO IT CANNOT BE FORGOTTEN.** No rule in this profile is justified by
> *"the study measured it."* Measurement appears below only in blocks marked
> **`[evidence · non-normative]`**, and **every such block could be deleted without weakening any rule
> in this document.** Measurement is how we found out that a hazard is real; it is not how a rule
> acquires force. This is the whole reason CAP exists as a separate artifact instead of the study
> being ratified.

### The sentence CAP inherits and does not relitigate

> **Successful transport does not establish admissibility.**

Everything below is a consequence of taking that seriously.

---

## 1. Scope

CAP governs **the admission boundary** — the one place where governed law and a concrete physical
representation are both in hand.

It does **not** govern lowering: a governed `value_domain` is the bare token `"decimal"`, carrying no
precision and no scale, so there is nothing there to compare against a physical envelope and refusing
there would require inventing a precision (ruling 2026-09-12 §4). It does not govern the wire. It does
not govern where material comes from — that is the source-adapter contract's jurisdiction, and CAP
checks what arrived regardless of which adapter delivered it.

**CAP is profile-scoped.** It is the Platform execution profile's admission law. K0v2 is a different
profile with a different execution grammar and is **not** amended by this document; where the two
profiles must agree, they must be repaired together and explicitly (see
[`ruling_2026_09_14_realization_claim_null_semantics.md`](ruling_2026_09_14_realization_claim_null_semantics.md)),
never by one importing the other's table.

---

## 2. The value envelope — **deliberately narrow**

### V1 · governed value domain

| governed `value_domain` | CAP v1 |
|---|---|
| `decimal` | in scope |
| anything else — `integer`, `text`, `boolean`, `date`, `timestamp`, `time` | **REFUSE** |
| unestablished | **REFUSE** (want of law — there is nothing to admit against) |

### V2 · the admitted carrier — one shape

> **`decimal128(18, 4)`. Exactly that, and nothing else.**

| Arrow type of the value column | CAP v1 |
|---|---|
| `decimal128(18, 4)` | **ADMIT** |
| any other `decimal128(p, s)` | **REFUSE** |
| `decimal256(p, s)` | **REFUSE** |
| `float32` / `float64` | **REFUSE** |
| `string` / `large_string` / `string_view` | **REFUSE** |
| `int8…int64`, `uint*` | **REFUSE** |
| `bool` | **REFUSE** |
| `timestamp[*]`, `date32`, `date64`, `time32`, `time64`, `duration`, `interval` | **REFUSE** |
| `list`, `large_list`, `struct`, `map`, `union`, `dictionary`, `fixed_size_binary`, `binary`, `null` | **REFUSE** |

**THE BROAD STATEMENT IS NOT RATIFIED.** The proposal on the table before the audit was *"all
`decimal128(p,s)` with 1 ≤ p ≤ 38, except (38,0)"*. That is withdrawn, for four reasons that are
reasons about **evidence**, not about caution:

- the excluded case `(38,0)` was excluded on a **misread discriminator** — the hop-four collapse is
  keyed on a value's digit count exceeding its declared precision, not on the `(38,0)` shape
  (study §0 `[E11]`), so the exclusion did not describe the hazard it was aimed at;
- the widest shapes cited in support — `(38,10)`, `(38,37)` — **never crossed hop four** at all
  (`[E4]`), and hop four is the hop inside the Platform;
- **no case above precision 38 was ever run** (`[E3]`), so the upper bound of the proposed range was
  not a measured boundary;
- the interior of the range — the great majority of `(p, s)` pairs — was **never measured on any
  crossing**. A range whose interior was never crossed is not an envelope; it is an extrapolation
  from the type system, and the type system is exactly what rule 2 above says is not evidence that a
  driver uses it faithfully.

**Therefore:** CAP v1's first positive ingress supports the **exact governed revenue case** and
nothing else. This is not a claim that `decimal128(9,2)` is unlawful. It is a statement that CAP v1
does not admit it, and that the way to make it admissible is §8, not an argument.

> **`[evidence · non-normative]`** `decimal128(18,4)` is the best-evidenced point in the corrected
> record: exact end to end on `duckdb-adbc` (run 1), exact end to end on `duckdb-native` through both
> the `RecordBatchReader` and `.read_all()` (run 2 §A), and exact through the complete path a CAP
> ingress would take — `→ arrow → to_pylist → pl.from_arrow` — in run 3's companion measurement. It is
> also the shape the lighthouse publication's `revenue` family actually governs. **If this block were
> deleted, V2 would still say `decimal128(18,4)` only**, because V2's force comes from being a
> deliberately narrow profile choice (authority 3), not from the measurements.

### V3 · every value must fit its declared precision — **PROPOSED, and flagged**

A driver may emit a value **out of range for the Arrow type it declares**. This is not hypothetical:
DuckDB's `HUGEINT` → `decimal128(38, 0)` mapping does it, and the resulting values lose digits at the
in-process conversion while nothing raises (study §0 `[E11]`, `run_3_errata_checks.txt`). pyarrow
itself will not construct such an array in-process — it raises `ArrowInvalid` — so the only way one
exists is that a driver built it.

**The rule proposed:** every non-null value in the admitted column must satisfy
`len(digits) ≤ declared precision`; any that does not is refused.

> ⚠ **This is the one rule in CAP v1 that is not merely a narrowing of what is already shipped, and
> it is flagged rather than assumed.** It is an **O(n) pass over values**, where every other check
> below is O(1) on schema or O(n) on coordinates that are already being scanned. It is also, at CAP
> v1's single admitted shape, **not obviously reachable** — the measured out-of-range emission is a
> `HUGEINT` mapping, and no `HUGEINT`-shaped source path is admitted here at all. So the question for
> ratification is whether CAP v1 pays a values pass for a hazard its own envelope may already
> exclude, or states the hazard and defers the check to whichever amendment first admits a shape that
> can reach it. **Recommendation: defer, and record the hazard as a named precondition of every §8
> amendment** — because the cost is real now and the hazard is not, and because an amendment that
> admits a wide decimal is exactly the moment someone should be made to think about it again.

### V4 · carrier NULL is not analytical absence — **retained unchanged**

Shipped, ruled (2026-09-12), and not reopened here. A carrier null is refused unless the family's C9
carries a rule about **absent observations** — and C9's *standing* is not that rule, because
`empty_fiber` answers what a fold over an **empty fiber** denotes, which is a different object and is
numerically coincident with absence under SUM. CAP v1 restates the shipped behaviour and changes
nothing about it.

---

## 3. The coordinate envelope — governed types are governed facts

The anchor declares its components **with their types** — `sale_at{store: text, day: date}` — and
CAP v1 treats those as what they are: governed facts of the same standing as the value domain. They
are currently read by nothing (OF-48).

### C1 · names — **retained unchanged**

Exact set equality between the carrier's coordinate columns and the anchor's declared components, in
both directions. Not a subset test in either direction: a missing coordinate retains a value at a
point **coarser** than the one it was constituted at, which is movement and needs a positive licence;
an extra coordinate retains it at a **finer** point than the anchor names, which the publication never
declared.

### C2 · types — **CLOSED MAPPING, exact, new**

| governed component type | the ONE admitted Arrow type | anything else |
|---|---|---|
| `text` | `string` (Arrow `utf8`) | **REFUSE** |
| `date` | `date32[day]` | **REFUSE** |
| **any other governed type** — `integer`, `decimal`, `boolean`, `timestamp`, `time`, or a type this profile does not recognise at all | — | **REFUSE** |

**Closed, not coercible.** A governed `date` presented as an Arrow `string` is refused even where the
string would parse. Parsing it would put a semantic decision — what `'2026-01-01'` denotes, in which
calendar, under which locale — **inside admission**, which is the profile deciding a governed meaning.
That is the same substitution V4 refuses on the value axis, and it is refused here for the same
reason.

**Narrow within the Arrow type too, and deliberately.** `large_string` and `string_view` are refused
for a governed `text`; `date64[ms]` is refused for a governed `date`. These are not oversights. They
are the point of authority 4: the profile inspects the schema **actually delivered**, so a driver
upgrade that starts emitting `string_view` surfaces as a **refusal a human reads**, not as a silent
pass that a later hop reinterprets.

**An unrecognised governed coordinate type refuses** rather than being waved through — the same
discipline the value domain already applies: *"we did not recognise it" must not read as "it is
fine"*.

### C3 · nullity — **coordinate NULL refuses, new**

**Any** null in **any** coordinate column refuses the whole carrier. Not the row — the carrier.

> **An analytical point cannot be partially specified merely because Arrow can carry a validity
> bitmap there.** `store=None` under an anchor that declares `store` is not a point, and a value
> retained at it is retained nowhere.

This is a **structural** rule (authority 2 + 3): Arrow's validity bitmap is a property of the format,
and the profile's choice is that the format's ability to say "absent here" does not give a coordinate
column permission to use it.

**Refusing the carrier rather than dropping the row is the conservative branch and is deliberate.**
Dropping rows would silently change which analytical points the answer covers, which is a disclosure
question nobody has ruled — and an admission boundary that quietly narrows the population is a worse
defect than one that refuses.

### C4 · grain against governed contribution structure — **retained unchanged**

The realization's `grain` claim and the family's C4 `contribution_structure` must agree. Two different
facts; the check is that they agree, not that either is read off the other.

### C5 · the coincident claim against the material — **retained unchanged**

Where `grain == coincident`, no analytical point may carry more than one contribution in the delivered
material. Note for readers of OF-48: **C5 is not, and never was, the coordinate type/nullity check** —
it keys points on coordinate *values*, and a null is a perfectly good key.

---

## 4. Refused by profile non-support — the explicit list

Every entry here is refused because **CAP v1 does not support it**, not because the representation is
unlawful. Naming that distinction per line, rather than once at the top, is the point of the section:
a future amendment should be able to admit any of these without contradicting a ratified claim.

| refused | the reason, precisely |
|---|---|
| **timestamps** as a value domain or a coordinate type, every unit, tz-aware or not | profile non-support. The record also contains two unresolved questions about them — that the tz **type** is set by session configuration rather than by data, and that sub-microsecond **value** preservation was never observed (`[E7]`) — neither of which CAP v1 needs to resolve in order to refuse. |
| **integer value domains** | profile non-support. Separately: COUNT's §11.5.1 target is not machine-readable (OF-44), so admitting an integer domain now would build the carriage for a semantics nobody has selected. |
| **booleans** | profile non-support. |
| **nested types** — `list`, `struct`, `map`, `union` | profile non-support. The record's own verdicts here are among the weakest it has (`[E5]`, `[E6]`), which is a reason not to build on them and not a reason to call them unlawful. |
| **strings as value carriers for a governed decimal** | profile non-support — **and note it is not the same case as a float.** A `TEXT`-stored decimal preserves the characters exactly at the source; what it lacks is the governed carrier type. That makes it a plausible *future* amendment and a poor *current* one, because admitting it means CAP deciding how to parse a decimal, which is §3's objection again. |
| **floats** for a governed exact-decimal domain | **NOT merely profile non-support.** Already ruled (2026-09-12): binary floating point *is not an exact-decimal carrier at all*, so delivery succeeding is precisely when the value is already not the governed one. This line keeps its stronger reason and its existing refusal text. |
| **unsupported decimal shapes** — every `decimal128(p,s)` other than `(18,4)`, and all `decimal256` | profile non-support, per §2. |
| `large_string`, `string_view`, `date64[ms]` | profile non-support, per C2 — listed separately because they are the cases a dependency bump is most likely to introduce. |

---

## 5. Which jurisdiction each refusal carries

The most consequential table in this document, and the one most worth ratifying explicitly: **the
same refusal in the wrong jurisdiction sends an operator to fix the wrong thing.**

| condition | jurisdiction | why |
|---|---|---|
| governed value domain **unestablished** | **want of law** | nothing to admit against; admission may not choose a domain on the law's behalf |
| governed formation responsibility unestablished, or a non-primitive family on the material path | **want of law** | as shipped |
| C9 carries no rule about absent observations, and the carrier has nulls | **want of law** | as shipped (V4) |
| governed value domain is recognised but outside CAP v1 (`integer`, `boolean`, …) | **unsupported by this profile** | the law is fine and the material may be fine; *this profile* does not implement it. Wire reason `unsupported` → mood `ERROR`, realization jurisdiction internally (ruled 2026-09-14) |
| governed **coordinate type** outside C2's closed map (e.g. a governed `timestamp` component) | **unsupported by this profile** | same: a capability limit, not a defect in the material |
| governed type is in C2's map but the delivered Arrow type differs | **want of state** | the *material* is wrong for a law this profile does implement — and **re-realization is the remedy**, which is exactly what want-of-state carries |
| value carrier is not `decimal128(18,4)` where the governed domain is `decimal` | **want of state** | same reasoning |
| value carrier is a **float** | **want of state** | as shipped, under the 2026-09-12 ruling |
| **coordinate NULL** | **want of state** | the point is unspecified in the *material*; re-realizing against a source that supplies it is the remedy |
| grain claim contradicts governed contribution structure | **want of state** | as shipped |
| coincident claim contradicted by delivered multiplicity | **want of state** | as shipped |
| value out of declared precision (V3, if adopted) | **want of state** | the driver emitted material its own declared type cannot hold |

**The dividing line, stated once:** *want of law* = the publication has not established something.
*Want of state* = the law is established and the **material** does not answer to it; re-realize.
*Unsupported* = both are fine and **this profile** cannot carry it. A capability limit must never be
dressed as a governed refusal, because it would tell an operator to go and re-materialize against a
capability that does not exist.

---

## 6. Ordering — **CAP v1 carries no ordering guarantee**

Stated positively so it cannot be inferred away:

> **CAP v1 makes no guarantee about the order of rows in admitted material, and nothing downstream
> may depend on one.** Admission neither imposes an order nor preserves one, and an admitted carrier's
> row order is not a fact about anything.

Any result whose meaning depends on order needs an explicit governed ordering fact. No such fact
exists in the governed model today, so no such result is servable under CAP v1.

> **`[evidence · non-normative]`** The record contains a 5-run row-order stability observation on
> `duckdb-native`. It is **not cited in support of anything** and cannot be: stability across five
> runs establishes nothing about ordering, as the study's own §5 says. It is mentioned here only so
> that a reader who finds it does not mistake it for a basis.

---

## 7. What CAP v1 deliberately does not do

- It does not widen to what Arrow can represent. The format's capability is not a licence.
- It says nothing about **eligibility, participation or support** — those are analytical standing, and
  no transport-level rule speaks to them.
- It does not establish **currency or freshness**. A realization claim's currency remains an open
  jurisdiction; admission checks the carrier, not the claim.
- It does not license a **join**. One governed-family execution must be satisfiable from one material
  object (see the source-adapter contract §7); anything else is `unsupported`.
- It makes **no claim about precision above 38**, in either direction — the record contains no such
  case (`[E3]`) and CAP will not invent one.
- It does not amend K0v2.

---

## 8. Amendment — how a shape becomes admissible

A shape is added to §2 or §3 only by **both** of:

1. **A measurement through the complete path the Platform actually uses** — source → driver → Arrow →
   in-process carrier, including `pl.from_arrow` and any `to_pylist` hop — for the specific `(p, s)` or
   Arrow type being added, with the raw run committed; **and**
2. **A ratified amendment to this profile.**

**Neither alone suffices, and the asymmetry is the point.** A measurement can only ever *permit* a
ratification; it can never *be* one. That is the whole correction this profile exists to embody, and
writing it into the amendment rule is how it survives the people who remember why.

Any amendment that admits a decimal shape wider than `(18,4)` must additionally record a decision on
**V3** (out-of-precision values), which is the hazard the current envelope may be accidentally
excluding rather than deliberately handling.

---

## 9. What this changes in shipped code

CAP v1 is a contract, not a patch. For review, the mapping onto `columna-platform/admission.py`:

| shipped | under CAP v1 |
|---|---|
| CHECK 1 · domain vocabulary `{decimal}` | unchanged |
| CHECK 1 · refuse float | unchanged, keeps its stronger reason (§4) |
| CHECK 1 · refuse non-decimal | unchanged |
| CHECK 1 · `precision > 38` refuses | **subsumed** — only `(18,4)` is admitted, so the bound is no longer load-bearing |
| CHECK 1 · `(38,0)` refuses, on the fourth-hop reason | **removed as written.** Subsumed by V2; and its stated reason is wrong (`[E11]`) — see the open ruling in §10 |
| CHECK 2 · carrier null vs analytical absence | unchanged (V4) |
| CHECK 3 · grain vs contribution structure | unchanged (C4) |
| CHECK 4 · coordinate names | unchanged (C1) |
| — | **NEW** C2 · coordinate types, closed mapping (OF-48) |
| — | **NEW** C3 · coordinate nullity (OF-48) |
| CHECK 5 · coincident vs delivered multiplicity | unchanged (C5) |
| — | **PROPOSED, recommended DEFERRED** V3 · value fits declared precision |

Each new rule needs a positive control **and** a negative control that fails without it — including
the three cases OF-48 measured serving today (`int32` for governed `text`, `string` for governed
`date`, and a `NULL` coordinate).

---

## 10. Open, for ratification

1. **V3** — adopt the out-of-precision value check now, or record the hazard and defer it to the
   first §8 amendment that admits a shape which can reach it? *(Recommendation: defer.)*
2. **The `(38,0)` refusal's stated reason in shipped code is wrong** (`[E11]`), independently of CAP
   v1 subsuming the refusal. Does that want its own OF row, or is recording it in the study's errata
   and in this table sufficient?
3. **Should `string`/`large_string`/`string_view` and `date32`/`date64` narrowness be restated as a
   general principle** — *"one governed type admits exactly one Arrow type, chosen explicitly"* — so
   future amendments inherit it, rather than as three specific lines?
4. **Naming.** This document uses **Carrier Admission Profile (CAP)** from the instruction. Is that
   the durable name, and is `v1` the right index given the profile has shipped four unversioned checks
   already?
