import json,hashlib,os,stat,datetime,subprocess
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
def now():return datetime.datetime.now().astimezone().isoformat()
def save(n,v):(P/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+"\n")
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert not (P/"two-deletion-results.json").exists()
rows=[r for r in json.loads((P/"inspection.json").read_text()) if r["id"] in (2,3)]
assert len(rows)==2
state=json.loads((ROOT.parent/"流程协作/流程状态.json").read_text())
state.pop("ai_funnel_vibe_20261020",None);state["runs"].pop("ai-funnel-vibe-20261020",None)
refs=[r["path"] for r in rows if r["path"] in json.dumps(state,ensure_ascii=False)]
assert not refs,"Other content reference"
save("two-dependencies.json",{"at":now(),"other_state_exact_refs":refs,"current_content":"User closed publication; old samples superseded by full v4-repair1; original source/render parameters retained","evidence":["two-history-matches.json","two-history-render-window.json","two-evidence/contact.png","../v4-fix1/src/Episode.tsx","../v4-fix1/src/index.tsx"]})
protected=[Path(r["path"]) for r in json.loads((P/"protected-before.json").read_text())]
protected += [q for q in (P.parent/"v4-fix1/src").rglob("*") if q.is_file() and not q.is_symlink()]
protected += [P.parent/"v4-fix1/render.cjs"]
before_protected=[{"path":str(p),"sha256":sha(p)} for p in protected]
save("two-protected-before.json",before_protected)
def df(label):
    r=subprocess.run(["df","-kP",str(ROOT)],capture_output=True,text=True,check=True)
    s=r.stdout.splitlines()[-1].split();d={"at":now(),"stdout":r.stdout,"unit_bytes":1024,"filesystem":s[0],"mount":s[-1],"available_blocks":int(s[3])}
    save("two-df-"+label+".json",d);return d
checks=[]
for r in rows:
    p=Path(r["path"]);s=p.lstat()
    assert stat.S_ISREG(s.st_mode) and s.st_nlink==1 and p.resolve()==p
    assert not any(q.is_symlink() for q in [p,*p.parents])
    assert (s.st_size,sha(p))==(r["bytes"],r["sha256"])
    meta=json.loads((P/f'two-evidence/id{r["id"]}-ffprobe.json').read_text())
    assert len(meta["streams"])==1 and meta["streams"][0]["codec_type"]=="video"
    assert meta["streams"][0]["nb_frames"]=="2160"
    checks.append({**r,"current_stat":{"dev":s.st_dev,"ino":s.st_ino,"size":s.st_size,"mtime":s.st_mtime_ns}})
save("two-predelete-identity.json",checks)
before=df("before");results=[]
for r in checks:
    p=Path(r["path"]);h=subprocess.run(["/usr/sbin/lsof","-nP","-Fpcfn","--",str(p)],capture_output=True,text=True)
    result={"path":str(p),"bytes":r["bytes"],"sha256":r["sha256"],"last_handle_check":{"at":now(),"code":h.returncode,"stdout":h.stdout,"stderr":h.stderr}}
    try:
        assert h.returncode==1 and not h.stdout and not h.stderr
        assert not any(q.is_symlink() for q in [p,*p.parents])
        s=p.lstat();old=r["current_stat"]
        assert stat.S_ISREG(s.st_mode) and s.st_nlink==1
        assert (s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns)==(old["dev"],old["ino"],old["size"],old["mtime"])
        assert sha(p)==r["sha256"]
        p.unlink();assert not p.exists()
        result["result"]="DELETED";result["at"]=now()
    except Exception as e:result.update(result="RETAINED",reason=repr(e))
    results.append(result);save("two-deletion-results.json",results)
after=df("after")
after_protected=[{**r,"exists":Path(r["path"]).exists(),"unchanged":Path(r["path"]).is_file() and sha(Path(r["path"]))==r["sha256"]} for r in before_protected]
save("two-protected-after.json",after_protected)
assert before["filesystem"]==after["filesystem"]
report={"at":now(),"scope":"Only former candidate IDs 2,3","deleted_count":sum(r["result"]=="DELETED" for r in results),"deleted_logical_bytes":sum(r["bytes"] for r in results if r["result"]=="DELETED"),"retained":[r for r in results if r["result"]!="DELETED"],"df_available_delta_bytes":(after["available_blocks"]-before["available_blocks"])*1024,"protected_count":len(protected),"protected_all_unchanged":all(r["unchanged"] for r in after_protected),"provenance":"Exact original Owner render/change/completion records, r2 historical SHA match, and sampled frames matching preserved 36s source; both obsolete generated silent previews","visual_coverage":"5/19/30 seconds per file, 6 frames; not continuous viewing","actual_model":"UNKNOWN","actual_effort":"UNKNOWN"}
save("余留两项核查报告.json",report);print(json.dumps(report,ensure_ascii=False,indent=2))
