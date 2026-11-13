#!/usr/bin/env python3
"""Reference arithmetic for the bracketed US state packs, written from the threshold form
('rate starting at X') used by the source, independently of the pack's up_to tables.
Own arithmetic, not an official calculator run.   python3 tools/reference_us_graduated.py [--tests]"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from decimal import Decimal as D
from us_graduated_data import STATES, FED_STD

def marginal(base, starts):
    tax = D(0)
    for i, (rate, s) in enumerate(starts):
        top = starts[i + 1][1] if i + 1 < len(starts) else base
        top = min(base, top)
        if top > s: tax += rate * (top - s)
    return tax

def tax(code, gross, status=1):
    s = STATES[code]; mfj = status == 2; i = 1 if mfj else 0
    g = D(gross)
    if s.get("fed"):
        fs = FED_STD["mfj" if mfj else ("hoh" if status == 3 else "single")]
        base = max(D(0), g - fs)
    else:
        base = max(D(0), g - D(s.get("std", (0, 0))[i]) - D(s.get("exempt", (0, 0))[i]))
    table = s["mfj"] if (mfj and "mfj" in s) else s["single"]
    t = marginal(base, table) - D(s.get("credit", (0, 0))[i])
    return max(D(0), t)

CASES = [(2000, 1), (30000, 1), (80000, 1), (250000, 1), (80000, 2), (250000, 2)]
if __name__ == "__main__":
    for code in STATES:
        lc = code.lower()
        for g, st in CASES:
            print(code, g, st, tax(code, g, st).quantize(D("0.001")))
