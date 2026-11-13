from pathlib import Path
import json,os,subprocess,hashlib
P=Path(__file__).resolve().parent;v=P/'output/ai-funnel-v4-representative-36s-silent.mp4';q=P/'qc';c=(P/'node_modules/@remotion/compositor-darwin-arm64').resolve();env=os.environ.copy();env['DYLD_LIBRARY_PATH']=str(c)
r=subprocess.run([str(c/'ffprobe'),'-v','error','-show_streams','-show_format','-of','json',str(v)],capture_output=True,text=True,env=env,check=True);d=json.loads(r.stdout);(q/'ffprobe.json').write_text(r.stdout)
s=d['streams'][0];assert s['width']==1080 and s['height']==1920 and s['r_frame_rate']=='60/1' and s['nb_frames']=='2160';assert len(d['streams'])==1;assert abs(float(d['format']['duration'])-36)<.001
r=subprocess.run(['/Users/USER/.local/bin/ffmpeg','-nostdin','-v','error','-i',str(v),'-f','null','-'],capture_output=True,text=True);(q/'decode.log').write_text(r.stderr);assert r.returncode==0
frames=[60,180,285,450,570,630,660,690,710,719,720,750,780,810,960,1139,1140,1169,1170,1200,1260,1380,1425,1460,1499,1500,1510,1520,1530,1540,1550,1590,1660,1740,1800,1860,1980,2159]
folder=q/'export-frames';folder.mkdir(exist_ok=True)
expr='+'.join(f'eq(n,{f})'for f in frames)
subprocess.run(['/Users/USER/.local/bin/ffmpeg','-nostdin','-n','-loglevel','error','-i',str(v),'-vf',f'select={expr.replace(",",chr(92)+",")}','-fps_mode','vfr',str(folder/'sample-%03d.png')],check=True)
records=[]
for i,f in enumerate(frames,1):
 src=folder/f'sample-{i:03}.png';records.append({'frame':f,'time_sec':f/60,'path':str(src),'sha256':hashlib.sha256(src.read_bytes()).hexdigest()})
(q/'export-frame-index.json').write_text(json.dumps(records,indent=2))
result={'video':str(v),'sha256':hashlib.sha256(v.read_bytes()).hexdigest(),'bytes':v.stat().st_size,'width':1080,'height':1920,'fps':'60/1','frames':2160,'duration':36,'audioStreams':0,'completeDecode':'PASS','exportSamples':len(records),'continuousVisual':'NOT_PERFORMED','PMOAcceptance':'PENDING','libraryGate':'FAIL: installed catalog marks locally owned paid sources needs-auth and lacks TypeScript at its fixed runtime path; unmodified result retained. Actual local modules compile/render; isolated AST check separate.'}
(q/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps(result,ensure_ascii=False))
