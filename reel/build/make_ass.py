import json, math
W=json.load(open("../words_roman.json"))
SEG=[(0.00,44.46,0.00),(50.14,55.02,44.46),(56.60,59.54,49.34)]
END=52.28; TOTAL=55.28
def o(t):
    for a,b,off in SEG:
        if a-0.001<=t<b-0.005: return t-a+off
    return None
KEY={"zyada","comments","kon","hospital","hospital?","misbah","noor","thokar","niaz","baig","dogar","sajji","dr.","hina","ahmed.","bohat","achay","24","ghante","walk","khud","khana","pain","100%","recommended","recommended,","staff","cooperative","private","munasib","doctor","zaroor","contact","operation","normal","try","batati","located","ali","town"}
def iskey(w): return w.lower().strip(",.?") in {k.strip(",.?") for k in KEY}
def ts(t):
    t=max(t,0); cs=int(round(t*100)); return f"{cs//360000}:{cs//6000%60:02d}:{cs//100%60:02d}.{cs%100:02d}"
ws=[]
for w in W:
    s=o(w['s']); e=o(min(w['e'],w['s']+1.0)-0.01)
    if s is None: continue
    if e is None or e<s: e=s+0.25
    ws.append(dict(s=s,e=e,w=w['w']))
# groups
groups=[];cur=[];budget=0
for i,w in enumerate(ws):
    c=len(w['w'])*(1.9 if iskey(w['w']) else 1.0)
    gap = cur and (w['s']-cur[-1]['e']>0.35)
    seg_break = cur and any(abs(w['s']-off)<0.02 for _,_,off in SEG[1:])
    if cur and (len(cur)>=4 or budget+c>30 or gap or seg_break):
        groups.append(cur);cur=[];budget=0
    cur.append(w);budget+=c+1
    if w["w"][-1] in ".?," and w["w"]!="Dr.": groups.append(cur);cur=[];budget=0
if cur: groups.append(cur)
hdr="""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Inter Black,60,&H00FFFFFF,&H00FFFFFF,&H00120D00,&H8C000000,0,0,0,0,100,100,0,0,1,0,5,2,80,80,0
Style: Chip,Inter SemiBold,40,&H00FFFFFF,&H00FFFFFF,&H50140C08,&H50140C08,0,0,0,0,100,100,0,0,3,20,0,5,40,40,0
Style: G,Inter Black,60,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0
Style: T,Inter Black,60,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,0,4,5,40,40,0
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
YEL="&H1ED2FF&"
ev=[]
POP="\\fscx55\\fscy55\\t(0,110,\\fscx110\\fscy110)\\t(110,190,\\fscx100\\fscy100)"
def fmt(w,new):
    t=w['w'].upper()
    if iskey(w['w']):
        base="{\\fs112\\c"+YEL+"\\bord4\\3c&H001A12&\\blur0.6"
    else:
        base="{\\fs60\\c&HFFFFFF&\\bord0"
    return base+(POP if new else "")+"}"+t+"{\\r}"
for gi,g in enumerate(groups):
    gend=min(g[-1]['e']+0.25, groups[gi+1][0]['s'] if gi+1<len(groups) else g[-1]['e']+0.4)
    gend=min(gend,END)
    for k,w in enumerate(g):
        st=w['s']; en=g[k+1]['s'] if k+1<len(g) else gend
        if en<=st: en=st+0.05
        txt="{\\fs60}\\h \\h".join(fmt(x,x is w) for x in g[:k+1])
        # invisible remainder keeps layout stable
        rest="\\h \\h".join("{\\alpha&HFF&"+("\\fs112" if iskey(x['w']) else "\\fs60")+"}"+x['w'].upper() for x in g[k+1:])
        ev.append(f"Dialogue: 5,{ts(st)},{ts(en)},Cap,,0,0,0,,{{\\an2\\pos(540,1370)}}{txt} {rest}".rstrip())
def chip(a,b,text,y=1600):
    ev.append(f"Dialogue: 4,{ts(a)},{ts(b)},Chip,,0,0,0,,{{\\an5\\move(540,{y+40},540,{y},0,260)\\fad(220,180)}}{{\\fnDejaVu Sans\\c{YEL}}}●{{\\r\\fnInter SemiBold}}  {text}")
chip(9.50,11.10,"Ali Town ke paas · Thokar Niaz Baig, Lahore")
chip(12.05,14.95,"Dogar Sajji wali line mein")
# lower third Dr.
ev.append(f"Dialogue: 4,{ts(17.45)},{ts(18.86)},G,,0,0,0,,{{\\an7\\pos(110,1545)\\c{YEL}\\bord0\\fad(150,120)\\clip(110,1545,122,1690)\\p1}}m 0 0 l 12 0 12 140 0 140{{\\p0}}")
ev.append(f"Dialogue: 4,{ts(17.45)},{ts(18.86)},T,,0,0,0,,{{\\an7\\move(90,1548,145,1548,0,260)\\fs66\\fad(150,120)}}DR. HINA AHMED")
ev.append(f"Dialogue: 4,{ts(17.55)},{ts(18.86)},T,,0,0,0,,{{\\an7\\move(90,1628,145,1628,0,260)\\fs38\\fnInter SemiBold\\c&HE6E6E6&\\fad(150,120)}}Meri doctor")
# ring counter 24 ghante
cx,cy,R1,R2=540,1610,108,94
def ring(frac):
    n=max(2,int(72*frac)); pts=[]
    for i in range(n+1):
        a=-math.pi/2+2*math.pi*frac*i/n; pts.append((cx+R1*math.cos(a),cy+R1*math.sin(a)))
    for i in range(n,-1,-1):
        a=-math.pi/2+2*math.pi*frac*i/n; pts.append((cx+R2*math.cos(a),cy+R2*math.sin(a)))
    return "m "+" l ".join(f"{x:.0f} {y:.0f}" for x,y in pts)
a0=21.45; b0=24.28
ev.append(f"Dialogue: 3,{ts(a0)},{ts(b0)},G,,0,0,0,,{{\\an7\\pos(0,0)\\c&HFFFFFF&\\alpha&HB0&\\fad(150,150)\\p1}}{ring(0.9999)}{{\\p0}}")
ev.append(f"Dialogue: 3,{ts(a0)},{ts(b0)},G,,0,0,0,,{{\\an7\\pos(0,0)\\c&H2A1E18&\\alpha&H60&\\fad(150,150)\\p1}}m {cx-R2} {cy} b {cx-R2} {cy-R2*1.33} {cx+R2} {cy-R2*1.33} {cx+R2} {cy} b {cx+R2} {cy+R2*1.33} {cx-R2} {cy+R2*1.33} {cx-R2} {cy}{{\\p0}}")
steps=24
for i in range(steps):
    t1=a0+0.85*i/steps; t2=a0+0.85*(i+1)/steps if i<steps-1 else b0
    fr=(i+1)/steps
    ev.append(f"Dialogue: 4,{ts(t1)},{ts(t2)},G,,0,0,0,,{{\\an7\\pos(0,0)\\c{YEL}\\p1}}{ring(fr if fr<1 else 0.9999)}{{\\p0}}")
    ev.append(f"Dialogue: 4,{ts(t1)},{ts(t2)},T,,0,0,0,,{{\\an5\\pos({cx},{cy-12})\\fs84}}{i+1}")
ev.append(f"Dialogue: 4,{ts(a0)},{ts(b0)},T,,0,0,0,,{{\\an5\\pos({cx},{cy+46})\\fs24\\fnInter Bold\\fsp3\\fad(200,150)}}GHANTE")
# check badge
bx,by,r=540,1610,62
ev.append(f"Dialogue: 4,{ts(31.62)},{ts(32.70)},G,,0,0,0,,{{\\an7\\pos(0,0)\\c&H5BC24A&\\fad(80,150)\\org({bx},{by})\\fscx40\\fscy40\\t(0,160,\\fscx110\\fscy110)\\t(160,260,\\fscx100\\fscy100)\\p1}}m {bx-r} {by} b {bx-r} {by-r*1.33} {bx+r} {by-r*1.33} {bx+r} {by} b {bx+r} {by+r*1.33} {bx-r} {by+r*1.33} {bx-r} {by}{{\\p0}}")
ev.append(f"Dialogue: 5,{ts(31.70)},{ts(32.70)},G,,0,0,0,,{{\\an7\\pos(0,0)\\c&HFFFFFF&\\fad(60,150)\\p1}}m {bx-30} {by+2} l {bx-12} {by+20} l {bx+30} {by-22} l {bx+38} {by-14} l {bx-12} {by+36} l {bx-38} {by+10}{{\\p0}}")
# end card
E0=END
ev.append(f"Dialogue: 6,{ts(E0)},{ts(TOTAL)},G,,0,0,0,,{{\\an7\\pos(0,0)\\c&H1A120B&\\alpha&H48&\\fad(300,0)\\p1}}m 0 0 l 1080 0 1080 1920 0 1920{{\\p0}}")
def et(a,y,txt,extra):
    ev.append(f"Dialogue: 7,{ts(a)},{ts(TOTAL)},T,,0,0,0,,{{\\an5\\move(540,{y+30},540,{y},0,320)\\fad(260,0){extra}}}{txt}")
et(E0+0.15,640,"Normal Delivery  •  Operation","\\fs40\\fnInter SemiBold\\c&HE6E6E6&")
et(E0+0.30,790,"MISBAH NOOR","\\fs124\\c"+YEL+"\\bord3\\3c&H001A12&")
et(E0+0.42,915,"MEDICAL COMPLEX","\\fs78")
ev.append(f"Dialogue: 7,{ts(E0+0.6)},{ts(TOTAL)},G,,0,0,0,,{{\\an7\\pos(0,0)\\c{YEL}\\fad(250,0)\\p1}}m 440 1000 l 640 1000 640 1006 440 1006{{\\p0}}")
et(E0+0.70,1090,"Ali Town ke paas, Thokar Niaz Baig, Lahore","\\fs44\\fnInter SemiBold")
et(E0+0.85,1165,"Dogar Sajji wali line mein","\\fs44\\fnInter SemiBold\\c&HD0D0D0&")
et(E0+1.10,1330,"Aaj hi contact karein","\\fs54\\c"+YEL)
open("captions.ass","w").write(hdr+"\n".join(ev)+"\n")
json.dump(groups,open("groups.json","w"),indent=0)
print(len(groups),"groups",len(ev),"events")
for g in groups[:12]: print(f"{g[0]['s']:.2f}", " ".join(x['w'] for x in g))
