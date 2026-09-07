from pathlib import Path
import re,json,hashlib,sys
from urllib.parse import unquote
from markdown_it import MarkdownIt
W=Path(__file__).resolve().parent;O=W/'output';S=W/'sources';D=W/'audit'
checks=[]
def ck(name,value,detail=''):
 checks.append(dict(check=name,pass_=bool(value),detail=detail))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((D/'source_manifest.json').read_text())
for m in manifest:ck('source hash: '+m['name'],sha(S/m['name'])==m['sha256'])
T='the_theory_of_data_v7_1_full_manuscript_working_draft_v0_4.md'
ck('fixed theory unchanged',sha(O/T)==sha(S/T))
ck('fixed theory expected hash',sha(O/T)=='6d44576eb6af2469c3223370c91f4efcd6c033d7f273d1fabd32060651edacd0')
# In active runtime additionally verify original supplied artifacts, when present.
for m in manifest:
 if m['source']=='confirmed local supplied artifact':
  p=Path('/mnt/data')/m['name']
  if p.exists():ck('original preserved: '+m['name'],sha(p)==m['sha256'])
# Replay exact recorded replacements; never count syntax checks as theorem proof.
def replay(file, mapping):
 changes=json.loads((D/file).read_text())
 for out,src in mapping.items():
  txt=(S/src).read_text()
  for e in changes:
   if e['document']==out:
    if txt.count(e['before'])!=1: raise ValueError((out,e['reason'],'edit precondition failed'))
    txt=txt.replace(e['before'],e['after'],1)
  ck('recorded edit replay: '+out,txt==(O/out).read_text())
replay('language_edits.json',{'frameql_language_vnext_working_draft_v0_4.md':'frameql_language_vnext_working_draft_v0_3.md'})
replay('companion_edits.json',{
 'columna_o3_governed_analytical_order_v0_2.md':'columna_o3_governed_analytical_order_v0_1.md',
 'frameql_an_introduction_v2_4_working_draft_v0_1.md':'frameql_an_introduction_v2_3_transcribed.md',
 'a_primer_on_frameql_v2_3_working_draft_v0_1.md':'a_primer_on_frameql_v2_2_transcribed.md'})
fq=lambda txt:re.findall(r'```frameql\n(.*?)\n```',txt,re.S)
math=lambda txt:re.findall(r'\$\$(.*?)\$\$',txt,re.S)
for stem,n in [('frameql_an_introduction',14),('a_primer_on_frameql',3)]:
 src=next(S.glob(stem+'*transcribed.md'));out=next(O.glob(stem+'*.md'))
 a=src.read_text();b=out.read_text()
 ck(stem+' all Frame-QL examples unchanged',fq(a)==fq(b) and len(fq(b))==n)
 ck(stem+' original displayed equations unchanged',math(a)==math(b))
 main=lambda t:re.findall(r'^# (.+)$',t,re.M)
 ck(stem+' main section order unchanged',main(a)==main(b))
 ck(stem+' no invented assigned DOI', '**DOI:**' not in b and 'no DOI assigned' in b)
# Parse every document and check structural syntax / local links.
parser=MarkdownIt('commonmark',{'html':True}).enable('table')
for p in sorted(O.glob('*.md')):
 txt=p.read_text();tokens=parser.parse(txt)
 ck('Markdown parses: '+p.name,len(tokens)>0)
 ck('balanced display dollar delimiters: '+p.name,len(re.findall(r'^\$\$\s*$',txt,re.M))%2==0)
 fences=[t for t in tokens if t.type=='fence']
 ck('closed code fences: '+p.name, all(txt.splitlines()[t.map[1]-1].lstrip().startswith(t.markup) for t in fences))
 refs=[]
 for t in tokens:
  if t.children:
   for c in t.children:
    if c.type=='link_open':refs.append(c.attrGet('href'))
 missing=[]
 for ref in refs:
  if not ref or re.match(r'^[a-zA-Z][\w+.-]*:',ref) or ref.startswith('#'):continue
  path=unquote(ref.split('#')[0])
  if path and not (p.parent/path).exists():missing.append(path)
 ck('local Markdown links: '+p.name,not missing,', '.join(missing))
# Required textual safeguards, not claimed semantic verification.
L=(O/'frameql_language_vnext_working_draft_v0_4.md').read_text()
for name,words in {
 'single governing family contract':['T §4 is the governing family-law contract','Target'],
 'explicit target specification':['nominated non-circular defining construction','agreement among bases'],
 'constituive lineage distinction':['constitutive analytical lineage','proof method'],
 'contextual formation not excluded':['contextual formation history does not categorically prohibit','faithful'],
 'no executable-intent shortcut':['only one is presently executable','does not choose'],
 'bases not multiple questions':['SUM/COUNT and an adequate multiset','two bases for one meaning'],
 'known-empty not missing':['unavailable intermediate witness must not be replaced','known-empty'],
 'guarded scalar argument':['fixed law, known nonemptiness, exhaustive possible-participant coverage, and supported equal values at every possible winner'],
 'lossy-state premise':['compressed winner is not a global consistency validator','Matching context labels alone'],
 'O3 proof not duplicated':['language refers to T\'s proofs'],
 'exact approximation boundary':['HLL','not an exact sufficient-state basis'],
 'runtime not claimed':['not a published language edition or implementation authorization'],
}.items():ck('guard: '+name,all(w.lower() in L.lower() for w in words))
for bad in ['The family ontology remains order-independent.','`last`\n\n is an ordered expression','FAIL AS ORDINARY LAG','TOP-k can also pass in principle','only for the request being made']:
 ck('withdrawn rule absent: '+bad,bad not in L)
# JSON acceptance is a review set, not executed computations.
j=json.loads((O/'frameql_v7_1_semantic_acceptance_cases_v0_1.json').read_text());cm=(O/'frameql_v7_1_semantic_acceptance_cases_v0_1.md').read_text()
ck('40 unique semantic cases',len(j['cases'])==40 and len({c['id']for c in j['cases']})==40)
ck('case Markdown matches JSON identifiers',all('## '+c['id']+' — '+c['topic'] in cm for c in j['cases']))
ck('every case has source and premises',all(all(c.get(k) for k in ['premises','expected','prohibited_shortcut','theory_sections','language_sections'])for c in j['cases']))
index=(O/'frameql_v7_1_authority_and_supersession_index_v0_1.md').read_text()
ss=json.loads((D/'supersession_dispositions.json').read_text())
ck('13 exact older guidance files dispositioned',len(ss)==13 and all(e['source']in index for e in ss))
ck('old instructions not current authorization','not reusable authorization' in index)
result=dict(kind='document integrity and explicit editorial safeguards only; no runtime or mathematical suite execution',checks_total=len(checks),checks_passed=sum(c['pass_']for c in checks),failures=[c for c in checks if not c['pass_']],checks=checks)
(D/'document_audit.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({k:result[k]for k in ['checks_total','checks_passed','failures']},ensure_ascii=False,indent=2))
if result['failures']:sys.exit(1)
