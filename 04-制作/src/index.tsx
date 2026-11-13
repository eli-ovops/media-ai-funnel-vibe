import React,{useLayoutEffect,useRef,useState} from 'react';
import {Composition,registerRoot,useCurrentFrame,delayRender,continueRender,staticFile} from 'remotion';
import {drawWorld} from './World';
const Film=()=>{const frame=useCurrentFrame();const canvas=useRef<HTMLCanvasElement>(null);const [ready,setReady]=useState(false);const [handle]=useState(()=>delayRender('load exact Fred fonts'));
 useLayoutEffect(()=>{let alive=true;Promise.all([['Fred MiSans','MiSans-Medium.otf','500'],['Fred MiSans Heavy','MiSans-Heavy.otf','800'],['Fred RuiZi','RuiZi.ttf','400']].map(async([family,file,weight])=>{const face=new FontFace(family,`url(${staticFile('fonts/'+file)})`,{weight});await face.load();document.fonts.add(face)})).then(()=>{if(alive){setReady(true);continueRender(handle)}});return()=>{alive=false}},[]);
 useLayoutEffect(()=>{if(ready&&canvas.current)drawWorld(canvas.current.getContext('2d')!,frame)},[frame,ready]);
 return <canvas ref={canvas} width={1080} height={1920} style={{width:1080,height:1920,display:'block'}}/>;
};
registerRoot(()=> <Composition id="Funnel150" component={Film} width={1080} height={1920} durationInFrames={9000} fps={60}/>);
