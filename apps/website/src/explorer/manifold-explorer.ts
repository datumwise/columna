// The Manifold Explorer — a PORTABLE component (CP-3 C-3). See ./README.md for the portability law.
//
// It binds any `describe_manifold` JSON (the CP-3 C-1 shape) and renders a measure-first reference with
// each fact's law / trial / demonstration triad + "copy as query". ZERO site imports. It does NO
// insulation work — it renders what describe hands it, verbatim (C-2 owns the wall; a physical leak is a
// describe bug, never an Explorer bug). Strings marked `COPY:` are DRAFTS pending Huayin's ratification.

// ---- the describe shape it binds (C-1) ---------------------------------------------------------
export interface License { verdict: string; lineages?: string[]; basis?: string; attestation?: string | null; timeless?: boolean }
export interface DescribeManifold {
  contract_version: string;
  manifold_id: string;
  dimensions: { level: string; is_base: boolean }[];
  edges: { frm: string; to: string; lineage: string }[];
  universes: { name: string; base_dimensions: string[]; predicate: string | null; basis: string | null; absence: string; basis_license: License | null }[];
  asserts: { name: string; universe: string; form: any; license: License | null }[];
  hierarchies: { lineage: string; chain: string[]; license: License | null }[];
  measures: { name: string; family: string[]; universe: string }[];
  derived: { name: string; formula: string; resolution_anchor: string | null; denotation_only: boolean; members: Record<string, { declared_lineages: string[]; license: License | null }> }[];
  published_scope: { cut: string[]; blocked_edges: string[][]; cut_by?: any; blocked_by?: any };
}

const esc = (s: any) => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const attr = (s: any) => esc(s).replace(/"/g, '&quot;');

// trial: the adjudicated License verdict as a badge. COPY: verdict labels pending ratification.
const VERDICT_LABEL: Record<string, string> = {
  verified: 'verified', corroborated: 'corroborated', untestable: 'untestable', contradicted: 'contradicted',
};
function badge(lic: License | null | undefined): string {
  if (!lic) return `<span class="mx-badge mx-badge--none" title="unadjudicated (not yet published)">—</span>`;
  const v = lic.verdict;
  const tl = lic.timeless ? ' · timeless' : (lic.attestation ? ` · @${esc(lic.attestation)}` : '');
  return `<span class="mx-badge mx-badge--${esc(v)}" title="${attr((lic.basis || '') + tl)}">${esc(VERDICT_LABEL[v] || v)}</span>`;
}

// demonstration: "copy as query" — a FrameQL a reader can paste. Structural, never invented.
function copyBtn(query: string): string {
  // COPY: button label pending ratification.
  return `<button class="mx-copy" data-q="${attr(query)}" type="button">copy as query</button>`;
}

// triad labels RATIFIED LABELLED (Huayin 2026-07-17): defined as / tested / show me.
function triad(law: string, lic: License | null | undefined, query: string): string {
  return `<div class="mx-triad">
    <div class="mx-law"><span class="mx-label">defined as</span>${law}</div>
    <div class="mx-trial"><span class="mx-label">tested</span>${badge(lic)}</div>
    ${query ? `<div class="mx-demo"><span class="mx-label">show me</span>${copyBtn(query)}</div>` : ''}
  </div>`;
}

// ---- sections (measure-first) ------------------------------------------------------------------
function measureCard(D: DescribeManifold, m: DescribeManifold['measures'][0]): string {
  const law = `<span class="mx-name">${esc(m.name)}</span>
    <span class="mx-meta">universe <b>${esc(m.universe)}</b> · family ${m.family.map((f) => `<code>${esc(f)}</code>`).join(' ')}</span>`;
  // a measure has no license of its own here; the query demonstrates it at its universe's base grain.
  return `<article class="mx-card" data-kind="measure" data-search="${attr(m.name + ' ' + m.universe + ' ' + m.family.join(' '))}">
    ${triad(law, null, `${m.name} @ ${(D.universes.find((u) => u.name === m.universe)?.base_dimensions || []).join(', ')}`)}
  </article>`;
}
function derivedCard(d: DescribeManifold['derived'][0]): string {
  const mem = Object.entries(d.members)
    .map(([name, fm]) => `<span class="mx-member">${esc(name)} ${badge(fm.license)}</span>`).join(' ');
  const law = `<span class="mx-name">${esc(d.name)}</span>
    <span class="mx-meta"><code>${esc(d.formula)}</code>${d.denotation_only ? ' · denotation-only' : ''}${mem ? ' · ' + mem : ''}</span>`;
  const anchor = d.resolution_anchor ? ` @ ${d.resolution_anchor}` : '';
  return `<article class="mx-card" data-kind="derived" data-search="${attr(d.name + ' ' + d.formula)}">
    ${triad(law, null, `${d.name}${anchor}`)}
  </article>`;
}
function universeCard(u: DescribeManifold['universes'][0]): string {
  const basis = u.basis ? `<b>${esc(u.basis)}</b>` : `<em>undeclared</em>`;
  const law = `<span class="mx-name">${esc(u.name)}</span>
    <span class="mx-meta">basis ${basis} · ${esc(u.absence)}${u.predicate ? ` · <code>${esc(u.predicate)}</code>` : ''}
    · grain ${u.base_dimensions.map((d) => `<code>${esc(d)}</code>`).join(' ')}</span>`;
  return `<article class="mx-card" data-kind="universe" data-search="${attr(u.name + ' ' + (u.basis || '') + ' ' + u.base_dimensions.join(' '))}">
    ${triad(law, u.basis_license, '')}
  </article>`;
}
function assertCard(a: DescribeManifold['asserts'][0]): string {
  const f = a.form || {};
  const body = f.kind === 'invariant'
    ? `${esc(f.left)} ${esc(f.op)} ${esc(f.right)} @ ${(f.anchor || []).join(', ')}`
    : `${esc(f.predicate)}`;
  const law = `<span class="mx-name">${esc(a.name)}</span>
    <span class="mx-meta">${esc(f.kind)} · universe <b>${esc(a.universe)}</b> · <code>${body}</code></span>`;
  return `<article class="mx-card" data-kind="assert" data-search="${attr(a.name + ' ' + a.universe)}">
    ${triad(law, a.license, '')}
  </article>`;
}
function hierarchyCard(h: DescribeManifold['hierarchies'][0]): string {
  const law = `<span class="mx-name">${esc(h.lineage)}</span>
    <span class="mx-meta">${h.chain.map((c) => `<code>${esc(c)}</code>`).join(' → ')}</span>`;
  return `<article class="mx-card" data-kind="hierarchy" data-search="${attr(h.lineage + ' ' + h.chain.join(' '))}">
    ${triad(law, h.license, '')}
  </article>`;
}

// COPY: section headings pending ratification.
const SECTIONS: [string, string, (D: DescribeManifold) => string][] = [
  ['measures', 'Measures', (D) => D.measures.map((m) => measureCard(D, m)).join('')],
  ['derived', 'Derived', (D) => D.derived.map(derivedCard).join('')],
  ['universes', 'Universes', (D) => D.universes.map(universeCard).join('')],
  ['asserts', 'Asserts', (D) => D.asserts.map(assertCard).join('')],
  ['hierarchies', 'Hierarchies', (D) => D.hierarchies.map(hierarchyCard).join('')],
];

/** Render the Explorer for a describe JSON. Returns an HTML string. Pure; no side effects, no imports. */
export function renderManifoldExplorer(D: DescribeManifold): string {
  const cut = (D.published_scope?.cut || []);
  const scopeNote = cut.length
    ? `<p class="mx-scope mx-scope--cut">cut: ${cut.map((c) => `<code>${esc(c)}</code>`).join(' ')}</p>`  // COPY
    : `<p class="mx-scope">full scope published</p>`;                                                      // COPY
  const sections = SECTIONS
    .filter(([, , build]) => build(D).length)
    .map(([id, title, build]) => `<section class="mx-section" data-section="${id}">
      <h3 class="mx-h">${esc(title)}</h3>${build(D)}</section>`).join('');
  return `<div class="mx-explorer" data-manifold="${attr(D.manifold_id)}">
    <div class="mx-bar">
      <input class="mx-search" type="search" placeholder="search measures, universes, edges…" aria-label="search the manifold" />
      ${scopeNote}
    </div>
    ${sections}
  </div>`;
}

/** Mount into a container element and wire search + copy-as-query. The ONLY browser coupling; the
 *  site instance calls this. Still zero site imports — `document`/`navigator` are platform, not site. */
export function mountManifoldExplorer(container: HTMLElement, D: DescribeManifold): void {
  container.innerHTML = renderManifoldExplorer(D);
  const search = container.querySelector<HTMLInputElement>('.mx-search');
  const cards = Array.from(container.querySelectorAll<HTMLElement>('.mx-card'));
  search?.addEventListener('input', () => {
    const q = search.value.trim().toLowerCase();
    for (const c of cards) {
      const hay = (c.getAttribute('data-search') || '').toLowerCase();
      c.style.display = !q || hay.includes(q) ? '' : 'none';
    }
    for (const s of Array.from(container.querySelectorAll<HTMLElement>('.mx-section'))) {
      const anyVisible = Array.from(s.querySelectorAll<HTMLElement>('.mx-card')).some((c) => c.style.display !== 'none');
      s.style.display = anyVisible ? '' : 'none';
    }
  });
  container.addEventListener('click', (e) => {
    const btn = (e.target as HTMLElement).closest<HTMLElement>('.mx-copy');
    if (!btn) return;
    const q = btn.getAttribute('data-q') || '';
    navigator.clipboard?.writeText(q);
    const prev = btn.textContent;
    btn.textContent = 'copied';                 // COPY: confirmation label pending ratification
    setTimeout(() => { btn.textContent = prev; }, 1200);
  });
}
