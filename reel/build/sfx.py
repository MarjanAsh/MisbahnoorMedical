import numpy as np, wave
SR=48000
def save(n,x):
    x=np.clip(x,-1,1); y=(np.stack([x,x],1)*32767).astype(np.int16)
    w=wave.open(n,"wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(y.tobytes()); w.close()
rng=np.random.default_rng(1)
# warm ambient pad, 56 s: Cmaj9 - Am9 - Fmaj7 - G6sus, 7 s per chord
T=56.0; t=np.arange(int(SR*T))/SR; out=np.zeros_like(t)
ch=[[130.81,196.0,246.94,329.63,293.66],[110.0,164.81,196.0,261.63,246.94],[87.31,174.61,220.0,261.63,329.63],[98.0,146.83,196.0,246.94,293.66]]
L=7.0
for i in range(int(T/L)+1):
    f=ch[i%4]; s=i*L; e=s+L+2.0
    m=(t>=s)&(t<e); tt=t[m]-s
    env=np.minimum(tt/1.8,1)*np.minimum((e-s-tt)/2.0,1)
    v=sum(np.sin(2*np.pi*fr*tt+k)*(0.9**k)+0.25*np.sin(2*np.pi*fr*2.003*tt) for k,fr in enumerate(f))
    out[m]+=v*env*0.06
# gentle movement + soft lowpass via moving average
out*=0.85+0.15*np.sin(2*np.pi*0.11*t)
k=np.ones(24)/24; out=np.convolve(out,k,"same")
out/=np.abs(out).max(); out*=0.5
save("music.wav",out)
def env(n,a,d): x=np.arange(n)/SR; return np.minimum(x/a,1)*np.exp(-x/d)
n=int(SR*0.45); x=np.arange(n)/SR
noise=rng.standard_normal(n); 
# whoosh: noise with sweeping one-pole lowpass
y=np.zeros(n); c=np.linspace(0.02,0.35,n)**1.5; c=np.concatenate([c[:n//2*1],c[n//2*1:][::-1]])[:n]; acc=0
for i in range(n): acc+= c[i]*(noise[i]-acc); y[i]=acc
y*=np.sin(np.pi*x/x[-1]); save("whoosh.wav",y/np.abs(y).max()*0.6)
n=int(SR*0.09); x=np.arange(n)/SR; f=np.linspace(950,520,n)
save("pop.wav",np.sin(2*np.pi*np.cumsum(f)/SR)*env(n,0.003,0.03)*0.6)
n=int(SR*1.2); x=np.arange(n)/SR
save("ding.wav",(np.sin(2*np.pi*1318.5*x)+0.4*np.sin(2*np.pi*2637*x)+0.3*np.sin(2*np.pi*1975.5*x))*env(n,0.004,0.35)*0.35)
n=int(SR*0.05); x=np.arange(n)/SR
save("tick.wav",np.sin(2*np.pi*2200*x)*env(n,0.001,0.012)*0.5)
