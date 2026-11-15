import numpy as np, onnxruntime as ort, sys, wave
M='sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2024-07-17/'
def fbank(x,sr=16000):
    x=x.astype(np.float64)
    fl,fs,nfft=400,160,512
    n=1+(len(x)-fl)//fs
    idx=np.arange(fl)[None,:]+fs*np.arange(n)[:,None]
    f=x[idx]; f=f-f.mean(1,keepdims=True)
    f=np.concatenate([f[:,:1],f[:,1:]-0.97*f[:,:-1]],1)
    w=(0.5-0.5*np.cos(2*np.pi*np.arange(fl)/(fl-1)))**0.85
    p=np.abs(np.fft.rfft(f*w,nfft))**2
    mel=lambda h:1127*np.log(1+h/700)
    lo,hi=mel(20),mel(8000); pts=np.linspace(lo,hi,82)
    fm=mel(np.arange(nfft//2+1)*sr/nfft)
    W=np.zeros((80,nfft//2+1))
    for i in range(80):
        l,c,r=pts[i],pts[i+1],pts[i+2]
        W[i]=np.clip(np.minimum((fm-l)/(c-l),(r-fm)/(r-c)),0,None)
    return np.log(np.maximum(p@W.T,1.19e-7)).astype(np.float32)
def run(path,s,tok,meta,off=0):
    w=wave.open(path); a=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32)
    F=fbank(a)
    F=np.concatenate([np.repeat(F[:1],3,0),F],0)
    T=(len(F)-7)//6+1
    L=np.stack([F[i*6:i*6+7].reshape(-1) for i in range(T)])
    nm=np.array(meta['neg_mean'].split(','),np.float32); iv=np.array(meta['inv_stddev'].split(','),np.float32)
    L=(L+nm)*iv
    lg=s.run(None,{'x':L[None],'x_length':np.array([T],np.int32),'language':np.array([3],np.int32),'text_norm':np.array([14],np.int32)})[0][0]
    ids=lg.argmax(-1); out=[];prev=-1;times=[]
    for t,i in enumerate(ids):
        if i!=prev and i!=0:
            out.append(tok[i]); times.append(off+max(t-4,0)*0.06)
        prev=i
    return out[4:],times[4:]
s=ort.InferenceSession(M+'model.int8.onnx'); meta=s.get_modelmeta().custom_metadata_map
tok={int(l.split()[-1]):l.rsplit(' ',1)[0] for l in open(M+'tokens.txt',encoding='utf8')}
o,t=run(sys.argv[1],s,tok,meta)
print(''.join(o).replace('▁',' '))
for a,b in zip(o,t): print(f'{b:.2f}\t{a}')
