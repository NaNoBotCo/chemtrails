# -*- coding: utf-8 -*-
"""physics.py: when a jet leaves a trail, and whether the trail stays.

The Schmidt-Appleman rule, as Schumann (1996) wrote it down, plus the ice arithmetic.
docs/sky.js carries the same formulas in JavaScript; tests/test_physics.py checks the two agree.

    python3 tools/physics.py        # prints the numbers the page quotes
"""
import math

# Saturation vapour pressure, Pa, T in kelvin. Murphy & Koop (2005), QJRMS 131:1539.
def e_water(T):
    return math.exp(54.842763 - 6763.22 / T - 4.210 * math.log(T) + 0.000367 * T
                    + math.tanh(0.0415 * (T - 218.8))
                    * (53.878 - 1331.22 / T - 9.44523 * math.log(T) + 0.014025 * T))


def e_ice(T):
    return math.exp(9.550426 - 5723.265 / T + 3.53068 * math.log(T) - 0.00728332 * T)


EI_H2O = 1.23     # kg of water per kg of Jet A burned (pycontrails fuel.py)
CP = 1004.0       # J/(kg K), heat capacity of air
EPS = 0.622       # molar mass of water / molar mass of dry air
Q = 43.13e6       # J/kg, heat released by burning Jet A (pycontrails fuel.py)
ETA = 0.35        # share of that heat that pushes the plane instead of warming the exhaust


def slope(p, eta=ETA):
    """G, Pa/K: how the exhaust plume's vapour pressure falls per degree as it cools
    and mixes into the air around it. A straight line on the vapour-temperature chart."""
    return EI_H2O * CP * p / (EPS * Q * (1 - eta))


def _de_water(T):
    h = 1e-3
    return (e_water(T + h) - e_water(T - h)) / (2 * h)


def t_tangent(G):
    """Where the mixing line just touches the water curve (T_LM, kelvin)."""
    lo, hi = 180.0, 300.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if _de_water(mid) > G:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def threshold(p, rh_w, eta=ETA):
    """T_LC, kelvin: air colder than this makes a trail. rh_w = humidity against water, 0..1."""
    G = slope(p, eta)
    TM = t_tangent(G)
    if rh_w >= 1:
        return TM
    eM = e_water(TM)
    lo, hi = TM - 40.0, TM
    for _ in range(80):
        mid = (lo + hi) / 2
        # the mixing line through (mid, U e_w(mid)) passes below or above the curve's tangent point
        if eM - G * (TM - mid) > rh_w * e_water(mid):
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def rh_ice(T, rh_w):
    return rh_w * e_water(T) / e_ice(T)


def verdict(T, p, rh_w, eta=ETA):
    """'none', 'short' or 'long' for air at T kelvin, p pascals, humidity rh_w against water."""
    if T > threshold(p, rh_w, eta):
        return "none"
    return "long" if rh_ice(T, rh_w) >= 1 else "short"


# ---- the weight of a trail
RV = 461.5  # J/(kg K), gas constant of water vapour


def ice_density(T, rhi):
    """kg of ice per m^3 that can come out of air at T with ice humidity rhi, once a trail
    gives the extra vapour something to freeze onto: everything above saturation."""
    return max(0.0, rhi - 1) * e_ice(T) / (RV * T)


def facts():
    f = {}
    for name, p in (("300", 30000), ("250", 25000), ("200", 20000)):
        f["G_" + name] = slope(p)
        f["Tdry_" + name] = threshold(p, 0) - 273.15
        f["Twet_" + name] = threshold(p, 1) - 273.15
    # a narrow-body cruising: ~2,400 kg of fuel an hour at ~830 km/h over the ground
    burn, speed = 2400.0, 830.0
    f["fuel_per_km"] = burn / speed
    f["water_per_km"] = burn / speed * EI_H2O
    # an hour-old spreading trail: 2 km wide, 500 m deep, at -50 C, 120 % ice humidity
    T, rhi, width, depth = 223.15, 1.20, 2000.0, 500.0
    f["ice_g_m3"] = ice_density(T, rhi) * 1000
    f["ice_per_km"] = ice_density(T, rhi) * width * depth * 1000.0
    f["ratio"] = f["ice_per_km"] / f["water_per_km"]
    f["payload_t"] = 20.0
    f["km_of_trail_per_payload"] = f["payload_t"] * 1000 / f["ice_per_km"] * 1000  # metres
    # the efficiency experiment: the more efficient engine makes trails in warmer air
    f["Tdry_250_eta31"] = threshold(25000, 0, 0.31) - 273.15
    f["Tdry_250_eta23"] = threshold(25000, 0, 0.23) - 273.15
    return f


if __name__ == "__main__":
    for k, v in facts().items():
        print(f"{k:28s} {v:12.3f}")
