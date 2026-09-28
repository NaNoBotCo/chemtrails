// planes-overhead: aircraft near a point, for the chemtrails page's live sky.
// GET /?lat=18.79&lon=98.98  ->  {now, src, ac:[{hex,cs,type,lat,lon,alt,gs,trk}]}
// Tries the free community ADS-B feeds in turn and adds the CORS header a browser needs.
const R = 120; // nautical miles
const UA = { "user-agent": "nanobotco-chemtrails/1 (+https://nanobotco.github.io/chemtrails/)" };
const FEEDS = [
  ["adsb.fi (open data)", (la, lo) => `https://opendata.adsb.fi/api/v2/lat/${la}/lon/${lo}/dist/${R}`],
  ["adsb.lol (ODbL)", (la, lo) => `https://api.adsb.lol/v2/point/${la}/${lo}/${R}`],
  ["OpenSky Network", (la, lo) => { const d = R / 60, e = d / Math.max(0.2, Math.cos(la * Math.PI / 180));
    return `https://opensky-network.org/api/states/all?lamin=${(la - d).toFixed(2)}&lamax=${(+la + d).toFixed(2)}&lomin=${(lo - e).toFixed(2)}&lomax=${(+lo + e).toFixed(2)}`; }],
];
// OpenSky rows are arrays: [icao24, callsign, country, tpos, tlast, lon, lat, baro_m, onground, vel_ms, track, vr, sensors, geo_m, ...]
function sky(d) {
  return (d.states || []).filter(s => s[5] != null && s[6] != null && !s[8] && (s[13] != null || s[7] != null))
    .map(s => ({ hex: s[0], cs: (s[1] || "").trim(), type: "", reg: "", lat: +s[6].toFixed(4), lon: +s[5].toFixed(4),
      alt: Math.round((s[13] != null ? s[13] : s[7]) * 3.28084), gs: s[9] != null ? Math.round(s[9] * 1.94384) : null,
      trk: s[10] != null ? Math.round(s[10]) : null }));
}
function trim(list) {
  return (list || []).filter(a => a.lat != null && a.lon != null && typeof a.alt_baro === "number")
    .map(a => ({ hex: a.hex, cs: (a.flight || "").trim(), type: a.t || "", reg: a.r || "",
      lat: +(+a.lat).toFixed(4), lon: +(+a.lon).toFixed(4), alt: a.alt_geom || a.alt_baro,
      gs: a.gs != null ? Math.round(a.gs) : null, trk: a.track != null ? Math.round(a.track) : null }));
}
export default {
  async fetch(req, env, ctx) {
    const cors = { "access-control-allow-origin": "*", "content-type": "application/json; charset=utf-8" };
    if (req.method === "OPTIONS") return new Response(null, { headers: { ...cors, "access-control-allow-methods": "GET" } });
    const u = new URL(req.url);
    const lat = +u.searchParams.get("lat"), lon = +u.searchParams.get("lon");
    if (!u.searchParams.get("lat") || !isFinite(lat) || !isFinite(lon) || Math.abs(lat) > 90 || Math.abs(lon) > 180)
      return new Response(JSON.stringify({ error: "lat and lon please" }), { status: 400, headers: cors });
    // round to ~10 km so neighbours share a cached answer
    const la = lat.toFixed(1), lo = lon.toFixed(1);
    const key = new Request(`https://planes-overhead.cache/${la}/${lo}`);
    const hit = await caches.default.match(key);
    if (hit) return hit;
    const tried = [];
    for (const [name, url] of FEEDS) {
      try {
        const r = await fetch(url(la, lo), { headers: UA });
        if (!r.ok) { tried.push(name + " " + r.status); continue; }
        const d = await r.json();
        const res = new Response(JSON.stringify({ now: d.now || Date.now(), src: name, ac: d.states ? sky(d) : trim(d.ac || d.aircraft) }),
          { headers: { ...cors, "cache-control": "public, max-age=20" } });
        ctx.waitUntil(caches.default.put(key, res.clone()));
        return res;
      } catch (e) { tried.push(name + " " + e); }
    }
    return new Response(JSON.stringify({ error: "feeds busy", tried }), { status: 502, headers: cors });
  },
};
