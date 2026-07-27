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

## What stays true regardless

The wedge **fails closed**. The retry budget is bounded and exhausting it exits non-zero. Widening
it buys propagation time; it never forgives a missing package. If the wedge fails, the site does not
deploy — that is the guarantee, and no ordering change is permitted to soften it.
