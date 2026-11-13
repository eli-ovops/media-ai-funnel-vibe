from pathlib import Path
import subprocess,json,hashlib
P=Path(__file__).resolve().parent
base=P.parent/'v4-complete/output/ai-funnel-v4-complete-150s-r5.mp4'
patch=P/'output/preview-r1-5040-8999.mp4'
out=P/'output/ai-funnel-v4-repair1-150s-r1.mp4'
cmd=['/Users/USER/.local/bin/ffmpeg','-nostdin','-n','-v','warning','-i',str(base),'-i',str(patch),
 '-filter_complex','[0:v]trim=start_frame=0:end_frame=5040,setpts=PTS-STARTPTS[a];[1:v]setpts=PTS-STARTPTS[b];[a][b]concat=n=2:v=1:a=0,format=yuv420p[out]',
 '-map','[out]','-an','-c:v','libx264','-preset','fast','-crf','16','-r','60','-video_track_timescale','15360','-movflags','+faststart',str(out)]
r=subprocess.run(cmd,capture_output=True,text=True)
(P/'qc/assembly.log').write_text(r.stderr);r.check_returncode()
rec=lambda f:dict(path=str(f),sha256=hashlib.sha256(f.read_bytes()).hexdigest())
(P/'qc/assembly.json').write_text(json.dumps(dict(inputs=[rec(base),rec(patch)],output=rec(out),protectedContentFramesExclusive=[0,5040],reRenderedFramesExclusive=[5040,9000],method='Exact original 60fps clock; protected0-84s decoded from frozen r5; concat then unified H264 encode, not byte-identical output',sources=[rec(P/'src/FullEpisode.tsx'),rec(P/'src/RepairScenes.tsx')]),indent=2))
print(json.dumps(rec(out)))
