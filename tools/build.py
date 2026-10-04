# -*- coding: utf-8 -*-
"""build.py: write docs/index.html (English) and docs/th/index.html (Thai) from one source.

    python3 tools/art.py && python3 tools/build.py
Numbers in the copy come from tools/physics.py, so the text and the arithmetic agree.
"""
import html
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DOCS = os.path.join(ROOT, "docs")
sys.path.insert(0, HERE)
from bands import band  # noqa: E402
from physics import facts  # noqa: E402

SITE = "https://nanobotco.github.io/chemtrails/"
L = "en"
F = facts()


def e(x):
    return html.escape("" if x is None else str(x))


def t(en, th):
    return th if L == "th" else en


def n0(x):
    return f"{x:,.0f}"


def cred(who, lic, url=""):
    w = f'<a href="{e(url)}">{e(who)}</a>' if url else e(who)
    return f"{w} · {e(lic)}"


C = "https://commons.wikimedia.org/wiki/File:"

BANDS = {
    "spread": ("Manchester, 2008", "แมนเชสเตอร์ 2008", "Old trails, spreading", "ทางเก่าที่แผ่กว้าง",
               "Hours-old trails fan out into thin cloud. The air was already holding more water than ice can stand.",
               "ทางที่อายุหลายชั่วโมงแผ่ออกเป็นเมฆบาง อากาศวันนั้นถือน้ำไว้เกินกว่าที่น้ำแข็งจะทนได้อยู่แล้ว",
               ("Anthony Appleyard", "public domain", C + "Aa_oldcontrails01.jpg"), ""),
    "three": ("One sky, three trails", "ฟ้าเดียว สามทาง", "Three planes, three heights", "สามลำ สามความสูง",
              "Each line is a plane at a different height, in its own layer of air.",
              "แต่ละเส้นคือเครื่องบินคนละความสูง อยู่ในชั้นอากาศของตัวเอง",
              ("Iamdev37", "CC BY-SA 4.0", C + "Contrails_(Condensation_Trail).jpg"), "right"),
    "b17": ("27 September 1943", "27 กันยายน 1943", "Trails before jets", "ทางก่อนยุคเครื่องบินเจ็ต",
            "B-17s of the 390th Bomb Group over Europe, their fighter escorts looping trails above them. Piston engines breathe out water too.",
            "เครื่องบิน B-17 ของกองบินทิ้งระเบิดที่ 390 เหนือยุโรป เครื่องบินขับไล่คุ้มกันวาดทางวนอยู่ข้างบน เครื่องยนต์ลูกสูบก็พ่นไอน้ำเหมือนกัน",
            ("Sgt. Stanley M. Smith, USAAF · Smithsonian NASM", "public domain", C + "Boeing_B-17F_Flying_Fortresses_in_flight_with_contrails.jpg"), "tall"),
    "satellite": ("From space, 15 Feb 2013", "จากอวกาศ 15 ก.พ. 2013", "The whole sky's worth", "ทั้งผืนฟ้า",
                  "Trails over Spain and Portugal from NASA's Terra satellite: the jet routes, drawn in ice.",
                  "ทางเหนือสเปนและโปรตุเกส ถ่ายจากดาวเทียมเทอร์ราของนาซา เส้นทางบินเจ็ต วาดด้วยน้ำแข็ง",
                  ("NASA Goddard / MODIS", "public domain", C + "Criss-Crossing_Contrails_(8495592530).jpg"), "right"),
    "wing": ("Over the wing", "เหนือปีก", "Trails from wings", "ทางจากปีก",
             "Air speeding over a wing drops in pressure and cools, and wet air makes a brief cloud. Gone the moment it leaves the wing.",
             "อากาศที่วิ่งเร็วผ่านปีกความดันลดและเย็นลง อากาศชื้นเลยเป็นเมฆชั่วครู่ พ้นปีกก็หายไป",
             ("Andrey Filippov", "CC BY 2.0", C + "Condensation_pattern_over_an_airliner_wing_(30987670468).jpg"), "short"),
}


def bnd(key, r):
    ken, kth, hen, hth, len_, lth, (who, lic, url), cls = BANDS[key]
    return band(r + "img/" + key + ".jpg", kicker=t(ken, kth), head=t(hen, hth), line=t(len_, lth),
                credit=cred(who, lic, url), cls=cls)


# NaN asks, Beer answers
QA = [
    ("Why does one plane leave a long trail and the next plane none?",
     "ทำไมลำหนึ่งทิ้งทางยาว แต่อีกลำไม่มีเลย",
     "They are at different heights, and wet air comes in layers. The panel above shows three heights; they often disagree. The engine matters too: see below.",
     "เพราะบินคนละความสูง และอากาศชื้นมาเป็นชั้น ๆ แผงด้านบนแสดงสามความสูง ซึ่งมักไม่ตรงกัน เครื่องยนต์ก็มีผลด้วย ดูข้างล่าง"),
    ("They didn't use to last this long.",
     "เมื่อก่อนทางไม่ค้างนานขนาดนี้",
     "They did in 1943 (the bombers above). There are more planes now: 153,359 commercial flights on 23 July 2026, a record day. And newer engines make trails in warmer air.",
     "ปี 1943 ก็ค้าง (ดูเครื่องบินทิ้งระเบิดข้างบน) ตอนนี้เครื่องบินเยอะขึ้น วันที่ 23 กรกฎาคม 2026 มีเที่ยวบินพาณิชย์ 153,359 เที่ยว มากที่สุดเท่าที่เคยมี และเครื่องยนต์รุ่นใหม่ทำให้เกิดทางในอากาศที่อุ่นกว่า"),
    ("What about the photos of barrels inside planes?",
     "แล้วรูปถังในเครื่องบินล่ะ",
     "Water ballast for test flights. Boeing's photo archive labels them so. On the Airbus A350 test plane each barrel holds about 300 kg of water, pumped fore and aft to move the balance point.",
     "ถังน้ำถ่วงน้ำหนักสำหรับบินทดสอบ คลังภาพของโบอิ้งก็เขียนไว้แบบนั้น บนเครื่องทดสอบแอร์บัส A350 แต่ละถังจุน้ำราว 300 กก. สูบไปหน้าไปหลังเพื่อย้ายจุดสมดุล"),
    ("Soil tests found aluminium and barium.",
     "ตรวจดินแล้วเจออะลูมิเนียมกับแบเรียม",
     "Aluminium is about 8% of the Earth's crust, the most common metal in it. Barium runs about 628 parts per million. Any soil test anywhere finds both.",
     "อะลูมิเนียมมีราว 8% ของเปลือกโลก เป็นโลหะที่มีมากที่สุด แบเรียมมีราว 628 ส่วนในล้านส่วน ตรวจดินที่ไหนก็เจอทั้งสองอย่าง"),
    ("There are patents and papers about spraying the sky.",
     "มีสิทธิบัตรและงานวิจัยเรื่องพ่นสารบนฟ้า",
     "There are. They are ideas on paper. The designs put the spray near 20 km up, higher than airliners fly, from a plane that has not been built. Harvard's one planned balloon test was dropped in March 2024 before it flew.",
     "มีจริง แต่เป็นความคิดบนกระดาษ แบบที่เสนอไว้ต้องพ่นที่ความสูงราว 20 กม. สูงกว่าที่เครื่องบินโดยสารบิน ด้วยเครื่องบินที่ยังไม่มีใครสร้าง การทดสอบด้วยบอลลูนของฮาร์วาร์ดถูกยกเลิกเมื่อมีนาคม 2024 ก่อนได้ขึ้นบิน"),
    ("The Air Force wrote about owning the weather.",
     "กองทัพอากาศเคยเขียนเรื่องครองสภาพอากาศ",
     "A 1996 student paper imagining the year 2025. Its front page says it holds fictional scenarios and is not Air Force policy.",
     "เป็นรายงานของนักศึกษาปี 1996 ที่จินตนาการถึงปี 2025 หน้าแรกเขียนไว้ว่ามีเรื่องสมมติ และไม่ใช่นโยบายของกองทัพอากาศ"),
    ("Weather modification is real, isn't it?",
     "การดัดแปรสภาพอากาศมีจริงใช่ไหม",
     "Yes. Thailand's royal rainmaking has flown since 1969: salt near cloud base, dry ice below it, silver iodide at the tops, up to about 21,500 ft. It seeds clouds that are already there. A trail at 35,000 ft in clear blue sky is something else.",
     "มีจริง ฝนหลวงบินมาตั้งแต่ปี 1969 โปรยเกลือแถวฐานเมฆ น้ำแข็งแห้งใต้ฐานเมฆ ซิลเวอร์ไอโอไดด์ที่ยอดเมฆ สูงสุดราว 21,500 ฟุต ใช้กับเมฆที่มีอยู่แล้ว ทางที่ 35,000 ฟุตบนฟ้าใสเป็นคนละเรื่อง"),
    ("Who else says so?",
     "มีใครพูดแบบนี้อีกบ้าง",
     "In 2016, 77 atmospheric chemists and geochemists were asked. 76 had seen no evidence of a secret spraying program. In 2025 the US EPA, under an administrator who took the question up, wrote that it knows of no trail ever made on purpose for weather over the US.",
     "ปี 2016 มีการถามนักเคมีบรรยากาศและนักธรณีเคมี 77 คน 76 คนไม่เคยเห็นหลักฐานโครงการพ่นสารลับ ปี 2025 สำนักงานปกป้องสิ่งแวดล้อมสหรัฐฯ ซึ่งผู้บริหารหยิบคำถามนี้ขึ้นมาเอง เขียนว่าไม่รู้ว่าเคยมีทางไหนถูกทำขึ้นโดยตั้งใจเพื่อดัดแปรอากาศเหนือสหรัฐฯ"),
    ("So do trails matter at all?",
     "แล้วทางเครื่องบินมีผลอะไรไหม",
     "They do, for warmth. Trail cloud holds heat in: about 57 of aviation's 101 milliwatts per square metre of warming in 2018, more than its carbon dioxide. Airlines now test steering around trail-making air. That is the trail story worth talking about.",
     "มี เรื่องความร้อน เมฆจากทางเก็บความร้อนไว้ ราว 57 จาก 101 มิลลิวัตต์ต่อตารางเมตรที่การบินทำให้โลกร้อนในปี 2018 มากกว่าคาร์บอนไดออกไซด์ของการบินเอง ตอนนี้สายการบินกำลังทดลองบินเลี่ยงอากาศที่ทำให้เกิดทาง เรื่องนี้แหละที่น่าคุยกัน"),
    ("How do I settle it myself?",
     "จะพิสูจน์เองได้ยังไง",
     "Make a prediction. Read the panel at the top, write down \"long trails at 3 pm\", then look up at 3 pm. A spraying program would not follow tomorrow's humidity forecast.",
     "ลองทำนาย อ่านแผงด้านบน จดไว้ว่า \"บ่ายสามโมงทางยาว\" แล้วแหงนดูตอนบ่ายสามโมง โครงการพ่นสารคงไม่เดินตามพยากรณ์ความชื้นของพรุ่งนี้"),
]

SOURCES = [
    ("Schumann 1996, On conditions for contrail formation from aircraft exhausts, Meteorol. Z. 5:4–23", "https://www.schweizerbart.de/papers/metz/detail/5/89525"),
    ("Appleman 1953, The formation of exhaust condensation trails by jet aircraft, BAMS 34:14–20", "https://doi.org/10.1175/1520-0477-34.1.14"),
    ("Murphy & Koop 2005, vapour pressures of ice and supercooled water, QJRMS 131:1539", "https://doi.org/10.1256/qj.04.94"),
    ("pycontrails: Schmidt–Appleman code and Jet A constants", "https://github.com/contrailcirrus/pycontrails/blob/main/pycontrails/models/sac.py"),
    ("Kärcher 2018, Formation and radiative forcing of contrail cirrus, Nature Communications 9:1824", "https://pmc.ncbi.nlm.nih.gov/articles/PMC5940853/"),
    ("IPCC 1999, Aviation and the Global Atmosphere, §3.4", "https://www.grida.no/climate/ipcc/aviation/038.htm"),
    ("Schumann, Busen & Plohr 2000, propulsion efficiency and contrail formation, J. Aircraft 37(6)", "https://arc.aiaa.org/doi/10.2514/2.2715"),
    ("Shearer, West, Caldeira & Davis 2016, expert survey, Environ. Res. Lett. 11:084011", "https://iopscience.iop.org/article/10.1088/1748-9326/11/8/084011"),
    ("EPA, FAA, NASA, NOAA 2000, Aircraft Contrails Factsheet", "https://www.faa.gov/sites/faa.gov/files/regulations_policies/policy_guidance/envir_policy/contrails.pdf"),
    ("EPA, FAA, NOAA 2025, Contrails Fact Sheet", "https://www.epa.gov/system/files/documents/2025-07/epa-faa-contrails-factsheet-2025-0718.pdf"),
    ("EPA, Geoengineering: frequent questions", "https://www.epa.gov/geoengineering/frequent-questions"),
    ("Boeing Images: 747-100 flight test ballast", "https://secure.boeingimages.com/archive/747-100-Flight-Test-Ballast-2F3XC5OK63W.html"),
    ("Lead Stories 2023: barrels are ballast tanks (A350)", "https://leadstories.com/hoax-alert/2023/09/fact-check-photo-of-barrels-on-a-plane-shows-ballast-tanks-for-load-testing-no-mystery-what-they-are-for.html"),
    ("USGS: aluminium in the crust", "https://pubs.usgs.gov/sir/2017/5118/elements/Aluminum/Al_txt.html"),
    ("USGS: barium in the crust", "https://pubs.usgs.gov/sir/2017/5118/elements/Barium/Ba_txt.html"),
    ("Smith & Wagner 2018, stratospheric aerosol injection tactics and costs, Environ. Res. Lett. 13:124001", "https://iopscience.iop.org/article/10.1088/1748-9326/aae98d"),
    ("Harvard Salata Institute: an update on SCoPEx, March 2024", "https://salatainstitute.harvard.edu/an-update-on-scopex/"),
    ("House et al. 1996, Weather as a Force Multiplier: Owning the Weather in 2025", "https://archive.org/download/WeatherAsAForceMultiplier/WeatherAsAForceMultiplier.pdf"),
    ("Royal Rainmaking patent EP1491088A1", "https://patents.google.com/patent/EP1491088A1/en"),
    ("Thai MFA: The Royal Rainmaking Project", "https://image.mfa.go.th/mfa/0/iyOJNVBddx/The_Royal_Rainmaking_Project_.pdf"),
    ("Department of Royal Rainmaking and Agricultural Aviation", "https://www.royalrain.go.th/"),
    ("Lee et al. 2021, aviation's contribution to climate forcing, Atmos. Environ. 244:117834", "https://repository.library.noaa.gov/view/noaa/45026"),
    ("American Airlines 2023: contrail-avoidance trial", "https://news.aa.com/news/news-details/2023/American-Airlines-participates-in-first-of-its-kind-research-on-contrail-avoidance-CORP-OTH-08/default.aspx"),
    ("Airways Magazine: Flightradar24 record day, July 2026", "https://www.airwaysmag.com/new-post/flightradar24-record-commercial-flights-july-2026"),
    ("FAA Aeronautical Information Manual 5-3-4: jet routes", "https://www.faa.gov/air_traffic/publications/atpubs/aim_html/chap5_section_3.html"),
    ("Wikipedia: Chemtrail conspiracy theory", "https://en.wikipedia.org/wiki/Chemtrail_conspiracy_theory"),
    ("Open-Meteo forecast API (ECMWF IFS), CC BY 4.0", "https://open-meteo.com/"),
    ("adsb.lol live planes, ODbL", "https://adsb.lol/"),
    ("Wikimedia Commons", "https://commons.wikimedia.org/"),
]

NOTRANS = ('<script>if(/[.]translate[.]goog$/.test(location.hostname))location.replace("https://"+location.hostname.slice(0,-15)'
           '.replace(/--/g,"~").replace(/-/g,".").replace(/~/g,"-")+location.pathname+location.search.replace(/([?&])_x_tr_[^&]*/g,"$1")'
           '.replace(/[?&]+$/,"").replace(/[?]&+/,"?")+location.hash)</script>')


def bubble(who, text):
    name = {"nan": ("NaN", "แนน"), "beer": ("Beer", "เบียร์")}[who]
    return (f'<div class="say {who}"><img src="{{r}}img/{who}.svg" alt="" width="64" height="64">'
            f'<p><b>{e(t(*name))}</b>{e(text)}</p></div>')


def page():
    r = "../" if L == "th" else ""
    here = SITE + ("th/" if L == "th" else "")
    title = t("Chemtrails? It's ice.", "เคมเทรล? มันคือน้ำแข็ง")
    desc = t("Why jets leave trails, why some stay, and a live check of whether planes over you will leave them right now. Drawn with math, from the physics.",
             "ทำไมเครื่องบินเจ็ตทิ้งทาง ทำไมบางทางค้าง และเช็กสดว่าเครื่องบินเหนือหัวคุณตอนนี้จะทิ้งทางไหม วาดด้วยคณิตศาสตร์ จากฟิสิกส์")
    nav = [("live", "Your sky", "ฟ้าของคุณ"), ("recipe", "Make a trail", "ลองทำทาง"), ("weight", "Weight", "น้ำหนัก"),
           ("patterns", "Patterns", "ลวดลาย"), ("questions", "Questions", "คำถาม"), ("sources", "Sources", "แหล่งข้อมูล")]
    navh = "".join(f'<a href="#{a}">{e(t(b, c))}</a>' for a, b, c in nav)
    en_cur = ' aria-current="page"' if L == "en" else ""
    th_cur = ' aria-current="page"' if L == "th" else ""
    langsw = (f'<a href="{r}" hreflang="en" lang="en"{en_cur}>EN</a> '
              f'<a href="{r}th/" hreflang="th" lang="th"{th_cur}>ไทย</a>')

    qa = "".join(f'<div class="qa">{bubble("nan", t(qe, qt))}{bubble("beer", t(ae, at))}</div>' for qe, qt, ae, at in QA)
    srcs = "".join(f'<li><a href="{e(u)}">{e(n)}</a></li>' for n, u in SOURCES)
    sfx = "-th" if L == "th" else ""

    slab = [(f'{F["water_per_km"]:.1f} kg', t("water out of the engines, per km", "น้ำจากเครื่องยนต์ ต่อ กม.")),
            (f'{n0(F["ice_per_km"])} kg', t("ice in that km an hour later", "น้ำแข็งใน กม. นั้น หนึ่งชั่วโมงต่อมา")),
            (f'×{n0(F["ratio"])}', t("came out of the sky", "มาจากท้องฟ้า")),
            (f'{F["km_of_trail_per_payload"] / 1000:.1f} km', t("of trail a full 20 t payload could fill", "ความยาวทางที่น้ำหนักบรรทุกเต็มลำ 20 ตันทำได้"))]
    slabh = "".join(f'<div><b>{e(a)}</b><span>{e(b)}</span></div>' for a, b in slab)

    css = open(os.path.join(HERE, "bands.css"), encoding="utf-8").read() + CSS
    body = f"""<!doctype html><html lang="{L}" translate="no" class="notranslate"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="google" content="notranslate"><meta name="robots" content="notranslate">
{NOTRANS}
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{here}">
<link rel="alternate" hreflang="en" href="{SITE}"><link rel="alternate" hreflang="th" href="{SITE}th/"><link rel="alternate" hreflang="x-default" href="{SITE}">
<meta property="og:type" content="website"><meta property="og:site_name" content="NaNoBotCo">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{here}">
<meta property="og:image" content="{SITE}card.jpg"><meta property="og:image:secure_url" content="{SITE}card.jpg"><meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(t("Jets crossing a rose sky, one leaving a long trail, with the words: Chemtrails? It's ice.", "เครื่องบินเจ็ตข้ามฟ้าสีชมพู ลำหนึ่งทิ้งทางยาว พร้อมข้อความ เคมเทรล? มันคือน้ำแข็ง"))}">
<meta property="og:locale" content="{t("en_US", "th_TH")}"><meta property="og:locale:alternate" content="{t("th_TH", "en_US")}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{SITE}card.jpg">
<link rel="icon" href="{r}icon.svg" type="image/svg+xml">
<link rel="alternate" type="text/plain" href="{SITE}llms.txt" title="llms.txt">
<link rel="preconnect" href="https://api.open-meteo.com">
<style>{css}</style>
</head><body>
<header class="top"><div class="in">
<a class="brand" href="{r}{"th/" if L == "th" else ""}">{e(t("It's ice", "น้ำแข็ง"))} <b>✦</b></a>
<nav aria-label="{e(t("Sections", "หัวข้อ"))}">{navh}</nav>
<span class="langsw">{langsw}</span>
</div></header>

<section class="hero" style="background-image:url({r}img/hero-bg.svg)">
<canvas id="hero-sky" aria-hidden="true"></canvas>
<div class="in">
<span class="kicker">{e(t("Chemtrails, drawn with math", "เคมเทรล วาดด้วยคณิตศาสตร์"))}</span>
<h1>{e(t("It's ice.", "มันคือน้ำแข็ง"))}</h1>
<p class="lede">{e(t("A jet burns kerosene and breathes out water. Eleven kilometres up, where the air is colder than a freezer, that water turns to ice in a line behind the plane. Whether the line stays or melts away is up to the sky, and the sky can be forecast.",
                     "เครื่องบินเจ็ตเผาน้ำมันแล้วพ่นไอน้ำออกมา ที่ความสูง 11 กิโลเมตร อากาศเย็นกว่าช่องแช่แข็ง ไอน้ำนั้นกลายเป็นน้ำแข็งเป็นเส้นตามหลังเครื่องบิน เส้นจะค้างหรือหายไปขึ้นกับท้องฟ้า และท้องฟ้าพยากรณ์ได้"))}</p>
<p><a class="btn" href="#live">{e(t("Check your sky", "เช็กฟ้าของคุณ"))}</a> <a class="btn ghost" href="#recipe">{e(t("Make a trail", "ลองทำทางเอง"))}</a></p> <!-- stylecheck: allow — button label -->
<div class="cast">{bubble("nan", t("Same planes, same fuel, different sky.", "เครื่องบินเดิม น้ำมันเดิม ฟ้าต่างกัน"))}{bubble("beer", t("It's physics. The math is right here.", "ฟิสิกส์ค่ะ คณิตศาสตร์อยู่ตรงนี้เลย"))}</div>
</div>
</section>
<div class="tinchok" aria-hidden="true"></div>

<section id="live" class="night" style="background-image:url({r}img/night-bg.svg)">
<div class="wrap">
<span class="kicker">{e(t("Live · forecast by the hour", "สด · พยากรณ์รายชั่วโมง"))}</span>
<h2>{e(t("Your sky, now", "ฟ้าของคุณ ตอนนี้"))}</h2>
<div class="live-grid">
<div>
<p class="lv-head" id="lv-head">{e(t("Reading the sky…", "กำลังอ่านท้องฟ้า…"))}</p>
<p class="verdict" id="lv-verdict" aria-live="polite"></p>
<p id="lv-why" class="small"></p>
<ul class="levels" id="lv-levels"></ul>
<p id="lv-wind"></p>
<p id="lv-next" class="next"></p>
<button type="button" class="here" id="lv-here">{e(t("Use my location", "ใช้ตำแหน่งของฉัน"))}</button>
</div>
<div class="mapcol">
<canvas id="lv-map" aria-label="{e(t("Map, north up, 150 km around you, with a trail you can turn and the wind that moves it", "แผนที่ ทิศเหนืออยู่บน รัศมี 150 กม. รอบตัวคุณ มีทางที่หมุนได้และลมที่พัดมัน"))}"></canvas>
<label class="bear">{e(t("Turn the trail", "หมุนทาง"))} <b id="lv-bear-val"></b><input id="lv-bear" type="range" min="0" max="179" value="45"></label>
<p id="lv-bear-out" class="small"></p>
</div>
</div>
<h3>{e(t("The next 48 hours", "48 ชั่วโมงข้างหน้า"))}</h3>
<p class="small legend"><i class="long"></i>{e(t("long trails", "ทางยาว"))} <i class="short"></i>{e(t("short trails", "ทางสั้น"))} <i class="none"></i>{e(t("no trails", "ไม่มีทาง"))} · {e(t("rows are feet above sea level, columns are hours", "แถวคือความสูงเป็นฟุต คอลัมน์คือชั่วโมง"))}</p>
<div id="lv-strip" class="strip"></div>
<h3>{e(t("Planes near you", "เครื่องบินใกล้คุณ"))}</h3>
<div id="lv-planes" class="planes small">{e(t("Asking the plane feeds…", "กำลังถามฟีดเครื่องบิน…"))}</div>
<button type="button" class="btn ghost light" id="lv-radar">{e(t("Open the live plane map", "เปิดแผนที่เครื่องบินสด"))}</button>
<p class="small mute">{e(t("Forecast: ECMWF through Open-Meteo. Humidity 11 km up is among the hardest numbers in weather to forecast. In 2023 American Airlines pilots steered around trail-making air using forecasts like this one and made 54% fewer trails, by distance.",
                          "พยากรณ์: ECMWF ผ่าน Open-Meteo ความชื้นที่ความสูง 11 กม. เป็นตัวเลขที่พยากรณ์ยากที่สุดตัวหนึ่ง ปี 2023 นักบินอเมริกันแอร์ไลน์ใช้พยากรณ์แบบนี้บินเลี่ยงอากาศที่ทำให้เกิดทาง แล้วเกิดทางน้อยลง 54% เมื่อวัดตามระยะทาง"))}</p>
</div>
</section>
<div class="tinchok" aria-hidden="true"></div>

<main>
<section id="recipe">
<span class="kicker">{e(t("Try it", "ลองเลย"))}</span>
<h2>{e(t("Make a trail", "ลองทำทางเอง"))}</h2>
<p class="lede">{e(t("Three things decide it: how cold the air is, how wet it is, and how much heat the engine throws away. Move them.",
                     "มีสามอย่างที่ตัดสิน อากาศเย็นแค่ไหน ชื้นแค่ไหน และเครื่องยนต์ทิ้งความร้อนเท่าไร ลองเลื่อนดู"))}</p>
<div class="rc">
<div class="rc-ctl">
<label>{e(t("Air temperature", "อุณหภูมิอากาศ"))} <b id="rc-t-out"></b><input id="rc-t" type="range" min="-70" max="-25" step="0.5" value="-52"></label>
<label>{e(t("Ice humidity", "ความชื้นเทียบน้ำแข็ง"))} <b id="rc-h-out"></b><input id="rc-h" type="range" min="0" max="150" value="115"></label>
<label>{e(t("Height", "ความสูง"))} <b id="rc-p-out"></b><input id="rc-p" type="range" min="200" max="300" step="50" value="250"></label>
<label>{e(t("Engine", "เครื่องยนต์"))} <b id="rc-e-out"></b><input id="rc-e" type="range" min="0.2" max="0.4" step="0.1" value="0.3"></label>
<p class="verdict" id="rc-verdict" aria-live="polite"></p>
<p id="rc-why" class="small"></p>
</div>
<div class="rc-view">
<canvas id="rc-scene" aria-hidden="true"></canvas>
<canvas id="rc-chart" aria-label="{e(t("Water vapour against temperature: the water and ice curves, your air, and the exhaust's mixing line", "ไอน้ำเทียบอุณหภูมิ: เส้นโค้งน้ำและน้ำแข็ง อากาศของคุณ และเส้นผสมของไอเสีย"))}"></canvas>
</div>
</div>
<div class="read">
<p><b>{e(t("Reading the chart.", "อ่านกราฟ"))}</b> {e(t("The gold curve is soaked air, measured against water. The pink dashes are soaked air measured against ice, which fills up sooner. Exhaust leaves the engine hot and wet, far up and to the right, and mixes into your air along the straight line. If the line pokes above the gold curve, droplets form and freeze at once: a trail. If your dot sits above the pink dashes, the ice has no reason to leave: the trail stays.",
                                                                                "เส้นโค้งสีทองคืออากาศอิ่มตัวเมื่อเทียบกับน้ำ เส้นประสีชมพูคืออากาศอิ่มตัวเมื่อเทียบกับน้ำแข็ง ซึ่งเต็มเร็วกว่า ไอเสียออกจากเครื่องยนต์ทั้งร้อนและชื้น อยู่ไกลขึ้นไปทางขวาบน แล้วผสมกับอากาศของคุณตามเส้นตรง ถ้าเส้นโผล่เหนือเส้นสีทอง จะเกิดหยดน้ำและแข็งตัวทันที นั่นคือทาง ถ้าจุดของคุณอยู่เหนือเส้นประสีชมพู น้ำแข็งก็ไม่มีเหตุให้หายไป ทางจึงค้าง"))}</p>
<p class="eq">G = EI · c<sub>p</sub> · p ⁄ ( ε · Q · (1 − η) )</p>
<p>{e(t(f"Reading it: G is how steep the straight line is. EI is 1.23 kg of water per kg of fuel. cp is the heat it takes to warm air. p is the air pressure at the plane's height. ε is 0.622, how light water vapour is next to air. Q is the heat in a kilogram of fuel. η is the share of that heat that pushes the plane. At 34,000 ft this gives trails below {F['Tdry_250']:.1f} °C in bone-dry air and below {F['Twet_250']:.1f} °C in soaked air.",
       f"อ่านว่า G คือความชันของเส้นตรง EI คือน้ำ 1.23 กก. ต่อน้ำมัน 1 กก. cp คือความร้อนที่ใช้ทำให้อากาศอุ่น p คือความดันอากาศที่ความสูงของเครื่องบิน ε คือ 0.622 ไอน้ำเบากว่าอากาศเท่านี้ Q คือความร้อนในน้ำมัน 1 กก. η คือส่วนของความร้อนที่ใช้ผลักเครื่องบิน ที่ 34,000 ฟุต สูตรนี้บอกว่าจะเกิดทางเมื่อเย็นกว่า {F['Tdry_250']:.1f} °C ในอากาศแห้งสนิท และเย็นกว่า {F['Twet_250']:.1f} °C ในอากาศอิ่มตัว"))}</p>
</div>
</section>

{bnd("three", r)}

<section id="engines" class="engines">
<img src="{r}img/engines.svg" alt="{e(t("Two jets side by side at one height: the upper one leaves a trail, the lower one none", "เครื่องบินเจ็ตสองลำบินคู่กันที่ความสูงเดียว ลำบนทิ้งทาง ลำล่างไม่มี"))}" width="1200" height="520" loading="lazy">
<div>
<span class="kicker">{e(t("A test flight, 2000", "บินทดสอบ ปี 2000"))}</span>
<h2>{e(t("The better engine makes the trail", "เครื่องยนต์ที่ดีกว่าทำให้เกิดทาง"))}</h2>
<p>{e(t("German researchers flew an Airbus A340 and a Boeing 707 wing by wing, at the same height, in the same air, and watched from a third plane. The A340, with its more efficient engines, left a trail. The 707 left none. An engine that turns more of its heat into push sends out cooler exhaust with the same water in it, so it reaches saturation sooner.",
                  "นักวิจัยเยอรมันให้แอร์บัส A340 กับโบอิ้ง 707 บินปีกชิดปีก ความสูงเดียวกัน อากาศเดียวกัน แล้วดูจากเครื่องบินลำที่สาม A340 ที่เครื่องยนต์ประหยัดกว่าทิ้งทาง 707 ไม่ทิ้งเลย เครื่องยนต์ที่เปลี่ยนความร้อนเป็นแรงผลักได้มากกว่า ปล่อยไอเสียที่เย็นกว่าแต่มีน้ำเท่าเดิม เลยอิ่มตัวเร็วกว่า"))}</p>
</div>
</section>

<section id="weight">
<span class="kicker">{e(t("Weigh it", "ชั่งดู"))}</span>
<h2>{e(t("Could a plane carry it?", "เครื่องบินแบกไหวไหม"))}</h2>
<div class="slab">{slabh}</div>
<img class="art" src="{r}img/weight{sfx}.svg" alt="{e(t("Two squares with areas in proportion: 7,650 kg of ice against 3.6 kg of engine water", "สี่เหลี่ยมสองรูปที่พื้นที่เป็นสัดส่วนจริง น้ำแข็ง 7,650 กก. เทียบกับน้ำจากเครื่องยนต์ 3.6 กก."))}" width="760" height="420" loading="lazy">
<p>{e(t(f"A narrow-body jet burns about 2,400 kg of fuel an hour and makes {F['water_per_km']:.1f} kg of water for every kilometre it flies. An hour later, a spreading trail can be 2 km wide and 500 m deep. At −50 °C with the air 20% past ice saturation, each cubic metre gives up about {F['ice_g_m3'] * 1000:.0f} milligrams of ice to the crystals the plane left behind. Multiply: {n0(F['ice_per_km'])} kg of ice in that kilometre. The engines supplied {F['water_per_km']:.1f} kg. The sky supplied the rest.",
                  f"เครื่องบินลำตัวแคบเผาน้ำมันราว 2,400 กก. ต่อชั่วโมง ได้น้ำ {F['water_per_km']:.1f} กก. ทุกกิโลเมตรที่บิน หนึ่งชั่วโมงต่อมา ทางที่แผ่ออกอาจกว้าง 2 กม. หนา 500 ม. ที่ −50 °C และอากาศเกินจุดอิ่มตัวเทียบน้ำแข็ง 20% อากาศทุกลูกบาศก์เมตรจะคายน้ำแข็งราว {F['ice_g_m3'] * 1000:.0f} มิลลิกรัมให้ผลึกที่เครื่องบินทิ้งไว้ คูณออกมาได้น้ำแข็ง {n0(F['ice_per_km'])} กก. ในกิโลเมตรนั้น เครื่องยนต์ให้แค่ {F['water_per_km']:.1f} กก. ที่เหลือมาจากท้องฟ้า"))}</p>
<p>{e(t(f"A tank could not do this. An airliner's whole payload, about 20 tonnes, would fill {F['km_of_trail_per_payload'] / 1000:.1f} km of that trail. The IPCC put it plainly in 1999: a new trail's ice grows to exceed the plane's water “by more than two orders of magnitude”.",
                  f"ถังบรรทุกทำแบบนี้ไม่ได้ น้ำหนักบรรทุกทั้งลำราว 20 ตัน เติมทางแบบนั้นได้แค่ {F['km_of_trail_per_payload'] / 1000:.1f} กม. รายงาน IPCC ปี 1999 เขียนไว้ว่า น้ำแข็งในทางใหม่โตจนมากกว่าน้ำจากเครื่องบินเกินร้อยเท่า"))}</p>
</section>

{bnd("spread", r)}

<section id="patterns">
<span class="kicker">{e(t("Bearings", "ทิศทาง"))}</span>
<h2>{e(t("Grids, X's and stripes", "ตาราง กากบาท และลายทาง"))}</h2>
<img class="art wide" src="{r}img/grid.svg" alt="{e(t("Three air routes crossing, each trail older, wider and further downwind than the one after it", "เส้นทางบินสามเส้นตัดกัน ทางยิ่งเก่ายิ่งกว้างและยิ่งถูกลมพัดไปไกล"))}" width="1600" height="900" loading="lazy">
<p class="lede">{e(t("A trail points the way the plane was going. You can read its bearing off the sky.", "ทางชี้ไปทางที่เครื่องบินมุ่งไป อ่านทิศได้จากท้องฟ้า"))}</p>
<p>{e(t("Airliners fly set highways in the sky, called jet routes, between 18,000 and 45,000 ft. Two routes crossing make an X. One busy route makes parallel stripes a few minutes apart. The wind pushes every stripe sideways, and each stripe is a different age, so each has moved a different distance: the oldest is widest and furthest downwind. A criss-cross sky is a day when the air is wet enough to keep every trail. The picture above is drawn from that rule alone: three routes, a plane every half hour or so on each, a steady wind.",
                  "เครื่องบินโดยสารบินตามทางหลวงบนฟ้าที่เรียกว่าเส้นทางบินเจ็ต ระหว่าง 18,000 ถึง 45,000 ฟุต สองเส้นทางตัดกันเป็นกากบาท เส้นทางที่คนบินเยอะเป็นลายทางขนานห่างกันไม่กี่นาที ลมพัดทุกเส้นไปด้านข้าง และแต่ละเส้นอายุไม่เท่ากัน เลยเลื่อนไปไม่เท่ากัน เส้นที่เก่าที่สุดกว้างที่สุดและไปไกลที่สุดตามลม วันที่ฟ้าเป็นตารางคือวันที่อากาศชื้นพอจะเก็บทุกทางไว้ ภาพข้างบนวาดจากกฎนี้อย่างเดียว สามเส้นทาง ราวครึ่งชั่วโมงต่อลำ ลมคงที่"))}</p>
</section>

{bnd("satellite", r)}
{bnd("b17", r)}

<section id="questions">
<span class="kicker">{e(t("NaN asks, Beer answers", "แนนถาม เบียร์ตอบ"))}</span>
<h2>{e(t("Questions", "คำถาม"))}</h2>
<div class="qas">{qa}</div>
</section>

{bnd("wing", r)}

<section class="send">
<h2>{e(t("Send this instead of arguing", "ส่งอันนี้แทนการเถียง"))}</h2>
<p class="url"><a href="{SITE}">nanobotco.github.io/chemtrails</a></p>
<button type="button" class="btn" id="copy" data-url="{here}">{e(t("Copy the link", "คัดลอกลิงก์"))}</button>
</section>

<section id="sources">
<h2>{e(t("Sources", "แหล่งข้อมูล"))}</h2>
<ul class="src">{srcs}</ul>
<p class="mute small">{e(t("Photographs from Wikimedia Commons, credited on each. Drawings and code: NaNoBotCo. NaN and Beer drawn by NaNoBotCo.",
                          "ภาพถ่ายจากวิกิมีเดียคอมมอนส์ ระบุผู้ถ่ายบนภาพ ภาพวาดและโค้ด: NaNoBotCo แนนกับเบียร์วาดโดย NaNoBotCo"))}</p>
</section>
</main>
<div class="tinchok" aria-hidden="true"></div>
<footer class="bot"><div class="in">{e(t("Text and drawings CC BY 4.0, NaNoBotCo. Code MIT. Photographs keep their own licences. Forecast data Open-Meteo, CC BY 4.0. Plane data adsb.lol, ODbL.",
                                              "ข้อความและภาพวาด CC BY 4.0 NaNoBotCo โค้ด MIT ภาพถ่ายใช้สัญญาอนุญาตของแต่ละภาพ ข้อมูลพยากรณ์ Open-Meteo CC BY 4.0 ข้อมูลเครื่องบิน adsb.lol ODbL"))} · <a href="https://github.com/NaNoBotCo/chemtrails">GitHub</a> · <a href="https://nanobotco.github.io/rain-chiang-mai/">{e(t("Rain in Chiang Mai", "ฝนเชียงใหม่"))}</a> · <a href="https://nanobotco.github.io/chaos/">{e(t("Chaos, Drawn", "ความอลวน"))}</a></div></footer>
<script src="{r}trail.js"></script><script src="{r}hero.js" defer></script><script src="{r}live.js" defer></script><script src="{r}recipe.js" defer></script><script src="{r}top.js" defer></script>
<script>document.getElementById("copy").addEventListener("click",function(){{var b=this,u=b.dataset.url;(navigator.clipboard?navigator.clipboard.writeText(u):Promise.reject()).then(function(){{b.textContent={json.dumps(t("Copied", "คัดลอกแล้ว"), ensure_ascii=False)}}}).catch(function(){{prompt("",u)}})}})</script>
</body></html>
"""
    return body.replace("{r}", r)


CSS = """
:root{
 --bg:#FBF3E4;--panel:#fff;--ink:#231A2A;--mute:#6A5A66;--line:#EBD9BC;
 --rose:#C9485A;--rose2:#EE9496;--wine:#7A1A2C;--ind:#283A6E;--ind2:#1E2C57;--gold:#D6A42C;--red:#B23A2E;--cream:#F6EBD6;
 --accent:#C9485A;--shadow:rgba(40,20,40,.14);
 --display:"Avenir Next",Avenir,"Segoe UI",system-ui,-apple-system,Helvetica,Arial,sans-serif;
 --body:"Avenir Next",Avenir,"Segoe UI",system-ui,-apple-system,Helvetica,Arial,sans-serif;
 --thai:"Sukhumvit Set","Noto Sans Thai","Leelawadee UI",Thonburi,Tahoma,sans-serif;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
 --bg:#141A30;--panel:#1E2745;--ink:#F6EBD6;--mute:#C4B8C8;--line:#2F3A62;--accent:#EE9496;--wine:#F4B3B0;--shadow:rgba(0,0,0,.5)}}
:root[data-theme="dark"]{--bg:#141A30;--panel:#1E2745;--ink:#F6EBD6;--mute:#C4B8C8;--line:#2F3A62;--accent:#EE9496;--wine:#F4B3B0;--shadow:rgba(0,0,0,.5)}
*{box-sizing:border-box}
html{font-size:18px;scroll-behavior:smooth;scroll-padding-top:3.5rem}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--body);line-height:1.6;-webkit-text-size-adjust:100%;overflow-x:hidden}
:lang(th),.th{font-family:var(--thai);line-height:1.8}
a{color:var(--accent);text-underline-offset:.18em}
a:focus-visible,button:focus-visible,input:focus-visible{outline:3px solid var(--gold);outline-offset:2px;border-radius:4px}
img{max-width:100%;height:auto;display:block}
.mute{color:var(--mute)}.small{font-size:.86rem}

header.top{position:sticky;top:0;z-index:30;background:var(--bg);border-bottom:3px solid var(--gold);transition:transform .26s cubic-bezier(.4,0,.2,1),box-shadow .26s}
body.nav-away header.top{transform:translateY(-102%)}
body.nav-tight header.top{box-shadow:0 10px 24px -14px var(--shadow)}
header.top nav,header.top .langsw{transition:opacity .18s,max-height .26s,margin .26s}
body.nav-tight header.top nav,body.nav-tight header.top .langsw{opacity:0;max-height:0;margin-block:0;overflow:hidden;pointer-events:none}
header.top .in{max-width:68rem;margin:0 auto;padding:.5rem 1rem;display:flex;gap:.4rem 1rem;align-items:center;flex-wrap:wrap}
.brand{font-family:var(--display);font-weight:700;font-size:1.15rem;text-decoration:none;color:var(--ink);white-space:nowrap}
.brand b{color:var(--gold)}
header.top nav{display:flex;gap:.1rem .8rem;flex-wrap:wrap;font-size:.76rem;letter-spacing:.08em;text-transform:uppercase;font-weight:600}
:lang(th) header.top nav{text-transform:none;letter-spacing:0;font-size:.85rem}
header.top nav a{text-decoration:none;color:var(--mute)}
header.top nav a:hover{color:var(--ink);box-shadow:inset 0 -3px 0 var(--rose)}
.langsw{margin-left:auto;font-size:.76rem;font-weight:700;letter-spacing:.08em}
.langsw a{text-decoration:none;padding:.18rem .5rem;border:2px solid var(--line);border-radius:99px;color:var(--mute)}
.langsw a[aria-current]{background:var(--ink);color:var(--bg);border-color:var(--ink)}

.tinchok{height:46px;background:url(img/tinchok.svg) repeat-x;background-size:64px 46px}
:lang(th) .tinchok{background-image:url(../img/tinchok.svg)}

.hero{position:relative;min-height:min(94vh,900px);display:grid;align-items:end;color:var(--cream);background-size:cover;background-position:center bottom;background-color:#C9485A;isolation:isolate;overflow:hidden}
.hero canvas{position:absolute;inset:0;width:100%;height:100%;z-index:-1}
.hero .in{max-width:68rem;margin:0 auto;width:100%;padding:3rem 1rem 2.6rem}
.kicker{display:block;font-family:var(--display);font-size:.74rem;font-weight:700;letter-spacing:.3em;text-transform:uppercase;color:var(--rose);margin-bottom:.4rem}
:lang(th) .kicker{letter-spacing:.02em;text-transform:none;font-size:.9rem}
.hero .kicker{color:#FFE3A3}
.hero h1{font-family:var(--display);font-weight:600;font-size:clamp(3.2rem,12vw,7.4rem);line-height:.92;margin:0;letter-spacing:.01em;text-shadow:0 4px 30px rgba(122,26,44,.35)}
:lang(th) .hero h1{font-family:var(--thai);font-size:clamp(2.6rem,10vw,6rem);line-height:1.15}
.hero .lede{max-width:33rem;color:#FFF4E6;text-shadow:0 1px 12px rgba(90,10,30,.5)}
.cast{display:flex;gap:1rem;flex-wrap:wrap;margin-top:1.4rem}
.cast .say{max-width:22rem}
.say{display:flex;gap:.7rem;align-items:flex-start}
.say img{width:64px;height:64px;flex:none;border-radius:50%;box-shadow:0 0 0 3px var(--gold),0 6px 18px rgba(0,0,0,.2)}
.say p{margin:0;background:var(--cream);color:#231A2A;border-radius:18px;border-top-left-radius:4px;padding:.55rem .9rem;font-size:.95rem;box-shadow:0 4px 0 rgba(122,26,44,.25);position:relative}
.say p b{display:block;font-size:.72rem;letter-spacing:.14em;text-transform:uppercase;color:var(--rose)}
:lang(th) .say p b{letter-spacing:0;text-transform:none;font-size:.85rem}
.say.beer p b{color:var(--ind)}
.say.beer p{background:#E9EEFB}

.btn{display:inline-block;font-family:var(--display);font-weight:700;letter-spacing:.06em;font-size:.88rem;padding:.6rem 1.15rem;border-radius:99px;background:var(--gold);color:#231A2A;text-decoration:none;margin:.2rem .3rem .2rem 0;border:0;cursor:pointer;box-shadow:0 4px 0 #9C7412}
.btn.ghost{background:transparent;color:inherit;box-shadow:inset 0 0 0 2px currentColor}
.btn.ghost.light{color:var(--cream)}
@media (prefers-reduced-motion:no-preference){.btn{transition:transform .18s cubic-bezier(.34,1.56,.64,1)}.btn:hover{transform:translateY(-2px) scale(1.04)}.btn:active{transform:translateY(2px)}}

.night{background-color:var(--ind2);background-size:cover;background-position:center bottom;color:var(--cream);padding:2.6rem 0 3rem}
.night .wrap{max-width:68rem;margin:0 auto;padding:0 1rem}
.night .kicker{color:#FFE3A3}
.night h2,.night h3{color:var(--cream);border-color:var(--gold)}
.night a{color:#FFE3A3}
.live-grid{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:1.6rem;align-items:start}
@media (max-width:820px){.live-grid{grid-template-columns:1fr}}
.lv-head{font-size:1.1rem;margin:.4rem 0 .2rem}
.verdict{font-family:var(--display);font-weight:700;font-size:clamp(1.7rem,4.6vw,2.6rem);line-height:1.08;margin:.2rem 0 .5rem;padding:.35rem .9rem;border-radius:14px;display:inline-block}
:lang(th) .verdict{font-family:var(--thai);line-height:1.35}
.verdict:empty{display:none}
.verdict.long{background:var(--cream);color:var(--wine)}
.verdict.short{background:var(--rose2);color:#3A0A18}
.verdict.none{background:#3B4E86;color:var(--cream)}
.levels{list-style:none;display:flex;gap:.5rem;padding:0;margin:.8rem 0;flex-wrap:wrap}
.levels li{border-radius:12px;padding:.4rem .7rem;min-width:7.2rem;background:#3B4E86}
.levels li.long{background:var(--cream);color:var(--wine)}.levels li.short{background:var(--rose2);color:#3A0A18}
.levels b{display:block;font-size:.95rem}.levels span{display:block;font-weight:700;text-transform:uppercase;letter-spacing:.1em;font-size:.72rem}
:lang(th) .levels span{text-transform:none;letter-spacing:0;font-size:.85rem}
.levels small{opacity:.85}
.next{font-weight:700;color:#FFE3A3}
.here{font:700 .78rem var(--display);letter-spacing:.1em;text-transform:uppercase;color:var(--cream);background:rgba(255,255,255,.08);border:2px solid rgba(246,235,214,.6);border-radius:99px;padding:.45rem .95rem;cursor:pointer}
:lang(th) .here{font-family:var(--thai);text-transform:none;letter-spacing:0;font-size:.9rem}
.here[hidden]{display:none}
.mapcol canvas{width:100%;max-width:480px;aspect-ratio:1;display:block;margin:0 auto;border-radius:50%;box-shadow:0 0 0 4px var(--gold),0 0 0 10px rgba(214,164,44,.25)}
.bear{display:block;margin:.9rem auto 0;max-width:480px;font-weight:700}
.bear b{color:#FFE3A3;margin-left:.3rem}
input[type=range]{width:100%;accent-color:var(--gold);height:2rem}
.strip{overflow-x:auto;padding-bottom:.4rem}
.strip .row{display:grid;grid-template-columns:4.2rem 1fr;align-items:center;gap:.4rem;min-width:620px}
.strip .row>b{font-size:.78rem;text-align:right}
.strip .cells{display:grid;grid-template-columns:repeat(48,1fr);gap:2px}
.strip .cells i{height:1.3rem;border-radius:3px;background:#3B4E86}
.strip .cells i.long{background:var(--cream)}.strip .cells i.short{background:var(--rose2)}
.strip .cells i.now{outline:2px solid var(--gold);outline-offset:1px}
.strip .ticks .cells i{background:none;height:auto;font-size:.62rem;font-style:normal;white-space:nowrap;overflow:visible;opacity:.8}
.legend i{display:inline-block;width:.9rem;height:.9rem;border-radius:3px;vertical-align:-2px;margin:0 .25rem 0 .6rem;background:#3B4E86;border:1px solid rgba(246,235,214,.4)}
.legend i.long{background:var(--cream)}.legend i.short{background:var(--rose2)}
.planes ul{list-style:none;padding:0;columns:2 18rem;margin:.4rem 0}
.planes li{padding:.2rem 0;break-inside:avoid}
.chip{font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;border-radius:99px;padding:.05rem .45rem;background:#3B4E86}
.chip.long{background:var(--cream);color:var(--wine)}.chip.short{background:var(--rose2);color:#3A0A18}
.night iframe{width:100%;height:min(70vh,520px);border:0;border-radius:16px;margin:.8rem 0;box-shadow:0 0 0 4px var(--gold)}

main{max-width:68rem;margin:0 auto;padding:1rem 1rem 3rem}
h2{font-family:var(--display);font-size:clamp(1.7rem,4.6vw,2.6rem);line-height:1.05;margin:2.8rem 0 .8rem;font-weight:700;border-bottom:3px solid var(--gold);padding-bottom:.3rem}
h3{font-family:var(--display);font-size:1.2rem;margin:1.6rem 0 .4rem;font-weight:700}
:lang(th) h2,:lang(th) h3,:lang(th) .band h2{font-family:var(--thai);line-height:1.3}
section>.kicker+h2{margin-top:.1rem}
section>.kicker{margin-top:2.8rem}
p{margin:.6rem 0;max-width:44rem}
.lede{font-size:clamp(1.05rem,2.3vw,1.25rem)}

.rc{display:grid;grid-template-columns:minmax(0,.8fr) minmax(0,1.2fr);gap:1.4rem;background:var(--panel);border:3px solid var(--ind);border-radius:22px;padding:1.2rem;box-shadow:0 6px 0 var(--ind)}
@media (max-width:820px){.rc{grid-template-columns:1fr}}
.rc label{display:block;font-weight:700;margin-bottom:.4rem}
.rc label b{float:right;color:var(--rose)}
.rc .verdict.long{background:var(--ind);color:var(--cream)}
.rc-view canvas{width:100%;display:block;border-radius:14px}
.rc-view canvas+canvas{margin-top:.8rem}
.read{margin-top:1.2rem}
.eq{font-family:"Iowan Old Style",Georgia,serif;font-size:clamp(1.2rem,3.4vw,1.7rem);background:var(--ind);color:var(--cream);display:inline-block;padding:.5rem 1.1rem;border-radius:12px;max-width:none}

.engines{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:1.4rem;align-items:center;margin:2.4rem 0}
.engines img{border-radius:18px}
.engines h2{margin-top:0}
@media (max-width:820px){.engines{grid-template-columns:1fr}}

.slab{display:grid;grid-template-columns:repeat(4,1fr);border:3px solid var(--ind);border-radius:18px;overflow:hidden;margin:1.2rem 0;background:var(--panel)}
.slab div{padding:.8rem .9rem;border-right:3px solid var(--ind)}
.slab div:last-child{border-right:0}
.slab b{display:block;font-family:var(--display);font-size:clamp(1.5rem,4vw,2.3rem);line-height:1;font-weight:700;color:var(--rose)}
.slab span{display:block;font-size:.8rem;color:var(--mute);margin-top:.3rem}
@media (max-width:760px){.slab{grid-template-columns:repeat(2,1fr)}.slab div:nth-child(2n){border-right:0}.slab div:nth-child(-n+2){border-bottom:3px solid var(--ind)}}
.art{border-radius:18px;margin:1rem 0;width:100%;max-width:760px}
.art.wide{max-width:none}

.qas{display:grid;gap:1.2rem;margin-top:1rem}
.qa{display:grid;gap:.5rem}
.qa .beer{margin-left:clamp(1rem,8vw,5rem)}
.qa .say p{max-width:40rem}

.send{text-align:center;background:var(--rose);color:var(--cream);border-radius:26px;padding:1.6rem 1rem 2rem;margin:2.6rem 0;box-shadow:0 6px 0 var(--wine)}
.send h2{border:0;margin:.2rem 0;color:var(--cream)}
.send .url{font-family:var(--display);font-size:clamp(1.2rem,4.4vw,2.2rem);font-weight:700;max-width:none;margin:.4rem 0 1rem;word-break:break-word}
.send .url a{color:#fff}
.src{columns:2 20rem;padding-left:1.1rem;font-size:.9rem}
.src li{margin-bottom:.35rem;break-inside:avoid}
.band .kicker{color:#FFE3A3}
footer.bot .in{max-width:68rem;margin:0 auto;padding:1.4rem 1rem 3rem;font-size:.82rem;color:var(--mute)}
footer.bot a{color:var(--mute)}
@media print{.hero canvas,header.top,.tinchok{display:none}}
"""


def extras():
    llms = f"""# Chemtrails? It's ice. · เคมเทรล? มันคือน้ำแข็ง

> Why jet trails form, why some stay, and a live forecast of whether planes over a place will leave them. Bilingual English/Thai. By NaNoBotCo.

- [English]({SITE}): the page
- [ไทย]({SITE}th/): Thai edition
- [Trail rule in JavaScript]({SITE}trail.js): Schmidt–Appleman criterion (Schumann 1996), Murphy & Koop vapour pressures

## Numbers on the page (computed by tools/physics.py)
- Water from a narrow-body jet: {F['water_per_km']:.1f} kg per km flown (2,400 kg fuel/h, 830 km/h, 1.23 kg water per kg Jet A)
- Ice in 1 km of an hour-old spreading trail (2 km × 500 m, −50 °C, 120% ice humidity): {n0(F['ice_per_km'])} kg
- Ratio: {n0(F['ratio'])}×
- Trail threshold at 250 hPa (~34,000 ft), η = 0.35: {F['Tdry_250']:.1f} °C dry air, {F['Twet_250']:.1f} °C saturated air
- 76 of 77 atmospheric chemists and geochemists surveyed in 2016 had seen no evidence of secret spraying (Shearer et al., ERL 11:084011)
"""
    open(os.path.join(DOCS, "llms.txt"), "w", encoding="utf-8").write(llms)
    open(os.path.join(DOCS, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}sitemap.xml\n")
    open(os.path.join(DOCS, "sitemap.xml"), "w").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        f"<url><loc>{SITE}</loc></url><url><loc>{SITE}th/</loc></url></urlset>\n")
    open(os.path.join(DOCS, "icon.svg"), "w").write(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#C9485A"/>'
        '<path d="M8 50 L44 18" stroke="#F6EBD6" stroke-width="7" stroke-linecap="round" opacity=".9"/>'
        '<path d="M47 12 l6 3 -3 6 z" fill="#F6EBD6"/><path d="M48 44 l2.4 5.6 5.6 2.4 -5.6 2.4 -2.4 5.6 -2.4 -5.6 -5.6 -2.4 5.6 -2.4z" fill="#D6A42C"/></svg>')


def main():
    global L
    for lang, path in (("en", "index.html"), ("th", "th/index.html")):
        L = lang
        out = os.path.join(DOCS, path)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, "w", encoding="utf-8").write(page())
        print("wrote", out)
    extras()


if __name__ == "__main__":
    main()
