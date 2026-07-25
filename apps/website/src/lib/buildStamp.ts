// THE BUILD STAMP — the deploy cache-buster's only moving part.
//
// WHY THIS EXISTS. `<meta name="build">` makes every production deploy's HTML byte-different, so
// Vercel's edge CDN re-caches every page globally on each deploy. That is the documented fix for the
// pre-#68 incident, where a stale /explorer <head> lingered at some PoPs after a deploy.
//
// HOW IT BROKE (found live on 2026-07-25, post-#88). Prod served `<meta name="build" content="">` —
// empty, not the SHA and not the 'dev' fallback. Two causes compounding:
//
//   1. This site is NOT built by Vercel's Git integration. The workflow builds in a GitHub runner and
//      ships with `vercel build --prebuilt` + `vercel deploy --prebuilt`. VERCEL_GIT_COMMIT_SHA is
//      injected by Vercel only when VERCEL builds from the Git integration, so in this flow it carries
//      no commit metadata — the CLI defines it EMPTY rather than leaving it unset.
//   2. The old code read `import.meta.env.VERCEL_GIT_COMMIT_SHA ?? 'dev'`. `??` only falls back on
//      null/undefined — an empty STRING sails straight through it. So the guard never fired and the
//      cache-buster silently went inert: every deploy emitted an identical meta, which is precisely the
//      condition the meta exists to prevent.
//
// THE RULE HERE: empty is the failure mode, so emptiness is made IMPOSSIBLE, not merely unlikely. The
// chain ends in a build-time timestamp, which can never be blank, and every candidate is rejected on
// *blankness* rather than on undefined-ness. The assertion below is the same has-to-be-loud principle
// as the llms-full anchor helper: if a future edit ever lets the stamp resolve blank, the BUILD FAILS
// rather than shipping a quietly inert cache-buster again.

/** A candidate counts only if it has non-whitespace content — `''` and `'   '` are treated as absent. */
function firstNonBlank(...candidates: Array<string | undefined | null>): string | null {
  for (const c of candidates) {
    if (typeof c === 'string' && c.trim() !== '') return c.trim();
  }
  return null;
}

// Vite statically replaces `import.meta.env.*`; process.env is the runtime truth in the Node build.
// Both are consulted because the value can arrive by either path depending on who runs the build.
const fromEnv = firstNonBlank(
  // 1. Vercel's own Git integration, if a Vercel-side build is ever used.
  import.meta.env.VERCEL_GIT_COMMIT_SHA,
  process.env.VERCEL_GIT_COMMIT_SHA,
  // 2. Explicitly exported by .github/workflows/website.yml — the authoritative value in OUR flow.
  process.env.SITE_BUILD_SHA,
  // 3. The GitHub runner's default, if the explicit export is ever dropped.
  process.env.GITHUB_SHA,
);

// 4. Last resort: a build-time timestamp. Not a commit identity, but it is unique per build, which is
//    all the cache-buster actually requires — and it cannot be blank.
export const BUILD_STAMP: string = fromEnv ?? `build-${new Date().toISOString()}`;

/** True when the stamp is a real commit SHA rather than the timestamp fallback (used in tests/debug). */
export const BUILD_STAMP_IS_COMMIT: boolean = fromEnv !== null;

// The loud guard. Unreachable by construction — which is the point: it fires only if someone edits the
// chain above into a state that can yield blank, and it fails the build instead of shipping silence.
if (BUILD_STAMP.trim() === '') {
  throw new Error(
    'build stamp resolved BLANK. <meta name="build"> must never be empty — an empty stamp makes every ' +
    "deploy's HTML byte-identical and silently disables the edge-CDN cache-buster (the pre-#68 stale-PoP " +
    'defense). Restore the fallback chain in src/lib/buildStamp.ts.',
  );
}
