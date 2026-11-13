from pathlib import Path
import subprocess,json,hashlib,os
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;B=P.parent/'v2-fix1'
FF='/Users/USER/.local/bin/ffmpeg';probe=(P/'node_modules/@remotion/compositor-darwin-arm64/ffprobe').resolve()
env=os.environ.copy();env['DYLD_LIBRARY_PATH']=str(probe.parent)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def run(a):return subprocess.run(a,check=True,capture_output=True,text=True,env=env)
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2))
visual=P/'output/canvas-final-visual.mp4';out=P/'output/ai-funnel-v3-review-final-150s.mp4';base=B/'output/ai-funnel-v2-fix1-internal-150s.mp4'
r=json.loads((P/'qc/canvas-final-composed-receipt.json').read_text());assert r['renderedFrames']==9000 and r['sourceSha256']==sha(P/'src/World.ts')
a=[FF,'-nostdin','-hide_banner','-n','-i',str(visual),'-i',str(base),'-map','0:v:0','-map','1:a:0','-c','copy','-t','150','-movflags','+faststart',str(out)]
run(a);save(P/'qc/delivery-mux-receipt.json',{'command':a,'source_video_sha256':sha(visual),'audio_source_sha256':sha(base),'output_sha256':sha(out),'music':'USER_WILL_ADD_NATIVE_PLATFORM_MUSIC; NOT_REQUIRED_IN_MASTER'})
meta=json.loads(run([str(probe),'-v','error','-show_format','-show_streams','-of','json',str(out)]).stdout);save(P/'qc/delivery-ffprobe.json',meta)
v=next(s for s in meta['streams'] if s['codec_type']=='video');a=next(s for s in meta['streams'] if s['codec_type']=='audio');assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(1080,1920,'60/1',9000);assert abs(float(v['duration'])-150)<.001 and a['sample_rate']=='48000'
d=run([FF,'-nostdin','-v','error','-xerror','-i',str(out),'-f','null','-']);save(P/'qc/delivery-full-decode.json',{'status':'PASS','exit_code':d.returncode,'stderr':d.stderr,'sha256':sha(out),'scope':'decode integrity only, not continuous watching/hearing'})
def audiohash(p):return run([FF,'-nostdin','-v','error','-i',str(p),'-map','0:a:0','-c','copy','-f','hash','-hash','sha256','-']).stdout.strip()
ah=audiohash(out);bh=audiohash(base);assert ah==bh
save(P/'qc/delivery-audio-copy-check.json',{'status':'PASS','output_packet_hash':ah,'base_packet_hash':bh,'same_encoded_audio_stream':True,'direct_hearing':False})
frames=sorted(set(json.loads((P/'qc/representative-frames.json').read_text())+json.loads((P/'qc/transition-frames.json').read_text())+[1619,1620,1644,1710,1979,1980,2759,2760,2772,2790,2820,2826,2844,5310,5334,5340,5358,5400,5424,5279,5280,5310,5339,5341,5717,5718,5735,5736,6995,6996,7019,7021,7103,7104,7105]))
fdir=P/'qc/delivery-frames';fdir.mkdir(exist_ok=True)
select='+'.join('eq(n\\,%s)'%f for f in frames)
run([FF,'-nostdin','-v','error','-n','-i',str(out),'-vf','select='+select,'-fps_mode','vfr',str(fdir/'sample-%03d.png')])
entries=[]
for i,f in enumerate(frames,1):
 path=fdir/f'sample-{i:03}.png';assert path.exists();entries.append({'frame':f,'time':f/60,'path':str(path),'sha256':sha(path)})
save(P/'qc/delivery-frame-index.json',{'video':str(out),'sha256':sha(out),'frame_selection':'zero-based decoded n; CFR60; no seek approximation','samples':entries,'continuous_viewing':False})
for k in range(0,len(entries),9):
 batch=entries[k:k+9];sheet=Image.new('RGB',(1080,2028),'#101714');dr=ImageDraw.Draw(sheet)
 for j,e in enumerate(batch):
  im=Image.open(e['path']).convert('RGB');im.thumbnail((354,630));x=(j%3)*360;y=(j//3)*676;sheet.paste(im,(x,y+34));dr.text((x+8,y+6),f"{e['time']:.3f}s / F{e['frame']}",fill='white')
 sheet.save(P/f'qc/delivery-contact-{k//9+1:02}.jpg',quality=93)
print(json.dumps({'file':str(out),'sha256':sha(out),'sample_count':len(entries),'contact_sheets':(len(entries)+8)//9},ensure_ascii=False))
