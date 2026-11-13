from pathlib import Path
import subprocess,json,hashlib
P=Path(__file__).resolve().parent;O=P/'output';base=O/'ai-funnel-v4-complete-150s-r4.mp4'
patches=[(1380,1458),(2100,2178),(8445,8478)];files=[base]+[O/f'preview-r5-{a}-{b-1}.mp4' for a,b in patches]
cmd=['/Users/USER/.local/bin/ffmpeg','-nostdin','-n','-v','warning']
for f in files:cmd+=['-i',str(f)]
fc='[0:v]split=4[a][b][c][d];[a]trim=start_frame=0:end_frame=1380,setpts=PTS-STARTPTS[v0];[1:v]setpts=PTS-STARTPTS[v1];[b]trim=start_frame=1458:end_frame=2100,setpts=PTS-STARTPTS[v2];[2:v]setpts=PTS-STARTPTS[v3];[c]trim=start_frame=2178:end_frame=8445,setpts=PTS-STARTPTS[v4];[3:v]setpts=PTS-STARTPTS[v5];[d]trim=start_frame=8478:end_frame=9000,setpts=PTS-STARTPTS[v6];[v0][v1][v2][v3][v4][v5][v6]concat=n=7:v=1:a=0,format=yuv420p[out]'
out=O/'ai-funnel-v4-complete-150s-r5.mp4'
cmd+=['-filter_complex',fc,'-map','[out]','-an','-c:v','libx264','-preset','fast','-crf','16','-r','60','-video_track_timescale','15360','-movflags','+faststart',str(out)]
r=subprocess.run(cmd,capture_output=True,text=True);(P/'qc/assembly-r5.log').write_text(r.stderr);r.check_returncode()
rec=lambda f:dict(path=str(f),sha256=hashlib.sha256(f.read_bytes()).hexdigest())
(P/'qc/assembly-r5.json').write_text(json.dumps(dict(inputs=[rec(f) for f in files],patchFrameRangesExclusive=patches,output=rec(out),method='Frame-exact trim/concat at original 60fps clock; final H264 encode at CRF16; unchanged content inherited from r4, encoded bytes not expected identical',expectedFrames=9000,source=rec(P/'src/FullEpisode.tsx')),indent=2));print('Assembled r5')
