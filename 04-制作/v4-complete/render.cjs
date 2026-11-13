const {bundle}=require('@remotion/bundler');
const {selectComposition,renderStill,renderMedia}=require('@remotion/renderer');
const fs=require('fs'),path=require('path'),P=__dirname;
process.env.TMPDIR=path.join(P,'tmp');
(async()=>{
 const serveUrl=await bundle({entryPoint:path.join(P,'src/index.tsx'),outDir:path.join(P,'tmp/bundle-'+Date.now()),publicDir:path.join(P,'public')});
 const browserExecutable='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
 const composition=await selectComposition({serveUrl,id:'Episode',browserExecutable});
 const mode=process.argv[2]||'full',tag=process.argv[3]||'r1';
 if(mode==='stills'){
  const frames=JSON.parse(fs.readFileSync(path.join(P,'planning/keyframes.json')));
  const dir=path.join(P,'qc','stills-'+tag);fs.mkdirSync(dir,{recursive:true});
  for(const frame of frames){
   await renderStill({composition,serveUrl,frame,output:path.join(dir,`F${frame}.png`),browserExecutable});
   console.log('F'+frame);
  }
 }else{
  const ranges=mode==='patch'?[[1380,1457],[2100,2177],[8445,8477]]:mode==='previews'?[[9,80],[4254,4367],[5418,5501],[5700,5850],[6420,6509],[6760,6850],[7638,7739],[8420,8489],[8770,8850]]:[null];
  for(const range of ranges){
   const filename=range?`preview-${tag}-${range[0]}-${range[1]}.mp4`:`ai-funnel-v4-complete-150s-${tag}.mp4`;
   const outputLocation=path.join(P,'output',filename);
   if(fs.existsSync(outputLocation))throw Error('Refuse overwrite '+outputLocation);
   let last=-1;
   await renderMedia({composition,serveUrl,codec:'h264',outputLocation,browserExecutable,concurrency:4,crf:16,muted:true,...(range?{frameRange:range}:{}),onProgress:({progress})=>{const n=Math.floor(progress*10)*10;if(n!==last){last=n;console.log(filename,n+'%')}}});
  }
 }
})().catch(e=>{console.error(e);process.exit(1)});
