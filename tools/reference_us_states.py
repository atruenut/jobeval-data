#!/usr/bin/env python3
"""Reference arithmetic for the US state packs (flat or zero tax). Own arithmetic from the cited
state figures, not an official calculator run.  python3 tools/reference_us_states.py --tests"""
import sys
from decimal import Decimal as D, ROUND_HALF_UP
# code: (rate, deduction or exemption subtracted from gross income, base)
NONE = ["AK", "FL", "NV", "NH", "SD", "TN", "TX", "WA", "WY"]
FLAT = {"PA": (D("0.0307"), D(0)), "IL": (D("0.0495"), D(2925)), "MI": (D("0.0425"), D(5900)), "KY": (D("0.035"), D(3360)), "GA": (D("0.0499"), D(15000))}
q = lambda x: x.quantize(D("0.001"), ROUND_HALF_UP)
def tax(code, gross):
    if code in NONE: return D(0)
    r, ex = FLAT[code]
    return max(D(0), D(gross) - ex) * r
if __name__ == "__main__":
    for code in NONE + list(FLAT):
        lc = code.lower(); print(f"# {code}")
        for g in (2000, 30000, 80000, 250000):
            print(f"  - id: {lc}-tax-{g}\n    status: derived\n    inputs: {{ gross_annual: {g}, as_of: 2026-11-12 }}\n    expect: {{ {lc}.tax: {q(tax(code, g))} }}")
