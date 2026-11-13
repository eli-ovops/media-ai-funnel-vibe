from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent
assert json.loads((P/'qc/canvas-full-receipt.json').read_text())['renderedFrames']==9000
p=P/'src/World.ts';old=p.read_text();(P/'src/World-before-camera-seam.ts').write_text(old)
s=old.replace('if(t>=89&&t<95.3){let v:V;','if(t>=88&&t<95.6){let v:V;').replace('if(t>=117&&t<118.4){const v=pathPoint','if(t>=116.6&&t<118.4){const v=pathPoint').replace('return{x:v[0],y:v[1]+45,z:1.35};','const u=q(t,117,118.4);return{x:v[0],y:v[1]+mix(45,40,u),z:mix(1.35,1.3,u)};')
assert old!=s and 'if(t>=88&&t<95.6)' in s;p.write_text(s)
(P/'qc/camera-seam-source-receipt.json').write_text(json.dumps({'before_sha256':hashlib.sha256(old.encode()).hexdigest(),'after_sha256':hashlib.sha256(s.encode()).hexdigest(),'ranges_frames_end_exclusive':[[5280,5736],[6996,7104]],'source_before':str(P/'src/World-before-camera-seam.ts'),'source_after':str(p),'scope':'camera function only; no chart/text/audio/source data changed'},indent=2))
