# Shared resources, local meaning — a recommendation

**Status:** recommendation, design only. Nothing here authorizes implementation.
**Responds to:** `columna_platform_shared_resources_local_meaning_architecture_note_v0_1.md` (CG + Huayin, 30 Sep 2026)
**Based on:** the Platform tree at `7849e8a`, read at file:line; the B-4a″ HLL work; `docs/architecture/topology_core_platform_delivery_v0_1.md`.
**Sections 8 and 9** record a follow-on discussion with Huayin, 1 Oct 2026, on MME lifecycle when meaning
changes and on the base MME. The rulings and the design principle in those two sections are his.

---

## Summary

I agree with the note. Much of it describes the Platform we already have rather than proposing
something new, which is good evidence that the architecture was found rather than invented.

I would change five things, and sections 8 and 9 then work through two cases Huayin raised
afterwards: what happens to stored material when meaning changes, and what the shared physical layer
actually is.

1. The note says what gets shared. It should also say how meaning stays local. The code has an answer,
   and that answer explains every problem we found.
2. The five kinds of customization can be reduced to three, and there is already a mechanical way to
   tell which kind a change is.
3. The rule about which direction authority flows needs a second part. It forbids physical facts from
   changing meaning. It does not forbid one Manifold's meaning from reaching into another's, which is
   the problem the code actually has.
4. The order of work should change. Closing the jurisdiction holes has to come before the Law
   Catalogue, not after.
5. Two corrections: universes are shared, not Manifold-local; and the second proof should be
   `ProviderProfile`, not the Operator Registry.

---

## 1. Two kinds of object, and only one of them carries its jurisdiction

Columna has values and it has declarations.

A value is a `FamilyState`, an `ExpressionOutput`, the material sitting in a store. Every value carries
an `AnalyticalInstance` that records which Manifold it belongs to, along with the universe,
participation, scope and data state. That record is compared whenever two values are combined and
whenever a value is admitted. Values cannot quietly move between Manifolds.

A declaration is a `MeasureFamily`, a `GovernedExpression`, an `AnalyticalLaw`, a `ProviderProfile`.
Declarations travel as bare strings or bare objects. Nothing checks which Manifold they came from.

Every leak we found is a declaration crossing a line that a value could not cross:

- `MME.subject()` hands back a foreign `MeasureFamily` unchanged (`mme.py:429`), and `authorize` then
  looks up that family's law in the *local* registry (`authorization.py:342`).
- `establish_root` folds data using the local law while stamping the result with the foreign Manifold's
  instance (`mme.py:471,484`).
- `ExpressionEvaluator.evaluate` takes an expression object with no check and resolves its operands
  locally (`expression.py:104,150`).
- One `REGISTRY` and one `ProviderProfile` are shared by every Manifold in the process, and both are
  backed by ordinary mutable dicts (`builtins.py:199,300`).

There is exactly one place where a declaration's Manifold is checked: `_require_own`, called when a
family or expression is registered (`mme.py:315,326`). That is the right idea in the right place. It is
just applied in one place out of five.

So the mechanism the note needs already exists in half-built form. The rule is:

Values carry their jurisdiction with them. Declarations have to be resolved into one before they mean
anything.

"Resolving a declaration into a jurisdiction" is exactly the Catalogue plus selection plus local
registry pattern the note proposes. That makes the pattern more important than the note claims: it is
not a convenient way to pick law members, it is the general fix for a general problem.

---

## 2. Three kinds of customization, and a test that sorts them

The note lists five kinds. They reduce to three if you ask what actually changes when the thing
changes:

- **Constitutional.** Existing governed state may no longer belong. Selecting a different law member
  is this. So is defining a new local measure.
- **Interpretive.** Future resolutions change; anything already resolved does not. Aliases and
  authoring defaults are this.
- **Operational.** Nothing analytical changes at all. Cache policy, pinning, provider preference.

There is already a mechanical test for which bucket a change falls into. `witness.py` works out what is
identity-bearing by subtraction over the record's fields, and a family's witness includes the full
digest of its law. So:

If a change moves a `ConstitutionWitness`, it is constitutional and needs succession. If it does not,
it is not.

That settles arguments like "is this a selection or a default?" without anyone having to rule on it.

The note also misses a kind that the accepted topology already names: the material map.
`PhysicalFamilyBinding` and `SourceBindings` map governed constituents to physical columns, and
`SourceBindings` is keyed by a bare connection token with no Manifold (`source.py:143`). Renaming a
column is not a constitutional change and it is not policy either. It needs its own slot.

---

## 3. The rule about direction of authority needs another part

The note says: authority flows from meaning towards realization, and physical convenience does not flow
back into meaning. That is right, and it is enforced for values. #367 proved it for HLL.

Two more things belong in the rule.

**One Manifold's meaning must not reach into another's.** Crossing between jurisdictions should be
explicit or it should not happen. Today it happens by accident, as section 1 shows.

**One Manifold's activity must not change another's choices.** A single process counter mints
`admitted_seq` (`materialization.py:84`), and `admitted_seq` breaks ties when candidates are ranked
(`:621`). So traffic in Manifold B shifts the ordering trace in Manifold A. No answer comes out wrong,
because the ordering within A is still total. But A's behaviour is no longer reproducible without
knowing what B was doing, and reproducibility matters for governance.

---

## 4. Order of work: close the holes first

This is the part I would most like you to agree with.

The Law Catalogue turns a dormant bug into a live one.

Right now, when `authorize` resolves a foreign family's law in the local registry, nothing goes wrong,
because every MME shares the same registry. The constitution is mixed, but it is mixed between
identical things. Once Manifold A can select `HLL_SKETCH[1]` while Manifold B selects `[2]`, a family
declared under B and authorized under A gets authorized against the wrong member's region and algebra.
That produces a wrong answer, not just untidy code.

So the order should be:

**J-0, jurisdiction closure.** Small. `subject()` refuses a declaration from another Manifold.
`establish_root` and `evaluate` get the same check. A credential is tied to the authority that minted
it. The shared catalogues are made genuinely immutable rather than immutable by docstring. The default
`manifold="default"`, `build="build-1"` goes away, so two MMEs built with no arguments cannot collide.

**B-4a″(ii), the Law Catalogue.** Exactly as the note scopes it. Its acceptance test — two Manifolds
with different selections coexisting in one process — only means something after J-0.

**Second proof: `ProviderProfile`.** See below.

**Abstraction, if it turns out to be earned.**

---

## 5. Second proof should be `ProviderProfile`, not the Operator Registry

Platform has no operator registry. It refuses to have one: `PlatformExecutionProvider.operators()`
raises, and the message says that a governed continuation law naming an operator is not the same thing
as a registry of callable signatures (`provider.py:129-132`). Operators live in Core, in
`columna_core/operators.py`, as a process-global dict with no Manifold anywhere in it.

So an operator unit would be a Core change, not a Platform one. It is not a peer of the law unit, and
the two would not even share a package, which is a good reason not to abstract from the pair.

`ProviderProfile` is a better second case. It is already passed into the MME in the same constructor
slot as `laws`. It already varies in the tree — `NO_MEAN` exists so that "a backend's inability does not
remove a law" can be tested. And it carries a different kind of authority (operational rather than
constitutional), which is what you want from a second case: something similar in shape and different in
meaning.

---

## 6. Universes are shared, not Manifold-local

The note says measure and dimension names are Manifold-local. Measures, yes. Dimensions, no.

The existing two-Manifold exhibit builds `andfam.commerce` and `acme.commerce` over the same `COMMERCE`
`Universe` object (`columnar/exhibit.py:54,64,162`). A `Universe` is a closed set of constituents, a
ground and a participation law. By the note's own test in section 5.1, that is governed machinery, so it
belongs on the shared side. Two tenants of one model sharing geometry while keeping separate
jurisdictions is a reasonable pattern and it already works.

This helps the architecture rather than hurting it. Universes are a second shared resource, and
constituent names belong to the universe rather than to the Manifold. Measures stay local, and already
are: a measure name is an MME registration, guarded by `_require_own`. No global measure catalogue.

One more placement point. The accepted topology says multi-Manifold work and the publication lifecycle
are shared Columna concerns, not Platform-only ones. It also already names the stages: authored,
accountably ratified, immutably published. I would use those words rather than introducing a parallel
set.

---

## 7. A Manifold is already an object graph, so do not add a class

What a Manifold amounts to today is this:

```
FrameQLService( MME( universe, laws, provider, manifold=…, build=… ) )
```

Names resolve through `MME.sort_of` against the families and expressions registered in that MME. Law
vocabulary and provider profile are already constructor arguments.

Three things are missing, and none of them is a class:

- `laws` never actually varies. Every construction site passes the same module-level object.
- `AnalyticalInstance.constitution_context` is a slot reserved for publication-level constitution and
  deliberately left empty. Its own comment says nothing computes it yet, because there is no
  publication object. So a Manifold's constitution currently has no identity.
- Nobody has said how `manifold` and `universe` relate.

A `Manifold` class would not supply any of those.

---

## 8. When meaning changes, the local MME is disposable

Huayin's design principle (1 Oct 2026): a Manifold-local MME should stay small, simple and agile, and he
would rather regenerate one than manage a partition.

There is no partition cost to add. `MME.__init__` constructs `MaterializationStore(self.build)` — one
store per MME, per build. So "wipe when the constitution changes" is, concretely: build a new MME for
the new build and do not hand it the old store. The old store then has no references and goes away.
Keeping it is a deployment choice, not a kernel feature.

The rule and the existing design are therefore the same design, differing only in whether a deployment
retains the old store. That choice should stay outside the kernel.

**The rule also lets us delete code rather than add it.** There is machinery today for a case the rule
forbids: changing a declaration in place inside one build. If a meaning change always means a new build,
an in-place change should **refuse** rather than be handled, and `_declaration_moved`,
`_declaration_moves`, `stale_states` and the looseness in `attach_store` all become removable. That is
worth doing on its own merits, because `_declaration_moved` currently supersedes by bare family name
across every attached store with no manifold or build filter — so one Manifold's declaration change can
supersede another's material of the same name.

One thing to keep from the current approach: supersession and removal stay separate levers.
Supersession stops material serving; `residency` and eviction decide whether the bytes linger.
Conflating them turns a governance act into a storage decision.

### The three detection holes

These are the real content of "meaning changed and the stored fact did not".

1. **The off-build guard is opt-in.** In `MME.put`, `witness` and `build` both default to `None` and the
   checks read `if build is not None and …`. The realization path supplies them because they come off
   the offer. The local path — `admit`, `establish_root`, `retain` — supplies nothing. So the check that
   enforces "material does not cross into a new world by being present" does not run on the path most
   material takes.
2. **`_declaration_moved` is manifold-blind and build-blind**, as above.
3. **Detection only fires at re-registration.** `_declaration_moved` is called from `register_family`
   and `register_expression`. But a family's witness includes the full digest of its bound law, so once
   member selection is per-Manifold, changing the selection moves every family witness in that
   Manifold — with no declaration re-registered, nothing notices. `stale_states` only reports moves
   already caught.

Three fixes, none of which is wiping:

- a change of law selection mints a new build, so the partition does the work it was designed for;
- the off-build check becomes mandatory rather than opt-in;
- an MME records the digest of its resolved constitution alongside the declared build, and refuses if
  the same build token returns with a different resolved constitution. The build token stays **declared,
  not computed** — that is the existing ruling and I would not change it. Reusing a build token after
  changing meaning simply stops being silent.

---

## 9. The base MME

The name is Huayin's (1 Oct 2026): **base MME**, not "shared MME". Whatever it is called, it must be a
`RealizationProvider` and nothing else. That protocol has only `propose` and `realize`, so no query
surface exists to misuse, and "it never faces clients" becomes structural. Any other kind of object makes
that guarantee a rule somebody has to remember.

### What it can be characterized by

It cannot rely on any Manifold for measure names or analytical laws. The vocabulary available to it is
exactly what is installation-shared:

```
AVAILABLE                               UNAVAILABLE
Catalogue member ids (HLL_SKETCH[1])    measure names
Universe geometry, constituent names    family ids
composition tokens                      a Manifold's SELECTION of a member
governed value type / value form        participation
evidence / data state                   scope
```

The distinction that makes this work: `HLL_SKETCH[1]` is a shared Catalogue address and is available to
the base layer. *That Finance chose `[1]`* is local meaning and is not. **Member identity is shared;
member selection is local.** This is also why universes being shared governed geometry (section 6)
matters: anchor geometry is one of the few jurisdiction-free facts the base layer can index on.

It follows that its description contains nothing a Manifold can change. Finance moving from `[1]` to
`[2]` does not invalidate base state described as `[1]`-compatible; that state simply stops matching
Finance's requirements. The base layer needs no wiping on any Manifold change.

### Why the two halves join — this is the architecture

Huayin's point, and it is a better argument for both halves than either has alone:

> The local MME can be small, agile and freely discarded precisely because the base layer holds the
> expensive jurisdiction-free work that survives a Manifold rebuild.

Regenerating a local MME after a constitution change is only affordable if the base-grain scan does not
have to happen again. The base layer is what makes disposability affordable.

What belongs down there: expensive root formation at base grain, keyed by geometry plus evidence state;
evidence-state identity, which is jurisdiction-free; cold start after a rebuild. **Not** coarsened family
state — a family's region and law live in its jurisdiction.

### Two corrections to the freedoms claimed for it

**It is not free of physical-source concerns.** It holds no binding — no map from governed constituent to
physical column — and that part is right. But its contents came from a source and carry that source's
access restrictions. A Manifold never permitted to see a warehouse's rows must not receive base state
derived from them. Said the other way round: the base layer is the one place where source access control
has to be explicit, because it is the only place where state outlives the jurisdiction that paid for it.

**Its correctness bar goes up, not down.** The local MME is wipeable, so a mistake there is cheap. The
base layer is never wiped and is shared by everyone, so a mistake is wrong everywhere at once and
survives every rebuild. Two consequences:

- it needs its own supersession lifecycle keyed on **evidence state** rather than on constitution. When
  the warehouse reloads, base state for the old load is stale for reasons that have nothing to do with
  any Manifold;
- admission from base layer into a local MME has to test entitlement rather than agreement. Fidelity
  check 4 compares the offer's instance against what the asking MME expects, which a provider satisfies
  by copying `requirement.instance` out of the requirement it was handed. What is missing is the stored
  payload's evidence and formation provenance, and `RealizationStanding` is only `(provider, carrier)`.

Both are the same shape as the HLL bug we fixed in #367, and the shape is worth stating plainly: a check
that compares a claim against an expectation only tests whether they agree. It does not test whether the
claim was earned. `get_estimate()` passed every type check for months by returning a plausible number.

### One distinction, so we do not over-constrain

Banning cross-Manifold access at the user surface should mean banning **ad-hoc** access — a Frame-QL
query naming another Manifold's measure. It should not rule out a future **declared** bridge, if someone
genuinely needs to compare Finance revenue with Marketing revenue. The code's current stance says the
same thing from the other side: crossing is *"an EXPLICIT governed crossing — not an incidental
consequence of one runtime, one store, or two worlds choosing the same name"*. Writing the rule as "no
incidental crossing" closes the hole without nailing the door shut on a governed object we may want.

---

## 10. What not to build

No `Manifold` class. No `ResolvedManifoldEnvironment` until two cases actually share visible machinery.
No generic overlay or `Catalogue[T]`. No global measure catalogue. No type catalogue until there are
types to put in it. No shared pool. No cross-Manifold identity by any route.

Also no authoring-default mechanism in Platform. The kernel already refuses a missing identity-bearing
parameter, with the message "No default is invented", and refuses an undeclared one. That refusal is
better doctrine than a default system. Defaults belong to the authoring surface, which is Core's.

---

## 11. Questions I cannot settle

- Whether the publication object that fills `constitution_context` belongs to Core or Platform. The
  topology says the lifecycle is shared; the empty slot is in the Platform kernel.
- Whether two Manifolds should be allowed different `lg_k` once the Catalogue can express it. It is
  fixed process-wide today, and the member constitution will carry it.
- Whether universes should ever be private to one Manifold. I recommend shared by default. Nothing in
  the code forces either answer.
- Whether the base MME is in scope at all before a concrete cross-Manifold reuse need exists. Sections 8
  and 9 argue it is what makes local disposability affordable, which is an argument for it earlier than
  "when sharing is needed" — but it is still a new component and nothing today requires it.
