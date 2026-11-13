from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
src=json.loads((P/'reference/sources.json').read_text())
uses=[
 ('T04b-RoleSplit','roleSplit','branching','54-75s','Contiguous bar splits; gap and inner radius change together; assigned endpoint falls into the same column.'),
 ('T05h-SyncVsCopy','syncPoint','path / carrier','0-12,33-46,54-75,89-117,124-150s','Same-source cubic path and identity-preserving carrier. Git claims, version labels and success claims excluded.'),
 ('T20m-PillToWindow','pillWindow','taskSteps / saveCheck / access','93-94,103-104,124-127s','Same pill changes width/height/radius into a window.'),
 ('Fred wave3 kit','q / p / springAt','roleSplit / collaboration / pillWindow','throughout','Exact timing primitives, centralized episode palette adaptation.'),
 ('sy17-editorial','editorialCamera','taskWorld / figures / synthesis','12-20,46-82,139-150s','Logarithmic zoom and inOutCubic. New camera stops; screen copy stays outside moving camera.'),
 ('sy20-blueprint','camMat / project','solidPlane','0-20,46-82,117-124s','Camera basis and perspective projection. New solid task-sheet geometry; no original microphone, labels or shader.')]
for item,use in zip(src,uses):
 item.update(name=use[0],implementation_symbols=use[1],call_sites=use[2],use_scope=use[3],adaptation=use[4],implementation_path=str(P/'src/kit.ts'),implementation_sha256=sha(P/'src/kit.ts'),world_sha256=sha(P/'src/World.ts'))
refs=[]
for rel in ['Nico/transition-1.jpg','Nico/transition-2.jpg','Xiao/transition-1.jpg','Bird/transition-1.jpg','Luck/transition-1.jpg','Curse/transition-1.jpg','Zhao/transition-1.jpg','Opus/transition-1.jpg']:
 f=P.parent/'01-七条Vibe参考'/rel
 if f.exists():refs.append({'path':str(f),'sha256':sha(f),'viewed':'Actual image displayed to model; discrete frames only'})
report={'source_implementations':src,'viewed_vibe_evidence':refs,'reference_coverage':'43 displayed frame presentations across 8 contact sheets, 7 creators. Zhao/Opus were additionally inspected during rendering as a scope audit; no new mechanism or fact was added from them. No continuous video/audio viewing claim.',
 'opus_prompts':[{'id':'rossaxbt-707651','adopted':'Time-pure persistent carrier and closed-form spring','evidence':'Text prompt read; original media not watched'},{'id':'oxpsats-182908','adopted':'Code graphics and procedural synthesis; offline PCM in this implementation','evidence':'Text prompt read; original media not watched'},{'id':'rneayan-417829','adopted':False,'reason':'Population marbles would imply unsupported statistical nesting; not read/used in this task'}],
 'fonts':[{'path':str(f),'sha256':sha(f)} for f in (P/'public/fonts').glob('*.otf')],
 'original_elements':['solid task sheets','input port glyph','conditional expected item slot','access portals','episode composition/timing'],
 'boundary':'Accurate component mechanisms adapted, not a pixel-identical Fred/sy recreation. No source videos incorporated.'}
(P/'source-map.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
