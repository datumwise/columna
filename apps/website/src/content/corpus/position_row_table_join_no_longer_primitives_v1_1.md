# Row, Table, Join: No Longer Primitives

*A position from datumwise · 2026-07-30*

For twenty years, one movement has been quietly taking the database apart — layer by layer, from the bottom up. It never had a manifesto. It has a pattern, and the pattern has now reached the last layer.

## The pattern, four times over

**Storage fell first.** The row-oriented file — data laid out the way transactions arrive — turned out to be a convention, not a necessity. Columnar formats decomposed it: values of one variable, stored together, typed together. Parquet made it the lake's native tongue; Arrow made it the in-memory standard. And the commercial verdict is in — this is no longer an insurgency. Snowflake is columnar under the hood. Databricks is columnar under the hood. Every serious analytical engine of the last fifteen years made the same choice. The war at the storage layer is simply over.

**Execution fell next.** The monolithic engine — parser to optimizer to executor, one vendor, one binary — decomposed into composable parts. DuckDB put a full analytical engine in a process. DataFusion and Velox made execution a library you embed. The engine stopped being a place you send data and became a component you assemble.

**Plans are falling now.** The query plan — always an internal, engine-private data structure — is decomposing into a portable artifact. Substrait standardizes the plan itself: a typed, serialized, engine-neutral description of a computation, produced by one system and executed by another. DataFusion speaks it in both directions; DuckDB consumes and produces it; Ibis compiles to it; and the earliest travelers are already trying to carry *semantics* on it as cargo. The plan stopped being implementation detail and became interchange.

**Transport fell alongside.** ADBC did for result-movement what the rest did for their layers: a standard, columnar, engine-neutral wire.

Four layers, one identical move each time: **something the industry treated as a primitive turned out to be an inheritance — and decomposed into typed, lawful, portable parts native to data itself.** The row-oriented file was not fundamental. The monolithic engine was not fundamental. The private plan was not fundamental. Each decomposition released a wave of capability the old bundle had been suppressing.

So here is the question the movement has been walking toward for twenty years without asking it out loud: *what about the concepts themselves?* The row. The table. The join. Are those bedrock — or are they the last inheritance left standing?

## Where row, table, and join actually come from

Be fair to them first, because they were never arbitrary. The row is an *event* — something happened, several facts arrived together. The table is an *entity ledger* — a collection of things of one kind. The join is a *connection* — this relates to that. Row, table, and join are the physical world's ontology, projected onto data: honest, intuitive, and productive for fifty years precisely because the projection is so natural. We even borrowed the semantics along with the shapes — governing data operations by reasoning about the events, entities, and connections the data depicts, as if the laws of the referents were the laws of the records.

That is the actual finding, and it is deeper than "these are conventions": **data has been living under a borrowed ontology.** And a borrowed ontology can describe data while being unable to govern it — the physical world's concepts carry no aggregation laws, no grain discipline, no account of what absence means. The recurring silent failures of analytics are not accidents of implementation. They are the interest paid on the loan.

## The last layer just moved

We are publishing the answer, and it is the movement's own move, one level deeper: **at the theoretical foundation, row, table, and join are no longer primitives — they are projections of another world's primitives.** Data has its own ontology, autonomous and more natural to it, with meaning defined by rules over abstract structural elements — and it has now been written down.

**The row** is a co-recording: several observations that happened to be captured together. Useful for bookkeeping and write-paths — and carrying no semantic authority. Nothing about a variable's meaning, its lawful aggregations, or its population lives at the row.

**The table** is a recording convention. The industry's own oldest term gives the game away: we have called tables "structured data" for fifty years, but a table's arrangement is *tabulation* — bookkeeping order. The structure that supports identity and law begins one level down, at the column: many observations of one variable, organized by one typed binding. The structure was never in the table.

**The join** — and this one will sting — is not one operation at all. It is the physical world's "connection" projected onto data, and under the projection it bundles seven distinct decisions into one keyword: coordinate matching, support selection, universe crossing, multiplicity propagation, unmatched-point policy, value duplication, frame construction. Inner-versus-outer is a physical choice standing in for semantic decisions that were never separately stated. A join may *implement* a lawful computation, but the physical operator receives no intrinsic semantic authority — which is precisely why the fan-out that doubles your revenue is syntactically indistinguishable from the join that doesn't.

What stands underneath, as data's own primitives: **the column** (the atom — the smallest unit of data with internal structure, a typed function from coordinates to values), **the anchor** (the typed coordinate structure those values live on), **the universe** (a population with a law of existence — the thing that decides what absence means), and **two primitive operations** whose division of labor can be stated in one sentence: *anchor operations determine which particles meet; mappers and reducers determine what their values may become.* Everything the row-and-table world does — filters, roll-ups, windows, allocations, and yes, joins — decomposes into these, the way the monolithic engine decomposed into components. The full construction is published and formal: the foundations note ([doi.org/10.5281/zenodo.21696104](https://doi.org/10.5281/zenodo.21696104)) for the shape of it, the technical paper ([doi.org/10.5281/zenodo.21707018](https://doi.org/10.5281/zenodo.21707018)) for all of it.

## Why this is the movement's own next step

Notice what the columnar movement's success has quietly implied all along. Vectorized execution works *because* a column is semantically homogeneous — one variable, one type, one meaning. The performance the movement won at every layer was the shadow of an ontology it never wrote down: the engines were organized around the column because **the column is what data actually is**, and the machines noticed before the theory did.

The decomposition of storage, execution, plans, and transport was the movement rebuilding *how data moves*. The decomposition of row, table, and join is the same movement arriving at *what data is*. Same pattern: name the convention, find the typed parts underneath, state the laws, let the layer become portable and checkable. The stack the movement built — columnar memory, composable engines, portable plans — is, not coincidentally, the physical layer shaped exactly like the theory's semantic atom. The two were always going to meet.

And one layer has not fallen: **the language.** SQL is the borrowed ontology's grammar — fluent in tables, rows, and joins; silent on grains, populations, and lawful movement, because its parent ontology never had them to say. Every layer beneath it has already decomposed; the language still speaks for a world the stack no longer lives in. We state this at the rank it deserves — an expectation, not an announcement: when a foundation moves, its language eventually follows, and a grammar generated from data's own ontology is what follows it. We build one. The retreat will take years; the direction, we think, is now legible.

Meanwhile the nearest gap is already concrete: the plans now traveling between engines carry *structure* and no *meaning* — a Substrait plan that fans out and double-counts is indistinguishable, on the wire, from one that doesn't. The movement standardized how computations travel before anyone could say what they lawfully mean. That gap — meaning, declared and adjudicated, riding the movement's own rails — is what [Columna](https://github.com/datumwise/columna) exists to close, and the foundations above are what closing it requires.

The movement took the database apart and found, at the bottom, an ontology on loan from another world. Row, table, join: honorably returned to the physical world they came from, still employed in the machinery. Data's own primitives are underneath — and they have laws, which borrowed concepts never could. Laws can be checked.

*— datumwise*
