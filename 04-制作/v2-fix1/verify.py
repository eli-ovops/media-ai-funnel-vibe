from pathlib import Path
import subprocess,json,hashlib,os,math
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;Q=P/'qc/final';Q.mkdir(exist_ok=True);F=P/'output/ai-funnel-v2-fix1-internal-150s.mp4';ff='/Users/USER/.local/bin/ffmpeg';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
probe=P/'node_modules/@remotion/compositor-darwin-arm64/ffprobe';env=os.environ.copy();env['DYLD_LIBRARY_PATH']=str(probe.parent.resolve())
def run(cmd,**kw):return subprocess.run(cmd,check=True,capture_output=True,**kw)
meta=json.loads(run([str(probe),'-v','error','-show_streams','-show_format','-of','json',str(F)],env=env).stdout);(Q/'metadata.json').write_text(json.dumps(meta,indent=2));v=next(s for s in meta['streams'] if s['codec_type']=='video');a=next(s for s in meta['streams'] if s['codec_type']=='audio');assert (v['width'],v['height'],v['r_frame_rate'],v['nb_frames'])==(1080,1920,'60/1','9000');assert v['duration']=='150.000000' and a['duration']=='150.000000'
dec=run([ff,'-nostdin','-v','error','-xerror','-i',str(F),'-progress','pipe:1','-f','null','-']);(Q/'decode-progress.txt').write_bytes(dec.stdout);(Q/'decode-errors.txt').write_bytes(dec.stderr)
base=Path(json.loads((P/'qc/scope.json').read_text())['base_artifact']);audio=[]
for f in [base,F]:audio.append(run([ff,'-nostdin','-v','error','-i',str(f),'-map','0:a:0','-c','copy','-f','hash','-hash','sha256','-']).stdout.decode().strip())
assert audio[0]==audio[1]
# Exact decoded frame numbers; collect motion samples and both adjacent splice frames.
offsets=[-12,-1,0,3,6,9,12,15,18,21,24,27,29,30,31,42];frames=sorted({s+o for s in [2400,3240,4080,7020] for o in offsets})
select='+'.join(f'eq(n,{f})' for f in frames);run([ff,'-nostdin','-v','error','-i',str(F),'-map','0:v:0','-vf',f"select='{select}'",'-vsync','0','-q:v','2',str(Q/'selected-%03d.jpg')]);records=[]
for i,f in enumerate(frames,1):
 source=Q/f'selected-{i:03d}.jpg';records.append({'frame':f,'time':f/60,'path':str(source),'sha256':sha(source)})
for j,start in enumerate([2400,3240,4080,7020]):
 group=[r for r in records if start-12<=r['frame']<=start+42]
 for k in range(0,len(group),8):
  im=Image.new('RGB',(1080,1024),'#333333');d=ImageDraw.Draw(im)
  for i,r in enumerate(group[k:k+8]):
   a=Image.open(r['path']);a.thumbnail((270,480));x=i%4*270;y=i//4*512;im.paste(a,(x,y));d.text((x+8,y+486),f"F{r['frame']}  {r['time']:.4f}s",fill='white')
  im.save(Q/f'range-{j+1}-{k//8+1}.jpg',quality=93)
(Q/'frame-index.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
# Four same-clock comparisons. Original QA evidence is read-only.
old=P.parents[1]/'05-质检/v2';pairs=[(2421,'issue-F2421.jpg'),(3255,'extra-049.jpg'),(4095,'extra-065.jpg'),(7035,'extra-121.jpg')];comp=[]
for frame,name in pairs:
 fresh=next(r for r in records if r['frame']==frame);im=Image.new('RGB',(1080,1010),'#333');d=ImageDraw.Draw(im)
 for i,f in enumerate([old/name,Path(fresh['path'])]):
  a=Image.open(f);a.thumbnail((540,960));im.paste(a,(540*i,0));d.text((540*i+15,978),f'{"V2 RETURNED" if i==0 else "V2 FIX1"} | F{frame}',fill='white')
 dest=Q/f'compare-F{frame}.jpg';im.save(dest,quality=94);comp.append({'frame':frame,'path':str(dest),'sha256':sha(dest),'old':str(old/name),'new':fresh['path']})
r={'artifact':str(F),'sha256':sha(F),'width':v['width'],'height':v['height'],'fps':v['r_frame_rate'],'avg_fps':v['avg_frame_rate'],'frames':v['nb_frames'],'video_duration':v['duration'],'audio_duration':a['duration'] if isinstance(a,dict) else next(s for s in meta['streams'] if s['codec_type']=='audio')['duration'],'audio_sample_rate':'48000','full_decode':'PASS','full_decode_errors':dec.stderr.decode(),'audio_stream_hashes':audio,'audio_stream_exact_match':True,'extracted_frames':len(records),'comparisons':comp,'actual_image_review':'PENDING','normal_speed_continuous':'NOT_PERFORMED','direct_hearing':'NOT_PERFORMED'}
(Q/'export-check.json').write_text(json.dumps(r,ensure_ascii=False,indent=2));print({k:v for k,v in r.items() if k not in ['comparisons','audio_stream_hashes']})
