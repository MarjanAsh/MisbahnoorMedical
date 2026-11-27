import subprocess,json,sys
S=sys.argv[1]
W=[(0.0,.18),(6.60,.16),(7.45,.12),(11.84,.15),(18.80,.16),(24.22,.13),(32.64,.14),(34.86,.12),(44.36,.14),(52.15,.18)]
P=[(12.0,.2),(17.45,.2),(24.42,.16),(25.78,.16),(26.94,.16),(28.78,.16),(36.30,.16),(39.24,.16),(47.70,.16),(48.52,.16),(49.30,.14)]
O=[(21.45,"4",.18),(31.62,"5",.2)]
fc=["[0:a]atrim=0:44.46,asetpts=PTS-STARTPTS,afade=t=out:st=44.44:d=0.02[a1]",
"[0:a]atrim=50.14:55.02,asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st=4.86:d=0.02[a2]",
"[0:a]atrim=56.60:59.54,asetpts=PTS-STARTPTS,afade=t=in:d=0.02[a3]",
"[a1][a2][a3]concat=n=3:v=0:a=1,aresample=48000,highpass=f=85,lowpass=f=14000,equalizer=f=3000:t=q:w=1.2:g=2,acompressor=threshold=-22dB:ratio=3:attack=8:release=120:makeup=4,apad=pad_dur=3.2,asplit=2[voice][vsc]",
"[1:a]atrim=0:55.3,afade=t=in:d=1.5,afade=t=out:st=53.6:d=1.6,volume=0.16[mus]","[mus][vsc]sidechaincompress=threshold=0.03:ratio=6:attack=40:release=400[musd]",
f"[2:a]asplit={len(W)}"+"".join(f"[w{i}]" for i in range(len(W))), f"[3:a]asplit={len(P)}"+"".join(f"[p{i}]" for i in range(len(P)))]
lab=[]
def d(src,t,v,n): ms=int(t*1000); fc.append(f"[{src}]adelay={ms}|{ms},volume={v}[{n}]"); lab.append(f"[{n}]")
for i,(t,v) in enumerate(W): d(f"w{i}",t,v,f"sw{i}")
for i,(t,v) in enumerate(P): d(f"p{i}",t,v,f"sp{i}")
for t,inp,v in O: d(f"{inp}:a",t,v,f"so{inp}")
fc.append("[voice][musd]"+"".join(lab)+f"amix=inputs={2+len(lab)}:normalize=0:duration=first[mix]")
subprocess.run(["ffmpeg","-v","error","-y","-i",f"{S}/src.mp4","-i","music.wav","-i","whoosh.wav","-i","pop.wav","-i","tick.wav","-i","ding.wav","-filter_complex",";".join(fc),"-map","[mix]","-t","55.3","-c:a","pcm_s24le","mix.wav"],check=True)
r=subprocess.run(["ffmpeg","-i","mix.wav","-af","loudnorm=I=-14:TP=-1.5:LRA=9:print_format=json","-f","null","-"],capture_output=True,text=True).stderr
j=json.loads(r[r.rindex("{"):r.rindex("}")+1])
mi=f"measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}"
subprocess.run(["ffmpeg","-v","error","-y","-i","mix.wav","-af",f"loudnorm=I=-14:TP=-1.5:LRA=9:{mi}:linear=true,aresample=48000","-c:a","aac","-b:a","256k","mix.m4a"],check=True)
