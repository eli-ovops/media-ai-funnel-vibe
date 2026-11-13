// Scene adaptations of exact T03e StepChain topology, T05h state transmission, T04g branches and T20m single-carrier geometry. All surfaces/font/easing from retained Fred kit.
import React from 'react';
import {Sequence} from 'remotion';
import {StepChain} from './components/T03e-StepChain';
import {DecisionTree} from './components/T04g-DecisionTree';
import {Frame,Surface,Pill,MacWindow,Cursor,ClickRing,textBase,useT} from './kit/ui';
import {S,p,q,mix} from './kit/theme';
const Text=({children,y=220,size=68,opacity=1,color=S.ink}:{children:React.ReactNode,y?:number,size?:number,opacity?:number,color?:string})=><div style={{position:'absolute',left:90,top:y,width:900,textAlign:'center',...textBase(size,900),whiteSpace:'normal',opacity,color}}>{children}</div>;
const Capsule=({children,x=90,y,w=900,h=180,size=70,opacity=1}:{children:React.ReactNode,x?:number,y:number,w?:number,h?:number,size?:number,opacity?:number})=><Pill box={{x,y,w,h}} style={{opacity}}><span style={{...textBase(size,400,S.display),color:'#fff'}}>{children}</span></Pill>;
function Record({y,done,opacity=1,typed=1,compact=false}:{y:number,done:number,opacity?:number,typed?:number,compact?:boolean}){
 const title='整理客户需求',w=compact?700:740,x=(1080-w)/2,h=compact?142:190;
 return <Surface box={{x,y,w,h}} style={{opacity}}>
  <div style={{position:'absolute',left:28,top:26,...textBase(30,900),color:S.accent}}>01</div>
  <div style={{position:'absolute',left:112,top:compact?40:63,...textBase(compact?51:57,900)}}>{title.slice(0,Math.ceil(title.length*typed))}</div>
  <svg width={w} height={h} style={{position:'absolute',inset:0}}>
   <rect x={32} y={compact?65:96} width={44} height={44} rx={10} fill={done>0?S.accent:'#fff'} stroke={S.accent} strokeWidth={4}/>
   <path d={`M41 ${compact?87:118} l10 11 l20 -24`} stroke="#fff" strokeWidth={5} fill="none" pathLength={1} strokeDasharray="1" strokeDashoffset={1-done}/>
  </svg>
 </Surface>;
}
// Same identifiable record is added, checked, sent into storage, reopened and compared.
// Conditional loss/retry stays explicitly conditional: no actual app or successful product test is claimed.
export function ConcreteTask(){
 const t=useT(),intro=q(t,6.4,7.1),open=q(t,0,.6),done=q(t,11,11.5);
 const save=q(t,14.4,15.6),close=q(t,17,17.7),reopen=q(t,19,19.7);
 const absent=q(t,27.2,27.8),retry=q(t,32.6,33.8),leave=q(t,40.1,41);
 const rowVisible=t<17?1:t<19.7?0:t<27.2?1:t<32.6?1-absent:retry;
 const rowY=t<19.7?850:t<20.7?mix(1500,850,q(t,19.7,20.7)):t>=32.6&&t<33.8?mix(1500,850,retry):850;
 const heading=t<7?'只问：怎样做待办清单？':t<11?'新增一条具体事项':t<14?'标记为完成':t<17?'保存这条记录':t<21?'关掉，再打开':t<27?'核对内容和完成状态':t<34?'如果这条记录不在':'再次打开，核对同一条';
 const active=t<11?0:t<14?1:t<19?2:t<21?3:4;
 const windowX=t>=17&&t<19?mix(90,-1100,close):t>=19&&t<19.7?mix(1190,90,reopen):90;
 return <Frame>
  <Text opacity={1-q(t,40.1,40.4)} size={t<7?63:68}>{heading}</Text>
  {t>=40.5&&<Text y={200} size={72} opacity={p(t,40.5,41)}>数学、编程</Text>}
  {t>=7.1&&<div style={{opacity:1-leave}}><Sequence from={426}><StepChain navigation steps={['新增','完成','保存','重开','核对']} highlight={active} cues={[0,3.9,6.9,11.9,13.9]}/></Sequence></div>}
  <div style={{position:'absolute',inset:0,transform:`translateY(${1500*leave}px)`}}>
   <MacWindow box={{x:windowX,y:mix(900,600,open),w:900,h:mix(180,810,open)}} title="待办清单">
    {t<7.1&&<div style={{opacity:p(t,.6,1)*(1-intro),padding:'90px 60px',color:'#fff'}}>
     <div style={{...textBase(65,900),whiteSpace:'normal'}}>怎样做待办清单？</div>
     <div style={{marginTop:80,...textBase(54,500),color:S.accentDark,opacity:p(t,2,2.5)}}>得到一段说明</div>
     {[380,600,490].map((w,i)=><div key={i} style={{marginTop:28,width:w*p(t,3+i*.4,3.5+i*.4),height:12,borderRadius:6,background:'#77777f'}}/>)}
    </div>}
    {t>=7.1&&<div style={{position:'absolute',inset:0}}>
     <div style={{position:'absolute',left:55,top:55,...textBase(45,900),color:'#fff'}}>{t<21?'我的事项':t<27?'重开后的记录':t<34?'如果记录丢失':'再次核对'}</div>
     {t<34&&!(t>=19.7&&t<20.7)&&!(t>=32.6&&t<33.8)&&<Pill box={{x:590,y:490,w:250,h:116}} dark={false}><span style={{...textBase(48,900),color:S.accent}}>保存</span></Pill>}
    </div>}
   </MacWindow>
   {t>=7.1&&(t<17||t>=19.7)&&<Record y={rowY} done={done} opacity={p(t,7.1,7.5)*rowVisible} typed={p(t,7.7,9)}/>}
   {t>=21&&t<27&&<svg width={1080} height={1920} style={{position:'absolute',inset:0}}>
    <path d="M265 1020 H850" fill="none" stroke={S.accentDark} strokeWidth={6} pathLength={1} strokeDasharray="1" strokeDashoffset={1-p(t,21.4,22.2)}/>
    <rect x={192} y={936} width={64} height={64} rx={15} fill="none" stroke={S.accentDark} strokeWidth={5} opacity={p(t,23.1,23.6)}/>
   </svg>}
   {t>=27.8&&t<32.6&&<div style={{position:'absolute',left:170,top:850,width:740,height:190,border:`4px dashed ${S.faint}`,borderRadius:S.radius,boxSizing:'border-box'}}/>}
   {t>=27.8&&t<32.6&&<Text y={1070} size={50} color="#fff" opacity={p(t,28,28.4)*(1-p(t,32,32.5))}>回到保存逻辑</Text>}
   {t>=14.4&&<><Text y={1670} size={39} opacity={p(t,14.4,14.8)}>保存的记录</Text><Record y={1500} compact done={1} opacity={save}/></>}
   {t>=14.4&&t<17&&<svg width={1080} height={1920} style={{position:'absolute',inset:0}}><path d="M805 1308 V1395 Q805 1415 785 1415 H560 Q540 1415 540 1435 V1495" fill="none" stroke={S.accent} strokeWidth={6} pathLength={1} strokeDasharray="1" strokeDashoffset={1-save}/></svg>}
   {t>=29&&t<32.6&&<svg width={1080} height={1920} style={{position:'absolute',inset:0}}><path d="M540 1500 V1460 Q540 1425 580 1425 H805 Q935 1425 935 1295 Q935 1250 895 1250" fill="none" stroke={S.accent} strokeWidth={6} pathLength={1} strokeDasharray="1" strokeDashoffset={1-p(t,29,30.2)}/></svg>}
   {t>=34&&<><Text y={1100} size={50} color={S.accentDark} opacity={p(t,34.3,34.8)}>01 · 整理客户需求</Text><Text y={1190} size={48} color="#fff" opacity={p(t,36.1,36.6)}>还在吗？完成状态保留了吗？</Text></>}
   {t>=10.2&&t<12.2&&<Cursor x={mix(700,209,q(t,10.2,10.9))} y={mix(1150,958,q(t,10.2,10.9))} scale={.9}/>}
   {t>=13.3&&t<15.2&&<Cursor x={mix(400,800,q(t,13.3,14.3))} y={mix(1080,1230,q(t,13.3,14.3))} scale={.9}/>}
   <ClickRing x={224} y={968} t={t} at={11} dark/><ClickRing x={805} y={1235} t={t} at={14.4} dark/>
  </div>
 </Frame>;
}
export function Domains(){
 const t=useT();
 return <Frame><Text y={200} size={72}>数学、编程</Text>
  {['数学','编程'].map((label,i)=><React.Fragment key={label}>
   <Capsule x={130+i*460} y={700} w={360} opacity={p(t,.6+i,1+i)}>{label}</Capsule>
   <Surface box={{x:130+i*460,y:1050,w:360,h:230}} style={{opacity:p(t,2+i,2.5+i),display:'flex',alignItems:'center',justifyContent:'center'}}><span style={{...textBase(62,900)}}>{i===0?'核算结果':'检查运行'}</span></Surface>
   <svg width={1080} height={1920} style={{position:'absolute',inset:0}}><path d={`M${310+i*460} 890 V1030`} stroke={S.ink} strokeWidth={5} pathLength={1} strokeDasharray="1" strokeDashoffset={1-p(t,1.5+i,2+i)}/></svg>
  </React.Fragment>)}
  <Text y={1460} opacity={p(t,3.7,4.2)}>结果更容易验证</Text>
 </Frame>;
}
export function AccessRepair(){
 const t=useT(),exit=q(t,8.1,9),merge=q(t,13.5,14.3),finalMove=q(t,14.35,15);
 // Tree occupies 132–140.85; it is completely gone before factor paths begin.
 return <Frame>
  {t<9&&<div style={{position:'absolute',inset:0,transform:`translateY(${1700*exit}px)`,opacity:1-exit}}>
   <DecisionTree question="访问条件" branches={[{condition:'免费版',answer:'公开入口'},{condition:'付费版',answer:'订阅入口'},{condition:'内部系统',answer:'内部授权'}]} recommend={-1} cues={[1.3,3.2,5.1,100]}/>
   <Text y={200} size={70}>能接触哪些系统</Text>
  </div>}
  {t>=8.4&&<>
   <Text y={250} size={74} opacity={p(t,8.4,8.7)*(1-merge)}>差距从这里产生</Text>
   <svg width={1080} height={1920} style={{position:'absolute',inset:0}}>
    {[220,540,860].map(x=><path key={x} d={`M${x} 1280 Q${x} 1350 540 1380`} fill="none" stroke={S.ink} strokeWidth={6} pathLength={1} strokeDasharray="1" strokeDashoffset={1-p(t,9.5,10.1)} opacity={1-merge}/>)}
   </svg>
   {merge<1&&['任务','领域','权限'].map((label,i)=><div key={label} style={{position:'absolute',left:mix(80+i*320,540,merge),top:mix(1100,1470,merge),width:280,height:180,transform:`translate(${-140*merge}px,${-90*merge}px) scale(${1-.92*merge})`,transformOrigin:'50% 50%',opacity:p(t,8.85+i*.12,9.25+i*.12)*(1-q(t,14,14.3))}}>
    <Pill box={{x:0,y:0,w:280,h:180}}><span style={{...textBase(75,400,S.display),color:'#fff',opacity:1-p(t,13.5,13.8)}}>{label}</span></Pill>
   </div>)}
   <Pill box={{x:90,y:mix(1380,850,finalMove),w:900,h:mix(180,220,finalMove)}} style={{opacity:p(t,10,10.5)}}>
    {t<14.65?<span style={{...textBase(74,400,S.display),color:'#fff',opacity:1-p(t,14.35,14.6)}}>共同影响 AI 体验</span>:<span style={{...textBase(67,400,S.display),color:'#fff',opacity:p(t,14.65,15)}}>你交给 AI 什么任务？</span>}
   </Pill>
  </>}
 </Frame>;
}
