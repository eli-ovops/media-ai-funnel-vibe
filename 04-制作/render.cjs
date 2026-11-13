const path=require('node:path');const fs=require('node:fs');
const {bundle}=require('@remotion/bundler');const {selectComposition,renderMedia,renderStill}=require('@remotion/renderer');
const P=__dirname;process.env.TMPDIR=path.join(P,'tmp');
(async()=>{const mode=process.argv[2]||'preflight';const out=path.join(P,'tmp/bundle');
 const serveUrl=await bundle({entryPoint:path.join(P,'src/index.tsx'),outDir:out,publicDir:path.join(P,'public'),webpackOverride:c=>({...c,cache:false})});
 const options={serveUrl,browserExecutable:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',chromiumOptions:{gl:'swangle'},logLevel:'warn'};
 const composition=await selectComposition({...options,id:'Funnel150'});
 if(mode==='stills'){for(const t of process.argv.slice(3).map(Number)){await renderStill({...options,composition,frame:Math.round(t*60),output:path.join(P,`qc/still-${t}.png`),imageFormat:'png'});console.log('still',t)}return}
 const frameRange=mode==='preflight'?[3240,3659]:mode==='segment'?[Number(process.argv[3])*60,Number(process.argv[4])*60-1]:undefined;
 let last=-1;await renderMedia({...options,composition,codec:'h264',outputLocation:path.join(P,'output',mode==='full'?'visual-v1.mp4':mode==='preflight'?'preflight-54-61s.mp4':`segment-${process.argv[3]}-${process.argv[4]}.mp4`),frameRange,concurrency:1,imageFormat:'png',crf:18,pixelFormat:'yuv420p',onProgress:({progress})=>{const n=Math.floor(progress*20);if(n!==last){last=n;console.log(`${mode} ${n*5}%`)}}});
})().catch(e=>{console.error(e);process.exit(1)});
