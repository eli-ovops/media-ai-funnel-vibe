import React from 'react';
import {registerRoot,Composition} from 'remotion';
import {Representative} from './Episode';
const Root=()=> <Composition id="Representative" component={Representative} width={1080} height={1920} fps={60} durationInFrames={2160}/>;
registerRoot(Root);
