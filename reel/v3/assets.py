import numpy as np, subprocess, math
from PIL import Image, ImageFilter, ImageDraw
FPS=30; W,H=1080,1920
def ease_out_back(x,s=1.6): x-=1; return x*x*((s+1)*x+s)+1
def ease_in(x): return x*x*x
def rounded(img,r):
    m=Image.new("L",img.size,0); ImageDraw.Draw(m).rounded_rectangle([0,0,img.size[0]-1,img.size[1]-1],r,fill=255); img.putalpha(m); return img
def card_clip(name,src,crop,dur,cw=760,cy=740,kb=(1.0,1.08),pan=(0,0)):
    im=Image.open(src).convert("RGB")
    if crop: im=im.crop(crop)
    ar=im.size[1]/im.size[0]; ch=int(cw*ar)
    n=int(round(dur*FPS)); tin=9; tout=8
    p=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","rgba","-s",f"{W}x{H}","-r","30","-i","-","-c:v","png","-f","mov",name],stdin=subprocess.PIPE)
    # shadow template
    sh=Image.new("L",(cw+160,ch+160),0); ImageDraw.Draw(sh).rounded_rectangle([80,95,80+cw,95+ch],40,fill=150); sh=sh.filter(ImageFilter.GaussianBlur(28))
    for i in range(n):
        u=i/(n-1)
        z=kb[0]+(kb[1]-kb[0])*u
        iw,ih=im.size; sw,shh=iw/z,ih/z; ox=(iw-sw)/2+pan[0]*u*iw; oy=(ih-shh)/2+pan[1]*u*ih
        inner=im.crop((int(ox),int(oy),int(ox+sw),int(oy+shh))).resize((cw,ch),Image.LANCZOS)
        if i<tin: a=i/tin; s=0.55+0.45*ease_out_back(a); dy=(1-a)*140; op=min(1,a*1.6); blur=(1-a)*6
        elif i>=n-tout: a=(i-(n-tout))/tout; s=1-0.22*ease_in(a); dy=-a*60; op=1-a; blur=a*5
        else: s=1; dy=0; op=1; blur=0
        c=rounded(inner.copy(),40)
        if blur>0.3: c=c.filter(ImageFilter.GaussianBlur(blur))
        cs=(max(2,int(cw*s)),max(2,int(ch*s))); c=c.resize(cs,Image.LANCZOS)
        shs=sh.resize((int(sh.size[0]*s),int(sh.size[1]*s)),Image.BILINEAR)
        f=Image.new("RGBA",(W,H),(0,0,0,0))
        cx=W//2; y=cy+dy
        shadow=Image.new("RGBA",shs.size,(0,0,0,255)); shadow.putalpha(shs.point(lambda v:int(v*op)))
        f.alpha_composite(shadow,(int(cx-shs.size[0]/2),int(y-shs.size[1]/2)))
        cl=c.copy(); al=np.array(cl.getchannel("A"),dtype=np.float32)*op; cl.putalpha(Image.fromarray(al.astype(np.uint8)))
        f.alpha_composite(cl,(int(cx-cs[0]/2),int(y-cs[1]/2)))
        p.stdin.write(f.tobytes())
    p.stdin.close(); p.wait()
card_clip("c1.mov","A.png",None,0.95,kb=(1.0,1.05))
card_clip("c2.mov","D.png",(0,0,816,1020),2.54,kb=(1.04,1.12),pan=(0.0,0.02))
card_clip("c3.mov","B.png",None,2.58,kb=(1.0,1.08),pan=(-0.03,0))
card_clip("c4.mov","A.png",(0,560,812,1020),2.70,cw=860,cy=760,kb=(1.0,1.10),pan=(0.04,0))
# light leak track (270x480), screen-blended later
LW,LH=270,480; EV=[7.57,9.43,44.46,49.34,52.28,30.12]; TOT=55.3; N=int(TOT*FPS)+2
yy,xx=np.mgrid[0:LH,0:LW].astype(np.float32)
p=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{LW}x{LH}","-r","30","-i","-","-c:v","libx264","-crf","10","-pix_fmt","yuv444p","leak.mp4"],stdin=subprocess.PIPE)
blank=np.zeros((LH,LW,3),np.uint8).tobytes()
for i in range(N):
    t=i/FPS; fr=None
    for k,e in enumerate(EV):
        d=t-(e-0.18)
        if 0<=d<0.5:
            a=math.sin(math.pi*d/0.5)**1.5
            sx=LW*(1.15-1.4*d/0.5) if k%2==0 else LW*(-0.15+1.4*d/0.5); sy=LH*(0.25+0.3*d/0.5)
            r=np.exp(-(((xx-sx)/(LW*0.75))**2+((yy-sy)/(LH*0.5))**2))
            col=np.array([255,150,60],np.float32)/255; core=np.array([255,235,200],np.float32)/255
            img=(r[...,None]*col*0.95+ (r**3)[...,None]*core*0.9)*a
            fr=(np.clip(img,0,1)*255).astype(np.uint8).tobytes()
    p.stdin.write(fr or blank)
p.stdin.close(); p.wait()
# end card background: blurred A with slow zoom (3 s)
im=Image.open("A.png").convert("RGB")
bg=im.resize((1080,int(1080*im.size[1]/im.size[0])),Image.LANCZOS)
c=Image.new("RGB",(1080,1920)); 
big=im.resize((int(1920*im.size[0]/im.size[1]),1920),Image.LANCZOS); c.paste(big,((1080-big.size[0])//2,0))
c=c.filter(ImageFilter.GaussianBlur(26)); c.save("endbg.png")
print("assets ok")
