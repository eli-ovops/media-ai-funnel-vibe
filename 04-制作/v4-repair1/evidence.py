from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).resolve().parent;Q=P/'qc';D=P.parent.parent/'05-质检/v4-complete'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rec=lambda p:dict(path=str(p),sha256=sha(p))
issues=[
 ('V4-Q1',[91,119],[91,125],[176,196,205,219],[5760,6000,6480,6840,7260],
  '同一01事项新增、打勾、保存状态进入记录区；关窗后重开并从保存记录回到主窗，分别核对文字及勾选。条件丢失再检查保留，不写真实App实测通过。'),
 ('V4-Q2',[133.7,140.5],[132,141],[253],[8280,8340,8406],
  '删去重复结论；三类访问条件逐路建立，齐备后必要阅读约2.55秒，140.1开始退出。释放6秒用于Q1。'),
 ('V4-Q3',[119,119.7],[124.1,125.7],[227],[7476,7500,7542],
  '旧事项窗向下退出；旧标题先退，124.5起新标题在顶部出现。数学/编程两列随后建立，无旧窗盖新标题。'),
 ('V4-Q4',[140.4,141],[140.1,142.1],[259],[8436,8460,8496],
  '旧树整组下移退出。新因素在旧树退离后进入，连线141.5起从新因素下缘1280开始，绝不从旧叶卡字区生长。'),
 ('V4-Q5',[146.4,146.9],[145.5,147],[279],[8760,8796,8820],
  '三个小因素缩入唯一结论胶囊，文字/阴影/线随之退净；146.3后只剩唯一结论载体，再向上移动换最终问题。')]
rows=[]
for i,old,new,before,after,note in issues:
 rows.append(dict(id=i,oldSeconds=old,newSeconds=new,before=[rec(D/f'frame-{n}.jpg') for n in before],
                  after=[dict(frame=n,time_sec=n/60,**rec(Q/f'export/F{n}.png')) for n in after],
                  result='SELF_REVIEWED_IN_SAMPLES_PENDING_INDEPENDENT05',finding=note))
(Q/'repair-evidence.json').write_text(json.dumps({'baselineVideoSha256':'6ac2862d8b34a813ff471ff13d14a572bb77f35e0c5df78e1267bcaab343cbd0','newVideoSha256':'71c213a4b4d90fc3448a463f8d96e6994786ec32c56168acba2d1518d4dff7dc','issues':rows},ensure_ascii=False,indent=2))
font=ImageFont.truetype('/System/Library/Fonts/SFNS.ttf',20)
for i,ns in enumerate([[5760,6000,6480,7260],[8280,8436,8796,8820]]):
 im=Image.new('RGB',(720,1340),'#dddddd');d=ImageDraw.Draw(im)
 for j,n in enumerate(ns):
  x=j%2*360;y=j//2*670;d.text((x+8,y+5),f'F{n} / {n/60:.1f}s',font=font,fill='black')
  im.paste(Image.open(Q/f'export/F{n}.png').convert('RGB').resize((360,640)),(x,y+30))
 im.save(Q/f'phone-scale-{i+1}.jpg',quality=94)
print('Five issue evidence groups and two phone-scale sheets saved')
