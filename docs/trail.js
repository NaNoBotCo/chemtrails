/* trail.js: the trail rule in the browser. Same formulas as tools/physics.py.
   Schmidt-Appleman criterion as Schumann (1996) wrote it; vapour pressures from Murphy & Koop (2005). */
(function (g) {
  var ln = Math.log, ex = Math.exp;
  function ew(T) { return ex(54.842763 - 6763.22 / T - 4.210 * ln(T) + 0.000367 * T + Math.tanh(0.0415 * (T - 218.8)) * (53.878 - 1331.22 / T - 9.44523 * ln(T) + 0.014025 * T)); }
  function ei(T) { return ex(9.550426 - 5723.265 / T + 3.53068 * ln(T) - 0.00728332 * T); }
  var EI = 1.23, CP = 1004, EPS = 0.622, Q = 43.13e6, ETA = 0.35;
  function G(p, eta) { return EI * CP * p / (EPS * Q * (1 - (eta == null ? ETA : eta))); }
  function dew(T) { return (ew(T + 1e-3) - ew(T - 1e-3)) / 2e-3; }
  function tm(Gv) { var lo = 180, hi = 300; for (var i = 0; i < 60; i++) { var m = (lo + hi) / 2; if (dew(m) > Gv) hi = m; else lo = m; } return (lo + hi) / 2; }
  function threshold(p, u, eta) {
    var Gv = G(p, eta), TM = tm(Gv); if (u >= 1) return TM;
    var eM = ew(TM), lo = TM - 40, hi = TM;
    for (var i = 0; i < 60; i++) { var m = (lo + hi) / 2; if (eM - Gv * (TM - m) > u * ew(m)) hi = m; else lo = m; }
    return (lo + hi) / 2;
  }
  function rhi(T, u) { return u * ew(T) / ei(T); }
  /* T kelvin, p pascals, u = humidity against water 0..1 */
  function verdict(T, p, u, eta) {
    if (T > threshold(p, u, eta)) return "none";
    return rhi(T, u) >= 1 ? "long" : "short";
  }
  g.Trail = { ew: ew, ei: ei, G: G, tm: tm, threshold: threshold, rhi: rhi, verdict: verdict, ETA: ETA };
})(window);
