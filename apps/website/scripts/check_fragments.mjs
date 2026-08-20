// Internal-fragment integrity check — every `#fragment` the built site links must exist in the
// page it points at, or the build fails.
//
// WHY THIS EXISTS. `#try-a-question` was declared a PERMANENT ANCHOR and carried a source comment
// saying so (styles/tokens.css). It broke anyway — twice: once as `#exhibit-b`, and again in the
// slice-1 homepage rebuild, when the moods widget it named was retired. Ten links on /ladder, a
// page whose thesis is "nothing here asks to be believed", silently pointed at nothing.
//
// A comment is documentation. This is a guard. The rule the repo already lives by — a generated
// surface stays true while a hand-written one rots — applies to link targets too.
//
// SCOPE, deliberately small: it reads `dist/` AFTER the build, so it tests the bytes that ship,
// not the sources that produce them. No Astro internals, no parser, no dependency. Text-scan only.
import { readdir, readFile } from 'node:fs/promises';
import { join, relative, sep } from 'node:path';

const DIST = new URL('../dist/', import.meta.url).pathname;

async function htmlFiles(dir) {
  const out = [];
  for (const e of await readdir(dir, { withFileTypes: true })) {
    const p = join(dir, e.name);
    if (e.isDirectory()) out.push(...(await htmlFiles(p)));
    else if (e.name.endsWith('.html')) out.push(p);
  }
  return out;
}

// dist/foo/index.html -> /foo ; dist/index.html -> / ; dist/foo.html -> /foo
const routeOf = (file) => {
  let r = '/' + relative(DIST, file).split(sep).join('/');
  r = r.replace(/index\.html$/, '').replace(/\.html$/, '');
  return r.length > 1 ? r.replace(/\/$/, '') : '/';
};
const norm = (r) => (r.length > 1 ? r.replace(/\/$/, '') : '/');

const ID_RE = /\bid\s*=\s*"([^"]+)"/g;
// href="...#frag" — internal only: same-page (#x) or root-relative (/path#x).
const HREF_RE = /\bhref\s*=\s*"(#[^"]+|\/[^"]*#[^"]+)"/g;

const files = await htmlFiles(DIST);
const ids = new Map();   // route -> Set(id)
const links = [];        // { fromRoute, targetRoute, frag }

for (const f of files) {
  const html = await readFile(f, 'utf8');
  const route = routeOf(f);
  const set = new Set();
  for (const m of html.matchAll(ID_RE)) set.add(m[1]);
  ids.set(route, set);
  for (const m of html.matchAll(HREF_RE)) {
    const href = m[1];
    const hash = href.indexOf('#');
    const path = href.slice(0, hash);
    const frag = decodeURIComponent(href.slice(hash + 1));
    if (!frag || frag === 'top') continue; // "#" and "#top" are browser-defined
    links.push({ fromRoute: route, targetRoute: path === '' ? route : norm(path), frag });
  }
}

const broken = [];
for (const l of links) {
  const set = ids.get(l.targetRoute);
  if (!set) broken.push({ ...l, why: 'no such page in dist/' });
  else if (!set.has(l.frag)) broken.push({ ...l, why: 'page exists; id does not' });
}

// Report each broken TARGET once, with every page that links it — the target is the fix site.
if (broken.length) {
  const byTarget = new Map();
  for (const b of broken) {
    const k = `${b.targetRoute}#${b.frag}`;
    if (!byTarget.has(k)) byTarget.set(k, { why: b.why, from: new Set() });
    byTarget.get(k).from.add(b.fromRoute);
  }
  console.error(`\nBROKEN INTERNAL FRAGMENTS — ${byTarget.size} target(s), ${broken.length} link(s)\n`);
  for (const [target, v] of [...byTarget].sort()) {
    console.error(`  ${target}`);
    console.error(`      ${v.why}`);
    console.error(`      linked from: ${[...v.from].sort().join(', ')}`);
  }
  console.error(
    `\nA link to a fragment that does not exist is a claim the site cannot keep. Either add the id\n` +
    `at its intended home or repoint the link. Deploy blocked.\n`
  );
  process.exit(1);
}

console.log(`fragments OK — ${links.length} internal fragment link(s) across ${files.length} page(s), all resolve`);
