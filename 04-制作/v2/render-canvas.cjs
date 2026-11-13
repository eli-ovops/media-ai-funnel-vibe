// Source renderer for this task's own deterministic Canvas. No remote/private media and no media playback.
const fs=require('node:fs');const path=require('node:path');const http=require('node:http');const {spawn}=require('node:child_process');const {once}=require('node:events');
const {openBrowser}=require('@remotion/renderer');const esbuild=require('esbuild');const crypto=require('node:crypto');
const P=__dirname;process.env.TMPDIR=path.join(P,'tmp');
(async()=>{const mode=process.argv[2]||'preflight';const start=mode==='full'?0:Number(process.argv[3]||54)*60;const end=mode==='full'?9000:Number(process.argv[4]||61)*60;
 const sourceSha256=crypto.createHash('sha256').update(fs.readFileSync(path.join(P,'src/World.ts'))).digest('hex');
 await esbuild.build({entryPoints:[path.join(P,'canvas-bootstrap.ts')],bundle:true,platform:'browser',format:'iife',outfile:path.join(P,'tmp/canvas-render.js')});
 const server=http.createServer((req,res)=>{if(req.url==='/'){res.setHeader('Content-Type','text/html');res.end('<!doctype html><body style="margin:0"><script src="/render.js"></script>');return}
 const file=req.url==='/render.js'?path.join(P,'tmp/canvas-render.js'):/^\/fonts\/[A-Za-z0-9-]+\.(otf|ttf)$/.test(req.url)?path.join(P,'public',req.url):null;
 if(!file||!fs.existsSync(file)){res.statusCode=404;res.end();return}res.setHeader('Content-Type',req.url.endsWith('.js')?'text/javascript':'font/otf');fs.createReadStream(file).pipe(res)});
 await new Promise(r=>server.listen(0,'127.0.0.1',r));const port=server.address().port;
 const browser=await openBrowser('chrome',{browserExecutable:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',chromiumOptions:{gl:'swangle'},logLevel:'error'});
 const page=await browser.newPage({context:()=>null,logLevel:'error',indent:false,pageIndex:0,onBrowserLog:null,onLog:null});
 const logPath=path.join(P,`qc/canvas-${mode}-encode.txt`);const out=fs.openSync(logPath,'w');
 const ff=spawn('/Users/USER/.local/bin/ffmpeg',['-nostdin','-hide_banner','-y','-f','image2pipe','-framerate','60','-i','pipe:0','-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',path.join(P,'output',`canvas-${mode}-visual.mp4`)],{stdio:['pipe','ignore',out]});
 let rendered=0;const t0=Date.now();const evidence=[];
 try{await page.goto({url:`http://127.0.0.1:${port}`,timeout:30000});await page.evaluate(()=>window.ready);if(mode==='full'){const metrics=await page.evaluate(()=>window.inspectCopy());fs.writeFileSync(path.join(P,'qc/copy-metrics.json'),JSON.stringify(metrics,null,2));if(metrics.outOfBounds.length)throw Error('copy bounds failures '+metrics.outOfBounds.length);}
  for(let f=start;f<end;f++){const b64=await page.evaluate((frame,format)=>window.renderPng(frame,format),f,mode==='preflight'?'png':'jpeg');const b=Buffer.from(b64,'base64');if(!ff.stdin.write(b))await once(ff.stdin,'drain');rendered++;
   if(mode!=='full'&&(f===start||f===Math.floor((start+end)/2)||f===end-1)){const file=path.join(P,`qc/canvas-${mode}-proof-${f}.${mode==='preflight'?'png':'jpg'}`);fs.writeFileSync(file,b);evidence.push({frame:f,path:file,sha256:crypto.createHash('sha256').update(b).digest('hex')})}
   if((f-start)%300===0)console.log(JSON.stringify({frame:f,progress:rendered/(end-start),fps:rendered/((Date.now()-t0)/1000)}));
  }ff.stdin.end();const [code]=await once(ff,'exit');if(code!==0)throw Error('ffmpeg exit '+code);
  fs.writeFileSync(path.join(P,`qc/canvas-${mode}-receipt.json`),JSON.stringify({startFrame:start,endFrameExclusive:end,renderedFrames:rendered,durationSeconds:(end-start)/60,width:1080,height:1920,fps:60,wallSeconds:(Date.now()-t0)/1000,frames:evidence,sourceSha256},null,2));
 }finally{await browser.close({silent:true});server.close();fs.closeSync(out)}
})().catch(e=>{console.error(e);process.exit(1)});
