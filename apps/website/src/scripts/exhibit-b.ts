// Exhibit B client. Renders real wire JSON from the recorded transcript (degrade) or, once the
// endpoint is live, from the MCP endpoint. The clarify round-trip mirrors `demo --play`:
// clarify → pick a population → refuse → "see them as separate columns" → disclose.

type Wire = any;
interface Data {
  meta: any;
  seeded: Record<'clarify' | 'disclose' | 'refuse' | 'serve', { label: string; wire: Wire }>;
  roundtrip: Record<string, Wire>;
  foolIt: { wire: Wire; measureIndex: string[]; placeholder: string; template: string };
}

const root = document.querySelector<HTMLElement>('.exhibit-b');
if (root) init(root);

function init(root: HTMLElement) {
  const dataEl = root.querySelector<HTMLElement>('[data-exhibit-b]');
  const DATA: Data = JSON.parse(dataEl!.textContent!);
  const respEl = root.querySelector<HTMLElement>('[data-response]')!;
  const degradeEl = root.querySelector<HTMLElement>('[data-degrade]');
  const foolForm = root.querySelector<HTMLFormElement>('[data-fool]')!;

  // Live path activates when the Fly endpoint is deployed; until then we degrade to the recorded
  // transcript (a first-class requirement — the site never looks broken). No fake data either way.
  const LIVE = false;
  if (!LIVE) {
    degradeEl?.removeAttribute('hidden');
    // per the exhibit contract, the free-text input is live-only; in degrade show the captured trap
    foolForm.querySelector('.fool-row')?.setAttribute('hidden', '');
    const captured = document.createElement('div');
    captured.className = 'response';
    captured.append(renderCard(DATA.foolIt.wire, { ask: DATA.foolIt.measureIndex, heading: 'captured — asking for a measure that does not exist:' }));
    foolForm.querySelector('.fool-hint')!.before(captured);
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

  // --- fool-it (live only) ---
  foolForm.addEventListener('submit', (e) => {
    e.preventDefault();
    // no-op in degrade; live path issues the query and renders whatever mood returns
  });
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
  if (opts.heading) parts.push(`<div class="disc-code">${esc(opts.heading)}</div>`);
  parts.push(moodBadge(outcome));
  parts.push(`<p class="resp-summary">${esc(summaryFor(wire))}</p>`);
  parts.push(renderValues(wire));

  // disclosures: material inline (severity-styled); immaterial behind the audit trail
  const { material, immaterial } = collectDisclosures(wire);
  material.forEach((d) => parts.push(renderDisclosure(d)));

  card.innerHTML = parts.join('');

  // alternatives (clarify/refuse) as buttons
  const alts = firstAlternatives(wire);
  if (alts.length && outcome === 'clarify') {
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

  // the ASK (fool-it): list what exists
  if (opts.ask?.length) {
    const ask = document.createElement('div');
    ask.className = 'resp-values';
    ask.innerHTML = `<div class="disc-code">here is what this manifold has:</div>` +
      opts.ask.map((m) => `<div class="vrow"><span>${esc(m)}</span><span></span></div>`).join('');
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
    body.innerHTML = immaterial.map(renderDisclosure).join('');
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

function summaryFor(wire: Wire): string {
  const o = wire.outcome;
  if (o === 'serve') return 'Fully specified — it just answers.';
  if (o === 'disclose') return 'It answers — and the assumption rides with the number.';
  if (o === 'error') return firstDetail(wire) || 'Not a valid query.';
  // clarify / refuse carry their reason on the wire
  return firstDetail(wire) || (o === 'clarify' ? 'Several legitimate readings — which did you mean?' : 'Not defined over this data.');
}

function firstDetail(wire: Wire): string | null {
  for (const c of wire.columns || []) {
    if (c.no_result?.detail) return c.no_result.detail;
  }
  return null;
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

function renderDisclosure(d: any): string {
  const sev = d.severity === 'critical' ? 'critical' : d.severity === 'caution' ? 'caution' : 'info';
  return `<div class="disc disc-${sev}"><span class="disc-code">${esc(d.code)} · ${esc(d.materiality)} · ${esc(d.severity)}</span><div>${esc(d.detail || '')}</div></div>`;
}

function renderValues(wire: Wire): string {
  const cols = (wire.columns || []).filter((c: any) => (c.values || []).length);
  if (!cols.length) return '';
  return cols.map((c: any) => {
    const rows = c.values.map((v: any) => {
      const label = Object.keys(v).filter((k) => k !== 'value').map((k) => v[k]).join(' · ');
      return `<div class="vrow"><span>${esc(label)}</span><span>${esc(fmt(v.value))}</span></div>`;
    }).join('');
    return `<div class="resp-values"><div class="disc-code">${esc(c.name)}${c.population ? ' · ' + esc(c.population) : ''}</div>${rows}</div>`;
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
