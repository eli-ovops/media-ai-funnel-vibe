from pathlib import Path
import subprocess,json,hashlib,os,re
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;FF='/Users/USER/.local/bin/ffmpeg';base=P.parent/'v3-fix1/output/ai-funnel-v3-fix1-review-150s.mp4';out=P/'output/ai-funnel-v3-fix2-review-150s.mp4';probe=(P/'node_modules/@remotion/compositor-darwin-arm64/ffprobe').resolve();env=os.environ.copy();env['DYLD_LIBRARY_PATH']=str(probe.parent)
def run(c):return subprocess.run(c,check=True,capture_output=True,env=env)
def save(n,x):(P/'qc'/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
m=json.loads(run([str(probe),'-v','error','-show_streams','-show_format','-of','json',str(out)]).stdout);save('ffprobe.json',m);v=next(x for x in m['streams'] if x['codec_type']=='video');assert (v['width'],v['height'],v['r_frame_rate'],v['nb_frames'])==(1080,1920,'60/1','9000');assert float(v['duration'])==150
h=lambda f:run([FF,'-nostdin','-v','error','-i',str(f),'-map','0:a:0','-c','copy','-f','hash','-hash','sha256','-']).stdout.decode().strip()
a,b=h(base),h(out);assert a==b;save('audio-check.json',{'status':'PASS','base_hash':a,'output_hash':b,'direct_hearing':False,'original_34_sfx_preserved_by_packet_copy':True})
s="select='not(between(n,1380,1619)+between(n,7884,8459))',setpts=N/(60*TB)";f=f'[0:v]{s}[a];[1:v]{s}[b];[a][b]ssim';r=run([FF,'-nostdin','-hide_banner','-xerror','-i',str(base),'-i',str(out),'-filter_complex',f,'-an','-f','null','-']);(P/'qc/protected-ssim.log').write_bytes(r.stderr);match=re.findall(r'All:([\d.]+)',r.stderr.decode());assert match and float(match[-1])>.999;save('technical-check.json',{'status':'PASS','full_9000_frame_decode':'PASS within full decode then temporal selection SSIM','protected_frames_compared':8184,'protected_ssim':float(match[-1]),'reencoded_video_bytes_not_identical':True})
frames=json.loads((P/'qc/representative-frames.json').read_text());d=P/'qc/export-frames';d.mkdir(exist_ok=True);sel='+'.join('eq(n\\,%s)'%f for f in frames);run([FF,'-nostdin','-v','error','-n','-i',str(out),'-vf','select='+sel,'-fps_mode','vfr',str(d/'sample-%03d.png')]);rows=[{'frame':f,'seconds':f/60,'path':str(d/f'sample-{i:03d}.png')} for i,f in enumerate(frames,1)];save('export-frame-index.json',rows)
for k in range(0,len(rows),6):
 im=Image.new('RGB',(1080,1370),'#101714');dr=ImageDraw.Draw(im)
 for j,r in enumerate(rows[k:k+6]):
  a=Image.open(r['path']).convert('RGB');a.thumbnail((354,630));x=j%3*360;y=j//3*680;im.paste(a,(x,y+35));dr.text((x+8,y+8),f"{r['seconds']:.4f}s / F{r['frame']}",fill='white')
 im.save(P/f'qc/export-contact-{k//6+1}.jpg',quality=95)
print(json.dumps({'spec':'1080x1920/60/9000/150','protected_ssim':float(match[-1]),'audio_equal':True,'export_samples':len(rows)}))
