import math, random
from draw import diamond, tinchok, rose, hills, GOLD, CREAM

WINE="#6E1020"; BLOOD="#9E1B2C"; RED="#B7243A"; DEEP="#2A0610"; BLACK="#1B1618"
SKIN="#E6AE86"; SKIN2="#CF9068"; LIP="#A81E34"
SIL="#65463A"; SIL2="#46302A"; SIL3="#DDD4C2"

def P(pts): return " ".join(f"{x:.1f},{y:.1f}" for x,y in pts)

def moon(cx,cy,r,phi,lit=CREAM,dark="#000",dop=.25):
    k=math.cos(phi); rx=abs(k)*r; wax=(phi%(2*math.pi))<math.pi
    if wax: outer,term=1,(0 if k>0 else 1)
    else:   outer,term=0,(1 if k>0 else 0)
    return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{dark}" opacity="{dop}"/>'
            f'<path d="M{cx:.1f} {cy-r:.1f} A{r} {r} 0 0 {outer} {cx:.1f} {cy+r:.1f} A{rx:.2f} {r} 0 0 {term} {cx:.1f} {cy-r:.1f}Z" fill="{lit}"/>')

def sparkle(cx,cy,r,col=CREAM,op=1):
    pts=[]
    for i in range(8):
        a=math.pi/4*i; rr=r if i%2==0 else r*.28
        pts.append((cx+rr*math.cos(a-math.pi/2),cy+rr*math.sin(a-math.pi/2)))
    return f'<polygon points="{P(pts)}" fill="{col}" opacity="{op}"/>'

def edge(side,y,phase=0):
    """Outer edge of the long hair: widens as it falls, with a slow wave."""
    t=(y-380)
    return 512+side*(232+0.16*t+12*math.sin(t/50+phase)+2*math.sin(t/13+phase*2))

def nan():
    s=[]
    # long silver hair, back layer
    ys=list(range(382,1041,10))
    crown=[(512+232*math.cos(a),382-194*math.sin(a)) for a in [math.pi*i/60 for i in range(61)]]
    right=[(edge(1,y,1.3),y) for y in ys]
    bottom=[(x,1030+10*math.sin(x/30)) for x in range(int(edge(-1,1040)),int(edge(1,1040)),12)]
    s.append(f'<polygon points="{P(crown[::-1]+right+bottom[::-1]+[(edge(-1,y),y) for y in ys[::-1]])}" fill="{SIL2}"/>')
    # neck
    s.append(f'<path d="M468 590 L468 770 L556 770 L556 590Z" fill="{SKIN}"/>')
    s.append(f'<path d="M468 610 L556 610 L556 652 Q512 676 468 652Z" fill="{SKIN2}"/>')
    # black blouse, V-neck with red piping, cream embroidery
    body="M104 1024 C116 870 250 784 430 756 L594 756 C774 784 908 870 920 1024Z"
    s.append(f'<path d="{body}" fill="{BLACK}"/>')
    s.append(f'<clipPath id="nb"><path d="{body}"/></clipPath><g clip-path="url(#nb)">')
    rnd=random.Random(4)
    for (x,y,R) in ((470,960,30),(566,1000,24)):
        s.append(rose(x,y,R,fill=CREAM,centre="#E9D9B8",rot=rnd.uniform(0,72)))
        for j in range(2):
            a=rnd.uniform(0,6.28); d=R*1.35
            s.append(f'<ellipse cx="{x+d*math.cos(a):.0f}" cy="{y+d*math.sin(a):.0f}" rx="{R*.36:.0f}" ry="{R*.14:.0f}" transform="rotate({math.degrees(a):.0f} {x+d*math.cos(a):.0f} {y+d*math.sin(a):.0f})" fill="{CREAM}" opacity=".85"/>')
    s.append('</g>')
    s.append(f'<path d="M430 756 L512 900 L594 756Z" fill="{SKIN}"/>')
    s.append(f'<path d="M430 756 L512 900 L594 756" fill="none" stroke="{RED}" stroke-width="7" stroke-linejoin="round"/>')
    # red shawl over the shoulders, tin chok hem on its inner edge
    for side in (-1,1):
        X=lambda x: 512+side*(x-512)
        sh=[(X(104),1024),(X(116),940),(X(200),830),(X(330),782),(X(440),760),(X(320),1024)]
        s.append(f'<polygon points="{P(sh)}" fill="{BLOOD}"/>')
        x1,y1,x2,y2=X(440),760,X(320),1024
        ang=math.degrees(math.atan2(y2-y1,x2-x1)); ln=math.hypot(x2-x1,y2-y1)
        s.append(f'<g transform="translate({x1} {y1}) rotate({ang:.2f})"><rect x="0" y="-11" width="{ln:.0f}" height="22" fill="{GOLD}"/>'
                 + "".join(diamond(10+i*20,0,16,16,DEEP)+diamond(10+i*20,0,6,6,GOLD) for i in range(int(ln//20))) + '</g>')
    # three strands of orange beads
    for d,n in ((0,22),(30,26),(60,30)):
        for i in range(n+1):
            t=i/n; x=(1-t)**2*474+2*(1-t)*t*512+t*t*550; y=(1-t)**2*730+2*(1-t)*t*(840+d*2)+t*t*730
            s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="#E2582A" stroke="#B8401C" stroke-width="1"/>')
    # face: long oval, soft jaw
    s.append(f'<path d="M372 430 C372 300 440 262 512 262 C584 262 652 300 652 430 C652 546 600 640 512 640 C424 640 372 546 372 430Z" fill="{SKIN}"/>')
    for x in (410,614):
        s.append(f'<ellipse cx="{x}" cy="512" rx="36" ry="18" fill="#E0736E" opacity=".35"/>')
    # eyes: dark ovals, catchlights, long lashes
    for x,sg in ((458,-1),(566,1)):
        s.append(f'<ellipse cx="{x}" cy="448" rx="17" ry="21" fill="#2A1C18"/>')
        s.append(f'<circle cx="{x+6}" cy="440" r="6.5" fill="#fff"/><circle cx="{x-6}" cy="456" r="3" fill="#fff"/>')
        for i,(dx,dy,lx,ly) in enumerate(((12,-16,20,-20),(16,-8,28,-14),(17,2,30,-2))):
            s.append(f'<path d="M{x+sg*dx} {448+dy} q{sg*lx*.4:.0f} {ly*.2:.0f} {sg*lx} {ly}" fill="none" stroke="#2A1C18" stroke-width="4" stroke-linecap="round"/>')
        s.append(f'<path d="M{x-28} 404 Q{x} 390 {x+28} 402" fill="none" stroke="#5A3C2C" stroke-width="6" stroke-linecap="round"/>')
    s.append(f'<path d="M506 500 Q512 512 520 504" fill="none" stroke="{SKIN2}" stroke-width="5" stroke-linecap="round"/>')
    # big smile, gold second bicuspid
    mouth="M444 550 Q512 562 580 550 Q572 610 512 614 Q452 610 444 550Z"
    s.append(f'<clipPath id="m"><path d="{mouth}"/></clipPath><path d="{mouth}" fill="#7A2230"/>')
    teeth=[]; x=512; widths=[12,11,10,9,9,8]
    for side in (-1,1):
        x=512
        for n,w in enumerate(widths):
            cx=x+side*w/2; x+=side*w
            teeth.append((cx,w,n,side))
    g=['<g clip-path="url(#m)">']
    for cx,w,n,side in teeth:
        top=551+6*(1-min(1,((cx-512)/68)**2))
        col="#E8B32E" if (n==4 and side==1) else "#FBF8F2"
        g.append(f'<rect x="{cx-w/2+1:.1f}" y="{top-4:.1f}" width="{w-2:.1f}" height="{24-2*n:.1f}" rx="4" fill="{col}"/>')
        if n==4 and side==1:
            g.append(f'<rect x="{cx-w/2+3:.1f}" y="{top:.1f}" width="3" height="10" rx="1.5" fill="#fff" opacity=".7"/>')
    g.append('<ellipse cx="512" cy="600" rx="30" ry="9" fill="#E07A86"/></g>')
    s+=g
    s.append(f'<path d="{mouth}" fill="none" stroke="{LIP}" stroke-width="5" stroke-linejoin="round"/>')
    s.append(sparkle(594,538,11,GOLD))
    # front locks: long, wavy, falling over the shoulders
    for side,ph in ((-1,0),(1,1.3)):
        ys2=list(range(350,1041,10))
        outer=[(edge(side,y,ph),y) for y in ys2]
        inner=[(512+side*(138+0.14*max(0,y-400)+6*math.sin((y-400)/50+ph+1)*min(1,max(0,y-400)/120)),y) for y in ys2]
        s.append(f'<polygon points="{P(outer+inner[::-1])}" fill="{SIL}"/>')
        for k in (0.35,0.84):
            line=[(o[0]*(1-k)+i[0]*k+4*math.sin(o[1]/50+k*5),o[1]) for o,i in zip(outer,inner)]
            s.append(f'<polyline points="{P(line)}" fill="none" stroke="{SIL3}" stroke-width="{7 if k<.5 else 16}" stroke-linecap="round" opacity=".9"/>')
    # centre part, big crown
    s.append(f'<path d="M300 490 C284 280 388 186 512 186 C636 186 740 280 724 490 '
             f'C704 372 616 300 512 298 C408 300 320 372 300 490Z" fill="{SIL}"/>')
    s.append(f'<path d="M512 298 L512 196" stroke="{SIL2}" stroke-width="4" stroke-linecap="round"/>')
    for side in (-1,1):
        X=lambda x: 512+side*(x-512)
        s.append(f'<path d="M{X(500)} 210 C{X(430)} 220 {X(360)} 290 {X(336)} 420" fill="none" stroke="{SIL3}" stroke-width="8" stroke-linecap="round" opacity=".9"/>')
        s.append(f'<path d="M{X(490)} 250 C{X(440)} 270 {X(392)} 320 {X(372)} 380" fill="none" stroke="{SIL3}" stroke-width="5" stroke-linecap="round" opacity=".7"/>')
    # feather tucked above the ear
    s.append('<g transform="rotate(28 700 330)">'
             '<path d="M700 250 C736 290 736 370 700 420 C664 370 664 290 700 250Z" fill="#E7507A"/>'
             '<path d="M700 262 L700 440" stroke="#F7E7C8" stroke-width="4" stroke-linecap="round"/>'
             + "".join(f'<path d="M700 {290+i*22} l{d*20} -12" stroke="#F7A1B8" stroke-width="3" stroke-linecap="round"/>' for i in range(5) for d in (-1,1))
             + '</g>')
    # small gold drops with a red bead
    for x in (382,642):
        s.append(f'<circle cx="{x}" cy="500" r="4" fill="{GOLD}"/><line x1="{x}" y1="504" x2="{x}" y2="528" stroke="{GOLD}" stroke-width="2"/>')
        s.append(diamond(x,536,12,16,GOLD)+f'<circle cx="{x}" cy="556" r="8" fill="{RED}"/>')
    return "".join(s)

def wand():
    """Action camera on a pole, held up like a wand."""
    s=[]
    s.append(f'<path d="M60 1024 C100 960 170 900 214 872 L292 930 C250 960 200 1000 180 1024Z" fill="{BLOOD}"/>')
    s.append(f'<line x1="250" y1="880" x2="190" y2="330" stroke="{GOLD}" stroke-width="14" stroke-linecap="round"/>')
    s.append(f'<line x1="246" y1="876" x2="188" y2="340" stroke="#F3D27A" stroke-width="4" stroke-linecap="round"/>')
    s.append(f'<g transform="rotate(-8 252 880)"><rect x="210" y="846" width="84" height="70" rx="32" fill="{SKIN}"/>'
             + "".join(f'<path d="M232 {866+i*16} L280 {866+i*16}" stroke="{SKIN2}" stroke-width="3" stroke-linecap="round"/>' for i in range(3))
             + f'<ellipse cx="224" cy="858" rx="16" ry="22" fill="{SKIN}" stroke="{SKIN2}" stroke-width="3"/></g>')
    s.append(f'<g transform="rotate(-8 190 250)">'
             f'<rect x="100" y="186" width="180" height="136" rx="30" fill="{CREAM}" stroke="#2A1C18" stroke-width="6"/>'
             f'<rect x="124" y="170" width="44" height="24" rx="8" fill="{RED}" stroke="#2A1C18" stroke-width="5"/>'
             f'<circle cx="190" cy="258" r="46" fill="#2A1C18"/><circle cx="190" cy="258" r="32" fill="#3E5C9A"/>'
             f'<circle cx="190" cy="258" r="16" fill="#1B2440"/><circle cx="176" cy="242" r="9" fill="#fff" opacity=".85"/>'
             f'<circle cx="252" cy="208" r="8" fill="{RED}"/></g>')
    for (x,y,r,o) in ((84,150,24,1),(318,160,16,1),(72,360,12,.9)):
        s.append(sparkle(x,y,r,GOLD,o))
    return "".join(s)

def profile():
    s=['<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024">',
       f'<defs><radialGradient id="bg" cx=".5" cy=".42" r=".62"><stop offset="0" stop-color="#F6B8B4"/><stop offset=".65" stop-color="#E97C80"/><stop offset="1" stop-color="#C9485A"/></radialGradient></defs>',
       '<rect width="1024" height="1024" fill="url(#bg)"/>']
    n=12
    for i in range(n):
        t=-math.pi/2+2*math.pi*i/n; cx=512+470*math.cos(t); cy=512+470*math.sin(t)
        s.append(moon(cx,cy,15,2*math.pi*i/n+.01,CREAM,CREAM,.35))
    s.append('<g transform="translate(512 640) scale(1.1) translate(-512 -640)">'+nan()+'</g>')
    s.append(wand())
    s.append('</svg>'); return "".join(s)

def cover():
    W,H=1640,624
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
       f'<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#C9485A"/><stop offset="1" stop-color="#EE9496"/></linearGradient></defs>',
       f'<rect width="{W}" height="{H}" fill="url(#sky)"/>']
    s.append(hills((W,H),455,[
        ((46,22,12),(.0031,.0083,.019),(0.6,2.1,.4),"#F4B3B0",.5,-70),
        ((38,18,9),(.0042,.011,.023),(2.2,.3,1.7),"#E27F84",.8,-20),
        ((28,14,7),(.0052,.013,.031),(4.0,1.2,.9),"#C9485A",1,30)]))
    rnd=random.Random(11)
    for _ in range(80):
        x,y=rnd.uniform(0,W),rnd.uniform(0,320); s.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.uniform(.8,2.2):.1f}" fill="#fff" opacity="{rnd.uniform(.3,.8):.2f}"/>')
    for (x,y,r) in ((300,120,14),(1400,90,18),(1520,250,10),(620,70,9),(1180,300,8)):
        s.append(sparkle(x,y,r,GOLD,.9))
    # a row of moon phases above the name
    cx=900
    for i in range(9):
        s.append(moon(cx-240+i*60,96,16,2*math.pi*i/8+.01,CREAM,CREAM,.35))
    s.append(tinchok(0,H-92,W,92,64).replace('#283A6E',DEEP).replace('#B23A2E',BLOOD))
    s.append(f'<text x="{cx}" y="262" text-anchor="middle" font-family="Avenir Next" font-weight="600" font-size="120" fill="{CREAM}" letter-spacing="3">NaN</text>')
    s.append(f'<text x="{cx}" y="336" text-anchor="middle" font-family="Sukhumvit Set" font-weight="600" font-size="56" fill="#7A1A2C">แนน</text>')
    s.append(f'<rect x="{cx-150}" y="364" width="300" height="3" fill="#7A1A2C" opacity=".6"/>')
    s.append('</svg>'); return "".join(s)

if __name__=="__main__":
    open("nan-fb-profile.svg","w").write(profile())
    open("nan-fb-cover.svg","w").write(cover())
