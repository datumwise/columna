// The Manifold Explorer (tier 1) — client-side rendering of captured describe wire.
//
// Everything here renders from DATA.describe (captured by gen_transcript.py running the shipped
// package) plus DATA.strings (the GOVERNED communicative layer, wire_strings.json). No engine
// prose is ever the source of a friendly string: placeholders are filled from STRUCTURAL wire
// fields (column.population, frame.universe, the column's measure name, the family members). The
// engine's verbatim detail is always available one toggle away.

type Any = any;

const esc = (s: Any) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

export interface ExplorerData {
  describe: {
    manifold: { id: string; universes: Any[]; edges: Any[]; measure_index: string[] };
    measures: Record<string, Any>;
  };
  strings: Any;
}

// ---- structural lookups -------------------------------------------------------------------
function measureNames(D: ExplorerData): Set<string> { return new Set(Object.keys(D.describe.measures)); }
function universeNames(D: ExplorerData): Set<string> { return new Set(D.describe.manifold.universes.map((u) => u.name)); }
function dimLabel(D: ExplorerData, dim: string): string { return D.strings.dimLabels?.[dim] || dim; }
function uniShort(D: ExplorerData, u: string): string { return D.strings.universeShort?.[u] || u; }

// ---- friendly strings (keyed to CODE, templated from structural fields) --------------------
function fill(tpl: string, vars: Record<string, string>): string {
  return tpl.replace(/\{(\w+)\}/g, (_, k) => (k in vars ? vars[k] : `{${k}}`));
}

// distinct populations actually present on the frame's columns (structural, not prose)
function framePopulations(wire: Any): string[] {
  const seen: string[] = [];
  for (const c of wire.columns || []) {
    if (c.population && !seen.includes(c.population)) seen.push(c.population);
  }
  return seen;
}

export function friendlyDisclosure(disc: Any, wire: Any, D: ExplorerData): { friendly: string | null; detail: string } {
  const entry = D.strings.disclosureCodes?.[disc.code];
  const detail = disc.detail || '';
  if (!entry) return { friendly: null, detail };
  const pops = framePopulations(wire);
  const vars = {
    populations: pops.map((p) => `${p} (${uniShort(D, p)})`).join(' and '),
  };
  return { friendly: fill(entry.friendly, vars), detail };
}

// friendly reason for a column's no_result, keyed to reason code + structural context
export function friendlyReason(col: Any, wire: Any, D: ExplorerData): { friendly: string | null; detail: string } {
  const nr = col.no_result || {};
  const detail = nr.detail || '';
  const entry = D.strings.reasonCodes?.[nr.reason];
  if (!entry) return { friendly: null, detail };
  const measure = col.name;
  const home = D.describe.measures[measure]?.universe;
  const members = D.describe.measures[measure]?.family_members || [];
  const vars: Record<string, string> = {
    measure,
    pinned: wire.frame?.universe ? `${wire.frame.universe} (${uniShort(D, wire.frame.universe)})` : 'that population',
    home: home ? `${home} (${uniShort(D, home)})` : 'another population',
    members: members.join(' or '),
    example: members.length ? `${measure}.${members[members.length - 1]}` : measure,
  };
  return { friendly: fill(entry.friendly, vars), detail };
}

// ---- linkify: turn known object names + house terms into doorways / glossary spans ----------
export function linkify(text: string, D: ExplorerData): string {
  const measures = measureNames(D);
  const universes = universeNames(D);
  const glossary = D.strings.glossary || {};
  const aliases = D.strings.glossaryAliases || {};
  // match identifiers, optionally single-quoted (so ['store_days', 'transactions'] resolves)
  return esc(text).replace(/'?([A-Za-z_][A-Za-z0-9_]*)'?/g, (m, word) => {
    if (measures.has(word)) return door('measure', word);
    if (universes.has(word)) return door('universe', word);
    const lw = word.toLowerCase();
    const gkey = glossary[lw] ? lw : aliases[lw];
    if (gkey && glossary[gkey]) return `<span class="gloss" data-term="${esc(gkey)}" tabindex="0">${esc(word)}</span>`;
    return m;
  });
}
function door(kind: string, name: string): string {
  return `<button type="button" class="door" data-door-kind="${esc(kind)}" data-door="${esc(name)}">${esc(name)}</button>`;
}

// ---- object cards (a measure card or a universe card) --------------------------------------
export function renderObjectCard(kind: string, name: string, D: ExplorerData): HTMLElement {
  return kind === 'universe' ? universeCard(name, D) : measureCard(name, D);
}

function measureCard(name: string, D: ExplorerData): HTMLElement {
  const m = D.describe.measures[name];
  const card = document.createElement('div');
  card.className = 'obj-card';
  if (!m) { card.innerHTML = `<div class="obj-head"><span class="obj-kind">measure</span> <strong>${esc(name)}</strong></div><p class="obj-note">not in this manifold’s index.</p>`; return card; }
  const uni = m.universe;
  const parts: string[] = [];
  parts.push(`<div class="obj-head"><span class="obj-kind">measure</span> <strong>${esc(name)}</strong>` +
    `<button class="obj-close" aria-label="close" data-close>✕</button></div>`);
  // v0.2: family members ARE reducers — label them as the operators they are
  parts.push(`<div class="obj-meta">` +
    `<span><em>reducers</em> ${esc(m.family_members.join(' · '))}</span>` +
    `<span><em>${gl('universe', 'universe', D)}</em> ${door('universe', uni)}</span>` +
    `<span><em>attested</em> ${esc(m.provenance)}</span></div>`);

  // per-member legal cone (ruling e-2)
  for (const member of m.family_members) {
    const info = m.members[member];
    const askable = info.may_be_asked_at.map((d: string) => `<span class="grain">${esc(dimLabel(D, d))}</span>`).join(' ');
    parts.push(`<div class="cone"><div class="cone-h">${esc(name)}.${esc(member)} — ${gl('may be asked at', 'anchor', D)}:</div><div class="grains">${askable}</div>`);
    if (info.barred.length) {
      const bars = info.barred.map((b: Any) => {
        const reason = barredReason(name, member, b.lineage, D);
        const lin = D.strings.lineageLabels?.[b.lineage] || b.lineage;
        return `<div class="barred"><span class="barred-x">barred</span> rolling up over ${esc(lin)} — <span class="barred-why">${esc(reason)}</span></div>`;
      }).join('');
      parts.push(bars);
    }
    parts.push('</div>');
  }
  parts.push(onePagerLink(D));
  card.innerHTML = parts.join('');
  return card;
}

function universeCard(name: string, D: ExplorerData): HTMLElement {
  const u = D.describe.manifold.universes.find((x) => x.name === name);
  const card = document.createElement('div');
  card.className = 'obj-card';
  const oneLiner = D.strings.universes?.[name] || '';
  const inThis = Object.values(D.describe.measures).filter((m: Any) => m.universe === name).map((m: Any) => m.name);
  const parts: string[] = [];
  parts.push(`<div class="obj-head"><span class="obj-kind">${gl('population', 'universe', D)}</span> <strong>${esc(name)}</strong>` +
    `<button class="obj-close" aria-label="close" data-close>✕</button></div>`);
  if (oneLiner) parts.push(`<p class="obj-note">${esc(oneLiner)}</p>`);
  if (u) {
    parts.push(`<div class="obj-meta"><span><em>${gl('anchor', 'anchor', D)} grain</em> ${u.base_dimensions.map((d: string) => `<span class="grain">${esc(dimLabel(D, d))}</span>`).join(' ')}</span>`);
    if (u.predicate) parts.push(`<span><em>only where</em> <code>${esc(u.predicate)}</code></span>`);
    parts.push(`</div>`);
  }
  if (inThis.length) parts.push(`<div class="cone"><div class="cone-h">measures in this population:</div><div class="grains">${inThis.map((n) => door('measure', n)).join(' ')}</div></div>`);
  parts.push(onePagerLink(D));
  card.innerHTML = parts.join('');
  return card;
}

function barredReason(measure: string, member: string, lineage: string, D: ExplorerData): string {
  const b = D.strings.barredReasons || {};
  return b[`${measure}.${member}.${lineage}`] || b._fallbackByLineage?.[lineage] || 'this reduction isn’t valid over that rollup.';
}

// wrap a literal term in a glossary span (used for card field labels)
function gl(label: string, term: string, D: ExplorerData): string {
  if (!D.strings.glossary?.[term]) return esc(label);
  return `<span class="gloss" data-term="${esc(term)}" tabindex="0">${esc(label)}</span>`;
}

function onePagerLink(D: ExplorerData): string {
  const op = D.strings.onePager || {};
  if (!op.route) return '';
  return `<a class="onepager-link" href="${esc(op.route)}">${esc(op.linkText || 'how to read the wire →')}</a>`;
}

// ---- the "what's in this manifold?" panel content (v0.2: THREE sections) --------------------
export function renderManifoldPanel(D: ExplorerData): string {
  const unis = D.describe.manifold.universes.map((u) =>
    `<div class="mf-uni">${door('universe', u.name)}<span class="mf-uni-desc">${esc(D.strings.universes?.[u.name] || '')}</span></div>`).join('');
  const measures = D.describe.manifold.measure_index.map((n) => door('measure', n)).join(' ');
  return `<div class="mf-block"><div class="vlabel">the ${D.describe.manifold.universes.length} populations</div>${unis}</div>` +
    `<div class="mf-block"><div class="vlabel">the ${D.describe.manifold.measure_index.length} measures — tap to describe</div><div class="index-tags">${measures}</div></div>` +
    renderDerivations(D);
}

// derived dimensions / rollups — the lattice-builders (v0.2). Grouped by (from-dim, lineage),
// derived structurally from the manifold edges; the phrasing lives in the reviewed strings file.
function renderDerivations(D: ExplorerData): string {
  const groups = new Map<string, { frm: string; lineage: string; targets: string[] }>();
  for (const e of D.describe.manifold.edges) {
    const key = `${e.frm}|${e.lineage}`;
    if (!groups.has(key)) groups.set(key, { frm: e.frm, lineage: e.lineage, targets: [] });
    groups.get(key)!.targets.push(e.to);
  }
  if (!groups.size) return '';
  const dv = D.strings.derivations || {};
  const rows = [...groups.values()].map((g) => {
    const line = fill(dv.rollup || '{frm} rolls up to {targets} — via {lineage}', {
      frm: dimLabel(D, g.frm),
      targets: g.targets.map((t) => dimLabel(D, t)).join(' / '),
      lineage: g.lineage,
    });
    // make the from-dim + targets tappable is out of scope; keep the lineage name as a code token
    return `<div class="mf-deriv">${esc(line)}</div>`;
  }).join('');
  return `<div class="mf-block"><div class="vlabel">${esc(dv.sectionLabel || 'derived dimensions & rollups')}</div>${rows}</div>`;
}

// ---- glossary tooltip (one shared floating element) -----------------------------------------
let tipEl: HTMLElement | null = null;
function tip(D: ExplorerData): HTMLElement {
  if (!tipEl) {
    tipEl = document.createElement('div');
    tipEl.className = 'gloss-tip';
    tipEl.hidden = true;
    document.body.append(tipEl);
  }
  return tipEl;
}
function showTip(target: HTMLElement, D: ExplorerData) {
  const term = target.dataset.term!;
  const def = D.strings.glossary?.[term];
  if (!def) return;
  const t = tip(D);
  const op = D.strings.onePager || {};
  t.innerHTML = `<strong>${esc(term)}</strong> — ${esc(def)}` +
    (op.route ? ` <a href="${esc(op.route)}">${esc(op.linkText || 'more →')}</a>` : '');
  t.hidden = false;
  const r = target.getBoundingClientRect();
  const tr = t.getBoundingClientRect();
  let left = r.left + window.scrollX;
  left = Math.min(left, window.scrollX + document.documentElement.clientWidth - tr.width - 12);
  t.style.left = `${Math.max(window.scrollX + 8, left)}px`;
  t.style.top = `${r.bottom + window.scrollY + 6}px`;
}
function hideTip() { if (tipEl) tipEl.hidden = true; }

// ---- wiring: doorways (delegated), glossary (hover/focus/tap), shared card slot -------------
export function initExplorer(root: HTMLElement, D: ExplorerData) {
  const slot = root.querySelector<HTMLElement>('[data-explorer-slot]');

  function openObject(kind: string, name: string) {
    if (!slot) return;
    slot.innerHTML = '';
    slot.append(renderObjectCard(kind, name, D));
    slot.hidden = false;
    slot.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  root.addEventListener('click', (e) => {
    const el = e.target as HTMLElement;
    const door = el.closest<HTMLElement>('.door');
    if (door) { e.preventDefault(); openObject(door.dataset.doorKind!, door.dataset.door!); return; }
    if (el.closest('[data-close]')) {
      const owned = el.closest<HTMLElement>('.obj-card');
      owned?.remove();
      if (slot && !slot.querySelector('.obj-card')) { slot.hidden = true; slot.innerHTML = ''; }
      return;
    }
    const gloss = el.closest<HTMLElement>('.gloss');
    if (gloss) { showTip(gloss, D); return; }  // tap-to-show on touch
  });

  // hover/focus glossary
  root.addEventListener('mouseover', (e) => {
    const g = (e.target as HTMLElement).closest?.<HTMLElement>('.gloss');
    if (g) showTip(g, D);
  });
  root.addEventListener('mouseout', (e) => { if ((e.target as HTMLElement).closest?.('.gloss')) hideTip(); });
  root.addEventListener('focusin', (e) => { const g = (e.target as HTMLElement).closest?.<HTMLElement>('.gloss'); if (g) showTip(g, D); });
  root.addEventListener('focusout', hideTip);
  window.addEventListener('scroll', hideTip, { passive: true });

  // expose the opener for exhibit-b.ts (fool-it bare-name → describe card)
  (root as Any)._openObject = openObject;
}

// classify a fool-it input: 'measure' (bare known name) | 'query' (looks like a query) | 'unknown'
export function classifyFoolInput(raw: string, D: ExplorerData): 'measure' | 'query' | 'unknown' {
  const s = raw.trim();
  if (/\s|@|\bby\b/i.test(s)) return 'query';
  if (measureNames(D).has(s)) return 'measure';
  return 'unknown';
}
