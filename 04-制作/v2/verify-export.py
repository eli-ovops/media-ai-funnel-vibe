from pathlib import Path
import subprocess,json,hashlib,os,math
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;F=P/'output/ai-funnel-v2-internal-150s.mp4';Q=P/'qc/final';Q.mkdir(exist_ok=True)
ff='/Users/USER/.local/bin/ffmpeg'
probe=P/'node_modules/@remotion/compositor-darwin-arm64/ffprobe';env=os.environ.copy();env['DYLD_LIBRARY_PATH']=str(probe.parent.resolve())
def run(args,**kw):return subprocess.run(args,check=True,capture_output=True,**kw)
meta=json.loads(run([str(probe),'-v','error','-show_streams','-show_format','-of','json',str(F)],env=env).stdout);(Q/'metadata.json').write_text(json.dumps(meta,indent=2))
decode=run([ff,'-nostdin','-v','error','-xerror','-i',str(F),'-progress','pipe:1','-f','null','-']);(Q/'decode-progress.txt').write_bytes(decode.stdout);(Q/'decode-errors.txt').write_bytes(decode.stderr)
c=json.loads((P/'content-package.json').read_text());times=[round((s['reading_start_sec']+s['reading_end_sec'])/2,3) for s in c['scenes']]
# Adjacent chapter midpoints and finer steps at the branching / save / access transformations.
seams=[27.5,40.5,54.167,54.833,61.167,68.5,72.0,75.0,89.5,103.5,117.5,124.5,139.5,146.35,12.0,12.167,12.35,20.167,33.167,46.167,54.5,55.25,56.5,68.6,69.4,71.8,74.983,75.25,75.5,81.983,82.167,82.5,89.167,90.9,92.4,93.2,93.6,94.4,103.167,104.5,110.6,111.8,114.6,117.167,124.167,124.8,126.1,132.5,139.167,145.8,146.2,146.5,149.983]
records=[]
for t in sorted(set(times+seams)):
 f=Q/f'frame-{t:.3f}.jpg';run([ff,'-nostdin','-v','error','-ss',str(t),'-i',str(F),'-frames:v','1','-q:v','2',str(f)]);records.append({'second':t,'path':str(f),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
def sheet(ts,name,cols=4):
 out=Image.new('RGB',(cols*270,520*math.ceil(len(ts)/cols)),'#272727');d=ImageDraw.Draw(out)
 for i,t in enumerate(ts):
  im=Image.open(Q/f'frame-{t:.3f}.jpg');im.thumbnail((270,480));x=i%cols*270;y=i//cols*520;out.paste(im,(x,y));d.text((x+9,y+488),f'{t:.3f}s',fill='white')
 out.save(Q/name,quality=93)
for k in range(0,len(times),8):sheet(times[k:k+8],f'content-{k//8+1}.jpg')
for k in range(0,len(seams),8):sheet(seams[k:k+8],f'seams-{k//8+1}.jpg')
v=next(s for s in meta['streams'] if s['codec_type']=='video');a=next(s for s in meta['streams'] if s['codec_type']=='audio')
result={'artifact':str(F),'sha256':hashlib.sha256(F.read_bytes()).hexdigest(),'width':v['width'],'height':v['height'],'r_frame_rate':v['r_frame_rate'],'avg_frame_rate':v['avg_frame_rate'],'nb_frames':v.get('nb_frames'),'video_duration':v.get('duration'),'audio_duration':a.get('duration'),'audio_codec':a['codec_name'],'audio_sample_rate':a['sample_rate'],'format_duration':meta['format']['duration'],'full_decode':'PASS','full_decode_errors':decode.stderr.decode(),'extracted_frames':len(records),'frame_records':records,'visual_review':'PENDING_ACTUAL_IMAGE_INSPECTION','normal_speed_continuous_visual':'NOT_PERFORMED','direct_hearing':'NOT_PERFORMED','specified_music':'MISSING'}
(Q/'export-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print({k:v for k,v in result.items() if k!='frame_records'})
