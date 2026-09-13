# Successor → shipped serving: first integration slice — **STOPPED AT THE RULED STOP CONDITION**

**Status:** finding, 2026-09-12. The §5 analytical-request resolution **SUCCEEDS at the governed
format level** and the slice **STOPS before the server**, for a reason that is a deployment and
compatibility fact rather than an implementation gap. Recorded under the stop condition ruled by
Huayin the same day: *"If the governed logical projection cannot resolve the public Frame-QL series
token to a unique governed `family_id` without using the legacy ontology, stop there. That result
would be the point of the integration proof, not a failure to work around."*

**What was authorized:** one deployment-opted-in governed Manifold, one family, `check_frame_query`
only, through `PlatformExecutionProvider`, with the legacy planner untouched.

**What exists as a result:** the resolver and the provider, proven against the v2 governed format.
**What does not:** the server-side opt-in, because no v2-governed Manifold can exist in the store.

---

## 1. §5 succeeds — at the format level

A public Frame-QL request resolves to `AnalyticalIdentity(family_id, anchor)` from governed law
alone. No `model.py` measure/member resolution, no planner identity logic, no `.cml` meaning lookup,
no fuzzy matching, no convenience map, no fixture special case.

| §5 question | answer | mechanism |
|---|---|---|
| 1 · series token → one `family_id` | **yes** | `GovernedPublicationV2.resolve_reference` — an EXISTING governed function: canonical reference or declared alias, one direction only |
| 2 · requested anchor → governed anchor | **yes** | the requested component set is matched against the publication's own `anchor` declarations; `AT {store*day}` → `sale_at` |
| 3 · no governed match | **`WantOfLaw`**, verbatim token, no guess | nothing near-matches, case-folds, or prefixes |
| 4 · more than one match | **cannot occur** | `parse_publication` refuses at read time (§2.2); the resolver relies on that guarantee rather than restating it |
| 5 · anchor not established | **`WantOfLaw`** naming what IS declared | undeclared components, a proper subset, and `AT {}` are each refused, the last two as unlicensed movement |

**No name→family map was written.** The resolution *is* the governed function; a second map in
platform or server code would have been the convenience map the ruling forbids and a second
enumeration of a rule the publication format already owns.

**The answer to question 4 is better than the question assumed.** Ambiguity is not resolved by the
resolver choosing well — it is prevented one layer earlier, at parse time, by the format itself. The
control therefore pins the format's refusal rather than the resolver's behaviour: if §2.2 ever
weakens, the control fails rather than the resolver silently taking the first match.

## 2. Where it stops, and why

Two independent facts, either of which alone is sufficient.

**(a) The shipped governed unit is publication format major 1, and carries no families.**
`columna_server/governed/firstlight/governed-publication.json` declares `measure` + `member` — the
legacy ontology — with no `family` declaration, hence no `family_id` and no `canonical_reference`.
Resolving a series token against it would mean resolving through measure/member, which §5 forbids.
The v2 reader refuses it outright, in its own words:

> this is a publication-format v1 artifact, and there is NO automatic v1 read. A v1 artifact
> under-determines its own meaning: its family law lives in a private realization mapping, so
> reading it here would require inferring analytical law — the exact defect v2 exists to remove.

**(b) The server cannot ingest a v2 publication at all.**
`columna_server.registry.SUPPORTED_PUBLICATION_FORMAT_MAJOR = 1`. Handed the v2 lighthouse artifact
it raises `UnsupportedPublicationFormat: publication_format_version '2' has an unsupported major
(this server supports major 1)`. So a v2 artifact placed in a runtime directory today does not
produce a governed entry — it produces a load *condition*.

**These are the same open question the freeze deliberately left open.** The realization-v2 freeze
(RATIFIED 2026-09-12, §10.2) records the server publication-major mismatch as **a separate
compatibility ruling, explicitly not realization-format constant coherence**. That ruling is the
gate on this integration. The stop is therefore not a surprise from an unexplored corner — it is the
held-open question arriving where it was always going to arrive.

**A third fact, smaller but real:** the store's unit of deployment is a directory containing
`manifold.cml` (`store.py` loads nothing else). There is no way to deploy a governed-only runtime
unit, so even after (a) and (b) are resolved, an opted-in Manifold would still ship a `.cml` beside
its artifact. The successor would not read it — but the store would still parse it through the
legacy parser to load the unit at all.

## 3. What was built, and what it proves

- `columna_platform/request.py` — the resolver. Governed inputs only; two kinds of no, kept apart.
- `columna_platform/provider.py` — `PlatformExecutionProvider`, implementing
  `columna_server.provider.ExecutionProvider` **structurally**, importing nothing from the server
  (the protocol is `@runtime_checkable`; and `columna_server.store` imports `columna_core.parser` at
  module scope, so importing the server would drag the legacy stack into the successor path).
- `columna_platform/serving.plan_result` — the pre-flight, returning the neutral `FrameResult`.
  It does not consult the retained-state store: a pre-flight that asked whether material state were
  present would answer "can this be served now" rather than "is this askable".
- `serving.decide_result` / `decide` — the §4 factoring: neutral core, wired wrapper, one serializer.

**Provider honesty (§7).** `run`, `explain` and `operators` raise `UnsupportedByThisProfile` and
never delegate to Core. That exception is deliberately **not** a `ProofRefusal`: it carries no
jurisdiction, because a capability limit wearing a governed jurisdiction would tell an operator
their question was unlawful when it was merely unimplemented — and `want_of_state`'s remedy would
send them to re-materialize against a path that does not exist.

`published_scope` returns `None`, the one method that answers rather than refusing. Not a stub: the
protocol says *"or None"* and both server consumers already branch on it (`tools.py:231`, `:467`).
There is no published scope on this path, and saying so is the smallest behaviour consistent with
the contract as written.

## 4. Public contract impact: none

The 13-tool set, `_CAVEAT_KEYS`, `contract_version "5"`, the stable condition codes, Frame-QL syntax
and physical-identifier insulation are all untouched — nothing in the server changed. No catalog kind
and no condition code was added; per §8 provider choice is operational, and per §6 no public enum was
extended. `platform_profile.toml` keeps `adds = []`: the successor exposes no capability Core does
not, and this slice adds no public capability at all.

## 5. The smallest unblock

Not authorized here; recorded so the next ruling has the options in front of it.

1. **Rule the server's publication-major question** (the one already held open). Until major 2 is
   readable by the server, no successor integration can be exercised on any surface.
2. **Deploy one v2-governed runtime unit.** Which requires (1), plus a decision about whether a
   governed unit may ship without a `.cml`, or must carry one it does not use for meaning.
3. Only then does the deployment opt-in have something to select, and negative control 1
   (*same artifact, no opt-in → Core provider*) become a test rather than a tautology.

Until then the opt-in seam is deliberately **not** written: an opt-in that can never select anything
would be built against a hypothesis, and its negative control would pass for the wrong reason.
