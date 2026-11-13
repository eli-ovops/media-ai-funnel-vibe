from pathlib import Path
import json,hashlib,subprocess
from PIL import Image,ImageDraw
p=Path('/Volumes/EXTERNAL/自媒体/ai-funnel-vibe-20261020');q=p/'05-质检/v4-complete';v=p/'04-制作/v4-complete/output/ai-funnel-v4-complete-150s-r5.mp4'
sha=hashlib.sha256(v.read_bytes()).hexdigest();assert sha=='6ac2862d8b34a813ff471ff13d14a572bb77f35e0c5df78e1267bcaab343cbd0'
frames=set(range(0,9000,60));frames.add(8999)
for t in [6,12,16,23,28,35,41,46,53.4,59,59.8,70,78,84,90.4,91,94,98,100.5,105,112,115.5,119,126,133.5,141,147]:
 frames.update(round(t*60)+n for n in [-1,18,36,48])
for a,b in [(140.5,141.3),(146.2,147.1),(23,24.3),(35,36.3)]:
 frames.update(range(round(a*60),round(b*60)+1,6))
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
import os
compositor=Path('/Volumes/EXTERNAL/自媒体/Fred复刻测试-20261016/7694088597179239690/source-snapshot/FredTalk-1.5-3D/camera/node_modules/@remotion/compositor-darwin-arm64')
env=dict(os.environ,DYLD_LIBRARY_PATH=str(compositor))
probe=subprocess.check_output([str(compositor/'ffprobe'),'-v','error','-show_streams','-show_format','-of','json',str(v)],env=env)
(q/'ffprobe.json').write_bytes(probe)
print('Frames',len(rows),'sheets',(len(rows)+11)//12,'SHA',sha)
