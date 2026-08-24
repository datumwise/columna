// Protected-discoverability check — the routes the repair sequence landed must stay reachable, and
// the "start here" designation must stay singular, or the build fails.
//
// WHY THIS EXISTS. Repair Units 1–4 landed two public-root surfaces and then nothing on the site
// pointed at them properly. /start-here — ruled the site's cold-reader entrance and placed first in
// /learn's "Start here" group by ruling — had NO homepage link at all, while the homepage went on
// marking a position piece "start here", so two surfaces claimed one role. /known-issues shipped with
// exactly one inbound link in the whole site (the footer meta line), which means one careless footer
// edit orphans it. Both conditions were invisible: `check_fragments.mjs` validates that a link's
// `#fragment` resolves, and says nothing about a link that was never written.
//
// This is the smallest guard that would have caught them. It is NOT a navigation framework and does
// not try to become one: it is a short, explicit table of relationships someone RULED, each carrying
// the reason it is defended. Adding a route here is a decision, not a default.
//
// SCOPE, deliberately small, matching check_fragments.mjs: it reads `dist/` AFTER the build, so it
// tests the bytes that ship rather than the sources that produce them. Text-scan only — no Astro
// internals, no parser, no dependency.
import { readFile, access } from 'node:fs/promises';
import { join } from 'node:path';

const DIST = new URL('../dist/', import.meta.url).pathname;

// dist route -> file on disk. Astro emits directory-style routes (`/start-here/index.html`).
const pageFile = (route) =>
  route === '/' ? join(DIST, 'index.html') : join(DIST, route.replace(/^\//, ''), 'index.html');

const read = async (file) => {
  try {
    return await readFile(file, 'utf8');
  } catch {
    return null;
  }
};

// A link to `/x` may ship as href="/x" or href="/x/". Both count; nothing else does.
const linksTo = (html, route) => {
  const re = new RegExp(`\\bhref\\s*=\\s*"${route.replace(/[/]/g, '\\/')}\\/?(?:[#?][^"]*)?"`);
  return re.test(html);
};

// ── THE PROTECTED RELATIONSHIPS ─────────────────────────────────────────────────────────────────
// Each row is a ruling someone made, not a convention someone noticed.
const PROTECTED = [
  {
    route: '/start-here',
    why: 'Repair Unit 4 (PR #222) landed the cold-reader on-ramp; Huayin 2026-08-24 ruled it the one site surface that owns the public "start here" role.',
    linkedFrom: [
      ['/', 'the homepage wayfinding band — the entrance a cold reader actually arrives at'],
      ['/learn', 'first in the "Start here" group, by ruling (Huayin, 2026-08-24)'],
      ['/evidence/walkthrough', 'the walkthrough bullet became a link only because this route landed (ruling, 2026-08-22)'],
    ],
    inLlms: true,
  },
  {
    route: '/known-issues',
    why: 'PR #221 landed the public technical record. Its ONLY inbound link is the footer meta line, so a footer edit orphans it silently.',
    linkedFrom: [['/', 'the global footer meta line — one durable link, unstyled and unalarmed']],
    inLlms: true,
  },
];

const failures = [];

for (const p of PROTECTED) {
  const file = pageFile(p.route);
  try {
    await access(file);
  } catch {
    failures.push({ what: `${p.route} does not exist in dist/`, why: p.why });
    continue;
  }
  for (const [from, reason] of p.linkedFrom) {
    const html = await read(pageFile(from));
    if (html === null) {
      failures.push({ what: `${from} does not exist in dist/, so ${p.route} cannot be linked from it`, why: reason });
    } else if (!linksTo(html, p.route)) {
      failures.push({ what: `${from} no longer links ${p.route}`, why: reason });
    }
  }
  if (p.inLlms) {
    const llms = await read(join(DIST, 'llms.txt'));
    if (llms === null) failures.push({ what: 'dist/llms.txt is missing', why: 'the machine-facing index' });
    else if (!llms.includes(p.route)) {
      failures.push({
        what: `/llms.txt does not mention ${p.route}`,
        why: 'machine-facing discovery must name the surfaces a reader is sent to',
      });
    }
  }
}

// ── THE SINGULAR "START HERE" ───────────────────────────────────────────────────────────────────
// The homepage wayfinding band marks exactly ONE unnumbered entrance, and that entrance must be the
// route that owns the role. Two "start here" marks is the precise contradiction this unit repaired.
const home = await read(pageFile('/'));
if (home === null) {
  failures.push({ what: 'dist/index.html is missing', why: 'the homepage' });
} else {
  const entrances = [...home.matchAll(/<li[^>]*class="[^"]*\bdir-entrance\b[^"]*"[^>]*>([\s\S]*?)<\/li>/g)];
  if (entrances.length !== 1) {
    failures.push({
      what: `the homepage wayfinding band has ${entrances.length} entrances marked "start here", expected exactly 1`,
      why: 'one role, one surface (Huayin, 2026-08-24)',
    });
  } else if (!linksTo(entrances[0][1], '/start-here')) {
    failures.push({
      what: 'the homepage "start here" entrance does not point at /start-here',
      why: '/start-here owns the public "start here" role outright (Huayin, 2026-08-24)',
    });
  }
}

// ── THE RETIRED /research CLAIM ─────────────────────────────────────────────────────────────────
// Repair Unit 3 made /research's real contract visible: a PRESERVED SNAPSHOT, not a running index,
// with current publication records on /about. The homepage promised the opposite for one more route
// than it should have. This asserts the retired claim does not return.
const RETIRED = 'one click from its DOI';
if (home !== null && home.includes(RETIRED)) {
  failures.push({
    what: `the homepage still carries the retired claim "${RETIRED}"`,
    why: 'Repair Unit 3 reframed /research as a preserved snapshot; the running-index promise is false',
  });
}

if (failures.length) {
  console.error(`\nPROTECTED DISCOVERABILITY BROKEN — ${failures.length} failure(s)\n`);
  for (const f of failures) {
    console.error(`  ${f.what}`);
    console.error(`      ${f.why}`);
  }
  console.error(
    `\nThese relationships were ruled, not assumed. A surface nobody links is a surface nobody reads,\n` +
      `and the site said otherwise for four days before anyone noticed. Restore the link or bring the\n` +
      `ruling back for review — do not delete the row to make this pass. Deploy blocked.\n`
  );
  process.exit(1);
}

const checks = PROTECTED.reduce((n, p) => n + p.linkedFrom.length + (p.inLlms ? 1 : 0) + 1, 0) + 2;
console.log(`discoverability OK — ${checks} protected relationship(s) across ${PROTECTED.length} route(s), all hold`);
