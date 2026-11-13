import {Easing, interpolate} from 'remotion';
// Exact Fred wave3 theme timing primitives. Palette is a centralized episode adaptation.
export const clamp=(x:number,a=0,b=1)=>Math.min(b,Math.max(a,x));
export const mix=(a:number,b:number,v:number)=>a+(b-a)*v;
export const p=(t:number,a:number,b:number)=>interpolate(t,[a,b],[0,1],{easing:Easing.bezier(.22,1,.36,1),extrapolateLeft:'clamp',extrapolateRight:'clamp'});
export const q=(t:number,a:number,b:number)=>{const v=clamp((t-a)/(b-a));return v*v*(3-2*v)};
export const springAt=(t:number,delay:number,dur=.55)=>{const v=clamp((t-delay)/dur);return v===1?1:1-Math.exp(-8*v)*Math.cos(9*v)};
export const S={bg:'#151b1b',ink:'#f3edda',dim:'#a7b2a9',gold:'#edcd87',teal:'#7ab7b0',dark:'#233432',edge:'#52635a',paper:'#f3edda',body:'Fred MiSans',display:'Fred RuiZi'};
// T05h-SyncVsCopy.pt: same-source cubic carrier path, retained exactly.
export function syncPoint(x0:number,y0:number,x1:number,y1:number,u:number){const my=(y0+y1)/2,m=1-u;return {x:m*m*m*x0+3*m*m*u*x0+3*m*u*u*x1+u*u*u*x1,y:m*m*m*y0+3*m*m*u*my+3*m*u*u*my+u*u*u*y1}}
// T04b-RoleSplit: contiguous bar splits into equal segments; inner radii and gap grow together.
export function roleSplit(t:number,at:number,w=660,h=116,n=3){const split=q(t,at,at+.6),gap=36*split;return {split,gap,segW:(w-(n-1)*gap)/n,innerR:mix(0,h/2,split)}}
// T20m-PillToWindow: the same pill expands into a window, instead of replacing its carrier.
export function pillWindow(t:number,at:number,smallW:number,smallH:number,w:number,h:number){const k=q(t,at,at+.8);return {w:mix(smallW,w,k),h:mix(smallH,h,k),r:mix(smallH/2,24,k)}}
// sy17-editorial camAt: logarithmic zoom and inOutCubic, with task-specific stops.
export function editorialCamera(t:number,keys:{t:number,x:number,y:number,z:number}[]){let i=0;while(i<keys.length-2&&t>keys[i+1].t)i++;const a=keys[i],b=keys[i+1],v=clamp((t-a.t)/(b.t-a.t)),u=v<.5?4*v*v*v:1-Math.pow(-2*v+2,3)/2;return{x:mix(a.x,b.x,u),y:mix(a.y,b.y,u),z:Math.exp(mix(Math.log(a.z),Math.log(b.z),u))}}
// sy20-blueprint camera basis/project, adapted only to vertical output coordinates.
const sub=(a:number[],b:number[])=>a.map((x,i)=>x-b[i]);
const dot=(a:number[],b:number[])=>a.reduce((s,x,i)=>s+x*b[i],0);
const cross=(a:number[],b:number[])=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
const norm=(a:number[])=>{const l=Math.hypot(...a);return a.map(x=>x/l)};
export function camMat(ro:number[],ta:number[]){const w=norm(sub(ta,ro)),u=norm(cross(w,[0,1,0])),v=cross(u,w);return{u,v,w}}
export function project(P:number[],ro:number[],M:ReturnType<typeof camMat>,cx=540,cy=1160){const d=sub(P,ro),z=dot(d,M.w);return [cx+dot(d,M.u)/z*1500,cy-dot(d,M.v)/z*1500]}
