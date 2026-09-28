/* live.js: will jets leave trails over you right now?
   Upper-air forecast: Open-Meteo, ECMWF IFS 0.25°, at 400/300/250/200 hPa.
   Planes: planes-overhead relay (community ADS-B feeds) when it answers; the adsb.lol map on a tap.
   Place: the reader's time zone gives a city; "Use my location" gives the device.
   Test hooks: ?ll=18.79,98.98 */
(function () {
  var box = document.getElementById("live"); if (!box || !window.Trail) return;
  var TH = document.documentElement.lang === "th";
  function t(en, th) { return TH ? th : en; }
  var $ = function (id) { return document.getElementById(id); };
  var Q = new URLSearchParams(location.search);
  var RELAY = "https://planes-overhead.nanobotco.workers.dev/";
  var LEV = [400, 300, 250, 200];

  var Z = {
    "Asia/Bangkok": [18.79, 98.98, "Chiang Mai", "เชียงใหม่"], "Asia/Vientiane": [17.97, 102.60, "Vientiane", "เวียงจันทน์"],
    "Asia/Yangon": [16.84, 96.17, "Yangon", "ย่างกุ้ง"], "Asia/Ho_Chi_Minh": [10.82, 106.63, "Ho Chi Minh City", "โฮจิมินห์"],
    "Asia/Phnom_Penh": [11.56, 104.92, "Phnom Penh", "พนมเปญ"], "Asia/Singapore": [1.35, 103.82, "Singapore", "สิงคโปร์"],
    "Asia/Kuala_Lumpur": [3.14, 101.69, "Kuala Lumpur", "กัวลาลัมเปอร์"], "Asia/Tokyo": [35.68, 139.69, "Tokyo", "โตเกียว"],
    "Asia/Shanghai": [31.23, 121.47, "Shanghai", "เซี่ยงไฮ้"], "Asia/Hong_Kong": [22.32, 114.17, "Hong Kong", "ฮ่องกง"],
    "Asia/Kolkata": [28.61, 77.21, "Delhi", "เดลี"], "Asia/Dubai": [25.20, 55.27, "Dubai", "ดูไบ"],
    "Europe/London": [51.51, -0.13, "London", "ลอนดอน"], "Europe/Paris": [48.86, 2.35, "Paris", "ปารีส"],
    "Europe/Berlin": [52.52, 13.40, "Berlin", "เบอร์ลิน"], "Europe/Madrid": [40.42, -3.70, "Madrid", "มาดริด"],
    "America/New_York": [40.71, -74.01, "New York", "นิวยอร์ก"], "America/Chicago": [41.88, -87.63, "Chicago", "ชิคาโก"],
    "America/Denver": [39.74, -104.99, "Denver", "เดนเวอร์"], "America/Phoenix": [33.45, -112.07, "Phoenix", "ฟีนิกซ์"],
    "America/Los_Angeles": [34.05, -118.24, "Los Angeles", "ลอสแองเจลิส"], "America/Vancouver": [49.28, -123.12, "Vancouver", "แวนคูเวอร์"],
    "America/Anchorage": [61.22, -149.9, "Anchorage", "แองเคอเรจ"], "Pacific/Honolulu": [21.31, -157.86, "Honolulu", "โฮโนลูลู"],
    "Australia/Sydney": [-33.87, 151.21, "Sydney", "ซิดนีย์"]
  };
  var tz = ""; try { tz = Intl.DateTimeFormat().resolvedOptions().timeZone || ""; } catch (e) {}
  var here = Z[tz] || Z["Asia/Bangkok"], place = { lat: here[0], lon: here[1], name: t(here[2], here[3]) };
  if (Q.get("ll")) { var ll = Q.get("ll").split(","); place = { lat: +ll[0], lon: +ll[1], name: t("your pin", "จุดที่ปักไว้") }; }

  var WX = null, NOW = 0, PLANES = null, BEAR = 45, animT = 0;

  /* ---- text helpers */
  var CMP = TH ? ["เหนือ", "ตะวันออกเฉียงเหนือ", "ตะวันออก", "ตะวันออกเฉียงใต้", "ใต้", "ตะวันตกเฉียงใต้", "ตะวันตก", "ตะวันตกเฉียงเหนือ"]
    : ["north", "northeast", "east", "southeast", "south", "southwest", "west", "northwest"];
  var CMP2 = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"];
  function cmp(b) { return CMP[Math.round(((b % 360) + 360) % 360 / 45) % 8]; }
  function cmp2(b) { return CMP2[Math.round(((b % 360) + 360) % 360 / 45) % 8]; }
  function ft(m) { return Math.round(m * 3.28084 / 500) * 500; }
  function fmt(n) { return n.toLocaleString(TH ? "th-TH" : "en-US"); }
  var WORD = { long: t("Long trails that stay and spread", "ทางยาว ค้างอยู่และแผ่กว้าง"),
    short: t("Short trails that vanish in seconds", "ทางสั้น หายไปในไม่กี่วินาที"), none: t("No trail", "ไม่มีทาง") };
  var CHIP = { long: t("long", "ยาว"), short: t("short", "สั้น"), none: t("none", "ไม่มี") };

  /* ---- the forecast */
  function wxUrl(model) {
    var v = [];
    LEV.forEach(function (l) { ["temperature", "relative_humidity", "wind_speed", "wind_direction", "geopotential_height"].forEach(function (k) { v.push(k + "_" + l + "hPa"); }); });
    return "https://api.open-meteo.com/v1/forecast?latitude=" + place.lat.toFixed(3) + "&longitude=" + place.lon.toFixed(3) +
      "&hourly=" + v.join(",") + "&forecast_days=2&timezone=auto&wind_speed_unit=kmh" + (model ? "&models=" + model : "");
  }
  function getWx() {
    $("lv-head").textContent = t("Reading the sky over " + place.name + "…", "กำลังอ่านฟ้าเหนือ" + place.name + "…");
    return fetch(wxUrl("ecmwf_ifs025")).then(function (r) { return r.json(); }).then(function (d) {
      if (d.error || !d.hourly) return fetch(wxUrl("")).then(function (r) { return r.json(); });
      return d;
    }).then(function (d) {
      WX = d;
      var local = new Date(Date.now() + d.utc_offset_seconds * 1000).toISOString().slice(0, 13) + ":00";
      NOW = Math.max(0, d.hourly.time.indexOf(local));
      paint();
    }).catch(function () { $("lv-head").textContent = t("The forecast did not answer. Try again in a minute.", "พยากรณ์ไม่ตอบ ลองใหม่อีกสักนาที"); });
  }
  function level(l, i) {
    var h = WX.hourly, k = "_" + l + "hPa";
    var T = h["temperature" + k][i] + 273.15, u = Math.min(1, h["relative_humidity" + k][i] / 100);
    return { l: l, T: T, u: u, rhi: Trail.rhi(T, u), z: h["geopotential_height" + k][i],
      ws: h["wind_speed" + k][i], wd: h["wind_direction" + k][i], v: Trail.verdict(T, l * 100, u),
      thr: Trail.threshold(l * 100, u) };
  }
  /* air at any altitude (m), straight lines between the levels */
  function at(zm, i) {
    var L = LEV.map(function (l) { return level(l, i); });
    if (zm <= L[0].z) return L[0]; if (zm >= L[3].z) return L[3];
    for (var k = 0; k < 3; k++) if (zm <= L[k + 1].z) {
      var a = L[k], b = L[k + 1], f = (zm - a.z) / (b.z - a.z);
      var T = a.T + f * (b.T - a.T), u = a.u + f * (b.u - a.u), p = Math.exp(Math.log(a.l * 100) + f * (Math.log(b.l * 100) - Math.log(a.l * 100)));
      return { T: T, u: u, rhi: Trail.rhi(T, u), v: Trail.verdict(T, p, u), ws: a.ws + f * (b.ws - a.ws), wd: b.wd, z: zm };
    }
  }

  function paint() {
    var c = level(250, NOW);
    $("lv-head").innerHTML = t("Over " + place.name + " right now, jets at about " + fmt(ft(c.z)) + " ft leave:",
      "เหนือ" + place.name + " ตอนนี้ เครื่องบินที่ความสูงราว " + fmt(ft(c.z)) + " ฟุต จะทิ้ง:");
    var v = $("lv-verdict"); v.textContent = WORD[c.v]; v.className = "verdict " + c.v;
    $("lv-why").textContent = t(
      "Air up there: " + (c.T - 273.15).toFixed(0) + " °C, ice humidity " + Math.round(c.rhi * 100) + "%. In this air a jet makes a trail below " + (c.thr - 273.15).toFixed(0) + " °C; the trail stays when ice humidity is 100% or more.",
      "อากาศข้างบน: " + (c.T - 273.15).toFixed(0) + " °C ความชื้นเทียบน้ำแข็ง " + Math.round(c.rhi * 100) + "% อากาศแบบนี้ เครื่องบินจะเกิดทางเมื่อเย็นกว่า " + (c.thr - 273.15).toFixed(0) + " °C และทางจะค้างเมื่อความชื้นเทียบน้ำแข็งถึง 100% ขึ้นไป");
    var rows = [300, 250, 200].map(function (l) {
      var x = level(l, NOW);
      return '<li class="' + x.v + '"><b>' + fmt(ft(x.z)) + ' ' + t("ft", "ฟุต") + '</b><span>' + CHIP[x.v] + '</span><small>' +
        (x.T - 273.15).toFixed(0) + ' °C · ' + Math.round(x.rhi * 100) + '%</small></li>';
    });
    $("lv-levels").innerHTML = rows.join("");
    $("lv-wind").textContent = t("Wind at that height: " + Math.round(c.ws) + " km/h from the " + cmp(c.wd) + ". Every trail up there slides toward the " + cmp(c.wd + 180) + ".",
      "ลมที่ความสูงนั้น: " + Math.round(c.ws) + " กม./ชม. พัดมาจากทิศ" + cmp(c.wd) + " ทุกทางบนนั้นจะเลื่อนไปทางทิศ" + cmp(c.wd + 180));
    strip(); next(); bearing(); drawMap();
  }

  /* 48 hours, three heights */
  function strip() {
    var h = WX.hourly, n = h.time.length, out = "";
    [200, 250, 300].forEach(function (l) {
      var z = ft(level(l, NOW).z), cells = "";
      for (var i = 0; i < n; i++) {
        var x = level(l, i), hr = +h.time[i].slice(11, 13);
        cells += '<i class="' + x.v + (i === NOW ? " now" : "") + '" title="' + h.time[i].replace("T", " ") + " · " + CHIP[x.v] + '"></i>';
      }
      out += '<div class="row"><b>' + fmt(z) + '</b><div class="cells">' + cells + '</div></div>';
    });
    var ticks = "";
    for (var i = 0; i < n; i++) { var hr = +h.time[i].slice(11, 13); ticks += "<i>" + (hr % 6 === 0 ? hr + ":00" : "") + "</i>"; }
    out += '<div class="row ticks"><b></b><div class="cells">' + ticks + "</div></div>";
    $("lv-strip").innerHTML = out;
  }
  function next() {
    var h = WX.hourly, cur = level(250, NOW).v, el = $("lv-next");
    for (var i = NOW + 1; i < h.time.length; i++) {
      var v = level(250, i).v;
      if (v !== cur) {
        var when = h.time[i].replace("T", " ");
        el.textContent = t("It changes at " + when + ": " + WORD[v].toLowerCase() + ". Look up then and check.",
          "จะเปลี่ยนตอน " + when + ": " + WORD[v] + " ถึงเวลานั้นลองแหงนดู");
        return;
      }
    }
    el.textContent = t("No change in the next " + (h.time.length - NOW) + " hours.", "ไม่เปลี่ยนใน " + (h.time.length - NOW) + " ชั่วโมงข้างหน้า");
  }

  /* ---- a trail's bearing and where the wind takes it */
  function bearing() {
    var c = level(250, NOW), to = (c.wd + 180) * Math.PI / 180, b = BEAR * Math.PI / 180;
    /* wind toward (east, north) and the trail's direction; only the part across the trail shows */
    var we = Math.sin(to) * c.ws, wn = Math.cos(to) * c.ws, ue = Math.sin(b), un = Math.cos(b);
    var across = Math.abs(we * un - wn * ue), along = Math.abs(we * ue + wn * un);
    var side = (we * un - wn * ue) > 0 ? BEAR + 90 : BEAR - 90;
    $("lv-bear-out").textContent = t(
      "A trail running " + cmp2(BEAR) + "–" + cmp2(BEAR + 180) + " here slides " + Math.round(across) + " km/h toward the " + cmp(side) + ". In an hour it lies " + Math.round(across) + " km to the side of where the plane drew it. The other " + Math.round(along) + " km/h of wind runs along the trail, so you cannot see it.",
      "ทางที่วิ่งแนว " + cmp(BEAR) + "–" + cmp(BEAR + 180) + " ตรงนี้จะเลื่อนไปทางทิศ" + cmp(side) + " " + Math.round(across) + " กม./ชม. หนึ่งชั่วโมงผ่านไป ทางจะอยู่ห่างจากที่เครื่องบินวาดไว้ " + Math.round(across) + " กม. ลมอีก " + Math.round(along) + " กม./ชม. พัดไปตามแนวทาง เลยมองไม่เห็น");
    $("lv-bear-val").textContent = cmp2(BEAR) + "–" + cmp2(BEAR + 180);
  }

  /* ---- the map: seen from above, north up, 150 km around you */
  var cv = $("lv-map"), cx = cv.getContext("2d"), dpr = Math.min(window.devicePixelRatio || 1, 2), S = 0, RKM = 150;
  function sizeMap() { S = cv.getBoundingClientRect().width; cv.width = cv.height = S * dpr; cx.setTransform(dpr, 0, 0, dpr, 0, 0); }
  function xy(e, n) { var k = S / 2 / RKM; return [S / 2 + e * k, S / 2 - n * k]; }
  function drawPlane(x, y, trk, col) {
    cx.save(); cx.translate(x, y); cx.rotate((trk - 90) * Math.PI / 180); cx.scale(.42, .42); cx.fillStyle = col;
    cx.beginPath(); cx.moveTo(-30, -4); cx.lineTo(24, -4); cx.quadraticCurveTo(36, 0, 24, 4); cx.lineTo(-30, 4); cx.closePath();
    cx.moveTo(2, -3); cx.lineTo(-12, -30); cx.lineTo(-19, -30); cx.lineTo(-10, -3); cx.closePath();
    cx.moveTo(2, 3); cx.lineTo(-12, 30); cx.lineTo(-19, 30); cx.lineTo(-10, 3); cx.closePath();
    cx.moveTo(-24, -2); cx.lineTo(-33, -12); cx.lineTo(-36, -12); cx.lineTo(-31, -2); cx.closePath();
    cx.moveTo(-24, 2); cx.lineTo(-33, 12); cx.lineTo(-36, 12); cx.lineTo(-31, 2); cx.closePath(); cx.fill(); cx.restore();
  }
  function trailPath(e0, n0, trk, kmh, mins, c, ph) {
    /* the plane flew along trk; a minute-old piece sits back along the track, pushed downwind */
    var b = trk * Math.PI / 180, to = (c.wd + 180) * Math.PI / 180, pts = [];
    for (var m = 0; m <= mins; m += mins / 30) {
      var back = kmh * m / 60, dr = c.ws * (m + ph) / 60;
      pts.push([e0 - Math.sin(b) * back + Math.sin(to) * dr, n0 - Math.cos(b) * back + Math.cos(to) * dr, m]);
    }
    return pts;
  }
  function stroke(pts, kind) {
    for (var j = 1; j < pts.length; j++) {
      var a = xy(pts[j - 1][0], pts[j - 1][1]), b = xy(pts[j][0], pts[j][1]), age = pts[j][2];
      var wkm = kind === "long" ? .4 + age / 60 * 3 : .3;
      cx.lineWidth = Math.max(1.4, wkm * S / 2 / RKM); cx.lineCap = "round";
      cx.strokeStyle = "rgba(255,248,236," + (kind === "long" ? Math.max(.25, .9 - age / 90) : .8) + ")";
      cx.beginPath(); cx.moveTo(a[0], a[1]); cx.lineTo(b[0], b[1]); cx.stroke();
    }
  }
  function drawMap() {
    if (!WX) return;
    if (!S) sizeMap();
    cx.clearRect(0, 0, S, S);
    var g = cx.createRadialGradient(S / 2, S / 2, 10, S / 2, S / 2, S / 2);
    g.addColorStop(0, "#34488A"); g.addColorStop(1, "#1E2C57");
    cx.fillStyle = g; cx.beginPath(); cx.arc(S / 2, S / 2, S / 2, 0, 7); cx.fill();
    cx.save(); cx.beginPath(); cx.arc(S / 2, S / 2, S / 2 - 1, 0, 7); cx.clip();
    cx.strokeStyle = "rgba(246,235,214,.18)"; cx.lineWidth = 1;
    [50, 100].forEach(function (r) { cx.beginPath(); cx.arc(S / 2, S / 2, r * S / 2 / RKM, 0, 7); cx.stroke(); });
    var c = level(250, NOW), ph = animT;
    /* the bearing you set: one long trail through the middle, drifting */
    var b = BEAR * Math.PI / 180, to = (c.wd + 180) * Math.PI / 180, d = c.ws * ph / 60, L = 180;
    var ox = Math.sin(to) * d, oy = Math.cos(to) * d;
    var p0 = xy(-Math.sin(b) * L + ox, -Math.cos(b) * L + oy), p1 = xy(Math.sin(b) * L + ox, Math.cos(b) * L + oy);
    cx.strokeStyle = "rgba(214,164,44,.9)"; cx.lineWidth = Math.max(2, (.4 + ph / 60 * 3) * S / 2 / RKM); cx.lineCap = "round";
    cx.setLineDash([2, 0]); cx.beginPath(); cx.moveTo(p0[0], p0[1]); cx.lineTo(p1[0], p1[1]); cx.stroke();
    /* real planes, when the relay answers */
    if (PLANES) PLANES.forEach(function (a) {
      if (a.trk == null) return;
      var e = (a.lon - place.lon) * 111.32 * Math.cos(place.lat * Math.PI / 180), n = (a.lat - place.lat) * 110.57;
      var air = at(a.alt / 3.28084, NOW), kmh = (a.gs || 450) * 1.852;
      if (a.alt > 18000 && air.v !== "none") stroke(trailPath(e, n, a.trk, kmh, air.v === "long" ? 40 : .6, air, 0), air.v);
      var p = xy(e, n); drawPlane(p[0], p[1], a.trk, a.alt > 18000 ? "#FFF8EC" : "rgba(255,248,236,.45)");
    });
    cx.restore();
    /* compass and you */
    cx.fillStyle = "#F6EBD6"; cx.font = "700 13px " + getComputedStyle(document.body).fontFamily; cx.textAlign = "center"; cx.textBaseline = "middle";
    [["N", "น", 0], ["E", "ออ", 90], ["S", "ต", 180], ["W", "ตก", 270]].forEach(function (q) {
      var a = q[2] * Math.PI / 180, r = S / 2 - 14; cx.fillText(TH ? q[1] : q[0], S / 2 + Math.sin(a) * r, S / 2 - Math.cos(a) * r);
    });
    cx.fillStyle = "#E7507A"; cx.beginPath(); cx.arc(S / 2, S / 2, 6, 0, 7); cx.fill();
    cx.strokeStyle = "#FFF8EC"; cx.lineWidth = 2; cx.stroke();
    /* wind arrow, top left */
    var ax = 34, ay = 34, wa = to;
    cx.save(); cx.translate(ax, ay); cx.rotate(wa); cx.strokeStyle = "#D6A42C"; cx.fillStyle = "#D6A42C"; cx.lineWidth = 3;
    cx.beginPath(); cx.moveTo(0, 14); cx.lineTo(0, -10); cx.stroke(); cx.beginPath(); cx.moveTo(0, -16); cx.lineTo(-6, -6); cx.lineTo(6, -6); cx.fill(); cx.restore();
  }
  var running = false, still = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  function loop(ms) {
    animT = (ms / 1000 * 8) % 60;  /* an hour of drift every 7.5 seconds */
    drawMap();
    if (running) requestAnimationFrame(loop);
  }
  if ("IntersectionObserver" in window && !still) new IntersectionObserver(function (es) {
    var on = es[0].isIntersecting; if (on && !running) { running = true; requestAnimationFrame(loop); } else if (!on) running = false;
  }).observe(cv);
  else animT = 30;

  $("lv-bear").addEventListener("input", function () { BEAR = +this.value; if (WX) { bearing(); drawMap(); } });
  addEventListener("resize", function () { S = 0; drawMap(); }, { passive: true });

  /* ---- planes */
  function getPlanes() {
    var el = $("lv-planes");
    fetch(RELAY + "?lat=" + place.lat.toFixed(2) + "&lon=" + place.lon.toFixed(2)).then(function (r) { return r.json(); }).then(function (d) {
      if (!d.ac) throw 0;
      PLANES = d.ac.filter(function (a) { return a.alt > 18000; }).sort(function (a, b) { return b.alt - a.alt; });
      if (!PLANES.length) { el.textContent = t("No jets above 18,000 ft within 220 km just now.", "ตอนนี้ไม่มีเครื่องบินสูงเกิน 18,000 ฟุตในรัศมี 220 กม."); return; }
      el.innerHTML = "<ul>" + PLANES.slice(0, 12).map(function (a) {
        var air = WX ? at(a.alt / 3.28084, NOW) : null;
        return "<li><b>" + (a.cs || a.hex) + "</b> " + (a.type || "") + " · " + fmt(Math.round(a.alt / 100) * 100) + " " + t("ft", "ฟุต") +
          " · " + t("heading ", "มุ่งหน้า") + cmp(a.trk) + (air ? ' <span class="chip ' + air.v + '">' + CHIP[air.v] + "</span>" : "") + "</li>";
      }).join("") + "</ul><p class=\"small mute\">" + t("Positions: ", "ตำแหน่ง: ") + d.src + "</p>";
      drawMap();
    }).catch(function () {
      el.textContent = t("The free plane feeds are busy. Open the live map below to see every plane near you, with its height.",
        "ฟีดเครื่องบินฟรีไม่ว่าง เปิดแผนที่สดด้านล่างเพื่อดูเครื่องบินทุกลำใกล้คุณพร้อมความสูง");
    });
  }
  $("lv-radar").addEventListener("click", function () {
    var f = document.createElement("iframe");
    f.src = "https://adsb.lol/?lat=" + place.lat.toFixed(3) + "&lon=" + place.lon.toFixed(3) + "&zoom=8&hideSidebar&hideButtons";
    f.title = t("Live planes near you, adsb.lol", "เครื่องบินสดใกล้คุณ adsb.lol"); f.loading = "lazy";
    this.replaceWith(f);
  });

  /* ---- where */
  $("lv-here").addEventListener("click", function () {
    var b = this; if (!navigator.geolocation) return;
    b.disabled = true;
    navigator.geolocation.getCurrentPosition(function (p) {
      place = { lat: p.coords.latitude, lon: p.coords.longitude, name: t("you", "ที่คุณอยู่") };
      b.hidden = true; PLANES = null; getWx().then(getPlanes);
    }, function () { b.disabled = false; }, { maximumAge: 6e5, timeout: 15000 });
  });

  getWx().then(getPlanes);
})();
