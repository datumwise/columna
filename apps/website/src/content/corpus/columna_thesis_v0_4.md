# The Columna Thesis (v0.5)

<!-- v0.4 → v0.5 (2026-07-14, S4 grammar reframe): §II close reframed — "the algebra of the
substance was never written. This is it." → concedes the fragments (summarizability, semi-additive
handling) in one clause and sharpens the claim to the unification: "…never a grammar … This is that
grammar." Priority claim no longer overclaims against Lenz & Shoshani 1997 et al. Filename kept
(v0_4) to avoid an import churn; version tracked in this header. -->

**A number owes you its assumptions.**

To explain why, we have to start further back than anyone in this industry usually starts — not
at the tool, not at the query language, but at what data *is*.

## I. Data is something about something else

Every datum is a predication: a value said *of* something. The measure is what is said; the
anchor — a set of coordinate dimensions — is what it is said of. A **column** is a measure over
its anchor: the true atom of analytical meaning.

And a table? A table is a container. Form, not substance. Its keys and layouts *hint* at
meaning — but hints are not declarations, and nothing checks them. (Others have circled this
truth before: every key-value pair is a small predication; the object-database movement reached
for substance over form. The instinct is old; the missing piece was the algebra.) This is why fifty years of table operations have been
necessarily *mechanical* — you can only do mechanical things to a container, because a container
has no aboutness to respect. Operations over columns are *substantial*: they must honor what
the column says, and what it is said of.

**Tables are how data is stored. Columns are what data says.**

## II. ColumnA: the algebra of substance

The name is the thesis: **Columna stands for Column Algebra.** The essence of data operation is
columns and their operators — mappers and reducers — composing into expressions. Some
expressions are grammatically well-formed; some are not. The algebra draws that line — and only
that line. Meaning it deliberately leaves free.

What governs it is the *nature* of each column, captured in three anchors: the **V-anchor**
(where its values live), the **M-anchor** (where they leak, and by what mechanism), the
**B-anchor** (which directions of reduction are barred) — plus its family, which binds it to
its kin under a common reducer. From these, legality *follows*. Whether you may sum this, roll
that up, divide these two — not policy, not convention, not a style guide: **theorems.**

Relational algebra was the algebra of containers — select, project, join, closed over tables,
indifferent to meaning. The substance side got theorems — summarizability said when a rollup is
lawful; semi-additive handling shipped in tools — but never a grammar: one closed algebra in which
legality follows and refusal is an answer. This is that grammar.

## III. The Manifold: the dataset without its costume

Strip a dataset of its arbitrary materialized form — the particular tables someone once chose,
the joins those choices force, the layout accidents frozen into schemas — and what remains is
the **Manifold**: the column set itself, with everything essential about each column and nothing
incidental. All of the substance, none of the packaging.

This is why we believe the Manifold is the construct an AI agent should meet. Hand a model the
tables and you hand it the distractions: containers to misread, joins to fan out, layouts to
mistake for meaning. Hand it the Manifold and it faces only the essence — what each column says,
of what, and how it may lawfully be treated. A mathematician's manifold is defined without
reference to any embedding space; so is ours. The tables were only ever one chart on it.

## IV. The liberation: metadata independence

Metadata was never one thing. It is two kinds, fused: the load-bearing kind that governs what
operations are legal and what value results, and the communicative kind that helps a person (or
a model) understand. The three anchors capture the first kind completely — the operational
governance layer — and in doing so set the second kind free. But because the load-bearing kind
historically had no home, the industry forced *names* to carry it — and then built a
governance regime to police the names, and called it the semantic layer. **It was never
semantic.** It was correctness wearing meaning's clothes: semantics conscripted into structural
duty, and therefore frozen.

Language solved this before we were born: grammar decides well-formedness independent of meaning
— "colorless green ideas sleep furiously" is perfect grammar and perfect nonsense — and that
autonomy is what makes language both checkable and infinitely expressive. Data deserves the same
constitution. Put correctness in the **grammar layer** — the algebra above, small, closed,
machine-checkable. The moment it has a home, meaning is demobilized: names become pure
communication, free to be colloquial, translated, plural, generated — because nothing
operational rides on a string anymore.

Codd separated logical from physical and called it data independence. We claim the sequel:
**metadata independence** — meaning separated from correctness so each can finally do its job.
Fused, they corrupt each other; that fusion is the last fifty years. **One inversion, two
liberations.**

## V. The stakes: the analyst who never hesitates

For fifty years the two layers lived fused and scattered — some in schema structure, some in
column names, some in documentation, and the decisive remainder in the analyst's mind. The
argument between human analysts was our only safety mechanism. That
mechanism is gone. The AI analyst answers instantly, confidently, singularly. **The debt came
due the day the analyst stopped being human.**

A language model is a semantic engine — magnificent at meaning, constitutionally incapable of
guaranteeing correctness. Hand it today's fused metadata and its greatest strength becomes its
signature failure: it reads `avg_order_value` and *confidently means something by it*. Split the
layers and the model is finally in its element — living entirely in semantics while every
operation it proposes is adjudicated by a grammar it cannot touch. Hallucination, injection,
drift: they can corrupt only the semantic layer. **The grammar layer is the blast wall.** The
model proposes; the grammar disposes; the human decides among genuine alternatives. And the
system's answers come in four moods — **serve, disclose, clarify, refuse** — because "it
depends," said precisely, is often the most correct answer there is.

## VI. What we learned about ourselves

Vigilance fails; structure holds. We made the silent-binding mistake ourselves — twice — *after
publishing the theory that names it.* The third time, our own system caught us: asked for a
metric that didn't exist, it refused to guess. The test was wrong; the model was right. The
defense must be architectural, because attention is demonstrably not enough. Even ours.

## VII. The practice, and the proof

The discipline needs no product. Declare your anchors. Name your populations. Mark your
materiality. Refuse, out loud, what your data cannot answer — any stack, starting today.

**Columna is our proof that the discipline can be made executable — the reference
implementation of the algebra, open, so no one has to take our word for anything.**

If a number has ever lied to you by omission, this movement is yours.

*Sign it. Practice it. Bring us the failure modes you've witnessed.*
