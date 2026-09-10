#!/usr/bin/env python3
"""Reproduce document-integrity checks only; no semantic execution or runtime tests."""
from pathlib import Path
from collections import Counter
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import difflib
import hashlib
import json
import re
import sys

BASE = Path(__file__).resolve().parent

def load(name):
    return json.loads((BASE / name).read_text(encoding='utf-8'))

def sha(data):
    return hashlib.sha256(data).hexdigest()

def require(condition, message):
    if not condition:
        raise ValueError(message)

def sections(text):
    lines = text.splitlines(); heads = []
    for i,line in enumerate(lines,1):
        m=re.match(r'^(#{1,6})\s+(?:Appendix\s+)?((?:[A-Z]|\d+)(?:\.\d+)*)(?:\.)?\s+(.+)',line)
        if m: heads.append((i,len(m[1]),m[2],line))
    result={}
    for j,(start,level,key,heading) in enumerate(heads):
        end=next((h[0]-1 for h in heads[j+1:] if h[1]<=level),len(lines))
        result[key]={'start_line':start,'end_line':end,'heading':heading}
    return result

def fences(text):
    return re.findall(r'^```[^\n]*\n.*?^```[ \t]*$',text,re.S|re.M)

def equations(text):
    return re.findall(r'\$\$.*?\$\$|\\\[.*?\\\]|\\\(.*?\\\)',text,re.S)

class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.values=[]
    def handle_starttag(self,tag,attrs):
        self.values.extend(v for k,v in attrs if k in ('href','src') and v)

manifest=load('tod_frameql_joint_review_source_manifest_v0_1.json')
for group,directory in [('active_documents','reviewed_sources'),('reading_copies','reviewed_sources'),('supplemental_historical_provenance','historical_provenance')]:
    for rec in manifest[group]:
        path=BASE/directory/rec['filename']; raw=path.read_bytes()
        require(sha(raw)==rec['sha256'],f'Source hash mismatch: {path.name}')
        if 'bytes' in rec: require(len(raw)==rec['bytes'],f'Byte count mismatch: {path.name}')
        if 'lines' in rec: require(len(raw.decode().splitlines())==rec['lines'],f'Line count mismatch: {path.name}')
ac_record=manifest['machine_readable_case_source']
ac_raw=(BASE/'reviewed_sources'/ac_record['filename']).read_bytes()
require(sha(ac_raw)==ac_record['sha256'],'Acceptance JSON changed')
original=json.loads(ac_raw); ledger=load('tod_frameql_joint_consistency_case_ledger_v0_1.json')
original_cases={c['id']:c for c in original['cases']}; rows=ledger['cases']
require(len(rows)==len(original_cases)==40,'Expected forty supplied cases')
require(len({c['id'] for c in rows})==40,'Duplicate ledger case ID')
require({c['id'] for c in rows}==set(original_cases),'Case ID mismatch')
spans={tag:sections((BASE/'reviewed_sources'/ledger[field]).read_text()) for tag,field in [('T','theory'),('LQ','language')]}
for r in rows:
    c=original_cases[r['id']]
    for key,value in c.items(): require(r[key]==value,f'Original case field changed: {r["id"]}/{key}')
    require(bool(r['review_reasoning']) and bool(r['other_companion_checks']),f'Missing review note: {r["id"]}')
    for tag,refs in r['source_locations'].items():
        for ref in refs:
            expected={'section':ref['section'],**spans[tag][ref['section']]}
            require(ref==expected,f'Section location mismatch: {r["id"]}/{tag}/{ref["section"]}')
counts=Counter(r['review_disposition'] for r in rows)
require(counts=={'consistent':39,'consistent_with_local_example_clarification':1},'Disposition count mismatch')
require(next(r for r in rows if r['review_disposition']!='consistent')['id']=='E02','Unexpected clarification case')
md=(BASE/'tod_frameql_joint_consistency_case_ledger_v0_1.md').read_text()
require(set(re.findall(r'^## ([FOCERG]\d\d) — ',md,re.M))==set(original_cases),'Markdown ledger IDs mismatch')

patches=load('tod_frameql_joint_review_editorial_corrections_v0_1.json')['edits']
require([p['id'] for p in patches]==['J1','J2'],'Unexpected patch IDs')
for p in patches:
    before=(BASE/'reviewed_sources'/p['source_file']).read_text()
    require(sha(before.encode())==p['source_sha256'],f'Patch source changed: {p["id"]}')
    require(before.count(p['old'])==1,f'Patch target not unique: {p["id"]}')
    require(before[:before.index(p['old'])].count('\n')+1==p['start_line'],'Patch line mismatch')
    after=before.replace(p['old'],p['new'],1)
    require(sha(after.encode())==p['proposed_content_sha256'],f'Patch replay mismatch: {p["id"]}')
    require(fences(before)==fences(after),f'Fenced example changed: {p["id"]}')
    require(equations(before)==equations(after),f'Equation changed: {p["id"]}')
    delta=''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='reviewed_sources/'+p['source_file'],tofile='proposed_adoption/'+p['source_file']))
    require(delta==(BASE/f'{p["id"]}_editorial_correction.diff').read_text(),f'Diff mismatch: {p["id"]}')
require('[S6]' in patches[1]['new'] and 'historical, not current' in patches[1]['new'],'Missing citation-status qualification')
old_o3=(BASE/'historical_provenance/columna_o3_governed_analytical_order_v0_1.md').read_text()
require('**[S6]' in old_o3 and 'START_HERE(2).md' in old_o3,'Historical citation referent not present')

# Test local file destinations only. External URLs and in-document fragment targets
# are not independently verified by these file-integrity checks.
checked_destinations=set()
for path in sorted(BASE.rglob('*')):
    if path.suffix=='.md':
        urls=re.findall(r'\]\(([^)]+)\)',path.read_text())
    elif path.suffix=='.html':
        parser=Links(); parser.feed(path.read_text()); urls=parser.values
    else: continue
    for raw in urls:
        parsed=urlsplit(raw)
        if parsed.scheme or parsed.netloc or not parsed.path: continue
        relative=unquote(parsed.path)
        require(not relative.startswith('/'),f'Absolute local link: {raw}')
        target=(path.parent/relative).resolve()
        require(target.is_relative_to(BASE),f'Link outside packet: {path.name}: {raw}')
        require(target.is_file(),f'Missing local link: {path.name}: {raw}')
        checked_destinations.add((str(path.relative_to(BASE)),relative))

# When packaged, verify the complete checksum manifest as well. Its presence does
# not change the deterministic review result below.
checksum_file=BASE/'MANIFEST_SHA256.json'
if checksum_file.exists():
    all_files=json.loads(checksum_file.read_text())['files']
    actual={str(p.relative_to(BASE)) for p in BASE.rglob('*') if p.is_file() and p.name!='MANIFEST_SHA256.json' and '__pycache__' not in p.parts}
    require(actual=={r['path'] for r in all_files},'Package file membership differs from manifest')
    for r in all_files:
        raw=(BASE/r['path']).read_bytes()
        require(sha(raw)==r['sha256'] and len(raw)==r['bytes'],f'Package hash mismatch: {r["path"]}')
result={
 'title':'ToD v7.1 / Frame-QL joint-review document-integrity audit',
 'version':'0.1','date':'2026-09-07','status':'passed',
 'scope':'File integrity, source mapping, and patch preservation only. No semantic scenarios, theorem suites, Columna tests, live sources, or CDT API were executed or verified.',
 'checks':{
  'twelve_active_markdown_source_hashes':'passed',
  'reading_copy_and_historical_source_hashes':'passed',
  'forty_original_cases_and_expected_judgments_preserved':'passed',
  'case_to_theory_and_language_section_locations':'passed',
  'case_ledger_dispositions':'39 consistent; E02 consistent with local example clarification',
  'J1_J2_unique_replay_and_exact_diffs':'passed',
  'equations_and_fenced_examples_unchanged_under_proposed_edits':'passed',
  'S6_historical_referent_and_scope':'passed',
  'packaged_local_file_link_destinations':'passed'
 },
 'not_claimed':['semantic proof','independent external review','new execution of historical mathematical suites','runtime conformance','published status','live corpus adoption'],
 'source_changes':'None. Patches were replayed in memory only.'
}
print(json.dumps(result,indent=2,ensure_ascii=False))
