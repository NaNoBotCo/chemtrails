# Chemtrails? It's ice. · เคมเทรล? มันคือน้ำแข็ง

https://nanobotco.github.io/chemtrails/ · Thai: /th/

Why jets leave trails and why some stay, from the Schmidt–Appleman rule (Schumann 1996), with a live
check: the ECMWF upper-air forecast (Open-Meteo) at 400/300/250/200 hPa decides, hour by hour, whether
jets over the reader will leave no trail, a short one, or a long one; the 250 hPa wind moves it.

    python3 tools/art.py      # drawings, docs/img/*.svg (NaN and Beer from tools/cast/)
    python3 tools/build.py    # docs/index.html + docs/th/index.html, llms.txt, sitemap
    python3 tools/card.py     # docs/card.jpg (rsvg-convert, magick)

- `tools/physics.py` and `docs/trail.js` carry the same formulas.
- `worker/` is `planes-overhead`, a Cloudflare Worker that relays community ADS-B feeds with CORS.
  The feeds currently refuse Cloudflare's servers, so the page falls back to the adsb.lol map on a tap.

Text and drawings CC BY 4.0 NaNoBotCo · code MIT · photographs keep their Commons licences.
