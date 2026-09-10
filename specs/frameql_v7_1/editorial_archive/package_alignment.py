from pathlib import Path
import hashlib,json,zipfile,shutil,subprocess,tempfile
from bs4 import BeautifulSoup
W=Path(__file__).resolve().parent;O=W/'output';D=W/'audit';R=Path('/mnt/data')
# Browser and structural rendering checks are recorded separately from semantic review cases.
html_checks=[]
for p in sorted(O.glob('*.html')):
 soup=BeautifulSoup(p.read_text(),'html.parser')
 if p.name.startswith(('the_theory_of_data_','tod_v7_1_statistical_')):continue
 missing=[]
 for tag in soup.find_all('a',href=True):
  h=tag['href'].split('#')[0]
  if h and not ':' in h and not (O/h).exists():missing.append(h)
 html_checks.append(dict(file=p.name,local_links_ok=not missing,missing=missing,script_tags=len(soup.find_all('script')),mathml=len(soup.find_all('math'))))
 if missing:raise RuntimeError((p.name,missing))
(D/'reading_copy_checks.json').write_text(json.dumps(dict(status='Pandoc rendering plus HTML inspection; three selected browser screenshots inspected; no page errors in those three previews',checks=html_checks),indent=2)+'\n')
for name,target in [('source_manifest.json','frameql_v7_1_companion_alignment_source_manifest_v0_1.json'),('document_audit.json','frameql_v7_1_companion_alignment_document_audit_v0_1.json')]:
 shutil.copy2(D/name,O/target)
manifest=[]
for p in sorted(O.iterdir()):
 if p.is_file() and p.name!='MANIFEST_SHA256.json':
  manifest.append(dict(file=p.name,bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
(O/'MANIFEST_SHA256.json').write_text(json.dumps(dict(status='local review artifacts; no repository or publication adoption',files=manifest),ensure_ascii=False,indent=2)+'\n')
# Leave all pre-existing source/theory files alone; publish only newly created outputs.
exclude={'START_HERE.md','START_HERE.html','MANIFEST_SHA256.json','the_theory_of_data_v7_1_full_manuscript_working_draft_v0_4.md','the_theory_of_data_v7_1_full_manuscript_working_draft_v0_4.html','tod_v7_1_statistical_extension_supplement_v0_1.md','tod_v7_1_statistical_extension_supplement_v0_1.html'}
for p in O.iterdir():
 if p.is_file() and p.name not in exclude:shutil.copy2(p,R/p.name)
reader=R/'frameql_tod_v7_1_aligned_companion_review_packet_v0_1.zip'
with zipfile.ZipFile(reader,'w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(O.iterdir()):
  if p.is_file():z.write(p,p.name)
(W/'README_EDITORIAL.md').write_text('''# Editorial archive

This archive contains output/ (the active review set), sources/ (preserved historical local files and normalized full web-text transcriptions), audit/ (source hashes, exact recorded edits, diffs and document checks), and the scripts used to create and inspect the new documents.

Start with output/START_HERE.md. Historical sources are NOT active guidance. The authority index lists their supersession dispositions. Introduction and Primer diffs are against normalized full-text transcriptions, not original deposit bytes. No mathematical or Columna suite was executed. The 40 semantic cases are review requirements.

To rerun document checks in an environment with Python and markdown-it-py, run `python audit_documents.py` from the archive root. Rendering additionally requires Pandoc, PyYAML and BeautifulSoup; browser preview requires Playwright and an available Chromium executable. This is document tooling, not Columna implementation code.
''')
# Do not include the failed browser attempt or render temporary files; final script uses current local Chromium.
editorial=R/'frameql_tod_v7_1_companion_alignment_editorial_package_v0_1.zip'
with zipfile.ZipFile(editorial,'w',zipfile.ZIP_DEFLATED) as z:
 for directory in ['output','sources','audit']:
  for p in sorted((W/directory).rglob('*')):
   if p.is_file():z.write(p,p.relative_to(W))
 for name in ['README_EDITORIAL.md','build_alignment.py','build_companions.py','build_acceptance_and_index.py','audit_documents.py','render_documents.py','inspect_reading_copies.py','package_alignment.py']:
  z.write(W/name,name)
# Verify portable reader checksums and rerun the editorial integrity audit on extraction.
with tempfile.TemporaryDirectory(prefix='frameql_packet_') as d:
 with zipfile.ZipFile(editorial) as z:z.extractall(d)
 r=subprocess.run(['python',str(Path(d)/'audit_documents.py')],text=True,capture_output=True,timeout=30)
 if r.returncode:raise RuntimeError(r.stdout+r.stderr)
 extracted=json.loads((Path(d)/'audit'/'document_audit.json').read_text());original=json.loads((D/'document_audit.json').read_text())
 if extracted!=original:raise RuntimeError('Extracted audit differs')
with zipfile.ZipFile(reader) as z:
 for ent in manifest:
  if hashlib.sha256(z.read(ent['file'])).hexdigest()!=ent['sha256']:raise RuntimeError(ent['file'])
print('Reader packet:',reader.name,reader.stat().st_size,'bytes;',len(manifest)+1,'files')
print('Editorial package:',editorial.name,editorial.stat().st_size,'bytes')
print('Extracted audit reproduced identically; all reader file hashes verified.')
print('Delivered core files:')
for n in ['frameql_language_vnext_working_draft_v0_4.md','frameql_v7_1_authority_and_supersession_index_v0_1.md','frameql_an_introduction_v2_4_working_draft_v0_1.md','a_primer_on_frameql_v2_3_working_draft_v0_1.md']:
 p=R/n;print(n,p.exists(),p.stat().st_size)
