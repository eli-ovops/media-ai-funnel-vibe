from pathlib import Path
import subprocess,json,hashlib,time
P=Path(__file__).resolve().parent;B=P.parent/'v2';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();scope=json.loads((P/'qc/scope.json').read_text());base=Path(scope['base_artifact']);assert sha(base)==scope['base_sha256'];world=sha(P/'src/World.ts')
names=['q1a','q1b','q1c','q2'];clips=[P/f'output/canvas-{x}-visual.mp4' for x in names]
for n,(a,b) in zip(names,scope['ranges_frames']):
 r=json.loads((P/f'qc/canvas-{n}-receipt.json').read_text());assert r['startFrame']==a and r['endFrameExclusive']==b and r['renderedFrames']==30 and r['sourceSha256']==world
out=P/'output/ai-funnel-v2-fix1-internal-150s.mp4';assert not out.exists()
segments=[];filters=['[0:v]split=5[b0][b1][b2][b3][b4]'];previous=0
for i,(a,b) in enumerate(scope['ranges_frames']):
 filters += [f'[b{i}]trim=start_frame={previous}:end_frame={a},setpts=PTS-STARTPTS[s{i*2}]',f'[{i+1}:v]setpts=PTS-STARTPTS[s{i*2+1}]'];segments += [[previous,a,'base'],[a,b,names[i]]];previous=b
filters += [f'[b4]trim=start_frame={previous}:end_frame=9000,setpts=PTS-STARTPTS[s8]',''.join(f'[s{i}]' for i in range(9))+'concat=n=9:v=1:a=0[out]'];segments.append([previous,9000,'base'])
cmd=['/Users/USER/.local/bin/ffmpeg','-nostdin','-hide_banner']
for f in [base]+clips:cmd+=['-i',str(f)]
cmd+=['-filter_complex',';'.join(filters),'-map','[out]','-map','0:a:0','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-r','60','-frames:v','9000','-c:a','copy','-t','150','-movflags','+faststart',str(out)]
t=time.time()
with (P/'qc/assembly.log').open('w') as log:subprocess.run(cmd,check=True,stdout=log,stderr=subprocess.STDOUT)
r={'artifact':str(out),'sha256':sha(out),'sourceSha256':world,'baseSha256':sha(base),'baseSourceSha256':scope['base_source_sha256'],'patches':[{'path':str(f),'sha256':sha(f),'frames':30} for f in clips],'segments':segments,'endExclusive':True,'totalPatchedFrames':120,'command':cmd,'wallSeconds':time.time()-t,'audio':'Copied original AAC stream; no mixing, regeneration, gain or event edits'}
(P/'qc/assembly.json').write_text(json.dumps(r,ensure_ascii=False,indent=2));print(r['sha256'])
