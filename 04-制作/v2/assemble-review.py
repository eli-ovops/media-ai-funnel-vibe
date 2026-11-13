from pathlib import Path
import json,hashlib,subprocess,time
P=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();fix=json.loads((P/'qc/final-transition-fixes.json').read_text())
assert sha(P/'src/World.ts')==fix['final_source_sha256']
for name,n in [('explain',450),('slot',30),('reunite',30)]:
 r=json.loads((P/f'qc/canvas-{name}-receipt.json').read_text());assert r['renderedFrames']==n and r['sourceSha256']==fix['final_source_sha256']
base=P/'output/canvas-final-visual.mp4';out=P/'output/ai-funnel-v2-review-150s.mp4';assert not out.exists()
files=[base]+[P/f'output/canvas-{n}-visual.mp4' for n in ['explain','slot','reunite']]+[P/'output/code-sfx-v2.wav']
f='[0:v]split=4[a][b][c][d];[a]trim=start_frame=0:end_frame=4920,setpts=PTS-STARTPTS[v0];[1:v]setpts=PTS-STARTPTS[v1];[b]trim=start_frame=5370:end_frame=6180,setpts=PTS-STARTPTS[v2];[2:v]setpts=PTS-STARTPTS[v3];[c]trim=start_frame=6210:end_frame=8340,setpts=PTS-STARTPTS[v4];[3:v]setpts=PTS-STARTPTS[v5];[d]trim=start_frame=8370:end_frame=9000,setpts=PTS-STARTPTS[v6];[v0][v1][v2][v3][v4][v5][v6]concat=n=7:v=1:a=0[out]'
cmd=['/Users/USER/.local/bin/ffmpeg','-nostdin','-hide_banner']
for file in files:cmd+=['-i',str(file)]
cmd+=['-filter_complex',f,'-map','[out]','-map','4:a:0','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-r','60','-frames:v','9000','-c:a','aac','-b:a','192k','-t','150','-movflags','+faststart',str(out)]
t0=time.time()
with (P/'qc/review-assembly.log').open('w') as log:subprocess.run(cmd,check=True,stdout=log,stderr=subprocess.STDOUT)
r={'final':str(out),'sha256':sha(out),'source_sha256':fix['final_source_sha256'],'input_files':[{'path':str(x),'sha256':sha(x)} for x in files],'changed_ranges':fix['ranges'],'command':cmd,'wall_seconds':time.time()-t0,'basis':'Prior 9000-frame composite retained; 510 frames replaced at same60fps source clock; no whole-scene dissolve or retiming'}
(P/'qc/final-assembly.json').write_text(json.dumps(r,ensure_ascii=False,indent=2));print(r['sha256'])
