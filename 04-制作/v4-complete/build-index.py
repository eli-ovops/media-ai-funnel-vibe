from pathlib import Path
import json,hashlib,shutil
P=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
rec=lambda p:dict(path=str(p),sha256=sha(p))
j=json.loads((P/'content-package.json').read_text())
order=[
 ('question',0,6,['同样谈 AI','为何判断差这么远？','问答','输入问题','一段回答']),
 ('contrast',6,12,['有人看到聊天框','有人看到复杂项目','项目','拆任务','实际操作','检查结果']),
 ('attribution',12,16,['AI 认知漏斗']),
 ('barely_exposed',16,23,['几乎未接触大语言模型','约75%','约60亿人','其余人群','25%']),
 ('exposure_meaning',23,28,['听过 AI','≠ 亲手用过']),
 ('casual_free',28,35,['偶尔使用免费聊天产品','约20%','约10—20亿人','其余人群','80%']),
 ('casual_tasks',35,41,['查资料 · 改文字','更像一个问答工具']),
 ('professional_frontier',41,53.4,['数学／编程中专业使用前沿模型','约0.2%','约2000万人','同一总体','放大范围：总体的1%','0','1%']),
 ('internal_access',53.4,59,['可访问内部前沿系统','约0.00006%','约5000人','放大范围：总体的0.0001%','0.2% · 约2000万人','0','0.0001%']),
 ('agent_projects',59,70,['检查保存功能','新增 · 完成 · 待办清单','保存后，再打开','一条事项','已完成','未保存','已保存','再打开：记录丢失','再打开：检查结果','回到保存逻辑','事项仍在','空']),
 ('internal_collaboration',70,78,['做一份待办清单','多 Agent 协作','新增','完成','保存','01','02','03','Agent A','Agent B','Agent C','分工，再汇合','待办清单']),
 ('causes',78,84,['差距来自哪里？','任务','领域','权限','从一个具体任务看']),
 ('small_task',84,91,['只问：怎样做待办清单？','待办清单','怎样做待办清单？','得到一段说明']),
 ('large_task',91,98,['新增事项 → 标记完成','新增事项','标记完成','保存','再打开','保存后，再打开']),
 ('scale_meaning',98,105,['把目标拆成步骤','检查记录','才知道要检查什么']),
 ('verifiable_domains',105,112,['检查保存功能','刷新后，事项还在吗？','待办清单','一条事项 ？']),
 ('training_feedback',112,119,['如果不在','回到保存逻辑','再检查记录']),
 ('uneven_capability',119,126,['数学、编程','数学','编程','核算结果','检查运行','结果更容易验证']),
 ('access_tiers',126,133.5,['能接触哪些系统','访问条件','免费版','付费版','内部系统','公开入口','订阅入口','内部授权']),
 ('access_meaning',133.5,141,['取决于访问条件']),
 ('synthesis',141,147,['差距从这里产生','任务','领域','权限','共同影响 AI 体验']),
 ('closing',147,150,['你交给 AI 什么任务？']),
]
original={x['id']:x for x in j['scenes']}
assert set(original)=={x[0] for x in order} and len(order)==22
rows=[]
for id,a,b,lines in order:
 rows.append(dict(id=id,start_sec=a,end_sec=b,start_frame=round(a*60),end_frame_exclusive=round(b*60),screen_lines=lines,original_screen_lines=original[id]['screen_lines'],scope='Semantic beat window; individual lines appear at component cues. Retained text may overlap adjacent beat windows.'))
index=dict(version='v4-complete-150s-r5',fps=60,total_frames=9000,semantics=rows,count=22,caption_layer='One visual text layer; no extra burned SRT',sources=[rec(P/'src/FullEpisode.tsx'),rec(P/'src/Magnified.tsx')],exact_line_timing='See cues in FullEpisode.tsx and individual components; indices are beat windows, not OCR-derived word boundaries.')
(P/'screen-text-index.json').write_text(json.dumps(index,ensure_ascii=False,indent=2))
(P/'screen-script.txt').write_text('\n\n'.join(f"{x['start_sec']:07.2f}–{x['end_sec']:07.2f}  {x['id']}\n"+'\n'.join(x['screen_lines']) for x in rows))
j['currentTimeline']='screen-text-index.json';j['currentRender']='src/FullEpisode.tsx';j['currentProductionVersion']='v4-complete-150s-r5'
j['sfx']='NONE: intentionally silent current delivery; visual cues kept in source';j['semanticInputOwnerOnly']=j['owner_thread'];j['productionOwnerThread']='01a11a6f-49ef-7653-934a-4312979fd4e7'
(P/'content-package.json').write_text(json.dumps(j,ensure_ascii=False,indent=2))
src=P.parents[1]/'01-同题参考/Karpathy-原文.txt'
if src.exists():shutil.copy2(src,P/'inputs'/src.name)
covers=[]
for f in sorted((P.parent/'v2/output/covers').glob('*.png')):
 covers.append(dict(**rec(f),status='INHERITED_CANDIDATE_NOT_USER_APPROVED_NOT_REGENERATED'))
(P/'covers-index.json').write_text(json.dumps(covers,ensure_ascii=False,indent=2))
deps={}
for name in ['react','remotion','@remotion/renderer','@remotion/bundler','typescript']:
 f=P/'node_modules'/name/'package.json';d=json.loads(f.read_text());deps[name]=dict(version=d['version'],**rec(f.resolve()))
runtime=dict(node_modules=str((P/'node_modules').resolve()),public=str((P/'public').resolve()),browser='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',dependencies=deps,fonts=[rec(f.resolve()) for f in (P/'public/fonts').glob('*') if f.is_file()],portable=False,note='Complete episode source; dependencies and fonts reuse existing authorized local runtime via symlink. No install or external upload performed.')
(P/'runtime.json').write_text(json.dumps(runtime,ensure_ascii=False,indent=2))
s=json.loads((P/'source-map.json').read_text())
for item in s.get('exactAdditionalT20m') or []:
 f=P/'src/components'/Path(item['implementation']['path']).name;item['implementation']=rec(f);item['call']='Episode -> PillToWindow -> Sequence from48 -> Task -> SyncVsCopy';item['useScope']='59-59.8s carrier; children59.8-70s'
s['counterexampleRemap']=[dict(oldRepresentativeFrame=1170,fullFrame=3210,fullTime=53.5,reason='second true-scale window handoff'),dict(oldRepresentativeFrame=1520,fullFrame=3560,fullTime=3560/60,reason='carrier mid-state before content ready'),dict(oldRepresentativeFrame=1548,fullFrame=3588,fullTime=59.8,reason='task source card ready')]
(P/'source-map.json').write_text(json.dumps(s,ensure_ascii=False,indent=2))
print('22/22 beats, source input, covers and local runtime indexed')
