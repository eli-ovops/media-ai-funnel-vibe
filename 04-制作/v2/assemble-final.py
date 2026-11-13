from pathlib import Path
import json,hashlib,subprocess,time
P=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();ff='/Users/USER/.local/bin/ffmpeg'
base=P/'output/canvas-full-visual.mp4';patch=P/'output/canvas-item-visual.mp4';visual=P/'output/canvas-final-visual.mp4';final=P/'output/ai-funnel-v2-internal-150s.mp4'
a=json.loads((P/'qc/canvas-full-receipt.json').read_text());b=json.loads((P/'qc/canvas-item-receipt.json').read_text());fix=json.loads((P/'qc/item-continuity-fix.json').read_text())
assert a['renderedFrames']==9000 and b['renderedFrames']==810
assert a['sourceSha256']==sha(P/'qc/World-full-base.ts')==fix['base_source_sha256']
assert b['sourceSha256']==sha(P/'src/World.ts')==fix['final_source_sha256']
assert not visual.exists() and not final.exists(),'Preserve existing outputs; use a new version for further changes'
filters='[0:v]split=2[a][b];[a]trim=start_frame=0:end_frame=5400,setpts=PTS-STARTPTS[v0];[1:v]setpts=PTS-STARTPTS[v1];[b]trim=start_frame=6210:end_frame=9000,setpts=PTS-STARTPTS[v2];[v0][v1][v2]concat=n=3:v=1:a=0[out]'
cmd=[ff,'-nostdin','-hide_banner','-i',str(base),'-i',str(patch),'-filter_complex',filters,'-map','[out]','-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-r','60','-frames:v','9000','-movflags','+faststart',str(visual)]
t0=time.time()
with (P/'qc/assembly-encode.log').open('w') as f:subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,check=True)
mux=[ff,'-nostdin','-hide_banner','-i',str(visual),'-i',str(P/'output/code-sfx-v2.wav'),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-t','150','-movflags','+faststart',str(final)]
with (P/'qc/assembly-mux.log').open('w') as f:subprocess.run(mux,stdout=f,stderr=subprocess.STDOUT,check=True)
r={'base':str(base),'baseSha256':sha(base),'patch':str(patch),'patchSha256':sha(patch),'ranges':[[0,5400,'base'],[5400,6210,'patch'],[6210,9000,'base']],'endFrameExclusive':True,'baseSourceSha256':a['sourceSha256'],'finalSourceSha256':b['sourceSha256'],'visualSha256':sha(visual),'final':str(final),'finalSha256':sha(final),'assemblyCommand':cmd,'muxCommand':mux,'wallSeconds':time.time()-t0,'technicalValidation':'PENDING final full decode and metadata','continuousAVAcceptance':'NOT_CLAIMED'}
(P/'qc/assembly.json').write_text(json.dumps(r,ensure_ascii=False,indent=2));print(json.dumps({k:r[k] for k in ['final','finalSha256','wallSeconds']},ensure_ascii=False))
