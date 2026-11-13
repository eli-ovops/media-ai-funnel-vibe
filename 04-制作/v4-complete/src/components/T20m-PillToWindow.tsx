// T20m 胶囊变窗（开场 4s）：先是一枚写着钩子的黑胶囊落在正中；胶囊的字退下，胶囊本身向四周撑开成一个大播放窗，真实画面在“胶囊里”亮出来；最后钩子缩成小胶囊压在窗口下沿。
// 观众要看懂的变化：一句钩子 → 这枚胶囊本身撑开成窗口，里面就是要讲的画面。
// 动作来源：motion-craft 第 4 节对象连续（点 → 胶囊 → 窗口是同一个 div，圆角从 h/2 收到 24）+ 108 大播放组件的窗口规格（圆角、软阴影）。
import React from 'react';
import { S, clamp, cueAt, mix, p, q, textWidth } from '../kit/theme';
import { Frame, Handoff, HandoffProps, Media, Sfx, textBase, useT } from '../kit/ui';
import { fit, splitHighlight } from './_shared';

export type PillToWindowProps = HandoffProps & {
  hook: string;         // 胶囊里的钩子
  highlight: string;
  children?: React.ReactNode;
  src: string;          // 窗口里的真实画面（视频或图片）
  ratio: number;
  start: number;
  cues?: number[];      // [0]=胶囊撑开，[1]=钩子回到窗口下沿
};

export const pillToWindowDefaults: PillToWindowProps = {
  hook: '模糊老照片，一键变高清',
  highlight: '一键变高清',
  src: 'media/up-app.mp4',
  ratio: 1440 / 1080,
  start: 1,
};

export function PillToWindow(props: Partial<PillToWindowProps>) {
  const c = { ...pillToWindowDefaults, ...props };
  const t = useT();
  const openAt = cueAt(c.cues, 0, 1.15);
  const backAt = cueAt(c.cues, 1, openAt + 0.9);
  const [a, hl, b] = splitHighlight(c.hook, c.highlight);

  // 1) 胶囊：点 → 胶囊（T12a 写法，无回弹）
  const size = 78;
  const PH = 200, PW = 850;
  const dot = 1;
  const spread = 1;
  const pw0 = mix(PH * dot, PW, spread), ph0 = PH * dot;
  const textIn = 1;

  // 2) 撑开成窗口（同一个对象）
  const WH = 310, WW = 720;
  const open = q(t, openAt, openAt + 0.7);
  const w = mix(pw0, WW, open), h = mix(ph0, WH, open);
  const cy = mix(950, 685, open);
  const r = mix(ph0 / 2, S.radius, open);
  const textOut = q(t, openAt + 0.45, openAt + 0.63);
  const ready = t >= openAt + 0.7;

  // 3) 钩子缩回窗口下沿
  const s2 = Math.min(84, size * 0.72);
  const P2H = s2 * 1.62, P2W = textWidth(c.hook, s2) + P2H * 1.05;
  const back = p(t, backAt, backAt + 0.45);

  return <Frame>
    <Handoff enter={c.enter} exit={c.exit} exitAt={c.exitAt}>
      {!ready && ph0 > 0.5 && <div style={{
        position: 'absolute', left: 540 - w / 2, top: cy - h / 2, width: w, height: h, borderRadius: r, overflow: 'hidden',
        background: S.dark, boxShadow: S.capsuleShadow,
        display: 'flex', alignItems: 'center', justifyContent: 'center',
      }}>
        {t >= openAt + 0.63 && <div style={{position:'absolute',inset:0,opacity:p(t,openAt+.63,openAt+.7)}}>
          <div style={{position:'absolute',left:0,right:0,top:30,textAlign:'center',...textBase(42,500),color:'#fff',opacity:.72}}>新增 · 完成 · 待办清单</div>
          <div style={{position:'absolute',left:0,right:0,top:88.6,textAlign:'center',...textBase(140,900),color:'#fff'}}>一条事项</div>
        </div>}
        {textOut < 1 && <span style={{
          ...textBase(size, 400, S.display), color: '#fff', opacity: textIn * (1 - textOut),
          transform: `translateY(${(1 - textIn) * 26 - textOut * 40}px)`,
        }}>{a}<span style={{ color: S.accentDark }}>{hl}</span>{b}</span>}
      </div>}
      {ready && c.children}
      {back > 0 && <div style={{
        position: 'absolute', left: 960 - P2W / 2, top: 70 + WH - P2H * 0.45, width: P2W, height: P2H, borderRadius: P2H / 2,
        background: S.dark, boxShadow: S.capsuleShadow, display: 'flex', alignItems: 'center', justifyContent: 'center',
        opacity: clamp(back * 4), transform: `translateY(${(1 - back) * 40}px) scale(${mix(1.1, 1, back)})`,
      }}>
        <span style={{ ...textBase(s2, 400, S.display), color: '#fff' }}>{a}<span style={{ color: S.accentDark }}>{hl}</span>{b}</span>
      </div>}
    </Handoff>
    <Sfx name="pop" at={0.2} />
    <Sfx name="whoosh-short" at={openAt} />
    <Sfx name="pop" at={backAt + 0.1} volume={0.4} />
  </Frame>;
}
