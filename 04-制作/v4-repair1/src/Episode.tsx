import {Magnified} from './Magnified';
import React from 'react';
import {AbsoluteFill,Sequence,useCurrentFrame,useVideoConfig} from 'remotion';
import {DonutShare} from './components/T15f-DonutShare';
import {PillToWindow} from './components/T20m-PillToWindow';
import {SyncVsCopy} from './components/T05h-SyncVsCopy';
import {Frame,Surface,textBase,useT} from './kit/ui';
import {S,p,q,mix,clamp} from './kit/theme';
const Text=({children,y,size=64,color=S.ink,opacity=1}:{children:React.ReactNode,y:number,size?:number,color?:string,opacity?:number})=><div style={{position:'absolute',left:90,top:y,width:900,textAlign:'center',...textBase(size,900),whiteSpace:'normal',color,opacity}}>{children}</div>;
function Population({share,count,meaning,cues,detail=0}:{share:number,count:string,meaning:string,cues:number[],detail?:number}){return <><DonutShare detailHandoff={detail} segments={[{label:meaning,value:share},{label:'其余人群',value:1-share}]} highlight={0} decimals={share<.01?1:0} centerNote="同一总体" highlightLabel={count} cues={cues}/><Text y={195} size={70} opacity={1-detail}>{meaning}</Text></>}
function Task(){const t=useT();return <><SyncVsCopy sourceReady author="待办清单" authorNote="新增 · 完成" versions={['一条事项','已完成']} zip={{title:'未保存',note:'再打开：记录丢失',after:'回到保存逻辑'}} clone={{title:'已保存',note:'再打开：检查结果',after:'事项仍在'}} cues={[1.2,3,4.5]}/><Text y={230} size={76} opacity={p(t,0,.3)}>保存后，再打开</Text></>}
export function Representative(){const t=useT();
 return <AbsoluteFill style={{background:'#fff'}}>
  {t<7&&<Population share={.75} count="约60亿人" meaning="几乎未接触大语言模型" cues={[.35,3.1]}/>}
  {t>=7&&t<12&&<Sequence from={420}><div style={{position:'absolute',inset:0,transform:`translate(${mix(0,235,q(t,10.5,12))}px,${mix(0,-340,q(t,10.5,12))}px) scale(${mix(1,.3125,q(t,10.5,12))})`,transformOrigin:'540px 790px'}}><Population share={.002} count="约2000万人" meaning="专业使用前沿模型" cues={[0,1.5]} detail={q(t,10.5,12)}/></div></Sequence>}
  {t>=12&&t<25&&<Magnified t={t-12}/>}
  {t>=25&&<Sequence from={1500}><PillToWindow hook="检查保存功能" highlight="" cues={[.1,100]}><Sequence from={48}><Task/></Sequence></PillToWindow></Sequence>}
 </AbsoluteFill>
}
