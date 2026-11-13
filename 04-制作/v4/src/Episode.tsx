import React from 'react';
import {AbsoluteFill,Sequence,useCurrentFrame,useVideoConfig} from 'remotion';
import {DonutShare} from './components/T15f-DonutShare';
import {PillToWindow} from './components/T20m-PillToWindow';
import {SyncVsCopy} from './components/T05h-SyncVsCopy';
import {Frame,Surface,textBase,useT} from './kit/ui';
import {S,p,q,mix,clamp} from './kit/theme';
const Text=({children,y,size=64,color=S.ink,opacity=1}:{children:React.ReactNode,y:number,size?:number,color?:string,opacity?:number})=><div style={{position:'absolute',left:90,top:y,width:900,textAlign:'center',...textBase(size,900),whiteSpace:'normal',color,opacity}}>{children}</div>;
function Population({share,count,meaning,cues,detail=0}:{share:number,count:string,meaning:string,cues:number[],detail?:number}){return <><DonutShare detailHandoff={detail} segments={[{label:meaning,value:share},{label:'其余人群',value:1-share}]} highlight={0} decimals={share<.01?1:0} centerNote="同一总体" highlightLabel={count} cues={cues}/><Text y={195} size={70} opacity={1-detail}>{meaning}</Text></>}
function Magnified({t}:{t:number}){
 const zoom=q(t,0,1.5),micro=t>=7.5?1:0,fraction=mix(.002,.0000006,micro),range=mix(.01,.000001,micro);
 const actualWidth=760*fraction/range,stable=micro===0||micro===1;
 const top=920,sourceY=450,sourceX=775,r=100;
 // Exact tiny arc is never inflated. The detail is a ruled window whose denominator is visible.
 const a=fraction*Math.PI*2;let d=`M${sourceX} ${sourceY-r} A${r} ${r} 0 0 1 ${sourceX+Math.sin(a)*r} ${sourceY-Math.cos(a)*r}`;
 const carrier=q(t,11.3,12.5),barW=mix(actualWidth*zoom,850,carrier),barH=mix(150,200,carrier),barX=mix(160,115,carrier),barY=mix(top,850,carrier);
 return <Frame>
  <div style={{opacity:(1-carrier)*(t<7.5?1-q(t,7,7.5):p(t,7.5,8))}}>
   <Text y={100} size={64}>{micro<.5?'数学／编程中':'可访问'}</Text><Text y={180} size={64}>{micro<.5?'专业使用前沿模型':'内部前沿系统'}</Text>
   <svg width={1080} height={1920} style={{position:'absolute',inset:0}}><circle cx={sourceX} cy={sourceY} r={r} fill="none" stroke="#d3d3d9" strokeWidth={41.25}/><path d={d} fill="none" stroke={S.accent} strokeWidth={41.25}/><path d={`M${sourceX} ${sourceY-r-26} L${sourceX} ${sourceY-r-54} L590 ${sourceY-r-54}`} stroke={S.muted} fill="none" strokeWidth={2}/></svg>
   <div style={{position:'absolute',left:160,top:420,...textBase(45,500)}}>同一总体</div><div style={{position:'absolute',left:160,top:485,...textBase(34,500),color:S.muted}}>紫色扇区位于十二点方向</div>
   <Text y={650} size={micro<.5?150:114} color={S.accent}>{micro<.5?'约 0.2%':'约 0.00006%'}</Text>
   <div style={{position:'absolute',left:160,top:top,width:760*zoom,height:150,background:'#d3d3d9'}}/>
   <svg width={1080} height={1920} style={{position:'absolute',inset:0}}>{[0,1,2,3,4].map(i=><g key={i} opacity={p(t,1.1,1.5)}><line x1={160+190*i*zoom} y1={top+166} x2={160+190*i*zoom} y2={top+190} stroke={S.ink} strokeWidth={2}/><text x={160+190*i*zoom} y={top+240} textAnchor="middle" style={{...textBase(30,500)}}>{micro<.5?(i*.25).toFixed(2)+'%':(i*.000025).toFixed(6)+'%'}</text></g>)}</svg>
   <Text y={1265} size={43}>放大视窗 · 整条代表总体的</Text><Text y={1340} size={70}>{micro<.5?'1%':'0.0001%'}</Text>
   <Text y={1505} size={58}>{micro<.5?'约2000万人':'约5000人'}</Text>

  </div>
  <div style={{position:'absolute',left:barX,top:barY,width:barW,height:barH,background:carrier>0?S.dark:S.accent,opacity:carrier>0?1:(t<7.5?1-q(t,7,7.5):p(t,7.5,8)),borderRadius:100*carrier,boxShadow:carrier?S.capsuleShadow:undefined,display:'flex',alignItems:'center',justifyContent:'center'}}>{carrier>0&&<span style={{...textBase(78,400,S.display),color:'#fff',opacity:p(t,12,12.5)}}>检查保存功能</span>}</div>
 </Frame>
}
function Task(){return <><SyncVsCopy author="待办清单" authorNote="新增 · 完成" versions={['一条事项','已完成']} zip={{title:'未保存',note:'再打开：记录丢失',after:'回到保存逻辑'}} clone={{title:'已保存',note:'再打开：检查结果',after:'事项仍在'}} cues={[1.2,3,4.5]}/><Text y={230} size={76}>保存后，再打开</Text></>}
export function Representative(){const t=useT();
 return <AbsoluteFill style={{background:'#fff'}}>
  {t<7&&<Population share={.75} count="约60亿人" meaning="几乎未接触大语言模型" cues={[.35,3.1]}/>}
  {t>=7&&t<12&&<Sequence from={420}><div style={{position:'absolute',inset:0,transform:`translate(${mix(0,235,q(t,10.5,12))}px,${mix(0,-340,q(t,10.5,12))}px) scale(${mix(1,.3125,q(t,10.5,12))})`,transformOrigin:'540px 790px'}}><Population share={.002} count="约2000万人" meaning="专业使用前沿模型" cues={[0,1.5]} detail={q(t,10.5,12)}/></div></Sequence>}
  {t>=12&&t<25&&<Magnified t={t-12}/>}
  {t>=25&&<Sequence from={1500}><PillToWindow hook="检查保存功能" highlight="" cues={[.1,100]}><Task/></PillToWindow></Sequence>}
 </AbsoluteFill>
}
