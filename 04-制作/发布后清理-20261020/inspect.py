import json, os, hashlib, stat
from pathlib import Path
ROOT=Path("/Volumes/EXTERNAL/自媒体/ai-funnel-vibe-20261020")
OUT=Path(__file__).resolve().parent
inv=json.loads((ROOT/"06-发布准备/PMO-发布完成清理前只读视频范围.json").read_text())
texts=[]
for base,dirs,files in os.walk(ROOT):
    dirs[:]=[d for d in dirs if d not in {"node_modules",".git","发布后清理-20261020"} and not (Path(base)/d).is_symlink()]
    for f in files:
        p=Path(base)/f
        if p.suffix in {".json",".log",".md",".py",".mjs",".js",".sh",".txt"} and p.stat().st_size<2000000 and p.name!="PMO-发布完成清理前只读视频范围.json":
            try: texts.append((p,p.read_text()))
            except UnicodeError: pass
results=[]
for n,item in enumerate(inv["paths"]):
    p=Path(item["path"])
    hits=[]
    for f,text in texts:
        if p.name not in text:continue
        if "/04-制作/" in str(p) and p.parent.parent not in f.parents:continue
        for line,s in enumerate(text.splitlines(),1):
            if p.name in s: hits.append({"file":str(f),"line":line,"text":s[:700]})
    st=p.lstat()
    record={**item,"id":n,"sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"dev":st.st_dev,"inode":st.st_ino,"mtime_ns":st.st_mtime_ns,"mode":st.st_mode,"nlink":st.st_nlink,"resolved":str(p.resolve()),"matches":hits}
    results.append(record)
    print(n,item["relative"],len(hits))
    for h in hits[:3]:print(" ",str(Path(h["file"]).relative_to(ROOT)),h["line"],h["text"][:180])
(OUT/"inspection.json").write_text(json.dumps(results,ensure_ascii=False,indent=2)+"\n")
