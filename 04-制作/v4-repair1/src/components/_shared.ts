// 本批（章节过渡 T12k–T12t、开场进场 T20h–T20q）共用的小工具；只做内容计算，不定义任何视觉值（视觉值一律取 ../kit）。
import { clamp, mix, textWidth } from '../kit/theme';

const CN = '一二三四五六七八九十';
const cnNum = (n: number) => n <= 10 ? CN[n - 1] : n < 20 ? `十${CN[n - 11]}` : n < 100 ? `${CN[Math.floor(n / 10) - 1]}十${n % 10 ? CN[n % 10 - 1] : ''}` : String(n);
// 「第N部分」；label 非空时用 label
export const partLabel = (index: number, label = '') => label || `第${index >= 1 ? cnNum(index) : index}部分`;
export const pad2 = (n: number) => String(Math.max(0, Math.round(n))).padStart(2, '0');

// 字号 = min(上限, 可用宽 / 估算宽)
export const fit = (s: string, max: number, avail: number) => Math.min(max, avail / Math.max(1, textWidth(s, 1)));

// 长标题折两行：优先在标点/空格处断（沿 T12a splitTitle）
export function splitTitle(title: string, maxUnits: number): string[] {
  if (textWidth(title, 1) <= maxUnits) return [title];
  const chars = Array.from(title);
  const half = textWidth(title, 1) / 2;
  let best = Math.floor(chars.length / 2), bestScore = Infinity, acc = 0;
  for (let i = 1; i < chars.length; i++) {
    acc += textWidth(chars[i - 1], 1);
    const prev = chars[i - 1];
    const brk = /[，,、：:；; ]/.test(prev) ? -3 : /[的和与]/.test(prev) ? -1.5 : 0;
    const score = Math.abs(acc - half) + brk;
    if (score < bestScore) { bestScore = score; best = i; }
  }
  return [chars.slice(0, best).join('').trim(), chars.slice(best).join('').trim()];
}

// 一句话按强调词拆三段（一句里只强调一处）
export function splitHighlight(text: string, hl: string): [string, string, string] {
  const i = hl ? text.indexOf(hl) : -1;
  if (i < 0) return [text, '', ''];
  return [text.slice(0, i), hl, text.slice(i + hl.length)];
}

// 固定种子伪随机（渲染必须确定）
export const rand = (seed: number) => {
  const x = Math.sin(seed * 127.1 + 311.7) * 43758.5453;
  return x - Math.floor(x);
};

// 对数插值缩放：推近/拉远时速度感均匀
export const zoomMix = (a: number, b: number, e: number) => Math.exp(mix(Math.log(a), Math.log(b), clamp(e)));

// ease-in（只给“撞上”这类加速到接触的动作用）
export const easeIn = (t: number, a: number, b: number) => { const v = clamp((t - a) / (b - a)); return v * v * v; };
