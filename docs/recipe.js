/* recipe.js: make a trail yourself. Set the air, pick the height and the engine,
   and the same rule the forecast uses decides what the plane leaves behind. */
(function () {
  var root = document.getElementById("recipe"); if (!root || !window.Trail) return;
  var TH = document.documentElement.lang === "th";
  function t(en, th) { return TH ? th : en; }
  var $ = function (id) { return document.getElementById(id); };
  var inT = $("rc-t"), inH = $("rc-h"), inP = $("rc-p"), inE = $("rc-e");
  var sc = $("rc-scene"), sx = sc.getContext("2d"), ch = $("rc-chart"), cx = ch.getContext("2d");
  var dpr = Math.min(window.devicePixelRatio || 1, 2), still = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var state = {}, pts = [], px = -60, last = 0;
  var WORD = { long: t("A long trail. It stays, and spreads.", "ทางยาว ค้างอยู่และแผ่กว้าง"),
    short: t("A short trail. Gone in seconds.", "ทางสั้น หายไปในไม่กี่วินาที"), none: t("No trail at all.", "ไม่มีทางเลย") };

  function read() {
    var T = +inT.value + 273.15, rhi = +inH.value / 100, p = +inP.value * 100, eta = +inE.value;
    var u = rhi * Trail.ei(T) / Trail.ew(T), capped = u > 1; if (capped) u = 1;
    state = { T: T, rhi: capped ? Trail.rhi(T, 1) : rhi, u: u, p: p, eta: eta, v: Trail.verdict(T, p, u, eta), thr: Trail.threshold(p, u, eta), capped: capped };
    $("rc-t-out").textContent = inT.value + " °C";
    $("rc-h-out").textContent = Math.round(state.rhi * 100) + "%";
    $("rc-p-out").textContent = { 300: "30,000", 250: "34,000", 200: "39,000" }[inP.value] + t(" ft", " ฟุต");
    $("rc-e-out").textContent = { "0.2": t("1960s", "ยุค 1960"), "0.3": t("1990s", "ยุค 1990"), "0.4": t("newest", "รุ่นใหม่ล่าสุด") }[inE.value];
    var v = $("rc-verdict"); v.textContent = WORD[state.v]; v.className = "verdict " + state.v;
    $("rc-why").textContent = state.v === "none"
      ? t("The exhaust never gets wet enough to make droplets. Trails form here only below " + (state.thr - 273.15).toFixed(1) + " °C.",
          "ไอเสียไม่ชื้นพอจะเป็นหยดน้ำ ที่นี่ทางจะเกิดเมื่อเย็นกว่า " + (state.thr - 273.15).toFixed(1) + " °C เท่านั้น")
      : state.v === "short"
        ? t("Droplets form and freeze, then the dry air takes the ice back. Ice humidity has to reach 100% for the trail to stay.",
            "เกิดหยดน้ำแล้วแข็งตัว แต่อากาศแห้งดึงน้ำแข็งกลับไป ความชื้นเทียบน้ำแข็งต้องถึง 100% ทางถึงจะค้าง")
        : t("The air already holds more water than ice can stand. The trail's crystals pull it out of the air and grow.",
            "อากาศมีน้ำมากเกินกว่าที่น้ำแข็งจะทนได้อยู่แล้ว ผลึกในทางดึงน้ำออกจากอากาศแล้วโตขึ้น");
    if (state.capped) $("rc-why").textContent += " " + t("(Air cannot hold more than water saturation, so humidity stops there.)", "(อากาศถือน้ำได้ไม่เกินจุดอิ่มตัวเทียบน้ำ ความชื้นเลยหยุดตรงนั้น)");
    chart();
  }

  function size(c, g, ratio) { var w = c.getBoundingClientRect().width; c.width = w * dpr; c.height = w * ratio * dpr; g.setTransform(dpr, 0, 0, dpr, 0, 0); return [w, w * ratio]; }
  var SW, SH, CW, CH;
  function sizes() { var a = size(sc, sx, .42); SW = a[0]; SH = a[1]; var b = size(ch, cx, .62); CW = b[0]; CH = b[1]; }

  /* the vapour-temperature chart with your air and your exhaust line */
  function chart() {
    var L = 46, R = CW - 12, T = 14, B = CH - 34, t0 = -70, t1 = -25, e1 = 90;
    function X(c) { return L + (c - t0) / (t1 - t0) * (R - L); } function Y(e) { return B - e / e1 * (B - T); }
    cx.clearRect(0, 0, CW, CH); cx.fillStyle = "#283A6E"; cx.fillRect(0, 0, CW, CH);
    cx.font = "12px " + getComputedStyle(document.body).fontFamily; cx.fillStyle = "rgba(246,235,214,.8)"; cx.textAlign = "center";
    for (var c = -70; c <= -25; c += 5) { cx.fillText(c + "°", X(c), B + 18); cx.fillStyle = "rgba(255,255,255,.07)"; cx.fillRect(X(c), T, 1, B - T); cx.fillStyle = "rgba(246,235,214,.8)"; }
    cx.textAlign = "right"; for (var e = 0; e <= 90; e += 30) cx.fillText(e, L - 6, Y(e) + 4);
    function curve(f, col, dash, w) {
      cx.beginPath(); cx.setLineDash(dash); cx.strokeStyle = col; cx.lineWidth = w;
      for (var i = 0; i <= 200; i++) { var c2 = t0 + i * (t1 - t0) / 200, v = f(c2 + 273.15); if (v > e1) break; i ? cx.lineTo(X(c2), Y(v)) : cx.moveTo(X(c2), Y(v)); }
      cx.stroke(); cx.setLineDash([]);
    }
    curve(Trail.ew, "#D6A42C", [], 3.5); curve(Trail.ei, "#EE9496", [7, 5], 2.5);
    var Tc = state.T - 273.15, ea = state.u * Trail.ew(state.T), G = Trail.G(state.p, state.eta), x2 = Math.min(t1, Tc + (e1 - ea) / G);
    var col = state.v === "none" ? "#8FA4D8" : "#FFF8EC";
    cx.strokeStyle = col; cx.lineWidth = 2.5; cx.beginPath(); cx.moveTo(X(Tc), Y(ea)); cx.lineTo(X(x2), Y(ea + G * (x2 - Tc))); cx.stroke();
    cx.fillStyle = col; cx.beginPath(); cx.arc(X(Tc), Y(ea), 7, 0, 7); cx.fill();
    cx.textAlign = "left"; cx.fillStyle = "#D6A42C"; cx.font = "700 12px " + getComputedStyle(document.body).fontFamily;
    cx.fillText(t("water", "น้ำ"), X(-33), Y(Trail.ew(240.15)) - 8);
    cx.fillStyle = "#EE9496"; cx.fillText(t("ice", "น้ำแข็ง"), X(-29), Y(Trail.ei(244.15)) + 18);
    cx.fillStyle = "#FFF8EC"; cx.fillText(t("your air", "อากาศของคุณ"), X(Tc) + 10, Y(ea) + 16);
  }

  /* the scene: one plane, flat sky, the trail the rule allows */
  function scene(t) {
    sx.clearRect(0, 0, SW, SH);
    var g = sx.createLinearGradient(0, 0, 0, SH); g.addColorStop(0, "#B83A55"); g.addColorStop(1, "#EE9496");
    sx.fillStyle = g; sx.fillRect(0, 0, SW, SH);
    var y = SH * .42, k = SW / 700;
    for (var j = 1; j < pts.length; j++) {
      var a = pts[j - 1], b = pts[j], age = t - b.t;
      var w = state.v === "short" ? 3 * k * Math.max(0, 1 - age / 1.2) : (2 + age * 2.2) * k;
      var op = state.v === "short" ? .85 * Math.max(0, 1 - age / 1.2) : Math.max(.15, .92 - age / 18);
      sx.strokeStyle = "rgba(255,248,236," + op.toFixed(3) + ")"; sx.lineWidth = Math.max(.5, w); sx.lineCap = "round";
      sx.beginPath(); sx.moveTo(a.x, a.y); sx.lineTo(b.x, b.y); sx.stroke();
    }
    sx.save(); sx.translate(px, y); sx.scale(k * 1.1, k * 1.1); sx.fillStyle = "#FFF8EC";
    sx.beginPath(); sx.moveTo(-30, -3.5); sx.lineTo(22, -3.5); sx.quadraticCurveTo(34, 0, 22, 3.5); sx.lineTo(-30, 3.5); sx.closePath();
    sx.moveTo(2, -3); sx.lineTo(-12, -30); sx.lineTo(-18, -30); sx.lineTo(-10, -3); sx.closePath();
    sx.moveTo(2, 3); sx.lineTo(-12, 30); sx.lineTo(-18, 30); sx.lineTo(-10, 3); sx.closePath();
    sx.moveTo(-24, -2); sx.lineTo(-32, -12); sx.lineTo(-35, -12); sx.lineTo(-31, -2); sx.closePath();
    sx.moveTo(-24, 2); sx.lineTo(-32, 12); sx.lineTo(-35, 12); sx.lineTo(-31, 2); sx.closePath(); sx.fill(); sx.restore();
  }
  function step(dt, t) {
    var k = SW / 700; px += SW / 7 * dt;
    if (px > SW + 80) { px = -60; pts = []; }
    if (state.v !== "none") pts.push({ x: px - 30 * k, y: SH * .42, t: t });
    for (var j = 0; j < pts.length; j++) pts[j].y += 3 * k * dt;            /* a slow sink and drift */
    var life = state.v === "short" ? 1.2 : 30;
    while (pts.length && t - pts[0].t > life) pts.shift();
  }
  var clock = 0, running = false;
  function frame(ms) {
    var s = ms / 1000, dt = Math.min(.05, last ? s - last : .016); last = s; clock += dt;
    step(dt, clock); scene(clock); if (running) requestAnimationFrame(frame); else last = 0;
  }
  [inT, inH, inP, inE].forEach(function (el) { el.addEventListener("input", function () { read(); pts = []; px = -60; if (still) settle(); }); });
  function settle() { pts = []; px = -60; for (var i = 0; i < 300; i++) step(1 / 60, i / 60); scene(300 / 60); }
  addEventListener("resize", function () { sizes(); read(); if (still) settle(); }, { passive: true });
  sizes(); read();
  if (still) { settle(); return; }
  if ("IntersectionObserver" in window) new IntersectionObserver(function (es) {
    var on = es[0].isIntersecting; if (on && !running) { running = true; requestAnimationFrame(frame); } else if (!on) running = false;
  }).observe(sc);
  else { running = true; requestAnimationFrame(frame); }
})();
