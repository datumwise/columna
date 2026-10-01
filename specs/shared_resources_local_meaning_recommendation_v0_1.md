# Shared resources, local meaning — a recommendation

**Status:** recommendation, design only. Nothing here authorizes implementation.
**Responds to:** `columna_platform_shared_resources_local_meaning_architecture_note_v0_1.md` (CG + Huayin, 30 Sep 2026)
**Based on:** the Platform tree at `7849e8a`, read at file:line; the B-4a″ HLL work; `docs/architecture/topology_core_platform_delivery_v0_1.md`.

---

## Summary

I agree with the note. Much of it describes the Platform we already have rather than proposing
something new, which is good evidence that the architecture was found rather than invented.

I would change five things:

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

## 8. The shared materialization pool: two things worth writing down now

The note's section 17 is right, and the evidence is better than it claims. A provider is handed only a
`FamilyRequirement`. A `RealizationOffer` has no Manifold field at all. `RealizationManager.establish`
is a static method whose first argument is the MME, so one manager can establish into any number of
them. And the one real provider is Manifold-agnostic by construction: it keeps the Manifold on a
per-proposal handle rather than on itself, rebuilds the governed wrapper on each call, and passes the
Arrow array through untouched. "The bytes are shared, the standing is jurisdiction-specific" is already
how it behaves.

Two problems to record before anyone builds a pool:

**The instance check verifies agreement, not entitlement.** Fidelity check 4 compares the offer's
instance against what the asking MME expects. A provider satisfies it by copying
`requirement.instance`. That is safe today only because a provider's claim is backed by a declared
physical binding and an actual refetch. A pool's claim is "I already have this", which is precisely the
claim nothing checks. What is missing is the stored payload's evidence and formation provenance, and
`RealizationStanding` is only `(provider, carrier)`, so it does not carry it.

**Supersession cascades across jurisdictions.** `supersede` walks descendants through
`establishment.derived_from` and marks them, with no Manifold check. The note wants Finance's admission
to lapse while Marketing keeps using the same bytes. That needs the cascade scoped first.

Both are the same shape as the HLL bug we just fixed, and it is worth stating the shape plainly: a check
that compares a claim against an expectation only tests whether they agree. It does not test whether the
claim was earned. `get_estimate()` passed every type check for months by returning a plausible number.

---

## 9. What not to build

No `Manifold` class. No `ResolvedManifoldEnvironment` until two cases actually share visible machinery.
No generic overlay or `Catalogue[T]`. No global measure catalogue. No type catalogue until there are
types to put in it. No shared pool. No cross-Manifold identity by any route.

Also no authoring-default mechanism in Platform. The kernel already refuses a missing identity-bearing
parameter, with the message "No default is invented", and refuses an undeclared one. That refusal is
better doctrine than a default system. Defaults belong to the authoring surface, which is Core's.

---

## 10. Questions I cannot settle

- Whether the publication object that fills `constitution_context` belongs to Core or Platform. The
  topology says the lifecycle is shared; the empty slot is in the Platform kernel.
- Whether two Manifolds should be allowed different `lg_k` once the Catalogue can express it. It is
  fixed process-wide today, and the member constitution will carry it.
- Whether universes should ever be private to one Manifold. I recommend shared by default. Nothing in
  the code forces either answer.
