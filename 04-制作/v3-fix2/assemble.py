from pathlib import Path
import subprocess,json,hashlib
P=Path(__file__).resolve().parent;FF='/Users/USER/.local/bin/ffmpeg';base=P.parent/'v3-fix1/output/ai-funnel-v3-fix1-review-150s.mp4';out=P/'output/ai-funnel-v3-fix2-review-150s.mp4'
f='[0:v]split=3[a][b][c];[a]trim=start_frame=0:end_frame=1380,setpts=PTS-STARTPTS[a0];[1:v]setpts=PTS-STARTPTS[a1];[b]trim=start_frame=1620:end_frame=7884,setpts=PTS-STARTPTS[a2];[2:v]setpts=PTS-STARTPTS[a3];[c]trim=start_frame=8460:end_frame=9000,setpts=PTS-STARTPTS[a4];[a0][a1][a2][a3][a4]concat=n=5:v=1:a=0[v]'
cmd=[FF,'-nostdin','-hide_banner','-n','-i',str(base),'-i',str(P/'output/canvas-q1-visual.mp4'),'-i',str(P/'output/canvas-q2-visual.mp4'),'-filter_complex',f,'-map','[v]','-map','0:a:0','-c:v','libx264','-preset','fast','-crf','12','-pix_fmt','yuv420p','-threads','8','-c:a','copy','-frames:v','9000','-t','150','-movflags','+faststart',str(out)]
with (P/'qc/assembly.log').open('w') as log:subprocess.run(cmd,check=True,stdout=log,stderr=log)
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
(P/'qc/assembly.json').write_text(json.dumps({'command':cmd,'base':str(base),'base_sha256':sha(base),'output':str(out),'sha256':sha(out),'bytes':out.stat().st_size,'rendered_frame_ranges_inclusive':[[1380,1619],[7884,8459]],'source_camera_actually_changed':[7885,8459],'method':'frame-index trim/concat, unchanged ranges from base; full stream H264 reencode, AAC packet copy'},indent=2));print(sha(out))
