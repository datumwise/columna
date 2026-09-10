from pathlib import Path
import re,subprocess,json,shutil,yaml
from bs4 import BeautifulSoup
W=Path(__file__).resolve().parent;O=W/'output';D=W/'audit';tmp=W/'render_work';tmp.mkdir(exist_ok=True)
css='''html{scroll-behavior:smooth}body{font-family:Georgia,"Times New Roman",serif;color:#202b33;background:#fff;max-width:920px;margin:auto;padding:42px 44px;line-height:1.58;font-size:17px}h1,h2,h3,h4{font-family:Arial,Helvetica,sans-serif;line-height:1.22;color:#173e4b;scroll-margin-top:20px}h1{font-size:2em;margin-top:2em}h2{font-size:1.45em;margin-top:1.8em}h3{font-size:1.12em;margin-top:1.6em}#title-block-header h1{margin-top:0}a{color:#17637a;text-decoration-thickness:.06em;text-underline-offset:.15em}p{margin:.85em 0}blockquote{border-left:3px solid #abc1c9;margin:1.2em 0;padding:.2em 1.25em;background:#f5f8f9}table{border-collapse:collapse;width:100%;font-size:.9em;margin:1.2em 0;display:block;overflow-x:auto}th,td{text-align:left;vertical-align:top;border-bottom:1px solid #d8e1e5;padding:.65em .8em}th{font-family:Arial,Helvetica,sans-serif;background:#eef4f6}pre{padding:1em;background:#f4f6f8;border:1px solid #e2e8eb;overflow-x:auto;font-size:.84em;line-height:1.45}code{font-family:ui-monospace,Consolas,monospace;font-size:.88em}pre code{font-size:inherit}math{font-size:1.04em}math[display=block]{margin:1.1em 0;max-width:100%;overflow-x:auto}nav#TOC{border:1px solid #dce5e9;background:#f8fafb;padding:18px 24px;font-size:.9em;margin:2em 0;max-height:420px;overflow:auto}nav#TOC ul{list-style:none;padding-left:1em}nav#TOC>ul{padding-left:0}nav#TOC li{margin:.24em 0}hr{border:0;border-top:1px solid #dce4e8;margin:2em 0}.reading-status{font:13px/1.5 Arial,Helvetica,sans-serif;border-bottom:1px solid #c8d8de;padding-bottom:12px;color:#48626d}.reading-status a{margin-right:18px}.math.display{display:block;overflow-x:auto;padding:.3em 0} @media(max-width:720px){body{padding:24px 18px;font-size:16px}h1{font-size:1.7em}th,td{min-width:140px}} @media print{body{max-width:none;padding:0;font-size:10.5pt}nav#TOC{max-height:none;background:white}.reading-status{font-size:8pt}h1,h2,h3{break-after:avoid}table,pre,blockquote{break-inside:avoid}a{color:inherit;text-decoration:none}}'''
(tmp/'reading.css').write_text(css)
records=[]
for p in sorted(O.glob('*.md')):
 if p.name in ['the_theory_of_data_v7_1_full_manuscript_working_draft_v0_4.md','tod_v7_1_statistical_extension_supplement_v0_1.md']:
  original=Path('/mnt/data')/p.with_suffix('.html').name
  if original.exists():shutil.copy2(original,p.with_suffix('.html'));continue
 text=p.read_text()
 # Render metadata only; the delivered Markdown retains its own typesetting metadata.
 if text.startswith('---\n'):
  _,front,body=text.split('---',2);data=yaml.safe_load(front)
  clean={k:data[k]for k in ['title','subtitle','author','date','lang']if k in data}
  text='---\n'+yaml.safe_dump(clean,allow_unicode=True,sort_keys=False)+'---\n'+body
 title=re.search(r'^# (.+)$',text,re.M)
 scratch=tmp/p.name;scratch.write_text(text)
 cmd=['pandoc',str(scratch),'-f','markdown+tex_math_dollars+tex_math_single_backslash','-t','html5','--standalone','--mathml','--toc','--toc-depth=2','--section-divs','--embed-resources','--css',str(tmp/'reading.css'),'-M','lang=en-US','-M','pagetitle='+(title.group(1)if title else p.stem),'-o',str(p.with_suffix('.html'))]
 r=subprocess.run(cmd,text=True,capture_output=True,timeout=15)
 if r.returncode:raise RuntimeError((p.name,r.stderr))
 html=p.with_suffix('.html').read_text();soup=BeautifulSoup(html,'html.parser')
 notice=soup.new_tag('div',attrs={'class':'reading-status'})
 notice.append('WORKING COMPANION SET · 7 SEPTEMBER 2026 · NOT A LANGUAGE RELEASE')
 notice.append(soup.new_tag('br'))
 for label,href in [('Reading index','frameql_v7_1_authority_and_supersession_index_v0_1.html'),('Source Markdown',p.name)]:
  a=soup.new_tag('a',href=href);a.string=label;notice.append(a)
 soup.body.insert(0,notice)
 for a in soup.find_all('a',href=True):
  href=a['href'];base,sep,frag=href.partition('#')
  if base.endswith('.md') and (O/base).is_file() and a.text!='Source Markdown':a['href']=base[:-3]+'.html'+(sep+frag if sep else '')
 p.with_suffix('.html').write_text(str(soup))
 records.append(dict(file=p.name,html=p.with_suffix('.html').name,math_elements=len(soup.find_all('math')),warnings=r.stderr.strip()))
(D/'render_log.json').write_text(json.dumps(records,indent=2,ensure_ascii=False)+'\n')
print('Rendered',len(records),'new reading copies; retained unchanged theory/supplement HTML where available.')
print('Warnings:',[r for r in records if r['warnings']])
