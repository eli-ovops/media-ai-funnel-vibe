import React from 'react';
import {registerRoot,Composition} from 'remotion';
import {Episode} from './FullEpisode';
const Root=()=> <Composition id="Episode" component={Episode} width={1080} height={1920} fps={60} durationInFrames={9000}/>;
registerRoot(Root);
