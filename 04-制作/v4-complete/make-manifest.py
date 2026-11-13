from pathlib import Path
import json,hashlib,sys,shutil
P=Path(__file__).resolve().parent;A=P.with_name('v4-fix1');R=P.parents[2]/'Fred付费资料全站学习-20261016/解包只读副本'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
rec=lambda p:dict(path=str(p),sha256=sha(p))
sys.path.insert(0,'/Users/USER/.codex/skills/fred-remotion-output/scripts');import library_gate
m=json.loads((A/'Manifest.json').read_text());page=m['pages'][0]
m.update(version='v4-complete-150s-r5',status='PRODUCTION_CANDIDATE_PENDING_PMO_AND_05',durationInFrames=9000,outputSpec=dict(width=1080,height=1920,fps=60,durationSeconds=150))
m['designContract'].update(authority=str(P.parents[1]/'04-v4完整150秒续接.md'),scope='Full 22 semantic beats after PMO release of representative; no final approval implied',existing22BeatSemantics='All 22 mapped to screen-text-index.json',audio='Intentionally silent: no audio stream, voice, TTS, music or SFX; user adds platform music')
m['revision']=dict(baseline=str(A),fullFilmReleased=True,actualModel='UNKNOWN',target='Astra/high',weeklyUsageAtDispatch='10%',fiveHourUsage='UNKNOWN',noUserApprovalAdded=True)
page.update(stableId='full-v4-complete',durationInFrames=9000,oneQuestion='Why do AI experiences differ across exposure, task, domain and access?')
for r in page['referenceChoices']:
 for k in ['implementation','callSite']:
  file=P/('src/FullEpisode.tsx' if k=='callSite' else 'src/components/'+Path(r[k]['path']).name);r[k].update(rec(file))
 r['useScope']='16-46s' if r['id'].endswith('t15f') else '59.8-70s'
new=[('fred-wave3-40','T02g-RoleRoadmap','RoleRoadmap','Intro','0-12s','Two experiences build separate lanes from role to steps; no completion checks'),('fred-wave2-42','T04b-RoleSplit','RoleSplit','Roles','70-77.2s','One task bar splits into assigned responsibilities; tool cards enter underneath'),('fred-wave2-42','T03e-StepChain','StepChain','TaskSequence','90.4-105s','Sequential arrows and wrap topology show what to do and inspect'),('fred-wave3-40','T04g-DecisionTree','DecisionTree','Access','126-141s','Access conditions branch to entry types; recommend=-1, no winner')]
for pkg,name,sym,caller,scope,reason in new:
 source=R/(pkg+'-20261012')/'src/components'/(name+'.tsx');impl=P/'src/components'/(name+'.tsx');id=pkg+'-'+name.split('-')[0].lower()
 r=dict(id=id,reason=reason,preserve=reason,change='Complete source module adapted to portrait geometry and local props/cues; exact source archived; original kit retained except documented portrait/fonts/silent adapters',useScope=scope,source={**rec(source),'symbol':sym},implementation={**rec(impl),'symbol':sym},callSite={**rec(P/'src/FullEpisode.tsx'),'symbol':caller,'callee':sym})
 page['referenceChoices'].append(r)
 key=name.split('-')[0];preview=P.parents[2]/'资产库/FredTalk/组件视频'/f'{key}-1-preview.mp4'
 page['componentPlan']['candidates'].append(dict(id=id,decision='selected',reason=reason))
 page['componentPlan']['inspectedReferences'].append(dict(id=id,**rec(preview),observations='Read exact full source and card; viewed all contact sheets of sampled preview. '+reason+'. Not continuous watching/hearing.'))
page['componentPlan']['query']='Population proportion, role lanes, task assignment, sequential inspection, access conditions'
page['componentPlan']['rejectedCandidates']=[dict(id='T14a2',reason='Race implies measured speed; no measurements'),dict(id='T05d',reason='Winner comparison does not describe access'),dict(id='T09d2',reason='Automatic completion can imply an actual test'),dict(id='T08i',reason='Glass surface not allowed')]
frames=[]
for folder,nums in [('stills-r1',[430,1260,2040,3210,3585,3910,4500,6800,7370,7950]),('stills-r3',[30,945,4200,4650,5520,6050,6210,8470,8830])]:
 frames.extend([rec(P/'qc'/folder/f'F{n}.png') for n in nums])
page['keyframeReview']=dict(frames=frames,sourceFiles=[rec(f) for f in (P/'src').rglob('*.tsx')])
page['componentAcceptance']=dict(status='passed',stage='keyframes',reviewer='assistant',checks=dict(semanticFit='22 meanings mapped; approximate source counts preserved; no normalized partition, real-app pass or ranking claims',corePreserved='Full TSX modules retain role extraction, continuous task split, sequential S-wrap, conditions-to-leaves; exact original snapshots and kit SHA retained',visualQuality='Viewed 82 initial and 24 revision keyframes/contact sheets. Fixed missing title, white task-window reset, overlap at joins and title-ring remnant. This is sampled keyframe acceptance only; final render and continuous viewing remain separate.'),evidence=frames)
page['componentAcceptance']['contextSha256']=library_gate.acceptance_signature(m,page,'keyframes')
m['inspectionLimits']=['No normal-speed continuous visual review','No phone timed-reading test','No audio stream; no direct hearing acceptance','Full final film pending PMO and independent 05 review']
(P/'Manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2))
source_map=dict(version=m['version'],componentRefs=page['referenceChoices'],exactAdditionalT20m=json.loads((A/'source-map.json').read_text()).get('additionalExactSources'),episodeExtension={**rec(P/'src/Magnified.tsx'),'description':'Approved annular interval to explicit linear window, fixed fractions; full-film offset +34s vs representative'},localExtensions={**rec(P/'src/FullEpisode.tsx'),'description':'Intro/title-ring handoff, task/feedback conceptual window, factor synthesis. Not claimed as complete original Fred components.'},kit=[rec(P/'src/kit/theme.ts'),rec(P/'src/kit/ui.tsx')],differences=['Portrait 1080x1920 geometry','Local fonts and zero-audio adapter','T15f enter fixed at1 to retain faint overall ring; data geometry unchanged','T04b enter fixed at1 to receive prior task pill; neutral numbered Agent labels replace product logos','T03e task window kept at90,600,900,810; no window reentry; original sequential arrows preserved','T04g recommend=-1: equal access branches, no recommended winner'],syUsed=False)
(P/'source-map.json').write_text(json.dumps(source_map,ensure_ascii=False,indent=2))
shutil.copy2(A/'qc/check-calls-local.mjs',P/'qc/check-calls-local.mjs')
print('Manifest and source map created')
