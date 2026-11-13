#!/usr/bin/env python3
"""Reference arithmetic for DE-2026 (own, from section 32a EStG and the cited third-party figures; not an
official BMF Lohnsteuer run).  python3 tools/reference_de.py --tests"""
import sys
from decimal import Decimal as D

def tariff(x):
    x = D(x)
    if x <= 12348: return D(0)
    if x <= 17799:
        y = (x - 12348) / 10000; return (D("914.51") * y + 1400) * y
    if x <= 69878:
        z = (x - 17799) / 10000; return (D("173.1") * z + 2397) * z + D("1034.87")
    if x <= 277825: return D("0.42") * x - D("11135.63")
    return D("0.45") * x - D("19470.38")

def de(g, children=1):
    g = D(g)
    pen = min(g, D(101400)) * D("0.093"); unemp = min(g, D(101400)) * D("0.013")
    health = min(g, D(69750)) * D("0.0875")
    care = min(g, D(69750)) * (D("0.018") + (D("0.006") if children == 2 else 0))
    zve = max(D(0), g - 1230 - pen - health - care)
    tax = tariff(zve)
    soli = min(D("0.055") * tax, max(D(0), D("0.119") * (tax - 20350)))
    return {"de.pension": pen, "de.unemployment": unemp, "de.health": health, "de.care": care, "de.zve": zve, "de.tax": tax, "de.soli": soli}

if __name__ == "__main__" and "--tests" in sys.argv:
    cases = ""
    for g, c in ((9000, 1), (20000, 1), (35000, 2), (60000, 1), (80000, 2), (120000, 1), (400000, 1)):
        exp = ", ".join(f"{k}: {v.quantize(D('0.001'))}" for k, v in de(g, c).items())
        cases += f"  - id: de-{g}-c{c}\n    status: derived\n    inputs: {{ gross_annual: {g}, children: {c}, as_of: 2026-11-13 }}\n    expect: {{ {exp} }}\n"
    open("tests-src/DE-2026.yaml", "w").write("# Golden tests for DE-2026.\n# status derived: tools/reference_de.py (own arithmetic from section 32a and cited figures; not an official run).\nsuite: DE-2026\npack: DE-2026\ntolerance: { abs: 0.01 }\ncases:\n" + cases)
