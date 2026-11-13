from pathlib import Path
import subprocess,json,hashlib,os
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;B=P.parent/'v3';out=P/'output/ai-funnel-v3-fix1-review-150s.mp4';base=B/'output/ai-funnel-v3-review-final-150s.mp4';FF='/Users/USER/.local/bin/ffmpeg';probe=(P/'node_modules/@remotion/compositor-darwin-arm64/ffprobe').resolve();env=os.environ.copy();env['DYLD_LIBRARY_PATH']=str(probe.parent)
def run(c):return subprocess.run(c,check=True,capture_output=True,env=env)
def save(n,d):(P/'qc'/n).write_text(json.dumps(d,ensure_ascii=False,indent=2))
meta=json.loads(run([str(probe),'-v','error','-show_streams','-show_format','-of','json',str(out)]).stdout);save('ffprobe.json',meta);v=next(x for x in meta['streams'] if x['codec_type']=='video');assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(1080,1920,'60/1',9000);assert abs(float(v['duration'])-150)<.001
h=lambda p:run([FF,'-nostdin','-v','error','-i',str(p),'-map','0:a:0','-c','copy','-f','hash','-hash','sha256','-']).stdout.decode().strip()
a=h(out);b=h(base);assert a==b;save('audio-check.json',{'status':'PASS','output':a,'base':b,'direct_hearing':False})
mask='drawbox=x=0:y=150:w=1080:h=90:color=black:t=fill,drawbox=x=0:y=1750:w=1080:h=90:color=black:t=fill'
c=[FF,'-nostdin','-hide_banner','-xerror','-i',str(base),'-i',str(out),'-filter_complex',f'[0:v]{mask}[a];[1:v]{mask}[b];[a][b]ssim','-an','-f','null','-'];r=run(c);(P/'qc/outside-ssim.txt').write_bytes(r.stderr);save('full-decode.json',{'status':'PASS','exit_code':r.returncode,'scope':'all9000frames decoded in SSIM comparison; not continuous perception'})
flt='split=2[a][b];[a]crop=1080:90:0:150[t];[b]crop=1080:90:0:1750[u];[t][u]vstack,format=gray'
ref=run([FF,'-nostdin','-v','error','-i',str(P/'qc/background.png'),'-filter_complex','format=yuv420p,'+flt,'-frames:v','1','-f','rawvideo','-']).stdout;expected=np.frombuffer(ref,dtype=np.uint8).astype(np.int16);size=len(ref);assert size==194400
pr=subprocess.Popen([FF,'-nostdin','-v','error','-xerror','-i',str(out),'-filter_complex',flt,'-an','-f','rawvideo','-'],stdout=subprocess.PIPE,stderr=subprocess.PIPE);count=0;peak=0;means=[];bad=[]
while True:
 chunk=pr.stdout.read(size)
 if not chunk:break
 assert len(chunk)==size
 delta=np.abs(np.frombuffer(chunk,dtype=np.uint8).astype(np.int16)-expected);m=int(delta.max());peak=max(peak,m);means.append(float(delta.mean()))
 if m>16:bad.append({'frame':count,'max_luma_error':m})
 count+=1
stderr=pr.stderr.read().decode();code=pr.wait();assert code==0 and count==9000
save('export-background-check.json',{'status':'PASS' if not bad else 'FAIL','frames':count,'max_luma_error':peak,'mean_luma_error':float(np.mean(means)),'threshold':16,'bad_frames':bad[:20],'method':'Every decoded final ROI compared to exact source background converted using same pixel format; source and export checks separate','stderr':stderr});assert not bad
frames=[0,1,240,720,1440,1710,1980,2772,3000,3900,4499,4500,4501,4560,5340,7038,7722,8820,8999];folder=P/'qc/frames';folder.mkdir(exist_ok=True);select='+'.join('eq(n\\,%s)'%f for f in frames)
run([FF,'-nostdin','-v','error','-n','-i',str(out),'-vf','select='+select,'-fps_mode','vfr',str(folder/'sample-%03d.png')])
rows=[]
for i,f in enumerate(frames,1):rows.append({'frame':f,'time':f/60,'path':str(folder/f'sample-{i:03d}.png')})
save('frame-index.json',rows)
for k in range(0,len(rows),6):
 im=Image.new('RGB',(1080,1370),'#101714');dr=ImageDraw.Draw(im)
 for j,r in enumerate(rows[k:k+6]):
  a=Image.open(r['path']).convert('RGB');a.thumbnail((354,630));x=j%3*360;y=j//3*680;im.paste(a,(x,y+35));dr.text((x+8,y+8),f"{r['time']:.3f}s / F{r['frame']}",fill='white')
 im.save(P/f'qc/contact-{k//6+1}.jpg',quality=93)
print(json.dumps({'frames':count,'background_max_luma_error':peak,'samples':len(rows),'audio_equal':True}))
