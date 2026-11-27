def ts(t):
    cs=int(round(t*100)); return f"{cs//360000}:{cs//6000%60:02d}:{cs//100%60:02d}.{cs%100:02d}"
def rr(x,y,w,h,r):
    k=0.5523*r
    return (f"m {x+r} {y} l {x+w-r} {y} b {x+w-r+k} {y} {x+w} {y+r-k} {x+w} {y+r} l {x+w} {y+h-r} "
            f"b {x+w} {y+h-r+k} {x+w-r+k} {y+h} {x+w-r} {y+h} l {x+r} {y+h} b {x+r-k} {y+h} {x} {y+h-r+k} {x} {y+h-r} "
            f"l {x} {y+r} b {x} {y+r-k} {x+r-k} {y} {x+r} {y}")
def circ(cx,cy,r): return rr(cx-r,cy-r,2*r,2*r,r)
def check(cx,cy,s=1.0):
    p=[(-17,1),(-6,12),(17,-12),(22,-7),(-6,21),(-22,6)]
    return "m "+" l ".join(f"{cx+a*s:.0f} {cy+b*s:.0f}" for a,b in p)
ev=[]
POPIN="\\fscx70\\fscy70\\t(0,140,\\fscx104\\fscy104)\\t(140,220,\\fscx100\\fscy100)"
def panel(a,b,x,y,w,h,layer=8):
    o=f"\\org({x+w//2},{y+h//2})"
    ev.append(f"Dialogue: {layer},{ts(a)},{ts(b)},G,,0,0,0,,{{\\an7\\pos(0,8)\\c&H000000&\\alpha&H90&\\blur12\\fad(150,150){o}{POPIN}\\p1}}{rr(x,y,w,h,44)}{{\\p0}}")
    ev.append(f"Dialogue: {layer},{ts(a)},{ts(b)},G,,0,0,0,,{{\\an7\\pos(0,0)\\c&HF7F5F3&\\alpha&H0A&\\fad(150,150){o}{POPIN}\\p1}}{rr(x,y,w,h,44)}{{\\p0}}")
def header(a,b,x,y,text,layer=9):
    ev.append(f"Dialogue: {layer},{ts(a)},{ts(b)},T,,0,0,0,,{{\\an4\\pos({x},{y})\\fnInter Bold\\fs34\\fsp4\\c&H8A8580&\\shad0\\fad(200,150)}}{text}")
def row(a,b,x,y,text,layer=9):
    ev.append(f"Dialogue: {layer},{ts(a)},{ts(b)},G,,0,0,0,,{{\\an7\\pos(0,0)\\c&H5BC24A&\\fad(60,150)\\org({x},{y})\\fscx30\\fscy30\\t(0,140,\\fscx112\\fscy112)\\t(140,220,\\fscx100\\fscy100)\\p1}}{circ(x,y,30)}{{\\p0}}")
    ev.append(f"Dialogue: {layer+1},{ts(a+0.05)},{ts(b)},G,,0,0,0,,{{\\an7\\pos(0,0)\\c&HFFFFFF&\\fad(60,150)\\p1}}{check(x,y,0.9)}{{\\p0}}")
    ev.append(f"Dialogue: {layer},{ts(a)},{ts(b)},T,,0,0,0,,{{\\an4\\move({x+70},{y},{x+56},{y},0,200)\\fnInter Black\\fs60\\c&H1A1816&\\shad0\\fad(120,150)}}{text}")
# 1) recovery checklist  24.28-30.12
A,B=24.28,30.05
panel(A,B,150,520,780,560); header(A+0.05,B,215,600,"24 GHANTE BAAD")
for t,txt,y in [(24.42,"Walk khud",700),(25.78,"Khana khud",810),(26.94,"Sab kuch khud",920),(28.78,"Koi pain nahi",1030)]:
    row(t,B,240,y,txt)
# 2) affordable  34.90-40.56
A,B=34.92,40.50
panel(A,B,150,600,780,400); header(A+0.05,B,215,680,"SAB SE ACHI CHEEZ")
row(36.30,B,240,790,"Private hospital"); row(39.24,B,240,900,"Kharcha munasib")
# 3) operation / normal 47.6-49.34
A,B=47.62,49.30
for t,txt,y in [(47.70,"Operation",760),(48.52,"Normal Delivery",890)]:
    w=620; x=(1080-w)//2
    o=f"\\org(540,{y})"
    ev.append(f"Dialogue: 8,{ts(t)},{ts(B)},G,,0,0,0,,{{\\an7\\pos(0,0)\\c&HF7F5F3&\\fad(80,150){o}\\fscx60\\fscy60\\t(0,150,\\fscx106\\fscy106)\\t(150,230,\\fscx100\\fscy100)\\p1}}{rr(x,y-52,w,104,52)}{{\\p0}}")
    ev.append(f"Dialogue: 9,{ts(t)},{ts(B)},G,,0,0,0,,{{\\an7\\pos(0,0)\\c&H5BC24A&\\fad(80,150){o}\\fscx60\\fscy60\\t(0,150,\\fscx106\\fscy106)\\t(150,230,\\fscx100\\fscy100)\\p1}}{circ(x+60,y,30)}{{\\p0}}")
    ev.append(f"Dialogue: 10,{ts(t+0.05)},{ts(B)},G,,0,0,0,,{{\\an7\\pos(0,0)\\c&HFFFFFF&\\fad(80,150)\\p1}}{check(x+60,y,0.9)}{{\\p0}}")
    ev.append(f"Dialogue: 9,{ts(t)},{ts(B)},T,,0,0,0,,{{\\an4\\pos({x+115},{y})\\fnInter Black\\fs56\\c&H1A1816&\\shad0\\fad(80,150){o}\\fscx60\\fscy60\\t(0,150,\\fscx106\\fscy106)\\t(150,230,\\fscx100\\fscy100)}}{text if False else txt}")
open("captions.ass","a").write("\n".join(ev)+"\n")
print(len(ev),"gfx events")
