# C3 · the candidate admission rule, tested to destruction

**2026-09-22. Discovery only. No implementation, no serialization, no native movement licence, no
P1-33 repair, no `MovementLicence` migration, no Frame-QL change, no producer change.** The working
tree is unchanged; two throw-away probes were run against the shipped engine and deleted, and their
transcripts are reproduced below.

**The rule under test** (Huayin, 2026-09-22):

> A measure family has a family root `A₀`. Its analytical domain is generated from that root through
> the governed geometry of its universe. Every geometrically available projection from `A₀` is
> admitted unless the distinctions forgotten by that projection intersect distinctions the family law
> explicitly prohibits.
>
> `A ∈ 𝒜_F  ⟺  A₀ ⪰ A  ∧  Spent(A₀→A) ∩ β_F = ∅`

**Method.** Corpus first, adversarially: ToD v7.1 + its statistical extension, Measure Algebra v2.0
(draft4 and rev1) + v1.0's Contract Calculus, Frame-QL 1.0 and the two adjudication rulings, the
legacy `FAMILY … BLOCKED {…}` / B-anchor / `FERTILE` machinery, and the native geometry now shipping.
Every family form named in the instruction was tested. Two live probes were run rather than argued.

---

## 0 · Verdict

**The rule survives as a DOMAIN rule within the scope the native model currently admits, and it is
not the whole of admission. It is falsified as a general biconditional, and every falsifier lies
outside the currently admitted scope — which is the useful part of the result, because each one names
precisely what will break it later.**

| | |
|---|---|
| **Survives, tested** | SUM · COUNT · MEAN · MIN · MAX · composite families whose state moves while the displayed value does not · incomparable anchors · ordered families · covariance/multi-input · contextual families · participation/support qualifiers |
| **Not a counterexample, and it refutes the one I expected** | ToD **§8.4** — *"Intermediate anchors need no new point order"*. Ordered families were the likeliest break and the theory closes it explicitly |
| **Falsifies the BICONDITIONAL, not the domain** | **`h ∈ γ(κ)`** — coverage permission is a second, positive, independent premise. Anchor-uniform, so it does not disturb the domain's shape |
| **Genuine falsifiers, all out of current scope** | **G2.8** relationship expansion (replicate/assign/allocate) · **§10.1(2)** non-commutative continuation laws · **Case G** anchors |
| **Ill-typed as written, and must be corrected either way** | `β` is **capability-indexed** in the corpus, not family-indexed · `β` **accumulates** (`β′(κ)=⋃ᵢβᵢ(κ)`) · **`Spent` is never defined**, and the corpus is split three ways on its type |

**Stopping point, as instructed:** I did not find a genuine counterexample to the *domain* rule inside
the admitted scope, so I did not stop early. §8 gives the smallest native C3 contract that follows.

---

## 1 · The rule, computed

Before arguing, run it. Over the shipped native fixture, with `Spent` taken to be C1's already-shipping
`Anchor.projection_forgets`:

```
U = harbour, constituents ['berth', 'day']
F = berthings, root A0 = harbour{berth, day}

  A0 >= harbour{berth, day}      spent = []
  A0 >= harbour{berth}           spent = ['day']
  A0 >= harbour{day}             spent = ['berth']
  A0 >= harbour{}                spent = ['berth', 'day']

  beta_F = []                 ->  A_F = [[berth,day], [berth], [day], []]
  beta_F = ['day']            ->  A_F = [[berth,day], [day]]
  beta_F = ['berth']          ->  A_F = [[berth,day], [berth]]
  beta_F = ['berth','day']    ->  A_F = [[berth,day]]
```

Now the same law as the shipped legacy engine actually enforces it. `afternoon.cml` declares a
POSITION — `MEASURE on_hand ON stock_snapshot` over `store * day`, `FAMILY { sum BLOCKED { calendar } }`
— and the probe asks the same measure at seven locations:

```
AT {store, month}    CLIMB within calendar: day -> month        -> refuse  blocked_reduction
AT {store, quarter}  CLIMB further: day -> quarter              -> refuse  blocked_reduction
AT {store}           DROP the day constituent entirely          -> refuse  blocked_reduction
AT {month}           DROP store, keep a calendar climb          -> serve   [1065, 980]
AT {region, month}   CLIMB geography, keep month                -> serve   [240, 825, 760]
AT {}                DROP everything -> the scalar anchor       -> refuse  blocked_reduction
AT {store, month}    CONTROL: max along calendar (not barred)   -> serve   [320, 240, 220]
AT {store, month}    CONTROL: a FLOW along calendar             -> serve   [150.0, 125.0, 300.0]
```

**⟨measured⟩ the shipped behaviour is exactly `Spent ∩ β ≠ ∅`, with `β = {the time axis}`.** Two
results are worth singling out:

* **`AT {store}` refuses.** Dropping the `day` constituent *entirely* is covered by a bar written as
  `BLOCKED { calendar }`. So the legacy lineage index is not merely about climbing a hierarchy — for
  the Case-S projection it behaves precisely as "may not spend `day`".
* **`AT {month}` and `AT {region, month}` serve.** Spending `store` is lawful for the same measure
  under the same reducer. **Admission is decided by the axis spent, not by the target.**

The native computation above and the legacy transcript agree cell for cell under `store↔berth`.

---

## 2 · The form-by-form test

| form | result | why |
|---|---|---|
| **SUM** | survives, β declared | `composition=ADDITION, has_identity=True`. Nothing in the law entails a β: a *flow* declares `β=∅`, a *stock* declares `β={time}`. This is the 2026-08-20 ruling's own point — *"do not infer a global stock personality"* |
| **COUNT** | survives, β=∅ | `entails_continuation=SUM`. `count(I)` vs `count(x@I)` are distinct targets (§11.5.1) but `I` is constitutive and stays inside `F` (§2.2), so moving the current anchor does not reinterpret it |
| **MEAN** | **survives, and it is the sharpest confirmation of the C7/C3 split** | ⟨measured, shipped vocabulary⟩ `entails_continuation=NO_CONTINUATION` (*"a mean of means is not a mean"*) **and** `state_basis=(SUM,COUNT)`. The displayed value does not compose; the basis does. So **what moves is the basis**, and C3 is not a fact about the value composing. β=∅ |
| **MIN / MAX** | survives, β=∅ | commutative semigroup, no identity. Composes over any fiber. The empty fiber is C9, not C3 |
| **ordered (FIRST/LAST)** | **survives — and ToD refutes the expected counterexample** | see §3 |
| **covariance / multi-input** | survives | the pairing anchor constrains **formation** (`Dom_L`), i.e. it fixes `A₀`; it is not a test on `𝒜_F`. *"Once joint pairing information has been discarded, independent marginal states cannot reconstruct Σxy"* is a **spend** condition — pairing ∈ β. Not natively expressible today in any case: covariance is not in the foundation vocabulary |
| **contextual families** | survives | ToD §3.4: *"A family constructed from a contextual expression is admitted only when … its claimed continuations are coherent over the admitted anchors without changing that formation. **This is the common family contract, not a second admission system.**"* The last sentence is the rule's strongest single endorsement |
| **incomparable anchors** | **survives, and §6.3 turns out to support it** | see §4 |
| **participation / support** | survives (edge) | MEAN's *"unchanged participation/support standing"*, COUNT's *"same participation rule"*. MA §21: *"Participation belongs inside the information law whenever an admitted continuation can observe it"*, and §5 lists participation among the distinctions in `Ω_L` — so "do not change the participation rule" **is** "do not spend that distinction" |

---

## 3 · Ordered families — the counterexample I expected, and why it is not one

I predicted this would break the rule: `LAST` ordered by `day`, root `{store, day}`, projected to
`{day}` — the order does not order stores, so the winner is undetermined. **ToD closes it explicitly.**

§8.4, *"Intermediate anchors need no new point order"*:

> "For `S ⪰ B ⪰ A`, the witness at `B` still identifies the winning **S-point**. The next combination
> uses `𝒪_S`, not a freshly invented order on `B`-point labels. … If a different ordered family is
> newly constituted at `B`, it needs its own governed order at that constitutive anchor. **This is a
> different formation question, not a prerequisite for continuing `W`.**"

and §5.7: *"A coordinate reference carried inside a FIRST/LAST witness likewise does not give the
witness-valued measure a second current anchor."* The ordering lives on the **constitutive** anchor
`S`, inside identity; the witness carries the winning S-point as part of its value. **The ordering
distinction is never in `Spent(A₀→A)` at all.** Nothing lands in β.

### But the probe found a real defect, in the legacy engine, one layer down

```
INVENTORY (store, day, level):   S1 2025-01-20 = 480   |   S3 2025-01-20 = 220
on_hand.last AT {store, month} -> serve   S1/2025-01 = 480 ; S3/2025-01 = 220
on_hand.last AT {month}        -> serve      2025-01 = 480
```

The latest January day carries **two** points, 480 and 220, and the engine serves 480. ToD §7.3 is
unambiguous:

> "Two distinct analytical points of `S` are distinguished by its **complete governed order**. … If a
> physical priority value or truncated label maps distinct points to the same comparison
> representation, **that representation has not realized the declared complete point order. Appending
> a storage identifier or relying on sort stability is not a repair of analytical law.**"

and §7.2: *"Day chronology within separately governed fixed-Customer contexts does not silently
establish Customer priority across those contexts."*

**`last ORDER day` over a `store * day` universe declares an order that is not complete on its own
points.** That is a **C2/formation** defect (order completeness), not a C3/domain one — the rule is
untouched — and it does **not** port: ⟨measured⟩ the native foundation vocabulary is
`{SUM, COUNT, MIN, MAX, MEAN}`, all commutative, none ordered, and `required_parameters` is empty for
every one. Ordered families are not natively expressible today.

> **Recommend rowing it** as a legacy finding: an ordered family whose governed order is incomplete on
> its constitutive points serves an arbitrary winner. Not repaired here; not in scope.

---

## 4 · Incomparable anchors — §6.3 supports the rule

§6.3, in full:

> "Family coherence does not erase partition geometry. Revenue at Week and Revenue at Month may belong
> to one additive family even when neither anchor refines the other. **The family guarantees agreement
> along admitted paths; it does not manufacture a path between incomparable locations.**"

A down-set generated from a root **is not a chain**: it routinely contains mutually incomparable
members. In the computed table of §1, `β=∅` admits both `{berth}` and `{day}`, and neither refines the
other, and no projection exists between them. §6.3 is making exactly this point — membership in `𝒜_F`
does not imply an edge in `Γ_F` — which is the domain/edge split the rule presupposes. **Not a
counterexample; a structural confirmation.**

Week and Month themselves are Case-G partitions of one axis and do not exist in the native model at
all (see §6).

---

## 5 · The four challenges, weighed

### Challenge A — `C_L` "contains … anchor … premises". **Downgraded: an empty slot.**

MA draft4 §4 lists the law tuple, and one bullet reads: *"`C_L` contains type, support, participation,
population, anchor, and other premises"*. On its face this is a positive anchor-condition component of
the law, which the rule has no slot for.

**⟨measured⟩ it is never used.** `C_L` (as distinct from the continuation class `𝒞_L`, with which the
draft collides notationally) occurs **three times in the whole document: in the tuple, in its own
defining bullet, and once in a box where it actually stands for the continuation class.** No rule
consumes it; no worked example exhibits an anchor premise from it. The only *worked* anchor premise
anywhere in the algebra is covariance's pairing contract, which governs **formation**.

> So `C_L` does not falsify the rule. What it does is **reserve room** for positive anchor premises
> that neither corpus has ever filled. ToD does the same thing from its side, and its version is more
> dangerous — §8.1's *"law-level domain admission"*, which imposes containment on a **witness family's**
> domain from a **target's** basis claim, and which explicitly disclaims the evidence reading. Both are
> recorded as the live risk to this rule (§9, Q-A).

### Challenge B — `h ∈ γ(κ)`. **Real, and it falsifies the biconditional, not the domain.**

`RED1` has two premises, not one:

> `Spent(q) ∩ β(κ) = ∅,   h ∈ γ(κ)` … *"Type compatibility is necessary but not sufficient. **Anchor
> movement and coverage permission are independent premises.**"*

`γ(κ)` is a **positive** set — coverage modes admitted for `κ` — and `S′ = S′_{q,h}`, so the output
support depends on it. If `γ(κ)=∅` nothing reduces, whatever β says.

**But γ is anchor-uniform**: it does not vary with the target, so it cannot make `𝒜_F` non-monotone
and cannot make it target-dependent. It is a second premise *of a movement*, which is the edge
contract's business — and it is the same `γ` the previous reconnaissance already flagged as having
*"no complete Core counterpart"*.

> **Verdict: the rule is correct about the DOMAIN and incomplete about ADMISSION.** Keeping the two
> apart — which the instruction requires — is exactly what makes γ land outside C3. It looks like
> participation/support (C5). It is still not C3's, and it is still missing.

### Challenge C — G2.8, relationship expansion. **A genuine falsifier, entirely out of scope.**

> *"if `χ` uses replication, `κ` lacks a duplication-invariance declaration, and a downstream reducer
> spends a tagged target axis, no inherited certification derivation crosses that reducer"* …
> **"Reachability therefore does not determine disposition."**

Three conjuncts, and two of them are not expressible in a fixed per-family `β`: the *upstream
disposition* (replicate vs assign vs allocate) is path-dependent, and the **tagged axis is created by
the expansion**, so no `β_F` fixed before the derivation can contain it.

This is the `G₂` fragment — `expand_χ`, membership universes, assignment and weighted allocation.
**Every one of those is currently HELD in the native model** (carve, membership universes,
cross-universe correspondence). It falsifies the rule for the fragment that does not exist here yet,
and it tells us precisely what will break first.

### Challenge D — §10.1 premises (2) and (3). **Genuine, and vacuous in the current vocabulary.**

> "(2) the state law admits the required regrouping; (3) the staging fibers form the governed
> partition/coarsening required by the law"

backed by MA v1.0 §4.1: *"For an associative but noncommutative law, **factorization may remain valid
while permutation does not**."* Two maps can spend the same set while only one regroups lawfully.

**In Case S the fibers of a projection *are* the governed coarsening** (set difference on constituents),
so (3) is automatic; and ⟨measured⟩ every law in the shipped vocabulary is `associative=True,
commutative=True`, so (2) is automatic. **The falsifier fires on the first non-commutative continuation
law, and there is none.**

---

## 6 · Can `β_F` be a set of universe constituents?

**Yes — and exactly, precisely, within Case S; and the corpus tells us what the general form is.**

* **In Case S it is exact.** A Case-S anchor *is* a set of constituents, so `⪰` is `⊇`, projection is
  set difference, and `Spent(A₀→A) = A₀ \ A` is a constituent set by construction. This is not a
  modelling choice; it is what Case S means.
* **ToD cannot define `Spent` in general, and says why.** §2.1.3: *"The constituent description need
  not be a uniquely discoverable factorization, and its dimensions need not be statistically
  independent."* An anchor is any governed partition (§2.1.1), so "the distinctions a projection
  forgets" has no canonical referent once anchors stop being constituent subsets. ⟨measured⟩ **ToD
  never uses the word "spent" at all** (0 occurrences in both v7.1 files).
* **The corpus is split three ways on `Spent`'s type** — axes (v1.0 §2.5, draft4 §30.1: *"blocked-axis
  … premises"*), analytical distinctions (v1.0 §7: *"a capability may spend only those analytical
  distinctions the contract permits"*), and implicitly anchors (`q : A → A′`). `Spent` is **never
  defined** in any source.
* **The legacy ancestor is indexed one level finer than a constituent.** `BLOCKED { calendar }` names a
  *lineage* — `day → month → quarter` — i.e. a chain of partitions of one axis. That is the Case-G
  generalisation of "a constituent", and it is why the legacy form needs a lineage where Case S needs
  only a name.

> **So: `β_F` as a set of `U`'s constituents is coextensive with Case S — adequate exactly while Case G
> is held, and the thing that must generalise to "governed distinctions" when Case G lands.**

### Two type corrections the rule needs regardless

1. **`β` is capability-indexed in the corpus (`β(κ)`), not family-indexed.** Natively that difference
   dissolves: a legacy `MEASURE … FAMILY { sum, last, … }` is *several* native families, each citing
   one continuation law, so *per capability × axis* becomes *per family × constituent*. The 2026-08-20
   ruling — *"applicability stays per operator × lineage"* — is preserved, not weakened, by the native
   family split.
2. **`β` is not a constant; it accumulates.** MAP1: `β′(κ) = ⋃ᵢ βᵢ(κ)`. **This is a derivation rule and
   it should be kept**: a constructed family inherits at least the union of its operands' prohibitions.
   It is the algebra's own analogue of ToD §8.1's domain propagation along the basis relation, and it
   means part of `β` for a construction is **derived, not declared**.

---

## 7 · Where the two legacy mechanisms actually belong

The legacy tree contains **both** polarities, and ⟨measured⟩ they attach to different objects — which
maps onto ToD's two symbols exactly:

| legacy | shape | ToD |
|---|---|---|
| `FAMILY { <agg> BLOCKED { <lineage> } }` · `BAnchor.blocked_lineages` — *"lineages this agg may NOT be reduced along"*, open-by-default | **negative, per axis** | **`𝒜_F` / `β_F`** — the domain |
| `<member> FERTILE { <lineages> }` + an adjudicated `License` (VERIFIED / CORROBORATED / UNTESTABLE), closed-by-default | **positive, per edge, evidence-bearing** | **`Γ_F(B→A)`** — the edge contract |

`model.py` states the polarity split in its own words: *"On DERIVED columns … closed-by-default; the
license opens travel. On MEASURE columns … open-by-default; the B-anchor closes."* **DG-4 is the row
where those two polarities were recorded as meeting, and it is still open.**

> **The candidate rule puts the allow-list shape where the legacy tree already put it — on edges, not
> on the domain.** That is the strongest independent corroboration found in this pass, and it was not
> designed toward: the two mechanisms predate the question.

**Polarity, settled.** The rule is *not* "absence of prohibition is permission", and the reason is
structural rather than rhetorical: **`β_F` has no meaning outside an established C3.** With C3
`UNESTABLISHED` there is no law to generate a domain from, so `𝒜_F = {A₀}` and nothing moves. The
positive act is establishing the law; `β` restricts what that law then generates. Frame-QL's own ruling
— *"Silence is not authority"* — is untouched.

---

## 8 · The smallest native C3 contract that follows

**One new carried fact.** For a family whose C3 is established:

> **`β_F` — the constituents of `U` that this family's law prohibits its sufficient state being
> composed away along.** Total over `A₀`'s constituents, so that a constituent's absence from `β_F` is
> a statement made under an established law, never a silence.

**Everything else is derived, and already ships:**

| derived | from | status |
|---|---|---|
| `A₀` | the family's own `constitutive_anchor` | ⟨measured⟩ **already carried by every family in both majors** — primitive and constructed alike. Nothing new |
| `⪰`, and `Spent(A₀→A)` | `Anchor.refines`, `Anchor.projection_forgets` | shipped in C1, tested |
| `𝒜_F` | computed on demand | **never stored** — ToD §4.1: *"not a proposed registry or new object"* |
| `β` of a construction | `⋃` over its operands (MAP1) | derived, not declared |
| path-independence of the domain | a consequence: `Spent` is compositional, so staged and direct agree by construction | supports Prop 6.1's premise rather than assuming it |

**Separately governed, and explicitly NOT C3:**

| fact | home | status |
|---|---|---|
| coverage permission `γ` / coverage mode | C5 participation-support, or `Γ_F` | **missing, confirmed real** (§5-B) |
| a basis's *domain of validity* (§5.1, §5.3) | C7 | ⟨measured⟩ implemented C7 is family-level; ToD's basis domains are anchor-level. **A gap** |
| complete governed order on `S` (§7.2, §7.3) | C2 formation parameters | not natively expressible yet; the legacy instance is defective (§3) |
| the edge premises: §10.1(4)(6), *"same participation rule"*, licence adjudication | `Γ_F(B→A)` | out of scope by instruction |

**The answerability rule, conceptually, once C3 exists** — unchanged in shape from C4, with step 3 now
computable:

```
1. GEOMETRY     A₀ ⪰ A            (computed; else not a location for F)
2. C7           a basis exists     (else unanswerable anywhere)
3. C3           established, and Spent(A₀→A) ∩ β_F = ∅
                (else want_of_law, NAMING the constituent that exceeded the law)
4. Γ / realization                 (not this unit's subject)
```

**Three spellings, one extension — flagged.** C3 `UNESTABLISHED`, C3 `EXPLICIT_NONE`, and
`β_F = A₀`'s constituents all yield `𝒜_F = {A₀}`. They mean different things (no law · a declared
negative · a law that prohibits everything) and the format currently distinguishes the first two. Whether
the third is a lawful spelling of the second is a representation question (§9, Q-C).

---

## 9 · What still needs a ruling

**Q-A · The reserved positive slot.** Both corpora keep room for positive anchor premises that neither
fills: MA's `C_L` (defined once, never used) and ToD §8.1's *"law-level domain admission"*, which
constrains a **witness family's** domain from a **target's** basis claim and explicitly disclaims the
evidence reading. Under the rule this lands on C7 (a basis claim restricted to where its components are
admitted), not on `𝒜_F`. **Confirm that reading**, because it is the one place the corpus uses the words
"domain admission" for something the rule does not generate.

**Q-B · Is `γ` C5's or `Γ`'s?** It is a real, positive, independent premise; it is not C3's; and it has
no home. Deciding this also decides whether "coverage mode" is a family law fact or a movement fact.

**Q-C · Three spellings of `𝒜_F = {A₀}` (§8). Keep all three, or collapse?**

**Q-D · Scope, stated so it cannot be forgotten.** `β_F`-as-constituent-set is coextensive with Case S.
**G2.8 and §10.1(2) are genuine falsifiers waiting on Case G, relationship expansion, and the first
non-commutative continuation law.** Recommend the ruling record the rule's scope explicitly rather than
as an unstated assumption.

**Q-E · `A₀` is a new object in the theory.** ⟨measured⟩ ToD has **no notion of a family root anchor as
a distinguished member of `𝒜_F`**; its nearest objects are the constitutive input anchor `I`/`S` (which
§2.2 keeps *inside* `F`: *"They do not become additional current anchors"*) and the universe root `R_U`.
The artifact's `constitutive_anchor` does name a location and every family carries one, so the rule is
implementable today — but **"family root" is the ruling's coinage, not the theory's**, and the theory
never states `A₀ ∈ 𝒜_F`. Q-1 of the previous reconnaissance is answered *by the rule's construction*,
which is a fine answer provided it is the ruling that says so.

### Recorded, not acted on

* **The ordered-family defect** measured in §3 — an incomplete governed order serving an arbitrary
  winner. Recommend rowing; legacy-only; does not port.
* **C7's granularity** — family-level as implemented, anchor-level in ToD §5.1.
* **DG-4** remains the same question from the legacy end, still open, and now with a recommended answer.
* **OF-59, F-3, P1-33, P1-34, OF-48, OF-58** — untouched.
