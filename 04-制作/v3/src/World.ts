// Adapted actions: T15f DonutShare sweep/radial extraction; T05h same-source paths; T04b role split; T20m carrier-to-window; sy17 logarithmic camera. One150s world clock.
import {S,clamp,mix,p,q,springAt,syncPoint,roleSplit,pillWindow,editorialCamera} from './kit';
import content from '../content-package.json';
type C=CanvasRenderingContext2D;type V=[number,number];const TAU=Math.PI*2;
const colors=[S.gold,S.teal,'#e7a77d','#b6b4ec'];
const shares=[.75,.20,.002,.0000006];const pct=['75%','20%','0.2%','0.00006%'];const counts=['约60亿人','约10—20亿人','约2000万人','约5000人'];
function alpha(c:C,a:number,fn:()=>void){if(a<=0)return;c.save();c.globalAlpha*=clamp(a);fn();c.restore()}
function text(c:C,s:string,x:number,y:number,size=52,col=S.ink,weight=500,align:CanvasTextAlign='left'){c.font=`${weight} ${size}px "${weight===800?'Fred MiSans Heavy':S.body}"`;c.textAlign=align;c.textBaseline='top';c.fillStyle=col;c.fillText(s,x,y)}
function rr(c:C,x:number,y:number,w:number,h:number,r:number,fill:string,stroke?:string){if(w<=0||h<=0)return;c.beginPath();c.roundRect(x,y,w,h,Math.min(r,w/2,h/2));c.fillStyle=fill;c.fill();if(stroke){c.strokeStyle=stroke;c.lineWidth=2;c.stroke()}}
function line(c:C,v:V[],col=S.edge,w=3,dash:number[]=[]){if(v.length<2)return;c.beginPath();c.moveTo(...v[0]);v.slice(1).forEach(x=>c.lineTo(...x));c.strokeStyle=col;c.lineWidth=w;c.lineCap='round';c.lineJoin='round';c.setLineDash(dash);c.stroke();c.setLineDash([])}
function circle(c:C,x:number,y:number,r:number,col:string,fill=false,w=3){if(r<=0)return;c.beginPath();c.arc(x,y,r,0,TAU);if(fill){c.fillStyle=col;c.fill()}else{c.strokeStyle=col;c.lineWidth=w;c.stroke()}}
function pathPoint(a:V,b:V,u:number):V{const v=syncPoint(...a,...b,u);return[v.x,v.y]}
function route(c:C,a:V,b:V,u=1,col=S.edge,w=3){if(u<=0)return;line(c,Array.from({length:49},(_,i)=>pathPoint(a,b,i/48*u)),col,w)}
function glowDot(c:C,x:number,y:number,r=7,col=S.gold){c.save();c.shadowColor=col;c.shadowBlur=20;circle(c,x,y,r,col,true);c.restore()}
function tick(c:C,x:number,y:number,k=1,size=24,col=S.dark){const ps:V[]=[[x-size*.5,y],[x-size*.1,y+size*.4],[x+size*.6,y-size*.45]];line(c,k<.5?[ps[0],[mix(ps[0][0],ps[1][0],k*2),mix(ps[0][1],ps[1][1],k*2)]]:[ps[0],ps[1],[mix(ps[1][0],ps[2][0],(k-.5)*2),mix(ps[1][1],ps[2][1],(k-.5)*2)]],col,5)}
function item(c:C,x:number,y:number,w=160,h=42,checked=0,col=S.gold){rr(c,x-w/2,y-h/2+7,w,h,8,'#0d1413');rr(c,x-w/2,y-h/2,w,h,8,col);rr(c,x-w/2+12,y-11,22,22,4,'#ffffff15',S.dark);line(c,[[x-w/2+49,y],[x+w/2-16,y]],S.dark,4);if(checked>0)tick(c,x-w/2+23,y,checked,14)}
function background(c:C){c.fillStyle=S.bg;c.fillRect(0,0,1080,1920);const g=c.createRadialGradient(540,1010,50,540,1010,1050);g.addColorStop(0,'#2b3c34');g.addColorStop(1,S.bg);c.fillStyle=g;c.fillRect(0,0,1080,1920);c.fillStyle='#ffffff05';for(let i=0;i<500;i++)c.fillRect((i*173+37)%1080,(i*283+79)%1920,1,1)}
// T15f exact accumulated share geometry, zero gap and butt caps: never impose minimum visible angle.
export function donutShare(c:C,x:number,y:number,r:number,sw:number,share:number,col:string,sweep=1,pull=0){
 const span=share*TAU,head=sweep*TAU;
 const segment=(a:number,b:number,color:string,offset=0)=>{if(b<=a)return;const mid=span/2,dx=Math.sin(mid)*offset,dy=-Math.cos(mid)*offset;c.beginPath();c.arc(x+dx,y+dy+10,r,a-Math.PI/2,b-Math.PI/2);c.lineCap='butt';c.lineWidth=sw;c.strokeStyle='#0b1312';c.stroke();c.beginPath();c.arc(x+dx,y+dy,r,a-Math.PI/2,b-Math.PI/2);c.strokeStyle=color;c.stroke()};
 circle(c,x,y+10,r,'#0b1312',false,sw);circle(c,x,y,r,'#3d4c43',false,sw);
 segment(span,Math.max(span,head),'#53655b');segment(0,Math.min(span,head),col,pull);
}
function ringTicks(c:C,x:number,y:number,r:number,u=1){for(let i=0;i<100;i++){if(i/100>u)break;let a=i/100*TAU;line(c,[[x+Math.sin(a)*r,y-Math.cos(a)*r],[x+Math.sin(a)*(r+(i%5===0?13:5)),y-Math.cos(a)*(r+(i%5===0?13:5))]],i%25===0?S.dim:S.edge,1.5)}}
function fmt(n:number){return n>=1?n.toFixed(n<10?2:0).replace(/\.00$/,''):n.toFixed(n>=.01?3:6).replace(/0+$/,'').replace(/\.$/,'')}
export function chartGeometry(t:number){let i=t<33?0:t<46?1:t<61?2:3;let range=1;if(t>=46&&t<61)range=1/editorialCamera(t,[{t:46.5,x:0,y:0,z:1},{t:49,x:0,y:0,z:100}]).z;if(t>=61)range=.01/editorialCamera(t,[{t:61.3,x:0,y:0,z:1},{t:64.5,x:0,y:0,z:10000}]).z;return{index:i,share:shares[i],denominator:'same original overall population',spanRadians:shares[i]*TAU,rangeFraction:range,detailWidth:720*shares[i]/range,fullRingArcPixels:330*shares[i]*TAU,gap:0,minAngle:0}}
// The selected arc is unrolled preserving arc-length proportion, then a labeled window zooms into it.
function arcLens(c:C,t:number){const g=chartGeometry(t),unroll=q(t,46,47.3),z=1/g.rangeFraction;const top=1080,left=180,width=720,h=94;
 const guide=(end:number,col:string,w:number)=>{const points:V[]=[];for(let k=0;k<=120;k++){const u=end*k/120,a=u*TAU;const sx=540+Math.sin(a)*330,sy=960-Math.cos(a)*330;points.push([mix(sx,left+u*width*z,unroll),mix(sy,top,unroll)])}c.beginPath();c.moveTo(...points[0]);points.slice(1).forEach(v=>c.lineTo(...v));c.strokeStyle=col;c.lineWidth=w;c.lineCap='butt';c.stroke()};
 c.save();c.beginPath();c.rect(86,550,908,850);c.clip();guide(Math.min(1,1/z),'#4e6056',h);guide(Math.min(g.share,1/z),colors[g.index],h);c.restore();
 alpha(c,q(t,47.3,47.6),()=>{line(c,[[left,top+75],[left+width,top+75]],S.dim,2);for(let j=0;j<=4;j++){const x=left+j*width/4;line(c,[[x,top+65],[x,top+90]],S.dim,2);text(c,fmt(g.rangeFraction*100*j/4)+'%',x,top+108,30,S.dim,500,'center')}
 text(c,'放大视窗',90,1305,38,S.dim);text(c,'这一整段 = 总体的 '+fmt(g.rangeFraction*100)+'%',90,1363,42,S.ink);
 if(t>=64.5)text(c,'全图中的扇区小于1像素',90,1430,34,S.dim);
 if(t>=49&&t<61){const x=left+g.detailWidth;line(c,[[x,top-55],[x,top-95]],colors[g.index],2);text(c,'0.2%',x,top-152,42,colors[g.index],800,'center')}
 if(t>=64.5){const x=left+g.detailWidth;line(c,[[x,top-55],[x,top-95]],colors[g.index],2);text(c,'0.00006%',x,top-152,40,colors[g.index],800,'center')}
 });
}
function chart(c:C,t:number){
 const g=chartGeometry(t),i=g.index,entry=1,small=q(t,46,47.3);const x=mix(540,855,small),y=mix(960,750,small),r=mix(330,82,small),sw=mix(126,29,small);
 const switchAt=i===0?20:i===1?33:46;const retract=i===0?1-q(t,32.5,33):i===1?1-q(t,45.5,46):0;
 const pull=i<2?36*springAt(t,switchAt,.75)*retract:0;
 donutShare(c,x,y,r*entry,sw*entry,g.share,colors[i],q(t,12.5,15),pull);ringTicks(c,x,y,(r+sw/2+30)*entry,q(t,13,15.4));
 if(t<20){alpha(c,q(t,13.4,14),()=>{text(c,'同一总体',540,904,62,S.ink,800,'center');text(c,'100%',540,985,48,S.dim,500,'center')})}
 else if(t<46){alpha(c,q(t,switchAt,switchAt+.7),()=>{text(c,'约 '+pct[i],540,876,i===0?100:104,colors[i],800,'center');text(c,counts[i],540,1008,i===0?64:58,S.ink,800,'center')});text(c,'以同一总体为参照',540,1398,38,S.dim,500,'center');if(i===0&&t>=23&&t<27)text(c,'其余约25%',832,562,36,S.dim,500,'center')}
 else{alpha(c,q(t,47.1,47.4),()=>{text(c,'总体',855,878,32,S.dim,500,'center');line(c,[[855,640],[855,610],[911,610]],S.dim,2);text(c,'位置',925,590,28,S.dim);text(c,'约 '+pct[i],90,687,i===2?110:78,colors[i],800);text(c,counts[i],90,825,67,S.ink,800)});arcLens(c,t)}
 // A real interaction occurs in the established ring, rather than a new card page.
 if(t>=27&&t<33){let u=q(t,28,29.3);alpha(c,q(t,27,27.5),()=>{route(c,[180,1510],[400,1510],.75,S.edge,4);glowDot(c,mix(180,330,u),1510,7);line(c,[[348,1488],[348,1532]],S.dim,4);text(c,'听过',160,1570,36,S.dim);text(c,'使用',365,1570,36,S.dim)})}
 if(t>=40&&t<46){alpha(c,q(t,40,40.5)*(1-q(t,45.5,46)),()=>{rr(c,385,1150,310,136,28,S.teal);for(let j=0;j<3;j++)line(c,[[421,1182+j*30],[421+230*q(t,40.6+j*.35,41.6+j*.35),1182+j*30]],S.dark,6);glowDot(c,695,1218,6,S.gold)})}
}
// Continuous work-space. These are working objects, not three reading cards.
const A:V=[-650,-120],E:V=[0,-120],D:V=[650,-120],R:V=[650,470],VFY:V=[0,470],H:V=[0,-670],G:V=[-650,470];
const edges:[V,V][]=[[H,A],[H,E],[H,D],[A,E],[E,D],[D,R],[R,VFY],[VFY,E],[G,A],[G,E],[G,H]];
function refresh(c:C,x:number,y:number,angle:number,col=S.teal){c.save();c.translate(x,y);c.rotate(angle);c.beginPath();c.arc(0,0,29,-.5,4.9);c.strokeStyle=col;c.lineWidth=5;c.stroke();line(c,[[0,-34],[14,-26],[19,-42]],col,5);c.restore()}
function paper(c:C,x:number,y:number,t:number,reopen=false){c.save();c.translate(x,y);const v=pillWindow(t,75.8,160,42,270,330);let w=t<78?v.w:270,h=t<78?v.h:330;rr(c,-w/2,-h/2+16,w,h,20,'#0b1312');rr(c,-w/2,-h/2,w,h,20,S.paper);alpha(c,q(t,76.1,77.2),()=>{line(c,[[-92,-111],[69,-111]],'#485f54',8);for(let j=0;j<3;j++){rr(c,-95,-57+j*62,22,22,4,'#d2d8c8');line(c,[[-52,-45+j*62],[87-j*14,-45+j*62]],'#adbba9',6)}});if(reopen)refresh(c,0,229,q(t,103.3,104.6)*TAU+q(t,110,111)*TAU);c.restore()}
function database(c:C,x:number,y:number,t:number){c.save();c.translate(x,y);for(let j=3;j>=0;j--){let yy=j*35-65;rr(c,-108,yy,216,48,13,j===0?'#50776a':'#29483e',S.edge);c.beginPath();c.ellipse(0,yy,108,28,0,0,TAU);c.fillStyle=j===0?'#80a698':'#3e6152';c.fill();c.strokeStyle=S.edge;c.lineWidth=2;c.stroke()}const v=q(t,92.5,93.5)+q(t,113.7,114.8);alpha(c,clamp(v),()=>{line(c,[[-68,91],[68,91]],S.gold,6);for(let i=0;i<3;i++)glowDot(c,-28+i*28,52,4,S.gold)});c.restore()}
function sceneCam(t:number){const ks=[
 {t:0,x:0,y:-250,z:.54},{t:1,x:0,y:-250,z:.58},{t:5,x:0,y:-250,z:.58},{t:6.8,x:0,y:-250,z:.62},{t:9,x:0,y:-250,z:.62},{t:11.7,x:0,y:-300,z:.56},
 {t:75,x:0,y:-670,z:.01},{t:76,x:0,y:-670,z:.55},{t:78,x:0,y:-220,z:.62},{t:81.5,x:0,y:-220,z:.62},
 {t:83,x:-520,y:-160,z:1.35},{t:88,x:-650,y:60,z:1.35},{t:89.4,x:0,y:-120,z:1.35},{t:91.5,x:0,y:-120,z:1.35},{t:92.8,x:650,y:-120,z:1.35},{t:94.4,x:650,y:470,z:1.35},{t:95.6,x:650,y:425,z:1.35},{t:97,x:300,y:130,z:.8},{t:102,x:300,y:130,z:.8},
 {t:103.4,x:650,y:470,z:1.45},{t:109.7,x:650,y:470,z:1.45},{t:111,x:650,y:190,z:1.04},{t:112.5,x:650,y:190,z:1.04},{t:114,x:650,y:-120,z:1.35},{t:115.4,x:650,y:-120,z:1.35},{t:116.6,x:650,y:470,z:1.35},
 {t:118.4,x:0,y:470,z:1.3},{t:123.4,x:0,y:470,z:1.3},{t:125,x:-220,y:0,z:.64},{t:131.4,x:-220,y:0,z:.64},{t:133,x:-400,y:140,z:.85},{t:138,x:-400,y:140,z:.85},{t:141,x:0,y:0,z:.46},{t:144,x:0,y:0,z:.16},{t:150,x:0,y:0,z:.16}];
 if(t>=88&&t<95.6){let v:V;
 if(t<90.4)v=pathPoint([A[0],A[1]+180],[E[0],E[1]-45],q(t,89,90.4));
 else if(t<92)v=[E[0],E[1]-45];else if(t<93.2)v=pathPoint([E[0],E[1]-45],[D[0],D[1]-35],q(t,92,93.2));
 else if(t<94.1)v=[D[0],D[1]-35];else v=pathPoint([D[0],D[1]-35],[R[0],R[1]-45],q(t,94.1,95.3));
 return{x:v[0],y:v[1],z:1.35};}
 if(t>=116.6&&t<118.4){const v=pathPoint([R[0],R[1]-45],[VFY[0],VFY[1]-40],q(t,117,118.4));const u=q(t,117,118.4);return{x:v[0],y:v[1]+mix(45,40,u),z:mix(1.35,1.3,u)};}
 return editorialCamera(t,ks);
}
export function workSpace(c:C,t:number,override?:{x:number,y:number,z:number}){let cam=override||sceneCam(t);c.save();c.beginPath();c.rect(0,540,1080,1110);c.clip();c.translate(540,960);c.scale(cam.z,cam.z*.86);c.rotate(-.10);c.translate(-cam.x,-cam.y);
 const intro=t<12,build=intro?q(t,.2,2):q(t,77,78.2),fadeGrid=intro?.35:1;
 // Route rails and small origin ticks provide a continuous map for camera tours.
 alpha(c,fadeGrid*build,()=>{for(let x=-1050;x<=1050;x+=75)for(let y=-900;y<=900;y+=75)circle(c,x,y,1.2,'#52665a',true)});
 (intro?edges.slice(0,2):edges).forEach(([a,b],i)=>route(c,a,b,clamp(build*2-i*.07),i<3?'#5c7565':'#53756c',3));
 alpha(c,build,()=>{circle(c,...H,41,S.gold,false,3);glowDot(c,...H,11);line(c,[[H[0]-19,H[1]],[H[0]+19,H[1]]],S.gold,4)});
 if(intro){
  alpha(c,q(t,.5,1),()=>{rr(c,A[0]-150,A[1]-100,300,180,34,S.teal);for(let j=0;j<3;j++)line(c,[[A[0]-110,A[1]-55+j*40],[A[0]-110+210*q(t,1+j*.3,2+j*.3),A[1]-55+j*40]],S.dark,7)});
  for(let j=0;j<6;j++){const a:V=[250+(j%3)*170,-330+Math.floor(j/3)*190];route(c,H,a,q(t,1.3+j*.25,2.3+j*.25));alpha(c,q(t,2+j*.2,2.8+j*.2),()=>{circle(c,...a,30,S.teal);tick(c,...a,1,20,S.teal)})}
  for(let j=0;j<3;j++){let u=q(t,3+j*.7,4.5+j*.7);if(u>0&&u<1){const a=pathPoint(H,j===0?A:j===1?E:D,u);item(c,...a,80,24)}}
 }else{
 alpha(c,build,()=>{
  rr(c,A[0]-160,A[1]-80,320,170,28,'#497b70');for(let j=0;j<3;j++)line(c,[[A[0]-120,A[1]-40+j*36],[A[0]-120+220*q(t,83+j*.5,84+j*.5),A[1]-40+j*36]],S.paper,6);
  paper(c,...E,t);database(c,...D,t);paper(c,...R,t,true);
  circle(c,...VFY,118,'#52786a',false,3);line(c,[[VFY[0]-40,VFY[1]-12],[VFY[0]+40,VFY[1]-12]],S.teal,6);line(c,[[VFY[0]-40,VFY[1]+14],[VFY[0]+40,VFY[1]+14]],S.teal,6);
  // Access is one selector opening route barriers on a shared graph.
  circle(c,...G,76,S.edge,false,6);const access=t<128?0:t<131?1:2;const aim=[A,E,H][access];let angle=Math.atan2(aim[1]-G[1],aim[0]-G[0]);const open=q(t,124,125);
  line(c,[G,[G[0]+Math.cos(angle)*58,G[1]+Math.sin(angle)*58]],S.gold,7);
  for(let j=0;j<3;j++){const b=pathPoint(G,[A,E,H][j],.34);const on=t>=124&&j===access;line(c,[[b[0]-25,b[1]-25],[b[0]+25,b[1]+25*(1-2*Number(on))*open]],on?S.gold:S.edge,7);if(on){route(c,G,[[A[0]-170,A[1]],[E[0]-145,E[1]],[H[0],H[1]+50]][j] as V,q(t,124+j*3,125+j*3),S.gold,4)}}
  // Object labels travel with the world; main reading copy stays screen anchored.
  alpha(c,t>=88.5&&t<90.4?1-q(t,88.5,88.9)+q(t,90,90.4):1,()=>text(c,'问答',A[0],A[1]+130,42,S.dim,500,'center'));text(c,'事项',E[0],E[1]+206,42,S.dim,500,'center');text(c,'保存',D[0],D[1]+150,42,S.dim,500,'center');text(c,'再打开',R[0],R[1]+285,42,S.dim,500,'center');
  alpha(c,q(t,124,125),()=>{text(c,['免费版','付费版','内部系统'][access],G[0],G[1]+120,55,S.gold,800,'center')});
 });
 // Same item traverses the pipeline and has explicit stored/empty/feedback states.
 let pos:V=[0,-45],checked=q(t,91,91.7),visible=t>=89;
 if(t<90.4)pos=pathPoint([A[0],A[1]+180],[E[0],E[1]-45],q(t,89,90.4));
 else if(t<92)pos=[E[0],E[1]-45];
 else if(t<93.2)pos=pathPoint([E[0],E[1]-45],[D[0],D[1]-35],q(t,92,93.2));
 else if(t<94.1)pos=[D[0],D[1]-35];
 else if(t<95.3)pos=pathPoint([D[0],D[1]-35],[R[0],R[1]-45],q(t,94.1,95.3));
 else pos=[R[0],R[1]-45];
 if(t>=103&&t<105){const lift=Math.sin(q(t,103.3,104.6)*Math.PI)*180;pos=[R[0],R[1]-45-lift]}
 if(t>=110&&t<115.8)visible=false;
 if(t>=115.8&&t<117)pos=pathPoint([D[0],D[1]-35],[R[0],R[1]-45],q(t,115.8,116.8));
 if(t>=117&&t<119)pos=pathPoint([R[0],R[1]-45],[VFY[0],VFY[1]-40],q(t,117,118.4));
 if(t>=119)pos=[VFY[0],VFY[1]-40];
 if(visible)item(c,...pos,172,44,checked);
 if(t>=96&&t<103){for(let j=0;j<3;j++){const a=[E,D,R][j];let u=q(t,97+j*1.1,98+j*1.1);if(u>0&&u<1){const b=pathPoint(a,j===0?D:j===1?R:VFY,u);glowDot(c,...b,7)}}}
 if(t>=110&&t<117){line(c,[[R[0]-90,R[1]-65],[R[0]+90,R[1]-65],[R[0]+90,R[1]-20],[R[0]-90,R[1]-20],[R[0]-90,R[1]-65]],'#b7936b',3,[9,10]);const u=q(t,111,113.6),ra:V=[R[0]+175,R[1]],rb:V=[D[0]+175,D[1]+65];route(c,ra,rb,u,'#e7a77d',5);if(u>0&&u<1){const b=pathPoint(ra,rb,u);glowDot(c,...b,11,'#e7a77d')}if(t>=113.6){const a=q(t,113.6,114.6);alpha(c,a,()=>tick(c,D[0]+160,D[1],1,35,S.teal))}}
 if(t>=117&&t<124){const u=q(t,118.7,120);item(c,VFY[0],VFY[1]+40,172,44,1,S.teal);alpha(c,u,()=>{line(c,[[VFY[0]-112,VFY[1]-65],[VFY[0]-130,VFY[1]-65],[VFY[0]-130,VFY[1]+65],[VFY[0]-112,VFY[1]+65]],S.teal,3);tick(c,VFY[0]+172,VFY[1],1,43,S.gold)})}
 }
 c.restore();
}
function previewCircuit(c:C,t:number){const at=t<61?54:68,active=q(t,at,at+.6)*(1-q(t,at+6.5,at+7));alpha(c,active,()=>{const split=roleSplit(t,at,500,38,3),x=290,y=1520;for(let i=0;i<3;i++){const px=x+i*(split.segW+split.gap);rr(c,px,y,split.segW,38,split.innerR,colors[t<61?2:3]);const end:V=[px+split.segW/2,1640];route(c,[540,1490],end,q(t,at+.5,at+1.5),S.edge,2);circle(c,...end,18,S.teal);alpha(c,q(t,at+2.8+i*.5,at+3.3+i*.5),()=>tick(c,...end,1,15,S.teal));let u=q(t,at+2+i*.5,at+3.5+i*.5);if(u>0&&u<1){let p=pathPoint(end,[540,1490],u);glowDot(c,...p,5,colors[t<61?2:3])}}})}
function copy(c:C,t:number){const s=content.scenes.find(v=>t>=v.start_sec&&t<v.end_sec)||content.scenes[21];const a=q(t,s.start_sec,s.start_sec+.45)*(s.id==='closing'?1:1-q(t,s.end_sec-.2,s.end_sec));let lines=s.screen_lines.filter(v=>!v.startsWith('约'));
 const chartMode=t>=12&&t<75;let y=chartMode?290:280;let size=s.id==='question'?75:s.id==='closing'?70:60;
 if(t>=27&&t<33)y=285;
 alpha(c,a,()=>{for(let i=0;i<lines.length;i++){text(c,lines[i],90,y,size,i===0?S.ink:S.dim,i===0?800:500);y+=size*1.48}});
 text(c,t<75?'Karpathy 粗估':'Karpathy 观点',90,174,36,S.dim);
 if(t>=12&&t<75)text(c,'各项独立比较 · 非四块相加',90,1770,32,S.dim);
}
export function geometryAt(t:number){return{time:t,chart:chartGeometry(t),camera:sceneCam(t),persistentIds:['whole-ring','selected-arc','gold-task-item','work-network','storage','reopen','access-selector'],wholeSceneCrossfade:false}}
export function drawWorld(c:C,frame:number){const t=frame/60;c.setTransform(1,0,0,1,0,0);c.globalAlpha=1;c.clearRect(0,0,1080,1920);background(c);
 if(t<12){let pull=1-q(t,10.8,12);const old=sceneCam(t);workSpace(c,t,{x:old.x,y:old.y,z:old.z*Math.max(.001,pull)});if(t>=10.8)donutShare(c,540,960,330*q(t,10.8,12),126*q(t,10.8,12),.75,S.gold,0)}
 else if(t<75){chart(c,t);if(t>=54)previewCircuit(c,t)}
 else if(t<78){const v=q(t,75,77.4);c.save();c.translate(540,960);c.scale(Math.max(.001,1-v),Math.max(.001,1-v));c.translate(-540,-960);chart(c,74.999);c.restore();const g=chartGeometry(74.999);const x=mix(180+g.detailWidth/2,540,v),y=mix(1080,960,v);rr(c,x-mix(g.detailWidth,160,v)/2,y-mix(94,42,v)/2,mix(g.detailWidth,160,v),mix(94,42,v),mix(0,8,v),colors[3]);workSpace(c,t);}
 else{workSpace(c,t);if(t>=139){const u=q(t,139,144);donutShare(c,540,960,330*u,126*u,.0000006,colors[3],1,0);ringTicks(c,540,960,423*u);if(t>=144){text(c,'同一总体',540,520,42,S.dim,500,'center');text(c,'不同任务，不同体验',540,1400,52,S.ink,500,'center')}}}
 copy(c,t);
}
