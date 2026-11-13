// Retains approved T15f/T05h/T02g/T04b/T20m; repair scenes adapt T03e/T04g with exact kit.
import {ConcreteTask,Domains,AccessRepair} from './RepairScenes';
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
export function Episode(){
 return <AbsoluteFill style={{background:'#fff'}}>
  <Sequence from={0} durationInFrames={960}><Intro/></Sequence>
  <Sequence from={960} durationInFrames={720}><Population share={.75} count="约60亿人" meaning="几乎未接触大语言模型" kind="large"/></Sequence>
  <Sequence from={1680} durationInFrames={780}><Population share={.2} count="约10—20亿人" meaning="偶尔使用免费聊天产品" kind="casual"/></Sequence>
  <Sequence from={2460} durationInFrames={300}><Population share={.002} count="约2000万人" meaning="数学／编程中专业使用前沿模型" kind="pro"/></Sequence>
  <Sequence from={2760} durationInFrames={780}><MagnifiedClock/></Sequence>
  <Sequence from={3540} durationInFrames={660}><PillToWindow hook="检查保存功能" highlight="" cues={[.1,100]}><Sequence from={48}><Task/></Sequence></PillToWindow></Sequence>
  <Sequence from={4200} durationInFrames={840}><Roles/></Sequence>
  <Sequence from={5040} durationInFrames={2460}><ConcreteTask/></Sequence>
  <Sequence from={7500} durationInFrames={420}><Domains/></Sequence>
  <Sequence from={7920} durationInFrames={1080}><AccessRepair/></Sequence>
 </AbsoluteFill>;
}
function MagnifiedClock(){return <Magnified t={useT()}/>;}
