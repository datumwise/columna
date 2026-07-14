# How these documents relate

**datumwise · draft v0.1 — a map of the corpus**

This project publishes several documents, and they are not interchangeable. Each does one job,
holds itself to one standard of evidence, and deliberately refuses to do the jobs of the others.
That separation is not editorial habit; it is the same discipline the project preaches —
correctness and meaning kept apart so each can be held to its own standard. Here is the whole
corpus, what each piece is for, and the order in which to read it.

## The map: The Silent Failure Atlas

*67 silent failure modes, in 9 families, across six layers — each with its mechanism, its silent
signature, and its detection check.* (Zenodo, DOI 10.5281/zenodo.20762839 · living document,
v1.3)

The Atlas is the reference map of the territory: every known way a query can run cleanly and
return a number that is wrong or misleading, with no error raised. It is compiled from the
failure space outward — independent of any tool's detection capabilities, including ours — and
it is kept deliberately **perspective-free**: it sorts the territory by where failures live and
how they are caught, and argues for nothing. That neutrality is the point. The map exists so
that anyone can grade anyone — any benchmark, any vendor, any architecture, this one included.

The Atlas is also where this project's community lives. It is a versioned, living document that
accepts contributed failure modes, sharper detection checks, and incident citations. If a number
has ever lied to you by omission, the Atlas is where that experience becomes a named, citable,
permanent part of the record. **Bring us the failure modes you've witnessed** — this is the door.

## The theory: why the territory is shaped that way

Two papers explain the map — one from the outside, one from the inside.

**The Silent Seam** asks why these failures are *silent*, and answers sociologically: a question
becomes an answer by crossing boundaries between three authorities — the business user who owns
intent, the analyst who owns translation, the engineer who owns data-truth — and no role can see
both sides of any boundary it crosses. Two structural results follow. First, the
**defense-depth ladder**: every failure is, at best, *inexpressible*, else *certifiable*, else
*disclosable only* — and a solution's worth is exactly the set of failures it moves up the
ladder. Second, the **ceiling**: a grammar can forbid ill-formed answers but cannot legislate
the meaning of a well-formed one, so disclosure is an irreducible floor for one whole stratum of
failure — not a gap better engineering will close. The Seam is diagnosis, not prescription; it
names the shape any cure must take, and the line no cure can cross. (Zenodo, DOI
10.5281/zenodo.20710717)

The Ladder is the public form of the Seam's defense-depth ladder — its five plain fates (can't be
written · refused · asked back · labeled · silent) are the reader's-eye view of the Seam's three
formal rungs (inexpressible · certifiable · disclosable-only). [The Ladder](/ladder)

**The Two Anchors of a Measure** works the heartland of the map formally (the Atlas's family F1,
where the aggregation failures live). It proves the mechanism: a common class of measures is
governed by *two* grains — the output anchor everyone states and the input anchor almost no one
records — gives the exact criterion for when the hidden one is live, and shows why the value
cannot be trusted to carry it (the map from anchor to value has no inverse). Its close derives —
not asserts — the properties any structured capture of the anchors must have: explicit,
structured, verifiable. It names no system. (Zenodo, DOI 10.5281/zenodo.20789318)

The two papers meet in the middle: the Seam's grammar stratum is the region where the Two
Anchors' criteria can be *checked*, and its inference stratum is the region where the Seam's
ceiling holds and only disclosure remains.

## The doctrine: what follows

**Metadata Independence** (the essay) draws the conclusion. Metadata was never one thing: some
of it is load-bearing — change it and you change what is legal or what value results — and some
is communicative. Fused, the two corrupt each other; that fusion is the last fifty years of
analytics, including the layer the industry calls *semantic*. Split them — correctness into a
small, closed, machine-checkable **grammar layer**; meaning set free as pure communication — and
both are finally held to the right standard. Codd separated logical from physical and called it
data independence. This is the sequel: **metadata independence**. One inversion, two liberations.

**The Columna Manifesto** is the same argument compressed to a creed — the version you can read
in four minutes, disagree with by paragraph, and sign. It begins where the whole corpus begins:
*a number owes you its assumptions.*

## The proof: Columna, and the benchmark

Doctrine that cannot run is opinion. **Columna** is the open reference implementation of the
grammar layer (Apache-2.0, [github.com/datumwise/columna](https://github.com/datumwise/columna)).
The name is the thesis — *Columna* stands for **Column Algebra**, because the column, not the
table, is the atom of analytical meaning: a measure over its anchor, something said *of*
something. What the engine serves is the **Manifold** — the dataset as a column set, stripped of
its materialized form. This is why we believe the Manifold is the construct an AI agent should
meet: all of the essence of the dataset, none of the distraction of the arbitrary forms it
happens to be stored in. Over it runs Frame-QL and the four moods — *serve, disclose, clarify,
refuse* — as structured data on one wire contract, identical to a human and to an AI agent. It
exists so no claim above has to be taken on faith:

```
pip install columna-core columna-server
columna-server demo --play
```

Two minutes, and a clarify, a refuse, and a disclose print on your machine as real wire JSON.
That transcript is the argument, executed.

**The benchmark** closes the loop — and the direction of the arrow is the integrity condition of
the whole corpus. The benchmark is graded *against* the Atlas: its coverage of the 67 modes is
published openly, gaps named, including the families our own tooling does not address. **The map
grades the exam; the exam never defines the map.** The same standard applies to us first.

## The entry point

If you read one thing, read **The Grain Gap** — the ninety-second version of the whole problem:
one small table, one ordinary question, three defensible answers, and an AI that picks one
silently and sounds terrific doing it. Everything above is what that ninety seconds looks like
when you take it seriously.

## Three reading paths

**The practitioner.** The Grain Gap → run the demo → the Atlas (find the modes you've met; pin
the ones your stack can't catch) → contribute the one we're missing.

**The skeptic.** The Silent Seam (the diagnosis, no product in sight) → The Two Anchors (the
formal core) → the benchmark and its Atlas grading (the evidence, gaps included) → then, and
only then, the manifesto.

**The convert.** The manifesto → Metadata Independence → the repo → the Atlas, to bring the
failure modes you've witnessed.

## One discipline, throughout

The separation you see in this corpus — a perspective-free map, theory that argues, doctrine
that concludes, an instrument that proves, and a benchmark graded by the map rather than
grading it — is the project's own thesis applied to itself. Keep the layers apart, hold each to
its own standard, and let every belief sit one click from its verification. Nothing here asks to
be believed. All of it asks to be checked.

---

*The Silent Failure Atlas (DOI 10.5281/zenodo.20762839) · The Silent Seam (DOI
10.5281/zenodo.20710717) · The Two Anchors of a Measure (DOI 10.5281/zenodo.20789318) · Silent
Failures in Single-Shot Text-to-SQL: A Blind, Nine-Model Cross-Comparison (DOI
10.5281/zenodo.21349581) · Metadata Independence · The Columna Manifesto · The Grain Gap ·
github.com/datumwise/columna*
