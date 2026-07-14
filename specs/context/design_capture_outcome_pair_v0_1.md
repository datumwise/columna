# Design capture — outcome as a pair (v0.1, ratified 2026-07-11)

**Status.** Ratified mental model (Huayin). Interpretation-layer only for contract v1 — the
shipped wire is unchanged and the site widget consumes it as-is. Feeds: the docs wire-contract
page, the WP-5.2 site agent's authored corpus, and the contract v2 ledger (entry below).

## The model

Every outcome is a pair: **(result, disclose)**. Both components always exist.

- result: populated or empty.
- disclose: always present; carries material content or not. (Serve's disclosure is never
  absent — it is merely immaterial: high-level execution record, filed for audit.)

The **mood is how the pair reads** — a derived classification, not a primitive:

| | disclose: nothing material | disclose: material content |
|---|---|---|
| **result populated** | **serve** | **disclose** (served-and-disclosed) |
| **result empty** | — | **clarify** (alternatives) / **refuse** (reasons) |

Classification rule, mechanically checkable from wire fields:
`material disclosure present ∧ result populated ⇒ serve promotes to disclose`. The empty-result
cell splits by what the disclosure carries: substitutable alternatives ⇒ clarify; reasons ⇒
refuse. The empty/immaterial cell is unreachable by construction — an empty result always owes
an explanation.

Consistency: this is Fork C of `structured_disclosure_capture.md` ("a disclosure with
materiality: material and a served value is served-and-disclosed; the same contested dimension
with no served value is a clarify"), stated as the general structure. It also resolves the
WP-2.2 acceptance-#5 wording wobble: result + material caveat *is* disclose, by definition.

**"Four moods" remains the public vocabulary** (homepage, essay, launch post, README): under
this model it stays true — four is exactly how many ways the pair can read.

## Error is not a mood

`error` conflates two unrelated things and therefore does not belong in the outcome vocabulary:

1. **Semantic non-service** — really a refuse or clarify wearing a stack trace; should be
   classified honestly as such, with reasons, in the outcome channel.
2. **Mechanical failure** — plumbing; not an analytical answer at all; belongs in the
   transport-level error path (MCP error), not the outcome channel.

Contract v1 ships `error` as a fifth outcome value (deliberately distinguishable from refuse —
acceptance #6). Unchanged for v1. Site treatment: render neutral, labeled "not a mood."

## Contract v2 ledger entry

> **CV2-1 (2026-07-11).** Outcome becomes an explicit derived classification over the
> (result, disclose) pair; the classification rule ships in the contract text. Mechanical
> errors leave the outcome channel for the transport error path; semantic non-service is
> classified as refuse or clarify with reasons. Rationale: this file. No v1 change.
>
> **CV2-2 (2026-07-14, WP-B fertility, ruling §5).** An *exercised* UNTESTABLE fertility license
> would owe a runtime "license is asserted, not proven" disclosure — but v1's closed caveat
> vocabulary has no code that fits it (checked: `unconfirmed_assumption→input_anchor` is material
> and means input-anchor choice; `provenance` would conflate asserted with verified; no reserved
> code matches), and we do NOT mint one (S1a lesson). Ruled deferred: in WP-B, UNTESTABLE licenses
> are recorded and visible in describe but **never exercised** (the reduce-path optimization runs
> only under VERIFIED/CORROBORATED), so an asserted license never changes a served number and needs
> no runtime caveat. The exercised-UNTESTABLE disclosure question waits for the era that can exercise
> it. No v1 change. (CORROBORATED rides the existing immaterial `provenance` code.)

## Site touchpoint — APPLIED (exhibit script v0.2, 2026-07-11)

Exhibit B first-response caption now reads: *"this is the actual wire — what an AI agent
receives. Every answer is a pair: a result, and its disclosure. The mood is how the pair
reads."*
