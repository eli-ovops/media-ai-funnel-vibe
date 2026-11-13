from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;B=P.parent/'v4-complete'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rec=lambda p:dict(path=str(p),sha256=sha(p))
mapping=[
 ('preserved',[0,84],[0,84],'从冻结r5继承，无场景改动'),
 ('small_task',[84,91],[84,91],'沿用问答窗，清除说明后接具体事项'),
 ('large_task',[91,98],[91,98],'同一01事项逐字新增和打勾'),
 ('scale_meaning',[98,105],[98,105],'保存01状态，关窗，再打开；StepChain只作导航'),
 ('verifiable_domains',[105,112],[105,111],'逐项检查同一事项文字和勾选状态'),
 ('training_feedback',[112,119],[111,125],'如果记录丢失，回保存逻辑，再核对同一事项；尾部退场'),
 ('uneven_capability',[119,126],[125,132],'数学/编程延后6秒，标题在旧窗退出时单独接入'),
 ('access_tiers',[126,133.5],[132,137.6],'三种条件按原组件cue建立'),
 ('access_meaning',[133.5,141],[137.6,141],'三分支阅读至140.1后退出；删除重复结论'),
 ('synthesis',[141,147],[141,147],'旧树退离后从新因素下缘连线；因素缩入唯一结论载体'),
 ('closing',[147,150],[147,150],'仅结论载体换成最终问题')]
mapping=[dict(id=i,old=o,new=n,note=note,oldFramesExclusive=[round(x*60) for x in o],newFramesExclusive=[round(x*60) for x in n]) for i,o,n,note in mapping]
(P/'time-map.json').write_text(json.dumps({'baseline':rec(B/'output/ai-funnel-v4-complete-150s-r5.mp4'),'fps':60,'mapping':mapping,'mappingType':'semantic ranges, not uniform timewarp'},ensure_ascii=False,indent=2))
d=json.loads((B/'screen-text-index.json').read_text());d['version']='v4-repair1-150s-r1'
texts={
 'large_task':['新增一条具体事项','01','整理客户需求','标记为完成','新增','完成'],
 'scale_meaning':['保存这条记录','关掉，再打开','保存的记录','保存','重开','核对'],
 'verifiable_domains':['核对内容和完成状态','重开后的记录','01','整理客户需求'],
 'training_feedback':['如果这条记录不在','如果记录丢失','回到保存逻辑','再次打开，核对同一条','01 · 整理客户需求','还在吗？完成状态保留了吗？'],
 'access_meaning':['访问条件','免费版 / 公开入口','付费版 / 订阅入口','内部系统 / 内部授权']}
for r in d['semantics']:
 hit=next((x for x in mapping if x['id']==r['id']),None)
 if hit:
  r['baseline_start_sec']=r['start_sec'];r['baseline_end_sec']=r['end_sec']
  r['start_sec'],r['end_sec']=hit['new'];r['start_frame'],r['end_frame_exclusive']=hit['newFramesExclusive'];r['adaptation']=hit['note']
 if r['id'] in texts:r['screen_lines']=texts[r['id']]
d['sources']=[rec(P/'src'/n) for n in ['FullEpisode.tsx','Magnified.tsx','RepairScenes.tsx']]
d['exact_line_timing']='Source cues; semantic windows not OCR timestamps. Access meaning is encoded in existing tree rather than repeated conclusion.'
(P/'screen-text-index.json').write_text(json.dumps(d,ensure_ascii=False,indent=2))
(P/'screen-script.txt').write_text('\n\n'.join(f"{r['start_sec']}–{r['end_sec']}s | {r['id']}\n"+'\n'.join(r['screen_lines']) for r in d['semantics']))
m=json.loads((B/'Manifest.json').read_text());m['version']='v4-repair1-150s-r1';m['status']='REPAIR_RENDERING_PENDING_SELF_REVIEW';m.pop('delivery',None)
m['designContract']['authority']=str(P.parent.parent/'04-v4整片五项集中返修.md')
m['designContract']['scope']='Q1-Q5 consolidated repair; 0-84s protected; candidate only';m['timeMap']=str(P/'time-map.json')
pg=m['pages'][0];pg['stableId']='full-v4-repair1';pg.pop('componentAcceptance',None)
pg['keyframeReview']={'status':'PRE_RENDER_SAMPLED_ONLY','frames':[],'sourceFiles':[rec(P/'src'/n) for n in ['FullEpisode.tsx','RepairScenes.tsx','Magnified.tsx']]}
for r in pg['referenceChoices']:
 old=Path(r['implementation']['path']);r['implementation']['path']=str(P/old.relative_to(B));r['implementation']['sha256']=sha(Path(r['implementation']['path']))
 name=r['callSite']['callee'];newfile='RepairScenes.tsx' if name in ['StepChain','DecisionTree'] else 'FullEpisode.tsx';r['callSite'].update(rec(P/'src'/newfile))
 if name=='StepChain':
  r['callSite']['symbol']='ConcreteTask';r['useScope']='91.1-124.9s'
  r['change']='Retained S-wrap link topology; navigation=true gives compact3/2 layout above concrete01 record; no primary full-screen verb diagram'
 if name=='DecisionTree':r['callSite']['symbol']='AccessRepair';r['useScope']='132-141s'
m['revision']={'baseline':str(B),'baselineVideoSha256':'6ac2862d8b34a813ff471ff13d14a572bb77f35e0c5df78e1267bcaab343cbd0','target':'Astra/high','actualModel':'UNKNOWN','actualEffort':'UNKNOWN','weeklyUsageAtDispatch':'17%','fiveHourUsage':'UNKNOWN','feedbackBatch':['V4-Q1','V4-Q2','V4-Q3','V4-Q4','V4-Q5']}
m['remainingReview']=['Actual repaired export self-review','05 changed-range independent review','Normal-speed continuous viewing NOT_PERFORMED','PMO acceptance','User final approval and inherited covers']
(P/'Manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2))
s=json.loads((B/'source-map.json').read_text());s['version']=m['version'];s['componentRefs']=pg['referenceChoices'];s['baselineHistoricalSourceMap']=str(B/'source-map.json')
for k in ['counterexampleRemap','finalOverlapFix','deliveryAssembly']:s.pop(k,None)
s['repairScenes']={'source':rec(P/'src/RepairScenes.tsx'),'basis':['T03e sequential S-wrap navigation','T05h same-source state transmission, single record not repeated two-way branch','T04g access branches','T20m single inherited capsule'],'notRealAppTest':True,'timing':str(P/'time-map.json')}
s['episodeExtension']={'entry':rec(P/'src/FullEpisode.tsx'),'repair':rec(P/'src/RepairScenes.tsx'),'historicalEntry':str(B/'src/FullEpisode.tsx')}
for r in s['exactAdditionalT20m']:
 r['implementation']=rec(P/'src/components/T20m-PillToWindow.tsx')
 r['changed']='Inherited approved source-card destination720x310; full-film title at59.73s, child sequence59.8s. Returns-to-pill unused.'
s['localExtensions']={'sources':[rec(P/'src/FullEpisode.tsx'),rec(P/'src/RepairScenes.tsx')],'description':'Episode-local scene adaptations, not claimed as complete original Fred components'}
s['kit']=[rec(P/'src/kit/theme.ts'),rec(P/'src/kit/ui.tsx')]
s['differences']=[x for x in s['differences'] if not x.startswith('T03e')]+['T03e compact navigation3/2 above same concrete record; full source topology retained; object state movement uses T05h transmission relation']
(P/'source-map.json').write_text(json.dumps(s,ensure_ascii=False,indent=2))
print('Mapped22 semantics and exact source references')
