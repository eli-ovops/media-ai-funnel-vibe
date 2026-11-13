from pathlib import Path
from PIL import Image,ImageDraw
import subprocess,math,json,hashlib,sys
P=Path(__file__).resolve().parent;mode=sys.argv[1];base={'branch':54,'access':124}[mode];ts={'branch':[54,54.5,55.5,57.65,61,64.65,68.5,72,74.983,75.25,75.5,75.983],'access':[124,124.167,124.5,126.5,128,132.5,135.65,138.983,139.167,139.5,139.983]}[mode]
Q=P/'qc'/('sample-'+mode);Q.mkdir(exist_ok=True);F=P/'output'/f'canvas-{mode}-visual.mp4';records=[]
for t in ts:
 f=Q/f'frame-{t:.3f}.jpg';subprocess.run(['/Users/USER/.local/bin/ffmpeg','-nostdin','-v','error','-ss',str(t-base),'-i',str(F),'-frames:v','1','-q:v','2',str(f)],check=True);records.append({'time':t,'file':str(f),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
for k in range(0,len(ts),8):
 im=Image.new('RGB',(1080,1024),'#333');d=ImageDraw.Draw(im)
 for i,t in enumerate(ts[k:k+8]):
  a=Image.open(Q/f'frame-{t:.3f}.jpg');a.thumbnail((270,480));x=i%4*270;y=i//4*512;im.paste(a,(x,y));d.text((x+8,y+486),f'{t:.3f}s',fill='white')
 im.save(Q/f'sheet-{k//8+1}.jpg')
(Q/'frames.json').write_text(json.dumps(records,indent=2));print(len(records))
