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
