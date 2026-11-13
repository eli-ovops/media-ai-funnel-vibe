import React from 'react';
import {Frame,textBase} from './kit/ui';
import {S,p,q,mix} from './kit/theme';
const SX=775,SY=450,R=100,SW=41.25;
// A selected annular interval unfolds into a ruled linear window. Coordinates
// interpolate geometry, never population values. Range and fraction stay fixed.
function outline(range:number,u0:number,u1:number,k:number,x:number,y:number,w:number,h:number){
 const pts:number[][]=[];
 for(const side of [0,1])for(let j=0;j<=24;j++){
  const u=side===0?mix(u0,u1,j/24):mix(u1,u0,j/24),a=u*range*Math.PI*2,rr=R+(side===0?SW/2:-SW/2);
  pts.push([mix(SX+Math.sin(a)*rr,x+u*w,k),mix(SY-Math.cos(a)*rr,y+side*h,k)]);
 }
 return pts.map((v,i)=>`${i?'L':'M'}${v[0]},${v[1]}`).join(' ')+'Z';
}
const label=(text:string,x:number,y:number,size:number,opacity=1,align:'left'|'center'='left',color=S.ink)=><div style={{position:'absolute',left:x,top:y,width:900,...textBase(size,900),whiteSpace:'normal',opacity,color,textAlign:align}}>{text}</div>;
export function Magnified({t}:{t:number}){
 const first=q(t,.35,2.3),swap=q(t,6.7,8.1),second=q(t,7.4,9),micro=t>=7.4;
 const carrier=q(t,11.3,12.5),remain=1-carrier;
 const ax=mix(160,160,swap),ay=mix(900,1390,swap),aw=mix(760,420,swap),ah=mix(150,76,swap),oldAlpha=1-q(t,9.3,10.1);
 const bx=160,by=900,bw=760,bh=150;
 const trueFraction=micro?.0000006:.002,a=trueFraction*Math.PI*2;
 const sourceArc=`M${SX} ${SY-R} A${R} ${R} 0 0 1 ${SX+Math.sin(a)*R} ${SY-Math.cos(a)*R}`;
 const layer=(range:number,fraction:number,k:number,x:number,y:number,w:number,h:number,alpha:number,scope:string)=><g opacity={alpha}>
  <path d={outline(range,0,1,k,x,y,w,h)} fill="#d3d3d9"/>
  <path d={outline(range,0,fraction/range,k,x,y,w,h)} fill={S.accent}/>
  {k>.08&&<path d={`M${SX} ${SY-R-SW/2} Q${SX-160} ${SY-60} ${mix(SX,x,k)} ${mix(SY-R,y,k)} M${SX+Math.sin(range*Math.PI*2)*(R+SW/2)} ${SY-Math.cos(range*Math.PI*2)*(R+SW/2)} Q${SX+150} ${SY+200} ${mix(SX,x+w,k)} ${mix(SY-R,y,k)}`} stroke="#9b9ba5" strokeWidth={2} fill="none" opacity={Math.min(k*2,1)*(1-q(k,.65,1))}/ >}
  {k>.98&&<><line x1={x} y1={y+h+20} x2={x+w} y2={y+h+20} stroke={S.ink} strokeWidth={2}/><text x={x} y={y+h+65} style={textBase(32,500)}>0</text><text x={x+w} y={y+h+65} textAnchor="end" style={textBase(32,500)}>{scope}</text></>}
 </g>;
 return <Frame>
  <div style={{opacity:remain}}>
   <svg width={1080} height={1920} style={{position:'absolute',inset:0}}>
    <circle cx={SX} cy={SY} r={R} fill="none" stroke="#d3d3d9" strokeWidth={SW}/><path d={sourceArc} fill="none" stroke={S.accent} strokeWidth={SW}/>
    {layer(.01,.002,first,ax,ay,aw,ah,oldAlpha,'1%')}
    {t>=7.4&&layer(.000001,.0000006,second,bx,by,bw,bh,1,'0.0001%')}
   </svg>
   {label('同一总体',160,380,45)}
   {label(micro?'可访问内部前沿系统':'数学／编程中专业使用前沿模型',90,140,60,1,'center')}
   {t<7.4?label('约0.2%',90,690,136,p(t,2.3,2.6),'center',S.accent):label('约0.00006%',90,690,112,p(t,9,9.3),'center',S.accent)}
   {micro&&label('0.2% · 约2000万人',160,ay-55,32,oldAlpha)}
   {label('放大范围：总体的1%',160,ay+ah+95,39,p(t,2.3,2.6)*oldAlpha)}
   {t>=7&&label('放大范围：总体的0.0001%',160,by+bh+95,39,p(t,9,9.3))}
   {t<7.4?label('约2000万人',90,1225,62,p(t,2.3,2.6)*(1-q(t,6.5,6.7)),'center'):label('约5000人',90,1225,62,p(t,9,9.3),'center')}
  </div>
  {carrier>0&&<div style={{position:'absolute',left:mix(160,115,carrier),top:mix(900,850,carrier),width:mix(456,850,carrier),height:mix(150,200,carrier),background:S.dark,borderRadius:100*carrier,boxShadow:S.capsuleShadow,display:'flex',alignItems:'center',justifyContent:'center'}}><span style={{...textBase(78,400,S.display),color:'#fff',opacity:p(t,12,12.5)}}>检查保存功能</span></div>}
 </Frame>;
}
