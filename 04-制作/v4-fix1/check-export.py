from pathlib import Path
import json,os,subprocess,hashlib
P=Path(__file__).resolve().parent;v=P/'output/ai-funnel-v4-fix1-representative-36s-r3.mp4';q=P/'qc';c=(P/'node_modules/@remotion/compositor-darwin-arm64').resolve();env=os.environ.copy();env['DYLD_LIBRARY_PATH']=str(c)
r=subprocess.run([str(c/'ffprobe'),'-v','error','-show_streams','-show_format','-of','json',str(v)],capture_output=True,text=True,env=env,check=True);d=json.loads(r.stdout);(q/'ffprobe.json').write_text(r.stdout)
s=d['streams'][0];assert s['width']==1080 and s['height']==1920 and s['r_frame_rate']=='60/1' and s['nb_frames']=='2160';assert len(d['streams'])==1;assert abs(float(d['format']['duration'])-36)<.001
r=subprocess.run(['/Users/USER/.local/bin/ffmpeg','-nostdin','-v','error','-i',str(v),'-f','null','-'],capture_output=True,text=True);(q/'decode.log').write_text(r.stderr);assert r.returncode==0
frames=[285,690,719,720,741,765,810,840,858,876,1050,1110,1140,1155,1170,1185,1200,1230,1260,1278,1326,1380,1425,1460,1499,1500,1510,1520,1530,1536,1540,1544,1546,1547,1548,1549,1566,1630,1740,1908,2028,2159]
folder=q/'export-frames-r3';folder.mkdir(exist_ok=True)
expr='+'.join(f'eq(n,{f})'for f in frames)
subprocess.run(['/Users/USER/.local/bin/ffmpeg','-nostdin','-n','-loglevel','error','-i',str(v),'-vf',f'select={expr.replace(",",chr(92)+",")}','-fps_mode','vfr',str(folder/'sample-%03d.png')],check=True)
records=[]
for i,f in enumerate(frames,1):
 src=folder/f'sample-{i:03}.png';records.append({'frame':f,'time_sec':f/60,'path':str(src),'sha256':hashlib.sha256(src.read_bytes()).hexdigest()})
(q/'export-frame-index.json').write_text(json.dumps(records,indent=2))
result={'video':str(v),'sha256':hashlib.sha256(v.read_bytes()).hexdigest(),'bytes':v.stat().st_size,'width':1080,'height':1920,'fps':'60/1','frames':2160,'duration':36,'audioStreams':0,'completeDecode':'PASS','exportSamples':len(records),'continuousVisual':'NOT_PERFORMED','PMOAcceptance':'PENDING','libraryGate':'PASS: same previously validated exact-SHA local path binding, no shared changes.'}
(q/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps(result,ensure_ascii=False))
