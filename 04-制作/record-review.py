from pathlib import Path
import json,hashlib,sys
P=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();Q=P/'qc/final'
sys.path.insert(0,'/Users/USER/.codex/skills/fred-remotion-output/scripts')
from library_gate import acceptance_signature
m=json.loads((P/'manifest.json').read_text())
selected={'S1':3.150,'S2':36.650,'S3':57.650,'S4':106.650,'S5':135.650,'S6':148.250}
notes={'S1':'同一个端口连接短答与立体任务纸；首段纸张已收进画布，文字无裁切。','S2':'断开端口与接通后的聊天/纸张有区别；人数只有约数文字，没有数量对应的粒子。','S3':'三功能分工、下方负责端和交换路径可见；5000绑定内部访问说明，未写Agent总人数。','S4':'保存前事项与刷新后虚线预期槽对照；回查线路保持条件句，没有测试成功勾。','S5':'三访问窗口大小按构图处理，未表示性能倍数；文字和线条分区，完整可读。','S6':'三关系收回到单个任务输入；最后提问保留到8999帧。'}
for pg in m['pages']:
 sid=pg['stableId'];rid=pg['referenceChoices'][0]['id'];label='T04b' if rid.endswith('t04b') else 'T05h'
 preview=Path('/Volumes/EXTERNAL/自媒体/资产库/FredTalk/组件视频')/(label+'-1-preview.mp4')
 sheet=Path('/Volumes/EXTERNAL/自媒体/Fred付费资料全站学习-20261016/证据/333视频动态读取/时间序列图')/(label+'-1-preview-p01.jpg')
 pg['componentPlan']['inspectedReferences']=[{'id':rid,'path':str(preview),'sha256':sha(preview),'observations':f'通过准确派生联系图实际查看{label}核心时序帧；不是连续观看。{sheet}；联系图SHA={sha(sheet)}；'+pg['referenceChoices'][0]['preserve']}]
 f=Q/f'frame-{selected[sid]:.3f}.jpg';record={'path':str(f),'sha256':sha(f),'atSeconds':selected[sid]}
 pg['keyframeReview']={'frames':[record],'sourceFiles':[{'path':str(P/'src/World.ts'),'sha256':sha(P/'src/World.ts')},{'path':str(P/'src/kit.ts'),'sha256':sha(P/'src/kit.ts')}],'scope':'Exported MP4 stills only'}
 pg['componentAcceptance']={'status':'passed','reviewer':'assistant','stage':'keyframes','checks':{'semanticFit':notes[sid],'corePreserved':pg['referenceChoices'][0]['preserve']+'，本期源码/调用另核。','visualQuality':'最终MP4联系图及高风险原尺寸图已看；采样中未发现文字裁切或文字与图形重叠。静帧结论不替代正常速度/声音。'},'evidence':[record,{'path':str(sheet),'sha256':sha(sheet)}]}
 pg['componentAcceptance']['contextSha256']=acceptance_signature(m,pg,'keyframes')
(P/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
report={'artifact':str(P/'output/ai-funnel-v1-internal-150s.mp4'),'artifactSha256':sha(P/'output/ai-funnel-v1-internal-150s.mp4'),'status':'SAMPLED_IMAGE_REVIEW_COMPLETED; FULL_AV_REVIEW_NOT_CLAIMED','unique_final_mp4_frames_viewed':61,'coverage':'22 cue midpoints +39 transition/semantic event points; 8 contact sheets actually displayed','additional_native_size_checks':[50.150,106.650,135.650],'observations':notes,'transitions':'10 conceptual boundary cross-dissolves last 0.35s within orientation windows; observed intentional brief double exposure. In-scene split/pulse/camera/reopen/return stages sampled. No full-time smoothness claim.','copy':'All22 screen cues visible in sampled frames, with proper approximate counts and persistent attribution. Actual font geometry has46 lines within safe area.','covers':'Four full candidate images and four phone thumbnails viewed; corrected3:4 bottom margin before final inspection; all are candidates, not user approved.','unverified':['Normal-speed continuous visual perception','Direct hearing and subjective mix','Exact Nico BGM','05 independent review','User final approval'],'repair_batch':{'user_rework_rounds':0,'internal_layout_rounds':1,'fixed':['intro project object right margin','chapter boundary 0.35s transitions','3:4 cover bottom margin']},'technical_only_fixes':['source catalog local path binding by exact hash','local existing TypeScript parser resolution','one aborted cwd/hash refresh attempt; final source receipt and video SHA govern','PNG full-page capture replaced by native Canvas image export after two same-code short tests']}
(P/'qc/visual-review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
e=json.loads((Q/'export-check.json').read_text());e['visual_review']='61 actual extracted frames inspected; see ../visual-review.json';(Q/'export-check.json').write_text(json.dumps(e,ensure_ascii=False,indent=2))
