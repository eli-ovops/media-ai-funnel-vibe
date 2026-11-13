from pathlib import Path
import json,subprocess,hashlib
P=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
inputs=[P/'output/canvas-full-visual.mp4',P/'output/canvas-seam-a-visual.mp4',P/'output/canvas-seam-b-visual.mp4'];out=P/'output/canvas-patched-visual.mp4'
graph='[0:v]split=3[a][b][c];[a]trim=start_frame=0:end_frame=5280,setpts=PTS-STARTPTS[a0];[b]trim=start_frame=5736:end_frame=6996,setpts=PTS-STARTPTS[a1];[c]trim=start_frame=7104:end_frame=9000,setpts=PTS-STARTPTS[a2];[1:v]setpts=PTS-STARTPTS[p0];[2:v]setpts=PTS-STARTPTS[p1];[a0][p0][a1][p1][a2]concat=n=5:v=1:a=0[v]'
cmd=['/Users/USER/.local/bin/ffmpeg','-nostdin','-hide_banner','-n']
for i in inputs:cmd+=['-i',str(i)]
cmd+=['-filter_complex',graph,'-map','[v]','-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-r','60','-frames:v','9000','-movflags','+faststart',str(out)]
with (P/'qc/patch-compose-encode.txt').open('w') as f:subprocess.run(cmd,check=True,stdout=f,stderr=f)
r={'renderedFrames':9000,'sourceSha256':sha(P/'src/World.ts'),'full_base_receipt':'qc/canvas-full-receipt.json','patch_receipts':['qc/canvas-seam-a-receipt.json','qc/canvas-seam-b-receipt.json'],'changed_frames':564,'ranges_frames_end_exclusive':[[5280,5736],[6996,7104]],'inputs':[{'path':str(i),'sha256':sha(i)} for i in inputs],'output':str(out),'sha256':sha(out),'command':cmd,'note':'Unchanged visual ranges reused from full render; two camera ranges replaced frame exactly. One complete9000frame stream reencoded.'}
(P/'qc/canvas-composed-receipt.json').write_text(json.dumps(r,indent=2));print(json.dumps({'output':str(out),'sha256':sha(out)}))
