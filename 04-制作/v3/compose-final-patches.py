from pathlib import Path
import json,subprocess,hashlib
P=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
inputs=[P/'output/canvas-full-visual.mp4',P/'output/canvas-labels-a-visual.mp4',P/'output/canvas-labels-b-visual.mp4',P/'output/canvas-labels-c-visual.mp4',P/'output/canvas-seam-b-visual.mp4'];out=P/'output/canvas-final-visual.mp4'
graph='[0:v]split=5[a][b][c][d][e];[a]trim=start_frame=0:end_frame=1620,setpts=PTS-STARTPTS[a0];[b]trim=start_frame=1980:end_frame=2760,setpts=PTS-STARTPTS[a1];[c]trim=start_frame=2844:end_frame=5280,setpts=PTS-STARTPTS[a2];[d]trim=start_frame=5736:end_frame=6996,setpts=PTS-STARTPTS[a3];[e]trim=start_frame=7104:end_frame=9000,setpts=PTS-STARTPTS[a4];[1:v]setpts=PTS-STARTPTS[p0];[2:v]setpts=PTS-STARTPTS[p1];[3:v]setpts=PTS-STARTPTS[p2];[4:v]setpts=PTS-STARTPTS[p3];[a0][p0][a1][p1][a2][p2][a3][p3][a4]concat=n=9:v=1:a=0[v]'
cmd=['/Users/USER/.local/bin/ffmpeg','-nostdin','-hide_banner','-n']
for i in inputs:cmd+=['-i',str(i)]
cmd+=['-filter_complex',graph,'-map','[v]','-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-r','60','-frames:v','9000','-movflags','+faststart',str(out)]
with (P/'qc/final-compose-encode.txt').open('w') as f:subprocess.run(cmd,check=True,stdout=f,stderr=f)
r={'renderedFrames':9000,'sourceSha256':sha(P/'src/World.ts'),'full_base_receipt':'qc/canvas-full-receipt.json','patch_receipts':['qc/canvas-labels-a-receipt.json','qc/canvas-labels-b-receipt.json','qc/canvas-labels-c-receipt.json','qc/canvas-seam-b-receipt.json'],'changed_frames':1008,'ranges_frames_end_exclusive':[[1620,1980],[2760,2844],[5280,5736],[6996,7104]],'inputs':[{'path':str(i),'sha256':sha(i)} for i in inputs],'output':str(out),'sha256':sha(out),'command':cmd,'note':'Unchanged visual ranges reused from full render; two camera and three local label changes replaced frame exactly in four disjoint ranges. One complete9000frame stream reencoded.'}
(P/'qc/canvas-final-composed-receipt.json').write_text(json.dumps(r,indent=2));print(json.dumps({'output':str(out),'sha256':sha(out)}))
