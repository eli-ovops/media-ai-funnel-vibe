from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,math
P=Path(__file__).resolve().parent;Q=P/'qc';A=P.with_name('v4');rows=json.loads((Q/'export-frame-index.json').read_text());old=json.loads((A/'qc/export-frame-index.json').read_text());font=ImageFont.truetype('/System/Library/Fonts/SFNS.ttf',18)
canvas=Image.new('RGB',(1140,math.ceil(len(rows)/6)*355),'#ddd');d=ImageDraw.Draw(canvas)
for i,r in enumerate(rows):
 im=Image.open(r['path']).convert('RGB');im.thumbnail((180,320));x=10+(i%6)*190;y=(i//6)*355;canvas.paste(im,(x,y+25));d.text((x,y+2),f"F{r['frame']} {r['time_sec']:.2f}s",fill='black',font=font)
canvas.save(Q/'export-timeline.jpg',quality=92)
lookup={r['frame']:r['path']for r in rows};older={r['frame']:r['path']for r in old}
canvas=Image.new('RGB',(1080,3*690),'#e5e5e5');d=ImageDraw.Draw(canvas)
for i,(name,t,frame) in enumerate([('T15f',4.05,285),('T05h',4.63,2028),('T20m',1.5,1520)]):
 y=i*690;d.text((24,y+12),f'{name} source {t}s | fix1 F{frame} {frame/60:.2f}s',fill='black',font=font)
 im=Image.open(A/f'qc/source-stages/{name}-{t}.png').convert('RGB');im.thumbnail((680,580));canvas.paste(im,(20,y+150))
 im=Image.open(lookup[frame]).convert('RGB');im.thumbnail((340,605));canvas.paste(im,(720,y+55))
canvas.save(Q/'source-stage-comparison.jpg',quality=94)
canvas=Image.new('RGB',(800,3*760),'#ddd');d=ImageDraw.Draw(canvas)
for i,f in enumerate([1170,1520,1530]):
 y=i*760
 for j,(label,fp) in enumerate([('v4 rejected',older[f]),('v4-fix1',lookup[f])]):
  d.text((20+j*400,y+10),f'{label} F{f} {f/60:.3f}s',fill='black',font=font);im=Image.open(fp).convert('RGB');im.thumbnail((390,695));canvas.paste(im,(5+j*400,y+45))
canvas.save(Q/'counterexample-comparison.jpg',quality=94)
