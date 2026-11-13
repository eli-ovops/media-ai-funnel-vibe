import json,os,subprocess,hashlib,datetime,stat
from pathlib import Path
ROOT=Path("/Volumes/EXTERNAL/自媒体/ai-funnel-vibe-20261020")
OUT=Path(__file__).resolve().parent
rows=json.loads((OUT/"inspection.json").read_text())
statepath=ROOT.parent/"流程协作/流程状态.json"
state=json.loads(statepath.read_text())
other={k:v for k,v in state.items() if k!="ai_funnel_vibe_20261020"}
other["runs"]={k:v for k,v in state.get("runs",{}).items() if k!="ai-funnel-vibe-20261020"}
refs=[]
def walk(v,trail=""):
    if isinstance(v,dict):
        for k,w in v.items():walk(w,trail+"/"+k)
    elif isinstance(v,list):
        for i,w in enumerate(v):walk(w,trail+"/"+str(i))
    elif isinstance(v,str) and any(r["path"] in v for r in rows):
        refs.append({"key":trail,"value":v})
walk(other)
(OUT/"other-state-references.json").write_text(json.dumps(refs,ensure_ascii=False,indent=2))
# Full paths passed directly as arguments; no shell expansion.
handle=subprocess.run(["/usr/sbin/lsof","-nP","-Fpcfn","--",*[r["path"] for r in rows]],capture_output=True,text=True)
(OUT/"handles-before.json").write_text(json.dumps({"at":datetime.datetime.now().astimezone().isoformat(),"args":"lsof -nP -Fpcfn -- [56 exact paths]","code":handle.returncode,"stdout":handle.stdout,"stderr":handle.stderr},ensure_ascii=False,indent=2))
ps=subprocess.run(["ps","-axo","pid=,comm="],capture_output=True,text=True)
processes=[s for s in ps.stdout.splitlines() if any(w in s.lower() for w in ["ffmpeg","remotion","render.cjs"])]
(OUT/"render-processes.json").write_text(json.dumps(processes,indent=2))
mapping={
0:"06-发布准备/带音频版核验/带音乐高清版核验.json",
1:"04-制作/v4-fix1/render.cjs",
4:"04-制作/v4-complete/assemble-r5.py",
5:"04-制作/v4-complete/render.cjs",
21:"04-制作/v2-fix1/assemble.py",
24:"04-制作/README.md",
27:"04-制作/qc/preflight-capability.json",
28:"04-制作/v3-fix1/compose.py",
29:"04-制作/v2/assemble-final.py",
31:"04-制作/v2/assemble-review.py",
38:"04-制作/v2/assemble-final.py",
39:"04-制作/v4/README.md",40:"04-制作/v4/README.md",
41:"04-制作/v3/post-render.py",42:"04-制作/v3/post-final-render.py",
45:"04-制作/v3/compose-camera-patches.py",50:"04-制作/v3/compose-final-patches.py",
51:"04-制作/v4-repair1/render.cjs",52:"04-制作/v4-repair1/assemble.py",
54:"04-制作/v3-fix2/assemble.py",
}
for n in range(6,18):mapping[n]="04-制作/v4-complete/render.cjs"
for r in rows:
    p=Path(r["path"]);n=r["id"]
    proof=mapping.get(n)
    if not proof:
        logs=[h for h in r["matches"] if "Output #0, mp4, to" in h["text"] and str(p) in h["text"]]
        if logs:proof=str(Path(logs[0]["file"]).relative_to(ROOT))
    r["source_evidence"]=str(ROOT/proof) if proof else None
    if proof:
        f=ROOT/proof
        r["source_evidence_sha256"]=hashlib.sha256(f.read_bytes()).hexdigest()
        r["source_basis"]="Explicit encoder output, render outputLocation/range mapping, assembly output, or historical generated-artifact record; see source evidence and inspection matches."
    r["decision"]="ELIGIBLE" if proof else "RETAIN"
    r["reason"]=None if proof else "No exact historical render/output record found for this old representative file; general README r1/r2 mention insufficient for precise provenance."
    st=p.lstat()
    if not stat.S_ISREG(st.st_mode) or p.is_symlink() or p.resolve()!=p or st.st_size!=r["bytes"] or st.st_nlink!=1:
        r["decision"]="RETAIN";r["reason"]="Identity/type/size/link check failed"
    if any(parent.is_symlink() for parent in p.parents):
        r["decision"]="RETAIN";r["reason"]="Symlink ancestor"
    if handle.returncode not in (0,1) or handle.stderr:
        r["decision"]="RETAIN";r["reason"]="Handle check uncertainty"
    if "n"+str(p)+"\n" in handle.stdout:
        r["decision"]="RETAIN";r["reason"]="Active file handle"
    if refs or processes:
        r["decision"]="RETAIN";r["reason"]="Review references/processes before execution"
(OUT/"reviewed-candidates.json").write_text(json.dumps(rows,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"refs":refs,"processes":processes,"handle_code":handle.returncode,"handle_stdout":handle.stdout,"handle_stderr":handle.stderr,"eligible":[r["id"] for r in rows if r["decision"]=="ELIGIBLE"],"retained":[{"id":r["id"],"reason":r["reason"]} for r in rows if r["decision"]!="ELIGIBLE"]},ensure_ascii=False,indent=2))
