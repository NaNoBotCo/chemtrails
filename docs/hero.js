/* hero.js: jets crossing a rose sky. Three layers of air: in one the trail stays and
   spreads, in one it melts back in seconds, in one there is none. Same planes, same fuel. */
(function () {
  var cv = document.getElementById("hero-sky"); if (!cv) return;
  var cx = cv.getContext("2d"), dpr = Math.min(window.devicePixelRatio || 1, 2);
  var still = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var W, H, planes = [], last = 0, clock = 0, wind = { x: 9, y: 2.5 };
  var LAYERS = [{ kind: "long", y: .16 }, { kind: "short", y: .34 }, { kind: "none", y: .5 }];
  function size() {
    var r = cv.getBoundingClientRect(); W = r.width; H = r.height;
    cv.width = W * dpr; cv.height = H * dpr; cx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }
  function spawn(i, t0) {
    var L = LAYERS[i], dir = Math.random() < .5 ? 1 : -1, ang = (Math.random() - .5) * .5;
    var sp = Math.max(W, 700) / (13 + Math.random() * 5);
    var p = { kind: L.kind, x: dir > 0 ? -60 : W + 60, y: H * (L.y + (Math.random() - .5) * .1),
      vx: dir * sp * Math.cos(ang), vy: sp * Math.sin(ang), s: .8 + (1 - L.y) * .5, pts: [], born: t0 };
    return p;
  }
  function drawPlane(p) {
    var a = Math.atan2(p.vy, p.vx);
    cx.save(); cx.translate(p.x, p.y); cx.rotate(a); cx.scale(p.s, p.s); cx.fillStyle = "#FFF8EC";
    cx.beginPath(); cx.moveTo(-30, -3.5); cx.lineTo(22, -3.5); cx.quadraticCurveTo(34, 0, 22, 3.5); cx.lineTo(-30, 3.5); cx.quadraticCurveTo(-34, 0, -30, -3.5); cx.fill();
    cx.beginPath(); cx.moveTo(2, -3); cx.lineTo(-12, -30); cx.lineTo(-18, -30); cx.lineTo(-10, -3); cx.closePath();
    cx.moveTo(2, 3); cx.lineTo(-12, 30); cx.lineTo(-18, 30); cx.lineTo(-10, 3); cx.closePath();
    cx.moveTo(-24, -2); cx.lineTo(-32, -12); cx.lineTo(-35, -12); cx.lineTo(-31, -2); cx.closePath();
    cx.moveTo(-24, 2); cx.lineTo(-32, 12); cx.lineTo(-35, 12); cx.lineTo(-31, 2); cx.closePath(); cx.fill();
    cx.restore();
  }
  function step(dt, t) {
    for (var i = 0; i < planes.length; i++) {
      var p = planes[i];
      p.x += p.vx * dt; p.y += p.vy * dt;
      if (p.kind !== "none" && p.x > -40 && p.x < W + 40) {
        var a = Math.atan2(p.vy, p.vx), gap = 26 * p.s;   /* clear air right behind the engines */
        p.pts.push({ x: p.x - Math.cos(a) * gap, y: p.y - Math.sin(a) * gap, t: t });
      }
      for (var j = 0; j < p.pts.length; j++) { p.pts[j].x += wind.x * dt; p.pts[j].y += wind.y * dt; }
      var life = p.kind === "short" ? 1.6 : 60;
      while (p.pts.length && t - p.pts[0].t > life) p.pts.shift();
    }
    planes = planes.filter(function (p) { return p.pts.length || (p.x > -200 && p.x < W + 200); });
    LAYERS.forEach(function (L, i) {
      var live = planes.filter(function (p) { return p.kind === L.kind && p.x > -100 && p.x < W + 100; }).length;
      if (!live && Math.random() < dt * .5) planes.push(spawn(i, t));
    });
  }
  function draw(t) {
    cx.clearRect(0, 0, W, H);
    cx.save(); cx.beginPath(); cx.rect(0, 0, W, H * .8); cx.clip();
    planes.forEach(function (p) {
      var n = p.pts.length; if (n < 2) return;
      for (var j = 1; j < n; j++) {
        var q = p.pts[j], r = p.pts[j - 1], age = t - q.t;
        var w = p.kind === "short" ? 2.2 * p.s * (1 - age / 1.6) + .3 : (1.6 + age * .9) * p.s;
        var op = p.kind === "short" ? .85 * (1 - age / 1.6) : Math.max(0, .9 - age / 70);
        cx.strokeStyle = "rgba(255,248,236," + op.toFixed(3) + ")"; cx.lineWidth = Math.max(.5, w); cx.lineCap = "round";
        cx.beginPath(); cx.moveTo(r.x, r.y); cx.lineTo(q.x, q.y); cx.stroke();
      }
    });
    planes.forEach(drawPlane);
    cx.restore();
  }
  function frame(ms) {
    var t = ms / 1000, dt = Math.min(.05, last ? t - last : .016); last = t; clock += dt;
    step(dt, clock); draw(clock);
    if (!document.hidden) requestAnimationFrame(frame); else last = 0;
  }
  size(); addEventListener("resize", size, { passive: true });
  LAYERS.forEach(function (L, i) { var p = spawn(i, 0); p.x = W * (.25 + i * .25); planes.push(p); });
  if (still) {           /* one settled picture: run the clock forward without drawing */
    for (var k = 0; k < 600; k++) step(1 / 60, k / 60);
    draw(600 / 60);
    return;
  }
  document.addEventListener("visibilitychange", function () { if (!document.hidden) requestAnimationFrame(frame); });
  requestAnimationFrame(frame);
})();
