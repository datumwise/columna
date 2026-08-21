# The release order — the flip choreography

**Standing release order, ratified 2026-07-27 (Huayin).** Not a suggestion and not a checklist item:
this order is what makes "publish-first means installable" structurally true instead of usually true.

---

## The order

```
1. Land the work on a release branch. CI green.
2. TAG the release branch — v<version> — and cut the GitHub Release from that tag.
3. Publish fires (OIDC Trusted Publisher). Wait for it green,
   INCLUDING the post-publish assert_pypi_versions gate.
4. Verify the pin resolves with the resolver a consumer actually uses:
       pip install --no-cache-dir "columna==<v>" "columna-core==<v>" "columna-server==<v>"
   NOT the JSON metadata API. See "the vantage point" below.
5. THEN merge to main. The push triggers the deploy, which finds the
   packages already installable and clears the wedge on attempt 1.
```

**Tag before merge. Publish before deploy. Every time.**

## Why — the race this removes

The deploy wedge lives in `website.yml` and refuses to build the site against packages it cannot
install. It is triggered by a **push to `main`**. The publish is triggered by a **release being
cut**. If you merge first and cut the release after, those two are racing, and the deploy is racing
from behind: it starts the moment the merge lands, while the packages it needs do not exist yet.

That race is not theoretical. **On 0.13.2 (2026-07-27) the deploy resolved on attempt 5 of 5** — the
final attempt of its retry budget, roughly 200 seconds of backoff, with no margin left. It went
green. It had no right to.

Reversing the order removes the race **structurally, with zero code**: by the time `main` moves, the
packages have been on PyPI for minutes and the pin has already been verified by a human or a gate.
The wedge then does what a wedge should — resolve immediately, and mean something when it doesn't.

This is not a new invention. It is what the house already did, correctly, twice (0.12.0 and 0.13.0,
both recorded in `specs/open_forks.md` as "executed publish-first"). 0.13.2 ran it backwards under
launch-eve pressure and got away with it by five seconds of CDN luck. Writing the order down is the
fix; the widened retry budget in `website.yml` (5 → 8 attempts, ~560s) is only a belt for the case
where someone runs it backwards again in an emergency.

## The vantage point — verify with the resolver, not the description

PyPI's `/simple/` index and its `/pypi/<name>/json` metadata endpoint are **separately cached across
a CDN, and can disagree in either direction.**

- **2026-07-26 (0.13.1):** a developer machine reported the pin installable; the CI runner, on a
  different edge, could not resolve it minutes later. → *one observer's "installable" is not global
  availability.*
- **2026-07-27 (0.13.2):** the JSON API reported `columna-core 0.13.2` **absent** while `/simple/`
  was already serving it. A checker trusting the JSON would have declared a live release broken.

So the rule is symmetric: the JSON API is not a slower mirror of the truth, it is a **different
vantage point** that can be stale either way. **Verify installability by installing** — `pip` against
`/simple/`, ideally more than once from more than one place. Never by reading a metadata endpoint
that merely describes the package. A convenient observation is still an observation.

## The deliberate inversion — a correctness unit merged before publication

**Annotation, 2026-08-20 (Huayin). The order above remains the norm; this is not a second default.**

Sometimes a correctness unit is reviewed and merged to `main` *before* its artifacts are published —
because the review is about the code, and the release decision is a separate, later judgement. That
happened on v0.15.0: PR #184 (the generated-family law) merged at `d164809` while `columna-core
0.15.0` did not yet exist on PyPI.

Two consequences, both expected, neither a fault:

1. **`main` sits shipped-coherent-red until publication.** The push triggers the deploy, the wedge
   cannot install a package that does not exist, and it fails closed with a named reason after its
   full retry budget. That red is the wedge holding. **Do not make it green by any means other than
   publishing the package** — not by relaxing the pin, not by widening the budget, not by skipping
   the job. A green obtained any other way is the exact failure the wedge exists to prevent.
2. **The shipped-coherent deploy must be explicitly rerun and verified after publication.** It will
   not fire again on its own: its trigger was the push, and that push has already been consumed. Use
   the repository's normal rerun mechanism once the packages are genuinely installable, and verify
   the live site rather than the workflow's conclusion.

Prefer the standard order. Choose the inversion only when the merge decision and the release decision
are genuinely separate, and record it — as this paragraph does — rather than letting a future reader
discover a red `main` and assume something broke.

## The v0.15.0 incident — content behind an unchanged version (2026-08-20)

**Recorded, not tidied away.** v0.15.0 published `columna 0.15.0` + `columna-core 0.15.0`, and
`columna-core 0.15.0` passed its shipped-artifact Afternoon gate. The release set was still not
coherent, and the reason is worth keeping:

`columna-server`'s **source** changed in that release — the generated-family law re-cut the four-mood
demo seeds — while its **version** stayed at `0.8.2`. So:

- `skip-existing` uploaded nothing for it, correctly: 0.8.2 was already on PyPI.
- `assert_pypi_versions.py` passed, correctly: 0.8.2 *is* live.
- The release-set coherence guard passed, correctly: it checks umbrella/core lockstep, and
  `columna-server` is not in lockstep.
- The published set installed cleanly, and `columna-server demo --play` printed a leg labelled
  `disclose` that returned `refuse` — **exiting 0**.

Three variants of one class, in order: a stale **pin** resolves (0.13.2/0.13.3); a stale **version**
resolves (the v0.15.0 preflight); stale **content behind an unchanged version** resolves (this one).
Each time, the guard that would have caught the previous variant behaved correctly and saw nothing.

Two guards close it, both fail-closed:

1. `scripts/release_pins.py --check-payload dist` — compares each **built** wheel against the wheel
   PyPI already serves for that same version, normalized. Changed payload under a reused version
   refuses the release. Runs in `publish.yml`'s build job, so it gates every PR as well as the tag.
2. `columna-server demo --play` now **verifies its own seeds**: a leg whose actual outcome differs
   from the mood its heading declares exits non-zero. The first-run surface is where a stranger meets
   the four moods; it must not be able to print a contradiction and succeed.

`v0.15.0` is **not** withdrawn, republished or overwritten — PyPI artifacts are immutable and the
0.15.0 core artifact remains valid, with a valid Afternoon attestation. It is superseded by `v0.15.1`,
which ships the coherent set (`columna 0.15.1` / `columna-core 0.15.1` / `columna-server 0.8.3`) and
raises the umbrella's **server** floor for the same reason the core floor exists: a release's umbrella
must not admit a stale companion.

## What stays true regardless

The wedge **fails closed**. The retry budget is bounded and exhausting it exits non-zero. Widening
it buys propagation time; it never forgives a missing package. If the wedge fails, the site does not
deploy — that is the guarantee, and no ordering change is permitted to soften it.
