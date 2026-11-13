import {S,clamp,mix,q,syncPoint,roleSplit,pillWindow,editorialCamera} from './kit';
import content from '../content-package.json';
type C=CanvasRenderingContext2D;type V=[number,number];type Pose={x:number,y:number,s:number,a:number,tilt:number};
const TAU=Math.PI*2;
function line(c:C,ps:V[],col=S.edge,w=3,dash:number[]=[]){if(ps.length<2)return;c.beginPath();c.moveTo(...ps[0]);ps.slice(1).forEach(v=>c.lineTo(...v));c.strokeStyle=col;c.lineWidth=w;c.lineCap='round';c.lineJoin='round';c.setLineDash(dash);c.stroke();c.setLineDash([])}
function rr(c:C,x:number,y:number,w:number,h:number,r:number,fill:string,stroke?:string){c.beginPath();c.roundRect(x,y,w,h,r);c.fillStyle=fill;c.fill();if(stroke){c.strokeStyle=stroke;c.lineWidth=2;c.stroke()}}
function dot(c:C,x:number,y:number,r=6,col=S.gold){c.beginPath();c.arc(x,y,r,0,TAU);c.fillStyle=col;c.fill()}
function curve(c:C,a:V,b:V,u=1,col=S.edge,w=3,dash=false){if(u<=0)return;line(c,Array.from({length:41},(_,i)=>{let p=syncPoint(...a,...b,i/40*u);return[p.x,p.y] as V}),col,w,dash?[8,10]:[])}
function token(c:C,p:V,w=32,h=15,col=S.gold){rr(c,p[0]-w/2,p[1]-h/2,w,h,h/2,col)}
function travel(a:V,b:V,u:number):V{const v=syncPoint(...a,...b,u);return[v.x,v.y]}
function text(c:C,s:string,x:number,y:number,size=64,col=S.ink,weight=500){c.font=`${weight} ${size}px "${weight===800?'Fred MiSans Heavy':S.body}"`;c.textBaseline='top';c.textAlign='left';c.fillStyle=col;c.fillText(s,x,y)}
function icon(c:C,k:number,x:number,y:number,sz=50,col=S.ink){c.save();c.translate(x,y);c.scale(sz/50,sz/50);c.strokeStyle=col;c.lineWidth=4;c.lineCap='round';c.lineJoin='round';c.beginPath();if(k===0){c.moveTo(-16,0);c.lineTo(16,0);c.moveTo(0,-16);c.lineTo(0,16)}else if(k===1){c.roundRect(-19,-19,38,38,6);c.moveTo(-10,0);c.lineTo(-2,9);c.lineTo(12,-9)}else if(k===2){c.roundRect(-22,-23,44,46,5);c.moveTo(-11,-23);c.lineTo(-11,-3);c.lineTo(11,-3);c.lineTo(11,-23);c.moveTo(-10,12);c.lineTo(10,12)}else{c.arc(0,0,21,-.4,5.1);c.moveTo(7,-24);c.lineTo(16,-16);c.lineTo(24,-24)}c.stroke();c.restore()}
// One stable paper/task ID. The full affine pose is interpolated, never cross-dissolved.
const keys=[
[0,745,850,1.05,-.12,.72],[6,745,850,1.05,-.12,.72],[12.5,760,1080,.64,-.06,.82],
[20,760,1080,.64,-.06,.82],[27,760,1080,.64,-.06,.82],[33.5,760,1120,.78,.06,1],
[40,760,1120,.78,.06,1],[46.5,760,1010,1,-.07,.76],[54.5,760,990,1,-.04,.86],
[61.5,760,990,.88,-.04,.86],[68,760,990,.88,-.04,.86],[75.5,540,1010,1.1,-.04,.86],
[82.5,540,1010,1.15,0,1],[89.5,280,1040,.92,0,1],[96,280,1040,.92,0,1],
[103.5,280,1040,.92,0,1],[110,280,1040,.92,0,1],[117.5,540,1040,1.1,-.09,.76],
[124.5,540,1110,.75,0,1],[132,540,1110,.75,0,1],[139.5,540,1070,1,0,1],[146,540,1070,1,0,1],[146.5,540,1120,1,0,1],[150,540,1120,1,0,1]];
function pose(t:number):Pose{let i=0;while(i<keys.length-2&&t>keys[i+1][0])i++;const a=keys[i],b=keys[i+1],u=q(t,Math.max(a[0],b[0]-.5),b[0]),cam=editorialCamera(t,[{t:Math.max(a[0],b[0]-.5),x:a[1],y:a[2],z:a[3]},{t:b[0],x:b[1],y:b[2],z:b[3]}]);return{x:cam.x,y:cam.y,s:cam.z,a:mix(a[4],b[4],u),tilt:mix(a[5],b[5],u)}}
function pt(p:Pose,x:number,y:number):V{return[p.x+p.s*(Math.cos(p.a)*x-Math.sin(p.a)*y*p.tilt),p.y+p.s*(Math.sin(p.a)*x+Math.cos(p.a)*y*p.tilt)]}
function normal(p:Pose,side:'bottom'|'right'):V{return side==='bottom'?[-Math.sin(p.a),Math.cos(p.a)]:[Math.cos(p.a),Math.sin(p.a)]}
function edge(p:Pose,side:'bottom'|'right',gap=18):V{let a=pt(p,side==='right'?148:0,side==='bottom'?190:0),n=normal(p,side);return[a[0]+n[0]*gap,a[1]+n[1]*gap]}
function alpha(c:C,a:number,fn:()=>void){if(a<=0)return;c.save();c.globalAlpha*=a;fn();c.restore()}
function paper(c:C,p:Pose,t:number,showItem:boolean){
 const close=q(t,146,146.5),w=mix(296,590,close),h=mix(380,100,close),r=mix(15,50,close);
 c.save();c.translate(p.x,p.y);c.rotate(p.a);c.scale(p.s,p.s*p.tilt);
 rr(c,-w/2,-h/2+12,w,h,r,'#9a9481');rr(c,-w/2,-h/2,w,h,r,S.paper);c.beginPath();c.roundRect(-w/2,-h/2,w,h,r);c.clip();
 alpha(c,1-close,()=>{line(c,[[-103,-137],[55,-137]],'#556961',10);line(c,[[-103,-109],[99,-109]],'#c2c5b5',5);for(let i=0;i<3;i++){let y=-40+i*65;rr(c,-105,y-14,26,26,5,'#e2e1d2','#a0ac9e');line(c,[[-58,y],[90-i*15,y]],'#b2bdac',7)}
 if(showItem){rr(c,-111,-67,224,56,10,S.gold);rr(c,-94,-51,24,24,5,t>=92?S.dark:'#eedbad',S.dark);line(c,[[-52,-39],[86,-39]],S.dark,7)} });
 alpha(c,close,()=>{line(c,[[-235,0],[185,0]],S.dark,7);dot(c,237,0,9,S.dark)});c.restore();
}
function chat(c:C,x:number,y:number,s=1,amount=1){c.save();c.translate(x,y);c.scale(s,s);rr(c,-145,-100,290,200,34,S.teal);c.beginPath();c.moveTo(-100,90);c.lineTo(-108,137);c.lineTo(-43,94);c.fillStyle=S.teal;c.fill();for(let i=0;i<3;i++)line(c,[[-97,-47+i*43],[-97+(i===2?136:190)*clamp(amount*3-i),-47+i*43]],S.bg,8);c.restore()}
const counts=['约60亿人','约10—20亿人','约2000万人','约5000人'];
const short=['几乎未接触','偶尔使用','专业使用前沿大模型','内部前沿系统'];
const at=[20,33,46,61],park=[27,40,54,68],rows=[790,1000,1210,1420];
function groups(c:C,t:number){if(t<12||t>=75.5)return;const leave=1-q(t,75,75.5);alpha(c,leave,()=>{
 // Equal editorial stations: not a proportional funnel or nested populations.
 for(let i=0;i<4;i++){let established=q(t,at[i],at[i]+.5),st=q(t,12+i*.7,13+i*.7);alpha(c,.5*st,()=>{line(c,[[66,rows[i]+10],[66,rows[i]+123]],S.edge,3);line(c,[[66,rows[i]+123],[100,rows[i]+123]],S.edge,3)});
 if(t<at[i])continue;const dock=q(t,park[i],park[i]+.5);let x=mix(90,96,dock),y=mix(326,rows[i],dock),size=mix(112,46,dock);alpha(c,established,()=>text(c,counts[i],x,y,size,dock>.95?S.ink:S.gold,800));
 alpha(c,dock,()=>{const ss=short[i];if(i===2){text(c,'专业使用',96,rows[i]+68,44,S.dim);text(c,'前沿大模型',96,rows[i]+119,44,S.dim)}else text(c,ss,96,rows[i]+69,44,S.dim)});
 }
 });}
function capPose(t:number,i:number):V{
 let base:[number,number]=[550+i*195,1370];let step:[number,number]=[560+i*190,910];let u=q(t,89,89.5),v=q(t,103,103.5),w=q(t,117,117.5),ac=q(t,124,124.5),end=q(t,139,139.5);
 let leaveGroup=q(t,75,75.5);base=[mix(base[0],310+i*230,leaveGroup),mix(base[1],1530,leaveGroup)];let x=mix(base[0],step[0],u),y=mix(base[1],step[1],u);
 // Save retains identity while add/complete retreat into the already-explained graph.
 x=mix(x,[540,720,540][i],i===2?q(t,103.3,103.5):v);y=mix(y,[1400,1400,1510][i],i===2?q(t,103,103.3):v);
 x=mix(x,330+i*210,w);y=mix(y,1470,w);x=mix(x,808+(i%2)*94,ac);y=mix(y,1030+Math.floor(i/2)*140,ac);
 x=mix(x,310+i*230,end);y=mix(y,1480,end);return[x,y];
}
function caps(c:C,t:number){if(t<54)return;const enter=q(t,54,54.5),leave=1-q(t,146,146.5),ac=q(t,124,124.5)*(1-q(t,139,139.5));let split=roleSplit(t,54,510,106,3);for(let i=0;i<3;i++){const a=capPose(t,i),size=mix(106,64,ac);alpha(c,enter*leave*(i<2?(1-q(t,103,103.3)+q(t,117,117.5)):1),()=>{const x=mix(745-255+i*(split.segW+split.gap)+split.segW/2,a[0],q(t,54.6,55.1)),width=mix(split.segW,size,q(t,54.6,55.1));rr(c,x-width/2,a[1]-size/2,width,size,mix(split.innerR,20,q(t,55,55.5)),i===2?'#35564c':S.dark,S.edge);icon(c,i,x,a[1],size*.5,i===2?S.gold:S.ink)})}}
function mainCopy(c:C,t:number){const s=content.scenes.find(s=>t>=s.start_sec&&t<s.end_sec)||content.scenes[21];let a=q(t,s.start_sec,s.start_sec+.5)*(s.id==='closing'?1:1-q(t,s.end_sec-.2,s.end_sec));
 if(t>=124&&t<132)return;let firstCount=s.screen_lines[0].startsWith('约');let lines=firstCount?s.screen_lines.slice(1):s.screen_lines;
 let y=firstCount?500:t<12?1290:t>=146?680:t>=82&&t<89?440:t>=89&&t<103?370:t>=117&&t<124?470:340;
 alpha(c,a,()=>{for(let i=0;i<lines.length;i++){let sz=t<6||t>=146?80:lines[i].length>=13?64:72;text(c,lines[i],90,y,sz,i===0?S.ink:S.dim);y+=sz*1.48}});
}
function accessGeometry(t:number){const u=q(t,124,124.5),exit=q(t,139,139.5);const windows=[{x:82,w:284},{x:398,w:284},{x:714,w:284}].map(v=>({...v,y:860,h:500}));return{u,exit,windows,busY:1540}}
function drawScene(c:C,t:number){const p=pose(t),bottom=edge(p,'bottom'),right=edge(p,'right');
 // Connecting geometry precedes opaque carriers. All endpoints derive from the live contour.
 if(t<12.5){alpha(c,1-q(t,12,12.5),()=>{const root:V=[540,540];line(c,[[470,540],[610,540]],S.gold,12);curve(c,root,[285,740],q(t,.6,1.4));curve(c,root,[745,670],q(t,1,1.8));chat(c,285,860,.95,q(t,1.5,2.5))})}
 if(t>=12&&t<33.5)alpha(c,q(t,12,12.5)*(1-q(t,33,33.5)),()=>{let y=720;for(let i=0;i<3;i++){let u=q(t,20+i*.45,21+i*.45);line(c,[[610,y-i*35],[610+270*u,y-i*35]],i===0?S.teal:S.edge,3)}curve(c,[760,750],[760,p.y-220],1,S.edge,3,true);line(c,[[690,p.y-210],[830,p.y-210]],S.gold,5)});
 if(t>=33&&t<46.5)alpha(c,q(t,33,33.5)*(1-q(t,46,46.5)),()=>{chat(c,730,790,.68,q(t,34,35));curve(c,[730,895],pt(p,0,-198),q(t,35,36));if(t>=40){icon(c,3,595,1420,52,S.teal);line(c,[[680,1420],[893,1420]],S.edge,4);token(c,travel([680,1420],[893,1420],q(t,41,44)),40,14)}});
 if(t>=54&&t<89.5){alpha(c,q(t,54,54.5)*(1-q(t,89,89.5)),()=>{for(let i=0;i<3;i++){const d=capPose(t,i),end:V=[d[0],d[1]-61];curve(c,bottom,end,q(t,54.5+i*.2,55.3+i*.2),S.edge,3);let u=q(t,55.5+i*.5,56.3+i*.5);if(u>0&&u<1)token(c,travel(bottom,end,u));}
 if(t>=68&&t<75.5){alpha(c,1-q(t,75,75.5),()=>{for(let i=0;i<3;i++){const a=capPose(t,i),b:V=[a[0],1575];curve(c,[a[0],a[1]+61],[b[0],b[1]-35],q(t,68+i*.2,68.8+i*.2),S.teal);alpha(c,q(t,68.4+i*.2,69+i*.2),()=>{rr(c,b[0]-45,b[1]-28,90,56,14,S.dark,S.edge);dot(c,b[0]-12,b[1],5,S.gold);dot(c,b[0]+12,b[1],5,S.teal)});let u=q(t,71+i*.5,72+i*.5);if(u>0&&u<1)token(c,travel([a[0],a[1]-61],bottom,u),28,13,S.teal)}}) }})}
 // The internal access outline is one boundary, expands into the workspace at 124.
 if(t>=61&&t<82.5){alpha(c,q(t,61,61.5)*(1-q(t,82,82.5)),()=>{const ex=q(t,75,75.5);let x=mix(480,230,ex),w=mix(540,620,ex);line(c,[[x,1190],[x,790],[x+w,790],[x+w,1190]],S.teal,3)})}
 if(t>=82&&t<89.5)alpha(c,q(t,82,82.5)*(1-q(t,89,89.5)),()=>{for(let i=0;i<4;i++)line(c,[[370,1320+i*32],[370+(350-i*25)*q(t,83+i*.35,84+i*.35),1320+i*32]],i===0?S.gold:S.edge,6)});
 // Same three functional carriers, same item token: add -> complete -> persist -> reopen.
 if(t>=89&&t<103.5){alpha(c,q(t,89,89.5)*(1-q(t,103,103.5)),()=>{for(let i=0;i<2;i++){let a=capPose(t,i),b=capPose(t,i+1);curve(c,[a[0]+61,a[1]],[b[0]-61,b[1]],q(t,90+i*.6,90.6+i*.6),S.edge,4)}
 let a=capPose(t,2);curve(c,[a[0],a[1]+61],[760,1215],q(t,93,94),S.teal,4);curve(c,right,[480,1040],q(t,89.5,90.5),S.edge,3,true);

 if(t>=96){line(c,[[616,1475],[905,1475]],S.gold,4);dot(c,760,1475,7,S.gold)}})}
 if(t>=103&&t<117.5){alpha(c,q(t,103,103.5)*(1-q(t,117,117.5)),()=>{curve(c,right,[607,1040],q(t,104,105),S.edge,3,true);let save=capPose(t,2);curve(c,bottom,[save[0]-55,save[1]-61],q(t,105,106));if(t>=110){curve(c,[760,1248],[save[0]+55,save[1]-61],q(t,110.5,111.5),S.gold,3,true);let u=q(t,111.5,112.5);if(u>0&&u<1)token(c,travel([760,1248],[save[0]+55,save[1]-61],u),35,16);curve(c,[save[0]+68,save[1]],[930,1040],q(t,113,114),S.teal,3,true)}})}
 if(t>=117&&t<124.5)alpha(c,q(t,117,117.5)*(1-q(t,124,124.5)),()=>{for(let i=0;i<3;i++){let a=capPose(t,i);curve(c,bottom,[a[0],a[1]-61],1);line(c,[[a[0]-26,1620],[a[0]+26,1620]],S.teal,4);line(c,[[a[0]-26,1635],[a[0]+26,1635]],S.teal,4)} });
 // Access scopes reveal different regions of ONE continuous workspace, not three duplicate plugs.
 if(t>=124&&t<139.5){const g=accessGeometry(t);alpha(c,g.u*(1-g.exit),()=>{
 
 g.windows.forEach((w,i)=>{rr(c,w.x,w.y,w.w,w.h,24,S.dark,S.edge);const a:V=[w.x+w.w/2,w.y+w.h+8];curve(c,a,[a[0],g.busY],q(t,126+i*.3,127+i*.3),S.teal,3);dot(c,a[0],g.busY,6,S.teal)});
 line(c,[[224,g.busY],[856,g.busY]],S.teal,3);line(c,[[540,g.busY+8],[540,1640]],S.gold,3);rr(c,450,1648,180,66,33,S.gold);line(c,[[487,1681],[593,1681]],S.dark,5);
 // Labels are the frozen copy; retained after reading so each aperture keeps its access identity.
 text(c,'免费版',103,740,60,S.ink);text(c,'付费版',420,740,60,S.ink);text(c,'内部系统',720,740,60,S.ink);text(c,'·',370,740,60,S.dim);
 });}
 if(t>=139){alpha(c,q(t,139,139.5)*(1-q(t,146,146.5)),()=>{for(let i=0;i<3;i++){let d=capPose(t,i);curve(c,bottom,[d[0],d[1]-61],1,S.edge,3);let u=q(t,141+i*.8,142+i*.8);if(u>0&&u<1)token(c,travel([d[0],d[1]-61],bottom,u),32,15,S.teal)}})}
 // Draw the paper once. Access clip is attached to its own shared workspace cell.
 const ac=t>=124&&t<139.5?accessGeometry(t):null;
 c.save();if(ac&&ac.u>.999&&ac.exit===0){c.beginPath();c.roundRect(398,860,284,500,24);c.clip()}
 const movingItem=t>=90&&t<103.5;paper(c,p,t,t>=46&&!movingItem);c.restore();
 if(t>=124&&t<139.5)alpha(c,ac!.u*(1-ac!.exit),()=>{c.save();c.beginPath();c.roundRect(82,860,284,500,24);c.clip();chat(c,224,1050,.68,1);for(let i=0;i<3;i++)line(c,[[132,1210+i*30],[300-i*18,1210+i*30]],S.dim,5);c.restore();c.save();c.beginPath();c.roundRect(714,860,284,500,24);c.clip();curve(c,[840,960],[808,994],1,S.teal);curve(c,[840,960],[902,994],1,S.teal);curve(c,[808,1070],[808,1130],1,S.teal);dot(c,840,960,8,S.gold);line(c,[[790,1270],[924,1270]],S.teal,3);c.restore()});

 if(t>=93&&t<117.5){alpha(c,q(t,93,93.5)*(1-q(t,117,117.5)),()=>{const u=q(t,103,103.5),v=pillWindow(t,93,70,40,260,200),ww=mix(v.w,290,u),hh=mix(v.h,390,u),cy=mix(1320,1045,u);rr(c,760-ww/2,cy-hh/2,ww,hh,mix(v.r,25,u),S.dark,S.edge);icon(c,3,760,mix(1320,1155,u),58,S.teal);alpha(c,u,()=>line(c,[[651,1005],[865,1005],[865,1060],[651,1060],[651,1005]],S.teal,3,[8,10]))})}
 caps(c,t);
 if(t>=90&&t<103.5){let pos:V=pt(p,1,-39);if(t<91)pos=travel(pt(p,1,-39),capPose(t,0),q(t,90,91));else if(t<92)pos=travel(capPose(t,0),capPose(t,1),q(t,91,92));else if(t<93)pos=travel(capPose(t,1),capPose(t,2),q(t,92,93));else if(t<94.5)pos=travel(capPose(t,2),[760,1270],q(t,93,94.5));else if(t<103)pos=[760,1270];else pos=travel([760,1270],pt(p,1,-39),q(t,103,103.5));const take=q(t,90,91),back=q(t,103,103.5),ww=mix(mix(224*p.s,100,take),224*p.s,back),hh=mix(mix(56*p.s*p.tilt,26,take),56*p.s*p.tilt,back);c.save();c.translate(...pos);c.rotate(p.a*(1-take+back));c.scale(ww/224,hh/56);rr(c,-112,-28,224,56,10,S.gold);rr(c,-95,-12,24,24,5,t>=92?S.dark:'#eedbad',S.dark);line(c,[[-53,0],[85,0]],S.dark,7);c.restore();}

}
export function geometryAt(t:number){let p=pose(t),g=accessGeometry(t);return{time:t,objectIds:['task-paper','task-item','function-add','function-complete','function-save'],paper:p,paperCorners:[pt(p,-148,-190),pt(p,148,-190),pt(p,148,190),pt(p,-148,190)],branchOrigin:edge(p,'bottom'),functionCenters:[0,1,2].map(i=>capPose(t,i)),accessWindows:g.windows,busY:g.busY,wholeSceneCrossfade:false}}
// clock-allow-global: One continuous 150s world; all object transitions have explicit absolute cue origins.
export function drawWorld(c:C,frame:number){const t=frame/60;c.setTransform(1,0,0,1,0,0);c.globalAlpha=1;c.clearRect(0,0,1080,1920);c.fillStyle=S.bg;c.fillRect(0,0,1080,1920);const light=c.createRadialGradient(650,1080,50,650,1080,1100);light.addColorStop(0,'#28372f');light.addColorStop(1,S.bg);c.fillStyle=light;c.fillRect(0,0,1080,1920);c.fillStyle='#ffffff05';for(let i=0;i<300;i++)c.fillRect((i*173+37)%1080,(i*283+79)%1920,1,1);drawScene(c,t);groups(c,t);mainCopy(c,t);if(t>=12)text(c,t<75?'Karpathy 粗估':'Karpathy 观点',90,181,44,S.dim)}
