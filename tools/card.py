# -*- coding: utf-8 -*-
"""card.py: the 1200 x 630 share card. python3 tools/card.py  (needs rsvg-convert, magick)"""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import art
W, H = 1200, 630
nan = art.medallion("nan"); beer = art.medallion("beer")
inner = lambda s: s[s.index(">") + 1:s.rindex("</svg>")]
s = [f'<defs><linearGradient id="k" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#B83A55"/><stop offset="1" stop-color="{art.ROSE2}"/></linearGradient></defs>',
     f'<rect width="{W}" height="{H}" fill="url(#k)"/>', art.stars(W, 380, 70, 5),
     art.trail(1110, 120, 380, 330, 6, 40, art.CREAM, .92, gap=60), art.plane(1110, 120, -16, 1.8, "#fff"),
     art.trail(1150, 300, 700, 250, 3, 5, art.CREAM, .7, gap=50), art.plane(1150, 300, 186, 1.2, "#fff"),
     art.plane(260, 90, 12, 1.0, "#fff")]
for (x, y, r) in ((90, 60, 14), (560, 70, 10), (960, 420, 12)):
    s.append(art.sparkle(x, y, r))
s.append(art.hills(W, H, 470, (art.ROSE3, "#E27F84", "#A8344B")))
s.append(f'<rect x="0" y="{H-46}" width="{W}" height="46" fill="#B23A2E"/>' + art.draw.tinchok(0, H - 46, W, 46, 64))
s.append(f'<text x="70" y="250" font-size="104" font-weight="600" fill="{art.CREAM}">Chemtrails?</text>')
s.append(f'<text x="70" y="370" font-size="120" font-weight="700" fill="#FFF">It\'s ice.</text>')
s.append(f'<text x="74" y="440" font-size="52" font-weight="600" fill="{art.WINE}" font-family="Sukhumvit Set">เคมเทรล? มันคือน้ำแข็ง</text>')
s.append(f'<text x="74" y="500" font-size="26" fill="#FFF4E6" letter-spacing="2">nanobotco.github.io/chemtrails</text>')
s.append(f'<g transform="translate(860 380) scale(.17)"><circle cx="512" cy="512" r="540" fill="#D6A42C"/>{inner(nan)}</g>')
s.append(f'<g transform="translate(1030 380) scale(.17)"><circle cx="512" cy="512" r="540" fill="#D6A42C"/>{inner(beer)}</g>')
svg = art.svg(W, H, "".join(s))
out = os.path.join(os.path.dirname(HERE), "build"); os.makedirs(out, exist_ok=True)
open(os.path.join(out, "card.svg"), "w").write(svg)
subprocess.run(["rsvg-convert", "-w", "1200", os.path.join(out, "card.svg"), "-o", os.path.join(out, "card.png")], check=True)
subprocess.run(["magick", os.path.join(out, "card.png"), "-quality", "86", os.path.join(os.path.dirname(HERE), "docs", "card.jpg")], check=True)
print("docs/card.jpg")
