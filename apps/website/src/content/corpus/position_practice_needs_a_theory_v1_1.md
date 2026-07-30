# Practice Needs a Firmer Foundation

*A position from datumwise · 2026-07-30*

Every data team knows the failures. The metric that disagreed between two dashboards. The average that was quietly an average of averages. The inventory number somebody summed across a year. The join that doubled revenue and nobody noticed for a quarter. The filter that changed the population and kept the label.

Here is the uncomfortable observation: these are the *same failures*, at every company, in every industry, every year. They have been the same failures for decades. The data changes, the stack changes, the vendors change — the failure shapes do not. A fan-out in 2026 is the fan-out of 1996 wearing a lakehouse.

When an entire field keeps failing in identical shapes, the problem is not discipline. It is not tooling. It is not that your team hasn't read the right blog post. And it is not — this matters — that the field lacks a foundation. It has one: rows, tables, SQL, relational containers. The observation is sharper than absence: **recurring, nameable failure shapes are the symptom of a foundational defect.** The field is not building on nothing. It is building on the wrong thing — a foundation borrowed from a different subject — and the cracks propagate upward into every practice built on top, in the same places, every time. So we did what you do with symptoms that never change: we stopped treating them one at a time and dug down to where they come from.

## The tell

You can see the missing floor in the field's own vocabulary. We have "best practices" for aggregation. Think about what that phrase concedes.

Arithmetic does not have best practices. It has laws. Nobody writes a style guide recommending that you not divide by zero; the operation is undefined, and systems refuse it. A field reaches for "best practices" exactly where it lacks laws — where correctness is folklore, transmitted by apprenticeship, re-learned at each company through each company's own incidents.

That is where analytical data practice stands. Twenty years of dimensional-modeling folklore, trap catalogs, tribal knowledge about grains and fan-outs and stock-versus-flow — real knowledge, hard-won, and *homeless*: not stated as law, not attached to the data itself, not enforceable by any machine, because the foundation underneath has no place to put it. A table has no slot for "this variable may not be summed along time." The knowledge is real; the foundation cannot carry it. So it lives in prose, and every warehouse rebuilds it, and every new hire re-learns it by breaking something.

And every tool built on top inherits the homelessness. Tests check what someone remembered to test. Contracts pin schemas, not meanings. Observability tells you a number moved, not whether it was ever lawful. Semantic layers assign names and definitions — and a definition can be perfectly consistent, centrally governed, and still used to compute something the variable's own nature forbids. None of these tools can refuse a computation *on principle*, because none of them has principles. They have configuration.

**Tooling cannot fix a foundation problem.** If the foundation cannot say what data *is* — what a variable is, where its meaning lives, which transformations preserve that meaning and which destroy it — then no amount of checking machinery on top will produce correctness. You cannot govern what your foundation cannot define.

## What a firmer foundation buys

A theoretical foundation is not academic decoration. It is the difference between arguing and deriving.

With foundations, "can I sum this along time?" stops being a judgment call escalated to the one person who remembers the incident from 2023, and becomes a *typed question with a computable answer* — the way "can I add a string to a socket?" is not a debate in a typed language. The trap folklore compresses into a small set of declarable, checkable laws. The recurring failure shapes stop being war stories and become *theorems about what happens when a specific law is violated* — predictable, preventable, refusable by machine.

That is what a rebuilt foundation buys: not papers, but the ability of ordinary systems to be lawful by construction, and honest when they cannot be.

## The foundations are now written down

This is the part of the position that is an announcement. We dug down to the defect, and we rebuilt from beneath it: we have published the theory of data — the foundation restated from first principles — in two registers, because foundations deserve both.

**The foundations note** — short, for the curious: what data is (a typed value at a typed location), why the column and not the table is the smallest unit with real structure, where meaning attaches, and what makes a transformation lawful. Five pages. [doi.org/10.5281/zenodo.21696104](https://doi.org/10.5281/zenodo.21696104)

**The technical construction** — complete, for the serious: the typed coordinate structure, particles and atoms, universes with their laws of existence, the anchor calculus, the aggregator algebra, and lawful movement defined as a decidable conjunction. Thirty-nine pages, formal throughout. [doi.org/10.5281/zenodo.21707018](https://doi.org/10.5281/zenodo.21707018)

We will not repeat the theory here — that is what the papers are for, and a position piece that restates its own citations is padding. Two sentences to orient you, no more. *A datum is a value of a variable at typed coordinates, and the column — not the table — is the smallest unit of data with internal structure: single values are smaller, but they are simple; structure begins at the column, and so do the laws.* And: *we have been calling tables "structured data" for fifty years — the structure was never in the table.*

One more thing the papers do that this field almost never does: they state their epistemic rank honestly. A working theory, externally corroborated by convergence from four independent traditions, with a named falsifiable edge and a published research program. If it is wrong, it is wrong in checkable ways. That is what foundations look like.

## What changes for practice

Three things, in order of arrival.

**Declaration replaces documentation.** The knowledge in your team's heads — which measures are additive, which axes are blocked, which populations may cross — becomes typed declarations attached to the data, instead of prose attached to a wiki.

**Adjudication replaces trust.** Declarations are tried against the data before anything is served. A hierarchy that isn't functional in the actual rows is not a weaker guarantee; it is an unavailable transport, and the system says so.

**Refusal becomes possible.** This is the deepest change. A system with laws can decline: it can serve, disclose its caveats, ask which of two lawful readings you meant, or refuse — with the violated law named. Today's systems answer everything, because they know nothing. A confident answer to an undefined question is not service. It is the entire problem.

We build [Columna](https://github.com/datumwise/columna) as the working implementation of these foundations — open source, papers and benchmark included. But the position stands independently of the product: **the industry has spent twenty years buying better engines to run on a foundation that cannot state its own laws. The next move is not faster. The next move is firmer.**

Read the foundations. Tell us where they break.

*— datumwise*
