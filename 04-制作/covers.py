from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageFilter
import json,hashlib
P=Path(__file__).resolve().parent;O=P/'output/covers';O.mkdir(exist_ok=True)
PURPLE='#7952d8';BLACK='#19191c';PAPER='#f9f7f1'
fontpath=str(P/'public/fonts/MiSans-Heavy.otf')
def make(w,h,tag):
 s=2;im=Image.new('RGB',(w*s,h*s),PAPER);d=ImageDraw.Draw(im)
 def text(x,y,line,size,color):d.text((x*s,y*s),line,font=ImageFont.truetype(fontpath,round(size*s)),fill=color,stroke_width=0)
 def poly(points,color):d.polygon([(int(x*s),int(y*s)) for x,y in points],fill=color)
 def stroke(points,color,width):d.line([(int(x*s),int(y*s)) for x,y in points],fill=color,width=round(width*s),joint='curve')
 landscape=w>h
 if landscape:
  x=82;y=160;size=112 if w==1920 else 100
  for line,col in [('同样谈AI',PURPLE),('为何判断',BLACK),('差这么远？',BLACK)]:text(x,y,line,size,col);y+=size*1.4
  cx=w*.76;cy=h*.53;k=.8 if w==1440 else 1
 else:
  x=80;y=120 if h==1440 else 215;size=126
  for line,col in [('同样谈AI',PURPLE),('为何判断',BLACK),('差这么远？',BLACK)]:text(x,y,line,size,col);y+=size*1.35
  cx=w*.56;cy=h*(.70 if h==1440 else .77);k=1.06
 def pt(x,y):return(cx+x*k,cy+y*k)
 # A solid dimensional sheet is constructed as an object, not a frame from the video.
 for offset,col in [(70,'#ddd6ec'),(35,'#aa94d4'),(0,PURPLE)]:
  corners=[pt(-300,-130+offset),pt(130,-220+offset),pt(330,-40+offset),pt(-100,55+offset)]
  poly([(x,y+16*k) for x,y in corners],'#42305f');poly(corners,col)
  if offset==0:
   for i in range(3):stroke([pt(-190,-112+i*40),pt(85,-171+i*40)],'#f7f2ff',12)
 # Short answer and complex project remain editorial objects; no population chart.
 bx,by=pt(-300,180);bw,bh=230*k,115*k
 d.rounded_rectangle((bx*s,by*s,(bx+bw)*s,(by+bh)*s),radius=26*k*s,fill=BLACK)
 for i in range(2):stroke([(bx+28*k,by+38*k+i*30*k),(bx+178*k,by+38*k+i*30*k)],'#ffffff',7)
 a=pt(-110,130);b=(bx+bw/2,by);stroke([a,((a[0]+b[0])/2,a[1]),b],'#b7a7d0',5)
 im=im.resize((w,h),Image.Resampling.LANCZOS);file=O/f'funnel-v1-cover-{tag}.png';im.save(file)
 thumb=im.copy();thumb.thumbnail((360,540));thumb.save(P/'qc'/f'cover-phone-{tag}.png')
 return {'path':str(file),'width':w,'height':h,'sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'status':'CANDIDATE_FOR_USER_REVIEW','method':'Original code drawing, frozen copy; no imagegen or personal photo. Current pure-code/no-person instruction overrides default portrait/imagegen cover method.'}
rows=[make(1080,1440,'3x4'),make(1080,1920,'9x16'),make(1920,1080,'16x9'),make(1440,1080,'4x3')]
(P/'qc/covers.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));print([(r['width'],r['height']) for r in rows])
