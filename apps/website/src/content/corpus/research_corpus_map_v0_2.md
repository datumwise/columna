# The research corpus

*how these documents relate*

**v0.3 · August 2026**

---

Everything below is published, versioned, and DOI'd. Nothing here asks to be believed: every claim is one click from the document that carries it, and every demo on this site is generated at build time from the shipped package. This page is the map.

### The root

***The Theory of Data*** — Version 4.0 ([doi.org/10.5281/zenodo.21774032](https://doi.org/10.5281/zenodo.21774032)), the canonical manuscript (Version 3.1 remains in the version chain) — states what everything else assumes: what data *is*, where meaning attaches, and what makes a transformation lawful. Its vocabulary is the corpus's vocabulary. The measure — `revenue` — is the governed family. A column realizes one **member** of it: a governed **series**, the family at one grain. Transaction revenue and customer-month revenue are two members of one measure. And **closure** is the question every calculation must answer: did this produce another member, synthesize a new measure, or produce a number with no governed identity at all? The original foundations note ([10.5281/zenodo.21696104](https://doi.org/10.5281/zenodo.21696104)) remains as the origin record.

### The kernel: what is proved

Doctrine that cannot run is opinion. Doctrine that cannot be checked is also opinion. ***A Contract Calculus for Governed Analytical Transformation*** ([10.5281/zenodo.21752373](https://doi.org/10.5281/zenodo.21752373)), with its technical supplement collection ([10.5281/zenodo.21752681](https://doi.org/10.5281/zenodo.21752681)), turns a growing fragment of the theory's laws into machine-checkable theorems. Within the fragments, "this number is deterministic, plausible, and not the thing it claims to be" is a verdict, not a review comment. The theory and the engine are checked against each other, both ways: obligations the theory derives about the mechanism are verified in the shipped code, not assumed.

### The bridges

Two introductions, written to be read before anything formal. ***The Theory of Data: An Introduction*** ([10.5281/zenodo.21763395](https://doi.org/10.5281/zenodo.21763395)) — also here on the site: [What is the Theory of Data?](/learn/what-is-the-theory-of-data). ***Frame-QL: An Introduction*** ([10.5281/zenodo.21763321](https://doi.org/10.5281/zenodo.21763321)) — also here: [the full introduction](/learn/frameql-an-introduction), the middle rung between [What is FrameQL](/what-is-frameql) and the Manual.

### The positions

Every stance, with its site edition and its citable paper edition. ***Analytical Practice Needs a Firmer Foundation*** ([10.5281/zenodo.21763451](https://doi.org/10.5281/zenodo.21763451) · [site edition](/positions/practice-needs-a-theory)) — the failures are symptoms; the defect is foundational. ***Row, Table, and Join Are Not the Foundations of Analytical Meaning*** ([10.5281/zenodo.21763488](https://doi.org/10.5281/zenodo.21763488) · site edition: [No Longer Primitives](/positions/row-table-join-no-longer-primitives)) — the machines noticed before the theory did. ***Never Let Your Agent Touch the Database*** ([10.5281/zenodo.21765252](https://doi.org/10.5281/zenodo.21765252) · [site edition](/positions/never-let-your-agent-touch-the-database)) — the intent boundary. ***The Two Great Sources of Silent Analytical Failure*** ([10.5281/zenodo.21553379](https://doi.org/10.5281/zenodo.21553379) · [site edition](/positions/the-two-great-sources-of-silent-analytical-failure)).

### The ripples

The theory leaves home. Each ripple paper walks into an established field and re-derives its foundations under governed objects. First: ***Missingness Has a Universe*** ([10.5281/zenodo.21760508](https://doi.org/10.5281/zenodo.21760508)) — missingness is defined only after an eligible universe point exists, and it is a compositional law that must transform with the member. Next in the series: the frame paper (in review), and a statistics-and-machine-learning companion. The series has one shape: the field's hardest folklore, stated as law, with the checkable part checked.

### The instruments

The working tools and the earlier evidence. ***The Silent Failure Atlas*** ([10.5281/zenodo.20762839](https://doi.org/10.5281/zenodo.20762839)) — the catalog, and the door: contributions welcome. ***The Silent Seam*** ([10.5281/zenodo.20710717](https://doi.org/10.5281/zenodo.20710717)). ***The Two Anchors of a Measure*** ([10.5281/zenodo.20789318](https://doi.org/10.5281/zenodo.20789318)) — the precursor of the Manual's Two Anchors law. The [text-to-SQL benchmark](https://doi.org/10.5281/zenodo.21349581). ***Multi-Universe Processing*** ([10.5281/zenodo.21543584](https://doi.org/10.5281/zenodo.21543584)). ***The Open Planner*** ([10.5281/zenodo.21632723](https://doi.org/10.5281/zenodo.21632723)).

### The engine is the proof

[Columna](https://github.com/datumwise/columna) is the executable form of all of the above — the Manifold, FrameQL, and an engine that serves nothing the model can't defend, in four moods, on one wire. The Frame-QL Manual (Second Edition) ships with the repository, pinned to the release, every example verified against the running parser. The discipline needs no product; Columna is our proof that it can be made executable.

### Four ways in

**The skeptic:** [the Atlas](/atlas) → [the benchmark](https://doi.org/10.5281/zenodo.21349581) → [run the demo](/install) — see the failures, see them measured, watch the refusal print on your machine.
**The practitioner:** [the case](/case) → [Learn](/learn) → the manuals — a working warehouse end to end.
**The researcher:** [the Theory, V4.0](https://doi.org/10.5281/zenodo.21774032) → [the Calculus](https://doi.org/10.5281/zenodo.21752373) → [the ripples](https://doi.org/10.5281/zenodo.21760508) — definitions, theorems, and the program.
**The agent-builder:** [Never Let Your Agent Touch the Database](/positions/never-let-your-agent-touch-the-database) → [Frame-QL: An Introduction](/learn/frameql-an-introduction) → the wire over MCP.

**✦ New to the corpus? Ask your own AI to walk you through it.**

```
datumwise publishes an open research corpus about governed analytical data. The root is "The Theory
of Data" v4.0 (doi:10.5281/zenodo.21774032): a measure is a governed family, a column realizes one
member of it (a governed series), and "closure" asks whether a calculation produced a governed object
at all. A proved
kernel (doi:10.5281/zenodo.21752373) makes a fragment of the laws machine-checkable theorems. The open-
source engine Columna (github.com/datumwise/columna) is the executable form: four answer moods — serve,
disclose, clarify, refuse — on one wire. Explain this project to me, then help me pick a first paper
to read based on what I do.
```

---

**Note, 2026-08-03.** The theory's vocabulary moved again, and this time the move retired a word. *The Theory of Data*, Version 4.0 ([10.5281/zenodo.21774032](https://doi.org/10.5281/zenodo.21774032)) replaces *atom* with **measure** — the governed family — because the old word named smallestness while the object is a family with laws. A column realizes a **member**: a governed **series**. The map is unchanged; a family is constituted by its law, and so, it turns out, is a vocabulary.
