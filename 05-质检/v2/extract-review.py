from pathlib import Path
import json,subprocess,hashlib,math
from PIL import Image,ImageDraw
R=Path('/Volumes/EXTERNAL/自媒体/ai-funnel-vibe-20261020');P=R/'04-制作/v2';Q=R/'05-质检/v2';V=P/'output/ai-funnel-v2-review-150s.mp4'
sc=json.loads((P/'content-package.json').read_text())['scenes'];wanted={0,30,8999}
for s in sc:
 wanted.add(round((s['start_sec']+s['end_sec'])*30))
for s in sc[1:]:
 f=s['start_sec']*60
 wanted.update([f-12,f-1,f,f+15,f+30])
for t in [54.7,55.1,55.5,56,68.8,69.4,71.5,72.5,90,90.5,91,91.5,92,92.5,93,93.25,93.5,94,94.5,105,106,111,111.75,112.5,113.5,126,127,128,141.5,143,144.5]:wanted.add(round(t*60))
old=json.loads((P/'qc/final-review/export-check.json').read_text())['frame_records'];oldmap={round(x['second']*60):x for x in old};frames=sorted(wanted);fresh=[f for f in frames if f not in oldmap]
sel='+'.join('eq(n,%d)'%f for f in fresh)
subprocess.run(['/Users/USER/.local/bin/ffmpeg','-nostdin','-v','error','-n','-i',str(V),'-vf',"select='"+sel+"'",'-fps_mode','vfr','-q:v','2',str(Q/'extra-%03d.jpg')],check=True)
records=[];i=0
for f in frames:
 if f in oldmap:path=Path(oldmap[f]['path']);kind='reused'
 else:i+=1;path=Q/f'extra-{i:03d}.jpg';kind='new'
 records.append({'frame':f,'seconds':f/60,'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'kind':kind})
(Q/'sample-index.json').write_text(json.dumps({'artifact':str(V),'sha256':'9a3ce43284d15afa47178e7e188d8baca3d17b2aedee5c64eab45a50ec3da537','samples':records},ensure_ascii=False,indent=2))
# 360px-wide phone scale, six per contact sheet; never alter evidence content.
for j in range(0,len(records),6):
 chunk=records[j:j+6];im=Image.new('RGB',(1080,680*math.ceil(len(chunk)/3)),'#292929');d=ImageDraw.Draw(im)
 for k,x in enumerate(chunk):
  xx=k%3*360;yy=k//3*680;im.paste(Image.open(x['path']).resize((360,640)),(xx,yy));d.text((xx+8,yy+648),f"F{x['frame']} | {x['seconds']:.3f}s",fill='white')
 im.save(Q/f'contact-{j//6+1:02d}.jpg',quality=94)
print(json.dumps({'samples':len(records),'new':len(fresh),'sheets':math.ceil(len(records)/6),'bytes':sum(x.stat().st_size for x in Q.iterdir() if x.is_file())}))
