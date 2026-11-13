import json,os,stat,hashlib,subprocess,datetime
from pathlib import Path
ROOT=Path("/Volumes/EXTERNAL/自媒体/ai-funnel-vibe-20261020")
OUT=Path(__file__).resolve().parent
def now():return datetime.datetime.now().astimezone().isoformat()
def save(name,obj):(OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n")
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
rows=json.loads((OUT/"reviewed-candidates.json").read_text())
inventory=json.loads((ROOT/"06-发布准备/PMO-发布完成清理前只读视频范围.json").read_text())
allowed={x["path"] for x in inventory["paths"]}
assert len(allowed)==56 and len(rows)==56
assert not (OUT/"deletion-results.json").exists(),"Do not repeat an executed deletion"
protected=[
 Path("/Users/USER/Downloads/微信视频2026-10-20_201157_614.mp4"),
 ROOT/"04-制作/v4-repair1/src/FullEpisode.tsx",
 ROOT/"04-制作/v4-repair1/src/RepairScenes.tsx",
 ROOT/"04-制作/v4-repair1/render.cjs",
 ROOT/"04-制作/v4-repair1/runtime.json",
 ROOT/"04-制作/v4-repair1/delivery-index.json",
 ROOT/"04-制作/v4-repair1/screen-script.txt",
 ROOT/"04-制作/output/code-sfx-v1.wav",
 ROOT/"01-七条Vibe参考/文件清单.json",
 ROOT/"06-发布准备/07-本期发布收口索引.json",
 ROOT/"06-发布准备/带音频版核验/带音乐高清版核验.json",
 ROOT.parent/"资产库/FredTalk/manifest.json",
]
for r in json.loads((ROOT/"04-制作/covers-v4/manifest.json").read_text()):protected.append(Path(r["file"]))
before_protected=[{"path":str(p),"exists":p.exists(),"sha256":sha(p) if p.is_file() else None} for p in protected]
assert all(r["exists"] for r in before_protected)
assert before_protected[0]["sha256"]=="b207dc5196bec1cfc1e866a2c727a83e6cc7300563b38a39a266bb7db5d49b95"
save("protected-before.json",before_protected)
# Sources for every eligible output must still be the inspected evidence.
for r in rows:
    assert r["path"] in allowed
    if r["decision"]=="ELIGIBLE":
        assert sha(Path(r["source_evidence"]))==r["source_evidence_sha256"]
def df(label):
    r=subprocess.run(["df","-kP",str(ROOT)],capture_output=True,text=True,check=True)
    parts=r.stdout.splitlines()[-1].split()
    obj={"at":now(),"command":["df","-kP",str(ROOT)],"unit_bytes":1024,"stdout":r.stdout,"stderr":r.stderr,"filesystem":parts[0],"available_blocks":int(parts[3]),"mount":parts[-1]}
    save("df-"+label+".json",obj)
    (OUT/("df-"+label+".txt")).write_text(obj["at"]+"\n"+r.stdout)
    return obj
before=df("before")
results=[]
for r in rows:
    p=Path(r["path"])
    result={k:r[k] for k in ("id","path","bytes","sha256","source_evidence","decision","reason")}
    if r["decision"]!="ELIGIBLE":
        result["result"]="RETAINED";results.append(result);continue
    try:
        assert p.resolve()==p and ROOT in p.parents and not any(q.is_symlink() for q in [p,*p.parents])
        fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
        try:
            st=os.fstat(fd)
            assert stat.S_ISREG(st.st_mode) and st.st_nlink==1
            assert (st.st_dev,st.st_ino,st.st_size,st.st_mtime_ns)==(r["dev"],r["inode"],r["bytes"],r["mtime_ns"])
            h=hashlib.sha256()
            while chunk:=os.read(fd,1048576):h.update(chunk)
            assert h.hexdigest()==r["sha256"]
        finally:os.close(fd)
        handles=subprocess.run(["/usr/sbin/lsof","-nP","-Fpcfn","--",str(p)],capture_output=True,text=True)
        result["last_handle_check"]={"at":now(),"code":handles.returncode,"stdout":handles.stdout,"stderr":handles.stderr}
        assert handles.returncode==1 and not handles.stdout and not handles.stderr,"Active/uncertain handle"
        st2=p.lstat()
        assert (st2.st_dev,st2.st_ino,st2.st_size,st2.st_mtime_ns)==(r["dev"],r["inode"],r["bytes"],r["mtime_ns"])
        p.unlink()
        assert not p.exists() and not p.is_symlink()
        result["result"]="DELETED";result["at"]=now()
    except Exception as e:
        result["result"]="RETAINED";result["reason"]=repr(e)
    results.append(result)
    save("deletion-results.json",results)
save("deletion-results.json",results)
after=df("after")
after_protected=[{"path":r["path"],"exists":Path(r["path"]).exists(),"sha256":sha(Path(r["path"])) if Path(r["path"]).is_file() else None,"unchanged":Path(r["path"]).is_file() and sha(Path(r["path"]))==r["sha256"]} for r in before_protected]
save("protected-after.json",after_protected)
deleted=[r for r in results if r["result"]=="DELETED"]
retained=[r for r in results if r["result"]!="DELETED"]
assert before["filesystem"]==after["filesystem"] and before["mount"]==after["mount"]
summary={"at":now(),"candidate_count":56,"deleted_count":len(deleted),"deleted_logical_bytes":sum(r["bytes"] for r in deleted),"retained_count":len(retained),"retained_logical_bytes":sum(r["bytes"] for r in retained),"df_available_delta_bytes":(after["available_blocks"]-before["available_blocks"])*1024,"df_note":"Observed filesystem available-space change only; allocation/APFS/concurrent activity may affect attribution.","protected_selected_all_unchanged":all(r["unchanged"] for r in after_protected),"actual_model":"UNKNOWN","actual_effort":"UNKNOWN"}
save("清理报告.json",summary);print(json.dumps(summary,ensure_ascii=False,indent=2))
