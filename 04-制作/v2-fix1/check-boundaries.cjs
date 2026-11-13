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
 try{await page.goto({url:`http://127.0.0.1:${port}`,timeout:30000});await page.evaluate(()=>window.ready);const records=await page.evaluate(()=>window.compareBoundaries());fs.writeFileSync(path.join(P,'qc/boundary-source-pixels.json'),JSON.stringify({scope:'Source Canvas pixels with same loaded font; final MP4 reencoding is lossy and not byte-identical',records},null,2));console.log(records);if(records.some(x=>!x.identicalSourcePixels))throw Error('Unexpected outside-range change');}finally{await browser.close({silent:true});server.close()}
})().catch(e=>{console.error(e);process.exit(1)});
