// Exhibit B client. Renders real wire JSON from the recorded transcript (degrade) or, once the
// endpoint is live, from the MCP endpoint. The clarify round-trip mirrors `demo --play`:
// clarify → pick a population → refuse → "see them as separate columns" → disclose.

import {
  initExplorer, renderManifoldPanel, friendlyDisclosure, friendlyReason,
  linkify, classifyFoolInput, renderObjectCard, type ExplorerData,
} from './explorer';

type Wire = any;
interface Data extends ExplorerData {
  meta: any;
  seeded: Record<'clarify' | 'disclose' | 'refuse' | 'serve', { label: string; wire: Wire }>;
  roundtrip: Record<string, Wire>;
  foolIt: { wire: Wire; measureIndex: string[]; placeholder: string; template: string };
  endpoint: string;
}

// module-level handle so the top-level render helpers can reach describe data + governed strings
let D: Data;

const root = document.querySelector<HTMLElement>('.exhibit-b');
if (root) init(root);

function init(root: HTMLElement) {
  const dataEl = root.querySelector<HTMLElement>('[data-exhibit-b]');
  const DATA: Data = JSON.parse(dataEl!.textContent!);
  D = DATA;
  const respEl = root.querySelector<HTMLElement>('[data-response]')!;
  const degradeEl = root.querySelector<HTMLElement>('[data-degrade]');
  const foolForm = root.querySelector<HTMLFormElement>('[data-fool]')!;
  const foolResp = document.createElement('div');
  foolResp.className = 'response fool-response';
  foolForm.querySelector('.fool-hint')!.before(foolResp);

  // Manifold Explorer: render the "what's in this manifold?" panel + wire doorways/glossary/slot.
  const panelBody = root.querySelector<HTMLElement>('[data-manifold-panel]');
  if (panelBody) panelBody.innerHTML = renderManifoldPanel(DATA);
  initExplorer(root, DATA);
  const openObject = (root as any)._openObject as (kind: string, name: string) => void;

  // The free-text fool-it goes LIVE against the read-only demo endpoint (real shipped-package wire).
  // Seeded buttons + the round-trip stay on the build-time transcript (identical, and instant). If a
  // live request fails/times out, that ONE interaction degrades to the captured trap + a stamped note
  // — the site never looks broken and never shows fake data.
  function degradeFool(reason: string) {
    console.warn('[exhibit-b] live fool-it degraded:', reason);
    degradeEl?.removeAttribute('hidden');
    foolForm.querySelector('.fool-row')?.setAttribute('hidden', '');
    foolResp.innerHTML = '';
    foolResp.append(renderCard(DATA.foolIt.wire, { ask: DATA.foolIt.measureIndex, heading: 'captured — asking for a measure that does not exist:' }));
  }

  // --- seeded buttons ---
  root.querySelectorAll<HTMLButtonElement>('.seed-row button').forEach((btn) => {
    btn.addEventListener('click', () => {
      root.querySelectorAll('.seed-row button').forEach((b) => b.removeAttribute('aria-pressed'));
      btn.setAttribute('aria-pressed', 'true');
      respEl.innerHTML = '';
      const id = btn.dataset.seed as keyof Data['seeded'];
      respEl.append(renderCard(DATA.seeded[id].wire, {}));
      if (id === 'clarify') wireRoundtrip(respEl, DATA);
      respEl.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    });
  });

  // --- fool-it (live) ---
  const foolInput = foolForm.querySelector<HTMLInputElement>('#fool-input')!;
  const foolBtn = foolForm.querySelector<HTMLButtonElement>('button[type="submit"]')!;

  foolForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const raw = foolInput.value.trim();
    if (!raw) return;
    const kind = classifyFoolInput(raw, DATA);

    // a bare KNOWN measure name → its describe card (the Explorer's atom), not a served value
    if (kind === 'measure') {
      foolResp.innerHTML = `<p class="pick-note">${esc(DATA.strings.foolIt?.describeIntro || 'Here’s what this measure is:')}</p>`;
      foolResp.append(renderObjectCard('measure', raw, DATA));
      foolResp.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      return;
    }
    // input that looks like a full query → friendly redirect (this box checks names)
    if (kind === 'query') {
      foolResp.innerHTML = `<p class="pick-note">${esc(DATA.strings.foolIt?.queryShapeRedirect || 'That looks like a query — use the buttons above.')}</p>`;
      return;
    }

    // unknown name → the real, honest refusal from the live endpoint + the (tappable) index
    const frameql = DATA.foolIt.template.replace('%s', () => raw);
    foolBtn.disabled = true;
    foolResp.innerHTML = '<p class="pick-note">asking the live endpoint…</p>';
    try {
      const wire = await postQuery(DATA.endpoint, frameql);
      if (wire.contract_version !== '1') throw new Error('unexpected contract');
      foolResp.innerHTML = '';
      foolResp.append(renderCard(wire, { ask: DATA.foolIt.measureIndex, heading: `you asked for “${raw}” — here is what came back over the wire:` }));
      foolResp.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    } catch (err) {
      degradeFool(String(err));
    } finally {
      foolBtn.disabled = false;
    }
  });
}

// POST a Frame-QL query to the read-only demo endpoint; returns the disclosure wire (real JSON).
async function postQuery(endpoint: string, frameql: string, universe: string | null = null): Promise<Wire> {
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), 6000);
  try {
    const res = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify({ frameql, universe }),
      signal: ctrl.signal,
    });
    if (!res.ok) throw new Error(`endpoint ${res.status}`);
    return await res.json();
  } finally {
    clearTimeout(t);
  }
}

// The clarify round-trip: pick → refuse → resolve → disclose (the demo --play arc).
function wireRoundtrip(container: HTMLElement, DATA: Data) {
  const note = document.createElement('p');
  note.className = 'pick-note';
  note.textContent = 'It will not pick for you. You pick.';
  container.append(note);

  const card = container.querySelector('.resp-card')!;
  card.querySelectorAll<HTMLButtonElement>('.alts button').forEach((altBtn) => {
    altBtn.addEventListener('click', () => {
      container.querySelectorAll('.alts button').forEach((b) => b.removeAttribute('aria-pressed'));
      altBtn.setAttribute('aria-pressed', 'true');
      // remove any prior downstream cards
      container.querySelectorAll('[data-downstream]').forEach((n) => n.remove());
      const uni = altBtn.dataset.universe!;
      const refuseWire = DATA.roundtrip[uni];
      const refCard = renderCard(refuseWire, { downstream: true });
      const picked = document.createElement('p');
      picked.className = 'pick-note';
      picked.dataset.downstream = '';
      picked.textContent = 'You picked — and the grammar showed you why that operand can’t live there. Still no guess.';
      container.append(picked, refCard);

      const resolve = document.createElement('button');
      resolve.className = 'resolve-btn';
      resolve.dataset.downstream = '';
      resolve.textContent = 'see them as separate columns →';
      resolve.addEventListener('click', () => {
        resolve.remove();
        const discCard = renderCard(DATA.seeded.disclose.wire, { downstream: true });
        const close = document.createElement('p');
        close.className = 'pick-note';
        close.dataset.downstream = '';
        close.textContent = 'The honest answer isn’t a single rate — it’s both numbers, with the assumption on the record.';
        container.append(discCard, close);
        discCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      });
      container.append(resolve);
      refCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    });
  });
}

interface CardOpts { downstream?: boolean; ask?: string[]; heading?: string }

function renderCard(wire: Wire, opts: CardOpts): HTMLElement {
  const card = document.createElement('div');
  card.className = 'resp-card';
  if (opts.downstream) card.dataset.downstream = '';
  const outcome: string = wire.outcome;

  const parts: string[] = [];
  if (opts.heading) parts.push(`<div class="resp-heading">${esc(opts.heading)}</div>`);
  // header: the mood badge + its one-line reading (friendly, keyed off the code, with doorways)
  parts.push(`<div class="resp-head">${moodBadge(outcome)}<p class="resp-summary">${summaryHTML(wire)}</p></div>`);
  parts.push(renderValues(wire));

  // disclosures: material inline (severity-styled); immaterial behind the audit trail
  const { material, immaterial } = collectDisclosures(wire);
  if (material.length) {
    parts.push(`<div class="disc-section"><div class="vlabel">disclosure — travels with the number</div>${material.map((m) => renderDisclosure(m, wire)).join('')}</div>`);
  }

  card.innerHTML = parts.join('');

  // alternatives (clarify/refuse) as buttons
  const alts = firstAlternatives(wire);
  if (alts.length && outcome === 'clarify') {
    const label = document.createElement('div');
    label.className = 'vlabel';
    label.textContent = 'tap the reading you meant →';
    card.append(label);
    const box = document.createElement('div');
    box.className = 'alts';
    alts.forEach((a: any) => {
      const u = a.apply?.universe;
      if (!u) return;
      const b = document.createElement('button');
      b.type = 'button';
      b.dataset.universe = u;
      b.textContent = a.description || a.token;
      box.append(b);
    });
    card.append(box);
  }

  // the ASK (fool-it): list what exists, as tappable-looking tags (not a jammed list)
  if (opts.ask?.length) {
    const ask = document.createElement('div');
    ask.className = 'resp-index';
    ask.innerHTML = `<div class="vlabel">the ${opts.ask.length} measures this manifold actually has — tap to describe:</div>` +
      `<div class="index-tags">${opts.ask.map((m) => `<button type="button" class="door tag" data-door-kind="measure" data-door="${esc(m)}">${esc(m)}</button>`).join('')}</div>`;
    card.append(ask);
  }

  // immaterial audit trail
  if (immaterial.length) {
    const toggle = document.createElement('button');
    toggle.className = 'audit-toggle';
    toggle.textContent = `audit trail (${immaterial.length})`;
    const body = document.createElement('div');
    body.className = 'audit-body';
    body.hidden = true;
    body.innerHTML = immaterial.map((m) => renderDisclosure(m, wire)).join('');
    toggle.addEventListener('click', () => { body.hidden = !body.hidden; });
    card.append(toggle, body);
  }

  // the wire pane — the JSON is the exhibit
  const pane = document.createElement('details');
  pane.className = 'wire-pane';
  pane.innerHTML = `<summary>the wire — the actual response JSON</summary><pre>${highlight(wire)}</pre>`;
  card.append(pane);
  return card;
}

function moodBadge(outcome: string): string {
  if (outcome === 'error') return `<span class="mood-badge mood-error">error — not a mood (plumbing)</span>`;
  return `<span class="mood-badge mood-${esc(outcome)}">${esc(outcome)}</span>`;
}

// One-line reading of a response. serve/disclose are fixed prose; clarify/refuse/error use the
// GOVERNED friendly string keyed off the reason code, with doorways/glossary and an engine-detail
// toggle carrying the verbatim wire detail.
function summaryHTML(wire: Wire): string {
  const o = wire.outcome;
  if (o === 'serve') return esc('Fully specified — it just answers.');
  if (o === 'disclose') return esc('It answers — and the assumption rides with the number.');
  const col = firstNoResultCol(wire);
  if (col) {
    const fr = friendlyReason(col, wire, D);
    if (fr.friendly) return linkify(fr.friendly, D) + engineDetailToggle(fr.detail);
    if (fr.detail) return linkify(fr.detail, D);
  }
  // frame-level syntax error carries its detail on wire.error
  if (wire.error?.detail) return esc(wire.error.detail);
  if (o === 'error') return esc('Not a valid query.');
  return esc(o === 'clarify' ? 'Several legitimate readings — which did you mean?' : 'Not defined over this data.');
}

function firstNoResultCol(wire: Wire): any | null {
  for (const c of wire.columns || []) {
    if (c.no_result) return c;
  }
  return null;
}

// a collapsed "engine detail ▸" carrying the engine's verbatim detail (correctness stays visible)
function engineDetailToggle(detail: string): string {
  if (!detail) return '';
  return `<details class="engine-detail"><summary>engine detail</summary><div class="engine-detail-body">${esc(detail)}</div></details>`;
}

function firstAlternatives(wire: Wire): any[] {
  for (const c of wire.columns || []) {
    if (c.no_result?.alternatives?.length) return c.no_result.alternatives;
  }
  return [];
}

function collectDisclosures(wire: Wire): { material: any[]; immaterial: any[] } {
  const all: any[] = [];
  (wire.frame?.disclosures || []).forEach((d: any) => all.push(d));
  (wire.columns || []).forEach((c: any) => (c.disclosures || []).forEach((d: any) => all.push(d)));
  return {
    material: all.filter((d) => d.materiality === 'material'),
    immaterial: all.filter((d) => d.materiality !== 'material'),
  };
}

function renderDisclosure(d: any, wire: Wire): string {
  const sev = d.severity === 'critical' ? 'critical' : d.severity === 'caution' ? 'caution' : 'info';
  const codeline = `<span class="disc-code">${esc(d.code)} · ${esc(d.materiality)} · ${esc(d.severity)}</span>`;
  const { friendly, detail } = friendlyDisclosure(d, wire, D);
  const bodyHTML = friendly ? linkify(friendly, D) + engineDetailToggle(detail) : esc(detail || '');
  return `<div class="disc disc-${sev}">${codeline}<div>${bodyHTML}</div></div>`;
}

// ordered anchor-dimension keys present on a column's value rows (everything except `value`)
function dimKeys(col: any): string[] {
  const first = (col.values || [])[0] || {};
  return Object.keys(first).filter((k) => k !== 'value');
}
function colIsNum(col: any): boolean {
  return (col.values || []).every((v: any) => typeof v.value === 'number');
}
function cell(val: any, num: boolean): string {
  return `<td${num ? ' class="num"' : ''}>${esc(num ? fmt(val) : String(val))}</td>`;
}

// Render column values as a real HTML table. When several columns share the same anchor
// dimensions, pivot them into ONE side-by-side table (the "revenue and inventory, by region" case).
function renderValues(wire: Wire): string {
  const cols = (wire.columns || []).filter((c: any) => (c.values || []).length);
  if (!cols.length) return '';

  const dims = dimKeys(cols[0]);
  const sameDims = dims.length > 0 && cols.every((c: any) => {
    const d = dimKeys(c);
    return d.length === dims.length && d.every((k, i) => k === dims[i]);
  });

  if (sameDims && cols.length > 1) {
    const rowMap = new Map<string, any>();
    const order: string[] = [];
    for (const c of cols) for (const v of c.values) {
      const key = dims.map((k) => String(v[k])).join('');
      if (!rowMap.has(key)) { rowMap.set(key, { _dims: dims.map((k) => v[k]) }); order.push(key); }
      rowMap.get(key)[c.name] = v.value;
    }
    const nums = cols.map(colIsNum);
    const head = `<tr>${dims.map((k) => `<th>${esc(k)}</th>`).join('')}` +
      cols.map((c: any, i: number) => `<th${nums[i] ? ' class="num"' : ''}>${esc(c.name)}</th>`).join('') + '</tr>';
    const body = order.map((key) => {
      const r = rowMap.get(key);
      const dcells = r._dims.map((d: any) => `<td>${esc(d)}</td>`).join('');
      const mcells = cols.map((c: any, i: number) =>
        c.name in r ? cell(r[c.name], nums[i]) : `<td${nums[i] ? ' class="num"' : ''}><span class="nil">—</span></td>`).join('');
      return `<tr>${dcells}${mcells}</tr>`;
    }).join('');
    const caption = cols.map((c: any) => `${c.name}${c.population ? ` · ${c.population}` : ''}`).join('   ·   ');
    return `<div class="resp-values"><div class="vlabel">result — ${linkify(caption, D)}</div>` +
      `<table class="wire-table"><thead>${head}</thead><tbody>${body}</tbody></table></div>`;
  }

  // one table per column
  return cols.map((c: any) => {
    const d = dimKeys(c);
    const num = colIsNum(c);
    const head = `<tr>${d.map((k) => `<th>${esc(k)}</th>`).join('')}<th${num ? ' class="num"' : ''}>value</th></tr>`;
    const body = c.values.map((v: any) =>
      `<tr>${d.map((k) => `<td>${esc(v[k])}</td>`).join('')}${cell(v.value, num)}</tr>`).join('');
    return `<div class="resp-values"><div class="vlabel">result — ${linkify(`${c.name}${c.population ? ` · ${c.population}` : ''}`, D)}</div>` +
      `<table class="wire-table"><thead>${head}</thead><tbody>${body}</tbody></table></div>`;
  }).join('');
}

function fmt(v: any): string {
  if (typeof v === 'number') return Number.isInteger(v) ? v.toLocaleString('en-US') : v.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  return String(v);
}

function esc(s: any): string {
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function highlight(obj: any): string {
  let json = JSON.stringify(obj, null, 2);
  json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  json = json.replace(/"([^"\\]*(?:\\.[^"\\]*)*)"(\s*:)/g, '<span class="k">"$1"</span>$2');
  json = json.replace(/: "([^"\\]*(?:\\.[^"\\]*)*)"/g, ': <span class="s">"$1"</span>');
  return json;
}
