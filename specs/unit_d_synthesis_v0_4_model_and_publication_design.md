# Unit D — v0.4: the settled successor model, and the smallest publication design
## Final conceptual model · twelve showings · `firstlight` migration · format consequence

**Status:** desk draft, 2026-09-11, **for authorization**. No implementation.
**Supersedes** v0.3 (which supersedes v0.2, which supersedes v0.1). **Evidence base:**
`unit_d_d1_crosswalk_v0_1.md`. **Target text:** ToD **v7.1**, DOI `10.5281/zenodo.22649945`.

---

## PART I — THE SETTLED MODEL

## 1. Settled (ruled 2026-09-11)

- **`MeasureFamily F` is the analytical identity.**
- **`Measure = F@A`**, and it is **not another governed catalog object**.
- **Primitive/constructed** and **named/query-constructed** are not separate ontological kinds.
- **Legacy `member` retires** rather than mapping one-for-one into the new model.
- **Shared foundation laws** are governed reusable vocabulary; a foundation-law token is a
  constituent of `Law(F)`, **not a family identity**.
- **Stable `family_id`**, distinct from canonical name, is required; generation remains open.
- **Absence of prohibition means unestablished, never permission.**

## 2. The seven closures v0.4 adds

| # | closure | consequence |
|---|---|---|
| 1 | **Never promote a legacy `member.anchor` to constitutive anchor.** Three things stay distinct: *constitutive formation/intake anchor* · *current anchor of `F@A`* · *physical source grain*. They may coincide; they are not definitionally identical. **And formation stays separate from continuation even where both name SUM.** | §3, §4.2 |
| 2 | **Foundation-law standing is positive presence.** *A family foundation law must be positively present in the family's semantic constitution, either by constitutive declaration or because an admitted canonical family-forming construction entails it.* **Never inherited** from a parent family, a namespace, a realization mapping, or an available engine operator | §4.3 |
| 3 | **MIN/MAX empty fibers are a theorem of the law**, established once and never re-asked | §4.4 |
| 4 | **Retire the governed kind named `measure`** — the name is taken: ToD defines a Measure as `F@A`. Prefer canonical family reference directly; aliases/default completion become **non-identity reference metadata** | §5 |
| 5 | **Migration evidence is not governing authority.** Legacy names and `root_evaluator` seed *proposals*; they may not become definitions. **Do not assume MIN/MAX/COUNT targets are governed because their names imply them.** Do not optimize the model around a fixed number of interview questions | §11 |
| 6 | **Family-law authority is a third standing**, distinct from mathematical entailment and runtime capability. Do not auto-generalize the universe-only ratification schema | §9 |
| 7 | **Query-constructed families** resolve a MeasureFamily under the same ontology as named ones. Persistent-ID/publication lifecycle open | §7.4 |

## 3. Three anchors, and why conflating them is the original defect

```text
I   constitutive formation / intake anchor   ANALYTICAL — inside F, identity-bearing (§2.2)
A   current anchor of F@A                    ANALYTICAL — a request coordinate, never declared
g   physical source grain                    REALIZATION — the grain the backend delivers at
```

§2.2 puts `I` inside `F` and forbids it becoming a current anchor. §2.2 also rules on `g`:
*"A physical key may represent the point; it does not define the point's analytical standing merely
by being unique in a table."*

**Their relationship is a claim, not an assumption.** Where `g` is finer than `I`, the resolution of
several contributions into one constituted value **is analytical law** — it is formation, C4. Where
`g` and `I` coincide, that coincidence is itself a claim the realization asserts and the consumer
checks. Neither may be inferred from the other.

This is the same defect D1 found, seen at the other end: D1 showed `root_evaluator` deciding
**continuation** from the realization side; the `firstlight` contribution-grain finding shows the
same token deciding **intake resolution** from the realization side. One token, two jurisdictions
violated, at both ends of the family's law.

---

## PART II — THE PUBLICATION DESIGN

*Field spelling is subordinate throughout. What is being fixed is which objects are serialized, what
each is authoritative for, and what a consumer must do with each.*

## 4. Showing 1 — the governed analytical objects actually serialized

| kind | status | authoritative for |
|---|---|---|
| `universe` | **unchanged** | population: basis, restriction, anchor, existence law |
| `anchor` | **unchanged** | analytical location and components |
| **`family`** | **the one new kind** | everything in §4 of ToD — *one authoritative account*, in one record |
| `attribute`, `relationship`, `hierarchy`, `crosswalk` | **unchanged** | as today; carried whether or not a consumer can read them |
| ~~`measure`~~ | **RETIRED** (closure 4) | — |
| ~~`member`~~ | **RETIRED** | — |
| ~~`boundary`~~ | **RETIRED as a kind** — its content is C3, folded into `family` | — |

**The publication gets smaller: three kinds retired, one added.** That is the strongest evidence the
model is right — a correct ontology should not need more records than a fossil one.

### 4.1 Why `boundary` folds rather than survives

Domain and movement is **C3**, one of the nine responsibilities, and §4 requires *"one authoritative
account"* of them. A prohibition held in a separate record makes admission a join across two records
and reintroduces exactly the admitted/prohibited/unestablished ambiguity R4 closed.

**The counter-argument, recorded:** a prohibition is often authored by a different person at a
different moment than the family. That is an **authority** concern, and authority is carried
separately (§9) — so it does not require a separate *meaning* record. Folding is recommended; the
counter-argument is named so the ruling is informed.

### 4.2 One record, five content groups

Not five records. §4: *"They are not separate ontological kinds or necessarily separate records."*

| group | carries | §4 |
|---|---|---|
| **Constitution** | target statement; **formation**; **constitutive anchor(s) `I`**; parents (for constructed families); identity-bearing law parameters (e.g. the order for FIRST/LAST) | C1, C2, C4 |
| **Law citations** | the **formation law** and the **continuation law**, cited *separately* (closure 1) | C1, C7, C8 |
| **Participation** | eligibility and participating contributions, grounded on the universe | C5 |
| **Domain & movement** | `𝒜_F`; per-edge conditions `Γ_F(B→A)`; explicit prohibitions | C3 |
| **Exceptional cases** | only what is **not** derivable: Φ where it is a choice, empty-result rules beyond the law's theorem, approximation conventions | C9 |

**C6 (semantic values) appears in none of them, deliberately.** The operand domain is declared on the
primitive family; every downstream result domain is **derived** from the cited law plus the operand
domain. Columna already does this correctly (`planner.py:2713`), and inventing a slot for it would
re-create the fossil it already escaped.

### 4.3 Formation and continuation are cited separately — even when both are SUM

Closure 1's last line, and it is not a nicety.

- **Formation law** answers: *how is the quantity constituted at `I` from participating
  contributions?*
- **Continuation law** answers: *how do established values compose across admitted refinement?*
  (§5.2's self-sufficiency.)

They answer different questions and can differ. COUNT is the standing proof from the other
direction: its formation counts participations, its continuation **sums** count-states (§5.2:
*"two retained count states 37 and 12 can combine to 49 under count-state continuation. Counting the
two scalar values as new observations gives 2"*). One citation cannot discharge both without
re-creating exactly the "one token, five responsibilities" defect D1 named.

**Continuation has three states, like every other law fact:** a cited law · an explicit **none**
(the family does not compose across refinement — a positive declaration) · **unestablished**.

### 4.4 What is derived, and never asked

The derivation rule, both clauses:

> **(i) Derivation is only ever from another declaration** — never from a name, never from a mapping,
> never from execution.
> **(ii) Declaration is for choices; derivation is for consequences.** A human is asked only where
> analytical meaning is genuinely chosen.

Derived, therefore never a field: result and state value domains (from cited law + operand domain) ·
self-sufficiency, identity existence, re-entry coherence (theorems of the cited law) · **MIN/MAX
empty-fiber behaviour** — the semigroup supplies no identity, therefore no fold value (§5.2, §6.1.1,
§11.5.1) · lineage edges (from formation's parents — §7.3) · the B-anchor verdict (declared lineage ∩
declared movement conditions).

## 5. Showing 2 — family identity and canonical reference

| carried | rule |
|---|---|
| **`family_id`** | opaque, stable, **required**. Distinct from canonical name, **foundation-law name**, namespace alias, and realization mapping key. Generation open. §2.2: *"A digest is one possible implementation, not a required mechanism"* |
| **canonical reference** | the family's canonical name or canonical construction. §2.2: *"Canonical names resolve this identity; they do not mint it"* |
| **aliases / default completion** | **non-identity reference metadata** (closure 4). Optional, and attached to the family it resolves to — not to a container object |

**Resolution is one-directional and namespace-versioned:** name → `family_id`, within one namespace
version. Nothing resolves `family_id` → name for any governance purpose. §2.2: *"Two distinct active
identities cannot be hidden under one ambiguous canonical reference."* This single rule is what
closes the synonym-operator hole D1 reclassified.

### 5.1 The `firstlight` test closure 4 asked for — it passes

*"Test whether the primitive family can simply carry canonical reference `revenue`, eliminating the
old grouping and `root_member` altogether."*

**It can.** Exactly one family wants the name `revenue`; it carries it as its canonical reference;
there is nothing to group and nothing to default-complete. **`measure` and `root_member` both
disappear from `firstlight` with no loss** — which is the cleanest possible confirmation that neither
was carrying analytical content.

Default completion survives in the model for the case §3.9 actually describes — *"a governed
single-valued default completion may allow a shorter reference to resolve to an already specified
construction"* — e.g. a namespace where bare `revenue` should resolve to a constructed family rather
than to a family literally named `revenue`. `firstlight` is not that case.

## 6. Showing 3 — how the §4 responsibilities are carried without inventing records

§4.2's table is the answer; three economies are worth stating explicitly, because each is a record
that a less careful design would have created:

1. **No `Σ(F)` record.** §2.2: *"the signature is not an additional ontological kind."* The signature
   is the canonicalization of the constitution group; `family_id` is bound to it. Nothing is stored
   twice.
2. **No lineage record.** A constructed family's formation names its parents by `family_id`, and
   §3.7 defines the edge as exactly that: *"A directed edge from `F` to `G` records that the governed
   constitution of `G` depends on `F`."* **Lineage is derived from formation**, and well-foundedness
   (acyclic, rooted in primitive families) is checkable rather than asserted.
3. **No state-schema / combine-law records.** Those live in the cited foundation law, once, shared.

## 7. Showing 4 — how foundation-law vocabulary is referenced

**Shared, versioned, external to the publication; cited, never embedded.**

- **Cited by `(law name, vocabulary version)`.** Embedding the law's content would let two
  publications disagree about what SUM is, which is the one thing shared vocabulary exists to prevent.
- **Semantic content only** (v0.3 §4): the continuation law on the value domain; the value-domain
  rule; algebraic properties; required law parameters. **Not** `deliver_sql`, `scan_impl`, `in_core`,
  planner `kind`, or the representation/approximation halves of `witness`.
- **A citation must be checkable.** A consumer that does not know a cited law **refuses** — it cannot
  guess, and it must not drop the family (§10).

### 7.1 Positive presence (closure 2)

> A family's foundation law is present **because the family declares it constitutively**, or
> **because an admitted canonical family-forming construction entails it** — and by no other route.

Never from a parent family; never from a namespace; never from a realization mapping; never from the
fact that an engine happens to register an operator of that name. **A family with no constitutive
citation and no entailing construction has no established law** — it is not admissible, and that is
a positive fact the publication can state.

### 7.2 Entailment by construction, stated carefully

Where a family is formed by `mean(revenue@order)`, the construction entails MEAN. Entailment is only
available where the construction is **complete and admitted** — an incomplete construction entails
nothing and mints nothing (§3.6: *"A general expression can also produce a result without minting a
family"*).

### 7.3 Constructed-family lineage (Showing 6)

Carried by formation, per §6.2 above. Two properties a consumer checks rather than trusts:
well-foundedness, and that every parent reference resolves to a declared `family_id` in the same
publication or an identified external one.

### 7.4 Query-constructed families (closure 7)

Same ontology, same record shape when published. What stays open and is **not** decided here: whether
a query-constructed family's `family_id` is minted, resolved against an existing family, or held
transient, and whether it is ever serialized. The model does not need that answer to be consistent;
the lifecycle does.

## 8. Showing 7 — how unestablished law stays visibly unestablished

**The family record is TOTAL over the nine responsibilities.** Every one is present, carrying exactly
one of:

```text
declared       a statement of the law
none           an explicit positive negative  ("this family does not compose across refinement")
unestablished  explicitly not yet established
```

**Silence is not a representable state.** A responsibility cannot be omitted, so absence-of-record
can never be confused with absence-of-law, and "nobody asked" can never read as "nothing applies".

This one decision discharges **three** separate requirements at once, which is the strongest argument
for it:

1. **R4** — admission requires a positive `𝒜_F` *and* a positive edge condition; an `unestablished`
   movement can never be read as permission.
2. **Showing 10** — a consumer cannot silently omit a semantic field it did not notice, because
   there is no shape in which a field is missing.
3. **O10 / refusal totality** — the refusal test becomes structural rather than a rule someone must
   remember to apply.

## 9. Showing 8 — authority over family declarations

§4 names exactly three standings, and they are three different things:

> *"A declaration states a proposed definition. **Human ratification establishes the declaration's
> authority in its domain; it does not prove its mathematical laws.** A proof establishes a
> conditional analytical statement; it does not certify that a particular source currently satisfies
> its premises. A backend computation establishes neither merely by returning a value."*

**Smallest mechanism consistent with the model — and deliberately not the universe schema
generalized** (closure 6):

- **Authority is carried in the `authority` block, never inline in a declaration.** That existing
  discipline is right and is preserved unchanged.
- **A distinct record type from universe ratification**, because the two fingerprint *different
  things*: a universe's ratification pins its **existence law** (`elf-1`); a family's would pin its
  **identity-bearing constitution** — Σ(F)'s content. Reusing one record type would let a
  currency check compare incomparable things. Same envelope shape (who · when · what was pinned ·
  which pinning scheme), different scheme identifier, different record type.
- **Nothing else enters the artifact.** Mathematical entailment is *derived* by any consumer from the
  cited law — publishing a proof would be publishing a derivable fact. Runtime capability is the
  realization's business and belongs nowhere near meaning.
- **An unratified family is publishable**, because a declaration *is* a proposed definition. Its
  authority state is carried and visible.

**Raised for ruling, not decided:** whether serving an unratified family is refused, disclosed, or
permitted. That is a policy about consumption, and the publication's job is to make the state legible
rather than to decide it. Note the asymmetry it creates with universes, whose publish gate today
requires ratification currency — deliberate, and worth an explicit call.

## 10. Showing 9 — what physical realization is allowed to say

**May say:**

1. the family it realizes, **by `family_id` only**;
2. the endpoint(s);
3. a **grain-correspondence claim** — the source grain `g`, and how it corresponds to the
   constitutive anchor `I` (coincident, or finer). *A claim, checked by the consumer;*
4. a **delivery claim** — this backend expression discharges the declared formation law, and this one
   the declared continuation law, **exactly** or **approximately with the approximation disclosed**
   (§10.9);
5. realization evidence — freshness, data-state version, producer attestation (§9, §10.8).

**May never say:** which reducer makes the family what it is · how contributions resolve into a
constituted value · which anchor is constitutive · who the parents are · what the participation is.
**The rule, in one line: nothing whose change would change `Σ(F)`.**

**And it is structural, not a rule to remember.** `family_id` is not derivable from anything in the
mapping, so a mapping edit cannot be a family succession — which is precisely the property P2-02's
four-mappings reproduction currently disproves, and precisely §3.9's test made mechanical.

**Note the sharpest consequence for `firstlight`:** the mapping may say *"the source is finer than
the constitutive anchor."* It may **not** say *"resolve the contributions by sum."* That is formation,
and if formation is unestablished the compile **refuses**. Today that same fact is supplied silently
by `root_evaluator`.

## 11. Showing 10 — consume-or-refuse, never silently omit

A consumer publishes a **profile**: which responsibilities it can represent, which foundation laws it
knows, which movement forms it can carry. Then, over a total record (§8):

| encountered | consumer must |
|---|---|
| a responsibility it cannot represent | **refuse**, with a named category |
| a cited foundation law it does not know | **refuse** — never guess, never drop the family |
| a value outside a known vocabulary | **refuse** |
| an unrecognised key | **refuse** — this is body-key totality, now a consequence of the shape rather than an extra rule |
| `unestablished` on a responsibility it needs | **refuse to admit the movement**, not the publication |
| law it can represent but not execute | **refuse the realization.** §4.1: *"a backend's inability to realize an admitted movement does not remove that movement from analytical law"* |

**Refusal never narrows or edits the law.** `K0_REDUCERS` is the shipped instance of this done right
and is the model to copy: it refuses with a named category rather than emitting a narrowed image.

## 12. Showing 11 — the `firstlight` migration

### 12.1 The governing rule (closure 5)

**Migration evidence is not governing authority.** Legacy member names and `root_evaluator` are
*evidence*; they seed **proposals**. The migration's product is not a publication — it is a set of
**ASSUMED declarations plus a surfaced list of unresolved analytical facts**, using the authoring
mechanism that already exists (`Status.ASSUMED`, `assumed_declaration`), which then require
authoritative establishment.

**Not optimized around a question count.** The three facts v0.3 counted are not a target; what
follows is the honest partition, and it is longer than three.

### 12.2 Evidence — non-authoritative, seeds proposals only

Four member names implying `sum`/`count`/`min`/`max` · a private mapping carrying those four tokens ·
an emitted `FAMILY { count max min sum }` · a `value_type: decimal` on the retired container · a
`root_member: revenue_sum` · six synthetic rows, one per `(store, day)`.

### 12.3 Entailed — derived, never asked

Result domains from cited law + operand domain · self-sufficiency, identity existence and re-entry
for each cited law · **MIN/MAX empty-fiber behaviour** · lineage edges, once formation names parents ·
well-foundedness of the resulting graph.

### 12.4 Unresolved — requires authoritative establishment

| # | fact | why it is not derivable |
|---|---|---|
| 1 | **Revenue's constitutive anchor `I` and its formation structure** | the realized table is `sales_lines`; the declared anchor was `sale_at = (store, day)`; **nothing asserts `sale_at` is unique there** — anchor uniqueness is gate *evidence*, which publication deliberately drops. The fixture's six rows are one per point: **a data fact, not a law** (§3.7). Closure 1 forbids promoting the legacy anchor |
| 2 | **Revenue's formation law** | if `g` is finer than `I`, intake resolution is law. SUM is *evidence* from the mapping, not authority |
| 3 | **Revenue's continuation law** | positive presence required (closure 2). That Revenue is additive is a governed claim, not a consequence of anything published |
| 4 | **Whether a SUM family distinct from Revenue exists at all** | under closure 5, `revenue_sum`'s existence is legacy evidence. §11.5.1/§3.9 identify it with Revenue *"only where identity and participation agree"*, and neither is declared |
| 5 | **Whether COUNT/MIN/MAX targets are governed at all** | closure 5 is explicit: *do not assume they are governed merely because their legacy names imply them* |
| 6 | **Which COUNT**, if COUNT is governed | §11.5.1: `count(I)` and `count(x@I)` are *"distinct targets."* P1-10's seam; the denominator of every mean |
| 7 | **Participation** for each established family | §4.2: participation *"is not automatically the set of surviving physical records"* |
| 8 | **Φ for Revenue** | a choice, not a consequence — flow vs stock |
| 9 | **Domain `𝒜_F` and movement conditions** for each | today **unestablished**, and they publish as `unestablished`. Nothing may be manufactured |
| 10 | **Authority** for each family declaration | §9 |

### 12.5 What the migrated publication looks like once established

```text
universe  sales                       basis events · anchor <I, established>   — ratification intact
anchor    sale_at (store, day)        — unchanged; whether it is I is fact #1
family    <revenue>                   canonical reference "revenue"
                                      formation: primitive intake @ I  · law: <established>
                                      continuation: <established or explicitly none>
                                      participation / Φ: <established>
                                      domain + movement: UNESTABLISHED  (visibly)
                                      authority: <record>
family    <count|min|max ...>         ONLY those established as governed targets
                                      formation: construction over <revenue>.family_id  (= lineage)
                                      continuation: <cited law>
                                      empty fiber: DERIVED, not declared
mapping   bindings keyed by family_id · endpoint sales_lines.amount
                                      grain-correspondence claim · delivery claims
                                      root_evaluator: GONE
```

**`measure` and `root_member` are absent, not relocated** (§5.1). The number of families is an
outcome of establishment, not a migration parameter — it may be fewer than four.

### 12.6 One asset worth spending deliberately

`firstlight`'s producer stage is **not byte-reproducible** and its artifact is *"produced once and
committed, and thereafter immutable"*; every downstream guard reads the committed bytes. So the v1
artifact is not edited — it stays as the historical record, and a **new v2 publication is authored**.
That is the right shape for a migration whose whole point is that the old artifact under-determines
its own meaning.

## 13. Showing 12 — the publication-format-version consequence

**A MAJOR bump, and a hard break with no compatibility path.**

- **Why major:** three kinds retired, one added and required, `family_id` required, and the record
  shape becomes total over the nine responsibilities. Any of those alone breaks a validating reader.
- **The loader already does the right thing:** an unsupported major refuses with a message naming the
  supported one. That is O10 satisfied by a mechanism that already ships.
- **A v2 reader must NOT read v1 — and this is the point, not a courtesy.** A v1 artifact
  **under-determines its own meaning** (P2-02): its family law lives in a private mapping. Reading it
  automatically would require the consumer to *infer* law, which is the exact defect being removed.
  **The format break is the boundary at which under-determined meaning stops being machine-readable
  at all.** v1 artifacts migrate through the proposal-and-establishment path of §12, with a human, or
  they do not migrate.
- **No dual-read, no shim, no optional keys.** An optional key cannot force a consumer that cannot
  represent the law to refuse; a major can.
- **Cost: one publication**, whose regeneration is authoring rather than rebuilding, and no external
  consumers. This is the cheapest this will ever be.

---

## 14. Open — and what authorization would cover

**Open, deliberately:**

1. `family_id` generation (digest / UUID / other).
2. Query-constructed family lifecycle — minted, resolved, or transient; ever serialized.
3. Whether serving an **unratified** family is refused, disclosed, or permitted (§9) — and the
   asymmetry with universes that today's publish gate creates.
4. Whether domain-and-movement folds into `family` or keeps a separate record (§4.1 — folding
   recommended, counter-argument recorded).
5. `firstlight`'s ten unresolved facts (§12.4) — authoring, not architecture, but they gate the
   migration.

**What authorization from this document would cover:** the object set (§4), the identity rules (§5),
the responsibility allocation and derivation rule (§4.2–4.4), law citation and positive presence
(§7), record totality (§8), the authority mechanism's *shape* (§9), the realization contract (§10),
consume-or-refuse (§11), and the format break (§13). **Field spelling, wire encoding, and the
`family_id` mechanism are explicitly not covered** and remain subordinate to the model above.
