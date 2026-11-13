from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import sys,math
P=Path(__file__).resolve().parent
src=P/sys.argv[1]; dest=P/sys.argv[2]
files=sorted(src.glob('F*.png'),key=lambda f:int(f.stem[1:]))
fnt=ImageFont.truetype('/System/Library/Fonts/SFNS.ttf',20)
for page in range(math.ceil(len(files)/24)):
 group=files[page*24:(page+1)*24];can=Image.new('RGB',(1440,math.ceil(len(group)/6)*455),'#dedede');d=ImageDraw.Draw(can)
 for i,f in enumerate(group):
  im=Image.open(f).convert('RGB');im.thumbnail((230,410));x=i%6*240;y=i//6*455;can.paste(im,(x+5,y+35));d.text((x+5,y+4),f'{f.stem} {int(f.stem[1:])/60:.2f}s',font=fnt,fill='black')
 can.save(str(dest)+f'-{page+1}.jpg',quality=92)
print(len(files))
