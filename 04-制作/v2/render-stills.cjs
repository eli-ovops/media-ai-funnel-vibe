// Source renderer for this task's own deterministic Canvas. No remote/private media and no media playback.
const fs=require('node:fs');const path=require('node:path');const http=require('node:http');const {spawn}=require('node:child_process');const {once}=require('node:events');
const {openBrowser}=require('@remotion/renderer');const esbuild=require('esbuild');const crypto=require('node:crypto');
const P=__dirname;process.env.TMPDIR=path.join(P,'tmp');
(async()=>{const mode=process.argv[2]||'preflight';const start=mode==='full'?0:Number(process.argv[3]||54)*60;const end=mode==='full'?9000:Number(process.argv[4]||61)*60;
 await esbuild.build({entryPoints:[path.join(P,'canvas-bootstrap.ts')],bundle:true,platform:'browser',format:'iife',outfile:path.join(P,'tmp/canvas-render.js')});
 const server=http.createServer((req,res)=>{if(req.url==='/'){res.setHeader('Content-Type','text/html');res.end('<!doctype html><body style="margin:0"><script src="/render.js"></script>');return}
 const file=req.url==='/render.js'?path.join(P,'tmp/canvas-render.js'):/^\/fonts\/[A-Za-z0-9-]+\.(otf|ttf)$/.test(req.url)?path.join(P,'public',req.url):null;
 if(!file||!fs.existsSync(file)){res.statusCode=404;res.end();return}res.setHeader('Content-Type',req.url.endsWith('.js')?'text/javascript':'font/otf');fs.createReadStream(file).pipe(res)});
 await new Promise(r=>server.listen(0,'127.0.0.1',r));const port=server.address().port;
 const browser=await openBrowser('chrome',{browserExecutable:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',chromiumOptions:{gl:'swangle'},logLevel:'error'});
 const page=await browser.newPage({context:()=>null,logLevel:'error',indent:false,pageIndex:0,onBrowserLog:null,onLog:null});
 const times=[3.15,12.167,20.5,27.5,36.65,43.15,50.15,54.5,55.5,57.65,64.65,68.5,72,74.983,75.25,78.65,82.167,85.65,89.167,91.5,94.5,99.65,103.167,106.65,114.5,117.167,120.65,124.167,124.5,128,132.5,135.65,138.983,139.167,142.65,146.2,149.983];
 let rendered=0;const t0=Date.now();const evidence=[];
 try{await page.goto({url:`http://127.0.0.1:${port}`,timeout:30000});await page.evaluate(()=>window.ready);
  for(const t of times){const f=Math.round(t*60);const b64=await page.evaluate(frame=>window.renderPng(frame,'png'),f);const file=path.join(P,`qc/still-${t.toFixed(3)}.png`);fs.writeFileSync(file,Buffer.from(b64,'base64'));evidence.push({time:t,frame:f,path:file,geometry:await page.evaluate(t=>window.geometryAt(t),t)});}
 fs.writeFileSync(path.join(P,'qc/still-geometry.json'),JSON.stringify(evidence,null,2));console.log({frames:evidence.length});
 }finally{await browser.close({silent:true});server.close()}
})().catch(e=>{console.error(e);process.exit(1)});
