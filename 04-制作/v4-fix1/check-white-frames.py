from pathlib import Path
import subprocess,json
import numpy as np
P=Path(__file__).resolve().parent;v=P/'output/ai-funnel-v4-fix1-representative-36s-r3.mp4'
r=subprocess.run(['/Users/USER/.local/bin/ffmpeg','-nostdin','-v','error','-i',str(v),'-vf','trim=start_frame=720:end_frame=1561,setpts=PTS-STARTPTS,scale=108:192,format=gray','-f','rawvideo','-'],capture_output=True,check=True)
a=np.frombuffer(r.stdout,np.uint8).reshape(-1,192,108);assert len(a)==841
nonwhite=(a<245).sum(axis=(1,2));bad=np.where(nonwhite<10)[0]+720
result={'rangeFramesInclusive':[720,1560],'framesChecked':len(a),'method':'Decode every frame in affected span;108x192 grayscale pixels<245; below10 nonwhite pixels flagged near-empty','nearEmptyFrames':bad.tolist(),'minNonwhitePixels':int(nonwhite.min()),'minAtFrame':int(nonwhite.argmin()+720),'claimLimit':'Only detects near-empty/full-white images; not a continuous visual or aesthetic review.'}
(P/'qc/white-frame-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result));assert len(bad)==0
