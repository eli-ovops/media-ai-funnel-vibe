from pathlib import Path
import os,subprocess,json,hashlib
P=Path(__file__).resolve().parent;Q=P/'qc'
V=P/'output/ai-funnel-v4-repair1-150s-r1.mp4'
probe=(P/'node_modules/@remotion/compositor-darwin-arm64/ffprobe').resolve()
env={**os.environ,'DYLD_LIBRARY_PATH':str(probe.parent)}
raw=subprocess.check_output([str(probe),'-v','error','-show_streams','-show_format','-of','json',str(V)],env=env)
(Q/'ffprobe.json').write_bytes(raw);data=json.loads(raw)
v=next(s for s in data['streams'] if s['codec_type']=='video')
checks={'1080x1920':(v['width'],v['height'])==(1080,1920),'native60':v['r_frame_rate']==v['avg_frame_rate']=='60/1','9000frames':int(v['nb_frames'])==9000,'150seconds':abs(float(data['format']['duration'])-150)<.001,'silent':not any(s['codec_type']=='audio' for s in data['streams'])}
r=subprocess.run(['/Users/USER/.local/bin/ffmpeg','-nostdin','-v','error','-i',str(V),'-f','null','-'],capture_output=True,text=True)
(Q/'decode.log').write_text(r.stderr);checks['completeDecode']=r.returncode==0
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
record=dict(status='PASS' if all(checks.values()) else 'FAIL',scope='Technical only',checks=checks,video=dict(path=str(V),sha256=sha(V),bytes=V.stat().st_size,width=v['width'],height=v['height'],fps=v['avg_frame_rate'],frames=v['nb_frames'],duration=data['format']['duration'],audioStreams=0),normalSpeedContinuousVisual='NOT_PERFORMED',independent05='PENDING',userFinal='PENDING')
(Q/'verification.json').write_text(json.dumps(record,indent=2));print(json.dumps(record,indent=2));assert all(checks.values())
# Focus on changed66s and exact boundary. Routine samples1s, hazard intervals0.1s.
frames=set(range(5040,9000,60))|{5039,8999}
for a,b in [(90.3,91.6),(94.7,95.8),(98.3,99.8),(100.9,101.9),(102.9,105),(110.9,112),(115.9,118.3),(124,126),(139.9,141.8),(145.4,147.2)]:
 frames.update(range(round(a*60),round(b*60)+1,6))
frames=sorted(frames);temp=Q/'raw';temp.mkdir(exist_ok=True);dest=Q/'export';dest.mkdir(exist_ok=True)
expr='+'.join(f'eq(n\\,{f})' for f in frames)
subprocess.run(['/Users/USER/.local/bin/ffmpeg','-nostdin','-v','error','-i',str(V),'-vf','select='+expr,'-vsync','0',str(temp/'%04d.png')],check=True)
files=sorted(temp.glob('*.png'));assert len(files)==len(frames)
rows=[]
for f,n in zip(files,frames):
 target=dest/f'F{n}.png';f.rename(target)
 rows.append(dict(frame=n,time_sec=n/60,path=str(target),sha256=sha(target)))
(Q/'sample-index.json').write_text(json.dumps(rows,indent=2))
print('Extracted',len(rows),'actual final frames')
