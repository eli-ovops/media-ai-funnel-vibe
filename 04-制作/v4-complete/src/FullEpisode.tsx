import React from 'react';
import {AbsoluteFill,Sequence} from 'remotion';
import {Magnified} from './Magnified';
import {DonutShare} from './components/T15f-DonutShare';
import {PillToWindow} from './components/T20m-PillToWindow';
import {SyncVsCopy} from './components/T05h-SyncVsCopy';
import {RoleRoadmap} from './components/T02g-RoleRoadmap';
import {RoleSplit} from './components/T04b-RoleSplit';
import {StepChain} from './components/T03e-StepChain';
import {DecisionTree} from './components/T04g-DecisionTree';
import {Frame,Surface,Pill,MacWindow,Cursor,ClickRing,textBase,useT} from './kit/ui';
import {S,p,q,mix} from './kit/theme';
const Text=({children,y,size=68,color=S.ink,opacity=1}:{children:React.ReactNode,y:number,size?:number,color?:string,opacity?:number})=><div style={{position:'absolute',left:90,top:y,width:900,textAlign:'center',...textBase(size,900),whiteSpace:'normal',color,opacity}}>{children}</div>;
const Capsule=({text,x=90,y=850,w=900,h=200,size=78,opacity=1}:{text:string,x?:number,y?:number,w?:number,h?:number,size?:number,opacity?:number})=><Pill box={{x,y,w,h}} style={{opacity}}><span style={{...textBase(size,400,S.display),color:'#fff'}}>{text}</span></Pill>;
function Intro(){
 const t=useT(),g=q(t,11.3,12.1),title=q(t,14.8,15.6);
 return <Frame>
  {t<12.1&&<div style={{position:'absolute',inset:0,transform:`translateY(${-900*g}px) scale(${1-.15*g})`,transformOrigin:'540px 1000px'}}>
   <RoleRoadmap lanes={[{role:'问答',steps:['输入问题','一段回答']},{role:'项目',steps:['拆任务','实际操作','检查结果']}]} mode="overview" current={null} cues={[.15,6.3]}/>
   <Text y={180} size={78}>{t<6?'同样谈 AI':'有人看到聊天框'}</Text>
   <Text y={285} size={64} color={S.accent}>{t<6?'为何判断差这么远？':'有人看到复杂项目'}</Text>
  </div>}
  {t>=11.3&&t<14.8&&<Capsule text="AI 认知漏斗" y={mix(1500,850,g)} w={mix(600,900,g)} x={mix(240,90,g)} opacity={p(t,11.3,11.5)}/>}
  {t>=14.8&&<svg width={1080} height={1920} style={{position:'absolute',inset:0}}><rect x={mix(90,154,title)} y={mix(850,404,title)} width={mix(900,772,title)} height={mix(200,772,title)} rx={mix(100,386,title)} fill={`rgb(${mix(24,242,title)},${mix(24,242,title)},${mix(27,242,title)})`}/><ellipse cx={540} cy={mix(950,790,title)} rx={254*q(t,15,15.6)} ry={254*q(t,15,15.6)} fill="white"/></svg>}
 </Frame>;
}
function Population({share,count,meaning,kind}:{share:number,count:string,meaning:string,kind:'large'|'casual'|'pro'}){
 const t=useT(),detail=kind==='pro'?q(t,3.5,5):0;
 const aux=kind==='large'?q(t,7,7.7):kind==='casual'?Math.max(1-q(t,0,.65),q(t,7,7.7)):0;
 return <Frame><div style={{position:'absolute',inset:0,transform:kind==='pro'?`translate(${235*detail}px,${mix(-150*(1-q(t,0,.65)),-340,detail)}px) scale(${mix(mix(.88,1,q(t,0,.65)),.3125,detail)})`:`translateY(${-150*aux}px) scale(${mix(1,.88,aux)})`,transformOrigin:'540px 790px'}}>
  <DonutShare detailHandoff={detail} segments={[{label:meaning,value:share},{label:'其余人群',value:1-share}]} highlight={0} decimals={share<.01?1:0} centerNote="同一总体" highlightLabel={count} cues={kind==='pro'?[0,1.5]:[.1,2.7]}/>
  <Text y={195} size={kind==='pro'?56:70} opacity={1-detail}>{meaning}</Text>
 </div>
 {kind==='large'&&t>=7&&<><Text y={1460} size={73} opacity={p(t,7.8,8.3)}>听过 AI</Text><Text y={1570} size={68} color={S.accent} opacity={p(t,8.4,8.9)}>≠ 亲手用过</Text></>}
 {kind==='casual'&&t>=7&&<><Text y={1460} size={73} opacity={p(t,7.8,8.3)}>查资料 · 改文字</Text><Text y={1570} size={60} color={S.accent} opacity={p(t,8.7,9.2)}>更像一个问答工具</Text></>}
 </Frame>;
}
function Task(){
 const t=useT(),out=q(t,9.5,10.2);
 return <Frame><div style={{position:'absolute',inset:0,transform:`translateY(${-1500*out}px) scale(${1-.25*out})`,transformOrigin:'540px 685px'}}>
  <SyncVsCopy sourceReady author="待办清单" authorNote="新增 · 完成" versions={['一条事项','已完成']} zip={{title:'未保存',note:'再打开：记录丢失',after:'回到保存逻辑'}} clone={{title:'已保存',note:'再打开：检查结果',after:'事项仍在'}} cues={[1.2,3,4.5]}/>
  <Text y={230} size={76} opacity={p(t,0,.3)*(1-out)}>保存后，再打开</Text>
 </div>{out>0&&<Capsule text="做一份待办清单" y={mix(1400,860,out)} x={80} w={920} opacity={p(t,9.5,9.7)} size={78}/>}</Frame>;
}
function Roles(){
 const t=useT(),join=q(t,6.4,7.2),cause=q(t,8.4,9.1);
 return <Frame>
  {t<7.2&&<div style={{position:'absolute',inset:0,clipPath:`inset(0px 0px ${mix(0,1060,join)}px 0px)`}}>
   <RoleSplit task="做一份待办清单" roles={[{step:'新增',tool:'Agent A',logo:''},{step:'完成',tool:'Agent B',logo:''},{step:'保存',tool:'Agent C',logo:''}]} highlight="" cues={[1.1,2,3.1,4.2]}/>
   <Text y={220} size={74}>多 Agent 协作</Text>
  </div>}
  {t<6.4&&<Text y={1430} size={70} opacity={p(t,4.6,5.1)}>分工，再汇合</Text>}
  {join>0&&<><svg width={1080} height={1920} style={{position:'absolute',inset:0}}>{[223,540,857].map(x=><path key={x} d={`M${x} 900 Q${x} 1050 540 1080`} fill="none" stroke={S.ink} strokeWidth={5} pathLength={1} strokeDasharray="1" strokeDashoffset={1-join} opacity={1-cause}/>)}</svg><Capsule text={cause<.5?'待办清单':'差距来自哪里？'} y={cause>0?mix(1080,450,cause):mix(1350,1080,join)} opacity={join}/></>}
  {t>=9.1&&['任务','领域','权限'].map((x,i)=><Capsule key={x} text={x} x={100+i*310} y={900+60*(1-p(t,9.2+i*.7,9.7+i*.7))} w={260} h={180} size={80} opacity={p(t,9.2+i*.7,9.7+i*.7)}/>)}
  {t>=11.3&&<Text y={1270} size={64} opacity={p(t,11.3,11.8)}>从一个具体任务看</Text>}
 </Frame>;
}
// The same task window continues from a question into its inspection sequence.
function TaskSequence(){
 const t=useT(),open=q(t,0,.6),chain=q(t,6.4,7.1);
 return <Frame>

  {t<7.1&&<MacWindow box={{x:90,y:mix(900,600,open),w:900,h:mix(180,810,open)}} title="待办清单"><div style={{opacity:p(t,.6,1)*(1-chain),padding:'90px 60px',color:'#fff'}}>
   <div style={{...textBase(65,900),whiteSpace:'normal'}}>怎样做待办清单？</div>
   <div style={{marginTop:80,...textBase(54,500),color:S.accentDark,opacity:p(t,2,2.5)}}>得到一段说明</div>
   {[380,600,490].map((w,i)=><div key={i} style={{marginTop:28,width:w*p(t,3+i*.4,3.5+i*.4),height:12,borderRadius:6,background:'#77777f'}}/>)}
  </div></MacWindow>}
  {t>=6.4&&<Sequence from={384}><div style={{position:'absolute',inset:0,clipPath:`inset(600px 90px 510px round 36px)`}}>
   <StepChain steps={['新增事项','标记完成','保存','再打开','检查记录']} title="待办清单" highlight={t<14?2:4} cues={[.7,3.1,5.2,7.3,10.1]}/>
  </div></Sequence>}
  <Text y={220} size={t<7?63:70}>{t<7?'只问：怎样做待办清单？':t<14?'新增事项 → 标记完成':'把目标拆成步骤'}</Text>
  {t>=10&&<Text y={1510} size={64} opacity={p(t,10,10.5)}>{t<14?'保存后，再打开':'才知道要检查什么'}</Text>}
 </Frame>;
}
// Conditional teaching graphic: no claimed test run or actual successful app.
function Inspect(){
 const t=useT(),refresh=q(t,2.2,2.9),missing=q(t,7,7.7),domain=q(t,14,14.7);
 return <Frame>
  <Text y={200} size={72}>{t<7?'检查保存功能':t<14?'如果不在':'数学、编程'}</Text>
  {t<14.7&&<div style={{position:'absolute',inset:0,transform:`scale(${1-.25*domain}) translateY(${-600*domain}px)`,transformOrigin:'540px 1000px'}}>
   <MacWindow box={{x:90,y:600,w:900,h:810}} title="待办清单"><div style={{position:'absolute',left:50,top:65,...textBase(58,900),color:'#fff'}}>刷新后，事项还在吗？</div></MacWindow>
   <svg width={1080} height={1920} style={{position:'absolute',inset:0}}><g transform={`translate(890 645) rotate(${360*refresh})`}><path d="M-20 0 A20 20 0 1 1 -5 19 M-20 0 L-23 -13 M-20 0 L-7 -3" stroke={S.accentDark} strokeWidth={5} fill="none"/></g></svg>
   <Surface box={{x:150,y:mix(880,1010,missing),w:780,h:160}} style={{display:'flex',alignItems:'center',justifyContent:'center',opacity:1-missing}}><span style={{...textBase(65,900)}}>一条事项 <span style={{color:S.accent}}>？</span></span></Surface>
   {t>=7&&<><Text y={910} size={62} color="#fff" opacity={p(t,7.7,8.2)}>回到保存逻辑</Text><svg width={1080} height={1920} style={{position:'absolute',inset:0}}><path d="M800 1110 C800 1240 280 1240 280 1110 L280 1050 M260 1072 L280 1050 L300 1072" fill="none" stroke={S.accentDark} strokeWidth={7} pathLength={1} strokeDasharray="1" strokeDashoffset={1-p(t,9,9.7)}/></svg><Text y={1270} size={48} color="#fff" opacity={p(t,10.5,11)}>再检查记录</Text></>}
   {t<4&&<Cursor x={mix(770,877,p(t,1.5,2.1))} y={mix(790,633,p(t,1.5,2.1))} scale={.9} press={1-Math.abs(2*q(t,2.1,2.4)-1)}/>}
   <ClickRing x={890} y={645} t={t} at={2.2} dark/>
  </div>}
  {t>=14&&<><Text y={1460} size={68} opacity={p(t,14.7,15.2)}>结果更容易验证</Text>
   {['数学','编程'].map((label,i)=><React.Fragment key={label}><Capsule text={label} x={130+i*460} y={700} w={360} opacity={p(t,14.6+i,15+i)}/><Surface box={{x:130+i*460,y:1050,w:360,h:230}} style={{opacity:p(t,16+i,16.5+i),display:'flex',alignItems:'center',justifyContent:'center'}}><span style={{...textBase(62,900)}}>{i===0?'核算结果':'检查运行'}</span></Surface><svg width={1080} height={1920} style={{position:'absolute',inset:0}}><path d={`M${310+i*460} 910 V1030`} stroke={S.ink} strokeWidth={5} pathLength={1} strokeDasharray="1" strokeDashoffset={1-p(t,15.5+i,16+i)}/></svg></React.Fragment>)}
  </>}
 </Frame>;
}
function Access(){
 const t=useT(),merge=q(t,14.2,15),close=q(t,20.2,21);
 return <Frame>
  {t<15&&<div style={{position:'absolute',inset:0,clipPath:`inset(0px 0px ${mix(0,850,merge)}px 0px)`}}>
   <DecisionTree question="访问条件" branches={[{condition:'免费版',answer:'公开入口'},{condition:'付费版',answer:'订阅入口'},{condition:'内部系统',answer:'内部授权'}]} recommend={-1} cues={[1.3,3.2,5.1,100]}/>
   <Text y={200} size={70}>能接触哪些系统</Text><Text y={1460} size={65} opacity={p(t,7.5,8)}>取决于访问条件</Text>
  </div>}
  {t>=14.2&&<><svg width={1080} height={1920} style={{position:'absolute',inset:0}}>{[220,540,860].map(x=><path key={x} d={`M${x} 1190 Q${x} 1380 540 1380`} fill="none" stroke={S.ink} strokeWidth={6} opacity={1-close} pathLength={1} strokeDasharray="1" strokeDashoffset={1-merge}/>)}</svg>
   {['任务','领域','权限'].map((label,i)=><Capsule key={label} text={close>.1?'':label} x={mix(80+i*320,90,close)} y={mix(1100,850,close)} w={mix(280,900,close)} h={180} size={75} opacity={p(t,15,15.3)*(close<1?1:0)}/>)}
   <Capsule text={close>.5?'你交给 AI 什么任务？':'共同影响 AI 体验'} y={mix(1380,850,close)} h={mix(180,220,close)} size={close>.5?67:74} opacity={p(t,16,16.5)}/>
   <Text y={250} size={74} opacity={p(t,15,15.5)*(1-close)}>差距从这里产生</Text>
  </>}
 </Frame>;
}
export function Episode(){
 return <AbsoluteFill style={{background:'#fff'}}>
  <Sequence from={0} durationInFrames={960}><Intro/></Sequence>
  <Sequence from={960} durationInFrames={720}><Population share={.75} count="约60亿人" meaning="几乎未接触大语言模型" kind="large"/></Sequence>
  <Sequence from={1680} durationInFrames={780}><Population share={.2} count="约10—20亿人" meaning="偶尔使用免费聊天产品" kind="casual"/></Sequence>
  <Sequence from={2460} durationInFrames={300}><Population share={.002} count="约2000万人" meaning="数学／编程中专业使用前沿模型" kind="pro"/></Sequence>
  <Sequence from={2760} durationInFrames={780}><MagnifiedClock/></Sequence>
  <Sequence from={3540} durationInFrames={660}><PillToWindow hook="检查保存功能" highlight="" cues={[.1,100]}><Sequence from={48}><Task/></Sequence></PillToWindow></Sequence>
  <Sequence from={4200} durationInFrames={840}><Roles/></Sequence>
  <Sequence from={5040} durationInFrames={1260}><TaskSequence/></Sequence>
  <Sequence from={6300} durationInFrames={1260}><Inspect/></Sequence>
  <Sequence from={7560} durationInFrames={1440}><Access/></Sequence>
 </AbsoluteFill>;
}
function MagnifiedClock(){return <Magnified t={useT()}/>;}
