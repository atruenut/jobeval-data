#!/usr/bin/env python3
"""Reference arithmetic for GB-2026 and GB-SCT-2026 (own arithmetic from the GOV.UK and Scottish
Government figures; not an official HMRC run).  Scottish bands are written in INCOME terms (as
published) and converted to taxable-income terms here, independently of the pack.
    python3 tools/reference_gb.py 80000"""
import sys
from decimal import Decimal as D

PA = D(12570)
RUK = [(D(50270), D("0.20")), (D(125140), D("0.40")), (None, D("0.45"))]      # income limits at full allowance
SCT = [(D(16537), D("0.19")), (D(29526), D("0.20")), (D(43662), D("0.21")), (D(75000), D("0.42")), (D(125140), D("0.45")), (None, D("0.48"))]

def allowance(income):
    return max(D(0), PA - max(D(0), D(income) - 100000) / 2)

def tax(income, bands):
    ti = max(D(0), D(income) - allowance(income)); t = D(0); lo = D(0)
    for limit, rate in bands:
        hi = None if limit is None else (limit - PA if limit != D(125140) else limit)   # 125,140 is already a taxable-income limit
        top = ti if hi is None else min(ti, hi)
        if top > lo: t += (top - lo) * rate
        if hi is not None: lo = hi
    return t

def ni(g):
    g = D(g)
    return max(D(0), min(g, D(50270)) - 12570) * D("0.08") + max(D(0), g - 50270) * D("0.02")

if __name__ == "__main__":
    for g in (sys.argv[1:] or (10000, 25000, 50270, 80000, 110000, 150000)):
        print(g, "ruk", tax(g, RUK), "scot", tax(g, SCT), "ni", ni(g))
