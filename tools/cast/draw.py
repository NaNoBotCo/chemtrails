import math
IND="#283A6E"; IND2="#1E2C57"; RED="#B23A2E"; GOLD="#D6A42C"; CREAM="#F6EBD6"
SKIN="#E8B48C"; SKIN2="#D29870"; HAIR="#1D1A1F"; SILVER="#D9DCE3"

def diamond(cx,cy,w,h,fill,rot=0):
    return (f'<path transform="rotate({rot:.2f} {cx:.1f} {cy:.1f})" d="M{cx:.1f} {cy-h/2:.1f} L{cx+w/2:.1f} {cy:.1f} '
            f'L{cx:.1f} {cy+h/2:.1f} L{cx-w/2:.1f} {cy:.1f}Z" fill="{fill}"/>')

def tinchok(x0,y0,width,h,cell):
    """Nested-lozenge band after the tin chok hem: gold, red, cream, indigo diamonds."""
    s=[f'<rect x="{x0}" y="{y0}" width="{width}" height="{h}" fill="{RED}"/>']
    n=int(width/cell)+2; cy=y0+h/2
    for i in range(n):
        cx=x0+i*cell
        s+= [diamond(cx,cy,cell*.96,h*.86,GOLD),diamond(cx,cy,cell*.68,h*.6,IND),
             diamond(cx,cy,cell*.4,h*.34,CREAM),diamond(cx,cy,cell*.14,h*.12,RED),
             diamond(cx+cell/2,cy,cell*.18,h*.22,CREAM)]
    s.append(f'<rect x="{x0}" y="{y0}" width="{width}" height="{h*.07:.1f}" fill="{GOLD}"/>')
    s.append(f'<rect x="{x0}" y="{y0+h*.93:.1f}" width="{width}" height="{h*.07:.1f}" fill="{GOLD}"/>')
    return "".join(s)

def rose(cx,cy,R,k=5,fill=GOLD,centre=RED,rot=-90):
    """Five rounded petals: r = R(0.5 + 0.5|cos(kθ/2)|)."""
    pts=[]
    for i in range(1441):
        t=2*math.pi*i/1440; r=R*(0.5+0.5*abs(math.cos(k*t/2))**0.6); a=t+math.radians(rot)
        pts.append(f'{cx+r*math.cos(a):.1f},{cy+r*math.sin(a):.1f}')
    return (f'<polygon points="{" ".join(pts)}" fill="{fill}" stroke="#A97A12" stroke-width="{R*.04:.1f}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{R*.2:.1f}" fill="{centre}"/>')

def hills(W,base,layers):
    s=""
    for amp,fs,ph,col,op,off in layers:
        pts=[f"0,{W[1]}"]
        for x in range(0,W[0]+1,8):
            y=base+off+sum(a*math.sin(f*x+p) for a,f,p in zip(amp,fs,ph))
            pts.append(f"{x},{y:.1f}")
        pts.append(f"{W[0]},{W[1]}")
        s+=f'<polygon points="{" ".join(pts)}" fill="{col}" opacity="{op}"/>'
    return s

def mirror(d):  # mirror a list of (x,y) about x=512
    return [(1024-x,y) for x,y in d]

def beer(defs_id="b"):
    s=[]
    # back hair
    s.append(f'<path d="M512 238 C296 238 314 420 318 560 L306 836 Q512 856 718 836 L706 560 C710 420 728 238 512 238Z" fill="{HAIR}"/>')
    # neck + shadow
    s.append(f'<path d="M464 590 L464 760 L560 760 L560 590Z" fill="{SKIN}"/>')
    s.append(f'<path d="M464 620 L560 620 L560 668 Q512 694 464 668Z" fill="{SKIN2}"/>')
    # open indigo blazer, cream scoop-neck top, tin-chok trim on the front edges
    body="M112 1024 C122 872 248 782 424 752 L600 752 C776 782 902 872 912 1024Z"
    s.append(f'<path d="{body}" fill="{IND}"/>')
    s.append(f'<clipPath id="{defs_id}c"><path d="{body}"/></clipPath><g clip-path="url(#{defs_id}c)">')
    s.append(f'<path d="M112 1024 C150 900 250 830 330 810 L300 1024Z" fill="{IND2}" opacity=".55"/>')
    s.append(f'<path d="M912 1024 C874 900 774 830 694 810 L724 1024Z" fill="{IND2}" opacity=".55"/>')
    s.append('</g>')
    s.append(f'<path d="M424 752 L600 752 Q512 818 424 752Z" fill="{SKIN}"/>')
    s.append(f'<path d="M424 752 Q512 818 600 752 L578 980 L584 1024 L440 1024 L446 980Z" fill="#F5EEE2"/>')
    s.append(f'<path d="M446 980 L440 1024 L584 1024 L578 980 Q512 1000 446 980Z" fill="#E9DFCE"/>')
    lap=[(424,752),(392,768),(366,852),(390,858),(446,980)]
    for pts in (lap,mirror(lap)):
        s.append(f'<polygon points="{" ".join(f"{x},{y}" for x,y in pts)}" fill="#34487F"/>')
        (x1,y1),(x2,y2)=pts[0],pts[4]
        ang=math.degrees(math.atan2(y2-y1,x2-x1)); ln=math.hypot(x2-x1,y2-y1)
        s.append(f'<g transform="translate({x1} {y1}) rotate({ang:.2f})"><rect x="0" y="-7" width="{ln:.0f}" height="14" fill="{GOLD}"/>')
        for i in range(int(ln//16)):
            s.append(diamond(8+i*16,0,12,10,RED))
        s.append('</g>')
        s.append(f'<polyline points="{" ".join(f"{x},{y}" for x,y in pts[1:4])}" fill="none" stroke="{GOLD}" stroke-width="3"/>')
    # chest-pocket welt in tin chok
    s.append(f'<g transform="rotate(-6 660 880)"><rect x="620" y="872" width="84" height="16" fill="{GOLD}"/>')
    for i in range(5): s.append(diamond(630+i*16,880,12,11,RED))
    s.append('</g>')
    # fine gold chain with a lozenge pendant
    s.append(f'<path d="M466 708 Q470 770 512 788 Q554 770 558 708" fill="none" stroke="{GOLD}" stroke-width="2.5"/>')
    s.append(diamond(512,800,18,26,GOLD)+diamond(512,800,7,11,RED))
    # face: oval
    s.append(f'<ellipse cx="512" cy="470" rx="150" ry="186" fill="{SKIN}"/>')
    # blush
    for x in (418,606):
        s.append(f'<ellipse cx="{x}" cy="566" rx="34" ry="17" fill="#F08A8A" opacity=".38"/>')
    # eyes, catchlights, lashes
    for x,sgn in ((452,-1),(572,1)):
        s.append(f'<ellipse cx="{x}" cy="484" rx="17" ry="21" fill="#231C1B"/>')
        s.append(f'<circle cx="{x+6}" cy="476" r="6.5" fill="#fff"/><circle cx="{x-6}" cy="492" r="3" fill="#fff"/>')
        s.append(f'<path d="M{x+sgn*12} 470 l{sgn*18} -11" stroke="#231C1B" stroke-width="5" stroke-linecap="round"/>')
    # nose, smile
    s.append(f'<path d="M506 540 Q512 548 518 540" fill="none" stroke="{SKIN2}" stroke-width="5" stroke-linecap="round"/>')
    s.append(f'<path d="M466 584 Q512 596 558 584 Q552 628 512 630 Q472 628 466 584Z" fill="#8E3A3A"/>')
    s.append(f'<path d="M469 586 Q512 598 555 586 L552 602 Q512 612 472 602Z" fill="#fff"/>')
    s.append(f'<path d="M466 584 Q512 596 558 584 Q552 628 512 630 Q472 628 466 584Z" fill="none" stroke="#C7645C" stroke-width="4"/>')
    # thin metal frames: round, or octagonal (SHAPE)
    M="#B08A3E"
    for x in (448,576):
        if SHAPE=="oct":
            r=66; pts=" ".join(f"{x+r*math.cos(math.radians(22.5+45*i)):.1f},{482+r*math.sin(math.radians(22.5+45*i)):.1f}" for i in range(8))
            s.append(f'<polygon points="{pts}" fill="#ffffff" fill-opacity=".12" stroke="{M}" stroke-width="3.5" stroke-linejoin="round"/>')
        else:
            s.append(f'<circle cx="{x}" cy="482" r="64" fill="#ffffff" fill-opacity=".12" stroke="{M}" stroke-width="3.5"/>')
        s.append(f'<path d="M{x-40} 452 A48 48 0 0 1 {x-12} 432" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" opacity=".6"/>')
        s.append(f'<circle cx="{x+(-58 if x<512 else 58)}" cy="470" r="3.5" fill="{M}"/>')
    s.append(f'<path d="M508 476 Q512 462 516 476" fill="none" stroke="{M}" stroke-width="3.5"/>')
    s.append(f'<path d="M500 490 l6 -4 M524 490 l-6 -4" stroke="{M}" stroke-width="2.5"/>')
    s.append(f'<path d="M386 470 L362 466 M638 470 L662 466" stroke="{M}" stroke-width="3.5"/>')
    # side locks, straight to the shoulder
    L=[(352,330),(318,470),(306,836),(424,842),(404,700),(372,560),(364,460),(386,360)]
    for pts in (L,mirror(L)):
        (a,b,c,d,e,f,g_,h)=pts
        s.append(f'<path d="M{a[0]} {a[1]} C{b[0]} {b[1]} {b[0]} {c[1]-60} {c[0]} {c[1]} L{d[0]} {d[1]} '
                 f'C{e[0]} {e[1]} {f[0]} {f[1]} {g_[0]} {g_[1]} S{h[0]} {h[1]} {a[0]} {a[1]}Z" fill="{HAIR}"/>')
    # crown with a side part, forehead open
    s.append(f'<path d="M340 452 C326 300 420 246 512 246 C604 246 698 300 684 452 '
             f'C668 384 604 330 470 322 C420 326 356 358 340 452Z" fill="{HAIR}"/>')
    s.append('<path d="M470 322 Q466 284 480 248" fill="none" stroke="#3A3438" stroke-width="3" stroke-linecap="round"/>')
    s.append('<path d="M520 262 Q600 270 650 318" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round" opacity=".12"/>')
    for sd in (-1,1):
        X=lambda x: 512+sd*(x-512)
        s.append(f'<path d="M{X(486)} 304 C{X(446)} 318 {X(404)} 362 {X(392)} 430 L{X(399)} 431 C{X(414)} 374 {X(452)} 330 {X(496)} 308Z" fill="{HAIR}"/>')
    # gold flower pin
    s.append(rose(680,372,26))
    return "".join(s)

def profile():
    s=['<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024">',
       f'<defs><radialGradient id="bg" cx=".5" cy=".42" r=".6"><stop offset="0" stop-color="#FBF3E4"/><stop offset="1" stop-color="#EFD9B4"/></radialGradient></defs>',
       '<rect width="1024" height="1024" fill="url(#bg)"/>']
    # polar ring of lozenges inside the circular crop
    for R,n,w,h,col in ((478,40,30,44,IND),(478,40,14,20,GOLD),(440,80,8,8,RED)):
        for i in range(n):
            t=2*math.pi*i/n; cx=512+R*math.cos(t); cy=512+R*math.sin(t)
            s.append(diamond(cx,cy,w,h,col,math.degrees(t)+90))
    s.append('<g transform="translate(512 640) scale(1.16) translate(-512 -640)">'+beer("p")+"</g>"); s.append('</svg>')
    return "".join(s)

def cover():
    W,H=1640,624
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
       f'<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1B284F"/><stop offset="1" stop-color="{IND}"/></linearGradient></defs>',
       f'<rect width="{W}" height="{H}" fill="url(#sky)"/>']
    # Doi Suthep-ish ridgelines as sums of sines
    s.append(hills((W,H),400,[
        ((46,22,12),(.0031,.0083,.019),(0.6,2.1,.4),"#3B4E86",.55,-70),
        ((38,18,9),(.0042,.011,.023),(2.2,.3,1.7),"#31447A",.8,-20),
        ((28,14,7),(.0052,.013,.031),(4.0,1.2,.9),"#263665",1,30)]))
    # moon + stars from a fixed seed
    s.append(f'<circle cx="1470" cy="118" r="46" fill="{CREAM}" opacity=".95"/>')
    import random; rnd=random.Random(9)
    for _ in range(70):
        x,y=rnd.uniform(0,W),rnd.uniform(0,300); s.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.uniform(.8,2.2):.1f}" fill="#fff" opacity="{rnd.uniform(.3,.8):.2f}"/>')
    s.append(tinchok(0,H-92,W,92,64))
    cx=900
    s.append(rose(cx,118,30))
    s.append(f'<text x="{cx}" y="248" text-anchor="middle" font-family="Avenir Next" font-weight="600" font-size="112" fill="{CREAM}" letter-spacing="2">Beer</text>')
    s.append(f'<text x="{cx}" y="318" text-anchor="middle" font-family="Sukhumvit Set" font-weight="600" font-size="54" fill="{GOLD}">เบียร์</text>')
    s.append(f'<rect x="{cx-150}" y="344" width="300" height="3" fill="{GOLD}" opacity=".8"/>')
    s.append(f'<text x="{cx}" y="398" text-anchor="middle" font-family="Avenir Next" font-weight="500" font-size="36" fill="{CREAM}" letter-spacing="7">OPERATIONS COORDINATOR</text>')
    s.append(f'<text x="{cx}" y="448" text-anchor="middle" font-family="Sukhumvit Set" font-size="34" fill="{CREAM}" opacity=".9">ผู้ประสานงานฝ่ายปฏิบัติการ</text>')
    s.append('</svg>')
    return "".join(s)

SHAPE="round"
if __name__=="__main__":
    import sys
    SHAPE=sys.argv[1] if len(sys.argv)>1 else "round"
    open(f"beer-fb-profile-{SHAPE}.svg","w").write(profile())
    open("beer-fb-cover.svg","w").write(cover())
