# Building on the Data World

## How Columna Uses an Independent Data Ontology to Govern Analytics

### Datumwise Architecture Note

*The Three Worlds of Analytics* establishes a general distinction among
the **Business World** of domain meaning and intent, the **Data World**
of governed data identity and law, and the **Material Data World** of
representation, storage, mutation, and computation.

This note begins downstream of that foundation. It asks what kind of
architecture becomes possible when a system takes the independent Data
World seriously.

Columna did not create the Data World. The Data World exists
independently. The Theory of Data describes its ontology and governing
laws. Because analytics must cross between this world and its two
neighbors, that independent jurisdiction creates an architectural
opportunity.

Columna takes advantage of it.

It gives a particular Data World explicit governed form through
**Manifold**, gives that world a ToD-native declarative and
representational language through **Frame-QL**, and governs the
crossings by which business meaning enters and leaves the Data World and
by which governed data is materially realized and returned.

Every analytical architecture must deal with these crossings somehow.
Columna's distinctive move is to make the middle jurisdiction explicit
enough that neither neighboring world needs to carry authority that
belongs to the Data World.

> **Use the independent ontology of the Data World to make both
> crossings explicit and governable.**

## 1. The architecture starts downstream of the ontology

The causal order matters:

> **Data World → Theory of Data → governance problem → architecture**

not:

> architecture → invented middle layer.

Theory of Data is the category-level account of the Data World. Columna
is one engineered consequence of taking that account seriously.

Nothing about this opportunity is proprietary to Columna. Another
architecture could build a different data constitution, language,
realization protocol, and serving machinery. The difficulty is
structural rather than insurmountable: the middle jurisdiction must be
rich enough to preserve data identity, population, reduction, movement,
support and absence, and lawful derivation, and the crossings must
preserve those distinctions rather than translate them away.

## 2. Manifold: the governed ontology of your data

A **Manifold** is the governed data ontology of a particular business or
domain under the Theory of Data.

It is the ontological manifestation of that business's **data**, not the
ontology of the business itself.

Business ontology may define concepts such as *customer*, *open store*,
*recognized revenue*, or *product hierarchy*. A Manifold governs the
Data World objects constituted from such meaning: measures, families,
anchors, universes, lineage, reducer law, and conceptual mappings among
governed data objects.

Reducer identity belongs here. If a governed measure is a sum, last
value, maximum, or another governed reduction, that is a fact about the
data object. **How** a particular backend realizes that reducer belongs
to material realization.

A semantic system may legitimately declare `SUM(amount)`, a metric
formula, or a join relationship. Those declarations can be meaningful
and computationally useful. They do not by themselves establish reducer
closure, admissible re-reduction, movement preservation, data identity,
or consistency across derivation paths.

The distinction is not **semantics versus computation**. It is
**business/domain authority versus data-law authority**.

By Columna's design, conceptual mappings among Data World objects may
belong in the Manifold; bindings from those objects to tables, files,
APIs, columns, or other material sources belong to **material
realization**.

## 3. Frame-QL: a ToD-native language of the Data World

Frame-QL is **a ToD-native declarative and representational language of
the Data World**.

It is declarative because it states **what** governed data object or
result is intended rather than **how** a material backend must compute
it.

It is representational because it expresses Data World concepts,
relationships, anchors, and domain knowledge in a form tied to a
governed Manifold.

A legal Frame-QL expression is intended to identify its governed object
**relative to a given Manifold**. The Manifold supplies the ontology;
Frame-QL supplies a language for representing and requesting objects in
that ontology.

Frame-QL can therefore participate on both sides of the architecture
without becoming either crossing. At the upper crossing, a resolved
business intent can be represented as a precise Data World request. At
the lower crossing, that same request is what realization machinery must
honor.

Frame-QL does not itself interpret the user's business intent, and it
does not itself prescribe the backend program. It is the
representational hinge between those acts.

## 4. Where governing authority comes from

Making the Data World explicit does not make every declaration inside it
authoritative.

Business meanings, data identities, reducer laws, support requirements,
permissions, material bindings, and serving rules acquire governing
standing through accountable declaration and ratification.

The accountable parties may differ by object and jurisdiction. Domain
experts may establish business meaning. Data and analytical authorities
may ratify measures, populations, laws, and derivations. Engineering
authorities may ratify material bindings and connector procedures.
Governance authorities may ratify permissions and serving rules.

AI can assist this work. It can harvest candidate definitions, propose a
measure, compare alternatives, inspect mappings, generate tests, and
surface inconsistencies.

It cannot give its own proposal governing authority merely by generating
it.

> **The agent may assist authoring. Accountable ratification supplies
> authority.**

This is not administrative decoration around the architecture. It is how
authority enters the governed world without being minted by the same
agent that will later rely on it.

## 5. Two governed crossings

The independent Data World creates two natural interfaces.

### Business World ⇄ Data World

The upper crossing governs **interpretation and constitution** in one
direction and **claim and use** in the other.

Business meaning may participate in constituting a governed data object.
It does not automatically become data law. A governed data result may
later become a business statement, decision input, interpretation, or
action. Validity as a Data World result does not automatically confer
unlimited standing for every business use.

### Data World ⇄ Material Data World

The lower crossing governs **realization** in one direction and
**observation / governed return** in the other.

A governed data request must be realized through material systems.
Material values and execution facts must then return in a way that
preserves their relationship to the governed request.

The lower crossing is not Frame-QL-to-SQL translation. A DuckDB
realization may use SQL; a Polars or future backend need not. The design
test is substitutability:

> **Can the material backend change while the Data World request retains
> its meaning and identity?**

## 6. The two Analytical Governance gaps sit over the crossings

### Intent gap: Business World ⇄ Data World

The user begins with business intent. The governance problem is whether
that intent has been correctly represented as the intended Data World
object.

Theory of Data supplies the distinctions needed to recognize the object.
Frame-QL gives the resolved object a declarative and representational
form relative to a Manifold.

Natural language can remain ambiguous. SQL is a material instruction
language and can be perfectly legal while embodying the wrong analytical
interpretation.

Frame-QL does not guarantee that a person or model understood the user
correctly. Its role begins after that interpretive act: once the
intended Data World object has been resolved, the request language need
not introduce another ambiguity about what governed object is being
requested.

### Servability gap: primarily Data World ⇄ Material Data World

The servability gap lies **primarily** over the lower crossing.

The Data World tells us what object is requested and what that object
requires. The Material Data World supplies observations, records, and
mechanical realization. The lower crossing exposes whether material
realization supplies the support needed by the governed request.

Servability itself is the Analytical Governance judgment, not the
interface. Its protected factorization includes both **Support
Sufficient** and **Analytically Established**. The latter depends on
Data World law as well as facts exposed by material realization.

Typical lower-crossing failures include an incomplete population,
untyped absence, an unavailable material relation, or successful
material execution that still fails to establish the requested data
object.

## 7. Worked upper crossing: *open store*

Suppose Operations defines an *open store* as a store operational under
policy P on a given day.

That definition belongs to the Business World. Through constitution, it
can participate in establishing a governed daily open-store universe in
the Data World.

A governed request can then ask for revenue at store-by-day grain:

> `SELECT revenue AT {store*cal.day}`

Only specified authority crosses. The business definition supplies what
qualifies as *open*. It does not, merely by crossing, establish revenue
support, reducer law, data identity for every derived object, or the
meaning of a missing revenue observation.

If Operations later changes the meaning of *open*, the architecture does
not block the change. The changed meaning must be constituted again. The
interface prevents **silent propagation**, not legitimate revision.

## 8. Worked lower crossing: realization and governed return

Take the governed request:

> `SELECT revenue AT {store*cal.day}`

Frame-QL represents the requested Data World object relative to its
Manifold.

Columna **adjudicates** what is lawful in Data World terms and **plans**
how the request will be realized. These are different acts: adjudication
concerns the governed object and its laws; planning chooses a
realization strategy.

The backend is instructed to realize the requested measure **at its
governed grain**. Columna does not ask the backend for arbitrary rows
and then let row mechanics redefine the measure. With DuckDB,
backend-specific machinery may use SQL to extract the governed member.
Another backend may use a different mechanism.

The return direction matters just as much.

The architecture requires an owned return contract. In the current
Columna implementation, the **connector/backend delivery seam** supplies
the backend-specific contract: the connector procedure warrants how
returned material values correspond to the issued governed request. A
richer shared serving-result model is a separate concern and need not be
assumed here.

Richer result envelopes can make identity, support, absence, conditions,
and provenance more explicit, but governed return does not begin only
when such an envelope exists.

Successful material execution establishes that the backend procedure ran
successfully. It does not by itself establish that the requested result
is servable.

## 9. The 47 / 48 / 50 case

Suppose **50 stores exist. 48 were open yesterday. Revenue observations
arrived for 47.**

The Business World can establish what *open store* means and which
stores qualify. The Material Data World can establish which revenue
observations are present. The Data World identifies the requested
object: average revenue over the governed open-store population.

Forty-seven material observations do not automatically redefine a
forty-eight-store governed population. The business definition of *open*
does not automatically settle whether the requested measure has
sufficient material support.

The servability decision must use facts from both sides without allowing
either side to usurp the Data World's identity and requirements.

Current implementation does not yet enforce every declared-domain
support case described by this example; that remains an open
implementation obligation. The architectural requirement is the point
here: material row presence must not silently redefine the governed
population.

## 10. Controlled freedom and bounded change

Making the Data World independent does not freeze its neighbors. It
gives each world a clearer domain of change.

Above it, business semantics can be departmental, project-specific,
product-specific, embedded, federated, and evolving. Columna does not
require one enterprise-wide semantic ontology before analytical
governance can begin.

A department may change semantic tooling without rewriting data law. If
the **meaning itself** changes, affected data objects may require
reconstitution.

Below it, material realization can evolve according to engineering
needs. Databases, dataframe systems, storage formats, query engines, and
execution strategies can change as long as the realization contract
preserves the governed request.

If Finance changes *recognized revenue*, that is a Business World
change. If the execution substrate changes, that is a Material Data
World change. Neither should silently rewrite Data World identity or
law.

Shared analytical rigor therefore does not require semantic monoculture,
and substrate independence is more than portability. Both follow from
keeping authority in the jurisdiction where it belongs.

## 11. Smaller failure domains

Separation also makes different classes of drift observable rather than
collapsing them into one generic statement that "the data changed."

A change in governed constitution, a contradiction or adjudication
failure in the Data World, and a change or integrity mismatch in
material realization are different events. Columna already carries
machinery that distinguishes important instances of these classes and
can fail closed rather than silently treating them as equivalent.

That makes testing, diagnosis, audit, and rollback more local. The
architectural benefit is not merely that changes are separated
conceptually; it is that the system can attach different checks and
responses to different jurisdictions.

## 12. Intelligent agents

An agent can interpret business intent, choose concepts, formulate a
data request, invoke material systems, inspect results, and recommend
actions.

Without explicit jurisdictions, one probabilistic component can collapse
several acts of authority into one invisible inference:

> I think this is what the user means\
> → therefore this is the data object\
> → therefore this material procedure should run\
> → therefore this result answers the question\
> → therefore this action should follow.

Columna's architecture keeps those acts typed.

An agent may participate in every world. It should not become sovereign
over all three.

The principle is broader than "do not let the model write SQL":

> **Do not let an intelligent agent collapse governed crossings into one
> probabilistic act.**

## 13. The blast-wall effect

Earlier drafts treated *blast wall* as though Columna had two walls
corresponding to two components. That was too literal.

The better use of the metaphor is as a description of the **isolation
effect** produced when an independently governed Data World is made
architecturally explicit.

Manifold gives a particular Data World its governed ontology. Frame-QL
gives that world a ToD-native declarative and representational language.
The two interfaces govern how business meaning and material realization
interact with it.

Together they create a no-bypass property:

> **Business meaning cannot legitimately become material execution
> without passing through governed Data World identity and law.**

And in the return direction:

> **Material observations cannot legitimately become business answers
> merely because they were successfully computed; they must return as
> the governed Data World result that was actually established.**

This is the sense in which Columna takes advantage of the Data World as
a blast wall.

The Data World was already there. Columna makes use of its independence.

## 14. Design principle and implementation

This is a living architecture note. It describes Columna's governing
design principles and may evolve as the architecture and implementation
mature.

This paper describes **Columna's architectural design principles**. It
does not claim that every implementation is defect-free or that every
transitional execution artifact already expresses the separation
perfectly.

The principles are the test:

-   Manifold belongs to the Data World;
-   governed declarations acquire authority through accountable
    ratification rather than mere generation;
-   governed reducer identity and law belong to the Data World, while
    backend realization of the reducer belongs to material realization;
-   conceptual mappings among Data World objects may belong in Manifold,
    while material bindings belong to realization;
-   Frame-QL represents governed Data World requests relative to a
    Manifold;
-   material backends remain replaceable behind the realization
    interface;
-   connector/backend procedures preserve the relationship between
    material results and governed requests;
-   business and material authority do not bypass the Data World.

Where a current implementation places a Data World law on the
realization side, that is design debt against these principles rather
than an exception that redefines them.

## 15. Closing

The Data World exists whether an architecture recognizes it or not.

Theory of Data describes that world. Analytics must cross between it and
the Business World above and the Material Data World below.

Columna is one architecture built from taking that fact seriously.

It gives a particular Data World explicit ontology through Manifold and
a ToD-native declarative representation through Frame-QL. It then
governs the crossings so that business meaning can constitute data
without becoming data law, and material systems can realize data without
becoming data identity.

The result is not another semantic layer and not another execution
engine.

It is an architecture that uses the independent Data World to keep
meaning, data, and material realization distinct enough to govern —
and connected enough to work.
