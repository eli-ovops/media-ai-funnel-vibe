from pathlib import Path
import os,subprocess,json,hashlib
P=Path(__file__).resolve().parent
V=P/'output/ai-funnel-v4-complete-150s-r5.mp4';Q=P/'qc'
probe=(P/'node_modules/@remotion/compositor-darwin-arm64/ffprobe').resolve()
env={**os.environ,'DYLD_LIBRARY_PATH':str(probe.parent)}
raw=subprocess.check_output([str(probe),'-v','error','-show_streams','-show_format','-of','json',str(V)],env=env)
data=json.loads(raw);(Q/'ffprobe-full.json').write_bytes(raw)
v=next(s for s in data['streams'] if s['codec_type']=='video')
audios=[s for s in data['streams'] if s['codec_type']=='audio']
checks={'width':v['width']==1080,'height':v['height']==1920,'native60':v['r_frame_rate']=='60/1' and v['avg_frame_rate']=='60/1','frames9000':int(v['nb_frames'])==9000,'duration150':abs(float(data['format']['duration'])-150)<.001,'silent':len(audios)==0}
decode=subprocess.run(['/Users/USER/.local/bin/ffmpeg','-nostdin','-v','error','-i',str(V),'-f','null','-'],capture_output=True,text=True)
(Q/'decode-full.log').write_text(decode.stderr);checks['completeDecode']=decode.returncode==0
frames=sorted(set(list(range(1368,1471,6))+list(range(2088,2191,6))+list(range(8433,8491,3))+[2040,3210,3560,3588,4200,4500,6210,7950,8999]))
temp=Q/'export-raw-r5';temp.mkdir(exist_ok=True)
out=Q/'export-frames-r5';out.mkdir(exist_ok=True)
expr='+'.join(f'eq(n\\,{f})' for f in frames)
subprocess.run(['/Users/USER/.local/bin/ffmpeg','-nostdin','-v','error','-i',str(V),'-vf','select='+expr,'-vsync','0',str(temp/'%04d.png')],check=True)
files=sorted(temp.glob('*.png'));assert len(files)==len(frames)
rows=[]
for f,n in zip(files,frames):
 target=out/f'F{n}.png';target.write_bytes(f.read_bytes())
 rows.append(dict(frame=n,time_sec=n/60,path=str(target),sha256=hashlib.sha256(target.read_bytes()).hexdigest()))
(Q/'export-frame-index.json').write_text(json.dumps(rows,indent=2))
result=dict(status='PASS' if all(checks.values()) else 'FAIL',scope='Technical delivery and extracted samples only',checks=checks,video=dict(path=str(V),sha256=hashlib.sha256(V.read_bytes()).hexdigest(),bytes=V.stat().st_size,duration=data['format']['duration'],frames=v['nb_frames'],width=v['width'],height=v['height'],fps=v['avg_frame_rate'],audioStreams=len(audios)),extractedFrameCount=len(rows),continuousVisualReview='NOT_PERFORMED',directAudioReview='NOT_APPLICABLE_NO_AUDIO_STREAM',aestheticFinalAcceptance='PENDING_PMO_AND_05')
(Q/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps(result,ensure_ascii=False,indent=2))
assert all(checks.values())
