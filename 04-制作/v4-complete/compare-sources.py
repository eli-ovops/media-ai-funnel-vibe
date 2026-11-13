from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib
P=Path(__file__).resolve().parent;S=P.parents[2]/'Fred付费资料全站学习-20261016/证据/01/动态采样图集'
rows=[('T02g',11,650),('T04b',19,4500),('T03e',28,6210),('T04g',7,7950)]
font=ImageFont.truetype('/System/Library/Fonts/SFNS.ttf',22)
canvas=Image.new('RGB',(1400,4*900),'#e4e4e4');d=ImageDraw.Draw(canvas);receipt=[]
for i,(key,n,frame) in enumerate(rows):
 source=S/f'{key}-key-{n:02d}.jpg';final=P/f'qc/export-frames-r4/F{frame}.png';y=i*900
 d.text((25,y+10),f'{key} exact preview sample | portrait full export F{frame} ({frame/60:.2f}s)',font=font,fill='black')
 im=Image.open(source).convert('RGB');im.thumbnail((840,740));canvas.paste(im,(20,y+180))
 im=Image.open(final).convert('RGB');im.thumbnail((460,820));canvas.paste(im,(920,y+50))
 receipt.append(dict(key=key,source=str(source),sourceSha256=hashlib.sha256(source.read_bytes()).hexdigest(),final=str(final),finalSha256=hashlib.sha256(final.read_bytes()).hexdigest()))
canvas.save(P/'qc/source-stage-comparison.jpg',quality=92)
(P/'qc/source-stage-comparison.json').write_text(json.dumps(receipt,indent=2))
