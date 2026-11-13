import json,subprocess,hashlib,os
from pathlib import Path
P=Path(__file__).resolve().parent
rows=[r for r in json.loads((P/"inspection.json").read_text()) if r["id"] in (2,3)]
Q=P/"two-evidence";Q.mkdir(exist_ok=True)
images=[]
C=(P.parent/"v4-fix1/node_modules/@remotion/compositor-darwin-arm64").resolve()
env=os.environ.copy();env["DYLD_LIBRARY_PATH"]=str(C)
for row,r in enumerate(rows):
    f=Path(r["path"]);assert hashlib.sha256(f.read_bytes()).hexdigest()==r["sha256"]
    proc=subprocess.run([str(C/"ffprobe"),"-v","error","-show_format","-show_streams","-of","json",str(f)],capture_output=True,text=True,check=True,env=env)
    (Q/f'id{r["id"]}-ffprobe.json').write_text(proc.stdout)
    for col,t in enumerate([5,19,30]):
        out=Q/f'id{r["id"]}-{t}s.png'
        subprocess.run(["/Users/USER/.local/bin/ffmpeg","-v","error","-nostdin","-ss",str(t),"-i",str(f),"-frames:v","1",str(out)],check=True)
        images.append(out)
args=[]
for f in images:args+=["-i",str(f)]
filters=[f"[{i}:v]scale=180:320[s{i}]" for i in range(6)]
filters+=["[s0][s1][s2][s3][s4][s5]xstack=inputs=6:layout=0_0|180_0|360_0|0_320|180_320|360_320[out]"]
subprocess.run(["/Users/USER/.local/bin/ffmpeg","-v","error","-nostdin",*args,"-filter_complex",";".join(filters),"-map","[out]","-frames:v","1",str(Q/"contact.png")],check=True)
print("2 SHA matched; metadata and 6 sampled frames saved")
