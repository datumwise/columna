"""The human review screen. One self-contained page, served by the service, token-gated.

WHY IT LIVES HERE AND NOT ON THE WEBSITE. apps/website is `output: 'static'` and ships through the
gated shipped-coherent pipeline that guards datumwise's publication claims. A screen whose whole
purpose is to WRITE publication state does not belong inside that pipeline; it belongs next to the
database it writes. Same reasoning as the service itself (see app.py).

It is deliberately one string. The review surface has one reader, needs no build step, and must keep
working when nothing else does — a broken asset pipeline should never be the reason an answer cannot
be un-published.
"""

REVIEW_PAGE = """<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>Ask review — datumwise</title>
<style>
  :root { --ink:#16181d; --dim:#5b6472; --line:#dfe3ea; --bg:#fbfcfd; --warn:#8a5a00;
          --warnbg:#fff8e6; --ok:#1c6b3f; --okbg:#eefaf2; --bad:#8c2b2b; --badbg:#fdeeee; }
  * { box-sizing:border-box }
  body { margin:0; font:15px/1.6 ui-sans-serif,-apple-system,"Segoe UI",Roboto,sans-serif;
         color:var(--ink); background:var(--bg) }
  header { padding:14px 20px; border-bottom:1px solid var(--line); background:#fff;
           display:flex; gap:14px; align-items:baseline; position:sticky; top:0; z-index:5 }
  h1 { font-size:15px; margin:0; font-weight:650; letter-spacing:-0.01em }
  .muted { color:var(--dim); font-size:13px }
  main { display:grid; grid-template-columns:340px 1fr; min-height:calc(100vh - 52px) }
  #queue { border-right:1px solid var(--line); background:#fff; overflow:auto }
  .cand { padding:12px 16px; border-bottom:1px solid var(--line); cursor:pointer }
  .cand:hover { background:#f5f7fa } .cand.sel { background:#eef3fb }
  .cand b { font-weight:600; display:block; font-size:14px }
  #detail { padding:22px 26px; max-width:900px }
  .notice { border:1px solid #e6d9a8; background:var(--warnbg); color:var(--warn);
            padding:9px 12px; border-radius:7px; font-size:13px; margin:0 0 16px }
  .box { background:#fff; border:1px solid var(--line); border-radius:9px; padding:16px;
         margin:0 0 16px; white-space:pre-wrap }
  h2 { font-size:12px; text-transform:uppercase; letter-spacing:.07em; color:var(--dim);
       margin:22px 0 8px; font-weight:650 }
  .src { font-size:13px; border-bottom:1px dotted var(--line); padding:6px 0 }
  .lay { display:inline-block; font-size:11px; padding:1px 6px; border-radius:4px;
         background:#eef1f6; color:#41506b; margin-right:6px; font-weight:600 }
  .lay.core { background:#e6f4ec; color:#1c6b3f }
  .lay.ext { background:#f3ecfa; color:#5b3a86 }
  .verdict { padding:12px 14px; border-radius:8px; margin:0 0 14px; font-size:14px }
  .APPROVE { background:var(--okbg); border:1px solid #bfe4cf; color:var(--ok) }
  .REVISE { background:var(--warnbg); border:1px solid #e6d9a8; color:var(--warn) }
  .DO_NOT_PUBLISH { background:var(--badbg); border:1px solid #edc4c4; color:var(--bad) }
  .find { font-size:13px; padding:3px 0 } .find .no { color:var(--bad); font-weight:600 }
  .find .yes { color:var(--ok) }
  .qf { font-size:13px; padding:7px 0; border-bottom:1px dotted var(--line) }
  .qf:last-child { border-bottom:0 }
  .qf .v { display:inline-block; font-size:11px; font-weight:700; padding:1px 6px;
           border-radius:4px; letter-spacing:.03em }
  .qf .v.match { background:var(--okbg); color:var(--ok) }
  .qf .v.nomatch { background:var(--badbg); color:var(--bad) }
  .qf .v.unknown { background:var(--warnbg); color:var(--warn) }
  .qf q { display:block; margin:4px 0 2px; font-style:italic }
  .qf .frag { color:var(--dim); font-size:12px; margin-left:14px }
  details.assent { margin-top:8px } details.assent summary { cursor:pointer; color:var(--dim);
    font-size:12px } details.assent pre { white-space:pre-wrap; font:12px/1.55 ui-monospace,
    SFMono-Regular,Menlo,monospace; background:#f7f9fb; border:1px solid var(--line);
    border-radius:7px; padding:10px; margin:8px 0 0 }
  textarea { width:100%; min-height:260px; font:14px/1.6 ui-monospace,SFMono-Regular,Menlo,monospace;
             padding:12px; border:1px solid var(--line); border-radius:8px; background:#fff }
  button { font:inherit; padding:8px 14px; border-radius:7px; border:1px solid var(--line);
           background:#fff; cursor:pointer }
  button.primary { background:var(--ink); color:#fff; border-color:var(--ink) }
  button.danger { color:var(--bad); border-color:#edc4c4 }
  button:disabled { opacity:.5; cursor:default }
  .row { display:flex; gap:10px; align-items:center; flex-wrap:wrap; margin-top:12px }
  input[type=text] { font:inherit; padding:7px 10px; border:1px solid var(--line);
                     border-radius:7px; background:#fff }
  #gate { padding:40px; max-width:460px }
</style></head><body>
<div id="gate">
  <h1>Ask review</h1>
  <p class="muted">This surface publishes under datumwise's name. Paste the review token.</p>
  <div class="row"><input type="text" id="tok" placeholder="review token" style="flex:1">
    <button class="primary" onclick="saveTok()">Enter</button></div>
  <p class="muted" id="gateerr"></p>
</div>
<div id="app" hidden>
<header><h1>Ask review</h1><span class="muted" id="count"></span>
  <span style="flex:1"></span>
  <input type="text" id="who" placeholder="your name" style="width:150px">
  <button onclick="logout()">Lock</button></header>
<main><div id="queue"></div><div id="detail"><p class="muted">Select a candidate.</p></div></main>
</div>
<script>
const K='ask_review_token';
// A token may arrive in the URL FRAGMENT (#tok=...), never the query string. A fragment is not
// sent to the server, so it cannot land in an access log or a proxy trace; the query string would
// land in both. It is stripped from the address bar immediately, and the page is already served
// with Referrer-Policy: no-referrer so it cannot leak sideways either.
let TOK=sessionStorage.getItem(K)||'', ITEMS=[], CUR=null;
let DEEP=null;
if (location.hash.length > 1) {
  const h = new URLSearchParams(location.hash.slice(1));
  if (h.get('tok')) { TOK = h.get('tok'); sessionStorage.setItem(K, TOK); }
  DEEP = h.get('id');                       // deep-link straight to one candidate
  history.replaceState(null, '', location.pathname);
}
const $=id=>document.getElementById(id);
const esc=s=>(s||'').replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
function saveTok(){ TOK=$('tok').value.trim(); sessionStorage.setItem(K,TOK); boot(); }
function logout(){ sessionStorage.removeItem(K); location.reload(); }
async function api(path,opts){
  const o=Object.assign({headers:{'Authorization':'Bearer '+TOK,'Content-Type':'application/json'}},opts||{});
  const r=await fetch(path,o);
  if(!r.ok) throw new Error((await r.json().catch(()=>({}))).error||('HTTP '+r.status));
  return r.json();
}
async function boot(){
  if(!TOK) return;
  try { const d=await api('/review/queue'); ITEMS=d.items;
        $('gate').hidden=true; $('app').hidden=false;
        $('who').value=localStorage.getItem('ask_reviewer')||''; renderQueue();
        if (DEEP) { const i=ITEMS.findIndex(x=>x.id===DEEP); if(i>=0) await open_(i); } }
  catch(e){ $('gateerr').textContent=String(e.message||e); }
}
function renderQueue(){
  $('count').textContent=ITEMS.length+' awaiting review';
  $('queue').innerHTML=ITEMS.map((it,i)=>
    `<div class="cand${CUR&&CUR.id===it.id?' sel':''}" onclick="open_(${i})"><b>${esc(it.question)}</b>
     <span class="muted">${it.review?it.review.disposition:'not yet reviewed'} ·
     ${(it.sources||[]).length} sources</span></div>`).join('')
    || '<p class="muted" style="padding:16px">Queue is empty.</p>';
}
async function open_(i){ CUR=await api('/review/item/'+ITEMS[i].id); renderQueue(); renderDetail(); }
// QUOTE VERIFICATION, RENDERED FOR THE HUMAN (CG2 ruling E.7, 2026-08-26).
//
// These verdicts were handed to the reviewer as FACTS and were previously visible only to it. A
// human asked to accept or overrule a review of a quotation could not see whether the quotation
// checked out. Four states, and the first one is the reason `quoteFactsRecorded` exists: a review
// that ran before the facts were persisted must not look like a review whose answer quoted nothing.
function quoteFacts(r){
  if (!r) return '';
  const head = '<h2>Quote verification — the facts the reviewer was given</h2>';
  if (!r.quoteFactsRecorded)
    return head + '<div class="notice">NOT RECORDED. This review ran before the quote-verification '
      + 'facts were persisted, so what the reviewer was told cannot be read back. It is not a '
      + 'claim that the answer quoted nothing.</div>';
  const fs = r.quoteFacts || [];
  const recon = r.quoteFactsReconstructed
    ? '<div class="notice">RECONSTRUCTED, not captured. These facts were recomputed from the '
      + 'stored answer and evidence after the review ran. quotes.verify() is deterministic, so they '
      + 'are the same facts — but a re-derived fact is not a recorded one.</div>' : '';
  if (!fs.length)
    return head + recon + '<div class="box" style="white-space:normal"><span class="muted">'
      + 'Checked: no direct quotation of five or more words was found in this answer. Nothing for '
      + 'this check to report — which is a result, not a gap.</span></div>';
  const rows = fs.map(f=>{
    let cls='unknown', label='UNKNOWN';
    if (f.attributed === false) { cls='unknown'; label='UNATTRIBUTED'; }
    else if (f.verbatimMatch === true) { cls='match'; label='VERBATIM MATCH'; }
    else if (f.verbatimMatch === false) { cls='nomatch'; label='NOT VERBATIM'; }
    const cites=(f.cites||[]).join(', ')||'(no citation attached)';
    const frags=(f.fragments||[]).map(fr=>`<div class="frag">fragment ${esc(fr.text||'')} → ${
      (fr.foundIn||[]).join(', ')||'not found'}</div>`).join('');
    return `<div class="qf"><span class="v ${cls}">${label}</span>
      <span class="muted"> attributed to ${esc(cites)}</span>
      <q>${esc(f.quote||'')}</q>
      <span class="muted">${esc(f.reason||'')}</span>${frags}</div>`;
  }).join('');
  const sent = r.quoteFactsAsSent
    ? `<details class="assent"><summary>the block exactly as the reviewer received it</summary>
       <pre>${esc(r.quoteFactsAsSent)}</pre></details>` : '';
  return head + recon + '<div class="box" style="white-space:normal">' + rows + sent + '</div>';
}
function findings(f){
  return Object.entries(f||{}).map(([k,v])=>
    `<div class="find"><span class="${v&&v.ok?'yes':'no'}">${v&&v.ok?'✓':'✗'}</span>
     <b>${esc(k)}</b> — ${esc((v&&v.note)||'')}</div>`).join('');
}
function renderDetail(){
  const q=CUR, r=(q.reviews&&q.reviews[0])||null;
  const proposed=r&&r.proposedAnswer;
  $('detail').innerHTML=`
   <div class="notice"><b>${esc(q.notice.label)}</b><br>${esc(q.notice.detail)}</div>
   <p class="muted">Reads · public (since publication) ${q.views===null||q.views===undefined?'—':q.views}
      · internal (before publication) ${q.provisionalViews||0}</p>
   <h2>Question</h2><div class="box">${esc(q.question)}</div>
   <h2>Provisional answer — never rewritten</h2><div class="box">${esc(q.provisionalAnswer)}</div>
   <h2>Sources</h2><div class="box" style="white-space:normal">${
     (q.sources||[]).map(s=>`<div class="src"><span class="lay ${s.layer==='core'?'core':''}">${
       esc(s.layer||'?')}</span><b>${esc(s.cite)}</b> ${esc(s.label)} — ${esc(s.heading)}${
       s.supersededSinceAnswer?' <span class="lay" style="background:#fdeeee;color:#8c2b2b">superseded since answered</span>':''}<br>
       <span class="muted">${esc(s.standing||'')}</span>${
       s.supersededSinceAnswer?'<br><span class="muted">at answer time: '+esc(s.standingAtAnswer||'')+'</span>':''
       }${/* An editorial rename is NOT a supersession, so it gets its own line and its own words. */
       s.labelChangedSinceAnswer?'<br><span class="muted">shown as “'+esc(s.labelAtAnswer||'')+
         '” when this answer was written — the label was renamed, the cited record did not change</span>':''
       }</div>`).join('')||'<span class="muted">none</span>'}</div>
   ${(q.external||[]).length||(q.externalOffered||[]).length ? `<h2>External sources — may not establish a datumwise position</h2>
     <div class="box" style="white-space:normal">${
       (q.external||[]).map(e=>`<div class="src"><span class="lay ext">external</span>
         <b>${esc(e.cite||'')}</b> ${esc(e.title||e.url)}<br>
         <span class="muted">${esc(e.url||'')}</span></div>`).join('')
       || '<span class="muted">offered but not cited</span>'}</div>` : ''}
   ${quoteFacts(r)}
   <h2>Review</h2>${ r ? `
     <div class="verdict ${r.disposition}"><b>${r.disposition}</b> — ${esc(r.summary)}</div>
     ${findings(r.findings)}
     ${(r.changes||[]).length?'<h2>Changes proposed</h2><div class="box">'+
        r.changes.map(esc).join('\\n')+'</div>':''}`
     : '<p class="muted">No review run yet.</p>' }
   <div class="row"><button onclick="runReview()">Run authority review</button></div>
   <h2>Text to publish</h2>
   <p class="muted">Pre-filled with ${proposed?'the reviewer\\'s proposed revision':'the provisional answer'}. Edit freely — publishing never alters the provisional record.</p>
   <textarea id="pub">${esc(proposed||q.provisionalAnswer)}</textarea>
   <div class="row">
     <button class="primary" onclick="publish()">Publish</button>
     <button class="danger" onclick="reject()">Reject</button>
     <input type="text" id="reason" placeholder="reason (required to reject)" style="flex:1">
   </div><p class="muted" id="msg"></p>`;
}
function who(){ const w=$('who').value.trim(); localStorage.setItem('ask_reviewer',w); return w; }
async function act(path,payload,label){
  $('msg').textContent=label+'…';
  try{ await api(path,{method:'POST',body:JSON.stringify(Object.assign({id:CUR.id,reviewer:who()},payload))});
       const d=await api('/review/queue'); ITEMS=d.items;
       if(path==='/review/run'){ CUR=await api('/review/item/'+CUR.id); renderDetail(); }
       else { CUR=null; $('detail').innerHTML='<p class="muted">Done. Select another candidate.</p>'; }
       renderQueue(); }
  catch(e){ $('msg').textContent='✗ '+(e.message||e); }
}
const runReview=()=>act('/review/run',{},'Reviewing');
const publish=()=>act('/review/publish',{answer:$('pub').value},'Publishing');
const reject=()=>act('/review/reject',{reason:$('reason').value},'Rejecting');
boot();
</script></body></html>
"""
