from pathlib import Path
import json,hashlib,subprocess
from PIL import Image,ImageDraw
r=Path('/Volumes/EXTERNAL/自媒体/ai-funnel-vibe-20261020');p=r/'04-制作/v3-fix1';q=r/'05-质检/v3';v=p/'output/ai-funnel-v3-fix1-review-150s.mp4'
sha=hashlib.sha256(v.read_bytes()).hexdigest();assert sha=='98f5e6328713e2f8bb4ad85c10f74f8957e931a4a27c064d243ed0edb188ca4d'
old=json.loads((p/'qc/frame-index.json').read_text());lookup={x['frame']:x for x in old};wanted=set(lookup)
for s in json.loads((p/'content-package.json').read_text())['scenes']:
 wanted.add(round((s['start_sec']+s['end_sec'])*30))
 if s['start_sec']:
  wanted.update(round(s['start_sec']*60)+k for k in [-1,18,48])
for t in [10.8,11.4,12.7,13.5,14.5,15.5,20.5,32.5,33.5,45.5,46.5,47,47.4,48,49,61.5,62,63,64,64.5,75.5,76.5,77,77.4,78,88,89.5,90.2,90.8,91.7,92.5,93.2,94.1,94.8,95.3,95.6,97.5,99,100.5,103.5,104,104.6,110.5,111.8,113,113.8,114.8,115.8,116.6,117.7,118.4,119.3,120.3,125,127.8,128.2,130.8,131.2,133,136,139.5,141,143,144]:wanted.add(round(t*60))
fresh=sorted(wanted-set(lookup));sel='+'.join('eq(n,%d)'%f for f in fresh)
subprocess.run(['ffmpeg','-v','error','-n','-i',str(v),'-vf',"select='"+sel+"'",'-fps_mode','vfr','-q:v','2',str(q/'extra-%03d.jpg')],check=True)
for i,f in enumerate(fresh,1):lookup[f]={'frame':f,'time':f/60,'path':str(q/f'extra-{i:03d}.jpg')}
rows=[]
for f in sorted(wanted):
 x=lookup[f];x['sha256']=hashlib.sha256(Path(x['path']).read_bytes()).hexdigest();rows.append(x)
for i in range(0,len(rows),6):
 sheet=Image.new('RGB',(1080,1340),'#282828');d=ImageDraw.Draw(sheet)
 for j,x in enumerate(rows[i:i+6]):
  xx=j%3*360;yy=j//3*670;sheet.paste(Image.open(x['path']).resize((360,640)),(xx,yy));d.text((xx+7,yy+645),f"F{x['frame']} | {x['time']:.3f}s",fill='white')
 sheet.save(q/f'sheet-{i//6+1:02d}.jpg',quality=93)
(q/'sample-index.json').write_text(json.dumps({'sha256':sha,'samples':rows},ensure_ascii=False,indent=2));print('total',len(rows),'new',len(fresh),'sheets',(len(rows)+5)//6)
