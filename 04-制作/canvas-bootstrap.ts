import {drawWorld} from './src/World';
const canvas=document.createElement('canvas');canvas.width=1080;canvas.height=1920;document.body.appendChild(canvas);
const ctx=canvas.getContext('2d')!;
(window as any).ready=Promise.all([['Fred MiSans','MiSans-Medium.otf','500'],['Fred MiSans Heavy','MiSans-Heavy.otf','800'],['Fred RuiZi','RuiZi.ttf','400']].map(async([family,file,weight])=>{const f=new FontFace(family,`url(/fonts/${file})`,{weight});await f.load();document.fonts.add(f)}));
(window as any).renderPng=(frame:number,format="png")=>{drawWorld(ctx,frame);return canvas.toDataURL(format==="png"?"image/png":"image/jpeg",.98).split(',')[1]};
