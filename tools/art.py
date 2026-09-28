# -*- coding: utf-8 -*-
"""art.py: the flat pictures, drawn from sums of sines and the trail physics.

Same kit as the NaN and Beer Facebook covers (tools/cast/): rose and indigo skies,
ridgelines as sums of sines, gold four-point sparkles, the tin chok lozenge band.
    python3 tools/art.py      # writes docs/img/*.svg
"""
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "cast"))
import draw  # noqa: E402  Beer, and the shared kit
import nan  # noqa: E402
from physics import e_water, e_ice, slope, threshold, t_tangent, ice_density, facts  # noqa: E402

IMG = os.path.join(os.path.dirname(HERE), "docs", "img")
IND, IND2, RED, GOLD, CREAM = draw.IND, draw.IND2, draw.RED, draw.GOLD, draw.CREAM
ROSE, ROSE2, ROSE3, WINE = "#C9485A", "#EE9496", "#F4B3B0", "#7A1A2C"


def P(pts):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)


def sparkle(cx, cy, r, col=GOLD, op=1):
    return nan.sparkle(cx, cy, r, col, op)


FONT = "font-family=\"'Avenir Next',Avenir,'Sukhumvit Set',Thonburi,'Segoe UI',system-ui,sans-serif\""


def svg(w, h, body, extra=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" {FONT}{extra}>'
            + body + "</svg>")


def tinchok_tile():
    """One repeat of the band, 64 x 46, for a CSS repeat-x background."""
    s = draw.tinchok(-32, 0, 128, 46, 64)
    return svg(64, 46, s, ' preserveAspectRatio="none"')


def medallion(who):
    """The Facebook profile, circle-cropped."""
    body = (nan.profile() if who == "nan" else draw.profile())
    inner = body[body.index(">") + 1:body.rindex("</svg>")]
    return svg(1024, 1024, f'<defs><clipPath id="o{who}"><circle cx="512" cy="512" r="512"/></clipPath></defs>'
               f'<g clip-path="url(#o{who})">{inner}</g>')


def plane(x, y, ang, s=1.0, col=CREAM):
    """A flat airliner seen from below, nose along +x before rotating."""
    body = (f'<g transform="translate({x:.1f} {y:.1f}) rotate({ang:.1f}) scale({s:.3f})">'
            f'<path d="M-30 -3.5 L22 -3.5 Q34 0 22 3.5 L-30 3.5 Q-34 0 -30 -3.5Z" fill="{col}"/>'
            f'<path d="M2 -3 L-12 -30 L-18 -30 L-10 -3Z M2 3 L-12 30 L-18 30 L-10 3Z" fill="{col}"/>'
            f'<path d="M-24 -2 L-32 -12 L-35 -12 L-31 -2Z M-24 2 L-32 12 L-35 12 L-31 2Z" fill="{col}"/>'
            f'<circle cx="-4" cy="-16" r="2.6" fill="{col}"/><circle cx="-4" cy="16" r="2.6" fill="{col}"/>'
            '</g>')
    return body


def trail(x0, y0, x1, y1, w0, w1, col=CREAM, op=.9, gap=.0):
    """A trail from the plane (x0,y0) back to (x1,y1), thin at the plane, wide far behind,
    with the short clear gap behind the engines where the exhaust has not yet cooled."""
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy) or 1
    ux, uy = dx / L, dy / L
    nx, ny = -uy, ux
    sx, sy = x0 + ux * gap, y0 + uy * gap
    pts = []
    n = 24
    for i in range(n + 1):
        t = i / n
        w = w0 + (w1 - w0) * t ** 1.3
        pts.append((sx + (x1 - sx) * t + nx * w / 2, sy + (y1 - sy) * t + ny * w / 2))
    for i in range(n, -1, -1):
        t = i / n
        w = w0 + (w1 - w0) * t ** 1.3
        pts.append((sx + (x1 - sx) * t - nx * w / 2, sy + (y1 - sy) * t - ny * w / 2))
    return f'<polygon points="{P(pts)}" fill="{col}" opacity="{op}"/>'


def hills(W, H, base, cols, seed_off=0):
    return draw.hills((W, H), base, [
        ((46, 22, 12), (.0031, .0083, .019), (0.6 + seed_off, 2.1, .4), cols[0], .55, -70),
        ((38, 18, 9), (.0042, .011, .023), (2.2, .3 + seed_off, 1.7), cols[1], .85, -20),
        ((28, 14, 7), (.0052, .013, .031), (4.0, 1.2, .9 + seed_off), cols[2], 1, 30)])


def stars(W, top, n, seed, rnd=None):
    rnd = random.Random(seed)
    return "".join(f'<circle cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(0, top):.0f}" r="{rnd.uniform(.8, 2.2):.1f}" '
                   f'fill="#fff" opacity="{rnd.uniform(.25, .7):.2f}"/>' for _ in range(n))


def hero_bg():
    """The hero's still layer: rose sky, sparkles, hills. Planes are drawn live by hero.js."""
    W, H = 1600, 900
    s = [f'<defs><linearGradient id="sk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#B83A55"/>'
         f'<stop offset=".55" stop-color="{ROSE}"/><stop offset="1" stop-color="{ROSE2}"/></linearGradient></defs>',
         f'<rect width="{W}" height="{H}" fill="url(#sk)"/>', stars(W, 520, 90, 7)]
    for (x, y, r) in ((180, 140, 16), (1420, 110, 20), (1510, 330, 11), (700, 80, 10), (1120, 250, 9), (420, 360, 8)):
        s.append(sparkle(x, y, r, GOLD, .9))
    s.append(hills(W, H, 740, (ROSE3, "#E27F84", "#A8344B")))
    return svg(W, H, "".join(s), ' preserveAspectRatio="xMidYMax slice"')


def night_bg():
    W, H = 1600, 600
    s = [f'<defs><linearGradient id="nk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#16213F"/>'
         f'<stop offset="1" stop-color="{IND}"/></linearGradient></defs>',
         f'<rect width="{W}" height="{H}" fill="url(#nk)"/>', stars(W, 420, 110, 9),
         f'<circle cx="1380" cy="110" r="44" fill="{CREAM}" opacity=".95"/>']
    s.append(hills(W, H, 470, ("#3B4E86", "#31447A", "#263665"), 1.1))
    return svg(W, H, "".join(s), ' preserveAspectRatio="xMidYMax slice"')


# ---- the Schmidt-Appleman chart, drawn from the formulas
def sac_chart(lang="en"):
    W, H = 760, 470
    L, R, T, B = 70, 730, 30, 410
    t0, t1 = -70.0, -25.0
    e0, e1 = 0.0, 90.0
    X = lambda t: L + (t - t0) / (t1 - t0) * (R - L)
    Y = lambda e: B - (e - e0) / (e1 - e0) * (B - T)
    th = lang == "th"
    s = [f'<rect width="{W}" height="{H}" rx="18" fill="{IND}"/>']
    for t in range(-70, -24, 5):
        s.append(f'<line x1="{X(t):.1f}" y1="{T}" x2="{X(t):.1f}" y2="{B}" stroke="#fff" stroke-opacity=".08"/>'
                 f'<text x="{X(t):.1f}" y="{B + 22}" fill="{CREAM}" font-size="13" text-anchor="middle" opacity=".8">{t}°</text>')
    for e in range(0, 91, 15):
        s.append(f'<line x1="{L}" y1="{Y(e):.1f}" x2="{R}" y2="{Y(e):.1f}" stroke="#fff" stroke-opacity=".08"/>'
                 f'<text x="{L - 10}" y="{Y(e) + 4:.1f}" fill="{CREAM}" font-size="13" text-anchor="end" opacity=".8">{e}</text>')
    curve = lambda f: P([(X(t), Y(f(t + 273.15))) for t in [t0 + i * (t1 - t0) / 200 for i in range(201)] if f(t + 273.15) <= e1])
    # the shaded "trail zone": above the water curve is where a plume turns to droplets, then ice
    s.append(f'<polyline points="{curve(e_water)}" fill="none" stroke="{GOLD}" stroke-width="4"/>')
    s.append(f'<polyline points="{curve(e_ice)}" fill="none" stroke="{ROSE2}" stroke-width="3" stroke-dasharray="8 6"/>')
    # mixing lines at 250 hPa from exhaust (hot, wet) down to three ambient states
    p = 25000
    G = slope(p)
    TM = t_tangent(G) - 273.15
    em = e_water(TM + 273.15)
    for (ta, u, col) in ((-58, .5, CREAM), (-45, .75, CREAM), (-35, .5, "#8FA4D8")):
        ea = u * e_water(ta + 273.15)
        x2 = ta + (e1 - ea) / G
        s.append(f'<line x1="{X(ta):.1f}" y1="{Y(ea):.1f}" x2="{X(min(x2, t1)):.1f}" y2="{Y(ea + G * (min(x2, t1) - ta)):.1f}" '
                 f'stroke="{col}" stroke-width="2.4" opacity=".85"/>'
                 f'<circle cx="{X(ta):.1f}" cy="{Y(ea):.1f}" r="7" fill="{col}"/>')
    s.append(f'<circle cx="{X(TM):.1f}" cy="{Y(em):.1f}" r="6" fill="none" stroke="{GOLD}" stroke-width="3"/>')
    lab = {
        "water": ("water saturation", "อิ่มตัวเทียบน้ำ"), "ice": ("ice saturation", "อิ่มตัวเทียบน้ำแข็ง"),
        "x": ("air temperature, °C", "อุณหภูมิอากาศ °C"), "y": ("water vapour, Pa", "ไอน้ำ ปาสคาล"),
        "a": ("trail", "มีทาง"), "b": ("trail", "มีทาง"), "c": ("no trail", "ไม่มีทาง"),
    }
    tl = lambda k: lab[k][1 if th else 0]
    s.append(f'<text x="{X(-31):.1f}" y="{Y(e_water(242.15)) - 12:.1f}" fill="{GOLD}" font-size="15" font-weight="700" text-anchor="end">{tl("water")}</text>')
    s.append(f'<text x="{X(-29):.1f}" y="{Y(e_ice(244.15)) + 22:.1f}" fill="{ROSE2}" font-size="15" font-weight="700" text-anchor="start">{tl("ice")}</text>')
    s.append(f'<text x="{(L + R) / 2}" y="{H - 16}" fill="{CREAM}" font-size="14" text-anchor="middle">{tl("x")}</text>')
    s.append(f'<text x="18" y="{(T + B) / 2}" fill="{CREAM}" font-size="14" text-anchor="middle" transform="rotate(-90 18 {(T + B) / 2})">{tl("y")}</text>')
    for (ta, u, k) in ((-58, .5, "a"), (-45, .75, "b"), (-35, .5, "c")):
        s.append(f'<text x="{X(ta) + 12:.1f}" y="{Y(u * e_water(ta + 273.15)) - 12:.1f}" fill="{CREAM}" font-size="14" font-weight="700" text-anchor="end">{tl(k)}</text>')
    return svg(W, H, "".join(s), ' role="img"')


# ---- the weight of a trail: two squares with areas in the true ratio
def weight_art(lang="en"):
    f = facts()
    W, H = 760, 420
    th = lang == "th"
    big = 360.0
    small = big * math.sqrt(f["water_per_km"] / f["ice_per_km"])
    s = [f'<rect width="{W}" height="{H}" rx="18" fill="{CREAM}"/>']
    x0, y0 = 360, 30
    s.append(f'<rect x="{x0}" y="{y0}" width="{big}" height="{big}" rx="6" fill="{ROSE2}"/>')
    rnd = random.Random(3)
    for _ in range(240):
        cx, cy = x0 + rnd.uniform(8, big - 8), y0 + rnd.uniform(8, big - 8)
        s.append(sparkle(cx, cy, rnd.uniform(2, 5), "#fff", rnd.uniform(.35, .9)))
    s.append(f'<rect x="{x0 + big - small - 12:.1f}" y="{y0 + big - small - 12:.1f}" width="{small:.1f}" height="{small:.1f}" fill="{IND}"/>')
    t1 = ("ice in one kilometre of an hour-old trail", "น้ำแข็งในทางยาว 1 กิโลเมตร อายุ 1 ชั่วโมง")
    t2 = ("water the engines put in that kilometre", "น้ำที่เครื่องยนต์ปล่อยออกมาในกิโลเมตรนั้น")
    n1 = f'{f["ice_per_km"]:,.0f} kg'
    n2 = f'{f["water_per_km"]:.1f} kg'
    s.append(f'<text x="330" y="90" fill="{WINE}" font-size="40" font-weight="800" text-anchor="end">{n1}</text>')
    s.append(f'<text x="330" y="120" fill="{WINE}" font-size="16" text-anchor="end">{t1[1 if th else 0]}</text>')
    s.append(f'<text x="330" y="330" fill="{IND}" font-size="40" font-weight="800" text-anchor="end">{n2}</text>')
    s.append(f'<text x="330" y="360" fill="{IND}" font-size="16" text-anchor="end">{t2[1 if th else 0]}</text>')
    s.append(f'<line x1="336" y1="352" x2="{x0 + big - small - 16:.1f}" y2="{y0 + big - small / 2 - 12:.1f}" stroke="{IND}" stroke-width="2"/>')
    return svg(W, H, "".join(s), ' role="img"')


# ---- the grid: three airways, planes every few minutes, wind pushing every trail sideways
def grid_art(hours=2.5, wind=(38.0, 12.0)):
    """Plan view, 160 x 90 km. Trails persist and spread. The criss-cross is three routes
    crossing, each trail an hour or two old and drifted downwind."""
    W, H = 1600, 900
    kx = W / 160.0
    s = [f'<defs><linearGradient id="gs" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#B83A55"/>'
         f'<stop offset="1" stop-color="{ROSE2}"/></linearGradient></defs><rect width="{W}" height="{H}" fill="url(#gs)"/>']
    rnd = random.Random(21)
    routes = [(-58, 30, 34), (28, 52, 41), (104, 64, 47)]  # bearing of travel (deg, 0 = east), offset km, minutes apart
    now = hours * 60
    items = []
    for ang, off, every in routes:
        a = math.radians(ang)
        ux, uy = math.cos(a), math.sin(a)
        nx, ny = -uy, ux
        cx, cy = 80 + nx * (off - 45), 45 + ny * (off - 45)
        t = rnd.uniform(0, every)
        while t < now:
            age = now - t  # minutes since this plane crossed the middle
            dx, dy = wind[0] * age / 60, wind[1] * age / 60
            L = 150 + 60 * min(1, age / 60)
            width = 0.5 + 1.6 * age / 60
            op = max(.18, .92 - age / (hours * 60) * .7)
            x0, y0 = (cx + dx - ux * L / 2) * kx, (cy + dy - uy * L / 2) * kx
            x1, y1 = (cx + dx + ux * L / 2) * kx, (cy + dy + uy * L / 2) * kx
            items.append((age, trail(x0, y0, x1, y1, width * kx, width * kx, CREAM, op)))
            t += every * rnd.uniform(.8, 1.25)
    for _, it in sorted(items, key=lambda z: -z[0]):
        s.append(it)
    # the newest plane on each route, still drawing its line
    for i, (ang, off, every) in enumerate(routes):
        a = math.radians(ang)
        ux, uy = math.cos(a), math.sin(a)
        nx, ny = -uy, ux
        cx, cy = 80 + nx * (off - 45), 45 + ny * (off - 45)
        px, py = (cx + ux * (10 + 12 * i)) * kx, (cy + uy * (10 + 12 * i)) * kx
        s.append(trail(px, py, px - ux * 40 * kx, py - uy * 40 * kx, .3 * kx, .7 * kx, "#fff", .95, gap=18))
        s.append(plane(px, py, ang, 1.3, "#fff"))
    s.append(hills(W, H, 820, (ROSE3, "#E27F84", "#A8344B"), .6))
    return svg(W, H, "".join(s), ' role="img" preserveAspectRatio="xMidYMid slice"')


def engines_art():
    """Two jets side by side at one height. The one that wastes less heat makes the trail."""
    W, H = 1200, 520
    s = [f'<defs><linearGradient id="es" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#16213F"/>'
         f'<stop offset="1" stop-color="{IND}"/></linearGradient></defs><rect width="{W}" height="{H}" rx="18" fill="url(#es)"/>',
         stars(W, 380, 70, 13)]
    s.append(trail(930, 170, 60, 150, 10, 46, CREAM, .92, gap=70))
    s.append(plane(930, 170, -1.3, 2.2, "#fff"))
    s.append(plane(930, 350, -1.3, 2.2, "#8FA4D8"))
    s.append(hills(W, H, 470, ("#3B4E86", "#31447A", "#263665"), 2.2))
    return svg(W, H, "".join(s), ' role="img"')


def main():
    os.makedirs(IMG, exist_ok=True)
    out = {
        "tinchok.svg": tinchok_tile(),
        "nan.svg": medallion("nan"),
        "beer.svg": medallion("beer"),
        "hero-bg.svg": hero_bg(),
        "night-bg.svg": night_bg(),
        "sac.svg": sac_chart("en"), "sac-th.svg": sac_chart("th"),
        "weight.svg": weight_art("en"), "weight-th.svg": weight_art("th"),
        "grid.svg": grid_art(),
        "engines.svg": engines_art(),
    }
    for k, v in out.items():
        open(os.path.join(IMG, k), "w", encoding="utf-8").write(v)
        print(f"{k:16s} {len(v) // 1024:5d} KB")


if __name__ == "__main__":
    main()
