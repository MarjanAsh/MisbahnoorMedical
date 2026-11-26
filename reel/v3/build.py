import os,subprocess,sys
AROLL=sys.argv[1]; OUT=sys.argv[2]
S="/tmp/claude-0/-home-user-MisbahnoorMedical/ed7f08f8-4982-5da4-8401-299beeb661bb/scratchpad"
# zoom levels (output time, level); ('d',a,b,amt) drift
LV=[(0,1.12),(2.78,1.0),(6.64,1.12),(7.57,1.0),(11.14,1.12),(15.0,1.0),(18.86,1.16),(21.40,1.12),(24.28,1.0),(25.56,1.12),(26.8,1.0),(28.06,1.12),(30.12,1.0),(32.70,1.16),(34.9,1.12),(37.6,1.0),(40.56,1.12),(44.46,1.0),(46.9,1.16),(49.34,1.12)]
DRIFT=[(18.86,21.40,0.10),(32.70,34.90,0.10),(46.90,49.34,0.10)]
T="(in/30)"; R=0.13
e=str(LV[0][1])
for (t,l),(_,p) in zip(LV[1:],LV[:-1]):
    d=l-p
    if abs(d)>1e-6: e+=f"+({d:.3f})*clip(({T}-{t})/{R},0,1)"
for a,b,amt in DRIFT: e+=f"+between({T},{a},{b})*{amt}*({T}-{a})/{b-a:.2f}"
Z=f"1.2*({e})"
steps=[t for t,_ in LV[1:]]+[44.46,49.34]
mb="+".join(f"between(t,{t-0.03:.2f},{t+0.17:.2f})" for t in sorted(set(steps)))
G="curves=master='0/0.065 0.22/0.215 0.5/0.515 0.8/0.81 1/0.965',colortemperature=temperature=6000:mix=0.35,huesaturation=colors=c+b:saturation=-0.18,huesaturation=colors=r+y:saturation=0.06:intensity=0.01,eq=saturation=1.05"
inputs=["-i",AROLL]; fc=[f"[0:v]fps=30,scale=1296:2304:flags=lanczos,setsar=1,zoompan=z='{Z}':x='iw/2-iw/zoom/2':y='(ih-ih/zoom)*0.38':d=1:s=1080x1920:fps=30,tmix=frames=3:weights='1 2 1':enable='{mb}'[b0]"]
cur="b0"; k=1
CARDS=[("c1.mov",6.66),("c2.mov",18.86),("c3.mov",30.12),("c4.mov",34.90)]
BROLL={"doctor":(18.86,21.40),"walk":(24.28,25.56),"meal":(25.56,26.80),"iv":(32.70,34.90),"newborn":(46.90,49.34)}
used_doc=os.path.exists("broll/doctor.mp4")
for f,t in CARDS:
    if f=="c2.mov" and used_doc: continue
    inputs+=["-i",f]; fc.append(f"[{k}:v]setpts=PTS-STARTPTS+{t}/TB[o{k}];[{cur}][o{k}]overlay=eof_action=pass:format=auto[b{k}]"); cur=f"b{k}"; k+=1
for n,(a,b) in BROLL.items():
    p=f"broll/{n}.mp4"
    if not os.path.exists(p): continue
    d=b-a
    inputs+=["-i",p]
    fc.append(f"[{k}:v]fps=30,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,trim=0:{d+0.05:.2f},setpts=PTS-STARTPTS,format=yuva420p,fade=t=in:d=0.15:alpha=1,fade=t=out:st={d-0.12:.2f}:d=0.12:alpha=1,setpts=PTS+{a}/TB[o{k}];[{cur}][o{k}]overlay=eof_action=pass[b{k}]"); cur=f"b{k}"; k+=1
fc.append(f"[{cur}]{G},trim=0:52.28,setpts=PTS-STARTPTS[main]")
inputs+=["-loop","1","-t","3.0","-i","endbg.png"]
fc.append(f"[{k}:v]fps=30,scale=1296:2304,zoompan=z='1.0+0.06*in/90':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1080x1920:fps=30,{G},trim=0:3.0,setpts=PTS-STARTPTS[end]"); k+=1
fc.append("[main][end]concat=n=2:v=1:a=0,format=gbrp[cat]")
inputs+=["-i","leak.mp4"]
fc.append(f"[{k}:v]scale=1080:1920:flags=bicubic,format=gbrp[lk];[cat][lk]blend=all_mode=screen:all_opacity=0.85:shortest=1,ass=captions.ass,noise=alls=3:allf=t,format=yuv420p[v]")
cmd=["ffmpeg","-v","error","-y",*inputs,"-filter_complex",";".join(fc),"-map","[v]","-t","55.28","-r","30","-c:v","libx264","-preset","slow","-crf","16","-profile:v","high","-pix_fmt","yuv420p",OUT]
open("cmd.txt","w").write(" ".join(cmd))
subprocess.run(cmd,check=True)
