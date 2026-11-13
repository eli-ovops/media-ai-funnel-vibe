"""Build only screen copy, deterministic timing and the 02 handoff; no video/audio rendering."""
from pathlib import Path
import json, hashlib, re, subprocess

R = Path(__file__).resolve().parent
ROOT = R.parent.parent
CID = 'ai-funnel-vibe-20261020'
FPS = 60
SOURCE = 'https://x.com/karpathy/status/2109361546505966046'

# screen_lines are the entire NEW foreground copy. Persisted attribution is separate.
rows = [
 ('question',0,5,['同样谈AI','为何判断差这么远？'],
  '建立体验反差，不声称同一版本对同一问题得到两种已测试结果。',
  '共用观察框内，一条短对话路径与多步任务路径同时可见；一个焦点环从二者之间移到观察框边缘。',
  '观察框、焦点环、未命名任务点', '原帖结尾：不同群体同时有不同体验', ['B:b-01','B:b-02']),
 ('attribution',5,11,['AI认知漏斗'],
  '明确是作者粗估的观点解读，建立四个观察位置。',
  '原观察框展开四个等尺寸观察节点，共用一根无箭头定位脊线。节点只代表四类体验，不代表人数、面积或个人升级。焦点环定位第一组。',
  '同一观察框、四个固定节点、焦点环', '原帖Napkin math及四组描述', ['A:a-01','B:b-02']),
 ('barely_exposed',11,17,['约60亿人','几乎未接触','大语言模型'],
  '没有使用经历，也构成公众对AI认知差异的背景。',
  '第一观察节点旁出现数字与组名。焦点环圈住尚未接通的模型接口符号；不出现60亿个粒子，也不把节点大小映射人数。',
  '四节点及第一节点状态；焦点环沿脊线移向第二节点', '原帖第1组：barely come in contact with LLMs', ['A:a-01']),
 ('casual_free',17,23,['约10—20亿人','偶尔使用','免费聊天产品'],
  '保留范围，说明使用频率与产品层级。',
  '第一组信息收为原节点上的静止数值；第二节点在同一框内接出单次问答线，返回一条短回答，再停稳阅读。不是免费版答错演示。',
  '第二节点的问答线与焦点环；其余节点保持位置', '原帖第2组：casual and infrequent users of free-tier ChatGPT-like products', ['B:b-01','B:b-02']),
 ('professional_frontier',23,30,['约2000万人','数学／编程中','专业使用前沿大模型'],
  '准确限定专业用途、领域及模型层级，不改成所有Agent用户。',
  '焦点环移到第三节点。原问答线的任务载体保留，由单端点展开为相连的任务、验证、结果三个无文字节点，表达工作跨度；不画速度倍数、完成率或必然成功打勾。',
  '第三节点及已展开的任务链；焦点环', '原帖第3组：professional use of frontier-grade LLMs in math&code', ['A:a-03','B:b-01','B:supp-ref-46']),
 ('internal_access',30,36,['约5000人','可访问','内部前沿系统'],
  '人数对应内部系统访问权限，不对应智力或Agent技能排名。',
  '焦点环定位第四节点，明确的访问门边界露出门内关联节点。不是第三组人口流入或筛选成5000人；只比较另一种访问环境。',
  '访问门、任务链和焦点环，四组位置保留', '原帖第4组：with access to frontier-grade systems internally', ['A:a-03','B:supp-ref-60']),
 ('task_scale',36,42,['任务规模','问一句话 → 做一个项目'],
  '从人数转到原因一：交给系统的问题规模。',
  '四组数字退到背景且不再承担阅读。第三节点已有任务链进入中心：单个问题端点延展为多个相连任务节点。该图解释跨度，没有时间倍率。',
  '同一任务链、验证节点、焦点环', '原帖因素1：ambition, problem size, horizon', ['B:b-01','B:supp-grid-70-75']),
 ('domain',42,48,['领域','数学、编程','结果更易验证'],
  '原因二：不同领域的可验证性不同，避免人人都能获得同等收益。',
  '不新开壳：焦点环沿任务链移动到已有验证节点；两条输入路径通过验证接口汇合为一个结果端点。几何动作说明可核对，不演出具体正确答案。',
  '任务链、验证接口、结果端点', '原帖因素2：digital, verifiable and economically valuable domains', ['B:b-01','B:supp-ref-75']),
 ('access',48,54,['访问权限','免费版 · 付费版','内部系统'],
  '原因三：访问层级影响所能接触的系统，不许诺付费必然答对。',
  '已有访问门回到任务链侧边，同一观察框内标出三个访问位置；焦点环依次触及位置，门后可见范围变化。没有购买按钮、价格、效果评分或等级奖章。',
  '同一任务端点与焦点环；访问门边界', '原帖因素3：Free-tier, paid-tier, internal', ['B:b-01','A:a-03']),
 ('closing',54,60,['你用AI问过什么？','又让它完成过什么？'],
  '回到观众自己的使用经历，结束一个核心反差。',
  '任务链收回开头的观察框；短问答端点和项目端点再次并置，焦点环在二者之间停稳。保留原始身份，不突然换成结尾大字卡。最后0.5秒保持完整可读。',
  '开头同一观察框及两个路径端点；不自动循环重放', '依据原帖任务规模因素作编辑性提问，不是效果承诺', ['B:b-01'])
]

def dump(name,obj):
    (R/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')

def units(text):
    # Planning assumption, not a population reading-speed claim or actual phone test.
    return sum(1 if '\u4e00'<=c<='\u9fff' else .5 if c.isalnum() else .25 if not c.isspace() else 0 for c in text)

def srt_ts(sec):
    ms=round(sec*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000)
    return f'{h:02}:{m:02}:{s:02},{ms:03}'

scenes=[]
for i,(sid,a,b,lines,purpose,change,handoff,basis,refs) in enumerate(rows):
    stable_a=a+.4
    stable_b=b-.1 if i<9 else b
    extra='Karpathy 粗估\n示意' if sid=='attribution' else '观点' if sid=='task_scale' else ''
    new='\n'.join(lines)+ ('\n'+extra if extra else '')
    u=units(new);need=round(.5+u/3.5,3)
    scenes.append(dict(id=sid,start_frame=round(a*FPS),end_frame_exclusive=round(b*FPS),start_sec=a,end_sec=b,
      screen_lines=lines,reading_start_frame=round(stable_a*FPS),reading_end_frame_exclusive=round(stable_b*FPS),
      reading_window_seconds=round(stable_b-stable_a,3),new_reading_units=u,estimated_reading_seconds=need,
      reading_margin_seconds=round(stable_b-stable_a-need,3),purpose=purpose,knowledge_change=change,
      handoff_object=handoff,source_basis=basis,reference_frame_ids=refs,
      component_selection='04_TO_SELECT_ACCURATE_SOURCE_AND_VERIFY; content mechanism only, no selected or validated component',
      movement_rule='前0.4秒建立焦点；阅读窗口内文字位置/尺寸固定，关系节点可做低幅动作，不穿过文字；末0.1秒只交接焦点，不移走未读完文字。'))

package={
 'content_id':CID,'version':'02-screen-v1','owner_thread':'01a11a70-35e6-7db1-86ac-80a7ce40a9cb',
 'status':'SUBMITTED_TO_PMO_NOT_STAGE_PASSED','duration_seconds':60,'fps':60,'total_frames':3600,'width':1080,'height':1920,
 'voiceover':False,'tts':False,'human_filming_required':False,'music':'04 deterministic local code synthesis','sfx':'04 deterministic local code synthesis',
 'text_role':'All spoken narration is absent. screen_lines and persistent_labels are the authoritative visible copy; SRT is review/accessibility export, not an extra duplicated subtitle layer.',
 'source_url':SOURCE,'source_status':'Attribution to author napkin estimates; counts not independently validated',
 'persistent_labels':[
   {'id':'attribution','start_frame':300,'end_frame_exclusive':2160,'text':'Karpathy 粗估','first_counted_in_scene':'attribution'},
   {'id':'diagram_label','start_frame':300,'end_frame_exclusive':2160,'text':'示意','first_counted_in_scene':'attribution'},
   {'id':'commentary_attribution','start_frame':2160,'end_frame_exclusive':3600,'text':'Karpathy 观点','first_counted_in_scene':'task_scale'}],
 'diagram_contract':{
   'four_group_nodes':'Equal-size semantic nodes with an unarrowed observation spine; no proportional area/width/count encoding.',
   'focus_ring':'Represents attention, not one person moving between groups.',
   'task_carrier':'A task symbol carried between explanations; never represents a counted individual.',
   'group_to_causes_handoff':'At36s retain the existing task-carrier/verification-node/access-boundary IDs and transforms. Move the task chain into focus while preserving frame edges as the working bounds. Reorganize relations within that same field; no replacement slide, fake population filtering or copied particle scale. Supplement B70-75 provides sampled evidence of field reorganization, not verified individual trajectories.',
   'retained_group_numbers':'After each group, retain its number only at its original node; no new copy. Maximum four numbers; never animate one number into another.',
   'prohibited':['100% normalization','exact pie chart','people filtering or falling between groups','population-count particles','5000=all Agent experts','20M=all Agent users','individual nested cohorts','value/intelligence ranking','paid always correct','copied wash-car test','unsupported speed or income claims'],
   'counts':[
     {'label':'约60亿人','value':6000000000,'scope':'几乎未接触LLM','scene':'barely_exposed'},
     {'label':'约10—20亿人','value_range':[1000000000,2000000000],'scope':'偶尔使用免费聊天产品','scene':'casual_free'},
     {'label':'约2000万人','value':20000000,'scope':'在数学/编程工作中专业使用前沿LLM','scene':'professional_frontier'},
     {'label':'约5000人','value':5000,'scope':'有内部前沿系统访问权限','scene':'internal_access'}]},
 'reading_method':{'units':'CJK=1; Latin letters/digits=.5; punctuation=.25; spaces=0','assumed_rate_units_per_second':3.5,'orientation_allowance_seconds':.5,'counting':'New foreground and newly introduced attribution; already-read static node numbers are retained navigation, not new reading.','claim_limit':'Planning estimate only; not an actual timed phone-reading, final font, motion or export acceptance.'},
 'scenes':scenes
}
dump('content-package.json',package)
(R/'屏幕文案.md').write_text('# AI认知漏斗｜完整屏幕文字 v1\n\n无旁白；以下是画内文字，不是口播稿。中文简体。结构化唯一文本见 content-package.json；无需另叠一层重复底部字幕。\n\n'+
 '\n\n'.join(f'## {s["start_sec"]:02}—{s["end_sec"]:02}秒\n\n'+ '\n\n'.join(s['screen_lines']) for s in scenes)+
 '\n\n## 持续短标签\n\n5—36秒：Karpathy 粗估；示意。\n\n36—60秒：Karpathy 观点。\n\n原文链接只入交付来源表，不把长URL塞入视频；四组数字出现时归因必须同时清晰可读。\n')
(R/'阅读时间轴.md').write_text('# 无旁白阅读与对象交接｜60秒／3600帧\n\n帧区间左闭右开。全局时钟 n/60；以下是内容机制需求，尚非组件选型或渲染通过。\n\n'+
 '\n\n'.join(f'## {s["id"]}｜{s["start_sec"]}—{s["end_sec"]}秒｜帧{s["start_frame"]}—{s["end_frame_exclusive"]-1}\n\n文字：'+ '／'.join(s['screen_lines'])+
 f'\n\n职责：{s["purpose"]}\n\n过程：{s["knowledge_change"]}\n\n交接：{s["handoff_object"]}\n\n停稳阅读：{s["reading_start_frame"]/60:.2f}—{s["reading_end_frame_exclusive"]/60:.2f}秒，共{s["reading_window_seconds"]:.2f}秒；估读{s["estimated_reading_seconds"]:.2f}秒，余量{s["reading_margin_seconds"]:.2f}秒。{s["movement_rule"]}\n\n原文依据：{s["source_basis"]}；实际源图：'+ ', '.join(s['reference_frame_ids']) for s in scenes))
(R/'screen-copy-review.srt').write_text('\n\n'.join(f'{i+1}\n{srt_ts(s["start_sec"]+.4)} --> {srt_ts(s["end_sec"]-.1 if i<9 else s["end_sec"])}\n'+ '\n'.join(s['screen_lines']) for i,s in enumerate(scenes))+'\n')

state=json.loads((ROOT/'流程协作/流程状态.json').read_text())
inputs=state['runs'][CID]['stages']['02']['inputs'];checks=[]
for item in inputs:
    actual=hashlib.sha256(Path(item['path']).read_bytes()).hexdigest()
    checks.append({**item,'actual_sha256':actual,'matches':actual==item['sha256']})
assert all(x['matches'] for x in checks)
assert scenes[0]['start_frame']==0 and scenes[-1]['end_frame_exclusive']==3600
assert all(a['end_frame_exclusive']==b['start_frame'] for a,b in zip(scenes,scenes[1:]))
assert all(s['reading_margin_seconds']>=0 for s in scenes), [(s['id'],s['reading_margin_seconds']) for s in scenes]
visible=''.join('\n'.join(s['screen_lines']) for s in scenes)
stats={'main_text_non_whitespace_characters':len(re.sub(r'\s','',visible)),
 'main_text_cjk_characters':len(re.findall(r'[\u4e00-\u9fff]',visible)),
 'persistent_label_unique_non_whitespace_characters':sum(len(re.sub(r'\s','',x)) for x in ['Karpathy 粗估','示意','Karpathy 观点']),
 'reading_units_total_including_first_introduction':sum(s['new_reading_units'] for s in scenes),
 'minimum_reading_margin_seconds':min(s['reading_margin_seconds'] for s in scenes),
 'densest_scene_by_new_reading_units':max(scenes,key=lambda s:s['new_reading_units'])['id']}
dump('校核结果.json',{'content_id':CID,'status':'CONTENT_AND_TIMING_SELF_CHECK_ONLY','gate':{'allowed':True,'content':CID,'stage':'02','thread':package['owner_thread']},'input_sha_checks':checks,'timing_contiguous':True,'duration_seconds':60,'total_frames':3600,'scenes':len(scenes),'statistics':stats,'reading_windows':[{'id':s['id'],'units':s['new_reading_units'],'stable_seconds':s['reading_window_seconds'],'estimated_seconds':s['estimated_reading_seconds'],'margin_seconds':s['reading_margin_seconds']} for s in scenes],'actual_phone_reading':'NOT_DONE','continuous_reference_video':'NOT_DONE','reference_direct_audio':'NOT_DONE','component_gate':'04 responsibility; no component selected or implementation produced by02','rendered_video':'NOT_DONE','pmo_approval':'PENDING','model_actual':'UNKNOWN','effort_actual':'UNKNOWN','speed_actual':'UNKNOWN'})
print(json.dumps(stats,ensure_ascii=False))
