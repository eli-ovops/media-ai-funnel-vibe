"""Keyframe gate with exact local source bindings; does not grant normal-speed AV acceptance."""
from pathlib import Path
import json,hashlib,sys,subprocess
P=Path(__file__).resolve().parent
sys.path.insert(0,'/Users/USER/.codex/skills/fred-remotion-output/scripts')
import library_gate,common
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
cat=library_gate.load_catalog();_,normalized=common.load_references(Path('/Users/USER/.codex/skill-repos/FredTalk'))
bindings=json.loads((P/'reference/sources.json').read_text())
for row in normalized['components']+normalized['clips']:
 for s in row.get('sourceCode',[]):
  hit=next((b for b in bindings if b['sha256']==s.get('sha256')),None)
  if hit:
   assert sha(hit['source'])==s['sha256'];s.update(path=hit['source'],available=True,status='local-sha-verified');row['sourceAvailability']={'available':True,'status':'local-sha-verified'}
   cat['items'][row['id']]['sourceHashes'].append(s['sha256'])
cat['portableNormalized']=normalized
run=subprocess.run
def adapted_run(*args,**kw):
 cmd=args[0] if args else kw.get('args')
 if isinstance(cmd,list) and len(cmd)>1 and str(cmd[1]).endswith('check_component_calls.mjs'):
  data=json.loads(kw['input']);data['root']=str(P);kw['input']=json.dumps(data);return run([cmd[0],str(P/'check-component-calls.mjs')],**kw)
 return run(*args,**kw)
library_gate.subprocess.run=adapted_run
stage=sys.argv[1] if len(sys.argv)>1 else 'keyframes'
m=json.loads((P/'manifest.json').read_text());errors=library_gate.validate_library_gate(m,stage,P,catalog=cat,root=Path('/Users/USER/.codex/skill-repos/FredTalk'))
r={'status':'FAIL' if errors else 'PASS','stage':stage,'scope':('Source-preview observations and current candidate/plan evidence only' if stage=='suggestion' else 'Sampled output images, source SHA and AST calls; not continuous visual/direct-hearing acceptance'),'errors':errors,'manifestSha256':sha(P/'manifest.json'),'local_binding_adapter':'Exact catalog SHA + already-authorized source files; no catalog mutation, network, token download or shared install.'}
(P/f'qc/library-{stage}-localpaths.json').write_text(json.dumps(r,ensure_ascii=False,indent=2));print(json.dumps(r,ensure_ascii=False,indent=2));sys.exit(bool(errors))
