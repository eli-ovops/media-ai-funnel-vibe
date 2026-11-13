from pathlib import Path
import numpy as np,json,wave,hashlib
P=Path(__file__).resolve().parent; sr=48000
mix=np.zeros((150*sr,2),np.float64)
rng=np.random.default_rng(20261020)
events=json.loads((P/'events.json').read_text())
for n,e in enumerate(events):
 kind=e['type'];dur={'tap':.14,'air':.55,'paper':.24}[kind];t=np.arange(round(dur*sr))/sr
 attack=np.minimum(t/.008,1);tail=np.minimum((dur-t)/.025,1)
 if kind=='tap':s=(np.sin(2*np.pi*510*t)*.65+np.sin(2*np.pi*1070*t)*.15)*np.exp(-t*38)*attack*tail*.12
 else:
  noise=rng.standard_normal(len(t));smooth=np.convolve(noise,np.ones(21)/21,mode='same');env=np.sin(np.pi*t/dur)**2
  s=smooth*env*({'air':.10,'paper':.12}[kind]);
  if kind=='paper':s*=.6+.4*np.sin(2*np.pi*34*t)**2
 pan=(n%3-1)*.16;clip=np.column_stack([s*np.sqrt((1-pan)/2),s*np.sqrt((1+pan)/2)])
 a=e['frame']*sr//60;mix[a:a+len(t)]+=clip
mix*=2.8
pcm=(np.clip(mix,-1,1)*32767).astype('<i2');out=P/'output/code-sfx-v1.wav'
with wave.open(str(out),'wb') as f:f.setnchannels(2);f.setsampwidth(2);f.setframerate(sr);f.writeframes(pcm.tobytes())
report={'sample_rate':sr,'channels':2,'duration_seconds':150,'seed':20261020,'events':len(events),'peak_dbfs':float(20*np.log10(np.max(np.abs(mix)))),'clipped_samples':int((np.abs(mix)>=1).sum()),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'music_bus':{'status':'PENDING_EXACT_NICO_ASSET','path':None},'hearing':'NOT_PERFORMED; no direct supported audio perception','voice_or_tts':False}
(P/'qc/audio-synthesis.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(report)
