# Referee report — *The Theory of Data*, Version 8.0 publication manuscript, revision v0.12

**Claude, at Huayin's direction, 2026-09-28.** Subject:
`attachments/2b0e0f13_theory_of_data_v8_publication_manuscript_v0_12_full.md` (2,023 lines) with
`attachments/ae4b7a30_tod_v8_v0_12_revision_note.md`. Supersedes
`tod_v8_publication_manuscript_referee_report_v0_3.md` (revision v0.9). v0.10 and v0.11 were not
circulated for review; this report reads v0.12 against v0.9.

**Standing.** Adversarial read of the revision. **No implementation. No changes to schemas, Core, Platform,
Manifold, MEL, Frame-QL or publications. The manuscript is not rewritten.**

---

## 1. Verdict

> **All three v0.9 findings are resolved, two of them by a better repair than I proposed. The architecture
> has also been simplified in the right direction: value closure is no longer a fifth criterion bolted onto
> four obligations — it *is* the third obligation. That is the correct collapse.**
>
> **But the collapse was not carried through the rest of the paper. The concept lost its name in Chapter 3
> and kept it in Chapters 6, 7 and the endnotes, so `value closure` is now used as established vocabulary
> and never defined. And §3.5 lost the three sentences that were the only place the paper said *why* any
> particular quantity is an expression.**

**No foundational blocker.** Two findings and one editorial note. Both findings are artifacts of an
incomplete rename, not disagreements about the theory.

---

## 2. The three v0.9 findings are resolved

### 2.1 Non-minimality restored, `smallest` withdrawn — both halves, exactly

§5.3 now carries the result verbatim in the right place:

> *"Sufficiency is target-relative. A basis need not be **minimal, necessary, recoverable from every other
> basis**, or materially available whenever another lawful route establishes the same expression."*

And §9.2 restates it in the continuity chapter, which is where a reader checking against v7.1 will look:
*"A sufficient basis remains target-relative, nonunique, and potentially nonminimal."* **Stating it twice is
better than restoring it once** — the v7.1 reader and the §7.4 alternative-bases reader are different readers.

The converse claim is gone. §7.7's *"the **smallest** authoritative family state"* is now
*"the **canonical authoritative** family state is its root measure."* That was the recommended word.

### 2.2 The value-closure loophole is closed, and closed harder than I asked

I asked for the elaboration to be aligned to the definition. The revision deleted the elaboration and replaced
it with an explicit whitelist **and an explicit blacklist**:

> *"The permitted fixed structure includes family law, anchor geometry, constitutive order where applicable,
> and fixed identity-bearing parameters. **It does not include additional per-instance counts, sketches,
> moments, pairings, witnesses, or other analytical values hidden outside the family measure.**"*

`governed family context` and `other family-specific state` — the two undefined phrases that carried the
loophole — have zero occurrences. **Naming counts, sketches and moments in the exclusion is the right move**,
because those are precisely the objects §3.5 reclassifies, so the reader cannot reach the forbidden reading by
charitable interpretation.

### 2.3 The structure/representation gap is dissolved rather than patched

I asked for a sentence saying MEAN meets the four obligations and fails only value closure. **The revision
instead makes that sentence unnecessary by merging the criterion into the obligation:** §3.1's third
obligation, *lawful derivability*, now **is** the closure property —

> *"The source family measure, together with fixed governed family structure, must contain the analytical
> information required by the admitted continuation. The family law cannot depend on hidden instance-varying
> analytical state that is not part of the family value."*
>
> *"The third obligation is the closure property at the heart of the family concept."*

**This is a real simplification and it should be kept.** v0.9 had four obligations defining family *structure*
plus a separate criterion selecting the family's *representation*, and the relationship between the two was
never stated. Four obligations, one of which is closure, has no such seam. §3.7's promotion gate follows
correctly: *"A new family can be constituted only when the chosen family value itself satisfies the four family
obligations above."*

**See finding 4.2 — the merge is right, but the reason MEAN fails obligation three went out with it.**

---

## 3. What else the revision achieves

**§3.2 is now its own section, and the root doctrine is stronger for it.** Splitting the root out of the family
definition lets it carry its own load-bearing sentence, which v0.9 did not have:

> *"The root must be sufficient for every family relation the constitution claims from it. … A coarser
> materialization that has already discarded information required by another claimed edge **cannot simply be
> renamed as the family root**."*

That closes a gap I did not flag and should have: v0.9 established that \(R_F\) need not be point-level but
never said what stops an implementer from declaring whatever they stored first to be the root. The boxed
\(\text{root anchor}\neq\text{whatever grain happened to be stored first}\) is the answer.

**§9.2 now explains the reclassification as continuity rather than announcing it.** The paragraph naming what
v7.1 permitted and what v8 narrows — *"Version 7.1 … allowed a durable derived measure family to be justified
either by self-sufficient continuation **or** by a sufficient-state basis. Version 8 narrows measure family to
the continuation-bearing case"* — is the single most useful paragraph added in this revision, because the
narrowing is the one change a v7.1 reader will experience as a loss. Pairing it with
*"without making them less governed"* and the four-item reclassification list is the right defusal.

**The Measure Algebra relationship is now stated as a renaming, not a resemblance:** *"What that paper called
**sufficient state** is called **continuation state** here."* That is a stronger and more checkable claim than
v0.9's citation, and it is correct against MA v1.0.

**Nothing load-bearing was lost in the 13k-byte contraction, and I checked the usual casualties.**
Proposition 6.2 keeps **both** branches in the statement (*"in the semigroup case without an identity, staged
and direct continuation agree on every finite nonempty contributing fiber"*), so MIN/MAX still have a theorem;
MIN and MAX remain **family** values in §3.4 rather than being exiled to expressions; the cross-universe
**carve** sentence survives in §8.1; the moment families of §5.4 survive as the constructive answer to §5.5's
pairing rule; §7.7 keeps root freshness, evidence validity and cross-family compatibility fenced off as
separate obligations. Proposition 6.2's scope note is intact.

**§7.7's materialization claim is narrower than v0.9's and more defensible.** v0.9 claimed intra-family
stale-derived-value inconsistency was *"eliminated by construction."* v0.12 permits a non-root cache and puts
an obligation on it — *"must remain derivationally consistent with the root"* — and claims only that the
architecture *"removes independently authoritative stale expression values from the semantic core."* **That is
the true claim.** The weaker statement is the correct one and it was not weakened under pressure from me.

---

## 4. Findings

### 4.1 ⚡ `value closure` is used in three places and defined in none

The concept is named **five different ways** across the manuscript, and the name the later chapters use is the
one Chapter 3 dropped.

| where | what it is called |
|---|---|
| Abstract | *"Its defining **closure property**"* |
| §3.1 | *"the **closure property** at the heart of the family concept"*; *"the **closure requirement**"* |
| §6.2, §6.4, §7.7 | ***"value closure"*** — used as an established term |
| Endnote 4 | *"**Family closure** and materialization"* |

**`value closure` / `value-closed` fell from 41 occurrences in v0.9 to 3 in v0.12 — and all 3 survivors are
back-references.** §7.7 opens *"**Value closure** gives family materialization a natural boundary."* §6.4's
scope note says the proposition *"establishes the canonical algebraic region of **value closure**."* §6.2 says
*"For **value closure**, the important question is whether the witness…"* A reader arriving at §6.2 has met the
property, in a box, under a different name, ninety sections earlier, and has never been told these are the same
thing.

This is a **merge artifact, not a disagreement**: Chapter 3 was rewritten to fold the criterion into obligation
three and the downstream references were not swept. It is the highest-value fix in this report because it costs
one decision and one pass.

**Repair.** Pick the name and sweep. If the term is kept, name it once in §3.1 — *"Call this **value
closure**"* immediately after the box — and leave §6.2, §6.4, §7.7 and endnote 4 alone. If it is retired in
favour of *the third obligation*, then those four sites must be rewritten. **Keeping it is better**: the
property is referred to often enough in Chapters 6 and 7 that *"the third obligation"* would be a worse read,
and §9.3 already treats *continuation-bearing family values* as a nameable thing.

### 4.2 §3.5 now classifies nine quantities as expressions and gives a reason for none of them

v0.9 gave the reason case by case, in three sentences:

> *"The scalar mean is not continuation-complete: materialized means at finer anchors do not generally
> determine the mean at a coarser anchor. SUM and COUNT do."*
> *"The scalar cardinality does not retain **overlap** information; the distinct subset does."*
> *"The estimate does not retain sketch-**merge capability**; the sketch does."*

**All three are gone.** `merge capab` and the reclassifying sense of `overlap` have zero occurrences in v0.12;
`continuation-complete` fell from 5 to 1, and the survivor is the LAST witness discussion in §6.2. In their
place §3.5 lists nine quantities —

> *"`mean_revenue_order`; Average Order Value; conversion rate; margin percentage; exact unique customers;
> approximate unique customers; variance; covariance; correlation"*

— followed by *"without pretending that their displayed values are continuation-bearing family state."*
**That is the conclusion with the argument removed.** The section is now shorter than its own list.

This matters more than a lost illustration, for two reasons.

**First, the reader cannot check the classification.** The manuscript's central architectural claim is that
value closure *explains* rather than *stipulates* why these quantities are not families. As written, §3.5
stipulates. The reason is recoverable — §3.1's blacklist names *counts* and *sketches* as inadmissible
per-instance state, so a reader who holds that sentence in mind through §3.5 can reconstruct why a scalar mean
fails — but **that is an inference the paper used to make for them, in one sentence each.**

**Second, my v0.9 finding 4.3 is still open in its new form.** Under the merged architecture the interesting
claim is sharper than before: **MEAN satisfies obligations one, two and four and fails exactly obligation
three.** One could declare a MEAN family with admitted measures at Day and Month, law-bearing relations,
and coherence of alternative paths — the failure is precise and local. Saying so is what demonstrates that
obligation three is doing independent work rather than restating the other three. **The paper still never says
it, and now there is no neighbouring sentence from which a reader could assemble it.**

**Repair.** Restore the three per-case sentences to §3.5 — they are three sentences and they were already
written — and add one more: that MEAN can meet the first, second and fourth obligations and fails the third.
The nine-item list can stay; it is useful as a scope statement once something in the section has been argued.

### 4.3 §9.3's compact form enumerates six family properties where §3.1 gives four obligations

§3.7 gates promotion on *"the **four** family obligations above."* §9.3 then lists six bullets:

> *"a family-relative root \(R_F\); admitted measures \(F@A\); law-bearing family relations;
> **continuation-bearing family values**; lawful derivability; path coherence."*

**`continuation-bearing family values` and `lawful derivability` appear as two bullets, and §3.1 says they are
one obligation.** This is the same seam as 4.1 — the compact form still reflects the pre-merge shape, where
closure sat beside the obligations rather than inside one. A reader who reads §9.3 first (many will; it is the
summary) will arrive at §3.7's *"four"* having counted six.

**Repair.** Editorial, and it follows from whatever is decided in 4.1: either merge the two bullets, or split
them and say in §3.1 that the third obligation has two readings. Merging is consistent with the rest of the
revision. The root bullet is correctly separate — §3.2 is its own section and the root is not an obligation.

---

## 5. Theorem audit

**Proposition 6.1** unchanged; premises each used, conclusion scoped to the region.
**Proposition 6.2** both branches survive in the statement; proof unchanged; the fences (*"does not turn every
projection into a family edge, treat changed participation as harmless staging, or establish interchange
between different laws"*) are intact.
**Proposition 6.3** retargeted to \(E@A\) and fenced as in v0.9.

**No proposition is invoked more broadly than it is proved.** The one term used beyond where it is established
is `value closure`, and that is a definition gap (4.1), not an inference gap — §6.4's scope note correctly
limits the proposition to *"the canonical algebraic region."*

---

## 6. Additions to the frozen list

- **Closure as the third family obligation** rather than a separate representational criterion. This supersedes
  the four-obligations-plus-value-closure structure frozen last time.
- **§3.1's explicit exclusion list** — counts, sketches, moments, pairings, witnesses are not fixed family
  structure.
- **§3.2's root-sufficiency rule**: the root must be sufficient for every relation claimed from it, and a
  coarser stored grain cannot be renamed the root.
- **§9.2's continuity statement**: v7.1 permitted family standing by self-sufficient continuation *or* by
  sufficient-state basis; v8 keeps only the first, and MA v1.0's *sufficient state* is v8's *continuation
  state*.

---

## 7. Summary

**Three findings resolved, and two of them by the better repair.** The merge of value closure into the third
obligation is the right architecture and is the most important thing in this revision; §3.2's root-sufficiency
rule closes a gap I missed; §9.2 now explains the narrowing to a v7.1 reader instead of announcing it.

**Both remaining findings are the same unfinished sweep.** Chapter 3 was rewritten and Chapters 6, 7, 9 and the
endnotes were not brought along.

**Name value closure once in §3.1 and leave the downstream references standing.** **Restore §3.5's three
per-case sentences and add that MEAN fails exactly the third obligation.** **Reconcile §9.3's six bullets with
§3.7's four.**

Nothing else stands between this manuscript and publication revision.
