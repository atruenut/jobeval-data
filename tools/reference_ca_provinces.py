#!/usr/bin/env python3
"""Independent reference for the CA provincial packs (all provinces/territories modelled except NB,
which has tools/reference_ca_nb.py). Written from CRA T4127 (122nd ed.) in its own form, tax =
V x A - KP - credits using the published constants KP, NOT the bracket tables in the pack YAML, so
a typo in either representation shows up as a mismatch. It is our own arithmetic, not an official run.

    python3 tools/reference_ca_provinces.py ON 70000
    python3 tools/reference_ca_provinces.py --tests > tests-src/generated.txt
"""
import sys
from decimal import Decimal as D, ROUND_HALF_UP
sys.path.insert(0, __file__.rsplit("/", 1)[0])
import reference_ca_nb as base

# code: (rows [(A, V, KP)], basic personal amount or None for the federal formula)
T = {
 "BC": ([(0,.0506,0),(50363,.0770,1330),(100728,.1050,4150),(115648,.1229,6220),(140430,.1470,9604),(190405,.1680,13603),(265545,.2050,23428)], 13216),
 "AB": ([(0,.08,0),(61200,.10,1224),(154259,.12,4309),(185111,.13,6160),(246813,.14,8628),(370220,.15,12331)], 22769),
 "SK": ([(0,.105,0),(54532,.125,1091),(155805,.145,4207)], 20381),
 "MB": ([(0,.108,0),(47000,.1275,917),(100000,.174,5567)], 15780),
 "ON": ([(0,.0505,0),(53891,.0915,2210),(107785,.1116,4376),(150000,.1216,5876),(220000,.1316,8076)], 12989),
 "NS": ([(0,.0879,0),(30995,.1495,1909),(61991,.1667,2976),(97417,.1750,3784),(157124,.2100,9283)], 11932),
 "NL": ([(0,.087,0),(44678,.145,2591),(89354,.158,3753),(159528,.178,6943),(223340,.198,11410),(285319,.208,14263),(570638,.213,17117),(1141275,.218,22823)], 11188),
 "YT": ([(0,.064,0),(58523,.09,1522),(117045,.109,3745),(181440,.128,7193),(500000,.15,18193)], None),
 "NT": ([(0,.059,0),(53003,.086,1431),(106009,.122,5247),(172346,.1405,8436)], 18198),
 "PE": ([(0,.095,0),(33928,.1347,1347),(65820,.166,3407),(106890,.1762,4497),(142250,.19,6460),(200000,.20,8460)], 15000),
 "NU": ([(0,.04,0),(55801,.07,1674),(111602,.09,3906),(181439,.115,8442)], 19659),
}


def exact_constants(rows):
    """CRA prints K rounded to whole dollars; the exact constant follows from continuity of the
    schedule: K(n) = K(n-1) + A(n) x (V(n) - V(n-1)). Each printed K must be within a dollar of it."""
    k = [D(0)]
    for i in range(1, len(rows)):
        k.append(k[-1] + D(rows[i][0]) * (D(str(rows[i][1])) - D(str(rows[i - 1][1]))))
        assert abs(k[i] - rows[i][2]) <= D("0.5"), ("printed constant disagrees with thresholds/rates", rows[i])
    return k


OT = {"BC": 40, "AB": 44, "SK": 40, "MB": 40, "ON": 44, "NS": 48, "PE": 48, "NT": 40, "NU": 40}


def calc(code, gross):
    rows, bpa = T[code]
    r = base.calc(gross)
    a = r["taxable"]
    if bpa is None:
        bpa = r["bpa"]  # Yukon uses the federal basic personal amount
    bpa = D(str(bpa))
    if code == "MB":
        bpa = max(D(0), bpa - max(D(0), a - 200000) * D("0.0789"))
    ks = exact_constants(rows)
    idx = max(i for i, (x, v, k) in enumerate(rows) if D(x) < a or x == 0)
    V, KP = D(str(rows[idx][1])), ks[idx]
    credit = D(str(rows[0][1])) * (bpa + r["cpp_base_credit"] + r["ei"])
    tax = max(D(0), V * a - KP - credit)
    out = {"tax": tax}
    if code == "BC":
        red = max(D(0), D(575) - max(D(0), a - 25570) * D("0.0356"))
        out["tax"] = max(D(0), tax - red)
    if code == "ON":
        red = max(D(0), min(tax, 2 * D(300) - tax))
        tax -= red
        out["tax"] = tax
        out["surtax"] = D("0.2") * max(D(0), tax - 5818) + D("0.36") * max(D(0), tax - 7446)
        i = a
        out["health_premium"] = (D(0) if i <= 20000 else min(D(300), D("0.06") * (i - 20000)) if i <= 36000 else
                                 min(D(450), 300 + D("0.06") * (i - 36000)) if i <= 48000 else
                                 min(D(600), 450 + D("0.25") * (i - 48000)) if i <= 72000 else
                                 min(D(750), 600 + D("0.25") * (i - 72000)) if i <= 200000 else
                                 min(D(900), 750 + D("0.25") * (i - 200000)))
    return out


def tests():
    lines = []
    for code in T:
        lc = code.lower()
        lines.append(f"# {code}")
        for g in (12000, 25000, 45000, 70000, 110000, 180000) + ((250000,) if code == "PE" else ()):
            o = calc(code, g)
            exp = ", ".join(f"{lc}.{k}: {v.quantize(D('0.001'), ROUND_HALF_UP)}" for k, v in o.items())
            lines.append(f"  - id: {lc}-tax-{g}\n    status: derived\n    inputs: {{ gross_annual: {g}, as_of: 2026-11-12 }}\n    expect: {{ {exp} }}")
        if code in OT:
            lines.append(f"  - id: {lc}-overtime-statutory\n    status: derived\n    inputs: {{ wage: 20.00, gross_annual: 40000, as_of: 2026-11-12 }}\n    expect: {{ {lc}.overtime_hourly: 30.00, {lc}.overtime_threshold_hours: {OT[code]} }}")
    return lines


if __name__ == "__main__":
    if sys.argv[1] == "--tests":
        print("\n".join(tests()))
    else:
        for k, v in calc(sys.argv[1], sys.argv[2]).items():
            print(k, v.quantize(D("0.001"), ROUND_HALF_UP))
