import json,hashlib
from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parent.parent
results=json.loads((P/"deletion-results.json").read_text())
retained=[r for r in results if r["result"]=="RETAINED"]
for r in results:
    assert Path(r["path"]).exists()==(r["result"]=="RETAINED")
    if r["result"]=="RETAINED":assert hashlib.sha256(Path(r["path"]).read_bytes()).hexdigest()==r["sha256"]
receipts=R/"06-发布准备/07-五站发布回执.json"
data=json.loads(receipts.read_text())
urls=[]
def visit(v,key=""):
    if isinstance(v,dict):
        for k,w in v.items():visit(w,key+"/"+k)
    elif isinstance(v,list):
        for i,w in enumerate(v):visit(w,key+"/"+str(i))
    elif isinstance(v,str) and v.startswith(("https://","http://")):urls.append({"field":key,"url":v,"source":str(receipts),"status":"historical receipt URL; not reverified in cleanup"})
visit(data)
index={"content_id":"ai-funnel-vibe-20261020","lifecycle":"发布后已清理：最终静音及带音乐成片本地不存在；两份来源未充分证明的旧代表段保留","cleanup_report":str(P/"清理报告.json"),"per_path_results":str(P/"deletion-results.json"),"retained_videos":retained,"final_silent_sha256":"71c213a4b4d90fc3448a463f8d96e6994786ec32c56168acba2d1518d4dff7dc","final_music_sha256":"d6673fb12be23bc07bf18fb5c2fd6539cc95858ece200062e9c2354a25838746","reexport_guide":str(P/"重新导出入口.md"),"covers_manifest":str(R/"04-制作/covers-v4/manifest.json"),"publication_closure":str(R/"06-发布准备/07-本期发布收口索引.json"),"published_or_native_receipt_urls":urls,"old_delivery_indexes":"Historical frozen evidence preserved; old video paths no longer available","pmo_current_pointer_update":"PENDING_PMO"}
(P/"发布后当前交付索引.json").write_text(json.dumps(index,ensure_ascii=False,indent=2)+"\n")
inventory=[{"path":str(p),"bytes":p.stat().st_size,"purpose":"cleanup authorization, provenance, safety check, deletion receipt or recovery/handoff evidence"} for p in P.iterdir() if p.is_file() and p.name!="artifact-inventory.json"]
(P/"artifact-inventory.json").write_text(json.dumps(inventory,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"deleted_verified_absent":sum(r["result"]=="DELETED" for r in results),"retained_verified":len(retained),"protected_selected":len(json.loads((P/"protected-after.json").read_text())),"receipt_urls":len(urls),"current_index":str(P/"发布后当前交付索引.json")},ensure_ascii=False))
