"""150-second content revision only. No rendering, collection or shared-state writes."""
from pathlib import Path
import json, re, hashlib
R=Path(__file__).resolve().parent
OLD=R.parent
CID='ai-funnel-vibe-20261020'
base=json.loads((OLD/'content-package.json').read_text())

# Each tuple is a knowledge beat inside one continuous scene, not a new slide.
rows=[
('question',0,6,['同样谈AI','为何判断差这么远？'],'原帖结尾的同时存在的不同体验',
 '同一个观察框内，两条路径尚未命名；短路径已返回，长路径仍有节点接续。焦点在两者之间建立。','观察框、焦点环、两条路径','B:b-01'),
('contrast',6,12,['有人看到聊天框','有人看到复杂项目'],'原帖免费聊天产品与专业复杂项目的反差',
 '保持观察框，短路径变成一问一答的轮廓；长路径展出相互依赖的任务节点，提示二者承担的工作不同。不是同题模型效果实测。','两种任务跨度、同一焦点环','B:b-01'),
('attribution',12,20,['AI认知漏斗'],'原帖Napkin math及四组观察',
 '两条路径退到同一观察框的侧边；无箭头脊线展开四个等尺寸观察节点。焦点停在第一组，归因与示意标签先于人数出现并稳定。','四节点、观察框、焦点环','A:a-01'),
('barely_exposed',20,27,['约60亿人','几乎未接触','大语言模型'],'原帖第1组',
 '第一节点旁显示粗估与定义。模型接口和人的抽象交互端未接通，只说明未接触状态；无人口粒子或数量面积编码。','第一节点和未接通接口','A:a-01'),
('exposure_meaning',27,33,['听过AI','不等于亲手用过'],'对barely come in contact的编辑性解释，不增加统计结论',
 '节点位置不变：外部信息线到达接口外沿，实际交互线仍未建立。两种关系可见，不能把某个虚构人物当真实案例。','未接通的交互线端点，焦点移向第二组','A:a-01'),
('casual_free',33,40,['约10—20亿人','偶尔使用','免费聊天产品'],'原帖第2组：casual and infrequent free-tier users',
 '第二节点展开；交互线进入短问答路径并返回。第一组只留下原位静止数值；不演出免费产品答错。','第二节点、短问答路径','B:b-02'),
('casual_tasks',40,46,['查资料 · 改文字','更像一个问答工具'],'原帖better Google search / a writing aid的比喻',
 '同一短路径两次承担不同信息职责：查询符号回到结果端，文字片段到编辑端后返回。流程仅解释使用方式，无虚构产品界面、答案或测评。','同一输入片段与返回路径','B:b-01'),
('professional_frontier',46,54,['约2000万人','数学／编程中','专业使用前沿大模型'],'原帖第3组：professional frontier LLM use in math&code',
 '焦点定位第三组，刚才的输入片段接到长任务链。专业领域与前沿模型文字必须同时可见；不是全球所有Agent人口。','第三节点、输入片段、长任务链','B:supp-ref-46'),
('agent_projects',54,61,['作者关注的是','Agent接手复杂项目'],'原帖第3组描述agents完成large complex projects；只归因转述',
 '输入片段在长链上触发多个互有依赖的子任务节点，再汇聚到项目端点。强调一个项目包含多个环节，不给速度倍率、成功勾或收益。','长任务链、子任务依赖、项目端点','A:a-03'),
('internal_access',61,68,['约5000人','可访问','内部前沿系统'],'原帖第4组：access to frontier-grade systems internally',
 '焦点移到第四个固定节点；访问门的边界开启一个内部工作区。前一组人口不流入，不筛选，不以人数推优秀程度。','第四节点、访问边界、内部工作区','A:a-03'),
('internal_collaboration',68,75,['内部系统中','多Agent持续协作'],'原帖描述内部系统预览中的agent swarms；不新增持续时间或数量',
 '已有内部工作区中的任务依赖形成几个并行分支，分支交换任务状态后汇回同一项目端点。无服务器照片、额外Agent计数或完成率。','任务分支、共享项目端点、访问边界','B:supp-ref-60'),
('causes',75,82,['差距来自哪里？','任务 · 领域 · 权限'],'原帖三个因素的编辑性归纳',
 '数字固定在原位置退为背景；任务链、验证接口、访问边界在同一对象场中重新排列，三个关系焦点依次明确。不是新增三张信息卡。','原有任务载体、验证节点、访问边界','B:supp-grid-70-75'),
('small_task',82,89,['问一句话','得到一段回答'],'原帖A question with a paragraph answer barely stresses the system',
 '共用输入片段只走一段短路径，到一段文字形状的回答端点即止。留出“请求—处理—返回”的可见过程，不需要假聊天文案。','输入片段和已返回回答端点','B:b-01'),
('large_task',89,96,['做一个项目','牵动一串步骤'],'原帖problem size / horizon及复杂项目；过程是本期解释示意',
 '同一输入片段进入已有长路径；依赖节点逐个显露，前一节点的输出成为下一节点的输入，并出现一处需返回检查的关系。不是把短任务拉长播放。','同一输入片段、依赖链与检查回路','B:supp-grid-70-75'),
('scale_meaning',96,103,['问题的规模','改变你看到的能力'],'原帖影响随ambition, problem size and horizon变化的观点',
 '短回答端点和长项目端点在共用输入端两侧同时保留；焦点沿两条关系往返一次，读者能比较工作跨度，而非人群级别或性能测评。','两种跨度、检查回路和验证节点','B:supp-grid-70-75'),
('verifiable_domains',103,110,['数学、编程','结果更容易验证'],'原帖能力峰值与digital/verifiable领域的联系',
 '检查回路进入中心，输出端对齐一个独立的验证接口。代码/数学用抽象符号区分，关系说明能对照结果，不编造具体模型答题结果。','输出端、验证接口、两类任务标识','B:supp-ref-75'),
('training_feedback',110,117,['训练也偏向','可验证的任务'],'原帖reinforcement learning on verifiable rewards / curated environment mixture',
 '验证接口返回反馈箭头，组成明确的训练回路。训练对象与前面一次用户请求用边界区分，不能画成每聊一句产品就自动训练或立刻变强。','验证反馈回路与领域位置','B:supp-ref-75'),
('uneven_capability',117,124,['不同领域','能力并不均匀'],'原帖jaggedness以及能力领域差异',
 '同一个模型轮廓对不同任务接口显出不同匹配关系：有些可直接验证，有些需要额外判断；只做无刻度关系示意，不画虚构得分曲线。','模型轮廓、不同任务接口、访问边界','B:supp-ref-75'),
('access_tiers',124,132,['免费版 · 付费版','内部系统'],'原帖因素3：Free-tier, paid-tier, internal',
 '之前的访问边界回到同一工作区前方，三个访问位置依次被焦点触及，能看到的接口范围不同；不把开门动画等同付费必然更正确。','同一工作区、访问边界、三个访问位置','B:b-01'),
('access_meaning',132,139,['你试过的版本','不代表AI的全部'],'依据原帖recency/tier与access的编辑性总结，不保证其他版本表现',
 '保留观察框，当前访问窗口只是工作区中的一个窗口；窗口边界后还有不同接口。只表达接触范围，不显示未经核实的隐藏能力或评分。','观察框、任务链、领域接口与访问窗口','B:b-01'),
('synthesis',139,146,['判断AI之前','先看任务、领域和权限'],'三个原文因素的编辑性总结',
 '任务链、验证接口、访问边界围绕同一输入片段收拢为三个可辨关系，随后接回开头两条路径。前景只留这两行，不重播四组数字。','开头观察框与两个路径端点','B:supp-grid-70-75'),
('closing',146,150,['你交给AI什么任务？'],'面向观众的编辑性提问，非效果承诺',
 '输入片段回到观察框的入口，焦点环停在可进入的两条路径之间；在阅读结束前保持文字稳定，最后0.5秒自然收声。','同一入口、输入片段和焦点环；正常结束','B:b-01')
]

def units(t):return sum(1 if '\u4e00'<=c<='\u9fff' else .5 if c.isalnum() else .25 if not c.isspace() else 0 for c in t)
def dump(n,o):(R/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
def ts(t):
 ms=round(t*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000)
 return f'{h:02}:{m:02}:{s:02},{ms:03}'
scenes=[]
for idx,(sid,a,b,lines,basis,process,handoff,ref) in enumerate(rows):
 extra='Karpathy 粗估\n示意' if sid=='attribution' else '观点' if sid=='causes' else ''
 u=units('\n'.join(lines)+'\n'+extra);need=round(.5+u/3.5,3);ra=a+.5;rb=b-.2 if b<150 else 150
 scenes.append({'id':sid,'start_sec':a,'end_sec':b,'start_frame':a*60,'end_frame_exclusive':b*60,'screen_lines':lines,
  'reading_start_sec':ra,'reading_end_sec':rb,'reading_start_frame':round(ra*60),'reading_end_frame_exclusive':round(rb*60),
  'new_reading_units':u,'estimated_reading_seconds':need,'reading_window_seconds':round(rb-ra,3),'reading_margin_seconds':round(rb-ra-need,3),
  'source_basis':basis,'knowledge_change':process,'handoff_object':handoff,'reference_frame_ids':[ref],
  'motion_contract':'这是一段解释过程，不是新卡片。前0.5秒建立焦点；停稳后文字不移动，图形按过程产生可理解的新关系；末0.2秒只交接对象焦点。实际动作节奏由04选准确组件实现，不要求每段重复同一缓动。',
  'component_selection':'04_TO_SELECT_AND_VALIDATE','new_seven_reference_adaptation':'PENDING_01_EVIDENCE_NO_NEW_VIDEO_CLAIM'})
base.update(version='02-screen-v2-150s',status='DRAFT_PENDING_UPDATED_GATE_AND_REFERENCE_EVIDENCE',duration_seconds=150,total_frames=9000,scenes=scenes)
base['persistent_labels']=[{'id':'estimate','start_frame':720,'end_frame_exclusive':4500,'text':'Karpathy 粗估','first_counted_in_scene':'attribution'}, {'id':'schematic','start_frame':720,'end_frame_exclusive':4500,'text':'示意','first_counted_in_scene':'attribution'}, {'id':'commentary','start_frame':4500,'end_frame_exclusive':9000,'text':'Karpathy 观点','first_counted_in_scene':'causes'}]
base['diagram_contract']['group_to_causes_handoff']='At75s retain task-carrier, verification-node and access-boundary identity/last transforms. Reorganize their relations within the same field; do not convert counted people or replace with a slide.'
base['revision']={'supersedes':'02-screen-v1 60-second submission','authority':'PMO relayed direct user correction to about150s plus seven exact Vibe reference videos on2026-10-20','scope':'Continue prior content; add meaning and causal process, not stretched timing','new_statistics_added':False,'new_person_biography_added':False,'new_research_by02':False}
base['music_reference']={'user_statement':'用户说七条参考的背景音乐都是Nico《人生容错率》这条','status':'01核原片与音乐中；02未听核、未判同曲、未复制音轨','implementation':'全代码音乐/SFX要求保留，最终沿PMO更新总单；不自行把曲风参考当音乐复用许可'}
base['new_user_references']=[{'creator':a,'topic':b,'url':c,'read_by02':False} for a,b,c in [
('赵逍遥Xavier','AI龙场悟道','https://v.douyin.com/tN31HmEsasA/'),('肖三川川川','电势思想','https://v.douyin.com/JiCl2ziP1XY/'),('无足鸟','2026诺奖手性','https://v.douyin.com/wSduLACVfKQ/'),('骑老爷爷过马路被罚300','opus家族史','https://v.douyin.com/bikvGGssjy8/'),('黑洞科学馆','知识诅咒','https://v.douyin.com/BxotiBr-b_k/'),('Iwanau','运气的形状','https://v.douyin.com/709NLbpqDeE/'),('Nico','人生容错率','https://v.douyin.com/X2r7DkfK704/')]]
dump('content-package.json',base)
(R/'屏幕文案.md').write_text('# AI认知漏斗｜150秒完整屏幕文案 v2\n\n当前为已授权150秒修订稿，待更新门禁/新参考接回后正式提交。无人声，无口播或TTS。以下是全部新前景文字；既有静止数字只作导航，不重复生成新的阅读负担。\n\n'+ '\n\n'.join(f'## {s["start_sec"]}—{s["end_sec"]}秒\n\n'+'\n\n'.join(s['screen_lines']) for s in scenes)+'\n\n持续标签：12—75秒“Karpathy 粗估”“示意”；75—150秒“Karpathy 观点”。所有人数出现时必须有粗估归因。\n')
(R/'阅读时间轴.md').write_text('# 150秒阅读与过程时间轴\n\n22个信息拍，组织为一个连续解释空间；不是22张卡片。150秒／9000帧／60fps，左闭右开。新增时长用于使用方式、任务跨度、训练反馈与访问关系，正文不添加新调查数字或人物履历。\n\n'+ '\n\n'.join(f'## {s["id"]}｜{s["start_sec"]}—{s["end_sec"]}秒\n\n文字：'+'／'.join(s['screen_lines'])+f'\n\n过程：{s["knowledge_change"]}\n\n交接：{s["handoff_object"]}\n\n原文依据：{s["source_basis"]}\n\n稳定阅读：{s["reading_start_sec"]:.1f}—{s["reading_end_sec"]:.1f}秒（{s["reading_window_seconds"]:.1f}秒），估读{s["estimated_reading_seconds"]:.3f}秒，余量{s["reading_margin_seconds"]:.3f}秒。\n\n{ s["motion_contract"] }' for s in scenes))
(R/'screen-copy-review.srt').write_text('\n\n'.join(f'{i+1}\n{ts(s["reading_start_sec"])} --> {ts(s["reading_end_sec"])}\n'+'\n'.join(s['screen_lines']) for i,s in enumerate(scenes))+'\n')
assert scenes[0]['start_frame']==0 and scenes[-1]['end_frame_exclusive']==9000
assert all(a['end_frame_exclusive']==b['start_frame'] for a,b in zip(scenes,scenes[1:]))
assert all(s['reading_margin_seconds']>=0 for s in scenes),[(s['id'],s['reading_margin_seconds']) for s in scenes]
text=''.join(''.join(s['screen_lines']) for s in scenes)
stats={'foreground_non_whitespace_characters':len(re.sub(r'\s','',text)),'foreground_cjk_characters':len(re.findall(r'[\u4e00-\u9fff]',text)),'persistent_labels_non_whitespace_characters':22,'new_reading_units':sum(s['new_reading_units'] for s in scenes),'minimum_reading_margin_seconds':min(s['reading_margin_seconds'] for s in scenes),'densest_scene':max(scenes,key=lambda s:s['new_reading_units'])['id']}
dump('校核结果.json',{'content_id':CID,'version':base['version'],'status':'DRAFT_SELF_CHECK_NOT_PMO_APPROVAL','seconds':150,'frames':9000,'cues':len(scenes),'timeline_contiguous':True,'stats':stats,'reading_method':base['reading_method'],'reading_actual_phone':'NOT_DONE','new_seven_videos_read_by02':False,'music_identity_heard_by02':False,'new_gate':'PENDING_PMO_UPDATE','direct_audio_or_continuous_visual':'NOT_DONE','rendered_video':'NOT_DONE'})
print(json.dumps(stats,ensure_ascii=False))
