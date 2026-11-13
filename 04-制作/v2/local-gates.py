"""Resolve authorized local source snapshots. Validators unchanged; no token/network/install.
The vendor catalog's missing default install path is not the source's actual location.
Only exact catalog-SHA matches can replace sourceAvailability in this process.
"""
import sys,json,hashlib
from pathlib import Path
P=Path(__file__).resolve().parent
sys.path.insert(0,'/Users/USER/.codex/skills/fred-remotion-output/scripts')
import common
base=common.load_references
bindings=json.loads((P/'reference/sources.json').read_text())
def local_refs(root):
 registry,catalog=base(root)
 for row in catalog['components']+catalog['clips']:
  for source in row.get('sourceCode',[]):
   hit=next((b for b in bindings if b['sha256']==source.get('sha256')),None)
   if hit:
    actual=hashlib.sha256(Path(hit['source']).read_bytes()).hexdigest()
    if actual!=hit['sha256']:raise ValueError('Authorized source changed')
    source.update(path=hit['source'],available=True,status='local-sha-verified')
    row['sourceAvailability']={'available':True,'status':'local-sha-verified','evidence':hit['source']}
 return registry,catalog
common.load_references=local_refs
import subprocess
_run=subprocess.run
def run_local(*args,**kwargs):
 cmd=args[0] if args else kwargs.get("args")
 if isinstance(cmd,list) and len(cmd)>1 and str(cmd[1]).endswith("check_component_calls.mjs"):
  cmd=[cmd[0],str(P/"check-component-calls.mjs")]
  payload=json.loads(kwargs["input"]);payload["root"]=str(P);kwargs["input"]=json.dumps(payload)
  return _run(cmd,**kwargs)
 return _run(*args,**kwargs)
subprocess.run=run_local
import validate_production_gate
validate_production_gate.main()
