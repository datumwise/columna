# Why Columna looks the way it does

*Design notes: where the framework came from. Same register as the What-is pieces — plain
words, loose lines; the manuals are exact.*

---

If you've read the What-is pieces, you might reasonably ask where all of this came from —
who designed the Manifold, the four moods, FrameQL. The honest answer is a little
unusual, and knowing it will change how you evaluate the framework, so it's worth a page.

Most of it wasn't designed. It was written down.

## A useful lens: taste versus no-choice

Here's a distinction that turns out to matter when you look at any framework. At each
fork in a design, you can ask: did the problem decide this, or did someone's taste?
Taste isn't bad — but in our experience it's usually the mark of a shortcut, the place
where working from first principles stopped early and preference filled the gap. When a
design keeps having no choice — when every fork gets settled by the structure of the
problem — you're not looking at an invention anymore. You're looking at something that
was found.

Columna kept failing the taste test, fork after fork. What absence means isn't a design
option; it follows from what kind of population a row is missing from. Whether you can
sort by a column that isn't in the frame isn't a style call; a frame's columns are all
there is. Where a population gets chosen isn't a preference; it's a fact of a
definition, not of a question. The choices that *were* ours are mostly notation — the
`@`, the braces — and notation is a thin layer.

## What analysts already knew

The structure that kept deciding things is one working analysts already carry. Listen to
anyone explaining carefully why a number is wrong: *you averaged at the wrong grain;
those two figures come from different populations; that's a snapshot, you can't sum it
across months; revenue rolls up along region but not along that path.*

None of that is SQL vocabulary. It's a description of structure the data always had:
populations, grains, functional paths between grains, families of quantities with rules
about which operations survive which paths, and missing rows that *mean* something
different in different kinds of population. Analysts have re-derived this structure per
query, per incident, per argument with finance, for decades — because the systems
underneath had nowhere to write it down.

A Manifold is that structure, written down next to the data. This is the same kind of
move Codd made in 1970: the relational model wasn't an invention so much as the
observation that predicate logic was already the right theory of records. The Manifold
observes that the analyst's whiteboard vocabulary was already the right theory of
meaning.

You can see the writing-down happen in the project's own history, in a small way: over
the months, the framework wouldn't keep its name — *Universal Grain Protocol*, then
*Typed Grain Protocol*, then *Entity Column Frame*, then *Data Algebra*, then *Column
Operator Frame*, then finally *Columna*, column algebra. Renaming something five times
is what it looks like to still be finding out what a thing is. The early names read, in
hindsight, like sketches of the same animal from different angles.

## The one real addition: checking

One part of Columna isn't in any analyst's head, and it isn't a modeling concept. Lots
of tools let you write down what data means — metrics files, semantic models, wiki
pages — and they all share a fate: they drift. The description says one thing, the data
grows into another, and nobody notices until a number is wrong in a meeting.

So in Columna, every declared claim is checked against the actual data and carries the
result — verified, corroborated, untestable, or contradicted — and a contradicted claim
cuts its own serving scope until something changes. Written-down meaning plus the
checking is what makes the rest usable; without the checking, a Manifold would just be
better documentation.

Worth noting: over the last decade, many tools independently arrived at pieces of this —
declared metrics in one, grain-awareness in another, governed definitions in a third.
That so many teams landed near the same place is a decent sign the structure was there
to be found. The piece that was generally missing is the checking.

## Why the query language is small

Once the model holds the structure, the query language has very little left to do — and
that's the practical explanation for everything unusual about FrameQL.

Every query language carries whatever knowledge its data model lacks. Tables know
nothing, so SQL has to carry everything: joins, grouping, grain, caveats — yours to
restate correctly in every query. A Manifold already knows the paths, the grains, and
the laws, so a FrameQL query only says the one thing the system can't know: what frame
you want. That's also why there's no way to write a join or a group-by in FrameQL — not
because it's forbidden, but because there's nothing for it to say. Anything operational
you could write would either repeat what the Manifold knows or contradict it. The
language is small because the model is full.

## How to check this yourself

The nice thing about "found, not invented" is that it's checkable against your own
experience. Think of your last few bad-number incidents and ask what they were,
underneath: a wrong grain? two populations mixed? a snapshot summed over time? a rollup
taken along a path it doesn't survive? If your incidents map onto that short list, the
structure was in your data all along — Columna just gives it a place to live and a
court to answer to.

- **[What is a Manifold?](/what-is-manifold)** — the structure, up close.
- **[What is FrameQL?](/what-is-frameql)** — the small language it leaves room for.
- **[The Explorer](/explorer)** — the demo Manifold, checked claims and all.
