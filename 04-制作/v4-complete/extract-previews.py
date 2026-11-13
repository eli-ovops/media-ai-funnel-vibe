from pathlib import Path
import subprocess,json,hashlib
P=Path(__file__).resolve().parent;Q=P/'qc/preview-frames-r4';Q.mkdir(exist_ok=True);rows=[]
for video in sorted((P/'output').glob('preview-r4-*.mp4')):
 a,b=map(int,video.stem.split('-')[-2:]);tmp=Q/video.stem;tmp.mkdir(exist_ok=True)
 subprocess.run(['/Users/USER/.local/bin/ffmpeg','-nostdin','-v','error','-i',str(video),'-vf','select=not(mod(n\,12))','-vsync','0',str(tmp/'%04d.png')],check=True)
 for j,f in enumerate(sorted(tmp.glob('*.png'))):
  frame=a+j*12;out=Q/f'F{frame}.png';out.write_bytes(f.read_bytes());rows.append(dict(frame=frame,time_sec=frame/60,path=str(out),video=str(video),sha256=hashlib.sha256(out.read_bytes()).hexdigest()))
(P/'qc/preview-frame-index.json').write_text(json.dumps(rows,indent=2));print(len(rows))
