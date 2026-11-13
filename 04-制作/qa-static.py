from pathlib import Path
from PIL import ImageFont
import json,hashlib
P=Path(__file__).resolve().parent;c=json.loads((P/'content-package.json').read_text());rows=[]
for s in c['scenes']:
 count=s['screen_lines'][0].startswith('约');intro=s['id'] in ['question','closing'];y=330 if count else 350 if intro else 340
 for i,text in enumerate(s['screen_lines']):
  size=112 if count and i==0 else 80 if intro else 72
  if len(text)>=13:size=64
  fp=P/'public/fonts'/('MiSans-Heavy.otf' if count and i==0 else 'MiSans-Medium.otf');font=ImageFont.truetype(str(fp),size);bbox=font.getbbox(text)
  rows.append({'scene':s['id'],'text':text,'font':fp.name,'size_px':size,'x':90,'y':y,'right_px':90+bbox[2],'bottom_px':y+bbox[3],'within_safe_area':90+bbox[2]<=990 and y+bbox[3]<720,'reading_window':[s['reading_start_frame'],s['reading_end_frame_exclusive']]});y+=size*(1.42 if count and i==0 else 1.48)
report={'scope':'Font-file glyph geometry and source schedule, not perception acceptance','exact_copy_input_sha256':hashlib.sha256((P/'content-package.json').read_bytes()).hexdigest(),'line_count':len(rows),'within_safe_area':all(r['within_safe_area'] for r in rows),'max_right':max(r['right_px'] for r in rows),'rows':rows,'reading_stability':'Canvas copy has no translation/scale; opacity is 1 from start+0.5 through end-0.2, closing through frame8999','no_population_geometry':'Counts are text only; graph population data is never imported','clock':'60fps frame/60; no frame skipping or time/random state'}
(P/'qc/copy-geometry.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print({k:v for k,v in report.items() if k!='rows'})
