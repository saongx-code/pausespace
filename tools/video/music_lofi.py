import numpy as np, wave
SR=44100; D=43.0; N=int(SR*D); rng=np.random.default_rng(11); t=np.arange(N)/SR
out=np.zeros((N,2))
BPM=84; beat=60/BPM; bar=beat*4
def add(y,at,pan=0.0,g=1.0):
    s=int(at*SR); n=min(len(y),N-s)
    if n<=0: return
    out[s:s+n,0]+=y[:n]*g*(1-pan); out[s:s+n,1]+=y[:n]*g*(1+pan)
def lp(x,k): return np.convolve(x,np.ones(k)/k,'same')
def kick():
    n=int(0.45*SR); tt=np.arange(n)/SR; f=48+90*np.exp(-tt/0.04)
    return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt/0.22)*1.0
def snare():
    n=int(0.3*SR); tt=np.arange(n)/SR; nz=lp(rng.standard_normal(n),3)
    return (nz*np.exp(-tt/0.07)*0.45+np.sin(2*np.pi*190*tt)*np.exp(-tt/0.05)*0.35)
def hat(o=False):
    n=int((0.18 if o else 0.05)*SR); tt=np.arange(n)/SR; nz=rng.standard_normal(n); nz=nz-lp(nz,4)
    return nz*np.exp(-tt/(0.06 if o else 0.012))*0.22
def rhodes(f,dur):
    n=int(dur*SR); tt=np.arange(n)/SR
    y=(np.sin(2*np.pi*f*tt)*np.exp(-tt/2.2)+0.3*np.sin(2*np.pi*2*f*tt)*np.exp(-tt/0.7)+0.06*np.sin(2*np.pi*6.9*f*tt)*np.exp(-tt/0.1))
    y*=(1+0.15*np.sin(2*np.pi*3.6*tt))*np.minimum(1,tt/0.008)*np.minimum(1,(n/SR-tt)/0.25)
    return y
def bass(f,dur):
    n=int(dur*SR); tt=np.arange(n)/SR
    return (np.sin(2*np.pi*f*tt)+0.25*np.sin(2*np.pi*2*f*tt))*np.exp(-tt/0.9)*np.minimum(1,tt/0.01)*np.minimum(1,(n/SR-tt)/0.05)
hz=lambda m:440*2**((m-69)/12)
# neo-soul lounge: Fmaj9 - Em9 - Dm9 - G13sus
prog=[([53,57,60,64,67],41),([52,55,59,62,66],40),([50,53,57,60,64],38),([55,60,62,65,69],43)]
start=1.2
nb=int((41.5-start)/bar)+1
for b in range(nb):
    st=start+b*bar; ch,root=prog[b%4]
    for i,m in enumerate(ch): add(rhodes(hz(m),bar*0.98),st+0.012*i+0.02,pan=(i-2)*0.12,g=0.05)
    add(rhodes(hz(ch[-1]+12),beat*1.2),st+beat*2.5,pan=0.3,g=0.025)
    add(bass(hz(root),beat*1.5),st,g=0.22); add(bass(hz(root),beat*0.6),st+beat*1.75,g=0.16); add(bass(hz(root+7),beat*1.2),st+beat*2.5,g=0.18)
    if st>2.8:
        for k in range(4):
            sw=0.055 if k%2 else 0
            if k in(0,):add(kick(),st+k*beat,g=0.55)
            if k==2: add(kick(),st+k*beat+beat*0.5+sw,g=0.4)
            if k in(1,3): add(snare(),st+k*beat+0.01,g=0.5)
        for e in range(8):
            add(hat(e==7),st+e*beat/2+(0.06 if e%2 else 0),pan=0.25,g=0.7 if e%2==0 else 0.45)
# vinyl
cr=np.zeros(N); idx=rng.integers(0,N,int(D*10)); cr[idx]=rng.standard_normal(len(idx))*0.2
out+=np.stack([cr,np.roll(cr,30)],1)*0.04
hiss=rng.standard_normal((N,2)); hiss-=np.apply_along_axis(lambda x:lp(x,3),0,hiss); out+=hiss*0.004
# tape wobble (slight lowpass + warmth)
for c in range(2): out[:,c]=lp(out[:,c],2)
# reverb
ir_n=int(1.6*SR); ir=rng.standard_normal((ir_n,2))*np.exp(-np.arange(ir_n)/SR/0.4)[:,None]; ir/=np.abs(ir).sum(0)*0.1
from numpy.fft import rfft,irfft
L=N+ir_n; wet=np.stack([irfft(rfft(out[:,c],L)*rfft(ir[:,c],L),L)[:N] for c in range(2)],1)
out=out*0.85+wet*0.25
out*=(np.minimum(1,t/1.5)*np.clip((D-t)/3.0,0,1))[:,None]
out=np.tanh(out/np.abs(out).max()*1.3)*0.55
def save(p,a):
    w=wave.open(p,'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(a,-1,1)*32767).astype('<i2').tobytes()); w.close()
save('music2.wav',out)
fx=np.zeros((N,2))
def bowl(at,f0,amp):
    s=int(at*SR); n=min(int(9*SR),N-s); tt=np.arange(n)/SR; y=np.zeros(n)
    for r,a,d in [(1,1,8),(2.71,.5,5),(5.12,.25,2.8),(8.43,.1,1.6)]:
        for dt in(-0.4,0.4): y+=a*0.5*np.sin(2*np.pi*(f0*r+dt*r)*tt+rng.random()*6)*np.exp(-tt/d)
    th=lp(rng.standard_normal(int(0.03*SR)),25)*np.exp(-np.arange(int(0.03*SR))/SR/0.006); y[:len(th)]+=th*2
    y*=np.minimum(1,tt/0.003); fx[s:s+n,0]+=y*amp; fx[s:s+n,1]+=np.roll(y,20)*amp
bowl(17.0,212,0.2); bowl(38.9,212,0.16)
save('fx2.wav',fx)
