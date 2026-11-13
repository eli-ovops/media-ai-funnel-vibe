from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
P=Path(__file__).resolve().parent;Q=P/'qc/final-review';old=P.parent/'qc/final';out=P/'qc/comparisons';out.mkdir(exist_ok=True)
issues={'V1-01':[3.15,50.15],'V1-02':[82.167,103.167,139.167],'V1-03':[57.65,135.65],'V1-04':[135.65]};rs=[]
for k,ts in issues.items():
 sheet=Image.new('RGB',(1080,len(ts)*1015),'#303030');d=ImageDraw.Draw(sheet)
 for j,t in enumerate(ts):
  for i,src in enumerate([old,Q]):
   f=src/f'frame-{(68.6 if src==old and t==68.5 else t):.3f}.jpg';a=Image.open(f);a.thumbnail((540,960));sheet.paste(a,(i*540,j*1015));d.text((i*540+15,j*1015+975),f'{k} | {"V1 RETURNED" if i==0 else "V2 CANDIDATE"} | {t:.3f}s',fill='white')
 f=out/f'{k}-before-after.jpg';sheet.save(f,quality=93);rs.append({'issue':k,'times':ts,'path':str(f),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
(out/'index.json').write_text(json.dumps(rs,indent=2));print(rs)
