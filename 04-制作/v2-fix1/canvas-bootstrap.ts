import {drawWorld,geometryAt} from './src/World';
const canvas=document.createElement('canvas');canvas.width=1080;canvas.height=1920;document.body.appendChild(canvas);
const ctx=canvas.getContext('2d')!;
(window as any).ready=Promise.all([['Fred MiSans','MiSans-Medium.otf','500'],['Fred MiSans Heavy','MiSans-Heavy.otf','800'],['Fred RuiZi','RuiZi.ttf','400']].map(async([family,file,weight])=>{const f=new FontFace(family,`url(/fonts/${file})`,{weight});await f.load();document.fonts.add(f)}));
(window as any).renderPng=(frame:number,format="png")=>{drawWorld(ctx,frame);return canvas.toDataURL(format==="png"?"image/png":"image/jpeg",.98).split(',')[1]};

(window as any).geometryAt=geometryAt;
(window as any).inspectCopy=()=>{
 const cues=require('./content-package.json').scenes,rows:any[]=[];
 const original=ctx.fillText.bind(ctx);
 for(const s of cues){for(const t of [s.reading_start_sec+.001,s.reading_end_sec-.001]){
  const texts:any[]=[];(ctx as any).fillText=(str:string,x:number,y:number)=>{const m=ctx.measureText(str);texts.push({text:str,x,y,width:m.width,font:ctx.font,right:x+m.width,bottom:y+m.actualBoundingBoxDescent});original(str,x,y)};
  drawWorld(ctx,Math.round(t*60));rows.push({cue:s.id,time:t,texts});
 }}(ctx as any).fillText=original;
 const outOfBounds=rows.flatMap(r=>r.texts.filter((x:any)=>x.x<60||x.right>1020||x.y<100||x.bottom>1830).map((x:any)=>({cue:r.cue,...x})));
 return{scope:'Actual loaded font metrics at both ends of each frozen reading window; not pixel or continuous audiovisual acceptance',rows,outOfBounds};
};
(window as any).inspectFix=()=>{
 const counts=['约60亿人','约10—20亿人','约2000万人','约5000人'];const ranges=[[2400,2430],[3240,3270],[4080,4110],[7020,7050]];const frames:any[]=[],failures:any[]=[];
 const original=ctx.fillText.bind(ctx),inter=(a:any,b:any)=>Math.min(a.r,b.r)>Math.max(a.l,b.l)&&Math.min(a.b,b.b)>Math.max(a.t,b.t);
 for(let k=0;k<4;k++)for(let frame=ranges[k][0];frame<ranges[k][1];frame++){
  const texts:any[]=[];(ctx as any).fillText=(str:string,x:number,y:number)=>{const m=ctx.measureText(str);texts.push({str,x,y,font:ctx.font,l:x-m.actualBoundingBoxLeft,r:x+m.actualBoundingBoxRight,t:y-m.actualBoundingBoxAscent,b:y+m.actualBoundingBoxDescent});original(str,x,y)};
  drawWorld(ctx,frame);const g=geometryAt(frame/60);const row:any={frame,time:frame/60};
  if(k<3){const active=texts.find(x=>x.str===counts[k+1]);const obstacles=texts.filter(x=>x!==active&&x.y>=700);const collided=obstacles.filter(x=>inter(active,x));const xs=g.paperCorners.map((v:any)=>v[0]),ys=g.paperCorners.map((v:any)=>v[1]);const paper={l:Math.min(...xs)-2,r:Math.max(...xs)+2,t:Math.min(...ys)-2,b:Math.max(...ys)+14};
   row.active=active;row.stationaryTextBounds=obstacles;row.paperBounds=paper;row.textCollisions=collided;row.paperCollision=inter(active,paper);row.viewportInside=active.l>=0&&active.r<=1080&&active.t>=0&&active.b<=1920;
   if(collided.length||row.paperCollision||!row.viewportInside)failures.push(row);
  }else{row.centers=g.functionCenters;row.gaps=[];for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){const a=g.functionCenters[i],b=g.functionCenters[j],gap=Math.max(Math.abs(a[0]-b[0])-108,Math.abs(a[1]-b[1])-108);row.gaps.push({i,j,gap});if(gap<0)failures.push({frame,i,j,gap})}row.saveBottomToEqualityTop=1618-(g.functionCenters[2][1]+54);if(row.saveBottomToEqualityTop<0)failures.push({frame,equalityOverlap:true})}
  frames.push(row);
 }(ctx as any).fillText=original;
 return{framesChecked:frames.length,failures,frames,scope:'Actual loaded-font glyph bounding boxes and live106px carrier contours plusstroke; computational per-frame avoidance, not continuous perception'};
};
import {drawWorld as baselineWorld} from '../v2/src/World';
(window as any).compareBoundaries=()=>{
 const fs=[2399,2400,2430,2431,3239,3240,3270,3271,4079,4080,4110,4111,7019,7020,7050,7051,1620,1635,1650];
 return fs.map(frame=>{baselineWorld(ctx,frame);const old=canvas.toDataURL();drawWorld(ctx,frame);return{frame,identicalSourcePixels:old===canvas.toDataURL()}});
};
