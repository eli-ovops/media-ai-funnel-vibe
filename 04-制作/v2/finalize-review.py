from pathlib import Path
import json,hashlib,sys
P=Path(__file__).resolve().parent;Q=P/'qc/final-review';sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert '--actual-images-inspected' in sys.argv,'Only run after actual final export images have been inspected'
sys.path.insert(0,'/Users/USER/.codex/skills/fred-remotion-output/scripts');from library_gate import acceptance_signature
m=json.loads((P/'manifest.json').read_text());selected={'S1':3.150,'S2':36.650,'S3':57.650,'S4':106.650,'S5':135.650,'S6':148.250}
notes={'S1':'任务纸和聊天图形前置，问题置于图形下方；12秒只保留一个任务纸，进入独立观察位。','S2':'人数按原顺序出现，旧数字保留左侧导航；图形不表示人口面积或筛落。','S3':'同一任务纸下缘法线外移18px起线，三个功能载体分段展开；四组数字保留至75秒。','S4':'同一事项含复选框沿步骤传递；同一重开窗口转为条件预期槽，未声称保存测试成功。','S5':'三个文字对应短答、任务纸、分工图三个工作区观察窗；底部总线与窗口间隔180px。','S6':'同一纸张收拢为输入；内部内容按变化轮廓裁切，最后问题保留到8999帧。'}
for pg in m['pages']:
 sid=pg['stableId']
 for rc in pg['referenceChoices']:rc['callSite']['sha256']=sha(P/'src/World.ts')
 f=Q/f'frame-{selected[sid]:.3f}.jpg';record={'path':str(f),'sha256':sha(f),'atSeconds':selected[sid]}
 pg['keyframeReview']={'frames':[record],'sourceFiles':[{'path':str(P/'src/World.ts'),'sha256':sha(P/'src/World.ts')},{'path':str(P/'src/kit.ts'),'sha256':sha(P/'src/kit.ts')}],'scope':'Actual final MP4 extracted stills; not continuous viewing'}
 pg['componentAcceptance']={'status':'passed','reviewer':'assistant','stage':'keyframes','checks':{'semanticFit':notes[sid],'corePreserved':pg['referenceChoices'][0]['preserve']+'；实际适配/调用见source-map，非逐帧复刻。','visualQuality':'完整v2导出抽帧已实际查看，并另核高风险原尺寸图片；仅记录采样层观察，不替代05/连续看听。'},'evidence':[record]}
 pg['componentAcceptance']['contextSha256']=acceptance_signature(m,pg,'keyframes')
(P/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
e=json.loads((Q/'export-check.json').read_text());e['visual_review']='ACTUAL_SAMPLED_IMAGES_INSPECTED; normal-speed continuous and direct hearing NOT_PERFORMED';(Q/'export-check.json').write_text(json.dumps(e,ensure_ascii=False,indent=2))
r=json.loads((P/'qc/rework-review.json').read_text());r['prior_complete_candidate_frames_viewed']=75;r['latest_version_review_scope']='25 final frames, concentrating on changed transitions and six semantic representative frames; prior candidate75-frame review retained for unchanged ranges';r.update(status='FOUR_ITEMS_IMPLEMENTED_AND_SAMPLED; PMO_ACCEPTANCE_PENDING',video_sha256=e['sha256'],actual_final_mp4_frames_viewed=e['extracted_frames'],native_size_final_checks=[50.150,57.650,103.167,106.650,124.167,135.650,139.167,146.350],scene_observations=notes)
for issue in r['issues']:
 issue['evidence']=[{'second':t,'path':str(Q/f'frame-{t:.3f}.jpg'),'sha256':sha(Q/f'frame-{t:.3f}.jpg')} for t in issue['target_times'] if (Q/f'frame-{t:.3f}.jpg').exists()]
(P/'qc/rework-review.json').write_text(json.dumps(r,ensure_ascii=False,indent=2))
sm=json.loads((P/'source-map.json').read_text())
for row in sm['source_implementations']:row['world_sha256']=sha(P/'src/World.ts')
(P/'source-map.json').write_text(json.dumps(sm,ensure_ascii=False,indent=2))
print('Recorded actual final sampled inspection; not formal AV approval')
