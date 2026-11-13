from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent
old=json.loads((P/'qc/final-frame-index.json').read_text())['samples'];new=json.loads((P/'qc/delivery-frame-index.json').read_text())['samples'];old={e['frame']:e for e in old};new={e['frame']:e for e in new}
rows=[]
for f,e in new.items():
 if f not in old or 1620<=f<1980 or 2760<=f<2844 or 5280<=f<5736:continue
 a=np.asarray(Image.open(old[f]['path'])).astype(float);b=np.asarray(Image.open(e['path'])).astype(float);m=float(np.abs(a-b).mean());rows.append({'frame':f,'mean_abs_rgb_error':m})
assert max(r['mean_abs_rgb_error'] for r in rows)<1
results=[]
for f,target,width in [(3000,[231,167,125],144),(3900,[182,180,236],432)]:
 a=np.array(Image.open(new[f]['path'])).astype(float);line=a[1080,150:930,:3];hits=np.where(np.linalg.norm(line-np.array(target),axis=1)<35)[0];got=int(hits[-1]-hits[0]+1);assert abs(got-width)<=2
 results.append({'frame':f,'expected_width_px':width,'measured_width_px':got,'measured_start_x':int(hits[0]+150),'ruler_width_px':720,'method':'decoded final MP4 frame row1080; RGB distance35 threshold; no image resampling'})
(P/'qc/final-pixel-check.json').write_text(json.dumps({'unchanged_sample_comparison':rows,'unchanged_sample_max_MAE':max(r['mean_abs_rgb_error'] for r in rows),'meaning':'unchanged sampled images visually equivalent after final encode; not continuous-video equivalence','chart_bar_checks':results,'status':'PASS'},indent=2));print(json.dumps(results))
