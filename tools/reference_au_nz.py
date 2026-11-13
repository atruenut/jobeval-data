#!/usr/bin/env python3
"""Reference arithmetic for AU-2026, NZ-2026 and IE-2026 (own arithmetic from the cited third-party figures; not an
official ATO / IRD run).   python3 tools/reference_au_nz.py --tests   writes tests-src/AU-2026.yaml and NZ-2026.yaml"""
import sys
from decimal import Decimal as D

def marginal(base, rows):  # rows: (starts_at, rate)
    t = D(0)
    for i, (s, r) in enumerate(rows):
        top = min(base, rows[i + 1][0]) if i + 1 < len(rows) else base
        if top > s: t += (top - s) * D(r)
    return t

NZ = [(0, "0.105"), (15600, "0.175"), (53500, "0.30"), (78100, "0.33"), (180000, "0.39")]
AU = [(0, "0"), (18200, "0.15"), (45000, "0.30"), (135000, "0.37"), (190000, "0.45")]

def nz(g):
    g = D(g); return {"nz.tax": marginal(g, NZ), "nz.acc": min(g, D(156641)) * D("0.0175")}

def au(g):
    g = D(g)
    lito = D(700) if g <= 37500 else (D(700) - D("0.05") * (g - 37500) if g <= 45000 else D(325) - D("0.015") * (g - 45000))
    lito = max(D(0), lito)
    med = D(0) if g <= 28011 else min(g * D("0.02"), (g - 28011) * D("0.10"))
    return {"au.lito": lito, "au.tax": max(D(0), marginal(g, AU) - lito), "au.medicare": med}

IE_USC = [(0, "0.005"), (12012, "0.02"), (28700, "0.03"), (70044, "0.08")]
IE_TAX = [(0, "0.20"), (44000, "0.40")]

def ie(g):
    g = D(g); w = g / 52
    usc = D(0) if g <= 13000 else marginal(g, IE_USC)
    prsi = D(0) if w <= 352 else max(D(0), w * D("0.042375") - max(D(0), D(12) - (w - 352) / 6)) * 52
    return {"ie.tax": max(D(0), marginal(g, IE_TAX) - 4000), "ie.usc": usc, "ie.prsi": prsi}

def write(suite, fn, grosses, note):
    cases = ""
    for g in grosses:
        exp = ", ".join(f"{k}: {v.quantize(D('0.001'))}" for k, v in fn(g).items())
        cases += f"  - id: {suite.split('-')[0].lower()}-{g}\n    status: derived\n    inputs: {{ gross_annual: {g}, as_of: 2026-11-13 }}\n    expect: {{ {exp} }}\n"
    open(f"tests-src/{suite}.yaml", "w").write(f"# Golden tests for {suite}.\n# status derived: tools/reference_au_nz.py ({note}; not an official run).\nsuite: {suite}\npack: {suite}\ntolerance: {{ abs: 0.01 }}\ncases:\n{cases}")

if __name__ == "__main__":
    if "--tests" in sys.argv:
        write("NZ-2026", nz, (10000, 15600, 40000, 53500, 80000, 180000, 200000), "own arithmetic from Deloitte and Baker Tilly figures")
        write("IE-2026", ie, (10000, 18304, 20000, 22048, 30000, 44000, 60000, 100000), "own arithmetic from gov.ie, Grant Thornton and BrightPay figures")
        write("AU-2026", au, (15000, 25000, 30000, 37500, 45000, 60000, 66667, 100000, 200000), "own arithmetic from Super Guide figures")
