# Doctrine ↔ code gaps — the ledger

Ratified doctrine the shipped code does not yet match. Every open row is a divergence `main` carries
**on the record** until the closing change merges. A gap lands here the moment it is known (a ruled
item leaving scope is a checkpoint event, surfaced before merge — never a silent drop); it is struck
when its fix merges, with the closing commit named.

| # | opened | doctrine | what `main` does | root cause | status |
|---|---|---|---|---|---|
| ~~DG-1~~ | 2026-07-14 (post WP-B merge `18189db`) | Capture v0.8 (§"Reduction OF a derivation"): unpinned `avg(aov) @ month` ⇒ **engine clarify** enumerating candidate input anchors; pinned `avg(aov@day) @ month` ⇒ **legal, definite quantity** served with a communicative disclosure naming the reading (ruling (A), CP-B1). | Both forms return **`error`/`unknown`**: pinned → "illegal expression construct: MatMult"; unpinned → "'avg' is not a scan operator". Inline reduction is unimplemented, so the ruled clarify and the ruled serve are both absent. | Ruling (A) was ruled at CP-B1 and scoped into B-4 by the B-1 report, then **descoped mid-build without a checkpoint** — surfaced at merge as if an agreed deferral. The descope fails closed (an error, not a wrong number), but the doctrine gap must not linger unrecorded. | ~~**CLOSED** 2026-07-14 by WP-B.1, merge `a074319` (PR #18). Both forms now match doctrine; verified green on merged main.~~ |

## Log
- **DG-1 opened 2026-07-14.** Recorded per Huayin's ruling (2026-07-14): "a ruled item leaving scope
  is a checkpoint event, raised before merge, every time"; "the unpinned case is capture-ruled — main
  currently contradicts ratified doctrine — that gap doesn't get to linger unrecorded." WP-B.1 (pinned
  inline reduction per (A), unpinned engine clarify per capture v0.8, the input_anchor-fit finding
  owed to CP-B2, and their tests) closes it.
- **DG-1 CLOSED 2026-07-14** by WP-B.1, merge commit `a074319` (PR #18). Pinned inline reduction serves
  with the immaterial communicative note; unpinned clarifies enumerating candidate input anchors —
  both match capture v0.8. No open gaps remain.
