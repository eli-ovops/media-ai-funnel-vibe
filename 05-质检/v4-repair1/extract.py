from pathlib import Path
import json,hashlib,subprocess
from PIL import Image,ImageDraw
p=Path('/Volumes/EXTERNAL/自媒体/ai-funnel-vibe-20261020');q=p/'05-质检/v4-repair1';v=p/'04-制作/v4-repair1/output/ai-funnel-v4-repair1-150s-r1.mp4'
sha=hashlib.sha256(v.read_bytes()).hexdigest();assert sha=='71c213a4b4d90fc3448a463f8d96e6994786ec32c56168acba2d1518d4dff7dc'
frames=set(range(5040,9000,60));frames.update([5039,8999])
for a,b in [(90.4,91.6),(94.6,95.8),(98.2,100),(100.8,102),(102.8,105.2),(110.8,112),(115.8,118.4),(124,126),(139.8,142),(145.4,147.2)]:
 frames.update(range(round(a*60),round(b*60)+1,12))
frames=sorted(frames);sel='+'.join('eq(n,%s)'%x for x in frames)
subprocess.run(['/Users/USER/.local/bin/ffmpeg','-v','error','-n','-i',str(v),'-vf',"select='"+sel+"'",'-fps_mode','vfr','-q:v','2',str(q/'frame-%03d.jpg')],check=True)
rows=[{'frame':f,'seconds':f/60,'path':str(q/f'frame-{i+1:03d}.jpg')} for i,f in enumerate(frames)]
for r in rows:r['sha256']=hashlib.sha256(Path(r['path']).read_bytes()).hexdigest()
for i in range(0,len(rows),12):
 sheet=Image.new('RGB',(1440,1310),'#ddd');d=ImageDraw.Draw(sheet)
 for j,r in enumerate(rows[i:i+12]):
  x=j%6*240;y=j//6*655;im=Image.open(r['path']);im.thumbnail((240,620));sheet.paste(im,(x,y+25));d.text((x+5,y+5),'F%d %.3fs'%(r['frame'],r['seconds']),fill='black')
 sheet.save(q/f'sheet-{i//12+1:02d}.jpg',quality=94)
(q/'sample-index.json').write_text(json.dumps({'video_sha256':sha,'samples':rows},ensure_ascii=False,indent=2))

print('Samples',len(rows),'Sheets',(len(rows)+11)//12,'SHA',sha)
