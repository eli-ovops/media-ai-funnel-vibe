import {S,clamp,mix,q,p,springAt,syncPoint,roleSplit,pillWindow,editorialCamera,camMat,project} from './kit';
import content from '../content-package.json';
type C=CanvasRenderingContext2D;
const TAU=Math.PI*2;
function rr(c:C,x:number,y:number,w:number,h:number,r=24,fill=S.dark,stroke?:string){c.beginPath();c.roundRect(x,y,w,h,r);c.fillStyle=fill;c.fill();if(stroke){c.lineWidth=2;c.strokeStyle=stroke;c.stroke()}}
function line(c:C,pts:number[][],color=S.edge,width=3,dash:number[]=[]){if(pts.length<2)return;c.beginPath();c.moveTo(...pts[0] as [number,number]);pts.slice(1).forEach(a=>c.lineTo(...a as [number,number]));c.strokeStyle=color;c.lineWidth=width;c.lineCap='round';c.lineJoin='round';c.setLineDash(dash);c.stroke();c.setLineDash([])}
function dot(c:C,x:number,y:number,r=9,color=S.gold){c.beginPath();c.arc(x,y,r,0,TAU);c.fillStyle=color;c.fill()}
function path(c:C,a:number[],b:number[],progress=1,color=S.edge,width=3,dashed=false){if(progress<=0)return;line(c,Array.from({length:49},(_,i)=>{const z=syncPoint(a[0],a[1],b[0],b[1],i/48*progress);return[z.x,z.y]}),color,width,dashed?[10,12]:[])}
function carrier(c:C,a:number[],b:number[],u:number,color=S.gold){if(u<=0||u>=1)return;const z=syncPoint(a[0],a[1],b[0],b[1],u);c.save();c.shadowColor='#000';c.shadowBlur=18;rr(c,z.x-25,z.y-13,50,26,13,color);c.restore()}
function icon(c:C,kind:string,x:number,y:number,size=70,color=S.ink){c.save();c.translate(x,y);c.scale(size/70,size/70);c.strokeStyle=color;c.fillStyle=color;c.lineWidth=5;c.lineCap='round';c.lineJoin='round';c.beginPath();
 if(kind==='plus'){c.moveTo(-19,0);c.lineTo(19,0);c.moveTo(0,-19);c.lineTo(0,19);c.stroke()}
 if(kind==='complete'){c.roundRect(-23,-23,46,46,7);c.stroke();c.fillRect(-11,-11,22,22)}
 if(kind==='save'){c.roundRect(-26,-27,52,54,7);c.stroke();c.moveTo(-14,-27);c.lineTo(-14,-4);c.lineTo(14,-4);c.lineTo(14,-27);c.stroke();c.fillRect(-12,10,24,4)}
 if(kind==='reload'){c.arc(0,0,24,-.4,5.1);c.stroke();line(c,[[10,-29],[17,-19],[28,-25]],color,5)}
 if(kind==='port'){c.roundRect(-26,-18,52,36,18);c.stroke();c.moveTo(0,-18);c.lineTo(0,18);c.stroke()}
 if(kind==='query'){c.arc(-5,-5,18,0,TAU);c.stroke();line(c,[[9,9],[25,25]],color,5)}
 if(kind==='write'){line(c,[[-23,22],[17,-19],[25,-11],[-15,30],[-23,30],[-23,22]],color,5)}
 c.restore()}
function plug(c:C,x:number,y:number,connected:number){rr(c,x-93,y-38,186,76,38,S.dark,S.edge);rr(c,x-70+connected*35,y-15,52,30,15,S.gold);rr(c,x+18,y-15,52,30,15,S.teal);line(c,[[x-7+connected*16,y],[x+18,y]],S.ink,4)}
function paper(c:C,x:number,y:number,scale=1,angle=-.08,item=1,filled=0){c.save();c.translate(x,y);c.rotate(angle);c.scale(scale,scale);c.shadowColor='#0009';c.shadowBlur=35;c.shadowOffsetY=24;
 rr(c,-148,-190,296,380,13,'#a69e87');c.shadowBlur=0;c.shadowOffsetY=0;rr(c,-148,-198,296,380,13,S.paper);
 line(c,[[-102,-137],[48,-137]],'#566864',10);line(c,[[-102,-109],[96,-109]],'#c7c3b0',5);
 for(let i=0;i<3;i++){const yy=-44+i*65;rr(c,-103,yy-14,26,26,5,'#e1dfd1','#9aa49a');line(c,[[-55,yy],[85-i*20,yy]],'#c4c5b6',7)}
 if(item>0){c.globalAlpha=item;rr(c,-107,-63,220,54,9,S.gold);rr(c,-91,-49,24,24,5,filled>.5?S.dark:'#efdaaa',S.dark);line(c,[[-49,-37],[83,-37]],S.dark,7)}
 c.restore()}
function solidPlane(c:C,cx:number,cy:number,t:number,explode:number,kind='task'){
 const ro=[4.6,5.2,9],M=camMat(ro,[0,0,0]);
 const P=(x:number,y:number,z:number)=>project([x,y,z],ro,M,cx,cy);
 for(let k=2;k>=0;k--){const h=k*.12+(2-k)*explode*.56;const poly=[P(-1.8,h,-1.15),P(1.8,h,-1.15),P(1.8,h,1.15),P(-1.8,h,1.15)];
  const lower=poly.map(a=>[a[0],a[1]+12]);line(c,[...lower,lower[0]],'#1a2522',15);
  c.beginPath();c.moveTo(...poly[0] as [number,number]);poly.slice(1).forEach(a=>c.lineTo(...a as[number,number]));c.closePath();c.fillStyle=[S.paper,'#b8c9be','#627b72'][k];c.fill();
  if(k===0){for(let i=0;i<3;i++){const z=-.65+i*.6;line(c,[P(-1.2,h+.01,z),P(.85,h+.01,z)],i===0?S.gold:'#a9b4a6',10)}
   if(kind==='task')for(let i=0;i<3;i++)dot(c,...P(-1.45,h+.01,-.65+i*.6) as[number,number],5,S.dark)}
 }
}
function chat(c:C,x:number,y:number,scale=1,amount=1){c.save();c.translate(x,y);c.scale(scale,scale);c.shadowColor='#0007';c.shadowBlur=24;rr(c,-155,-105,310,210,40,S.teal);c.shadowBlur=0;c.beginPath();c.moveTo(-100,90);c.lineTo(-108,145);c.lineTo(-44,100);c.fillStyle=S.teal;c.fill();for(let i=0;i<3;i++){const g=clamp(amount*3-i);if(g>0)line(c,[[-105,-50+i*45],[-105+(i===2?140:205)*g,-50+i*45]],S.bg,9)}c.restore()}
function endpoints(c:C,t:number,root:number[],branches:number[][],start:number,reverse=false){branches.forEach((b,i)=>{const k=q(t,start+i*.3,start+.8+i*.3);path(c,root,b,k,S.edge,3);const a=start+1.2+i*.38,u=q(t,a,a+.8);carrier(c,reverse?b:root,reverse?root:b,u,i===1?S.teal:S.gold)})}
function branching(c:C,t:number,base=54){
 const root=[500,1075],ends=[[230,1390],[500,1390],[770,1390]];const v=q(t,base+.5,base+1.4);
 ends.forEach((b,i)=>{path(c,root,b,q(t,base+.5+i*.24,base+1.3+i*.24),S.edge,4);carrier(c,root,b,q(t,base+1.4+i*.45,base+2.1+i*.45))});
 const g=roleSplit(t,base+1,750,106,3);
 for(let i=0;i<3;i++){const x=500-375+i*(g.segW+g.gap);c.save();c.globalAlpha=v;rr(c,x,1350,g.segW,106,[53,g.innerR,g.innerR,53] as any,S.dark,S.edge);icon(c,['plus','complete','save'][i],x+g.segW/2,1403,57,i===2?S.gold:S.ink);c.restore()}
}
function collaboration(c:C,t:number){
 const u=q(t,68,69);const xs=[230,500,770];xs.forEach((x,i)=>{const y=1530+(1-springAt(t,68.6+i*.45,.8))*50;c.save();c.globalAlpha=q(t,68.6+i*.45,69.1+i*.45);rr(c,x-67,y-46,134,92,20,i===1?'#375f5b':'#303f38',S.edge);dot(c,x-18,y,7,S.gold);dot(c,x+18,y,7,S.teal);c.restore();path(c,[x,1456],[x,y-46],u,S.edge,3);carrier(c,[x,y-46],[x,1456],q(t,70+i*.45,70.7+i*.45))});
 if(t>71){path(c,[230,1530],[770,1530],q(t,71,71.7),S.teal,3);carrier(c,[230,1530],[770,1530],q(t,71.7,72.5),S.teal);xs.forEach((x,i)=>carrier(c,[x,1390],[500,1075],q(t,72.3+i*.4,73.4+i*.4)))}
}
function taskWorld(c:C,t:number){
 const cam=editorialCamera(t,[{t:46,x:500,y:1210,z:.84},{t:46.5,x:500,y:1210,z:1},{t:74.8,x:500,y:1210,z:1},{t:75.5,x:500,y:1120,z:.75},{t:81.8,x:500,y:1120,z:.75},{t:82,x:500,y:1120,z:.75}]);
 c.save();c.translate(500,1210);c.scale(cam.z,cam.z);c.translate(-cam.x,-cam.y);
 if(t<54)solidPlane(c,500,1130,t,1-q(t,47,52));else{const k=q(t,54,54.5);solidPlane(c,500,1130,t,0);branching(c,t)}
 if(t>=61){const gate=q(t,61,62);c.save();c.globalAlpha=gate;line(c,[[100,1250],[100,920],[900,920],[900,1250]],'#6d7968',3);line(c,[[116,1250],[116,936],[884,936],[884,1250]],'#35433b',2);plug(c,500,900,q(t,63,64));c.restore()}
 if(t>=68)collaboration(c,t);
 c.restore();
}
function taskSteps(c:C,t:number){const xs=[220,500,780];const y=1070;
 xs.forEach((x,i)=>{const show=q(t,89+i*.55,89.5+i*.55);c.save();c.globalAlpha=show;rr(c,x-77,y-70,154,140,28,i===2?'#36564f':S.dark,S.edge);icon(c,['plus','complete','save'][i],x,y,70,i===2?S.gold:S.ink);c.restore()});
 for(let i=0;i<2;i++)path(c,[xs[i]+77,y],[xs[i+1]-77,y],q(t,90+i*.65,90.6+i*.65),S.edge,4);
 const u=q(t,90.7,91.6);carrier(c,[220,y],[500,y],u);carrier(c,[500,y],[780,y],q(t,92,92.9));
 const win=pillWindow(t,93,90,45,310,244);c.save();c.globalAlpha=q(t,93,93.5);win && (c.fillStyle=S.dark); // one carrier opens below the saving branch
 const k=q(t,93,93.8);c.beginPath();c.roundRect(500-win.w/2,1390-win.h/2,win.w,win.h,win.r);c.fillStyle=S.dark;c.fill();c.strokeStyle=S.edge;c.lineWidth=2;c.stroke();c.restore();
 path(c,[780,1140],[500,1268],q(t,93,94),S.teal,4);carrier(c,[780,1140],[500,1268],q(t,94,94.7),S.teal);if(t>=93.5){c.save();c.globalAlpha=k;icon(c,'reload',500,1390,66,S.teal);c.restore()}
 if(t>=96){const focus=q(t,96,96.6);c.save();c.globalAlpha=focus;line(c,[[712,1174],[712,1215],[573,1215],[573,1242]],S.gold,5);c.restore();carrier(c,[780,1140],[500,1268],q(t,98.6,99.8),S.gold)}
}
function saveCheck(c:C,t:number){
 const k=q(t,103,103.5);c.save();c.globalAlpha=k;paper(c,240,1140,.78,-.06,1);c.restore();
 const box=pillWindow(t,103,90,60,310,356);c.save();c.globalAlpha=k;rr(c,745-box.w/2,1140-box.h/2,box.w,box.h,box.r,S.dark,S.edge);c.setLineDash([8,9]);c.strokeStyle=S.teal;c.lineWidth=3;c.strokeRect(659,1085,174,43);c.setLineDash([]);icon(c,'reload',745,1230,57,S.teal);c.restore();
 path(c,[365,1140],[590,1140],q(t,104,105),S.edge,3,true);carrier(c,[365,1140],[590,1140],q(t,105,106));
 c.save();c.globalAlpha=q(t,104.6,105.1);rr(c,423,1450,154,130,24,'#36564f',S.edge);icon(c,'save',500,1515,65,S.gold);c.restore();
 path(c,[240,1295],[500,1450],q(t,105.7,106.7),S.edge,3);
 if(t>=110){path(c,[745,1318],[500,1450],q(t,110.4,111.5),S.gold,4,true);carrier(c,[745,1318],[500,1450],q(t,111.5,112.6));path(c,[500,1450],[745,1318],q(t,113,114),S.teal,3);carrier(c,[500,1450],[745,1318],q(t,114.2,115.3),S.teal)}
}
function access(c:C,t:number){
 const ks=q(t,124,125);const base=1170;const shift=q(t,132,132.8);
 const windows=[{x:210,y:base+120,z:.8},{x:500,y:base-70,z:1},{x:790,y:base+120,z:.8}];
 windows.forEach((w,i)=>{const a=q(t,124+i*.65,124.7+i*.65);const f=pillWindow(t,124+i*.65,70,40,190,260);c.save();c.globalAlpha=a;c.translate(w.x,w.y);c.transform(1,(i-1)*.12,0,1,0,0);c.shadowColor='#0007';c.shadowBlur=26;c.shadowOffsetY=20;rr(c,-f.w/2,-f.h/2,f.w,f.h,f.r,i===1?'#375851':'#263c36',S.edge);c.shadowBlur=0;c.shadowOffsetY=0;line(c,[[-f.w/2+18,-f.h/2+46],[f.w/2-18,-f.h/2+46]],S.edge,2);plug(c,0,20,shift*(i===2?.25:1));c.restore();path(c,[500,1510],[w.x,w.y+130],q(t,126.5+i*.35,127.4+i*.35),S.edge,3);carrier(c,[500,1510],[w.x,w.y+130],q(t,128+i*.6,128.7+i*.6),S.gold)});
 c.save();c.globalAlpha=ks;rr(c,420,1490,160,82,41,S.gold);line(c,[[461,1531],[539,1531]],S.bg,6);c.restore();
 if(t>=132){const a=q(t,133,134);line(c,[[100,985],[900*a+100*(1-a),985]],S.teal,3);windows.forEach(w=>{path(c,[w.x,985],[w.x,w.y-130],a,S.teal,3);dot(c,w.x,985,6,S.teal)});}
}
function synthesis(c:C,t:number){
 const cam=editorialCamera(t,[{t:139,x:500,y:1190,z:.8},{t:139.6,x:500,y:1190,z:1},{t:145.8,x:500,y:1190,z:1},{t:146.5,x:500,y:1170,z:1.2},{t:150,x:500,y:1170,z:1.2}]);
 c.save();c.translate(500,1190);c.scale(cam.z,cam.z);c.translate(-cam.x,-cam.y);const exit=q(t,145.8,146.5),ends=[[230,1410],[500,1510],[770,1410]];
 c.save();c.globalAlpha=1-exit;ends.forEach((e,i)=>{path(c,[500,1110],e,q(t,139+i*.3,139.8+i*.3),S.edge,3);rr(c,e[0]-60,e[1]-50,120,100,24,S.dark,S.edge);icon(c,['plus','reload','port'][i],e[0],e[1],57,i===1?S.teal:S.gold);carrier(c,e,[500,1110],q(t,141+i*.7,142.2+i*.7))});c.restore();
 const w=mix(300,530,exit),h=mix(180,90,exit);rr(c,500-w/2,1110-h/2,w,h,mix(25,45,exit),S.gold);line(c,[[500-w/2+45,1110],[500+w/2-45,1110]],S.bg,6);dot(c,500+w/2-35,1110,7,S.bg);c.restore();
}
function figures(c:C,t:number){
 if(t<12){const root=[500,920];const pts=[[255,1260],[745,1260]];const enter=q(t,0,.5);c.save();c.globalAlpha=enter;plug(c,...root as[number,number],1);endpoints(c,t,root,pts,1);const a=q(t,1.2,2.5);chat(c,255,1260,.68,a);c.save();c.globalAlpha=a;c.save();c.translate(700,1260);c.scale(.72,.72);solidPlane(c,0,0,t,1-q(t,7,10));c.restore();c.restore();if(t>6){carrier(c,root,pts[0],q(t,6.5,7.5));carrier(c,root,pts[1],q(t,7.5,8.5));path(c,[745,1330],[745,1510],q(t,8.6,9.6),S.edge,3);dot(c,745,1510,8,S.teal)}c.restore();return}
 if(t<20){const k=q(t,12,12.5);c.save();c.globalAlpha=k;const cam=editorialCamera(t,[{t:12,x:500,y:1200,z:.86},{t:13,x:500,y:1200,z:1},{t:19.5,x:500,y:1200,z:1},{t:20,x:350,y:1200,z:1.12}]);c.translate(500,1200);c.scale(cam.z,cam.z);c.translate(-cam.x,-cam.y);plug(c,235,1010,0);chat(c,740,1010,.64);c.save();c.translate(250,1400);c.scale(.65,.65);solidPlane(c,0,0,t,0);c.restore();rr(c,642,1270,196,250,24,S.dark,S.edge);plug(c,740,1400,.7);c.restore();return}
 if(t<33){const conn=0;plug(c,500,1240,conn);const listen=q(t,20.5,24.5);for(let i=0;i<4;i++){c.save();c.globalAlpha=.7;const r=110+i*58;const a=q(t,20.6+i*.6,21.4+i*.6);if(a>0){c.beginPath();c.ellipse(500,1030,r,r*.45,0,Math.PI*1.1,Math.PI*(1.1+.8*a));c.lineWidth=3;c.strokeStyle=i%2?S.teal:S.edge;c.stroke()}c.restore()}
 line(c,[[500,1115],[500,1170]],S.edge,3,[8,12]);if(t>=27){const fade=q(t,27,27.5);c.save();c.globalAlpha=fade;paper(c,500,1530,.48,0,0);line(c,[[500,1305],[500,1395]],S.edge,3,[8,12]);c.restore()}return}
 if(t<46){plug(c,500,945,q(t,33,34));const out=q(t,34.2,35.1);c.save();c.globalAlpha=out;chat(c,mix(500,300,out),mix(945,1215,out),.85,q(t,34.5,36));paper(c,mix(500,750,out),mix(945,1215,out),.65,.08,0);c.restore();endpoints(c,t,[500,990],[[300,1115],[750,1080]],33.8);if(t>=40){icon(c,'query',300,1500,70,S.teal);icon(c,'write',750,1500,70,S.gold);path(c,[300,1350],[300,1450],q(t,40,41));path(c,[750,1340],[750,1450],q(t,41,42));carrier(c,[750,1215],[500,945],q(t,43,44));carrier(c,[300,1215],[500,945],q(t,44,45),S.teal)}return}
 if(t<82){taskWorld(c,t);return}
 if(t<89){paper(c,500,1160,.9,-.03,0);const a=q(t,83,85);for(let i=0;i<4;i++){line(c,[[365,1430+i*28],[365+(270-i*25)*clamp(a*4-i),1430+i*28]],i===0?S.gold:S.edge,5)}return}
 if(t<103){taskSteps(c,t);return}
 if(t<117){saveCheck(c,t);return}
 if(t<124){const k=q(t,117,117.6);c.save();c.globalAlpha=k;solidPlane(c,500,1120,t,q(t,118,121));for(let i=0;i<3;i++){const y=1350+i*75;rr(c,245,y,510,55,12,i===0?S.gold:S.dark);line(c,[[285,y+27],[520,y+27]],i===0?S.bg:S.edge,7);line(c,[[578,y+19],[615,y+19]],S.teal,4);line(c,[[578,y+35],[615,y+35]],S.teal,4)}c.restore();return}
 if(t<139){access(c,t);return}synthesis(c,t);
}
function copy(c:C,t:number){
 const s=content.scenes.find(s=>t>=s.start_sec&&t<s.end_sec)||content.scenes[21];
 const a=q(t,s.start_sec,s.start_sec+.5)*(s.id==='closing'?1:1-q(t,s.end_sec-.2,s.end_sec));
 c.save();c.globalAlpha=a;c.textBaseline='top';c.textAlign='left';
 const count=s.screen_lines[0].startsWith('约');const intro=s.id==='question'||s.id==='closing';
 let y=count?330:intro?350:340;
 for(let i=0;i<s.screen_lines.length;i++){const str=s.screen_lines[i];let size=count&&i===0?112:intro?80:72;
  if(str.length>=13)size=64;const font=count&&i===0?`800 ${size}px "Fred MiSans Heavy"`:`500 ${size}px "${S.body}"`;c.font=font;
  c.fillStyle=count&&i===0?S.gold:i===0?S.ink:S.dim;
  c.fillText(str,90,y);y+=size*(count&&i===0?1.42:1.48);
 }
 c.restore();
 if(t>=12){c.font='500 44px "Fred MiSans"';c.fillStyle=S.dim;c.textAlign='left';c.textBaseline='top';c.fillText(t<75?'Karpathy 粗估':'Karpathy 观点',92,181)}
}
let transitionLayer:HTMLCanvasElement|null=null;
function compositeFigures(c:C,t:number,alpha:number){if(!transitionLayer){transitionLayer=document.createElement("canvas");transitionLayer.width=1080;transitionLayer.height=1920;}const g=transitionLayer.getContext("2d")!;g.setTransform(1,0,0,1,0,0);g.globalAlpha=1;g.clearRect(0,0,1080,1920);figures(g,t);c.save();c.globalAlpha=alpha;c.drawImage(transitionLayer,0,0);c.restore()}
export function drawWorld(c:C,frame:number){
 // clock-allow-global: One continuous scene, with explicit per-object time origins; copy uses frozen cue-local intervals.
 const t=frame/60;c.setTransform(1,0,0,1,0,0);c.globalAlpha=1;c.clearRect(0,0,1080,1920);c.fillStyle=S.bg;c.fillRect(0,0,1080,1920);
 const light=c.createRadialGradient(500,1110,0,500,1110,1000);light.addColorStop(0,'#28352d');light.addColorStop(1,S.bg);c.fillStyle=light;c.fillRect(0,0,1080,1920);
 // Deterministic fixed stipple: texture belongs to the solid background, no moving particles/counts.
 c.fillStyle='#ffffff05';for(let i=0;i<320;i++){const x=(i*173+37)%1080,y=(i*283+79)%1920;c.fillRect(x,y,1.2,1.2)}
 const boundary=[12,20,33,46,82,89,103,117,124,139].find(b=>t>=b&&t<b+.35);
 if(boundary!==undefined){const k=q(t,boundary,boundary+.35);compositeFigures(c,boundary-1/60,1-k);compositeFigures(c,t,k)}else figures(c,t);
 copy(c,t);
}
